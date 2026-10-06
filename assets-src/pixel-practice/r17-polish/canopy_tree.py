"""町の草むら（terrain:forest。128×128、上下左右がつながる）を、新しい木（tree2d.py）と同じ描き方で作りなおす
（2026-10-06、人間の指示「これを基準に草むらも作ってみて」）。

木の樹冠と同じく、葉のかたまり（カリフラワーのような、ふちが小さくでこぼこした丸）をびっしり重ね、
  - かたまりごとに、左上から光を当てる（左上の頭が明るく、右下と底が暗い）
  - となりの、より手前に出ているかたまりが、左上から影を落とす（重なりの下に暗い帯）
  - かたまりのすき間は、いちばん暗い青みの緑（奥の暗い葉）
  - 色は明るい所ほど黄色寄り、暗い所ほど青寄り。深い影の中はまぜない。光を受けた葉に小さな照り、ごく少しの花
町の芝（terrain:grass-a、#496d36〜#6a8f48）とまざる所（ground-decor.ts の canopyBlend）でなじむよう、
まんなかの明るさは芝と同じくらいにする。
書き出し: canopy.txt / pal-canopy.json（エディタで確かめる）と、tools/pixel-art/canopy-terrain.json（ゲーム用）。
前の作り方（細い葉の株）は canopy3d.py に残してある。"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
N = 128
LEAF = ["#1c3026", "#243d2e", "#2e4c32", "#395c35", "#456b38", "#527a3c", "#608842", "#70964a", "#84a754", "#9cb862", "#b4c972"]
L = np.array([-0.55, -0.62, 0.56])
L = L / np.linalg.norm(L)


def hn(*a):
    n = 2166136261
    for v in a:
        n = ((n ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    n ^= n >> 15
    return n


def rnd(*a):
    return (hn(*a) & 0xFFFF) / 65535


# かたまり: ずらした格子に大きめ、そのあいだに小さめ
clumps = []
for gy in range(N // 8):
    for gx in range(N // 11 + 1):
        x = (gx * 11 + (5.5 if gy % 2 else 0) + (rnd(gx, gy, 1) - 0.5) * 5) % N
        y = (gy * 8 + (rnd(gx, gy, 2) - 0.5) * 4) % N
        clumps.append((x, y, 4.6 + rnd(gx, gy, 3) * 2.2, 2.0 + rnd(gx, gy, 4) * 3.0))
for k in range(80):
    clumps.append((rnd(k, 11) * N, rnd(k, 12) * N, 2.6 + rnd(k, 13) * 1.5, 3.5 + rnd(k, 14) * 2.5))

hgt = np.full((N, N), -1e9)
own = np.full((N, N), -1, dtype=int)
nrm = np.zeros((N, N, 3))
for i, (cx, cy, r, z) in enumerate(clumps):
    lobes = max(4, int(r / 1.4))
    for oy in range(int(-r - 2), int(r + 3)):
        for ox in range(int(-r - 2), int(r + 3)):
            px, py = int(math.floor(cx + ox)) % N, int(math.floor(cy + oy)) % N
            dx, dy = math.floor(cx + ox) + 0.5 - cx, math.floor(cy + oy) + 0.5 - cy
            ang = math.atan2(dy, dx)
            re = r * (1 + 0.1 * math.sin(ang * lobes + i * 1.3) + 0.05 * math.sin(ang * (2 * lobes + 1) + i))
            d = math.hypot(dx, dy) + (rnd(px, py, 9) - 0.5) * 0.6
            if d >= re:
                continue
            h = z + math.sqrt(re * re - d * d)
            if h > hgt[py, px]:
                hgt[py, px] = h
                own[py, px] = i
                lx, ly = dx / re, dy / re
                nrm[py, px] = (lx, ly, math.sqrt(max(0.0, 1 - lx * lx - ly * ly)))

lum = np.zeros((N, N))
for y in range(N):
    for x in range(N):
        if own[y, x] < 0:
            lum[y, x] = 0.14                                       # すき間（奥の暗い葉。暗すぎると芝の中で穴に見える）
            continue
        n = nrm[y, x] / max(1e-6, np.linalg.norm(nrm[y, x]))
        v = 0.26 + 0.66 * max(0.0, float(n @ L))
        v -= 0.12 * max(0.0, n[1])                                   # かたまりの底は暗い
        for s in (1, 2, 3, 4):                                       # 左上の、より手前のかたまりが落とす影
            qx, qy = (x - round(s * 0.6)) % N, (y - s) % N
            if own[qy, qx] >= 0 and own[qy, qx] != own[y, x] and hgt[qy, qx] > hgt[y, x] + 0.6 + s * 0.4:
                v -= 0.26 if s <= 2 else 0.18
                break
        v += ((hn(x // 2, y // 2, 3) % 5) - 2) * 0.015               # 葉のかたまりのむら
        lum[y, x] = v

TH = [0.08, 0.17, 0.26, 0.34, 0.42, 0.5, 0.58, 0.67, 0.77, 0.88]
img = np.full((N, N), "", dtype=object)
for y in range(N):
    for x in range(N):
        v = lum[y, x]
        k = sum(v > t for t in TH)
        if 3 <= k < 10 and v - TH[k - 1] < 0.02 and (x + y) % 2 == 0:
            k -= 1                                                    # 段の境目だけ市松（暗い所ではまぜない）
        if k in (6, 7, 8) and hn(x, y, 51) % 9 == 0:
            k += 1                                                    # 光を受けた葉の小さな照り
        elif k in (3, 4, 5) and hn(x, y, 52) % 11 == 0:
            k -= 1                                                    # 葉と葉のあいだの小さな暗がり
        img[y, x] = LEAF[min(10, k)]
# ごく少しの小さな花（光の当たるかたまりの上だけ）
for k in range(18):
    x, y = hn(k, 61) % N, hn(k, 62) % N
    if own[y, x] >= 0 and lum[y, x] > 0.55:
        img[y, x] = ["#f2eedc", "#e8cf6c", "#d9a4c4"][k % 3]
        img[(y + 1) % N, x] = LEAF[4]

cols = sorted(set(img.flatten().tolist()))
syms = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
cmap = {c: syms[i] for i, c in enumerate(cols)}
open(os.path.join(HERE, "canopy.txt"), "w").write("\n".join("".join(cmap[img[y, x]] for x in range(N)) for y in range(N)) + "\n")
json.dump({cmap[c]: c for c in cols}, open(os.path.join(HERE, "pal-canopy.json"), "w"))


def b36(v):
    s = ""
    while v:
        s = "0123456789abcdefghijklmnopqrstuvwxyz"[v % 36] + s
        v //= 36
    return s


idx = [cols.index(img[y, x]) for y in range(N) for x in range(N)]
out = []
prev = None
n = 0
for k in idx + [None]:
    if k == prev:
        n += 1
        continue
    if prev is not None:
        out.append(chr(65 + prev) + (b36(n) if n > 1 else ""))
    prev, n = k, 1
assert len(cols) <= 26
json.dump({"terrain:forest": {"size": N, "palette": cols, "rle": "".join(out)}}, open(os.path.join(ROOT, "tools", "pixel-art", "canopy-terrain.json"), "w"))
print("ok colors", len(cols))
