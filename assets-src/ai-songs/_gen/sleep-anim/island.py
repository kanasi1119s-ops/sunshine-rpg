"""島（家・木・岩・ランタン）を、鯨より手前に重ねるための形（2026-10-18: 鯨が家の屋根に重なって家を隠していたため。鯨は島の向こうの空を泳ぐ）。"""
import numpy as np, cv2
from PIL import Image
from scipy import ndimage as nd
b = np.load("bg.npy"); H, W, _ = b.shape
img = np.clip(b, 0, 255).astype(np.uint8)
lum = b @ [0.3, 0.59, 0.11]; ratio = b[..., 0] / (b[..., 2] + 1)
mask = np.full((H, W), cv2.GC_BGD, np.uint8)
YY, XX = np.mgrid[0:H, 0:W]
roi = (XX >= 318) & (XX <= 480) & (YY >= 74) & (YY <= 140)
mask[roi] = cv2.GC_PR_BGD
core = (ratio > 0.55) & roi & (YY > 84)          # 家の壁・木・岩（空より赤み・緑み）
mask[core] = cv2.GC_PR_FGD
mask[nd.binary_erosion(core, iterations=2)] = cv2.GC_FGD
mask[(YY >= 128) & (XX >= 330) & (XX <= 470) & (YY <= 140) & (ratio > 0.4)] = cv2.GC_FGD
bgm = np.zeros((1, 65)); fgm = np.zeros((1, 65))
cv2.grabCut(img, mask, None, bgm, fgm, 8, cv2.GC_INIT_WITH_MASK)
fg = ((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD)) & roi
fg = nd.binary_closing(fg, iterations=1)
lab, n = nd.label(fg); sz = nd.sum(fg, lab, range(1, n + 1)); fg = np.isin(lab, np.where(sz >= 6)[0] + 1)
fg = nd.binary_fill_holes(fg)
skyl = fg & (ratio < 0.36) & (lum < 75)            # 屋根と木のあいだ・木の下の空（大きなかたまり・外とつながる所）だけ外す。影の小さな点は残す
lab, n = nd.label(skyl); sz = nd.sum(skyl, lab, range(1, n + 1))
outer = np.unique(lab[skyl & ~nd.binary_erosion(fg)]); 
fg &= ~np.isin(lab, np.union1d(np.where(sz >= 25)[0] + 1, outer[outer > 0]))
lab, n = nd.label(fg); sz = nd.sum(fg, lab, range(1, n + 1)); fg = np.isin(lab, np.where(sz >= 6)[0] + 1)
fg[YY > 140] = False     # 水面より下は不要（鯨はそこまで下りない）
np.save("island.npy", fg)
Image.fromarray((fg * 255).astype(np.uint8)).resize((W * 4, H * 4), Image.NEAREST).save("islandmask.png")
v = b.copy(); v[~fg] = v[~fg] * 0.3 + np.array([255, 0, 0]) * 0.4
Image.fromarray(v[60:150, 300:500].astype(np.uint8)).resize((1200, 540), Image.NEAREST).save("island-chk.png")
print(fg.sum())
