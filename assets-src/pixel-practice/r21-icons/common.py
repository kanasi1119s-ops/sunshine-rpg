"""r21-icons 共通部品: 16x16 キャンバス、色表、自動縁取り。"""

SIZE = 16

# 1文字=1色。どのアイコンでも同じ文字は同じ色（パレットJSONは使った文字だけ書き出す）
COLORS = {
    # 縁取り（素材ごとの暗い色。黒一色にしない）
    'k': '#2a3040',  # 鋼の縁
    'n': '#35200f',  # 木・革・肌の縁
    'y': '#523210',  # 金の縁
    'r': '#4a1420',  # 赤・炎の縁
    'b': '#14284e',  # 青・水の縁
    'e': '#123a24',  # 緑の縁
    'v': '#31184e',  # 紫・闇の縁
    'm': '#2e2e38',  # 石・灰色の縁
    # 鋼
    'S': '#e0e7f1', 's': '#a9b5ca', 'z': '#75819c',
    # 金
    'G': '#f6d466', 'H': '#d49a2e', 'J': '#94621c',
    # 木・革
    'W': '#c08850', 'w': '#94603a', 'x': '#66402a',
    # 赤
    'R': '#e86a5e', 'Q': '#c03c40', 'q': '#8a2434',
    # 青
    'B': '#6ab0f0', 'C': '#3e7ac8', 'c': '#285096',
    # 緑
    'L': '#7cd070', 'l': '#46a04e', 'd': '#2e7038',
    # 紫
    'V': '#b890e8', 'U': '#8a5cc4', 'u': '#5e3a92',
    # 布・紙
    'F': '#f4eedc', 'f': '#d4ccb0', 'h': '#a39c84',
    # 炎・光
    'Y': '#fff0a0', 'O': '#f89a3c', 'T': '#e06a28',
    # 肌
    'P': '#f0c8a0', 'p': '#c89070',
    # 石
    'M': '#b0b0bc', 'N': '#82828f', 'D': '#585866',
    # 闇
    'A': '#22222c', 'a': '#40404e',
    # 水の淡い色
    'I': '#a6e0f0',
    # 青緑（風）
    'j': '#2f8c8a', 'o': '#1d5a5c',
}

# 縁取りの文字（これ自身の外側には縁を足さない）
OUTLINE_KEYS = set('knyrebvm')

# 塗りの文字 -> 縁取りの文字
OMAP = {}
for _ks, _o in [('Ssz', 'k'), ('GHJ', 'y'), ('Wwx', 'n'), ('RQq', 'r'), ('BCcI', 'b'),
                ('Lld', 'e'), ('VUu', 'v'), ('Ffh', 'n'), ('YOT', 'r'), ('Pp', 'n'),
                ('MND', 'm'), ('Aa', 'v'), ('jo', 'b')]:
    for _k in _ks:
        OMAP[_k] = _o


class Canvas:
    def __init__(self):
        self.g = [['.'] * SIZE for _ in range(SIZE)]
        self.omap = dict(OMAP)
        self.no_outline = False

    def px(self, x, y, k):
        if 0 <= x < SIZE and 0 <= y < SIZE:
            self.g[y][x] = k
        return self

    def pts(self, k, *p):
        for x, y in p:
            self.px(x, y, k)
        return self

    def rect(self, x0, y0, x1, y1, k):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, k)
        return self

    def line(self, x0, y0, x1, y1, k):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.px(x0, y0, k)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy
        return self

    def poly(self, points, k):
        n = len(points)
        for y in range(SIZE):
            for x in range(SIZE):
                px_, py_ = x + 0.5, y + 0.5
                inside = False
                j = n - 1
                for i in range(n):
                    xi, yi = points[i]
                    xj, yj = points[j]
                    if (yi > py_) != (yj > py_) and px_ < (xj - xi) * (py_ - yi) / (yj - yi) + xi:
                        inside = not inside
                    j = i
                if inside:
                    self.g[y][x] = k
        return self

    def ell(self, cx, cy, rx, ry, k):
        for y in range(SIZE):
            for x in range(SIZE):
                if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1.0:
                    self.g[y][x] = k
        return self

    def sphere(self, cx, cy, rx, ry, keys):
        """丸い物を 明・中・暗 の3段で塗る（左上が明るい。照りの点は打たない）"""
        lit, mid, dark = keys
        for y in range(SIZE):
            for x in range(SIZE):
                u, v = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
                if u * u + v * v <= 1.0:
                    t = (u + v) / 2
                    self.g[y][x] = lit if t < -0.28 else (dark if t > 0.30 else mid)
        return self

    def stamp(self, x0, y0, rows):
        for dy, row in enumerate(rows):
            for dx, ch in enumerate(row):
                if ch not in '. ':
                    self.px(x0 + dx, y0 + dy, ch)
        return self

    def replace(self, a, b):
        for y in range(SIZE):
            for x in range(SIZE):
                if self.g[y][x] == a:
                    self.g[y][x] = b
        return self

    def outline(self):
        if self.no_outline:
            return self
        add = []
        for y in range(SIZE):
            for x in range(SIZE):
                if self.g[y][x] != '.':
                    continue
                best = None
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < SIZE and 0 <= ny < SIZE:
                        c = self.g[ny][nx]
                        if c != '.' and c not in OUTLINE_KEYS and best is None:
                            best = self.omap.get(c, 'm')
                if best:
                    add.append((x, y, best))
        for x, y, k in add:
            self.g[y][x] = k
        return self

    def rows(self):
        return [''.join(r) for r in self.g]


ART = {}  # (種類, 名前) -> (説明, 関数)


def icon(kind, name, desc):
    def deco(fn):
        ART[(kind, name)] = (desc, fn)
        return fn
    return deco


def from_rows(rows, x0=0, y0=0):
    c = Canvas()
    c.stamp(x0, y0, rows)
    return c
