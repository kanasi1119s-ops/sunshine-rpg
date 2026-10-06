"""積乱雲の中の雷（2026-10-05、人間の指示「雲をこの雲に差し替えて。あと黄色く光ってる部分にも雷のエフェクトを入れて」）。
cumulonimbus.txt（352×256）から、4コマを作る:
  0: ふだん
  1: 雲の中が光る（黄色く光る所が、1段明るくなる）
  2: 強く光る＋雲の中を走る稲妻 A（黄色い所の中を、横にジグザグに走り、枝分かれする）
  3: 強く光る＋稲妻 B（別の所）
光るのは、黄色い所（あたたかい色の所）と、そのまわりの灰色の所の少し。稲妻に近いほど明るい。
稲妻は、まん中が白（1ドット）、そのとなりが薄い黄色（光のにじみ）。雲の外には出ない。
書き出し: frame-0〜3.txt と pal-frame-0〜3.json（エディタで確かめる）、src/assets/falls/cloud.png（横に4コマ）。"""
import json
import math
import os
import random
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "..", "src", "assets", "falls")
import sys
# 2026-10-06: 人間が「雲採用」と決めた、段になってそびえ横にも雲がある雲（reshape3、440×256）に変えた。
# 前の雲（cumulonimbus、352×256）で作るときは: python3 cloud_fx.py cumulonimbus
NAME = sys.argv[1] if len(sys.argv) > 1 else "reshape3"
rows = [l for l in open(os.path.join(HERE, NAME + ".txt")).read().split("\n") if l]
pal = json.load(open(os.path.join(HERE, "pal-" + NAME + ".json")))
rgb = {k: (int(v[1:3], 16), int(v[3:5], 16), int(v[5:7], 16)) for k, v in pal.items()}
W, H = len(rows[0]), len(rows)
base = {(x, y): rgb[c] for y, r in enumerate(rows) for x, c in enumerate(r) if c != "."}


def warmth(c):
    return max(0.0, min(1.0, (c[0] - c[2] - 10) / 60))


def mix(a, b, t):
    return tuple(int(round(a[i] * (1 - t) + b[i] * t)) for i in range(3))


FLASH = (255, 236, 176)
CORE = (255, 252, 236)
HALO = (255, 226, 140)


def bolt(seed, x0, y0, direction):
    """黄色い所の中を走る稲妻（ドットの道）。横へジグザグに進み、ときどき枝分かれする。"""
    rnd = random.Random(seed)
    path = set()

    def walk(x, y, dx, n, branch):
        for _ in range(n):
            if (x, y) not in base or warmth(base[(x, y)]) < 0.15 and rnd.random() < 0.6:
                return
            path.add((x, y))
            x += dx
            r = rnd.random()
            if r < 0.3:
                y -= 1
            elif r < 0.6:
                y += 1
            if rnd.random() < 0.1:              # 2ドットぶん段を落とす（とがった折れ目）
                path.add((x, y))
                y += rnd.choice((-1, 1))
            if branch and rnd.random() < 0.06:
                walk(x, y, dx, rnd.randint(6, 14), False)
                walk(x, y, -dx if rnd.random() < 0.3 else dx, rnd.randint(5, 10), False)
    walk(x0, y0, direction, 70, True)
    walk(x0, y0, -direction, 30, True)
    return path


def frame(level, path):
    out = {}
    pts = list(path)
    for (x, y), c in base.items():
        wm = warmth(c)
        near = 0.0
        if pts:
            d = min(abs(x - px) + abs(y - py) for (px, py) in pts[::3])
            near = max(0.0, 1 - d / 34)
        t = level * 0.5 * wm ** 0.8 + near * 0.45 * wm ** 0.6 + near * near * 0.12
        out[(x, y)] = mix(c, FLASH, min(0.8, t)) if t > 0.04 else c
    for (x, y) in path:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            q = (x + dx, y + dy)
            if q in out and q not in path:
                out[q] = mix(out[q], HALO, 0.75)
    for q in path:
        out[q] = CORE
    return out


# 稲妻の始まり: 黄色い所の中から選ぶ
warm_pts = sorted(p for p, c in base.items() if warmth(c) > 0.55)
rnd = random.Random(7)
# 稲妻の始まり（黄色く光る所の中）。reshape3 は、前の雲の位置を、雲の本体の置き場所（0.9 倍、塔のまん中 x=215）に合わせて写した所
A0, B0 = ((150, 186), (236, 196)) if NAME == "cumulonimbus" else ((192, 192), (269, 201))
pA = bolt(11, *min(warm_pts, key=lambda p: abs(p[0] - A0[0]) + abs(p[1] - A0[1])), 1)
pB = bolt(23, *min(warm_pts, key=lambda p: abs(p[0] - B0[0]) + abs(p[1] - B0[1])), -1)
frames = [frame(0, set()), frame(0.6, set()), frame(1.0, pA), frame(1.0, pB)]
# 色を、コマごとに62色までにしぼる（光の色はまぜた色なので、近い色にまとめる）
pool = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
sheet = Image.new("RGBA", (W * 4, H), (0, 0, 0, 0))
for i, fr in enumerate(frames):
    cols = sorted(set(fr.values()))
    if len(cols) > len(pool):
        keep = {CORE, HALO}
        rest = [p for p, c in fr.items() if c not in keep]
        img = Image.new("RGB", (len(rest), 1))
        img.putdata([fr[p] for p in rest])
        q = img.quantize(colors=len(pool) - 4, method=Image.MEDIANCUT)
        qp = q.getpalette()
        qd = list(q.get_flattened_data()) if hasattr(q, 'get_flattened_data') else list(q.getdata())
        nf = dict(fr)
        for j, p in enumerate(rest):
            nf[p] = tuple(qp[qd[j] * 3:qd[j] * 3 + 3])
        fr = nf
        frames[i] = fr
        cols = sorted(set(fr.values()))
    key = {c: pool[j] for j, c in enumerate(cols)}
    out_rows = ["".join(key[fr[(x, y)]] if (x, y) in fr else "." for x in range(W)) for y in range(H)]
    open(os.path.join(HERE, f"frame-{i}.txt"), "w").write("\n".join(out_rows) + "\n")
    json.dump({key[c]: "#%02x%02x%02x" % c for c in cols}, open(os.path.join(HERE, f"pal-frame-{i}.json"), "w"))
    for (x, y), c in fr.items():
        sheet.putpixel((i * W + x, y), c + (255,))
sheet.save(os.path.join(OUT, "cloud.png"))
print("ok", [len(set(f.values())) for f in frames], len(pA), len(pB))
