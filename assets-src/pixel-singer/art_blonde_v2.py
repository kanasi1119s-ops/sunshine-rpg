"""金髪ショートの歌い手（第2版）の絵の設計（どのマスに何色を置くか）。エディタに打ちこむのは editor_drive.py。
2026-11-27 人間が用意した絵（金色の短いくせ毛・赤いヘアバンド・白い半そでシャツ・赤いチェックのスカーフ・デニムのショートパンツ・茶色のブーツ）をもとに、
縦ロールの歌い手（art_24x40_v24.py）と同じ大きさ（横26×縦40）・同じコマ（動き16 × 口と目7＝112コマ）で作る。"""
import math
PAL = [("X", "ふち", "#1a0e14"), ("1", "かみ1", "#7a4a14"), ("2", "かみ2", "#b47a22"), ("3", "かみ3", "#dca63a"), ("4", "かみ4", "#f4c95c"), ("5", "かみ5", "#ffe48c"), ("6", "かみ光", "#fff6cc"),
       ("a", "はだ光", "#fff0e2"), ("b", "はだ", "#ffd9c0"), ("c", "はだ影", "#e8a888"), ("d", "はだ暗", "#b06c58"), ("p", "ほほ", "#ffb0a8"),
       ("e", "目暗", "#143c80"), ("f", "目", "#3c94e8"), ("w", "白", "#ffffff"), ("v", "白影1", "#d6dbe8"), ("u", "白影2", "#9aa4bc"),
       ("n", "デニム暗", "#18223c"), ("N", "デニム", "#2c4470"), ("M", "デニム明", "#4a6c9e"), ("L", "デニム光", "#8aaad2"),
       ("o", "茶暗", "#2e1c14"), ("O", "茶", "#5a3a26"), ("Q", "茶明", "#8a5e3c"), ("y", "金具", "#d8c890"),
       ("m", "口", "#5a1018"), ("t", "舌", "#ff8a94"),
       ("r", "赤暗", "#6a0e18"), ("R", "赤影", "#9a1822"), ("S", "赤", "#cc2a30"), ("T", "赤明", "#f05a50")]
W, H = 26, 40; OX = 1; OY = 1
# 頭（x5 から14マス）。短いくせ毛: てっぺんは丸く、ヘアバンドの下で前髪が束になり、えりあしの毛先が外へはねる
HEAD = ["....344443....", "..3455655432..", ".34565545543 .".replace(" ", "2"), "2STTTTTTTTSSR2", "34543545345432", "34534c43c43543",
        "2354cbccbc4532", "2343XXccXX3432", "1343vebbev3431", "1243wfaafw3421", "2342paccap2432", "3421cbbbbc1243", "342..dccd..243"]
# 体（x5 から14マス）: 首とスカーフ → 白い半そで → むき出しのうで → ベルト
BODY = ["....STccTS....", "..wwRSTSRSww..", ".wvwwRTSRwwvw.", ".bcvwSRwRSvcb.", ".bc.wwvwwv.cb.", ".bc.wvwwvu.cb.", ".ab.OQyQOo.ba.", ".cd........dc."]
# ショートパンツ（x5 から14マス、y20〜22）: すそはほつれて白っぽい
# 第2版（2026-11-27 人間「ホットパンツもう少し長くしましょう」）: 3段 → 5段。ももの中ほどまで
SHORTS = ["...NMMLNMMNn..", "..NMLMNnMMMNn.", "..NMMLNnMLMNn.", "..NMLMn.NMMNn.", "..vLvLn.LvLvn."]
L_STAND = {23: (8, "bbc"), 24: (8, "abc"), 25: (8, "bbc"), 26: (8, "bc"), 27: (8, "ac"), 28: (8, "bc"), 29: (8, "bc"), 30: (8, "bc"), 31: (8, "wv"), 32: (7, "OQo"), 33: (7, "OyO"), 34: (7, "OQo"), 35: (6, "QQOo"), 36: (6, "oooo")}
R_STAND = {23: (13, "cbb"), 24: (13, "cba"), 25: (13, "cbb"), 26: (14, "cb"), 27: (14, "ca"), 28: (14, "cb"), 29: (14, "cb"), 30: (14, "cb"), 31: (14, "vw"), 32: (14, "oQO"), 33: (14, "OyO"), 34: (14, "oQO"), 35: (14, "oOQQ"), 36: (14, "oooo")}
# 左足のつま先でリズムを取る形: かかとは床に付けたまま、つま先だけ1マス上げる
L_TAP = dict(L_STAND); L_TAP.update({34: (6, "QQOo"), 35: (7, "OOo"), 36: (8, "oo")})
def base(dy=0, off=None, legs=None):
    """dy: くつ以外を下げるマス数。off: 部分ごとの左右のずれ（-1・0・1）。head 頭／torso 体／tip 毛先"""
    o = dict(head=0, torso=0, tip=0); o.update(off or {}); legs = legs or (L_STAND, R_STAND)
    g = [["."] * W for _ in range(H)]
    def put(x, y, ch):
        x += OX
        if ch != "." and 0 <= x < W and 0 <= y + OY < H: g[y + OY][x] = ch
    for leg in legs:
        for y, (x0, r) in leg.items():
            for j, ch in enumerate(r): put(x0 + j, y + (dy if y < 31 else 0), ch)          # 足首から上は体といっしょにしずむ。くつは動かさない
    for i, r in enumerate(SHORTS):
        for j, ch in enumerate(r): put(5 + j + o["torso"], 20 + i + dy, ch)
    for i, r in enumerate(BODY):
        for j, ch in enumerate(r): put(5 + j + o["torso"], 13 + i + dy, ch)
    for i, r in enumerate(HEAD):
        for j, ch in enumerate(r):
            side = j < 4 or j > 9
            put(5 + j + (o["tip"] if i >= 10 and side else o["head"]), i + dy, ch)
    add = []
    for y in range(H):
        for x in range(W):
            if g[y][x] == ".":
                nb = [g[y + b][x + a] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + a < W and 0 <= y + b < H and g[y + b][x + a] != "."]
                if nb: add.append((x, y, "1" if any(c in "123456" for c in nb) and y < OY + 14 else "X"))
    for x, y, c in add: g[y][x] = c
    return g
def face(mouth, blink=False, dy=0, bx=0):
    M = {"closed": ["acca", "bbbb"], "a": ["mttm", "bmmb"], "i": ["mwwm", "bbbb"], "u": ["amma", "bbbb"], "e": ["mwwm", "bttb"], "o": ["amma", "bmmb"]}[mouth]
    E = ["cccccc", "bbbbbb", "XXaaXX"] if blink else ["XXccXX", "vebbev", "wfaafw"]
    d = {}
    for j, r in enumerate(M):
        for i, ch in enumerate(r): d[(10 + i + OX + bx, OY + 10 + j + dy)] = ch
    for j, r in enumerate(E):
        for i, ch in enumerate(r): d[(9 + i + OX + bx, OY + 7 + j + dy)] = ch
    return d
# 動き16 × 口と目7つ = 112コマ（縦ロールの歌い手と同じ動き: 体は左右3コマずつだけ1マス寄る／つま先を下ろす拍で1マスしずむ／毛先がおくれてゆれる／左足のつま先だけでリズム）
NP = 16
def _w(t, lag, th=0.5):
    v = math.sin(2 * math.pi * (t - lag) / NP); return 1 if v > th else -1 if v < -th else 0
POSES = []
for t in range(NP):
    _b = _w(t, 0, 0.8); off = dict(torso=_b, head=_b, tip=_w(t, 2.5, 0.5))
    dy = 1 if t in (4, 5, 12, 13) else 0
    legs = (L_TAP, R_STAND) if t in (0, 1, 2, 3, 8, 9, 10, 11) else (L_STAND, R_STAND)
    POSES.append(("動き%d" % (t + 1), dy, off, legs))
FACES = [("とじる", "closed", False), ("あ", "a", False), ("い", "i", False), ("う", "u", False), ("え", "e", False), ("お", "o", False), ("まばたき", "closed", True)]
# 第2版（人間「まずは正面のドット絵だけにしましょう」）: 正面で立つ1コマだけ（動きと口の形は、絵が決まってから足す）
_g = base()
for (x, y), ch in face("closed").items(): _g[y][x] = ch
FRAME_GRIDS = [("正面", 400, _g)]
COLS = 1
