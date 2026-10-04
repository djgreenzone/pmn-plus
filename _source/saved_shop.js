/* Saved items in the shop: heart on every product card + on the product page (uses window.pmnSaved from pmn-nav.js) */
function svAttrs(el,p){el.dataset.saveRef=p.id;el.dataset.saveKind="product";el.dataset.saveTitle=p.name+(p.colourName?" – "+p.colourName:"");
  el.dataset.saveImage=new URL(heroURL(p.id),location.href).href;el.dataset.saveUrl=(typeof pmnURL==="function"?pmnURL(p.id):"/shop")}
function svDecorate(){document.querySelectorAll("button[data-id] .im, a[data-id] .im").forEach(im=>{if(im.querySelector(".sv-btn"))return;
  const card=im.closest("[data-id]"),p=BY[card.dataset.id];if(!p)return;const s=document.createElement("span");s.className="sv-btn";s.setAttribute("role","button");s.tabIndex=0;
  s.innerHTML=window.PMN_HEART||"&#9825;";svAttrs(s,p);im.style.position="relative";im.appendChild(s)});window.pmnSavedPaint&&window.pmnSavedPaint()}
function svPdp(p){const b=document.getElementById("pSave");if(!b||!p)return;if(!b.firstChild)b.innerHTML=window.PMN_HEART||"&#9825;";svAttrs(b,p);window.pmnSavedPaint&&window.pmnSavedPaint()}
new MutationObserver(()=>{clearTimeout(svDecorate._t);svDecorate._t=setTimeout(svDecorate,60)}).observe(document.documentElement,{childList:true,subtree:true});
