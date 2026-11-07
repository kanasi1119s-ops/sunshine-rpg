# vtp 01「白い息のリテイク」White Breath Retake（仮）— プロ仕様のボカロ曲（冬のバラードロック）。148・4/4（Aメロ1は半分のノリ）。
# A長調 → 最後のサビは +2（B長調）。2026-11-07 人間「プロ仕様のボカロ曲作ろうか。プロがどのように作っているか学んで来て」
# 物語: 冬の寒い夜、大好きな人に告白する。でも「ごめんなさい」。春に髪を切り、夏は走り、苦手なことも練習した。
#   秋、去年のわたしに手をふる。1年後の冬、同じ道で、変われたわたしで、もう一度「好き」と言う（答えは言わない）。
# 調べたプロのやり方で入れたこと:
#   ・0サビ（曲の頭にサビの節）・短いイントロ・2番のAメロはドラムを変えて明るく・Cメロで調を外す（借りた和音）
#     → ギターソロ → 落ちサビ（急に落とさない）→ 最後のサビは +2
#   ・調声: しゃくり・長い音の後半だけのビブラート・句の山で強く・句の間の息つぎ（teto の決まり）。サビに3度下のハモリ（ビブラートを変える）。
#     最後のサビは歌を重ねる（ダブル）
#   ・ミックス: ギターとシンセは声の帯域（2〜3kHz）を少し下げる。パッドは「鳴っているかわからないくらい」
# 場面と強さは docs/sound/vtp-plan.md の表のとおり。
# この曲だけの音: 冬の鈴（グロッケン）のリフが曲の合いことば。去年は短調の和音の上で、今年は明るい和音の上で鳴る。同じ節に違う言葉。
from vt25_lib import *
import json as _json2, re as _re2, os as _os2

S = Song("01", "whitebreath", "白い息のリテイク（仮）", "White Breath Retake", 148, 4, "A", "major", "冬のバラードロック（ボカロ）")
S.kit = "naked-x"
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags + " --piano salamander --space hall --space-wet 0.15"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.45
S.drum_scale = 0.85
K = Key("A", "major")          # oct 3 で 1 = A3
KL = Key("B", "major")         # 最後のサビ（+2）

C_HALF1 = ["Dmaj7", "E", "C#m7", "F#m7", "Bm7", "C#7", "F#m7", "Esus4"]
C_HALF2 = ["Dmaj7", "E", "C#m7", "F#m7", "Bm7", "E", "A", "A"]
C_SAD = ["Dmaj7", "E", "C#m7", "F#m7", "Bm7", "E", "Dmaj7", "Dmaj7"]       # サビ1 の終わり（「ごめんなさい」）は解決しない
A_CH = ["A", "E", "F#m7", "C#m7", "D", "A", "Bm7", "Esus4"]
B_CH = ["Bm7", "C#m7", "Dmaj7", "E", "Bm7", "C#m7", "Dmaj7", "E7sus4"]
CM_CH = ["Fmaj7", "G", "Am7", "Am7", "Dm7", "G", "Bm7", "E7"]              # Cメロ: A長調から借りた和音（♭VI・♭VII・i）
LAST = [tr_chord(c, 2) for c in C_HALF1 + C_HALF2]

S.scene("0サビ", 8, "intro", C_HALF1[:7] + ["E"])
S.scene("イントロ", 8, "intro", C_HALF2)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_HALF1 + C_SAD)
S.scene("間奏", 8, "break", ["F#m7", "Dmaj7", "A", "E", "F#m7", "Dmaj7", "Bm7", "Esus4"])
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_HALF1 + C_HALF2)
S.scene("Cメロ", 8, "bridge", CM_CH)
S.scene("ギターソロ", 8, "solo", C_HALF1)
S.scene("落ちサビ", 8, "bridge", C_HALF1[:7] + ["F#7"])               # 最後の小節は B長調への入り口
S.scene("最後のサビ", 24, "chorus", LAST + LAST[:8])
S.scene("アウトロ", 6, "outro", ["Emaj7", "F#", "D#m7", "G#m7", "B", "B"])

V = Voice(S, vol=0.2, delay=0.5, bright=0.0, patch="surgeFriendly", low=False)
PNL = S.track("ピアノ（左手）", "piano", volume=0.1, pan=-0.12, reverb=0.3, fx=[{"type": "eq", "low": -2, "mid": -1, "midHz": 400, "high": -1}])
PNR = [S.track(f"ピアノ（右手{i + 1}）", "piano", volume=0.06, pan=-0.05, reverb=0.3, fx=[{"type": "eq", "low": -3, "mid": -1.5, "midHz": 2500, "high": -1}]) for i in range(3)]
GLK = S.track("冬の鈴（グロッケン）", "glockenspiel", volume=0.075, pan=0.2, reverb=0.5)
CLN = S.track("クリーンギター（アルペジオ）", "guitar", amp="crystal", volume=0.07, pan=0.4, reverb=0.3, chorus=0, sustain=0.9)
GL = [S.track(f"Lギター{i + 1}", "distGuitar", **rock_gtr_spec(0.04, -0.55, drive=0.45)) for i in range(2)]
GR = [S.track(f"Rギター{i + 1}", "distGuitar", **rock_gtr_spec(0.038, 0.55, drive=0.45)) for i in range(2)]
LEAD = S.track("リードギター", "distGuitar", **lead_gtr_spec(0.11, -0.05))
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.045, pan=-0.45 + 0.45 * i, reverb=0.45, sustain=1.4) for i in range(3)]
PAD = [S.track(f"うすいパッド{i + 1}", "pad", patch="surgePadNeverending", volume=0.018, pan=-0.3 + 0.6 * i, reverb=0.4) for i in range(2)]
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.22))
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
# サビの節: 5度の跳躍（E4→B4）で始まり、3つめの句で E5 まで上がる。句は 8・7・8・6 音
VC = ["R:0.5 5:0.5 2':1 1':0.5 7:0.5 1':1", "3':1.5 2':0.5 1':1 R:1", "R:0.5 6:0.5 1':0.5 2':0.5 3':1 2':1", "1':2 6:1 R:1",
      "R:0.5 5:0.5 2':1 1':0.5 7:0.5 1':1", "5':1.5 4':0.5 3':1 R:1", "R:0.5 4':0.5 3':0.5 2':0.5 1':1 2':1", "1':3 R:1"]
VSAD = VC[:6] + ["R:0.5 3:0.5 3:0.5 2:0.5 1:1 2:1", "1:3 R:1"]          # 「ごめんなさい」は低く下りる
HOOK = "しろいいきでいう"
Z0 = "きょねんのふゆのひ/ここでいったんだ/しろいいきのなか/きみがすきと"
C1 = (f"{HOOK}/きみがすきだって/ふるえるこえごと/ゆきにとけた/"
      "しろいいきのさき/きみはうつむき/ありがとうでもね/ごめんなさい")
C2 = ("しろいいきをはく/かわりたいんだ/だれのためでなく/わたしのため/"
      "しろいいきのさき/はるがくるから/ころんだぶんだけ/つよくなれる")
C3 = (f"{HOOK}/きみがすきだって/かわれたわたしで/もういちどね/"
      "しろいいきのさき/こたえはあとで/いまはただきみに/とどけたいの/"
      f"{HOOK}/もういちどだけ/ふるえないこえで/きみがすきだ")
OC = "しろいいきのなか/もういちどだけ/いわせてほしいの/きみのまえで"
# Aメロ: 話すような低めの短い句（7・6・7・6 音）。2番は2度高く、はずむ
VA = ["R:1 3:0.5 3:0.5 3:0.5 2:0.5 1:1", "2:1 3:1 R:2", "R:1 3:0.5 3:0.5 5:0.5 4:0.5 3:1", "2:2 R:2",
      "R:1 3:0.5 3:0.5 3:0.5 2:0.5 1:1", "2:1 5:1 R:2", "R:1 5:0.5 4:0.5 3:0.5 2:0.5 1:1", "1:2 R:2"]
VA2 = ["R:1 5:0.5 5:0.5 5:0.5 4:0.5 3:1", "4:1 5:1 R:2", "R:1 5:0.5 5:0.5 1':0.5 6:0.5 5:1", "4:2 R:2",
       "R:1 5:0.5 5:0.5 5:0.5 4:0.5 3:1", "4:1 6:1 R:2", "R:1 1':0.5 6:0.5 5:0.5 4:0.5 3:1", "3:2 R:2"]
A1 = ("ゆきのふるみち/ふたりきりで/てぶくろのなか/ゆびがふるえ/"
      "いうときめたの/きょうこそはね/かがやくまちの/あかりのした")
A2 = ("さくらのころに/かみをきったよ/なつのあさには/はしりだした/"
      "にがてなことも/れんしゅうした/かがみのなかの/わらうわたし")
VB = ["R:0.5 4:0.5 4:0.5 5:0.5 6:1 5:1", "4:1 3:1 R:2", "R:0.5 5:0.5 5:0.5 6:0.5 7:1 6:1", "5:2 R:2",
      "R:0.5 6:0.5 6:0.5 7:0.5 1':1 2':1", "3':1 2':1 R:2", "R:0.5 1':0.5 2':0.5 3':0.5 4':1 3':1", "2':2 5:1 R:1"]
B1 = "こころのなかで/なんどもいった/しまっていたこえ/いまこそだすの"
B2 = "あきのゆうぐれ/おちばをけって/きょねんのわたし/さよならをいう"
VCM = ["R:1 3':1 2':1 1':1", "7:2 6:1 R:1", "R:1 1':1 7:1 6:1", "5:3 R:1",
       "R:1 3':1 4':1 5':1", "4':2 3':1 R:1", "R:1 2':0.5 3':0.5 2':1 1':1", "2':3 R:1"]
CMT = "またふゆだ/このみち/いきしろく/きみがいた"
LY = Lyrics(S)


def put(name, key, lines, text, o=3):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("0サビ", K, VC, Z0)
put("Aメロ1", K, VA + VA, A1)
put("Bメロ1", K, VB, B1)
put("サビ1", K, VC + VSAD, C1)
put("Aメロ2", K, VA2 + VA2, A2)
put("Bメロ2", K, VB, B2)
put("サビ2", K, VC + VC, C2)
put("Cメロ", K, VCM, CMT)
put("落ちサビ", K, VC, OC)
put("最後のサビ", KL, VC + VC + VC, C3)

# ================= ピアノ・ギター・ストリングス・鈴 =================
def piano(b, ch, style):
    r = low(ch, "E2"); v = voice(ch, 64, 3)
    if style == "soft":       # 0サビ・落ちサビ: 左手は根音と5度をのばし、右手は和音を2分で
        PNL.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2")
        for j in range(3): PNR[j].bar(b, f"{nm(v[j])}:2 {nm(v[j])}:2")
    elif style == "arp":      # Aメロ1: 右手は分散和音
        PNL.bar(b, f"{nm(r)}:4")
        t = tones(ch, "C#4", "C#5")
        PNR[0].bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 1, 2, 1, 3, 2, 1, 2)))
    elif style == "drive":    # サビ: 左手は根音・オクターブ・5度、右手は8分の和音（アクセントは1拍と2拍半）
        PNL.bar(b, f"{nm(r)}:1.5 {nm(r + 12)}:0.5 {nm(r + 7)}:2")
        for j in range(3): PNR[j].bar(b, f"{nm(v[j])}:1 {nm(v[j])}:0.5 {nm(v[j])}:1 {nm(v[j])}:0.5 {nm(v[j])}:1")
    else:                     # Bメロ・Aメロ2: 2拍ずつ
        PNL.bar(b, f"{nm(r)}:2 {nm(r + 7)}:1 {nm(r + 12)}:1")
        for j in range(3): PNR[j].bar(b, f"R:0.5 {nm(v[j])}:1.5 R:0.5 {nm(v[j])}:1.5")


def arp(b, ch):
    t = tones(ch, "E3", "E5")
    CLN.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 1, 3, 2, 4, 3, 2)))


def dist(b, ch, pat="8"):
    pw = power(ch, "E2")
    for j, (gl, gr) in enumerate(zip(GL, GR)):
        if pat == "8":
            gl.bar(b, " ".join(f"{nm(pw[j])}:0.5{'!' if q % 4 == 0 else ''}" for q in range(8)))
            gr.bar(b, " ".join(f"{nm(pw[j + 1 if j + 1 < len(pw) else j])}:0.5{'!' if q % 4 == 0 else ''}" for q in range(8)))
        else:   # のばす（Bメロ・Cメロ）
            gl.bar(b, f"{nm(pw[j])}:2 {nm(pw[j])}:2"); gr.bar(b, f"{nm(pw[j + 1 if j + 1 < len(pw) else j])}:4")


def strings(b, ch, c=64):
    v = voice(ch, c, 3)
    for j in range(3): STR[j].bar(b, f"{nm(v[j])}:4")


def pad(b, ch):
    v = voice(ch, 60, 2)
    for j in range(2): PAD[j].bar(b, f"{nm(v[j])}:4")


# 冬の鈴のリフ（曲の合いことば）: 2小節で1つ。去年（A長調・短調の和音の上）と今年（B長調）
RIFF = ["C#6:0.5 B5:0.5 A5:0.5 E5:0.5 F#5:1 E5:1", "A5:0.5 B5:0.5 C#6:0.5 E6:0.5 B5:2"]
RIFF_SAD = ["C#6:0.5 B5:0.5 A5:0.5 E5:0.5 F#5:1 C#5:1", "D5:1 E5:1 F#5:2"]
RIFF_B = ["D#6:0.5 C#6:0.5 B5:0.5 F#5:0.5 G#5:1 F#5:1", "B5:0.5 C#6:0.5 D#6:0.5 F#6:0.5 C#6:2"]
SOLO = ["E5:0.5 F#5:0.5 A5:1 B5:1.5 A5:0.5", "C#6:2 B5:1 A5:1", "F#5:0.5 A5:0.5 B5:1 C#6:1 E6:1", "C#6:3 B5:1",
        "A5:1 B5:0.5 C#6:0.5 E6:1.5 F#6:0.5", "E6:1 C#6:1 B5:1 A5:1", "F#5:1 A5:1 C#6:1 B5:0.5 A5:0.5", "B5:4"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "0サビ":
        piano(b, ch, "soft"); pad(b, ch)
        if i >= 4: strings(b, ch, 60)
    elif n == "イントロ":
        piano(b, ch, "drive"); dist(b, ch); strings(b, ch, 64); GLK.bar(b, RIFF[i % 2])
    elif n == "Aメロ1":
        piano(b, ch, "arp"); pad(b, ch)
        if i >= 8: arp(b, ch)
        if i % 8 == 7: GLK.bar(b, "R:2 E5:0.5 F#5:0.5 A5:1")
    elif n == "Aメロ2":           # 2番のAメロ: ピアノを2拍ずつにして、クリーンギターを最初から
        piano(b, ch, "pulse"); arp(b, ch)
        if i >= 8: strings(b, ch, 60)
    elif n in ("Bメロ1", "Bメロ2"):
        piano(b, ch, "pulse"); strings(b, ch, 62 + (i // 2)); dist(b, ch, "long" if i < 6 else "8")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        sad = n == "サビ1" and i >= 14
        piano(b, ch, "soft" if sad else "drive"); strings(b, ch, 67 if n == "最後のサビ" else 65)
        if not sad: dist(b, ch)
        if n == "最後のサビ" and i % 4 == 3: GLK.bar(b, RIFF_B[1])
        if n == "サビ2" and i % 8 == 7: GLK.bar(b, RIFF[1])
    elif n == "間奏":
        piano(b, ch, "soft"); GLK.bar(b, RIFF_SAD[i % 2]); pad(b, ch)
        if i >= 4: strings(b, ch, 60); arp(b, ch)
    elif n == "Cメロ":
        arp(b, ch); strings(b, ch, 62); dist(b, ch, "long"); pad(b, ch)
    elif n == "ギターソロ":
        piano(b, ch, "drive"); dist(b, ch); strings(b, ch, 64); LEAD.bar(b, SOLO[i])
    elif n == "落ちサビ":
        piano(b, ch, "soft"); strings(b, ch, 62); pad(b, ch)
        if i >= 4: arp(b, ch)
    elif n == "アウトロ":
        if i < 4: piano(b, ch, "soft"); strings(b, ch, 64); GLK.bar(b, RIFF_B[i % 2])
        elif i == 4: piano(b, ch, "soft"); GLK.bar(b, "F#5:0.5 B5:0.5 C#6:0.5 D#6:0.5 B5:2")
        else: GLK.bar(b, "B6:4")

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n == "0サビ": BASS.bar(b, f"{nm(r)}:4") if i >= 4 else None; continue
    if n == "Aメロ1": BASS.bar(b, f"{nm(r)}:2.5 {nm(r)}:0.5 {nm(r + 7)}:1" if i >= 4 else f"{nm(r)}:4"); continue
    if n == "Aメロ2": BASS.bar(b, f"{nm(r)}:1.5 {nm(r)}:0.5 {nm(r + 7)}:1 {nm(r + 12)}:0.5 {nm(r + 7)}:0.5"); continue
    if n in ("間奏", "落ちサビ"): BASS.bar(b, f"{nm(r)}:4" if (n == "落ちサビ" or i >= 4) else "R:4"); continue
    if n == "Cメロ": BASS.bar(b, f"{nm(r)}:2 {nm(r)}:1 {nm(r + 7)}:1"); continue
    if n == "サビ1" and i >= 14: BASS.bar(b, f"{nm(r)}:4"); continue
    if n == "アウトロ":
        if i < 5: BASS.bar(b, f"{nm(r)}:4")
        continue
    BASS.bar(b, bass_line(S, b, "root8", lo="E1"))

for name in ("サビ1", "サビ2", "最後のサビ"): cym_swell(CYM, S.sc(name)[0], 2, "C4")
season(S, S.sc("0サビ")[0], "雪", beats=8, vol=0.03) if "雪" in SEASON else None

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "0サビ":
        if i == 7: put_fill(D, b, "build")
        continue
    if n == "イントロ":
        vgroove(D, b, "vrock2", ghosts=0.2, seed=b)
        if i == 0: crash(D, b, "C2", 6)
        if last: put_fill(D, b, "tomdown")
        continue
    if n == "Aメロ1":           # 半分のノリ。ライドで刻む
        if i >= 4:
            D.set(b, "X.........X.....", "........X.......", "................"); D.R.bar(b, "D2:1 D2:1 D2:1 D2:1")
        if last: put_fill(D, b, "snare16")
        elif i % 8 == 7: put_fill(D, b, "small")
        continue
    if n == "Aメロ2":           # 2番は8ビートで明るく
        vgroove(D, b, "beat8", ghosts=0.3, seed=b)
        if i % 8 == 7 and not last: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
        continue
    if n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "halfdrive", ghosts=0.25, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 1)
        continue
    if n in ("サビ1", "サビ2", "最後のサビ"):
        if n == "サビ1" and i >= 14:
            if i == 14: crash(D, b, "C2", 8)
            continue
        vgroove(D, b, "vrock2", ghosts=0.2, seed=b)
        if i % 8 == 0: crash(D, b, "C2", 7 if (n == "最後のサビ" and i == 0) else 5)
        if i % 8 == 7 and not last: put_fill(D, b, "tomdown" if i % 16 == 15 else "small")
        if last and n == "サビ2": put_fill(D, b, "snare16")
        continue
    if n == "間奏":
        if i >= 4: D.set(b, "X.........X.....", "................", "................"); D.R.bar(b, "D2:2 D2:2")
        if last: put_fill(D, b, "small")
        continue
    if n == "Cメロ":
        D.set(b, "X.......X.......", "....x.......x...", "................"); D.R.bar(b, "D2:1 D2:1 D2:1 D2:1")
        if last: put_fill(D, b, "tomdown")
        continue
    if n == "ギターソロ":
        vgroove(D, b, "vrock2", ghosts=0.2, seed=b)
        if i == 0: crash(D, b, "C2", 5)
        if last: put_fill(D, b, "build")
        continue
    if n == "落ちサビ":
        if i >= 4: D.set(b, "X.........X.....", "................", "................"); D.R.bar(b, "D2:2 D2:2")
        if last: put_fill(D, b, "snare16")
        continue
    if n == "アウトロ":
        if i == 0: crash(D, b, "C2", 8)
        if i < 4: D.R.bar(b, "D2:2 D2:2")

SIL.add(S.sc("Bメロ1")[-1], 1, 4); SIL.add(S.sc("Bメロ2")[-1], 1, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: プロ仕様のボカロ曲（重音テト）01。冬のバラードロック。A長調・148、最後のサビは +2（B長調）。"
          "冬に告白してふられる。1年かけて自分を変えて、次の冬にもう一度告白する。0サビ・冬の鈴のリフ・ピアノとバンドとストリングス・"
          "Cメロの借りた和音・ギターソロ・落ちサビ。サビは3度下のハモリ、最後のサビは歌の重ね。自作")
HARM = _os2.environ.get("VTP_HARM", "1") == "1"; DBL = _os2.environ.get("VTP_DBL", "1") == "1"
finish(S, LY, V, 0, double=[("最後のサビ", 0.5)] if DBL else None,
       level={"verse": -0.25}, special={"0サビ": -0.2, "落ちサビ": -0.3, "最後のサビ": 0.4, "サビ1": 0.3})

# ================= サビの3度下のハモリ（プロのやり方: ビブラートを本線と変えて、声が混ざらないように）=================
if VOCAL and HARM:
    path = sys.argv[1]; js = _json2.load(open(path))
    main = js["vocals"][0]
    rng = []
    for nm_ in ("サビ1", "サビ2", "最後のサビ"):
        bs = S.sc(nm_); end = bs[-1] + 1
        if nm_ == "サビ1": end = bs[0] + 12      # 「ごめんなさい」の句はひとりで歌う
        rng.append((bs[0] * S.beats, end * S.beats, KL if nm_ == "最後のサビ" else K))
    SC = {}
    for kk in (K, KL):
        SC[id(kk)] = sorted({(midi(kk.mel(f"{d}:1", oct=4).split(":")[0]) % 12) for d in range(1, 8)})
    out = []; t = 0.0
    for tok in main["notes"].split():
        m = _re2.match(r"^([A-G][b#]?-?\d)([^:]*):([0-9.]+):(.+)$", tok)
        L_ = float(tok.split(":")[1])
        hit = [x for x in rng if x[0] - 1e-6 <= t < x[1]] if m else []
        if m and hit:
            pcs = SC[id(hit[0][2])]; p = midi(m.group(1)); steps = 0; q = p
            while steps < 2:
                q -= 1
                if q % 12 in pcs: steps += 1
            mk = m.group(2).replace("/", "").replace("!", "")
            out.append(f"{nm(q)}{mk}:{m.group(3)}:{m.group(4)}" if q >= 57 else f"R:{m.group(3)}")
        else:
            out.append(f"R:{L_:g}")
        t += L_
    harm = dict(main); harm.update({"notes": " ".join(out), "volume": float(_os2.environ.get("VTP_HVOL", "0.42")), "pan": 0, "vibrato": 22, "vibratoRate": 5.9, "vibratoMap": [],
                                    "blend": {"voice": "teto-soft", "amount": 0.45}, "reverb": 0.24, "dynamics": [], "consonant": 1.2})
    js["vocals"].append(harm)
    _json2.dump(js, open(path, "w"), ensure_ascii=False)
    print("  サビに3度下のハモリを入れた")
