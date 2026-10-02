/* Shopify Storefront API (public token: read-only + cart, safe in the browser). Shopify wins on price. */
const SHOPIFY={domain:"polynesianmusicnetwork.myshopify.com",token:"ac4ace2c0dde0ff361595f32f36beb6f",api:"2025-07"};
/* site product id -> [Shopify handle, Color option value (null = only one colour)] */
const SHOPIFY_MAP={
  "mmt-oversized":["mmt-samoa-crest-oversized-tee","Black"],"toa-oversized":["toa-samoa-crest-oversized-tee","Black"],
  "mmt-676-black":["mmt-676-tee-shirt","Black"],"mmt-676-tee":["mmt-676-tee","Red"],
  "toa-685-black":["toa-samoa-685-tee-shirt","Black"],"toa-685-tee":["toa-samoa-685-tee-shirt","Bright Royal"],
  "mmt-silver-blackout":["mmt-silver-blackout-tee","Black"],"toa-silver-blackout":["toa-samoa-silver-blackout-tee","Black"],
  "mmt-trucker":["tonga-trucker-snapback",null],"toa-trucker":["samoa-trucker-snapback",null],
  "pmn-tee":["pmn-classic-tee","Black"],"pmn-trucker":["pmn-retro-trucker-hat-blk",null],"pmn-dad-hat":["pmn-classic-dad-hat-khaki",null],
  "mmt-hp-snapback":["toa-samoa-snapback-red-wht",null],"toa-hp-snapback":["toa-samoa-snapback-nvy-wht",null]
  /* add when published: mmt-snapback, toa-snapback (curved bill) */
};
/* sold out on the site regardless of Shopify stock */
var SOLD=new Set(["mmt-oversized","toa-oversized"]);
const SHOPIFY_BUMP_HANDLE="sticker-pack";
const VAR={};let shopifyOK=false;
async function sf(query,variables){
  const r=await fetch(`https://${SHOPIFY.domain}/api/${SHOPIFY.api}/graphql.json`,{method:"POST",headers:{"Content-Type":"application/json","X-Shopify-Storefront-Access-Token":SHOPIFY.token},body:JSON.stringify({query,variables})});
  const j=await r.json();if(j.errors)throw new Error(j.errors[0].message);return j.data}
const shopifyReady=(async()=>{try{
  const d=await sf(`{products(first:100){nodes{handle variants(first:60){nodes{id availableForSale price{amount} selectedOptions{name value}}}}}}`);
  const H={};d.products.nodes.forEach(p=>H[p.handle]=p);const norm=v=>String(v||"").replace(/\s+/g,"").toLowerCase();let changed=false;
  for(const [id,[h,col]] of Object.entries(SHOPIFY_MAP)){const sp=H[h],p=BY[id];if(!sp||!p)continue;
    const vs=sp.variants.nodes.filter(v=>{if(!col)return true;const c=v.selectedOptions.find(o=>/colou?r/i.test(o.name));return !c||norm(c.value)===norm(col)});
    if(!vs.length)continue;const m={};
    vs.forEach(v=>{const z=v.selectedOptions.find(o=>/size/i.test(o.name));m[z?z.value.trim():"One size"]={id:v.id,ok:v.availableForSale}});
    VAR[id]=m;const pr=Math.min(...vs.map(v=>+v.price.amount));if(pr&&pr!==p.price){p.price=pr;changed=true}}
  const b=H[SHOPIFY_BUMP_HANDLE];if(b&&b.variants.nodes[0]){BUMP.variant=b.variants.nodes[0].id;BUMP.price=+b.variants.nodes[0].price.amount}
  SOLD.forEach(id=>{if(VAR[id])Object.values(VAR[id]).forEach(v=>v.ok=false)});
  shopifyOK=true;
  if(changed)document.querySelectorAll("[data-pid]").forEach(el=>{const p=BY[el.dataset.pid],pr=el.querySelector(".pr");if(p&&pr)pr.textContent=money(p.price)});
}catch(e){console.warn("Shopify",e)}})();
