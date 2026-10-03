# Klaviyo Reviews widgets on product pages (appended into make_shop.py run)
s=open(sys.argv[1]).read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:70],s.count(a));s=s.replace(a,b)
rep('<details id="pRevAcc"><summary>Reviews</summary><p>No reviews yet. Reviews from verified buyers will show here after the first orders ship.</p></details>',
    '<details id="pRevAcc"><summary>Reviews</summary><div id="pRevBox" class="rev-box"></div></details>')
rep('$("pTeam").textContent=teamName(p);$("pName").textContent=p.name;','$("pTeam").textContent=teamName(p);$("pName").textContent=p.name;try{klReviews(p)}catch(e){}')
rep('const reduceMotion=',open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'reviews.js')).read()+'const reduceMotion=')
rep('<div class="price-row"><strong class="num" id="pPrice">','<div id="pStars" class="p-stars"></div>\n          <div class="price-row"><strong class="num" id="pPrice">')
rep('.size.so{','#pStars{min-height:0;margin:6px 0 2px}#pStars:empty{display:none}.rev-box{padding:4px 0 12px;color:var(--ink)}.rev-none{margin:0;opacity:.7}.size.so{')
open(sys.argv[1],'w').write(s)
print('reviews ok')
