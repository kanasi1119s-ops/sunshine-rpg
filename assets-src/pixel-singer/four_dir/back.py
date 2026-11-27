import sys; sys.path.insert(0,'/tmp/px4'); from lib import *
import math, random
g = [r[:] for r in FRONT]
rnd = random.Random(7)
def span(y):
    xs = [x for x in range(W) if FRONT[y][x] != "."]; return (min(xs), max(xs)) if xs else None
# ---------- 頭（後ろ髪） ----------
hm = set()
tip = {}
for y in range(2, 42):
    sp = span(y)
    if not sp: continue
    a, b = sp
    if y >= 36:   # 正面では あご・首が見える所。後ろからは髪でおおう（両はしの毛先の形はそのまま）
        a0, b0 = span(35); a, b = min(a, a0 + (y - 35) // 2), max(b, b0 - (y - 35) // 2)
    for x in range(a, b + 1): hm.add((x, y))
# 房を1本ずつ決める: つむじ（上）から毛先（下）への中心の線。となりの房とのさかいは、中心と中心のまん中
CL = []   # (上の x, 下の x, 毛先の y, 波の大きさ, 波のずれ)
for k, bx in enumerate([2, 7, 11.5, 16, 20.5, 25, 29.5, 34, 38.5, 43, 48]):
    tx = 25.5 + (bx - 25.5) * 0.28
    CL.append((tx, bx, (39, 40, 41, 39, 41, 40, 41, 39, 41, 40, 39)[k], 1.2 + 0.4 * (k % 3), k * 1.3))
def cx_at(c, y):
    tx, bx, ey, amp, ph = c; t = max(0, min(1, (y - 3) / 34)); t2 = 1 - (1 - t) ** 1.6
    return tx + (bx - tx) * t2 + amp * math.sin(t * math.pi * 1.4 + ph) * t
def clump_of(x, y):
    xs = [cx_at(c, y) for c in CL]
    for i in range(len(xs) - 1):
        if x < (xs[i] + xs[i + 1]) / 2: 
            lo = (xs[i - 1] + xs[i]) / 2 if i else xs[i] - 4; hi = (xs[i] + xs[i + 1]) / 2
            return i, (x - lo) / max(1, hi - lo)
    i = len(xs) - 1; lo = (xs[i - 1] + xs[i]) / 2; return i, (x - lo) / max(1, xs[i] + 4 - lo)
# 毛先: 房ごとに長さを変えて、先をとがらせる（下へふくらませない）
for (x, y) in list(hm):
    i, fr = clump_of(x, y); ey = CL[i][2] - (1 if i % 2 else 0)
    cut = ey - round(3 * abs(fr - 0.5) * 2)        # 房のまん中が長く、さかいほど短い（先がとがる）
    if y > cut or y >= 41: hm.discard((x, y))
R = RAMP["hair"]
cells = {}
for (x, y) in hm:
    i, fr = clump_of(x, y)
    gl = 1.0 - 0.7 * max(0, (x - 12) / 36) - 0.25 * max(0, (y - 4) / 34)       # 頭全体: 左上が明るく、右下が暗い
    if fr < 0.14: cl = -0.38                                                  # 房のさかい（深いかげ）
    elif fr < 0.45: cl = 0.22                                                 # 房の左がわ（光が当たる）
    elif fr < 0.75: cl = 0.08
    else: cl = -0.12                                                          # 房の右がわ（かげ）
    light = gl * 0.8 + 0.06 + cl
    r = math.hypot(x - 25.5, (y - 3) * 1.25)
    if 11.5 <= r <= 13.5 and 8 < x < 32 and 0.14 <= fr < 0.75: light += 0.3   # つやの帯
    light -= 0.25 * max(0, (y - 31) / 9)                                      # 毛先へ向かって暗く
    i_ = 3 + round(max(0, min(1, light)) * 8)
    cells[(x, y)] = R[min(11, i_)]
put(g, {(x, y): "." for y in range(0, 42) for x in range(W)})
put(g, cells)
# ヘアバンド: つむじの前を通る帯のうしろがわ（上の2〜3段だけ見える）
for x in range(W):
    for y in (3, 4):
        if (x, y) in hm and 13 <= x <= 37:
            g[y][x] = ("g" if x < 24 else "Y") if y == 3 else "P"
# ---------- 首・スカーフ・えり ----------
for y in range(38, 48):
    for x in range(W):
        if (x, y) in hm: continue
        if FRONT[y][x] == "." and not (36 <= y <= 47 and 16 <= x <= 34): continue
        if y <= 41 and 21 <= x <= 29: g[y][x] = "k" if x in (21, 29) else "p"            # うなじ
        elif 41 <= y <= 44 and 16 <= x <= 34: g[y][x] = "P" if y == 44 or x in (16, 34) else ("g" if x < 25 else "Y")   # スカーフの帯
        elif y >= 44 and FRONT[y][x] != ".": g[y][x] = "3"
# ---------- 背中・うで ----------
for y in range(44, 77):
    sp = span(y)
    if not sp: continue
    a, b = sp
    for x in range(a, b + 1):
        if y < 44 or FRONT[y][x] == ".": continue
        if (x, y) in hm: continue
        if y == 44 and not (12 <= x <= 38): continue
        g[y][x] = "w"   # 仮の白
# うでの位置: 正面と同じ（そで y44〜61・ひじ y60〜72）
def arm_spans(left):
    out = {}
    for y in range(45, 74):
        a, b = span(y)
        if y <= 61: w_ = 9 if y > 47 else 6
        else: w_ = max(4, 8 - (y - 62) // 3)
        out[y] = (a, a + w_) if left else (b - w_, b)
    return out
la, ra = arm_spans(True), arm_spans(False)
armmask = set()
for sp_ in (la, ra):
    for y, (a, b) in sp_.items():
        for x in range(a, b + 1): armmask.add((x, y))
torso = set()
for y in range(44, 77):
    sp = span(y)
    if not sp: continue
    for x in range(sp[0], sp[1] + 1):
        if g[y][x] == "w" and (x, y) not in armmask: torso.add((x, y))
# 背中の白: 少し右へ暗く。肩甲骨のあたりにかげ、腰で軽いしわ
tc = shade(torso, "white", peak=0.38, lo=3, hi=8, vgrad=0.2)
for (x, y), ch in tc.items():
    if y in (52, 53) and (16 <= x <= 20 or 30 <= x <= 34): ch = darker(ch, 1)      # 肩甲骨のかげ
    if x == 25 and 46 <= y <= 74: ch = darker(ch, 1)                               # 背中のまん中の縫い目
    if y >= 70 and x % 4 == 1: ch = darker(ch, 1)                                   # 腰のしわ（ベルトに入れたあたり）
    if y == 49 and 14 <= x <= 36: ch = darker(ch, 1)                                # 肩のヨーク
    tc[(x, y)] = ch
put(g, tc)
for side, sp_ in ((0, la), (1, ra)):
    sl = {(x, y) for y, (a, b) in sp_.items() if y <= 61 for x in range(a, b + 1) if FRONT[y][x] != "."}
    sk = {(x, y) for y, (a, b) in sp_.items() if y >= 60 for x in range(a, b + 1) if FRONT[y][x] != "."}
    put(g, shade(sl, "white", peak=0.25 if side == 0 else 0.55, lo=2, hi=8, vgrad=0.25))
    put(g, shade(sk, "skin", peak=0.3 if side == 0 else 0.6, lo=2, hi=9, vgrad=0.2))
    for x in range(W):                                   # そでのすそ
        if (x, 60) in sl: g[60][x] = "j"; g[61][x] = "r"
    # うでと背中のあいだの線
    for y in range(47, 74):
        if y not in sp_: continue
        a, b = sp_[y]; xe = b + 1 if side == 0 else a - 1
        if 0 <= xe < W and g[y][xe] != ".": g[y][xe] = "b" if y <= 61 else "D"
# ---------- ベルト（うしろ: 金具なし、ベルト通し） ----------
for y in range(76, 81):
    for x in range(W):
        if FRONT[y][x] == "." or mat_of(FRONT[y][x]) in ("denim",): continue
        if y == 76: g[y][x] = "t" if FRONT[y][x] != "." else "."
        else: g[y][x] = {77: "S", 78: "O", 79: "L", 80: "H"}[y]
        if x in (14, 20, 30, 36) and 77 <= y <= 80: g[y][x] = "F" if y in (77, 80) else "C"
# ---------- ショートパンツ（うしろ: 左右のふくらみ、まん中の縫い目、ポケット2つ）----------
SHM = {(x, y) for y in range(81, 95) for x in range(W) if FRONT[y][x] != "." and mat_of(FRONT[y][x]) in ("denim", "white", "sock", None)}
for half, (x0, x1) in enumerate(((0, 25), (25, W))):
    m = {(x, y) for (x, y) in SHM if x0 <= x < x1}
    put(g, shade(m, "denim", peak=0.35, lo=2, hi=7, vgrad=0.3, bias=0.12, noise=0.1, seed=3 + half))
for y in range(81, 95): g[y][25] = "G"                                    # まん中の縫い目
for y in range(91, 95): g[y][24] = "K"; g[y][26] = "K"
for px0 in (13, 29):                                                     # うしろポケット（上が白っぽい縫い目、下はとがった形）
    for y in range(83, 92):
        hw = 4 if y < 90 else (3 if y == 90 else 2)
        for x in range(px0 + 4 - hw, px0 + 5 + hw):
            if (x, y) not in SHM: continue
            edge = y == 83 or x in (px0 + 4 - hw, px0 + 4 + hw) or y == 91
            if y == 83: g[y][x] = "e"
            elif y == 84: g[y][x] = "K"
            elif edge: g[y][x] = "Z" if x < px0 + 4 else "R"
for x, y, c in ((8, 89, "x"), (9, 89, "2"), (10, 90, "x"), (11, 90, "t"), (40, 89, "x"), (41, 89, "2"), (39, 90, "t"), (42, 90, "x"), (21, 92, "x"), (33, 92, "x")):
    if (x, y) in SHM: g[y][x] = c                                       # ダメージ加工の白いすじ
# ---------- ひざのうら ----------
for y, xs in ((125, (18, 19, 20)), (126, (17, 21)), (125, (31, 32, 33)), (126, (30, 34))):
    for x in xs:
        if g[y][x] != ".": g[y][x] = "c"
# ---------- ブーツ（うしろ: ひもなし。まん中にかかとの縫い目、上につまみ） ----------
for side in (0, 1):
    bm = {(x, y) for y in range(150, 167) for x in (range(12, 26) if side == 0 else range(26, 42)) if FRONT[y][x] != "."}
    put(g, shade(bm, "brown", peak=0.35, lo=1, hi=7, vgrad=0.25))
    xs = [x for x, y in bm]; c = (min(xs) + max(xs)) // 2
    for y in range(151, 166): g[y][c] = darker(g[y][c], 1)
    for y in (148, 149, 150): 
        if g[y][c] != ".": g[y][c] = "L"
    for x in range(min(xs), max(xs) + 1):
        if (x, 157) in bm: g[157][x] = "H"
        if (x, 158) in bm: g[158][x] = "L"
outline(g, lambda ch: OUT.get(mat_of(ch), "A"))
BACK = g
if __name__ == "__main__":
    save_png([FRONT, BACK], "/tmp/px4/back.png", z=4)
