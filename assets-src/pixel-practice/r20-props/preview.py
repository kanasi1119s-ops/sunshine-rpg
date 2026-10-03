"""全部の飾りを4倍に拡大して並べた確認画像 preview.png を作る。使い方: python3 preview.py [名前 ...]（名前を渡すとその分だけ preview-tmp.png に出す）"""
import json, sys, glob, os
from PIL import Image, ImageDraw

TOWN_BG = (96, 138, 80)
DUNG_BG = (58, 54, 74)
DUNG = {"pillar", "pillar-broken", "statue-soldier", "statue-winged", "banner-purple", "banner-red", "bones", "cobweb", "candelabra",
        "coffin", "barrel-broken", "box-broken", "crystal-blue", "crystal-red", "mushrooms", "chest-closed", "chest-open", "chains", "jail-bars"}

def load(name):
    rows = open(f"{name}.txt").read().split("\n")
    rows = [r for r in rows if r != ""]
    pal = json.load(open(f"pal-{name}.json"))
    w, h = max(len(r) for r in rows), len(rows)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch in pal:
                v = pal[ch].lstrip("#")
                im.putpixel((x, y), tuple(int(v[i:i+2], 16) for i in (0, 2, 4)) + (255,))
    return im

def sheet(names, out, scale=4, cols=6, cell=(56, 56)):
    ims = [(n, load(n)) for n in names]
    cw, ch = cell
    rows_n = (len(ims) + cols - 1) // cols
    W, H = cols * (cw * scale + 8) + 8, rows_n * (ch * scale + 24) + 8
    img = Image.new("RGB", (W, H), (30, 30, 30))
    d = ImageDraw.Draw(img)
    for i, (n, im) in enumerate(ims):
        cx, cy = 8 + (i % cols) * (cw * scale + 8), 8 + (i // cols) * (ch * scale + 24)
        bg = DUNG_BG if n in DUNG else TOWN_BG
        d.rectangle([cx, cy, cx + cw * scale - 1, cy + ch * scale - 1], fill=bg)
        big = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
        ox = cx + (cw * scale - big.width) // 2
        oy = cy + ch * scale - big.height
        img.paste(big, (ox, oy), big)
        d.text((cx + 2, cy + ch * scale + 4), f"{n} {im.width}x{im.height}", fill=(230, 230, 230))
    img.save(out)

if __name__ == "__main__":
    allp = sorted(os.path.basename(p)[:-4] for p in glob.glob("*.txt"))
    names = sys.argv[1:] or [n for n in allp if n not in DUNG] + [n for n in allp if n in DUNG]
    if sys.argv[1:]:
        sheet(names, "preview-tmp.png", scale=6, cols=4)
    else:
        sheet(names, "preview.png")
