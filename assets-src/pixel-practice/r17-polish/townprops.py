"""町の小さな飾り（樽・街灯・井戸・道しるべ・木箱の山・花壇）を一から作る。光は左上、ハイライトなし（影と地の2〜3段）。
使い方: python3 townprops.py → barrel.txt, lamp.txt, well.txt, signpost.txt, crates.txt, flowerbed.txt と pal-*.json（48×48枠に下そろえで置く前の絵）"""
import json, math

W = H = 48
def blank(): return [["."]*W for _ in range(H)]

def rect(g, x0, y0, x1, y1, c):
    for y in range(y0, y1+1):
        for x in range(x0, x1+1):
            if 0 <= x < W and 0 <= y < H: g[y][x] = c

def ell(g, cx, cy, rx, ry, fn):
    for y in range(int(cy-ry-1), int(cy+ry+2)):
        for x in range(int(cx-rx-1), int(cx+rx+2)):
            if 0 <= x < W and 0 <= y < H and ((x-cx)/rx)**2 + ((y-cy)/ry)**2 <= 1: g[y][x] = fn(x, y, (x-cx)/rx, (y-cy)/ry)

def outline(g, c="A"):
    res = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] != ".": continue
            if any(0 <= y+dy < H and 0 <= x+dx < W and g[y+dy][x+dx] != "." for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))): res[y][x] = c
    return res

def shadow(g, cx, y, rx, c="S"):
    for x in range(cx-rx, cx+rx+1):
        for yy in (y, y+1):
            if 0 <= x < W and 0 <= yy < H and g[yy][x] == ".": g[yy][x] = c

WOOD = {"A": "#1c120c", "J": "#3a2616", "K": "#5a3a20", "L": "#7a5230", "M": "#9a6c40", "S": "#00000040"}
def hnoise(x, y, s=0):
    v = (x*374761393 + y*668265263 + s*1013) & 0xFFFFFFFF
    v = ((v ^ (v >> 13)) * 1274126177) & 0xFFFFFFFF
    return (v ^ (v >> 16)) & 0xFFFFFFFF

def barrel():
    g = blank()
    # 胴: 中ほどがふくらむ樽。左が地の色、右が影。縦の板目
    for y in range(22, 44):
        t = (y-22)/21
        half = 8 + 2.2*math.sin(math.pi*t)
        for x in range(int(24-half), int(24+half)+1):
            u = (x-(24-half))/(2*half)
            c = "L" if u < 0.3 else "K" if u < 0.75 else "J"
            if (x % 4) == 0: c = "J" if c != "J" else "A"
            g[y][x] = c
    # 鉄の帯（3本）
    for by in (25, 33, 41):
        for x in range(14, 35):
            if g[by][x] != ".": g[by][x] = "I" if x < 26 else "H"
        for x in range(14, 35):
            if g[by+1][x] != ".": g[by+1][x] = "H"
    # ふた
    ell(g, 24, 22, 8.2, 3.0, lambda x, y, nx, ny: "M" if nx < 0.1 else "L")
    g = outline(g)
    shadow(g, 24, 45, 11)
    pal = {**WOOD, "I": "#8a8f9a", "H": "#505560"}
    return g, pal

def lamp():
    g = blank()
    rect(g, 23, 14, 24, 44, "D")        # 柱
    for y in range(14, 45): g[y][23] = "E"
    rect(g, 21, 42, 26, 44, "D"); rect(g, 22, 40, 25, 41, "E")   # 台座
    # ランタン: 金枠の箱に、温かい光のガラス
    rect(g, 19, 6, 28, 7, "D"); rect(g, 20, 4, 27, 5, "D"); rect(g, 22, 2, 25, 3, "D")  # 屋根
    rect(g, 20, 8, 27, 15, "G")
    rect(g, 21, 9, 26, 14, "F")
    for y in range(9, 15): g[y][21] = "E"
    rect(g, 22, 10, 25, 13, "Y")
    rect(g, 23, 11, 24, 12, "W")
    rect(g, 19, 16, 28, 16, "D")
    g = outline(g)
    shadow(g, 24, 45, 6)
    pal = {"A": "#14100c", "D": "#2a2630", "E": "#4a4658", "G": "#3a3240", "F": "#c88a30", "Y": "#ffd060", "W": "#fff4b0", "S": "#00000040"}
    return g, pal

def well():
    g = blank()
    # 石の井筒（円柱）
    ell(g, 24, 38, 12, 6, lambda x, y, nx, ny: "N" if nx < -0.4 else "O" if nx < 0.4 else "P")
    for y in range(30, 40):
        for x in range(12, 37):
            if g[y][x] != "." and y >= 34:
                g[y][x] = "N" if x < 20 else "O" if x < 30 else "P"
    for y in range(34, 42):
        for x in range(12, 37):
            if g[y][x] != "." and (y-34) % 4 == 3: g[y][x] = "Q"
            if g[y][x] != "." and (x + (y//4)*3) % 7 == 0: g[y][x] = "Q"
    ell(g, 24, 33, 11, 4.6, lambda x, y, nx, ny: "R" if ny*ny + nx*nx > 0.5 else "Z")   # 水面
    # 屋根を支える2本の柱と、切妻の屋根
    rect(g, 13, 14, 14, 33, "K"); rect(g, 33, 14, 34, 33, "J")
    for x in range(8, 40):
        top = 6 + abs(x-24)*0.35
        for y in range(int(top), int(top)+5):
            g[y][x] = "T" if (x < 24) else "U"
        g[int(top)+4][x] = "V"
    rect(g, 24, 14, 24, 28, "L")        # つるべ縄
    rect(g, 22, 28, 26, 31, "K"); rect(g, 22, 28, 26, 28, "M")   # 桶
    g = outline(g)
    shadow(g, 24, 45, 14)
    pal = {"A": "#1c120c", "J": "#3a2616", "K": "#5a3a20", "L": "#8a6a40", "M": "#a88050", "N": "#9a968c", "O": "#7a766c", "P": "#585450", "Q": "#403c38", "R": "#2a4a68", "Z": "#4a86b0", "T": "#c0553c", "U": "#8a3a2c", "V": "#5a2418", "S": "#00000040"}
    return g, pal

def signpost():
    g = blank()
    rect(g, 23, 12, 25, 44, "K")
    for y in range(12, 45): g[y][23] = "L"; g[y][25] = "J"
    # 矢印の板（右向きと左向き）
    for (y0, x0, x1, tip) in ((14, 24, 40, 1), (24, 8, 24, -1)):
        for y in range(y0, y0+6):
            for x in range(x0, x1+1):
                g[y][x] = "M" if y == y0 else "L" if y < y0+4 else "K"
        if tip == 1:
            for k in range(3): g[y0+k][x1+1+k] = "L"; g[y0+5-k][x1+1+k] = "K"
        else:
            for k in range(3): g[y0+k][x0-1-k] = "L"; g[y0+5-k][x0-1-k] = "K"
        for x in range(x0+3, x1-3, 3): g[y0+2][x] = "J"   # 文字風の点々
    g = outline(g)
    shadow(g, 24, 45, 6)
    return g, {**WOOD}

def crates():
    g = blank()
    def crate(x0, y0, sz):
        for y in range(y0, y0+sz):
            for x in range(x0, x0+sz):
                edge = x in (x0, x0+sz-1) or y in (y0, y0+sz-1)
                c = "J" if edge else "L" if x < x0+sz-4 else "K"
                if not edge and abs((x-x0) - (y-y0)) <= 0: c = "J"
                if not edge and (x-x0) + (y-y0) == sz-1: c = "J"
                g[y][x] = c
        for x in range(x0+1, x0+sz-1): g[y0+1][x] = "M"
    crate(10, 30, 15); crate(26, 30, 15); crate(18, 15, 15)
    # 麻袋
    ell(g, 36, 40, 5.5, 4.5, lambda x, y, nx, ny: "B" if nx < -0.3 else "C" if nx < 0.4 else "D")
    for x in range(33, 40): g[34][x] = "C"
    g = outline(g)
    shadow(g, 24, 45, 15)
    return g, {**WOOD, "B": "#d8c080", "C": "#b89c58", "D": "#8a7240"}

def flowerbed():
    g = blank()
    # 木枠の花壇（低い）に、色とりどりの花
    rect(g, 8, 38, 40, 44, "K")
    for x in range(8, 41): g[38][x] = "M"; g[44][x] = "J"; g[43][x] = "J"
    rect(g, 9, 39, 39, 42, "E")          # 土・葉
    cols = ["R", "Y", "P", "W", "V"]
    for i in range(14):
        x = 10 + (i*5) % 29 + (i % 2); y = 36 + (i % 3)
        c = cols[i % 5]
        g[y][x] = c; g[y][x+1] = c; g[y-1][x] = c; g[y+1][x] = "G"; g[y+2][x] = "G"
        g[y][x+1] = "Y" if i % 3 == 0 else c
    for y in range(39, 43):
        for x in range(9, 40):
            if g[y][x] == "E" and (x*7+y*3) % 5 == 0: g[y][x] = "G"
    g = outline(g)
    shadow(g, 24, 45, 17)
    return g, {**WOOD, "E": "#3a5a2a", "G": "#5a9a3a", "R": "#e8506a", "Y": "#ffd848", "P": "#c070e0", "W": "#f8f4e8", "V": "#7aa0f0"}

def write(name, g, pal):
    used = sorted({c for r in g for c in r if c != "."})
    pal = {k: v for k, v in pal.items() if k in used}
    # 影（半透明）はゲームの絵に使えないので、暗い色で
    if "S" in pal: pal["S"] = "#2a3a28"
    open(f"{name}.txt", "w").write("\n".join("".join(r) for r in g) + "\n")
    json.dump(pal, open(f"pal-{name}.json", "w"))
    print(name, len(used))

if __name__ == "__main__":
    for n, fn in (("barrel", barrel), ("lamp", lamp), ("well", well), ("signpost", signpost), ("crates", crates), ("flowerbed", flowerbed)):
        g, p = fn(); write(n, g, p)
