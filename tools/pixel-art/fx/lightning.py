"""ボスが使う雷の術のエフェクト（ドット絵のコマ）を作る。

人間の指示「ボスが使う魔法エフェクトを作ろうか。まずは雷系」（2026-10-04）。
戦闘画面（論理 400×225、戦闘の場は上の 169）と同じ1ドットの大きさで描く。

使い方: python3 lightning.py 出力フォルダ [--seed 7] [--boss ボスのanim.json]
出力: charge.json（ため）・bolt.json（落雷・1人）・storm.json（雷の嵐・全体）・aura.json（発動・ボスのまわり。--boss ボスのanim.json のとき）
  {"name", "w", "h", "anchor": [x, y], "palette": {記号: 色}, "frames": [
     {"ms", "x", "y", "rows": [...], "dim": 0〜1（画面を暗くする強さ）, "flash": 0〜1（白く光る強さ）, "shake": ドット}]}
  rows は w×h の中で絵のある範囲だけ（x, y がその左上）。"." は透明。
  anchor は、ためでは「術をとなえる点」、落雷では「当たる人の足元のまん中」、嵐では「味方の一団のまん中」。

考え方（docs/design/battle-effects.md）:
- 光るものは、芯を白、そのまわりを薄い黄、外を水色、いちばん外を青（1ドットおきの点々）にする。明るい背景でも見えるよう、術のあいだは画面を暗くする。
- 落雷は「細い先がけの稲妻が下へ伸びる → 太い本体が落ちる（画面が白く光る・揺れる）→ 一瞬消える → もう一度光る → 火花と煙が残る」。本物の雷も何度か光りなおす。
- コマごとに稲妻の形を少し変えて、ちらつかせる（同じ形のままだと止まって見える）。
"""
import json
import math
import random
import sys

import numpy as np
from scipy import ndimage

PAL = {
    "W": "#ffffff",  # 芯
    "Y": "#fff4b0",  # 芯のまわり（薄い黄）
    "G": "#ffd75e",  # 黄（火花）
    "O": "#ff9a3c",  # 橙（地面の火花）
    "C": "#8ee6ff",  # 水色（光）
    "B": "#4d7bff",  # 青（外の光）
    "V": "#7a4fe0",  # 紫（残光）
    "D": "#2e2163",  # 暗い紫（煙・焦げ）
}
DOT = "."


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.a = np.full((h, w), DOT, dtype="<U1")

    def put(self, y, x, c, over=True):
        y, x = int(round(y)), int(round(x))
        if 0 <= y < self.h and 0 <= x < self.w and (over or self.a[y, x] == DOT):
            self.a[y, x] = c

    def mask_put(self, m, c, dither=False, under=False):
        if dither:
            yy, xx = np.indices(m.shape)
            m = m & (((yy + xx) % 2) == 0)
        if under:
            m = m & (self.a == DOT)
        self.a[m] = c

    def out(self):
        ys, xs = np.nonzero(self.a != DOT)
        if not len(ys):
            return 0, 0, ["."]
        y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
        return int(x0), int(y0), ["".join(r) for r in self.a[y0:y1 + 1, x0:x1 + 1]]


def line_pts(y0, x0, y1, x1):
    pts = []
    n = int(max(abs(y1 - y0), abs(x1 - x0))) + 1
    for i in range(n + 1):
        t = i / max(1, n)
        pts.append((int(round(y0 + (y1 - y0) * t)), int(round(x0 + (x1 - x0) * t))))
    return pts


def zigzag(rnd, y0, x0, y1, x1, step=(7, 14), wob=(3, 9)):
    """上から下へ、ぎざぎざに折れながら目標へ向かう点のならび"""
    pts = [(y0, x0)]
    y, x = y0, x0
    while y < y1 - 2:
        dy = rnd.randint(*step)
        y2 = min(y1, y + dy)
        left = (y1 - y2) / max(1, (y1 - y0))      # 残り（1→0）
        target = x1 + (x - x1) * left * 0.6       # だんだん目標へ寄せる
        x2 = target + rnd.choice((-1, 1)) * rnd.uniform(*wob) * (0.35 + left)
        pts.append((y2, x2)); y, x = y2, x2
    pts.append((y1, x1))
    return pts


def path_mask(pts, h, w):
    m = np.zeros((h, w), bool)
    for (a, b), (c, d) in zip(pts, pts[1:]):
        for y, x in line_pts(a, b, c, d):
            if 0 <= y < h and 0 <= x < w:
                m[y, x] = True
    return m


def draw_glow(cv, core, width=2, halo=2, core_c="W", rim_c="Y", glow_c="C", halo_c="B"):
    """芯（太さ width）＋薄い黄の縁＋水色の光＋青い点々の外の光"""
    k = np.ones((3, 3), bool)
    c = ndimage.binary_dilation(core, k, iterations=max(0, width - 1)) if width > 1 else core
    rim = ndimage.binary_dilation(c, k) & ~c
    glow = ndimage.binary_dilation(c, k, iterations=2) & ~c & ~rim
    hal = ndimage.binary_dilation(c, k, iterations=2 + halo) & ~c & ~rim & ~glow
    if halo_c and halo > 0:
        cv.mask_put(hal, halo_c, dither=True, under=True)
    if glow_c:
        cv.mask_put(glow, glow_c, dither=width < 2)
    if rim_c:
        cv.mask_put(rim, rim_c)
    cv.mask_put(c, core_c)


def branches(rnd, pts, n, h, w, depth_frac=0.75):
    """本体の途中から、斜め下へ伸びる細い枝"""
    out = []
    usable = [p for p in pts[1:-1] if p[0] < pts[-1][0] * depth_frac + pts[0][0] * (1 - depth_frac)] or pts[1:-1]
    for _ in range(n):
        if not usable:
            break
        y, x = rnd.choice(usable)
        side = rnd.choice((-1, 1))
        seg = [(y, x)]
        for _ in range(rnd.randint(2, 5)):
            y += rnd.randint(4, 9); x += side * rnd.randint(3, 9) + rnd.randint(-2, 2)
            seg.append((y, x))
        out.append(seg)
    return out


def starburst(cv, cy, cx, r, rays=8, rot=0.0, core="W", mid="Y", tip="C"):
    for i in range(rays):
        a = rot + 2 * math.pi * i / rays
        L = r * (1.0 if i % 2 == 0 else 0.55)
        for t in range(int(L) + 1):
            col = core if t < L * 0.35 else (mid if t < L * 0.7 else tip)
            cv.put(cy + math.sin(a) * t, cx + math.cos(a) * t, col)
    for y in range(-2, 3):
        for x in range(-2, 3):
            if y * y + x * x <= 4:
                cv.put(cy + y, cx + x, core)


def ring(cv, cy, cx, rx, ry, col, dither=False):
    for k in range(int(2 * math.pi * max(rx, ry)) * 2 + 8):
        a = 2 * math.pi * k / (int(2 * math.pi * max(rx, ry)) * 2 + 8)
        y, x = cy + math.sin(a) * ry, cx + math.cos(a) * rx
        if dither and (int(round(y)) + int(round(x))) % 2:
            continue
        cv.put(y, x, col, over=False)


def orb(cv, cy, cx, r):
    """光の玉: 外から青の点々・水色・薄い黄・白"""
    for y in range(int(cy - r - 2), int(cy + r + 3)):
        for x in range(int(cx - r - 2), int(cx + r + 3)):
            d = math.hypot(y - cy, x - cx)
            if d <= r * 0.4: cv.put(y, x, "W")
            elif d <= r * 0.7: cv.put(y, x, "Y")
            elif d <= r: cv.put(y, x, "C")
            elif d <= r + 1.6 and (y + x) % 2 == 0: cv.put(y, x, "B", over=False)


class Sparks:
    """地面に散る火花（重さで落ちて、だんだん消える）"""

    def __init__(self, rnd, cy, cx, n, ground):
        self.p = []
        for _ in range(n):
            a = rnd.uniform(math.pi * 1.05, math.pi * 1.95)   # 上向きの半円
            v = rnd.uniform(1.4, 3.6)
            self.p.append([cy, cx, math.sin(a) * v, math.cos(a) * v, rnd.randint(4, 8)])
        self.ground = ground

    def step(self, cv):
        for q in self.p:
            if q[4] <= 0:
                continue
            col = "W" if q[4] > 6 else ("G" if q[4] > 3 else "O")
            cv.put(q[0], q[1], col)
            if q[4] > 4:
                cv.put(q[0] - q[2] * 0.5, q[1] - q[3] * 0.5, "Y")   # 尾
            q[0] += q[2]; q[1] += q[3]; q[2] += 0.55
            if q[0] > self.ground:
                q[0] = self.ground; q[2] *= -0.3
            q[4] -= 1


def frame(cv, ms, dim=0.0, flash=0.0, shake=0):
    x, y, rows = cv.out()
    return {"ms": ms, "x": x, "y": y, "rows": rows, "dim": round(dim, 2), "flash": round(flash, 2), "shake": shake}


# ---------------------------------------------------------------- ため（術をとなえる）
def make_charge(seed):
    rnd = random.Random(seed)
    W = H = 96; cy, cx = 48, 48
    frames = []
    N = 14
    for i in range(N):
        cv = Canvas(W, H)
        t = i / (N - 1)
        R = 44 - 30 * t                       # 集まってくる円の半径
        # 外から中心へ走る小さな稲妻（数が増えていく）
        for _ in range(2 + int(5 * t)):
            a = rnd.uniform(0, 2 * math.pi)
            r0 = R + rnd.uniform(0, 8)
            y0, x0 = cy + math.sin(a) * r0, cx + math.cos(a) * r0
            r1 = max(4, r0 - rnd.uniform(10, 18))
            y1, x1 = cy + math.sin(a) * r1, cx + math.cos(a) * r1
            pts = [(y0, x0)]
            for k in range(1, 4):
                f = k / 4
                pts.append((y0 + (y1 - y0) * f + rnd.uniform(-3, 3), x0 + (x1 - x0) * f + rnd.uniform(-3, 3)))
            pts.append((y1, x1))
            m = path_mask([(int(round(p)), int(round(q))) for p, q in pts], H, W)
            draw_glow(cv, m, width=1, halo=0, rim_c=None, core_c="W" if rnd.random() < 0.5 else "Y", glow_c="C")
        # 光の玉（だんだん大きく、明るさが脈打つ）
        r = 2 + 6 * t + (0.8 if i % 2 else 0)
        orb(cv, cy, cx, r)
        # 点々の光の粒が、まわりから吸いこまれる
        for _ in range(10):
            a = rnd.uniform(0, 2 * math.pi); rr = rnd.uniform(r + 4, R + 10)
            cv.put(cy + math.sin(a) * rr, cx + math.cos(a) * rr, rnd.choice("CCB"))
        frames.append(frame(cv, 80 if i < N - 3 else 70, dim=0.15 + 0.35 * t))
    # 最後: 玉がはじける光
    for j, (rr, rot) in enumerate(((20, 0.0), (26, 0.39))):
        cv = Canvas(W, H)
        orb(cv, cy, cx, 9 - j * 3)
        starburst(cv, cy, cx, rr, rays=12, rot=rot)
        ring(cv, cy, cx, 14 + j * 8, 14 + j * 8, "C", dither=bool(j))
        frames.append(frame(cv, 60, dim=0.5, flash=0.35 - j * 0.2))
    return {"name": "雷のため", "w": W, "h": H, "anchor": [cx, cy], "palette": PAL, "frames": frames}


# ---------------------------------------------------------------- 落雷（1人）
def make_bolt(seed):
    rnd = random.Random(seed)
    W, H = 128, 200
    ax, ay = 64, 192                          # 当たる人の足元
    hit_y = ay - 16                           # 体のまん中あたりに落ちる
    top = 0
    frames = []
    dims = [0.25, 0.45, 0.55, 0.6]
    main = zigzag(rnd, top, ax + rnd.randint(-18, 18), hit_y, ax)
    # 1〜3: 細い先がけの稲妻が、上から下へ伸びる
    for i, reach in enumerate((0.35, 0.65, 0.9)):
        cv = Canvas(W, H)
        ycut = top + (hit_y - top) * reach
        pts = [p for p in main if p[0] <= ycut]
        if len(pts) < 2:
            pts = main[:2]
        m = path_mask([(int(p[0]), int(p[1])) for p in pts], H, W)
        draw_glow(cv, m, width=1, halo=0, core_c="Y", rim_c=None, glow_c="C")
        for br in branches(rnd, pts, 1 + i, H, W):
            draw_glow(cv, path_mask([(int(a), int(b)) for a, b in br], H, W), width=1, halo=0, core_c="C", rim_c=None, glow_c=None)
        # 足元に小さな光（ここに落ちる、という予告）
        cv.put(ay, ax, "C"); cv.put(ay, ax - 2, "B"); cv.put(ay, ax + 2, "B")
        frames.append(frame(cv, 50, dim=dims[i]))
    sparks = Sparks(rnd, ay - 2, ax, 18, ay)

    def strike(width, nbr, burst, ring_r, jitter, dim, flash, shake, ms, sp=True, smoke=0):
        cv = Canvas(W, H)
        pts = [(p[0], p[1] + (rnd.uniform(-jitter, jitter) if 0 < k < len(main) - 1 else 0)) for k, p in enumerate(main)]
        m = path_mask([(int(p[0]), int(round(p[1]))) for p in pts], H, W)
        for br in branches(rnd, pts, nbr, H, W):
            draw_glow(cv, path_mask([(int(a), int(b)) for a, b in br], H, W), width=1, halo=1, core_c="Y", rim_c=None, glow_c="C")
        # 地面に当たる所: 縦の光の柱を足元まで
        m |= path_mask([(hit_y, ax), (ay, ax)], H, W)
        draw_glow(cv, m, width=width, halo=2)
        if burst:
            starburst(cv, hit_y + 4, ax, burst, rays=10, rot=rnd.uniform(0, 0.6))
        if ring_r:
            ring(cv, ay, ax, ring_r, ring_r / 3.2, "C")
            ring(cv, ay, ax, ring_r + 3, (ring_r + 3) / 3.2, "B", dither=True)
        if sp:
            sparks.step(cv)
        return frame(cv, ms, dim=dim, flash=flash, shake=shake)

    frames.append(strike(3, 4, 16, 8, 1.0, 0.65, 0.45, 4, 60))     # 本体が落ちる（いちばん明るい）
    frames.append(strike(3, 3, 12, 13, 2.0, 0.65, 0.2, 3, 60))
    # 一瞬消える（残光だけ）
    cv = Canvas(W, H)
    m = path_mask([(int(p[0]), int(p[1])) for p in main], H, W)
    cv.mask_put(ndimage.binary_dilation(m), "V", dither=True)
    ring(cv, ay, ax, 18, 18 / 3.2, "B", dither=True)
    sparks.step(cv)
    frames.append(frame(cv, 40, dim=0.6, shake=2))
    # もう一度光る（少し形が違う）
    frames.append(strike(2, 3, 14, 20, 3.0, 0.6, 0.3, 3, 60))
    frames.append(strike(2, 2, 8, 24, 3.5, 0.55, 0.08, 1, 70))
    frames.append(strike(1, 1, 0, 0, 4.0, 0.5, 0.0, 0, 70))
    # 消えていく: 焦げと煙、火花
    smoke = [[ay - rnd.uniform(2, 6), ax + rnd.uniform(-8, 8), rnd.uniform(1.5, 3)] for _ in range(7)]
    for i in range(5):
        cv = Canvas(W, H)
        if i < 2:
            m = path_mask([(int(p[0]), int(p[1])) for p in main], H, W)
            cv.mask_put(m & (np.indices(m.shape)[0] % (2 + i) == 0), "V")
        for s in smoke:
            r = s[2] + i * 0.9
            for y in range(int(s[0] - r), int(s[0] + r) + 1):
                for x in range(int(s[1] - r), int(s[1] + r) + 1):
                    if (y - s[0]) ** 2 + (x - s[1]) ** 2 <= r * r and (y + x + i) % (2 if i < 3 else 3) == 0:
                        cv.put(y, x, "D", over=False)
            s[0] -= 1.6; s[1] += rnd.uniform(-0.8, 0.8)
        for x in range(ax - 7, ax + 8):          # 地面の焦げあと
            if (x + i) % 2 == 0 or abs(x - ax) < 4:
                cv.put(ay + 1, x, "D")
        sparks.step(cv)
        frames.append(frame(cv, 80 + 10 * i, dim=max(0, 0.45 - 0.12 * i)))
    return {"name": "落雷（1人）", "w": W, "h": H, "anchor": [ax, ay], "palette": PAL, "frames": frames}


# ---------------------------------------------------------------- 雷の嵐（全体）
def make_storm(seed, targets=((22, 5), (8, -13), (-8, 5), (-22, -13))):
    """targets: 一団のまん中から見た、味方の足元の位置（x, y）。ほかに地面へも落ちる"""
    rnd = random.Random(seed)
    W, H = 200, 200
    ax, ay = 100, 180
    spots = [(ax + dx, ay + dy) for dx, dy in targets] + [(ax + 40, ay + 2), (ax - 52, ay - 4)]
    order = [4, 0, 2, 5, 1, 3]
    starts = {k: 2 + j * 2 for j, k in enumerate(order)}      # 2コマずつずらして落ちる
    bolts = {}
    for k, (x, y) in enumerate(spots):
        bolts[k] = zigzag(rnd, 0, x + rnd.randint(-20, 20), y - 14, x, step=(6, 12), wob=(3, 8))
    sparks = [Sparks(rnd, y - 2, x, 8, y) for x, y in spots]
    frames = []
    N = 2 + 2 * len(spots) + 6
    for i in range(N):
        cv = Canvas(W, H)
        # 雲: 上に暗い雲の帯（点々）が広がる
        cw = min(1.0, (i + 1) / 3)
        for y in range(0, 16):
            for x in range(int(W * (0.5 - 0.5 * cw)), int(W * (0.5 + 0.5 * cw))):
                n = math.sin(x * 0.21 + y * 0.5 + i * 0.3) + math.sin(x * 0.07 - i * 0.2)
                if y < 9 + 4 * n and (x + y) % 2 == 0:
                    cv.put(y, x, "D")
                elif y < 6 + 3 * n and (x + y) % 2 == 1:
                    cv.put(y, x, "V")
        flash = 0.0; shake = 0
        for k, (x, y) in enumerate(spots):
            s = i - starts[k]
            if s < 0 or s > 5:
                continue
            pts = [(p[0], p[1] + (rnd.uniform(-2, 2) if 0 < q < len(bolts[k]) - 1 else 0)) for q, p in enumerate(bolts[k])]
            if s == 0:      # 先がけ
                m = path_mask([(int(a), int(round(b))) for a, b in pts[: max(2, len(pts) // 2)]], H, W)
                draw_glow(cv, m, width=1, halo=0, core_c="Y", rim_c=None, glow_c="C")
                continue
            if s == 3:      # 一瞬消える
                m = path_mask([(int(a), int(round(b))) for a, b in pts], H, W)
                cv.mask_put(ndimage.binary_dilation(m), "V", dither=True)
                sparks[k].step(cv)
                continue
            width = {1: 2, 2: 2, 4: 1, 5: 1}[s]
            m = path_mask([(int(a), int(round(b))) for a, b in pts] + [(y, x)], H, W)
            for br in branches(rnd, pts, 2 if s < 3 else 1, H, W):
                draw_glow(cv, path_mask([(int(a), int(b)) for a, b in br], H, W), width=1, halo=0, core_c="Y", rim_c=None, glow_c="C")
            draw_glow(cv, m, width=width, halo=1 if s < 3 else 0)
            if s in (1, 2, 4):
                starburst(cv, y - 10, x, 9 if s == 1 else 6, rays=8, rot=rnd.uniform(0, 0.8))
                ring(cv, y, x, 6 + s * 4, (6 + s * 4) / 3.2, "C")
            sparks[k].step(cv)
            # 白い光は、最初の1本だけ強め。ほかは弱く（画面が何度も白く点滅すると、目にきつい）
            if s == 1:
                flash = max(flash, 0.35 if k == order[0] else 0.1); shake = max(shake, 3 if k == order[0] else 2)
            elif s == 4:
                shake = max(shake, 1)
        # 終わり: 全部に光が残り、煙
        if i >= N - 6:
            j = i - (N - 6)
            for k, (x, y) in enumerate(spots):
                sparks[k].step(cv)
                for q in range(3):
                    cv.put(y - j * 2 - q * 3, x + (q - 1) * 3 + (j % 2), "D", over=False)
                cv.put(y + 1, x - 3, "D"); cv.put(y + 1, x + 3, "D")
        dim = min(0.7, 0.2 + 0.12 * i) if i < N - 4 else max(0.0, 0.7 - 0.18 * (i - (N - 4)))
        frames.append(frame(cv, 60 if i < N - 6 else 90, dim=dim, flash=flash, shake=shake))
    return {"name": "雷の嵐（全体）", "w": W, "h": H, "anchor": [ax, ay], "palette": PAL, "frames": frames}


# ---------------------------------------------------------------- 発動（ボスのまわり）
def make_aura(seed, boss_mask, n=16, fade=4):
    """術をとなえるあいだ、ボスのまわりにかかるエフェクト（人間の指示「魔法を発動するとき、ボス周りに発動のエフェクトも」）。
    boss_mask: 画面に出す大きさ（132×132）のボスの形（True が絵）。キャンバスは上下左右に24ドットの余白をつける。
    - 足もとに、光の輪（術の陣）が広がって回る。奥の半分はボスのうしろ（"back"）、手前の半分はボスの前に描く
    - ボスの体のふちを、細い稲妻がはう（ふちから外へ、短いぎざぎざ）。ふちに水色の光が脈打つ
    - 陣から光の粒がのぼる。最後に光の柱が立ち、輪がはじけて消える
    """
    rnd = random.Random(seed + 11)
    M = 24
    bh, bw = boss_mask.shape
    W, H = bw + 2 * M, bh + 2 * M
    body = np.zeros((H, W), bool); body[M:M + bh, M:M + bw] = boss_mask
    ys, xs = np.nonzero(body)
    foot_y = int(ys.max()) - 2
    cx = int(np.median(xs[ys > ys.max() - 30]))
    edge = body & ~ndimage.binary_erosion(body)
    ey, ex = np.nonzero(edge)
    dist, (iy, ix) = ndimage.distance_transform_edt(~body, return_indices=True)
    k3 = np.ones((3, 3), bool)
    rim1 = ndimage.binary_dilation(body, k3) & ~body
    rim2 = ndimage.binary_dilation(body, k3, iterations=3) & ~ndimage.binary_dilation(body, k3, iterations=2)
    parts = []
    frames = []
    total = n + fade
    for i in range(total):
        front, back = Canvas(W, H), Canvas(W, H)
        t = min(1.0, i / (n - 1))
        out = max(0.0, (i - n + 1) / fade)              # 0→1 で消えていく
        # 術の陣（足もとの光の輪）
        R = 62 * min(1.0, (i + 1) / 5) * (1 + 0.15 * out)
        rot = i * 0.22
        if R > 2 and out < 1:
            for rr, col, dith in ((R, "C", False), (R * 0.78, "B", True), (R * 0.5, "C", True)):
                steps = int(2 * math.pi * rr) * 2 + 8
                for q in range(steps):
                    a = 2 * math.pi * q / steps
                    y, x = foot_y + math.sin(a) * rr * 0.26, cx + math.cos(a) * rr
                    if dith and (q % 2):
                        continue
                    if out and rnd.random() < out:
                        continue
                    (back if math.sin(a) < 0 else front).put(y, x, col, over=False)
            # 輪の上の、まわる印（小さな縦の棒と点。どの作品の文字でもない、この術だけの印）
            for q in range(12):
                a = rot + 2 * math.pi * q / 12
                y, x = foot_y + math.sin(a) * R * 0.89 * 0.26, cx + math.cos(a) * R * 0.89
                cv = back if math.sin(a) < 0 else front
                cv.put(y, x, "Y"); cv.put(y - 1, x, "Y" if q % 3 else "W")
                if q % 2 == 0:
                    cv.put(y - 3, x, "C")
        # 光の粒がのぼる
        if i < n:
            for _ in range(3 + int(4 * t)):
                a = rnd.uniform(0, 2 * math.pi); rr = rnd.uniform(0.2, 1.0) * R
                parts.append([foot_y + math.sin(a) * rr * 0.26, cx + math.cos(a) * rr, rnd.uniform(1.5, 3.5), rnd.randint(5, 9)])
        for q in parts:
            if q[3] <= 0:
                continue
            col = "W" if q[3] > 6 else ("C" if q[3] > 3 else "B")
            (back if rnd.random() < 0.4 else front).put(q[0], q[1], col)
            q[0] -= q[2]; q[3] -= 1
        # ボスのふちの光（脈打つ）。術を放ったあとはボスの姿が変わるので、ふちの光と稲妻は消す
        if i < n:
            pulse = (i % 4) < 2
            front.mask_put(rim1 & (np.indices(rim1.shape).sum(0) % 2 == (i % 2)), "C" if pulse else "B", under=True)
            if pulse and t > 0.3:
                front.mask_put(rim2, "B", dither=True, under=True)
        # ふちをはう細い稲妻
        if i < n:
            for _ in range(int(3 + 7 * t)):
                j = rnd.randrange(len(ey)); y0, x0 = ey[j], ex[j]
                # 外向き: ふちから、体のまん中と反対の向きへ
                vy, vx = y0 - (M + bh * 0.45), x0 - cx
                L = math.hypot(vy, vx) or 1; vy, vx = vy / L, vx / L
                pts = [(y0, x0)]; y, x = float(y0), float(x0)
                for _ in range(rnd.randint(2, 4)):
                    step = rnd.uniform(3, 6)
                    y += vy * step + rnd.uniform(-2.5, 2.5); x += vx * step + rnd.uniform(-2.5, 2.5)
                    pts.append((int(round(y)), int(round(x))))
                m = path_mask(pts, H, W) & ~body
                draw_glow(front, m, width=1, halo=0, core_c="W" if rnd.random() < 0.5 else "Y", rim_c=None, glow_c="C")
        # 最後: 光の柱が立つ（陣から上へ）
        if n - 3 <= i < n + 1:
            h = (i - (n - 3) + 1) * 30
            for q in range(7):
                x = cx + (q - 3) * R * 0.28
                for y in range(int(foot_y - h), foot_y):
                    if (y + q + i) % 2 == 0:
                        front.put(y, x, "C" if abs(q - 3) > 1 else "Y", over=False)
        fr = frame(front, 70 if i < n else 60, dim=0.0)
        bx, by, brows = back.out()
        fr.update({"bx": bx, "by": by, "back": brows})
        frames.append(fr)
    return {"name": "発動（ボスのまわり）", "w": W, "h": H, "anchor": [M, M], "palette": PAL, "frames": frames,
            "note": "anchor はボスの絵（132×132）の左上。back はボスのうしろに描く"}


if __name__ == "__main__":
    out = sys.argv[1]
    seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 7
    import os
    os.makedirs(out, exist_ok=True)
    todo = [("charge", make_charge(seed)), ("bolt", make_bolt(seed)), ("storm", make_storm(seed))]
    if "--boss" in sys.argv:     # --boss ボスのanim.json: 両手を振り上げた姿の形で「発動」を作る
        from PIL import Image
        an = json.load(open(sys.argv[sys.argv.index("--boss") + 1]))
        rows = an["flat_attack3"][5]
        a = np.array([[c != "." for c in r] for r in rows], np.uint8) * 255
        m = np.array(Image.fromarray(a).resize((132, 132), Image.LANCZOS)) > 110
        todo.append(("aura", make_aura(seed, m)))
    for name, fx in todo:
        json.dump(fx, open(f"{out}/{name}.json", "w"), ensure_ascii=False)
        print(name, fx["name"], len(fx["frames"]), "コマ", sum(f["ms"] for f in fx["frames"]), "ミリ秒")
