"""全体フィールドに置く目印の絵（祠・洞窟・森）を、1から描きなおす（2026-10-06、人間の指示「フィールドオブジェクト小屋以外1から作り直し
祠、洞窟、森、フィールドになじむよう、リアルに細かく、光も気にしてドットも一つ一つ細かく使い作り直して」）。
新しい木（tree2d.py）と同じ技法: 形全体に左上から光を当て、そのうえで面ごと・かたまりごとに明暗をつける。重なりの影、色相のずれ
（明るい所は黄色寄り、影は青寄り）、りんかくは右下だけ（こい色）、左上のふちは光、深い影の中はまぜない。
足もとは、フィールドの草原（ground_tex.py の草）と同じ色の草の葉先と、うすく透ける影でなじませる。どれも 48×48。

  icon-shrine   祠: 街道わきの西洋風の小さな礼拝堂（しっくいの壁とすみ石・半円アーチの入口・かわら屋根・鐘つき・三つの環の石の帯・鉄の街灯）
  icon-cave     洞窟: 草におおわれた岩山の、ななめの地層とひび。まんなか下に、奥ほど暗くなる洞窟の口（口のまわりの石は光を受ける）。
                上と根もとに草、こけ
  icon-bigtree  森: 新しい木と同じ描き方の木を3本、奥から手前へ重ね、根もとに茂み。木ごとに葉の色を少しかえる
書き出し: icon-shrine.txt / icon-cave.txt / icon-bigtree.txt と pal-*.json（前の絵を上書き）。"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
S = 48
L = np.array([-0.55, -0.62, 0.56])
L = L / np.linalg.norm(L)

LEAF = ["#1e3328", "#2b4a34", "#3b6236", "#557f3a", "#7ea447", "#b0c862"]
LEAF2 = ["#1c3026", "#28452f", "#355a31", "#4b7435", "#6d9541", "#9cba58"]   # 少し青みの木
LEAF_OUT = "#14241c"
BARK = ["#2e2119", "#4e3727", "#6e4f35", "#94704b"]
STONE = ["#2a2a34", "#3c3c48", "#52525e", "#6a6874", "#82808a", "#9a97a0", "#b2aeb2", "#c8c4c2", "#dcd8d0"]   # 影は青み、光は黄み
STONE_OUT = "#1a1a22"
ROCK = ["#2a2420", "#3a322a", "#4c4236", "#5e5242", "#72644e", "#86765c", "#9a8a6c", "#b09e80", "#c6b494"]
MOSS = ["#2c4426", "#3e5c2e", "#557a38"]
GRASS = ["#26402a", "#37572f", "#4b7137", "#628a40", "#7da24d", "#a0bb62"]          # ground_tex.py の草と同じ段
SHADOW = ["#18301c58", "#18301c90"]
FLAME = ["#c75a2a", "#f2a544", "#f9edb3", "#fffdf2"]


def hn(*a):
    n = 2166136261
    for v in a:
        n = ((n ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    n ^= n >> 15
    return n


def rnd(*a):
    return (hn(*a) & 0xFFFF) / 65535


def new():
    return np.full((S, S), "", dtype=object)


def pick(ramp, v):
    return ramp[int(np.clip(round(v), 0, len(ramp) - 1))]


def outline_br(img, col, only=None):
    """右下のふちだけに、こい色のりんかく。"""
    solid = lambda x, y: 0 <= x < S and 0 <= y < S and img[y, x] and len(img[y, x]) == 7
    add = []
    for y in range(S):
        for x in range(S):
            if not img[y, x] and (solid(x - 1, y) or solid(x, y - 1)):
                add.append((x, y))
    for x, y in add:
        img[y, x] = col


def ground(img, x0, x1, gy, seed, dark=False):
    """足もとの、うすく透ける横長の影と、草の葉先（フィールドの草と同じ色）。"""
    cx, rx = (x0 + x1) / 2 + 1.5, (x1 - x0) / 2 + 3
    for y in range(gy - 2, min(S, gy + 3)):
        for x in range(int(cx - rx - 1), int(cx + rx + 2)):
            if not (0 <= x < S) or img[y, x]:
                continue
            e = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - gy) / 2.2) ** 2 + (rnd(x, y, seed) - 0.5) * 0.15
            if e < 1:
                img[y, x] = SHADOW[1] if (e < 0.45 or dark) else SHADOW[0]
    for k in range(int((x1 - x0) * 0.7)):
        x = int(x0 - 2 + rnd(k, seed, 3) * (x1 - x0 + 4))
        h = 1 + hn(k, seed, 4) % 3
        for t in range(h):
            y = gy + 1 - t - (hn(k, seed, 5) % 2)
            if 0 <= x < S and 0 <= y < S:
                img[y, x] = GRASS[min(5, 2 + t + hn(k, seed, 6) % 2)]


# ===================================================================== 森（木を3本）
def paint_tree(img, cx, gy, R, seed, leaf):
    """新しい木（tree2d.py）と同じ描き方の木を1本。cx: 幹のまんなか、gy: 根もとの高さ、R: 樹冠の半径。"""
    CY = gy - R * 1.45
    RX, RY = R, R * 0.92
    # 幹（根もとが広がる。右は影。樹冠のすぐ下は暗い）
    for y in range(int(CY), gy + 1):
        t = (gy - y) / max(1, gy - CY)
        w = max(1.2, R * 0.16) * (1 + 0.6 * (1 - t) ** 3)
        for x in range(int(cx - w - 1), int(cx + w + 2)):
            u = (x + 0.5 - cx) / w
            if abs(u) > 1 or not (0 <= x < S):
                continue
            k = 0 if u > 0.55 else 1 if u > 0.0 else 2 if u > -0.6 else 3
            if y < CY + RY * 0.95 + 3:
                k = max(0, k - 1)
            img[y, x] = BARK[k]
    # 房（大きいかたまり＋ふちの小さなでこぼこ）
    big = [(-0.48, -0.42, 0.42), (0.22, -0.6, 0.44), (0.62, -0.1, 0.38), (-0.62, 0.12, 0.38), (-0.08, 0.05, 0.46), (0.34, 0.38, 0.4), (-0.36, 0.48, 0.36)]
    clumps = [(cx + dx * RX, CY + dy * RY, r * R, 5 - 0.1 * math.hypot(dx, dy) * R + rnd(i, seed) * 1.5) for i, (dx, dy, r) in enumerate(big)]
    for k in range(14):
        a = k / 14 * 2 * math.pi + rnd(k, seed, 2) * 0.3
        rr = R * (0.12 + rnd(k, seed, 3) * 0.12)
        clumps.append((cx + math.cos(a) * (RX - rr * 0.9), CY + math.sin(a) * (RY - rr * 0.9), rr, 1 + rnd(k, seed, 4)))
    hgt = np.full((S, S), -1e9)
    own = np.full((S, S), -1, dtype=int)
    for i, (x, y, r, z) in enumerate(clumps):
        lobes = max(3, int(r / 1.4))
        for py in range(int(y - r - 1), int(y + r + 2)):
            for px in range(int(x - r - 1), int(x + r + 2)):
                if not (0 <= px < S and 0 <= py < S):
                    continue
                ang = math.atan2(py + 0.5 - y, px + 0.5 - x)
                re = r * (1 + 0.1 * math.sin(ang * lobes + i * 1.7))
                d = math.hypot(px + 0.5 - x, py + 0.5 - y)
                if d < re:
                    h = z + math.sqrt(re * re - d * d)
                    if h > hgt[py, px]:
                        hgt[py, px] = h
                        own[py, px] = i
    TH = [0.24, 0.36, 0.49, 0.64, 0.84]
    for py in range(S):
        for px in range(S):
            if own[py, px] < 0:
                continue
            gx, gyy = (px + 0.5 - cx) / RX, (py + 0.5 - CY) / RY
            gz = math.sqrt(max(0.05, 1 - min(1, gx * gx + gyy * gyy)))
            g = np.array([gx, gyy, gz]); g /= np.linalg.norm(g)
            x, y, r, z = clumps[own[py, px]]
            lx, ly = (px + 0.5 - x) / r, (py + 0.5 - y) / r
            l3 = np.array([lx, ly, math.sqrt(max(0, 1 - lx * lx - ly * ly))])
            n = 0.45 * g + 0.55 * l3; n /= np.linalg.norm(n)
            v = 0.18 + 0.72 * max(0.0, float(n @ L)) - 0.14 * max(0.0, gyy)
            for s in (1, 2, 3):
                qx, qy = int(round(px - s * 0.6)), py - s
                if 0 <= qx < S and 0 <= qy < S and own[qy, qx] >= 0 and own[qy, qx] != own[py, px] and hgt[qy, qx] > hgt[py, px] + 0.6 + s * 0.3:
                    v -= 0.26
                    break
            v += ((hn(px // 2, py // 2, seed) % 5) - 2) * 0.015
            k = sum(v > t for t in TH)
            if k in (3, 4) and hn(px, py, seed, 51) % 9 == 0:
                k += 1
            img[py, px] = leaf[k]
    # 樹冠のふち: 右下はりんかく、左上は光
    for py in range(S):
        for px in range(S):
            if own[py, px] >= 0:
                continue
            nb = [(px - 1, py), (px, py - 1)]
            if any(0 <= a < S and 0 <= b < S and own[b, a] >= 0 for a, b in nb) and ((px - cx) / RX + (py - CY) / RY) > -0.2:
                if not img[py, px] or img[py, px] in BARK:
                    img[py, px] = LEAF_OUT


def forest():
    img = new()
    paint_tree(img, 29, 37, 11.5, 3, LEAF2)          # 奥の木（右うしろ、少し青み）
    paint_tree(img, 14, 41, 10.0, 7, LEAF)           # 左の木
    paint_tree(img, 31, 45, 9.0, 11, LEAF)           # 手前の木
    # 根もとの茂み（小さなかたまり）
    for (bx, by, r, sd) in ((7, 43, 3.6, 21), (22, 44, 3.2, 22), (41, 44, 3.4, 23)):
        for y in range(int(by - r - 1), int(by + 2)):
            for x in range(int(bx - r - 1), int(bx + r + 2)):
                if not (0 <= x < S and 0 <= y < S):
                    continue
                d = math.hypot((x + 0.5 - bx) / r, (y + 0.5 - by) / (r * 0.8)) + (rnd(x, y, sd) - 0.5) * 0.25
                if d < 1 and y <= by:
                    v = 3.4 - (x - bx) / r * 1.2 - (y - by + r) / r * 0.3 + (1 - d) * 0.6
                    img[y, x] = pick(LEAF, v)
    ground(img, 6, 42, 45, 31)
    outline_br(img, LEAF_OUT)
    return img


# ===================================================================== 祠
GOLD = ["#5a3a10", "#8a5e1a", "#b8862c", "#e0b248", "#f6dc8a"]


WOOD = ["#2a1810", "#3e2416", "#56341e", "#704628", "#8c5a32", "#a8703e", "#c08a50", "#d4a468"]
PLASTER = ["#4e4a40", "#6c6557", "#8a8170", "#a89d87", "#c4b89e", "#dcd0b4", "#efe4c8"]   # しっくいの壁（影は青み、光は黄み）
TILE = ["#3a1a14", "#5a2a1c", "#7a3a22", "#98482a", "#b45a34", "#cc7244", "#e08e5c"]      # 素焼きのかわら
IRON = ["#15161a", "#26282e", "#383c44", "#4e5460", "#6e7682"]
GLOW = ["#5a3418", "#a8642a", "#e8a850", "#f8dc98"]
GOLD = ["#5a3a10", "#8a5e1a", "#b8862c", "#e0b248", "#f6dc8a"]


def shrine():
    """街道わきの、西洋風の小さな礼拝堂（2026-10-06 人間の指示「和じゃなくて洋にして」で、和風の祠から描きなおした）。
    しっくいの白い壁に、角は切り石（すみ石）。正面は半円アーチの入口で、くさび石のアーチが囲む。中は暗く、ろうそくの灯りがもれる。
    入口の上に石の帯をめぐらせ、三つの環を金で彫る。屋根は素焼きのかわら（手前へ傾く。左が明るく、右は影。こけ）。
    棟の上に、小さなアーチの鐘つき（中に金色の鐘）。石の段と、両わきの鉄の街灯。右の壁につたがからむ。"""
    img = new()
    CX = 23.5
    # ---- 鐘つき（棟の上に立つ、小さな石のアーチ。中に鐘。下のほうは屋根にかくれる） ----
    BX0, BX1, BY0, BY1 = 19, 28, 3, 12
    for y in range(BY0, BY1 + 1):                                         # 石の壁（左は光、右は影。目地）
        for x in range(BX0, BX1 + 1):
            v = 7.4 - (x - BX0) / (BX1 - BX0) * 3.2
            if (y - BY0) % 3 == 0:
                v -= 1.5
            if hn(x, y, 103) % 9 == 0:
                v -= 0.5
            img[y, x] = pick(STONE, v)
    BCX, BCY, BR = 23.5, 7.0, 2.6                                         # アーチの中（暗がり）
    for y in range(BY0 + 1, BY1 + 1):
        for x in range(BX0 + 1, BX1):
            ins = (BX0 + 2 <= x <= BX1 - 2) if y >= BCY else math.hypot(x + 0.5 - BCX, y + 0.5 - BCY) <= BR
            if ins:
                img[y, x] = "#16161e" if y < BCY + 1 else "#101016"
    for y in range(5, 11):                                                # 鐘（上は細く下は広がる。左上が光る）
        w = 0.7 + (y - 5) * 0.38
        for x in range(21, 27):
            if abs(x + 0.5 - BCX) <= w:
                lit = x + 0.5 < BCX
                img[y, x] = GOLD[4 if lit and y < 9 else 3 if lit else 2 if y < 9 else 1]
    img[4, 23] = IRON[4]; img[4, 24] = IRON[2]                            # 鐘をつるす横木
    for x in range(17, 31):                                               # 鐘つきの屋根（小さなきりづま。2段の厚み）
        top = int(1 + abs(x + 0.5 - BCX) * 0.26)
        left = x + 0.5 < BCX
        img[top, x] = pick(STONE, 8.4 if left else 5.8)
        img[top + 1, x] = pick(STONE, 6.4 if left else 3.6)
        if top + 2 <= BY0 and BX0 <= x <= BX1:
            img[top + 2, x] = pick(STONE, 3.0)                            # 軒の下の影
    img[0, 23] = GOLD[3]; img[0, 24] = GOLD[1]                            # 棟の先の飾り
    # ---- かわら屋根（手前へ傾く面。段ごとのかわらと、まるい先） ----
    RX0, RX1, RY0, RY1 = 8, 39, 11, 20
    def eaves(y):
        """屋根の左右のはし（上ほど少しせまい＝手前へ傾いて見える）。"""
        t = (y - RY0) / (RY1 - RY0)
        return int(round(RX0 + 1 - t * 1)), int(round(RX1 - 1 + t * 1))
    for y in range(RY0, RY1 + 1):
        t = (y - RY0) / (RY1 - RY0)
        xl, xr = eaves(y)
        for x in range(xl, xr + 1):
            u = (x - xl) / max(1, xr - xl)
            v = 5.6 - u * 2.0 - t * 0.9                                   # 上ほど空の光を受けて明るい
            col = (x - RX0) % 3
            if col == 0:
                v -= 1.5                                                  # かわらとかわらのすじ（たて）
            elif col == 1:
                v += 0.6                                                  # かわらの丸い背の光
            if (y - RY0) % 3 == 0:
                v -= 1.2 + (0.8 if col == 0 else 0)                       # 段の下のふち（影。かわらの先はまるい）
            elif (y - RY0) % 3 == 1:
                v += 0.5                                                  # 段の上のふち（光）
            if hn(x // 3, (y - RY0) // 3, 91) % 7 == 0:
                v -= 0.8                                                  # 焼きむら（かわら1枚ごと）
            if hn(x, y, 92) % 19 == 0 and t > 0.35 and u > 0.1:
                img[y, x] = MOSS[2 if u < 0.5 else 1]                     # こけ
                continue
            if x in (xl, xl + 1):
                v += 0.7                                                  # 左のはし（光）
            if x >= xr - 1:
                v -= 1.0                                                  # 右のはし（影）
            img[y, x] = pick(TILE, v)
    xl, xr = eaves(RY0)
    for x in range(xl - 1, xr + 2):                                       # 棟のかわら（いちばん上。まるい）
        img[RY0 - 1, x] = pick(TILE, 6.2 - (x - xl) / max(1, xr - xl) * 2.0 - (1.2 if (x % 3 == 0) else 0))
    xl, xr = eaves(RY1)
    for x in range(xl - 1, xr + 2):                                       # 軒（かわらの先と、その下の暗い影）
        img[RY1 + 1, x] = pick(TILE, 3.2 - (x - xl) / max(1, xr - xl) * 1.6) if (x - RX0) % 3 else pick(TILE, 1.0)
        img[RY1 + 2, x] = pick(STONE, 1.6)
    # ---- しっくいの壁（角は切り石） ----
    bx0, bx1, by0, by1 = 11, 36, 23, 41
    for y in range(by0, by1 + 1):
        for x in range(bx0, bx1 + 1):
            u = (x - bx0) / (bx1 - bx0)
            quoin = x <= bx0 + 2 or x >= bx1 - 2
            if quoin:
                row = (y - by0) // 3
                inner = (x == bx0 + 2 or x == bx1 - 2)
                v = (7.0 if x <= bx0 + 2 else 4.4) - (0.9 if inner else 0)
                if row % 2 == 0 and inner:
                    v = 6.0 if x <= bx0 + 2 else 3.6                      # 1段おきに、石が内がわへ出る
                if (y - by0) % 3 == 0:
                    v -= 1.6                                              # すみ石の目地
                if hn(x, y, 93) % 9 == 0:
                    v -= 0.5
                img[y, x] = pick(STONE, v)
            else:
                v = 5.6 - u * 1.8 - max(0.0, (y - 34) * 0.07)
                if hn(x // 2, y // 2, 94) % 7 == 0:
                    v -= 0.4                                              # しっくいのむら
                if hn(x, y, 95) % 23 == 0:
                    v -= 0.9                                              # 小さな欠け
                img[y, x] = pick(PLASTER, v)
    for x in range(bx0, bx1 + 1):                                         # 軒の下の、壁に落ちる影
        for y in (by0, by0 + 1):
            c = img[y, x]
            ramp = STONE if c in STONE else PLASTER
            img[y, x] = ramp[max(0, ramp.index(c) - (2 if y == by0 else 1))]
    for x in range(bx0, bx1 + 1):                                         # 根もとの石の帯（水切り）
        for y in (by1 - 1, by1):
            img[y, x] = pick(STONE, (6.6 if y == by1 - 1 else 4.4) - (x - bx0) / (bx1 - bx0) * 1.8)
    # ---- 入口（半円アーチ。くさび石の囲み・中の灯り・木の扉） ----
    DX0, DX1, SPR, R = 20, 27, 34.0, 4.0
    def inside(x, y):
        if y >= SPR:
            return DX0 <= x <= DX1
        return math.hypot(x + 0.5 - CX, y + 0.5 - SPR) <= R
    for y in range(int(SPR - R - 3), by1 + 1):
        for x in range(DX0 - 3, DX1 + 4):
            if not (0 <= x < S and 0 <= y < S):
                continue
            if inside(x, y):
                d = math.hypot((x + 0.5 - CX) * 1.1, (y + 0.5 - 38.5))
                g = max(0.0, 1 - d / 7.0)
                img[y, x] = ["#120e0c", "#2a1a12", "#60381a", GLOW[1]][3 if g > 0.78 else 2 if g > 0.52 else 1 if g > 0.26 else 0]
                continue
            dd = math.hypot(x + 0.5 - CX, y + 0.5 - SPR)
            arch = y < SPR and R < dd <= R + 2.4
            jamb = y >= SPR and (DX0 - 3 < x < DX0 or DX1 < x < DX1 + 3)
            if arch or jamb:
                a = math.atan2(SPR - (y + 0.5), x + 0.5 - CX)
                v = 7.6 - (x - (DX0 - 3)) / 14 * 2.8
                if arch and (int((a + 3.2) * 3.6) % 2 == 0):
                    v -= 1.5                                              # くさび石の目地（放射状）
                if jamb and (y - int(SPR)) % 3 == 0:
                    v -= 1.5
                if hn(x, y, 96) % 13 == 0:
                    v -= 0.5
                img[y, x] = pick(STONE, v)
    for x in range(DX0, DX1 + 1):                                         # 入口の下の、すり減った石の敷居
        img[by1, x] = pick(STONE, 6.2 - (x - DX0) * 0.2)
    for x in range(DX0 + 1, DX1):                                         # 中の祭壇（石の台）
        img[39, x] = pick(STONE, 4.6 - (x - DX0) * 0.3)
        img[40, x] = pick(STONE, 2.6)
    for (x, y, k) in ((23, 38, 1), (24, 38, 1), (23, 37, 2), (24, 37, 1), (23, 36, 3), (23, 35, 2), (24, 36, 1)):
        img[y, x] = FLAME[k]                                              # ろうそくのほのお
    # ---- 入口の上の、三つの環を彫った石の帯 ----
    for y in range(24, 29):
        for x in range(bx0 + 3, bx1 - 2):
            v = (7.8 if y == 24 else 6.8 if y < 28 else 4.6) - (x - bx0) / (bx1 - bx0) * 2.0
            if (x - bx0) % 5 == 0 and 24 < y < 28:
                v -= 1.2                                                  # 帯の石の継ぎ目
            if hn(x, y, 104) % 13 == 0 and 24 < y < 28:
                v -= 0.5
            img[y, x] = pick(STONE, v)
    for cxr in (18.0, 23.5, 29.0):
        for y in range(24, 29):
            for x in range(int(cxr) - 2, int(cxr) + 3):
                d = math.hypot(x + 0.5 - cxr, y + 0.5 - 26.3)
                if 0.85 <= d < 1.75:
                    lit = (x + 0.5 - cxr) + (y + 0.5 - 26.3) < 0
                    img[y, x] = GOLD[4 if lit else 2]
                elif d < 0.85:
                    img[y, x] = pick(STONE, 3.4)                          # 輪の中（彫った影）
    # ---- 右の壁をのぼる、つた ----
    for k in range(26):
        x = 33 + hn(k, 97) % 3
        y = 40 - k - hn(k, 98) % 2
        if by0 + 2 < y < by1 - 1:
            img[y, x] = MOSS[1 + hn(k, 99) % 2]
            if hn(k, 100) % 2 == 0 and x - 1 > bx0:
                img[y, x - 1] = MOSS[hn(k, 101) % 2]
    # ---- 石の段（2段） ----
    for (y0, y1, x0, x1) in ((44, 46, 9, 38), (42, 44, 13, 34)):
        for y in range(y0, y1):
            for x in range(x0, x1 + 1):
                u = (x - x0) / (x1 - x0)
                v = (7.2 if y == y0 else 5.0) - u * 2.0 - (0.8 if y == y1 - 1 else 0)
                if (x - x0 + (3 if y0 == 44 else 0)) % 9 == 0 and y > y0:
                    v -= 1.7
                if hn(x, y, 102) % 11 == 0:
                    v -= 0.6
                img[y, x] = pick(STONE, v)
    # ---- 両わきの鉄の街灯（ガラスの中に灯り） ----
    def lamp(cx):
        for y in range(31, 45):
            img[y, cx] = IRON[3] if y % 6 else IRON[4]
            img[y, cx + 1] = IRON[1]
        for x in range(cx - 1, cx + 3):                                   # 台
            img[44, x] = IRON[2 if x <= cx else 1]
            img[45, x] = IRON[1]
        for y in range(27, 31):                                           # 火袋（鉄の枠とガラス）
            for x in range(cx - 1, cx + 3):
                edge = x in (cx - 1, cx + 2) or y == 30
                img[y, x] = IRON[3 if x <= cx else 1] if edge else GLOW[3 if y == 28 else 2]
        for x in range(cx - 2, cx + 4):                                   # かさ
            img[26, x] = IRON[4 if x <= cx else 2]
        img[25, cx] = IRON[3]; img[25, cx + 1] = IRON[1]
    lamp(5)
    lamp(40)
    ground(img, 8, 40, 46, 41)
    outline_br(img, STONE_OUT)
    return img


# ===================================================================== 洞窟
def cave():
    img = new()
    ys, xs = np.mgrid[0:S, 0:S]
    # 岩山の高さ（いくつかの丸いふくらみ）
    h = np.zeros((S, S))
    for (bx, by, rx, ry, a) in ((24, 30, 20, 17, 1.0), (14, 34, 11, 10, 0.7), (35, 33, 11, 11, 0.75), (26, 18, 10, 9, 0.6)):
        d = ((xs + 0.5 - bx) / rx) ** 2 + ((ys + 0.5 - by) / ry) ** 2
        h = np.maximum(h, np.where(d < 1, a * np.sqrt(np.clip(1 - d, 0, 1)) * 14, 0))
    h = np.where(h > 0, h + np.array([[rnd(x // 3, y // 2, 4) for x in range(S)] for y in range(S)]) * 1.4, 0)   # ごつごつ（岩山の中だけ）
    mask = (h > 0.6) & (ys < 44)
    dx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) * 0.5
    dy = (np.roll(h, -1, 0) - np.roll(h, 1, 0)) * 0.5
    for y in range(S):
        for x in range(S):
            if not mask[y, x]:
                continue
            n = np.array([-dx[y, x], -dy[y, x], 1.6]); n /= np.linalg.norm(n)
            v = 1.6 + 6.2 * max(0.0, float(n @ L))
            # ななめの地層（少し右上がり）と、ひび
            band = (y * 1.0 - x * 0.18 + math.sin(x * 0.35) * 1.2) % 4.5
            if band < 0.7:
                v -= 1.4
            elif band < 1.4:
                v += 0.5
            if hn(x // 2, y, 6) % 23 == 0:
                v -= 1.6
            img[y, x] = pick(ROCK, v)
            # 上の面の草とこけ（上を向いて光を受ける所）
            if -dy[y, x] > 0.9 and n @ L > 0.55 and hn(x, y, 8) % 3 != 0:
                img[y, x] = GRASS[3 if v > 5 else 2]
            elif -dy[y, x] > 0.5 and hn(x, y, 9) % 7 == 0:
                img[y, x] = MOSS[1]
    # 洞窟の口（まんなか下。上はまるく、奥ほど暗い。口のまわりの石は光を受ける）
    mx, mtop, mbot, mw = 25.0, 27, 43, 7.5
    for y in range(mtop - 2, mbot + 1):
        for x in range(int(mx - mw - 2), int(mx + mw + 3)):
            if not (0 <= x < S):
                continue
            t = (y - mtop) / (mbot - mtop)
            half = mw * math.sqrt(max(0.0, min(1.0, (y - mtop + 1) / 5.0))) if y < mtop + 5 else mw
            half += (rnd(y, 11) - 0.5) * 1.0
            d = abs(x + 0.5 - mx)
            if d < half:
                depth = 1 - d / max(1, half)
                k = 0 if depth > 0.35 or t < 0.5 else 1
                if y > mbot - 3 and depth < 0.5:
                    k = 2                                                  # 口の床（少し見える）
                img[y, x] = ["#0c0908", "#16110e", "#2a221a"][k]
            elif d < half + 1.5 and mask[y, x]:
                img[y, x] = pick(ROCK, 7.6 if x < mx else 3.0)              # 口のふちの石（左は光、右は影）
    # 根もとの草とこけ
    for x in range(4, 45):
        for y in range(40, 45):
            if mask[y, x] and img[y, x] in ROCK and hn(x, y, 12) % 3 == 0 and not (abs(x + 0.5 - mx) < mw + 1):
                img[y, x] = GRASS[2 + hn(x, y, 13) % 2]
    ground(img, 4, 44, 44, 51, dark=True)
    outline_br(img, "#1a1410")
    return img


def save(img, name):
    cols = sorted({c for c in img.flatten().tolist() if c})
    syms = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    assert len(cols) <= len(syms), (name, len(cols))
    cmap = {c: syms[i] for i, c in enumerate(cols)}
    open(os.path.join(HERE, name + ".txt"), "w").write("\n".join("".join(cmap[img[y, x]] if img[y, x] else "." for x in range(S)) for y in range(S)) + "\n")
    json.dump({cmap[c]: c for c in cols}, open(os.path.join(HERE, "pal-" + name + ".json"), "w"))
    print(name, len(cols), "colors")


if __name__ == "__main__":
    save(forest(), "icon-bigtree")
    save(shrine(), "icon-shrine")
    save(cave(), "icon-cave")
