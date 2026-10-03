// POST /api/account/link
// After someone signs in, find their Shopify customer by email (e.g. earlier guest orders) or create one,
// and save the link on their PMN+ profile. Safe to call on every sign-in.
const { send, env, currentUser, ensureProfile, updateProfile, shopify } = require('../_account');

const FIND = `query($q:String!){customers(first:1,query:$q){nodes{id firstName lastName}}}`;
const CREATE = `mutation($input:CustomerInput!){customerCreate(input:$input){customer{id firstName lastName} userErrors{field message}}}`;

module.exports = async (req, res) => {
  if (req.method !== 'POST') return send(res, 405, { error: 'POST only' });
  const e = env();
  if (e.missing.length) return send(res, 503, { error: 'Accounts are not configured yet', missing: e.missing });
  try {
    const user = await currentUser(req, e);
    if (!user) return send(res, 401, { error: 'Not signed in' });
    if (!user.email_confirmed_at && !user.confirmed_at) return send(res, 403, { error: 'Email not verified' });
    let p = await ensureProfile(e, user);
    if (p && p.shopify_customer_id) return send(res, 200, { linked: true, created: false, customerId: p.shopify_customer_id });

    const email = String(user.email).toLowerCase();
    const found = (await shopify(e, FIND, { q: `email:"${email.replace(/"/g, '')}"` })).customers.nodes[0];
    let customer = found, created = false;
    if (!customer) {
      const input = { email, firstName: (p && p.first_name) || undefined, lastName: (p && p.last_name) || undefined, tags: ['pmn-account'] };
      if (!p || p.marketing_opt_in) input.emailMarketingConsent = { marketingState: 'SUBSCRIBED', marketingOptInLevel: 'SINGLE_OPT_IN' };
      const r = (await shopify(e, CREATE, { input })).customerCreate;
      if (r.userErrors && r.userErrors.length) throw new Error(r.userErrors.map(x => x.message).join('; '));
      customer = r.customer; created = true;
    }
    const patch = { shopify_customer_id: customer.id };
    if (p && !p.first_name && customer.firstName) patch.first_name = customer.firstName;
    if (p && !p.last_name && customer.lastName) patch.last_name = customer.lastName;
    await updateProfile(e, user.id, patch);
    return send(res, 200, { linked: true, created, customerId: customer.id });
  } catch (err) {
    console.error('account/link', err);
    return send(res, 502, { error: 'Could not link your account right now' });
  }
};
