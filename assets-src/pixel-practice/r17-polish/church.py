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
def exterior():
    W, H = 80, 88
    g = Grid(W, H)
    pal = {
        "K": "#1e1a24",  # 輪郭
        "s": "#4a4c5c",  # 石の影
        "S": "#7a7c8c",  # 石
        "T": "#a8aab8",  # 石の明るい面
        "U": "#d4d6e0",  # 石のいちばん明るい所
        "r": "#243250",  # 屋根の影
        "R": "#36507a",  # 屋根
        "Q": "#5a78a8",  # 屋根の明るい所
        "w": "#4a2a18",  # 木の扉の影
        "O": "#7a4a24",  # 木の扉
        "o": "#a86a34",  # 木の扉の明るい所
        "g": "#8a6418",  # 金の影
        "G": "#e0b040",  # 金
        "Y": "#fff0a0",  # 灯
        "W": "#ffffff",  # 光
        "b": "#2a4a88",  # ステンドグラス 青
        "c": "#4aa0d0",  # ステンドグラス 水色
        "m": "#b04070",  # ステンドグラス 紅
        "v": "#e8c060",  # ステンドグラス 黄
        "n": "#3a3640",  # 石段の影
        "N": "#6a6874",  # 石段
        "h": "#2c4a2c",  # つたの影
        "H": "#4a7a3a",  # つた
    }
    body_top, foot = 40, 84
    # 本堂の壁（石積み）
    g.rect(8, body_top, 71, foot, "S")
    for y in range(body_top, foot + 1):
        for x in range(8, 72):
            row = (y - body_top) // 4
            off = 0 if row % 2 == 0 else 4
            if (y - body_top) % 4 == 0:
                g.put(x, y, "s")
            elif (x + off) % 8 == 0:
                g.put(x, y, "s")
            elif x < 24 and (y - body_top) % 4 == 1:
                g.put(x, y, "T")
    g.rect(8, body_top, 10, foot, "T"); g.rect(69, body_top, 71, foot, "s")
    g.vline(7, body_top, foot, "K"); g.vline(72, body_top, foot, "K")
    # 控え壁（左右）
    for bx in (14, 63):
        g.rect(bx, body_top + 8, bx + 3, foot, "T" if bx < 40 else "s")
        g.vline(bx - 1, body_top + 8, foot, "K"); g.vline(bx + 4, body_top + 8, foot, "K")
        g.hline(bx - 1, bx + 4, body_top + 7, "K")
    # 本堂の屋根（左右の切妻）
    for y in range(26, body_top + 1):
        half = int((y - 26) * 2.6) + 4
        for x in range(40 - half, 40 + half + 1):
            if 3 <= x <= 76:
                g.put(x, y, "Q" if x < 40 - half + 3 else ("r" if x > 40 + half - 4 else "R"))
        g.put(40 - half - 1, y, "K"); g.put(40 + half + 1, y, "K")
    g.hline(3, 76, body_top + 1, "K")
    for x in range(4, 76, 3):   # 屋根のふちの瓦
        g.put(x, body_top, "r")
    # 鐘楼（まんなかの塔）
    tx0, tx1 = 31, 48
    g.rect(tx0, 6, tx1, body_top + 2, "S")
    for y in range(6, body_top + 3):
        if (y - 6) % 4 == 0:
            g.hline(tx0, tx1, y, "s")
    g.rect(tx0, 6, tx0 + 2, body_top + 2, "T"); g.rect(tx1 - 2, 6, tx1, body_top + 2, "s")
    g.vline(tx0 - 1, 6, body_top + 2, "K"); g.vline(tx1 + 1, 6, body_top + 2, "K")
    # 鐘の窓（アーチ）と鐘
    g.arch(35, 44, 9, 19, "K")
    g.arch(36, 43, 10, 19, "n")
    g.rect(38, 13, 41, 17, "G"); g.hline(37, 42, 17, "g"); g.put(39, 18, "g"); g.put(38, 13, "Y")
    # 塔のとがり屋根
    for y in range(0, 7):
        half = y + 3
        for x in range(39 - half, 41 + half):
            g.put(x, y + 1, "Q" if x < 40 else "r")
        g.put(39 - half - 1, y + 1, "K"); g.put(40 + half + 1, y + 1, "K")
    # 塔のてっぺんの、小さな灯の環
    g.ring(39.5, 0.5, 1.6, "G")
    # 塔の正面: 大きな灯の環（丸窓）
    g.disk(39.5, 29, 6.5, "K")
    g.disk(39.5, 29, 5.6, "b")
    for y in range(22, 37):
        for x in range(33, 47):
            d = math.hypot(x - 39.5, y - 29)
            if d <= 5.6:
                a = math.atan2(y - 29, x - 39.5)
                seg = int(((a + math.pi) / (2 * math.pi)) * 8) % 8
                g.put(x, y, ["c", "b", "m", "b", "v", "b", "m", "b"][seg] if d > 2 else "Y")
    emblem(g, 39.5, 29, 6.2)
    # 本堂の窓（左右に2つずつ、アーチのステンドグラス）
    for wx in (19, 27, 51, 59):
        g.arch(wx - 1, wx + 4, 48, 66, "K")
        g.arch(wx, wx + 3, 49, 65, "b")
        for y in range(49, 66):
            for x in range(wx, wx + 4):
                if g.a[y, x] == "b":
                    k = (y + x) % 6
                    g.put(x, y, "c" if k == 0 else ("m" if (y // 4) % 3 == 0 and x == wx + 1 else ("v" if y == 54 else "b")))
        g.put(wx + 1, 51, "Y"); g.put(wx + 2, 51, "Y")
        g.hline(wx - 1, wx + 4, 67, "T")
    # 正面の大きな扉（アーチ、両開き）
    g.arch(31, 48, 56, foot - 3, "K")
    g.arch(32, 47, 57, foot - 3, "w")
    for y in range(57, foot - 2):
        for x in range(33, 47):
            if g.a[y, x] == "w":
                g.put(x, y, "o" if x in (34, 41) else ("O" if x != 39 and x != 40 else "w"))
    g.vline(39, 58, foot - 3, "K"); g.vline(40, 58, foot - 3, "w")
    for y in (64, 72):
        g.hline(33, 46, y, "g")
    g.put(37, 69, "G"); g.put(42, 69, "G")
    emblem(g, 39.5, 61, 3.0)
    # 扉の上の飾り石と、石段
    g.arch(29, 50, 54, 56, "T")
    g.rect(26, foot - 2, 53, foot - 1, "N"); g.hline(26, 53, foot - 2, "U")
    g.rect(22, foot, 57, foot + 1, "N"); g.hline(22, 57, foot, "T")
    g.hline(22, 57, foot + 2, "n")
    # つた（左の壁）
    for (x, y) in [(9, 70), (10, 71), (9, 73), (11, 74), (10, 76), (9, 78), (12, 79), (10, 81), (11, 82), (9, 83), (13, 77)]:
        g.put(x, y, "H"); g.put(x + 1, y + 1, "h")
    for (x, y) in [(69, 72), (70, 74), (68, 76), (70, 79), (69, 81), (68, 83)]:
        g.put(x, y, "H"); g.put(x - 1, y + 1, "h")
    # 地面の影
    g.hline(6, 73, foot + 3, "n")
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
    # ---------------- 左右の壁と柱
    for side in (0, 1):
        x0 = 0 if side == 0 else W - T
        g.rect(x0, 3 * T, x0 + T - 1, H - 1, "Z")
        for y in range(3 * T, H):
            if y % 6 == 0:
                g.hline(x0, x0 + T - 1, y, "z")
        g.vline(x0 + (T - 1 if side == 0 else 0), 3 * T, H - 1, "K")
        # 柱（3本ずつ）
        for py in (3 * T + 4, 6 * T + 4, 9 * T - 4):
            px = x0 + (6 if side == 0 else 2)
            g.rect(px, py - 30, px + 7, py, "P")
            g.vline(px, py - 30, py, "Q"); g.vline(px + 7, py - 30, py, "p")
            g.rect(px - 1, py - 32, px + 8, py - 30, "S"); g.hline(px - 1, px + 8, py - 32, "T")
            g.rect(px - 1, py + 1, px + 8, py + 2, "s")
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
            # ひじかけの飾り
            g.put(x0, y0 - 1, "o"); g.put(x1, y0 - 1, "o")
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
