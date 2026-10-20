# Run by make_shop.py as its last step.
# 1. Makes the shop indexable and gives every product / collection its own URL inside the app
#    (/shop/<product-slug>, /shop/<collection>), with title, description, canonical and share tags
#    kept in sync as people browse.
# 2. Writes a pre-rendered page per product and per collection next to the shop page
#    (shop/<slug>/index.html) with its own <head>, structured data and visible content,
#    so search engines and link previews see the right thing without running JavaScript.
# 3. Writes the site sitemap (../sitemap.xml) with image entries.
import json, os, re, sys, html
D_=os.path.dirname(os.path.abspath(__file__))+'/'
OUT=sys.argv[1]; SHOPDIR=os.path.dirname(os.path.abspath(OUT))
SD=json.load(open(D_+'site2/seo/seo-data.json'))
DOM=SD['domain']
s=open(OUT).read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:80],s.count(a));s=s.replace(a,b)
E=lambda t:html.escape(t,quote=True)

# ---------- indexable ----------
rep('<meta name="robots" content="noindex,nofollow">','<meta name="robots" content="index,follow,max-image-preview:large">')
rep('const BASE_TITLE="PMN+ Store Hero";','const BASE_TITLE="Shop PMN+ | RLWC 2026 Toa Samoa & Mate Ma\'a Tonga Merch";')
rep('<h1>Spin lab</h1>','<h2>Spin lab</h2>')

# ---------- app hooks: every view change reports itself to the router ----------
rep('document.title=so.title||p.name;','document.title=so.title||p.name;window.pmnRoute&&pmnRoute("p",p.id);')
rep('document.title=c.title;grid();','document.title=c.title;window.pmnRoute&&pmnRoute("c",k);grid();')
rep('busy=true;document.title=BASE_TITLE;$("pSticky")','busy=true;document.title=BASE_TITLE;window.pmnRoute&&(origin==="coll"?pmnRoute("c",Coll.key()):pmnRoute("h"));$("pSticky")')
rep('el.hidden=true;document.title=BASE_TITLE;Hero.show()}','el.hidden=true;document.title=BASE_TITLE;window.pmnRoute&&pmnRoute("h");Hero.show()}')
rep('$("pageBack").onclick=()=>{$("page").hidden=true;document.title=BASE_TITLE;','$("pageBack").onclick=()=>{$("page").hidden=true;if(window.pmnRoute)pmnRoute.refresh();else document.title=BASE_TITLE;')
rep('return{open,focus:','return{open,key:()=>key,focus:')
rep('return{open,close,current:()=>cur};','return{open,close,swap:id=>swap(id),current:()=>cur};')
rep('if(reduceMotion){Hero.stop();$("hero").hidden=true;$("coll").hidden=true;pdp.classList.remove("entering");busy=false;return}',
    'if(reduceMotion||window.pmnInstant){Hero.stop();$("hero").hidden=true;$("coll").hidden=true;pdp.classList.remove("entering");busy=false;return}')

# ---------- speed: deep links (/shop/<product>, /shop/<collection>) don't boot the hero carousel ----------
# Pre-rendered product/collection pages ship with #hero hidden. The carousel then holds back its ~2 MB of
# images and 360° prefetches until someone actually goes to the shop home (Hero.show()).
rep('const Hero=(()=>{const PRODUCTS=HERO_P;',
    'let HLIVE=!$("hero").hidden;const HDEFER=[],hsrc=(im,u)=>{if(HLIVE)im.src=u;else HDEFER.push([im,u])};\nconst Hero=(()=>{const PRODUCTS=HERO_P;')
rep('im.decoding="async";im.src=heroURL(p.id);arc.append(im);return im});','im.decoding="async";hsrc(im,heroURL(p.id));arc.append(im);return im});')
rep('items[i].src=hiURL(p.id,f);','hsrc(items[i],hiURL(p.id,f));')
rep('a.decoding="async";a.src=hiURL(p.id,k);a.style.opacity=0;arc.append(a);','a.decoding="async";hsrc(a,hiURL(p.id,k));a.style.opacity=0;arc.append(a);')
rep('c.decoding="async";c.src=crestURL(p.team);','c.decoding="async";hsrc(c,crestURL(p.team));')
rep('show(){hero.hidden=false;measure();','show(){if(!HLIVE){HLIVE=true;HDEFER.splice(0).forEach(([im,u])=>im.src=u);label(0)}hero.hidden=false;measure();')
rep('\nHero.init();\n','\nif(HLIVE)Hero.init();\n')
# other colourways' 360° frames: wait until the page has finished loading
rep('setTimeout(()=>p.opts.slice(1).forEach(o=>loadFrames(o)),1500);',
    '{const f=()=>setTimeout(()=>p.opts.slice(1).forEach(o=>loadFrames(o)),1500);document.readyState==="complete"?f():addEventListener("load",f,{once:true})}')
rep('crests.map(t=>`<img alt="" src="${crestURL(t)}">`)','crests.map(t=>`<img alt="" loading="lazy" decoding="async" src="${crestURL(t)}">`)')
rep('muted loop playsinline preload="metadata" aria-hidden="true"','muted loop playsinline preload="none" aria-hidden="true"')  # plays on scroll-into-view anyway
# the product page's crest is already right in the HTML: don't reset it (that re-triggered the largest paint after the app loaded)
rep('$("pdpCrest").src=crestURL(p.team);','{const cu=crestURL(p.team),ce=$("pdpCrest");if(ce.getAttribute("src")!==cu)ce.src=cu}')
# below-the-fold team crests on the shop home: lazy (they also downloaded inside the hidden hero on every product page)
rep('<img src="brand/toa-samoa-rugby-league-crest.webp" alt="" id="hSamoaCrest">','<img src="brand/toa-samoa-rugby-league-crest.webp" alt="" id="hSamoaCrest" loading="lazy" decoding="async">')
rep('<img src="brand/mate-maa-tonga-rugby-league-crest.webp" alt="" id="hTongaCrest">','<img src="brand/mate-maa-tonga-rugby-league-crest.webp" alt="" id="hTongaCrest" loading="lazy" decoding="async">')

# ---------- crawlable product + collection links (real <a href>, app still opens in place) ----------
m=re.search(r'\nconst SEO=\{.*?\n',s); assert m
s=s[:m.end()]+'const pmnURL=id=>SEO.products[id]?"/shop/"+SEO.products[id].slug:"/shop";\nconst pmnNav=(a,fn)=>{a.addEventListener("click",e=>{if(e.metaKey||e.ctrlKey||e.shiftKey||e.button)return;e.preventDefault();fn()})};\n'+s[m.end():]
# shop-home cards
rep('const card=(p,cls)=>{const b=document.createElement("button");b.className=cls;b.type="button";b.dataset.pid=p.id;',
    'const card=(p,cls)=>{const b=document.createElement("a");b.className=cls;b.href=pmnURL(p.id);b.dataset.pid=p.id;')
rep('b.onclick=()=>PDP.open(p.id,b.querySelector("img"),"home");return b};','pmnNav(b,()=>PDP.open(p.id,b.querySelector("img"),"home"));return b};')
# team tiles
rep('const tile=(k,cls,crests)=>{const b=document.createElement("button");b.className="team "+cls;b.type="button";',
    'const tile=(k,cls,crests)=>{const b=document.createElement("a");b.className="team "+cls;b.href="/shop/"+k;')
rep('b.onclick=()=>Coll.open(k);g.append(b)};','pmnNav(b,()=>Coll.open(k));g.append(b)};')
# collection grid
rep('.forEach(p=>{const b=document.createElement("button");b.className="gcard";b.dataset.id=p.id;',
    '.forEach(p=>{const b=document.createElement("a");b.className="gcard";b.href=pmnURL(p.id);b.dataset.id=p.id;')
rep('b.onclick=()=>PDP.open(p.id,b.querySelector("img"),"coll");g.append(b)})}','pmnNav(b,()=>PDP.open(p.id,b.querySelector("img"),"coll"));g.append(b)})}')
# "More from the drop" on product pages
rep('rest.slice(0,8).forEach(o=>{const b=document.createElement("button");b.className="card";',
    'rest.slice(0,8).forEach(o=>{const b=document.createElement("a");b.className="card";b.href=pmnURL(o.id);')
rep('b.onclick=()=>{$("pdpScroll").scrollTo({top:0,behavior:reduceMotion?"auto":"smooth"});swap(o.id)};$("pAlso").append(b)});',
    'pmnNav(b,()=>{$("pdpScroll").scrollTo({top:0,behavior:reduceMotion?"auto":"smooth"});swap(o.id)});$("pAlso").append(b)});')
# product view thumbnails: describe the view for image search
rep('const im=new Image();im.loading="lazy";im.alt="";im.src=`hires/${p.id}/${name}.webp`;',
    'const im=new Image();im.loading="lazy";im.alt=altFor(p,views(ang).toLowerCase());im.src=`hires/${p.id}/${name}.webp`;')
rep('.size.so{',':where(a.card,a.big,a.gcard,a.team){box-sizing:border-box;padding:1px 6px;color:inherit;text-decoration:none;-webkit-tap-highlight-color:transparent}.size.so{')

# ---------- router ----------
OG0=DOM+'/shop/pmn-plus-shop-og-rlwc-2026-toa-samoa-mate-maa-tonga.jpg'
D0=re.search(r'<meta name="description" content="([^"]*)">',s).group(1)
ROUTER='''<script>/* ROUTES */(()=>{const D=%s,OG0=%s,D0=%s,SL={};
Object.entries(SEO.products).forEach(([id,o])=>{if(BY[id])SL[o.slug]=id});
const set=(sel,v)=>{document.querySelectorAll(sel).forEach(e=>e.setAttribute(e.tagName==="LINK"?"href":"content",v))};
const info=(k,key)=>{if(k==="p"){const o=SEO.products[key];return{u:"/shop/"+o.slug,t:o.title,d:o.meta,img:D+"/shop/og/"+o.slug+".jpg"}}
  if(k==="c"){const c=SEO.collections[key];return{u:"/shop/"+key,t:c.title,d:c.meta,img:OG0}}return{u:"/shop",t:BASE_TITLE,d:D0,img:OG0}};
let cur={k:"h"},mode="push",last=0;
window.pmnRoute=(k,key)=>{if(k==="p"&&!SEO.products[key])return;if(k==="c"&&!SEO.collections[key])return;cur={k,key};const i=info(k,key);
  document.title=i.t;set('meta[name="description"],meta[property="og:description"],meta[name="twitter:description"]',i.d);
  set('meta[property="og:title"],meta[name="twitter:title"]',i.t);set('link[rel="canonical"],meta[property="og:url"]',D+i.u);
  set('meta[property="og:image"],meta[property="og:image:secure_url"],meta[name="twitter:image"]',i.img);
  if(mode==="none")return;const path=location.pathname.replace(/\\/+$/,"")||"/";if(path===i.u&&!location.hash)return;
  const now=Date.now(),r=mode==="replace"||location.hash||now-last<150;history[r?"replaceState":"pushState"]({pmn:1},"",i.u);if(!r)last=now};
pmnRoute.refresh=()=>{const m=mode;mode="none";pmnRoute(cur.k,cur.key);mode=m};
const parse=p=>{p=decodeURIComponent(p).replace(/^\\/shop\\/?/,"").replace(/\\/+$/,"");if(!p)return{k:"h"};if(SL[p])return{k:"p",key:SL[p]};if(SEO.collections[p])return{k:"c",key:p};return{k:"h"}};
const show=r=>{window.pmnInstant=true;try{$("page").hidden=true;$("pSticky").classList.remove("on");
  if(r.k==="p"){if(!$("pdp").hidden&&PDP.current()){if(PDP.current()!==r.key)PDP.swap(r.key)}else{const im=new Image();im.src=heroURL(r.key);PDP.open(r.key,im,"home")}}
  else if(r.k==="c")Coll.open(r.key);
  else{const back=$("hero").hidden;$("pdp").hidden=true;$("coll").hidden=true;if(back)Hero.show();pmnRoute("h")}}catch(e){console.warn("route",e)}finally{window.pmnInstant=false}};
window.pmnGo=p=>show(parse(p));
addEventListener("popstate",()=>{mode="none";show(parse(location.pathname));mode="push"});
const r0=parse(location.pathname);if(r0.k!=="h"){mode="replace";show(r0);mode="push"}
})();</script>
'''%(json.dumps(DOM),json.dumps(OG0),json.dumps(html.unescape(D0)))
# router goes right after the app script, before the deep-link helper
i=s.index('\n<script>/* DEEPLINK */'); s=s[:i]+'\n'+ROUTER+s[i:]
# ---------- speed: the ~170 KB shop app is the same on every shop page, so ship it as one cacheable file ----------
import hashlib, glob as _glob
APP=max(re.findall(r'<script>(.*?)</script>',s,re.S),key=len); assert len(APP)>100000 and 'const Hero=' in APP
app_name='app-'+hashlib.sha1(APP.encode()).hexdigest()[:10]+'.js'
for old in _glob.glob(os.path.join(SHOPDIR,'app-*.js')):
    if os.path.basename(old)!=app_name: os.remove(old)
open(os.path.join(SHOPDIR,app_name),'w').write(APP)
rep('<script>'+APP+'</script>','<script src="/shop/'+app_name+'"></script>')
# Run the end-of-page scripts after the HTML has painted: defer the files, and make the two small inline
# scripts modules (modules are deferred too and keep document order, so ROUTES/DEEPLINK still run after the app).
for f_ in ['/assets/pmn-config.js','/assets/pmn-nav.js','/shop/'+app_name]: rep(f'<script src="{f_}"></script>',f'<script src="{f_}" defer></script>')
rep('<script>/* ROUTES */','<script type="module">/* ROUTES */')
rep('<script>/* DEEPLINK */','<script type="module">/* DEEPLINK */')
open(OUT,'w').write(s)
BASE=s

# ---------- pre-rendered pages ----------
def head(page,title,desc,url,img,alt,ld,extra='',ogtype='website'):
    t=E(title);d=E(desc)
    page=re.sub(r'<title>.*?</title>',lambda m:'<title>'+t+'</title>',page,count=1,flags=re.S)
    page=re.sub(r'<meta name="description" content="[^"]*">',lambda m:f'<meta name="description" content="{d}">',page,count=1)
    for k,v in [('link rel="canonical" href',url),('meta property="og:url" content',url),('meta property="og:title" content',t),('meta name="twitter:title" content',t),
                ('meta property="og:description" content',d),('meta name="twitter:description" content',d),('meta property="og:image" content',img),
                ('meta property="og:image:secure_url" content',img),('meta name="twitter:image" content',img),('meta property="og:image:alt" content',E(alt)),
                ('meta name="twitter:image:alt" content',E(alt)),('meta property="og:type" content',ogtype)]:
        page,n=re.subn('<'+re.escape(k)+r'="[^"]*">',lambda m:'<'+k+'="'+v+'">',page,count=1); assert n==1,k
    page=page.replace('<meta name="twitter:card" content="summary_large_image">','<meta name="twitter:card" content="summary_large_image">\n'+extra,1)
    page,n=re.subn(r'<script type="application/ld\+json">.*?</script>',lambda m:'<script type="application/ld+json">'+json.dumps(ld,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+'</script>',page,count=1,flags=re.S); assert n==1
    return page
def sub1(page,pat,repl):
    page,n=re.subn(pat,lambda m:repl,page,count=1,flags=re.S); assert n==1,pat; return page
TEAMK={'samoa':'toa-samoa','tonga':'mate-maa-tonga','pmn':'pmn-plus'}
n_p=0
for pid,o in SD['products'].items():
    url=o['url']; img=o['og']
    alt=f"{o['h1']} in {o['colour'].lower()} from the PMN+ {o['teamName']} collection"
    extra=(f'<meta property="product:brand" content="PMN+">\n<meta property="product:price:amount" content="{o["price"]}.00">\n<meta property="product:price:currency" content="USD">\n'
           f'<meta property="product:availability" content="{"out of stock" if o["sold"] else "in stock"}">\n<meta property="product:condition" content="new">\n<meta property="product:retailer_item_id" content="{o["slug"]}">\n')
    pg=head(BASE,o['title'],o['meta'],url,img,alt,o['jsonld'],extra,'product')
    pg=pg.replace('<link rel="preconnect" href="https://polynesianmusicnetwork.myshopify.com" crossorigin>',
                  '<link rel="preconnect" href="https://polynesianmusicnetwork.myshopify.com" crossorigin>\n<link rel="preload" as="image" href="'+o['images'][0].split('/shop/')[1]+'">',1)
    # paint the product view straight from the HTML (hero carousel stays hidden and idle)
    pg=sub1(pg,r'<section id="hero" class="view" ','<section id="hero" class="view" hidden ')
    pg=sub1(pg,r'<section id="pdp" class="view entering" hidden ','<section id="pdp" class="view" data-team="'+o['team']+'" style="--flood:'+{'pmn':'#141416','samoa':'#0b1b5e','tonga':'#8f0a14'}[o['team']]+'" ')
    csrc={'samoa':'brand/toa-samoa-rugby-league-crest.webp','tonga':'brand/mate-maa-tonga-rugby-league-crest.webp','pmn':'brand/pmn-plus-logo-white.svg'}[o['team']]
    pg=sub1(pg,r'<img class="crest" id="pdpCrest" alt="" src="[^"]*">',f'<img class="crest" id="pdpCrest" alt="" src="{csrc}" fetchpriority="high">')
    # visible content in the HTML itself (the app re-renders the same thing)
    pg=sub1(pg,r'<button class="eyebrow team-link" id="pTeam" type="button">[^<]*</button>',f'<button class="eyebrow team-link" id="pTeam" type="button">{E(o["teamName"])}</button>')
    pg=sub1(pg,r'<h2 id="pName">[^<]*</h2>',f'<h1 id="pName">{E(o["h1"])}</h1>')
    pg=re.sub(r'<h1 class="hero-h">(.*?)</h1>',r'<h2 class="hero-h">\1</h2>',pg,count=1)
    pg=sub1(pg,r'<strong class="num" id="pPrice">[^<]*</strong>',f'<strong class="num" id="pPrice">${o["price"]}.00</strong>')
    pg=sub1(pg,r'<div id="pDesc"></div>','<div id="pDesc">'+''.join(f'<p>{E(t)}</p>' for t in o['description'])+'</div>')
    th=''.join(f'<button class="thumb" type="button"><img loading="lazy" src="{u.split("/shop/")[1]}" alt="{E(a)}" width="72" height="72"></button>' for u,a in zip(o['images'],o['alt']))
    T0='<div class="thumbs reveal d1" id="pThumbs" role="group" aria-label="Product views"></div>'
    assert pg.count(T0)==1;pg=pg.replace(T0,T0[:-6]+th+'</div>')
    os.makedirs(os.path.join(SHOPDIR,o['slug']),exist_ok=True)
    open(os.path.join(SHOPDIR,o['slug'],'index.html'),'w').write(pg); n_p+=1
for k,c in SD['collections'].items():
    url=c['url']
    crumbs={"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Shop","item":DOM+"/shop"},{"@type":"ListItem","position":2,"name":c['name'],"item":url}]}
    ld={"@context":"https://schema.org","@graph":[{kk:vv for kk,vv in c['jsonld'].items() if kk!='@context'},crumbs]}
    for it,pid in zip(ld['@graph'][0]['mainEntity']['itemListElement'],c['products']): it['name']=SD['products'][pid]['h1']
    pg=head(BASE,c['title'],c['meta'],url,OG0,"Toa Samoa and Mate Ma'a Tonga tees and snapbacks from PMN+",ld)
    pg=sub1(pg,r'<section id="hero" class="view" ','<section id="hero" class="view" hidden ')
    pg=sub1(pg,r'<section id="coll" class="view" hidden ','<section id="coll" class="view" ')
    pg=sub1(pg,r'<h2 id="collH" class="sr"></h2><p id="cIntro" class="sr"></p>',f'<h1 id="collH" class="sr">{E(c["name"])}</h1><p id="cIntro" class="sr">{E(c["intro"])}</p>')
    pg=re.sub(r'<h1 class="hero-h">(.*?)</h1>',r'<h2 class="hero-h">\1</h2>',pg,count=1)
    cards=''.join(f'<a class="gcard" href="/shop/{SD["products"][pid]["slug"]}"><span class="im"><img loading="lazy" src="{SD["products"][pid]["images"][0].split("/shop/")[1]}" alt="{E(SD["products"][pid]["alt"][0])}"></span><b>{E(SD["products"][pid]["h1"])}</b><span class="num">{"Sold out" if SD["products"][pid]["sold"] else "$"+str(SD["products"][pid]["price"])+".00"}</span></a>' for pid in c['products'])
    pg=sub1(pg,r'<div class="grid" id="cGrid"></div>',f'<div class="grid" id="cGrid">{cards}</div>')
    os.makedirs(os.path.join(SHOPDIR,k),exist_ok=True)
    open(os.path.join(SHOPDIR,k,'index.html'),'w').write(pg)
# ---------- search index for the header search ----------
import unicodedata
def _norm(t): t=unicodedata.normalize('NFD',t.lower());t=''.join(c for c in t if not unicodedata.combining(c));t=re.sub(r"[’'`]","",t);return re.sub(r'[^a-z0-9+]+',' ',t).strip()
_idx=[]
for pid,o in SD['products'].items():
    syn='tee t-shirt tshirt shirt top' if o['kind']=='tee' else 'hat cap snapback trucker'
    _idx.append(dict(id=pid,n=o['h1'],c=o['colour'],t=o['teamName'],k=o['kind'],p=o['price'],s=o['slug'],i='/shop/'+o['images'][0].split('/shop/')[1],so=o['sold'],
      h=' '+_norm(' '.join([o['h1'],o['colour'],o['teamName'],syn,o.get('keyword',''),'rlwc rugby league world cup 2026' if o['team']!='pmn' else 'pmn+ pmn plus pasifika']))+' '))
_idx.sort(key=lambda x:x['so'])
for x in _idx: x['h']=x['h'].strip()
json.dump(_idx,open(os.path.join(SHOPDIR,'search.json'),'w'),ensure_ascii=False,separators=(',',':'))
# ---------- sitemap ----------
open(os.path.join(SHOPDIR,'..','sitemap.xml'),'w').write(open(D_+'site2/seo/sitemap-shop.xml').read())
print('routes ok:',n_p,'product pages,',len(SD['collections']),'collection pages, sitemap')
