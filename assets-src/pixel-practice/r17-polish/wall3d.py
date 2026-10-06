"""町を囲む石の塀を、立体の模型から描きなおす（2026-10-06、人間の指示「塀も立体感、光り加減、リアルな感じ、細かいドットすべてこだわって」）。
道具は sdf3d.py。光は左上前から。石は1つずつ角の丸い石（大きさ・出っぱり・色合いをかえる）で、石と石のあいだは奥へ下がった目地。
となりのタイルとつながるよう、石の並びは横 16 ごとにくり返す（はしの石は、となりへ続く）。

  townwall-h / -h2   横の塀（町の上と下のはし）: 正面の少し上から見る。積んだ石の面と、上の笠石（少し張り出す）、根もとのこけ
  townwall-v / -v2   たての塀（町の左右のはし）: 真上から見る。笠石の上の面（板石がたてに並ぶ）と、右へ落ちる影
  townwall-post      角と門の柱（16×28）: 一段高い角柱。石の段・笠石・灯りの環の飾り石（金）
書き出し: ../r20-props/townwall-*.txt と pal-townwall-*.json（前の平らな絵 townwall.py の版を上書き）。"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sdf3d import Model, box, rbox, torus_y, render, save

HERE = os.path.dirname(os.path.abspath(__file__))
R20 = os.path.join(HERE, "..", "r20-props")
STONE = ["#3a3630", "#4e4942", "#635d55", "#78726a", "#8e877e", "#a49d93", "#b9b2a7", "#cdc7bc", "#e0dbd1", "#efebe3"]
RAMPS = {
    "stone": STONE, "cap": STONE,
    "mortar": ["#24201c", "#302b26", "#3c3630", "#48413a"],
    "moss": ["#24361a", "#304822", "#3e5a2a", "#4e6e34", "#5e8040"],
    "gold": ["#4a3008", "#7a5410", "#a87a20", "#d4a434", "#f0cc60", "#fff0a8"],
}


def hn(*a):
    n = 2166136261
    for v in a:
        n = ((n ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    n ^= n >> 15
    return n


def rnd(*a):
    return (hn(*a) & 0xFFFF) / 65535


def shade(m, p, n, lum, x, y):
    if m in ("stone", "cap"):
        # 石ごとの色合い（石のまんなかの位置で決める）と、表面のこまかなざらつき・欠け
        key = (math.floor(p[0] / 2.0), math.floor(p[1] / 2.0), math.floor(p[2] / 2.0))
        lum += ((hn(*key) % 7) - 3) * 0.018
        lum += ((hn(int(p[0] * 3), int(p[1] * 3), int(p[2] * 3)) % 5) - 2) * 0.02
        if n[1] > 0.6 and m == "stone" and rnd(int(p[0] * 2), int(p[2] * 2), 5) > 0.82:
            return lum, "moss"                                  # 上を向いた石の段に、こけ
        if p[1] < 1.6 and m == "stone":
            lum -= 0.08 * (1.6 - p[1])                          # 根もとは、しめって暗い
    return lum, m


def colour(m, p, n, lum, x, y, c):
    if m == "stone" and p[1] < 1.2 and rnd(x, 7) > 0.6:
        return RAMPS["moss"][2 if lum > 0.4 else 1]             # 根もとのこけ・草
    return c


def wall_h(variant):
    """横の塀。幅 16 を3回ならべた模型を描き、まんなかの 16 を切り出す（はしの石が、となりのタイルへ続く）。"""
    m = Model()
    Hw, D = 11.0, 5.0
    m.add(box((0, Hw / 2, -D / 2), (24, Hw / 2, D / 2 - 0.4)), "mortar")      # 目地（石のうしろの、奥へ下がった面）
    rows = [(0.0, 3.8), (3.8, 7.4), (7.4, 11.0)]
    for ri, (y0, y1) in enumerate(rows):
        # 1つの周期（16）の中で石を並べ、それを左右へ写す（となりのタイルとつながる）。段ごとに目地をずらす
        start = -8.0 + ((ri * 5 + variant * 7) % 8)
        cuts = [start]
        k = 0
        while cuts[-1] < start + 16 - 3.5:
            cuts.append(min(start + 16, cuts[-1] + 4.0 + rnd(k, ri, variant) * 2.5))
            k += 1
        cuts[-1] = start + 16
        for i in range(len(cuts) - 1):
            xa, xb = cuts[i] + 0.5, cuts[i + 1] - 0.5
            out = 0.3 + rnd(i, ri, variant + 3) * 0.6                  # 石ごとの出っぱり（目地より前へ）
            for rep in (-32, -16, 0, 16, 32):
                m.add(rbox(((xa + xb) / 2 + rep, (y0 + y1) / 2, -D / 2 + out / 2), ((xb - xa) / 2, (y1 - y0) / 2 - 0.45, D / 2 - 0.2 + out / 2), 0.7), "stone")
    # 笠石（上の、少し張り出した板石。2まいずつ）
    for i in range(2):
        cx = -8 + i * 8 + 4 + (variant * 3 % 8)
        for rep in (-32, -16, 0, 16, 32):
            m.add(rbox((cx + rep, Hw + 0.9, -D / 2 + 0.2), (3.7, 0.9, D / 2 + 0.7), 0.4), "cap")
    img = render(m, 48, 24, 24, 22, RAMPS, shade_fn=shade, colour_fn=colour, outline="#24201c", ground_contact=True, ambient=0.16)
    return img[8:24, 16:32]


def wall_v(variant):
    """たての塀。真上から見た笠石の上の面（左上の光で、板石ごとに上のふちが明るく下のふちが暗い）と、
    影になる右の側面（石の段と目地）、その右の地面へ落ちる影。たて 16 ごとにくり返す（2026-10-06 描きなおし）。"""
    out = np.full((16, 16), "", dtype=object)
    S = STONE
    joints = [(0 + variant * 3) % 16, (5 + variant * 3) % 16, (11 + variant * 3) % 16]
    slab = {}
    sid = 0
    for y in range(16):
        if y in joints:
            sid += 1
        slab[y] = sid % 3
    for y in range(16):
        j = y in joints
        below_j = (y + 1) % 16 in joints
        above_j = (y - 1) % 16 in joints
        tone = [0, 1, -1][slab[y]] + (variant % 2)
        for x in range(2, 12):
            if j:
                c = "#302b26" if x > 2 else S[3]                     # 目地（奥へ下がった暗い線）
            else:
                l = 6 + tone
                if x == 2:
                    l = 8                                           # 光を受ける左のふち
                elif above_j:
                    l += 1                                          # 板石の上のふち（光の側）
                elif below_j:
                    l -= 2                                          # 板石の下のふち（影の側）
                if x == 11:
                    l -= 1
                r = rnd(x, y, variant, 9)
                if r > 0.86:
                    l -= 1                                          # 石のざらつき・小さな欠け
                elif r < 0.07:
                    l += 1
                c = S[max(0, min(9, l))]
                if not j and rnd(x, y, variant, 4) > 0.975 and x > 3:
                    c = RAMPS["moss"][2]                            # 石のすきまに少しのこけ
            out[y, x] = c
        for x in (12, 13):                                          # 影になる右の側面（石の段が見える）
            if j or (x == 13 and (y + variant) % 4 == 1):
                c = "#24201c"
            else:
                c = S[3 if x == 12 else 2] if rnd(x, y, variant, 7) > 0.2 else S[2 if x == 12 else 1]
            out[y, x] = c
        out[y, 14] = "#10201860"                                    # 地面へ落ちる影（うすく透ける）
        out[y, 15] = "#10201830" if rnd(y, variant, 11) > 0.3 else ""
        out[y, 1] = "#24201ca0"                                     # 左のりんかく（半分透ける）
    return out


def post():
    m = Model()
    m.add(rbox((0, 0.7, -3), (6.6, 0.7, 6.6), 0.3), "stone")             # 土台の段
    for k, (y0, y1) in enumerate(((1.4, 5.2), (5.2, 9.0), (9.0, 12.8), (12.8, 16.6), (16.6, 20.4))):
        off = 0.25 if k % 2 else 0.0
        m.add(rbox((off * 0.3, (y0 + y1) / 2, -3), (5.6 + off * 0.3, (y1 - y0) / 2 - 0.2, 5.6), 0.5), "stone")
    m.add(box((0, 11, -3), (5.3, 9.6, 5.3)), "mortar")
    m.add(rbox((0, 21.3, -3), (6.6, 0.9, 6.6), 0.4), "cap")              # 笠石
    m.add(rbox((0, 22.6, -3), (5.6, 0.5, 5.6), 0.3), "cap")
    m.add(torus_y((0, 15.0, 2.9), 0.0001, 0.0001), "gold")               # （場所あわせ）
    m.add(lambda p: np.maximum(np.abs(np.sqrt(p[..., 0] ** 2 + (p[..., 1] - 15.0) ** 2) - 2.0) - 0.55, np.abs(p[..., 2] - 2.75) - 0.35), "gold")   # 灯りの環
    return render(m, 16, 28, 8, 27, RAMPS, shade_fn=shade, colour_fn=colour, outline="#24201c", ground_contact=True)


if __name__ == "__main__":
    for name, img in (("townwall-h", wall_h(0)), ("townwall-h2", wall_h(1)), ("townwall-v", wall_v(0)), ("townwall-v2", wall_v(1)), ("townwall-post", post())):
        print(name, save(img, os.path.join(R20, name + ".txt"), os.path.join(R20, "pal-" + name + ".json")))
