# 空を感じる疾走メタルコア（2026-10-21 人間「この組み合わせにシンセを入れて、空を感じる疾走感あるメタルコアを作ります。
#   スウィープやタッピング、ベースのジャズっぽさ、ツーバスを連打でドコドコずっとするのではなく、プログレッシブに入れてみましょう。」）
# 完全オリジナル（既存曲のメロディ・進行・リフは写さない）。
#   調: Aメロは B マイナー（ドロップB）、サビは D メジャーに開ける。サビの E メジャー（D から見て II の長三和音）で浮く響き（リディアン）。
#   刻み＝electro-rock（採用）、リード＝bmth-lead（採用）、スウィープとタッピング＝bmth-lead の乾いた版。シンセ＝16分のアルペジオ・パッド・サビの重ね・ライザー。
#   ベース＝ジャズベースの音源（--bass growly）で、半音の経過音・7th の分散和音・ゴースト・Cメロのウォーキング。
#   ツーバス＝連打を続けない。フレーズ終わりの短い連打、3+3+2 の区切り、ソロの山場の2小節だけ。
# 使い方: python3 sky_metalcore.py <出力.json>
#   書き出し: node tools/composer/song.mjs build <出力.json> --wav --drums muldjord --bass finger --piano salamander --master-preset rock-clean
import json, sys

out = sys.argv[1]
BPM = 172
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
FLAT = {"Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#", "Bb": "A#"}

def midi(n):
    """'F#4' → 66"""
    p, o = (n[:2], n[2:]) if len(n) > 2 and n[1] in "#b" else (n[:1], n[1:])
    p = FLAT.get(p, p)
    return NAMES.index(p) + (int(o) + 1) * 12
def name(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"

# コード: 根音とその上の音程（半音）
QUAL = {"": [0, 4, 7], "m": [0, 3, 7], "7": [0, 4, 7, 10], "m7": [0, 3, 7, 10], "maj7": [0, 4, 7, 11], "m9": [0, 3, 7, 10, 14],
        "sus4": [0, 5, 7], "13": [0, 4, 7, 10, 21], "add9": [0, 4, 7, 14]}
def chord(sym):
    r = sym[:2] if len(sym) > 1 and sym[1] in "#b" else sym[:1]
    q = sym[len(r):]
    return NAMES.index(FLAT.get(r, r)), QUAL[q], q
def simple(sym):  # 曲の chords 欄（解析用）に書ける形
    r, _, q = chord(sym)
    return NAMES[r] + {"m9": "m7", "13": "7", "add9": ""}.get(q, q)
def at_least(pc, low):  # low（midi）以上で最も低い、その音名の音
    m = low + ((pc - low) % 12)
    return m

# ── 構成（小節）とコード（1小節ずつ）──
SEC = [
    # 2026-10-21 人間「全弦解放で最初スタートするのはどうかな？」: ドロップBの全弦開放（B F# B E G# C#）を1回かき鳴らして2小節響かせ、ライザーで導入へ
    ("open", "全弦開放", 4, "Bsus4 Bsus4 Bsus4 Bsus4"),
    ("intro", "導入（シンセ）", 8, "Gmaj7 Gmaj7 Em9 Em9 Bm7 Bm7 Asus4 A"),
    ("introB", "導入（バンド・タッピング）", 8, "Bm Bm Gmaj7 Gmaj7 C C F#sus4 F#"),
    ("verse", "Aメロ", 16, "Bm Bm Gmaj7 Gmaj7 C C F# F# Bm Bm Gmaj7 Em7 C C F#sus4 F#"),
    ("pre", "Bメロ", 8, "Em7 Em7 F#m7 F#m7 Gmaj7 Gmaj7 A A"),
    ("chorus", "サビ", 16, "D D Em7 Em7 F#m7 F#m7 Gmaj7 Gmaj7 F#m7 Bm7 E E Gmaj7 Gmaj7 A A"),
    ("sweep", "間奏（スウィープ）", 8, "Bm Bm G G D D F# F#"),
    ("verse", "Aメロ2", 16, "Bm Bm Gmaj7 Gmaj7 C C F# F# Bm Bm Gmaj7 Em7 C C F#sus4 F#"),
    ("pre", "Bメロ2", 8, "Em7 Em7 F#m7 F#m7 Gmaj7 Gmaj7 A A"),
    ("chorus", "サビ2", 16, "D D Em7 Em7 F#m7 F#m7 Gmaj7 Gmaj7 F#m7 Bm7 E E Gmaj7 Gmaj7 A A"),
    ("bridge", "Cメロ（ベースが歌う）", 16, "Gmaj7 Gmaj7 F#m7 F#m7 Em9 Em9 A13 A13 Gmaj7 F#m7 Em9 A13 Bm7 Bm7 C C"),
    ("breakdown", "ブレイクダウン（3+3+2）", 8, "Bm Bm C C Bm Bm F# F#"),
    ("solo", "ソロ（スウィープ→タッピング）", 16, "Bm G D A Bm G D F# Em7 F#m7 Gmaj7 A Em7 F#m7 Gmaj7 A"),
    ("chorus", "最後のサビ（半音上げ）", 16, "D D Em7 Em7 F#m7 F#m7 Gmaj7 Gmaj7 F#m7 Bm7 E E Gmaj7 Gmaj7 A A"),
    ("outro", "終わり", 8, "D D Gmaj7 Gmaj7 Em9 Em9 D D"),
]
KIND = {"open": "intro", "intro": "intro", "introB": "intro", "verse": "verse", "pre": "pre", "chorus": "chorus", "sweep": "interlude",
        "bridge": "bridge", "breakdown": "break", "solo": "solo", "outro": "outro"}
BARS = []  # (section, chord, index_in_section, section_len, section_no)
for no, (sec, _, n, chs) in enumerate(SEC):
    cs = chs.split()
    assert len(cs) == n, (sec, len(cs), n)
    for k, c in enumerate(cs):
        BARS.append((sec, c, k, n, no))
NB = len(BARS)
CHORUS_NO = [no for no, s in enumerate(SEC) if s[0] == "chorus"]

def join(bars):
    for i, b in enumerate(bars):
        t = sum(float(x.split(":")[1].rstrip("!,'_~^/\\")) for x in b.split())
        assert abs(t - 4) < 1e-6, (i, BARS[i][:2], b, t)
    return " ".join(bars)

def gtr_root(c):  # 刻みの根音（ドロップB: B1〜A#2）
    return name(at_least(chord(c)[0], midi("B1")))
def bass_root(c):  # ベースの根音（B1〜A#2）
    return name(at_least(chord(c)[0], midi("B1")))
def nxt(i):
    return BARS[i + 1][1] if i + 1 < NB else BARS[i][1]

# ── 刻みのギター（electro-rock、左右の二重録り）──
def rhythm_bar(i):
    sec, c, k, n, no = BARS[i]
    r = gtr_root(c)
    if sec == "introB":
        # 顔のリフ: シンコペーションで和音を切り、4・8小節目は止めてタッピングを聞かせる
        if k % 4 == 3:
            return f"{r}:0.75! {r}:0.75! {r}:0.5! R:2"
        return f"{r}:0.75! {r}:0.75! {r}:0.5 R:0.5 {r}:0.5! {r}:0.25' {r}:0.25' {r}:0.5"
    if sec == "pre":
        if k < 4:
            return f"{r}:2! {r}:1 {r}:1"            # 伸ばして広げる
        if k < 7:
            return f"{r}:0.5! {r}:0.5 {r}:0.5 {r}:0.5 {r}:0.5! {r}:0.5 {r}:0.5 {r}:0.5"
        return f"{r}:0.5! {r}:0.5! {r}:0.5! {r}:0.5! {r}:1! R:1"   # 最後の拍で全員止める
    if sec == "chorus":
        # 疾走: 8分で前へ。2小節目ごとに伸ばして空を見せる
        if k % 2 == 0:
            return f"{r}:1.5! {r}:0.5 {r}:0.5 {r}:0.5 {r}:0.5! {r}:0.5"
        return f"{r}:0.5! {r}:0.5 {r}:0.5 {r}:0.5 {r}:2"
    if sec == "sweep":
        return f"{r}:2! {r}:2" if k % 2 == 0 else f"{r}:3 R:1"
    if sec == "bridge":
        if k < 12:
            return "R:4"
        return f"{r}:4" if k < 14 else f"{r}:1! {r}:1! {r}:0.5! {r}:0.5! {r}:0.5! {r}:0.5!"
    if sec == "breakdown":
        # 3+3+2（16分で 3・3・2・3・3・2）。キックと同じ位置
        return f"{r}:0.75! {r}:0.75! {r}:0.5! {r}:0.75! {r}:0.75! {r}:0.5!" if k % 2 == 0 else \
               f"{r}:0.75! {r}:0.75! {r}:0.5! R:0.5 {r}:0.25' {r}:0.25' {r}:0.5! {r}:0.5!"
    if sec == "solo":
        return f"{r}:0.5! {r}:0.5, {r}:0.5 {r}:0.5, {r}:0.5! {r}:0.5, {r}:0.5 {r}:0.5,"
    if sec == "outro":
        return f"{r}:4!" if k == 0 else "R:4"
    return "R:4"

# Aメロの刻み（ブリッジミュート。ギャロップと16分。4小節目ごとに開く）
def palm_bar(i):
    sec, c, k, n, no = BARS[i]
    if sec != "verse":
        return "R:4"
    r = gtr_root(c)
    if k % 4 == 3:
        return f"{r}:0.5! {r}:0.25' {r}:0.25' {r}:0.5! {r}:0.25' {r}:0.25' {r}:2"
    return f"{r}:0.5! {r}:0.25' {r}:0.25' {r}:0.5 {r}:0.25' {r}:0.25' R:0.5 {r}:0.25' {r}:0.25' {r}:0.5! {r}:0.25' {r}:0.25'"

# ── リード（bmth-lead）: サビの旋律、Aメロ2の合いの手、終わり ──
CHORUS_MELODY = [
    "F#5:1.5! E5:0.5 D5:1 A4:1", "B4:1 D5:1 E5:2",
    "G5:1.5! F#5:0.5 E5:1 D5:1", "B4:2 R:1 A4:0.5 B4:0.5",
    "C#5:1.5 E5:0.5 F#5:1 A5:1!", "A5:2 F#5:1 E5:1",
    "F#5:1.5! G5:0.5 F#5:1 D5:1", "B4:3 R:1",
    "A4:1 C#5:1 E5:1 F#5:1", "F#5:1.5 E5:0.5 D5:1 B4:1",
    "G#5:2! F#5:1 E5:1", "B5:3!^ R:1",
    "A5:1.5 G5:0.5 F#5:1 E5:1", "D5:2 F#5:2",
    "E5:1.5 F#5:0.5 G5:1 A5:1", "A5:2 E5:2",
]
# 2回目のサビ（リズムを変える）・最後のサビ（後半を高く）
VAR2 = {0: "F#5:1! F#5:0.5 E5:0.5 D5:1 A4:1", 2: "G5:1! G5:0.5 F#5:0.5 E5:1 D5:1", 8: "A4:0.5 C#5:0.5 E5:1 F#5:1 A5:1"}
VAR3 = {4: "C#5:1 E5:1 F#5:1.5 A5:0.5", 5: "B5:2! A5:1 F#5:1", 6: "G5:1.5! A5:0.5 F#5:1 D5:1", 8: "C#5:1 E5:1 F#5:1 A5:1!", 9: "B5:1.5! A5:0.5 F#5:1 D5:1", 10: "G#5:1.5! F#5:0.5 G#5:1 B5:1", 12: "B5:1.5! A5:0.5 G5:1 F#5:1"}
# Aメロ2の合いの手（4小節目ごとに2拍だけ）
VERSE_ANSWER = ["R:2 F#5:0.5 E5:0.5 D5:1", "R:2 A#4:0.5 C#5:0.5 F#5:1", "R:2 G5:0.5 F#5:0.5 E5:1", "R:2 C#5:0.5 E5:0.5 F#5:1"]
def lead_bar(i):
    sec, c, k, n, no = BARS[i]
    if sec == "chorus":
        m = CHORUS_MELODY[k]
        if no == CHORUS_NO[1] and k in VAR2:
            m = VAR2[k]
        if no == CHORUS_NO[-1] and k in VAR3:
            m = VAR3[k]
        if no == CHORUS_NO[-1] and k == 15:
            m = "A5:4!"
        return m
    if sec == "verse" and no != CHORUS_NO[0] - 2 and k % 4 == 3 and no > 3:
        return VERSE_ANSWER[(k // 4) % 4]
    if sec == "outro" and k < 4:
        return ["F#5:4", "E5:2 D5:2", "B4:4", "R:4"][k]
    return "R:4"

# ── スウィープとタッピング（bmth-lead の乾いた版）──
def triad(c):
    r, iv, q = chord(c)
    third = 3 if "m" in q and q != "maj7" else 4
    if q == "sus4":
        third = 5
    return r, third
def sweep_bar(c):
    r, third = triad(c)
    base = at_least(r, midi("E3"))
    # 2オクターブ駆け上がって下り、また上る（16分×16）。いちばん上は根音の2オクターブ上（E6 をこえない）
    seq = [base, base + third, base + 7, base + 12, base + 12 + third, base + 19, base + 24,
           base + 19, base + 12 + third, base + 12, base + 7, base + third, base, base + third, base + 7, base + 12]
    toks = [f"{name(m)}:0.25" + ("!" if j in (0, 6) else "_") for j, m in enumerate(seq)]
    return " ".join(toks)
TAP_POS = [0]
def tap_bar(c):
    # 3音ひと組（タップ→プル→プル）を 16分で回す。4拍の上で組の頭がずれていく
    r, third = triad(c)
    hi = at_least(r, midi("C#5")) + 7   # 5度上をタップ
    if hi > midi("E6"):
        hi -= 12
    grp = [hi, hi - 7 + third, hi - 7]  # 5度 → 3度 → 根音
    toks = []
    for _ in range(16):
        j = TAP_POS[0] % 3
        toks.append(f"{name(grp[j])}:0.25" + ("!" if j == 0 else "_"))
        TAP_POS[0] += 1
    return " ".join(toks)
def tech_bar(i):
    sec, c, k, n, no = BARS[i]
    if sec == "introB" and k % 4 != 3:
        return tap_bar(c)
    if sec == "introB":
        TAP_POS[0] = 0
        return "R:2 " + " ".join(f"{name(m)}:0.25" + ("!" if j == 0 else "_") for j, m in
                                 enumerate([midi(x) for x in ("B5", "A5", "F#5", "E5", "D5", "C#5", "B4", "A#4")]))
    if sec == "sweep":
        return sweep_bar(c) if k < 7 else "R:4"
    if sec == "solo":
        if k < 8:
            return sweep_bar(c)
        if k < 14:
            return tap_bar(c)
        if k == 14:
            return "E6:2!^^ D6:1 B5:1"  # 山場（チョーキング）
        return "R:4"
    return "R:4"

# ── ベース（ジャズっぽさ: 半音の経過音・7th の分散和音・ゴースト）──
def approach(i):
    nr = at_least(chord(nxt(i))[0], midi("B1"))
    cur = at_least(chord(BARS[i][1])[0], midi("B1"))
    m = (nr - 1 if nr > cur else nr + 1) if nr != cur else cur + 7
    return name(m - 12 if m > midi("D3") else m)
def bass_bar(i):
    sec, c, k, n, no = BARS[i]
    r, iv, q = chord(c)
    R = at_least(r, midi("B1"))
    cap = lambda m: name(m - 12 if m > midi("D3") else m)
    rn, fifth, octv = name(R), cap(R + 7), cap(R + 12)
    seventh = cap(R + (iv[3] if len(iv) > 3 and iv[3] < 12 else 12))
    third = cap(R + iv[1])
    ap = approach(i)
    if sec == "open":
        return f"{rn}:4!" if k == 0 else "R:4"
    if sec == "intro":
        return "R:4" if k < 4 else (f"{rn}:4" if k % 2 == 0 else f"{rn}:3 {ap}:1")
    if sec == "introB":
        if k % 4 == 3:
            return f"{rn}:0.75 {rn}:0.75 {rn}:0.5 R:2"
        return f"{rn}:0.75 {rn}:0.75 {rn}:0.5 R:0.5 {rn}:0.5 {octv}:0.25' {rn}:0.25, {fifth}:0.5"
    if sec == "verse":
        if k % 4 == 3:  # 開く小節: 7th の分散和音で歌う
            return f"{rn}:0.5 {third}:0.5 {fifth}:0.5 {seventh}:0.5 {octv}:1 {seventh}:0.5 {ap}:0.5"
        return f"{rn}:0.75 {rn}:0.25, {rn}:0.5 {fifth}:0.5 {rn}:0.5 {rn}:0.25, {octv}:0.25' {rn}:0.5 {ap}:0.5"
    if sec == "pre":
        if k < 4:
            return f"{rn}:1 {third}:1 {fifth}:1 {seventh}:1"
        if k < 7:
            return f"{rn}:0.5 {rn}:0.5 {octv}:0.5 {rn}:0.5 {fifth}:0.5 {rn}:0.5 {seventh}:0.5 {ap}:0.5"
        return f"{rn}:0.5 {rn}:0.5 {rn}:0.5 {rn}:0.5 {rn}:1 R:1"
    if sec == "chorus":
        if k % 2 == 0:
            return f"{rn}:1.5 {rn}:0.5 {rn}:0.5 {octv}:0.5 {rn}:0.5 {rn}:0.5"
        return f"{rn}:0.5 {rn}:0.5 {octv}:0.5 {rn}:0.5 {fifth}:1 {seventh}:0.5 {ap}:0.5"
    if sec == "sweep":
        return f"{rn}:2 {fifth}:1 {ap}:1"
    if sec == "bridge":
        # ウォーキング（4分）: 根音 → 3度 → 5度 → 次の根音への半音。後半は 8分で歌う
        if k < 8:
            return f"{rn}:1 {third}:1 {fifth}:1 {ap}:1"
        if k < 12:
            return f"{rn}:0.5 {fifth}:0.5 {seventh}:0.5 {octv}:0.5 {seventh}:0.5, {fifth}:0.5 {third}:0.5 {ap}:0.5"
        return f"{rn}:4" if k < 14 else f"{rn}:1 {rn}:1 {rn}:0.5 {rn}:0.5 {rn}:0.5 {rn}:0.5"
    if sec == "breakdown":
        return f"{rn}:0.75 {rn}:0.75 {rn}:0.5 {rn}:0.75 {rn}:0.75 {rn}:0.5" if k % 2 == 0 else \
               f"{rn}:0.75 {rn}:0.75 {rn}:0.5 R:0.5 {rn}:0.25 {rn}:0.25 {rn}:0.5 {ap}:0.5"
    if sec == "solo":
        return f"{rn}:0.5 {rn}:0.5 {fifth}:0.5 {rn}:0.5 {octv}:0.5 {rn}:0.5 {seventh}:0.5 {ap}:0.5"
    if sec == "outro":
        return f"{rn}:4" if k < 2 else "R:4"
    return "R:4"

# ── ベースの旋律（2026-10-21 人間「ベースは前の状態に戻そう（音色）。ベースでメロディラインをバッキバキに入れて欲しい」）──
#   音色はジャズベースの録音をやめ、ラウドロックの試験曲と同じ標準のベース＋bassSplit（歪みを少し）に戻す。
#   弾き方は、根音の刻みの合間に「次のコードへ駆け上がる／駆け下りる16分の音階」・オクターブの跳躍・5度と3度の歌う動きを入れる。
SCALE_PC = [11, 1, 2, 4, 6, 7, 9]   # B マイナー＝D メジャーの音（B C# D E F# G A）
LOW, HIGH = midi("B1"), midi("D3")
def scale_notes():
    return [m for m in range(LOW, HIGH + 1) if m % 12 in SCALE_PC]
SN = scale_notes()
def fold(m):
    while m > HIGH: m -= 12
    while m < LOW: m += 12
    return m
def run_to(target, n=4, up=None):
    """target（次の根音）へ音階で近づく n 音（16分）。up=True で下から上る"""
    t = min(SN, key=lambda x: abs(x - target))
    j = SN.index(t)
    if up is None:
        up = j - n >= 0 and (j + n >= len(SN) or j % 2 == 0)
    seq = [SN[max(0, min(len(SN) - 1, j - (n - q) if up else j + (n - q)))] for q in range(n)]
    return seq
def mel_bass_bar(i):
    sec, c, k, n, no = BARS[i]
    r, iv, q = chord(c)
    R = at_least(r, LOW)
    t3, t5, oc = fold(R + iv[1]), fold(R + 7), fold(R + 12)
    t7 = fold(R + (iv[3] if len(iv) > 3 and iv[3] < 12 else 10 if "m" in q else 11))
    nr = at_least(chord(nxt(i))[0], LOW)
    rn = name(R)
    run = " ".join(f"{name(m)}:0.25" + ("!" if q2 == 0 else "'") for q2, m in enumerate(run_to(nr)))
    if sec == "verse":
        if k % 2 == 0:
            return f"{rn}:0.5! {rn}:0.25' {rn}:0.25' {name(t5)}:0.5! {rn}:0.25' {rn}:0.25' {name(oc)}:0.5! {name(t7)}:0.25' {name(t5)}:0.25' {rn}:0.5 {name(t3)}:0.5"
        return f"{rn}:0.5! {rn}:0.25' {rn}:0.25' {name(t3)}:0.5 {name(t5)}:0.5! {name(oc)}:0.5 {rn}:0.5 " + run
    if sec == "pre":
        if k < 4:
            up = run_to(oc, 4, up=True)
            return f"{rn}:1! {name(t5)}:0.5 {name(oc)}:0.5! {name(t7)}:1 " + " ".join(f"{name(m)}:0.25'" for m in up)
        if k < 7:
            return f"{rn}:0.5! {name(oc)}:0.5' {rn}:0.5 {name(oc)}:0.5' {name(t5)}:0.5! {name(oc)}:0.5' " + " ".join(f"{name(m)}:0.25'" for m in run_to(nr, 2)) + f" {name(t3)}:0.5"
        return f"{rn}:0.5! {rn}:0.5! {rn}:0.5! {rn}:0.5! {rn}:1! R:1"
    if sec == "chorus":
        if k % 4 == 3:
            return f"{rn}:0.5! {name(oc)}:0.5 {name(t7)}:0.5 {name(t5)}:0.5 " + " ".join(f"{name(m)}:0.25" + ("!" if q2 % 4 == 0 else "'") for q2, m in enumerate(run_to(nr, 8)))
        if k % 2 == 0:
            return f"{rn}:1! {name(t5)}:0.5 {name(oc)}:0.5! {name(t7)}:0.5 {name(t5)}:0.5 {name(t3)}:0.5 {name(t5)}:0.5"
        return f"{rn}:0.5! {rn}:0.5 {name(oc)}:0.5! {rn}:0.5 {name(t5)}:0.5! {name(t3)}:0.5 " + run
    if sec == "sweep":
        # スウィープと一緒に、ベースも分散和音で駆ける
        return " ".join(f"{name(m)}:0.25" + ("!" if q2 % 4 == 0 else "'") for q2, m in enumerate([R, t3, t5, oc, t5, t3, R, t3, t5, oc, t7, oc, t5, t3, t5, R]))
    if sec == "bridge":
        if k < 8:   # ベースが主役で歌う（高めの音域で長い音と装飾）
            hi = [oc, t7, t5, t3]
            return f"{name(oc)}:1.5! {name(t7)}:0.5 {name(t5)}:1 " + " ".join(f"{name(m)}:0.25" + ("!" if q2 == 0 else "'") for q2, m in enumerate(run_to(nr, 4)))
        if k < 12:
            return f"{rn}:0.25! {name(t5)}:0.25' {name(oc)}:0.25' {name(t5)}:0.25' " * 2 + f"{name(t3)}:0.5 {name(t5)}:0.5 " + run
        return f"{rn}:4" if k < 14 else f"{rn}:1 {rn}:1 {rn}:0.5 {rn}:0.5 {rn}:0.5 {rn}:0.5"
    if sec == "solo":
        return f"{rn}:0.5! {rn}:0.25' {rn}:0.25' {name(oc)}:0.5! {rn}:0.5 {name(t5)}:0.5! {rn}:0.5 " + run
    return bass_bar(i)

# ── ドラム（16分のグリッド）──
def phrase_end(i):
    sec, c, k, n, no = BARS[i]
    return k == n - 1 or (k % 8 == 7)
def kick_bar(i):
    sec, c, k, n, no = BARS[i]
    if sec == "open":
        return "X..............." if k == 0 else "................"
    if sec == "intro":
        return "................" if k < 6 else ("X...X...X...X..." if k == 6 else "X...X...X.X.XXXX")
    if sec == "introB":
        if k % 4 == 3:
            return "X..X..X........."
        return "X..X..X...X.X..." if k % 4 != 2 else "X..X..X...X.XXX."
    if sec == "verse":
        if k % 8 == 7:
            return "X..X..X.XXX.XXX."          # 3+3+2 の短い連打（フレーズ終わり）
        if k % 4 == 3:
            return "X..X..X.X.......X"[:16]
        return "X..X..X.X.....X." if k % 2 == 0 else "X..X..X.X..X..X."
    if sec == "pre":
        if k < 4:
            return "X.......X......."            # ハーフタイム
        if k < 6:
            return "X...X...X...X..."
        return "X.X.X.X.X.X.X.X." if k == 6 else "XXXXXXXX........"   # 最後は1拍半止める（全員）
    if sec == "chorus":
        if k == 15:
            return "X..x..X.XXXXXX.." if no != CHORUS_NO[-1] else "X...X...X......."
        if k % 4 == 3:
            return "X..x..X.X...XXXX"            # 4小節ごとに1拍だけ連打
        return "X..x..X.X..x..x."
    if sec == "sweep":
        return "X..X..X.X..X..X." if k % 2 == 0 else "X..X..X.X.X.X.XX"
    if sec == "bridge":
        if k < 8:
            return "X..............." if k % 2 == 0 else "........X......."
        if k < 12:
            return "X.......X..X...."
        if k < 15:
            return "X...X...X...X..."
        return "X.X.X.X.XXXXXXXX"
    if sec == "breakdown":
        return "X..X..X.X..X..X." if k % 2 == 0 else ("X..X..X...XXX.X." if k != 7 else "XXX.XXX.XX.XXXX.")
    if sec == "solo":
        if k < 8:
            return "X..X..X.X..X..X." if k % 2 == 0 else "X..x..X.X...XX.X"
        if k < 14:
            return "X..x..X.X..x..x." if k % 2 == 0 else "X..x..X.X..xXXXX"
        return "X.X.X.X.X.X.X.X." if k == 14 else "XXXXXXXXXXXX...."   # 山場の2小節だけ（ブラスト→連打）
    if sec == "outro":
        return "X..............." if k == 0 else "................"
    return "................"
def snare_bar(i):
    sec, c, k, n, no = BARS[i]
    if sec == "intro":
        return "................" if k < 7 else "x.x.x.x.xxxxXXXX"
    if sec == "introB":
        return "....X.......X..." if k != 7 else "....X.......XXXX"
    if sec == "verse":
        if k % 8 == 7:
            return "....X..o....X.XX"
        return "....X..o.o..X..o"
    if sec == "pre":
        if k < 4:
            return "........X......."
        if k < 6:
            return "....X.......X..."
        return "....X...X...X.X." if k == 6 else "........XXXX...."
    if sec == "chorus":
        if k == 15 and no != CHORUS_NO[-1]:
            return "....X.......xXXX"
        return "....X.......X..."
    if sec == "sweep":
        return "........X......." if k < 7 else "....X...XXXXXXXX"
    if sec == "bridge":
        if k < 8:
            return "................" if k % 4 != 3 else "............o.o."
        if k < 12:
            return "........X......."
        if k < 15:
            return "....X.......X..."
        return "x.x.x.x.xxxxXXXX"
    if sec == "breakdown":
        return "........X......."
    if sec == "solo":
        if k == 14:
            return ".X.X.X.X.X.X.X.X"
        if k == 15:
            return "............XXXX"
        return "....X.......X..."
    if sec == "outro":
        return "................"
    return "................"
def hat_bar(i):
    sec, c, k, n, no = BARS[i]
    if sec == "verse":
        if k in (0, 8):
            return "....x.x.x.x.x.x."            # 1拍目はクラッシュ
        if k == n - 1:
            return "x.x.x.x........."            # 後ろ2拍はタム
        return "x.x.x.x.x.x.x.x." if k % 4 != 3 else "....x.x.x.x.O..."
    if sec == "pre" and 4 <= k < 7:
        return "x.x.x.x.x.x.x.x." if k != 4 and k != 6 else "....x.x.x.x.x.x."
    # Cメロ後半はライドで刻む（ハイハットは休む）
    if sec == "bridge" and k < 8:
        return "................"
    return "................"
def tom_bar(i):
    sec, c, k, n, no = BARS[i]
    if sec in ("verse",) and k == n - 1:
        return "R:2 C4:0.25! C4:0.25 A3:0.25! A3:0.25 F3:0.25! F3:0.25 D3:0.25! D3:0.25"
    if sec == "sweep" and k == 3:
        return "R:3 A3:0.25! A3:0.25 F3:0.25! D3:0.25"
    if sec == "breakdown" and k % 2 == 1:
        return "R:3 F3:0.5! D3:0.5"
    if sec == "solo" and k == 7:
        return "C4:0.5! A3:0.5 F3:0.5! D3:0.5 C4:0.25 C4:0.25 A3:0.25 A3:0.25 F3:0.25 F3:0.25 D3:0.25 D3:0.25"
    return "R:4"
def cym_bar(i):
    # C2 クラッシュ／D2 ライド／B2 チャイナ／A2 スプラッシュ
    sec, c, k, n, no = BARS[i]
    first = k == 0
    if sec == "open":
        return "C2:4!" if k == 0 else "R:4"
    if sec == "intro":
        return "R:4" if k < 7 else "R:4"
    if sec == "introB":
        return "C2:4!" if k % 4 == 0 else ("B2:0.75! B2:0.75 B2:0.5 R:2" if k % 4 == 3 else "D2:1 D2:1 D2:1 D2:1")
    if sec == "verse":
        if first or k == 8:
            return "C2:4!"
        return "B2:1! R:3" if k % 4 == 3 and k != n - 1 else "R:4"   # 開く小節の頭にチャイナ
    if sec == "pre":
        return "C2:4!" if k in (0, 4) else ("A2:1 R:3" if k == 6 else "R:4")
    if sec == "chorus":
        if k % 4 == 0:
            return "C2:1! D2:0.5 D2:0.5 D2:0.5 D2:0.5 D2:0.5 D2:0.5"
        if k == 11:
            return "C2:2! C2:2!"                 # E メジャーで空が開くところ
        if k % 4 == 2:
            return "B2:1! D2:0.5 D2:0.5 D2:0.5 D2:0.5 D2:0.5 B2:0.5!"   # チャイナのアクセント（頭と、次の小節への食い）
        return "D2:0.5! D2:0.5 D2:0.5 D2:0.5 D2:0.5! D2:0.5 D2:0.5 D2:0.5"
    if sec == "sweep":
        return "C2:4!" if k % 4 == 0 else "B2:1 B2:1 B2:1 B2:1"
    if sec == "bridge":
        if k < 8:
            return "D2:1, D2:1, D2:1, D2:1," if k % 2 == 1 else "D2:2, D2:2,"
        if k == 8 or k == 12:
            return "C2:4!"
        return "D2:0.5 D2:0.5 D2:0.5 D2:0.5 D2:0.5 D2:0.5 D2:0.5 D2:0.5" if k < 15 else "R:4"
    if sec == "breakdown":
        return "B2:0.75! B2:0.75 B2:0.5 B2:0.75! B2:0.75 B2:0.5" if k % 2 == 0 else "B2:0.75! B2:0.75 B2:0.5 R:2"
    if sec == "solo":
        if k == 7:
            return "R:4"   # タム回し
        if k % 4 == 0:
            return "C2:4!"
        if k < 14 and k % 4 == 2:
            return "B2:1! D2:0.5 D2:0.5 B2:1! D2:0.5 D2:0.5"
        return "D2:0.5 D2:0.5 D2:0.5 D2:0.5 D2:0.5 D2:0.5 D2:0.5 D2:0.5" if k < 14 else ("B2:0.5! B2:0.5 B2:0.5! B2:0.5 B2:0.5! B2:0.5 B2:0.5! B2:0.5" if k == 14 else "C2:4!")
    if sec == "outro":
        return "C2:4!" if k == 0 else "R:4"
    return "R:4"
def grid(fn):
    bars = [fn(i) for i in range(NB)]
    for i, b in enumerate(bars):
        assert len(b) == 16, (fn.__name__, i, b)
    return "g:" + "".join(bars)

# ── シンセ ──
def arp_bar(i, rev=False):
    sec, c, k, n, no = BARS[i]
    on = sec in ("intro", "verse", "pre", "chorus", "bridge", "outro") and not (sec == "outro" and k > 6)
    if not on:
        return "R:4"
    r, iv, q = chord(c)
    R = at_least(r, midi("C4"))
    tones = [R + x for x in iv[:4]] + [R + 12]
    t3 = tones[1]; t5 = tones[2]; top = R + 12
    pat = [R, t5, top, t3 + 12, t5 + 12, t3 + 12, top, t5]
    if sec == "verse" and k % 2 == 1:
        pat = [R, t3, t5, top, t5, t3, R, t5]
    if sec == "verse" and k % 4 >= 2:
        return "R:4"   # Aメロは2小節鳴らして2小節休む（息継ぎ）
    pat = [m - 12 if m > midi("C6") else m for m in pat]
    if rev:   # 右側は逆向き（上から下へ）にして、左右でからみ合わせる
        pat = pat[4:] + pat[:4]
    toks = [f"{name(m)}:0.25" + ("!" if j % 4 == 0 else ",") for j, m in enumerate(pat * 2)]
    if k % 4 == 3:
        toks = toks[:12] + ["R:1"]   # 4小節ごとに1拍の息継ぎ
    return " ".join(toks)
PAD_VOICES = 3
def pad_voice(i, v):
    sec, c, k, n, no = BARS[i]
    if sec in ("introB", "breakdown", "sweep") or (sec == "solo" and k < 8) or (sec == "outro" and k == 7):
        return None
    r, iv, q = chord(c)
    R = at_least(r, midi("F#3"))
    # 根音・3度・（7度があれば7度、なければ5度）を下から重ねる
    third = R + iv[1]
    top = R + (iv[3] if len(iv) > 3 and iv[3] < 12 else iv[2])
    if top <= third:
        top += 12
    m = [R, third, top][v]
    return name(m - 12 if m > midi("C5") else m)
def pad_part(v):
    toks, cur, dur = [], None, 0
    for i in range(NB):
        nn = pad_voice(i, v)
        nn = nn or "R"
        if nn == cur:
            dur += 4
        else:
            if cur is not None:
                toks.append(f"{cur}:{dur}")
            cur, dur = nn, 4
    toks.append(f"{cur}:{dur}")
    # 長い音・休みを 8 拍以下に分ける
    out = []
    for t in toks:
        nm, d = t.split(":"); d = int(d)
        while d > 0:
            out.append(f"{nm}:{min(8, d)}"); d -= 8
    return " ".join(out)
def sky_bar(i):  # サビ2・最後のサビで、旋律を明るいシンセで重ねる
    sec, c, k, n, no = BARS[i]
    if sec == "chorus" and no in CHORUS_NO[1:]:
        return lead_bar(i).replace("!^", "!").replace("!~", "!")
    return "R:4"
def riser_bar(i):
    sec, c, k, n, no = BARS[i]
    nxt_sec = BARS[i + 2][0] if i + 2 < NB else None
    if BARS[i + 1][2] == 0 if i + 1 < NB else False:
        pass
    # 次のセクションがサビ／導入／ブレイクダウンになる直前の3小節（C4＝4秒のライザー。172bpm の 12 拍＝4.2秒で、頂点が次の頭に来る）
    #   2026-10-21: 8 拍（2.8秒）では 4秒のライザーが頂点の前で切れて、ほとんど聞こえなかった
    TARGET = ("chorus", "intro", "introB", "breakdown")
    if i + 3 < NB and BARS[i + 3][2] == 0 and BARS[i + 3][0] in TARGET and k == n - 3:
        return "C4:12"
    if any(i + d < NB and BARS[i + d][2] == 0 and BARS[i + d][0] in TARGET and k == n - d for d in (1, 2)):
        return None  # 前の小節の 8 拍に含まれる
    return "R:4"
def riser_part():
    toks = []
    for i in range(NB):
        t = riser_bar(i)
        if t:
            toks.append(t)
    return " ".join(toks)

drum = {"pan": 0, "amp": "auto", "gainDb": -4}
parts = [
    {"instrument": "distGuitar", "role": "刻み（エレクトロロック・左右）", "volume": 0.1, "pan": 0, "guitarTone": "electro-rock", "gainDb": -5, "notes": join([rhythm_bar(i) for i in range(NB)])},
    {"instrument": "distGuitar", "role": "Aメロの刻み（ブリッジミュート）", "volume": 0.1, "pan": 0, "guitarTone": "electro-rock", "palmMute": True, "gainDb": -5, "notes": join([palm_bar(i) for i in range(NB)])},
    {"instrument": "leadGuitar", "role": "リード（サビの旋律）", "volume": 0.13, "pan": 0, "guitarTone": "bmth-lead", "noRestrike": True, "phrase": 8, "notes": join([lead_bar(i) for i in range(NB)])},
    {"instrument": "leadGuitar", "role": "スウィープとタッピング", "volume": 0.11, "pan": 0.12, "guitarTone": "bmth-lead", "noRestrike": True, "legato": True,
     "fx": [{"type": "eq", "low": -2, "mid": 3, "midHz": 1800, "high": 1}, {"type": "delay", "beats": 0.75, "mix": 0.12, "feedback": 0.2}, {"type": "plate", "mix": 0.12}],
     "notes": join([tech_bar(i) for i in range(NB)])},
    {"instrument": "bass", "role": "ベース（旋律をバキバキに）", "volume": 0.19, "pan": 0, "amp": "bassGrind", "ampDrive": 0.75, "notes": join([mel_bass_bar(i) for i in range(NB)])},  # 2026-10-21 人間「音がこもっていてラウドのベースじゃなかった」「指弾きの方がいい」: 明るい歪み＋指弾き（--bass finger）
    {"instrument": "kick", "role": "キック（ツーバスはところどころ）", "volume": 0.22, **drum, "trigger": "punch", "notes": grid(kick_bar)},
    {"instrument": "snare", "role": "スネア", "volume": 0.18, **drum, "push": 0.02, "notes": grid(snare_bar)},
    {"instrument": "hihat", "role": "ハイハット", "volume": 0.05, **drum, "push": -0.01, "notes": grid(hat_bar)},
    {"instrument": "tom", "role": "タム", "volume": 0.16, **drum, "notes": join([tom_bar(i) for i in range(NB)])},
    {"instrument": "crash", "role": "シンバル（クラッシュ・ライド・チャイナ）", "volume": 0.057, **drum, "notes": join([cym_bar(i) for i in range(NB)])},
    # 2026-10-21 人間「シンセの音をもうちょっと現代的な感じで空間を感じるように」: ガラスのプラック（長い尾）＋ピンポンディレイ＋左右の広げ＋ホール。キックで少し凹ませる
    # 2026-10-21 人間「シンセのふわふわ強いかな。あれならキーボードに変えよう」: アルペジオと和音をピアノ（右手・左手）に
    {"instrument": "piano", "role": "キーボード（右手のアルペジオ）", "volume": 0.09, "pan": 0.2, "reverb": 0.22, "notes": join([arp_bar(i) for i in range(NB)])},
]
# 2026-10-21 全弦開放のパートにチャンネルを空けるため、パッド（halo）はスーパーソーの壁が弱く鳴らす形にまとめた
if False:
  for v in range(PAD_VOICES):
    parts.append({"instrument": "pad", "role": f"パッド（空気）{v + 1}", "patch": "halo", "volume": 0.045, "pan": 0, "reverb": 0.65, "duck": 0.25,
                  "fx": [{"type": "widen", "mix": 0.8}, {"type": "reverb", "mix": 0.35}], "notes": pad_part(v)})
# 現代的なスーパーソーの壁（サビ・導入・Bメロ後半・ソロ後半・終わり）。キックに合わせて凹ませ（サイドチェイン風）、左右に広げる
def wall_voice(i, v):
    sec, c, k, n, no = BARS[i]
    on = sec == "chorus" or (sec == "intro" and k >= 4) or (sec == "pre" and k >= 4) or (sec == "solo" and k >= 8) or (sec == "outro" and k < 6)
    soft = not on and pad_voice(i, v) is not None and sec != "open"   # もとのパッドの場面は弱く（空気）
    if not on and not soft:
        return None
    r, iv, q = chord(c)
    R = at_least(r, midi("B3"))
    third = R + iv[1]
    top = R + (iv[3] if len(iv) > 3 and iv[3] < 12 else iv[2])
    if top <= third:
        top += 12
    return name([R, third, top][v]) + ("," if soft else "")
def wall_part(v):
    toks = []
    for i in range(NB):
        nn = wall_voice(i, v)
        if not nn:
            toks.append("R:4")
        elif nn.endswith(","):
            toks.append(f"{nn[:-1]}:4,")                    # 静かな場面は全音符で弱く
        else:
            toks.append(f"{nn}:1.5! {nn}:1 {nn}:1.5")       # キーボードらしく、刻みと同じシンコペーションで弾く
    return join(toks)
for v in range(PAD_VOICES):
    # 3つの声を左・中・右に置き、ダブラーで左右に二重にする（チャンネルは3つ使う）
    parts.append({"instrument": "piano", "role": f"キーボード（和音）{v + 1}", "volume": 0.07, "pan": -0.15, "reverb": 0.22, "notes": wall_part(v)})
# 2026-10-21 チャンネルが足りないので、サビの旋律の重ね（sawLead）は外す（リードの1オクターブ上が同じ役目をする）
if False: parts.append({"instrument": "lead", "role": "サビの旋律の重ね（明るいシンセ）", "patch": "sawLead", "volume": 0.04, "pan": 0, "reverb": 0.5,
              "fx": [{"type": "pingpong", "beats": 0.5, "mix": 0.25, "feedback": 0.35}, {"type": "widen", "mix": 0.6}],
              "notes": join([sky_bar(i) for i in range(NB)])})
OPEN = ["B1", "F#2", "B2", "E3", "G#3", "C#4"]
for j, nn in enumerate(OPEN):
    notes = join([f"{nn}:4!" if (BARS[i][0] == "open" and BARS[i][2] == 0) else "R:4" for i in range(NB)]).replace(f"{nn}:4! R:4", f"{nn}:8! ", 1).replace("  ", " ")
    parts.append({"instrument": "distGuitar", "role": f"全弦開放（{j + 1}弦目）", "volume": 0.07, "pan": 0, "guitarTone": "electro-rock", "double": False,
                  "ampDrive": 0.25, "ampGate": 0, "powerChord": False, "sustain": 2, "reverb": 0.4, "push": round(j * 12 / 1000 * BPM / 60, 3), "notes": notes})
parts.append({"instrument": "pad", "role": "ライザー（場面の前の盛り上げ）", "patch": "fxRiser", "volume": 0.09, "pan": 0, "notes": riser_part()})

chords = " ".join(simple(b[1]) for b in BARS)
song = {
    "title": "蒼穹ストライド",
    "description": "仮: 空を感じる疾走メタルコア（自作。ドロップB・bpm172。シンセ・スウィープ・タッピング・ジャズっぽいベース・ところどころのツーバス）",
    "bpm": BPM, "beats": 4, "chords": chords, "barsPerChord": 1, "repeats": 1,
    "autoAccompaniment": False, "feel": "rock", "tone": "metal", "dynamics": True, "human": 0.3,
    "sections": [{"kind": KIND[s], "bars": n} for s, _, n, _ in SEC],
    "modulate": {"at": "lastChorus", "semitones": 1},
    "diGuitar": "emily", "autoScoop": False, "guitarWobble": False,
    # 2026-10-21 人間「シンバル系なりとか少し伸ばして鋭い音」「バスドラはトリガー入れて重い音に」
    "drumMix": {"kick": {"level": 1.15}, "crash": {"level": 1.1}},
    "parts": parts,
}
json.dump(song, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(out, NB, "小節", round(NB * 4 * 60 / BPM, 1), "秒")
