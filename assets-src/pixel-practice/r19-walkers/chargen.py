"""キャラクター描画エンジン。部品（太さが変わる四肢・多角形・楕円）を重ね、素材ごとのランプで円柱状の明暗を付ける。
光は左上。出力: 文字グリッド（1文字=1色）とパレットJSON。"""
import math, json, random
class Img:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.mat = [[None]*w for _ in range(h)]
        self.lum = [[0.0]*w for _ in range(h)]
        self.part = [[None]*w for _ in range(h)]
        self.ink = [[None]*w for _ in range(h)]       # 固定色（目の白など）
    def ok(self, x, y): return 0 <= x < self.w and 0 <= y < self.h
    def set(self, x, y, mat, lum, part=None):
        if self.ok(x, y): self.mat[y][x] = mat; self.lum[y][x] = lum; self.part[y][x] = part; self.ink[y][x] = None
    def fixed(self, x, y, key, part=None):
        if self.ok(x, y): self.mat[y][x] = key; self.ink[y][x] = key; self.part[y][x] = part; self.lum[y][x] = 0
LIGHT = (-0.62, -0.78)     # 光の向き（左上）
def capsule(im, a, b, ra, rb, mat, part=None, bulge=0.0, light_bias=0.0):
    (ax, ay), (bx, by) = a, b
    dx, dy = bx-ax, by-ay; L = math.hypot(dx, dy) or 1; ux, uy = dx/L, dy/L; px, py = -uy, ux
    x0, x1 = int(min(ax, bx)-max(ra, rb)-2), int(max(ax, bx)+max(ra, rb)+2)
    y0, y1 = int(min(ay, by)-max(ra, rb)-2), int(max(ay, by)+max(ra, rb)+2)
    for y in range(y0, y1+1):
        for x in range(x0, x1+1):
            vx, vy = x+.5-ax, y+.5-ay
            t = (vx*ux+vy*uy)/L; s = vx*px+vy*py
            tt = max(0, min(1, t))
            r = ra+(rb-ra)*tt + bulge*math.sin(tt*math.pi)
            # 端の丸み
            if t < 0 or t > 1:
                ex, ey = (ax, ay) if t < 0 else (bx, by)
                if math.hypot(x+.5-ex, y+.5-ey) > (ra if t < 0 else rb): continue
                s = (x+.5-ex)*px+(y+.5-ey)*py
            elif abs(s) > r: continue
            n = s/r                       # 断面の位置 -1..1
            nx, ny = n*px, n*py           # 表面の法線（横向き成分）
            z = math.sqrt(max(0, 1-n*n))
            lum = -(nx*LIGHT[0]+ny*LIGHT[1])*0.9 + 0.45*z + light_bias - 0.15
            im.set(x, y, mat, lum, part)
def poly(im, pts, mat, part=None, shade=None, light_bias=0.0):
    ys = [p[1] for p in pts]; xs = [p[0] for p in pts]
    cx, cy = sum(xs)/len(xs), sum(ys)/len(ys); rx = (max(xs)-min(xs))/2 or 1; ry = (max(ys)-min(ys))/2 or 1
    for y in range(int(min(ys)), int(max(ys))+2):
        for x in range(int(min(xs)), int(max(xs))+2):
            inside = False
            for i in range(len(pts)):
                (xi, yi), (xj, yj) = pts[i], pts[i-1]
                if (yi > y+.5) != (yj > y+.5) and x+.5 < (xj-xi)*(y+.5-yi)/(yj-yi)+xi: inside = not inside
            if inside:
                nx, ny = (x+.5-cx)/rx, (y+.5-cy)/ry
                lum = shade(x, y, nx, ny) if shade else (nx*LIGHT[0]+ny*LIGHT[1])*-0.7 + 0.3 + light_bias
                im.set(x, y, mat, lum, part)
def ellipse(im, cx, cy, rx, ry, mat, part=None, light_bias=0.0, shade=None):
    for y in range(int(cy-ry-1), int(cy+ry+2)):
        for x in range(int(cx-rx-1), int(cx+rx+2)):
            nx, ny = (x+.5-cx)/rx, (y+.5-cy)/ry; r2 = nx*nx+ny*ny
            if r2 > 1: continue
            z = math.sqrt(1-r2)
            lum = shade(x, y, nx, ny) if shade else (nx*LIGHT[0]+ny*LIGHT[1])*-0.85+0.5*z+light_bias
            im.set(x, y, mat, lum, part)
def render(im, ramps, edges, seps=(), thresholds=None, dither=False, merge=True):
    """ramps: {mat: [暗...明の色]}。edges: {mat: 縁取りの色}。seps: 部品どうしの境に内側の線を引く組 (partA, partB)。"""
    W, H = im.w, im.h
    colors = []; idx = {}
    def key(c):
        if c in idx: return idx[c]
        def rgb(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
        r0 = rgb(c)
        for e in (colors if merge else []):      # ほぼ同じ色は1色にまとめる（色数を減らす）
            if sum(abs(a-b) for a, b in zip(r0, rgb(e))) <= 30: idx[c] = idx[e]; return idx[c]
        idx[c] = len(colors); colors.append(c)
        return idx[c]
    grid = [[None]*W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            m = im.mat[y][x]
            if m is None: continue
            if im.ink[y][x]: grid[y][x] = key(ramps[im.ink[y][x]][0]); continue
            r = ramps[m]; n = len(r)
            t = thresholds or [-0.1, 0.25, 0.6][:n-1]
            if n != 4: t = [(-0.45+0.15*i+0.0) for i in range(n-1)]
            lum = im.lum[y][x]
            level = sum(1 for th in t if lum > th)
            grid[y][x] = key(r[min(level, n-1)])
    out = [row[:] for row in grid]
    # 外周の縁取り（素材ごとの暗色）。外側に1ドット足す
    for y in range(H):
        for x in range(W):
            if grid[y][x] is not None: continue
            nb = [(x+dx, y+dy) for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)) if im.ok(x+dx, y+dy) and im.mat[y+dy][x+dx] is not None]
            if nb:
                m = im.mat[nb[0][1]][nb[0][0]]
                e = edges.get(m, "#1a1420")
                # 明るい側（左上）の縁は少し明るく
                out[y][x] = key(e)
    # 部品の境の内側の線
    for y in range(H):
        for x in range(W):
            p = im.part[y][x]
            if p is None: continue
            for dx, dy in ((1,0),(0,1)):
                if im.ok(x+dx, y+dy):
                    q = im.part[y+dy][x+dx]
                    if q is not None and q != p and ((p, q) in seps or (q, p) in seps):
                        a, b = (x, y), (x+dx, y+dy)
                        # 奥にある（先に描かれた）側を縁取り色にする: ここでは手前=q と仮定し、pの側に線
                        m = im.mat[y][x]
                        if im.ink[y][x] is None: out[y][x] = key(edges.get(m, "#1a1420"))
    return out, colors
def to_text(out, colors):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    rows = []
    for r in out: rows.append("".join("." if v is None else letters[v] for v in r))
    pal = {letters[i]: c for i, c in enumerate(colors)}
    return "\n".join(rows)+"\n", pal
