"""特技・呪文の種類の印（16x16）。系統ごとの色と形で、字が読めなくても何の技か分かるようにする。

どれも既存作品の呪文アイコンの形は真似しない（炎=炎の形、水=しずく、など自然物の形だけを使う）。
"""
import math

from common import Canvas, icon, from_rows


@icon('skill', 'fire', '炎|火照系の攻撃呪文・火の技。炎の形（赤〜橙〜黄の3段）')
def _():
    return from_rows([
        "................",
        "........R.......",
        ".......RR.......",
        ".......RRR..R...",
        "......RRRR..RR..",
        ".....RRRRRR.RRQ.",
        ".....RRROORRRRQ.",
        "....RRROOOORRQQ.",
        "....RRROOOOORQQ.",
        "...RRROOYYOOOQQ.",
        "...RRROYYYYOOQQ.",
        "...RRROYYYYOOQQ.",
        "...RRQOOYYOOQQ..",
        "....RQQOOOOQQ...",
        ".....QQQQQQQ....",
        "................"])


@icon('skill', 'water', '水|水紋系の呪文・水の技。しずくの形（青の3段）')
def _():
    return from_rows([
        "................",
        ".......B........",
        "......BB........",
        "......BBC.......",
        ".....BBBCC......",
        ".....BBBCCC.....",
        "....BBBBCCC.....",
        "....BBBBCCCC....",
        "...BBBBBCCCC....",
        "...BBBBCCCCCc...",
        "...BBBBCCCCCc...",
        "...BBBCCCCCCc...",
        "....BBCCCCCcc...",
        ".....BCCCCcc....",
        "......cccc......",
        "................"])


@icon('skill', 'wind', '風|風唱系の呪文・風の技。ぐるりと巻く風の渦（水色の3段）')
def _():
    c = Canvas()
    pts = []
    for i in range(0, 80):
        th = i * 0.12
        r = 0.6 + th * 0.55
        x = 7.5 + r * math.cos(th + 2.7)
        y = 7.0 + r * math.sin(th + 2.7)
        pts.append((round(x), round(y)))
    for (x, y) in pts:
        if 1 <= x <= 13 and 1 <= y <= 13:
            t = (x + y - 14) / 10
            k = 'I' if t < -0.2 else ('C' if t > 0.3 else 'B')
            c.px(x, y, k)
    # すそへ流れる尾
    c.line(9, 14, 13, 14, 'C')
    c.line(2, 13, 6, 13, 'B')
    c.pts('C', (13, 13), (14, 12))
    return c


@icon('skill', 'earth', '土|地固系の呪文・土の技。地面から突き出る岩のとげ')
def _():
    return from_rows([
        "................",
        "................",
        ".......M........",
        ".......MN.......",
        "....M..MN..M....",
        "....MN.MND.MN...",
        "....MN.MND.MND..",
        "...MMNNMNDDMND..",
        "...MMNNMNDDNND..",
        "..MMNNNNNDDNDD..",
        "..WWWWWWWWWWWw..",
        ".WWWWWWWwwwwwww.",
        ".WWWWwwwwwwwwxx.",
        "..wwwwwwwwwxxx..",
        "...xxxxxxxxxx...",
        "................"])


@icon('skill', 'light', '光|光断系の呪文・聖なる技。光を放つ太陽（金の3段）')
def _():
    c = Canvas()
    for (x0, y0, x1, y1) in ((8, 1, 8, 4), (8, 11, 8, 14), (1, 8, 4, 8), (11, 8, 14, 8)):
        c.line(x0, y0, x1, y1, 'G')
        c.line(x0 + 1, y0, x1 + 1, y1, 'H') if x0 == x1 else c.line(x0, y0 + 1, x1, y1 + 1, 'H')
    for (x0, y0, x1, y1) in ((3, 3, 4, 4), (12, 3, 11, 4), (3, 12, 4, 11), (12, 12, 11, 11)):
        c.line(x0, y0, x1, y1, 'G')
    c.sphere(8, 8, 3.6, 3.6, ('Y', 'G', 'H'))
    c.pts('H', (9, 1), (9, 2), (9, 3), (9, 4), (9, 11), (9, 12), (9, 13), (9, 14))
    return c


@icon('skill', 'dark', '闇|闇の呪文・呪い・悪神の技。もやをまとった黒い玉（紫の3段）')
def _():
    c = Canvas()
    for k in range(8):
        a = math.radians(k * 45 + 22.5)
        x0, y0 = 8 + 5.2 * math.cos(a), 8 + 5.2 * math.sin(a)
        x1, y1 = 8 + 7.2 * math.cos(a), 8 + 7.2 * math.sin(a)
        c.line(round(x0 - 0.5), round(y0 - 0.5), round(x1 - 0.5), round(y1 - 0.5), 'U')
    c.sphere(8, 8, 5.6, 5.6, ('U', 'u', 'A'))
    c.ell(8.7, 8.7, 3.6, 3.6, 'A')
    c.sphere(8, 8, 3.4, 3.4, ('u', 'A', 'A'))
    c.pts('V', (4, 6), (5, 5))
    return c


@icon('skill', 'heal', '回復|水紋系の回復呪文・癒しの技。四つ葉（緑の3段）')
def _():
    c = Canvas()
    for (cx, cy) in ((5.4, 5.4), (10.6, 5.4), (5.4, 10.6), (10.6, 10.6)):
        c.sphere(cx, cy, 3.1, 3.1, ('L', 'l', 'd'))
    c.rect(7, 6, 8, 9, 'l')
    c.rect(6, 7, 9, 8, 'l')
    c.pts('d', (7, 7), (8, 8), (7, 8), (8, 7))
    c.pts('L', (6, 6), (9, 6))
    return c


@icon('skill', 'buff', '強化|味方の能力を上げる技。上向きの矢（橙の3段）')
def _():
    c = Canvas()
    c.poly([(8, 1), (14, 8), (10.2, 8), (10.2, 14), (5.8, 14), (5.8, 8), (2, 8)], 'T')
    c.poly([(8, 1), (8, 14), (5.8, 14), (5.8, 8), (2, 8)], 'O')
    c.poly([(10.2, 8), (10.2, 14), (8, 14), (8, 8)], 'T')
    c.rect(9, 9, 9, 13, 'Q')
    c.pts('Q', (10, 8), (11, 8), (12, 8), (13, 8))
    c.pts('Y', (6, 9), (6, 10), (6, 11))
    return c


@icon('skill', 'debuff', '弱体|敵の能力を下げる技。下向きの矢（紫の3段）')
def _():
    c = Canvas()
    c.poly([(8, 14.5), (14, 7.5), (10.2, 7.5), (10.2, 1.5), (5.8, 1.5), (5.8, 7.5), (2, 7.5)], 'U')
    for y in range(16):
        for x in range(8):
            if c.g[y][x] == 'U':
                c.g[y][x] = 'V'
    for y in range(16):
        for x in range(16):
            if c.g[y][x] == 'U' and (x >= 10 or y >= 11):
                c.g[y][x] = 'u'
    c.pts('u', (9, 8), (9, 9), (9, 10))
    return c


@icon('skill', 'sleep', '眠り|敵を眠らせる技（風唱の眠り唄など）。大小のZ（青の3段）')
def _():
    c = Canvas()
    # 大きなZ
    c.rect(1, 2, 8, 3, 'B')
    c.line(8, 4, 2, 8, 'C')
    c.line(8, 5, 3, 8, 'C')
    c.rect(1, 9, 8, 10, 'B')
    c.rect(4, 9, 8, 10, 'C')
    c.pts('c', (8, 3), (8, 10), (7, 10), (6, 10))
    # 小さなz
    c.rect(9, 8, 13, 8, 'B')
    c.line(13, 9, 9, 12, 'C')
    c.rect(9, 13, 13, 13, 'C')
    c.pts('c', (13, 13), (12, 13))
    return c


@icon('skill', 'poison', '毒|毒の技・毒状態。どくろと、したたる緑のしずく')
def _():
    return from_rows([
        "................",
        "................",
        "....FFFFFF......",
        "...FFFFFFFF.....",
        "..FFFFFFFFFf....",
        "..FAAFFFAAFf....",
        "..FAAFFFAAFf....",
        "..FFFFAFFFFf....",
        "...FFFFFFFf.....",
        "....FfFfFf......",
        "....FfFfFf......",
        "....L..L..L.....",
        "....L..l..l.....",
        "....d..d........",
        "................",
        "................"])


@icon('skill', 'all', '全体攻撃|敵全体に当たる技（波・雨矢・大地の怒りなど）。とげのある爆発')
def _():
    c = Canvas()
    pts = []
    for i in range(16):
        r = 7.0 if i % 2 == 0 else 3.8
        a = math.radians(-90 + i * 22.5)
        pts.append((8 + r * math.cos(a), 8 + r * math.sin(a)))
    c.poly(pts, 'R')
    for y in range(16):
        for x in range(16):
            if c.g[y][x] == 'R' and (x + y) > 17:
                c.g[y][x] = 'Q'
    pts2 = []
    for i in range(16):
        r = 4.6 if i % 2 == 0 else 2.6
        a = math.radians(-90 + i * 22.5)
        pts2.append((8 + r * math.cos(a), 8 + r * math.sin(a)))
    c.poly(pts2, 'O')
    c.ell(8, 8, 2.0, 2.0, 'Y')
    return c


@icon('skill', 'slash', '斬る|物理の斬撃（剣・刃の技）。振りぬいた刃の三日月')
def _():
    c = Canvas()
    for y in range(16):
        for x in range(16):
            a = math.hypot(x + 0.5 - 8.0, y + 0.5 - 8.5)
            b = math.hypot(x + 0.5 - 11.5, y + 0.5 - 5.0)
            if a <= 6.6 and b >= 6.0:
                c.px(x, y, 'S' if b > 8.2 else ('s' if b > 7.0 else 'z'))
    c.omap['z'] = 'k'
    return c


@icon('skill', 'pierce', '突く|物理の刺突（槍・矢の技）。鋭いとげと、走る線')
def _():
    c = Canvas()
    c.line(5, 10, 14, 1, 'S')
    c.line(6, 10, 14, 2, 's')
    c.line(5, 9, 13, 1, 'S')
    c.line(7, 10, 14, 3, 'z')
    c.line(5, 11, 8, 11, 'z')
    c.pts('s', (6, 10), (6, 11), (7, 11))
    c.line(1, 8, 4, 5, 'I')
    c.line(1, 11, 3, 9, 'I')
    c.line(2, 14, 6, 14, 'I')
    c.line(4, 13, 8, 13, 'B')
    c.omap['I'] = 'b'
    return c


@icon('skill', 'guard', '守り|物理の防御・かばう・守りの構え。木の丸盾に鉄のふち')
def _():
    c = Canvas()
    c.sphere(8, 8, 6.9, 6.9, ('S', 's', 'z'))
    for y in range(16):
        for x in range(16):
            u, v = (x + 0.5 - 8) / 5.0, (y + 0.5 - 8) / 5.0
            if u * u + v * v <= 1.0:
                t = (u + v) / 2
                c.px(x, y, 'W' if t < -0.3 else ('x' if t > 0.4 else 'w'))
    for x in (6, 10):
        for y in range(4, 13):
            if c.g[y][x] in 'Wwx':
                c.px(x, y, 'x' if c.g[y][x] != 'x' else 'x')
    c.sphere(8, 8, 2.0, 2.0, ('S', 's', 'z'))
    return c
