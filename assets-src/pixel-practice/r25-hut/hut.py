"""船大工の小屋（世界地図のアイコン 48×48）。2026-10-05、人間の指示「船をくれる人は小屋の方がいいか。小屋を丁寧に作って」。
斜め上から見下ろす見え方・光は左上。黒い縁はつけず、素材ごとのいちばん暗い色で縁どる。
板張りの小屋（瓦ぶきではなく、タールを塗った板屋根）・石の煙突と煙・明かりのついた窓・錨の看板の扉・
となりの差しかけ小屋の中に組みかけの小舟の骨組み・材木の山・ロープの輪・樽・灯の柱。既存作品の絵は写していない。
出力: icon-hut.txt / pal-icon-hut.json → tools/pixel-practice/editor-draw.mjs で確かめる。"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PAL = {
    "k": "#1c1612",  # いちばん暗い（すき間・扉の奥）
    "W": "#3e2618",  # 木（濃い影・縁）
    "w": "#6a4226",  # 木（影）
    "o": "#94603a",  # 木
    "O": "#bf8a52",  # 木（光）
    "R": "#2e3644",  # 屋根の板（影）
    "r": "#465264",  # 屋根の板
    "L": "#66768a",  # 屋根の板（光）
    "S": "#5e5a58",  # 石（影）
    "s": "#8c8680",  # 石
    "T": "#b8b0a4",  # 石（光）・煙
    "Y": "#ffd878",  # 窓の明かり
    "y": "#e89a40",  # 明かり（影）・灯
    "G": "#3d6e2c",  # 草（影）
    "g": "#62a040",  # 草
    "C": "#d8cfb8",  # ロープ・煙（光）
    "c": "#a89a7a",  # ロープ（影）
    "B": "#5a6a7a",  # 鉄（錨）
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

    def poly(self, pts, c):
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        for y in range(int(min(ys)), int(max(ys)) + 1):
            for x in range(int(min(xs)), int(max(xs)) + 1):
                inside = False
                j = len(pts) - 1
                for i in range(len(pts)):
                    xi, yi = pts[i]; xj, yj = pts[j]
                    if (yi > y + 0.5) != (yj > y + 0.5) and x + 0.5 < xi + (y + 0.5 - yi) * (xj - xi) / (yj - yi):
                        inside = not inside
                    j = i
                if inside:
                    self.put(x, y, c)

    def line(self, x0, y0, x1, y1, c):
        n = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
        for i in range(n):
            t = i / max(1, n - 1)
            self.put(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, c)


DARKEST = {"o": "W", "O": "W", "w": "W", "r": "R", "L": "R", "s": "S", "T": "S", "g": "G", "C": "c", "y": "w", "Y": "w"}


def hut():
    g = G(48, 48)
    # ---- 地面の影（右下へ）と、足もとの草
    for y in range(38, 46):
        for x in range(4, 47):
            d = ((x + 0.5 - 27) / 20) ** 2 + ((y + 0.5 - 41.5) / 3.6) ** 2
            if d <= 1:
                g.put(x, y, "G")
    # ---- 差しかけ小屋（右。柱と斜めの屋根。中に組みかけの小舟）
    g.rect(31, 24, 44, 38, "k")                                   # 中の暗がり
    for (x0, x1) in ((31, 31), (44, 44)):
        g.rect(x0, 24, x1, 38, "w")                               # 柱
    g.put(31, 24, "O"); g.put(44, 24, "o")
    # 組みかけの小舟（竜骨と、あばら骨のような肋材。台の上）
    g.rect(32, 36, 43, 36, "w"); g.rect(33, 37, 34, 38, "W"); g.rect(41, 37, 42, 38, "W")      # 台
    g.line(33, 35, 43, 34, "o")                                    # 竜骨
    for x in range(34, 43, 2):
        top = 28 + abs(x - 38) // 2
        g.line(x, 35, x - 1, top, "O" if x < 38 else "o")          # 肋材
        g.put(x + 1, top + 1, "w")
    g.line(33, 30, 43, 29, "w")                                    # 舷の板（1枚だけ張った）
    # 差しかけの屋根（板。小屋の壁から右へ下る）
    g.poly([(30, 18), (46, 21), (46, 25), (30, 23)], "r")
    for k in range(4):
        g.line(30, 19 + k, 46, 22 + k, "L" if k == 0 else ("r" if k < 3 else "R"))
    for x in range(32, 46, 3):
        g.line(x, 18 + (x - 30) * 3 // 16, x, 23 + (x - 30) * 2 // 16, "R")
    # ---- 母屋の壁（手前の面: 横板。左が光、右へ暗く）
    wx0, wx1, wy0, wy1 = 6, 30, 25, 38
    for y in range(wy0, wy1 + 1):
        for x in range(wx0, wx1 + 1):
            band = (y - wy0) % 3
            c = "O" if band == 0 else ("o" if band == 1 else "w")
            if x > 24 and band != 2:
                c = "o" if c == "O" else "w"
            if (x * 7 + (y // 3) * 11) % 13 == 0:
                c = "W"                                            # 板の継ぎ目
            g.put(x, y, c)
    g.rect(wx0, wy1, wx1, wy1, "W")
    for y in range(wy0, wy1 + 1):
        g.put(wx0, y, "O"); g.put(wx0 + 1, y, "o"); g.put(wx1, y, "W"); g.put(wx1 - 1, y, "w")     # 角柱
    g.rect(wx0, 37, wx1, 38, "S"); g.rect(wx0, 37, wx1, 37, "s")                              # 石の土台
    # 窓（明かり・十字の桟・木の鎧戸）
    g.rect(10, 28, 15, 32, "W")
    g.rect(11, 29, 14, 31, "Y"); g.put(12, 29, "y"); g.put(13, 31, "y")
    g.rect(12, 29, 12, 31, "w"); g.rect(11, 30, 14, 30, "w")
    g.rect(8, 28, 9, 32, "o"); g.rect(16, 28, 17, 32, "w"); g.put(8, 28, "O")
    g.rect(10, 33, 15, 33, "O")                                                               # 窓台
    # 扉（板戸・鉄の帯・取っ手）と、上の錨の看板
    g.rect(20, 28, 26, 37, "W")
    g.rect(21, 29, 25, 37, "w")
    for x in (22, 24):
        g.rect(x, 29, x, 37, "o")
    g.rect(21, 31, 25, 31, "B"); g.rect(21, 35, 25, 35, "B"); g.put(25, 33, "Y")
    g.rect(20, 25, 26, 27, "o"); g.rect(20, 25, 26, 25, "O"); g.rect(20, 27, 26, 27, "W")      # 看板
    for (x, y) in ((23, 25), (23, 26), (22, 26), (24, 26), (21, 27), (25, 27), (22, 27), (24, 27)):
        g.put(x, y, "B")                                                                       # 錨
    g.put(23, 25, "T")
    # ---- 母屋の屋根（板ぶき。手前の面が大きく見える。棟は横。軒が張り出す）
    rx0, rx1, ry0, ry1 = 3, 33, 8, 25
    for y in range(ry0, ry1 + 1):
        t = (y - ry0) / (ry1 - ry0)
        inset = int(round((1 - t) * 3))
        for x in range(rx0 + inset, rx1 - inset + 1):
            row = (y - ry0) // 3
            off = 3 if row % 2 else 0
            if (y - ry0) % 3 == 2:
                c = "R"                                               # 板の段の影
            elif (x + off) % 6 == 0:
                c = "R"                                               # 板の継ぎ目
            elif x < rx0 + inset + 9 and (y - ry0) % 3 == 0:
                c = "L"                                               # 左の光
            else:
                c = "r"
            if x > rx1 - inset - 4 and c == "r":
                c = "R" if (x + y) % 2 else "r"
            g.put(x, y, c)
    g.rect(rx0 + 3, ry0, rx1 - 3, ry0, "L")                           # 棟（光）
    g.rect(rx0 + 3, ry0 - 1, rx1 - 3, ry0 - 1, "W")                   # 棟木
    g.rect(rx0, ry1, rx1, ry1, "W")                                   # 軒の影
    g.rect(rx0, ry1 - 1, rx1, ry1 - 1, "o")                           # 鼻隠しの板
    # ---- 石の煙突（屋根の右うしろ）と煙
    g.rect(26, 3, 30, 12, "s")
    for y in range(3, 13):
        g.put(26, y, "T"); g.put(30, y, "S"); g.put(29, y, "S" if y % 3 == 0 else "s")
        if y % 3 == 0:
            g.rect(27, y, 28, y, "S")
    g.rect(25, 2, 31, 3, "T"); g.rect(25, 3, 31, 3, "s")
    for (cx, cy, rr) in ((32.5, 1.5, 2.2), (36.5, 2.5, 2.6), (40.5, 1.5, 1.8)):
        for y in range(0, int(cy + 4)):
            for x in range(int(cx - 3), int(cx + 4)):
                if math.hypot(x + 0.5 - cx, y + 0.5 - cy) <= rr:
                    g.put(x, y, "C" if (x + 0.5 - cx) + (y + 0.5 - cy) < 0.5 else "T")
    # ---- 左: 丸太の山（切り口の年輪が見える）と樽
    LOG = [".oO.", "oOwo", "owWw", ".ww."]
    for (lx, ly) in ((0, 36), (4, 36), (2, 33)):
        for dy, row in enumerate(LOG):
            for dx, ch in enumerate(row):
                if ch != ".":
                    g.put(lx + dx, ly + dy, ch)
    g.rect(1, 40, 7, 40, "W")
    g.rect(1, 26, 4, 31, "o"); g.rect(1, 26, 1, 31, "O"); g.rect(4, 26, 4, 31, "w")         # 樽
    g.rect(1, 27, 4, 27, "B"); g.rect(1, 30, 4, 30, "B"); g.rect(2, 25, 3, 25, "w"); g.rect(1, 32, 4, 32, "W")
    for (x, y, c) in ((8, 40, "C"), (9, 40, "C"), (10, 40, "c"), (7, 41, "C"), (11, 41, "c"), (8, 42, "c"), (9, 42, "c"), (10, 42, "c"), (9, 41, "W")):
        g.put(x, y, c)                                                # ロープの輪
    # ---- 灯の柱（扉の前・右）
    g.rect(28, 31, 28, 40, "W"); g.put(28, 31, "w")
    g.rect(27, 29, 29, 30, "y"); g.put(28, 29, "Y"); g.put(27, 28, "W"); g.put(29, 28, "W")
    # ---- 草のふさ（手前）
    for (x, y) in ((13, 42), (19, 43), (36, 41), (41, 42), (5, 41)):
        g.put(x, y, "g"); g.put(x + 1, y - 1, "g"); g.put(x + 2, y, "G")
    # ---- 縁: 透明に面したふちを、その素材のいちばん暗い色に
    a = [r[:] for r in g.a]
    for y in range(48):
        for x in range(48):
            c = a[y][x]
            if c != "." and c in DARKEST and any(g.get(x + dx, y + dy) == "." for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1))):
                lit = g.get(x - 1, y) == "." or g.get(x, y - 1) == "."
                if not lit:
                    a[y][x] = DARKEST[c]
    g.a = a
    rows = ["".join(r) for r in g.a]
    used = set("".join(rows)) - {"."}
    with open(os.path.join(HERE, "icon-hut.txt"), "w") as f:
        f.write("\n".join(rows) + "\n")
    with open(os.path.join(HERE, "pal-icon-hut.json"), "w") as f:
        json.dump({k: v for k, v in PAL.items() if k in used}, f, ensure_ascii=False)
    print("色数", len(used))


if __name__ == "__main__":
    hut()
