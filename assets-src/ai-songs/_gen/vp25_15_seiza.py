# vp25 15「星座をつなぐ線」Connect the Constellations（仮）— エレクトロニカ。E♭長調（リディアン寄り）・96・4/4（3+3+2 の強拍）。主役の楽器: ハープ
# 物語: 夏休みの夜、丘の上で星図を広げる。ばらばらの星を線でつなぐと、星座が一つずつ現れる。天の川が流れ、冬の星座まで描きおえると、
#   夜空ぜんぶが一枚の大きな絵になる。明け方、星は一つずつ消えていく。
# 形: 夜空の点を線でつないで星座を描く。星座が一つできるたびに次へ。最後に全部が一枚の絵
# 場面と強さ: 夜空＝静か／星座が完成するたびに小さな山／天の川＝流れる中くらい／全天＝最大／明け方＝長い和音で消える
# 旋律の性格: はじめは離れた点（大きな跳躍・ひとつだけの音）→ だんだんつながってなめらかな旋律に
# 崩す所: 旋律が最後まで「点」のままの楽器を1つ残す（左右に散るガラスの粒）
from vp25_lib import *

S = Song("15", "seiza", "星座をつなぐ線（仮）", "Connect the Constellations", 96, 4, "Eb", "lydian", "エレクトロニカ")
K = S.key
SKY = ["Ebmaj7", "F/Eb", "Ebmaj7", "F/Eb"]
C1 = ["Ebmaj7", "F/Eb", "Gm7", "Cm7", "Abmaj7", "Bb", "Ebmaj7", "F/Eb"]
C2 = ["Cm7", "Gm7", "Abmaj7", "Ebmaj7/G", "Fm7", "Gm7", "Abmaj7", "Bbsus4"]
MILKY = ["Abmaj7", "Bb/Ab", "Gm7", "Cm7", "Fm7", "Bb", "Ebmaj7", "Ebmaj7"]
WINTER = ["Gm7", "Abmaj7", "Bb", "Cm7"]
ALL = ["Ebmaj7", "F/Eb", "Gm7", "Cm7", "Abmaj7", "Bb", "Gm7", "Cm7", "Fm7", "Gm7", "Abmaj7", "Bbsus4"]
S.scene("夜空", 8, "intro", SKY)
S.scene("北の星座", 16, "verse", C1)
S.scene("夏の三角", 16, "pre", C2)
S.scene("天の川", 20, "bridge", MILKY + MILKY[:4] + MILKY)
S.scene("冬の星座", 16, "verse", WINTER)
S.scene("全天", 24, "chorus", ALL + ALL)
S.scene("明け方", 8, "outro", ["Ebmaj7", "Ebmaj7", "F/Eb", "F/Eb", "Ebmaj7", "Ebmaj7", "Ebmaj7", "Ebmaj7"])

HP = S.track("主役: ハープ", "harp", patch="folkHarp", volume=0.24, pan=-0.15, reverb=0.4, sustain=1.8, gainDb=5,
             fx=[{"type": "eq", "low": -3, "mid": 2, "midHz": 2500, "high": 1}])
HP2 = S.track("ハープ（分散和音）", "harp", patch="folkHarp", volume=0.15, pan=0.35, reverb=0.45, sustain=2.0, gainDb=2)
STAR = S.track("星の粒（最後まで点のまま）", "pad", patch="glassPluck", volume=0.07, pan=0.5, sustain=1.0, reverb=0.5,
               fx=[{"type": "filter", "kind": "highpass", "freq": 1000, "q": 0.7}, {"type": "pingpong", "beats": 1.5, "mix": 0.3, "feedback": 0.35}])
LEAD = S.track("リード（歌の役）", "lead", **lead_spec("calliope", vol=0.17, pan=0.05, delay=1.5))
BASS = S.track("低音", "bass", **synth_bass_spec("synthBass1", vol=0.19, duck=0.15))
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("halo", vol=0.06, pan=[-0.55, 0.55, 0][i])) for i in range(3)]
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()

# ---------- 星座の動機（6音）。「点」→「線」 ----------
# 点: 動機の音だけを、間を大きくあけて（跳躍が大きく見える）。線: 音の間を音階でつないで、なめらかに
MOT = ["1'", "5", "3'", "4'", "2'", "5'"]          # 星の位置（度数）


def points(k, shift=0, oct=4):
    a, b_ = MOT[k % 6], MOT[(k + 1) % 6]
    return K.mel(seq_up(f"{a}:1 R:1.5 {b_}:1.5", K, shift), oct=oct)


def line(k, shift=0, oct=4):
    a, b_, c = MOT[k % 6], MOT[(k + 1) % 6], MOT[(k + 2) % 6]
    return K.mel(seq_up(f"{a}:1 {b_}:0.5 {c}:0.5 {b_}:1 {a}:1", K, shift), oct=oct)


for i, b in enumerate(S.sc("夜空")):
    HP.bar(b, ["R:4", K.mel("1':1 R:3", oct=4), "R:4", K.mel("R:2 5':2", oct=4), K.mel("3':1 R:3", oct=4), "R:4", K.mel("R:1 4':3", oct=4), "R:4"][i])
for i, b in enumerate(S.sc("北の星座")):
    HP.bar(b, points(i) if i < 8 else (points(i, 1) if i % 2 == 0 else line(i)))
for i, b in enumerate(S.sc("夏の三角")):
    HP.bar(b, line(i, -1) if i % 2 == 0 else points(i, 2))
# 天の川: 流れる16分の分散和音（ハープ2台）
for i, b in enumerate(S.sc("天の川")):
    t = tones(S.chords[b], "Eb4", "Eb6")
    HP2.bar(b, " ".join(f"{nm(t[q % len(t)], True)}:0.25" for q in list(range(8)) + list(range(8, 0, -1))))
    HP.bar(b, line(i, 0, 4) if i % 4 < 2 else line(i, 2, 4))
for i, b in enumerate(S.sc("冬の星座")):
    HP.bar(b, line(i, -2) if i < 8 else line(i, 0))
for i, b in enumerate(S.sc("全天")):
    HP.bar(b, line(i, 0, 5) if i < 12 else line(i, 2, 4))
    t = tones(S.chords[b], "Eb4", "Eb6")
    HP2.bar(b, " ".join(f"{nm(t[q % len(t)], True)}:0.25" for q in list(range(8)) + list(range(8, 0, -1))))
for i, b in enumerate(S.sc("明け方")):
    if i < 4: HP.bar(b, points(i, 0, 4))

# 歌の役: 星座ができる所（各場面の後半）で、点をつないだ長い旋律
LN = ["5':2 3':1 2':1", "1':3 R:1", "3':2 5':1 6':1", "5':4", "4':2 5':1 3':1", "2':3 1':1", "7:2 1':1 2':1", "1':4"]
LN2 = ["3':1 5':1 1'':2", "7':2 5':2", "6':1 5':1 3':2", "5':4", "4':1 5':1 6':2", "5':2 3':2", "2':2 4':2", "5':4"]
for sc_, pool, start in (("北の星座", LN, 8), ("夏の三角", LN2, 8), ("冬の星座", LN, 8), ("全天", LN2 + LN + LN2, 0)):
    for i, b in enumerate(S.sc(sc_)):
        if i >= start: LEAD.bar(b, K.mel(pool[(i - start) % len(pool)], oct=4 if sc_ != "全天" or i < 16 else 5))

# 星の粒（最後まで点のまま）
rnd = random.Random(15)
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    dens = {"夜空": 0.15, "北の星座": 0.15, "夏の三角": 0.2, "天の川": 0.3, "冬の星座": 0.2, "全天": 0.3, "明け方": 0.15 - 0.02 * i}[n]
    t = tones(S.chords[b], "Bb5", "Bb7")
    STAR.bar(b, merge_rests(" ".join(f"{nm(rnd.choice(t), True)}:0.5" if rnd.random() < dens else "R:0.5" for _ in range(8))))

# ---------- 低音・パッド ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    r = low(S.chords[b], "E1")
    if n in ("北の星座", "夏の三角", "冬の星座") and i >= 8 or n in ("天の川", "全天"):
        BASS.bar(b, f"{nm(r, True)}:1.5 {nm(r, True)}:1.5 {nm(r + 7, True)}:1" if n != "天の川" else f"{nm(r, True)}:4")
    v = voice(S.chords[b], 58, 3)
    if n != "夜空" or i >= 4:
        for j in range(3): PAD[j].bar(b, f"{nm(v[j], True)}:4")
cym_swell(CYM, S.sc("全天")[0], 4, "E4"); cym_swell(CYM, S.sc("天の川")[0], 2, "C4")
CYM.bar(S.sc("明け方")[2], "B4:24")

# ---------- ドラム（3+3+2 の強拍。星座ができる所で入る） ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n in ("北の星座", "夏の三角", "冬の星座") and i >= 8:
        D.set(b, "X.....X.....X...", "......o.....X...", "x.x.x.x.x.x.x.x." if n != "冬の星座" else "x...x...x...x...")
        if i == 8: D.cym(b, "A2:4")
    elif n == "天の川":
        D.set(b, "X.........X.....", "........X.......", "..x...x...x...x.")
    elif n == "全天":
        D.set(b, "X.....X.....X...", "....X.......X..o", "x.xox.xox.xox.xo")
        if i % 12 == 0: crash(D, b, "C2")
        if i % 12 == 11: D.S[b] = "....X...x.xxXXXX"

S.flags += " --space hall --space-wet 0.2"
S.desc = ("仮: ボカロ曲のインスト25曲の15。エレクトロニカ。E♭長調（リディアン寄り）・96・3+3+2 の強拍。主役の楽器はハープ。夏休みの夜、丘の上で星座をつなぐ。"
          "はじめはばらばらの点（大きな跳躍・ひとつだけの音）だったハープの旋律が、星座ができるたびに音階でつながり、なめらかな線になる。"
          "天の川、冬の星座をへて、全部の星座が一枚の絵（最大）。左右に散るガラスの粒だけは最後まで点のまま。明け方、長い和音で消える。自作")
S.write()
