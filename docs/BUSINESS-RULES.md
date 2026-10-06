# Business rules

The site, Shopify, Klaviyo emails and Google Merchant Center must all say the same thing. When one changes, change all.

## Products and sizes (as of Oct 6, 2026)
| Line | Colours | Sizes | Price |
|---|---|---|---|
| Standard tees (685/676, RLWC26, Player, Silver Blackout, PMN+ Logo Tee) | Black | S–5XL (6XL once set up in Fulfill Engine) | $45 |
| Standard tees | Red (Tonga) / Royal blue (Samoa) | **L–3XL only**; S, M, 4XL, 5XL shown crossed out | $45 |
| Crest Oversized Tee (heavyweight) | Black | S–5XL | $60 |
| Snapbacks / truckers / dad hat | — | One size | $35–55 |

- Prices: **Shopify is the source of truth**; keep `PRODUCTS[].price` in sync for SEO/feeds.
- Standard tee blank: 5.3 oz (180 gsm) 100% ring-spun cotton, regular fit. Oversized: 8.2 oz (275 gsm), boxy fit.
- **Never name the blank manufacturer on the site.** Describe weight, fabric and fit instead.
- White tees and other drafts in Shopify are **not** sold; don't publish them.

## Buy 3 tees, get 1 free
- Shopify automatic Buy X Get Y discount "Buy 3 tees, get 1 free" (id `1536209322183`).
- Any 3 tees qualify (oversized included). The **free tee** must be a **black, red or royal standard tee in L, XL or 2XL**.
  Oversized tees are never the free one.
- 100% off one tee per 4 tees, **max 2 free per order**.
- Doesn't combine with discount codes or the Game Day Set (Shopify applies the better discount). Combines with shipping discounts.
- Site mirrors this in `bx()` / `FREE_SZ` (bag meter + messages) and fine print. Every new tee product must be added to the discount.

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
- USA only (all 50 states). Standard **$8**, Express **$15**. Free shipping over $100 is **not** live; don't advertise it.
- Made to order: printing 2–4 business days + shipping 3–7 business days ≈ 5–11 business days.
- **All sales final** (made to order). Damaged, defective, misprinted or incorrect items reported within **7 days** of
  delivery with photos → replacement, store credit or refund once approved.
- Contact: info@islandcitymediagroup.com · 8545 W Warm Springs Rd A4, Las Vegas, NV 89113.
- Payments: cards, Apple Pay, Google Pay, Shop Pay (incl. Shop Pay Installments). Afterpay being added (Oct 6).

## Brand and wording
- Never "official", "licensed" or similar for Toa Samoa / Mate Ma'a Tonga merch. They're independent supporter designs.
  The Player Tee's 00 number is generic (no real player names).
- Team names: "Toa Samoa", "Mate Ma'a Tonga" (with the apostrophe). 685 = Samoa's calling code, 676 = Tonga's.
- Colours: Samoa = royal blue world, Tonga = red world, PMN+ = black/neutral.
- Voice: proud, warm, short; talks to fans as family. No fake urgency or invented stock counts.
- Headings Bebas Neue, body Instrument Sans.
- Footer pill "Powered by ICM Creative" (icmcreative.com) on every page.
