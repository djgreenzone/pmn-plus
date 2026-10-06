# Runbook

Step-by-step for the jobs that come up. Every shop change ends with **rebuild → check locally → branch → preview → merge**.

## 0. Setup (once)

```
git clone https://github.com/djgreenzone/pmn-plus.git && cd pmn-plus
python3 -m pip install Pillow          # builds
brew install ffmpeg                    # only for new 360° spins
```

## 1. Everyday workflow

```
git checkout main && git pull
git checkout -b fix/short-description
# … edit sources …
cd _source
python3 seo_content.py && python3 seo_build.py && python3 seo_inject.py && python3 make_og.py && python3 make_shop.py ../shop/index.html
cd .. && python3 -m http.server 8765      # open http://localhost:8765/shop/
git add -A && git commit -m "What changed and why"
git push -u origin fix/short-description
```
Open the PR on GitHub. Vercel posts a **Preview** link on the PR; check it on desktop and phone, then merge.
Merging to `main` deploys production in about a minute.

- Only changed hand-edited pages (homepage, footer, policies)? No rebuild needed, **except** that the homepage header
  and the account page footer come from the build, so run `make_shop.py` if you changed the homepage footer.
- `make_og.py` is only needed when a product, its name or its photos change (it's the slowest step).
- The build prints a title/description length table. Keep titles ≤60 characters and descriptions ≤160.

## 2. Add a new product (tee example)

**Shopify first**
1. Product exists (Fulfill Engine creates it), status **Active**, variants named `Color / Size` (e.g. `Black / XL`).
2. Price set on every variant.
3. **Publish it to the "Polynesian Music Network Headless" sales channel** (product page → Publishing → Manage,
   or Settings → Apps and sales channels). Without this the site can show it but **checkout fails**.
4. Remove variants we don't sell (e.g. red S, M, 4XL, 5XL) in Fulfill Engine, or leave them: the site never offers them.
5. Add it to the **Buy 3 tees, get 1 free** discount (Discounts → Buy 3 tees, get 1 free):
   - *Customer buys*: add the product.
   - *Customer gets*: add only the **L, XL, 2XL** variants, and only black, red or royal standard tees (never oversized).
6. Don't publish white or draft variants we aren't selling.

**Images: 360° spin + stills**
You need a turntable video (`.mov` with transparency, e.g. Pacdora ProRes 4444 export, 1080², ~4 s) and transparent
2K stills (front, ¾ front-right, right side, back, ¾ front-left).
```
mkdir -p /tmp/spin/my-tee && ffmpeg -v error -i turn.mov -pix_fmt rgba /tmp/spin/my-tee/f%03d.png
ls /tmp/spin/my-tee | wc -l                                  # e.g. 121
```
Find the loop length: the frame after a full turn repeats `f001` (usually 91 or 92 frames; frames after it are held).
Then:
```
cd _source
python3 tools/add_spin.py toa-newtee-black toa-samoa-newtee-tee-black /tmp/spin/my-tee 91 \
  0=front.png 48=front-right.png 92=right.png 180=back.png 312=front-left.png
```
- Args: site id, SEO slug (becomes file names + the page URL), frames folder, loop length, then `angle=still` pairs.
- Angles: 0 front, ~48 ¾ front-right (sleeve with the PMN+ badge), ~92 side, 180 back, ~312 ¾ front-left. If unsure which
  angle a still matches, compare it with the spin frames; the existing tees use these angles.
- It writes `shop/frames/<id>/` and `shop/hires/<id>/` and **prints a `META` JSON entry**. Copy it.
- Takes 30–90 s per product. Run several in the background (`&`) for a batch.

**Site code**
1. `_source/site2/index.html`
   - Paste the printed entry into `const META={…}`.
   - Add a `PRODUCTS` entry (copy a sibling: same team + colour gives the right `world/glow/flood/wordc` colours).
     Set `opts` to `[self, other colour, other team's version]`. Position in the array = position in the hero carousel.
   - Add `COPY["<id>"]` (one line + 3 points, describe what's printed and where).
   - If the product page should open on the back print, add `"<id>":180` to `REST`.
2. `_source/seo_content.py`: add `P["<id>"]` (copy a sibling; state the size range: black "S–5XL", colour "L–3XL").
   Never write "official".
3. `_source/shopify_layer.js`: add `"<id>":["<shopify-handle>","<Color value exactly as in Shopify>"]`.
   Royal blue is `"Bright Royal"` in Shopify.
4. `_source/seo_build.py` → `GROUP`: add both colourways under one group id so Google sees one product with colours.
5. `_source/account/template.html`: add the Shopify title pattern to `SITE_ID`'s list `M`, the handle to `HANDLE`, and the
   Shopify numeric product id to `KL_PID` (for reviews and Buy again).
6. Rebuild, check `/shop/<slug>` locally (sizes, spin, stills, colour swatches), push a branch, check the preview.

**After it's live**
- Add 4 tees including the new one (L–2XL) to the bag and go to checkout: the line must be accepted and "Buy 3 tees,
  get 1 free" must show. Use a 100%-off test code or cancel the order.
- Search Console → Sitemaps → resubmit `sitemap.xml`; URL inspection → Request indexing for the new pages.
- Merchant Center picks up the feed on its next daily fetch.

## 3. Change a price
Change it in **Shopify** (all variants). The site shows the Shopify price live. Also update `price:` in the product's
`PRODUCTS` entry and rebuild, because the pre-rendered pages, structured data and Merchant feed use that value.

## 4. Change which sizes a colour is sold in
- `BLANK` in `site2/index.html` (`fwjCore` = black standard tees, `fwjColour` = red/royal, `oversized`) and `blankFor()`.
- `sizes()` in `seo_build.py` (structured data + Merchant feed).
- Size wording in `seo_content.py` copy.
- The Buy 3 get 1 discount's *Customer gets* variants in Shopify, if the free sizes change.
- Size chart values: `FWJ_CHART` (standard tees) / `HEAVY_CHART` (oversized), inches measured flat.

## 5. Sold out, hide, unhide
- Sold out (whole product): add the id to `SOLD` in `shopify_layer.js`. Single sizes follow Shopify stock automatically.
- Hide a product from the site: add the id to `HIDE` in `make_shop.py` (currently the two curved-bill snapbacks).
- Rebuild after either.

## 6. Offers and discount codes
All live in **Shopify → Discounts**. Rules are in `BUSINESS-RULES.md`. If a rule changes, update in the same PR:
- `bx()` / `FREE_SZ` and the bag messages in `site2/index.html` (search "Buy 3 tees, get 1 free").
- The bag fine print `#bxFine` in `site2/index.html` and the offer bar tooltip in `nav/pmn-nav.js`.
- Klaviyo email copy that mentions the offer (Added to Cart, Abandoned Checkout, Welcome).

## 7. Policies, shipping, returns wording
Hand-edited pages `shipping/`, `returns/`, `terms/`, `privacy-policy/`, plus `POLICY` in `seo_content.py` (feeds the
product FAQ and structured data). Keep **Shopify → Settings → Policies** and **Merchant Center** returns/shipping
identical to the site.

## 8. Footer / header
- Header: `_source/nav/` (`nav_build.py` markup, `pmn-nav.css`, `pmn-nav.js`), rebuild. The static pages (`about/`,
  `shipping/` …) carry their own copy of the header markup; update those by hand if the markup changes.
- Footer: edit it in **every** hand-edited page (`index.html`, `about/`, `shipping/`, `returns/`, `contact/`, `terms/`,
  `privacy-policy/`, `sms-terms/`, `404.html`), then rebuild so the account page picks it up from `index.html`.

## 9. Redirects
`vercel.json` → `redirects`. Use `permanent: true` (301) for moved pages. Keep `trailingSlash: false`.

## 10. Feature flags (no rebuild)
`assets/pmn-config.js`: `payLater:false` hides the pay-in-4 line, `offerBar:false` hides the top offer bar,
`accountsLive`, `google`, `apple` (sign-in buttons), `analytics` IDs (blank = off).

## 11. Environment variables
Vercel → Project → Settings → Environment Variables (Production + Preview). After changing one, **redeploy**
(Deployments → ⋯ → Redeploy). Names are listed in `ACCESS.md`.

## 12. Shopify admin jobs
| Job | Where |
|---|---|
| Publish a product to the site | Product → Publishing → **Polynesian Music Network Headless** |
| Buy 3 get 1 eligible products/sizes | Discounts → Buy 3 tees, get 1 free |
| Member pricing | Discounts → MEMBER10 (segment "PMN+ members" = customer tag `pmn-member`) |
| Payout bank | Settings → Payments → Shopify Payments → Payout account (currently Chase) |
| Afterpay | Settings → Payments → Add payment method → **Afterpay US (New)** (needs Afterpay Business Hub) |
| Checkout tracking | Settings → Customer events (paste `_source/analytics/shopify-checkout-pixel.js`) |
| Refund/return policy text | Settings → Policies |
| Shipping rates | Settings → Shipping and delivery (Standard $8, Express $15). Must match Merchant Center. |

## 13. Klaviyo (email/SMS)
Account: ICM (company `T9JJzp`). Lists: PMN+ Launch List `SLSsGL`, PMN+ Newsletter `Sggasa`.
Flows: Welcome `XUhuh8`, Review request `WEXsca` (template `W7aDFd`), Added to Cart (4h), Abandoned Checkout,
Post-purchase `TyUvSh`. Master email template `Rfxuvi`. Coupons WELCOME10/WELCOME20 are unique codes generated in
Klaviyo and imported into Shopify. The site's server function `/api/account/reviews` uses `KLAVIYO_PRIVATE_KEY`.

## 14. Supabase
Project `pmn-plus` (`zacfssfjlmixnqhjuoed`). Schema and row-level security: `_source/account/schema.sql`. Auth email
template: `_source/account/email-signin.html` (paste into Supabase → Auth → Email templates). SMTP is Resend
(`no-reply@polynesianmusicnetwork.com`). Google sign-in uses Google Cloud project "PMN Plus".
