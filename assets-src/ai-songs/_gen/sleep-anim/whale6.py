"""鯨の泳ぎ 第6版（2026-10-18「クジラのドット絵切れたりしてる。滑らかにするなら200コマぐらい」）:
  区間ごとに別々に回すと、つなぎ目でドットが切れたり欠けたりした → 体を「なめらかにつながった骨格」で曲げる（関節のまわりで、となりの区間の動きを少しずつ混ぜる＝スキニング）。
  細いひれ・尾びれが消えないよう、4×4 の中で鯨の色が 7 つ以上あれば鯨のドットにする。200コマ（30コマ/秒で約6.7秒の1かき）。
第5版（2026-10-18、人間の指示「クジラのドット絵崩れてる」「ぼやけない様に、滑らかなクジラの動きで、画面内を優雅に泳ぐように」）。
ドットをくずさない作り方（ドット絵の回転でよく使う RotSprite の考え方）:
  1) 鯨のドット絵を Scale2x（となりのドットを見て角をなめらかにする拡大）で 2 回、4 倍にする。
  2) 骨格どおりに区間ごとに回す（4 倍の細かさで、色は混ぜない）。
  3) 4×4 ごとに「いちばん多い色」を選んで、元のドットの大きさにもどす → どのコマも 1 ドット 1 色のきれいなドット絵。
  4) 5 倍（整数倍）に拡大する。ドットはすべて同じ大きさの正方形のまま。
動き: 骨格は第3〜4版と同じ（頭と胸はかたい・腰から尾へ波・尾びれはおくれて角度を変える・胸びれは肩で回る）。
  ゆったり優雅に: 1かき 6 秒（180コマ・30コマ/秒）。体全体の浮き沈みと向きの変化は大きめ、尾の動きはやわらかく。
出力: sprites/whale_000〜179.png（透明つき・5倍）・whale-layer.sunshine-pixel.json（エディタ用の別レイヤー。ドット単位）"""
import numpy as np, cv2, json, re
from PIL import Image
from scipy import ndimage as nd

UP = 4; SC = 5; SN = 200
a = np.load("base512.npy"); whale = np.load("whale512_final.npy")
ys, xs = np.where(whale); y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
PAD = 20
SW, SH = x1 - x0 + 1 + 2 * PAD, y1 - y0 + 1 + 2 * PAD
# 色の番号（0＝透明）
cols = np.unique(a[whale].reshape(-1, 3), axis=0)
PAL = np.vstack([[0, 0, 0], cols]).astype(np.uint8)
lut = {tuple(c): i + 1 for i, c in enumerate(cols.astype(int))}
ix = np.zeros((SH, SW), np.int32)
for (yy, xx) in zip(ys, xs): ix[yy - y0 + PAD, xx - x0 + PAD] = lut[tuple(a[yy, xx].astype(int))]
m = ix > 0
gy0, gx0 = np.mgrid[0:SH, 0:SW].astype(float)


def scale2x(g):
    p = np.pad(g, 1, mode="edge")
    B, D, E, F, Hh = p[:-2, 1:-1], p[1:-1, :-2], p[1:-1, 1:-1], p[1:-1, 2:], p[2:, 1:-1]
    e0 = np.where((D == B) & (B != F) & (D != Hh), D, E); e1 = np.where((B == F) & (B != D) & (F != Hh), F, E)
    e2 = np.where((D == Hh) & (D != B) & (Hh != F), D, E); e3 = np.where((Hh == F) & (D != Hh) & (B != F), F, E)
    out = np.empty((g.shape[0] * 2, g.shape[1] * 2), g.dtype)
    out[0::2, 0::2] = e0; out[0::2, 1::2] = e1; out[1::2, 0::2] = e2; out[1::2, 1::2] = e3
    return out


# ---- 体の軸と骨の区間（第4版と同じ考え方）
hy, hx = np.where(m); i = np.argmin(hx); head = np.array([hx[i], hy[i]], float)
th = {x: (np.where(m[:, x])[0].max() - np.where(m[:, x])[0].min()) for x in range(SW) if m[:, x].any()}
xr = [x for x in th if head[0] + 0.62 * (SW - 2 * PAD) < x < head[0] + 0.86 * (SW - 2 * PAD)]
pedx = min(xr, key=lambda x: th[x]); pr = np.where(m[:, pedx])[0]; ped = np.array([pedx, (pr.min() + pr.max()) / 2], float)
axis = (ped - head) / np.linalg.norm(ped - head); L = np.linalg.norm(ped - head)
s = ((gx0 - head[0]) * axis[0] + (gy0 - head[1]) * axis[1]) / L
P = lambda u: head + axis * L * u
JOINTS = [(0.22, 1.2, 3.6), (0.50, 2.6, 0.0), (0.66, 5.0, 0.6), (0.84, 7.0, 1.2), (1.00, 20.0, 2.4)]
bounds = [-9] + [j[0] for j in JOINTS] + [9]
segid = np.zeros((SH, SW), np.int32)
for k in range(len(bounds) - 1): segid[m & (s >= bounds[k]) & (s < bounds[k + 1])] = k + 1
# 胸びれ（長いほう）: 肩の関節。体の下で右下へのびる板
X = gx0 + x0 - PAD; Y = gy0 + y0 - PAD
finm = m & (X >= 236) & (Y >= 110) & (Y <= 129) & (X <= 288) & ((Y - 110) >= (X - 236) * 0.12)
segid[finm] = 9
shoulder = np.array([240.0 - x0 + PAD, 113.0 - y0 + PAD])
# 4 倍（Scale2x を 2 回）
ixU = scale2x(scale2x(ix))
segU = cv2.resize(segid.astype(np.uint8), (SW * UP, SH * UP), interpolation=cv2.INTER_NEAREST)
HU, WU = SH * UP, SW * UP
gy, gx = np.mgrid[0:HU, 0:WU].astype(np.float32)
qx, qy = (gx + 0.5) / UP - 0.5, (gy + 0.5) / UP - 0.5


def rot(c, ang):
    ca, sa = np.cos(ang), np.sin(ang)
    return np.array([[1, 0, c[0]], [0, 1, c[1]], [0, 0, 1]]) @ np.array([[ca, -sa, 0], [sa, ca, 0], [0, 0, 1]]) @ np.array([[1, 0, -c[0]], [0, 1, -c[1]], [0, 0, 1]])


def sig(x): return 1 / (1 + np.exp(-x))


finU = cv2.resize(finm.astype(np.uint8), (WU, HU), interpolation=cv2.INTER_NEAREST)
BND = [j[0] for j in JOINTS]
WID = [0.035, 0.04, 0.04, 0.04, 0.018]


def weights(px, py):
    """体の軸の上の位置から、6つの区間（頭・胸・腰・尾の前・尾柄・尾びれ）の混ぜぐあい"""
    u = ((px - head[0]) * axis[0] + (py - head[1]) * axis[1]) / L
    cs = [sig((u - b) / w) for b, w in zip(BND, WID)]       # その関節より後ろにいる度合い
    ws = [1 - cs[0]]
    for k in range(len(cs) - 1): ws.append(cs[k] - cs[k + 1])
    ws.append(cs[-1])
    # 頭（区間0）と胸（区間1）の順番: Ms[0]＝頭、Ms[1]＝胸
    return ws


def render(Ms, Mfin):
    """画面の4倍の点ごとに、元の絵のどこから来たかを、くり返しで逆算する（なめらかに曲がる骨格）"""
    tx, ty = qx.astype(np.float64), qy.astype(np.float64)
    px, py = tx.copy(), ty.copy()
    for _ in range(6):
        ws = weights(px, py)
        fx = np.zeros_like(px); fy = np.zeros_like(py)
        for w, M in zip(ws, Ms):
            fx += w * (M[0, 0] * px + M[0, 1] * py + M[0, 2]); fy += w * (M[1, 0] * px + M[1, 1] * py + M[1, 2])
        # 胸びれ（肩から先ほど大きく、肩の関節で回る）
        sxi = np.clip(((px + 0.5) * UP - 0.5).round().astype(int), 0, WU - 1); syi = np.clip(((py + 0.5) * UP - 0.5).round().astype(int), 0, HU - 1)
        onfin = finU[syi, sxi] > 0
        if onfin.any():
            d = np.hypot(px - shoulder[0], py - shoulder[1]); k = np.clip(d / 8.0, 0, 1)
            gx_ = Mfin[0, 0] * px + Mfin[0, 1] * py + Mfin[0, 2]; gy_ = Mfin[1, 0] * px + Mfin[1, 1] * py + Mfin[1, 2]
            fx = np.where(onfin, fx * (1 - k) + gx_ * k, fx); fy = np.where(onfin, fy * (1 - k) + gy_ * k, fy)
        px -= (fx - tx); py -= (fy - ty)
    sx = ((px + 0.5) * UP - 0.5).astype(np.float32); sy = ((py + 0.5) * UP - 0.5).astype(np.float32)
    return cv2.remap(ixU.astype(np.float32), sx, sy, cv2.INTER_NEAREST, borderMode=cv2.BORDER_CONSTANT, borderValue=0).astype(np.int32)


def mode_down(u):
    """4×4 の中に鯨の色が 7 つ以上あれば、いちばん多い鯨の色。少なければ透明（細いひれも消えない・ふちに空がつかない）"""
    b = u.reshape(SH, UP, SW, UP).transpose(0, 2, 1, 3).reshape(SH, SW, UP * UP)
    nz = (b > 0).sum(-1)
    best = np.zeros((SH, SW), np.int32); bc = np.full((SH, SW), -1)
    for j in range(UP * UP):
        c = np.where(b[..., j] > 0, (b == b[..., j:j + 1]).sum(-1), -1)
        upd = c > bc; best[upd] = b[..., j][upd]; bc[upd] = c[upd]
    return np.where(nz >= 7, best, 0)


com = P(0.38)
frames = []
for f in range(SN):
    ph = 2 * np.pi * f / SN
    heave = np.array([[1, 0, 0], [0, 1, -2.4 * np.sin(ph + 0.9)], [0, 0, 1]])
    M = heave @ rot(com, np.deg2rad(2.6) * np.sin(ph - 0.5))
    neck = rot(P(JOINTS[0][0]), np.deg2rad(JOINTS[0][1]) * np.sin(ph - JOINTS[0][2]))
    Ms = [M @ neck, M]
    for (u, deg, lag) in JOINTS[1:]: Ms.append(Ms[-1] @ rot(P(u), np.deg2rad(deg) * np.sin(ph - lag)))
    U = render(Ms, Ms[1] @ rot(shoulder, np.deg2rad(4.0) * np.sin(ph + 1.4)))
    d = mode_down(U)
    frames.append(d)
    rgba = np.zeros((SH, SW, 4), np.uint8); rgba[..., :3] = PAL[d]; rgba[..., 3] = (d > 0) * 255
    Image.fromarray(rgba, "RGBA").resize((SW * SC, SH * SC), Image.NEAREST).save(f"sprites/whale_{f:03d}.png")

info = json.load(open("sprites/info.json")); info["whale"] = dict(w=int(SW * SC), h=int(SH * SC)); json.dump(info, open("sprites/info.json", "w"))
# ---- エディタ用の別レイヤー（ドット単位・180コマ）
HTML = open("/home/claude/wt-mix/tools/pixel-editor/index.html", encoding="utf-8").read()
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789" + re.search(r'SYMBOL_EXTRA\s*=\s*"([^"]*)"', HTML).group(1)
used = np.unique(np.concatenate([fr.ravel() for fr in frames])); used = used[used > 0]
from scipy.spatial import cKDTree
if len(used) > 230:   # エディタの色の上限に合わせる
    _, _, C = cv2.kmeans(PAL[used].astype(np.float32), 230, None, (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.5), 1, cv2.KMEANS_PP_CENTERS)
    remap = {u: int(i) for u, i in zip(used, cKDTree(C).query(PAL[used].astype(float))[1])}; EC = C
else:
    remap = {u: i for i, u in enumerate(used)}; EC = PAL[used]
sym = np.array(["."] + list(chars[:len(EC)]))
look = np.zeros(len(PAL), np.int32)
for u, i in remap.items(): look[u] = i + 1
proj = {"format": "sunshine-pixel", "version": 2, "width": int(SW), "height": int(SH),
        "symbols": [{"sym": sym[i + 1], "label": f"鯨{i + 1}", "color": "#%02x%02x%02x" % tuple(int(round(v)) for v in EC[i])} for i in range(len(EC))],
        "layers": [{"name": "鯨（別レイヤー）", "visible": True, "opacity": 1}], "frames": [{"dur": 33} for _ in range(SN)],
        "cels": [[["".join(r) for r in sym[look[fr]]] for fr in frames]], "layer": 0, "frame": 0}
json.dump(proj, open("whale-layer.sunshine-pixel.json", "w", encoding="utf-8"), ensure_ascii=False)
print("鯨", SW * SC, SH * SC, "色", len(PAL) - 1)
