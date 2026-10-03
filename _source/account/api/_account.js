// Shared helpers for /api/account/* (files starting with "_" are not public routes on Vercel).
// Secrets come only from Vercel environment variables:
//   SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, SHOPIFY_ADMIN_TOKEN (and optionally SHOPIFY_STORE)
const SHOP = process.env.SHOPIFY_STORE || 'polynesianmusicnetwork.myshopify.com';
const API = '2025-07';

function send(res, status, body) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(JSON.stringify(body));
}

function env() {
  const e = { url: process.env.SUPABASE_URL, service: process.env.SUPABASE_SERVICE_ROLE_KEY, shopify: process.env.SHOPIFY_ADMIN_TOKEN };
  const missing = Object.entries({ SUPABASE_URL: e.url, SUPABASE_SERVICE_ROLE_KEY: e.service, SHOPIFY_ADMIN_TOKEN: e.shopify }).filter(([, v]) => !v).map(([k]) => k);
  return { ...e, missing, url: (e.url || '').replace(/\/+$/, '') };
}

// The signed-in person, checked with Supabase (never trusted from the browser).
async function currentUser(req, e) {
  const h = req.headers.authorization || '';
  const token = h.startsWith('Bearer ') ? h.slice(7) : '';
  if (!token) return null;
  const r = await fetch(`${e.url}/auth/v1/user`, { headers: { apikey: e.service, Authorization: `Bearer ${token}` } });
  if (!r.ok) return null;
  const u = await r.json();
  return u && u.id && u.email ? u : null;
}

async function db(e, path, opts = {}) {
  const r = await fetch(`${e.url}/rest/v1/${path}`, {
    ...opts,
    headers: { apikey: e.service, Authorization: `Bearer ${e.service}`, 'Content-Type': 'application/json', Prefer: 'return=representation', ...(opts.headers || {}) },
  });
  const t = await r.text();
  if (!r.ok) throw new Error(`db ${r.status}: ${t.slice(0, 200)}`);
  return t ? JSON.parse(t) : null;
}
async function getProfile(e, id) {
  const rows = await db(e, `profiles?id=eq.${encodeURIComponent(id)}&select=*`);
  return rows && rows[0];
}
async function updateProfile(e, id, patch) {
  const rows = await db(e, `profiles?id=eq.${encodeURIComponent(id)}`, { method: 'PATCH', body: JSON.stringify(patch) });
  return rows && rows[0];
}
async function ensureProfile(e, user) {
  let p = await getProfile(e, user.id);
  if (!p) {
    const rows = await db(e, 'profiles', { method: 'POST', headers: { Prefer: 'return=representation,resolution=merge-duplicates' },
      body: JSON.stringify({ id: user.id, email: user.email, first_name: (user.user_metadata || {}).first_name || null }) });
    p = rows && rows[0];
  }
  return p;
}

async function shopify(e, query, variables) {
  const r = await fetch(`https://${SHOP}/admin/api/${API}/graphql.json`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-Shopify-Access-Token': e.shopify },
    body: JSON.stringify({ query, variables }),
  });
  const j = await r.json();
  if (!r.ok || j.errors) throw new Error('shopify: ' + JSON.stringify(j.errors || r.status).slice(0, 300));
  return j.data;
}

module.exports = { send, env, currentUser, getProfile, updateProfile, ensureProfile, shopify };
