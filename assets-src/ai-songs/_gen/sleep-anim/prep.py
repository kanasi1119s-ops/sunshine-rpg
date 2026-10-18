"""届いた絵（512×286）を 640×360 ドットにして、鯨とクラゲの形（マスク）を取り出す。
出力: base.npy（RGB 浮動小数）、whale.npy・jelly*.npy（マスク）、mask.png（確認用）"""
import numpy as np, cv2
from PIL import Image
from scipy import ndimage as nd

im = Image.open("/root/.claude/uploads/945c1fd5-bcd9-525d-8abc-22b5d22e1041/0519d36b-image.jpg").convert("RGB")
im = im.resize((640, 358), Image.LANCZOS)
a = np.asarray(im).astype(float)
a = np.vstack([a, a[-1:], a[-1:]])   # 360 行に
H, W, _ = a.shape
np.save("base.npy", a)
lum = a @ [0.3, 0.59, 0.11]


def comp(mask, seed=None):
    lab, n = nd.label(mask)
    if n == 0: return mask
    if seed is not None:
        k = lab[seed[1], seed[0]]
        if k == 0:
            sizes = nd.sum(mask, lab, range(1, n + 1)); k = int(np.argmax(sizes)) + 1
    else:
        sizes = nd.sum(mask, lab, range(1, n + 1)); k = int(np.argmax(sizes)) + 1
    return lab == k


# ---- 鯨: 空より少し明るい青灰色のかたまり（星の点はならして消す）
x0, y0, x1, y1 = 205, 40, 470, 170
# 鯨の輪郭のおおよその形（拡大した絵で読んだ点。512 の絵の座標→640）
Z = [(65,305),(150,250),(300,200),(450,130),(560,95),(650,80),(700,72),(735,45),(780,35),(770,70),(830,112),(790,124),(730,104),(690,112),
     (600,145),(520,205),(470,275),(440,320),(505,385),(380,350),(330,355),(335,395),(290,390),(250,355),(150,348),(75,330)]
poly = np.array([((160 + zx / 4) * 1.25, (30 + zy / 4) * 1.25) for zx, zy in Z], np.int32)
pm = np.zeros((H, W), np.uint8); cv2.fillPoly(pm, [poly], 1)
pm = nd.binary_dilation(pm.astype(bool), iterations=3)
sub = a[y0:y1, x0:x1]
L = cv2.medianBlur(np.clip(lum[y0:y1, x0:x1], 0, 255).astype(np.uint8), 5).astype(float)
b = sub[..., 2] - sub[..., 0]
sky = np.median(L[:8, :40])
m = (L > sky + 6) & pm[y0:y1, x0:x1]
m = nd.binary_closing(m, iterations=4)
m = comp(m)
m = nd.binary_fill_holes(m | (nd.binary_erosion(pm[y0:y1, x0:x1], iterations=4)))
m = nd.binary_opening(m, iterations=1)
m = comp(m)
m = nd.binary_dilation(m, iterations=1)
whale = np.zeros((H, W), bool); whale[y0:y1, x0:x1] = m
np.save("whale.npy", whale)

# ---- クラゲ: 水の中の、まわりより明るく色の強い所（光っている体と足）
hsv = cv2.cvtColor(np.clip(a, 0, 255).astype(np.uint8), cv2.COLOR_RGB2HSV).astype(float)
J = {"jcyan": (338, 277, 380, 333), "jgold": (372, 310, 399, 348), "jblue": (531, 283, 560, 331)}
jm = {}
for k, (jx0, jy0, jx1, jy1) in J.items():
    if jx0 >= W: continue
    s = lum[jy0:jy1, jx0:jx1]
    bg = np.percentile(s, 35)
    m = (s > bg + 22) | ((hsv[jy0:jy1, jx0:jx1, 1] > 90) & (s > bg + 12))
    m = nd.binary_closing(m, iterations=2)
    m = comp(m)
    m = nd.binary_fill_holes(m)
    m = nd.binary_dilation(m, iterations=1)
    full = np.zeros((H, W), bool); full[jy0:jy1, jx0:jx1] = m
    jm[k] = full; np.save(k + ".npy", full)
    print(k, m.sum())
print("whale", whale.sum())
vis = a.copy()
vis[whale] = vis[whale] * 0.4 + np.array([255, 0, 0]) * 0.6
for k, c in zip(jm, ([0, 255, 0], [255, 0, 255], [255, 255, 0])):
    vis[jm[k]] = vis[jm[k]] * 0.4 + np.array(c) * 0.6
Image.fromarray(np.clip(vis, 0, 255).astype(np.uint8)).resize((1280, 720), Image.NEAREST).save("mask.png")
