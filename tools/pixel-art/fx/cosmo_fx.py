"""レジェンドの装備「コスモリングライト」のエフェクト（ドット絵のコマ）を作る（2026-10-06、人間の指示
「攻撃のモーションは砲台が自由に飛び回り電撃型のビームを6連射する形にしよう」「モーションはド派手に」
「戦闘開始時リングが輝きに装着するモーションを入れよう」）。
作り方は spells.py・arbiter_fx.py と同じ。できたコマは fx-editor.mjs でドット絵エディタに1コマずつ入れてシートにし、
verify_sheet.py で食い違い0マスを確かめてから、export-spell-sheets.py でゲームに入れる。

  charge（装着）: 光の粒がうずを巻いて体に集まる → 背に光の環が生まれて広がる → 環がかがやき、白い閃光 →
                  6方向から鎧の板（白と金のかけら）が飛んできて体にはまる → 環が静かに光り続ける
  bolt（雷のビーム）: 砲口（右はし）から左へのびる、太い雷のビーム。芯は白、ふちは水色、外は青の点々。枝の稲妻と、
                  砲口の光の星。くり返す（ゲームでは、砲台から敵へ向けて回して、長さを合わせて描く）
  hit（命中）: 白い閃光の芯・十字の星・まわりへ走る短い稲妻・広がる光の輪・火花
  aura（いつもの輝き。くり返す）: 体のまわりで脈打つ光・外へ広がって消える光の輪・逆向きにまわる2つの光の粒の輪・
                  立ちのぼる光のすじ（人間の指示「常時輝きのモーション入れて」）

使い方: python3 tools/pixel-art/fx/cosmo_fx.py assets-src/effects/spells
"""
import json
import math
import os
import random
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import spells  # noqa: E402
from spells import Canvas, frame, ellipse_ring, star, Bits, CW, CH, CAX, CAY  # noqa: E402
from lightning import zigzag, path_mask, draw_glow, branches  # noqa: E402

PAL = {"W": "#ffffff", "Y": "#e8fbff", "G": "#a8ecff", "O": "#5ad0ff", "R": "#2a9ae8", "D": "#1a5ab0", "M": "#10306a",
       "K": "#c8d4e8", "S": "#f0f4fb", "L": "#8a96b0", "X": "#ffe27a", "Z": "#d8a030"}
spells.PALS["cosmo"] = PAL
spells.FLASH["cosmo"] = "#d8f6ff"

BW, BH, BAX, BAY = 112, 28, 111, 14     # ビーム（右はしが砲口）
HW, HH, HAX, HAY = 80, 80, 40, 40       # 命中（まん中が当たる所）
AUW, AUH, AUX, AUY = 72, 80, 36, 42     # いつもの輝き（まん中が体のまん中）


def zig(rnd, y0, x0, y1, x1, seg=(4, 8), amp=(2, 5)):
    """どの向きにも使える、ぎざぎざの稲妻の点の並び（(y, x)）。進む向きに対して左右へ交互にふれる"""
    L = math.hypot(y1 - y0, x1 - x0) or 1
    uy, ux = (y1 - y0) / L, (x1 - x0) / L
    py, px = ux, -uy
    pts = [(y0, x0)]
    d, side = 0.0, 1
    while True:
        d += rnd.uniform(*seg)
        if d >= L:
            break
        o = side * rnd.uniform(*amp)
        side = -side
        pts.append((y0 + uy * d + py * o, x0 + ux * d + px * o))
    pts.append((y1, x1))
    return pts


def glow_disk(cv, cy, cx, r):
    for y in range(int(cy - r * 1.6) - 1, int(cy + r * 1.6) + 2):
        for x in range(int(cx - r * 1.6) - 1, int(cx + r * 1.6) + 2):
            d = math.hypot(y - cy, x - cx)
            if d <= r * 0.55:
                cv.put(y, x, "W")
            elif d <= r * 0.85:
                cv.put(y, x, "Y")
            elif d <= r * 1.15:
                cv.put(y, x, "G", over=False)
            elif d <= r * 1.6 and (x + y) % 2 == 0:
                cv.put(y, x, "O", over=False)


def equip_charge(rnd):
    el = "cosmo"
    W, H, ax, ay = CW, CH, CAX, CAY
    cy = ay - 18                       # 体のまん中（鎧の胸）
    frames = []
    N = 26
    motes = [[rnd.uniform(0, 2 * math.pi), rnd.uniform(30, 46), rnd.uniform(0.18, 0.3)] for _ in range(26)]
    plates = [(2 * math.pi * q / 6 + 0.3, rnd.choice("SK")) for q in range(6)]
    sparks = Bits()
    for k in range(N):
        cv = Canvas(W, H)
        t = k / (N - 1)
        # 1) 光の粒が、うずを巻いて体へ集まる（0〜10コマ）
        if k <= 11:
            for m in motes:
                a, r, sp = m
                rr = r * (1 - k / 12)
                aa = a + k * sp * 2
                y, x = cy + math.sin(aa) * rr * 0.8, ax + math.cos(aa) * rr
                cv.put(y, x, "W" if rr < 14 else "G")
                cv.put(y + 1, x, "O", over=False)
                if rr > 10:
                    cv.put(y - math.sin(aa) * 2, x - math.cos(aa) * 2, "R", over=False)
        # 2) 背の光の環が生まれ、広がる（4コマ目〜）。たての円（少しななめから見た楕円）
        if k >= 4:
            R = min(22, 3 + (k - 4) * 3.2)
            glow = k in range(10, 15)
            ellipse_ring(cv, cy, ax, R, R * 0.92, "W" if glow else "G", over=True)
            ellipse_ring(cv, cy, ax, R + 1, (R + 1) * 0.92, "O" if glow else "R", over=False)
            ellipse_ring(cv, cy, ax, R + 3, (R + 3) * 0.92, "D", dither=True, k=k, over=False)
            # 環の上の6つの金の節
            for q in range(6):
                a = q * math.pi / 3 + k * 0.08
                cv.put(cy + math.sin(a) * R * 0.92, ax + math.cos(a) * R, "X")
                cv.put(cy + math.sin(a) * R * 0.92 - 1, ax + math.cos(a) * R, "W")
            if glow:
                ellipse_ring(cv, cy, ax, R - 2, (R - 2) * 0.92, "Y", dither=True, k=k + 1, over=False)
        # 3) 環がかがやき、白い閃光（11〜14コマ）
        if 11 <= k <= 15:
            L = [14, 30, 38, 26, 14][k - 11]
            glow_disk(cv, cy, ax, [5, 10, 13, 9, 5][k - 11])
            star(cv, cy, ax, L, rays=4, core="W", mid="Y", tip="G")
            star(cv, cy, ax, L * 0.55, rays=4, core="W", mid="X", tip="Z", rot=math.pi / 4)
            if k == 12:
                sparks.burst(rnd, cy, ax, 22, speed=(1.6, 4.2), up=False, life=(4, 9), grav=0.15)
        # 4) 鎧の板が6方向から飛んできて、はまる（13〜20コマ）
        if 13 <= k <= 20:
            q_t = (k - 13) / 7
            for a, c in plates:
                r = 34 * (1 - q_t)
                y, x = cy + math.sin(a) * r * 0.8, ax + math.cos(a) * r
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        cv.put(y + dy, x + dx, c)
                cv.put(y - 1, x - 1, "W"); cv.put(y + 1, x + 1, "L"); cv.put(y, x + 2, "X")
                # 飛んでくる光の尾
                for s in range(1, 6):
                    cv.put(y + math.sin(a) * s * 1.6, x + math.cos(a) * s * 2, "O" if s < 3 else "R", over=False)
            if k == 20:
                star(cv, cy, ax, 18, rays=4, core="W", mid="X", tip="Z")
        sparks.step(cv, "WYGO")
        flash = 0.5 if k == 12 else (0.22 if k == 20 else 0.0)
        shake = 3 if k == 12 else (2 if k == 20 else 0)
        frames.append(frame(cv, 60 if k < 16 else 70, el, dim=0.45 if k < N - 4 else 0.45 - 0.1 * (k - N + 4), flash=flash, shake=shake))
    return frames


def beam(rnd):
    """砲口（右はし）から左へのびる雷のビーム。6コマをくり返す"""
    el = "cosmo"
    frames = []
    for k in range(6):
        cv = Canvas(BW, BH)
        # 太い本体の稲妻（ぎざぎざ）＋枝
        pts = zig(rnd, BAY, BAX - 2, BAY + rnd.uniform(-2, 2), 1, seg=(5, 9), amp=(2, 5))
        core = path_mask(pts, BH, BW)
        for _ in range(3):
            i = rnd.randrange(1, len(pts) - 1)
            y, x = pts[i]
            ey, ex = y + rnd.choice((-1, 1)) * rnd.uniform(5, 9), x - rnd.uniform(5, 12)
            core |= path_mask(zig(rnd, y, x, ey, ex, seg=(2, 4), amp=(1, 2)), BH, BW)
        draw_glow(cv, core, width=2 if k % 2 == 0 else 3, halo=2, core_c="W", rim_c="Y", glow_c="O", halo_c="D")
        # もう2本、細い稲妻がからみつく
        for _ in range(2):
            p2 = zig(rnd, BAY + rnd.uniform(-3, 3), BAX - 4, BAY + rnd.uniform(-4, 4), 3, seg=(3, 7), amp=(2, 6))
            draw_glow(cv, path_mask(p2, BH, BW), width=1, halo=0, core_c="Y", rim_c=None, glow_c="R", halo_c=None)
        # 砲口の光の星
        star(cv, BAY, BAX - 3, 8 if k % 2 == 0 else 6, rays=4, core="W", mid="Y", tip="G")
        frames.append(frame(cv, 45, el, dim=0.0, flash=0.0, shake=0))
    return frames


def hit(rnd):
    el = "cosmo"
    frames = []
    sparks = Bits()
    N = 11
    for k in range(N):
        cv = Canvas(HW, HH)
        cy, cx = HAY, HAX
        if k <= 5:
            L = [16, 26, 22, 18, 12, 8][k]
            glow_disk(cv, cy, cx, [6, 10, 8, 6, 4, 2][k])
            star(cv, cy, cx, L, rays=4, core="W", mid="Y", tip="G")
            star(cv, cy, cx, L * 0.6, rays=4, core="W", mid="G", tip="O", rot=math.pi / 4)
        if k == 1:
            sparks.burst(rnd, cy, cx, 18, speed=(1.8, 4.6), up=False, life=(3, 8), grav=0.25)
        # まわりへ走る短い稲妻（6本）
        if 1 <= k <= 6:
            for q in range(6):
                a = q * math.pi / 3 + rnd.uniform(-0.3, 0.3)
                r1 = 6 + k * 2
                r2 = r1 + rnd.uniform(8, 16)
                pts = zig(rnd, cy + math.sin(a) * r1, cx + math.cos(a) * r1, cy + math.sin(a) * r2, cx + math.cos(a) * r2, seg=(2, 4), amp=(1, 3))
                draw_glow(cv, path_mask(pts, HH, HW), width=1, halo=0, core_c="W" if k < 4 else "Y", rim_c=None, glow_c="O", halo_c=None)
        # 広がる光の輪
        if 1 <= k <= 8:
            R = 6 + k * 4
            ellipse_ring(cv, cy, cx, R, R * 0.9, "G" if k < 5 else "R", dither=k >= 4, k=k, over=False)
        sparks.step(cv, "WYGO")
        frames.append(frame(cv, 40 if k < 4 else 55, el, dim=0.0, flash=0.35 if k == 1 else 0.0, shake=3 if k == 1 else 0))
    return frames


def aura(rnd):
    """いつもの輝き。16コマでひとめぐり（くり返してもつながる）"""
    el = "cosmo"
    frames = []
    N = 16
    streaks = [(rnd.uniform(-16, 16), rnd.uniform(0, 1), rnd.choice((3, 4, 5))) for _ in range(9)]
    for k in range(N):
        cv = Canvas(AUW, AUH)
        cy, cx = AUY, AUX
        ph = k / N
        # 体のまわりの、脈打つ光（芯はうすく、まわりは1ドットおき）
        pulse = 0.5 + 0.5 * math.cos(ph * 2 * math.pi)
        R0 = 13 + pulse * 3
        for y in range(int(cy - R0 * 1.5) - 1, int(cy + R0 * 1.5) + 2):
            for x in range(int(cx - R0) - 1, int(cx + R0) + 2):
                d = math.hypot((x - cx) / R0, (y - cy) / (R0 * 1.45))
                if 0.82 < d <= 1.0:
                    cv.put(y, x, "G" if pulse > 0.5 else "O", over=False)
                elif 0.6 < d <= 0.82 and (x + y + k) % 2 == 0:
                    cv.put(y, x, "R", over=False)
        # 外へ広がって消える光の輪（2つ、半周ずらし）
        for off in (0.0, 0.5):
            q = (ph + off) % 1
            R = 14 + q * 18
            ellipse_ring(cv, cy, cx, R, R * 1.25, "Y" if q < 0.35 else ("O" if q < 0.7 else "D"), dither=q > 0.45, k=k, over=False)
        # 逆向きにまわる、光の粒の輪（6つずつ）
        for q in range(6):
            a1 = ph * 2 * math.pi + q * math.pi / 3
            a2 = -ph * 2 * math.pi + q * math.pi / 3 + 0.5
            for (a, rx, ry, c) in ((a1, 20, 9, "W"), (a2, 16, 24, "Y")):
                y, x = cy + math.sin(a) * ry, cx + math.cos(a) * rx
                cv.put(y, x, c); cv.put(y, x + 1, "G", over=False); cv.put(y + 1, x, "O", over=False)
        # 立ちのぼる光のすじ
        for (ox, st, ln) in streaks:
            q = (ph + st) % 1
            y0 = cy + 22 - q * 46
            for j in range(ln):
                cv.put(y0 + j, cx + ox, "W" if j == 0 else ("G" if j < 2 else "O"))
        frames.append(frame(cv, 70, el))
    return frames


def build(seed=21):
    rnd = random.Random(seed)
    meta = lambda name, frames, w, h, a: {"name": name, "w": w, "h": h, "anchor": list(a), "palette": PAL, "frames": frames}
    return {
        "charge": meta("コスモリングライト 装着", equip_charge(rnd), CW, CH, (CAX, CAY)),
        "bolt": meta("コスモリングライト 雷のビーム（砲口＝右はし）", beam(rnd), BW, BH, (BAX, BAY)),
        "hit": meta("コスモリングライト 命中", hit(rnd), HW, HH, (HAX, HAY)),
        "aura": meta("コスモリングライト いつもの輝き（くり返す）", aura(rnd), AUW, AUH, (AUX, AUY)),
    }


if __name__ == "__main__":
    outdir = sys.argv[1]
    d = os.path.join(outdir, "cosmo")
    os.makedirs(d, exist_ok=True)
    for kind, fx in build().items():
        json.dump(fx, open(os.path.join(d, f"{kind}.json"), "w"), ensure_ascii=False)
        print("cosmo", kind, len(fx["frames"]), "コマ", sum(f["ms"] for f in fx["frames"]), "ミリ秒")
