/* Klaviyo Reviews: star rating under the product name + full reviews in the Reviews panel.
   data-id = Shopify product ID (Klaviyo catalog is synced from Shopify). klaviyo.js loads in pmn-nav.js. */
const KL_PID={"mmt-samoa-crest-oversized-tee":15382958342343,"toa-samoa-crest-oversized-tee":15382957359303,
  "mmt-676-tee-shirt":15382959227079,"mmt-676-tee":15382961225927,"toa-samoa-685-tee-shirt":15382961651911,
  "mmt-silver-blackout-tee":15382961914055,"toa-samoa-silver-blackout-tee":15382962143431,
  "tonga-trucker-snapback":15382965911751,"samoa-trucker-snapback":15382966141127,"pmn-classic-tee":15382962929863,
  "pmn-retro-trucker-hat-blk":15382967091399,"pmn-classic-dad-hat-khaki":15382966862023,
  "toa-samoa-snapback-red-wht":15382968565959,"toa-samoa-snapback-nvy-wht":15382983803079};
function klReviews(p){
  const m=SHOPIFY_MAP[p.id],pid=m&&KL_PID[m[0]],st=document.getElementById("pStars"),box=document.getElementById("pRevBox");
  if(!st||!box)return;
  if(!pid){st.innerHTML="";box.innerHTML='<p class="rev-none">No reviews yet.</p>';return}
  if(st.dataset.pid==String(pid))return;st.dataset.pid=pid;
  const t=(p.kind==="hat"||/hat|snapback|trucker/i.test(p.name))?"Hats":"T-Shirts";
  const esc=v=>String(v).replace(/&/g,"&amp;").replace(/"/g,"&quot;");
  st.innerHTML=`<div class="klaviyo-star-rating-widget" data-id="${pid}" data-product-title="${esc(p.name)}" data-product-type="${t}"></div>`;
  box.innerHTML=`<div id="klaviyo-reviews-all" data-id="${pid}"></div>`;
}
/* Review-request deep link from Klaviyo email: /shop/?review=<Shopify product ID>
   opens that product, expands the Reviews panel and scrolls to it. */
addEventListener("load",()=>setTimeout(()=>{try{
  const q=new URLSearchParams(location.search).get("review");if(!q)return;
  const id=Object.keys(SHOPIFY_MAP).find(k=>String(KL_PID[SHOPIFY_MAP[k][0]])===q);if(!id)return;
  if($("pdp").hidden||PDP.current()!==id){const im=new Image();im.src=heroURL(id);PDP.open(id,im,"home")}
  const go=()=>{const d=document.getElementById("pRevAcc");if(!d)return;d.open=true;d.scrollIntoView({behavior:"smooth",block:"start"});
    const w=document.querySelector("#pRevBox button, #pRevBox [class*='write' i]");if(w&&/write/i.test(w.textContent||""))w.click()};
  setTimeout(go,900);setTimeout(go,2500);
}catch(e){console.warn("review link",e)}},300));
