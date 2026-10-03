"""PMN+ store SEO content. One table; names swap here when the lookbook names arrive.
Shipping, returns and care are typical print-to-order defaults, marked TO CONFIRM with JQF."""
import json

DOMAIN = "https://www.polynesianmusicnetwork.com"

# --- policy defaults (TO CONFIRM with JQF) ---
POLICY = {
    "production": "2–4 business days",
    "shipping": "3–7 business days",
    "total": "about 5–11 business days",
    "returnDays": 30,
    "returns": ("Wrong size? Exchange unworn, unwashed items within 30 days of delivery. "
                "Misprinted, damaged or wrong items are replaced free: email a photo within 30 days. "
                "Every piece is printed to order, so returns for change of mind are store credit, and the customer pays return postage."),
    "care": "Machine wash cold, inside out, with similar colours. Tumble dry low or hang dry. Do not iron directly on the print. Do not dry clean.",
}

# name, colour, keywords focus, description paragraphs, product-specific FAQ
P = {
 "mmt-oversized": dict(
   m="Heavyweight oversized Mate Ma'a Tonga tee with the Est. 1986 crest print and a PMN+ tapa band.",
   kw="Mate Ma'a Tonga oversized tee",
   d=["A heavyweight oversized tee for Mate Ma'a Tonga fans. The front carries the Mate Ma'a Tonga Est. 1986 crest print in red and white; a PMN+ tapa band runs across the upper back.",
      "Cut from 7.5 oz 100% USA cotton with a relaxed body and dropped shoulder, it holds its shape wash after wash. Made for Rugby League World Cup 2026 and every Tonga game after it."],
   faq=[("How does the oversized fit run?","It's cut roomy with a dropped shoulder. Take your normal size for the relaxed oversized look, or one size down for a closer fit. Compare with the size guide: chest is measured armpit to armpit.")]),
 "toa-oversized": dict(
   m="Heavyweight oversized Toa Samoa tee with the Est. 1986 crest print and a PMN+ tapa band.",
   kw="Toa Samoa oversized tee",
   d=["A heavyweight oversized tee for Toa Samoa fans. The front carries the Toa Samoa Est. 1986 crest print; a PMN+ tapa band runs across the upper back.",
      "Cut from 7.5 oz 100% USA cotton with a relaxed body and dropped shoulder. Built for Rugby League World Cup 2026 and every Samoa game after it."],
   faq=[("How does the oversized fit run?","It's cut roomy with a dropped shoulder. Take your normal size for the relaxed oversized look, or one size down for a closer fit.")]),
 "mmt-676-black": dict(
   m="Black Tonga 676 shirt with a large MATE MA'A TONGA 676 back print. S–5XL, 100% cotton.",
   kw="Tonga 676 shirt",
   d=["The 676 tee in black. A large MATE MA'A TONGA 676 print fills the back in red and white, with a Six·Seven·Six badge on the chest and a PMN+ badge on the sleeve.",
      "676 is Tonga's international calling code, worn here as a mark of home. Printed on a 5.3 oz 100% cotton midweight tee with a regular fit, from S to 5XL at one price."],
   faq=[("What does 676 mean?","676 is Tonga's international dialling code. Tongans around the world use it as shorthand for home and for representing Tonga.")]),
 "mmt-676-tee": dict(
   m="Red Tonga 676 shirt with a large MATE MA'A TONGA 676 back print. 100% cotton tee.",
   kw="Tonga 676 shirt red",
   d=["The 676 tee in Tonga red. A large MATE MA'A TONGA 676 print fills the back, with a Six·Seven·Six badge on the chest and a PMN+ badge on the sleeve.",
      "676 is Tonga's international calling code, worn as a mark of home. Printed on a 5.3 oz 100% cotton midweight tee with a regular fit, S to 5XL."],
   faq=[("What does 676 mean?","676 is Tonga's international dialling code. Tongans around the world use it as shorthand for home and for representing Tonga.")]),
 "toa-685-black": dict(
   m="Black Samoa 685 shirt with a large TOA SAMOA 685 back print. S–5XL, 100% cotton.",
   kw="Samoa 685 shirt",
   d=["The 685 tee in black. A large TOA SAMOA 685 print fills the back, with a Six·Eight·Five badge on the chest and a PMN+ badge on the sleeve.",
      "685 is Samoa's international calling code, worn as a mark of home. Printed on a 5.3 oz 100% cotton midweight tee with a regular fit, from S to 5XL at one price."],
   faq=[("What does 685 mean?","685 is Samoa's international dialling code. Samoans around the world use it as shorthand for home and for representing Samoa.")]),
 "toa-685-tee": dict(
   m="Royal blue Samoa 685 shirt with a large TOA SAMOA 685 back print. 100% cotton tee.",
   kw="Samoa 685 shirt blue",
   d=["The 685 tee in royal blue. A large TOA SAMOA 685 print in white fills the back, with a Six·Eight·Five badge on the chest and a PMN+ badge on the sleeve.",
      "685 is Samoa's international calling code, worn as a mark of home. Printed on a 5.3 oz 100% cotton midweight tee with a regular fit, S to 5XL."],
   faq=[("What does 685 mean?","685 is Samoa's international dialling code. Samoans around the world use it as shorthand for home and for representing Samoa.")]),
 "mmt-snapback": dict(
   m="Red Mate Ma'a Tonga curved-bill snapback with script and crest, Mafana! patch and Tonga flag.",
   kw="Mate Ma'a Tonga snapback",
   d=["A red curved-bill snapback with Mate Ma'a Tonga script and crest across the front, a Mafana! patch on the left side, PMN+ and the Tonga flag on the right, and Tonga script on the back.",
      "Embroidered on all four sides, with a structured crown, curved bill and an adjustable snap closure that fits most heads."],
   faq=[("Will it fit me?","It's one size with an adjustable snap strap, which fits most adult heads, roughly 21.5 to 24 inches around.")]),
 "toa-snapback": dict(
   m="Royal blue Toa Samoa curved-bill snapback with script and crest, O ai le toa patch and Samoa flag.",
   kw="Toa Samoa snapback",
   d=["A royal blue curved-bill snapback with Toa Samoa script and crest across the front, an O ai le toa patch on the left side, PMN+ and the Samoa flag on the right, and Samoa script on the back.",
      "Embroidered on all four sides, with a structured crown, curved bill and an adjustable snap closure that fits most heads."],
   faq=[("Will it fit me?","It's one size with an adjustable snap strap, which fits most adult heads, roughly 21.5 to 24 inches around.")]),
 "mmt-hp-snapback": dict(
   m="White and crimson high-profile Tonga snapback: Est. 1986 Mate Ma'a Tonga front, Pasifika patch.",
   kw="Tonga snapback white",
   d=["A two-tone high-profile snapback with a white crown and crimson brim. The front reads Est. 1986 Mate Ma'a Tonga with the crest; the left side carries a Pasifika Polynesian Music patch, the right side PMN+ and the Tonga flag.",
      "Embroidered on all four sides, with a high-profile structured crown, flat brim and an adjustable snap closure."],
   faq=[("How do I keep the white crown clean?","Spot clean with cold water, mild soap and a soft brush, then air dry. Don't machine wash or tumble dry a structured cap.")]),
 "toa-hp-snapback": dict(
   m="White and navy high-profile Samoa snapback: Est. 1986 Toa Samoa front, Pasifika patch.",
   kw="Samoa snapback white",
   d=["A two-tone high-profile snapback with a white crown and navy brim. The front reads Est. 1986 Toa Samoa with the crest; the left side carries a Pasifika Polynesian Music patch, the right side PMN+ and the Samoa flag.",
      "Embroidered on all four sides, with a high-profile structured crown, flat brim and an adjustable snap closure."],
   faq=[("How do I keep the white crown clean?","Spot clean with cold water, mild soap and a soft brush, then air dry. Don't machine wash or tumble dry a structured cap.")]),
 "mmt-silver-blackout": dict(
   m="Tonal grey-on-black Mate Ma'a Tonga tee with a vertical 676 back print. S–5XL.",
   kw="Mate Ma'a Tonga black shirt",
   d=["A tonal blackout tee for Mate Ma'a Tonga: grey prints on black for a quieter way to rep Tonga. A vertical 676 runs down the back with the PMN+ mark.",
      "Printed on a 5.3 oz 100% cotton midweight tee with a regular fit, S to 5XL."],
   faq=[("Is the print reflective?","No. The silver tone is a flat grey ink, so it stays subtle in daylight and photos.")]),
 "toa-silver-blackout": dict(
   m="Tonal grey-on-black Toa Samoa tee with a vertical 685 back print. S–5XL.",
   kw="Toa Samoa black shirt",
   d=["A tonal blackout tee for Toa Samoa: O Ai Le Toa Samoa across the chest in grey with the flag and crest, and a vertical 685 down the back with the PMN+ mark.",
      "Printed on a 5.3 oz 100% cotton midweight tee with a regular fit, S to 5XL."],
   faq=[("Is the print reflective?","No. The silver tone is a flat grey ink, so it stays subtle in daylight and photos.")]),
 "pmn-tee": dict(
   m="Black PMN+ logo tee with the circle logo on the left chest. Midweight 100% cotton, S–5XL.",
   kw="PMN+ t-shirt",
   d=["The PMN+ core tee in black, with the PMN+ circle logo on the left chest and a clean back. An everyday tee from the Pasifika media platform.",
      "Printed on a 5.3 oz 100% cotton midweight tee with a regular fit, from S to 5XL at one price."],
   faq=[("Is this part of the RLWC drop?","No. It's a PMN+ core piece, available all year.")]),
 "toa-cream-tee": dict(
   m="Cream Toa Samoa tee with an arched O Ai Le Toa Samoa print in black. Regular fit, S–5XL.",
   kw="Toa Samoa cream t-shirt",
   d=["A cream (ecru) tee for Toa Samoa fans, with O Ai Le Toa Samoa arched across the chest in black.",
      "Regular fit, from S to 5XL at one price."],
   faq=[("Is this part of the RLWC drop?","It's a PMN+ Apparel piece you can wear to every Samoa game.")]),
 "pmn-dad-hat": dict(
   m="Khaki PMN+ Classic Dad Hat with the embroidered Community · Culture · Connection seal. Exclusive, while stocks last.",
   kw="PMN+ dad hat",
   d=["The PMN+ Classic Dad Hat in khaki, with the PMN+ Community · Culture · Connection seal embroidered in white on the front. An exclusive run, available only while stocks last.",
      "100% cotton, unstructured low-profile crown, curved bill and an adjustable strap with a metal buckle. One size fits most."],
   faq=[("Will it fit me?","It's one size with an adjustable strap and metal buckle, which fits most adult heads."),("Will it be restocked?","It's an exclusive run, so once it sells out it may not come back.")]),
 "pmn-trucker": dict(
   m="Black mesh-back PMN+ trucker hat with the circle logo on the front panel. One size, snap closure.",
   kw="PMN+ trucker hat",
   d=["The PMN+ core trucker in black, with the PMN+ circle logo on the front panel.",
      "Curved bill, breathable mesh side and back panels and an adjustable snap closure. One size fits most."],
   faq=[("Will it fit me?","It's one size with an adjustable snap strap, which fits most adult heads.")]),
 "mmt-trucker": dict(
   m="Black mesh-back Tonga trucker hat with an arched Mate Ma'a Tonga 2026 print and crest.",
   kw="Tonga trucker hat",
   d=["A black mesh-back trucker with an arched Mate Ma'a Tonga 2026 print and the crest on the front panel.",
      "Curved bill, breathable mesh side and back panels and an adjustable snap closure. One size fits most."],
   faq=[("Will it fit me?","It's one size with an adjustable snap strap, which fits most adult heads.")]),
 "toa-trucker": dict(
   m="Black mesh-back Samoa trucker hat with an arched Toa Samoa 2026 print and crest.",
   kw="Samoa trucker hat",
   d=["A black mesh-back trucker with an arched Toa Samoa 2026 print and the crest on the front panel.",
      "Curved bill, breathable mesh side and back panels and an adjustable snap closure. One size fits most."],
   faq=[("Will it fit me?","It's one size with an adjustable snap strap, which fits most adult heads.")]),
}

SHARED_FAQ = [
 ("When will my order arrive?", f"Each piece is printed to order. Printing takes {POLICY['production']}, then shipping takes {POLICY['shipping']} within the USA, so {POLICY['total']} in total. You'll get a tracking link by email when it ships."),
 ("Do you ship outside the USA?", "Not yet. We ship to all 50 US states, including Hawaii and Alaska. We're working on New Zealand and Australia."),
 ("What payment methods do you take?", "Visa, Mastercard, Amex, Apple Pay, Google Pay and Shop Pay at secure checkout."),
 ("What's your return and exchange policy?", POLICY["returns"]),
 ("How do I wash it?", POLICY["care"]),
]

COLLECTIONS = {
 "mate-maa-tonga": dict(name="Mate Ma'a Tonga", title="Mate Ma'a Tonga Merch: 676 Tees, Snapbacks & Hats | PMN+",
   meta="Shop Mate Ma'a Tonga merch for Rugby League World Cup 2026: 676 tees, oversized crest tees, snapbacks and trucker hats. Ships across the USA.",
   intro="Rep Tongan red for Rugby League World Cup 2026. The Mate Ma'a Tonga collection brings the 676 back print, the Est. 1986 crest and Tongan patches to heavyweight tees, snapbacks and truckers, printed to order and shipped across the USA."),
 "toa-samoa": dict(name="Toa Samoa", title="Toa Samoa Merch: 685 Tees, Snapbacks & Hats | PMN+",
   meta="Shop Toa Samoa merch for Rugby League World Cup 2026: 685 tees, oversized crest tees, snapbacks and trucker hats. Ships across the USA.",
   intro="Rep Toa Samoa blue for Rugby League World Cup 2026. The Toa Samoa collection brings the 685 back print, the Est. 1986 crest and Samoan patches to heavyweight tees, snapbacks and truckers, printed to order and shipped across the USA."),
 "pmn-plus": dict(name="PMN+", title="PMN+ Apparel: Logo Tee, Trucker & Dad Hat | PMN+ Shop",
   meta="Shop PMN+ apparel from the Pasifika media platform: the PMN+ Logo Tee, Trucker Hat and Classic Dad Hat. Printed to order and shipped across the USA.",
   intro="PMN+ is a multimedia platform for the Pasifika community: music, news, sports and culture, shared worldwide. PMN+ apparel carries that same pride on everyday pieces, from the Logo Tee to the Trucker and Classic Dad Hat, printed to order and shipped across the USA."),
}

if __name__ == "__main__":
    json.dump(dict(domain=DOMAIN, policy=POLICY, products=P, sharedFaq=SHARED_FAQ, collections=COLLECTIONS),
              open("seo_content.json", "w"), ensure_ascii=False, indent=1)
    print(len(P), "products")
