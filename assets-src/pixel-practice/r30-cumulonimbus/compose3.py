"""（試し4）採用した雲（reshape3）の感じのまま、形を試しに変える（2026-10-06、人間の指示「参考にして作ったやつの形を試しに変えたバージョンを作って」）。
compose2.py と同じく、写真の雲の一部分を、ゆがめずに切り出して重ねる（のばしたりゆがめたりはしない）。今回は、
上が横へ平たく大きく広がり（かなとこ形）、まん中がくびれ、下に本体がある形にする:
  上の広がり: 白い頭を、左に1つ・左右入れかえて右に1つ、少し上へずらして横にならべる。まん中のうしろにも小さく1つ。
  くびれ: 白い頭を小さく、まん中に。
  本体（いちばんまえ）: 写真の雲ぜんぶを、少し小さく、やや左に。
  横: 左下に小さな雲、右下に小さな雲。
重ねた絵は composite4.png。ドットにするのは reshape.py（python3 reshape.py composite4.png reshape4）。"""
import math
from PIL import Image, ImageFilter

photo = Image.open("ref-photo.png").convert("RGB")
crop = photo.crop((28, 0, 412, 262))
SKY = (32, 62, 120)
import sys
CW, CH = 480, 384


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
flip = dome.transpose(Image.FLIP_LEFT_RIGHT)


def put(img, scale, x, y, start):
    p = img.resize((int(384 * scale), int(150 * scale)), Image.LANCZOS)
    canvas.paste(p, (x, y), fade_bottom(alpha_of(p, 999), start))


# 横の小さな雲（いちばんうしろ）
put(dome, 0.38, 20, 232, 0.8)
put(flip, 0.34, CW - 146, 220, 0.8)
# 上の広がり（かなとこ形）: まん中のうしろに1つ、左右に大きく1つずつ。下はくびれのうしろへ入る
put(dome, 0.5, 144, 62, 0.85)
put(dome, 0.6, 26, 96, 0.85)
put(flip, 0.62, CW - 264, 90, 0.85)
# くびれ（上の広がりと本体のあいだ。下は本体のうしろへ入る）
put(flip, 0.64, 116, 136, 0.85)
# 本体（いちばんまえ、やや左）
body = crop.resize((int(384 * 0.8), int(262 * 0.8)), Image.LANCZOS)
canvas.paste(body, (78, CH - body.height), alpha_of(body, 100))
canvas.save("composite4.png")
print("ok")
