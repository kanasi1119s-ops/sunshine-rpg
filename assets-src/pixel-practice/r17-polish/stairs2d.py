"""家の中の階段を、新しい木（tree2d.py）と同じ技法で描きなおす（2026-10-06、人間の指示「この階段もっとリアルにしようか。技法は木と同じで」）。

木と同じ考え方:
  - 形全体を1つのかたまりとして光を決める（左上から。下の段・手前ほど明るく、天井の口に近い上の段は暗い）
  - そのうえで、面の向きごとに明るさを分ける: 踏み板の上の面（いちばん明るい）・段の正面（蹴込み。中くらい）・階段の下の板壁（奥まって暗い）
  - 上の段の踏み板のはなが、すぐ下の蹴込みに細い影を落とす（重なりの影）。手すりの柱も、うしろへ影を落とす
  - 木目は、板の長い向きにそった、とぎれとぎれのすじ。板ごとに少し色がちがう
  - 色は明るい所ほど黄色寄り、暗い所ほど赤み・青みのある暗い茶色（色相のずれ）。深い影の中はまぜない
  - りんかくは右下だけ（こい茶色）。左上のふちには、光のふち
  - 床に接する所は、うすく透ける影

  stairs-up    48×48（3マス幅）: 奥の壁ぞいに、左から右へ上がる木の階段。親柱・手すり・細い柱、閉じた側板、階段下の板壁、天井へぬける口
  stairs-down  20×20: 床にあいた下り口。縁板（左上が明るい）、奥へ下がっていく段（奥ほど暗い）、縁板が口の中へ落とす影、左の手すり
書き出し: ../r20-props/stairs-up.txt / stairs-down.txt（stairs3d.py の版を上書き）。"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
R20 = os.path.join(HERE, "..", "r20-props")
# 木の色の段（暗→明）。暗い所は赤み・青みのある暗い茶、明るい所は黄色寄り
WOOD = ["#1e1210", "#2c1a14", "#3e2618", "#53341e", "#6a4426", "#83562e", "#9c6a38", "#b48044", "#c99854", "#dbb06a", "#ead08e"]
OUT = "#1a100c"
VOID = ["#0c0807", "#120c0a", "#1a120e"]
SHADOW = ["#10181440", "#10181470"]


def hn(*a):
    n = 2166136261
    for v in a:
        n = ((n ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    n ^= n >> 15
    return n


def grain(x, y, seed, horizontal=True):
    """木目: 板の長い向きにそった、とぎれとぎれのすじ（-1, 0, +1）。"""
    a, b = (y, x) if horizontal else (x, y)
    if hn(a, seed) % 3 == 0 and (b // 3 + hn(a, seed, 2)) % 4 != 0:
        return -1
    if hn(a, b // 5, seed, 3) % 23 == 0:
        return 1
    return 0


def save(img, name):
    H, W = img.shape
    cols = sorted({c for c in img.flatten().tolist() if c})
    syms = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    cmap = {c: syms[i] for i, c in enumerate(cols)}
    open(os.path.join(R20, name + ".txt"), "w").write("\n".join("".join(cmap[img[y, x]] if img[y, x] else "." for x in range(W)) for y in range(H)) + "\n")
    json.dump({cmap[c]: c for c in cols}, open(os.path.join(R20, "pal-" + name + ".json"), "w"))
    return len(cols)


def outline_bottom_right(img):
    """右下のふちだけに、こい茶色のりんかく。左上のふちは、1段明るい光のふち。"""
    H, W = img.shape
    solid = lambda x, y: 0 <= x < W and 0 <= y < H and img[y, x] and len(img[y, x]) == 7
    out = img.copy()
    for y in range(H):
        for x in range(W):
            if img[y, x]:
                continue
            if solid(x - 1, y) or solid(x, y - 1):                           # 形の右・下のすぐ外がわ
                out[y, x] = OUT
    for y in range(H):
        for x in range(W):
            if solid(x, y) and img[y, x] in WOOD and (not solid(x - 1, y) or not solid(x, y - 1)):
                k = WOOD.index(img[y, x])
                out[y, x] = WOOD[min(len(WOOD) - 1, k + 1)]
    return out


# ===================================================================== 上り階段
def stairs_up():
    W, H = 48, 48
    img = np.full((H, W), "", dtype=object)
    n, run, rise = 8, 5, 4                       # 段の数・1段の横はば・1段の高さ（ドット）
    x0, base = 2, 45                             # いちばん左の段の左はし・床の高さ
    tread = 3                                    # 踏み板の上の面の見えるはば（奥行き。少し上から見下ろす）

    def light(x, y):
        """形全体の光: 左下（手前・光の側）ほど明るく、右上（天井の口の近く）ほど暗い。"""
        return -0.9 * ((x - x0) / (n * run)) * 0.6 - 0.9 * ((base - y) / (n * rise)) * 0.4

    # 正面から見えるのは、階段の側面（段の形をした三角の板）と、奥の壁へのびる踏み板の上の面。段の正面（蹴込み）は横を向くので見えない
    # 1) 側面の板（光を正面から受ける。たての板と継ぎ目・木目。床に近いほど少し暗い）
    for i in range(n):
        xa = x0 + i * run
        top = base - (i + 1) * rise
        for x in range(xa, xa + run):
            for y in range(top, base + 1):
                v = 5.6 + light(x, y) * 2.0 + grain(x, y, 7, horizontal=False) * 0.7 - max(0, y - (base - 4)) * 0.35
                if (x - x0) % 5 == 4:
                    v -= 1.8                                                  # 板の継ぎ目
                elif (x - x0) % 5 == 0:
                    v += 0.6                                                  # 継ぎ目の右の、光を受けたふち
                if y == top:
                    v -= 1.4                                                  # すぐ上の踏み板のはなが落とす影
                img[y, x] = WOOD[int(np.clip(round(v), 0, 10))]
    # 2) 踏み板の上の面（奥の壁へのびる。いちばん明るい）。手前のふち（はな）は光を受けて、さらに明るい
    for i in range(n):
        xa = x0 + i * run
        top = base - (i + 1) * rise
        for x in range(xa, xa + run + (1 if i < n - 1 else 0)):
            L = light(x, top)
            for t in range(1, tread + 2):
                y = top - t
                v = 8.0 + L * 2.0 + grain(x, y, 11 + i) * 0.6 - (t - 1) * 0.5      # 奥ほど少し暗い
                if x == xa + run and i < n - 1:
                    v -= 2.5                                                  # 上の段の側のかど（奥まって暗い）
                img[y, x] = WOOD[int(np.clip(round(v), 0, 10))]
            img[top - 1, x] = WOOD[int(np.clip(round(9.3 + L * 1.6), 0, 10))]   # はな
    # 3) 天井へぬける口（いちばん上の段の上。上のふちに梁）
    for y in range(base - n * rise - tread - 10, base - n * rise - tread):
        for x in range(x0 + (n - 2) * run, x0 + n * run + 2):
            img[y, x] = VOID[1] if y > base - n * rise - tread - 9 else WOOD[3]
    # 4) 手すり: 下の親柱（3ドット幅・頭つき）、2段ごとの細い柱、ななめの手すり（2ドット: 上が明るい）
    def rail_y(x):
        return base - 12 - (x - x0 - 1) * rise / run

    for x in range(x0, x0 + n * run - 1):
        yr = int(round(rail_y(x)))
        if 0 <= yr < H - 1:
            img[yr, x] = WOOD[9]
            img[yr + 1, x] = WOOD[5]
    for i in range(0, n, 2):
        px = x0 + i * run + 2
        y_top = int(round(rail_y(px))) + 2
        y_bot = base - (i + 1) * rise - tread
        for y in range(y_top, y_bot):
            img[y, px] = WOOD[7]
            if px + 1 < W and not (img[y, px + 1] in WOOD and WOOD.index(img[y, px + 1]) <= 3):
                img[y, px + 1] = WOOD[3]                                          # 柱の右（影の側）
    for y in range(base - 15, base + 1):                                       # 親柱
        img[y, x0 - 1] = WOOD[9]
        img[y, x0] = WOOD[7]
        img[y, x0 + 1] = WOOD[4]
    for x in range(x0 - 2, x0 + 3):                                           # 親柱の頭
        img[base - 16, x] = WOOD[8] if x < x0 + 1 else WOOD[5]
        img[base - 17, x] = WOOD[10] if x < x0 + 1 else WOOD[7]
    # 5) りんかく（右下だけ）と、左上の光のふち
    img = outline_bottom_right(img)
    # 6) 床の影: 階段の右と、手前の足もとに、うすく透ける影（光は左上から）
    for y in range(base - 2, H):
        for x in range(x0, W):
            if img[y, x] == "":
                d = (y - (base + 1)) / 2.2
                if -1 <= d <= 1 and x < x0 + n * run + 4:
                    img[y, x] = SHADOW[1] if abs(d) < 0.5 else SHADOW[0]
    return img


# ===================================================================== 床の下り口
def stairs_down():
    W, H = 20, 20
    img = np.full((H, W), "", dtype=object)
    x0, x1, y0, y1 = 3, 17, 5, 18                                   # 口の外がわ（縁板をふくむ）
    # 口の中: 奥（上）へ下がっていく段。3ドットごとに1段（踏み板2・蹴込み1）。奥ほど暗い。縁板が上と左から影を落とす
    for y in range(y0 + 1, y1):
        for x in range(x0 + 1, x1):
            k = y1 - 1 - y
            step, r = k // 3, k % 3
            v = (7.4 if r == 1 else (8.4 if r == 2 else 4.2)) - step * 1.7 + grain(x, y, 31 + step) * 0.6
            if r == 2:
                v += 0.6 if x < x0 + 4 else 0                                # 段のはなの光（光の側）
            if x <= x0 + 1 or y <= y0 + 1:
                v -= 2.2                                                     # 縁板が落とす影（左と奥のふち）
            if x >= x1 - 1:
                v -= 0.8
            img[y, x] = WOOD[int(np.clip(round(v), 0, 10))] if v > 1.2 else VOID[0 if v < 0.5 else 1]
    # 縁板（四方）: 左と上（光の側）は明るく、右と下は暗い。四すみは継ぎ目
    for x in range(x0, x1 + 1):
        img[y0, x] = WOOD[9] if (x - x0) % 7 else WOOD[7]
        img[y1, x] = WOOD[5] if (x - x0) % 7 else WOOD[4]
    for y in range(y0, y1 + 1):
        img[y, x0] = WOOD[8]
        img[y, x1] = WOOD[4]
    img[y0, x0] = WOOD[10]
    # 左の手すり: 柱2本（頭つき）と横木
    for (py, h) in ((y0 - 1, 5), (y1 - 1, 5)):
        for i in range(h):
            img[py - i, 1] = WOOD[8]
            img[py - i, 2] = WOOD[5]
        img[py - h, 1] = WOOD[10]
        img[py - h, 2] = WOOD[7]
    for y in range(y0 - 4, y1 - 4):
        if img[y, 1] == "":
            img[y, 1] = WOOD[7]
            img[y, 2] = WOOD[4]
    img = outline_bottom_right(img)
    for x in range(x0, x1 + 3):                                      # 縁板の外の、うすい影
        if img[y1 + 1, x] in ("", OUT):
            img[y1 + 1, x] = SHADOW[0] if img[y1 + 1, x] == "" else OUT
    return img


if __name__ == "__main__":
    print("stairs-up", save(stairs_up(), "stairs-up"))
    print("stairs-down", save(stairs_down(), "stairs-down"))
