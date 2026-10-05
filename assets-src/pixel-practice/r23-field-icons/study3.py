"""フィールドのアイコンの勉強・3回目（2026-10-05、人間の指示「いいね、教会以外はもっと勉強してきて」）。

2回目の弱いところを直し（お城・雪の町・洞窟・特別な塔）、ゲームにあるほかのアイコンの種類（港町・村・湖の町・山の寺・遺跡・立ち石・
大樹・火山・渦・潜る場所・砂漠の野営地・浮き島・宮殿・小島4つ）も、同じ「ひとつの家族」に見えるきまりで練習する。
どれも一から考えたオリジナルの形で、参考の素材は写していない。くわしくは docs/design/field-icons-study.md の「3回目の勉強」。

3回目に足したきまり（家族のきまり）
  G. 色は1枚16色まで。すべての素材が「共通の縁の色 o」と「共通の穴の色 k」を使い、素材ごとの色は3〜4段だけ
  H. 色は全部この下の MASTER（家族のパレット）から選ぶ。同じ素材は、どの絵でも同じ色
  I. 光は左上、だ円のつぶれは 0.36（ER）。屋根・壁・岩の明るさの段の決め方も共通の道具（このファイルと study2.py）で
  J. 岩は「向きと大きさがばらばらの面」＋「ななめの割れ目」（rock）。レンガのように並べない
  K. 雪は丸いこぶ（半円の並び）で屋根にのせ、軒からまるいしずくを垂らす（snow_cap）
  L. 奥にあるものは細く暗く、手前にあるものは太く明るく（環・壁・石）。奥の物は先に描き、手前の物で隠す
出力: 21点の .txt / pal-*.json、study3-preview.png、study3-grounds.png、study3-world.png
"""
import json
import math
import os
import random

from study import Grid, tone, outline_dark
from study2 import cyl_light, cylinder, ellipse_top, cone, hip_roof, brick_face, top_face, parapet, ring_mark, to_img

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ER = 0.36            # だ円のつぶれ（縦÷横）。家族で共通

# ===================================================================== 家族のパレット（H）
MASTER = {
    "o": "#2b2631", "k": "#120e16",                                          # 共通の縁・共通の穴
    "a": "#4f4a4e", "b": "#7a726e", "c": "#a49a88", "d": "#d2c6a8",          # 石（あたたかい灰）
    "p": "#3a3150", "q": "#574a72", "r": "#7d6c98", "s": "#a998c0",          # 暗い石（宮殿・渦の針）
    "A": "#1e3c48", "B": "#2e6068", "C": "#4a8c8a", "D": "#80c0b0",          # 青緑の屋根
    "E": "#6a2820", "F": "#a4443a", "G": "#d26a4e", "H": "#f0a27c",          # 赤い屋根・布
    "w": "#4c3222", "x": "#7a5432", "y": "#ac7e4a",                          # 木
    "m": "#c9b893", "n": "#efe3c3",                                          # しっくいの壁
    "I": "#1c3a22", "J": "#2c5e30", "K": "#488a3a", "N": "#7cba52",          # 葉・草
    "Q": "#1a3a6e", "R": "#2a5e9e", "U": "#4a90cc", "X": "#a0d8f0",          # 水
    "i": "#a07c4a", "j": "#d2b07a", "l": "#f0dcaa",                          # 砂・わら
    "u": "#93a6c8", "v": "#c6d4ea", "z": "#f2f7ff",                          # 雪・雲・波の白
    "L": "#ffd068", "M": "#fff4c8",                                          # 灯
    "g": "#b0802a", "h": "#f2ca56",                                          # 金（環のしるし）
    "f": "#c23c1c", "t": "#ff8a2c",                                          # 溶岩
    "O": "#2c82a0", "P": "#78d8e8", "e": "#e8fcff",                          # 不思議な光（青）
    "W": "#3c1e5c", "Y": "#8a52c0",                                          # 不思議な光（むらさき）
}
STONE = "oabcd"; DARK = "opqrs"; TEAL = "oABCD"; RED = "oEFGH"; WOOD = "owxy"; LEAF = "oIJKN"
WATER = "oQRUX"; SAND = "oijl"; SNOW = "ouvz"; GOLD = "ogh"; LAVA = "oftLM"; MAGIC = "oOPe"; WALL = "omn"
RAMPS = [STONE, DARK, TEAL, RED, WOOD, LEAF, WATER, SAND, SNOW, WALL]


def ramp_of(*ramps):
    out = {}
    for r in ramps or RAMPS:
        for c in r:
            if c != "o":
                out.setdefault(c, r)
    return out


def save(g, name, limit=16):
    used = sorted(set("".join("".join(r) for r in g.a)) - {"."})
    pal = {c: MASTER[c] for c in used}
    assert len(pal) <= limit, (name, len(pal), used)
    g.save(name, pal)
    return name, g, pal


def ell(x, y, cx, cy, rx, ry):
    return ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2


def fill_ellipse(g, cx, cy, rx, ry, fn):
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            d = ell(x, y, cx, cy, rx, ry)
            if d <= 1:
                c = fn(x, y, (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry, d)
                if c:
                    g.put(x, y, c)


# ===================================================================== 岩（J）: 向きと大きさがばらばらの面＋ななめの割れ目
def rock(g, inside, box, ramp=STONE, seed=1, n=18, cracks=0.45, base=0.0, light=(0.32, 0.22)):
    """inside(x,y) が真の所を岩にする。box=(x0,y0,x1,y1)。面は異方性のボロノイ（向き・伸び・重みが面ごとにちがう）"""
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    pts = []
    tries = 0
    while len(pts) < n and tries < 5000:
        tries += 1
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        if inside(int(x), int(y)):
            th = rnd.uniform(0, math.pi)
            pts.append((x, y, math.cos(th), math.sin(th), rnd.uniform(1.3, 2.3), rnd.uniform(0.7, 1.5), rnd.uniform(-0.12, 0.12)))
    cell = {}
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if not inside(x, y):
                continue
            best, bi = 1e9, 0
            for i, (sx, sy, c, s, st, w, _) in enumerate(pts):
                dx, dy = x + 0.5 - sx, (y + 0.5 - sy) * 1.2
                a, b = dx * c + dy * s, -dx * s + dy * c
                d = (a * a + (b * st) ** 2) / w
                if d < best:
                    best, bi = d, i
            cell[(x, y)] = bi
    w_, h_ = max(1, x1 - x0), max(1, y1 - y0)
    for (x, y), i in cell.items():
        sx, sy, *_rest, tilt = pts[i]
        nx, ny = (sx - x0) / w_ - 0.5, (sy - y0) / h_ - 0.5
        v = 0.6 - nx * 2 * light[0] - ny * 2 * light[1] + tilt + base
        v -= (x + 0.5 - sx) * 0.012 + (y + 0.5 - sy) * 0.02
        dn, rt = cell.get((x, y + 1), -1), cell.get((x + 1, y), -1)
        up, lf = cell.get((x, y - 1), -1), cell.get((x - 1, y), -1)
        if dn not in (i, -1) or rt not in (i, -1):
            v = min(v, 0.28)
        elif up not in (i, -1) or lf not in (i, -1):
            v += 0.18
        g.put(x, y, tone(ramp, v))
    # ななめの割れ目（大きい面の中だけ。右下へ3〜5ドット、左上どなりに光）
    area = {}
    for (x, y), i in cell.items():
        area[i] = area.get(i, 0) + 1
    for i, (sx, sy, *_r) in enumerate(pts):
        if area.get(i, 0) < 22 or rnd.random() > cracks:
            continue
        ln = rnd.randint(3, 5)
        dirx = 1 if rnd.random() < 0.6 else -1
        x, y = int(sx) - dirx, int(sy) - 1
        for k in range(ln):
            if cell.get((x, y)) != i:
                break
            g.put(x, y, ramp[1])                                   # 割れ目
            lx = x - 1
            if cell.get((lx, y)) == i and g.get(lx, y) in ramp:
                g.put(lx, y, ramp[min(len(ramp) - 1, ramp.index(g.get(lx, y)) + 1)])   # 割れ目の左どなりは光
            if k % 2 == 0:
                x += dirx
            y += 1
    return cell


# ===================================================================== 雪（K）: 丸いこぶ＋しずく
def snow_cap(g, x0, x1, ytop, depth, under=None, drip=False):
    """x0..x1 の、ytop から depth 行に雪。下のふちは、5ドットはばの丸いこぶ（下へふくらむ半円）。
    こぶの中は明るく、こぶの右下の1ドットだけ影の色（とがった歯にしない）"""
    for x in range(x0, x1 + 1):
        ph = ((x - x0) % 5) - 2.0                       # -2..2
        bump = 1.3 * math.sqrt(max(0.0, 1 - (ph / 2.6) ** 2))
        d = depth + bump
        yb = int(ytop + d)
        for y in range(ytop, yb + 1):
            cur = g.get(x, y)
            if cur == "." or (under and cur not in under):
                continue
            rel = (x - x0) / max(1, x1 - x0)
            c = "z" if rel < 0.6 else "v"
            if y == yb and ph > 0.5:
                c = "u"                                   # こぶの右下だけ影
            elif y == yb:
                c = "v"
            g.put(x, y, c)


# ===================================================================== 葉のかたまり
def foliage(g, lobes, ramp=LEAF, hi=True):
    """lobes=[(cx,cy,r)...] 奥（上）から。房ごとに左上が明るく、下右は暗い。房の重なりのふちに影"""
    for (bx, by, rr) in lobes:
        for y in range(int(by - rr) - 1, int(by + rr) + 2):
            for x in range(int(bx - rr) - 1, int(bx + rr) + 2):
                u, v = (x + 0.5 - bx) / rr, (y + 0.5 - by) / rr
                d = u * u + v * v
                if d <= 1:
                    val = 0.62 - u * 0.25 - v * 0.3
                    if d > 0.72 and (u + v) > 0.35:
                        val = 0.22                       # 房の右下のふち（影）
                    if hi and (u + 0.35) ** 2 + (v + 0.4) ** 2 < 0.09:
                        val = 0.95                       # 房の左上の光（かたまり）
                    g.put(x, y, tone(ramp, val))


# ===================================================================== 家（屋根の形を3種類）
def house(g, x0, y0, w, style, roof, wall="nm", rd=5, wh=4, door="x", win=True, chimney=False, snow=False, shadow=None):
    """style: 'hip'＝寄棟 / 'side'＝棟が横（手前の屋根の面が見える）/ 'gable'＝妻（三角の壁）がこちらを向く。
    roof は暗→明の色の並び（先頭は o）。返り値は壁の下のy"""
    x1 = x0 + w - 1
    if style == "hip":
        hip_roof(g, x0, x1, y0, y0 + rd, roof, wb=1.6, ws=1.0)
        top = y0 + rd + 2
    elif style == "side":
        for x in range(x0 + 1, x1):
            g.put(x, y0, roof[-1])                                       # 奥の面（細く明るい）
        for y in range(y0 + 1, y0 + rd + 1):
            for x in range(x0, x1 + 1):
                v = 0.62 - (x - x0) / w * 0.2 - (0.18 if (y - y0) % 2 == 0 else 0)
                g.put(x, y, tone(roof, v))
        for x in range(x0, x1 + 1):
            g.put(x, y0 + rd + 1, roof[0])
        top = y0 + rd + 2
    else:   # gable: 屋根の左の面（明るい）と右の面（暗い）が奥へのび、手前に三角の壁
        cx = (x0 + x1) / 2
        for y in range(y0, y0 + rd):
            for x in range(x0, x1 + 1):
                v = 0.85 if x + 0.5 < cx else 0.4
                if abs(x + 0.5 - cx) < 0.8:
                    v = 0.99
                if (y - y0) % 2 == 1:
                    v -= 0.12
                g.put(x, y, tone(roof, v))
        gh = max(2, w // 2 - 1)                                           # 三角の壁の高さ
        for k in range(gh):
            y = y0 + rd + k
            half = (k + 1) * (w / 2) / gh
            for x in range(x0, x1 + 1):
                dx = x + 0.5 - cx
                if abs(dx) <= half - 1:
                    g.put(x, y, wall[0] if dx < 0 else wall[1])
                elif abs(dx) <= half + 0.3:
                    g.put(x, y, roof[-2] if dx < 0 else roof[1])         # 破風（屋根のふち）
                elif y == y0 + rd + k and abs(dx) <= w / 2:
                    g.put(x, y, tone(roof, 0.85 if dx < 0 else 0.4))
        top = y0 + rd + gh
    for y in range(top, top + wh):
        for x in range(x0, x1 + 1):
            g.put(x, y, wall[0] if x < x1 - 1 else wall[1])
    g.rect(x0, top + wh - 1, x1, top + wh - 1, wall[1])
    dx = x1 - 3 if w > 7 else x0 + w // 2            # 扉は右より（まん中に置くと、窓と合わせて顔に見える）
    g.rect(dx, top + 1, dx + (1 if w > 9 else 0), top + wh - 1, door)
    if win:
        g.rect(x0 + 1, top + 1, x0 + 2 if w > 9 else x0 + 1, top + 1, "L")
        if w > 11:
            g.put(x0 + 5, top + 1, "L")
    if chimney:
        cxm = x1 - 2
        for y in range(y0 - 3, y0 + 2):
            g.put(cxm, y, "c"); g.put(cxm + 1, y, "b")
        g.put(cxm, y0 - 4, "o"); g.put(cxm + 1, y0 - 4, "o")
    if snow:
        under = set(roof)
        snow_cap(g, x0, x1, y0, max(1, rd // 2), under=under | set("ouvz"))
    if shadow:   # 家が地面に落とす影（右と下に1ドット。地面の色の1段暗い色）
        for y in range(y0 + 1, top + wh + 1):
            if g.get(x1 + 1, y) not in ".":
                g.put(x1 + 1, y, shadow)
        for x in range(x0 + 1, x1 + 2):
            if g.get(x, top + wh) not in ".":
                g.put(x, top + wh, shadow)
    return top + wh


# ===================================================================== 小島の土台（4つの小島で共通）
def islet_base(g, cx=24, cy=31, rx=20, ry=None, top="grass", cliff=5, seed=3):
    ry = ry or rx * ER
    T = "oJKN" if top == "grass" else SAND
    # がけ（だ円の手前半分を下へ cliff ドット。岩の面で）
    def inside(x, y):
        u = (x + 0.5 - cx) / rx
        if abs(u) > 1:
            return False
        bow = ry * math.sqrt(1 - u * u)
        return cy <= y + 0.5 <= cy + bow + cliff
    rock(g, inside, (int(cx - rx) - 1, int(cy), int(cx + rx) + 1, int(cy + ry + cliff) + 1), STONE, seed=seed, n=10, cracks=0.3, base=-0.08)
    # 上の面（だ円。ふちは1段明るい、まん中はかたまりの模様）
    fill_ellipse(g, cx, cy, rx, ry, lambda x, y, u, v, d: tone(T, (0.95 if (d > 0.72 and v < 0.2) else 0.62) - u * 0.15 - (0.2 if d > 0.8 and v > 0.3 else 0)
                                                           - (0.16 if ((x // 3) + (y // 2) * 2) % 7 == 0 and d < 0.7 else 0)))
    # 波の白（水ぎわの手前に、決まった間かくの短い線。点はまかない）
    for k in range(0, 360, 1):
        a = math.radians(k)
        if math.sin(a) < 0.15:
            continue
        x = cx + math.cos(a) * (rx + 1.5)
        y = cy + math.sin(a) * (ry + 1.2) + cliff + 1
        if int(k / 9) % 3 != 2:
            g.put(x, y, "z" if math.cos(a) < 0.3 else "X")
    for x in (int(cx - rx) - 1, int(cx + rx) + 1):
        g.put(x, cy + 2, "z")
    return T


# ===================================================================== 1) お城（本当の斜め上からの見え方。中庭が見える）
def castle3():
    g = Grid(64, 64)
    S = STONE
    # 奥の壁（上の面＋中庭がわの面。高さは3ドットだけ＝見下ろす角度が急）
    top_face(g, 7, 56, 14, 16, S, 0.86)
    parapet(g, 7, 56, 14, S, 4)
    brick_face(g, 7, 56, 17, 19, S, 0.42, seed=1)
    # 中庭（草）と、門から天守への石の道、井戸
    for y in range(20, 45):
        for x in range(9, 55):
            c = "c" if ((x // 4) + (y // 2) * 3) % 5 == 0 else "b"     # 石だたみ（明るい敷石をかたまりで）
            if y < 22:
                c = "a"                                                    # 奥の壁の影
            g.put(x, y, c)
    for (tx, ty) in ((15, 35), (48, 35), (15, 26), (48, 26)):             # 中庭の4本の木（四すみの花壇）
        g.rect(tx - 3, ty + 2, tx + 3, ty + 4, "J")
        fill_ellipse(g, tx, ty, 3.6, 3.0, lambda x, y, u, v, d: "o" if d > 0.75 and u + v > 0.4 else ("K" if u + v < -0.2 else "J"))
    for y in range(29, 45):
        for x in range(29, 35):
            g.put(x, y, "d" if (x + y // 2) % 3 else "c")
    for y in range(29, 33):
        for x in range(13, 51):
            if g.get(x, y) in "JK" and 29 <= y <= 30:
                g.put(x, y, "d" if (x // 3 + y) % 3 else "c")              # 天守の前の広場
    # 左右の壁の上の面
    top_face(g, 5, 8, 14, 45, S, 0.86); top_face(g, 55, 58, 14, 45, S, 0.66)
    for y in range(14, 46, 4):                                            # 左右の壁の胸壁（すき間の影）
        g.put(8, y, "a"); g.put(55, y, "a")
    # 天守（奥のまん中。寄棟の屋根＋手前の壁。壁の下＝中庭に影）
    hip_roof(g, 20, 43, 3, 16, TEAL, wb=1.5, ws=1.0)
    brick_face(g, 20, 43, 18, 28, S, 0.6, seed=2)
    g.rect(20, 18, 43, 18, "a")
    for i, wx in enumerate((23, 27, 36, 40)):
        g.rect(wx, 21, wx, 23, "k")
        if i in (1, 2):
            g.put(wx, 22, "L")
        g.put(wx, 24, "d")
    for y in range(23, 29):                                                # 天守の入口（アーチ）
        for x in range(30, 34):
            if y > 23 or 31 <= x <= 32:
                g.put(x, y, "k")
    ring_mark(g, 32, 20, "h", "k", "h")
    for bx in (25, 37):                                                    # 垂れ幕
        for y in range(19, 26):
            g.put(bx, y, "G"); g.put(bx + 1, y, "F")
        g.put(bx, 26, "F")
    for x in range(44, 47):
        for y in range(19, 30):
            if g.get(x, y) in "bc":
                g.put(x, y, "a")                                           # 天守の右の影
    for x in range(20, 45):
        if g.get(x, 29) in "bcd":
            g.put(x, 29, "b")
    # 奥の角の塔（とんがり屋根）
    for tx in (7, 56):
        cylinder(g, tx, 5.5, 9, 17, 2.0, S, shade=-0.04)
        ellipse_top(g, tx, 9, 6.0, 2.2, S)
        cone(g, tx, 9, 6.6, 8, 2.2, TEAL)
        g.rect(tx - 1, 12, tx - 1, 14, "k")
        g.put(tx, 0, "a"); g.put(tx + 1, 0, "G"); g.put(tx + 2, 0, "F")
    # 手前の壁（低い。中庭が見えるように、手前の面は5ドット）
    top_face(g, 8, 55, 44, 46, S, 0.86)
    parapet(g, 8, 55, 45, S, 4)
    brick_face(g, 8, 55, 47, 51, S, 0.55, seed=0)
    # 手前の角の塔（平らな屋上＋胸壁。とんがり屋根にしないので中庭が隠れない）
    for tx in (7, 56):
        cylinder(g, tx, 6.2, 38, 52, 2.3, S)
        ellipse_top(g, tx, 38, 6.8, 2.5, S, inner=2.2, merlons=12)
        g.rect(tx - 1, 43, tx - 1, 45, "k"); g.put(tx - 1, 44, "L")
    # 門の建物（手前に張り出す）
    top_face(g, 26, 37, 40, 43, S, 0.92)
    parapet(g, 26, 37, 41, S, 3)
    brick_face(g, 26, 37, 44, 55, S, 0.58, seed=3)
    for y in range(48, 56):
        for x in range(29, 35):
            if y > 49 or 30 <= x <= 33:
                g.put(x, y, "k" if (x - 29) % 2 or y > 53 else "o")
    for x in range(28, 36):
        if g.get(x, 47) != "k":
            g.put(x, 47, "d" if x < 32 else "c")
    for y in range(56, 62):                                                # 門前の道
        for x in range(30 - (y - 56) // 2, 34 + (y - 56) // 2 + 1):
            g.put(x, y, "c" if (x + y) % 3 else "b")
    outline_dark(g, ramp_of(STONE, TEAL, RED, "oJK"))
    return save(g, "castle3")


# ===================================================================== 2) 特別な塔（上の段を太く、窓を大きく、環に奥行き）
def spire3():
    W, H = 64, 112
    g = Grid(W, H)
    S = STONE
    cx = 32
    tiers = [(13.5, 78, 103), (11, 55, 78), (9.5, 30, 55)]
    rings = [(24, 90, False), (20, 66, False), (10.5, 12, True)]

    def ring(rx, cy, broken, front):
        ry = rx * 0.3
        for k in range(1440):
            a = k / 1440 * 2 * math.pi
            if broken and 0.45 < a < 1.25:
                continue
            s, c = math.sin(a), math.cos(a)
            if (s > 0) != front:
                continue
            x, y = cx + c * rx, cy + s * ry
            if front:
                thick = 3 if s > 0.75 else 2                               # 手前は太く明るい
                g.put(x, y, "h" if c < 0.5 else "g")
                for t in range(1, thick):
                    g.put(x, y + t, "g" if t < thick - 1 or s < 0.75 else "o")
            else:
                g.put(x, y, "g" if c < -0.3 else "o")                     # 奥は細く暗い

    for rx, cy, br in rings:
        ring(rx, cy, br, False)
    for (rx, cy, h) in ((22, 104, 4), (18, 101, 3)):
        cylinder(g, cx, rx, cy, cy + h, rx * 0.3, S, course=0, joints=False, shade=-0.05)
        ellipse_top(g, cx, cy, rx, rx * 0.3, S)
    for (r, yt, yb) in tiers:
        cylinder(g, cx, r, yt, yb, r * ER, S, course=4)
        ellipse_top(g, cx, yt, r + 1.6, (r + 1.6) * ER, S)
    for i in range(len(tiers) - 1):
        r, yt, yb = tiers[i + 1]
        cylinder(g, cx, r, yt, yb, r * ER, S, course=4)
    # 下の2段の窓（1つずつ、互いちがい）
    for (r, yt, yb), wx in zip(tiers[:2], (cx - 8, cx + 4)):
        wy = int((yt + yb) / 2) - 3
        g.rect(wx, wy, wx + 1, wy + 3, "k"); g.put(wx, wy + 2, "O")
        g.put(wx, wy + 4, "d"); g.put(wx + 1, wy + 4, "c")
    # 上の段: 大きなアーチの窓3つ（3×6。中が青く光る）と、窓の下の張り出し
    r, yt, yb = tiers[2]
    for wx in (cx - 7, cx - 1, cx + 5):
        for y in range(yt + 7, yt + 14):
            for x in range(wx, wx + 3):
                if y > yt + 7 or x == wx + 1:
                    inner = (x == wx + 1 and y > yt + 9)
                    g.put(x, y, ("P" if wx < cx else "O") if inner else "k")
        g.put(wx, yt + 14, "d"); g.put(wx + 1, yt + 14, "d"); g.put(wx + 2, yt + 14, "c")
    ellipse_top(g, cx, yt + 17, r + 1.2, (r + 1.2) * ER * 0.6, S)
    # てっぺん: 胸壁つきの上の面と、4本の小さな尖塔
    ellipse_top(g, cx, yt, r + 1.0, (r + 1.0) * ER, S, inner=2.4, merlons=14)
    for px_ in (cx - 8, cx + 7):
        for y in range(yt - 6, yt + 1):
            g.put(px_, y, "c" if px_ < cx else "a"); g.put(px_ + 1, y, "b" if px_ < cx else "o")
        g.put(px_, yt - 7, "d"); g.put(px_ + 1, yt - 7, "b")
    # 扉
    for y in range(93, 107):
        for x in range(cx - 3, cx + 3):
            if y > 95 or cx - 2 <= x <= cx + 1:
                g.put(x, y, "k")
    for y in range(95, 107):
        g.put(cx - 4, y, "O"); g.put(cx + 3, y, "O")
    for x in range(cx - 2, cx + 2):
        g.put(x, 94, "P")
    g.put(cx - 3, 95, "P"); g.put(cx + 2, 95, "O")
    # 浮かぶ光の石（芯＋まわり1段）
    for y in range(2, 24):
        t = (y - 2) / 21
        half = 4.4 * math.sin(t * math.pi) ** 0.8 + 0.2
        for x in range(cx - 5, cx + 6):
            u = (x + 0.5 - cx) / max(0.5, half)
            if abs(u) <= 1:
                g.put(x, y, "e" if (u < -0.1 and t < 0.75) else ("P" if u < 0.45 else "O"))
    for (x, y) in ((cx - 7, 20), (cx + 7, 5)):
        g.put(x, y, "P"); g.put(x - 1, y, "O"); g.put(x + 1, y, "O"); g.put(x, y - 1, "O"); g.put(x, y + 1, "O")
    for (x, y) in ((cx - 12, 99), (cx - 11, 100), (cx - 10, 100), (cx + 9, 101), (cx + 10, 101)):
        g.put(x, y, "K" if x < cx else "J")
    for rx, cy, br in rings:
        ring(rx, cy, br, True)
    outline_dark(g, ramp_of(STONE))
    return save(g, "spire3")


# ===================================================================== 3) 雪の町（家の形をばらばらに、雪はまるく）
def town3():
    g = Grid()
    S = "obcd"
    cx, cy, rx, ry = 24, 29, 22.5, 15
    for y in range(48):
        for x in range(48):
            if ell(x, y, cx, cy, rx - 2, ry - 2) <= 1:
                road = 23 <= x <= 25 or 34 <= y <= 35
                g.put(x, y, "u" if road else ("z" if ((x // 4) + (y // 3)) % 6 == 0 else "v"))   # 広場は踏まれた雪（屋根の雪より1段暗く）
    for y in range(48):
        for x in range(48):
            e = ell(x, y, cx, cy, rx, ry)
            e2 = ell(x, y, cx, cy, rx - 2.2, ry - 2.2)
            if e <= 1 and e2 > 1:
                g.put(x, y, "z" if (x + y) % 5 else "v") if y < cy else g.put(x, y, tone(S, 0.86 - (x - cx) / rx * 0.22))
            for h in range(1, 4):
                eh = ell(x, y - h, cx, cy, rx, ry)
                if y > cy and eh <= 1 and e > 1:
                    v = 0.55 - (x - cx) / rx * 0.3 - h * 0.05
                    if (x + (y // 3) * 2) % 5 == 0 or h == 3:
                        v -= 0.2
                    g.put(x, y, tone(S, v))
    RR, TT = "oFG", "oBC"
    # 鐘の塔（まん中の奥）
    for y in range(6, 24):
        for x in range(21, 28):
            g.put(x, y, tone(S, 0.75 - (x - 21) * 0.08 - (0.2 if (y - 6) % 3 == 2 else 0)))
    for y in range(0, 7):
        half = 0.6 + y * 0.75
        for x in range(19, 30):
            if abs(x + 0.5 - 24.5) <= half:
                g.put(x, y, ("z" if x < 25 else "v") if y < 3 else ("C" if x < 24 else "B"))
    g.rect(23, 9, 25, 12, "k"); g.put(24, 10, "L"); g.put(24, 11, "L")
    # 家（形も大きさもばらばら）
    house(g, 3, 4, 12, "gable", TT, rd=4, wh=4, snow=True, shadow="u")            # 奥の左: 妻がこちらを向く大きな家
    house(g, 30, 6, 15, "side", RR, rd=4, wh=4, chimney=True, snow=True, shadow="u")  # 奥の右: 横長の家・えんとつ
    house(g, 2, 21, 11, "hip", RR, rd=4, wh=4, snow=True, shadow="u")             # 手前の左: 寄棟
    house(g, 14, 24, 8, "gable", RR, rd=3, wh=3, snow=True, shadow="u")           # 手前の中: 小さな妻の家
    house(g, 29, 21, 15, "hip", TT, rd=5, wh=4, snow=True, shadow="u")            # 手前の右: 大きな寄棟
    # 門
    for y in range(41, 48):
        for x in range(21, 28):
            if g.get(x, y) != "." or y < 47:
                g.put(x, y, "c" if (x + y) % 3 else "b")
    for y in range(40, 46):
        g.put(20, y, "d"); g.put(21, y, "c"); g.put(27, y, "b"); g.put(28, y, "o")
    g.put(20, 39, "z"); g.put(21, 39, "z"); g.put(27, 39, "v"); g.put(28, 39, "v")
    g.put(21, 38, "L"); g.put(27, 38, "L")
    outline_dark(g, ramp_of("obcd", RR, TT, SNOW, "omn"))
    return save(g, "town3")


# ===================================================================== 4) 洞窟（自然の岩山。ばらばらの面と割れ目）
def crag_mask(cx, peaks, base_y, rx, top_y):
    def inside(x, y):
        if y > base_y:
            return False
        xx = x + 0.5
        # からだ: すそが広いだ円の下半分＋上の半分
        body = ((xx - cx) / rx) ** 2 + ((y + 0.5 - base_y) / (base_y - top_y)) ** 2 <= 1
        if body:
            return True
        for (px_, py_, w) in peaks:
            if y >= py_ and abs(xx - px_) <= w * ((y - py_ + 1) / (base_y - py_ + 1)) ** 0.7 * 1.0 + 1.2:
                return True
        return False
    return inside


def cave3():
    g = Grid()
    inside = crag_mask(24, [(14, 6, 15), (28, 3, 16), (38, 11, 11)], 44, 22, 14)
    rock(g, inside, (1, 2, 47, 45), STONE, seed=21, n=22, cracks=0.6)
    # 口（ふちがでこぼこのアーチ。奥ほど暗い）
    for y in range(26, 45):
        for x in range(14, 34):
            ph = math.sin(y * 1.7) * 0.8
            half = 7.5 + ph
            top = 26 + ((x + 0.5 - 24) / 8) ** 2 * 6
            if abs(x + 0.5 - 24) <= half and y >= top:
                depth = math.hypot(x + 0.5 - 24, (y - 44) * 0.7)
                g.put(x, y, "k" if depth < 8.5 else "o")
    # 口の上のふち（明るい岩のひさし）
    for x in range(16, 32):
        y = int(26 + ((x + 0.5 - 24) / 8) ** 2 * 6) - 1
        if g.get(x, y) not in ".ko":
            g.put(x, y, "d" if x < 24 else "c")
    # 苔（上を向いた面に、かたまりで3つ）
    for (mx, my) in ((12, 14), (27, 8), (37, 18)):
        for (dx, dy, c) in ((0, 0, "N"), (1, 0, "K"), (2, 0, "K"), (0, 1, "K"), (1, 1, "J")):
            if g.get(mx + dx, my + dy) in "abcd":
                g.put(mx + dx, my + dy, c)
    # 口の床の石
    g.put(20, 44, "a"); g.put(21, 44, "b"); g.put(28, 43, "a")
    outline_dark(g, ramp_of(STONE, LEAF))
    return save(g, "cave3")


def mine3():
    g = Grid()
    inside = crag_mask(24, [(18, 5, 14), (32, 9, 12)], 43, 21, 12)
    rock(g, inside, (1, 2, 47, 44), STONE, seed=8, n=20, cracks=0.6, base=-0.03)
    for y in range(27, 44):
        for x in range(18, 30):
            g.put(x, y, "k" if (y > 29 and 19 < x < 28) else "o")
    for y in range(26, 44):
        g.put(17, y, "y"); g.put(18, y, "x"); g.put(19, y, "w")
        g.put(28, y, "x"); g.put(29, y, "w"); g.put(30, y, "o")
    for x in range(15, 33):
        g.put(x, 24, "y" if x < 30 else "x"); g.put(x, 25, "x" if x < 30 else "w"); g.put(x, 26, "w")
    g.put(15, 23, "x"); g.put(32, 23, "w")
    g.put(15, 29, "M"); g.put(15, 30, "L"); g.put(14, 30, "L"); g.put(15, 28, "w")
    for y in range(35, 47):
        t = (y - 35) / 11
        lx, rx_ = 21 - t * 4, 26 + t * 4
        if (y - 35) % 3 == 1:
            for x in range(int(lx) - 1, int(rx_) + 2):
                g.put(x, y, "x" if x < 24 else "w")
        g.put(lx, y, "d"); g.put(rx_, y, "c")
    # トロッコ（右に。箱の上の面が見える）
    for y in range(36, 42):
        for x in range(33, 41):
            g.put(x, y, ("c" if y < 38 else "b") if y < 40 else "a")
    g.rect(34, 37, 39, 37, "k"); g.put(34, 36, "d")
    for x in (34, 38):
        g.put(x, 42, "o"); g.put(x + 1, 42, "o")
    g.put(35, 36, "L")                                                 # 鉱石のかがやき
    outline_dark(g, ramp_of(STONE, WOOD))
    return save(g, "mine3")


# ===================================================================== 5) 港町（石の岸壁・桟橋・小舟・灯台）
def port3():
    g = Grid()
    S = "obcd"
    RR = "oFG"
    # 港の水（手前。だ円の入り江）
    fill_ellipse(g, 22, 42, 21, 6.5, lambda x, y, u, v, d: "U" if d < 0.55 else ("R" if d < 0.9 else "R"))
    for (x, y) in ((10, 41), (11, 41), (30, 44), (31, 44), (18, 45), (19, 45)):
        g.put(x, y, "X")                                                   # 水面の光（短い線）
    # 岸壁（上の面＋手前の面）
    for y in range(30, 33):
        for x in range(2, 46):
            g.put(x, y, "d" if y == 30 else "c")
    for y in range(33, 36):
        for x in range(2, 46):
            g.put(x, y, "b" if (x + (y - 33) * 3) % 6 else "o")
    # 桟橋（左へ水の上にのびる板）
    for y in range(36, 44):
        for x in range(8, 13):
            g.put(x, y, "c" if (y % 2) else "x")
        g.put(8, y, "x"); g.put(12, y, "w")
    g.rect(8, 44, 8, 45, "w"); g.rect(12, 44, 12, 45, "w")
    # 小舟（右。帆は白く大きく、船体は木）
    for y in range(40, 44):
        half = 7 - (y - 40)
        for x in range(int(31 - half), int(31 + half) + 1):
            g.put(x, y, "c" if y == 40 else ("x" if x < 31 + half - 2 else "w"))
    g.rect(30, 30 - 2, 30, 39, "w")
    for y in range(29, 39):
        for x in range(31, 31 + min(8, (y - 28))):
            g.put(x, y, "n" if x < 35 else "m")
    # 町の地面（石だたみ。家々が1つの台に乗ると「町」に見える）
    for y in range(13, 30):
        for x in range(1, 47):
            if ell(x, y, 24, 30, 23, 17) <= 1:
                g.put(x, y, "c" if ((x // 3) + (y // 2) * 2) % 5 == 0 else "b")
    # 家（奥に3軒。形をかえる）
    house(g, 2, 6, 11, "gable", RR, rd=4, wh=4, door="w")
    house(g, 14, 9, 12, "side", RR, rd=4, wh=4, door="w", chimney=True)
    house(g, 27, 12, 9, "hip", RR, rd=4, wh=4, door="w")
    # 灯台（右の奥。白と赤の帯。いちばん高い）
    cylinder(g, 41, 3.6, 7, 29, 1.3, "obcdn", course=0, joints=False)
    for y in range(8, 29):
        if (y // 5) % 2 == 1:
            for x in range(38, 45):
                if g.get(x, y) in "obcdn":
                    g.put(x, y, "G" if x < 41 else "F")
    g.rect(39, 2, 43, 6, "o"); g.rect(40, 3, 42, 5, "L")
    g.rect(38, 1, 44, 1, "F"); g.rect(39, 0, 43, 0, "G")
    outline_dark(g, ramp_of(S, RR, WOOD, "omn"))
    return save(g, "port3")


# ===================================================================== 6) 村（わら屋根の家・風車・畑・木）
def village3():
    g = Grid()
    TH = SAND                                                            # わら屋根
    # 村の地面（こげ茶の土の広場。わら屋根の黄色と分けるため、屋根より暗い色。家々が同じ地面に乗る。ふちは1段暗く、明るい土はかたまりで）
    fill_ellipse(g, 22, 30, 21, 13, lambda x, y, u, v, d: "w" if d > 0.85 else ("y" if ((x // 4) + (y // 3) * 2) % 7 == 0 else "x"))
    # 畑（右手前。うねは2ドットごと、上の面が明るい）
    for y in range(30, 44):
        for x in range(26, 46):
            if x - 26 + (44 - y) * 0.2 < 20:
                g.put(x, y, "K" if (y % 3) == 0 else ("J" if y % 3 == 1 else "x"))
    for y in range(30, 45):
        g.put(25, y, "y" if y % 2 else "w")                               # 柵
    for x in range(25, 46, 3):
        g.put(x, 44, "w"); g.put(x, 43, "y")
    # 風車（左の奥。しっくいの胴＋わらの帽子＋十字の羽）
    for y in range(9, 30):
        half = 3.2 + (y - 9) * 0.07
        for x in range(4, 18):
            u = (x + 0.5 - 10.5) / half
            if abs(u) <= 1:
                g.put(x, y, "n" if u < 0.2 else "m")
    g.rect(10, 25, 11, 29, "w")
    cone(g, 10.5, 10, 4.8, 5, 1.6, TH)
    for k in range(-9, 10):                                               # 羽（ななめの十字。板の色）
        for (x, y) in ((10 + k, 10 + k), (10 + k, 10 - k)):
            if 0 <= x < 48 and 0 <= y < 48:
                g.put(x, y, "y" if k < 0 else "x")
                if abs(k) > 3:
                    g.put(x + (1 if (k > 0) == (y > 10) else -1), y, "n" if k < 0 else "m")
    g.rect(10, 9, 11, 10, "w")
    # 家（わら屋根3軒。形と大きさをかえる）
    house(g, 18, 6, 12, "hip", TH, rd=5, wh=4, door="w")
    house(g, 32, 10, 12, "gable", TH, rd=4, wh=4, door="w")
    house(g, 5, 31, 10, "side", TH, rd=4, wh=4, door="w")
    # 木（かたまり）
    foliage(g, [(19, 32, 4.2), (22, 35, 3.6)])
    g.rect(20, 38, 20, 40, "w")
    outline_dark(g, ramp_of(TH, WOOD, LEAF, "omn"))
    return save(g, "village3")


# ===================================================================== 7) 湖の町（水の上の高床の家と、板の道）
def lake3():
    g = Grid()
    fill_ellipse(g, 24, 29, 23.5, 16.5, lambda x, y, u, v, d: "R" if d > 0.85 else ("U" if (x // 3 + y) % 7 else "X"))
    # 板の道（十字）
    for y in range(24, 46):
        for x in range(22, 26):
            g.put(x, y, "y" if y % 2 else "x")
    for y in range(32, 35):
        for x in range(4, 44):
            g.put(x, y, "y" if x % 2 else "x")
    for x in range(4, 44):
        g.put(x, 35, "w")
    # 高床の家（柱が水に立つ。柱の足もとに波の白）
    def stilt_house(x0, y0, w, style):
        bot = house(g, x0, y0, w, style, "oBCD", rd=4, wh=4, door="w")
        for px_ in (x0 + 1, x0 + w - 2):
            for y in range(bot, bot + 3):
                g.put(px_, y, "w")
            g.put(px_ - 1, bot + 3, "z"); g.put(px_ + 1, bot + 3, "z")
    stilt_house(3, 6, 11, "hip")
    stilt_house(30, 5, 13, "gable")
    stilt_house(5, 21, 9, "gable")
    stilt_house(31, 21, 11, "hip")
    # 葦（右手前と左手前に、かたまりで）
    for (x, y) in ((40, 40), (41, 39), (42, 41), (6, 41), (7, 40)):
        g.put(x, y, "K"); g.put(x, y + 1, "w")
    g.put(44, 22, "L")
    outline_dark(g, ramp_of("oBCD", WOOD, "omn"))
    return save(g, "lake3")


# ===================================================================== 8) 山の寺（雪をいただく岩山の中腹に、寺と石段）
def temple3():
    g = Grid()
    def inside(x, y):
        xx = x + 0.5
        h = 2 + abs(xx - 26) * 1.55 + (2 if xx < 20 else 0)
        return y >= h and y <= 45 and 1 <= x <= 46
    cell = rock(g, inside, (1, 2, 46, 45), STONE, seed=31, n=20, cracks=0.4)
    # 雪（高い所の面を、雪の色に置きかえる。ふちは丸く）
    for (x, y), i in cell.items():
        lim = 13 + math.sin(x * 0.9) * 1.5
        if y < lim:
            c = g.get(x, y)
            g.put(x, y, {"o": "u", "a": "u", "b": "v", "c": "z", "d": "z"}.get(c, c))
    # 寺の台（岩を切った平らな面）
    for y in range(24, 28):
        for x in range(9, 40):
            g.put(x, y, "d" if y == 24 else "c")
    for y in range(28, 30):
        for x in range(9, 40):
            g.put(x, y, "b")
    # 寺（赤い柱の堂。寄棟の屋根の上に金の環）
    hip_roof(g, 13, 35, 11, 18, "oFG", wb=1.5, ws=1.0)
    for y in range(20, 25):
        for x in range(14, 35):
            g.put(x, y, "n" if x < 33 else "m")
    for x in (14, 19, 29, 34):
        g.rect(x, 20, x, 24, "F")
    g.rect(22, 21, 26, 24, "k"); g.put(15, 21, "L"); g.put(33, 21, "L")
    for (x, y) in ((23, 6), (24, 6), (25, 6), (22, 7), (26, 7), (22, 8), (26, 8), (23, 9), (24, 9), (25, 9)):
        g.put(x, y, "h")
    g.put(24, 8, "g"); g.rect(24, 10, 24, 10, "g")
    # 石段（台から下へ、まっすぐ）
    for k in range(8):
        y = 30 + k * 2
        for x in range(21 - k // 2, 28 + k // 2):
            g.put(x, y, "d"); g.put(x, y + 1, "b")
    outline_dark(g, ramp_of(STONE, SNOW, "oFG"))
    return save(g, "temple3")


# ===================================================================== 9) 遺跡（高さのちがう柱・折れた柱・横たわる柱・はり）
def ruin3():
    g = Grid()
    S = STONE
    # 基壇（2段）
    top_face(g, 3, 44, 33, 38, S, 0.86); brick_face(g, 3, 44, 39, 42, S, 0.5, seed=1)
    top_face(g, 8, 40, 30, 32, S, 0.92); brick_face(g, 8, 40, 33, 34, S, 0.55, seed=2)
    # 柱（丸い柱。奥から。高さはばらばら）
    def column(cx, top, bot, broken=False):
        cylinder(g, cx, 2.6, top, bot, 0.9, S, course=3, joints=False)
        if broken:
            for x in range(int(cx - 3), int(cx + 4)):
                t = top + (1 if (x * 7) % 3 == 0 else 0) + (2 if x > cx + 1 else 0)
                for y in range(top - 2, t):
                    if g.get(x, y) in S:
                        g.put(x, y, ".")
            g.put(cx - 2, top, "d"); g.put(cx - 1, top, "d"); g.put(cx, top + 1, "c")
        else:
            for x in range(int(cx - 3), int(cx + 4)):
                g.put(x, top - 1, "d" if x < cx + 1 else "c"); g.put(x, top, "b")   # 柱頭
    column(11, 6, 31)
    column(20, 9, 31)
    column(29, 17, 31, broken=True)
    column(38, 12, 31, broken=True)
    # はり（左の2本の柱にかかる石）
    top_face(g, 7, 24, 3, 4, S, 0.95); brick_face(g, 7, 24, 5, 6, S, 0.5, course=9, brick=8)
    # 横たわる柱（手前。円の切り口が見える）
    for y in range(36, 40):
        for x in range(26, 40):
            g.put(x, y, tone(S, 0.75 - (y - 36) * 0.15))
    fill_ellipse(g, 25, 38, 2, 2.2, lambda x, y, u, v, d: "d" if d < 0.5 else "c")
    fill_ellipse(g, 15, 37, 2.5, 1.6, lambda x, y, u, v, d: tone(S, 0.8 - v * 0.3))     # くずれた石
    # つた（かたまり）
    for (x, y) in ((10, 14), (11, 15), (10, 16), (12, 17), (20, 22), (21, 23), (37, 20), (38, 21)):
        g.put(x, y, "K"); g.put(x, y + 1, "J")
    g.put(10, 13, "N"); g.put(20, 21, "N")
    outline_dark(g, ramp_of(S, LEAF))
    return save(g, "ruin3")


# ===================================================================== 10) 立ち石（だ円に並ぶ石。奥は小さく、手前は大きい。まん中に光る環の石）
def stones3():
    g = Grid()
    S = STONE
    cx, cy, rx, ry = 24, 29, 18, 10
    fill_ellipse(g, cx, cy, 7, 3.4, lambda x, y, u, v, d: "d" if v < -0.2 else ("c" if d < 0.8 else "b"))   # まん中の平たい石
    for y in range(int(cy) + 2, int(cy) + 4):
        for x in range(cx - 6, cx + 7):
            if ell(x, y - 2, cx, cy, 7, 3.4) <= 1 and ell(x, y, cx, cy, 7, 3.4) > 1:
                g.put(x, y, "a")
    for k in range(240):                                                   # 光る環の彫り（欠けた環）
        a = k / 240 * 2 * math.pi
        if 0.4 < a < 1.2:
            continue
        g.put(cx + math.cos(a) * 3.6, cy + math.sin(a) * 1.7, "P" if math.cos(a) < 0.3 else "O")
    g.put(cx, cy, "e")
    stones = []
    for k in range(8):
        a = (k + 0.5) / 8 * 2 * math.pi + 0.39
        if abs(a - math.pi / 2) < 0.4:
            continue                                                       # 手前は入口としてあける（まん中の石が隠れない）
        stones.append((math.sin(a), cx + math.cos(a) * rx, cy + math.sin(a) * ry, k))
    for (sn, x, y, k) in sorted(stones):
        h = int(9 + sn * 2 + (k % 3) - (k % 2))
        w = 6 + (1 if sn > 0 else 0)
        x0 = int(x - w / 2)
        for yy in range(int(y) - h, int(y) + 1):
            taper = 1 if yy < int(y) - h + 3 else 0                      # 上は少し細い
            for xx in range(x0 + taper, x0 + w - (taper if k % 2 else 0)):
                t = (xx - x0) / (w - 1)
                v = 0.78 - t * 0.45
                if yy <= int(y) - h + 1:
                    v = 0.95 - t * 0.2                                     # 上の面（明るい）
                if (xx == x0 or xx == x0 + w - 1) and yy == int(y) - h:
                    continue                                               # 角を丸く
                g.put(xx, yy, tone(S, v))
        g.put(x0 + 1, int(y) - h + 3, "K"); g.put(x0 + 1, int(y) - h + 4, "J")   # 苔
    outline_dark(g, ramp_of(S, LEAF))
    return save(g, "stones3")


# ===================================================================== 11) 大樹（大きな房の葉・太い幹と根・うろの灯）
def bigtree3():
    g = Grid()
    # 幹と根
    for y in range(24, 45):
        t = (y - 24) / 20
        half = 4.5 + (t ** 3) * 9
        for x in range(48):
            u = (x + 0.5 - 24) / half
            if abs(u) <= 1:
                v = 0.7 - u * 0.4
                if (x + y // 4) % 4 == 0:
                    v -= 0.2                                               # 樹皮のたてのすじ
                g.put(x, y, tone(WOOD, v))
    for (rx0, d) in ((10, -1), (38, 1)):                                    # 根の先
        for k in range(5):
            g.put(rx0 + d * k // 2, 44 - k // 3, "x")
    for y in range(34, 41):                                                # うろ（中に灯）
        for x in range(22, 27):
            if y > 35 or 23 <= x <= 25:
                g.put(x, y, "k")
    g.put(24, 38, "L"); g.put(24, 37, "M")
    # 葉（大きな房を7つ。奥から）
    foliage(g, [(12, 12, 9), (35, 11, 9.5), (24, 7, 9), (8, 22, 7), (40, 22, 7), (18, 22, 8), (31, 22, 8.5)])
    outline_dark(g, ramp_of(LEAF, WOOD))
    return save(g, "bigtree3")


# ===================================================================== 12) 火山（上の面＝火口が見える。溶岩の流れ、けむりは丸いかたまり3つ）
def volcano3():
    g = Grid()
    def inside(x, y):
        xx = x + 0.5
        return y >= 14 + 0 * xx and y <= 45 and abs(xx - 24) <= 8 + (y - 14) * 0.52
    rock(g, inside, (1, 13, 46, 45), STONE, seed=41, n=18, cracks=0.4, base=-0.18)
    # 火口（だ円。ふちは明るい岩、中は溶岩）
    fill_ellipse(g, 24, 14, 9, 3.3, lambda x, y, u, v, d: ("b" if v < 0 else "a") if d > 0.6 else ("t" if d > 0.3 else "L"))
    # 溶岩の流れ（火口から手前へ2本。ゆれる線、芯は明るい）
    def flow(x, y0, y1, drift, wide):
        for y in range(y0, y1):
            x += drift
            xi = int(x + math.sin(y * 0.45) * 1.2)
            w = wide if y < (y0 + y1) / 2 else max(1, wide - 1)
            for k in range(w):
                g.put(xi + k, y, "L" if (k == 0 and y < y0 + 6) else "t")
            g.put(xi + w, y, "f")
        return x
    xm = flow(23.0, 16, 30, -0.05, 3)          # 太い流れが途中で2つに分かれる
    flow(xm, 30, 44, -0.35, 2)
    flow(xm + 2, 30, 42, 0.3, 1)
    # けむり（丸いかたまり3つ。下が暗い）
    for (bx, by, r) in ((24, 9, 4.0), (27, 5.5, 3.6), (23, 3, 2.8), (30, 2.5, 2.4)):   # 右へ流れるけむり（丸いかたまり4つ）
        fill_ellipse(g, bx, by, r, r * 0.85, lambda x, y, u, v, d: "d" if u + v < -0.1 else ("c" if d < 0.8 or u + v < 0.6 else "b"))
    outline_dark(g, ramp_of(STONE, SNOW))
    return save(g, "volcano3")


# ===================================================================== 13) 渦（うずまく海と、まん中から立つ暗い石の針）
def vortex3():
    g = Grid()
    cx, cy, rx, ry = 24, 36, 23, 10
    def swirl(x, y, u, v, d):
        r = math.sqrt(d)
        a = math.atan2(v, u)
        arm = (a + r * 7.0) % (2 * math.pi / 3)
        if r < 0.18:
            return "k"
        if arm < 0.45:
            return "z" if r > 0.5 else "X"
        if arm < 1.1:
            return "U" if r > 0.35 else "R"
        return "R" if r > 0.4 else "Q"
    fill_ellipse(g, cx, cy, rx, ry, swirl)
    # 石の針（まん中から上へ。左が明るい。先にむらさきの光）
    for y in range(4, 37):
        t = (y - 4) / 32
        half = 1 + t * 3.6
        for x in range(cx - 6, cx + 7):
            u = (x + 0.5 - cx) / half
            if abs(u) <= 1:
                g.put(x, y, tone(DARK, 0.7 - u * 0.45 - (0.15 if (y % 5 == 0) else 0)))
    for (x, y, c) in ((24, 2, "Y"), (24, 3, "s"), (23, 3, "Y"), (25, 3, "W"), (24, 1, "W"), (22, 4, "W"), (26, 4, "W")):
        g.put(x, y, c)
    outline_dark(g, ramp_of(DARK, WATER))
    return save(g, "vortex3")


# ===================================================================== 14) 潜る場所（浅い海の中の、深い青の穴。泡と光）
def dive3():
    g = Grid()
    cx, cy = 24, 30
    fill_ellipse(g, cx, cy, 20, 9, lambda x, y, u, v, d: "X" if d > 0.82 else ("U" if d > 0.45 else ("R" if d > 0.18 else "Q")))
    for k in range(0, 360, 6):
        a = math.radians(k)
        if (k // 18) % 2:
            g.put(cx + math.cos(a) * 21, cy + math.sin(a) * 10, "z")            # 浅瀬の白い線（とぎれとぎれ）
    for (bx, by, r) in ((24, 18, 1.6), (21, 12, 1.2), (26, 8, 1.0), (23, 4, 0.8)):  # 泡（上へ小さく）
        fill_ellipse(g, bx, by, r + 0.6, r + 0.6, lambda x, y, u, v, d: "z" if (d > 0.45 and u + v < 0.6) else ("P" if d > 0.45 else None))
    for (x, y) in ((12, 25), (36, 33)):
        g.put(x, y, "e"); g.put(x - 1, y, "P"); g.put(x + 1, y, "P"); g.put(x, y - 1, "P"); g.put(x, y + 1, "P")
    return save(g, "dive3")


# ===================================================================== 15) 砂漠の野営地（しまの天幕3つ・やしの木・たき火）
def tents3():
    g = Grid()
    def tent(cx, top, w, h, cloth, stripe):
        """棟が奥へのびる天幕。左の面は明るく、右の面は暗い。手前は三角の入口"""
        for y in range(top, top + h):
            t = (y - top + 1) / h
            half = w / 2 * t
            for x in range(int(cx - half) - 1, int(cx + half) + 2):
                dx = x + 0.5 - cx
                if abs(dx) > half:
                    continue
                st = (int(abs(dx)) // 2) % 2 == 0
                if dx < 0:
                    c = cloth[2] if st else stripe[1]
                else:
                    c = cloth[1] if st else stripe[0]
                g.put(x, y, c)
        # 入口（下のまん中の三角）
        for y in range(top + h - 5, top + h):
            k = y - (top + h - 5)
            for x in range(int(cx - k * 0.6), int(cx + k * 0.6) + 1):
                g.put(x, y, "k")
        g.put(int(cx), top - 1, "w"); g.put(int(cx), top - 2, "w"); g.put(int(cx) + 1, top - 2, "G")
    # やしの木（右の奥）
    for y in range(9, 31):                                               # 幹（ゆるく右へ曲がる。2ドットはば、節）
        x = 37 + ((y - 9) / 22) ** 2 * 3
        g.put(x, y, "y" if y % 3 else "x"); g.put(x + 1, y, "x" if y % 3 else "w")
    for (ang, ln) in ((-2.6, 9), (-2.0, 8), (-1.2, 7), (-0.5, 9), (0.1, 8), (-1.6, 5)):   # 葉（弧をえがいて垂れる6本）
        for k in range(ln):
            t = k / ln
            x = 37.5 + math.cos(ang) * k
            y = 8 + math.sin(ang) * k * 0.6 + t * t * 6
            g.put(x, y, "N" if k < ln * 0.5 and math.cos(ang) < 0 else "K")
            g.put(x, y + 1, "J")
    g.rect(37, 8, 38, 9, "w")
    tent(22, 8, 22, 20, ("o", "F", "G"), ("m", "n"))
    tent(10, 20, 15, 15, ("o", "m", "n"), ("x", "y"))
    tent(36, 22, 15, 14, ("o", "m", "n"), ("F", "G"))
    # たき火（手前のまん中。石の輪＋炎）
    fill_ellipse(g, 24, 41, 4, 1.8, lambda x, y, u, v, d: ("c" if v < 0 else "b") if d > 0.45 else "w")
    for (x, y, c) in ((24, 37, "t"), (23, 38, "t"), (24, 38, "L"), (25, 38, "t"), (24, 39, "M"), (23, 39, "L"), (25, 39, "L")):
        g.put(x, y, c)
    outline_dark(g, ramp_of("oFG", "omn", WOOD, LEAF, STONE))
    return save(g, "tents3")


# ===================================================================== 16) 浮き島（草の上の面・岩の底・小さな塔と家・雲のかたまり）
def sky3():
    g = Grid()
    cx, cy, rx = 24, 20, 19
    ry = rx * ER
    def under(x, y):
        u = (x + 0.5 - cx) / rx
        if abs(u) > 1 or y + 0.5 < cy:
            return False
        depth = 22 * (1 - abs(u)) ** 1.2 + ry * math.sqrt(max(0, 1 - u * u))
        return y + 0.5 <= cy + depth
    rock(g, under, (4, int(cy), 44, 44), "oabc", seed=51, n=12, cracks=0.4, base=-0.05)
    fill_ellipse(g, cx, cy, rx, ry, lambda x, y, u, v, d: tone("oJKN", (0.95 if (d > 0.7 and v < 0) else 0.62) - u * 0.15 - (0.25 if d > 0.82 and v > 0.3 else 0)))
    # 塔（左）と家（右）
    cylinder(g, 15, 3, 6, 19, 1.1, "oabc", course=3, joints=False)
    cone(g, 15, 6, 3.8, 6, 1.3, "oBCD")
    g.rect(14, 10, 14, 12, "k"); g.put(14, 11, "L")
    house(g, 23, 11, 12, "hip", "oBCD", rd=4, wh=4, door="k")
    # 雲（左下と右に、丸いかたまり）
    for (bx, by, r) in ((6, 33, 3.4), (10, 34, 2.6), (41, 28, 3.0), (44, 29, 2.2)):
        fill_ellipse(g, bx, by, r, r * 0.75, lambda x, y, u, v, d: "z" if u + v < 0.3 else "v")
    outline_dark(g, ramp_of("oabc", "oJKN", "oBCD", "omn"))
    return save(g, "sky3")


# ===================================================================== 17) 宮殿（暗い石・金の屋根・むらさきの光。左右対称で、まん中がいちばん高い）
def palace3():
    g = Grid()
    P = DARK
    # テラス（上の面＋手前の面）
    top_face(g, 2, 45, 35, 38, P, 0.8); brick_face(g, 2, 45, 39, 43, P, 0.45, seed=1)
    for y in range(39, 44):                                                # 正面の階段
        for x in range(19, 29):
            g.put(x, y, "s" if y % 2 else "q")
    # 左右の翼（寄棟の屋根は金）
    for (x0, x1) in ((3, 16), (31, 44)):
        hip_roof(g, x0, x1, 17, 23, "oghL", wb=1.5, ws=1.0)
        brick_face(g, x0, x1, 25, 34, P, 0.6, seed=2)
        for i, wx in enumerate(range(x0 + 2, x1 - 1, 4)):
            g.rect(wx, 28, wx, 30, "k")
            if i % 2 == 0:
                g.put(wx, 29, "L")
    # まん中の館（高い。正面に大きな扉）
    hip_roof(g, 15, 32, 13, 19, "oghL", wb=1.5, ws=1.0)
    brick_face(g, 15, 32, 21, 34, P, 0.65, seed=3)
    for y in range(26, 35):
        for x in range(21, 27):
            if y > 27 or 22 <= x <= 25:
                g.put(x, y, "k")
    g.put(23, 30, "Y"); g.put(24, 30, "Y"); g.put(23, 29, "W"); g.put(24, 29, "W")
    for wx in (17, 29):
        g.rect(wx, 24, wx + 1, 27, "k"); g.put(wx, 25, "L")
    # まん中の尖塔（いちばん高い）
    for y in range(0, 14):
        half = 0.5 + y * 0.32
        for x in range(18, 30):
            u = (x + 0.5 - 24) / max(0.6, half)
            if abs(u) <= 1:
                g.put(x, y, tone(P, 0.8 - u * 0.45))
    g.put(24, 0, "h"); g.put(23, 6, "Y"); g.put(23, 7, "W")
    # 左右の小塔
    for tx in (5, 42):
        for y in range(8, 18):
            half = 0.5 + (y - 8) * 0.3
            for x in range(tx - 4, tx + 5):
                u = (x + 0.5 - tx) / max(0.6, half)
                if abs(u) <= 1:
                    g.put(x, y, tone("oghL", 0.85 - u * 0.35))
    outline_dark(g, ramp_of(P, "ogh"))
    return save(g, "palace3")


# ===================================================================== 18〜21) 小島（共通の土台）
def islet_fort3():
    g = Grid()
    islet_base(g, top="sand", seed=61)
    S = STONE
    top_face(g, 12, 35, 19, 21, S, 0.9); parapet(g, 12, 35, 19, S, 3)
    brick_face(g, 12, 35, 22, 32, S, 0.55, seed=4)
    for y in range(26, 33):
        for x in range(21, 27):
            if y > 27 or 22 <= x <= 25:
                g.put(x, y, "k")
    cylinder(g, 12, 4, 10, 30, 1.4, S)                                    # 左の塔
    ellipse_top(g, 12, 10, 4.5, 1.6, S, inner=1.6, merlons=10)
    g.rect(12, 1, 12, 9, "w"); g.put(13, 1, "G"); g.put(14, 1, "G"); g.put(15, 2, "F"); g.put(13, 2, "F"); g.put(14, 2, "F")
    g.rect(11, 16, 11, 18, "k"); g.put(11, 17, "L")
    for (x, y) in ((33, 20), (34, 21), (35, 22), (34, 23)):
        g.put(x, y, ".")                                                  # 右の壁のくずれ
    outline_dark(g, ramp_of(S, SAND))
    return save(g, "islet-fort3")


def islet_shrine3():
    g = Grid()
    islet_base(g, top="grass", seed=62)
    # 円い台（石）と、立った大きな石の環（金のふち）。中に欠けた小さな環が光る
    fill_ellipse(g, 24, 30, 10, 3.6, lambda x, y, u, v, d: "d" if v < 0 else "c")
    for y in range(29, 32):
        for x in range(15, 34):
            if ell(x, y - 2, 24, 30, 10, 3.6) <= 1 and ell(x, y, 24, 30, 10, 3.6) > 1:
                g.put(x, y, "b")
    for k in range(720):
        a = k / 720 * 2 * math.pi
        for th in (0, 0.9, 1.8):
            r = 10 - th
            x, y = 24 + math.cos(a) * r * 0.82, 18 + math.sin(a) * r
            c = "d" if th == 0 and math.cos(a) < 0.2 else ("c" if th < 1.5 else "b")
            if th == 0 and math.sin(a) < -0.5:
                c = "h"
            g.put(x, y, c)
    for k in range(360):
        a = k / 360 * 2 * math.pi
        if 0.4 < a < 1.3:
            continue
        g.put(24 + math.cos(a) * 3.2, 18 + math.sin(a) * 3.6, "P" if math.cos(a) < 0.3 else "O")
    g.put(24, 18, "e")
    outline_dark(g, ramp_of(STONE, "oJKN"))
    return save(g, "islet-shrine3")


def islet_cave3():
    g = Grid()
    islet_base(g, top="sand", seed=63)
    inside = crag_mask(24, [(18, 4, 10), (29, 7, 9)], 31, 15, 12)
    rock(g, inside, (6, 3, 42, 31), STONE, seed=64, n=12, cracks=0.5)
    for y in range(20, 32):
        for x in range(18, 31):
            top = 20 + ((x + 0.5 - 24.5) / 6) ** 2 * 4
            if abs(x + 0.5 - 24.5) <= 5.5 and y >= top:
                g.put(x, y, "k" if abs(x + 0.5 - 24.5) < 4 and y > top + 1 else "o")
    outline_dark(g, ramp_of(STONE, SAND))
    return save(g, "islet-cave3")


def islet_ruin3():
    g = Grid()
    islet_base(g, top="grass", seed=65)
    S = STONE
    def col(cx, top, bot, broken=False):
        cylinder(g, cx, 2.4, top, bot, 0.8, S, course=3, joints=False)
        if not broken:
            for x in range(int(cx - 3), int(cx + 4)):
                g.put(x, top - 1, "d" if x < cx + 1 else "c")
        else:
            g.put(cx - 2, top, "d"); g.put(cx + 1, top + 1, ".")
    col(14, 9, 30); col(25, 9, 30)
    top_face(g, 10, 29, 5, 6, S, 0.95); brick_face(g, 10, 29, 7, 8, S, 0.5, course=9, brick=7)
    col(34, 18, 31, broken=True)
    fill_ellipse(g, 38, 33, 3, 1.6, lambda x, y, u, v, d: tone(S, 0.8 - v * 0.3))
    for (x, y) in ((13, 20), (14, 21), (26, 14), (25, 15), (24, 16)):
        g.put(x, y, "K"); g.put(x, y + 1, "J")
    outline_dark(g, ramp_of(S, "oJKN"))
    return save(g, "islet-ruin3")


# ===================================================================== 22) 森の祠（2回目の祠を、家族のパレット16色におさめて描きなおし）
def shrine3():
    g = Grid()
    cx = 24
    foliage(g, [(9, 13, 7), (38, 13, 7), (17, 8, 6.5), (31, 8, 6.5), (8, 26, 5.5), (40, 26, 5.5)])
    cylinder(g, cx, 15, 33, 36, 15 * ER * 0.85, STONE, course=0, joints=False, shade=-0.08)
    ellipse_top(g, cx, 33, 15, 15 * ER * 0.85, STONE)
    for (mx, my) in ((11, 33), (16, 31), (33, 32), (28, 34)):
        for (dx, dy) in ((0, 0), (1, 0), (0, 1), (1, 1), (2, 0)):
            if g.get(mx + dx, my + dy) in "cd":
                g.put(mx + dx, my + dy, "K" if dy == 0 else "J")
    cylinder(g, cx, 8, 21, 31, 2.6, STONE, course=3)
    for y in range(23, 33):
        for x in range(cx - 2, cx + 3):
            if y > 24 or abs(x + 0.5 - (cx + 0.5)) < 2:
                g.put(x, y, "k")
    g.put(cx, 28, "L")
    fill_ellipse(g, cx, 21, 10, 11, lambda x, y, u, v, d: None if y > 22 else tone("oBCD", 0.62 - u * 0.4 - v * 0.15 - (0.15 if (y - 9) % 4 == 3 else 0) + (0.2 if (u + 0.35) ** 2 + (v + 0.55) ** 2 < 0.08 else 0)))
    for x in range(cx - 10, cx + 11):
        g.put(x, 22, "o" if x > cx + 3 else "B")
    for k in range(480):                                                  # 屋根の上の環（外の環と、欠けた内の環）
        a = k / 480 * 2 * math.pi
        g.put(cx + math.cos(a) * 3.4, 4 + math.sin(a) * 3.2, "h" if math.cos(a) + math.sin(a) < 0.4 else "g")
        if not (-1.4 < a - math.pi * 2 < -0.2 or -1.4 < a < -0.2):
            g.put(cx + math.cos(a) * 1.7, 4 + math.sin(a) * 1.6, "h")
    for y in range(8, 11):
        g.put(cx, y, "g")
    for y in range(36, 46):                                               # 手前の環の石板
        for x in range(cx - 4, cx + 5):
            if y > 37 or abs(x + 0.5 - (cx + 0.5)) < 3.5:
                g.put(x, y, tone(STONE, 0.85 - (x - cx + 4) * 0.07))
    ring_mark(g, cx, 40, "h", "L", "g")
    foliage(g, [(8, 40, 4.6), (40, 40, 4.6)])
    outline_dark(g, ramp_of(STONE, LEAF, "oBCD"))
    return save(g, "shrine3")


PIECES = [castle3, spire3, town3, cave3, mine3, port3, village3, lake3, temple3, ruin3, stones3, bigtree3, volcano3,
          vortex3, dive3, tents3, sky3, palace3, islet_fort3, islet_shrine3, islet_cave3, islet_ruin3, shrine3]


# ===================================================================== 確かめ用
def show(names, kind="grass", Z=7, out=None):
    from PIL import Image
    from study3_view import on_terrain
    ims = []
    for n in names:
        rows = [l for l in open(os.path.join(HERE, n + ".txt")).read().split("\n") if l]
        pal = json.load(open(os.path.join(HERE, f"pal-{n}.json")))
        im = on_terrain(to_img(rows, pal), kind)
        ims.append(im.resize((im.width * Z, im.height * Z), Image.NEAREST))
    W = sum(i.width + 10 for i in ims); H = max(i.height for i in ims)
    sheet = Image.new("RGBA", (W, H), (40, 40, 48, 255)); x = 0
    for i in ims:
        sheet.paste(i, (x, 0)); x += i.width + 10
    sheet.save(out or "/tmp/claude-0/study2/s3.png")


def world(path):
    from PIL import Image
    from study3_view import world_rows, world_panel
    rows = world_rows()
    panels = [   # (左上のマスx, y, はば, 高さ, [(絵, マスx, マスy, 影の地面)], 見出し)。座標は world-map.generated.ts の本物の位置
        (38, 130, 28, 36, [("port3", 47, 137, "grass"), ("village3", 57, 161, "grass")], "namioto / mugikano"),
        (72, 134, 28, 28, [("lake3", 88, 142, "grass"), ("stones3", 78, 157, "grass")], "garasuko / stones"),
        (236, 18, 42, 32, [("town3", 245, 27, "snow"), ("town3", 269, 31, "snow"), ("shrine3", 272, 47, "snow")], "yukimachi / shimohara"),
        (220, 180, 40, 34, [("castle3", 238, 198, "grass"), ("stones3", 224, 190, "grass"), ("cave3", 256, 187, "grass"), ("shrine3", 231, 212, "grass")], "toushin castle"),
        (164, 110, 26, 30, [("spire3", 177, 135, "sea")], "the spire"),
        (260, 196, 44, 24, [("palace3", 300, 212, "waste"), ("tents3", 269, 217, "sand"), ("ruin3", 265, 204, "grass")], "kyotoukyu / arano"),
        (258, 232, 28, 20, [("volcano3", 272, 246, "ash")], "volcano islet"),
        (154, 20, 22, 20, [("islet-shrine3", 164, 31, None)], "islet"),
    ]
    ims = [world_panel(rows, *p) for p in panels]
    # 棚づめ（横はば 1500 ドットまで並べ、はみ出たら次の段）
    maxw, x, y, rowh, pos = 1500, 0, 0, 0, []
    for im in ims:
        if x + im.width > maxw:
            x, y, rowh = 0, y + rowh + 8, 0
        pos.append((x, y)); x += im.width + 8; rowh = max(rowh, im.height)
    sheet = Image.new("RGBA", (maxw, y + rowh), (20, 20, 24, 255))
    for im, (px, py) in zip(ims, pos):
        sheet.paste(im, (px, py))
    sheet = sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST)   # 2倍（ドットが見えるように）
    sheet.save(path)


if __name__ == "__main__":
    from study3_view import preview, grounds
    for f in PIECES:
        n, g, pal = f()
        print(n, len(pal), "色")
    preview(os.path.join(HERE, "study3-preview.png"))
    grounds(os.path.join(HERE, "study3-grounds.png"))
    world(os.path.join(HERE, "study3-world.png"))
    print("ok")
