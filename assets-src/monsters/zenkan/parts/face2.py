"""全観の顔 第2版（2026-10-06、人間の指示「観音の顔を少し怖い・重い感じに」「頭の感じをもう少し丸く」）
下絵 zenkan_2 の顔（face_src.png）から: 平らな頭の上を丸い形に引きのばし（髪の筋はそのまま）、
金を古びた暗い青銅寄りにして、目のくぼみ・眉の下・頬・口元に重い影を入れる。唇の赤は消す。目は閉じたまま（足さない）。"""
import math, sys
import numpy as np
from PIL import Image
from scipy import ndimage
Z = '/tmp/monster-work/zk/'; O = '/tmp/monster-work/zk2/'
src = np.asarray(Image.open(Z + 'face_src.png').convert('RGB')).astype(float)
H, W = src.shape[:2]
m = src.min(2) < 236
m = ndimage.binary_opening(m, iterations=2)
l, n = ndimage.label(m); sz = ndimage.sum(m, l, range(1, n + 1))
cxs = [ndimage.center_of_mass(l == i + 1)[1] for i in range(n)]
keep = max(range(n), key=lambda i: sz[i])
m = ndimage.binary_fill_holes(l == keep + 1)
# 1) 頭を丸く: 列ごとに、髪の上端を楕円の弧まで引きのばす
cx, base_y = 170.0, 135.0          # 髪の帯の下（ここより下は動かさない）
top_now = np.array([np.argmax(m[:, x]) if m[:, x].any() else H for x in range(W)])
rx, top = 78.0, 52.0                # 丸い頭の横半径と、てっぺんの高さ
out = src.copy(); m2 = m.copy()
for x in range(W):
    dx = (x - cx) / rx
    if abs(dx) >= 1 or top_now[x] >= base_y: continue
    ny = base_y - (base_y - top) * math.sqrt(1 - dx * dx) ** 0.8
    oy = top_now[x]
    if ny >= oy: continue
    for y in range(int(math.ceil(ny)), int(base_y)):
        t = (y - ny) / (base_y - ny)
        sy = oy + t * (base_y - oy)
        y0 = int(sy); f = sy - y0
        out[y, x] = src[y0, x] * (1 - f) + src[min(y0 + 1, H - 1), x] * f
        m2[y, x] = True
img = out
# 2) 重く・こわく: 古びた暗い青銅、強い明暗
lum = img.mean(2, keepdims=True)
bronze = np.array([0.80, 0.66, 0.42])
img = lum * bronze * 1.05 * 0.55 + img * 0.45 * np.array([0.85, 0.78, 0.6])
img = (img - 70) * 1.25 + 60
yy, xx = np.mgrid[0:H, 0:W].astype(float)
def shade(cx_, cy_, rx_, ry_, k):
    d = ((xx - cx_) / rx_) ** 2 + ((yy - cy_) / ry_) ** 2
    return np.where(d < 1, 1 - k * np.clip(1 - d, 0, 1) ** 1.6, 1.0)
mul = np.ones((H, W))
mul *= shade(118, 208, 54, 30, 0.6)   # 目のくぼみ
mul *= shade(222, 208, 54, 30, 0.6)
mul *= shade(118, 190, 44, 9, 0.45)    # 眉の下の影（重いまぶた）
mul *= shade(222, 190, 44, 9, 0.45)
mul *= shade(170, 292, 40, 12, 0.2)   # 口元
mul *= shade(118, 292, 10, 16, 0.5)    # への字の口角
mul *= shade(222, 292, 10, 16, 0.5)
mul *= shade(95, 260, 30, 50, 0.35)    # こけた頬
mul *= shade(245, 260, 30, 50, 0.35)
mul *= shade(170, 345, 70, 30, 0.35)   # あごの下
edge = ndimage.distance_transform_edt(m2)
mul *= np.clip(0.55 + edge / 40, 0.55, 1.0)   # ふちを暗く（重さ）
# 眉間のしわ・ほうれい線・への字の口角の線（暗い線を少しぼかして）
ln = np.zeros((H, W))
def line(pts, w=2.2):
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        for t in np.linspace(0, 1, 60):
            x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t
            ln[int(y)-2:int(y)+3, int(x)-2:int(x)+3] = np.maximum(ln[int(y)-2:int(y)+3, int(x)-2:int(x)+3], 1)
line([(160, 170), (164, 192)]); line([(180, 170), (176, 192)])
line([(140, 245), (128, 268), (126, 290)]); line([(200, 245), (212, 268), (214, 290)])
line([(140, 290), (128, 300)]); line([(200, 290), (212, 300)])
ln = ndimage.gaussian_filter(ln, 1.6)
mul *= 1 - 0.55 * np.clip(ln * 1.6, 0, 1)
img = img * mul[..., None]
# 唇の赤を消す
red = (src[..., 0] - src[..., 1] > 40) & (yy > 260)
lipl = np.maximum(src[..., :3].mean(2) * 1.0, 70)[red][:, None]
img[red] = lipl * np.array([1.0, 0.72, 0.22]) * mul[red][:, None]
img = np.clip(img, 0, 255)
a = np.dstack([img, m2 * 255]).astype(np.uint8)
Image.fromarray(a, 'RGBA').save(O + 'face_big.png')
crop = Image.fromarray(a, 'RGBA').crop((40, 40, 300, 360))
w = 80; h = round(crop.height * w / crop.width)
sm = np.asarray(crop.resize((w, h), Image.LANCZOS)).copy()
sm[..., 3] = np.where(sm[..., 3] > 120, 255, 0)
Image.fromarray(sm, 'RGBA').save(O + 'face.png')
v = Image.new('RGBA', (w, h), (40, 36, 52, 255)); v.alpha_composite(Image.fromarray(sm, 'RGBA'))
big = Image.new('RGBA', crop.size, (40, 36, 52, 255)); big.alpha_composite(crop)
s = Image.new('RGB', (crop.width + w * 4 + 8, max(crop.height, h * 4)), (20, 20, 20))
s.paste(big.convert('RGB'), (0, 0)); s.paste(v.convert('RGB').resize((w * 4, h * 4), Image.NEAREST), (crop.width + 8, 0))
s.save(sys.argv[1]); print(w, h)
