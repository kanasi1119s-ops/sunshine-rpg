"""全体フィールド（世界地図）の地形テクスチャ（128×128・つなぎ目なしで繰り返せる）を作る（2026-10-04）。

人間が用意した全体フィールドの見本の絵（明るい草原、丸い木が密集した森、灰色のごつごつした岩山、茶色のとがった山、
波模様の青い海、雪原と雪をかぶった針葉樹、砂の波紋）の「質の要素」を、型と乱数で描き直したもの。見本の絵は写していない。
ゲームはこの128×128から、マスの位置にあたる16×16を切り出して描く（隣のマスと絵がつながる）。

使い方: python3 world_tiles.py 出力フォルダ
  出力: <名前>.png（確認用）・<名前>.txt と <名前>.json（エディタ用）・world-terrain.json（ゲーム用。export-game-data.mjs が読み込む）
"""
import json
import math
import os
import random
import sys

import numpy as np
from PIL import Image

S = 128


def hx(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


class Tex:
    def __init__(self, base):
        self.g = np.zeros((S, S), np.int16)
        self.pal = [hx(base)]

    def col(self, c):
        c = hx(c)
        if c not in self.pal:
            self.pal.append(c)
        return self.pal.index(c)

    def put(self, x, y, c):
        self.g[y % S, x % S] = self.col(c) if isinstance(c, str) else c

    def get(self, x, y):
        return self.g[y % S, x % S]


def speckle(t, rng, colors, n, size=1):
    for _ in range(n):
        x, y = rng.randrange(S), rng.randrange(S)
        c = rng.choice(colors)
        for dy in range(size):
            for dx in range(size):
                t.put(x + dx, y + dy, c)


def tufts(t, rng, light, dark, n):
    """草の房（ハの字の葉先）。"""
    for _ in range(n):
        x, y = rng.randrange(S), rng.randrange(S)
        t.put(x, y, dark)
        t.put(x - 1, y - 1, light); t.put(x + 1, y - 1, light); t.put(x, y - 1, light)


def grass():
    rng = random.Random(1)
    t = Tex("#58a83a")
    speckle(t, rng, ["#4e9c34", "#62b240"], 900, 2)
    tufts(t, rng, "#86cc52", "#3e8a2c", 260)
    speckle(t, rng, ["#3e8a2c"], 120)
    return t


def hills():
    t = grass()
    rng = random.Random(2)
    for _ in range(26):
        cx, cy = rng.randrange(S), rng.randrange(S)
        w, h = rng.choice([(9, 5), (11, 6), (7, 4)])
        for yy in range(-h, 1):
            half = int(w * math.sqrt(max(0, 1 - (yy / h) ** 2)))
            for xx in range(-half, half + 1):
                c = "#78c04a" if (xx < 0 and yy < -1) else "#5aa63c"
                if yy == 0 or abs(xx) == half:
                    c = "#3a7a2a"
                t.put(cx + xx, cy + yy, c)
        t.put(cx - half // 2, cy - h + 1, "#9ad86a")
    return t


def crowns(t, rng, pts, r, cols, outline, ground=None):
    """丸い樹冠を、上から順に重ねて描く（下の木が上の木に重なる）。cols: 暗→明の4色。"""
    for (cx, cy) in sorted(pts, key=lambda p: p[1]):
        for yy in range(-r - 1, r + 2):
            for xx in range(-r - 1, r + 2):
                d = math.hypot(xx + 0.3, yy + 0.3)
                if d > r + 0.5:
                    continue
                if d > r - 0.6 and (yy > -r // 2):
                    c = outline
                else:
                    lt = (-xx - yy) / (2 * r)          # 左上ほど明るい
                    k = 1 + (lt > 0.15) + (lt > 0.45) - (yy > r * 0.45)
                    c = cols[max(0, min(3, k))]
                t.put(cx + xx, cy + yy, c)
        t.put(cx - r // 2, cy - r // 2, cols[3])
        if ground:
            t.put(cx, cy + r + 1, ground)


def lattice(rng, dx, dy, jit):
    pts = []
    nx, ny = max(1, round(S / dx)), max(1, round(S / dy))
    ny += ny % 2                                     # 互い違いの段がつなぎ目でずれないよう偶数段
    fx, fy = S / nx, S / ny                          # 128 を割り切る間隔にして、つなぎ目にすき間を作らない
    for j in range(ny):
        for i in range(nx):
            x = int(i * fx + (fx / 2 if j % 2 else 0)) + rng.randint(-jit, jit)
            y = int(j * fy) + rng.randint(-jit, jit)
            pts.append((x % S, y % S))
    return pts


def forest():
    rng = random.Random(3)
    t = Tex("#123a16")
    speckle(t, rng, ["#0e3012"], 400, 2)
    crowns(t, rng, lattice(rng, 9, 7, 1), 5, ["#1c5a22", "#28742a", "#3a9034", "#62b04a"], "#0c2a10")
    return t


def rocks(t, rng, pts, cols, outline, w=(6, 10), h=(5, 8)):
    """ごつごつした岩のかたまり。輪郭は暗い1ドット、左上の面が明るく、右下が暗い（3段＋光の縁）。cols: 暗→明の4色。"""
    for (cx, cy) in sorted(pts, key=lambda p: p[1]):
        rw, rh = rng.randint(*w), rng.randint(*h)
        # 角ばった形: 8方向の半径を少しずつ変えた多角形
        rad = [rng.uniform(0.75, 1.05) for _ in range(8)]
        def inside(xx, yy):
            a = math.atan2(yy / rh, xx / rw) % (2 * math.pi)
            k = a / (2 * math.pi) * 8; i0 = int(k) % 8; f = k - int(k)
            r = rad[i0] * (1 - f) + rad[(i0 + 1) % 8] * f
            return (xx / rw) ** 2 + (yy / rh) ** 2 <= r * r
        cells = [(xx, yy) for yy in range(-rh - 1, rh + 2) for xx in range(-rw - 1, rw + 2) if inside(xx, yy)]
        cs = set(cells)
        for (xx, yy) in cells:
            edge = any((xx + dx, yy + dy) not in cs for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if edge and (yy >= -rh // 3 or xx > 0):
                c = outline
            elif edge:
                c = cols[3]                                   # 左上の縁に光
            else:
                v = -xx / rw - yy / rh                        # 左上ほど明るい
                c = cols[2] if v > 0.35 else cols[1] if v > -0.45 else cols[0]
            t.put(cx + xx, cy + yy, c)
        x0 = cx + rng.randint(-rw // 3, rw // 3)              # 割れ目（右下へ）
        for s_ in range(rng.randint(2, 4)):
            t.put(x0 + s_ // 2, cy + s_, outline)


def mountain():
    rng = random.Random(4)
    t = Tex("#5c5c64")
    rocks(t, rng, lattice(rng, 12, 9, 2), ["#727280", "#9696a2", "#babac4", "#e2e2e8"], "#383842", w=(5, 8), h=(6, 9))
    return t


def peaks():
    """高峰（山の中心部）: 山より大きく暗い岩が重なる（見本の絵では山はほぼ灰色の岩）。"""
    rng = random.Random(5)
    t = Tex("#4a4a54")
    rocks(t, rng, lattice(rng, 14, 10, 2), ["#5a5a66", "#7a7a86", "#9e9eaa", "#c6c6d0"], "#2c2c36", w=(8, 12), h=(6, 9))
    for (cx, cy) in lattice(random.Random(55), 28, 22, 4):   # ところどころ雪をかぶった頂
        for xx in range(-2, 3):
            t.put(cx + xx, cy, "#eef2f8")
        t.put(cx, cy - 1, "#ffffff"); t.put(cx - 1, cy + 1, "#c8d4e4"); t.put(cx + 1, cy + 1, "#c8d4e4")
    return t


def pyramids():
    """茶色のとがった山（左の面が明るく、右の面が暗い）。今は使っていない（見本の一部の地方用の予備）。"""
    rng = random.Random(5)
    t = Tex("#6a5034")
    speckle(t, rng, ["#5a4228"], 300, 2)
    pts = lattice(rng, 14, 11, 2)
    for (cx, cy) in sorted(pts, key=lambda p: p[1]):
        hgt = rng.randint(10, 13); half = hgt
        for yy in range(hgt + 1):
            wd = int(half * yy / hgt)
            for xx in range(-wd, wd + 1):
                if xx == -wd or xx == wd or yy == hgt:
                    c = "#3a2818"
                elif xx < 0:
                    c = "#e2c48c" if xx > -wd * 0.45 and yy < hgt * 0.7 else "#c8a46c"
                elif xx == 0:
                    c = "#a07a48"
                else:
                    c = "#7e5c38" if xx < wd * 0.6 else "#5e4226"
                t.put(cx + xx, cy - hgt + yy, c)
        t.put(cx, cy - hgt, "#f4e2b4")
    return t


def water(base, light, dark, seed, n):
    rng = random.Random(seed)
    t = Tex(base)
    speckle(t, rng, [dark], 500, 2)
    for _ in range(n):                                   # 波の光
        x, y = rng.randrange(S), rng.randrange(S)
        ln = rng.randint(2, 5)
        for k in range(ln):
            t.put(x + k, y, light)
        t.put(x + 1, y + 1, dark); t.put(x + ln - 2, y + 1, dark)
    return t


def sea():
    return water("#2456a4", "#5a8ad0", "#1c4890", 6, 170)


def lake():
    t = water("#3070c4", "#7ab0ea", "#2660b0", 7, 200)
    rng = random.Random(70)
    speckle(t, rng, ["#a8d0f4"], 60)
    return t


def sand(base="#e6d29a", light="#f6e8bc", dark="#cdb47c", seed=8):
    rng = random.Random(seed)
    t = Tex(base)
    for j in range(0, S, 6):                                # 砂の波紋
        ph = rng.uniform(0, 6.28)
        for x in range(S):
            y = j + int(2 * math.sin(x * 2 * math.pi / 32 + ph))
            t.put(x, y, light)
            if x % 3 != 0:
                t.put(x, y + 1, dark)
    speckle(t, rng, [dark, light], 300)
    return t


def ash():
    """灰の大地（虚灯宮のまわり）: 見本の絵では、暗い紫の渦。渦の腕を、つなぎ目なしでくり返す。"""
    rng = random.Random(17)
    t = Tex("#24102e")
    speckle(t, rng, ["#1a0a22", "#2e163a"], 900, 2)
    for (cx, cy) in [(32, 32), (96, 96), (96, 32), (32, 96)]:
        for arm in range(3):
            for k in range(140):
                a = k * 0.09 + arm * 2.094
                r = 2 + k * 0.2
                x, y = cx + r * math.cos(a), cy + r * math.sin(a)
                c = "#7a3a8c" if k % 9 < 5 else "#4e2260"
                if k > 110:
                    c = "#3a1848"
                t.put(int(x), int(y), c)
                t.put(int(x) + 1, int(y), "#9a5ab0" if k < 40 else c)
    return t


def snow():
    rng = random.Random(9)
    t = Tex("#e8f0f8")
    speckle(t, rng, ["#d4e2f0", "#ffffff"], 700, 2)
    speckle(t, rng, ["#b4cce2"], 160)
    return t


def snowforest():
    t = snow()
    rng = random.Random(10)
    for (cx, cy) in sorted(lattice(rng, 10, 9, 2), key=lambda p: p[1]):
        for tier in range(3):                              # 3段の針葉樹
            top = cy - 11 + tier * 3
            for yy in range(5):
                wd = 1 + yy * (tier + 2) // 4
                for xx in range(-wd, wd + 1):
                    if abs(xx) == wd:
                        c = "#3a5a7a"
                    elif yy <= 1 or xx < 0:
                        c = "#ffffff" if yy == 0 or xx < -wd // 2 else "#d6e8f4"
                    else:
                        c = "#8ab0cc"
                    t.put(cx + xx, top + yy, c)
        t.put(cx, cy + 1, "#5a4030"); t.put(cx, cy + 2, "#3a2a20")
    return t


def road():
    rng = random.Random(11)
    t = Tex("#a8703c")
    speckle(t, rng, ["#b8844c", "#946032"], 900, 2)
    speckle(t, rng, ["#7a4c26", "#cc9a60"], 260)
    return t


def cloud():
    rng = random.Random(12)
    t = Tex("#cfe0f2")
    for (cx, cy) in sorted(lattice(rng, 12, 9, 2), key=lambda p: p[1]):
        crowns(t, rng, [(cx, cy)], 5, ["#b6cce6", "#d6e4f4", "#eef4fc", "#ffffff"], "#a2bcdc")
    return t


def waste():
    rng = random.Random(13)
    t = Tex("#5c4e66")
    speckle(t, rng, ["#6a5c74", "#4c4056"], 900, 2)
    for _ in range(70):                                   # ひび
        x, y = rng.randrange(S), rng.randrange(S)
        for k in range(rng.randint(3, 7)):
            x += rng.choice([0, 1]); y += 1
            t.put(x, y, "#382c40")
    return t


def chasm():
    rng = random.Random(14)
    t = Tex("#2a1e2a")
    speckle(t, rng, ["#3a2c3a", "#1a121a"], 1200, 2)
    return t


def lava():
    rng = random.Random(15)
    t = Tex("#c8401a")
    speckle(t, rng, ["#a02a10", "#e05a1c"], 900, 2)
    for j in range(0, S, 8):
        ph = rng.uniform(0, 6.28)
        for x in range(S):
            y = j + int(3 * math.sin(x * 2 * math.pi / 64 + ph))
            t.put(x, y, "#ffb040")
            t.put(x, y + 1, "#f07a24")
    return t


TEXTURES = {
    "w-grass": grass, "w-hills": hills, "w-forest": forest, "w-mountain": mountain, "w-peaks": peaks,
    "w-sea": sea, "w-lake": lake, "w-sand": sand, "w-snow": snow, "w-snowforest": snowforest,
    "w-road": road, "w-cloud": cloud, "w-waste": waste, "w-chasm": chasm, "w-lava": lava, "w-ash": ash, "w-pyramids": pyramids,
}
NAMES = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode(g):
    s, prev, n = "", None, 0
    for row in g:
        for k in row:
            ch = NAMES[k]
            if ch == prev:
                n += 1
            else:
                if prev is not None:
                    s += prev + (np.base_repr(n, 36).lower() if n > 1 else "")
                prev, n = ch, 1
    s += prev + (np.base_repr(n, 36).lower() if n > 1 else "")
    return s


def main(out):
    os.makedirs(out, exist_ok=True)
    game = {}
    for name, fn in TEXTURES.items():
        t = fn()
        assert len(t.pal) <= 26, (name, len(t.pal))
        rgb = np.array(t.pal, np.uint8)[t.g]
        Image.fromarray(rgb).save(f"{out}/{name}.png")
        open(f"{out}/{name}.txt", "w").write("\n".join("".join(NAMES[k] for k in row) for row in t.g) + "\n")
        hexes = ["#%02x%02x%02x" % c for c in t.pal]
        json.dump({NAMES[i]: h for i, h in enumerate(hexes)}, open(f"{out}/{name}.json", "w"))
        game[f"terrain:{name}"] = {"size": S, "palette": hexes, "rle": encode(t.g)}
        print(name, len(t.pal), "色")
    json.dump(game, open(f"{out}/world-terrain.json", "w"))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "out")
