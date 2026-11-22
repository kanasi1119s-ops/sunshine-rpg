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
def base(dy=0, sway=0, bx=0, body=None):
    body = body or BODY
    """dy: くつ以外（頭・かみ・胴・うで・スカート）を下げるマス数。足はその分だけスカートにかくれる。sway: 縦ロールの下半分とあほ毛を左右にずらすマス数（-1・0・1）"""
    g = [["."] * W for _ in range(H)]
    def put(x, y, ch):
        x += OX
        if ch != "." and 0 <= x < W and 0 <= y + OY < H: g[y + OY][x] = ch
    for x0, rows in ((0, LD), (19, RD)):
        for i, r in enumerate(rows):
            for j, ch in enumerate(r): put(x0 + j + bx + (sway if i >= 6 else 0), 5 + i + dy, ch)
    for y, (x0, r) in LOW.items():
        for j, ch in enumerate(r): put(x0 + j, y, ch)
    for (sx, sy), ch in skirt().items(): g[sy + OY + dy][sx + OX + bx + (sway if sy >= 25 else 0)] = ch   # すその方（下半分）は、かみと同じようにおくれてゆれる      # スカートも体といっしょに下がる（足はひざを曲げた分だけ短く見える）
    for i, r in enumerate(HEAD):
        for j, ch in enumerate(r): put(6 + j + bx + (sway if i == 0 else 0), i + dy, ch)
    for i, r in enumerate(body):
        for j, ch in enumerate(r): put(5 + j + bx, 13 + i + dy, ch)
    for y, r in RIB.items():
        for j, ch in enumerate(r): put(18 + j + bx, y + dy, ch)
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
# 動き4つ × 口と目7つ = 28コマ。足（くつ）は動かさない。
# 動き: 0 まん中・上／1 右へ1マス・1マス下（かみの先はおくれて元の所に残る）／2 まん中・上／3 左へ1マス・1マス下
POSES = [("まん中", 0, 0, 0, BODY), ("右・下", 1, -1, 1, BODY_L), ("まん中2", 0, 0, 0, BODY), ("左・下", 1, 1, -1, BODY_R)]
FACES = [("とじる", "closed", False), ("あ", "a", False), ("い", "i", False), ("う", "u", False), ("え", "e", False), ("お", "o", False), ("まばたき", "closed", True)]
FRAME_GRIDS = []
for pn, dy, sw, bx, bd in POSES:
    for fn, m, bl in FACES:
        g = base(dy, sw, bx, bd)
        for (x, y), ch in face(m, bl, dy, bx).items(): g[y][x] = ch
        FRAME_GRIDS.append((pn + "・" + fn, 150, g))
COLS = len(FACES)
