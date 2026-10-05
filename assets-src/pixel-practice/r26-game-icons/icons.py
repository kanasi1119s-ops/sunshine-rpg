"""ゲームに入れるフィールドのアイコン（5回目、2026-10-05）。

人間の判断「お城は馴染んでいない方のがいい。町は全部馴染んだ方がいい。鉄工の町は作り直し、洞窟はもっと勉強して。」
            「城は影をなくしてね」
  - 町・村: 4回目の「地形になじむ」作り方（r23-field-icons/study4.py の道具）。置く地面ごとに作る。
    4回目の弱点（小さく静かで見落とす）を直すため、どの絵にも「見つける目じるし」を1つ以上入れ、
    その明るさを地面の平均と 25〜35 ちがえる（目じるしの明るさの差は、このスクリプトの最後で測って表示する）。
  - 町ごとの「らしさ」を1つ入れる（docs/story/bible.md の町の説明から）。
  - 鉄鏈鉱山は一から作りなおし（山の斜面の段々の町・かじ場とえんとつのけむり・坑口・トロッコの線路）。
  - お城（灯芯都）と宮殿（虚灯宮）: 3回目の作り方（r23-field-icons/study3.py の道具と家族のパレット）。48×48。
    **地面の影はない**（絵にも描かず、ゲームでもコードの影をつけない）。
  - どれも 48×48、1枚16色まで。どれも一から考えたオリジナルの形。
出力: この folder の <prop の名前>.txt / pal-<prop の名前>.json、preview-world.png、preview.png
"""
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R23 = os.path.join(HERE, "..", "r23-field-icons")
sys.path.insert(0, R23)

import study4 as S4                      # noqa: E402  なじむ作り方の道具
from study4 import (GRASS, GSHADE, FOREST, STONE, DIRT, SAND, SNOW, SNOWTREE, ROOF, SLATE, THATCH, WALL, LIGHT, GLOW, GOLD,  # noqa: E402
                    texture, hx, h2, skirt, contact_shadow, tufts, tree, pine, stone_wall, roof_rows, house, road, rock_ledge)
from PIL import Image                     # noqa: E402

# 地面の種類を足す（雲・荒れ地・丘）。色は地形の絵から取ったもの
S4.GROUND["cloud"] = dict(tex="cloud", sh=["#a2bcdc", "#b6cce6"], tuft=["#ffffff", "#eef4fc", "#cfe0f2"])
S4.GROUND["waste"] = dict(tex="waste", sh=["#382c40", "#4c4056"], tuft=["#6a5c74", "#5c4e66", "#4c4056"])
S4.GROUND["hills"] = dict(tex="hills", sh=GSHADE, tuft=[GRASS[4], GRASS[3], GRASS[1]])
PURE_KINDS = ("grass", "snow", "sand", "cloud", "waste", "hills")
CLOUD = ["#a2bcdc", "#b6cce6", "#cfe0f2", "#d6e4f4", "#eef4fc", "#ffffff"]
SMOKE = ["#8a8a96", "#a8a8b4", "#c8c8d2", "#e2e2e8"]
FIRE = ["#c2401c", "#ff8a2c", LIGHT]
LAKE = ["#2660b0", "#3070c4", "#7ab0ea", "#a8d0f4"]


def pure_colors():
    out = set()
    for k in PURE_KINDS:
        out |= {hx(c) for n, c in texture(k).getcolors(65536)}
    return out


class Canvas(S4.Canvas):
    """4回目の Canvas。地面の種類をふやし、この folder に書き出す"""

    def trim_ground(self, keep=1):
        pure = pure_colors()
        core = {(x, y) for y in range(self.h) for x in range(self.w) if self.c[y][x] and self.c[y][x] not in pure}
        near = set(core)
        for _ in range(keep):
            near |= {(x + dx, y + dy) for (x, y) in near for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))}
        for y in range(self.h):
            for x in range(self.w):
                if self.c[y][x] in pure and (x, y) not in near:
                    self.c[y][x] = None

    def reduce(self, limit=16):
        pure = pure_colors()
        prot = {LIGHT, GOLD, *GLOW, *FIRE, CLOUD[3], CLOUD[5]}

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
            pc = [cc for cc in cols if cc in pure]
            if len(pc) > 2:
                cols = pc                       # まず地面の粒の色どうしをまとめる
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

    def save(self, name, trim=True):
        S4.HERE = HERE
        return super().save(name, trim)


# ===================================================================== 部品（5回目に足したもの）
def puff(c, cx, cy, r, pal=SMOKE):
    """けむり・雲・霧の丸いかたまり（左上が明るく、下右は1段暗い。点はまかない）"""
    for y in range(int(cy - r) - 1, int(cy + r) + 2):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            u, v = (x + 0.5 - cx) / r, (y + 0.5 - cy) / (r * 0.8)
            d = u * u + v * v
            if d <= 1:
                s = u * 0.6 + v
                c.put(x, y, pal[3] if s < -0.3 else pal[2] if s < 0.45 else pal[1], pal)


def mist(c, x0, x1, y, pal=CLOUD):
    """霧の帯: 2行の、はしが丸い横長のかたまり。上の行は明るく、下の行は1段暗い"""
    for x in range(x0, x1 + 1):
        edge = x in (x0, x1)
        if not edge:
            c.put(x, y, pal[4] if (x // 5) % 2 else pal[5])
        c.put(x, y + 1, pal[3] if not edge else pal[2])


def water(c, cx, cy, rx, ry, tex="lake", rim=None):
    t = texture(tex)
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            d = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2
            if d <= 1:
                c.put(x, y, hx(t.getpixel((x % 128, y % 128))))
            elif rim and d <= 1.18:
                c.put(x, y, rim)


def chimney(c, x, ytop, h=5):
    for y in range(ytop, ytop + h):
        c.put(x, y, STONE[2], STONE); c.put(x + 1, y, STONE[1], STONE)
    c.put(x, ytop - 1, STONE[0], STONE); c.put(x + 1, ytop - 1, STONE[0], STONE)


def flat_house(c, x0, ybase, w, h, pal=THATCH, top=2, door=True, win=True):
    """平屋根の土の家（砂の町）。上の面が明るく、手前の面はまん中、右のふちは暗い"""
    x1 = x0 + w - 1
    for y in range(ybase - h - top + 1, ybase - h + 1):
        for x in range(x0, x1 + 1):
            c.put(x, y, pal[4] if x < x1 - 1 else pal[3], pal)
    for y in range(ybase - h + 1, ybase + 1):
        for x in range(x0, x1 + 1):
            c.put(x, y, pal[3] if x < x1 - 1 else pal[2], pal)
    for x in range(x0, x1 + 1):
        c.put(x, ybase - h + 1, pal[2] if x < x1 - 1 else pal[1], pal)            # 屋根のふちの影
    if door:
        c.put(x0 + w // 2, ybase, DIRT[0], pal); c.put(x0 + w // 2, ybase - 1, DIRT[0], pal)
    if win:
        c.put(x0 + 1, ybase - h + 3, DIRT[0], pal)


def awning(c, x0, x1, y, pal=(ROOF[3], WALL[3])):
    """しまの日よけ（屋台の布）: 上の面3行（2ドットごとのしま）＋前のふちの影、下に柱"""
    for x in range(x0, x1 + 1):
        st = (x - x0) // 2 % 2 == 0
        for k in range(3):
            c.put(x, y + k, (pal[0] if st else pal[1]) if k < 2 else (ROOF[1] if st else WALL[1]), ROOF)
    for x in (x0, x1):
        c.put(x, y + 3, DIRT[0]); c.put(x, y + 4, DIRT[0])
    for x in range(x0 + 1, x1):
        c.put(x, y + 3, DIRT[1]); c.put(x, y + 4, ROOF[3] if x % 3 == 0 else THATCH[3])   # 台の上の品物


def rock_slope(c, pts_top, ybot, seed=5, n=40):
    """山の斜面: pts_top（x → 上のふちのy）の下を、山の地形と同じ岩の房でうめる"""
    rnd = random.Random(seed)
    xs = sorted(pts_top)
    rocks = []
    for _ in range(n):
        x = rnd.uniform(xs[0], xs[-1])
        top = top_at(pts_top, x)
        if top >= ybot - 2:
            continue
        rocks.append((x, rnd.uniform(top + 2, ybot), rnd.uniform(3.0, 4.4)))
    for (px_, py_, r) in sorted(rocks, key=lambda p: p[1]):
        for y in range(int(py_ - r), int(py_ + r) + 1):
            for x in range(int(px_ - r * 1.2), int(px_ + r * 1.2) + 1):
                u, v = (x + 0.5 - px_) / (r * 1.2), (y + 0.5 - py_) / r
                d = u * u + v * v
                if d <= 1 and y <= ybot and y >= top_at(pts_top, x):
                    s = u * 0.6 + v
                    col = STONE[5] if s < -0.85 else STONE[4] if s < -0.25 else STONE[3] if s < 0.45 else STONE[2]
                    if d > 0.72 and s > 0.35:
                        col = STONE[0]
                    c.put(x, y, col, STONE)


def top_at(pts, x):
    xs = sorted(pts)
    for a, b in zip(xs, xs[1:]):
        if a <= x <= b:
            t = (x - a) / (b - a)
            return pts[a] + (pts[b] - pts[a]) * t
    return pts[xs[0]] if x < xs[0] else pts[xs[-1]]


def lighthouse(c, cx, ybase, h=15):
    """灯台: 石の台＋下が太い白い塔（赤い帯2本）＋ガラスの灯室（黄色い灯）＋暗いとんがり屋根"""
    for x in range(int(cx) - 4, int(cx) + 5):                      # 石の台
        c.put(x, ybase, STONE[3] if x < cx + 2 else STONE[1], STONE); c.put(x, ybase - 1, STONE[4] if x < cx + 2 else STONE[2], STONE)
    top = ybase - h
    for y in range(top + 4, ybase - 1):
        t = (y - top) / h
        half = 1.6 + t * 1.8
        for x in range(int(cx - half) - 1, int(cx + half) + 2):
            u = (x + 0.5 - cx) / half
            if abs(u) <= 1:
                band = (y - top) in (8, 9, 13, 14)
                col = (ROOF[3] if u < 0.2 else ROOF[1]) if band else (WALL[3] if u < 0.2 else WALL[1])
                c.put(x, y, col, WALL)
    for x in range(int(cx) - 3, int(cx) + 4):                      # 回廊
        c.put(x, top + 4, SLATE[1], SLATE)
    for y in range(top + 1, top + 4):                              # 灯室
        for x in range(int(cx) - 2, int(cx) + 3):
            c.put(x, y, LIGHT if x < cx + 1 else FIRE[1], WALL)
    for x in range(int(cx) - 2, int(cx) + 3):
        c.put(x, top, SLATE[2] if x < cx else SLATE[0], SLATE)
    c.put(cx, top - 1, SLATE[1], SLATE)


# ===================================================================== 1) 港町（灯里・波音の浜）: 灯台・入り江・桟橋・小舟・灯のともる家
def icon_port():
    c = Canvas()
    bio = "grass"
    skirt(c, 22, 26, 22, 18, bio, seed=101)
    water(c, 38, 46, 20, 10, tex="sea", rim=SAND[2])
    for k in range(0, 180, 6):                                     # 波打ちぎわ
        a = math.radians(180 + k)
        x, y = 38 + math.cos(a) * 20.6, 46 + math.sin(a) * 10.4
        if (k // 12) % 2 == 0:
            c.put(x, y, "#a8d0f4")
    for y in range(36, 47):                                         # 桟橋
        for x in range(25, 28):
            c.put(x, y, DIRT[3] if y % 2 else DIRT[2], DIRT)
    for x in range(31, 40):                                         # 小舟（白い帆）
        c.put(x, 43, DIRT[2], DIRT); c.put(x, 44, DIRT[0], DIRT)
    for y in range(36, 43):
        for x in range(34, 34 + (y - 35) // 2 + 2):
            c.put(x, y, WALL[3] if x < 36 else WALL[2], WALL)
    plan = [(3, 15, 11, ROOF, True), (17, 12, 10, ROOF, False), (5, 29, 10, SLATE, True), (17, 26, 9, ROOF, True)]
    for (x0, yb, w, rf, hp) in plan:
        contact_shadow(c, x0 + 1, x0 + w, yb + 1, bio, depth=2, right=2)
        house(c, x0, yb, w, rf, hip=hp)
        tufts(c, x0, x0 + w - 1, yb + 1, bio, seed=x0)
    contact_shadow(c, 38, 46, 34, bio, depth=2, right=2)
    lighthouse(c, 41, 33, 19)                                       # 目じるし: 白と赤の灯台、てっぺんの灯
    for (x, y, r) in ((33, 10, 3.2), (36, 20, 2.8)):
        tree(c, x, y, r)
    c.shadow_edges()
    return c.save("icon-port")


# ===================================================================== 2) 村（麦香野ほか）: 水路と水車小屋・畑・わら屋根
def wheel(c, cx, cy, r=4):
    for y in range(int(cy - r) - 1, int(cy + r) + 2):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            if r - 1.2 <= d <= r:
                c.put(x, y, DIRT[0] if x > cx else DIRT[1], DIRT)
            elif d < r - 1.2:
                a = math.atan2(y + 0.5 - cy, x + 0.5 - cx)
                if (int((a + math.pi) / (math.pi / 4) + 0.5)) % 2 == 0 and abs(math.sin(a * 4)) < 0.4:
                    c.put(x, y, DIRT[0], DIRT)                     # 水車の板
    c.put(cx, cy, DIRT[0], DIRT)


def icon_village():
    c = Canvas()
    bio = "grass"
    skirt(c, 24, 28, 22, 17, bio, seed=111)
    # 水路（左上から右下へ。湖の地形の色）
    for k in range(0, 60):
        t = k / 59
        x = 2 + t * 44
        y = 30 + math.sin(t * 3.0) * 4 + t * 6
        for dy in range(3):
            col = LAKE[2] if dy == 0 else LAKE[1] if dy == 1 else LAKE[0]
            c.put(x, y + dy, col)
    # 畑（右上。うね）
    for y in range(8, 22):
        for x in range(28, 46):
            if ((x + 0.5 - 37) / 9.5) ** 2 + ((y + 0.5 - 15) / 7) ** 2 < 1:
                c.put(x, y, THATCH[4] if y % 2 == 0 else THATCH[3], THATCH)        # 麦の畑（明るい列と暗い列）
    # 水車小屋（水路にかかる。いちばん暗い木の水車が目じるし）
    contact_shadow(c, 13, 22, 31, bio, depth=2, right=2)
    house(c, 12, 30, 10, THATCH, hip=False)
    wheel(c, 24, 31, 4.5)
    # わら屋根の家2軒と赤い屋根の家1軒
    for (x0, yb, w, rf, hp) in ((3, 19, 11, THATCH, True), (16, 15, 10, ROOF, True), (27, 42, 11, THATCH, False)):
        contact_shadow(c, x0 + 1, x0 + w, yb + 1, bio, depth=2, right=2)
        house(c, x0, yb, w, rf, hip=hp)
        tufts(c, x0, x0 + w - 1, yb + 1, bio, seed=x0)
    for (x, y, r) in ((5, 41, 3.2), (42, 31, 3.0), (11, 6, 2.8)):
        tree(c, x, y, r)
    c.shadow_edges()
    return c.save("icon-village")


# ===================================================================== 3) 霧間の集落（山あいの、霧にうかぶ小さな集落）
def icon_village_mist():
    c = Canvas()
    bio = "grass"
    skirt(c, 24, 30, 21, 15, bio, seed=121)
    rock_slope(c, {6: 20, 14: 10, 22: 15, 30: 7, 38: 13, 44: 20}, 22, seed=7, n=22)    # 奥の小さな岩山
    GP = ["#0c2a10", "#1c5a22", "#28742a", "#3a9034", "#62b04a"]
    for (x, yb, h) in ((5, 31, 10), (42, 31, 11), (3, 42, 8), (44, 42, 8)):
        pine(c, x, yb, h, pal=GP)                                  # 山の針葉樹（森の色）
    for (x0, yb, w) in ((9, 29, 11), (26, 27, 12), (17, 41, 11)):
        contact_shadow(c, x0 + 1, x0 + w, yb + 1, bio, depth=2, right=2)
        house(c, x0, yb, w, SLATE, hip=False)                      # 急な青い石板の屋根、白い壁（目じるし）
        tufts(c, x0, x0 + w - 1, yb + 1, bio, seed=x0)
    mist(c, 1, 14, 33); mist(c, 33, 47, 35)                        # 霧の帯（はしだけ。家は隠さない）
    c.shadow_edges()
    return c.save("icon-village-mist")


# ===================================================================== 4) 硝子湖: 湖の上にうかぶ交易の町（石の島・ガラスの丸屋根・橋）
def glass_dome(c, cx, yb, r):
    for y in range(int(yb - r), yb + 1):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            u, v = (x + 0.5 - cx) / r, (y + 0.5 - yb) / r
            if u * u + v * v <= 1:
                s = u + v * 0.5
                c.put(x, y, GLOW[2] if s < -0.6 else GLOW[1] if s < 0.2 else GLOW[0], GLOW)


def icon_lake():
    c = Canvas()
    bio = "grass"
    skirt(c, 24, 30, 23, 16, bio, seed=131)
    water(c, 24, 30, 22.5, 14, tex="lake", rim=SAND[1])
    # 石の島（上の面＋手前の厚み）2つと、岸への橋
    for (cx, cy, rx, ry) in ((15, 26, 9, 5), (33, 33, 8, 4.5)):
        for y in range(int(cy - ry), int(cy + ry) + 3):
            for x in range(int(cx - rx), int(cx + rx) + 1):
                d = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2
                dd = ((x + 0.5 - cx) / rx) ** 2 + ((y - 2 + 0.5 - cy) / ry) ** 2
                if d <= 1:
                    c.put(x, y, STONE[4] if (x // 3 + y) % 4 else STONE[3], STONE)
                elif dd <= 1:
                    c.put(x, y, STONE[2] if x < cx + rx * 0.5 else STONE[1], STONE)
    for x in range(22, 28):                                       # 島と島の橋
        c.put(x, 30, DIRT[3], DIRT); c.put(x, 31, DIRT[1], DIRT)
    for y in range(37, 46):                                       # 岸への橋
        c.put(31, y, DIRT[3], DIRT); c.put(32, y, DIRT[2], DIRT); c.put(33, y, DIRT[1], DIRT)
    # 建物（ガラスの丸屋根＝目じるし。交易の塔）
    contact_shadow(c, 9, 20, 27, bio, depth=1, right=1)
    house(c, 8, 26, 9, ROOF, hip=True)
    glass_dome(c, 21, 26, 4)
    for y in range(13, 27):                                       # 交易の塔（細く高い）
        for x in range(14, 18):
            c.put(x, y, WALL[3] if x < 16 else WALL[1], WALL)
    roof_rows(c, 13, 18, 9, 12, SLATE, hip=True)
    c.put(15, 16, LIGHT, WALL)
    glass_dome(c, 33, 32, 5)
    house(c, 26, 34, 6, ROOF, hip=True, lit=False)
    for x in range(36, 42):
        c.put(x, 40, DIRT[2], DIRT); c.put(x + 1, 41, DIRT[0], DIRT)   # 小舟
    for (x, y, r) in ((4, 12, 3.2), (43, 18, 3.0)):
        tree(c, x, y, r)
    c.shadow_edges()
    return c.save("icon-lake")


# ===================================================================== 5) 鉄鏈鉱山（作りなおし）: 山の斜面の段々の町・かじ場とえんとつのけむり・坑口・トロッコの線路
def terrace(c, x0, x1, y, h=3):
    """段々の石垣（上の面1行＋手前の石積み）"""
    for x in range(x0, x1 + 1):
        c.put(x, y, STONE[4] if x < x1 - 1 else STONE[3], STONE)
    stone_wall(c, x0, x1, y + 1, y + h, seed=x0)


def icon_mine():
    c = Canvas()
    bio = "grass"
    skirt(c, 24, 32, 23, 15, bio, seed=141)
    # 山の斜面（右上が高い）。坑口は右上
    rock_slope(c, {14: 18, 22: 8, 30: 3, 38: 2, 47: 6}, 22, seed=17, n=34)
    for y in range(10, 20):                                       # 坑口（暗い穴と木の枠）
        for x in range(33, 41):
            c.put(x, y, STONE[0] if 33 < x < 40 and y > 11 else STONE[1], STONE)
    for y in range(9, 20):
        c.put(32, y, DIRT[3], DIRT); c.put(41, y, DIRT[0], DIRT)
    for x in range(31, 43):
        c.put(x, 9, DIRT[4] if x < 40 else DIRT[2], DIRT)
    # 段々（3段）。下の段ほど手前で広い
    terrace(c, 18, 46, 20)
    terrace(c, 6, 40, 30)
    terrace(c, 2, 34, 40, h=2)
    # トロッコの線路（坑口からジグザグに下りる。レールは明るい石の2本、まくら木は土の色）
    for (xa, ya, xb, yb) in ((36, 20, 44, 20), (44, 21, 44, 29), (44, 29, 38, 29)):
        n = max(abs(xb - xa), abs(yb - ya))
        for k in range(n + 1):
            x = xa + (xb - xa) * k // max(1, n); y = ya + (yb - ya) * k // max(1, n)
            if ya == yb:
                c.put(x, y - 1, STONE[5], STONE); c.put(x, y, DIRT[1] if x % 2 else STONE[3], STONE)
            else:
                c.put(x - 1, y, STONE[5], STONE); c.put(x, y, DIRT[1] if y % 2 else STONE[3], STONE)
    for y in range(17, 20):                                       # トロッコ
        for x in range(38, 43):
            c.put(x, y, DIRT[0] if y == 19 else (STONE[4] if y == 17 else DIRT[1]), DIRT)
    c.put(39, 16, "#c8b45a"); c.put(40, 16, LIGHT)               # 灯り石のかがやき
    # 上の段: かじ場（ふいごの火）とえんとつ＋けむり
    house(c, 20, 19, 11, SLATE, hip=False, lit=False)
    c.put(23, 18, FIRE[1]); c.put(24, 18, LIGHT); c.put(23, 19, FIRE[0]); c.put(24, 19, FIRE[0])   # 目じるし: かじ場の火
    chimney(c, 27, 6, 6)
    puff(c, 29, 3, 2.6); puff(c, 33, 1.5, 2.0)
    # 中の段: 家とかじ場
    house(c, 8, 29, 10, ROOF, hip=True)
    house(c, 22, 29, 10, SLATE, hip=False, lit=False)
    c.put(25, 28, FIRE[1]); c.put(25, 29, FIRE[0])
    chimney(c, 29, 17, 5)
    puff(c, 31, 14, 2.2)
    # 下の段: 長屋（横長の家）
    house(c, 4, 39, 13, ROOF, hip=False)
    house(c, 19, 39, 10, SLATE, hip=True)
    tufts(c, 2, 34, 43, bio, seed=7, density=0.35)
    road(c, [(36, 41), (39, 46)], w=3)
    c.shadow_edges()
    return c.save("icon-mine")


# ===================================================================== 6) 砂音（砂漠の隊商都市）: 平屋根の土の家・しまの日よけの市場・丸屋根の天幕・井戸とやし
def palm(c, x0, ytop, ybot):
    for y in range(ytop, ybot):
        x = x0 - ((y - ytop) / max(1, ybot - ytop)) ** 2 * 2
        c.put(x, y, DIRT[3] if y % 3 else DIRT[1], DIRT); c.put(x + 1, y, DIRT[1], DIRT)
    for (ang, ln) in ((-2.7, 7), (-2.1, 6), (-0.9, 6), (-0.3, 7), (-1.5, 4)):
        for k in range(ln):
            x = x0 + 0.5 + math.cos(ang) * k
            y = ytop - 1 + math.sin(ang) * k * 0.6 + (k / ln) ** 2 * 4
            c.put(x, y, FOREST[3] if k < ln / 2 else FOREST[2], FOREST); c.put(x, y + 1, FOREST[1], FOREST)


def dome_tent(c, cx, yb, rx, ry, cloth):
    for y in range(int(yb - ry), yb + 1):
        for x in range(int(cx - rx), int(cx + rx) + 1):
            u, v = (x + 0.5 - cx) / rx, (y + 0.5 - yb) / ry
            if u * u + v * v <= 1:
                c.put(x, y, cloth[3] if u + v * 0.6 < -0.5 else cloth[2] if u < 0.35 else cloth[1], cloth)
    for y in range(yb - 2, yb + 1):
        c.put(int(cx), y, DIRT[0], cloth); c.put(int(cx) + 1, y, DIRT[0], cloth)
    c.put(int(cx), int(yb - ry) - 1, DIRT[0], cloth)


# ===================================================================== 6) 砂音（砂漠の隊商都市）: 寄りあう平屋根の土の家・まん中の丸屋根の隊商宿・しまの日よけの市・井戸とやし
def icon_tents():
    c = Canvas()
    bio = "sand"
    skirt(c, 24, 30, 23, 16, bio, seed=151)
    ADOBE = ["#6e5228", "#8a6a36", "#a8864a", "#c4a260", "#dcc07c"]
    # 奥から手前へ、高さのちがう土の家を寄せて並べる（町の壁のように連なる）
    for (x0, yb, w, h) in ((3, 20, 10, 7), (12, 17, 8, 9), (28, 18, 9, 8), (36, 21, 9, 6), (4, 31, 9, 6), (35, 32, 10, 6)):
        contact_shadow(c, x0 + 1, x0 + w, yb + 1, bio, depth=2, right=2)
        flat_house(c, x0, yb, w, h, ADOBE)
    # まん中の隊商宿（大きな丸屋根。赤茶＝目じるし）
    contact_shadow(c, 16, 33, 28, bio, depth=2, right=2)
    for y in range(20, 28):
        for x in range(17, 32):
            c.put(x, y, ADOBE[3] if x < 30 else ADOBE[2], ADOBE)
    dome_tent(c, 24, 20, 7, 7, [ROOF[0], ROOF[2], ROOF[3], ROOF[4]])
    for y in range(23, 28):
        c.put(24, y, DIRT[0], ADOBE); c.put(25, y, DIRT[0], ADOBE)
    # 手前の市（しまの日よけ3つ）と井戸
    awning(c, 12, 20, 36); awning(c, 24, 32, 38)
    for (x, y) in ((6, 39), (7, 38), (8, 38), (9, 39), (6, 40), (9, 40), (7, 41), (8, 41)):
        c.put(x, y, STONE[3], STONE)
    c.put(7, 39, LAKE[1]); c.put(8, 39, LAKE[1]); c.put(7, 40, LAKE[0]); c.put(8, 40, LAKE[0])
    palm(c, 41, 30, 44)
    tufts(c, 4, 44, 45, bio, seed=3, density=0.3)
    c.shadow_edges()
    return c.save("icon-tents")


# ===================================================================== 7) 草の上の野営地（砂守のいずみ・荒野の市）: 丸屋根の天幕・市場の屋台・小さな泉
def icon_tents_grass():
    c = Canvas()
    bio = "grass"
    skirt(c, 24, 32, 22, 13, bio, seed=161)
    water(c, 35, 37, 8, 4, tex="lake", rim=SAND[1])
    contact_shadow(c, 6, 22, 31, bio, depth=2, right=3)
    dome_tent(c, 14, 30, 8, 7, [ROOF[0], ROOF[2], ROOF[3], ROOF[4]])
    contact_shadow(c, 21, 31, 25, bio, depth=2, right=2)
    dome_tent(c, 26, 24, 6, 5, [WALL[0], WALL[1], WALL[2], WALL[3]])
    awning(c, 4, 13, 37); awning(c, 16, 25, 39)                   # 屋台（市）
    for (x, y, col) in ((20, 33, DIRT[0]), (21, 33, DIRT[1]), (20, 32, FIRE[1]), (21, 32, LIGHT)):
        c.put(x, y, col)
    palm(c, 42, 20, 34)
    tufts(c, 4, 44, 32, bio, seed=5, density=0.3)
    c.shadow_edges()
    return c.save("icon-tents-grass")


# ===================================================================== 8) 霧断崖（断崖にはりつく古い宗教都市）: 崖の段に重なる建物・環のしるしの堂・霧
def icon_temple():
    c = Canvas()
    bio = "grass"
    skirt(c, 24, 36, 22, 10, bio, seed=171)
    # 断崖（まん中の高い岩。山の地形の岩の房）
    rock_slope(c, {4: 30, 10: 14, 18: 4, 30: 3, 38: 12, 45: 28}, 42, seed=23, n=46)
    # 崖の段に、上へ重なる建物（白い壁＝目じるし、青い石板の屋根）
    for (x0, yb, w) in ((8, 36, 9), (30, 38, 10), (13, 26, 9), (27, 24, 8), (19, 15, 10)):
        terrace(c, x0 - 1, x0 + w, yb + 1, h=2)
        house(c, x0, yb, w, SLATE, wall=WALL, hip=True)
    for (x, y) in ((24, 3), (23, 4), (25, 4), (22, 5), (26, 5), (23, 6), (25, 6), (24, 6)):
        c.put(x, y, GOLD)                                          # 堂の上の環のしるし
    c.put(24, 7, GOLD); c.put(24, 8, GOLD)
    for k in range(6):                                             # つづら折りの石段
        c.put(19 + (k % 2) * 6, 27 + k * 2, STONE[5], STONE); c.put(20 + (k % 2) * 6, 27 + k * 2, STONE[4], STONE)
    mist(c, 2, 16, 30); mist(c, 30, 46, 20); mist(c, 14, 36, 43)  # 霧の帯
    c.shadow_edges()
    return c.save("icon-temple")


# ===================================================================== 9) 雪の町（霜原・雪待ちの小屋町）: 木の壁の家・雪の屋根・見張りの塔とかがり火・針葉樹
def icon_snowtown():
    c = Canvas()
    bio = "snow"
    skirt(c, 24, 30, 23, 16, bio, seed=181)
    road(c, [(30, 47), (27, 38), (22, 31), (24, 22)], w=3, pal=SNOW[1:])
    TIMBER = [DIRT[0], DIRT[1], DIRT[2], DIRT[3]]                  # 雪の白とはっきり分かれる、木の壁
    plan = [(4, 18, 11, ROOF, True), (28, 16, 11, SLATE, False), (3, 32, 10, SLATE, True), (29, 31, 12, ROOF, True), (13, 42, 10, ROOF, False)]
    for (x0, yb, w, rf, hp) in plan:
        contact_shadow(c, x0 + 1, x0 + w, yb + 1, bio, depth=2, right=2)
        house(c, x0, yb, w, rf, wall=TIMBER, hip=hp, snow=True)
        tufts(c, x0, x0 + w - 1, yb + 1, bio, seed=x0)
    # 見張りの塔（古戦場のなごり。かがり火＝目じるし）
    for y in range(6, 24):
        for x in range(19, 24):
            c.put(x, y, STONE[3] if x < 22 else STONE[2], STONE)
    for x in range(18, 25):
        c.put(x, 5, STONE[4], STONE); c.put(x, 6, STONE[1], STONE)
    c.put(20, 3, FIRE[1]); c.put(21, 3, LIGHT); c.put(21, 2, FIRE[1]); c.put(20, 4, FIRE[0]); c.put(21, 4, FIRE[0]); c.put(22, 4, FIRE[0])
    c.put(21, 12, STONE[0], STONE); c.put(21, 13, LIGHT, STONE)
    for (x, yb, h) in ((43, 26, 9), (2, 26, 7), (40, 44, 7), (16, 30, 6)):
        pine(c, x, yb, h)
    c.shadow_edges()
    return c.save("icon-snowtown")


# ===================================================================== 10) 浮嶼（雲の上の浮島群）: 小さな浮島3つ・家・橋・雲
def floating_isle(c, cx, cy, rx, depth, seed=1):
    ry = rx * 0.36
    rnd = random.Random(seed)
    for y in range(int(cy), int(cy + depth) + 1):
        t = (y - cy) / depth
        half = rx * (1 - t) ** 1.1
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            u = (x + 0.5 - cx) / max(0.6, half)
            if abs(u) <= 1:
                col = STONE[3] if u < -0.3 else STONE[2] if u < 0.4 else STONE[1]
                if (h2(x, y, seed) % 7) == 0:
                    col = STONE[4] if u < 0 else STONE[0]
                c.put(x, y, col, STONE)
    for y in range(int(cy - ry), int(cy + ry) + 1):
        for x in range(int(cx - rx), int(cx + rx) + 1):
            d = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2
            if d <= 1:
                c.put(x, y, GRASS[4] if (d > 0.7 and y < cy) else GRASS[3] if y < cy + 1 else GRASS[1], GRASS)


def icon_sky():
    c = Canvas()
    bio = "cloud"
    floating_isle(c, 13, 20, 11, 14, seed=3)
    floating_isle(c, 35, 14, 9, 11, seed=5)
    floating_isle(c, 33, 34, 8, 9, seed=7)
    house(c, 7, 18, 11, ROOF, hip=True)                            # 赤茶の屋根＝目じるし
    house(c, 30, 12, 10, ROOF, hip=False)
    for y in range(25, 33):                                        # 見張りの小塔
        for x in range(32, 35):
            c.put(x, y, WALL[3] if x < 34 else WALL[1], WALL)
    roof_rows(c, 31, 35, 22, 24, SLATE, hip=True)
    c.put(33, 28, LIGHT, WALL)
    for x in range(22, 28):                                        # つり橋（2つの島のあいだ）
        y = 17 - int(math.sin((x - 22) / 5 * math.pi) * -1.5)
        c.put(x, y, DIRT[3], DIRT); c.put(x, y + 1, DIRT[0], DIRT)
    for (x, y, r) in ((6, 38, 3.4), (11, 40, 2.8), (42, 26, 3.0), (20, 44, 2.6)):
        puff(c, x, y, r, CLOUD[1:])
    tree(c, 20, 16, 2.6)
    c.shadow_edges()
    return c.save("icon-sky")


# ===================================================================== 11) 灯芯都のお城（3回目の作り方。48×48。影なし）
import study as _study                   # noqa: E402  3回目の Grid の書き出し先を、この folder にするため
import study3 as S3                     # noqa: E402
from study3 import (STONE as S3STONE, TEAL, DARK, ramp_of, ring_mark, fill_ellipse)   # noqa: E402
from study2 import cylinder, ellipse_top, cone, hip_roof, brick_face, top_face, parapet   # noqa: E402


def s3save(g, name):
    _study.HERE = HERE
    return S3.save(g, name)


def icon_castle():
    g = _study.Grid(48, 48)
    S = S3STONE
    # 奥の壁（上の面2行＋中庭がわの面2行）
    top_face(g, 5, 42, 9, 10, S, 0.86); parapet(g, 5, 42, 9, S, 3)
    brick_face(g, 5, 42, 11, 12, S, 0.42, seed=1)
    # 中庭（石だたみ）と、天守への道、四すみの木
    for y in range(13, 33):
        for x in range(6, 42):
            g.put(x, y, "a" if y < 14 else ("c" if ((x // 3) + (y // 2) * 3) % 5 == 0 else "b"))
    for y in range(20, 33):
        for x in range(22, 26):
            g.put(x, y, "d" if (x + y // 2) % 3 else "c")
    for (tx, ty) in ((10, 26), (37, 26)):
        fill_ellipse(g, tx, ty, 3.0, 2.6, lambda x, y, u, v, d: "o" if d > 0.75 and u + v > 0.4 else ("K" if u + v < -0.2 else "J"))
    # 左右の壁の上の面
    top_face(g, 3, 5, 9, 33, S, 0.86); top_face(g, 42, 44, 9, 33, S, 0.66)
    # 天守（寄棟の屋根＋手前の壁、垂れ幕、入口、環のしるし）
    hip_roof(g, 14, 33, 2, 10, TEAL, wb=1.5, ws=1.0)
    brick_face(g, 14, 33, 12, 19, S, 0.6, seed=2)
    g.rect(14, 12, 33, 12, "a")
    for i, wx in enumerate((17, 20, 27, 30)):
        g.rect(wx, 14, wx, 15, "k")
        if i in (1, 2):
            g.put(wx, 15, "L")
    for y in range(16, 20):
        for x in range(22, 26):
            if y > 16 or 23 <= x <= 24:
                g.put(x, y, "k")
    ring_mark(g, 24, 14, "h", "k", "h")
    g.rect(15, 13, 15, 17, "G"); g.rect(16, 13, 16, 17, "F"); g.rect(32, 13, 32, 17, "G"); g.rect(33, 13, 33, 17, "F")
    for x in range(34, 37):
        for y in range(13, 21):
            if g.get(x, y) in "bc":
                g.put(x, y, "a")                                       # 天守の右の影（中庭の上）
    # 奥の角の塔（とんがり屋根）
    for tx in (4, 43):
        cylinder(g, tx, 4.0, 6, 11, 1.4, S, shade=-0.04)
        ellipse_top(g, tx, 6, 4.4, 1.6, S)
        cone(g, tx, 6, 4.9, 6, 1.6, TEAL)
        g.rect(tx - 1, 8, tx - 1, 9, "k")
    # 手前の壁（低い）
    top_face(g, 5, 42, 32, 33, S, 0.86); parapet(g, 5, 42, 32, S, 3)
    brick_face(g, 5, 42, 34, 37, S, 0.55, seed=0)
    # 手前の角の塔（平らな屋上）
    for tx in (4, 43):
        cylinder(g, tx, 4.4, 28, 38, 1.6, S)
        ellipse_top(g, tx, 28, 4.8, 1.8, S, inner=1.6, merlons=10)
        g.rect(tx - 1, 31, tx - 1, 33, "k"); g.put(tx - 1, 32, "L")
    # 門の建物
    top_face(g, 19, 28, 29, 31, S, 0.92); parapet(g, 19, 28, 29, S, 3)
    brick_face(g, 19, 28, 32, 41, S, 0.58, seed=3)
    for y in range(35, 42):
        for x in range(22, 26):
            if y > 36 or 23 <= x <= 24:
                g.put(x, y, "k" if (x - 22) % 2 or y > 39 else "o")
    for y in range(42, 47):                                            # 門前の道
        for x in range(22 - (y - 42) // 2, 26 + (y - 42) // 2):
            g.put(x, y, "c" if (x + y) % 3 else "b")
    outline_dark(g, ramp_of(S3STONE, TEAL, "oJK"))
    return s3save(g, "icon-castle")


# ===================================================================== 12) 虚灯宮（3回目の作り方。48×48。影なし）: 段々の台・列柱・まん中の「からっぽの灯」の塔
def icon_palace():
    g = _study.Grid(48, 48)
    S = S3STONE
    P = DARK
    # いちばん下の段（上の面＋石積み）と、まん中の大階段
    top_face(g, 2, 45, 34, 36, S, 0.9); brick_face(g, 2, 45, 37, 41, S, 0.5, seed=1)
    for k in range(10):
        y = 34 + k
        for x in range(20 - k // 3, 28 + k // 3):
            g.put(x, y, "d" if k % 2 == 0 else "b")
    # 中の段（列柱の回廊）
    top_face(g, 7, 40, 27, 29, S, 0.92)
    for y in range(30, 34):
        for x in range(7, 41):
            k = (x - 7) % 4
            g.put(x, y, "k" if k == 3 else ("d" if k == 0 else "c" if k == 1 else "b"))
    # 左右の丸屋根（暗い石）
    for cx in (11, 36):
        fill_ellipse(g, cx, 26, 4.2, 4.0, lambda x, y, u, v, d: None if v > 0.15 else tone_dark(u, v))
        g.put(cx, 21, "h")
    # 上の広間（寄棟の暗い屋根＋手前の壁、入口）
    hip_roof(g, 13, 34, 15, 21, P, wb=1.5, ws=1.0)
    brick_face(g, 13, 34, 23, 26, S, 0.62, seed=2)
    g.rect(13, 23, 34, 23, "a")
    for y in range(24, 27):
        for x in range(22, 26):
            g.put(x, y, "k")
    # まん中の「からっぽの灯」の塔: 4本の柱の枠、中は暗いからっぽ、ふちにだけむらさきの光
    for y in range(3, 16):
        for x in range(19, 29):
            edge = x in (19, 20, 27, 28)
            if edge:
                g.put(x, y, "d" if x in (19, 27) else "b")
            else:
                g.put(x, y, "k")
    for y in (3, 9, 15):
        for x in range(19, 29):
            g.put(x, y, "d" if x < 27 else "b")
    for (x, y) in ((22, 5), (25, 5), (21, 6), (26, 6), (21, 7), (26, 7), (22, 8), (25, 8), (23, 5), (24, 5)):
        g.put(x, y, "W")
    g.put(22, 6, "Y"); g.put(22, 7, "Y")
    hip_roof(g, 18, 29, 0, 2, P, wb=1.5, ws=1.0)
    g.put(23, 0, "h"); g.put(24, 0, "h")
    outline_dark(g, ramp_of(S3STONE, DARK))
    return s3save(g, "icon-palace")


def tone_dark(u, v):
    from study import tone
    return tone(DARK, 0.75 - u * 0.4 - v * 0.2)


from study import outline_dark            # noqa: E402

PIECES = [icon_port, icon_village, icon_village_mist, icon_lake, icon_mine, icon_tents, icon_tents_grass, icon_temple,
          icon_snowtown, icon_sky, icon_castle, icon_palace]

TERRAIN = {"icon-port": "grass", "icon-village": "grass", "icon-village-mist": "grass", "icon-lake": "grass", "icon-mine": "grass",
           "icon-tents": "sand", "icon-tents-grass": "grass", "icon-temple": "grass", "icon-snowtown": "snow", "icon-sky": "cloud",
           "icon-castle": "hills", "icon-palace": "waste"}
NAMES = list(TERRAIN)


def show(names, Z=5, out="/tmp/claude-0/study2/r26.png"):
    from study3_view import terrain, load_icon
    ims = []
    for n in names:
        im = load_icon("r26-game-icons", n)
        bg = terrain(TERRAIN[n], im.width + 16, im.height + 16)
        bg.alpha_composite(im, (8, 8))
        ims.append(bg.resize((bg.width * Z, bg.height * Z), Image.NEAREST))
    W = sum(i.width + 8 for i in ims); H = max(i.height for i in ims)
    sheet = Image.new("RGBA", (W, H), (40, 40, 48, 255)); x = 0
    for i in ims:
        sheet.paste(i, (x, 0)); x += i.width + 8
    sheet.save(out)


# ===================================================================== 確かめ: 目じるしの明るさの差・今のアイコンとの形の重なり
def lab_l(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    y = 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    return 116 * y ** (1 / 3) - 16 if y > 0.008856 else 903.3 * y


def ground_l(kind):
    t = texture(kind)
    cols = t.getcolors(65536)
    tot = sum(n for n, _ in cols)
    return sum(n * lab_l(hx(cc)) for n, cc in cols) / tot


def landmark(name):
    """地面の色でない色のうち、4ドット以上ある色で、地面の平均との明るさの差が 25〜35 のもの（多い順に3つまで）"""
    rows = [l for l in open(os.path.join(HERE, f"{name}.txt")).read().split("\n") if l]
    pal = json.load(open(os.path.join(HERE, f"pal-{name}.json")))
    g = ground_l(TERRAIN[name])
    pure = pure_colors()
    cnt = {}
    for r in rows:
        for ch in r:
            if ch != "." and pal[ch] not in pure:
                cnt[pal[ch]] = cnt.get(pal[ch], 0) + 1
    ok = [(n, col, round(abs(lab_l(col) - g), 1)) for col, n in cnt.items() if n >= 4 and 25 <= abs(lab_l(col) - g) <= 35]
    ok.sort(reverse=True)
    return round(g, 1), ok[:3]


OLD = {"icon-port": ["icon-port"], "icon-village": ["icon-village"], "icon-village-mist": ["icon-village"], "icon-lake": ["icon-lake"],
       "icon-mine": ["icon-mine", "r23:mine3", "r23:mine4"], "icon-tents": ["icon-tents"], "icon-tents-grass": ["icon-tents"],
       "icon-temple": ["icon-temple"], "icon-snowtown": ["icon-snowtown"], "icon-sky": ["icon-sky"], "icon-castle": ["icon-castle"],
       "icon-palace": ["icon-palace"]}


def overlaps(name):
    a, wa, ha = S4.mask(os.path.join(HERE, f"{name}.txt"))
    out = []
    for o in OLD[name]:
        path = os.path.join(R23, o[4:] + ".txt") if o.startswith("r23:") else os.path.join(HERE, "..", "r17-polish", f"{o}.txt")
        b, wb, hb = S4.mask(path)
        best = 0
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                bb = {(x + dx + (wa - wb) // 2, y + dy + (ha - hb)) for (x, y) in b}
                best = max(best, len(a & bb) / max(1, len(a | bb)))
        out.append((o, round(best, 2)))
    return out
