"""ダンジョン・遺跡の飾りの続き（壊れた樽と箱・水晶2色・光るきのこ・宝箱2種・鎖・牢の柵）。"""
import sys, math
from lib import *
from dungeon import STC, WOOD, BRONZE

def barrel_broken():
    p = Pal(); g = G(36, 26)
    ol, wk, wl, wm = p(*WOOD)
    sh = p(DUNG_SH)
    ir, ird = p("#6a6e7c", "#3a3e4c")
    dark = p("#1a1014")
    cx = 15.5
    jag = [10, 8, 12, 7, 11, 13, 9, 6, 10, 12, 8, 11, 7, 10, 12, 9, 11, 8, 12, 10, 11]   # 板ごとの折れた高さ
    for x in range(5, 26):
        top = jag[x - 5]
        for y in range(top, 23):
            half = 9.6 + 1.5 * math.sin(math.pi * min(1, max(0, (y - 5) / 18)))
            if abs(x + .5 - cx) > half: continue
            u = (x - 5) / 20
            c = wl if u < 0.3 else wk if u < 0.78 else ol
            if (x - 5) % 4 == 3: c = {wl: wk, wk: ol, ol: ol}[c]
            g.put(x, y, c)
        g.put(x, top, wm if x < 15 else wl)
    # 中の暗がり
    for x in range(10, 21):
        for y in range(11, 14): 
            if g.get(x, y) not in (".", wm): g.put(x, y, dark)
    # 鉄の帯（2本。1本はゆがんではずれかけ）
    for y0 in (15, 21):
        for x in range(5, 26):
            if g.get(x, y0) != "." and g.get(x, y0) != dark:
                g.put(x, y0, ir if x < 15 else ird); g.put(x, y0 + 1, ird) if g.get(x, y0 + 1) != "." else None
    # はずれて床に落ちた帯（輪の一部）
    for (x, y) in ((27, 22), (28, 22), (29, 22), (30, 22), (31, 22), (30, 21), (29, 21), (31, 23), (28, 23)): g.put(x, y, ir if x < 30 else ird)
    # 折れた板（ななめに床へ）
    g.line(24, 17, 31, 21, wm); g.line(24, 18, 31, 22, wl) if False else None
    g.line(25, 13, 32, 18, wm); g.line(25, 14, 32, 19, wl)
    g.line(1, 22, 6, 19, wl); g.line(1, 23, 6, 20, wk)
    g.outline(ol, {ir: ird, ird: ol, wm: ol})
    g.shadow(17, 25, 16, sh, 0)
    return g, p

def box_broken():
    p = Pal(); g = G(32, 24)
    ol, wk, wl, wm = p(*WOOD)
    sh = p(DUNG_SH)
    dark = p("#1a1014")
    ir, ird = p("#6a6e7c", "#3a3e4c")
    L, R, T, B = 4, 21, 5, 21
    # 木箱の本体（上のふちはぎざぎざに欠けている）
    tops = {}
    for x in range(L, R + 1):
        tops[x] = T + (3 if 8 <= x <= 12 else 1 if 13 <= x <= 15 else 2 if x >= 18 else 0)
    for x in range(L, R + 1):
        for y in range(tops[x], B + 1):
            c = wl if x < 15 else wk
            g.put(x, y, c)
        g.put(x, tops[x], wm if x < 15 else wl)
    # 角の柱（濃い木）
    for y in range(T, B + 1):
        for x in (L, L + 1): g.put(x, y, wm if y >= tops[x] and x == L else wl if y >= tops[x] else ".")
        for x in (R - 1, R): g.put(x, y, wk if y >= tops[x] else ".")
    # 斜めの補強板（×印）
    for i in range(0, 15):
        x = L + 3 + i; y = T + 5 + i
        for dy in (0, 1): g.put(x, y + dy, wm if x < 15 else wl)
    g.line(R - 2, T + 3, L + 2, B - 1, wk) if False else None
    # 前の板が抜け落ちた暗い穴
    for y in range(11, 17):
        for x in range(9, 16): g.put(x, y, dark)
    for (x, y) in ((9, 11), (10, 11), (9, 12), (15, 11), (14, 12), (15, 16)): g.put(x, y, wl)
    # 割れた板が箱から飛び出している
    g.line(8, tops[8], 5, 1, wm); g.line(9, tops[9], 6, 1, wl)
    g.line(19, tops[19], 24, 2, wm); g.line(20, tops[20], 25, 3, wl)
    # 角の鉄金具と釘
    for (x, y) in ((L, B), (L + 1, B), (L, B - 1), (R, B), (R - 1, B), (R, B - 1)): g.put(x, y, ir if x < 14 else ird)
    g.put(L + 3, T + 7, ir); g.put(R - 4, B - 3, ird)
    # 床に落ちた板
    g.line(23, 19, 30, 22, wl); g.line(23, 20, 30, 23, wk)
    g.line(0, 21, 4, 19, wl); g.line(0, 22, 4, 20, wk)
    g.outline(ol, {ir: ird, ird: ol})
    g.shadow(16, 23, 15, sh, 0)
    return g, p

def _crystals(c_ol, c_dp, c_md, c_lt, c_core, tint):
    p = Pal(); g = G(34, 38)
    ol = p(c_ol); dp, md, lt, core = p(c_dp, c_md, c_lt, c_core)
    sh = p(DUNG_SH)
    r1, r2, r3 = p("#3e3c52", "#5e5c74", "#7e7c94")
    rt = p(tint)
    # 土台の岩
    g.poly([(1, 36), (3, 30), (9, 27), (17, 26), (26, 27), (31, 30), (33, 36)], lambda x, y: r3 if x < 12 and y < 32 else r2 if x < 24 else r1)
    for (x, y) in ((8, 31), (9, 32), (22, 30), (26, 33), (5, 34)): g.put(x, y, r1)
    # 水晶（根元の位置、先端の位置、太さ）
    cs = [((18, 29), (18, 2), 5.0), ((11, 30), (4, 11), 4.0), ((25, 30), (30, 12), 4.0), ((7, 32), (1, 24), 3.0), ((29, 32), (33, 25), 3.0), ((14, 31), (12, 17), 3.0)]
    cs = sorted(cs, key=lambda c: (abs(c[0][0] - 18) * -1))
    for (bx, by), (tx, ty), w in cs:
        L = math.hypot(tx - bx, ty - by)
        ux, uy = (tx - bx) / L, (ty - by) / L; nx_, ny_ = -uy, ux
        # 六角柱＋尖った先（左面は地、右面は影、中央に光る芯）
        pts = [(bx - nx_ * w / 2, by - ny_ * w / 2), (bx + nx_ * w / 2, by + ny_ * w / 2)]
        tipb = 0.78
        pts += [(bx + ux * L * tipb + nx_ * w / 2, by + uy * L * tipb + ny_ * w / 2), (tx, ty), (bx + ux * L * tipb - nx_ * w / 2, by + uy * L * tipb - ny_ * w / 2)]
        def f(x, y, bx=bx, by=by, nx_=nx_, ny_=ny_, w=w, ux=ux, uy=uy):
            s = ((x + .5 - bx) * nx_ + (y + .5 - by) * ny_) / (w / 2)   # -1(左)..1(右)
            if abs(s) < 0.2: return lt
            return md if s < 0 else dp
        g.poly(pts, f)
        # 光る芯の線
        t0, t1 = 0.25, 0.8
        g.line(bx + ux * L * t0, by + uy * L * t0, bx + ux * L * t1, by + uy * L * t1, core)
        g.put(tx - ux * 2, ty - uy * 2, core)
    # 床に落ちる光の点
    for (x, y) in ((4, 36), (30, 36), (17, 36), (11, 35), (24, 35)): g.put(x, y, rt)
    g.outline(ol, {r1: ol, r2: ol, r3: ol})
    g.shadow(17, 37, 16, sh, 0)
    return g, p

def crystal_blue(): return _crystals("#10224a", "#2a56a8", "#4a8cf0", "#8cc8ff", "#e4f6ff", "#3a6cc0")
def crystal_red(): return _crystals("#3a0c1c", "#8a1e3c", "#e0405a", "#ff909c", "#ffe8e4", "#b03050")

def mushrooms():
    p = Pal(); g = G(32, 26)
    ol = p("#0c2a34")
    c1, c2, c3 = p("#3ee0c4", "#22a0a4", "#146070")
    sp = p("#d4fff0")
    st1, st2 = p("#d8e8d4", "#9cb4a8")
    d1, d2 = p("#3a3446", "#26222e")
    m1, m2 = p("#4a8a58", "#2e5a3c")
    sh = p(DUNG_SH)
    # 根元の土と苔
    g.ell(16, 23, 14, 3, lambda x, y, nx, ny: d1 if nx < 0.2 else d2)
    for (x, y) in ((4, 22), (5, 21), (6, 22), (26, 22), (27, 21), (10, 23), (22, 23)): g.put(x, y, m1)
    for (x, y) in ((5, 22), (27, 22)): g.put(x, y, m2)
    def shroom(cx, base, h, rx, ry, lean=0.0):
        # 柄
        for y in range(int(base - h), int(base) + 1):
            t = (base - y) / h
            x0 = cx + lean * t * 4
            for x in range(int(x0 - 1.4), int(x0 + 1.6)):
                g.put(x, y, st1 if x < x0 else st2)
        # 笠（丸い。左が地、右が影。下のふち＝ひだは暗い）
        capx, capy = cx + lean * 4, base - h
        def f(x, y, nx, ny):
            if ny > 0.55: return c3
            return c1 if (nx * 0.8 + ny * 0.7) < 0.2 else c2 if (nx * 0.8 + ny * 0.7) < 0.75 else c3
        g.ell(capx, capy, rx, ry, f)
        for (dx, dy) in ((-0.45, -0.35), (0.25, -0.55), (0.1, 0.0), (-0.1, -0.1)):
            if abs(dx) < 0.5 and hn(int(cx * 3), int(h), 5) % 2 == 0 or True:
                g.put(capx + dx * rx, capy + dy * ry, sp)
        g.put(capx - rx * 0.55, capy - ry * 0.1, sp)
    shroom(9, 22, 11, 6.5, 4.6, -0.2)
    shroom(21, 22, 15, 7.5, 5.4, 0.15)
    shroom(15, 22, 7, 4.6, 3.4, 0.0)
    shroom(27, 22, 7, 3.6, 2.8, 0.1)
    shroom(3, 22, 5, 3.2, 2.5, -0.1)
    g.outline(ol, {c1: ol, c2: ol, c3: ol, st1: ol, st2: ol})
    g.shadow(16, 25, 14, sh, 0)
    return g, p

def _chest(open_):
    p = Pal(); h = 30 if open_ else 22
    g = G(26, h)
    ol, wk, wl, wm = p(*WOOD)
    br1, br2, br0 = p("#e8c050", "#a8761c", "#7a5210")   # 金具（金）
    ir = p("#5c6070")
    dark = p("#1a1014")
    cn1, cn2 = p("#ffe070", "#e0a830")
    sh = p(DUNG_SH)
    bot = h - 2
    # 箱の本体（前面）
    top = bot - 11
    g.rect(2, top, 23, bot, wl)
    for y in range(top, bot + 1):
        for x in range(2, 24):
            c = wl if x < 15 else wk
            if y in (top + 5,): c = wk
            g.put(x, y, c)
    for x in range(2, 24): g.put(x, bot, wk)
    # 金具の帯（左右）と下の角
    for x0 in (4, 19):
        g.rect(x0, top, x0 + 2, bot, br1); g.rect(x0 + 2, top, x0 + 2, bot, br2)
    g.rect(2, top, 23, top, br1)
    g.rect(2, bot - 1, 4, bot, br2); g.rect(21, bot - 1, 23, bot, br2)
    if not open_:
        # ふた（まるい屋根形）：上は明るく、正面はやや暗い
        lid_top = top - 9
        def lf(x, y, nx, ny):
            return wm if (ny < -0.1 and nx < 0.5) else wl if ny < 0.35 else wk
        g.ell(13, top + 1, 11.5, 9.5, lambda x, y, nx, ny: lf(x, y, nx, ny) if y < top else None)
        for x0 in (4, 19):
            for y in range(lid_top + 1, top):
                if g.get(x0 + 1, y) != ".": g.put(x0, y, br1); g.put(x0 + 1, y, br1); g.put(x0 + 2, y, br2)
        g.rect(2, top - 1, 23, top - 1, wk) if False else None
        # 錠前
        g.rect(11, top - 1, 14, top + 4, br2); g.rect(11, top - 1, 13, top + 3, br1)
        g.put(12, top + 1, dark); g.put(12, top + 2, dark)
    else:
        # ふたは後ろへ開いている（裏の板が見える）
        g.rect(3, 1, 22, top - 3, wk)
        for y in range(1, top - 2):
            for x in range(3, 23):
                g.put(x, y, wl if x < 12 else wk)
        g.rect(3, 1, 22, 2, wm)
        for x0 in (4, 19):
            g.rect(x0, 1, x0 + 2, top - 3, br1); g.rect(x0 + 2, 1, x0 + 2, top - 3, br2)
        # 中の暗がりと金貨の山
        g.rect(3, top - 2, 22, top + 1, dark)
        for y in range(top - 3, top + 1):
            for x in range(4, 22):
                half = 9 - abs(y - (top - 1)) * 2.0
                if abs(x - 13) < half: g.put(x, y, cn1 if (x + y) % 3 == 0 else cn2 if (x * 2 + y) % 5 else br2)
        for (x, y) in ((10, top - 4), (14, top - 4), (12, top - 5), (17, top - 3), (8, top - 2)): g.put(x, y, cn1)
        g.rect(2, top - 1, 4, top - 1, wm) if False else None
    g.outline(ol, {br1: br0, br2: br0, br0: ol, cn1: br2, cn2: br2})
    g.shadow(13, h - 1, 12, sh, 0)
    return g, p

def chest_closed(): return _chest(False)
def chest_open(): return _chest(True)

def chains():
    p = Pal(); g = G(22, 44)
    ol = p("#14161c"); i1, i2, i3 = p("#8a8f9e", "#555a6a", "#353848")
    ru = p("#8a5a34")
    # 天井の金具
    g.rect(2, 0, 19, 2, i2); g.rect(2, 0, 19, 0, i1); g.rect(14, 1, 19, 2, i3)
    g.rect(5, 3, 6, 4, i2); g.rect(14, 3, 15, 4, i2)
    def chain(x, y0, y1, ring_first):
        y = y0; k = 0
        while y < y1:
            if (k + ring_first) % 2 == 0:
                # 正面を向いた輪（中が抜けている）
                g.rect(x - 2, y, x + 1, y + 4, i1)
                g.rect(x - 1, y + 1, x, y + 3, ".")
                for yy in range(y, y + 5): g.put(x + 1, yy, i3 if yy % 2 else i2)
                g.put(x - 2, y, i1); g.put(x + 1, y + 4, i3)
                y += 3
            else:
                # 横向きの輪（細長い）
                g.rect(x - 1, y, x, y + 3, i2)
                g.put(x, y + 1, i3); g.put(x, y + 2, i3)
                y += 3
            k += 1
        return y
    ye = chain(6, 4, 28, 0)
    ye2 = chain(15, 4, 21, 1)
    # 手かせ（開いた輪）
    def cuff(cx, y):
        g.ell(cx, y + 4, 4.4, 4.2, lambda x, yy, nx, ny: (i1 if nx < 0 else i2) if (nx * nx + ny * ny > 0.4) else None)
        g.rect(cx - 5, y + 2, cx - 4, y + 3, i3) if False else None
        g.put(cx + 3, y + 6, ".") ; g.put(cx + 4, y + 5, ".")
        g.put(cx - 1, y, i2); g.put(cx, y, i2)
        g.put(cx + 2, y + 4, ru); g.put(cx - 3, y + 6, ru)
    cuff(6, ye - 1)
    cuff(15, ye2 - 1)
    g.outline(ol, {})
    return g, p

def jail_bars():
    p = Pal(); g = G(34, 50)
    ol, sd, md, lt = p(*STC)
    sh = p(DUNG_SH)
    i1, i2, i3 = p("#8a8f9e", "#555a6a", "#353848")
    ru = p("#8a5a34"); rud = p("#5a3a22")
    gd1, gd2 = p("#e8c050", "#a8761c")
    mo, mod = p("#4a7a48", "#2e5034")
    # 床の石の台
    g.rect(0, 43, 33, 46, md)
    for x in range(0, 34): g.put(x, 43, lt if x < 24 else md); g.put(x, 46, sd)
    for y in range(44, 47):
        for x in range(25, 34): g.put(x, y, sd)
    for x in (8, 16, 24): g.rect(x, 44, x, 45, sd)
    # 左右の石の柱
    for (x0, x1) in ((0, 4), (29, 33)):
        for y in range(4, 43):
            for x in range(x0, x1 + 1):
                u = (x - x0) / (x1 - x0)
                g.put(x, y, lt if u < 0.3 else md if u < 0.7 else sd)
        for y in range(8, 42, 7): g.rect(x0, y, x1, y, sd)
    # 上の石の梁（まぐさ）
    g.rect(0, 0, 33, 4, md)
    for x in range(0, 34): g.put(x, 0, lt if x < 24 else md); g.put(x, 4, sd); g.put(x, 3, sd if x > 22 else md)
    for x in (10, 21): g.rect(x, 1, x, 3, sd)
    # 鉄格子（細い棒。左が明るく右が暗い。間は透ける）
    for x in range(7, 28, 5):
        for y in range(5, 43):
            g.put(x, y, i1); g.put(x + 1, y, i3 if y % 9 else i2)
        # 棒の頭
        g.put(x, 5, i2); g.put(x + 1, 5, i3)
    # 横の鉄（上下の2本）。さびを少し
    for y0 in (12, 36):
        for x in range(4, 30):
            g.put(x, y0, i2); g.put(x, y0 + 1, i3)
        for x in range(4, 30):
            if hn(x, y0, 2) % 7 == 0: g.put(x, y0, ru)
    # 扉の継ぎ目（中の2本のあいだ）と錠前
    g.rect(14, 22, 19, 27, gd2); g.rect(14, 22, 18, 26, gd1)
    g.rect(15, 20, 15, 21, i2); g.rect(18, 20, 18, 21, i2); g.rect(15, 19, 18, 19, i2)
    g.put(16, 24, ol); g.put(16, 25, ol)
    # さびの汚れ・苔
    for (x, y) in ((8, 20), (8, 21), (13, 30), (13, 31), (23, 15), (23, 16), (28, 28)): g.put(x, y, ru)
    for (x, y) in ((1, 42), (2, 41), (2, 42), (3, 42), (31, 42), (30, 41), (31, 41)): g.put(x, y, mo)
    g.put(2, 42, mod); g.put(31, 42, mod)
    g.outline(ol, {i1: ol, i2: ol, i3: ol, mo: mod, mod: ol, gd1: gd2, gd2: ol})
    g.shadow(17, 49, 16, sh, 0)
    return g, p

ALL = ["barrel-broken", "box-broken", "crystal-blue", "crystal-red", "mushrooms", "chest-closed", "chest-open", "chains", "jail-bars"]

if __name__ == "__main__":
    names = sys.argv[1:] or ALL
    for n in names:
        g, p = globals()[n.replace("-", "_")]()
        print(n, write(n, g, p))
