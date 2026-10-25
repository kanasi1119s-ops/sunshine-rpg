# vb25 01「無限階エレベーター」Infinite Floor Elevator（仮）— テクノポップ。178・4/4。D → E → F# → G#（階が上がるたびに全音ずつ、3回転調）
# 2026-10-25 人間「ゲームの話は俺が言うまで出さない約束」→ 前の「ネオンキャンディ・バグ」（ゲーム機の話）をやめ、曲名・物語・リフから作り直した。
# 物語: 雨の日曜日、デパートのエレベーターに乗ると、ボタンに「屋上」より上の階が増えている。押すたびに、ありえない売り場の扉が開く。
#   1階 香水売り場（きらきら）→ 3階 楽器売り場（試し弾きの音が混ざる）→ 4階・5階 → ガタンと揺れる → 6階 布団売り場（ふかふか・Half feel）
#   → 屋上で一息 → 屋上より上 → 空の階で扉が開く → 和音が1段ずつ積み上がり、いちばん上の音が空に消える
# 旋律の性格: 階段のように一音ずつ上がる。大きな跳躍は、最後のサビの終わりの1回だけ。
# 音の決め方（2026-10-25 人間「薄くするな、ごちゃごちゃにもするな」）: 場面ごとに 低い所・中くらい・高い所・リズム を埋め、役割をかぶらせない。
from vb25_lib import *

S = Song("01", "elevator", "無限階エレベーター（仮）", "Infinite Floor Elevator", 178, 4, "D", "major", "テクノポップ（ボカロ）")
S.kit = "electro"
S.flags = S.flags + " --piano salamander"
S.no_depth = True            # 共通のパッド・きらめきは足さない（この曲の音は場面ごとに決める）
S.keep_old_synth = True
KD, KE, KF, KG = Key("D", "major"), Key("E", "major"), Key("F#", "major"), Key("G#", "major")

VD = ["Dmaj7", "Em7", "F#m7", "Gmaj7", "A", "Bm7", "C", "A/C#"]
PRE1 = ["Gmaj7", "A/G", "F#m7", "Bm7", "Em7", "F#m7", "G", "B7"]
CE = ["E", "B/D#", "C#m7", "Amaj7", "F#m7", "G#m7", "A", "B"]
CE2 = ["E", "G#7", "C#m7", "Amaj7", "F#m7", "G#m7", "Asus2", "B"]
VE = ["Emaj7", "F#m7", "G#m7", "Amaj7", "B", "C#m7", "D", "B/D#"]
PRE2 = ["Amaj7", "B/A", "G#m7", "C#m7", "F#m7", "G#m7", "A", "C#7"]
CF = ["F#", "C#/F", "D#m7", "Bmaj7", "G#m7", "A#m7", "B", "C#"]
CF2 = ["F#", "A#7", "D#m7", "Bmaj7", "G#m7", "A#m7", "Bsus2", "C#"]
BR = ["Bmaj7", "A#m7", "G#m7", "C#sus4", "Bmaj7", "A#m7", "D#m7", "C#"]
ROOF = ["D#m7", "Bmaj7", "F#", "C#", "D#m7", "Bmaj7", "G#m7", "C#"]
INT2 = ["F#maj7", "G#m7", "A#m7", "Bmaj7", "C#", "D#m7", "E", "D#7"]
PRE3 = ["C#maj7", "D#/C#", "Cm7", "Fm7", "A#m7", "Cm7", "C#", "D#7"]
CG = ["G#", "D#/G", "Fm7", "C#maj7", "A#m7", "Cm7", "C#", "D#"]
CG2 = ["G#", "C7", "Fm7", "C#maj7", "A#m7", "Cm7", "C#sus2", "D#"]
CG3 = ["G#", "C7", "Fm7", "C#maj7", "A#m7", "D#/G", "C#", "D#sus4"]
OUT = ["C#maj7", "D#/C#", "G#", "G#", "C#maj7", "D#/C#", "Fm7", "D#sus4", "G#", "G#"]

S.scene("扉の向こう", 8, "intro", ["Dmaj7", "Em7", "F#m7", "Gmaj7"] * 2)
S.scene("1階", 16, "verse", VD * 2)
S.scene("上へ", 8, "pre", PRE1)
S.scene("3階", 16, "chorus", CE + CE2)
S.scene("エレベーターの中", 8, "interlude", ["Emaj7", "F#m7", "G#m7", "Amaj7"] * 2)
S.scene("4階", 16, "verse", VE * 2)
S.scene("上へ2", 8, "pre", PRE2)
S.scene("5階", 16, "chorus", CF + CF2)
S.scene("ガタン", 1, "break", ["F"])
S.scene("6階", 16, "bridge", BR * 2)
S.scene("屋上", 8, "break", ROOF)
S.scene("エレベーターの中2", 8, "interlude", INT2)
S.scene("屋上より上", 8, "pre", PRE3)
S.scene("空の階", 32, "chorus", CG + CG2 + CG + CG3)
S.scene("いちばん上", 10, "outro", OUT)

# ---------------- パート ----------------
V = Voice(S, vol=0.22, delay=0.75, patch="surgeFormantPulse")            # 歌の役: 声のような丸いパルス（案内の声にも重なる）
VS = S.track("歌の役の重ね（サビ）", "lead", patch="surgeHappySaws", volume=0.085, pan=0.0, reverb=0.16, mono=True,
             fx=[{"type": "filter", "kind": "highpass", "freq": 300, "q": 0.7}, {"type": "plate", "mix": 0.16}])
RIFF = S.track("階段のリフ", "lead", patch="surgeChordReset", volume=0.12, pan=-0.15, reverb=0.14, mono=True,
               fx=[{"type": "filter", "kind": "highpass", "freq": 200, "q": 0.7}, {"type": "pingpong", "beats": 0.75, "mix": 0.14, "feedback": 0.25}])
BASS = S.track("シンセベース", "bass", **synth_bass_spec("surgeBassAnalogBassImaged", vol=0.24, duck=0.25))
PADSPEC = dict(patch="surgePadSparkly", volume=0.05, pan=0.0, reverb=0.35, sustain=1.5, duck=0.2,
               fx=[{"type": "filter", "kind": "highpass", "freq": 250, "q": 0.7}])
SPARK = [S.track(f"きらめくパッド{i + 1}", "pad", **dict(PADSPEC)) for i in range(3)]
POP = S.track("香水のきらめき", "pad", patch="surgePopcorn", volume=0.08, pan=0.4, reverb=0.3, sustain=0.6,
              fx=[{"type": "filter", "kind": "highpass", "freq": 400, "q": 0.7}, {"type": "pingpong", "beats": 0.75, "mix": 0.25, "feedback": 0.3}])
STSPEC = dict(patch="surgeChord5thElement", volume=0.06, pan=0.0, reverb=0.2, sustain=0.6, duck=0.3,
              fx=[{"type": "filter", "kind": "highpass", "freq": 220, "q": 0.7}, {"type": "eq", "low": 0, "mid": -2, "midHz": 400, "high": 0}])
STAB = [S.track(f"和音の刻み{i + 1}", "pad", **dict(STSPEC)) for i in range(3)]
EPSPEC = dict(patch="surgeKeysDxEp", volume=0.09, pan=-0.25, reverb=0.25, sustain=1.2)
EP = [S.track(f"FM エレピ{i + 1}", "pad", **dict(EPSPEC)) for i in range(3)]      # 4階・屋上の和音。前奏と各階の頭の「チャイム」も
PN = S.track("ピアノ（試し弾き・右手）", "piano", volume=0.12, pan=-0.3, reverb=0.25)
PNL = S.track("ピアノ（試し弾き・左手）", "piano", volume=0.12, pan=-0.3, reverb=0.25)
GTR = S.track("ギター（試し弾き）", "guitar", **clean_gtr_spec(vol=0.1, pan=0.5))
BRS = S.track("ブラス（試し弾き）", "brass", volume=0.1, pan=0.3, reverb=0.25, sustain=0.8)
SOFT = [S.track(f"やわらかいパッド{i + 1}", "pad", **dict(patch="surgePadPad2Mw", volume=0.07, pan=0.0, reverb=0.4, sustain=2.0,
                                                           fx=[{"type": "filter", "kind": "lowpass", "freq": 2500, "q": 0.7}])) for i in range(3)]
SKY = [S.track(f"空のパッド{i + 1}", "pad", **dict(patch="surgePadNeverending", volume=0.06, pan=0.0, reverb=0.45, sustain=2.5,
                                                    fx=[{"type": "filter", "kind": "highpass", "freq": 200, "q": 0.7}])) for i in range(3)]
STR = [S.track(f"ストリングス{i + 1}", "strings", **dict(volume=0.07, pan=0.0, reverb=0.4, sustain=1.6)) for i in range(2)]
D = S.drumkit()
SIL = Silence(S)


def dg(n):
    """度数の番号（1〜）→ 度数の文字（8＝1'）"""
    o, d = divmod(n - 1, 7)
    return f"{d + 1}" + "'" * o


def stair(a):
    """階段のリフ（1小節）: a から4つの音で一段ずつ上がり、休んでもう一度（2つ目から）"""
    return f"{dg(a)}:0.5 {dg(a + 1)}:0.5 {dg(a + 2)}:0.5 {dg(a + 3)}:0.5 R:0.5 {dg(a + 1)}:0.5 {dg(a + 2)}:0.5 {dg(a + 3)}:0.5"


# ---------------- 旋律 ----------------
VA = ["1:1 2:0.5 3:0.5 3:1 R:1", "2:1 3:0.5 4:0.5 4:1 R:1", "3:1 4:0.5 5:0.5 5:1.5 R:0.5", "4:0.5 3:0.5 2:0.5 1:0.5 2:2",
      "5:1 6:0.5 7:0.5 7:1 R:1", "6:1 7:0.5 1':0.5 1':1 R:1", "b7:1 1':0.5 2':0.5 2':1 1':1", "7:3 R:1"]
VA2 = VA[:6] + ["b7:1 1':0.5 2':0.5 3':1 2':1", "7:1 6:1 5:2"]
PR = ["R:1 4:0.5 5:0.5 6:1 5:1", "R:1 5:0.5 6:0.5 7:1 6:1", "R:1 6:0.5 7:0.5 1':1 7:1", "R:1 7:0.5 1':0.5 2':1 1':1",
      "R:1 1':0.5 2':0.5 3':1 2':1", "R:1 3':0.5 5':0.5 5':1 3':1", "4':1 5':1 6':1 5':1", "6':2 R:2"]
CH = ["3:0.5 4:0.5 5:1 5:0.5 6:0.5 5:1", "5:0.5 4:0.5 3:1 2:0.5 3:0.5 4:1", "3:0.5 4:0.5 5:0.5 6:0.5 7:1 6:1", "5:2 3:1 R:1",
      "4:0.5 5:0.5 6:1 6:0.5 7:0.5 6:1", "5:0.5 6:0.5 7:1 7:0.5 1':0.5 7:1", "6:0.5 7:0.5 1':1 2':1 1':1", "7:3 R:1"]
CH2 = CH[:6] + ["1':1 7:1 6:1 7:1", "7:2 R:2"]
BRL = ["3:2 4:2", "5:4", "4:2 3:2", "2:4", "3:2 4:2", "5:2 6:2", "7:2 1':2", "2':4"]

for name, K in (("1階", KD), ("4階", KE)):
    lines = VA + VA2
    for i, b in enumerate(S.sc(name)): V.bar(b, K.mel(lines[i], oct=4))
for name, K in (("上へ", KD), ("上へ2", KE), ("屋上より上", KG)):
    for i, b in enumerate(S.sc(name)): V.bar(b, K.mel(PR[i], oct=4 if K is not KG else 3))
for name, K in (("3階", KE), ("5階", KF)):
    lines = CH + CH2
    for i, b in enumerate(S.sc(name)):
        V.bar(b, K.mel(lines[i], oct=4)); VS.bar(b, plain(K.mel(lines[i], oct=4)))
# 空の階: 4周目の最後の2小節だけ、いちばん上へ大きく跳ぶ（曲の中で1回だけ）
SKYL = CH + CH2 + CH + CH[:6] + ["6:0.5 7:0.5 1':1 R:0.5 5':1.5", "5':4"]
for i, b in enumerate(S.sc("空の階")):
    V.bar(b, KG.mel(SKYL[i], oct=3)); VS.bar(b, plain(KG.mel(SKYL[i], oct=3)))
for i, b in enumerate(S.sc("6階")):
    V.bar(b, KF.mel(BRL[i % 8], oct=3 if i < 8 else 4), low=False)
for i, b in enumerate(S.sc("屋上")):
    V.bar(b, KF.mel(CH[i], oct=3), low=False)

# ---------------- 階段のリフ ----------------
for i, b in enumerate(S.sc("扉の向こう")): RIFF.bar(b, KD.mel(stair(1 + i % 4), oct=4))
for i, b in enumerate(S.sc("エレベーターの中")): RIFF.bar(b, KE.mel(stair(1 + i % 4), oct=4))
for i, b in enumerate(S.sc("エレベーターの中2")):
    RIFF.bar(b, KF.mel(stair(1 + i) if i < 6 else ("b7:0.5 1':0.5 2':0.5 3':0.5 R:0.5 1':0.5 2':0.5 3':0.5" if i == 6 else "6:0.5 7:0.5 1':0.5 2':0.5 #2':2"), oct=4))
for name, K in (("上へ", KD), ("上へ2", KE), ("屋上より上", KG)):       # Bメロ: 歌の下で、リフが一段ずつ上がる（小さく・高め）
    for i, b in enumerate(S.sc(name)):
        if i < 7: RIFF.bar(b, K.mel(stair(4 + i), oct=4 if K is not KG else 3))
for i, b in enumerate(S.sc("空の階")):                               # 空の階: リフが高い所で回り続ける
    if i % 8 in (0, 1, 2, 3) and i >= 8: RIFF.bar(b, KG.mel(stair(8 + i % 4), oct=3))
# 前奏の扉の向こう: リフとベースは、扉ごしにこもって聞こえる（最後の1小節で扉が開く）
muffle(S, [RIFF], range(0, 7), freq=700)

# ---------------- 伴奏 ----------------
def chord3(tracks, b, ch, center, rhythm):
    v = voice(ch, center, len(tracks))
    for j, t in enumerate(tracks): t.bar(b, " ".join(f"{nm(v[j])}:{L}" if L > 0 else f"R:{-L}" for L in rhythm))


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    # ベース
    if n == "扉の向こう": BASS.bar(b, bass_line(S, b, "long" if i < 6 else "oct8"))
    elif n in ("1階", "4階"): BASS.bar(b, bass_line(S, b, "root8" if i < 8 else "oct8"))
    elif n.startswith("上へ") or n == "屋上より上": BASS.bar(b, bass_line(S, b, "push" if i < 7 else "long"))
    elif n in ("3階", "5階", "空の階"): BASS.bar(b, bass_line(S, b, "oct8"))
    elif n.startswith("エレベーターの中"): BASS.bar(b, bass_line(S, b, "pulse"))
    elif n == "ガタン": BASS.bar(b, f"{nm(low(ch, 'E1'))}:2 R:2")
    elif n == "6階": BASS.bar(b, bass_line(S, b, "long") if i >= 2 else "R:4")
    elif n == "いちばん上" and i < 8: BASS.bar(b, bass_line(S, b, "long"))
    # 1階: きらめくパッド＋香水のきらめき（歌のすき間に）
    if n == "1階" or (n == "5階" and i >= 8):
        chord3(SPARK, b, ch, 66, [4])
    if n == "1階" and i % 2 == 1:
        t = tones(ch, "A5", "A6"); POP.bar(b, "R:2 " + " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 1, 2, 3)))
    # 和音の刻み（サビ）: 中くらいの帯域で裏を刻む
    if n in ("3階", "5階", "空の階"):
        chord3(STAB, b, ch, 64, [-0.5, 1, -0.5, 1, -0.5, 0.5])
    # 3階: 試し弾き（本物のピアノの和音・ギターの合いの手・ブラスの短い句）。主役ではなく、すき間に
    if n == "3階":
        PNL.bar(b, f"{nm(low(ch, 'C3'))}:2 {nm(low(ch, 'C3') + 12)}:2")
        v = voice(ch, 72, 3); PN.bar(b, " ".join(f"{nm(x)}:1" for x in [v[0], v[1], v[2], v[1]]))
        if i % 4 == 1: GTR.bar(b, "R:2.5 " + " ".join(f"{nm(x)}:0.25" for x in tones(ch, "E4", "E5")[:4]) + " R:0.5")
        if i % 4 == 3: BRS.bar(b, "R:3 " + f"{nm(tones(ch, 'G4', 'G5')[0])}:0.5 {nm(tones(ch, 'G4', 'G5')[1])}:0.5")
    # 4階・屋上: FM エレピの和音
    if n == "4階": chord3(EP, b, ch, 64, [1.5, 1, 1.5])
    if n == "屋上": chord3(EP, b, ch, 62, [4])
    # チャイム（扉の向こうの最後・各階の頭）: FM エレピの高い2音
    if (n == "扉の向こう" and i == 6) or (i == 0 and n in ("1階", "3階", "4階", "5階", "6階", "空の階")):
        K = {"扉の向こう": KD, "1階": KD, "3階": KE, "4階": KE, "5階": KF, "6階": KF, "空の階": KG}[n]
        if n == "扉の向こう": EP[0].bar(b, "R:2 " + K.mel("5':1 3':1", oct=4))
        else: EP[0].bar(b, K.mel("5':0.5 3':1.5", oct=4) + " R:2")
    # 6階: やわらかいパッド
    if n == "6階": chord3(SOFT, b, ch, 60, [4])
    # 空の階: 広いパッド＋ストリングス
    if n == "空の階":
        chord3(SKY, b, ch, 62, [4])
        if i >= 8: chord3(STR, b, ch, 70, [4])
    if n == "屋上より上" and i >= 4: chord3(SKY, b, ch, 62, [4])

# いちばん上: 和音を下から1音ずつ積み上げる（それぞれ最後までのばす）→ いちばん上の音が空に消える
ob = S.sc("いちばん上")
stack = [("STR0", STR[0], "G#3"), ("SKY0", SKY[0], "C4"), ("SKY1", SKY[1], "D#4"), ("STR1", STR[1], "G4"), ("SKY2", SKY[2], "A#4"), ("EP0", EP[0], "C5"), ("EP1", EP[1], "D#5")]
for j, (_, t, note) in enumerate(stack):
    st = ob[0] * 4 + j * 2
    t.at(st, f"{note}:{max(2, (ob[-1] + 1) * 4 - st - 2)}")
V.at(ob[0] * 4 + 16, "G5:16~")

# ---------------- ドラム ----------------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "扉の向こう":
        if i < 6: D.set(b, "X...X...X...X...", "................", "................")
        elif i == 6: vgroove(D, b, "four", seed=b)
        else: put_fill(D, b, "build")
    elif n in ("1階", "4階"):
        vgroove(D, b, "vrock2" if n == "1階" else "beat8", ghosts=0.3, seed=b)
        if n == "4階" and i >= 8: ride(D, b, "x.x.x.x.")
        if i == 0: crash(D, b)
        if i % 8 == 7: put_fill(D, b, "small")
    elif n.startswith("上へ") or n == "屋上より上":
        vgroove(D, b, "half" if i < 4 else "four16", ghosts=0.25, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: put_fill(D, b, "lift")
    elif n in ("3階", "空の階"):
        vgroove(D, b, "vrock", ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16")
        if last and n == "3階": put_fill(D, b, "tomdown")
    elif n == "5階":
        vgroove(D, b, "halfdrive" if i < 8 else "vrock", ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b)
        if i == 7: put_fill(D, b, "tomtrip")
    elif n.startswith("エレベーターの中"):
        vgroove(D, b, "four16", seed=b)
        if i == 0: crash(D, b, "G2")
        if last: put_fill(D, b, "snare16")
    elif n == "ガタン":
        D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 2)
    elif n == "6階":
        if i < 4: D.set(b, "." * 16, "." * 16, "." * 16)
        else: vgroove(D, b, "half", ghosts=0.2, seed=b, h="x...x...x...x...")
        if last: put_fill(D, b, "build")
    elif n == "屋上":
        D.set(b, "." * 16, "." * 16, "." * 16)
    elif n == "いちばん上":
        if i == 0: D.set(b, "X" + "." * 15, "." * 16, "." * 16); crash(D, b, "C2", 4)
        else: D.set(b, "." * 16, "." * 16, "." * 16)

# ガタン: 全員が半音下（F）で2拍鳴って、残り2拍は無音
SIL.add(S.sc("ガタン")[0], 2, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の01。テクノポップ・178。D→E→F#→G#（階ごとに全音ずつ3回転調）。"
          "雨の日曜日、デパートのエレベーターに屋上より上の階が増えていて、押すたびにありえない売り場の扉が開く。"
          "扉の向こうでこもって聞こえる階段のリフから始まり、香水売り場のきらめき、楽器売り場の試し弾き、ガタンと揺れて半音下がり、"
          "布団売り場の Half feel、屋上で一息、空の階で扉が開く。最後は和音が1段ずつ積み上がって空に消える。歌の役は声のようなシンセ。自作")
S.flags += " --space hall --space-wet 0.18"
vwrite(S)
