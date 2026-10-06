"""全観 イメージ版「知りたくなかった」（第3版の部品から）（2026-10-06、人間の指示「手を均等配置で、リアルにドット絵作って。観音もっとゲーム感出したドット絵に」）
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



def ash(c, k=0.65, tint=(0.86, 0.86, 0.98), dim=0.85):
    l = c[0] * .3 + c[1] * .59 + c[2] * .11
    return tuple(int(min(255, (v * (1 - k) + l * k) * t * dim)) for v, t in zip(c, tint))
GOLD_A = [ash(c) for c in GOLD]
DARK_A = [ash(c, 0.4, (0.9, 0.85, 1.0), 0.9) for c in DARK]
img = Image.new('RGBA', (W, H))
yy, xx = np.mgrid[0:H, 0:W]; d = np.hypot(xx - cx, yy - cy); ang = np.degrees(np.arctan2(yy - cy, xx - cx))
# 1) 輪: 灰色にくすんだ金。右下が欠けて、かけらが落ちていく
rows = [r for r in open(Z + 'ring_final.txt').read().split('\n') if r]; P = json.load(open(Z + 'ring_final.json'))
base = np.zeros((H, W, 4), 'uint8')
for y, r in enumerate(rows):
    for x, c in enumerate(r):
        if c != '.' and math.hypot(x - cx, y - cy) >= 84:
            base[y, x, :3] = ash(tuple(int(P[c][q:q + 2], 16) for q in (1, 3, 5)), 0.6, (0.88, 0.88, 1.0), 0.8); base[y, x, 3] = 255
gap = (ang > 48) & (ang < 66) & (d >= 84)
frag = base.copy(); base[gap] = 0
al = base[..., 3] > 0
q = np.asarray(Image.fromarray(base[..., :3]).quantize(22, method=Image.Quantize.MEDIANCUT).convert('RGB'))
base[..., :3] = np.where(al[..., None], q, 0)
img.alpha_composite(Image.fromarray(base, 'RGBA'))
# 欠けたかけら（4つ、外へ・下へずれて小さくなる）
for n, (a0, a1, r0, r1, dx, dy) in enumerate(((49, 54, 96, 112, 6, 10), (55, 59, 90, 104, 10, 22), (60, 63, 100, 114, 14, 34), (63, 65, 92, 100, 18, 44))):
    sel = (ang > a0) & (ang < a1) & (d > r0) & (d < r1)
    ys, xs = np.where(sel & (frag[..., 3] > 0))
    for y, x in zip(ys, xs):
        ny, nx = y + dy, x + dx
        if 0 <= ny < H and 0 <= nx < W: img.putpixel((nx, ny), tuple(int(v) for v in base[..., :3][al][0]) if False else tuple(int(v) for v in frag[y, x, :3]) + (255,))
# 欠けた所から走る暗いひび（3本）
for a0, ln in ((47, 26), (67, 22), (44, 18)):
    a = math.radians(a0); r = 100
    for t in range(ln):
        a += math.radians(-1.6 if a0 < 50 else 1.6) * (1 + (t % 3 == 0))
        r += math.sin(t * 0.9) * 1.2
        xi = int(round(cx + r * math.cos(a))); yi = int(round(cy + r * math.sin(a)))
        if img.getpixel((xi, yi))[3]: img.putpixel((xi, yi), (22, 16, 26, 255))
# 2) 顔のうしろ: 冷たく重いもや。光の筋は消え、光背は途切れて暗い
lay = np.zeros((H, W, 4), 'uint8')
inside = d < 84
lay[inside] = (22, 18, 34, 255)
lay[inside & ((xx + yy) % 2 == 0) & (d > 40)] = (34, 26, 50, 255)
lay[inside & ((xx // 2 + yy // 2) % 2 == 0) & (d > 66)] = (46, 34, 64, 255)
halo = (np.abs(d - 54.5) < 1.0) & (((ang + 180) % 40) < 26)      # 途切れた光背
lay[halo] = (150, 122, 74, 255)
img.alpha_composite(Image.fromarray(lay, 'RGBA'))
# 3) 手: 外側12は力なく下を向いて垂れる。内側10は顔へ手をのばす（どちらも均等・左右対称）
def place(spr, ramp, x, y, mirror=False):
    im = to_rgba(spr[:, ::-1] if mirror else spr, ramp)
    img.alpha_composite(im, (int(round(x - im.width / 2)), int(round(y - im.height / 2))))
cache = {}
for k in range(12):
    adeg = -90 + 30 * k
    if 48 < (adeg % 360) < 66: continue
    ramp = GOLD_A if k % 2 == 0 else DARK_A
    x = cx + 104 * math.cos(math.radians(adeg)); y = cy + 104 * math.sin(math.radians(adeg))
    key = ('down', ramp is GOLD_A)
    if key not in cache: cache[key] = hand_sprite(34, 180, ramp)
    place(cache[key], ramp, x, y + 4, mirror=(math.cos(math.radians(adeg)) < -1e-6))
cache = {}
for k in range(10):
    adeg = -90 + 18 + 36 * k
    ramp = DARK_A if k % 2 == 0 else GOLD_A
    x = cx + 76 * math.cos(math.radians(adeg)); y = cy + 76 * math.sin(math.radians(adeg))
    norm = (adeg + 90) % 360
    if norm <= 180:
        spr = hand_sprite(22, -(adeg + 180) - 90, ramp); cache[norm] = spr; place(spr, ramp, x, y)
    else:
        mm = 360 - norm; spr = cache.get(mm)
        if spr is None: spr = hand_sprite(22, -((mm - 90) + 180) - 90, ramp); cache[mm] = spr
        place(spr, ramp, x, y, mirror=True)
# 4) 顔
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

FACE_A = [ash(c, 0.35, (0.92, 0.92, 1.0), 0.92) for c in FACE]
face = to_rgba(fidx, FACE_A)
fx0 = cx - fw // 2; fy0 = cy - fh // 2 + 2
img.alpha_composite(face, (fx0, fy0))
def put(x, y, c):
    if 0 <= x < W and 0 <= y < H and img.getpixel((x, y))[3]: img.putpixel((x, y), c)
# 5) 黒い涙: 長く流れて、あごから落ちる
for ex in (fx0 + 25, fx0 + 57):
    for t in range(fh - 52):
        put(ex, fy0 + 56 + t, (16, 8, 14, 255)); put(ex + (1 if ex < cx else -1), fy0 + 56 + t, (70, 24, 40, 255))
    for k, dy in enumerate((6, 13, 21)):
        y = fy0 + fh + dy; x = ex + (2 if ex < cx else -2)
        img.putpixel((x, y), (16, 8, 14, 255)); img.putpixel((x, y + 1), (70, 24, 40, 255))
# 顔のひび（額から目へ）
for x, y in [(fx0 + 41 + (i % 4 == 0) - (i % 7 == 0), fy0 + 18 + i) for i in range(26)]:
    put(x, y, FACE_A[0] + (255,))
# 6) 両目を覆う手（見てしまったものを、もう見たくない）
cover = hand_sprite(46, 14, GOLD)
place(cover, GOLD, fx0 + 57 + 2, fy0 + 50, mirror=False)
place(cover, GOLD, fx0 + 25 - 2, fy0 + 50, mirror=True)
img.save(O + 'zenkan4.png')
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
open(O + 'zenkan4.txt', 'w').write('\n'.join(out) + '\n')
json.dump({m[c]: '#%02x%02x%02x' % c for c in cols}, open(O + 'zenkan4.json', 'w'))
v = Image.new('RGBA', (W, H), (40, 36, 52, 255)); v.alpha_composite(Image.fromarray(a.astype('uint8'), 'RGBA'))
v.resize((768, 768), Image.NEAREST).save(sys.argv[1] if len(sys.argv) > 1 else O + 'zenkan4_view.png')
