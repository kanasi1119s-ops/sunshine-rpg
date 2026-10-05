"""フィールドのアイコンの勉強・4回目（2026-10-05、人間の指示「別のバージョンでフィールドに違和感なく馴染む作り方でやってみてください」）。

1〜3回目は「アイコンとして目立つ絵」を描いた。4回目は反対に、**地図の地形（ぴぽや風の、やわらかく、縁どりのない、明るさの差の小さい絵）の
一部に見える**ことを目ざす。どれも一から考えたオリジナルの形で、ぴぽやの形も、今のゲームのアイコンの形もまねしない。
くわしくは docs/design/field-icons-study.md の「4回目の勉強（フィールドになじむ作り方）」。

4回目のきまり（なじませるきまり）
  N1. 色は、置く地面の地形の絵（assets-src/field/terrain/w-*.png）から取った色が中心。足す色（屋根・壁・灯）は少しだけで、
      あざやかさ（彩度）と明るさを、地形の色の幅の中におさめる
  N2. 黒い縁どりはしない。縁は「影の側（右と下）だけ、その素材のいちばん暗い色」。森の木のかたまりや山の岩のすき間と同じやり方
  N3. 面の模様のきめを、地形にそろえる（石＝山の岩の色と同じ4段、木＝森のかたまりと同じ6ドットの房、草＝草地の1ドットの葉）
  N4. 足もと: 地面の色の「すそ」と、地面の色を暗くした影を、ドットで描きこむ。建物の下のふちには草・雪・砂を手前にかぶせる。
      地面ごとに1枚（-grass / -snow / -sand）
  N5. 大きさ: 家は横 8〜12 ドット（森の木の房 7〜8 ドットの1.5倍くらい）。1つのアイコンは 3×3 マス（48 ドット）より小さめに収める
  N6. 光は地形と同じ左上
出力: *4.txt / pal-*4.json、study4-preview.png、study4-world.png
"""
import json
import math
import os
import random

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
TER = os.path.join(HERE, "..", "..", "field", "terrain")

# ===================================================================== 地形から取った色（N1）
GRASS = ["#3e8a2c", "#4e9c34", "#58a83a", "#62b240", "#86cc52"]            # w-grass（暗→明）
GSHADE = ["#2f6e24", "#3a7a2a"]                                              # 草の影（w-hills の暗い色＋さらに1段）
FOREST = ["#0c2a10", "#1c5a22", "#28742a", "#3a9034", "#62b04a"]           # w-forest の木の房
STONE = ["#383842", "#5c5c64", "#727280", "#9696a2", "#babac4", "#e2e2e8"]  # w-mountain の岩
DIRT = ["#7a4c26", "#946032", "#a8703c", "#b8844c", "#cc9a60"]             # w-road
SAND = ["#b39a62", "#cdb47c", "#e6d29a", "#f6e8bc"]                         # w-sand（いちばん暗い色だけ足した）
SNOW = ["#3a5a7a", "#8ab0cc", "#b4cce2", "#d4e2f0", "#e8f0f8", "#ffffff"]  # w-snow / w-snowforest
SNOWTREE = ["#24405a", "#3a5a7a", "#8ab0cc", "#d4e2f0", "#ffffff"]
SEA = ["#163c78", "#1c4890", "#2456a4", "#5a8ad0", "#a8d0f4"]               # w-sea / w-lake
# 足す色（少しだけ。あざやかさは地形の 0.6 前後、明るさは 30〜80 の中）
ROOF = ["#5a2a20", "#7e3a2a", "#a24e36", "#c06a48", "#d88c62"]             # 赤茶の瓦
SLATE = ["#2c3a52", "#3a4e6c", "#4e688c", "#6c88aa", "#94acc8"]             # 青い石板（城）
THATCH = ["#6e5228", "#8a6a36", "#a8864a", "#c4a260", "#dcc07c"]                       # わら（砂と道の色の間）
WALL = ["#8c7c64", "#b4a282", "#d6c8a6", "#ece2c6"]                         # しっくい
LIGHT = "#ffd878"
GLOW = ["#3a8aa8", "#7ad0e0", "#d8f8ff"]
GOLD = "#e0b850"


def texture(kind):
    return Image.open(os.path.join(TER, f"w-{kind}.png")).convert("RGB")


def hx(c):
    return "#%02x%02x%02x" % c


def h2(x, y, s=0):
    return ((x * 73856093) ^ (y * 19349663) ^ (s * 83492791)) & 0xFFFF


class Canvas:
    """色（#rrggbb）を直接ためる。mat は縁の処理のための素材の色の並び（None は地面のすそ＝縁の処理をしない）"""

    def __init__(self, w=48, h=48):
        self.w, self.h = w, h
        self.c = [[None] * w for _ in range(h)]
        self.m = [[None] * w for _ in range(h)]

    def put(self, x, y, col, mat=None):
        x, y = int(x), int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            self.c[y][x] = col
            self.m[y][x] = mat

    def get(self, x, y):
        return self.c[y][x] if 0 <= x < self.w and 0 <= y < self.h else None

    def shadow_edges(self):
        """N2: 透明に面した右・下のふちだけ、その素材のいちばん暗い色に。左・上のふちはそのまま（縁どりなし）"""
        out = [r[:] for r in self.c]
        for y in range(self.h):
            for x in range(self.w):
                mat = self.m[y][x]
                if self.c[y][x] is None or not mat:
                    continue
                if self.get(x + 1, y) is None or self.get(x, y + 1) is None:
                    out[y][x] = mat[0]
        self.c = out

    def reduce(self, limit=16):
        """色が多すぎるときは、いちばん近い2色を、よく使われるほうへまとめる（地形の色はそのまま残りやすい）"""
        def lab(h):
            r, g, b = [int(h[i:i + 2], 16) for i in (1, 3, 5)]
            return (0.3 * r + 0.59 * g + 0.11 * b, r - g, (r + g) / 2 - b)
        while True:
            cnt = {}
            for r in self.c:
                for v in r:
                    if v:
                        cnt[v] = cnt.get(v, 0) + 1
            if len(cnt) <= limit:
                return
            cols = list(cnt)
            # まず、地面のすその「地形と同じ色」どうしをまとめる（地面の細かな粒は2色でも見え方が変わらない。
            # 建物や森の色をまとめるより害が少ない）
            pure = set()
            for k in ("grass", "snow", "sand"):
                pure |= {hx(cc) for n, cc in texture(k).getcolors(65536)}
            pc = [cc for cc in cols if cc in pure]
            if len(pc) > 2:
                cols = pc
            prot = {LIGHT, GOLD, *GLOW}
            best = None
            for i in range(len(cols)):
                for j in range(i + 1, len(cols)):
                    if cols[i] in prot and cols[j] in prot:
                        continue
                    a, b = lab(cols[i]), lab(cols[j])
                    d = (a[0] - b[0]) ** 2 * 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2
                    if best is None or d < best[0]:
                        best = (d, cols[i], cols[j])
            _, a, b = best
            keep, drop = (a, b) if cnt[a] >= cnt[b] else (b, a)
            if drop in prot:
                keep, drop = drop, keep
            self.c = [[keep if v == drop else v for v in r] for r in self.c]

    def trim_ground(self, keep=1):
        """地形と同じ色だけの「すそ」は、建物・影・草のふさから keep ドットより遠い所をけずる（地図の上では見えないので、
        なくても同じ。重なりの測定でも、見えない地面が形に数えられなくなる）"""
        pure = set()
        for k in ("grass", "snow", "sand"):
            pure |= {hx(c) for n, c in texture(k).getcolors(65536)}
        core = {(x, y) for y in range(self.h) for x in range(self.w) if self.c[y][x] and self.c[y][x] not in pure}
        near = set(core)
        for _ in range(keep):
            near |= {(x + dx, y + dy) for (x, y) in near for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))}
        for y in range(self.h):
            for x in range(self.w):
                if self.c[y][x] in pure and (x, y) not in near:
                    self.c[y][x] = None

    def save(self, name, trim=True):
        if trim:
            self.trim_ground()
        self.reduce(16)
        used = sorted({v for r in self.c for v in r if v}, key=lambda h: sum(int(h[i:i + 2], 16) for i in (1, 3, 5)))
        letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        mp = {c: letters[i] for i, c in enumerate(used)}
        with open(os.path.join(HERE, f"{name}.txt"), "w") as f:
            f.write("\n".join("".join(mp[v] if v else "." for v in r) for r in self.c) + "\n")
        with open(os.path.join(HERE, f"pal-{name}.json"), "w") as f:
            json.dump({mp[c]: c for c in used}, f)
        return name, len(used)


# ===================================================================== 地面のすそと影（N4）
GROUND = {
    "grass": dict(tex="grass", sh=GSHADE, tuft=[GRASS[4], GRASS[3], GRASS[1]]),
    "snow": dict(tex="snow", sh=["#8ab0cc", "#b4cce2"], tuft=["#ffffff", "#e8f0f8", "#d4e2f0"]),
    "sand": dict(tex="sand", sh=["#b39a62", "#cdb47c"], tuft=["#f6e8bc", "#e6d29a", "#cdb47c"]),
}


def skirt(c, cx, cy, rx, ry, biome, seed=1):
    """建物のまわりの地面（地形の絵からそのまま色を取る）。ふちは、ハッシュでぎざぎざにして、地面にとけるように"""
    t = texture(GROUND[biome]["tex"])
    for y in range(int(cy - ry) - 2, int(cy + ry) + 3):
        for x in range(int(cx - rx) - 2, int(cx + rx) + 3):
            d = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2
            if d < 1 - 0.35 * (h2(x, y, seed) % 100) / 100:
                c.put(x, y, hx(t.getpixel((x % 128, y % 128))))


def contact_shadow(c, x0, x1, ybase, biome, depth=4, right=4):
    """建物の足もとの影: 下と右へのびる。建物に近いほど暗い（2段）。とちゅうは市松でまぜて、やわらかく"""
    sh = GROUND[biome]["sh"]
    for y in range(ybase, ybase + depth):
        k = y - ybase
        for x in range(x0 + k // 2, x1 + right - k + 1):
            if c.get(x, y) is None:
                continue
            far = (k >= depth // 2) or (x > x1 + right // 2)
            if far and (x + y) % 2 == 0 and k == depth - 1:
                continue
            c.put(x, y, sh[1] if far else sh[0])


def tufts(c, x0, x1, y, biome, seed=2, density=0.45):
    """建物の下のふちに、手前から地面（草の葉・雪の吹きだまり・砂）をかぶせる"""
    tl = GROUND[biome]["tuft"]
    rnd = random.Random(seed)
    for x in range(x0, x1 + 1):
        if rnd.random() < density:
            h = rnd.choice((1, 1, 2))
            for k in range(h):
                c.put(x, y - k, tl[0] if k == h - 1 else tl[1])
            c.put(x, y + 1, tl[2])
        elif biome != "grass" and rnd.random() < 0.6:
            c.put(x, y, tl[1])


# ===================================================================== 部品（N3: きめを地形にそろえる）
def tree(c, cx, cy, r=3.4, pal=FOREST):
    """森の地形の木の房と同じ作り（左上が明るく、右下に暗いすき間の色）。
    大きさも森の地形の房（はば 7〜8 ドット）にそろえるため、半径を 1.2 倍にする（1回目の見直しで、房が小さすぎて「しげみ」に見えた）"""
    r *= 1.2
    for y in range(int(cy - r) - 1, int(cy + r) + 2):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            u, v = (x + 0.5 - cx) / r, (y + 0.5 - cy) / r
            d = u * u + v * v
            if d > 1:
                continue
            s = u * 0.7 + v * 0.9
            col = pal[4] if s < -0.8 else pal[3] if s < -0.25 else pal[2] if s < 0.5 else pal[1]   # 森の地形の色の割合（明 23%・中 26%・暗 37%）に近づける
            if d > 0.7 and s > 0.6:
                col = pal[0]
            c.put(x, y, col, pal)


def pine(c, cx, yb, h=8, pal=SNOWTREE):
    """雪の森の地形と同じ、小さな針葉樹。からだは暗い青緑、枝の段の上に雪（左は白、右は青白）"""
    for y in range(yb - h, yb + 1):
        k = y - (yb - h)
        t = k / h
        half = 0.6 + t * 3.4 - (0.9 if k % 3 == 0 and k > 0 else 0)
        for x in range(int(cx - half - 1), int(cx + half) + 2):
            u = (x + 0.5 - cx) / max(0.6, half)
            if abs(u) > 1:
                continue
            col = pal[2] if u < 0.0 else pal[1]
            if k % 3 == 1 or k == 0:
                col = pal[4] if u < 0.2 else pal[3]                # 枝の上の雪
            c.put(x, y, col, pal)
    c.put(cx, yb + 1, "#5a4030", pal)


def stone_wall(c, x0, x1, y0, y1, pal=STONE, top=False, seed=0):
    """山の岩と同じ色の4段で、小さな石積み（3×2）。目地は2段目の色（いちばん暗い色は縁と影だけ）"""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            r = y - y0
            row = r // 2
            bx = (x - x0 + (row % 2) * 2 + seed) % 4
            col = pal[3]
            if r % 2 == 1:
                col = pal[2] if bx != 3 else pal[1]
            elif bx == 3:
                col = pal[1]
            elif bx == 0 and h2(x, y, seed) % 3 == 0:
                col = pal[4]                                     # 石の左上の光
            if x >= x1 - 1:
                col = pal[1] if col != pal[4] else pal[2]        # 右のふちは影
            if top and r == 0:
                col = pal[4] if x < x1 - 1 else pal[3]
            c.put(x, y, col, pal)


def roof_rows(c, x0, x1, y0, y1, pal, hip=True):
    """瓦の屋根: 2行ごとに明るい行。寄棟なら上の行ほど両はしをけずる。左が明るく右が暗い"""
    for y in range(y0, y1 + 1):
        k = y - y0
        cut = max(0, (y1 - y0 - k) // 2) if hip else 0
        cut = min(cut, (x1 - x0) // 2 - 1)
        for x in range(x0 + cut, x1 - cut + 1):
            t = (x - x0) / max(1, x1 - x0)
            i = 3 if t < 0.55 else 2
            if k % 2 == 1:
                i -= 1
            if x == x1 - cut:
                i = 1
            if k == 0:
                i = min(4, i + 1)
            c.put(x, y, pal[i], pal)
    for x in range(x0, x1 + 1):
        c.put(x, y1 + 1, pal[0], pal)                           # 軒の影


def house(c, x0, ybase, w=9, roof=ROOF, wall=WALL, hip=True, snow=False, door=True, lit=True):
    """小さな家。ybase は壁の下の行。屋根の高さは横はばの半分くらい"""
    x1 = x0 + w - 1
    rh = w // 2
    wh = 3
    wy0 = ybase - wh + 1
    roof_rows(c, x0, x1, wy0 - rh - 1, wy0 - 2, roof, hip)
    for y in range(wy0, ybase + 1):
        for x in range(x0, x1 + 1):
            c.put(x, y, wall[2] if x < x1 - 1 else wall[1], wall)
    if door:
        dx = x0 + w - 3
        c.put(dx, ybase, DIRT[0], wall); c.put(dx, ybase - 1, DIRT[1], wall)
    if lit:
        c.put(x0 + 1, wy0, LIGHT, wall)
    if snow:
        for x in range(x0, x1 + 1):
            yt = wy0 - rh - 1
            dep = 2 + (1 if (x - x0) % 4 in (1, 2) else 0)
            for y in range(yt, yt + dep):
                if c.get(x, y) in roof:
                    c.put(x, y, SNOW[5] if x < x1 - 2 else SNOW[3], SNOW)
            if c.get(x, yt + dep) in roof:
                c.put(x, yt + dep, SNOW[2], SNOW)


def road(c, pts, w=2, pal=DIRT, seed=4):
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]):
        n = max(abs(xb - xa), abs(yb - ya), 1)
        for k in range(n + 1):
            x = xa + (xb - xa) * k / n
            y = ya + (yb - ya) * k / n
            for dx in range(w):
                col = pal[2] if h2(int(x + dx), int(y), seed) % 5 else pal[3]
                if dx == w - 1:
                    col = pal[1]
                c.put(x + dx, y, col)


# ===================================================================== 町（草・雪）: 壁で囲まない。道ぞいの家と、森と同じ木
def town4(biome="grass"):
    c = Canvas()
    snow = biome == "snow"
    tp = SNOWTREE if snow else FOREST
    skirt(c, 24, 30, 22, 15, biome, seed=11)
    contact_shadow(c, 6, 40, 40, biome, depth=3, right=2)
    road(c, [(30, 47), (27, 38), (22, 31), (24, 22), (21, 12)], w=3, pal=SNOW[1:] if snow else DIRT)
    # 家（大きさと屋根をかえ、道の両側に互いちがい）
    plan = [(9, 18, 10, ROOF, True), (27, 16, 9, SLATE, False), (5, 30, 9, SLATE, True),
            (29, 28, 11, ROOF, True), (13, 39, 8, ROOF, False), (32, 40, 8, SLATE, True)]
    for (x0, yb, w, rf, hp) in sorted(plan, key=lambda p: p[1]):
        contact_shadow(c, x0 + 1, x0 + w, yb + 1, biome, depth=2, right=2)
        house(c, x0, yb, w, rf, hip=hp, snow=snow)
        tufts(c, x0, x0 + w - 1, yb + 1, biome, seed=x0)
    # 木（森の房と同じ。家のあいだと、はしに）
    for (x, y, r) in ((4, 15, 3.4), (40, 13, 3.6), (43, 25, 3.2), (19, 26, 3.0), (39, 34, 2.8), (6, 40, 3.0)):
        if snow:
            pine(c, x, int(y + r), int(r * 2.3))
        else:
            tree(c, x, y, r, tp)
    c.shadow_edges()
    return c.save(f"town4-{biome}")


# ===================================================================== お城: 小高い丘の上の、小さめのとりで。壁は丘の形にそい、四角い天守は左より、丸い塔は右
def castle4():
    c = Canvas()
    biome = "grass"
    skirt(c, 24, 37, 19, 8, biome, seed=21)
    # 丘（草の盛り上がり。地形の丘と同じく、上は明るく、下のふちに暗い草）
    for y in range(28, 46):
        for x in range(4, 45):
            d = ((x + 0.5 - 24) / 15.5) ** 2 + ((y + 0.5 - 38.5) / 5.5) ** 2
            if d <= 1:
                v = GRASS[3] if y < 36 else GRASS[2]
                if d > 0.8 and y > 38:
                    v = GSHADE[1]
                if (h2(x, y, 3) % 9) == 0:
                    v = GRASS[4] if y < 38 else GRASS[1]
                c.put(x, y, v)
    contact_shadow(c, 12, 36, 39, biome, depth=3, right=3)
    # 城の中（石だたみ）
    for y in range(27, 37):
        for x in range(12, 37):
            if ((x + 0.5 - 24.5) / 12.5) ** 2 + ((y + 0.5 - 32) / 5.5) ** 2 <= 1:
                c.put(x, y, STONE[3] if (x // 3 + y) % 3 else STONE[4], STONE)
    # 四角い天守（左より）
    roof_rows(c, 13, 22, 11, 16, SLATE, hip=True)
    stone_wall(c, 14, 22, 18, 31, seed=1)
    for (wx, wy) in ((16, 21), (19, 25)):
        c.put(wx, wy, STONE[0], STONE); c.put(wx, wy + 1, STONE[0], STONE)
    c.put(19, 26, LIGHT, STONE)
    # 丸い塔（右）
    for y in range(17, 33):
        for x in range(28, 35):
            u = (x + 0.5 - 31) / 3.6
            if abs(u) <= 1:
                col = STONE[4] if u < -0.4 else STONE[3] if u < 0.3 else STONE[2]
                if (y - 17) % 3 == 2:
                    col = STONE[2] if u < 0.3 else STONE[1]
                c.put(x, y, col, STONE)
    for y in range(11, 18):
        half = (y - 10) * 0.65
        for x in range(26, 37):
            u = (x + 0.5 - 31) / max(0.5, half)
            if abs(u) <= 1:
                c.put(x, y, SLATE[4] if u < -0.3 else SLATE[3] if u < 0.4 else SLATE[1], SLATE)
    c.put(30, 23, STONE[0], STONE); c.put(30, 24, LIGHT, STONE)
    c.put(31, 10, DIRT[0]); c.put(31, 9, DIRT[0]); c.put(32, 9, ROOF[3]); c.put(33, 9, ROOF[2])
    # 城壁（丘のふちにそう低い帯。手前だけ。胸壁は1ドットおき）
    for x in range(11, 38):
        yb = int(36 + 2.5 * math.sqrt(max(0, 1 - ((x + 0.5 - 24.5) / 13.5) ** 2)))
        for y in range(yb - 2, yb + 1):
            col = STONE[4] if y == yb - 2 else (STONE[3] if (x + y) % 4 else STONE[2])
            if x > 35:
                col = STONE[2] if y > yb - 2 else STONE[3]
            c.put(x, y, col, STONE)
        if x % 2 == 0:
            c.put(x, yb - 3, STONE[4] if x < 33 else STONE[3], STONE)
    for y in range(36, 40):
        for x in range(23, 26):
            c.put(x, y, STONE[0], STONE)
    road(c, [(23, 40), (21, 44), (23, 47)], w=3)
    for (x, y, r) in ((8, 35, 3.0), (40, 34, 3.2)):
        tree(c, x, y, r)
    tufts(c, 10, 38, 41, biome, seed=5, density=0.25)
    c.shadow_edges()
    return c.save("castle4")


# ===================================================================== 塔（64×112）: 海の岩場から立つ、細く高い古い塔。らせんの階段の帯と、てっぺんのやわらかな光
def spire4():
    c = Canvas(64, 112)
    t = texture("sea")
    # 岩場（山の岩と同じ色の房）
    rnd = random.Random(7)
    rocks = [(32 + rnd.uniform(-16, 16), 101 + rnd.uniform(-4, 5), rnd.uniform(3.5, 6)) for _ in range(14)]
    for (rx_, ry_, r) in sorted(rocks, key=lambda p: p[1]):
        for y in range(int(ry_ - r), int(ry_ + r) + 1):
            for x in range(int(rx_ - r), int(rx_ + r) + 1):
                u, v = (x + 0.5 - rx_) / r, (y + 0.5 - ry_) / (r * 0.8)
                d = u * u + v * v
                if d <= 1:
                    s = u * 0.7 + v
                    col = STONE[5] if s < -0.8 else STONE[4] if s < -0.2 else STONE[3] if s < 0.5 else STONE[2]
                    if d > 0.75 and s > 0.5:
                        col = STONE[0]
                    c.put(x, y, col, STONE)
    # 波（海の色の明るい2色だけ。岩のまわりに、とぎれとぎれ）
    for k in range(0, 360, 4):
        a = math.radians(k)
        x = 32 + math.cos(a) * 24
        y = 103 + math.sin(a) * 7
        if math.sin(a) > -0.2 and c.get(int(x), int(y)) is None and (k // 8) % 2 == 0:
            c.put(x, y, SEA[4]); c.put(x + 1, y, SEA[3])
    # 塔（下ほど少し太い。らせんの帯＝明るい石の斜めの線）
    for y in range(14, 100):
        half = 6.5 + (y - 14) * 0.035
        for x in range(16, 48):
            u = (x + 0.5 - 32) / half
            if abs(u) > 1:
                continue
            col = STONE[4] if u < -0.45 else STONE[3] if u < 0.25 else STONE[2] if u < 0.7 else STONE[1]
            if (y + int(u * 5)) % 14 in (0, 1):
                col = STONE[5] if u < 0 else STONE[3]           # らせんの帯
            elif (y // 3 + int((u + 1) * 3)) % 4 == 0 and (y % 3 == 0):
                col = STONE[2] if u < 0.25 else STONE[1]        # 石の目地（まばらに）
            c.put(x, y, col, STONE)
    for (wy, wx) in ((30, 29), (48, 34), (66, 28), (84, 33)):
        c.put(wx, wy, STONE[0], STONE); c.put(wx, wy + 1, STONE[0], STONE); c.put(wx, wy + 2, STONE[1], STONE)
    for y in range(92, 100):
        for x in range(30, 34):
            if y > 92 or x in (31, 32):
                c.put(x, y, STONE[0], STONE)
    # てっぺん（少し張り出す冠と、やわらかな光: 芯1色＋まわり1段、まわりの空気は塗らない）
    for y in range(8, 15):
        for x in range(23, 42):
            u = (x + 0.5 - 32) / 8.5
            if abs(u) <= 1 and (y > 9 or abs(u) < 0.8):
                c.put(x, y, STONE[4] if u < -0.3 else STONE[3] if u < 0.4 else STONE[2], STONE)
    for x in range(24, 41, 3):
        c.put(x, 7, STONE[4], STONE)
    for y in range(0, 8):
        for x in range(28, 37):
            d = ((x + 0.5 - 32) / 3.2) ** 2 + ((y + 0.5 - 4) / 3.8) ** 2
            if d <= 1:
                c.put(x, y, GLOW[2] if d < 0.35 else GLOW[1] if d < 0.75 else GLOW[0])
    c.shadow_edges()
    return c.save("spire4")


# ===================================================================== 洞窟: 横に長い岩の丘（山の地形と同じ岩の房）に、暗い口
def rock_hill(c, cx, cy, rx, ry, seed=3, n=26):
    rnd = random.Random(seed)
    rocks = []
    for _ in range(n):
        a = rnd.uniform(0, math.pi)
        rr = math.sqrt(rnd.random())
        rocks.append((cx + math.cos(a) * rx * rr * 0.9, cy - math.sin(a) * ry * rr * 0.9, rnd.uniform(3.2, 4.6)))
    for (px_, py_, r) in sorted(rocks, key=lambda p: p[1]):
        for y in range(int(py_ - r), int(py_ + r) + 1):
            for x in range(int(px_ - r * 1.15), int(px_ + r * 1.15) + 1):
                u, v = (x + 0.5 - px_) / (r * 1.15), (y + 0.5 - py_) / r
                d = u * u + v * v
                if d <= 1 and y <= cy:
                    s = u * 0.6 + v
                    col = STONE[5] if s < -0.85 else STONE[4] if s < -0.25 else STONE[3] if s < 0.45 else STONE[2]
                    if d > 0.72 and s > 0.35:
                        col = STONE[0]
                    c.put(x, y, col, STONE)


# ===================================================================== 洞窟: 横に長い、低い岩の崖（山の地形と同じ岩の房）の左に、暗い口。上に木
def rock_ledge(c, x0, x1, ytop, ybot, seed=3, n=30):
    """横に長い岩の帯。上のふちは、なだらかな波"""
    rnd = random.Random(seed)
    rocks = []
    for _ in range(n):
        x = rnd.uniform(x0 + 2, x1 - 2)
        top = ytop + 3 * math.sin((x - x0) * 0.21 + seed) + 2
        rocks.append((x, rnd.uniform(top + 2, ybot - 1), rnd.uniform(3.0, 4.4)))
    for (px_, py_, r) in sorted(rocks, key=lambda p: p[1]):
        for y in range(int(py_ - r), int(py_ + r) + 1):
            for x in range(int(px_ - r * 1.2), int(px_ + r * 1.2) + 1):
                u, v = (x + 0.5 - px_) / (r * 1.2), (y + 0.5 - py_) / r
                d = u * u + v * v
                if d <= 1 and y <= ybot and x0 <= x <= x1:
                    s = u * 0.6 + v
                    col = STONE[5] if s < -0.85 else STONE[4] if s < -0.25 else STONE[3] if s < 0.45 else STONE[2]
                    if d > 0.72 and s > 0.35:
                        col = STONE[0]
                    c.put(x, y, col, STONE)


def cave4(biome="grass"):
    """奥に横長の岩の崖。崖のすその口へ、手前の地面から飛び石の道がのびる（洞窟は地面の奥にある）"""
    c = Canvas()
    skirt(c, 24, 38, 22, 8, biome, seed=31)
    contact_shadow(c, 7, 43, 37, biome, depth=3, right=2)
    rock_ledge(c, 5, 44, 15, 36, seed=13, n=26)
    for y in range(26, 37):
        for x in range(10, 30):
            u = (x + 0.5 - 19.5) / 8.0
            top = 26 + u * u * 4
            if abs(u) <= 1 and y >= top:
                c.put(x, y, STONE[0] if abs(u) < 0.75 and y > top + 1 else STONE[1], STONE)
    for x in range(11, 29):
        u = (x + 0.5 - 19.5) / 8.0
        y = int(26 + u * u * 4) - 1
        if c.get(x, y) in STONE[2:]:
            c.put(x, y, STONE[5] if u < 0 else STONE[4], STONE)
    for (x, y) in ((19, 39), (21, 42), (19, 45)):                    # 飛び石
        c.put(x, y, STONE[4], STONE); c.put(x + 1, y, STONE[3], STONE); c.put(x, y + 1, STONE[2], STONE); c.put(x + 1, y + 1, STONE[1], STONE)
    tp = SNOWTREE if biome == "snow" else FOREST
    for (x, y, r) in ((34, 15, 3.4), (40, 18, 3.0), (9, 16, 2.8), (39, 39, 3.0)):
        if biome == "snow":
            pine(c, x, int(y + r), int(r * 2.3))
        else:
            tree(c, x, y, r, tp)
    tufts(c, 6, 43, 37, biome, seed=9, density=0.4)
    c.shadow_edges()
    return c.save(f"cave4-{biome}")

# ===================================================================== 祠: 森の中の空き地。森と同じ木の房に囲まれた、小さな石の祠と灯
def shrine4():
    c = Canvas()
    biome = "grass"
    skirt(c, 24, 30, 23, 17, biome, seed=41)
    # 空き地のまわりの森（森の地形と同じ、6ドットの房を互いちがいの格子にならべる。手前のまん中は道としてあける）
    spots = []
    for gy in range(0, 9):
        for gx in range(0, 9):
            x = 3 + gx * 5.2 + (2.6 if gy % 2 else 0)
            y = 6 + gy * 4.2
            d = ((x - 24) / 13) ** 2 + ((y - 28) / 9) ** 2
            far = ((x - 24) / 23) ** 2 + ((y - 24) / 19) ** 2
            if d > 1 and far < 1 and not (abs(x - 24) < 6 and y > 30):
                spots.append((x, y, 3.3))
    for (x, y, r) in sorted(spots, key=lambda p: p[1]):
        if y < 28:
            tree(c, x, y, r)
    # 石畳の小道と、祠（山の岩の色。屋根は1段明るい石の板）
    for (x, y) in ((23, 44), (24, 41), (23, 38), (24, 35)):          # 飛び石（山の岩の色）
        c.put(x, y, STONE[4], STONE); c.put(x + 1, y, STONE[3], STONE); c.put(x, y + 1, STONE[2], STONE); c.put(x + 1, y + 1, STONE[1], STONE)
    # （空き地を明るい草でぬる案は、色の数が16をこえて森の色が草の色にまとめられてしまったので、やめた）
    contact_shadow(c, 17, 31, 34, biome, depth=2, right=2)
    stone_wall(c, 17, 30, 27, 33, seed=2, top=True)
    roof_rows(c, 15, 32, 19, 25, SLATE, hip=True)                   # 屋根は青い石板（見つけやすい色を1つだけ）
    for y in range(29, 34):
        c.put(23, y, STONE[0], STONE); c.put(24, y, STONE[0], STONE)
    c.put(23, 30, LIGHT, STONE); c.put(24, 31, LIGHT, STONE)
    for (x, y) in ((24, 15), (23, 16), (25, 16), (22, 17), (26, 17), (23, 18), (25, 18), (24, 18)):   # 屋根の上の環のしるし
        c.put(x, y, GOLD, STONE)
    tufts(c, 16, 32, 35, biome, seed=7, density=0.5)
    for (x, y, r) in sorted(spots, key=lambda p: p[1]):
        if y >= 28:
            tree(c, x, y, r)
    c.shadow_edges()
    return c.save("shrine4")


# ===================================================================== 港: 砂浜と海（地形の色）、木の桟橋、家、小舟
def port4():
    c = Canvas()
    sea = texture("sea")
    # 海（右下のだ円。地形の海の絵をそのまま。岸は砂の色）
    for y in range(48):
        for x in range(48):
            d = ((x + 0.5 - 40) / 26) ** 2 + ((y + 0.5 - 50) / 14) ** 2
            if d <= 1:
                c.put(x, y, hx(sea.getpixel((x % 128, y % 128))))
            elif d <= 1.25 and ((x + 0.5 - 24) / 23) ** 2 + ((y + 0.5 - 28) / 18) ** 2 <= 1.1:
                c.put(x, y, SAND[2] if d < 1.12 else SAND[1])
    for k in range(0, 180, 5):                                   # 波打ちぎわ（とぎれとぎれの白い線）
        a = math.radians(180 + k)
        x = 40 + math.cos(a) * 26.5; y = 50 + math.sin(a) * 14.3
        if (k // 10) % 2 == 0:
            c.put(x, y, SEA[4])
    # 陸の草（町の地面）
    gt = texture("grass")
    for y in range(4, 40):
        for x in range(1, 47):
            if c.get(x, y) is None and ((x + 0.5 - 22) / 22) ** 2 + ((y + 0.5 - 24) / 18) ** 2 < 1 - 0.3 * (h2(x, y, 5) % 100) / 100:
                c.put(x, y, hx(gt.getpixel((x % 128, y % 128))))
    # 桟橋（道の木の色）
    for y in range(34, 46):
        for x in range(28, 31):
            c.put(x, y, DIRT[3] if y % 2 else DIRT[2], DIRT)
    # 小舟（白い帆。2色）
    for x in range(33, 41):
        c.put(x, 42, DIRT[2], DIRT); c.put(x + 1 if x < 40 else x, 43, DIRT[1], DIRT)
    for y in range(35, 42):
        for x in range(36, 36 + (y - 34) // 2 + 1):
            c.put(x, y, WALL[3] if x < 38 else WALL[2], WALL)
    c.put(35, 37, DIRT[0]); c.put(35, 41, DIRT[0])
    # 家（坂の上に3軒＋見張りの小屋）
    for (x0, yb, w, rf, hp) in ((5, 17, 10, ROOF, True), (19, 14, 9, ROOF, False), (8, 30, 9, SLATE, True), (19, 27, 8, ROOF, True)):
        contact_shadow(c, x0 + 1, x0 + w, yb + 1, "grass", depth=2, right=2)
        house(c, x0, yb, w, rf, hip=hp)
        tufts(c, x0, x0 + w - 1, yb + 1, "grass", seed=x0)
    for (x, y, r) in ((34, 12, 3.4), (40, 20, 3.0), (3, 24, 2.8)):
        tree(c, x, y, r)
    c.shadow_edges()
    return c.save("port4")


# ===================================================================== 村: 畑（丘の緑と道の土のうね）、わら屋根の家、干し草、木
def village4():
    c = Canvas()
    biome = "grass"
    skirt(c, 24, 29, 23, 16, biome, seed=51)
    # 畑（右下。うねは2行ごと: 明るい緑の葉と、土）
    for y in range(28, 44):
        for x in range(25, 45):
            if (x - 25) + (y - 28) * 0.3 < 20 and ((x + 0.5 - 35) / 11) ** 2 + ((y + 0.5 - 36) / 9) ** 2 < 1.15:
                col = (GRASS[4] if x % 3 else GRASS[3]) if y % 2 == 0 else DIRT[2]
                c.put(x, y, col)
    # 家（わら屋根3軒。大きさをかえる）
    for (x0, yb, w, hp) in ((4, 19, 12, True), (20, 15, 11, False), (7, 35, 11, True)):
        contact_shadow(c, x0 + 1, x0 + w, yb + 1, biome, depth=2, right=2)
        house(c, x0, yb, w, THATCH, hip=hp)
        tufts(c, x0, x0 + w - 1, yb + 1, biome, seed=x0)
    # 干し草（わらの小山2つ）
    for (hx_, hy) in ((24, 26), (29, 24)):
        for y in range(hy - 3, hy + 1):
            for x in range(hx_ - 3, hx_ + 4):
                d = ((x + 0.5 - hx_) / 3.2) ** 2 + ((y + 0.5 - hy) / 3.4) ** 2
                if d <= 1:
                    c.put(x, y, THATCH[3] if x < hx_ - 1 else THATCH[2] if x < hx_ + 2 else THATCH[1], THATCH)
    road(c, [(19, 44), (17, 36), (14, 30)], w=3)
    for (x, y, r) in ((38, 12, 3.6), (42, 20, 3.0), (3, 27, 3.0), (33, 18, 2.6)):
        tree(c, x, y, r)
    c.shadow_edges()
    return c.save("village4")


# ===================================================================== 鉱山: 右の岩の崖に木の枠の坑口、左にくず石の山とレール、小屋
def mine4():
    c = Canvas()
    biome = "grass"
    skirt(c, 24, 40, 23, 6, biome, seed=61)
    contact_shadow(c, 20, 45, 42, biome, depth=3, right=2)
    rock_ledge(c, 22, 46, 25, 42, seed=29, n=20)
    for y in range(31, 43):
        for x in range(28, 36):
            c.put(x, y, STONE[0] if 28 < x < 35 and y > 32 else STONE[1], STONE)
    for y in range(30, 43):
        c.put(27, y, DIRT[3], DIRT); c.put(28, y, DIRT[1], DIRT); c.put(35, y, DIRT[2], DIRT); c.put(36, y, DIRT[0], DIRT)
    for x in range(26, 38):
        c.put(x, 29, DIRT[4] if x < 35 else DIRT[2], DIRT); c.put(x, 30, DIRT[1], DIRT)
    c.put(25, 32, LIGHT); c.put(25, 31, DIRT[0])
    # レール（坑口から左へ。まくら木は道の木の色、レールは岩の明るい色）
    for x in range(6, 30):
        y = 42 - (30 - x) // 9
        c.put(x, y, STONE[4]); c.put(x, y + 2, STONE[3])
        if x % 3 == 0:
            c.put(x, y + 1, DIRT[1])
    # くず石の山（左。山の岩の小さい房）
    rnd = random.Random(3)
    for _ in range(9):
        px_, py_, r = rnd.uniform(7, 17), rnd.uniform(34, 39), rnd.uniform(1.6, 2.6)
        for y in range(int(py_ - r), int(py_ + r) + 1):
            for x in range(int(px_ - r), int(px_ + r) + 1):
                if ((x + 0.5 - px_) / r) ** 2 + ((y + 0.5 - py_) / r) ** 2 <= 1:
                    s = (x - px_) * 0.6 + (y - py_)
                    c.put(x, y, STONE[4] if s < -0.8 else STONE[3] if s < 0.8 else STONE[1], STONE)
    # 小屋（左の奥。板屋根）
    contact_shadow(c, 7, 16, 29, biome, depth=2, right=2)
    house(c, 6, 28, 9, DIRT, wall=WALL, hip=False)
    tufts(c, 4, 45, 43, biome, seed=13, density=0.35)
    c.shadow_edges()
    return c.save("mine4")


# ===================================================================== 砂漠の野営地: 低い丸屋根の天幕（布は砂・道・壁の色）、日よけの布、小さな泉とやし
def tents4():
    c = Canvas()
    biome = "sand"
    skirt(c, 24, 34, 22, 10, biome, seed=71)
    lake = texture("lake")
    for y in range(30, 41):
        for x in range(27, 45):
            d = ((x + 0.5 - 36) / 8) ** 2 + ((y + 0.5 - 36) / 4) ** 2
            if d <= 1:
                c.put(x, y, hx(lake.getpixel((x % 128, y % 128))) if d < 0.7 else SAND[0])
    def dome(cx, yb, rx, ry, cloth, band):
        for y in range(int(yb - ry), yb + 1):
            for x in range(int(cx - rx), int(cx + rx) + 1):
                u, v = (x + 0.5 - cx) / rx, (y + 0.5 - yb) / ry
                if u * u + v * v <= 1:
                    col = cloth[3] if u + v * 0.6 < -0.5 else cloth[2] if u < 0.35 else cloth[1]
                    c.put(x, y, col, cloth)
        for y in range(yb - 2, yb + 1):
            c.put(int(cx), y, DIRT[0], cloth); c.put(int(cx) + 1, y, DIRT[0], cloth)      # 入口
        c.put(int(cx), int(yb - ry) - 1, DIRT[0], cloth)                                  # 柱の先
    contact_shadow(c, 21, 31, 25, biome, depth=2, right=2)
    dome(25, 24, 6, 5, DIRT[1:], WALL)
    contact_shadow(c, 6, 22, 31, biome, depth=2, right=3)
    dome(14, 30, 8, 7, ROOF[1:], WALL)
    contact_shadow(c, 18, 27, 40, biome, depth=2, right=2)
    dome(22, 39, 5, 4, THATCH[1:], DIRT)
    for (x, y, col) in ((11, 39, DIRT[0]), (12, 39, DIRT[1]), (13, 40, DIRT[0]), (12, 38, "#ff9a40"), (12, 37, LIGHT)):   # たき火
        c.put(x, y, col)
    for y in range(18, 33):                                       # やし（幹は道の色、葉は森の色）
        x = 40 - ((y - 18) / 15) ** 2 * 2
        c.put(x, y, DIRT[3] if y % 3 else DIRT[1], DIRT); c.put(x + 1, y, DIRT[1], DIRT)
    for (ang, ln) in ((-2.7, 7), (-2.1, 6), (-0.9, 6), (-0.3, 7), (-1.5, 4)):
        for k in range(ln):
            x = 40.5 + math.cos(ang) * k
            y = 17 + math.sin(ang) * k * 0.6 + (k / ln) ** 2 * 4
            c.put(x, y, FOREST[3] if k < ln / 2 else FOREST[2], FOREST); c.put(x, y + 1, FOREST[1], FOREST)
    tufts(c, 5, 24, 32, biome, seed=3, density=0.3)
    c.shadow_edges()
    return c.save("tents4")


PIECES = [lambda: town4("grass"), lambda: town4("snow"), castle4, spire4, lambda: cave4("grass"), lambda: cave4("snow"),
          shrine4, port4, village4, mine4, tents4]
NAMES = ["town4-grass", "town4-snow", "castle4", "spire4", "cave4-grass", "cave4-snow", "shrine4", "port4", "village4", "mine4", "tents4"]


# ===================================================================== 今のアイコンとの「形の重なり」（シルエットの重なり＝IoU。ずらして最大の値）
OLD = {"town4-grass": "icon-village", "town4-snow": "icon-snowtown", "castle4": "icon-castle", "cave4-grass": "icon-cave",
       "cave4-snow": "icon-cave", "shrine4": "icon-shrine", "port4": "icon-port", "village4": "icon-village", "mine4": "icon-mine",
       "tents4": "icon-tents", "spire4": "spire"}


def mask(path):
    rows = [l for l in open(path).read().split("\n") if l]
    return {(x, y) for y, r in enumerate(rows) for x, ch in enumerate(r) if ch != "."}, len(rows[0]), len(rows)


def overlap(name):
    a, wa, ha = mask(os.path.join(HERE, f"{name}.txt"))
    o = OLD[name]
    d = "r22-vehicles" if o == "spire" else "r17-polish"
    b, wb, hb = mask(os.path.join(HERE, "..", d, f"{o}.txt"))
    best = 0
    for dx in range(-4, 5):
        for dy in range(-4, 5):
            bb = {(x + dx + (wa - wb) // 2, y + dy + (ha - hb)) for (x, y) in b}
            iou = len(a & bb) / max(1, len(a | bb))
            best = max(best, iou)
    return round(best, 2)


def show(names, kind="grass", Z=6, out="/tmp/claude-0/study2/s4.png"):
    from study3_view import terrain, load_icon
    ims = []
    for n in names:
        im = load_icon("r23-field-icons", n)
        bg = terrain(kind if not isinstance(kind, dict) else kind[n], im.width, im.height)
        bg.alpha_composite(im)
        ims.append(bg.resize((im.width * Z, im.height * Z), Image.NEAREST))
    W = sum(i.width + 10 for i in ims); H = max(i.height for i in ims)
    sheet = Image.new("RGBA", (W, H), (40, 40, 48, 255)); x = 0
    for i in ims:
        sheet.paste(i, (x, H - i.height)); x += i.width + 10
    sheet.save(out)


def ground_colors():
    out = set()
    for k in ("grass", "snow", "sand", "sea", "lake"):
        out |= {hx(c) for n, c in texture(k).getcolors(65536)}
    return out | set(GSHADE) | set(GROUND["snow"]["sh"]) | set(GROUND["sand"]["sh"]) | set(GRASS) | set(SAND) | set(SNOW[1:])


def overlap_structure(name):
    """地面の色（地形と同じ色・地面の影）をのぞいた「建物や岩そのもの」の形で、今のアイコンとの重なりを測る"""
    gc = ground_colors()
    rows = [l for l in open(os.path.join(HERE, f"{name}.txt")).read().split("\n") if l]
    pal = json.load(open(os.path.join(HERE, f"pal-{name}.json")))
    a = {(x, y) for y, r in enumerate(rows) for x, ch in enumerate(r) if ch != "." and pal[ch] not in gc}
    wa, ha = len(rows[0]), len(rows)
    o = OLD[name]
    d = "r22-vehicles" if o == "spire" else "r17-polish"
    b, wb, hb = mask(os.path.join(HERE, "..", d, f"{o}.txt"))
    best = 0
    for dx in range(-4, 5):
        for dy in range(-4, 5):
            bb = {(x + dx + (wa - wb) // 2, y + dy + (ha - hb)) for (x, y) in b}
            best = max(best, len(a & bb) / max(1, len(a | bb)))
    return round(best, 2)


# ===================================================================== プレビュー
KIND = {"town4-grass": "grass", "town4-snow": "snow", "castle4": "grass", "spire4": "sea", "cave4-grass": "grass", "cave4-snow": "snow",
        "shrine4": "grass", "port4": "grass", "village4": "grass", "mine4": "grass", "tents4": "sand"}


def preview(path, Z=4):
    from PIL import ImageDraw
    from study3_view import terrain, load_icon
    cells = []
    for n in NAMES:
        im = load_icon("r23-field-icons", n)
        bg = terrain(KIND[n], im.width + 16, im.height + 16)          # まわりにも地面を見せる（なじみ方を見るため）
        bg.alpha_composite(im, (8, 8))
        cells.append((f"{n} ({KIND[n]})  overlap {overlap(n)} / {overlap_structure(n)}", bg))
    maxw = 1600
    x, y, rowh, placed = 10, 10, 0, []
    for label, im in cells:
        w, h = im.width * Z, im.height * Z
        if x + w > maxw:
            x, y, rowh = 10, y + rowh + 24, 0
        placed.append((label, im, x, y)); x += w + 12; rowh = max(rowh, h)
    sheet = Image.new("RGBA", (maxw, y + rowh + 24), (40, 40, 48, 255))
    dr = ImageDraw.Draw(sheet)
    for label, im, px, py in placed:
        sheet.paste(im.resize((im.width * Z, im.height * Z), Image.NEAREST), (px, py))
        dr.text((px, py + im.height * Z + 4), label, fill=(255, 255, 255))
    sheet.save(path)


def world(path):
    """同じ場面を、左＝3回目の絵（コードの影つき）、右＝4回目の絵（影は絵に描きこみ）で並べる。本物の地形・本物の位置"""
    from PIL import ImageDraw
    from study3_view import world_rows, world_panel
    rows = world_rows()
    scenes = [   # (左上のマス, はば, 高さ) は、アイコンのまわりの 18×14 マス。位置は本物
        ((48, 152, 18, 14), [("village", 57, 161)], {"village": ("village3", "village4")}, "mugikano village"),
        ((38, 128, 18, 14), [("port", 47, 137)], {"port": ("port3", "port4")}, "namioto port"),
        ((102, 157, 18, 14), [("town", 111, 167)], {"town": ("village3", "town4-grass")}, "tomoshimori (grass town)"),
        ((236, 18, 18, 14), [("snowtown", 245, 27)], {"snowtown": ("town3", "town4-snow")}, "yukimachi (snow town)"),
        ((229, 189, 18, 14), [("castle", 238, 198)], {"castle": ("castle3", "castle4")}, "toushin castle"),
        ((247, 178, 18, 14), [("cave", 256, 187)], {"cave": ("cave3", "cave4-grass")}, "cave"),
        ((222, 203, 18, 14), [("shrine", 231, 212)], {"shrine": ("shrine3", "shrine4")}, "shrine"),
        ((113, 104, 18, 14), [("mine", 122, 113)], {"mine": ("mine3", "mine4")}, "tetsukusari mine"),
        ((260, 208, 18, 14), [("tents", 269, 217)], {"tents": ("tents3", "tents4")}, "arano camp"),
        ((168, 118, 18, 22), [("spire", 177, 135)], {"spire": ("spire3", "spire4")}, "the spire"),
    ]
    pairs = []
    for (x0, y0, tw, th), spots, mp, title in scenes:
        shade = {"port": "grass", "village": "grass", "town": "grass", "snowtown": "snow", "castle": "grass", "cave": "grass",
                 "shrine": "grass", "mine": "grass", "spire": "sea", "tents": "sand"}
        a = world_panel(rows, x0, y0, tw, th, [(mp[k][0], gx, gy, shade[k]) for (k, gx, gy) in spots], "3: " + title)
        b = world_panel(rows, x0, y0, tw, th, [(mp[k][1], gx, gy, None) for (k, gx, gy) in spots], "4: " + title)
        pr = Image.new("RGBA", (a.width * 2 + 6, a.height), (20, 20, 24, 255))
        pr.paste(a, (0, 0)); pr.paste(b, (a.width + 6, 0))
        pairs.append(pr)
    maxw, x, y, rowh, pos = 1200, 0, 0, 0, []
    for im in pairs:
        if x + im.width > maxw:
            x, y, rowh = 0, y + rowh + 10, 0
        pos.append((x, y)); x += im.width + 12; rowh = max(rowh, im.height)
    sheet = Image.new("RGBA", (maxw, y + rowh), (20, 20, 24, 255))
    for im, p in zip(pairs, pos):
        sheet.paste(im, p)
    sheet = sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST)
    sheet.save(path)


if __name__ == "__main__":
    for f in PIECES:
        print(*f())
    for n in NAMES:
        print(n, "形の重なり（全体 / 建物だけ）", overlap(n), overlap_structure(n))
    preview(os.path.join(HERE, "study4-preview.png"))
    world(os.path.join(HERE, "study4-world.png"))
    print("ok")
