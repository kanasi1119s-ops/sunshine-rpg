"""家の中の階段を、立体の模型から描く（2026-10-06、人間の指示「階段もちゃんとしたのを作ろう」）。
道具は sdf3d.py（正面の少し上から見下ろす見え方、光は左上前から）。このあと restyle.py --apply stairs-up stairs-down で、木の感じにする。

  stairs-up    上り階段（48×48。3マス幅）: 奥の壁ぞいに、左から右へ上がっていく木の階段。踏み板と正面の板（継ぎ目）、
               手前の手すり（親柱・細い柱・ななめの手すり）、上の階へぬける天井の暗い口。いちばん左の段が上り口
  stairs-down  床の下り口（20×20）: 床にあいた四角い口と、奥へ下がっていく段、口のまわりの床の縁板、左がわの手すり
書き出し: ../r20-props/stairs-up.txt / stairs-down.txt（prop:stairs-up / prop:stairs-down）。"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sdf3d import Model, box, rbox, cyl_y, diff, render, save

HERE = os.path.dirname(os.path.abspath(__file__))
R20 = os.path.join(HERE, "..", "r20-props")
WOOD = ["#24140a", "#3a2312", "#54341a", "#6e4624", "#8a5a30", "#a6703e", "#be8850", "#d2a066", "#e2b880"]
RAMPS = {
    "tread": WOOD, "riser": WOOD, "under": WOOD, "string": WOOD, "rail": WOOD, "post": WOOD, "trim": WOOD,
    "void": ["#0a0806", "#120e0a", "#1a140e", "#221a12"],
}


def hn(*a):
    n = 2166136261
    for v in a:
        n = ((n ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    n ^= n >> 15
    return n


def shade(m, p, n, lum, x, y):
    if m in ("tread", "riser", "string", "trim", "rail", "post"):
        # 木目（板の長い向きにそったすじ）と、板ごとの色のちがい
        lum += ((hn(int(p[1] * 2), int(p[2] * 2)) % 5) - 2) * 0.012
        if m == "tread":
            if (p[0] * 0.9 + p[2] * 0.2) % 3.1 < 0.35:
                lum -= 0.05
            lum += 0.06                                            # 踏み板の上の面は、すり減って少し明るい
        if m == "riser":
            lum -= 0.04
        if m == "under":
            lum -= 0.2                                             # 階段の下は、奥まって暗い
    if m == "void":
        lum = min(lum, 0.3) * 0.6
    return lum, m


def stairs_up():
    """壁ぞいに、左から右へ上がっていく階段（48×48。正面から見ると、段の形がそのまま見える）。"""
    m = Model()
    n, rise, run = 8, 4.4, 5.0
    x0 = -20.0
    zb, zf = -6.0, 1.0                                             # 奥（壁）と手前
    for i in range(n):
        xa = x0 + i * run
        y1 = (i + 1) * rise
        m.add(box((xa + run / 2, y1 - 0.5, (zb + zf) / 2 + 0.3), (run / 2 + 0.25, 0.5, (zf - zb) / 2 + 0.3)), "tread")   # 踏み板（少し手前へ出る）
        m.add(box((xa + run / 2, y1 - rise / 2 - 0.5, (zb + zf) / 2), (run / 2, rise / 2, (zf - zb) / 2)), "riser")      # 段の正面の板（蹴込み）
        m.add(box((xa + run / 2, (y1 - 1) / 2, (zb + zf) / 2 - 1.2), (run / 2, (y1 - 1) / 2, (zf - zb) / 2 - 1.2)), "under")  # 階段の下（少し奥まった板の壁）
    # 手前の手すり: 下の親柱、各段の細い柱、ななめの手すり
    L = math.hypot(n * run, n * rise)
    ang = math.atan2(n * rise, n * run)
    m.add(rbox((x0 + 0.8, 6.5, zf + 0.4), (0.9, 6.5, 0.9), 0.3), "post")
    for i in range(1, n, 2):
        m.add(box((x0 + i * run + run / 2, (i + 1) * rise + 3.6, zf + 0.4), (0.3, 3.6, 0.3)), "post")

    def rail(p):
        q = p - np.array([x0 + n * run / 2 + 0.8, n * rise / 2 + 9.0, zf + 0.4])
        c, s_ = math.cos(ang), math.sin(ang)
        u = q[..., 0] * c + q[..., 1] * s_
        v = -q[..., 0] * s_ + q[..., 1] * c
        d = np.stack([np.abs(u) - L / 2 - 0.6, np.abs(v) - 0.6, np.abs(q[..., 2]) - 0.6], -1)
        return np.minimum(np.max(d, -1), 0) + np.linalg.norm(np.maximum(d, 0), axis=-1)
    m.add(rail, "rail")
    # 上の階へぬける天井の口（いちばん上の段の上の、暗い所）
    m.add(box((x0 + n * run - 3.0, n * rise + 4.0, zb - 0.6), (5.0, 4.0, 0.6)), "void")

    def colour(mm, p, nn, lum, x, y, c):
        if mm == "under" and nn[2] > 0.7 and abs((p[0] - x0) % 6.0 - 3.0) < 0.4:
            return WOOD[1]                                          # 階段の下の板壁の、たての継ぎ目
        return c
    return render(m, 48, 48, 24, 45, RAMPS, shade_fn=shade, colour_fn=colour, outline="#1a120a", ambient=0.22, front_tilt=25)


def stairs_down():
    """床にあいた下り口（20×20）。床の口は正面の少し上からだと中が見えないので、絵として描く:
    四方の縁板（左上が明るく、右下が暗い）、口の中に奥へ下がっていく段（踏み板と蹴込み。奥ほど暗い）、左がわの手すり。"""
    W, H = 20, 20
    img = np.full((H, W), "", dtype=object)
    x0, x1, y0, y1 = 3, 17, 5, 18                                   # 口の外がわ（縁板をふくむ）
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            edge = x in (x0, x1) or y in (y0, y1)
            if edge:
                img[y, x] = WOOD[6] if (x == x0 or y == y0) else WOOD[3]   # 縁板（光の側は明るい）
            else:
                # 段: 下（手前）から上（奥）へ、3ドットごとに1段下がる。踏み板（上2ドット）と蹴込み（下1ドット）
                k = (y1 - 1 - y)                                    # 手前からの距離
                step = k // 3
                tread = k % 3 != 0
                base = 5 - step                                     # 奥ほど暗い
                c = max(0, base if tread else base - 2)
                if x == x0 + 1:
                    c = max(0, c - 1)                               # 左のかべぎわの影
                img[y, x] = WOOD[c] if c > 0 else RAMPS["void"][1]
    for y in range(y0 + 1, y1):                                     # 右と上の縁板の内がわの影
        img[y, x1 - 1] = WOOD[max(0, WOOD.index(img[y, x1 - 1]) - 1)] if img[y, x1 - 1] in WOOD else img[y, x1 - 1]
    # 左がわの手すり: 柱2本（上と下）と横木
    for (py, h) in ((y0 - 1, 5), (y1 - 1, 5)):
        for i in range(h):
            img[py - i, 1] = WOOD[6] if i < h - 1 else WOOD[7]
            img[py - i, 2] = WOOD[3]
    for y in range(y0 - 5, y1 - 4):
        img[y, 1] = WOOD[6]
        img[y, 2] = WOOD[4]
    # 縁板の外がわに、うすい接地の影
    for x in range(x0, x1 + 2):
        if img[y1 + 1, x] == "":
            img[y1 + 1, x] = "#10201840"
    return img


if __name__ == "__main__":
    print("stairs-up", save(stairs_up(), os.path.join(R20, "stairs-up.txt"), os.path.join(R20, "pal-stairs-up.json")))
    print("stairs-down", save(stairs_down(), os.path.join(R20, "stairs-down.txt"), os.path.join(R20, "pal-stairs-down.json")))
