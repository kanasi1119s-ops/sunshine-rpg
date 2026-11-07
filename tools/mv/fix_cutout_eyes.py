# テトの切り抜きの顔の中にあいた穴（目のまわりが透明になっている所）を埋める。
# 顔の肌の色の領域を「穴埋め」した範囲の内側にある、透明な小さい穴だけを、まわりの色で埋めて不透明にする。
import sys, glob, numpy as np, cv2
from PIL import Image
from scipy import ndimage
src, dst = sys.argv[1], sys.argv[2]
tot = 0
for f in sorted(glob.glob(src + '/*.png')):
    im = np.array(Image.open(f)); a = im[:, :, 3]; rgb = im[:, :, :3].astype(int)
    H = im.shape[0]
    skin = (rgb[:, :, 0] > 190) & (rgb[:, :, 1] > 150) & (rgb[:, :, 2] > 120) & (rgb[:, :, 0] - rgb[:, :, 2] < 90) & (a > 200)
    skin[int(H * 0.35):] = False                       # 頭のあたりだけ
    lab, n = ndimage.label(skin)
    if n == 0: Image.fromarray(im).save(f.replace(src, dst)); continue
    big = 1 + int(np.argmax(ndimage.sum(skin, lab, range(1, n + 1))))
    face = ndimage.binary_fill_holes(ndimage.binary_closing(lab == big, iterations=6))
    hole = (a < 250) & face
    hl, hn = ndimage.label(hole)
    mask = np.zeros(a.shape, np.uint8)
    for i in range(1, hn + 1):
        m = hl == i
        if m.sum() <= 400: mask[m] = 255
    if mask.any():
        mask = cv2.dilate(mask, np.ones((3, 3), np.uint8))
        fixed = cv2.inpaint(cv2.cvtColor(im[:, :, :3], cv2.COLOR_RGB2BGR), mask, 4, cv2.INPAINT_TELEA)
        im[:, :, :3] = np.where(mask[..., None] > 0, cv2.cvtColor(fixed, cv2.COLOR_BGR2RGB), im[:, :, :3])
        im[:, :, 3] = np.where(mask > 0, 255, a)
        tot += 1
    Image.fromarray(im).save(f.replace(src, dst))
print('穴を埋めたコマ', tot)
