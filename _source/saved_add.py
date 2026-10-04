# Saved items (heart) in the shop (appended into make_shop.py run)
s=open(sys.argv[1]).read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:70],s.count(a));s=s.replace(a,b)
rep('$("pAlso").innerHTML="";rest.slice(0,8).forEach(o=>{const b=document.createElement("button");b.className="card";','$("pAlso").innerHTML="";rest.slice(0,8).forEach(o=>{const b=document.createElement("button");b.className="card";b.dataset.id=o.id;')
rep('<div id="pStars" class="p-stars"></div>','<div class="p-namerow"><div id="pStars" class="p-stars"></div><button type="button" class="sv-btn" id="pSave" aria-pressed="false" aria-label="Save"></button></div>')
rep('try{klReviews(p)}catch(e){}','try{klReviews(p)}catch(e){}try{svPdp(p)}catch(e){}')
rep('const reduceMotion=',open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'saved_shop.js')).read()+'const reduceMotion=')
rep('.size.so{','.p-namerow{display:flex;align-items:center;justify-content:space-between;gap:12px;margin:6px 0 2px}.p-namerow #pStars{margin:0}.p-namerow .sv-btn{flex:none;margin-left:auto}.size.so{')
open(sys.argv[1],'w').write(s)
print('saved ok')
