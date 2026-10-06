"""町の草むら（terrain:forest。128×128、上下左右がつながる）を、「草」として描きなおす（2026-10-06、人間の指示「草作り直し」）。
前の版（canopy_tree.py）は、新しい木と同じ丸い葉のかたまりで描いたので、草ではなく木の茂みに見えた。
ここでは、細い葉が根もとから扇のように立ち上がる「草の株」を、新しい木と同じ光の考え方で描く。

  - 株全体を1つのふくらみ（ドーム）として、左上から光を当てる（左の葉・上の葉先が明るく、右と根もとが暗い）
  - 葉は1本ずつ。根もとは太く（2ドット）先は細く、外の葉ほど外へしなる。まんなかの葉ほど手前（あとに描く）
  - 葉が、右うしろの葉に細い影を落とす（葉と葉が分かれて見える）
  - 手前（下）の株が、奥の株の根もとをかくす（奥行き）。株の根もとの地面に、やわらかい影
  - 色は新しい木と同じ考え方: 明るい所ほど黄色寄り、暗い所ほど青寄り。地面（すき間）は町の芝と同じ明るさ
  - 葉先に、ごく少しの穂と小さな花
書き出し: canopy.txt / pal-canopy.json と、tools/pixel-art/canopy-terrain.json（ゲーム用）。"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
N = 128
LEAF = ["#1c3026", "#243d2e", "#2e4c32", "#395c35", "#456b38", "#527a3c", "#608842", "#70964a", "#84a754", "#9cb862", "#b4c972"]
LAWN = ["#3d5f30", "#466a35", "#4f7239", "#577d3e", "#5e8441", "#658b45", "#6e924b", "#7a9c52"]   # 町の芝（terrain:grass-a）に合わせた段
GROUND = 0.47                       # 地面（株のすき間）の明るさ。町の芝（#496d36〜#6a8f48）と同じくらい
L = np.array([-0.62, -0.55, 0.56])
L = L / np.linalg.norm(L)


def hn(*a):
    n = 2166136261
    for v in a:
        n = ((n ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    n ^= n >> 15
    return n


def rnd(*a):
    return (hn(*a) & 0xFFFF) / 65535


def make(scale, lawnlike=False, front=False):
    """scale: 草の高さの倍率（1=ふつう。しげみの端ほど小さい絵を使う）。株の並びはどれも同じ。"""
    global blade_id
    lum = np.full((N, N), GROUND)
    lum += (np.array([[hn(x // 3, y // 2, 1) % 5 for x in range(N)] for y in range(N)]) - 2) * 0.012   # 芝のこまかなむら
    owner = np.full((N, N), -1, dtype=int)       # どの葉の点か（葉の影をつけるため）
    tip = np.zeros((N, N), dtype=bool)

    tufts = []
    for gy in range(N // 7):
        for gx in range(N // 12):
            x = gx * 12 + (6 if gy % 2 else 0) + (rnd(gx, gy, 1) - 0.5) * 5
            y = gy * 7 + (rnd(gx, gy, 2) - 0.5) * 3
            tufts.append((y, x, hn(gx, gy, 3)))
    tufts.sort()                                    # 奥（上）から手前（下）へ

    blade_id = 0
    for (by, bx, seed) in tufts:
        if lawnlike and seed % 5 >= 3:
            continue                                # 芝に近い所は、株をまばらに
        rx = (5.5 + (seed % 7) * 0.45) * (0.65 + 0.35 * scale)   # 株の横の広がり
        H = (10 + (seed >> 3) % 5) * scale           # 株の高さ（端ほど低い）
        # 根もとの地面の影（やわらかい、横長）
        for dy in range(-1, 3):
            for dx in range(-int(rx) - 2, int(rx) + 3):
                e = (dx / (rx + 1.5)) ** 2 + ((dy - 0.5) / 1.8) ** 2
                if e < 1:
                    xx, yy = int(bx + dx + 1) % N, int(by + dy) % N
                    if owner[yy, xx] < 0:
                        lum[yy, xx] = min(lum[yy, xx], GROUND - (0.2 * (1 - e) + 0.05) * (0.4 + 0.6 * scale))
        nb = 9 + seed % 4
        order = sorted(range(nb), key=lambda k: -abs((k + 0.5) / nb - 0.5))   # 外の葉から（奥）、まんなかの葉はあと（手前）
        for k in order:
            u = ((k + 0.5) / nb - 0.5) * 2           # -1（左）〜 1（右）
            lean = u * 1.15 + (rnd(seed, k, 5) - 0.5) * 0.35
            h = H * (1 - 0.38 * u * u) * (0.82 + rnd(seed, k, 6) * 0.3)
            x0 = bx + u * rx * 0.55
            tone = (rnd(seed, k, 7) - 0.5) * 0.08
            blade_id += 1
            prev = None
            for i in range(int(h) + 1):
                t = i / max(1.0, h)
                px = x0 + lean * h * t * t * 0.55
                py = by - i
                xi, yi = int(round(px)) % N, int(py) % N
                # 株全体のふくらみ（ドーム）の向き → 左上の光
                nx = (px - bx) / (rx + 3)
                ny = -(0.25 + 0.75 * t)
                n = np.array([nx, ny, max(0.15, 1 - abs(nx))])
                n /= np.linalg.norm(n)
                v = 0.13 + 0.56 * max(0.0, float(n @ L))
                v += 0.16 * t - 0.2 * (1 - t) ** 1.5 + tone        # 葉先は明るく、根もとは暗い
                v -= 0.06 * lean                              # 左へかたむく葉は光を受ける
                if i == int(h):
                    v += 0.07
                cells = [(xi, yi)]
                if t < 0.5:
                    cells.append(((xi + 1) % N, yi))          # 根もと側は2ドットの太さ
                for j, (cx, cy) in enumerate(cells):
                    lum[cy, cx] = v - (0.05 if j == 1 else 0)
                    owner[cy, cx] = blade_id
                    tip[cy, cx] = i == int(h)
                # 葉が、右となりの（先に描いた）葉に落とす細い影
                sx = (cells[-1][0] + 1) % N
                if 0 <= owner[yi, sx] < blade_id and owner[yi, sx] > blade_id - nb - 2:
                    lum[yi, sx] -= 0.11

    TH = [0.1, 0.18, 0.26, 0.33, 0.4, 0.465, 0.53, 0.6, 0.69, 0.8]
    img = np.full((N, N), "", dtype=object)
    for y in range(N):
        for x in range(N):
            v = lum[y, x]
            k = sum(v > t for t in TH)
            c = LEAF[min(10, k)]
            if front and owner[y, x] < 0:
                continue                                  # 葉だけの絵（木の根元の手前に重ねる）。地面は透かす
            if lawnlike:
                # 2026-10-06「この低いしげみの草が少ない部分、もっと芝のドットに近い感じにして」:
                # 地面は透かして、下の町の芝の絵をそのまま見せる。株の根もとの影はうすく透ける色。葉は芝と同じ色合いの段で
                if owner[y, x] < 0:
                    img[y, x] = "#1830184a" if v < GROUND - 0.1 else ("#18301826" if v < GROUND - 0.04 else "")
                    continue
                c = LAWN[min(len(LAWN) - 1, max(0, int((v - 0.12) / 0.62 * len(LAWN))))]
            if tip[y, x] and hn(x, y, 41) % 23 == 0:
                c = ["#e8d898", "#f2eedc", "#e6cf6a", "#d9a4c4"][hn(x, y, 42) % 4]   # 穂・小さな花
            img[y, x] = c

    return img


OUTS = {}
for key, sc in (("terrain:forest", 1.0), ("terrain:forest-mid", 0.62), ("terrain:forest-low", 0.34), ("terrain:forest-front", 0.62)):   # 木の根元の手前の草は、中くらいの高さ（少しだけかくす）
    blade_id = 0
    OUTS[key] = make(sc, lawnlike=key.endswith("-low"), front=key.endswith("-front"))
img = OUTS["terrain:forest"]
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


def encode(im):
    cs = sorted(set(im.flatten().tolist()))
    assert len(cs) <= 26
    cs = [c for c in cs if c]
    idx = [cs.index(im[y, x]) if im[y, x] else -1 for y in range(N) for x in range(N)]
    out = []
    prev = None
    n = 0
    for k in idx + [None]:
        if k == prev:
            n += 1
            continue
        if prev is not None:
            out.append(("_" if prev < 0 else chr(65 + prev)) + (b36(n) if n > 1 else ""))
        prev, n = k, 1
    return {"size": N, "palette": cs, "rle": "".join(out)}


for key, nm in (("terrain:forest-mid", "canopy-mid"), ("terrain:forest-low", "canopy-low"), ("terrain:forest-front", "canopy-front")):    # エディタで確かめる用
    im = OUTS[key]
    cs = sorted({c for c in im.flatten().tolist() if c})
    cm = {c: syms[i] for i, c in enumerate(cs)}
    cm[""] = "."
    open(os.path.join(HERE, nm + ".txt"), "w").write("\n".join("".join(cm[im[y, x]] for x in range(N)) for y in range(N)) + "\n")
    json.dump({cm[c]: c for c in cs if c}, open(os.path.join(HERE, "pal-" + nm + ".json"), "w"))
json.dump({k: encode(v) for k, v in OUTS.items()}, open(os.path.join(ROOT, "tools", "pixel-art", "canopy-terrain.json"), "w"))
print("ok colors", len(cols))
