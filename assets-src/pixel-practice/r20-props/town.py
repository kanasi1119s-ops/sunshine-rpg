"""町の飾り（噴水・屋台・干し草・荷車・洗濯物・柵・ベンチ・旅人像・墓石・立て札・かがり火台・灯りの祠）を一から作る。
使い方: python3 town.py [名前 ...]  → <名前>.txt と pal-<名前>.json"""
import sys, math
from lib import *

# ---- 共通の色（素材ごと。影＝地より少し暗く彩度を上げる）----
WOOD = ("#2a1a10", "#5a3a20", "#7a5230", "#9a6c40")        # 縁, 影, 地, 上面
STONE = ("#2a2624", "#585450", "#7e7a72", "#a4a094")       # 縁, 影, 地, 明るい面（上面）
IRON = ("#1a1c24", "#3a3e4c", "#5c6070")

def fountain():
    p = Pal(); g = G(48, 48)
    ol, sd, md, lt = p(*STONE)
    deep = p("#403c38")
    wa, wd, sp = p("#4a8ab8", "#2a5078", "#bfe4f2")
    sh = p(GRASS_SH)
    # 水盤の側面（円柱）
    def wall(x, y, nx, ny):
        c = lt if nx < -0.35 else md if nx < 0.35 else sd
        if (y % 5 == 0 and y > 36) or ((x + (y // 5) * 4) % 9 == 0 and y > 36): c = {lt: md, md: sd, sd: deep}[c]
        return c
    g.ell(24, 39, 22, 8, wall)
    # 縁の上面（輪）と水面
    g.ell(24, 36, 22, 9, lambda x, y, nx, ny: lt if nx < 0.3 else md)
    for x in range(2, 47):
        pass
    g.ell(24, 36.5, 18.5, 6.4, lambda x, y, nx, ny: wd if (nx * nx + ny * ny > 0.62 and (nx + ny) > -0.2) else wa)
    # 水面の波紋（暗い水の線）
    for (x, y) in ((12, 37), (13, 37), (31, 39), (32, 39), (33, 39), (18, 40), (19, 40)): g.put(x, y, wd)
    # 中央の柱と上の小皿
    g.rect(21, 20, 26, 35, md)
    for y in range(20, 36): g.put(21, y, lt); g.put(22, y, lt); g.put(25, y, sd); g.put(26, y, sd)
    g.ell(24, 33.5, 5, 2, lambda x, y, nx, ny: md)
    g.ell(24, 19, 8, 3, lambda x, y, nx, ny: lt if nx < 0.2 else md)
    g.ell(24, 18.6, 6, 1.7, lambda x, y, nx, ny: wa if nx < 0.3 else wd)
    # 噴き上がる水（中央＋弧）
    for y in range(4, 18): g.put(23, y, sp if y < 12 else wa); g.put(24, y, wa if y < 12 else wd)
    for y in range(2, 5): g.put(23, y, sp); g.put(24, y, sp)
    for dirn in (-1, 1):
        for reach, top, k in ((15, 5, 0), (10, 8, 1), (6, 3, 2)):
            for i in range(0, 26):
                t = i / 25
                x = 24 + dirn * (reach * t) + (0 if dirn < 0 else 0)
                y = top + (35 - top) * t * t if reach > 9 else top + (19 - top) * t * t * 1.0
                if reach > 9 and y > 34: break
                if reach <= 9 and y > 17: break
                g.put(round(x), round(y), sp if (i % 3 == 0) else wa)
    # 水盤に落ちる水しぶき
    for (x, y) in ((8, 35), (9, 34), (39, 35), (40, 34), (15, 37), (33, 38), (24, 22)): g.put(x, y, sp)
    g.outline(ol, {wa: wd, wd: wd, sp: wd})
    g.shadow(24, 46, 22, sh, 1)
    return g, p

def stall():
    p = Pal(); g = G(48, 48)
    ol, wk, wl, wm = p(*WOOD)
    sh = p(GRASS_SH)
    re, rd, rdd = p("#c84a42", "#963032", "#6a1e28")
    cr, crd = p("#f0e4c4", "#c8b48c")
    inside = p("#2e2230")
    # 日よけ（斜めの屋根）：縞は赤とクリーム
    for y in range(4, 17):
        t = (y - 4) / 12
        x0, x1 = int(9 - t * 6), int(38 + t * 6)
        for x in range(x0, x1 + 1):
            stripe = ((x - 3) // 6) % 2 == 0
            if stripe: c = re if x < 24 else rd
            else: c = cr if x < 24 else crd
            if y >= 15: c = {re: rd, rd: rdd, cr: crd, crd: crd}[c]
            g.put(x, y, c)
    # ふちのひらひら（半円の垂れ）
    for k in range(7):
        x0 = 3 + k * 6
        stripe = (k % 2 == 0)
        for dy, w in ((17, 6), (18, 4), (19, 2)):
            for x in range(x0 + (6 - w) // 2, x0 + (6 + w) // 2):
                if stripe: c = rd if x < 24 else rdd
                else: c = crd
                g.put(x, dy, c)
    # 柱
    for y in range(20, 42):
        g.rect(5, y, 6, y, wl); g.put(6, y, wk)
        g.rect(41, y, 42, y, wl); g.put(42, y, wk)
    # 日よけの下の暗がり
    g.rect(7, 20, 40, 29, inside)
    # 吊るした干しぶどう風の束（暗がりの中のアクセント）
    for x in (12, 20, 28, 35):
        g.put(x, 20, wm); g.put(x, 21, wl); g.put(x, 22, re); g.put(x, 23, rd)
    # 台（正面）と天板
    g.rect(5, 31, 42, 41, wl)
    g.rect(5, 29, 42, 30, wm)
    for y in range(31, 42):
        for x in range(5, 43):
            if x > 30: g.put(x, y, wk)
            if y in (35, 38) : g.put(x, y, wk if x <= 30 else wk)
    for x in range(5, 43): g.put(x, 30, wl if x > 20 else wm); g.put(x, 41, wk)
    for x in (13, 22, 31, 39): g.rect(x, 32, x, 40, wk)
    # 台の上：果物の籠と麻袋
    ba, bd = wm, wl
    fr1, fr1d = p("#e8503c", "#a8302c")
    fr2, fr2d = p("#f0a030", "#b8701c")
    fr3, fr3d = p("#f0a030", "#b8701c")
    fr3, fr3d = fr2, fr2d
    def basket(cx, f1, f1d, f2, f2d):
        g.ell(cx, 26.5, 6.5, 3.2, lambda x, y, nx, ny: ba if nx < 0.2 else bd)
        for (dx, dy, f, fd) in ((-3, -1, f1, f1d), (0, -2, f2, f2d), (3, -1, f1, f1d), (-1, 0, f2, f2d), (2, 0, f1, f1d)):
            g.ell(cx + dx, 24 + dy + 1, 2.1, 2.1, lambda x, y, nx, ny, f=f, fd=fd: f if (nx + ny) < 0.5 else fd)
        for x in range(int(cx - 5), int(cx + 6)):
            if (x + 1) % 2 == 0: g.put(x, 27, bd)
    basket(14, fr1, fr1d, fr2, fr2d)
    basket(30, fr2, fr2d, fr1, fr1d)
    # 袋
    sk, skd = cr, crd
    g.ell(38, 26, 3.8, 3.6, lambda x, y, nx, ny: sk if nx < 0.2 else skd)
    g.rect(37, 21, 38, 22, skd)
    g.outline(ol, {re: rdd, rd: rdd, rdd: rdd, cr: crd, crd: rdd, ba: wk, bd: ol})
    g.shadow(24, 45, 21, sh, 0)
    return g, p

def haystack():
    p = Pal(); g = G(32, 28)
    ol = p("#4a3418"); dp, sdw, base = p("#8a6428", "#b48a34", "#d8b44c")
    sh = p(GRASS_SH)
    wk, wl = p("#5a3a20", "#7a5230"); ir = p("#8a8f9a"); irs = p("#505560")
    def f(x, y, nx, ny):
        c = base if (nx * 0.9 + ny * 0.5) < 0.0 else sdw if (nx * 0.9 + ny * 0.5) < 0.45 else dp
        return c
    g.ell(16, 21, 14, 7, f)
    g.poly([(3, 21), (6, 12), (11, 6), (16, 3), (21, 6), (26, 12), (29, 21)], lambda x, y: f(x, y, (x - 16) / 13, (y - 14) / 11))
    # 藁のすじ（短い線）
    for y in range(5, 25):
        for x in range(3, 30):
            if g.get(x, y) in (base, sdw, dp) and hn(x, y, 3) % 7 == 0:
                c = g.get(x, y)
                g.put(x, y, {base: sdw, sdw: dp, dp: dp}[c]); g.put(x + 1, y + 1, {base: sdw, sdw: dp, dp: dp}[c])
    for (x, y) in ((16, 2), (17, 1), (15, 3), (19, 4), (13, 4), (21, 5)): g.put(x, y, base if x < 17 else sdw)
    g.rect(2, 22, 29, 23, dp)
    g.outline(ol)
    # 縄の帯と、地面にこぼれた藁
    for x in range(5, 28):
        if g.get(x, 16) in (base, sdw, dp): g.put(x, 16, dp if x % 2 else ol)
    for (x, y) in ((1, 24), (2, 24), (3, 25), (29, 24), (30, 24), (28, 25)): g.put(x, y, sdw)
    g.outline(ol)
    g.shadow(16, 26, 14, sh, 1)
    return g, p

PEOPLE = None

def make(names):
    import importlib
    out = {}
    for n in names:
        fn = globals()[n.replace("-", "_")]
        g, p = fn()
        out[n] = write(n, g, p)
    return out

ALL = ["fountain", "stall", "haystack"]

if __name__ == "__main__":
    names = sys.argv[1:] or ALL
    print(make(names))
