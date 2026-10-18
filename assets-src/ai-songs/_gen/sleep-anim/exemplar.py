"""穴を、まわりの絵の小さな切れはし（7×7 ドット）を写して埋める（ぼかさない）。ふちから内へ、形の強い所から順に埋めていく（Criminisi 法の簡単な形）。"""
import numpy as np, cv2
from scipy import ndimage as nd


def fill(img, hole, avoid=None, ps=7, win=70, seed=0):
    img = img.astype(np.float32).copy(); hole = hole.copy(); H, W, _ = img.shape
    r = ps // 2
    avoid = np.zeros_like(hole) if avoid is None else avoid
    gray = img @ np.array([0.3, 0.59, 0.11], np.float32)
    conf = (~hole).astype(np.float32)
    rng = np.random.default_rng(seed)
    while hole.any():
        front = hole & nd.binary_dilation(~hole)
        ys, xs = np.where(front)
        # 優先度: まわりが分かっている割合 × 形（明るさの変化）の強さ
        gk = np.abs(cv2.Sobel(gray, cv2.CV_32F, 1, 0)) + np.abs(cv2.Sobel(gray, cv2.CV_32F, 0, 1))
        gk[hole] = 0
        Cs = cv2.boxFilter(conf, -1, (ps, ps), normalize=True)
        Gs = cv2.boxFilter(gk, -1, (ps, ps), normalize=True)
        pr = Cs[ys, xs] * (Gs[ys, xs] + 5) + rng.uniform(0, 1e-3, len(ys))
        i = np.argmax(pr); y, x = ys[i], xs[i]
        y0, y1, x0, x1 = max(r, y - r) - r, min(H - r - 1, y + r) + r + 1, max(r, x - r) - r, min(W - r - 1, x + r) + r + 1
        cy, cx = min(max(y, r), H - r - 1), min(max(x, r), W - r - 1)
        T = img[cy - r:cy + r + 1, cx - r:cx + r + 1]; Tm = (~hole[cy - r:cy + r + 1, cx - r:cx + r + 1]).astype(np.float32)
        sy0, sy1, sx0, sx1 = max(0, cy - win), min(H, cy + win + 1), max(0, cx - win), min(W, cx + win + 1)
        S = img[sy0:sy1, sx0:sx1]
        res = cv2.matchTemplate(S, T, cv2.TM_SQDIFF, mask=np.repeat(Tm[..., None], 3, -1))
        bad = (hole | avoid)[sy0:sy1, sx0:sx1].astype(np.float32)
        badc = cv2.boxFilter(bad, -1, (ps, ps), normalize=False)[r:r + res.shape[0], r:r + res.shape[1]]
        res[badc > 0] = np.inf
        if not np.isfinite(res).any():
            win *= 2; continue
        res = res + rng.uniform(0, 1e-3, res.shape).astype(np.float32)
        my, mx = np.unravel_index(np.argmin(res), res.shape)
        Sp = S[my:my + ps, mx:mx + ps]
        fillm = hole[cy - r:cy + r + 1, cx - r:cx + r + 1]
        img[cy - r:cy + r + 1, cx - r:cx + r + 1][fillm] = Sp[fillm]
        conf[cy - r:cy + r + 1, cx - r:cx + r + 1][fillm] = Cs[y, x]
        hole[cy - r:cy + r + 1, cx - r:cx + r + 1][fillm] = False
        gray = img @ np.array([0.3, 0.59, 0.11], np.float32)
    return img
