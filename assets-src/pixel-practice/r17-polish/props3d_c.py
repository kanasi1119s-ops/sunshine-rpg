"""町の木や草・岩を、立体の模型から描きなおす（2026-10-06、人間の指示
「町に置いてあるキャラ建物以外のオブジェクト立体感奥行きにこだわって。木々は場所の気候に合わせて。」「ドットを細かく。光加減も大事に。」）。
道具は sdf3d.py（props3d.py と同じ作り方）。光は左上前から。ほかの形が落とす影・すみの暗さつき、足もとにうすく透ける影。すべて一から自作。

  tree4      ふつうの土地の広葉樹: 葉のかたまり（楕円）を何こも重ね、まわりに小さな葉のふさ。かたまりごとに光と影。幹は木の皮のすじ、根の張り出し
  tree-snow  雪をかぶったモミ: 段になった枝（円すい）と、その上に積もった雪（段ごとのふくらみと、たれた雪のかたまり）
  tree-dead  枯れ木: ねじれた幹と、ふた股に分かれていく枝（まるい柱）。上を向いた所に少しの雪、根もとに雪だまり
  palm       ヤシ（砂漠）: 節のある、しなった幹。弓なりにたれる葉（軸と、左右に下がる小葉）、ヤシの実
  cactus     サボテン（砂漠）: たてのひだ（すじ）のある幹と2本の腕、ひだの上のとげ、てっぺんの花
  bush2      実のなる丸い茂み: 葉のかたまりと、赤い実
  bush-snow  雪をかぶった茂み
  rock-snow  雪をかぶった岩: 面のある大きな岩と小石、上に積もった雪
  tree-pine  針葉樹（高原・霧の町・山の町）: 段になった、濃い緑の葉の固まりをのせた枝と、赤みのある幹

使い方: python3 props3d_c.py [名前 ...]   （名前を省くと、ぜんぶ書き出す。書き出し先はこのフォルダ）"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sdf3d import (Model, box, cyl_y, cone_y, sphere, ellipsoid, capsule, diff, inter, render, save)

HERE = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------- 小さな道具
def hn(*a):
    """数をまぜて、毎回おなじになる「でたらめな数」をつくる。"""
    n = 2166136261
    for v in a:
        n = ((n ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    n ^= n >> 15
    n = (n * 2246822519) & 0xFFFFFFFF
    n ^= n >> 13
    return n


def fnoise(p, s, seed=0):
    """たて・よこ・奥の s ごとのます目で、0〜1 の数（ます目ごとにちがう）。"""
    return (hn(math.floor(p[0] / s), math.floor(p[1] / s), math.floor(p[2] / s), seed) & 0xFFFF) / 65535


def spheres(C, R):
    """たくさんの球を、まとめて一つの形にする（速くするため）。"""
    C = np.array(C, float); R = np.array(R, float)

    def f(p):
        d = np.sqrt(((p[..., None, :] - C) ** 2).sum(-1)) - R
        return d.min(-1)
    return f


def capsules(A, B, R, R2=None):
    """たくさんの、まるい柱を、まとめて一つの形にする（R2 があれば、B の側の太さ）。"""
    A = np.array(A, float); B = np.array(B, float); R = np.array(R, float)
    R2 = R if R2 is None else np.array(R2, float)
    BA = B - A; BB = np.maximum((BA * BA).sum(-1), 1e-9)

    def f(p):
        pa = p[..., None, :] - A
        h = np.clip((pa * BA).sum(-1) / BB, 0, 1)
        rr = R + (R2 - R) * h
        d = np.sqrt(((pa - BA * h[..., None]) ** 2).sum(-1)) - rr
        return d.min(-1)
    return f


def ellipsoids(C, Rr):
    """たくさんの楕円の玉を、まとめて一つの形にする。"""
    C = np.array(C, float); Rr = np.array(Rr, float)

    def f(p):
        q = (p[..., None, :] - C) / Rr
        k0 = np.sqrt((q * q).sum(-1)); k1 = np.sqrt(((q / Rr) ** 2).sum(-1))
        return (k0 * (k0 - 1) / np.maximum(k1, 1e-6)).min(-1)
    return f


def tufts(clumps, rng, n, r, down=-0.35, scale=0.9):
    """葉のかたまり（楕円）の表面に、小さな葉のふさ（球）をちらす。下を向いた所には、あまり付けない。"""
    C, R = [], []
    for (c, rr) in clumps:
        for _ in range(n):
            d = rng.normal(size=3); d /= np.linalg.norm(d)
            if d[1] < down:
                continue
            C.append(np.array(c) + d * np.array(rr) * scale)
            R.append(r * (0.75 + 0.5 * rng.random()))
    return spheres(C, R)


class Scaled:
    """模型全体を s 倍の大きさにして見せる（色や模様の計算には、もとの大きさの位置をわたす）。"""
    def __init__(self, model, s):
        self.m, self.s = model, s

    def sdf(self, p):
        return self.m.sdf(p / self.s) * self.s

    def material(self, p):
        return self.m.material(p / self.s)


def fit(model, W, H, ramps, shade_fn=None, colour_fn=None, shadow_r=(12, 2.2), shadow_dx=3.0, outline="#1e1a18", ambient=0.22, pad=24, scale=1.0, front_tilt=25):   # 2026-10-06: 木はすべて正面の少し上から見る（丸い形がゆがまない）
    """s（scale）倍にした模型を大きめの紙に描いてから、形（影はのぞく）が横のまんなか、いちばん下が紙の下になるよう、W×H に切りぬく。
    はみ出したら知らせる。影は、幹の足もと（x=0, y=0）から、光と反対の右奥へ少しずらした楕円。"""
    BW, BH = W + 2 * pad, H + 2 * pad
    CX, GROUND = BW / 2, BH - pad - 1.5
    if scale != 1.0:
        sf, cf = shade_fn, colour_fn
        shade_fn = sf and (lambda m_, p, n, lum, x, y: sf(m_, p / scale, n, lum, x, y))
        colour_fn = cf and (lambda m_, p, n, lum, x, y, c: cf(m_, p / scale, n, lum, x, y, c))
        model = Scaled(model, scale)
    img = render(model, BW, BH, CX, GROUND, ramps, shade_fn=shade_fn, colour_fn=colour_fn, outline=outline, ambient=ambient,
                 shadow=(CX + shadow_dx, GROUND + 0.3, shadow_r[0], shadow_r[1]), front_tilt=front_tilt)
    solid = np.array([[c != "" and len(c) == 7 for c in row] for row in img])
    anyc = np.array([[c != "" for c in row] for row in img])
    ys, xs = np.nonzero(solid)
    x0, x1 = xs.min(), xs.max()
    bottom = np.nonzero(anyc.any(1))[0].max()
    left = int(round((x0 + x1 + 1) / 2 - W / 2))
    top = bottom + 1 - H
    out = img[top:top + H, left:left + W]
    lost = solid.sum() - np.array([[c != "" and len(c) == 7 for c in row] for row in out]).sum()
    if lost:
        print("  はみ出し", lost, "ドット / 形の大きさ", x1 - x0 + 1, "×", bottom - ys.min() + 1)
    return out


# ---------------------------------------------------------------- 色の段（暗い → 明るい）
LEAF = ["#0b1d10", "#112a16", "#18381b", "#20491f", "#2b5c23", "#387028", "#47852d", "#5a9a33", "#72af3c", "#90c44c", "#b4d968"]
BARK = ["#1a110b", "#2a1c12", "#3b2a1a", "#4e3822", "#62472b", "#785935", "#8e6c42", "#a68352"]
SNOW = ["#2e3a58", "#46557a", "#62739a", "#8294b8", "#a4b4d2", "#c4d2e8", "#dfe8f4", "#f2f6fb", "#ffffff"]
FIR = ["#08161a", "#0d2024", "#132c2c", "#1a3a36", "#234a40", "#2e5c4a", "#3b6e55", "#4c8262"]
PINE = ["#08150f", "#0d1f14", "#132b19", "#1a381f", "#224726", "#2c572d", "#386836", "#467a40", "#578e4a"]
PINEBARK = ["#1c0e0a", "#2e1810", "#432316", "#5a301c", "#713f24", "#8a502e", "#a2643a"]
DEADBARK = ["#16120f", "#241d18", "#342a22", "#463a2f", "#5a4b3d", "#6e5e4d", "#837360", "#9a8a74"]
PALMBARK = ["#21160c", "#342414", "#4a361e", "#614829", "#7a5c35", "#937043", "#ab8754", "#c4a068"]
FROND = ["#0e2210", "#153216", "#1d451c", "#275a22", "#337029", "#428632", "#549c3a", "#6cb246", "#8cc85a"]
COCO = ["#1e1408", "#33230e", "#4c3616", "#664a1e", "#7e5e28"]
CACTUS = ["#0c2216", "#12301c", "#1a4024", "#22522c", "#2c6434", "#38763e", "#468a48", "#5a9e56", "#74b468"]
SPINE = "#f0ead2"
FLOWER = ["#6e1c34", "#a8284a", "#dc4466", "#f47a90", "#ffb4c0"]
FLOWER_Y = ["#7a5410", "#b88418", "#ecc030", "#ffe27a"]
BERRY = ["#3a0a12", "#6a1220", "#a01e2c", "#d23a40", "#f27466"]
ROCK = ["#1e1e26", "#2e2e38", "#40404c", "#545462", "#6a6a78", "#82828e", "#9a9aa4", "#b2b2ba", "#c8c8ce"]
LEAF_BUSH = ["#0b1d10", "#112a16", "#18381b", "#20491f", "#2b5c23", "#387028", "#47852d", "#5a9a33", "#72af3c", "#90c44c"]
LEAF_COLD = ["#0a1a18", "#10261f", "#173327", "#1f4230", "#29523a", "#346346", "#427552", "#54885f"]


def leaf_shade(lum, p, n, seed=0, k=0.07):
    """葉のこまかなむら（1ドットくらいのます目で明るさをゆらす）と、葉の重なりの暗いすじ。"""
    lum += (fnoise(p, 0.9, seed) - 0.5) * 2 * k
    if fnoise(p + 0.45, 1.6, seed + 7) > 0.78:
        lum -= 0.08                                   # 葉と葉のすき間の、小さな暗がり
    return lum


def leaf_colour(m, lum, p, x, y, c, ramp, seed=0):
    """光の当たった所に、ときどき明るい葉の点（きらり）を置く。"""
    if lum > 0.62 and fnoise(p, 0.8, seed + 31) > 0.86:
        i = ramp.index(c) if c in ramp else -1
        if 0 <= i < len(ramp) - 1:
            return ramp[i + 1]
    return c


def bark_shade(lum, p, axis_x=0.0, axis_z=0.0, stripes=7, seed=0):
    """幹の皮のたてのすじ（幹のまわりの角度で）と、こまかなむら。"""
    ang = math.atan2(p[2] - axis_z, p[0] - axis_x)
    s = (ang * stripes / math.pi + fnoise((p[0], p[1] * 0.25, p[2]), 1.0, seed) * 0.6) % 1
    if s < 0.22:
        lum -= 0.11
    elif s < 0.35:
        lum += 0.03
    lum += (fnoise(p, 0.8, seed + 3) - 0.5) * 0.08
    return lum


# ===================================================================== 1. ふつうの広葉樹
# 2026-10-06 作りなおし（人間の指示「木も作り直し」「町になじんでない」）: 正面の少し上から見る見え方（丸い物が卵形にゆがまない）。
# 大きな葉のかたまり5つで、まるい冠（上がもり上がり、左右がふくらむ）。かたまりのふちに小さな葉の玉をのせて、葉のぎざぎざに。
# 色は町の草地と同じ、オリーブがかった落ちついた緑（OLIVE）。幹は根もとが広がり、冠の下は暗い。
OLIVE_LEAF = ["#1a2a14", "#223619", "#2c441f", "#375226", "#42602d", "#4e6e34", "#5a7c3c", "#668a44", "#73974d", "#82a458", "#93b266"]


def tree4():
    """2026-10-06 作りなおし（人間の指示「木。いっそのこともっとでかくしてリアルな木にしようか。ドットを細かく。強弱が感じられるような、
    立体感ある、木を作ろう」「全部光の感じも意識して」）: 64×80 の大きな広葉樹。
    幹から枝が何度も分かれてのび、枝の先ごとに葉のかたまり（大小40ほど）。かたまりのすきまから、奥の枝と暗い冠の中がのぞく。
    光: 左上からの日ざしで、冠の左上は明るく、右下と中は深いかげ（明暗の強弱をはっきり）。冠のふちの葉は、すける光で少し明るい。"""
    rng = np.random.default_rng(31)
    m = Model()
    # 幹（根もとが広がる）
    m.add(capsule((0, -0.5, 0), (0.6, 13, 0), 3.2, 2.4), "bark")
    for ang in (-2.7, -1.2, 0.2, 1.4, 2.6):
        dx, dz = math.cos(ang), math.sin(ang)
        m.add(capsule((dx * 5.5, 0.0, dz * 3.6), (dx * 0.8, 4.5, dz * 0.8), 0.9, 2.2), "bark")
    # 枝: 再帰で分かれる
    tips = []

    def branch(p0, d, length, r, depth):
        p1 = (p0[0] + d[0] * length, p0[1] + d[1] * length, p0[2] + d[2] * length)
        m.add(capsule(p0, p1, r, r * 0.7), "bark")
        if depth == 0:
            tips.append(p1)
            return
        for k in range(2 if depth > 1 else 3):
            yaw = rng.uniform(-1.0, 1.0); up = rng.uniform(0.15, 0.6)
            nd = np.array([d[0] + yaw * 0.8, d[1] + up, d[2] + rng.uniform(-0.6, 0.6)])
            nd /= np.linalg.norm(nd)
            branch(p1, nd, length * rng.uniform(0.62, 0.78), r * 0.68, depth - 1)
    for (dx, dz) in ((-1.0, 0.2), (1.0, -0.1), (0.15, -0.9), (-0.3, 0.8), (0.6, 0.7), (0.0, 0.0)):
        d = np.array([dx, 2.1, dz]); d /= np.linalg.norm(d)
        branch((0.4, 11.5, 0), d, 12.5, 1.8, 3)
    # 葉のかたまり: 枝の先ごとに1〜2つ、上ほど大きく
    clumps = []
    for t in tips:
        for _ in range(2):
            c = (t[0] + rng.uniform(-1.5, 1.5), t[1] + rng.uniform(-0.5, 2.0), t[2] + rng.uniform(-1.5, 1.5))
            rr = rng.uniform(3.8, 5.6)
            clumps.append((c, (rr * 1.1, rr * 0.95, rr)))
    # 冠の中をうめる、まるい大きなかたまり（奥）と、冠の下のふくらみ
    cy_ = float(np.mean([c[0][1] for c in clumps]))
    clumps.append(((0, cy_, -2.5), (13, 11, 10)))
    clumps.append(((0, cy_ - 8, 1.5), (10, 6, 7)))
    m.add(ellipsoids([c for c, _ in clumps], [r for _, r in clumps]), "leaf")
    m.add(tufts(clumps, rng, 110, 1.15), "leaf")

    V = np.array([0.0, math.sin(math.radians(25)), math.cos(math.radians(25))])

    def shade(mm, p, n, lum, x, y):
        if mm == "bark":
            lum = bark_shade(lum, p, 0, 0, stripes=9)
            if p[1] > 18:
                lum -= 0.16                                    # 冠の下・中の枝は暗い
        if mm == "leaf":
            lum = leaf_shade(lum, p, n, 1, k=0.07)
            lum = (lum - 0.45) * 1.25 + 0.52                   # 明暗の強弱をはっきり（全体は暗くしすぎない）
            lum += 0.12 * max(0.0, float(n[1]))               # 空からの光（上を向いた葉は明るい）
            rim = (1 - max(0.0, float(np.dot(n, V)))) ** 3
            lum += 0.18 * rim * (1 if n[0] < 0.3 else 0.4)     # ふちの葉は、すける光で少し明るい
            if n[1] < -0.35:
                lum -= 0.12                                    # 下を向いた葉は深いかげ
        return lum, mm

    def colour(mm, p, n, lum, x, y, c):
        if mm == "leaf":
            return leaf_colour(mm, lum, p, x, y, c, TREE_BIG, 1)
        if mm == "bark" and p[1] > 24:
            return TREE_BIG[2]                                   # 冠の奥の枝は、葉のかげにしずむ
        if mm == "bark" and p[1] > 15:
            k = BARK.index(c) if c in BARK else 2
            return BARK[max(1, min(k, 3))]                       # 冠の下の枝は、暗い樹皮
        return c

    return fit(m, 64, 80, {"leaf": TREE_BIG, "bark": BARK}, shade_fn=shade, colour_fn=colour, scale=1.32,
               shadow_r=(22, 3.2), outline="#101a0c", ambient=0.26)


# 大きな木の葉の色（町の草地と同じ色合いで、暗い所はより深く、明るい所はより明るく。強弱のため段を多く）
TREE_BIG = ["#0e180a", "#14220e", "#1a2c12", "#223817", "#2b451c", "#355322", "#406129", "#4c6f31", "#587d39", "#648b42", "#71984b", "#80a556", "#90b262", "#a2c070"]


# ===================================================================== 2. 雪をかぶったモミ
def tree_snow():
    m = Model()
    TZ = -2.0
    m.add(capsule((0, -0.5, TZ), (0, 46, TZ), 2.0, 0.6), "bark")
    tiers = [(4.0, 18.5, 12.0), (12.0, 15.5, 11.0), (19.5, 12.5, 10.0), (26.5, 9.8, 9.0), (33.0, 7.0, 8.0), (38.5, 4.4, 7.0)]
    tipC, tipR, snC, snR = [], [], [], []
    for i, (y0, r0, h) in enumerate(tiers):
        m.add(cone_y(0, TZ, r0, 0.6, y0, y0 + h), "fir")
        # 段のふち: たれ下がった枝先（小さな球を輪にならべる）
        k = int(r0 * 1.2) + 6
        for j in range(k):
            a = (j + 0.5 * (i % 2)) / k * 2 * math.pi
            rr = r0 - 0.4 + 0.6 * math.sin(j * 2.3)
            tipC.append((math.cos(a) * rr, y0 - 0.2 - 0.4 * math.cos(j * 1.7), TZ + math.sin(a) * rr)); tipR.append(1.25)
        # 積もった雪: 段より少し小さく高い円すいと、雪のふちの、たれたかたまり
        rs = r0 * 0.72
        ys = y0 + h * (1 - (rs - 0.6) / (r0 - 0.6)) + 0.4
        # 段の円すいを少し上へずらした「雪の層」を、ふちが波うつ円の内側だけ残す
        layer = cone_y(0, TZ, r0, 0.6, y0 + 0.85, y0 + h + 0.85)
        edge = (lambda rs=rs, i=i: (lambda p: np.sqrt(p[..., 0] ** 2 + (p[..., 2] - TZ) ** 2)
                                    - (rs + 0.9 * np.sin(5 * np.arctan2(p[..., 2] - TZ, p[..., 0]) + i * 1.3))))()
        m.add(inter(layer, edge), "snow")
        k2 = int(rs * 1.1) + 5
        for j in range(k2):
            a = (j + 0.3 * i) / k2 * 2 * math.pi
            rr = rs - 0.3
            snC.append((math.cos(a) * rr, ys + 0.3 + 0.35 * math.sin(j * 3.1), TZ + math.sin(a) * rr)); snR.append(1.35 + 0.35 * math.sin(j * 1.9 + i))
    m.add(spheres(tipC, tipR), "fir")
    m.add(spheres(snC, snR), "snow")
    m.add(cone_y(0, TZ, 1.6, 0.2, 44, 51), "fir")                          # てっぺん
    m.add(sphere((0, 47.4, TZ), 1.2), "snow")
    m.add(ellipsoid((0, 0.2, TZ), (8, 1.2, 5)), "snow")                    # 根もとの雪だまり

    def shade(mm, p, n, lum, x, y):
        if mm == "fir":
            ang = math.atan2(p[2] - TZ, p[0])
            if (ang * 9 / math.pi + fnoise(p, 1.3, 2) * 0.5) % 1 < 0.25:
                lum -= 0.1                                                  # 枝のすき間（放射のすじ）
            lum += (fnoise(p, 0.8, 5) - 0.5) * 0.12
        if mm == "snow":
            lum = lum * 1.1 + 0.08 + (fnoise(p, 1.0, 9) - 0.5) * 0.05
        if mm == "bark":
            lum = bark_shade(lum, p, 0, TZ, 5)
        return lum, mm

    return fit(m, 44, 48, {"fir": FIR, "snow": SNOW, "bark": BARK}, shade_fn=shade, scale=0.76,
                  shadow_r=(14, 2.4), outline="#0a1418", ambient=0.24)


# ===================================================================== 3. 枯れ木
def tree_dead():
    m = Model()
    A, B, R0, R1 = [], [], [], []
    snowy = []

    def branch(a, d, length, r, depth, seed):
        """a から d の向きへ枝をのばし、先で2つ（ときどき3つ）に分かれる。少しずつ曲がる（ねじれ）。"""
        a = np.array(a, float); d = np.array(d, float); d /= np.linalg.norm(d)
        segs = 3
        for s in range(segs):
            bend = np.array([math.sin(seed * 1.7 + s * 2.1), 0.1, math.cos(seed * 2.3 + s * 1.3) * 0.3]) * 0.3
            d = d + bend; d[1] += 0.03; d /= np.linalg.norm(d)
            b = a + d * length / segs
            rr = r * (1 - 0.25 * (s + 1) / segs)
            A.append(a); B.append(b); R0.append(max(r * (1 - 0.25 * s / segs), 0.38)); R1.append(max(rr, 0.38))
            a = b
        if depth == 0:
            return
        k = 3 if (seed % 3 == 0 and depth >= 2) else 2
        for j in range(k):
            sp = (j - (k - 1) / 2) * 1.0 + math.sin(seed * 3.7) * 0.2 + (0.45 if d[0] > 0 else -0.45)
            side = np.cross(d, [0, 0, 1.0]);
            if np.linalg.norm(side) < 1e-3:
                side = np.array([1.0, 0, 0])
            side /= np.linalg.norm(side)
            nd = d * 0.8 + side * sp * 0.95 + np.array([0, -0.1, math.cos(seed + j * 2.0) * 0.25])
            branch(a, nd, length * 0.74, r * 0.6, depth - 1, seed * 3 + j + 1)

    TZ = -2.0
    # 幹: 3つのまるい柱で、少し右へ左へよじれる
    trunk = [(0, -0.5, TZ), (0.8, 6, TZ - 0.4), (-0.6, 11, TZ + 0.3), (0.4, 16, TZ)]
    for i in range(3):
        m.add(capsule(trunk[i], trunk[i + 1], 3.0 - i * 0.6, 2.4 - i * 0.6), "bark")
    for ang in (-2.4, -0.7, 0.8, 2.2):
        m.add(capsule((math.cos(ang) * 5.0, 0.0, TZ + math.sin(ang) * 3.6), (math.cos(ang) * 0.8, 4.5, TZ + math.sin(ang) * 0.8), 0.8, 1.9), "bark")
    branch(trunk[3], (-0.6, 1, 0.1), 11.5, 1.2, 3, 2)
    branch(trunk[3], (0.65, 1, -0.2), 11, 1.15, 3, 5)
    branch((0.6, 10.0, TZ + 0.2), (-1, 0.5, 0.3), 7.5, 0.85, 2, 7)
    branch((-0.3, 13.0, TZ), (1, 0.55, 0.2), 7.5, 0.8, 2, 11)
    m.add(capsules(A, B, R0, R1), "bark")
    m.add(ellipsoid((0.5, 0.0, TZ), (9, 1.3, 5.5)), "snow")               # 根もとの雪だまり
    m.cut(sphere((0.8, 7.5, TZ + 2.7), 0.9), "hole")                       # 幹のうろ

    def shade(mm, p, n, lum, x, y):
        if mm == "bark":
            lum = bark_shade(lum, p, 0, TZ, 6, 4) if p[1] < 16 else lum + (fnoise(p, 0.7, 3) - 0.5) * 0.1
            if n[1] > 0.62 and p[1] > 9 and fnoise(p, 1.4, 8) > 0.35:
                return lum + 0.25, "snow"                                   # 上を向いた所に、少し雪
        if mm == "snow":
            lum = lum * 1.1 + 0.08
        if mm == "hole":
            lum = 0.05
        return lum, mm

    return fit(m, 48, 48, {"bark": DEADBARK, "snow": SNOW, "hole": DEADBARK}, shade_fn=shade, scale=0.8,
                  shadow_r=(13, 2.2), outline="#100c0a", ambient=0.24)


# ===================================================================== 4. ヤシ
def palm():
    m = Model()
    TZ = -1.0
    # しなった幹: ゆるい弧の上を、少しずつ細くなる節の柱でつなぐ
    pts = []
    for i in range(9):
        t = i / 8
        pts.append((-5.0 * t * t + 2.5 * t, t * 33.0, TZ))
    for i in range(8):
        m.add(capsule(pts[i], pts[i + 1], 2.1 - i * 0.1, 2.0 - i * 0.1), "trunk")
        m.add(cyl_y(pts[i + 1][0], TZ, 2.3 - i * 0.1, pts[i + 1][1] - 0.9, pts[i + 1][1] - 0.2), "trunk")   # 節のふくらみ
    top = np.array(pts[-1]) + np.array([0, 1.0, 0])
    m.add(sphere(top, 2.6), "frond")                                        # 葉の付け根
    # 葉: 軸（まるい柱のつながり）と、左右に下がる小葉
    A, B, R0, R1 = [], [], [], []
    LA, LB, LR = [], [], []
    fr = [(-2.75, 14, 0.5), (2.6, 13.5, 0.3), (-0.35, 14.5, 0.6), (0.45, 13.5, 0.2), (-2.05, 9, 1.0), (1.6, 11, 0.4), (3.14, 11, 0.0)]
    for k, (az, L, droop) in enumerate(fr):
        d = np.array([math.cos(az), 0, -math.sin(az) * 0.8])
        prev = top.copy()
        N = 12
        for s in range(1, N + 1):
            t = s / N
            pos = top + d * L * t + np.array([0, 6.0 * math.sin(t * 2.2) - (9.0 + droop * 3.0) * t * t, 0])
            A.append(prev); B.append(pos); R0.append(0.55 * (1 - t) + 0.3); R1.append(0.55 * (1 - t) + 0.25)
            if s >= 2:
                tang = pos - prev; tang /= np.linalg.norm(tang)
                side = np.cross(tang, [0, 1, 0]); side /= max(np.linalg.norm(side), 1e-6)
                ll = 3.8 * math.sin(math.pi * min(1, t * 1.05)) + 0.5
                for sg in (-1, 1):
                    tip = pos + side * sg * ll * 0.6 + np.array([0, -ll * 0.9, 0]) + tang * 1.1
                    LA.append(pos); LB.append(tip); LR.append(0.34)
            prev = pos
    m.add(capsules(A, B, R0, R1), "frond")
    m.add(capsules(LA, LB, LR), "frond")
    m.add(spheres([top + (-1.7, -2.4, 2.2), top + (1.0, -2.6, 2.4), top + (-0.3, -3.6, 2.8), top + (2.2, -1.9, 1.0)], [1.5, 1.5, 1.4, 1.35]), "coco")
    m.add(ellipsoid((0.3, 0.0, TZ), (5.5, 0.9, 3.5)), "trunk")             # 根もとの、ふくらみ

    def shade(mm, p, n, lum, x, y):
        if mm == "trunk":
            seg = (p[1] / 4.125) % 1
            lum += 0.1 if seg > 0.7 else (-0.12 if seg < 0.18 else 0)       # 節: 上がふくらんで明るく、下に影
            if fnoise((p[0], p[1] * 0.5, p[2]), 0.8, 2) > 0.7:
                lum -= 0.08                                                 # 皮のささくれ
        if mm == "frond":
            lum = lum * 1.05 + (fnoise(p, 0.7, 4) - 0.5) * 0.12
        if mm == "coco":
            lum += 0.05
        return lum, mm

    return fit(m, 48, 48, {"trunk": PALMBARK, "frond": FROND, "coco": COCO}, shade_fn=shade,
                  shadow_r=(13, 2.2), outline="#0e1408", ambient=0.22)


# ===================================================================== 5. サボテン
def rib_col(cx, cz, R, y0, y1, ribs=9, depth=0.32):
    """たてのひだのある、上がまるい柱（サボテンの幹・腕）。"""
    def f(p):
        dx = p[..., 0] - cx; dz = p[..., 2] - cz
        yy = np.clip(p[..., 1], y0, y1)
        ang = np.arctan2(dz, dx)
        rr = R + depth * np.cos(ribs * ang)
        d = np.sqrt(dx ** 2 + dz ** 2 + (p[..., 1] - yy) ** 2)
        return (d - rr) * 0.8
    return f


def cactus():
    m = Model()
    TZ = -1.0
    RIBS = 10
    m.add(rib_col(0, TZ, 3.1, 0.0, 34.0, RIBS), "cac")
    arms = [(-1, 12.0, 10.0, 25.0, 2.0), (1, 17.0, 10.0, 30.0, 1.9)]
    for sg, ya, ax, ytop, r in arms:
        # ひじ: 幹から横へ出て、上へまがる（四分の一の輪を、まるい柱でつなぐ）
        rad = ax - 2.5
        prev = (sg * 2.0, ya, TZ)
        for k in range(1, 7):
            a = k / 6 * math.pi / 2
            pt = (sg * (ax - rad * math.cos(a)), ya + rad * math.sin(a) * 0.9 - (1 - math.cos(a)) * 0.0, TZ)
            pt = (sg * (2.0 + rad * math.sin(a)), ya + rad * (1 - math.cos(a)), TZ)
            m.add(capsule(prev, pt, r), "cac")
            prev = pt
        m.add(rib_col(prev[0], TZ, r, prev[1], ytop, 8, 0.25), "cac")
    m.add(spheres([(-0.6, 37.2, TZ + 1.1), (0.9, 37.0, TZ + 0.9), (0.1, 37.3, TZ - 0.4), (0.15, 37.6, TZ + 0.5)], [0.95, 0.95, 0.9, 0.8]), "flower")
    m.add(sphere((0.15, 38.0, TZ + 0.6), 0.55), "flower_y")
    m.add(spheres([(9.5 + 0.2, 32.1, TZ + 0.5), (9.5 - 0.6, 31.9, TZ)], [0.8, 0.7]), "flower")

    def shade(mm, p, n, lum, x, y):
        if mm == "cac":
            lum = lum * 1.05 + (fnoise(p, 0.9, 6) - 0.5) * 0.06
        return lum, mm

    def colour(mm, p, n, lum, x, y, c):
        if mm == "cac":
            # とげ: ひだの山の上に、間をあけて白い点（光の当たる側は、はっきり）
            for (cx_, r_) in ((0.0, 3.6),):
                pass
            ax_x = 0.0
            for sg, ya, ax, ytop, r in arms:
                if abs(p[0] - sg * (ax - 0.5)) < r + 0.8 and p[1] > ya + 3.5:
                    ax_x = sg * (ax - 0.5)
            ang = math.atan2(p[2] - TZ, p[0] - ax_x)
            ridge = math.cos(RIBS * ang) > 0.82
            if ridge and (p[1] * 0.9 + (hn(round(ang * 3)) % 3) * 0.3) % 2.2 < 0.45 and lum > 0.25:
                return SPINE if lum > 0.45 else "#b8b098"
        return c

    return fit(m, 48, 48, {"cac": CACTUS, "flower": FLOWER, "flower_y": FLOWER_Y}, shade_fn=shade, colour_fn=colour,
                  shadow_r=(9.5, 2.0), outline="#08140c", ambient=0.22)


# ===================================================================== 6. 茂み・雪の茂み・雪の岩
def bush_model(rng):
    m = Model()
    clumps = [
        ((-7, 6.0, -3), (6.5, 5.5, 4.5)),
        ((5.5, 6.5, -3.5), (7, 6, 4.5)),
        ((-1, 9.5, -4), (6, 5, 4)),
        ((-1.5, 4.5, 0), (6.5, 4.5, 3.0)),
        ((9.5, 4.0, -2), (4, 3.6, 3.5)),
        ((-11, 3.5, -1.5), (3.6, 3.3, 3.2)),
    ]
    m.add(ellipsoids([c for c, _ in clumps], [r for _, r in clumps]), "leaf")
    m.add(tufts(clumps, rng, 18, 1.2, down=-0.2), "leaf")
    return m, clumps


def bush2():
    rng = np.random.default_rng(12)
    m, clumps = bush_model(rng)
    berries = []
    for (c, r) in clumps:
        for _ in range(3):
            a = rng.uniform(-1.0, 1.0); b = rng.uniform(-0.2, 0.6)
            d = np.array([math.sin(a) * math.cos(b), math.sin(b), math.cos(a) * math.cos(b)])
            berries.append(np.array(c) + d * np.array(r) * 0.98)
    m.add(spheres(berries, [0.75] * len(berries)), "berry")

    def shade(mm, p, n, lum, x, y):
        if mm == "leaf":
            lum = leaf_shade(lum, p, n, 3)
        if mm == "berry":
            lum += 0.1
        return lum, mm

    def colour(mm, p, n, lum, x, y, c):
        if mm == "leaf":
            return leaf_colour(mm, lum, p, x, y, c, LEAF_BUSH, 3)
        return c

    return fit(m, 30, 18, {"leaf": LEAF_BUSH, "berry": BERRY}, shade_fn=shade, colour_fn=colour, scale=0.88,
                  shadow_r=(13, 1.7), outline="#0a160c", ambient=0.22)


def bush_snow():
    rng = np.random.default_rng(12)
    m, clumps = bush_model(rng)
    # 雪: かたまりの上に、うすく平たい楕円をのせる
    snow = [((c[0] - 0.4, c[1] + r[1] * 0.62, c[2]), (r[0] * 0.82, r[1] * 0.42, r[2] * 0.8)) for c, r in clumps]
    m.add(ellipsoids([c for c, _ in snow], [r for _, r in snow]), "snow")
    berries = [(-4.5, 4.0, 2.6), (2.0, 5.0, 2.8), (6.5, 4.0, 0.6), (-8.5, 4.5, 0.5), (0.0, 3.0, 2.9)]
    m.add(spheres(berries, [0.7] * len(berries)), "berry")

    def shade(mm, p, n, lum, x, y):
        if mm == "leaf":
            lum = leaf_shade(lum, p, n, 5) - 0.04
        if mm == "snow":
            lum = lum * 1.1 + 0.1 + (fnoise(p, 1.0, 9) - 0.5) * 0.05
        if mm == "berry":
            lum += 0.1
        return lum, mm

    return fit(m, 30, 18, {"leaf": LEAF_COLD, "snow": SNOW, "berry": BERRY}, shade_fn=shade, scale=0.8,
                  shadow_r=(13, 1.7), outline="#0a1418", ambient=0.24)


def rock_snow():
    m = Model()
    # 岩: 楕円の玉を、ななめの平らな面でけずって、角のある岩に
    big = ellipsoid((-1.5, 5.5, -3), (10.5, 7.5, 6.5))
    for (nx, ny, nz, off) in ((0.6, 0.5, 0.6, 7.0), (-0.75, 0.35, 0.55, 7.6), (0.1, 0.9, 0.4, 9.6), (0.9, 0.2, -0.3, 7.2), (-0.2, 0.3, 0.95, 4.8)):
        nn = np.array([nx, ny, nz]) / math.sqrt(nx * nx + ny * ny + nz * nz)
        big = (lambda f, nn=nn, off=off: (lambda p: np.maximum(f(p), (p - np.array([-1.5, 1.0, -3])) @ nn - off)))(big)
    m.add(big, "rock")
    small = ellipsoid((8.5, 2.3, 0.5), (3.6, 2.8, 2.8))
    small = (lambda f: (lambda p: np.maximum(f(p), (p - np.array([8.5, 0, 0.5])) @ (np.array([0.5, 0.7, 0.5]) / 1.0) - 2.6)))(small)
    m.add(small, "rock")
    m.add(ellipsoid((-10.5, 1.3, 0.5), (2.2, 1.7, 1.8)), "rock")
    # 雪: 上の面に、あつみのある雪（岩の形を上にずらして、上の半分だけ）
    cap = lambda p: np.maximum(m.solids[0][0](p - np.array([0.3, 1.1, 0.2])), 8.8 - p[..., 1] - 0.7 * np.sin(p[..., 0] * 0.9) + 0.12 * p[..., 0])
    m.add(cap, "snow")
    m.add(inter(lambda p: small(p - np.array([0, 0.7, 0])), lambda p: 3.4 - p[..., 1]), "snow")
    m.add(ellipsoid((-1.0, 0.1, -1.5), (13, 0.9, 6)), "snow")             # 足もとの雪

    def shade(mm, p, n, lum, x, y):
        if mm == "rock":
            lum += (fnoise(p, 1.1, 2) - 0.5) * 0.12
            if fnoise((p[0] * 0.6, p[1] * 1.6, p[2]), 1.0, 5) > 0.88:
                lum -= 0.15                                                 # ひび
        if mm == "snow":
            lum = lum * 1.1 + 0.1 + (fnoise(p, 1.0, 9) - 0.5) * 0.05
        return lum, mm

    return fit(m, 28, 20, {"rock": ROCK, "snow": SNOW}, shade_fn=shade, scale=0.9,
                  shadow_r=(12, 1.6), outline="#14141c", ambient=0.24)


# ===================================================================== 7. 針葉樹（高原・霧・山の町）
def tree_pine():
    rng = np.random.default_rng(7)
    m = Model()
    TZ = -2.0
    m.add(capsule((0, -0.5, TZ), (-2.2, 44, TZ), 2.1, 0.5), "bark")
    for ang in (-2.4, -0.6, 1.0, 2.5):
        m.add(capsule((math.cos(ang) * 4.0, 0.0, TZ + math.sin(ang) * 3.0), (math.cos(ang) * 0.6, 3.5, TZ + math.sin(ang) * 0.6), 0.7, 1.5), "bark")
    # 段ごとに、幹のまわりへ枝をのばし、先に平たい葉の固まり（楕円）をのせる。上へ行くほど小さく
    clumps = []
    BA, BB, BR = [], [], []
    tiers = [(9.0, 16.0, 7), (16.0, 13.5, 6), (22.5, 11.0, 6), (28.5, 8.5, 5), (34.0, 6.0, 4), (38.5, 3.8, 3)]
    for i, (y0, reach, k) in enumerate(tiers):
        for j in range(k):
            a = (j + 0.5 * (i % 2)) / k * 2 * math.pi + 0.3
            rr = reach * (0.8 + 0.2 * math.sin(j * 2.7 + i))
            px, pz = math.cos(a) * rr * 0.66 - 0.05 * y0, TZ + math.sin(a) * rr * 0.5   # 上ほど少し左へ（右へ傾いて見えないように）
            py = y0 + 0.5 * math.sin(j * 1.9 + i)
            BA.append((-0.05 * y0, y0 - 1.2, TZ)); BB.append((px * 0.8, py - 0.6, TZ + (pz - TZ) * 0.8)); BR.append(0.5)
            sz = 1.8 + reach * 0.3
            clumps.append(((px, py, pz), (sz, 1.35 + reach * 0.03, sz * 0.8)))   # 平たい葉の固まり（雲のような段）
        clumps.append(((-0.05 * y0, y0 + 0.6, TZ), (reach * 0.32, 1.6, reach * 0.28)))  # 幹のまわり（段のまんなか）
    clumps.append(((-2.1, 41.5, TZ), (1.6, 2.8, 1.6)))
    m.add(capsules(BA, BB, BR), "bark")
    m.add(ellipsoids([c for c, _ in clumps], [r for _, r in clumps]), "pine")
    m.add(tufts(clumps, rng, 10, 1.05, down=-0.1, scale=0.92), "pine")

    def shade(mm, p, n, lum, x, y):
        if mm == "pine":
            # 針の葉: 小さなます目のむらと、よこ長の暗いすじ（針の束）
            lum = lum * 1.12 + 0.03 + (fnoise(p, 0.75, 8) - 0.5) * 0.14
            if fnoise((p[0] * 0.5, p[1] * 1.8, p[2] * 0.5), 1.0, 9) > 0.75:
                lum -= 0.09
        if mm == "bark":
            lum = bark_shade(lum, p, 0, TZ, 5, 6)
        return lum, mm

    def colour(mm, p, n, lum, x, y, c):
        if mm == "pine":
            return leaf_colour(mm, lum, p, x, y, c, PINE, 8)
        return c

    return fit(m, 44, 48, {"pine": PINE, "bark": PINEBARK}, shade_fn=shade, colour_fn=colour, scale=0.93,
                  shadow_r=(12, 2.2), outline="#06100a", ambient=0.22)


# ---------------------------------------------------------------- 書き出し
OUT = {
    "tree4": ("tree4", "tree"),
    "tree-snow": ("tree-snow", "tree-snow"),
    "tree-dead": ("tree-dead", "tree-dead"),
    "palm": ("palm", "palm"),
    "cactus": ("cactus", "cactus"),
    "bush2": ("bush2", "bush2"),
    "bush-snow": ("bush-snow", "bush-snow"),
    "rock-snow": ("rock-snow", "rock-snow"),
    "tree-pine": ("tree-pine", "tree-pine"),
}

if __name__ == "__main__":
    todo = sys.argv[1:] or list(OUT)
    for name in todo:
        img = globals()[name.replace("-", "_")]()
        txt, pal = OUT[name]
        print(name, "色の数", save(img, os.path.join(HERE, txt + ".txt"), os.path.join(HERE, "pal-" + pal + ".json")))
