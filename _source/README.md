# PMN+ site source (not published)

This folder holds the editable sources the live site is built from. Vercel ignores it (see `/.vercelignore`).

## What's what
- `site2/index.html` – editable source of the shop page (product data, layout, 360° viewer, cart).
- `make_shop.py` – turns the source into the live `/shop/index.html`. It adds Klaviyo sign-ups, Shopify prices/variants/checkout, cart upgrades, deep links, hidden products (`HIDE`) and sold-out items.
- `shopify_layer.js` – maps site products to Shopify handles (`SHOPIFY_MAP`) and lists sold-out items (`SOLD`).
- `shopify_checkout.js` – cart → Shopify checkout, discount codes, auto-applied welcome codes.
- `seo_content.py` → `seo_content.json` → `seo_build.py` → `seo_inject.py` – SEO copy, structured data, feed and sitemap.

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
- **SEO copy changed:** `python3 seo_content.py && python3 seo_build.py && python3 seo_inject.py`, then rebuild.
