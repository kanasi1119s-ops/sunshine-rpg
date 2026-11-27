import sys; sys.path.insert(0,'/tmp/px4'); from lib import *
import math
g = blank()
def part(keys_or_mask, mat, z_edge=True, **kw):
    """形を置いて陰影を付ける。ふちのうち、すでに描いた部分と接する所は、自分の暗い色で線を引く（重なりの線）"""
    m = keys_or_mask if isinstance(keys_or_mask, set) else mask_from_spans(spans(keys_or_mask))
    cells = shade(m, mat, **kw)
    if z_edge:
        for (x, y) in m:
            for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (x + a, y + b)
                if q not in m and 0 <= q[0] < W and 0 <= q[1] < H and g[q[1]][q[0]] != ".":
                    cells[(x, y)] = RAMP[mat][1]; break
    put(g, cells); return m
def band(p0, p1, r):
    """2点を結ぶ太さ r の帯（うで用）"""
    (x0, y0), (x1, y1) = p0, p1; m = set(); ri = int(math.ceil(r))
    for y in range(min(y0, y1) - ri - 1, max(y0, y1) + ri + 2):
        for x in range(min(x0, x1) - ri - 1, max(x0, x1) + ri + 2):
            dx, dy = x1 - x0, y1 - y0; t = 0 if dx == dy == 0 else max(0, min(1, ((x - x0) * dx + (y - y0) * dy) / (dx * dx + dy * dy)))
            if math.hypot(x - (x0 + t * dx), y - (y0 + t * dy)) <= r: m.add((x, y))
    return m
# ---- うしろの足（右足）とブーツ: 少し後ろ・暗め ----
part([(98, 21, 33), (112, 22, 32), (124, 22, 31), (128, 22, 31), (134, 24, 32), (140, 24, 31), (146, 24, 29)], "skin", peak=0.2, lo=1, hi=6)
part([(146, 24, 30), (150, 24, 30)], "sock", peak=0.2, lo=1, hi=3)
part([(150, 23, 31), (160, 23, 31), (161, 17, 32), (168, 16, 32)], "brown", peak=0.2, lo=1, hi=5)
# ---- 体（シャツ）----
TORSO = part([(44, 19, 30), (46, 17, 32), (49, 15, 33), (52, 14, 33), (57, 14, 33), (61, 15, 33), (66, 17, 32), (72, 18, 32), (76, 18, 32)], "white", peak=0.25, lo=2, hi=8, vgrad=0.25)
# ---- ショートパンツ・ベルト ----
SH = part([(80, 17, 33), (84, 16, 34), (88, 16, 35), (93, 16, 35), (96, 16, 34), (97, 17, 33)], "denim", peak=0.25, lo=3, hi=7, vgrad=0.25, bias=0.1, noise=0.12, seed=4)
import random; _r = random.Random(11)
for x in range(16, 36):                       # すそのほつれ: 白い糸を不ぞろいの長さで
    if (x, 95) not in SH: continue
    n = _r.choice((0, 1, 1, 2, 2, 3)); 
    for k in range(n): g[95 + k][x] = ("2", "t", "x")[min(2, k + _r.randint(0, 1))]
    if _r.random() < 0.3: g[94][x] = "x"
for y in range(81, 95): g[y][26 + (1 if y > 88 else 0)] = "N" if y % 3 else "R"      # 外がわの縫い目
for x, y, c in ((18, 89, "x"), (19, 89, "2"), (20, 89, "x"), (21, 90, "t"), (19, 90, "e"), (22, 90, "x"), (24, 91, "x"), (18, 84, "e"), (19, 84, "e"), (20, 85, "Z"), (30, 88, "x"), (31, 88, "t")):
    if g[y][x] != ".": g[y][x] = c                                                 # ダメージ加工の白いすじ（正面と同じ感じ）
part([(76, 18, 33), (80, 17, 33)], "brown", peak=0.25, lo=2, hi=7, vgrad=0.0)
for y in range(76, 81): g[y][23] = "F"; g[y][31] = "F"          # ベルト通し
for y in range(77, 80): g[y][17] = "i"; g[y][18] = "Q"           # バックルの横はし
for y in range(81, 93): g[y][34] = "G" if y < 92 else g[y][34]  # うしろポケットのはし
for x in range(28, 35): g[82][x] = "e"
# ---- 前の足（左足）----
LEG = part([(98, 18, 31), (104, 18, 31), (112, 19, 30), (120, 19, 29), (124, 19, 28), (127, 18, 28), (130, 20, 28), (134, 20, 29), (138, 21, 29), (142, 21, 27), (146, 21, 26)], "skin", peak=0.3, lo=2, hi=9, vgrad=0.15)
for y in (125, 126, 127): g[y][19] = "y" if y != 127 else "s"   # ひざの光
for y in (126, 127): g[y][27] = "h"                                # ひざのうら
part([(146, 20, 27), (150, 20, 27)], "sock", peak=0.3, lo=1, hi=4)
BOOT = part([(150, 19, 28), (160, 19, 28), (161, 14, 29), (164, 12, 29), (168, 12, 29)], "brown", peak=0.3, lo=1, hi=7, vgrad=0.2)
for x in range(12, 30): g[168][x] = "C"; g[167][x] = "F" if x < 29 else g[167][x]     # くつ底
for y in range(151, 161, 2): g[y][20] = "V"; g[y + 1][21] = "V"                      # ひも
for x in range(19, 29): g[156][x] = "H"; g[157][x] = "L"                             # ベルト
g[156][26] = "i"; g[157][26] = "Q"                                                   # 金具
g[161][19] = "H"; g[162][18] = "H"
# ---- 首・顔 ----
part([(37, 20, 27), (45, 19, 28)], "skin", peak=0.2, lo=2, hi=7)
FL = {12: 14, 13: 13, 14: 13, 15: 12, 16: 12, 17: 12, 18: 12, 19: 12, 20: 12, 21: 12, 22: 12, 23: 12, 24: 13, 25: 13, 26: 13, 27: 13, 28: 12, 29: 11, 30: 10, 31: 11, 32: 12, 33: 12, 34: 12, 35: 12, 36: 13, 37: 13, 38: 14, 39: 16, 40: 19}
FR = {y: (30 if y <= 36 else {37: 28, 38: 26, 39: 24, 40: 22}[y]) for y in FL}
FACE = part({(x, y) for y in FL for x in range(FL[y], FR[y] + 1)}, "skin", peak=0.12, lo=4, hi=9, vgrad=0.12)
# 目（横から: 縦長で細め）
# 目（横から: 前のはしが細く、うしろへ広がる。上まぶたは濃く、下は明るい）
EYE = {(14, 23): "A", (15, 23): "A", (16, 23): "A", (17, 23): "A", (18, 23): "D", (14, 24): "A", (15, 24): "3", (16, 24): "G", (17, 24): "B", (18, 24): "A",
       (14, 25): "x", (15, 25): "8", (16, 25): "8", (17, 25): "G", (18, 25): "t", (14, 26): "x", (15, 26): "9", (16, 26): "8", (17, 26): "8", (18, 26): "t",
       (15, 27): "8", (16, 27): "9", (17, 27): "8", (18, 27): "x", (15, 28): "c", (16, 28): "c", (17, 28): "k"}
put(g, EYE)
put(g, {(19, 22): "D", (19, 23): "D"})                                                # まつげのはね
put(g, {(13, 21): "X", (14, 21): "a", (15, 21): "a", (16, 21): "f"})                # まゆ
put(g, {(17, 30): "p", (18, 30): "n", (19, 30): "p", (17, 31): "p", (18, 31): "p"})   # ほほの赤み
put(g, {(11, 29): "y", (10, 30): "s", (11, 31): "k"})                               # 鼻
put(g, {(12, 33): "D", (13, 33): "D", (14, 32): "k", (12, 34): "I", (13, 34): "U", (14, 34): "D", (12, 35): "D", (13, 35): "c"})   # 開いた口（笑う。舌がのぞく）
# ---- 髪 ----
HAIR = mask_from_spans(spans([(2, 18, 30), (3, 15, 33), (4, 13, 35), (6, 12, 37), (8, 11, 39), (10, 10, 40), (13, 10, 41), (16, 10, 42), (20, 10, 43), (22, 11, 44), (24, 16, 46), (25, 18, 45), (26, 20, 44), (30, 20, 43), (34, 20, 42), (38, 21, 41), (40, 22, 39)]))
# 顔の前（まゆより下・x18 より前）は髪にしない。前髪の毛先はぎざぎざに
for (x, y) in list(HAIR):
    if y >= 21 and x < 20: HAIR.discard((x, y))
    if y in (19, 20) and x < 20 and (x % 3 != 0 if y == 20 else x % 3 == 1): HAIR.discard((x, y))   # 前髪の毛先
    if y >= 18 and x < 12: HAIR.discard((x, y))
for (x, y) in list(HAIR):           # 横の髪とうしろの毛先: 房ごとに長さを変える
    if y >= 36 and ((x // 3) % 2 == (1 if y >= 38 else 2)): HAIR.discard((x, y))
    if y >= 39 and x % 3: HAIR.discard((x, y))
R = RAMP["hair"]; hc = {}
def hclump(x, y):
    # 房: 頭のてっぺん（x24, y3）を中心に、前は前へ、うしろは下へ流れる
    ang = math.atan2(x - 24, y - 1) ; k = ang / 0.32 + 0.8 * math.sin(y / 6)
    return k - math.floor(k)
for (x, y) in HAIR:
    fr = hclump(x, y)
    gl = 1.0 - 0.7 * max(0, (x - 10) / 36) - 0.2 * max(0, (y - 4) / 36)
    cl = -0.38 if fr < 0.14 else 0.22 if fr < 0.45 else 0.08 if fr < 0.75 else -0.12
    light = gl * 0.8 + 0.06 + cl
    r = math.hypot(x - 24, (y - 3) * 1.2)
    if 11 <= r <= 13 and x < 30 and 0.14 <= fr < 0.75: light += 0.3
    if 20 <= x <= 22 and 21 <= y <= 38: light -= 0.1                      # 顔のよこの髪のかげ
    light -= 0.25 * max(0, (y - 32) / 8)
    hc[(x, y)] = R[min(11, 3 + round(max(0, min(1, light)) * 8))]
# 顔と髪のさかい
for (x, y) in HAIR:
    if (x - 1, y) in FACE and (x - 1, y) not in HAIR: hc[(x, y)] = "U"
    if (x, y + 1) in FACE and (x, y + 1) not in HAIR and y >= 17: hc[(x, y)] = "X"
put(g, hc)
# ヘアバンド: 額の上から頭の上を通って、耳のうしろへ
HB = set()
for i in range(41):
    t = i / 40; bx = (1 - t) ** 2 * 12 + 2 * t * (1 - t) * 17 + t * t * 31; by = (1 - t) ** 2 * 11 + 2 * t * (1 - t) * (-5) + t * t * 18
    HB |= band((round(bx), round(by)), (round(bx), round(by)), 1.2)
HB = {p for p in HB if p in HAIR}
put(g, {(x, y): ("g" if (x, y - 1) not in HB else "Y" if (x, y + 1) in HB else "P") if x < 26 else ("Y" if (x - 1, y) not in HB else "P") for (x, y) in HB})
for (x, y) in HB:                     # バンドの下に、髪へ落ちるかげ
    if (x, y + 1) not in HB and (x, y + 1) in HAIR and y + 1 < 21: g[y + 1][x] = "a"
# ---- スカーフ: 首のまわりと、前の結び目 ----
SC = band((18, 43), (29, 41), 1.9) | band((15, 45), (17, 45), 2.2) | band((14, 47), (12, 52), 1.2) | band((16, 48), (17, 52), 1.1)
part(SC, "red", peak=0.2, lo=1, hi=5)
for p in ((15, 46), (16, 46), (13, 48)): g[p[1]][p[0]] = "M"        # 結び目のしわ
for p in ((14, 44), (15, 44)): g[p[1]][p[0]] = "g"
for x, y in ((19, 45), (20, 45), (20, 46), (21, 46), (19, 46)): g[y][x] = "3" if g[y][x] != "." else "."   # えりの先（スカーフの下から）
for x in range(22, 31): g[45][x] = "t" if g[45][x] != "." else "."      # えり
# ---- 前のうで（右うで）: そで → 二の腕 → ひじ → 前うで → 組んだ手 ----
part([(45, 22, 30), (48, 21, 32), (52, 21, 33), (57, 21, 33), (59, 22, 33)], "white", peak=0.25, lo=2, hi=8, vgrad=0.2)
for x in range(22, 34): 
    if g[59][x] != ".": g[59][x] = "j"
part([(60, 23, 31), (63, 24, 31), (66, 25, 31), (68, 26, 30)], "skin", peak=0.25, lo=2, hi=8)
part(band((28, 65), (19, 58), 2.7), "skin", peak=0.35, lo=2, hi=9, vgrad=0.35)
HAND = part([(49, 14, 17), (50, 13, 19), (53, 11, 20), (57, 11, 20), (59, 12, 20), (61, 14, 18)], "skin", peak=0.3, lo=3, hi=9, vgrad=0.1)
for y in (52, 55, 58):                                                  # 指のさかい（前のはしの3本）
    for x in (12, 13, 14): g[y][x] = "h"
    g[y][11] = "D"
for p in ((15, 49), (16, 49), (14, 50)): g[p[1]][p[0]] = "y"            # 親指の光
g[50][17] = "k"; g[51][18] = "k"
outline(g, lambda ch: OUT.get(mat_of(ch), "A"))
SIDE_L = g
SIDE_R = [r[::-1] for r in g]
if __name__ == "__main__":
    import back
    save_png([FRONT, SIDE_L, back.BACK, SIDE_R], "/tmp/px4/four.png", z=4)
    from PIL import Image
    im = Image.open("/tmp/px4/four.png"); w, h = im.size; q = w // 4
    im.crop((q, 0, 2 * q, h // 2)).resize((q * 2, h), Image.NEAREST).save("/tmp/px4/side_zoom.png")
