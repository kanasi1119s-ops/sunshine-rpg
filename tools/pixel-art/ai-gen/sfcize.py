"""絵画風の下絵を、スーファミ後期の敵グラフィックのような手触りのドット絵にする。
1) AIで背景を切り抜く 2) 少しシャープにして縮小 3) Lab空間のk-meansで減色
4) 孤立点を消す 5) 外周に「その部分の色を暗くした」縁取り（黒一色にしない）
6) 左上から光が当たる縁にハイライト 7) 全体を最終の色数に再減色（エディタの上限26色以内）
出力: PNG と、エディタで描くための文字グリッド(.txt)・パレット(.json)
使い方: python3 tools/pixel-art/ai-gen/sfcize.py 下絵.png 出力名 [大きさ=96] [色数=20]
（出力名.png・出力名.txt（エディタ用の文字グリッド）・出力名.json（パレット）ができる。エディタで描くときは tools/pixel-practice/editor-draw.mjs）
"""
import sys, json
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
from scipy import ndimage
from skimage import color as skc
from sklearn.cluster import KMeans
from pixelize import remove_bg_ai  # 同じフォルダの pixelize.py

src, out = sys.argv[1], sys.argv[2]
SIZE = int(sys.argv[3]) if len(sys.argv) > 3 else 96
NCOL = int(sys.argv[4]) if len(sys.argv) > 4 else 20


def kmeans_lab(rgb, k, seed=0):
    lab = skc.rgb2lab(rgb.reshape(-1, 1, 3) / 255.0).reshape(-1, 3)
    km = KMeans(k, n_init=4, random_state=seed).fit(lab)
    cent = skc.lab2rgb(km.cluster_centers_.reshape(-1, 1, 3)).reshape(-1, 3)
    return np.clip(cent * 255 + 0.5, 0, 255).astype(np.uint8), km.labels_


im = remove_bg_ai(Image.open(src))
im = im.crop(im.getbbox())
rgb = im.convert("RGB").filter(ImageFilter.UnsharpMask(radius=2, percent=80, threshold=2))
rgb = ImageEnhance.Contrast(rgb).enhance(1.12)
rgb = ImageEnhance.Color(rgb).enhance(1.1)
im = Image.merge("RGBA", (*rgb.split(), im.split()[3]))
w, h = im.size
s = (SIZE - 4) / max(w, h)
tw, th = max(1, round(w * s)), max(1, round(h * s))
small = np.asarray(im.resize((tw, th), Image.LANCZOS)).astype(np.float32)
alpha = small[:, :, 3] >= 128
alpha = ndimage.binary_opening(alpha, iterations=1) | (ndimage.binary_erosion(alpha, iterations=1))
lab_, n = ndimage.label(alpha)
if n > 1:
    sizes = ndimage.sum(alpha, lab_, range(1, n + 1))
    alpha = np.isin(lab_, [i + 1 for i, v in enumerate(sizes) if v >= max(6, sizes.max() * 0.02)])
filled = ndimage.binary_fill_holes(alpha)
hl, hn = ndimage.label(filled & ~alpha)
if hn:  # 小さな穴だけ埋める（足のあいだなど大きなすき間は透明のまま）
    hs = ndimage.sum(np.ones_like(alpha), hl, range(1, hn + 1))
    alpha = alpha | np.isin(hl, [i + 1 for i, v in enumerate(hs) if v <= 12])

# 3) 減色（形と陰影の段をはっきりさせる）
pal, lab = kmeans_lab(small[:, :, :3][alpha], NCOL - 4)
img = np.zeros((th, tw, 3), np.float32)
img[alpha] = pal[lab]


# 4) 孤立点を消す（8近傍に同じ色が1つも無い点 → 近傍でいちばん多い色）
def orphans(img, alpha):
    out = img.copy()
    H, W = alpha.shape
    for y in range(H):
        for x in range(W):
            if not alpha[y, x]:
                continue
            c = tuple(img[y, x]); same = 0; nb = {}
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dy == dx == 0:
                        continue
                    yy, xx = y + dy, x + dx
                    if 0 <= yy < H and 0 <= xx < W and alpha[yy, xx]:
                        cc = tuple(img[yy, xx])
                        if cc == c:
                            same += 1
                        nb[cc] = nb.get(cc, 0) + 1
            if same == 0 and nb:
                out[y, x] = max(nb, key=nb.get)
    return out


img = orphans(img, alpha)

# 5) 縁取り: 透明に接する外周を、その色の暗い版に（色相を残す。黒一色にしない）
pad = np.pad(alpha, 1)
edge = alpha & ~(pad[:-2, 1:-1] & pad[2:, 1:-1] & pad[1:-1, :-2] & pad[1:-1, 2:])
img[edge] = img[edge] * np.array([0.38, 0.36, 0.45]) + np.array([4, 3, 10])
# 6) 左上からの光: 上か左が透明な外周の1つ内側を明るく（縁の内側の照り）
up_open = alpha & ~pad[:-2, 1:-1]
left_open = alpha & ~pad[1:-1, :-2]
lit_edge = (up_open | left_open) & edge
rim = np.zeros_like(alpha)
rim[1:, :] |= lit_edge[:-1, :] & up_open[:-1, :]
rim[:, 1:] |= lit_edge[:, :-1] & left_open[:, :-1]
rim &= alpha & ~edge
img[rim] = np.clip(img[rim] * 1.28 + 18, 0, 255)

# 7) 最終の色数に再減色
pal2, lab2 = kmeans_lab(img[alpha], NCOL, seed=1)
final = np.zeros((th, tw, 3), np.uint8)
final[alpha] = pal2[lab2]
final = orphans(final.astype(np.float32), alpha).astype(np.uint8)

canvas = np.zeros((SIZE, SIZE, 4), np.uint8)
ox, oy = (SIZE - tw) // 2, SIZE - 2 - th
canvas[oy:oy + th, ox:ox + tw, :3] = final
canvas[oy:oy + th, ox:ox + tw, 3] = alpha * 255
Image.fromarray(canvas, "RGBA").save(out + ".png")

# エディタ用の文字グリッドとパレット
names = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
cols = {}
rows = []
for y in range(SIZE):
    r = ""
    for x in range(SIZE):
        p = canvas[y, x]
        if p[3] < 128:
            r += "."; continue
        k = tuple(int(v) for v in p[:3])
        if k not in cols:
            cols[k] = names[len(cols)]
        r += cols[k]
    rows.append(r)
open(out + ".txt", "w").write("\n".join(rows) + "\n")
json.dump({v: "#%02x%02x%02x" % k for k, v in cols.items()}, open(out + ".json", "w"))
print(out, tw, th, len(cols), "色")
