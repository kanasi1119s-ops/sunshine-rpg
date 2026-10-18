"""鯨の切り抜き 第4版（2026-10-18「体の一部がなくなってる」「背景が上についている」「尾びれと背びれの間に背景」「おなかの前のヒレが欠けている」）。
元の絵を明るくして 8 倍で見て、体の形を読み直した:
  - 体の後ろ半分の下のふちは、明るい斜めの線（尾の下へ続く）。その線より下は空（星がある）。
  - 胸びれ（長い）: 体の下から右下へ細長くのびる。上のふちが明るい。
  - もう片方の胸びれ（小さい）: 腹の下に少し見える。
GrabCut（色で前後を分ける）で体を取り、そのあと上の3つを手で合わせる。"""
import numpy as np, cv2
from PIL import Image
from scipy import ndimage as nd
a = np.load("base512.npy"); H, W, _ = a.shape
img = np.clip(a, 0, 255).astype(np.uint8); lum = a @ [0.3, 0.59, 0.11]
YY, XX = np.mgrid[0:H, 0:W]
poly = lambda pts: cv2.fillPoly(np.zeros((H, W), np.uint8), [np.array(pts, np.int32)], 1).astype(bool)
BODY = [(175,105),(186,98),(206,91),(244,81),(279,62),(300,53),(320,48),(337,47),(344,41),(353,39),(350,49),(366,57),(363,61),(349,60),(335,58),(318,62),(312,66),
        (260,111),(245,115),(232,121),(206,117),(184,112)]
FIN = [(238,110),(246,112),(256,115),(266,118),(276,121),(284,124),(286,127),(276,128),(262,126),(250,124),(241,121),(236,117)]
SMALL = [(228,121),(238,122),(247,125),(244,129),(234,128),(228,125)]
pm = poly(BODY)
mask = np.full((H, W), cv2.GC_BGD, np.uint8)
mask[nd.binary_dilation(pm, iterations=4)] = cv2.GC_PR_BGD
mask[pm] = cv2.GC_PR_FGD
mask[nd.binary_erosion(pm, iterations=3)] = cv2.GC_FGD
bgm = np.zeros((1, 65)); fgm = np.zeros((1, 65))
cv2.grabCut(img, mask, None, bgm, fgm, 8, cv2.GC_INIT_WITH_MASK)
fg = ((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD))
# 体の後ろの下のふち（明るい斜めの線）より下は空
below = poly([(265, 117), (318, 68), (340, 68), (340, 140), (265, 140)])
fg &= ~below
fg |= poly(FIN)
fg |= poly(SMALL) & (lum > 30)
fg = nd.binary_closing(fg, iterations=1)
lab, n = nd.label(fg); fg = lab == (np.argmax(nd.sum(fg, lab, range(1, n + 1))) + 1)
fg = nd.binary_fill_holes(fg)
# 尾びれのつけ根・背中のふちに入りこんだ暗い空（鯨のいちばん暗い所より暗い）と、ふちの星のでっぱりを外す
zone = (XX >= 284) & (YY < 72)
for _ in range(3):
    e2 = fg & ~nd.binary_erosion(fg, iterations=2)
    sky_px = e2 & zone & (lum < 27)
    if not sky_px.any(): break
    fg &= ~sky_px
fg[45:50, 303:310] = False   # 背中の上の星のでっぱり
star = fg & (lum > 95) & ~nd.binary_erosion(fg, iterations=1)
nb = nd.convolve(fg.astype(int), np.ones((3, 3), int), mode="constant")
fg &= ~(star & (nb <= 5) & ~poly(FIN) & ~poly(SMALL))
lab, n = nd.label(fg); fg = lab == (np.argmax(nd.sum(fg, lab, range(1, n + 1))) + 1)
fg = nd.binary_fill_holes(fg)
np.save("whale512.npy", fg)
x0, y0, x1, y1 = 170, 34, 372, 134
o = a[y0:y1, x0:x1].copy(); o[~fg[y0:y1, x0:x1]] = [40, 200, 40]
Image.fromarray(o.astype(np.uint8)).resize(((x1 - x0) * 6, (y1 - y0) * 6), Image.NEAREST).save("wm2.png")
print(fg.sum())
