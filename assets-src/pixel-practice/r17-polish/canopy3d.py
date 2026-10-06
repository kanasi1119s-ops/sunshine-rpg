"""町の草むら（treeCanopy）の地形の絵を、立体の茂みにする（2026-10-06、人間の指示「草むらり立体感ないよ」）。
128×128 の、上下左右がつながる（くり返せる）絵。丸い葉の株（茂み）を、ずらした格子にたくさん並べ、
奥（上）から手前（下）へ順に重ねて描く（手前の株が、奥の株の下の方をかくす）。
1つずつの株は、丸いもりあがりとして、左上の光で明るさを決め、下と、株と株のすきまは暗く、
株の上には、こまかな葉のむら・明るい葉先・ところどころ小さな花。
書き出し: canopy.txt / pal-canopy.json（エディタで確かめる）と、tools/pixel-art/canopy-terrain.json（ゲームの terrain:forest を置きかえる）。"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
N = 128
# 2026-10-06「木も草も作り直し町になじんでない」: 町の草地（オリーブがかった落ちついた緑）と同じ色合いに
LEAF = ["#223619", "#2c441f", "#375226", "#42602d", "#4e6e34", "#5a7c3c", "#668a44", "#73974d", "#82a458", "#93b266"]
GAP = "#1a2a14"


def hn(*a):
    n = 2166136261
    for v in a:
        n = ((n ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    n ^= n >> 15
    return n


def rnd(*a):
    return (hn(*a) & 0xFFFF) / 65535


# 株の置き場所（ずらした格子＋ゆらぎ）。くり返せるよう、格子は 128 をちょうど割り切る
STEP = 16
clumps = []
for gy in range(N // STEP * 2):
    for gx in range(N // STEP):
        x = gx * STEP + (STEP / 2 if gy % 2 else 0) + (rnd(gx, gy, 1) - 0.5) * 6
        y = gy * STEP / 2 + (rnd(gx, gy, 2) - 0.5) * 4
        r = 8.5 + rnd(gx, gy, 3) * 3.0
        clumps.append((y, x, r, hn(gx, gy, 4)))
clumps.sort()                                       # 奥（上）から順に

lum = np.full((N, N), 0.15)                         # すきまは暗い
height = np.full((N, N), -1.0)
L = np.array([-0.55, -0.6, 0.58]); L /= np.linalg.norm(L)   # 光（左上・手前）。画面の y は下向き
for (cy, cx, r, seed) in clumps:
    ry = r * 0.78                                   # 少しつぶれた丸（上から見た茂み）
    for oy in (-N, 0, N):
        for ox in (-N, 0, N):
            x0, x1 = int(cx + ox - r - 1), int(cx + ox + r + 2)
            y0, y1 = int(cy + oy - ry - 1), int(cy + oy + ry + 2)
            if x1 < 0 or y1 < 0 or x0 >= N or y0 >= N:
                continue
            for y in range(max(0, y0), min(N, y1)):
                for x in range(max(0, x0), min(N, x1)):
                    u = (x + 0.5 - (cx + ox)) / r
                    v = (y + 0.5 - (cy + oy)) / ry
                    # ふちを葉のぎざぎざに（角度でゆれる半径）
                    ang = math.atan2(v, u)
                    edge = 1.0 - 0.09 * (0.5 + 0.5 * math.sin(ang * 7 + seed % 13)) - 0.05 * rnd(int(ang * 9), seed)
                    d2 = u * u + v * v
                    if d2 > edge * edge:
                        continue
                    nz = math.sqrt(max(0.0, 1 - d2 / (edge * edge)))
                    n = np.array([u, v, nz * 1.3]); n /= np.linalg.norm(n)
                    l = 0.22 + 0.78 * max(0.0, float(n @ L))
                    l *= 0.6 + 0.4 * min(1.0, (1.15 - v) )          # 株の下の方は、影で暗い
                    if d2 > (edge * 0.86) ** 2 and v > 0:
                        l *= 0.7                                     # 下のふちの影の線
                    # こまかな葉のむら
                    l += ((hn(x, y, 9) % 7) - 3) * 0.025
                    lum[y, x] = l * 0.8                              # まわりの草地より少し暗く（茂みとしてうき出る）
                    height[y, x] = nz

# 色にする（段のあいだは、市松でまぜる）
BAYER = np.array([[0.125, 0.625], [0.875, 0.375]])
img = np.full((N, N), "", dtype=object)
for y in range(N):
    for x in range(N):
        if height[y, x] < 0:
            img[y, x] = GAP
            continue
        v = np.clip(lum[y, x], 0, 0.999) * (len(LEAF) - 1)
        lo = int(v); fr = v - lo
        k = lo + (1 if (fr > 0.62 or (0.38 <= fr <= 0.62 and BAYER[y % 2, x % 2] < 0.5)) else 0)
        c = LEAF[min(len(LEAF) - 1, k)]
        # 明るい所に、ときどき葉先の光と、小さな花
        if lum[y, x] > 0.72 and hn(x, y, 21) % 23 == 0:
            c = LEAF[-1]
        if height[y, x] > 0.55 and hn(x // 2, y // 2, 33) % 97 == 0:
            c = ["#f4f0e0", "#f2c14e", "#e86a8a"][hn(x, y, 5) % 3]
        img[y, x] = c

cols = sorted(set(img.flatten().tolist()))
syms = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
cmap = {c: syms[i] for i, c in enumerate(cols)}
rows = ["".join(cmap[img[y, x]] for x in range(N)) for y in range(N)]
open(os.path.join(HERE, "canopy.txt"), "w").write("\n".join(rows) + "\n")
json.dump({cmap[c]: c for c in cols}, open(os.path.join(HERE, "pal-canopy.json"), "w"))

# ゲームの形（export-game-data.mjs と同じ RLE。色が27色以上なら「~色番号:数,...」）
pal = cols
idx = [cols.index(img[y, x]) for y in range(N) for x in range(N)]
if len(pal) > 26:
    toks = []; prev = None; n = 0
    for k in idx:
        if k == prev:
            n += 1
        else:
            if prev is not None:
                toks.append(f"{prev}:{n}")
            prev, n = k, 1
    toks.append(f"{prev}:{n}")
    rle = "~" + ",".join(toks)
else:
    def b36(v):
        s = ""
        while v:
            s = "0123456789abcdefghijklmnopqrstuvwxyz"[v % 36] + s; v //= 36
        return s
    out = []; prev = None; n = 0
    for k in idx + [None]:
        if k == prev:
            n += 1
            continue
        if prev is not None:
            out.append(chr(65 + prev) + (b36(n) if n > 1 else ""))
        prev, n = k, 1
    rle = "".join(out)
json.dump({"terrain:forest": {"size": N, "palette": pal, "rle": rle}}, open(os.path.join(ROOT, "tools", "pixel-art", "canopy-terrain.json"), "w"))
print("ok colors", len(cols))
