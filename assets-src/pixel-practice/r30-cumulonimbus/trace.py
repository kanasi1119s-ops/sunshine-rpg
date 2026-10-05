"""積乱雲のトレース（2026-10-05、人間の指示「さっきの画像トレースしてみて 256×256 で」「エディタ使ってね」）。
人間が見せた積乱雲の写真（ref-photo.png）を、256×256 のドット絵に写す。
- 雲のある所（x 28〜412）を切り出し、横幅 256 に合わせて縮める（縦横の比はそのまま。下にそろえ、上はあける）。
- 空（青）は、とうめいにする。いちばん下の地面は切り出さない。雲の本体（いちばん大きなかたまり）だけを残す。
- 色は、雲の色だけから 28 色にしぼる。ぽつんと1ドットだけちがう色は、まわりの色にする。
- 書き出した txt と色の表を、ドット絵エディタに描き入れて PNG にする（tools/pixel-practice/editor-draw.mjs）。"""
import json
from PIL import Image

src = Image.open("ref-photo.png").convert("RGB")
crop = src.crop((28, 0, 412, 262))           # いちばん下の地面（暗い帯）は入れない
w = 256
h = round(crop.height * w / crop.width)
small = crop.resize((w, h), Image.LANCZOS)
S = 256
px = small.load()

def is_sky(r, g, b, y):
    if b - r > 62 and b > 70:
        return True
    if y > h - 8 and r + g + b < 70:
        return True
    return False

mask = [[not is_sky(*px[x, y], y) for x in range(w)] for y in range(h)]
# 小さな穴・小さな点をなくす（まわり8つの多数決を2回）
for _ in range(2):
    nm = [row[:] for row in mask]
    for y in range(h):
        for x in range(w):
            c = sum(mask[yy][xx] for yy in range(max(0, y - 1), min(h, y + 2)) for xx in range(max(0, x - 1), min(w, x + 2)))
            nm[y][x] = c >= 5
    mask = nm
# 雲の本体（いちばん大きなかたまり）だけを残す（すみの空のかけらを消す）
seen = [[False] * w for _ in range(h)]
best = []
for y0 in range(h):
    for x0 in range(w):
        if mask[y0][x0] and not seen[y0][x0]:
            comp, st = [], [(x0, y0)]
            seen[y0][x0] = True
            while st:
                x, y = st.pop()
                comp.append((x, y))
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < w and 0 <= ny < h and mask[ny][nx] and not seen[ny][nx]:
                        seen[ny][nx] = True
                        st.append((nx, ny))
            if len(comp) > len(best):
                best = comp
mask = [[False] * w for _ in range(h)]
for x, y in best:
    mask[y][x] = True
# 色を28色に
cloud = Image.new("RGB", (w, h))
pts = [px[x, y] for y in range(h) for x in range(w) if mask[y][x]]
cloud.putdata(pts + [pts[0]] * (w * h - len(pts)))
pal_img = cloud.quantize(colors=28, method=Image.MEDIANCUT)
pal = pal_img.getpalette()[:28 * 3]
colors = [tuple(pal[i * 3:i * 3 + 3]) for i in range(28)]

def nearest(c):
    return min(range(len(colors)), key=lambda i: sum((colors[i][k] - c[k]) ** 2 for k in range(3)))

idx = [[nearest(px[x, y]) if mask[y][x] else -1 for x in range(w)] for y in range(h)]
for _ in range(2):
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            k = idx[y][x]
            if k < 0:
                continue
            nb = [idx[y][x - 1], idx[y][x + 1], idx[y - 1][x], idx[y + 1][x]]
            if all(n != k for n in nb) and -1 not in nb:
                idx[y][x] = max(set(nb), key=nb.count)
keys = "ABCDEFGHIJKLMNOPQRSTUVWXYZab"
top = S - h
rows = ["." * S] * top + ["".join(keys[k] if k >= 0 else "." for k in r) for r in idx]
used = sorted(set("".join(rows)) - {"."})
open("cumulonimbus.txt", "w").write("\n".join(rows) + "\n")
json.dump({keys[i]: "#%02x%02x%02x" % colors[i] for i in range(28) if keys[i] in used}, open("pal-cumulonimbus.json", "w"))
print("ok", S, len(rows), "colors", len(used))
