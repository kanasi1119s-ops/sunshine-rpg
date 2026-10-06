"""立体の模型からドット絵を描く、小さな道具（2026-10-06。church3d.py の作り方を、ほかの飾りにも使えるようにしたもの）。

  形は「きょり関数（SDF）」で組む（箱・円柱・球・まるい柱・円すい・輪など）。けずる形（くぼみ・穴）も使える。
  町の家と同じ見え方（正面はそのまま、奥へ1すすむと右へ1・上へ0.45）で、1ドットずつ光線を飛ばして形に当て、
  光（左上前から）・ほかの形が落とす影・すみの暗さ（AO）で明るさを決め、材質ごとの色の段へ。段のちょうどあいだだけ市松でまぜる。
  最後に外のりんかくと、地面のうすい影（透ける色の楕円）をつける。
使い方は props3d.py を見る。"""
import json
import math

import numpy as np

K = 0.45


def length(v):
    return np.sqrt((v * v).sum(-1))


# ---------------------------------------------------------------- 形
def box(c, h):
    c = np.array(c, float); h = np.array(h, float)

    def f(p):
        q = np.abs(p - c) - h
        return length(np.maximum(q, 0)) + np.minimum(q.max(-1), 0)
    return f


def rbox(c, h, r):
    """かどの丸い箱。"""
    b = box(c, np.array(h, float) - r)
    return lambda p: b(p) - r


def cyl_y(cx, cz, r, y0, y1):
    def f(p):
        d_r = np.sqrt((p[..., 0] - cx) ** 2 + (p[..., 2] - cz) ** 2) - r
        d_y = np.maximum(y0 - p[..., 1], p[..., 1] - y1)
        return np.minimum(np.maximum(d_r, d_y), 0) + np.sqrt(np.maximum(d_r, 0) ** 2 + np.maximum(d_y, 0) ** 2)
    return f


def cyl_x(cy, cz, r, x0, x1):
    def f(p):
        d_r = np.sqrt((p[..., 1] - cy) ** 2 + (p[..., 2] - cz) ** 2) - r
        d_x = np.maximum(x0 - p[..., 0], p[..., 0] - x1)
        return np.minimum(np.maximum(d_r, d_x), 0) + np.sqrt(np.maximum(d_r, 0) ** 2 + np.maximum(d_x, 0) ** 2)
    return f


def cone_y(cx, cz, r0, r1, y0, y1):
    """下の半径 r0、上の半径 r1 の、たての円すい台（近い値の SDF）。"""
    def f(p):
        t = np.clip((p[..., 1] - y0) / (y1 - y0), 0, 1)
        rr = r0 + (r1 - r0) * t
        d_r = (np.sqrt((p[..., 0] - cx) ** 2 + (p[..., 2] - cz) ** 2) - rr) * 0.85
        d_y = np.maximum(y0 - p[..., 1], p[..., 1] - y1)
        return np.maximum(d_r, d_y)
    return f


def sphere(c, r):
    c = np.array(c, float)
    return lambda p: length(p - c) - r


def ellipsoid(c, r):
    c = np.array(c, float); r = np.array(r, float)

    def f(p):
        q = (p - c) / r
        k0 = length(q); k1 = length(q / r)
        return k0 * (k0 - 1) / np.maximum(k1, 1e-6)
    return f


def capsule(a, b, r, r2=None):
    """a から b への、まるい柱（r2 があれば、b の側の太さ）。"""
    a = np.array(a, float); b = np.array(b, float)
    ba = b - a; bb = (ba * ba).sum()

    def f(p):
        pa = p - a
        h = np.clip((pa * ba).sum(-1) / bb, 0, 1)
        rr = r if r2 is None else r + (r2 - r) * h
        return length(pa - ba * h[..., None]) - rr
    return f


def torus_y(c, R, r):
    c = np.array(c, float)

    def f(p):
        q = p - c
        a = np.sqrt(q[..., 0] ** 2 + q[..., 2] ** 2) - R
        return np.sqrt(a ** 2 + q[..., 1] ** 2) - r
    return f


def gable_x(x0, x1, z0, z1, y_eave, y_ridge):
    """横（x）へのびる切妻屋根（棟は x の向き。前後 z に流れる）。"""
    cz = (z0 + z1) / 2; hw = (z1 - z0) / 2; hgt = y_ridge - y_eave; n = math.hypot(hgt, hw)

    def f(p):
        z = np.abs(p[..., 2] - cz); y = p[..., 1] - y_eave
        d = np.maximum((z * hgt + y * hw - hw * hgt) / n, -y)
        return np.maximum(d, np.maximum(x0 - p[..., 0], p[..., 0] - x1))
    return f


def shell(f, t):
    """形のからだけ（厚み t）。"""
    return lambda p: np.abs(f(p)) - t


def inter(a, b):
    return lambda p: np.maximum(a(p), b(p))


def diff(a, b):
    return lambda p: np.maximum(a(p), -b(p))


# ---------------------------------------------------------------- 絵にする
BAYER = np.array([[0.125, 0.625], [0.875, 0.375]])


class Model:
    def __init__(self):
        self.solids = []
        self.cuts = []

    def add(self, f, m="stone"):
        self.solids.append((f, m))

    def cut(self, f, m=None):
        self.cuts.append((f, m))

    def sdf(self, p):
        d = np.full(p.shape[:-1], 1e9)
        for f, _ in self.solids:
            d = np.minimum(d, f(p))
        for f, _ in self.cuts:
            d = np.maximum(d, -f(p))
        return d

    def material(self, p):
        best = np.full(len(p), 1e9); mat = np.array(["?"] * len(p), dtype=object)
        for f, m in self.solids:
            d = np.abs(f(p)); sel = d < best
            best[sel] = d[sel]; mat[sel] = m
        for f, m in self.cuts:
            if m is None:
                continue
            d = np.abs(f(p)); sel = (d < 0.1) & (d <= best + 0.05)
            mat[sel] = m
        return mat


def render(model, W, H, CX, GROUND, ramps, shade_fn=None, colour_fn=None, light=(-0.55, 0.62, 0.56),
           outline="#1e1a18", shadow=None, ambient=0.22):
    sx, sy = np.meshgrid(np.arange(W) + 0.5, np.arange(H) + 0.5)
    Z0 = 30.0
    start = np.stack([sx - CX + Z0, GROUND - sy + K * Z0, np.full_like(sx, Z0)], -1)
    rd = np.array([-1.0, -K, -1.0]); rd /= np.linalg.norm(rd)
    dist = np.zeros(sx.shape); hit = np.zeros(sx.shape, bool); alive = np.ones(sx.shape, bool)
    for _ in range(300):
        idx = np.nonzero(alive)
        p = start[idx] + rd * dist[idx][:, None]
        d = model.sdf(p)
        dist[idx] += np.maximum(d * 0.9, 0.01)
        h = d < 0.01
        hit[idx[0][h], idx[1][h]] = True
        gone = h | (dist[idx] > 150) | (p[:, 1] < -0.3)
        alive[idx[0][gone], idx[1][gone]] = False
        if not alive.any():
            break
    P = start + rd * dist[..., None]
    HP = P[hit]
    e = 0.04
    def g(o):
        return model.sdf(HP + np.array(o)) - model.sdf(HP - np.array(o))
    N = np.stack([g([e, 0, 0]), g([0, e, 0]), g([0, 0, e])], -1)
    N /= np.maximum(length(N)[..., None], 1e-6)
    L = np.array(light, float); L /= np.linalg.norm(L)
    dif = np.clip((N * L).sum(-1), 0, 1)
    sh = np.ones(len(HP)); t = np.full(len(HP), 0.2); q = HP + N * 0.08
    for _ in range(70):
        d = model.sdf(q + L * t[:, None])
        sh = np.minimum(sh, np.clip(10 * d / t, 0, 1))
        t += np.clip(d, 0.05, 1.5)
    ao = np.ones(len(HP))
    for k, s in enumerate((0.3, 0.7, 1.3, 2.2)):
        d = model.sdf(HP + N * s)
        ao -= (s - np.minimum(d, s)) / s * (0.5 ** k) * 0.5
    ao = np.clip(ao, 0.3, 1)
    MAT = model.material(HP)
    img = np.full((H, W), "", dtype=object)
    ys, xs = np.nonzero(hit)
    for i in range(len(HP)):
        x, y = xs[i], ys[i]
        m = MAT[i]
        lum = ambient + (1 - ambient) * dif[i] * (0.3 + 0.7 * sh[i])
        lum *= 0.55 + 0.45 * ao[i]
        if shade_fn:
            lum, m = shade_fn(m, HP[i], N[i], lum, x, y)
        ramp = ramps[m]
        v = np.clip(lum, 0, 0.999) * (len(ramp) - 1)
        lo = int(v); fr = v - lo
        k = lo + (1 if (fr > 0.62 or (0.38 <= fr <= 0.62 and BAYER[y % 2, x % 2] < 0.5)) else 0)
        c = ramp[min(len(ramp) - 1, k)]
        if colour_fn:
            c = colour_fn(m, HP[i], N[i], lum, x, y, c)
        img[y, x] = c
    if outline:
        add = []
        for y in range(H):
            for x in range(W):
                if img[y, x] == "" and any(0 <= x + a < W and 0 <= y + b < H and img[y + b, x + a] != "" for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    add.append((x, y))
        for x, y in add:
            img[y, x] = outline
    if shadow:
        cx, cy, rx, ry = shadow
        for y in range(int(cy - ry - 1), int(cy + ry + 2)):
            for x in range(int(cx - rx - 1), int(cx + rx + 2)):
                if not (0 <= x < W and 0 <= y < H) or img[y, x] != "":
                    continue
                dd = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2
                if dd < 0.45:
                    img[y, x] = "#10201860"
                elif dd < 0.8 or (dd <= 1 and (x + y) % 2 == 0):
                    img[y, x] = "#10201830"
    return img


def save(img, path_txt, path_pal):
    H, W = img.shape
    cols = sorted(set(img[img != ""].tolist()))
    syms = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,-/:;<=>?@[]^_{|}~"
    assert len(cols) <= len(syms), len(cols)
    cmap = {c: syms[i] for i, c in enumerate(cols)}
    rows = ["".join(cmap[img[y, x]] if img[y, x] != "" else "." for x in range(W)) for y in range(H)]
    open(path_txt, "w").write("\n".join(rows) + "\n")
    json.dump({cmap[c]: c for c in cols}, open(path_pal, "w"))
    return len(cols)
