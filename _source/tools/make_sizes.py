"""Makes phone-sized copies of every product photo: shop/hires/<id>/<name>-320.webp and -640.webp.
The originals stay as they are (360° viewer stills, Google Shopping, share images).
Run after adding or replacing photos:  python3 tools/make_sizes.py   (from _source/). Safe to re-run."""
import glob, os, re
from PIL import Image
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','shop','hires')
made=0
for f in sorted(glob.glob(os.path.join(ROOT,'*','*.webp'))):
    if re.search(r'-(320|640)\.webp$',f): continue
    im=Image.open(f); im.load()
    for w in (320,640):
        out=f[:-5]+f'-{w}.webp'
        if os.path.exists(out) and os.path.getmtime(out)>=os.path.getmtime(f): continue
        if im.width<=w: im.save(out,'WEBP',quality=80,method=6)
        else: im.resize((w,round(im.height*w/im.width)),Image.LANCZOS).save(out,'WEBP',quality=80,method=6)
        made+=1
print(made,'sized copies written')
