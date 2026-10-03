"""世界地図の町・遺跡のアイコン（48×48枠に下そろえ、おおよそ32×28）を一から作る。光は左上、ハイライトなし。
使い方: python3 worldicons.py → icon-*.txt と pal-icon-*.json"""
import json, math
W = H = 48
def blank(): return [["."]*W for _ in range(H)]
def rect(g, x0, y0, x1, y1, c):
    for y in range(y0, y1+1):
        for x in range(x0, x1+1):
            if 0 <= x < W and 0 <= y < H: g[y][x] = c
def tri(g, cx, ytop, ybase, half, cl, cr, ridge=None):
    for y in range(ytop, ybase+1):
        w = half*(y-ytop)/max(1, ybase-ytop)
        for x in range(int(round(cx-w)), int(round(cx+w))+1):
            if 0 <= x < W and 0 <= y < H: g[y][x] = cl if x < cx else cr
def outline(g, c="A"):
    res = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] != ".": continue
            if any(0 <= y+dy < H and 0 <= x+dx < W and g[y+dy][x+dx] != "." for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))): res[y][x] = c
    return res
def mound(g, cx, cy, rx, ry, cg="G", cs="g"):
    for y in range(cy-ry, cy+ry+1):
        for x in range(cx-rx, cx+rx+1):
            if ((x-cx)/rx)**2 + ((y-cy)/ry)**2 <= 1 and g[y][x] == ".": g[y][x] = cg if (x-cx)+(y-cy) < 3 else cs
def house(g, x, y, w, h, roof=("R","r"), wall=("W","w"), door=True):
    """x,yは左下。壁と切妻の屋根。左が地、右が影。"""
    top = y-h
    for yy in range(top, y+1):
        for xx in range(x, x+w):
            g[yy][xx] = wall[0] if xx < x+w*0.62 else wall[1]
    rh = max(3, w//2)
    for k in range(rh):
        for xx in range(x-1+k, x+w+1-k):
            if 0 <= top-k+1 < H: g[top-k+1][xx] = roof[0] if xx < x+w/2 else roof[1]
    if door:
        rect(g, x+w//2-1, y-3, x+w//2, y, "K")
        if w >= 8: rect(g, x+1, top+2, x+2, top+3, "B")

PAL = {"A": "#1c1410", "W": "#e8dcc0", "w": "#b8a888", "R": "#c0553c", "r": "#8a3a2c", "K": "#4a2c18", "B": "#7ab0d8", "G": "#5a9a40", "g": "#3a7032", "T": "#8a8f9c", "t": "#686d7a", "N": "#a89070", "n": "#7a6850",
       "S": "#f4f6fa", "s": "#c8d0e0", "Y": "#e8c040", "P": "#6a4a8a", "p": "#4a2e66", "D": "#d8c080", "d": "#b09858", "L": "#3a6a9a", "l": "#2a4a78", "O": "#e86a20", "Q": "#5a5060", "q": "#3a3040", "C": "#f0f6fc", "c": "#c0d4e8", "E": "#6a8a3a", "e": "#4a6a28", "M": "#7a5230", "m": "#5a3a20", "F": "#e0e8f0", "X": "#00000000"}

def icon_port():
    g = blank(); mound(g, 24, 42, 15, 4)
    house(g, 10, 40, 8, 7); house(g, 20, 41, 9, 9, roof=("R","r")); house(g, 31, 40, 7, 6, roof=("L","l"))
    # 帆かけ船
    rect(g, 36, 25, 36, 37, "M"); 
    for k in range(10):
        for x in range(37, 37+max(1, 9-k)): g[26+k][x] = "C" if x < 41 else "c"
    rect(g, 31, 38, 42, 39, "m"); rect(g, 32, 39, 41, 40, "M")
    return g
def icon_village():
    g = blank(); mound(g, 24, 42, 15, 4)
    house(g, 9, 40, 8, 6, roof=("D","d")); house(g, 19, 41, 8, 7, roof=("D","d")); house(g, 29, 40, 7, 6, roof=("D","d"))
    # 風車
    rect(g, 38, 28, 41, 40, "N"); rect(g, 41, 28, 41, 40, "n"); tri(g, 39, 22, 28, 4, "n", "m")
    for (dx, dy) in ((-6, -6), (6, -6), (-6, 6), (6, 6)):
        for k in range(7): 
            x = 40+int(dx*k/6); y = 29+int(dy*k/6)
            g[y][x] = "m"; g[y][x+1] = "M"
    return g
def icon_lake():
    g = blank()
    for y in range(40, 47):
        for x in range(6, 42): g[y][x] = "L" if (x+y) % 5 else "l"
    house(g, 9, 39, 8, 7, roof=("L","l")); house(g, 19, 40, 9, 9, roof=("L","l")); house(g, 30, 39, 7, 6, roof=("L","l"))
    for x in (10, 14, 21, 26, 32, 35): rect(g, x, 40, x, 44, "m")
    return g
def icon_mine():
    g = blank(); tri(g, 24, 14, 42, 17, "T", "t")
    for y in range(18, 42):
        for x in range(8, 41):
            if g[y][x] != "." and (x*5+y*3) % 11 == 0: g[y][x] = "N" if x < 24 else "n"
    for y in range(30, 42):
        for x in range(19, 29):
            if abs(x-23.5) < 5 - (42-y)*0.0 and g[y][x] != ".": g[y][x] = "A" if y > 31 else "q"
    rect(g, 18, 29, 19, 41, "M"); rect(g, 28, 29, 29, 41, "M"); rect(g, 18, 29, 29, 30, "M")
    rect(g, 31, 38, 36, 40, "Q"); rect(g, 31, 38, 36, 38, "T"); rect(g, 32, 41, 33, 41, "A"); rect(g, 35, 41, 36, 41, "A")
    g[24][22] = "Y"; g[24][23] = "Y"; g[27][27] = "Y"
    return g
def icon_castle():
    g = blank(); mound(g, 24, 42, 16, 4)
    rect(g, 12, 24, 36, 41, "T"); rect(g, 30, 24, 36, 41, "t")
    for x in range(12, 37, 4): rect(g, x, 21, x+1, 24, "T") if x < 30 else rect(g, x, 21, x+1, 24, "t")
    for (cx) in (10, 38):
        rect(g, cx-3, 14, cx+3, 41, "T" if cx < 20 else "t"); tri(g, cx, 6, 14, 5, "R", "r")
    rect(g, 22, 10, 26, 24, "T"); tri(g, 24, 3, 10, 4, "R", "r")
    g[1][24] = "Y"; rect(g, 24, 1, 24, 3, "K")
    rect(g, 21, 32, 27, 41, "A"); rect(g, 22, 31, 26, 31, "A")
    for (x, y) in ((16, 28), (32, 28), (9, 20), (37, 20)): rect(g, x, y, x+1, y+2, "B")
    return g
def icon_tents():
    g = blank()
    for y in range(40, 46):
        for x in range(4, 44): g[y][x] = "D" if (x+y*2) % 7 else "d"
    for (cx, base, h, c1, c2) in ((14, 42, 12, "R", "r"), (27, 43, 15, "W", "w"), (37, 41, 10, "R", "r")):
        tri(g, cx, base-h, base, h*0.75, c1, c2)
        rect(g, cx-1, base-4, cx, base, "K")
    # ヤシ
    rect(g, 6, 28, 7, 41, "M")
    for (dx, dy) in ((-5, 1), (5, 1), (-3, -3), (3, -3), (0, -4)):
        for k in range(5): g[27+int(dy*k/4)+k//3][7+int(dx*k/4)] = "E"
    return g
def icon_temple():
    g = blank(); tri(g, 24, 10, 42, 20, "T", "t")
    for y in range(14, 42):
        for x in range(4, 45):
            if g[y][x] != "." and (x*3+y*7) % 9 == 0: g[y][x] = "t" if x > 24 else "N"
    rect(g, 17, 24, 30, 35, "W"); rect(g, 26, 24, 30, 35, "w"); tri(g, 23, 15, 24, 8, "C", "c")
    rect(g, 22, 29, 24, 35, "K"); rect(g, 19, 27, 20, 28, "B"); rect(g, 27, 27, 28, 28, "B")
    rect(g, 23, 6, 23, 14, "K"); rect(g, 21, 8, 25, 8, "K"); 
    return g
def icon_snowtown():
    g = blank(); mound(g, 24, 42, 16, 4, "S", "s")
    house(g, 9, 40, 8, 7, roof=("S","s"), wall=("N","n")); house(g, 19, 41, 9, 9, roof=("S","s"), wall=("N","n")); house(g, 30, 40, 7, 6, roof=("S","s"), wall=("N","n"))
    for (cx, cy) in ((6, 36), (40, 35)): tri(g, cx, cy-10, cy, 4, "e", "E"); tri(g, cx, cy-10, cy-6, 3, "S", "s")
    return g
def icon_sky():
    g = blank()
    # 浮島: 上は草と家、下は逆三角の岩
    for y in range(34, 46):
        w = 17 - (y-34)*1.35
        for x in range(int(24-w), int(24+w)+1):
            if x >= 0: g[y][x] = "N" if x < 24 else "n"
    rect(g, 7, 32, 41, 35, "G"); rect(g, 7, 35, 41, 35, "g")
    house(g, 13, 32, 8, 7, roof=("P","p")); house(g, 25, 32, 9, 9, roof=("P","p"))
    for (x, y, w) in ((4, 44, 8), (36, 44, 8), (14, 18, 8), (30, 12, 6)):
        for xx in range(x, x+w): g[y][xx] = "C"; g[y-1][xx+1 if xx+1 < W else xx] = "C"
    return g
def icon_palace():
    g = blank(); mound(g, 24, 42, 16, 4, "p", "q")
    rect(g, 14, 22, 34, 41, "P"); rect(g, 28, 22, 34, 41, "p")
    for (cx, h) in ((10, 26), (38, 26), (24, 32)):
        rect(g, cx-3, 41-h, cx+3, 41, "P" if cx < 24 else "p"); tri(g, cx, 41-h-8, 41-h, 5, "q", "A")
    rect(g, 22, 30, 26, 41, "A"); 
    for (x, y) in ((17, 26), (30, 26), (9, 20), (38, 20), (24, 16)): rect(g, x, y, x+1, y+2, "Y")
    return g


def icon_ruin():
    g = blank(); mound(g, 24, 42, 15, 3, "g", "g")
    rect(g, 8, 38, 40, 41, "T"); rect(g, 26, 38, 40, 41, "t")
    for (x, h) in ((11, 16), (20, 22), (30, 12), (36, 18)):
        rect(g, x, 38-h, x+3, 38, "T"); rect(g, x+2, 38-h, x+3, 38, "t")
        for k in range(0, h, 4): rect(g, x, 38-k, x+3, 38-k, "s")
        if h % 2 == 0: rect(g, x-1, 38-h-1, x+4, 38-h, "T")
    rect(g, 14, 33, 18, 35, "T"); rect(g, 24, 36, 28, 37, "t")
    for x in (9, 19, 33): g[39][x] = "G"
    return g
def icon_shrine():
    g = blank(); mound(g, 24, 42, 13, 3, "G", "g")
    # 環の輪の門（石の輪が2本の柱に乗る）
    rect(g, 12, 22, 15, 41, "T"); rect(g, 32, 22, 35, 41, "T"); rect(g, 14, 22, 15, 41, "t"); rect(g, 34, 22, 35, 41, "t")
    for y in range(8, 24):
        for x in range(10, 38):
            d = math.hypot((x-23.5)/13.0, (y-17)/9.0)
            if 0.72 < d < 1.0: g[y][x] = "T" if x < 24 else "t"
    rect(g, 22, 28, 26, 41, "N"); rect(g, 22, 28, 26, 30, "n"); g[24][24] = "Y"; g[25][24] = "Y"
    return g
def icon_cave():
    g = blank(); tri(g, 24, 18, 42, 15, "N", "n")
    for y in range(22, 42):
        for x in range(10, 38):
            if g[y][x] != "." and (x*5+y*3) % 9 == 0: g[y][x] = "T" if x < 24 else "t"
    for y in range(33, 42):
        for x in range(19, 29):
            if (x-23.5)**2/20 + (y-41)**2/70 <= 1: g[y][x] = "A" if y > 34 else "q"
    return g
def icon_stones():
    g = blank(); mound(g, 24, 41, 15, 4, "G", "g")
    for (x, y, h) in ((8, 40, 11), (16, 36, 14), (24, 35, 15), (32, 36, 13), (39, 40, 10)):
        rect(g, x, y-h, x+3, y, "T"); rect(g, x+2, y-h, x+3, y, "t"); rect(g, x, y-h, x+3, y-h, "s")
    return g
def icon_bigtree():
    g = blank()
    rect(g, 21, 28, 27, 43, "M"); rect(g, 25, 28, 27, 43, "m")
    for (cx, cy, r) in ((24, 14, 11), (14, 20, 8), (34, 20, 8), (24, 24, 9)):
        for y in range(cy-r, cy+r+1):
            for x in range(cx-r, cx+r+1):
                if (x-cx)**2+(y-cy)**2 <= r*r and 0 <= x < W: g[y][x] = "E" if (x-cx)+(y-cy) < 0 else "e"
    return g
def icon_vortex():
    g = blank()
    for y in range(8, 46):
        for x in range(2, 46):
            dx, dy = (x-24)/21.0, (y-27)/17.0
            d = math.hypot(dx, dy)
            if d > 1.0: continue
            ang = math.atan2(dy, dx)
            band = (d*6.0 + ang/(2*math.pi)*3.0) % 1.0
            g[y][x] = "C" if band < 0.18 else "c" if band < 0.35 else "L" if band < 0.75 else "l"
    for y in range(22, 33):
        for x in range(19, 30):
            if math.hypot((x-24)/5.0, (y-27)/5.5) <= 1.0: g[y][x] = "q"
    # 渦の中心にそびえる塔のかげ
    rect(g, 22, 12, 26, 28, "Q"); rect(g, 25, 12, 26, 28, "q"); rect(g, 21, 10, 27, 12, "Q"); rect(g, 23, 6, 25, 10, "Q"); g[5][24] = "Y"
    return g
def icon_volcano():
    g = blank()
    # 火山: 裾の広い黒い山。頂きに火口、赤い溶岩のすじ、けむり
    for y in range(14, 43):
        half = 6 + (y-14)*0.72
        for x in range(int(24-half), int(24+half)+1):
            if 0 <= x < W: g[y][x] = "Q" if x < 24 else "q"
    for y in range(14, 17):
        for x in range(18, 31):
            if abs(x-24) <= 5 - (y-14)//2 + 1: g[y][x] = "O" if y > 14 else "Y"
    for (x0, y0, ln) in ((22, 17, 12), (27, 17, 9), (19, 24, 8)):
        for k in range(ln):
            x = x0 + (k//4)*(1 if x0 > 23 else -1); g[y0+k][x] = "O" if k % 5 else "Y"
    for (cx, cy, r) in ((22, 8, 3), (27, 4, 3), (24, 1, 2)):
        for y in range(cy-r, cy+r+1):
            for x in range(cx-r, cx+r+1):
                if 0 <= y < H and (x-cx)**2+(y-cy)**2 <= r*r and g[y][x] == ".": g[y][x] = "T" if (x+y) % 2 else "t"
    return g
def icon_dive():
    g = blank()
    # 潜り場: 青い渦と、立ちのぼる泡。まんなかに暗い穴
    for y in range(18, 44):
        for x in range(4, 44):
            dx, dy = (x-24)/20.0, (y-31)/12.0
            d = math.hypot(dx, dy)
            if d > 1.0: continue
            ang = math.atan2(dy, dx)
            band = (d*4.0 + ang/(2*math.pi)*2.0) % 1.0
            g[y][x] = "C" if band < 0.12 else "B" if band < 0.4 else "L" if band < 0.75 else "l"
    for y in range(28, 35):
        for x in range(19, 30):
            if math.hypot((x-24)/5.0, (y-31)/3.2) <= 1.0: g[y][x] = "q"
    for (x, y, r) in ((24, 22, 2), (28, 15, 2), (21, 10, 1), (26, 6, 1), (23, 3, 1)):
        for yy in range(y-r, y+r+1):
            for xx in range(x-r, x+r+1):
                if (xx-x)**2+(yy-y)**2 <= r*r: g[yy][xx] = "C" if (xx+yy) % 2 else "c"
    return g
ICONS = {"port": icon_port, "village": icon_village, "lake": icon_lake, "mine": icon_mine, "castle": icon_castle, "tents": icon_tents, "temple": icon_temple, "snowtown": icon_snowtown, "sky": icon_sky, "palace": icon_palace, "ruin": icon_ruin, "shrine": icon_shrine, "cave": icon_cave, "stones": icon_stones, "bigtree": icon_bigtree, "vortex": icon_vortex, "volcano": icon_volcano, "dive": icon_dive}
if __name__ == "__main__":
    for n, fn in ICONS.items():
        g = outline(fn())
        used = sorted({c for r in g for c in r if c != "."})
        open(f"icon-{n}.txt", "w").write("\n".join("".join(r) for r in g) + "\n")
        json.dump({k: v for k, v in PAL.items() if k in used}, open(f"pal-icon-{n}.json", "w"))
        print(n, len(used))
