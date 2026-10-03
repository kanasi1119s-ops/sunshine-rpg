"""r20-props 共通の道具。1文字=1色の文字グリッド。光は左上、ハイライト（照り）なし、影と地の2〜3段。
色は Pal が自動で1文字ずつ割り当てる（A=最初に登録した縁取り）。"""
import json, math

def hn(x, y, s=0):
    v = (x*374761393 + y*668265263 + s*1013) & 0xFFFFFFFF
    v = ((v ^ (v >> 13)) * 1274126177) & 0xFFFFFFFF
    return (v ^ (v >> 16)) & 0xFFFFFFFF

class Pal:
    POOL = "BCDEFGHIJKLMNOPQRTUVWXYZabcdefghijklmnopqrstuvwxyz"
    def __init__(self):
        self.m = {}; self.n = 0
    def add(self, hexv):
        for k, v in self.m.items():
            if v == hexv: return k
        if hexv in ("#26382a", "#14121c"): key = "S"     # 足元の影はいつも S（本体側で色を差し替えられるように）
        elif not self.m: key = "A"
        else: key = self.POOL[self.n]; self.n += 1
        self.m[key] = hexv
        return key
    def __call__(self, *hexes):
        r = [self.add(h) for h in hexes]
        return r if len(r) > 1 else r[0]

class G:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.g = [["."]*w for _ in range(h)]
    def put(self, x, y, c):
        x, y = int(x), int(y)
        if 0 <= x < self.w and 0 <= y < self.h: self.g[y][x] = c
    def get(self, x, y):
        return self.g[y][x] if 0 <= x < self.w and 0 <= y < self.h else "."
    def rect(self, x0, y0, x1, y1, c):
        for y in range(int(y0), int(y1)+1):
            for x in range(int(x0), int(x1)+1): self.put(x, y, c)
    def ell(self, cx, cy, rx, ry, fn):
        for y in range(int(cy-ry-1), int(cy+ry+2)):
            for x in range(int(cx-rx-1), int(cx+rx+2)):
                nx, ny = (x+.5-cx)/rx, (y+.5-cy)/ry
                if nx*nx+ny*ny <= 1:
                    c = fn(x, y, nx, ny) if callable(fn) else fn
                    if c: self.put(x, y, c)
    def poly(self, pts, fn):
        ys = [p[1] for p in pts]
        for y in range(int(min(ys)), int(max(ys))+1):
            for x in range(self.w):
                ins = False
                for i in range(len(pts)):
                    (xi, yi), (xj, yj) = pts[i], pts[i-1]
                    if (yi > y+.5) != (yj > y+.5) and x+.5 < (xj-xi)*(y+.5-yi)/(yj-yi)+xi: ins = not ins
                if ins:
                    c = fn(x, y) if callable(fn) else fn
                    if c: self.put(x, y, c)
    def line(self, x0, y0, x1, y1, c):
        n = int(max(abs(x1-x0), abs(y1-y0))) or 1
        for i in range(n+1): self.put(round(x0+(x1-x0)*i/n), round(y0+(y1-y0)*i/n), c)
    def thick(self, x0, y0, x1, y1, r, c):
        n = int(max(abs(x1-x0), abs(y1-y0))*2) or 1
        for i in range(n+1):
            cx, cy = x0+(x1-x0)*i/n, y0+(y1-y0)*i/n
            for y in range(int(cy-r-1), int(cy+r+2)):
                for x in range(int(cx-r-1), int(cx+r+2)):
                    if (x+.5-cx)**2+(y+.5-cy)**2 <= r*r: self.put(x, y, c)
    def outline(self, default, by=None):
        by = by or {}
        add = []
        for y in range(self.h):
            for x in range(self.w):
                if self.g[y][x] != ".": continue
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    n = self.get(x+dx, y+dy)
                    if n != ".":
                        add.append((x, y, by.get(n, default))); break
        for x, y, c in add: self.g[y][x] = c
    def shadow(self, cx, y, rx, c, ry=1):
        """足元の濃い楕円の影（空いているマスだけ塗る）"""
        for yy in range(y-ry, y+ry+1):
            for x in range(cx-rx, cx+rx+1):
                if ((x+.5-cx)/(rx+.5))**2 + ((yy-y)/(ry+.5))**2 <= 1 and self.get(x, yy) == ".": self.put(x, yy, c)
    def flipx(self):
        self.g = [r[::-1] for r in self.g]

def write(name, g, pal, outdir="."):
    while g.g and all(c == "." for c in g.g[0]): g.g.pop(0)   # 上の空き行を詰める（足元は下そろえ）
    used = {c for r in g.g for c in r if c != "."}
    p = {k: v for k, v in pal.m.items() if k in used}
    open(f"{outdir}/{name}.txt", "w").write("\n".join("".join(r) for r in g.g) + "\n")
    json.dump(p, open(f"{outdir}/pal-{name}.json", "w"))
    return len(p)

GRASS_SH = "#26382a"   # 草地に落ちる影
DUNG_SH = "#14121c"    # ダンジョンの床に落ちる影
