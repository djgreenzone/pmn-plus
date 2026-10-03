// Shared helpers for /api/account/* (files starting with "_" are not public routes on Vercel).
// Secrets come only from Vercel environment variables:
//   SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
//   Shopify, either: SHOPIFY_CLIENT_ID + SHOPIFY_CLIENT_SECRET (Dev Dashboard app, recommended)
//                or: SHOPIFY_ADMIN_TOKEN (older admin-created custom app)
//   optionally SHOPIFY_STORE (defaults to polynesianmusicnetwork.myshopify.com)
const SHOP = process.env.SHOPIFY_STORE || 'polynesianmusicnetwork.myshopify.com';
const API = '2025-07';

function send(res, status, body) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(JSON.stringify(body));
}

function env() {
  const P = process.env;
  const e = { url: P.SUPABASE_URL, service: P.SUPABASE_SERVICE_ROLE_KEY, shopify: P.SHOPIFY_ADMIN_TOKEN,
    clientId: P.SHOPIFY_CLIENT_ID, clientSecret: P.SHOPIFY_CLIENT_SECRET };
  const missing = Object.entries({ SUPABASE_URL: e.url, SUPABASE_SERVICE_ROLE_KEY: e.service }).filter(([, v]) => !v).map(([k]) => k);
  if (!e.shopify && !(e.clientId && e.clientSecret)) missing.push('SHOPIFY_CLIENT_ID + SHOPIFY_CLIENT_SECRET');
  return { ...e, missing, url: (e.url || '').replace(/\/+$/, '') };
}

// Dev Dashboard apps get a 24-hour Admin API token from their client ID + secret (client credentials grant).
// Cached per warm function instance and refreshed an hour before it expires.
let tok = { value: null, until: 0 };
async function adminToken(e) {
  if (e.shopify) return e.shopify;
  if (tok.value && Date.now() < tok.until) return tok.value;
  const r = await fetch(`https://${SHOP}/admin/oauth/access_token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ client_id: e.clientId, client_secret: e.clientSecret, grant_type: 'client_credentials' }),
  });
  const j = await r.json().catch(() => ({}));
  if (!r.ok || !j.access_token) throw new Error('shopify token: ' + r.status + ' ' + JSON.stringify(j).slice(0, 200));
  tok = { value: j.access_token, until: Date.now() + Math.max(60, (j.expires_in || 86399) - 3600) * 1000 };
  return tok.value;
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
    headers: { 'Content-Type': 'application/json', 'X-Shopify-Access-Token': await adminToken(e) },
    body: JSON.stringify({ query, variables }),
  });
  const j = await r.json();
  if (!r.ok || j.errors) throw new Error('shopify: ' + JSON.stringify(j.errors || r.status).slice(0, 300));
  return j.data;
}

module.exports = { send, env, currentUser, getProfile, updateProfile, ensureProfile, shopify };
