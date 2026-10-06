"""町を囲む石の塀（2026-10-06、人間の指示「町は基本立体的な塀で囲むようにしてください。塀はエディタで細かく、リアルにドット絵で」）。
すべて一から自作。光は左上。石は一つずつ大きさ・色合いをかえ、目地・欠け・苔・雨だれのしみを入れる。

  townwall-h    横にのびる塀（町の上と下のはし）。上に笠石（かさいし）、前に積んだ石の面。16×16。となりとつながる
  townwall-h2   同じ（石の並びちがい。交互に置いて、くり返しに見えないように）
  townwall-v    たてにのびる塀（町の左右のはし）。上から見た笠石の帯と、右の陰の面。16×16
  townwall-v2   同じ（石の並びちがい）
  townwall-post 角と門の柱。ほかより一段高い角柱に、灯りの環の飾り石。16×28（下の16が足もとのマス、上へ12はみ出す）

使い方: python3 townwall.py [名前...]。書き出し先は、この場所の <名前>.txt と pal-<名前>.json。
"""
import sys
from lib import Pal, G, write, hn

# 石（暖かい灰色。明→暗）、目地、苔、笠石
STONE = ["#c8c0b0", "#b0a796", "#988f80", "#7e766a", "#625b52"]
JOINT = "#3e3832"
MOSS = ["#7a9a4a", "#5a7a36", "#3f5a28"]
CAP = ["#d8d2c4", "#bdb6a6", "#9a9284", "#6e675c"]
STAIN = "#857c70"


def stones(p):
    return [p(c) for c in STONE]


def wall_h(variant):
    p = Pal()
    st = stones(p); jt = p(JOINT); mo = [p(c) for c in MOSS]; cp = [p(c) for c in CAP]; sn = p(STAIN)
    g = G(16, 16)
    # 笠石（上の面と、前のふち）: 0〜4行
    g.rect(0, 0, 15, 2, cp[0]); g.rect(0, 0, 15, 0, cp[1])
    g.rect(0, 3, 15, 3, cp[2]); g.rect(0, 4, 15, 4, cp[3])
    for x in range(0, 16, 8 if variant == 0 else 5):
        g.put((x + variant * 3) % 16, 1, cp[1]); g.put((x + variant * 3) % 16, 2, cp[2])
    # 前の面: 石の段（高さ 3〜4 の段を3つ）。段ごとに目地をずらす
    rows = [(5, 8), (9, 11), (12, 15)]
    for ri, (y0, y1) in enumerate(rows):
        g.rect(0, y0, 15, y1, st[2])
        off = (ri * 5 + variant * 7) % 9
        x = -off
        k = 0
        while x < 16:
            wdt = 5 + hn(k, ri, variant + 3) % 4
            xa, xb = max(0, x), min(15, x + wdt - 1)
            tone = 1 + hn(k, ri, variant) % 3
            g.rect(xa, y0, xb, y1, st[tone])
            g.rect(xa, y0, xb, y0, st[max(0, tone - 1)])        # 石の上のふち（光）
            g.rect(xa, y1, xb, y1, st[min(4, tone + 1)])        # 下のふち（陰）
            if xb + 1 <= 15:
                g.rect(xb + 1, y0, xb + 1, y1, jt)               # たての目地
            if hn(k, ri, variant + 9) % 5 == 0 and xb - xa > 2:
                g.put(xa + 1, y0 + 1, st[0])                      # 欠けの明るい所
            x += wdt + 1
            k += 1
        if y1 + 1 <= 15:
            pass
        g.rect(0, y0 - 1, 15, y0 - 1, jt) if y0 - 1 >= 5 else None   # 横の目地
    # 雨だれのしみ（笠石の下から、たてに）
    for x in (3 + variant * 4, 11 - variant * 2):
        g.rect(x, 5, x, 7 + hn(x, 1, variant) % 3, sn)
    # 苔（笠石のふちと、下の段のすみ）
    for x in range(0, 16):
        if hn(x, 4, variant + 5) % 4 == 0:
            g.put(x, 4, mo[1])
        if hn(x, 15, variant + 6) % 5 == 0:
            g.put(x, 15, mo[2]); g.put(x, 14, mo[1])
    g.put((6 + variant * 5) % 16, 3, mo[0])
    return g, p


def wall_v(variant):
    p = Pal()
    st = stones(p); jt = p(JOINT); mo = [p(c) for c in MOSS]; cp = [p(c) for c in CAP]
    g = G(16, 16)
    # 上から見た笠石の帯（x 3〜11）と、右の陰の面（x 12〜13）、左の光の面（x 2）
    g.rect(2, 0, 2, 15, cp[1])
    g.rect(3, 0, 11, 15, cp[0])
    g.rect(12, 0, 13, 15, st[3]); g.rect(13, 0, 13, 15, st[4])
    # 笠石の継ぎ目（たてに並ぶ板石の境）
    for y in range(0, 16):
        if (y + variant * 3) % 6 == 0:
            g.rect(3, y, 11, y, cp[2])
            g.rect(12, y, 13, y, jt)
    # 笠石の上の、細かなでこぼこ・苔
    for y in range(16):
        for x in range(3, 12):
            hv = hn(x, y, variant + 11)
            if hv % 23 == 0:
                g.put(x, y, cp[1])
            elif hv % 37 == 0:
                g.put(x, y, mo[0])
    # 陰の面の石の目地
    for y in range(2, 16, 4):
        g.put(12, (y + variant) % 16, jt)
    # 地面に落ちる影（右）
    g.rect(14, 0, 14, 15, p("#2a2620"))
    return g, p


def post():
    p = Pal()
    st = stones(p); jt = p(JOINT); mo = [p(c) for c in MOSS]; cp = [p(c) for c in CAP]
    gold, gold2 = p("#e8c050"), p("#a07a20")
    g = G(16, 28)
    # 柱の頭（四角い笠石、ひさしのように少し張り出す）
    g.rect(1, 0, 14, 2, cp[0]); g.rect(1, 0, 14, 0, cp[1]); g.rect(1, 3, 14, 3, cp[2]); g.rect(1, 4, 14, 4, cp[3])
    # 柱の面（左は光、右は陰）
    g.rect(2, 5, 13, 27, st[2])
    g.rect(2, 5, 4, 27, st[1]); g.rect(11, 5, 13, 27, st[3]); g.rect(13, 5, 13, 27, st[4])
    # 石の段
    for y in (10, 16, 22):
        g.rect(2, y, 13, y, jt)
    for (y0, xs) in ((5, (7,)), (11, (5, 10)), (17, (8,)), (23, (5, 10))):
        for x in xs:
            g.rect(x, y0, x, y0 + 4, jt)
    # 灯りの環の飾り石（まんなか、金の輪）
    g.rect(6, 6, 9, 6, gold); g.rect(5, 7, 5, 8, gold); g.rect(10, 7, 10, 8, gold2); g.rect(6, 9, 9, 9, gold2)
    g.rect(7, 7, 8, 8, st[0])
    # 苔（足もと）
    for x in range(2, 14):
        if hn(x, 27, 3) % 3 == 0:
            g.put(x, 27, mo[1]); g.put(x, 26, mo[2]) if hn(x, 26, 4) % 2 else None
    g.put(3, 4, mo[0]); g.put(12, 4, mo[1])
    return g, p


def townwall_h():
    return wall_h(0)


def townwall_h2():
    return wall_h(1)


def townwall_v():
    return wall_v(0)


def townwall_v2():
    return wall_v(1)


def townwall_post():
    return post()


ALL = ["townwall-h", "townwall-h2", "townwall-v", "townwall-v2", "townwall-post"]

if __name__ == "__main__":
    for n in (sys.argv[1:] or ALL):
        g, p = globals()[n.replace("-", "_")]()
        print(n, write(n, g, p))
