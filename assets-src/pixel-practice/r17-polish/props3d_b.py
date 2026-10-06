"""町の飾り（建物・人物いがい）6つを、立体の模型から描きなおす（2026-10-06、人間の指示
「町にあるオブジェクト。建物、キャラ以外、もっと作りにこだわって立体感大事に。ドットを細かく。光加減も大事に。」）。
道具は sdf3d.py、色の段・こまかな模様の作り方は props3d.py と同じ。光は左上前から、ほかの形が落とす影・すみの暗さつき。
すべて一から自作（ほかの作品の絵はまねていない）。

  stall        市場の屋台: 木の台（たての板・上の天板）、かごに入った果物と野菜（りんご・みかん・キャベツ・レモン・なす）、
               4本の柱に、赤と白の縞の布の日よけ（前のふちは波の形のたれ）
  cart         手押しの荷車: 板をはった荷台と囲い、スポークのある木の車輪（鉄の輪）、左へのびる2本の取っ手と足、
               麻袋3つと木箱1つ
  noticeboard  掲示板: 2本の柱、木の枠の板、小さな切妻屋根、ピンでとめた紙（生成り色に、こまかな字の行）
  brazier      かがり火台: 3本足の鉄の火皿（ふちの輪・足をつなぐ輪）、赤くおこった炭、炎（日の光ではなく、炎そのものの色）と火の粉
  shrine       道ばたの石の祠: 2段の石の台、小さな石の堂（切妻屋根）、正面のくぼみに小さな灯り、
               屋根の三角の面に金の「三つの環（いちばん小さな環が欠けている）」のしるし。こけ
  grave-cross  墓石（ファイル名はそのまま）: 上の丸い、古びた石の墓じるし。正面に彫った環、かけた角、こけ、足もとの草
               （十字の形はやめた。じっさいの宗教のしるしは使わない）
書き出し: r20-props/<名前>.txt と pal-<名前>.json（前の平らな絵を上書き。大きさはもとの絵に近いまま）。
使い方: python3 props3d_b.py [名前 ...]（名前を書かなければ6つ全部）。"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sdf3d import (Model, box, rbox, cyl_y, cyl_x, cone_y, sphere, ellipsoid, capsule, torus_y, gable_x, diff, inter, render, save)
from props3d import RAMPS, hn, vnoise, common_shade

R20 = os.path.join(HERE, "..", "r20-props")


# ---------------------------------------------------------------- この絵のために足した形
def cyl_z(cx, cy, r, z0, z1):
    """前うしろ（z）へのびる円柱（車輪のじく・まるい板など）。"""
    def f(p):
        d_r = np.sqrt((p[..., 0] - cx) ** 2 + (p[..., 1] - cy) ** 2) - r
        d_z = np.maximum(z0 - p[..., 2], p[..., 2] - z1)
        return np.minimum(np.maximum(d_r, d_z), 0) + np.sqrt(np.maximum(d_r, 0) ** 2 + np.maximum(d_z, 0) ** 2)
    return f


def torus_z(c, R, r):
    """こちらを向いた輪（車輪の鉄の輪・彫った環・しるしの環）。"""
    c = np.array(c, float)

    def f(p):
        q = p - c
        a = np.sqrt(q[..., 0] ** 2 + q[..., 1] ** 2) - R
        return np.sqrt(a ** 2 + q[..., 2] ** 2) - r
    return f


def gable_z(x0, x1, z0, z1, y_eave, y_ridge):
    """前うしろ（z）へのびる切妻屋根（三角の面がこちらを向く）。"""
    cx = (x0 + x1) / 2; hw = (x1 - x0) / 2; hgt = y_ridge - y_eave; n = math.hypot(hgt, hw)

    def f(p):
        x = np.abs(p[..., 0] - cx); y = p[..., 1] - y_eave
        d = np.maximum((x * hgt + y * hw - hw * hgt) / n, -y)
        return np.maximum(d, np.maximum(z0 - p[..., 2], p[..., 2] - z1))
    return f


def slope_slab(x0, x1, zf, yf, zb, yb, t):
    """前のふち（zf, yf）から、うしろのふち（zb, yb）へ傾いた、うすい板（日よけの布）。"""
    s = (yb - yf) / (zb - zf); k = math.sqrt(1 + s * s)

    def f(p):
        yp = yf + (p[..., 2] - zf) * s
        d = np.abs(p[..., 1] - yp) / k - t
        d = np.maximum(d, np.maximum(x0 - p[..., 0], p[..., 0] - x1))
        return np.maximum(d, np.maximum(zb - p[..., 2], p[..., 2] - zf))
    return f


def soften_outline(img, keys, colour):
    """光る物（炎・灯り）のまわりの黒いりんかくを、あたたかい暗い色にかえる（光がにじんで見えるように）。"""
    H, W = img.shape
    out = img.copy()
    for y in range(H):
        for x in range(W):
            if img[y, x] != OUT:
                continue
            for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if 0 <= x + a < W and 0 <= y + b < H and img[y + b, x + a] in keys:
                    out[y, x] = colour
                    break
    return out


OUT = "#1e1a18"


def snap(lum, n):
    """平らな面の明るさを、色の段のまんなかにそろえる（市松のまぜが出ないので、板や石の面がすっきり見える）。"""
    v = np.clip(lum, 0, 0.999) * (n - 1)
    return (round(v) + 0.0) / (n - 1)
VIEW = np.array([1.0, 0.45, 1.0]) / np.linalg.norm([1.0, 0.45, 1.0])     # 見ている向き（形から目のほうへ）

WOOD2 = ["#22140a", "#36200f", "#4e2e16", "#683e1e", "#845228", "#a06834", "#ba8046", "#d29a5e"]   # 明るめの木（扉の色とはちがう段）
PRODUCE = {
    "apple": ["#3c0c10", "#6a1418", "#9a2020", "#c83a30", "#e8644c", "#f8a088"],
    "orange": ["#5a2a06", "#8e4a0c", "#c87014", "#ec9426", "#fab850", "#ffd88c"],
    "cabbage": ["#1a3010", "#2a4a18", "#3e6a22", "#5a8c30", "#7cae46", "#a8d070"],
    "lemon": ["#5a4a08", "#8c760e", "#c4a818", "#e6cc30", "#f6e46a", "#fff6b0"],
    "plum": ["#1e0e2c", "#341a48", "#4e2a6a", "#6c3e8e", "#9060b0", "#b48ed0"],
    "basket": ["#2e1e0c", "#4a3214", "#6a4c20", "#8c6a30", "#ae8a46", "#ccaa64", "#e2c888"],
    "cloth_r": ["#3a0e12", "#5e161a", "#8a2222", "#b2322c", "#d24a3a", "#ea6c52", "#f89474"],
    "cloth_w": ["#5a5248", "#7e766a", "#a49a8a", "#c6bca8", "#e0d8c4", "#f2ecdc", "#fdfaf0"],
    "skirt": ["#0e1e2e", "#16304a", "#204466", "#2c5a84", "#3e74a2", "#5890be"],
}


# ===================================================================== 屋台
def stall():
    m = Model()
    X = 12.5; ZB, ZF = -7.0, 0.0; HT = 9.0
    m.add(box((0, HT / 2 - 0.3, (ZB + ZF) / 2), (X, HT / 2 - 0.3, (ZF - ZB) / 2)), "plank")         # 台の箱
    m.add(box((0, HT, (ZB + ZF) / 2), (X + 0.6, 0.45, (ZF - ZB) / 2 + 0.6)), "top")                # 天板（少しはみ出す）
    m.add(box((0, 0.35, (ZB + ZF) / 2), (X + 0.3, 0.35, (ZF - ZB) / 2 + 0.3)), "post")             # 下の横木
    # 前の布（台の前にさげた青い布。上のふちは波）
    m.add(box((0, 7.4, ZF + 0.25), (X - 0.5, 1.3, 0.22)), "skirt")
    for i in range(-4, 5):
        m.add(ellipsoid((i * 2.8, 6.1, ZF + 0.25), (1.45, 0.9, 0.22)), "skirt")
    # 柱（4本）
    YF, YB = 25.0, 29.0
    for px, pz, top in ((-X - 0.2, ZF + 0.6, YF), (X + 0.2, ZF + 0.6, YF), (-X - 0.2, ZB, YB - 0.8), (X + 0.2, ZB, YB - 0.8)):
        m.add(box((px, top / 2, pz), (0.55, top / 2, 0.55)), "post")
    # 日よけ（縞の布、前へ下がる）と、前のふちのたれ（波の形）
    AX = 14.2; AZF, AZB = 2.2, -8.0
    m.add(slope_slab(-AX, AX, AZF, YF + 0.6, AZB, YB + 1.6, 0.35), "cloth")
    m.add(box((0, YF + 0.1, AZF), (AX, 0.9, 0.3)), "cloth")
    for i in range(-4, 5):
        m.add(ellipsoid((i * 3.15, YF - 0.9, AZF), (1.55, 1.25, 0.3)), "cloth")
    # 品物: 左のかご（りんご）、まんなかの木箱（キャベツ）、右のかご（みかん）、うしろの段（レモン・なす）
    def basket(cx, cz, r, h):
        m.add(diff(cone_y(cx, cz, r - 0.4, r, HT + 0.4, HT + 0.4 + h), cyl_y(cx, cz, r - 0.55, HT + 1.0, HT + 3 + h)), "basket")
        m.add(torus_y((cx, HT + 0.4 + h, cz), r - 0.05, 0.32), "basket")
    basket(-8.3, -1.8, 3.4, 1.6)
    for k, (ox, oz, oy) in enumerate(((-1.4, 0.7, 0), (0.3, 1.1, 0), (1.5, -0.1, 0), (-0.6, -1.0, 0), (1.0, -1.3, 0), (-0.4, 0.0, 1.05), (0.9, 0.3, 0.9))):
        m.add(sphere((-8.3 + ox * 1.2, HT + 2.6 + oy * 1.3, -1.8 + oz * 1.2), 1.3), "apple")
    basket(8.0, -1.8, 3.4, 1.6)
    for k, (ox, oz, oy) in enumerate(((-1.3, 0.8, 0), (0.4, 1.1, 0), (1.5, -0.2, 0), (-0.8, -1.0, 0), (1.0, -1.3, 0), (-0.2, 0.1, 1.0), (1.0, 0.4, 0.9))):
        m.add(sphere((8.0 + ox * 1.2, HT + 2.6 + oy * 1.3, -1.8 + oz * 1.2), 1.3), "orange")
    m.add(box((0, HT + 1.4, -1.6), (3.2, 1.0, 2.2)), "crate")                                        # まんなかの木箱
    for ox, oz in ((-1.6, -0.6), (1.5, -0.4), (0.0, 0.8), (-0.3, -2.4), (1.8, -2.6)):
        m.add(sphere((ox, HT + 3.5, -1.6 + oz + 0.4), 1.6), "cabbage")
    m.add(box((0, HT + 1.6, -5.5), (X - 0.6, 1.2, 1.3)), "plank")                                    # うしろの段
    for i, ox in enumerate(np.arange(-10.5, 11, 1.9)):
        if -4.0 < ox < 4.0:
            m.add(ellipsoid((ox, HT + 3.9, -5.4 + (i % 2) * 0.4), (0.95, 0.75, 1.6)), "plum")
        else:
            m.add(ellipsoid((ox, HT + 3.8, -5.4 + (i % 2) * 0.4), (1.1, 0.95, 0.95)), "lemon")

    def shade(mm, p, n, lum, x, y):
        if mm == "cloth":
            mm = "cloth_r" if math.floor((p[0] + AX) / 3.15) % 2 == 0 else "cloth_w"
            if n[1] > 0.3:
                lum += 0.06                                                    # 日よけの上は日なた
        if mm == "plank" and abs(n[2]) > 0.5:
            if (p[0] / 2.5) % 1 < 0.14:
                lum -= 0.13                                                    # たての板のすき間
            lum += ((hn(math.floor(p[0] / 2.5)) % 5) - 2) * 0.025
        if mm == "plank" and abs(n[0]) > 0.5 and (p[2] / 2.4) % 1 < 0.15:
            lum -= 0.12
        if mm == "crate" and abs(n[1]) < 0.5 and (p[1] - HT) % 0.95 < 0.25:
            lum -= 0.12
        if mm == "basket" and abs(n[1]) < 0.7 and ((p[1] * 2.2 + math.atan2(p[2] + 1.8, p[0] - 8 * np.sign(p[0])) * 2) % 1.4) < 0.4:
            lum -= 0.1                                                         # かごの編み目
        if mm in ("top", "post", "crate"):
            if ((p[0] * 0.3 + p[1] * 2.1 + p[2] * 0.4) % 1.7) < 0.25:
                lum -= 0.05
        if mm in ("plank", "top", "post", "crate", "skirt", "cloth_r", "cloth_w"):
            lum = snap(lum, len(ramps[mm]))
        return lum, mm

    ramps = dict(RAMPS); ramps.update(PRODUCE)
    ramps.update(plank=WOOD2, top=WOOD2, post=RAMPS["wood"], crate=WOOD2)
    img = render(m, 48, 46, 24, 43, ramps, shade_fn=shade, shadow=(27.5, 43.7, 18.5, 2.4), outline=OUT)
    return img


# ===================================================================== 荷車
def cart():
    m = Model()
    BX0, BX1, BZ0, BZ1 = -11.5, 12.0, -7.4, -0.4
    BY = 10.0
    cz = (BZ0 + BZ1) / 2
    m.add(box(((BX0 + BX1) / 2, BY, cz), ((BX1 - BX0) / 2, 0.5, (BZ1 - BZ0) / 2)), "bed")             # 荷台の床
    m.add(box(((BX0 + BX1) / 2, BY + 1.8, BZ1 - 0.25), ((BX1 - BX0) / 2, 1.5, 0.3)), "side")          # 前の囲い
    m.add(box(((BX0 + BX1) / 2, BY + 1.8, BZ0 + 0.25), ((BX1 - BX0) / 2, 1.5, 0.3)), "side")          # うしろの囲い
    for ex in (BX0 + 0.3, BX1 - 0.3):
        m.add(box((ex, BY + 1.8, cz), (0.3, 1.5, (BZ1 - BZ0) / 2)), "side")                           # 左右の囲い
    for sx in (BX0 + 0.3, -1.0, BX1 - 0.3):
        m.add(box((sx, BY + 1.9, BZ1 + 0.05), (0.45, 1.8, 0.3)), "iron")                               # 囲いの金具
    m.add(box(((BX0 + BX1) / 2, BY - 1.0, cz), ((BX1 - BX0) / 2 - 0.6, 0.6, (BZ1 - BZ0) / 2 - 1.0)), "frame")   # 下の枠
    # 車輪（前とうしろ）、じく
    WX, WR = 3.5, 6.4
    m.add(cyl_z(WX, WR, 0.55, BZ0 - 1.2, BZ1 + 1.2), "iron")
    for wz in (BZ1 + 0.75, BZ0 - 0.75):
        m.add(torus_z((WX, WR, wz), WR - 0.7, 0.75), "wheel")
        m.add(torus_z((WX, WR, wz), WR - 0.05, 0.35), "iron")                                          # 鉄の輪
        m.add(cyl_z(WX, WR, 1.2, wz - 0.6, wz + 0.6), "wood")                                           # こしき
        m.add(cyl_z(WX, WR, 0.55, wz + 0.3, wz + 0.8), "iron")
        for k in range(6):
            a = k * math.pi / 3 + 0.3
            m.add(capsule((WX + math.cos(a) * 1.0, WR + math.sin(a) * 1.0, wz), (WX + math.cos(a) * (WR - 1.0), WR + math.sin(a) * (WR - 1.0), wz), 0.45), "wheel")
    # 取っ手（左へ）と、ささえの足
    for hz in (BZ1 - 0.9, BZ0 + 0.9):
        m.add(capsule((BX0 + 1.0, BY - 0.6, hz), (-21.5, BY - 3.4, hz), 0.55), "frame")
    m.add(capsule((-21.1, BY - 3.3, BZ1 - 0.9), (-21.1, BY - 3.3, BZ0 + 0.9), 0.48), "frame")          # 握りの横棒
    m.add(capsule((-9.0, BY - 1.2, BZ1 - 0.9), (-9.6, 0.4, BZ1 - 0.9), 0.5), "frame")                  # 足
    m.add(capsule((-9.0, BY - 1.2, BZ0 + 0.9), (-9.6, 0.4, BZ0 + 0.9), 0.5), "frame")
    # 荷: 麻袋3つ（口をしばる）と木箱
    for (sx, sy, sz, rx, ry, rz) in ((-6.6, BY + 3.3, cz + 0.3, 3.6, 3.0, 2.9), (-0.8, BY + 3.3, cz - 0.3, 3.3, 3.1, 2.8), (-3.9, BY + 7.6, cz - 0.4, 3.2, 2.7, 2.6)):
        m.add(ellipsoid((sx, sy, sz), (rx, ry, rz)), "sack")
        m.add(cone_y(sx + 0.3, sz, 1.0, 0.5, sy + ry - 0.5, sy + ry + 1.0), "sack")
        m.add(torus_y((sx + 0.3, sy + ry + 0.2, sz), 0.75, 0.3), "rope")
        m.add(ellipsoid((sx + 0.3, sy + ry + 1.4, sz), (0.9, 0.5, 0.8)), "sack")
    m.add(box((7.4, BY + 3.2, cz - 0.1), (3.2, 2.7, 2.7)), "crate")
    m.add(box((7.4, BY + 5.9, cz - 0.1), (3.4, 0.32, 2.9)), "crate")
    for ox in (-2.6, 2.6):
        m.add(box((7.4 + ox, BY + 3.2, cz + 2.75), (0.45, 2.7, 0.15)), "iron")                         # 木箱のかどの金具

    def shade(mm, p, n, lum, x, y):
        if mm in ("side", "crate", "bed") and abs(n[1]) < 0.5:
            if ((p[1] - BY + 0.5) / 1.7) % 1 < 0.22:
                lum -= 0.12                                                    # 板のすき間
        if mm == "bed" and n[1] > 0.5 and (p[0] / 1.6) % 1 < 0.18:
            lum -= 0.1
        if mm == "crate" and n[1] > 0.5 and (p[2] / 1.6) % 1 < 0.2:
            lum -= 0.1
        if mm == "sack":
            lum += ((hn(int(p[0] * 2.5), int(p[1] * 2.5)) % 3) - 1) * 0.03    # 麻の目
            if abs(((p[0] - p[1] * 0.4) * 0.8) % 2.4 - 1.2) < 0.12:
                lum -= 0.08                                                    # しわ
        if mm in ("frame", "wood", "wheel", "side", "crate"):
            if ((p[0] * 0.25 + p[1] * 2.0 + p[2] * 0.35) % 1.7) < 0.25:
                lum -= 0.05
        if mm in ("frame", "wood", "wheel", "side", "crate", "bed"):
            lum = snap(lum, len(ramps[mm]))
        return lum, mm

    ramps = dict(RAMPS)
    ramps.update(bed=WOOD2, side=WOOD2, frame=RAMPS["wood"], wheel=WOOD2, crate=["#2c1c0c", "#46301a", "#644626", "#846034", "#a47c46", "#c09a5e", "#d8b67c"],
                 sack=["#3a2e1c", "#56462c", "#74623e", "#948052", "#b29e6a", "#cab886", "#e0d2a4"])
    return render(m, 48, 34, 24, 31.6, ramps, shade_fn=shade, shadow=(25.5, 32.3, 21.5, 2.1), outline=OUT)


# ===================================================================== 掲示板
PAPERS = [  # (まんなかx, まんなかy, 半分の幅, 半分の高さ, 字の行があるか, ピンの色)
    (-6.2, 19.5, 3.0, 3.4, True, "apple"),
    (0.2, 20.6, 2.4, 2.3, True, "plum"),
    (5.9, 18.4, 3.1, 4.0, True, "apple"),
    (-5.0, 12.8, 3.6, 2.4, True, "lemon"),
    (1.2, 13.6, 2.2, 3.4, True, "plum"),
]


def noticeboard():
    m = Model()
    BW = 10.5; Y0, Y1 = 8.5, 25.0
    for sx in (-BW + 0.6, BW - 0.6):
        m.add(box((sx, 13.5, -0.4), (0.75, 13.5, 0.75)), "post")                                       # 柱
        m.add(box((sx, 0.5, -0.4), (1.1, 0.5, 1.1)), "stone")                                           # 柱の根石
    m.add(box((0, (Y0 + Y1) / 2, -0.6), (BW, (Y1 - Y0) / 2, 0.45)), "board")                         # 板
    for (c, h) in (((0, Y1 - 0.4, -0.2), (BW + 0.4, 0.55, 0.65)), ((0, Y0 + 0.4, -0.2), (BW + 0.4, 0.55, 0.65)),
                   ((-BW, (Y0 + Y1) / 2, -0.2), (0.55, (Y1 - Y0) / 2, 0.65)), ((BW, (Y0 + Y1) / 2, -0.2), (0.55, (Y1 - Y0) / 2, 0.65))):
        m.add(box(c, h), "frame")                                                                         # 枠
    m.add(box((0, Y0 - 0.2, 0.25), (BW - 0.6, 0.25, 0.5)), "frame")                                     # 下の小さな棚
    # 屋根（前後に流れる切妻）
    m.add(gable_x(-BW - 2.4, BW + 2.4, -3.6, 2.8, Y1 + 1.0, Y1 + 6.4), "roof")
    m.add(box((0, Y1 + 6.3, -0.4), (BW + 2.5, 0.45, 0.55)), "ridge")
    m.add(box((0, Y1 + 0.7, -0.4), (BW + 0.5, 0.55, 0.7)), "frame")                                    # 屋根の下の横木
    for (px, py, hw, hh, txt, pin) in PAPERS:
        m.add(box((px, py, -0.05), (hw, hh, 0.12)), "paper")
        m.add(sphere((px, py + hh - 0.7, 0.3), 0.55), pin)

    def shade(mm, p, n, lum, x, y):
        if mm == "board" and (p[0] / 2.2) % 1 < 0.12:
            lum -= 0.1                                                         # 板のたてのすき間
        if mm in ("post", "frame", "board") and ((p[0] * 0.3 + p[1] * 2.1 + p[2] * 0.3) % 1.7) < 0.25:
            lum -= 0.05
        if mm == "roof":
            if (p[1] / 1.2) % 1 < 0.3:
                lum -= 0.12                                                    # 板ぶきの段
            elif ((p[0] + (math.floor(p[1] / 1.2) % 2) * 1.3) / 2.6) % 1 < 0.16:
                lum -= 0.07
        if mm == "paper":
            lum = 0.62 + 0.3 * lum                                              # 紙は光をよく返す
        return lum, mm

    def colour(mm, p, n, lum, x, y, c):
        if mm == "paper" and n[2] > 0.5:
            for (px, py, hw, hh, txt, pin) in PAPERS:
                if abs(p[0] - px) <= hw + 0.05 and abs(p[1] - py) <= hh + 0.05:
                    lx, ly = p[0] - (px - hw), (py + hh) - p[1]
                    if ly > 1.3 and ly < 2 * hh - 0.6 and 0.9 < lx < 2 * hw - 0.7:
                        row = math.floor(ly - 1.3)
                        end = 2 * hw - 0.7 - (hn(px * 10, row) % 3) * 0.8
                        if row % 2 == 0 and lx < end:
                            return "#6a5e52" if (hn(x, y) % 4) else "#8a8074"      # こまかな字の行
                    if lx < 0.45 or ly < 0.4:
                        return "#fbf6e6"                                       # 紙のふちの光
            return c
        return c

    ramps = dict(RAMPS); ramps.update(PRODUCE)
    ramps.update(post=RAMPS["wood"], frame=WOOD2, board=["#2a1a0e", "#3e2816", "#563a20", "#6e4c2a", "#886036", "#a07444"],
                 roof=["#2a1610", "#422418", "#5e3622", "#7a4a2e", "#96603a", "#b07a4c", "#c8946a"], ridge=RAMPS["wood"],
                 paper=["#8a8270", "#a8a08a", "#c4bca4", "#d8d2bc", "#e8e2ce", "#f4efde"])
    return render(m, 32, 38, 16, 36.2, ramps, shade_fn=shade, colour_fn=colour, shadow=(17.5, 36.8, 12.5, 1.8), outline=OUT)


# ===================================================================== かがり火台
FLAME = ["#a8241a", "#d8481c", "#f07a22", "#ffae34", "#ffd860", "#fff4b8"]
COAL = ["#2c0e08", "#5a160c", "#9a2a10", "#d8521a", "#ff9a30", "#ffd870"]


def brazier():
    m = Model()
    BY = 13.5; BR = 5.4
    bowl = inter(diff(sphere((0, BY + 1.0, 0), BR), sphere((0, BY + 1.0, 0), BR - 0.7)), box((0, BY - 2.5, 0), (8, 3.5, 8)))
    m.add(bowl, "iron")
    m.add(torus_y((0, BY + 1.0, 0), BR - 0.1, 0.5), "rim")                                              # ふちの輪
    m.add(torus_y((0, BY - 1.6, 0), BR - 1.1, 0.32), "iron")                                             # 飾りの帯
    m.add(cyl_y(0, 0, 1.3, BY - 4.8, BY - 3.2), "iron")                                                  # 下のつぼみ
    for k in range(3):
        a = math.pi / 2 + k * 2 * math.pi / 3 + 0.35
        ca, sa = math.cos(a), math.sin(a)
        top = (ca * 2.8, BY - 2.6, sa * 2.8); knee = (ca * 3.9, 5.5, sa * 3.9); foot = (ca * 4.6, 0.6, sa * 4.6)
        m.add(capsule(top, knee, 0.55), "iron")
        m.add(capsule(knee, foot, 0.55, 0.45), "iron")
        m.add(sphere((ca * 5.0, 0.55, sa * 5.0), 0.7), "iron")                                          # 足の先
    m.add(torus_y((0, 5.5, 0), 3.85, 0.3), "iron")                                                      # 足をつなぐ輪
    # 炭（火皿の上にもりあがる）
    for i in range(14):
        a = i * 2.4; r = 0.6 + (i % 4) * 1.1
        m.add(sphere((math.cos(a) * r, BY + 0.9 + (0.5 if r < 1.5 else 0), math.sin(a) * r), 1.05), "coal")
    # 炎（まんなかの大きな舌と、まわりの小さな舌）、火の粉
    tongues = [((0.0, BY + 1.0, 0.3), (0.4, BY + 14.2, 0.2), 2.9),
               ((-2.1, BY + 1.2, 0.8), (-3.0, BY + 8.6, 0.6), 1.6),
               ((2.2, BY + 1.2, 0.4), (3.2, BY + 9.6, 0.0), 1.7),
               ((0.8, BY + 1.2, 2.2), (1.2, BY + 7.0, 2.6), 1.3),
               ((-1.0, BY + 1.0, -2.0), (-1.4, BY + 10.5, -2.2), 1.6)]
    for a, b, r in tongues:
        m.add(capsule(a, b, r, 0.12), "flame")
    m.add(capsule((0.4, BY + 9.0, 0.2), (-0.8, BY + 12.2, 0.3), 0.9, 0.1), "flame")
    for (sx, sy, sz) in ((-3.4, BY + 13.0, 0.5), (3.6, BY + 14.8, 0.0), (1.8, BY + 17.0, 0.4)):
        m.add(sphere((sx, sy, sz), 0.42), "spark")

    def shade(mm, p, n, lum, x, y):
        if mm in ("iron", "rim"):
            if mm == "rim" or (p[1] > BY - 1.0 and n[1] > -0.2):
                warm = max(0.0, 1 - math.hypot(p[0], p[2]) / 6.5) + (0.4 if mm == "rim" else 0)
                if warm > 0.25:
                    return lum * 0.7 + warm * 0.4, "hot"                       # 炎に照らされたふち
            if (p[1] % 1.3) < 0.12 and p[1] > BY - 4:
                lum -= 0.05
        return lum, mm

    def colour(mm, p, n, lum, x, y, c):
        if mm in ("flame", "spark"):
            face = max(0.0, float(n @ VIEW))
            t = np.clip((p[1] - BY) / 14.0, 0, 1)
            heat = 0.55 * face + 0.55 * (1 - t) - 0.05
            if mm == "spark":
                heat = 0.75
            v = heat * (len(FLAME) - 1) + (0.35 if (x + y) % 2 else -0.05)
            return FLAME[int(np.clip(v, 0, len(FLAME) - 1))]
        if mm == "coal":
            glow = 0.35 + 0.45 * max(0.0, n[1]) + ((hn(int(p[0] * 3), int(p[2] * 3)) % 5) - 2) * 0.12
            if math.hypot(p[0], p[2]) < 1.8:
                glow += 0.25                                                   # まんなかは熱い
            return COAL[int(np.clip(glow, 0, 0.999) * len(COAL))]
        return c

    ramps = dict(RAMPS)
    ramps.update(rim=RAMPS["iron"], hot=["#2a1410", "#4e2416", "#7a3a1c", "#a8562a", "#d47a3c", "#f2a258"],
                 iron=["#18181e", "#282a32", "#3a3e4a", "#525866", "#6e7684", "#9098a6", "#b2bac6"], flame=FLAME, coal=COAL, spark=FLAME)
    img = render(m, 26, 34, 13, 31.6, ramps, shade_fn=shade, colour_fn=colour, shadow=(14.5, 32.2, 8.5, 1.7), outline=OUT, ambient=0.2)
    return soften_outline(img, set(FLAME), "#5a1a10")


# ===================================================================== 石の祠
def shrine():
    m = Model()
    m.add(box((0, 0.8, -0.2), (7.6, 0.8, 3.9)), "stone")                                                  # 下の段
    m.add(box((0, 2.3, -0.3), (6.7, 0.75, 3.4)), "cap")                                                  # 上の段
    BW, BD, BH0, BH1 = 5.6, 2.8, 3.0, 21.5
    for sx in (-BW, BW):
        m.add(box((sx, (BH0 + BH1) / 2, BD - 0.2), (0.75, (BH1 - BH0) / 2, 0.55)), "cap")                 # 角の柱
    m.add(box((0, BH1 + 0.4, -0.4), (BW + 0.9, 0.5, BD + 0.8)), "cap")                                    # 屋根の下の帯
    # くぼみ（上がまるいアーチ）と、中の灯り
    NX, NY0, NY1 = 2.6, 4.4, 9.4
    niche = lambda p: np.maximum(np.minimum(np.maximum(np.abs(p[..., 0]) - NX, np.maximum(NY0 - p[..., 1], p[..., 1] - NY1)),
                                            np.sqrt(p[..., 0] ** 2 + (p[..., 1] - NY1) ** 2) - NX),
                                 np.maximum(p[..., 2] - 4.0, (BD - 0.4 - 2.2) - p[..., 2]))
    FZ = BD - 0.4                                                                                         # 堂の正面の z
    EY, EX = BH1 - 5.3, 0.5
    plaque = lambda p: np.maximum(np.sqrt((p[..., 0] - EX) ** 2 + (p[..., 1] - EY) ** 2) - 4.85, np.abs(p[..., 2] - FZ) - 0.4)
    m.add(diff(diff(box((0, (BH0 + BH1) / 2, -0.4), (BW, (BH1 - BH0) / 2, BD)), niche), plaque), "block")   # 堂のからだ（くぼみと、しるしの丸いくぼみをけずる）
    m.add(box((0, NY0 + 0.4, BD - 1.6), (1.4, 0.4, 0.9)), "cap")                                            # 灯りの台
    m.add(cyl_y(0, BD - 1.6, 0.75, NY0 + 0.8, NY0 + 2.0), "iron")                                         # 灯り皿
    m.add(capsule((0, NY0 + 2.4, BD - 1.6), (0, NY0 + 4.3, BD - 1.6), 0.85, 0.1), "flame")              # 小さな火
    # 屋根（三角がこちらを向く切妻）と棟
    m.add(gable_x(-BW - 1.7, BW + 1.7, -BD - 2.0, BD + 1.4, BH1 + 0.9, BH1 + 6.6), "roof")
    m.add(box((0, BH1 + 1.1, -0.3), (BW + 1.75, 0.35, BD + 1.75)), "roofedge")                          # 軒のあつみ
    m.add(box((0, BH1 + 6.6, -0.3), (BW + 2.0, 0.5, 0.55)), "cap")                                         # 棟
    for sx in (-BW - 2.0, BW + 2.0):
        m.add(sphere((sx, BH1 + 6.9, -0.3), 0.75), "cap")                                                  # 棟の両はしの丸い石
    m.add(sphere((0, BH1 + 7.4, -0.3), 0.65), "gold")                                                      # 棟のまんなかの玉                                                 # 棟の先の玉
    # 三つの環のしるし（いちばん小さな環は欠ける）。屋根の三角の面に、金で
    # 三つの環のしるし（いちばん小さな環は右上が欠ける）は、丸いくぼみの底に、1ドットずつ金で描く（下の colour）
    G, ZB = 33.4, FZ - 0.4
    EI = int(round(13 + EX - ZB - 0.5)); EJ = int(round(G - EY + 0.45 * ZB - 0.5))
    # 供えた花（左）と、足もとの小石
    m.add(ellipsoid((-5.6, 3.6, 2.2), (0.9, 0.8, 0.8)), "moss")

    def shade(mm, p, n, lum, x, y):
        if mm == "block" and abs(n[1]) < 0.6:
            course = math.floor((p[1] - BH0) / 2.5)
            along = p[0] if abs(n[2]) > 0.5 else p[2]
            if ((p[1] - BH0) / 2.5) % 1 < 0.17:
                lum -= 0.09
            elif ((along + (course % 2) * 2.0) / 4.0) % 1 < 0.12:
                lum -= 0.07
            lum += ((hn(course, math.floor((along + (course % 2) * 2.0) / 4.0)) % 5) - 2) * 0.02
            if vnoise(p[0] + 0.4, p[1], p[2], 1.4) > 0.86:
                lum -= 0.08                                                    # 古びたしみ
        if mm == "block" and abs(plaque(p[None])[0]) < 0.15 and p[2] < FZ - 0.05:
            return 0.18, "gable"                                               # しるしのくぼみの底（暗い）
        if mm == "block" and abs(niche(p[None])[0]) < 0.2 and p[2] < BD - 0.3 and abs(p[0]) < NX + 0.05 and p[1] > NY0 - 0.05:
            d = math.hypot(p[0], p[1] - (NY0 + 3.0))
            return 0.12 + max(0.0, 0.55 - d * 0.12), "glow"                     # 灯りにてらされたくぼみの奥
        if mm == "roof":
            if (p[1] / 1.25) % 1 < 0.28:
                lum -= 0.1                                                     # 石の屋根の段
            elif ((p[0] + (math.floor(p[1] / 1.25) % 2) * 1.4) / 2.8) % 1 < 0.14:
                lum -= 0.06
        if mm in ("stone", "cap") and n[1] > 0.5 and vnoise(p[0] + 0.7, p[1], p[2] + 0.2, 1.5) > 0.8:
            return lum + 0.05, "moss"
        if mm in ("stone", "block") and p[1] < 1.6:
            lum -= 0.05
        if mm in ("stone", "cap", "block", "roof", "moss"):
            lum = snap(lum, len(ramps[mm]))
        return lum, mm

    def colour(mm, p, n, lum, x, y, c):
        if mm == "gable" and n[2] > 0.7:
            dx, dy = x - EI, y - EJ
            d = math.hypot(dx, dy)
            ring = (0.9 <= d <= 1.5 and not (dx == 1 and dy == -1)) or (2.7 <= d <= 3.3) or (3.9 <= d <= 4.6)
            if ring:
                if dx + dy <= -4:
                    return "#fff0a8"                                      # 左上は光る
                return "#f0cc60" if dx + dy <= 2 else "#c8962c"           # 右下は少し暗い
            return "#1c1e24"                                              # くぼみの底
        if mm == "flame":
            face = max(0.0, float(n @ VIEW))
            v = (0.6 * face + 0.6 * (1 - np.clip((p[1] - NY0 - 2.4) / 2.0, 0, 1))) * (len(FLAME) - 1)
            return FLAME[int(np.clip(v, 1, len(FLAME) - 1))]
        return c

    ramps = dict(RAMPS)
    STONE_W = ["#2c2a2a", "#454240", "#5f5b56", "#7a756e", "#958f86", "#aea89e", "#c6c0b4", "#dcd6ca", "#eeeae0"]   # 少しあたたかい石
    ramps.update(stone=STONE_W, cap=STONE_W, block=STONE_W, roof=["#1c222e", "#28303e", "#364052", "#465268", "#58667e", "#6c7c94"], roofedge=["#14181e", "#20262e", "#2e3640", "#3e4854"],
                 gable=["#1c1e24", "#2a2c34", "#3a3e48", "#4e535e", "#646a76", "#7c828e"],
                 glow=["#1a100c", "#3a2214", "#6a3c1c", "#a2622a", "#d89440"], flame=FLAME)
    img = render(m, 26, 36, 13, 33.4, ramps, shade_fn=shade, colour_fn=colour, shadow=(15.0, 34.4, 10.5, 1.8), outline=OUT)
    return soften_outline(img, set(FLAME), "#4a2410")


# ===================================================================== 墓石（丸い頭の石と、彫った環）
def grave_cross():
    m = Model()
    m.add(box((0, 0.9, 0), (6.2, 0.9, 2.5)), "stone")                                                     # 台石
    SW, SD = 4.6, 1.25
    slab = lambda p: np.maximum(np.minimum(box((0, 7.0, -0.2), (SW, 6.0, SD))(p), cyl_z(0, 13.0, SW, -0.2 - SD, -0.2 + SD)(p)),
                                -p[..., 1] + 1.0)
    m.add(slab, "grave")
    m.add(box((0, 13.0, -0.2), (SW + 0.1, 0.25, SD + 0.1)), "grave")
    m.cut(box((0, 13.0, -0.2), (SW + 1, 0.2, SD + 1)))                                                    # 頭の下のきざみの線
    FZ = -0.2 + SD
    m.cut(lambda p: np.maximum(np.abs(np.sqrt(p[..., 0] ** 2 + (p[..., 1] - 9.2) ** 2) - 2.5) - 0.55, np.abs(p[..., 2] - FZ) - 0.45), "carve")   # 彫った環
    m.cut(sphere((SW + 0.4, 16.0, 0.9), 1.3))                                                             # かけた角
    m.cut(sphere((-SW - 0.2, 4.0, 1.2), 0.8))
    for i in range(4):                                                                                    # 足もとの草
        gx = -5.4 + i * 3.6 + (hn(i) % 3) * 0.3
        m.add(ellipsoid((gx, 0.9, 2.6 - (i % 2) * 0.6), (1.4, 1.0, 0.9)), "grass")

    def shade(mm, p, n, lum, x, y):
        if mm in ("grave", "stone", "carve"):
            lum += ((hn(int(p[0] * 1.6), int(p[1] * 1.6)) % 5) - 2) * 0.025   # ざらざらの石
            if vnoise(p[0] + 0.5, p[1], p[2], 1.3) > 0.88 and mm != "carve" and abs(p[1] - 9.2) > 3.4:
                lum -= 0.08                                                    # 古びたしみ（環のまわりはさける）
            if (n[1] > 0.45 or p[1] < 3.2) and vnoise(p[0] + 0.2, p[1] * 0.8, p[2], 1.2) > 0.5 and mm != "carve":
                return lum + 0.04, "moss"
            if mm == "carve":
                lum -= 0.12
        if mm == "grass":
            lum += ((hn(int(p[0] * 3), int(p[1] * 3)) % 3) - 1) * 0.06
        return lum, mm

    ramps = dict(RAMPS)
    GS = ["#26282a", "#3c3f42", "#55585a", "#6e7172", "#888a8a", "#a2a3a1", "#bbbbb7", "#d2d1cb"]
    ramps.update(grave=GS, stone=GS, carve=GS, grass=["#14280e", "#1e3c16", "#2c5620", "#3c722a", "#509036", "#6aae46"])
    return render(m, 18, 24, 9, 21.6, ramps, shade_fn=shade, shadow=(10.5, 22.2, 7.5, 1.4), outline=OUT)


if __name__ == "__main__":
    todo = sys.argv[1:] or ["stall", "cart", "noticeboard", "brazier", "shrine", "grave-cross"]
    for name in todo:
        img = globals()[name.replace("-", "_")]()
        print(name, img.shape[1], "x", img.shape[0], "色", save(img, os.path.join(R20, name + ".txt"), os.path.join(R20, "pal-" + name + ".json")))
