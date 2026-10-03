"""消耗品・どうぐ・灯貨のアイコン（16x16）。"""
import math

from common import Canvas, icon


def bottle(c, cx, cy, rx, ry, liquid, neck_top, neck_w=2, cork=True, glass='I'):
    """丸底の薬びん。cx,cy=胴の中心、neck_top=首の上端の行"""
    c.sphere(cx, cy, rx, ry, liquid)
    x0 = int(cx - neck_w / 2 + 0.5)
    body_top = int(cy - ry + 1)
    for y in range(neck_top, body_top + 1):
        for x in range(x0, x0 + neck_w):
            c.px(x, y, glass)
    # 首の影側
    if cork:
        c.rect(x0, neck_top - 2, x0 + neck_w - 1, neck_top - 1, 'W')
        c.rect(x0 + neck_w - 1, neck_top - 2, x0 + neck_w - 1, neck_top - 1, 'w')
    return x0


RED = ('R', 'Q', 'q')
BLUE = ('B', 'C', 'c')
GREEN = ('L', 'l', 'd')


@icon('item', 'potion-s', '回復薬(小)|HPを少し回復するどうぐ。小さな丸びん・赤')
def _():
    c = Canvas()
    bottle(c, 8, 11.2, 3.3, 3.2, RED, 6)
    c.omap['I'] = 'b'
    c.omap['W'] = 'n'
    c.omap['w'] = 'n'
    return c


@icon('item', 'potion-m', '回復薬(中)|HPをかなり回復するどうぐ。ふつうの丸びん・赤')
def _():
    c = Canvas()
    bottle(c, 8, 10.4, 4.4, 4.2, RED, 4)
    c.omap['I'] = 'b'
    c.omap['W'] = 'n'
    c.omap['w'] = 'n'
    return c


@icon('item', 'potion-l', '回復薬(大)|HPを大きく回復するどうぐ。大びん・赤。首に金の帯')
def _():
    c = Canvas()
    bottle(c, 8, 10.2, 5.2, 4.8, RED, 4, neck_w=3)
    c.rect(6, 5, 8, 5, 'W')
    c.rect(8, 5, 8, 5, 'w')
    c.omap['I'] = 'b'
    c.omap['W'] = 'n'
    c.omap['w'] = 'n'
    return c


@icon('item', 'potion-mp', '魔力の薬|MPを回復するどうぐ。青い液体のびん')
def _():
    c = Canvas()
    bottle(c, 8, 10.4, 4.4, 4.2, BLUE, 4)
    c.omap['I'] = 'b'
    c.omap['W'] = 'n'
    c.omap['w'] = 'n'
    c.replace('W', 'w')
    c.px(7, 2, 'W')
    c.px(7, 3, 'W')
    return c


@icon('item', 'antidote', '毒消し|毒を治すどうぐ。緑の液体のびんに、白いラベル')
def _():
    c = Canvas()
    bottle(c, 8, 10.4, 4.4, 4.2, GREEN, 4)
    c.rect(7, 9, 9, 11, 'I')
    c.pts('d', (8, 10))
    c.omap['I'] = 'b'
    c.omap['W'] = 'n'
    c.omap['w'] = 'n'
    return c


@icon('item', 'revive', '復活の薬|戦闘不能の仲間を起こすどうぐ。金色の液体と白い羽根')
def _():
    c = Canvas()
    bottle(c, 8, 11.2, 3.9, 3.7, ('Y', 'G', 'H'), 6, cork=False)
    c.omap['I'] = 'b'
    c.omap['W'] = 'n'
    c.omap['Y'] = 'y'
    c.omap['G'] = 'y'
    c.omap['H'] = 'y'
    c.rect(7, 4, 8, 5, 'W')
    # 羽根
    c.line(8, 3, 12, 0 + 1, 'F')
    c.line(7, 3, 10, 1, 'F')
    c.pts('F', (11, 2), (10, 2), (9, 2), (8, 2), (7, 2), (10, 1), (9, 1), (11, 1), (9, 3), (10, 3))
    c.omap['F'] = 'n'
    return c


@icon('item', 'herb', '薬草|HPを少し回復する草。やくそうの束')
def _():
    c = Canvas()
    c.line(8, 14, 8, 8, 'd')
    c.line(7, 14, 7, 12, 'd')
    c.poly([(8, 1.5), (10.8, 5), (8.4, 9), (5.6, 5)], 'l')
    c.poly([(8, 1.5), (8.4, 9), (5.6, 5)], 'L')
    c.poly([(2, 5), (6.8, 7.5), (7.4, 11), (2.8, 9.8)], 'l')
    c.poly([(2, 5), (6.8, 7.5), (5.5, 9.6), (2.8, 9.8)], 'L')
    c.poly([(14, 5), (9.2, 7.5), (8.6, 11), (13.2, 9.8)], 'd')
    c.poly([(14, 5), (9.2, 7.5), (10.5, 9.6), (13.2, 9.8)], 'l')
    c.line(8, 3, 8, 8, 'd')
    c.rect(6, 12, 9, 13, 'w')
    c.rect(6, 12, 9, 12, 'W')
    return c


@icon('item', 'light-stone', '灯り石|暗い所を照らす石。金色に光る結晶（ダンジョンの道具）')
def _():
    c = Canvas()
    c.poly([(8, 1.5), (12.8, 4.8), (12.8, 10.2), (8, 14.5), (3.2, 10.2), (3.2, 4.8)], 'G')
    c.poly([(8, 1.5), (8, 14.5), (3.2, 10.2), (3.2, 4.8)], 'Y')
    c.poly([(8, 8), (12.8, 10.2), (8, 14.5)], 'H')
    c.poly([(8, 8), (8, 14.5), (3.2, 10.2)], 'G')
    c.line(3, 5, 8, 8, 'G')
    c.line(8, 8, 12, 5, 'H')
    c.line(8, 2, 8, 8, 'G')
    c.pts('O', (8, 8), (8, 9), (7, 8))
    return c


@icon('item', 'map', '地図|行き先を調べる地図。折りたたんだ紙に道と×じるし')
def _():
    c = Canvas()
    c.rect(2, 3, 13, 13, 'F')
    c.rect(6, 3, 9, 13, 'f')
    c.rect(5, 3, 5, 13, 'h')
    c.rect(10, 3, 10, 13, 'h')
    c.rect(11, 3, 13, 3, 'f')
    c.rect(3, 4, 4, 5, 'C')
    c.pts('C', (3, 6), (4, 6)) 
    c.pts('Q', (3, 11), (4, 10), (6, 9), (7, 8), (8, 8), (9, 7))
    c.pts('Q', (11, 5), (13, 5), (12, 6), (11, 7), (13, 7))
    c.omap['C'] = 'n'
    return c


@icon('item', 'key', '鍵|扉を開ける鍵。金色の輪っかの頭と、ぎざぎざの先')
def _():
    c = Canvas()
    for y in range(16):
        for x in range(16):
            u = (x + 0.5 - 5.2)
            v = (y + 0.5 - 5.2)
            r = math.hypot(u, v)
            if r <= 3.9:
                if r >= 1.6:
                    t = (u + v) / 7
                    c.px(x, y, 'G' if t < -0.2 else ('J' if t > 0.25 else 'H'))
    c.line(8, 8, 13, 13, 'H')
    c.line(8, 9, 12, 13, 'J')
    c.line(7, 8, 12, 13, 'G')
    c.pts('H', (11, 12), (12, 11), (13, 10))
    c.pts('J', (13, 11), (13, 12))
    c.pts('G', (10, 13), (9, 12), (10, 14), (8, 13))
    c.pts('J', (10, 15 - 1))
    return c


@icon('item', 'letter', '手紙|イベントで受け取る手紙。赤いろうの封印つき')
def _():
    c = Canvas()
    c.rect(2, 4, 13, 12, 'F')
    c.rect(2, 11, 13, 12, 'f')
    c.rect(12, 4, 13, 12, 'f')
    c.poly([(2, 4), (13.9, 4), (8, 8.8)], 'f')
    c.line(2, 4, 8, 8, 'h')
    c.line(13, 4, 9, 7, 'h')
    c.line(2, 12, 6, 9, 'h')
    c.line(13, 12, 10, 9, 'h')
    c.rect(7, 8, 9, 10, 'Q')
    c.pts('R', (7, 8), (8, 8), (7, 9))
    c.pts('q', (9, 10), (8, 10), (9, 9))
    return c


# ---------------- 灯貨 ----------------

def coin(c, cx, cy, r, mark=True):
    c.ell(cx, cy, r + 0.9, r + 0.9, 'y')
    for y in range(16):
        for x in range(16):
            u, v = (x + 0.5 - cx) / r, (y + 0.5 - cy) / r
            d = u * u + v * v
            if d <= 1.0:
                if d > 0.58:
                    c.px(x, y, 'J' if (u + v) > 0.3 else 'H')
                else:
                    c.px(x, y, 'G')
    if mark and r >= 4.2:
        ix, iy = int(cx - 0.5), int(cy - 2)
        c.pts('H', (ix + 1, iy), (ix, iy + 1), (ix + 1, iy + 1), (ix, iy + 2), (ix + 1, iy + 2), (ix, iy + 3), (ix + 1, iy + 3))
        c.pts('J', (ix + 1, iy + 3))
    elif mark:
        c.px(int(cx), int(cy), 'H')


@icon('coin', 'one', '灯貨1枚|お金の少ない額（1枚）を表す。灯のしるしがある金貨')
def _():
    c = Canvas()
    coin(c, 8, 8, 6.4)
    return c


@icon('coin', 'few', '灯貨数枚|お金の中くらいの額（数枚）を表す。3枚の重なり')
def _():
    c = Canvas()
    coin(c, 8, 5.6, 3.7)
    coin(c, 5.6, 10.2, 3.8)
    coin(c, 10.4, 10.2, 3.8)
    return c


@icon('coin', 'bag', '灯貨の袋|お金の多い額（袋）を表す。口をしばった革袋と金貨')
def _():
    c = Canvas()
    c.sphere(8, 10, 5.7, 4.8, ('W', 'w', 'x'))
    c.poly([(5, 6.5), (11, 6.5), (10, 3.5), (6, 3.5)], 'w')
    c.poly([(5, 6.5), (8, 6.5), (8, 3.5), (6, 3.5)], 'W')
    c.rect(5, 6, 10, 6, 'H')
    c.pts('G', (5, 6), (6, 6), (7, 6))
    c.pts('H', (4, 7), (11, 7))
    c.ell(8, 10.5, 2.6, 2.6, 'H')
    c.ell(7.8, 10.2, 1.7, 1.7, 'G')
    c.pts('J', (8, 9), (8, 10), (8, 11))
    c.pts('G', (6, 2), (7, 2), (8, 2), (9, 2))
    c.pts('H', (9, 2), (7, 3), (8, 3))
    return c
