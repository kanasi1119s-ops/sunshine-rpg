"""積乱雲を、横に広げる（2026-10-05、人間の指示「この感じを崩さないで形を変えて。横に広げるように」）。
natural.py と同じ作り方で、縦の高さはそのまま、横だけ 1.375 倍（256 → 352）にのばしてから、ドットにする
（のばしたあとでドットにするので、ドットはつぶれない）。絵は 352×256。前の版は cumulonimbus-v2.*。

以下は natural.py の説明: 積乱雲のトレースを、少し自然にする（2026-10-05、人間の指示「これを少し自然な感じにして」）。
trace.py の版（cumulonimbus-v1.*）は、色の面がまだらで、色の境と外のふちがぎざぎざだった。ここでは:
- 縮めたあと、3×3 の中央値でならして、こまかなまだらを消す（形はそのまま）。
- 色は 32 色。となり合う2色のあいだの色は、2×2 の市松で1ドットずつまぜる（なめらかなグラデーション）。
  まぜるのは、ちょうどあいだの所だけ（ざらざらにしない）。
- 外のふちは、空と雲がまざる所（写真で少し青い所）を、市松の「うすい雲」にする（ふちがやわらかく、少し透けて見える）。
- 底は、まっすぐ切れないよう、下へ行くほどうすくして、市松で消えていくようにする。
空はとうめい。雲の本体だけ。256×256（下にそろえる）。"""
import json
import math
from PIL import Image, ImageFilter

src = Image.open("ref-photo.png").convert("RGB")
crop = src.crop((28, 0, 412, 262))
h = round(crop.height * 256 / crop.width)
w = 352
small = crop.resize((w, h), Image.LANCZOS).filter(ImageFilter.MedianFilter(3))
px = small.load()
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
open("cumulonimbus.txt", "w").write("\n".join(rows) + "\n")
json.dump({keys[i]: "#%02x%02x%02x" % colors[i] for i in range(32) if keys[i] in used}, open("pal-cumulonimbus.json", "w"))
im = Image.new("RGBA", (SW, S), (0, 0, 0, 0))
for y, r in enumerate(rows):
    for x, ch in enumerate(r):
        if ch != ".":
            im.putpixel((x, y), colors[keys.index(ch)] + (255,))
im.save("cumulonimbus.png")
print("ok colors", len(used))
