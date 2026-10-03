"""世界地図（大陸アルテシア）の地形を作る。決まった種（seed）から毎回同じ地図ができる。
出力: src/game/map/world/world-map.generated.ts（地形を1行1文字の文字列で）と、確認用の画像 /tmp/claude-0-s/world-preview.png
地形: O=海 P=平原 F=森 T=雪の森 M=山（通れない） D=砂漠 S=雪原 R=道 H=丘 L=湖・川（通れない） C=雲の橋・浮島の雲 W=荒れ地（虚灯宮のまわり）
町・環灯台・渡し場の位置は、ここで決めて TypeScript に書き出す。"""
import math, heapq, sys
import numpy as np
from PIL import Image

S = 3.5   # 大きさの倍率（ドラクエ5のような広い大陸にする）
W, H = int(72*S), int(54*S)
rng = np.random.default_rng(20261003)
def sc(v): return int(round(v*S))

def value_noise(w, h, scale, seed):
    r = np.random.default_rng(seed)
    gw, gh = int(w/scale)+3, int(h/scale)+3
    g = r.random((gh, gw))
    out = np.zeros((h, w))
    for y in range(h):
        for x in range(w):
            fx, fy = x/scale, y/scale
            ix, iy = int(fx), int(fy)
            tx, ty = fx-ix, fy-iy
            tx = tx*tx*(3-2*tx); ty = ty*ty*(3-2*ty)
            a = g[iy, ix]*(1-tx)+g[iy, ix+1]*tx
            b = g[iy+1, ix]*(1-tx)+g[iy+1, ix+1]*tx
            out[y, x] = a*(1-ty)+b*ty
    return out

def fbm(w, h, seed, base=12):
    # 大きなうねり（base）に、タイル数で決まった細かいゆらぎ（12・6・3マス）を重ねる（広くしても、海岸線や森の形が細かくなる）
    return (value_noise(w, h, base, seed)*0.40 + value_noise(w, h, base/2, seed+1)*0.22 + value_noise(w, h, 12, seed+2)*0.17
            + value_noise(w, h, 6, seed+3)*0.13 + value_noise(w, h, 3, seed+4)*0.08)/1.0

n1 = fbm(W, H, 11, 12*S); n2 = fbm(W, H, 23, 9*S); n3 = fbm(W, H, 37, 7*S)
T = [["O"]*W for _ in range(H)]

# 大陸の陸地: 東西に長いだ円を、ノイズでぎざぎざに
for y in range(H):
    for x in range(W):
        d = math.hypot((x-36*S)/(32.0*S), (y-27*S)/(21.0*S))
        if d + (n1[y, x]-0.5)*0.75 < 0.98:
            T[y][x] = "P"
# 北東の浮島（浮嶼）
for cx, cy, r in ((64*S, 20*S, 3.6*S), (68*S, 25*S, 3.0*S), (62*S, 26*S, 2.6*S)):
    for y in range(H):
        for x in range(W):
            if math.hypot(x-cx, (y-cy)*1.1) + (n2[y, x]-0.5)*3*S < r:
                T[y][x] = "C"
# 虚灯宮の半島（東の海岸）
for y in range(H):
    for x in range(W):
        if math.hypot((x-67*S)/(5.0*S), (y-37*S)/(6.0*S)) + (n2[y, x]-0.5)*0.6 < 1.0:
            T[y][x] = "W"

def land(x, y): return T[y][x] not in "O"

# 山脈（分水嶺）: x=29〜33の南北の帯。北の端から南の端まで、ノイズで幅を変える
for y in range(sc(5), sc(46)):
    cx = 30*S + math.sin(y*0.22/S)*2.5*S
    wid = (2.2 + n2[y, int(cx)%W]*2.2)*S
    for x in range(W):
        if abs(x-cx) < wid and T[y][x] == "P":
            T[y][x] = "M"
# 霧断崖のあたり（北東の断崖）
for y in range(H):
    for x in range(W):
        if math.hypot((x-53*S)/(5.5*S), (y-18*S)/(5.0*S)) + (n3[y, x]-0.5)*0.9 < 1.0 and T[y][x] == "P":
            T[y][x] = "M" if n1[y, x] > 0.45 else "H"
# 雪原（北）
for y in range(H):
    for x in range(W):
        if y <= 13*S + (n1[y, x]-0.5)*9*S and T[y][x] in "PH" and x > 40*S - (n3[y, x]-0.5)*6*S:
            T[y][x] = "S"
        if y <= 10 and T[y][x] == "M":
            T[y][x] = "M"
# 砂漠（中南東）
for y in range(H):
    for x in range(W):
        if math.hypot((x-46*S)/(9.0*S), (y-36*S)/(6.5*S)) + (n3[y, x]-0.5)*0.7 < 1.0 and T[y][x] == "P":
            T[y][x] = "D"
# 森（ノイズの高いところ）と丘
for y in range(H):
    for x in range(W):
        if T[y][x] == "P":
            if n1[y, x] > 0.53 and n3[y, x] > 0.43: T[y][x] = "F"
            elif n2[y, x] > 0.57: T[y][x] = "H"
# 小さな山地（あちこちに）と、そのふもとの丘
for y in range(H):
    for x in range(W):
        if T[y][x] == "P" and n2[y, x] > 0.70 and n3[y, x] > 0.5 and abs(x-30*S) > 6*S:
            T[y][x] = "M"
for y in range(1, H-1):
    for x in range(1, W-1):
        if T[y][x] == "P" and any(T[y+dy][x+dx] == "M" for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))) and n1[y, x] > 0.4:
            T[y][x] = "H"
# 雪原の針葉樹林（T）
for y in range(H):
    for x in range(W):
        if T[y][x] == "S" and n1[y, x] > 0.56 and n3[y, x] > 0.42:
            T[y][x] = "T"
# 小さな湖（あちこちに）
for y in range(H):
    for x in range(W):
        if T[y][x] in "PFH" and n3[y, x] > 0.80 and n1[y, x] > 0.5:
            T[y][x] = "L"
# 湖（硝子湖）と川
for y in range(H):
    for x in range(W):
        if math.hypot((x-22*S)/(5.2*S), (y-22*S)/(3.8*S)) + (n3[y, x]-0.5)*0.7 < 1.0 and land(x, y):
            T[y][x] = "L"
def river(x0, y0, x1, y1):
    n = max(abs(x1-x0), abs(y1-y0))*2
    for i in range(n+1):
        t = i/n
        x = int(round(x0+(x1-x0)*t + math.sin(t*9*S/2+x0)*1.6*S/1.5)); y = int(round(y0+(y1-y0)*t))
        if 0 <= x < W and 0 <= y < H and T[y][x] in "PFHDS": T[y][x] = "L"
river(sc(22), sc(25), sc(20), sc(40)); river(sc(38), sc(8), sc(41), sc(22)); river(sc(44), sc(24), sc(47), sc(30))

TOWNS = {  # マップID: (x, y, 名前)
    "touri-town": (24, 105, "灯里"), "mugikano-village": (52, 108, "麦香野"), "garasuko-town": (77, 94, "硝子湖"),
    "tetsukusari-town": (108, 60, "鉄鏈鉱山"), "toushin-town": (133, 88, "灯芯都"), "sanone-town": (158, 122, "砂音"),
    "kiri-town": (182, 74, "霧断崖"), "shimohara-town": (203, 35, "霜原"), "fushima-town": (224, 74, "浮嶼"), "kyotoukyu-court": (234, 130, "虚灯宮"),
}
# 町のまわり（半径2）は、通れる地面にならす
for mid, (tx, ty, _n) in TOWNS.items():
    base = "C" if mid == "fushima-town" else "W" if mid == "kyotoukyu-court" else "S" if mid == "shimohara-town" else "D" if mid == "sanone-town" else "P"
    for y in range(ty-2, ty+3):
        for x in range(tx-2, tx+3):
            if 0 <= x < W and 0 <= y < H and (abs(x-tx)+abs(y-ty) <= 3):
                T[y][x] = base if T[y][x] in "OLMF" or mid in ("fushima-town",) else T[y][x]

COST = {"T": 2.2, "P": 1.0, "F": 2.2, "D": 1.4, "S": 1.8, "H": 2.0, "M": 9.0, "R": 0.4, "W": 1.2, "C": 1.0, "L": 99999, "O": 99999}
def astar(a, b):
    (ax, ay), (bx, by) = a, b
    pq = [(0, ax, ay)]; best = {(ax, ay): 0}; prev = {}
    while pq:
        c, x, y = heapq.heappop(pq)
        if (x, y) == (bx, by): break
        if c > best[(x, y)]: continue
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if not (0 <= nx < W and 0 <= ny < H): continue
            k = COST[T[ny][nx]]
            if k >= 99999: continue
            k += (n3[ny, nx]-0.5)*0.8
            nc = c + k
            if nc < best.get((nx, ny), 1e9):
                best[(nx, ny)] = nc; prev[(nx, ny)] = (x, y); heapq.heappush(pq, (nc, nx, ny))
    path = []; cur = (bx, by)
    while cur != (ax, ay):
        path.append(cur); cur = prev[cur]
    path.append((ax, ay)); return path[::-1]

def carve_road(a, b, bridge=True):
    for (x, y) in astar(a, b):
        if T[y][x] not in "CW": T[y][x] = "R"   # 海・川の上は、そのまま橋・堤道になる

def pos(mid): return TOWNS[mid][:2]
# 川をわたる橋のために、川も通れる道を許す: 道を引くときだけ川（L）に高いが有限の費用を付けて通す
COST["L"] = 6.0
COST["O"] = 25.0   # 小さな入り江などは、道（堤道）でわたれる
for a, b in (("touri-town", "mugikano-village"), ("mugikano-village", "garasuko-town"), ("garasuko-town", "tetsukusari-town"),
             ("garasuko-town", "toushin-town"), ("toushin-town", "sanone-town"), ("toushin-town", "kiri-town"),
             ("kiri-town", "shimohara-town"), ("sanone-town", "kyotoukyu-court"), ("kiri-town", "fushima-town")):
    carve_road(pos(a), pos(b))
COST["L"] = 99999
COST["O"] = 99999
# 浮嶼への雲の橋: 霧断崖から浮島へ、雲のタイルでつなぐ
x0, y0 = pos("kiri-town"); x1, y1 = pos("fushima-town")
n = max(abs(x1-x0), abs(y1-y0))*2
for i in range(n+1):
    t = i/n
    x = int(round(x0+(x1-x0)*t)); y = int(round(y0+(y1-y0)*t + math.sin(t*5)*1.2*S))
    if T[y][x] in "OLM": T[y][x] = "C"
    elif T[y][x] != "R": pass

# 到達確認（町すべてに、灯里から歩いて行ける）
def reachable():
    sx, sy = pos("touri-town")
    seen = {(sx, sy)}; st = [(sx, sy)]
    while st:
        x, y = st.pop()
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in seen and T[ny][nx] in "PFDSRHCWT":
                seen.add((nx, ny)); st.append((nx, ny))
    return seen
seen = reachable()
for mid, (x, y, nm) in TOWNS.items():
    assert (x, y) in seen, f"{nm} に歩いて行けない"
    assert (x, y+1) in seen, f"{nm} の入口の下が歩けない"

# 環灯台（8神の欠片をささげる灯台）: 各地方の町のそばの、道ではない通れるマス
BEACON_TOWNS = ["mugikano-village", "garasuko-town", "tetsukusari-town", "sanone-town", "kiri-town", "shimohara-town", "fushima-town", "toushin-town"]
OFFS = [(3, 0), (-3, 0), (0, -3), (0, 3), (3, 2), (-3, 2), (3, -2), (-3, -2), (2, 3), (-2, 3), (4, 1), (-4, 1)]
BEACONS = []
used = set()
for mid in BEACON_TOWNS:
    tx, ty, _ = TOWNS[mid]
    for dx, dy in OFFS:
        x, y = tx+dx, ty+dy
        if 0 <= x < W and 0 <= y < H and T[y][x] in "PFDSHCWT" and (x, y) in seen and (x, y) not in used and all((x+ax, y+ay) not in used for ax, ay in ((1,0),(-1,0),(0,1),(0,-1))):
            BEACONS.append((x, y)); used.add((x, y)); break
    else:
        raise SystemExit(f"{mid} の環灯台を置けない")
assert len(BEACONS) == 8

# 渡し場（虚灯宮の南の海岸）: 海に接する通れるマス
FERRY = None
for y in range(sc(44), sc(30), -1):
    for x in range(sc(60), sc(71)):
        if T[y][x] in "PFDHW" and (x, y) in seen and any(0 <= y+dy < H and 0 <= x+dx < W and T[y+dy][x+dx] == "O" for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))) and abs(x-67*S)+abs(y-37*S) > 3*S:
            FERRY = (x, y); break
    if FERRY: break
assert FERRY, "渡し場を置けない"
# 渦（大渦）: 南東の沖
VORTEX = (sc(66), sc(49))

rows = ["".join(r) for r in T]
ts = ["// 自動生成: tools/world-map/gen_world.py（手で編集しない）。大陸アルテシアの地形。1文字=1マス。",
      "// O=海 P=平原 F=森 T=雪の森 M=山 D=砂漠 S=雪原 R=道 H=丘 L=湖・川 C=雲 W=荒れ地",
      f"export const WORLD_WIDTH = {W};", f"export const WORLD_HEIGHT = {H};",
      "export const WORLD_ROWS: string[] = [", *[f'  "{r}",' for r in rows], "];",
      "export const WORLD_TOWNS: Record<string, { x: number; y: number; name: string }> = {",
      *[f'  "{k}": {{ x: {v[0]}, y: {v[1]}, name: "{v[2]}" }},' for k, v in TOWNS.items()], "};",
      "/** 環灯台（8神の欠片をささげる灯台）。番号は神の番号（1=女神…8=冥神）。 */",
      "export const WORLD_BEACONS: Array<{ x: number; y: number }> = [", *[f"  {{ x: {x}, y: {y} }}," for x, y in BEACONS], "];",
      f"export const WORLD_FERRY = {{ x: {FERRY[0]}, y: {FERRY[1]} }};", f"export const WORLD_VORTEX = {{ x: {VORTEX[0]}, y: {VORTEX[1]} }};"]
import os
os.makedirs("/home/user/sunshine-rpg/src/game/map/world", exist_ok=True)
open("/home/user/sunshine-rpg/src/game/map/world/world-map.generated.ts", "w").write("\n".join(ts) + "\n")

col = {"O": (30, 90, 150), "P": (96, 170, 70), "F": (40, 110, 50), "M": (130, 120, 120), "D": (220, 190, 120), "S": (240, 244, 250), "R": (190, 150, 90), "H": (130, 170, 80), "L": (60, 130, 200), "C": (225, 235, 245), "W": (90, 70, 110), "T": (200, 225, 235)}
im = Image.new("RGB", (W*4, H*4))
for y in range(H):
    for x in range(W):
        for dy in range(4):
            for dx in range(4): im.putpixel((x*4+dx, y*4+dy), col[T[y][x]])
from PIL import ImageDraw
d = ImageDraw.Draw(im)
for mid, (x, y, nm) in TOWNS.items(): d.rectangle((x*4-3, y*4-3, x*4+6, y*4+6), outline=(255, 0, 0), width=2)
for i, (x, y) in enumerate(BEACONS): d.ellipse((x*4, y*4, x*4+5, y*4+5), fill=(255, 220, 0))
d.rectangle((FERRY[0]*4, FERRY[1]*4, FERRY[0]*4+5, FERRY[1]*4+5), fill=(0, 0, 0))
im.save("/tmp/claude-0-s/world-preview.png")
print("OK", W, H, "towns", len(TOWNS), "beacons", BEACONS, "ferry", FERRY)
