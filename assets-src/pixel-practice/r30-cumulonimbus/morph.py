"""（試し5）雲を増やさずに、元の雲（写真の雲1つ）の形を変える（2026-10-06、人間の指示「増やすんじゃなくて、元のやつの形を変えよう」）。
雲は1つだけ。行ごとにのばす方法（shape.py、不採用）ではなく、雲の「かたまり」（頭・左の翼・右のこぶ）を、
それぞれまるごと動かす（かたまりの中の模様は、ほとんどそのまま動く。動かしたかたまりのつなぎ目だけ、なめらかにずれる）:
  頭（上の白いもくもく）: 上へ、少し右へ。雲が高くそびえ、右へかたむく。
  左の翼（暗い平たい雲）: 左へ、少し下へ。
  右のこぶ: 上へ、外へ。
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
Image.fromarray(out.clip(0, 255).astype(np.uint8)).save("composite5.png")
print("ok")
