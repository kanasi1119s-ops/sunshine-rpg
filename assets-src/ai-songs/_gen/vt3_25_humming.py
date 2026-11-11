# vt3 25「25時のハミング」Humming at 25 O'Clock（仮）— シンセポップ・アンセム。148・4/4。A長調 → 最後のサビは +1（B♭）。 書き出しは全体を+1半音（B♭長調 → 最後は B）。
# 第3弾（0時〜24時の街）の 24時（アルバムの最後）。表は docs/sound/vt3-plan.md。
# 物語: 日付がまた変わる。パン屋のかまど、銭湯の桶、コインランドリーのドラム、くらげの夜。今日の24人が、それぞれの場所で同じ鼻歌を歌う。
#   1時のラジオで生まれた5つの音の節が、町じゅうをめぐって、いま全員の声になる。0時の秒読み、1拍の無音。そして最後のサビ。
#   さいごは、1曲目の秒針の「カチ」に戻って終わる（アルバムがひとまわりする）。
# 場面と強さ: ダイヤル（ラジオのダイヤルを回すように、前の曲の音が1小節ずつ流れる）→ イントロ（シンセのリードと手拍子・強）
#   → Aメロ1 → Bメロ1 → サビ1（強）→ 間奏（リードの節）→ Aメロ2 → Bメロ2 → サビ2 → 秒読み（秒針とパッド・弱）
#   → 1拍の無音 → 最後のサビ（+1・いちばん強い）→ 合唱（全員で「節」を歌う）→ 秒針（1曲目の時計の音に戻る）
# 旋律の性格: アルバムでいちばん大きな跳躍。サビの頭は合いことばの節（3・5・6・5・2）を低く歌い、すぐ1オクターブ上へ跳ぶ（B3〜F5）。
# この曲だけの音: 前の曲たちの楽器（エレピ・裏打ちのギター・ナイロンギター・ブラス・ビブラフォン・グロッケン・チェンバロ・口笛）が
#   ダイヤルで次々に流れ、最後の合唱では全員（合唱・リード・グロッケン・口笛）が同じ節を鳴らす。
from vt25_lib import *

S = Song("25", "humming", "25時のハミング（仮）", "Humming at 25 O'Clock", 148, 4, "A", "major", "シンセポップ・アンセム（ボカロ）")
S.kit = "jpop"      # v2: electro → jpop（生に近い太鼓。シンセの区間がどこも 6.4〜7.1 だった）
S.flags = S.flags + " --piano salamander --space room --space-wet 0.14"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.5
K = Key("A", "major")          # oct 3 で 1 = A3
KL = Key("Bb", "major")        # 最後のサビと合唱（+1）

A_CH = ["A", "E", "F#m7", "Dmaj7", "Bm7", "E", "A", "E"]
B_CH = ["D", "E", "C#m7", "F#m7", "D", "E", "Bm7", "E7sus4"]
C_CH = ["D", "E", "C#m7", "F#m7", "Bm7", "E", "A", "A"]
LAST = [tr_chord(c, 1) for c in C_CH]

S.scene("ダイヤル", 8, "intro", ["Ebmaj7", "Gm7", "Amaj7", "Bb6", "Cm9", "Dadd9", "Gmaj7", "E7sus4"])
S.scene("イントロ", 16, "intro", A_CH)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 8, "break", A_CH)
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("秒読み", 4, "bridge", ["Dmaj7", "E", "C#m7", "F7sus4"])      # 最後の小節は B♭ への入り口
S.scene("最後のサビ", 24, "chorus", LAST)
S.scene("合唱", 8, "chorus", LAST)
S.scene("秒針", 4, "outro", ["Bb", "Bb", "Bb", "Bb"])

V = Voice(S, vol=0.21, delay=0.75, bright=0.4, patch="kfbSineLead", low=True)   # v2: 歌をなぞるシンセは、高さの揺れない音に
LEAD = S.track("シンセのリード", "lead", patch="kfbFutureSax", volume=0.07,   # v2: カワイイ・フューチャーベース系の電子のリードに   # v3: modernLead → やわらかい音（イントロ・間奏が 6.8）
                pan=0.0, reverb=0.3)
PNL = S.track("ピアノ（左手）", "piano", volume=0.09, pan=-0.15, reverb=0.3, fx=[{"type": "eq", "low": -2, "mid": -1, "midHz": 400, "high": -1}])   # v2
PNR = [S.track(f"ピアノ（右手{i + 1}）", "piano", volume=0.06, pan=0.1, reverb=0.3, fx=[{"type": "eq", "low": -3, "mid": -1, "midHz": 400, "high": -1}]) for i in range(3)]
SAW = [S.track(f"シンセの和音{i + 1}", "pad", patch="kfbSupersaw", volume=0.03, pan=-0.4 + 0.4 * i, reverb=0.3, duck=0.35) for i in range(3)]
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.05, pan=-0.4 + 0.4 * i, reverb=0.4, sustain=1.2) for i in range(3)]
CHOIR = [S.track(f"合唱{i + 1}", "pad", patch="choir", volume=0.06, pan=-0.3 + 0.3 * i, reverb=0.45) for i in range(3)]
PLK = S.track("プラック", "pad", patch="kfbSquarePluck", volume=0.05, pan=0.3, reverb=0.3, sustain=0.5)
BASS = S.track("シンセベース", "bass", **synth_bass_spec("kfbFmBass", vol=0.14, duck=0.35))
# ダイヤルで流れる前の曲たちの楽器（最後の合唱でもまた出てくる）
EPD = [S.track(f"ラジオ: エレピ{i + 1}", "keys", patch="kfbGlassEp", volume=0.05, pan=-0.2, reverb=0.3, sustain=0.6) for i in range(3)]
SKA = [S.track(f"ラジオ: 裏打ちのギター{i + 1}", "guitar", amp="jpopClean", volume=0.045, pan=0.35, reverb=0.2, chorus=0, sustain=0.3) for i in range(3)]
NYL = [S.track(f"ラジオ: ナイロンギター{i + 1}", "guitar", patch="nylonGuitar", amp="crystal", volume=0.06, pan=-0.35, reverb=0.25, chorus=0, sustain=0.8) for i in range(3)]
BR = [S.track(f"ラジオ: ブラス{i + 1}", "brass", patch="trumpet", volume=0.05, pan=0.2, reverb=0.3) for i in range(3)]
VIB = S.track("ラジオ: ビブラフォン", "harp", patch="vibraphone", volume=0.08, pan=0.35, reverb=0.4, sustain=1.5, bright=-0.2)
GL = S.track("グロッケン", "glockenspiel", volume=0.07, pan=0.15, reverb=0.45)
HC = [S.track(f"ラジオ: チェンバロ{i + 1}", "harpsichord", volume=0.06, pan=0.15, reverb=0.3) for i in range(3)]
WH = S.track("口笛（高い縦笛）", "lead", patch="kfbSineLead", volume=0.06, pan=0.1, reverb=0.35)
TICK = S.track("秒針（カホンの縁）", "cajon", volume=0.08, pan=0.15, reverb=0.1)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.05, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 1:0.5 2:0.5 3:0.5 5:1 3:1", "2:1.5 1:0.5 2:1 R:1", "R:0.5 1:0.5 2:0.5 3:0.5 6:1 5:1", "3:2 R:2",
      "R:0.5 3:0.5 4:0.5 5:0.5 1':1 7:1", "6:1.5 5:0.5 6:1 R:1", "R:0.5 5:0.5 4:0.5 3:0.5 2:1 3:1", "5:2 R:2"]
A1 = ("にじゅうよじかんの/まちのうたが/だれかのこえがね/きこえてくる/"
      "ぱんやのかまどや/ゆぶねのおけ/らんどりのどらむ/くらげのよる")
A2 = ("しんぶんはいたつ/しはつでんしゃ/ゆうやけのそらと/しょうてんがい/"
      "それぞれのばしょで/おなじふしを/みんながうたうよ/はなうたなの")
VB = ["R:1 3:0.5 5:0.5 6:1 5:1", "1':2 7:1 R:1", "R:1 3:0.5 5:0.5 6:1 5:1", "2':2 1':1 R:1",
      "R:1 4:0.5 6:0.5 1':1 2':1", "3':2 2':1 R:1", "R:0.5 1':0.5 2':0.5 3':0.5 4':1 3':1", "2':3 R:1"]
B1 = "ひづけがまた/かわるまえに/もういちどね/うたいだそう"
B2 = "らじおのこえ/ちいさなこえ/ぜんぶあわせ/ひとつになる"
# v4: 歌の版がサビで 6.4〜6.8（1オクターブ跳んだ先の高い音 F5〜F#5 を長くのばすところで声が細くなっていた）
#     → 跳ぶ先を 3'（6度）にし、そのあとの下りも1つ低くする
VC = ["R:1 3:0.5 5:0.5 6:1 5:0.5 2:0.5", "1:1 5:1 3':1.5 R:0.5", "R:0.5 3':0.5 2':0.5 1':0.5 7:1 1':1", "1':2 R:2",
      "R:1 3:0.5 5:0.5 6:1 5:0.5 2:0.5", "1:1 6:1 2':1.5 R:0.5", "R:0.5 2':0.5 1':0.5 7:0.5 6:1 7:1", "1':3 R:1"]
HOOK = "にじゅうごじのうた"
C1 = (f"{HOOK}/さあうたおう/{HOOK}/あしたへゆく/"
      "はなれていてもね/おなじふしを/だれかとつながる/はみんぐだよ")
C2 = (f"{HOOK}/さあうたおう/きのうとあしたを/つなぐうただ/"
      "にじゅうよにんぶん/こえをのせて/ひとつのはなうた/よぞらにとぶ")
C3 = (f"{HOOK}/さあうたおう/{HOOK}/あしたへゆく/"
      "にじゅうよにんぶん/こえをのせて/ひとつのはなうた/よぞらにとぶ/"
      f"{HOOK}/またあしたも/このまちのかどで/うたいだそう")
HUM = ["R:1 3:0.5 5:0.5 6:1 5:0.5 2:0.5", "1:3 R:1"]
LY = Lyrics(S)


def put(name, key, lines, text, o=3):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA + VA, A1)
put("Bメロ1", K, VB, B1)
put("サビ1", K, VC + VC, C1)
put("Aメロ2", K, VA + VA, A2)
put("Bメロ2", K, VB, B2)
put("サビ2", K, VC + VC, C2)
put("最後のサビ", KL, VC + VC + VC, C3)
put("合唱", KL, HUM * 4, "らららららら/らららららら/らららららら/らららららら")

# ================= ダイヤル（前の曲たちが1小節ずつ）=================
def chord3(tracks, b, ch, pat, c=62):
    v = voice(ch, c, len(tracks))
    for j, t in enumerate(tracks): t.bar(b, " ".join(x.replace("x", nm(v[j])) for x in pat.split()))


DB = S.sc("ダイヤル")
chord3(EPD, DB[0], "Ebmaj7", "x:1.5 x:0.5 R:2")                                   # 1時のラジオ（シティポップのエレピ）
chord3(SKA, DB[1], "Gm7", "R:0.5 x:0.5 R:0.5 x:0.5 R:0.5 x:0.5 R:0.5 x:0.5", 66)    # 新聞配達（スカの裏打ち）
chord3(NYL, DB[2], "Amaj7", "x:0.5 R:0.5 x:0.75 x:0.75 R:0.5 x:1")                  # パン屋（ボサノバ）
chord3(BR, DB[3], "Bb6", "x:1.5 x:0.5 R:2", 70)                                    # 銭湯（ビッグバンド）
VIB.bar(DB[4], "R:1 Eb4:0.5 G4:0.5 Ab4:1 G4:0.5 D4:0.5")                            # コインランドリー（ビブラフォンの節）
GL.bar(DB[5], "R:1 F#5:0.5 A5:0.5 B5:1 A5:0.5 E5:0.5")                              # 水族館（グロッケンの節）
chord3(HC, DB[6], "Gmaj7", "R:0.5 x:0.5 R:0.5 x:0.5 R:0.5 x:0.5 x:0.5 R:0.5", 64)   # 服えらび（チェンバロ）
WH.bar(DB[7], "R:1 C#6:0.5 E6:0.5 F#6:1 E6:0.5 B5:0.5")                             # そして、この曲の節（口笛）
for b in DB: FX.bar(b, "A4:0.25 R:3.75")                                         # ダイヤルを回す「ザッ」

# ================= シンセ・ストリングス・合唱 =================
def saw(b, ch, pat="x:4", c=64):
    chord3(SAW, b, ch, pat, c)


def strings(b, ch, c=64):
    chord3(STR, b, ch, "x:4", c)


def pluck(b, ch):
    t = tones(ch, "A4", "A5")
    PLK.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 1, 2, 1, 0, 2, 1, 2)))


MOTIF_A = ["R:1 C#5:0.5 E5:0.5 F#5:1 E5:0.5 B4:0.5", "A4:3 R:1"]       # 合いことばの節（A長調）
MOTIF_B = ["R:1 D5:0.5 F5:0.5 G5:1 F5:0.5 C5:0.5", "Bb4:3 R:1"]       # 合いことばの節（B♭長調）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "イントロ":
        saw(b, ch, "x:1.5 x:0.5 R:0.5 x:1.5" if i < 8 else "x:4"); pluck(b, ch)
        LEAD.bar(b, MOTIF_A[i % 2] if i < 8 else ["R:0.5 E5:0.5 F#5:0.5 A5:0.5 B5:1 A5:1", "F#5:2 E5:1 R:1",
                                                    "R:0.5 C#5:0.5 E5:0.5 F#5:0.5 A5:1 G#5:1", "E5:3 R:1"][i % 4])
        if i >= 8: strings(b, ch)
    elif n in ("Aメロ1", "Aメロ2"):
        pluck(b, ch)
        if n == "Aメロ2" or i >= 8: saw(b, ch, "x:1.5 x:0.5 R:0.5 x:1.5", 60)
    elif n in ("Bメロ1", "Bメロ2"):
        pluck(b, ch); strings(b, ch, 62); saw(b, ch, "x:2 x:2", 62)
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        saw(b, ch, "x:4", 66 if n == "最後のサビ" else 64); strings(b, ch, 67); pluck(b, ch)
        if n == "最後のサビ":
            chord3(CHOIR, b, ch, "x:4", 62)
            if i >= 16 and i % 2 == 0: GL.bar(b, MOTIF_B[0])
    elif n == "間奏":
        saw(b, ch, "x:1.5 x:0.5 R:0.5 x:1.5"); pluck(b, ch)
        LEAD.bar(b, MOTIF_A[i % 2] if i < 4 else ["R:0.5 A5:0.5 B5:0.5 C#6:0.5 E6:1 C#6:1", "B5:3 R:1", "R:0.5 F#5:0.5 E5:0.5 C#5:0.5 B4:1 C#5:1", "E5:3 R:1"][i - 4])
    elif n == "秒読み":
        if i < 3: chord3(STR, b, ch, "x:4", 60)
    elif n == "合唱":
        saw(b, ch, "x:4", 64); strings(b, ch, 67)
        for j, t in enumerate(CHOIR): t.bar(b, shift_oct(MOTIF_B[i % 2], -1) if j == 0 else MOTIF_B[i % 2] if j == 1 else f"{nm(voice(ch, 60, 3)[2])}:4")
        LEAD.bar(b, MOTIF_B[i % 2]); GL.bar(b, shift_oct(MOTIF_B[i % 2], 1))
        WH.bar(b, shift_oct(MOTIF_B[i % 2], 1) if i >= 4 else "R:4")      # v3: 合唱のエレピの裏打ちはやめる（音が多すぎた）
    elif n == "秒針":
        if i < 2: chord3(STR, b, ch, "x:4", 62)
        if i == 0: chord3(CHOIR, b, ch, "x:4", 62)

# ================= ピアノ（v2: 左手と右手で和音を弾き、シンセだけの音を生の手ざわりで支える）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n not in ("イントロ", "Aメロ1", "Aメロ2", "Bメロ1", "Bメロ2", "サビ1", "サビ2", "最後のサビ", "間奏"): continue
    if n == "イントロ" and i < 8: continue
    ch = S.chords[b]; r = low(ch, "E2"); v = voice(ch, 64, 3)
    big = n in ("サビ1", "サビ2", "最後のサビ")
    PNL.bar(b, f"{nm(r)}:1.5 {nm(r + 12)}:0.5 {nm(r + 7)}:2" if big else f"{nm(r)}:2 {nm(r + 7)}:2")
    for j in range(3): PNR[j].bar(b, f"{nm(v[j])}:1 {nm(v[j])}:0.5 {nm(v[j])}:1 {nm(v[j])}:0.5 {nm(v[j])}:1" if big else f"R:0.5 {nm(v[j])}:1.5 R:0.5 {nm(v[j])}:1.5")

# ================= 秒針（1曲目と同じカホンの縁「カチ」）=================
for b in S.sc("秒読み")[:3]: TICK.bar(b, "E3:1 E3:1 E3:1 E3:1")
TICK.bar(S.sc("秒読み")[3], "E3:1 E3:1 E3:1 R:1")                 # 0時ちょうど（1拍の無音）
for b in S.sc("秒針")[:3]: TICK.bar(b, "E3:1 E3:1 E3:1 E3:1")
TICK.bar(S.sc("秒針")[3], "E3:1 R:3")
season(S, S.sc("合唱")[0], "手拍子", beats=32, vol=0.05, every=1)

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n in ("ダイヤル", "秒針"): continue
    if n == "秒読み":
        if i < 3: BASS.bar(b, f"{nm(r)}:4")
        continue
    if n in ("Aメロ1",) and i < 8: BASS.bar(b, f"{nm(r)}:1.5 {nm(r)}:0.5 R:0.5 {nm(r)}:1.5"); continue
    BASS.bar(b, bass_line(S, b, "oct8" if n in ("サビ1", "サビ2", "最後のサビ", "合唱") else "root8", lo="E1"))

riser(FX, S.sc("サビ1")[0], 4, "C4"); riser(FX, S.sc("サビ2")[0], 4, "C4")
cym_swell(CYM, S.sc("イントロ")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 2, "C4")

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("ダイヤル", "秒読み", "秒針"): continue
    if n in ("Aメロ1", "Aメロ2") and i < 8:
        vgroove(D, b, "beat8", ghosts=0.15, seed=b)
    else:
        vgroove(D, b, "beat8", ghosts=0.2, seed=b)     # v3: 合唱の4つ打ちもやめる（6.7）
    if n in ("サビ1", "サビ2", "最後のサビ", "合唱", "イントロ") and i % 8 == 0: crash(D, b, "C2", 7 if n == "最後のサビ" and i == 0 else 5)
    if i % 8 == 7 and not last: put_fill(D, b, "small")
    if last and n in ("Bメロ1", "Bメロ2", "間奏", "イントロ", "サビ2"): put_fill(D, b, "snare16")
    if last and n == "合唱": halt(D, b, 2)

SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の25（24時・アルバムの最後）。シンセポップ・アンセム。A長調・148、最後のサビは +1（B♭）。"
          "日付がまた変わる。今日の24人が、それぞれの場所で同じ鼻歌を歌う。始まりはラジオのダイヤルで前の曲たちの音が次々に流れ、"
          "0時の秒読みと1拍の無音のあと最後のサビ、全員で合いことばの節を歌う合唱。1曲目の秒針の音に戻って終わる。自作")
finish(S, LY, V, 1,
       level={"verse": -0.2}, special={"秒読み": -0.45, "最後のサビ": 0.4, "合唱": 0.35, "秒針": -0.4, "ダイヤル": -0.15})

# ================= v2（2026-11-12 作り直し。docs/sound/vt3-remake-plan.md）=================
# この曲（25時・1日の全部の節が集まる・シンセポップのアンセム）で直すこと:
#   電子の音を全部カワイイ・フューチャーベース系に: リード＝電子のサックス、和音＝スーパーソー（キックで凹む）、プラック＝短い矩形波、ベース＝はじく FM、ラジオのエレピ＝ガラスのエレピ。
#   最後のサビと合唱に丸いサブベース、合唱の 2・4拍に電子のクラップ（みんなの手拍子）。サビの前に上がる音、サビの頭にインパクト、合唱の頭にきらきら
#   口笛（高い縦笛）は電子の笛に（人間「フルートの仲間の音は指定しない限り使わない」）
#   歌: Aメロはウィスパー（真夜中のひとり）、Bメロはクリア、サビはキュート、合唱はクリア（みんなの声）。ハモリは サビ2 の後半・最後のサビ・合唱＝声が増えていく（アルバムのしめくくり）
from vt3x_lib import *
path = sys.argv[1]
fx, sub, clap = {}, {}, {}
for name in ("サビ1", "サビ2", "最後のサビ"):
    b0 = S.sc(name)[0]; fx[b0] = "G5:2 R:2"; fx[b0 - 1] = "R:2 F#4:2"
fx[S.sc("合唱")[0]] = "D4:2 R:2"
for name in ("最後のサビ", "合唱"):
    for b in S.sc(name): sub[b] = f"{nm(low(S.chords[b].split('|')[0], 'C1') + 1)}:3.5 R:0.5"      # +1: 書き出しで全体が半音上がる
for b in S.sc("合唱"): clap[b] = "R:1 B4:1 R:1 B4:1"
add_parts(path, [pad_part(S, "カワイイ効果音", "kawaiiFx", fx, 0.06, pan=0.1, reverb=0.15, modulate=False, instrument="guitar"),
                 pad_part(S, "サブベース", "kfbSub", sub, 0.028, instrument="bass", reverb=0, duck=0.5),
                 pad_part(S, "電子のクラップ", "kawaiiFx", clap, 0.07, reverb=0.1, modulate=False, instrument="guitar")])
humanize(path, "ピアノ（右手", mid=82, down=12, up=10, seed=4)
set_parts(path, "シンセベース", sustain=1.1)
final_gain(path, {"ダイヤル": 4, "最後のサビ": 1.6, "合唱": 1.5})
if VOCAL:
    remark(path, S, std_mark(("chorus",), jump=5))
    vocal_polish(path, S, {"verse": 6, "pre": 14, "chorus": 22, "最後のサビ": 28, "合唱": 16, "bridge": 0, "outro": 0}, scoop=0.3, slash=0.8, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.5)
    harmony(path, S, [("サビ2", 8, None, K), ("最後のサビ", 0, None, KL), ("合唱", 0, None, KL)], vol=0.38, shift=1)
    voice_by_scene(path, S, {"verse": "whisper", "pre": "clear", "chorus": "cute", "合唱": "clear", "bridge": "whisper"}, default="clear")
