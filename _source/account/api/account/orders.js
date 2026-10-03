// GET /api/account/orders
// The signed-in person's Shopify orders (newest first) with items, status and tracking.
const { send, env, currentUser, getProfile, shopify } = require('../_account');

const Q = `query($id:ID!){customer(id:$id){
  firstName numberOfOrders
  defaultAddress{city provinceCode zip}
  orders(first:20,sortKey:PROCESSED_AT,reverse:true){nodes{
    id name processedAt cancelledAt statusPageUrl
    displayFinancialStatus displayFulfillmentStatus
    totalPriceSet{shopMoney{amount currencyCode}}
    lineItems(first:10){nodes{title variantTitle quantity image{url altText}}}
    fulfillments(first:5){status trackingInfo{company number url}}
  }}}}`;

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
    const orders = c.orders.nodes.map(o => ({
      name: o.name, date: o.processedAt, cancelled: !!o.cancelledAt, url: o.statusPageUrl,
      payment: o.displayFinancialStatus, fulfillment: o.displayFulfillmentStatus,
      total: o.totalPriceSet.shopMoney.amount, currency: o.totalPriceSet.shopMoney.currencyCode,
      items: o.lineItems.nodes.map(i => ({ title: i.title, variant: i.variantTitle, qty: i.quantity, image: i.image && i.image.url })),
      tracking: o.fulfillments.flatMap(f => f.trackingInfo.map(t => ({ company: t.company, number: t.number, url: t.url }))),
    }));
    return send(res, 200, { linked: true, count: c.numberOfOrders, orders });
  } catch (err) {
    console.error('account/orders', err);
    return send(res, 502, { error: 'Could not load your orders right now' });
  }
};
