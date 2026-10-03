/* back-in-stock requests -> Klaviyo list "PMN+ Back in Stock Requests" (X4re4C) */
document.addEventListener("submit",async e=>{const f=e.target;if(f.id!=="pBis")return;e.preventDefault();
  const em=(f.querySelector("#bisEmail").value||"").trim(),m=f.querySelector("#bisMsg");m.className="bis-msg";
  if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em)){m.textContent="Enter a valid email address.";return}
  const slug=(location.pathname.match(/^\/shop\/([a-z0-9-]+)/)||[])[1]||f.dataset.id;
  try{const body={data:{type:"subscription",attributes:{custom_source:"Back in stock: "+f.dataset.name,profile:{data:{type:"profile",attributes:{email:em,properties:{bis_last_product:f.dataset.name,bis_last_slug:slug}}}}},relationships:{list:{data:{type:"list",id:"X4re4C"}}}}};
    const r=await fetch("https://a.klaviyo.com/client/subscriptions/?company_id="+KLAVIYO_COMPANY_ID,{method:"POST",headers:{"content-type":"application/json","revision":"2026-07-15"},body:JSON.stringify(body)});
    if(!(r.status===202||r.ok))throw new Error(r.status);
    try{localStorage.setItem("pmn_email",em)}catch(_){}
    try{window.klaviyo&&window.klaviyo.push(["track","Requested Back in Stock",{ProductName:f.dataset.name,ProductID:slug,URL:location.origin+"/shop/"+slug}])}catch(_){}
    m.classList.add("ok");m.textContent="You're on the list. We'll email you when it's back.";f.querySelector("#bisEmail").value=""}
  catch(err){m.textContent="That didn't go through. Please try again."}});
