"""第4版の切り抜き（体はよい）に、腹びれのまわりだけ、色の割合で空を外す直しをかける。"""
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as nd
a = np.load("base512.npy"); fg = np.load("whale512_v3.npy"); H, W = fg.shape
lum = a @ [0.3, 0.59, 0.11]; ratio = a[..., 0] / (a[..., 2] + 1)
YY, XX = np.mgrid[0:H, 0:W]
box = (XX >= 222) & (XX <= 292) & (YY >= 108) & (YY <= 133)
keep = (ratio >= 0.36) & (YY <= 126) | (lum > 62) & (YY <= 127)
fg = np.where(box, fg & keep, fg)
fg = nd.binary_closing(fg, iterations=1)
lab, n = nd.label(fg); fg = lab == (np.argmax(nd.sum(fg, lab, range(1, n + 1))) + 1)
fg = nd.binary_fill_holes(fg)
fg &= ~(box & ~(nd.binary_erosion(fg) | keep))
np.save("whale512.npy", fg)
x0, y0, x1, y1, s = 215, 100, 295, 134, 12
c = np.clip(a[y0:y1, x0:x1] * 2.0, 0, 255).astype(np.uint8); o = c.copy(); o[~fg[y0:y1, x0:x1]] = [40, 200, 40]
Image.fromarray(np.vstack([c, o])).resize(((x1 - x0) * s, (y1 - y0) * 2 * s), Image.NEAREST).save("finfix.png")
x0, y0, x1, y1 = 170, 34, 372, 134
o = a[y0:y1, x0:x1].copy(); o[~fg[y0:y1, x0:x1]] = [40, 200, 40]
Image.fromarray(o.astype(np.uint8)).resize(((x1 - x0) * 6, (y1 - y0) * 6), Image.NEAREST).save("wm2.png")
print(fg.sum())
