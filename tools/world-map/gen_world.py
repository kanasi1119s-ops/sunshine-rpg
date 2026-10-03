"""世界地図（大陸アルテシア）の地形を作る。決まった種（seed）から毎回同じ地図ができる。
出力: src/game/map/world/world-map.generated.ts（地形を1行1文字の文字列で）と、確認用の画像 /tmp/claude-0-s/world-preview.png
地形: O=海 P=平原 F=森 M=山（通れない） D=砂漠 S=雪原 R=道 H=丘 L=湖・川（通れない） C=雲の橋・浮島の雲 W=荒れ地（虚灯宮のまわり）
町・環灯台・渡し場の位置は、ここで決めて TypeScript に書き出す。"""
import math, heapq, sys
import numpy as np
from PIL import Image

W, H = 72, 54
rng = np.random.default_rng(20261003)

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
    return value_noise(w, h, base, seed)*0.55 + value_noise(w, h, base/2, seed+1)*0.3 + value_noise(w, h, base/4, seed+2)*0.15

n1 = fbm(W, H, 11); n2 = fbm(W, H, 23, 9); n3 = fbm(W, H, 37, 7)
T = [["O"]*W for _ in range(H)]

# 大陸の陸地: 東西に長いだ円を、ノイズでぎざぎざに
for y in range(H):
    for x in range(W):
        d = math.hypot((x-36)/32.0, (y-27)/21.0)
        if d + (n1[y, x]-0.5)*0.75 < 0.98:
            T[y][x] = "P"
# 北東の浮島（浮嶼）
for cx, cy, r in ((64, 20, 3.6), (68, 25, 3.0), (62, 26, 2.6)):
    for y in range(H):
        for x in range(W):
            if math.hypot(x-cx, (y-cy)*1.1) + (n2[y, x]-0.5)*3 < r:
                T[y][x] = "C"
# 虚灯宮の半島（東の海岸）
for y in range(H):
    for x in range(W):
        if math.hypot((x-67)/5.0, (y-37)/6.0) + (n2[y, x]-0.5)*0.6 < 1.0:
            T[y][x] = "W"

def land(x, y): return T[y][x] not in "O"

# 山脈（分水嶺）: x=29〜33の南北の帯。北の端から南の端まで、ノイズで幅を変える
for y in range(5, 46):
    cx = 30 + math.sin(y*0.22)*2.5
    wid = 2.2 + n2[y, int(cx)%W]*2.2
    for x in range(W):
        if abs(x-cx) < wid and T[y][x] == "P":
            T[y][x] = "M"
# 霧断崖のあたり（北東の断崖）
for y in range(H):
    for x in range(W):
        if math.hypot((x-53)/5.5, (y-18)/5.0) + (n3[y, x]-0.5)*0.9 < 1.0 and T[y][x] == "P":
            T[y][x] = "M" if n1[y, x] > 0.45 else "H"
# 雪原（北）
for y in range(H):
    for x in range(W):
        if y <= 13 and T[y][x] in "PH" and x > 40:
            T[y][x] = "S"
        if y <= 10 and T[y][x] == "M":
            T[y][x] = "M"
# 砂漠（中南東）
for y in range(H):
    for x in range(W):
        if math.hypot((x-46)/9.0, (y-36)/6.5) + (n3[y, x]-0.5)*0.7 < 1.0 and T[y][x] == "P":
            T[y][x] = "D"
# 森（ノイズの高いところ）と丘
for y in range(H):
    for x in range(W):
        if T[y][x] == "P":
            if n1[y, x] > 0.60 and n3[y, x] > 0.45: T[y][x] = "F"
            elif n2[y, x] > 0.66: T[y][x] = "H"
# 湖（硝子湖）と川
for y in range(H):
    for x in range(W):
        if math.hypot((x-22)/5.2, (y-22)/3.8) + (n3[y, x]-0.5)*0.7 < 1.0 and land(x, y):
            T[y][x] = "L"
def river(x0, y0, x1, y1):
    n = max(abs(x1-x0), abs(y1-y0))*2
    for i in range(n+1):
        t = i/n
        x = int(round(x0+(x1-x0)*t + math.sin(t*9+x0)*1.6)); y = int(round(y0+(y1-y0)*t))
        if 0 <= x < W and 0 <= y < H and T[y][x] in "PFHDS": T[y][x] = "L"
river(22, 25, 20, 40); river(38, 8, 41, 22); river(44, 24, 47, 30)

TOWNS = {  # マップID: (x, y, 名前)
    "touri-town": (7, 30, "灯里"), "mugikano-village": (15, 31, "麦香野"), "garasuko-town": (22, 27, "硝子湖"),
    "tetsukusari-town": (31, 17, "鉄鏈鉱山"), "toushin-town": (38, 25, "灯芯都"), "sanone-town": (45, 35, "砂音"),
    "kiri-town": (52, 21, "霧断崖"), "shimohara-town": (58, 10, "霜原"), "fushima-town": (64, 21, "浮嶼"), "kyotoukyu-court": (67, 37, "虚灯宮"),
}
# 町のまわり（半径2）は、通れる地面にならす
for mid, (tx, ty, _n) in TOWNS.items():
    base = "C" if mid == "fushima-town" else "W" if mid == "kyotoukyu-court" else "S" if mid == "shimohara-town" else "D" if mid == "sanone-town" else "P"
    for y in range(ty-2, ty+3):
        for x in range(tx-2, tx+3):
            if 0 <= x < W and 0 <= y < H and (abs(x-tx)+abs(y-ty) <= 3):
                T[y][x] = base if T[y][x] in "OLMF" or mid in ("fushima-town",) else T[y][x]

COST = {"P": 1.0, "F": 2.2, "D": 1.4, "S": 1.8, "H": 2.0, "M": 9.0, "R": 0.4, "W": 1.2, "C": 1.0, "L": 99999, "O": 99999}
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
        if T[y][x] not in "CW": T[y][x] = "R"

def pos(mid): return TOWNS[mid][:2]
# 川をわたる橋のために、川も通れる道を許す: 道を引くときだけ川（L）に高いが有限の費用を付けて通す
COST["L"] = 6.0
for a, b in (("touri-town", "mugikano-village"), ("mugikano-village", "garasuko-town"), ("garasuko-town", "tetsukusari-town"),
             ("garasuko-town", "toushin-town"), ("toushin-town", "sanone-town"), ("toushin-town", "kiri-town"),
             ("kiri-town", "shimohara-town"), ("sanone-town", "kyotoukyu-court"), ("kiri-town", "fushima-town")):
    carve_road(pos(a), pos(b))
COST["L"] = 99999
# 浮嶼への雲の橋: 霧断崖から浮島へ、雲のタイルでつなぐ
x0, y0 = pos("kiri-town"); x1, y1 = pos("fushima-town")
n = max(abs(x1-x0), abs(y1-y0))*2
for i in range(n+1):
    t = i/n
    x = int(round(x0+(x1-x0)*t)); y = int(round(y0+(y1-y0)*t + math.sin(t*5)*1.2))
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
            if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in seen and T[ny][nx] in "PFDSRHCW":
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
        if 0 <= x < W and 0 <= y < H and T[y][x] in "PFDSHCW" and (x, y) in seen and (x, y) not in used and all((x+ax, y+ay) not in used for ax, ay in ((1,0),(-1,0),(0,1),(0,-1))):
            BEACONS.append((x, y)); used.add((x, y)); break
    else:
        raise SystemExit(f"{mid} の環灯台を置けない")
assert len(BEACONS) == 8

# 渡し場（虚灯宮の南の海岸）: 海に接する通れるマス
FERRY = None
for y in range(44, 30, -1):
    for x in range(60, 71):
        if T[y][x] in "PFDHW" and (x, y) in seen and any(0 <= y+dy < H and 0 <= x+dx < W and T[y+dy][x+dx] == "O" for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))) and abs(x-67)+abs(y-37) > 3:
            FERRY = (x, y); break
    if FERRY: break
assert FERRY, "渡し場を置けない"
# 渦（大渦）: 南東の沖
VORTEX = (66, 49)

rows = ["".join(r) for r in T]
ts = ["// 自動生成: tools/world-map/gen_world.py（手で編集しない）。大陸アルテシアの地形。1文字=1マス。",
      "// O=海 P=平原 F=森 M=山 D=砂漠 S=雪原 R=道 H=丘 L=湖・川 C=雲 W=荒れ地",
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

col = {"O": (30, 90, 150), "P": (96, 170, 70), "F": (40, 110, 50), "M": (130, 120, 120), "D": (220, 190, 120), "S": (240, 244, 250), "R": (190, 150, 90), "H": (130, 170, 80), "L": (60, 130, 200), "C": (225, 235, 245), "W": (90, 70, 110)}
im = Image.new("RGB", (W*8, H*8))
for y in range(H):
    for x in range(W):
        for dy in range(8):
            for dx in range(8): im.putpixel((x*8+dx, y*8+dy), col[T[y][x]])
from PIL import ImageDraw
d = ImageDraw.Draw(im)
for mid, (x, y, nm) in TOWNS.items(): d.rectangle((x*8-2, y*8-2, x*8+9, y*8+9), outline=(255, 0, 0), width=2)
for i, (x, y) in enumerate(BEACONS): d.ellipse((x*8, y*8, x*8+8, y*8+8), fill=(255, 220, 0))
d.rectangle((FERRY[0]*8, FERRY[1]*8, FERRY[0]*8+8, FERRY[1]*8+8), fill=(0, 0, 0))
im.save("/tmp/claude-0-s/world-preview.png")
print("OK", W, H, "towns", len(TOWNS), "beacons", BEACONS, "ferry", FERRY)
