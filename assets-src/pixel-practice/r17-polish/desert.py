"""砂漠の飾り（ヤシの木・サボテン）を一から作る。使い方: python3 desert.py → palm.txt, cactus.txt と pal-*.json"""
import json, math

def h(x, y, s=0):
    v = (x * 374761393 + y * 668265263 + s * 144665) & 0xFFFFFFFF
    v = ((v ^ (v >> 13)) * 1274126177) & 0xFFFFFFFF
    return (v ^ (v >> 16)) & 0xFFFFFFFF

W = H = 48

class Canvas:
    def __init__(self): self.m = [[None]*W for _ in range(H)]
    def brush(self, cx, cy, r, tag):
        for y in range(int(cy-r-1), int(cy+r+2)):
            for x in range(int(cx-r-1), int(cx+r+2)):
                if 0 <= x < W and 0 <= y < H and (x-cx)**2 + (y-cy)**2 <= r*r: self.m[y][x] = tag
    def line(self, x0, y0, x1, y1, w0, w1, tag):
        n = int(max(abs(x1-x0), abs(y1-y0))*2) + 1
        for i in range(n+1):
            t = i/n; self.brush(x0+(x1-x0)*t, y0+(y1-y0)*t, (w0+(w1-w0)*t)/2, tag)

def outline(g, out_letter):
    res = [r[:] for r in g]
    for y in range(H):
        for x in range(W):
            if g[y][x] != ".": continue
            if any(0 <= y+dy < H and 0 <= x+dx < W and g[y+dy][x+dx] != "." for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))): res[y][x] = out_letter
    return res

def palm():
    c = Canvas()
    # 幹: ゆるくしなる曲線。節（横のすじ）を付ける
    pts = [(22, 45), (23, 38), (25, 30), (26, 22), (25, 15)]
    for (xa, ya), (xb, yb) in zip(pts, pts[1:]): c.line(xa, ya, xb, yb, 5 if ya > 40 else 4, 3.6 if yb > 20 else 3, "t")
    # 葉: 頂点から放射状に伸び、先が下へ垂れる細い葉を9枚
    cx, cy = 25, 14
    for k, ang in enumerate((-180, -150, -120, -90, -60, -30, 0, -135, -45)):
        a = math.radians(ang)
        length = 18 if k < 7 else 12
        for i in range(0, 31):
            t = i/30
            x = cx + math.cos(a)*length*t
            y = cy + math.sin(a)*length*t*0.95 + 14*t*t
            c.brush(x, y, 1.0*(1-t) + 0.45, "f")
    # ココナッツ
    for dx, dy in ((-2, 2), (1, 3), (3, 1)): c.brush(cx+dx, cy+dy, 1.5, "n")
    g = [["."]*W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            m = c.m[y][x]
            if m is None: continue
            left = x == 0 or c.m[y][x-1] != m
            right = x == W-1 or c.m[y][x+1] != m
            if m == "t":
                col = "M" if left else "K" if right else ("L" if (y % 4) else "J")
            elif m == "f":
                col = "H" if (y < cy-1 and h(x, y) % 4 == 0) else "G" if left else "E" if right else "F"
            else: col = "N"
            g[y][x] = col
    g = outline(g, "A")
    # 根もとの砂だまり
    for y in range(43, 47):
        for x in range(12, 33):
            e = ((x-22)/10.0)**2 + ((y-45)/2.0)**2
            if e <= 1 and g[y][x] == ".": g[y][x] = "S" if y < 46 else "T"
    pal = {"A": "#2a1a0e", "J": "#4a3018", "K": "#6a4a28", "L": "#8a6638", "M": "#b08850", "E": "#2f6a2a", "F": "#4a9a36", "G": "#74c050", "H": "#a8e078", "N": "#5a3a1c", "S": "#e8cf90", "T": "#c8a868"}
    return g, pal

def cactus():
    c = Canvas()
    c.line(24, 45, 24, 14, 9, 8, "b")
    c.brush(24, 13, 4, "b")
    c.line(24, 30, 15, 30, 3.4, 3.4, "a"); c.line(15, 30, 15, 21, 3.8, 3.4, "a"); c.brush(15, 20, 1.9, "a")
    c.line(24, 26, 34, 26, 3.4, 3.4, "a"); c.line(34, 26, 34, 18, 3.8, 3.4, "a"); c.brush(34, 17, 1.9, "a")
    g = [["."]*W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            m = c.m[y][x]
            if m is None: continue
            # 円柱の陰影: 左が地、右が影（ハイライトなし）。縦のうね
            xs = [xx for xx in range(W) if c.m[y][xx] == m]
            x0, x1 = min(xs), max(xs)
            t = (x - x0) / max(1, x1 - x0)
            col = "E" if t < 0.2 else "F" if t < 0.62 else "D"
            if (x - x0) % 4 == 2 and 0.2 <= t < 0.9: col = "D" if col == "F" else col
            if m == "a": col = "F" if t < 0.55 else "D"
            g[y][x] = col
    # とげ（点々）と花
    for y in range(12, 44, 3):
        for x in range(W):
            if g[y][x] in "F" and h(x, y) % 6 == 0: g[y][x] = "I"
    g[9][24] = "P"; g[9][23] = "P"; g[10][24] = "P"; g[9][25] = "P"
    g = outline(g, "A")
    for y in range(44, 47):
        for x in range(14, 34):
            e = ((x-24)/9.0)**2 + ((y-45)/1.8)**2
            if e <= 1 and g[y][x] == ".": g[y][x] = "S" if y < 46 else "T"
    pal = {"A": "#14301c", "D": "#2a6a38", "E": "#5aaa5a", "F": "#3e8a46", "I": "#d8e8a0", "P": "#e86a8a", "S": "#e8cf90", "T": "#c8a868"}
    return g, pal

def write(name, g, pal):
    used = sorted({c for r in g for c in r if c != "."})
    open(f"{name}.txt", "w").write("\n".join("".join(r) for r in g) + "\n")
    json.dump({k: v for k, v in pal.items() if k in used}, open(f"pal-{name}.json", "w"))
    print(name, len(used))

if __name__ == "__main__":
    for n, fn in (("palm", palm), ("cactus", cactus)):
        g, p = fn(); write(n, g, p)
