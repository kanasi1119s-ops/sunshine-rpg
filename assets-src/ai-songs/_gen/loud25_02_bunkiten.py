# ラウドロック25曲 2曲目「白い分岐点」（仮）。インスト（歌は後日）
# 人間（2026-10-22）「ドラムプログレ風いい音だしてる。これ大事にしてほしい。一音一音崩れてない。これ使って、ラウドロック作ってみて。BPM110で」
# ドラムは assets-src/ai-songs/drum-refs/prog100-naked.json の叩き方（3・3・2 のキック、ライドのベル、5つずつのかたまり、リニアのフィル、3連のタム下り）と
# 同じ設定（--drums naked・処理なし・trigger なし）を土台にする。旋律・進行は自作（既存曲の写しなし。CLAUDE.md 1-1）
# 書き出し: node tools/composer/song.mjs build <json> --wav --drums naked --bass bnb-loud --master -13.5 --widen 1.0
import json, sys, copy

BPM = 110
KEY = "E マイナー"

# ---------------- 形（小節数） ----------------
FORM = [("intro", 8), ("verse", 8), ("pre", 8), ("chorus", 16), ("inter", 8), ("verse2", 8), ("pre2", 4),
        ("chorus2", 16), ("bridge", 8), ("break", 4), ("chorus3", 16), ("outro", 4)]

# 小節ごとの根音と和音（ベース・リズムギター・分散和音が使う）
CH = {
    "intro":   ["E5"] * 8,
    "verse":   ["Em9", "Em9", "Cmaj7", "Cmaj7", "Am9", "Am9", "Bsus4", "B7"],
    "pre":     ["C", "C", "D", "D", "Em", "Em", "B7sus4", "B7"],
    "chorus":  ["C", "C", "D", "D", "Bm", "Bm", "Em", "Em", "C", "C", "D", "D", "F", "F", "B", "B"],
    "inter":   ["E5"] * 8,
    "verse2":  ["Em9", "Em9", "Cmaj7", "Cmaj7", "Am9", "Am9", "Bsus4", "B7"],
    "pre2":    ["C", "D", "B7sus4", "B7"],
    "chorus2": ["C", "C", "D", "D", "Bm", "Bm", "Em", "Em", "C", "C", "D", "D", "F", "F", "B", "B"],
    "bridge":  ["Am9", "Am9", "G", "G", "D/F#", "D/F#", "B7", "B7"],
    "break":   ["E5"] * 4,
    "chorus3": ["C", "C", "D", "D", "Bm", "Bm", "Em", "Em", "C", "C", "D", "D", "F", "F", "B", "E5"],
    "outro":   ["E5"] * 4,
}
ROOT = {"E5": "E", "Em9": "E", "Em": "E", "Cmaj7": "C", "C": "C", "Am9": "A", "Bsus4": "B", "B7": "B", "B7sus4": "B",
        "D": "D", "Bm": "B", "F": "F", "B": "B", "G": "G", "F#m7b5": "F#", "D/F#": "F#"}
TONES = {  # 分散和音の音（低い方から）
    "Em9": ["E3", "B3", "D4", "F#4", "G4"], "Cmaj7": ["C3", "G3", "E4", "G4", "B4"], "Am9": ["A2", "E3", "G3", "B3", "C4"],
    "Bsus4": ["B2", "F#3", "B3", "E4", "F#4"], "B7": ["B2", "F#3", "A3", "D#4", "F#4"], "G": ["G2", "D3", "G3", "B3", "D4"],
    "F#m7b5": ["F#2", "C3", "E3", "A3", "C4"], "D/F#": ["F#2", "A2", "D3", "F#3", "A3"],
}
BASS_LOW = {"E": "E1", "C": "C2", "A": "A1", "B": "B1", "D": "D2", "F": "F1", "G": "G1", "F#": "F#1"}
GTR_LOW = {"E": "E2", "C": "C3", "A": "A2", "B": "B2", "D": "D3", "F": "F2", "G": "G2", "F#": "F#2"}

def up(note, n):
    """音名を n オクターブ上げる"""
    i = len(note) - 1
    while note[i].isdigit() or note[i] == "-": i -= 1
    return note[:i + 1] + str(int(note[i + 1:]) + n)

def beats(tok):
    return float(tok.split(":")[1].rstrip("!,'^/\\_~"))

def bar(*toks):
    """1小節の音（拍の合計が4になることを確かめる）"""
    t = " ".join(toks).split()
    s = sum(beats(x) for x in t)
    assert abs(s - 4) < 1e-3, (toks, s)
    return " ".join(t)

REST = "R:4"
SECS = []
for name, n in FORM:
    SECS += [(name, i) for i in range(n)]
NB = len(SECS)

# ---------------- ドラム（1文字＝16分） ----------------
# 小節ごとに kick・snare・hihat のグリッド、tom と cym（crash パートの音名）の音符を決める。8小節ごとに必ず変化、4・8 小節目にフィル
K332 = "X..x..X.X..x..x."
def drums_for(name, i, n):
    last = i == n - 1
    k = s = h = "................"
    tom = REST
    cym = REST
    if name in ("intro", "inter", "outro"):
        # 看板リフと同じ 3・3・2。ライドのベルはかたまりの頭（0・3・6 拍目の16分＝0,6,12 マス）
        k = "X..X..X.X..X..X." if i % 2 == 0 else "X..X..X.X..X.xX."
        s = "....X.......X..." if i % 4 != 3 else "....X..o..X.X.oX"
        cym = "F2:0.75! F2:0.75 D2:0.5 F2:0.75! F2:0.75 D2:0.5" if i % 4 != 0 else "C2:1.5! F2:1.5! D2:0.5 D2:0.5"
        if name == "intro" and i < 2:   # 頭の2小節はキックとベルだけで、静かに入る
            s = "................"; cym = "F2:0.75 F2:0.75 D2:0.5 F2:0.75 F2:0.75 D2:0.5"
        if name == "outro" and last:
            k = "X..............."; s = "X..............."; cym = "C2:4!";
        elif last and name != "outro":
            # 3連16分でタムを下る（2拍）
            k = "X..X..X........."; s = "....X..........."
            cym = "F2:0.75! D2:0.75 F2:0.5! R:2"
            tom = "R:2 A3:0.1667 A3:0.1667, A3:0.1667 F3:0.1667 F3:0.1667, F3:0.1667 D3:0.1667 D3:0.1667, D3:0.1667 A2:0.1667 A2:0.1667 A2:0.1667!"
    elif name in ("verse", "verse2"):
        # ハイハット（verse2 はライド）・キックはまばらにずらす・スネアの間にゴースト
        kp = ["X......X..X.....", "X.....X...X..X..", "X......X..X.....", "X..X......X....."]
        sp = ["....X..o.o..X...", "..o.X.......X..o", "....X..o....X.o.", "....X..o.o..X..."]
        k = kp[i % 4]; s = sp[i % 4]
        if name == "verse":
            h = "X.x.X.x.X.x.X.x." if i % 2 == 0 else "X.x.X.o.X.x.X.xh"
        else:
            cym = "D2:0.5! D2:0.5 F2:0.5! D2:0.5 D2:0.5! D2:0.5 F2:0.5! D2:0.5"
        if i == 0:
            cym = "C2:1! " + ("D2:0.5 D2:0.5 F2:0.5! D2:0.5 D2:0.5! D2:0.5" if name == "verse2" else "R:3")
            if name == "verse": h = "..x.X.x.X.x.X.x."
        if i == 3:   # 4小節目: スネアをずらした小節
            s = "...o..X.o..o..X."; k = "X.....x..x..x..."
        if last:     # リニアのフィル（手と足が重ならない）
            k = "X..........x..x."; s = "..X..x..X......."; h = "................"
            if name == "verse2": cym = "D2:0.5! D2:0.5 D2:0.5 D2:0.5 R:2"
            tom = "R:2.5 A3:0.25 A3:0.25, F3:0.25 F3:0.25, D3:0.25 A2:0.25!"
    elif name in ("pre", "pre2"):
        # 5つずつのかたまり（2小節で 4/4 にもどる）。ハイハットは16分で積み上げる
        k = "X....x....x....x" if i % 2 == 0 else "....x....X....x."
        s = "........X......." if i % 2 == 0 else "o.......X..o..o."
        h = "x.x.xox.x.x.xox." if i < n - 2 else "x.xxxox.x.xxxxX."
        if i == 0: cym = "B2:2! R:2"; h = "." + h[1:]
        if last:     # 最後は止める（4拍目を全員休む）
            k = "X.x.X.x.X......."; s = "X.x.X.x.X......."; h = "................"
            tom = "R:2 A3:0.25! F3:0.25! D3:0.25! A2:0.25! R:1"
    elif name in ("chorus", "chorus2", "chorus3"):
        half = name == "chorus3" and i < 4
        if half:     # ラストのサビの頭4小節はハーフ（スネアは3拍目）
            k = "X.......X.x....."; s = "........X......."
            cym = "C2:2! D2:1 D2:1" if i == 0 else "D2:1! D2:1 F2:1! D2:1"
        else:
            kp = ["X.x...X.X.x...x.", "X.x...X.X...X.x.", "X.x...X.X.x...x.", "X...X.X.X.x.X..."]
            k = kp[i % 4]
            s = "....X.......X..." if i % 4 != 3 else "....X..o....X.oo"
            h = "X.X.X.X.X.X.X.X." if i % 8 < 4 else "................"
            cym = REST if i % 8 < 4 else "D2:0.5! D2:0.5 F2:0.5! D2:0.5 D2:0.5! D2:0.5 F2:0.5! D2:0.5"
            if i % 4 == 0 and h[0] != ".": h = "." + h[1:]   # クラッシュを叩く右手は、その瞬間ハイハットを叩けない
            if i % 4 == 0: cym = ("C2:1! " if i % 8 == 0 else "G2:1! ") + ("D2:0.5 D2:0.5 F2:0.5! D2:0.5 D2:0.5 D2:0.5" if i % 8 >= 4 else "R:3")
            if name == "chorus2" and i in (12, 13):   # 2回目のサビだけ、2小節ツーバス
                k = "XxXxXxXxXxXxXxXx"
        if i in (7, 15) and not (name == "chorus3" and i == 15):
            # 8小節目と16小節目: 3連のタム下り
            k = "X.x...X........."; s = "....X..........."; h = "................"
            if i % 8 >= 4: cym = "D2:0.5! D2:0.5 D2:0.5 D2:0.5 R:2"
            tom = "R:2 C4:0.1667 C4:0.1667, A3:0.1667 A3:0.1667 F3:0.1667, F3:0.1667 D3:0.1667 D3:0.1667, A2:0.1667 A2:0.1667 A2:0.1667 A2:0.1667!"
        if name == "chorus3" and last:
            k = "X..............."; s = "X..............."; h = "................"; cym = "C2:4!"
    elif name == "bridge":
        # 静かに: ライドのベルとフロアタム、キックは小さく
        k = "X.......x......." if i % 2 == 0 else "X.....x........."
        s = "................" if i < 4 else "........o......."
        cym = "F2:1 D2:1 F2:1 D2:1" if i < 4 else "F2:1! D2:0.5 D2:0.5 F2:1! D2:0.5 D2:0.5"
        tom = "R:3 A2:1," if i % 2 == 1 else REST
        if last:
            tom = "R:1 A3:0.25 A3:0.25 F3:0.25 F3:0.25 D3:0.25 D3:0.25 A2:0.25 A2:0.25 A2:0.25! A2:0.25! A2:0.25! A2:0.25!"
            cym = "D2:1 R:3"
    elif name == "break":
        # ブレイク: キック・スネア・チャイナをそろえた一撃（3・3・2）と休み
        k = "X..X..X........." if i < n - 1 else "X..X..X.X..X..X."
        s = "X..X..X........." if i < n - 1 else "X..X..X.X..X..X."
        cym = "B2:0.75! B3:0.75! B2:2.5!" if i < n - 1 else "B2:0.75! B3:0.75! B2:0.5! B3:0.75! B2:0.75! B3:0.5!"
    return k, s, h, tom, cym

KICK, SN, HH, TOM, CYM = [], [], [], [], []
from collections import Counter
cnt = Counter(n for n, _ in FORM)
for name, n in FORM:
    for i in range(n):
        k, s, h, tom, cym = drums_for(name, i, n)
        for g in (k, s, h): assert len(g) == 16, (name, i, g)
        KICK.append(k); SN.append(s); HH.append(h); TOM.append(bar(tom)); CYM.append(bar(cym))

# ---------------- 看板リフ（3・3・2。刻みではなく、オクターブの跳びと単音） ----------------
RIFF = [
    bar("E2:0.75! E3:0.75 G3:0.5", "E2:0.75! D3:0.75 B2:0.5"),
    bar("E2:0.75! E3:0.75 A3:0.5", "E2:0.75! G3:0.75 F#3:0.5"),
    bar("E2:0.75! E3:0.75 G3:0.5", "E2:0.75! D3:0.75 B2:0.5"),
    bar("C3:0.75! C4:0.75 B3:0.5", "B2:0.75! A3:0.75 F#3:0.5"),
]
RIFF_HI = [bar(*[(" ".join(up(x.split(":")[0], 1) + ":" + x.split(":", 1)[1] for x in r.split()))]) for r in RIFF]

# ---------------- 旋律（サビ・ブリッジだけ。歌うように、息つぎを入れる） ----------------
CHORUS_MEL = [
    bar("R:0.5 E5:0.5 D5:0.5 E5:0.5 G5:2!"),
    bar("E5:1 D5:0.5 B4:0.5 C5:2"),
    bar("R:0.5 F#5:0.5 E5:0.5 F#5:0.5 A5:2!"),
    bar("F#5:1 E5:0.5 D5:0.5 E5:2"),
    bar("R:0.5 D5:0.5 E5:0.5 F#5:0.5 A5:2!^^"),
    bar("R:1.5 F#5:0.5 D5:2"),
    bar("E5:3! G5:0.5 F#5:0.5"),
    bar("E5:2 R:2"),
    bar("R:0.5 E5:0.5 D5:0.5 E5:0.5 G5:2!"),
    bar("E5:1 D5:0.5 B4:0.5 G5:2"),
    bar("R:0.5 F#5:0.5 E5:0.5 F#5:0.5 A5:2!"),
    bar("B5:1 A5:0.5 F#5:0.5 A5:2"),
    bar("R:0.5 A5:0.5 G5:0.5 A5:0.5 C6:2!"),
    bar("A5:1 G5:0.5 F5:0.5 A5:2"),
    bar("F#5:2! D#5:2"),
    bar("B4:2 R:2"),
]
BRIDGE_MEL = [bar("E5:4!"), bar("C5:2 D5:2"), bar("B4:4"), bar("R:2 G5:2!"), bar("A5:3 G5:0.5 F#5:0.5"), bar("D5:4"), bar("D#5:2! F#5:2"), bar("E5:2^^ R:2")]

def arp(chord, i):
    """分散和音（8分）。小節ごとに上がり方・下がり方を変える"""
    t = TONES[chord]
    pats = [[0, 1, 2, 3, 4, 3, 2, 1], [0, 2, 1, 3, 2, 4, 3, 1], [0, 1, 3, 2, 4, 2, 3, 1], [0, 2, 4, 3, 1, 3, 2, 4]]
    p = pats[i % 4]
    return bar(*[f"{t[j]}:0.5{'!' if n % 4 == 0 else ''}" for n, j in enumerate(p)])

# ---------------- パートを組み立てる ----------------
P = {r: [] for r in ["riff", "rhythm", "rhythm_in", "arp", "lead", "bass", "harm"]}
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    ch = CH[name][i]; r = ROOT[ch]
    last = i == n - 1
    # リフ
    if name in ("intro", "inter", "outro") and not (name == "outro" and last):
        rf = RIFF[i % 4] if not (name == "inter" and i >= 4) else RIFF_HI[i % 4]
        if last and name != "outro": rf = bar("E2:0.75! E3:0.75 G3:0.5", "R:2")
        P["riff"].append(rf)
    elif name == "break":
        P["riff"].append(bar("E2:0.75! E3:0.75 E2:2.5!") if i < n - 1 else bar("E2:0.75! E3:0.75 G3:0.5! E2:0.75! D3:0.75 B2:0.5!"))
    elif name == "outro" and last:
        P["riff"].append(bar("E2:4!"))
    else:
        P["riff"].append(REST)
    # リズムギター（刻まずに伸ばす。付点のアクセント）
    low = GTR_LOW[r]
    if name.startswith("chorus"):
        if name == "chorus3" and i < 4:
            P["rhythm"].append(bar(f"{low}:4!"))
        elif i in (7, 15):
            P["rhythm"].append(bar(f"{low}:1.5! {low}:0.5 R:2") if not (name == "chorus3" and i == 15) else bar("E2:4!"))
        else:
            P["rhythm"].append(bar(f"{low}:1.5! {low}:1.5 {low}:1"))
        P["rhythm_in"].append(P["rhythm"][-1] if not (name == "chorus3" and i < 4) else REST)
    elif name in ("pre", "pre2"):
        P["rhythm"].append(bar(f"{low}:2! {low}:2") if not last else bar(f"{low}:0.5! {low}:0.5 {low}:0.5 {low}:0.5 {low}:1! R:1"))
        P["rhythm_in"].append(REST)
    elif name == "verse" and i >= 4 or name == "verse2":
        P["rhythm"].append(bar(f"{low}:4") if not last else bar(f"{low}:2! R:2"))
        P["rhythm_in"].append(REST)
    elif name == "break":
        P["rhythm"].append(P["riff"][-1]); P["rhythm_in"].append(P["riff"][-1])
    else:
        P["rhythm"].append(REST); P["rhythm_in"].append(REST)
    # 分散和音（Aメロ・ブリッジ）
    if name in ("verse", "verse2", "bridge") and ch in TONES and not (last and name != "bridge"):
        P["arp"].append(arp(ch, i))
    else:
        P["arp"].append(REST)
    # 旋律
    if name.startswith("chorus"):
        m = CHORUS_MEL[i]
        # 2回目・3回目のサビは同じ4小節にしない（人間「単調になりやすい」）: 2回目はフックの終わりを変え、3回目の頭（ハーフ）は長い音で
        if name == "chorus2" and i in (0, 2, 8):
            m = {0: bar("R:0.5 E5:0.5 D5:0.5 E5:0.5 G5:1.5! A5:0.5"), 2: bar("R:0.5 F#5:0.5 E5:0.5 F#5:0.5 A5:1.5! B5:0.5"), 8: bar("R:0.5 E5:0.5 G5:0.5 E5:0.5 G5:2!")}[i]
        if name == "chorus3" and i < 4:
            m = [bar("G5:4!"), bar("E5:2 C5:2"), bar("A5:4!"), bar("F#5:2 D5:2")][i]
        if name == "chorus3" and i == 15: m = bar("E5:4!")
        P["lead"].append(m)
        # 2回目と3回目のサビは、3度下のハモりを入れる（和音の音から選ぶ代わりに、旋律の1オクターブ下を薄く）
        def low8(t):
            if t.startswith("R") or beats(t) < 1: return "R:" + t.split(":")[1].rstrip("!,'^/\\_~")
            return up(t.split(":")[0], -1) + ":" + t.split(":", 1)[1]
        P["harm"].append(" ".join(low8(t) for t in m.split()) if name != "chorus" else REST)
    elif name == "bridge":
        P["lead"].append(BRIDGE_MEL[i]); P["harm"].append(REST)
    else:
        P["lead"].append(REST); P["harm"].append(REST)
    # ベース（指弾き。明るくゴリッと。リフはユニゾン、Aメロは動く、サビは8分の根音にアクセントと経過音）
    b = BASS_LOW[r]
    if name in ("intro", "inter", "outro", "break"):
        src = RIFF[i % 4] if name in ("intro", "inter") and not last else P["riff"][-1]   # ベースは高い版のリフに付いていかない
        P["bass"].append(" ".join((up(t.split(":")[0], -1) + ":" + t.split(":", 1)[1]) if not t.startswith("R") else t for t in src.split()) if not (name == "intro" and i < 2) else bar("E1:4!") if i == 0 else bar("E1:2 E1:1.5 E1:0.5"))
    elif name in ("verse", "verse2"):
        b5 = {"E": "B1", "C": "G1", "A": "E2", "B": "F#2"}[r]
        P["bass"].append(bar(f"{b}:1.5! {b}:0.5 {b5}:1 {up(b,1)}:0.5 {b5}:0.5") if not last else bar(f"{b}:1! {b}:1 R:2"))
    elif name in ("pre", "pre2"):
        P["bass"].append(bar(" ".join([f"{b}:0.5{'!' if j % 2 == 0 else ''}" for j in range(8)])) if not last else bar(f"{b}:0.5! {b}:0.5 {b}:0.5 {b}:0.5 {b}:1! R:1"))
    elif name.startswith("chorus"):
        if name == "chorus3" and i < 4:
            P["bass"].append(bar(f"{b}:3! {b}:1"))
        elif i in (7, 15):
            P["bass"].append(bar(f"{b}:1.5! {b}:0.5 R:2") if not (name == "chorus3" and i == 15) else bar("E1:4!"))
        else:
            nxt = BASS_LOW[ROOT[CH[name][i + 1]]] if i + 1 < n else b
            NOTE = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
            iv = (NOTE[ROOT[CH[name][i + 1]]] - NOTE[r]) % 12 if i + 1 < n else 0
            FIFTH = {"E": "B1", "C": "G1", "A": "E2", "B": "F#2", "D": "A1", "F": "C2", "G": "D2", "F#": "C#2"}
            appr = FIFTH[r] if iv in (1, 6, 11) else (nxt if nxt != b else up(b, 1))
            P["bass"].append(bar(f"{b}:0.5! {b}:0.5 {b}:0.5 {up(b,1)}:0.5 {b}:0.5! {b}:0.5 {b}:0.5 {appr}:0.5"))
    elif name == "bridge":
        P["bass"].append(bar(f"{b}:4") if i % 2 == 0 else bar(f"{b}:2 {up(b,1)}:2"))
    else:
        P["bass"].append(REST)

# ---------------- 曲の JSON ----------------
LEAD_BASE = {"instrument": "distGuitar", "double": False, "noRestrike": True, "phrase": 8, "humanPitch": 0, "noScoop": True, "di": "emily", "chorus": 0,
             "amp": "namJVM", "ampDrive": 0.69, "ampGate": 10, "ampTight": 0.6, "ampTightHz": 150, "ampCabIr": "jd-greenback-4x12-01", "reverb": 0.12,
             "fx": [{"type": "eq", "low": -2, "mid": 2.5, "midHz": 1200, "high": 2}, {"type": "filter", "kind": "lowpass", "freq": 10000, "q": 0.7},
                    {"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.25}, {"type": "plate", "mix": 0.16}], "powerChord": False, "autoScoop": False}
def part(role, inst, notes, **kw):
    d = {"role": role, "instrument": inst, "notes": notes}; d.update(kw); return d

drum_ref = json.load(open(__file__.rsplit("/", 2)[0] + "/drum-refs/prog100-naked.json"))
dset = {p["instrument"]: {k: v for k, v in p.items() if k not in ("notes", "role", "instrument")} for p in drum_ref["parts"]}

parts = [
    part("看板リフ", "distGuitar", " ".join(P["riff"]), volume=0.11, pan=0, guitarTone="loud-mid", gainDb=-3, powerChord=False, ampDrive=0.44, fx=[{"type": "filter", "kind": "highpass", "freq": 85, "q": 0.7}, {"type": "eq", "low": 0, "mid": -5, "midHz": 320, "high": 0}, {"type": "eq", "low": 0, "mid": 2.5, "midHz": 1500, "high": 0}, {"type": "eq", "low": 0, "mid": 2, "midHz": 3500, "high": 4}, {"type": "plate", "mix": 0.08}]),
    part("看板リフ（透明感の層）", "distGuitar", " ".join(P["riff"]), **{**LEAD_BASE, "volume": 0.07, "pan": 0, "ampDrive": 0.18, "phrase": None, "reverb": 0.1, "fx": [{"type": "filter", "kind": "highpass", "freq": 140, "q": 0.7}, {"type": "eq", "low": -3, "mid": -3, "midHz": 400, "high": 3}, {"type": "plate", "mix": 0.12}]}),
    part("リズム（左右）", "distGuitar", " ".join(P["rhythm"]), volume=0.1, pan=0, guitarTone="loud-mid", gainDb=-5, ampDrive=0.44, fx=[{"type": "eq", "low": 0, "mid": -3.5, "midHz": 300, "high": 0}, {"type": "eq", "low": 0, "mid": 2.5, "midHz": 1500, "high": 0}, {"type": "eq", "low": 0, "mid": 2, "midHz": 3200, "high": 3}]),
    part("リズム（内側の2本）", "distGuitar", " ".join(P["rhythm_in"]), volume=0.1, pan=0, guitarTone="loud-mid-hs", gainDb=-10, ampDrive=0.44, fx=[{"type": "eq", "low": 0, "mid": -3.5, "midHz": 300, "high": 0}, {"type": "eq", "low": 0, "mid": 2.5, "midHz": 1500, "high": 0}, {"type": "eq", "low": 0, "mid": 2, "midHz": 3200, "high": 3}]),
    part("分散和音のギター", "distGuitar", " ".join(P["arp"]), **{**LEAD_BASE, "volume": 0.1, "pan": -0.2, "ampDrive": 0.34, "phrase": None,
         "fx": [{"type": "eq", "low": -3, "mid": 1.5, "midHz": 1000, "high": 1.5}, {"type": "filter", "kind": "lowpass", "freq": 9500, "q": 0.7},
                {"type": "delay", "beats": 0.75, "mix": 0.22, "feedback": 0.35}, {"type": "plate", "mix": 0.24}]}),
    part("リード（旋律）", "distGuitar", " ".join(P["lead"]), **{**LEAD_BASE, "volume": 0.13, "pan": -0.05}),
    part("リード（オクターブ下）", "distGuitar", " ".join(P["harm"]), **{**LEAD_BASE, "volume": 0.07, "pan": 0.3}),
    part("ベース", "bass", " ".join(P["bass"]), volume=0.15, pan=0, amp="bassSplit", ampDrive=0.6, duck=0.2,
         fx=[{"type": "eq", "low": 0, "mid": 3, "midHz": 2200, "high": 2}]),
    part("キック", "kick", "g:" + "".join(KICK), **dset["kick"]),
    part("スネア", "snare", "g:" + "".join(SN), **dset["snare"]),
    part("ハイハット", "hihat", "g:" + "".join(HH), **dset["hihat"]),
    part("タム", "tom", " ".join(TOM), **dset["tom"]),
    part("シンバル", "crash", " ".join(CYM), **dset["crash"]),
]
for p in parts:
    if p.get("phrase") is None: p.pop("phrase", None)
    tot = sum(beats(t) for t in p["notes"].split()) if not p["notes"].startswith("g:") else (len(p["notes"]) - 2) / 4
    assert abs(tot - NB * 4) < 0.05, (p["role"], tot, NB * 4)

song = {
    "title": "白い分岐点（仮）",
    "description": f"仮: ラウドロック25曲の2曲目。インスト（歌は後日）。{KEY}・{BPM}。人間が気に入ったプログレ風のドラム（Naked Drums の素直な版）の叩き方を土台に、3・3・2 の看板リフ、5つずつのかたまりの Bメロ、サビの終わりに借用の F（♭II）で光が差す。自作",
    "bpm": BPM, "beats": 4, "barsPerChord": 1, "repeats": 1, "autoAccompaniment": False, "feel": "rock", "tone": "metal", "dynamics": "natural",
    "human": 0.35, "humanProfile": "role", "humanDist": "triangle",
    "diGuitar": "emily", "autoScoop": False, "guitarWobble": False,
    "drumMix": {"kick": {"level": 1.0}, "crash": {"level": 0.9}, "snare": {"level": 1.0}},
    "chords": " ".join({"E5": "Em", "D/F#": "D/F#"}.get(CH[n][i], CH[n][i]) for n, i in SECS),
    "sections": [{"kind": {"verse2": "verse", "pre2": "pre", "chorus2": "chorus", "chorus3": "chorus", "inter": "interlude"}.get(n, n), "bars": b} for n, b in FORM],
    "parts": parts,
}
if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lr/s2/bunkiten.json"
    import os; os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(song, open(out, "w"), ensure_ascii=False)
    print("小節", NB, "長さ", round(NB * 4 * 60 / BPM, 1), "秒", out)
