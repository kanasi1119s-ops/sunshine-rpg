# vt25 09「ヘッドライト・セレナーデ」Headlight Serenade（仮）— ロック（シティポップ寄りのバンド）。116・4/4。A♭長調 → 最後のサビは +1（A）。
# 物語: 免許をとった夜、はじめての夜道。助手席の母は、すぐにすやすや眠ってしまう。昔は、いつも逆だった。
#   ラジオの歌が小さく流れて、母の寝顔が小さく見える。いつの間にか、大切な人を乗せて運ぶのは、わたしになった。
#   海沿いの道、ヘッドライトの先に海。小さいころ聞いた母の子守歌を、今度はわたしがセレナーデにして返す。
#   トンネルの中は音がこもって、出口で一気に開ける。家の前でウインカーの音。
# 場面と強さ: エンジン（「ドン」と低い音とベース）→ イントロ（カッティングのギターとエレピ・サックスの節）→ Aメロ1（語る・弱）→ Bメロ1
#   → サビ1（海沿いの道・強）→ 間奏 → Aメロ2 → Bメロ2 → サビ2 → ギターソロ → トンネル（音がこもる・弱）→ 出口で開ける最後のサビ（+1）
#   → ウインカーの音で終わる
# 旋律の性格: ゆったり歌う、なめらかな上り下り（E♭4〜C5）。サビは A♭4 → C5 → E♭5 の三和音を上がって、なだらかに降りる。
# ほかの曲とちがう所（この曲だけの音）: トンネルの所だけ音がこもって、出口（最後のサビ）で一気に開ける。ウインカーの「カチ、カチ」で終わる。
from vt25_lib import *

S = Song("09", "headlight", "ヘッドライト・セレナーデ（仮）", "Headlight Serenade", 116, 4, "Ab", "major", "ロック（シティポップ寄りのバンド・ボカロ）")
S.kit = "naked-x"
S.flags = "--ref-tone glossy-jrock " + S.flags + " --piano salamander --space hall --space-wet 0.14"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.55
S.keepers = {"Aメロ1": "closed", "Aメロ2": "ride", "サビ2": "open", "最後のサビ": "wash"}
K = Key("Ab", "major")          # oct 3 で 1 = A♭3。歌うのは C4〜E♭5
KL = Key("A", "major")          # 最後のサビ（+1）

A_CH = ["Dbmaj7", "Cm7", "Bbm7", "Eb7", "Dbmaj7", "Cm7", "Fm7", "Bb7"]
B_CH = ["Bbm7", "Cm7", "Dbmaj7", "Eb", "Bbm7", "Cm7", "Dbmaj7", "Eb7sus4"]
C_CH = ["Dbmaj7", "Eb", "Cm7", "Fm7", "Bbm7", "Eb7", "Abmaj7", "Abmaj7", "Dbmaj7", "Eb", "Cm7", "Fm7", "Bbm7", "Eb7", "Dbmaj7", "Abmaj7"]
INTRO = ["Dbmaj7", "Cm7", "Bbm7", "Eb7"]
LAST = [tr_chord(c, 1) for c in C_CH]

S.scene("エンジン", 4, "intro", ["Ab", "Ab", "Dbmaj7", "Eb7"])
S.scene("イントロ", 8, "intro", INTRO * 2)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 4, "break", INTRO)
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("ギターソロ", 8, "solo", INTRO * 2)
S.scene("トンネル", 8, "bridge", ["Dbmaj7", "Cm7", "Bbm7", "Eb7", "Dbmaj7", "Cm7", "Bbm7", "E7"])   # 最後の小節は +1 への入り口（E7）
S.scene("最後のサビ", 16, "chorus", LAST)
S.scene("ウインカー", 6, "outro", ["Dmaj7", "C#m7", "Bm7", "E7", "Amaj9", "Amaj9"])

V = Voice(S, vol=0.21, delay=0.75, bright=0.0, patch="calliope", low=False)
EP = [S.track(f"エレピ{i + 1}", "keys", patch="surgeKeysDxEp", volume=0.075, pan=-0.25 + 0.25 * i, reverb=0.28, sustain=0.9,
              fx=[{"type": "eq", "low": -2, "mid": 0, "midHz": 800, "high": 1}]) for i in range(3)]
CUT = S.track("カッティングのギター", "guitar", amp="jpopClean", volume=0.085, pan=0.4, reverb=0.2, chorus=0, sustain=0.35)
GTR = S.track("ギター（アルペジオ）", "guitar", amp="crystal", volume=0.075, pan=-0.4, reverb=0.3, chorus=0, sustain=0.9)
LGS = S.track("リードギター（ソロ）", "leadGuitar", **lead_gtr_spec(0.13, 0.05))
SAX = S.track("サックス（イントロの節）", "brass", patch="altoSax", volume=0.11, pan=0.1, reverb=0.3)
BASS = S.track("ベース（スラップしない指弾き）", "bass", **finger_bass_spec(vol=0.22))
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.055, pan=-0.3 + 0.3 * i, reverb=0.4, sustain=1.4) for i in range(3)]
ENG = S.track("エンジン（低い一撃）", "impactHit", volume=0.09, pan=0, reverb=0.3)
TICK = S.track("ウインカー（カホンの縁）", "cajon", volume=0.07, pan=0.3, reverb=0.08)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:1 5:0.5 6:0.5 1':1 6:1", "5:1.5 3:0.5 5:1 R:1", "R:1 4:0.5 5:0.5 6:1 1':1", "7:1.5 6:0.5 5:1 R:1",
      "R:1 5:0.5 6:0.5 1':1 2':1", "3':1.5 2':0.5 7:1 R:1", "R:1 1':0.5 7:0.5 6:1 5:1", "6:2 R:2"]
A1 = "めんきょとったよる/ははをのせてね/あたらしいみち/はしりだす/となりのははは/すやすやねむる/むかしはいつも/ぎゃくだったね"
A2 = "らじおのうたが/ちいさくながれ/ははのねがおが/ちいさくて"
VB = ["R:0.5 2':0.5 2':0.5 3':0.5 4':1 3':1", "2':1.5 1':0.5 7:1 R:1", "R:0.5 1':0.5 1':0.5 2':0.5 3':1 4':1", "5':1.5 4':0.5 3':1 R:1",
      "R:0.5 2':0.5 2':0.5 3':0.5 4':1 5':1", "3':1.5 2':0.5 7:1 R:1", "R:0.5 1':0.5 2':0.5 3':0.5 4':1 5':1", "6':2 R:2"]
B1 = "ちいさないびきが/ちょっぴりおかしくて/わたしはなぜだか/なきそうだよ"
B2 = "いつからだろうね/わたしがはこぶの/たいせつなひとを/のせてるんだ"
VC = ["R:0.5 1':0.5 3':0.5 5':0.5 5':1 4':1", "3':1.5 2':0.5 3':1 R:1", "R:0.5 7:0.5 2':0.5 3':0.5 3':1 2':1", "1':2 R:2",
      "R:0.5 6:0.5 1':0.5 3':0.5 3':1 2':1", "2':1.5 1':0.5 7:1 R:1", "R:0.5 5:0.5 6:0.5 1':0.5 3':1 2':1", "1':2 R:2"]
VC2 = VC[:6] + ["R:0.5 5:0.5 6:0.5 1':0.5 4':1 3':1", "1':3 R:1"]
C1 = "へっどらいとのさき/うみがみえる/ねむるははにそっと/くちずさむの/ははのこもりうた/いまわたしが/せれなーでにして/かえすからね"
C2 = "へっどらいとのさき/ほしがゆれる/かーぶのむこうへ/あしたがある/ゆっくりでいいから/だいじょうぶよ/ねむっていていいよ/いえまでずっと"
CL = "へっどらいとのさき/あさがくるよ/ねむるははにそっと/くちずさむの/ははのこもりうた/いまわたしが/せれなーでにして/かえすからね"
LY = Lyrics(S)


def put(name, key, lines, text, o=3):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA + VA, A1)
put("Bメロ1", K, VB, B1); put("Bメロ2", K, VB, B2)
put("サビ1", K, VC + VC2, C1); put("サビ2", K, VC + VC2, C2)
put("最後のサビ", KL, VC + VC2, CL)
if VOCAL: put("Aメロ2", K, VA, A2)
else:
    for i, (b, l) in enumerate(zip(S.sc("Aメロ2"), VA)): SAX.bar(b, K.mel(l, oct=4))

# ================= エレピ・ギター・サックス =================
SAXH = ["R:0.5 Eb5:0.5 F5:0.5 Ab5:0.5 C6:1 Bb5:1", "Ab5:1.5 F5:0.5 Eb5:1 R:1", "R:0.5 Db5:0.5 Eb5:0.5 F5:0.5 Ab5:1 Bb5:1", "G5:3 R:1"]
prev = None
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; v = voice(ch, 63, 3, prev=prev); prev = v; t = tones(ch, "Ab3", "Ab5")
    if n == "エンジン":
        continue
    if n == "ウインカー" and i >= 4:
        if i == 4:
            for j in range(3): EP[j].bar(b, f"{nm(v[j])}:8")
            GTR.bar(b, " ".join(f"{nm(x)}:0.5" for x in t[:4]) + f" {nm(t[4 % len(t)])}:6")
        continue
    # エレピ: シティポップの、裏で押す和音
    for j in range(3): EP[j].bar(b, f"{nm(v[j])}:1.5 {nm(v[j])}:1 R:0.5 {nm(v[j])}:1" if i % 2 == 0 else f"R:0.5 {nm(v[j])}:1 {nm(v[j])}:1.5 R:1")
    if n not in ("Aメロ1", "トンネル") or (n == "Aメロ1" and i >= 8):
        CUT.bar(b, " ".join(f"{nm(v[q % 3] + 12)}:0.25" if q % 4 in (1, 3) else "R:0.25" for q in range(16)))
    if n in ("Aメロ1", "Aメロ2", "トンネル", "間奏"):
        GTR.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 1, 3, 2, 4, 3, 1)))
    if n in ("イントロ", "間奏"): SAX.bar(b, SAXH[i % 4])
    if n in ("サビ1", "サビ2", "最後のサビ", "Bメロ2"):
        sv = voice(ch, 64, 3)
        for j in range(3): STR[j].bar(b, f"{nm(sv[j])}:4")
# 2026-11-04 v2: 人間「トライデントの音の割には高すぎて音が強く感じる」→ リードギターを1オクターブ下げる（中音域で太く鳴らす）
SOLO = ["R:0.5 Eb4:0.5 Ab4:0.5 C5:0.5 Eb5:1^ C5:1", "Bb4:1 Ab4:0.5 F4:0.5 Eb4:2~", "R:0.5 F4:0.5 Ab4:0.5 Bb4:0.5 Db5:1 C5:1", "Bb4:0.5 Ab4:0.5 G4:0.5 F4:0.5 G4:2~",
        "Ab4:0.25 Bb4:0.25 C5:0.5 Eb5:0.5 F5:1^ Eb5:0.5 C5:1", "Bb4:2~ Ab4:2", "Db5:0.5 C5:0.5 Bb4:0.5 Ab4:0.5 G4:1 Bb4:1", "Eb5:3~ R:1"]
for i, b in enumerate(S.sc("ギターソロ")): LGS.bar(b, SOLO[i])

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n == "エンジン":
        if i >= 2: BASS.bar(b, f"{nm(r)}:0.5 R:0.5 {nm(r)}:0.25 {nm(r)}:0.25 {nm(r + 12)}:0.5 {nm(r + 10)}:0.5 {nm(r + 7)}:0.5 {nm(r + 5)}:0.5 {nm(r + 3)}:0.5")
        continue
    if n == "トンネル": BASS.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2"); continue
    if n == "ウインカー":
        if i < 5: BASS.bar(b, f"{nm(r)}:4")
        continue
    # シティポップのベース: 16分の弾み＋オクターブ
    BASS.bar(b, f"{nm(r)}:0.75 {nm(r)}:0.25 R:0.5 {nm(r + 12)}:0.5 {nm(r)}:0.5 R:0.25 {nm(r + 7)}:0.25 {nm(r + 10)}:0.5 {nm(r + 12)}:0.5"
             if n not in ("Aメロ1",) or i >= 8 else f"{nm(r)}:1.5 {nm(r + 7)}:0.5 {nm(r + 12)}:1 R:1")

# ================= エンジン・ウインカー =================
ENG.bar(S.sc("エンジン")[0], "E1:4"); ENG.bar(S.sc("最後のサビ")[0], "R:0 E1:2")
for i, b in enumerate(S.sc("ウインカー")): TICK.bar(b, "G3:0.5! R:0.5 F3:0.5, R:0.5 G3:0.5! R:0.5 F3:0.5, R:0.5")
cym_swell(CYM, S.sc("サビ1")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 4, "E4")

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "エンジン":
        if i == 3: put_fill(D, b, "small")
    elif n in ("イントロ", "間奏"):
        vgroove(D, b, "disco", ghosts=0.25, seed=b, k="X.....X...X.....", h="x.xxx.xxx.xxx.xx", vary=False)
        if i == 0: crash(D, b)
    elif n in ("Aメロ1", "Aメロ2"):
        vgroove(D, b, "beat8", ghosts=0.3, seed=b, k="X.....X...X.....")
        if i == 0: crash(D, b, "C2", 3)
        if i % 8 == 7: put_fill(D, b, "small" if not last else "snare16")
    elif n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "halfdrive", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        vgroove(D, b, "disco", ghosts=0.25, seed=b, k="X.....X...X..X..", vary=True)
        if i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
        if i % 8 == 7 and not last: put_fill(D, b, "tomdown" if i == 15 else "small")
    elif n == "ギターソロ":
        vgroove(D, b, "beat8", ghosts=0.35, seed=b)
        if i == 0: crash(D, b)
    elif n == "トンネル":
        D.set(b, "X.......X.......", "................", "x...x...x...x..." if i >= 4 else "................")
        if last: put_fill(D, b, "build")
    elif n == "ウインカー":
        if i < 4: vgroove(D, b, "beat8", ghosts=0.2, seed=b)

# トンネル: 中の音はこもる（ローパス 700Hz）。出口（最後のサビ）で一気に開ける
muffle(S, [t for t in S.tracks if t not in (V.main, V.low, ENG, CYM)], S.sc("トンネル"), 700)
SIL.add(S.sc("最後のサビ")[0] - 1, 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の09。ロック（シティポップ寄りのバンド）。A♭長調・116、最後のサビは +1（A）。"
          "免許をとって初めての夜のドライブ、助手席で眠る母を家まで運ぶ。エンジンの低い音とベースで始まり、エレピとカッティングのギター、サックスの節、"
          "海沿いの道のサビ、ギターソロ、音がこもるトンネルから出口で一気に開ける最後のサビ、ウインカーの音で終わる。自作")
finish(S, LY, V, 0, level={"verse": -0.35}, special={"最後のサビ": 0.5})
