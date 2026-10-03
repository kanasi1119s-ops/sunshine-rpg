"""参考画像（小さな絵）を、トレース練習用に切り出す: 不透明部分の外接矩形（余白1）に切り、文字グリッドとパレットJSONにする。
使い方: python3 prep-trace.py 参考.png 出力フォルダ 名前   （色が多すぎる絵は 2 を返す）"""
import sys, json, os
from PIL import Image
import numpy as np
src, outdir, name = sys.argv[1:4]
MAXC = int(os.environ.get("MAXC", "14"))
im = Image.open(src).convert("RGBA")
a = np.array(im); m = a[..., 3] > 127
if not m.any(): sys.exit(2)
ys, xs = np.where(m); y0, y1, x0, x1 = max(0, ys.min()-1), min(a.shape[0], ys.max()+2), max(0, xs.min()-1), min(a.shape[1], xs.max()+2)
a = a[y0:y1, x0:x1]; h, w = a.shape[:2]
if max(h, w) > int(os.environ.get("MAXSIZE", "40")): sys.exit(3)
names = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
cols = {}; rows = []
for y in range(h):
    s = ""
    for x in range(w):
        p = tuple(int(v) for v in a[y, x])
        if p[3] < 128: s += "."; continue
        if p[:3] not in cols:
            if len(cols) >= MAXC: sys.exit(4)
            cols[p[:3]] = names[len(cols)]
        s += cols[p[:3]]
    rows.append(s)
os.makedirs(outdir, exist_ok=True)
open(f"{outdir}/{name}.txt", "w").write("\n".join(rows) + "\n")
json.dump({v: "#%02x%02x%02x" % k for k, v in cols.items()}, open(f"{outdir}/{name}.json", "w"))
Image.fromarray(a, "RGBA").save(f"{outdir}/{name}.png")
print(name, w, h, len(cols))
