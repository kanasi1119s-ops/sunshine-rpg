"""全体フィールド（世界地図）の地面のテクスチャを、町の飾り（木・樽・塀など）になじむよう描きなおす
（2026-10-06、人間の指示「ドット絵、フィールド系、地面系今までのオブジェクトになじむように、リアル感、光加減、
ドットの細かさ奥行きすべて意識して作って」「フィールド地面系ね」）。

前のテクスチャ（tools/pixel-art/ai-gen/world_tiles.py）は、3〜5色の平らな色に点を散らしたもので、
新しい立体の飾り（左上からの光・色相のずれ・細かいドット）とくらべて、のっぺりしていた。ここでは、地面ごとに

  1. くり返してもつなぎ目の出ない、ゆるい起伏（大・中・小の重ね）を作り、
  2. その起伏に左上から光を当てて（左上を向いた面は明るく、右下を向いた面は暗く）、
  3. 草の株・小石・砂の波紋・雪のふきだまり・ひび割れなど、その地面らしい細かなものを、1つずつ光と影つきで置き、
  4. 明るい所は黄色寄り、暗い所は青寄りの色の段（色相のずれ）で塗る。深い影の中はディザを使わない。

書き出し: tools/pixel-art/ground-terrain.json（export-game-data.mjs が world-terrain.json のあとに読み込み、同じ名前の絵を置きかえる）と、
確認用の ground-*.txt / pal-ground-*.json（エディタ用）。128×128、上下左右がつながる。"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
S = 128
L = np.array([-0.62, -0.62, 0.48])           # 光（左上の手前から）
L = L / np.linalg.norm(L)


def hn(*a):
    n = 2166136261
    for v in a:
        n = ((n ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    n ^= n >> 15
    return n


def rnd(*a):
    return (hn(*a) & 0xFFFF) / 65535


def vnoise(g, seed):
    """g×g の格子の値を、なめらかにつないだノイズ（128 で周期的）。"""
    grid = np.array([[rnd(i, j, seed) for i in range(g)] for j in range(g)])
    ys, xs = np.mgrid[0:S, 0:S]
    fx, fy = xs * g / S, ys * g / S
    x0, y0 = np.floor(fx).astype(int), np.floor(fy).astype(int)
    tx, ty = fx - x0, fy - y0
    tx, ty = tx * tx * (3 - 2 * tx), ty * ty * (3 - 2 * ty)
    x1, y1 = (x0 + 1) % g, (y0 + 1) % g
    x0, y0 = x0 % g, y0 % g
    a = grid[y0, x0] * (1 - tx) + grid[y0, x1] * tx
    b = grid[y1, x0] * (1 - tx) + grid[y1, x1] * tx
    return a * (1 - ty) + b * ty


def fbm(seed, octs=((4, 0.5), (8, 0.25), (16, 0.15), (32, 0.1))):
    return sum(vnoise(g, seed + k) * w for k, (g, w) in enumerate(octs))


def relief(h, k=1.0):
    """高さの場に、左上から光を当てた明るさ（-1〜1 くらい）。"""
    dx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) * 0.5 * k
    dy = (np.roll(h, -1, 0) - np.roll(h, 1, 0)) * 0.5 * k
    n = np.stack([-dx, -dy, np.ones_like(h)], -1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    return (n @ L) - L[2]


BAYER = np.array([[0.125, 0.625], [0.875, 0.375]])


def quant(v, ramp, x, y, dither=True):
    """0〜1 の明るさを、色の段へ。段の境目だけ市松でまぜる（暗い所ではまぜない）。"""
    f = np.clip(v, 0, 0.999) * (len(ramp) - 1)
    k = int(f)
    fr = f - k
    if dither and k >= 2 and 0.4 < fr < 0.6 and BAYER[y % 2, x % 2] < 0.5:
        k += 1
    elif fr >= 0.6:
        k += 1
    return ramp[min(len(ramp) - 1, k)]


class Img:
    def __init__(self):
        self.v = np.zeros((S, S))
        self.over = {}                        # (x,y) -> 色（そのまま置く細かな物）

    def put(self, x, y, c):
        self.over[(x % S, y % S)] = c


def to_colors(img, ramp, dither=True):
    out = np.full((S, S), "", dtype=object)
    for y in range(S):
        for x in range(S):
            out[y, x] = img.over.get((x, y)) or quant(img.v[y, x], ramp, x, y, dither)
    return out


# ------------------------------------------------------------------ 草原
GRASS = ["#26402a", "#2e4b2c", "#37572f", "#416433", "#4b7137", "#567e3b", "#628a40", "#6f9646", "#7da24d", "#8dae56", "#a0bb62"]


def blades(img, seed, cell, hmin, hmax, base_dv=-0.12, tip_dv=0.2, density=1.0):
    """草の株（2〜4本の葉）。根もとは暗く、先は明るい。株の右下に小さな影。"""
    for gy in range(S // cell):
        for gx in range(S // cell):
            if rnd(gx, gy, seed, 1) > density:
                continue
            x = gx * cell + int(rnd(gx, gy, seed, 2) * cell)
            y = gy * cell + int(rnd(gx, gy, seed, 3) * cell)
            hgt = hmin + int(rnd(gx, gy, seed, 4) * (hmax - hmin + 1))
            nb = 2 + hn(gx, gy, seed, 5) % 2
            img.v[(y + 1) % S, (x + 1) % S] -= 0.1                       # 株の右下の影
            for b in range(nb):
                lean = (b - (nb - 1) / 2) * 0.9 + (rnd(gx, gy, b, seed) - 0.5) * 0.6
                for i in range(hgt):
                    f = i / max(1, hgt - 1)
                    px = int(round(x + lean * f * f * 1.6))
                    py = y - i
                    dv = base_dv + (tip_dv - base_dv) * f - 0.05 * lean     # 左へかたむく葉は光を受ける
                    img.v[py % S, px % S] += dv


def grass_tex(seed=11, hills=False):
    img = Img()
    macro = fbm(seed)
    h = macro * 5 + vnoise(16, seed + 9) * 0.8
    if hills:
        # なだらかな丘: 大きなふくらみを、ずらした格子に（ふくらみの左上は明るく、右下はかげる）
        ys, xs = np.mgrid[0:S, 0:S]
        for k, (cx, cy, rx, ry) in enumerate([(28, 26, 34, 20), (96, 40, 36, 22), (40, 92, 36, 20), (104, 106, 30, 18)]):
            for ox in (-S, 0, S):
                for oy in (-S, 0, S):
                    d = ((xs - cx - ox) / rx) ** 2 + ((ys - cy - oy) / ry) ** 2
                    h += np.where(d < 1, (np.cos(np.sqrt(np.clip(d, 0, 1)) * math.pi) + 1) * 6.5, 0)
    img.v = 0.5 + (macro - 0.5) * 0.4 + relief(h, 1.0) * 0.5
    blades(img, seed, 3, 2, 3, base_dv=-0.07, tip_dv=0.09)
    blades(img, seed + 50, 6, 3, 5, base_dv=-0.12, tip_dv=0.2, density=0.55)
    # 小さな花と小石（ごく少し）
    for k in range(26):
        x, y = hn(k, seed, 71) % S, hn(k, seed, 72) % S
        if k % 3 == 0:
            img.put(x, y, "#8a8478"); img.put(x + 1, y, "#b4ae9e"); img.put(x, y + 1, GRASS[1])   # 小石（左上が明るい）
        else:
            c = ["#e8e4d0", "#e6cf6a", "#c9a0c8", "#e8e4d0"][k % 4]
            img.put(x, y, c); img.put(x, y + 1, GRASS[3])
    return to_colors(img, GRASS, dither=False)   # 草の株がこまかな模様になるので、市松のまぜは使わない


# ------------------------------------------------------------------ 道（ふみ固めた土）
ROAD = ["#4a3322", "#5a3f29", "#6b4c31", "#7c5a39", "#8d6842", "#9d774c", "#ad8758", "#bc9866", "#caa976"]


def road_tex(seed=21):
    img = Img()
    macro = fbm(seed)
    h = macro * 5 + vnoise(16, seed + 3) * 1.0 + vnoise(64, seed + 4) * 0.25
    img.v = 0.55 + (macro - 0.5) * 0.35 + relief(h) * 0.5
    # 小石: 左上が明るく、右下に影
    for k in range(110):
        x, y = hn(k, seed, 1) % S, hn(k, seed, 2) % S
        big = k % 4 == 0
        img.put(x, y, "#b8a48a" if big else "#a08a70")
        if big:
            img.put(x + 1, y, "#8c7860"); img.put(x, y + 1, "#7a6650"); img.put(x + 1, y + 1, ROAD[1])
        else:
            img.put(x + 1, y + 1, ROAD[2])
    # 細いひび（ところどころ）
    for k in range(10):
        x, y = hn(k, seed, 5) % S, hn(k, seed, 6) % S
        for i in range(3 + hn(k, 7) % 4):
            x += 1 if hn(k, i, 8) % 3 else 0
            y += 1 if hn(k, i, 9) % 2 else 0
            img.put(x, y, ROAD[1])
    return to_colors(img, ROAD)


# ------------------------------------------------------------------ 砂（風の波紋）
SAND = ["#9a7c50", "#ad8f5e", "#bfa06c", "#cdb07a", "#d9be88", "#e3cb96", "#ecd8a6", "#f4e4b8", "#faefcc"]


def sand_tex(seed=31):
    img = Img()
    ys, xs = np.mgrid[0:S, 0:S]
    warp = (fbm(seed) - 0.5) * 14
    # 波紋: 斜めの縞（周期 128 でつながるよう、xs と ys の整数倍）。風上側はゆるく、風下側は急
    ph = (xs * 2 + ys * 6) / S * 2 * math.pi * 1.5 + warp * 0.6
    rip = np.sin(ph) + 0.35 * np.sin(2 * ph + 0.8)
    h = rip * 1.4 + fbm(seed + 5) * 6
    img.v = 0.58 + relief(h, 1.0) * 0.75 + (fbm(seed + 9) - 0.5) * 0.25
    for k in range(120):                                               # 砂つぶ
        x, y = hn(k, seed, 1) % S, hn(k, seed, 2) % S
        img.put(x, y, SAND[8] if k % 3 else SAND[2])
    return to_colors(img, SAND)


# ------------------------------------------------------------------ 雪（ふきだまり）
SNOW = ["#7e94b0", "#91a7c2", "#a5b9d2", "#b7c9df", "#c8d7e9", "#d7e3f1", "#e4edf7", "#eff5fb", "#f8fbfe"]


def snow_tex(seed=41):
    img = Img()
    ys, xs = np.mgrid[0:S, 0:S]
    h = fbm(seed) * 9
    # ふきだまり: 横長のふくらみ（右下に青いかげ）
    for k in range(9):
        cx, cy = hn(k, seed, 1) % S, hn(k, seed, 2) % S
        rx, ry = 18 + hn(k, seed, 3) % 14, 6 + hn(k, seed, 4) % 5
        for ox in (-S, 0, S):
            for oy in (-S, 0, S):
                d = ((xs - cx - ox) / rx) ** 2 + ((ys - cy - oy) / ry) ** 2
                h += np.where(d < 1, (np.cos(np.sqrt(np.clip(d, 0, 1)) * math.pi) + 1) * 1.4, 0)
    img.v = 0.72 + relief(h, 1.1) * 0.6 + (fbm(seed + 3) - 0.5) * 0.12
    for k in range(40):                                                # きらめき
        img.put(hn(k, seed, 7) % S, hn(k, seed, 8) % S, "#ffffff")
    return to_colors(img, SNOW)


# ------------------------------------------------------------------ 荒れ地（ゆがみに侵された、むらさきがかった土）
WASTE = ["#251c2c", "#2f2438", "#3a2d44", "#463750", "#52425c", "#5f4e68", "#6c5a74", "#7a6882"]


def waste_tex(seed=51):
    img = Img()
    macro = fbm(seed)
    h = macro * 6 + vnoise(16, seed + 2) * 1.0
    img.v = 0.5 + (macro - 0.5) * 0.35 + relief(h) * 0.5
    # ひび割れ（乾いた土の多角形のひび）: 格子の点をずらし、となりの点を結ぶ
    pts = {}
    G = 16
    for j in range(S // G):
        for i in range(S // G):
            pts[(i, j)] = (i * G + int(rnd(i, j, seed) * 10), j * G + int(rnd(i, j, seed + 1) * 10))
    for (i, j), (x0, y0) in pts.items():
        for di, dj in ((1, 0), (0, 1)):
            if hn(i, j, di, seed) % 2 == 0:
                continue
            x1, y1 = pts[((i + di) % (S // G), (j + dj) % (S // G))]
            if di and x1 < x0:
                x1 += S
            if dj and y1 < y0:
                y1 += S
            n = max(abs(x1 - x0), abs(y1 - y0))
            for t in range(n + 1):
                x = round(x0 + (x1 - x0) * t / n)
                y = round(y0 + (y1 - y0) * t / n)
                img.put(x, y, WASTE[1])
                img.put(x + 1, y + 1, WASTE[5])                         # ひびの右下のふち（光を受ける）
    blades(img, seed, 10, 2, 3, base_dv=-0.15, tip_dv=0.1, density=0.35)  # 枯れた草
    return to_colors(img, WASTE)


# ------------------------------------------------------------------ 灰の地（火山のまわり）
ASH = ["#170b1d", "#211028", "#2c1734", "#381f42", "#452850", "#53325e", "#623d6c"]


def ash_tex(seed=61):
    img = Img()
    macro = fbm(seed)
    h = macro * 6 + vnoise(64, seed + 2) * 1.2
    img.v = 0.45 + (macro - 0.5) * 0.4 + relief(h) * 0.5
    for k in range(60):                                                # 火山の小石（左上が明るい）
        x, y = hn(k, seed, 1) % S, hn(k, seed, 2) % S
        img.put(x, y, ASH[6]); img.put(x + 1, y + 1, ASH[0])
        if k % 4 == 0:
            img.put(x + 1, y, ASH[5]); img.put(x, y + 1, ASH[2])
    for k in range(14):                                                # まだ温かい、おき火の点
        img.put(hn(k, seed, 5) % S, hn(k, seed, 6) % S, "#c0501e" if k % 3 else "#f08a2c")
    return to_colors(img, ASH, dither=False)


TEX = {
    "terrain:w-grass": grass_tex,
    "terrain:w-hills": lambda: grass_tex(13, hills=True),
    "terrain:w-road": road_tex,
    "terrain:w-sand": sand_tex,
    "terrain:w-snow": snow_tex,
    "terrain:w-waste": waste_tex,
    "terrain:w-ash": ash_tex,
}


def encode(img):
    cols = sorted(set(img.flatten().tolist()))
    idx = [cols.index(img[y, x]) for y in range(S) for x in range(S)]
    if len(cols) > 26:
        toks = []; prev = None; n = 0
        for k in idx:
            if k == prev:
                n += 1
            else:
                if prev is not None:
                    toks.append(f"{prev}:{n}")
                prev, n = k, 1
        toks.append(f"{prev}:{n}")
        return cols, "~" + ",".join(toks)

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
    return cols, "".join(out)


if __name__ == "__main__":
    allj = {}
    syms = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    for key, fn in TEX.items():
        img = fn()
        cols, rle = encode(img)
        allj[key] = {"size": S, "palette": cols, "rle": rle}
        name = "ground-" + key.split(":")[1]
        cmap = {c: syms[i] for i, c in enumerate(cols)}
        open(os.path.join(HERE, name + ".txt"), "w").write("\n".join("".join(cmap[c] for c in r) for r in img) + "\n")
        json.dump({cmap[c]: c for c in cols}, open(os.path.join(HERE, "pal-" + name + ".json"), "w"))
        print(key, len(cols), "colors")
    # 森（w-forest）は形はそのままに、色だけを新しい木（tree2d.py）と同じ色の段へ（暗い所は青寄り、明るい所は黄色寄り）。
    # 草原が落ちついた色になったので、前のあざやかな緑のままだと森だけが浮いて見えた
    wt = json.load(open(os.path.join(ROOT, "tools", "pixel-art", "world-terrain.json")))
    forest = dict(wt["terrain:w-forest"])
    FOREST = ["#14241c", "#1a2c22", "#1e3328", "#2b4a34", "#3b6236", "#557f3a", "#7ea447"]
    lum = lambda c: 0.3 * int(c[1:3], 16) + 0.59 * int(c[3:5], 16) + 0.11 * int(c[5:7], 16)
    order = sorted(range(len(forest["palette"])), key=lambda i: lum(forest["palette"][i]))
    pal = list(forest["palette"])
    for rank, i in enumerate(order):
        pal[i] = FOREST[round(rank * (len(FOREST) - 1) / max(1, len(order) - 1))]
    forest["palette"] = pal
    allj["terrain:w-forest"] = forest
    print("terrain:w-forest", pal)
    json.dump(allj, open(os.path.join(ROOT, "tools", "pixel-art", "ground-terrain.json"), "w"))
