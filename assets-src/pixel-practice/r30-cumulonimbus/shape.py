"""積乱雲の形を、ガラッと変える（2026-10-05、人間の指示「似たような感じで、形をガラッと変えてみよう」）。
写真の雲の、色・もくもく・光り方（中の金色）はそのままに、形だけを「かなとこ雲」（上がたいらに横へ大きく広がる、
背の高い積乱雲）に変える。
- 写真の雲を、横の段ごとに見て（その段の雲の左はしと右はし）、新しい形の同じ段の左はしと右はしへ、横にのばしたり
  ちぢめたりして写す（雲のふちのもくもくは、ふちに写るので、ふちらしさが残る）。
- 縦は、新しい形の「かなとこ（上の広がり）」には写真の雲の上のほう、「柱（まん中）」には写真のまん中（金色に光る所）、
  「すそ（下の広がり）」には写真の下のほうを写す。
- そのあとの、ドットにするやり方（なめらかな色・やわらかいふち・消えていく底）は、natural.py / wide.py と同じ。
絵は 352×256。書き出しは shape-*.txt / pal-shape-*.json / shape.png（いまゲームの雲は変えない）。"""
import json
import math
from PIL import Image, ImageFilter

src = Image.open("ref-photo.png").convert("RGB")
crop = src.crop((28, 0, 412, 262))
CW, CH = crop.size
cpx = crop.load()
# 写真の雲の、段ごとの左はし・右はし（いちばん大きなかたまりで）
cm = [[(cpx[x, y][2] - cpx[x, y][0]) < 44 for x in range(CW)] for y in range(CH)]
seen = [[False] * CW for _ in range(CH)]
big = []
for y0 in range(CH):
    for x0 in range(CW):
        if cm[y0][x0] and not seen[y0][x0]:
            comp, st = [], [(x0, y0)]
            seen[y0][x0] = True
            while st:
                x, y = st.pop()
                comp.append((x, y))
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < CW and 0 <= ny < CH and cm[ny][nx] and not seen[ny][nx]:
                        seen[ny][nx] = True
                        st.append((nx, ny))
            if len(comp) > len(big):
                big = comp
ext = {}
for x, y in big:
    a, b = ext.get(y, (x, x))
    ext[y] = (min(a, x), max(b, x))
ys = sorted(ext)
TOP, BOT = ys[0], min(ys[-1], CH - 1)


def src_ext(sy):
    sy = max(TOP, min(BOT, int(round(sy))))
    ls, rs = [], []
    for k in range(-3, 4):                     # 上下の段とならす
        e = ext.get(sy + k)
        if e:
            ls.append(e[0])
            rs.append(e[1])
    return sum(ls) / len(ls), sum(rs) / len(rs)


W, H = 352, 256
CXo = 176


def hsh(x, y):
    n = (x * 374761393 + y * 668265263) & 0xFFFFFFFF
    n = (n ^ (n >> 13)) * 1274126177 & 0xFFFFFFFF
    return (n & 0xFFFF) / 65535


def noise(x, s, k=7):
    i = math.floor(x / s)
    f = x / s - i
    a, b = hsh(i, k), hsh(i + 1, k)
    return a + (b - a) * f * f * (3 - 2 * f)


def shape(y):
    """新しい形（その段の左はし・右はし）と、写す写真の段。かなとこ・柱・すそ。"""
    if y < 12 or y > 252:
        return None
    if y < 64:                                  # かなとこ: 上はまるく、すぐ横へ大きく広がる。右へ長くのびる
        t = (y - 12) / 52
        hw = 30 + 140 * math.sin(min(1.0, t * 1.5) * math.pi / 2) ** 0.7
        l, r = CXo - hw * 0.82, CXo + hw * 1.0
        sy = TOP + (y - 12) / 52 * 50
    elif y < 92:                                # かなとこの下側: 柱へ向かってすぼまる
        t = (y - 64) / 28
        hw = 170 - 100 * math.sin(t * math.pi / 2)
        l, r = CXo - hw * 0.82 + t * 6, CXo + hw
        sy = TOP + 50 + t * 25
    elif y < 196:                               # 柱: 少しふくらむ（金色に光る所）
        t = (y - 92) / 104
        hw = 70 + 16 * math.sin(t * math.pi)
        l, r = CXo - hw + 6, CXo + hw + 4
        sy = TOP + 75 + t * (BOT - TOP - 75 - 40)
    else:                                       # すそ: 横に広がって、たいらに
        t = (y - 196) / 56
        hw = 74 + 44 * math.sin(min(1.0, t * 1.7) * math.pi / 2)
        if t > 0.8:
            hw *= 1 - (t - 0.8) * 1.1               # 底のかどは丸く
        l, r = CXo - hw * 1.08, CXo + hw
        sy = BOT - 40 + t * 40
    j = (noise(y, 6, 11) - 0.5) * 10           # ふちのゆらぎ
    return l + j, r - j * 0.6, sy


small = Image.new("RGB", (W, H), (36, 70, 150))
px = small.load()
for y in range(H):
    sh = shape(y)
    if not sh:
        continue
    l, r, sy = sh
    sl, sr = src_ext(sy)
    m = 0.12 * (r - l)                           # ふちの外も少し写す（空とまざる、やわらかいふち）
    for x in range(max(0, int(l - m)), min(W, int(r + m) + 1)):
        u = (x + 0.5 - l) / (r - l)
        sx = sl + u * (sr - sl)
        if 0 <= sx < CW - 1:
            ix = int(sx)
            fx = sx - ix
            iy = max(0, min(CH - 1, int(round(sy))))
            a, b = cpx[ix, iy], cpx[ix + 1, iy]
            px[x, y] = tuple(int(a[k] * (1 - fx) + b[k] * fx) for k in range(3))
small = small.filter(ImageFilter.MedianFilter(3))
px = small.load()
w, h = W, H
S = 256
SW = 352
BAYER = [[0.125, 0.625], [0.875, 0.375]]


def hsh(x, y):
    n = (x * 374761393 + y * 668265263) & 0xFFFFFFFF
    n = (n ^ (n >> 13)) * 1274126177 & 0xFFFFFFFF
    return (n & 0xFFFF) / 65535


def noise(x, s):
    i = math.floor(x / s)
    f = x / s - i
    a, b = hsh(i, 7), hsh(i + 1, 7)
    return a + (b - a) * f * f * (3 - 2 * f)


# 雲らしさ（0=空 1=雲）
def cloudness(r, g, b):
    return max(0.0, min(1.0, (78 - (b - r)) / 34))

alpha = [[cloudness(*px[x, y]) for x in range(w)] for y in range(h)]
for x in range(w):                                   # 底: 下へ行くほどうすくなり、市松で消えていく（まっすぐ切れない）
    depth = 6 + noise(x, 30) * 8
    for y in range(h - 16, h):
        k = (h - 1 - y) / depth
        if k < 1:
            alpha[y][x] = min(alpha[y][x], 0.3 + 0.32 * k)
# 上の方で、空の青が多くまざった所（写真の右上の、うすいかすみ）は、うすい雲にする（四角い面に見えないよう）
for y in range(int(h * 0.4)):
    for x in range(w):
        r, g, b = px[x, y]
        if b - r > 36:
            alpha[y][x] = min(alpha[y][x], 0.5)
solid = [[alpha[y][x] >= 0.62 for x in range(w)] for y in range(h)]
thin = [[0.3 <= alpha[y][x] < 0.62 for x in range(w)] for y in range(h)]
# 雲の本体（いちばん大きなかたまり）
seen = [[False] * w for _ in range(h)]
best = []
for y0 in range(h):
    for x0 in range(w):
        if solid[y0][x0] and not seen[y0][x0]:
            comp, st = [], [(x0, y0)]
            seen[y0][x0] = True
            while st:
                x, y = st.pop()
                comp.append((x, y))
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < w and 0 <= ny < h and solid[ny][nx] and not seen[ny][nx]:
                        seen[ny][nx] = True
                        st.append((nx, ny))
            if len(comp) > len(best):
                best = comp
body = set(best)
# うすい雲は、本体から2ドット以内だけ
near = set()
for (x, y) in body:
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            near.add((x + dx, y + dy))
# 色を32色に（本体の色から）
pts = [px[x, y] for (x, y) in body]
tmp = Image.new("RGB", (len(pts), 1))
tmp.putdata(pts)
q = tmp.quantize(colors=32, method=Image.MEDIANCUT, kmeans=4)
pal = q.getpalette()[:32 * 3]
colors = [tuple(pal[i * 3:i * 3 + 3]) for i in range(32)]


def two_nearest(c):
    d = sorted(range(32), key=lambda i: sum((colors[i][k] - c[k]) ** 2 for k in range(3)))
    return d[0], d[1]


def between(c, a, b):
    A, B = colors[a], colors[b]
    v = [B[k] - A[k] for k in range(3)]
    vv = sum(t * t for t in v) or 1
    return max(0.0, min(1.0, sum((c[k] - A[k]) * v[k] for k in range(3)) / vv))

idx = [[-1] * w for _ in range(h)]
for (x, y) in body:
    c = px[x, y]
    a, b = two_nearest(c)
    t = between(c, a, b)
    k = a
    if 0.36 < t < 0.64 and BAYER[y % 2][x % 2] < t:   # ちょうどあいだの所だけ、市松でまぜる
        k = b
    idx[y][x] = k
# うすい雲（ふち）: 市松で半分だけ、明るめの色を置く
light = sorted(range(32), key=lambda i: -sum(colors[i]))
for y in range(h):
    for x in range(w):
        if thin[y][x] and (x, y) in near and (x, y) not in body and (x + y) % 2 == 0:
            c = px[x, y]
            # 空の青が少しまざった色に近い、雲の色
            a, _ = two_nearest((min(255, c[0] + 20), min(255, c[1] + 16), c[2]))
            idx[y][x] = a
# ぽつんと1ドットの色（市松でないもの）を、まわりの色に
for y in range(1, h - 1):
    for x in range(1, w - 1):
        k = idx[y][x]
        if k < 0 or (x, y) not in body:
            continue
        nb = [idx[y][x - 1], idx[y][x + 1], idx[y - 1][x], idx[y + 1][x]]
        dg = [idx[y - 1][x - 1], idx[y + 1][x + 1], idx[y - 1][x + 1], idx[y + 1][x - 1]]
        if all(n != k for n in nb) and -1 not in nb and k not in dg:
            idx[y][x] = max(set(nb), key=nb.count)
keys = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef"
rows = ["." * SW] * (S - h) + ["".join(keys[k] if k >= 0 else "." for k in r) for r in idx]
used = sorted(set("".join(rows)) - {"."})
open("shape.txt", "w").write("\n".join(rows) + "\n")
json.dump({keys[i]: "#%02x%02x%02x" % colors[i] for i in range(32) if keys[i] in used}, open("pal-shape.json", "w"))
im = Image.new("RGBA", (SW, S), (0, 0, 0, 0))
for y, r in enumerate(rows):
    for x, ch in enumerate(r):
        if ch != ".":
            im.putpixel((x, y), colors[keys.index(ch)] + (255,))
im.save("shape.png")
print("ok colors", len(used))
