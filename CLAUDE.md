# PMN+ Shop — read this first

polynesianmusicnetwork.com: the PMN+ (Polynesian Music Network Plus) site and merch store.
Static site on **Vercel**, checkout on **Shopify** (headless), accounts on **Supabase**, email/SMS on **Klaviyo**,
print-on-demand by **JQF Printing** via **Fulfill Engine**. Owner: DJ Green (ammon@islandcitymediagroup.com).

Full docs live in `docs/`. Read the one that matches the task before changing anything:

| Task | Read |
|---|---|
| How the pieces fit, which file controls what | `docs/ARCHITECTURE.md` |
| Add a product, change sizes/prices, deploy, Shopify admin jobs | `docs/RUNBOOK.md` |
| Something is broken | `docs/TROUBLESHOOTING.md` |
| Offer rules, sizes, codes, shipping/returns wording, brand rules | `docs/BUSINESS-RULES.md` |
| Accounts, logins, env vars, who has access | `docs/ACCESS.md` |

## Golden rules
1. **Never hand-edit generated files.** These are build output; edit the source and rebuild:
   - `shop/index.html`, `shop/<slug>/index.html`, `shop/search.json`, `shop/og/*`, `sitemap.xml`, `merchant-center-feed.txt`
     ← `_source/site2/index.html` + `_source/*.py` / `*.js`
   - `account/index.html` ← `_source/account/template.html`
   - `api/_account.js`, `api/account/*.js` ← `_source/account/api/...` (the build copies them over)
   - `assets/pmn-nav.css`, `assets/pmn-nav.js` and the **site header** on `index.html`, `/shop` and `/account` ← `_source/nav/`
2. **Hand-edited files** (no build step): `index.html` (homepage, except its header), `about/`, `shipping/`, `returns/`,
   `contact/`, `terms/`, `privacy-policy/`, `sms-terms/`, `404.html`, `api/reels.js`, `assets/pmn-config.js`,
   `vercel.json`, `sitemap.xsl`, `robots.txt`. The **footer** markup/CSS is duplicated in each page, so a footer change
   goes to all of them (the account page copies the homepage footer at build time).
3. **Rebuild after any shop change** (from `_source/`):
   ```
   python3 seo_content.py && python3 seo_build.py && python3 seo_inject.py && python3 make_og.py && python3 make_shop.py ../shop/index.html
   ```
   `make_shop.py` uses exact-string replacements with asserts. If it fails with an AssertionError, the source text it
   expects changed: fix the `rep()` call, don't delete the assert.
4. **Shopify is the source of truth for price, variants and stock.** The site reads them live via the Storefront API.
   A product only works at checkout if it is **published to the "Polynesian Music Network Headless" sales channel**.
5. **Every new Shopify tee must be added to the "Buy 3 tees, get 1 free" discount** (see `docs/RUNBOOK.md`), or the offer
   silently stops working for it.
6. **No manufacturer/blank brand names on the site** (the site says "5.3 oz midweight", not the blank's brand), and
   **never "official"** for team merch: PMN+ is not licensed by the rugby league bodies.
7. **Secrets never go in the repo.** Only public keys live in `assets/pmn-config.js`. Server keys are Vercel env vars.
8. Test locally before pushing: `python3 -m http.server 8765` from the repo root, open `http://localhost:8765/shop/`.
   Don't `pkill -f` a pattern that appears in your own command line (it kills your shell).

## Workflow (two people on the site)
- Work on a **branch**, push it, and use the **Vercel preview URL** Vercel posts on the commit/PR to check it.
- Open a PR into `main`; merge when the preview looks right. Merging to `main` deploys production.
- Small urgent fixes can go straight to `main`, but say so in the commit message.
- DJ's own Claude sessions can't push (GitHub 403): they commit, export `git format-patch` and DJ applies it with
  `git am`. Before starting work, always `git fetch && git status` so you don't build on a stale copy.
- Commit messages: what changed and why, in plain English.

## Quick facts
- Live: https://www.polynesianmusicnetwork.com · Shop: `/shop` · Product: `/shop/<slug>` · Account: `/account`
- Shopify store: `polynesianmusicnetwork.myshopify.com` · Supabase project `pmn-plus` (`zacfssfjlmixnqhjuoed`)
- Klaviyo company/public key `T9JJzp` · GA4 `G-KEQ8HPTH9W` · Meta pixel `1983591485663494` · Clarity `ys5h8s9j8m`
- Google Merchant Center `5866912143` (feed = `/merchant-center-feed.txt`, built by `seo_build.py`; don't also connect
  Shopify's Google channel, it duplicates products)
- Search Console: domain property `sc-domain:polynesianmusicnetwork.com`
- Python 3 + Pillow for builds; `ffmpeg` only for new 360° spins (`_source/tools/add_spin.py`).
