# vt25 14「午前0時のポップコーン」Midnight Popcorn（仮）— ロック（ポップパンク）。200・4/4。G 長調 → 最後のサビは +2（A）。
# 物語: 受験勉強の夜、午前0時。台所の電気をそっとつける。問題集はまだ半分。おなかの虫がぐうと鳴いて、ポップコーンを出す。ひみつだよ。
#   鍋にふたをして火をつけたら、ぽんっとはじけだす。かたい種でも、熱が加われば、ふわっと開く。わたしみたい。
#   階段に親の足音、しーん。セーフ。数学は苦手だけど、負けたくない。がんばれわたし、って小さく言う。最後のひとつぶを食べちゃおうか。
# 場面と強さ: カウント（「ワン・ツー」とキック）→ イントロ（ギター・強）→ Aメロ1（跳ねる・中）→ Bメロ1（止め1）→ サビ1（24小節・強）→ 間奏（ポップコーンのリフ）
#   → Aメロ2 → Bメロ2（止め2）→ サビ2（24小節）→ はじける（ポップコーンがいちばんはじける間奏）→ 足音（Cメロ・ハーフ・頭で止め3＝親の足音に固まる）→ ギターソロ → 1拍の無音
#   → 最後のサビ（+2・24小節・いちばん強い）→ アウトロ（急に止める）
# 旋律の性格: 跳ねる8分（D4〜B4）。掛け声のような短い句。サビは G4 → B4 → D5 の三和音を駆け上がる。最高音は最後のサビの F#5。
# ほかの曲とちがう所（この曲だけの音）: ポップコーンのはじける音（はじける短いシンセとカホンの縁）が、Aメロ2 とサビのリズムに入る（だんだん数がふえる）。
#   和音は I・V・vi・IV の決まった回しを避けて、IV・V・iii・vi で回す。
from vt25_lib import *

S = Song("14", "popcorn", "午前0時のポップコーン（仮）", "Midnight Popcorn", 200, 4, "G", "major", "ロック（ポップパンク・ボカロ）")
S.kit = "naked-x"
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags + " --piano salamander"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.6
S.keepers = {"Aメロ2": "ride", "サビ2": "open", "最後のサビ": "wash", "ギターソロ": "bell"}
K = Key("G", "major")           # oct 3 で 1 = G3。歌うのは D4〜E5
KL = Key("A", "major")          # 最後のサビ（+2）

A_CH = ["G", "Bm", "Em", "C", "G", "Bm", "Am", "D"]
B_CH = ["Am", "Bm", "C", "D", "Am", "Bm", "C", "D"]
C_CH = ["C", "D", "Bm", "Em", "C", "D", "G", "G", "C", "D", "Bm", "Em", "Am", "D", "G", "G"]
X_CH = ["C", "D", "Bm", "Em", "C", "D", "G", "D"]
LAST = [tr_chord(c, 2) for c in C_CH + C_CH[8:]]

S.scene("カウント", 2, "intro", ["G", "G"])
S.scene("イントロ", 14, "intro", ["C", "D", "Bm", "Em"] * 3 + ["Am", "D"])
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 24, "chorus", C_CH + C_CH[8:])
S.scene("間奏", 12, "break", ["C", "D", "Bm", "Em"] * 3)
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 24, "chorus", C_CH + C_CH[8:])
S.scene("はじける", 8, "break", ["C", "D", "Bm", "Em"] * 2)       # 間奏: ポップコーンがいちばんたくさんはじける
S.scene("足音", 16, "bridge", X_CH * 2)
S.scene("ギターソロ", 16, "solo", ["C", "D", "Bm", "Em"] * 3 + ["Am", "Bm", "C", "E7"])
S.scene("最後のサビ", 24, "chorus", LAST)
S.scene("アウトロ", 14, "outro", [tr_chord(c, 2) for c in ["C", "D", "Bm", "Em"] * 3] + ["A", "A"])

V = Voice(S, vol=0.22, delay=0.75, bright=0.8, patch="picoLead", low=True)
GT = [S.track(f"ギター1（{['根音', '5度', 'オクターブ'][i]}）", "distGuitar", **rock_gtr_spec(0.07, -0.45 + 0.45 * i)) for i in range(3)]
LG = S.track("ギター2（リフ）", "leadGuitar", **lead_gtr_spec(0.11, 0.2))
LGS = S.track("ギター2（ソロ）", "leadGuitar", **lead_gtr_spec(0.15, 0.0))
ORG = [S.track(f"オルガン{i + 1}", "drawbarOrgan", volume=0.05, pan=0.3, reverb=0.25, sustain=1.0) for i in range(3)]
BASS = S.track("ベース", "bass", **rock_bass_spec(0.24))
POP = S.track("ポップコーン（はじける音）", "pad", patch="surgePopcorn", volume=0.06, pan=0.4, reverb=0.2, sustain=0.2)
POPK = S.track("ポップコーン（カホンの縁）", "cajon", volume=0.07, pan=-0.35, reverb=0.12)
CLAP = S.track("手拍子とカウント（カホン）", "cajon", volume=0.1, pan=0.0, reverb=0.2)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.065, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 5:0.5 5:0.5 6:0.5 1':1 5:1", "7:1 6:1 5:1 R:1", "R:0.5 5:0.5 5:0.5 6:0.5 7:1 6:1", "5:1.5 3:0.5 5:1 R:1",
      "R:0.5 1':0.5 1':0.5 2':0.5 3':1 2':1", "2':1 7:1 5:1 R:1", "R:0.5 6:0.5 6:0.5 1':0.5 2':1 1':1", "2':2 R:2"]
A1 = "ごぜんれいじだよ/きっちんのでんきを/そっとつけてみたの/まだはんぶん/おなかのむしがね/ぐうってないたから/ぽっぷこーんをだす/ひみつだよね"
A2 = "なべにふたをして/ひをつけたらほら/ぽんっとはじけだす/わたしみたい/かたいたねでもね/ねつがくわわれば/ふわっとひらくんだ/そうなんだよ"
VB = ["R:0.5 1':0.5 1':0.5 2':0.5 3':1 1':1", "2':1.5 1':0.5 7:1 R:1", "R:0.5 3':0.5 3':0.5 4':0.5 5':1 3':1", "2':1.5 1':0.5 2':1 R:1",
      "R:0.5 3':0.5 3':0.5 4':0.5 5':1 6':1", "5':1.5 4':0.5 3':1 R:1", "R:0.5 4':0.5 5':0.5 6':0.5 5':1 4':1", "5':2 R:2"]
B1 = "すうがくのしけん/にがてなんだけど/まけたくないから/がんばるんだ"
B2 = "ぽっぷこーんのおと/ちょっぴりうるさいね/しーっとゆびたてて/わらいこらえ"
VC = ["R:0.5 1':0.5 3':0.5 5':0.5 5':1 4':1", "3':1 2':1 2':1 R:1", "R:0.5 7:0.5 2':0.5 5':0.5 5':1 3':1", "3':1.5 2':0.5 1':1 R:1",
      "R:0.5 1':0.5 3':0.5 5':0.5 6':1 5':1", "4':1 3':1 2':1 R:1", "R:0.5 1':0.5 2':0.5 3':0.5 5':1 3':1", "1':2 R:2"]
VC2 = VC[:4] + ["R:0.5 1':0.5 3':0.5 5':0.5 6':1 5':1", "4':1 3':1 2':1 R:1", "R:0.5 3':0.5 3':0.5 2':0.5 1':1 2':1", "1':2 R:2"]
C1 = ("ぽっぷこーんはじけ/よなかのだいどこ/がんばれわたしって/ちいさくいう/ぽっぷこーんだから/まだかたいけれど/あしたはきっとほら/はじけるんだ/"
      "ぽっぷこーんはじけ/しおかばたーかで/まよってるうちにね/よがあけそう")
C2 = ("ぽっぷこーんはじけ/しおかばたーかで/まよってるうちにね/よがあけそう/ぽっぷこーんだから/ゆうきもはじける/めをこすりながら/もういちどね/"
      "ぽっぷこーんはじけ/てすとのひのあさ/わたしのなかでね/はじけるかな")
CL = ("ぽっぷこーんはじけ/ごうかくのさくら/さいたらいいなって/ゆめにみるよ/ぽっぷこーんだから/はじけるひまでね/がんばれわたしって/いうんだよね/"
      "ぽっぷこーんはじけ/よるがあけていく/さいごのひとつぶ/たべちゃおうか")
VX = ["R:1 3':1 2':1 1':1", "2':3 R:1", "R:1 3':1 5':1 6':1", "5':3 R:1", "R:1 6':1 5':1 3':1", "2':3 R:1", "R:1 1':1 2':1 3':1", "2':3 R:1"]
X1 = "あしおと/かいだん/まずいよ/かくれて/しーんと/せーふだ/わらうよ/がんばる"
LY = Lyrics(S)


def put(name, key, lines, text, o=3):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA + VA, A1)
put("Bメロ1", K, VB, B1); put("Bメロ2", K, VB, B2)
put("サビ1", K, VC + VC2 + VC2, C1); put("サビ2", K, VC + VC2 + VC2, C2)
put("足音", K, VX + VX, X1)
put("最後のサビ", KL, VC + VC2 + VC2, CL)
if VOCAL: put("Aメロ2", K, VA + VA, A2)
else:
    for i, (b, l) in enumerate(zip(S.sc("Aメロ2"), VA + VA)):
        if i < 8: LG.bar(b, K.mel(l, oct=4))
        else: V.bar(b, K.mel(l, oct=3))

# ================= ギター =================
# 2026-11-04 v2: 人間「トライデントの音の割には高すぎて音が強く感じる」→ リードギターを1オクターブ下げる（中音域で太く鳴らす）
RIFF = ["G4:0.5 E4:0.25 G4:0.25 A4:0.5 G4:0.5 E4:0.5 D4:0.5 C4:0.5 D4:0.5", "F#4:0.5 D4:0.25 F#4:0.25 A4:0.5 F#4:0.5 D4:1 E4:0.5 F#4:0.5",
        "D4:0.5 B3:0.25 D4:0.25 F#4:0.5 D4:0.5 B3:0.5 A3:0.5 B3:0.5 D4:0.5", "E4:0.5 G4:0.5 B4:1 A4:0.5 G4:0.5 E4:1"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; pw = power(ch, "E2")
    if n == "カウント": continue
    if n in ("イントロ", "間奏", "はじける") or (n == "アウトロ" and i < 12):
        LG.bar(b, RIFF[i % 4] if n != "アウトロ" else " ".join(f"{nm(midi(x.split(':')[0]) + 2)}:{x.split(':')[1]}" for x in RIFF[i % 4].split()))
    if n == "足音":
        for j in range(3): GT[j].bar(b, f"{nm(pw[j])}:4" if i % 2 == 0 else f"{nm(pw[j])}:2 R:2")
    elif n in ("Aメロ1", "Aメロ2") and i < 8:
        for j in range(3): GT[j].bar(b, f"{nm(pw[j])}:1 R:1 {nm(pw[j])}:0.5 {nm(pw[j])}:0.5 R:1")
    elif n == "アウトロ" and i >= 12:
        if i == 12:
            for j in range(3): GT[j].bar(b, f"{nm(pw[j])}:0.5! R:3.5")
    else:
        for j in range(3): GT[j].bar(b, " ".join(f"{nm(pw[j])}:0.5{'!' if q % 4 == 0 else ''}" for q in range(8)))
SOLO = ["G4:0.5 A4:0.5 B4:1^ A4:0.5 G4:0.5 E4:1", "F#4:0.5 A4:0.5 D5:2~ R:1", "B4:0.25 A4:0.25 G4:0.25 F#4:0.25 D4:0.5 F#4:0.5 B4:2", "G4:1 E4:1 B3:2~",
        "C5:0.5 B4:0.5 A4:0.5 G4:0.5 A4:1 B4:1", "D5:1^ C5:0.5 B4:0.5 A4:2~", "F#4:0.5 G4:0.5 A4:0.5 B4:0.5 D5:1 B4:1", "E5:3~ R:1",
        "G4:0.25 B4:0.25 D5:0.25 G5:0.25 F#5:1 D5:1 B4:1", "A4:0.25 C5:0.25 E5:0.25 A5:0.25 G5:1 E5:1 D5:1", "F#4:0.5 A4:0.5 D5:0.5 F#5:0.5 E5:1 D5:1", "B4:2 G4:2",
        "A4:1 C5:1 E5:1 A5:1", "B4:1 D5:1 F#5:1 B5:1^", "C5:1 E5:1 G5:1 C6:1", "B5:2~ G#5:2"]
for i, b in enumerate(S.sc("ギターソロ")): LGS.bar(b, SOLO[i])

# ================= オルガン・ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; ov = voice(ch, 62, 3)
    if n.startswith(("サビ", "最後")) or n == "ギターソロ":
        for j in range(3): ORG[j].bar(b, f"{nm(ov[j])}:4")
    if n == "カウント": continue
    if n == "アウトロ" and i >= 12:
        if i == 12: BASS.bar(b, f"{nm(low(ch, 'E1'))}:0.5! R:3.5")
        continue
    if n == "足音": BASS.bar(b, bass_line(S, b, "half", lo="E1"))
    elif n in ("Aメロ1", "Aメロ2") and i < 8: BASS.bar(b, bass_line(S, b, "push", lo="E1"))
    else: BASS.bar(b, bass_line(S, b, "root8", lo="E1"))

# ================= ポップコーン（Aメロ2 とサビで、だんだん数がふえる） =================
rnd = random.Random(1414)
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    cnt = 0
    if n == "Aメロ2": cnt = 1 + i // 4
    elif n in ("サビ1", "サビ2"): cnt = 3
    elif n == "最後のサビ": cnt = 4 + i // 8
    elif n == "間奏": cnt = 2
    elif n == "はじける": cnt = 4 + i
    t = tones(S.chords[b], "C6", "C7")
    for j in range(cnt):
        st = rnd.choice([x * 0.25 for x in range(16)])
        POP.at(S.bar_beat(b) + st, f"{nm(rnd.choice(t))}:0.25")
        POPK.at(S.bar_beat(b) + rnd.choice([x * 0.25 for x in range(16)]), "G3:0.25")
CLAP.bar(S.sc("カウント")[0], "G3:1! R:1 G3:1! R:1"); CLAP.bar(S.sc("カウント")[1], "G3:1! G3:1! G3:1! G3:1!")
for name in ("サビ1", "サビ2", "最後のサビ"):
    for i, b in enumerate(S.sc(name)):
        if i % 2 == 1: CLAP.bar(b, "R:1 G3:1 R:1 G3:1")
riser(FX, S.sc("サビ1")[0], 4, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 2, "E4")

# ================= ドラム（ポップパンクの2ビート寄り） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "カウント":
        D.set(b, "X.......X......." if i == 1 else "................", "................", "x...x...x...x...")
    elif n in ("イントロ", "間奏", "はじける"):
        vgroove(D, b, "punk", ghosts=0.2, seed=b)
        if i % 4 == 0: crash(D, b)
        if last: put_fill(D, b, "snare16")
    elif n in ("Aメロ1", "Aメロ2"):
        vgroove(D, b, "beat8" if i < 8 else "punk", ghosts=0.3, seed=b)
        if i == 0: crash(D, b)
        if i == 7: put_fill(D, b, "small")
    elif n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "halfdrive", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 1)
    elif n.startswith(("サビ", "最後")):
        vgroove(D, b, "punk", ghosts=0.25, seed=b)
        if i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
        if i % 8 == 7 and not last: put_fill(D, b, "tomdown" if i % 16 == 15 else "small")
    elif n == "足音":
        vgroove(D, b, "half", ghosts=0.2, seed=b)
        if last: put_fill(D, b, "build")
    elif n == "ギターソロ":
        vgroove(D, b, "punk", ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b)
    elif n == "アウトロ":
        if i < 12: vgroove(D, b, "punk", ghosts=0.2, seed=b)
        if i in (0, 8): crash(D, b)
        if i == 11: put_fill(D, b, "snare16")
        if i == 12: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 6)

# 止め3回: Bメロ1・Bメロ2 の最後、足音の頭（親の足音に固まる）。1拍の完全な無音: 最後のサビの直前
for name in ("Bメロ1", "Bメロ2"): SIL.add(S.sc(name)[-1], 1, 4)
SIL.add(S.sc("足音")[0], 1, 4)
SIL.add(S.sc("最後のサビ")[0] - 1, 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の14。ロック（ポップパンク）。G 長調・200、最後のサビは +2（A）。"
          "受験勉強の夜、こっそりポップコーンを作りながら、自分で自分を応援する。「ワン・ツー」のカウントとキックで始まり、跳ねる8分の Aメロ、"
          "ポップコーンのはじける音がリズムに入ってだんだん増える、止め3回（親の足音に固まる）、ギターソロ、1拍の無音から +2 の最後のサビ、急に止めて終わる。自作")
finish(S, LY, V, 0, level={"verse": -0.2}, special={"足音": -0.4, "最後のサビ": 0.55})
