// GET /api/account/reviews
// Reviews the signed-in person has written (Klaviyo Reviews), matched on email.
// Needs KLAVIYO_PRIVATE_KEY (reviews:read) in Vercel env; returns {reviews:[],soon:true} until it is set.
const { send, env, currentUser } = require('../_account');

const REV = '2026-07-15';
let cache = { at: 0, rows: [] };            // all reviews, per warm instance, 10 min

async function allReviews(key) {
  if (Date.now() - cache.at < 600e3) return cache.rows;
  const rows = [];
  let url = 'https://a.klaviyo.com/api/reviews/?page[size]=100&sort=-created&filter=' +
    encodeURIComponent('and(equals(status,"all"),equals(review_type,"review"))') +
    '&fields[review]=author,content,created,email,product,rating,status,title,verified,images';
  for (let i = 0; i < 10 && url; i++) {
    const r = await fetch(url, { headers: { Authorization: `Klaviyo-API-Key ${key}`, revision: REV, accept: 'application/vnd.api+json' } });
    if (!r.ok) throw new Error('klaviyo reviews ' + r.status);
    const j = await r.json();
    rows.push(...(j.data || []));
    url = j.links && j.links.next;
  }
  cache = { at: Date.now(), rows };
  return rows;
}

module.exports = async (req, res) => {
  if (req.method !== 'GET') return send(res, 405, { error: 'GET only' });
  const e = env();
  if (e.missing.length) return send(res, 503, { error: 'Accounts are not configured yet', missing: e.missing });
  const key = process.env.KLAVIYO_PRIVATE_KEY;
  try {
    const user = await currentUser(req, e);
    if (!user) return send(res, 401, { error: 'Not signed in' });
    if (!key) return send(res, 200, { reviews: [], soon: true });
    const em = user.email.toLowerCase();
    const mine = (await allReviews(key)).filter(x => ((x.attributes || {}).email || '').toLowerCase() === em);
    res.setHeader('Cache-Control', 'private, max-age=120');
    return send(res, 200, {
      reviews: mine.map(x => { const a = x.attributes || {}, p = a.product || {}, st = a.status || {};
        return { id: x.id, rating: a.rating, title: a.title || '', content: a.content || '', created: a.created,
          status: st.value || '', verified: !!a.verified, images: a.images || [],
          product: { id: p.external_id || '', name: p.name || '', image: p.image_url || '', url: p.url || '' } }; }),
    });
  } catch (err) {
    console.error('reviews', err);
    return send(res, 502, { error: String(err.message || err), reviews: [] });
  }
};
