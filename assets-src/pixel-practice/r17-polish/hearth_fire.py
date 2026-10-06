"""暖炉の火を動かす（2026-10-06、人間の指示「暖炉も火が動いてるようにしよう」）。
いまの暖炉の絵（../r20-props/hearth.txt）の、火のある所（口の中の下のほう）を、4コマのゆらぐ炎に描きなおす。
炎は、根もとの薪の上から立ちのぼる3〜4本の舌の形。外がわは赤みのある橙、なかは橙、芯は黄色、いちばん下の芯はほぼ白。
舌の高さと、ゆれる向きを、コマごとに少しずつかえる（ゆらぎ）。火のあった所で炎がない所は、口の中の暗い色にもどす。
書き出し: ../r20-props/hearth.txt（1コマめ）と hearth-1〜3.txt（prop:hearth-1〜3。ゲームでは順番に見せる）。
使い方: python3 hearth_fire.py（restyle.py・gloss.py のあとに。元の絵は、この場所の hearth-base.txt に残す）"""
import colorsys
import json
import math
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
R20 = os.path.join(HERE, "..", "r20-props")
OUTER, MID, INNER, CORE = "#c75a2a", "#f2a544", "#f9edb3", "#fefcf1"


def load(name, d=R20):
    rows = [l for l in open(os.path.join(d, name + ".txt")).read().split("\n") if l]
    pal = json.load(open(os.path.join(d, "pal-" + name + ".json")))
    return [[pal[c] if c != "." else "" for c in r] for r in rows]


def is_fire(c):
    if not c or len(c) != 7:
        return False
    r, g, b = (int(c[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h <= 0.17 and s > 0.6 and l > 0.45


def main():
    # 元の絵は、この場所（r17-polish）に残す（r20-props に置くと、ゲームの絵として書き出されてしまう）
    if not os.path.exists(os.path.join(HERE, "hearth-base.txt")):
        shutil.copy(os.path.join(R20, "hearth.txt"), os.path.join(HERE, "hearth-base.txt"))
        shutil.copy(os.path.join(R20, "pal-hearth.json"), os.path.join(HERE, "pal-hearth-base.json"))
    base = load("hearth-base", HERE)
    H, W = len(base), len(base[0])
    fire = [(x, y) for y in range(H) for x in range(W) if is_fire(base[y][x]) and y > H // 2]
    xs = [p[0] for p in fire]; ys = [p[1] for p in fire]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    # 口の中の暗い色（火のまわりで、いちばん多い暗い色）
    cnt = {}
    for y in range(y0 - 4, y1 + 1):
        for x in range(x0 - 2, x1 + 3):
            c = base[y][x]
            if c and len(c) == 7 and not is_fire(c):
                r, g, b = (int(c[i:i + 2], 16) for i in (1, 3, 5))
                if r + g + b < 200:
                    cnt[c] = cnt.get(c, 0) + 1
    dark = max(cnt, key=cnt.get)
    # 炎のまんなか: 口の中（火の高さの列で、火か暗い色がつづく所）のまんなか
    row = y1 - 2
    inside = [x for x in range(W) if base[row][x] == dark or is_fire(base[row][x])]
    runs, cur = [], []
    for x in inside:
        if cur and x != cur[-1] + 1:
            runs.append(cur); cur = []
        cur.append(x)
    if cur:
        runs.append(cur)
    best = max(runs, key=len)
    cx = (best[0] + best[-1] + 1) / 2
    for f in range(4):
        img = [r[:] for r in base]
        for x, y in fire:
            img[y][x] = dark
        # 炎の舌: 3〜4本。根もとは y1、高さはコマごとにかわる
        tongues = [(-3.2, 6.5), (0.2, 8.5), (3.4, 6.0), (-0.8, 4.5)]
        for i, (dx, h) in enumerate(tongues):
            hh = h * (0.8 + 0.25 * math.sin(f * 1.7 + i * 2.1))
            lean = 0.6 * math.sin(f * 1.3 + i)
            for t in range(int(hh) + 1):
                fy = y1 - t
                k = t / max(1.0, hh)
                half = (2.6 if i != 3 else 2.0) * (1 - k) ** 0.8 + 0.3
                xc = cx + dx + lean * k * k * 2
                for x in range(int(xc - half - 1), int(xc + half + 2)):
                    d = abs(x + 0.5 - xc) / max(0.4, half)
                    if d > 1 or not (0 <= x < W) or fy < y0 - 3:
                        continue
                    c = OUTER if d > 0.66 or k > 0.8 else (MID if d > 0.33 or k > 0.5 else INNER)
                    if t <= 1 and d < 0.5:
                        c = CORE
                    img[fy][x] = c
        name = "hearth" if f == 0 else f"hearth-{f}"
        cols = sorted({c for r in img for c in r if c})
        syms = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        cmap = {c: syms[i] for i, c in enumerate(cols)}
        open(os.path.join(R20, name + ".txt"), "w").write("\n".join("".join(cmap[c] if c else "." for c in r) for r in img) + "\n")
        json.dump({cmap[c]: c for c in cols}, open(os.path.join(R20, "pal-" + name + ".json"), "w"))
        print(name, len(cols))


if __name__ == "__main__":
    main()
