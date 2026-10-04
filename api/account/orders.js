// GET /api/account/orders
// The signed-in person's Shopify orders (newest first) with items, status timeline, tracking and address.
const { send, env, currentUser, getProfile, shopify } = require('../_account');

const Q = `query($id:ID!){customer(id:$id){
  firstName numberOfOrders
  orders(first:20,sortKey:PROCESSED_AT,reverse:true){nodes{
    id name processedAt cancelledAt closedAt
    displayFinancialStatus displayFulfillmentStatus
    totalPriceSet{shopMoney{amount currencyCode}}
    subtotalPriceSet{shopMoney{amount}}
    totalShippingPriceSet{shopMoney{amount}}
    totalTaxSet{shopMoney{amount}}
    totalDiscountsSet{shopMoney{amount}}
    totalRefundedSet{shopMoney{amount}}
    shippingAddress{name address1 address2 city provinceCode zip}
    shippingLine{title}
    lineItems(first:10){nodes{title variantTitle quantity image{url altText}
      originalUnitPriceSet{shopMoney{amount}}}}
    fulfillments(first:5){status displayStatus createdAt updatedAt estimatedDeliveryAt inTransitAt deliveredAt
      trackingInfo{company number url}
      events(first:20,sortKey:HAPPENED_AT){nodes{status happenedAt}}}
    events(first:30){nodes{message createdAt}}
  }}}}`;

const addr = a => a ? [a.name, a.address1, a.address2, [a.city, a.provinceCode, a.zip].filter(Boolean).join(' ')].filter(Boolean) : null;

module.exports = async (req, res) => {
  if (req.method !== 'GET') return send(res, 405, { error: 'GET only' });
  const e = env();
  if (e.missing.length) return send(res, 503, { error: 'Accounts are not configured yet', missing: e.missing });
  try {
    const user = await currentUser(req, e);
    if (!user) return send(res, 401, { error: 'Not signed in' });
    const p = await getProfile(e, user.id);
    if (!p || !p.shopify_customer_id) return send(res, 200, { linked: false, orders: [] });
    const c = (await shopify(e, Q, { id: p.shopify_customer_id })).customer;
    if (!c) return send(res, 200, { linked: false, orders: [] });
    const orders = c.orders.nodes.map(o => {
      const ev = o.events.nodes;
      const accepted = ev.find(x => /accepted the request for fulfillment/i.test(x.message));
      const f = o.fulfillments || [];
      const fev = f.flatMap(x => x.events.nodes.map(y => ({ status: y.status, at: y.happenedAt })));
      const first = k => { const x = fev.find(y => y.status === k); return x && x.at; };
      const shipped = f.length ? f.map(x => x.createdAt).sort()[0] : null;
      const disp = f.map(x => x.displayStatus);
      const delivered = f.find(x => x.deliveredAt) ? f.find(x => x.deliveredAt).deliveredAt : (disp.includes('DELIVERED') ? first('DELIVERED') || f[0].updatedAt : null);
      const ofd = first('OUT_FOR_DELIVERY') || (disp.includes('OUT_FOR_DELIVERY') ? f[0].updatedAt : null);
      const transit = first('IN_TRANSIT') || (f.find(x => x.inTransitAt) || {}).inTransitAt || null;
      const eta = (f.find(x => x.estimatedDeliveryAt) || {}).estimatedDeliveryAt || null;
      const problem = disp.find(x => /FAILURE|ATTEMPTED_DELIVERY|NOT_DELIVERED/.test(x)) || null;
      const m = s => s && s.shopMoney ? +s.shopMoney.amount : 0;
      return {
        name: o.name, date: o.processedAt, cancelled: !!o.cancelledAt,
        payment: o.displayFinancialStatus, fulfillment: o.displayFulfillmentStatus,
        total: o.totalPriceSet.shopMoney.amount, currency: o.totalPriceSet.shopMoney.currencyCode,
        subtotal: m(o.subtotalPriceSet), shipping: m(o.totalShippingPriceSet), tax: m(o.totalTaxSet), discount: m(o.totalDiscountsSet), refunded: m(o.totalRefundedSet),
        shipMethod: o.shippingLine && o.shippingLine.title, address: addr(o.shippingAddress),
        items: o.lineItems.nodes.map(i => ({ title: i.title, variant: i.variantTitle, qty: i.quantity, image: i.image && i.image.url, price: m(i.originalUnitPriceSet) })),
        tracking: f.flatMap(x => x.trackingInfo.map(t => ({ company: t.company, number: t.number, url: t.url }))),
        steps: { received: o.processedAt, production: accepted ? accepted.createdAt : (o.displayFulfillmentStatus === 'IN_PROGRESS' ? o.processedAt : null),
          shipped, transit, outForDelivery: ofd, delivered, eta, problem },
      };
    });
    return send(res, 200, { linked: true, count: c.numberOfOrders, orders });
  } catch (err) {
    console.error('account/orders', err);
    return send(res, 502, { error: 'Could not load your orders right now' });
  }
};
