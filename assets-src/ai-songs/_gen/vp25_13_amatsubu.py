# vp25 13「雨粒のプログラム」Raindrop Program（仮）— エレクトロニカ。F# の陽旋法（1・2・4・5・6）・100・4/4。主役の楽器: 琴
# 物語: 縁側で雨を聞いている。最初の1粒、降り始め、本降り。水たまりに落ちた雨粒の音が、細かく刻まれ、遅れてこだまで返ってくる。
#   小雨になり、軒から落ちる雫の間がだんだん広がって、最後は静けさだけ。
# 形: 降りはじめの1粒→本降り→（水たまり）→本降り→やんで、軒から雫が落ちる
# 場面と強さ: 1粒＝極小／降り始め＝少しずつ／本降り＝細かい音が密で中〜大／水たまり＝刻みとこだまの掛け合い／小雨・雫＝間が広がって無音へ
# 旋律の性格: 同じ短い句が水たまりに落ちて細かく刻まれ（スタッター）、遅れてこだまで返ってくる（ディレイの掛け合い）
# 崩す所: 和の5音音階（陽旋法）を、エレクトロニカの細かい刻みに乗せる
from vp25_lib import *

S = Song("13", "amatsubu", "雨粒のプログラム（仮）", "Raindrop Program", 100, 4, "F#", "major", "エレクトロニカ")
K = S.key
YO = [0, 2, 5, 7, 9]                     # 陽旋法（1・2・4・5・6）
PCS = [(PC["F#"] + x) % 12 for x in YO]
DRIFT = ["Bsus2", "C#sus4", "D#m7", "G#m7"]
HEAVY = ["Bsus2", "C#sus4", "D#m7", "D#m7", "G#m7", "Bsus2", "C#7sus4", "C#7sus4"]
PUDDLE = ["G#m7", "D#m7", "Bsus2", "F#sus2"]
S.scene("一粒", 4, "intro", ["F#sus2"] * 4)
S.scene("降り始め", 16, "verse", DRIFT)
S.scene("本降り", 32, "chorus", HEAVY)
S.scene("水たまり", 16, "bridge", PUDDLE)
S.scene("本降り2", 24, "chorus", HEAVY)
S.scene("小雨", 12, "verse", DRIFT)
S.scene("雫", 8, "outro", ["F#sus2"] * 8)

KO = S.track("主役: 琴", "koto", volume=0.26, pan=-0.1, reverb=0.35, sustain=1.6, gainDb=5,
             fx=[{"type": "eq", "low": -3, "mid": 2.5, "midHz": 2500, "high": 1}])
KOE = S.track("琴（こだま）", "koto", volume=0.16, pan=0.55, reverb=0.5, sustain=1.6, gainDb=2,
              fx=[{"type": "filter", "kind": "lowpass", "freq": 4000, "q": 0.7}, {"type": "tape", "beats": 0.75, "mix": 0.3}])
LEAD = S.track("リード（歌の役）", "lead", **lead_spec("chiff", vol=0.17, pan=0.0, delay=1.5))
DROPS = S.track("雨の粒（左右）", "pad", patch="glassPluck", volume=0.07, pan=0.45, sustain=0.5, reverb=0.45,
                fx=[{"type": "filter", "kind": "highpass", "freq": 900, "q": 0.7}, {"type": "pingpong", "beats": 0.25, "mix": 0.25, "feedback": 0.3}])
GL = S.track("刻みの電子音", "pad", patch="pluckSynth", volume=0.07, pan=-0.45, sustain=0.3, reverb=0.2,
             fx=[{"type": "bitcrusher", "bits": 8, "mix": 0.2}, {"type": "filter", "kind": "highpass", "freq": 500, "q": 0.7}])
SUB = S.track("低音", "sub808", **sub_spec(0.2))
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("bowedGlass", vol=0.06, pan=[-0.55, 0.55, 0][i])) for i in range(3)]
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()

SC = [m for m in range(midi("F#3"), midi("F#6") + 1) if m % 12 in PCS]


def yo(i): return SC[max(0, min(len(SC) - 1, i))]


# 雨の句（琴）: 陽旋法の短い句。段（SC の番号）で書く
PHR = [[8, 9, 10, 8, 7], [7, 8, 10, 11, 10], [10, 9, 8, 7, 5], [5, 7, 8, 7, 5, 4]]
RHY = [[0.5, 0.5, 1, 0.5, 1.5], [0.5, 0.5, 0.5, 0.5, 2], [0.75, 0.25, 0.5, 0.5, 2], [0.5, 0.5, 0.5, 0.5, 1, 1]]


def phrase(k, shift=0):
    return " ".join(f"{nm(yo(p + shift))}:{r:g}" for p, r in zip(PHR[k % 4], RHY[k % 4]))


def stutter(k, shift=0):
    """句の最初の音を32分で刻み（水たまりに落ちる）、残りを短く"""
    p = PHR[k % 4]
    s = " ".join(f"{nm(yo(p[0] + shift))}:0.125{'!' if j == 0 else ','}" for j in range(8))
    rest = " ".join(f"{nm(yo(x + shift))}:0.5" for x in p[1:4])
    return f"{s} {rest} R:1.5"


# 一粒・降り始め: ひと粒ずつ（間をあけて）→ 句に育つ
for i, b in enumerate(S.sc("一粒")):
    KO.bar(b, [f"{nm(yo(10))}:4", "R:4", f"R:2 {nm(yo(8))}:2", "R:4"][i])
for i, b in enumerate(S.sc("降り始め")):
    if i < 8: KO.bar(b, [f"{nm(yo(10))}:1 R:3", f"R:2 {nm(yo(8))}:1 R:1", f"{nm(yo(9))}:1 R:1 {nm(yo(7))}:2", "R:4",
                         f"{nm(yo(10))}:0.5 {nm(yo(9))}:0.5 R:3", f"R:1 {nm(yo(8))}:0.5 {nm(yo(7))}:0.5 R:2", phrase(0), "R:4"][i])
    else: KO.bar(b, phrase(i) if i % 2 == 0 else "R:4"); KOE.bar(b, phrase(i - 1, 5) if i % 2 == 1 else "R:4")
# 本降り: 句とこだま（琴が言い、こだまが遅れて高く返す）。歌の役の長い音
HV = ["5':4", "6':2 5':2", "4':3 2':1", "1':4", "2':2 4':2", "5':4", "6':2 4':2", "5':4"]
for i, b in enumerate(S.sc("本降り") + S.sc("本降り2")):
    KO.bar(b, phrase(i) if i % 2 == 0 else stutter(i))
    KOE.bar(b, "R:1 " + " ".join(f"{nm(yo(x + 5))}:0.5" for x in PHR[i % 4][:4]) + " R:1")
    if i >= 8: LEAD.bar(b, K.mel(HV[i % 8], oct=4 if i < 32 else 5))
# 水たまり: 刻みとこだまの掛け合い（低音が旋律を受けつぐ）
for i, b in enumerate(S.sc("水たまり")):
    KO.bar(b, stutter(i, -2) if i % 2 == 0 else "R:4")
    KOE.bar(b, "R:4" if i % 2 == 0 else stutter(i, 3))
    SUB.bar(b, f"{nm(low(S.chords[b], 'E1'))}:1.5 {nm(low(S.chords[b], 'E1') + 7)}:0.5 {nm(low(S.chords[b], 'E1') + 12)}:1 {nm(low(S.chords[b], 'E1') + 10)}:1")
# 小雨・雫: 間が広がる
for i, b in enumerate(S.sc("小雨")):
    KO.bar(b, phrase(i) if i % 3 == 0 else "R:4")
    if i < 8 and i % 2 == 0: LEAD.bar(b, K.mel(["2':4", "1':4", "6:4", "5:4"][i // 2], oct=4))
for i, b in enumerate(S.sc("雫")):
    KO.bar(b, [f"{nm(yo(10))}:1 R:3", "R:4", f"R:2 {nm(yo(9))}:2", "R:4", "R:4", f"{nm(yo(8))}:4", "R:4", "R:4"][i])

# 雨の粒（左右に散る細かい音）: 本降りで密に
rnd = random.Random(13)
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    dens = {"一粒": 0.0, "降り始め": 0.1 + 0.02 * i, "本降り": 0.55, "水たまり": 0.25, "本降り2": 0.7, "小雨": 0.3 - 0.02 * i, "雫": 0.05}[n]
    toks = []
    for q in range(16):
        toks.append(f"{nm(rnd.choice([m for m in SC if m >= midi('C#5')]))}:0.25" if rnd.random() < dens else "R:0.25")
    DROPS.bar(b, merge_rests(" ".join(toks)))
    if n in ("本降り", "本降り2", "水たまり"):
        t = tones(S.chords[b], "F#4", "F#5")
        toks = []
        for q in range(16):
            toks.append(f"{nm(t[q % len(t)])}:0.25{',' if q % 3 else '!'}" if rnd.random() < 0.45 else "R:0.25")
        GL.bar(b, merge_rests(" ".join(toks)))

# 低音とパッド
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    r = low(S.chords[b], "E1")
    if n in ("本降り", "本降り2"): SUB.bar(b, f"{nm(r)}:2.5 {nm(r)}:1 R:0.5" if i % 2 == 0 else f"{nm(r)}:1.5 R:0.5 {nm(r + 12)}:0.5 {nm(r)}:1.5")
    elif n == "降り始め" and i >= 8: SUB.bar(b, f"{nm(r)}:4")
    v = voice(S.chords[b], 58, 3)
    if n not in ("一粒",) and not (n == "雫" and i >= 4):
        for j in range(3): PAD[j].bar(b, f"{nm(v[j])}:4")
cym_swell(CYM, S.sc("本降り")[0], 4, "E4"); cym_swell(CYM, S.sc("本降り2")[0], 2, "C4")

# ---------- ドラム（細かく刻んだ、くずれたビート。小節ごとに少しずつ違う） ----------
BK = ["X.....x...X.....", "X......x..X..x..", "X..x......X.....", "X.....x..x..X..."]
BS = ["....X.......X...", "....X..o....X.o.", "....X.......Xx..", "..o.X.......X..."]
BH = ["x.xxx.x.x.xxx.x.", "xx.x.xx.x.x.xx.x", "x.x.xxx.x.xxx.x.", "x.xx.x.xx.x.x.xx"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "降り始め" and i >= 8: D.set(b, "X...............", "." * 16, "x...x...x...x..."); continue
    if n in ("本降り", "本降り2"):
        D.set(b, BK[(i * 3) % 4], BS[(i * 5) % 4], BH[(i * 7) % 4])
        if i % 8 == 7:
            D.S[b] = "....X...x.xxXXXX"; D.H[b] = "x.x.x.x........."
        if i % 16 == 0: crash(D, b, "A2", 2)
        continue
    if n == "水たまり": D.set(b, "X.........X.....", "........X.......", "..x...x...x...x."); continue
    if n == "小雨" and i < 8: D.set(b, "X.........X.....", "." * 16, "x...x...x...x..."); continue

S.flags += " --space hall --space-wet 0.16"
S.desc = ("仮: ボカロ曲のインスト25曲の13。エレクトロニカ。F# の陽旋法（1・2・4・5・6）・100。主役の楽器は琴。縁側で聞く雨。"
          "最初の1粒、降り始め、本降り（細かく刻んだくずれたビート）。水たまりに落ちた琴の句が32分で刻まれ、遅れてこだまで返ってくる。"
          "小雨になり、軒からの雫の間が広がって、静けさだけが残る。自作")
S.write()
