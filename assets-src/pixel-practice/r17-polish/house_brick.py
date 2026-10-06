"""レンガの家（2026-10-06、人間の指示「家の壁もレンガ調にしようか。ドット絵リアルな感じで。あと、家の屋根不自然だから直して」）。
house3d.py（漆喰の家）の作りなおし。すべて一から自作。光は左上。

屋根の直し: 前の屋根は、棟（いちばん上の線）が正面と平行に横へのびているのに、右の面だけ奥へななめに引いていて、
形がつながらなかった。ここでは、正面の壁＋奥へ引く右の壁（ななめ 0.45）の箱に、ふつうの「切妻屋根」をのせる:
  - 棟は正面と平行で、奥行きのまん中にある（正面から見ると、正面の屋根の面が少し右上へずれた平行四辺形になる）。
  - 右の壁の上は、三角の妻壁（つまかべ。レンガ）。屋根はその上に少し張り出し、ふちの厚み（破風）が見える。
  - 屋根の下（軒下）は、壁に影が落ちる。
レンガ: 長さ5・高さ2のレンガを、目地1ドットで、段ごとに半分ずらして積む（長手積み）。レンガ一つずつ色合いをかえ、
ところどころ焼けて暗いレンガ・欠け・すすけた所、足もとは湿って暗い。右の壁は陰で暗い色、段は奥へななめに上がる。
窓は石のまぐさ（上）と窓台（下）、玄関は石のアーチ。扉の色は前と同じ（扉の場所の見つけ方 doorRectOf が、扉の4色で探すため）。
書き出し: cottage-brick*.txt / manor-brick*.txt と pal-*.json（赤・青・緑の屋根）。"""
import json
import math
import random
import sys

SL = 0.45
pal = {
    "A": "#1e1620",                     # りんかく
    # 屋根（赤）
    "R1": "#4a1820", "R2": "#7a2a2c", "R3": "#9c3a2e", "R4": "#bc5236", "R5": "#d8744a", "R6": "#f09a68",
    # レンガ（正面: 明るい）
    "C1": "#6a3426", "C2": "#86432e", "C3": "#9e5236", "C4": "#b46442", "C5": "#c87c58",
    "J1": "#b8a890", "J2": "#94846c",   # 目地（正面）
    # レンガ（右の壁: 陰）
    "E1": "#40201c", "E2": "#552a22", "E3": "#68362a", "E4": "#7a4232",
    "J3": "#6e604e",                    # 目地（陰）
    # 石（土台・まぐさ・窓台・アーチ）
    "K1": "#585468", "K2": "#807c94", "K3": "#aaa8bc", "K4": "#cfcdd8",
    # 木（窓わく）
    "B2": "#5c3a1c", "B3": "#845428",
    # 扉（doorRectOf が探す4色。変えない）
    "D1": "#4a2a14", "D2": "#7a4a22", "D3": "#a8703a", "Y": "#f4cc50",
    # 窓ガラス・カーテン・花
    "G1": "#5a8cb4", "G2": "#9cd0ee", "G3": "#30506e", "CUR": "#d86a5a", "F1": "#3a7a34", "F2": "#5aa844", "F3": "#e84a5a",
    "M1": "#4a6a34", "M2": "#6a8a44",   # こけ
    "SOOT": "#3a3036", "L1": "#fff2b0",                  # すす
}
BLUE = {"R1": "#1c2850", "R2": "#2c4a88", "R3": "#3a5ea4", "R4": "#4a76c0", "R5": "#6a96dc", "R6": "#9cc0f4"}
GREEN = {"R1": "#183a28", "R2": "#2a5a3c", "R3": "#36764c", "R4": "#46905c", "R5": "#68b07a", "R6": "#9ad4a8"}


def hn(*a):
    n = 2166136261
    for v in a:
        n = ((n ^ (int(v) & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    n ^= n >> 15
    return n


class G:
    def __init__(s, w, h):
        s.w, s.h = w, h
        s.g = [["."] * w for _ in range(h)]

    def put(s, x, y, k):
        x, y = int(x), int(y)
        if 0 <= x < s.w and 0 <= y < s.h and k:
            s.g[y][x] = k

    def get(s, x, y):
        x, y = int(x), int(y)
        return s.g[y][x] if 0 <= x < s.w and 0 <= y < s.h else "."

    def poly(s, pts, f):
        ys = [p[1] for p in pts]
        for y in range(max(0, int(min(ys))), min(s.h, int(max(ys)) + 1)):
            for x in range(s.w):
                inside = False
                for i in range(len(pts)):
                    (xi, yi), (xj, yj) = pts[i], pts[i - 1]
                    if (yi > y + .5) != (yj > y + .5) and x + .5 < (xj - xi) * (y + .5 - yi) / (yj - yi) + xi:
                        inside = not inside
                if inside:
                    s.put(x, y, f(x, y) if callable(f) else f)


def brick(u, v, lit, seed):
    """レンガの面の色。u は横（面にそった位置）、v は下からではなく上からの段の位置。"""
    row = v // 3
    if v % 3 == 2:
        return "J1" if lit else "J3"
    off = 3 if row % 2 else 0
    col = (u + off) // 6
    if (u + off) % 6 == 5:
        return "J2" if lit else "J3"
    h = hn(row, col, seed)
    ramp = ["C1", "C2", "C3", "C4", "C5"] if lit else ["E1", "E2", "E3", "E4", "E4"]
    base = [1, 2, 2, 3, 3, 2, 4, 1, 2, 3, 0][h % 11] if lit else [1, 2, 2, 3, 1, 2, 0][h % 7]
    i = (u + off) % 6
    t = base
    # レンガ一つずつに立体感: 上の段は明るめ、下の段は1つ暗い（下のふちの影）。右はしは少し暗く、左上のかどに光
    if v % 3 == 1:
        t = base - 1 if (h >> 4) % 3 else base
    if i == 4 and v % 3 == 1:
        t = base - 1
    if lit and v % 3 == 0 and i == 0 and (h >> 6) % 3 == 0:
        t = base + 1
    if lit and (h >> 8) % 19 == 0 and i == 2:
        t = 0                                            # 欠け（暗い点）
    if lit and (h >> 9) % 23 == 0 and v % 3 == 0 and i in (1, 2, 3):
        return "J1"                                      # 角の欠け（目地の色がのぞく）
    return ramp[max(0, min(4, t))]


def build(W, H, FW, D, floors, FH, RH, ox=3, door=0.5, nwin=3, ov=3, porch=False, dormer=False, chimney=0.72, seed=1, door_h=None):
    rnd = random.Random(seed)
    g = G(W, H)
    x0, x1 = ox, ox + FW - 1
    bot = H - 9
    top = bot - floors * FH

    def sideY(x, y):
        return y - (x - x1) * SL

    xr = x1 + D                                          # 右の壁の奥のはし
    # ---- 右の壁（陰のレンガ）と、三角の妻壁 ----
    ridge_dy = D / 2 * SL + RH                           # 正面の軒から棟までの高さ
    apex = (x1 + D / 2, top - ridge_dy)
    for x in range(x1 + 1, xr + 1):
        u = x - x1
        ytop = sideY(x, top)
        # 妻壁の上のふち（三角）
        if u <= D / 2:
            yg = top - (u / (D / 2)) * ridge_dy
        else:
            yg = top - D * SL - ((D - u) / (D / 2)) * (ridge_dy - D / 2 * SL)
        for y in range(int(math.ceil(yg)), int(sideY(x, bot)) + 1):
            v = int(round(y - ytop)) + 300           # 段は奥へななめに上がる
            g.put(x, y, brick(u, v, False, seed + 7))
    # ---- 正面の壁（明るいレンガ） ----
    for y in range(top, bot + 1):
        for x in range(x0, x1 + 1):
            k = brick(x - x0, y - top, True, seed)
            # 足もとは湿って暗い（下の4段）
            if y > bot - 5 and k in ("C4", "C5") and hn(x, y, 3) % 3 == 0:
                k = "C2"
            g.put(x, y, k)
    # 角の石（コーナーストーン。正面の左はしと右はしに、段ごとに長短）
    for y in range(top, bot + 1):
        n = (y - top) // 3
        for x in (x0, x1):
            w = 3 if n % 2 == 0 else 2
            rng = range(x, x + w) if x == x0 else range(x - w + 1, x + 1)
            for xx in rng:
                k = "K3" if (y - top) % 3 != 2 else "K2"
                if x == x1:
                    k = "K2" if k == "K3" else "K1"
                g.put(xx, y, k)
    # 階のさかいの石の帯
    for f in range(1, floors):
        yb = top + f * FH
        for x in range(x0, x1 + 1):
            g.put(x, yb - 1, "K4"); g.put(x, yb, "K3"); g.put(x, yb + 1, "K2")
        for x in range(x1 + 1, xr + 1):
            g.put(x, sideY(x, yb), "K2"); g.put(x, sideY(x, yb) + 1, "K1")
    # ---- 土台（石） ----
    for y in range(bot + 1, bot + 6):
        for x in range(x0 - 1, x1 + 2):
            r = y - bot - 1
            off = (r // 2 % 2) * 4
            k = "K3" if r == 0 else "K2"
            if (x + off) % 8 == 7 or r == 4:
                k = "K1"
            elif r % 2 == 1 and hn(x // 8, r, seed) % 3 == 0:
                k = "K3"
            g.put(x, y, k)
    for x in range(x1 + 2, xr + 1):
        yb = sideY(x, bot)
        for r in range(5):
            k = "K2" if r == 0 else "K1"
            if (x + r) % 7 == 0 and r:
                k = "K2"
            g.put(x, yb + 1 + r, k)
    # ---- 窓 ----
    def window(wx, wy, w, h):
        for y in range(wy, wy + h):
            for x in range(wx, wx + w):
                k = "G1"
                if (x - wx) + (y - wy) in (1, 2, 3) or (x - wx) + (y - wy) == h + 1:
                    k = "G2"                              # 空のうつりこみ
                if y == wy:
                    k = "G3"                              # 上は、まぐさの影
                g.put(x, y, k)
        for y in range(wy, wy + h):
            g.put(wx - 1, y, "B3"); g.put(wx + w, y, "B2"); g.put(wx + w // 2, y, "B2")
        for x in range(wx, wx + w):
            g.put(x, wy + h // 2, "B2")
        for y in range(wy + 1, wy + 3):
            g.put(wx, y, "CUR"); g.put(wx + w - 1, y, "CUR")
        # 石のまぐさ（上）と窓台（下、少し張り出す）
        for x in range(wx - 2, wx + w + 2):
            g.put(x, wy - 2, "K4" if x < wx + w // 2 else "K3"); g.put(x, wy - 1, "K2")
        for x in range(wx - 2, wx + w + 2):
            g.put(x, wy + h, "K4"); g.put(x, wy + h + 1, "K1")

    def sidewin(sx, w, ytop, h):
        """右の壁（奥へななめ）の窓。木の枠（上・左は明るい木、下・右は暗い木）、まん中に桟、下に石の窓台。"""
        def ty(x, y):
            return int(round(sideY(x, y)))
        for dx in range(-1, w + 1):
            x = sx + dx
            yt = ty(x, ytop)
            for y in range(yt - 1, yt + h + 1):
                if dx in (-1, w) or y in (yt - 1, yt + h):
                    k = "B3" if (dx == -1 or y == yt - 1) else "B2"
                elif dx == w // 2 or y == yt + h // 2:
                    k = "B2"                              # 桟
                elif y == yt:
                    k = "G3"                              # 上は枠の影
                elif (dx + (y - yt)) % 6 in (2, 3) and dx < w // 2:
                    k = "G2"                              # 空のうつりこみ（ななめ）
                else:
                    k = "G1"
                g.put(x, y, k)
            g.put(x, yt + h + 1, "K3"); g.put(x, yt + h + 2, "K1")   # 石の窓台
            g.put(x, yt - 2, "E1")                                    # 上のまぐさの影
        for y in range(ty(sx, ytop), ty(sx, ytop) + 2):
            g.put(sx, y, "CUR")                                       # カーテン

    # door=None: 玄関を、左右の窓がちょうど同じ大きさになる所（窓のあく所のまんなか）に置く
    doorx = x0 + int(FW * door) if door is not None else (x0 + 3 + x1 - 5) // 2
    for fl in range(floors):
        wy = top + fl * FH + 5
        wh = FH - 10
        if fl == floors - 1:
            # 玄関のある階: 窓は、玄関のアーチの左と右の、あいた所のまん中に
            spans = [(x0 + 3, doorx - 8), (doorx + 8, x1 - 5)]
            slots = []
            for a_, b_ in spans:
                ww = min(7, b_ - a_ - 1)
                if ww >= 4:
                    slots.append(((a_ + b_ - ww) // 2 + 1, ww))
        else:
            slots = [(x0 + int(FW * (i + 0.5) / nwin) - 3, 7) for i in range(nwin)]
        for sx, ww in slots:
            window(sx, wy, ww, wh)
            if fl == floors - 1:                      # 下の階の窓には、花の植木箱
                for x in range(sx - 1, sx + ww + 1):
                    g.put(x, wy + wh + 2, "B3"); g.put(x, wy + wh + 3, "B2")
                    g.put(x, wy + wh + 1, "F1" if x % 2 else "F2")
                for x in range(sx, sx + ww, 3):
                    g.put(x, wy + wh + 1, "F3")
        sw = max(5, D // 2 + 1) if D < 15 else D // 2 + 2
        sidewin(x1 + max(3, (D - sw) // 2), sw, top + fl * FH + 4, FH - 9)
    # ---- 玄関（石のアーチ＋扉） ----
    dh = door_h if door_h else min(FH - 11, 13)   # 扉の高さ
    for y in range(bot - dh - 3, bot + 1):
        for x in range(doorx - 7, doorx + 8):
            d = abs(x - doorx)
            ya = bot - dh - (2 if d <= 3 else 1 if d <= 5 else 0)
            if y >= ya - 2 and d <= 6:
                g.put(x, y, "K3" if (x + y) % 4 else "K2")   # アーチの石
    for y in range(bot - dh, bot + 1):
        for x in range(doorx - 5, doorx + 6):
            d = abs(x - doorx)
            if y < bot - dh + (2 if d == 5 else 1 if d == 4 else 0):
                continue
            k = "D3" if x < doorx else "D2"
            if (x - doorx + 5) % 3 == 2:
                k = "D1"
            g.put(x, y, k)
    for y in range(bot - dh, bot + 1):
        g.put(doorx, y, "D1")
    g.put(doorx - 2, bot - 5, "Y"); g.put(doorx + 2, bot - 5, "Y")
    g.put(doorx, bot - dh - 2, "K4")                # かなめ石
    for x in range(doorx - 6, doorx + 7):
        g.put(x, bot + 1, "K4"); g.put(x, bot + 2, "K3")
    # 出入口の屋根（石のアーチの上の、小さな瓦の庇。両はしに木の腕木）
    py = bot - dh - 8
    for x in range(doorx - 9, doorx + 10):
        for r in range(5):
            y = py + r
            if r == 0:
                k = "R6"                                    # 壁につく所の水切り
            elif r == 4:
                k = "R1"                                    # 軒のふち
            else:
                cell = (x + (2 if r % 2 else 0)) % 3
                k = "R5" if cell == 0 else ("R3" if cell == 2 else "R4")
                if r == 3:
                    k = "R2" if cell == 2 else "R3"
            g.put(x, y, k)
    for x in range(doorx - 8, doorx + 9):                   # 庇の下の影（アーチの石に落ちる）
        g.put(x, py + 5, "SOOT" if x % 2 else "K1")
    for side in (-1, 1):                                    # 腕木（ななめの木）
        bx = doorx + side * 8
        for k in range(4):
            g.put(bx - side * k * 0, py + 5 + k, "B3" if side < 0 else "B2")
            g.put(bx + side * 0 - side * (k // 2), py + 5 + k, "B2")
    # 雨どい（正面の右のかど、たて）
    for y in range(top + 1, bot + 1):
        g.put(x1 - 3, y, "K2"); g.put(x1 - 2, y, "K1")
        if (y - top) % 7 == 3:
            g.put(x1 - 4, y, "K3"); g.put(x1 - 1, y, "K1")   # とめ金
    g.put(x1 - 4, bot, "K2"); g.put(x1 - 5, bot, "K1")    # 下の口
    # 玄関の横のかべ灯り
    lx = doorx + 9
    ly = bot - dh + 1
    if any(g.get(lx + a_, ly + b_)[0] in "GBF" for a_ in (-1, 0, 1) for b_ in (-1, 0, 1, 2)):
        lx = -100                                   # 窓とかさなるときは、灯りをつけない
    g.put(lx, ly - 1, "SOOT"); g.put(lx - 1, ly, "SOOT"); g.put(lx + 1, ly, "SOOT")
    g.put(lx, ly, "Y"); g.put(lx, ly + 1, "L1"); g.put(lx - 1, ly + 1, "SOOT"); g.put(lx + 1, ly + 1, "SOOT"); g.put(lx, ly + 2, "SOOT")
    # ---- 屋根（切妻。棟は正面と平行で、奥行きのまん中） ----
    ex0, ex1 = x0 - ov, x1 + ov                      # 正面の軒の左右
    ey = top + 1                                     # 軒の高さ（壁の上に少しかぶる）
    sh = D / 2                                       # 棟は軒から右へ D/2 ずれる
    ry = top - ridge_dy                              # 棟の高さ
    span = ey - ry

    def roof_front(x, y):
        t = (ey - y) / span                         # 0（軒）〜1（棟）
        xs = x - t * sh                             # 斜めのずれをもどした横の位置
        r = int((ey - y) // 3)
        ly = int((ey - y) % 3)
        off = 2 if r % 2 else 0
        cell = int(xs + off) % 4
        k = "R4"
        if ly == 0:
            k = "R2"                                # 瓦の下のふち（影）
        elif ly == 2:
            k = "R5"                                # 瓦の上のふち（光）
        if cell == 3:
            k = "R3"
        tv = hn(int(xs + off) // 4, r, seed + 2) % 7
        if ly == 1 and tv == 0:
            k = "R3"                                # すこし色のちがう瓦（ふき替えた所）
        if cell == 0 and ly == 1:
            k = "R5"                                # 瓦の左のふちの光
        if ly == 1 and hn(int(xs + off) // 4, r, seed) % 9 == 0:
            k = "R5"
        if ly == 1 and hn(int(xs + off) // 4, r, seed + 1) % 13 == 0:
            k = "R3"
        return k

    # 軒下の影（壁の上の2ドット）
    for x in range(x0, x1 + 1):
        for k in (1, 2):
            c = g.get(x, top + k)
            if c.startswith("C") or c.startswith("J"):
                g.put(x, top + k, "E3" if k == 1 else ("C1" if hn(x, 9) % 2 else c))
    g.poly([(ex0, ey + 1), (ex1, ey + 1), (ex1 + sh, ry), (ex0 + sh, ry)], roof_front)
    # 軒のふち（下は暗い線、そのすぐ上は明るい鼻先）
    for x in range(ex0, ex1 + 1):
        g.put(x, ey + 1, "R1"); g.put(x, ey, "R2")
    # 棟（いちばん上。明るい棟瓦）
    for x in range(int(ex0 + sh), int(ex1 + sh) + 1):
        g.put(x, ry, "R6"); g.put(x, ry + 1, "R5")
    # 右のふち（破風）: 正面の軒の右はしから棟の右はしへ、さらに奥の軒へ下りる。厚み2ドット
    bx_end, by_end = ex1 + D, ey - D * SL
    for i in range(0, 101):
        t = i / 100
        x = ex1 + t * sh; y = ey + 1 + t * (ry - ey - 1)
        g.put(x, y, "R6"); g.put(x + 1, y, "R3")
        x2 = ex1 + sh + t * (D - sh); y2 = ry + t * (by_end - ry)
        g.put(x2, y2, "R5"); g.put(x2, y2 + 1, "R2"); g.put(x2, y2 + 2, "R1")
    # 破風の下の、妻壁に落ちる影
    for x in range(x1 + 1, xr + 1):
        u = x - x1
        if u <= D / 2:
            yg = top - (u / (D / 2)) * ridge_dy
        else:
            yg = top - D * SL - ((D - u) / (D / 2)) * (ridge_dy - D / 2 * SL)
        for dy in range(0, 3):
            y = int(math.ceil(yg)) + dy + 2
            c = g.get(x, y)
            if c.startswith("E") or c == "J3":
                g.put(x, y, "E1")
    # 左のふち（正面の軒の左はしから棟の左はしへ）
    for i in range(0, 101):
        t = i / 100
        g.put(ex0 + t * sh, ey + 1 + t * (ry - ey - 1), "R5")
    # ---- 屋根窓 ----
    if dormer:
        cx = x0 + int(FW * 0.5)
        dy = int(ey - 4)                               # 屋根窓のてっぺんが、棟より下に来るように
        g.poly([(cx - 6, dy), (cx - 6, dy - 8), (cx, dy - 13), (cx + 6, dy - 8), (cx + 6, dy)],
               lambda x, y: brick(x - cx + 6, y - dy + 30, True, seed + 3))
        window(cx - 3, dy - 7, 7, 6)
        for k in range(7):
            g.put(cx - 7 + k, dy - 8 - k, "R5"); g.put(cx - 7 + k, dy - 7 - k, "R2")
            g.put(cx + 7 - k, dy - 8 - k, "R3"); g.put(cx + 7 - k, dy - 7 - k, "R1")
    # ---- 煙突（レンガ。棟の近く、正面の屋根の上） ----
    chx = int(x0 + FW * chimney + sh * 0.7)
    cy0 = int(ry + span * 0.3)
    for y in range(int(ry) - 7, cy0 + 1):
        for x in range(chx - 3, chx + 4):
            if x <= chx + 1:
                g.put(x, y, brick(x - chx + 3, y - ry + 40, True, seed + 5))
            else:
                g.put(x, y, brick(x - chx, y - ry + 40, False, seed + 6))
    for x in range(chx - 4, chx + 5):
        g.put(x, int(ry) - 8, "K3" if x < chx + 2 else "K2"); g.put(x, int(ry) - 7, "K1")
    for x in range(chx - 3, chx + 4):
        g.put(x, int(ry) - 6, "SOOT")
    # 煙突のつけ根の、屋根の影
    for x in range(chx + 4, chx + 7):
        g.put(x, cy0 - 1, "R2") if g.get(x, cy0 - 1).startswith("R") else None
    # ---- 写実の追加: 屋根のこけ、壁のすす・こけ ----
    for _ in range(int(FW * 0.4)):
        x = rnd.randint(x0, x1); y = rnd.randint(int(ey - 5), int(ey - 1))
        if g.get(x, y) in ("R3", "R4", "R5"):
            g.put(x, y, "M2")
            if rnd.random() < 0.5:
                g.put(x + 1, y, "M1")
    for x in range(x0 + 2, x1 - 1):
        if hn(x, 5, seed) % 4 == 0 and g.get(x, bot).startswith("C"):
            g.put(x, bot, "M1")
            if hn(x, 6, seed) % 2 == 0 and g.get(x, bot - 1).startswith("C"):
                g.put(x, bot - 1, "M2")
    # ---- りんかく ----
    add = []
    for y in range(H):
        for x in range(W):
            if g.g[y][x] == "." and any(g.get(x + a, y + b) != "." for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                add.append((x, y))
    for x, y in add:
        g.g[y][x] = "A"
    # ---- 足もとの草（一本ずつ、高さと色をかえる） ----
    for x in range(x0 - 2, xr + 1):
        yb = (bot + 6) if x <= x1 + 1 else int(sideY(x, bot)) + 6
        if hn(x, 77, seed) % 5 < 3:
            h = 1 + hn(x, 78, seed) % 3
            for k in range(h):
                g.put(x, yb - k, "F1" if k == 0 else "F2")
    return g


letters = "BCDEFGHIJKLMNOPQRTUVXYZabcdefghijklmnopqrstuvwxyz0123456789"
names = list(pal)
mp = {n: (n if n == "A" else letters[i]) for i, n in enumerate(names)}


def save(name, g, palette=None):
    open(name + ".txt", "w").write("\n".join("".join("." if ch == "." else mp[ch] for ch in r) for r in g.g) + "\n")
    p = {mp[k]: v for k, v in (palette or pal).items()}
    json.dump(p, open("pal-" + name + ".json", "w"))


def variants(name, g):
    save(name, g)
    for nm, vv in (("blue", BLUE), ("green", GREEN)):
        save(name + "-" + nm, g, {**pal, **vv})


if __name__ == "__main__":
    variants("cottage-brick", build(56, 56, FW=39, D=12, floors=1, FH=22, RH=12, ox=2, door=None, nwin=2, ov=2, chimney=0.62, seed=3))
    variants("manor-brick", build(80, 80, FW=55, D=19, floors=2, FH=21, RH=14, door_h=16, ox=2, door=0.45, nwin=3, ov=2, porch=True, dormer=True, chimney=0.74, seed=8))
