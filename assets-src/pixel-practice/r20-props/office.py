"""相談所の支部・ユーリの家の家具（2026-10-06、人間の指示「支部の部屋もっと大きくしてカウンター、机、棚、資料を置くように」
「ユーリの自宅を作って」）。すべて一から自作。interior.py と同じ約束（光は左上、照りなし、影と地の2〜3段＋暗い縁取り、足元に影 S）。
  desk          事務机（書類・インク壺・羽ペン・灯り石のランプ）  32×30
  papers        書類の山（ひもでしばった束・帳面・巻いた地図）      16×22
  cabinet       資料棚（とじた帳面・巻物・木箱・名札）               32×42
  front-counter 受付カウンター（帳簿・呼び鈴・灯の徽章）             48×28
  hearth        かまど（れんが・鍋・火）                             32×36
  ladder        屋根裏への梯子                                       16×40
使い方: python3 office.py [名前...]。書き出し先は、この場所の <名前>.txt と pal-<名前>.json。"""
import sys
from lib import Pal, G, write, hn

SH = "#14121c"


def wood(p):
    return p("#c89258", "#a06c3a", "#774c26", "#4a301a")


def paper_cols(p):
    return p("#f6efdc", "#e0d4b4", "#b8a882")


def desk():
    p = Pal(); ol = p("#2a1a10"); w1, w2, w3, w4 = wood(p); sh = p(SH)
    top1 = p("#dcae72")
    pa1, pa2, pa3 = paper_cols(p)
    ink, ink2 = p("#2a2a40"), p("#4a4a68")
    qu1, qu2 = p("#f4f0e8"), p("#b8b0a0")
    br1, br2 = p("#c8a040"), p("#8a6a20")
    gl1, gl2 = p("#f2e090"), p("#e0b040")
    g = G(32, 30)
    # 天板の上の面
    g.rect(1, 9, 30, 15, top1)
    g.rect(1, 9, 30, 9, w1)
    g.rect(1, 15, 30, 15, w2)
    g.rect(30, 10, 30, 15, w3)
    # 書類（重ねた紙・少しずらして）
    g.rect(4, 10, 13, 14, pa2); g.rect(5, 10, 13, 13, pa1); g.rect(6, 11, 11, 11, pa3); g.rect(6, 12, 10, 12, pa3)
    g.rect(13, 11, 13, 14, pa3)
    # インク壺と羽ペン
    g.rect(16, 11, 18, 13, ink); g.put(16, 11, ink2); g.rect(16, 10, 18, 10, ink2)
    g.line(17, 9, 21, 4, qu1); g.line(18, 9, 22, 5, qu2); g.put(17, 10, qu2)
    # 灯り石のランプ（真鍮の台と、ほのかに光るガラス）
    g.rect(24, 13, 28, 14, br2); g.rect(25, 12, 27, 12, br1)
    g.rect(25, 6, 27, 11, gl1); g.rect(27, 6, 27, 11, gl2); g.rect(24, 5, 28, 5, br1); g.rect(25, 4, 27, 4, br2)
    # 天板の前の面
    g.rect(0, 16, 31, 17, w1); g.rect(0, 17, 31, 17, w3)
    # 引き出しの袖（左）と、足もとのあき（右）
    g.rect(1, 18, 12, 27, w2); g.rect(1, 18, 2, 27, w1); g.rect(11, 18, 12, 27, w3)
    for y0 in (19, 23):
        g.rect(3, y0, 10, y0 + 2, w1); g.rect(3, y0 + 3, 10, y0 + 3, w3)
        g.rect(6, y0 + 1, 7, y0 + 1, br1)
    g.rect(13, 18, 28, 27, w4)                 # 机の下の暗がり
    g.rect(13, 18, 28, 18, w3)
    g.rect(28, 18, 30, 27, w2); g.rect(30, 18, 30, 27, w3)   # 右の脚
    g.outline(ol, {})
    g.shadow(16, 29, 15, sh, 0)
    return g, p


def papers():
    p = Pal(); ol = p("#2a1a10"); sh = p(SH)
    pa1, pa2, pa3 = paper_cols(p)
    st1, st2 = p("#c8a070", "#8a6a44")              # しばったひも
    bk1, bk2, bk3 = p("#7a4a3a", "#5a3428", "#9a6a52")   # 帳面の表紙
    mp1, mp2 = p("#e8dcb8", "#c0ae80")            # 巻いた地図
    g = G(16, 22)
    # いちばん下: 帳面の束
    g.rect(1, 14, 14, 19, bk2); g.rect(1, 14, 14, 15, bk3); g.rect(1, 16, 14, 16, pa2); g.rect(1, 18, 14, 18, pa3)
    g.rect(14, 14, 14, 19, bk1)
    # 上: ひもでしばった紙の束
    g.rect(2, 7, 13, 13, pa1); g.rect(2, 7, 13, 7, pa1); g.rect(13, 8, 13, 13, pa3)
    for y in (9, 11): g.rect(3, y, 12, y, pa2)
    g.rect(7, 7, 8, 13, st1); g.put(8, 7, st2); g.rect(6, 6, 9, 6, st1)
    # いちばん上: 巻いた地図
    g.rect(3, 3, 12, 5, mp1); g.rect(3, 5, 12, 5, mp2); g.rect(3, 3, 3, 5, mp2); g.rect(12, 3, 12, 5, mp2)
    g.put(4, 4, mp2); g.rect(7, 3, 7, 5, p("#b84a42"))
    g.outline(ol, {})
    g.shadow(8, 21, 7, sh, 0)
    return g, p


def cabinet():
    p = Pal(); ol = p("#2a1a10"); w1, w2, w3, w4 = wood(p); sh = p(SH)
    top1 = p("#dcae72")
    pa1, pa2, pa3 = paper_cols(p)
    bind = [p("#7a4a3a", "#5a3428"), p("#3e5a7a", "#2a3e58"), p("#5a6a3a", "#3e4a28"), p("#8a6a3a", "#5e4626")]
    lab = p("#f0e6c8")
    sc1, sc2 = p("#e8dcb8", "#b8a47a")
    bx1, bx2 = p("#a87a48", "#7a5430")
    g = G(32, 42)
    g.rect(2, 0, 29, 4, top1); g.rect(2, 0, 29, 0, w1); g.rect(2, 4, 29, 4, w2); g.rect(29, 1, 29, 4, w3)
    g.rect(1, 5, 30, 7, w1); g.rect(1, 7, 30, 7, w3)
    g.rect(1, 8, 30, 39, w2); g.rect(1, 8, 3, 39, w1); g.rect(28, 8, 30, 39, w3)
    g.rect(4, 9, 27, 38, w4); g.rect(4, 9, 5, 38, w3)
    rows = [(9, 17), (18, 27), (28, 38)]
    for si, (y0, y1) in enumerate(rows):
        g.rect(4, y1, 27, y1, w1)
        if y1 + 1 <= 38: g.rect(4, y1 + 1, 27, y1 + 1, w3)
        g.rect(6, y0, 25, y0, w4)
        if si == 0:
            # とじた帳面（背に名札）
            x = 6
            for i in range(6):
                c1, c2 = bind[(i + hn(i, 1)) % len(bind)]
                g.rect(x, y0 + 2, x + 2, y1 - 1, c1); g.rect(x + 2, y0 + 2, x + 2, y1 - 1, c2)
                g.rect(x, y0 + 4, x + 1, y0 + 5, lab)
                x += 3
            g.rect(25, y1 - 5, 25, y1 - 1, pa3)
        elif si == 1:
            # 巻物を積んだ所と、書類の束
            for i, (cx, cy) in enumerate(((7, y1 - 2), (11, y1 - 2), (9, y1 - 5), (15, y1 - 2))):
                g.rect(cx - 2, cy - 1, cx + 1, cy + 1, sc1); g.put(cx - 2, cy, sc2); g.put(cx + 1, cy + 1, sc2)
            g.rect(18, y1 - 5, 25, y1 - 1, pa1); g.rect(18, y1 - 3, 25, y1 - 3, pa2); g.rect(25, y1 - 5, 25, y1 - 1, pa3)
        else:
            # 木箱（名札つき）
            for x0 in (6, 16):
                g.rect(x0, y0 + 3, x0 + 8, y1 - 1, bx1); g.rect(x0 + 8, y0 + 3, x0 + 8, y1 - 1, bx2); g.rect(x0, y0 + 3, x0 + 8, y0 + 3, bx2)
                g.rect(x0 + 3, y0 + 5, x0 + 5, y0 + 6, lab)
    g.rect(2, 40, 5, 40, w3); g.rect(26, 40, 29, 40, w4)
    g.outline(ol, {})
    g.shadow(16, 41, 15, sh, 0)
    return g, p


def front_counter():
    p = Pal(); ol = p("#2a1a10"); w1, w2, w3, w4 = wood(p); sh = p(SH)
    top1 = p("#e8bc80")
    pa1, pa2, pa3 = paper_cols(p)
    bk1, bk2 = p("#7a4a3a", "#5a3428")
    br1, br2 = p("#d8b048", "#9a7420")
    em1, em2 = p("#f2c14e", "#b07a20")
    g = G(48, 28)
    # 天板の上の面（奥行き）
    g.rect(1, 6, 46, 11, top1); g.rect(1, 6, 46, 6, w1); g.rect(1, 11, 46, 11, w2); g.rect(46, 7, 46, 11, w3)
    # 開いた帳簿
    g.rect(5, 7, 16, 10, pa1); g.rect(10, 7, 11, 10, pa3); g.rect(6, 8, 9, 8, pa2); g.rect(12, 8, 15, 8, pa2); g.rect(6, 9, 8, 9, pa2)
    g.rect(4, 10, 17, 10, bk2)
    # 呼び鈴
    g.rect(29, 8, 32, 9, br1); g.rect(32, 8, 32, 9, br2); g.rect(28, 10, 33, 10, br2); g.put(30, 7, br1)
    # 書類のトレー
    g.rect(37, 8, 44, 10, w3); g.rect(38, 7, 43, 9, pa1); g.rect(43, 7, 43, 9, pa3)
    # 前の面（板）
    g.rect(0, 12, 47, 13, w1); g.rect(0, 13, 47, 13, w3)
    g.rect(0, 14, 47, 25, w2)
    for x in (0, 11, 23, 35, 46):
        g.rect(x, 14, x + 1, 25, w1 if x < 23 else w3)
    for x in range(3, 46, 6):
        g.rect(x, 15, x, 24, w3)
    # 灯の徽章（まんなか。丸い環に灯り）
    g.ell(24, 19, 4, 4, lambda x, y, nx, ny: em2 if (nx * nx + ny * ny) > 0.55 else w2)
    g.rect(23, 18, 25, 20, em1); g.put(24, 17, em1)
    g.rect(0, 25, 47, 25, w4)
    g.outline(ol, {})
    g.shadow(24, 27, 23, sh, 0)
    return g, p


def hearth():
    p = Pal(); ol = p("#241a16"); sh = p(SH)
    b1, b2, b3, b4 = p("#b06a4a", "#8a4a34", "#6a3426", "#4a2418")   # れんが
    mo = p("#c8b49a")                                          # 目地
    ir1, ir2, ir3 = p("#6a6e7a", "#4a4e5a", "#2e3038")          # 鉄の鍋
    f1, f2, f3 = p("#fff0a0", "#f2a040", "#c85a2a")           # 火
    st1, st2 = p("#e8e0d0", "#c8c0b0")                         # 湯気
    g = G(32, 36)
    # 煙突（上）
    g.rect(10, 0, 21, 9, b2); g.rect(10, 0, 11, 9, b1); g.rect(20, 0, 21, 9, b3)
    # 本体
    g.rect(1, 10, 30, 33, b2)
    g.rect(1, 10, 3, 33, b1); g.rect(28, 10, 30, 33, b3)
    for y in range(12, 33, 3):
        g.rect(1, y, 30, y, mo)
        off = 0 if (y // 3) % 2 == 0 else 3
        for x in range(1 + off, 30, 6):
            g.put(x, y + 1, mo); g.put(x, y + 2, mo)
    for y in range(2, 9, 3):
        g.rect(10, y, 21, y, mo)
    # かまどの口（暗い穴と火）
    g.rect(8, 21, 23, 32, b4); g.rect(9, 22, 22, 32, ir3)
    g.rect(10, 28, 21, 31, f3); g.rect(12, 26, 19, 30, f2); g.rect(14, 25, 17, 29, f1); g.put(13, 25, f2); g.put(18, 24, f2)
    g.rect(9, 32, 22, 32, b4)
    # 上の鍋と湯気
    g.rect(9, 12, 22, 18, ir2); g.rect(9, 12, 22, 13, ir1); g.rect(21, 13, 22, 18, ir3); g.rect(7, 13, 8, 14, ir2); g.rect(23, 13, 24, 14, ir2)
    g.rect(10, 11, 21, 11, ir3)
    g.put(13, 9, st2); g.put(14, 8, st1); g.put(13, 7, st1); g.put(17, 9, st2); g.put(18, 8, st1); g.put(17, 6, st1)
    g.outline(ol, {})
    g.shadow(16, 35, 15, sh, 0)
    return g, p


def ladder():
    p = Pal(); ol = p("#2a1a10"); w1, w2, w3, w4 = wood(p); sh = p(SH)
    g = G(16, 40)
    for x0 in (2, 12):
        g.rect(x0, 0, x0 + 1, 37, w2); g.put(x0, 0, w1)
        g.rect(x0, 0, x0, 37, w1); g.rect(x0 + 1, 0, x0 + 1, 37, w3)
    for y in range(3, 37, 5):
        g.rect(4, y, 11, y, w1); g.rect(4, y + 1, 11, y + 1, w3)
    g.outline(ol, {})
    g.shadow(8, 39, 7, sh, 0)
    return g, p


ALL = ["desk", "papers", "cabinet", "front-counter", "hearth", "ladder"]

if __name__ == "__main__":
    for n in (sys.argv[1:] or ALL):
        g, p = globals()[n.replace("-", "_")]()
        print(n, write(n, g, p))
