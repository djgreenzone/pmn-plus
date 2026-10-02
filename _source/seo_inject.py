import json, re
d=json.load(open('site2/seo/seo-data.json'))
p='site2/index.html'; s=open(p).read()
def rep(a,b):
    global s; assert a in s, a[:90]; s=s.replace(a,b,1)
lite={'policy':d['policy'],'collections':{k:{kk:v[kk] for kk in ('name','title','meta','intro','products')} for k,v in d['collections'].items()},
      'products':{k:{kk:v[kk] for kk in ('slug','title','meta','description','faq')} for k,v in d['products'].items()}}
blob='const SEO='+json.dumps(lite,ensure_ascii=False,separators=(',',':'))+';\n'
if 'const SEO=' in s:
    s=re.sub(r'const SEO=.*?;\n',lambda m:blob,s,count=1,flags=re.S)
else:
    rep('/* Product copy: written from the renders','%s/* Product copy: written from the renders'%blob)
# head JSON-LD from seo-data
org=next(n for v in d['products'].values() for n in v['jsonld']['@graph'] if n['@type']=='Organization')
D=d['domain']
graph=[org,{"@type":"WebSite","@id":D+"/#website","url":D+"/","name":"PMN+","publisher":{"@id":D+"/#org"}},
  {"@type":"CollectionPage","@id":D+"/shop#page","url":D+"/shop","name":"Shop PMN+","isPartOf":{"@id":D+"/#website"},
   "mainEntity":{"@type":"ItemList","numberOfItems":len(d['products']),"itemListElement":[{"@type":"ListItem","position":i+1,"url":v['url'],"name":v['h1']} for i,v in enumerate(d['products'].values())]}}]
ld='<script type="application/ld+json">'+json.dumps({"@context":"https://schema.org","@graph":graph},ensure_ascii=False,separators=(',',':'))+'</script>'
s=re.sub(r'<script type="application/ld\+json">.*?</script>',lambda m:ld,s,count=1,flags=re.S)
open(p,'w').write(s); print('injected', len(blob)//1024,'KB seo,', len(ld)//1024,'KB ld')
