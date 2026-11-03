# vt25 04「ラストオーダー・ラプソディ」Last Order Rhapsody（仮）— ロック（高速ロック）。192・4/4。D の短調（サビは平行調の F）→ 最後のサビは +1（G♭）。
#   （表では C#m→E だったが、第1弾の 19 が同じ調・近い速さだったので、D の短調 → F に変えた）
# 物語: アルバイト最後の夜。エプロンをしめて、いつものお客さんの、いつもの注文。お皿を割って泣いた初めての日も、まかないのパスタも、
#   ぜんぶ宝物。店長の口ぐせは「まあ、なんとかなる」。ラストオーダーの声がひびいて、閉店のあと、シャッターの前で、
#   まだ言えていなかった「ありがとう」を言う。泣かないで、笑顔で終わるって決めていた。最後に店の明かりが消えて、テープが止まるように音が落ちる。
# 場面と強さ: 開店のリフ（いきなりギター・強）→ Aメロ1（16分の語り・中）→ Bメロ1（止め）→ サビ1（強）→ リフ → Aメロ2 → Bメロ2（止め）
#   → サビ2（強・24小節）→ ギターソロ → レジを締める（全員休み・レジの鈴とピアノ1音だけ）→ Cメロ（思い出・ハーフ）→ 落ちサビ（ピアノと歌・弱）
#   → 1拍の無音 → 最後のサビ（+1・いちばん強い・32小節）→ 閉店（リフ → テープが止まるように音が落ちて終わる）
# 旋律の性格: Aメロは 16分の弾みと休符で語る（A4 の連打から D5 へ跳ぶ）。サビは5度の跳躍（F4 → C5）で入り、F5 まで。
#   止めは Bメロの終わり2回・サビ1とサビ2の終わり2回の、合わせて4回。
# ほかの曲とちがう所（この曲だけの音）: 最後に曲ごと回転が落ちて止まる（テープストップ）。レジの「チーン」と、閉店の全員休み。
from vt25_lib import *

S = Song("04", "lastorder", "ラストオーダー・ラプソディ（仮）", "Last Order Rhapsody", 192, 4, "D", "minor", "ロック（高速ロック・ボカロ）")
S.kit = "naked-x"
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags + " --piano salamander"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.6
S.keepers = {"Aメロ1": "closed", "Aメロ2": "ride", "サビ1": "wash", "サビ2": "open", "最後のサビ": "wash", "ギターソロ": "bell"}
K = Key("D", "minor")          # oct 4 で 1 = D4
KF = Key("F", "major")         # Bメロ・サビ（oct 4 で 1 = F4）
KL = Key("Gb", "major")        # 最後のサビ（+1）

RIFF_CH = ["Dm", "Dm", "Bb", "C", "Dm", "Dm", "Bb", "A7"]
A_CH = ["Dm", "Bbmaj7", "C", "Am7", "Gm7", "Bb", "Eb", "A7"]
B_CH = ["Bbmaj7", "C", "Am7", "Dm7", "Gm7", "Am7", "Bbmaj7", "C"]
C_CH = ["F", "C", "Dm7", "Bbmaj7", "F", "Am7", "Gm7", "C"]
C_CH2 = ["F", "C", "Dm7", "Bbmaj7", "F", "Am7", "Bbmaj7", "F"]
X_CH = ["Bbmaj7", "C", "Am7", "Dm7", "Gm7", "Am7", "Bbmaj7", "C"]
LAST = [tr_chord(c, 1) for c in (C_CH + C_CH2) * 2]

S.scene("開店のリフ", 8, "intro", RIFF_CH)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH + C_CH2)
S.scene("リフ", 12, "break", RIFF_CH + ["Dm", "Bb", "C", "A7"])
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 24, "chorus", C_CH + C_CH2 + C_CH2)
S.scene("ギターソロ", 16, "solo", RIFF_CH * 2)
S.scene("レジを締める", 4, "break", ["Bbmaj7", "Bbmaj7", "C", "C"])
S.scene("Cメロ", 16, "bridge", X_CH * 2)
S.scene("落ちサビ", 8, "bridge", C_CH[:7] + ["Db7"])          # 最後の小節は G♭ への入り口（D♭7）
S.scene("最後のサビ", 32, "chorus", LAST)
S.scene("閉店", 10, "outro", [tr_chord(c, 1) for c in RIFF_CH] + ["Ebm", "Ebm"])

V = Voice(S, vol=0.22, delay=0.75, bright=0.8, patch="modernLead", low=True)
GT = [S.track(f"ギター1（{['根音', '5度', 'オクターブ'][i]}）", "distGuitar", **rock_gtr_spec(0.07, -0.45 + 0.45 * i)) for i in range(3)]
LG = S.track("ギター2（リフ）", "leadGuitar", **lead_gtr_spec(0.11, 0.2))
LGS = S.track("ギター2（ソロ）", "leadGuitar", **lead_gtr_spec(0.15, 0.0))
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.24))
PNFX = [{"type": "eq", "low": -3, "mid": -1, "midHz": 400, "high": 3}]
PM = S.track("ピアノ（合いの手）", "piano", volume=0.16, pan=-0.15, reverb=0.22, fx=PNFX)
PC = [S.track(f"ピアノ（和音{i + 1}）", "piano", volume=0.1, pan=-0.15, reverb=0.22, fx=PNFX) for i in range(3)]
ORG = [S.track(f"オルガン{i + 1}", "drawbarOrgan", volume=0.05, pan=0.3, reverb=0.25, sustain=1.0) for i in range(3)]
REG = S.track("レジの鈴（チーン）", "pad", patch="surgeBell1", volume=0.07, pan=0.35, reverb=0.4, sustain=1.5)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 5:0.25 5:0.25 5:0.5 4:0.5 3:0.5 R:0.5 3:0.5 4:0.5", "5:1 1':1 R:2",
      "R:0.5 5:0.25 5:0.25 5:0.5 6:0.5 7:0.5 R:0.5 7:0.5 6:0.5", "5:2 R:2",
      "R:0.5 1':0.25 1':0.25 1':0.5 7:0.5 6:0.5 R:0.5 6:0.5 7:0.5", "7:1 1':1 R:2",
      "R:0.5 4:0.25 4:0.25 4:0.5 5:0.5 6:0.5 R:0.5 5:0.5 4:0.5", "5:2 R:2"]
A1 = "さいごのしふとのひ/えぷろんをしめる/いつものおきゃくさん/いつものちゅうもん/ふたりでわらってたの/まかないのぱすた/しかられたひもある/ぜんぶたからもの"
A2 = "てんちょうのくちぐせ/まあなんとかなる/そのことばにいつも/すくわれていたの/せんぱいのてがみが/ろっかーにはいってた/またきてねなんてさ/なみだがでちゃうよ"
VB = ["R:0.5 3:0.5 3:0.5 4:0.5 5:1 3:1", "2:1.5 1:0.5 2:1 R:1", "R:0.5 3:0.5 3:0.5 4:0.5 5:1 6:1", "5:1.5 3:0.5 2:1 R:1",
      "R:0.5 4:0.5 4:0.5 5:0.5 6:1 4:1", "5:1.5 4:0.5 3:1 R:1", "R:0.5 6:0.5 7:0.5 1':0.5 7:1 6:1", "5:1 R:3"]
B1 = "ありがとうってこと/まだいえてないよ/とけいのはりがね/すすんでいく"
B2 = "らすとおーだーの/こえがひびいたら/みせのあかりもね/きえちゃうんだ"
VC = ["R:0.5 1:0.5 5:1 5:0.5 6:0.5 5:1", "4:0.5 3:0.5 2:1 R:2", "R:0.5 2:0.5 6:1 6:0.5 7:0.5 6:1", "5:0.5 4:0.5 3:1 R:2",
      "R:0.5 3:0.5 1':1 1':0.5 7:0.5 1':1", "7:0.5 6:0.5 5:1 R:2", "R:0.5 4:0.5 5:0.5 6:0.5 7:1 1':1", "5:2 R:2"]
VC2 = VC[:6] + ["R:0.5 6:0.5 6:0.5 5:0.5 4:1 3:1", "1:2 R:2"]
C1 = "ありがとういうよ/しゃったーのまえでね/えぷろんたたんで/またねっていう/らすとおーだーは/さよならじゃないよ/あしたのわたしへ/つづくからね"
C2 = (C1.split("/")[0] + "/てんちょうのせなか/ふかくおじぎして/こえにしたよ/らすとおーだーで/なみだはだめだよ/えがおでおわるの/きめてたから/"
      "おつかれさまだね/みんながわらうよ/さいごのまかない/おいしいよね")
CL = ("ありがとういうよ/いまならいえるよ/このみせのぜんぶ/ありがとうね/" + "/".join(C1.split("/")[4:]) + "/"
      "しゃったーがおりてく/あかりがきえても/このよるのことは/わすれないよ/ほんとにほんとに/たのしかったんだよ/こんどはおきゃくで/きますからね")
CO = "ありがとういうよ/ちいさなこえでも/とどきますように/このみせへと"
VX = ["R:1 3:1 4:1 5:1", "6:2 5:2", "R:1 5:1 6:1 7:1", "1':3 R:1", "R:1 6:1 5:1 4:1", "3:2 2:2", "R:1 4:1 5:1 6:1", "5:4"]
X1 = "はじめては/こわかった/おさらわった/ないてた/だけどいま/わかるよ/ここにいた/いみがね"
LY = Lyrics(S)


def put(name, key, lines, text, o=4):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA + VA, A1)
put("Bメロ1", KF, VB, B1); put("Bメロ2", KF, VB, B2)
put("サビ1", KF, VC + VC2, C1)
put("サビ2", KF, VC + VC2 + VC2, C2)
put("Cメロ", KF, VX + VX, X1)
put("落ちサビ", KF, VC, CO)
put("最後のサビ", KL, (VC + VC2) * 2, CL)
if VOCAL: put("Aメロ2", K, VA + VA, A2)
else:
    for i, (b, l) in enumerate(zip(S.sc("Aメロ2"), VA + VA)):
        if i < 8: LG.bar(b, K.mel(l, oct=4))
        else: V.bar(b, K.mel(l, oct=4))

# ================= ギター（刻みとリフ） =================
RIFF = ["D5:0.25 R:0.25 D5:0.25 F5:0.25 R:0.25 A5:0.25 G5:0.5 F5:0.25 R:0.25 E5:0.25 D5:0.25 C5:0.5 A4:0.5",
        "D5:0.25 R:0.25 D5:0.25 F5:0.25 R:0.25 A5:0.25 C6:0.5 A5:0.5 G5:0.5 F5:0.5 E5:0.5"]
RIFF_L = ["D5:0.25 R:0.25 D5:0.25 F5:0.25 R:0.25 A5:0.25 G5:0.5 F5:0.25 R:0.25 E5:0.25 D5:0.25 C5:0.5 A4:0.5",
          "Bb4:0.5 D5:0.5 F5:0.5 D5:0.5 C5:0.5 E5:0.5 G5:0.5 E5:0.5"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; pw = power(ch, "E2")
    if n in ("開店のリフ", "リフ", "閉店"):
        LG.bar(b, RIFF[0] if i % 4 in (0, 1) else (RIFF[1] if i % 4 == 2 else RIFF_L[1]))
        for j in range(3): GT[j].bar(b, " ".join(f"{nm(pw[j])}:0.25{'!' if q % 4 == 0 else ''}" if q % 8 != 7 else "R:0.25" for q in range(16)))
    elif n in ("Aメロ1", "Aメロ2"):
        # Aメロ: ブリッジミュートを使わず、2拍ずつ鳴らして（あいだは歌のすき間）
        for j in range(3): GT[j].bar(b, f"{nm(pw[j])}:1.5 R:0.5 {nm(pw[j])}:0.5 {nm(pw[j])}:1.5" if i % 2 == 0 else f"{nm(pw[j])}:2 R:1 {nm(pw[j])}:0.5 {nm(pw[j])}:0.5")
    elif n in ("Bメロ1", "Bメロ2"):
        for j in range(3): GT[j].bar(b, " ".join(f"{nm(pw[j])}:0.5" for _ in range(8)))
    elif n in ("サビ1", "サビ2", "最後のサビ", "ギターソロ"):
        for j in range(3): GT[j].bar(b, f"{nm(pw[j])}:0.75! {nm(pw[j])}:0.75 {nm(pw[j])}:0.5 {nm(pw[j])}:1 {nm(pw[j])}:0.5 {nm(pw[j])}:0.5")
    elif n == "Cメロ":
        for j in range(3): GT[j].bar(b, f"{nm(pw[j])}:4" if i < 8 else f"{nm(pw[j])}:2 {nm(pw[j])}:2")
SOLO = ["R:0.5 A5:0.5 D6:1^ C6:0.5 A5:0.5 G5:1", "F5:0.5 G5:0.5 A5:2~ R:1", "R:0.5 Bb5:0.5 D6:0.5 F6:0.5 E6:1 D6:1", "C6:1.5 A5:0.5 E5:2~",
        "D5:0.25 F5:0.25 A5:0.25 D6:0.25 F6:1^ E6:0.5 D6:0.5 C6:1", "A5:3~ R:1", "Bb5:0.5 C6:0.5 D6:0.5 E6:0.5 F6:1 G6:1", "E6:2 C#6:2~",
        "D6:0.25 C6:0.25 A5:0.25 G5:0.25 F5:0.25 G5:0.25 A5:0.5 D6:2", "R:1 F6:1 E6:1 D6:1", "C6:1 A5:1 G5:1 F5:1", "E5:2 G5:2",
        "D6:1.5 C6:0.5 A5:1 G5:1", "F5:1 G5:1 A5:2", "Bb5:1 A5:1 G5:1 F5:1", "E5:2 A5:2~"]
for i, b in enumerate(S.sc("ギターソロ")): LGS.bar(b, SOLO[i])

# ================= ピアノ・オルガン =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; v = voice(ch, 66, 3); t = tones(ch, "C5", "C7")
    if n in ("サビ1", "サビ2", "最後のサビ"):
        for j in range(3): PC[j].bar(b, f"{nm(v[j])}:0.75 {nm(v[j])}:0.75 {nm(v[j])}:0.5 {nm(v[j])}:2")
        ov = voice(ch, 60, 3)
        for j in range(3): ORG[j].bar(b, f"{nm(ov[j])}:4")
        if i % 4 == 1: PM.bar(b, "R:2 " + " ".join(f"{nm(x)}:0.25" for x in sorted(t[:8], reverse=True)))      # 16分の駆け下り
    elif n in ("Bメロ1", "Bメロ2"):
        for j in range(3): PC[j].bar(b, f"{nm(v[j])}:1 {nm(v[j])}:1 {nm(v[j])}:1 {nm(v[j])}:1")
    elif n in ("Aメロ1", "Aメロ2"):
        if i % 4 == 3: PM.bar(b, "R:2.5 " + " ".join(f"{nm(x)}:0.25" for x in t[:6]))                   # 句の終わりの合いの手
    elif n == "Cメロ":
        for j in range(3): PC[j].bar(b, f"{nm(v[j])}:2 {nm(v[j])}:2")
        ov = voice(ch, 60, 3)
        for j in range(3): ORG[j].bar(b, f"{nm(ov[j])}:4")
    elif n == "落ちサビ":
        PM.bar(b, f"{nm(low(ch, 'C3'))}:1 {nm(v[0])}:1 {nm(v[1])}:1 {nm(v[2])}:1")
    elif n == "レジを締める":
        if i == 0: PM.bar(b, f"{nm(v[2])}:4")
        if i == 2: PM.bar(b, f"{nm(v[1])}:4")
REG.bar(S.sc("レジを締める")[0], "R:1 E6:3"); REG.bar(S.sc("レジを締める")[2], "R:2 E6:2")
REG.bar(S.sc("開店のリフ")[0], "E6:1 R:3")                                       # 開店の「チーン」

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n in ("開店のリフ", "リフ", "閉店", "ギターソロ"): BASS.bar(b, bass_line(S, b, "root8", lo="E1"))
    elif n in ("Aメロ1", "Aメロ2"): BASS.bar(b, bass_line(S, b, "push" if i % 2 else "root8", lo="E1"))
    elif n in ("Bメロ1", "Bメロ2"): BASS.bar(b, bass_line(S, b, "root8", lo="E1"))
    elif n in ("サビ1", "サビ2", "最後のサビ"): BASS.bar(b, bass_line(S, b, "oct8" if i % 4 != 3 else "walk", lo="E1"))
    elif n == "Cメロ": BASS.bar(b, bass_line(S, b, "half" if i < 8 else "root8", lo="E1"))
    elif n == "落ちサビ" and i == 7: BASS.bar(b, bass_line(S, b, "long", lo="E1"))

riser(FX, S.sc("サビ1")[0], 4, "C4"); riser(FX, S.sc("サビ2")[0], 4, "C4")
cym_swell(CYM, S.sc("最後のサビ")[0], 4, "E4"); cym_swell(CYM, S.sc("Cメロ")[0], 2, "C4")

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("開店のリフ", "リフ", "閉店"):
        vgroove(D, b, "vrock", ghosts=0.25, seed=b)
        if i == 0: crash(D, b)
        if i % 4 == 3: put_fill(D, b, "small")
    elif n in ("Aメロ1", "Aメロ2"):
        vgroove(D, b, "vrock2", ghosts=0.3, seed=b)
        if i == 0: crash(D, b)
        if i % 8 == 7: put_fill(D, b, "small" if not last else "snare16")
    elif n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "halfdrive", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 1)
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        vgroove(D, b, "vrock", ghosts=0.25, seed=b)
        if i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
        if i % 8 == 7 and not last: put_fill(D, b, "tomdown" if i % 16 == 15 else "small")
        if last and n != "最後のサビ": halt(D, b, 1)
    elif n == "ギターソロ":
        vgroove(D, b, "vrock2", ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b)
        if last: put_fill(D, b, "snare16")
    elif n == "Cメロ":
        vgroove(D, b, "half", ghosts=0.2, seed=b)
        if i == 8: crash(D, b)
        if last: put_fill(D, b, "build")
    elif n == "落ちサビ" and i >= 4:
        D.set(b, "X.......X.......", "................", "x...x...x...x...")

# 止め4回: Bメロの終わり2回・サビ1とサビ2の終わり2回（1拍だけ叩いて全員休み）。レジを締める: 全員休み（ピアノとレジの鈴だけ）。
for name in ("Bメロ1", "Bメロ2", "サビ1", "サビ2"): SIL.add(S.sc(name)[-1], 1, 4)
SIL.add(S.sc("最後のサビ")[0] - 1, 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の04。ロック（高速ロック）。D の短調（サビは F）・192、最後のサビは +1（G♭）。"
          "アルバイト最後の夜、閉店後の店で、店長と仲間に言えなかった「ありがとう」。いきなりギターのリフで始まり、16分の弾みで語る Aメロ、止め4回、"
          "ギターソロ、レジの鈴とピアノだけの全員休み、最後は曲ごとテープが止まるように音が落ちて終わる。ギター2本・ピアノの合いの手・オルガン。自作")
finish(S, LY, V, 0, fx=[{"type": "tapestop", "at": "end", "dur": 2.2}],
       level={"verse": -0.25}, special={"落ちサビ": -0.6, "Cメロ": -0.4, "最後のサビ": 0.55})
