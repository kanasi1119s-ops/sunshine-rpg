"""霧断崖の「環の聖堂」の外観を、立体の模型から描く（2026-10-06、人間の指示「教会の建物勉強してきて」
「リアルだけど、立体感もさらに作って。細かく細かくドットを使って」）。
勉強ノート docs/design/church-architecture-notes.md のしくみ（高い身廊と低い側廊の2段の屋根・高窓・控え壁と飛び梁・
三つの入口と奥へ下がるアーチ・像の帯・バラ窓・塔）を、実在の建物を写さずに組み立てた。十字は使わず、三つの環のしるし。

作り方:
  1. 建物を、箱・円柱・砲弾形の塔・三角の屋根・アーチのくぼみなどの「形のきょり関数（SDF）」の組み合わせで作る。
     窓・入口・像の帯のくぼみは、形をけずって作るので、ほんとうに奥行きがある。
  2. 町の家と同じ見え方（正面はそのまま、奥へ行くほど右上へ 1 : 0.45）で、1ドットずつ光線を飛ばして形に当てる。
  3. 光は左上前から。面の向きの明るさ・ほかの形が落とす影（光の方へもう一度光線を飛ばす）・すみの暗さ（AO）を合わせる。
  4. 石の段・目地・下の方のよごれ・雨だれを、場所の値から足し、明るさを色の段へ。段のあいだは2×2の市松でまぜる。
  5. 外のりんかくをつけ、三つの環のしるし（バラ窓・塔の先）を上から描く。
絵は 112×96（足もとのまんなか x=56）。書き出しは church.txt / pal-church.json（church.py の中の絵 church-interior はそのまま）。"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 176, 176
CX, GROUND = 88, 173          # 正面 (z=0) の地面 (y=0) が、絵の y=173
S = 1.6                       # 模型を1.6倍に（2026-10-06「でかく、でかく」「もっと大きい教会でもいいよ」）
K = 0.45                      # 奥へ1すすむと、右へ1・上へ0.45

# ===================================================================== 形（SDF）
def length(v):
    return np.sqrt((v * v).sum(-1))


def sd_box(p, c, h):
    q = np.abs(p - np.array(c)) - np.array(h)
    return length(np.maximum(q, 0)) + np.minimum(q.max(-1), 0)


def sd_cyl_y(p, cx, cz, r, y0, y1):
    d_r = np.sqrt((p[..., 0] - cx) ** 2 + (p[..., 2] - cz) ** 2) - r
    d_y = np.maximum(y0 - p[..., 1], p[..., 1] - y1)
    return np.minimum(np.maximum(d_r, d_y), 0) + np.sqrt(np.maximum(d_r, 0) ** 2 + np.maximum(d_y, 0) ** 2)


def sd_spire(p, cx, cz, r, y0, h):
    """砲弾形の塔の先（下が太く、上へなめらかにすぼむ）。y0 から高さ h。"""
    y = p[..., 1] - y0
    t = np.clip(y / h, 0, 1)
    rad = r * np.maximum(1 - t, 0) ** 0.85 + 0.01     # 2026-10-06「塔の先を鋭く」: 上へまっすぐ細くなる、とがった円すい
    d_r = np.sqrt((p[..., 0] - cx) ** 2 + (p[..., 2] - cz) ** 2) - rad
    d = np.maximum(d_r * 0.7, np.maximum(-y, y - h))
    return d


def sd_sphere(p, c, r):
    return length(p - np.array(c)) - r


def sd_capsule(p, a, b, r):
    a = np.array(a, float); b = np.array(b, float)
    pa = p - a; ba = b - a
    h = np.clip((pa * ba).sum(-1) / (ba * ba).sum(), 0, 1)
    return length(pa - ba * h[..., None]) - r


def sd_gable_z(p, x0, x1, y_eave, y_ridge, z0, z1):
    """奥（z）へのびる三角の屋根（切妻）。"""
    cx = (x0 + x1) / 2; hw = (x1 - x0) / 2; hgt = y_ridge - y_eave
    x = np.abs(p[..., 0] - cx); y = p[..., 1] - y_eave
    n = math.hypot(hgt, hw)
    d_slope = (x * hgt + y * hw - hw * hgt) / n
    d = np.maximum(d_slope, -y)
    d = np.maximum(d, np.maximum(z0 - p[..., 2], p[..., 2] - z1))
    return d


def sd_gable_x(p, z0, z1, y_eave, y_ridge, x0, x1):
    """横（x）へのびる三角（正面の破風）。"""
    cz = (z0 + z1) / 2; hw = (z1 - z0) / 2; hgt = y_ridge - y_eave
    z = np.abs(p[..., 2] - cz); y = p[..., 1] - y_eave
    n = math.hypot(hgt, hw)
    d = np.maximum((z * hgt + y * hw - hw * hgt) / n, -y)
    return np.maximum(d, np.maximum(x0 - p[..., 0], p[..., 0] - x1))


def sd_tri_front(p, cx, hw, y0, y1, z0, z1):
    """正面に立つ三角の飾り破風（とがった三角の板）。"""
    x = np.abs(p[..., 0] - cx); y = p[..., 1] - y0; hgt = y1 - y0
    n = math.hypot(hgt, hw)
    d = np.maximum((x * hgt + y * hw - hw * hgt) / n, -y)
    return np.maximum(d, np.maximum(z0 - p[..., 2], p[..., 2] - z1))


def sd_leanto(p, x_in, x_out, y_in, y_out, z0, z1):
    """側廊の片流れ屋根（内がわ x_in で高さ y_in、外がわ x_out で y_out）。"""
    lo, hi = min(x_in, x_out), max(x_in, x_out)
    t = (p[..., 0] - x_in) / (x_out - x_in)
    ytop = y_in + (y_out - y_in) * t
    d = p[..., 1] - ytop
    d = np.maximum(d, -(p[..., 1] - (y_out - 3)))
    d = np.maximum(d, np.maximum(lo - p[..., 0], p[..., 0] - hi))
    return np.maximum(d, np.maximum(z0 - p[..., 2], p[..., 2] - z1)) * 0.8


def sd_arch_z(p, cx, w, y0, ys, zf, depth, pointed=True):
    """正面（z=zf の面）に、奥行き depth でけずる、上がとがったアーチの形。y0〜ys は縦の部分、その上がとがり。"""
    x = p[..., 0] - cx; y = p[..., 1]
    hw = w / 2
    d_rect = np.maximum(np.abs(x) - hw, np.maximum(y0 - y, y - ys))
    if pointed:
        R = w * 0.85
        c1 = np.sqrt((x - (hw - R)) ** 2 + (y - ys) ** 2) - R
        c2 = np.sqrt((x + (hw - R)) ** 2 + (y - ys) ** 2) - R
        d_top = np.maximum(np.maximum(c1, c2), ys - y)
    else:
        d_top = np.maximum(np.sqrt(x ** 2 + (y - ys) ** 2) - hw, ys - y)
    d2 = np.minimum(d_rect, d_top)
    return np.maximum(d2, np.maximum(p[..., 2] - (zf + 3), (zf - depth) - p[..., 2]))


def sd_arch_x(p, cz, w, y0, ys, xf, depth):
    """右向きの壁（x=xf の面）をけずる、とがったアーチの窓。"""
    q = p.copy()
    q[..., 0], q[..., 2] = p[..., 2], -p[..., 0]
    return sd_arch_z(q, cz, w, y0, ys, -xf, depth)


def sd_disc_z(p, cx, cy, r, zf, depth):
    d = np.sqrt((p[..., 0] - cx) ** 2 + (p[..., 1] - cy) ** 2) - r
    return np.maximum(d, np.maximum(p[..., 2] - (zf + 3), (zf - depth) - p[..., 2]))


# ===================================================================== 建物の組み立て
SOLIDS = []    # (関数, 材質)
CUTS = []      # (関数, 材質): けずる形。けずった面の奥（正面向き）は、この材質になる

def solid(f, m="stone"):
    SOLIDS.append((f, m))


def cut(f, m="dark"):
    CUTS.append((f, m))


FW = 26          # 正面の半分の幅
DEP = 24         # 奥行き
NAVE = 11        # 身廊の半分の幅
AISLE_H = 24     # 側廊の壁の高さ
NAVE_H = 42      # 身廊の壁の高さ（高窓のある所まで）
RIDGE = 56

# 身廊・側廊・屋根
solid(lambda p: sd_box(p, (0, NAVE_H / 2, -DEP / 2), (NAVE, NAVE_H / 2, DEP / 2)))
solid(lambda p: sd_box(p, (0, AISLE_H / 2, -DEP / 2), (FW, AISLE_H / 2, DEP / 2)))
solid(lambda p: sd_gable_z(p, -NAVE - 1.5, NAVE + 1.5, NAVE_H, RIDGE, -DEP - 0.5, -1), "roof")
solid(lambda p: sd_leanto(p, NAVE, FW + 1.5, NAVE_H - 9, AISLE_H, -DEP - 0.5, -1), "roof")
solid(lambda p: sd_leanto(p, -NAVE, -FW - 1.5, NAVE_H - 9, AISLE_H, -DEP - 0.5, -1), "roof")
# 土台（少し張り出す石の帯）と、正面の石段
solid(lambda p: sd_box(p, (0, 1.5, -DEP / 2), (FW + 1, 1.5, DEP / 2 + 1)))
solid(lambda p: sd_box(p, (0, 0.7, 2.2), (9, 0.7, 2.2)))
solid(lambda p: sd_box(p, (0, 1.6, 1.4), (7.5, 0.9, 1.4)))
# 正面の4本の塔（外の2本は太く、内の2本は細く高い）。円柱の上に砲弾形の先、節の輪
def castle(cx, y0, cz, r):
    """塔の先の、金色の小さな城（2026-10-06「先にある金色は城に変えて」）: まるい胴に、ぎざぎざの胸壁（凸凹）、
    まんなかに細い小塔と、そのとがり。とがった塔の先が、この城の上へ、さらにのびる。"""
    solid(lambda p: sd_cyl_y(p, cx, cz, r + 0.9, y0, y0 + 2.2), "gold")
    for k in range(6):
        a = k * math.pi / 3
        solid(lambda p, a=a: sd_box(p, (cx + math.cos(a) * (r + 0.6), y0 + 2.8, cz + math.sin(a) * (r + 0.6)), (0.42, 0.6, 0.42)), "gold")
    solid(lambda p: sd_cyl_y(p, cx, cz, r * 0.55 + 0.3, y0 + 2.0, y0 + 4.6), "gold")
    for k in range(4):
        a = k * math.pi / 2 + 0.4
        solid(lambda p, a=a: sd_box(p, (cx + math.cos(a) * (r * 0.55 + 0.25), y0 + 5.0, cz + math.sin(a) * (r * 0.55 + 0.25)), (0.3, 0.45, 0.3)), "gold")
    cut(lambda p: sd_box(p, (cx - 0.2, y0 + 1.1, cz + r + 0.9), (0.35, 0.6, 0.6)), "dark")    # 城の小さな門


TOWERS = [(-19.5, 5.6, 54, 32), (19.5, 5.6, 54, 30), (-9.5, 3.6, 60, 36), (9.5, 3.6, 60, 34)]
for (tx, r, hcol, hsp) in TOWERS:
    solid(lambda p, tx=tx, r=r, hcol=hcol: sd_cyl_y(p, tx, -r * 0.6, r, 0, hcol))
    solid(lambda p, tx=tx, r=r, hcol=hcol, hsp=hsp: sd_spire(p, tx, -r * 0.6, r * 0.82, hcol, hsp))
    for ky in range(14, hcol, 9):
        solid(lambda p, tx=tx, r=r, ky=ky: sd_cyl_y(p, tx, -r * 0.6, r + 0.6, ky, ky + 1.2))      # 節の輪（帯）
    castle(tx, hcol + hsp * 0.72, -r * 0.6, r * 0.42)
    # 塔の胴の、たてのすき間（穴）
    for ky in range(18, hcol - 2, 9):
        for ang in (-0.5, 0.35):
            cut(lambda p, tx=tx, r=r, ky=ky, ang=ang: sd_box(p, (tx + math.sin(ang) * r, ky + 3, -r * 0.6 + math.cos(ang) * r), (0.55, 2.6, 1.6)), "dark")
    # 塔の先の、穴の輪
    for kk in range(3):
        yy = hcol + 6 + kk * 7
        cut(lambda p, tx=tx, r=r, yy=yy: sd_box(p, (tx - 0.8, yy, -r * 0.6 + r * 0.9), (0.5, 1.2, 1.2)), "dark")
# 交差部の高い塔（うしろ）
solid(lambda p: sd_cyl_y(p, 0, -DEP + 7, 5.5, NAVE_H, 64))
solid(lambda p: sd_spire(p, 0, -DEP + 7, 4.6, 64, 22))
castle(0, 64 + 22 * 0.72, -DEP + 7, 4.6 * 0.42)
for ky in (48, 54, 60):
    cut(lambda p, ky=ky: sd_box(p, (2.5, ky + 2, -DEP + 7 + 5), (0.6, 2.4, 1.6)), "dark")
# 正面のまんなかの壁（身廊の正面）と、上の飾り破風
solid(lambda p: sd_box(p, (0, (NAVE_H + 4) / 2, -0.8), (NAVE - 1, (NAVE_H + 4) / 2, 0.8)))
solid(lambda p: sd_tri_front(p, 0, 8.5, NAVE_H + 4, NAVE_H + 17, -1.4, 0.4))
solid(lambda p: sd_sphere(p, (0, NAVE_H + 18.2, -0.6), 1.3), "gold")
# 控え壁（右の側廊の横）と、その上の小尖塔、身廊へわたる飛び梁
for bz in (-7.5, -14.5, -21.5):
    solid(lambda p, bz=bz: sd_box(p, (FW + 1.6, 9, bz), (1.6, 9, 1.1)))
    solid(lambda p, bz=bz: sd_box(p, (FW + 1.1, 21, bz), (1.1, 4, 0.9)))
    solid(lambda p, bz=bz: sd_spire(p, FW + 1.1, bz, 1.2, 25, 7))
    solid(lambda p, bz=bz: sd_capsule(p, (FW + 0.5, 24, bz), (NAVE + 0.2, NAVE_H - 4, bz), 0.75))
# 入口: まんなかの大きな入口（3重に奥へ下がる）と、左右の小さな入口（2重）
for k in range(4):
    cut(lambda p, k=k: sd_arch_z(p, 0, 15 - k * 2.4, 0, 17 - k * 0.8, 0.3, 1.0 + k * 1.1), "stone" if k < 3 else "door")
for sx in (-19.5, 19.5):
    for k in range(3):
        cut(lambda p, sx=sx, k=k: sd_arch_z(p, sx, 8 - k * 1.8, 0, 9 - k * 0.6, 0.3 + 5.6 * 0.4, 0.8 + k * 0.9), "stone" if k < 2 else "door")
# 入口の上の、半月の面（タンパン）は、扉の上を少し浅くして残す
solid(lambda p: sd_box(p, (0, 22.5, -3.5), (5.5, 2.4, 0.6)))
# バラ窓（まんなかの壁）
cut(lambda p: sd_disc_z(p, 0, 34.5, 6.2, 0.0, 1.6), "rose")
# 像の帯（入口の上の、小さなくぼみの列）と、その中の像
for i, x in enumerate((-15, -13, 13, 15)):
    cut(lambda p, x=x: sd_arch_z(p, x, 1.6, 26, 29, 0.6, 1.0, pointed=False), "dark")
# ステンドグラスの窓（2026-10-06「ステンドグラスがはっきりするような」「その枠もしっかり作って」）:
# 窓を大きくし、まわりに張り出した石の枠（アーチの縁どり）、窓台、まんなかのたての桟をつける
def framed_z(sx, w, y0, ys, zf):
    cut(lambda p: sd_arch_z(p, sx, w, y0, ys, zf, 1.1), "glass")
    ring = lambda p: np.maximum(sd_arch_z(p, sx, w + 1.5, y0 - 0.6, ys, zf + 0.5, 0.95), -sd_arch_z(p, sx, w, y0, ys, zf + 0.5, 3.0))
    solid(ring, "frame")
    solid(lambda p: sd_box(p, (sx, y0 - 0.8, zf + 0.3), (w / 2 + 1.1, 0.4, 0.5)), "frame")


def framed_x(cz, w, y0, ys, xf):
    cut(lambda p: sd_arch_x(p, cz, w, y0, ys, xf, 1.2), "glass")
    ring = lambda p: np.maximum(sd_arch_x(p, cz, w + 1.5, y0 - 0.6, ys, xf + 0.5, 0.95), -sd_arch_x(p, cz, w, y0, ys, xf + 0.5, 3.0))
    solid(ring, "frame")
    solid(lambda p: sd_box(p, (xf + 0.3, y0 - 0.8, cz), (0.5, 0.4, w / 2 + 1.1)), "frame")


# （正面の塔のあいだの窓は、塔にかくれて見えないので置かない）
for wz in (-4.0, -11.0, -18.0):
    framed_x(wz, 4.4, 5.5, 16.5, FW)
    framed_x(wz, 3.4, 33.0, 39.0, NAVE)


# ---- 像（立体）: 像の帯のくぼみの中と、まんなかの入口の両わき（柱の像）。体はまるい柱、頭は球、台座は箱
def statue(x, y0, z, hgt, m="statue"):
    solid(lambda p: sd_capsule(p, (x, y0 + 0.9, z), (x, y0 + hgt * 0.62, z), hgt * 0.16), m)          # 体（衣のすそ広がりは、下を少し太く）
    solid(lambda p: sd_capsule(p, (x, y0 + 0.5, z), (x, y0 + hgt * 0.3, z), hgt * 0.2), m)
    solid(lambda p: sd_sphere(p, (x, y0 + hgt * 0.82, z + 0.1), hgt * 0.13), m)                       # 頭
    solid(lambda p: sd_box(p, (x, y0 + 0.3, z), (hgt * 0.24, 0.35, hgt * 0.2)), "stone")             # 台座


for x in (-15, -13, 13, 15):
    statue(x, 26.2, -0.4, 3.0)
for sx in (-8.6, 8.6):
    statue(sx, 2.4, 0.9, 7.6)
    solid(lambda p, sx=sx: sd_box(p, (sx, 1.2, 0.9), (1.4, 1.2, 1.2)))                                 # 柱の像の台
# ---- 細かな飾り: 正面の横の帯（蛇腹）、左右の入口の上の小さな飾り破風、側廊の正面のかどの小尖塔
for yb in (24.5, 31.0):
    solid(lambda p, yb=yb: sd_box(p, (0, yb, 0.25), (FW - 0.5, 0.35, 0.35)))
for sx in (-19.5, 19.5):
    solid(lambda p, sx=sx: sd_tri_front(p, sx, 4.2, 9.6, 15.5, 1.6, 2.6))
    solid(lambda p, sx=sx: sd_sphere(p, (sx, 16.2, 2.1), 0.7), "gold")
for cx_ in (-FW + 0.6, FW - 0.6):
    solid(lambda p, cx_=cx_: sd_cyl_y(p, cx_, 0.0, 1.1, 0, AISLE_H + 2))
    solid(lambda p, cx_=cx_: sd_spire(p, cx_, 0.0, 1.2, AISLE_H + 2, 7))
# 窓の中の桟（たての石の線）
for wz in (-4.0, -11.0, -18.0):
    solid(lambda p, wz=wz: sd_box(p, (FW - 0.75, 12, wz), (0.3, 6.0, 0.28)), "frame")
# バラ窓の、張り出した石の輪
solid(lambda p: np.maximum(np.abs(np.sqrt(p[..., 0] ** 2 + (p[..., 1] - 34.5) ** 2) - 6.9) - 0.75, np.abs(p[..., 2] - 0.2) - 0.45), "frame")


def scene0(p):
    d = np.full(p.shape[:-1], 1e9)
    for f, _ in SOLIDS:
        d = np.minimum(d, f(p))
    for f, _ in CUTS:
        d = np.maximum(d, -f(p))
    return d


def scene(p):
    return scene0(p / S) * S


# ===================================================================== 光線を飛ばす
sx, sy = np.meshgrid(np.arange(W) + 0.5, np.arange(H) + 0.5)
# 絵の (sx, sy) にうつる点: x = sx - CX + (-z)... を、z について進む光線にする
# 正面から: 点 (x, y, z) は、絵の (CX + x - z, GROUND - y + K*z) にうつる（z は奥へ負）
Z0 = 40.0
start = np.stack([sx - CX + Z0, GROUND - sy + K * Z0, np.full_like(sx, Z0)], -1)
rd = np.array([-1.0, -K, -1.0]); rd /= np.linalg.norm(rd)
dist = np.zeros(sx.shape)
hit = np.zeros(sx.shape, bool)
alive = np.ones(sx.shape, bool)
for it in range(260):
    p = start[alive] + rd * dist[alive][:, None]
    d = scene(p)
    idx = np.nonzero(alive)
    dist[idx] += np.maximum(d * 0.9, 0.02)
    h = d < 0.02
    hit[idx[0][h], idx[1][h]] = True
    far = dist[idx] > 200
    gone = h | far | (p[:, 1] < -0.5)
    a2 = alive.copy(); a2[idx[0][gone], idx[1][gone]] = False
    alive = a2
    if not alive.any():
        break
P = start + rd * dist[..., None]
HP = P[hit]


def normal(p):
    e = 0.06
    n = np.stack([scene(p + np.array([e, 0, 0])) - scene(p - np.array([e, 0, 0])),
                  scene(p + np.array([0, e, 0])) - scene(p - np.array([0, e, 0])),
                  scene(p + np.array([0, 0, e])) - scene(p - np.array([0, 0, e]))], -1)
    return n / np.maximum(length(n)[..., None], 1e-6)


N = normal(HP)
L = np.array([-0.55, 0.62, 0.56]); L /= np.linalg.norm(L)
diff = np.clip((N * L).sum(-1), 0, 1)
# 影（光の方へもう一度）
sh = np.ones(len(HP))
q = HP + N * 0.15
t = np.full(len(HP), 0.3)
for it in range(90):
    d = scene(q + L * t[:, None])
    sh = np.minimum(sh, np.clip(8 * d / t, 0, 1))
    t += np.clip(d, 0.08, 2.0)
sh = np.clip(sh, 0, 1)
# すみの暗さ（AO）
ao = np.ones(len(HP))
for k, s in enumerate((0.5, 1.2, 2.2, 3.4)):
    d = scene(HP + N * s)
    ao -= (s - np.minimum(d, s)) / s * (0.5 ** k) * 0.55
ao = np.clip(ao, 0.25, 1)

# 材質（いちばん近い形）
def material(p, n):
    best = np.full(len(p), 1e9); mat = np.array(["stone"] * len(p), dtype=object)
    for f, m in SOLIDS:
        d = np.abs(f(p))
        sel = d < best
        best[sel] = d[sel]; mat[sel] = m
    for f, m in CUTS:
        d = np.abs(f(p))
        sel = (d < 0.12) & (d <= best + 0.05)
        if m in ("glass", "rose", "door"):
            back = sel & ((n[:, 2] > 0.7) | (n[:, 0] > 0.7))
            mat[back] = m
            mat[sel & ~back] = "stone"
        else:
            mat[sel] = m
    return mat


MAT = material(HP / S, N)

# ===================================================================== 色
RAMPS = {
    # 2026-10-06 人間の指示「教会の色白系統で」: 白い石（すこしあたたかい白）
    "stone": ["#34323a", "#4c4a54", "#66646e", "#82808a", "#9e9ca4", "#b8b6bc", "#cfcdd0", "#e2e0e0", "#f0eeea", "#fbfaf6"],
    "statue": ["#3a3a46", "#555564", "#727282", "#9090a0", "#aeaebc", "#cacad4", "#e2e2ea", "#f6f6fa"],
    "roof": ["#1c2230", "#283042", "#363f56", "#47526c", "#5b6884", "#72809c", "#8c9ab4"],
    "dark": ["#140e0c", "#1e1612", "#2a201a", "#382c22"],
    "door": ["#2a160a", "#3e2210", "#5a3418", "#784824", "#965c2e"],
    "glass": ["#141c3a", "#1e3060", "#2c4a88", "#3e6aac", "#5a90cc"],
    "rose": ["#141c3a", "#1e3060", "#2c4a88", "#3e6aac", "#5a90cc"],
    "gold": ["#5a3e10", "#8a6418", "#c0902a", "#e0b040", "#f8dc80"],
    "frame": ["#2a2a32", "#44444e", "#60606a", "#7e7e88", "#9c9ca4", "#b8b8be", "#d2d2d6", "#e8e8ea", "#f8f8f8"],
    "mosaic": ["#5a3e10", "#8a6418", "#c0902a", "#e0b040", "#f8dc80"],
}
BAYER = np.array([[0.125, 0.625], [0.875, 0.375]])

ys_, xs_ = np.nonzero(hit)
img = np.full((H, W), "", dtype=object)
# 2026-10-06 人間の指示「教会はドット一つ一つを細かく」: 奥行きの段差のふちを、1ドットずつ描きわける
#   - 手前の形に重なられている、奥の側のふち → 1段暗い線（形と形の境目がはっきりする）
#   - 光の側（左・上）で、手前に出ている形のふち → 1段明るい線（光があたるふち）
DEPTH = np.full((H, W), np.inf)
DEPTH[ys_, xs_] = dist[ys_, xs_]
for i in range(len(HP)):
    x, y = xs_[i], ys_[i]
    m = MAT[i]
    wp = HP[i] / S
    n = N[i]
    lum = 0.2 + 0.8 * diff[i] * (0.35 + 0.65 * sh[i])
    lum *= 0.55 + 0.45 * ao[i]
    d0 = DEPTH[y, x]
    nb_closer = [DEPTH[y + b, x + a] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + a < W and 0 <= y + b < H]
    if any(dd < d0 - 2.5 for dd in nb_closer):
        lum -= 0.16                                            # 奥のふち（暗い線）
    elif m not in ("glass", "rose", "dark", "door") and diff[i] > 0.3 and any(
            0 <= x + a < W and 0 <= y + b < H and DEPTH[y + b, x + a] > d0 + 2.5 for a, b in ((-1, 0), (0, -1))):
        lum += 0.12                                            # 光の側のふち（明るい線）
    if m == "stone":
        # 石の段と目地: 4ドットごとの横の目地（細く）と、段ごとにずらしたたての目地（ところどころ）
        yy = wp[1]
        course = math.floor(yy / 4.0)
        along = wp[0] if abs(n[2]) > 0.5 else wp[2]
        if abs(n[1]) < 0.6:
            if (yy / 4.0) % 1 < 0.18:
                lum -= 0.06
            elif ((along + (course % 2) * 3.0) / 6.0) % 1 < 0.12 and (course * 7) % 3 != 0:
                lum -= 0.04
        if yy < 9:
            lum -= 0.05 * (1 - yy / 9)                        # 下の方は、しめって暗い
        if n[1] > 0.7:
            lum += 0.06                                        # 上を向いた段の上面は明るい
    if m == "roof":
        rows = (wp[1] * 1.3) % 1
        if rows < 0.25:
            lum -= 0.08
        lum += ((int(wp[2] * 3 + math.floor(wp[1] * 1.3) * 17) % 5) - 2) * 0.015
    ramp = RAMPS[m]
    v = np.clip(lum, 0, 0.999) * (len(ramp) - 1)
    lo = int(v); fr = v - lo
    # 市松でまぜるのは、2つの段のちょうどあいだの所だけ（ざらざらにしない）
    k = lo + (1 if (fr > 0.62 or (0.38 <= fr <= 0.62 and BAYER[y % 2, x % 2] < 0.5)) else 0)
    c = ramp[min(len(ramp) - 1, k)]
    if m == "rose" or m == "glass":
        # ステンドグラス（2026-10-06「はっきりするような」）: 鉛の線で区切った小さな色ガラスの面を、
        # 青・赤・金・緑・むらさき・水色の、はっきりした色で。中から光るので、明るさはあまり落とさない
        LEAD = "#1a1622"
        BRIGHT = [("#2f5fb8", "#22457e"), ("#d03a4a", "#8e2632"), ("#e8b830", "#a87e1c"), ("#3a9a5a", "#276a3e"),
                  ("#7a4ab0", "#54327a"), ("#4aa8dc", "#2e74a0")]
        if m == "rose":
            dx_, dy_ = wp[0], wp[1] - 34.5
            rr = math.hypot(dx_, dy_); ang = (math.atan2(dy_, dx_) + math.pi) / (2 * math.pi)
            ring_i = int(rr / 1.7)
            seg = int(ang * (8 if ring_i < 2 else 16))
            lead = (rr / 1.7) % 1 < 0.22 or (ang * (8 if ring_i < 2 else 16)) % 1 < 0.12
            col = BRIGHT[(seg * 2 + ring_i * 3) % len(BRIGHT)]
        else:
            u = wp[0] if abs(n[2]) > 0.5 else wp[2]
            v = wp[1]
            lead = (u * 1.25) % 1 < 0.22 or (v * 0.9) % 1 < 0.18
            col = BRIGHT[(int(math.floor(u * 1.25)) * 5 + int(math.floor(v * 0.9)) * 3) % len(BRIGHT)]
        c = LEAD if lead else (col[0] if ao[i] > 0.7 else col[1])
    if m == "mosaic":
        c = ["#e04848", "#e0b040", "#f4f0ec", "#4aa0d0", "#3a8a5a", "#c0902a"][(x * 7 + y * 13) % 6] if lum > 0.35 else "#8a6418"
    img[y, x] = c

# バラ窓の放射の桟と、中の灯
rc = (CX + 0 - 0.0, GROUND - 34.5 * S + K * 0)
for y in range(H):
    for x in range(W):
        if img[y, x] == "":
            continue
        dx, dy = x + 0.5 - rc[0], y + 0.5 - rc[1]
        d = math.hypot(dx, dy)
        if 1.5 * S < d < 5.6 * S:
            a = (math.atan2(dy, dx) + math.pi) / (2 * math.pi) * 12
            if a % 1 < 0.2:
                img[y, x] = "#2a201a"
        if d < 1.6 * S:
            img[y, x] = "#fff0a0"

# りんかく
OUT = "#1e1610"
add = []
for y in range(H):
    for x in range(W):
        if img[y, x] != "":
            continue
        if any(0 <= x + a < W and 0 <= y + b < H and img[y + b, x + a] != "" for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            add.append((x, y))
for x, y in add:
    img[y, x] = OUT


# 三つの環のしるし（バラ窓の上に小さく、塔の先の飾り玉に）
def ring(cx, cy, r, col, gap=False):
    for y in range(int(cy - r - 2), int(cy + r + 3)):
        for x in range(int(cx - r - 2), int(cx + r + 3)):
            if not (0 <= x < W and 0 <= y < H):
                continue
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            if abs(d - r) < 0.55:
                a = math.atan2(y + 0.5 - cy, x + 0.5 - cx)
                if gap and -1.35 < a < -0.35:
                    continue
                img[y, x] = col


ring(rc[0], rc[1], 5.2 * S, "#e0b040")
ring(rc[0], rc[1], 3.3 * S, "#c0902a")
ring(rc[0], rc[1], 1.9 * S, "#f8dc80", gap=True)
# 交差部の塔の先に、立つ環
tx, ty = CX + (DEP - 7) * S, GROUND - 89.5 * S - K * (DEP - 7) * S
ring(tx, ty, 2.6, "#e0b040"); ring(tx, ty, 1.3, "#f8dc80", gap=True)
for k in range(2):
    if 0 <= int(ty + 2.5 + k) < H:
        img[int(ty + 2.5 + k), int(tx)] = "#8a6418"

# ===================================================================== 書き出し
cols = sorted(set(img[img != ""].tolist()))
syms = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,-/:;<=>?@[]^_{|}~"
assert len(cols) <= len(syms), len(cols)
cmap = {c: syms[i] for i, c in enumerate(cols)}
rows = ["".join(cmap[img[y, x]] if img[y, x] != "" else "." for x in range(W)) for y in range(H)]
open(os.path.join(HERE, "church.txt"), "w").write("\n".join(rows) + "\n")
json.dump({cmap[c]: c for c in cols}, open(os.path.join(HERE, "pal-church.json"), "w"))
print("ok colors", len(cols))
