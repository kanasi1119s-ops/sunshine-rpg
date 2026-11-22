"""第5版の絵の設計（どのマスに何色を置くか）。エディタに打ちこむのは editor_drive.py。"""
PAL = [("X", "ふち", "#0c0612"), ("1", "かみ1", "#4a0a1a"), ("2", "かみ2", "#7a1022"), ("3", "かみ3", "#b01c2a"), ("4", "かみ4", "#d93a38"), ("5", "かみ5", "#f47460"), ("6", "かみ光", "#ffbe9e"),
       ("a", "はだ光", "#fff0e2"), ("b", "はだ", "#ffd9c0"), ("c", "はだ影", "#e0a080"), ("d", "はだ暗", "#a85c4c"), ("p", "ほほ", "#ffb0a8"),
       ("e", "目暗", "#0c3f4c"), ("f", "目", "#22a8a4"), ("w", "白", "#ffffff"), ("v", "白影1", "#d8d2e2"), ("u", "白影2", "#9a8fae"), ("U", "白影3", "#6a5f80"),
       ("n", "紺暗", "#0c1430"), ("N", "紺", "#1e2c58"), ("M", "紺明", "#34508c"), ("L", "紺光", "#6c8ccc"),
       ("k", "黒", "#181018"), ("K", "黒明1", "#362a3c"), ("J", "黒明2", "#5c4c64"), ("I", "黒光", "#8a7a92"),
       ("y", "金", "#f0c040"), ("m", "口", "#5a1018"), ("t", "舌", "#ff8a94"),
       ("r", "赤暗", "#5e0c18"), ("R", "赤影", "#8e1420"), ("S", "赤", "#c02030"), ("T", "赤明", "#e84a4c")]
W, H = 26, 40      # 左右にゆれる分、両がわに1マスずつ余白を足した（絵そのものは横24マス）
OX = 1
OY = 1
HEAD = [".....45.....", "..34542.Nw.w", ".3465243wNnN", "345625443N32", "354653245432", "243542324531",
        "232c32c32321", "232XXccXX221", "132vebbev221", "122wfaafw221", "122paccap121", ".21cbbbbc12.", ".1..dccd..1."]
# 体（x5 から14マス）。お手本の体つき: 細い胴（6マス→腰で4マス）、胴からはなした細いうで、手は腰の外
BODY = ["..MLwvwwvwNn..", "..MnN4324NnN..", "..LnMN33NnnN..", ".MNnMLyNNnnNn.", ".MN1nMNNNn1Nn.", ".wv1nMyNnn1vu.", "bc.1vwvwvu1.bc", "cd.TSRSTSRr.cd"]
# うでの形ちがい: 体がかたむくとき、おくれる方のうでを外へ1マス開き、手を1段上げる
BODY_L = ["..MLwvwwvwNn..", "..MnN4324NnN..", ".MLnMN33NnnN..", "MN.nMLyNNnnNn.", "wv.1nMNNNn1Nn.", "bc.1nMyNnn1vu.", "cd.1vwvwvu1.bc", "...TSRSTSRr.cd"]
BODY_R = ["..MLwvwwvwNn..", "..MnN4324NnN..", "..LnMN33NnnNn.", ".MNnMLyNNnn.Nn", ".MN1nMNNNn1.vu", ".wv1nMyNnn1.bc", "bc.1vwvwvu1.cd", "cd.TSRSTSRr..."]
# 足の形ちがい: ふつうに立つ／体重が反対の足にのって、かかとが1マスうき、足先が1マス内へ入る
L_STAND = {31: (8, "vU"), 32: (8, "wu"), 33: (8, "vU"), 34: (7, "kIk"), 35: (6, "IJKk"), 36: (6, "kkkk")}
L_LIFT = {31: (8, "vU"), 32: (9, "wu"), 33: (8, "kIk"), 34: (7, "IJKk"), 35: (7, "kkkk")}
R_STAND = {31: (14, "uU"), 32: (14, "vU"), 33: (14, "uU"), 34: (14, "kJk"), 35: (14, "kKJK"), 36: (14, "kkkk")}
R_LIFT = {31: (14, "uU"), 32: (13, "vU"), 33: (13, "kJk"), 34: (13, "kKJK"), 35: (13, "kkkk")}
# 足先でリズムを取る形: かかとは床に付けたまま、つま先だけ1マス上げる
L_TAP = {31: (8, "vU"), 32: (8, "wu"), 33: (8, "vU"), 34: (6, "IJIk"), 35: (7, "KKk"), 36: (8, "kk")}
RIB = {1: "N", 2: "w"}
# 足: 太もも1段 → くつ下の口（3マス）→ くつ下2段 → 細い足首 → くつ（ひも・こう・底）。段ごとに幅を変えて棒に見えないようにする
LOW = {31: (7, ".vU....uU."), 32: (7, ".wu....vU."), 33: (7, ".vU....uU."),
       34: (7, "kIk....kJk"), 35: (6, "IJKk....kKJK"), 36: (6, "kkkk....kkkk")}
# スカート: 少し上から見た形。すそと黒いフリルをゆるい弧にして（まん中が下・両はしが上）、ひだは腰から外へ広がる
def skirt():
    c = {}
    for x in range(1, 23):
        u = (x - 11.5) / 10.5; drop = round(2 * (1 - u * u)); hem = 27 + drop
        for y in range(20, hem + 2):
            hw = min(10.5, 4 + (y - 20) * 6.5 / 7)
            if abs(x - 11.5) > hw: continue
            t = (x - 11.5) / hw; ph = (t * 4.5) % 1
            if y == hem + 1:
                if x % 3 == 1 or abs(u) > 0.9: continue
                col = "w" if x % 3 == 2 else "v"
            elif y == hem or y == 23 + drop: col = "kKIKkJ"[x % 6] if t < 0.5 else "kKkJkk"[x % 6]
            else:
                col = "T" if ph < 0.3 else "S" if ph < 0.72 else "R"
                if t > 0.62: col = {"T": "S", "S": "R", "R": "r"}[col]
                if y == 24 + drop or (y == 20 and ph >= 0.3): col = {"T": "S", "S": "R", "R": "r", "r": "r"}[col]   # フリルの下とベルトの下のかげ
            c[(x, y)] = col
    return c
# 縦ロール: 丸い玉を重ねず、下へ細くなる1本のつつに、ななめの巻き線を入れる
def drill(mir):
    rows = []; wid = [3, 4] + [5] * 4 + [4] * 3 + [3] * 2 + [2] + [1]   # 長さは前の半分（13段）
    for i, w in enumerate(wid):
        x0 = {5: 0, 4: 1, 3: 1, 2: 2, 1: 2}[w] if not (i < 2) else (1 if w == 3 else 0)
        r = ["."] * 5
        for x in range(x0, x0 + w):
            xx = 4 - x if mir else x
            d = (i - [3, 3, 2, 2, 1][xx]) % 4; t = (1, 5, 4, 3)[d]
            if x in (x0, x0 + w - 1) and w > 2: t = max(1, t - 1)
            if d == 1 and x == x0 + 1 and not mir and w >= 4: t = 6
            if mir and d: t = max(2, t - 1)
            r[4 - x if mir and False else x] = str(t)
        rows.append("".join(r))
    return rows
LD = drill(False); RD = [r[::-1] for r in drill(True)]
import math
def base(dy=0, off=None, legs=None):
    """dy: くつ以外を下げるマス数。off: 部分ごとの左右のずれ（-1・0・1）。head 頭／torso 胸から上／d_mid 縦ロールの中ほど／d_tip 縦ロールの先／ahoge あほ毛／s_mid スカートの中ほど／s_hem すそ"""
    o = dict(head=0, torso=0, d_mid=0, d_tip=0, ahoge=0, s_mid=0, s_hem=0); o.update(off or {}); legs = legs or (L_STAND, R_STAND)
    g = [["."] * W for _ in range(H)]
    def put(x, y, ch):
        x += OX
        if ch != "." and 0 <= x < W and 0 <= y + OY < H: g[y + OY][x] = ch
    for x0, rows in ((0, LD), (19, RD)):
        for i, r in enumerate(rows):
            dx = o["head"] if i < 6 else o["d_mid"] if i < 10 else o["d_tip"]
            for j, ch in enumerate(r): put(x0 + j + dx, 5 + i + dy, ch)
    for leg in legs:
        for y, (x0, r) in leg.items():
            for j, ch in enumerate(r): put(x0 + j, y, ch)
    for (sx, sy), ch in skirt().items():
        g[sy + OY + dy][sx + OX + (o["s_hem"] if sy >= 26 else o["s_mid"] if sy >= 23 else 0)] = ch
    for i, r in enumerate(HEAD):
        for j, ch in enumerate(r): put(6 + j + (o["ahoge"] if i == 0 else o["head"]), i + dy, ch)
    for i, r in enumerate(BODY):
        for j, ch in enumerate(r): put(5 + j + (o["torso"] if i < 4 else 0), 13 + i + dy, ch)      # かたむくのは胸から上だけ。腰と手は動かさない
    for y, r in RIB.items():
        for j, ch in enumerate(r): put(18 + j + o["head"], y + dy, ch)
    add = []
    for y in range(H):
        for x in range(W):
            if g[y][x] == ".":
                nb = [g[y + b][x + a] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + a < W and 0 <= y + b < H and g[y + b][x + a] != "."]
                if nb: add.append((x, y, "1" if any(c in "123456" for c in nb) and y < OY + 26 else "X"))
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
# 動き16 × 口と目7つ = 112コマ。1マスより細かくは動かせないので、部分ごとに動き出すコマをずらして波のようにつなぐ:
# 胸 → 頭（1コマあと）→ 縦ロールの中ほど・スカートの中ほど（2コマあと）→ 縦ロールの先・あほ毛・すそ（3〜4コマあと）
NP = 16
def _w(t, lag, th=0.5):
    v = math.sin(2 * math.pi * (t - lag) / NP); return 1 if v > th else -1 if v < -th else 0
POSES = []
for t in range(NP):
    off = dict(torso=_w(t, 0, 0.6), head=_w(t, 1, 0.6), d_mid=_w(t, 2), s_mid=_w(t, 2, 0.7), d_tip=_w(t, 3.5, 0.35), ahoge=_w(t, 3), s_hem=_w(t, 3.5, 0.35))
    dy = 1 if t in (4, 5, 12, 13) else 0                                  # つま先を下ろす拍で1マスしずむ
    legs = (L_TAP, R_STAND) if t in (0, 1, 2, 3, 8, 9, 10, 11) else (L_STAND, R_STAND)   # 左足のつま先だけでリズムを取る。右足は動かさない
    POSES.append(("動き%d" % (t + 1), dy, off, legs))
FACES = [("とじる", "closed", False), ("あ", "a", False), ("い", "i", False), ("う", "u", False), ("え", "e", False), ("お", "o", False), ("まばたき", "closed", True)]
FRAME_GRIDS = []
for pn, dy, off, lg in POSES:
    for fn, m, bl in FACES:
        g = base(dy, off, lg)
        for (x, y), ch in face(m, bl, dy, off["head"]).items(): g[y][x] = ch
        FRAME_GRIDS.append((pn + "・" + fn, 100, g))
COLS = len(FACES)
