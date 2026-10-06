"""町の小物6つを、立体の模型から描きなおす（2026-10-06、人間の指示
「町にあるオブジェクト。建物、キャラ以外、もっと作りにこだわって立体感大事に。ドットを細かく。光加減も大事に。」）。
道具は sdf3d.py（props3d.py と同じ作り方）。光は左上前から。形どうしが落とす影・すみの暗さ・地面のうすい影つき。すべて一から自作。

  barrel    樽: ふくらんだ板（板と板のすき間）、鉄のたが4本と鋲、ふちの立ったまるいふた（板の合わせ目）、横の栓
  crates    木箱3つの山: 枠のある箱（たすきの筋かい・角の釘）を2つならべ、上に1つ。わきに麻の袋（口をしばったもの）
  rock2     岩: 面のかどが立った大きな岩、ひび、上のこけ、足もとの小石
  lamp      街灯: 石の台、みぞのある鉄の柱、ガラスの灯り箱（中の灯りは光の向きに関係なく、あたたかい色）、かさ、てっぺんの飾り
  signpost  道しるべ: 木の柱（木目）、ちがう向きをさす矢の板2まい（釘どめ）
  bench     ベンチ: 木の板を並べた座面と背もたれ、鉄の脚と石の足
書き出し: bench は r20-props/bench.txt、ほかは r17-polish/<名前>.txt（前の絵を上書き。どれも 48×48 の枠で、足もとはまんなか下）。
使い方: python3 props3d_a.py [名前 ...]（名前を書かなければ6つとも作る）。"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sdf3d import (Model, box, rbox, cyl_y, cone_y, sphere, ellipsoid, capsule, torus_y, inter, render, save)
from props3d import RAMPS, hn, vnoise

HERE = os.path.dirname(os.path.abspath(__file__))
R20 = os.path.join(HERE, "..", "r20-props")

MY = {
    # 樽・木箱・道しるべ・ベンチの木（扉の色とは別の色にしてある）
    "stave": ["#24140a", "#3a2210", "#553216", "#70441e", "#8c5828", "#a86e34", "#c28644", "#d8a05c", "#ecc080"],
    "lidtop": ["#3a2614", "#563a1e", "#74502a", "#906838", "#aa8048", "#c09a60", "#d4b47c", "#e6cc98"],
    "lid": ["#2a180c", "#432812", "#5e3a1a", "#7a4e24", "#966430", "#b07c40", "#c89656", "#dcb070"],
    "crate": ["#2c1e10", "#463018", "#624422", "#7e5a2e", "#9a723c", "#b48c4e", "#cca464", "#e0bc7e", "#f0d49c"],
    "frame": ["#1c120a", "#2e1e10", "#442c16", "#5a3a1e", "#724c26", "#8a5e30", "#a2723c", "#b8884e"],
    "post": ["#1e140c", "#322214", "#48321c", "#5e4426", "#765832", "#8e6e40", "#a68652", "#bc9e68"],
    "board": ["#2a1a0e", "#422a16", "#5c3c1e", "#764e28", "#926434", "#ac7c44", "#c49458", "#d8ac72", "#eac690"],
    "slat": ["#2a1a0e", "#42291a", "#5c3a20", "#774e2a", "#926436", "#ac7c46", "#c4945a", "#d8ac74"],
    "iron": ["#14161c", "#22252e", "#323642", "#464b5a", "#5e6474", "#7a8292", "#9aa2b2", "#c0c8d4"],
    "rivet": ["#1a1c22", "#3a3e4a", "#6a7080", "#a8b0bc", "#e0e6ec"],
    "sack": ["#2e2618", "#463c26", "#605434", "#7c6e46", "#988a5a", "#b2a470", "#c8bc88", "#ddd2a4"],
    "rope": ["#2e2414", "#4a3c22", "#6a5834", "#8c7a4c", "#ac9a66", "#c8b886"],
    "rock": ["#24242a", "#34343c", "#46464e", "#5a5a62", "#706f76", "#87868c", "#9e9ca0", "#b6b4b6", "#cecbcb", "#e4e2df"],
    "pebble": ["#2c2a2c", "#45424a", "#5f5c62", "#7c787c", "#9a9698", "#b6b2b2", "#d0ccca"],
    "moss": ["#1a2c14", "#24401a", "#305620", "#3e6c28", "#4e8232", "#62983c", "#7cb04a", "#9cc860"],
    "lampstone": ["#26262c", "#38383f", "#4c4c54", "#62626a", "#7a7a82", "#93929a", "#acabb0", "#c6c4c6"],
    "lamp": ["#121218", "#1c1c26", "#282a36", "#363a48", "#484e5e", "#5e6678", "#7a8496", "#a0aab8"],
    "glass": ["#ffd468"],
    "stone": ["#2a2a30", "#3e3e46", "#55545c", "#6d6c73", "#86848a", "#9f9da1", "#b8b6b8", "#d0cecd"],
}
ramps_all = dict(RAMPS)
ramps_all.update(MY)


def rot_y(f, ang, c=(0, 0, 0)):
    """形 f を、点 c を中心に y の軸のまわりへ ang（ラジアン）まわす。"""
    c = np.array(c, float); ca, sa = math.cos(ang), math.sin(ang)

    def g(p):
        q = p - c
        x = q[..., 0] * ca + q[..., 2] * sa
        z = -q[..., 0] * sa + q[..., 2] * ca
        return f(np.stack([x, q[..., 1], z], -1) + c)
    return g


# ===================================================================== 樽
def barrel():
    """2026-10-06 作りなおし（人間の指示「樽戻しちゃダメ、リアル感は追及して。変に立体感がありすぎただけだから」）:
    ななめの見え方だと、丸い樽が横に引きのばされてかたむいて見えたので、正面の少し上（25度）から見下ろす見え方で描く。
    ふくらみはひかえめに、まっすぐ立つ。板（16まい）ごとの色・すき間・木目、鉄のたが4本と鋲、ふたの板と、ふちの木口、横の栓。"""
    m = Model()
    H, R0, R1 = 27.0, 10.0, 11.2             # 高さ、上下のはしの半径、まんなかのふくらみ（ひかえめ）。前の樽と同じくらいの大きさ

    def rad(y):
        return R0 + (R1 - R0) * np.sin(np.pi * np.clip(y / H, 0, 1))

    def body(p):
        y = p[..., 1]
        dr = (np.sqrt(p[..., 0] ** 2 + p[..., 2] ** 2) - rad(y)) * 0.95
        return np.maximum(dr, np.maximum(-y, y - H))
    m.add(body, "stave")
    m.cut(cyl_y(0, 0, R0 - 0.9, H - 0.9, H + 2), "lid")              # ふたは、ふちより少し下
    for yh in (2.2, 7.0, 20.0, 24.8):                                  # 鉄のたが4本（細め）
        r = float(rad(yh)) + 0.25
        m.add(lambda p, yh=yh, r=r: np.maximum(np.abs(np.sqrt(p[..., 0] ** 2 + p[..., 2] ** 2) - r + 0.2) - 0.35,
                                               np.abs(p[..., 1] - yh) - 0.6), "iron")
        for a in (1.05, 1.57, 2.1):                                     # 鋲（こちらを向いた側だけ）
            m.add(sphere((math.cos(a) * (r + 0.05), yh, math.sin(a) * (r + 0.05)), 0.32), "rivet")
    m.add(capsule((math.cos(1.25) * R1 * 0.92, 13.5, math.sin(1.25) * R1 * 0.92), (math.cos(1.25) * R1 * 1.07, 13.5, math.sin(1.25) * R1 * 1.07), 0.9), "lid")   # 栓

    # 光の実物感（2026-10-06「少し光の感じ、実物感を出そうか」）: 見る向き（正面の少し上）と光の向きのあいだの向きで、
    # つや（鏡のような照り返し）を出す。木はやわらかいつやの帯、鉄のたがは、するどい光の点。ふちは少し暗く（丸みが出る）
    V = np.array([0.0, math.sin(math.radians(25)), math.cos(math.radians(25))])
    Lg = np.array([-0.55, 0.62, 0.56]); Lg /= np.linalg.norm(Lg)
    Hh = (V + Lg) / np.linalg.norm(V + Lg)

    def gloss(n, power):
        return max(0.0, float(np.dot(n, Hh))) ** power

    def shade(mm, p, n, lum, x, y):
        rim = (1 - max(0.0, float(np.dot(n, V)))) ** 2
        if mm == "iron" or mm == "rivet":
            lum += 0.7 * gloss(n, 24) - 0.15 * rim
            return lum, mm
        if mm == "stave":
            lum += 0.3 * gloss(n, 8) - 0.14 * rim
            if n[1] > 0.7:
                return lum + 0.08, "stave"                            # ふちの木口
            if p[1] > H - 1.2 and math.hypot(p[0], p[2]) < R0 - 0.6:
                return min(lum, 0.32) - 0.1, "stave"                  # ふちの内がわは、かげ
            ang = math.atan2(p[2], p[0])
            s = (ang / (2 * math.pi)) * 16 + 0.3
            if s % 1 < 0.13:
                lum -= 0.14                                           # 板と板のすき間（細く）
            lum += ((hn(math.floor(s)) % 5) - 2) * 0.018                # 板ごとの色のちがい
            if (p[1] * 1.7 + math.floor(s) * 0.37) % 2.3 < 0.18:
                lum -= 0.04                                           # 木目
        if mm == "lid" and n[1] > 0.6:
            mm = "lidtop"
            if ((p[2] + 20) / 2.4) % 1 < 0.2:
                lum -= 0.14                                           # ふたの板の合わせ目
        return lum, mm
    def colour(mm, p, n, lum, x, y, c):
        if mm in ("iron", "rivet") and gloss(n, 24) > 0.55:
            return "#eef2f6"                                          # 鉄のするどい光
        if mm == "stave" and gloss(n, 8) > 0.82 and (x + y) % 2 == 0:
            return "#e8b47a"                                          # 木のつやの、いちばん明るい所
        return c
    return render(m, 48, 48, 24, 44, ramps_all, shade_fn=shade, colour_fn=colour, shadow=(26, 45.4, 15, 2.5), front_tilt=25)


# ===================================================================== 木箱
FRAMES = []                                                              # 枠と筋かいの形（枠のきわに、かげの線を入れるため）


def crate_box(m, c, h):
    """枠のある木箱1つ（正面・右・上の面に枠、正面と右にたすきの筋かい、角に釘）。c はまんなか、h は半分の大きさ。
    板の箱を少し小さく作り、枠と筋かいを、その面より少し外へ出して重ねる（浮き出た枠になる）。"""
    cx, cy, cz = c; hx, hy, hz = h
    e = 0.45                                                             # 枠が面から出る分
    m.add(box(c, (hx - e, hy - e, hz - e)), "crate")
    t = 0.95                                                             # 枠のはば
    for sx in (-1, 1):                                                   # たての角の枠
        for sz in (-1, 1):
            FRAMES.append(box((cx + sx * (hx - t / 2), cy, cz + sz * (hz - t / 2)), (t / 2, hy, t / 2)))
            m.add(FRAMES[-1], "frame")
    for sy in (-1, 1):                                                   # 上下の横の枠（四方）
        yy = cy + sy * (hy - t / 2)
        for f in (box((cx, yy, cz + hz - t / 2), (hx, t / 2, t / 2)), box((cx, yy, cz - hz + t / 2), (hx, t / 2, t / 2)),
                  box((cx + hx - t / 2, yy, cz), (t / 2, t / 2, hz)), box((cx - hx + t / 2, yy, cz), (t / 2, t / 2, hz))):
            FRAMES.append(f)
            m.add(f, "frame")
    # たすきの筋かい（正面: 左下→右上。右の面: 手前下→奥上）。面から少し出た、平たい板
    a = np.array([cx - hx + t, cy - hy + t, cz + hz - e]); b = np.array([cx + hx - t, cy + hy - t, cz + hz - e])
    FRAMES.append(lambda p, a=a, b=b: np.maximum(capsule(a, b, 0.85)(p), np.abs(p[..., 2] - (cz + hz - e)) - e * 0.9))
    m.add(FRAMES[-1], "brace")
    a2 = np.array([cx + hx - e, cy - hy + t, cz + hz - t]); b2 = np.array([cx + hx - e, cy + hy - t, cz - hz + t])
    FRAMES.append(lambda p, a=a2, b=b2: np.maximum(capsule(a, b, 0.85)(p), np.abs(p[..., 0] - (cx + hx - e)) - e * 0.9))
    m.add(FRAMES[-1], "brace")
    for sx in (-1, 1):                                                   # 角の釘（正面と右の面）
        for sy in (-1, 1):
            m.add(sphere((cx + sx * (hx - t / 2), cy + sy * (hy - t / 2), cz + hz + 0.02), 0.32), "rivet")
            m.add(sphere((cx + hx + 0.02, cy + sy * (hy - t / 2), cz + sx * (hz - t / 2)), 0.32), "rivet")


def crates():
    m = Model()
    S = 5.6
    crate_box(m, (-6.2, S, -3.5), (S, S, S))
    crate_box(m, (5.4, S - 0.4, -2.6), (S - 0.4, S - 0.4, S - 0.4))
    crate_box(m, (-5.4, 2 * S + S - 0.6 + 0.02, -4.4), (S - 0.6, S - 0.6, S - 0.6))
    # 麻の袋（右手前。口をしばったもの）
    sx_, sz_ = 12.6, 3.0
    m.add(ellipsoid((sx_, 3.3, sz_), (3.8, 3.4, 3.2)), "sack")                  # 袋のふくらみ
    m.add(ellipsoid((sx_ - 0.2, 6.4, sz_ - 0.2), (2.8, 2.6, 2.4)), "sack")      # 肩
    m.add(cone_y(sx_ - 0.3, sz_ - 0.3, 1.3, 0.75, 8.2, 9.2), "sack")             # しばった首
    m.add(cone_y(sx_ - 0.3, sz_ - 0.3, 0.75, 1.7, 9.2, 10.8), "sack")            # しばった口の上（ひろがる）
    m.add(torus_y((sx_ - 0.3, 9.0, sz_ - 0.3), 0.95, 0.42), "rope")

    def shade(mm, p, n, lum, x, y):
        if mm == "crate":
            d = min(float(f(np.array(p))) for f in FRAMES)
            if d < 0.5:
                lum -= 0.16                                           # 枠・筋かいのきわの、かげの線
            along = p[1] if abs(n[1]) < 0.6 else p[2]
            if (along / 2.5) % 1 < 0.24:
                lum -= 0.12                                            # 板のすき間（横板）
            if ((p[0] * 2.3 + p[2] * 2.3 + p[1] * 0.25) % 2.1) < 0.25:
                lum -= 0.04                                           # 木目
            lum += ((hn(math.floor(along / 2.5), math.floor(p[0] / 11)) % 5) - 2) * 0.02
        if mm == "sack":
            if (math.floor(p[0] * 2) + math.floor(p[1] * 2) + math.floor(p[2] * 2)) % 2 == 0:
                lum -= 0.035                                          # 麻の織り目
            if abs(p[0] - 12.0 + (p[1] - 4) * 0.35) < 0.3 and 1.5 < p[1] < 7:
                lum -= 0.1                                            # 袋のしわ
        if mm in ("frame", "brace"):
            lum -= 0.06
            if ((p[0] + p[1] + p[2]) * 1.7) % 2.3 < 0.3:
                lum -= 0.04
            mm = "frame"
        return lum, mm
    return render(m, 48, 48, 24, 45, ramps_all, shade_fn=shade, shadow=(28, 45.6, 18.5, 2.6))


# ===================================================================== 岩
def faceted(c, r, seed, cut=0.86, n_planes=14):
    """楕円の玉を、いろいろな向きの平らな面で切って、かどの立った岩のかたまりにする。"""
    f = ellipsoid(c, r)
    c = np.array(c, float); r = np.array(r, float)
    for k in range(n_planes):
        h1 = hn(seed, k, 1); h2 = hn(seed, k, 2); h3 = hn(seed, k, 3)
        th = (h1 % 1000) / 1000 * 2 * math.pi
        ph = 0.15 + (h2 % 1000) / 1000 * 1.25                     # 上むき〜横むき（下むきの面は作らない）
        nrm = np.array([math.cos(th) * math.cos(ph), math.sin(ph), math.sin(th) * math.cos(ph)])
        sup = math.sqrt(((nrm * r) ** 2).sum())                    # 楕円のその向きの、いちばん外
        d = sup * (cut + (h3 % 1000) / 1000 * 0.1)
        f = inter(f, (lambda nn, cc, dd: (lambda p: ((p - cc) * nn).sum(-1) - dd))(nrm, c, d))
    return f


def rock2():
    m = Model()
    big = faceted((-1.5, 4.0, -3.0), (10.0, 8.6, 7.4), 11, 0.78, 11)
    side = faceted((8.0, 2.2, -0.6), (5.0, 4.4, 4.2), 23, 0.86, 10)
    top = faceted((-3.5, 8.6, -3.8), (5.6, 3.4, 4.4), 37, 0.84, 9)
    for f in (big, side, top):
        m.add(lambda p, f=f: np.maximum(f(p), -p[..., 1] - 0.2), "rock")
    # ひび（けずったところは、ひびの色）
    m.cut(capsule((-3.6, 10.6, 0.2), (-1.2, 6.6, 2.6), 0.42), "crack")
    m.cut(capsule((-1.2, 6.6, 2.6), (-2.0, 2.0, 3.4), 0.38), "crack")
    m.cut(capsule((-1.2, 6.6, 2.6), (1.6, 4.4, 3.0), 0.34), "crack")
    m.cut(capsule((9.0, 4.8, 2.8), (10.4, 1.6, 3.0), 0.34), "crack")
    # 足もとの小石
    for (px, pz, r) in ((-12.6, -0.6, 1.25), (-13.4, 1.8, 0.8), (11.6, -4.6, 1.0)):
        m.add(ellipsoid((px, r * 0.55, pz), (r, r * 0.8, r)), "pebble")

    def shade(mm, p, n, lum, x, y):
        if mm == "rock":
            lum = 0.06 + lum * 0.86
            lum += (vnoise(p[0] + 0.5, p[1], p[2], 1.4) - 0.5) * 0.06       # 岩はだのむら
            if vnoise(p[0], p[1] + 0.4, p[2], 0.7) > 0.86:
                lum -= 0.09                                                # 小さなくぼみ
            if n[1] > 0.6 and p[1] > 7.5:
                mv = vnoise(p[0] + 1.3, p[1] * 0.6, p[2] + 0.7, 1.6)
                if mv > 0.42:
                    return lum + (0.04 if mv > 0.58 else -0.08), "moss"      # 上のこけ（ふちは少し暗く）
            if p[1] < 1.2:
                lum -= 0.07
        if mm == "crack":
            lum = min(lum, 0.12)
            mm = "rock"
        return lum, mm
    return render(m, 48, 48, 24, 45, ramps_all, shade_fn=shade, shadow=(26.5, 45.6, 17, 2.6))


# ===================================================================== 街灯
def lamp():
    m = Model()
    # 石の台（2段）と、鉄の足
    m.add(box((0, 0.8, 0), (2.9, 0.8, 2.9)), "lampstone")
    m.add(box((0, 2.1, 0), (2.3, 0.6, 2.3)), "lampstone")
    m.add(cone_y(0, 0, 2.0, 1.1, 2.6, 5.2), "lamp")
    m.add(torus_y((0, 5.3, 0), 1.05, 0.4), "lamp")
    # みぞのある柱
    m.add(cyl_y(0, 0, 0.95, 5.0, 29.7), "lamp")
    for k in range(6):
        a = k * math.pi / 3 + 0.3
        m.cut(capsule((math.cos(a) * 1.05, 7.0, math.sin(a) * 1.05), (math.cos(a) * 1.05, 27.7, math.sin(a) * 1.05), 0.3))
    m.add(torus_y((0, 17.5, 0), 1.0, 0.38), "lamp")                    # 柱のなかほどの輪
    m.add(cone_y(0, 0, 1.0, 2.2, 28.0, 29.8), "lamp")                  # 灯り箱の受け
    # 灯り箱（ガラス4まい、上へ少しひろがる。鉄の角柱と、まんなかの横桟）
    yb, yt = 29.8, 37.6

    def hw(y):
        return 2.2 + (y - yb) * 0.06
    m.add(lambda p: np.maximum(np.maximum(np.abs(p[..., 0]), np.abs(p[..., 2])) - hw(p[..., 1]),
                               np.maximum(yb - p[..., 1], p[..., 1] - yt)) * 0.97, "glass")
    for sx in (-1, 1):
        for sz in (-1, 1):
            m.add(capsule((sx * hw(yb), yb, sz * hw(yb)), (sx * hw(yt), yt, sz * hw(yt)), 0.42), "lamp")
    m.add(box((0, yb + 0.3, 0), (2.5, 0.4, 2.5)), "lamp")
    # かさ（張り出したひさしと、四角い屋根）とてっぺんの飾り
    m.add(box((0, yt + 0.3, 0), (3.5, 0.45, 3.5)), "lamp")
    m.add(lambda p: np.maximum((np.maximum(np.abs(p[..., 0]), np.abs(p[..., 2])) - (3.1 - (p[..., 1] - yt - 0.7) * 1.15)) * 0.65,
                               np.maximum(yt + 0.7 - p[..., 1], p[..., 1] - (yt + 3.2))), "cap")
    m.add(cyl_y(0, 0, 0.5, yt + 3.0, yt + 3.9), "lamp")
    m.add(sphere((0, yt + 4.4, 0), 0.8), "lamp")
    m.add(cone_y(0, 0, 0.42, 0.05, yt + 4.9, yt + 5.7), "lamp")

    def colour(mm, p, n, lum, x, y, c):
        if mm == "glass":
            # 灯りは光の向きに関係なく、まんなかほど明るい、あたたかい色
            t = abs(p[1] - (yb + yt) / 2 + 0.6) / ((yt - yb) / 2)
            side = abs(n[0]) > abs(n[2])                              # 右の面（光から遠い面）は、少しこい色
            u = abs(p[2]) if side else abs(p[0])
            core = t * 0.8 + u / 2.6 * 0.6
            if core < 0.42 and not side:
                return "#fffbe0"                                      # まんなかの炎のしん
            if core < 0.72:
                return "#ffe68a" if not side else "#ffcf5c"
            if core < 1.0:
                return "#ffc24a" if not side else "#f0a038"
            return "#e8963a" if not side else "#c8762a"
        return c

    def shade(mm, p, n, lum, x, y):
        if mm == "lamp" and n[1] < 0.3 and p[1] < 30:
            lum += 0.04
        if mm == "cap":
            mm = "lamp"
            if ((p[0] + p[2] + 30) / 1.6) % 1 < 0.2 and n[1] > 0.2:
                lum -= 0.08                                           # 屋根の板金の筋
        return lum, mm
    return render(m, 48, 48, 24, 45, ramps_all, shade_fn=shade, colour_fn=colour, shadow=(26, 45.6, 7.5, 1.9), outline="#141018")


# ===================================================================== 道しるべ
def arrow_board(L, h, tip, th):
    """板の矢（長さの向きは +x。左のはし -L、矢の先 +L、高さの半分 h、厚みの半分 th）。"""
    def f(p):
        u, v, w = p[..., 0], p[..., 1], p[..., 2]
        rect = np.maximum(np.maximum(-L - u, u - (L - tip)), np.abs(v) - h)
        tri = np.maximum(u - L + (np.abs(v) / h) * tip, (L - tip) - u)            # 先の三角
        tri = np.maximum(tri * 0.7, np.abs(v) - h)
        shape = np.minimum(rect, tri)
        return np.maximum(shape, np.abs(w) - th)
    return f


def signpost():
    m = Model()
    # 柱（かどを少し落とした角材）と、てっぺんのとがり、足もとの石
    m.add(rbox((0, 15.5, -2.0), (1.2, 15.5, 1.2), 0.35), "post")
    m.add(lambda p: np.maximum((np.maximum(np.abs(p[..., 0]), np.abs(p[..., 2] + 2.0)) - (1.2 - (p[..., 1] - 31.0) * 0.9)) * 0.7,
                               np.maximum(31.0 - p[..., 1], p[..., 1] - 32.4)), "post")
    m.add(ellipsoid((0.4, 0.4, -1.4), (3.0, 1.2, 2.6)), "stone")
    # 上の矢: 右をさし、少し奥へ向く。下の矢: 左をさし、少し手前へ向く。どちらも柱の前の面に、根もとをとめる
    zf = -2.0 + 1.2 + 0.45                                     # 柱の前の面のすぐ前（板のまんなか）
    for (L, h, base, ang) in ((8.6, 2.1, (-1.0, 26.4, zf), -0.30), (8.4, 2.0, (1.0, 19.2, zf), math.pi - 0.34)):
        cen = np.array(base) + L * np.array([math.cos(ang), 0, math.sin(ang)])   # 板のまんなか（根もとから、さす向きへ L）
        m.add((lambda f, cc: (lambda p: f(p - cc)))(rot_y(arrow_board(L, h, 2.7, 0.42), ang), cen), "board")
    # 釘（板を柱にとめる）
    for yy in (27.3, 25.5, 20.1, 18.3):
        m.add(sphere((0.0, yy, zf + 0.42), 0.38), "rivet")

    def shade(mm, p, n, lum, x, y):
        if mm == "post":
            lum = 0.12 + lum * 0.9
            if ((p[1] * 0.25 + (p[0] + p[2]) * 1.9) % 1.6) < 0.28:
                lum -= 0.06                                           # たての木目
            if p[1] < 2.5:
                lum -= 0.07
        if mm == "board":
            if ((p[1] * 2.2 + p[0] * 0.12 + p[2] * 0.12) % 1.5) < 0.22 and abs(n[1]) < 0.6:
                lum -= 0.06                                           # 横の木目
        return lum, mm

    def colour(mm, p, n, lum, x, y, c):
        if mm == "board" and abs(n[1]) < 0.6:
            # 板に彫った文字の代わりの、こまかい刻み（読めない印。かげの色）
            yy = p[1] - (26.4 if p[1] > 23 else 19.2)
            u = abs(p[0])
            if abs(yy) < 0.5 and 2.8 < u < 11.5 and (x % 4 != 3):
                return MY["board"][2] if lum > 0.4 else MY["board"][1]
        return c
    return render(m, 48, 48, 24, 45, ramps_all, shade_fn=shade, colour_fn=colour, shadow=(25.5, 45.6, 9, 2.0))


# ===================================================================== ベンチ
def bench():
    m = Model()
    Wd = 12.4                                     # 半分の幅
    zs = -3.4                                     # 座面の奥行きのまんなか
    ys = 5.6                                      # 座面の高さ
    for sx in (-1, 1):
        x = sx * (Wd - 2.0)
        # 鉄の脚（横から見て、前の脚・うしろの脚・座面の受け・ひじかけが一つながりの板）
        m.add(box((x, ys / 2, zs + 2.3), (0.42, ys / 2, 0.5)), "iron")                       # 前の脚
        m.add(capsule((x, 0.4, zs - 2.6), (x, ys + 4.9, zs - 2.2), 0.5), "iron")             # うしろの脚（背もたれの柱まで）
        m.add(box((x, ys - 0.75, zs), (0.42, 0.42, 2.7)), "iron")                             # 座面の受け
        m.add(capsule((x, ys + 2.6, zs - 2.1), (x, ys + 2.3, zs + 2.4), 0.42), "iron")        # ひじかけ
        m.add(capsule((x, ys + 2.3, zs + 2.4), (x, ys - 0.3, zs + 2.4), 0.36), "iron")
        m.add(sphere((x, ys + 2.35, zs + 2.55), 0.55), "iron")
        # 石の足（脚の下に、小さな角石）
        for zz in (zs + 2.3, zs - 2.6):
            m.add(rbox((x, 0.45, zz), (0.95, 0.45, 0.95), 0.2), "stone")
    # 座面の板（3まい、前後にならべ、あいだにすき間）
    for dz in (1.75, 0.0, -1.75):
        m.add(rbox((0, ys, zs + dz), (Wd, 0.45, 0.72), 0.18), "slat")
    m.add(box((0, ys - 0.75, zs + 2.15), (Wd - 1.2, 0.4, 0.25)), "slat")                       # 前のはしの幕板
    # 背もたれの板（2まい、少しうしろへかたむく）
    for yy in (ys + 2.6, ys + 4.5):
        m.add(rbox((0, yy, zs - 2.45 - (yy - ys) * 0.1), (Wd + 0.2, 0.75, 0.32), 0.2), "slat")

    def shade(mm, p, n, lum, x, y):
        if mm == "slat":
            if ((p[0] * 0.45 + p[1] * 3.0 + p[2] * 3.0) % 2.2) < 0.28:
                lum -= 0.05                                           # 木目
            lum += ((hn(math.floor(p[1] * 1.2), math.floor(p[2] * 0.6)) % 3) - 1) * 0.025
        if mm == "iron":
            lum += 0.05
        return lum, mm
    return render(m, 48, 48, 20, 45, ramps_all, shade_fn=shade, shadow=(21.5, 45.4, 16.5, 2.2))


OUT = {"barrel": (HERE, "barrel"), "crates": (HERE, "crates"), "rock2": (HERE, "rock2"), "lamp": (HERE, "lamp"),
       "signpost": (HERE, "signpost"), "bench": (R20, "bench")}

if __name__ == "__main__":
    todo = sys.argv[1:] or list(OUT)
    for n in todo:
        img = globals()[n]()
        d, name = OUT[n]
        print(n, save(img, os.path.join(d, name + ".txt"), os.path.join(d, "pal-" + name + ".json")))
