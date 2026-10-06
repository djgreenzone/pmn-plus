# Access, services and environment variables

**No secret values in this repo or this file.** Names and locations only. Ask DJ for access.

## Services
| Service | What it does | Account / id | Who has access |
|---|---|---|---|
| GitHub `djgreenzone/pmn-plus` | Source + generated site | — | DJ (owner), lead developer |
| Vercel | Hosting, serverless `/api`, previews per branch | Project linked to the repo | DJ, lead developer |
| Shopify | Products, prices, checkout, discounts, payouts | `polynesianmusicnetwork.myshopify.com` | DJ (owner), lead developer (staff, full) |
| Fulfill Engine | Creates Shopify products/variants, routes orders to JQF | — | DJ (admin), JQF |
| Supabase | Auth, profiles, saved items, events | project `pmn-plus` `zacfssfjlmixnqhjuoed` (Infortum org) | DJ, lead developer |
| Klaviyo | Email/SMS flows, sign-up lists, reviews | ICM account, company `T9JJzp` | DJ, lead developer |
| Resend | SMTP for Supabase sign-in emails | domain polynesianmusicnetwork.com | DJ |
| Google Cloud "PMN Plus" | Google sign-in OAuth client "PMN+ website" | ICMG org | DJ |
| Google Search Console | `sc-domain:polynesianmusicnetwork.com` | ammon@islandcitymediagroup.com | DJ |
| Google Merchant Center | Shopping listings from the feed | `5866912143` | DJ |
| GA4 / Meta / Clarity | Analytics | `G-KEQ8HPTH9W` / `1983591485663494` / `ys5h8s9j8m` | DJ |
| Instagram Graph API | Homepage reels | token in `IG_ACCESS_TOKEN` | DJ |

## Vercel environment variables (Production and Preview)
| Name | Used by |
|---|---|
| `SUPABASE_URL` | `/api/account/*` |
| `SUPABASE_SERVICE_ROLE_KEY` | `/api/account/*` (server only, never in the browser) |
| `SHOPIFY_CLIENT_ID`, `SHOPIFY_CLIENT_SECRET` | `/api/account/*` via the Shopify app "PMN+ Accounts" (read/write customers, read orders) |
| `SHOPIFY_ADMIN_TOKEN` | optional alternative to client credentials in `_account.js` |
| `SHOPIFY_STORE` | optional, defaults to `polynesianmusicnetwork.myshopify.com` |
| `KLAVIYO_PRIVATE_KEY` | `/api/account/reviews` |
| `IG_ACCESS_TOKEN` | `/api/reels` |

## Public keys (safe in the browser, live in the repo)
- `assets/pmn-config.js`: Supabase URL + **publishable** key, analytics IDs, feature flags.
- `_source/shopify_layer.js`: Shopify **Storefront** access token (read products + create carts only).
- Klaviyo company id `T9JJzp` (client API).

## Working with Claude
- Claude Code reads `CLAUDE.md` at the repo root automatically. Keep it short and current; put detail in `docs/`.
- When you fix something new, add it to the top of `docs/TROUBLESHOOTING.md` in the same PR.
- Claude can change Shopify through the Shopify connector (discounts, publishing, products). It should say what it is
  about to change, and confirm the result by reading it back afterwards.
- DJ's Claude sessions can't push to GitHub; they send `git format-patch` files that DJ applies with `git am`.
  If you're both working, **pull before you start** and keep PRs small to avoid conflicts.
