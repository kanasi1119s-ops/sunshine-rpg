# vt25 16「おやすみ天文台」Goodnight Observatory（仮）— J-POP（ミドルバラード）。88・4/4。D♭長調 → 最後のサビは +1（D）。
# 物語: 遠く離れた町のきみと電話している。窓の外には丸い月。「そっちからも見える？」とたずねると、「見えるよ」の小さな声。
#   同じ月を見て、同じ時間に、別の部屋で笑いあう。電車で一日の道のり。ねむいね、ときみがあくび。電話のむこうで寝息が聞こえる。
#   「おやすみ」をいうよ。同じ月の下、離れていても、ここにいる。最後に、ふたりの声がひとつに重なる。電話が切れたあとの静けさ。
# 場面と強さ: アルペジオ（アコギ・弱）→ Aメロ1（語りかける）→ Bメロ1 → サビ1（中）→ 間奏 → Aメロ2 → Bメロ2 → サビ2
#   → ストリングスの間奏（バイオリンの旋律）→ Cメロ（電話のやりとり。左のわたしと右のきみが交互に）→ 最後のサビ（+1・いちばん強い。最後の8小節でふたりの声が重なる）
#   → 電話が切れたあと（ピアノだけ・1音）
# 旋律の性格: 語りかける中音域（B♭3〜A♭4）。サビは D♭4 → A♭4 → D♭5 と開いて、最後のサビで F5・F#5 まで高く。
# ほかの曲とちがう所（この曲だけの音）: 歌の版は、左のわたし（テト）と、右の「電話のむこうのきみ」（テトの弱い声）の2つの声。
#   Cメロで交互にやりとりし、最後のサビの終わりで、ふたりの声がひとつに重なる。BGM では、右のクラリネットが「きみ」。
from vt25_lib import *

S = Song("16", "oyasumi", "おやすみ天文台（仮）", "Goodnight Observatory", 88, 4, "Db", "major", "J-POP（ミドルバラード・ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --piano salamander --space hall --space-wet 0.18"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.45
K = Key("Db", "major")          # oct 4 で 1 = D♭4。歌うのは B♭3〜F5
KL = Key("D", "major")          # 最後のサビ（+1）

A_CH = ["Dbmaj7", "Ab/C", "Bbm7", "Gbmaj7", "Dbmaj7/F", "Gbmaj7", "Ebm7", "Ab7"]
B_CH = ["Gbmaj7", "Ab", "Dbmaj7", "Ebm7"]
C_CH = ["Gbmaj7", "Ab", "Fm7", "Bbm7", "Gbmaj7", "Ab", "Dbmaj7", "Dbmaj7"]
X_CH = ["Bbm7", "Ab", "Gbmaj7", "Ab", "Dbmaj7", "Bbm7", "Ebm7", "Ab7"]
LAST = [tr_chord(c, 1) for c in C_CH * 2]

S.scene("アルペジオ", 4, "intro", ["Dbmaj7", "Gbmaj7", "Dbmaj7", "Ab7"])
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 4, "pre", B_CH)
S.scene("サビ1", 8, "chorus", C_CH)
S.scene("間奏", 6, "break", ["Dbmaj7", "Gbmaj7", "Dbmaj7", "Gbmaj7", "Ebm7", "Ab7"])
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 4, "pre", B_CH)
S.scene("サビ2", 8, "chorus", C_CH)
S.scene("ストリングスの間奏", 8, "solo", ["Gbmaj7", "Ab", "Fm7", "Bbm7", "Gbmaj7", "Ab", "Bbm7", "Ab"])
S.scene("Cメロ", 8, "bridge", X_CH[:7] + ["A7"])                  # 最後の小節は D への入り口
S.scene("最後のサビ", 16, "chorus", LAST)
S.scene("電話が切れたあと", 8, "outro", ["Gmaj7", "A", "F#m7", "Bm7", "Gmaj7", "A", "Dmaj9", "Dmaj9"])

V = Voice(S, vol=0.21, delay=0.75, bright=-0.2, patch="surgeKeysLightEp", low=False)
YOU = S.track("電話のむこうのきみ（BGM・クラリネット）", "brass", patch="clarinet", volume=0.12, pan=0.6, reverb=0.3)
GTR = S.track("アコースティックギター（アルペジオ）", "guitar", amp="crystal", volume=0.085, pan=-0.35, reverb=0.3, chorus=0, sustain=1.0)
PL = S.track("ピアノ（左手）", "piano", volume=0.13, pan=-0.1, reverb=0.3, fx=[{"type": "eq", "low": -1, "mid": -2, "midHz": 400, "high": 2}])
PR = S.track("ピアノ（右手）", "piano", volume=0.13, pan=-0.1, reverb=0.3, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 3}])
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.065, pan=-0.35 + 0.35 * i, reverb=0.45, sustain=1.6) for i in range(3)]
VLN = S.track("バイオリン（間奏の旋律）", "fiddle", patch="violin", volume=0.1, pan=0.2, reverb=0.45, gainDb=1, bright=-0.3, attack=0.1, release=0.6)
GLK = S.track("グロッケン（星）", "glockenspiel", patch="glockenspiel", volume=0.05, pan=0.45, reverb=0.5)
BASS = S.track("ベース", "bass", **finger_bass_spec(vol=0.19))
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.05, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌（わたし） =================
VA = ["R:1 6,:0.5 1:0.5 3:1 2:1", "2:1.5 1:0.5 7,:1 R:1", "R:1 6,:0.5 1:0.5 3:1 5:1", "4:1.5 3:0.5 2:1 R:1",
      "R:1 3:0.5 5:0.5 1':1 7:1", "6:1.5 5:0.5 4:1 R:1", "R:1 4:0.5 5:0.5 6:1 5:1", "5:2 R:2"]
A1 = "とおくのきみと/でんわしてるの/まどのそとには/まるいつき/そっちからみえる/とたずねてみる/みえるよってこえ/ちいさくて"
A2 = "おなじつきみて/おなじじかんに/べつのへやでね/わらいあう"
VB = ["R:0.5 3:0.5 4:0.5 5:0.5 6:1 5:1", "4:1.5 3:0.5 2:1 R:1", "R:0.5 3:0.5 5:0.5 6:0.5 7:1 1':1", "6:2 5:1 R:1"]
B1 = "ねむいねってきみが/あくびをしたね"
B2 = "でんわのむこうで/ねいきがきこえ"
VC = ["R:0.5 1:0.5 5:1 6:0.5 5:0.5 1':1", "7:1.5 6:0.5 5:1 R:1", "R:0.5 1:0.5 5:1 6:0.5 5:0.5 2':1", "1':1.5 6:0.5 5:1 R:1",
      "R:0.5 3:0.5 6:1 1':0.5 6:0.5 3':1", "2':1.5 1':0.5 7:1 R:1", "R:0.5 5:0.5 6:0.5 1':0.5 2':1 1':1", "1':2 R:2"]
C1 = "おやすみをいうよ/おなじつきのした/はなれていてもね/ここにいるよ"
C2 = "おやすみをいうよ/ほしをかぞえてね/きみのそらにもね/かがやいてる"
CL = C1 + "/おやすみまたねって/なんどもいうよね/つきがきえるまで/そばにいるよ"
VX = ["R:1 5:1 6:1 5:1", "R:4", "R:1 3:1 5:1 6:1", "R:4", "R:1 5:1 6:1 1':1", "R:4", "R:1 6:1 5:1 3:1", "R:4"]
X1 = "ねむい/すきよ/あした/またね"
VY = ["R:4", "R:1 3:1 2:1 7,:1", "R:4", "R:1 2:1 3:1 5:1", "R:4", "R:1 3:1 2:1 1:1", "R:4", "R:1 5:1 6:1 5:1"]
Y1 = "まだよ/ぼくも/あえる/またね"
LY = Lyrics(S)
LY2 = Lyrics(S)        # 電話のむこうのきみ（右の声）


def put(name, key, lines, text, o=4):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)
    return bars, mel


put("Aメロ1", K, VA + VA, A1)
put("Bメロ1", K, VB, B1); put("Bメロ2", K, VB, B2)
put("サビ1", K, VC, C1); put("サビ2", K, VC, C2)
put("Cメロ", K, VX, X1)
LB, LM = put("最後のサビ", KL, VC + VC, CL)
if VOCAL: put("Aメロ2", K, VA, A2)
else:
    for b, l in zip(S.sc("Aメロ2"), VA): YOU.bar(b, K.mel(l, oct=4))
# 電話のむこうのきみ: Cメロで答え、最後のサビの後半8小節で、わたしと同じ旋律を歌う（ふたりの声が重なる）
YB = S.sc("Cメロ"); YM = [K.mel(x, oct=4) for x in VY]
if VOCAL:
    LY2.flow(YB, YM, Y1, "Cメロ（きみ）")
    LY2.flow(LB[8:], LM[8:], "/".join(CL.split("/")[4:]), "最後のサビ（きみ）")
else:
    for b, m in zip(YB, YM): YOU.bar(b, m)
    for b, m in zip(LB[8:], LM[8:]): YOU.bar(b, shift_oct(plain(m), -1))

# ================= 伴奏 =================
VLM = ["Bb5:2 Db6:1 F6:1", "Eb6:3 C6:1", "Ab5:2 C6:1 Eb6:1", "Db6:3 F5:1", "Gb5:1 Bb5:1 Db6:1 F6:1", "Eb6:1.5 Db6:0.5 C6:2", "Db6:1 Bb5:1 F5:1 Ab5:1", "Ab5:4"]
prev = None
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "C2"); t = tones(ch, "Ab3", "Ab5"); v4 = voice(ch, 65, 4, prev=prev); prev = v4; sv = voice(ch, 62, 3)
    if n == "電話が切れたあと":
        if i < 6:
            PL.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2"); PR.bar(b, " ".join(f"{nm(x)}:1" for x in v4))
        elif i == 6:
            PL.bar(b, f"{nm(r)}:8"); PR.bar(b, f"R:1 {nm(v4[3] + 12)}:7")
        continue
    GTR.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 4, 3, 1, 3, 2, 4)))
    if n in ("Aメロ1",) and i < 4: continue
    PL.bar(b, f"{nm(r)}:2 {nm(r + 7)}:1 {nm(r + 12)}:1")
    PR.bar(b, f"{nm(v4[0])}:1 {nm(v4[1])}:1 {nm(v4[2])}:1 {nm(v4[3])}:1" if n.startswith(("サビ", "最後")) else f"R:1 {nm(v4[1])}:1 {nm(v4[2])}:1 {nm(v4[3])}:1")
    if n.startswith(("サビ", "最後", "ストリングス")) or n in ("Bメロ2", "Cメロ") or (n == "Aメロ2" and i >= 4):
        for j in range(3): STR[j].bar(b, f"{nm(sv[j])}:4")
    if n == "ストリングスの間奏": VLN.bar(b, VLM[i])
    if n.startswith(("サビ", "最後")) and i % 4 == 3:
        GLK.bar(b, "R:2 " + " ".join(f"{nm(x)}:0.5" for x in tones(ch, "Db6", "Db7")[:4]))

for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n in ("アルペジオ",) or (n == "Aメロ1" and i < 4): continue
    if n == "電話が切れたあと":
        if i < 7: BASS.bar(b, bass_line(S, b, "long", lo="E1"))
        continue
    BASS.bar(b, bass_line(S, b, "half" if not n.startswith(("サビ", "最後")) else "walk", lo="E1"))
cym_swell(CYM, S.sc("最後のサビ")[0], 2, "E4")

# ================= ドラム（バラード: ブラシのような軽い刻み → サビで2拍4拍） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("アルペジオ", "電話が切れたあと") or (n == "Aメロ1" and i < 4): continue
    if n in ("Aメロ1", "Aメロ2", "Cメロ"):
        D.set(b, "X.......X.......", "....o.......o...", "x.x.x.x.x.x.x.x.")
    elif n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "half", ghosts=0.2, seed=b)
        if last: put_fill(D, b, "small")
    elif n.startswith(("サビ", "最後", "ストリングス")) or n == "間奏":
        vgroove(D, b, "beat8", ghosts=0.25, seed=b, k="X.......X.x.....")
        if i % 8 == 0: crash(D, b, "C2", 6)
        if i % 8 == 7 and not last: put_fill(D, b, "small")

SIL.add(S.sc("最後のサビ")[0] - 1, 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の16。J-POP（ミドルバラード）。D♭長調・88、最後のサビは +1（D）。"
          "遠距離の恋人と、同じ月を見ながら電話で「おやすみ」。アコギのアルペジオで始まり、語りかける Aメロ、ストリングスの間奏、"
          "Cメロは左のわたしと右のきみが交互に歌い、最後のサビの終わりでふたりの声がひとつに重なる。電話が切れたあとのピアノの1音で終わる。自作")
finish(S, LY, V, 0, level={"verse": -0.35}, special={"Cメロ": -0.3, "最後のサビ": 0.5}, vib={"chorus": 38})
# 歌の版: 右の声（電話のむこうのきみ）を足す。わたしの声は少し左に
if VOCAL:
    import json as _j, sys as _s
    path = _s.argv[1]; js = _j.load(open(path))
    js["vocals"][0]["pan"] = -0.3
    toks, t = [], 0.0
    for st, L, nn, kana in sorted(LY2.ev):
        if st > t + 1e-6: toks.append(f"R:{st - t:g}")
        m = midi(nn); toks.append(f"{FLAT[m % 12]}{m // 12 - 1}:{L:g}:{kana}"); t = st + L
    you = dict(js["vocals"][0]); you.update({"voice": "teto-soft", "notes": " ".join(toks), "pan": 0.6, "volume": 0.75, "reverb": 0.2,
                                             "blend": None, "dynamics": [[0, -0.3]]})
    you.pop("blend")
    js["vocals"].append(you)
    _j.dump(js, open(path, "w"), ensure_ascii=False)
    print("  電話のむこうのきみ（右の声）を足した:", len(LY2.ev), "音")
