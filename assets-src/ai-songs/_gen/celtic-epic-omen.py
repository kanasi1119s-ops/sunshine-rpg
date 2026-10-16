# 『霧の森の予兆』（仮）: 自然の壮大さと、これから大変なことが起きる予感をあわせ持つ、ミステリアスなケルト音楽（2026-10-16、人間の依頼
#   「自然を感じる壮大性があり、今から大変なことが起きる、ミステリーなケルト音楽を作って」）。
# 6/8（1小節に2拍、1拍を3つに分ける）・付点4分＝70・ホ短調（主題はドリアン＝C# を使う明るい短調。不穏な所は C と F を借りる）・92小節（約2分38秒）。
# 形と、だれが鳴るか:
#   予兆8（霧。ハープの点・遠いベル・低い弦の持続。笛が主題の頭を出し、最後に B→C の半音でおびえる。ティンパニのロール）
#   → 主題A16（ロー・ホイッスル風の笛ひとりで主題。ハープの6/8の分散和音・チェロ。後半8小節でボーラン・コントラバス）
#   → B16（フィドルが高い旋律で「自然の壮大さ」。弦が入り、後半は笛が3度下でハモり、ホルンが長い音で支える）
#   → 不穏8（E の持続の上でチェロの刻みが E E E E E F と半音で揺れる。ホルンの低い音、笛の B→C、太鼓が近づいてくる）
#   → 山場B16（ホルン2本とフィドルが B の旋律を堂々と。合唱・弦・ハープ・チェロとコントラバスの刻み・大太鼓・クラッシュ）
#   → 山場A16（笛とフィドルのオクターブで主題。ホルンの対旋律）
#   → 終わり12（主題が終わったと思ったら、不穏の刻みが戻る。太鼓が迫り、♭VI（C）で全員が打ち、1小節の静寂のあと低い一撃で終わる。解決しない）
# 進行（chord-variety-guide のレシピ: ドリアンの IV 長（A/C#）と、借用の ♭VI（C）・ナポリ風の F をペダルの上に。分数コードで低音を順に動かす）。
# 2026-10-16 の人間の指示を取り入れた: ①FX（笛にディレイ＋プレート、フィドルにプレート、ホルンにリバーブ、ハープにピンポンディレイ、チェロにコンプ、ピアノにプレート）
#   ②ピアノは左手（低音を6/8で転がす）と右手（3音の和音を同時に）③定番から外したコード進行（B の前半 G Bm C E Am7 Fmaj7 D B7。急に明るい E と、ナポリの Fmaj7）
#   ④作曲ソフトに足したアコーディオン（A の後半で和音をのばし、山場Aで旋律の1オクターブ下）と鉄琴（霧のきらめき、山場Bで旋律の1オクターブ上）
#   ほかに、アコギ4本の6/8の刻み（Aの後半から。不穏の所は低い E と B）。
# 既存の曲のメロディは使わない（CLAUDE.md 1-1）。旋律はすべてこの曲のために書いたもの。
# 使い方: python3 celtic-epic-omen.py <出力.json>
# 書き出し: --drums muldjord --bass finger --orchestra vsco --piano salamander --guitar shiny-acoustic --master-preset rock-clean --master -13.5（点数 8.01）
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from celtic_lib import Song, nm, md, fmt

DOR = [4, 6, 7, 9, 11, 1, 2]       # E ドリアン
AEO = [4, 6, 7, 9, 11, 0, 2]       # E エオリアン（C を借りる所）
HARM = [4, 6, 7, 9, 11, 0, 3]      # E 和声的短音階（B・B7 の上）
EMAJ = [4, 6, 8, 9, 11, 1, 2]      # E 長3和音（急に明るくなる所）の上
PHR = [4, 5, 7, 9, 11, 0, 2]       # F（ナポリの和音）の上
def scale_of(ch):
    c = ch.split("/")[0]
    if c.startswith("B") and not c.startswith("Bm"): return HARM
    if c.startswith("F") and not c.startswith("F#"): return PHR
    if c.startswith("E") and not c.startswith("Em"): return EMAJ
    if c.startswith("C") or c.startswith("Am") or c.startswith("Dm"): return AEO
    return DOR

# ---------------- 旋律 ----------------
A1 = ["E5:3 D5:1 B4:2", "A4:2 B4:1 D5:3", "G4:1 A4:1 B4:1 D5:2 E5:1", "F#5:3 E5:1 D5:2",
      "E5:2 G5:1 B5:3", "A5:2 G5:1 E5:2 C#5:1", "D5:2 B4:1 G4:2 A4:1", "B4:4 R:2"]
A2 = ["E5:3 D5:1 B4:2", "A4:2 B4:1 D5:3", "G5:2 F#5:1 E5:2 D5:1", "F#5:2 A5:1 D6:3",
      "B5:3 A5:1 G5:2", "A5:2 E5:1 C#5:2 E5:1", "F#5:2 D5:1 B4:2 A4:1", "E5:6"]
B1 = ["B5:3 D6:1 B5:2", "A5:3 F#5:1 D5:2", "G5:2 A5:1 B5:2 D6:1", "E6:4 C#6:2",
      "D6:2 B5:1 G5:2 B5:1", "E6:2 C6:1 G5:2 C6:1", "D6:3 A5:1 F#5:2", "G5:4 A5:2"]
B2 = ["B5:2 D6:1 E6:3", "D6:2 A5:1 F#5:3", "G5:2 B5:1 E6:3", "C#6:3 B5:1 A5:2",
      "G5:2 C6:1 E6:3", "D6:3 B5:1 G5:2", "E6:2 D6:1 A5:3", "B5:3 D#6:3"]
CA1 = "Em D/F# G D Em A/C# G Bm".split()
CA2 = "Em D/F# G D Em A/C# Bm Em".split()
CB1 = "G Bm C E Am7 Fmaj7 D B7".split()      # 急に明るい E（長3和音）と、ナポリの Fmaj7。定番の進行から外す（2026-10-16、人間の指示）
CB2 = "G Bm/F# Em A C Em/B Asus4 B".split()
CPRO = "Em Em C/E Em Am/E Em D/E Bsus4".split()
CDRD = "Em F/E Em F/E Em F/E C/E B7".split()
CTAG = "Em F/E Em F/E Em F/E Em F/E C C Em Em".split()

plan = [("pro", i) for i in range(8)] + [("A", i) for i in range(16)] + [("B", i) for i in range(16)] + [("dread", i) for i in range(8)] \
     + [("B2", i) for i in range(16)] + [("A3", i) for i in range(16)] + [("tag", i) for i in range(12)]
def chord_at(k, i):
    return {"pro": CPRO, "dread": CDRD, "tag": CTAG}.get(k, None)[i] if k in ("pro", "dread", "tag") else \
        ((CA1 + CA2) if k in ("A", "A3") else (CB1 + CB2))[i]
chords = [chord_at(k, i) for k, i in plan]
S = Song(2, 3, len(plan), DOR); S.check(A1, A2, B1, B2); S.G = 0.1   # 付点4分＝70 で約86ms（短いと笛の録音がプチッと鳴った）。笛は音を切らずにつなぐ（legato。切ると前の音が途切れてプチッと鳴った）
MA = A1 + A2; MB = B1 + B2

# ---------------- 和音の音 ----------------
PCN = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def pc(s): return (PCN[s[0]] + (1 if len(s) > 1 and s[1] == "#" else 0)) % 12
def chord_pcs(ch):
    m = re.match(r"^([A-G]#?)(.*)$", ch.split("/")[0]); r = pc(m.group(1)); q = m.group(2)
    if q.startswith("sus4") or "sus4" in q: pcs = [r, (r + 5) % 12, (r + 7) % 12]
    elif q.startswith("m"): pcs = [r, (r + 3) % 12, (r + 7) % 12]
    else: pcs = [r, (r + 4) % 12, (r + 7) % 12]
    if "maj7" in q: pcs.append((r + 11) % 12)
    elif "7" in q: pcs.append((r + 10) % 12)
    return pcs
def bass_pc(ch): return pc(ch.split("/")[1]) if "/" in ch else chord_pcs(ch)[0]
def low(pcx, lo): return lo + ((pcx - lo) % 12)
def arp6(ch, lo=52):
    """ハープの6/8の分散和音（根音・5度・オクターブ・10度・オクターブ・5度）。"""
    p = chord_pcs(ch); r = low(p[0], 47); t3 = r + ((p[1] - p[0]) % 12); t5 = r + ((p[2] - p[0]) % 12)
    return [r, t5, r + 12, t3 + 12, t5 + 12, r + 24]   # 6つとも違う高さ（同じ高さを弾き直すと前の音が切れてプチッと鳴った）
def diat(seq_str, ch, k):
    sc = scale_of(ch); out = []
    for x in seq_str.split():
        n_, d = x.split(":")
        if n_ == "R": out.append(x); continue
        m = md(n_); dd = 1 if k > 0 else -1
        for _ in range(abs(k)):
            m += dd
            while m % 12 not in sc: m += dd
        out.append(f"{nm(m)}:{d}")
    return " ".join(out)
def oct_(seq_str, k): return " ".join(x if x.startswith("R:") else f"{nm(md(x.split(':')[0]) + 12 * k)}:{x.split(':')[1]}" for x in seq_str.split())

# ---------------- パート ----------------
S.part("flute", "panflute", "笛（ロー・ホイッスル風の旋律）", 0.21, 0.15, reverb=0.4, gainDb=2, breath=True,
       fx=[{"type": "delay", "beats": 1, "mix": 0.12, "feedback": 0.28}, {"type": "plate", "mix": 0.1}])   # 笛は標準のパンフルート（VSCO のフルート patch="flute" は音の変わり目でプチッと鳴った。2026-10-16 パートごとに書き出して確かめた）
S.part("fiddle", "fiddle", "フィドル（旋律）", 0.19, -0.2, patch="violin", reverb=0.38, gainDb=1, fx=[{"type": "plate", "mix": 0.14}])
# MIDI のチャンネルは（ドラム以外で）15まで。同じ楽器のパートは pan・reverb・fx をそろえて1つのチャンネルを共有させる（2026-10-16。あふれると別の楽器の音で鳴った）
S.part("horn", "brass", "ホルン（旋律・対旋律）", 0.15, -0.1, patch="horn", reverb=0.35, breath=True, release=0.5, fx=[{"type": "reverb", "mix": 0.15}])
S.part("horn2", "brass", "ホルン2（低い声部）", 0.12, -0.1, patch="horn", reverb=0.35, breath=True, release=0.5, fx=[{"type": "reverb", "mix": 0.15}])
for _k, _pan in (("g1", -0.5), ("g2", 0.5), ("g3", -0.5), ("g4", 0.5)):   # アコギ（6/8の刻み。B から）
    S.part(_k, "guitar", f"アコギ（{_k[1]}本目）", 0.08, _pan, amp="crystal", chorus=0, sustain=1.0, reverb=0.25, autoScoop=False, humanPitch=0, push=0.008 * int(_k[1]))
S.part("harp", "harp", "ハープ（6/8の分散和音）", 0.13, 0.4, reverb=0.38, bright=-0.4, sustain=2.2, release=0.6,
       fx=[{"type": "pingpong", "beats": 0.6667, "mix": 0.12, "feedback": 0.25}])
# ピアノは左手と右手で弾くイメージで（2026-10-16、人間の指示「ピアノ左手と右手で弾くイメージもあると曲の印象変わるかも」）:
#   右手＝3音の和音を同時に（コード弾き）、左手＝低音の根音・5度・オクターブを6/8で転がす
for _k in ("pno1", "pno2", "pno3"):
    S.part(_k, "piano", f"ピアノ右手（和音・{_k[3]}）", 0.09, 0.05, reverb=0.3, sustain=1.6, fx=[{"type": "plate", "mix": 0.15}])
S.part("pnoL", "piano", "ピアノ左手（低音）", 0.12, 0.05, reverb=0.3, sustain=1.4, fx=[{"type": "plate", "mix": 0.15}])
# アコーディオン（ケルトの伴奏と旋律の重ね）と、鉄琴（霧のきらめき・山場で旋律の1オクターブ上）。2026-10-16 に作曲ソフトへ足した音源
S.part("acc", "accordion", "アコーディオン", 0.12, 0.3, reverb=0.3, fx=[{"type": "room", "mix": 0.12}])
S.part("glock", "glockenspiel", "鉄琴", 0.07, 0.35, reverb=0.4, fx=[{"type": "delay", "beats": 0.6667, "mix": 0.15, "feedback": 0.3}])
S.part("cello", "strings", "チェロ（持続・刻み）", 0.14, -0.35, patch="cello", reverb=0.35,
       fx=[{"type": "compressor", "threshold": -18, "ratio": 3, "attack": 0.01, "release": 0.15}])
S.part("cb", "strings", "コントラバス", 0.15, 0, patch="contrabass", reverb=0.3)
S.part("sth", "strings", "弦（上・のばす）", 0.08, 0.55, patch="slowStrings", reverb=0.4, release=0.6)
S.part("stl", "strings", "弦（下・のばす）", 0.08, -0.55, patch="slowStrings", reverb=0.4, release=0.6)
S.part("choir", "choir", "合唱（遠く）", 0.07, 0, reverb=0.5, breath=True)   # 2026-10-16 点数の試行で外した（下の dump の前で消す）
# 遠いベル（fmBell）は外した: MIDI のチャンネルは16までで、楽器が17種類になると別の楽器と同じチャンネルに入り、音が崩れた（点数 8.01→7.52）。霧のきらめきは鉄琴が受けもつ
S.part("timp", "strings", "ティンパニ", 0.18, 0, patch="timpani", reverb=0.3, gainDb=-4)   # -4dB は点数の試行で決めた（7.98→8.01）
S.part("big", "inchTom", "大太鼓（18インチのタム）", 0.14, 0, patch="inchTom", reverb=0.15, gainDb=-10)
S.part("bodhran", "tom", "ボーラン風の刻み", 0.12, 0.1, reverb=0, gainDb=-8, bright=-0.4)
S.part("kick", "kick", "キック", 0.26, 0, gainDb=-8)
S.part("snare", "snare", "スネア（ロール）", 0.18, 0, gainDb=-10)
S.part("crash", "crash", "クラッシュ", 0.09, 0, gainDb=-8)

arc = []
GAIN = {"pro": (0.62, 0.74), "A": (0.74, 0.82), "B": (0.84, 0.94), "dread": (0.78, 0.96), "B2": (1.0, 1.03), "A3": (0.96, 1.0), "tag": (0.86, 1.04)}
def roll(note, n=12, acc=""):
    d = fmt(2 / n); return [f"{note}:{d}" + ("," if j < n // 2 and not acc else acc) for j in range(n)]

for bi, (k, i) in enumerate(plan):
    ch = chords[bi]; a, z = GAIN[k]; L = {"pro": 8, "dread": 8, "tag": 12}.get(k, 16)
    arc.append(round(a + (z - a) * i / (L - 1), 3))
    nxt = chords[bi + 1] if bi + 1 < len(chords) else ch
    if k == "tag" and i >= 10:   # 終わりの静寂
        if i == 10: S.put("horn2", bi, ["F3:2"])           # ♭2 の低いホルンだけが残る
        if i == 11:
            S.put("timp", bi, ["E2:2!"]); S.put("cb", bi, ["E2:2"]); S.put("big", bi, ["E2:2!"])
        continue
    S.scale = scale_of(ch)
    br = low(bass_pc(ch), 40)   # 低音（E2〜）
    # ---- 旋律 ----
    if k == "pro":
        if 2 <= i <= 4: S.put("flute", bi, S.ornament(S.seq(A1[i - 2]), "cut", bi, dens=0.3, legato=True))
        if i == 5: S.put("flute", bi, ["A4:2"])
        if i == 6: S.put("flute", bi, ["B4:1_", "C5:1"])
        if i == 7: S.put("flute", bi, ["B4:2"])
    if k == "A":
        S.put("flute", bi, S.ornament(S.seq(MA[i]), "cut", bi, dens=0.35, legato=True))
    if k == "B":
        S.put("fiddle", bi, S.ornament(S.seq(MB[i]), "roll", bi, dens=0.45, legato=True))
        if i >= 8: S.put("flute", bi, S.plain(S.seq(diat(MB[i], ch, -2)), legato=True))
    if k == "dread":
        if i in (1, 3): S.put("flute", bi, ["B4:1_", "C5:1"])
        if i in (2, 4): S.put("flute", bi, ["B4:2"])
    if k == "B2":
        S.put("fiddle", bi, S.ornament(S.seq(MB[i]), "plain", bi, legato=True))
        S.put("horn", bi, S.plain(S.seq(oct_(MB[i], -1)), legato=True))
        S.put("horn2", bi, S.plain(S.seq(oct_(diat(MB[i], ch, -2), -1)), legato=True))
        if i >= 8: S.put("flute", bi, S.plain(S.seq(diat(MB[i], ch, -2)), legato=True))
    if k == "A3":
        S.put("flute", bi, S.ornament(S.seq(MA[i]), "cut", bi + 7, dens=0.4, legato=True))
        # ホルンの対旋律: 和音の3度を、旋律が長い音のときに動く形で（1小節に2音）
        p = chord_pcs(ch); t3 = low(p[1], 55); t5 = low(p[2], 55)
        S.put("horn", bi, [f"{nm(t5)}:1_", f"{nm(t3)}:1"] if i % 2 == 0 else [f"{nm(t3)}:2"])
        S.put("horn2", bi, [f"{nm(low(p[0], 43))}:2"])
    if k == "tag":
        if i in (1, 3): S.put("flute", bi, ["B4:1_", "C5:1"])
        if i in (2, 4): S.put("flute", bi, ["B4:2"])
        if i in (6, 7): S.put("horn", bi, ["B3:2"] if i == 6 else ["C4:2"])
        if i == 8: S.put("horn", bi, ["G4:2!"]); S.put("horn2", bi, ["C4:2!"]); S.put("fiddle", bi, ["E5:2!"])
        if i == 9: S.put("horn", bi, ["G4:2"]); S.put("horn2", bi, ["C4:2"]); S.put("fiddle", bi, ["E5:2"])
    # ---- ハープ ----
    if k in ("A", "B", "B2", "A3", "pro"):   # 前奏から6/8の分散和音（まばらな点だけだと点数が低かった: 0〜15秒 7.52）
        t = arp6(ch)
        S.put("harp", bi, [f"{nm(x)}:{fmt(1 / 3)}" for x in t])
    # ---- ピアノのコード弾き（3音を同時に。前奏の後半は1小節1回、B と山場は 1拍目と2拍目、終わりの C は強く2回）----
    pv = sorted(low(x, 60) for x in chord_pcs(ch)[:3])
    pon = (k == "pro" and i >= 4) or k in ("B", "B2", "A3") or (k == "tag" and i in (8, 9)) or (k == "A" and i >= 8)
    if pon:
        for vi, g in enumerate(("pno1", "pno2", "pno3")):   # 右手
            n0 = nm(pv[vi])
            if k == "pro" or (k == "A"): S.put(g, bi, [f"{n0}:2" + ("," if k == "pro" else "")])
            elif k == "tag": S.put(g, bi, [f"{n0}:1!", f"{n0}:1"] if i == 8 else [f"{n0}:2"])
            elif k == "B": S.put(g, bi, [f"{n0}:{fmt(4 / 3)}", f"{n0}:{fmt(2 / 3)},"])
            else: S.put(g, bi, [f"{n0}:1!", f"{n0}:{fmt(2 / 3)},", f"{n0}:{fmt(1 / 3)},"])
        lr = low(bass_pc(ch), 36); lo5 = lr + 7; lo8 = lr + 12   # 左手（C2〜B2 の根音から）
        T3 = fmt(1 / 3)
        if k == "pro": S.put("pnoL", bi, [f"{nm(lr)}:2,"])
        elif k == "A": S.put("pnoL", bi, [f"{nm(lr)}:1", f"{nm(lo5)}:1,"])
        elif k == "B": S.put("pnoL", bi, [f"{nm(lr)}:{fmt(2 / 3)}", f"{nm(lo5)}:{T3},", f"{nm(lo8)}:1"])
        elif k == "tag": S.put("pnoL", bi, [f"{nm(lr)}:1!", f"{nm(lr)}:1"] if i == 8 else [f"{nm(lr)}:2"])
        else: S.put("pnoL", bi, [f"{nm(x)}:{T3}" + ("!" if j == 0 else ("," if j in (2, 5) else "")) for j, x in enumerate((lr, lo5, lo8, lo5 + 12 if lo5 + 12 < 60 else lo5, lo8, lo5))])
    # ---- アコーディオン（A の後半は和音の3度をのばして息づかい、山場Aでは旋律の1オクターブ下）----
    if k == "A" and i >= 8: S.put("acc", bi, [f"{nm(low(chord_pcs(ch)[1], 57))}:2"])
    if k == "A3": S.put("acc", bi, S.plain(S.seq(oct_(MA[i], -1)), legato=True))
    if k == "B" and i >= 8: S.put("acc", bi, [f"{nm(low(chord_pcs(ch)[2], 57))}:{fmt(4 / 3)}", f"{nm(low(chord_pcs(ch)[1], 57))}:{fmt(2 / 3)},"])
    # ---- 鉄琴（前奏のきらめき、山場B で旋律の1オクターブ上）----
    if k == "pro" and i in (3, 5): S.put("glock", bi, [f"{nm(low(chord_pcs(ch)[2], 79))}:1", f"{nm(low(chord_pcs(ch)[0], 84))}:1"])
    if k == "B2": S.put("glock", bi, S.plain(S.seq(oct_(MB[i], 1)), legato=False))
    # ---- アコギ（各拍: ダウン2/3・アップ1/3。低い2本はのばす）----
    if k == "dread" or (k == "tag" and i < 10):   # 不穏の所は低い E と B を、刻みと同じ6/8で
        for gi, g in enumerate(("g1", "g2")):
            n0 = (40, 47)[gi]
            S.put(g, bi, [f"{nm(n0)}:{fmt(1 / 3)}" + ("!" if j in (0, 3) else ",") for j in range(6)])
    if k in ("B", "B2", "A3") or (k == "A" and i >= 8):
        pp = chord_pcs(ch); gb = low(bass_pc(ch), 40); g0 = low(pp[0], 45)
        v = [gb, g0 + ((pp[2] - pp[0]) % 12), g0 + 12, g0 + 12 + ((pp[1] - pp[0]) % 12)]
        for gi, g in enumerate(("g1", "g2", "g3", "g4")):
            n0 = v[gi]
            if gi < 2: S.put(g, bi, [f"{nm(n0)}:2!"]); continue
            toks = []
            for beat in range(2):
                toks += [f"{nm(n0)}:{fmt(2 / 3)}" + ("!" if beat == 0 else ""), f"{nm(n0)}:{fmt(1 / 3)},"]
            S.put(g, bi, toks)
    # ---- 低い弦 ----
    if k == "pro":
        S.put("cb", bi, ["E2:2"])
        S.put("cello", bi, [f"{nm(br + 12 if br + 12 < 52 else br)}:2"])
    elif k == "A":
        S.put("cello", bi, [f"{nm(br + 12)}:2"])
        if i >= 8: S.put("cb", bi, [f"{nm(br)}:2"])
    elif k == "B":
        r3 = br + 12; p = chord_pcs(ch); f5 = r3 + ((p[2] - bass_pc(ch)) % 12)
        S.put("cello", bi, [f"{nm(r3)}:1_", f"{nm(f5 if f5 < r3 + 12 else f5 - 12)}:1"])
        S.put("cb", bi, [f"{nm(br)}:2"])
    elif k in ("dread", "tag"):
        S.put("cello", bi, ["E3:" + fmt(1 / 3)] * 5 + [("F3" if i % 2 == 0 else "D#3") + ":" + fmt(1 / 3)] if i < (10 if k == "tag" else 8) else ["R:2"])
        S.put("cb", bi, ["E2:2"])
    elif k in ("B2", "A3"):
        r3 = br + 12
        S.put("cello", bi, [f"{nm(r3)}:{fmt(1 / 3)}"] * 5 + [f"{nm(r3 + 7 if r3 + 7 < 60 else r3 - 5)}:{fmt(1 / 3)}"])
        S.put("cb", bi, [f"{nm(br)}:2"])
    # ---- 弦（のばす）・合唱 ----
    p = chord_pcs(ch); hi = low(p[1], 64); lo_ = low(p[2], 55)
    if k in ("pro", "A", "B", "B2", "A3", "dread") or (k == "tag" and i < 10):
        if k in ("dread", "tag"): S.put("sth", bi, ["B4:2" if i % 2 == 0 else "C5:2"]); S.put("stl", bi, ["E4:2"])
        else: S.put("sth", bi, [f"{nm(hi)}:2"]); S.put("stl", bi, [f"{nm(lo_)}:2"])
    if (k == "pro" and i >= 4) or k == "dread" or k in ("B2", "A3") or (k == "tag" and i < 10):
        S.put("choir", bi, [f"{nm(low(p[0], 52) if k not in ('dread', 'tag') else 52)}:2"])
    if k == "pro" and i in (0, 4): S.put("glock", bi, ["B6:2" if i == 0 else "E7:2"])
    if k == "tag" and i in (0, 4): S.put("glock", bi, ["C7:2,"])
    # ---- 打楽器 ----
    if k == "pro" and i == 7: S.put("timp", bi, roll("E2", 12))
    if k == "dread":
        S.put("timp", bi, ["E2:1!", "R:1"] if i < 7 else roll("E2", 12, "!"))
        if i >= 2: S.put("big", bi, S.pgrid("X..x.." if i < 6 else "X..XxX", {"X": "E2!", "x": "A2"}))
        if i >= 4: S.put("bodhran", bi, S.pgrid("x.ox.o" if i < 6 else "XxoXxo", {"X": "A2!", "x": "C3", "o": "C3,,"}))
        if i == 7: S.put("snare", bi, S.grid("ooxxXX"))
    if k == "A" and i >= 8: S.put("bodhran", bi, S.pgrid("X..x.o" if i % 4 != 3 else "X.oxXx", {"X": "A2", "x": "C3,", "o": "C3,,"}))
    if k == "B":
        S.put("bodhran", bi, S.pgrid("X.ox.o" if i % 4 != 3 else "XxoXxX", {"X": "A2!", "x": "C3", "o": "C3,,"}))
        if i % 2 == 0: S.put("kick", bi, S.grid("x....."))
        if i == 15: S.put("snare", bi, S.grid("ooxxXX"))
    if k in ("B2", "A3"):
        S.put("big", bi, S.pgrid("X..x.." if i % 4 != 3 else "X.xXxX", {"X": "E2!", "x": "A2"}))
        S.put("bodhran", bi, S.pgrid("XxoXxo", {"X": "A2!", "x": "C3", "o": "C3,,"}))
        S.put("kick", bi, S.grid("X.....") if i % 4 != 3 else S.grid("X..X.."))
        if i in (0, 8): S.put("crash", bi, S.grid("X....."))
        if i % 4 == 0: S.put("timp", bi, [f"{nm(low(bass_pc(ch), 40))}:2!"])
        if k == "A3" and i == 15: S.put("snare", bi, S.grid("ooxxXX"))
    if k == "tag" and i < 10:
        S.put("big", bi, S.pgrid("X..x.." if i < 4 else ("X..XxX" if i < 8 else "XxXXxX"), {"X": "E2!", "x": "A2"}))
        if i >= 4: S.put("bodhran", bi, S.pgrid("XxoXxo", {"X": "A2!", "x": "C3", "o": "C3,,"}))
        S.put("timp", bi, ["E2:1!", "R:1"] if i < 6 else roll("E2", 12, "!"))
        if i == 7: S.put("snare", bi, S.grid("ooxxXX"))
        if i == 8: S.put("crash", bi, S.grid("X.....")); S.put("kick", bi, S.grid("X....."))
    if (k == "dread" and i == 0) or (k == "B2" and i == 0) or (k == "tag" and i == 8): S.put("big", bi, ["E2:2!"])   # 場面の頭の一撃（インパクトの代わり）

S.parts.pop("choir"); S.order.remove("choir")   # 合唱は点数が下がった（7.89→7.92 で外した方が上）
out = sys.argv[1] if len(sys.argv) > 1 else "assets-src/ai-songs/celtic-epic-omen.json"
S.dump(out, "霧の森の予兆（仮）",
       "（仮）自然の壮大さと、これから大変なことが起きる予感をあわせ持つ、ミステリアスなケルト音楽。6/8・付点4分＝70・ホ短調（主題はドリアン）、約2分38秒。"
       "霧の予兆（ハープの点・遠いベル・笛が主題の頭と B→C の半音）→ ロー・ホイッスル風の笛の主題 → フィドルの高い旋律（自然の壮大さ）→ "
       "E の持続の上で半音にゆれるチェロの刻み・ホルン・近づく太鼓（不穏）→ ホルン2本とフィドルの山場 → 笛とフィドルのオクターブで主題 → "
       "不穏の刻みが戻り、♭VI で全員が打ち、静寂と ♭2 の低いホルンのあと、低い一撃で解決せずに終わる。"
       "ピアノは左手の低音と右手の和音、アコーディオン・鉄琴・アコギの6/8の刻み、笛のディレイ・ハープのピンポンディレイなどのFX。"
       "進行: ドリアンの IV 長（A/C#）、B の前半は G Bm C E Am7 Fmaj7 D B7（急に明るい E とナポリの Fmaj7）、借用の ♭VI（C）、E のペダルの上の F（半音の不安）。入り方: 5（ドローン＝低い持続音の上に点）。終わり方: 静寂と一撃（解決しない）。",
       70, chords, arc, extra={"guitarWobble": False})

# ---- 仕上げ: のばす楽器の「同じ高さの音の弾き直し」をつなぐ（音が切れてプチッと鳴った。2026-10-16、パートごとに書き出して確かめた）----
import json as _json
def _merge(notes, legato):
    toks = notes.split(); out = []
    for t in toks:
        n_, d = t.split(":", 1); mark = "".join(c for c in d if not (c.isdigit() or c == ".")); dv = float(d[:len(d) - len(mark)])
        if out and n_ != "R" and out[-1][0] == n_ and dv >= 1 and out[-1][1] >= 1 and "!" not in mark:
            out[-1][1] += dv; out[-1][2] = out[-1][2].replace("_", ""); continue
        out.append([n_, dv, mark.replace("_", "") if legato else mark])
    res = []
    for j, (n_, dv, mark) in enumerate(out):
        nxt = out[j + 1][0] if j + 1 < len(out) else "R"
        lg = "_" if legato and n_ != "R" and nxt not in ("R", n_) and dv >= 1 else ""
        res.append(f"{n_}:{fmt(dv)}{mark}{lg}")
    return " ".join(res)
_song = _json.load(open(out, encoding="utf-8"))
for _p in _song["parts"]:
    r = _p["role"]
    if r.startswith(("弦（", "コントラバス", "ホルン2", "チェロ")): _p["notes"] = _merge(_p["notes"], legato=r.startswith("弦（"))
    if r.startswith("笛"):   # 小節をまたぐ所も、休みがなければつないで吹く
        tk = _p["notes"].split()
        for j in range(len(tk) - 1):
            a_, b_ = tk[j].split(":")[0], tk[j + 1].split(":")[0]
            if a_ != "R" and b_ != "R" and a_ != b_ and not tk[j].endswith("_"): tk[j] += "_"
        _p["notes"] = " ".join(tk)
_json.dump(_song, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
