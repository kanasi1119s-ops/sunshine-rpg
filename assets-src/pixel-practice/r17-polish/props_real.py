"""町の小さな飾りを、細かく写実的に描きなおす（2026-10-06、人間の指示「町にある岩、樽、箱、花壇、もっとリアルなものにして。ドット絵細かくして」
「井戸とか樽とか影は薄く自然な形で」）。すべて一から自作。光は左上。

  rock      岩: でこぼこした形を高さの地図から作り、面ごとに光と影、ひび、上にこけ、足もとに小石
  barrel    樽: ふくらんだ丸い胴を、板（たが板）ごとに明るさをかえ、板のすき間、鉄のたが4本（光る線とびょう）、上は丸いふた（板とふち）
  crates    木箱の山: 箱を立体（正面・上の面・右の面）で3つ。板・すみの枠・ななめの筋かい・くぎ、横に麻袋
  flowerbed 花壇: 木の植木箱（正面の板・上のふち・土）に、葉と、花びらのある花（赤・黄・白・紫・桃）

影: 地面に落ちる影は、まっ黒の帯ではなく、うすく透ける楕円（まん中は少しこく、ふちはうすい。光が左上なので少し右下へ）。
    色は "#rrggbbaa"（最後の2けたが不透明さ）。ゲームの絵のしくみ（sprite.ts）が透ける色に対応した。
大きさ・置き場所は前の絵（townprops.py / smallprops.py）と同じ（48×48 の枠、下そろえ）。町の重なりを見る箱（town-tidy.ts）も前のまま。
書き出し: <名前>.txt / pal-<名前>.json（このフォルダ。rock は rock2 の名前で上書き）。
使い方: python3 props_real.py [rock barrel crates flowerbed shadows]
  shadows: ほかの飾り（井戸・街灯・道しるべ・木・茂み）の、まっ黒な影の帯を、同じうすい楕円の影にかえる（その .txt / pal を書きかえる）。"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 48
SHADOW_CORE = "#10201860"
SHADOW_EDGE = "#10201830"


def hn(*a):
    n = 2166136261
    for v in a:
        n = ((n ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    n ^= n >> 15
    return n


def noise2(x, y, s, seed):
    """なめらかな値のノイズ（0〜1）"""
    xi, yi = math.floor(x / s), math.floor(y / s)
    fx, fy = x / s - xi, y / s - yi

    def v(a, b):
        return (hn(a, b, seed) & 0xFFFF) / 65535

    def sm(t):
        return t * t * (3 - 2 * t)
    a = v(xi, yi) + (v(xi + 1, yi) - v(xi, yi)) * sm(fx)
    b = v(xi, yi + 1) + (v(xi + 1, yi + 1) - v(xi, yi + 1)) * sm(fx)
    return a + (b - a) * sm(fy)


class Pic:
    def __init__(self):
        self.g = [["."] * W for _ in range(H)]
        self.pal = {}
        self.keys = {}

    def k(self, hexc):
        if hexc not in self.keys:
            sym = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"[len(self.keys)]
            self.keys[hexc] = sym
            self.pal[sym] = hexc
        return self.keys[hexc]

    def put(self, x, y, hexc):
        x, y = int(x), int(y)
        if 0 <= x < W and 0 <= y < H:
            self.g[y][x] = self.k(hexc)

    def get(self, x, y):
        x, y = int(x), int(y)
        return self.g[y][x] if 0 <= x < W and 0 <= y < H else "."

    def hexat(self, x, y):
        c = self.get(x, y)
        return None if c == "." else self.pal[c]

    def outline(self, dark, light=None):
        """外のりんかく。上と左（光の側）は light（あれば）、下と右は dark。"""
        add = []
        for y in range(H):
            for x in range(W):
                if self.g[y][x] != "." or self.pal.get(self.g[y][x], "").startswith("#1020"):
                    continue
                nb = [(dx, dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if self.get(x + dx, y + dy) != "." and not self.hexat(x + dx, y + dy).startswith("#1020")]
                if nb:
                    lit = light and all(d in ((1, 0), (0, 1)) for d in nb)
                    add.append((x, y, light if lit else dark))
        for x, y, c in add:
            self.put(x, y, c)

    def shadow(self, cx, cy, rx, ry):
        """地面の影（うすく透ける楕円）。絵のない所だけに置く。"""
        for y in range(int(cy - ry - 1), int(cy + ry + 2)):
            for x in range(int(cx - rx - 1), int(cx + rx + 2)):
                d = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2
                if d > 1 or self.get(x, y) != ".":
                    continue
                if d < 0.45:
                    self.put(x, y, SHADOW_CORE)
                elif d < 0.8 or (x + y) % 2 == 0:
                    self.put(x, y, SHADOW_EDGE)

    def save(self, name):
        with open(os.path.join(HERE, name + ".txt"), "w") as f:
            f.write("\n".join("".join(r) for r in self.g) + "\n")
        used = set("".join("".join(r) for r in self.g)) - {"."}
        with open(os.path.join(HERE, "pal-" + name + ".json"), "w") as f:
            json.dump({k: v for k, v in self.pal.items() if k in used}, f)


def ramp(cols, t):
    t = max(0.0, min(0.999, t))
    return cols[int(t * len(cols))]


# ===================================================================== 岩
def rock():
    p = Pic()
    STONE = ["#3e3a44", "#55505c", "#6c6774", "#86818c", "#a29ea6", "#bebac0", "#d8d6da"]
    MOSS = ["#3e5a2a", "#56783a", "#74964a"]
    cx, base = 24, 45
    # 高さの地図: いくつかのふくらみ（大きな岩と、右うしろの小さな岩）
    lumps = [(23, 38, 11.5, 7.5, 1.0), (31, 41, 6.5, 4.6, 0.75), (15, 42, 5.0, 3.4, 0.55)]
    Hm = {}
    for y in range(26, base + 1):
        for x in range(8, 41):
            h = 0
            for (lx, ly, rx, ry, a) in lumps:
                # ふちだけ少しでこぼこ（形はひとかたまりのまま）
                rr = rx * (1 + (noise2(x, y, 5, 7) - 0.5) * 0.18)
                d = ((x + 0.5 - lx) / rr) ** 2 + ((y + 0.5 - ly) / ry) ** 2
                if d < 1:
                    h = max(h, a * math.sqrt(1 - d))
            if h > 0 and y <= base:
                Hm[(x, y)] = h
    # 面: 大きな面（角ばった岩肌）を作るため、高さに、ゆるい折れ目を足してから向きを見る
    def hh(x, y):
        if (x, y) not in Hm:
            return 0
        return Hm[(x, y)] + 0.12 * abs(((x * 0.6 + y) % 9) / 9 - 0.5) + (noise2(x, y, 4, 9) - 0.5) * 0.08
    for (x, y), h in Hm.items():
        hx = hh(x + 1, y) - hh(x - 1, y)
        hy = hh(x, y + 1) - hh(x, y - 1)
        lum = 0.42 + hx * 1.5 + hy * 1.3 + h * 0.3          # 左や上を向く面（左上の光の方）ほど明るい
        lum = round(lum * 5) / 5
        if y >= base - 1:
            lum -= 0.2
        p.put(x, y, ramp(STONE, lum))
    # ひび（暗い線）と、ひびのふちの光
    for (sx, sy, dx, n) in ((20, 33, 1, 7), (28, 37, -1, 5)):
        x, y = sx, sy
        for i in range(n):
            if (x, y) in Hm:
                p.put(x, y, STONE[0])
                if (x - 1, y) in Hm:
                    p.put(x - 1, y, STONE[5])
            y += 1
            x += dx if hn(i, sx) % 2 else 0
    # こけ（上を向いた面の、明るい所に）
    for (x, y), h in Hm.items():
        up = Hm.get((x, y - 1), 0) < h - 0.08 or (x, y - 1) not in Hm
        if up and noise2(x, y, 3, 3) > 0.68 and y < 40:
            p.put(x, y, MOSS[1 + (hn(x, y) % 2)])
            if (x, y + 1) in Hm and hn(x, y, 5) % 3 == 0:
                p.put(x, y + 1, MOSS[0])
    p.outline("#24202a")
    # 足もとの小石
    for (x, y) in ((38, 44), (39, 45), (10, 45), (35, 46)):
        if p.get(x, y) == ".":
            p.put(x, y, STONE[3]); p.put(x + 1, y, STONE[1])
    p.shadow(cx + 3, base + 0.5, 15, 2.6)
    p.save("rock2")


# ===================================================================== 樽
WOOD = ["#2a170c", "#422412", "#5e3519", "#7c4824", "#9a5e31", "#b8783f", "#d29654"]
IRON = ["#24262c", "#3e424c", "#5e636e", "#868c98", "#b4bac4", "#e4e8ee"]


def barrel():
    p = Pic()
    cx = 24
    top, bot = 20, 44
    for y in range(top, bot + 1):
        t = (y - top) / (bot - top)
        hw = 9.2 + 2.0 * math.sin(math.pi * t)
        for x in range(int(cx - hw), int(cx + hw) + 1):
            nx = (x + 0.5 - cx) / (hw + 0.5)
            if abs(nx) > 1:
                continue
            th = math.asin(max(-1, min(1, nx)))
            lum = 0.42 + 0.42 * math.cos(th + 0.75) - 0.08 * t
            stave = math.floor((th + 1.6) / 0.36)
            lum += ((hn(stave, 3) % 5) - 2) * 0.035          # 板ごとに少し色がちがう
            if (th + 1.6) / 0.36 - stave < 0.16:
                lum -= 0.22                                  # 板のすき間
            if abs(nx) > 0.93:
                lum -= 0.12
            if 0.18 < (nx + 1) / 2 < 0.26:
                lum += 0.12                                  # つやの線
            if hn(x, y, 9) % 23 == 0:
                lum -= 0.1                                   # 木目
            p.put(x, y, ramp(WOOD, lum))
    # 鉄のたが（上下2本ずつ）
    for hy in (23, 27, 37, 41):
        t = (hy - top) / (bot - top)
        hw = 9.2 + 2.0 * math.sin(math.pi * t)
        for x in range(int(cx - hw), int(cx + hw) + 1):
            nx = (x + 0.5 - cx) / (hw + 0.5)
            if abs(nx) > 1:
                continue
            th = math.asin(max(-1, min(1, nx)))
            lum = 0.4 + 0.5 * math.cos(th + 0.75)
            p.put(x, hy, ramp(IRON, lum + 0.1))
            p.put(x, hy + 1, ramp(IRON, lum - 0.25))
            if hn(x, hy) % 6 == 0 and abs(nx) < 0.8:
                p.put(x, hy, IRON[5] if nx < 0 else IRON[3])   # びょう
    # 栓（横の小さな穴）
    p.put(cx + 3, 32, WOOD[0]); p.put(cx + 4, 32, WOOD[1]); p.put(cx + 3, 31, WOOD[4])
    # ふた（だ円）: ふち（チャイム）と、板、まんなかの合わせ目
    rx, ry = 9.2, 3.2
    for y in range(int(top - ry) - 1, top + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            d = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - top) / ry) ** 2
            if d > 1:
                continue
            if d > 0.62:
                c = WOOD[5] if (y < top or x < cx) else WOOD[3]   # ふち
                if y >= top and x >= cx:
                    c = WOOD[2]
            else:
                lum = 0.55 - (x - cx) * 0.02
                if (y - top) % 2 == 0:
                    lum -= 0.12
                c = ramp(WOOD, lum)
            p.put(x, y, c)
    for y in range(int(top - ry) + 1, top + 1):
        if p.get(cx, y) != ".":
            p.put(cx, y, WOOD[2])
    p.outline("#1a0f08")
    p.shadow(cx + 3, bot + 1.8, 13, 2.8)
    p.save("barrel")


# ===================================================================== 木箱の山
CRATE = ["#2c1c10", "#46301a", "#644626", "#846034", "#a47c46", "#c49a5c", "#dcb878"]


def crate(p, x0, ybot, w, h, dep, seed):
    """立体の木箱。正面 (x0..x0+w-1, ybot-h+1..ybot)、上の面と右の面は奥へ（右上へ 0.5 の傾き）。"""
    yt = ybot - h + 1
    # 右の面
    for i in range(1, dep + 1):
        x = x0 + w - 1 + i
        for y in range(int(yt - i * 0.5), int(ybot - i * 0.5) + 1):
            k = 2 if (y - yt) % 4 else 1
            if i == dep:
                k = 1
            p.put(x, y, CRATE[k])
    # 上の面
    for i in range(1, dep + 1):
        y = int(round(yt - i * 0.5))
        for x in range(x0 + i, x0 + w + i):
            k = 5 if (x - x0 - i) % 4 else 4
            if x - x0 - i in (0, 1) or x == x0 + w - 1 + i:
                k = 6 if x - x0 - i in (0, 1) else 4
            p.put(x, y, CRATE[k])
    # 正面: 板（横）と、すみの枠、ななめの筋かい
    for y in range(yt, ybot + 1):
        for x in range(x0, x0 + w):
            u, v = x - x0, y - yt
            frame = u <= 1 or u >= w - 2 or v <= 1 or v >= h - 2
            if frame:
                k = 5 if (u <= 1 or v <= 1) else 2
                if u == 0 or v == 0:
                    k = 6 if not (u == w - 1 or v == h - 1) else 3
            else:
                k = 3 if (v - 2) % 3 else 2                  # 板と板のすき間
                if hn(x, y, seed) % 13 == 0:
                    k = 4
                d = abs((u - 1) * (h - 3) / (w - 3) - (v - 1))
                if d < 1.0:
                    k = 4                                    # 筋かい（光）
                elif d < 1.8 and (u - 1) * (h - 3) / (w - 3) < (v - 1):
                    k = 1                                    # 筋かいの影
            p.put(x, y, CRATE[k])
    for (u, v) in ((1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2)):
        p.put(x0 + u, yt + v, "#2a2a30")                     # くぎ
        p.put(x0 + u - 1, yt + v - 1, "#c8ccd4") if u == 1 and v == 1 else None


def crates():
    p = Pic()
    crate(p, 9, 45, 14, 13, 4, 1)
    crate(p, 23, 45, 13, 12, 4, 2)
    crate(p, 12, 32, 13, 12, 4, 3)
    # 麻袋（右の箱にもたれる）
    SACK = ["#5a4a30", "#7a6646", "#9a8460", "#b8a27c", "#d2bc94"]
    for y in range(33, 46):
        for x in range(34, 45):
            nx, ny = (x + 0.5 - 39.5) / 5.4, (y + 0.5 - 40) / 6.3
            d = nx * nx + ny * ny
            if d > 1 or p.get(x, y) != "." and y < 44:
                continue
            lum = 0.6 - nx * 0.35 - ny * 0.15 - d * 0.2
            if (x * 3 + y) % 5 == 0:
                lum -= 0.08                                  # 布目
            if abs(nx + 0.2 - ny * 0.4) < 0.08:
                lum -= 0.2                                   # しわ
            p.put(x, y, ramp(SACK, lum))
    for x in range(37, 42):
        p.put(x, 34, SACK[0])                                # しばったひも
    p.put(39, 33, SACK[3]); p.put(40, 32, SACK[2])
    p.outline("#1a120a")
    p.shadow(27, 46.6, 19, 2.6)
    p.save("crates")


# ===================================================================== 花壇
def flowerbed():
    p = Pic()
    x0, x1 = 8, 40
    BOX = ["#3a2412", "#56361c", "#74502a", "#946a3a", "#b4884c"]
    SOIL = ["#2e2016", "#44301e", "#5a4028"]
    LEAF = ["#244a1e", "#356a28", "#4c8a34", "#6aaa44", "#8ec85a"]
    # 植木箱の正面（板2枚）と上のふち、奥のふち
    for y in range(41, 47):
        for x in range(x0, x1 + 1):
            v = y - 41
            k = 3 if v in (0, 3) else 2
            if v == 2 or v == 5:
                k = 1                                         # 板のすき間・下の影
            if x in (x0, x0 + 1):
                k = 4 if v != 5 else 2
            if x in (x1 - 1, x1):
                k = 1
            if hn(x, y, 4) % 11 == 0 and k in (2, 3):
                k -= 1                                        # 木目
            p.put(x, y, BOX[k])
    for x in range(x0, x1 + 1):
        p.put(x, 40, BOX[4]); p.put(x, 38, BOX[2])
    for y in (38, 39, 40):
        p.put(x0, y, BOX[4]); p.put(x1, y, BOX[1])
    for x in range(x0 + 1, x1):
        p.put(x, 39, SOIL[hn(x, 39) % 3])
    for x in (x0 + 10, x0 + 21):                              # 板のつなぎの金具
        p.put(x, 42, "#5e636e"); p.put(x, 45, "#5e636e")
    # 葉（ふちから上へ、ふさふさ）
    for x in range(x0 + 1, x1):
        hgt = 2 + hn(x, 1) % 3
        for k in range(hgt):
            y = 39 - k
            lum = 0.3 + k * 0.18 + (0.15 if hn(x, k) % 3 == 0 else 0) - (x - x0) * 0.004
            p.put(x, y, ramp(LEAF, lum))
    # 花（花びら4つ＋まんなか。色と高さをかえる）
    FL = [("#e04848", "#a02828", "#f4d040"), ("#f4d040", "#c09820", "#c06020"), ("#f4f0ec", "#c8c0c0", "#e8c040"),
          ("#a060d0", "#6a3a98", "#f4e080"), ("#f08cb0", "#c05a80", "#f4e080")]
    xs = list(range(x0 + 3, x1 - 1, 4))
    for i, fx in enumerate(xs):
        fx += hn(i, 2) % 2
        fy = 35 - hn(i, 3) % 2
        petal, dark, mid = FL[hn(i, 5) % len(FL)]
        for (dx, dy) in ((0, -1), (-1, 0), (1, 0), (0, 1)):
            p.put(fx + dx, fy + dy, petal if (dx <= 0 and dy <= 0) else dark)
        p.put(fx, fy, mid)
        p.put(fx, fy + 2, LEAF[1]); p.put(fx, fy + 3, LEAF[2])     # くき
    p.outline("#1c140c")
    p.shadow(25, 47.2, 19, 1.8)
    p.save("flowerbed")


# ===================================================================== ほかの飾りの影を、うすい楕円に
def soften_shadows(name, palname=None):
    """名前.txt の、まっ黒な影の色（前の作り方の "S"）を消して、うすい楕円の影に置きかえる。"""
    path = os.path.join(HERE, name + ".txt")
    rows = [list(l) for l in open(path).read().split("\n") if l]
    palpath = os.path.join(HERE, "pal-" + (palname or name) + ".json")
    pal = json.load(open(palpath))
    sk = [k for k, v in pal.items() if k == "S"]
    if not sk:
        return False
    cells = [(x, y) for y, r in enumerate(rows) for x, c in enumerate(r) if c == "S"]
    if not cells:
        return False
    xs = [c[0] for c in cells]; ys = [c[1] for c in cells]
    for (x, y) in cells:
        rows[y][x] = "."
    hgt, wid = len(rows), len(rows[0])
    cx = (min(xs) + max(xs) + 1) / 2 + 1.5
    cy = (min(ys) + max(ys) + 1) / 2 + 0.3
    rx = (max(xs) - min(xs) + 1) / 2 + 1
    ry = max(1.6, (max(ys) - min(ys) + 1) / 2 + 0.6)
    pal["S"] = SHADOW_CORE
    pal["Z"] = SHADOW_EDGE if "Z" not in pal else pal["Z"]
    edge = "Z" if pal["Z"] == SHADOW_EDGE else None
    if edge is None:
        for cand in "0123456789":
            if cand not in pal:
                edge = cand; pal[cand] = SHADOW_EDGE; break
    for y in range(int(cy - ry - 1), int(cy + ry + 2)):
        for x in range(int(cx - rx - 1), int(cx + rx + 2)):
            if not (0 <= x < wid and 0 <= y < hgt) or rows[y][x] != ".":
                continue
            d = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2
            if d > 1:
                continue
            if d < 0.45:
                rows[y][x] = "S"
            elif d < 0.8 or (x + y) % 2 == 0:
                rows[y][x] = edge
    open(path, "w").write("\n".join("".join(r) for r in rows) + "\n")
    json.dump(pal, open(palpath, "w"))
    return True


if __name__ == "__main__":
    todo = sys.argv[1:] or ["rock", "barrel", "crates", "flowerbed", "shadows"]
    for n in todo:
        if n == "shadows":
            for other, pn in (("well", None), ("lamp", None), ("signpost", None), ("tree4", "tree"), ("bush2", None)):
                print(other, soften_shadows(other, pn))
        else:
            globals()[n]()
            print(n, "ok")
