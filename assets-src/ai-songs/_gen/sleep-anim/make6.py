"""第4版の背景とクラゲ（2026-10-18、人間の指示「背景もドットが崩れて不自然な部分があるから自然な感じに。とにかく徹底して」
「水面とか、クジラがいた部分の周りぼやけてるよね。しっかり直そう」）。
直したこと:
  - ドットの細かさを元の絵のまま（512×288 ドット）にする。前は 1.25 倍に引きのばしてドットがくずれていた。動画では 4 倍（2048×1152）にして、ドットの形をそのまま見せる。
  - JPEG のにじみを軽く取ってから、色を 220 色にそろえる（ドットごとに 1 色）。
  - 鯨・水面の映りこみ・クラゲのあとを「ぼかして埋める」のをやめ、同じ高さの行のとなりの空や水から、ドットを写して埋める
    （空の明るさの段階・星の散らばり・水面の横すじが、そのままつながる）。星座の線・月・家・木は写しもとにしない。
  - 背景の動きは 300 コマ（毎秒30コマで10秒）。煙や光の粒が1コマで大きく飛ばない（なめらか）。
出力: bgframes/bg_000〜299.png（512×288）・frames.npy・palette.npy・bg.npy・whale512.npy・sprites/j*_00〜59.png・sprites/info.json"""
import numpy as np, cv2, os, json
import exemplar as ex
from PIL import Image
from scipy import ndimage as nd
from scipy.spatial import cKDTree

N = 300; SN = 60; SC = 4
W, H = 512, 288
src = Image.open("/root/.claude/uploads/945c1fd5-bcd9-525d-8abc-22b5d22e1041/0519d36b-image.jpg").convert("RGB")
r = np.asarray(src).astype(np.uint8)
r = cv2.bilateralFilter(r, 3, 18, 3)          # JPEG のにじみ・ざらつきを軽く取る（ふちは残す）
a = np.vstack([r, r[-1:], r[-1:]]).astype(float)
# 色を 220 色にそろえる
Z = a.reshape(-1, 3).astype(np.float32)
br = Z[(Z.max(1) > 150) | ((Z.max(1) - Z.min(1)) > 70)]
_, _, PAL0 = cv2.kmeans(np.vstack([Z, np.repeat(br, 3, axis=0)]), 220, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.2), 2, cv2.KMEANS_PP_CENTERS)
PAL0 = np.clip(np.round(PAL0), 0, 255)
t0 = cKDTree(PAL0)
a = PAL0[t0.query(a.reshape(-1, 3))[1]].reshape(H, W, 3)
lum = a @ [0.3, 0.59, 0.11]
YY, XX = np.mgrid[0:H, 0:W]

# ---- マスク（640 の座標で作ったものを 512 に）
def m512(p):
    m = np.load(p).astype(np.uint8)
    return cv2.resize(m, (W, H), interpolation=cv2.INTER_NEAREST).astype(bool)
whale = np.load("whale512_final.npy")   # 第5版の切り抜き（wseg3.py → wfix.py。元の絵を見て形を読み直したもの）
JK = ["jcyan", "jgold", "jblue"]
jel = {k: m512(k + ".npy") for k in JK}
np.save("base512.npy", a)

# ---- 埋める: 同じ行の、となりの空・水からドットを写す
lines = (YY < 140) & ((a[..., 0] - a[..., 2] > 12) & (lum > 60) | ((a[..., 0] > 120) & (a[..., 1] > 100) & (a[..., 2] < 150)))   # 星座の線（黄みのある線）
moon = np.hypot(XX - 156, YY - 53) < 30
house = (XX > 300) & (YY > 85)
island = (XX > 255) & (YY > 120) & (YY < 220)
moonref = (XX > 110) & (XX < 200) & (YY > 170) & (YY < 210)
avoid = {"sky": nd.binary_dilation(lines | moon | house, iterations=2), "water": nd.binary_dilation(island | moonref, iterations=2)}
refl = ((XX - 206) / 38.0) ** 2 + ((YY - 175) / 8.5) ** 2 < 1          # 水面の鯨の映りこみ
holes = {"whale": nd.binary_dilation(whale, iterations=4), "refl": refl}   # 鯨のふちの光（うす青のにじみ）もいっしょに埋める   # 鯨のふちの光（うす青のにじみ）もいっしょに埋める
for k in JK: holes[k] = nd.binary_dilation(jel[k], iterations=7)   # クラゲのまわりの光のにじみもいっしょに
bg = a.copy()
allhole = np.zeros((H, W), bool)
for v in holes.values(): allhole |= v
# まわりの明るさの流れ（穴は使わずにならす）。写したドットの明るさを、写す先の流れに合わせる
okm = (~nd.binary_dilation(allhole, iterations=5)).astype(float)
est = np.stack([nd.gaussian_filter(a[..., c] * okm, 6) for c in range(3)], -1) / np.maximum(nd.gaussian_filter(okm, 6), 1e-6)[..., None]
rng = np.random.default_rng(3)
for name, hm in holes.items():
    if name == "whale": continue   # 空は下で、星の散らばりごと作り直す
    if name in JK:   # 水の中: まわりの絵の小さな切れはしを写して埋める（ぼかさない）
        av = (allhole & ~hm) | (np.hypot(XX - 360, YY - 249) < 40) | (YY < 224) | (lum > 85)   # 時計・水面・明るい物は写しもとにしない
        bg = ex.fill(bg, hm, avoid=av, ps=7, win=70, seed=len(name)).astype(float)
        continue
    bad = allhole | (avoid["sky"] if name == "whale" else avoid["water"] if name == "refl" else np.zeros_like(allhole))
    for y in np.where(hm.any(1))[0]:
        allx = np.where(hm[y])[0]
        for xs in np.array_split(allx, max(1, int(np.ceil(len(allx) / 36)))):   # 長い行は 36 ドットずつに分けて、それぞれ写しもとを選ぶ
            if not len(xs): continue
            best = None
            for d in range(-(W - 1), W):
                sx = xs + d
                if abs(d) < 3 or sx.min() < 0 or sx.max() >= W or bad[y, sx].any(): continue
                c = np.abs(est[y, xs] - est[y, sx]).mean() + 0.01 * abs(d) + rng.uniform(0, 0.5)
                if best is None or c < best[0]: best = (c, d)
            if best is None:
                ok = np.where(~bad[y])[0]; bg[y, xs] = a[y, ok[rng.integers(0, len(ok), len(xs))]]; continue
            d = best[1]
            bg[y, xs] = np.clip(a[y, xs + d] + (est[y, xs] - est[y, xs + d]), 0, 255)
# ---- 鯨のあとの空: 明るさの流れ（大きくならした空の色）＋もとの空と同じきめ（わずかなざらつき）＋本物の星をスタンプのように散らす
hw = holes["whale"]
oks = ((YY < 138) & ~nd.binary_dilation(hw | lines | moon | house, iterations=3) & (lum < nd.median_filter(lum, 5) + 12)).astype(float)
sk = np.stack([nd.gaussian_filter(a[..., c] * oks, 18) for c in range(3)], -1) / np.maximum(nd.gaussian_filter(oks, 18), 1e-6)[..., None]
resid = (a - sk)[oks > 0]
grain = resid[np.abs(resid).sum(1) < 25]
gy_, gx_ = np.where(hw)
bg[gy_, gx_] = sk[gy_, gx_] + grain[rng.integers(0, len(grain), len(gy_))] * 0.8
# 星: 鯨のまわり以外の空の星（明るい点とそのまわり 1 ドット）を、同じくらいの数だけ写す
bright = (lum > nd.median_filter(lum, 5) + 28)
iso = nd.convolve(bright.astype(int), np.ones((3, 3), int), mode="constant") <= 2       # まわりに明るい点が少ない＝線ではなく星
sp = (YY < 138) & ~nd.binary_dilation(hw | lines | moon | house, iterations=3) & bright & iso & (a[..., 2] >= a[..., 0] - 8)
sy0, sx0 = np.where(sp)
area_sky = ((YY < 138) & ~nd.binary_dilation(hw | lines | moon | house, iterations=3)).sum()
nst = int(len(sy0) / area_sky * hw.sum())
used = np.zeros_like(hw)
for _ in range(nst * 3):
    if nst <= 0: break
    i = rng.integers(len(gy_)); y, x = gy_[i], gx_[i]
    if y < 2 or x < 2 or y > H - 3 or x > W - 3 or used[y - 2:y + 3, x - 2:x + 3].any(): continue
    j = rng.integers(len(sy0)); ys, xs = sy0[j], sx0[j]
    if ys < 1 or xs < 1 or ys > H - 2 or xs > W - 2: continue
    patch = a[ys - 1:ys + 2, xs - 1:xs + 2] - sk[ys - 1:ys + 2, xs - 1:xs + 2]
    pm = np.abs(patch).sum(-1) > 20
    tgt = bg[y - 1:y + 2, x - 1:x + 2]
    tgt[pm] = sk[y - 1:y + 2, x - 1:x + 2][pm] + patch[pm]
    used[y, x] = True; nst -= 1
# ---- 星座の線をつなぐ（2026-10-18、人間の指示「星の線もつなげるようにして」）
# 鯨のうしろで切れていた 3 本の線（上から下りてくる線・左の星座から右へのびる線・左下から右上へ上がる線）を、
# 鯨のいた所に置いた 1 つの星（結び目）で結び、そこからもう 1 本、右上の星へのばす。線の色は、それぞれの線の色をそのまま使う。
L2 = (YY < 140) & (a[..., 0] > a[..., 2] - 12) & (lum > nd.median_filter(lum, 5) + 6) & ~moon & ~house
lab, n = nd.label(L2, structure=np.ones((3, 3))); L2 = np.isin(lab, np.where(nd.sum(L2, lab, range(1, n + 1)) >= 4)[0] + 1)
def snap(p, r=7):
    ys, xs = np.where(L2 & ~hw & (np.hypot(XX - p[0], YY - p[1]) <= r))
    if not len(xs): return np.array(p, float)
    i = np.argmin(np.hypot(xs - p[0], ys - p[1])); return np.array([xs[i], ys[i]], float)
def linecol(p):
    ys, xs = np.where(L2 & (np.hypot(XX - p[0], YY - p[1]) <= 8))
    return np.median(a[ys, xs], 0) if len(xs) else np.array([150, 140, 110.0])
def draw_line(p, q, col):
    n_ = int(max(abs(q[0] - p[0]), abs(q[1] - p[1]))) + 1
    for t_ in np.linspace(0, 1, n_):
        x, y = int(round(p[0] + (q[0] - p[0]) * t_)), int(round(p[1] + (q[1] - p[1]) * t_))
        if 0 <= x < W and 0 <= y < H: bg[y, x] = col
def node(p):   # 星座の結び目の星（もとの絵の結び目を写す）
    src_p = (250, 36); pa = a[src_p[1] - 2:src_p[1] + 3, src_p[0] - 2:src_p[0] + 3] - sk[src_p[1] - 2:src_p[1] + 3, src_p[0] - 2:src_p[0] + 3]
    x, y = int(round(p[0])), int(round(p[1])); m_ = np.abs(pa).sum(-1) > 24
    bg[y - 2:y + 3, x - 2:x + 3][m_] = sk[y - 2:y + 3, x - 2:x + 3][m_] + pa[m_]
ends = {"top": snap((244, 70)), "left": snap((172, 110)), "low": snap((190, 122))}
hub = np.array([236.0, 107.0]); far = np.array([292.0, 84.0])
cols = {k: linecol(v) for k, v in ends.items()}
for k, e in ends.items(): draw_line(e, hub, cols[k])
draw_line(hub, far, cols["top"])
node(hub); node(far)
bg = PAL0[t0.query(np.clip(bg, 0, 255).reshape(-1, 3))[1]].reshape(H, W, 3)
np.save("bg.npy", bg)

# ---- 背景の動き（300コマ・10秒でひと回り）
lumb = bg @ [0.3, 0.59, 0.11]
sky = (YY < 132) & ~moon
stars = np.where(sky & (lumb > nd.median_filter(lumb, 5) + 28) & ~lines)
st_k = rng.choice([1, 2, 3], len(stars[0])); st_p = rng.uniform(0, 6.28, len(stars[0])); st_d = rng.uniform(0.15, 0.5, len(stars[0]))
warm = (bg[..., 0] > 190) & (bg[..., 1] > 140) & (bg[..., 2] < 150) & ((XX > 240) | (YY > 96))
warm = nd.binary_dilation(warm, iterations=1) & (bg[..., 0] > 120)
water = (YY > 138) & (YY < 216)
wbright = water & (lumb > nd.median_filter(lumb, 7) + 10)
clock = (np.hypot(XX - 360, YY - 249) < 27) & (YY > 219) & (bg[..., 1] > bg[..., 0] + 30)
BUB = [dict(x=rng.uniform(240, 480), ph=rng.uniform(0, 1), sw=rng.uniform(1, 2.5), k=rng.choice([1, 2]), y0=rng.uniform(262, 286)) for _ in range(20)]
MOTE = [dict(x=rng.uniform(200, 505), y=rng.uniform(120, 208), ax=rng.uniform(2, 7), ay=rng.uniform(2, 5), kx=rng.choice([1, 2]), ky=rng.choice([1, 2]),
             px=rng.uniform(0, 6.28), py=rng.uniform(0, 6.28), kb=rng.choice([1, 2, 3]), pb=rng.uniform(0, 6.28)) for _ in range(22)]
UMOTE = [dict(x=rng.uniform(225, 500), y=rng.uniform(224, 284), ax=rng.uniform(2, 5), ay=rng.uniform(2, 4), kx=rng.choice([1, 2]), ky=rng.choice([1, 2]),
              px=rng.uniform(0, 6.28), py=rng.uniform(0, 6.28), kb=rng.choice([1, 2]), pb=rng.uniform(0, 6.28)) for _ in range(26)]
SMOKE = [dict(ph=i / 7 + rng.uniform(0, 0.04), sw=rng.uniform(1.5, 4)) for i in range(7)]
CHIM = (378, 89)
EXTRA = np.array([[255, 226, 150], [200, 160, 80], [120, 240, 230], [170, 230, 240], [90, 150, 170], [150, 150, 175]], float)
PAL = np.vstack([PAL0, EXTRA])


def put(img, x, y, c, al):
    x, y = int(round(x)), int(round(y))
    if 0 <= x < W and 0 <= y < H and al > 0: img[y, x] = img[y, x] * (1 - al) + np.array(c, float) * al


tree = cKDTree(PAL)
os.makedirs("bgframes", exist_ok=True)
idx = np.empty((N, H, W), np.uint8)
for f in range(N):
    t = f / N; tp = 2 * np.pi * t
    img = bg.copy()
    sy_, sx_ = stars
    img[sy_, sx_] = np.clip(img[sy_, sx_] * (1 + st_d * np.sin(tp * st_k * 2 + st_p))[:, None], 0, 255)
    wv = 1 + 0.16 * np.sin(tp * 3 - XX * 0.09 + YY * 0.6)
    img[wbright] = np.clip(img[wbright] * wv[wbright][:, None], 0, 255)
    for y in range(178, 202):                                     # 月の映りこみが波でゆれる
        s = int(round(1.2 * np.sin(tp * 3 + y * 0.8)))
        if s: img[y, 120:190] = np.roll(img[y, 120:190], s, axis=0)
    img[warm] = np.clip(img[warm] * (0.9 + 0.07 * np.sin(tp * 5) + 0.05 * np.sin(tp * 11 + 1)), 0, 255)
    img[clock] = np.clip(img[clock] * (1 + 0.14 * np.sin(tp * 2)), 0, 255)
    # 煙は別の層（鯨より手前に重ねる。鯨は島と煙の向こうを泳ぐ）
    sm = np.zeros((H, W, 4))
    for s in SMOKE:
        ph = (t * 2 + s["ph"]) % 1.0
        y = CHIM[1] - ph * 44; x = CHIM[0] + ph * 8 + s["sw"] * np.sin(2 * np.pi * (ph * 1.5 + s["ph"]))
        al = 0.32 * np.sin(np.pi * ph) ** 0.8; rr = 1 + ph * 2.5
        for dy in range(-int(rr), int(rr) + 1):
            for dx in range(-int(rr), int(rr) + 1):
                if dx * dx + dy * dy <= rr * rr:
                    xx, yy = int(round(x + dx)), int(round(y + dy))
                    if 0 <= xx < W and 0 <= yy < H:
                        aa = al * (1 - (dx * dx + dy * dy) / (rr * rr + 1)); sm[yy, xx, 3] = 1 - (1 - sm[yy, xx, 3]) * (1 - aa); sm[yy, xx, :3] = EXTRA[5]
    os.makedirs("smoke", exist_ok=True)
    smq = (np.round(sm[..., 3] * 6) / 6)   # 不透明さは 7 段（ドット絵らしく）
    Image.fromarray(np.dstack([sm[..., :3], smq * 255]).astype(np.uint8), "RGBA").save(f"smoke/sm_{f:03d}.png")
    for q in MOTE:
        x = q["x"] + q["ax"] * np.sin(tp * q["kx"] + q["px"]); y = q["y"] + q["ay"] * np.sin(tp * q["ky"] + q["py"])
        b = 0.5 + 0.5 * np.sin(tp * q["kb"] * 2 + q["pb"])
        if b > 0.35:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)): put(img, x + dx, y + dy, EXTRA[1], 0.3 * b)
            put(img, x, y, EXTRA[0], min(1, b * 1.1))
    for q in UMOTE:
        x = q["x"] + q["ax"] * np.sin(tp * q["kx"] + q["px"]); y = q["y"] + q["ay"] * np.sin(tp * q["ky"] + q["py"])
        b = 0.5 + 0.5 * np.sin(tp * q["kb"] * 2 + q["pb"])
        if b > 0.3: put(img, x, y, EXTRA[2], 0.8 * b)
    for q in BUB:
        ph = (t * q["k"] * 2 + q["ph"]) % 1.0
        y = q["y0"] - ph * (q["y0"] - 221); x = q["x"] + q["sw"] * np.sin(2 * np.pi * (ph * 2 + q["ph"]))
        al = 0.75 * min(1, ph * 6) * min(1, (1 - ph) * 8)
        put(img, x, y, EXTRA[3], al); put(img, x + 1, y, EXTRA[4], al * 0.4)
    idx[f] = tree.query(img.reshape(-1, 3))[1].reshape(H, W)
    Image.fromarray(PAL[idx[f]].astype(np.uint8)).save(f"bgframes/bg_{f:03d}.png")
np.save("frames.npy", idx); np.save("palette.npy", PAL)
print("背景", idx.shape, len(PAL))

# ---- クラゲ（60コマで1周）。光は「明るさ＝不透明さ」で重ねる
os.makedirs("sprites", exist_ok=True)
JPH = {"jcyan": 0.0, "jgold": 2.2, "jblue": 4.1}
info = json.load(open("sprites/info.json")) if os.path.exists("sprites/info.json") else {}
for k in JK:
    m = nd.gaussian_filter(jel[k].astype(float), 0.6)
    ex = np.clip(a - bg, 0, None) * m[..., None]
    ys, xs = np.where(jel[k]); y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    P2 = 7
    JW, JH = x1 - x0 + 1 + 2 * P2, y1 - y0 + 1 + 2 * P2
    J = np.zeros((JH, JW, 3)); J[P2:P2 + y1 - y0 + 1, P2:P2 + x1 - x0 + 1] = ex[y0:y1 + 1, x0:x1 + 1]
    keep = J.max(-1) > 14; lab, n = nd.label(nd.binary_dilation(keep, iterations=1))
    if n > 1: big = np.argmax(nd.sum(keep, lab, range(1, n + 1))) + 1; J *= (lab == big)[..., None]
    # 画面の画素で曲げる（1ドットより細かく動かして、なめらかに）
    Jh = cv2.resize(J.astype(np.float32), (JW * SC, JH * SC), interpolation=cv2.INTER_NEAREST)
    gy, gx = np.mgrid[0:JH * SC, 0:JW * SC].astype(np.float32)
    hgt = (y1 - y0) * SC; cx = JW * SC / 2; top = P2 * SC
    for f in range(SN):
        tp = 2 * np.pi * f / SN + JPH[k]
        pulse = np.sin(tp)
        fr = np.clip((gy - top) / hgt, 0, 1)
        bell = fr < 0.35
        sy = top + (gy - top) / (1 + np.where(bell, 0.07, 0.03) * pulse)
        dx = 2.2 * SC * fr ** 1.3 * np.sin(tp - fr * 3.5)
        sx = cx + (gx - cx) * (1 + np.where(bell, 0.09, 0.05) * pulse * (1 - fr)) - dx
        out = cv2.remap(Jh, sx.astype(np.float32), sy.astype(np.float32), cv2.INTER_NEAREST, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        al = np.clip(out.max(-1) / 110.0, 0, 1)
        col = np.where(al[..., None] > 0, out / np.maximum(al[..., None], 1e-3), 0)
        Image.fromarray(np.dstack([np.clip(col, 0, 255), al * 255]).astype(np.uint8), "RGBA").save(f"sprites/{k}_{f:02d}.png")
    info[k] = dict(w=int(JW * SC), h=int(JH * SC), x=int((x0 - P2) * SC), y=int((y0 - P2) * SC))
json.dump(info, open("sprites/info.json", "w"))
print("クラゲ", {k: info[k] for k in JK})
