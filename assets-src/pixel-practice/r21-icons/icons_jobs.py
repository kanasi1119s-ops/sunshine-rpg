"""ジョブのしるし（16x16の丸い紋章）。

枠の色でランクが分かる:
  初期ジョブ=鋼の枠 / 上級ジョブ=金の枠 / 天神ジョブ=白金の枠 / 悪神ジョブ=紫の枠 / レジェンド=炎色の枠
中の絵（8x8）でジョブの特徴が分かる。
"""
import math

from common import Canvas, icon

RING_STEEL = ('S', 's', 'z')
RING_GOLD = ('G', 'H', 'J')
RING_PALE = ('F', 'f', 'h')
RING_EVIL = ('U', 'u', 'A')
RING_FLAME = ('Y', 'O', 'T')

F_SWORD = ('m', 'A')
F_FIST = ('x', 'n')
F_ARCHER = ('d', 'e')
F_FIRE = ('q', 'r')
F_WATER = ('c', 'b')
F_WIND = ('j', 'o')
F_EARTH = ('w', 'x')
F_WAND = ('u', 'v')
F_HOLY = ('c', 'b')
F_EVIL = ('a', 'A')


def medal(ring, field):
    c = Canvas()
    c.sphere(8, 8, 7.4, 7.4, ring)
    # 内側の面
    for y in range(16):
        for x in range(16):
            u, v = (x + 0.5 - 8) / 5.5, (y + 0.5 - 8) / 5.5
            if u * u + v * v <= 1.0:
                c.px(x, y, field[1] if (u + v) / 2 > 0.45 else field[0])
    return c


class Sym:
    """8x8の絵を、紋章の中央(4,4)に描くための手助け"""
    def __init__(self, c):
        self.c = c

    def rows(self, rows):
        self.c.stamp(4, 4, rows)

    def line(self, x0, y0, x1, y1, k):
        self.c.line(x0 + 4, y0 + 4, x1 + 4, y1 + 4, k)

    def pts(self, k, *p):
        for x, y in p:
            self.c.px(x + 4, y + 4, k)


def job(name, label, desc, ring, field, art, omap=None):
    @icon('job', name, f'{label}|{desc}')
    def _():
        c = medal(ring, field)
        if callable(art):
            art(Sym(c))
        else:
            Sym(c).rows(art)
        c.omap.update({'S': 'k', 'G': 'y', 'F': 'n', 'U': 'v', 'Y': 'r'})
        if omap:
            c.omap.update(omap)
        return c
    return _


SWORD = ["...SS...",
         "...Ss...",
         "...Ss...",
         "...Ss...",
         ".GGGGGG.",
         "...ww...",
         "...ww...",
         "...HH..."]

FIST = ["..PPPP..",
        ".PPPPPp.",
        "PpPpPpPp",
        "PpPpPpPp",
        "PPPPPPpp",
        "PPPPPppp",
        ".FFFFFF.",
        ".fffffff"]

BOW = ["..WWW...",
       ".W...F..",
       "W....F..",
       "WwwwwSSs",
       "W....F..",
       ".W...F..",
       "..WWW...",
       "........"]

FLAME = ["...R....",
         "..RR.R..",
         "..RRRR..",
         ".RRORRR.",
         ".RROOQR.",
         ".RROYOQ.",
         "..QOOQ..",
         "...QQ..."]

RIPPLE = ["..IIII..",
          ".I....I.",
          "I..BB..I",
          "I.B..B.I",
          "I.B..B.I",
          "I..BB..I",
          ".I....I.",
          "..IIII.."]

MOUNTAIN = ["...MM...",
            "..MMNN..",
            "..MNNN..",
            ".MMNNDD.",
            ".MNNNDD.",
            "MMNNNDDD",
            "MNNNNDDD",
            "NNNNDDDD"]

JESTER = ["G......G",
          "RR....BB",
          "RRR..BBB",
          ".RRRBBB.",
          ".RRRBBB.",
          ".RRRBBB.",
          "GGGGGGGG",
          ".GHGHGH."]


def wind(s):
    for i in range(0, 40):
        th = i * 0.17
        r = 0.4 + th * 0.55
        x = round(3.5 + r * math.cos(th + 3.4))
        y = round(3.5 + r * math.sin(th + 3.4))
        if 0 <= x < 8 and 0 <= y < 8:
            s.pts('F', (x, y))
    s.pts('F', (7, 5), (7, 6), (6, 7))


job('sword-guard', '剣衛士', '初期ジョブ。攻守バランスの近接アタッカー兼盾役。剣の紋', RING_STEEL, F_SWORD, SWORD)
job('fist-fighter', '拳闘士', '初期ジョブ。連続攻撃の高速アタッカー。包帯を巻いた拳の紋', RING_STEEL, F_FIST, FIST)
job('archer', '弓術士', '初期ジョブ。会心率の高い遠距離アタッカー。弓と矢の紋', RING_STEEL, F_ARCHER, BOW)
job('flame-mage', '火照術士', '初期ジョブ。攻撃呪文特化（火照系）。炎の紋', RING_STEEL, F_FIRE, FLAME)
job('ripple-mage', '水紋術士', '初期ジョブ。回復・防御呪文特化（水紋系）。波紋の紋', RING_STEEL, F_WATER, RIPPLE)
job('wind-mage', '風唱術士', '初期ジョブ。すばやさ強化と状態異常（風唱系）。渦の紋', RING_STEEL, F_WIND, wind)
job('earth-guard', '地固衛士', '初期ジョブ。防御・拘束特化（地固系）。山の紋', RING_STEEL, F_EARTH, MOUNTAIN)
job('wanderer', '旅芸人', '初期ジョブ。バフ・デバフ・不確定な効果。道化の帽子の紋', RING_STEEL, F_WAND, JESTER)


def crossed(s):
    s.line(0, 0, 5, 5, 'S')
    s.line(1, 0, 5, 4, 's')
    s.line(7, 0, 2, 5, 'S')
    s.line(6, 0, 2, 4, 's')
    s.pts('G', (6, 6), (7, 7), (5, 6), (6, 5), (0, 6), (1, 7), (2, 6), (1, 5))
    s.pts('H', (7, 6), (6, 7), (0, 7), (1, 6))


WINGFIST = ["...PPPP.",
            "FF.PpPpP",
            "...PpPpP",
            "FFFPPPPp",
            "...PPPpp",
            "FF.PPppp",
            "....wwww",
            "........"]


def rain(s):
    for x, y0, y1 in ((0, 0, 4), (3, 1, 5), (6, 0, 4)):
        s.line(x, y0, x, y1, 'F')
        s.pts('S', (x, y1 + 1), (x - 1, y1), (x + 1, y1), (x, y1))
        s.pts('R', (x - 1, y0), (x + 1, y0))


DOUBLEFLAME = ["R...R..R",
               "RR.RR.RR",
               "RRRRRRRR",
               "RROOROOR",
               ".ROOOOOR",
               ".QOYYOOQ",
               "..QOOOQ.",
               "...QQQ.."]


def waves(s):
    for base, k in ((0, 'I'), (3, 'B'), (6, 'C')):
        for x in range(8):
            y = base + (1 if (x // 2) % 2 else 0)
            s.pts(k, (x, y))


def gale(s):
    for row, k in ((1, 'F'), (4, 'F')):
        for x in range(7):
            y = row + round(math.sin(x * 0.9) * 1.1)
            s.pts(k, (x, y))
    s.pts('F', (7, 1), (7, 2), (6, 2), (6, 5), (7, 5), (7, 6))
    s.pts('L', (2, 6), (3, 7), (3, 6), (4, 7))
    s.pts('l', (4, 6), (5, 7))


GUARDIAN_SHIELD = ["MMMMMMMM",
                   "MNNNNNND",
                   "MNNGGNND",
                   "MNNGGNND",
                   ".MNNNNDD",
                   ".MNNNND.",
                   "..MNND..",
                   "...DD..."]

MASK = [".FFFFFF.",
        "FFFFFFFf",
        "FAAFFAAf",
        "FAAFFAAf",
        "FRFFFFRf",
        "FAFFFFAf",
        ".FAAAAf.",
        "..ffff.."]

job('sword-saint', '剛剣聖', '上級ジョブ（剣衛士の上）。攻防とも強い主力。交差した2本の剣の紋', RING_GOLD, F_SWORD, crossed)
job('sky-fist', '天翔拳士', '上級ジョブ（拳闘士の上）。最速の乱れ撃ち。風を切る速い線と拳の紋', RING_GOLD, F_FIST, WINGFIST)
job('hundred-archer', '百矢の射手', '上級ジョブ（弓術士の上）。範囲攻撃。降りそそぐ3本の矢の紋', RING_GOLD, F_ARCHER, rain)
job('inferno-guide', '業火導師', '上級ジョブ（火照術士の上）。範囲攻撃呪文。三つに燃え上がる大きな炎の紋', RING_GOLD, F_FIRE, DOUBLEFLAME)
job('stream-sage', '清流賢者', '上級ジョブ（水紋術士の上）。全体回復。流れる波の紋', RING_GOLD, F_WATER, waves)
job('gale-dancer', '疾風の舞手', '上級ジョブ（風唱術士の上）。風の刃と舞い。風の筋と木の葉の紋', RING_GOLD, F_WIND, gale)
job('immovable-guardian', '不動の守人', '上級ジョブ（地固衛士の上）。かばう・半減の構え。石の盾の紋', RING_GOLD, F_EARTH, GUARDIAN_SHIELD)
job('many-faced-artist', '千変の遊芸師', '上級ジョブ（旅芸人の上）。何が出るか分からない芸。仮面の紋', RING_GOLD, F_WAND, MASK)

def moon(s):
    for y in range(8):
        for x in range(8):
            a = math.hypot(x + 0.5 - 3.8, y + 0.5 - 4.0)
            b = math.hypot(x + 0.5 - 5.4, y + 0.5 - 3.4)
            if a <= 3.9 and b >= 3.2:
                s.pts('F' if a < 3.0 else 'f', (x, y))
    s.pts('G', (6, 1), (7, 5), (5, 6))


WINGSWORD = ["...SS...",
             "F..Ss..F",
             "FF.Ss.FF",
             "FFfSsfFF",
             ".fGGGGf.",
             "...ww...",
             "...ww...",
             "...ww..."]

DEMON = ["F......F",
         "FF....FF",
         ".RRRRRR.",
         "RRYRRYRR",
         "RQQRRQQR",
         "RRRRRRRq",
         ".RFRRFR.",
         "..qqqq.."]

BUG = [".U....U.",
       "..U..U..",
       "VV.YY.VV",
       "VVVUUVVV",
       "VuVUUVuV",
       ".VuUUuV.",
       "..VUUV..",
       "...uu..."]

LAMP = ["...Y....",
        "..YOY...",
        "..OOO...",
        "...Q....",
        ".GGGGGG.",
        "GHHHHHHG",
        ".JHHHHJ.",
        "..JJJJ.."]

job('goddess-shaman', '女神の巫覡', '天神ジョブ。最高クラスの回復。月と星の紋', RING_PALE, F_HOLY, moon, omap={'G': 'n'})
job('pure-paladin', '純神の聖騎士', '天神ジョブ。最高クラスの守り。翼のある白い剣の紋', RING_PALE, F_HOLY, WINGSWORD)
job('demon-breaker', '鬼神の破戒者', '悪神ジョブ。最高の攻撃力とHPの代償。角のある鬼の顔の紋', RING_EVIL, F_EVIL, DEMON, omap={'R': 'r'})
job('bug-curser', '蟲神の呪術師', '悪神ジョブ。呪いと一撃のチャンス。羽ばたく蟲の紋', RING_EVIL, F_EVIL, BUG)
job('torch-heir', '灯心継承者', 'レジェンドジョブ（主人公専用）。五系統を扱う。灯心に火のともる油つぼの紋', RING_FLAME, F_FIRE, LAMP, omap={'O': 'r', 'T': 'r'})


@icon('job', 'star', '熟練度の星|ジョブ熟練度（☆1〜15）を数える金の星。ジョブ画面の☆表示用')
def _():
    c = Canvas()
    pts = []
    for i in range(10):
        r = 7.0 if i % 2 == 0 else 3.0
        a = math.radians(-90 + i * 36)
        pts.append((8 + r * math.cos(a), 8.6 + r * math.sin(a)))
    c.poly(pts, 'H')
    for y in range(16):
        for x in range(8):
            if c.g[y][x] == 'H':
                c.g[y][x] = 'G'
    for y in range(16):
        for x in range(16):
            if c.g[y][x] == 'G' and x + y > 17 and x >= 6:
                c.g[y][x] = 'H'
    c.pts('J', (11, 12), (10, 12), (12, 12), (11, 11))
    return c
