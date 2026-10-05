"""Turn a 360 render (folder of RGBA PNG frames, e.g. `ffmpeg -i turn.mov -pix_fmt rgba f%03d.png`)
plus transparent stills into the site's spin assets.

  python3 tools/add_spin.py <id> <seo-slug> <frames_dir> <loop> [angle=still.png ...]

<loop> = number of source frames in one full turn (frame loop+1 repeats frame 1; the 4s
Pacdora ProRes exports are 91 or 92). The turn is resampled to 90 frames, 4° apart, and
packed into 6 interleaved sprite sheets (sheet j = frames j, j+6, …) like the existing tees.
Stills are trimmed to their alpha box and saved as hires/<id>/<seo>-<view>.webp.
Prints the META entry for site2/index.html."""
import sys, os, glob, json
from PIL import Image
N, S, COLS, PAD = 90, 6, 5, 4
def view(a):
    a %= 360
    for lo, hi, n in ((350, 361, "front"), (0, 10, "front"), (30, 60, "front-right"), (75, 105, "right"),
                      (160, 200, "back"), (255, 285, "left"), (300, 330, "front-left")):
        if lo <= a < hi: return n
    return f"a{a}"
pid, seo, src, loop, *stills = sys.argv[1:]
loop = int(loop)
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "shop")
files = sorted(glob.glob(os.path.join(src, "*.png")))
ims = [Image.open(files[round(k * 4 * loop / 360) % loop]).convert("RGBA") for k in range(N)]
bb = None
for im in ims:
    b = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
W, H = ims[0].size
box = (max(0, bb[0] - PAD), max(0, bb[1] - PAD), min(W, bb[2] + PAD), min(H, bb[3] + PAD))
fw, fh = box[2] - box[0], box[3] - box[1]
fr = [im.crop(box) for im in ims]
fd = os.path.join(root, "frames", pid); os.makedirs(fd, exist_ok=True)
fr[0].save(f"{fd}/00.webp", quality=82, method=4)
kb, rows = 0, -(-(N // S) // COLS)
for j in range(S):
    sh = Image.new("RGBA", (COLS * fw, rows * fh), (0, 0, 0, 0))
    for q, k in enumerate(range(j, N, S)):
        sh.paste(fr[k], ((q % COLS) * fw, (q // COLS) * fh))
    p = f"{fd}/s{j}.webp"; sh.save(p, quality=80, method=4); kb += os.path.getsize(p)
hi, hikb = {}, 0
hd = os.path.join(root, "hires", pid); os.makedirs(hd, exist_ok=True)
for s in stills:
    a, f = s.split("=", 1); a = int(a) % 360
    im = Image.open(f).convert("RGBA")
    b = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    im = im.crop((max(0, b[0] - 8), max(0, b[1] - 8), min(im.width, b[2] + 8), min(im.height, b[3] + 8)))
    name = f"{seo}-{view(a)}"; p = f"{hd}/{name}.webp"
    im.save(p, quality=84, method=4); hi[str(a)] = name; hikb += os.path.getsize(p)
print(json.dumps({pid: {"w": fw, "h": fh, "sw": fw, "sh": fh, "src": "transparent export", "n": N, "strips": S, "cols": COLS,
      "kb": kb // 1024, "hi": hi, "hiKb": hikb // 1024, "seo": seo}}, separators=(",", ":")))
