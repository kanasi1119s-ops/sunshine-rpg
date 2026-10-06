"""噴水と干し草（牧草）を、立体の模型から描きなおす（2026-10-06、人間の指示
「噴水、牧草はもっとリアルな感じで、細かく立体感で細かいドットを使って作って」「噴水は水が流れるようにして」）。
道具は sdf3d.py。正面の少し上（25度）から見下ろす見え方、光は左上前から。

  fountain / fountain-1〜3   噴水（48×48、4コマ）: 石の丸い水盤（石の段・目地・笠石の輪・根もとのこけ）、水盤の水（深い所ほど暗い青）、
                             まんなかの柱と、中ほどの受け皿、上の小さな皿と玉。水の動き（コマごとに少しずつ下へ流れる）:
                             上の玉から噴き上がって皿へ落ちる水、受け皿のふちから幕のように落ちる水、水面の波の輪と白いあわ、きらめき
  haystack                   干し草の山（32×28）: 丸くもり上がった干し草を、1本ずつのわらのすじで描く（光の側は明るい金色、影は茶色）、
                             しばった縄、根もとにこぼれたわら
ゲームでは prop:fountain, prop:fountain-1〜3 を、順番に見せる（prop-renderer.ts）。
書き出し: ../r20-props/fountain*.txt と haystack.txt（このあと restyle.py --apply fountain fountain-1 fountain-2 fountain-3 haystack で、新しい木の感じにする）。"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sdf3d import Model, cyl_y, cone_y, sphere, torus_y, diff, render, save

HERE = os.path.dirname(os.path.abspath(__file__))
R20 = os.path.join(HERE, "..", "r20-props")
TILT = math.radians(25)
STONE = ["#2c2a30", "#423f46", "#59565e", "#716d75", "#8a868d", "#a39fa4", "#bbb8ba", "#d1cecd", "#e4e2dd", "#f2f0ea"]
RAMPS = {
    "stone": STONE, "cap": STONE,
    "water": ["#0e2036", "#16304e", "#1f4468", "#2a5a84", "#3a729e", "#5590b8", "#7cb0d0", "#a8d0e6"],
    "moss": ["#24381c", "#344e26", "#466830", "#5a823c"],
    "hay": ["#3e2a10", "#5a3e16", "#78561e", "#966e28", "#b48834", "#cca244", "#ddb858", "#eacc72", "#f4de94"],
    "rope": ["#3a2a18", "#56402a", "#76603e", "#988256"],
}


def hn(*a):
    n = 2166136261
    for v in a:
        n = ((n ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    n ^= n >> 15
    return n


def rnd(*a):
    return (hn(*a) & 0xFFFF) / 65535


def scr(x, y, z, CX, GROUND):
    """模型の点 → 絵の上の位置（sdf3d の front_tilt と同じ見え方）。"""
    return CX + x, GROUND - (y * math.cos(TILT) - z * math.sin(TILT))


# ===================================================================== 噴水
def fountain_model():
    m = Model()
    R, Hb = 20.5, 5.0
    m.add(cyl_y(0, 0, R + 1.0, 0, 1.0), "stone")                                   # 土台の段
    m.add(diff(cyl_y(0, 0, R, 0, Hb), cyl_y(0, 0, R - 2.4, 1.0, Hb + 1)), "stone")  # 水盤の石の壁
    m.add(torus_y((0, Hb + 0.2, 0), R - 1.1, 1.45), "cap")                          # 笠石の輪
    m.add(cyl_y(0, 0, R - 2.3, 0, 3.6), "water")                                    # 水盤の水
    m.add(cyl_y(0, 0, 3.4, 0, 2.2), "stone")                                        # 柱の根もと
    m.add(cyl_y(0, 0, 2.4, 0, 16.0), "stone")                                       # 柱
    m.add(torus_y((0, 8.0, 0), 2.6, 0.5), "cap")                                    # 柱の飾りの輪
    m.add(diff(cone_y(0, 0, 2.8, 10.0, 15.0, 18.6), cone_y(0, 0, 2.0, 9.0, 16.6, 19.4)), "stone")   # 中ほどの受け皿
    m.add(torus_y((0, 18.4, 0), 9.5, 0.7), "cap")                                   # 受け皿のふち
    m.add(cyl_y(0, 0, 8.8, 16.8, 18.0), "water")                                    # 受け皿の水
    m.add(cyl_y(0, 0, 1.4, 18.0, 25.5), "stone")                                    # 上の細い柱
    m.add(diff(cone_y(0, 0, 1.5, 4.6, 25.0, 27.0), cone_y(0, 0, 0.9, 3.9, 26.2, 27.6)), "stone")   # 上の小さな皿
    m.add(cyl_y(0, 0, 3.7, 26.2, 26.9), "water")                                    # 上の皿の水
    m.add(sphere((0, 28.2, 0), 1.3), "cap")                                         # 玉（水の出口）
    return m


def fountain_shade(m, p, n, lum, x, y):
    if m in ("stone", "cap"):
        lum += ((hn(int(p[0] * 2), int(p[1] * 2), int(p[2] * 2)) % 5) - 2) * 0.02     # 石のざらつき
        if m == "stone" and abs(n[1]) < 0.6:
            r = math.hypot(p[0], p[2])
            if r > 17 and p[1] < 5.2:                                             # 水盤の壁: 石の段と目地
                if (p[1] / 2.5) % 1 < 0.2:
                    lum -= 0.1
                ang = math.atan2(p[2], p[0])
                if ((ang / (2 * math.pi) * 22 + (0.5 if math.floor(p[1] / 2.5) % 2 else 0)) % 1) < 0.1:
                    lum -= 0.1
                if p[1] < 1.6 and hn(int(ang * 30), 3) % 3 == 0:
                    return lum, "moss"                                            # 根もとのこけ
        if n[1] > 0.7 and m == "cap" and hn(int(p[0] * 3), int(p[2] * 3), 7) % 13 == 0:
            return lum, "moss"
    if m == "water":
        r = math.hypot(p[0], p[2])
        if p[1] > 3 and p[1] < 4:                                                 # 水盤の水面: ふちは浅く明るい、まんなかは深い
            lum = 0.32 + 0.3 * max(0, (r - 12) / 6) + 0.08 * math.sin(p[0] * 0.9 + p[2] * 1.3)
        else:
            lum = 0.5 + 0.12 * math.sin(p[0] * 1.4)
    return lum, m


FOAM = ["#ffffff", "#e6f4fb", "#c2e2f2", "#94c8e4"]


def fountain_frame(f):
    CX, G = 24, 37                                                               # 手前のふち（z=+21）が絵の下におさまる高さ
    img = render(fountain_model(), 48, 48, CX, G, RAMPS, shade_fn=fountain_shade, outline="#1c1e24", ambient=0.2, front_tilt=25)
    put = lambda x, y, c: (0 <= int(x) < 48 and 0 <= int(y) < 48) and img.__setitem__((int(y), int(x)), c)

    def flow(points, phase, bright=True):
        """水のすじ（点の列）。4ドットごとの明るい玉が、コマごとに1ドットずつ下へ流れる。"""
        for k, (x, y) in enumerate(points):
            s = (k - f) % 4
            c = FOAM[0] if s == 0 and bright else (FOAM[1] if s == 1 else (FOAM[2] if s == 2 else FOAM[3]))
            put(x, y, c)

    # 1) 上の玉から噴き上がり、外へ弧をえがいて上の皿・受け皿へ落ちる水（手前がわの4本）
    for a in (-0.35, 0.35, 0.95, -0.95):
        pts = []
        for i in range(14):
            t = i / 13
            r = 1.0 + 3.6 * t
            yy = 28.6 + 3.0 * t - 5.0 * t * t                                      # 上がってから落ちる
            x, y = scr(math.sin(a) * r, yy, math.cos(a) * r * 0.6, CX, G)
            pts.append((round(x), round(y)))
        flow(dict.fromkeys(pts), f)
    # 2) 受け皿のふちから、幕のように水盤へ落ちる水（手前の半分。すじは、ふちにそって数本）
    for j in range(7):
        a = -1.2 + j * 0.4
        pts = []
        for i in range(12):
            t = i / 11
            r = 9.7 + 1.8 * t
            yy = 18.2 - 14.6 * t * t
            x, y = scr(math.sin(a) * r, yy, math.cos(a) * r, CX, G)
            pts.append((round(x), round(y)))
        flow(dict.fromkeys(pts), f + j, bright=j % 2 == 0)
        # 落ちた所の、あわと波の輪（コマごとに広がる）
        bx, by = pts[-1]
        rr = 1 + (f + j) % 4
        for k in range(-rr, rr + 1):
            if (k + f + j) % 2 == 0:
                put(bx + k, by + (1 if abs(k) < rr else 0), FOAM[2] if abs(k) == rr else FOAM[1])
    # 3) 水面のきらめき（コマごとに場所がかわる）
    for k in range(9):
        a = rnd(k, f, 3) * math.pi
        r = 12 + rnd(k, f, 4) * 5
        x, y = scr(math.cos(a) * r, 3.7, math.sin(a) * r, CX, G)
        put(round(x), round(y), FOAM[0] if k % 2 else FOAM[1])
    return img


# ===================================================================== 干し草
def haystack():
    m = Model()
    # 丸くもり上がった干し草（下は少しすぼまり、上はまるい）
    def body(p):
        x, y, z = p[..., 0], p[..., 1], p[..., 2]
        r = np.sqrt(x * x + z * z)
        t = np.clip(y / 22.0, 0, 1)
        rad = 13.2 * np.clip(1 - t, 0, 1) ** 0.6 * (1 + 0.1 * np.sin(t * math.pi))   # 下が広く、上へまるくすぼまる山
        return np.maximum((r - rad) * 0.7, -y)
    m.add(body, "hay")
    t = 3.0 / 22.0                                                                  # 根もとをおさえる縄（1本だけ）
    m.add(torus_y((0, 3.0, 0), 13.2 * (1 - t) ** 0.6 * (1 + 0.1 * math.sin(t * math.pi)) - 0.2, 0.5), "rope")

    def shade(mm, p, n, lum, x, y):
        if mm == "hay":
            # わらのすじ: 表面を、上から下へ流れる細い線（ななめに少しねじれる）。1本ずつ明るさがちがう
            if hn(int(p[0] * 3), int(p[1] * 3), int(p[2] * 3)) % 17 == 0:
                lum += 0.18                                                     # 光を受けた、はみ出したわら
            if p[1] < 1.5:
                lum -= 0.08
        return lum, mm

    def colour(mm, p, n, lum, x, y, c):
        if mm != "hay":
            return c
        # わらのすじ（絵の上で、上から下へ、外がわへ少しかたむいた細い線）。すじごとに明るさがちがい、ところどころで切れる
        lean = (x - 16) * 0.12
        sid = math.floor(x - lean * (y / 4.0))
        seg = (y + hn(sid, 3) % 5) // 4
        off = ((hn(sid, seg, 11) % 5) - 2) * 0.06
        v = min(0.999, max(0.0, lum + off))
        ramp = RAMPS["hay"]
        return ramp[int(v * (len(ramp) - 1))]

    img = render(m, 32, 28, 16, 21.5, RAMPS, shade_fn=shade, colour_fn=colour, outline="#3a2610", ambient=0.2, front_tilt=25)
    # はみ出したわら（上と横に、1〜3ドットの細い線）と、根もとにこぼれたわら
    for k in range(16):
        ys = [y for y in range(28) for x in range(32) if img[y, x] not in ("", "#3a2610") and len(img[y, x]) == 7]
        if not ys:
            break
        y = min(ys) + int(rnd(k, 1) * 14)
        row = [x for x in range(32) if img[y, x] == "#3a2610"]
        if not row:
            continue
        x = row[0] if k % 2 else row[-1]
        dx = -1 if k % 2 else 1
        for i in range(1 + hn(k, 2) % 3):
            if 0 <= x + dx * i < 32 and 0 <= y - i // 2 < 28 and img[y - i // 2, x + dx * i] in ("", "#3a2610"):
                img[y - i // 2, x + dx * i] = RAMPS["hay"][6 if k % 2 else 3]
    for k in range(9):
        x = 3 + int(rnd(k, 7) * 26)
        y = 25 + hn(k, 8) % 3
        if img[y, x] == "" or len(img[y, x]) > 7:
            img[y, x] = RAMPS["hay"][5 + k % 3]
            if x + 1 < 32 and (img[y, x + 1] == "" or len(img[y, x + 1]) > 7):
                img[y, x + 1] = RAMPS["hay"][4]
    return img


if __name__ == "__main__":
    for f in range(4):
        name = "fountain" if f == 0 else f"fountain-{f}"
        print(name, save(fountain_frame(f), os.path.join(R20, name + ".txt"), os.path.join(R20, "pal-" + name + ".json")))
    print("haystack", save(haystack(), os.path.join(R20, "haystack.txt"), os.path.join(R20, "pal-haystack.json")))
