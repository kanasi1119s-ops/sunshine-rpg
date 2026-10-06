"""全体フィールドに置く目印の絵（祠・洞窟・森）を、1から描きなおす（2026-10-06、人間の指示「フィールドオブジェクト小屋以外1から作り直し
祠、洞窟、森、フィールドになじむよう、リアルに細かく、光も気にしてドットも一つ一つ細かく使い作り直して」）。
新しい木（tree2d.py）と同じ技法: 形全体に左上から光を当て、そのうえで面ごと・かたまりごとに明暗をつける。重なりの影、色相のずれ
（明るい所は黄色寄り、影は青寄り）、りんかくは右下だけ（こい色）、左上のふちは光、深い影の中はまぜない。
足もとは、フィールドの草原（ground_tex.py の草）と同じ色の草の葉先と、うすく透ける影でなじませる。どれも 48×48。

  icon-shrine   祠: 石を積んだ2本の柱と、その上の石の環（この世界のしるし「環」）。中に小さな石の台と、ともった灯り（灯りのまわりがほんのり明るい）。
                石の段2つ、石の目地・欠け・こけ、根もとの草
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
def shrine():
    img = new()
    # 石の段（2段）
    for (y0, y1, x0, x1) in ((42, 45, 7, 40), (39, 42, 10, 37)):
        for y in range(y0, y1):
            for x in range(x0, x1 + 1):
                v = 5.4 - (x - x0) / (x1 - x0) * 1.8 + (1.6 if y == y0 else 0) - (0.8 if y == y1 - 1 else 0)
                if (x - x0 + (y0 // 3) * 4) % 9 == 0 and y > y0:
                    v -= 1.6                                              # 石の目地
                if hn(x, y, 5) % 13 == 0:
                    v -= 0.8
                img[y, x] = pick(STONE, v)
    # 柱（石を積む。左の柱は光の側、右の柱は少し暗い）
    def pillar(x0, x1, top, lit):
        for y in range(top, 39):
            row = (y - top) // 4
            for x in range(x0, x1 + 1):
                u = (x - x0) / (x1 - x0)
                v = (6.4 if lit else 5.2) - u * 2.6
                if (y - top) % 4 == 0:
                    v = v - 1.8 if y > top else v + 1.2                    # 石と石の目地（いちばん上は光）
                elif (y - top) % 4 == 1:
                    v += 0.6                                               # 石の上のふちの光
                if x == x0:
                    v += 0.8
                if hn(x, row, x0) % 11 == 0 and (y - top) % 4 == 2:
                    v -= 1.0                                               # 欠け
                img[y, x] = pick(STONE, v)
            if hn(row, x0, 7) % 3 == 0 and (y - top) % 4 == 3:
                img[y, x1 - 1] = MOSS[1]                                   # 目地のこけ
    pillar(11, 16, 17, True)
    pillar(31, 36, 17, False)
    # 石の環（柱の上。環の左上は光、右下は影。内がわのふちは暗い）
    cx, cy, R0, R1 = 23.8, 13.0, 8.0, 12.6
    for y in range(0, 24):
        for x in range(6, 42):
            dx, dy = x + 0.5 - cx, (y + 0.5 - cy) * 1.05
            d = math.hypot(dx, dy)
            if R0 <= d <= R1 and not (y > 17 and (x < 11 or x > 36)):
                t = (d - R0) / (R1 - R0)                                  # 0=内がわ 1=外がわ
                nx, ny = dx / d, dy / d
                # 環の断面はまるい: まんなかが手前に出る
                bulge = math.sin(t * math.pi)
                n = np.array([nx * (1 - bulge) * (1 if t > 0.5 else -1), ny * (1 - bulge) * (1 if t > 0.5 else -1), bulge + 0.3])
                n /= np.linalg.norm(n)
                v = 1.2 + 7.0 * max(0.0, float(n @ L))
                seg = int((math.atan2(dy, dx) + math.pi) / (2 * math.pi) * 12)
                if abs(((math.atan2(dy, dx) + math.pi) / (2 * math.pi) * 12) - round((math.atan2(dy, dx) + math.pi) / (2 * math.pi) * 12)) < 0.06:
                    v -= 1.8                                               # 環を組んだ石の継ぎ目
                if hn(seg, 3) % 4 == 0 and t > 0.7 and ny < -0.3:
                    img[y, x] = MOSS[2 if v > 5 else 1]                    # 上のこけ
                    continue
                img[y, x] = pick(STONE, v)
    # 中の石の台と、ともった灯り（台のまわりが、ほんのり明るい）
    for y in range(31, 39):
        for x in range(20, 28):
            v = 6.2 - (x - 20) / 8 * 2.4 + (1.4 if y == 31 else 0)
            img[y, x] = pick(STONE, v)
    for y in range(29, 31):
        for x in range(22, 26):
            img[y, x] = pick(STONE, 7.2 - (x - 22) * 0.6)                 # 灯りの皿
    for (x, y, k) in ((23, 28, 1), (24, 28, 1), (23, 27, 2), (24, 27, 1), (23, 26, 2), (23, 25, 3), (24, 26, 0)):
        img[y, x] = FLAME[k]
    for y in range(22, 33):                                               # 灯りの照り（柱の内がわ・台の上）
        for x in range(17, 31):
            if img[y, x] in STONE:
                d = math.hypot(x - 23.5, y - 27)
                if d < 7 and hn(x, y, 9) % 2 == 0:
                    k = STONE.index(img[y, x])
                    img[y, x] = STONE[min(8, k + 1)] if d < 4.5 else img[y, x]
    ground(img, 6, 41, 45, 41)
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
