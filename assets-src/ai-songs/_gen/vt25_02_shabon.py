# vt25 02「シャボン玉フォルテッシモ」Soap Bubble Fortissimo（仮）— J-POP（疾走ピアノ）。176・4/4。A♭長調 → 最後のサビは +2（B♭）。
# 物語: 合唱コンクールの練習。音楽室のすみの「わたし」は、口だけ動かして声を出さない。声はシャボン玉みたいに、出したとたんに消えそうで。
#   放課後のろうかでひとり練習していると、となりの子が「いっしょに歌おう」と笑ってくれた。本番の前の日、鏡の前で大きく口を開けたら、声が出た。
#   本番。指揮者が手を上げる1小節の静けさ。そして、ありったけの声で歌う。わたしの声が、みんなの声と重なって、空へのぼっていく。
# 場面と強さ: 音楽室（合唱曲ふうのピアノの和音・テンポどおり）→ Aメロ1（小さな声・弱）→ Bメロ1（鏡の前・ためる）→ サビ1（強）
#   → 間奏（ピアノの16分）→ Aメロ2（放課後のろうか）→ Bメロ2（舞台の上）→ サビ2（声が重なりはじめる・強）→ 間奏2（ピアノのソロ）
#   → Cメロ（こわかった・ハーフの重さ）→ 手を上げる（1小節の完全な無音）→ 落ちサビ（ピアノとテトだけ・とても弱い）
#   → 最後のサビ（+2・みんなの声・いちばん強い）→ 後奏（全員でのばす和音）
# 旋律の性格: 小さく始まり、句ごとに一段ずつ高くなる（Aメロの4つの句の頭が C4 → D♭4 → E♭4 → F4 と上がる）。サビは5度の跳躍で入り、
#   長い音でのびやかに。最高音は最後のサビの F5。
# ほかの曲とちがう所（この曲だけの音）: サビでテトの声が「何人もの声」に増えていく（歌の重ね＝ダブラー。サビ2で少し、最後のサビでいっぱいに）。
#   合唱の声（choir）が最後のサビで同じ旋律を歌う。1小節の完全な無音（指揮者が手を上げる）。
from vt25_lib import *

S = Song("02", "shabon", "シャボン玉フォルテッシモ（仮）", "Soap Bubble Fortissimo", 176, 4, "Ab", "major", "J-POP（疾走ピアノ・ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --piano salamander --space hall --space-wet 0.14"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.55
K = Key("Ab", "major")          # oct 3 で 1 = A♭3
KL = Key("Bb", "major")         # 最後のサビ（+2）

A_CH = ["Ab", "Eb/G", "Dbmaj7", "Bbm7", "Cm7", "Eb", "Fm7", "Eb"]
B_CH = ["Dbmaj7", "Eb", "Cm7", "Fm7", "Dbmaj7", "Fm7", "Dbmaj7", "Eb7"]
C_CH = ["Ab", "Eb/G", "Fm7", "Dbmaj7", "Bbm7", "Eb", "Fm7", "Ab"]
C_CH2 = C_CH[:6] + ["Dbmaj7", "Ab"]
X_CH = ["Fm7", "Db", "Eb", "Ab", "Fm7", "Db", "Bbm7", "Eb"]
LAST = [tr_chord(c, 2) for c in C_CH + C_CH2 + C_CH2]

S.scene("音楽室", 8, "intro", ["Ab", "Db/Ab", "Fm7", "Eb", "Db", "Ab/C", "Bbm7", "Eb"])
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH + C_CH2)
S.scene("間奏", 8, "break", ["Ab", "Eb/G", "Fm7", "Dbmaj7", "Ab", "Eb/G", "Dbmaj7", "Eb"])
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 24, "chorus", C_CH + C_CH2 + C_CH2)
S.scene("間奏2", 16, "solo", ["Dbmaj7", "Eb", "Cm7", "Fm7", "Dbmaj7", "Eb", "Ab", "Ab"] * 2)
S.scene("Cメロ", 16, "bridge", X_CH * 2)
S.scene("手を上げる", 1, "break", ["Eb"])
S.scene("落ちサビ", 8, "bridge", C_CH[:7] + ["F7"])           # 最後の小節は B♭ への入り口（F7）
S.scene("最後のサビ", 24, "chorus", LAST)
S.scene("後奏", 8, "outro", ["Ebmaj7", "F", "Dm7", "Gm7", "Ebmaj7", "F", "Bb", "Bb"])

V = Voice(S, vol=0.22, delay=0.75, bright=0.5, patch="flute", low=False)
PL = S.track("ピアノ（左手）", "piano", volume=0.14, pan=-0.12, reverb=0.24, fx=[{"type": "eq", "low": -1, "mid": -2, "midHz": 400, "high": 2}])
PR = S.track("ピアノ（右手）", "piano", volume=0.14, pan=-0.12, reverb=0.24, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 3.5}])
PR2 = S.track("ピアノ（右手の上の音）", "piano", volume=0.12, pan=-0.12, reverb=0.24, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 3.5}])
PRM = S.track("ピアノ（歌を受け取る）", "piano", volume=0.17, pan=-0.12, reverb=0.24, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 3}])
BASS = S.track("ベース", "bass", **finger_bass_spec(vol=0.2))
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.07, pan=-0.35 + 0.35 * i, reverb=0.42, sustain=1.4) for i in range(3)]
VLN = S.track("バイオリン（対旋律）", "fiddle", patch="violin", volume=0.08, pan=0.3, reverb=0.42, gainDb=1, bright=-0.3, attack=0.08, release=0.5)
# 2026-11-04 v2: 合唱の音（choir）があるサビが点数を下げていた（サビ2 6.38・最後のサビ 7.01、ほかの場面は 7.5〜8.1）→ クラスの声はゆっくりした弦（slowStrings）に。
#   同じ旋律の合唱はやめた（歌の版は、テトの歌の重ね＝ダブラーが「みんなの声」になる）
CHO = [S.track(f"クラスの声のかわり（ゆっくりした弦）{i + 1}", "strings", patch="slowStrings", volume=0.06, pan=-0.3 + 0.3 * i, reverb=0.45, sustain=1.4) for i in range(3)]
GLK = S.track("グロッケン（シャボン玉）", "glockenspiel", patch="glockenspiel", volume=0.06, pan=0.45, reverb=0.45)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の旋律と歌詞（A♭長調の度数。oct 3 で 1 = A♭3） =================
VA = ["R:1 3:0.5 3:0.5 3:1 2:0.5 3:0.5", "5:1.5 3:0.5 2:1 R:1", "R:1 4:0.5 4:0.5 4:1 3:0.5 4:0.5", "6:1.5 4:0.5 3:1 R:1",
      "R:1 5:0.5 5:0.5 5:1 4:0.5 5:0.5", "7:1.5 5:0.5 4:1 R:1", "R:1 6:0.5 6:0.5 1':1 7:0.5 6:0.5", "5:3 R:1"]
A1 = "すみっこのいちれつ/くちだけうごかす/わたしのこえはね/すぐにきえる/せんせいはいうの/おなかからこえを/わかっているけれど/ふるえちゃうの"
A2 = "ほうかごのろうか/ひとりでれんしゅう/まどにうつるかお/まっかでわらう/となりのあのこが/いっしょにうたおうと/わらってくれたから/がんばれるよ"
VB = ["R:0.5 1':0.5 1':0.5 7:0.5 6:1 5:1", "6:1.5 5:0.5 5:1 R:1", "R:0.5 2':0.5 2':0.5 1':0.5 7:1 6:1", "1':1.5 7:0.5 6:1 R:1",
      "R:0.5 3':0.5 3':0.5 2':0.5 1':1 2':1", "3':1.5 2':0.5 1':1 R:1", "R:0.5 4':0.5 3':0.5 2':0.5 1':0.5 2':0.5 3':1", "2':2 R:2"]
B1 = "ほんばんまえのひ/かがみのまえでね/おおきくあけたら/こえがでたんだ"
B2 = "ぶたいのうえはね/ひかりがまぶしい/ゆびさきつめたい/でもだいじょうぶ"
VC = ["R:0.5 5:0.5 1':1 2':0.5 3':1.5", "2':1 3':1 2':1.5 R:0.5", "R:0.5 5:0.5 1':1 2':0.5 3':1 4':0.5", "3':1.5 2':0.5 1':1.5 R:0.5",
      "R:0.5 5':0.5 5':1 4':0.5 3':1.5", "2':1 3':1 4':1.5 R:0.5", "R:0.5 3':0.5 3':0.5 2':0.5 1':1 2':1", "1':3 R:1"]
VC2 = VC[:6] + ["R:0.5 5':0.5 5':0.5 4':0.5 3':1 2':1", "1':3 R:1"]
C1 = ("しゃぼんだまいま/そらへのぼってゆく/わたしのこえも/とんでいけよ/"
      "ふぉるてっしもへと/ふぉるてっしものそら/とどけみんなへ/わらってうたう")
C2 = ("しゃぼんだままた/ふくらむこころが/はじけるまえに/うたうんだよ/ふぉるてっしもまで/みんなのこえとね/かさなるんだよ/ひとりじゃない/"
      "しゃぼんだまとぶ/まどのそとへとぶ/にじいろのそら/きらきらだね")
CO = "しゃぼんだまそっと/てのひらにのせて/いきをすいこむ/いまなんだね"
CL = ("しゃぼんだまいけ/ありったけのこえで/おおきなこえで/うたうんだよ/しゃぼんだまとべ/かくしてたぶんも/そらまでとどけ/わたしのうた/"
      "しゃぼんだまぱっと/はじけてもいいよ/こえはのこるよ/ふぉるてっしもー")
VX = ["R:1 6:1 1':1 7:1", "6:2 5:2", "R:1 5:1 7:1 2':1", "1':3 R:1", "R:1 6:1 1':1 2':1", "3':2 2':2", "R:1 1':1 2':1 3':1", "2':4"]
X1 = "わらわれる/こわかった/おおごえは/むりだった/でもきょうは/ちがうよ/みんながね/まってるの"
LY = Lyrics(S)


def put(name, key, lines, text, o=3):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)
    return mel


put("Aメロ1", K, VA + VA, A1)
put("Bメロ1", K, VB, B1); put("Bメロ2", K, VB, B2)
put("サビ1", K, VC + VC2, C1)
put("サビ2", K, VC + VC2 + VC2, C2)
put("Cメロ", K, VX + VX, X1)
put("落ちサビ", K, VC, CO)
LM = put("最後のサビ", KL, VC + VC2 + VC2, CL)
if VOCAL: put("Aメロ2", K, VA + VA, A2)
else:
    for i, (b, l) in enumerate(zip(S.sc("Aメロ2"), VA + VA)):
        if i < 8: PRM.bar(b, K.mel(l, oct=4))
        else: V.bar(b, K.mel(l, oct=3))

# ================= ピアノ =================
prev = None
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "C2")
    v4 = voice(ch, 68, 4, prev=prev); prev = v4
    if n == "音楽室":
        # 合唱曲の伴奏ふう: 2分音符の和音（左手は根音とオクターブ）。テンポはそのまま、ゆったり聞こえるように
        PL.bar(b, f"{nm(r)}:2 {nm(r + 12)}:2" if i < 7 else f"{nm(r)}:1 {nm(r + 7)}:1 {nm(r + 12)}:1 {nm(r + 7)}:1")
        PR.bar(b, f"{nm(v4[0])}:2 {nm(v4[1])}:2")
        PR2.bar(b, f"{nm(v4[3])}:2 {nm(v4[2])}:2")
    elif n in ("Aメロ1", "Aメロ2"):
        PL.bar(b, f"{nm(r)}:1.5 {nm(r + 7)}:0.5 {nm(r + 12)}:2" if i % 2 == 0 else f"{nm(r)}:1 {nm(r + 7)}:1 {nm(r + 12)}:1 {nm(r + 7)}:1")
        PR.bar(b, f"R:0.5 {nm(v4[0])}:0.5 R:0.5 {nm(v4[1])}:0.5 R:0.5 {nm(v4[2])}:0.5 R:0.5 {nm(v4[3])}:0.5")
    elif n in ("Bメロ1", "Bメロ2"):
        PL.bar(b, " ".join(f"{nm(r if q % 2 == 0 else r + 12)}:0.5" for q in range(8)))
        PR.bar(b, f"{nm(v4[0])}:1 {nm(v4[1])}:1 {nm(v4[2])}:1 {nm(v4[3])}:1")
        PR2.bar(b, f"{nm(v4[3] + 12)}:2 {nm(v4[2] + 12)}:2" if i >= 4 else "R:4")
    elif n in ("サビ1", "サビ2", "最後のサビ", "間奏"):
        # 疾走ピアノ: 右手は16分の分散和音、左手はオクターブの8分
        PL.bar(b, " ".join(f"{nm(r if q % 2 == 0 else r + 12)}:0.5" for q in range(8)))
        # v3: 16分の分散和音がサビ・間奏の点数を下げていた（サビ2 6.4・間奏 7.13、8分の Aメロは 7.95）→ 8分の分散和音に（半分の細かさ）
        PR.bar(b, " ".join(f"{nm(v4[q])}:0.5" for q in (0, 2, 1, 3, 2, 3, 1, 2)))
        if i % 2 == 0: PR2.bar(b, f"{nm(v4[3])}:1.5 {nm(v4[2])}:1 {nm(v4[3])}:1.5")
    elif n == "間奏2":
        # ピアノのソロ: サビの旋律を右手で（16分の飾り）、左手は10度の分散
        PL.bar(b, f"{nm(r)}:0.5 {nm(r + 7)}:0.5 {nm(r + 16 if 'm' not in ch[1:3] else r + 15)}:0.5 {nm(r + 7)}:0.5 {nm(r + 12)}:0.5 {nm(r + 7)}:0.5 {nm(r + 16 if 'm' not in ch[1:3] else r + 15)}:0.5 {nm(r + 7)}:0.5")
        mel = K.mel((VC + VC2)[i], oct=4)
        PRM.bar(b, mel)
    elif n == "Cメロ":
        PL.bar(b, f"{nm(r)}:4")
        PR.bar(b, f"{nm(v4[0])}:2 {nm(v4[2])}:2" if i % 2 == 0 else f"{nm(v4[1])}:1 {nm(v4[3])}:1 {nm(v4[2])}:2")
    elif n == "落ちサビ":
        PL.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2")
        PR.bar(b, f"R:0.5 {nm(v4[0])}:0.5 {nm(v4[1])}:0.5 {nm(v4[2])}:0.5 {nm(v4[3])}:2" if i % 2 == 0 else f"{nm(v4[1])}:2 {nm(v4[2])}:2")
    elif n == "後奏":
        if i < 6:
            PL.bar(b, " ".join(f"{nm(r if q % 2 == 0 else r + 12)}:0.5" for q in range(8)))
            PR.bar(b, piano_arp16(ch, "Bb4", "Bb6", pat=(0, 2, 1, 3, 2, 4, 3, 1)))
        elif i == 6:
            PL.bar(b, f"{nm(r)}:8"); PR.bar(b, " ".join(f"{nm(x)}:0.25" for x in v4) + f" {nm(v4[3] + 12)}:7")

# ================= ストリングス・バイオリン・合唱・グロッケン =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    v = voice(ch, 62, 3)
    if (n == "音楽室" and i >= 4) or n in ("Bメロ1", "Bメロ2", "Cメロ", "Aメロ1") or (n in ("Aメロ2",) and i >= 8):   # v2: Aメロ1 にも（前奏から Aメロで小さくなる段差 3.2dB を埋める）
        for j in range(3): STR[j].bar(b, f"{nm(v[j])}:4")
    elif n in ("サビ1", "サビ2", "最後のサビ", "間奏2", "後奏"):
        for j in range(3): STR[j].bar(b, f"{nm(v[j])}:2 {nm(v[j])}:2" if n != "後奏" or i < 6 else f"{nm(v[j])}:8")
    if n in ("最後のサビ", "後奏"):          # v3: サビ2 からはゆっくりした弦をはずす（重なりすぎ）
        cv = voice(ch, 66, 3)
        for j in range(3): CHO[j].bar(b, f"{nm(cv[j])}:4" if n != "後奏" or i < 6 else (f"{nm(cv[j])}:8" if i == 6 else "R:4"))
    if n == "サビ1" and i >= 8:
        cv = voice(ch, 66, 3)
        for j in range(2): CHO[j].bar(b, f"{nm(cv[j])}:4")
    # シャボン玉（グロッケン）: 小節のおわりに、ふわっと上がる3音
    if n in ("Aメロ1", "サビ1", "サビ2", "最後のサビ", "後奏") and i % 4 == 3:
        t = tones(ch, "C6", "C7")
        GLK.bar(b, f"R:2.5 {nm(t[0])}:0.5 {nm(t[1])}:0.5 {nm(t[2 % len(t)])}:0.5")
VLM = ["Eb6:2 F6:1 G6:1", "Ab6:3 G6:1", "F6:2 Eb6:1 C6:1", "Db6:3 F6:1", "Eb6:2 Db6:1 C6:1", "Bb5:2 G5:2", "Ab5:2 C6:1 Eb6:1", "Eb6:4"]
for i, b in enumerate(S.sc("最後のサビ")[16:]): VLN.bar(b, " ".join(f"{nm(midi(t.split(':')[0]) + 2)}:{t.split(':')[1]}" for t in VLM[i].split()))   # +2 の調で

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "音楽室":
        if i >= 4: BASS.bar(b, bass_line(S, b, "half", lo="E1"))
    elif n in ("Aメロ1", "Aメロ2"): BASS.bar(b, bass_line(S, b, "half" if i < 8 else "root8", lo="E1"))
    elif n in ("Bメロ1", "Bメロ2"): BASS.bar(b, bass_line(S, b, "walk", lo="E1"))
    elif n in ("サビ1", "サビ2", "最後のサビ", "間奏", "間奏2"): BASS.bar(b, bass_line(S, b, "oct8" if i % 4 != 3 else "root8", lo="E1"))
    elif n == "Cメロ": BASS.bar(b, bass_line(S, b, "long" if i < 8 else "half", lo="E1"))
    elif n == "後奏" and i < 7: BASS.bar(b, bass_line(S, b, "oct8" if i < 6 else "long", lo="E1"))

cym_swell(CYM, S.sc("サビ1")[0], 2, "C4"); cym_swell(CYM, S.sc("サビ2")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 4, "E4")

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "音楽室":
        if i == 7: put_fill(D, b, "lift")
    elif n in ("Aメロ1", "Aメロ2"):
        if n == "Aメロ1" and i < 8: D.set(b, "X.......X.......", "................", "x.x.x.x.x.x.x.x.")
        else: vgroove(D, b, "beat8", ghosts=0.3, seed=b)
        if i == 0 and n == "Aメロ2": crash(D, b)
        if i % 8 == 7: put_fill(D, b, "small" if not last else "snare16")
    elif n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "halfdrive", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 1)
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        vgroove(D, b, "vrock2", ghosts=0.25, seed=b)
        if i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
        if i % 8 == 7 and not last: put_fill(D, b, "tomdown" if i % 16 == 7 else "small")
        if last and n != "最後のサビ": put_fill(D, b, "snare16")
    elif n in ("間奏", "間奏2"):
        vgroove(D, b, "vrock" if n == "間奏" else "beat8", ghosts=0.3, seed=b)
        if i == 0: crash(D, b)
        if last: put_fill(D, b, "lift")
    elif n == "Cメロ":
        vgroove(D, b, "half", ghosts=0.2, seed=b)
        if i == 0: crash(D, b, "C2", 6)
        if i == 15: put_fill(D, b, "build")
    elif n == "落ちサビ":
        pass
    elif n == "後奏":
        if i < 6: vgroove(D, b, "vrock2", ghosts=0.2, seed=b)
        if i == 0: crash(D, b)
        if i == 5: put_fill(D, b, "snare16")
        if i == 6: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 8)

# 止め: Bメロの最後（1拍だけ叩いて全員休み）。手を上げる: 1小節の完全な無音
for name in ("Bメロ1", "Bメロ2"): SIL.add(S.sc(name)[-1], 1, 4)
SIL.add(S.sc("手を上げる")[0], 0, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の02。J-POP（疾走ピアノ）。A♭長調・176、最後のサビは +2（B♭）。"
          "合唱コンクールで、口だけ動かしていた子が、はじめて大きな声で歌う。合唱曲ふうのピアノの和音で始まり、句ごとに一段ずつ高くなる旋律、"
          "1小節の完全な無音（指揮者が手を上げる）、ピアノとテトだけの落ちサビ、みんなの声が重なる最後のサビ（歌の重ね・合唱）。自作")
finish(S, LY, V, 0, double=[("サビ2", 0.35), ("最後のサビ", 0.7)],
       level={"verse": -0.45}, special={"Aメロ2": -0.3, "落ちサビ": -0.6, "Cメロ": -0.35, "最後のサビ": 0.55})
