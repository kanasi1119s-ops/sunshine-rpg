"""第5版の絵の設計（どのマスに何色を置くか）。エディタに打ちこむのは editor_drive.py。"""
PAL = [("X", "ふち", "#0c0612"), ("1", "かみ1", "#4a0a1a"), ("2", "かみ2", "#7a1022"), ("3", "かみ3", "#b01c2a"), ("4", "かみ4", "#d93a38"), ("5", "かみ5", "#f47460"), ("6", "かみ光", "#ffbe9e"),
       ("a", "はだ光", "#fff0e2"), ("b", "はだ", "#ffd9c0"), ("c", "はだ影", "#e0a080"), ("d", "はだ暗", "#a85c4c"), ("p", "ほほ", "#ffb0a8"),
       ("e", "目暗", "#0c3f4c"), ("f", "目", "#22a8a4"), ("w", "白", "#ffffff"), ("v", "白影1", "#d8d2e2"), ("u", "白影2", "#9a8fae"), ("U", "白影3", "#6a5f80"),
       ("n", "紺暗", "#0c1430"), ("N", "紺", "#1e2c58"), ("M", "紺明", "#34508c"), ("L", "紺光", "#6c8ccc"),
       ("k", "黒", "#181018"), ("K", "黒明1", "#362a3c"), ("J", "黒明2", "#5c4c64"), ("I", "黒光", "#8a7a92"),
       ("y", "金", "#f0c040"), ("m", "口", "#5a1018"), ("t", "舌", "#ff8a94"),
       ("r", "赤暗", "#5e0c18"), ("R", "赤影", "#8e1420"), ("S", "赤", "#c02030"), ("T", "赤明", "#e84a4c")]
W, H = 24, 40
OY = 1
HEAD = [".....45.....", "..34542.Nw.w", ".3465243wNnN", "345625443N32", "354653245432", "243542324531",
        "232c32c32321", "232XXccXX221", "132vebbev221", "122wfaafw221", "122paccap121", ".21cbbbbc12.", ".1..dccd..1."]
# 体（x5 から14マス）。お手本の体つき: 細い胴（6マス→腰で4マス）、胴からはなした細いうで、手は腰の外
BODY = ["..MLwvwwvwNn..", "..MnN4324NnN..", "..LnMN33NnnN..", ".MNnMLyNNnnNn.", ".MN1nMNNNn1Nn.", ".wv1nMyNnn1vu.", "bc.1vwvwvu1.bc", "cd.TSRSTSRr.cd"]
RIB = {1: "N", 2: "w"}
# 足: 太もも1段 → くつ下の口（3マス）→ くつ下2段 → 細い足首 → くつ（ひも・こう・底）。段ごとに幅を変えて棒に見えないようにする
LOW = {29: (7, "cdrrrrrrcd"), 30: (6, "uvU......uuU"), 31: (6, "wvu......vvU"), 32: (6, "wvU......vuU"), 33: (7, "vU......uU"),
       34: (6, "kIk......kJk"), 35: (5, "IJKk......kKJK"), 36: (5, "kkkk......kkkk")}
# スカート: 少し上から見た形。すそと黒いフリルをゆるい弧にして（まん中が下・両はしが上）、ひだは腰から外へ広がる
def skirt():
    c = {}
    for x in range(1, 23):
        u = (x - 11.5) / 10.5; drop = round(2 * (1 - u * u)); hem = 25 + drop
        for y in range(20, hem + 2):
            hw = min(10.5, 4 + (y - 20) * 6.5 / 5)
            if abs(x - 11.5) > hw: continue
            t = (x - 11.5) / hw; ph = (t * 4.5) % 1
            if y == hem + 1:
                if x % 3 == 1 or abs(u) > 0.9: continue
                col = "w" if x % 3 == 2 else "v"
            elif y == hem or y == 22 + drop: col = "kKIKkJ"[x % 6] if t < 0.5 else "kKkJkk"[x % 6]
            else:
                col = "T" if ph < 0.3 else "S" if ph < 0.72 else "R"
                if t > 0.62: col = {"T": "S", "S": "R", "R": "r"}[col]
                if y == 23 + drop or (y == 20 and ph >= 0.3): col = {"T": "S", "S": "R", "R": "r", "r": "r"}[col]   # フリルの下とベルトの下のかげ
            c[(x, y)] = col
    return c
# 縦ロール: 丸い玉を重ねず、下へ細くなる1本のつつに、ななめの巻き線を入れる
def drill(mir):
    rows = []; wid = [3, 4] + [5] * 8 + [4] * 6 + [3] * 5 + [2] * 3 + [1]
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
def base():
    g = [["."] * W for _ in range(H)]
    def stamp(tbl):
        for y, (x0, s) in tbl.items():
            for i, ch in enumerate(s):
                if ch != ".": g[y + OY][x0 + i] = ch
    stamp({5 + i: (0, r) for i, r in enumerate(LD)}); stamp({5 + i: (19, r) for i, r in enumerate(RD)})
    stamp({i: (6, r) for i, r in enumerate(HEAD)}); stamp({13 + i: (5, r) for i, r in enumerate(BODY)}); stamp({y: (18, r) for y, r in RIB.items()}); stamp(LOW)
    for (sx, sy), ch in skirt().items(): g[sy + OY][sx] = ch
    add = []
    for y in range(H):
        for x in range(W):
            if g[y][x] == ".":
                nb = [g[y + dy][x + dx] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if 0 <= x + dx < W and 0 <= y + dy < H and g[y + dy][x + dx] != "."]
                if nb: add.append((x, y, "1" if any(c in "123456" for c in nb) and y < OY + 26 else "X"))
    for x, y, c in add: g[y][x] = c
    return g
def face(mouth, blink=False):
    M = {"closed": ["acca", "bbbb"], "a": ["mttm", "bmmb"], "i": ["mwwm", "bbbb"], "u": ["amma", "bbbb"], "e": ["mwwm", "bttb"], "o": ["amma", "bmmb"]}[mouth]
    E = ["cccccc", "bbbbbb", "XXaaXX"] if blink else ["XXccXX", "vebbev", "wfaafw"]
    d = {}
    for j, r in enumerate(M):
        for i, ch in enumerate(r): d[(10 + i, OY + 10 + j)] = ch
    for j, r in enumerate(E):
        for i, ch in enumerate(r): d[(9 + i, OY + 7 + j)] = ch
    return d
FRAMES = [("とじる", 400, face("closed")), ("あ", 200, face("a")), ("い", 200, face("i")), ("う", 200, face("u")), ("え", 200, face("e")), ("お", 200, face("o")), ("まばたき", 150, face("closed", True))]
