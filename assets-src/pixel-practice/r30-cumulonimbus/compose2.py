"""（試し2）採用した積乱雲の感じのまま、形をガラッと変える（2026-10-05、人間の指示「感じを崩さないで、形をガラッと試しに変えてみて」）。
compose.py と同じく、写真の雲の一部分を、ゆがめずに切り出して重ねる。今回は、横長の雲を、上へ段になってそびえる塔のような雲にする（雲が上へ上へとわき上がっていく形）:
  本体（いちばんまえ）: 写真の雲ぜんぶを少し小さく。
  2段目: 写真の雲の上半分（白い頭）を左右入れかえて、小さく、本体のうしろの上に。
  3段目: 同じ頭を、さらに小さく、いちばん上に。
切り出すのは、横と上が雲のもとのふちになる所だけ（雲の中を切ったふちは不自然なので使わない）。下のはしだけ、
下の段の雲のうしろへ入るように、だんだん消す。
重ねた絵は composite2.png（空は写真の空の色）。ドットにするのは reshape.py（python3 reshape.py composite2.png reshape2）。"""
import math
from PIL import Image, ImageFilter

photo = Image.open("ref-photo.png").convert("RGB")
crop = photo.crop((28, 0, 412, 262))
SKY = (32, 62, 120)
import sys
WIDE = len(sys.argv) > 1 and sys.argv[1] == "wide"     # 横にも雲を足す版（試し3）
CW, CH = (480 if WIDE else 384), 384
OX = 48 if WIDE else 0                          # 横に広げた分、まん中へずらす


def alpha_of(img, top_rows=0):
    a = Image.new("L", img.size)
    src = img.load()
    out = a.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = src[x, y]
            v = (78 - (b - r)) / 34
            if y < top_rows and b - r > 28:
                v = 0
            if r + g + b < 30:
                v = 0
            out[x, y] = int(max(0.0, min(1.0, v)) * 255)
    return a.filter(ImageFilter.GaussianBlur(0.6))


def feather(a, cy=0.4, soft=0.28, bottom=True):
    """だ円の形で、はしをやわらかく消す。bottom=False なら、下のはしは消さない（いちばんまえの雲）。"""
    m = a.load()
    w, h = a.size
    for y in range(h):
        for x in range(w):
            u = (x + 0.5 - w / 2) / (w / 2)
            v = (y + 0.5 - h * cy) / (h * (1 - cy))
            if not bottom:
                v = min(v, 0.0)
            vv = (y + 0.5 - h * cy) / (h * cy) if y < h * cy else v
            d = math.sqrt(u * u + (min(0.0, vv) ** 2) * 0.6 + max(0.0, v) ** 2)
            f = max(0.0, min(1.0, (1.0 - d) / soft))
            m[x, y] = int(m[x, y] * f)
    return a


def piece(box, scale, top_rows=0):
    p = crop.crop(box)
    if scale != 1:
        p = p.resize((int(p.width * scale), int(p.height * scale)), Image.LANCZOS)
    return p, alpha_of(p, top_rows)


def fade_bottom(a, start=0.55):
    """下のほうだけを、だんだん消す（下の段の雲のうしろへ入る所）。横と上は、雲のもとのふちのまま。"""
    m = a.load()
    w, h = a.size
    for y in range(h):
        f = 1.0 if y < h * start else max(0.0, 1 - (y - h * start) / (h * (1 - start)))
        for x in range(w):
            m[x, y] = int(m[x, y] * f)
    return a


canvas = Image.new("RGB", (CW, CH), SKY)
dome = crop.crop((0, 0, 384, 150))              # 写真の雲の上半分（白い頭。横と上は、雲のもとのふち）
# 横の雲（試し3）: 本体のうしろの左右に、白い頭を小さく置く（本体の横から、もくもくがはみ出して広がる）
if WIDE:
    sl = dome.resize((int(384 * 0.5), int(150 * 0.5)), Image.LANCZOS)
    canvas.paste(sl, (8, 196), fade_bottom(alpha_of(sl, 999), 0.7))
    sr = dome.transpose(Image.FLIP_LEFT_RIGHT).resize((int(384 * 0.44), int(150 * 0.44)), Image.LANCZOS)
    canvas.paste(sr, (CW - sr.width - 6, 214), fade_bottom(alpha_of(sr, 999), 0.7))
    lo = dome.resize((int(384 * 0.36), int(150 * 0.36)), Image.LANCZOS)
    canvas.paste(lo, (CW - lo.width - 30, 288), fade_bottom(alpha_of(lo, 999), 0.75))
# いちばん上の段（いちばんうしろ・小さい）
d3 = dome.resize((int(384 * 0.42), int(150 * 0.42)), Image.LANCZOS)
canvas.paste(d3, (150 + OX, 62), fade_bottom(alpha_of(d3, 999), 0.75))
# 2段目（左右を入れかえて、くり返しに見えないように）
d2 = dome.transpose(Image.FLIP_LEFT_RIGHT).resize((int(384 * 0.66), int(150 * 0.66)), Image.LANCZOS)
canvas.paste(d2, (90 + OX, 98), fade_bottom(alpha_of(d2, 999), 0.78))
# 本体（いちばんまえ）
body = crop.resize((int(384 * 0.9), int(262 * 0.9)), Image.LANCZOS)
canvas.paste(body, (14 + OX, CH - body.height), alpha_of(body, 100))
canvas.save("composite3.png" if WIDE else "composite2.png")
print("ok")
