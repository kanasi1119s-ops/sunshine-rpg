"""町の草むら（treeCanopy）の地形の絵を、立体の草むらにする（2026-10-06 作りなおし: 細い葉の株をびっしり並べた草むら）。
以下は前の説明: 町の草むら（treeCanopy）の地形の絵を、立体の茂みにする（2026-10-06、人間の指示「草むらり立体感ないよ」）。
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


# 2026-10-06 作りなおし（人間の指示「草むら作り直して、もっといいものを」）: 丸い茂みをやめ、
# 背の高い草の株（細い葉が7〜9本、根もとから扇のように広がる）を、ずらした格子にびっしり並べた「草むら」にする。
# 葉は1本ずつ、根もとは暗く、先は明るく。左（光の側）へかたむく葉は明るく、右へかたむく葉は暗い。
# 株の根もとには影。奥（上）から手前（下）へ順に描くので、手前の株が奥の株の根もとをかくし、奥行きが出る。
lum = np.full((N, N), 0.27)                         # 地面（株のすきま）は暗い緑
height = np.full((N, N), -1.0)
tufts_ = []
for gy in range(N // 8):
    for gx in range(N // 16):
        x = gx * 16 + (8 if gy % 2 else 0) + (rnd(gx, gy, 1) - 0.5) * 4
        y = gy * 8 + (rnd(gx, gy, 2) - 0.5) * 2
        tufts_.append((y, x, hn(gx, gy, 3)))
tufts_.sort()


def put(x, y, l, hgt):
    x %= N; y %= N
    lum[y, x] = l
    height[y, x] = hgt


for (by, bx, seed) in tufts_:
    # 根もとの影（だ円）
    for dy in range(-1, 3):
        for dx in range(-8, 9):
            if (dx / 8.5) ** 2 + (dy / 2.2) ** 2 <= 1:
                xx, yy = int(bx + dx) % N, int(by + dy + 1) % N
                lum[yy, xx] = min(lum[yy, xx], 0.12)
    nb = 6 + seed % 2
    for k in range(nb):
        t = (k + 0.5) / nb - 0.5                     # -0.5（左）〜 0.5（右）
        lean = t * 1.4 + (rnd(seed, k, 5) - 0.5) * 0.25
        hgt = 10 + rnd(seed, k, 6) * 4 - abs(t) * 5  # まんなかの葉ほど高い
        x0 = bx + t * 9
        for i in range(int(hgt) + 1):
            f = i / max(1.0, hgt)
            xx = x0 + lean * hgt * f * f * 0.9        # 先へ行くほど外へしなる
            yy = by - i
            l = 0.3 + 0.55 * f                        # 根もとは暗く、先は明るい
            l += -0.18 * lean                         # 左へかたむく葉は光を受ける
            if i == int(hgt):
                l += 0.08                             # 葉先の光
            put(int(round(xx)), int(round(yy)), l, f)
            if f < 0.6:
                put(int(round(xx)) + 1, int(round(yy)), l - 0.07, f)   # 根もと側は2ドットの太さ（先へ細くなる）
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
        # 葉先に、ときどき小さな花・穂
        if height[y, x] > 0.95 and hn(x, y, 33) % 41 == 0:
            c = ["#f4f0e0", "#e8d07a", "#d8a0b8"][hn(x, y, 5) % 3]
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
