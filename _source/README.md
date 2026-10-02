# PMN+ site source (not published)

This folder holds the editable sources the live site is built from. Vercel ignores it (see `/.vercelignore`).

## What's what
- `site2/index.html` – editable source of the shop page (product data, layout, 360° viewer, cart).
- `make_shop.py` – turns the source into the live `/shop/index.html`. It adds Klaviyo sign-ups, Shopify prices/variants/checkout, cart upgrades, deep links, hidden products (`HIDE`) and sold-out items.
- `shopify_layer.js` – maps site products to Shopify handles (`SHOPIFY_MAP`) and lists sold-out items (`SOLD`).
- `shopify_checkout.js` – cart → Shopify checkout, discount codes, auto-applied welcome codes.
- `seo_content.py` → `seo_content.json` → `seo_build.py` → `seo_inject.py` – SEO copy, structured data, feed and sitemap.
- `seo_routes.py` – run automatically by `make_shop.py`. Gives every product and collection its own URL (`/shop/<product>`, `/shop/toa-samoa` …), writes a pre-rendered page for each into `/shop/<slug>/index.html` (own title, description, canonical, share image, structured data and visible content) and writes `/sitemap.xml`.
- `make_og.py` – makes the 1200×630 share image for each product in `/shop/og/` (needs Pillow). Re-run when a product or its photos change.

The homepage (`/index.html`) and `/api/reels.js` are edited directly in the repo; they have no build step.

## Rebuild the shop page
```
cd _source
python3 make_shop.py ../shop/index.html
```
Then commit and push as usual.

## Common changes
- **Mark something sold out / back in stock:** edit the `SOLD` list in `shopify_layer.js`, rebuild.
- **Connect a new Shopify product:** add it to `SHOPIFY_MAP` in `shopify_layer.js`, rebuild.
- **Hide / unhide a product:** edit `HIDE` in `make_shop.py`, rebuild.
- **SEO copy changed / product added:** `python3 seo_content.py && python3 seo_build.py && python3 seo_inject.py && python3 make_og.py`, then rebuild.
