// /api/vote — "Who you reppin'?" fan vote (Samoa vs Tonga) on /rlwc-playlists.
//
// GET  /api/vote?poll=rlwc26-samoa-tonga          -> {totals:{samoa,tonga}}
// POST {poll, team:"samoa"|"tonga", voter}        -> {status:"ok"|"already"|"limit", team, totals}
//
// One vote per voter id (random id the browser keeps in a cookie + localStorage). On top of that, at most
// 8 votes per network (hashed IP, never stored raw) per poll, so clearing cookies can't stuff the count.
// Votes live in Supabase table `fan_votes`; the SQL functions fan_vote_cast / fan_vote_totals do the work
// and are callable only with the service role. Env (already in Vercel): SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY.
const crypto = require('crypto');

const POLLS = { 'rlwc26-samoa-tonga': ['samoa', 'tonga'] };

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

function ipHash(req) {
  const ip = String(req.headers['x-forwarded-for'] || req.socket?.remoteAddress || '').split(',')[0].trim();
  if (!ip) return null;
  const salt = process.env.SUPABASE_SERVICE_ROLE_KEY || 'pmn';
  return crypto.createHash('sha256').update(salt.slice(-16) + '|' + ip).digest('hex').slice(0, 32);
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
    if (!POLLS[poll] || !POLLS[poll].includes(team)) return send(res, 400, { error: 'Pick Samoa or Tonga' });
    if (!/^[a-zA-Z0-9-]{16,64}$/.test(voter)) return send(res, 400, { error: 'Bad voter id' });
    const out = await rpc('fan_vote_cast', { p_poll: poll, p_team: team, p_voter: voter, p_ip: ipHash(req) });
    send(res, 200, out);
  } catch (e) {
    console.error('vote', e.code || '', e.message);
    send(res, 500, { error: 'Voting is busy right now. Try again in a minute.', code: e.code || 'server' });
  }
};
