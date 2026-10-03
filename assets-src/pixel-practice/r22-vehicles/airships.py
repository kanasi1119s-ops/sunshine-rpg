"""飛空艇「環翔船」（40×40、飛行中は各向き2コマ）、影（24×10）、着陸中（48×48）。
独自の形: 胴体の上に「灯の環」の輪（真鍮の縁に青緑の膜を張った円盤）が立ち、その輪が浮かぶ力を生む。
横から見ると細い楕円、前後から見ると真円。尾に赤いひれ、プロペラ。コマ違いはプロペラ・ひれ・輪の中心の灯。"""
import math
from lib import Canvas


def disc(c, cx, cy, rx, ry, face, glow):
    """輪の円盤。face=True なら真円（前後から）、False なら横から（細い楕円）。"""
    c.ell(cx, cy, rx, ry, "S")
    for y in range(c.h):
        for x in range(c.w):
            if c.get(x, y) == "S" and ((x + 0.5 - cx) * 0.8 + (y + 0.5 - cy) * 0.6) > 0.5 * rx:
                c.px(x, y, "s")
    if face:
        for k in range(8):                                   # 放射状のすじ（膜を支える骨）
            a = k * math.pi / 4 + math.pi / 8
            x1, y1 = cx + math.cos(a) * (rx - 2.2), cy + math.sin(a) * (ry - 2.2)
            c.line(int(cx), int(cy), int(round(x1 - 0.5)), int(round(y1 - 0.5)), "z" if x1 > cx else "s")
    else:
        c.rect(int(cx), int(cy - ry + 2), int(cx), int(cy + ry - 2), "z")
    # 真鍮の縁（左が明るく、右が暗い）
    for y in range(c.h):
        for x in range(c.w):
            d = math.hypot((x + 0.5 - cx) / rx, (y + 0.5 - cy) / ry)
            if (1.0 - (1.9 / rx if face else 1.5 / rx)) <= d <= 1.0:
                c.px(x, y, "D" if (x + 0.5 - cx) * 0.7 + (y + 0.5 - cy) * 0.7 < 1.0 else "d")
    g = "D" if glow else "Y"
    c.rect(int(cx) - 1, int(cy) - 1, int(cx), int(cy), g)


def prop_side(c, x, y, frame):
    """横向きのプロペラ（後ろ）。frame0=縦に長い、frame1=短くぼやける。"""
    if frame == 0:
        c.rect(x, y - 3, x, y + 3, "T"); c.rect(x + 1, y - 2, x + 1, y + 2, "t")
    else:
        c.rect(x, y - 1, x, y + 1, "T"); c.px(x - 1, y - 2, "T"); c.px(x - 1, y + 2, "T"); c.px(x, y - 3, "T"); c.px(x, y + 3, "T")
    c.px(x + 1, y, "K")


def side(frame):
    c = Canvas(40, 40)
    # ひもで輪を吊る（輪の下から甲板へ）
    cx, cy = 20, 13
    disc(c, cx, cy, 6, 11, False, frame == 1)
    c.line(17, 23, 13, 27, "K"); c.line(23, 23, 27, 27, "K"); c.line(20, 24, 20, 27, "K")
    # 尾びれ（赤）：コマで先がゆれる
    dy = 0 if frame == 0 else 1
    c.poly([(6, 21 + dy), (14, 27), (6, 30)], "R")
    c.poly([(9, 25), (14, 27), (6, 30)], "r", only="R")
    # 胴体（クリーム色の船体。船尾がはね上がり、船首は丸く、腹は深い）
    hull = [(5, 26), (9, 27), (29, 27), (35, 28), (37, 30), (34, 34), (28, 37), (14, 38), (8, 35), (5, 31)]
    c.poly(hull, "W")
    c.poly([(5, 34.2), (12, 34.2), (14, 38), (8, 35)], "w", only="W")
    c.poly([(11, 35), (33, 35), (28, 37), (14, 38)], "w", only="W")
    c.poly([(30, 27), (35, 28), (37, 30), (34, 34), (31, 34)], "w", only="W")
    c.rect(5, 26, 36, 26, "D") if False else None
    c.rect(9, 27, 34, 27, "D")                                       # 甲板のふち（真鍮）
    c.rect(5, 31, 36, 31, "R")                                       # 赤いライン
    for x in (10, 14, 18, 22, 26):                                   # 舷窓
        c.rect(x, 28, x + 1, 29, "B")
    c.px(37, 30, "Y")                                                # 先のあかり
    prop_side(c, 3, 31, frame)
    return c.outline()


def front(frame, toward):
    """toward=True: こちらへ向かう（鼻先とあかり）。False: 遠ざかる（船尾・窓・舵）。"""
    c = Canvas(40, 40)
    cx, cy = 20, 13
    disc(c, cx, cy, 11, 11, True, frame == 1)
    # ひれ（左右。コマで先がゆれる）
    dy = 0 if frame == 0 else 1
    c.poly([(2, 24 - dy), (13, 27), (13, 33), (2, 31 - dy)], "R")
    c.poly([(27, 27), (38, 24 - dy), (38, 31 - dy), (27, 33)], "r")
    c.poly([(2, 27 - dy), (13, 30), (13, 33), (2, 31 - dy)], "r", only="R")
    # 胴体
    c.poly([(11, 24), (29, 24), (30, 29), (27, 34), (20, 36), (13, 34), (10, 29)], "W")
    c.poly([(21, 24), (29, 24), (30, 29), (27, 34), (20, 36), (21, 29)], "w", only="W")
    c.poly([(11, 33), (29, 33), (27, 34), (20, 36), (13, 34)], "w", only="W")
    c.rect(11, 24, 29, 24, "D")
    c.rect(10, 29, 30, 29, "R")
    if toward:
        c.px(20, 34, "Y"); c.px(19, 34, "Y"); c.px(20, 33, "Y")
        for x in (14, 17, 23, 26):
            c.rect(x, 26, x + 1, 27, "B")
        # 鼻先のプロペラ（十字／ななめ）
        if frame == 0:
            c.rect(14, 37, 26, 37, "T"); c.rect(20, 36, 20, 39, "t")
        else:
            for k in range(-4, 5):
                c.px(20 + k, 37 + k // 2, "T")
            c.px(20, 36, "t"); c.px(20, 39, "t")
    else:
        # 船尾：大きな窓と舵、まん中にプロペラ
        c.rect(15, 26, 25, 27, "B"); c.rect(20, 26, 20, 27, "w")
        if frame == 0:
            c.rect(14, 31, 26, 31, "T"); c.rect(20, 28, 20, 34, "t")
        else:
            for k in range(-4, 5):
                c.px(20 + k, 31 + k // 2, "T")
            c.px(20, 29, "t"); c.px(20, 34, "t")
    return c.outline()


def shadow():
    """地面に落ちる丸い影（24×10）。外側は市松で半透明ふうに、中は濃く。"""
    c = Canvas(24, 10)
    for y in range(10):
        for x in range(24):
            d = math.hypot((x + 0.5 - 12) / 12.0, (y + 0.5 - 5) / 5.0)
            if d <= 0.62:
                c.px(x, y, "q")
            elif d <= 1.0 and (x + y) % 2 == 0:
                c.px(x, y, "q")
    return c


def landed():
    """着陸中（48×48）。足の台と、はしご。プロペラは止まっている（ななめ）。"""
    c = Canvas(48, 48)
    # 地面の影（市松）
    for y in range(38, 46):
        for x in range(0, 48):
            d = math.hypot((x + 0.5 - 22) / 21.0, (y + 0.5 - 42) / 3.0)
            if d <= 0.7 or (d <= 1.0 and (x + y) % 2 == 0):
                c.px(x, y, "V")
    s = side(0)
    # 止まったプロペラに差し替え（横向きに寝かせる）
    for y in range(26, 36):
        for x in range(0, 5):
            s.g[y][x] = "."
    s.rect(3, 30, 4, 32, "T"); s.rect(3, 31, 3, 31, "t")
    s.rect(2, 28, 2, 28, "T"); s.rect(2, 34, 2, 34, "T"); s.px(3, 28, "t"); s.px(3, 34, "t")
    for y in range(26, 36):
        s.g[y][0] = "."
    c.paste(s, 4, 3)
    # 足（着陸そり）
    for x in (14, 31):
        c.rect(x, 40, x + 1, 43, "t"); c.px(x, 40, "T")
    c.rect(10, 43, 36, 43, "K"); c.rect(10, 44, 36, 44, "A")
    c.px(9, 42, "K"); c.px(37, 42, "K")
    # はしご
    c.line(26, 40, 29, 44, "K")
    return c.outline()


def make():
    d = {}
    for f in (0, 1):
        r = side(f)
        d[f"airship-right-{f}"] = r
        d[f"airship-left-{f}"] = r.mirror()
        d[f"airship-down-{f}"] = front(f, True)
        d[f"airship-up-{f}"] = front(f, False)
    d["airship-shadow"] = shadow()
    d["airship-landed"] = landed()
    return d
