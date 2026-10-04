"""ボスが使う炎の術のエフェクト（ドット絵のコマ）を作る（2026-10-04、人間の指示「では火の魔法のバージョンも作って」）。

雷の術（lightning.py）と同じ形・同じ1ドットの大きさ。使い方:
  python3 fire.py 出力フォルダ --boss ボスのanim.json [--seed 7]
出力: aura.json（発動・ボスのまわり）・charge.json（ため: 手の上の火の玉）・
      fireball.json（火球・1人: 火の玉が飛んで当たり、はじける）・pillars.json（火柱・全体: 味方の足もとから火柱が立つ）
コマには、雷の形に加えて次を入れる（見本の動画・効果音の道具がこれを読む）:
  "flash_color": 光の色（炎はあたたかい色）、"party": [[味方の番号, 絵, 後ろへのずれ], ...]（当たった味方の絵）、
  "se": [[効果音の名前, 音量], ...]（このコマで鳴らす音）
炎の描き方（docs/design/battle-effects.md）:
- 炎は「熱さ」の格子を下から上へ流して冷ましていく（ゆらぐ舌の形が自然に出る）。熱いほど 白→黄→橙→赤→暗い赤。
- 芯がいちばん明るく、外へ向かって暗く（pixel-trace-log.md の決まり）。暗い赤は1ドットおき。
- 爆発は、ふくらむ火の玉 → まん中から燃えつきて輪になる → 煙（灰色の点々）がのぼる。
"""
import json
import math
import os
import random
import sys

import numpy as np
from scipy import ndimage

sys.path.insert(0, os.path.dirname(__file__))
from lightning import Canvas, ring, Sparks  # noqa: E402

PAL = {
    "W": "#fffbe6",  # 芯（白に近い黄）
    "Y": "#ffe36b",  # 黄
    "G": "#ffc23d",  # 濃い黄（火の粉）
    "O": "#ff8c1f",  # 橙
    "R": "#e0401c",  # 赤
    "D": "#9a1f14",  # 暗い赤
    "M": "#5a1410",  # いちばん暗い赤（炎のふち・焦げ）
    "K": "#2f2424",  # 黒い煙・すす
    "S": "#5e5050",  # 煙
    "L": "#8a7c78",  # 薄い煙
}
WARM = "#ffb060"
RAMP = [(0.88, "W"), (0.74, "Y"), (0.6, "G"), (0.46, "O"), (0.32, "R"), (0.2, "D")]


def noise(rnd, h, w, cell, seed_shift=0):
    """なめらかな雑音（0〜1）。cell ドットごとの乱数の格子を、なめらかに広げる"""
    gh, gw = h // cell + 3, w // cell + 3
    g = np.array([[rnd.random() for _ in range(gw)] for _ in range(gh)])
    z = ndimage.zoom(g, cell, order=1)
    return z[:h, :w]


def heat_paint(cv, heat, layer_mask=None, dither_low=True, smooth=0.9):
    """熱さの配列を、炎の色でキャンバスに描く。smooth: 色を分ける前に少しぼかす（1ドットのざらつきを消し、色の帯をきれいに）"""
    if smooth:
        heat = ndimage.gaussian_filter(heat, smooth)
    H, W = heat.shape
    yy, xx = np.indices((H, W))
    out = np.full((H, W), ".", dtype="<U1")
    for th, c in RAMP[::-1]:
        out[heat > th] = c
    low = (heat > 0.12) & (heat <= 0.2) & (((yy + xx) % 2 == 0) if dither_low else True)
    out[low] = "M"
    m = out != "."
    if layer_mask is not None:
        m &= layer_mask
    cv.a[m] = out[m]


class FireField:
    """下から上へ流れる熱さの格子（炎の舌がゆらぐ）"""

    def __init__(self, h, w, rnd, decay=0.92, cool=0.035, wind=0.0):
        self.h, self.w, self.rnd = h, w, rnd
        self.heat = np.zeros((h, w))
        self.decay, self.cool, self.wind = decay, cool, wind
        self.np = np.random.default_rng(rnd.randint(0, 1 << 30))

    def step(self, src=None, src_heat=1.0, sub=1):
        """1コマ分すすめる。sub: 1コマのあいだに何回流すか（多いほど、炎が速く高くのびる）"""
        for _ in range(sub):
            self._one(src, src_heat)
        return self.heat

    def _one(self, src, src_heat):
        H = self.heat
        if src is not None:
            flick = 0.65 + 0.35 * self.np.random(H.shape)
            H[src] = np.maximum(H[src], (src_heat * flick)[src])
        P = np.pad(H, ((0, 2), (1, 1)))
        avg = (P[1:-1, :-2] + P[1:-1, 1:-1] + P[1:-1, 2:] + P[2:, 1:-1]) / 4.0
        # すぐ下の熱さを、左右に1ドットずつランダムにずらして持ち上げる（炎の舌がちぎれて、ゆらぐ）
        pick = self.np.integers(0, 3, H.shape)
        below = np.choose(pick, [P[1:-1, :-2], P[1:-1, 1:-1], P[1:-1, 2:]])
        up = below * 0.6 + avg * 0.4
        new = up * self.decay - self.cool * 2 * self.np.random(H.shape) ** 2
        if self.wind:
            new = np.roll(new, int(round(self.wind)), axis=1)
        self.heat = np.clip(new, 0, 1)


def frame(cv, ms, dim=0.0, flash=0.0, shake=0, party=None, se=None, back=None):
    x, y, rows = cv.out()
    f = {"ms": ms, "x": x, "y": y, "rows": rows, "dim": round(dim, 2), "flash": round(flash, 2), "shake": shake, "flash_color": WARM}
    if party: f["party"] = party
    if se: f["se"] = se
    if back is not None:
        bx, by, brows = back.out()
        f.update({"bx": bx, "by": by, "back": brows})
    return f


def ellipse_mask(h, w, cy, cx, rx, ry, thick=1.5):
    yy, xx = np.indices((h, w))
    d = np.sqrt(((xx - cx) / max(rx, 0.5)) ** 2 + ((yy - cy) / max(ry, 0.5)) ** 2)
    return np.abs(d - 1) * min(rx, ry * 3) < thick


# ---------------------------------------------------------------- 発動（ボスのまわり）
def make_aura(seed, boss_mask, n=16, fade=4):
    """足もとに炎の陣（赤い輪と、回る炎の印）。輪から炎の舌が立ちのぼり、体のふちが赤く脈打ち、ふちから小さな炎がゆらぐ。
    火の粉がのぼり、最後に炎が大きく立って消える。奥の半分はボスのうしろ（back）"""
    rnd = random.Random(seed + 21)
    M = 24
    bh, bw = boss_mask.shape
    W, H = bw + 2 * M, bh + 2 * M
    body = np.zeros((H, W), bool); body[M:M + bh, M:M + bw] = boss_mask
    ys, xs = np.nonzero(body)
    foot_y = int(ys.max()) - 2
    cx = int(np.median(xs[ys > ys.max() - 30]))
    k3 = np.ones((3, 3), bool)
    rim1 = ndimage.binary_dilation(body, k3) & ~body
    edge = body & ~ndimage.binary_erosion(body)
    ey, ex = np.nonzero(edge)
    top_edge = [(y, x) for y, x in zip(ey, ex) if y < foot_y - 20]
    f_front = FireField(H, W, rnd, decay=0.93, cool=0.03)
    f_back = FireField(H, W, rnd, decay=0.97, cool=0.014)
    f_lick = FireField(H, W, rnd, decay=0.86, cool=0.06)
    yy, xx = np.indices((H, W))
    embers = []
    frames = []
    for i in range(n + fade):
        t = min(1.0, i / (n - 1)); out = max(0.0, (i - n + 1) / fade)
        front, back = Canvas(W, H), Canvas(W, H)
        R = 62 * min(1.0, (i + 1) / 5)
        # 炎の陣: 赤い輪（2重）と、回る炎の印
        if out < 1:
            for rr, col, dith in ((R, "R", False), (R * 0.8, "D", True), (R * 0.52, "O", True)):
                steps = int(2 * math.pi * rr) * 2 + 8
                for q in range(steps):
                    a = 2 * math.pi * q / steps
                    if dith and q % 2: continue
                    if out and rnd.random() < out: continue
                    y, x = foot_y + math.sin(a) * rr * 0.26, cx + math.cos(a) * rr
                    (back if math.sin(a) < 0 else front).put(y, x, col, over=False)
            for q in range(8):
                a = i * 0.25 + 2 * math.pi * q / 8
                y, x = foot_y + math.sin(a) * R * 0.66 * 0.26, cx + math.cos(a) * R * 0.66
                cv = back if math.sin(a) < 0 else front
                cv.put(y, x, "O"); cv.put(y - 1, x, "Y"); cv.put(y - 2, x, "W" if q % 2 else "Y"); cv.put(y, x - 1, "R"); cv.put(y, x + 1, "R")
        # 輪から立ちのぼる炎（奥は背の高い炎、手前は低い炎）
        ring_m = ellipse_mask(H, W, foot_y, cx, R * 0.92, R * 0.92 * 0.26, 1.2)
        src_on = i < n
        hb = f_back.step(ring_m & (yy < foot_y) if src_on else None, 0.55 + 0.45 * t, sub=3)
        hf = f_front.step(ring_m & (yy >= foot_y) if src_on else None, 0.45 + 0.35 * t, sub=3)
        heat_paint(back, hb * (1 - out))
        heat_paint(front, hf * (1 - out), layer_mask=~body | (yy > foot_y - 10))
        # 体のふち: 赤く脈打ち、上のほうのふちから小さな炎がゆらぐ
        if i < n:
            pulse = (i % 4) < 2
            front.mask_put(rim1 & ((yy + xx) % 2 == (i % 2)), "R" if pulse else "D", under=True)
            src = np.zeros((H, W), bool)
            for _ in range(int(4 + 10 * t)):
                y, x = rnd.choice(top_edge); src[max(0, y - 1), x] = True
            hl = f_lick.step(src & ~body, 0.9, sub=2)
        else:
            hl = f_lick.step(None, sub=2)
        heat_paint(front, hl * (1 - out), layer_mask=~body)
        # 火の粉
        if i < n:
            for _ in range(3 + int(4 * t)):
                a = rnd.uniform(0, 2 * math.pi); rr = rnd.uniform(0.3, 1.0) * R
                embers.append([foot_y + math.sin(a) * rr * 0.26, cx + math.cos(a) * rr, rnd.uniform(1.2, 2.8), rnd.randint(6, 11), rnd.uniform(0, 6)])
        for e in embers:
            if e[3] <= 0: continue
            col = "W" if e[3] > 8 else ("Y" if e[3] > 5 else ("O" if e[3] > 2 else "R"))
            (back if rnd.random() < 0.35 else front).put(e[0], e[1] + math.sin(e[4] + e[3]) * 1.2, col)
            e[0] -= e[2]; e[3] -= 1
        # 最後: 炎が大きく立つ（陣の上に背の高い炎）
        if n - 3 <= i < n:
            f_back.step(ring_m, 1.0, sub=3); f_front.step(ring_m & (yy >= foot_y), 0.8, sub=2)
        se = [["fire/cast", 0.9]] if i == 0 else None
        frames.append(frame(front, 70 if i < n else 60, back=back, se=se))
    return {"name": "炎の発動（ボスのまわり）", "w": W, "h": H, "anchor": [M, M], "palette": PAL, "frames": frames,
            "note": "anchor はボスの絵（132×132）の左上。back はボスのうしろに描く"}


# ---------------------------------------------------------------- ため（手の上の火の玉）
def fire_ball(cv, cy, cx, r, rnd, t, vel=(0.0, 0.0), stretch=3.2, extra=0.0):
    """火の玉: まん中が白く、外へ向かって赤く。動いていると、進む向きの反対へ尾をひく"""
    H, W = cv.h, cv.w
    pad = int(r * (stretch + 2)) + 4
    y0, y1 = max(0, int(cy - pad)), min(H, int(cy + pad))
    x0, x1 = max(0, int(cx - pad)), min(W, int(cx + pad))
    if y0 >= y1 or x0 >= x1:
        return
    yy, xx = np.indices((y1 - y0, x1 - x0)); yy = yy + y0; xx = xx + x0
    ry, rx = yy - cy, xx - cx
    sp = math.hypot(*vel)
    if sp > 0.1:
        vy, vx = vel[0] / sp, vel[1] / sp
        along = -(ry * vy + rx * vx)
        perp = np.abs(ry * vx - rx * vy)
        d = np.where(along > 0, np.sqrt((along / stretch) ** 2 + perp ** 2), np.hypot(ry, rx))
    else:
        d = np.hypot(ry, rx)
    nz = noise(rnd, y1 - y0, x1 - x0, 3)
    heat = (1 - d / max(r, 0.5)) * 1.15 + (nz - 0.5) * 0.5 + extra
    sub = Canvas(x1 - x0, y1 - y0)
    heat_paint(sub, np.clip(heat, 0, 1))
    m = sub.a != "."
    cv.a[y0:y1, x0:x1][m] = sub.a[m]


def make_charge(seed):
    rnd = random.Random(seed + 22)
    W = H = 96; cy, cx = 50, 48
    ff = FireField(H, W, rnd, decay=0.88, cool=0.06)
    yy, xx = np.indices((H, W))
    frames = []
    N = 14
    swirl = []
    for i in range(N):
        cv = Canvas(W, H)
        t = i / (N - 1)
        r = 3 + 10 * t + (0.8 if i % 2 else 0)
        # 玉の上半分から炎の舌がのびる
        top = (np.hypot(yy - cy, xx - cx) < r + 1) & (yy < cy)
        heat_paint(cv, ff.step(top, 1.0, sub=3))
        fire_ball(cv, cy, cx, r, rnd, t)
        # まわりから、うずを巻いて火の粉が吸いこまれる
        for _ in range(4):
            swirl.append([rnd.uniform(0, 2 * math.pi), rnd.uniform(28, 40)])
        for s in swirl:
            if s[1] <= r: continue
            y, x = cy + math.sin(s[0]) * s[1] * 0.8, cx + math.cos(s[0]) * s[1]
            cv.put(y, x, "Y" if s[1] < 18 else ("O" if s[1] < 28 else "R"))
            s[0] += 0.5; s[1] -= 4.5
        frames.append(frame(cv, 80 if i < N - 3 else 70, dim=0.1 + 0.25 * t))
    # 最後: 玉がぎゅっと縮んで、光る
    for j, rr in enumerate((10, 15)):
        cv = Canvas(W, H)
        fire_ball(cv, cy, cx, rr, rnd, 1, extra=0.25 - 0.1 * j)
        ring(cv, cy, cx, 14 + j * 7, 14 + j * 7, "O", dither=bool(j))
        frames.append(frame(cv, 60, dim=0.35, flash=0.2 - 0.1 * j))
    return {"name": "炎のため", "w": W, "h": H, "anchor": [cx, cy], "palette": PAL, "frames": frames}


# ---------------------------------------------------------------- 火球（1人）
def make_fireball(seed, start=(87, 10), target=(368, 165), member=0):
    """画面ぜんたいのキャンバス（400×170、anchor は画面の左上）。火の玉がボスの手の上から、弧をえがいて味方1人へ飛び、はじける"""
    rnd = random.Random(seed + 23)
    W, H = 400, 172
    sx, sy = start; tx, ty = target[0], target[1] - 14        # 胸のあたりに当たる
    cxp, cyp = (sx + tx) / 2, min(sy, ty) - 40                # 弧の頂点のめやす
    def bez(u):
        return ((1 - u) ** 2 * sy + 2 * (1 - u) * u * cyp + u * u * ty, (1 - u) ** 2 * sx + 2 * (1 - u) * u * cxp + u * u * tx)
    frames = []
    centers = []   # コマごとの、絵のまん中（火の玉の位置・当たった所）
    trail = []
    us = [0.08, 0.2, 0.36, 0.55, 0.76, 0.93]
    for k, u in enumerate(us):
        cv = Canvas(W, H)
        y, x = bez(u); py, px = bez(max(0, u - 0.06))
        vel = (y - py, x - px)
        for tr in trail:                                   # 通ったあとの火の粉と煙
            tr[2] -= 1
            if tr[2] <= 0: continue
            col = ("O" if tr[2] > 3 else "R") if tr[3] else ("S" if tr[2] > 2 else "K")
            if tr[3] or (int(tr[0]) + int(tr[1])) % 2 == 0:
                cv.put(tr[0], tr[1], col)
            tr[0] += -0.6 if not tr[3] else 0.8
        fire_ball(cv, y, x, 14, rnd, u, vel=vel, stretch=3.6)
        for _ in range(9):
            trail.append([y + rnd.uniform(-4, 4), x - vel[1] * rnd.uniform(0.5, 2) + rnd.uniform(-3, 3), rnd.randint(3, 6), rnd.random() < 0.6])
        se = [["fire/whoosh", 0.9]] if k == 0 else None
        frames.append(frame(cv, 50, dim=0.3, se=se)); centers.append((int(round(x)), int(round(y))))
    # 当たって、はじける
    ff = FireField(H, W, rnd, decay=0.9, cool=0.045)
    fcol = FireField(H, W, rnd, decay=0.975, cool=0.012)
    yy, xx = np.indices((H, W))
    ground = (np.abs(yy - target[1]) < 3) & (np.abs(xx - tx) < 34)
    sparks = Sparks(rnd, ty, tx, 40, target[1])
    smoke = []
    R = [16, 28, 36, 41, 43, 42, 40, 37, 34, 31, 28, 25, 22]
    for k, rr in enumerate(R):
        cv = Canvas(W, H)
        burn = min(1.0, k / 6)
        # 火の玉がふくらみ、まん中から燃えつきていく（輪に）
        d = np.hypot((yy - ty) * 1.15, xx - tx)
        nz = noise(rnd, H, W, 4)
        heat = (1 - d / rr) * 1.25 + (nz - 0.5) * 0.55
        heat = heat - np.clip(burn * 1.1 - d / rr, 0, 1) * 1.4
        if k >= 2:
            heat = heat * (1 - (k - 2) / 13)
        # つづけて2つの小さな爆発（左下・右上）。豪快に（人間の指示「火のエフェクトをもっと豪快に」）
        for (ox, oy, k0) in ((-24, 2, 2), (22, -16, 3)):
            kk = k - k0
            if 0 <= kk < 7:
                r2 = [8, 15, 19, 20, 19, 17, 14][kk]
                d2 = np.hypot((yy - ty - oy) * 1.15, xx - tx - ox)
                h2 = (1 - d2 / r2) * 1.25 + (noise(rnd, H, W, 3) - 0.5) * 0.5 - np.clip(kk / 4 * 1.1 - d2 / r2, 0, 1) * 1.4
                heat = np.maximum(heat, np.clip(h2, 0, 1))
        # 爆発のまん中から、火がもくもくと立ちのぼる（きのこの形）
        if 2 <= k <= 8:
            col = (np.hypot(yy - (ty - 6), (xx - tx) * 0.8) < 9)
            fcol.step(col, 1.0, sub=7)
        else:
            fcol.step(None, sub=7)
        heat = np.maximum(heat, fcol.heat)
        # 地面から炎が立つ（ところどころから。一面に置くと、平らな帯に見えた）
        gsrc = ground & (noise(rnd, H, W, 3) > 0.5) & (np.abs(xx - tx) < 34 - k)
        hf = ff.step(gsrc if k < 9 else None, 0.95, sub=6)
        heat = np.maximum(np.clip(heat, 0, 1), hf * (1 - max(0, k - 6) / 5))
        # 煙（灰色の点々。のぼって大きくなる）
        if 2 <= k <= 6:
            for _ in range(2):
                smoke.append([ty - rnd.uniform(0, 10), tx + rnd.uniform(-14, 14), rnd.uniform(2, 4)])
        for s in smoke:
            for y in range(int(s[0] - s[2]), int(s[0] + s[2]) + 1):
                for x in range(int(s[1] - s[2]), int(s[1] + s[2]) + 1):
                    if (y - s[0]) ** 2 + (x - s[1]) ** 2 <= s[2] ** 2 and (y + x + k) % 2 == 0:
                        cv.put(y, x, "K" if s[2] < 4 else ("S" if s[2] < 6 else "L"), over=False)
            s[0] -= 1.8; s[2] += 0.6
        heat_paint(cv, heat)
        if k <= 3:   # 当たった瞬間の、とがった光（白→黄→橙）
            for q in range(10):
                a = q * math.pi / 5 + rnd.uniform(-0.2, 0.2); L = rr * (1.5 if q % 2 == 0 else 1.0)
                for s_ in range(int(L)):
                    cv.put(ty + math.sin(a) * s_, tx + math.cos(a) * s_, "W" if s_ < L * 0.3 else ("Y" if s_ < L * 0.6 else "O"), over=False)
        sparks.step(cv)
        for x in range(tx - 12, tx + 13):               # 地面の焦げ
            if k >= 3 and ((x + k) % 2 == 0 or abs(x - tx) < 7):
                cv.put(target[1] + 1, x, "K", over=False)
        flash = {0: 0.4, 1: 0.18}.get(k, 0.0)
        shake = {0: 6, 1: 5, 2: 4, 3: 3, 4: 2, 5: 1}.get(k, 0)
        party = [[member, "flash_left", 2]] if k == 0 else ([[member, "burn_left" if k in (1, 3, 5, 7) else "hurt_left", 3]] if k < 9 else [[member, "hurt_left", 1]])
        se = [["fire/explode", 1.0]] if k == 0 else None
        frames.append(frame(cv, 55 if k < 4 else 75, dim=0.45 - 0.04 * k, flash=flash, shake=shake, party=party, se=se)); centers.append((tx, ty))
    # ドット絵エディタは幅256までなので、コマごとに「火の玉（当たった所）のまわり 120×104」だけを切り出し、
    # 画面のどこに置くかを "at"（画面の点）に書く（anchor はキャンバスの中のその点）
    CW, CH, AX, AY = 200, 160, 100, 112
    out = []
    for f, (cx, cy) in zip(frames, centers):
        full = np.full((H, W), ".", dtype="<U1")
        for yy_, r in enumerate(f["rows"]):
            full[f["y"] + yy_, f["x"]:f["x"] + len(r)] = list(r)
        win = Canvas(CW, CH)
        x0, y0 = cx - AX, cy - AY
        sy0, sy1 = max(0, y0), min(H, y0 + CH); sx0, sx1 = max(0, x0), min(W, x0 + CW)
        win.a[sy0 - y0:sy1 - y0, sx0 - x0:sx1 - x0] = full[sy0:sy1, sx0:sx1]
        x, y, rows = win.out()
        g = dict(f); g.update({"x": x, "y": y, "rows": rows, "at": [cx, cy]})
        out.append(g)
    return {"name": "火球（1人）", "w": CW, "h": CH, "anchor": [AX, AY], "palette": PAL, "frames": out,
            "note": "コマごとに \"at\"（画面の点）へ anchor を合わせて置く。ボスの手の上 (87,10) から味方1人の足もと (368,165) へ飛ぶ形で作った（ほかの組み合わせは作りなおす）"}


# ---------------------------------------------------------------- 火柱（全体）
def make_pillars(seed, targets=((22, 5), (8, -13), (-8, 5), (-22, -13))):
    """味方の足もとが赤く光り（予告）、地面から太い火柱が少しずつずれて立ち、足もとが火の海になる。
    最後に、ぜんぶの火柱がいっせいに燃え上がって（大炎上）、煙と火の粉が残る（人間の指示「火のエフェクトをもっと豪快に」）"""
    rnd = random.Random(seed + 24)
    W, H = 220, 220
    ax, ay = 110, 200
    spots = [(ax + dx, ay + dy) for dx, dy in targets] + [(ax + 44, ay + 2), (ax - 52, ay - 4)]
    order = [4, 0, 2, 5, 1, 3]
    starts = {k: 4 + j * 2 for j, k in enumerate(order)}
    fields = {k: FireField(H, W, rnd, decay=0.99, cool=0.005) for k in range(len(spots))}
    sea = FireField(H, W, rnd, decay=0.955, cool=0.02)
    yy, xx = np.indices((H, W))
    sparks = [Sparks(rnd, y - 4, x, 14, y) for x, y in spots]
    smoke = []
    frames = []
    last_start = max(starts.values())
    BIG = last_start + 6                      # 大炎上のコマ
    N = BIG + 12
    sea_band = (yy >= ay - 22) & (yy <= ay + 6) & (np.abs(xx - ax) < 72)
    for i in range(N):
        cv = Canvas(W, H)
        party, se = [], []
        if i == 0: se.append(["fire/rumble", 0.9])
        big = BIG <= i < BIG + 3
        if i == BIG: se.append(["fire/explode", 1.0]); se.append(["fire/erupt", 0.9])
        for k, (x, y) in enumerate(spots):
            s = i - starts[k]
            if s < 0:
                # 予告: 足もとに赤い輪が光る（だんだん強く、ひびから火の粉）
                if i >= 1:
                    rr = 9 + (i % 2)
                    for q in range(32):
                        a_ = 2 * math.pi * q / 32
                        if (q + i) % 2: continue
                        cv.put(y + math.sin(a_) * rr * 0.3, x + math.cos(a_) * rr, "R" if s < -2 else "O", over=False)
                    if s >= -2:
                        cv.put(y - rnd.randint(1, 6), x + rnd.randint(-6, 6), "Y")
                continue
            on = s < 6 or big
            src = (np.abs(yy - y) <= 2) & (np.abs(xx - x) <= 10) if on else None
            fields[k].step(src, 1.0, sub=13 if (s < 3 or big) else 10)
            if s == 0:
                se.append(["fire/erupt", 1.0 if k == order[0] else 0.75])
            if k < 4:
                if s == 0 or i == BIG: party.append([k, "flash_left", 2])
                elif s < 6 or big: party.append([k, "burn_left" if (s + i) % 2 else "hurt_left", 3 if big else 2])
                else: party.append([k, "hurt_left", 1])
            if s >= 1:
                sparks[k].step(cv)
                if s in (1, 4) or i == BIG:
                    sparks[k] = Sparks(rnd, y - 6, x, 10, y) if i != BIG else Sparks(rnd, y - 10, x, 18, y)
            if s == 7 or i == BIG + 3:
                for _ in range(4): smoke.append([y - rnd.uniform(10, 50), x + rnd.uniform(-10, 10), rnd.uniform(2.5, 4)])
        # 足もとの火の海（2本目の火柱が立ったころから、大炎上のあとまで）
        sea_on = starts[order[1]] <= i < BIG + 3
        sea_src = sea_band & (noise(rnd, H, W, 4) > (0.6 if not big else 0.4)) if sea_on else None
        sea.step(sea_src, 0.8 if not big else 1.0, sub=5)
        heat = sea.heat.copy()
        for k in fields:
            heat = np.maximum(heat, fields[k].heat)
        for s_ in smoke:
            for y in range(int(s_[0] - s_[2]), int(s_[0] + s_[2]) + 1):
                for x in range(int(s_[1] - s_[2]), int(s_[1] + s_[2]) + 1):
                    if (y - s_[0]) ** 2 + (x - s_[1]) ** 2 <= s_[2] ** 2 and (y + x + i) % 2 == 0:
                        cv.put(y, x, "K" if s_[2] < 4.5 else ("S" if s_[2] < 7 else "L"), over=False)
            s_[0] -= 1.8; s_[2] += 0.55
        heat_paint(cv, heat)
        first = i == starts[order[0]]
        flash = 0.25 if first else (0.35 if i == BIG else 0.0)
        shake = 3 if first else (5 if i == BIG else (3 if i == BIG + 1 else (2 if any(i == starts[k] for k in starts) else 0)))
        dim = min(0.6, 0.15 + 0.08 * i) if i < N - 6 else max(0.0, 0.6 - 0.1 * (i - (N - 6)))
        frames.append(frame(cv, 60 if i < BIG + 3 else 85, dim=dim, flash=flash, shake=shake, party=party or None, se=se or None))
    return {"name": "火柱（全体）", "w": W, "h": H, "anchor": [ax, ay], "palette": PAL, "frames": frames}

if __name__ == "__main__":
    out = sys.argv[1]
    seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 7
    os.makedirs(out, exist_ok=True)
    from PIL import Image
    an = json.load(open(sys.argv[sys.argv.index("--boss") + 1]))
    a = np.array([[c != "." for c in r] for r in an["flat_attack3"][5]], np.uint8) * 255
    bm = np.array(Image.fromarray(a).resize((132, 132), Image.LANCZOS)) > 110
    for name, fx in (("aura", make_aura(seed, bm)), ("charge", make_charge(seed)), ("fireball", make_fireball(seed)), ("pillars", make_pillars(seed))):
        json.dump(fx, open(f"{out}/{name}.json", "w"), ensure_ascii=False)
        print(name, fx["name"], len(fx["frames"]), "コマ", sum(f["ms"] for f in fx["frames"]), "ミリ秒")
