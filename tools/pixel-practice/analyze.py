"""トレースした絵の色づかいを数字にする。使い方: python3 analyze.py トレースフォルダ 名前...
出力: 色数・縁取りの色・明るい順の色（色相H・彩度S・明度L・ドット数）・暗→明で色相がどちらへずれるか。"""
import sys, json, colorsys
from PIL import Image
import numpy as np
d = sys.argv[1]
for n in sys.argv[2:]:
    a = np.array(Image.open(f"{d}/{n}.png").convert("RGBA")); m = a[..., 3] > 127
    cols = {}
    for p in a[m]: cols[tuple(p[:3])] = cols.get(tuple(p[:3]), 0) + 1
    hsl = lambda c: tuple(round(v, 2) for v in colorsys.rgb_to_hls(*[x / 255 for x in c]))
    items = sorted(((hsl(c)[1], c, k) for c, k in cols.items()))
    dark = items[0]; edge = a[m]  # 外周の色
    h, w = m.shape; border = []
    for y in range(h):
        for x in range(w):
            if m[y, x] and any(not (0 <= y+dy < h and 0 <= x+dx < w and m[y+dy, x+dx]) for dy, dx in ((1,0),(-1,0),(0,1),(0,-1))): border.append(tuple(a[y, x, :3]))
    from collections import Counter
    bc = Counter(border).most_common(1)[0]
    bl = hsl(bc[0])[1]
    line = f"{n}: {w}x{h} 色{len(cols)} 外周の主な色 L={bl:.2f}({bc[1]*100//max(1,len(border))}%) "
    ramp = [(round(l, 2), round(hsv_h*360), round(s, 2)) for (l, c, k) in items for (hh, l2, s) in [colorsys.rgb_to_hls(*[x / 255 for x in c])] for hsv_h in [hh]]
    line += "明→ " + " ".join(f"L{l:.2f}/H{h}/S{s:.2f}" for l, h, s in ramp[::-1][:6])
    print(line)
