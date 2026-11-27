"""ダンスのコマを作る: 正面の絵を部位に分けて、肩・ひじで腕を回し、ひざを曲げて足を上げる。回るときは4方向の絵を順に切りかえ、横に少し縮めて回って見せる。
回転は、8倍に拡大してから回して、もとの大きさに戻す（ドット絵の線がくずれにくい）。"""
import json, math
from collections import Counter
D = json.load(open('/tmp/px5/sheet2.json')); PAL = D['pal']
SW, SH = len(D['grids'][0][0]), len(D['grids'][0])
PADX, PADY = 6, 6
W, H = SW + 2 * PADX, SH + PADY
def to_layer(rows): return {(x + PADX, y + PADY): ch for y, r in enumerate(rows) for x, ch in enumerate(r) if ch != "."}
VIEWS = [to_layer(r) for r in D['grids']]
FRONT, RIGHT, BACK = VIEWS[0], VIEWS[1], VIEWS[2]
LEFT = {(W - 1 - x, y): ch for (x, y), ch in RIGHT.items()}
def inpoly(x, y, poly):
    c = False; n = len(poly)
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: c = not c
    return c
P = lambda pts: [(x + PADX, y + PADY) for x, y in pts]
ARM_L = P([(9, 56), (20, 56), (20, 64), (18, 70), (18, 82), (15, 86), (14, 96), (14, 112), (1, 112), (3, 96), (5, 84), (7, 70)])
ARM_R = P([(54, 56), (43, 56), (43, 64), (45, 70), (45, 82), (48, 86), (49, 96), (50, 112), (62, 112), (60, 96), (58, 84), (56, 70)])
ELBOW_Y = 83 + PADY
SHO_L, SHO_R = (14 + PADX, 57 + PADY), (49 + PADX, 57 + PADY)
ELB_L, ELB_R = (12 + PADX, ELBOW_Y), (51 + PADX, ELBOW_Y)
HIP_Y, KNEE_Y = 101 + PADY, 127 + PADY
MID = 32 + PADX
parts = {k: {} for k in ("body", "head", "uarmL", "farmL", "uarmR", "farmR", "legL", "legR")}
for (x, y), ch in FRONT.items():
    if inpoly(x + 0.5, y + 0.5, ARM_L): parts["uarmL" if y < ELBOW_Y else "farmL"][(x, y)] = ch
    elif inpoly(x + 0.5, y + 0.5, ARM_R): parts["uarmR" if y < ELBOW_Y else "farmR"][(x, y)] = ch
    elif y >= HIP_Y: parts["legL" if x < MID else "legR"][(x, y)] = ch
    elif y < 44 + PADY: parts["head"][(x, y)] = ch
    else: parts["body"][(x, y)] = ch
# 腕を外した所の体のはしに、ふちを付ける（腕が動いても体のはしが切れて見えないように）
DARK = min(PAL, key=lambda k: sum(int(PAL[k][i:i + 2], 16) for i in (1, 3, 5)))
body = parts["body"]
for y in range(58 + PADY, HIP_Y):
    xs = sorted(x for (x, yy) in body if yy == y)
    if not xs: continue
    for x in (xs[0], xs[-1]): body[(x, y)] = DARK
def rot(layer, pivot, ang, dx=0, dy=0, S=8):
    """8倍にして回し、もとの大きさに戻す（8×8 の中でいちばん多い色）。pivot を中心に ang 度（画面で時計回り）"""
    if not layer: return {}
    if abs(ang) < 0.5: return {(x + dx, y + dy): ch for (x, y), ch in layer.items()}
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a); px, py = pivot
    out = {}
    xs = [x for x, _ in layer]; ys = [y for _, y in layer]
    corners = [(x, y) for x in (min(xs) - 1, max(xs) + 2) for y in (min(ys) - 1, max(ys) + 2)]
    tc = [(px + (x - px) * ca - (y - py) * sa, py + (x - px) * sa + (y - py) * ca) for x, y in corners]
    X0, X1 = int(math.floor(min(t[0] for t in tc))) - 1, int(math.ceil(max(t[0] for t in tc))) + 1
    Y0, Y1 = int(math.floor(min(t[1] for t in tc))) - 1, int(math.ceil(max(t[1] for t in tc))) + 1
    for Y in range(Y0, Y1):
        for X in range(X0, X1):
            cnt = Counter()
            for j in range(S):
                for i in range(S):
                    fx, fy = X + (i + 0.5) / S - px, Y + (j + 0.5) / S - py
                    sx, sy = px + fx * ca + fy * sa, py - fx * sa + fy * ca          # 逆回し
                    ch = layer.get((math.floor(sx), math.floor(sy)))
                    cnt[ch] += 1
            ch, n = cnt.most_common(1)[0]
            if ch is None:
                if n < S * S * 0.62:                                                 # 半分より少し多く色が入っていれば色にする
                    ch = next(c for c, _ in cnt.most_common() if c is not None)
                else: continue
            out[(X + dx, Y + dy)] = ch
    return out
def shift(layer, dx, dy): return {(x + dx, y + dy): ch for (x, y), ch in layer.items()}
def squash_x(layer, s, cx):
    """横に s 倍（回っているように見せる）。いちばん近いマスの色"""
    if abs(s - 1) < 0.01: return dict(layer)
    out = {}
    xs = [x for x, _ in layer]; ys = [y for _, y in layer]
    for y in range(min(ys), max(ys) + 1):
        for X in range(int(cx + (min(xs) - cx) * s) - 1, int(cx + (max(xs) + 1 - cx) * s) + 2):
            sx = math.floor(cx + (X + 0.5 - cx) / s)
            if (sx, y) in layer: out[(X, y)] = layer[(sx, y)]
    return out
def bend_leg(layer, lift, out_dx=0):
    """足を上げる: ひざから下を lift マス上へ、ふとももは lift 行ぶんちぢめる（ひざが前に出たように見える）"""
    if lift <= 0 and out_dx == 0: return dict(layer)
    out = {}
    thigh = [y for y in range(HIP_Y, KNEE_Y)]; n = len(thigh); keep = n - lift
    for (x, y), ch in layer.items():
        if y < HIP_Y: out[(x, y)] = ch
        elif y < KNEE_Y:
            k = y - HIP_Y; ny = HIP_Y + int(k * keep / n)
            out[(x + round(out_dx * k / n), ny)] = ch
        else: out[(x + out_dx, y - lift)] = ch
    return out
def pose(t):
    """t: コマの番号 → 部位ごとの動かし方"""
    return dict(bx=0, by=0, hy=0, ua=(0, 0), fa=(0, 0), liftL=0, liftR=0, legdx=(0, 0), spin=None)
def render(p):
    if p["spin"] is not None:                                                     # 回る: 4方向の絵を切りかえ、横を縮める
        phi = p["spin"] % 360; q = int(((phi + 45) % 360) // 90)
        view = [FRONT, RIGHT, BACK, LEFT][q]
        u = ((phi + 45) % 90) / 90; s = 0.72 + 0.28 * math.sin(math.pi * u)
        return shift(squash_x(view, s, W / 2), 0, p["by"])
    bx, by, hy = p["bx"], p["by"], p["hy"]
    L = {}
    def add(layer): L.update(layer)
    add(bend_leg(shift(parts["legL"], bx + p["legdx"][0], 0), p["liftL"]))
    add(bend_leg(shift(parts["legR"], bx + p["legdx"][1], 0), p["liftR"]))
    add(shift(parts["body"], bx, by))
    add(shift(parts["head"], bx, by + hy))
    for side, sgn in (("L", 1), ("R", -1)):
        ua, fa = p["ua"][0 if side == "L" else 1], p["fa"][0 if side == "L" else 1]
        sho = (SHO_L if side == "L" else SHO_R); elb = (ELB_L if side == "L" else ELB_R)
        add(rot(parts["uarm" + side], sho, sgn * ua, bx, by))
        a = math.radians(sgn * ua); ex = sho[0] + (elb[0] - sho[0]) * math.cos(a) - (elb[1] - sho[1]) * math.sin(a); ey = sho[1] + (elb[0] - sho[0]) * math.sin(a) + (elb[1] - sho[1]) * math.cos(a)
        if p.get("hide_farm"): continue
        fr = rot(parts["farm" + side], elb, sgn * (ua + fa), 0, 0)
        add(shift(fr, round(ex - elb[0]) + bx, round(ey - elb[1]) + by))
    return L
def grid(layer):
    g = [["."] * W for _ in range(H)]
    for (x, y), ch in layer.items():
        if 0 <= x < W and 0 <= y < H: g[y][x] = ch
    return ["".join(r) for r in g]
def png(frames, path, z=3, cols=8):
    from PIL import Image
    rgb = {k: tuple(int(v[i:i + 2], 16) for i in (1, 3, 5)) for k, v in PAL.items()}
    rows_ = (len(frames) + cols - 1) // cols
    im = Image.new('RGB', (W * z * cols, H * z * rows_), (104, 100, 92))
    for k, g in enumerate(frames):
        ox, oy = (k % cols) * W * z, (k // cols) * H * z
        for y, r in enumerate(g):
            for x, ch in enumerate(r):
                if ch != ".": im.paste(rgb[ch], (ox + x * z, oy + y * z, ox + x * z + z, oy + y * z + z))
    im.save(path)
if __name__ == "__main__":
    base = dict(bx=0, by=0, hy=0, ua=(0, 0), fa=(0, 0), liftL=0, liftR=0, legdx=(0, 0), spin=None)


# ---------- 手拍子の腕: 前うでと手を、肌の色の段で描く ----------
SKIN = ["U", "e", "i", "m", "n", "t", "x", "z", "1"]; SKO = "H"
def draw_arm(L, elb, wr, side, open_=0.0):
    """elb（ひじ）から wr（手首）へ前うでを描き、手首の先に手（指は上）を描く。side: 'L' か 'R'（画面の左右）"""
    (ex, ey), (wx, wy) = elb, wr; m = {}
    dx, dy = wx - ex, wy - ey; ln = math.hypot(dx, dy); ux, uy = dx / ln, dy / ln; nx, ny = -uy, ux
    for y in range(int(min(ey, wy)) - 4, int(max(ey, wy)) + 5):
        for x in range(int(min(ex, wx)) - 4, int(max(ex, wx)) + 5):
            px, py = x + 0.5 - ex, y + 0.5 - ey; t = max(0, min(1, (px * ux + py * uy) / ln))
            r = 3.1 - 0.7 * t; d = (px - t * dx) * nx + (py - t * dy) * ny
            if abs(d) <= r and -1.5 <= px * ux + py * uy <= ln + 0.5: m[(x, y)] = d / r
    # 手: 手のひらを内がわに向けて、指は上（横から見た手の形）
    hx = wx + (1.5 if side == "L" else -1.5); hm = {}
    for y in range(int(wy) - 9, int(wy) + 2):
        for x in range(int(hx) - 4, int(hx) + 4):
            u = (x + 0.5 - hx) / 2.4; v = (y + 0.5 - (wy - 3.5)) / 5.2
            if u * u + v * v <= 1: hm[(x, y)] = u
    light = (-0.6, -0.8)
    cells = {}
    for (x, y), d in m.items():
        l = 0.55 + 0.45 * (-d if side == "L" else -d) * (nx * light[0] + ny * light[1]) * -1
        cells[(x, y)] = SKIN[max(0, min(len(SKIN) - 1, round(l * (len(SKIN) - 1))))]
    for (x, y), u in hm.items():
        l = 0.75 - 0.35 * u if side == "L" else 0.62 + 0.3 * -u
        cells[(x, y)] = SKIN[max(0, min(len(SKIN) - 1, round(l * (len(SKIN) - 1))))]
    allm = set(m) | set(hm)
    for (x, y) in allm:                                       # ふち
        if any((x + a, y + b) not in allm for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))): cells[(x, y)] = SKO
    fx = int(hx) + (1 if side == "L" else -2)                 # 指のさかい（2本）
    for y in (int(wy) - 6, int(wy) - 4):
        if (fx, y) in cells and cells[(fx, y)] != SKO: cells[(fx, y)] = "i"
    L.update(cells)
def clap_arms(L, bx, by, open_):
    """open_: 0＝手を合わせる、1＝ひらく"""
    cy = 77 + PADY - round(2 * open_)
    for side, elb, sgn in (("L", ELB_L, -1), ("R", ELB_R, 1)):
        wx = MID + sgn * (3 + 9 * open_) - (0 if side == "L" else 1)
        draw_arm(L, (elb[0] + bx + (1 if side == "L" else -1), elb[1] + by - 1), (wx + bx, cy + by), side, open_)
_render0 = render
def render(p):
    if p["spin"] is not None or p.get("clap") is None: return _render0(p)
    q = dict(p); L = _render0(dict(q, ua=(0, 0), fa=(0, 0), hide_farm=True))
    clap_arms(L, p["bx"], p["by"], p["clap"])
    return L

if __name__ == "__main__":
    base = dict(bx=0, by=0, hy=0, ua=(0, 0), fa=(0, 0), liftL=0, liftR=0, legdx=(0, 0), spin=None)
    tests = [dict(base, clap=c) for c in (0, 0.3, 0.7, 1.0)] + [dict(base, clap=0, by=2), dict(base, bx=4, liftR=4)]
    png([grid(render(p)) for p in tests], '/tmp/px5/rigtest.png', z=3)
    from PIL import Image
    im = Image.open('/tmp/px5/rigtest.png'); im.crop((0, 0, W * 3 * 2, H * 3 * 2 // 3)).resize((W * 3 * 4, H * 3 * 4 // 3), Image.NEAREST).save('/tmp/px5/claptest.png')
