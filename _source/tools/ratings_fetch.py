#!/usr/bin/env python3
"""Pull published review aggregates from Klaviyo and write seo/reviews-summary.json.

Feeds aggregateRating JSON-LD in seo_build.py. Safe to run anytime:
- No reviews yet  -> writes an empty map, so no ratings are emitted (correct).
- Reviews exist   -> writes {shopify_product_id: {count, average}} and schema lights up.

Needs a Klaviyo private key (read-only is fine):
    KLAVIYO_PRIVATE_KEY=pk_xxx python3 tools/ratings_fetch.py
Run it before seo_build.py in the build chain (make_shop.py calls it; it no-ops
without a key so local builds never break).
"""
import json, os, sys, urllib.request, urllib.error

KEY = os.environ.get("KLAVIYO_PRIVATE_KEY", "").strip()
REV = "2026-07-15"  # Klaviyo API revision used elsewhere in this project
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site2", "seo", "reviews-summary.json")
OUT = os.path.normpath(OUT)


def get(url):
    req = urllib.request.Request(url, headers={
        "Authorization": "Klaviyo-API-Key " + KEY,
        "revision": REV,
        "accept": "application/vnd.api+json",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main():
    if not KEY:
        # No key in this shell: don't clobber an existing summary, don't fail the build.
        if not os.path.exists(OUT):
            os.makedirs(os.path.dirname(OUT), exist_ok=True)
            json.dump({}, open(OUT, "w"))
            print("ratings: no KLAVIYO_PRIVATE_KEY; wrote empty summary")
        else:
            print("ratings: no KLAVIYO_PRIVATE_KEY; kept existing summary")
        return

    # Aggregate published reviews per Klaviyo item (item id maps to the Shopify
    # product id via $shopify:::$default:::<id>). We only count public, published,
    # non-rejected reviews with a rating.
    agg = {}  # shopify_pid -> [sum_rating, count]
    url = ("https://a.klaviyo.com/api/reviews/"
           "?fields[review]=rating,status,public,product"
           "&filter=equals(status,\"published\"),equals(public,true)"
           "&page[size]=100")
    pages = 0
    while url and pages < 100:
        try:
            data = get(url)
        except urllib.error.HTTPError as e:
            print("ratings: Klaviyo error %s %s" % (e.code, e.read()[:200]), file=sys.stderr)
            break
        for row in data.get("data", []):
            at = row.get("attributes", {})
            rating = at.get("rating")
            if rating is None:
                continue
            # product reference: try relationship, then attribute
            pid = None
            rel = (row.get("relationships", {}).get("item") or {}).get("data") or {}
            raw = rel.get("id") or at.get("product", {}).get("external_id") or ""
            # external id form: $shopify:::$default:::15382958342343
            if ":::" in str(raw):
                pid = str(raw).split(":::")[-1]
            elif str(raw).isdigit():
                pid = str(raw)
            if not pid:
                continue
            s = agg.setdefault(pid, [0.0, 0])
            s[0] += float(rating)
            s[1] += 1
        url = (data.get("links") or {}).get("next")
        pages += 1

    summary = {pid: {"count": c, "average": round(tot / c, 2)}
               for pid, (tot, c) in agg.items() if c > 0}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(summary, open(OUT, "w"), indent=0)
    print("ratings: wrote %d products with reviews" % len(summary))


if __name__ == "__main__":
    main()
