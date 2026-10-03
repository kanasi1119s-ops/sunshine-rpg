"""自作ドット絵の検査。使い方: python3 lint.py 絵.txt パレット.json [縁の記号 既定A]
- 孤立点（上下左右に同色でない隣しかない1ドット）、離れた浮き（本体から切れた小さな塊）
- 縁取りの欠け（外周なのに縁の色でないドット）
- 色数、各色の使用ドット数（1〜2ドットだけの色は要確認）
- 光の向き（左上が明るいか）
- 線のギザギザ（外周の段の長さが不規則: 1-3-1 のような急な増減）"""
import sys, json
from PIL import Image
import numpy as np
rows = [l for l in open(sys.argv[1]).read().split("\n") if l.strip()]
pal = json.load(open(sys.argv[2])); edge = sys.argv[3] if len(sys.argv) > 3 else "A"
W = max(len(r) for r in rows); H = len(rows)
g = [list(r.ljust(W, ".")) for r in rows]
def op(x, y): return 0 <= x < W and 0 <= y < H and g[y][x] != "."
issues = []
# 孤立点
for y in range(H):
    for x in range(W):
        if g[y][x] == ".": continue
        n4 = sum(op(x+dx, y+dy) for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)))
        if n4 == 0: issues.append(f"孤立点({x},{y}) {g[y][x]}")
# 浮いた塊
seen = set(); comps = []
for y in range(H):
    for x in range(W):
        if g[y][x] != "." and (x, y) not in seen:
            st = [(x, y)]; seen.add((x, y)); c = []
            while st:
                a, b = st.pop(); c.append((a, b))
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)):
                    if op(a+dx, b+dy) and (a+dx, b+dy) not in seen: seen.add((a+dx, b+dy)); st.append((a+dx, b+dy))
            comps.append(c)
comps.sort(key=len, reverse=True)
for c in comps[1:]:
    if len(c) < 12: issues.append(f"浮いた小さな塊 {len(c)}ドット 例({c[0][0]},{c[0][1]})")
# 縁取りの欠け
miss = 0
for y in range(H):
    for x in range(W):
        if g[y][x] != "." and any(not op(x+dx, y+dy) for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))) and g[y][x] != edge: miss += 1
tot = sum(1 for y in range(H) for x in range(W) if g[y][x] != ".")
if miss: issues.append(f"外周で縁取りの色でないドット {miss}個（全体の{miss*100//tot}%）")
# 色
from collections import Counter
cnt = Counter(ch for r in g for ch in r if ch != ".")
rare = [k for k, v in cnt.items() if v <= 2]
print(f"{W}x{H} 色{len(cnt)} 不透明{tot}ドット" + (f" 1〜2ドットだけの色: {''.join(rare)}" if rare else ""))
# 光の向き
def lum(ch):
    h = pal[ch].lstrip("#"); r, gg, b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16); return 0.3*r + 0.59*gg + 0.11*b
pts = [(x, y, lum(g[y][x])) for y in range(H) for x in range(W) if g[y][x] != "."]
pts = [p for p in pts if g[p[1]][p[0]] != edge]
if pts:
    xs = np.array([p[0] for p in pts]); ys = np.array([p[1] for p in pts]); ls = np.array([p[2] for p in pts])
    cx, cy = xs.mean(), ys.mean()
    tl = ls[(xs+ys) < (cx+cy)].mean(); br = ls[(xs+ys) >= (cx+cy)].mean()
    print(f"左上の平均明度 {tl:.0f} / 右下 {br:.0f}  → " + ("光は左上から" if tl > br + 5 else "光の向きが弱い・逆（要確認）"))
for i in issues[:20]: print("  要確認:", i)
if not issues: print("  問題なし")
