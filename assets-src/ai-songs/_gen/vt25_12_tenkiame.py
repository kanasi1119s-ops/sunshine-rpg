# vt25 12「天気雨のアンダンテ」Sunshower Andante（仮）— J-POP（6/8 のバラード）。6/8・付点4分＝68（8分＝204 で書く）。B♭長調 → 最後のサビは +2（C）。
# 物語: 卒業式のあとの帰り道。晴れているのに、雨が降る。傘はいらない、このくらいなら。ほほがぬれても、雨のせい。
#   教室の窓も、らくがきの机も、ぜんぶ置いていく。笑っていたのに、門を出たとき雨がきた。泣かないつもりでいたけれど、空はなんでもお見通し。
#   本当はさみしい。言えなくて「またね」。天気雨がやんだら、虹が出る。ありがとう、またいつか、晴れの日に。
# 場面と強さ: 雨（雨の音とピアノ・とても弱い）→ 1番（ピアノだけ・弱。Aメロ1 → Bメロ1 → サビ1）→ 間奏 → 2番（ドラムとベースが入る。Aメロ2 → Bメロ2 → サビ2・24小節）
#   → Cメロ（本当はさみしい）→ 落ちサビ（ピアノと歌）→ 最後のサビ（+2・いちばん強い）→ 雨がやむ（1音）
# 句の終わりは8分の休み（息つぎ）。
# 旋律の性格: 大きな上下の跳躍（B♭4 → D5、F4 → D5）と、付点4分ののびやかな長い音。8分のつなぎは和音の音で。
# ほかの曲とちがう所（この曲だけの音）: 晴れているのに雨の音（明るい長調の和音と、雨の音がいっしょに鳴る）。6/8 のゆれ。ドラムは2番から。
from vt25_lib import *

S = Song("12", "tenkiame", "天気雨のアンダンテ（仮）", "Sunshower Andante", 204, 6, "Bb", "major", "J-POP（6/8 のバラード・ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --piano salamander --space hall --space-wet 0.18"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
K = Key("Bb", "major")          # oct 3 で 1 = B♭3。歌うのは C4〜D5（最後のサビは E5 まで）
KL = Key("C", "major")          # 最後のサビ（+2）

A_CH = ["Bb", "F/A", "Gm7", "Dm7", "Ebmaj7", "Bb/D", "Cm7", "F"]
B_CH = ["Ebmaj7", "F", "Gm7", "Ebmaj7", "Cm7", "F", "Ebmaj7", "F"]
C_CH = ["Bb", "F/A", "Gm7", "Ebmaj7", "Bb/D", "Cm7", "Fsus4", "F", "Bb", "F/A", "Gm7", "Ebmaj7", "Bb/D", "Cm7", "Ebmaj7", "Bb"]
X_CH = ["Gm7", "Dm7", "Ebmaj7", "Bb/D", "Cm7", "Gm7", "Ebmaj7", "F"]
LAST = [tr_chord(c, 2) for c in C_CH]

S.scene("雨", 4, "intro", ["Bb", "Ebmaj7", "Bb", "F"])
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 8, "break", ["Bb", "F/A", "Gm7", "Ebmaj7", "Bb", "F/A", "Ebmaj7", "F"])
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 24, "chorus", C_CH + C_CH[8:])
S.scene("Cメロ", 8, "bridge", X_CH)
S.scene("落ちサビ", 8, "bridge", C_CH[:7] + ["G7"])            # 最後の小節は C への入り口
S.scene("最後のサビ", 16, "chorus", LAST)
S.scene("雨がやむ", 8, "outro", ["Fmaj7", "G", "Em7", "Am7", "Fmaj7", "G", "Cmaj9", "Cmaj9"])

V = Voice(S, vol=0.21, delay=0.5, bright=0.0, patch="oboe", low=False)
PL = S.track("ピアノ（左手）", "piano", volume=0.15, pan=-0.12, reverb=0.3, fx=[{"type": "eq", "low": -1, "mid": -2, "midHz": 400, "high": 2}])
PR = S.track("ピアノ（右手）", "piano", volume=0.15, pan=-0.12, reverb=0.3, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 3}])
PRM = S.track("ピアノ（歌を受け取る）", "piano", volume=0.17, pan=-0.12, reverb=0.3, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 3}])
GTR = S.track("アコースティックギター（アルペジオ）", "guitar", amp="crystal", volume=0.075, pan=0.4, reverb=0.3, chorus=0, sustain=1.0)
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.065, pan=-0.35 + 0.35 * i, reverb=0.45, sustain=1.6) for i in range(3)]
VLN = S.track("バイオリン（対旋律）", "fiddle", patch="violin", volume=0.08, pan=0.3, reverb=0.45, gainDb=1, bright=-0.3, attack=0.1, release=0.6)
BASS = S.track("ベース", "bass", **finger_bass_spec(vol=0.19))
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.05, pan=0, modulate=False)
D = S.drumkit()                 # 6/8: 1小節＝24マス（8分＝4マス）
SIL = Silence(S)

# ================= 歌（拍＝8分音符。付点4分＝3） =================
VA = ["3:1 2:1 1:1 5:3", "6:2 5:1 3:2 R:1", "5:1 6:1 5:1 3:3", "2:2 3:1 2:2 R:1", "1:1 2:1 3:1 5:3", "6:2 5:1 3:2 R:1", "4:1 5:1 6:1 1':3", "7:3 R:3"]
A1 = "そつぎょうしきの/かえりみちだよ/はれているのに/あめがふる/かさはいらない/このくらいなら/ほほがぬれても/あめのせい"
A2 = "きょうしつのまど/らくがきつくえ/ぜんぶおいてく/さよならね/わらっていたのに/ずっとへいきでね/もんをでたとき/あめがきた"
VB = ["5:1 6:1 1':1 2':3", "2':2 6:1 5:2 R:1", "6:1 1':1 2':1 3':3", "2':2 1':1 6:2 R:1", "1':1 2':1 3':1 4':3", "3':2 2':1 2':2 R:1", "1':1 2':1 3':1 5':3", "4':3 R:3"]
B1 = "なかないつもり/でいたんだけど/そらはなんでも/おみとおし"
B2 = "さいごのちゃいむ/ききおえたあと/かおをあげたら/あおいそら"
VC = ["1':3 3':3", "2':2 7:1 5:2 R:1", "6:1 1':1 2':1 3':3", "2':3 R:3", "5:3 3':3", "2':2 1':1 6:2 R:1", "5:1 6:1 1':1 2':3", "7:3 R:3"]
VC2 = VC[:6] + ["5:1 6:1 1':1 2':3", "1':3 R:3"]
C1 = "てんきあめ/あおぞらに/ひかるつぶ/なきながら/てんきあめ/さよならは/はれのひに/あうといい"
C2 = "てんきあめ/そのままで/いいんだよ/そらもなく/てんきあめ/まぶしくて/めをとじた/あめのおと/てんきあめ/みんなのね/かさのはな/ひらいてく"
CL = "てんきあめ/やんだなら/にじがでる/あるきだす/てんきあめ/ありがとう/またいつか/はれのひに"
CO = "てんきあめ/しずかだね/ふたりだけ/かさのした"
VX = ["5:3 6:3", "5:2 3:1 2:2 R:1", "3:3 5:3", "6:2 5:1 3:2 R:1", "4:3 5:3", "6:2 1':1 6:2 R:1", "1':3 2':3", "2':5 R:1"]
X1 = "ほんとはね/さみしいの/いえなくて/またね"
LY = Lyrics(S)


def put(name, key, lines, text, o=3):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA + VA, A1)
put("Bメロ1", K, VB, B1); put("Bメロ2", K, VB, B2)
put("サビ1", K, VC + VC2, C1); put("サビ2", K, VC + VC2 + VC2, C2)
put("Cメロ", K, VX, X1)
put("落ちサビ", K, VC, CO)
put("最後のサビ", KL, VC + VC2, CL, o=4)     # C 長調は oct 4 で 1 = C4（B♭ の oct 3 と同じ高さの並び）
if VOCAL: put("Aメロ2", K, VA + VA, A2)
else:
    for i, (b, l) in enumerate(zip(S.sc("Aメロ2"), VA + VA)):
        if i < 8: PRM.bar(b, K.mel(l, oct=4))
        else: V.bar(b, K.mel(l, oct=3))

# ================= ピアノ（6/8: 左手は根音と5度・10度の分散、右手は和音） =================
prev = None
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "C2"); v4 = voice(ch, 65, 4, prev=prev); prev = v4
    third = r + (3 if "m" in ch.split("/")[0][1:3] else 4) + 12
    if n == "雨" and i < 2:
        PR.bar(b, f"{nm(v4[0])}:3 {nm(v4[2])}:3"); continue
    if n == "雨がやむ":
        if i < 6: PL.bar(b, f"{nm(r)}:1 {nm(r + 7)}:1 {nm(third)}:1 {nm(r + 12)}:1 {nm(r + 7)}:1 {nm(third)}:1"); PR.bar(b, f"{nm(v4[1])}:3 {nm(v4[3])}:3")
        elif i == 6: PL.bar(b, f"{nm(r)}:12"); PR.bar(b, " ".join(f"{nm(x)}:0.5" for x in v4) + f" {nm(v4[3] + 12)}:10")
        continue
    PL.bar(b, f"{nm(r)}:1 {nm(r + 7)}:1 {nm(third)}:1 {nm(r + 12)}:1 {nm(r + 7)}:1 {nm(third)}:1")
    if n in ("サビ1", "サビ2", "最後のサビ", "間奏"):
        PR.bar(b, f"{nm(v4[0])}:1 {nm(v4[1])}:1 {nm(v4[2])}:1 {nm(v4[3])}:3")
    elif n.startswith("Bメロ"):
        PR.bar(b, f"R:1 {nm(v4[1])}:1 {nm(v4[2])}:1 R:1 {nm(v4[2])}:1 {nm(v4[3])}:1")
    else:
        PR.bar(b, f"R:3 {nm(v4[1])}:1 {nm(v4[2])}:1 {nm(v4[3])}:1" if i % 2 == 0 else f"{nm(v4[0])}:3 R:3")

# ================= ギター・ストリングス・バイオリン（2番から少しずつ） =================
VLM = ["D6:3 F6:3", "Eb6:3 C6:3", "D6:2 C6:1 Bb5:3", "C6:6", "F5:3 D6:3", "Eb6:3 G5:3", "A5:2 C6:1 Eb6:3", "D6:6"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; t = tones(ch, "F3", "F5"); sv = voice(ch, 62, 3)
    if n in ("Aメロ2", "Bメロ2", "サビ2", "Cメロ", "最後のサビ") or (n == "間奏" and i >= 4):
        GTR.bar(b, " ".join(f"{nm(t[q % len(t)])}:1" for q in (0, 2, 4, 3, 2, 1)))
    if n in ("Bメロ2", "サビ2", "最後のサビ", "Cメロ") or (n == "サビ1" and i >= 8) or n == "雨がやむ" and i < 7:
        for j in range(3): STR[j].bar(b, f"{nm(sv[j])}:6" if n != "雨がやむ" or i < 6 else f"{nm(sv[j])}:12")
    if n == "サビ2" and i >= 16: VLN.bar(b, VLM[i - 16])
    if n == "最後のサビ" and i >= 8: VLN.bar(b, " ".join(f"{nm(midi(x.split(':')[0]) + 2)}:{x.split(':')[1]}" for x in VLM[i - 8].split()))

# ================= ベース（2番から） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n in ("Aメロ2", "Bメロ2", "サビ2", "Cメロ", "最後のサビ") or (n == "間奏" and i >= 4):
        BASS.bar(b, f"{nm(r)}:3 {nm(r + 7)}:2 {nm(r)}:1" if not n.startswith(("サビ", "最後")) else f"{nm(r)}:2 {nm(r)}:1 {nm(r + 7)}:2 {nm(r + 12)}:1")
    elif n == "雨がやむ" and i < 7:
        BASS.bar(b, f"{nm(r)}:6" if i < 6 else f"{nm(r)}:12")

# ================= 雨の音（晴れているのに鳴る）=================
season(S, S.sc("雨")[0], "雨", beats=6 * 4 + 6 * 16, vol=0.07, every=24)
season(S, S.sc("落ちサビ")[0], "雨", beats=6 * 8, vol=0.06, every=24)
season(S, S.sc("雨がやむ")[0], "雨", beats=6 * 4, vol=0.05, every=24)
season(S, S.sc("雨がやむ")[6], "小鳥", beats=12, vol=0.05)
cym_swell(CYM, S.sc("サビ2")[0], 3, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 6, "E4")

# ================= ドラム（2番から。6/8: キックは1拍目、スネアは4拍目、ハイハットは8分） =================
K68, S68, H68 = "X.......x...........x...", "............X...........", "x...x...x...x...x...x..."
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("Aメロ2",):
        D.set(b, "X.......................", "............o...........", H68 if i >= 8 else "x.......x.......x.......")
        if last: D.set(b, K68, "............X...XXXXXXXX", "........................")
    elif n in ("Bメロ2", "Cメロ"):
        D.set(b, K68, S68, H68)
        if last: D.set(b, K68, "............X.X.XXXXXXXX", "........................")
    elif n in ("サビ2", "最後のサビ"):
        D.set(b, "X.....x.x...X.......x...", "............X.........o.", "x.x.x.x.x.x.x.x.x.x.x.x.")
        if i % 8 == 0: crash(D, b, "C2", 6)
        if i % 8 == 7 and not last: D.set(b, K68, "............X...XXXXXXXX", "........................")
    elif n == "間奏" and i >= 4:
        D.set(b, K68, S68, H68)
        if last: D.set(b, K68, "............X.X.XXXXXXXX", "........................")
    elif n == "雨がやむ" and i < 6:
        D.set(b, K68, S68, H68 if i < 4 else "x...........x...........")
        if i == 0: crash(D, b, "C2", 6)

SIL.add(S.sc("最後のサビ")[0] - 1, 4, 6)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の12。J-POP（6/8 のバラード）。B♭長調・付点4分＝68、最後のサビは +2（C）。"
          "卒業式のあと、晴れているのに雨が降る。泣いているのを空のせいにする。雨の音とピアノで始まり、1番はピアノだけ、2番からドラムとベース、"
          "大きく跳ぶ旋律と付点4分ののびやかな長い音、明るい和音と雨の音がいっしょに鳴る。雨がやんで小鳥の声と1音で終わる。自作")
finish(S, LY, V, 0, level={"verse": -0.35}, special={"Aメロ1": -0.5, "落ちサビ": -0.55, "Cメロ": -0.35, "最後のサビ": 0.55},
       vib={"chorus": 40, "verse": 30})
