"""飛空艇「風待ち」のドット絵（2026-10-05、人間の指示「カッコいい飛空艇のドット絵も作って」）。
第7章の小説の場面の姿にそろえた: 細長い木の船・布を張った二枚の羽根・灯り石を埋めた丸い機関・船首に羽を広げた空鳥の彫刻。
既存作品の飛空艇の形は写していない（羽根は帆布を張った木の骨組み、機関は輪の中で灯り石が光る、この世界の作り）。

出力（このフォルダ）:
  airship-right-0/1, airship-left-0/1, airship-down-0/1, airship-up-0/1（40×40。フィールドを飛ぶ絵、各向き2コマ）
  airship-landed（48×48。着陸中）、airship-shadow（24×10。飛んでいるときの地面の影）
  airship-showcase（160×96。空を飛ぶ大きな絵）
どれも .txt（1文字=1色、'.'=透明）と pal-*.json。tools/pixel-practice/editor-draw.mjs でエディタに描き入れて確かめる。
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# フィールド用の16色（光は左上）
PAL = {
    "K": "#1e1620",  # 縁・いちばん暗い
    "W": "#4a2a18",  # 木（影）
    "w": "#7a4a28",  # 木
    "o": "#a8703c",  # 木（光）
    "B": "#8a6418",  # 真鍮（影）
    "b": "#d8a838",  # 真鍮
    "h": "#f8e088",  # 真鍮（光）
    "P": "#f4ecd8",  # 帆布（光）
    "p": "#cdbd98",  # 帆布
    "q": "#8a7c66",  # 帆布（影）
    "R": "#c0442c",  # 赤（尾びれ・旗）
    "r": "#782420",  # 赤（影）
    "C": "#8af0ff",  # 灯り石（光）
    "c": "#2a9ab8",  # 灯り石
    "G": "#ffe9a0",  # 窓の明かり
    "I": "#5a5866",  # 鉄・影
}


class G:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.a = [["."] * w for _ in range(h)]

    def put(self, x, y, c):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < self.w and 0 <= y < self.h:
            self.a[y][x] = c

    def get(self, x, y):
        return self.a[y][x] if 0 <= x < self.w and 0 <= y < self.h else "."

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.put(x, y, c)

    def poly(self, pts, c, cond=None):
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        for y in range(int(min(ys)), int(max(ys)) + 1):
            for x in range(int(min(xs)), int(max(xs)) + 1):
                inside = False
                j = len(pts) - 1
                for i in range(len(pts)):
                    xi, yi = pts[i]; xj, yj = pts[j]
                    if (yi > y + 0.5) != (yj > y + 0.5):
                        if x + 0.5 < xi + (y + 0.5 - yi) * (xj - xi) / (yj - yi):
                            inside = not inside
                    j = i
                if inside and (cond is None or cond(x, y)):
                    self.put(x, y, c)

    def line(self, x0, y0, x1, y1, c):
        n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
        for i in range(n):
            t = i / max(1, n - 1)
            self.put(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, c)

    def disk(self, cx, cy, rx, ry, c):
        for y in range(int(cy - ry - 1), int(cy + ry + 2)):
            for x in range(int(cx - rx - 1), int(cx + rx + 2)):
                if ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2 <= 1:
                    self.put(x, y, c)

    def mirror(self):
        m = G(self.w, self.h)
        m.a = [list(reversed(r)) for r in self.a]
        return m

    def outline(self, color="K"):
        """透明に面したふち（外がわ1ドット）に縁の色を足す。"""
        add = []
        for y in range(self.h):
            for x in range(self.w):
                if self.a[y][x] == "." and any(self.get(x + dx, y + dy) not in (".", color) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    add.append((x, y))
        for (x, y) in add:
            self.a[y][x] = color
        return self

    def save(self, name, pal):
        rows = ["".join(r) for r in self.a]
        used = set("".join(rows)) - {"."}
        assert not (used - set(pal)), (name, used - set(pal))
        with open(os.path.join(HERE, f"{name}.txt"), "w") as f:
            f.write("\n".join(rows) + "\n")
        with open(os.path.join(HERE, f"pal-{name}.json"), "w") as f:
            json.dump({k: v for k, v in pal.items() if k in used}, f, ensure_ascii=False)
        return len(used)


# ===================================================================== 横から（右向き）40×40
def hull_side(g, x0, x1, top, depth, prow_rise):
    """細長い木の船体（横から）。へさき（右）は上へ反り、底はまるい。上のふちは真鍮。"""
    L = x1 - x0
    for x in range(x0, x1 + 1):
        t = (x - x0) / L
        tp = top - int(round(prow_rise * max(0.0, (t - 0.75) / 0.25) ** 1.6))      # へさきが反る
        bt = top + int(round(depth * math.sin(math.pi * min(1.0, 0.12 + t * 0.88))))  # 底のまるみ
        bt = max(bt, tp + 2)
        for y in range(tp, bt + 1):
            if y == tp:
                c = "h" if t < 0.5 else "b"
            elif y == tp + 1:
                c = "B"
            elif y == bt:
                c = "K"
            elif y >= bt - 1:
                c = "W"
            elif y == tp + 2:
                c = "o"
            else:
                c = "w" if (x * 3 + y * 7) % 11 else "W"
            g.put(x, y, c)
    for x in range(x0 + 2, x1 - 3, 3):
        g.put(x, top + depth - 1, "W")


def side(frame):
    g = G(40, 40)
    flap = -1 if frame else 0
    # ---- 奥の羽根（暗い帆布。手前の羽根より少し上・うしろ）
    g.poly([(17, 22), (11, 6 + flap), (6, 4 + flap), (10, 13), (13, 22)], "q")
    g.line(16, 21, 7, 5 + flap, "W")
    # ---- 船体
    hull_side(g, 6, 35, 22, 6, 4)
    for (x, y) in ((12, 25), (18, 25), (24, 25)):    # まるい窓（明かり）
        g.put(x, y, "G"); g.put(x + 1, y, "G"); g.put(x, y + 1, "b"); g.put(x + 1, y + 1, "B")
    # ---- 船首の空鳥の彫刻（金。羽を広げて前を向く）
    BIRD = ["..h..",
            ".hbh.",
            "hbbBh",
            ".bbB.",
            "..bBK",
            "...B."]
    for dy, row in enumerate(BIRD):
        for dx, ch in enumerate(row):
            if ch != ".":
                g.put(34 + dx, 13 + dy, ch)
    g.put(39, 15, "b"); g.put(38, 14, "h")
    # ---- 帆柱と旗（へさき寄り。なびく）
    g.line(29, 21, 29, 9, "W"); g.put(29, 8, "h")
    flag = [(29, 9), (23, 9), (25, 11), (22, 12), (29, 12)] if frame == 0 else [(29, 9), (22, 10), (24, 11), (22, 13), (29, 12)]
    g.poly(flag, "R"); g.line(23 + frame, 12, 28, 12, "r")
    # ---- 手前の羽根（帆布を張った木の骨組み。上へ反り、うしろへ流れる。骨のあいだの布は、骨の近くが明るい）
    root_a, root_b = (25, 22), (16, 22)
    ribs = [((25, 22), (17, 6 + flap)), ((23, 22), (5, 2 + flap)), ((20, 22), (6, 9)), ((18, 22), (8, 14))]
    g.poly([root_a, (17, 6 + flap), (5, 2 + flap), (6, 9), (8, 14), root_b], "p")
    for k in range(len(ribs) - 1):
        (ax, ay), (bx, by) = ribs[k]
        (cx_, cy_), (dx_, dy_) = ribs[k + 1]
        # 骨のすぐうしろ（光の当たる布）
        g.poly([(ax, ay), (bx, by), (bx - 2, by + 2), (ax - 1, ay)], "P")
    for (a, b) in ribs:
        g.line(a[0], a[1], b[0], b[1], "w")
    g.line(25, 22, 17, 6 + flap, "o")
    for (x, y) in ((6, 6), (7, 11), (9, 16), (12, 19)):
        g.put(x, y, ".")                                          # うしろのふちの切れこみ（波形）
    # ---- 尾びれ（赤）
    g.poly([(8, 22), (3, 14), (6, 14), (12, 22)], "R")
    g.line(4, 14, 8, 21, "r"); g.put(5, 14, "R")
    # ---- 丸い機関（船尾。真鍮の輪の中で灯り石が光り、羽根車が回る）
    cx, cy = 6, 26
    g.disk(cx, cy, 4.3, 4.6, "B")
    g.disk(cx, cy, 3.3, 3.6, "I")
    for y in range(int(cy - 5), int(cy + 5)):
        for x in range(int(cx - 5), int(cx + 5)):
            d = math.hypot((x + 0.5 - cx) / 4.3, (y + 0.5 - cy) / 4.6)
            if 0.78 < d <= 1 and (x + 0.5 - cx) + (y + 0.5 - cy) < -1:
                g.put(x, y, "h")
    if frame == 0:
        g.line(cx, cy - 3, cx, cy + 3, "p"); g.line(cx - 3, cy, cx + 3, cy, "q")
    else:
        g.line(cx - 2, cy - 2, cx + 2, cy + 2, "p"); g.line(cx - 2, cy + 2, cx + 2, cy - 2, "q")
    g.put(cx, cy, "C"); g.put(cx - 1, cy, "c"); g.put(cx, cy - 1, "C"); g.put(cx - 1, cy - 1, "C")
    for (x, y, c) in (((1, 31, "C"), (0, 29, "c"), (2, 33, "c")) if frame == 0 else ((0, 32, "c"), (1, 30, "C"), (0, 34, "C"))):
        g.put(x, y, c)
    return g.outline()


# ===================================================================== 前から（下向き）・うしろから（上向き）40×40
def wings_front(g, frame, cy):
    """左右に広げた二枚の羽根（前・うしろから見ると、上へ反ったV字）。骨と、骨のあいだの帆布。"""
    flap = -1 if frame else 0
    for side in (-1, 1):
        cx = 20
        root_in, root_out = (cx + side * 2, cy + 2), (cx + side * 3, cy - 2)
        tip = (cx + side * 19, cy - 13 + flap)
        mid = (cx + side * 15, cy - 4 + flap)
        g.poly([root_out, tip, mid, (cx + side * 9, cy + 1), root_in], "p")
        g.poly([root_out, tip, (cx + side * 16, cy - 9 + flap), (cx + side * 4, cy - 1)], "P")
        for t in (tip, mid, (cx + side * 9, cy + 1)):
            g.line(cx + side * 3, cy - 1, t[0], t[1], "w")
        g.line(root_out[0], root_out[1], tip[0], tip[1], "o")
        g.put(cx + side * 12, cy - 1 + flap, ".")                          # 波形の切れこみ


def front(frame, toward):
    g = G(40, 40)
    if toward:
        # うしろの機関（輪）が、船の上に少し見える
        g.disk(20, 15, 4.5, 4.5, "B"); g.disk(20, 15, 3.4, 3.4, "I")
        g.put(20, 15, "C"); g.put(19, 15, "c"); g.put(19, 14, "C")
        # 帆柱と旗
        g.line(20, 18, 20, 5, "W"); g.put(20, 4, "h")
        g.poly([(20, 5), (25 + frame, 6), (23, 7), (25 - frame, 8), (20, 8)], "R")
        wings_front(g, frame, 23)
        # 船体（手前へ近づくほど太い、まるい舳先）
        for y in range(20, 34):
            half = 2 + int(round(4.5 * math.sin(math.pi * (y - 20) / 16)))
            for x in range(20 - half, 20 + half):
                u = (x + 0.5 - 20) / max(1, half)
                c = "o" if u < -0.4 else ("w" if u < 0.4 else "W")
                if y == 20 or x in (20 - half, 20 + half - 1) and y < 30:
                    c = "b" if u < 0 else "B"
                g.put(x, y, c)
        g.put(17, 26, "G"); g.put(22, 26, "G")                              # 窓
        # 空鳥の彫刻（手前・まん中）
        BIRD = ["h...h", "hbhbB", ".bbB.", "..B.."]
        for dy, row in enumerate(BIRD):
            for dx, ch in enumerate(row):
                if ch != ".":
                    g.put(18 + dx, 31 + dy, ch)
    else:
        # うしろから: 船体は奥へ細くなり、へさきの鳥が上に小さく見える
        g.line(20, 18, 20, 5, "W"); g.put(20, 4, "h")
        g.poly([(20, 5), (15 - frame, 6), (17, 7), (15 + frame, 8), (20, 8)], "R")
        g.put(20, 9, "b"); g.put(19, 10, "h"); g.put(21, 10, "B")
        for y in range(11, 30):
            half = 1 + int(round(5 * (y - 11) / 18))
            for x in range(20 - half, 20 + half):
                u = (x + 0.5 - 20) / max(1, half)
                g.put(x, y, "o" if u < -0.4 else ("w" if u < 0.4 else "W"))
            g.put(20 - half, y, "b"); g.put(20 + half - 1, y, "B")
        wings_front(g, frame, 22)
        # 尾びれ（赤。まん中に立つ）
        g.poly([(19, 26), (20, 17), (21, 17), (22, 26)], "R"); g.line(21, 18, 21, 25, "r")
        # 機関（大きな輪。灯り石が光り、羽根車が回る）
        cx, cy = 20, 31
        g.disk(cx, cy, 5.5, 5.5, "B"); g.disk(cx, cy, 4.3, 4.3, "I")
        for y in range(cy - 6, cy + 6):
            for x in range(cx - 6, cx + 6):
                d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
                if 4.3 < d <= 5.5 and (x + 0.5 - cx) + (y + 0.5 - cy) < -2:
                    g.put(x, y, "h")
        for k in range(4):
            a = k * math.pi / 2 + (math.pi / 4 if frame else 0)
            g.line(cx, cy, cx + math.cos(a) * 3.6, cy + math.sin(a) * 3.6, "p" if k % 2 else "q")
        g.disk(cx, cy, 1.5, 1.5, "C"); g.put(cx, cy, "c")
        for (x, y) in (((17, 38), (23, 37)) if frame == 0 else ((18, 37), (22, 38))):
            g.put(x, y, "C")
    return g.outline()


def shadow():
    """地面に落ちる影（24×10）。羽根を広げた形の、ぼんやりした影（外がわは市松）。"""
    g = G(24, 10)
    for y in range(10):
        for x in range(24):
            d = math.hypot((x + 0.5 - 12) / 12.0, (y + 0.5 - 5) / 4.0)
            if d <= 0.6 or (d <= 1.0 and (x + y) % 2 == 0):
                g.put(x, y, "I")
    return g


def landed():
    """着陸中（48×48）。羽根をたたみ（うしろへ寝かせ）、そりの足で地面に立つ。機関は止まり、灯り石だけがほのかに光る。"""
    g = G(48, 48)
    s = side(0)
    # 地面の影（市松）
    for y in range(40, 46):
        for x in range(0, 48):
            d = math.hypot((x + 0.5 - 24) / 21.0, (y + 0.5 - 43) / 3.0)
            if d <= 0.7 or (d <= 1.0 and (x + y) % 2 == 0):
                g.put(x, y, "I")
    for y in range(40):
        for x in range(40):
            if s.a[y][x] != ".":
                g.put(x + 4, y + 6, s.a[y][x])
    # そりの足とはしご
    for x in (16, 32):
        g.rect(x, 37, x + 1, 41, "W"); g.put(x, 37, "o")
    g.rect(11, 42, 38, 42, "K"); g.rect(11, 41, 38, 41, "w")
    g.line(27, 36, 30, 41, "K")
    return g


if __name__ == "__main__":
    for f in (0, 1):
        side(f).save(f"airship-right-{f}", PAL)
        side(f).mirror().save(f"airship-left-{f}", PAL)
        front(f, True).save(f"airship-down-{f}", PAL)
        front(f, False).save(f"airship-up-{f}", PAL)
    shadow().save("airship-shadow", PAL)
    landed().save("airship-landed", PAL)
    print("ok")
