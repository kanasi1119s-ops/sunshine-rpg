"""全観 第3版（2026-10-06、人間の指示「手を均等配置で、リアルにドット絵作って。観音もっとゲーム感出したドット絵に」）
- 手: AIの下絵の手（hand_gold.png）を、置く向きごとに大きいまま回してから縮め、決めた7色の段階（金・黒金）に塗り分けて、
  1マスの暗い縁をつける（ぼかしの縮小ではなく、ドット絵の色の段で描く）。外側12・内側12を30度ずつ、半径・大きさをそろえて置く。
  右半分を作り、左半分は左右反転（左右対称）。金と黒金は1つおき。
- 顔: face_big.png（face2.py の重い顔・丸い頭）を、9色の青銅の段階に塗り分け、孤立した点を消し、外周に暗い縁。
- 輪は前の全観の輪（目なし）を28色にまとめて使う。全体で62色以内。"""
import json, math, sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

Z = '/tmp/monster-work/zk/'; O = '/tmp/monster-work/zk2/'
W = H = 256; cx = cy = 128

GOLD = [(40, 18, 12), (92, 48, 20), (146, 86, 30), (196, 134, 44), (228, 180, 70), (248, 220, 124), (255, 246, 196)]
DARK = [(12, 6, 8), (36, 14, 18), (62, 24, 28), (94, 38, 36), (130, 62, 46), (172, 100, 62), (214, 148, 82)]
FACE = [(24, 10, 14), (50, 22, 22), (80, 40, 28), (114, 64, 34), (152, 96, 44), (188, 132, 56), (218, 168, 76), (238, 202, 112), (250, 234, 168)]


def ramp_map(rgb, alpha, ramp, lo=3, hi=97):
    """明るさの順に、ramp[1:] の段に分ける（ramp[0] は縁の色）"""
    lum = rgb[..., 0] * .3 + rgb[..., 1] * .59 + rgb[..., 2] * .11
    v = lum[alpha]
    a, b = np.percentile(v, lo), np.percentile(v, hi)
    n = len(ramp) - 1
    idx = np.clip(((lum - a) / max(b - a, 1) * n).astype(int), 0, n - 1) + 1
    return np.where(alpha, idx, -1)


def clean(idx, passes=2):
    """まわり4マスと全部ちがう孤立点を、まわりで一番多い段にする"""
    for _ in range(passes):
        p = np.pad(idx, 1, constant_values=-1)
        nb = np.stack([p[:-2, 1:-1], p[2:, 1:-1], p[1:-1, :-2], p[1:-1, 2:]])
        lone = (idx >= 0) & np.all(nb != idx, axis=0)
        for y, x in zip(*np.where(lone)):
            vals = [v for v in nb[:, y, x] if v >= 0]
            if vals:
                idx[y, x] = max(set(vals), key=vals.count)
    return idx


def outline(idx):
    """外側に1マスの縁（段0）"""
    a = idx >= 0
    ring = ndimage.binary_dilation(a) & ~a
    idx = idx.copy(); idx[ring] = 0
    return idx


def to_rgba(idx, ramp):
    out = np.zeros(idx.shape + (4,), 'uint8')
    for k, c in enumerate(ramp):
        out[idx == k] = c + (255,)
    return Image.fromarray(out, 'RGBA')


# --- 手 ---
HAND = Image.open(O + 'hand_gold.png').convert('RGBA')


def hand_sprite(size, deg, ramp):
    big = HAND.resize((HAND.width * 3, HAND.height * 3), Image.LANCZOS)
    big = big.rotate(deg, resample=Image.BICUBIC, expand=True)
    s = size / (HAND.height * 3)
    sm = big.resize((max(1, round(big.width * s)), max(1, round(big.height * s))), Image.BOX)
    a = np.asarray(sm).astype(float)
    alpha = a[..., 3] > 140
    alpha = ndimage.binary_opening(alpha, structure=np.ones((2, 1))) | ndimage.binary_opening(alpha, structure=np.ones((1, 2)))
    idx = clean(ramp_map(a[..., :3], alpha, ramp))
    idx = np.pad(idx, 1, constant_values=-1)
    return outline(idx)


img = Image.new('RGBA', (W, H))
# 1) 輪（28色にまとめる）
rows = [r for r in open(Z + 'ring_final.txt').read().split('\n') if r]; P = json.load(open(Z + 'ring_final.json'))
base = np.zeros((H, W, 4), 'uint8')
for y, r in enumerate(rows):
    for x, c in enumerate(r):
        if c != '.' and math.hypot(x - cx, y - cy) >= 84:
            base[y, x, :3] = [int(P[c][q:q + 2], 16) for q in (1, 3, 5)]; base[y, x, 3] = 255
al = base[..., 3] > 0
q = np.asarray(Image.fromarray(base[..., :3]).quantize(28, method=Image.Quantize.MEDIANCUT).convert('RGB'))
base[..., :3] = np.where(al[..., None], q, 0)
img.alpha_composite(Image.fromarray(base, 'RGBA'))
# 2) 顔のうしろ: 黒紫のもや（規則正しい市松の点、中ほど濃く）と光背・光の筋（均等）
lay = np.zeros((H, W, 4), 'uint8')
yy, xx = np.mgrid[0:H, 0:W]; d = np.hypot(xx - cx, yy - cy)
mist = (d < 84) & ((xx + yy) % 2 == 0)
lay[mist & (d < 60)] = (46, 16, 50, 255)
lay[mist & (d >= 60)] = (32, 12, 38, 255)
lay[(d < 84) & ((xx + yy) % 2 == 1) & (d < 50)] = (32, 12, 38, 255)
for k in range(24):
    a = k * math.pi / 12 + math.pi / 24
    for r in range(58, 84):
        x = int(round(cx + r * math.cos(a))); y = int(round(cy + r * math.sin(a)))
        lay[y, x] = (255, 232, 150, 255) if r < 70 else (200, 150, 64, 255)
ring_halo = (np.abs(d - 54.5) < 1.0); lay[ring_halo] = (240, 200, 90, 255)
lay[np.abs(d - 57.2) < 0.6] = (120, 70, 20, 255)
img.alpha_composite(Image.fromarray(lay, 'RGBA'))
# 輪の赤いひび（左右対称に4本ずつ、均等）
for k in range(4):
    for side in (1, -1):
        a0 = math.radians(-90 + side * (15 + 45 * k) + (0 if side > 0 else 0))
        for t in range(14):
            r = 92 + t * 1.6; a = a0 + side * 0.02 * math.sin(t)
            xi = int(round(cx + r * math.cos(a))); yi = int(round(cy + r * math.sin(a)))
            if img.getpixel((xi, yi))[3]:
                img.putpixel((xi, yi), (60, 6, 10, 255))
                if 0 < xi + side < W and img.getpixel((xi + side, yi))[3]: img.putpixel((xi + side, yi), (200, 40, 30, 255))
# 3) 手（均等・左右対称）
def place(spr, ramp, x, y, mirror=False):
    im = to_rgba(spr[:, ::-1] if mirror else spr, ramp)
    img.alpha_composite(im, (int(round(x - im.width / 2)), int(round(y - im.height / 2))))

for ring_r, size, start, gold_even in ((104, 34, 0, True), (72, 24, 15, False)):
    cache = {}
    for k in range(12):
        adeg = -90 + start + 30 * k                      # 置く向き（上が -90）
        ramp = GOLD if ((k % 2 == 0) == gold_even) else DARK
        x = cx + ring_r * math.cos(math.radians(adeg)); y = cy + ring_r * math.sin(math.radians(adeg))
        norm = ((adeg + 90) % 360)                       # 0=上, 180=下
        if norm <= 180:
            spr = hand_sprite(size, -adeg - 90, ramp); cache[norm] = spr
            place(spr, ramp, x, y)
        else:
            m = 360 - norm                               # 左右反転のもと
            spr = cache.get(m)
            if spr is None:
                spr = hand_sprite(size, -(m - 90) - 90, ramp); cache[m] = spr
            place(spr, ramp, x, y, mirror=True)
# 4) 顔（ゲームらしいドット絵に）
from skimage import exposure
fb = Image.open(O + 'face_big.png').convert('RGBA').crop((40, 40, 300, 360))
frgb = np.asarray(fb.convert('RGB')).astype(float) / 255
flum = frgb.mean(2)
eq = exposure.equalize_adapthist(flum, clip_limit=0.02, kernel_size=48)   # 目・鼻・口の彫りをはっきり
frgb = np.clip(frgb * (eq / np.maximum(flum, 1e-3))[..., None] * 0.6 + frgb * 0.4, 0, 1)
fim = Image.fromarray((frgb * 255).astype('uint8')).filter(ImageFilter.MedianFilter(3)).filter(ImageFilter.UnsharpMask(3, 120, 2))
fw = 82; fh = round(fb.height * fw / fb.width)
sm_rgb = np.asarray(fim.resize((fw, fh), Image.BOX)).astype(float)
sm_a = ndimage.binary_opening(np.asarray(fb.split()[3].resize((fw, fh), Image.BOX)) > 128)
fidx = ramp_map(sm_rgb, sm_a, FACE, 2, 99)
L = sm_rgb.mean(2); ink = sm_a & (L < ndimage.uniform_filter(L, 3) - 16)   # 彫りの線（2段暗く）
fidx[ink] = np.maximum(fidx[ink] - 2, 1)
fidx = clean(fidx, 3)
fidx[sm_a & ~ndimage.binary_erosion(sm_a)] = 0          # 外周の暗い縁
face = to_rgba(fidx, FACE)
fx0 = cx - fw // 2; fy0 = cy - fh // 2 + 2
img.alpha_composite(face, (fx0, fy0))
# 5) 禍々しさ: 顔のひび（はっきりした1マスの線）と黒い涙（左右対称）
def put(x, y, c):
    if 0 <= x < W and 0 <= y < H and img.getpixel((x, y))[3]: img.putpixel((x, y), c)
for x, y in [(fx0 + 50 + i // 3, fy0 + 10 + i) for i in range(12)] + [(fx0 + 54 - (i // 4), fy0 + 22 + i) for i in range(10)]:
    put(x, y, FACE[0] + (255,))
for ex in (fx0 + 25, fx0 + 57):
    for t in range(16):
        put(ex, fy0 + 55 + t, (20, 6, 12, 255)); put(ex + 1, fy0 + 55 + t, (96, 20, 30, 255) if t > 2 else (20, 6, 12, 255))
img.save(O + 'zenkan3.png')
# 6) 文字グリッドに（色はそのまま。62色を超えたらまとめる）
a = np.asarray(img); al = a[..., 3] > 0
cols = sorted({tuple(c) for c in a[..., :3][al].tolist()})
print('色数', len(cols))
if len(cols) > 62:
    q = Image.fromarray(a[..., :3]).quantize(62, method=Image.Quantize.MEDIANCUT).convert('RGB')
    a = np.dstack([np.asarray(q), a[..., 3]]); cols = sorted({tuple(c) for c in a[..., :3][al].tolist()})
syms = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
m = {c: syms[n] for n, c in enumerate(cols)}
out = [''.join(m[tuple(a[y, x, :3])] if al[y, x] else '.' for x in range(W)) for y in range(H)]
open(O + 'zenkan3.txt', 'w').write('\n'.join(out) + '\n')
json.dump({m[c]: '#%02x%02x%02x' % c for c in cols}, open(O + 'zenkan3.json', 'w'))
v = Image.new('RGBA', (W, H), (40, 36, 52, 255)); v.alpha_composite(Image.fromarray(a.astype('uint8'), 'RGBA'))
v.resize((768, 768), Image.NEAREST).save(sys.argv[1] if len(sys.argv) > 1 else O + 'zenkan3_view.png')
