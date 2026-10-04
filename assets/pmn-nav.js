/* PMN+ site header behaviour (homepage + shop): menu drawer, product search, bag count.
   Built from _source/nav, copied to /assets by make_shop.py */
(()=>{
const LIVE=!!(window.PMN_CONFIG&&window.PMN_CONFIG.accountsLive);
const INI=(()=>{try{return (localStorage.getItem("pmn_initials")||"").replace(/[^A-Za-z0-9]/g,"").slice(0,2).toUpperCase()}catch(e){return ""}})();   // set by /account when signed in
const IG="https://www.instagram.com/polynesianmusic/";
const ic={
  chev:'<svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg>',
  x:'<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg>',
  bag:'<svg viewBox="0 0 24 24"><path d="M5 8h14l-1 12H6L5 8z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>',
  home:'<svg viewBox="0 0 24 24"><path d="M4 11l8-7 8 7v9h-5v-6H9v6H4z"/></svg>',
  play:'<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="3"/><path d="M10 9.5v5l4.5-2.5z"/></svg>'};
const LINKS=[["Shop","/shop"],["Toa Samoa","/shop/toa-samoa"],["Mate Ma'a Tonga","/shop/mate-maa-tonga"],["PMN+","/shop#pmn"],["Tees","/shop#tee"],["Hats","/shop#hat"]];
const onShop=()=>/^\/shop(\/|$)/.test(location.pathname);
let data=null,loading=null;
const load=()=>data?Promise.resolve(data):loading||(loading=fetch("/shop/search.json").then(r=>r.json()).then(j=>data=j).catch(()=>data=[]));
const esc=t=>String(t).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const money=n=>"$"+Number(n).toFixed(2);

/* in-shop links stay in the app (no reload); elsewhere they are normal links */
function go(e,href){
  if(e&&(e.metaKey||e.ctrlKey||e.shiftKey||e.button))return;
  const u=new URL(href,location.href);
  if(u.origin!==location.origin||!onShop()||!/^\/shop(\/|$)/.test(u.pathname))return;
  if(u.hash&&window.pmnDeep){e&&e.preventDefault();closeDrawer();window.pmnDeep(u.hash.slice(1));return}
  if(window.pmnGo){e&&e.preventDefault();closeDrawer();window.pmnGo(u.pathname)}
}

/* ---------- drawer ---------- */
let drawer,scrim,lastFocus=null;
function buildDrawer(){
  scrim=document.createElement("div");scrim.className="pn-scrim";scrim.hidden=true;
  drawer=document.createElement("nav");drawer.className="pn-drawer";drawer.id="pnDrawer";drawer.hidden=true;drawer.setAttribute("aria-label","Menu");
  drawer.innerHTML=`<div class="pn-dh">${LIVE?`<a href="/account">${INI?"My account":"Sign in / Join"} ${ic.chev}</a>`:`<b class="pn-dtitle">Menu</b>`}<button type="button" class="pn-ic pn-dx" aria-label="Close menu">${ic.x}</button></div>
  <div class="pn-db"><ul class="pn-dl">${LINKS.map(([t,h])=>`<li><a href="${h}"><span>${esc(t)}</span>${ic.chev}</a></li>`).join("")}</ul>
  <div class="pn-dsec"><b>Featured</b><div class="pn-feat" id="pnFeat"></div></div>
  <div class="pn-dsec"><b>Help</b><div class="pn-help"><a href="/about">About PMN+</a><a href="/shipping">Shipping</a><a href="/returns">Returns</a><a href="/contact">Contact</a></div></div></div>
  <div class="pn-dt"><a href="/shop" class="${onShop()?"on":""}">${ic.bag}Shop</a><a href="/" class="${location.pathname==="/"?"on":""}">${ic.home}Home</a><a href="${IG}" target="_blank" rel="noopener">${ic.play}Watch</a></div>`;
  document.body.append(scrim,drawer);
  scrim.onclick=closeDrawer;drawer.querySelector(".pn-dx").onclick=closeDrawer;
  drawer.addEventListener("click",e=>{const a=e.target.closest("a");if(a)go(e,a.getAttribute("href"))});
  drawer.addEventListener("keydown",e=>{if(e.key==="Escape")closeDrawer();
    if(e.key==="Tab"){const f=[...drawer.querySelectorAll("a,button")].filter(x=>x.offsetParent);const a=f[0],z=f[f.length-1];
      if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus()}else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus()}}});
  load().then(d=>{const pick=d.filter(p=>!p.so).slice(0,2);const f=drawer.querySelector("#pnFeat");
    f.innerHTML=pick.map(p=>`<a href="/shop/${p.s}"><img loading="lazy" src="${p.i}" alt="${esc(p.n)} in ${esc(p.c.toLowerCase())}"><span>${esc(p.n)}<small>${money(p.p)}</small></span></a>`).join("")});
}
function openDrawer(btn){if(!drawer)buildDrawer();lastFocus=btn||document.activeElement;scrim.hidden=drawer.hidden=false;document.documentElement.classList.add("pn-lock");
  document.querySelectorAll(".pn-menu").forEach(b=>b.setAttribute("aria-expanded","true"));
  requestAnimationFrame(()=>{document.documentElement.classList.add("pn-on");drawer.querySelector(".pn-dx").focus()})}
function closeDrawer(){if(!drawer||drawer.hidden)return;document.documentElement.classList.remove("pn-on","pn-lock");
  document.querySelectorAll(".pn-menu").forEach(b=>b.setAttribute("aria-expanded","false"));
  setTimeout(()=>{scrim.hidden=drawer.hidden=true},matchMedia("(prefers-reduced-motion:reduce)").matches?0:300);lastFocus&&lastFocus.focus&&lastFocus.focus()}
window.pmnMenu={open:openDrawer,close:closeDrawer};

/* ---------- search ---------- */
const norm=t=>t.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g,"").replace(/[’'`]/g,"").replace(/[^a-z0-9+]+/g," ").trim();
function search(q){const toks=norm(q).split(" ").filter(Boolean);if(!toks.length)return[];
  return data.map(p=>{const h=p.h;let sc=0;for(const t of toks){const i=h.indexOf(t);if(i<0)return null;sc+=(i===0||h[i-1]===" ")?2:1}return[sc-(p.so?1:0),p]}).filter(Boolean).sort((a,b)=>b[0]-a[0]).map(x=>x[1])}
function wireSearch(root){
  const form=root.querySelector(".pn-search"),inp=form.querySelector("input"),res=form.querySelector(".pn-res");let sel=-1,items=[];
  const close=()=>{res.hidden=true;sel=-1;inp.setAttribute("aria-expanded","false")};
  const mark=()=>res.querySelectorAll("a[data-i]").forEach((a,i)=>a.setAttribute("aria-selected",i===sel));
  function render(){const q=inp.value.trim();if(!q){close();return}
    load().then(()=>{items=search(q).slice(0,6);sel=-1;
      res.innerHTML=items.length?items.map((p,i)=>`<a data-i="${i}" role="option" href="/shop/${p.s}"><img src="${p.i}" alt=""><span><b>${esc(p.n)}</b><small>${esc(p.c)} · ${esc(p.t)}</small></span><span class="pr${p.so?" so":""}">${p.so?"Sold out":money(p.p)}</span></a>`).join("")+`<a class="pn-all" href="/shop">Shop all</a>`
        :`<div class="pn-none">No matches for “${esc(q)}”. Try “685”, “snapback” or “Tonga”, or <a href="/shop">shop everything</a>.</div>`;
      res.hidden=false;inp.setAttribute("aria-expanded","true")})}
  inp.addEventListener("focus",load);inp.addEventListener("input",render);
  inp.addEventListener("keydown",e=>{
    if(e.key==="ArrowDown"||e.key==="ArrowUp"){if(res.hidden)return;e.preventDefault();sel=(sel+(e.key==="ArrowDown"?1:-1)+items.length)%items.length;mark()}
    else if(e.key==="Escape"){close();root.classList.remove("pn-s-open");inp.blur()}});
  form.addEventListener("submit",e=>{e.preventDefault();const p=items[sel>-1?sel:0];if(!p)return;const h="/shop/"+p.s;close();inp.value="";root.classList.remove("pn-s-open");
    if(onShop()&&window.pmnGo)window.pmnGo(h);else location.href=h});
  res.addEventListener("click",e=>{const a=e.target.closest("a");if(!a)return;close();inp.value="";root.classList.remove("pn-s-open");go(e,a.getAttribute("href"))});
  document.addEventListener("click",e=>{if(!form.contains(e.target)&&!e.target.closest(".pn-sbtn")){close();root.classList.remove("pn-s-open")}});
  const sb=root.querySelector(".pn-sbtn");if(sb)sb.onclick=()=>{const on=root.classList.toggle("pn-s-open");if(on){inp.focus();load()}else close()};
}

/* ---------- mount every header on the page ---------- */
function bagCount(){let n=0;try{n=JSON.parse(localStorage.getItem("pmn_cart")||"[]").reduce((t,i)=>t+(+i.qty||0),0)}catch(e){}
  document.querySelectorAll(".pn .bag-count").forEach(b=>{if(!onShop()||!b.textContent){b.hidden=!n;b.textContent=n||""}})}
document.querySelectorAll(".pn").forEach(root=>{
  root.querySelectorAll(".pn-menu").forEach(b=>b.onclick=()=>openDrawer(b));
  wireSearch(root);
  root.querySelectorAll(".pn-cats a").forEach(a=>{a.addEventListener("click",e=>go(e,a.getAttribute("href")));
    const u=new URL(a.href);if(u.pathname===location.pathname&&!u.hash&&u.pathname!=="/shop")a.setAttribute("aria-current","page")});
});
bagCount();addEventListener("storage",bagCount);
if(LIVE)document.querySelectorAll(".pn-acct").forEach(a=>{a.hidden=false;if(INI){a.innerHTML=`<span class="pn-av">${INI}</span>`;a.setAttribute("aria-label","Your PMN+ account")}else a.setAttribute("aria-label","Sign in or join PMN+");if(location.pathname.startsWith("/account"))a.setAttribute("aria-current","page")});
addEventListener("keydown",e=>{if(e.key==="/"&&!/input|textarea|select/i.test(document.activeElement.tagName)){const i=[...document.querySelectorAll(".pn-search input")].find(x=>x.offsetParent);if(i){e.preventDefault();i.focus()}}});
})();

/* ---------- Klaviyo onsite tracking (Viewed Product, Added to Cart, identify) ----------
   Our shop is a custom site, so Klaviyo can't see browsing on its own. This loads klaviyo.js
   and sends the events the Browse Abandonment and Added to Cart flows run on. */
(()=>{
const KL_ID="T9JJzp",ORIGIN="https://www.polynesianmusicnetwork.com";
if(!window.klaviyo){window._klOnsite=window._klOnsite||[];
  window.klaviyo={push:function(){window._klOnsite.push.apply(window._klOnsite,arguments)}};}
const s=document.createElement("script");s.async=true;s.src="https://static.klaviyo.com/onsite/js/klaviyo.js?company_id="+KL_ID;document.head.appendChild(s);
const kl=(...a)=>{try{window.klaviyo.push(a)}catch(e){}};
const emit=(n,d)=>{try{window.pmnTrack&&window.pmnTrack(n,d)}catch(e){}};
const abs=u=>!u?"":/^https?:/.test(u)?u:ORIGIN+(u[0]==="/"?"":"/")+u;
const get=k=>{try{return localStorage.getItem(k)}catch(e){return null}};
const em=get("pmn_email");if(em)kl("identify",{email:em});

let cat=null;const loadCat=()=>cat?Promise.resolve(cat):fetch("/shop/search.json").then(r=>r.json()).then(j=>cat=j).catch(()=>cat=[]);
const item=p=>({ProductName:p.n+(p.c?" – "+p.c:""),ProductID:p.s,SKU:p.s,Categories:[p.t,p.k].filter(Boolean),
  ImageURL:abs(p.i),URL:ORIGIN+"/shop/"+p.s,Brand:"PMN+",Price:p.p});

/* Viewed Product: product pages and in-app product opens */
let lastView="";
function view(){const m=location.pathname.match(/^\/shop\/([a-z0-9-]+)\/?$/);if(!m)return;const slug=m[1];
  loadCat().then(c=>{const p=c.find(x=>x.s===slug);if(!p||slug===lastView)return;lastView=slug;
    const it=item(p);kl("track","Viewed Product",it);emit("view_item",{value:p.p,items:[{id:p.s,name:it.ProductName,price:p.p,category:p.t,qty:1}]});kl("trackViewedItem",{Title:it.ProductName,ItemId:it.ProductID,Categories:it.Categories,ImageUrl:it.ImageURL,Url:it.URL,Metadata:{Brand:"PMN+",Price:it.Price}})})}
["pushState","replaceState"].forEach(f=>{const o=history[f];history[f]=function(){const r=o.apply(this,arguments);setTimeout(view,0);return r}});
addEventListener("popstate",view);view();

/* Added to Cart + identify: watch what the shop saves to the bag and the sign-up email */
const qty=a=>{const m={};(a||[]).forEach(i=>{const k=i.id+"|"+(i.size??"");m[k]=(m[k]||0)+(+i.qty||0)});return m};
let before=qty((()=>{try{return JSON.parse(get("pmn_cart")||"[]")}catch(e){return[]}})());
const set=Storage.prototype.setItem;
Storage.prototype.setItem=function(k,v){set.apply(this,arguments);try{
  if(k==="pmn_email"&&v)kl("identify",{email:v});
  if(k!=="pmn_cart")return;const cart=JSON.parse(v||"[]"),now=qty(cart),prev=before;before=now;
  const added=Object.keys(now).filter(x=>now[x]>(prev[x]||0));if(!added.length)return;
  const by=typeof BY!=="undefined"?BY:{};
  loadCat().then(c=>{const find=id=>{const b=by[id];if(!b)return null;return c.find(x=>x.n===b.name&&(!b.colourName||x.c===b.colourName))||c.find(x=>x.n===b.name)};
    const lines=cart.map(i=>{const p=find(i.id),b=by[i.id]||{};return{ProductName:p?item(p).ProductName:(b.name||i.id),ProductID:p?p.s:i.id,Size:i.size||"",Quantity:+i.qty||1,
      ItemPrice:b.price||(p&&p.p)||0,RowTotal:(b.price||(p&&p.p)||0)*(+i.qty||1),ImageURL:p?abs(p.i):"",ProductURL:p?ORIGIN+"/shop/"+p.s:ORIGIN+"/shop"}});
    added.forEach(key=>{const id=key.split("|")[0],size=key.split("|")[1],p=find(id),b=by[id]||{},it=p?item(p):{ProductName:b.name||id,ProductID:id,ImageURL:"",URL:ORIGIN+"/shop",Price:b.price||0};
      emit("add_to_cart",{value:it.Price*(now[key]-(prev[key]||0)),items:[{id:it.ProductID,name:it.ProductName,price:it.Price,category:p?p.t:"",size,qty:now[key]-(prev[key]||0)}]});
      kl("track","Added to Cart",{$value:lines.reduce((n,l)=>n+l.RowTotal,0),AddedItemProductName:it.ProductName,AddedItemProductID:it.ProductID,AddedItemSize:size,
        AddedItemImageURL:it.ImageURL,AddedItemURL:it.URL,AddedItemPrice:it.Price,AddedItemQuantity:now[key]-(prev[key]||0),
        ItemNames:lines.map(l=>l.ProductName),CheckoutURL:ORIGIN+"/shop#bag",Items:lines})})})
}catch(e){}};
})();

/* ---------- Analytics + ad pixels (GA4, Meta, TikTok, Clarity) ----------
   IDs live in /assets/pmn-config.js (analytics:{ga4,meta,tiktok,clarity}); a blank ID loads nothing.
   Shop events: view_item, add_to_cart, begin_checkout. Purchases are sent by the Shopify checkout pixel. */
(()=>{
const C=Object.assign({},(window.PMN_CONFIG&&window.PMN_CONFIG.analytics)||{}),q=[];
/* "Do not sell or share": Global Privacy Control or the opt-out on /privacy-policy turns off ad pixels (Meta, TikTok) */
const optedOut=()=>{try{return navigator.globalPrivacyControl===true||localStorage.getItem("pmn_ads_optout")==="1"}catch(e){return navigator.globalPrivacyControl===true}};
if(optedOut()){C.meta="";C.tiktok=""}
window.pmnAdsOptOut=on=>{try{on?localStorage.setItem("pmn_ads_optout","1"):localStorage.removeItem("pmn_ads_optout")}catch(e){}
  if(on){try{window.fbq&&fbq("consent","revoke")}catch(e){}try{window.ttq&&ttq.disableCookie()}catch(e){}}};
window.pmnAdsOptedOut=optedOut;
const load=src=>{const s=document.createElement("script");s.async=true;s.src=src;document.head.appendChild(s)};
if(C.ga4){window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments)};gtag("js",new Date());gtag("config",C.ga4);load("https://www.googletagmanager.com/gtag/js?id="+C.ga4)}
if(C.meta){!function(f,b,e,v,n){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version="2.0";n.queue=[]}(window,document);
  load("https://connect.facebook.net/en_US/fbevents.js");fbq("init",C.meta);fbq("track","PageView")}
if(C.tiktok){!function(w,t){w.TiktokAnalyticsObject=t;const tt=w[t]=w[t]||[];tt.methods=["page","track","identify","instances","debug","on","off","once","ready","alias","group","enableCookie","disableCookie","holdConsent","revokeConsent","grantConsent"];
  tt.setAndDefer=(o,m)=>{o[m]=function(){o.push([m].concat([].slice.call(arguments,0)))}};tt.methods.forEach(m=>tt.setAndDefer(tt,m));
  tt.load=id=>{tt._i=tt._i||{};tt._i[id]=[];tt._t=tt._t||{};tt._t[id]=+new Date;tt._o=tt._o||{};load("https://analytics.tiktok.com/i18n/pixel/events.js?sdkid="+id+"&lib="+t)};tt.load(C.tiktok);tt.page()}(window,"ttq")}
if(C.clarity){!function(c,l,a,r,i){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};load("https://www.clarity.ms/tag/"+i)}(window,document,"clarity","script",C.clarity)}
/* SPA route changes on /shop (pushState) -> page views */
let path=location.pathname;const route=()=>{if(location.pathname===path)return;path=location.pathname;
  if(window.gtag)gtag("event","page_view",{page_location:location.href,page_title:document.title});if(window.fbq)fbq("track","PageView");if(window.ttq)ttq.page()};
["pushState","replaceState"].forEach(f=>{const o=history[f];history[f]=function(){const r=o.apply(this,arguments);setTimeout(route,0);return r}});addEventListener("popstate",route);
const META={view_item:"ViewContent",add_to_cart:"AddToCart",begin_checkout:"InitiateCheckout"},TT={view_item:"ViewContent",add_to_cart:"AddToCart",begin_checkout:"InitiateCheckout"};
window.pmnTrack=(name,d)=>{try{const items=d.items||[],value=+(d.value||0);
  if(window.gtag)gtag("event",name,{currency:"USD",value,items:items.map(i=>({item_id:i.id,item_name:i.name,item_brand:"PMN+",item_category:i.category||"",item_variant:i.size||"",price:i.price,quantity:i.qty||1}))});
  if(window.fbq&&META[name])fbq("track",META[name],{currency:"USD",value,content_type:"product",content_ids:items.map(i=>i.id),contents:items.map(i=>({id:i.id,quantity:i.qty||1,item_price:i.price})),num_items:items.reduce((n,i)=>n+(i.qty||1),0)});
  if(window.ttq&&TT[name])ttq.track(TT[name],{currency:"USD",value,content_type:"product",contents:items.map(i=>({content_id:i.id,content_name:i.name,quantity:i.qty||1,price:i.price}))});
  if(window.clarity)clarity("event",name)}catch(e){}};
/* IDs the checkout pixel needs to tie the purchase back to this visit */
window.pmnAttribution=()=>{const ck=n=>(document.cookie.match("(?:^|; )"+n+"=([^;]*)")||[])[1]||"";const ga=ck("_ga").split(".").slice(-2).join(".");
  return[["_ga_client_id",ga],["_fbp",ck("_fbp")],["_fbc",ck("_fbc")],["_ttp",ck("_ttp")],["_landing",(()=>{try{return sessionStorage.getItem("pmn_land")||""}catch(e){return""}})()]].filter(a=>a[1]).map(([key,value])=>({key,value}))};
try{if(!sessionStorage.getItem("pmn_land"))sessionStorage.setItem("pmn_land",location.pathname+location.search)}catch(e){}
})();

/* ---------- Saved items (heart). Works signed out (this browser) and syncs to the PMN+ account (Supabase saved_items) when signed in. ---------- */
(()=>{
const KEY="pmn_saved",C=window.PMN_CONFIG||{},SB=C.supabaseUrl,AK=C.supabaseAnonKey;
const rd=()=>{try{return JSON.parse(localStorage.getItem(KEY)||"[]")}catch(e){return[]}};
const wr=a=>{try{localStorage.setItem(KEY,JSON.stringify(a))}catch(e){}};
const tok=()=>{try{if(!SB)return null;const ref=SB.split("//")[1].split(".")[0];const s=JSON.parse(localStorage.getItem("sb-"+ref+"-auth-token")||"null");
  return s&&s.access_token&&(s.expires_at||0)*1000>Date.now()+30000?s.access_token:null}catch(e){return null}};
const api=(path,opt={})=>{const t=tok();if(!t)return Promise.resolve(null);
  return fetch(SB+"/rest/v1/"+path,Object.assign({},opt,{headers:Object.assign({apikey:AK,Authorization:"Bearer "+t,"Content-Type":"application/json"},opt.headers||{})})).then(r=>r.ok?(r.status===204?[]:r.json().catch(()=>[])):null).catch(()=>null)};
const k=(kind,ref)=>kind+":"+ref;
const subs=[];const emit=()=>{const a=rd();subs.forEach(f=>{try{f(a)}catch(e){}});paint()};
const S=window.pmnSaved={
  all:rd,
  has:(ref,kind="product")=>rd().some(x=>k(x.kind,x.ref)===k(kind,ref)),
  toggle(item){item=Object.assign({kind:"product"},item);const a=rd(),i=a.findIndex(x=>k(x.kind,x.ref)===k(item.kind,item.ref));let on;
    if(i>=0){a.splice(i,1);on=false;api(`saved_items?kind=eq.${encodeURIComponent(item.kind)}&ref=eq.${encodeURIComponent(item.ref)}`,{method:"DELETE"})}
    else{const it={kind:item.kind,ref:String(item.ref),title:item.title||"",image:item.image||"",url:item.url||"",t:Date.now()};a.unshift(it);on=true;
      api("saved_items?on_conflict=user_id,kind,ref",{method:"POST",headers:{Prefer:"resolution=ignore-duplicates,return=minimal"},body:JSON.stringify([{kind:it.kind,ref:it.ref,title:it.title,image:it.image,url:it.url}])});
      try{window.pmnTrack&&window.pmnTrack("add_to_wishlist",{items:[{id:it.ref,name:it.title}]})}catch(e){}}
    wr(a);emit();return on},
  remove(ref,kind="product"){if(S.has(ref,kind))S.toggle({ref,kind})},
  onChange(f){subs.push(f)},
  /* merge this browser's saves with the account: called by /account after sign-in */
  async sync(){const srv=await api("saved_items?select=kind,ref,title,image,url,created_at&order=created_at.desc");if(!srv)return rd();
    const loc=rd(),have=new Set(srv.map(x=>k(x.kind,x.ref)));const up=loc.filter(x=>!have.has(k(x.kind,x.ref)));
    if(up.length)await api("saved_items?on_conflict=user_id,kind,ref",{method:"POST",headers:{Prefer:"resolution=ignore-duplicates,return=minimal"},body:JSON.stringify(up.map(x=>({kind:x.kind,ref:x.ref,title:x.title,image:x.image,url:x.url})))});
    const m=new Map();[...srv.map(x=>Object.assign({t:Date.parse(x.created_at)||0},x)),...loc].forEach(x=>{const kk=k(x.kind,x.ref);if(!m.has(kk))m.set(kk,x)});
    const out=[...m.values()].sort((a,b)=>(b.t||0)-(a.t||0));wr(out);emit();return out}
};
/* header heart: shows once something is saved */
const HEART='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20.5s-7.5-4.6-9.2-9.3C1.6 7.9 3.8 4.5 7.2 4.5c2 0 3.6 1.1 4.8 2.8 1.2-1.7 2.8-2.8 4.8-2.8 3.4 0 5.6 3.4 4.4 6.7-1.7 4.7-9.2 9.3-9.2 9.3z"/></svg>';
window.PMN_HEART=HEART;
function paint(){const n=rd().filter(x=>x.kind==="product").length;
  document.querySelectorAll(".pn-r").forEach(r=>{let a=r.querySelector(".pn-saved");
    if(!a){a=document.createElement("a");a.className="pn-ic pn-saved";a.href="/account#saved";a.innerHTML=HEART+'<span class="pn-sn"></span>';const ac=r.querySelector(".pn-acct");r.insertBefore(a,ac||r.lastChild)}
    a.hidden=!n;a.setAttribute("aria-label",`Saved items (${n})`);a.querySelector(".pn-sn").textContent=n>9?"9+":n||""});
  document.querySelectorAll("[data-save-ref]").forEach(b=>{const on=S.has(b.dataset.saveRef,b.dataset.saveKind||"product");b.classList.toggle("on",on);b.setAttribute("aria-pressed",on);b.setAttribute("aria-label",(on?"Remove from saved: ":"Save: ")+(b.dataset.saveTitle||"item"))})}
/* any element with data-save-ref becomes a save toggle (works inside product-card buttons too) */
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("[data-save-ref]");if(!b)return;e.preventDefault();e.stopPropagation();
  const on=S.toggle({kind:b.dataset.saveKind||"product",ref:b.dataset.saveRef,title:b.dataset.saveTitle,image:b.dataset.saveImage,url:b.dataset.saveUrl});
  b.classList.remove("pop");void b.offsetWidth;b.classList.add("pop");
  const t=document.getElementById("pnSaveToast")||Object.assign(document.createElement("div"),{id:"pnSaveToast",className:"pn-stoast"});t.setAttribute("role","status");document.body.appendChild(t);
  t.innerHTML=on?`Saved. <a href="/account#saved">View saved</a>`:"Removed from saved.";t.classList.add("on");clearTimeout(t._h);t._h=setTimeout(()=>t.classList.remove("on"),2600)},true);
document.addEventListener("keydown",e=>{if((e.key==="Enter"||e.key===" ")&&e.target.matches&&e.target.matches("span[data-save-ref]")){e.preventDefault();e.target.click()}},true);
addEventListener("storage",e=>{if(e.key===KEY)emit()});
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",paint);else paint();
window.pmnSavedPaint=paint;
})();
