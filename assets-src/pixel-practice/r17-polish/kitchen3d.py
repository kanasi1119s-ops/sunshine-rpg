"""ユーリの家の台所の家具を、立体の模型から描く（2026-10-06、人間の指示「キッチンもないとおかしいよね」
「家の中に使うオブジェクト全部木の技法で作ってみて」）。道具は sdf3d.py（正面の少し上から、光は左上前から）。
このあと restyle.py --apply kitchen cupboard で、新しい木の感じにする。

  kitchen   調理台（32×38）: 木の戸棚（戸板2枚・とって）、石の天板、石の流し（水）、まな板と野菜、つぼ、
            うしろの壁の横木につるした、おたまと小さな鍋
  cupboard  食器棚（30×42）: 上は棚板が3段（立てた皿・おわん・小さなつぼ）、下は戸板2枚
書き出し: ../r20-props/kitchen.txt / cupboard.txt（prop:kitchen / prop:cupboard。家具の人（NPC）の id に kitchen / cupboard をふくめると、この絵になる）。"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sdf3d import Model, box, rbox, cyl_y, cyl_x, sphere, ellipsoid, capsule, torus_y, diff, render, save

HERE = os.path.dirname(os.path.abspath(__file__))
R20 = os.path.join(HERE, "..", "r20-props")
WOOD = ["#24140a", "#3a2312", "#54341a", "#6e4624", "#8a5a30", "#a6703e", "#be8850", "#d2a066", "#e2b880"]
RAMPS = {
    "wood": WOOD, "door": WOOD, "board": ["#5a3e1c", "#7a5628", "#9a7038", "#b88a4a", "#d0a462", "#e2bc7e"],
    "stone": ["#2e2c2e", "#464348", "#605c62", "#7a767c", "#94909a", "#aeaab2", "#c8c4ca"],
    "water": ["#14304e", "#1f4468", "#2a5a84", "#3e7cac", "#6aa6d0", "#a8d4ee"],
    "iron": ["#1c1e24", "#2e323a", "#464c58", "#646c7a", "#8a92a0", "#b4bcc8"],
    "clay": ["#4a2214", "#6a321c", "#8a4626", "#a85e34", "#c47a48", "#dc9a64"],
    "plate": ["#6a7078", "#8a9098", "#aab0b8", "#c8ccd2", "#e2e4e8", "#f4f6f8"],
    "veg_r": ["#5a1414", "#7e1e1a", "#a02c22", "#c43e2c", "#e0604a"],
    "veg_g": ["#1e3a18", "#2c5222", "#3e6c2c", "#548a3a", "#70a84c"],
    "veg_y": ["#6a4a10", "#8e6618", "#b48a24", "#d4ac3c", "#ecca62"],
    "brass": ["#4a3008", "#7a5410", "#a87a20", "#d4a434", "#f0cc60"],
}


def hn(*a):
    n = 2166136261
    for v in a:
        n = ((n ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    n ^= n >> 15
    return n


def shade(m, p, n, lum, x, y):
    if m in ("wood", "door", "board"):
        lum += ((hn(int(p[1] * 2), int(p[0] // 3)) % 5) - 2) * 0.015      # 板ごとの色・木目
        if m == "door" and abs(n[2]) > 0.7 and (abs(p[0]) % 7.0) < 0.5:
            lum -= 0.12                                                   # 戸板と戸板のすき間
    if m == "stone":
        lum += ((hn(int(p[0] * 2), int(p[2] * 2)) % 5) - 2) * 0.02
    return lum, m


def kitchen():
    m = Model()
    W2, D2 = 14.5, 5.5
    m.add(box((0, 6.0, 0), (W2 - 0.6, 6.0, D2 - 0.6)), "wood")                        # 戸棚の箱
    for sx in (-7.0, 7.0):
        m.add(rbox((sx, 6.4, D2 - 0.4), (6.2, 4.8, 0.35), 0.2), "door")                # 戸板2枚
        m.add(sphere((sx + (-4.6 if sx > 0 else 4.6), 7.0, D2 + 0.1), 0.55), "brass")  # とって
    m.add(box((0, 0.5, 0.3), (W2 - 0.2, 0.5, D2 - 0.3)), "wood")                       # 台輪
    m.add(diff(box((0, 12.9, 0), (W2, 0.9, D2)), box((-7.5, 13.2, 0.3), (4.2, 1.2, 3.4))), "stone")   # 石の天板（流しの穴）
    m.add(box((-7.5, 12.9, 0.3), (4.2, 0.4, 3.4)), "water")                            # 流しの水
    m.add(rbox((3.0, 14.0, 1.0), (4.6, 0.3, 3.0), 0.2), "board")                       # まな板
    m.add(ellipsoid((1.6, 15.1, 1.6), (1.4, 1.1, 1.4)), "veg_r")                        # 野菜（赤）
    m.add(capsule((3.6, 14.7, 2.6), (6.4, 14.7, 1.4), 0.7), "veg_y")                    # 野菜（黄・細長い）
    m.add(ellipsoid((5.2, 15.0, -0.6), (1.2, 1.0, 1.2)), "veg_g")                       # 野菜（緑）
    m.add(cyl_y(10.6, -1.0, 2.2, 13.8, 18.4), "clay")                                   # つぼ
    m.add(torus_y((10.6, 18.4, -1.0), 2.0, 0.5), "clay")
    m.add(box((0, 27.0, -D2 + 0.3), (W2 - 1.0, 0.45, 0.45)), "wood")                   # うしろの壁の横木
    m.add(capsule((-4.0, 26.6, -D2 + 0.6), (-4.0, 19.5, -D2 + 0.9), 0.35), "iron")     # おたまの柄
    m.add(ellipsoid((-4.0, 19.0, -D2 + 1.2), (1.3, 0.9, 1.0)), "iron")                  # おたまの皿
    m.add(capsule((3.0, 26.6, -D2 + 0.6), (3.0, 23.6, -D2 + 0.8), 0.3), "iron")        # 小鍋のつる
    m.add(diff(cyl_x(21.0, -D2 + 1.6, 3.0, 0.4, 5.6), cyl_x(21.0, -D2 + 2.2, 2.4, 1.2, 6.0)), "iron")   # 小鍋（横向き）
    return render(m, 32, 38, 16, 36, RAMPS, shade_fn=shade, outline="#1a120c", ambient=0.22, front_tilt=25)


def cupboard():
    m = Model()
    W2, D2, H = 13.5, 5.0, 38.0
    m.add(diff(box((0, H / 2, 0), (W2, H / 2, D2)), box((0, 25.0, 1.2), (W2 - 1.2, 11.5, D2))), "wood")   # 箱（上は開いた棚）
    for yb in (14.6, 22.5, 30.0):
        m.add(box((0, yb, 0.4), (W2 - 1.1, 0.45, D2 - 0.8)), "wood")                    # 棚板
    for i in range(4):                                                                   # 立てた皿（下の棚。奥の板によりかかる）
        cx = -8.4 + i * 5.6
        m.add(ellipsoid((cx, 18.6, -2.4), (2.9, 2.9, 0.5)), "plate")
        m.add(ellipsoid((cx, 18.6, -1.9), (1.6, 1.6, 0.3)), "plate")
    for i in range(3):                                                                   # おわん（中の棚）
        cx = -8.0 + i * 7.5
        m.add(diff(sphere((cx, 25.6, 0.6), 2.6), box((cx, 27.2, 0.6), (3, 1.6, 3))), "plate")
    m.add(cyl_y(-6.0, 0.4, 1.8, 30.5, 35.0), "clay")                                   # 小さなつぼ（上の棚）
    m.add(cyl_y(1.0, 0.4, 1.4, 30.5, 33.6), "clay")
    m.add(cyl_y(7.0, 0.4, 2.0, 30.5, 34.0), "plate")
    for sx in (-6.6, 6.6):
        m.add(rbox((sx, 7.0, D2 - 0.3), (6.0, 6.0, 0.35), 0.2), "door")                # 下の戸板
        m.add(sphere((sx + (-4.2 if sx > 0 else 4.2), 8.0, D2 + 0.2), 0.55), "brass")
    m.add(box((0, H + 0.6, 0.3), (W2 + 0.8, 0.6, D2 + 0.8)), "wood")                  # 上の飾り板
    return render(m, 30, 42, 15, 40, RAMPS, shade_fn=shade, outline="#1a120c", ambient=0.22, front_tilt=25)


if __name__ == "__main__":
    print("kitchen", save(kitchen(), os.path.join(R20, "kitchen.txt"), os.path.join(R20, "pal-kitchen.json")))
    print("cupboard", save(cupboard(), os.path.join(R20, "cupboard.txt"), os.path.join(R20, "pal-cupboard.json")))
