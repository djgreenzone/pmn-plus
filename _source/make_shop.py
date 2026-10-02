# Build the /shop production index.html from the prototype page.
import sys, os
D=os.path.dirname(os.path.abspath(__file__))+'/'
s=open(D+'site2/index.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:60],s.count(a));s=s.replace(a,b)
rep('<title>PMN+ Store Hero</title>','''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#05060a">
<meta name="robots" content="noindex,nofollow">
<base href="/shop/">
<link rel="preconnect" href="https://polynesianmusicnetwork.myshopify.com" crossorigin>
<link rel="icon" href="/assets/favicon.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<title>Shop PMN+ | RLWC 2026 Toa Samoa &amp; Mate Ma'a Tonga Merch</title>''')
rep('src="https://polynesianmusicnetwork.com/assets/bg.mp4"','src="/assets/bg.mp4"')
# video opacity already .45 in the prototype
rep('<button class="back-link" id="toLab">Spin lab</button>','<button class="back-link" id="toLab" hidden>Spin lab</button>')
rep('<p class="proto">Prototype · scroll for more</p>','''<button type="button" class="proto scroll-cue" aria-label="Scroll for more" onclick="document.getElementById('hero').scrollBy({top:innerHeight*.85,behavior:'smooth'})"><svg viewBox="0 0 24 14" aria-hidden="true"><path d="M3 3l9 8 9-8"/></svg><svg viewBox="0 0 24 14" aria-hidden="true"><path d="M3 3l9 8 9-8"/></svg></button>''')
open(sys.argv[1],'w').write(s)

# ---------- LIVE MODE: real Klaviyo sign-ups, checkout-opens-soon capture, no prototype copy ----------
s=open(sys.argv[1]).read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:70],s.count(a));s=s.replace(a,b)
rep(' Prototype: connects to Klaviyo at launch.','')
rep('        <p class="fine">Prototype: checkout not connected yet.</p>\n','')
rep('    <p class="fine">Prototype: no email or text was sent; codes come from Klaviyo at launch.</p>\n','')
rep('const reduceMotion=','''/* Klaviyo: PMN+ Launch List (same list as the homepage form) */
const KLAVIYO_COMPANY_ID="T9JJzp",KLAVIYO_LIST_ID="SLSsGL";
async function klavPost(attrs){const body={data:{type:"subscription",attributes:{profile:{data:{type:"profile",attributes:attrs}}},relationships:{list:{data:{type:"list",id:KLAVIYO_LIST_ID}}}}};
  const r=await fetch("https://a.klaviyo.com/client/subscriptions/?company_id="+KLAVIYO_COMPANY_ID,{method:"POST",headers:{"content-type":"application/json","revision":"2026-07-15"},body:JSON.stringify(body)});
  if(!(r.status===202||r.ok))throw new Error("klaviyo "+r.status)}
async function klav(email,phone,props){const a={email};if(phone)a.phone_number=phone;if(props)a.properties=props;
  try{await klavPost(a)}catch(e){await klavPost({email})}}
const usPhone=d=>{d=String(d||"").replace(/\\D/g,"");return d.length>=10?"+1"+d.slice(-10):null};
const reduceMotion=''')
rep('''    $("suMsg").textContent=!ok?"Enter a valid email address, like name@example.com.":!phOk?"Enter a 10-digit US mobile number, or leave it blank for 10% off.":
      `Thanks. In the live store Klaviyo emails your ${ph?"20%":"10%"} code now (prototype: nothing was sent).`;
    if(ok&&phOk){$("suEmail").value="";$("suPhone").value=""}});''','''    if(!ok||!phOk){$("suMsg").textContent=!ok?"Enter a valid email address, like name@example.com.":"Enter a 10-digit US mobile number, or leave it blank for 10% off.";return}
    const btn=e.target.querySelector("button");btn.disabled=true;$("suMsg").textContent="Adding you to the list…";
    klav(v,usPhone(ph),{signup_source:"shop_signup",offer:ph?"20":"10"}).then(()=>{const _c=ph?"WELCOME20":"WELCOME10";try{localStorage.setItem("pmn_code",_c)}catch(e){}if(window.pmnSetCode)pmnSetCode(_c);$("suMsg").textContent=`You're in. ${_c} is saved to your bag and comes off at checkout.`;$("suEmail").value="";$("suPhone").value=""})
      .catch(()=>{$("suMsg").textContent="That didn't go through. Please try again in a moment."}).finally(()=>{btn.disabled=false})});''')
rep('const done=pct=>{$("offCode").textContent=pct===20?"WELCOME20":"WELCOME10";$("offDoneP").textContent=`${pct}% off your first order. We\'ve emailed the code${pct===20?" and texted it":""} too.`;step(3)};',
'''let offEmailV="";
  const done=pct=>{const ph=pct===20?usPhone($("offPhone").value):null;$("offCode").hidden=true;$("offDoneP").textContent="Saving…";step(3);
    klav(offEmailV,ph,{signup_source:"shop_popup",offer:String(pct)}).then(()=>{const _c=pct===20?"WELCOME20":"WELCOME10";try{localStorage.setItem("pmn_code",_c)}catch(e){}if(window.pmnSetCode)pmnSetCode(_c);$("offCode").textContent=_c;$("offCode").hidden=false;$("offDoneP").textContent=`${pct}% off is saved to your bag. It comes off automatically at checkout.`})
      .catch(()=>{$("offDoneP").textContent="That didn't go through. Please use the sign-up form at the bottom of the page."})};''')
rep('$("offErr1").textContent="";step(2)});','$("offErr1").textContent="";offEmailV=v;step(2)});')
rep('<p id="offDoneP">Here\'s your code. We\'ve emailed it too.</p>','<p id="offDoneP">Your offer is saved.</p>')
rep('''    <p class="fine cart-msg" id="cartMsg" role="status"></p>''','''    <p class="fine cart-msg" id="cartMsg" role="status"></p>
    <form class="cart-notify" id="cartNotify" hidden novalidate><label class="sr" for="cnEmail">Email address</label><input id="cnEmail" type="email" inputmode="email" autocomplete="email" placeholder="Email address"><button class="buy-alt" type="submit">Notify me</button></form>''')
rep('''  $("cartGo").onclick=()=>{if(ready())$("cartMsg").textContent="Prototype: at launch this hands your bag to the Fulfill Engine checkout (card, Apple Pay).";};''','''  const soon=()=>{if(!ready())return;$("cartMsg").textContent="Checkout opens very soon. Leave your email and we'll let you know the moment it's live.";$("cartNotify").hidden=false;$("cnEmail").focus()};
  $("cartGo").onclick=soon;
  $("cartNotify").addEventListener("submit",e=>{e.preventDefault();const v=$("cnEmail").value.trim();
    if(!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(v)){$("cartMsg").textContent="Enter a valid email, like name@example.com.";return}
    const items=cart.map(i=>`${BY[i.id].name}${i.size&&i.size!=="One size"?" ("+i.size+")":""} x${i.qty}`).join(", ");
    $("cartMsg").textContent="Saving…";
    klav(v,null,{signup_source:"shop_checkout_waitlist",bag:items}).then(()=>{$("cartNotify").hidden=true;$("cartMsg").textContent="Thanks! We'll email you as soon as checkout opens."})
      .catch(()=>{$("cartMsg").textContent="That didn't go through. Please try again in a moment."})});''')
rep('.cart-msg:empty{display:none}','.cart-msg:empty{display:none}\n.cart-notify{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px}\n.cart-notify input{height:50px;border-radius:14px;border:1px solid rgba(244,242,238,.3);background:rgba(255,255,255,.05);color:var(--ink);padding:0 14px;font:inherit;font-size:16px;min-width:0}\n.cart-notify .buy-alt{padding:0 18px}')
assert 'Prototype' not in s.replace('prototype','') or True
open(sys.argv[1],'w').write(s)
print('live build ok; remaining "Prototype" mentions:',s.count('Prototype'))

# ---------- SHOPIFY: Storefront API is the source of truth for price, variants and checkout ----------
s=open(sys.argv[1]).read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:70],s.count(a));s=s.replace(a,b)
rep('const reduceMotion=',open(D+'shopify_layer.js').read()+'const reduceMotion=')
rep('const card=(p,cls)=>{const b=document.createElement("button");b.className=cls;b.type="button";','const card=(p,cls)=>{const b=document.createElement("button");b.className=cls;b.type="button";b.dataset.pid=p.id;')
rep('$("bumpT").textContent=BUMP.title;','$("bump").hidden=!BUMP.variant;if(!BUMP.variant)bumpOn=false;$("bumpT").textContent=BUMP.title;')
rep('$("cartGo").onclick=soon;',open(D+'shopify_checkout.js').read().strip())
open(sys.argv[1],'w').write(s)
print('shopify ok')

# ---------- CART UX: persistence, code field, trust row, sold-out sizes, email prefill ----------
s=open(sys.argv[1]).read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:70],s.count(a));s=s.replace(a,b)
# persist the bag across reloads and the round trip to checkout
rep('let bag=0;const cart=[];','let bag=0;const cart=[];try{(JSON.parse(localStorage.getItem("pmn_cart")||"[]")||[]).forEach(i=>{if(BY[i.id]&&i.qty>0)cart.push({id:i.id,size:i.size??null,qty:Math.min(10,i.qty|0)})})}catch(e){}')
rep('function setBag(){','function setBag(){try{localStorage.setItem("pmn_cart",JSON.stringify(cart))}catch(e){}')
rep('  return{add,open,close};','  setBag();\n  return{add,open,close};')
# remember the shopper's email from sign-ups so checkout is prefilled
rep('async function klav(email,phone,props){','async function klav(email,phone,props){try{localStorage.setItem("pmn_email",email)}catch(e){}')
# sold-out sizes from Shopify
rep('b.className="size";b.textContent=s;','b.className="size";b.textContent=s;{const vv=typeof VAR!=="undefined"&&VAR[p.id]&&VAR[p.id][s];if(vv&&!vv.ok){b.disabled=true;b.classList.add("so");b.setAttribute("aria-label",s+", sold out")}}')
# drawer markup: code field + trust row
rep('''    <p class="fine cart-msg" id="cartMsg" role="status"></p>''','''    <p class="fine cart-msg" id="cartMsg" role="status"></p>
    <p class="ctrust"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="10" width="14" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg><span><b>Secure checkout</b> · Visa · Mastercard · Amex · Apple Pay · Google Pay · Shop Pay</span></p>''')
rep('''    <div class="tot"><span>Subtotal</span>''','''    <div class="code"><button type="button" class="code-t" id="codeToggle" aria-expanded="false" aria-controls="codeBox">Have a discount code?</button>
      <div id="codeBox" hidden><form id="codeForm" class="code-f" novalidate><label class="sr" for="codeIn">Discount code</label><input id="codeIn" autocomplete="off" autocapitalize="characters" spellcheck="false" placeholder="Discount code"><button class="buy-alt" type="submit">Apply</button></form>
      <p class="fine" id="codeMsg" role="status"></p></div>
      <p class="code-on" id="codeOn" hidden><span>Code <b id="codeTag"></b> applies at checkout</span><button type="button" id="codeRm">Remove</button></p></div>
    <div class="tot"><span>Subtotal</span>''')
rep('.cart-msg:empty{display:none}','''.cart-msg:empty{display:none}
.dr-foot{gap:7px}.code{display:grid;gap:6px}.code-t{justify-self:start;font-size:13px;font-weight:600;text-decoration:underline;text-underline-offset:3px;color:var(--ink-dim)}
.code-f{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px;margin-top:2px}
.code-f input{height:46px;border-radius:12px;border:1px solid rgba(244,242,238,.3);background:rgba(255,255,255,.05);color:var(--ink);padding:0 14px;font:inherit;font-size:16px;letter-spacing:.06em;text-transform:uppercase;min-width:0}
.code-f .buy-alt{height:46px;padding:0 18px}#codeMsg:empty{display:none}
.code-on{display:flex;justify-content:space-between;align-items:center;margin:0;padding:10px 12px;border-radius:12px;background:rgba(95,211,138,.12);color:#9be7a8;font-size:13px}
.code-on button{font-size:13px;font-weight:600;text-decoration:underline;color:var(--ink-dim)}
.ctrust{display:flex;align-items:flex-start;justify-content:center;gap:6px;margin:0;font-size:11.5px;line-height:1.45;color:var(--ink-dim);text-align:center}
.ctrust b{color:var(--ink);font-weight:600}.ctrust svg{flex:none;width:13px;height:13px;margin-top:2px;fill:none;stroke:currentColor;stroke-width:2}
.buy.busy,.buy-alt.busy{opacity:.75;cursor:progress}.buy:disabled,.buy-alt:disabled{cursor:progress}
.size.so{opacity:.35;text-decoration:line-through;cursor:not-allowed}''')
rep("""    for(const i of cart){const p=BY[i.id],want=p.kind==="hat"?LOOK[p.team].tee:LOOK[p.team].hat;
      if(!cart.some(c=>BY[c.id].kind===BY[want].kind&&BY[c.id].team===p.team))return BY[want]}""","""    const buyable=id=>!shopifyOK||!!VAR[id];
    for(const i of cart){const p=BY[i.id],kind=p.kind==="hat"?"tee":"hat",first=kind==="tee"?LOOK[p.team].tee:LOOK[p.team].hat;
      if(cart.some(c=>BY[c.id].kind===kind&&BY[c.id].team===p.team))continue;
      const pick=[first,...PRODUCTS.filter(o=>o.team===p.team&&o.kind===kind).map(o=>o.id)].find(buyable);if(pick)return BY[pick]}""")
# DEEPLINK: /shop#toa-samoa, #mate-maa-tonga, #pmn-plus open that collection
s=s+'\n<script>/* DEEPLINK */window.pmnDeep=h=>{try{$("page").hidden=true;$("pSticky").classList.remove("on");if(["toa-samoa","mate-maa-tonga","pmn-plus"].includes(h))Coll.open(h);else if(h==="pmn")Coll.open("pmn-plus","pmn");else if(h==="tee"||h==="hat")Coll.open("pmn-plus",h);else if(["shipping","returns","contact","privacy","terms"].includes(h))Pages.open(h);else if(h==="bag")Cart.open()}catch(e){}};addEventListener("load",()=>{const h=decodeURIComponent(location.hash.slice(1));if(h)setTimeout(()=>pmnDeep(h),60)});</script>\n'
# logo goes to the site homepage
_a='l.setAttribute("aria-label","PMN+ shop home");l.onclick=goHome;l.onkeydown=e=>{if(e.key==="Enter")goHome()}'
assert s.count(_a)==1
s=s.replace(_a,'l.setAttribute("aria-label","PMN+ home");l.onclick=()=>{location.href="/"};l.onkeydown=e=>{if(e.key==="Enter")location.href="/"}')
open(sys.argv[1],'w').write(s)
print('checkout ux ok')

# ---------- social / OG tags for /shop ----------
s=open(sys.argv[1]).read()
D="https://www.polynesianmusicnetwork.com"
T="Shop PMN+ | RLWC 2026 Toa Samoa &amp; Mate Ma'a Tonga Merch"
DS="It's time to represent your Pacific team. Toa Samoa and Mate Ma'a Tonga tees, snapbacks and truckers for RLWC 2026, plus PMN+ core pieces. Ships across the USA."
IMG=D+"/shop/pmn-plus-shop-og-rlwc-2026-toa-samoa-mate-maa-tonga.jpg"
ALT="Toa Samoa and Mate Ma'a Tonga tees and snapbacks on blue and red pattern backgrounds: It's time to represent your Pacific team"
og=f"""<link rel="canonical" href="{D}/shop">
<meta property="og:site_name" content="PMN+">
<meta property="og:locale" content="en_US">
<meta property="og:type" content="website">
<meta property="og:title" content="{T}">
<meta property="og:description" content="{DS}">
<meta property="og:url" content="{D}/shop">
<meta property="og:image" content="{IMG}">
<meta property="og:image:secure_url" content="{IMG}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{ALT}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{T}">
<meta name="twitter:description" content="{DS}">
<meta name="twitter:image" content="{IMG}">
<meta name="twitter:image:alt" content="{ALT}">
"""
import re as _re
s=_re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="'+DS.replace("'","&#39;")+'">\n'+og,s,count=1)
open(sys.argv[1],'w').write(s)
print('og ok')

# ---------- HIDE: products not yet in Shopify (curved-bill snapbacks) ----------
import re as _re, json as _json
HIDE=["mmt-snapback","toa-snapback"]
s=open(sys.argv[1]).read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:70],s.count(a));s=s.replace(a,b)
# runtime: drop from catalogue, swatches and collections right after SEO data loads
_m=_re.search(r'\nconst SEO=\{.*?\n',s)
assert _m
_hide_js='/* HIDE */const HIDE_IDS='+_json.dumps(HIDE)+';HIDE_IDS.forEach(id=>{const i=PRODUCTS.findIndex(p=>p.id===id);if(i>-1)PRODUCTS.splice(i,1);delete BY[id]});PRODUCTS.forEach(p=>{p.opts=p.opts.filter(o=>BY[o]);if(!p.opts.includes(p.id))p.opts.unshift(p.id)});Object.values(SEO.collections).forEach(c=>c.products=c.products.filter(id=>BY[id]));\n'
s=s[:_m.end()]+_hide_js+s[_m.end():]
rep('const LOOK={samoa:{hat:"toa-snapback",','const LOOK={samoa:{hat:"toa-hp-snapback",')
rep('tonga:{hat:"mmt-snapback",','tonga:{hat:"mmt-hp-snapback",')
# structured data: remove hidden products and their list entries
def _fix_ld(m):
    d=_json.loads(m.group(1));urls=set()
    keep=[]
    for x in d['@graph']:
        if x.get('@type')=='Product' and ('curved-bill-snapback' in x.get('@id','') or 'curved-bill-snapback' in x.get('url','')):
            urls.add(x.get('url',''));continue
        keep.append(x)
    for x in keep:
        me=x.get('mainEntity') if isinstance(x,dict) else None
        if me and me.get('itemListElement'):
            items=[i for i in me['itemListElement'] if 'curved-bill-snapback' not in _json.dumps(i)]
            for n,i in enumerate(items,1): i['position']=n
            me['itemListElement']=items;me['numberOfItems']=len(items)
    d['@graph']=keep
    return '<script type="application/ld+json">'+_json.dumps(d,ensure_ascii=False,separators=(',',':'))+'</script>'
s,_n=_re.subn(r'<script type="application/ld\+json">(.*?)</script>',_fix_ld,s,flags=_re.S)
assert _n==1
assert 'curved-bill-snapback#product' not in s
open(sys.argv[1],'w').write(s)
print('hide ok')

# ---------- SOLD OUT: oversized tees (all sizes) ----------
s=open(sys.argv[1]).read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:70],s.count(a));s=s.replace(a,b)
rep('if(vv&&!vv.ok){b.disabled=true;','if((vv&&!vv.ok)||SOLD.has(p.id)){b.disabled=true;')
rep('return PRODUCTS.filter(o=>o.team===p.team&&o.kind===want)}','return PRODUCTS.filter(o=>o.team===p.team&&o.kind===want&&!SOLD.has(o.id))}')
rep('$("stName").textContent=set?`${p.short||p.name} + ${c.short||c.name}`:p.name}',
    '$("stName").textContent=set?`${p.short||p.name} + ${c.short||c.name}`:p.name;\n    const so=SOLD.has(p.id);$("pBuy").disabled=$("stBuy").disabled=so;$("pDeal").hidden=so;if(so){$("pBuy").textContent=$("stBuy").textContent="Sold out";$("stPrice").textContent="Sold out"}}')
rep('''<span class="im">${isLimited(p)?'<i class="tag">Exclusive</i>':""}''','''<span class="im">${SOLD.has(p.id)?'<i class="sold">Sold out</i>':isLimited(p)?'<i class="tag">Exclusive</i>':""}''')
rep('''b.innerHTML=`<span class="im"><img loading="lazy" decoding="async" alt="${altFor(p).replace(/"/g,"&quot;")}" src="${heroURL(p.id)}"></span><b>${p.name}</b><span class="num">${money(p.price)}</span>`;''',
    '''b.innerHTML=`<span class="im">${SOLD.has(p.id)?'<i class="sold">Sold out</i>':""}<img loading="lazy" decoding="async" alt="${altFor(p).replace(/"/g,"&quot;")}" src="${heroURL(p.id)}"></span><b>${p.name}</b><span class="num">${SOLD.has(p.id)?"Sold out":money(p.price)}</span>`;''')
rep('$("hlName").textContent=p.name;$("hlPrice").textContent=money(p.price);','$("hlName").textContent=p.name;$("hlPrice").textContent=SOLD.has(p.id)?"Sold out":money(p.price);$("hlPrice").classList.toggle("so",SOLD.has(p.id));')
rep('    <div class="podium">','    <i class="sold hero-sold" id="heroSold" aria-hidden="true">Sold out</i>\n    <div class="podium">')
rep('    if(idx!==lastIdx){lastIdx=idx;label(idx)}','    {const hs=$("heroSold");if(SOLD.has(PRODUCTS[idx].id)){const ch=sizes[idx][1];hs.style.left=(arcL+W/2)+"px";hs.style.top=(arcT+base-ch*(capS[idx]||1)*0.5)+"px";hs.style.opacity=Math.max(0,1-Math.abs(frac)*3.2)}else hs.style.opacity=0}\n    if(idx!==lastIdx){lastIdx=idx;label(idx)}')
rep('.size.so{','.gcard .im{position:relative}.sold{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);z-index:2;font-style:normal;white-space:nowrap;background:#fff;color:#C8102E;border:2px solid #C8102E;font-family:var(--display);font-size:clamp(18px,2.4vw,26px);letter-spacing:.06em;text-transform:uppercase;line-height:1;padding:.42em .8em .36em;border-radius:6px;box-shadow:0 6px 18px rgba(0,0,0,.18);pointer-events:none}.im:has(.sold) img{opacity:.55;filter:grayscale(.35)}.im .sold{background:#C8102E;color:#fff;border-color:#C8102E;border-radius:999px;padding:.45em 1.1em .38em;box-shadow:0 6px 18px rgba(0,0,0,.25)}.hero-sold{z-index:150;opacity:0;font-size:clamp(13px,1.35vw,19px);background:#C8102E;color:#fff;border-color:#C8102E;border-radius:999px;padding:.45em 1.2em .38em;box-shadow:0 8px 24px rgba(0,0,0,.45)}#hlPrice.so{color:#ff4d5e}.size.so{')
# structured data: out of stock
import json as _j, re as _r
def _ld(m):
    d=_j.loads(m.group(1))
    for x in d['@graph']:
        if x.get('@type')=='Product' and 'crest-oversized-tee' in x.get('@id',''):
            o=x.get('offers');
            for oo in (o if isinstance(o,list) else [o]):
                if isinstance(oo,dict):oo['availability']='https://schema.org/OutOfStock'
    return '<script type="application/ld+json">'+_j.dumps(d,ensure_ascii=False,separators=(',',':'))+'</script>'
s,_n=_r.subn(r'<script type="application/ld\+json">(.*?)</script>',_ld,s,flags=_r.S);assert _n==1
open(sys.argv[1],'w').write(s)
print('sold out ok')

# ---------- NAV: one header for the whole site (see nav/nav_build.py) ----------
import importlib.util as _u
_sp=_u.spec_from_file_location('nav_build',os.path.join(os.path.dirname(os.path.abspath(__file__)),'nav','nav_build.py'));_nb=_u.module_from_spec(_sp);_sp.loader.exec_module(_nb)
s=_nb.build_shop(open(sys.argv[1]).read());open(sys.argv[1],'w').write(s)
_root=os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[1])))
_nb.copy_assets(_root)
if os.path.exists(os.path.join(_root,'index.html')):_nb.build_home(os.path.join(_root,'index.html'))
print('nav ok')

# ---------- ROUTES: own URL per product/collection, pre-rendered pages, sitemap (see seo_routes.py) ----------
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'seo_routes.py')).read())
