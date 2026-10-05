"""稲妻のドット絵（96×220・2本×6コマ）。2026-10-05、人間の指示「雷まであるドットの動きを出して」。
雲の底から、穴のふちへ落ちるジグザグの稲妻。芯は白（1〜2ドット）、そのまわりに青白い光、さらに外にうすい光（点々）。枝分かれあり。
コマ: 0=先に走る細い光（上の半分まで）／1=いちばん明るい本体と枝・強い光／2=本体（枝の光は弱く）／3=消えかけの残り火／4=もう一度光る／5=消える。
出力: bolt-<a|b>-0..5.txt / pal-*.json と、src/assets/falls/bolt.png（横に12コマ: a の6コマ、b の6コマ）。"""
import json
import math
import os
import random

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "..", "src", "assets", "falls")
W, H = 96, 220
PAL = {"W": "#ffffff", "C": "#d8ecff", "B": "#8cc4ff", "G": "#4a78c8"}


def path(seed):
    rnd = random.Random(seed)
    pts = [(W / 2 + rnd.uniform(-6, 6), 0.0)]
    x, y = pts[0]
    while y < H - 4:
        y += rnd.uniform(7, 15)
        x += rnd.uniform(-9, 9)
        x = max(10, min(W - 10, x))
        pts.append((x, min(y, H - 2)))
    branches = []
    for _ in range(3):
        i = rnd.randrange(2, len(pts) - 4)
        bx, by = pts[i]
        bpts = [(bx, by)]
        d = rnd.choice((-1, 1))
        for _ in range(rnd.randint(2, 4)):
            bx += d * rnd.uniform(4, 10)
            by += rnd.uniform(5, 11)
            bpts.append((max(2, min(W - 3, bx)), min(H - 2, by)))
        branches.append(bpts)
    return pts, branches


def raster(g, pts, ch, upto=None):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if upto is not None and y0 > upto:
            break
        n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
        for k in range(n + 1):
            t = k / max(1, n)
            x, y = round(x0 + (x1 - x0) * t), round(y0 + (y1 - y0) * t)
            if upto is not None and y > upto:
                break
            if 0 <= x < W and 0 <= y < H:
                g[y][x] = ch


def glow(g, core, ch, rad, dots=False):
    for y in range(H):
        for x in range(W):
            if g[y][x] != ".":
                continue
            near = any(core[yy][xx] for yy in range(max(0, y - rad), min(H, y + rad + 1)) for xx in range(max(0, x - rad), min(W, x + rad + 1)))
            if near and (not dots or (x + y) % 2 == 0):
                g[y][x] = ch


def frame(seed, fr):
    pts, branches = path(seed)
    g = [["."] * W for _ in range(H)]
    if fr == 0:
        raster(g, pts, "C", upto=H * 0.45)
    elif fr in (1, 4):
        raster(g, pts, "W")
        for b in branches:
            raster(g, b, "C" if fr == 1 else "B")
        # 芯を少し太く（右どなりも白）
        for y in range(H):
            for x in range(W - 1, 0, -1):
                if g[y][x - 1] == "W" and g[y][x] == ".":
                    g[y][x] = "W" if fr == 1 else "C"
    elif fr == 2:
        raster(g, pts, "W")
        for b in branches:
            raster(g, b, "B")
    elif fr == 3:
        raster(g, pts, "B")
    elif fr == 5:
        raster(g, pts, "G")
    core = [[g[y][x] != "." for x in range(W)] for y in range(H)]
    if fr in (1, 4):
        glow(g, core, "B", 1)
        core2 = [[g[y][x] != "." for x in range(W)] for y in range(H)]
        glow(g, core2, "G", 1, dots=True)
    elif fr == 2:
        glow(g, core, "G", 1, dots=True)
    return g


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    sheet = Image.new("RGBA", (W * 12, H), (0, 0, 0, 0))
    i = 0
    for name, seed in (("a", 7), ("b", 23)):
        for fr in range(6):
            g = frame(seed, fr)
            rows = ["".join(r) for r in g]
            used = sorted(set("".join(rows)) - {"."})
            with open(os.path.join(HERE, f"bolt-{name}-{fr}.txt"), "w") as f:
                f.write("\n".join(rows) + "\n")
            with open(os.path.join(HERE, f"pal-bolt-{name}-{fr}.json"), "w") as f:
                json.dump({k: PAL[k] for k in used}, f)
            for y, r in enumerate(rows):
                for x, ch in enumerate(r):
                    if ch != ".":
                        v = PAL[ch]
                        sheet.putpixel((i * W + x, y), (int(v[1:3], 16), int(v[3:5], 16), int(v[5:7], 16), 255))
            i += 1
    sheet.save(os.path.join(OUT, "bolt.png"))
    print("ok")
