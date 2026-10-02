"""練習用: 図形（多角形・楕円・線）で文字グリッドの下書きを作る小さな道具。仕上げは手で直してエディタに描き込む。
使い方: from shapes import Canvas ; c = Canvas(32, 32); c.poly([(x,y),...], 'B'); c.line(x0,y0,x1,y1,'A'); c.outline('A'); print(c)"""
class Canvas:
    def __init__(self, w, h): self.w, self.h = w, h; self.g = [["." for _ in range(w)] for _ in range(h)]
    def put(self, x, y, k):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < self.w and 0 <= y < self.h: self.g[y][x] = k
    def get(self, x, y): return self.g[y][x] if 0 <= x < self.w and 0 <= y < self.h else "."
    def poly(self, pts, k):
        ys = [p[1] for p in pts]
        for y in range(int(min(ys)), int(max(ys)) + 1):
            for x in range(self.w):
                inside = False
                for i in range(len(pts)):
                    (xi, yi), (xj, yj) = pts[i], pts[i - 1]
                    if (yi > y + .5) != (yj > y + .5) and x + .5 < (xj - xi) * (y + .5 - yi) / (yj - yi) + xi: inside = not inside
                if inside:
                    kk = k(x, y) if callable(k) else k
                    if kk: self.put(x, y, kk)
    def ellipse(self, cx, cy, rx, ry, k):
        for y in range(self.h):
            for x in range(self.w):
                if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1:
                    kk = k(x, y) if callable(k) else k
                    if kk: self.put(x, y, kk)
    def line(self, x0, y0, x1, y1, k):
        n = int(max(abs(x1 - x0), abs(y1 - y0))) or 1
        for i in range(n + 1): self.put(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n, k)
    def outline(self, k, skip=()):
        add = []
        for y in range(self.h):
            for x in range(self.w):
                if self.g[y][x] in (".",) + tuple(skip) and any(self.get(x + a, y + b) not in (".",) + tuple(skip) for a, b in ((1,0),(-1,0),(0,1),(0,-1))): add.append((x, y))
        for x, y in add: self.g[y][x] = k
    def __str__(self): return "\n".join("".join(r) for r in self.g)
