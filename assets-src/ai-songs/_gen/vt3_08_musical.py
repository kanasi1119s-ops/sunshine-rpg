# vt3 08「満員電車ミュージカル」Rush-Hour Musical（仮）— ブロードウェイ（ショーチューン）。168・4/4（2ビートのノリ）。
# C長調 → サビ2は D → 最後のサビは E♭（転調2回）。
# 第3弾（0時〜24時の街）の 7時。表は docs/sound/vt3-plan.md。
# 物語: 朝7時のぎゅうぎゅうの電車。ため息をついたら、となりの人がふいに口ずさんだのは、あの鼻歌（1時のラジオの節）。
#   前の人も後ろの人もつられて歌い出し、電車はミュージカルの舞台になる。スーツのおじさんはかばんを振って踊り、窓からは朝日のスポットライト。
#   車内アナウンスで、はっと現実にもどる。でも胸ははずんだまま。駅に着いてドアが開く ── フィナーレ。「またあした、同じ電車で」。
# 場面と強さ: 発車のブラス（強）→ 序曲（弦とブラス）→ Aメロ1（語るような早口・中）→ Bメロ1（半音ずつ上がる・ためる・止め）
#   → サビ1（全員のコーラス・強）→ タップ（止めのリズム・ブラスの合いの手）→ Aメロ2 → Bメロ2 → サビ2（D）
#   → アナウンス（ピアノだけ・語り・とても弱い）→ 間奏（車掌の笛＝節・弦がふくらむ）→ 最後のサビ（E♭・いちばん強い）→ フィナーレ
# 旋律の性格: Aメロは語りのような同じ音の8分（C4〜C5）、サビはオクターブの大きな跳躍（ド→高いド、レ→高いレ）。
# この曲だけの音: ショーチューンの2ビート（ウッドベースの1・3拍）と、タップダンスのような止め（スネアの細かいたたき）。
#   合いことばの節（3・5・6・5・2）は、間奏で車掌の笛（ピッコロ）が吹く。
from vt25_lib import *

S = Song("08", "musical", "満員電車ミュージカル（仮）", "Rush-Hour Musical", 168, 4, "C", "major", "ブロードウェイ（ショーチューン・ボカロ）")
S.kit = "naked-x"
S.flags = "--bass rubner " + S.flags + " --piano salamander --space hall --space-wet 0.16"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.45
S.keepers = {"Aメロ1": "ride", "Aメロ2": "ride", "サビ2": "open", "最後のサビ": "open"}
K = Key("C", "major")          # oct 4 で 1 = C4
K2 = Key("D", "major")
K3 = Key("Eb", "major")

C_CH = ["C", "Am7", "F", "C", "D7", "G7", "Em7", "A7sus4", "Dm7", "G7", "F", "C", "Am7", "Em7", "G7", "C"]
A_CH = ["C", "C", "F", "C", "Am7", "Dm7", "G7", "G7"]
B_CH = ["C", "D7", "Em", "E7", "Am", "G7", "G7sus4", "G7"]
OVER = ["C", "Am7", "Dm7", "G7"]

S.scene("発車のブラス", 4, "intro", ["C", "C", "F", "G7"])
S.scene("序曲", 12, "intro", OVER)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 24, "chorus", C_CH + C_CH[:8])
S.scene("タップ", 8, "break", OVER)
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", [B_CH[k] if k < 7 else "A7" for k in range(8)])          # 最後は D への入り口
S.scene("サビ2", 24, "chorus", [tr_chord(c, 2) for c in C_CH + C_CH[:8]])
S.scene("アナウンス", 8, "bridge", ["Dmaj7", "Bm7", "Gmaj7", "A7", "Dmaj7", "Bm7", "Em7", "Bb7"])   # 最後は E♭ への入り口
S.scene("間奏", 8, "solo", ["Eb", "Cm7", "Fm7", "Bb7", "Eb", "Cm7", "Fm7", "Bb7"])
S.scene("最後のサビ", 24, "chorus", [tr_chord(c, 3) for c in C_CH + C_CH[:8]])
S.scene("フィナーレ", 8, "outro", ["Ab", "Bb", "Gm7", "Cm7", "Ab", "Bb7", "Eb", "Eb"])

V = Voice(S, vol=0.2, delay=0.5, bright=0.0, patch="clarinet", low=False)
BR = [S.track(f"ブラス{i + 1}", "brass", patch="brassSection", volume=0.065, pan=0.3, reverb=0.3, sustain=0.6) for i in range(3)]
TP = S.track("トランペット（ファンファーレ）", "brass", patch="trumpet", volume=0.1, pan=0.15, reverb=0.3)
TB = S.track("トロンボーン", "brass", patch="trombone", volume=0.09, pan=-0.2, reverb=0.3)
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.05, pan=-0.55 + 0.55 * i, reverb=0.4, sustain=1.2) for i in range(3)]
STRL = S.track("ストリングス（駆け上がり）", "strings", patch="stringEnsemble", volume=0.07, pan=-0.3, reverb=0.4, sustain=0.6)
PL = S.track("ピアノ（左手）", "piano", volume=0.11, pan=-0.15, reverb=0.25, fx=[{"type": "eq", "low": -2, "mid": -1, "midHz": 400, "high": 2}])
PR = [S.track(f"ピアノ（右手{i + 1}）", "piano", volume=0.08, pan=-0.15, reverb=0.25, fx=[{"type": "eq", "low": -3, "mid": -1, "midHz": 400, "high": 3}]) for i in range(3)]
PIC = S.track("車掌の笛（ピッコロ）", "lead", patch="piccolo", volume=0.09, pan=0.2, reverb=0.4)
BASS = S.track("ウッドベース", "bass", **finger_bass_spec(vol=0.24))
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 5:0.5 5:0.5 5:0.5 6:0.5 5:0.5 3:0.5 1:0.5", "2:0.5 3:0.5 2:1 R:2",
      "R:0.5 5:0.5 5:0.5 5:0.5 6:0.5 5:0.5 1':0.5 7:0.5", "6:0.5 5:0.5 6:1 R:2",
      "R:0.5 6:0.5 6:0.5 6:0.5 1':0.5 6:0.5 5:0.5 3:0.5", "5:0.5 6:0.5 5:1 R:2",
      "R:0.5 4:0.5 4:0.5 4:0.5 3:0.5 2:0.5 3:0.5 4:0.5", "5:2 R:2"]
A1 = ("しちじのでんしゃのなか/ぎゅうぎゅうでうごけない/つりかわにぶらさがって/ためいきついたら/"
      "となりのひとがふいに/くちずさんだあのふし/まえのひともうしろも/うたがひろがるよ")
A2 = ("すーつのおじさんたち/かばんをふりおどるよ/がくせいもあかちゃんも/てびょうしならすよ/"
      "まどのけしきもまわる/すぽっとらいとみたいに/あさひがさしこむから/ぶたいのまんなか")
VB = ["R:1 3:1 3:1 3:1", "#4:1 #4:1 #4:1 R:1", "R:1 5:1 5:1 5:1", "#5:1 #5:1 #5:1 R:1",
      "R:1 6:1 6:1 6:1", "7:1 7:1 7:1 R:1", "R:0.5 1':0.5 1':0.5 1':0.5 1':0.5 1':0.5 2':1", "R:4"]
B1 = "ぎゅうぎゅうでも/こえはあがる/ゆれるたびに/はーもにーだ"
B2 = "えきのあいだ/あとすこしね/ゆれるでんしゃ/はくしゅかっさい"
VC = ["1:1 1':2 7:0.5 6:0.5", "5:2 3:1 R:1", "4:1 6:2 5:0.5 4:0.5", "3:3 R:1",
      "2:1 2':2 1':0.5 7:0.5", "6:2 5:1 R:1", "5:1 6:1 7:1 1':1", "2':3 R:1",
      "1:1 1':2 7:0.5 6:0.5", "5:2 3:1 R:1", "4:1 6:2 1':0.5 2':0.5", "1':3 R:1",
      "6:1 1':1 2':1 1':1", "7:2 5:1 R:1", "4:1 3:1 2:1 7,:1", "1:3 R:1"]
SCAT = "らーらららら/らららーら/らーらららら/らららーら"
C1 = "みんなうたえ/しちじはん/まんいんでも/すてーじだ/しらないひと/かたならべ/おなじふしで/ゆれていく/" + SCAT
C2 = "みんなうたえ/しちじはん/おりるえきを/わすれても/このうただけ/おわるまで/てをとりあって/まわるのさ/" + SCAT
C3 = ("みんなうたえ/えきにつく/どあがひらく/ふぃなーれだ/ばらばらでも/わすれない/あさのうたを/もっていこう/"
      "みんなうたえ/またあした/おなじでんしゃ/まっているよ")
ANN = ["5:0.5 5:0.5 5:0.5 5:0.5 3:1 R:1"] * 8
AN = "まもなくー/ちゅうおうー/おでぐちは/ひだりがわ/めがさめた/でもすこし/はずんでる/あのふしが"
LY = Lyrics(S)


def put(name, key, lines, text, o=4):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA + VA, A1)
put("Bメロ1", K, VB, B1)
put("サビ1", K, VC + VC[:8], C1)
put("Aメロ2", K, VA + VA, A2)
put("Bメロ2", K, VB, B2)
put("サビ2", K2, VC + VC[:8], C2)
put("アナウンス", K2, ANN, AN)
put("最後のサビ", K3, VC + VC[:8], C3)

# ================= 伴奏 =================
def brass(b, ch, pat, c=67):
    v = voice(ch, c, 3)
    for j in range(3): BR[j].bar(b, " ".join(t.replace("x", nm(v[j])) for t in pat.split()))


def strings(b, ch, c=70):
    v = voice(ch, c, 3)
    for j in range(3): STR[j].bar(b, f"{nm(v[j])}:4")


def piano2(b, ch):
    """2ビートのピアノ: 左手は1・3拍の低音、右手は2・4拍の和音"""
    r = low(ch, "C2"); v = voice(ch, 64, 3)
    PL.bar(b, f"{nm(r)}:1 R:1 {nm(r + 7)}:1 R:1")
    for j in range(3): PR[j].bar(b, f"R:1 {nm(v[j])}:0.75 R:1.25 {nm(v[j])}:0.75 R:0.25")


FAN = ["G4:0.5! C5:0.5 E5:0.5 G5:2.5", "G5:0.5 A5:0.5 G5:0.5 E5:0.5 C5:2", "A5:1 G5:1 F5:1 A5:1", "G5:3 R:1"]
MOTIF = ["R:2 G5:0.5 Bb5:0.5 C6:1", "Bb5:0.5 F5:1.5 R:2"]     # 合いことばの節（E♭で 3・5・6・5・2）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "発車のブラス":
        TP.bar(b, FAN[i]); brass(b, ch, "x:0.5! R:0.5 x:3" if i < 3 else "x:1 x:1 x:2")
        TB.bar(b, f"{nm(low(ch, 'C3'))}:4")
    elif n == "序曲":
        strings(b, ch); piano2(b, ch)
        if i % 4 == 3: STRL.bar(b, "R:2 " + " ".join(f"{nm(x)}:0.25" for x in (tones(ch, "C5", "C6") * 3)[:8]))
        if i >= 8: brass(b, ch, "x:1.5 x:0.5 R:2")
    elif n in ("Aメロ1", "Aメロ2"):
        piano2(b, ch)
        if n == "Aメロ2" or i >= 8: strings(b, ch, 66)
        if i % 8 == 7: brass(b, ch, "R:2 x:0.5 x:0.5 x:1")
    elif n in ("Bメロ1", "Bメロ2"):
        piano2(b, ch); strings(b, ch, 66 + i)
        if i < 7: TB.bar(b, f"{nm(low(ch, 'C3'))}:1 {nm(low(ch, 'C3'))}:1 {nm(low(ch, 'C3'))}:1 R:1")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        piano2(b, ch); strings(b, ch, 72)
        brass(b, ch, "R:1 x:0.75 R:1.25 x:0.75 R:0.25" if i % 2 == 0 else "R:2.5 x:0.5 x:1")
        if i % 8 == 7: STRL.bar(b, "R:2 " + " ".join(f"{nm(x)}:0.25" for x in (tones(ch, "C5", "C6") * 3)[:8]))
    elif n == "タップ":
        brass(b, ch, "x:0.5! R:3.5" if i % 2 == 0 else "R:3 x:0.5! R:0.5")
        PL.bar(b, f"{nm(low(ch, 'C2'))}:0.5 R:3.5")
    elif n == "アナウンス":
        v = voice(ch, 62, 3)
        for j in range(3): PR[j].bar(b, f"{nm(v[j])}:4")
        PL.bar(b, f"{nm(low(ch, 'C2'))}:4")
    elif n == "間奏":
        strings(b, ch, 66 + i // 2); piano2(b, ch)
        if i in (0, 1): PIC.bar(b, MOTIF[i])
        if i >= 4: brass(b, ch, "x:2 x:2")
        if i == 7: STRL.bar(b, "R:2 " + " ".join(f"{nm(x)}:0.25" for x in (tones(ch, "D5", "D6") * 3)[:8]))
    elif n == "フィナーレ":
        strings(b, ch, 72)
        if i < 6: piano2(b, ch); brass(b, ch, "x:1 R:1 x:1 R:1" if i < 4 else "x:4")
        elif i == 6: brass(b, ch, "x:4"); TP.bar(b, "Bb5:4"); PL.bar(b, f"{nm(low(ch, 'C2'))}:4")
        else: brass(b, ch, "x:0.5! R:3.5"); TP.bar(b, "Eb6:0.5! R:3.5"); PL.bar(b, f"{nm(low(ch, 'C2'))}:0.5 R:3.5")

# ================= ウッドベース（1・3拍の2ビート）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n in ("序曲", "Aメロ1", "Aメロ2", "サビ1", "サビ2", "最後のサビ", "間奏") or (n == "フィナーレ" and i < 6):
        BASS.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2" if i % 4 != 3 else bass_line(S, b, "walk", lo="E1"))
    elif n in ("Bメロ1", "Bメロ2") and i < 7: BASS.bar(b, bass_line(S, b, "walk", lo="E1"))
    elif n == "タップ": BASS.bar(b, f"{nm(r)}:0.5 R:3.5")
    elif n == "発車のブラス": BASS.bar(b, f"{nm(r)}:4")
    elif n == "フィナーレ": BASS.bar(b, f"{nm(r)}:4" if i == 6 else f"{nm(r)}:0.5 R:3.5")

cym_swell(CYM, S.sc("サビ1")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 4, "E4")

# ================= ドラム（2ビート・タップの止め）=================
TWO = ("X.......X.......", "....x.......x...", "x..xx..xx..xx..x")
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "発車のブラス":
        if i == 0: crash(D, b, "C2", 6)
        if i == 3: put_fill(D, b, "snare16")
    elif n in ("序曲", "Aメロ1", "Aメロ2"):
        vgroove(D, b, "beat8", ghosts=0.3, seed=b, k=TWO[0], s=TWO[1], h=TWO[2])
        if i == 0: crash(D, b)
        if i % 8 == 7 and not last: put_fill(D, b, "small")
    elif n in ("Bメロ1", "Bメロ2"):
        if i < 7: vgroove(D, b, "beat8", ghosts=0.2, seed=b, k="X...X...X...X...", s=TWO[1], h="x.x.x.x.x.x.x.x.")
        if i == 6: put_fill(D, b, "build")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        vgroove(D, b, "beat8", ghosts=0.3, seed=b, k="X.......X.......", s="....X.......X...", h="x.x.x.x.x.x.x.x.")
        if i % 8 == 0: crash(D, b, "C2", 6 if i == 0 else 4)
        if i % 8 == 7 and not last: put_fill(D, b, "small" if i < 16 else "tomdown")
        if last and n != "最後のサビ": put_fill(D, b, "snare16")
    elif n == "タップ":   # タップダンスのような細かいスネア（止めの間）
        D.set(b, "X...............", "X..x.x.xx.x..x.x" if i % 2 == 0 else "X.x..x.x.xx.x..x", "................")
        if i == 0: crash(D, b)
    elif n == "アナウンス":
        pass
    elif n == "間奏":
        if i >= 4: vgroove(D, b, "beat8", ghosts=0.2, seed=b, k=TWO[0], s=TWO[1], h=TWO[2])
        if last: put_fill(D, b, "lift")
    elif n == "フィナーレ":
        if i < 6: vgroove(D, b, "beat8", ghosts=0.2, seed=b, k="X.......X.......", s="....X.......X...", h="x.x.x.x.x.x.x.x.")
        if i == 0: crash(D, b, "C2", 6)
        if i == 5: put_fill(D, b, "snare16")
        if i == 6: D.set(b, "X...............", "X.X.X.X.XXXXXXXX", "................"); crash(D, b, "C2", 6)
        if i == 7: D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 8)

for name in ("Bメロ1", "Bメロ2"): SIL.add(S.sc(name)[-1], 0, 4)     # 1小節まるごと止め（サビの前の息）
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の08（7時）。ブロードウェイのショーチューン。C → D → E♭・168。"
          "朝7時の満員電車が、あの鼻歌をきっかけにミュージカルの舞台になる。ブラス・ストリングス・ピアノ・ウッドベースの2ビート、タップの止め。"
          "合いことばの節は間奏の車掌の笛（ピッコロ）。自作")
finish(S, LY, V, 0,
       level={"verse": -0.2}, special={"アナウンス": -0.7, "最後のサビ": 0.4, "フィナーレ": 0.2})
