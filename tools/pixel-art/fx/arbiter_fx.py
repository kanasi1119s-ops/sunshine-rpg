"""隠しボス「機械の悪神巨人兵」の魔法3つのエフェクト（ドット絵のコマ）を作る（2026-10-06、人間の指示
「魔法のモーションもすべて作ってください。ものすごく派手でカッコいいのを期待してます」「モーションづくりはエディタを使ってください」）。
作り方は spells.py と同じ（熱さの格子を流す・芯が白く外へ暗く・いちばん外は1ドットおき・けむりは網目）。
できたコマは、spells.py と同じく fx-editor.mjs でドット絵エディタに1コマずつ入れてシートに書き出し、ゲームはそのシートを使う。

  meteor（流星の裁き。全体・防御無視）
    charge: 巨人兵の足もとに紫の二重の陣と8つの光の珠（灯の環の印）。陣のふちから紫の炎が立ち、まわりの光が吸いこまれ、
            最後に天へ向かって太い光の柱がのびる（流星を呼ぶ）
    area  : 1人ずつ。足もとに赤い照準の陣 → 左上の空から、紫の炎の尾を引く流星が落ちる → 白い閃光と大爆発、地面を走る衝撃の輪、
            飛び散る岩、立ちのぼる紫の火柱、けむり
  judgement（神の調停。全員の体力を半分に）
    charge: 巨人兵のまわりに金の輪が三重に広がり、紫の紋（ルーン）がまわる。光が集まり、最後に金の星がはじける
    area  : 1人ずつ。金の紋の輪が天から降りてきて体をしめつける → 白金の光の槍がまっすぐ落ちる → 金の一閃が体をまっぷたつに
            （体力が半分になる印）→ 輪がくだけて金の破片がふり、紋が消える
  blessing（神の祝福。減ったHPの半分を回復）
    hit   : 巨人兵の体に。金の歯車の輪が二つ、逆向きにまわり、光の柱と、緑に光るいやしの粒が立ちのぼる。最後にやわらかい光がはじける

使い方: python3 tools/pixel-art/fx/arbiter_fx.py assets-src/effects/spells
"""
import json
import math
import os
import random
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import spells  # noqa: E402
from spells import Canvas, paint, frame, ellipse_ring, blob_heat, star, Bits, Smoke, noise, FireField, CW, CH, CAX, CAY, CHAR_H  # noqa: E402

PALS = {
    "meteor": {"W": "#ffffff", "Y": "#f6e8ff", "G": "#e0b0ff", "O": "#b060f0", "R": "#7a2ad0", "D": "#4a1490", "M": "#22083f",
               "K": "#2a1830", "S": "#4a3858", "L": "#7a6890", "X": "#ffb060", "Z": "#ff4a3a"},
    "judgement": {"W": "#ffffff", "Y": "#fff6d0", "G": "#ffe08a", "O": "#f2b83c", "R": "#c8841c", "D": "#7a4a10", "M": "#3a2208",
                  "K": "#3a2a50", "S": "#6a5a8a", "L": "#b8a8e0", "X": "#d890ff", "Z": "#fffbe8"},
    "blessing": {"W": "#ffffff", "Y": "#fffbe0", "G": "#fff0a0", "O": "#ffd060", "R": "#e8a030", "D": "#a86818", "M": "#5a3a10",
                 "K": "#c8b0f0", "S": "#e0d0ff", "L": "#f4ecff", "X": "#d890ff", "Z": "#8affd0"},
}
FLASH = {"meteor": "#e8c8ff", "judgement": "#fff2c0", "blessing": "#fff8e0"}
spells.PALS.update(PALS)
spells.FLASH.update(FLASH)

AW, AH, AAX, AAY = 128, 208, 64, 196      # 全体の術（1人ずつ）のキャンバス。足もと（anchor）
BODY = 30


def disk(cv, cy, cx, r, c, over=True):
    for y in range(int(cy - r), int(cy + r) + 1):
        for x in range(int(cx - r), int(cx + r) + 1):
            if (y - cy) ** 2 + (x - cx) ** 2 <= r * r:
                cv.put(y, x, c, over=over)


# ================================================================ 流星の裁き
def meteor_charge(rnd):
    """紫の二重の陣・8つの光の珠・ふちから立つ紫の炎・吸いこまれる光。最後に天への光の柱"""
    el = "meteor"
    W, H, ax, ay = CW, CH, CAX, CAY
    yy, xx = np.indices((H, W))
    f = FireField(H, W, rnd, decay=0.9, cool=0.05)
    swirl = []
    frames = []
    N = 18
    for k in range(N):
        cv = Canvas(W, H)
        t = k / (N - 1)
        R = 40 * min(1.0, (k + 1) / 4)
        ring_m = np.abs(np.hypot((xx - ax) / max(R * 0.95, 1), (yy - ay) / max(R * 0.95 * 0.3, 1)) - 1) * R * 0.3 < 1.3
        f.step(ring_m & (noise(rnd, H, W, 3) > 0.42), 0.7 + 0.3 * t, sub=4)
        paint(cv, f.heat)
        # 陣: 外の輪・内の輪（1ドットおき）・回る8つの光の珠
        ellipse_ring(cv, ay, ax, R, R * 0.3, "O", over=True)
        ellipse_ring(cv, ay, ax, R * 1.12, R * 1.12 * 0.3, "D", dither=True, k=k, over=True)
        ellipse_ring(cv, ay, ax, R * 0.7, R * 0.7 * 0.3, "G", dither=True, k=k + 1, over=True)
        for q in range(8):
            a = k * 0.28 + 2 * math.pi * q / 8
            y, x = ay + math.sin(a) * R * 0.3, ax + math.cos(a) * R
            disk(cv, y, x, 2.2, "G"); cv.put(y, x, "W"); cv.put(y - 1, x - 1, "W")
        # 吸いこまれる光（紫の粒）
        for _ in range(4):
            swirl.append([rnd.uniform(0, 2 * math.pi), rnd.uniform(34, 50)])
        for s in swirl:
            if s[1] <= 4:
                continue
            y, x = ay - 40 + math.sin(s[0]) * s[1] * 0.8, ax + math.cos(s[0]) * s[1]
            cv.put(y, x, "W" if s[1] < 16 else "G"); cv.put(y + 1, x, "O")
            s[0] += 0.5; s[1] -= 3.4
        # 天への光の柱（最後の5コマ）
        if k >= N - 6:
            u = (k - (N - 6)) / 5
            half = 3 + 7 * u
            top = ay - 10 - int(110 * min(1.0, u * 1.6))
            for y in range(max(0, top), ay - 6):
                for x in range(int(ax - half - 2), int(ax + half + 3)):
                    d = abs(x - ax) / max(1, half)
                    c = "W" if d < 0.35 else ("Y" if d < 0.6 else ("G" if d < 0.85 else ("O" if d <= 1.0 else None)))
                    if c is None:
                        if (x + y) % 2 == 0 and d < 1.35:
                            cv.put(y, x, "R", over=False)
                        continue
                    cv.put(y, x, c)
            star(cv, ay - 40, ax, 14 + 10 * u, rays=8, core="W", mid="Y", tip="O")
        frames.append(frame(cv, 70, el, dim=0.2 + 0.35 * t, flash=0.3 if k == N - 1 else (0.12 if k == N - 3 else 0.0), shake=2 if k >= N - 3 else 0))
    return frames


def meteor_area(rnd):
    """照準の陣 → 左上の空から流星 → 閃光・大爆発・衝撃の輪・岩・紫の火柱・けむり"""
    el = "meteor"
    W, H, ax, ay = AW, AH, AAX, AAY
    ty = ay - BODY
    yy, xx = np.indices((H, W))
    col = FireField(H, W, rnd, decay=0.986, cool=0.006)
    bits = Bits()
    rocks = []
    smoke = Smoke()
    frames = []
    FALL = 7
    sx, sy = 6.0, -10.0                       # 流星の出どころ（左上の空）
    ex, ey = ax - 2, ty + 6                   # 当たる所
    trail = []
    for k in range(22):
        cv = Canvas(W, H)
        # 足もとの照準の陣（赤い輪と十字。落ちてくるあいだ、ちぢむ）
        if k < FALL + 1:
            r = 30 - k * 2.4
            ellipse_ring(cv, ay, ax, r, r * 0.32, "Z", over=True)
            ellipse_ring(cv, ay, ax, r * 0.55, r * 0.55 * 0.32, "X", dither=True, k=k)
            for d in (-1, 1):
                for s in range(4, int(r) + 6):
                    if s % 2 == 0:
                        cv.put(ay, ax + d * s, "Z")
        if k < FALL:
            u = (k + 1) / FALL
            u = u * u                         # 加速して落ちる
            hx, hy = sx + (ex - sx) * u, sy + (ey - sy) * u
            # 尾: 出どころから頭まで、頭ほど太く明るい炎（ゆらぐふち）
            heat = np.zeros((H, W))
            L = math.hypot(hx - sx, hy - sy) + 40
            ux, uy = (hx - sx) / max(1, L - 40), (hy - sy) / max(1, L - 40)
            n = int(L / 2.5)
            for i in range(n + 1):
                q = i / max(1, n)                 # 0＝尾のはし、1＝頭
                py, px = hy - uy * (1 - q) * L, hx - ux * (1 - q) * L
                r = 2.5 + 11 * q ** 1.8
                jy, jx = (rnd.random() - 0.5) * 3 * (1 - q), (rnd.random() - 0.5) * 3 * (1 - q)
                heat = np.maximum(heat, blob_heat(H, W, py + jy, px + jx, r, rnd, sq=1.0, rough=0.7) * (0.45 + 0.55 * q))
            heat = np.maximum(heat, blob_heat(H, W, hy, hx, 13 + k * 0.8, rnd, sq=1.0, rough=0.35))
            paint(cv, heat, smooth=0.6)
            disk(cv, hy, hx, 4 + k * 0.4, "W")
            # 頭の前の、光のくさび（空気をさく）
            for q in range(10):
                a = math.atan2(uy, ux) + (q - 4.5) * 0.16
                for s_ in range(int(16 + k * 1.5)):
                    if s_ > 6:
                        cv.put(hy + math.sin(a) * s_ * 0.6, hx + math.cos(a) * s_ * 0.6, "Y" if s_ < 12 else "G", over=False)
            # 頭のまわりの燃えるかけら
            for _ in range(4):
                bits.p.append([hy + rnd.uniform(-7, 7), hx + rnd.uniform(-7, 7), rnd.uniform(-1.5, 0.5), rnd.uniform(-3, -0.5), rnd.randint(3, 7), 0.2, 1])
            bits.step(cv, "YGOR")
            flash = 0.0
            shake = 0
        else:
            kk = k - FALL                      # 当たってからのコマ
            if kk == 0:
                bits.burst(rnd, ty, ax, 48, speed=(2.0, 5.5))
                for _ in range(10):
                    a = rnd.uniform(math.pi * 1.05, math.pi * 1.95)
                    v = rnd.uniform(2.5, 5.5)
                    rocks.append([ty, ax + rnd.uniform(-6, 6), math.sin(a) * v, math.cos(a) * v, rnd.randint(2, 3)])
            # 大爆発（まん中から燃えつきて輪になる）
            Rr = [26, 40, 50, 54, 54, 52, 48, 44, 40, 35, 30, 25, 20, 15, 10][kk] if kk < 15 else 0
            heat = blob_heat(H, W, ty, ax, Rr, rnd, burn=min(1.0, kk / 6)) * (1 - max(0, kk - 3) / 13) if Rr else np.zeros((H, W))
            # 紫の火柱（立ちのぼる）
            if 1 <= kk <= 10:
                col.step((np.hypot(yy - (ty - 2), (xx - ax) * 0.6) < 16) & (noise(rnd, H, W, 3) > 0.45), 1.0, sub=14)
            else:
                col.step(None, sub=14)
            heat = np.maximum(heat, col.heat)
            if 2 <= kk <= 9:
                for _ in range(3):
                    smoke.add(ty - rnd.uniform(0, 30), ax + rnd.uniform(-22, 22), rnd.uniform(2, 4.5))
            smoke.step(cv, k)
            paint(cv, heat)
            # 地面を走る衝撃の輪（2本）
            for (k0, col_) in ((0, "W"), (2, "G")):
                q = kk - k0
                if 0 <= q < 8:
                    rx = 14 + q * 9
                    ellipse_ring(cv, ay, ax, rx, rx * 0.28, col_ if q < 4 else "O", dither=q >= 4, k=k)
            # はじめの閃光（とがった光の線）
            if kk <= 2:
                for q in range(16):
                    a = q * math.pi / 8 + rnd.uniform(-0.15, 0.15)
                    L = (60 if q % 2 == 0 else 34) * (1 - kk * 0.25)
                    for s_ in range(int(L)):
                        cv.put(ty + math.sin(a) * s_, ax + math.cos(a) * s_, "W" if s_ < L * 0.35 else ("Y" if s_ < L * 0.7 else "G"), over=False)
                disk(cv, ty, ax, 16 - kk * 4, "W")
            # 飛び散る岩（暗い石に、燃えるふち）
            for r_ in rocks:
                if r_[0] > ay:
                    r_[0] = ay
                for dy in range(r_[4]):
                    for dx in range(r_[4]):
                        cv.put(r_[0] + dy, r_[1] + dx, "M" if (dy + dx) else "X")
                r_[0] += r_[2]; r_[1] += r_[3]; r_[2] += 0.55
            bits.step(cv, "WGOR", ground=ay)
            # 焼けた地面
            if kk >= 2:
                for x in range(ax - 22, ax + 23):
                    if (x + k) % 2 == 0 or abs(x - ax) < 12:
                        cv.put(ay + 1, x, "M", over=False)
            flash = {0: 0.6, 1: 0.3, 2: 0.12}.get(kk, 0.0)
            shake = {0: 9, 1: 7, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1}.get(kk, 0)
        frames.append(frame(cv, 45 if k < FALL else (55 if k < FALL + 4 else 70), el, dim=0.55 - 0.015 * k, flash=flash, shake=shake))
    return frames


# ================================================================ 神の調停
GLYPHS = [["010", "111", "010", "101", "010"], ["111", "101", "111", "010", "111"], ["101", "010", "111", "010", "101"], ["011", "110", "011", "110", "011"]]


def rune_ring(cv, cy, cx, rx, ry, rot, k, main="G", rune="L", edge="R", fill=True):
    """紋の輪: 3ドットの太さの金の輪（外は暗い金・まん中は金・内は明るい）と、内がわの金のうす明かり（市松）、
    輪にそって回る紫の紋（3×5の記号。前の半分は明るく、うしろの半分は暗い）"""
    if fill:
        for y in range(int(cy - ry), int(cy + ry) + 1):
            for x in range(int(cx - rx), int(cx + rx) + 1):
                if ((x - cx) / max(rx, 1)) ** 2 + ((y - cy) / max(ry, 1)) ** 2 < 0.8 and (x + 2 * y + k) % 5 == 0:
                    cv.put(y, x, "O", over=False)
    ellipse_ring(cv, cy, cx, rx + 2, ry + 1, edge, over=True)
    ellipse_ring(cv, cy, cx, rx + 1, ry + 0.5, main, over=True)
    ellipse_ring(cv, cy, cx, rx, ry, main, over=True)
    ellipse_ring(cv, cy, cx, rx - 1, ry - 0.5, "Y", over=True)
    ellipse_ring(cv, cy, cx, rx - 2, ry - 1, "W", dither=True, k=k)
    for q in range(8):
        a = rot + 2 * math.pi * q / 8
        y0, x0 = cy + math.sin(a) * (ry + 5) - 2, cx + math.cos(a) * (rx + 5) - 1
        front = math.sin(a) > -0.15
        g = GLYPHS[q % 4]
        for gy, row in enumerate(g):
            for gx, ch in enumerate(row):
                if ch == "1":
                    cv.put(y0 + gy, x0 + gx, ("W" if gy == 0 else rune) if front else "S")


def judgement_charge(rnd):
    el = "judgement"
    W, H, ax, ay = CW, CH, CAX, CAY
    cy = ay - 46
    frames = []
    motes = []
    N = 16
    for k in range(N):
        cv = Canvas(W, H)
        t = k / (N - 1)
        # 足もとの金の陣
        R = 38 * min(1.0, (k + 1) / 3)
        ellipse_ring(cv, ay, ax, R, R * 0.3, "O", over=True)
        ellipse_ring(cv, ay, ax, R * 0.75, R * 0.75 * 0.3, "G", dither=True, k=k)
        # 体のまわりに広がる三重の金の輪（紋がまわる）
        for i, (k0, col_) in enumerate(((0, "G"), (3, "O"), (6, "Y"))):
            q = k - k0
            if q >= 0:
                r = min(44, 10 + q * 5)
                rune_ring(cv, cy, ax, r, r * 0.42, k * (0.3 if i % 2 == 0 else -0.25), k, main=col_, fill=False)
        # 集まる光の粒
        for _ in range(4):
            motes.append([rnd.uniform(0, 2 * math.pi), rnd.uniform(36, 48)])
        for s in motes:
            if s[1] <= 4:
                continue
            y, x = cy + math.sin(s[0]) * s[1] * 0.7, ax + math.cos(s[0]) * s[1]
            cv.put(y, x, "W" if s[1] < 18 else "G")
            s[0] += 0.35; s[1] -= 3.0
        if k >= N - 4:
            u = (k - (N - 4)) / 3
            star(cv, cy, ax, 16 + 22 * u, rays=8, core="W", mid="Y", tip="O", rot=u * 0.4)
            star(cv, cy, ax, 8 + 10 * u, rays=4, core="W", mid="Z", tip="G", rot=math.pi / 4)
        frames.append(frame(cv, 70, el, dim=0.2 + 0.35 * t, flash=0.3 if k == N - 1 else 0.0, shake=2 if k == N - 1 else 0))
    return frames


def judgement_area(rnd):
    """金の紋の輪が天から降りる → 体をしめつける → 白金の光の槍 → 金の三日月の一閃で体をまっぷたつに → 輪がくだけ、破片がふる"""
    el = "judgement"
    W, H, ax, ay = AW, AH, AAX, AAY
    ty = ay - BODY
    frames = []
    shards = []
    motes = []
    N = 24
    for k in range(N):
        cv = Canvas(W, H)
        flash = 0.0
        shake = 0
        # 1) 紋の輪が天から降りてくる（まわりながら。輪のまわりに4本の光の柱）
        if k < 7:
            u = (k + 1) / 7
            yy_ = -16 + (ty - 2 + 16) * (1 - (1 - u) ** 2)
            r = 46 - 8 * u
            for q in range(4):
                a = k * 0.3 + q * math.pi / 2
                px = ax + math.cos(a) * r
                for y in range(0, int(yy_) + int(math.sin(a) * r * 0.3)):
                    if (y + k + q) % 2 == 0:
                        cv.put(y, px, "G" if math.sin(a) > 0 else "R")
                        cv.put(y, px + 1, "Y" if math.sin(a) > 0 else "D")
            rune_ring(cv, yy_, ax, r, r * 0.32, k * 0.45, k)
        # 2) 輪が体をしめつける（二重）
        elif k < 10:
            q = k - 7
            r = 36 - q * 6
            rune_ring(cv, ty - 4, ax, r, r * 0.32, k * 0.5, k, main="Y")
            rune_ring(cv, ty + 14, ax, r + 6, (r + 6) * 0.32, -k * 0.5, k, main="O", fill=False)
            for _ in range(10):
                a = rnd.uniform(0, 2 * math.pi)
                cv.put(ty + math.sin(a) * r * 0.4, ax + math.cos(a) * r, "W")
        # 3) 白金の光の槍がまっすぐ落ちる（まわりにうす明かり、足もとに光の花）
        if 9 <= k <= 14:
            q = k - 9
            half = [3, 9, 12, 10, 6, 3][q]
            for y in range(0, ay + 1):
                for x in range(ax - half * 2, ax + half * 2 + 1):
                    d = abs(x - ax) / max(1, half)
                    if d < 0.35:
                        cv.put(y, x, "W")
                    elif d < 0.65:
                        cv.put(y, x, "Z")
                    elif d < 0.85:
                        cv.put(y, x, "Y")
                    elif d <= 1.0:
                        cv.put(y, x, "G")
                    elif (x + y + k) % 2 == 0 and d < 1.6:
                        cv.put(y, x, "O", over=False)
                    elif (x + y + k) % 4 == 0 and d < 2.0:
                        cv.put(y, x, "R", over=False)
            for (rr, c) in ((14 + q * 9, "Y"), (8 + q * 6, "W")):
                ellipse_ring(cv, ay, ax, rr, rr * 0.3, c if q < 4 else "O", dither=q >= 3, k=k)
            star(cv, ay - 2, ax, 18 + q * 4, rays=8, core="W", mid="Y", tip="O")
            if q == 1:
                flash, shake = 0.5, 7
        # 4) 金の三日月の一閃（左上から右下へ。体をまっぷたつに＝体力が半分）
        if 13 <= k <= 18:
            q = k - 13
            sweep = min(1.0, (q + 1) / 3)
            cx_, cy_ = ax, ty - 58
            R = 62
            a0, a1 = math.radians(318), math.radians(318 - 96 * sweep)
            n = 120
            for i in range(n + 1):
                a = a0 + (a1 - a0) * i / n
                th = (1 - abs(i / n - 0.6) * 1.5) * (11 if q < 3 else 11 - (q - 2) * 3)
                for t in range(int(max(0, th)) + 1):
                    rr = R - t + th / 2
                    y, x = cy_ - math.sin(a) * rr, cx_ - math.cos(a) * rr
                    c = "W" if abs(t - th / 2) < th * 0.18 else ("Z" if abs(t - th / 2) < th * 0.3 else ("Y" if abs(t - th / 2) < th * 0.42 else "G"))
                    cv.put(y, x, c)
                if i % 5 == 0 and q < 4:
                    for d in (-3, 3):
                        y, x = cy_ - math.sin(a) * (R + d * 2), cx_ - math.cos(a) * (R + d * 2)
                        cv.put(y, x, "O" if d < 0 else "Y")
            if q == 1:
                flash, shake = 0.55, 9
                for _ in range(34):
                    a = rnd.uniform(0, 2 * math.pi)
                    v = rnd.uniform(1.5, 5)
                    shards.append([ty, ax + rnd.uniform(-22, 22), math.sin(a) * v - 1.5, math.cos(a) * v, rnd.randint(7, 13), rnd.choice((1, 2))])
        # 5) 輪がくだけ、金の破片がふる・紫の紋の光がのぼって消える
        if k == 17:
            for _ in range(26):
                a = rnd.uniform(0, 2 * math.pi)
                shards.append([ty + 10 + math.sin(a) * 6, ax + math.cos(a) * 30, rnd.uniform(-2.5, 0.5), math.cos(a) * rnd.uniform(1, 3.5), rnd.randint(8, 13), 2])
        for sh in shards:
            if sh[4] <= 0:
                continue
            c = "W" if sh[4] > 9 else ("G" if sh[4] > 6 else ("O" if sh[4] > 3 else "R"))
            for dy in range(sh[5]):
                for dx in range(sh[5]):
                    cv.put(sh[0] + dy, sh[1] + dx, c if (dy + dx) == 0 else ("R" if sh[4] > 3 else "D"))
            sh[0] += sh[2]; sh[1] += sh[3]; sh[2] += 0.35; sh[4] -= 1
        if k >= 16:
            for _ in range(3):
                motes.append([ty + rnd.uniform(-10, 20), ax + rnd.uniform(-28, 28)])
            for m in motes:
                cv.put(m[0], m[1], "L"); cv.put(m[0] - 1, m[1], "X"); cv.put(m[0] + 1, m[1], "S")
                m[0] -= 2.6
        frames.append(frame(cv, 55 if k < 13 else 62, el, dim=0.6 - 0.012 * k, flash=flash, shake=shake))
    return frames


# ================================================================ 神の祝福
BW_, BH_, BAX_, BAY_ = 96, 112, 48, 104   # 巨人兵の体に（2倍で描かれる）


def gear_ring(cv, cy, cx, rx, ry, rot, k, main, teeth="W"):
    ellipse_ring(cv, cy, cx, rx, ry, main, over=True)
    ellipse_ring(cv, cy, cx, rx - 1.2, ry - 0.6, "R", dither=True, k=k)
    for q in range(14):
        a = rot + 2 * math.pi * q / 14
        y, x = cy + math.sin(a) * (ry + 1.2), cx + math.cos(a) * (rx + 1.2)
        cv.put(y, x, teeth if math.sin(a) > 0 else "O"); cv.put(y + (1 if math.sin(a) > 0 else -1), x, main)


def blessing_hit(rnd):
    el = "blessing"
    W, H, ax, ay = BW_, BH_, BAX_, BAY_
    cy = ay - 40
    yy, xx = np.indices((H, W))
    sparks = []
    frames = []
    N = 22
    for k in range(N):
        cv = Canvas(W, H)
        t = k / (N - 1)
        fade = 1.0 if k < N - 5 else (N - k) / 5
        # 光の柱（足もとから立ちのぼる、細い光の帯が何本も。まん中は白、ふちは金、外は市松でうすく）
        for c in range(6):
            cx_ = ax + (c - 2.5) * 12 + math.sin(k * 0.5 + c) * 2
            hgt = min(1.0, max(0, k - c * 0.5) / 5) * (78 + 18 * math.sin(c * 1.7)) * fade
            half = 1.5 if c % 2 == 0 else 1.0
            for y in range(int(ay - hgt), ay + 1):
                ph = ((ay - y) + k * 7 + c * 11) % 22
                if ph >= 10:
                    continue                                       # 光のすじは、とぎれとぎれに上へ流れる
                for x in range(int(cx_ - half - 1), int(cx_ + half + 2)):
                    d = abs(x - cx_) / half
                    if d < 0.6:
                        cv.put(y, x, "W" if ph < 6 else "Y")
                    elif d <= 1.0:
                        cv.put(y, x, "G" if ph < 6 else "O")
                    elif (x + y + k) % 2 == 0 and d < 1.8 and ph < 6:
                        cv.put(y, x, "O", over=False)
        # 二つの金の歯車の輪（逆向きにまわり、上下へ動く）
        if 2 <= k < N - 2:
            gear_ring(cv, cy - 10 + math.sin(k * 0.4) * 4, ax, 34, 11, k * 0.35, k, "G")
            gear_ring(cv, cy + 18 - math.sin(k * 0.4) * 4, ax, 28, 9, -k * 0.45, k, "O")
        # 足もとの陣
        ellipse_ring(cv, ay, ax, 36, 9, "O", over=True)
        ellipse_ring(cv, ay, ax, 26, 6.5, "Y", dither=True, k=k)
        # いやしの粒（緑と白）が立ちのぼる・十字にかがやく
        for _ in range(4 if k < N - 4 else 0):
            sparks.append([ay - rnd.uniform(0, 10), ax + rnd.uniform(-34, 34), rnd.uniform(2.0, 3.6)])
        for s in sparks:
            if s[0] < 0:
                continue
            cv.put(s[0], s[1], "Z"); cv.put(s[0] - 1, s[1], "W")
            if int(s[0]) % 9 == 0:
                cv.put(s[0], s[1] - 1, "Z"); cv.put(s[0], s[1] + 1, "Z"); cv.put(s[0] + 1, s[1], "Z")
            s[0] -= s[2]
        if 6 <= k <= 16:
            L = [10, 18, 26, 30, 28, 24, 20, 16, 12, 8, 5][k - 6]
            star(cv, cy, ax, L, rays=4, core="W", mid="Y", tip="G")
            star(cv, cy, ax, L * 0.5, rays=4, core="W", mid="Z", tip="Z", rot=math.pi / 4)
        frames.append(frame(cv, 70, el, dim=0.35 - 0.012 * k, flash=0.25 if k == 8 else 0.0))
    return frames


def build(seed=11):
    rnd = random.Random(seed)
    meta = lambda el, name, frames, w, h, a: {"name": name, "w": w, "h": h, "anchor": list(a), "palette": PALS[el], "frames": frames}
    return {
        "meteor": {
            "charge": meta("meteor", "流星の裁き ため", meteor_charge(rnd), CW, CH, (CAX, CAY)),
            "area": meta("meteor", "流星の裁き 全体（1人ずつ）", meteor_area(rnd), AW, AH, (AAX, AAY)),
        },
        "judgement": {
            "charge": meta("judgement", "神の調停 ため", judgement_charge(rnd), CW, CH, (CAX, CAY)),
            "area": meta("judgement", "神の調停 全体（1人ずつ）", judgement_area(rnd), AW, AH, (AAX, AAY)),
        },
        "blessing": {
            "hit": meta("blessing", "神の祝福（巨人兵に）", blessing_hit(rnd), BW_, BH_, (BAX_, BAY_)),
        },
    }


if __name__ == "__main__":
    outdir = sys.argv[1]
    for el, kinds in build().items():
        d = os.path.join(outdir, el)
        os.makedirs(d, exist_ok=True)
        for kind, fx in kinds.items():
            json.dump(fx, open(os.path.join(d, f"{kind}.json"), "w"), ensure_ascii=False)
            print(el, kind, len(fx["frames"]), "コマ", sum(f["ms"] for f in fx["frames"]), "ミリ秒")
