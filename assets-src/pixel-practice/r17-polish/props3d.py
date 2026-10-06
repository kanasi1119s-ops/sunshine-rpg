"""井戸と、町の像3つを、立体の模型から描く（2026-10-06、人間の指示「井戸はもっとこだわって」「像とかもすべて立体感を追及して」）。
道具は sdf3d.py（church3d.py と同じ作り方）。光は左上前から、影・すみの暗さつき。すべて一から自作。

  well             井戸: 石を積んだ丸い井戸（石の段と目地・上の笠石の輪・こけ）、水面、2本の木の柱、瓦の小さな屋根、
                   巻き上げの木の軸と取っ手、つな、つり下がった桶（鉄のたが）
  statue-traveler  旅人の像（石）: 台座（土台と笠石）、フードのある外套の旅人、長い杖、背中の荷
  statue-soldier   兵士の像（青銅の緑青）: 石の台座、かぶと・肩当て・丸い盾・槍
  statue-winged    つばさの像（白い大理石）: 台座、衣の人が、三つの環のしるしの輪を両手でかかげ、背中に大きなつばさ
書き出し: well は r17-polish/well.txt、像は r20-props/statue-*.txt（前の平らな絵を上書き。大きさは 48×48 の枠におさまる）。"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sdf3d import (Model, box, rbox, cyl_y, cyl_x, cone_y, sphere, ellipsoid, capsule, torus_y, gable_x, diff, render, save)

HERE = os.path.dirname(os.path.abspath(__file__))
R20 = os.path.join(HERE, "..", "r20-props")

STONE = ["#2a282e", "#423f46", "#5b5860", "#76727a", "#918d94", "#aca8ae", "#c6c3c6", "#dddbda", "#efeeea"]
RAMPS = {
    "stone": STONE,
    "cap": STONE,
    "wood": ["#26150a", "#3c2210", "#583218", "#764422", "#94582e", "#b2703c", "#cc8c52"],
    "roof": ["#341212", "#541c1a", "#742822", "#96382c", "#b65034", "#d27048", "#ea9464"],
    "water": ["#0c1a2e", "#142a46", "#1c3e64", "#285a86", "#3e7cac", "#6aa6d0", "#a8d4ee"],
    "rope": ["#3e3020", "#5e4c32", "#80704e", "#a4946e", "#c4b690"],
    "iron": ["#202228", "#363a44", "#525866", "#747c8a", "#a0a8b4"],
    "moss": ["#24381c", "#344e26", "#466830", "#5a823c", "#74a04a"],
    "bronze": ["#14221e", "#20342e", "#2e4a42", "#3e6258", "#527c6e", "#6c9884", "#8cb49e", "#b0d0ba"],
    "marble": ["#3c3c48", "#585866", "#767686", "#9494a4", "#b0b0be", "#c8c8d4", "#dcdce6", "#ececf2", "#f8f8fc"],
    "figure": ["#2c2a2e", "#46424a", "#625e66", "#807a82", "#9e98a0", "#bab4ba", "#d4d0d2", "#eae8e6"],
    "wing": ["#3c3c48", "#585866", "#767686", "#9494a4", "#b0b0be", "#c8c8d4", "#dcdce6", "#ececf2", "#f8f8fc"],
    "gold": ["#4a3008", "#7a5410", "#a87a20", "#d4a434", "#f0cc60", "#fff0a8"],
}


def hn(*a):
    n = 2166136261
    for v in a:
        n = ((n ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    n ^= n >> 15
    return n


def vnoise(x, y, z, s):
    xi, yi, zi = math.floor(x / s), math.floor(y / s), math.floor(z / s)
    return (hn(xi, yi, zi) & 0xFFFF) / 65535


def common_shade(m, p, n, lum, x, y):
    """石の段と目地・上を向いた所のこけ・瓦の段・水面のゆらぎ。"""
    if m in ("stone", "cap", "marble"):
        if m == "stone" and abs(n[1]) < 0.6:
            course = math.floor(p[1] / 2.6)
            if (p[1] / 2.6) % 1 < 0.2:
                lum -= 0.09                                        # 横の目地
            else:
                ang = math.atan2(p[2], p[0]) * 9 / math.pi + (course % 2) * 0.5
                along = ang if getattr(common_shade, "round", False) else (p[0] + p[2] + (course % 2) * 2.5) / 5
                if along % 1 < 0.12:
                    lum -= 0.07                                    # たての目地
                lum += ((hn(course, math.floor(along)) % 5) - 2) * 0.02
        if n[1] > 0.55 and vnoise(p[0] + 0.3, p[1], p[2], 1.6) > 0.62 and m != "marble":
            return lum + 0.05, "moss"                               # 上を向いた所のこけ
        if p[1] < 2.0 and m == "stone":
            lum -= 0.06                                            # 足もとのよごれ
    if m == "roof":
        if (p[1] / 1.6) % 1 < 0.28:
            lum -= 0.12
        elif ((p[0] + (math.floor(p[1] / 1.6) % 2) * 1.5) / 3.0) % 1 < 0.15:
            lum -= 0.07
    if m == "wood":
        if ((p[0] * 0.3 + p[1] * 2.1 + p[2] * 0.3) % 1.7) < 0.25:
            lum -= 0.06                                            # 木目
    if m == "wing":
        if (p[1] * 0.9 - abs(p[0]) * 0.5) % 1.6 < 0.35:
            lum -= 0.12                                            # 羽の段
    if m == "water":
        lum = 0.45 + 0.25 * math.sin(p[0] * 1.3 + p[2] * 0.7) * math.sin(p[2] * 1.1 - p[0] * 0.4) + (0.18 if (p[0] + p[2]) < -6 else 0)
    return lum, m


# ===================================================================== 井戸
def well():
    m = Model()
    R = 9.5
    common_shade.round = True
    ring = diff(cyl_y(0, -1, R, 0, 8), cyl_y(0, -1, R - 2.2, 0.8, 9))
    m.add(ring, "stone")
    m.add(torus_y((0, 8.2, -1), R - 1.1, 1.35), "cap")            # 笠石の輪
    m.add(cyl_y(0, -1, R - 2.2, 0, 4.6), "water")
    for sx in (-R - 0.2, R + 0.2):                                 # 柱と、柱の足もとの石
        m.add(box((sx, 17.5, -1), (1.1, 10.5, 1.1)), "wood")
        m.add(box((sx, 7.0, -1), (1.7, 1.0, 1.7)), "stone")
        m.add(capsule((sx, 23.5, -1), (sx * 0.62, 26.6, -1), 0.45), "wood")   # 腕木
    m.add(gable_x(-R - 3.5, R + 3.5, -7.0, 5.0, 26.6, 33.0), "roof")
    m.add(box((0, 33.1, -1), (R + 3.6, 0.45, 0.6)), "roof")         # 棟
    m.add(cyl_x(21.5, -1, 1.25, -R + 0.9, R - 0.9), "wood")         # 巻き上げの軸
    for xx in (-R + 2.0, R - 2.0):
        m.add(cyl_x(21.5, -1, 1.5, xx - 0.3, xx + 0.3), "iron")
    m.add(capsule((R + 1.0, 21.5, -1), (R + 2.6, 21.5, -1), 0.35), "iron")      # 取っ手
    m.add(capsule((R + 2.6, 21.5, -1), (R + 2.6, 19.0, 0.2), 0.35), "iron")
    m.add(capsule((R + 2.6, 19.0, 0.2), (R + 3.4, 19.0, 0.2), 0.5), "wood")
    m.add(cyl_x(21.5, -1, 1.45, -1.2, 1.2), "rope")                  # 軸に巻いたつな
    m.add(capsule((0.4, 21.0, -1), (0.4, 13.6, -1), 0.32), "rope")
    bucket = diff(cone_y(0.4, -1, 2.0, 2.5, 9.8, 13.4), cyl_y(0.4, -1, 1.8, 10.6, 14))
    m.add(bucket, "wood")
    for yb in (10.6, 12.6):
        m.add(diff(cyl_y(0.4, -1, 2.35 + (yb - 9.8) * 0.12, yb, yb + 0.45), cyl_y(0.4, -1, 1.9, 9, 15)), "iron")
    m.add(capsule((-1.9, 13.4, -1), (0.4, 14.3, -1), 0.2), "iron")
    m.add(capsule((2.7, 13.4, -1), (0.4, 14.3, -1), 0.2), "iron")
    img = render(m, 48, 48, 24, 45, RAMPS, shade_fn=common_shade, shadow=(27.5, 45.8, 15.5, 2.8))
    common_shade.round = False
    return img


# ===================================================================== 像
def pedestal(m, w, d, hgt, mat="stone"):
    m.add(box((0, 0.6, 0), (w / 2 + 1.0, 0.6, d / 2 + 1.0)), mat)                  # 土台の段
    m.add(box((0, hgt / 2, 0), (w / 2, hgt / 2, d / 2)), mat)                        # 胴
    m.add(box((0, hgt - 0.5, 0), (w / 2 + 0.8, 0.55, d / 2 + 0.8)), "cap")           # 笠石
    m.cut(box((0, hgt * 0.5, d / 2 + 0.2), (w / 2 - 1.6, hgt * 0.22, 0.45)))         # 正面の銘板のくぼみ


def statue_traveler():
    m = Model()
    ph = 7.0
    pedestal(m, 12, 9, ph)
    S = "figure"; b = ph
    robe = cone_y(0, 0, 4.4, 2.8, b, b + 15)
    m.add(robe, S)                                                      # 外套のすそ（広がる）
    for ang in (-1.0, -0.3, 0.4, 1.1):                                  # すそのひだ（たてのみぞ）
        m.cut(capsule((math.sin(ang) * 4.3, b + 0.5, math.cos(ang) * 4.3), (math.sin(ang) * 2.9, b + 13, math.cos(ang) * 2.9), 0.45))
    m.add(capsule((0, b + 14, 0), (0, b + 21, 0), 2.6, 2.3), S)        # 胸
    m.add(capsule((-2.5, b + 21.3, 0), (2.5, b + 21.3, 0), 1.2), S)    # 肩
    m.add(rbox((0, b + 18.5, -2.9), (2.2, 3.0, 1.2), 0.7), "stone")     # 背中の荷（台座と同じ石の色で、体とわける）
    m.add(capsule((0, b + 22.3, 0), (0, b + 23.6, 0), 1.0), S)          # 首
    m.add(sphere((0, b + 25.3, 0.3), 2.25), S)                          # 頭
    m.add(diff(ellipsoid((0, b + 25.9, -0.4), (2.7, 2.9, 2.6)), box((0, b + 24.8, 2.6), (1.7, 2.0, 1.9))), S)   # フード
    m.add(capsule((2.5, b + 21.0, 0), (4.4, b + 17.0, 1.5), 0.9), S)   # 右うで（杖をもつ）
    m.add(sphere((4.6, b + 16.7, 1.6), 0.95), S)                        # 右手
    m.add(capsule((-2.5, b + 21.0, 0), (-3.1, b + 14.5, 0.6), 0.9), S)  # 左うで
    m.add(capsule((4.9, b + 0.4, 1.6), (5.4, b + 30.0, 1.4), 0.55), "bronze")   # 杖（青銅）
    m.add(torus_y((5.4, b + 30.4, 1.4), 0.9, 0.35), "bronze")
    return render(m, 48, 48, 24, 46, RAMPS, shade_fn=common_shade, shadow=(26.5, 46.6, 12.5, 2.3))


def statue_soldier():
    m = Model()
    ph = 10.0
    pedestal(m, 12, 9, ph)
    B = "bronze"; b = ph
    for sx in (-1.4, 1.4):
        m.add(capsule((sx, b + 0.6, 0), (sx, b + 9.5, 0), 1.25, 1.45), B)      # 足
    m.add(cone_y(0, 0, 3.6, 2.6, b + 7.5, b + 12), B)                         # 腰の垂れ
    m.add(capsule((0, b + 11.5, 0), (0, b + 18.5, 0), 2.6, 2.9), B)          # 胴
    for sx in (-3.0, 3.0):
        m.add(sphere((sx, b + 18.6, 0), 1.6), B)                               # 肩当て
    m.add(capsule((0, b + 19.5, 0), (0, b + 21.0, 0), 1.0), B)               # 首
    m.add(sphere((0, b + 22.6, 0.2), 2.0), B)                                 # 頭
    m.add(diff(sphere((0, b + 23.0, 0), 2.45), box((0, b + 22.0, 2.4), (1.4, 1.2, 1.4))), B)  # かぶと
    m.add(capsule((0, b + 25.2, -1.2), (0, b + 25.6, 1.4), 0.55), B)         # かぶとの飾り
    m.add(capsule((3.0, b + 18.0, 0), (4.4, b + 13.5, 1.2), 0.9), B)         # 右うで
    m.add(capsule((5.0, b + 0.5, 1.4), (5.0, b + 31.0, 1.4), 0.42), B)       # 槍
    m.add(cone_y(5.0, 1.4, 0.9, 0.05, b + 31.0, b + 34.0), "bronze")        # 穂先
    m.add(capsule((-3.0, b + 18.0, 0), (-4.0, b + 14.0, 1.6), 0.9), B)       # 左うで
    shield = lambda p: np.maximum(np.sqrt((p[..., 0] + 4.4) ** 2 + (p[..., 1] - (b + 12.5)) ** 2) - 3.6, np.abs(p[..., 2] - 2.6) - 0.5)
    m.add(shield, B)
    m.add(sphere((-4.4, b + 12.5, 3.1), 0.9), "gold")                        # 盾のまんなかの金具
    return render(m, 48, 48, 24, 46, RAMPS, shade_fn=common_shade, shadow=(26.5, 46.6, 13, 2.3))


def statue_winged():
    m = Model()
    ph = 9.0
    pedestal(m, 13, 9, ph, "marble")
    M = "marble"; b = ph
    m.add(cone_y(0, 0, 4.2, 2.4, b, b + 15), M)                      # 衣のすそ
    m.add(capsule((0, b + 14, 0), (0, b + 20, 0), 2.4, 2.2), M)       # 胸
    m.add(sphere((0, b + 22.8, 0.3), 1.9), M)                         # 頭
    m.add(ellipsoid((0, b + 22.6, -0.8), (2.0, 2.4, 1.8)), M)         # 髪
    for sx in (-1, 1):
        m.add(capsule((sx * 2.2, b + 19.6, 0), (sx * 2.6, b + 25.0, 1.0), 0.75), M)          # うで（上へ）
        # つばさ: 肩のうしろから、外へ上へひろがる、うすい楕円を2まい重ねる
        m.add(ellipsoid((sx * 5.4, b + 22.0, -2.8), (3.8, 6.4, 0.9)), "wing")
        m.add(ellipsoid((sx * 7.6, b + 18.0, -3.1), (2.6, 4.6, 0.7)), "wing")
    # かかげた輪（三つの環のしるし）
    m.add(lambda p: np.sqrt((np.sqrt((p[..., 0]) ** 2 + (p[..., 1] - (b + 27.6)) ** 2) - 2.7) ** 2 + (p[..., 2] - 1.0) ** 2) - 0.5, "gold")
    m.add(lambda p: np.sqrt((np.sqrt((p[..., 0]) ** 2 + (p[..., 1] - (b + 27.6)) ** 2) - 1.4) ** 2 + (p[..., 2] - 1.0) ** 2) - 0.4, "gold")
    return render(m, 48, 48, 24, 46, RAMPS, shade_fn=common_shade, shadow=(26.5, 46.6, 15, 2.3), outline="#24222a")


if __name__ == "__main__":
    todo = sys.argv[1:] or ["well", "statue-traveler", "statue-soldier", "statue-winged"]
    for n in todo:
        img = globals()[n.replace("-", "_")]()
        d = HERE if n == "well" else R20
        print(n, save(img, os.path.join(d, n + ".txt"), os.path.join(d, "pal-" + n + ".json")))
