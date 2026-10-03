"""雪の地方の飾り（雪をかぶった木・枯れ木・雪の岩と茂み）を、既存の絵から／一から作る。
使い方: python3 snow.py   → tree-snow.txt, tree-dead.txt, rock-snow.txt, bush-snow.txt と pal-*.json を書き出す（48×48枠に下そろえで置く前の絵）"""
import json, math, random

def load(txt, pal):
    rows = [l.rstrip("\n") for l in open(txt) if l.strip("\n") != ""]
    w = max(len(r) for r in rows)
    return [list(r.ljust(w, ".")) for r in rows], json.load(open(pal))

def h(x, y, s=0):
    v = (x * 374761393 + y * 668265263 + s * 144665) & 0xFFFFFFFF
    v = ((v ^ (v >> 13)) * 1274126177) & 0xFFFFFFFF
    return (v ^ (v >> 16)) & 0xFFFFFFFF

SNOW = {"a": "#f6faff", "b": "#dbe7f5", "c": "#b4c6e0", "d": "#8ea2c4"}

def cap(g, foliage, depth_fn):
    """上を向いた面（すぐ上が空・縁取り）の葉・岩の上に雪をのせる。"""
    H, W = len(g), len(g[0])
    out = [r[:] for r in g]
    for x in range(W):
        run = None
        for y in range(H):
            c = g[y][x]
            if c in foliage:
                above = g[y-1][x] if y > 0 else "."
                if run is None and (above == "." or above not in foliage):
                    run = 0
                if run is not None:
                    d = depth_fn(x, y, run, W)
                    if run < d:
                        right = x > W * 0.55
                        out[y][x] = ("b" if run >= d-1 else "a") if not right else ("c" if run >= d-1 else "b")
                    run += 1
            else:
                run = None
    return out

def tree_snow():
    g, pal = load("tree4.txt", "pal-tree.json")
    frost = {"D": "#22403a", "E": "#2f5a4c", "F": "#416f5c", "G": "#5a8a72", "H": "#7aa690", "I": "#9cc0aa", "S": "#7a8cac"}
    pal.update(frost); pal.update(SNOW)
    out = cap(g, set("DEFGHI"), lambda x, y, run, W: 3 + (h(x // 2, y // 3) % 2))
    # 枝の段ごとに積もる雪の「ふくらみ」を足す: 明るい葉（H・I）の一部も雪にする
    for y, row in enumerate(g):
        for x, c in enumerate(row):
            if c in "HI" and out[y][x] == c and h(x, y, 5) % 3 == 0:
                out[y][x] = "b"
    return out, pal

def rock_snow():
    g, pal = load("rock2.txt", "pal-rock2.json")
    pal.update(SNOW)
    out = cap(g, set("DEFGHIJK"), lambda x, y, run, W: 3)
    return out, pal

def bush_snow():
    g, pal = load("bush2.txt", "pal-bush2.json")
    pal.update({"D": "#22403a", "E": "#2f5a4c", "F": "#416f5c", "G": "#5a8a72", "H": "#7aa690", "I": "#9cc0aa"}); pal.update(SNOW)
    out = cap(g, set("DEFGHIJK"), lambda x, y, run, W: 3)
    return out, pal

def dead_tree():
    W = H = 48
    mask = [[0]*W for _ in range(H)]
    def brush(cx, cy, r):
        for y in range(int(cy-r-1), int(cy+r+2)):
            for x in range(int(cx-r-1), int(cx+r+2)):
                if 0 <= x < W and 0 <= y < H and (x-cx)**2 + (y-cy)**2 <= r*r: mask[y][x] = 1
    def line(x0, y0, x1, y1, w0, w1):
        n = int(max(abs(x1-x0), abs(y1-y0))*2) + 1
        for i in range(n+1):
            t = i/n
            brush(x0+(x1-x0)*t, y0+(y1-y0)*t, (w0+(w1-w0)*t)/2)
    # 幹（根もとが太く、ゆるく曲がる）と枝
    line(24, 44, 23.5, 30, 7, 5)
    line(23.5, 30, 24.5, 18, 5, 3.6)
    line(24.5, 18, 23, 6, 3.6, 1.6)
    branches = [(23.8, 27, 12, 20, 3.4, 1.4), (12, 20, 6, 13, 1.8, 1.0), (12, 20, 14, 11, 1.6, 1.0), (24.3, 22, 36, 15, 3.0, 1.3), (36, 15, 41, 8, 1.7, 1.0), (36, 15, 43, 17, 1.5, 0.9),
                (24.5, 15, 17, 8, 2.2, 1.0), (23.2, 33, 33, 28, 2.6, 1.2), (33, 28, 40, 26, 1.5, 0.9), (23.6, 35, 14, 31, 2.4, 1.1), (14, 31, 9, 28, 1.3, 0.8), (12, 20, 9, 22, 1.2, 0.8)]
    for b in branches: line(*b)
    # 根もとのふくらみ
    for dx, r in ((-4, 2.2), (4, 2.0)): brush(24+dx, 44, r)
    pal = {"A": "#14100e", "J": "#2a1a12", "K": "#4a3020", "L": "#6a4a30", "M": "#8c6a48", **SNOW}
    out = [["."]*W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            if not mask[y][x]: continue
            left = x == 0 or not mask[y][x-1]
            right = x == W-1 or not mask[y][x+1]
            c = "M" if left else "K" if right else "L"
            if (x + y*3) % 7 == 0 and not left and not right: c = "J"
            out[y][x] = c
    # 縁取り
    ol = [r[:] for r in out]
    for y in range(H):
        for x in range(W):
            if out[y][x] != ".": continue
            if any(0 <= y+dy < H and 0 <= x+dx < W and out[y+dy][x+dx] != "." for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))): ol[y][x] = "A"
    out = ol
    # 雪: 上を向いた面（すぐ上が空）の1〜2ドット、根もとの雪だまり
    res = [r[:] for r in out]
    for y in range(1, H):
        for x in range(W):
            if out[y][x] in "MKLJ" and out[y-1][x] in ".A":
                res[y][x] = "a" if x < 28 else "b"
                if y+1 < H and out[y+1][x] in "MKLJ" and h(x, y) % 2 == 0: res[y+1][x] = "b"
    cx, by = 24, 45
    for y in range(by-2, by+3):
        for x in range(cx-10, cx+11):
            e = ((x-cx)/10.0)**2 + ((y-by)/2.4)**2
            if e <= 1 and 0 <= y < H:
                res[y][x] = "a" if y <= by-1 and x < cx+3 else "b" if y <= by else "c"
        # ふちに縁取り
    return res, pal

def write(name, g, pal):
    used = sorted({c for r in g for c in r if c != "."})
    open(f"{name}.txt", "w").write("\n".join("".join(r) for r in g) + "\n")
    json.dump({k: v for k, v in pal.items() if k in used}, open(f"pal-{name}.json", "w"))
    print(name, len(g[0]), len(g), len(used))

if __name__ == "__main__":
    for n, fn in (("tree-snow", tree_snow), ("rock-snow", rock_snow), ("bush-snow", bush_snow), ("tree-dead", dead_tree)):
        g, p = fn(); write(n, g, p)
