"""Branded 1200x630 share cards for the editorial hub pages -> <root>/assets/og/<name>.jpg

Story and issue pages share their own photography (the hero, the cover). Hub pages have no single
image that honestly represents them: /digital-magazine covers every issue, /stories covers every
story, a category covers a whole subject. They were borrowing their newest story's hero, which is
why sharing /digital-magazine showed one artist's cover as if the page were about him.

Per the brand guide: PMN+ is black and white — no accent colour, team colours only on team content.
Headlines are Bebas uppercase, photography is darkened with a black gradient before text goes over it.

Two layouts:
  "shelf" — covers shown whole, overlapping, like issues on a shelf. For /digital-magazine, where no
            single cover should stand for the magazine.
  "bleed" — a full-bleed collage of up to three photos under a black gradient. For /stories and the
            category and author hubs.
With no usable images either falls back to type on black, which still beats someone else's photo.

Imported and run by build.py.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "fonts", "BebasNeue-Regular.ttf")
W, H = 1200, 630
INK, DIM, LINE = (255, 255, 255), (138, 138, 142), (36, 36, 38)


def _f(px):
    return ImageFont.truetype(FONT, px)


def _ls(dr, xy, text, font, fill, ls=0):
    """Pillow has no letter-spacing; step the pen manually."""
    x, y = xy
    for ch in text:
        dr.text((x, y), ch, font=font, fill=fill)
        x += dr.textlength(ch, font=font) + ls


def _wrap(dr, text, font, maxw):
    out, line = [], ""
    for w in text.split():
        t = (line + " " + w).strip()
        if dr.textlength(t, font=font) <= maxw:
            line = t
        else:
            out.append(line)
            line = w
    out.append(line)
    return [l for l in out if l]


def _fit(dr, text, maxw, maxlines, big=112, small=52):
    size = big
    while size > small:
        f = _f(size)
        if len(_wrap(dr, text, f, maxw)) <= maxlines:
            break
        size -= 6
    f = _f(size)
    return f, _wrap(dr, text, f, maxw)[:maxlines], size


def _cover(im, w, h):
    r = max(w / im.width, h / im.height)
    im = im.resize((max(1, round(im.width * r)), max(1, round(im.height * r))), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def _contain(im, w, h):
    r = min(w / im.width, h / im.height)
    return im.resize((max(1, round(im.width * r)), max(1, round(im.height * r))), Image.LANCZOS)


def _vgrad(w, h, top=0, bottom=235):
    """Black, transparent at the top, `bottom` alpha at the bottom."""
    g = Image.new("L", (1, h))
    px = g.load()
    for y in range(h):
        t = y / max(1, h - 1)
        px[0, y] = int(top + (bottom - top) * (t ** 1.45))
    a = g.resize((w, h))
    out = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    out.putalpha(a)
    return out


def _hgrad(w, h, left=242, right=0, stop=0.72):
    g = Image.new("L", (w, 1))
    px = g.load()
    for x in range(w):
        t = min(1.0, (x / max(1, w - 1)) / stop)
        px[x, 0] = int(left + (right - left) * (t ** 0.85))
    out = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    out.putalpha(g.resize((w, h)))
    return out


def _open(p):
    try:
        return Image.open(p).convert("RGB")
    except Exception:
        return None


def card(path, headline, eyebrow="PMN+", images=(), layout="bleed",
         kicker="polynesianmusicnetwork.com", logo=None):
    ims = [i for i in (_open(p) for p in (images or [])) if i is not None][:3]
    im = Image.new("RGB", (W, H), (0, 0, 0))

    if ims and layout == "bleed":
        n = len(ims)
        cw = W // n
        for k, src in enumerate(ims):
            x = k * cw
            im.paste(_cover(src, (W - x) if k == n - 1 else cw, H), (x, 0))
        im = Image.alpha_composite(im.convert("RGBA"), _vgrad(W, H, 25, 212))
        im = Image.alpha_composite(im, _hgrad(W, H, 222, 0, 0.62)).convert("RGB")
        tx, tw = 72, 660

    elif ims and layout == "shelf":
        # Covers whole and side by side — never overlapping, which hid everything but the newest and
        # said the opposite of "every issue". One or two covers sit large beside the headline; three
        # run across the top with the headline underneath, so the card fills either way.
        gap = 18
        ch = {1: 470, 2: 404}.get(len(ims), 296)
        plates = [_contain(s, int(ch * 0.8), ch) for s in ims]
        total = sum(p.width for p in plates) + gap * (len(plates) - 1)
        side = len(ims) < 3
        x = W - 56 - total
        y = (H - ch) // 2 if side else 40
        dr0 = ImageDraw.Draw(im)
        for pl in plates:
            yy = y + (ch - pl.height) // 2
            dr0.rectangle([x - 1, yy - 1, x + pl.width, yy + pl.height], fill=LINE)
            im.paste(pl, (x, yy))
            x += pl.width + gap
        im = Image.alpha_composite(im.convert("RGBA"), _vgrad(W, H, 0, 150)).convert("RGB")
        tx = 72
        tw = (W - 56 - total - 48 - tx) if side else W - 144

    else:
        im = Image.alpha_composite(im.convert("RGBA"), _vgrad(W, H, 0, 90)).convert("RGB")
        tx, tw = 72, W - 144

    dr = ImageDraw.Draw(im)
    if logo and os.path.exists(logo):
        mark = Image.open(logo).convert("RGBA")
        mark.thumbnail((96, 96), Image.LANCZOS)
        im.paste(mark, (tx, 54), mark)

    nl = 3 if (ims and layout == "shelf" and len(ims) < 3) else 2
    f, lines, size = _fit(dr, headline.upper(), tw, nl, big=104 if ims and layout == "shelf" else 112)
    lh = int(size * 0.9)
    y = H - 118 - lh * len(lines)
    _ls(dr, (tx, y - 44), eyebrow.upper(), _f(28), DIM, 5)
    for ln in lines:
        _ls(dr, (tx, y), ln, f, INK, 2)
        y += lh
    _ls(dr, (tx, H - 72), kicker.upper(), _f(24), DIM, 3)

    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, "JPEG", quality=88, optimize=True)
    return path
