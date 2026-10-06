"""（試し5）雲を増やさずに、元の雲（写真の雲1つ）の形を変える（2026-10-06、人間の指示「増やすんじゃなくて、元のやつの形を変えよう」）。
雲は1つだけ。行ごとにのばす方法（shape.py、不採用）ではなく、雲の「かたまり」（頭・左の翼・右のこぶ）を、
それぞれまるごと動かす（かたまりの中の模様は、ほとんどそのまま動く。動かしたかたまりのつなぎ目だけ、なめらかにずれる）:
  頭（上の白いもくもく）: 上へ、少し右へ。雲が高くそびえ、右へかたむく。
  左の翼（暗い平たい雲）: 左へ、少し下へ。
  右のこぶ: 上へ、外へ。
2026-10-06 追記（人間の指示「中央左側に暗い雲を足して」）: 写真の左の暗い平たい雲（翼）を切り出し、まん中の左の前に、ふちをぼかして重ねる。
2026-10-06 追記（人間の指示「さらに雲の上部、周りに雲を足して」）: 写真の雲の白い頭（上と横は雲のもとのふち）を小さくして、
（人間の指示「くもの足し方、前のほうがよかったな」で）採用した雲と同じく、上へ段に重ねる（うしろ）。下のはしは本体のうしろへ入るように消す。
重ねた絵は composite5.png（480×384、空は写真の空の色）。ドットにするのは reshape.py（python3 reshape.py composite5.png reshape5）。"""
import numpy as np
from PIL import Image

photo = Image.open("ref-photo.png").convert("RGB")
crop = np.asarray(photo.crop((28, 0, 412, 262)), float)
SKY = np.array([32, 62, 120], float)
CW, CH = 480, 384
OX, OY = 48, CH - 262
# (かたまりの中心（写真の切り出しの中の位置）, 動かす量, 広さ)
HANDLES = [
    ((190, 70), (26, -64), 105),
    ((40, 192), (-34, 14), 58),
    ((360, 146), (22, -30), 42),
]
yy, xx = np.mgrid[0:CH, 0:CW].astype(float)
dx = np.zeros((CH, CW)); dy = np.zeros((CH, CW))
for (hx, hy), (mx, my), s in HANDLES:
    cx, cy = hx + OX + mx, hy + OY + my          # 動かしたあとの中心のまわりで、もとの場所を引く
    w = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * s * s))
    dx += w * mx; dy += w * my
sx = xx - dx - OX; sy = yy - dy - OY
x0 = np.floor(sx).astype(int); y0 = np.floor(sy).astype(int)
fx = (sx - x0)[..., None]; fy = (sy - y0)[..., None]


def at(x, y):
    ok = (x >= 0) & (x < crop.shape[1]) & (y >= 0) & (y < crop.shape[0])
    v = crop[np.clip(y, 0, crop.shape[0] - 1), np.clip(x, 0, crop.shape[1] - 1)]
    return np.where(ok[..., None], v, SKY)


out = (at(x0, y0) * (1 - fx) * (1 - fy) + at(x0 + 1, y0) * fx * (1 - fy)
       + at(x0, y0 + 1) * (1 - fx) * fy + at(x0 + 1, y0 + 1) * fx * fy)
# 中央左の暗い雲（写真の左の翼の、暗い所。ふちはだ円でぼかし、空の色の所はのせない）
DARK_BOX = (6, 166, 126, 222)                      # 写真の切り出しの中の範囲
DARK_AT = (118, 226)                              # 置く所（重ねた絵の中の左上）
pc = crop[DARK_BOX[1]:DARK_BOX[3], DARK_BOX[0]:DARK_BOX[2]]
pc = np.asarray(Image.fromarray(pc.astype(np.uint8)).resize((int(pc.shape[1] * 1.35), int(pc.shape[0] * 1.35)), Image.LANCZOS), float)   # ひとまわり大きく
ph, pw = pc.shape[:2]
py, px_ = np.mgrid[0:ph, 0:pw].astype(float)
u = (px_ + 0.5 - pw / 2) / (pw / 2); v = (py + 0.5 - ph / 2) / (ph / 2)
ell = np.clip((1 - np.sqrt(u * u + v * v)) / 0.45, 0, 1)
sky_like = np.clip((78 - (pc[..., 2] - pc[..., 0])) / 34, 0, 1)
lum = pc.mean(-1)
dark = np.clip((150 - lum) / 60, 0, 1)            # 暗い所ほど濃くのせる
a = (ell * sky_like * (0.35 + 0.65 * dark))[..., None]
y0_, x0_ = DARK_AT[1], DARK_AT[0]
out[y0_:y0_ + ph, x0_:x0_ + pw] = out[y0_:y0_ + ph, x0_:x0_ + pw] * (1 - a) + pc * a
# 上のまわりの雲（うしろ）: 先にうしろの絵を作り、その上に本体をのせる
from PIL import ImageFilter


def cloudness(img):
    return np.clip((78 - (img[..., 2] - img[..., 0])) / 34, 0, 1)


back = np.zeros((CH, CW, 3)) + SKY
dome = Image.fromarray(crop[0:150].astype(np.uint8))
TOPS = [   # (左右入れかえ, 大きさ, 置く所（左上）, 下の消えはじめ)
    # 2026-10-06 人間の指示「くもの足し方、前のほうがよかったな」: 小さな雲をまわりに散らすのをやめ、
    # 採用した雲（reshape3）と同じ足し方にした。白い頭を上へ段に重ねる（2段目は左右入れかえ、3段目はさらに小さく）。
    (True, 0.64, (124, 44), 0.75),
    (False, 0.42, (178, 10), 0.75),
]
for flip, sc, (px0, py0), st in TOPS:
    d = dome.transpose(Image.FLIP_LEFT_RIGHT) if flip else dome
    d = np.asarray(d.resize((int(384 * sc), int(150 * sc)), Image.LANCZOS), float)
    hh, ww = d.shape[:2]
    a = cloudness(d)
    fade = np.clip(1 - (np.arange(hh) - hh * st) / (hh * (1 - st)), 0, 1)[:, None]
    a = (a * np.minimum(1, fade))[..., None]
    reg = back[py0:py0 + hh, px0:px0 + ww]
    back[py0:py0 + hh, px0:px0 + ww] = reg * (1 - a[:reg.shape[0], :reg.shape[1]]) + d[:reg.shape[0], :reg.shape[1]] * a[:reg.shape[0], :reg.shape[1]]
am = np.asarray(Image.fromarray((cloudness(out) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)), float)[..., None] / 255
out = back * (1 - am) + out * am
Image.fromarray(out.clip(0, 255).astype(np.uint8)).save("composite5.png")
print("ok")
