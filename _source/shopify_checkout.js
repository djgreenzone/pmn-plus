/* ---- Shopify checkout: build the cart (lines, code, email), open hosted checkout ---- */
  const CODE_KEY="pmn_code",SCART_KEY="pmn_scart";
  const store={get:k=>{try{return localStorage.getItem(k)}catch(e){return null}},set:(k,v)=>{try{v==null?localStorage.removeItem(k):localStorage.setItem(k,v)}catch(e){}}};
  let code=store.get(CODE_KEY)||"";
  const lineFor=i=>{const v=VAR[i.id]&&VAR[i.id][i.size||"One size"];return v&&v.ok?{merchandiseId:v.id,quantity:i.qty}:null};
  function cartInput(codes){const lines=cart.map(lineFor).filter(Boolean);if(bumpOn&&BUMP.variant)lines.push({merchandiseId:BUMP.variant,quantity:1});
    const bi={countryCode:"US"},em=store.get("pmn_email");if(em)bi.email=em;
    const at=[{key:"source",value:"pmn-shop"}].concat(window.pmnAttribution?window.pmnAttribution():[]);
    return{lines,discountCodes:codes,buyerIdentity:bi,attributes:at}}
  const CART_Q=`mutation($i:CartInput!){cartCreate(input:$i){cart{id checkoutUrl discountCodes{code applicable}} userErrors{message}}}`;
  function busy(on,label){[$("cartGo")].forEach(b=>{b.disabled=on;b.classList.toggle("busy",on&&b===busyBtn)});if(label)$("cartMsg").textContent=label}
  let busyBtn=null;
  async function checkout(e){if(!ready())return;busyBtn=e&&e.currentTarget||$("cartGo");
    busy(true,"Opening secure checkout…");await shopifyReady;
    try{const its=cart.map(i=>({id:i.id,name:(BY[i.id]||{}).name||i.id,price:(BY[i.id]||{}).price||0,size:i.size||"",qty:+i.qty||1}));window.pmnTrack&&window.pmnTrack("begin_checkout",{value:its.reduce((n,i)=>n+i.price*i.qty,0),items:its})}catch(e){}
    if(!shopifyOK){busy(false,"");return soon()}
    /* a size that isn't sold in this colour (e.g. from an older bag) -> ask for a size instead of failing */
    let fixed=0;cart.forEach(i=>{const p=BY[i.id];if(p&&p.kind==="tee"&&i.size&&!blankFor(p).sizes.includes(i.size)){i.size=null;fixed++}});
    if(fixed){setBag();render();busy(false,"Please choose a size for the highlighted item"+(fixed>1?"s":"")+".");return}
    const miss=cart.filter(i=>!lineFor(i)).map(i=>BY[i.id].name+(i.size&&i.size!=="One size"?` (${i.size})`:""));
    if(miss.length){busy(false,`${miss.join(", ")} ${miss.length>1?"aren't":"isn't"} available to order yet. Remove ${miss.length>1?"them":"it"} to check out.`);return}
    try{const d=await sf(CART_Q,{i:cartInput(code?[code]:[])});const r=d.cartCreate;
      if(r.userErrors&&r.userErrors.length)throw new Error(r.userErrors[0].message);
      store.set(SCART_KEY,r.cart.id);setTimeout(()=>busy(false,""),8000);location.href=r.cart.checkoutUrl}
    catch(err){console.warn("checkout",err);busy(false,"Checkout didn't load. Please try again in a moment.")}}
  $("cartGo").onclick=checkout;
  /* coming back from checkout (Back button / bfcache): unlock the button */
  addEventListener("pageshow",()=>busy(false,""));busy(false,"");
  /* discount code: validated against Shopify, applied at checkout */
  function showCode(){const has=!!code;$("codeForm").hidden=has;$("codeOn").hidden=!has;$("codeTag").textContent=code;window.pmnCodeNote&&pmnCodeNote()}
  $("codeToggle").onclick=()=>{const f=$("codeBox");f.hidden=!f.hidden;$("codeToggle").setAttribute("aria-expanded",!f.hidden);if(!f.hidden)$("codeIn").focus()};
  $("codeForm").addEventListener("submit",async ev=>{ev.preventDefault();const c=$("codeIn").value.trim().toUpperCase();const m=$("codeMsg");
    if(!c){m.textContent="Enter a code.";return}
    m.textContent="Checking…";await shopifyReady;
    if(!shopifyOK){m.textContent="Codes can't be checked right now. Enter it at checkout.";return}
    try{const inp=cartInput([c]);if(!inp.lines.length){m.textContent="Add something to your bag first.";return}
      const d=await sf(CART_Q,{i:inp}),dc=(d.cartCreate.cart&&d.cartCreate.cart.discountCodes||[]).find(x=>x.code.toUpperCase()===c);
      if(dc&&dc.applicable){code=c;store.set(CODE_KEY,c);m.textContent="";$("codeIn").value="";showCode();toast(`${c} added. Your savings show at checkout.`)}
      else m.textContent=`${c} isn't valid for this bag.`}
    catch(err){m.textContent="Couldn't check that code. Try again."}});
  $("codeRm").onclick=()=>{code="";store.set(CODE_KEY,null);showCode()};
  window.pmnSetCode=c=>{code=c;store.set(CODE_KEY,c);showCode()};
  showCode();
  /* back from checkout: if the Shopify cart became an order, clear the bag */
  (async()=>{const id=store.get(SCART_KEY);if(!id)return;await shopifyReady;if(!shopifyOK)return;
    try{const d=await sf(`query($id:ID!){cart(id:$id){id}}`,{id});
      if(!d.cart){store.set(SCART_KEY,null);store.set(CODE_KEY,null);code="";showCode();cart.splice(0,cart.length);bumpOn=false;setBag();render();
        toast("Thanks for your order! Your confirmation is on its way by email.")}}catch(e){}})();
