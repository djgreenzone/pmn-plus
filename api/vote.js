// /api/vote — "Who you reppin'?" fan vote (Samoa vs Tonga) on /rlwc-playlists.
//
// GET  /api/vote?poll=rlwc26-samoa-tonga                       -> {totals:{samoa,tonga}}
// POST {poll, team:"samoa"|"tonga", voter, name, email}       -> {status:"ok"|"already"|"limit", team, totals}
//
// Voting needs a first name + email. The voter is subscribed to the PMN+ newsletter list in Klaviyo
// (custom source "RLWC fan vote") and a "RLWC Fan Vote" event with their team is recorded on their profile,
// so flows/segments can target Samoa vs Tonga fans.
// Limits: one vote per email per poll (email stored only as a hash; the address lives in Klaviyo), one per
// browser id, and at most 8 per network (hashed IP). Votes live in Supabase table `fan_votes`; the SQL functions
// fan_vote_cast / fan_vote_totals are callable only with the service role.
// Each new vote also makes sure the voter has a PMN+ account (passwordless: they sign in at /account with an
// emailed code) and saves the team they voted for as the profile's favourite team, unless they already picked one.
// Env (already in Vercel): SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY. Optional: KLAVIYO_LIST_ID (default Sggasa).
const crypto = require('crypto');

const KLAVIYO_COMPANY_ID = 'T9JJzp';
const KLAVIYO_REVISION = '2026-07-15';
const POLLS = { 'rlwc26-samoa-tonga': { teams: ['samoa', 'tonga'], label: { samoa: 'Toa Samoa', tonga: "Mate Ma'a Tonga" },
  // profiles.favourite_team values used by the account page
  slug: { samoa: 'toa-samoa', tonga: 'mate-maa-tonga' } } };

function send(res, status, body, cache) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', cache || 'no-store');
  res.end(JSON.stringify(body));
}

async function rpc(fn, args) {
  const url = (process.env.SUPABASE_URL || '').replace(/\/+$/, '');
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) throw Object.assign(new Error('Supabase env missing'), { code: 'config' });
  const r = await fetch(`${url}/rest/v1/rpc/${fn}`, {
    method: 'POST',
    headers: { apikey: key, Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(args),
  });
  if (!r.ok) throw Object.assign(new Error(`rpc ${fn} ${r.status}: ${(await r.text()).slice(0, 200)}`), { code: 'db' });
  return r.json();
}

async function klaviyo(path, body) {
  const r = await fetch(`https://a.klaviyo.com/client/${path}/?company_id=${KLAVIYO_COMPANY_ID}`, {
    method: 'POST', headers: { 'content-type': 'application/json', revision: KLAVIYO_REVISION }, body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(`klaviyo ${path} ${r.status} ${(await r.text()).slice(0, 200)}`);
}

// Create the voter's PMN+ account if they don't have one, then save their team on the profile when it's empty.
// The on_auth_user_created trigger makes the profiles row. No email is sent; they sign in later with a code.
async function linkAccount(email, name, team) {
  const url = (process.env.SUPABASE_URL || '').replace(/\/+$/, '');
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  const h = { apikey: key, Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' };
  const r = await fetch(`${url}/auth/v1/admin/users`, { method: 'POST', headers: h, body: JSON.stringify({
    email, email_confirm: true, user_metadata: { first_name: name, signup_source: 'rlwc_fan_vote', marketing_opt_in: true } }) });
  if (!r.ok && r.status !== 422) throw new Error(`account create ${r.status} ${(await r.text()).slice(0, 160)}`); // 422 = already has an account
  const q = `email=eq.${encodeURIComponent(email)}&or=(favourite_team.is.null,favourite_team.eq.)`;
  const u = await fetch(`${url}/rest/v1/profiles?${q}`, { method: 'PATCH', headers: { ...h, Prefer: 'return=minimal' },
    body: JSON.stringify({ favourite_team: team, updated_at: new Date().toISOString() }) });
  if (!u.ok) throw new Error(`profile team ${u.status} ${(await u.text()).slice(0, 160)}`);
  await fetch(`${url}/rest/v1/profiles?email=eq.${encodeURIComponent(email)}&first_name=is.null`, { method: 'PATCH',
    headers: { ...h, Prefer: 'return=minimal' }, body: JSON.stringify({ first_name: name }) });
}

const salt = () => (process.env.SUPABASE_SERVICE_ROLE_KEY || 'pmn').slice(-16);
const hash = (v) => crypto.createHash('sha256').update(salt() + '|' + v).digest('hex').slice(0, 40);
function ipHash(req) {
  const ip = String(req.headers['x-forwarded-for'] || req.socket?.remoteAddress || '').split(',')[0].trim();
  return ip ? hash('ip|' + ip) : null;
}

module.exports = async (req, res) => {
  try {
    if (req.method === 'GET') {
      const poll = String((req.query && req.query.poll) || '');
      if (!POLLS[poll]) return send(res, 400, { error: 'Unknown poll' });
      const totals = await rpc('fan_vote_totals', { p_poll: poll });
      return send(res, 200, { totals }, 'public, s-maxage=5, stale-while-revalidate=30');
    }
    if (req.method !== 'POST') return send(res, 405, { error: 'GET or POST only' });
    let b = req.body;
    if (typeof b === 'string') b = JSON.parse(b || '{}');
    b = b || {};
    const poll = String(b.poll || ''), team = String(b.team || ''), voter = String(b.voter || '');
    const name = String(b.name || '').trim().slice(0, 60);
    const email = String(b.email || '').trim().toLowerCase().slice(0, 200);
    const P = POLLS[poll];
    if (!P || !P.teams.includes(team)) return send(res, 400, { error: 'Pick Samoa or Tonga.' });
    if (!/^[a-zA-Z0-9-]{16,64}$/.test(voter)) return send(res, 400, { error: 'Reload the page and try again.' });
    if (!name) return send(res, 400, { error: 'Add your first name.', field: 'name' });
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) return send(res, 400, { error: 'Check your email address.', field: 'email' });

    const out = await rpc('fan_vote_cast', { p_poll: poll, p_team: team, p_voter: voter, p_ip: ipHash(req), p_email_hash: hash('email|' + email) });

    if (out.status === 'ok') {
      const list = process.env.KLAVIYO_LIST_ID || 'Sggasa';
      const profile = { email, first_name: name, properties: { rlwc_team: P.label[team] } };
      await Promise.allSettled([
        linkAccount(email, name, P.slug[team]),
        klaviyo('subscriptions', { data: { type: 'subscription', attributes: {
          custom_source: 'RLWC fan vote',
          profile: { data: { type: 'profile', attributes: { email, first_name: name, subscriptions: { email: { marketing: { consent: 'SUBSCRIBED' } } } } } },
        }, relationships: { list: { data: { type: 'list', id: list } } } } }),
        klaviyo('events', { data: { type: 'event', attributes: {
          properties: { Poll: poll, Team: P.label[team], Page: '/rlwc-playlists' },
          metric: { data: { type: 'metric', attributes: { name: 'RLWC Fan Vote' } } },
          profile: { data: { type: 'profile', attributes: profile } },
        } } }),
      ]).then((r) => r.forEach((x) => x.status === 'rejected' && console.warn('vote: follow-up', x.reason && x.reason.message)));
    }
    send(res, 200, out);
  } catch (e) {
    console.error('vote', e.code || '', e.message);
    send(res, 500, { error: 'Voting is busy right now. Try again in a minute.', code: e.code || 'server' });
  }
};
