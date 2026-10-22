// /api/join — PMN+ Content Team applications (page: /join-the-team).
//
// POST {action:"upload", files:[{type,size}]}  -> {uploads:[{path,url}]}   signed URLs the browser PUTs each photo to
// POST {action:"submit", ...answers, photos:[path]} -> {ok:true}
//
// On submit the application is:
//   1. stored in Supabase table `content_team_applications` (skipped quietly if the table doesn't exist yet,
//      see docs/RUNBOOK.md "Content Team applications"),
//   2. sent to Klaviyo as the event "Content Team Application" on the applicant's profile. The Klaviyo flow
//      "Content Team Application" emails Tiomai an alert and sends the applicant a confirmation,
//   3. subscribed to the newsletter list if they ticked the box.
// Photos live in the private Supabase Storage bucket `content-team` (created automatically on first upload).
// Env (already set in Vercel): SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY. Optional: KLAVIYO_LIST_ID (default Sggasa).
const KLAVIYO_COMPANY_ID = 'T9JJzp';
const KLAVIYO_REVISION = '2026-07-15';
const BUCKET = 'content-team';
const MAX_FILE = 10 * 1024 * 1024;
const TYPES = { 'image/jpeg': 'jpg', 'image/png': 'png', 'image/webp': 'webp', 'image/heic': 'heic', 'image/heif': 'heif' };
const ROLES = ['photographer', 'videographer', 'model', 'content-creator', 'graphic-designer', 'journalist', 'sports-analyst', 'personality'];
const ROLE_LABEL = { photographer: 'Photographer', videographer: 'Videographer', model: 'Model', 'content-creator': 'Content creator',
  'graphic-designer': 'Graphic designer', journalist: 'Journalist', 'sports-analyst': 'Sports analyst', personality: 'Personality' };
const CITIES = { 'las-vegas': 'Las Vegas', 'los-angeles': 'Los Angeles', both: 'Las Vegas and Los Angeles' };

function send(res, status, body) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.end(JSON.stringify(body));
}
const str = (v, n = 200) => (typeof v === 'string' ? v.trim().slice(0, n) : '');
const list = (v, allowed) => (Array.isArray(v) ? [...new Set(v.filter((x) => typeof x === 'string' && (!allowed || allowed.includes(x))))] : []);
const emailOk = (e) => /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(e);

function supa() {
  const url = (process.env.SUPABASE_URL || '').replace(/\/+$/, '');
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!url || !key) throw Object.assign(new Error('Supabase env missing'), { code: 'config' });
  const h = { apikey: key, Authorization: `Bearer ${key}` };
  return { url, h };
}

async function ensureBucket(s) {
  const r = await fetch(`${s.url}/storage/v1/bucket/${BUCKET}`, { headers: s.h });
  if (r.ok) return;
  const c = await fetch(`${s.url}/storage/v1/bucket`, {
    method: 'POST', headers: { ...s.h, 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: BUCKET, name: BUCKET, public: false, file_size_limit: MAX_FILE, allowed_mime_types: Object.keys(TYPES) }),
  });
  if (!c.ok && c.status !== 409 && c.status !== 400) throw Object.assign(new Error('bucket ' + c.status + ' ' + (await c.text()).slice(0, 200)), { code: 'storage-bucket' });
}

async function signUpload(s, path) {
  const r = await fetch(`${s.url}/storage/v1/object/upload/sign/${BUCKET}/${path}`, { method: 'POST', headers: s.h });
  const j = await r.json().catch(() => ({}));
  if (!r.ok || !j.url) throw Object.assign(new Error('sign upload ' + r.status + ' ' + JSON.stringify(j).slice(0, 200)), { code: 'storage-sign' });
  return `${s.url}/storage/v1${j.url}`;
}

async function signDownload(s, path) {
  const r = await fetch(`${s.url}/storage/v1/object/sign/${BUCKET}/${path}`, {
    method: 'POST', headers: { ...s.h, 'Content-Type': 'application/json' }, body: JSON.stringify({ expiresIn: 60 * 60 * 24 * 365 }),
  });
  const j = await r.json().catch(() => ({}));
  return r.ok && j.signedURL ? `${s.url}/storage/v1${j.signedURL}` : null;
}

async function klaviyo(path, body) {
  const r = await fetch(`https://a.klaviyo.com/client/${path}/?company_id=${KLAVIYO_COMPANY_ID}`, {
    method: 'POST', headers: { 'content-type': 'application/json', revision: KLAVIYO_REVISION }, body: JSON.stringify(body),
  });
  if (!r.ok) throw Object.assign(new Error(`klaviyo ${path} ${r.status} ${(await r.text()).slice(0, 300)}`), { code: 'klaviyo-' + path + '-' + r.status });
}

async function upload(req, res) {
  const files = Array.isArray(req.body.files) ? req.body.files.slice(0, 3) : [];
  if (!files.length) return send(res, 400, { error: 'No files' });
  for (const f of files) {
    if (!TYPES[f.type]) return send(res, 400, { error: 'Photos must be JPG, PNG, WebP or HEIC.' });
    if (!(f.size > 0 && f.size <= MAX_FILE)) return send(res, 400, { error: 'Each photo must be under 10 MB.' });
  }
  const s = supa();
  await ensureBucket(s);
  const day = new Date().toISOString().slice(0, 10);
  const batch = Math.random().toString(36).slice(2, 10) + Date.now().toString(36);
  const uploads = [];
  for (let i = 0; i < files.length; i++) {
    const path = `${day}/${batch}-${i + 1}.${TYPES[files[i].type]}`;
    uploads.push({ path, url: await signUpload(s, path) });
  }
  send(res, 200, { uploads });
}

async function submit(req, res) {
  const b = req.body || {};
  if (str(b.website)) return send(res, 200, { ok: true }); // honeypot: bots fill hidden fields
  const a = {
    first_name: str(b.first_name, 60), last_name: str(b.last_name, 60), email: str(b.email, 120).toLowerCase(),
    phone: str(b.phone, 30).replace(/[^\d+]/g, ''), roles: list(b.roles, ROLES), city: str(b.city, 20), age: str(b.age, 10),
    portfolio: str(b.portfolio, 300), instagram: str(b.instagram, 40).replace(/^@/, ''),
    photo_types: list(b.photo_types), photo_gear: str(b.photo_gear, 300), photo_edit: str(b.photo_edit, 300),
    video_types: list(b.video_types), video_gear: str(b.video_gear, 300), video_edit: str(b.video_edit, 300),
    height: str(b.height, 20), tee_size: str(b.tee_size, 10), model_exp: str(b.model_exp, 10),
    guardian_name: str(b.guardian_name, 120), guardian_email: str(b.guardian_email, 120).toLowerCase(),
    availability: list(b.availability), why: str(b.why, 600), newsletter: b.newsletter === true,
    photos: list(b.photos).filter((p) => /^\d{4}-\d{2}-\d{2}\/[a-z0-9]+-[1-3]\.(jpg|png|webp|heic|heif)$/.test(p)).slice(0, 3),
  };
  const digits = a.phone.replace(/\D/g, '').replace(/^1(?=\d{10}$)/, '');
  const bad = [];
  if (!a.first_name || !a.last_name) bad.push('name');
  if (!emailOk(a.email)) bad.push('email');
  if (digits.length !== 10) bad.push('phone');
  if (!a.roles.length) bad.push('roles');
  if (!CITIES[a.city]) bad.push('city');
  if (!['16-17', '18+'].includes(a.age)) bad.push('age');
  if (!/^https?:\/\/[^\s.]+\.[^\s]+$/i.test(a.portfolio)) bad.push('portfolio');
  if (!/^(?!.*\.\.)(?!\.)[A-Za-z0-9._]{1,30}$/.test(a.instagram)) bad.push('instagram');
  if (a.age === '16-17' && (!a.guardian_name || !emailOk(a.guardian_email))) bad.push('guardian');
  if (bad.length) return send(res, 400, { error: 'Please check: ' + bad.join(', ') });
  a.phone = '+1' + digits;

  const s = supa();
  const photoLinks = (await Promise.all(a.photos.map((p) => signDownload(s, p).catch(() => null)))).filter(Boolean);
  const submitted = new Date().toISOString();
  const id = 'CT-' + Date.now().toString(36).toUpperCase();

  // 1. Supabase record (the roster). Quietly skipped until the table exists.
  try {
    const r = await fetch(`${s.url}/rest/v1/content_team_applications`, {
      method: 'POST', headers: { ...s.h, 'Content-Type': 'application/json', Prefer: 'return=minimal' },
      body: JSON.stringify({ ref: id, ...a, status: 'applied', created_at: submitted }),
    });
    if (!r.ok && r.status !== 404) console.warn('join: db', r.status, (await r.text()).slice(0, 200));
  } catch (e) { console.warn('join: db', e.message); }

  // 2. Klaviyo event -> flow emails Tiomai + confirms to the applicant.
  const props = {
    reference: id, submitted,
    first_name: a.first_name, last_name: a.last_name, full_name: `${a.first_name} ${a.last_name}`,
    email: a.email, phone: a.phone,
    roles: a.roles.map((r) => ROLE_LABEL[r]), roles_text: a.roles.map((r) => ROLE_LABEL[r]).join(', '),
    city: CITIES[a.city], age: a.age === '18+' ? '18 or older' : '16–17 (guardian required)',
    portfolio: a.portfolio, instagram: '@' + a.instagram, instagram_url: `https://www.instagram.com/${a.instagram}/`,
    photo_types: a.photo_types.join(', '), photo_gear: a.photo_gear, photo_edit: a.photo_edit,
    video_types: a.video_types.join(', '), video_gear: a.video_gear, video_edit: a.video_edit,
    height: a.height, tee_size: a.tee_size, model_experience: a.model_exp,
    guardian_name: a.guardian_name, guardian_email: a.guardian_email,
    availability: a.availability.join(', '), why: a.why, newsletter: a.newsletter ? 'Yes' : 'No',
    photo_count: photoLinks.length, photo_1: photoLinks[0] || '', photo_2: photoLinks[1] || '', photo_3: photoLinks[2] || '',
  };
  await klaviyo('events', { data: { type: 'event', attributes: {
    properties: props, unique_id: id,
    metric: { data: { type: 'metric', attributes: { name: 'Content Team Application' } } },
    profile: { data: { type: 'profile', attributes: { email: a.email, first_name: a.first_name, last_name: a.last_name,
      properties: { content_team_applicant: true, content_team_roles: props.roles, content_team_city: props.city, instagram: props.instagram } } } },
  } } });

  // 3. Newsletter opt-in (only when ticked).
  if (a.newsletter) {
    await klaviyo('subscriptions', { data: { type: 'subscription', attributes: {
      custom_source: 'Join the Team page',
      profile: { data: { type: 'profile', attributes: { email: a.email, first_name: a.first_name, last_name: a.last_name,
        subscriptions: { email: { marketing: { consent: 'SUBSCRIBED' } } } } } },
    }, relationships: { list: { data: { type: 'list', id: process.env.KLAVIYO_LIST_ID || 'Sggasa' } } } } }).catch((e) => console.warn('join: subscribe', e.message));
  }
  send(res, 200, { ok: true, reference: id });
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') return send(res, 405, { error: 'POST only' });
  try {
    if (typeof req.body === 'string') req.body = JSON.parse(req.body || '{}');
    req.body = req.body || {};
    if (req.body.action === 'upload') return await upload(req, res);
    if (req.body.action === 'submit') return await submit(req, res);
    send(res, 400, { error: 'Unknown action' });
  } catch (e) {
    console.error('join', e.code || '', e.message);
    send(res, 500, { error: 'Something went wrong sending your application. Please try again.', code: e.code || 'server' });
  }
};
