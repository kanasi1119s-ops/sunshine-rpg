"""味方・敵が使う術のエフェクト（ドット絵のコマ）を、属性ごとに作る（2026-10-05、人間の指示
「モーションドットをもっと派手にできないかな？この動画の炎の術みたいに」「モーション作るときドット絵エディタ使って細かく作って」
「細かく派手に作っていいからね」）。

ボスの雷・炎の術（lightning.py・fire.py）と同じ作り方（熱さの格子を流す・芯が白く外へ暗く・いちばん外は1ドットおき・
けむりは網目）で、どの戦いでも使える形にした。1ドットは戦闘画面（論理 400×225）の1ドット。

使い方: python3 spells.py 出力フォルダ [--seed 7] [--only fire,water]
出力: 出力フォルダ/<属性>/<種類>.json
  種類: hit（1人に当たる。anchor＝当たる人の足もとのまん中）、area（全体の術で、1人ずつに立つもの。anchor＝足もと）、
        charge（ため。anchor＝となえる人の足もとのまん中）、bolt（飛んでいく弾。左へ飛ぶ向き。anchor＝弾のまん中。くり返す）
  {"name", "w", "h", "anchor": [x, y], "palette": {記号: 色}, "frames": [{"ms", "x", "y", "rows", "dim", "flash", "shake", "flash_color"}]}
ドット絵エディタ（tools/pixel-practice/fx-editor.mjs）に1コマずつ入れて、シート（PNG）に書き出し、ゲームはそのシートを使う。

記号（どの属性も同じ記号で、色だけちがう）:
  W 芯（いちばん明るい）→ Y → G → O → R → D（暗い）→ M（いちばん暗い。1ドットおき）、K S L けむり・霧（濃い→うすい）、X Z 飾りの色
"""
import json
import math
import os
import random
import sys

import numpy as np
from scipy import ndimage

sys.path.insert(0, os.path.dirname(__file__))
from lightning import Canvas, zigzag, path_mask, draw_glow, branches  # noqa: E402
from fire import FireField, noise  # noqa: E402

# ---------------------------------------------------------------- 属性ごとの色
PALS = {
    "fire": {"W": "#fffbe6", "Y": "#ffe36b", "G": "#ffc23d", "O": "#ff8c1f", "R": "#e0401c", "D": "#9a1f14", "M": "#5a1410",
             "K": "#2f2424", "S": "#5e5050", "L": "#8a7c78", "X": "#ffd9a0", "Z": "#3a1a10"},
    "water": {"W": "#f4fcff", "Y": "#c4ecff", "G": "#86ccff", "O": "#4a9cf0", "R": "#2a68cc", "D": "#1a3e94", "M": "#0f2460",
              "K": "#5a7aa0", "S": "#9ab8d8", "L": "#d0e4f4", "X": "#e8f8ff", "Z": "#204a80"},
    "ice": {"W": "#ffffff", "Y": "#e0f6ff", "G": "#b0e4fa", "O": "#78c4ee", "R": "#4a94d8", "D": "#2a5ca8", "M": "#1a3470",
            "K": "#7a98b8", "S": "#b4cce0", "L": "#e4f2fa", "X": "#f0fbff", "Z": "#3a6ab0"},
    "wind": {"W": "#ffffff", "Y": "#dcfff0", "G": "#a8f0cc", "O": "#6ad8a0", "R": "#38b070", "D": "#1e7a48", "M": "#0f4a2a",
             "K": "#8a7a5a", "S": "#b8a888", "L": "#e0d8c0", "X": "#6ac040", "Z": "#a07040"},
    "light": {"W": "#ffffff", "Y": "#fffbd0", "G": "#fff09a", "O": "#ffd85a", "R": "#f0b030", "D": "#c07a18", "M": "#7a4a10",
              "K": "#c8b890", "S": "#e8dcb8", "L": "#fff8e4", "X": "#fff4c0", "Z": "#d89a30"},
    "bolt": {"W": "#ffffff", "Y": "#fff4b0", "G": "#ffd75e", "O": "#ff9a3c", "R": "#8ee6ff", "D": "#4d7bff", "M": "#2e2163",
             "K": "#2a2440", "S": "#4a4460", "L": "#7a7490", "X": "#7a4fe0", "Z": "#c8f4ff"},
    "rock": {"W": "#f4e4c4", "Y": "#dcc49a", "G": "#c0a070", "O": "#a07c50", "R": "#7c5a38", "D": "#563c24", "M": "#33220f",
             "K": "#6a5a48", "S": "#9a8a74", "L": "#c8bca6", "X": "#ffd080", "Z": "#4a4a50"},
    "heal": {"W": "#ffffff", "Y": "#e6ffee", "G": "#b4ffcc", "O": "#78f0a0", "R": "#40d078", "D": "#22a058", "M": "#126a38",
             "K": "#9ad8b0", "S": "#c4f0d4", "L": "#ecfff2", "X": "#fff6b0", "Z": "#5ac060"},
    "buff": {"W": "#ffffff", "Y": "#fff8c8", "G": "#ffe890", "O": "#ffd050", "R": "#f2a828", "D": "#c07818", "M": "#7a4a0c",
             "K": "#c8a860", "S": "#e8d098", "L": "#fff4d8", "X": "#ffffff", "Z": "#f2c14e"},
    "debuff": {"W": "#f4e4ff", "Y": "#d8b4ff", "G": "#b080f0", "O": "#8a50d8", "R": "#6a30b0", "D": "#4a1a80", "M": "#2a0a4a",
               "K": "#1a0a24", "S": "#3a2048", "L": "#5a3a6a", "X": "#ff6ab0", "Z": "#120818"},
    "burst": {"W": "#ffffff", "Y": "#fff6c0", "G": "#ffe070", "O": "#ffb040", "R": "#ff7a28", "D": "#c04a18", "M": "#6a2a10",
              "K": "#3a3438", "S": "#6a6670", "L": "#9a96a0", "X": "#ffffff", "Z": "#ffe8a0"},
}
FLASH = {"fire": "#ffb060", "water": "#bfe4ff", "ice": "#e8f8ff", "wind": "#d8fff0", "light": "#fff6d0", "bolt": "#ffffff",
         "rock": "#ffe0b0", "heal": "#d8ffe4", "buff": "#fff0b0", "debuff": "#b080e0", "burst": "#fff6d0"}
RAMP = [(0.88, "W"), (0.74, "Y"), (0.6, "G"), (0.46, "O"), (0.32, "R"), (0.2, "D")]


def paint(cv, heat, mask=None, smooth=0.9, under=False):
    """熱さ（明るさ）の配列を、属性の色の段で描く。いちばん外（暗い段）は1ドットおき"""
    if smooth:
        heat = ndimage.gaussian_filter(heat, smooth)
    H, W = heat.shape
    yy, xx = np.indices((H, W))
    out = np.full((H, W), ".", dtype="<U1")
    for th, c in RAMP[::-1]:
        out[heat > th] = c
    out[(heat > 0.12) & (heat <= 0.2) & ((yy + xx) % 2 == 0)] = "M"
    m = out != "."
    if mask is not None:
        m &= mask
    if under:
        m &= cv.a == "."
    cv.a[m] = out[m]


def frame(cv, ms, el, dim=0.0, flash=0.0, shake=0):
    x, y, rows = cv.out()
    return {"ms": ms, "x": x, "y": y, "rows": rows, "dim": round(dim, 2), "flash": round(flash, 2), "shake": shake, "flash_color": FLASH[el]}


def puff(cv, cy, cx, r, k, chars="KSL"):
    """網目のけむり・霧（大きくなるほど、うすい色）"""
    col = chars[0] if r < 4 else (chars[1] if r < 6.5 else chars[2])
    for y in range(int(cy - r), int(cy + r) + 1):
        for x in range(int(cx - r), int(cx + r) + 1):
            if (y - cy) ** 2 + (x - cx) ** 2 <= r * r and (y + x + k) % 2 == 0:
                cv.put(y, x, col, over=False)


class Smoke:
    def __init__(self):
        self.p = []

    def add(self, y, x, r, rise=1.6, grow=0.55):
        self.p.append([y, x, r, rise, grow])

    def step(self, cv, k, chars="KSL"):
        for s in self.p:
            if s[2] > 11:
                continue
            puff(cv, s[0], s[1], s[2], k, chars)
            s[0] -= s[3]; s[2] += s[4]


class Bits:
    """飛び散るもの（火花・しずく・破片・葉）。重さで落ち、だんだん色が暗くなって消える"""

    def __init__(self):
        self.p = []

    def burst(self, rnd, cy, cx, n, speed=(1.4, 3.6), up=True, life=(4, 9), grav=0.5, size=1):
        for _ in range(n):
            a = rnd.uniform(math.pi * 1.05, math.pi * 1.95) if up else rnd.uniform(0, 2 * math.pi)
            v = rnd.uniform(*speed)
            self.p.append([cy, cx, math.sin(a) * v, math.cos(a) * v, rnd.randint(*life), grav, size])

    def step(self, cv, cols="WGOR", ground=None):
        for q in self.p:
            if q[4] <= 0:
                continue
            col = cols[0] if q[4] > 6 else (cols[1] if q[4] > 4 else (cols[2] if q[4] > 2 else cols[3]))
            for dy in range(q[6]):
                for dx in range(q[6]):
                    cv.put(q[0] + dy, q[1] + dx, col)
            if q[4] > 3:
                cv.put(q[0] - q[2] * 0.5, q[1] - q[3] * 0.5, cols[1])
            q[0] += q[2]; q[1] += q[3]; q[2] += q[5]
            if ground is not None and q[0] > ground:
                q[0] = ground; q[2] = -q[2] * 0.3; q[3] *= 0.6
            q[4] -= 1


def ellipse_ring(cv, cy, cx, rx, ry, col, dither=False, k=0, over=False, gap=None):
    n = int(2 * math.pi * max(rx, ry)) * 2 + 8
    for q in range(n):
        a = 2 * math.pi * q / n
        y, x = cy + math.sin(a) * ry, cx + math.cos(a) * rx
        if dither and (int(round(y)) + int(round(x)) + k) % 2:
            continue
        if gap and gap(a):
            continue
        cv.put(y, x, col, over=over)


def blob_heat(H, W, cy, cx, r, rnd, burn=0.0, sq=1.15, rough=0.55):
    """ふくらむ玉の明るさ（まん中から燃えつきて輪になる: burn）"""
    yy, xx = np.indices((H, W))
    d = np.hypot((yy - cy) * sq, xx - cx)
    nz = noise(rnd, H, W, 4)
    h = (1 - d / max(r, 0.5)) * 1.25 + (nz - 0.5) * rough
    h = h - np.clip(burn * 1.1 - d / max(r, 0.5), 0, 1) * 1.4
    return np.clip(h, 0, 1)


def spikes(cv, base_y, cx, w, h, lean=0.0, light="Y", mid="G", dark="O", edge="D", tip="W", facet=True, rough=None):
    """とがった柱（氷・岩）: 左の面が明るく、右の面が暗い。ふちは暗い色、芯に光る線"""
    if h < 1:
        return
    for y in range(int(h) + 1):
        q = y / max(1, h)
        half = w * (1 - q)
        if rough is not None:
            half += (math.sin(y * 0.9 + cx) + math.sin(y * 0.37 + cx * 2)) * 0.9
        xc = cx + lean * y
        x0, x1 = int(round(xc - half)), int(round(xc + half))
        for x in range(x0, x1 + 1):
            if x in (x0, x1) or y == 0:
                c = edge
            elif facet and x < xc - half * 0.25:
                c = light
            elif facet and x <= xc + half * 0.2:
                c = mid
            else:
                c = dark
            cv.put(base_y - y, x, c)
        if 0.15 < q < 0.8 and facet and (rough is None or y % 4 < 2):
            cv.put(base_y - y, int(round(xc - half * 0.55)), tip)


def star(cv, cy, cx, r, core="W", mid="Y", tip="G", rays=4, rot=0.0):
    for i in range(rays):
        a = rot + 2 * math.pi * i / rays
        for t in range(int(r) + 1):
            col = core if t < r * 0.35 else (mid if t < r * 0.7 else tip)
            cv.put(cy + math.sin(a) * t, cx + math.cos(a) * t, col)
    cv.put(cy, cx, core)


# ================================================================ 当たる（1人）
HW, HH, HAX, HAY = 120, 128, 60, 116   # キャンバスと、足もと（anchor）。体のまん中は足もとの32ドット上（64ドットの敵）
BODY = 32


def hit_explosion(el, rnd, rise="flame"):
    """炎型（炎・回復・強化）: とがった光 → ふくらむ玉 → まん中から燃えつきて輪 → 体の上に炎が立ちのぼる → けむり"""
    W, H, ax, ay = HW, HH, HAX, HAY
    ty = ay - BODY
    yy, xx = np.indices((H, W))
    col = FireField(H, W, rnd, decay=0.975, cool=0.012)
    gnd = FireField(H, W, rnd, decay=0.9, cool=0.045)
    ground = (np.abs(yy - ay) < 3) & (np.abs(xx - ax) < 32)
    bits = Bits(); bits.burst(rnd, ty, ax, 36)
    smoke = Smoke()
    R = [14, 24, 31, 35, 36, 35, 33, 30, 27, 24, 21, 18, 15, 12, 9, 6, 4, 2]
    frames = []
    for k, rr in enumerate(R):
        cv = Canvas(W, H)
        heat = blob_heat(H, W, ty, ax, rr, rnd, burn=min(1.0, k / 6)) * (1 - max(0, k - 2) / 14)
        for (ox, oy, k0) in ((-22, 6, 2), (20, -14, 3), (4, 16, 5)):
            kk = k - k0
            if 0 <= kk < 7:
                r2 = [7, 13, 17, 18, 16, 13, 9][kk]
                heat = np.maximum(heat, blob_heat(H, W, ty + oy, ax + ox, r2, rnd, burn=kk / 4))
        if 2 <= k <= 9:
            col.step(np.hypot(yy - (ty - 4), (xx - ax) * 0.8) < 9, 1.0, sub=7)
        else:
            col.step(None, sub=7)
        heat = np.maximum(heat, col.heat)
        gsrc = ground & (noise(rnd, H, W, 3) > 0.5) & (np.abs(xx - ax) < 32 - k)
        heat = np.maximum(heat, gnd.step(gsrc if k < 9 else None, 0.95, sub=6) * (1 - max(0, k - 7) / 6))
        if 2 <= k <= 7:
            for _ in range(2):
                smoke.add(ty - rnd.uniform(0, 10), ax + rnd.uniform(-16, 16), rnd.uniform(2, 4))
        smoke.step(cv, k)
        paint(cv, heat)
        if k <= 3:
            for q in range(12):
                a = q * math.pi / 6 + rnd.uniform(-0.2, 0.2); L = rr * (1.6 if q % 2 == 0 else 1.0)
                for s_ in range(int(L)):
                    cv.put(ty + math.sin(a) * s_, ax + math.cos(a) * s_, "W" if s_ < L * 0.3 else ("Y" if s_ < L * 0.6 else "O"), over=False)
        bits.step(cv, "WGOR", ground=ay)
        if k >= 3:
            for x in range(ax - 14, ax + 15):
                if (x + k) % 2 == 0 or abs(x - ax) < 8:
                    cv.put(ay + 1, x, "Z" if el == "fire" else "D", over=False)
        flash = {0: 0.4, 1: 0.16}.get(k, 0.0)
        shake = {0: 6, 1: 5, 2: 4, 3: 3, 4: 2, 5: 1}.get(k, 0)
        frames.append(frame(cv, 55 if k < 4 else 70, el, dim=0.45 - 0.02 * k, flash=flash, shake=shake))
    return frames


def hit_water(rnd):
    """水: しぶきがはじけ → 足もとから水柱が噴きあがり（てっぺんで王冠のしぶき）→ くずれて雨のように落ちる → 波紋と霧"""
    el = "water"
    W, H, ax, ay = HW, HH, HAX, HAY
    ty = ay - BODY
    yy, xx = np.indices((H, W))
    geyser = FireField(H, W, rnd, decay=0.995, cool=0.003)
    drops = Bits()
    mist = Smoke()
    frames = []
    N = 20
    for k in range(N):
        cv = Canvas(W, H)
        # 1. はじけるしぶき（青い玉が、まん中から輪になって散る）
        heat = np.zeros((H, W))
        if k < 6:
            heat = blob_heat(H, W, ty, ax, [10, 20, 27, 30, 30, 28][k], rnd, burn=k / 4, rough=0.7)
        # 2. 水柱（足もとから）
        src = (np.abs(yy - ay) <= 2) & (np.abs(xx - ax) <= 11) & (noise(rnd, H, W, 2) > 0.3) if 2 <= k <= 11 else None
        geyser.step(src, 1.0, sub=14 if k < 8 else 10)
        if k > 11:
            geyser.heat *= 0.72
            geyser.heat = np.roll(geyser.heat, 4, axis=0)   # くずれて下へ落ちる
            geyser.heat[: 4] = 0
        g = geyser.heat.copy()
        for y in range(H):                     # 上ほど細く・左右にうねる
            q = max(0.0, (ay - y) / 90)
            sh = int(round(math.sin(y * 0.11 + k * 0.8) * 3 * q))
            row = np.roll(g[y], sh)
            if q > 0:
                row = row * np.clip(1 - (np.abs(np.arange(W) - ax - sh) / (12 - 5 * min(1, q))) ** 4 * 0.6, 0, 1)
            g[y] = row
        heat = np.maximum(heat, g)
        paint(cv, heat, smooth=1.1)
        # 白い泡のすじ（水柱の中を上へ）
        if 2 <= k <= 11:
            top = int(np.argmax(geyser.heat[:, ax] > 0.3)) if (geyser.heat[:, ax] > 0.3).any() else ay
            for _ in range(10):
                y = rnd.randint(top, ay); x = ax + rnd.randint(-6, 6)
                cv.put(y, x, "W"); cv.put(y + 1, x, "Y")
            if k in (6, 8, 10):          # てっぺんの王冠のしぶき
                drops.burst(rnd, top + 2, ax, 22, speed=(1.6, 4.2), life=(7, 12), grav=0.55, size=2)
        if k in (1, 3):
            drops.burst(rnd, ty, ax, 18, speed=(1.4, 3.8), life=(5, 9), grav=0.5)
        drops.step(cv, "WYGO", ground=ay)
        # 3. 足もとの波紋
        for j, k0 in enumerate((3, 7, 11, 15)):
            u = k - k0
            if 0 <= u < 8:
                ellipse_ring(cv, ay, ax, 10 + u * 6, 3 + u * 1.6, "G" if u < 3 else ("O" if u < 6 else "R"), dither=u > 4, k=k)
        if k >= 9:
            for _ in range(2):
                mist.add(ay - rnd.uniform(4, 30), ax + rnd.uniform(-22, 22), rnd.uniform(2, 3.5), rise=1.0)
        mist.step(cv, k, "LLS")
        flash = {2: 0.3, 3: 0.12}.get(k, 0.0)
        shake = {2: 5, 3: 4, 4: 3, 5: 2, 6: 1}.get(k, 0)
        frames.append(frame(cv, 60 if k < 12 else 75, el, dim=0.42 - 0.015 * k, flash=flash, shake=shake))
    return frames


def hit_ice(rnd, many=1):
    """氷: 足もとが凍る（霜の輪）→ 氷の柱が次々に突き出す → きらめく → くだけて破片が飛び散る → 霜の霧"""
    el = "ice"
    W, H, ax, ay = HW, HH, HAX, HAY
    shards = Bits()
    mist = Smoke()
    n_sp = 7 if many == 1 else 9
    sp = []
    for i in range(n_sp):
        off = (i - (n_sp - 1) / 2) * (9 if many == 1 else 11) + rnd.uniform(-2, 2)
        mid = abs(off) < 6
        sp.append({"x": ax + off, "h": (70 if mid else rnd.uniform(28, 52)) * (1.15 if many > 1 else 1), "w": 9 if mid else rnd.uniform(5, 7.5),
                   "lean": -off * 0.012 + rnd.uniform(-0.05, 0.05), "start": 2 + abs(i - n_sp // 2) // 1})
    frames = []
    N = 20
    BREAK = 13
    for k in range(N):
        cv = Canvas(W, H)
        # 霜の輪（足もとが凍っていく）
        R = min(44, 8 + k * 7)
        if k < BREAK + 3:
            ellipse_ring(cv, ay, ax, R, R * 0.28, "O", dither=False)
            ellipse_ring(cv, ay, ax, R * 0.75, R * 0.75 * 0.28, "G", dither=True, k=k)
            for q in range(10):
                a = 2 * math.pi * q / 10 + 0.3
                x0, y0 = ax + math.cos(a) * R * 0.5, ay + math.sin(a) * R * 0.14
                for s in range(int(R * 0.45)):
                    cv.put(y0 + math.sin(a) * s * 0.28, x0 + math.cos(a) * s, "Y" if s % 3 else "W", over=False)
        if k < BREAK:
            for s in sp:
                g = min(1.0, max(0.0, (k - s["start"]) / 3))
                if g <= 0:
                    continue
                hh = s["h"] * (1 - (1 - g) ** 2)
                spikes(cv, ay, s["x"], s["w"], hh, lean=s["lean"])
            # きらめき（とがった先で、回る十字の光）
            if k >= 6:
                for j, s in enumerate(sp):
                    if (j + k) % 3 == 0:
                        star(cv, ay - s["h"] * 0.9, s["x"] + s["lean"] * s["h"] * 0.9, 4 + (k % 2) * 2, rays=4, rot=(k % 2) * math.pi / 4)
        elif k == BREAK:
            # くだける瞬間: 柱がひびだらけで白く光る
            for s in sp:
                spikes(cv, ay, s["x"], s["w"], s["h"], lean=s["lean"], light="W", mid="Y", dark="G", edge="O")
                for _ in range(int(s["h"] / 4)):
                    y = ay - rnd.uniform(0, s["h"]); cv.put(y, s["x"] + rnd.uniform(-s["w"] * 0.6, s["w"] * 0.6), "R")
            for s in sp:
                for _ in range(int(s["h"] / 3)):
                    y = ay - rnd.uniform(0, s["h"])
                    shards.burst(rnd, y, s["x"], 1, speed=(1.8, 4.6), up=False, life=(6, 10), grav=0.35, size=2)
        if k >= BREAK - 1:
            for _ in range(2):
                mist.add(ay - rnd.uniform(4, 40), ax + rnd.uniform(-26, 26), rnd.uniform(2, 3.5), rise=0.8)
        shards.step(cv, "WYGO", ground=ay)
        mist.step(cv, k, "LLS")
        flash = {3: 0.25, BREAK: 0.35}.get(k, 0.0)
        shake = {3: 3, 4: 2, BREAK: 6, BREAK + 1: 4, BREAK + 2: 2}.get(k, 0)
        frames.append(frame(cv, 60 if k < BREAK else 70, el, dim=0.45 - 0.012 * k, flash=flash, shake=shake))
    return frames


def hit_wind(rnd, big=1.0):
    """風: 足もとで砂が舞い → ろうと形の竜巻が立ち、しま模様の風がうずまく（葉や砂が巻きあがる）→ ほどけて消える"""
    el = "wind"
    W, H, ax, ay = HW, HH, HAX, HAY
    yy, xx = np.indices((H, W))
    debris = []
    for _ in range(26):
        debris.append([rnd.uniform(0, 2 * math.pi), rnd.uniform(0, 1), rnd.choice("XZXL"), rnd.uniform(0.25, 0.45)])
    dust = Smoke()
    frames = []
    N = 20
    for k in range(N):
        cv = Canvas(W, H)
        grow = min(1.0, k / 5) * (1 - max(0, k - 15) / 5)
        TH = 104 * big * grow
        if TH > 4:
            top = ay - TH
            q = np.clip((ay - yy) / TH, 0, 1)
            sway = np.sin((ay - yy) * 0.07 + k * 0.9) * 6 * q
            half = (5 + q * 26 * big) * (0.9 + 0.1 * np.sin(k * 1.3))
            dx = xx - ax - sway
            inside = (yy <= ay) & (yy >= top) & (np.abs(dx) <= half)
            # しま模様: 高さと横の位置で、回る帯（コマごとに進む）
            phase = (dx / np.maximum(half, 1)) * 2.2 + (ay - yy) * 0.16 - k * 1.25
            band = np.sin(phase * math.pi)
            heat = np.where(inside, 0.45 + 0.5 * band - np.abs(dx / np.maximum(half, 1)) ** 4 * 0.35, 0)
            heat = heat * (0.7 + 0.3 * noise(rnd, H, W, 3))
            if k > 15:
                heat = heat * (noise(rnd, H, W, 2) > (k - 15) / 5)
            paint(cv, np.clip(heat, 0, 1), smooth=0.6)
            # 巻きあがる葉・砂（竜巻のまわりを回りながらのぼる）
            for d in debris:
                d[0] += 0.7; d[1] = (d[1] + 0.06) % 1
                y = ay - d[1] * TH
                hq = d[1]
                x = ax + math.sin(y * 0.07 + k * 0.9) * 6 * hq + math.cos(d[0]) * (6 + hq * 28 * big)
                if math.sin(d[0]) > -0.2:
                    cv.put(y, x, d[2]); cv.put(y, x + 1, d[2])
        # 足もとの砂けむり
        if k < 17:
            for _ in range(2):
                dust.add(ay - rnd.uniform(0, 6), ax + rnd.choice((-1, 1)) * rnd.uniform(14, 34), rnd.uniform(2, 3), rise=0.5, grow=0.45)
        dust.step(cv, k, "KSL")
        # 風の切りつけ（白い弧）
        if 3 <= k <= 13 and k % 2 == 1:
            for j in range(3):
                yc = ay - 20 - j * 22 - rnd.uniform(0, 8)
                for s in range(-16, 17):
                    cv.put(yc - abs(s) * 0.35, ax + s * (1.5 if j % 2 else -1.5), "W" if abs(s) < 6 else "Y")
        flash = {4: 0.22}.get(k, 0.0)
        shake = {4: 3, 5: 3, 6: 2, 8: 2, 10: 2, 12: 1}.get(k, 0)
        frames.append(frame(cv, 60, el, dim=0.4 - 0.01 * k, flash=flash, shake=shake))
    return frames


def hit_light(rnd, wide=1.0):
    """光: 天から細い光が降り → 太い光の柱がそそぎ（中を光の粒が下る）→ 体の上で十字の光がかがやく → 光の羽がまう → 消える"""
    el = "light"
    W, H, ax, ay = HW, HH, HAX, HAY
    ty = ay - BODY
    yy, xx = np.indices((H, W))
    beam = FireField(H, W, rnd, decay=0.997, cool=0.0015)
    feathers = []
    rings = []
    frames = []
    N = 20
    for k in range(N):
        cv = Canvas(W, H)
        # 光の柱は「下へ流れる」: 上下を逆にした格子を、上のふちから流す
        half = (2 + 12 * wide * min(1.0, max(0, k - 1) / 3)) if k < 14 else 14 * wide * (1 - (k - 13) / 7)
        src = (yy >= H - 3) & (np.abs(xx - ax) <= max(1, half)) if k < 15 else None
        beam.step(src, 1.0, sub=40)
        h = beam.heat[::-1]
        reach = min(1.0, (k + 1) / 3)
        h = h * (yy <= ay * reach + 2)
        paint(cv, h, smooth=0.8)
        if 2 <= k < 15:
            # 足もとの光の円と、降りる光の粒
            ellipse_ring(cv, ay, ax, 20 + (k % 3) * 3, 6, "Y")
            ellipse_ring(cv, ay, ax, 28 + (k % 3) * 3, 8, "O", dither=True, k=k)
            for _ in range(8):
                cv.put(rnd.uniform(0, ay), ax + rnd.uniform(-half, half), "W")
        if k == 4 or k == 9:
            rings.append([0])
        for r in rings:
            u = r[0]
            if u < 7:
                ellipse_ring(cv, ty, ax, 8 + u * 9, 8 + u * 9, "Y" if u < 3 else "O", dither=u > 3, k=k)
            r[0] += 1
        # 十字の光（体のまん中で、のびて縮む）
        if 4 <= k < 14:
            L = [18, 34, 46, 50, 46, 40, 34, 28, 20, 12][k - 4] * wide
            star(cv, ty, ax, L, core="W", mid="Y", tip="O", rays=4)
            star(cv, ty, ax, L * 0.45, core="W", mid="Y", tip="G", rays=4, rot=math.pi / 4)
        # 光の羽（ゆらゆら落ちる）
        if 5 <= k <= 12:
            for _ in range(2):
                feathers.append([rnd.uniform(-10, 30), ax + rnd.uniform(-40, 40), rnd.uniform(0, 6)])
        for f in feathers:
            y, x = f[0], f[1] + math.sin(f[2]) * 3
            cv.put(y, x, "W"); cv.put(y + 1, x - 1, "Y"); cv.put(y + 1, x + 1, "Y"); cv.put(y + 2, x, "G")
            f[0] += 3.2; f[2] += 0.7
        flash = {4: 0.38, 5: 0.15}.get(k, 0.0)
        shake = {4: 4, 5: 3, 6: 2}.get(k, 0)
        frames.append(frame(cv, 60 if k < 14 else 75, el, dim=0.5 - 0.02 * k, flash=flash, shake=shake))
    return frames


def hit_bolt(rnd, strikes=1):
    """雷: 細い先がけ → 太い稲妻が落ちる（光る・揺れる）→ 一瞬消える → もう一度光る → 火花・焦げ・煙"""
    el = "bolt"
    W, H, ax, ay = HW, HH, HAX, HAY
    sparks = Bits()
    smoke = Smoke()
    frames = []
    xs = [ax] if strikes == 1 else [ax - 22, ax + 20, ax]
    order = list(range(len(xs)))
    plan = {0: "lead", 1: "main", 2: "main", 3: "off", 4: "main", 5: "fade"}
    N = 16 if strikes == 1 else 20
    for k in range(N):
        cv = Canvas(W, H)
        for j in order:
            kk = k - j * 3
            st = plan.get(kk)
            x = xs[j]
            if st in ("lead", "main", "fade"):
                pts = zigzag(rnd, 0, x + rnd.uniform(-10, 10), ay, x, step=(6, 12), wob=(3, 8))
                if st == "lead":
                    pts = pts[: max(2, len(pts) // 2)]
                core = path_mask(pts, H, W)
                for b in branches(rnd, pts, 3 if st == "main" else 1, H, W):
                    core |= path_mask(b, H, W)
                draw_glow(cv, core, width=3 if st == "main" else 1, halo=2, core_c="W", rim_c="Y", glow_c="R", halo_c="D")
                if st == "main":
                    sparks.burst(rnd, ay - 2, x, 14, speed=(1.6, 4.0), life=(4, 8))
                    # 足もとの光の輪
                    ellipse_ring(cv, ay, x, 18, 5, "Y")
                    ellipse_ring(cv, ay, x, 26, 7, "R", dither=True, k=k)
            if kk >= 5:
                for xx_ in range(x - 10, x + 11):
                    if (xx_ + k) % 2 == 0 or abs(xx_ - x) < 5:
                        cv.put(ay + 1, xx_, "M", over=False)
                if kk in (5, 7, 9):
                    smoke.add(ay - 6, x + rnd.uniform(-6, 6), 2.5, rise=1.6)
        sparks.step(cv, "WGOR", ground=ay)
        smoke.step(cv, k, "KSL")
        main_now = any(plan.get(k - j * 3) == "main" for j in order)
        first = k == 1
        flash = 0.42 if first else (0.18 if main_now else 0.0)
        shake = 6 if first else (4 if main_now else 0)
        frames.append(frame(cv, 55 if k < 8 else 70, el, dim=0.55 if k < N - 4 else 0.55 - 0.12 * (k - N + 4), flash=flash, shake=shake))
    return frames


def hit_rock(rnd, many=1):
    """岩: 上から大岩が落ちてくる → 当たってくだける（とがった光・土けむり）→ 地面が割れて岩のとげが突き出す → 土けむりになって消える"""
    el = "rock"
    W, H, ax, ay = HW, HH, HAX, HAY
    ty = ay - BODY
    chunks = Bits()
    dust = Smoke()
    sp = []
    n_sp = 4 if many == 1 else 6
    for i in range(n_sp):
        off = (i - (n_sp - 1) / 2) * 15 + rnd.uniform(-2, 2)
        sp.append({"x": ax + off, "h": rnd.uniform(34, 52) * (1.25 if abs(off) < 10 else 1), "w": rnd.uniform(8, 11), "lean": off * 0.014})
    frames = []
    N = 20
    for k in range(N):
        cv = Canvas(W, H)
        # 大岩（0〜3コマ: 落ちてくる）
        if k < 4:
            R = 20
            by = R - 4 + (ty - R + 4) * ((k + 1) / 4) ** 2
            for y in range(int(by - R), int(by + R) + 1):
                for x in range(ax - R - 2, ax + R + 3):
                    d = math.hypot((y - by) * 1.1, x - ax) + (rnd.random() - 0.5) * 1.5
                    if d > R:
                        continue
                    lit = (x - ax) + (y - by) * 1.2
                    c = "D" if d > R - 1.5 else ("Y" if lit < -10 else ("G" if lit < -2 else ("O" if lit < 8 else "R")))
                    cv.put(y, x, c)
            for j in range(4):   # 落ちる線
                cv.put(by - R - 3 - j * 3, ax + (j - 1.5) * 8, "L")
        if k == 4:
            chunks.burst(rnd, ty, ax, 30, speed=(1.8, 4.8), life=(6, 11), grav=0.55, size=2)
            for q in range(12):
                a = q * math.pi / 6; L = 30 if q % 2 == 0 else 18
                for s in range(L):
                    cv.put(ty + math.sin(a) * s, ax + math.cos(a) * s, "W" if s < 8 else ("Y" if s < 16 else "G"))
        # 地面のひび → とげ
        if 4 <= k < 17:
            for q in range(7):
                a = math.pi * (0.08 + 0.84 * q / 6)
                L = min(46, (k - 3) * 10)
                for s in range(int(L)):
                    if s % 5 != 4:
                        cv.put(ay + math.sin(a) * s * 0.18, ax + math.cos(a) * s, "M", over=False)
            g = min(1.0, (k - 5) / 3) if k >= 5 else 0
            fall = max(0.0, (k - 13) / 4)
            for s in sp:
                hh = s["h"] * (1 - (1 - g) ** 2) * (1 - fall)
                if hh > 1:
                    spikes(cv, ay, s["x"], s["w"], hh, lean=s["lean"], light="Y", mid="O", dark="R", edge="M", tip="W", rough=rnd)
        if 4 <= k <= 15:
            for _ in range(2 if k < 8 else 1):
                dust.add(ay - rnd.uniform(0, 14), ax + rnd.uniform(-34, 34), rnd.uniform(2.5, 4), rise=0.9, grow=0.6)
        chunks.step(cv, "YGOD", ground=ay)
        dust.step(cv, k, "KSL")
        flash = {4: 0.32}.get(k, 0.0)
        shake = {4: 7, 5: 6, 6: 4, 7: 3, 8: 2, 9: 1}.get(k, 0)
        frames.append(frame(cv, 55 if k < 8 else 70, el, dim=0.42 - 0.012 * k, flash=flash, shake=shake))
    return frames


def hit_aura(el, rnd):
    """回復・強化・弱体: 体を包むオーラ。回復＝緑の光がのぼり十字の光が舞う、強化＝金の炎がのぼり上向きの矢じるし、
    弱体＝紫の闇が上からのしかかり、輪がしめつける"""
    W, H, ax, ay = HW, HH, HAX, HAY
    ty = ay - BODY
    yy, xx = np.indices((H, W))
    down = el == "debuff"
    f = FireField(H, W, rnd, decay=0.978 if el != "debuff" else 0.965, cool=0.011 if el != "debuff" else 0.018)
    parts = []
    rings = []
    frames = []
    N = 18
    for k in range(N):
        cv = Canvas(W, H)
        on = k < 12
        if down:
            # 上下を逆にした格子で、頭の上から下へ流れる闇
            src = (yy >= H - (ay - BODY * 2) - 2) & (yy <= H - (ay - BODY * 2) + 2) & (np.abs(xx - ax) <= 20) & (noise(rnd, H, W, 2) > 0.4)
            f.step(src if on else None, 1.0, sub=8)
            heat = f.heat[::-1] * ((yy <= ay + 2))
        else:
            ringm = np.abs(np.hypot((xx - ax) / 17, (yy - ay) / 5) - 1) < 0.35
            src = ringm & (noise(rnd, H, W, 2) > 0.42)
            f.step(src if on else None, 1.0, sub=9)
            heat = f.heat
        paint(cv, heat, smooth=0.8)
        # 足もとの輪（ひろがる）
        if k % 4 == 0 and k < 13:
            rings.append([0])
        for r in rings:
            u = r[0]
            if u < 6:
                ellipse_ring(cv, ay if not down else ty, ax, 10 + u * 6, (3 + u * 1.6) if not down else (6 + u * 2), "Y" if u < 3 else "O", dither=u > 3, k=k)
            r[0] += 1
        # 舞うもの
        if k < 13:
            for _ in range(3):
                if down:
                    parts.append([ay - BODY * 2 - rnd.uniform(0, 10), ax + rnd.uniform(-26, 26), 2.6, rnd.randint(7, 11)])
                else:
                    parts.append([ay - rnd.uniform(0, 8), ax + rnd.uniform(-28, 28), -2.8, rnd.randint(7, 12)])
        for p_ in parts:
            if p_[3] <= 0:
                continue
            y, x = p_[0], p_[1]
            if el == "heal":   # 十字の光
                cv.put(y, x, "W"); cv.put(y - 1, x, "Y"); cv.put(y + 1, x, "Y"); cv.put(y, x - 1, "Y"); cv.put(y, x + 1, "Y")
                if p_[3] > 8:
                    cv.put(y - 2, x, "G"); cv.put(y + 2, x, "G"); cv.put(y, x - 2, "G"); cv.put(y, x + 2, "G")
            elif el == "buff":  # 上向きの矢じるし
                for s in range(4):
                    cv.put(y + s, x - s, "W" if s == 0 else "Y"); cv.put(y + s, x + s, "W" if s == 0 else "Y")
            else:  # 闇のかけら
                cv.put(y, x, "X" if p_[3] > 8 else "G"); cv.put(y + 1, x, "O"); cv.put(y - 1, x, "R")
            p_[0] += p_[2]; p_[3] -= 1
        if down and 3 <= k <= 13:
            # 体をしめつける輪（くさりのように、輪が3本、すこしずつ縮む）
            for j in range(3):
                rr = 30 - min(12, (k - 3) * 1.5)
                ellipse_ring(cv, ty - 14 + j * 14, ax, rr, rr * 0.3, "W" if (k + j) % 3 == 0 else "Y", gap=lambda a: int(a * 6) % 3 == 0)
        if el == "heal" and k in (10, 11):
            star(cv, ty, ax, 22 if k == 10 else 14, core="W", mid="Y", tip="G", rays=8)
        if el == "buff" and k in (9, 10):
            star(cv, ty - 10, ax, 26 if k == 9 else 16, core="W", mid="Y", tip="O", rays=8)
        flash = {0: 0.14} .get(k, 0.0)
        frames.append(frame(cv, 70, el, dim=0.3 - 0.015 * k, flash=flash, shake=1 if (down and k == 3) else 0))
    return frames


def hit_burst(rnd):
    """爆発（体の技）: とがった星形の光 → 輪がひろがる → 火花"""
    el = "burst"
    W, H, ax, ay = HW, HH, HAX, HAY
    ty = ay - BODY
    sparks = Bits(); sparks.burst(rnd, ty, ax, 30, speed=(2.0, 4.6), up=False, life=(4, 8), grav=0.3)
    frames = []
    for k in range(12):
        cv = Canvas(W, H)
        if k < 6:
            heat = blob_heat(H, W, ty, ax, [10, 18, 22, 22, 18, 12][k], rnd, burn=k / 3)
            paint(cv, heat)
            L = [26, 40, 46, 40, 28, 14][k]
            star(cv, ty, ax, L, rays=8, rot=0.2 + k * 0.05, core="W", mid="Y", tip="O")
        if 1 <= k < 9:
            u = k - 1
            ellipse_ring(cv, ty, ax, 10 + u * 7, 10 + u * 7, "W" if u < 2 else ("Y" if u < 5 else "O"), dither=u > 4, k=k)
        sparks.step(cv, "WYGO")
        frames.append(frame(cv, 50, el, dim=0.2, flash={0: 0.3}.get(k, 0.0), shake={0: 5, 1: 4, 2: 2}.get(k, 0)))
    return frames


def hit_area_flame(el, rnd):
    """全体（炎型）: 足もとに予告の輪 → 太い柱が噴きあがる → 大きく燃えあがる → けむり"""
    W, H, ax, ay = HW, HH, HAX, HAY
    yy, xx = np.indices((H, W))
    col = FireField(H, W, rnd, decay=0.99, cool=0.005)
    sea = FireField(H, W, rnd, decay=0.955, cool=0.02)
    band_ = (np.abs(yy - ay) <= 3) & (np.abs(xx - ax) < 40)
    smoke = Smoke()
    bits = Bits()
    frames = []
    N = 22
    for k in range(N):
        cv = Canvas(W, H)
        if k < 3:
            rr = 12 + k * 3
            ellipse_ring(cv, ay, ax, rr, rr * 0.3, "R" if k < 2 else "O", dither=k % 2 == 1, k=k)
            cv.put(ay - rnd.randint(1, 6), ax + rnd.randint(-8, 8), "Y")
        else:
            s = k - 3
            big = 9 <= k <= 11
            on = s < 9 or big
            src = (np.abs(yy - ay) <= 2) & (np.abs(xx - ax) <= (12 if not big else 16)) if on else None
            col.step(src, 1.0, sub=14 if (s < 3 or big) else 11)
            sea.step(band_ & (noise(rnd, H, W, 4) > (0.55 if not big else 0.35)) if k < 13 else None, 0.85, sub=5)
            heat = np.maximum(col.heat, sea.heat)
            paint(cv, heat)
            if s in (0, 6):
                bits.burst(rnd, ay - 6, ax, 16)
            if k in (12, 14, 16):
                for _ in range(3):
                    smoke.add(ay - rnd.uniform(20, 80), ax + rnd.uniform(-12, 12), rnd.uniform(2.5, 4), rise=1.8)
        bits.step(cv, "WGOR", ground=ay)
        smoke.step(cv, k)
        flash = {3: 0.3, 9: 0.2}.get(k, 0.0)
        shake = {3: 5, 4: 4, 5: 2, 9: 5, 10: 3}.get(k, 0)
        frames.append(frame(cv, 60 if k < 12 else 80, el, dim=min(0.55, 0.2 + 0.06 * k) if k < N - 5 else 0.55 - 0.1 * (k - N + 5), flash=flash, shake=shake))
    return frames


# ================================================================ ため（となえる人の足もと）
CW, CH, CAX, CAY = 96, 104, 48, 92
CHAR_H = 30   # となえる人（味方）の背の高さのめやす


def make_charge(el, rnd):
    """足もとに属性の色の陣（二重の輪・回る印）。陣のふちから属性の色の光（炎は炎の舌）が立ちのぼり、
    まわりから属性のもの（火の粉・しずく・雪・風・光・稲妻・小石・葉・矢じるし・闇）が吸いこまれ、頭の上に玉がふくらむ。最後にはじける"""
    W, H, ax, ay = CW, CH, CAX, CAY
    oy = ay - CHAR_H - 12   # 玉の高さ
    yy, xx = np.indices((H, W))
    f = FireField(H, W, rnd, decay=0.9, cool=0.05)
    swirl = []
    frames = []
    N = 16
    for k in range(N):
        cv = Canvas(W, H)
        t = k / (N - 1)
        R = 34 * min(1.0, (k + 1) / 4)
        # 陣のふちから立つ光
        ring_m = np.abs(np.hypot((xx - ax) / max(R * 0.95, 1), (yy - ay) / max(R * 0.95 * 0.3, 1)) - 1) * R * 0.3 < 1.2
        f.step(ring_m & (noise(rnd, H, W, 3) > 0.45), 0.6 + 0.4 * t, sub=3 if el != "fire" else 4)
        paint(cv, f.heat * (0.8 if el not in ("fire", "buff") else 1.0))
        # 陣（輪2本と、回る印）
        ellipse_ring(cv, ay, ax, R, R * 0.3, "O", over=True)
        ellipse_ring(cv, ay, ax, R * 0.72, R * 0.72 * 0.3, "Y", dither=True, k=k, over=True)
        for q in range(6):
            a = k * 0.35 + 2 * math.pi * q / 6
            y, x = ay + math.sin(a) * R * 0.86 * 0.3, ax + math.cos(a) * R * 0.86
            cv.put(y, x, "W"); cv.put(y - 1, x, "Y"); cv.put(y + 1, x, "Y"); cv.put(y, x - 1, "G"); cv.put(y, x + 1, "G")
        # 吸いこまれるもの
        for _ in range(3):
            swirl.append([rnd.uniform(0, 2 * math.pi), rnd.uniform(30, 44)])
        for s in swirl:
            if s[1] <= 4:
                continue
            y, x = oy + math.sin(s[0]) * s[1] * 0.85, ax + math.cos(s[0]) * s[1]
            if el == "bolt":
                cv.put(y, x, "W"); cv.put(y + 1, x + 1, "Y"); cv.put(y + 2, x, "R")
            elif el == "ice":
                cv.put(y, x, "W"); cv.put(y - 1, x, "G"); cv.put(y + 1, x, "G"); cv.put(y, x - 1, "G"); cv.put(y, x + 1, "G")
            elif el == "rock":
                cv.put(y, x, "O"); cv.put(y, x + 1, "R"); cv.put(y + 1, x, "D"); cv.put(y + 1, x + 1, "D")
            elif el == "wind":
                cv.put(y, x, "W"); cv.put(y, x + 1, "Y"); cv.put(y, x + 2, "G")
            elif el in ("heal", "wind"):
                cv.put(y, x, "Z"); cv.put(y - 1, x + 1, "X")
            elif el == "debuff":
                cv.put(y, x, "G"); cv.put(y + 1, x, "R"); cv.put(y + 2, x, "D")
            else:
                cv.put(y, x, "Y" if s[1] < 18 else ("O" if s[1] < 28 else "R"))
            s[0] += 0.45; s[1] -= 3.6
        # 頭の上の玉
        r = 2 + 9 * t + (0.8 if k % 2 else 0)
        heat = blob_heat(H, W, oy, ax, r, rnd, sq=1.0, rough=0.4)
        paint(cv, heat, smooth=0.6)
        if k >= N - 3:
            # 最後: 陣から光の柱が立ち、玉がぎゅっと光る
            for q in range(8):
                a = 2 * math.pi * q / 8
                x = ax + math.cos(a) * R * 0.9; y0 = ay + math.sin(a) * R * 0.27
                for s in range(int(50 * (k - N + 4) / 3)):
                    if (s + q) % 2 == 0:
                        cv.put(y0 - s, x, "W" if s % 4 == 0 else "G")
            star(cv, oy, ax, 14 + (k - N + 3) * 6, rays=8, core="W", mid="Y", tip="O")
        frames.append(frame(cv, 70, el, dim=0.1 + 0.3 * t, flash=0.18 if k == N - 1 else 0.0))
    return frames


# ================================================================ 飛んでいく弾（左へ飛ぶ。くり返し）
BW, BH, BAX, BAY = 72, 40, 22, 20


def make_bolt(el, rnd):
    """弾の頭は左。尾は右へ流れる（炎・水は格子を横に流す、氷はつらら、岩は回る岩）"""
    W, H, ax, ay = BW, BH, BAX, BAY
    frames = []
    yy, xx = np.indices((H, W))
    if el in ("fire", "water", "light"):
        f = FireField(W, H, rnd, decay=0.93 if el == "fire" else 0.95, cool=0.03)   # 横むき（転置して使う）
        for k in range(10):
            src = np.zeros((W, H), bool)
            src[W - ax - 3: W - ax + 3, ay - 5: ay + 6] = True     # 転置した格子の下のほう＝弾の頭
            f.step(src, 1.0, sub=6)
            heat = f.heat[::-1, :].T                                  # 上へ流れる → 右へ流れる
            heat = np.maximum(heat, blob_heat(H, W, ay, ax, 9, rnd, sq=1.0, rough=0.35))
            if k < 4:
                continue    # はじめの数コマは、尾がのびるまで捨てる
            cv = Canvas(W, H)
            paint(cv, heat, smooth=0.7)
            for _ in range(6):
                cv.put(ay + rnd.uniform(-8, 8), ax + rnd.uniform(10, 50), "Y" if el != "water" else "W")
            frames.append(frame(cv, 50, el, dim=0.3))
    elif el == "ice":
        for k in range(6):
            cv = Canvas(W, H)
            for x in range(40):
                half = 7 * (x / 40) ** 0.7 if x < 30 else 7 * (1 - (x - 30) / 10)
                for y in range(int(-half), int(half) + 1):
                    c = "W" if y < -half * 0.4 else ("G" if y < half * 0.3 else "O")
                    if abs(y) >= half - 0.5:
                        c = "D"
                    cv.put(ay + y, ax - 6 + x, c)
            for j in range(10):
                x = ax + 30 + j * 3 + rnd.uniform(-1, 1)
                cv.put(ay + rnd.uniform(-6, 6), x, "Y" if j % 2 else "L")
            star(cv, ay - 2, ax - 2, 5 if k % 2 else 3, rays=4, rot=(k % 2) * math.pi / 4)
            frames.append(frame(cv, 50, el, dim=0.3))
    else:   # rock: 回る岩
        for k in range(6):
            cv = Canvas(W, H)
            R = 13
            rot = k * math.pi / 6
            for y in range(-R, R + 1):
                for x in range(-R - 1, R + 2):
                    ang = math.atan2(y, x) - rot
                    rr = R * (0.85 + 0.15 * math.cos(ang * 3))
                    d = math.hypot(y, x)
                    if d > rr:
                        continue
                    lit = x + y * 1.2
                    c = "D" if d > rr - 1.5 else ("Y" if lit < -8 else ("G" if lit < 0 else ("O" if lit < 8 else "R")))
                    if (int(x * math.cos(rot) + y * math.sin(rot)) % 7 == 0) and d < rr - 3:
                        c = "D"
                    cv.put(ay + y, ax + x, c)
            for j in range(4):
                for s in range(8):
                    if s % 2 == 0:
                        cv.put(ay - 8 + j * 5, ax + R + 4 + j * 2 + s * 2, "L")
            frames.append(frame(cv, 50, el, dim=0.3))
    return frames


# ================================================================
def build(el, seed):
    rnd = random.Random(seed * 31 + sum(map(ord, el)))
    out = {}
    pal = PALS[el]
    meta = lambda name, frames, w, h, a: {"name": name, "w": w, "h": h, "anchor": list(a), "palette": pal, "frames": frames}
    hit = {
        "fire": lambda: hit_explosion("fire", rnd),
        "water": lambda: hit_water(rnd),
        "ice": lambda: hit_ice(rnd),
        "wind": lambda: hit_wind(rnd),
        "light": lambda: hit_light(rnd),
        "bolt": lambda: hit_bolt(rnd),
        "rock": lambda: hit_rock(rnd),
        "heal": lambda: hit_aura("heal", rnd),
        "buff": lambda: hit_aura("buff", rnd),
        "debuff": lambda: hit_aura("debuff", rnd),
        "burst": lambda: hit_burst(rnd),
    }[el]()
    out["hit"] = meta(f"{el} 当たる（1人）", hit, HW, HH, (HAX, HAY))
    area = {
        "fire": lambda: hit_area_flame("fire", rnd),
        "water": lambda: hit_water(rnd),
        "ice": lambda: hit_ice(rnd, many=2),
        "wind": lambda: hit_wind(rnd, big=1.12),
        "light": lambda: hit_light(rnd, wide=1.35),
        "bolt": lambda: hit_bolt(rnd, strikes=3),
        "rock": lambda: hit_rock(rnd, many=2),
    }.get(el)
    if area:
        out["area"] = meta(f"{el} 全体（1人ずつ）", area(), HW, HH, (HAX, HAY))
    out["charge"] = meta(f"{el} ため", make_charge(el, rnd), CW, CH, (CAX, CAY))
    if el in ("fire", "water", "ice", "rock", "light"):
        out["bolt"] = meta(f"{el} 飛ぶ弾", make_bolt(el, rnd), BW, BH, (BAX, BAY))
    return out


if __name__ == "__main__":
    outdir = sys.argv[1]
    seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 7
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else list(PALS)
    for el in only:
        d = os.path.join(outdir, el)
        os.makedirs(d, exist_ok=True)
        for kind, fx in build(el, seed).items():
            json.dump(fx, open(os.path.join(d, f"{kind}.json"), "w"), ensure_ascii=False)
            print(el, kind, len(fx["frames"]), "コマ", sum(f["ms"] for f in fx["frames"]), "ミリ秒")
