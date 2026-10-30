#!/usr/bin/env python3
"""PMN+ editorial renderer — generates the static /stories + /digital-magazine site
from the Supabase content tables (posts, issues, authors, categories).

Run from _source/content/:
    python3 build.py                 # production: fetch published rows from Supabase REST
    python3 build.py --data f.json   # test: read a local {issues,authors,categories,posts} snapshot

Output (committed, served by Vercel):
    /stories/index.html                      all stories, newest first
    /stories/<slug>/index.html               a story (canonical unit)
    /stories/<category>/index.html           category hub
    /stories/author/<slug>/index.html        author page
    /stories/tag/<tag>/index.html            tag page
    /stories/feed.xml                        RSS (latest 50)
    /digital-magazine/index.html             all issues
    /digital-magazine/<slug>/index.html      issue reader (read mode) + contents
    /sitemap-stories.xml                     stories/magazine sitemap (add to robots.txt)
    /assets/content/story.css, shop-this-story.{css,js}   copied
Build to the SEO contract (claude/pmn-content-seo-contract.md). Never hand-edit the output.
"""
import os, sys, json, html, re, shutil, urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SITE = "https://www.polynesianmusicnetwork.com"
SB_URL = os.environ.get("SUPABASE_URL", "https://zacfssfjlmixnqhjuoed.supabase.co")
SB_KEY = os.environ.get("SUPABASE_ANON_KEY", "sb_publishable__o1QyHHm3--jPJ2iz61m8A_ssXrOmWk")
ORG_ID = SITE + "/#org"
FONTS = ("https://fonts.googleapis.com/css2?family=Bebas+Neue&"
         "family=Instrument+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap")

sys.path.insert(0, os.path.join(HERE, "..", "nav"))
import nav_build  # shared site header

def esc(s): return html.escape("" if s is None else str(s), quote=True)
def slugify(s): return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", (s or "").lower())).strip("-")
def trim(s, n): s = s or ""; return s if len(s) <= n else s[:n-1].rsplit(" ", 1)[0] + "…"

# ---------- data ----------
def fetch(path):
    req = urllib.request.Request(SB_URL + "/rest/v1/" + path,
                                 headers={"apikey": SB_KEY, "Authorization": "Bearer " + SB_KEY})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def load_data(argv):
    if "--data" in argv:
        return json.load(open(argv[argv.index("--data") + 1]))
    return {
        "issues": fetch("issues?status=eq.published&select=*&order=created_at"),
        "authors": fetch("authors?select=*"),
        "categories": fetch("categories?select=*&order=position"),
        "posts": fetch("posts?status=eq.published&select=*&order=order_in_issue"),
    }

# ---------- shared chrome ----------
def footer_html():
    try:
        h = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
        m = re.search(r"<footer\b.*?</footer>", h, re.S)
        if m: return m.group(0)
    except Exception:
        pass
    return ('<footer class="ed-foot ed-wrap"><span>PMN+ · Community. Culture. Connection.</span>'
            '<span>&copy; Polynesian Music Network Plus</span></footer>')

HEADER = '<header class="nav pn-bar" id="nav">' + nav_build.header(bag="link") + '</header>'

def page(title, desc, canonical, *, body, og_image=None, og_type="website",
         robots="index,follow", ld=None, head_extra=""):
    og_image = og_image or (SITE + "/assets/pmn-plus-og-music-culture-tradition-sports.jpg")
    ld_block = ""
    if ld:
        ld_block = '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{esc(canonical)}">
<meta name="theme-color" content="#000000">
<link rel="icon" type="image/png" href="/assets/favicon.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta property="og:site_name" content="PMN+">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{esc(canonical)}">
<meta property="og:image" content="{esc(og_image)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{esc(og_image)}">
<link rel="alternate" type="application/rss+xml" title="PMN+ Stories" href="/stories/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="{FONTS}" onload="this.onload=null;this.rel='stylesheet'"><noscript><link rel="stylesheet" href="{FONTS}"></noscript>
<link rel="stylesheet" href="/assets/pmn-nav.css">
<link rel="stylesheet" href="/assets/content/story.css">
<link rel="stylesheet" href="/assets/content/shop-this-story.css">
{head_extra}
{ld_block}
<style>html{{-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}}*{{margin:0;padding:0;box-sizing:border-box}}body{{background:#000;color:#fff;min-height:100svh;display:flex;flex-direction:column}}main{{flex:1}}[hidden]{{display:none!important}}</style>
</head>
<body>
<script src="/assets/pmn-config.js"></script>
{HEADER}
<main class="ed">
{body}
</main>
{footer_html()}
<script src="/assets/pmn-nav.js"></script>
<script src="/assets/content/shop-this-story.js" defer></script>
</body>
</html>"""

# ---------- cards ----------
def rail_card(p, idx):
    cat = idx["cat"].get(p.get("category_id"), {})
    au = idx["au"].get(p.get("author_id"), {})
    thumb = p.get("hero_image_url") or ""
    img = f'<img class="thumb" loading="lazy" src="{esc(thumb)}" alt="{esc(p.get("hero_alt") or p["title"])}">' if thumb else '<div class="thumb"></div>'
    return (f'<a class="ed-scard" href="/stories/{esc(p["slug"])}">{img}'
            f'<div class="meta"><span class="cat">{esc((cat.get("name") or "").upper())}</span>'
            f'<span class="t">{esc(p["title"])}</span>'
            f'<span class="by">{esc(au.get("name") or "PMN+")}</span></div></a>')

def big_card(p, idx):
    cat = idx["cat"].get(p.get("category_id"), {})
    au = idx["au"].get(p.get("author_id"), {})
    thumb = p.get("hero_image_url") or ""
    img = f'<img class="ph" loading="lazy" src="{esc(thumb)}" alt="{esc(p.get("hero_alt") or p["title"])}">' if thumb else '<div class="ph"></div>'
    return (f'<a class="ed-card" href="/stories/{esc(p["slug"])}">{img}<div class="b">'
            f'<span class="cat">{esc((cat.get("name") or "").upper())}</span>'
            f'<span class="t">{esc(p["title"])}</span>'
            f'<span class="d">{esc(p.get("dek") or "")}</span>'
            f'<span class="by">{esc(au.get("name") or "PMN+")}</span></div></a>')

# ---------- related ----------
def related(post, idx, n=6):
    others = [q for q in idx["posts"] if q["id"] != post["id"]]
    tagset = set(t.lower() for t in (post.get("tags") or []))
    def score(q):
        s = len(tagset & set(t.lower() for t in (q.get("tags") or []))) * 2
        if q.get("category_id") == post.get("category_id"): s += 1
        if q.get("issue_id") == post.get("issue_id"): s += 1
        return s
    ranked = sorted(others, key=lambda q: (-score(q), q.get("published_at") or ""), reverse=False)
    return ranked[:n]

# ---------- JSON-LD ----------
def post_ld(post, idx):
    cat = idx["cat"].get(post.get("category_id"), {})
    au = idx["au"].get(post.get("author_id"), {})
    iss = idx["iss"].get(post.get("issue_id"))
    url = post.get("canonical_url") or (SITE + "/stories/" + post["slug"])
    imgs = [post["hero_image_url"]] if post.get("hero_image_url") else []
    org = {"@type": "Organization", "@id": ORG_ID, "name": "PMN+",
           "alternateName": "Polynesian Music Network Plus", "url": SITE,
           "logo": SITE + "/shop/brand/pmn-plus-logo-black.png"}
    article = {
        "@type": post.get("schema_type") or "Article",
        "@id": url + "#article",
        "headline": trim(post["title"], 110),
        "description": post.get("seo_description") or trim(post.get("dek") or "", 155),
        "image": imgs,
        "datePublished": post.get("published_at"),
        "dateModified": post.get("updated_at") or post.get("published_at"),
        "author": {"@type": "Person", "name": au.get("name") or "PMN+",
                   "url": SITE + "/stories/author/" + (au.get("slug") or "pmn")},
        "publisher": {"@id": ORG_ID},
        "mainEntityOfPage": url,
        "articleSection": cat.get("name"),
        "keywords": ", ".join(post.get("keywords") or []),
    }
    crumbs = [("Home", SITE + "/"), ("Stories", SITE + "/stories")]
    if cat: crumbs.append((cat.get("name"), SITE + "/stories/" + cat.get("slug")))
    crumbs.append((post["title"], url))
    breadcrumb = {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]}
    graph = [article, breadcrumb, org]
    if iss:
        article["isPartOf"] = {"@type": "CollectionPage", "@id": SITE + "/digital-magazine/" + iss["slug"] + "#issue",
                               "name": "PMN+ Magazine — " + iss["title"]}
    return {"@context": "https://schema.org", "@graph": graph}

# ---------- pages ----------
def post_page(post, idx):
    cat = idx["cat"].get(post.get("category_id"), {})
    au = idx["au"].get(post.get("author_id"), {})
    iss = idx["iss"].get(post.get("issue_id"))
    url = post.get("canonical_url") or (SITE + "/stories/" + post["slug"])
    title = post.get("seo_title") or (post["title"] + " | PMN+")
    desc = post.get("seo_description") or trim(post.get("dek") or "", 155)
    kicker = (cat.get("name") or "").upper() + (" · COVER STORY" if post.get("is_cover_story") else "")
    hero = ""
    if post.get("hero_image_url"):
        hero = (f'<div class="ed-hero"><img src="{esc(post["hero_image_url"])}" alt="{esc(post.get("hero_alt") or post["title"])}">'
                f'<div class="grad"></div><div class="copy"><span class="ed-chip">{esc(kicker)}</span>'
                f'<h1>{esc(post["title"])}</h1><p class="ed-dek">{esc(post.get("dek") or "")}</p>'
                f'{byline(post, au)}</div></div>')
    else:
        hero = (f'<div class="ed-head"><span class="ey">{esc(kicker)}</span><h1>{esc(post["title"])}</h1>'
                f'<p>{esc(post.get("dek") or "")}</p>{byline(post, au)}</div>')
    crumb = (f'<div class="ed-crumb"><a href="/stories">Stories</a><span class="sep">/</span>'
             f'<a href="/stories/{esc(cat.get("slug"))}">{esc(cat.get("name"))}</a>'
             f'<span class="sep">/</span><span>{esc(trim(post["title"],40))}</span></div>')
    tags = "".join(f'<a class="ed-tag" href="/stories/tag/{esc(slugify(t))}">{esc(t)}</a>' for t in (post.get("tags") or []))
    mag_line = ""
    if iss:
        mag_line = (f' Originally published in <a href="/digital-magazine/{esc(iss["slug"])}">'
                    f'PMN+ Magazine, {esc(iss["title"])} ({esc(iss.get("period_label") or "")})</a>.')
    rel = related(post, idx)
    rail = "".join(rail_card(q, idx) for q in rel[:5])
    strip = ""
    issue_mates = [q for q in idx["by_issue"].get(post.get("issue_id"), []) if q["id"] != post["id"]][:3]
    if issue_mates and iss:
        strip = (f'<div class="ed-strip"><div class="ey">FROM THIS ISSUE</div>'
                 f'<h2>{esc(iss["title"])} · Digital Magazine</h2>'
                 f'<div class="grid3">{"".join(big_card(q, idx) for q in issue_mates)}</div></div>')
    body = f"""<div class="ed-wrap" data-post-slug="{esc(post['slug'])}" data-content-ref="{esc(post['slug'])}">
{crumb}
{hero}
<div class="ed-grid">
<article class="ed-article">
{post.get('body_html') or ''}
<div class="ed-tags">{tags}</div>
<p class="ed-rights">{esc(post.get('rights_note') or '')}{mag_line}</p>
{strip}
</article>
<aside class="ed-aside">
<h2 class="ed-rail-h">More Stories</h2>
<div class="ed-cards">{rail}</div>
<a class="ed-btn" href="/stories">Browse all stories &rarr;</a>
</aside>
</div>
</div>"""
    return page(title, desc, url, body=body, og_image=post.get("og_image_url") or post.get("hero_image_url"),
                og_type="article", ld=post_ld(post, idx),
                head_extra=f'<meta property="article:published_time" content="{esc(post.get("published_at"))}">'
                           f'<meta property="article:author" content="{esc(au.get("name") or "PMN+")}">'
                           f'<meta property="article:section" content="{esc(cat.get("name"))}">')

def byline(post, au):
    bits = [f'<span class="who">{esc(au.get("name") or "PMN+")}</span>']
    if post.get("published_at"):
        bits.append(f'<span class="dot"></span><span>{fmt_date(post["published_at"])}</span>')
    if post.get("reading_minutes"):
        bits.append(f'<span class="dot"></span><span>{int(post["reading_minutes"])} min read</span>')
    return '<div class="ed-byline">' + "".join(bits) + "</div>"

def fmt_date(iso):
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%B %-d, %Y")
    except Exception:
        return iso or ""

def index_page(title, desc, canonical, heading, eyebrow, posts, idx, *, cats_nav=None, intro="", on=None):
    og = next((p.get("hero_image_url") for p in posts if p.get("hero_image_url")), None)
    cards = "".join(big_card(p, idx) for p in posts) or '<p style="color:var(--dim)">No stories yet.</p>'
    cat_links = ""
    if cats_nav:
        cat_links = '<nav class="ed-cats"><a href="/stories"' + (' class="on"' if on is None else "") + ">All</a>" + "".join(
            f'<a href="/stories/{esc(c["slug"])}"' + (' class="on"' if on == c["slug"] else "") + f'>{esc(c["name"])}</a>'
            for c in cats_nav) + "</nav>"
    body = (f'<div class="ed-wrap"><div class="ed-head"><span class="ey">{esc(eyebrow)}</span>'
            f'<h1>{esc(heading)}</h1>{("<p>"+esc(intro)+"</p>") if intro else ""}{cat_links}</div>'
            f'<div class="ed-grid-cards">{cards}</div></div>')
    return page(title, desc, canonical, body=body, og_image=og)

def magazine_page(iss, idx):
    posts = idx["by_issue"].get(iss["id"], [])
    url = SITE + "/digital-magazine/" + iss["slug"]
    title = iss.get("seo_title") or ("PMN+ Digital Magazine — " + iss["title"])
    desc = iss.get("seo_description") or trim(iss.get("intro") or "", 155)
    cover = iss.get("cover_image_url")
    cov = ""
    if cover:
        cov = (f'<div class="ed-mag-cover"><img src="{esc(cover)}" alt="PMN+ {esc(iss["title"])} cover">'
               f'<div class="grad"></div><div class="copy"><span class="ed-chip">DIGITAL MAGAZINE</span>'
               f'<h1>{esc(iss["title"])}</h1><p class="ed-dek">{esc(iss.get("intro") or "")}</p>'
               f'<div class="ed-byline"><span>{esc(iss.get("period_label") or "")}</span></div></div></div>')
    toc = "".join(big_card(p, idx) for p in posts)
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url + "#issue", "name": title, "url": url,
         "description": desc, "isPartOf": {"@id": ORG_ID},
         "hasPart": [SITE + "/stories/" + p["slug"] for p in posts]},
        {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": SITE + "/stories/" + p["slug"], "name": p["title"]}
            for i, p in enumerate(posts)]},
        {"@type": "Organization", "@id": ORG_ID, "name": "PMN+", "url": SITE,
         "logo": SITE + "/shop/brand/pmn-plus-logo-black.png"}]}
    body = (f'<div class="ed-wrap"><div class="ed-crumb"><a href="/digital-magazine">Digital Magazine</a>'
            f'<span class="sep">/</span><span>{esc(iss["title"])}</span></div>{cov}'
            f'<div class="ed-strip"><div class="ey">IN THIS ISSUE</div>'
            f'<h2>{len(posts)} stories</h2><div class="grid3">{toc}</div></div></div>')
    return page(title, desc, url, body=body, og_image=cover, og_type="website", ld=ld)

# ---------- feeds ----------
def rss(posts, idx):
    items = []
    for p in sorted(posts, key=lambda q: q.get("published_at") or "", reverse=True)[:50]:
        url = SITE + "/stories/" + p["slug"]
        pub = p.get("published_at") or ""
        try:
            pub = datetime.fromisoformat(pub.replace("Z", "+00:00")).strftime("%a, %d %b %Y %H:%M:%S +0000")
        except Exception:
            pass
        items.append(f"""<item><title>{esc(p['title'])}</title><link>{esc(url)}</link>
<guid isPermaLink="true">{esc(url)}</guid><pubDate>{esc(pub)}</pubDate>
<description>{esc(p.get('seo_description') or p.get('dek') or '')}</description>
{('<enclosure url="'+esc(p['hero_image_url'])+'" type="image/jpeg"/>') if p.get('hero_image_url') else ''}</item>""")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
<title>PMN+ Stories</title><link>{SITE}/stories</link>
<description>Pacific music, sport and culture from PMN+.</description><language>en-us</language>
{''.join(items)}
</channel></rss>"""

def sitemap(posts, issues, cats, authors):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    urls = [(SITE + "/stories", now), (SITE + "/digital-magazine", now)]
    for c in cats: urls.append((SITE + "/stories/" + c["slug"], now))
    for a in authors: urls.append((SITE + "/stories/author/" + a["slug"], now))
    for p in posts:
        lm = (p.get("updated_at") or p.get("published_at") or now)[:10]
        urls.append((SITE + "/stories/" + p["slug"], lm))
    for i in issues:
        lm = (i.get("updated_at") or i.get("published_at") or now)[:10]
        urls.append((SITE + "/digital-magazine/" + i["slug"], lm))
    body = "".join(f"<url><loc>{esc(u)}</loc><lastmod>{lm}</lastmod></url>" for u, lm in urls)
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + body + "</urlset>"

# ---------- write helpers ----------
def write(relpath, content):
    path = os.path.join(ROOT, relpath)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(content)
    return relpath

# ---------- main ----------
def main():
    data = load_data(sys.argv)
    posts = [p for p in data["posts"] if p.get("status") == "published"]
    issues = [i for i in data["issues"] if i.get("status") == "published"]
    cats = data["categories"]; authors = data["authors"]
    idx = {
        "posts": posts,
        "cat": {c["id"]: c for c in cats},
        "au": {a["id"]: a for a in authors},
        "iss": {i["id"]: i for i in issues},
        "by_issue": {},
    }
    for p in posts:
        idx["by_issue"].setdefault(p.get("issue_id"), []).append(p)
    for k in idx["by_issue"]:
        idx["by_issue"][k].sort(key=lambda q: q.get("order_in_issue") or 0)
    newest = sorted(posts, key=lambda q: q.get("published_at") or "", reverse=True)

    out = []
    # copy assets
    os.makedirs(os.path.join(ROOT, "assets", "content"), exist_ok=True)
    for f in ("story.css", "shop-this-story.css", "shop-this-story.js"):
        src = os.path.join(HERE, f)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(ROOT, "assets", "content", f))
    # posts
    for p in posts:
        out.append(write(f"stories/{p['slug']}/index.html", post_page(p, idx)))
    # stories index
    out.append(write("stories/index.html", index_page(
        "Pasifika Stories | PMN+",
        "Pasifika stories — Pacific music, sport, entertainment and culture, from the people who live it. PMN+.",
        SITE + "/stories", "Pasifika Stories", "PMN+", newest, idx, cats_nav=cats,
        intro="No one tells our stories better than we can.")))
    # category hubs
    for c in cats:
        cp = [p for p in newest if p.get("category_id") == c["id"]]
        out.append(write(f"stories/{c['slug']}/index.html", index_page(
            f"{c['name']} | PMN+ Stories", f"PMN+ {c['name'].lower()} stories.",
            SITE + "/stories/" + c["slug"], c["name"], "Stories", cp, idx, cats_nav=cats, on=c["slug"])))
    # author pages
    for a in authors:
        ap = [p for p in newest if p.get("author_id") == a["id"]]
        out.append(write(f"stories/author/{a['slug']}/index.html", index_page(
            f"{a['name']} | PMN+", f"Stories by {a['name']}, {a.get('role') or 'PMN+'}.",
            SITE + "/stories/author/" + a["slug"], a["name"], a.get("role") or "Writer", ap, idx)))
    # tag pages
    tags = {}
    for p in newest:
        for t in (p.get("tags") or []):
            tags.setdefault(slugify(t), {"label": t, "posts": []})["posts"].append(p)
    for tslug, t in tags.items():
        out.append(write(f"stories/tag/{tslug}/index.html", index_page(
            f"{t['label']} | PMN+ Stories", f"PMN+ stories tagged {t['label']}.",
            SITE + "/stories/tag/" + tslug, t["label"], "Tagged", t["posts"], idx)))
    # magazine
    for i in issues:
        out.append(write(f"digital-magazine/{i['slug']}/index.html", magazine_page(i, idx)))
    out.append(write("digital-magazine/index.html", index_page(
        "Digital Magazine | PMN+", "Every issue of the PMN+ digital magazine.",
        SITE + "/digital-magazine", "Digital Magazine", "PMN+", [], idx) if not issues else
        page("Digital Magazine | PMN+", "Every issue of the PMN+ digital magazine.", SITE + "/digital-magazine",
             body='<div class="ed-wrap"><div class="ed-head"><span class="ey">PMN+</span><h1>Digital Magazine</h1>'
                  '<p>Every issue — read online, story by story.</p></div><div class="ed-grid-cards">' +
                  "".join(
                      f'<a class="ed-card" href="/digital-magazine/{esc(i["slug"])}">'
                      f'{("<img class=ph loading=lazy src=\"" + esc(i.get("cover_image_url")) + "\" alt=\"" + esc(i["title"]) + " cover\">") if i.get("cover_image_url") else "<div class=ph></div>"}'
                      f'<div class="b"><span class="cat">ISSUE</span><span class="t">{esc(i["title"])}</span>'
                      f'<span class="d">{esc(i.get("intro") or "")}</span>'
                      f'<span class="by">{esc(i.get("period_label") or "")}</span></div></a>'
                      for i in sorted(issues, key=lambda x: x.get("published_at") or "", reverse=True)) +
                  "</div></div>")))
    # feeds
    out.append(write("stories/feed.xml", rss(posts, idx)))
    out.append(write("sitemap-stories.xml", sitemap(posts, issues, cats, authors)))

    print(f"generated {len(out)} files:")
    for r in out: print("  " + r)
    print("\nNOTE: add  Sitemap: %s/sitemap-stories.xml  to robots.txt (once)." % SITE)

if __name__ == "__main__":
    main()
