"""隠しダンジョンの小島のアイコン4種（48×48）と、渦の配色見本（48×48）。
小さな岩の島（砂浜・草・切り立つ岩肌）を白い波と濃い青の水かげで囲み、海に浮いて見えるようにする。"""
import math
from lib import Canvas

CX, CY, RX, RY = 24, 33, 19, 8      # 島の上面の楕円


def island(c, grass=("G", "g"), cliff_h=4):
    # 水かげ（島の下の濃い青。島が海にうく感じ）
    c.ell(CX, CY + cliff_h + 2, RX + 3, RY - 1, "l")
    # 岩肌（上面の前半分の下にのびる）
    for x in range(CX - RX, CX + RX + 1):
        u = (x + 0.5 - CX) / RX
        if abs(u) > 1:
            continue
        ytop = CY + RY * math.sqrt(1 - u * u)
        hgt = cliff_h * (1 - 0.35 * abs(u)) + 0.5 + (1 if (x * 7 + 3) % 5 == 0 else 0) - (1 if (x * 3) % 7 == 0 else 0)
        for y in range(int(ytop), int(ytop + hgt) + 1):
            s = u
            c.px(x, y, "U" if s < -0.25 else ("u" if s < 0.45 else "V"))
    # 上面（草。左上が明るい）。ふちは砂浜
    for y in range(CY - RY - 1, CY + RY + 2):
        for x in range(CX - RX - 1, CX + RX + 2):
            d = math.hypot((x + 0.5 - CX) / RX, (y + 0.5 - CY) / RY)
            if d <= 1.0:
                if d > 0.80:
                    c.px(x, y, "D" if (x - CX) * 0.5 + (y - CY) < 3 else "d")
                else:
                    c.px(x, y, grass[0] if (x - CX) * 0.45 + (y - CY) < 1 else grass[1])
    # ふちの小さな岩（島を円盤に見せない）
    for (bx, by, rx, ry) in ((CX - RX - 1, CY + 3, 3, 2), (CX + RX, CY + 5, 3, 2), (CX - 9, CY + RY + cliff_h, 3, 1), (CX + 11, CY + RY + cliff_h - 1, 2, 1)):
        for yy in range(by - ry, by + ry + 1):
            for xx in range(bx - rx, bx + rx + 1):
                if ((xx + 0.5 - bx) / rx) ** 2 + ((yy + 0.5 - by) / ry) ** 2 <= 1.0:
                    c.px(xx, yy, "U" if xx <= bx else "u")
    # 草の点々
    for (x, y) in ((12, 31), (35, 36), (30, 29), (16, 36), (38, 32)):
        if c.get(x, y) in "Gg":
            c.px(x, y, "g" if c.get(x, y) == "G" else "G")


def foam(c, cliff_h=4):
    """島のまわりの白い波（楕円のふち、とぎれとぎれ）。島の下側ほど手前に見える。"""
    for x in range(CX - RX - 4, CX + RX + 5):
        u = (x + 0.5 - CX) / (RX + 4)
        if abs(u) > 1:
            continue
        y0 = CY + cliff_h + 1 + (RY - 1) * math.sqrt(1 - u * u)
        for dy, ch in ((0, "C"), (1, "c")):
            y = int(round(y0)) + dy
            if (x + dy * 3) % 5 < 3 and c.get(x, y) in ".l":
                c.px(x, y, ch)
    # 左右のしぶき
    for (x, y) in ((CX - RX - 3, CY + 1), (CX - RX - 2, CY + 2), (CX + RX + 3, CY + 1), (CX + RX + 2, CY + 3), (CX - RX - 4, CY + 3), (CX + RX + 4, CY + 4)):
        if c.get(x, y) in ".l":
            c.px(x, y, "C")


def col(c, x, base, h, w=4, broken=0, moss=False):
    """石柱（左が明るく右が暗い）。broken>0 なら先がギザギザに欠けている。"""
    for y in range(base - h, base + 1):
        for xx in range(x, x + w):
            t = (xx - x) / (w - 1)
            c.px(xx, y, "U" if t < 0.4 else ("u" if t < 0.8 else "V"))
    for k in range(0, h, 5):
        c.rect(x, base - k, x + w - 1, base - k, "u")
        c.px(x + w - 1, base - k, "V")
    if broken:
        for i in range(w):
            cut = (broken if i % 2 == 0 else 0) + (1 if i == 1 else 0)
            for y in range(base - h, base - h + cut):
                c.px(x + i, y, ".")
    else:
        c.rect(x - 1, base - h - 1, x + w, base - h, "U"); c.rect(x + w - 2, base - h - 1, x + w, base - h, "u")
    if moss:
        c.px(x, base - 3, "G"); c.px(x + 1, base - 2, "g"); c.px(x, base - h // 2, "g")


def ruin():
    c = Canvas(48, 48)
    island(c)
    c.ell(24, 34, 14, 5, "u"); c.ell(23, 33, 13, 4, "U")              # 土台の石畳
    c.rect(11, 34, 33, 34, "u")
    # 倒れた柱（手前）
    for x in range(15, 32):
        c.rect(x, 36, x, 37, "U" if x < 25 else "u"); c.px(x, 38, "V")
    c.rect(15, 36, 15, 38, "u"); c.rect(28, 36, 30, 37, "u")
    # 二本の柱とその上の梁（ゲートの名残）
    col(c, 10, 35, 22, 4, broken=0, moss=True)
    col(c, 22, 33, 22, 4, broken=0)
    c.rect(8, 11, 27, 12, "U"); c.rect(18, 11, 27, 12, "u"); c.rect(8, 13, 27, 13, "V")
    c.rect(24, 11, 27, 13, ".")                                        # 梁の右はしは欠けている
    c.px(23, 11, "."); c.px(25, 10, "u")
    # 右の柱は折れた切り株
    col(c, 33, 35, 8, 4, broken=3, moss=True)
    # 欠けた石のかけら
    c.rect(28, 31, 30, 32, "U"); c.rect(30, 32, 31, 32, "u")
    for (x, y) in ((11, 24), (11, 26), (12, 28), (23, 22), (23, 23), (35, 31)):
        c.px(x, y, "G")
    foam(c)
    return c.outline()


def cave():
    c = Canvas(48, 48)
    island(c)
    # 岩山
    c.poly([(5, 36), (11, 24), (18, 14), (25, 10), (32, 15), (39, 24), (44, 36), (36, 40), (12, 40)], "U")
    c.poly([(25, 10), (32, 15), (39, 24), (44, 36), (36, 40), (27, 40), (27, 24)], "u", only="U")
    c.poly([(34, 22), (39, 24), (44, 36), (36, 40), (33, 40)], "V", only="u")
    # 岩のすじ
    for (x0, y0, x1, y1) in ((13, 28, 18, 25), (20, 17, 24, 16), (29, 20, 35, 22), (31, 31, 37, 29), (10, 34, 15, 33)):
        for i in range(x0, x1 + 1):
            ch = c.get(i, y0 + (y1 - y0) * (i - x0) // max(1, x1 - x0))
            if ch in "Uu":
                c.px(i, y0 + (y1 - y0) * (i - x0) // max(1, x1 - x0), {"U": "u", "u": "V"}[ch])
    # 入口（黒い穴、アーチ）
    for y in range(24, 41):
        for x in range(14, 36):
            u = (x + 0.5 - 24.5) / 6.2
            top = 24 + 7 * (1 - math.sqrt(max(0.0, 1 - u * u))) if abs(u) <= 1 else 99
            if abs(u) <= 1 and y >= top and y <= 38:
                c.px(x, y, "A" if y > top + 2 else "q")
    # 入口のふち石
    for x in range(17, 33):
        u = (x + 0.5 - 24.5) / 6.2
        if abs(u) <= 1.25:
            y = int(24 + 7 * (1 - math.sqrt(max(0.0, 1 - min(1.0, abs(u)) ** 2)))) - 1
            if c.get(x, y) in "Uu":
                c.px(x, y, "V")
    # 苔と道
    for (x, y) in ((9, 32), (10, 31), (40, 30), (41, 31), (21, 13)):
        c.px(x, y, "G")
    for y in range(36, 41):
        for x in range(21, 29):
            if c.get(x, y) in "GgD" or (y > 38 and c.get(x, y) in "UuVAq"):
                c.px(x, y, "D" if x < 25 else "d")
    foam(c)
    return c.outline()


def shrine():
    c = Canvas(48, 48)
    island(c, grass=("G", "g"))
    # 石の段（前に）
    c.rect(15, 36, 33, 37, "U"); c.rect(26, 36, 33, 37, "u")
    c.rect(18, 34, 30, 35, "U"); c.rect(26, 34, 30, 35, "u")
    # 環の祠：2本の短い台座に、石の輪が立つ
    for x in (14, 31):
        c.rect(x, 28, x + 3, 34, "U"); c.rect(x + 2, 28, x + 3, 34, "u"); c.rect(x, 28, x + 3, 28, "u")
    cx, cy = 24, 18
    for y in range(4, 33):
        for x in range(10, 39):
            d = math.hypot((x + 0.5 - cx) / 13.0, (y + 0.5 - cy) / 14.0)
            if 0.66 <= d <= 1.0:
                c.px(x, y, "U" if (x + 0.5 - cx) * 0.6 + (y + 0.5 - cy) * 0.6 < 1.0 else "u")
    # 輪の内側のふち（影）と、真鍮のしるし
    for y in range(4, 33):
        for x in range(10, 39):
            d = math.hypot((x + 0.5 - cx) / 13.0, (y + 0.5 - cy) / 14.0)
            if 0.66 <= d <= 0.72 and c.get(x, y) == "U":
                c.px(x, y, "u")
    for a in range(0, 360, 45):
        x = int(round(cx + math.cos(math.radians(a)) * 11)); y = int(round(cy + math.sin(math.radians(a)) * 11.8))
        c.px(x, y, "D")
    # 輪の中心にうかぶ灯
    c.rect(23, 17, 24, 18, "Y"); c.px(23, 16, "D"); c.px(24, 19, "D"); c.px(22, 17, "D"); c.px(25, 18, "D")
    # 苔
    for (x, y) in ((14, 31), (15, 32), (33, 30), (11, 33), (35, 33)):
        if c.get(x, y) in "UuG":
            c.px(x, y, "G")
    foam(c)
    return c.outline()


def fort():
    c = Canvas(48, 48)
    island(c)
    # 城壁（正面。上はギザギザに欠けている）
    c.rect(8, 22, 38, 37, "U"); c.rect(28, 22, 38, 37, "u"); c.rect(35, 22, 38, 37, "V")
    for x in (8, 12, 17, 28, 33):                      # 残った胸壁
        c.rect(x, 19, x + 2, 22, "U" if x < 28 else "u")
    # れんがの目地
    for y in range(24, 37, 3):
        for x in range(8, 41):
            if (x + (y // 3) * 2) % 6 != 0 or True:
                if (x + (y // 3) * 3) % 5 and c.get(x, y) in "Uu":
                    c.px(x, y, {"U": "u", "u": "V"}[c.get(x, y)])
    # 左の塔（高い。てっぺんが欠けている）
    c.rect(5, 12, 15, 37, "U"); c.rect(11, 12, 15, 37, "u")
    for k, (x, y) in enumerate(((5, 12), (6, 12), (9, 12), (10, 12), (13, 12))):
        c.px(x, y, "."); c.px(x, y + 1, "." if k % 2 == 0 else c.get(x, y + 1))
    for y in range(14, 37, 3):
        for x in range(5, 16):
            if (x + (y // 3) * 2) % 4 and c.get(x, y) in "Uu":
                c.px(x, y, {"U": "u", "u": "V"}[c.get(x, y)])
    c.rect(8, 18, 9, 21, "A"); c.rect(8, 18, 9, 18, "q")        # 塔の窓
    # 右の塔のなれのはて（くずれた切り株）
    c.poly([(34, 27), (42, 29), (42, 37), (34, 37)], "u"); c.rect(38, 29, 42, 37, "V")
    # 門（アーチ、黒い穴）
    for y in range(28, 38):
        for x in range(19, 29):
            u = (x + 0.5 - 23.5) / 4.6
            if abs(u) <= 1 and y >= 28 + 4 * (1 - math.sqrt(max(0.0, 1 - u * u))):
                c.px(x, y, "A" if y > 31 else "q")
    # 旗ざお、やぶれた旗
    c.rect(10, 4, 10, 12, "K"); c.poly([(11, 5), (17, 6), (15, 7), (17, 9), (11, 9)], "r"); c.px(11, 5, "R"); c.px(12, 5, "R")
    # がれきと草
    c.rect(30, 36, 33, 38, "u"); c.rect(33, 37, 36, 38, "V"); c.rect(15, 37, 17, 38, "U")
    for (x, y) in ((9, 30), (10, 31), (30, 24), (38, 26), (16, 36), (18, 36)):
        if c.get(x, y) in "UuV":
            c.px(x, y, "G")
    foam(c)
    return c.outline()


def whirlpool():
    """渦の配色見本。深い青・青・白い泡。渦巻きの腕の作り方の見本（ゲームではコードで回す）。"""
    c = Canvas(48, 48)
    for y in range(48):
        for x in range(48):
            dx, dy = x + 0.5 - 24, y + 0.5 - 24
            r = math.hypot(dx, dy)
            if r > 23.5:
                continue
            ang = math.atan2(dy, dx)
            ph = (ang / (2 * math.pi) * 3 + math.log(r + 2.0) * 2.4) % 1.0
            if r < 3.5:
                ch = "a"
            elif ph < 0.10:
                ch = "C" if r > 6 else "c"
            elif ph < 0.2:
                ch = "c" if r > 8 else "B"
            elif ph < 0.34:
                ch = "B"
            elif ph < 0.7:
                ch = "L"
            else:
                ch = "l" if r > 7 else "a"
            if r > 20 and ph > 0.3:     # ふちはとぎれさせて、水になじませる
                ch = "." if (x + y) % 2 else ch
            c.px(x, y, ch)
    return c


def make():
    return {"islet-ruin": ruin(), "islet-cave": cave(), "islet-shrine": shrine(), "islet-fort": fort(), "whirlpool-ring": whirlpool()}
