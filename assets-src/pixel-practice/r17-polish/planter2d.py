"""町の木の根もとの、レンガの囲い（植えます）（2026-10-06、人間の指示「地面がすべて芝じゃない町は木の周りの芝の地面に
町の色に合わせたレンガの囲いを作りましょう。作り方は木の技法で」）。
新しい木（tree2d.py）と同じ技法で、1ドットずつ描く。正面の少し上から見下ろす見え方。光は左上から。

  - 囲い: だ円の輪の形の、低いレンガの壁（高さ4ドット）。上の面は笠石のレンガ（放射状の目地）。前の面は2段のレンガ積み
    （横の目地・たての目地は段ごとにずらす）。左の前は光を受け、右は影。上の面の前のふちは光の線。下の段は地面ぎわで暗い。
    奥の内がわの壁（輪の内がわ）は、影の中。レンガ1つずつ、少し色をかえる（焼きむら）
  - 中の芝: 町の芝と同じ色の段。左上が明るく、囲いの内がわのふち（奥と左）は囲いのかげで暗い。まんなか（幹の立つ所）は木のかげ。
    短い草の葉先を、ところどころ明るく立てる
  - 地面: 囲いの外の、右下へうすく透ける接地の影（黒い線で切らない）
色は町に合わせて3つ: red（赤茶のレンガ。石だたみの町）・pale（白っぽい石のレンガ。白い家の霧断崖）・sand（砂色のレンガ。板の町など）。
書き出し: ../r20-props/planter-<色>.txt（奥の半分＋芝。地面の上に、木より先に描く）と planter-<色>-front.txt
（前の半分の囲い。木を描いたあとに重ねて、幹の根もとをかくす）。どれも 44×26、足もとのまんなか（22, 17）が木の根もと。"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R20 = os.path.join(HERE, "..", "r20-props")
W, H = 44, 26
CX, GY = 22.0, 18.0             # 地面の上の、囲いのまんなか
A, B = 20.0, 8.0                # 外がわのだ円
AI, BI = 15.5, 5.2              # 内がわのだ円
HW = 4.0                        # 壁の高さ
TOP = GY - HW                   # 上の面のまんなかの高さ
L2 = (-0.72, 0.69)              # 地面の上での、光の来る向き（左、手前）

RAMPS = {
    "red": ["#2e1612", "#45201a", "#5f2c22", "#7a3a2a", "#944a34", "#ac5c40", "#c27350", "#d48c66", "#e2a882"],
    "pale": ["#3c3c44", "#52525a", "#6a6a72", "#84848a", "#9e9ca0", "#b6b2b2", "#cac6c0", "#dcd8ce", "#ebe7dc"],
    "sand": ["#3e2a1a", "#563c24", "#705030", "#8c683e", "#a8824e", "#c09c62", "#d4b47a", "#e2c894", "#eedcb0"],
}
MORTAR = {"red": ["#5a4c44", "#7c6e62", "#a29482"], "pale": ["#4e4c4c", "#6c6a68", "#8e8a84"], "sand": ["#5a4a3a", "#7a6a54", "#9c8a70"]}
GRASS = ["#26402a", "#37572f", "#4b7137", "#628a40", "#7da24d", "#a0bb62"]
SHADOW = ["#10181440", "#10181470"]


def hn(*a):
    n = 2166136261
    for v in a:
        n = ((n ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    n ^= n >> 15
    return n


def pick(ramp, v):
    return ramp[max(0, min(len(ramp) - 1, int(round(v))))]


def ell(x, y, a, b, cy):
    return ((x + 0.5 - CX) / a) ** 2 + ((y + 0.5 - cy) / b) ** 2


def wall_height(x, y):
    """外がわの壁の、このドットの地面からの高さ（壁でなければ None）。"""
    best = None
    t = 0.0
    while t <= HW + 1e-6:
        if ell(x, y, A, B, GY - t) <= 1:
            best = t
            break
        t += 0.25
    return best


def draw(name):
    R, M = RAMPS[name], MORTAR[name]
    back = [["" for _ in range(W)] for _ in range(H)]
    front = [["" for _ in range(W)] for _ in range(H)]
    for y in range(H):
        for x in range(W):
            # 地面の接地の影（右下へ少しずれた、だ円）
            if ell(x - 1.2, y - 1.0, A + 1.0, B + 0.8, GY) <= 1 and not ell(x, y, A, B, GY) <= 1:
                back[y][x] = SHADOW[1] if ell(x - 1.2, y - 1.0, A + 0.2, B + 0.2, GY) <= 1 else SHADOW[0]
            in_top_o = ell(x, y, A, B, TOP) <= 1
            in_top_i = ell(x, y, AI, BI, TOP) <= 1
            is_front = y + 0.5 > TOP + 0.6                      # 幹より手前の半分
            if in_top_i:
                # 輪の内がわ: 奥の内がわの壁（影の中）か、芝
                lawn_y = TOP + 1.3
                if not ell(x, y, AI, BI, lawn_y) <= 1 and y + 0.5 < TOP:
                    th = math.atan2((y + 0.5 - TOP) / BI, (x + 0.5 - CX) / AI)
                    nx, ny = -math.cos(th), -math.sin(th)       # 内がわを向く面
                    v = 2.0 + 1.6 * max(0.0, nx * L2[0] + ny * L2[1])
                    s = (th + math.pi) / (2 * math.pi) * 18
                    back[y][x] = pick(M, 0) if (s % 1) < 0.2 else pick(R, v)
                    continue
                e = ell(x, y, AI, BI, lawn_y)
                v = 3.3 - (x + 0.5 - CX) / AI * 0.7 - (y + 0.5 - lawn_y) / BI * 0.3
                th = math.atan2((y + 0.5 - lawn_y) / BI, (x + 0.5 - CX) / AI)
                if e > 0.55:
                    # 囲いのかげ: 奥と左のふち（光は左上から来るので、左上の壁が、内がわの芝にかげを落とす）
                    occl = (e - 0.55) / 0.45
                    side = max(0.0, -math.sin(th)) * 0.8 + max(0.0, -math.cos(th)) * 0.7 + 0.35
                    v -= occl * 2.2 * side
                d = math.hypot((x + 0.5 - CX - 1.5) / 7.0, (y + 0.5 - lawn_y - 0.5) / 2.6)
                if d < 1:
                    v -= 1.3 * (1 - d)                           # まんなかの、木のかげ
                if hn(x, y, 3) % 7 == 0 and v > 1.5:
                    v += 1.2                                     # 草の葉先（明るい）
                elif hn(x, y, 4) % 9 == 0:
                    v -= 0.8                                     # 草の根もとのすき間
                fr = v - math.floor(v)
                if 0.4 < fr < 0.6:
                    v = math.floor(v) + (1 if (x + y) % 2 else 0)   # 段と段のあいだだけ市松
                back[y][x] = pick(GRASS, v)
                continue
            if in_top_o:
                # 上の面（笠石のレンガ。放射状の目地）
                th = math.atan2((y + 0.5 - TOP) / ((B + BI) / 2), (x + 0.5 - CX) / ((A + AI) / 2))
                s = (th + math.pi) / (2 * math.pi) * 22
                k = int(s)
                v = 6.4 - math.cos(th) * 1.1 - max(0.0, -math.sin(th)) * 0.4 + ((hn(k, 7, ord(name[0])) % 5) - 2) * 0.25
                below = wall_height(x, y + 1)
                if below is not None and not ell(x, y + 1, A, B, TOP) <= 1:
                    v += 1.0                                     # 前のふちの、光の線
                c = pick(M, 2 if math.cos(th) < 0 else 1) if (s % 1) < 0.16 else pick(R, v)
                (front if is_front else back)[y][x] = c
                continue
            hgt = wall_height(x, y)
            if hgt is not None:
                # 前の面（2段のレンガ積み）
                thw = math.atan2((y + 0.5 - (GY - hgt)) / B, (x + 0.5 - CX) / A)
                nx, ny = math.cos(thw), math.sin(thw)
                course = 0 if hgt < 2.0 else 1
                v = 3.3 + 2.6 * (nx * L2[0] + ny * L2[1])
                s = (thw + math.pi) / (2 * math.pi) * 26 + course * 0.5
                k = int(s)
                v += ((hn(k, course, 11, ord(name[0])) % 5) - 2) * 0.3   # 焼きむら
                if hgt < 0.6:
                    v -= 1.0                                     # 地面ぎわは暗い
                if 1.75 <= hgt < 2.25:
                    c = pick(M, 1 if nx < 0 else 0)              # 横の目地
                elif (s % 1) < 0.17:
                    c = pick(M, 1 if nx < 0 else 0)              # たての目地
                else:
                    c = pick(R, v)
                (front if is_front else back)[y][x] = c
    for img, nm in ((back, f"planter-{name}"), (front, f"planter-{name}-front")):
        cols = sorted({c for r in img for c in r if c})
        syms = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        cmap = {c: syms[i] for i, c in enumerate(cols)}
        open(os.path.join(R20, nm + ".txt"), "w").write("\n".join("".join(cmap[c] if c else "." for c in r) for r in img) + "\n")
        json.dump({cmap[c]: c for c in cols}, open(os.path.join(R20, "pal-" + nm + ".json"), "w"))
        print(nm, len(cols), "colors")


if __name__ == "__main__":
    for n in RAMPS:
        draw(n)
