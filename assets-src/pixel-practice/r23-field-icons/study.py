"""フィールドの町・塔・洞窟・祠のアイコンの練習（2026-10-05、人間の指示「フィールド上の町、塔、洞窟、祠のドット絵をちょっと学んできて」）。

学んだこと（くわしくは docs/design/field-icons-study.md）を、4つの練習の絵で試す。どれも一から描いたオリジナルで、参考にした素材の絵は写していない。
  1. 黒い縁取りをやめ、縁はその物の色のいちばん暗い色で（地面の絵となじませる）
  2. 真横ではなく「斜め上から見下ろす」見え方（屋根・塔の上・岩山の上の面が見える）
  3. 光は左上から。左上の面が明るく、右下の面が暗い。1つの素材に5〜6段の色
  4. 岩・石垣・瓦は「かたまり」で描く（1ドットの点をばらまかない）
  5. 足もとの影（ゲームでは、絵の下にコードで半透明の影を敷く。ここではプレビューだけで試す）
出力: town / tower / cave / shrine の .txt と pal-*.json（48×48）、study-preview.png（今のアイコンと並べた比較）
"""
import json
import math
import os
import random

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
L = (-0.6, -0.75, 0.55)          # 光の向き（左上・手前から）
_n = math.sqrt(sum(c * c for c in L))
L = tuple(c / _n for c in L)


class Grid:
    def __init__(self, w=48, h=48):
        self.w, self.h = w, h
        self.a = np.full((h, w), ".", dtype="<U1")

    def put(self, x, y, c):
        x, y = int(x), int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            self.a[y, x] = c

    def get(self, x, y):
        return self.a[y, x] if 0 <= x < self.w and 0 <= y < self.h else "."

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.put(x, y, c)

    def save(self, name, pal):
        with open(os.path.join(HERE, f"{name}.txt"), "w") as f:
            f.write("\n".join("".join(r) for r in self.a) + "\n")
        with open(os.path.join(HERE, f"pal-{name}.json"), "w") as f:
            json.dump(pal, f, ensure_ascii=False)
        used = set("".join("".join(r) for r in self.a)) - {"."}
        assert not (used - set(pal)), used - set(pal)


def tone(ramp, v):
    """0〜1 の明るさを、ramp（暗→明の記号の並び）の1つに"""
    v = max(0.0, min(0.999, v))
    return ramp[int(v * len(ramp))]


def outline_dark(g, ramp_of):
    """透明に面したふちを、その色の素材のいちばん暗い色に（黒い縁取りの代わり）"""
    a = g.a.copy()
    for y in range(g.h):
        for x in range(g.w):
            c = a[y, x]
            if c == ".":
                continue
            edge = any(g.get(x + dx, y + dy) == "." for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
            if edge and c in ramp_of:
                r = ramp_of[c]
                # 下と右のふちはいちばん暗く、上と左のふちは1段だけ暗く（光が当たる側）
                lit_side = g.get(x - 1, y) == "." or g.get(x, y - 1) == "."
                shade_side = g.get(x + 1, y) == "." or g.get(x, y + 1) == "."
                k = r.index(c)
                a[y, x] = r[0] if shade_side else r[max(0, k - 1)] if lit_side else c
    g.a = a


# ===================================================================== 洞窟（岩のかたまりの小山と、暗い口）
def cave():
    g = Grid()
    R = "abcdef"                          # 岩: 暗→明
    pal = {"a": "#2a2622", "b": "#454038", "c": "#635c50", "d": "#857c6a", "e": "#a89e86", "f": "#ccc2a6",
           "k": "#0c0a09", "K": "#1c1713", "J": "#2e2620", "m": "#3e5a2c", "M": "#5e8a3a", "N": "#86b44c"}
    rnd = random.Random(7)
    cx, cy, rx, ry = 24, 27, 21, 17      # 小山（横長のだ円のドーム）
    seeds = []
    for _ in range(38):
        x = rnd.uniform(cx - rx, cx + rx); y = rnd.uniform(cy - ry, cy + ry + 6)
        seeds.append((x, y, rnd.uniform(0.85, 1.25)))
    for y in range(48):
        for x in range(48):
            u, v = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
            if y > cy + 12:
                v = (y + 0.5 - cy) / (ry + 20)      # すそは横に広がる
            d = u * u + v * v
            if d > 1 or y > 44:
                continue
            nz = math.sqrt(max(0.0, 1 - d))
            dome = -u * L[0] * 0.9 + -v * L[1] * 0.9 + nz * L[2]     # 山ぜんたいの明るさ
            # いちばん近い岩（かたまり）と、2番目との差＝岩のすき間
            ds = sorted(((x + 0.5 - sx) ** 2 + ((y + 0.5 - sy) * 1.35) ** 2) / s for sx, sy, s in seeds)
            gap = math.sqrt(ds[1]) - math.sqrt(ds[0])
            sx, sy, s = min(seeds, key=lambda p: ((x + 0.5 - p[0]) ** 2 + ((y + 0.5 - p[1]) * 1.35) ** 2) / p[2])
            local = -((x + 0.5 - sx) * 0.06 + (y + 0.5 - sy) * 0.09)   # 岩1つの中でも左上が明るい
            val = 0.42 + dome * 0.42 + local
            if gap < 0.38:
                val = min(val, 0.3)                                    # すき間は暗い
            g.put(x, y, tone(R, val))
    # 口（下のまんなか。上がまるいアーチ、奥へ行くほど暗い）
    mx, mtop, mbot, mr = 24, 28, 42, 7
    for y in range(mtop, mbot + 1):
        for x in range(mx - mr - 1, mx + mr + 2):
            yy = y - (mtop + mr)
            inside = (yy >= 0 and abs(x + 0.5 - mx) <= mr) or math.hypot(x + 0.5 - mx, yy) <= mr
            if inside:
                depth = math.hypot(x + 0.5 - mx, (y - mbot) * 0.8) / (mr + 2)
                g.put(x, y, "k" if depth < 0.75 else "K")
    # 口のふちの石（上の縁は明るい石、左のふちに光、右のふちは影）
    for y in range(mtop - 2, mbot + 1):
        for x in range(mx - mr - 3, mx + mr + 4):
            yy = y - (mtop + mr)
            d = math.hypot(x + 0.5 - mx, min(0, yy))
            ring = (mr + 0.3 < abs(x + 0.5 - mx) <= mr + 2.2 and yy >= 0) or (yy < 0 and mr + 0.3 < d <= mr + 2.2)
            if ring and g.get(x, y) not in ("k", "K", "."):
                g.put(x, y, "e" if x < mx and yy < 2 else ("b" if x > mx else "d"))
    for x in range(mx - mr, mx + mr + 1):
        if g.get(x, mtop + mr + 1) in "kK":
            pass
    g.put(mx - 3, mbot, "J"); g.put(mx - 2, mbot, "J"); g.put(mx + 3, mbot - 1, "J")   # 口の床の小石
    # 岩山のすその草（かたまりで）
    for (tx, ty) in ((6, 41), (10, 43), (38, 42), (42, 40), (15, 44), (33, 44)):
        for (dx, dy, c) in ((0, 0, "M"), (1, 0, "N"), (-1, 0, "m"), (0, -1, "N"), (1, 1, "m"), (0, 1, "m"), (-1, 1, "m")):
            if g.get(tx + dx, ty + dy) != "k":
                g.put(tx + dx, ty + dy, c)
    outline_dark(g, {c: R for c in R})
    g.save("cave", pal)
    return g, pal


# ===================================================================== 塔（斜め上から見た丸い塔。上の面と、のこぎりの歯の胸壁が見える）
def tower():
    g = Grid()
    S = "abcdef"                          # 石: 暗→明
    pal = {"a": "#2c2a34", "b": "#46424e", "c": "#625d6a", "d": "#837d88", "e": "#a69fa6", "f": "#cbc5c4",
           "w": "#1a1820", "y": "#ffd870", "Y": "#fff4c0", "r": "#7a2a24", "R": "#b8483a", "h": "#e07a5a",
           "p": "#4a3a2c", "P": "#6a5440", "g": "#3e5a2c", "G": "#5e8a3a"}
    cx, r = 24, 10.5
    top_y, base_y = 13, 43                  # 上の面のだ円の中心・足もとのだ円の中心
    ry = 4.0                               # だ円のつぶれ（見下ろす角度）
    # 足もとの土台（少し広い）
    for y in range(base_y - 3, base_y + 4):
        for x in range(48):
            u = (x + 0.5 - cx) / (r + 2.5)
            if abs(u) <= 1 and (y + 0.5 - base_y) <= ry * math.sqrt(max(0, 1 - u * u)) + 0.5:
                g.put(x, y, tone(S, 0.45 - u * 0.35 - (0.15 if y > base_y + 1 else 0)))
    # 円柱（横に、左から光。石の段は 4 ドットごと、目地は段ごとにずらす）
    for y in range(top_y, base_y + 1):
        for x in range(48):
            u = (x + 0.5 - cx) / r
            if abs(u) > 1:
                continue
            bottom = base_y - 2 + ry * math.sqrt(max(0, 1 - u * u)) * 0.7
            if y > bottom:
                continue
            nx = u; nz = math.sqrt(max(0, 1 - u * u))
            val = 0.45 + (-nx * L[0] + nz * L[2]) * 0.5
            course = (y - top_y) // 4
            if (y - top_y) % 4 == 0:
                val -= 0.2                             # 段の目地
            else:
                ang = math.asin(max(-1, min(1, u)))
                off = 0.35 if course % 2 else 0.0
                if int((ang + off) * 2.6) != int((ang + off + 0.09) * 2.6):
                    val -= 0.15                        # 縦の目地（まわりこむので、はしほど細かい）
            g.put(x, y, tone(S, val))
    # 窓（縦長。上がまるい。中の明かり）
    for (wx, wy) in ((24, 20), (19, 29), (28, 30)):
        for y in range(wy, wy + 5):
            for x in (wx, wx + 1):
                g.put(x, y, "w")
        g.put(wx, wy + 3, "y"); g.put(wx + 1, wy + 4, "y")
        g.put(wx - 1, wy + 5, "f" if wx < 26 else "d"); g.put(wx, wy + 5, "e"); g.put(wx + 1, wy + 5, "e"); g.put(wx + 2, wy + 5, "c")
    # 扉（木。まるいアーチ）
    for y in range(36, 44):
        for x in range(21, 27):
            if y > 37 or abs(x + 0.5 - 24) < 2.5:
                g.put(x, y, "P" if x < 24 else "p")
    g.put(25, 40, "y")
    # 上の面（だ円）: 胸壁（歯）のふちと、内がわの床
    for y in range(0, top_y + 6):
        for x in range(48):
            u = (x + 0.5 - cx) / (r + 1.2)
            vy = (y + 0.5 - top_y) / (ry + 0.6)
            if u * u + vy * vy <= 1:
                inner = ((x + 0.5 - cx) / (r - 1.8)) ** 2 + ((y + 0.5 - top_y) / (ry - 1.2)) ** 2
                if inner <= 1:
                    g.put(x, y, "c" if (y + 0.5 - top_y) < 0 else "b")      # 内がわの床（奥の壁の影）
                else:
                    g.put(x, y, tone(S, 0.82 - u * 0.3 + (0.08 if vy < 0 else -0.05)))
    # 歯（ふちの上に、たてに2ドット立つ石。奥の歯は小さく）
    for k in range(14):
        ang = k / 14 * 2 * math.pi
        if k % 2:
            continue
        x = cx + math.cos(ang) * (r + 0.2)
        y = top_y + math.sin(ang) * (ry + 0.1)
        front = math.sin(ang) > 0
        h = 3 if front else 2
        for dy in range(h):
            for dx in (0, 1):
                top = dy == h - 1
                g.put(x + dx, y - dy, tone(S, (0.95 if top else 0.6) - (x - cx) / r * 0.3 - dx * 0.08))
    # 旗（上の面のまんなかから）
    for y in range(3, 13):
        g.put(cx, y, "p")
    for (x, y, c) in ((25, 3, "R"), (26, 3, "R"), (27, 3, "h"), (25, 4, "R"), (26, 4, "R"), (27, 4, "R"), (28, 4, "h"), (25, 5, "r"), (26, 5, "r"), (27, 5, "R"), (25, 6, "r")):
        g.put(x, y, c)
    # 足もとの草
    for (tx, ty) in ((11, 45), (36, 45), (14, 46), (33, 46)):
        g.put(tx, ty, "G"); g.put(tx + 1, ty, "g"); g.put(tx, ty - 1, "G")
    outline_dark(g, {c: S for c in S})
    g.save("tower", pal)
    return g, pal


# ===================================================================== 町（低い石垣に囲まれた家々を、斜め上から）
def town():
    g = Grid()
    S = "abcdef"                          # 石垣
    O = "ABCDE"                           # だいだいの屋根
    T = "GHIJ"                            # 青緑の屋根
    W = "uvw"                             # しっくいの壁
    pal = {"a": "#2c2a30", "b": "#47434c", "c": "#655f66", "d": "#86807e", "e": "#a8a294", "f": "#ccc6b2",
           "A": "#5a2414", "B": "#8a3a20", "C": "#b8542a", "D": "#de7c42", "E": "#f2a874",
           "G": "#1a3e46", "H": "#2a6068", "I": "#3e8a8e", "J": "#6ab8b2",
           "u": "#7a6a56", "v": "#b4a486", "w": "#e2d6b6",
           "k": "#1a140e", "y": "#ffd870",
           "t": "#1c3a20", "s": "#2c5a2c", "S": "#457a34", "q": "#68a242", "Q": "#94cc5c",
           "p": "#5a3e26", "P": "#8a6a42", "x": "#9a8a68", "X": "#c4b48a"}
    cx, cy, rx, ry = 24, 28, 22, 15
    # 町の中の地面（土の広場）
    for y in range(48):
        for x in range(48):
            if ((x + 0.5 - cx) / (rx - 2)) ** 2 + ((y + 0.5 - cy) / (ry - 2)) ** 2 <= 1:
                g.put(x, y, "x" if (x * 3 + y * 5) % 11 else "X")
    # 石垣（だ円の輪。上の面＋手前に見える側面。手前ほど側面が見える）
    for y in range(48):
        for x in range(48):
            e = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2
            e2 = ((x + 0.5 - cx) / (rx - 2.2)) ** 2 + ((y + 0.5 - cy) / (ry - 2.2)) ** 2
            if e <= 1 and e2 > 1:
                g.put(x, y, tone(S, 0.82 - (x - cx) / rx * 0.25 - (0.1 if y > cy else 0)))
            # 側面（下がわだけ、3ドットの高さ）
            for h in range(1, 4):
                eh = ((x + 0.5 - cx) / rx) ** 2 + ((y - h + 0.5 - cy) / ry) ** 2
                if y > cy and eh <= 1 and e > 1:
                    v = 0.5 - (x - cx) / rx * 0.3 - h * 0.05
                    if (x + (y // 2)) % 4 == 0:
                        v -= 0.2
                    g.put(x, y, tone(S, v))
    # 門（手前のまんなか。石垣を切って、木の門）
    for y in range(40, 47):
        for x in range(21, 28):
            g.put(x, y, "x" if y < 43 else g.get(x, y))
    for y in range(41, 46):
        g.put(20, y, "e"); g.put(21, y, "d"); g.put(27, y, "c"); g.put(28, y, "b")
    g.put(20, 40, "f"); g.put(21, 40, "f"); g.put(27, 40, "e"); g.put(28, 40, "d")

    def house(x0, y0, w, roof):
        """屋根（奥の面は細く明るい、手前の面は太く瓦の列）・手前の壁（扉と窓）・右の壁は影"""
        R = O if roof == "O" else T
        rd = 6          # 屋根の手前の面の高さ
        # 奥の屋根の面（2行）
        for x in range(x0 + 1, x0 + w - 1):
            g.put(x, y0, R[-1] if x < x0 + w - 3 else R[-2]); g.put(x, y0 + 1, R[-2])
        # 手前の屋根の面（瓦の列は2ドットごと、右へ暗く）
        for y in range(y0 + 2, y0 + 2 + rd):
            for x in range(x0, x0 + w):
                k = len(R) - 2 - (1 if (y - y0) % 2 == 1 else 0) - (1 if x >= x0 + w - 2 else 0)
                if (x - x0 + (y // 2)) % 4 == 0 and (y - y0) % 2 == 0:
                    k -= 1
                g.put(x, y, R[max(0, k)])
        g.rect(x0, y0 + 2 + rd, x0 + w - 1, y0 + 2 + rd, R[0])      # 軒の影
        # 壁
        wy0 = y0 + 3 + rd
        for y in range(wy0, wy0 + 5):
            for x in range(x0, x0 + w):
                g.put(x, y, "w" if x < x0 + w - 2 else "v")
        g.rect(x0, wy0 + 4, x0 + w - 1, wy0 + 4, "u")
        dx = x0 + w // 2 - 1
        g.rect(dx, wy0 + 1, dx + 1, wy0 + 4, "p")
        g.put(x0 + 1, wy0 + 1, "k"); g.put(x0 + 1, wy0 + 2, "y")
        if w > 7:
            g.put(x0 + w - 3, wy0 + 1, "k"); g.put(x0 + w - 3, wy0 + 2, "y")

    def tree(tx, ty):
        for y in range(ty - 5, ty + 2):
            for x in range(tx - 4, tx + 5):
                d = ((x + 0.5 - tx) / 4.2) ** 2 + ((y + 0.5 - (ty - 2)) / 3.6) ** 2
                if d <= 1:
                    v = 0.55 - (x - tx) * 0.09 - (y - ty + 2) * 0.1
                    if (x + y * 2) % 5 == 0:
                        v -= 0.15
                    g.put(x, y, tone("tsSqQ", v))
        g.put(tx, ty + 2, "p"); g.put(tx, ty + 3, "p")

    tree(9, 23); tree(39, 22)
    house(13, 12, 9, "T")
    house(25, 13, 10, "O")
    house(8, 26, 8, "O")
    house(31, 27, 9, "T")
    tree(24, 34)
    # 広場の井戸
    g.put(20, 37, "c"); g.put(21, 37, "d"); g.put(20, 38, "b"); g.put(21, 38, "c")
    outline_dark(g, {**{c: S for c in S}, **{c: O for c in O}, **{c: T for c in T}, **{c: "tsSqQ" for c in "tsSqQ"}})
    g.save("town", pal)
    return g, pal


# ===================================================================== 祠（石の基壇の上の小さな堂。屋根が大きく見え、灯の環のしるし）
def shrine():
    g = Grid()
    S = "abcdef"                          # 石
    V = "ABCD"                            # 屋根（青むらさきの石板）
    pal = {"a": "#2a2830", "b": "#45424c", "c": "#625e68", "d": "#837e86", "e": "#a8a2a6", "f": "#d0cac6",
           "A": "#24203c", "B": "#38325e", "C": "#524a86", "D": "#7a70b0",
           "g": "#8a6418", "G": "#e0b040", "h": "#f8d878",
           "k": "#141018", "o": "#ff9a3c", "O": "#ffe060",
           "m": "#3e5a2c", "M": "#5e8a3a", "N": "#86b44c"}
    cx = 24
    # 基壇（上の面＝明るい、手前の面＝暗い、2段）
    def slab(x0, x1, y0, depth, h):
        for y in range(y0, y0 + depth):
            for x in range(x0, x1 + 1):
                g.put(x, y, tone(S, 0.85 - (x - x0) / (x1 - x0) * 0.25 - (0.08 if (x + y) % 7 == 0 else 0)))
        for y in range(y0 + depth, y0 + depth + h):
            for x in range(x0, x1 + 1):
                v = 0.45 - (x - x0) / (x1 - x0) * 0.25
                if (x - x0 + (y % 2) * 3) % 6 == 0:
                    v -= 0.18
                g.put(x, y, tone(S, v))
    slab(4, 43, 30, 9, 5)
    slab(9, 38, 26, 6, 3)
    # 階段（手前のまんなか）
    for k in range(3):
        y = 39 + k * 2
        for x in range(18 - k, 31 + k):
            g.put(x, y, tone(S, 0.8 - (x - 18) / 13 * 0.2)); g.put(x, y + 1, tone(S, 0.4 - (x - 18) / 13 * 0.2))
    # 堂の壁（奥へ引っこんだ、暗い入口と、左右の石の柱）
    for y in range(17, 30):
        for x in range(13, 35):
            g.put(x, y, tone(S, 0.6 - (x - 13) / 22 * 0.3))
    for y in range(20, 30):
        for x in range(19, 29):
            g.put(x, y, "k" if y > 21 or abs(x + 0.5 - 24) < 4 else g.get(x, y))
    for y in range(17, 30):
        g.put(13, y, "e"); g.put(14, y, "f"); g.put(15, y, "d")
        g.put(32, y, "d"); g.put(33, y, "c"); g.put(34, y, "b")
    # 奥の灯（入口の中に、小さな火と環）
    g.put(24, 25, "O"); g.put(24, 24, "o"); g.put(23, 26, "g"); g.put(24, 26, "G"); g.put(25, 26, "g")
    # 屋根（大きく張り出す。上の面が見え、手前のふちは厚み）
    for y in range(7, 18):
        t = (y - 7) / 10
        half = 11 + t * 9
        for x in range(48):
            if abs(x + 0.5 - cx) <= half:
                u = (x + 0.5 - cx) / half
                v = 0.85 - t * 0.35 - u * 0.25
                if (y - 7) % 3 == 2:
                    v -= 0.22                      # 石板の段
                g.put(x, y, tone(V, v))
    for x in range(int(cx - 20), int(cx + 20)):
        g.put(x, 18, "B" if x < cx + 10 else "A"); g.put(x, 19, "A")
    for x in range(int(cx - 10), int(cx + 10)):
        g.put(x, 6, "D")
    # 屋根の上の、灯の環（三つの環。いちばん小さな環は欠ける）
    for (rr, c) in ((3.6, "G"), (2.2, "h")):
        for y in range(-6, 7):
            for x in range(-6, 7):
                if abs(math.hypot(x, y) - rr) < 0.55:
                    a = math.atan2(y, x)
                    if rr < 3 and -1.4 < a < -0.3:
                        continue
                    g.put(cx + x, 2 + y, c if x + y < 0 else "g")
    # 左右の火皿（石の柱の上で燃える）
    for bx in (7, 40):
        g.rect(bx, 24, bx + 1, 30, "d"); g.put(bx + 1, 25, "c"); g.put(bx + 1, 27, "c")
        g.rect(bx - 1, 23, bx + 2, 23, "G"); g.rect(bx - 1, 22, bx + 2, 22, "g")
        g.put(bx, 21, "o"); g.put(bx + 1, 21, "O"); g.put(bx, 20, "O"); g.put(bx + 1, 19, "o")
    # 草
    for (tx, ty) in ((5, 45), (42, 45), (9, 46), (37, 46)):
        g.put(tx, ty, "M"); g.put(tx + 1, ty, "N"); g.put(tx, ty + 1, "m")
    outline_dark(g, {**{c: S for c in S}, **{c: V for c in V}})
    g.save("shrine", pal)
    return g, pal


def preview(items, path, old=None):
    from PIL import Image, ImageDraw
    Z = 5
    grass = Image.open(os.path.join(HERE, "..", "..", "pipoya", "pipo-map001", "640x480", "pipo-map001.png")).convert("RGBA").crop((0, 0, 32, 32))
    cols = len(items)
    rows = 2 if old else 1
    W, H = cols * (48 * Z + 20) + 20, rows * (48 * Z + 40) + 20
    sheet = Image.new("RGBA", (W, H), (40, 40, 48, 255))
    dr = ImageDraw.Draw(sheet)

    def render(rows_, pal, at, shadow):
        bg = Image.new("RGBA", (48, 48))
        for y in range(0, 48, 32):
            for x in range(0, 48, 32):
                bg.paste(grass, (x, y))
        if shadow:   # 足もとの半透明の影（ゲームではコードで敷く予定）
            sh = Image.new("RGBA", (48, 48), (0, 0, 0, 0))
            ImageDraw.Draw(sh).ellipse((8, 38, 46, 47), fill=(10, 30, 10, 90))
            bg.alpha_composite(sh)
        im = Image.new("RGBA", (48, 48))
        for y, r in enumerate(rows_):
            for x, c in enumerate(r):
                if c in pal:
                    im.putpixel((x, y), tuple(int(pal[c][k:k + 2], 16) for k in (1, 3, 5)) + (255,))
        bg.alpha_composite(im)
        sheet.paste(bg.resize((48 * Z, 48 * Z), Image.NEAREST), at)

    for i, (name, g, pal) in enumerate(items):
        render(["".join(r) for r in g.a], pal, (20 + i * (48 * Z + 20), 20), True)
        dr.text((20 + i * (48 * Z + 20), 48 * Z + 24), f"new: {name}", fill=(255, 255, 255))
        if old and old[i]:
            d, n = old[i]
            rows_ = [l for l in open(os.path.join(HERE, "..", d, f"{n}.txt")).read().split("\n") if l]
            p = json.load(open(os.path.join(HERE, "..", d, f"pal-{n}.json")))
            render(rows_, p, (20 + i * (48 * Z + 20), 48 * Z + 60), False)
            dr.text((20 + i * (48 * Z + 20), 2 * 48 * Z + 64), f"now: {n}", fill=(255, 255, 255))
    sheet.save(path)


if __name__ == "__main__":
    items = [("town", *town()), ("tower", *tower()), ("cave", *cave()), ("shrine", *shrine())]
    preview(items, os.path.join(HERE, "study-preview.png"),
            old=[("r17-polish", "icon-village"), None, ("r17-polish", "icon-cave"), ("r17-polish", "icon-shrine")])
    print("ok")
