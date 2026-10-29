# Editorial renderer — /stories + /digital-magazine

Generates the static stories/magazine site from the Supabase content tables
(`posts`, `issues`, `authors`, `categories`). Built to `claude/pmn-content-seo-contract.md`.
The **dashboard** (`admin/`), its **API** (`_source/account/api/admin/posts.js`) and the
`shop-this-story` cards are the other track; this is the renderer on top.

## Build

From `_source/content/`:

```
python3 build.py
```

Fetches **published** rows from Supabase REST with the public publishable key
(`assets/pmn-config.js`) — no secret needed. Writes, at the repo root:

- `stories/<slug>/index.html` — a story (canonical unit, flat URL)
- `stories/index.html`, `stories/<category>/`, `stories/author/<slug>/`, `stories/tag/<tag>/`
- `digital-magazine/index.html`, `digital-magazine/<issue-slug>/index.html`
- `stories/feed.xml` (RSS, latest 50) and `sitemap-stories.xml`
- copies `story.css` + `shop-this-story.{css,js}` to `assets/content/`

Then commit the generated output (same as the shop build). The team dashboard
fires a Vercel Deploy Hook on publish, which re-runs this on deploy.

Test offline against a snapshot instead of Supabase:

```
python3 build.py --data snapshot.json    # {issues,authors,categories,posts}
```

## One-time
`robots.txt` lists `sitemap-stories.xml` (done). Add `/sitemap-stories.xml` as a
sitemap in Search Console. Full WebP/AVIF + 1200×630 OG crops are a later pass
(reuse `make_og.py`); heroes currently come straight from Supabase Storage.

## Rules
Edit `_source/content/*` and rebuild — never hand-edit `stories/` or
`digital-magazine/` output. Single "moana" teal accent (`#22c5c5`); team colours
stay on team content only.
