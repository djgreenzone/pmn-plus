"""PMN+ store SEO content. One table; names swap here when the lookbook names arrive.
Shipping, returns and care copy for the PMN+ Shop."""
import json

DOMAIN = "https://www.polynesianmusicnetwork.com"

# --- policy defaults (TO CONFIRM with JQF) ---
POLICY = {
    "production": "2–4 business days",
    "shipping": "1–5 business days",
    "total": "about 3–9 business days",
    "returnDays": 0,
    "returns": ("Every PMN+ piece is made to order, just for you, so all sales are final: no returns or exchanges for size, colour or change of mind. "
                "If your item arrives damaged, misprinted or incorrect, email photos within 7 days of delivery and we'll review it and make it right."),
    "care": "Machine wash cold, inside out, with similar colours. Tumble dry low or hang dry. Do not iron directly on the print. Do not dry clean.",
}

# name, colour, keywords focus, description paragraphs, product-specific FAQ
P = {
 "mmt-oversized": dict(
   m="Heavyweight oversized Mate Ma'a Tonga tee with the Est. 1986 crest print and a PMN+ tapa band. S–6XL.",
   kw="Mate Ma'a Tonga oversized tee",
   d=["A heavyweight oversized tee for Mate Ma'a Tonga fans. The front carries the Mate Ma'a Tonga Est. 1986 crest print in red and white; a PMN+ tapa band runs across the upper back.",
      "Cut from 8.2 oz 100% ring-spun cotton with a boxy body and dropped shoulders, it holds its shape wash after wash. Sizes S to 6XL at one price. Made for Rugby League World Cup 2026 and every Tonga game after it."],
   faq=[("How does the oversized fit run?","It's cut roomy with a dropped shoulder. Take your normal size for the relaxed oversized look, or one size down for a closer fit. Compare with the size guide: chest is measured armpit to armpit.")]),
 "toa-oversized": dict(
   m="Heavyweight oversized Toa Samoa tee with the Est. 1986 crest print and a PMN+ tapa band. S–6XL.",
   kw="Toa Samoa oversized tee",
   d=["A heavyweight oversized tee for Toa Samoa fans. The front carries the Toa Samoa Est. 1986 crest print; a PMN+ tapa band runs across the upper back.",
      "Cut from 8.2 oz 100% ring-spun cotton with a boxy body and dropped shoulders, in sizes S to 6XL at one price. Built for Rugby League World Cup 2026 and every Samoa game after it."],
   faq=[("How does the oversized fit run?","It's cut roomy with a dropped shoulder. Take your normal size for the relaxed oversized look, or one size down for a closer fit.")]),
 "mmt-676-black": dict(
   m="Black Tonga 676 shirt with a large MATE MA'A TONGA 676 back print. S–6XL, 100% cotton.",
   kw="Tonga 676 shirt",
   d=["The 676 tee in black. A large MATE MA'A TONGA 676 print fills the back in red and white, with a Six·Seven·Six badge on the chest and a PMN+ badge on the sleeve.",
      "676 is Tonga's international calling code, worn here as a mark of home. Printed on a 5.3 oz 100% cotton midweight tee with a regular fit, from S to 6XL at one price."],
   faq=[("What does 676 mean?","676 is Tonga's international dialling code. Tongans around the world use it as shorthand for home and for representing Tonga.")]),
 "mmt-676-tee": dict(
   m="Red Tonga 676 shirt with a large MATE MA'A TONGA 676 back print. S–6XL, 100% cotton.",
   kw="Tonga 676 shirt red",
   d=["The 676 tee in Tonga red. A large MATE MA'A TONGA 676 print fills the back, with a Six·Seven·Six badge on the chest and a PMN+ badge on the sleeve.",
      "676 is Tonga's international calling code, worn as a mark of home. Printed on a 5.3 oz 100% cotton midweight tee with a regular fit, from S to 6XL at one price."],
   faq=[("What does 676 mean?","676 is Tonga's international dialling code. Tongans around the world use it as shorthand for home and for representing Tonga.")]),
 "toa-685-black": dict(
   m="Black Samoa 685 shirt with a large TOA SAMOA 685 back print. S–6XL, 100% cotton.",
   kw="Samoa 685 shirt",
   d=["The 685 tee in black. A large TOA SAMOA 685 print fills the back, with a Six·Eight·Five badge on the chest and a PMN+ badge on the sleeve.",
      "685 is Samoa's international calling code, worn as a mark of home. Printed on a 5.3 oz 100% cotton midweight tee with a regular fit, from S to 6XL at one price."],
   faq=[("What does 685 mean?","685 is Samoa's international dialling code. Samoans around the world use it as shorthand for home and for representing Samoa.")]),
 "toa-685-tee": dict(
   m="Royal blue Samoa 685 shirt with a large TOA SAMOA 685 back print. S–6XL, 100% cotton.",
   kw="Samoa 685 shirt blue",
   d=["The 685 tee in royal blue. A large TOA SAMOA 685 print in white fills the back, with a Six·Eight·Five badge on the chest and a PMN+ badge on the sleeve.",
      "685 is Samoa's international calling code, worn as a mark of home. Printed on a 5.3 oz 100% cotton midweight tee with a regular fit, from S to 6XL at one price."],
   faq=[("What does 685 mean?","685 is Samoa's international dialling code. Samoans around the world use it as shorthand for home and for representing Samoa.")]),
 "mmt-rlwc26-black": dict(
   m="Black Mate Ma'a Tonga RLWC 2026 shirt with an arched 1986 crest back print and Tonga script chest logo. S–6XL, 100% cotton.",
   kw="Mate Ma'a Tonga World Cup 2026 shirt",
   d=["The RLWC26 tee in black. The back carries an arched MATE MA'A over the Tonga crest, 19 and 86 either side, Tonga in script and a Rugby League World Cup 2026 line. A small crest and Mate Ma'a Tonga script sit on the left chest, with a PMN+ badge on the sleeve.",
      "A supporter tee for Rugby League World Cup 2026. Printed on a 5.3 oz 100% cotton midweight tee with a regular fit, from S to 6XL at one price."],
   faq=[("Is this an official team shirt?","No. It's an independent PMN+ supporter tee, made to rep Mate Ma'a Tonga through the Rugby League World Cup 2026.")]),
 "mmt-rlwc26-red": dict(
   m="Red Mate Ma'a Tonga RLWC 2026 shirt with an arched 1986 crest back print and Tonga script chest logo. S–6XL, 100% cotton.",
   kw="Mate Ma'a Tonga World Cup 2026 shirt red",
   d=["The RLWC26 tee in Tonga red. The back carries an arched MATE MA'A over the Tonga crest, 19 and 86 either side, Tonga in script and a Rugby League World Cup 2026 line, all in white. A small crest and Mate Ma'a Tonga script sit on the left chest, with a PMN+ badge on the sleeve.",
      "A supporter tee for Rugby League World Cup 2026. Printed on a 5.3 oz 100% cotton midweight tee with a regular fit, from S to 6XL at one price."],
   faq=[("Is this an official team shirt?","No. It's an independent PMN+ supporter tee, made to rep Mate Ma'a Tonga through the Rugby League World Cup 2026.")]),
 "toa-rlwc26-black": dict(
   m="Black Toa Samoa RLWC 2026 shirt with an arched TOA 1986 crest back print and Samoa script chest logo. S–6XL, 100% cotton.",
   kw="Toa Samoa World Cup 2026 shirt",
   d=["The RLWC26 tee in black. The back carries an arched TOA over the Samoa crest, 19 and 86 either side, Samoa in script and a Rugby League World Cup 2026 line. A small crest and Toa Samoa script sit on the left chest, with a PMN+ badge on the sleeve.",
      "A supporter tee for Rugby League World Cup 2026. Printed on a 5.3 oz 100% cotton midweight tee with a regular fit, from S to 6XL at one price."],
   faq=[("Is this an official team shirt?","No. It's an independent PMN+ supporter tee, made to rep Toa Samoa through the Rugby League World Cup 2026.")]),
 "toa-rlwc26-royal": dict(
   m="Royal blue Toa Samoa RLWC 2026 shirt with an arched TOA 1986 crest back print and Samoa script chest logo. S–6XL, 100% cotton.",
   kw="Toa Samoa World Cup 2026 shirt blue",
   d=["The RLWC26 tee in royal blue. The back carries an arched TOA over the Samoa crest, 19 and 86 either side, Samoa in script and a Rugby League World Cup 2026 line, in white. A small crest and Toa Samoa script sit on the left chest, with a PMN+ badge on the sleeve.",
      "A supporter tee for Rugby League World Cup 2026. Printed on a 5.3 oz 100% cotton midweight tee with a regular fit, from S to 6XL at one price."],
   faq=[("Is this an official team shirt?","No. It's an independent PMN+ supporter tee, made to rep Toa Samoa through the Rugby League World Cup 2026.")]),
 "mmt-player-black": dict(
   m="Black Mate Ma'a Tonga player tee: MATE MA'A TONGA 676 crest front in red, jersey-style TONGA 00 back. S–6XL, 100% cotton.",
   kw="Tonga rugby league jersey tee",
   d=["A jersey-style supporter tee in black with red prints. The front reads Six·Seven·Six over MATE MA'A TONGA and Rugby League, with the Tonga crest and 676 below. The back carries TONGA with the crest in the O and big 00 numbers, plus a PMN+ badge on the sleeve.",
      "Printed on a 5.3 oz 100% cotton midweight tee with a regular fit, from S to 6XL at one price."],
   faq=[("Can I get my own name or number?","Not yet. Every Player Tee carries the 00 number shown. Join the PMN+ list to hear first if custom names and numbers launch.")]),
 "mmt-player-red": dict(
   m="Red Mate Ma'a Tonga player tee: MATE MA'A TONGA 676 crest front, jersey-style TONGA 00 back. S–6XL, 100% cotton.",
   kw="Tonga rugby league jersey tee red",
   d=["A jersey-style supporter tee in Tonga red with white prints. The front reads Six·Seven·Six over MATE MA'A TONGA and Rugby League, with the Tonga crest and 676 below. The back carries TONGA with the crest in the O and big 00 numbers, plus a PMN+ badge on the sleeve.",
      "Printed on a 5.3 oz 100% cotton midweight tee with a regular fit, from S to 6XL at one price."],
   faq=[("Can I get my own name or number?","Not yet. Every Player Tee carries the 00 number shown. Join the PMN+ list to hear first if custom names and numbers launch.")]),
 "toa-player-black": dict(
   m="Black Toa Samoa player tee: TOA SAMOA 685 crest front, jersey-style SAMOA 00 back. S–6XL, 100% cotton.",
   kw="Samoa rugby league jersey tee",
   d=["A jersey-style supporter tee in black. The front reads Six·Eight·Five over TOA SAMOA and Rugby League, with the Samoa crest and 685 below. The back carries SAMOA with the crest in the O and big white 00 numbers outlined in red, plus a PMN+ badge on the sleeve.",
      "Printed on a 5.3 oz 100% cotton midweight tee with a regular fit, from S to 6XL at one price."],
   faq=[("Can I get my own name or number?","Not yet. Every Player Tee carries the 00 number shown. Join the PMN+ list to hear first if custom names and numbers launch.")]),
 "toa-player-royal": dict(
   m="Royal blue Toa Samoa player tee: TOA SAMOA 685 crest front, jersey-style SAMOA 00 back. S–6XL, 100% cotton.",
   kw="Samoa rugby league jersey tee blue",
   d=["A jersey-style supporter tee in royal blue. The front reads Six·Eight·Five over TOA SAMOA and Rugby League, with the Samoa crest and 685 below. The back carries SAMOA with the crest in the O and big white 00 numbers outlined in red, plus a PMN+ badge on the sleeve.",
      "Printed on a 5.3 oz 100% cotton midweight tee with a regular fit, from S to 6XL at one price."],
   faq=[("Can I get my own name or number?","Not yet. Every Player Tee carries the 00 number shown. Join the PMN+ list to hear first if custom names and numbers launch.")]),
 "mmt-snapback": dict(
   m="Red Mate Ma'a Tonga curved-bill snapback with script and crest, Mafana! patch and Tonga flag.",
   kw="Mate Ma'a Tonga snapback",
   d=["A red curved-bill snapback with Mate Ma'a Tonga script and crest across the front, a Mafana! patch on the left side, PMN+ and the Tonga flag on the right, and Tonga script on the back.",
      "Embroidered on all four sides. 5-panel mid-profile structured cap in a 65/35 polyester-cotton twill with a seamless buckram front panel, curved bill with six rows of stitching, matching undervisor and sweatband, four sewn eyelets and an adjustable plastic snap closure. OSFA (one size fits all)."],
   faq=[("Will it fit me?","It's OSFA with an adjustable snap strap, sized for most adult heads (about 22.8 in / 58 cm around)."),("Is it structured?","Yes. The front panel is fully backed with buckram, so it holds its shape and gives the embroidery a firm, smooth base.")]),
 "toa-snapback": dict(
   m="Royal blue Toa Samoa curved-bill snapback with script and crest, O ai le toa patch and Samoa flag.",
   kw="Toa Samoa snapback",
   d=["A royal blue curved-bill snapback with Toa Samoa script and crest across the front, an O ai le toa patch on the left side, PMN+ and the Samoa flag on the right, and Samoa script on the back.",
      "Embroidered on all four sides. 5-panel mid-profile structured cap in a 65/35 polyester-cotton twill with a seamless buckram front panel, curved bill with six rows of stitching, matching undervisor and sweatband, four sewn eyelets and an adjustable plastic snap closure. OSFA (one size fits all)."],
   faq=[("Will it fit me?","It's OSFA with an adjustable snap strap, sized for most adult heads (about 22.8 in / 58 cm around)."),("Is it structured?","Yes. The front panel is fully backed with buckram, so it holds its shape and gives the embroidery a firm, smooth base.")]),
 "mmt-hp-snapback": dict(
   m="White and crimson high-profile Tonga snapback: Est. 1986 Mate Ma'a Tonga front, Pasifika patch.",
   kw="Tonga snapback white",
   d=["A two-tone high-profile snapback with a white crown and crimson brim. The front reads Est. 1986 Mate Ma'a Tonga with the crest; the left side carries a Pasifika Polynesian Music patch, the right side PMN+ and the Tonga flag.",
      "Four embroideries: front, back, left and right. 6-panel high-profile structured crown in a wool-look acrylic/polyester, retro flat bill and an adjustable plastic snap closure. OSFA (one size fits all)."],
   faq=[("Will it fit me?","It's OSFA with an adjustable snap strap, which fits most adult heads."),("How do I keep the white crown clean?","Spot clean with cold water, mild soap and a soft brush, then air dry. Don't machine wash or tumble dry a structured cap.")]),
 "toa-hp-snapback": dict(
   m="White and navy high-profile Samoa snapback: Est. 1986 Toa Samoa front, Pasifika patch.",
   kw="Samoa snapback white",
   d=["A two-tone high-profile snapback with a white crown and navy brim. The front reads Est. 1986 Toa Samoa with the crest; the left side carries a Pasifika Polynesian Music patch, the right side PMN+ and the Samoa flag.",
      "Four embroideries: front, back, left and right. 6-panel high-profile structured crown in a wool-look acrylic/polyester, retro flat bill and an adjustable plastic snap closure. OSFA (one size fits all)."],
   faq=[("Will it fit me?","It's OSFA with an adjustable snap strap, which fits most adult heads."),("How do I keep the white crown clean?","Spot clean with cold water, mild soap and a soft brush, then air dry. Don't machine wash or tumble dry a structured cap.")]),
 "mmt-silver-blackout": dict(
   m="Tonal grey-on-black Mate Ma'a Tonga tee with a vertical 676 back print. S–6XL.",
   kw="Mate Ma'a Tonga black shirt",
   d=["A tonal blackout tee for Mate Ma'a Tonga: grey prints on black for a quieter way to rep Tonga. A vertical 676 runs down the back with the PMN+ mark.",
      "Printed on a 5.3 oz 100% cotton midweight tee with a regular fit, from S to 6XL at one price."],
   faq=[("Is the print reflective?","No. The silver tone is a flat grey ink, so it stays subtle in daylight and photos.")]),
 "toa-silver-blackout": dict(
   m="Tonal grey-on-black Toa Samoa tee with a vertical 685 back print. S–6XL.",
   kw="Toa Samoa black shirt",
   d=["A tonal blackout tee for Toa Samoa: O Ai Le Toa Samoa across the chest in grey with the flag and crest, and a vertical 685 down the back with the PMN+ mark.",
      "Printed on a 5.3 oz 100% cotton midweight tee with a regular fit, from S to 6XL at one price."],
   faq=[("Is the print reflective?","No. The silver tone is a flat grey ink, so it stays subtle in daylight and photos.")]),
 "pmn-tee": dict(
   m="Black PMN+ logo tee with the circle logo on the left chest. Midweight 100% cotton, S–6XL.",
   kw="PMN+ t-shirt",
   d=["The PMN+ core tee in black, with the PMN+ circle logo on the left chest and a clean back. An everyday tee from the Pasifika media platform.",
      "Printed on a 5.3 oz 100% cotton midweight tee with a regular fit, from S to 6XL at one price."],
   faq=[("Is this part of the RLWC drop?","No. It's a PMN+ core piece, available all year.")]),
 "toa-cream-tee": dict(
   m="Cream Toa Samoa tee with an arched O Ai Le Toa Samoa print in black. Regular fit, S–5XL.",
   kw="Toa Samoa cream t-shirt",
   d=["A cream (ecru) tee for Toa Samoa fans, with O Ai Le Toa Samoa arched across the chest in black.",
      "Regular fit, from S to 5XL at one price."],
   faq=[("Is this part of the RLWC drop?","It's a PMN+ Apparel piece you can wear to every Samoa game.")]),
 "pmn-dad-hat": dict(
   m="Khaki PMN+ Classic Dad Hat with the PMN+ circle logo embroidered in white. Exclusive, while stocks last.",
   kw="PMN+ dad hat",
   d=["The PMN+ Classic Dad Hat in khaki, with the PMN+ circle logo embroidered in white on the front panel. An exclusive run, available only while stocks last.",
      "6-panel low-profile relaxed crown in 100% brushed cotton, with a cotton sweatband, ventilation eyelets, a pre-curved stitched bill and an adjustable strap with a brass buckle. OSFA (one size fits all)."],
   faq=[("Will it fit me?","It's OSFA with an adjustable strap and brass buckle, which fits most adult heads."),("Will it be restocked?","It's an exclusive run, so once it sells out it may not come back.")]),
 "pmn-trucker": dict(
   m="Black mesh-back PMN+ trucker hat with the circle logo embroidered on the front panel. OSFA, snap closure.",
   kw="PMN+ trucker hat",
   d=["The PMN+ core trucker in black, with the PMN+ circle logo embroidered on the front panel.",
      "5-panel mid-profile structured trucker: a 60/40 cotton-polyester front panel, breathable 100% polyester mesh side and back panels, a cotton sweatband, a pre-curved bill and an adjustable plastic snap closure. OSFA (one size fits all)."],
   faq=[("Will it fit me?","It's OSFA with an adjustable snap strap, which fits most adult heads.")]),
 "mmt-trucker": dict(
   m="Black mesh-back Tonga trucker hat with an arched Mate Ma'a Tonga 2026 DTF print and crest.",
   kw="Tonga trucker hat",
   d=["A black mesh-back trucker with an arched Mate Ma'a Tonga 2026 design and the crest on the front panel, applied as a DTF (direct-to-film) transfer for a sharp, full-colour finish.",
      "5-panel mid-profile structured trucker: a 60/40 cotton-polyester front panel, breathable 100% polyester mesh side and back panels, a cotton sweatband, a pre-curved bill and an adjustable plastic snap closure. OSFA (one size fits all)."],
   faq=[("Will it fit me?","It's OSFA with an adjustable snap strap, which fits most adult heads.")]),
 "toa-trucker": dict(
   m="Black mesh-back Samoa trucker hat with an arched Toa Samoa 2026 DTF print and crest.",
   kw="Samoa trucker hat",
   d=["A black mesh-back trucker with an arched Toa Samoa 2026 design and the crest on the front panel, applied as a DTF (direct-to-film) transfer for a sharp, full-colour finish.",
      "5-panel mid-profile structured trucker: a 60/40 cotton-polyester front panel, breathable 100% polyester mesh side and back panels, a cotton sweatband, a pre-curved bill and an adjustable plastic snap closure. OSFA (one size fits all)."],
   faq=[("Will it fit me?","It's OSFA with an adjustable snap strap, which fits most adult heads.")]),
}

# --- Extra product copy (Oct 2026 SEO pass): story, fit and pairs-with paragraphs plus product-specific FAQs.
# Appended to each product's description and FAQ above, so every product page carries 120-200 words of its own.
GAME="Add a hat and the Game Day Set takes $10 off the pair."
B3="Mix it into a Buy 3 tees, get 1 free order with any other tees in the drop."
X = {
 "mmt-oversized": (["The crest is the whole story here: Mate Ma'a Tonga, Est. 1986, in Tongan red and white, front and centre, game-day style. The tapa band across the shoulders nods to the ngatu patterns found in Tongan homes and churches.",
   "The heavyweight cotton and boxy cut give it the structure of streetwear rather than a fan-shop tee, so it works with jeans, cargos or shorts long after the final whistle. It pairs with the white and crimson Mate Ma'a Tonga High Profile Snapback. "+GAME],
   [("Is the oversized tee heavier than the other tees?","Yes. It's 8.2 oz cotton, about half as heavy again as our 5.3 oz midweight tees, so it feels thicker and hangs straighter.")]),
 "toa-oversized": (["Toa means warrior in Samoan, and the crest says it plainly: Toa Samoa, Est. 1986, front and centre. Across the upper back a PMN+ tapa band draws on siapo, the bark-cloth patterns Samoan families have handed down for generations.",
   "The heavyweight cotton and boxy, dropped-shoulder cut give it a streetwear drape that sits right over jeans, cargos or a lavalava. It pairs with the navy and white Toa Samoa High Profile Snapback or the black Toa Samoa Trucker. "+GAME],
   [("Is the oversized tee heavier than the other tees?","Yes. It's 8.2 oz cotton, about half as heavy again as our 5.3 oz midweight tees, so it feels thicker and holds a boxier shape.")]),
 "mmt-676-black": (["Ask any Tongan abroad what 676 means and you'll get a smile. It's the number that rings home, and this tee wears it big across the back so the whole stand can read it. On black, the red and white print stays bold under stadium lights and in photos.",
   "The regular fit is cut true to size; between sizes, go up for a relaxed fit. Wear it with the Mate Ma'a Tonga Trucker Snapback for a black-on-black game day look, or with the white and crimson High Profile Snapback for contrast. "+B3],
   [("Is 676 printed on the front too?","The front carries a small Six·Seven·Six badge on the chest. The large MATE MA'A TONGA 676 print is on the back.")]),
 "mmt-676-tee": (["Red is Tonga's colour, and this is the 676 tee in full Mate Ma'a Tonga red: the number that rings home printed big across the back so family can spot you from the other side of the stadium. It's the one to wear when the sea of red rises.",
   "The regular fit is cut true to size; between sizes, go up for a relaxed fit. It looks sharpest with the white and crimson Mate Ma'a Tonga High Profile Snapback. "+GAME],
   [("How close is the red to Tonga's team red?","It's a deep, true red chosen to sit alongside Tonga's jerseys and flags. Screens vary a little, so the colour can look slightly brighter or darker on your phone.")]),
 "toa-685-black": (["For Samoans living away from the islands, 685 is more than a dialling code. It's family on the other end of the line, and this tee wears it large across the back. On black, the white and red TOA SAMOA 685 print reads clean in the stands and in photos.",
   "The regular fit is cut true to size; between sizes, go up for a relaxed fit. Pair it with the black Toa Samoa Trucker Snapback for an all-black look, or the navy and white High Profile Snapback for contrast. "+B3],
   [("Is 685 printed on the front too?","The front carries a small Six·Eight·Five badge on the chest. The large TOA SAMOA 685 print is on the back.")]),
 "toa-685-tee": (["Royal blue is Toa Samoa's colour, and this is the 685 tee in it: Samoa's calling code printed big in white across the back, so the aiga can find you in a stand full of blue. It's the brightest way to say where home is.",
   "The regular fit is cut true to size; between sizes, go up for a relaxed fit. It pairs with the navy and white Toa Samoa High Profile Snapback, whose white crown echoes the white print. "+GAME],
   [("How close is the blue to Samoa's team blue?","It's a bright royal blue chosen to sit alongside Toa Samoa's jerseys and flags. Screens vary a little, so it can look slightly lighter or darker on your phone.")]),
 "mmt-rlwc26-black": (["This is the World Cup tee: built around the 2026 tournament with the arched MATE MA'A and 19 / 86 framing the crest, the way a vintage team badge is laid out. Black lets the red and white do the talking.",
   "It's made for match days but simple enough for the school run or the airport. The regular fit is cut true to size. It pairs with the Mate Ma'a Tonga Trucker Snapback, the 2026 hat from the same drop. "+B3],
   [("Will this design be around after the World Cup?","The RLWC26 tees are part of the 2026 World Cup drop. We don't promise restocks of drop designs, so if you want one, get it while it's in the shop.")]),
 "mmt-rlwc26-red": (["The World Cup tee in Tonga red, with every line printed in white: arched MATE MA'A, 19 and 86 either side of the crest, Tonga in script and Rugby League World Cup 2026 underneath. It's the matchday shirt for the red wall.",
   "The regular fit is cut true to size; between sizes, go up for a relaxed fit. Pair it with the white and crimson Mate Ma'a Tonga High Profile Snapback to carry the red and white all the way up. "+GAME],
   [("Is the red tee the same design as the black one?","Yes. The layout is identical; on the red tee every print is white, while the black tee uses red and white.")]),
 "toa-rlwc26-black": (["This is the Toa Samoa World Cup tee: an arched TOA and 19 / 86 framing the Samoa crest like a vintage team badge, with Samoa in script and the 2026 tournament line beneath. On black, the colours of the crest pop.",
   "It's made for match days but plain enough to wear every day. The regular fit is cut true to size. It pairs with the Toa Samoa Trucker Snapback, the 2026 hat from the same drop. "+B3],
   [("Will this design be around after the World Cup?","The RLWC26 tees are part of the 2026 World Cup drop. We don't promise restocks of drop designs, so grab yours while it's in the shop.")]),
 "toa-rlwc26-royal": (["The Toa Samoa World Cup tee in royal blue, with every line printed in white: arched TOA, 19 and 86 either side of the crest, Samoa in script and Rugby League World Cup 2026 underneath. Blue on blue, made for the Toa Samoa end.",
   "The regular fit is cut true to size; between sizes, go up for a relaxed fit. Pair it with the navy and white Toa Samoa High Profile Snapback. "+GAME],
   [("Is the royal blue tee the same design as the black one?","Yes. The layout is identical; on the royal blue tee every print is white.")]),
 "mmt-player-black": (["Styled like a team jersey: TONGA across the back with the crest set inside the O, and big 00 numbers underneath. The 00 is ours, not any player's, so it belongs to every fan who wears it. Red on black keeps it bold without shouting.",
   "It's a cotton tee, not a polyester jersey, so it's soft enough to wear all day. The regular fit is cut true to size. It pairs with the Mate Ma'a Tonga Trucker Snapback. "+B3],
   [("Is this a real playing jersey?","No. It's a 100% cotton supporter tee printed in a jersey style, not performance fabric, and it isn't an official team product.")]),
 "mmt-player-red": (["The jersey-style Player Tee in Tonga red with white prints: TONGA across the back with the crest inside the O and big 00 numbers, and the 676 crest stack on the front. Wear the red the way the team does.",
   "It's soft 100% cotton, not jersey polyester, so it works well beyond game day. The regular fit is cut true to size; between sizes, go up. Pair it with the white and crimson High Profile Snapback. "+GAME],
   [("Why 00?","The 00 is a generic PMN+ number, so the tee isn't tied to any one player. It belongs to every fan who wears it.")]),
 "toa-player-black": (["Styled like a team jersey: SAMOA across the back with the crest set inside the O and big white 00 numbers outlined in red. The 00 isn't any player's number, so it's yours. Black makes the white and red outline stand out.",
   "It's a cotton tee, not a polyester jersey, so it's soft enough to wear all day. The regular fit is cut true to size. Pair it with the black Toa Samoa Trucker Snapback. "+B3],
   [("Is this a real playing jersey?","No. It's a 100% cotton supporter tee printed in a jersey style, not performance fabric, and it isn't an official team product.")]),
 "toa-player-royal": (["The jersey-style Player Tee in Toa Samoa royal blue: SAMOA across the back with the crest inside the O, big white 00 numbers outlined in red, and the 685 crest stack on the front. The closest thing to the team look in a soft cotton tee.",
   "The regular fit is cut true to size; between sizes, go up. Pair it with the navy and white Toa Samoa High Profile Snapback. "+GAME],
   [("Why 00?","The 00 is a generic PMN+ number, so the tee isn't tied to any one player. It belongs to every fan who wears it.")]),
 "mmt-hp-snapback": (["A retro high-profile crown in white with a crimson flat brim, the shape of the classic team caps of the 80s and 90s. The Est. 1986 Mate Ma'a Tonga front gives it the feel of a vintage club cap, and the Pasifika patch on the side ties it to PMN+.",
   "Four embroidered sides mean it looks finished from every angle in photos. It pairs with any red or black Mate Ma'a Tonga tee; the Game Day Set takes $10 off a tee and hat bought together."],
   [("Does the brim come flat?","Yes. It's a retro flat bill. You can curve it gently by hand if you prefer.")]),
 "toa-hp-snapback": (["A retro high-profile crown in white with a navy flat brim, the shape of the classic team caps of the 80s and 90s. The Est. 1986 Toa Samoa front gives it a vintage club feel, and the Pasifika patch on the side ties it to PMN+.",
   "Four embroidered sides mean it looks finished from every angle. It pairs with the royal blue or black Toa Samoa tees; the Game Day Set takes $10 off a tee and hat bought together."],
   [("Does the brim come flat?","Yes. It's a retro flat bill. You can curve it gently by hand if you prefer.")]),
 "mmt-silver-blackout": (["Not everyone wants to wear red every day. The Silver Blackout keeps Tonga close in a quieter way: grey on black, with 676 running down the spine so it reads clearly from behind without the volume of a match shirt.",
   "It works for work, travel and nights out as well as the stands. The regular fit is cut true to size. Pair it with the black Mate Ma'a Tonga Trucker Snapback for a fully tonal look. "+B3],
   [("Will the grey print fade?","Washed inside out on cold and hung or tumbled dry low, the print holds up for a long time. Avoid ironing directly on it.")]),
 "toa-silver-blackout": (["A quieter way to rep Samoa: O Ai Le Toa Samoa across the chest in grey with the flag and crest, and 685 running down the spine. It keeps the pride without the volume of a match shirt.",
   "It works for work, travel and nights out as well as the stands. The regular fit is cut true to size. Pair it with the black Toa Samoa Trucker Snapback for a fully tonal look. "+B3],
   [("What does O Ai Le Toa mean?","It's a Samoan rallying call, often translated as 'who is the warrior?' Fans shout it to lift the team.")]),
 "mmt-trucker": (["The trucker that carries the World Cup arch: Mate Ma'a Tonga 2026 over the crest in full colour on a black front, with breathable mesh behind so it stays cool through a long day in the stands.",
   "The DTF transfer keeps the fine lines of the crest sharp. It pairs with the black Mate Ma'a Tonga RLWC26 Tee, from the same 2026 drop, or any red Tonga tee. The Game Day Set takes $10 off a tee and hat together."],
   [("Is the front print embroidered?","No. The front design is a DTF (direct-to-film) transfer, which keeps the crest's fine detail and full colour.")]),
 "toa-trucker": (["The trucker that carries the World Cup arch: Toa Samoa 2026 over the crest in full colour on a black front, with breathable mesh behind so it stays cool through a long day in the stands.",
   "The DTF transfer keeps the fine lines of the crest sharp. It pairs with the black Toa Samoa RLWC26 Tee, from the same 2026 drop, or any royal blue Samoa tee. The Game Day Set takes $10 off a tee and hat together."],
   [("Is the front print embroidered?","No. The front design is a DTF (direct-to-film) transfer, which keeps the crest's fine detail and full colour.")]),
 "pmn-tee": (["PMN+ started as a place to share Pasifika music and stories the mainstream misses. The Logo Tee is the simplest way to carry that: the circle mark on the chest, nothing on the back, nothing to date it.",
   "The regular fit is cut true to size, and every size from S to 6XL is the same price. It pairs with the PMN+ Trucker Hat or the khaki Classic Dad Hat. It also counts toward Buy 3 tees, get 1 free alongside the team tees."],
   [("Does the Logo Tee count toward Buy 3, get 1 free?","Yes. Any three tees qualify, including the Logo Tee. The free tee must be a black, red or royal blue standard tee in L, XL or 2XL.")]),
 "pmn-trucker": (["The everyday PMN+ trucker: the circle logo embroidered on a structured front, with mesh side and back panels that breathe on hot days at the field, the beach or a festival.",
   "Embroidery keeps the logo crisp wash after wash of sweat and sun. It pairs with the PMN+ Logo Tee or any team tee; the Game Day Set takes $10 off a tee and hat bought together."],
   [("Is the logo embroidered or printed?","Embroidered, so it's raised and stays crisp over time.")]),
 "pmn-dad-hat": (["A soft, unstructured classic in khaki brushed cotton with the PMN+ circle logo embroidered in white. The low crown and pre-curved bill make it the easiest hat in the shop to wear with anything.",
   "The brass buckle strap adjusts for a relaxed fit. It pairs with the PMN+ Logo Tee or a black team tee. Because it's an exclusive run, we can't promise a restock once it sells out."],
   [("Is it structured?","No. It's an unstructured low-profile dad hat, so the crown softens and shapes to you over time.")]),
}
for _k,(_d,_f) in X.items():
    P[_k]["d"]=P[_k]["d"]+_d
    P[_k]["faq"]=P[_k]["faq"]+_f

SHARED_FAQ = [
 ("What sizes do you carry?", "Every PMN+ tee comes in S to 6XL at one price, so big and tall sizes (4XL, 5XL and 6XL) cost the same as a medium. Hats are one size with an adjustable strap. Check the size guide on each tee for chest and length."),
 ("When will my order arrive?", f"Each piece is printed to order. Printing takes {POLICY['production']}, then shipping takes {POLICY['shipping']} to the contiguous US, so {POLICY['total']} in total. Hawaii, Alaska, territories and APO can take a few days longer. You'll get a tracking link by email when it ships."),
 ("Is shipping free?", "Yes. Every order ships free to the 48 contiguous US states and Washington, DC, with no minimum. Hawaii, Alaska, US territories (including Guam) and APO/FPO addresses are not included in free shipping and pay a flat $15 for standard shipping."),
 ("Do you ship outside the USA?", "Not yet. We ship within the USA only. We're working on New Zealand and Australia."),
 ("What payment methods do you take?", "Visa, Mastercard, Amex, Apple Pay, Google Pay and Shop Pay at secure checkout. You can also pay in 4 interest-free installments with Afterpay."),
 ("What's your return policy?", POLICY["returns"]),
 ("How do I wash it?", POLICY["care"]),
]

COLLECTIONS = {
 "all": dict(name="Shop all", tab="All", title="Shop All PMN+ Tees & Hats | Toa Samoa, Tonga, PMN+",
   meta="The full PMN+ catalogue in one grid: every Toa Samoa, Mate Ma'a Tonga and PMN+ tee and hat. Filter tees or hats, sort by price. S–6XL, ships across the USA.",
   intro="The full PMN+ catalogue in one grid: every Toa Samoa, Mate Ma'a Tonga and PMN+ tee and hat, with filters for tees and hats and sorting by price or best sellers.",
   aboutH="Every tee and hat, in one place",
   about=["This is the whole PMN+ shop on one page. Use the Tees and Hats filters to narrow it down, or sort by best sellers or price. Prefer to shop by team? The Toa Samoa and Mate Ma'a Tonga collections hold each team's Rugby League World Cup 2026 range, and the PMN+ collection holds our everyday core pieces.",
     "Every standard tee is 5.3 oz, 100% cotton with a regular fit, and the Crest Oversized Tees are a heavier 8.2 oz with a boxy cut. All tees run S to 6XL at one price, so 4XL, 5XL and 6XL cost the same as a medium. Hats are one size with an adjustable closure.",
     "Two offers run across the whole shop: Buy 3 tees, get 1 free (the free tee is a black, red or royal blue standard tee in L, XL or 2XL), and the Game Day Set, which takes $10 off a tee and hat bought together. Everything is printed to order and ships to the contiguous US in about 3–9 business days."]),
 "mate-maa-tonga": dict(name="Mate Ma'a Tonga", title="Mate Ma'a Tonga Shirts, Hats & Merch | RLWC 2026 | PMN+",
   meta="Mate Ma'a Tonga shirts, hats and merch for Rugby League World Cup 2026: Tonga 676 tees, RLWC26 and player tees in S–6XL, oversized crest tees and snapbacks.",
   intro="Tonga shirts, hats and merch for Rugby League World Cup 2026: the 676 tee, the RLWC26 crest tee, the jersey-style TONGA 00 Player Tee, the Est. 1986 oversized crest tee, snapbacks and truckers, in black and Tonga red, S to 6XL.",
   aboutH="Mate Ma'a Tonga merch, made for the red wall",
   about=["Mate Ma'a Tonga means to die for Tonga, and Tongan fans live up to it: a sea of red flags and voices wherever the team plays. This collection brings that pride to tees and hats for Rugby League World Cup 2026 and every game after it.",
     "Start with the 676 tee. 676 is Tonga's international dialling code, the number that rings home, and it's printed large across the back in red and white. The RLWC26 tee frames the Tonga crest with an arched MATE MA'A and 19 / 86, the Player Tee gives you a jersey-style TONGA 00 back, and the heavyweight Crest Oversized Tee puts the Est. 1986 crest front and centre. For a quieter look, the Silver Blackout runs 676 down the spine in grey on black.",
     "Tees come in black and Tonga red, sizes S to 6XL at one price. Finish the outfit with the white and crimson High Profile Snapback or the black 2026 Trucker; the Game Day Set takes $10 off a tee and hat together, and Buy 3 tees, get 1 free covers family orders. These are independent PMN+ supporter designs, printed to order and shipped across the USA."]),
 "toa-samoa": dict(name="Toa Samoa", title="Toa Samoa Shirts, Hats & Merch | RLWC 2026 | PMN+",
   meta="Toa Samoa shirts, hats and merch for Rugby League World Cup 2026: Samoa 685 tees, RLWC26 and player tees in S–6XL, oversized crest tees and snapbacks.",
   intro="Toa Samoa shirts, hats and merch for Rugby League World Cup 2026: the 685 tee, the RLWC26 crest tee, the jersey-style SAMOA 00 Player Tee, the Est. 1986 oversized crest tee, snapbacks and truckers, in black and royal blue, S to 6XL.",
   aboutH="Toa Samoa merch for the blue army",
   about=["Toa means warrior in Samoan, and Toa Samoa fans bring that spirit to every game in a wall of royal blue. This collection is built for Rugby League World Cup 2026, with tees and hats you'll keep wearing long after the tournament.",
     "The 685 tee is the one most fans start with: 685 is Samoa's international dialling code, worn here as a mark of home in a big TOA SAMOA 685 back print. The RLWC26 tee sets the Samoa crest under an arched TOA with 19 and 86 either side, the Player Tee has a jersey-style SAMOA 00 back, and the heavyweight Crest Oversized Tee carries the Est. 1986 crest with a siapo-inspired tapa band. The Silver Blackout keeps it low-key: O Ai Le Toa Samoa on the chest and 685 down the spine in grey on black.",
     "Tees come in black and royal blue, S to 6XL at one price, so big and tall sizes cost the same. Add the navy and white High Profile Snapback or the black 2026 Trucker and the Game Day Set takes $10 off the pair; Buy 3 tees, get 1 free makes kitting out the aiga easier. All independent PMN+ supporter designs, printed to order and shipped across the USA."]),
 "pmn-plus": dict(name="PMN+", title="PMN+ Apparel: Logo Tee, Trucker & Dad Hat | PMN+ Shop",
   meta="Shop PMN+ apparel from the Pasifika media platform: the PMN+ Logo Tee, Trucker Hat and Classic Dad Hat. Printed to order and shipped across the USA.",
   intro="PMN+ is a multimedia platform for the Pasifika community: music, news, sports and culture, shared worldwide. PMN+ apparel carries that same pride on everyday pieces, from the Logo Tee to the Trucker and Classic Dad Hat, printed to order and shipped across the USA.",
   aboutH="Everyday PMN+ apparel",
   about=["PMN+ shares Pasifika music, sport and culture with the community worldwide. These core pieces aren't tied to a tournament: the Logo Tee with the circle mark on the chest, the mesh-back PMN+ Trucker and the khaki Classic Dad Hat.",
     "The Logo Tee is 5.3 oz, 100% cotton in S to 6XL at one price, and it counts toward Buy 3 tees, get 1 free with any team tees. Add a hat and the Game Day Set takes $10 off the pair."]),
}

if __name__ == "__main__":
    json.dump(dict(domain=DOMAIN, policy=POLICY, products=P, sharedFaq=SHARED_FAQ, collections=COLLECTIONS),
              open("seo_content.json", "w"), ensure_ascii=False, indent=1)
    print(len(P), "products")
