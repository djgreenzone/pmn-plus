import json, re, os, glob, html
from PIL import Image
C=json.load(open('seo_content.json')); D=C['domain']; POL=C['policy']
s=open('site2/index.html').read()
a=s.index('const META=')+len('const META='); b=s.index('};\nfor(const m of Object.values(META))')+1
META=json.loads(s[a:b])
HIDE=json.loads(re.search(r'HIDE=(\[[^\]]*\])',open('make_shop.py').read()).group(1))
SOLD=set(json.loads(re.search(r'SOLD=new Set\((\[[^\]]*\])\)',open('shopify_layer.js').read()).group(1)))
REST={k:int(v) for k,v in re.findall(r'"([a-z0-9-]+)":(\d+)',re.search(r'const REST=\{([^}]*)\}',s).group(1))}
def hero_angle(pid):
    h=META[pid].get('hi') or {};r=REST.get(pid,0)
    for a in h:
        if abs(((int(a)-r)%360+540)%360-180)<=8: return a
    return None
prods=[dict(id=m[0],name=m[1].replace('\u2011','-').replace('MMT ','Mate Ma\'a Tonga '),price=int(m[2]),kind=m[3],team=m[4],colour=m[5].replace(' / ','/')) for m in re.findall(r'\{id:"([^"]+)",name:"([^"]+)",short:"[^"]*",price:(\d+),kind:"(\w+)",team:"(\w+)"[^}]*?colourName:"([^"]+)"',s)]
TEAM={'samoa':'Toa Samoa','tonga':"Mate Ma'a Tonga",'pmn':'PMN+'}
COLL={'samoa':'toa-samoa','tonga':'mate-maa-tonga','pmn':'pmn-plus'}
def sizes(p):
    if p['kind']=='hat': return ['One size']
    if 'oversized' in p['id'] or p['colour'].startswith('Black'): return ['S','M','L','XL','2XL','3XL','4XL','5XL']
    return ['L','XL','2XL','3XL']  # red / royal: L–3XL only
GROUP={'mmt-rlwc26-black':'mate-maa-tonga-rlwc26-tee','mmt-rlwc26-red':'mate-maa-tonga-rlwc26-tee','toa-rlwc26-black':'toa-samoa-rlwc26-tee','toa-rlwc26-royal':'toa-samoa-rlwc26-tee','mmt-player-black':'mate-maa-tonga-player-tee','mmt-player-red':'mate-maa-tonga-player-tee','toa-player-black':'toa-samoa-player-tee','toa-player-royal':'toa-samoa-player-tee','mmt-676-tee':'mate-maa-tonga-676-tee','mmt-676-black':'mate-maa-tonga-676-tee','toa-685-tee':'toa-samoa-685-tee','toa-685-black':'toa-samoa-685-tee'}
def trim(t,n):
    return t if len(t)<=n else t[:n-1].rsplit(' ',1)[0].rstrip(',.;:')+'…'
out={'domain':D,'policy':POL,'sharedFaq':C['sharedFaq'],'collections':{},'products':{}}
org={"@type":"Organization","@id":D+"/#org","name":"PMN+","alternateName":"Polynesian Music Network Plus","url":D,"logo":D+"/shop/brand/pmn-plus-logo-black.png","legalName":"Polynesian Music"}
ret={"@type":"MerchantReturnPolicy","applicableCountry":"US","returnPolicyCategory":"https://schema.org/MerchantReturnNotPermitted"}
prods=[p for p in prods if p['id'] not in HIDE]
ship={"@type":"OfferShippingDetails","shippingRate":{"@type":"MonetaryAmount","value":"8.00","currency":"USD"},"shippingDestination":{"@type":"DefinedRegion","addressCountry":"US"},"deliveryTime":{"@type":"ShippingDeliveryTime","handlingTime":{"@type":"QuantitativeValue","minValue":2,"maxValue":4,"unitCode":"DAY"},"transitTime":{"@type":"QuantitativeValue","minValue":3,"maxValue":7,"unitCode":"DAY"}}}
for p in prods:
    sc=C['products'][p['id']]; m=META[p['id']]; slug=m['seo']; url=f"{D}/shop/{slug}"
    ha=hero_angle(p['id']);order=sorted(m['hi'].items(),key=lambda x:(x[0]!=ha,int(x[0])))
    imgs=[f"{D}/shop/hires/{p['id']}/{n}.webp" for a_,n in order]
    og=f"{D}/shop/og/{slug}.jpg"
    if not imgs and m.get('src')=='shopify photo': imgs=['https://cdn.shopify.com/s/files/1/0814/5030/3687/files/7c0c7b35-e27f-4a48-9b05-c0ef2d0a4375-481207-front-ecru-zoom.png']
    nc=f"{p['name']} – {p['colour']}"
    cands=([nc+" | World Cup 2026 | PMN+"] if 'RLWC' in p['name'] else [])+([nc+" | RLWC 2026 | PMN+"] if p['team']!='pmn' else [nc+" | Pasifika Apparel"])+[nc+" | PMN+",nc]
    title=next(t for t in cands if len(t)<=60)
    tails=[f"${p['price']}" + (" · RLWC 2026" if p['team']!='pmn' else "") + ". Printed to order and shipped across the USA by PMN+, the Pasifika media platform.",
           f"${p['price']}. Printed to order and shipped across the USA by PMN+, the Pasifika media platform.",
           f"${p['price']}. Printed to order and shipped across the USA by PMN+.",
           f"${p['price']}. Printed to order and shipped across the USA.",
           f"${p['price']} · Ships across the USA."]
    meta=next(sc["m"]+" "+t for t in tails if len(sc["m"]+" "+t)<=155)
    faq=[{"q":q,"a":a_} for q,a_ in sc['faq']+C['sharedFaq']]
    prod={"@type":"Product","@id":url+"#product","name":f"{p['name']} – {p['colour']}","sku":slug,"brand":{"@type":"Brand","name":"PMN+"},"color":p['colour'],
          "category":"Apparel & Accessories > "+("Clothing Accessories > Hats" if p['kind']=='hat' else "Clothing > Shirts & Tops"),
          "image":imgs,"description":" ".join(sc['d']),"url":url,
          "audience":{"@type":"PeopleAudience","suggestedGender":"unisex"},
          "offers":{"@type":"Offer","url":url,"price":f"{p['price']}.00","priceCurrency":"USD","availability":"https://schema.org/"+("OutOfStock" if p['id'] in SOLD else "InStock"),"itemCondition":"https://schema.org/NewCondition","seller":{"@id":D+"/#org"},"hasMerchantReturnPolicy":ret,"shippingDetails":ship}}
    if p['id'] in GROUP: prod["isVariantOf"]={"@type":"ProductGroup","name":p['name'],"brand":{"@type":"Brand","name":"PMN+"},"productGroupID":GROUP[p['id']],"variesBy":["https://schema.org/color","https://schema.org/size"]}
    crumbs={"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Shop","item":D+"/shop"},{"@type":"ListItem","position":2,"name":TEAM[p['team']],"item":f"{D}/shop/{COLL[p['team']]}"},{"@type":"ListItem","position":3,"name":p['name'],"item":url}]}
    faqld={"@type":"FAQPage","mainEntity":[{"@type":"Question","name":f['q'],"acceptedAnswer":{"@type":"Answer","text":f['a']}} for f in faq]}
    out['products'][p['id']]=dict(slug=slug,url=url,title=title,meta=meta,h1=p['name'],colour=p['colour'],price=p['price'],team=p['team'],keyword=sc['kw'],
        description=sc['d'],faq=faq,sizes=sizes(p),images=imgs,og=og,sold=p['id'] in SOLD,kind=p['kind'],teamName=TEAM[p['team']],alt=[f"{p['name']} in {p['colour'].lower()}, {n.rsplit('-',1)[-1] if not n.endswith(('front-left','front-right','back-left','back-right')) else ' '.join(n.split('-')[-2:])} view" for a_,n in order],jsonld={"@context":"https://schema.org","@graph":[org,prod,crumbs,faqld]})
for k,c in C['collections'].items():
    members=[p['id'] for p in prods] if k=='all' else [p['id'] for p in prods if COLL[p['team']]==k]
    out['collections'][k]=dict(c,url=f"{D}/shop/{k}",products=members,jsonld={"@context":"https://schema.org","@type":"CollectionPage","name":c['name'],"url":f"{D}/shop/{k}","description":c['meta'],
        "mainEntity":{"@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"url":out['products'][pid]['url']} for i,pid in enumerate(members)]}})
os.makedirs('site2/seo',exist_ok=True)
json.dump(out,open('site2/seo/seo-data.json','w'),ensure_ascii=False,indent=1)
# ---- Merchant Center feed (one row per size) ----
cols=['id','item_group_id','title','description','link','image_link','additional_image_link','availability','price','brand','condition','google_product_category','product_type','gender','age_group','color','size','size_system','material','shipping(country)','custom_label_0','identifier_exists']
rows=['\t'.join(cols)]
for p in prods:
    o=out['products'][p['id']]; grp=GROUP.get(p['id'],o['slug'])
    if META[p['id']].get('src')=='shopify photo': continue  # test product: keep out of Google Shopping
    mat='100% cotton' if p['kind']=='tee' else ''
    gpc='173' if p['kind']=='hat' else '212'
    for z in o['sizes']:
        sid=f"{o['slug']}-{z.lower().replace(' ','-')}"
        rows.append('\t'.join([sid,grp,trim(f"{p['name']} – {p['colour']}"+("" if z=='One size' else f" – {z}"),150)," ".join(o['description']),
          o['url']+("" if z=='One size' else f"?size={z}"),o['images'][0],",".join(o['images'][1:10]),'out_of_stock' if p['id'] in SOLD else 'in_stock',f"{p['price']}.00 USD",'PMN+','new',gpc,
          f"{TEAM[p['team']]} > {'Hats' if p['kind']=='hat' else 'Tees'}",'unisex','adult',p['colour'],z,'US',mat,'US','RLWC 2026' if p['team'] in ('samoa','tonga') else 'PMN+','no']))  # own designs: no GTIN/MPN
feed='\n'.join(rows)+'\n'
open('site2/seo/merchant-center-feed.tsv','w').write(feed)
open('../merchant-center-feed.txt','w').write(feed)  # public URL for Merchant Center scheduled fetch
# ---- sitemap with images ----
u=['<?xml version="1.0" encoding="UTF-8"?>','<?xml-stylesheet type="text/xsl" href="/sitemap.xsl"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
u.append(f"  <url><loc>{D}/</loc><lastmod>2026-10-02</lastmod><image:image><image:loc>{D}/assets/pmn-plus-og-music-culture-tradition-sports.jpg</image:loc></image:image></url>")
u.append(f"  <url><loc>{D}/shop</loc><lastmod>2026-10-02</lastmod><image:image><image:loc>{D}/shop/pmn-plus-shop-og-rlwc-2026-toa-samoa-mate-maa-tonga.jpg</image:loc></image:image></url>")
CIMG={'toa-samoa':['shop/brand/toa-samoa-rugby-league-crest.webp'],'mate-maa-tonga':['shop/brand/mate-maa-tonga-rugby-league-crest.webp']}   # collection page images
for k,c in out['collections'].items():
    slug=c['url'].rstrip('/').rsplit('/',1)[-1]
    imgs=[f"{D}/{x}" for x in CIMG.get(slug,[])]+[f"{D}/shop/pmn-plus-shop-og-rlwc-2026-toa-samoa-mate-maa-tonga.jpg"]
    u.append(f"  <url><loc>{c['url']}</loc><lastmod>2026-10-02</lastmod>"+"".join(f"<image:image><image:loc>{i}</image:loc></image:image>" for i in imgs)+"</url>")
for pid,o in out['products'].items():
    u.append(f"  <url><loc>{o['url']}</loc><lastmod>2026-10-02</lastmod>"+"".join(f"<image:image><image:loc>{html.escape(i)}</image:loc></image:image>" for i in [o['og']]+o['images'])+"</url>")
u.append(f"  <url><loc>{D}/about</loc><lastmod>2026-10-03</lastmod><image:image><image:loc>{D}/assets/about/pmn-plus-about-og.jpg</image:loc></image:image><image:image><image:loc>{D}/assets/about/pmn-plus-reporter-rugby-league-las-vegas-allegiant-stadium.webp</image:loc></image:image><image:image><image:loc>{D}/assets/about/pmn-plus-photographer-hsbc-la-sevens.webp</image:loc></image:image><image:image><image:loc>{D}/assets/about/pmn-plus-locker-room-interview.webp</image:loc></image:image><image:image><image:loc>{D}/assets/about/pmn-plus-photographer-rugby-league-las-vegas-sideline.webp</image:loc></image:image><image:image><image:loc>{D}/assets/about/pmn-plus-photographer-pasifika-music-festival.webp</image:loc></image:image><image:image><image:loc>{D}/assets/about/pmn-plus-instagram-polynesianmusic-iphone.webp</image:loc></image:image></url>")
u.append(f"  <url><loc>{D}/privacy-policy</loc><lastmod>2026-10-02</lastmod></url>")
u.append(f"  <url><loc>{D}/terms</loc><lastmod>2026-10-02</lastmod></url>")
u.append(f"  <url><loc>{D}/shipping</loc><lastmod>2026-10-03</lastmod></url>")
u.append(f"  <url><loc>{D}/returns</loc><lastmod>2026-10-03</lastmod></url>")
u.append(f"  <url><loc>{D}/contact</loc><lastmod>2026-10-03</lastmod></url>")
u.append('</urlset>')
open('site2/seo/sitemap-shop.xml','w').write('\n'.join(u)+'\n')
print(len(rows)-1,'feed rows')
for pid,o in out['products'].items(): print(f"{len(o['title']):>3} {len(o['meta']):>3}  {o['title']}")
