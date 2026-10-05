"""フィールドのアイコンの勉強・2回目（2026-10-05、人間の指示「町、塔、洞窟、祠、さらに特別な塔とお城ももっと勉強してきて」）。

1回目（study.py）のきまりに、2回目の観察で分かったことを足して描く。どれも一から考えたオリジナルの形で、参考の素材は写していない。
くわしくは docs/design/field-icons-study.md の「2回目の勉強」。

  A. 形は「上の面＋手前の面」の2面だけで組む（真正面から少し見下ろす見え方。横の面は描かない）
     上の面がいちばん明るく、手前の面はまん中、右の面（屋根の右の流れ）はいちばん暗い
  B. 丸い物（塔）は、上のだ円のつぶれ 0.35〜0.4、石の段の線も同じだ円の弧で下にふくらませる（まわりこんで見える）
  C. 屋根は「いちばん近い軒からの距離」で面を分ける（寄棟の4つの面が自然に出る）。瓦の線は面ごとに軒と平行
  D. 高さのちがう物を重ねて、シルエットにでこぼこを作る（城＝角の塔・天守・門、町＝鐘の塔、特別な塔＝浮かぶ環）
  E. 光る物は「芯（白に近い1〜2色）→まわりの1段」の2重のかたまりだけ。ぼかしの点はまかない
  F. 雪や砂の上にも置けるよう、絵の中には草のふさを描かない（地面の色の違いは、ゲームの影と地面にまかせる）

出力: castle(64×64) / spire2(64×112) / town2 / tower2 / cave2 / shrine2（48×48）の .txt と pal-*.json、
     study2-preview.png（草・雪・砂の上で、今のアイコンと比べる）
"""
import json
import math
import os

from study import Grid, tone, outline_dark

HERE = os.path.dirname(os.path.abspath(__file__))


# ===================================================================== 道具
def cyl_light(u):
    """円柱の明るさ（u=-1 左はし … +1 右はし）。左が明るく、右のはしがいちばん暗い"""
    return 0.62 - 0.38 * u - 0.22 * u ** 4


def cylinder(g, cx, r, ytop, ybot, ry, ramp, course=3, joints=True, shade=0.0, skip=None):
    """円柱の胴。ytop/ybot は上と下のだ円の中心。石の段の線は、だ円の弧にそって下へふくらむ"""
    for y in range(int(ytop), int(ybot + ry) + 2):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            u = (x + 0.5 - cx) / r
            if abs(u) > 1:
                continue
            bow = ry * math.sqrt(max(0.0, 1 - u * u))
            if y + 0.5 > ybot + bow or y + 0.5 < ytop:
                continue
            if skip and skip(x, y):
                continue
            v = cyl_light(u) + shade
            yr = y - bow * 0.9 - ytop          # 弧にそった高さ
            if course and int(yr) % course == 0:
                v -= 0.17
            elif joints and abs(u) < 0.82:
                k = int(yr) // course
                a = math.asin(max(-1.0, min(1.0, u)))
                off = 0.5 if k % 2 else 0.0
                if int((a * 2.4 + off) % 1 * 10) == 0:
                    v -= 0.13
            g.put(x, y, tone(ramp, v))


def ellipse_top(g, cx, cy, rx, ry, ramp, inner=None, merlons=0, floor_ramp=None):
    """円柱の上の面。inner があれば、胸壁の輪と、内がわの床（奥の壁の影で暗い）"""
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
            u, v = (x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry
            if u * u + v * v > 1:
                continue
            if inner:
                iu, iv = (x + 0.5 - cx) / (rx - inner), (y + 0.5 - cy) / max(1.0, ry - inner * 0.6)
                if iu * iu + iv * iv <= 1:
                    fr = floor_ramp or ramp
                    g.put(x, y, tone(fr, 0.32 if v < 0.1 else 0.5 - iu * 0.1))
                    continue
            g.put(x, y, tone(ramp, 0.9 - u * 0.28 - (0.1 if v > 0.4 else 0)))
    if merlons:
        # 胸壁の歯: 手前の半分は1段高く（2ドット）、奥は1ドット。左の歯ほど明るい
        for k in range(merlons):
            ang = (k + 0.5) / merlons * 2 * math.pi
            if k % 2:
                continue
            x = cx + math.cos(ang) * (rx - 0.8)
            y = cy + math.sin(ang) * (ry - 0.3)
            u = math.cos(ang)
            front = math.sin(ang) > 0.15
            for dx in (0, 1):
                g.put(x - 0.5 + dx, y - 1, tone(ramp, 0.99 - u * 0.2 - dx * 0.1))
                if front:
                    g.put(x - 0.5 + dx, y, tone(ramp, 0.55 - u * 0.25))


def cone(g, cx, ybase, r, h, ry, ramp, rows=2):
    """とんがり屋根。左が明るく右が暗い。下のふちは、だ円の弧。2行ごとに瓦の線（弧にそう）"""
    for y in range(int(ybase - h), int(ybase + ry) + 2):
        t = (y + 0.5 - (ybase - h)) / h                 # 0=先 … 1=すそ
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            rr = r * min(1.0, t)
            if rr <= 0.3:
                continue
            u = (x + 0.5 - cx) / rr
            if abs(u) > 1:
                continue
            bow = ry * math.sqrt(max(0.0, 1 - u * u))
            if y + 0.5 > ybase + bow:
                continue
            v = cyl_light(u) + 0.08
            yr = y - bow * min(1.0, t)
            if t > 0.25 and int(yr) % rows == 0:
                v -= 0.16
            if y + 1.5 > ybase + bow:
                v -= 0.22                               # 軒の影
            g.put(x, y, tone(ramp, v))


def hip_roof(g, x0, x1, yb, yf, ramp, wb=2.0, ws=1.15, step=2, eave=True):
    """寄棟の屋根を上から。いちばん近い軒で面を分ける（奥＝明るい、左＝明るい、手前＝まん中、右＝暗い）"""
    for y in range(yb, yf + 1):
        for x in range(x0, x1 + 1):
            d = {"f": (yf + 0.5 - (y + 0.5)), "b": (y + 0.5 - yb) * wb,
                 "l": (x + 0.5 - x0) * ws, "r": (x1 + 0.5 - (x + 0.5)) * ws}
            face = min(d, key=d.get)
            base = {"b": 0.92, "l": 0.78, "f": 0.56, "r": 0.3}[face]
            dist = d[face] / (wb if face == "b" else ws if face in "lr" else 1)
            if int(dist) % step == step - 1:
                base -= 0.07 if face == "r" else 0.15   # 瓦の段（軒と平行。暗い面では弱く）
            # 稜（面のさかい）は明るい線
            ds = sorted(d.values())
            if ds[1] - ds[0] < 0.6 and face != "r":
                base += 0.12
            g.put(x, y, tone(ramp, base))
    if eave:
        for x in range(x0, x1 + 1):
            g.put(x, yf + 1, ramp[0])


def brick_face(g, x0, x1, y0, y1, ramp, v0=0.5, course=3, brick=6, seed=0):
    """手前の面の石積み。段ごとに目地をずらす。右へ少しずつ暗く"""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            v = v0 - (x - x0) / max(1, x1 - x0) * 0.16
            r = y - y0
            if r % course == course - 1:
                v -= 0.17
            elif (x - x0 + (r // course) * (brick // 2) + seed) % brick == 0:
                v -= 0.12
            g.put(x, y, tone(ramp, v))


def top_face(g, x0, x1, y0, y1, ramp, v0=0.88):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            g.put(x, y, tone(ramp, v0 - (x - x0) / max(1, x1 - x0) * 0.18))


def parapet(g, x0, x1, y, ramp, period=4):
    """手前のふちの胸壁: 歯（明るい上の面）とすき間（影）をくり返す"""
    for x in range(x0, x1 + 1):
        if (x - x0) % period < period // 2:
            g.put(x, y - 1, tone(ramp, 0.99 - (x - x0) / max(1, x1 - x0) * 0.2))
            g.put(x, y, tone(ramp, 0.55))
        else:
            g.put(x, y, tone(ramp, 0.3))


def ring_mark(g, cx, cy, c_out, c_in, c_dark=None):
    """この世界の『環信仰』のしるしの小さな版（5×5）: 外の環と、欠けた内の環"""
    for (dx, dy) in ((-1, -2), (0, -2), (1, -2), (-2, -1), (2, -1), (-2, 0), (2, 0), (-2, 1), (2, 1), (-1, 2), (0, 2), (1, 2)):
        g.put(cx + dx, cy + dy, c_out if dx + dy < 1 else (c_dark or c_out))
    g.put(cx, cy, c_in)


def save(g, name, pal):
    used = set("".join("".join(r) for r in g.a)) - {"."}
    pal = {k: v for k, v in pal.items() if k in used}       # 使っていない色はパレットに残さない
    g.save(name, pal)
    return name, g, pal


# ===================================================================== お城（64×64）
def castle():
    g = Grid(64, 64)
    S = "abcdef"            # 城の石（あたたかい灰色）
    R = "ABCDE"             # 屋根（深い青緑のスレート）
    C = "pqrs"              # 中庭の石だたみ
    pal = {"a": "#2e2a2c", "b": "#4a4446", "c": "#6c6462", "d": "#908678", "e": "#b6aa94", "f": "#ddd2b8",
           "A": "#14262e", "B": "#1f3d48", "C": "#2f5e68", "D": "#4a8a8a", "E": "#78b8ac",
           "p": "#5e5446", "q": "#7a6e5a", "r": "#988a70", "s": "#b4a688",
           "k": "#140e0c", "K": "#2a201a", "y": "#ffd474", "Y": "#fff2c0",
           "m": "#6a1e1c", "M": "#a8322a", "n": "#d65a3c", "g": "#c89430", "G": "#f2cc5a",
           "w": "#4a3420", "W": "#6e5034"}

    # 奥の壁（上の面と、中庭がわの面）
    top_face(g, 8, 55, 15, 17, S, 0.86)
    parapet(g, 8, 55, 15, S, 4)
    brick_face(g, 8, 55, 18, 23, S, 0.42, seed=1)
    # 左右の壁の上の面
    for x0 in (7, 54):
        top_face(g, x0, x0 + 2, 15, 45, S, 0.86 if x0 < 30 else 0.72)
    # 中庭（石だたみ。ところどころ明るい石。かたまりで）
    for y in range(24, 44):
        for x in range(10, 54):
            v = 0.5 + (0.16 if ((x // 4) + (y // 3)) % 3 == 0 else 0) - (0.22 if y < 26 else 0)
            g.put(x, y, tone(C, v))
    # 天守（寄棟の屋根＋手前の壁。軒下に旗）
    hip_roof(g, 19, 44, 6, 22, R, wb=1.5, ws=1.0)
    brick_face(g, 20, 43, 24, 37, S, 0.6, seed=2)
    g.rect(20, 24, 43, 24, "b")                                   # 軒下の影
    # 窓: 上の段に5つ、下の段に4つ（互いちがい）。明かりは一部だけ（顔に見えないよう、2つ並びの穴を作らない）
    for i, wx in enumerate((25, 28, 31, 34, 37)):
        g.rect(wx, 27, wx, 29, "k")
        if i in (1, 4):
            g.put(wx, 28, "y")
        g.put(wx, 30, "e")
    for i, wx in enumerate((26, 29, 35, 38)):
        g.rect(wx, 33, wx, 34, "k")
        if i == 2:
            g.put(wx, 34, "y")
    g.rect(30, 32, 34, 32, "d"); g.rect(30, 33, 34, 34, "c")     # まん中の張り出し（バルコニー）
    for x in range(21, 46):                                       # 天守が中庭に落とす影
        if g.get(x, 38) in "pqrs":
            g.put(x, 38, "p")
    # 天守の上の見張りの小塔（屋根の棟から立つ。シルエットのいちばん高い所）
    cylinder(g, 32, 3.0, 2, 10, 1.1, S)
    ellipse_top(g, 32, 2, 3.4, 1.3, S, inner=1.3, merlons=8)
    g.rect(31, 5, 31, 7, "k")
    for bx in (21, 40):                                           # 垂れ幕（赤。下は燕尾、環のしるし）
        for y in range(25, 34):
            for x in (bx, bx + 1, bx + 2):
                if y == 33 and x == bx + 1:
                    continue
                g.put(x, y, "n" if x == bx else ("M" if x == bx + 1 else "m"))
        g.put(bx + 1, 28, "G"); g.put(bx, 29, "g"); g.put(bx + 2, 29, "g"); g.put(bx + 1, 30, "g")
        g.rect(bx - 1, 25, bx + 3, 25, "w")
    # 奥の角の塔（円柱＋上の面＋とんがり屋根）
    for tx in (8, 55):
        cylinder(g, tx, 6, 11, 21, 2.4, S, shade=-0.04)
        ellipse_top(g, tx, 11, 6.6, 2.6, S)
        cone(g, tx, 11, 7.2, 10, 2.6, R)
        g.put(tx, 0, "W"); g.put(tx, 1, "W")
        g.put(tx + 1, 0, "M"); g.put(tx + 2, 0, "n"); g.put(tx + 1, 1, "m")
        g.rect(tx - 1, 15, tx, 17, "k")                           # 矢ざま
    # 手前の壁（上の面＋胸壁＋石積み）
    top_face(g, 9, 54, 43, 45, S, 0.86)
    parapet(g, 9, 54, 44, S, 4)
    brick_face(g, 9, 54, 46, 54, S, 0.55, seed=0)
    # 手前の角の塔
    for tx in (8, 55):
        cylinder(g, tx, 6.5, 38, 55, 2.6, S)
        ellipse_top(g, tx, 38, 7.1, 2.8, S, inner=2.2, merlons=12)
        cone(g, tx, 37, 7.6, 10, 2.8, R)
        g.put(tx, 26, "W"); g.put(tx, 27, "W")
        g.put(tx + 1, 26, "M"); g.put(tx + 2, 26, "n"); g.put(tx + 1, 27, "m")
        g.rect(tx - 1, 45, tx, 48, "k"); g.put(tx - 1, 47, "y")   # 明かりの窓
    # 門の建物（手前に張り出す。上に胸壁、暗いアーチの門、格子）
    top_face(g, 24, 39, 40, 43, S, 0.9)
    parapet(g, 24, 39, 41, S, 3)
    brick_face(g, 24, 39, 44, 58, S, 0.58, seed=3)
    for y in range(49, 59):
        for x in range(28, 36):
            if y > 51 or abs(x + 0.5 - 32) ** 2 + (y - 52) ** 2 <= 16.5:
                g.put(x, y, "k" if (x - 28) % 2 or y > 55 else "K")
    for x in range(27, 37):                                      # アーチの石のふち
        if g.get(x, 48) != "k":
            g.put(x, 48, "e" if x < 32 else "d")
    g.rect(26, 46, 26, 47, "k"); g.rect(37, 46, 37, 47, "k")    # 細い窓
    ring_mark(g, 32, 45, "G", "g", "g")                           # 門の上のしるし
    g.put(32, 45, "k")
    # 門前の石の道（足もとまで。ここだけ土の色）
    for y in range(59, 63):
        for x in range(28 - (y - 59), 36 + (y - 59)):
            g.put(x, y, "q" if (x + y) % 3 else "r")

    ramp_of = {**{c: S for c in S}, **{c: R for c in R}, **{c: C for c in C}}
    outline_dark(g, ramp_of)
    return save(g, "castle", pal)


# ===================================================================== 特別な塔（64×112）: 環の古塔。3つの浮かぶ環をまとう、3段の塔
def spire2():
    W, H = 64, 112
    g = Grid(W, H)
    S = "abcdef"            # 古い白い石（青みの灰）
    pal = {"a": "#262a3a", "b": "#3c4256", "c": "#5a6276", "d": "#7e8798", "e": "#a8b0bc", "f": "#d6dce0",
           "j": "#1c4a5e", "J": "#2f86a0", "i": "#6cd2e0", "I": "#e6fbff",
           "o": "#8a6418", "O": "#d8a838", "P": "#ffe27a",
           "k": "#12141e", "m": "#3e4a3a", "M": "#5e6e4c"}
    cx = 32
    tiers = [  # (半径, 上のだ円の中心y, 下のだ円の中心y)
        (13.5, 72, 102),
        (10.5, 49, 72),
        (7.5, 30, 49),
    ]
    ry_of = lambda r: r * 0.36

    # 輪（奥の半分）: 塔より先に描く
    rings = [(24.0, 86, "P", "o", False), (19.0, 61, "P", "o", False), (10.0, 13, "P", "o", True)]   # 大・中・欠けた小（光の石のまわり）

    def ring(rx, cy, c_hi, c_lo, broken, front):
        ry = rx * 0.3
        n = 720
        for k in range(n):
            a = k / n * 2 * math.pi
            if broken and 0.5 < a < 1.3:
                continue          # 欠けた環（いちばん小さな環）
            s = math.sin(a)
            if (s > 0) != front:
                continue
            for th in (0, 1):
                x = cx + math.cos(a) * rx
                y = cy + s * ry + th
                c = c_hi if th == 0 and math.cos(a) < 0.4 else ("O" if th == 0 else c_lo)
                g.put(x, y, c)

    for (rx, cy, hi, lo, br) in rings:
        ring(rx, cy, hi, lo, br, front=False)

    # 足もとの台座（2段のだ円の石段）
    for (rx, cy, h) in ((22, 103, 4), (18, 100, 3)):
        cylinder(g, cx, rx, cy, cy + h, rx * 0.3, S, course=0, joints=False, shade=-0.05)
        ellipse_top(g, cx, cy, rx, rx * 0.3, S)
    # 3段の塔（下から。上の段の胴が、下の段の上の面に乗る）
    for i, (r, yt, yb) in enumerate(tiers):
        cylinder(g, cx, r, yt, yb, ry_of(r), S, course=4)
        # 段のへりの上の面（張り出しの輪）
        ellipse_top(g, cx, yt, r + 1.6, ry_of(r + 1.6), S, inner=None)
    for i, (r, yt, yb) in enumerate(tiers[:-1]):
        nr, nyt, nyb = tiers[i + 1]
        cylinder(g, cx, nr, nyt, nyb, ry_of(nr), S, course=4)
    # 光の筋（まん中に1本だけ。段の上から窓の高さまで。芯の色＋右に1段暗い色）
    for (r, yt, yb) in tiers[1:]:
        for y in range(int(yt + ry_of(r) + 2), int((yt + yb) / 2) + 2):
            g.put(cx - 1, y, "i"); g.put(cx, y, "J")
    # 窓（段ごとに1つだけ。左右を互いちがいに。2つ並べると顔に見えるので並べない）
    for i, (r, yt, yb) in enumerate(tiers):
        wy = int((yt + yb) / 2) - (4 if i == 0 else 2)
        wx = cx + (int(r * 0.4) if i % 2 == 0 else -int(r * 0.5) - 1)
        if i == 0:
            wx = cx - int(r * 0.55)
        g.rect(wx, wy, wx + 1, wy + 3, "k"); g.put(wx, wy + 2, "j")
        g.put(wx, wy + 4, "e"); g.put(wx + 1, wy + 4, "d")
    # 扉（いちばん下。光る縁どり）
    for y in range(92, 106):
        for x in range(cx - 3, cx + 4):
            if y > 94 or abs(x + 0.5 - (cx + 0.5)) < 2.5:
                g.put(x, y, "k")
    for y in range(93, 106):
        g.put(cx - 4, y, "J"); g.put(cx + 4, y, "j")
    g.put(cx - 3, 92, "J"); g.put(cx + 3, 92, "j"); g.put(cx - 2, 91, "i"); g.put(cx - 1, 91, "i"); g.put(cx, 91, "i"); g.put(cx + 1, 91, "J"); g.put(cx + 2, 91, "J")
    # てっぺん: 上の面（胸壁つき）と、浮かぶ光の石（芯→まわりの2段だけ）
    ellipse_top(g, cx, 30, 8.6, 3.1, S, inner=2.2, merlons=12, floor_ramp=S)
    for y in range(3, 25):
        t = (y - 3) / 21
        half = 4.2 * math.sin(t * math.pi) ** 0.8 + 0.2
        for x in range(cx - 5, cx + 6):
            u = (x + 0.5 - cx) / max(0.5, half)
            if abs(u) <= 1:
                g.put(x, y, "I" if (u < -0.1 and t < 0.75) else ("i" if u < 0.45 else "J"))
    for (x, y) in ((cx - 6, 20), (cx + 6, 6)):
        g.put(x, y, "i")                                         # まわりの光（点ではなく、決まった4か所の十字）
        g.put(x - 1, y, "J"); g.put(x + 1, y, "J"); g.put(x, y - 1, "J"); g.put(x, y + 1, "J")
    # 苔（下の段のすそに、かたまりで少しだけ）
    for (x, y) in ((cx - 12, 98), (cx - 11, 99), (cx - 10, 99), (cx + 9, 100), (cx + 10, 100)):
        g.put(x, y, "M" if x < cx else "m")
    # 輪（手前の半分）: 塔のあとに描く
    for (rx, cy, hi, lo, br) in rings:
        ring(rx, cy, hi, lo, br, front=True)
    outline_dark(g, {c: S for c in S})
    return save(g, "spire2", pal)


# ===================================================================== 町・2（雪の町。鐘の塔で高さのでこぼこ、家は広場を向いて並ぶ）
def town2():
    g = Grid()
    S = "abcdef"            # 石垣
    O = "ABCDE"             # 赤茶の屋根
    T = "GHIJ"              # 青い屋根
    N = "uvwx"              # 屋根の上の雪（青白）
    pal = {"a": "#2c2a34", "b": "#46434e", "c": "#646070", "d": "#86808c", "e": "#a8a2a8", "f": "#cec8c6",
           "A": "#4a1c18", "B": "#76302a", "C": "#a2463a", "D": "#c86650", "E": "#e8967a",
           "G": "#1a2a48", "H": "#2a4470", "I": "#3e6698", "J": "#6a94c4",
           "u": "#9aaccc", "v": "#c4d2e8", "w": "#e6eef8", "x": "#ffffff",
           "k": "#16121a", "y": "#ffd36a", "Y": "#fff0b8",
           "p": "#5c4430", "P": "#86664a", "z": "#8e8c98", "Z": "#b2b0ba",
           "g": "#c08a2c", "h": "#f0c858"}

    cx, cy, rx, ry = 24, 28, 22.5, 15.5
    # 町の中の地面（積もった雪。門から鐘の塔へ、石だたみの道が十字に通る）
    for y in range(48):
        for x in range(48):
            if ((x + 0.5 - cx) / (rx - 2)) ** 2 + ((y + 0.5 - cy) / (ry - 2)) ** 2 <= 1:
                road = 21 <= x <= 27 or 30 <= y <= 33
                if road:
                    g.put(x, y, "Z" if ((x // 2) + y) % 3 else "z")
                else:
                    g.put(x, y, "v" if ((x // 4) + (y // 3)) % 5 == 0 else "w")
    # 石垣の輪（上の面＋手前に見える側面）
    for y in range(48):
        for x in range(48):
            e = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2
            e2 = ((x + 0.5 - cx) / (rx - 2.2)) ** 2 + ((y + 0.5 - cy) / (ry - 2.2)) ** 2
            if e <= 1 and e2 > 1:
                g.put(x, y, "w" if y < cy - 4 else tone(S, 0.86 - (x - cx) / rx * 0.22))   # 奥の石垣には雪
            for h in range(1, 4):
                eh = ((x + 0.5 - cx) / rx) ** 2 + ((y - h + 0.5 - cy) / ry) ** 2
                if y > cy and eh <= 1 and e > 1:
                    v = 0.5 - (x - cx) / rx * 0.3 - h * 0.04
                    if (x + (y // 3) * 2) % 5 == 0 or h == 3:
                        v -= 0.17
                    g.put(x, y, tone(S, v))

    def house(x0, y0, w, roof, snow_rows=2):
        """寄棟の屋根（上の段は雪）＋手前の壁。窓は2×2で明かり1つ"""
        R = O if roof == "O" else T
        hip_roof(g, x0, x0 + w - 1, y0, y0 + 6, R, wb=2.0, ws=1.3, eave=True)
        for y in range(y0, y0 + 6):
            for x in range(x0, x0 + w):
                d_b = (y - y0) * 2.0
                d_s = min(x - x0, x0 + w - 1 - x) * 1.3
                if y - y0 < snow_rows + (1 if d_s > 2 else 0) and g.get(x, y) != ".":
                    g.put(x, y, "x" if (x - x0) < w * 0.4 else ("w" if (x - x0) < w * 0.8 else "v"))
        for x in range(x0, x0 + w):                                # 軒のつらら（雪のふち）
            if (x - x0) % 3 == 0:
                g.put(x, y0 + 5, "v")
        wy = y0 + 8
        for y in range(wy, wy + 4):
            for x in range(x0, x0 + w):
                g.put(x, y, "f" if x < x0 + w - 2 else "e")
        g.rect(x0, wy + 3, x0 + w - 1, wy + 3, "d")
        dx = x0 + w // 2
        g.rect(dx, wy + 1, dx, wy + 3, "p"); g.put(dx - 1, wy + 1, "p"); g.rect(dx - 1, wy + 2, dx - 1, wy + 3, "P")
        g.put(x0 + 1, wy + 1, "y"); g.put(x0 + 1, wy + 2, "k")
        if w > 7:
            g.put(x0 + w - 2, wy + 1, "y"); g.put(x0 + w - 2, wy + 2, "k")

    # 鐘の塔（まん中の奥。高さで町の「顔」を作る）
    for y in range(4, 22):
        for x in range(21, 28):
            g.put(x, y, tone(S, 0.72 - (x - 21) * 0.07 - (0.17 if (y - 4) % 3 == 2 else 0)))
    for y in range(0, 6):                                          # とんがり屋根（上は雪）
        half = 1 + y * 0.8
        for x in range(20, 29):
            if abs(x + 0.5 - 24.5) <= half:
                g.put(x, y, ("x" if x < 24 else "v") if y < 3 else ("I" if x < 24 else ("H" if x < 26 else "G")))
    g.rect(23, 8, 25, 11, "k"); g.put(24, 8, "g"); g.put(24, 9, "h")      # 鐘
    ring_mark(g, 24, 15, "h", "g", "g")
    g.put(24, 15, "k")

    house(6, 9, 10, "T")
    house(31, 9, 11, "O")
    house(4, 23, 9, "O")
    house(35, 23, 9, "T")
    house(16, 25, 7, "T")
    house(26, 26, 8, "O")
    # 門（手前のまん中を切り、道が外へ出る）
    for y in range(40, 48):
        for x in range(20, 29):
            if g.get(x, y) != "." or y < 47:
                g.put(x, y, "Z" if (x + y) % 4 else "z")
    for y in range(39, 46):
        g.put(19, y, "e"); g.put(20, y, "d"); g.put(28, y, "c"); g.put(29, y, "b")
    g.put(19, 38, "x"); g.put(20, 38, "w"); g.put(28, 38, "w"); g.put(29, 38, "v")
    g.put(20, 37, "y"); g.put(28, 37, "y")                          # 門の灯
    outline_dark(g, {**{c: S for c in S}, **{c: O for c in O}, **{c: T for c in T}, **{c: N for c in N}, **{c: "zZ" for c in "zZ"}})
    return save(g, "town2", pal)


# ===================================================================== 塔・2（くずれた古い塔。上の面がギザギザに欠け、つたがからむ）
def tower2():
    g = Grid()
    S = "abcdef"
    V = "lmnN"              # つた
    pal = {"a": "#2e2a26", "b": "#4a443c", "c": "#6a6254", "d": "#8e8470", "e": "#b2a68c", "f": "#d6cbae",
           "l": "#1e3a22", "m": "#2f5a30", "n": "#4a8040", "N": "#78ac58",
           "k": "#120f0c", "K": "#241e18"}
    cx, r, ry = 23, 10.5, 3.8
    top_of = lambda x: 9 + int(abs(math.sin((x - 10) * 0.55)) * 3) + (6 if x > 27 else 0) + (3 if x > 31 else 0)   # くずれた上のふち
    base_y = 41
    # 胴（くずれた形で上を切る）
    cylinder(g, cx, r, 8, base_y, ry, S, course=3, skip=lambda x, y: y < top_of(x))
    # 欠けた上のふちの断面（上を向いた面は明るく、厚み2ドット）
    for x in range(int(cx - r), int(cx + r) + 1):
        if abs((x + 0.5 - cx) / r) > 1:
            continue
        t = top_of(x)
        g.put(x, t, tone(S, 0.95 - (x - cx) / r * 0.25))
        g.put(x, t + 1, tone(S, 0.8 - (x - cx) / r * 0.25))
    # 中の暗がり（くずれて中が見える所）
    for x in range(int(cx - r) + 2, int(cx + r) - 1):
        t = top_of(x)
        for y in range(t + 2, t + 4):
            if top_of(x) > 12:
                g.put(x, y, "K" if y == t + 2 else "b")
    # 窓（縦長。ひとつは割れて大きい）
    for (wx, wy, hh) in ((17, 22, 4), (26, 27, 6)):
        g.rect(wx, wy, wx + 1, wy + hh - 1, "k")
        g.put(wx - 1, wy + hh, "e"); g.put(wx, wy + hh, "e"); g.put(wx + 1, wy + hh, "d")
    g.put(28, 28, "k"); g.put(28, 29, "k")
    # 入口（板がはずれた暗いアーチ）
    for y in range(35, base_y + 3):
        for x in range(20, 26):
            if y > 36 or 21 <= x <= 24:
                if g.get(x, y) != ".":
                    g.put(x, y, "k")
    # くずれた石（足もとに、大きめのかたまり3つ）
    for (bx, by, w, h) in ((6, 41, 4, 3), (36, 40, 5, 3), (31, 44, 3, 2), (11, 44, 3, 2)):
        for y in range(by, by + h):
            for x in range(bx, bx + w):
                top = y == by
                g.put(x, y, tone(S, (0.9 if top else 0.5) - (x - bx) / w * 0.25))
    # つた（左の明るい面を上から下へ。房＝3〜5ドットのかたまりを、つるでつなぐ）
    vine = [(14, 12), (15, 15), (14, 18), (15, 21), (14, 24), (15, 27), (14, 30), (31, 19), (31, 22), (30, 25)]
    for (vx, vy) in vine:
        for (dx, dy, c) in ((0, 0, "n"), (1, 0, "m"), (0, 1, "m"), (-1, 1, "n"), (0, -1, "N"), (1, 1, "l")):
            if g.get(vx + dx, vy + dy) != ".":
                g.put(vx + dx, vy + dy, c if vx < cx else ("m" if c in "nN" else "l"))
    # 割れ目（右の暗い面に、斜めの1本）
    for (x, y) in ((29, 33), (30, 34), (30, 35), (31, 36)):
        g.put(x, y, "a")
    outline_dark(g, {**{c: S for c in S}, **{c: V for c in V}})
    return save(g, "tower2", pal)


# ===================================================================== 洞窟・2（鉱山の入口。地層の帯の小山＋木の枠＋レール）
def cave2():
    g = Grid()
    R = "abcdef"            # 岩（赤みの土色）
    pal = {"a": "#28241f", "b": "#443c33", "c": "#645849", "d": "#877760", "e": "#ab9a7e", "f": "#d0c0a0",
           "k": "#0e0a08", "K": "#1e1712",
           "w": "#3c2614", "W": "#6a4626", "X": "#9a6c3c",
           "r": "#5a5a64", "R": "#9a9aa6", "y": "#ffcf60", "Y": "#fff0b0"}
    cx = 24

    def half_w(y):
        """小山の半幅: 上は丸く平ら、すそは広い。2つのこぶで形にでこぼこ"""
        t = (y - 5) / 36
        if t < 0:
            return -1
        hw = 6 + 16 * math.sqrt(t) if t < 1 else 22 - (y - 41) * 0.6
        return hw

    # 小山: 大きな岩の面（12〜16個）の集まり。面ごとに明るさは1色（平らな面）で、
    # 面のさかいの上・左のふちに明るい線、下・右のふちに暗い線。山ぜんたいは左上が明るい
    import random
    rnd = random.Random(5)
    seeds = []
    for gy in range(5):
        for gx in range(4):
            sx = 4 + gx * 12 + rnd.uniform(-3, 3) + (6 if gy % 2 else 0)
            sy = 8 + gy * 8.5 + rnd.uniform(-2, 2)
            seeds.append((sx, sy, rnd.uniform(-0.12, 0.12)))
    cell = {}
    for y in range(4, 46):
        hw = half_w(y)
        bump = 1.6 if 13 <= y <= 19 else (1.0 if 27 <= y <= 30 else 0)
        for x in range(48):
            dx = x + 0.5 - cx
            if hw < 0 or not (-hw - bump <= dx <= hw + (1.0 if 21 <= y <= 25 else 0)):
                continue
            i = min(range(len(seeds)), key=lambda k: (x + 0.5 - seeds[k][0]) ** 2 + ((y + 0.5 - seeds[k][1]) * 1.3) ** 2)
            cell[(x, y)] = i
    for (x, y), i in cell.items():
        sx, sy, tilt = seeds[i]
        dx = x + 0.5 - cx
        v = 0.6 - (sx - cx) / 24 * 0.32 - (sy - 4) / 40 * 0.12 + tilt     # 面ごとに1色
        v -= (x + 0.5 - sx) * 0.018 + (y + 0.5 - sy) * 0.03              # 面の中でも左上が少し明るい
        up, left = cell.get((x, y - 1), -1), cell.get((x - 1, y), -1)
        down, right = cell.get((x, y + 1), -1), cell.get((x + 1, y), -1)
        if (down not in (i, -1)) or (right not in (i, -1)):
            v = min(v, 0.3)                       # さかいの影
        elif (up not in (i, -1)) or (left not in (i, -1)):
            v += 0.2                              # さかいの光（岩の角）
        g.put(x, y, tone(R, v))
    # すその大岩（左に2つ。上の面が明るい）
    for (bx, by, rr) in ((7, 41, 3.6), (12, 43, 2.6)):
        for y in range(int(by - rr), int(by + rr) + 1):
            for x in range(int(bx - rr) - 1, int(bx + rr) + 2):
                u, v_ = (x + 0.5 - bx) / (rr * 1.25), (y + 0.5 - by) / rr
                if u * u + v_ * v_ <= 1:
                    g.put(x, y, tone(R, 0.7 - u * 0.3 - v_ * 0.35))
    # 入口の穴（四角い。奥ほど暗い）
    for y in range(28, 44):
        for x in range(18, 30):
            g.put(x, y, "k" if (y > 30 and 19 < x < 28) else "K")
    # 木の枠（柱2本＋はり。左の面が明るい）
    for y in range(27, 44):
        g.put(17, y, "X"); g.put(18, y, "W"); g.put(19, y, "w")
        g.put(28, y, "W"); g.put(29, y, "w"); g.put(30, y, "w")
    for x in range(15, 33):
        g.put(x, 25, "X" if x < 30 else "W"); g.put(x, 26, "W" if x < 30 else "w"); g.put(x, 27, "w")
    g.put(15, 24, "W"); g.put(32, 24, "w")
    # ランプ（左の柱に。芯→まわりの2段）
    g.put(15, 30, "Y"); g.put(15, 31, "y"); g.put(14, 31, "y"); g.put(15, 29, "w")
    # レール（穴から手前へ。奥で狭く、手前で広い）
    for y in range(36, 47):
        t = (y - 36) / 10
        lx = 21 - t * 4; rx_ = 26 + t * 4
        for x in (lx, rx_):
            g.put(x, y, "R" if x < 24 else "r")
        if (y - 36) % 3 == 1:
            for x in range(int(lx) - 1, int(rx_) + 2):
                g.put(x, y, "W" if x < 24 else "w")
    # 掘り出した石の山（右に小さく。いちばん明るい石を1つ）
    for (x, y, c) in ((36, 42, "e"), (37, 42, "d"), (35, 43, "d"), (36, 43, "c"), (37, 43, "c"), (38, 43, "b"), (36, 41, "f")):
        g.put(x, y, c)
    outline_dark(g, {c: R for c in R})
    return save(g, "cave2", pal)


# ===================================================================== 祠・2（森の祠。木立のかたまりに囲まれた、丸い石の小堂と、光る環の石）
def shrine2():
    g = Grid()
    S = "abcdef"            # 苔のついた石
    F = "lmnoN"             # 木立（暗→明）
    V = "ABCD"              # 小堂の屋根（ドーム。青緑の銅）
    pal = {"a": "#2a2c2a", "b": "#454842", "c": "#64685c", "d": "#868a7a", "e": "#aaac98", "f": "#d0d0b8",
           "l": "#122a1c", "m": "#1e4028", "n": "#2e5c34", "o": "#467e40", "N": "#6ca452",
           "A": "#1a3a3a", "B": "#2c6060", "C": "#46908a", "D": "#7ec4b4",
           "k": "#0e1210", "i": "#ffe486", "I": "#fffbe0", "j": "#c89a38"}
    cx = 24

    def canopy(tx, ty, r):
        """木のかたまり: 丸い房を3つ重ね、房ごとに左上が明るい（1ドットの点はまかない）"""
        for (ox, oy, rr) in ((-r * 0.45, r * 0.15, r * 0.7), (r * 0.45, r * 0.2, r * 0.7), (0, -r * 0.3, r * 0.75)):
            bx, by = tx + ox, ty + oy
            for y in range(int(by - rr) - 1, int(by + rr) + 2):
                for x in range(int(bx - rr) - 1, int(bx + rr) + 2):
                    u, v = (x + 0.5 - bx) / rr, (y + 0.5 - by) / rr
                    d = u * u + v * v
                    if d <= 1:
                        val = 0.55 - u * 0.3 - v * 0.35 - (0.25 if d > 0.75 and (u + v) > 0.3 else 0)
                        g.put(x, y, tone(F, val))

    # 奥の木立（祠の後ろを囲む。高さで奥行き）
    for (tx, ty, r) in ((9, 13, 7), (38, 13, 7), (17, 8, 6.5), (31, 8, 6.5), (8, 26, 5.5), (40, 26, 5.5)):
        canopy(tx, ty, r)
    # 石の基壇（だ円。上の面＋手前の厚み）
    cylinder(g, cx, 15, 33, 36, 4.6, S, course=0, joints=False, shade=-0.08)
    ellipse_top(g, cx, 33, 15, 4.6, S)
    for (mx, my) in ((11, 33), (16, 31), (33, 32), (28, 34), (20, 30)):   # 基壇の上の苔（2×2以上のかたまり）
        for (dx, dy) in ((0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (-1, 1)):
            if g.get(mx + dx, my + dy) in "cdef":
                g.put(mx + dx, my + dy, "o" if (dx + dy) < 2 else "n")
    # 小堂（丸い胴＋ドームの屋根）
    cylinder(g, cx, 8, 21, 31, 2.6, S, course=3)
    for y in range(23, 33):                                       # 入口（アーチ）
        for x in range(cx - 2, cx + 3):
            if y > 24 or abs(x + 0.5 - (cx + 0.5)) < 2:
                g.put(x, y, "k")
    g.put(cx, 28, "j"); g.put(cx, 27, "i")                        # 奥の灯
    for y in range(9, 23):                                        # ドーム（左上が明るい）
        for x in range(cx - 11, cx + 12):
            u = (x + 0.5 - cx) / 10.0
            v = (y + 0.5 - 21) / 11.0
            if u * u + v * v <= 1 and y <= 22:
                lit = 0.6 - u * 0.4 - v * 0.15 + (0.15 if (u + 0.35) ** 2 + (v + 0.55) ** 2 < 0.08 else 0)
                if (y - 9) % 4 == 3:
                    lit -= 0.15
                g.put(x, y, tone(V, lit))
    for x in range(cx - 10, cx + 11):
        g.put(x, 22, "A" if x > cx + 3 else "B")
    # 屋根の上の環（三つの環。いちばん小さな環は欠ける）
    for (rr, c) in ((3.4, "j"), (1.9, "i")):
        for y in range(-5, 6):
            for x in range(-5, 6):
                if abs(math.hypot(x, y * 1.15) - rr) < 0.5:
                    a = math.atan2(y, x)
                    if rr < 3 and -1.4 < a < -0.2:
                        continue
                    g.put(cx + x, 4 + y, c if x + y < 1 else "j")
    for y in range(8, 11):
        g.put(cx, y, "j")
    g.put(cx - 1, 10, "j"); g.put(cx + 1, 10, "j")
    # 手前の光る環の石（基壇の前。立った石の板に、光る環が彫ってある）
    for y in range(36, 46):
        for x in range(cx - 4, cx + 5):
            if y > 37 or abs(x + 0.5 - (cx + 0.5)) < 3.5:
                g.put(x, y, tone(S, 0.82 - (x - cx + 4) * 0.07))
    ring_mark(g, cx, 40, "I", "i", "i")
    g.put(cx, 40, "j")
    # 手前の左右の小さな木（森の中の感じ。基壇のはしを少し隠す）
    canopy(8, 40, 4.6)
    canopy(40, 40, 4.6)
    outline_dark(g, {**{c: S for c in S}, **{c: F for c in F}, **{c: V for c in V}})
    return save(g, "shrine2", pal)


# ===================================================================== プレビュー（草・雪・砂の上で。足もとに半透明の影）
def load_txt(d, n, pn=None):
    rows = [l for l in open(os.path.join(HERE, "..", d, f"{n}.txt")).read().split("\n") if l]
    p = json.load(open(os.path.join(HERE, "..", d, f"pal-{pn or n}.json")))
    return rows, p


def to_img(rows, pal):
    from PIL import Image
    w, h = max(len(r) for r in rows), len(rows)
    im = Image.new("RGBA", (w, h))
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c in pal:
                im.putpixel((x, y), tuple(int(pal[c][k:k + 2], 16) for k in (1, 3, 5)) + (255,))
    return im


def ground(kind, w, h):
    from PIL import Image
    pip = os.path.join(HERE, "..", "..", "pipoya", "pipo-map001", "640x480")
    if kind == "grass":
        tile = Image.open(os.path.join(pip, "pipo-map001.png")).convert("RGBA").crop((0, 0, 32, 32))
    elif kind == "sand":
        tile = Image.open(os.path.join(pip, "pipo-map001_at-sabaku.png")).convert("RGBA").crop((0, 64, 32, 96))
    else:   # 雪（ゲームの雪の地面の色 #e8eef2 に、少し明るい・暗いかたまり）
        tile = Image.new("RGBA", (32, 32), (0xe8, 0xee, 0xf2, 255))
        for y in range(32):
            for x in range(32):
                k = (x * 7 + y * 13 + (x // 4) * (y // 3)) % 23
                if k == 0:
                    tile.putpixel((x, y), (0xdb, 0xe7, 0xf5, 255))
                elif k == 5:
                    tile.putpixel((x, y), (0xf6, 0xfa, 0xff, 255))
    bg = Image.new("RGBA", (w, h))
    for y in range(0, h, 32):
        for x in range(0, w, 32):
            bg.paste(tile, (x, y))
    return bg


def on_ground(im, kind, shadow=True):
    """地面の上に置く。影は絵のいちばん下の行の幅で、半透明のだ円（ゲームではコードで敷く予定）"""
    from PIL import Image, ImageDraw
    w, h = im.size
    bg = ground(kind, w, h)
    if shadow:
        a = im.split()[3]
        bbox = a.getbbox()
        x0, x1 = bbox[0], bbox[2]
        sh = Image.new("RGBA", (w, h))
        col = {"grass": (10, 30, 10, 90), "snow": (40, 60, 100, 70), "sand": (60, 40, 10, 80)}[kind]
        ImageDraw.Draw(sh).ellipse((x0 + (x1 - x0) * 0.08, h - 9, x1 - (x1 - x0) * 0.02, h - 1), fill=col)
        bg.alpha_composite(sh)
    bg.alpha_composite(im)
    return bg


def preview(items, path):
    from PIL import Image, ImageDraw
    Z = 4
    pairs = [  # (練習, 比べる今のアイコン, 地面)
        ("castle", ("r17-polish", "icon-castle"), ["grass", "snow", "sand"]),
        ("spire2", ("r22-vehicles", "spire"), ["grass"]),
        ("town2", ("r17-polish", "icon-snowtown"), ["snow", "grass", "sand"]),
        ("tower2", ("r17-polish", "icon-ruin"), ["grass"]),
        ("cave2", ("r17-polish", "icon-mine"), ["grass", "sand"]),
        ("shrine2", ("r17-polish", "icon-shrine"), ["grass"]),
    ]
    imgs = {n: to_img(["".join(r) for r in g.a], pal) for (n, g, pal) in items}
    # 1行目: 拡大（Z倍）で、練習を各地面の上に、右に今のアイコン（草）
    cells = []
    for name, old, grounds in pairs:
        im = imgs[name]
        for kd in grounds:
            cells.append((f"{name} / {kd}", on_ground(im, kd)))
        orows, opal = load_txt(*old)
        cells.append((f"now: {old[1]}", on_ground(to_img(orows, opal), "grass", shadow=False)))
    # 並べる（高さはまちまちなので、行ごとに詰める）
    maxw = 1500
    x, y, rowh = 16, 16, 0
    placed = []
    for label, im in cells:
        w, h = im.width * Z, im.height * Z
        if x + w > maxw:
            x, y, rowh = 16, y + rowh + 30, 0
        placed.append((label, im, x, y))
        x += w + 16
        rowh = max(rowh, h)
    H1 = y + rowh + 30
    # 下の帯: 2倍（ゲームの大きさ）で、草の地面に足もとをそろえて並べる
    WH = 118
    world = ground("grass", maxw // 2, WH)
    wx = 6
    from PIL import ImageChops
    for name, _, _ in pairs:
        im = imgs[name]
        sh = on_ground(im, "grass")
        # 地面ごと貼ると四角が見えるので、地面とちがう所（影と絵）だけを貼る
        diff = ImageChops.difference(sh.convert("RGB"), ground("grass", im.width, im.height).convert("RGB")).convert("L").point(lambda v: 255 if v else 0)
        world.paste(sh, (wx, WH - 2 - im.height), diff)
        wx += im.width + 6
    strip_h = WH * 2
    sheet = Image.new("RGBA", (maxw, H1 + strip_h), (40, 40, 48, 255))
    dr = ImageDraw.Draw(sheet)
    for label, im, px, py in placed:
        sheet.paste(im.resize((im.width * Z, im.height * Z), Image.NEAREST), (px, py))
        dr.text((px, py + im.height * Z + 4), label, fill=(255, 255, 255))
    sheet.paste(world.resize((maxw, strip_h), Image.NEAREST), (0, H1))
    dr.text((8, H1 + 2), "x2 (game scale)", fill=(255, 255, 255))
    sheet.save(path)


if __name__ == "__main__":
    items = [castle(), spire2(), town2(), tower2(), cave2(), shrine2()]
    preview(items, os.path.join(HERE, "study2-preview.png"))
    print("ok")
