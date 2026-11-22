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
HEAD = [".....45.....", "..34542.Nw.w", ".3456543wNnN", "345625443N32", "354653245432", "243542324531",
        "232c32c32321", "232XXccXX221", "132vebbev221", "122wfaafw221", "122paccap121", ".21cbbbbc12.", ".1..dccd..1.",
        ".MLwvwvwvNn.", "MLnN4324NnNn", "MLnML33NnnNn", "MNnMNyNNnnNn", "MNnLNNNNnnNn", "vwnMNyNnnnwu", "bcnwvwvwunbc", "cd.TSRSRr.cd"]
RIB = {1: "N", 2: "w"}
LOW = {21: (8, "TSSRSSRr"), 22: (7, "TTSRSTSRRr"), 23: (6, "kKIKkJKkKIkk"), 24: (5, "STSSRSTSRSSRRr"), 25: (4, "STTSRSSTSRRSTSRr"),
       26: (2, "kIKkKIKkKJKkKIKkKJkk"), 27: (3, "k.vw.wv.wvw.wv.w.k"),
       28: (7, "cbd....cbd"), 29: (7, "vwu....vwu"), 30: (7, "wwu....wwu"), 31: (7, "wvu....wvu"), 32: (7, "wvu....wvu"), 33: (7, "vuU....vuU"),
       34: (6, "kJIk....kIJk"), 35: (6, "KJKk....kKJK"), 36: (6, "kkkk....kkkk")}
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
    stamp({i: (6, r) for i, r in enumerate(HEAD)}); stamp({y: (18, r) for y, r in RIB.items()}); stamp(LOW)
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
