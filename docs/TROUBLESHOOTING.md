# Troubleshooting

Problems we've actually hit, newest first. Format: **symptom → cause → fix**. Add new ones at the top.

## Checkout

**"<Product> (size) isn't available to order yet. Remove it to check out."**
- Cause A: the product isn't published to the **Polynesian Music Network Headless** channel. The Storefront API doesn't
  return it, so the site has no variant ids. (Oct 5: all 5 new RLWC26/Player products.)
  Fix: Shopify → product → Publishing → add the Headless channel. No deploy needed; hard-refresh the site.
- Cause B: the `SHOPIFY_MAP` entry has the wrong handle or Color value (e.g. "Royal Blue" vs Shopify's "Bright Royal").
  Fix: correct `_source/shopify_layer.js`, rebuild.
- Cause C: a stale bag line with a size that colour isn't sold in (e.g. red 676 in 5XL saved before sizes changed).
  The site now clears such sizes on load and asks for a size (Oct 5 fix). If it reappears, check `BLANK` sizes vs Shopify variants.
- Cause D: the variant is out of stock or the product is draft/archived in Shopify.

**Checkout button does nothing / "opens very soon" message**
Storefront API unreachable or token wrong (`SHOPIFY.token` in `shopify_layer.js`), so `shopifyOK` is false. Check the
browser console for `Shopify` warnings. The token is a public Storefront token from the Headless channel.

**Buy 3 tees, get 1 free not applying at Shopify checkout**
- The tee isn't in the discount (Discounts → Buy 3 tees, get 1 free). Every new tee product must be added to *Customer
  buys*, and its black/red/royal **L–2XL** variants to *Customer gets*. (Oct 5: the 5 new products were missing.)
- The cart has 4+ tees but none is an eligible free size/colour (e.g. all oversized or all 3XL+): working as designed;
  the bag says "Almost there…".
- A discount code is applied: codes don't combine with Buy 3 get 1; Shopify keeps the better one.
- The bag predicts a saving but checkout doesn't: the site rule (`bx()` / `FREE_SZ`) and the Shopify discount disagree. Align them.

## Product pages / shop

**New product shows on the site but not at checkout** → see "isn't available to order yet" above (Headless channel).

**Build fails with `AssertionError` in `make_shop.py`**
A `rep(old,new)` didn't find its exact text in `site2/index.html` (someone changed that text). Update the `old`
string in `make_shop.py` to the new text; keep the assert.

**Hero/product image shows the front when you expected the back**
The product page opens on `REST[id]` (e.g. 180 = back). The **hero carousel always shows the front** for tees, by design.

**Spin looks jerky or starts on the wrong side**
Wrong loop length passed to `tools/add_spin.py`. Find the frame that repeats `f001` and use that frame number minus 1.

**Wrong price showing**
Shopify price wins at runtime; if Shopify didn't load (blocked network) the `PRODUCTS[].price` fallback shows. Keep both in sync.

**Sizes wrong on a product page**
`blankFor()` picks the size list from `colourName`: anything containing "Black" gets S–5XL. Check the product's
`colourName` and the `BLANK` lists.

## Payments / Shopify admin

**Plaid "No compatible accounts" when linking a Chase business account**
New business accounts often aren't shareable through Plaid yet. Use **Enter account details manually** (routing +
account number from Chase → Account details), then confirm the micro-deposits. (Oct 6.)

**Payouts going to Shopify Balance instead of the bank**
Settings → Payments → Shopify Payments → payout account → Switch to a different account. The first payout after a switch is delayed ~4 days.

**Afterpay: which provider?**
Use **Afterpay US (New)** (green $ logo). Ignore the cross-border aggregators (Asiabill, LianLian, Airwallex, UseePay).

## SEO / Google

**Search Console "Couldn't fetch" on the sitemap**
Usually just pending first read. Test `https://www.polynesianmusicnetwork.com/sitemap.xml` (it renders styled in a
browser via `sitemap.xsl`; crawlers get plain XML). Resubmit after big changes.

**Duplicate products in Merchant Center**
Don't connect Shopify's Google & YouTube channel; the feed is `/merchant-center-feed.txt`.

**Old WordPress URLs 404**
Add a 301 in `vercel.json`.

## Accounts

**Sign-in code email not arriving**
Supabase Auth → SMTP (Resend) settings and the Resend domain status. Template: `_source/account/email-signin.html`.

**Orders not showing in Account**
`/api/account/link` must have run (it tags the Shopify customer `pmn-member`). Check Vercel function logs and the env
vars `SHOPIFY_CLIENT_ID` / `SHOPIFY_CLIENT_SECRET` / `SUPABASE_SERVICE_ROLE_KEY`.

**Reviews not posting**
`KLAVIYO_PRIVATE_KEY` missing in Vercel, or the product's Shopify id is missing from `KL_PID` in `account/template.html`.

## Local dev

**Local server dies / port busy** → `lsof -i :8765` then kill that PID. Don't `pkill -f http.server` from a shell whose
own command line contains that text.

**External calls fail locally** (fonts, Shopify, Supabase, analytics): fine for layout checks; test checkout on the
Vercel preview URL instead.
