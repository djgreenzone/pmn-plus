/* PMN+ checkout pixel — paste into Shopify admin → Settings → Customer events → Add custom pixel ("PMN+ analytics").
   Sends checkout steps and purchases to GA4, Meta and TikTok. Fill in the same IDs as /assets/pmn-config.js.
   The site passes the visitor's GA client ID and Meta browser ID into the cart (attributes), so the purchase
   joins up with the visit that started on polynesianmusicnetwork.com. Not committed to the site (Vercel ignores _source). */
const IDS = { ga4: "G-KEQ8HPTH9W", meta: "1983591485663494", tiktok: "" };

const load = src => { const s = document.createElement("script"); s.async = true; s.src = src; document.head.appendChild(s); };
const attr = (c, k) => ((c && c.attributes) || []).find(a => a.key === k)?.value || "";
const items = c => (c.lineItems || []).map(l => ({
  item_id: l.variant?.product?.url?.split("/").pop() || l.variant?.sku || l.id,
  item_name: l.title, item_brand: "PMN+", item_variant: l.variant?.title || "",
  price: +(l.variant?.price?.amount || 0), quantity: l.quantity }));

let gaReady = false;
function ga(c) {
  if (!IDS.ga4) return null;
  if (!gaReady) {
    window.dataLayer = window.dataLayer || []; window.gtag = function () { dataLayer.push(arguments); };
    gtag("js", new Date());
    const cid = attr(c, "_ga_client_id");
    gtag("config", IDS.ga4, Object.assign({ send_page_view: false }, cid ? { client_id: cid } : {}));
    load("https://www.googletagmanager.com/gtag/js?id=" + IDS.ga4); gaReady = true;
  }
  return window.gtag;
}
let fbReady = false;
function fb(c) {
  if (!IDS.meta) return null;
  if (!fbReady) {
    !function (f) { if (f.fbq) return; const n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = true; n.version = "2.0"; n.queue = []; }(window);
    load("https://connect.facebook.net/en_US/fbevents.js");
    const em = c?.email ? { em: c.email.trim().toLowerCase() } : {};
    fbq("init", IDS.meta, em); fbReady = true;
  }
  return window.fbq;
}
let ttReady = false;
function tt() {
  if (!IDS.tiktok) return null;
  if (!ttReady) {
    !function (w, t) { w.TiktokAnalyticsObject = t; const q = w[t] = w[t] || [];
      q.methods = ["page", "track", "identify", "instances", "debug", "on", "off", "once", "ready", "alias", "group", "enableCookie", "disableCookie"];
      q.setAndDefer = (o, m) => { o[m] = function () { o.push([m].concat([].slice.call(arguments, 0))); }; };
      q.methods.forEach(m => q.setAndDefer(q, m));
      q.load = id => { q._i = q._i || {}; q._i[id] = []; q._t = q._t || {}; q._t[id] = +new Date(); load("https://analytics.tiktok.com/i18n/pixel/events.js?sdkid=" + id + "&lib=" + t); };
      q.load(IDS.tiktok); }(window, "ttq");
    ttReady = true;
  }
  return window.ttq;
}

analytics.subscribe("checkout_shipping_info_submitted", e => {
  const c = e.data.checkout, g = ga(c);
  if (g) g("event", "add_shipping_info", { currency: c.currencyCode, value: +c.subtotalPrice.amount, items: items(c) });
});
analytics.subscribe("payment_info_submitted", e => {
  const c = e.data.checkout, g = ga(c), f = fb(c), t = tt();
  if (g) g("event", "add_payment_info", { currency: c.currencyCode, value: +c.subtotalPrice.amount, items: items(c) });
  if (f) f("track", "AddPaymentInfo", { currency: c.currencyCode, value: +c.subtotalPrice.amount });
  if (t) t.track("AddPaymentInfo", { currency: c.currencyCode, value: +c.subtotalPrice.amount });
});
analytics.subscribe("checkout_completed", e => {
  const c = e.data.checkout, id = c.order?.id || c.token, value = +c.totalPrice.amount, its = items(c);
  const coupon = (c.discountApplications || []).map(d => d.title).filter(Boolean).join(",");
  const g = ga(c), f = fb(c), t = tt();
  if (g) g("event", "purchase", { transaction_id: id, currency: c.currencyCode, value, tax: +(c.totalTax?.amount || 0),
    shipping: +(c.shippingLine?.price?.amount || 0), coupon, items: its });
  if (f) f("track", "Purchase", { currency: c.currencyCode, value, content_type: "product",
    content_ids: its.map(i => i.item_id), num_items: its.reduce((n, i) => n + i.quantity, 0) }, { eventID: "order-" + id });
  if (t) { if (c.email) t.identify({ email: c.email }); t.track("CompletePayment", { currency: c.currencyCode, value, content_type: "product",
    contents: its.map(i => ({ content_id: i.item_id, content_name: i.item_name, quantity: i.quantity, price: i.price })) }, { event_id: "order-" + id }); }
});
