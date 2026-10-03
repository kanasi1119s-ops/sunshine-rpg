"""ダンジョン・遺跡の飾り（前半: 石柱2種・石像2種・垂れ幕2色・骨の山・くも巣・燭台・棺）。"""
import sys, math
from lib import *

STC = ("#24222e", "#4c4a62", "#6e6c86", "#9694ae")   # 縁, 影, 地, 上面（冷たい石）
WOOD = ("#2a1a10", "#5a3a20", "#7a5230", "#9a6c40")
BRONZE = ("#4a2c14", "#8a5a24", "#c08a3c")

def _col_stone(p):
    return p(*STC)

def pillar():
    p = Pal(); g = G(20, 48)
    ol, sd, md, lt = _col_stone(p)
    sh = p(DUNG_SH)
    mo, mod = p("#4a7a48", "#2e5034")
    # 柱頭（階段状）
    g.rect(1, 0, 18, 2, md); g.rect(1, 0, 18, 0, lt)
    g.rect(3, 3, 16, 5, md)
    for y in range(0, 6):
        for x in range(0, 20):
            if g.get(x, y) != ".":
                if x >= 13: g.put(x, y, sd)
                elif x >= 6 and y > 0: pass
    for x in range(3, 17): g.put(x, 5, sd)
    # 柱身（縦のみぞで丸みを出す）
    for y in range(6, 41):
        for x in range(4, 16):
            u = (x - 4) / 11
            c = lt if u < 0.28 else md if u < 0.68 else sd
            if x in (7, 10, 13): c = {lt: md, md: sd, sd: sd}[c]
            g.put(x, y, c)
    # 台座
    g.rect(2, 41, 17, 43, md); g.rect(0, 44, 19, 46, md)
    for x in range(2, 18): g.put(x, 41, lt if x < 12 else md); g.put(x, 43, sd)
    for x in range(0, 20): g.put(x, 44, lt if x < 12 else md); g.put(x, 46, sd)
    for y in range(41, 47):
        for x in range(13, 20):
            if g.get(x, y) == md: g.put(x, y, sd)
    # ひび・欠け・苔
    for (x, y) in ((8, 14), (8, 15), (9, 16), (9, 17), (10, 18), (7, 26), (7, 27), (6, 28), (6, 29)): g.put(x, y, ol)
    for (x, y) in ((4, 39), (5, 40), (4, 40), (5, 39), (6, 40), (3, 44), (2, 45), (3, 45)): g.put(x, y, mo)
    for (x, y) in ((5, 40), (3, 45), (6, 40)): g.put(x, y, mod)
    g.outline(ol, {mo: mod, mod: ol})
    g.shadow(10, 47, 9, sh, 0)
    return g, p

def pillar_broken():
    p = Pal(); g = G(26, 40)
    ol, sd, md, lt = _col_stone(p)
    sh = p(DUNG_SH)
    mo, mod = p("#4a7a48", "#2e5034")
    Y = 10   # 台座の上端をずらす
    # 台座
    g.rect(4, 34, 17, 35, md); g.rect(2, 36, 19, 38, md)
    for x in range(4, 18): g.put(x, 34, lt if x < 11 else md); g.put(x, 35, sd)
    for x in range(2, 20): g.put(x, 36, lt if x < 11 else md); g.put(x, 38, sd)
    for y in range(34, 39):
        for x in range(13, 20):
            if g.get(x, y) == md: g.put(x, y, sd)
    # 柱身（折れ口はななめにぎざぎざ。左が高く右が低い）
    tops = {5: 15, 6: 13, 7: 12, 8: 14, 9: 13, 10: 17, 11: 16, 12: 19, 13: 18, 14: 21, 15: 20, 16: 22}
    for x in range(5, 17):
        t = tops[x]
        for y in range(t, 34):
            u = (x - 5) / 11
            c = lt if u < 0.28 else md if u < 0.68 else sd
            if x in (8, 11, 14): c = {lt: md, md: sd, sd: sd}[c]
            g.put(x, y, c)
        g.put(x, t, lt if x < 11 else md)
        if x % 2 == 1: g.put(x, t + 1, sd)
    # 倒れた柱のかけら（輪切り）
    g.ell(21, 35, 4.4, 3.2, lambda x, y, nx, ny: md if nx < 0.2 else sd)
    g.ell(18.8, 34.6, 1.8, 2.7, lambda x, y, nx, ny: lt)
    for (x, y) in ((1, 38), (2, 38), (2, 37), (0, 39), (24, 39), (23, 38)): g.put(x, y, md if x < 12 else sd)
    for (x, y) in ((5, 32), (6, 33), (5, 33), (7, 33)): g.put(x, y, mo)
    g.put(6, 33, mod)
    for (x, y) in ((10, 22), (10, 23), (11, 24), (11, 25), (8, 28), (8, 29)): g.put(x, y, ol)
    g.outline(ol, {mo: mod, mod: ol})
    g.shadow(12, 39, 12, sh, 0)
    return g, p

def _statue_base(g, md, lt, sd, ol, x0, x1, y0):
    g.rect(x0, y0, x1, y0 + 1, md)
    g.rect(x0 + 1, y0 + 2, x1 - 1, y0 + 7, md)
    for x in range(x0, x1 + 1): g.put(x, y0, lt if x < (x0 + x1) / 2 + 2 else md)
    for y in range(y0 + 2, y0 + 8):
        for x in range(x0 + 1, x1):
            g.put(x, y, lt if x < x0 + 5 else md if x < x1 - 4 else sd)
    g.rect(x0, y0 + 8, x1, y0 + 9, md)
    for x in range(x0, x1 + 1): g.put(x, y0 + 8, md if x < x1 - 4 else sd); g.put(x, y0 + 9, sd)

def statue_soldier():
    p = Pal(); g = G(26, 46)
    ol, sd, md, lt = _col_stone(p)
    sh = p(DUNG_SH)
    mo, mod = p("#4a7a48", "#2e5034")
    S = lambda x, a=10, b=15: lt if x < a else md if x < b else sd
    _statue_base(g, md, lt, sd, ol, 3, 22, 36)
    # 脚
    g.rect(8, 28, 11, 35, md); g.rect(14, 28, 17, 35, md)
    for y in range(28, 36):
        for x in (8, 9): g.put(x, y, lt)
        for x in (14, 15): g.put(x, y, lt)
        g.put(11, y, sd); g.put(17, y, sd)
    g.rect(7, 35, 11, 35, sd); g.rect(14, 35, 18, 35, sd)
    # 胴（鎧）
    g.poly([(7, 28), (6, 19), (9, 15), (17, 15), (20, 19), (19, 28)], lambda x, y: S(x, 11, 16))
    for y in range(20, 28): g.put(13, y, sd)
    g.rect(7, 27, 19, 28, sd)       # 帯
    g.rect(7, 26, 12, 26, md)
    # 肩あて
    g.ell(7, 17, 3, 2.3, lambda x, y, nx, ny: lt if nx < 0 else md)
    g.ell(19, 17, 3, 2.3, lambda x, y, nx, ny: sd)
    # 兜（面頬のすきま、とさか）
    g.ell(13, 11, 4.2, 4.8, lambda x, y, nx, ny: lt if nx < -0.2 else md if nx < 0.5 else sd)
    g.rect(10, 11, 16, 12, ol)
    g.rect(13, 12, 13, 15, ol)
    g.rect(12, 4, 13, 6, md); g.rect(13, 3, 14, 5, sd); g.put(12, 4, lt)
    # 盾（左手側＝向かって左）
    g.poly([(1, 20), (7, 19), (7, 28), (4, 32), (1, 28)], lambda x, y: lt if x < 4 else md)
    g.rect(1, 22, 6, 22, sd); g.rect(4, 20, 4, 30, sd)
    g.put(3, 25, ol)
    # 槍（右手側）
    g.rect(22, 4, 22, 35, md)
    for y in range(4, 36): g.put(23, y, sd)
    g.poly([(21, 4), (22, -1), (24, 4)], md) if False else None
    g.rect(21, 2, 23, 4, md); g.put(22, 1, md); g.put(22, 0, lt); g.put(23, 3, sd); g.put(23, 2, sd)
    g.rect(19, 21, 21, 23, md); g.put(21, 22, sd)   # 手
    # 苔
    for (x, y) in ((4, 44), (5, 43), (5, 44), (6, 44), (20, 44), (21, 43), (21, 44)): g.put(x, y, mo)
    g.put(5, 44, mod); g.put(21, 44, mod)
    g.outline(ol, {mo: mod, mod: ol})
    g.shadow(13, 45, 11, sh, 0)
    return g, p

def statue_winged():
    p = Pal(); g = G(36, 50)
    ol, sd, md, lt = _col_stone(p)
    sh = p(DUNG_SH)
    gl1, gl2, gl3 = p("#6ab8d8", "#a8e4f4", "#e8fbff")    # 手の中の光の玉（光る）
    mo, mod = p("#4a7a48", "#2e5034")
    S = lambda x, a, b: lt if x < a else md if x < b else sd
    _statue_base(g, md, lt, sd, ol, 8, 27, 40)
    # 翼（左右。ふちはぎざぎざの風切り羽、羽根の筋を影色で入れる。左が明るい）
    pts = [(14, 22), (9, 12), (4, 6), (1, 5), (1, 11), (2, 17), (4, 16), (3, 23), (6, 22), (6, 29), (9, 27), (10, 32), (13, 28)]
    for side in (-1, 1):
        P = [(x if side < 0 else 35 - x, y) for (x, y) in pts]
        g.poly(P, lambda x, y, side=side: (lt if (x + y) % 9 < 5 else md) if side < 0 else (md if (x - y) % 9 < 5 else sd))
        for (ex, ey) in ((2, 8), (3, 14), (4, 20), (7, 25), (10, 29)):
            ex2 = ex if side < 0 else 35 - ex; sx = 13 if side < 0 else 22
            g.line(sx, 22, ex2, ey, sd if side < 0 else ol)
    # 衣
    g.poly([(10, 40), (12, 24), (14, 18), (21, 18), (23, 24), (25, 40)], lambda x, y: S(x, 15, 20))
    for y in range(26, 40): g.put(17, y, sd) if y % 3 else None
    for y in range(28, 40): g.put(21, y, sd)
    g.rect(12, 24, 23, 25, md); g.rect(16, 24, 19, 25, sd)   # 帯
    # 頭
    g.ell(17.5, 13, 3.6, 4.2, lambda x, y, nx, ny: lt if nx < -0.1 else md if nx < 0.55 else sd)
    g.rect(15, 12, 16, 12, ol); g.rect(19, 12, 20, 12, ol)
    g.rect(13, 8, 22, 9, md)   # 髪の輪（かんむり）
    g.rect(14, 7, 21, 7, lt)
    # 腕と光の玉
    g.rect(13, 20, 14, 26, md); g.rect(21, 20, 22, 26, sd)
    g.ell(17.5, 25, 3.2, 3.2, lambda x, y, nx, ny: gl3 if nx * nx + ny * ny < 0.25 else gl2 if nx + ny < 0.4 else gl1)
    g.rect(15, 27, 20, 28, md)
    for (x, y) in ((10, 49), (11, 48), (28, 49), (27, 48)): g.put(x, y, mo)
    g.put(11, 49, mod)
    g.outline(ol, {mo: mod, mod: ol, gl1: sd, gl2: gl1, gl3: gl1})
    g.shadow(18, 49, 14, sh, 0)
    return g, p

def _banner(base, shade, deep):
    p = Pal(); g = G(22, 42)
    ol = p("#2a1c18")
    c1, c2, c3 = p(base, shade, deep)
    gd1, gd2 = p("#f0c850", "#b08428")
    wl, wk = p("#7a5230", "#5a3a20")
    ir = p("#5c6070")
    # 吊り棒と先かざり
    g.rect(1, 1, 20, 2, wl); g.rect(1, 2, 20, 2, wk)
    g.rect(0, 0, 1, 3, gd1); g.rect(20, 0, 21, 3, gd2)
    # 布（ゆるく波打つ）
    for y in range(3, 36):
        sway = round(math.sin(y / 5.0) * 0.8)
        # 下端は燕尾（V字の切れ込み）
        notch = 0
        if y >= 28: notch = (y - 27) * 1.4
        for x in range(3 + sway, 19 + sway):
            if abs(x - (10.5 + sway)) < notch: continue
            u = (x - 3 - sway) / 15
            c = c1 if u < 0.55 else c2
            if (x - 3 - sway) in (5, 11): c = c2 if c == c1 else c3     # たて折り
            g.put(x, y, c)
        # 縁どり（金）
        g.put(3 + sway, y, gd1); g.put(18 + sway, y, gd2)
    for x in range(3, 19): g.put(x, 3, gd1 if x < 11 else gd2)
    # 紋章：輪（灯の環）
    cx, cy = 10.5, 15
    for y in range(8, 23):
        for x in range(5, 17):
            d = math.hypot(x + .5 - cx, y + .5 - cy)
            if 3.2 <= d <= 5.0: g.put(x, y, gd1 if (x < 11 or y < 15) else gd2)
    g.rect(10, 13, 11, 17, gd2) if False else None
    g.put(10, 15, gd1); g.put(11, 15, gd2); g.put(10, 14, gd1); g.put(11, 16, gd2)
    # 房（ふさ）
    g.put(5, 34, gd1); g.put(5, 35, gd2); g.put(16, 34, gd1); g.put(16, 35, gd2)
    g.outline(ol, {gd1: c3, gd2: c3, c1: c3, c2: c3, c3: ol, wl: ol, wk: ol})
    return g, p

def banner_purple(): return _banner("#8a52b8", "#5e3a8a", "#3a2460")
def banner_red(): return _banner("#c8403c", "#8e2c34", "#5a1a28")

def bones():
    p = Pal(); g = G(34, 18)
    ol = p("#2e2620")
    b1, b2, b3 = p("#ece0c4", "#bcae8e", "#7e705a")
    sh = p(DUNG_SH)
    dark = p("#1a1618")
    # 土台の小さな骨のかたまり
    def pile(x, y, nx, ny):
        n = hn(x, y, 7) % 5
        return b3 if (ny > 0.35 or nx > 0.6) else b2 if n < 2 else b1 if n < 3 else b3
    g.ell(17, 14, 15, 4.2, pile)
    # 長い骨（交差）
    def bone(x0, y0, x1, y1):
        g.line(x0, y0, x1, y1, b1); g.line(x0, y0 + 1, x1, y1 + 1, b2)
        for (x, y) in ((x0, y0), (x1, y1)):
            g.put(x, y - 1, b1); g.put(x + (1 if x == x0 else -1), y - 1, b1); g.put(x, y + 2, b2); g.put(x + (1 if x == x0 else -1), y + 2, b2)
    # あばら骨（弧）
    for k in range(3):
        for t in range(0, 11):
            x = 20 + t; y = 11 - 2 * math.sin(math.pi * t / 10) - k * 0.0 + k * 1.2
            g.put(x, round(y), b1 if t % 2 == 0 else b2)
    # どくろ
    def skull(cx, cy, r):
        g.ell(cx, cy, r, r * 0.92, lambda x, y, nx, ny: b1 if (nx < 0.1 and ny < 0.3) else b2 if (nx + ny) < 0.9 else b3)
        g.rect(cx - r * 0.5, cy + r * 0.55, cx + r * 0.4, cy + r * 1.05, b2)   # あご
        e = max(1, int(r / 3))
        g.rect(cx - r * 0.6, cy - 0.5, cx - r * 0.6 + e, cy - 0.5 + e, dark)
        g.rect(cx + r * 0.1, cy - 0.5, cx + r * 0.1 + e, cy - 0.5 + e, dark)
        g.put(cx - 0.2, cy + r * 0.45, dark)
        for k in range(int(r * 0.9)):
            if k % 2 == 0: g.put(cx - r * 0.45 + k, cy + r * 1.0, ol)
    skull(11, 6, 4)
    skull(25, 6, 3)
    skull(5, 13, 2)
    bone(3, 14, 18, 10)
    bone(14, 10, 30, 14)
    g.outline(ol, {b1: ol, b2: ol, b3: ol})
    g.shadow(17, 17, 15, sh, 0)
    return g, p

def cobweb():
    p = Pal(); g = G(26, 26)
    w1, w2 = p("#e4e4f0", "#a0a0b8")
    sp = p("#1a1618"); sg = p("#c04a4a")
    # 左上の角から放射状に糸（6本）と、そのあいだをつなぐ弧（少したるむ）
    angs = [6, 24, 42, 60, 78]
    for k in angs:
        a = math.radians(k)
        g.line(0, 0, 25 * math.cos(a), 25 * math.sin(a), w1 if k in (24, 60) else w2)
    for r in (10, 17, 24):
        for i in range(len(angs) - 1):
            a0, a1 = math.radians(angs[i]), math.radians(angs[i + 1])
            p0 = (r * math.cos(a0), r * math.sin(a0)); p1 = (r * math.cos(a1), r * math.sin(a1))
            am = (a0 + a1) / 2; rm = r - 2.8
            pm = (rm * math.cos(am), rm * math.sin(am))
            g.line(p0[0], p0[1], pm[0], pm[1], w1 if r != 10 else w2); g.line(pm[0], pm[1], p1[0], p1[1], w1 if r != 10 else w2)
    # ぶら下がるくも
    for y in range(8, 15): g.put(18, y, w2)
    g.ell(18, 17, 1.8, 1.6, lambda x, y, nx, ny: sp)
    g.put(18, 16, sg)
    for (dx, dy) in ((-3, 15), (-2, 14), (3, 15), (2, 14), (-3, 19), (-2, 18), (3, 19), (2, 18)): g.put(18 + dx, dy + 1, sp)
    return g, p

def candelabra():
    p = Pal(); g = G(20, 38)
    ol, b2, b1 = p(*BRONZE)
    sh = p(DUNG_SH)
    wx, wxd = p("#ece0c4", "#b4a888")
    f1, f2, f3 = p("#f08428", "#ffd050", "#fff4b8")
    # 脚（三つ足）と台
    g.ell(10, 35, 6, 2, lambda x, y, nx, ny: b1 if nx < 0 else b2)
    g.rect(9, 20, 10, 34, b1);
    for y in range(20, 35): g.put(10, y, b2)
    g.rect(8, 27, 11, 28, b1); g.put(11, 27, b2); g.put(11, 28, b2)
    g.rect(7, 31, 12, 32, b1); g.put(12, 31, b2); g.put(12, 32, b2)
    # 腕（左右に曲がって上へ）
    for side in (-1, 1):
        pts = [(10, 21), (10 + side * 3, 23), (10 + side * 5, 22), (10 + side * 7, 18), (10 + side * 7, 14)]
        for (xa, ya), (xb, yb) in zip(pts, pts[1:]): g.line(xa, ya, xb, yb, b1 if side < 0 else b2)
    g.rect(10, 12, 10, 20, b1)
    # ろうそくと皿
    cs = ((3, 14), (10, 12), (17, 14))
    for (cx, cy) in cs:
        g.rect(cx - 2, cy, cx + 2, cy, b1); g.put(cx + 2, cy, b2)
        g.rect(cx - 1, cy - 4, cx, cy - 1, wx); g.put(cx + 1, cy - 4, wxd); g.put(cx + 1, cy - 3, wxd); g.put(cx + 1, cy - 2, wxd); g.put(cx + 1, cy - 1, wxd)
        # 炎
        g.rect(cx, cy - 8, cx, cy - 5, f2); g.put(cx - 1, cy - 6, f1); g.put(cx - 1, cy - 7, f1) if False else None
        g.put(cx, cy - 9, f1); g.put(cx, cy - 8, f2); g.put(cx, cy - 7, f3); g.put(cx, cy - 6, f3); g.put(cx - 1, cy - 6, f2); g.put(cx + 1, cy - 6, f1)
        g.put(cx, cy - 5, f2)
    g.outline(ol, {f1: b2, f2: f1, f3: f2})
    g.shadow(10, 37, 7, sh, 0)
    return g, p

def coffin():
    p = Pal(); g = G(44, 28)
    ol, dp, sd, md = p("#1e1218", "#3c2430", "#5a3a44", "#7a5058")
    lt = p("#94646c")
    br1, br2 = p("#c08a3c", "#8a5a24")
    sh = p(DUNG_SH)
    mo, mod = p("#4a7a48", "#2e5034")
    # 前面（側板）と、ふた（上面は明るく、へこんだ中の板は一段暗く）
    g.poly([(5, 15), (11, 20), (35, 20), (41, 15), (41, 23), (35, 26), (11, 26), (5, 23)], lambda x, y: md if x < 18 else sd if x < 32 else dp)
    g.poly([(2, 12), (9, 5), (35, 5), (42, 12), (35, 19), (9, 19)], lambda x, y: lt if x < 30 else md)
    g.poly([(7, 12), (12, 8), (32, 8), (37, 12), (32, 16), (12, 16)], lambda x, y: md if x < 24 else sd)
    # 頭側の肩（ふたの左の角を少し持ち上げて棺らしく）
    for (x, y) in ((3, 12), (4, 11), (5, 10)): g.put(x, y, lt)
    # 金具の帯と留め
    for x0 in (14, 30):
        g.rect(x0, 8, x0 + 1, 16, br1)
        g.rect(x0 + 1, 8, x0 + 1, 16, br2)
        g.rect(x0, 21, x0 + 1, 25, br1)
    # 紋章：輪
    for y in range(6, 19):
        for x in range(17, 29):
            d = math.hypot(x + .5 - 22.5, y + .5 - 12)
            if 2.6 <= d <= 4.0: g.put(x, y, br1 if (x < 22 or y < 12) else br2)
    # 縁のけずれと苔
    for (x, y) in ((6, 24), (7, 25), (8, 25), (38, 22), (39, 22)): g.put(x, y, mo)
    g.put(7, 25, mod)
    g.outline(ol, {mo: mod, mod: ol, br1: br2, br2: ol})
    g.shadow(22, 27, 20, sh, 0)
    return g, p

ALL = ["pillar", "pillar-broken", "statue-soldier", "statue-winged", "banner-purple", "banner-red", "bones", "cobweb", "candelabra", "coffin"]

if __name__ == "__main__":
    names = sys.argv[1:] or ALL
    for n in names:
        g, p = globals()[n.replace("-", "_")]()
        print(n, write(n, g, p))
