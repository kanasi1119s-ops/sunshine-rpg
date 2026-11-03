# vt25 03「深夜2時のメロンソーダ」Melon Soda at 2 A.M.（仮）— エレクトロニカ（ローファイハウス）。122・4/4。F の短調（サビは平行調の A♭）。転調なし。
# 物語: 眠れない夜の2時。課題のしめきりは明日。通話をつないだまま、友だちとそれぞれ自分の作業をしている。何も話さない。
#   聞こえるのは、むこうのキーボードの音と、コップのメロンソーダの泡。ときどき「まだ起きてる？」「うん、起きてる」。それだけで、あたたかい。
#   一度、通話が切れたかと思う静けさ。でも「ぽこん」とつながって、くすっと笑う声。窓の外が白くなるころ、「おはようだね」。
# 場面と強さ: 泡（コップの泡とエレピ・とても弱い）→ Aメロ1（ささやく・弱）→ サビ1（「まだ起きてる？」・中）→ 切れた？（2小節、泡だけ）
#   → 間奏（エレピ）→ Aメロ2 → サビ2（中）→ ソロ（エレピのソロ・フィルターが開く）→ Cメロ（しずけさ・とても弱い）
#   → サビ3（いちばん強い。でも控えめ）→ 朝（窓が白くなる）→ 通話の「ぽこん」1つ
# 旋律の性格: ささやくような低めの旋律（C4〜A♭4）。サビで少しだけ上がる（A♭4〜E♭5）。山は大きくせず、ずっと同じ部屋の中の声。
# ほかの曲とちがう所（この曲だけの音）: 通話の入り・切れの小さな音（「ぽこん」）が、句の終わりの合いの手になる。コップの泡（高い所の小さな粒）。
#   2小節、バンドが全部消えて泡だけになる（通話が切れたかと思う間）。
from vt25_lib import *

S = Song("03", "melonsoda", "深夜2時のメロンソーダ（仮）", "Melon Soda at 2 A.M.", 122, 4, "F", "minor", "エレクトロニカ（ローファイハウス・ボカロ）")
S.kit = "electro"
S.flags = S.flags + " --piano salamander --space room --space-wet 0.2"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.drum_scale = 0.82
S.open_hat_vol = 0.5
K = Key("F", "minor")          # oct 3 で 1 = F3

A_CH = ["Fm9", "Bbm9", "Eb9", "Abmaj7", "Dbmaj7", "Gm7b5", "C7", "Fm9"]
C_CH = ["Dbmaj7", "Eb7sus4", "Cm7", "Fm9", "Dbmaj7", "Eb7sus4", "Abmaj7", "Fm9"]
C_CH2 = ["Dbmaj7", "Eb7sus4", "Cm7", "Fm9", "Dbmaj7", "Eb7sus4", "Bbm9", "Abmaj7"]
X_CH = ["Dbmaj7", "Eb", "Fm9", "Dbmaj7", "Bbm9", "Eb7sus4", "C7sus4", "C7"]

S.scene("泡", 8, "intro", ["Fm9", "Dbmaj7", "Fm9", "Dbmaj7", "Fm9", "Bbm9", "Eb9", "Abmaj7"])
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("サビ1", 16, "chorus", C_CH + C_CH2)
S.scene("切れた？", 2, "break", ["Fm9", "Fm9"])
S.scene("間奏", 8, "break", ["Fm9", "Bbm9", "Eb9", "Abmaj7", "Dbmaj7", "Gm7b5", "C7", "C7"])
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("サビ2", 16, "chorus", C_CH + C_CH2)
S.scene("ソロ", 8, "solo", A_CH)
S.scene("Cメロ", 8, "bridge", X_CH)
S.scene("サビ3", 16, "chorus", C_CH + C_CH2)
S.scene("朝", 10, "outro", ["Dbmaj7", "Eb7sus4", "Cm7", "Fm9", "Dbmaj7", "Eb7sus4", "Abmaj7", "Abmaj7", "Abmaj7", "Abmaj7"])

V = Voice(S, vol=0.2, delay=0.75, bright=-0.5, patch="chiff", low=False)
EP = [S.track(f"エレピ{i + 1}", "keys", patch="surgeKeysDxEp", volume=0.075, pan=-0.2 + 0.2 * i, reverb=0.3, sustain=0.9,
              fx=[{"type": "filter", "kind": "lowpass", "freq": 3800, "q": 0.6}, {"type": "eq", "low": -2, "mid": 0, "midHz": 800, "high": -1}]) for i in range(4)]
EPS = S.track("エレピ（ソロ）", "keys", patch="surgeKeysLightEp", volume=0.11, pan=0.15, reverb=0.32, sustain=0.8,
              fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.15, "feedback": 0.3}])
BASS = S.track("ベース", "bass", **finger_bass_spec(vol=0.21))
PAD = [S.track(f"やわらかいパッド{i + 1}", "pad", **pad_spec("surgePadVerbPad", vol=0.04, pan=-0.35 + 0.35 * i, duck=0.35, sustain=1.6)) for i in range(3)]
FIZZ = S.track("コップの泡", "pad", patch="surgeChordXyloChill", volume=0.04, pan=0.45, sustain=0.5, reverb=0.4,
               fx=[{"type": "filter", "kind": "highpass", "freq": 1500, "q": 0.7}])
POKON = S.track("通話の「ぽこん」", "pad", patch="popBell", volume=0.06, pan=-0.35, reverb=0.25, sustain=0.4,
                fx=[{"type": "filter", "kind": "highpass", "freq": 700, "q": 0.7}])
KEYS = S.track("むこうのキーボード（カホンの縁）", "cajon", volume=0.05, pan=0.55, reverb=0.15)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.05, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌（F の短調の度数。oct 3 で 1 = F3。歌うのは C4〜E♭5） =================
VA = ["R:1 5:0.5 1':0.5 1':1 7:0.5 1':0.5", "2':1 1':1 5:1 R:1", "R:1 6:0.5 1':0.5 1':1 7:0.5 6:0.5", "5:2 R:2",
      "R:1 3':0.5 2':0.5 1':1 2':0.5 3':0.5", "4':1 2':1 1':1 R:1", "R:1 7:0.5 1':0.5 2':1 1':0.5 7:0.5", "1':2 R:2"]
A1 = "ねむれないよるの/いまにじだよ/こっぷのなかのあわ/めろんそーだ/つうわのむこうで/かたかたかた/なにもはなさない/それでいいの"
A2 = "かだいのしめきり/あしたなのに/すすまないぺーじ/ためいきだね/まいくのむこうで/くすっとわらう/ひとりじゃないよと/きこえたきが"
VC = ["R:0.5 3':0.5 3':0.5 5':1 3':0.5 4':1", "3':2 R:2", "R:0.5 5':0.5 5':0.5 7':1 6':0.5 5':1", "4':2 R:2",
      "R:0.5 3':0.5 3':0.5 5':1 3':0.5 4':1", "5':1 4':1 3':1 R:1", "R:0.5 2':0.5 3':0.5 4':1 3':0.5 2':1", "1':2 R:2"]
VC2 = VC[:6] + ["R:0.5 2':0.5 3':0.5 5':1 4':0.5 3':1", "3':2 R:2"]
C1 = "まだおきてる/うんおきてる/それだけのことば/あたたかいよ/まだおきてる/もうすこしね/よあけがくるまで/このままでね"
C2 = "まだおきてる/ねむくなったね/まぶたのうらにね/きみのこえが/まだおきてる/おやすみはね/まだいわないでね/もうすこしね"
C3 = "まだおきてる/そらがしろい/そーだのみどりが/すけていくよ/まだおきてる/ありがとうね/きみがいたからね/おはようだね"
VX = ["R:1 5':1 4':1 3':1", "2':3 R:1", "R:1 3':1 4':1 5':1", "7':3 R:1", "R:1 5':1 6':1 5':1", "4':2 3':2", "R:1 2':1 4':1 5':0.5 4':0.5", "5':4"]
X1 = "しずけさ/やさしい/ふたりのね/いきのおと"
LY = Lyrics(S)


def put(name, lines, text, o=3):
    bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", VA + VA, A1)
put("サビ1", VC + VC2, C1); put("サビ2", VC + VC2, C2); put("サビ3", VC + VC2, C3)
put("Cメロ", VX, X1)
if VOCAL: put("Aメロ2", VA + VA, A2)
else:
    for i, (b, l) in enumerate(zip(S.sc("Aメロ2"), VA + VA)):
        if i < 8: EPS.bar(b, K.mel(l, oct=4))
        else: V.bar(b, K.mel(l, oct=3))

# ================= エレピ（ローファイの和音。左右に分けた4声） =================
SOLO = ["R:0.5 C5:0.5 F5:0.5 Ab5:0.5 G5:1 F5:0.5 Eb5:0.5", "Db5:1.5 C5:0.5 Bb4:1 R:1", "R:0.5 Bb4:0.5 Eb5:0.5 G5:0.5 F5:1 Eb5:0.5 Db5:0.5", "C5:3 R:1",
        "R:0.5 Ab5:0.5 G5:0.5 F5:0.5 Ab5:1 C6:1", "Bb5:1.5 Ab5:0.5 G5:1 R:1", "R:0.5 E5:0.5 G5:0.5 Bb5:0.5 Db6:1 C6:0.5 Bb5:0.5", "Ab5:1 G5:1 F5:2"]
prev = None
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    v = voice(ch, 64, 4, prev=prev); prev = v
    if n == "泡" and i < 2: continue
    if n == "切れた？": continue
    if n == "朝" and i >= 8:
        if i == 8:
            for j in range(4): EP[j].bar(b, f"{nm(v[j])}:8")
        continue
    # ローファイハウスのコード打ち: 2拍目の裏と4拍目の裏で押す（Aメロは控えめに1回）
    if n in ("Aメロ1", "Aメロ2", "Cメロ", "泡"):
        for j in range(4): EP[j].bar(b, f"R:1.5 {nm(v[j])}:2.5" if i % 2 == 0 else f"{nm(v[j])}:1.5 R:0.5 {nm(v[j])}:2")
    else:
        for j in range(4): EP[j].bar(b, f"R:0.5 {nm(v[j])}:1 R:1 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5")
    if n == "ソロ": EPS.bar(b, SOLO[i])
    if n in ("サビ1", "サビ2", "サビ3", "ソロ", "朝"):
        pv = voice(ch, 60, 3)
        for j in range(3): PAD[j].bar(b, f"{nm(pv[j])}:4")

# ================= ベース（ディープハウスの、裏で歌うベース） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n == "泡":
        if i >= 4: BASS.bar(b, f"{nm(r)}:3 R:1")
    elif n in ("Aメロ1", "Aメロ2", "Cメロ"):
        BASS.bar(b, f"{nm(r)}:1.5 R:0.5 {nm(r + 12)}:0.5 R:0.5 {nm(r + 7)}:1" if i % 2 == 0 else f"{nm(r)}:2.5 {nm(r + 10)}:0.5 {nm(r + 12)}:0.5 R:0.5")
    elif n in ("サビ1", "サビ2", "サビ3", "ソロ", "間奏"):
        BASS.bar(b, f"R:0.5 {nm(r)}:0.5 R:0.5 {nm(r)}:0.5 R:0.5 {nm(r + 12)}:0.5 {nm(r + 10)}:0.5 {nm(r + 7)}:0.5")
    elif n == "朝" and i < 9:
        BASS.bar(b, f"{nm(r)}:4" if i >= 6 else f"R:0.5 {nm(r)}:0.5 R:0.5 {nm(r)}:0.5 R:0.5 {nm(r + 12)}:0.5 R:1")

# ================= 通話の「ぽこん」（句の終わりの合いの手）・むこうのキーボード =================
for name in ("Aメロ1", "Aメロ2"):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3: POKON.bar(b, "R:3 G5:0.25 C6:0.75" if i % 8 == 3 else "R:3 C6:0.25 G5:0.75")
        if i % 2 == 1: KEYS.bar(b, "R:2 E3:0.25, F3:0.25, R:0.25 E3:0.25, F3:0.25 R:0.5 E3:0.25,")
for name in ("サビ1", "サビ2", "サビ3"):
    for i, b in enumerate(S.sc(name)):
        if i in (1, 3, 9): POKON.bar(b, "R:2.5 G5:0.25 C6:0.75 R:0.5")

# ================= ドラム（ローファイハウス: 4つ打ちのキック、裏のハット、軽いクラップ） =================
LOFI_H = "..x...x...x...xx"
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "泡":
        if i >= 4: D.set(b, "X...X...X...X...", "................", LOFI_H if i >= 6 else "................")
        if i == 7: put_fill(D, b, "small")
    elif n in ("Aメロ1", "Aメロ2"):
        vgroove(D, b, "four", ghosts=0.15, seed=b, s="....X.......X...", h=LOFI_H if i % 4 != 3 else "..x...x...x.O.x.", vary=False)
        if i == 0: crash(D, b, "C2", 3)
        if i == 15: put_fill(D, b, "small")
    elif n in ("サビ1", "サビ2", "サビ3"):
        vgroove(D, b, "four", ghosts=0.2, seed=b, h="x.x.x.x.x.x.x.xO" if i % 2 else "x.O.x.O.x.O.x.O.", vary=False)
        if i % 8 == 0: crash(D, b, "C2", 4)
        if i % 8 == 7 and not last: put_fill(D, b, "small")
    elif n == "間奏":
        D.set(b, "X...X...X...X...", "................", LOFI_H)
    elif n == "ソロ":
        vgroove(D, b, "twostep", ghosts=0.25, seed=b)
        if i == 7: put_fill(D, b, "lift")
    elif n == "Cメロ":
        D.set(b, "X.......X.......", "................", "x...x...x...x..." if i >= 4 else "................")
        if last: put_fill(D, b, "build")
    elif n == "朝":
        if i < 6: vgroove(D, b, "four", ghosts=0.1, seed=b, s="....X.......X...", h=LOFI_H, vary=False)
        elif i < 8: D.set(b, "X...X...X...X...", "................", "................")
cym_swell(CYM, S.sc("サビ3")[0], 2, "C4")

# 通話が切れたかと思う2小節: 全員が消える（泡だけが残る）
SIL.add(S.sc("切れた？")[0], 0, 4); SIL.add(S.sc("切れた？")[1], 0, 4)
SIL.apply()

# コップの泡（高い所の小さな粒。静けさの所でも鳴る。無音の処理のあとに置く）
rnd = random.Random(303)
for b in list(S.sc("泡")) + S.sc("切れた？") + S.sc("朝")[6:]:
    n, i, L, k = S.scene_of(b)
    t = tones(S.chords[b], "C6", "C7")
    cnt = 3 if n != "切れた？" else 5
    for j in range(cnt):
        FIZZ.at(S.bar_beat(b) + rnd.choice([x * 0.25 for x in range(16)]), f"{nm(rnd.choice(t))}:0.25")
b1 = S.sc("切れた？")[1]; POKON.bar(b1, "R:3 G5:0.25 C6:0.75")          # つながった「ぽこん」
POKON.bar(S.sc("朝")[-1], "R:2 C6:0.25 G5:0.75 R:1")                    # 終わり: 通話を切る「ぽこん」1つ

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の03。エレクトロニカ（ローファイハウス）。F の短調（サビは A♭）・122、転調なし。"
          "眠れない夜の2時、通話をつないだまま何も話さずに作業する友だち。コップの泡とエレピで始まり、ささやくような低めの旋律、"
          "「まだ起きてる？」のサビ、2小節だけ泡だけになる静けさ（通話が切れたかと思う間）、エレピのソロ、通話を切る「ぽこん」1つで終わる。自作")
finish(S, LY, V, 0, level={"verse": -0.5, "chorus": 0.1}, special={"Cメロ": -0.6, "サビ3": 0.25},
       settings={"breathy": 0.16}, vocal_level=0.55)
