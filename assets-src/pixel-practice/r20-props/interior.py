"""家の中の家具（本棚・ベッド・箪笥・テーブル）。すべて一から自作。光は左上、ハイライト（照り）なし、影と地の2〜3段＋暗い縁取り。
使い方: python3 interior.py [名前...]。書き出し先は、この場所の <名前>.txt と pal-<名前>.json。"""
import sys
from lib import Pal, G, write, hn

SH = "#14121c"   # 足元の影（キー S）

def wood(p):
    return p("#c89258", "#a06c3a", "#774c26", "#4a301a")   # 明 / 地 / 影 / いちばん暗い

def bookshelf():
    p = Pal(); ol = p("#2a1a10"); w1, w2, w3, w4 = wood(p); sh = p(SH)
    top1 = p("#dcae72")                                    # 天板の上の面（いちばん明るい）
    book_cols = [("#b84a42", "#8a2e2e"), ("#4a78b0", "#2e4e80"), ("#d8b048", "#a08028"), ("#58985a", "#34683a"), ("#8a58a8", "#5a3478"), ("#d8d0b8", "#a8a088"), ("#c87a3a", "#8a4a1c")]
    cols = [(p(a), p(b)) for a, b in book_cols]
    g = G(30, 40)
    # 天板の上の面（奥行き）: 手前へ向かって少し広がる台形ではなく、奥の縁と手前の縁がある長方形
    g.rect(2, 0, 27, 5, top1)
    g.rect(2, 0, 27, 0, w1)
    g.rect(2, 5, 27, 5, w2)
    g.rect(27, 1, 27, 5, w3)
    # 天板の前の面
    g.rect(1, 6, 28, 8, w1); g.rect(1, 8, 28, 8, w3)
    # 本体（左右の側板は手前に厚みが見える）
    g.rect(1, 9, 28, 37, w2)
    g.rect(1, 9, 3, 37, w1)      # 左の側板の前の面
    g.rect(26, 9, 28, 37, w3)    # 右の側板の前の面
    # 中のくぼみ（奥の板は暗く。側板の内側の面が見えて、奥行きになる）
    g.rect(4, 10, 25, 36, w4)
    g.rect(4, 10, 5, 36, w3)     # 左の側板の内側（影）
    g.rect(24, 10, 25, 36, w4)
    shelves = [(10, 18), (19, 27), (28, 36)]
    for si, (y0, y1) in enumerate(shelves):
        # 棚板（手前の厚みと、下にできる影）
        g.rect(4, y1, 25, y1, w1)
        g.rect(4, y1 + 1, 25, y1 + 1, w3) if y1 + 1 <= 36 else None
        x = 6
        while x < 24:
            wb = 2 + hn(x, y0, si) % 2
            hb = 5 + hn(x, y0, si + 7) % 4
            if hn(x, y0, si + 3) % 11 == 0:
                x += 2
                continue
            if x + wb > 24: break
            lc, dc = cols[(hn(x, y0, 5) + si) % len(cols)]
            top = y1 - hb
            g.rect(x, top, x + wb - 1, y1 - 1, lc)
            g.rect(x + wb - 1, top, x + wb - 1, y1 - 1, dc)
            if hn(x, y0, 9) % 3 == 0:
                g.rect(x, top + 2, x + wb - 1, top + 2, dc)
            x += wb
        # 棚のなかの、上の暗がり
        g.rect(6, y0, 23, y0, w4)
    g.outline(ol, {})
    g.shadow(15, 39, 14, sh, 0)
    return g, p

def bed():
    p = Pal(); ol = p("#2a1a10"); w1, w2, w3, w4 = wood(p); sh = p(SH)
    cl, cm, cd = p("#fbf4e4", "#e0d4bc", "#b8a88c")      # まくら・シーツ
    q1, q2, q3 = p("#5f8fc4", "#3f68a0", "#2c4a78")      # 掛けぶとん（青）
    g = G(34, 32)
    # ヘッドボード（背の高い板。上が丸い）
    g.rect(2, 3, 31, 14, w2)
    g.rect(3, 2, 30, 2, w2); g.rect(5, 1, 28, 1, w1)
    g.rect(2, 3, 31, 3, w1)
    g.rect(2, 14, 31, 14, w3)
    for x in range(4, 30, 5): g.rect(x, 5, x + 2, 12, w3)   # 板のくぼみ
    for x in range(4, 30, 5): g.rect(x, 5, x, 12, w1)
    # 柱
    g.rect(1, 2, 3, 30, w1); g.rect(30, 2, 32, 30, w3); g.rect(2, 2, 2, 30, w1)
    # シーツとまくら
    g.rect(4, 13, 29, 27, cm)
    g.rect(5, 11, 14, 17, cl); g.rect(5, 16, 14, 17, cm); g.rect(13, 11, 14, 17, cd)   # まくら
    g.rect(17, 11, 26, 17, cl); g.rect(17, 16, 26, 17, cm); g.rect(25, 11, 26, 17, cd)
    # 掛けぶとん（上のへりを折り返す）
    g.rect(4, 18, 29, 27, q2)
    g.rect(4, 18, 29, 19, cl)
    g.rect(4, 20, 29, 20, cd)
    for y in range(21, 27):
        for x in range(4, 30):
            if (x // 4 + y // 3) % 2 == 0: g.put(x, y, q1)
    g.rect(4, 26, 29, 27, q3)
    g.rect(29, 18, 29, 27, q3)
    # フットボード（手前の低い板）
    g.rect(2, 26, 31, 29, w2); g.rect(2, 26, 31, 26, w1); g.rect(2, 29, 31, 29, w3)
    # 脚
    g.rect(2, 30, 4, 30, w3); g.rect(29, 30, 31, 30, w4)
    g.outline(ol, {})
    g.shadow(17, 31, 16, sh, 0)
    return g, p

def tansu():
    p = Pal(); ol = p("#2a1a10"); w1, w2, w3, w4 = wood(p); sh = p(SH)
    top1 = p("#dcae72")
    ir1, ir2 = p("#7e8494", "#4e5464"); gd = p("#e8c050")
    fr, fr2 = p("#e8c050", "#a07a20"); pic1, pic2, pic3, pic4 = p("#8ac0e8", "#58985a", "#d8b048", "#f4ecd8")
    g = G(30, 38)
    # 上に飾った写し絵（金のわくに、空と丘）
    g.rect(4, 0, 12, 9, fr)
    g.rect(5, 1, 11, 8, pic4)
    g.rect(5, 1, 11, 4, pic1); g.rect(5, 5, 11, 8, pic2); g.rect(8, 2, 9, 3, pic3)
    g.rect(4, 9, 12, 9, fr2); g.rect(12, 0, 12, 9, fr2)
    g.put(8, 10, w4)
    # 小さな花びん
    g.rect(21, 6, 24, 10, p("#8a98c0")); g.rect(23, 6, 24, 10, p("#5a6890")); g.put(22, 5, p("#c0504a")); g.put(23, 4, p("#c0504a")); g.put(24, 5, p("#58985a"))
    # 天板の上の面（奥行き）
    g.rect(2, 11, 27, 15, top1)
    g.rect(2, 11, 27, 11, w1)
    g.rect(2, 15, 27, 15, w2)
    g.rect(27, 12, 27, 15, w3)
    # 天板の前の面
    g.rect(1, 16, 28, 17, w1); g.rect(1, 17, 28, 17, w3)
    # 本体（前の面）
    g.rect(1, 18, 28, 33, w2)
    g.rect(1, 18, 2, 33, w1)
    g.rect(27, 18, 28, 33, w3)
    # 引き出し4段
    for i in range(4):
        y0 = 19 + i * 4
        g.rect(4, y0, 25, y0 + 2, w2 if i % 2 == 0 else w1)
        g.rect(4, y0 + 3, 25, y0 + 3, w3)
        g.rect(4, y0, 4, y0 + 2, w1)
        g.rect(25, y0, 25, y0 + 2, w3)
        g.rect(13, y0 + 1, 16, y0 + 1, ir1); g.rect(13, y0 + 2, 16, y0 + 2, ir2)
    for (x0, y0) in ((1, 18), (27, 18), (1, 32), (27, 32)):
        g.rect(x0, y0, x0 + 1, y0 + 1, ir1); g.put(x0 + 1, y0 + 1, ir2)
    g.put(14, 33, gd)
    # 脚
    g.rect(2, 34, 5, 35, w3); g.rect(24, 34, 27, 35, w4)
    g.outline(ol, {})
    g.shadow(15, 37, 14, sh, 0)
    return g, p

def table():
    p = Pal(); ol = p("#2a1a10"); w1, w2, w3, w4 = wood(p); sh = p(SH)
    c1, c2, c3 = p("#f4ecd8", "#d8cbb0", "#b0a284")       # テーブルクロス
    r1, r2 = p("#b84a42", "#8a2e2e")                        # 赤いふち
    t1, t2, t3 = p("#e8e0d0", "#c0b6a2", "#8a8070")         # 陶器
    fl, fl2 = p("#f2c14e", "#d8902a")                             # ろうそくの火
    g = G(32, 28)
    # 脚（中央の台）と足
    g.rect(13, 14, 18, 22, w2); g.rect(13, 14, 14, 22, w1); g.rect(18, 14, 18, 22, w3)
    g.rect(8, 23, 23, 24, w2); g.rect(8, 23, 23, 23, w1); g.rect(8, 24, 23, 24, w3)
    # 天板（楕円）+ クロス
    g.ell(16, 10, 15, 6, lambda x, y, nx, ny: r2 if ny > 0.75 else c2 if (nx + ny) > 0.55 else c1)
    g.ell(16, 9, 12, 4.2, lambda x, y, nx, ny: c3 if (nx * 0.6 + ny) > 0.65 else c1)
    for x in range(3, 29, 3):
        g.put(x, 14, r1)  # たれ布のふち飾り
    # ポットとカップ
    g.rect(11, 5, 16, 8, t1); g.rect(11, 8, 16, 8, t2); g.rect(15, 5, 16, 8, t3)
    g.rect(10, 6, 10, 7, t2); g.rect(17, 6, 18, 6, t2)
    g.rect(12, 4, 14, 4, t2)
    g.rect(21, 6, 24, 8, t1); g.rect(21, 8, 24, 8, t2); g.put(24, 7, t3)
    # ろうそく
    g.rect(6, 5, 7, 8, c1); g.rect(7, 5, 7, 8, c3)
    g.put(6, 3, fl); g.put(6, 4, fl2); g.put(7, 4, fl)
    g.outline(ol, {})
    g.shadow(16, 27, 15, sh, 0)
    return g, p

ALL = ["bookshelf", "bed", "tansu", "table"]

if __name__ == "__main__":
    for n in (sys.argv[1:] or ALL):
        g, p = globals()[n.replace("-", "_")]()
        print(n, write(n, g, p))
