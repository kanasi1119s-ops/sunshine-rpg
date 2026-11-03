# vt25 19「いいねの数だけ」As Many As the Likes（仮）— ヒップホップ（トラップポップ）。72（倍の 144 で感じる）・4/4。G# の短調（サビは平行調の B）→ 最後のサビは +1。
# 物語: 画面の「いいね」が増えない夜。指がスクロールをやめられなくて、疲れた。誰かのしあわせとくらべてばかり。数が価値みたいで、へんだね。
#   通知の音が鳴るたびに胸がきゅうっとなる。本当は知ってる、数じゃないって。夕方の電車、窓の外の空を、ずっと見てもいなかった。
#   スマホを置いたら、空がある。夕焼けを誰にも見せずに見つめる。いいねのかわりに「きれいね」って言う。
# 場面と強さ: 通知（通知の音の連打とパッド）→ Aメロ1（語る・中）→ Bメロ1 → サビ1（強）→ 間奏 → Aメロ2 → Bメロ2 → サビ2
#   → 通知が消える（とても弱い）→ Cメロ（夕焼け・ハーフのまま弱く）→ 最後のサビ（+1・いちばん強い）→ 夕焼け（通知はひとつもない）
# 旋律の性格: Aメロは語るような 16分（D#4 を3つ → B3 → G#4）。サビはのびやかに（F#4 → B4 → C#5、D#5 まで）。
# ほかの曲とちがう所（この曲だけの音）: 曲が進むほど、通知の音が減っていく（前奏は1小節に8つ → 最後はひとつもない）。
from vt25_lib import *

S = Song("19", "iine", "いいねの数だけ（仮）", "As Many As the Likes", 72, 4, "G#", "minor", "ヒップホップ（トラップポップ・ボカロ）")
S.kit = "electro"
S.flags = S.flags + " --piano salamander --space room --space-wet 0.18"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.drum_scale = 0.85
K = Key("G#", "minor")          # Aメロ・Bメロ（oct 3 で 1 = G#3。歌うのは A#3〜G#4）
KB = Key("B", "major")          # サビ・Cメロ（oct 3 で 1 = B3）
KL = Key("C", "major")          # 最後のサビ（+1。oct 4 で 1 = C4）

A_CH = ["G#m9", "Emaj7", "F#", "D#m7"]
B_CH = ["C#m7", "D#m7", "Emaj7", "F#"]
C_CH = ["Emaj7", "F#", "D#m7", "G#m7", "C#m7", "F#", "Bmaj7", "Bmaj7"]
X_CH = ["Emaj7", "F#", "D#m7", "G#m7", "Emaj7", "F#", "C#m7", "G7"]      # 最後の小節は C への入り口
LAST = [tr_chord(c, 1) for c in C_CH + C_CH[:4]]

S.scene("通知", 4, "intro", A_CH)
S.scene("Aメロ1", 8, "verse", A_CH)
S.scene("Bメロ1", 4, "pre", B_CH)
S.scene("サビ1", 8, "chorus", C_CH)
S.scene("間奏", 2, "break", ["G#m9", "Emaj7"])
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 4, "pre", B_CH)
S.scene("サビ2", 8, "chorus", C_CH)
S.scene("通知が消える", 4, "break", ["Emaj7", "F#", "D#m7", "G#m7"])
S.scene("Cメロ", 8, "bridge", X_CH)
S.scene("最後のサビ", 12, "chorus", LAST)
S.scene("夕焼け", 4, "outro", ["Fmaj7", "G", "Cmaj9", "Cmaj9"])

V = Voice(S, vol=0.21, delay=0.75, bright=0.6, patch="popLeadClear", low=True)
EP = [S.track(f"エレピ{i + 1}", "keys", patch="surgeKeysDxEp", volume=0.075, pan=-0.25 + 0.25 * i, reverb=0.3, sustain=0.9,
              fx=[{"type": "eq", "low": -2, "mid": 0, "midHz": 800, "high": 1}]) for i in range(3)]
PN = [S.track(f"ピアノ{i + 1}", "piano", volume=0.09, pan=-0.1, reverb=0.3, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 2.5}]) for i in range(3)]
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("surgePadVerbPad", vol=0.04, pan=-0.35 + 0.35 * i, duck=0.4, sustain=1.6)) for i in range(3)]
B808 = S.track("808", "sub808", volume=0.17, pan=0, sustain=1.0, fx=[{"type": "filter", "kind": "highpass", "freq": 30, "q": 0.7},
                                                                     {"type": "eq", "low": -1, "mid": 2.5, "midHz": 900, "high": 0}])
BELL = S.track("ベル（夕焼け）", "pad", patch="surgeFantasyBell", volume=0.05, pan=0.4, reverb=0.45, sustain=1.0)
PING = S.track("通知の音", "pad", patch="popBell", volume=0.045, pan=0.3, reverb=0.2, sustain=0.3,
               fx=[{"type": "filter", "kind": "highpass", "freq": 800, "q": 0.7}])
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.055, pan=-0.3 + 0.3 * i, reverb=0.45, sustain=1.5) for i in range(3)]
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.05, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 5:0.25 5:0.25 5:0.5 3:0.25 5:0.25 1':0.5 7:0.5 5:0.5 R:0.5", "R:0.5 6:0.25 6:0.25 6:0.5 5:0.25 6:0.25 1':0.5 7:0.5 6:1",
      "R:0.5 7:0.25 7:0.25 7:0.5 5:0.25 7:0.25 2':0.5 1':0.5 7:0.5 R:0.5", "5:1 4:0.5 3:0.5 2:1 R:1"]
A1 = "がめんのいいねが/ふえないよるだよ/ゆびがとまらない/つかれた/だれかのしあわせ/くらべてばかりで/かずがかちみたい/へんだね"
A2 = "つうちのおとがね/なるたびにはねる/むねがきゅうってなる/くるしい/ゆうがたのでんしゃ/まどのそとのそら/みてもいなかったね/そらいろ"
VB = ["R:0.5 1':0.5 1':0.5 7:0.5 6:1 5:1", "5:1.5 4:0.5 5:1 R:1", "R:0.5 3:0.5 5:0.5 1':0.5 2':1 1':1", "7:2 R:2"]
B1 = "ほんとうはしってる/かずじゃないって"
B2 = "ゆうひがまちをね/そめてゆくよ"
VC = ["R:0.5 5:0.5 1':1 7:0.5 1':0.5 2':1", "2':1.5 7:0.5 5:2", "R:0.5 5:0.5 7:1 6:0.5 7:0.5 3':1", "2':1.5 1':0.5 7:1 R:1",
      "R:0.5 3:0.5 6:1 5:0.5 6:0.5 1':1", "7:1.5 6:0.5 5:1 R:1", "R:0.5 3:0.5 5:0.5 6:0.5 7:1 1':1", "1':2 R:2"]
C1 = "いいねのかずだけ/わらえていたかな/すまほをおいたら/そらがあるね"
C2 = "いいねのかずより/きれいだとおもう/ゆうやけのいろを/みつめてるの"
CL = "いいねのかずだけ/わらわなくていい/だれにもみせない/このゆうひを/いいねのかわりに/きれいねっていうよ"
VX = ["R:1 3:1 5:1 6:1", "5:3 R:1", "R:1 5:1 7:1 2':1", "7:3 R:1", "R:1 6:1 5:1 3:1", "2:3 R:1", "R:1 3:1 5:1 6:1", "4:4"]
X1 = "ゆうやけ/きれいだ/だれかに/みせずに"
LY = Lyrics(S)


def put(name, key, lines, text, o=3):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA + VA, A1)
put("Bメロ1", K, VB, B1); put("Bメロ2", K, VB, B2)
put("サビ1", KB, VC, C1); put("サビ2", KB, VC, C2)
put("Cメロ", KB, VX, X1)
put("最後のサビ", KL, VC + VC[:4], CL, o=4)
if VOCAL: put("Aメロ2", K, VA + VA, A2)
else:
    for i, (b, l) in enumerate(zip(S.sc("Aメロ2"), VA + VA)):
        if i < 4: BELL.bar(b, K.mel(l, oct=4))
        else: V.bar(b, K.mel(l, oct=3))

# ================= 伴奏 =================
prev = None
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; v = voice(ch, 63, 3, prev=prev); prev = v; pv = voice(ch, 60, 3); v4 = voice(ch, 67, 3)
    if n == "夕焼け":
        if i < 2:
            for j in range(3): EP[j].bar(b, f"{nm(v[j])}:4"); PAD[j].bar(b, f"{nm(pv[j])}:4")
        elif i == 2:
            for j in range(3): EP[j].bar(b, f"{nm(v[j])}:8"); PAD[j].bar(b, f"{nm(pv[j])}:8")
            BELL.bar(b, " ".join(f"{nm(x)}:0.5" for x in tones(ch, "C6", "C7")[:4]) + " R:2")
        continue
    for j in range(3): PAD[j].bar(b, f"{nm(pv[j])}:4")
    if n == "通知が消える":
        for j in range(3): PN[j].bar(b, f"{nm(v4[j])}:4,")
        continue
    # エレピ: 8分の裏で弾む和音（トラップの上の、温かい和音）
    for j in range(3): EP[j].bar(b, f"{nm(v[j])}:1.5 {nm(v[j])}:1 R:0.5 {nm(v[j])}:1" if i % 2 == 0 else f"R:0.5 {nm(v[j])}:1 {nm(v[j])}:1.5 R:1")
    if n.startswith(("サビ", "最後")) or n in ("Bメロ1", "Bメロ2", "Cメロ"):
        for j in range(3): PN[j].bar(b, f"{nm(v4[j])}:2 {nm(v4[j])}:2")
    if n.startswith(("サビ2", "最後")) or n == "Cメロ":
        sv = voice(ch, 62, 3)
        for j in range(3): STR[j].bar(b, f"{nm(sv[j])}:4")
    if n.startswith(("サビ", "最後")) and i % 4 == 3:
        BELL.bar(b, "R:2 " + " ".join(f"{nm(x)}:0.5" for x in tones(ch, "C6", "C7")[:4]))

# ================= 808 =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "C1")
    if r < midi("D1"): r += 12
    if n == "通知" and i < 2: continue
    if n in ("通知が消える",):
        if i % 2 == 0: B808.bar(b, f"{nm(r)}:4")
        continue
    if n == "夕焼け":
        if i < 3: B808.bar(b, f"{nm(r)}:4" if i < 2 else f"{nm(r)}:8")
        continue
    B808.bar(b, f"{nm(r)}:1.5! {nm(r)}:0.5 {nm(r + 12)}:0.5 {nm(r)}:1.5" if i % 2 == 0 else f"{nm(r)}:2.5! {nm(r + 7)}:0.5 {nm(r)}:1")

# ================= 通知の音（曲が進むほど減る） =================
rnd = random.Random(1919)
COUNT = {"通知": 8, "Aメロ1": 4, "Bメロ1": 3, "サビ1": 3, "間奏": 3, "Aメロ2": 2, "Bメロ2": 1, "サビ2": 1, "通知が消える": 0, "Cメロ": 0, "最後のサビ": 0, "夕焼け": 0}
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    c = COUNT.get(n, 0)
    if n == "通知が消える" and i == 0: c = 1                            # 最後の1つ
    for j in range(c):
        st = rnd.choice([x * 0.25 for x in range(16)])
        PING.at(S.bar_beat(b) + st, f"{rnd.choice(['E6', 'G#6', 'B6'])}:0.25")
cym_swell(CYM, S.sc("最後のサビ")[0], 2, "E4")

# ================= ドラム（トラップ: ハットの細かい連打） =================
TRAPH = ["x.x.x.x.xxxxx.x.", "x.x.xxx.x.x.xxXx", "x.x.x.x.x.xxx.xx", "xxx.x.x.x.x.XxXx"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "通知":
        if i >= 2: vgroove(D, b, "trap", ghosts=0, seed=b, s="................", h=TRAPH[i % 4], vary=False)
    elif n in ("Aメロ1", "Aメロ2"):
        vgroove(D, b, "trap", ghosts=0.15, seed=b, h=TRAPH[i % 4], vary=False, k="X.......X.X....." if i % 2 == 0 else "X.....X...X..X..")
        if i == 0: crash(D, b, "C2", 3)
    elif n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "half", ghosts=0.2, seed=b)
        if last: put_fill(D, b, "snare16")
    elif n.startswith(("サビ", "最後")) or n == "間奏":
        vgroove(D, b, "trap", ghosts=0.2, seed=b, h=TRAPH[(i + 1) % 4], vary=False)
        if i % 4 == 0: crash(D, b, "C2", 4)
        if i % 4 == 3 and not last: put_fill(D, b, "small")
    elif n == "Cメロ":
        vgroove(D, b, "half", ghosts=0.15, seed=b, h="x...x...x...x...")
        if last: put_fill(D, b, "build")

SIL.add(S.sc("最後のサビ")[0] - 1, 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の19。ヒップホップ（トラップポップ）。G# の短調（サビは B）・72（倍の 144）、最後のサビは +1。"
          "SNS の数字に疲れた子が、スマホを置いて夕焼けを見る。通知の音の連打で始まり、語るような 16分の Aメロ、温かいエレピの和音とトラップのハット、"
          "曲が進むほど通知の音が減り、最後は通知がひとつもない夕焼けの和音で終わる。自作")
finish(S, LY, V, 0, level={"verse": -0.25}, special={"通知が消える": -0.6, "Cメロ": -0.4, "最後のサビ": 0.5})
