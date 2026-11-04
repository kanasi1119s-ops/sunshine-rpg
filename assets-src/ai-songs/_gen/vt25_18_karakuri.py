# vt25 18「からくり時計のワルツ」Clockwork Waltz（仮）— ロック（変拍子のピアノロック）。168・4/4。B の短調（サビは D 長調）。転調なし。
#   （作曲ソフトは曲の途中で拍子を変えられないので、表の「Aメロ 7/8・最後に 3/4」は、4/4 の上で
#     ・Aメロ: 歯車の刻みを 3.5拍（＝8分7つ）でくり返し、4拍の小節とずれて「つまずく」
#     ・人形が踊る: 伴奏とドラムを 3拍ずつのまとまり（ワルツ）にして、小節線をまたいで回す
#   という形で書いた）
# 物語: 祖父の時計屋が、今日でおしまい。ちくたく、針の音がひびく店の中。鳩時計も、今日は黙ったまま。ねじのすり傷に、祖父の指のあと。
#   窓のそばのからくり人形は、毎日、正午に踊りだした。祖父はそれを見て笑っていた。明日からここは空っぽになる。時計の音たちは、どこへ行くの。
#   最後に、ねじを巻く。正午の鐘。からくりの扉が開いて、人形が最後のワルツを踊る。祖父と踊っているのが見えた。時計が止まっても、胸の中では動いている。
# 場面と強さ: 時計の刻み（チェンバロの歯車とカホンの縁の刻み・弱）→ Aメロ1（歯車がつまずく・語る）→ Bメロ1 → サビ1（強）→ ピアノソロ
#   → Aメロ2 → Bメロ2 → サビ2 → Cメロ（ねじまき・弱）→ 止まった時計（刻みがゆっくりになって止まる・とても弱い）
#   → 人形が踊る（ワルツの大サビ・いちばん強い）→ 最後のサビ → 時計の鐘1つ
# 旋律の性格: Aメロは 3＋3＋2 のつまずくリズム（付点8分・付点8分・8分）で B3〜B4。サビは D 長調で F#5 まで。
# ほかの曲とちがう所（この曲だけの音）: 時計の歯車（チェンバロの8分の刻みが 3.5拍でくり返す）が、拍の刻みになる。最後の大サビはワルツ。
from vt25_lib import *

S = Song("18", "karakuri", "からくり時計のワルツ（仮）", "Clockwork Waltz", 168, 4, "B", "minor", "ロック（変拍子のピアノロック・ボカロ）")
S.kit = "naked-x"
S.flags = "--ref-tone glossy-jrock " + S.flags + " --piano salamander --space hall --space-wet 0.14"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.55
K = Key("B", "minor")           # Aメロ（oct 3 で 1 = B3）
KD = Key("D", "major")          # Bメロ・サビ・Cメロ（oct 4 で 1 = D4）

A_CH = ["Bm", "G", "D", "A", "Bm", "G", "Em", "F#"]
B_CH = ["Em", "F#m", "G", "A", "Em", "F#m", "G", "F#7"]
C_CH = ["G", "A", "F#m", "Bm", "G", "A", "D", "D", "G", "A", "F#m", "Bm", "Em", "F#", "Bm", "Bm"]
X_CH = ["Em", "F#m", "G", "A", "Em", "F#m", "G", "F#7"]

S.scene("時計の刻み", 10, "intro", ["Bm", "Bm", "G", "G", "D", "D", "A", "A", "Em", "F#"])
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("ピアノソロ", 16, "solo", A_CH * 2)
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("Cメロ", 8, "bridge", X_CH)
S.scene("止まった時計", 8, "break", ["Bm", "Bm", "G", "G", "Em", "Em", "F#", "F#"])
S.scene("人形が踊る", 24, "chorus", C_CH + C_CH[:8])
S.scene("最後のサビ", 16, "chorus", C_CH)
S.scene("時計の鐘", 8, "outro", ["G", "A", "F#m", "Bm", "G", "A", "Bm", "Bm"])

V = Voice(S, vol=0.21, delay=0.75, bright=0.3, patch="surgeKeysBellPiano", low=False)
GEAR = S.track("時計の歯車（チェンバロ）", "harpsichord", volume=0.075, pan=0.3, reverb=0.2, sustain=0.4)
TICK = S.track("時計の刻み（カホンの縁）", "cajon", volume=0.06, pan=-0.3, reverb=0.15)
PL = S.track("ピアノ（左手）", "piano", volume=0.14, pan=-0.12, reverb=0.22, fx=[{"type": "eq", "low": -1, "mid": -2, "midHz": 400, "high": 2}])
PR = S.track("ピアノ（右手）", "piano", volume=0.14, pan=-0.12, reverb=0.22, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 3.5}])
PRS = S.track("ピアノ（ソロ）", "piano", volume=0.17, pan=-0.12, reverb=0.22, fx=[{"type": "eq", "low": -3, "mid": -1, "midHz": 400, "high": 3}])
GT = [S.track(f"ギター（{['根音', '5度'][i]}）", "distGuitar", **rock_gtr_spec(0.06, -0.4 + 0.8 * i)) for i in range(2)]
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.06, pan=-0.35 + 0.35 * i, reverb=0.4, sustain=1.4) for i in range(3)]
BOX = S.track("オルゴール（グロッケン）", "glockenspiel", patch="glockenspiel", volume=0.055, pan=0.4, reverb=0.45)
BELL = S.track("時計の鐘", "bell", volume=0.09, pan=0, reverb=0.5)
BASS = S.track("ベース", "bass", **rock_bass_spec(0.22))
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)
B = S.beats

# ================= 歌 =================
VA = ["1:0.75 2:0.75 3:0.5 5:0.75 4:0.75 3:0.5", "1:1.5 R:2.5", "3:0.75 4:0.75 5:0.5 1':0.75 7:0.75 6:0.5", "5:1.5 R:2.5",
      "1:0.75 2:0.75 3:0.5 5:0.75 6:0.75 5:0.5", "3:1.5 R:2.5", "4:0.75 3:0.75 2:0.5 4:0.75 3:0.75 2:0.5", "#7,:1.5 R:2.5"]
A1 = "そふのとけいや/きょうでおしまい/はりのおとがね/ひびいているの/はとどけいもね/なかないままで/そふのゆびあと/ねじのすりきず"
A2 = "からくりのこが/まどのそばでね/まいにちしょうご/おどりだしたの/そふはわらってた/まいにちのこと/そのすがたまで/おぼえているよ"
VB = ["R:0.5 2:0.5 2:0.5 3:0.5 4:1 2:1", "3:1.5 2:0.5 7,:1 R:1", "R:0.5 4:0.5 4:0.5 5:0.5 6:1 4:1", "3:1.5 2:0.5 3:1 R:1",
      "R:0.5 2:0.5 2:0.5 3:0.5 5:1 4:1", "3:1.5 2:0.5 7,:1 R:1", "R:0.5 4:0.5 5:0.5 6:0.5 1':1 7:1", "#5:2 R:2"]
B1 = "あしたからここは/からっぽになるんだ/とけいのおとたち/どこへいくの"
B2 = "しょうごのかねがね/なるそのときだけ/からくりのとびら/ひらくんだよ"
VC = ["R:0.5 5:0.5 6:0.5 1':0.5 3':1 2':1", "2':1.5 7:0.5 5:1 R:1", "R:0.5 5:0.5 6:0.5 1':0.5 2':1 3':1", "1':1.5 7:0.5 6:1 R:1",
      "R:0.5 3:0.5 5:0.5 1':0.5 2':1 1':1", "7:1.5 6:0.5 5:1 R:1", "R:0.5 5:0.5 6:0.5 7:0.5 1':1 2':1", "1':2 R:2",
      "R:0.5 5:0.5 6:0.5 1':0.5 3':1 2':1", "2':1.5 7:0.5 5:1 R:1", "R:0.5 5:0.5 6:0.5 1':0.5 2':1 3':1", "1':1.5 7:0.5 6:1 R:1",
      "R:0.5 3:0.5 5:0.5 1':0.5 2':1 1':1", "7:1.5 6:0.5 #5:1 R:1", "R:0.5 5:0.5 6:0.5 7:0.5 1':1 6:1", "6:2 R:2"]
C1 = "からくりのわるつ/さいごにおどってよ/ねじをまいたなら/うごきだすよ/からくりのわるつ/そふのてのあとが/はぐるまのなかに/いきているよ"
C2 = "からくりのわるつ/くるくるまわってね/おもいだすことを/ありがとうね/からくりのわるつ/みせはしまうけど/わたしがもっていく/つれていくよ"
CW = "からくりのわるつ/いちにさんまわる/にんぎょうがおじぎ/してくれたね/からくりのわるつ/さいごのいっきょくを/そふとおどってるの/みえたんだよ"
CL = "からくりのわるつ/とけいはとまっても/わたしのむねでは/うごいてるよ/からくりのわるつ/ちくたくきこえる/さよならじゃなくて/またあしたね"
VX = ["R:1 2:1 3:1 4:1", "3:3 R:1", "R:1 4:1 5:1 6:1", "5:3 R:1", "R:1 2:1 3:1 5:1", "3:3 R:1", "R:1 4:1 6:1 1':1", "#5:3 R:1"]
X1 = "ねじまき/とまるよ/しずかだ/でもまだ"
LY = Lyrics(S)


def put(name, key, lines, text, o):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA + VA, A1, 3)
put("Bメロ1", KD, VB, B1, 4); put("Bメロ2", KD, VB, B2, 4)
put("サビ1", KD, VC, C1, 4); put("サビ2", KD, VC, C2, 4)
put("Cメロ", KD, VX, X1, 4)
put("人形が踊る", KD, VC, CW, 4)
put("最後のサビ", KD, VC, CL, 4)
if VOCAL: put("Aメロ2", K, VA + VA, A2, 3)
else:
    for i, (b, l) in enumerate(zip(S.sc("Aメロ2"), VA + VA)):
        if i < 8: BOX.bar(b, K.mel(l, oct=5))
        else: V.bar(b, K.mel(l, oct=3))

# ================= 時計の歯車（3.5拍＝8分7つでくり返す。小節とずれてつまずく） =================
def gear(bars, vel=""):
    b0, b1 = bars[0], bars[-1] + 1
    t = b0 * B; k = 0
    while t < b1 * B - 1e-6:
        bar = int(t // B); ts = tones(S.chords[bar], "B4", "B5")
        pat = (0, 2, 1, 3, 2, 1, 4)                       # 8分7つ: 歯車の上下
        m = ts[pat[k % 7] % len(ts)]
        GEAR.at(round(t, 3), f"{nm(m)}:0.5{'!' if k % 7 == 0 else vel}")
        t += 0.5; k += 1


gear(S.sc("時計の刻み")[2:]); gear(S.sc("Aメロ1")); gear(S.sc("Aメロ2")); gear(S.sc("ピアノソロ")[:8], ",")
# 時計の刻み（カホンの縁: 4分。止まった時計では、だんだん間があいて止まる）
for name in ("時計の刻み", "Aメロ1", "Aメロ2", "Cメロ"):
    for b in S.sc(name): TICK.bar(b, "G3:1! F3:1, G3:1 F3:1,")
STOP = ["G3:1! F3:1, G3:1 F3:1,", "G3:1! F3:1, G3:1 F3:1,", "G3:1! R:0.25 F3:1, R:0.25 G3:1 R:0.5", "G3:1.5! R:0.5 F3:1.5 R:0.5",
        "G3:2! R:2", "F3:2 R:2", "R:2 G3:2", "R:4"]
for i, b in enumerate(S.sc("止まった時計")): TICK.bar(b, STOP[i])

# ================= ピアノ（ロックのピアノ。人形が踊るはワルツ: 3拍のまとまりで小節線をまたぐ） =================
prev = None
SOLO = ["B5:0.5 D6:0.5 F#6:0.5 D6:0.5 B5:0.5 F#5:0.5 D5:1", "G5:0.5 B5:0.5 D6:0.5 B5:0.5 G5:1 R:1", "A5:0.5 D6:0.5 F#6:0.5 A6:0.5 F#6:1 D6:1", "C#6:2 A5:2",
        "B5:0.25 C#6:0.25 D6:0.25 E6:0.25 F#6:1 E6:0.5 D6:0.5 B5:1", "D6:1 B5:1 G5:2", "E6:0.5 D6:0.5 B5:0.5 G5:0.5 E5:1 G5:1", "F#5:2 A#5:2",
        "F#6:0.5 E6:0.5 D6:0.5 C#6:0.5 B5:1 F#5:1", "G5:1 B5:1 D6:1 G6:1", "F#6:0.5 D6:0.5 A5:0.5 F#5:0.5 D6:2", "C#6:1 E6:1 A6:2",
        "B6:1 F#6:1 D6:1 B5:1", "G6:1 D6:1 B5:1 G5:1", "E6:0.5 G6:0.5 B6:1 A#6:1 F#6:1", "F#6:4"]
WALTZ = S.sc("人形が踊る")
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "C2"); v4 = voice(ch, 66, 4, prev=prev); prev = v4
    if n in ("時計の刻み", "止まった時計"):
        if (n == "時計の刻み" and i >= 6) or (n == "止まった時計" and i % 2 == 0): PR.bar(b, f"{nm(v4[1])}:2 {nm(v4[3])}:2")
        continue
    if n == "人形が踊る": continue
    if n == "時計の鐘":
        if i < 6: PL.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2"); PR.bar(b, " ".join(f"{nm(x)}:1" for x in v4))
        elif i == 6: PL.bar(b, f"{nm(r)}:8"); PR.bar(b, " ".join(f"{nm(x)}:0.25" for x in v4) + f" {nm(v4[3] + 12)}:7")
        continue
    if n == "ピアノソロ": PRS.bar(b, SOLO[i])
    if n in ("Aメロ1", "Aメロ2", "Cメロ"):
        PL.bar(b, f"{nm(r)}:1.5 {nm(r + 7)}:1 {nm(r + 12)}:1.5")
        PR.bar(b, f"R:1 {nm(v4[1])}:0.5 {nm(v4[2])}:0.5 R:1 {nm(v4[2])}:0.5 {nm(v4[3])}:0.5")
    else:
        PL.bar(b, " ".join(f"{nm(r if q % 2 == 0 else r + 12)}:0.5" for q in range(8)))
        PR.bar(b, f"{nm(v4[0])}:0.5 {nm(v4[1])}:0.5 {nm(v4[2])}:0.5 {nm(v4[3])}:0.5 {nm(v4[2])}:0.5 {nm(v4[3])}:0.5 {nm(v4[2] + 12 if v4[2] + 12 < 90 else v4[2])}:1")
# ワルツ（3拍のまとまり: 1拍目に低い音、2・3拍目に和音）
t = WALTZ[0] * B; k = 0
while t < (WALTZ[-1] + 1) * B - 1e-6:
    bar = int(t // B); ch = S.chords[bar]; r = low(ch, "C2"); v = voice(ch, 66, 3)
    PL.at(round(t, 3), f"{nm(r)}:1!")
    for j, x in enumerate(v): PR.at(round(t + 1, 3), f"{nm(x)}:0.75"); PR.at(round(t + 2, 3), f"{nm(x)}:0.75")
    if k % 2 == 1: BOX.at(round(t, 3), f"{nm(tones(ch, 'D6', 'D7')[k % 3])}:1")
    t += 3; k += 1

# ================= ギター・ストリングス =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; pw = power(ch, "E2"); sv = voice(ch, 62, 3)
    if n in ("サビ1", "サビ2", "最後のサビ") or (n == "ピアノソロ" and i >= 8):
        # 2026-11-04: 人間「ギター、ジャン、ジャン、という感じで弾くところを、ジャジャジャジャジャジャ…と弾いて欲しい」→ のばす所を8分の刻みに
        for j in range(2): GT[j].bar(b, f"{nm(pw[j])}:0.75! {nm(pw[j])}:0.75 {nm(pw[j])}:0.5 " + " ".join(f"{nm(pw[j])}:0.5" for _ in range(4)))
    if n in ("Bメロ2", "サビ2", "人形が踊る", "最後のサビ", "Cメロ"):
        for j in range(3): STR[j].bar(b, f"{nm(sv[j])}:4")
    if n == "時計の鐘" and i == 6:
        for j in range(3): STR[j].bar(b, f"{nm(sv[j])}:8")

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "時計の刻み" and i < 6: continue
    if n == "止まった時計":
        if i % 2 == 0: BASS.bar(b, bass_line(S, b, "long", lo="E1"))
        continue
    if n == "人形が踊る": continue
    if n == "時計の鐘":
        if i < 7: BASS.bar(b, bass_line(S, b, "half" if i < 6 else "long", lo="E1"))
        continue
    BASS.bar(b, bass_line(S, b, "root8" if n.startswith(("サビ", "最後", "ピアノ")) or n.startswith("Bメロ") else "half", lo="E1"))
t = WALTZ[0] * B
while t < (WALTZ[-1] + 1) * B - 1e-6:
    bar = int(t // B); BASS.at(round(t, 3), f"{nm(low(S.chords[bar], 'E1'))}:2.5"); t += 3

# ================= 時計の鐘（正午の鐘・最後の1つ） =================
BELL.bar(S.sc("人形が踊る")[0] - 1, "R:2 B4:2"); BELL.bar(S.sc("時計の鐘")[-1], "B4:4")
cym_swell(CYM, S.sc("人形が踊る")[0], 2, "E4")

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "時計の刻み":
        if i >= 6: vgroove(D, b, "half", ghosts=0.15, seed=b)
        if last: put_fill(D, b, "small")
    elif n in ("Aメロ1", "Aメロ2"):
        # つまずく刻み: キックを 3.5拍の歯車に合わせて置く（2小節で1回り）
        kk = "X.....X.......X." if i % 2 == 0 else "......X.......X."
        vgroove(D, b, "beat8", ghosts=0.3, seed=b, k=kk)
        if i == 0: crash(D, b)
        if i % 8 == 7: put_fill(D, b, "small" if not last else "snare16")
    elif n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "halfdrive", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
    elif n in ("サビ1", "サビ2", "最後のサビ", "ピアノソロ"):
        vgroove(D, b, "vrock2", ghosts=0.25, seed=b)
        if i % 8 == 0: crash(D, b, "C2", 4)
        if i % 8 == 7 and not last: put_fill(D, b, "tomdown" if i % 16 == 15 else "small")
    elif n == "Cメロ":
        vgroove(D, b, "half", ghosts=0.2, seed=b)
    elif n == "時計の鐘":
        if i < 6: vgroove(D, b, "beat8", ghosts=0.2, seed=b)
        if i == 6: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 6)
# ワルツのドラム（3拍のまとまり: 1拍目にキック、2・3拍目にスネアとハイハット）
cells = {}
t = WALTZ[0] * B
while t < (WALTZ[-1] + 1) * B - 1e-6:
    for off, kind in ((0, "K"), (1, "S"), (2, "S"), (0, "H"), (1, "H"), (2, "H"), (1.5, "h"), (2.5, "h")):
        x = t + off; bar = int(x // B); c = int(round((x - bar * B) * 4))
        cells.setdefault(bar, []).append((c, kind))
    t += 3
for bar, lst in cells.items():
    kk, ss, hh = ["."] * 16, ["."] * 16, ["."] * 16
    for c, kind in lst:
        if kind == "K": kk[c] = "X"
        elif kind == "S": ss[c] = "x"
        elif kind == "H": hh[c] = "X"
        else: hh[c] = "x"
    D.set(bar, "".join(kk), "".join(ss), "".join(hh))
crash(D, WALTZ[0], "C2", 6); crash(D, WALTZ[16], "C2", 4)

SIL.add(S.sc("人形が踊る")[0] - 1, 2, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の18。ロック（変拍子のピアノロック）。B の短調（サビは D）・168、転調なし。"
          "祖父の時計屋をたたむ日、からくり人形が最後に踊る。時計の刻みと、3.5拍でくり返してつまずくチェンバロの歯車で始まり、ピアノロックのサビ、ピアノソロ、"
          "刻みがゆっくりになって止まる時計、正午の鐘のあとの大サビはワルツ（3拍のまとまり）、時計の鐘1つで終わる。自作")
finish(S, LY, V, 0, level={"verse": -0.3}, special={"止まった時計": -0.7, "Cメロ": -0.4, "人形が踊る": 0.55, "最後のサビ": 0.35})
