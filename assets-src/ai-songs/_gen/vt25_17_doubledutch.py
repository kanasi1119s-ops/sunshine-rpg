# vt25 17「シンクロ・ダブルダッチ」Synchro Double Dutch（仮）— ダンス（リキッドのドラムンベース）。174・4/4。A の短調（サビは C 長調）→ 最後のサビは +1。
#   （表では F# の短調だったが、06 と同じになるので A の短調にした）
# 物語: クラスの大縄大会。練習のたびに、わたしが引っかかる。うしろのため息が聞こえる気がして、足がすくむ。縄の音がこわい。
#   放課後の庭で、縄をまわす子が「いち、に、でいいよ」と数えてくれた。その声に合わせて跳んだら、はじめて跳べた。空が近くなる。
#   本番の朝、同じはちまきで並ぶ。みんなの息がひとつになる。引っかかってもいい、もう一回跳ぼう。最後の一回、跳んでみる。
# 場面と強さ: ブレイク（ドラムンベースのブレイク・中）→ Aメロ1（ハーフ・語る）→ Bメロ1 → サビ1（ドラムンベース・強）→ 縄に引っかかる（止め・とても弱い）
#   → 間奏 → Aメロ2（放課後のふたり）→ Bメロ2 → サビ2（24小節）→ ジャンプ（間奏・いちばん激しい）→ Cメロ（ハーフ・弱）
#   → 最後のサビ（+1・24小節）→ ゴール（縄が止まる）
# 旋律の性格: 縄のリズムに合う、はずむ同音（G4 G4 G4 → C5）。Aメロは A3〜A4 で語り、サビは E5 まで。
# ほかの曲とちがう所（この曲だけの音）: 縄がまわる「ひゅん」（逆再生のシンバルのごく短い音）が、2拍ごとの拍になる。
#   引っかかる所は、全員が止まって縄の音だけが残る。
from vt25_lib import *

S = Song("17", "doubledutch", "シンクロ・ダブルダッチ（仮）", "Synchro Double Dutch", 174, 4, "A", "minor", "ダンス（リキッドのドラムンベース・ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --piano salamander --space hall --space-wet 0.14"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.5
K = Key("A", "minor")           # Aメロ・Bメロ（oct 3 で 1 = A3）
KC = Key("C", "major")          # サビ・Cメロ（oct 4 で 1 = C4）
KL = Key("Db", "major")         # 最後のサビ（+1）

A_CH = ["Am9", "Fmaj7", "Cmaj7", "G6"]
B_CH = ["Dm9", "Em7", "Fmaj7", "G", "Dm9", "Em7", "Fmaj7", "E7"]
C_CH = ["Fmaj7", "G", "Em7", "Am9", "Fmaj7", "G", "Cmaj7", "E7"]
C_CH2 = ["Fmaj7", "G", "Em7", "Am9", "Dm9", "G", "Cmaj7", "Cmaj7"]
X_CH = ["Am9", "Fmaj7", "Dm9", "G", "Am9", "Fmaj7", "Em7", "E7"]
LAST = [tr_chord(c, 1) for c in C_CH + C_CH2 + C_CH2]

S.scene("ブレイク", 10, "intro", A_CH * 2 + ["Fmaj7", "E7"])
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH + C_CH2)
S.scene("縄に引っかかる", 4, "break", ["Am9", "Am9", "Fmaj7", "E7"])
S.scene("間奏", 8, "break", A_CH * 2)
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 24, "chorus", C_CH + C_CH2 + C_CH2)
S.scene("ジャンプ", 16, "solo", A_CH * 3 + ["Dm9", "Em7", "Fmaj7", "E7"])
S.scene("Cメロ", 16, "bridge", X_CH[:7] + ["E7"] + X_CH[:7] + ["Ab7"])     # 最後の小節は +1 への入り口
S.scene("最後のサビ", 24, "chorus", LAST)
S.scene("ゴール", 10, "outro", [tr_chord(c, 1) for c in ["Fmaj7", "G", "Em7", "Am9", "Fmaj7", "G", "Cmaj7", "Cmaj7"]] + ["Db", "Db"])

V = Voice(S, vol=0.21, delay=0.75, bright=0.5, patch="surgeTropics", low=True)
PN = [S.track(f"ピアノ{i + 1}", "piano", volume=0.1, pan=-0.12, reverb=0.3, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 3}]) for i in range(4)]
PAD = [S.track(f"リキッドのパッド{i + 1}", "pad", **pad_spec("surgePadVerbPad", vol=0.04, pan=-0.35 + 0.35 * i, duck=0.45, sustain=1.5)) for i in range(3)]
PLK = S.track("プラック（縄のきらめき）", "pad", patch="surgeNicePluck", volume=0.055, pan=0.35, reverb=0.35, sustain=0.5,
              fx=[{"type": "filter", "kind": "highpass", "freq": 500, "q": 0.7}])
BASS = S.track("ベース", "bass", **synth_bass_spec("synthBass1", vol=0.2, duck=0.4))
SUB = S.track("サブベース", "sub808", volume=0.13, pan=0, sustain=0.9, fx=[{"type": "filter", "kind": "highpass", "freq": 30, "q": 0.7}])
ROPE = S.track("縄の「ひゅん」", "guitar", patch="cymbalFx", volume=0.03, pan=0.2, modulate=False)
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.055, pan=-0.3 + 0.3 * i, reverb=0.4, sustain=1.4) for i in range(3)]
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.06, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 3:0.5 3:0.5 3:0.5 5:1 3:1", "2:1 1:1 2:1 R:1", "R:0.5 5:0.5 5:0.5 5:0.5 7:1 5:1", "4:1.5 3:0.5 2:1 R:1"]
A1 = "おおなわたいかい/みんなでとぶんだ/れんしゅうのたびに/わたしがひっかかる/うしろのためいき/きこえるきがして/あしがすくむんだ/なわのおとこわい"
A2 = "ほうかごのにわで/ふたりでれんしゅう/なわをまわすこが/いちにでいいよと/かぞえるこえにね/あわせてとんだら/はじめてとべたの/そらがちかくなる"
VB = ["R:0.5 1':0.5 1':0.5 7:0.5 6:1 1':1", "7:1.5 6:0.5 5:1 R:1", "R:0.5 1':0.5 1':0.5 2':0.5 3':1 1':1", "2':1.5 1':0.5 7:1 R:1",
      "R:0.5 3':0.5 3':0.5 2':0.5 1':1 3':1", "2':1.5 1':0.5 7:1 R:1", "R:0.5 1':0.5 2':0.5 3':0.5 4':1 3':1", "#7:2 R:2"]
B1 = "いちにのさんでね/とびこんでみるの/こわくてもいいよ/まえをむいて"
B2 = "ほんばんのあさだ/くらすのみんなが/おなじはちまきで/ならんでるよ"
VC = ["R:0.5 5:0.5 5:0.5 5:0.5 1':1 6:1", "5:1 3:1 2:1 R:1", "R:0.5 5:0.5 5:0.5 5:0.5 2':1 7:1", "6:1.5 5:0.5 3:1 R:1",
      "R:0.5 6:0.5 6:0.5 6:0.5 3':1 2':1", "2':1.5 7:0.5 5:1 R:1", "R:0.5 3:0.5 5:0.5 6:0.5 1':1 2':1", "#5:2 R:2"]
VC2 = VC[:6] + ["R:0.5 3:0.5 5:0.5 6:0.5 1':1 2':1", "1':2 R:2"]
C1 = "しんくろするんだ/なわのおとあわせ/みんなのいきがね/ひとつになる/しんくろするんだ/ひっかかってもいいよ/もういっかいとぼう/いちにのさん"
C2 = ("しんくろするんだ/かぞえるかずより/みんなとそろったの/うれしいんだ/しんくろするんだ/まわるなわのなか/わたしのばしょだよ/とびこもうね/"
      "しんくろするんだ/そらへとどくまで/たかくとびあがれ/いちにのさん")
CL = ("しんくろするんだ/なわのおとあわせ/みんなのいきがね/ひとつになる/しんくろするんだ/もうこわくないよ/さいごのいっかいを/とんでみるよ/"
      "しんくろするんだ/ごーるのそのさき/みんなとわらうよ/いちにのさん")
VX = ["R:1 3:1 5:1 6:1", "5:3 R:1", "R:1 6:1 1':1 2':1", "2':3 R:1", "R:1 3':1 2':1 1':1", "6:3 R:1", "R:1 5:1 6:1 7:1", "#5:3 R:1"]
X1 = "なわとび/にがてで/ないてた/あのひも/いまはね/たのしい/いちにと/とべるよ"
LY = Lyrics(S)


def put(name, key, lines, text, o):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA * 4, A1, 3)
put("Bメロ1", K, VB, B1, 3); put("Bメロ2", K, VB, B2, 3)
put("サビ1", KC, VC + VC2, C1, 4); put("サビ2", KC, VC + VC2 + VC2, C2, 4)
put("Cメロ", KC, VX + VX, X1, 4)
put("最後のサビ", KL, VC + VC2 + VC2, CL, 4)
if VOCAL: put("Aメロ2", K, VA * 4, A2, 3)
else:
    for i, (b, l) in enumerate(zip(S.sc("Aメロ2"), VA * 4)):
        if i < 8: PLK.bar(b, K.mel(l, oct=4))
        else: V.bar(b, K.mel(l, oct=3))

# ================= 伴奏（リキッド: ピアノの和音・パッド・プラック） =================
prev = None
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; v4 = voice(ch, 66, 4, prev=prev); prev = v4; t = tones(ch, "A4", "A6"); pv = voice(ch, 60, 3)
    if n == "縄に引っかかる": continue
    if n == "ブレイク" and i < 4: continue
    if n == "ゴール" and i >= 8:
        if i == 8:
            for j in range(4): PN[j].bar(b, f"{nm(v4[j])}:8")
        continue
    if n.startswith(("サビ", "最後", "ジャンプ")) or n in ("間奏", "ゴール"):
        for j in range(4): PN[j].bar(b, f"{nm(v4[j])}:0.75 R:0.25 {nm(v4[j])}:0.5 R:1 {nm(v4[j])}:0.5 R:1")
        for j in range(3): PAD[j].bar(b, f"{nm(pv[j])}:4")
        if not (n == "Aメロ2" and not VOCAL): PLK.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" for q in (0, 2, 4, 2, 1, 3, 5, 3, 0, 2, 4, 2, 1, 3, 5, 3)) if n == "ジャンプ" else
                                                    " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 4, 3, 1, 3, 2, 4)))
        if n.startswith(("サビ2", "最後")) or n == "ジャンプ":
            for j in range(3): STR[j].bar(b, f"{nm(pv[j])}:4")
    elif n in ("Aメロ1", "Aメロ2", "ブレイク", "Cメロ"):
        for j in range(4): PN[j].bar(b, f"{nm(v4[j])}:2 R:2" if i % 2 == 0 else f"R:1 {nm(v4[j])}:3")
        if n == "Cメロ" or i >= 8:
            for j in range(3): PAD[j].bar(b, f"{nm(pv[j])}:4")
    elif n in ("Bメロ1", "Bメロ2"):
        for j in range(4): PN[j].bar(b, f"{nm(v4[j])}:1 {nm(v4[j])}:1 {nm(v4[j])}:1 {nm(v4[j])}:1")
        for j in range(3): PAD[j].bar(b, f"{nm(pv[j])}:4")

# ================= ベース（ドラムンベース: 長い低音と、2拍目の裏で動く） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n == "縄に引っかかる" or (n == "ブレイク" and i < 4): continue
    if n == "ゴール" and i >= 8:
        if i == 8: BASS.bar(b, f"{nm(r)}:8")
        continue
    if n.startswith(("サビ", "最後", "ジャンプ")) or n in ("間奏", "ゴール"):
        BASS.bar(b, f"{nm(r)}:1.5 R:1 {nm(r)}:0.5 {nm(r + 12)}:0.5 {nm(r + 10)}:0.5")
        SUB.bar(b, f"{nm(r + 12 if r < 30 else r)}:2.5 R:1.5")
    else:
        BASS.bar(b, f"{nm(r)}:3 R:1" if n != "Bメロ1" and n != "Bメロ2" else bass_line(S, b, "half", lo="E1"))

# ================= 縄の「ひゅん」（2拍ごと。サビとジャンプだけ） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n.startswith(("サビ", "最後", "ジャンプ")) or n == "縄に引っかかる" or (n == "ブレイク" and i >= 4):
        ROPE.bar(b, "R:1.5 C4:0.5 R:1.5 C4:0.5" if n != "縄に引っかかる" or i < 2 else ("R:1.5 C4:0.5 R:2" if i == 2 else "R:4"))
# 引っかかったあと: 縄がゆっくり止まり、ピアノの和音がそっと鳴って、もう一度はじまる
for j in range(4): PN[j].bar(S.sc("縄に引っかかる")[3], f"{nm(voice(S.chords[S.sc('縄に引っかかる')[3]], 66, 4)[j])}:4,")
riser(FX, S.sc("サビ1")[0], 4, "C4"); riser(FX, S.sc("ジャンプ")[0], 4, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 2, "E4")

# ================= ドラム（Aメロはハーフ、サビとジャンプはドラムンベース） =================
DNB2 = ("X.........X.....", "....X..o.o..X..o", "x.x.x.x.x.x.x.xO")
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "ブレイク":
        vgroove(D, b, "dnb", ghosts=0.4, seed=b) if i < 8 else vgroove(D, b, "dnb", ghosts=0.4, seed=b, k=DNB2[0], s=DNB2[1], h=DNB2[2])
        if i == 4: crash(D, b)
        if last: put_fill(D, b, "snare16")
    elif n in ("Aメロ1", "Aメロ2"):
        vgroove(D, b, "half", ghosts=0.25, seed=b)
        if i == 0: crash(D, b, "C2", 3)
        if last: put_fill(D, b, "small")
    elif n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "halfdrive", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 1)
    elif n.startswith(("サビ", "最後")) or n in ("間奏", "ジャンプ", "ゴール"):
        if n == "ゴール" and i >= 8:
            if i == 8: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 6)
            continue
        if i % 2 == 0: vgroove(D, b, "dnb", ghosts=0.35, seed=b)
        else: vgroove(D, b, "dnb", ghosts=0.35, seed=b, k=DNB2[0], s=DNB2[1], h=DNB2[2])
        if i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
        if i % 8 == 7 and not last: put_fill(D, b, "snare16" if i % 16 == 15 else "small")
    elif n == "Cメロ":
        vgroove(D, b, "half", ghosts=0.15, seed=b)
        if last: put_fill(D, b, "build")

# 止め: Bメロ2 の最後。縄に引っかかる: 4小節、縄の音だけ（はじめの2小節）
SIL.add(S.sc("Bメロ1")[-1], 1, 4); SIL.add(S.sc("Bメロ2")[-1], 1, 4)
SIL.add(S.sc("最後のサビ")[0] - 1, 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の17。ダンス（リキッドのドラムンベース）。A の短調（サビは C）・174、最後のサビは +1。"
          "クラスの大縄大会で、みんなと息を合わせて跳ぶ。ドラムンベースのブレイクで始まり、ハーフの Aメロ、縄がまわる「ひゅん」が拍になるサビ、"
          "縄に引っかかって全員が止まる静けさ、いちばん激しい間奏、最後は縄が止まって和音で終わる。自作")
finish(S, LY, V, 0, fx=[{"type": "ott", "scenes": ["ジャンプ"], "depth": 0.3}],
       level={"verse": -0.25}, special={"Cメロ": -0.4, "最後のサビ": 0.5})
