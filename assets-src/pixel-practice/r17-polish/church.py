"""霧断崖の「環の聖堂」（教会）の絵を、一から描く（2026-10-05、人間の指示「司祭がいるなら教会もほしい。教会内ならエディタ使って細かく作って」）。

この世界の信仰は「環信仰」。十字などの現実の宗教のしるしは使わず、霧断崖の門の石柱に刻まれた「三つの環（いちばん小さな環だけが欠けている）」を、聖堂のしるしにする（第5章の場面の設定どおり）。
既存作品の聖堂・教会の絵は写していない。

出力（このフォルダ）:
  church.txt / pal-church.json                   … 外観（80×88）。町の地図の飾り `prop:church`
  church-interior.txt / pal-church-interior.json … 中（208×224＝13×14マス）。聖堂の中の地図の1枚絵 `prop:church-interior`
このあと、tools/pixel-practice/editor-draw.mjs でドット絵エディタに描き入れ、食い違い0マスを確かめる。
"""
import json
import math
import random
import os

import numpy as np

HERE = os.path.dirname(__file__)


class Grid:
    def __init__(self, w, h, fill="."):
        self.w, self.h = w, h
        self.a = np.full((h, w), fill, dtype="<U1")

    def put(self, x, y, c):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < self.w and 0 <= y < self.h:
            self.a[y, x] = c

    def rect(self, x0, y0, x1, y1, c):
        for y in range(max(0, y0), min(self.h, y1 + 1)):
            for x in range(max(0, x0), min(self.w, x1 + 1)):
                self.a[y, x] = c

    def hline(self, x0, x1, y, c):
        self.rect(x0, y, x1, y, c)

    def vline(self, x, y0, y1, c):
        self.rect(x, y0, x, y1, c)

    def ring(self, cx, cy, r, c, thick=1.0, dots=None):
        for y in range(int(cy - r - 2), int(cy + r + 3)):
            for x in range(int(cx - r - 2), int(cx + r + 3)):
                d = math.hypot(x - cx, y - cy)
                if abs(d - r) <= thick / 2:
                    self.put(x, y, c)

    def disk(self, cx, cy, r, c):
        for y in range(int(cy - r - 1), int(cy + r + 2)):
            for x in range(int(cx - r - 1), int(cx + r + 2)):
                if math.hypot(x - cx, y - cy) <= r:
                    self.put(x, y, c)

    def arch(self, x0, x1, top, bottom, c):
        """上が半円の、アーチ形の窓・扉（塗り）"""
        cx = (x0 + x1) / 2
        r = (x1 - x0) / 2
        for y in range(top, bottom + 1):
            for x in range(x0, x1 + 1):
                if y >= top + r or math.hypot(x - cx, (y - (top + r))) <= r + 0.3:
                    self.put(x, y, c)

    def get(self, x, y):
        return self.a[y, x] if 0 <= x < self.w and 0 <= y < self.h else "."

    def save(self, name, pal):
        with open(os.path.join(HERE, f"{name}.txt"), "w") as f:
            f.write("\n".join("".join(r) for r in self.a) + "\n")
        with open(os.path.join(HERE, f"pal-{name}.json"), "w") as f:
            json.dump(pal, f, ensure_ascii=False)
        used = set("".join("".join(r) for r in self.a)) - {"."}
        missing = used - set(pal)
        assert not missing, f"色の無い記号: {missing}"


def emblem(g, cx, cy, r, ring="G", ring_d="g", lamp="Y", core="W"):
    """環信仰のしるし（霧断崖の門の石柱と同じ）: 三つの環が重なり、いちばん小さな環だけが欠けている。
    大きい環から 1、2/3、1/3 の半径。欠けは、いちばん小さな環の右上。"""
    # 小さく描くときは、線を細くし、つぶれないよう環の間をあける（小さすぎるときは2つの環）
    radii = [r, r * 0.66, r * 0.33] if r >= 6 else [r, r * 0.45]
    for k, rr in enumerate(radii):
        th = 1.7 if r >= 10 else 1.0
        k = k if r >= 6 else (2 if k == 1 else 0)
        for y in range(int(cy - rr - 2), int(cy + rr + 3)):
            for x in range(int(cx - rr - 2), int(cx + rr + 3)):
                d = math.hypot(x - cx, y - cy)
                if abs(d - rr) > th / 2:
                    continue
                a = math.atan2(y - cy, x - cx)
                if k == 2 and -1.35 < a < -0.35:
                    continue          # 欠けている所
                shade = ring if (x - cx) + (y - cy) < 0 else ring_d
                g.put(x, y, shade)
    # 環のまん中に、小さな灯
    g.put(cx, cy, core)
    if r >= 6:
        g.put(cx + 1, cy, lamp); g.put(cx - 1, cy, lamp); g.put(cx, cy - 1, lamp); g.put(cx, cy + 1, lamp)


# ===================================================================== 外観（80×88）
def fill_poly(g, pts, c, cond=None):
    """多角形の中を塗る（cond(x, y) が真のマスだけ）"""
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    for y in range(int(min(ys)), int(max(ys)) + 1):
        for x in range(int(min(xs)), int(max(xs)) + 1):
            inside = False
            j = len(pts) - 1
            for i in range(len(pts)):
                xi, yi = pts[i]; xj, yj = pts[j]
                if (yi > y + 0.5) != (yj > y + 0.5):
                    xc = xi + (y + 0.5 - yi) * (xj - xi) / (yj - yi)
                    if x + 0.5 < xc:
                        inside = not inside
                j = i
            if inside and (cond is None or cond(x, y)):
                g.put(x, y, c)


def exterior():
    """町の家（manor4.py）と同じ見え方: 正面の破風と、右の奥へ遠ざかる身廊の横の壁（右へ行くほど上がる）。屋根の斜面・控え壁・石の土台・落ちる影で立体に。"""
    W, H = 80, 88
    g = Grid(W, H)
    pal = {
        "K": "#1e1a24",  # 輪郭
        "s": "#4a4c5c",  # 石の影
        "S": "#7a7c8c",  # 石
        "T": "#a8aab8",  # 石の明るい面
        "U": "#d4d6e0",  # 石のいちばん明るい所
        "j": "#5c5e6e",  # 横の壁の石（暗い面）
        "J": "#6a6c7c",  # 横の壁の石
        "r": "#243250",  # 屋根の影
        "R": "#36507a",  # 屋根
        "Q": "#5a78a8",  # 屋根の明るい所
        "q": "#2c3e62",  # 屋根の斜面（奥）
        "w": "#4a2a18",  # 木の扉の影
        "O": "#7a4a24",  # 木の扉
        "o": "#a86a34",  # 木の扉の明るい所
        "g": "#8a6418",  # 金の影
        "G": "#e0b040",  # 金
        "Y": "#fff0a0",  # 灯
        "W": "#ffffff",  # 光
        "b": "#2a4a88",  # ステンドグラス 青
        "c": "#4aa0d0",  # 水色
        "m": "#b04070",  # 紅
        "v": "#e8c060",  # 黄
        "n": "#3a3640",  # 石段・土台の影
        "N": "#6a6874",  # 石段
        "h": "#2c4a2c",  # つたの影
        "H": "#4a7a3a",  # つた
        "z": "#2a2a36",  # 地面の影
    }
    SL = 0.5                      # 横の壁の傾き（右へ1行くと0.5上がる＝奥へ遠ざかる）
    FX0, FX1 = 4, 50              # 正面の左右
    FOOT = 82                     # 正面の足もと
    EAVE = 46                     # 正面の軒の高さ
    APEX = 26                     # 破風のてっぺん
    D = 26                        # 奥行き（横の壁の幅）
    cx = (FX0 + FX1) / 2
    def side_y(x, y0):            # 正面の右の角から x だけ奥の、同じ高さの行
        return y0 - (x - FX1) * SL
    # ---- 地面の影（右の奥へ）
    fill_poly(g, [(FX0 + 2, FOOT + 3), (FX1 + D + 2, FOOT - D * SL + 3), (FX1 + D + 2, FOOT - D * SL + 5), (FX0 + 2, FOOT + 5)], "z")
    # ---- 横の壁（身廊。暗い石、右へ上がる石積み）
    fill_poly(g, [(FX1, EAVE), (FX1 + D, EAVE - D * SL), (FX1 + D, FOOT - D * SL), (FX1, FOOT)], "J")
    for x in range(FX1, FX1 + D + 1):
        for y in range(int(EAVE - (x - FX1) * SL), int(FOOT - (x - FX1) * SL) + 1):
            row = int(round(y + (x - FX1) * SL - EAVE))
            if row % 5 == 0 or ((x - FX1 + (row // 5) * 3) % 7 == 0):
                g.put(x, y, "j")
    # 横の壁の窓（細長いアーチを、傾きに合わせて）と控え壁
    for wx in (FX1 + 5, FX1 + 14):
        for x in range(wx, wx + 4):
            top = side_y(x, 54) - (1 if x in (wx + 1, wx + 2) else 0)
            for y in range(int(top), int(side_y(x, 70))):
                g.put(x, y, "b" if (y + x) % 5 else "c")
            g.put(x, int(side_y(x, 70)), "T")
        g.put(wx + 1, int(side_y(wx + 1, 56)), "v"); g.put(wx + 2, int(side_y(wx + 2, 56)), "m")
        for x in (wx - 1, wx + 4):
            for y in range(int(side_y(x, 53)), int(side_y(x, 71))):
                g.put(x, y, "K")
    for bx in (FX1 + 10, FX1 + 20):                     # 控え壁（壁から出っぱる柱。明るい正面と暗い側面）
        for x in range(bx, bx + 3):
            for y in range(int(side_y(x, 58)), int(side_y(x, FOOT)) + 1):
                g.put(x, y, "S" if x < bx + 2 else "s")
        g.put(bx, int(side_y(bx, 57)), "T"); g.put(bx + 1, int(side_y(bx + 1, 57)), "T")
    # 横の壁の土台
    for x in range(FX1, FX1 + D + 1):
        for k in range(3):
            g.put(x, int(side_y(x, FOOT - k)), "n" if k == 0 else "N")
    for x in range(FX1, FX1 + D + 1):
        g.put(x, int(side_y(x, FOOT + 1)), "K")
    g.vline(FX1 + D, int(EAVE - D * SL), int(FOOT - D * SL), "K")
    # ---- 屋根の斜面（右の奥へ。正面の破風から棟が奥へのびる）
    ridge_front = (cx, APEX); ridge_back = (cx + D, APEX - D * SL)
    eave_front = (FX1 + 2, EAVE + 1); eave_back = (FX1 + D + 2, EAVE + 1 - D * SL)
    fill_poly(g, [ridge_front, ridge_back, eave_back, eave_front], "R")
    for x in range(int(cx), FX1 + D + 3):           # 瓦の段（軒に平行な線）
        for y in range(0, H):
            if g.a[y, x] == "R":
                t = (y + (x - cx) * SL - APEX)
                if int(t) % 4 == 0:
                    g.put(x, y, "r")
                elif (x + int(t)) % 9 == 0:
                    g.put(x, y, "q")
    for x in range(int(cx), int(cx) + D + 1):       # 棟の線（正面のてっぺんから、奥へ）
        g.put(x, int(round(APEX - (x - cx) * SL)) - 1, "K")
        g.put(x, int(round(APEX - (x - cx) * SL)), "Q")
    for x in range(FX1 + 2, FX1 + D + 3):
        g.put(x, int(round(EAVE + 1 - (x - FX1 - 2) * SL)) + 1, "K")
    # ---- 正面（破風と壁。左から光）
    fill_poly(g, [(FX0, EAVE), (cx, APEX + 2), (FX1, EAVE), (FX1, FOOT), (FX0, FOOT)], "S")
    for y in range(APEX, FOOT + 1):
        for x in range(FX0, FX1 + 1):
            if g.a[y, x] != "S":
                continue
            row = (y - APEX) // 4
            off = 0 if row % 2 == 0 else 4
            if (y - APEX) % 4 == 0 or (x + off) % 8 == 0:
                g.put(x, y, "s")
            elif x < FX0 + 10 and (y - APEX) % 4 == 1:
                g.put(x, y, "T")
    g.rect(FX0, EAVE, FX0 + 2, FOOT, "T"); g.rect(FX1 - 2, EAVE, FX1, FOOT, "s")
    # 破風の縁取り（屋根の正面の厚み）
    for x in range(FX0 - 2, FX1 + 3):
        y = int(round(APEX + abs(x - cx) * (EAVE - APEX) / ((FX1 - FX0) / 2)))
        for k in range(3):
            g.put(x, y - k, "Q" if (x < cx and k == 2) else ("R" if k == 1 else "r"))
        g.put(x, y - 3, "K")
    g.vline(FX0 - 1, EAVE, FOOT, "K")
    # 正面の土台・石段
    g.rect(FX0, FOOT - 2, FX1, FOOT, "N"); g.hline(FX0, FX1, FOOT - 2, "T"); g.hline(FX0, FX1, FOOT + 1, "K")
    # ---- 正面のバラ窓（三つの環）
    g.disk(cx, 40, 6.5, "K"); g.disk(cx, 40, 5.6, "b")
    for y in range(33, 48):
        for x in range(int(cx) - 7, int(cx) + 8):
            d = math.hypot(x - cx, y - 40)
            if d <= 5.6:
                a = math.atan2(y - 40, x - cx)
                seg = int(((a + math.pi) / (2 * math.pi)) * 8) % 8
                g.put(x, y, ["c", "b", "m", "b", "v", "b", "m", "b"][seg] if d > 2 else "Y")
    emblem(g, cx, 40, 6.2)
    # 正面の左右の窓
    for wx in (FX0 + 6, FX1 - 10):
        g.arch(wx - 1, wx + 4, 52, 68, "K"); g.arch(wx, wx + 3, 53, 67, "b")
        for y in range(53, 68):
            for x in range(wx, wx + 4):
                if g.a[y, x] == "b" and (y + x) % 5 == 0:
                    g.put(x, y, "c")
        g.put(wx + 1, 55, "v"); g.put(wx + 2, 55, "m"); g.hline(wx - 1, wx + 4, 69, "T")
    # 正面の大きな扉（アーチ、両開き、石の飾り縁）
    g.arch(int(cx) - 9, int(cx) + 9, 55, FOOT - 3, "T")
    g.arch(int(cx) - 8, int(cx) + 8, 56, FOOT - 3, "K")
    g.arch(int(cx) - 7, int(cx) + 7, 57, FOOT - 3, "w")
    for y in range(57, FOOT - 2):
        for x in range(int(cx) - 6, int(cx) + 7):
            if g.a[y, x] == "w":
                g.put(x, y, "o" if x in (int(cx) - 5, int(cx) + 2) else ("O" if x not in (int(cx), int(cx) + 1) else "w"))
    g.vline(int(cx), 58, FOOT - 3, "K")
    for y in (64, 72):
        g.hline(int(cx) - 6, int(cx) + 6, y, "g")
    g.put(int(cx) - 2, 69, "G"); g.put(int(cx) + 3, 69, "G")
    emblem(g, cx, 61, 3.0)
    g.rect(int(cx) - 11, FOOT, int(cx) + 12, FOOT + 1, "N"); g.hline(int(cx) - 11, int(cx) + 12, FOOT, "U")
    g.hline(int(cx) - 11, int(cx) + 12, FOOT + 2, "n")
    # ---- 鐘楼（破風のうしろに立つ。正面の面と右の面）
    tx0, tx1, ttop = int(cx) - 6, int(cx) + 6, 6
    td = 6                                            # 塔の奥行き
    fill_poly(g, [(tx1, ttop + 2), (tx1 + td, ttop + 2 - td * SL), (tx1 + td, APEX + 4 - td * SL), (tx1, APEX + 4)], "J",
              cond=lambda x, y: g.a[y, x] in ".Rrq")
    g.rect(tx0, ttop + 2, tx1, APEX + 1, "S")
    for y in range(ttop + 2, APEX + 2):
        if (y - ttop) % 4 == 0:
            g.hline(tx0, tx1, y, "s")
    g.rect(tx0, ttop + 2, tx0 + 1, APEX + 1, "T")
    g.vline(tx0 - 1, ttop + 2, APEX + 2, "K"); g.vline(tx1 + td, int(ttop + 2 - td * SL), int(APEX + 4 - td * SL), "K")
    g.arch(tx0 + 3, tx1 - 3, ttop + 5, ttop + 14, "K"); g.arch(tx0 + 4, tx1 - 4, ttop + 6, ttop + 14, "n")
    g.rect(int(cx) - 1, ttop + 9, int(cx) + 1, ttop + 12, "G"); g.hline(int(cx) - 2, int(cx) + 2, ttop + 12, "g"); g.put(int(cx) - 1, ttop + 9, "Y")
    # 塔のとがり屋根（正面の三角と、右の面）
    for y in range(0, ttop + 3):
        half = (y * (tx1 - tx0 + 2)) / (2 * (ttop + 2))
        for x in range(int(cx - half), int(cx + half) + 1):
            g.put(x, y, "Q" if x < cx else "R")
        g.put(int(cx - half) - 1, y, "K")
        for x in range(int(cx + half) + 1, int(cx + half + y * 0.45) + 1):
            g.put(x, y, "r")          # とがり屋根の右の面（奥へ回りこむ暗い面）
        g.put(int(cx + half + y * 0.45) + 1, y, "K")
    g.put(cx, 0, "G"); g.put(cx, 1, "G")
    # ---- つた（正面の左の角）
    for (x, y) in [(5, 68), (6, 69), (5, 71), (7, 72), (6, 74), (5, 76), (8, 77), (6, 79), (7, 80), (9, 75)]:
        g.put(x, y, "H"); g.put(x + 1, y + 1, "h")
    g.save("church", pal)


# ===================================================================== 中（208×224＝13×14マス）
def interior():
    """奥行きのある聖堂の中（2026-10-05、人間の指示「教会の中も奥行きが欲しい。エディタ使って凝った教会にして」）。
    奥のまんなかに大きなアーチがあり、その向こうへ内陣が遠ざかる: 天井のリブ（肋骨のような梁）が奥へいくつも重なり、左右の壁は奥へすぼまり、
    床は奥へ上がっていく（1点に集まる見え方）。手前の身廊は、奥ほど目の細かい石畳（縦の目地も奥の1点へ集まる）、奥ほど細くなるじゅうたん、
    背もたれ・座面・影のある立体の長いす。奥ほど明るく、手前の角ほど暗い（点描のぼかし）。"""
    W, H = 208, 224
    T = 16
    CX = W / 2
    FLOOR_Y = 5 * T          # 身廊の床の、いちばん奥の行（ここから手前が歩ける）
    FRONT_Y = H - T          # 手前の壁
    g = Grid(W, H, "f")
    pal = {
        "K": "#16121c",  # 輪郭・いちばん暗い
        "k": "#241e2c",  # 天井の奥の暗がり
        "z": "#2a2430",  # 壁の影
        "Z": "#463c4c",  # 壁（奥）
        "y": "#5e5466",  # 壁の石
        "R": "#5a5066",  # 内陣の右の壁（かげ）
        "N": "#7a7088",  # 内陣の左の壁（ひなた）
        "Y": "#fff0a0",  # 灯
        "W": "#ffffff",  # 光
        "f": "#6e6876",  # 床の石
        "j": "#5e5866",  # 床の石（暗いところ）
        "F": "#827c8a",  # 床の石（明るい）
        "e": "#5a5462",  # 床の目地
        "E": "#9a94a2",  # 床の光
        "c": "#6a1a24",  # じゅうたんの影
        "C": "#9a2a32",  # じゅうたん
        "D": "#c44a4a",  # じゅうたんの明るい所
        "g": "#8a6418",  # 金の影
        "G": "#e0b040",  # 金
        "h": "#f8d878",  # 金の光
        "w": "#3e2414",  # 木の影
        "O": "#6e4222",  # 木（長いす）
        "o": "#9a6234",  # 木の明るい所
        "q": "#c08a4a",  # 木のいちばん明るい所
        "P": "#8a8898",  # 柱
        "Q": "#b8b6c4",  # 柱の明るい所
        "b": "#203c80",  # ステンドグラス 青
        "B": "#3a6ac0",  # ステンドグラス 青（明）
        "n": "#3aa0c8",  # 水色
        "m": "#a03466",  # 紅
        "M": "#d05a8a",  # 紅（明）
        "v": "#e8c060",  # 黄
        "u": "#4a2a6a",  # 旗の影（むらさき）
        "U": "#6a3a96",  # 旗
        "V": "#9a6ac8",  # 旗の明るい所
        "L": "#fffbe6",  # 祭壇の布
        "l": "#d8d0bc",  # 祭壇の布の影
        "s": "#3a3640",  # 段の影
        "S": "#9c98a6",  # 段
        "T": "#c4c0cc",  # 段の明るい所
        "r": "#fff6c8",  # 光の筋
        "i": "#6a6878",  # 柱の影の面
        "I": "#dcdae6",  # 柱のいちばん明るい筋
        "x": "#4c4a58",  # 柱の溝・いちばん暗い面
        "a": "#ff9a3c",  # ろうそくの炎（外）
        "A": "#ffe060",  # 炎（中）
    }
    B4 = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]

    def dith(x, y, amount):
        return amount * 16 > B4[y % 4][x % 4] + 0.5

    # ---------------- 身廊の床（石の板を1枚ずつ描く: 左上のふちに光・右下のふちに影・ひびや欠け。
    #                  奥ほど低い列、縦の目地は奥の1点へ集まる。明るさは板ごとに1色で、点描はしない）
    VPY = -160
    slabs = []
    y = FLOOR_Y
    ri = 0
    while y < H:
        hgt = 9 + (min(y, FRONT_Y) - FLOOR_Y) * 7 / (FRONT_Y - FLOOR_Y)
        slabs.append((ri, int(round(y)), min(int(round(y + hgt)), H)))
        y += hgt
        ri += 1
    for (ri, y0, y1) in slabs:
        ym = (y0 + y1) / 2
        s = (ym - VPY) / (FRONT_Y - VPY)
        off = 14 if ri % 2 else 0
        xs = sorted({int(round(CX + (k * 28 - off) * s)) for k in range(-7, 8)})
        for a, b in zip(xs, xs[1:]):
            mx = (a + b) / 2
            dist = math.hypot(mx - CX, (ym - FLOOR_Y) * 1.5)
            h = (a * 31 + ri * 17) % 7
            base = "F" if dist < 52 else ("j" if dist > 150 else "f")
            if h == 0 and base == "f":
                base = "F"
            if h == 3 and base == "f" and dist > 105:
                base = "j"
            hi = {"F": "E", "f": "F", "j": "f"}[base]
            lo = {"F": "f", "f": "j", "j": "e"}[base]
            for yy in range(y0, y1):
                for x in range(max(0, a), min(W, b)):
                    if yy == y0 or x == a:
                        c = "e"                      # 目地
                    elif yy == y0 + 1 or x == a + 1:
                        c = hi                       # 左上のふち（光）
                    elif yy == y1 - 1 or x == b - 1:
                        c = lo                       # 右下のふち（影）
                    else:
                        c = base
                    g.a[yy, x] = c
            # ひび（何枚かに1枚。ジグザグに下りる線と、その右の光）
            if h in (2, 5) and b - a > 12 and y1 - y0 > 8:
                px, py = a + 4 + (h * 7 + ri * 3) % max(1, b - a - 9), y0 + 2
                for step in range(y1 - y0 - 4):
                    g.put(px, py, "e")
                    g.put(px + 1, py, hi)
                    py += 1
                    if (h + step) % 3 == 0:
                        px += 1 if h == 2 else -1
            if h == 4 and b - a > 6:
                g.put(b - 2, y1 - 2, "e"); g.put(b - 3, y1 - 2, lo); g.put(b - 2, y1 - 3, lo)   # 角の欠け

    # ---------------- 奥の壁（0〜4マス目）。石を1つずつ: 上のふちに光、ところどころ明るい石・欠けた石
    g.rect(0, 0, W - 1, FLOOR_Y - 1, "Z")
    for yy in range(FLOOR_Y):
        for x in range(W):
            off = 0 if (yy // 6) % 2 == 0 else 6
            lx, ly = (x + off) % 12, yy % 6
            h = (((x + off) // 12) * 7 + (yy // 6) * 13) % 11
            if ly == 0 or lx == 0:
                c = "z"
            elif h == 0:
                c = "N" if ly == 1 and lx < 9 else "y"
            elif ly == 1 and lx < 8:
                c = "y"
            elif h == 5 and lx >= 9 and ly >= 4:
                c = "z"
            else:
                c = "Z"
            g.put(x, yy, c)

    def glass(x0, x1, top, bottom, big=False):
        """ステンドグラス: 外のふちは黄と紅の帯、鉛の線、青い菱形の地、まるい絵（メダル）。大きい窓は光の放射。"""
        cxw = (x0 + x1) / 2
        rw = (x1 - x0) / 2

        def win(x, yy):
            return x0 <= x <= x1 and top <= yy <= bottom and (yy >= top + rw or math.hypot(x - cxw, yy - (top + rw)) <= rw + 0.3)
        g.arch(x0 - 1, x1 + 1, top - 1, bottom + 1, "K")
        for yy in range(top, bottom + 1):
            for x in range(x0, x1 + 1):
                if not win(x, yy):
                    continue
                layer = 0
                while layer < 3 and all(win(x + dx * (layer + 1), yy + dy * (layer + 1)) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    layer += 1
                if layer == 0:
                    c = "v" if ((x + yy) // 4) % 2 == 0 else "m"
                elif layer == 1:
                    c = "K"
                elif big:
                    ang = math.atan2(yy - (top + rw), x - cxw)
                    d = math.hypot(x - cxw, yy - (top + rw))
                    sec = int((ang + math.pi) / (math.pi / 8))
                    if d < 2.5:
                        c = "Y"
                    elif ((ang + math.pi) % (math.pi / 8)) < 0.09:
                        c = "v" if d < 9 else "z"            # 光の線（まん中の近くは金、外は鉛）
                    else:
                        c = ["b", "B"][sec % 2] if d < 12 else ["B", "n"][sec % 2]
                else:
                    if (x + yy) % 6 == 0 or (x - yy) % 6 == 0:
                        c = "z"
                    else:
                        c = "b" if (((x + yy) // 6) + ((x - yy) // 6)) % 2 else "B"
                g.put(x, yy, c)
        if not big:
            for k, (cyk, fill, fill_d, core) in enumerate(((top + rw, "M", "m", "v"), (top + rw + 12, "n", "B", "W"), (top + rw + 24, "M", "m", "v"))):
                if cyk + 5 > bottom:
                    continue
                for yy in range(int(cyk) - 5, int(cyk) + 6):
                    for x in range(int(cxw) - 5, int(cxw) + 6):
                        d = math.hypot(x - cxw, yy - cyk)
                        if d <= 4.6:
                            g.put(x, yy, "K" if d > 3.6 else (core if 1.4 < d < 2.6 else (fill if (x - cxw) + (yy - cyk) < 0 else fill_d)))
        g.hline(x0 - 2, x1 + 2, bottom + 2, "T"); g.hline(x0 - 2, x1 + 2, bottom + 3, "s")      # 窓の下の石の台

    def stone_arch(x0a, x1a, top):
        cxa = (x0a + x1a) / 2
        ra = (x1a - x0a) / 2 + 1
        for yy in range(int(top - 3), int(top + ra + 2)):
            for x in range(x0a - 4, x1a + 5):
                d = math.hypot(x - cxa, yy - (top + ra))
                if yy <= top + ra and ra + 0.5 <= d <= ra + 2.5:
                    ang = math.atan2(yy - (top + ra), x - cxa)
                    g.put(x, yy, "K" if int((ang + math.pi) * 7) % 3 == 0 else ("T" if x < cxa else "S"))

    # 左右の奥の壁の、細長いステンドグラス
    for wcx in (18, 190):
        glass(wcx - 8, wcx + 8, 12, 50)
        stone_arch(wcx - 10, wcx + 10, 10)

    # ---------------- 内陣（アーチの向こうへ遠ざかる。t=0 が手前のアーチ、t=1 が奥の壁）
    def contour(t):
        return 56 - 14 * t, 48 - 26 * t, 64 - 14 * t      # 半円の中心の高さ・半径・床の線

    def inside(t, x, yy):
        cy, r, yb = contour(t)
        dx = abs(x + 0.5 - CX)
        if dx > r or yy > yb:
            return False
        return yy >= cy or math.hypot(dx, yy + 0.5 - cy) <= r

    for yy in range(0, 66):
        for x in range(W):
            if not inside(0, x, yy):
                continue
            if inside(1, x, yy):
                # 奥の壁（明るい石）
                off = 0 if (yy // 5) % 2 == 0 else 5
                g.put(x, yy, "R" if yy % 5 == 0 or (x + off) % 10 == 0 else "N")
                continue
            lo, hi = 0.0, 1.0
            for _ in range(18):
                mid = (lo + hi) / 2
                if inside(mid, x, yy):
                    lo = mid
                else:
                    hi = mid
            t = lo
            cy, r, yb = contour(hi)
            dx = abs(x + 0.5 - CX)
            f4 = (t * 3) % 1.0
            if yy > yb:
                # 内陣の床（白と灰の市松。奥へ細かく）
                u = (x + 0.5 - CX) / (r / 48)
                f7 = (t * 7) % 1.0
                if f7 < 0.14:
                    c = "s"
                else:
                    c = "T" if (int(math.floor(u / 10)) + int(t * 7)) % 2 == 0 else "S"
            elif dx > r and yy >= cy:
                # 左右の壁: リブの柱・石の目地・細長い窓
                left = x < CX
                v = (yy - cy) / max(1.0, yb - cy)
                if f4 < 0.10:
                    c = "Q" if left else "P"
                elif f4 < 0.17:
                    c = "i" if left else "x"
                elif 0.40 < f4 < 0.66 and 0.12 < v < 0.62:
                    c = ("n" if (x + yy) % 3 else "W") if left else ("B" if (x + yy) % 3 else "n")
                elif 0.36 < f4 < 0.70 and 0.06 < v < 0.68:
                    c = "K"
                elif (v * 8) % 1.0 < 0.14:
                    c = "R" if left else "Z"
                else:
                    c = "N" if left else "R"
            else:
                # 天井（暗い丸天井に、奥へ重なるリブと、まんなかの背骨のリブ、金の星）
                if f4 < 0.16:
                    c = "T" if x < CX else "S"
                elif f4 < 0.24:
                    c = "s"
                elif abs(x + 0.5 - CX) < 1.0:
                    c = "S"
                elif f4 < 0.30 and abs(x + 0.5 - CX) < 2.5:
                    c = "G"                                   # リブと背骨が交わる所の金の飾り
                else:
                    c = ["y", "Z", "z"][min(2, int(t * 3))]   # 奥のくぼみほど暗く（区切りごとに1色）
            g.put(x, yy, c)
    # 手前のアーチの石（くさび石と、まんなかの要石）
    ACY, AR = 56, 48
    for yy in range(0, 66):
        for x in range(W):
            dx = x + 0.5 - CX
            if yy < ACY:
                d = math.hypot(dx, yy + 0.5 - ACY)
                if AR + 0.3 <= d <= AR + 5:
                    ang = math.atan2(yy + 0.5 - ACY, dx)
                    edge = d > AR + 4
                    blk = int((ang + math.pi) / 0.26)
                    joint = (ang + math.pi) % 0.26 < 0.045
                    if edge or d < AR + 1.0:
                        c = "K"
                    elif joint:
                        c = "z"
                    elif dx < 0:
                        c = "T" if d < AR + 2.6 or blk % 2 else "S"
                    else:
                        c = "S" if d < AR + 2.6 or blk % 2 else "P"
                    g.put(x, yy, c)
            elif AR + 0.3 <= abs(dx) <= AR + 5:
                g.put(x, yy, "K" if abs(dx) > AR + 4 or abs(dx) < AR + 1.2 else ("s" if yy % 7 == 0 else ("T" if dx < 0 else "S")))
    g.rect(int(CX) - 4, 2, int(CX) + 3, 10, "T"); g.vline(int(CX) + 3, 2, 10, "S"); g.hline(int(CX) - 4, int(CX) + 3, 10, "s")
    g.rect(int(CX) - 5, 1, int(CX) + 4, 1, "K")
    emblem(g, CX, 6, 2.6, ring="G", ring_d="g", lamp="h", core="W")
    # 奥の壁の大きなステンドグラスと、灯の環
    glass(94, 114, 23, 46, big=True)
    emblem(g, CX, 33, 8, ring="G", ring_d="g", lamp="Y", core="W")
    # 祭壇（上の面・前の面。白い布と金のふち）
    g.rect(84, 43, 124, 46, "L"); g.hline(84, 124, 43, "W")
    g.rect(84, 47, 124, 57, "l"); g.hline(84, 124, 47, "G"); g.hline(84, 124, 48, "h"); g.hline(84, 124, 57, "g")
    for x in range(88, 122, 6):
        g.vline(x, 50, 56, "L")
    # 祭壇の前の垂れ布（むらさきの地、金のふち、すそのふさ、灯の環）
    g.rect(96, 48, 112, 58, "U"); g.vline(96, 48, 58, "V"); g.vline(112, 48, 58, "u")
    g.hline(96, 112, 48, "G"); g.vline(97, 49, 57, "g"); g.vline(111, 49, 57, "g")
    for x in range(96, 113, 2):
        g.put(x, 59, "G"); g.put(x + 1, 59, "g")
    emblem(g, CX, 53, 3.4, ring="G", ring_d="g", lamp="h", core="W")
    for cx in (88, 96, 111, 119):
        g.rect(cx, 38, cx + 1, 44, "L")
        g.put(cx, 37, "A"); g.put(cx + 1, 37, "a"); g.put(cx, 36, "Y"); g.put(cx, 35, "a")
        g.hline(cx - 1, cx + 2, 44, "g")
    # 内陣の手前の、背の高い燭台（左右）
    for cx in (66, 141):
        g.rect(cx, 30, cx + 1, 62, "g"); g.vline(cx, 30, 62, "G")
        g.hline(cx - 3, cx + 4, 63, "g"); g.hline(cx - 2, cx + 3, 64, "G")
        g.hline(cx - 4, cx + 5, 30, "G"); g.hline(cx - 4, cx + 5, 31, "g")
        for k in (-4, 0, 4):
            g.rect(cx + k, 25, cx + k + 1, 29, "L")
            g.put(cx + k, 24, "A"); g.put(cx + k + 1, 24, "a"); g.put(cx + k, 23, "Y"); g.put(cx + k + 1, 22, "a")

    # ---------------- 奥の壁の飾りの帯と、すその台石（アーチの外だけ）
    for x in range(W):
        if abs(x + 0.5 - CX) <= AR + 5:
            continue
        g.put(x, 56, "T"); g.put(x, 57, "S"); g.put(x, 58, "s" if x % 4 < 2 else "S")
        g.put(x, 72, "T"); g.rect(x, 73, x, 78, "S"); g.put(x, 79, "s")
    # ---------------- 祭壇へ上がる段（3段。下ほど広い）
    for (sy0, sy1, sx0, sx1) in ((64, 68, 54, 154), (69, 73, 46, 162), (74, 80, 38, 170)):
        g.rect(sx0, sy0, sx1, sy1, "S")
        g.hline(sx0, sx1, sy0, "T"); g.hline(sx0, sx1, sy1, "s")
        g.vline(sx0, sy0, sy1, "T"); g.vline(sx1, sy0, sy1, "s")
    g.hline(38, 170, 81, "e")
    # じゅうたんは段の上まで（段ごとに、上のふちが明るく、下のふちが暗い。金の押さえ棒）
    for (sy0, sy1) in ((64, 68), (69, 73), (74, 80)):
        for yy in range(sy0, sy1 + 1):
            for x in range(90, 118):
                c = "D" if yy == sy0 else ("c" if yy == sy1 else "C")
                if x in (90, 117):
                    c = "c"
                elif x == 91 and yy != sy1:
                    c = "G"
                elif x == 116 and yy != sy1:
                    c = "g"
                g.put(x, yy, c)
        g.hline(91, 116, sy0 + 1, "g"); g.put(90, sy0 + 1, "G"); g.put(117, sy0 + 1, "G")

    def column(cx, base_y, top_y, width=10, sconce=0):
        """丸い柱: 台座（2段）・金の飾り帯・溝のある円柱（左から光、右へ暗く）・柱頭。床に右へ影。"""
        x0 = cx - width // 2
        for yy in range(base_y - 2, base_y + 1):
            for x in range(x0 + width + 3, x0 + width + 7):
                if g.get(x, yy) in "fFjE":
                    g.put(x, yy, "j")
        g.rect(x0 - 3, base_y - 3, x0 + width + 2, base_y, "S"); g.hline(x0 - 3, x0 + width + 2, base_y - 3, "T"); g.hline(x0 - 3, x0 + width + 2, base_y, "s")
        g.vline(x0 - 3, base_y - 3, base_y, "T"); g.vline(x0 + width + 2, base_y - 3, base_y, "s")
        g.rect(x0 - 1, base_y - 6, x0 + width, base_y - 4, "P"); g.hline(x0 - 1, x0 + width, base_y - 6, "Q"); g.vline(x0 + width, base_y - 6, base_y - 4, "i")
        g.hline(x0, x0 + width - 1, base_y - 7, "G"); g.put(x0 + width - 1, base_y - 7, "g")
        tones = ["x", "Q", "I", "Q", "P", "P", "P", "i", "i", "x"]
        for k in range(width):
            tn = tones[int(k * len(tones) / width)]
            for yy in range(top_y + 6, base_y - 7):
                c = tn
                if k % 3 == 2 and tn not in ("I", "x"):
                    c = "i" if tn in ("P", "Q") else "x"
                g.put(x0 + k, yy, c)
        g.hline(x0, x0 + width - 1, top_y + 5, "G"); g.hline(x0, x0 + width - 1, top_y + 6, "g")
        g.rect(x0 - 1, top_y + 3, x0 + width, top_y + 4, "P"); g.put(x0 - 1, top_y + 3, "Q"); g.put(x0 + width, top_y + 4, "i")
        g.rect(x0 - 3, top_y, x0 + width + 2, top_y + 2, "S"); g.hline(x0 - 3, x0 + width + 2, top_y, "T"); g.hline(x0 - 3, x0 + width + 2, top_y + 2, "s")
        g.put(x0 - 2, top_y + 1, "G"); g.put(x0 + width + 1, top_y + 1, "G")
        if sconce:
            sy = (top_y + base_y) // 2
            sx = x0 + width if sconce > 0 else x0 - 1
            for k in range(3):
                g.put(sx + sconce * k, sy, "g"); g.put(sx + sconce * k, sy + 1, "G" if k == 2 else "g")
            tip = sx + sconce * 2
            g.put(tip, sy - 1, "L"); g.put(tip, sy - 2, "L"); g.put(tip, sy - 3, "A"); g.put(tip, sy - 4, "a")
            g.put(tip - sconce, sy - 3, "r"); g.put(tip + sconce, sy - 3, "r")

    # アーチの左右の大柱
    for gcx in (40, 168):
        column(gcx, 79, 4, width=10)

    # ---------------- 光の筋（左右の窓から、内がわの床へ、ななめに。床の板の色を1段だけ明るくする）
    LIGHTER = {"j": "f", "f": "F", "F": "E", "E": "E"}
    for (sx, dirx) in ((26, 1), (182, -1)):
        for yy in range(FLOOR_Y + 2, FRONT_Y - 24):
            k = yy - FLOOR_Y
            half = 6 if k < 60 else 5
            c0 = sx + dirx * k * 0.4
            for x in range(int(c0 - half), int(c0 + half)):
                if 0 <= x < W and g.a[yy, x] in LIGHTER:
                    v = LIGHTER[g.a[yy, x]]
                    if abs(x + 0.5 - c0) < half - 2.5 and v in LIGHTER:
                        v = LIGHTER[v]                      # 光の芯は、もう1段明るく
                    g.put(x, yy, v)

    # ---------------- 左右の壁（壁の上の面・内がわの面。柱・壁のくぼみの灯・旗）
    for side in (0, 1):
        x0 = 0 if side == 0 else W - T
        g.rect(x0, FLOOR_Y, x0 + T - 1, FRONT_Y + 1, "Z")
        for yy in range(FLOOR_Y, FRONT_Y + 1):
            if yy % 6 == 0:
                g.hline(x0, x0 + T - 1, yy, "z")
        if side == 0:
            g.rect(12, FLOOR_Y, 14, FRONT_Y, "y"); g.vline(15, FLOOR_Y, FRONT_Y, "K")
        else:
            g.rect(W - T + 1, FLOOR_Y, W - T + 3, FRONT_Y, "z"); g.vline(W - T, FLOOR_Y, FRONT_Y, "K")
        # 壁ぎわの床の影（壁の足もとが暗く）
        for yy in range(FLOOR_Y, FRONT_Y):
            for k in range(1, 5):
                x = (T - 1 + k) if side == 0 else (W - T - k)
                if k == 1 and g.a[yy, x] in "fFjE":
                    g.put(x, yy, "e")
                elif k == 2 and g.a[yy, x] in "fFE":
                    g.put(x, yy, "j")
        # 壁のくぼみ（灯）
        nx0 = x0 + 3
        g.arch(nx0, nx0 + 8, 102, 116, "K")
        g.arch(nx0 + 1, nx0 + 7, 103, 116, "k")
        g.vline(nx0 + 1 if side == 0 else nx0 + 7, 107, 116, "R")
        g.hline(nx0, nx0 + 8, 117, "T")
        g.rect(nx0 + 4, 111, nx0 + 4, 116, "L"); g.put(nx0 + 4, 110, "A"); g.put(nx0 + 4, 109, "a"); g.put(nx0 + 3, 110, "r"); g.put(nx0 + 5, 110, "r")
        # むらさきの旗
        bx = x0 + (3 if side == 0 else 6)
        for yy in range(151, 172):
            for x in range(bx, bx + 7):
                g.put(x, yy, "V" if x == bx else ("U" if x < bx + 5 else "u"))
        for x in range(bx, bx + 7, 2):
            g.put(x, 172, "u")
        g.hline(bx - 1, bx + 7, 150, "G")
        emblem(g, bx + 3, 160, 2.4, ring="G", ring_d="g", lamp="h", core="W")
        for base in (100, 150, 200):
            column(x0 + 8, base, base - 30, width=8, sconce=1 if side == 0 else -1)

    # ---------------- じゅうたん（扉から段へ。石のふち・金の縁どり・左に光・右に影・菱形の模様）
    CL, CR = 90, 117
    for yy in range(FLOOR_Y + 2, FRONT_Y + 1):
        for x in range(CL - 3, CR + 4):
            if x == CL - 3:
                c = "T"
            elif x == CL - 2:
                c = "S"
            elif x == CR + 2:
                c = "S"
            elif x == CR + 3:
                c = "s"
            elif x in (CL - 1, CR + 1):
                c = "e"
            elif x in (CL, CR):
                c = "c"
            elif x == CL + 1:
                c = "h" if yy % 6 == 0 else "G"
            elif x == CR - 1:
                c = "G" if yy % 6 == 0 else "g"
            elif x in (CL + 2, CR - 2):
                c = "c"
            elif x == CL + 4:
                c = "D"
            elif x >= CR - 4:
                c = "c" if x == CR - 3 else "C"
            else:
                c = "C"
            g.put(x, yy, c)
    DIAMOND = ["...g...",
               "..gGg..",
               ".gGDGg.",
               "gGD.DGg",
               ".gGDGg.",
               "..gGg..",
               "...g..."]
    for my in range(FLOOR_Y + 26, FRONT_Y - 8, 18):
        for dy, row in enumerate(DIAMOND):
            for dx, ch in enumerate(row):
                if ch != ".":
                    g.put(100 + dx, my + dy, ch)
        for (px, py) in ((95, my + 3), (111, my + 3), (103, my + 12)):
            g.put(px, py, "D"); g.put(px + 1, py, "c")
    for x in range(CL + 1, CR, 2):                                # 段の前のふさ
        g.put(x, FLOOR_Y + 2, "G"); g.put(x + 1, FLOOR_Y + 2, "D")
    # 祭壇の前の床の、象眼の環（司祭が立つ所）
    emblem(g, CX, FLOOR_Y + 8, 7, ring="h", ring_d="g", lamp="G", core="W")

    # ---------------- 長いす（左右に4列ずつ。木目・彫りの板・はしの飾り板・床の影を、1ドットずつ）
    rndw = random.Random(5)
    END = ["..G..",
           ".whw.",
           "wqoOw",
           "wqoOw",
           "wqgOw",
           "wgGgw",
           "wqgOw",
           "wqoOw",
           "wqOOw",
           "wqoOw",
           "wqOOw",
           "wqOOw",
           "wqoOw",
           "wqOOw",
           "wqOww",
           ".www."]
    for row in range(4):
        y0 = 7 * T + 2 + row * 20
        for (px0, px1) in ((20, 76), (132, 188)):
            for x in range(px0 + 1, px1 + 3):                             # 床の影（右下へ）
                for yy, c in ((y0 + 14, "e"), (y0 + 15, "e"), (y0 + 16, "j")):
                    if g.a[yy, x] in "fFjE":
                        g.put(x, yy, c)
            g.hline(px0, px1, y0, "q")                                    # 背もたれの上の木（光）
            g.hline(px0, px1, y0 + 1, "o")
            g.rect(px0, y0 + 2, px1, y0 + 4, "O")                         # 背もたれの板
            for x in range(px0 + 2, px1 - 1, 11):                         # 彫りの板（へこみ: 上と左が影、下と右が光）
                g.hline(x, x + 7, y0 + 2, "w"); g.vline(x, y0 + 2, y0 + 4, "w")
                g.hline(x + 1, x + 7, y0 + 4, "o"); g.vline(x + 7, y0 + 3, y0 + 4, "o")
                g.put(x + 4, y0 + 3, "g")
            g.hline(px0, px1, y0 + 5, "w")
            g.hline(px0, px1, y0 + 6, "w")                                # 背もたれと座面のすき間
            g.hline(px0, px1, y0 + 7, "q")                                # 座面
            g.rect(px0, y0 + 8, px1, y0 + 9, "o")
            g.rect(px0, y0 + 10, px1, y0 + 10, "O")
            g.hline(px0, px1, y0 + 11, "w")
            for yy in (y0 + 1, y0 + 8, y0 + 9):                           # 木目（長さのちがう線）
                x = px0 + rndw.randint(1, 6)
                while x < px1 - 3:
                    ln = rndw.randint(3, 8)
                    for k in range(ln):
                        if x + k < px1:
                            g.put(x + k, yy, "O" if yy != y0 + 1 else "O")
                    x += ln + rndw.randint(5, 12)
            for lx in (px0 + 3, (px0 + px1) // 2, px1 - 4):              # 脚
                g.rect(lx, y0 + 12, lx + 1, y0 + 13, "w"); g.put(lx, y0 + 12, "O")
            for ex in (px0 - 2, px1 - 2):                                 # 両はしの飾り板
                for dy, rowc in enumerate(END):
                    for dx, ch in enumerate(rowc):
                        if ch != ".":
                            g.put(ex + dx, y0 - 2 + dy, ch)

    # ---------------- 扉のそばの、聖水の鉢（左右）
    for bcx in (2 * T + 8, 10 * T + 8):
        for yy in range(203, 208):
            for x in range(bcx - 6, bcx + 9):
                if ((x + 0.5 - bcx - 1.5) / 7) ** 2 + ((yy + 0.5 - 205) / 2.2) ** 2 <= 1 and g.a[yy, x] in "fFjE":
                    g.put(x, yy, "e")
        g.rect(bcx - 2, 198, bcx + 2, 205, "P"); g.vline(bcx - 2, 198, 205, "Q"); g.vline(bcx + 2, 198, 205, "i")
        g.rect(bcx - 4, 205, bcx + 4, 206, "S"); g.hline(bcx - 4, bcx + 4, 206, "s")
        for yy in range(192, 199):
            for x in range(bcx - 8, bcx + 9):
                d = ((x + 0.5 - bcx - 0.5) / 7.5) ** 2 + ((yy + 0.5 - 194.5) / 3.2) ** 2
                if d <= 1:
                    g.put(x, yy, "Q" if yy < 195 else ("P" if yy < 198 else "i"))
        for yy in range(193, 196):
            for x in range(bcx - 6, bcx + 7):
                if ((x + 0.5 - bcx - 0.5) / 5.5) ** 2 + ((yy + 0.5 - 194.5) / 1.6) ** 2 <= 1:
                    g.put(x, yy, "n")
        g.put(bcx - 2, 194, "W"); g.put(bcx + 2, 195, "B")

    # ---------------- 手前の壁（上の面の石を1つずつ）と、両開きの扉（石の枠・木の板・金具）
    g.rect(0, FRONT_Y + 2, W - 1, H - 1, "Z")
    for yy in range(FRONT_Y + 4, H):
        for x in range(W):
            off = 0 if ((yy - FRONT_Y - 4) // 5) % 2 == 0 else 7
            lx, ly = (x + off) % 14, (yy - FRONT_Y - 4) % 5
            h = (((x + off) // 14) * 5 + (yy // 5) * 3) % 7
            g.put(x, yy, "z" if lx == 0 or ly == 4 else ("y" if ly == 0 or h == 0 else "Z"))
    g.hline(0, W - 1, FRONT_Y + 2, "K"); g.hline(0, W - 1, FRONT_Y + 3, "N")
    dx0, dx1 = 6 * T - 2, 7 * T + 1
    g.rect(dx0 - 4, FRONT_Y + 1, dx1 + 4, H - 1, "S"); g.vline(dx0 - 4, FRONT_Y + 1, H - 1, "T"); g.vline(dx1 + 4, FRONT_Y + 1, H - 1, "s")
    g.hline(dx0 - 4, dx1 + 4, FRONT_Y + 1, "T")
    g.rect(dx0 - 1, FRONT_Y + 2, dx1 + 1, H - 1, "K")
    g.rect(dx0, FRONT_Y + 3, dx1, H - 1, "O")
    for x in range(dx0, dx1 + 1):
        if (x - dx0) % 4 == 0:
            g.vline(x, FRONT_Y + 3, H - 1, "w")                 # 板のつなぎ目
        elif (x - dx0) % 4 == 1:
            g.vline(x, FRONT_Y + 3, H - 1, "o")
    mid = (dx0 + dx1) // 2
    g.vline(mid, FRONT_Y + 3, H - 1, "K"); g.vline(mid + 1, FRONT_Y + 3, H - 1, "w")
    for yy in (FRONT_Y + 6, H - 4):                              # 金の帯
        g.hline(dx0, dx1, yy, "g"); g.hline(dx0, mid - 1, yy, "G")
    g.put(mid - 2, FRONT_Y + 10, "h"); g.put(mid + 3, FRONT_Y + 10, "G")        # 取っ手
    g.rect(dx0 + 2, FRONT_Y - 3, dx1 - 2, FRONT_Y, "c"); g.hline(dx0 + 2, dx1 - 2, FRONT_Y - 3, "D")
    for x in range(dx0 + 2, dx1 - 1, 2):
        g.put(x, FRONT_Y - 4, "G")                               # 入口のマットのふさ
    g.save("church-interior", pal)


if __name__ == "__main__":
    exterior()
    interior()
    print("ok")
