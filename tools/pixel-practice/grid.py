"""文字グリッド（練習で手書きした絵）⇔ PNG、および参考画像との一致率。
グリッドの書式: 1行目以降が絵。'.'は透明、1文字=1色。パレットは別ファイル(JSON {"文字":"#rrggbb"})。
使い方:
  python3 grid.py render 絵.txt パレット.json 出力.png [倍率]
  python3 grid.py ascii 参考.png [x,y,w,h]    # 参考画像を文字グリッド＋パレットに起こす（模写・トレースの下準備）
  python3 grid.py score 絵.txt パレット.json 参考.png [x,y,w,h]  # 画素の一致率と輪郭の一致率
"""
import sys, json
from PIL import Image
import numpy as np
def load_grid(path, pal):
    rows = [l.rstrip("\n") for l in open(path, encoding="utf-8") if l.strip() != "" and not l.startswith("#")]
    w = max(len(r) for r in rows)
    a = np.zeros((len(rows), w, 4), dtype=np.uint8)
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != "." and ch != " ":
                h = pal[ch].lstrip("#"); a[y, x] = (int(h[0:2],16), int(h[2:4],16), int(h[4:6],16), 255)
    return a
def crop(im, spec):
    if spec:
        x, y, w, h = map(int, spec.split(",")); return im.crop((x, y, x+w, y+h))
    return im
cmd = sys.argv[1]
if cmd == "render":
    pal = json.load(open(sys.argv[3])); a = load_grid(sys.argv[2], pal)
    z = int(sys.argv[5]) if len(sys.argv) > 5 else 8
    im = Image.fromarray(a, "RGBA"); bg = Image.new("RGBA", im.size, (61,49,96,255)); bg.alpha_composite(im)
    bg.resize((im.width*z, im.height*z), Image.NEAREST).convert("RGB").save(sys.argv[4])
elif cmd == "ascii":
    im = crop(Image.open(sys.argv[2]).convert("RGBA"), sys.argv[3] if len(sys.argv) > 3 else None)
    a = np.array(im); cols = {}; names = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    out = []
    for y in range(a.shape[0]):
        s = ""
        for x in range(a.shape[1]):
            p = tuple(int(v) for v in a[y, x])
            if p[3] < 128: s += "."; continue
            if p[:3] not in cols: cols[p[:3]] = names[len(cols)] if len(cols) < len(names) else "?"
            s += cols[p[:3]]
        out.append(s)
    print("\n".join(out)); print(json.dumps({v: "#%02x%02x%02x" % k for k, v in cols.items()}, ensure_ascii=False), file=sys.stderr)
elif cmd == "score":
    pal = json.load(open(sys.argv[3])); a = load_grid(sys.argv[2], pal)
    r = np.array(crop(Image.open(sys.argv[4]).convert("RGBA"), sys.argv[5] if len(sys.argv) > 5 else None))
    h, w = min(a.shape[0], r.shape[0]), min(a.shape[1], r.shape[1]); a, r = a[:h,:w], r[:h,:w]
    ma, mr = a[...,3] > 127, r[...,3] > 127
    sil = (ma == mr).mean(); both = ma & mr
    exact = ((a[...,:3] == r[...,:3]).all(-1) & both).sum() / max(1, (ma | mr).sum())
    # 色は近さで評価（1色の違いに厳しすぎないよう、RGB距離48以内なら近いとする）
    near = ((np.abs(a[...,:3].astype(int) - r[...,:3].astype(int)).sum(-1) < 48) & both).sum() / max(1, (ma | mr).sum())
    print(f"シルエット一致 {sil*100:.1f}% / 色まで完全一致 {exact*100:.1f}% / 色が近い {near*100:.1f}%  （{w}x{h}）")
if cmd == "compare":
    # 参考 | 自作 | 差（赤＝食い違い）を並べた画像。 compare 絵.txt パレット.json 参考.png 出力.png [倍率]
    pal = json.load(open(sys.argv[3])); a = load_grid(sys.argv[2], pal)
    r = np.array(Image.open(sys.argv[4]).convert("RGBA")); z = int(sys.argv[6]) if len(sys.argv) > 6 else 10
    h, w = min(a.shape[0], r.shape[0]), min(a.shape[1], r.shape[1]); a, r = a[:h,:w], r[:h,:w]
    diff = np.zeros((h, w, 4), dtype=np.uint8); diff[...] = (40, 30, 60, 255)
    ma, mr = a[...,3] > 127, r[...,3] > 127
    for y in range(h):
        for x in range(w):
            if ma[y,x] != mr[y,x]: diff[y,x] = (230, 40, 40, 255)
            elif ma[y,x] and np.abs(a[y,x,:3].astype(int) - r[y,x,:3].astype(int)).sum() >= 48: diff[y,x] = (240, 190, 40, 255)
            elif ma[y,x]: diff[y,x] = (60, 160, 90, 255)
    def prep(arr):
        im = Image.fromarray(arr, "RGBA"); bg = Image.new("RGBA", im.size, (61,49,96,255)); bg.alpha_composite(im); return bg.resize((w*z, h*z), Image.NEAREST).convert("RGB")
    ims = [prep(r), prep(a), prep(diff)]
    c = Image.new("RGB", (w*z*3 + 20, h*z), (0,0,0))
    for i, im in enumerate(ims): c.paste(im, (i*(w*z+10), 0))
    c.save(sys.argv[5])
if cmd == "trace":
    # 参考画像の輪郭だけを写した下書き（縁=A、中=x）。中の陰影は自分の目で描き込む。 trace 参考.png [x,y,w,h]
    im = crop(Image.open(sys.argv[2]).convert("RGBA"), sys.argv[3] if len(sys.argv) > 3 else None)
    m = np.array(im)[..., 3] > 127; h, w = m.shape
    for y in range(h):
        s = ""
        for x in range(w):
            if not m[y, x]: s += "."; continue
            edge = any(not (0 <= y+dy < h and 0 <= x+dx < w and m[y+dy, x+dx]) for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)))
            s += "A" if edge else "x"
        print(s)
