"""世界地図（大陸アルテシア）の地形を作る。決まった種（seed）から毎回同じ地図ができる。
4つの大陸（西の灯里大陸・北東の霧霜大陸・東の空の浮島群・南東の灯芯大陸）と、海のまんなかの芯環塔（まわりを渦の輪が囲む）、
隠しダンジョンの小島4つ。大陸どうしは海でへだてられ、船（砂音で手に入れる）・飛空艇（浮嶼へ向かう前に手に入れる）で渡る。
出力: src/game/map/world/world-map.generated.ts と、確認用の画像 /tmp/claude-0-s/world-preview.png
地形: O=海 P=平原 F=森 T=雪の森 M=山（通れない） D=砂漠 S=雪原 R=道 H=丘 L=湖・川（通れない） C=雲 W=荒れ地
      V=渦の輪（嵐。通れない） Q=渦の輪の切れ目（航路が開くまでは通れない）"""
import math, heapq, os
import numpy as np
from PIL import Image, ImageDraw

W, H = 252, 189
S = 3.5

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

def fbm(seed, base):
    return (value_noise(W, H, base, seed)*0.40 + value_noise(W, H, base/2, seed+1)*0.22 + value_noise(W, H, 12, seed+2)*0.17
            + value_noise(W, H, 6, seed+3)*0.13 + value_noise(W, H, 3, seed+4)*0.08)

n1 = fbm(11, 12*S); n2 = fbm(23, 9*S); n3 = fbm(37, 7*S)
T = [["O"]*W for _ in range(H)]

def blob(cx, cy, rx, ry, amp, glyph, only=None):
    for y in range(H):
        for x in range(W):
            d = math.hypot((x-cx)/rx, (y-cy)/ry)
            if d + (n1[y, x]-0.5)*amp < 1.0 and (only is None or T[y][x] in only):
                T[y][x] = glyph

# ---- 4つの大陸と小島 ----
blob(60, 108, 52, 44, 1.05, "P")          # A 西の灯里大陸
blob(172, 42, 50, 30, 1.05, "P")          # B 北東の霧霜大陸
blob(182, 148, 46, 36, 1.05, "P")         # D 南東の灯芯大陸
for cx, cy, r in ((226, 90, 8), (239, 100, 6), (229, 106, 6), (216, 99, 5)):   # C 空の浮島群（雲の島）
    for y in range(H):
        for x in range(W):
            if math.hypot(x-cx, (y-cy)*1.1) + (n2[y, x]-0.5)*5 < r: T[y][x] = "C"
ISLETS = [("islet-1", 30, 40, "月影の島"), ("islet-2", 96, 176, "底なしの井戸の島"), ("islet-3", 116, 22, "古灯台の島"), ("islet-4", 243, 62, "忘れられた砦の島"), ("islet-5", 124, 152, "青い穴の洲")]
for _id, cx, cy, nm in ISLETS:
    for y in range(H):
        for x in range(W):
            if math.hypot((x-cx)/5.2, (y-cy)/4.4) + (n2[y, x]-0.5)*0.9 < 1.0 and T[y][x] == "O": T[y][x] = "P"
# 青い穴の洲（海底への入口）は、白い砂の洲にする
for y in range(H):
    for x in range(W):
        if math.hypot((x-124)/5.2, (y-152)/4.4) < 1.15 and T[y][x] == "P": T[y][x] = "D"
# 芯環塔の島（海のまんなか）
TOWER = (125, 95)
for y in range(H):
    for x in range(W):
        if math.hypot(x-TOWER[0], y-TOWER[1]) + (n2[y, x]-0.5)*1.5 < 3.3: T[y][x] = "W"

def land(x, y): return T[y][x] != "O"

# ---- 地形 ----
# A: 山脈（東寄りの分水嶺）、砂漠（南東）、湖（硝子湖）
for y in range(66, 150):
    cx = 94 + math.sin(y*0.15)*3.0
    wid = 2.8 + n2[y, int(cx) % W]*2.4
    for x in range(W):
        if abs(x-cx) < wid and T[y][x] == "P": T[y][x] = "M"
for y in range(H):
    for x in range(W):
        if math.hypot((x-72)/15.0, (y-137)/9.5) + (n3[y, x]-0.5)*0.7 < 1.0 and T[y][x] == "P": T[y][x] = "D"   # 砂音の砂漠
        if math.hypot((x-62)/9.0, (y-90)/6.5) + (n3[y, x]-0.5)*0.7 < 1.0 and T[y][x] in "PH": T[y][x] = "L"      # 硝子湖
# B: 霧断崖（山と丘）、雪原（北）
for y in range(H):
    for x in range(W):
        if math.hypot((x-150)/15.0, (y-42)/10.0) + (n3[y, x]-0.5)*0.9 < 1.0 and T[y][x] == "P":
            T[y][x] = "M" if n1[y, x] > 0.45 else "H"
        if 12 < y < 36 and T[y][x] in "PH" and x > 168 - (n3[y, x]-0.5)*14 and y < 26 + (n1[y, x]-0.5)*10:
            T[y][x] = "S"
        if y < 20 and T[y][x] in "PH" and x > 155:
            T[y][x] = "S"
# D: 荒れ地（虚灯宮）
for y in range(H):
    for x in range(W):
        if math.hypot((x-212)/13.0, (y-150)/15.0) + (n2[y, x]-0.5)*0.6 < 1.0 and T[y][x] != "O": T[y][x] = "W"
# 森・丘・山地・小さな湖（大陸の平原に）
for y in range(H):
    for x in range(W):
        if T[y][x] == "P":
            if n1[y, x] > 0.53 and n3[y, x] > 0.43: T[y][x] = "F"
            elif n2[y, x] > 0.57: T[y][x] = "H"
for y in range(H):
    for x in range(W):
        if T[y][x] == "P" and n2[y, x] > 0.70 and n3[y, x] > 0.5: T[y][x] = "M"
for y in range(1, H-1):
    for x in range(1, W-1):
        if T[y][x] == "P" and any(T[y+dy][x+dx] == "M" for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))) and n1[y, x] > 0.4: T[y][x] = "H"
for y in range(H):
    for x in range(W):
        if T[y][x] == "S" and n1[y, x] > 0.56 and n3[y, x] > 0.42: T[y][x] = "T"
        if T[y][x] in "PFH" and n3[y, x] > 0.80 and n1[y, x] > 0.5: T[y][x] = "L"
def river(x0, y0, x1, y1):
    n = max(abs(x1-x0), abs(y1-y0))*2
    for i in range(n+1):
        t = i/n
        x = int(round(x0+(x1-x0)*t + math.sin(t*9*S/2+x0)*1.6*S/1.5)); y = int(round(y0+(y1-y0)*t))
        if 0 <= x < W and 0 <= y < H and T[y][x] in "PFHDS": T[y][x] = "L"
river(62, 96, 52, 150); river(150, 36, 160, 60); river(176, 120, 170, 160)

# ---- 複雑な地形: 山脈（ノイズの等高線）で大陸を区切る。尾根は細く長く、ところどころで途切れ、峠になる ----
TOWN_PTS0 = [(18, 108), (40, 114), (62, 100), (86, 80), (72, 138), (150, 44), (190, 22), (226, 92), (168, 140), (212, 150)]
def far_from_towns(x, y, d=8): return all(abs(x-a) + abs(y-b) >= d for a, b in TOWN_PTS0)
for y in range(H):
    for x in range(W):
        if T[y][x] in "PFHDST" and far_from_towns(x, y):
            if abs(n2[y, x] - 0.50) < 0.030 and n1[y, x] > 0.38:
                T[y][x] = "M"
            elif abs(n3[y, x] - 0.44) < 0.022 and n2[y, x] > 0.45:
                T[y][x] = "M"
# 山塊の内部は、ごつごつした高峰（N）にする
for y in range(1, H-1):
    for x in range(1, W-1):
        if T[y][x] == "M" and all(T[y+dy][x+dx] in "MN" for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))):
            T[y][x] = "N"
# ---- 水系: 山から海へ、低いほうへ流れる川（枝わかれあり）。海までの距離から、流れる向きを決める ----
from collections import deque
dist = [[9999]*W for _ in range(H)]
dq = deque()
for y in range(H):
    for x in range(W):
        if T[y][x] == "O":
            dist[y][x] = 0; dq.append((x, y))
while dq:
    x, y = dq.popleft()
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        nx, ny = x+dx, y+dy
        if 0 <= nx < W and 0 <= ny < H and dist[ny][nx] > dist[y][x]+1:
            dist[ny][nx] = dist[y][x]+1; dq.append((nx, ny))
rr2 = np.random.default_rng(4242)
starts = [(x, y) for y in range(H) for x in range(W) if T[y][x] in "MN" and 12 < dist[y][x] < 60]
rr2.shuffle(starts)
rivers_made = 0
for (sx0, sy0) in starts:
    if rivers_made >= 14: break
    x, y = sx0, sy0
    path = []
    for _ in range(160):
        cand = [(x+dx, y+dy) for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)) if 0 <= x+dx < W and 0 <= y+dy < H]
        cand.sort(key=lambda c: dist[c[1]][c[0]] + rr2.random()*1.6)
        nx, ny = cand[0]
        if dist[ny][nx] >= dist[y][x] + 1 and rr2.random() < 0.7: nx, ny = cand[1]
        x, y = nx, ny
        path.append((x, y))
        if T[y][x] == "O": break
    else:
        continue
    for (px, py) in path:
        if T[py][px] in "PFHDSTM" and far_from_towns(px, py, 6): T[py][px] = "L"
    rivers_made += 1

TOWNS = {  # マップID: (x, y, 名前)
    "touri-town": (18, 108, "灯里"), "mugikano-village": (40, 114, "麦香野"), "garasuko-town": (62, 100, "硝子湖"),
    "tetsukusari-town": (86, 80, "鉄鏈鉱山"), "sanone-town": (72, 138, "砂音"),
    "kiri-town": (150, 44, "霧断崖"), "shimohara-town": (190, 22, "霜原"),
    "fushima-town": (226, 92, "浮嶼"),
    "toushin-town": (168, 140, "灯芯都"), "kyotoukyu-court": (212, 150, "虚灯宮"),
}
CONTINENT = {"touri-town": "A", "mugikano-village": "A", "garasuko-town": "A", "tetsukusari-town": "A", "sanone-town": "A",
             "kiri-town": "B", "shimohara-town": "B", "fushima-town": "C", "toushin-town": "D", "kyotoukyu-court": "D"}
for mid, (tx, ty, _n) in TOWNS.items():
    base = "C" if mid == "fushima-town" else "W" if mid == "kyotoukyu-court" else "S" if mid == "shimohara-town" else "D" if mid == "sanone-town" else "P"
    for y in range(ty-2, ty+3):
        for x in range(tx-2, tx+3):
            if 0 <= x < W and 0 <= y < H and (abs(x-tx)+abs(y-ty) <= 3) and not (mid != "fushima-town" and T[y][x] == "O" and False):
                if T[y][x] in "OLMNF" or mid in ("fushima-town",): T[y][x] = base

COST = {"X": 99999, "N": 13.0, "T": 2.2, "P": 1.0, "F": 2.2, "D": 1.4, "S": 1.8, "H": 2.0, "M": 9.0, "R": 0.4, "W": 1.2, "C": 1.0, "L": 6.0, "O": 99999, "V": 99999, "Q": 99999, "A": 1.3, "Z": 99999}
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
def carve_road(a, b):
    for (x, y) in astar(a, b):
        if T[y][x] not in "CW": T[y][x] = "R"
def pos(mid): return TOWNS[mid][:2]
for a, b in (("touri-town", "mugikano-village"), ("mugikano-village", "garasuko-town"), ("garasuko-town", "tetsukusari-town"),
             ("tetsukusari-town", "sanone-town"), ("kiri-town", "shimohara-town"), ("toushin-town", "kyotoukyu-court")):
    carve_road(pos(a), pos(b))
# ---- 深い谷（通れない裂け目 X）: 険しい土地に、短い谷。道と町のまわりには作らない ----
road_pts = [(x, y) for y in range(H) for x in range(W) if T[y][x] == "R"]
road_set = set(road_pts)
def near_road(x, y, d=4): return any((x+dx, y+dy) in road_set for dx in range(-d, d+1) for dy in range(-d, d+1))
for y in range(H):
    for x in range(W):
        if T[y][x] in "PFHD" and abs(n3[y, x] - 0.60) < 0.012 and n1[y, x] > 0.46 and far_from_towns(x, y, 10) and not near_road(x, y) and not any(abs(x-cx) < 8 and abs(y-cy) < 7 for _i, cx, cy, _n in ISLETS):
            T[y][x] = "X"

# ---- 火山（灯芯大陸の南東）: 火口の溶岩Z → 山の本体N（通れない）→ 灰の大地A。溶岩の川が三すじ流れ出る。入口は山の南のふもと ----
vbest = None
for vy0 in range(120, 178):
    for vx0 in range(150, 224):
        if not all(0 <= vy0+dy < H and 0 <= vx0+dx < W and T[vy0+dy][vx0+dx] not in "OL" for dx in range(-11, 12, 2) for dy in range(-11, 12, 2)): continue
        if min(math.hypot(vx0-a, vy0-b) for a, b, _n in TOWNS.values()) < 26: continue
        sc = math.hypot(vx0-208, vy0-170)
        if vbest is None or sc < vbest[0]: vbest = (sc, vx0, vy0)
assert vbest, "火山を置けない"
VOLCANO = (vbest[1], vbest[2])
vx, vy = VOLCANO
streams = [math.radians(a) for a in (200, 330, 20)]
for y in range(max(0, vy-14), min(H, vy+15)):
    for x in range(max(0, vx-14), min(W, vx+15)):
        d = math.hypot(x-vx, y-vy) + (n2[y, x]-0.5)*2.4
        if T[y][x] == "O": continue
        if d < 2.7: T[y][x] = "Z"
        elif d < 5.6: T[y][x] = "N"
        elif d < 12.5:
            T[y][x] = "A" if (n1[y, x] > 0.30 or d < 9) else T[y][x]
            if d > 9.5 and n3[y, x] > 0.62: T[y][x] = "M"
for ang in streams:
    for k in range(5, 13):
        x = int(round(vx + math.cos(ang)*k + math.sin(k*0.9)*0.8)); y = int(round(vy + math.sin(ang)*k + math.cos(k*0.7)*0.8))
        if 0 <= x < W and 0 <= y < H and T[y][x] not in "O": T[y][x] = "Z"
# 入口（山の南のふもとの灰の道）。入口の周りは通れる地面にそろえる
for yy in range(vy+5, vy+9):
    for xx in range(vx-2, vx+3):
        if T[yy][xx] not in "O": T[yy][xx] = "A"
VOLCANO_ENTRY = (vx, vy+6)
carve_road((vx, vy+9), pos("kyotoukyu-court"))
ISLETS.append(("islet-6", VOLCANO_ENTRY[0], VOLCANO_ENTRY[1], "火口の迷宮"))

# ---- 小さな町・村（8か所）: 各大陸の、広い平地に。いちばん近い町へ道をつなぐ ----
VILLAGE_DEFS = [  # (マップID, 名前, 大陸, 範囲(x0,y0,x1,y1), 地形, アイコン)
    ("village-namioto", "波音の浜", "A", (12, 85, 40, 135), "P", "port"),
    ("village-kazami", "風見の丘", "A", (36, 70, 62, 92), "P", "village"),
    ("village-tomoshimori", "灯守りの宿場", "A", (55, 100, 88, 125), "P", "village"),
    ("village-samori", "砂守のいずみ", "A", (60, 128, 90, 150), "D", "tents"),
    ("village-kirima", "霧間の集落", "B", (125, 25, 165, 60), "P", "village"),
    ("village-yukimachi", "雪待ちの小屋町", "B", (168, 14, 215, 34), "S", "snowtown"),
    ("village-minori", "実り野", "D", (140, 120, 190, 175), "P", "village"),
    ("village-arano", "荒野の市", "D", (190, 118, 228, 175), "P", "tents"),
]
VILLAGES = []
vr = np.random.default_rng(31415)
main_pts = [(v[0], v[1]) for v in TOWNS.values()]
def flat_ok(x, y, ground):
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            if not (0 <= x+dx < W and 0 <= y+dy < H) or T[y+dy][x+dx] not in ground + "R": return False
    return True
for vid, nm, cont, (x0, y0, x1, y1), ground, icon in VILLAGE_DEFS:
    spot = None
    for _ in range(6000):
        x = int(vr.integers(x0, x1)); y = int(vr.integers(y0, y1))
        if not flat_ok(x, y, "PFHD" if ground != "S" else "SPT"): continue
        if any(abs(x-a) + abs(y-b) < 20 for a, b in main_pts + [(v[1], v[2]) for v in VILLAGES]): continue
        spot = (x, y); break
    assert spot, f"{nm} を置けない"
    x, y = spot
    for yy in range(y-2, y+3):
        for xx in range(x-2, x+3):
            if T[yy][xx] in "FHLMNX": T[yy][xx] = "D" if ground == "D" else "S" if ground == "S" else "P"
    # いちばん近い町（同じ大陸）へ道
    same = [k for k, c in CONTINENT.items() if c == cont]
    near = min(same, key=lambda k: abs(TOWNS[k][0]-x) + abs(TOWNS[k][1]-y))
    carve_road((x, y+1), (TOWNS[near][0], TOWNS[near][1]))
    VILLAGES.append((vid, x, y, nm, cont, icon))

# 小島の入口（島の中心）、塔の入口（塔の島の中心）は、道のタイルにする
for _id, cx, cy, nm in ISLETS:
    for dy in (0, 1):
        T[cy+dy][cx] = "R"
for dy in (0, 1): T[TOWER[1]+dy][TOWER[0]] = "R"

# ---- 塔を覆う地形（海のまんなか）: 内側から、塔の島 → 静かな内海 → 岩礁の外輪（岩の山。南だけ切れ目） → 渦の輪（嵐。南に切れ目 Q） ----
CHANNEL = []
for y in range(H):
    for x in range(W):
        d = math.hypot(x-TOWER[0], y-TOWER[1])
        if T[y][x] != "O":
            continue
        ang = math.degrees(math.atan2(y-TOWER[1], x-TOWER[0]))
        south = 70 <= ang <= 110
        # 岩礁の外輪（半径5.2〜7.6）。ぎざぎざにゆらがせる。南は、船の通り道があく
        if 5.2 <= d + (n2[y, x]-0.5)*2.2 <= 7.6 and not south:
            T[y][x] = "M"
        elif 8.6 <= d <= 12.6:
            if south:
                T[y][x] = "Q"; CHANNEL.append((x, y))
            else:
                T[y][x] = "V"

# ---- 検査 ----
LANDWALK = "PFDSRHCWTA"   # M N X L V Q は通れない
def flood(sx, sy, walk):
    seen = {(sx, sy)}; st = [(sx, sy)]
    while st:
        x, y = st.pop()
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x+dx, y+dy
            if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in seen and walk(nx, ny):
                seen.add((nx, ny)); st.append((nx, ny))
    return seen
landwalk = lambda x, y: T[y][x] in LANDWALK
for cont, first in (("A", "touri-town"), ("B", "kiri-town"), ("C", "fushima-town"), ("D", "toushin-town")):
    seen = flood(*pos(first), landwalk)
    for mid, (x, y, nm) in TOWNS.items():
        if CONTINENT[mid] == cont:
            assert (x, y) in seen, f"{nm} に歩いて行けない"
            assert (x, y+1) in seen, f"{nm} の入口の下が歩けない"
# 小島の入口の下が歩ける
for _id, cx, cy, nm in ISLETS:
    assert T[cy+1][cx] in LANDWALK, f"{nm} の入口の下が歩けない"
assert T[TOWER[1]+1][TOWER[0]] in LANDWALK

# ---- 環灯台（8神の欠片をささげる灯台）: 各地方の町のそばの、道ではない通れるマス ----
BEACON_TOWNS = ["mugikano-village", "garasuko-town", "tetsukusari-town", "sanone-town", "kiri-town", "shimohara-town", "fushima-town", "toushin-town"]
OFFS = sorted([(dx, dy) for dx in range(-8, 9) for dy in range(-8, 9) if 3 <= max(abs(dx), abs(dy)) <= 8], key=lambda o: (max(abs(o[0]), abs(o[1])), abs(o[0]) + abs(o[1])))
BEACONS = []
used = set()
for mid in BEACON_TOWNS:
    tx, ty, _ = TOWNS[mid]
    seen = flood(tx, ty, landwalk)
    for dx, dy in OFFS:
        x, y = tx+dx, ty+dy
        if 0 <= x < W and 0 <= y < H and T[y][x] in "PFDSHCWT" and (x, y) in seen and (x, y) not in used and all((x+ax, y+ay) not in used for ax, ay in ((1,0),(-1,0),(0,1),(0,-1))):
            BEACONS.append((x, y)); used.add((x, y)); break
    else:
        raise SystemExit(f"{mid} の環灯台を置けない")
assert len(BEACONS) == 8

# ---- 飾りの名所（入れない目印。遺跡・祠・洞窟の入口・立石・大樹）: 大陸のあちこちに ----
LANDMARKS = []
def near_any(x, y, pts, d): return any(abs(x-a) + abs(y-b) < d for a, b in pts)
town_pts = [(v[0], v[1]) for v in TOWNS.values()]
taken = list(town_pts) + [(v[1], v[2]) for v in VILLAGES] + BEACONS + [(cx, cy) for _i, cx, cy, _n in ISLETS] + [TOWER]
rr = np.random.default_rng(777)
spec = [("ruin", "PDWH", 7), ("shrine", "PH", 6), ("cave", "PFDH", 6), ("stones", "H", 6), ("bigtree", "F", 7)]
for kind, ground, count in spec:
    placed = 0
    tries = 0
    while placed < count and tries < 4000:
        tries += 1
        x = int(rr.integers(4, W-4)); y = int(rr.integers(4, H-4))
        if T[y][x] not in ground or near_any(x, y, taken, 12): continue
        if T[y+1][x] not in LANDWALK or T[y-1][x] not in LANDWALK: continue
        if kind == "cave" and not any(T[y+dy][x+dx] == "M" for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))): continue
        LANDMARKS.append((kind, x, y)); taken.append((x, y)); placed += 1

# ---- 船の停泊場所: 砂音のいちばん近い海岸（陸の海に接するマス）と、そのとなりの海 ----
sx, sy = pos("sanone-town")
best = None
for y in range(H):
    for x in range(W):
        if T[y][x] in "PFDHW" and any(T[y+dy][x+dx] == "O" for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)) if 0 <= y+dy < H and 0 <= x+dx < W) and (x, y) in flood(sx, sy, landwalk) if abs(x-sx) < 40 and abs(y-sy) < 40 else False:
            d = math.hypot(x-sx, y-sy)
            if best is None or d < best[0]: best = (d, x, y)
assert best, "船の停泊場所を置けない"
SHIP_DOCK = (best[1], best[2])
# 船の置き場所（海のマス）
SHIP_SEA = None
for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
    if T[SHIP_DOCK[1]+dy][SHIP_DOCK[0]+dx] == "O": SHIP_SEA = (SHIP_DOCK[0]+dx, SHIP_DOCK[1]+dy); break
assert SHIP_SEA

# ---- 飛空艇の置き場所: 霜原のそばの平地 ----
tx, ty, _ = TOWNS["shimohara-town"]
AIRSHIP = None
seen = flood(tx, ty, landwalk)
for r in range(5, 14):
    for dx in range(-r, r+1):
        for dy in range(-r, r+1):
            x, y = tx+dx, ty+dy
            if max(abs(dx), abs(dy)) == r and 0 <= x < W and 0 <= y < H and T[y][x] in "PS" and (x, y) in seen and AIRSHIP is None:
                AIRSHIP = (x, y)
assert AIRSHIP

rows = ["".join(r) for r in T]
ts = ["// 自動生成: tools/world-map/gen_world.py（手で編集しない）。大陸アルテシアの地形。1文字=1マス。",
      "// O=海 P=平原 F=森 T=雪の森 M=山 D=砂漠 S=雪原 R=道 H=丘 L=湖・川 C=雲 W=荒れ地 A=灰の大地（火山） Z=溶岩 V=渦の輪 Q=渦の輪の切れ目",
      f"export const WORLD_WIDTH = {W};", f"export const WORLD_HEIGHT = {H};",
      "export const WORLD_ROWS: string[] = [", *[f'  "{r}",' for r in rows], "];",
      "export const WORLD_TOWNS: Record<string, { x: number; y: number; name: string; continent: string }> = {",
      *[f'  "{k}": {{ x: {v[0]}, y: {v[1]}, name: "{v[2]}", continent: "{CONTINENT[k]}" }},' for k, v in TOWNS.items()], "};",
      "/** 環灯台（8神の欠片をささげる灯台）。番号は神の番号（1=女神…8=冥神）。 */",
      "export const WORLD_BEACONS: Array<{ x: number; y: number }> = [", *[f"  {{ x: {x}, y: {y} }}," for x, y in BEACONS], "];",
      "export const WORLD_VILLAGES: Array<{ id: string; x: number; y: number; name: string; continent: string; icon: string }> = [", *[f'  {{ id: "{i}", x: {x}, y: {y}, name: "{n}", continent: "{c}", icon: "{ic}" }},' for i, x, y, n, c, ic in VILLAGES], "];",
      "/** 飾りの名所（入れない目印）。 */",
      "export const WORLD_LANDMARKS: Array<{ kind: string; x: number; y: number }> = [", *[f'  {{ kind: "{k}", x: {x}, y: {y} }},' for k, x, y in LANDMARKS], "];",
      "/** 隠しダンジョンの小島（入口は島の中心のマス）。 */",
      "export const WORLD_ISLETS: Array<{ id: string; x: number; y: number; name: string }> = [", *[f'  {{ id: "{i}", x: {x}, y: {y}, name: "{n}" }},' for i, x, y, n in ISLETS], "];",
      f"export const WORLD_TOWER = {{ x: {TOWER[0]}, y: {TOWER[1]} }};",
      "/** 渦の輪の切れ目（航路が開くと、ここが海になって通れる）。 */",
      "export const WORLD_CHANNEL: Array<[number, number]> = [" + ", ".join(f"[{x}, {y}]" for x, y in CHANNEL) + "];",
      f"export const WORLD_SHIP_DOCK = {{ x: {SHIP_DOCK[0]}, y: {SHIP_DOCK[1]} }};",
      f"export const WORLD_SHIP_START = {{ x: {SHIP_SEA[0]}, y: {SHIP_SEA[1]} }};",
      f"export const WORLD_AIRSHIP_START = {{ x: {AIRSHIP[0]}, y: {AIRSHIP[1]} }};"]
os.makedirs("/home/user/sunshine-rpg/src/game/map/world", exist_ok=True)
open("/home/user/sunshine-rpg/src/game/map/world/world-map.generated.ts", "w").write("\n".join(ts) + "\n")

col = {"O": (30, 90, 150), "P": (96, 170, 70), "F": (40, 110, 50), "M": (130, 120, 120), "D": (220, 190, 120), "S": (240, 244, 250), "R": (190, 150, 90), "H": (130, 170, 80), "L": (60, 130, 200), "C": (225, 235, 245), "W": (90, 70, 110), "T": (200, 225, 235), "V": (20, 50, 110), "Q": (40, 70, 130), "N": (92, 84, 92), "X": (50, 36, 56), "A": (74, 66, 68), "Z": (230, 90, 30)}
im = Image.new("RGB", (W*4, H*4))
for y in range(H):
    for x in range(W):
        for dy in range(4):
            for dx in range(4): im.putpixel((x*4+dx, y*4+dy), col[T[y][x]])
d = ImageDraw.Draw(im)
for mid, (x, y, nm) in TOWNS.items(): d.rectangle((x*4-3, y*4-3, x*4+6, y*4+6), outline=(255, 0, 0), width=2)
for _v in VILLAGES: d.rectangle((_v[1]*4-2, _v[2]*4-2, _v[1]*4+5, _v[2]*4+5), outline=(255, 160, 0), width=1)
for i, (x, y) in enumerate(BEACONS): d.ellipse((x*4, y*4, x*4+5, y*4+5), fill=(255, 220, 0))
for _id, cx, cy, nm in ISLETS: d.rectangle((cx*4-3, cy*4-3, cx*4+6, cy*4+6), outline=(255, 0, 255), width=2)
d.rectangle((TOWER[0]*4-3, TOWER[1]*4-3, TOWER[0]*4+6, TOWER[1]*4+6), outline=(255, 255, 0), width=2)
d.rectangle((SHIP_DOCK[0]*4, SHIP_DOCK[1]*4, SHIP_DOCK[0]*4+5, SHIP_DOCK[1]*4+5), fill=(0, 0, 0))
d.rectangle((AIRSHIP[0]*4, AIRSHIP[1]*4, AIRSHIP[0]*4+5, AIRSHIP[1]*4+5), fill=(255, 128, 0))
im.save("/tmp/claude-0-s/world-preview.png")
print("OK", W, H, "ship", SHIP_DOCK, SHIP_SEA, "airship", AIRSHIP)
