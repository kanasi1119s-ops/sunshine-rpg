# 「予言の歪み」の動き（歩く16コマ・攻撃3種類）を PNG のコマに書き出す（オープニング映像用）。
# 使い方: python3 export-yogen.py <anim.json> <final.json> <出力フォルダ>
#   anim.json・final.json は monster-fullbody ブランチの assets-src/monsters/kiri-yugami/ にある。
# 出力: <出力>/frames/<動き>_<番号>.png と <出力>/ms.json（コマごとの長さ・ミリ秒）
import json, os, sys
import numpy as np
from PIL import Image, ImageColor
anim, palf, out = sys.argv[1:4]
a = json.load(open(anim)); pal = json.load(open(palf))
pal.update({"0": "#e8fbff", "1": "#9ee8ff", "2": "#4fb7d8"})   # boss_rig.py が足す光の色
lut = np.zeros((256, 4), np.uint8)
for k, v in pal.items(): lut[ord(k)] = ImageColor.getrgb(v) + (255,)
def arr(rows): return np.frombuffer("".join(rows).encode("latin1"), np.uint8).reshape(len(rows), len(rows[0]))
os.makedirs(f"{out}/frames", exist_ok=True)
names = ["walk", "attack", "attack2", "attack3"]
for n in names:
    for i, fr in enumerate(a[n]):
        if a.get("flat_" + n): g = arr(a["flat_" + n][i])
        else:
            g = None
            for L in a["layers"]:
                x = arr(fr[L])
                if g is None: g = np.full(x.shape, ord("."), np.uint8)
                g[x != ord(".")] = x[x != ord(".")]
        Image.fromarray(lut[g], "RGBA").save(f"{out}/frames/{n}_{i:02d}.png")
json.dump({n: a[n + "_ms"] for n in names}, open(f"{out}/ms.json", "w"))
