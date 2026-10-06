"""町の広葉樹（64×80）を、勉強ノート docs/design/tree-notes.md の手順どおりに描く（2026-10-06、人間の指示
「この木は没。作り直し、もっと木の勉強してきて」）。前の木（props3d_c.py の tree4）は、房を1つずつ丸く塗ったため
もこもこが全部同じ明るさになり、立体に見えなかった。ここでは次の順で描く。

1. シルエット: たまご形の樹冠。ふちのでこぼこは「大きな山2〜3個＋小さな山」で、左右対称にしない。
2. 樹冠全体を1つの球として、左上の光で明るさを決める（上ほど明るく、底がいちばん暗い）。
3. その上に房（カリフラワーのようなかたまり）を重ね、上の房が下の房に影を落とす。下の房は左上の頭だけ明るい。
4. 色は明るい所ほど黄色寄り、影ほど青寄り（葉は6色＋りんかく1色、幹は4色）。深い影の中はディザを使わない。
5. 房のあいだに暗いすき間を数か所。うち2か所から、暗い枝がのぞく。
6. りんかくは右下だけ（いちばん暗い青緑）。左上はりんかくなし。左上のふちに、透けた黄緑を数ドット。
7. 幹: 根元がいちばん太く根が2〜3本はう。上へ細く、少し曲がる。右側はまるごと影、樹冠のすぐ下は暗い。
8. 地面の影: 横長のでこぼこしただ円を少し右下へ。草を暗く青くした色で、うすく透ける。根元に草の葉先をかぶせる。
書き出し: tree4.txt / pal-tree.json（ゲームの prop:tree。エディタで確かめる）。"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 64, 80
LEAF = ["#1e3328", "#2b4a34", "#3b6236", "#557f3a", "#7ea447", "#b0c862"]   # 暗→明（影は青、光は黄色へ）
OUTLINE = "#14241c"
BARK = ["#2e2119", "#4e3727", "#6e4f35", "#94704b"]
SHADOW = ["#18301c70", "#18301ca8"]                                       # 地面の影（うすい／根もと）
GRASS = ["#496d36", "#5a7e40", "#6a8f48"]


def hn(*a):
    n = 2166136261
    for v in a:
        n = ((n ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    n ^= n >> 15
    return n


def rnd(*a):
    return (hn(*a) & 0xFFFF) / 65535


img = np.full((H, W), "", dtype=object)
GROUND = 76                       # 根元の地面の高さ（いちばん下の数行は、影と草の葉先）
SC = 0.88                         # 町の物の重なり判定（PROP_BOX tree）の大きさにおさまるよう、少しちぢめる
CX, CY = 31.0, 36.0               # 樹冠のまん中
RX, RY = 27.0 * SC, 25.0 * SC

# ---- 1. 房（大・中・小）を、たまご形の中にならべる -------------------------------------------
clumps = []                       # (x, y, r, z)  z は手前への出っぱり
big = [(-13, -12, 11.0), (6, -16, 12.0), (17, -3, 10.0), (-17, 3, 10.0), (-3, 1, 12.0), (9, 10, 10.5), (-10, 13, 9.5), (20, 11, 7.5)]
for i, (dx, dy, r) in enumerate(big):
    dx, dy, r = dx * SC, dy * SC, r * SC
    clumps.append((CX + dx, CY + dy, r, 6.0 - 0.15 * math.hypot(dx, dy) + rnd(i, 1) * 2))
# ふちの小さな房（でこぼこ）: 角度ごとに、大きさをばらばらに
for k in range(22):
    a = k / 22 * 2 * math.pi + rnd(k, 2) * 0.2
    rr = (3.0 + rnd(k, 3) * 3.2) * SC
    ex = RX * (1.0 + 0.06 * math.sin(a * 2 + 1.0))
    ey = RY * (1.0 - 0.08 * math.sin(a))                                  # 下がやや広い、たまご形
    x = CX + math.cos(a) * (ex - rr * 0.9)
    y = CY + math.sin(a) * (ey - rr * 0.9)
    if y > CY + RY - 6 and abs(x - CX) < 8:
        continue                                                          # 幹の上の底は少しへこませる
    clumps.append((x, y, rr, 1.0 + rnd(k, 4)))
# 中くらいの房
for k in range(14):
    a = rnd(k, 5) * 2 * math.pi
    d = 0.35 + rnd(k, 6) * 0.45
    clumps.append((CX + math.cos(a) * RX * d, CY + math.sin(a) * RY * d, (4.5 + rnd(k, 7) * 2.5) * SC, 4.0 + rnd(k, 8) * 3))

# 高さの場（房を球として、いちばん手前の面）
hgt = np.full((H, W), -1e9)
own = np.full((H, W), -1, dtype=int)
for i, (x, y, r, z) in enumerate(clumps):
    for py in range(int(y - r - 1), int(y + r + 2)):
        for px in range(int(x - r - 1), int(x + r + 2)):
            if not (0 <= px < W and 0 <= py < H):
                continue
            # 房のふちを、葉の小さなでこぼこでゆらす
            ang = math.atan2(py + 0.5 - y, px + 0.5 - x)
            lobes = max(3, int(r / 1.6))                                  # 房のふちの、小さな葉のかたまり（カリフラワー形）
            re = r * (1 + 0.09 * math.sin(ang * lobes + i * 1.7) + 0.04 * math.sin(ang * (lobes * 2 + 1) + i))
            d = math.hypot(px + 0.5 - x, py + 0.5 - y) + (rnd(px, py, 9) - 0.5) * 0.6
            if d < re:
                r_ = re
                h = z + math.sqrt(r_ * r_ - d * d)
                if h > hgt[py, px]:
                    hgt[py, px] = h
                    own[py, px] = i
mask = own >= 0

# ---- 2〜3. 光: 全体の球 ＋ 房ごとの面 ＋ 上の房から落ちる影 ---------------------------------
L = np.array([-0.55, -0.62, 0.56])
L = L / np.linalg.norm(L)
lum = np.zeros((H, W))
for py in range(H):
    for px in range(W):
        if not mask[py, px]:
            continue
        gx, gy = (px + 0.5 - CX) / RX, (py + 0.5 - CY) / RY
        gz = math.sqrt(max(0.05, 1 - min(1, gx * gx + gy * gy)))
        g = np.array([gx, gy, gz]); g /= np.linalg.norm(g)
        x, y, r, z = clumps[own[py, px]]
        lx, ly = (px + 0.5 - x) / r, (py + 0.5 - y) / r
        lz = math.sqrt(max(0.0, 1 - lx * lx - ly * ly))
        n = 0.45 * g + 0.55 * np.array([lx, ly, lz]); n /= np.linalg.norm(n)
        v = max(0.0, float(n @ L))
        v = 0.18 + 0.72 * v
        v -= 0.22 * max(0.0, (py - CY) / RY)                             # 底ほど暗い（空の光が届かない）
        # 上（光の側）の房が、この点に影を落とす
        for s in (1, 2, 3, 4, 5):
            qx, qy = int(round(px - s * 0.6)), int(py - s)
            if 0 <= qx < W and 0 <= qy < H and mask[qy, qx] and own[qy, qx] != own[py, px] and hgt[qy, qx] > hgt[py, px] + 0.8 + s * 0.35:
                v -= 0.3 if s <= 2 else 0.22
                break
        v += ((hn(px // 3, py // 2, 3) % 5) - 2) * 0.015                  # 葉のかたまりのむら（2ドット単位）
        lum[py, px] = v

# ---- 4. 色にする ------------------------------------------------------------------------
TH = [0.24, 0.36, 0.49, 0.64, 0.84]
for py in range(H):
    for px in range(W):
        if not mask[py, px]:
            continue
        v = lum[py, px]
        k = sum(v > t for t in TH)
        # 段の境目だけ、うすくまぜる（深い影の中ではまぜない）
        if k >= 2 and k < 5:
            t = TH[k - 1]
            if v - t < 0.025 and (px + py) % 2 == 0:
                k -= 1
        if k in (3, 4) and hn(px, py, 51) % 9 == 0 and lum[py, px] - TH[k - 1] > 0.05:
            k += 1                                                        # 光を受けた葉の、小さな照り（ちらす）
        elif k in (2, 3) and hn(px, py, 52) % 11 == 0:
            k -= 1                                                        # 葉と葉のあいだの、小さな暗がり
        img[py, px] = LEAF[k]

# ---- 5. 暗いすき間と、のぞく枝 ------------------------------------------------------------
gaps = [(CX + 4, CY + 8, True), (CX - 8, CY + 10, True), (CX + 13, CY + 1, False)]
for gi, (gx, gy, br) in enumerate(gaps):
    for py in range(int(gy) - 2, int(gy) + 3):
        for px in range(int(gx) - 3, int(gx) + 4):
            if 0 <= px < W and 0 <= py < H and mask[py, px]:
                e = ((px - gx) / 3.2) ** 2 + ((py - gy) / 1.9) ** 2 + (rnd(px, py, gi) - 0.5) * 0.5
                if e < 1:
                    img[py, px] = LEAF[0]
    if br:
        # 幹から、すき間へ向かって上へのびる暗い枝（2〜4ドット見える）
        sx = 1 if gx > CX else -1
        for t in range(4):
            px = int(gx) - sx * (2 - t // 2) + (0 if t < 2 else sx)
            py = int(gy) + 1 - t
            if 0 <= px < W and mask[py, px]:
                img[py, px] = BARK[2] if t >= 2 and sx < 0 else BARK[1]

# ---- 6. りんかく（右下だけ）と、左上のふちの透け ----------------------------------------
outl = np.zeros((H, W), dtype=bool)
for py in range(H):
    for px in range(W):
        if mask[py, px]:
            continue
        nb = [(px + dx, py + dy) for dx, dy in ((-1, 0), (0, -1), (-1, -1), (1, 0), (0, 1))]
        ins = [(qx, qy) for qx, qy in nb if 0 <= qx < W and 0 <= qy < H and mask[qy, qx]]
        if not ins:
            continue
        # 外側の点が、樹冠から見て右下にあるときだけ、りんかくを置く
        if any(qx < px or qy < py for qx, qy in ins) and ((px - CX) / RX + (py - CY) / RY) > -0.2:
            outl[py, px] = True
for py in range(H):
    for px in range(W):
        if outl[py, px]:
            img[py, px] = OUTLINE
        elif mask[py, px]:
            edge = any(not (0 <= px + dx < W and 0 <= py + dy < H) or not mask[py + dy, px + dx] for dx, dy in ((-1, 0), (0, -1)))
            if edge and ((px - CX) / RX + (py - CY) / RY) < -0.55 and rnd(px, py, 21) > 0.35:
                img[py, px] = LEAF[5]                                     # 光が透けた黄緑の葉先
            elif edge and ((px - CX) / RX + (py - CY) / RY) > 0.9 and img[py, px] == LEAF[0]:
                img[py, px] = LEAF[1]                                     # 影の側のふちの、ほんの少しの照り返し

# ---- 7. 幹（樹冠より先に見える部分だけ描く）---------------------------------------------
def trunk_half(y):
    t = (GROUND - y) / (GROUND - 46)                                      # 0=根元 1=上
    w = 3.2 + 1.6 * (1 - t)                                               # 上へ細く
    if y > GROUND - 4:
        w += (y - (GROUND - 4)) ** 1.6 * 0.9                              # 根張り
    return w


def trunk_cx(y):
    return CX + 1.0 + math.sin((GROUND - y) / 11.0) * 1.3                 # 少し曲がる


for py in range(40, GROUND + 1):
    c = trunk_cx(py)
    w = trunk_half(py)
    for px in range(int(c - w - 1), int(c + w + 2)):
        u = (px + 0.5 - c) / w                                            # -1（左）〜 1（右）
        if abs(u) > 1 or not (0 <= px < W):
            continue
        if mask[py, px] and img[py, px] != "":
            continue                                                      # 樹冠がかくす
        if u > 0.62:
            k = 0
        elif u > 0.05:
            k = 1                                                         # 右側はまるごと影
        elif u > -0.55:
            k = 2
        else:
            k = 3
        # 縦の樹皮のすじ（明るい側だけ）
        if k >= 2 and hn(px, 5) % 3 == 0 and hn(px, py // 3, 6) % 4 != 0:
            k -= 1
        # 樹冠のすぐ下は暗い
        top = max(qy for qy in range(H) if mask[qy, min(W - 1, max(0, px))]) if mask[:, px].any() else 0
        if py - top < 5:
            k = max(0, k - (2 if py - top < 3 else 1))
        img[py, px] = BARK[k]
    if abs(trunk_half(py) - 0) and py >= GROUND - 1:
        pass
# 根: 左右へ2〜3本、地面にはう（右の根は影）
for (dx0, dirx, ln, k) in ((-4, -1, 6, 2), (4, 1, 5, 0), (0, 1, 3, 1)):
    for t in range(ln):
        px = int(trunk_cx(GROUND) + dx0 + dirx * t)
        py = GROUND - (1 if t < ln // 2 else 0)
        if 0 <= px < W:
            img[py, px] = BARK[k] if t < ln - 1 else BARK[max(0, k - 1)]

# ---- 8. 地面の影と、根元の草の葉先 ---------------------------------------------------------
sh_cx, sh_cy = CX + 3.5, GROUND + 0.5
for py in range(GROUND - 3, H):
    for px in range(W):
        if img[py, px] != "":
            continue
        e = ((px + 0.5 - sh_cx) / 23.0) ** 2 + ((py + 0.5 - sh_cy) / 3.6) ** 2
        e += math.sin(px * 0.7) * 0.08 + (rnd(px, py, 31) - 0.5) * 0.12   # でこぼこのだ円
        if e < 1:
            img[py, px] = SHADOW[1] if abs(px + 0.5 - trunk_cx(GROUND)) < 7 and py >= GROUND else SHADOW[0]
for k in range(9):
    px = int(trunk_cx(GROUND) + (k - 4) * 2.3 + (rnd(k, 41) - 0.5) * 2)
    hgt_ = 1 + hn(k, 42) % 2
    for t in range(hgt_):
        py = H - 2 - t
        if 0 <= px < W:
            img[py, px] = GRASS[min(2, t + hn(k, 43) % 2)]

cols = sorted({c for c in img.flatten().tolist() if c})
syms = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
cmap = {c: syms[i] for i, c in enumerate(cols)}
rows = ["".join(cmap[c] if c else "." for c in img[y]) for y in range(H)]
open(os.path.join(HERE, "tree4.txt"), "w").write("\n".join(rows) + "\n")
json.dump({cmap[c]: c for c in cols}, open(os.path.join(HERE, "pal-tree.json"), "w"))
print("tree4", len(cols), "colors")
