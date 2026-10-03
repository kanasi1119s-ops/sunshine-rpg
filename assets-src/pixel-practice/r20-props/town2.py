"""町の飾りの続き（荷車・洗濯物・柵・ベンチ・旅人像・墓石・立て札・かがり火台・灯りの祠）。"""
import sys, math
from lib import *
from town import WOOD, STONE, IRON

def cart():
    p = Pal(); g = G(48, 32)
    ol, wk, wl, wm = p(*WOOD)
    sh = p(GRASS_SH)
    ir, ird = p("#6a6e7c", "#3a3e4c")
    sk, skd, skdd = p("#d8c080", "#a89050", "#7a6638")
    hy, hyd = p("#d8b44c", "#a88430")
    # 荷：麻袋の山とわら
    for (cx, cy, rx, ry) in ((15, 8, 6, 5), (26, 7, 6.5, 5.5), (37, 9, 5.5, 4.5), (21, 4, 5, 3.6)):
        g.ell(cx, cy, rx, ry, lambda x, y, nx, ny: sk if (nx * .8 + ny * .6) < 0.1 else skd if (nx + ny) < 0.9 else skdd)
    for (x, y) in ((15, 3), (16, 3), (26, 2), (27, 2), (37, 5), (38, 5), (21, 1), (22, 1)): g.put(x, y, skdd)
    # 荷台
    g.rect(6, 13, 44, 21, wl)
    for x in range(6, 45): g.put(x, 13, wm); g.put(x, 21, wk); g.put(x, 20, wk)
    for x in range(30, 45):
        for y in range(14, 20): g.put(x, y, wk)
    for y in range(14, 20): g.put(6, y, wm); g.put(7, y, wm)
    g.rect(6, 17, 44, 17, wk)
    for x in (13, 21, 30, 38): g.rect(x, 14, x, 19, wk)
    # 後ろの足（地面に立つ棒）
    g.rect(39, 22, 40, 29, wk); g.put(39, 22, wl)
    # 持ち手（左へ伸びる2本の柄）
    g.line(6, 16, 1, 27, wl); g.line(7, 16, 2, 27, wl); g.line(7, 18, 3, 27, wk)
    # 車輪（手前）
    cx, cy, R = 24, 23.5, 7.6
    g.ell(cx, cy, R, R, lambda x, y, nx, ny: (wm if (nx < 0.1 and ny < 0.2) else wl) if math.hypot(nx, ny) > 0.74 else ol)
    for k in range(8):
        a = k * math.pi / 4
        g.line(cx, cy, cx + math.cos(a) * 5.4, cy + math.sin(a) * 5.4, wl if math.cos(a) + math.sin(a) < 0.3 else wk)
    g.ell(cx, cy, 2, 2, lambda x, y, nx, ny: ir if nx < 0 else ird)
    g.outline(ol, {sk: skdd, skd: skdd, skdd: ol})
    g.shadow(24, 31, 22, sh, 1)
    return g, p

def laundry():
    p = Pal(); g = G(48, 36)
    ol, wk, wl, wm = p(*WOOD)
    sh = p(GRASS_SH); rope = p("#d8c8a0")
    st, std = p("#8a8478", "#5a564e")
    wh, whd, whdd = p("#f4f0e4", "#c8c4b8", "#9c98a0")
    bl, bld = p("#5a86c8", "#3a5a98")
    rd, rdd = p("#d0504a", "#98303a")
    yl, yld = p("#e8c050", "#b88c30")
    gr, grd = p("#6ab070", "#3e8050")
    # 柱
    for y in range(7, 33):
        g.put(4, y, wl); g.put(5, y, wk); g.put(42, y, wl); g.put(43, y, wk)
    for (x0) in (3, 41):
        g.rect(x0, 31, x0 + 3, 33, st); g.rect(x0 + 2, 31, x0 + 3, 33, std)
    # ロープ（たるむ曲線）
    pts = []
    for x in range(5, 43):
        t = (x - 5) / 37
        y = 8 + 4 * math.sin(math.pi * t)
        pts.append((x, round(y)))
        g.put(x, round(y), rope)
    def ry(x): return dict(pts)[x]
    def cloth(x0, w, h, a, ad, add=None, style="sheet"):
        for x in range(x0, x0 + w):
            top = ry(x) + 1
            hh = h + (1 if (x - x0) % 3 == 1 and style == "sheet" else 0)
            for y in range(top, top + hh):
                u = (x - x0) / (w - 1)
                c = a if u < 0.5 else ad
                if add and u > 0.8: c = add
                g.put(x, y, c)
        # 洗濯ばさみ
        g.put(x0 + 1, ry(x0 + 1), wl); g.put(x0 + w - 2, ry(x0 + w - 2), wl)
    cloth(8, 11, 14, wh, whd, whd)
    # シャツ（青）：袖つき
    x0 = 22
    cloth(x0, 7, 9, bl, bld)
    for k in range(2):
        g.put(x0 - 1 - k, ry(x0) + 2 + k, bl); g.put(x0 - 1 - k, ry(x0) + 3 + k, bl)
        g.put(x0 + 7 + k, ry(x0 + 6) + 2 + k, bld); g.put(x0 + 7 + k, ry(x0 + 6) + 3 + k, bld)
    cloth(33, 5, 6, rd, rdd)
    cloth(39, 3, 5, yl, yld)
    # 小さな布（靴下・緑）
    cloth(18, 3, 6, wh, whd)
    # 裾のぎざぎざ
    for x in range(8, 19, 2): g.put(x, ry(x) + 15, ".")
    g.outline(ol, {wh: whdd, whd: ol, whdd: ol, rope: ol, st: std, std: ol, bl: bld, bld: ol, rd: rdd, rdd: ol, yl: yld, yld: ol, gr: grd, grd: ol})
    g.shadow(24, 34, 22, sh, 1)
    return g, p

def _fence(end):
    p = Pal(); g = G(16, 18)
    ol, wk, wl, wm = p(*WOOD)
    sh = p(GRASS_SH)
    px0, px1 = (6, 9) if not end else (10, 14)
    top = 3 if not end else 1
    # 2段の横木（左から右まで全幅。隣とつながる）
    x_end = 15 if not end else 11
    for (y0) in (7, 12):
        for x in range(0, x_end + 1):
            g.put(x, y0, wm); g.put(x, y0 + 1, wl); g.put(x, y0 + 2, wk)
    # 杭
    for y in range(top, 17):
        for x in range(px0, px1 + 1):
            c = wl if x - px0 < (px1 - px0) / 2 else wk
            g.put(x, y, c)
    if end:
        # 端の杭は少し太く、頭に笠
        for x in range(px0 - 1, px1 + 2): g.put(x, top, wm); g.put(x, top + 1, wl)
    else:
        for x in range(px0 + 1, px1): g.put(x, top - 1, wl if x < 8 else wk)
    ob = {wm: ol, wl: ol, wk: ol}
    # 縁取りは杭の上と横木のふちだけ（横は隣とつながるので左右には引かない）
    g2 = G(16, 18); g2.g = [r[:] for r in g.g]
    g.outline(ol, {})
    # 左右の端（横木が隣へ続くところ）の縁取りは消す
    if not end:
        for y in range(18):
            for x in (0, 15):
                pass
    # 地面の影
    for x in range(0, 16 if not end else 14):
        g.put(x, 17, sh)
    g.put(6, 17, ol)
    return g, p

def fence(): return _fence(False)
def fence_end(): return _fence(True)

def bench():
    p = Pal(); g = G(32, 20)
    ol, wk, wl, wm = p(*WOOD)
    sh = p(GRASS_SH)
    ir, ird = p("#5c6070", "#3a3e4c")
    # 背もたれ（2枚）
    g.rect(3, 1, 28, 3, wl); g.rect(3, 4, 28, 6, wl)
    for x in range(3, 29): g.put(x, 1, wm); g.put(x, 4, wm); g.put(x, 3, wk); g.put(x, 6, wk)
    # 背の支え
    g.rect(5, 7, 6, 11, wk); g.rect(25, 7, 26, 11, wk)
    # 座面（上面＋前面）
    g.rect(1, 9, 30, 10, wm)
    g.rect(1, 11, 30, 13, wl)
    for x in range(1, 31): g.put(x, 13, wk)
    for x in range(1, 31):
        if x % 7 == 3: g.put(x, 9, wl); g.put(x, 10, wl)
    # 脚（鉄の脚）
    for x0 in (3, 26):
        g.rect(x0, 14, x0 + 2, 17, ir); g.put(x0 + 2, 14, ird); g.rect(x0 + 2, 15, x0 + 2, 17, ird)
        g.rect(x0 - 1, 17, x0 + 3, 17, ird)
    g.outline(ol, {ir: ird, ird: ird})
    g.shadow(16, 18, 15, sh, 1)
    return g, p

def statue_traveler():
    p = Pal(); g = G(24, 44)
    ol, sd, md, lt = p(*STONE)
    sh = p(GRASS_SH)
    st, std, stl = p("#6a6e7a", "#8e929e", "#4c505c")   # 像：青みの石（台座とは別の色）
    mo, mod = p("#5a8a48", "#3a6034")
    # 台座
    g.rect(3, 33, 20, 41, md)
    for y in range(33, 42):
        for x in range(3, 21):
            if x > 13: g.put(x, y, sd)
    for x in range(2, 22): g.put(x, 33, lt if x < 14 else md); g.put(x, 32, lt if x < 14 else md)
    g.rect(2, 41, 21, 42, md)
    for x in range(2, 22):
        if x > 13: g.put(x, 41, sd); g.put(x, 42, sd)
        else: g.put(x, 42, sd)
    for (x, y) in ((8, 36), (9, 36), (15, 38), (6, 40)): g.put(x, y, sd if x < 14 else ol)
    for (x, y) in ((3, 41), (4, 40), (5, 41), (4, 41), (19, 41), (20, 40)): g.put(x, y, mo)
    g.put(4, 41, mod)
    # 像：旅人（つば広の帽子、マフラー、外套、杖、背負い袋）。光は左上
    sh3 = lambda x, c0=11, c1=14: std if x < c0 else st if x < c1 else stl
    g.poly([(6, 32), (7, 24), (8, 19), (16, 19), (17, 24), (18, 32)], lambda x, y: sh3(x))
    for y in range(26, 32): g.put(12, y, stl if y % 2 else st)
    # 肩のマント線とマフラー
    g.rect(8, 18, 16, 19, st); g.rect(8, 18, 11, 18, std); g.rect(14, 18, 16, 19, stl)
    g.rect(10, 20, 11, 24, stl)
    # 顔
    g.ell(12, 14.5, 3.0, 3.4, lambda x, y, nx, ny: std if nx < 0.1 else st)
    g.put(11, 14, stl); g.put(13, 14, stl)
    # 帽子（広いつば＋とんがり帽）
    g.rect(5, 11, 19, 11, st); g.rect(5, 11, 11, 11, std); g.rect(16, 11, 19, 11, stl)
    g.rect(6, 12, 18, 12, stl)
    g.poly([(8, 11), (9, 6), (12, 4), (15, 6), (16, 11)], lambda x, y: std if x < 11 else st if x < 14 else stl)
    g.rect(8, 9, 16, 9, stl)
    # 背負い袋
    g.ell(18.5, 25, 3, 4.8, lambda x, y, nx, ny: st if nx < 0 else stl)
    g.rect(16, 21, 17, 22, stl)
    # 杖（左手）。杖は少し明るい石
    g.rect(4, 11, 4, 32, lt)
    g.put(3, 10, lt); g.put(4, 10, lt); g.put(5, 10, lt)
    g.rect(5, 24, 8, 27, std); g.put(6, 25, st)
    g.outline(ol, {std: stl, st: stl, stl: ol, mo: mod, mod: ol})
    g.shadow(12, 43, 11, sh, 1)
    return g, p

def _grave(cross):
    p = Pal(); h = 24 if cross else 22
    g = G(16, h)
    ol, sd, md, lt = p(*STONE)
    sh = p(GRASS_SH)
    so, sod = p("#6a4a30", "#4a3220")      # 土
    gr, grd = p("#5a9a40", "#3a6a2c")
    fl = p("#f0d860")
    if cross:
        g.rect(6, 3, 9, 17, md)
        g.rect(2, 6, 13, 9, md)
        for y in range(3, 18): g.put(6, y, lt); g.put(9, y, sd); g.put(8, y, sd)
        for x in range(2, 14): g.put(x, 6, lt); g.put(x, 9, sd) if x > 5 else g.put(x, 9, md)
        g.put(2, 7, lt); g.put(2, 8, lt)
        for x in range(10, 14): g.put(x, 7, md); g.put(x, 8, sd)
        g.put(13, 6, md)
        g.put(7, 12, sd); g.put(7, 13, ol)
        base_y = 17
    else:
        g.ell(8, 9, 5, 5.5, lambda x, y, nx, ny: lt if nx < -0.3 else md if nx < 0.45 else sd)
        g.rect(3, 9, 12, 17, md)
        for y in range(9, 18):
            for x in range(3, 13):
                g.put(x, y, lt if x < 6 else md if x < 10 else sd)
        # 彫り：小さな輪（灯の環のかたち）
        for (x, y) in ((7, 7), (8, 7), (6, 8), (9, 8), (6, 9), (9, 9), (7, 10), (8, 10)): g.put(x, y, sd if x < 8 else ol)
        for x in range(5, 11): g.put(x, 13, sd if x < 8 else ol)
        for x in range(5, 10): g.put(x, 15, sd if x < 8 else ol)
        base_y = 17
    # 土まんじゅうと草
    g.ell(8, base_y + 2.2, 7.5, 2.8, lambda x, y, nx, ny: so if nx < 0.2 else sod)
    for (x, y) in ((2, base_y + 1), (3, base_y), (13, base_y + 1), (12, base_y), (1, base_y + 2)): g.put(x, y, gr)
    g.put(3, base_y + 1, grd); g.put(13, base_y + 2, grd)
    g.put(11, base_y + 1, fl)
    g.outline(ol, {so: sod, sod: ol, gr: grd, grd: ol})
    g.shadow(8, h - 1, 7, sh, 0)
    return g, p

def grave_cross(): return _grave(True)
def grave_round(): return _grave(False)

def noticeboard():
    p = Pal(); g = G(32, 38)
    ol, wk, wl, wm = p(*WOOD)
    sh = p(GRASS_SH)
    pa, pad = p("#f2e8c8", "#c8b890")
    pb, pbd = p("#d8e4f0", "#9cacc0")
    pr = p("#c8483c"); ink = p("#5a4a3a")
    # 柱と小さな屋根
    g.rect(4, 14, 6, 36, wl); g.rect(25, 14, 27, 36, wl)
    for y in range(14, 37): g.put(6, y, wk); g.put(27, y, wk)
    g.poly([(1, 11), (16, 2), (31, 11)], lambda x, y: wm if x < 16 else wl)
    for x in range(1, 32): g.put(x, 11, wk) if x > 15 else g.put(x, 11, wl)
    g.rect(2, 11, 29, 12, wk)
    # 板
    g.rect(3, 13, 28, 28, wl)
    for y in range(13, 29): g.put(3, y, wm); g.put(28, y, wk); g.put(27, y, wk)
    for x in range(3, 29): g.put(x, 13, wm); g.put(x, 28, wk)
    for x in range(4, 27): g.put(x, 20, wk)
    # 貼り紙
    def note(x0, y0, w, h, a, ad, lines):
        g.rect(x0, y0, x0 + w - 1, y0 + h - 1, a)
        for y in range(y0, y0 + h): g.put(x0 + w - 1, y, ad)
        for x in range(x0, x0 + w): g.put(x, y0 + h - 1, ad)
        for k in range(lines):
            for x in range(x0 + 1, x0 + w - 2):
                if (x + k) % 3 != 2: g.put(x, y0 + 2 + k * 2, ink)
        g.put(x0 + w // 2, y0, pr)
    note(5, 15, 7, 8, pa, pad, 2)
    note(14, 15, 6, 5, pb, pbd, 1)
    note(22, 15, 5, 9, pa, pad, 3)
    note(14, 22, 7, 5, pa, pad, 1)
    note(5, 24, 6, 4, pb, pbd, 0)
    g.outline(ol, {pa: pad, pb: pbd, pad: ol, pbd: ol})
    g.shadow(16, 37, 14, sh, 0)
    for x in range(3, 29): g.put(x, 37, sh) if g.get(x, 37) == "." else None
    return g, p

def brazier():
    p = Pal(); g = G(24, 34)
    sh = p(GRASS_SH)
    ol = p(IRON[0]); i2, i1, i0 = p("#3a3e4c", "#5c6070", "#7a7e8e")
    f1, f2, f3, f4 = p("#d8421c", "#f08428", "#ffd050", "#fff4b8")
    em = p("#8a2a1c")
    # 三本脚
    g.line(6, 33, 9, 22, i1); g.line(7, 33, 10, 22, i2)
    g.line(17, 33, 14, 22, i2); g.line(16, 33, 13, 22, i2)
    g.line(12, 33, 12, 22, i2); g.line(11, 33, 11, 22, i1)
    g.rect(7, 28, 16, 28, i2)   # 横の輪
    # 火皿
    g.ell(12, 21, 9, 4.2, lambda x, y, nx, ny: i1 if (ny > 0.25 or nx < -0.3) and nx < 0.4 else i2)
    g.ell(12, 20, 7.6, 2.6, lambda x, y, nx, ny: em if nx * nx + ny * ny > 0.4 else f1)
    # 炎
    def flame(cx, base, hgt, w, col):
        for y in range(int(base - hgt), int(base) + 1):
            t = (y - (base - hgt)) / hgt
            half = w * math.sin(math.pi * min(1, t * 0.9 + 0.1) * 0.5 + 0.0) * (0.35 + 0.65 * t)
            for x in range(int(round(cx - half)), int(round(cx + half)) + 1):
                if g.get(x, y) in (".", f1, f2, f3, em): g.put(x, y, col)
    flame(12, 20, 17, 6.5, f1)
    flame(11.5, 20, 13, 4.8, f2)
    flame(12, 20, 9, 3.0, f3)
    flame(12, 20, 5, 1.6, f4)
    g.put(8, 8, f2); g.put(17, 10, f3)
    g.put(15, 6, f2)
    g.outline(ol, {f1: em, f2: f1, f3: f2, f4: f3})
    for x in range(0, 24): pass
    g.shadow(12, 33, 9, sh, 0)
    return g, p

def shrine():
    p = Pal(); g = G(24, 34)
    ol, sd, md, lt = p(*STONE)
    sh = p(GRASS_SH)
    gl, gd = p("#e8c050", "#a8761c")
    fl1, fl2, fl3 = p("#ffd868", "#f09a30", "#fff4c0")
    dark = p("#2a2426")
    fw, fwd = p("#e8708a", "#a84060")
    # 台
    g.rect(2, 28, 21, 32, md); g.rect(2, 28, 21, 28, lt)
    for y in range(29, 33):
        for x in range(2, 22):
            if x > 13: g.put(x, y, sd)
    for x in range(2, 22): g.put(x, 32, sd)
    # 本体
    g.rect(4, 12, 19, 27, md)
    for y in range(12, 28):
        for x in range(4, 20):
            g.put(x, y, lt if x < 8 else md if x < 15 else sd)
    # 屋根（石の切妻）
    g.poly([(1, 12), (12, 4), (23, 12)], lambda x, y: lt if x < 12 else md)
    for x in range(1, 24): g.put(x, 11, md if x < 12 else sd); g.put(x, 12, sd)
    g.rect(0, 12, 23, 12, sd)
    for (x, y) in ((8, 8), (9, 8), (14, 9), (15, 9), (11, 6)): g.put(x, y, md if x < 12 else sd)
    g.put(12, 3, gd); g.put(12, 2, gl)
    # 正面の輪（灯の環：金の輪の彫り）
    cx, cy = 12, 17
    for y in range(11, 24):
        for x in range(6, 18):
            d = math.hypot(x + .5 - cx, y + .5 - cy)
    for y in range(11, 24):
        for x in range(6, 19):
            d = math.hypot(x + .5 - 12, y + .5 - 17)
            if 3.6 <= d <= 5.2: g.put(x, y, gl if (x < 12 or y < 17) else gd)
    # 灯り（輪の中の小さな炎）
    g.rect(11, 15, 12, 19, dark)
    g.rect(11, 16, 12, 18, fl2); g.put(11, 15, fl1); g.put(12, 15, fl1); g.put(11, 16, fl3); g.put(12, 17, fl1)
    # 供えの花
    g.put(6, 27, fw); g.put(7, 26, fw); g.put(7, 27, fwd); g.put(17, 27, fw); g.put(18, 27, fwd)
    g.outline(ol, {gl: gd, gd: ol})
    g.shadow(12, 33, 11, sh, 0)
    return g, p

ALL = ["cart", "laundry", "fence", "fence-end", "bench", "statue-traveler", "grave-cross", "grave-round", "noticeboard", "brazier", "shrine"]

if __name__ == "__main__":
    names = sys.argv[1:] or ALL
    for n in names:
        g, p = globals()[n.replace("-", "_")]()
        print(n, write(n, g, p))
