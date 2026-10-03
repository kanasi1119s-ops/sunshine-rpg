"""r22-vehicles 共通の道具（キャンバス・図形・縁取り・パレット）。worldicons.py と同じ考え方:
1文字=1色、光は左上、ハイライト（照り）なし、縁取りは素材ごとの暗い色、1枚あたり最大16色。"""
import math

PAL = {
    "A": "#1c1410", "a": "#14243e",
    "M": "#7a5230", "m": "#5a3a20", "N": "#a89070", "n": "#7a6850", "K": "#4a2c18",
    "C": "#f0f6fc", "c": "#c0d4e8",
    "R": "#c0553c", "r": "#8a3a2c",
    "L": "#3a6a9a", "l": "#2a4a78", "B": "#7ab0d8",
    "Y": "#e8c040", "O": "#e86a20",
    "D": "#d8c080", "d": "#b09858",
    "G": "#5a9a40", "g": "#3a7032", "F": "#1f3a20",
    "T": "#8a8f9c", "t": "#686d7a", "Q": "#5a5060", "q": "#3a3040",
    "U": "#a8987f", "u": "#7a6c5c", "V": "#4e443c",
    "P": "#f4f0e4", "p": "#c4ccdc",
    "W": "#e8dcc0", "w": "#b8a888",
    "S": "#7ab8b0", "s": "#4a8a8a", "z": "#2e5e66",
}

# 縁取りの色（素材ごと）。泡・水は縁取りしない。
OUT = {
    "M": "A", "m": "A", "N": "A", "n": "A", "K": "A", "W": "A", "w": "A",
    "R": "A", "r": "A", "Y": "K", "O": "K", "D": "K", "d": "K",
    "G": "F", "g": "F", "F": "F",
    "T": "A", "t": "A", "Q": "q", "q": "q",
    "U": "A", "u": "A", "V": "A",
    "P": "Q", "p": "Q", "S": "z", "s": "z", "z": "a", "B": "a",
}
NOOUT = set("CcLl")


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.g = [["."] * w for _ in range(h)]

    def px(self, x, y, c):
        x, y = int(x), int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            self.g[y][x] = c

    def get(self, x, y):
        if 0 <= x < self.w and 0 <= y < self.h:
            return self.g[y][x]
        return "."

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, c)

    def poly(self, pts, c, only=None):
        """多角形を塗る（ピクセル中心で判定）。only を渡すと、その文字の上だけ塗る。"""
        ys = [p[1] for p in pts]
        n = len(pts)
        for y in range(int(math.floor(min(ys))), int(math.ceil(max(ys))) + 1):
            yc = y + 0.5
            xs = []
            for i in range(n):
                (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
                if (y1 <= yc < y2) or (y2 <= yc < y1):
                    xs.append(x1 + (yc - y1) * (x2 - x1) / (y2 - y1))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                for x in range(int(math.ceil(xs[i] - 0.5)), int(math.floor(xs[i + 1] - 0.5)) + 1):
                    if only is None or self.get(x, y) in only:
                        self.px(x, y, c)

    def line(self, x0, y0, x1, y1, c):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            self.px(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy; x0 += sx
            if e2 <= dx:
                err += dx; y0 += sy

    def ell(self, cx, cy, rx, ry, c, only=None):
        for y in range(int(cy - ry - 1), int(cy + ry + 2)):
            for x in range(int(cx - rx - 1), int(cx + rx + 2)):
                if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1.0:
                    if only is None or self.get(x, y) in only:
                        self.px(x, y, c)

    def ring(self, cx, cy, rx, ry, t, c, only=None):
        for y in range(int(cy - ry - 2), int(cy + ry + 3)):
            for x in range(int(cx - rx - 2), int(cx + rx + 3)):
                d = math.hypot((x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry)
                if 1.0 - t <= d <= 1.0:
                    if only is None or self.get(x, y) in only:
                        self.px(x, y, c)

    def mirror(self):
        o = Canvas(self.w, self.h)
        o.g = [r[::-1] for r in self.g]
        return o

    def paste(self, other, ox, oy, skip="."):
        for y in range(other.h):
            for x in range(other.w):
                c = other.g[y][x]
                if c != skip:
                    self.px(ox + x, oy + y, c)

    def outline(self):
        res = [r[:] for r in self.g]
        for y in range(self.h):
            for x in range(self.w):
                if self.g[y][x] != ".":
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    n = self.get(x + dx, y + dy)
                    if n != "." and n not in NOOUT and n in OUT:
                        res[y][x] = OUT[n]
                        break
        self.g = res
        return self

    def rows(self):
        return ["".join(r) for r in self.g]


def shade(c, light, dark, split):
    """c の中で split(x,y) が真の所を dark、偽を light にする（元の文字が light のときだけ）。"""
    for y in range(c.h):
        for x in range(c.w):
            if c.g[y][x] == light and split(x, y):
                c.g[y][x] = dark
