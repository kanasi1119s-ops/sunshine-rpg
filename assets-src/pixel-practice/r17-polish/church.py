"""霧断崖の「環の聖堂」（教会）の絵を、一から描く（2026-10-05、人間の指示「司祭がいるなら教会もほしい。教会内ならエディタ使って細かく作って」）。

この世界の信仰は「環信仰」。十字などの現実の宗教のしるしは使わず、霧断崖の門の石柱に刻まれた「三つの環（いちばん小さな環だけが欠けている）」を、聖堂のしるしにする（第5章の場面の設定どおり）。
既存作品の聖堂・教会の絵は写していない。

出力（このフォルダ）:
  church.txt / pal-church.json                   … 外観（80×88）。町の地図の飾り `prop:church`
  church-interior.txt / pal-church-interior.json … 中（208×176＝13×11マス）。聖堂の中の地図の1枚絵 `prop:church-interior`
このあと、tools/pixel-practice/editor-draw.mjs でドット絵エディタに描き入れ、食い違い0マスを確かめる。
"""
import json
import math
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


# ===================================================================== 中（208×176＝13×11マス）
def interior():
    W, H = 208, 176
    g = Grid(W, H, "f")
    pal = {
        "K": "#16121c",  # 輪郭・いちばん暗い
        "z": "#2a2430",  # 壁の影
        "Z": "#463c4c",  # 壁（奥）
        "y": "#5e5466",  # 壁の石
        "Y": "#fff0a0",  # 灯
        "W": "#ffffff",  # 光
        "f": "#6e6876",  # 床の石
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
        "p": "#2a2050",  # 柱の影
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
    T = 16
    # ---------------- 床（石畳。2マスで1枚の大きな石）
    for y in range(H):
        for x in range(W):
            bx, by = x % 32, y % 16
            off = 16 if (y // 16) % 2 else 0
            bx = (x + off) % 32
            c = "f"
            if by == 0 or bx == 0:
                c = "e"
            elif by == 1 or bx == 1:
                c = "F"
            elif (x * 7 + y * 13) % 29 == 0:
                c = "F"
            g.a[y, x] = c
    # ---------------- 奥の壁（0〜2マス目）
    g.rect(0, 0, W - 1, 3 * T - 1, "Z")
    for y in range(0, 3 * T):
        for x in range(W):
            row = y // 6
            off = 0 if row % 2 == 0 else 6
            if y % 6 == 0 or (x + off) % 12 == 0:
                g.put(x, y, "z")
            elif y % 6 == 1 and (x + off) % 12 < 4:
                g.put(x, y, "y")
    g.hline(0, W - 1, 3 * T - 1, "K")
    g.hline(0, W - 1, 3 * T - 2, "S")
    # ステンドグラスの窓（奥の壁に3つ: 左・まんなか（大）・右）
    def glass(x0, x1, top, bottom, big=False):
        g.arch(x0 - 1, x1 + 1, top - 1, bottom + 1, "K")
        g.arch(x0, x1, top, bottom, "b")
        cx = (x0 + x1) / 2
        for y in range(top, bottom + 1):
            for x in range(x0, x1 + 1):
                if g.a[y, x] != "b":
                    continue
                # 鉛の枠（格子）と、色ガラス
                if (x - x0) % 5 == 0 or (y - top) % 6 == 0:
                    g.put(x, y, "K" if (x - x0) % 5 == 0 and (y - top) % 6 == 0 else "z")
                    continue
                k = ((x - x0) // 5 * 3 + (y - top) // 6 * 5) % 7
                g.put(x, y, ["B", "b", "n", "m", "B", "v", "M"][k])
        # まんなかに灯の環
        cy = top + (x1 - x0) / 2 + 2
        if not big:
            emblem(g, cx, cy, 3.2, ring="G", ring_d="g", lamp="Y", core="W")
    glass(30, 46, 6, 40)
    glass(161, 177, 6, 40)
    glass(86, 121, 3, 40, big=True)
    # 光の筋（窓から床へ、ななめに。1ドットおき）
    for (sx, w_) in ((38, 8), (169, 8), (103, 16)):
        for y in range(3 * T, 9 * T):
            k = (y - 3 * T)
            for x in range(int(sx - w_ / 2 + k * 0.35), int(sx + w_ / 2 + k * 0.35)):
                if 0 <= x < W and (x + y) % 2 == 0 and g.a[y, x] in "fFeE":
                    g.put(x, y, "E" if (x + y) % 4 == 0 else "r")
    def column(cx, base_y, top_y, width=10, sconce=0):
        """丸い柱: 台座（2段）・金の飾り帯・溝のある円柱（左から光、右へ暗く）・柱頭（まるいふくらみと四角い板）。床に右へ影。"""
        half = width // 2
        x0 = cx - half
        # 床の影（右へ、1ドットおき）
        for y in range(base_y - 2, base_y + 1):
            for x in range(cx + half + 1, cx + half + 5):
                if (x + y) % 2 == 0:
                    g.put(x, y, "e")
        # 台座（下の大きい段・上の段）
        g.rect(x0 - 3, base_y - 3, x0 + width + 2, base_y, "S"); g.hline(x0 - 3, x0 + width + 2, base_y - 3, "T"); g.hline(x0 - 3, x0 + width + 2, base_y, "s")
        g.vline(x0 - 3, base_y - 3, base_y, "T"); g.vline(x0 + width + 2, base_y - 3, base_y, "s")
        g.rect(x0 - 1, base_y - 6, x0 + width, base_y - 4, "P"); g.hline(x0 - 1, x0 + width, base_y - 6, "Q"); g.vline(x0 + width, base_y - 6, base_y - 4, "i")
        g.hline(x0, x0 + width - 1, base_y - 7, "G"); g.put(x0 + width - 1, base_y - 7, "g")
        # 円柱（縦の溝。左が明るく、右が暗い）
        tones = ["x", "Q", "I", "Q", "P", "P", "P", "i", "i", "x"]
        for k in range(width):
            t = tones[int(k * len(tones) / width)]
            for y in range(top_y + 6, base_y - 7):
                c = t
                if k % 3 == 2 and t not in ("I", "x"):
                    c = "i" if t in ("P", "Q") else "x"      # 溝
                g.put(x0 + k, y, c)
        # 金の飾り帯（柱頭の下）
        g.hline(x0, x0 + width - 1, top_y + 5, "G"); g.hline(x0, x0 + width - 1, top_y + 6, "g")
        # 柱頭（ふくらみ→四角い板）
        g.rect(x0 - 1, top_y + 3, x0 + width, top_y + 4, "P"); g.put(x0 - 1, top_y + 3, "Q"); g.put(x0 + width, top_y + 4, "i")
        g.rect(x0 - 3, top_y, x0 + width + 2, top_y + 2, "S"); g.hline(x0 - 3, x0 + width + 2, top_y, "T"); g.hline(x0 - 3, x0 + width + 2, top_y + 2, "s")
        g.put(x0 - 2, top_y + 1, "G"); g.put(x0 + width + 1, top_y + 1, "G")       # 角の小さなうず巻き
        # 柱のろうそく受け（内がわへ向く）
        if sconce:
            sy = (top_y + base_y) // 2
            sx = x0 + width if sconce > 0 else x0 - 1
            for k in range(3):
                g.put(sx + sconce * k, sy, "g"); g.put(sx + sconce * k, sy + 1, "G" if k == 2 else "g")
            tip = sx + sconce * 2
            g.put(tip, sy - 1, "L"); g.put(tip, sy - 2, "L"); g.put(tip, sy - 3, "A"); g.put(tip, sy - 4, "a")
            g.put(tip - sconce, sy - 3, "r"); g.put(tip + sconce, sy - 3, "r")

    # ---------------- 奥の壁の飾り: 窓を囲む石のアーチ（くさび石）と、上を走る飾りの帯
    for (x0a, x1a, top) in ((28, 48, 4), (84, 123, 1), (159, 179, 4)):
        cxa = (x0a + x1a) / 2
        ra = (x1a - x0a) / 2 + 1
        for y in range(int(top - 2), int(top + ra + 2)):
            for x in range(x0a - 3, x1a + 4):
                d = math.hypot(x - cxa, y - (top + ra))
                if y <= top + ra and ra + 0.5 <= d <= ra + 2.5:
                    ang = math.atan2(y - (top + ra), x - cxa)
                    g.put(x, y, "K" if int((ang + math.pi) * 7) % 3 == 0 else ("T" if x < cxa else "S"))
    for x in range(W):                                   # 飾りの帯（歯形の飾り）
        g.put(x, 3 * T - 6, "T"); g.put(x, 3 * T - 5, "S"); g.put(x, 3 * T - 4, "s" if x % 4 < 2 else "S")
    # ---------------- 祭壇の左右の、大きな柱（奥の壁の前に立つ）
    for gcx in (66, 141):
        column(gcx, 3 * T + 2, 2, width=10)

    # ---------------- 左右の壁と柱
    for side in (0, 1):
        x0 = 0 if side == 0 else W - T
        g.rect(x0, 3 * T, x0 + T - 1, H - 1, "Z")
        for y in range(3 * T, H):
            if y % 6 == 0:
                g.hline(x0, x0 + T - 1, y, "z")
        g.vline(x0 + (T - 1 if side == 0 else 0), 3 * T, H - 1, "K")
        # 柱（3本ずつ。台座・溝のある円柱・柱頭。ろうそく受けは内がわへ）
        for py in (3 * T + 6, 6 * T + 6, 9 * T - 2):
            column(x0 + 8, py, py - 34, width=8, sconce=1 if side == 0 else -1)
        # むらさきの旗（灯の環のしるし）
        bx = x0 + (2 if side == 0 else 7)
        for y in range(7 * T, 9 * T + 4):
            for x in range(bx, bx + 7):
                c = "U" if x < bx + 5 else "u"
                if x == bx:
                    c = "V"
                g.put(x, y, c)
        for x in range(bx, bx + 7):
            if (x - bx) % 2 == 0:
                g.put(x, 9 * T + 5, "u")
        emblem(g, bx + 3, 8 * T, 2.4, ring="G", ring_d="g", lamp="h", core="W")
    # ---------------- 祭壇（2マス目の奥、まんなか）
    ax0, ax1 = 5 * T - 6, 8 * T + 5
    # 段（2段）
    g.rect(ax0 - 8, 3 * T, ax1 + 8, 3 * T + 10, "S"); g.hline(ax0 - 8, ax1 + 8, 3 * T, "T"); g.hline(ax0 - 8, ax1 + 8, 3 * T + 10, "s")
    g.rect(ax0 - 16, 3 * T + 11, ax1 + 16, 3 * T + 18, "S"); g.hline(ax0 - 16, ax1 + 16, 3 * T + 11, "T"); g.hline(ax0 - 16, ax1 + 16, 3 * T + 18, "s")
    # 祭壇の台（白い布・金のふち）
    g.rect(ax0 + 4, 2 * T + 4, ax1 - 4, 3 * T + 4, "L")
    g.rect(ax1 - 10, 2 * T + 4, ax1 - 4, 3 * T + 4, "l")
    g.hline(ax0 + 4, ax1 - 4, 2 * T + 4, "G"); g.hline(ax0 + 4, ax1 - 4, 2 * T + 5, "h")
    g.hline(ax0 + 4, ax1 - 4, 3 * T + 5, "g")
    g.vline(ax0 + 3, 2 * T + 4, 3 * T + 5, "K"); g.vline(ax1 - 3, 2 * T + 4, 3 * T + 5, "K")
    for x in range(ax0 + 8, ax1 - 6, 6):
        g.vline(x, 2 * T + 7, 3 * T + 3, "l")
    emblem(g, (ax0 + ax1) / 2, 2 * T + 17, 4.5, ring="G", ring_d="g", lamp="Y", core="W")
    # 祭壇のうしろの、大きな灯の環（金の輪と8つの灯。光をまとう）
    ex, ey = (ax0 + ax1) / 2, 1 * T + 6
    emblem(g, ex, ey, 14, ring="G", ring_d="g", lamp="Y", core="W")
    # 祭壇の上のろうそく（4本）
    for cx in (ax0 + 10, ax0 + 20, ax1 - 20, ax1 - 10):
        g.rect(cx, 2 * T - 3, cx + 1, 2 * T + 3, "L")
        g.put(cx, 2 * T - 4, "A"); g.put(cx + 1, 2 * T - 4, "a"); g.put(cx, 2 * T - 5, "Y"); g.put(cx, 2 * T - 6, "a")
        g.hline(cx - 1, cx + 2, 2 * T + 3, "g")
    # ---------------- 燭台（祭壇の左右、背の高いもの）
    for cx in (3 * T + 4, 10 * T - 6):
        g.rect(cx, 2 * T + 6, cx + 1, 3 * T + 14, "g"); g.vline(cx, 2 * T + 6, 3 * T + 14, "G")
        g.hline(cx - 3, cx + 4, 3 * T + 15, "g"); g.hline(cx - 2, cx + 3, 3 * T + 16, "G")
        g.hline(cx - 4, cx + 5, 2 * T + 6, "G"); g.hline(cx - 4, cx + 5, 2 * T + 7, "g")
        for k in (-4, 0, 4):
            g.rect(cx + k, 2 * T + 1, cx + k + 1, 2 * T + 5, "L")
            g.put(cx + k, 2 * T, "A"); g.put(cx + k + 1, 2 * T, "a"); g.put(cx + k, 2 * T - 1, "Y"); g.put(cx + k + 1, 2 * T - 2, "a")
    # ---------------- まんなかの通路のじゅうたん（扉から祭壇へ）
    cx0, cx1 = 5 * T + 10, 8 * T - 10
    for y in range(4 * T + 3, H - T + 2):
        for x in range(cx0, cx1 + 1):
            c = "C"
            if x in (cx0, cx1):
                c = "c"
            elif x in (cx0 + 1, cx1 - 1):
                c = "G" if y % 4 else "g"
            elif x == cx0 + 3 or (y // 8) % 2 == 0 and (x - cx0) % 9 == 4:
                c = "D"
            g.put(x, y, c)
    # ---------------- じゅうたんの両わきの、床のモザイクの縁取り（小さな四角を交互に）
    for y in range(4 * T + 3, H - T + 2):
        for x in (cx0 - 3, cx0 - 2, cx1 + 2, cx1 + 3):
            k = (y // 2 + x) % 4
            g.put(x, y, ["S", "T", "s", "G"][k] if (y // 2) % 6 != 0 else "e")
    # 祭壇の前の床の、象眼の環（三つの環を大きく）
    emblem(g, (cx0 + cx1) / 2, 4 * T + 10, 9, ring="T", ring_d="s", lamp="E", core="W")

    # ---------------- 長いす（左右に4列ずつ。3マスぶんの幅）
    for row in range(4):
        y0 = 5 * T + row * 20 + 4
        for (x0, x1) in ((1 * T + 4, 5 * T - 2), (8 * T + 2, 12 * T - 4)):
            # 背もたれ
            g.rect(x0, y0, x1, y0 + 4, "O")
            g.hline(x0, x1, y0, "q"); g.hline(x0, x1, y0 + 1, "o"); g.hline(x0, x1, y0 + 4, "w")
            # 座面
            g.rect(x0, y0 + 5, x1, y0 + 9, "o")
            g.hline(x0, x1, y0 + 5, "q"); g.hline(x0, x1, y0 + 9, "w")
            # 脚とふち
            for lx in (x0, x0 + (x1 - x0) // 2, x1):
                g.rect(lx, y0 + 10, lx + 1, y0 + 13, "w")
            g.vline(x0 - 1, y0, y0 + 10, "K"); g.vline(x1 + 1, y0, y0 + 10, "K")
            g.hline(x0, x1, y0 + 14, "e")
            # 両はしの彫りのある板（うず巻きの形）と、金のつまみ
            for ex in (x0, x1 - 2):
                g.rect(ex, y0 - 2, ex + 2, y0 + 10, "O")
                g.vline(ex, y0 - 2, y0 + 10, "q"); g.vline(ex + 2, y0 - 2, y0 + 10, "w")
                g.put(ex + 1, y0 - 3, "w"); g.put(ex + 1, y0 + 3, "w"); g.put(ex + 1, y0 + 6, "q")
                g.put(ex + 1, y0 - 2, "G")
    # ---------------- 手前の壁と、両開きの扉（下のまんなか）
    g.rect(0, H - T + 4, W - 1, H - 1, "Z")
    g.hline(0, W - 1, H - T + 4, "K"); g.hline(0, W - 1, H - T + 5, "y")
    dx0, dx1 = 6 * T - 2, 7 * T + 1
    g.rect(dx0 - 2, H - T + 2, dx1 + 2, H - 1, "K")
    g.rect(dx0, H - T + 3, dx1, H - 1, "O")
    g.vline((dx0 + dx1) // 2, H - T + 3, H - 1, "w")
    g.vline(dx0 + 2, H - T + 3, H - 1, "q"); g.vline(dx1 - 2, H - T + 3, H - 1, "w")
    g.put((dx0 + dx1) // 2 - 2, H - 7, "G"); g.put((dx0 + dx1) // 2 + 2, H - 7, "G")
    # 入口のマット
    g.rect(dx0 + 2, H - T - 2, dx1 - 2, H - T + 1, "c"); g.hline(dx0 + 2, dx1 - 2, H - T - 2, "D")
    g.save("church-interior", pal)


if __name__ == "__main__":
    exterior()
    interior()
    print("ok")
