# vt25 07「宇宙人のふりをした日」The Day I Pretended to Be an Alien（仮）— エレクトロニカ（エレクトロポップ×トランス）。138・4/4。A 長調 → 最後のサビは +1（B♭）。
# 物語: 転校の初日、朝の教室で自己紹介。緊張で口がすべって「宇宙から来ました」。教室じゅうがしーんとした。
#   でも休み時間、となりの子が「宇宙語」で話しかけてくれた。どの星から来たの？ わたしはとっさに、うそを重ねる。
#   ふたりで作った秘密の言葉。うそがばれそうな日、胸がひかる。本当は、ふつうのわたしで友だちでいたい。
#   最後に、宇宙語じゃなく日本語で言う。「はじめまして。よろしくね」。ふたりの星の名前は、まだない。
# 場面と強さ: 信号（宇宙の信号のようなアルペジオ。宇宙語のあいさつ＝逆再生・中）→ Aメロ1（不思議な音程・語る）→ Bメロ1 → サビ1（素直な長調・強）
#   → 間奏（トランスのリード）→ Aメロ2（秘密の言葉）→ Bメロ2 → サビ2 → ばれそう（ハーフの重さ・弱）→ 最後のサビ（+1・24小節）→ よろしく（1音）
# 旋律の性格: Aメロは A のリディア（D# の音）の不思議な跳び（E → D# → E → A）。サビは素直な長調の三和音をかけ上がる（C#4 → E4 → A4 → C#5）。
# ほかの曲とちがう所（この曲だけの音）: 宇宙語のような逆再生の声（始まりの2小節。歌の版はテトの「よろしく」、BGM はリードを逆さに）。
#   B/A（リディアの和音）が「この星じゃない」感じを出す。
from vt25_lib import *

S = Song("07", "alien", "宇宙人のふりをした日（仮）", "The Day I Pretended to Be an Alien", 138, 4, "A", "major", "エレクトロニカ（エレクトロポップ×トランス・ボカロ）")
S.kit = "electro"
S.flags = S.flags + " --piano salamander --space sky --space-wet 0.2"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.55
K = Key("A", "major")           # oct 3 で 1 = A3
KL = Key("Bb", "major")         # 最後のサビ（+1）

INTRO = ["Amaj7", "B/A", "Amaj7", "B/A"]
A_CH = ["Amaj7", "B/A", "Amaj7", "B/A", "F#m7", "C#m7", "Dmaj7", "E"]
B_CH = ["Dmaj7", "E", "C#m7", "F#m7", "Dmaj7", "E", "Bm7", "E7sus4"]
C_CH = ["A", "E/G#", "F#m7", "D", "A", "E", "Bm7", "E", "A", "E/G#", "F#m7", "D", "A", "E", "Bm7", "A"]
X_CH = ["F#m7", "D", "E", "C#m7", "F#m7", "D", "Bm7", "E"]
LAST = [tr_chord(c, 1) for c in C_CH + C_CH[8:]]

S.scene("信号", 8, "intro", INTRO * 2)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 12, "solo", INTRO * 2 + ["F#m7", "C#m7", "Dmaj7", "E"])
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("ばれそう", 8, "bridge", X_CH[:7] + ["F7"])          # 最後の小節は +1 への入り口
S.scene("最後のサビ", 24, "chorus", LAST)
S.scene("よろしく", 8, "outro", [tr_chord(c, 1) for c in INTRO] + ["Bbmaj7", "C/Bb", "Bbmaj9", "Bbmaj9"])

V = Voice(S, vol=0.21, delay=0.75, bright=1.0, patch="brightLead", low=True)
ARP = S.track("宇宙の信号（アルペジオ）", "lead", patch="surgeDnaSeq", volume=0.065, pan=-0.25, reverb=0.3, mono=True,
              fx=[{"type": "filter", "kind": "highpass", "freq": 350, "q": 0.7}, {"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.35}])
ARP2 = S.track("トランスのアルペジオ（16分）", "pad", patch="pluckSynth", volume=0.06, pan=0.3, reverb=0.3, sustain=0.4,
               fx=[{"type": "filter", "kind": "highpass", "freq": 400, "q": 0.7}])
GATE = [S.track(f"刻まれるパッド{i + 1}", "pad", patch="surgePadSparkly", volume=0.045, pan=-0.3 + 0.3 * i, reverb=0.3, sustain=0.25) for i in range(3)]
SAW = [S.track(f"スーパーソー{i + 1}", "pad", **pad_spec("surgeHappySaws", vol=0.04, pan=-0.45 + 0.45 * i, duck=0.45, sustain=0.9)) for i in range(3)]
TLEAD = S.track("トランスのリード（間奏）", "lead", patch="surgeTropics", volume=0.1, pan=0.0, reverb=0.35, mono=True,
                fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
BELL = S.track("ベル（星）", "pad", patch="surgeFantasyBell", volume=0.055, pan=0.4, reverb=0.45, sustain=1.0)
BASS = S.track("ベース", "bass", **finger_bass_spec(vol=0.21))
PN = [S.track(f"ピアノ{i + 1}", "piano", volume=0.09, pan=-0.12, reverb=0.25, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 3}]) for i in range(3)]
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.065, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 5:0.5 #4:0.5 5:0.5 1':1 7:1", "3':1.5 #4':0.5 3':1 R:1", "R:0.5 5:0.5 #4:0.5 5:0.5 2':1 1':1", "7:2 R:2",
      "R:0.5 3:0.5 3:0.5 6:0.5 1':1 6:1", "5:1.5 3:0.5 2:1 R:1", "R:0.5 4:0.5 5:0.5 6:0.5 1':1 2':1", "7:2 R:2"]
A1 = "てんこうしょにちの/あさのくらす/じこしょうかいでね/くちがすべった/うちゅうからきたの/うそついちゃった/きょうしつのみんな/しーんとした"
A2 = "やすみじかんにね/となりのこが/うちゅうのことばで/はなしかけた/わたしもしらない/うちゅうごだよ/ふたりでつくったの/ひみつのこえ"
VB = ["R:0.5 1':0.5 1':0.5 2':0.5 3':1 2':1", "7:1.5 6:0.5 5:1 R:1", "R:0.5 1':0.5 1':0.5 2':0.5 3':1 5':1", "3':1.5 2':0.5 1':1 R:1",
      "R:0.5 4':0.5 4':0.5 3':0.5 2':1 3':1", "4':1.5 3':0.5 2':1 R:1", "R:0.5 2':0.5 3':0.5 4':0.5 5':1 4':1", "3':2 R:2"]
B1 = "きみだけわらったの/どのほしなのってね/わたしはとっさにね/うそかさねた"
B2 = "だけどほんとうは/ふつうのわたしで/ともだちでいたい/いえるかなあ"
VC = ["R:0.5 3:0.5 5:0.5 1':0.5 3':1 2':1", "2':1 7:1 5:1 R:1", "R:0.5 3:0.5 6:0.5 1':0.5 3':1 2':1", "1':1.5 6:0.5 1':1 R:1",
      "R:0.5 3:0.5 5:0.5 1':0.5 3':1 5':1", "4':1 3':1 2':1 R:1", "R:0.5 2':0.5 3':0.5 4':0.5 5':1 4':1", "3':2 R:2"]
VC2 = VC[:6] + ["R:0.5 4':0.5 3':0.5 2':0.5 1':1 2':1", "1':2 R:2"]
C1 = "ほんとのことをね/いまからいうから/うちゅうじんじゃない/ただのわたし/それでもいいなら/もういちどいうね/はじめましてだよ/よろしくだね"
C2 = "うちゅうごじゃなくて/にほんごでいうよ/ふるえるこえでも/いいたいんだ/きみがいたからね/こわくなんかない/ありがとうっていう/ほんとうだよ"
CL = C1 + "/ほしのなまえはね/まだきめてないの/ふたりのほしだよ/またあしたね"
VX = ["R:1 6:1 5:1 3:1", "5:3 R:1", "R:1 5:1 7:1 2':1", "3':3 R:1", "R:1 6:1 5:1 3:1", "5:3 R:1", "R:1 4:1 6:1 1':1", "7:4"]
X1 = "ばれちゃう/どうしよ/むねがね/ひかるの"
GREET = ["R:4", "R:4", "R:4", "R:4", "R:1 3':0.5 5':0.5 6':1 5':1", "R:4", "R:4", "R:4"]       # 宇宙語のあいさつ（「よろしく」を逆さに）
LY = Lyrics(S)


def put(name, key, lines, text, o=3):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("信号", K, GREET, "よろしく")
put("Aメロ1", K, VA + VA, A1)
put("Bメロ1", K, VB, B1); put("Bメロ2", K, VB, B2)
put("サビ1", K, VC + VC2, C1); put("サビ2", K, VC + VC2, C2)
put("ばれそう", K, VX, X1)
put("最後のサビ", KL, VC + VC2 + VC2, CL)
put("よろしく", KL, ["R:4"] * 3 + ["R:1 3:0.5 5:0.5 6:1 1':1", "R:4", "R:4", "R:4", "R:4"], "よろしく")
if VOCAL: put("Aメロ2", K, VA + VA, A2)
else:
    for i, (b, l) in enumerate(zip(S.sc("Aメロ2"), VA + VA)):
        if i < 8: BELL.bar(b, K.mel(l, oct=4))
        else: V.bar(b, K.mel(l, oct=3))

# ================= アルペジオ・刻まれるパッド・スーパーソー・ピアノ =================
TL = ["R:0.5 E5:0.5 D#5:0.5 E5:0.5 A5:1 G#5:1", "C#6:1.5 D#6:0.5 C#6:1 B5:1", "R:0.5 E5:0.5 D#5:0.5 E5:0.5 B5:1 A5:1", "G#5:3 R:1",
      "R:0.5 C#6:0.5 E6:0.5 F#6:0.5 A6:1 F#6:1", "E6:1.5 C#6:0.5 B5:1 R:1", "R:0.5 D6:0.5 E6:0.5 F#6:0.5 A6:1 B6:1", "G#6:2 E6:2",
      "A6:1 G#6:0.5 E6:0.5 C#6:1 E6:1", "F#6:1 E6:0.5 C#6:0.5 B5:1 A5:1", "D6:1 C#6:0.5 B5:0.5 A5:1 F#5:1", "G#5:2 B5:1 E6:1"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; v = voice(ch, 64, 3); t = tones(ch, "E4", "E6")
    ARP_ON = n in ("信号", "Aメロ1", "Aメロ2", "間奏", "よろしく") or n.startswith(("サビ", "最後"))
    if ARP_ON and not (n == "Aメロ1" and i < 4):
        ARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 4, 3, 1, 3, 2, 4)))
    if n.startswith(("サビ", "最後")) or n == "間奏":
        ARP2.bar(b, piano_arp16(ch, "A4", "A6", pat=(0, 2, 4, 2, 1, 3, 5, 3)))
        sv = voice(ch, 64, 3)
        for j in range(3): SAW[j].bar(b, f"{nm(sv[j])}:1.5 {nm(sv[j])}:1 {nm(sv[j])}:1.5")
    if n in ("Bメロ1", "Bメロ2") or (n in ("Aメロ1", "Aメロ2") and i >= 8) or n == "信号":
        for j in range(3): GATE[j].bar(b, " ".join(f"{nm(v[j])}:0.25" if q % 2 == 0 else "R:0.25" for q in range(16)))
    if n == "間奏": TLEAD.bar(b, TL[i])
    if n in ("Bメロ1", "Bメロ2", "ばれそう"):
        for j in range(3): PN[j].bar(b, f"{nm(v[j])}:2 {nm(v[j])}:2" if n != "ばれそう" else f"{nm(v[j])}:4")
    if n == "よろしく":
        if i < 4:
            for j in range(3): SAW[j].bar(b, f"{nm(v[j])}:4")
        elif i == 6:
            for j in range(3): PN[j].bar(b, f"{nm(v[j])}:8")
    if n in ("Aメロ1", "Aメロ2", "サビ1", "サビ2", "最後のサビ") and i % 8 == 7:
        BELL.bar(b, "R:2 " + " ".join(f"{nm(x + 12)}:0.5" for x in t[2:6]))

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "信号":
        if i >= 4: BASS.bar(b, bass_line(S, b, "long", lo="E1"))
    elif n in ("Aメロ1", "Aメロ2"): BASS.bar(b, bass_line(S, b, "half" if i < 8 else "house", lo="E1"))
    elif n in ("Bメロ1", "Bメロ2"): BASS.bar(b, bass_line(S, b, "root8", lo="E1"))
    elif n.startswith(("サビ", "最後")) or n == "間奏": BASS.bar(b, bass_line(S, b, "house" if i % 4 != 3 else "oct8", lo="E1"))
    elif n == "ばれそう": BASS.bar(b, bass_line(S, b, "long", lo="E1"))
    elif n == "よろしく" and i < 7: BASS.bar(b, bass_line(S, b, "house" if i < 4 else "long", lo="E1"))

riser(FX, S.sc("サビ1")[0], 4, "C4"); riser(FX, S.sc("最後のサビ")[0], 8, "D4")
cym_swell(CYM, S.sc("サビ2")[0], 2, "C4")

# ================= ドラム（トランスの4つ打ち・裏で開くハイハット） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "信号":
        if i >= 4: vgroove(D, b, "four", ghosts=0, seed=b, s="................", vary=False)
        if i == 7: put_fill(D, b, "lift")
    elif n in ("Aメロ1", "Aメロ2"):
        vgroove(D, b, "half" if i < 8 else "four", ghosts=0.2, seed=b)
        if i == 0: crash(D, b)
        if i == 15: put_fill(D, b, "snare16")
    elif n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "halfdrive", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
    elif n.startswith(("サビ", "最後")):
        vgroove(D, b, "four16", ghosts=0.2, seed=b)
        if i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
        if i % 8 == 7 and not last: put_fill(D, b, "small" if i % 16 == 7 else "tomdown")
    elif n == "間奏":
        vgroove(D, b, "four", ghosts=0.2, seed=b)
        if i in (0, 8): crash(D, b)
        if last: put_fill(D, b, "lift")
    elif n == "ばれそう":
        vgroove(D, b, "half", ghosts=0.15, seed=b)
        if last: put_fill(D, b, "build")
    elif n == "よろしく" and i < 4:
        vgroove(D, b, "four", ghosts=0.1, seed=b)

SIL.add(S.sc("最後のサビ")[0] - 1, 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の07。エレクトロニカ（エレクトロポップ×トランス）。A 長調・138、最後のサビは +1（B♭）。"
          "転校初日に「宇宙人です」とうそをついた。そのうそで最初の友だちができた。宇宙の信号のようなアルペジオと、宇宙語のような逆再生のあいさつで始まり、"
          "リディアの不思議な跳びの Aメロ、素直な長調のサビ、トランスのリードの間奏、ばれそうな静けさ、最後は「よろしく」の1音。自作")
REV = [{"type": "reverse", "scene": "信号", "bars": [4, 6], "bpm": 138}]
finish(S, LY, V, 0, fx=REV, level={"verse": -0.25}, special={"ばれそう": -0.55, "最後のサビ": 0.5, "信号": -0.2})
