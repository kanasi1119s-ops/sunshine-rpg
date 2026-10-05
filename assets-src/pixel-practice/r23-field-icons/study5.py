"""洞窟の勉強・5回目（2026-10-05、人間の指示「洞窟はもっと勉強して」）。練習だけで、ゲームには入れない。

4回目の「地形になじむ」作り方（study4.py）と、5回目の「見つける目じるし」のきまり（r26-game-icons/icons.py）を使って、
洞窟の5つの作り方を試す。どれも一から考えたオリジナルの形。今の icon-cave との形の重なりは 0.5 未満にする。
  cave5-cliff     崖の面: 地層の段がある縦の岩の壁に、背の高い暗い口
  cave5-sea       海の洞窟: 海につき出た岩の岬の下に、水が入りこむアーチ
  cave5-overhang  大岩の下: 平たい大きな岩が屋根のようにかぶさり、その下が暗い
  cave5-forest    森の洞窟: 森の木の房と根にかこまれた、苔むした小さな口
  cave5-crystal   水晶の洞窟: 岩の口のまわりに、青く光る水晶のかたまり
出力: cave5-*.txt / pal-cave5-*.json、study5-preview.png
"""
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "r26-game-icons"))

import study4 as S4                                   # noqa: E402
import icons as IC                                    # noqa: E402
from study4 import (GRASS, GSHADE, FOREST, STONE, DIRT, SAND, LIGHT, GLOW, texture, hx, h2, skirt, contact_shadow, tufts, tree)   # noqa: E402
from icons import rock_slope, water, puff, MIST     # noqa: E402
from PIL import Image                                 # noqa: E402


class Canvas(IC.Canvas):
    def save(self, name, trim=True):
        r = IC.Canvas.save(self, name, trim)          # いったん r26 の場所へ（icons.Canvas の決まり）…
        return r

    def save5(self, name):
        S4.HERE = HERE                                # …ではなく、この folder に書き出す
        return S4.Canvas.save(self, name, True)


def mouth(c, cx, top, bot, half, jag=0.0, seed=1):
    """洞窟の口: 上がまるく、ふちは少しでこぼこ。奥ほど暗い（いちばん暗い石の色＋1段上）"""
    for y in range(top, bot + 1):
        for x in range(int(cx - half) - 2, int(cx + half) + 3):
            u = (x + 0.5 - cx) / half
            t = top + (u * u) * (half * 0.8) + (h2(x, y, seed) % 3 - 1) * jag
            if abs(u) <= 1 and y >= t:
                c.put(x, y, STONE[0] if (abs(u) < 0.7 and y > t + 1) else STONE[1], STONE)


# ===================================================================== 1) 崖の面
def cave5_cliff():
    """ふちがぎざぎざの崖。地層は波うつ3段。1回目は四角くて「石の建物」に見えたので、上と横のふちをくずした"""
    c = Canvas()
    skirt(c, 24, 38, 22, 7, "grass", seed=501)
    contact_shadow(c, 4, 44, 40, "grass", depth=2, right=2)
    def top(x):
        return 9 + 3 * math.sin(x * 0.35) + 2 * math.sin(x * 0.9 + 1) + (4 if x < 9 or x > 40 else 0)
    def left(y):
        return 4 + 2.5 * abs(math.sin(y * 0.3)) + (3 if y < 16 else 0)
    def right(y):
        return 44 - 2.5 * abs(math.cos(y * 0.27)) - (3 if y < 18 else 0)
    for y in range(4, 40):
        for x in range(2, 47):
            if y < top(x) or x < left(y) or x > right(y):
                continue
            wav = y - 2 * math.sin(x * 0.25)
            k = int(wav) % 9
            band = int(wav) // 9
            col = [STONE[4], STONE[3], STONE[3], STONE[2], STONE[2]][min(4, band)]
            if k == 0:
                col = STONE[1]
            elif k == 1:
                col = STONE[5] if x < 30 else STONE[4]
            if x > right(y) - 3:
                col = STONE[1] if col not in (STONE[5],) else STONE[2]
            c.put(x, y, col, STONE)
    for x in range(4, 45):                                           # 崖の上の草（ふちにそって）
        t = int(top(x))
        for y in range(t - 2, t + 1):
            if c.get(x, y) is None or y == t - 2 + (h2(x, 1, 3) % 2):
                c.put(x, y, GRASS[4] if y < t else GRASS[2], GRASS)
    mouth(c, 20, 21, 39, 6.5, jag=0.8, seed=2)
    for (x, y, r) in ((38, 6, 3.0), (11, 7, 2.6)):
        tree(c, x, y, r)
    tufts(c, 4, 44, 40, "grass", seed=5, density=0.4)
    c.shadow_edges()
    return c.save5("cave5-cliff")


# ===================================================================== 2) 海の洞窟
def cave5_sea():
    c = Canvas()
    water(c, 24, 42, 23, 8, tex="sea")
    for k in range(0, 360, 5):                                       # 波の白（岩のまわり）
        a = math.radians(k)
        x, y = 24 + math.cos(a) * 18, 37 + math.sin(a) * 5
        if math.sin(a) > 0 and (k // 15) % 2 == 0:
            c.put(x, y, "#a8d0f4")
    # 岬の岩（上は草、手前に海へつき出るアーチ）
    rock_slope(c, {3: 18, 10: 9, 20: 6, 30: 8, 40: 12, 46: 20}, 38, seed=31, n=46)
    for y in range(5, 12):
        for x in range(10, 38):
            if y >= 8 + abs(x - 24) * 0.25 + (h2(x, 2, 1) % 2):
                c.put(x, y, GRASS[4] if y < 10 else GRASS[2], GRASS)
    mouth(c, 25, 26, 38, 8, jag=0.5, seed=3)
    for y in range(34, 39):                                          # 口の中に入りこむ水
        for x in range(19, 32):
            if c.get(x, y) == STONE[0]:
                c.put(x, y, "#1c4890" if (x + y) % 3 else "#2456a4")
    for x in range(20, 31, 3):
        c.put(x, 38, "#5a8ad0")
    c.shadow_edges()
    return c.save5("cave5-sea")


# ===================================================================== 3) 大岩の下
def cave5_overhang():
    """大きな丸い岩が、地面の岩の上にななめにかぶさる。その下のすき間が暗い。1回目は机や家に見えたので、形を岩らしくくずした"""
    c = Canvas()
    skirt(c, 24, 36, 22, 9, "grass", seed=503)
    contact_shadow(c, 6, 42, 38, "grass", depth=3, right=3)
    rock_slope(c, {5: 30, 14: 27, 24: 29, 34: 26, 43: 30}, 38, seed=53, n=26)     # 足もとの岩
    for y in range(27, 38):                                          # すき間の暗がり（下がまるい）
        for x in range(13, 36):
            u = (x + 0.5 - 24) / 11
            if abs(u) <= 1 and y <= 37 - u * u * 6:
                c.put(x, y, STONE[0] if y > 28 else STONE[1], STONE)
    # かぶさる大岩: 山の地形と同じ岩の房を、横長に重ねる（1回目のなめらかなだ円は、空飛ぶ船に見えた）
    rnd = random.Random(11)
    lumps = [(rnd.uniform(6, 42), rnd.uniform(12, 24), rnd.uniform(4.5, 6.5)) for _ in range(9)]
    lumps += [(10, 20, 6), (24, 16, 7.5), (38, 20, 6)]
    for (px_, py_, r) in sorted(lumps, key=lambda p: p[1]):
        for y in range(int(py_ - r), int(py_ + r) + 1):
            for x in range(int(px_ - r * 1.3), int(px_ + r * 1.3) + 1):
                u, v = (x + 0.5 - px_) / (r * 1.3), (y + 0.5 - py_) / r
                d = u * u + v * v
                if d <= 1 and y <= 27:
                    s_ = u * 0.6 + v
                    col = STONE[5] if s_ < -0.8 else STONE[4] if s_ < -0.2 else STONE[3] if s_ < 0.45 else STONE[2]
                    if d > 0.72 and s_ > 0.35:
                        col = STONE[0]
                    c.put(x, y, col, STONE)
    for (x, y) in ((12, 11), (22, 9), (31, 11)):                     # 岩の上の草
        c.put(x, y, GRASS[4], GRASS); c.put(x + 1, y, GRASS[3], GRASS); c.put(x + 1, y - 1, GRASS[4], GRASS)
    c.put(24, 33, LIGHT); c.put(25, 33, "#ff8a2c")
    tufts(c, 6, 42, 38, "grass", seed=7, density=0.4)
    c.shadow_edges()
    return c.save5("cave5-overhang")


# ===================================================================== 4) 森の洞窟
def cave5_forest():
    c = Canvas()
    skirt(c, 24, 32, 22, 13, "grass", seed=504)
    spots = []
    for gy in range(6):
        for gx in range(9):
            x = 3 + gx * 5.2 + (2.6 if gy % 2 else 0)
            y = 6 + gy * 4.4
            if ((x - 24) / 21) ** 2 + ((y - 20) / 15) ** 2 < 1 and not (abs(x - 24) < 9 and y > 18):
                spots.append((x, y, 3.3))
    for (x, y, r) in sorted(spots, key=lambda p: p[1]):
        tree(c, x, y, r)
    # 苔むした岩の小山と口
    for y in range(22, 40):
        for x in range(12, 37):
            d = ((x + 0.5 - 24) / 12) ** 2 + ((y + 0.5 - 39) / 15) ** 2
            if d <= 1:
                s = (x - 24) / 12 + (y - 30) / 15
                col = STONE[4] if s < -0.5 else STONE[3] if s < 0.3 else STONE[2]
                if (h2(x, y, 9) % 5) == 0 and y < 32:
                    col = "#5a8a3a"                                  # 苔
                c.put(x, y, col, STONE)
    mouth(c, 24, 29, 39, 5.5, jag=0.4, seed=4)
    for (x, y) in ((15, 30), (16, 31), (17, 33), (32, 30), (31, 32), (30, 34)):   # 木の根
        c.put(x, y, DIRT[1], DIRT); c.put(x + 1, y, DIRT[0], DIRT)
    contact_shadow(c, 13, 36, 40, "grass", depth=2, right=2)
    tufts(c, 12, 36, 40, "grass", seed=8, density=0.5)
    c.shadow_edges()
    return c.save5("cave5-forest")


# ===================================================================== 5) 水晶の洞窟
def crystal(c, x, yb, h, lean=0):
    for k in range(h):
        y = yb - k
        xx = x + int(lean * k / max(1, h))
        c.put(xx, y, GLOW[2] if k > h - 2 else GLOW[1], GLOW)
        if k < h - 1:
            c.put(xx + 1, y, GLOW[0], GLOW)


def cave5_crystal():
    c = Canvas()
    skirt(c, 30, 37, 17, 6, "grass", seed=505)
    contact_shadow(c, 24, 45, 40, "grass", depth=2, right=2)
    rock_slope(c, {22: 36, 28: 28, 36: 25, 43: 27, 47: 33}, 40, seed=41, n=24)
    mouth(c, 35, 31, 40, 5.5, jag=0.6, seed=5)
    for (x, yb, h, ln) in ((4, 41, 11, -1), (7, 41, 7, 0), (36, 27, 9, 1), (41, 28, 7, 1), (25, 38, 9, -1), (29, 31, 6, 0), (12, 41, 8, 1)):
        crystal(c, x, yb, h, ln)
    c.put(35, 36, GLOW[2]); c.put(36, 37, GLOW[1])                  # 口の奥の光
    tufts(c, 22, 46, 41, "grass", seed=6, density=0.35)
    c.shadow_edges()
    return c.save5("cave5-crystal")


PIECES = [cave5_cliff, cave5_sea, cave5_overhang, cave5_forest, cave5_crystal]
NAMES = ["cave5-cliff", "cave5-sea", "cave5-overhang", "cave5-forest", "cave5-crystal"]
TER = {"cave5-cliff": "grass", "cave5-sea": "sea", "cave5-overhang": "grass", "cave5-forest": "forest", "cave5-crystal": "grass"}


def overlap(name, old="icon-cave"):
    a, wa, ha = S4.mask(os.path.join(HERE, f"{name}.txt"))
    b, wb, hb = S4.mask(os.path.join(HERE, "..", "r17-polish", f"{old}.txt"))
    best = 0
    for dx in range(-4, 5):
        for dy in range(-4, 5):
            bb = {(x + dx + (wa - wb) // 2, y + dy + (ha - hb)) for (x, y) in b}
            best = max(best, len(a & bb) / max(1, len(a | bb)))
    return round(best, 2)


def preview(path, Z=5):
    from PIL import ImageDraw
    from study3_view import terrain, load_icon
    cells = []
    for n in NAMES:
        im = load_icon("r23-field-icons", n)
        bg = terrain(TER[n], im.width + 16, im.height + 16)
        bg.alpha_composite(im, (8, 8))
        cells.append((f"{n}  overlap(icon-cave) {overlap(n)}", bg))
    old = load_icon("r17-polish", "icon-cave")
    bg = terrain("grass", old.width + 16, old.height + 16); bg.alpha_composite(old, (8, 8))
    cells.append(("now: icon-cave", bg))
    W = sum(im.width * Z + 12 for _, im in cells) + 12
    sheet = Image.new("RGBA", (W, 64 * Z + 30), (40, 40, 48, 255))
    dr = ImageDraw.Draw(sheet)
    x = 12
    for label, im in cells:
        sheet.paste(im.resize((im.width * Z, im.height * Z), Image.NEAREST), (x, 8))
        dr.text((x, 8 + im.height * Z + 4), label, fill=(255, 255, 255))
        x += im.width * Z + 12
    # 下に1倍（ゲームの大きさ）を2倍で
    strip = terrain("grass", 64 * 6, 64)
    for i, n in enumerate(NAMES):
        strip.alpha_composite(load_icon("r23-field-icons", n), (8 + i * 62, 8))
    sheet2 = Image.new("RGBA", (max(sheet.width, strip.width * 2), sheet.height + strip.height * 2 + 8), (40, 40, 48, 255))
    sheet2.paste(sheet, (0, 0)); sheet2.paste(strip.resize((strip.width * 2, strip.height * 2), Image.NEAREST), (0, sheet.height + 8))
    sheet2.save(path)


if __name__ == "__main__":
    for f in PIECES:
        print(*f())
    for n in NAMES:
        print(n, "icon-cave との形の重なり", overlap(n), "cave3", overlap(n, "../r23-field-icons/cave3"), "cave4-grass", overlap(n, "../r23-field-icons/cave4-grass"))
    preview(os.path.join(HERE, "study5-preview.png"))
    print("ok")
