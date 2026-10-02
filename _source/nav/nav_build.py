# One header for the whole site (homepage + every shop view). Run by make_shop.py.
# - writes the header markup into each shop view and into the homepage (between the <header id="nav"> tags)
# - copies pmn-nav.css / pmn-nav.js to /assets
import os, re, shutil
NAVDIR=os.path.dirname(os.path.abspath(__file__))
ACCOUNT="https://shopify.com/81450303687/account"
SV=lambda d:f'<svg viewBox="0 0 24 24" aria-hidden="true">{d}</svg>'
I_MENU=SV('<path d="M4 7h16M4 12h16M4 17h16"/>')
I_SEARCH=SV('<circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/>')
I_USER=SV('<circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/>')
I_BAG=SV('<path d="M5 8h14l-1 12H6L5 8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>')
I_BACK='<svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg>'
CATS=[("Shop all","/shop"),("Toa Samoa","/shop/toa-samoa"),("Mate Ma'a Tonga","/shop/mate-maa-tonga"),("PMN+","/shop#pmn"),("Tees","/shop#tee"),("Hats","/shop#hat")]
def header(back_id=None,back_label="Back",bag="button",extra=""):
    back=f'<button type="button" class="pn-ic icon-btn" id="{back_id}" aria-label="{back_label}">{I_BACK}</button>' if back_id else ''
    bagel=(f'<button type="button" class="pn-ic icon-btn bag" aria-label="Bag">{I_BAG}<span class="bag-count" hidden></span></button>' if bag=="button"
           else f'<a class="pn-ic bag" href="/shop#bag" aria-label="Bag">{I_BAG}<span class="bag-count" id="bagN" hidden></span></a>')
    cats=''.join(f'<a href="{h}">{t}</a>' for t,h in CATS)
    return (f'<div class="pn"><div class="pn-row">'
      f'<div class="pn-l">{back}<button type="button" class="pn-ic pn-menu" aria-label="Open menu" aria-expanded="false" aria-controls="pnDrawer">{I_MENU}</button></div>'
      f'<a class="pn-logo" href="/" aria-label="PMN+ home"><img class="logo" src="/shop/brand/pmn-plus-logo-white.svg" alt="PMN+ Polynesian Music Network Plus" width="48" height="52"></a>'
      f'<div class="pn-r"><form class="pn-search" role="search" action="/shop"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>'
      f'<input type="search" name="q" placeholder="Search tees, hats, teams…" aria-label="Search the shop" autocomplete="off" role="combobox" aria-expanded="false" aria-autocomplete="list"><div class="pn-res" role="listbox" hidden></div></form>'
      f'<button type="button" class="pn-ic pn-sbtn" aria-label="Search">{I_SEARCH}</button>'
      f'{bagel}</div></div>'  # account icon: add back when PMN+ accounts are built
      f'<nav class="pn-cats" aria-label="Shop categories">{cats}</nav>{extra}</div>')

def build_shop(s):
    """replace the four shop view headers"""
    views=[(None,"Back",'<button type="button" id="heroShop" hidden>Shop</button>'),("pdpBack","Back to the drop",""),("collBack","Back to the drop",""),("pageBack","Back","")]
    out=[];pos=0;n=0
    for m in re.finditer(r'<header class="bar( reveal)?">(.*?)</header>',s,re.S):
        inner=m.group(2)
        bid=re.search(r'id="(pdpBack|collBack|pageBack)"',inner)
        v=next(v for v in views if v[0]==(bid.group(1) if bid else None))
        out.append(s[pos:m.start()]+f'<header class="bar pn-bar{m.group(1) or ""}">'+header(v[0],v[1],"button",v[2])+'</header>');pos=m.end();n+=1
    assert n==4,n
    s=''.join(out)+s[pos:]
    i=s.index('<style>');s=s[:i]+'<link rel="stylesheet" href="/assets/pmn-nav.css">\n'+s[i:]
    a='<script>\n/* ---------- Product data';assert s.count(a)==1
    s=s.replace(a,'<script src="/assets/pmn-nav.js"></script>\n'+a)
    return s

def build_home(path):
    h=open(path).read()
    i=h.index('<header class="nav');j=h.index('</header>',i)+9
    h=h[:i]+'<header class="nav pn-bar" id="nav">'+header(bag="link")+'</header>'+h[j:]
    if '/assets/pmn-nav.css' not in h: h=h.replace('</head>','<link rel="stylesheet" href="/assets/pmn-nav.css">\n</head>',1)
    if '/assets/pmn-nav.js' not in h: h=h.replace('</body>','<script src="/assets/pmn-nav.js"></script>\n</body>',1)
    # old homepage header styles (superseded by pmn-nav.css)
    h=re.sub(r'\n(?:\.nav \.mark|\.nav nav|\.nav \.bag|@media \(min-width:900px\)\{\.nav nav)[^\n]*','',h)
    h=h.replace('.nav{position:fixed;inset:0 0 auto;z-index:20;display:flex;align-items:center;justify-content:space-between;padding:.85rem clamp(1rem,5vw,2.5rem);background:linear-gradient(180deg,rgba(0,0,0,.75),rgba(0,0,0,0));transition:background .25s}','.nav{position:fixed;inset:0 0 auto;z-index:20}')
    h=h.replace('<section class="ig" aria-labelledby="igH">','<section class="ig" id="reels" aria-labelledby="igH">')
    open(path,'w').write(h)

def copy_assets(root):
    os.makedirs(os.path.join(root,'assets'),exist_ok=True)
    for f in ('pmn-nav.css','pmn-nav.js'): shutil.copyfile(os.path.join(NAVDIR,f),os.path.join(root,'assets',f))
