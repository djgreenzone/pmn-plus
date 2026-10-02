"""Per-product share images (1200x630) -> ../shop/og/<slug>.jpg
Run after seo_build.py:  python3 make_og.py [path-to-shop-folder]"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
D=os.path.dirname(os.path.abspath(__file__))+'/'
SHOP=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else D+'../shop')+'/'
d=json.load(open(D+'site2/seo/seo-data.json'))
F=lambda n:ImageFont.truetype(D+'fonts/BebasNeue-Regular.ttf',n)
W,H=1200,630
BG={'samoa':'brand/toa-samoa-pattern-background-blue.webp','tonga':'brand/mate-maa-tonga-pattern-background-red.webp'}
CREST={'samoa':'brand/toa-samoa-rugby-league-crest.webp','tonga':'brand/mate-maa-tonga-rugby-league-crest.webp'}
def cover(im):
    r=max(W/im.width,H/im.height);im=im.resize((round(im.width*r),round(im.height*r)),Image.LANCZOS)
    x=(im.width-W)//2;y=(im.height-H)//2;return im.crop((x,y,x+W,y+H))
def wrap(dr,text,font,maxw):
    out=[];line=''
    for w in text.split():
        t=(line+' '+w).strip()
        if dr.textlength(t,font=font)<=maxw: line=t
        else: out.append(line);line=w
    out.append(line);return out
os.makedirs(SHOP+'og',exist_ok=True)
for pid,o in d['products'].items():
    team=o['team']
    if team in BG: bg=ImageEnhance.Brightness(cover(Image.open(SHOP+BG[team]).convert('RGB'))).enhance(.55)
    else:
        bg=Image.new('RGB',(W,H),(10,11,15));g=Image.new('L',(W,H),0);ImageDraw.Draw(g).ellipse((560,-120,1300,760),fill=90);bg.paste((60,62,70),mask=g.filter(ImageFilter.GaussianBlur(120)))
    # soft dark band behind the text
    sh=Image.new('L',(W,H),0);ImageDraw.Draw(sh).rectangle((0,0,640,H),fill=150);bg.paste((0,0,0),mask=sh.filter(ImageFilter.GaussianBlur(90)))
    rel=o['images'][0].split('/shop/')[1]
    im=Image.open(SHOP+rel).convert('RGBA');bb=im.getbbox();im=im.crop(bb)
    r=min(520/im.height,540/im.width);im=im.resize((round(im.width*r),round(im.height*r)),Image.LANCZOS)
    x=620+(540-im.width)//2;y=(H-im.height)//2
    shadow=Image.new('RGBA',bg.size,(0,0,0,0));sa=im.split()[3].point(lambda a:a*.55)
    shadow.paste((0,0,0,255),(x+14,y+22),sa);bg=Image.alpha_composite(bg.convert('RGBA'),shadow.filter(ImageFilter.GaussianBlur(18)))
    bg.alpha_composite(im,(x,y))
    dr=ImageDraw.Draw(bg);X=64
    if team in CREST:
        c=Image.open(SHOP+CREST[team]).convert('RGBA');c=c.resize((round(c.width*96/c.height),96),Image.LANCZOS);bg.alpha_composite(c,(X,64));ty=196
    else:
        dr.text((X,64),'PMN+',font=F(84),fill=(255,255,255));ty=190
    dr.text((X,ty),o['teamName'].upper()+('  ·  RLWC 2026' if team!='pmn' else '  ·  PASIFIKA APPAREL'),font=F(30),fill=(255,255,255,190))
    f=F(88);lines=wrap(dr,o['h1'].upper(),f,520)
    if len(lines)>2:f=F(70);lines=wrap(dr,o['h1'].upper(),f,520)
    yy=ty+46
    for l in lines: dr.text((X,yy),l,font=f,fill=(255,255,255));yy+=int(f.size*.92)
    dr.text((X,yy+10),o['colour'].upper(),font=F(34),fill=(255,255,255,200))
    foot='SOLD OUT' if o.get('sold') else 'SHIPS ACROSS THE USA'
    dr.text((X,H-64-30),'POLYNESIANMUSICNETWORK.COM/SHOP  ·  '+foot,font=F(30),fill=(255,255,255,170))
    bg.convert('RGB').save(SHOP+f"og/{o['slug']}.jpg",quality=86,optimize=True,progressive=True)
    print(o['slug'])
