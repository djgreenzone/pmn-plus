// Team dashboard API — create/edit/publish editorial posts.
// Writes with the service role (server-side) after verifying the caller is an
// admin (ADMIN_EMAILS). Mirrors the /api/account/* pattern. Content lives in the
// Supabase tables the content build uses: posts, issues, authors, categories.
//
// Routes (single function, action in the body or querystring):
//   GET  /api/admin/posts                 -> list posts (+authors, categories, issues) incl. drafts
//   GET  /api/admin/posts?meta=1          -> authors + categories + issues (for the editor dropdowns)
//   POST /api/admin/posts {post}          -> create (status defaults to 'draft')
//   PATCH/POST /api/admin/posts {id, patch}        -> update fields
//   POST /api/admin/posts {id, action:'publish'|'unpublish'}  -> set status + published_at, fire deploy
//   POST /api/admin/posts {action:'deploy'}        -> fire the deploy hook only
//   DELETE /api/admin/posts {id}          -> delete a post
const { send, env, currentUser, db, isAdmin, fireDeploy } = require('../_account.js');

const ALLOWED = ['slug','category_id','issue_id','author_id','title','dek','body_html','hero_image_url',
  'hero_alt','order_in_issue','is_cover_story','reading_minutes','seo_title','seo_description','keywords',
  'tags','og_image_url','schema_type','canonical_url','rights_note','status'];

function clean(obj) {
  const o = {};
  for (const k of ALLOWED) if (k in obj) o[k] = obj[k];
  return o;
}
function readBody(req) {
  return new Promise((res) => {
    let s = ''; req.on('data', (c) => (s += c)); req.on('end', () => { try { res(s ? JSON.parse(s) : {}); } catch (e) { res({}); } });
  });
}

module.exports = async (req, res) => {
  const e = env();
  if (e.missing.length) return send(res, 500, { error: 'server not configured', missing: e.missing });

  const user = await currentUser(req, e);
  if (!user) return send(res, 401, { error: 'sign in' });
  if (!isAdmin(e, user)) return send(res, 403, { error: 'not authorized' });

  try {
    const url = new URL(req.url, 'http://x');
    const method = req.method.toUpperCase();

    if (method === 'GET') {
      if (url.searchParams.get('meta')) {
        const [authors, categories, issues] = await Promise.all([
          db(e, 'authors?select=id,slug,name,role&order=name'),
          db(e, 'categories?select=id,slug,name,position&order=position'),
          db(e, 'issues?select=id,slug,title,period_label,status&order=created_at.desc'),
        ]);
        return send(res, 200, { authors, categories, issues });
      }
      const full = url.searchParams.get('full');
      if (full) {
        const rows = await db(e, `posts?id=eq.${encodeURIComponent(full)}&select=*`);
        return send(res, 200, { post: rows && rows[0] });
      }
      const rows = await db(e, 'posts?select=id,slug,title,dek,status,published_at,updated_at,order_in_issue,' +
        'is_cover_story,category:categories(name),author:authors(name),issue:issues(title,slug)&order=updated_at.desc');
      return send(res, 200, { posts: rows });
    }

    const body = await readBody(req);

    if (method === 'DELETE' || body.action === 'delete') {
      if (!body.id) return send(res, 400, { error: 'id required' });
      await db(e, `posts?id=eq.${encodeURIComponent(body.id)}`, { method: 'DELETE' });
      return send(res, 200, { ok: true });
    }

    if (body.action === 'deploy') {
      const d = await fireDeploy(e);
      return send(res, 200, { ok: d.ok, deploy: d });
    }

    if (body.action === 'publish' || body.action === 'unpublish') {
      if (!body.id) return send(res, 400, { error: 'id required' });
      const patch = body.action === 'publish'
        ? { status: 'published', published_at: new Date().toISOString() }
        : { status: 'draft' };
      const rows = await db(e, `posts?id=eq.${encodeURIComponent(body.id)}`, { method: 'PATCH', body: JSON.stringify(patch) });
      const deploy = await fireDeploy(e);          // rebuild so the change goes live / drops off
      return send(res, 200, { post: rows && rows[0], deploy });
    }

    if (method === 'PATCH' || (method === 'POST' && body.id)) {
      if (!body.id) return send(res, 400, { error: 'id required' });
      const patch = clean(body.patch || body);
      patch.updated_at = new Date().toISOString();
      const rows = await db(e, `posts?id=eq.${encodeURIComponent(body.id)}`, { method: 'PATCH', body: JSON.stringify(patch) });
      return send(res, 200, { post: rows && rows[0] });
    }

    if (method === 'POST') {
      const post = clean(body.post || body);
      if (!post.title) return send(res, 400, { error: 'title required' });
      if (!post.slug) post.slug = String(post.title).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 80);
      if (!post.body_html) post.body_html = '';
      if (!post.status) post.status = 'draft';
      if (!('keywords' in post)) post.keywords = [];
      if (!('tags' in post)) post.tags = [];
      if (!post.schema_type) post.schema_type = 'Article';
      const rows = await db(e, 'posts', { method: 'POST', body: JSON.stringify(post) });
      return send(res, 200, { post: rows && rows[0] });
    }

    return send(res, 405, { error: 'method not allowed' });
  } catch (err) {
    return send(res, 500, { error: String(err).slice(0, 300) });
  }
};
