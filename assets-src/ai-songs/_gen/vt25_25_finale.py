# vt25 25「フィナーレは君の声で」Finale in Your Voice（仮）— ロック（ストリングスとピアノのアンセム）。93・4/4（サビは倍の速さに感じる 8ビート）。
#   A 長調 → 最後のサビは +1（B♭）。第2弾のしめくくりの曲。
# 物語: これが最後の歌。25曲の旅も、もうすぐ終わる。笑った日も泣いた日も、どの歌の中にも君の笑顔がいた。
#   だから最後、お願い。幕が下りる前に。フィナーレは君の声で歌おう。小さな声でも届くから。まちがえたっていい。
#   歌が終わっても心に残るよ。またあえる日まで、ありがとう。
# 場面と強さ: アカペラ（テトの声だけ）→ イントロ（バンドが一気に入る）→ Aメロ1 → Bメロ1 → サビ1 → 間奏 → Aメロ2 → Bメロ2 → サビ2
#   → シンガロング（「オーオー」と、みんなで歌う・手拍子）→ Cメロ（静か）→ 落ちサビ（もう一度アカペラ・手拍子だけ）
#   → 最後のサビ（+1・声が何人にも重なる・いちばん強い）→ 終わり（全員でのばす和音）
# 旋律の性格: サビは「6 → 1' → 2' → 4' → 3'」と上がっていく、口ずさめる形。シンガロングは4つの音の「オーオー」。
# ほかの曲とちがう所: 声だけで始まる（アカペラ）。落ちサビももう一度アカペラ。シンガロングと最後のサビで、歌が何人もの声に重なる（ダブラー）。
from vt25_lib import *

S = Song("25", "finale", "フィナーレは君の声で（仮）", "Finale in Your Voice", 93, 4, "A", "major", "ロック（アンセム・ストリングス・ボカロ）")
S.kit = "jpop"
# v3: 人間「04と同じギターの音トライデントに変えようか」→ 歪みギターの音を TRiDENT の音（参考の音 glossy-jrock）に
S.flags = "--ref-tone glossy-jrock " + S.flags + " --piano salamander --space hall --space-wet 0.18"
S.no_depth = True              # アカペラの所に深いパッドを足さない
K = Key("A", "major")           # oct 3 で 1 = A3（歌うのは A3〜E5）
KL = Key("Bb", "major")         # 最後のサビ（oct 3）

A_CH = ["A", "E/G#", "F#m", "D", "A", "E", "D", "E"]
B_CH = ["Bm7", "C#m7", "D", "E"]
C_CH = ["D", "E", "C#m7", "F#m", "D", "E", "A", "A"]
SG_CH = ["D", "A", "E", "F#m", "D", "A", "E", "E"]
X_CH = ["F#m", "D", "A", "E", "F#m", "D", "Bm7", "E"]
up = lambda cs: [tr_chord(c, 1) for c in cs]

S.scene("アカペラ", 4, "intro", C_CH[:4])
S.scene("イントロ", 4, "intro", ["D", "E", "A", "A"])
S.scene("Aメロ1", 8, "verse", A_CH)
S.scene("Bメロ1", 4, "pre", B_CH)
S.scene("サビ1", 8, "chorus", C_CH)
S.scene("間奏", 4, "break", ["D", "E", "A", "A"])
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 4, "pre", B_CH)
S.scene("サビ2", 8, "chorus", C_CH)
S.scene("シンガロング", 8, "chorus", SG_CH)
S.scene("Cメロ", 8, "bridge", X_CH)
S.scene("落ちサビ", 4, "bridge", C_CH[:4])
S.scene("最後のサビ", 16, "chorus", up(C_CH) * 2)
S.scene("終わり", 8, "outro", ["Eb", "F", "Bb", "Bb", "Eb", "F", "Bb", "Bb"])

V = Voice(S, vol=0.21, delay=0.75, bright=0.6, patch="popLeadClear", low=True)
GT = [S.track(f"ギター1（{['根音', '5度', 'オクターブ'][i]}）", "distGuitar", **rock_gtr_spec(0.06, -0.45 + 0.45 * i)) for i in range(3)]
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.22))
PNFX = [{"type": "eq", "low": -3, "mid": -1.5, "midHz": 400, "high": 3}]
PN = [S.track(f"ピアノ{i + 1}", "piano", volume=0.1, pan=-0.12, reverb=0.25, fx=PNFX) for i in range(4)]
PNL = S.track("ピアノ（左手）", "piano", volume=0.11, pan=-0.12, reverb=0.25, fx=PNFX)
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.06, pan=-0.4 + 0.4 * i, reverb=0.45, sustain=1.4) for i in range(3)]
VLN = S.track("ストリングス（高い旋律）", "strings", patch="stringEnsemble", volume=0.06, pan=0.3, reverb=0.45, sustain=1.2)
GLK = S.track("ベル", "glockenspiel", patch="glockenspiel", volume=0.05, pan=0.4, reverb=0.5)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)
CLAP = season(S, 0, "手拍子", beats=0.5, vol=0.08, pan=-0.1); CLAP.ev = []

# ================= 歌 =================
VA = ["R:0.5 3:0.5 3:0.5 3:0.5 2:0.5 3:0.5 5:1", "5:1.5 3:0.5 2:1 R:1", "R:0.5 3:0.5 3:0.5 3:0.5 2:0.5 3:0.5 6:1", "6:1.5 5:0.5 3:1 R:1",
      "R:0.5 3:0.5 3:0.5 3:0.5 2:0.5 3:0.5 5:1", "5:1.5 6:0.5 5:1 R:1", "R:0.5 4:0.5 4:0.5 4:0.5 3:0.5 4:0.5 6:1", "5:2 R:2"]
A1 = "これがさいごのうた/ここまでありがとう/にじゅうごきょくのたび/もうすぐおわる"
A2 = "わらったひもないたひ/どのうたのなかにも/きみのえがおがいた/きづいていたよ"
VB = ["R:1 4:0.5 4:0.5 4:0.5 5:0.5 6:1", "5:2 R:2", "R:1 6:0.5 6:0.5 6:0.5 7:0.5 1':1", "2':2 R:2"]
B1 = "だからさいご/おねがいだよ"
B2 = "まくがおりる/そのまえにね"
VC = ["R:0.5 6:0.5 1':0.5 2':0.5 4':1 3':1", "2':1.5 1':0.5 7:1 R:1", "R:0.5 5:0.5 7:0.5 1':0.5 3':1 2':1", "3':1.5 2':0.5 1':1 R:1",
      "R:0.5 6:0.5 1':0.5 2':0.5 4':1 5':1", "5':1.5 4':0.5 2':1 R:1", "R:0.5 3:0.5 5:0.5 1':0.5 3':1 2':1", "1':2 R:2"]
C0 = "ふぃなーれはきみの/こえでうたおうよ"
C1 = "ふぃなーれはきみの/こえでうたおうよ/ちいさなこえでも/とどくからね"
C2 = "ふぃなーれはきみの/こえでかざろうよ/まちがえたっていい/わらいながら"
CL = C1 + "/ふぃなーれはきみと/ふたりでうたうの/またあえるひまで/ありがとうね"
CO = "ちいさなこえでも/きこえているから"
VS = ["6:1 6:0.5 5:0.5 6:2", "R:4", "7:1 7:0.5 6:0.5 5:2", "R:4", "6:1 6:0.5 5:0.5 6:2", "R:4", "2':1 2':0.5 1':0.5 7:2", "R:4"]
SG = "おーおお/おーおお/おーおお/らーらら"
VX = ["R:1 3:1 5:1 6:1", "5:3 R:1", "R:1 3:1 2:1 1:1", "2:3 R:1", "R:1 3:1 5:1 6:1", "1':3 R:1", "R:1 1':1 7:1 6:1", "5:3 R:1"]
X1 = "うたがね/おわっても/こころに/のこるよ"
LY = Lyrics(S)


def put(name, key, lines, text, o=3):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel):
        if m != "R:4": V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("アカペラ", K, VC[:4], C0)
put("Aメロ1", K, VA, A1)
put("Bメロ1", K, VB, B1); put("Bメロ2", K, VB, B2)
put("サビ1", K, VC, C1); put("サビ2", K, VC, C2)
put("シンガロング", K, VS, SG)
put("Cメロ", K, VX, X1)
put("落ちサビ", K, VC[:4], CO)
put("最後のサビ", KL, VC + VC, CL)
if VOCAL: put("Aメロ2", K, VA, A2)
else:                                            # 歌なしの版: 2番の Aメロはピアノが歌う（1オクターブ上）
    for b, l in zip(S.sc("Aメロ2"), VA): GLK.bar(b, K.mel(l, oct=4))

# ================= 伴奏 =================
prev = None
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    full = S.chords[b]; ch = full.split("/")[0]
    r = midi(full.split("/")[1] + "1") if "/" in full else low(ch, "E1")
    if r < midi("E1"): r += 12
    v = voice(ch, 64, 4, prev=prev); prev = v; gr = low(ch, "E2")
    if n in ("アカペラ", "落ちサビ"): continue           # 声だけ
    if n == "終わり" and i >= 6:
        if i == 6:
            for j in range(3): GT[j].bar(b, f"{nm(gr + [0, 7, 12][j])}:8")
            for j in range(4): PN[j].bar(b, f"{nm(v[j])}:8")
            sv = voice(ch, 67, 3)
            for j in range(3): STR[j].bar(b, f"{nm(sv[j])}:8")
            BASS.bar(b, f"{nm(r)}:8"); PNL.bar(b, f"{nm(r + 12)}:8")
        continue
    chorus = n.startswith(("サビ", "最後")) or n in ("シンガロング", "イントロ", "間奏") or n == "終わり"
    if n == "Cメロ":
        for j in range(4): PN[j].bar(b, f"{nm(v[j])}:2 {nm(v[j])}:2" if i >= 4 else f"{nm(v[j])}:4")
        PNL.bar(b, f"{nm(r + 12)}:4")
        sv = voice(ch, 62, 3)
        for j in range(3): STR[j].bar(b, f"{nm(sv[j])}:4")
        if i >= 4: BASS.bar(b, f"{nm(r)}:4")
        continue
    # ピアノ: 8分で和音を刻むアンセム（サビ）、Aメロは2分音符でのばす
    if chorus or n.startswith("Bメロ"):
        # v2 で試した「サビのピアノを4分に」は点数が変わらなかった（歌 7.43）ので、v1 の8分に戻した（完成に選んだのは v1）
        for j in range(4): PN[j].bar(b, " ".join(f"{nm(v[j])}:0.5" for _ in range(8)) if chorus else f"{nm(v[j])}:1 {nm(v[j])}:1 {nm(v[j])}:1 {nm(v[j])}:1")
        PNL.bar(b, f"{nm(r + 12)}:1 {nm(r + 24)}:1 {nm(r + 12)}:1 {nm(r + 24)}:1")
    else:
        for j in range(4): PN[j].bar(b, f"{nm(v[j])}:2 {nm(v[j])}:2")
        PNL.bar(b, f"{nm(r + 12)}:2 {nm(r + 19)}:2")
    # ギター: サビとイントロは8分のパワーコード、Aメロは小節の頭だけ、Bメロは4分
    if chorus:
        for j in range(3): GT[j].bar(b, " ".join(f"{nm(gr + [0, 7, 12][j])}:0.5" for _ in range(8)))
    elif n.startswith("Bメロ"):
        for j in range(3): GT[j].bar(b, " ".join(f"{nm(gr + [0, 7, 12][j])}:1" for _ in range(4)))
    elif n == "Aメロ2":
        for j in range(3): GT[j].bar(b, f"{nm(gr + [0, 7, 12][j])}:1.5 R:2.5")
    # ベース
    if chorus: BASS.bar(b, " ".join(f"{nm(r)}:0.5" for _ in range(8)))
    elif n.startswith("Bメロ"): BASS.bar(b, f"{nm(r)}:1 {nm(r)}:1 {nm(r)}:1 {nm(r + 7)}:1")
    else: BASS.bar(b, f"{nm(r)}:2 {nm(r)}:1.5 {nm(r + 7)}:0.5")
    # ストリングス: サビ2から、のばす和音と高い旋律
    if n in ("サビ2", "シンガロング", "最後のサビ", "終わり") or (n == "サビ1" and i >= 4) or n.startswith("Bメロ"):
        sv = voice(ch, 66, 3)
        for j in range(3): STR[j].bar(b, f"{nm(sv[j])}:4")
    if n in ("最後のサビ", "シンガロング") or n == "終わり":
        t = tones(ch, "A5", "A6")
        VLN.bar(b, f"{nm(t[0])}:2 {nm(t[1 % len(t)])}:1 {nm(t[2 % len(t)])}:1" if i % 2 == 0 else f"{nm(t[-1])}:4")
    if chorus and i % 4 == 3 and n != "イントロ":
        GLK.bar(b, "R:2 " + " ".join(f"{nm(x)}:0.5" for x in tones(ch, "C6", "C7")[:4]))
# BGM の版: アカペラの所は、ベルが旋律をそっと重ねる
if not VOCAL:
    for b, l in zip(S.sc("アカペラ") + S.sc("落ちサビ"), VC[:4] * 2): GLK.bar(b, K.mel(l, oct=4))
# 手拍子（シンガロング・落ちサビ・最後のサビの後半: 2・4拍）
for b in S.sc("シンガロング") + S.sc("落ちサビ") + S.sc("最後のサビ")[8:]:
    for st in (1, 3): CLAP.at(S.bar_beat(b) + st, "B4:0.5")
cym_swell(CYM, S.sc("イントロ")[0], 1, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 1, "E4")

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("アカペラ", "落ちサビ"):
        if n == "アカペラ" and last: put_fill(D, b, "build")
        continue
    if n == "終わり":
        if i < 6: vgroove(D, b, "beat8", ghosts=0.2, seed=b, h="x.xxx.xxx.xxx.xx")
        elif i == 6: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 8)
        continue
    chorus = n.startswith(("サビ", "最後")) or n in ("イントロ", "間奏")
    if n == "シンガロング":
        vgroove(D, b, "four", ghosts=0, seed=b, s="....X.......X...", h="x.x.x.x.x.x.x.x.")
    elif n.startswith("Aメロ"):
        vgroove(D, b, "half", ghosts=0.15, seed=b, s="....X.......X...", h="x.x.x.x.x.x.x.x.")
    elif n.startswith("Bメロ"):
        vgroove(D, b, "beat8", ghosts=0.2, seed=b, k="X...X...X...X...")
    elif n == "Cメロ":
        if i >= 4: vgroove(D, b, "half", ghosts=0, seed=b, h="x...x...x...x...")
    else:
        vgroove(D, b, "beat8", ghosts=0.25, seed=b, k="X.X...X.X.X...X." if chorus else None, h="x.xxx.xxx.xxx.xx" if chorus else None)
    if i == 0 or (chorus and i % 4 == 0): crash(D, b, "C2", 4)
    if last and n not in ("Cメロ",): put_fill(D, b, "snare16")
    elif chorus and i % 4 == 3: put_fill(D, b, "small")
    if n == "Cメロ" and last: halt(D, b, 1)

SIL.add(S.sc("落ちサビ")[-1], 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の25（しめくくり）。ロック（ストリングスとピアノのアンセム）。A 長調・93（サビは 8ビートで倍に感じる）、"
          "最後のサビは +1（B♭）。「これが最後の歌」── 聴いてくれた君に、最後は君の声で歌ってほしいとお願いする。"
          "テトの声だけのアカペラで始まり、バンドが一気に入る。オーオーのシンガロングと手拍子、もう一度アカペラの落ちサビ、"
          "最後のサビは声が何人にも重なる。自作")
finish(S, LY, V, 0, double=[("シンガロング", 0.6), ("最後のサビ", 0.7)],
       level={"verse": -0.3}, special={"アカペラ": 0.0, "Cメロ": -0.45, "落ちサビ": -0.2, "最後のサビ": 0.55})
