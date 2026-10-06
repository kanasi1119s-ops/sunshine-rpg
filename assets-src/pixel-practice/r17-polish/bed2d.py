"""ベッドを、布団までリアルに描きなおす（2026-10-06、人間の指示「ベッドは布団もリアルな感じにして」）。
新しい木（tree2d.py）と同じ技法で、1ドットずつ描く。光は左上から。

  - 木の枠: 頭の板（たての細い板・上の横木）、左右の柱（頭つき）、足もとの板。左の面は明るく、右の面は影
  - 枕: ふっくらしたかたまり（左上が明るく、右下と下のふちが暗い）。まんなかに、くぼみのしわ
  - 折り返したシーツ: 掛け布団の上のはしを、白いシーツで折り返した帯（帯の下に細い影）
  - 掛け布団: 青いキルト。やわらかいしわ（なだらかな山と谷）。山の左の面は光を受け、右の面は影。縫い目の線も、しわにそってゆがむ
    左右のはしは、ベッドのふちから少したれる（すその波）。足もとの板の上に、布団のはしがかぶさる
  - 色は、明るい所ほど黄色寄り、暗い所ほど青寄り。りんかくは右下だけ（こい色）。床に、うすく透ける影
書き出し: ../r20-props/bed.txt / pal-bed.json（prop:bed。家の中のベッドすべて）。"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
R20 = os.path.join(HERE, "..", "r20-props")
W, H = 34, 32
WOOD = ["#1e1210", "#2c1a14", "#3e2618", "#53341e", "#6a4426", "#83562e", "#9c6a38", "#b48044", "#c99854", "#dbb06a"]
CLOTH = ["#6e7286", "#868a9c", "#a0a3b2", "#b9bbc6", "#cfd0d6", "#e1e1e2", "#efede8", "#faf7ee", "#fffdf6"]   # 白い布（影は青み、光は黄み）
BLUE = ["#1a2a50", "#223864", "#2c4878", "#38598e", "#466ca4", "#5880b8", "#6e96c8", "#88acd6"]
OUT = "#1a100c"
SHADOW = ["#10181440", "#10181470"]


def hn(*a):
    n = 2166136261
    for v in a:
        n = ((n ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    n ^= n >> 15
    return n


def pick(ramp, v):
    return ramp[int(np.clip(round(v), 0, len(ramp) - 1))]


img = np.full((H, W), "", dtype=object)
XL, XR = 3, 30                 # 枠の柱の内がわ
HEAD_B = 10                    # 頭の板の下のはし
FOOT_T = 25                    # 足もとの板の上のはし

# ---- 頭の板（奥。たての細い板と、上の横木） ----
for y in range(1, HEAD_B):
    for x in range(XL, XR + 1):
        if y <= 2:
            v = 8 - (y - 1) * 2 - (x - XL) / (XR - XL) * 1.5        # 上の横木（上の面が明るい）
        else:
            slat = (x - XL) % 4
            v = (6.4 if slat == 1 else 5.4 if slat == 2 else 3.4 if slat == 3 else 2.2) - (x - XL) / (XR - XL) * 1.4
            v -= (y - 3) * 0.12
        img[y, x] = pick(WOOD, v)

# ---- マットレスの上: 枕・折り返したシーツ・掛け布団 ----
def cloth_light(x, y):
    """布の、形全体の光: 左上ほど明るく、右下ほど暗い。"""
    return -0.9 * ((x - XL) / (XR - XL)) - 0.6 * ((y - HEAD_B) / (FOOT_T - HEAD_B))


# 枕（ふっくらしたかたまり。2つぶん横に長い）
PCX, PCY, PRX, PRY = (XL + XR) / 2, HEAD_B + 1.6, 12.2, 3.6
for y in range(HEAD_B - 3, HEAD_B + 6):
    for x in range(XL + 1, XR):
        dx, dy = (x + 0.5 - PCX) / PRX, (y + 0.5 - PCY) / PRY
        e = dx * dx * dx * dx + dy * dy                       # かどの丸い長方形
        if e > 1:
            continue
        nz = math.sqrt(max(0.0, 1 - min(1, e)))
        v = 5.6 + nz * 2.2 - dx * 1.2 - dy * 1.4 + cloth_light(x, y) * 0.8
        if abs(x + 0.5 - PCX) < 1.0 and dy > -0.4:
            v -= 1.6                                            # まんなかのくぼみ（2つの枕のさかい）
        if e > 0.78 and (dy > 0.2 or dx > 0.3):
            v -= 1.2                                            # 下と右のふち（まわりこむ影）
        img[y, x] = pick(CLOTH, v)

# 掛け布団（しわのある面）と、折り返したシーツ
SHEET_T, SHEET_B = HEAD_B + 5, HEAD_B + 7


def fold(x, y):
    """しわの高さ（なだらかな山と谷）。2本のゆるいしわが、ななめに入る。"""
    return 0.9 * math.sin(x * 0.42 + y * 0.18 + 0.6) + 0.5 * math.sin(x * 0.21 - y * 0.35 + 2.0)


for y in range(SHEET_T, FOOT_T + 2):
    # すそ: 左右のはしは、少したれる（はしが外へ1ドット出て、波うつ）
    sag = 1 if y > SHEET_B + 2 and math.sin(y * 0.9) > -0.2 else 0
    for x in range(XL - sag, XR + 1 + sag):
        h0 = fold(x, y)
        slope = fold(x + 1, y) - fold(x - 1, y)                 # 右へ上がる面は光の側を向く（左が明るい）
        L = cloth_light(x, y) - 0.9 * slope
        if y < SHEET_B:
            v = 7.0 + L * 1.2 + (0.6 if y == SHEET_T else 0)     # 折り返したシーツ（白い帯）
            img[y, x] = pick(CLOTH, v)
            continue
        if y == SHEET_B:
            img[y, x] = pick(BLUE, 1.2 + L)                      # シーツの帯が落とす細い影
            continue
        # 青い掛け布団。しわの山の左は明るく、谷は暗い。キルトの縫い目（うすい線）が、しわにそってゆがむ
        u = x + h0 * 0.9
        vv = y + h0 * 0.6
        v = 4.2 + L * 1.7 + h0 * 0.55
        if (u % 6) < 0.9 or (vv % 5) < 0.8:
            v -= 0.9                                            # 縫い目（少しへこむ）
        elif (u % 6) < 1.9 or (vv % 5) < 1.8:
            v += 0.35                                           # 縫い目のすぐ右下の、ふくらみの光
        check = 1
        img[y, x] = pick(BLUE, v)
        if x in (XL - sag, XR + sag) or (sag and x in (XL, XR)):
            img[y, x] = pick(BLUE, 2.4 + (0.7 if x < W / 2 else -0.5))   # はしのたれた面（側面は暗い）

# ---- 左右の柱と、足もとの板 ----
for y in range(0, H - 1):
    for (x, v0) in ((XL - 2, 8.2), (XL - 1, 6.4), (XR + 1, 4.2), (XR + 2, 2.6)):
        if y <= FOOT_T + 5:
            img[y, x] = pick(WOOD, v0 - (0.8 if y > FOOT_T else 0))
for x in range(XL - 2, XR + 3):                                   # 柱の頭
    img[0, x] = pick(WOOD, 9 if x < W / 2 else 6) if x in (XL - 2, XL - 1, XR + 1, XR + 2) else img[0, x]
for y in range(FOOT_T + 2, H - 2):                                # 足もとの板（手前の面）
    for x in range(XL, XR + 1):
        v = 5.6 - (x - XL) / (XR - XL) * 2.2 - (y - FOOT_T - 2) * 0.25
        if y == FOOT_T + 2:
            v = 8.4 - (x - XL) / (XR - XL) * 2                     # 上のふち（光）
        if (x - XL) % 9 == 0 and y > FOOT_T + 2:
            v -= 1.6                                               # 板の継ぎ目
        if hn(x, y // 2, 7) % 6 == 0:
            v -= 0.6                                               # 木目
        img[y, x] = pick(WOOD, v)

# ---- りんかく（右下だけ）と、床の影 ----
solid = lambda x, y: 0 <= x < W and 0 <= y < H and img[y, x] and len(img[y, x]) == 7
out = img.copy()
for y in range(H):
    for x in range(W):
        if not img[y, x] and (solid(x - 1, y) or solid(x, y - 1)):
            out[y, x] = OUT
img = out
for x in range(XL - 2, min(W, XR + 5)):
    for y in (H - 2, H - 1):
        if img[y, x] == "":
            img[y, x] = SHADOW[1] if y == H - 2 else SHADOW[0]

cols = sorted({c for c in img.flatten().tolist() if c})
syms = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
cmap = {c: syms[i] for i, c in enumerate(cols)}
open(os.path.join(R20, "bed.txt"), "w").write("\n".join("".join(cmap[img[y, x]] if img[y, x] else "." for x in range(W)) for y in range(H)) + "\n")
json.dump({cmap[c]: c for c in cols}, open(os.path.join(R20, "pal-bed.json"), "w"))
print("bed", len(cols), "colors")
