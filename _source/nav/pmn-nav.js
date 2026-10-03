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
const LINKS=[["Shop all","/shop"],["Toa Samoa","/shop/toa-samoa"],["Mate Ma'a Tonga","/shop/mate-maa-tonga"],["PMN+","/shop#pmn"],["Tees","/shop#tee"],["Hats","/shop#hat"]];
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
  <div class="pn-dsec"><b>Help</b><div class="pn-help"><a href="/about">About PMN+</a><a href="/shop#shipping">Shipping</a><a href="/shop#returns">Returns &amp; exchanges</a><a href="/shop#contact">Contact</a></div></div></div>
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
    const it=item(p);kl("track","Viewed Product",it);kl("trackViewedItem",{Title:it.ProductName,ItemId:it.ProductID,Categories:it.Categories,ImageUrl:it.ImageURL,Url:it.URL,Metadata:{Brand:"PMN+",Price:it.Price}})})}
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
      kl("track","Added to Cart",{$value:lines.reduce((n,l)=>n+l.RowTotal,0),AddedItemProductName:it.ProductName,AddedItemProductID:it.ProductID,AddedItemSize:size,
        AddedItemImageURL:it.ImageURL,AddedItemURL:it.URL,AddedItemPrice:it.Price,AddedItemQuantity:now[key]-(prev[key]||0),
        ItemNames:lines.map(l=>l.ProductName),CheckoutURL:ORIGIN+"/shop#bag",Items:lines})})})
}catch(e){}};
})();
