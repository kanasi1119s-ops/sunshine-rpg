"""芯環塔（64×112、足元＝y=111）。海のど真ん中にそびえる巨岩の柱。上半分は渦巻く灰色の雲にかくれ、てっぺんは雲に消える。
根もとは小さな岩の島と白い波。塔の壁には「灯の環」の輪の筋がうすく巻いている。"""
import math
from lib import Canvas

W, H = 64, 112
CX = 32


def hash2(a, b):
    return ((a * 73856093) ^ (b * 19349663)) & 0xFFFF


def half_width(y):
    """塔の半幅。下ほどすこし広く、岩肌のでこぼこ（3行ごとに±1）。"""
    base = 8.6 + (y - 20) * 0.085 + ((y - 60) ** 2) / 1800.0
    wob = (hash2(y // 3, 7) % 3) - 1
    return base + wob * 1.1


def cloud_lobe(c, cx, cy, r, ry=None):
    ry = ry or r * 0.82
    for y in range(int(cy - ry) - 1, int(cy + ry) + 2):
        for x in range(int(cx - r) - 1, int(cx + r) + 2):
            dx, dy = (x + 0.5 - cx) / r, (y + 0.5 - cy) / ry
            if dx * dx + dy * dy <= 1.0:
                s = dx * 0.7 + dy * 0.9
                c.px(x, y, "T" if s < -0.25 else ("Q" if s > 0.5 else "t"))


def tower(c):
    # 柱の本体。左が明るく、右が暗い
    for y in range(10, 108):
        hw = half_width(y)
        xl, xr = int(round(CX - hw)), int(round(CX + hw))
        for x in range(xl, xr + 1):
            t = (x - CX) / hw
            c.px(x, y, "U" if t < -0.15 else ("u" if t < 0.45 else "V"))
    # 地層の横線（8行ごと。ずらして）
    for y in range(14, 106):
        if (y + (hash2(y // 8, 3) % 3)) % 8 == 0:
            hw = half_width(y)
            xl, xr = int(round(CX - hw)), int(round(CX + hw))
            for x in range(xl + 1, xr):
                if (x + y) % 5 != 0:
                    ch = c.get(x, y)
                    c.px(x, y, {"U": "u", "u": "V"}.get(ch, ch))
    # たて割れ
    for (x0, y0, ln) in ((24, 62, 6), (38, 70, 8), (28, 84, 7), (40, 92, 6), (22, 96, 5)):
        for k in range(ln):
            ch = c.get(x0 + (k // 3), y0 + k)
            c.px(x0 + (k // 3), y0 + k, {"U": "u", "u": "V"}.get(ch, ch))
    # 灯の環の筋（輪が柱を巻く。手前側の下に弧を描く）。うすく。
    for yc in (64, 78, 92):
        for x in range(CX - 18, CX + 19):
            hw = half_width(yc)
            if abs(x - CX) >= hw - 1:
                continue
            u = (x - CX) / hw
            y = int(round(yc + math.sqrt(max(0.0, 1 - u * u)) * 3.2))
            ch = c.get(x, y)
            if ch in "UuV":
                c.px(x, y, {"U": "d", "u": "U", "V": "u"}[ch])
    # 苔（根もとに）
    for (x, y) in ((20, 100), (21, 101), (22, 100), (43, 99), (44, 100), (30, 103)):
        if c.get(x, y) in "UuV":
            c.px(x, y, "g")


def base_island(c):
    # 波の下の影（濃い青）
    c.ell(32, 108, 29, 4, "l")
    # 岩の島：左右の岩塊
    for (cx, cy, rx, ry) in ((13, 103, 12, 6), (51, 104, 12, 5), (32, 104, 19, 5), (6, 106, 6, 4), (58, 107, 5, 3)):
        for y in range(cy - ry, cy + ry + 1):
            for x in range(cx - rx, cx + rx + 1):
                d = ((x + 0.5 - cx) / rx) ** 2 + ((y + 0.5 - cy) / ry) ** 2
                if d <= 1.0:
                    s = ((x - cx) / rx) * 0.6 + ((y - cy) / ry) * 0.8
                    c.px(x, y, "U" if s < -0.2 else ("u" if s < 0.45 else "V"))
    # 砂浜（水ぎわ）
    for x in range(3, 61):
        for y in range(104, 109):
            if c.get(x, y) in "UuV" and y >= 107 - (hash2(x // 2, 1) % 2):
                c.px(x, y, "D" if x < 32 else "d")
    # 岩のすじ
    for (x, y) in ((9, 101), (10, 102), (15, 105), (48, 102), (49, 103), (54, 106), (36, 106), (26, 106)):
        ch = c.get(x, y)
        if ch in "UuV":
            c.px(x, y, {"U": "u", "u": "V", "V": "V"}[ch])
    for (x, y) in ((12, 99), (13, 99), (47, 101), (14, 100)):
        if c.get(x, y) in "UuV":
            c.px(x, y, "G")


def foam(c):
    # 根もとをとりまく白い波（楕円のふち、とぎれとぎれ）
    for x in range(0, 64):
        u = (x - 31.5) / 31.5
        y0 = 108 + math.sqrt(max(0.0, 1 - u * u)) * 3.2
        for k, dy in enumerate((0, 1)):
            y = int(round(y0)) + dy
            if (x + dy * 2) % 6 < 4:
                if c.get(x, y) in ".l":
                    c.px(x, y, "C" if dy == 0 else "c")
    for x in range(2, 62, 5):
        y = 111 if (x // 5) % 2 else 110
        if c.get(x, y) in ".l":
            c.px(x, y, "c"); c.px(x + 1, y, "c")


def clouds(c):
    # 3段のふくらみ。段のあいだから、塔がちらりと見える。いちばん上の段で、てっぺんは見えなくなる。
    tiers = (
        ((18, 11, 9), (30, 8, 11), (44, 11, 9), (26, 15, 8), (38, 15, 9), (35, 3, 7), (22, 5, 6)),                       # 上の段
        ((8, 30, 9), (20, 27, 11), (32, 29, 12), (44, 27, 11), (56, 30, 9), (26, 33, 8), (40, 33, 8), (13, 24, 6), (51, 24, 6)),   # 中の段
        ((6, 50, 9), (17, 47, 11), (32, 49, 13), (47, 47, 11), (58, 50, 9), (25, 54, 9), (40, 54, 9)),   # 下の段（いちばん暗い嵐）
    )
    for tier in tiers:
        for (cx, cy, r) in tier:
            cloud_lobe(c, cx, cy, r, r * (0.82 if cy < 20 else 0.72))
    # 渦巻きのすじ（時計まわり、段にそって）
    for (rr, a0, ln, cy) in ((8, 3.4, 2.4, 9), (12, 4.6, 2.2, 28), (16, 3.6, 2.4, 28), (14, 3.2, 2.4, 49), (22, 4.4, 2.2, 49)):
        n = int(rr * ln * 1.8)
        for i in range(n):
            a = a0 + ln * i / n
            x = int(round(32 + math.cos(a) * rr * 1.8))
            y = int(round(cy + math.sin(a) * rr * 0.42))
            ch = c.get(x, y)
            if ch in "Tt":
                c.px(x, y, {"T": "t", "t": "Q"}[ch])
    # 段のあいだの塔は、もやでうす暗く
    for y in range(14, 64):
        for x in range(0, 64):
            if c.get(x, y) in "UuV" and y < 60 and (x + y) % 2 == 0:
                c.px(x, y, {"U": "u", "u": "V", "V": "V"}[c.get(x, y)])


def make():
    c = Canvas(W, H)
    foam_layer = Canvas(W, H)
    base_island(c)
    tower(c)
    clouds(c)
    c.outline()
    foam(c)
    return {"spire": c}
