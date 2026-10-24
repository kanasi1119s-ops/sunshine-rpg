# vp25 21「しりとり」Word Chain（仮）— J-POP。A長調・136→152（回すたびに少しずつ速く）・4/4。主役の楽器: マリンバ
# 物語: 雨の日、家族でしりとり。マリンバ（わたし）から始まって、母（リード）、父（ピアノ）、兄（ギター）、祖母（弦）、祖父（ベース）へ。
#   回すたびに速くなり、とうとう誰かが「ん」で終わってしまう（一瞬しんとする）。みんなで笑って、最初からもう一度、全員で。
# 形: 旋律のしりとり。前の句の最後の音から次の句が始まり、楽器から楽器へ渡っていく。最後に最初の音に戻って輪になる
# 場面と強さ: 回すたびに少しずつ速く大きく（4小節ずつ→2小節ずつ→1小節ずつ）／「ん」（解決しない音）で無音／もう一度、最初から全員で（最大）
# 旋律の性格: 句の最後の音を長く伸ばし、次の楽器がその音から始める受け渡し
# 崩す所: 句の終わりをわざと解決しない音にする（しりとりの「ん」）
from vp25_lib import *

S = Song("21", "shiritori", "しりとり（仮）", "Word Chain", 136, 4, "A", "major", "J-POP")
S.kit = "naked"
K = S.key
P1 = ["A", "F#m7", "Dmaj7", "E", "C#m7", "F#m7", "Bm7", "E7sus4"]
P2 = ["Dmaj7", "E/D", "C#m7", "F#m7", "Bm7", "C#7", "F#m7", "E"]
S.scene("一回目", 28, "verse", P1 + P2 + P1 + ["A", "A", "E/G#", "E/G#"])
S.scene("二回目", 24, "pre", P2 + P1 + P2)
S.scene("三回目", 24, "chorus", P1 + P2 + P1)
S.scene("ん", 4, "break", ["Bm7", "C#m7", "Dmaj7", "Dmaj7"])
S.scene("もう一度", 48, "chorus", P1 + P2 + P1 + P2 + P1 + P2)
S.scene("輪になる", 20, "outro", P1 + ["Dmaj7", "E", "Dmaj7", "E", "A", "A", "A", "A", "A", "A", "A", "A"])
S.tempo = [{"bar": S.sc("二回目")[0] + 1, "bpm": 142}, {"bar": S.sc("三回目")[0] + 1, "bpm": 148}, {"bar": S.sc("もう一度")[0] + 1, "bpm": 152},
           {"bar": S.sc("輪になる")[8] + 1, "bpm": 152}, {"bar": S.sc("輪になる")[9] + 1, "bpm": 126, "ramp": 8}]
S.extra.update({"tone": "rock", "diGuitar": "emily"})
S.flags = "--bass bnb-loud " + S.flags

VO = {
    "わたし": S.track("主役: マリンバ（わたし）", "marimba", patch="marimba", volume=0.27, pan=-0.1, reverb=0.3, gainDb=6, sustain=1.4),
    "母": S.track("リード（母・歌の役）", "lead", **lead_spec("calliope", vol=0.18, pan=0.15, delay=0.75)),
    "父": S.track("ピアノ（父）", "piano", volume=0.2, pan=-0.3, reverb=0.25, gainDb=3, mono=True),
    "兄": S.track("ギター（兄）", "distGuitar", **lead_gtr_spec(0.14, 0.3)),
    "祖母": S.track("弦（祖母）", "strings", patch="violin", volume=0.2, pan=0.35, reverb=0.35, gainDb=3, mono=True),
    "祖父": S.track("ベース（祖父・旋律）", "bass", **rock_bass_spec(0.22)),
}
ORDER = ["わたし", "母", "父", "兄", "祖母", "祖父"]
RANGE = {"わたし": ("A4", "E6"), "母": ("E4", "A5"), "父": ("C4", "A5"), "兄": ("E4", "A5"), "祖母": ("A4", "E6"), "祖父": ("A1", "E3")}
BASSV = S.track("ベース（伴奏）", "bass", **rock_bass_spec(0.18))
PI = [S.track(f"ピアノの和音{i + 1}", "piano", **piano_spec(0.1, [-0.35, -0.25, -0.15][i])) for i in range(3)]
CL = S.track("クリーンのギター", "guitar", **clean_gtr_spec(0.09, 0.5))
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()


def fit(m, who):
    lo, hi = midi(RANGE[who][0]), midi(RANGE[who][1])
    while m < lo: m += 12
    while m > hi: m -= 12
    return m


# ---------- しりとりの受け渡し（句の最後の音から、次の楽器が始める） ----------
note = midi("A5")
turn = 0
plan = [("一回目", 4), ("二回目", 2), ("三回目", 1)]
seed = 1
for name, L_ in plan:
    bars = S.sc(name)
    if name == "一回目": bars = bars[:24]
    for k in range(0, len(bars), L_):
        who = ORDER[turn % 6]; turn += 1
        seg = bars[k:k + L_]
        st = fit(note, who)
        lo, hi = RANGE[who]
        ts = tones(S.chords[seg[-1]], lo, hi)
        # 終わりの音（次の人の始まりの音）: 和音の音の中から、今の音から離れた所へ（受け渡しで高さが変わる）
        rnd = random.Random(seed); seed += 1
        en = rnd.choice([m for m in ts if 3 <= abs(m - st) <= 9] or ts)
        rhy = "song" if L_ >= 2 else "walk8"
        phr = gen_phrase(S, seg, st, en, rhy=rhy, seed=seed, lo=lo, hi=hi, arch=4 if who != "祖父" else 3)
        for b, s_ in zip(seg, phr): VO[who].bar(b, s_)
        note = en
# 一回目の最後の4小節: 全員の短い間奏（マリンバの和音の分散）
for b in S.sc("一回目")[24:]:
    t = tones(S.chords[b], "A4", "A6")
    VO["わたし"].bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in [0, 2, 4, 2, 1, 3, 5, 3]))
# 「ん」: 解決しない音（D の和音の上の G#＝#11 で止まり、そのまま無音）
nb_ = S.sc("ん")
VO["わたし"].bar(nb_[0], "B5:1 C#6:1 D6:1 E6:1")
VO["わたし"].bar(nb_[1], "F#6:2 G#6:2!")
# もう一度、最初から全員で: 同じ受け渡しを、全員が同じ旋律（ユニゾンとオクターブ）で
HOOK = ["5:1 6:0.5 5:0.5 3:1 1':1", "7:1.5 6:0.5 5:2", "4:1 5:0.5 6:0.5 1':1 6:1", "5:4", "3:1 4:0.5 5:0.5 6:1 5:1", "6:1.5 7:0.5 1':2", "2':1 1':0.5 7:0.5 6:1 4:1", "5:3 R:1",
        "1':1 2':0.5 1':0.5 7:1 5:1", "6:1.5 5:0.5 4:2", "3:1 4:0.5 5:0.5 6:1 1':1", "2':4", "3':1 2':0.5 1':0.5 6:1 5:1", "4:1.5 #5:0.5 7:2", "1':1 7:0.5 6:0.5 5:1 #5:1", "6:3 R:1"]
for i, b in enumerate(S.sc("もう一度")):
    m = HOOK[i % 16]
    VO["わたし"].bar(b, K.mel(m, oct=5 if i >= 16 else 4))
    VO["母"].bar(b, K.mel(m, oct=4))
    if i >= 16: VO["祖母"].bar(b, K.mel(m, oct=5))
    if i >= 32: VO["父"].bar(b, K.mel(m, oct=4))
# 輪になる: 一人ずつ、最初の音へ戻っていく（最後はマリンバの A）
RING = ["わたし", "母", "父", "祖母"]
for i, b in enumerate(S.sc("輪になる")):
    if i < 8:
        who = RING[i // 2]
        if i % 2 == 0:
            lo, hi = RANGE[who]
            phr = gen_phrase(S, [b, b + 1], fit(midi("E5"), who), fit(midi("A5"), who), rhy="long", seed=40 + i, lo=lo, hi=hi)
            VO[who].bar(b, phr[0]); VO[who].bar(b + 1, phr[1])
    elif i == 9: VO["わたし"].bar(b, "E5:2 F#5:2")
    elif i == 11: VO["わたし"].bar(b, "G#5:4")
    elif i == 13: VO["わたし"].bar(b, "A5:4")
    elif i == 16: VO["わたし"].bar(b, "A5:8")

# ---------- 伴奏 ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "ん" and i >= 2: continue
    if n == "輪になる" and i >= 13: continue
    r = low(S.chords[b], "E1")
    if not (n == "一回目" and i < 4):
        BASSV.bar(b, bass_line(S, b, {"一回目": "half", "二回目": "root8", "三回目": "oct8", "ん": "half", "もう一度": "root8", "輪になる": "half"}[n]) if n != "ん" or i < 2 else "R:4")
    v = voice(S.chords[b], 66, 3)
    pat = {"一回目": "X:2 X:2", "二回目": "R:0.5 X:1 R:0.5 X:2", "三回目": "X:0.5 R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:1", "もう一度": "X:1.5 X:1 X:1.5", "輪になる": "X:4", "ん": "X:4"}[n]
    for j in range(3): PI[j].bar(b, pat.replace("X", nm(v[j])))
    if n in ("二回目", "三回目", "もう一度"):
        t = tones(S.chords[b], "E3", "E5")
        CL.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in [0, 2, 1, 3, 2, 4, 3, 1]))
# 祖父の句のときは、伴奏のベースを休む（旋律のベースと重ねない）
for t0, L0, x in list(VO["祖父"].ev):
    b = int(t0 // 4)
    BASSV.ev = [e for e in BASSV.ev if int(e[0] // 4) != b]
cym_swell(CYM, S.sc("もう一度")[0], 2, "C4")

# ---------- ドラム（回すたびに細かく） ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "一回目":
        if i < 4: continue
        put_groove(D, b, ("X.......X.......", "....X.......X...", "x...x...x...x..."), seed=b, hat_vary=False)
    elif n == "二回目": put_groove(D, b, "pop8", ghosts=0.3, seed=b, hat_vary=False)
    elif n == "三回目": put_groove(D, b, "pop16", ghosts=0.5, seed=b, hat_vary=False)
    elif n == "ん":
        if i == 0: D.set(b, "X.......X.......", "....X...X.X.X.X.", "x.x.x.x.x.x.x.x.")
        elif i == 1: D.set(b, "X...............", "X...............", "." * 16)
        continue
    elif n == "もう一度":
        put_groove(D, b, "vocarock", ghosts=0.4, seed=b, hat_vary=False)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
    elif n == "輪になる":
        if i < 8: put_groove(D, b, ("X.......X.......", "....X.......X...", "x...x...x...x..."), seed=b, hat_vary=False)
        continue
    if i % 8 == 7: put_fill(D, b, "small" if not last else "tomdown")

S.desc = ("仮: ボカロ曲のインスト25曲の21。J-POP。A長調。テンポは 136 から、回すたびに 142・148・152 と少しずつ速く。主役の楽器はマリンバ。雨の日の家族のしりとり。"
          "前の句の最後の音から、次の楽器（母＝リード・父＝ピアノ・兄＝ギター・祖母＝弦・祖父＝ベースの旋律）が始める受け渡し。4小節ずつ→2小節ずつ→1小節ずつ。"
          "とうとう「ん」（解決しない G#）で止まって無音。もう一度、最初から全員で。最後は一人ずつ最初の音へ戻り、マリンバの A で輪になる。自作")
S.write()
