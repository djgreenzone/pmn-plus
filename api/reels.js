// Vercel serverless function: GET /api/reels
// Returns the latest Instagram Reels for the account behind IG_ACCESS_TOKEN.
// Set IG_ACCESS_TOKEN in Vercel → Project → Settings → Environment Variables.
module.exports = async (req, res) => {
  const token = process.env.IG_ACCESS_TOKEN;
  const limit = Math.min(parseInt(req.query.limit || '8', 10) || 8, 12);
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  if (!token) { res.statusCode = 503; return res.end(JSON.stringify({ error: 'IG_ACCESS_TOKEN not set', reels: [] })); }
  const base = 'https://graph.instagram.com';
  const fields = 'id,caption,media_type,media_product_type,media_url,thumbnail_url,permalink,timestamp';
  try {
    const me = await (await fetch(`${base}/me?fields=username&access_token=${encodeURIComponent(token)}`)).json();
    if (me.error) throw new Error(me.error.message);
    let url = `${base}/me/media?fields=${fields}&limit=50&access_token=${encodeURIComponent(token)}`;
    const reels = [];
    for (let page = 0; page < 4 && url && reels.length < limit; page++) {
      const j = await (await fetch(url)).json();
      if (j.error) throw new Error(j.error.message);
      for (const m of j.data || []) {
        const isReel = m.media_product_type === 'REELS' || (m.media_type === 'VIDEO' && /\/reel\//.test(m.permalink || ''));
        if (isReel && (m.thumbnail_url || m.media_url)) {
          reels.push({ id: m.id, url: m.permalink, thumb: m.thumbnail_url || null, video: m.media_url || null,
            caption: (m.caption || '').replace(/\s+/g, ' ').trim().slice(0, 140), ts: m.timestamp });
        }
      }
      url = j.paging && j.paging.next;
    }
    res.setHeader('Cache-Control', 's-maxage=1800, stale-while-revalidate=86400');
    res.end(JSON.stringify({ username: me.username, reels: reels.slice(0, limit) }));
  } catch (e) {
    res.statusCode = 502;
    res.setHeader('Cache-Control', 's-maxage=60');
    res.end(JSON.stringify({ error: String(e.message || e), reels: [] }));
  }
};
