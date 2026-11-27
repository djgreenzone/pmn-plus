# Business rules

The site, Shopify, Klaviyo emails and Google Merchant Center must all say the same thing. When one changes, change all.

## Products and sizes (as of Oct 6, 2026)
| Line | Colours | Sizes | Price |
|---|---|---|---|
| Standard tees (685/676, RLWC26, Player, Silver Blackout, PMN+ Logo Tee) | Black | S–6XL | $49.95 |
| Standard tees | Red (Tonga) / Royal blue (Samoa) | S–6XL | $49.95 |
| Crest Oversized Tee (heavyweight) | Black | S–6XL | $60 |
| Snapbacks / truckers / dad hat | — | One size | $35–55 |

- Prices: **Shopify is the source of truth**; keep `PRODUCTS[].price` in sync for SEO/feeds.
- Standard tee blank: 5.3 oz (180 gsm) 100% ring-spun cotton, regular fit. Oversized: 8.2 oz (275 gsm), boxy fit.
- **Never name the blank manufacturer on the site.** Describe weight, fabric and fit instead.
- White tees and other drafts in Shopify are **not** sold; don't publish them.

## Buy 2 tees, get 1 free (Black Friday weekend 2026: Fri Nov 27 to Mon Nov 30, ends 11:59pm PST)
- Shopify automatic Buy X Get Y discount "Buy 2 tees, get 1 free" (id `1544616935623`, ends 2026-12-01T07:59:59Z).
  For the weekend it **replaces** the standing "Buy 3 tees, get 1 free" (id `1536209322183`), which was deactivated on Nov 27.
- Any 2 tees qualify (oversized included). The **free tee** must be a **black, red or royal standard tee in L, XL or 2XL**.
  Oversized tees are never the free one. Same buy/get products and variants as the Buy 3 offer.
- 100% off one tee per 3 tees, **max 2 free per order**.
- Doesn't combine with discount codes or the Game Day Set (Shopify applies the better discount). Doesn't combine with the
  Black Friday 30% off either: Shopify gives each cart whichever saves more (1-2 tees: 30%; 3 tees: the free tee).
- Site mirrors this in `bx()` / `BX_BUY` / `FREE_SZ` (bag meter + messages), the offer bar and account page. Every new tee
  product must be added to the discount.
- **After the sale:** reactivate "Buy 3 tees, get 1 free" in Shopify and `git revert` the commit that switched the site to Buy 2
  (it restores `BX_BUY=3`, `BUNDLE_OFF=10`, the product-page Game Day Set box, the SEO/feed copy and the offer bar text in `assets/pmn-config.js`).
  Also reactivate "Game Day Set: $10 off" (id `1535948751047`), which was deactivated for the weekend.

## Black Friday 30% off (Nov 27 to Nov 30, 2026)
- Shopify automatic discount "Black Friday 30% Off" (id `1544614904007`), store-wide, no code, doesn't combine with any other
  discount or code. Ends 2026-12-01T07:59:59Z (Mon 11:59pm PST). Free US shipping stays.

## Other offers and codes
| Offer | Rule |
|---|---|
| Game Day Set | $10 off a tee + hat in the same order (automatic). Stacks with WELCOME codes. |
| WELCOME10 / WELCOME20 | 10% (email) / 20% (email + SMS) sign-up codes, unique, first order, one per customer. |
| COMEBACK10 | Abandoned-checkout code, one per customer. |
| MEMBER10 | 10% off every order for signed-in members (customer tag `pmn-member`, segment "PMN+ members"). Shown on the account page once a WELCOME code has been used. |
| Member gift | Surprise item in every member order (JQF adds it; orders tagged `member-gift`). |
- One code per order.

## Shipping, production, returns
- USA only. **Free shipping on every order** (no minimum) to the 48 contiguous states + DC, since Oct 22, 2026. Hawaii, Alaska,
  US territories (Guam etc.) and APO/FPO are **not** free: they pay a flat **$15** "Standard shipping" (since Oct 23). Shopify zone
  "Contiguous US (free shipping)" = flat $0; zone "HI, AK, territories and APO (paid)" = one flat $15 rate (no carrier-calculated rates).
  Merchant Center shipping must say the same. Express shipping is parked until DJ decides on fast options.
- Made to order: printing 2–4 business days + shipping 1–5 business days (Fulfill Engine Standard, contiguous US) ≈ 3–9 business days.
  The site ETA (`ETA` in `site2/index.html`), `POLICY` in `seo_content.py`, the shipping page and the feed transit times must match.
- **All sales final** (made to order). Damaged, defective, misprinted or incorrect items reported within **7 days** of
  delivery with photos → replacement, store credit or refund once approved.
- Contact: info@islandcitymediagroup.com · 8545 W Warm Springs Rd A4, Las Vegas, NV 89113.
- Payments: cards, Apple Pay, Google Pay, Shop Pay (incl. Shop Pay Installments) and Afterpay (pay in 4). Afterpay is advertised in the offer bar, ticker, team section, product pages and bag.
  Product page + bag use Afterpay's own `<square-placement>` widget (official logo, MPID/placement ids in `AP` in
  `site2/index.html`); our text line is the fallback if their script is blocked. Say "Pay in 4" / "interest-free", never "no fees".
  Flags: `payLater:false` hides it on product pages/bag, `offerAfterpay:false` drops it from the offer bar.

## Brand and wording
- Never "official", "licensed" or similar for Toa Samoa / Mate Ma'a Tonga merch. They're independent supporter designs.
  The Player Tee's 00 number is generic (no real player names).
- Team names: "Toa Samoa", "Mate Ma'a Tonga" (with the apostrophe). 685 = Samoa's calling code, 676 = Tonga's.
- Colours: Samoa = royal blue world, Tonga = red world, PMN+ = black/neutral.
- Voice: proud, warm, short; talks to fans as family. No fake urgency or invented stock counts.
- Headings Bebas Neue, body Instrument Sans.
- Footer pill "Powered by ICM Creative" (icmcreative.com) on every page.

- **Story "Shop this story" cards** also show the sale price + 30% OFF chip: set `SALE = 0` in `_source/content/shop-this-story.js`
  (and copy it to `assets/content/`) after the sale. It covers every story, since the script is shared.

## End-of-sale checklist (Tue Dec 1, right after Mon Nov 30 11:59pm PST)
Shopify (the two sale discounts end themselves at 07:59:59Z Dec 1; the old ones were given an end date, so clear it):
1. "Buy 3 tees, get 1 free" (`gid://shopify/DiscountAutomaticNode/1536209322183`): set `endsAt` to null so it is ACTIVE again.
2. "Game Day Set: $10 off" (`.../1535948751047`): set `endsAt` to null.
3. Leave "Black Friday 30% Off" (`.../1544614904007`) and "Buy 2 tees, get 1 free" (`.../1544616935623`) ended.
Site (one PR to main, then check /shop, a product page, the bag, a story, the homepage):
4. `_source/site2/index.html`: `SALE=0`, `BX_BUY=3`, `BUNDLE_OFF=10`, remove the `#pDeal` hide rule; rebuild with the pipeline in CLAUDE.md.
5. `_source/content/shop-this-story.js` and `assets/content/shop-this-story.js`: `SALE = 0`.
6. `assets/pmn-config.js`: delete the 4 `offer*` keys (offerText, offerCta, offerLink, offerFine).
7. `index.html`: change the `.bf-pill` eyebrow in the "Who you reppin" section back to "RLWC 2026 &middot; Toa Samoa vs Mate Ma&#8217;a Tonga" (drop the pill span), and replace the Black Friday line under the best-sellers carousel with the normal shipping line.
8. Restore the SEO copy and homepage promo line per the sections above.
9. Mark red/blue 4XL-6XL sizes as needed (they are sold out in Shopify by inventory tracking at 0; restock = set quantity).
- **Black Friday banners** (remove after the sale): in `index.html` delete the block between `<!-- BF-BANNER` and `<!-- /BF-BANNER -->` and the `/* BF-BANNER` CSS block;
  in `_source/site2/index.html` delete the `.bf-rib` line between the same comment markers in the hero and the `/* BF-BANNER */` CSS block, then rebuild the shop.
