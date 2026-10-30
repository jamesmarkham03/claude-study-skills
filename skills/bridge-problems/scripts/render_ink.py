# Render ink-stroke PDF pages (filled vector paths) to PNG with PIL.
#
# Handwritten tablet notes are often saved as vector paths with no text layer, so text
# extraction finds nothing. This draws the paths so the pages can be read as images,
# without needing Poppler or PyMuPDF installed.
#
# Usage: python render_ink.py <notes.pdf> <first-last> <out_dir>   e.g. 1-5 ./pages
import sys, os, pypdf
from pypdf.generic import ContentStream
from PIL import Image, ImageDraw, ImageFont

def bez(p0, p1, p2, p3, n=8):
    pts = []
    for k in range(1, n + 1):
        t = k / n; u = 1 - t
        pts.append((u**3*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t**3*p3[0],
                    u**3*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t**3*p3[1]))
    return pts

def render(pdf, pages, out, S=2.0):
    r = pypdf.PdfReader(pdf)
    font = ImageFont.load_default(size=22)
    for i in pages:
        pg = r.pages[i - 1]
        W, H = float(pg.mediabox.width), float(pg.mediabox.height)
        img = Image.new("RGB", (int(W*S), int(H*S)), "white"); d = ImageDraw.Draw(img)
        T = lambda x, y: (x*S, (H - y)*S)
        col = (0, 0, 0); stack = []; subs = []; cur = []; pt = (0, 0); tm = (0, 0)
        for ops, op in ContentStream(pg.get_contents(), r).operations:
            a = [float(v) for v in ops] if op in (b"m", b"l", b"c", b"g", b"rg", b"k") else ops
            if op == b"q": stack.append(col)
            elif op == b"Q": col = stack.pop() if stack else col
            elif op == b"g": v = int(a[0]*255); col = (v, v, v)
            elif op == b"rg": col = tuple(int(x*255) for x in a)
            elif op == b"k": c, m, y, kk = a; col = tuple(int(255*(1-min(1, x+kk))) for x in (c, m, y))
            elif op == b"m":
                if cur: subs.append(cur)
                pt = (a[0], a[1]); cur = [T(*pt)]
            elif op == b"l": pt = (a[0], a[1]); cur.append(T(*pt))
            elif op == b"c":
                p3 = (a[4], a[5]); cur += [T(*q) for q in bez(pt, (a[0], a[1]), (a[2], a[3]), p3)]; pt = p3
            elif op == b"h": pass
            elif op in (b"f", b"f*", b"F", b"B", b"b"):
                if cur: subs.append(cur)
                for sp in subs:
                    if len(sp) > 2: d.polygon(sp, fill=col)
                subs, cur = [], []
            elif op in (b"S", b"s"):
                if cur: subs.append(cur)
                for sp in subs:
                    if len(sp) > 1: d.line(sp, fill=col, width=2)
                subs, cur = [], []
            elif op == b"n": subs, cur = [], []
            elif op == b"Tm": tm = (float(ops[4]), float(ops[5]))
            elif op in (b"TJ", b"Tj"):
                txt = "".join(str(x) for x in (ops[0] if op == b"TJ" else ops) if isinstance(x, str))
                d.text(T(*tm), txt, fill=(0, 0, 160), font=font, anchor="ls")
        fn = os.path.join(out, f"{os.path.basename(pdf)[:20]}_p{i:02d}.png")
        img.save(fn); print(fn)

if __name__ == "__main__":
    pdf, rng, out = sys.argv[1], sys.argv[2], sys.argv[3]
    a, b = map(int, rng.split("-"))
    render(pdf, range(a, b + 1), out)
