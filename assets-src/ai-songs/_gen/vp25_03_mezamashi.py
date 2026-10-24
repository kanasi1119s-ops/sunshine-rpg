# vp25 03「目覚まし三段構え」Three Alarms Deep（仮）— テクノポップ。G長調・140・4/4。主役の楽器: FMベル
# 物語: 目覚まし時計が3つ。1つ目で起きかけて二度寝の夢（雲の上）、2つ目でまた二度寝（今度は空を飛ぶ夢）、3つ目で飛び起きて、
#   歯みがき・着替え・トースト・靴と、全力で支度して玄関を飛び出す。
# 形: 目覚まし→夢→目覚まし→夢→3つ目で飛び起き→全力の支度（最後まで止まらない）
# 場面と強さ: ベル＝鋭く大きい一瞬（3回とも少しずつ大きく）／夢＝ふわっと静か（ドラムなし、半分の速さに感じる）／支度＝最後まで最大
# 旋律の性格: ベルは同じ音の16分の連打。夢は高い所の長いレガート。支度は階段を駆け上がる8分
# 崩す所: 夢の場面は、テンポはそのままで、和音と旋律を2倍に引き延ばして「半分の速さ」に聞かせる
from vp25_lib import *

S = Song("03", "mezamashi", "目覚まし三段構え（仮）", "Three Alarms Deep", 140, 4, "G", "major", "テクノポップ")
K = S.key
BELL = ["G", "G", "C/G", "D/G"]
DREAM1 = ["Cmaj7#11", "Cmaj7#11", "G/B", "G/B", "Am7", "Am7", "D7sus4", "D7sus4"]
DREAM2 = ["Em7", "Em7", "Cmaj7", "Cmaj7", "Am7", "Am7", "Bm7", "E7"]
RUN = ["G", "Am7", "Bm7", "Cmaj7", "D", "Em7", "F", "D7sus4"]
RUN_A = [tr_chord(c, 2) for c in RUN]

S.scene("ベル1", 8, "intro", BELL)
S.scene("夢1", 24, "verse", DREAM1)
S.scene("ベル2", 8, "break", BELL)
S.scene("夢2", 28, "bridge", DREAM2 + DREAM2 + DREAM2[:4] + ["Bm7", "Bm7", "D7sus4", "D7"] + DREAM2[:4] + ["C", "C", "D", "D"])
S.scene("ベル3", 10, "break", BELL + BELL + ["D", "D"])
S.scene("歯みがき", 16, "chorus", RUN)
S.scene("着替え", 16, "verse", RUN)
S.scene("トースト", 16, "pre", ["Cmaj7", "Bm7", "Am7", "D7"] * 4)
S.scene("靴", 24, "chorus", RUN_A + RUN_A + RUN_A[:6] + ["E", "E"])
KA = K.up(2)

BELLP = S.track("主役: FMベル（目覚まし）", "fmBell", volume=0.24, pan=0.0, reverb=0.25, sustain=0.9, gainDb=4,
                fx=[{"type": "eq", "low": -4, "mid": 2, "midHz": 2600, "high": 0}])
# 2026-10-25: 10秒ごとの PQ で、目覚ましの場面だけ 5.5〜6.9 と低かった（高いベルの16分の連打が耳に痛い）。
#   目覚ましは別のパートにして、小さく・高い所を丸く・連打をまばらにする
ALARM = S.track("目覚ましのベル", "fmBell", volume=0.14, pan=0.1, reverb=0.3, sustain=0.8, gainDb=1,
                fx=[{"type": "filter", "kind": "lowpass", "freq": 5000, "q": 0.7}, {"type": "eq", "low": -4, "mid": 1, "midHz": 2000, "high": -2}])
BELLD = S.track("FMベル（夢の中のきらめき）", "fmBell", volume=0.16, pan=-0.35, reverb=0.45, sustain=2.0, gainDb=2,
                fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.22, "feedback": 0.35}])
LEADD = S.track("リード（夢の歌）", "lead", **lead_spec("calliope", vol=0.19, pan=0.05, delay=1.0))
LEADW = S.track("リード（起きてからの歌）", "lead", **lead_spec("chiff", vol=0.19, pan=-0.05, delay=0.5))
BASS = S.track("シンセベース", "bass", **synth_bass_spec("synthBass1", vol=0.22, duck=0.2))
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("newAge", vol=0.06, pan=[-0.55, 0.55, 0][i])) for i in range(3)]
ARP = S.track("ガラスのアルペジオ", "pad", **pluck_spec("glassPluck", vol=0.08, pan=0.4, delay=0.75, sustain=1.0))
STAB = [S.track(f"刻み{i + 1}", "pad", **pluck_spec("polysynth", vol=0.06, pan=[-0.45, 0.45, 0][i], delay=0.5, sustain=0.3)) for i in range(3)]
FX = S.track("効果音（ライザー）", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()

# ---------- ベル（同じ音の16分の連打。3回とも少しずつ形が詰まる） ----------
def ring(b, top, n_burst):
    """1小節に n_burst 回の「チリッ」（各 1拍＝16分2つと休み）"""
    toks = []
    for k in range(4):
        if k < n_burst: toks.append(f"{top}:0.25! {top}:0.25 R:0.5")
        else: toks.append("R:1")
    return " ".join(toks)


for sc_, tops, lv in (("ベル1", ["D6", "D6", "E6", "D6"], 2), ("ベル2", ["D6", "E6", "F#6", "G6"], 3), ("ベル3", ["G6", "G6", "A6", "B6"], 4)):
    for i, b in enumerate(S.sc(sc_)):
        if sc_ == "ベル1" and i == 0: BELLP.bar(b, "R:1 D6:3!"); continue                  # 無音（1拍）のあとの一撃
        if i >= 8: ALARM.bar(b, ring(b, "D6", 4) if i == 8 else "D6:0.25! D6:0.25 R:3.5"); continue
        ALARM.bar(b, ring(b, tops[i % 4], lv if i % 2 == 0 else lv - 1))

# ---------- 夢: 和音と旋律を2倍に引き延ばす（半分の速さに聞こえる）。高い所の長いレガート ----------
DM1 = ["3':4", "2':2 1':2", "7:3 5:1", "7:2 1':2", "1':4", "6:2 7:2", "1':4", "6:2 R:2",
       "#4':4", "3':2 2':2", "2':3 1':1", "7:2 5:2", "3':4", "1':2 2':2", "2':4", "R:4",
       "3':2 5':2", "#4':2 3':2", "2':3 7:1", "1':2 2':2", "3':4", "2':2 1':2", "1':4", "R:4"]
for i, b in enumerate(S.sc("夢1")):
    if i < 4: continue
    LEADD.bar(b, K.mel(DM1[i - 4] if i - 4 < len(DM1) else "R:4", oct=5))
DM2 = ["5':4", "4':2 3':2", "3':4", "3':4", "1':4", "7:2 6:2", "#4':4", "b7':2 #5':2",
       "5':3 3':1", "2':4", "3':2 5':2", "5':4", "6':3 5':1", "3':4", "4':2 3':2", "2':4",
       "5':3 6':1", "5':2 3':2", "2':4", "3':2 5':2", "1'':4", "7':2 6':2", "5':4", "R:4"]
for i, b in enumerate(S.sc("夢2")):
    if i < 4: continue
    LEADD.bar(b, K.mel(DM2[i - 4], oct=4))
# 夢のきらめき: ベルが4拍ごとに1音（ディレイで空に散る）
for b in S.sc("夢1") + S.sc("夢2"):
    t = tones(S.chords[b], "G5", "G6")
    BELLD.bar(b, f"{nm(t[(b * 2) % len(t)])}:2 {nm(t[(b * 2 + 1) % len(t)])}:2" if b % 2 == 0 else f"{nm(t[-1])}:4")
for i, b in enumerate(S.sc("夢2")):
    if i >= 12:
        t = tones(S.chords[b], "B4", "B6")
        ARP.bar(b, " ".join(f"{nm(t[k % len(t)])}:0.5" for k in [0, 2, 4, 3, 1, 3, 5, 2]))

# ---------- 支度: 階段を駆け上がる8分 ----------
RUNM = ["1:0.5 2:0.5 3:0.5 5:0.5 6:1 5:0.5 3:0.5", "R:0.5 1:0.5 2:0.5 3:0.5 4:1 3:0.5 1:0.5", "2:0.5 3:0.5 4:0.5 6:0.5 7:1 6:0.5 4:0.5", "3:1.5 2:0.5 3:1 5:1",
        "6:0.5 5:0.5 6:0.5 1':0.5 2':1 1':0.5 6:0.5", "7:1 6:0.5 5:0.5 3:1 5:1", "b7:1.5 6:0.5 4:1 b7:1", "5:3 R:1"]
RUNM2 = ["5:0.5 6:0.5 7:0.5 2':0.5 3':1 2':0.5 7:0.5", "R:0.5 1':0.5 7:0.5 6:0.5 5:1 6:0.5 1':0.5", "2':0.5 1':0.5 7:0.5 6:0.5 5:1 6:0.5 7:0.5", "1':2 7:1 5:1",
         "6:0.5 7:0.5 1':0.5 2':0.5 3':1 2':0.5 1':0.5", "7:1 1':0.5 2':0.5 3':1 2':1", "1':1.5 b7:0.5 6:1 4:1", "5:2 R:2"]
for i, b in enumerate(S.sc("歯みがき")): LEADW.bar(b, K.mel(RUNM[i % 8] if i < 8 else RUNM2[i % 8]))
# 着替え: 歌は休み、ベルが主役（ボタンを留めるような短い音型）
for i, b in enumerate(S.sc("着替え")):
    t = tones(S.chords[b], "G5", "G6")
    BELLP.bar(b, " ".join(f"{nm(t[k % len(t)])}:0.5{'!' if k == 0 else ''}" for k in [0, 1, 2, 1, 3, 2, 1, 0]) if i % 2 == 0 else
              f"{nm(t[2])}:1 {nm(t[1])}:1 {nm(t[0])}:2")
    if i >= 8: LEADW.bar(b, K.mel(["3':2 2':2", "1':4", "7:2 6:2", "5:4", "6:2 7:2", "1':2 2':2", "b7':2 6':2", "5':4"][i - 8], oct=4))
# トースト: 「チン！」（ベルの高い1音）と、跳ねる歌
TOAST = ["3:0.5 5:0.5 R:0.5 3:0.5 2:1 1:1", "7,:0.5 2:0.5 R:0.5 7,:0.5 6,:1 5,:1", "6,:0.5 1:0.5 R:0.5 3:0.5 5:1 4:0.5 3:0.5", "2:2 R:2"]
for i, b in enumerate(S.sc("トースト")):
    LEADW.bar(b, K.mel(TOAST[i % 4] if i < 8 else seq_up(TOAST[i % 4], K, 2)))
    if i % 4 == 3: BELLP.bar(b, "R:2 G6:2!")
# 靴: A長調で、歯みがきの歌を高く
for i, b in enumerate(S.sc("靴")):
    m = (RUNM2 if i < 8 else RUNM if i < 16 else RUNM2)[i % 8]
    if i >= 22: m = ["1':4!", "1':1 R:3"][i - 22]
    LEADW.bar(b, KA.mel(m, oct=5 if i < 16 else 5))
    t = tones(S.chords[b], "A5", "A6")
    if i < 22: BELLP.bar(b, " ".join(f"{nm(t[k % len(t)])}:0.5" for k in [0, 1, 2, 1]) + " R:2")
BELLP.bar(S.sc("靴")[-1], "A6:0.25! A6:0.25 A6:0.25 A6:0.25 R:3")

# ---------- ベース ----------
for b in range(S.nb):
    n, i, L, kind = S.scene_of(b)
    if n.startswith("ベル"):
        if n == "ベル1" and i == 0: continue
        BASS.bar(b, bass_line(S, b, "oct8" if i < 8 else "long")); continue
    if n.startswith("夢"):
        if i < 4: continue
        BASS.bar(b, f"{nm(low(S.chords[b]))}:4" if i % 2 == 0 else "R:4"); continue
    if n in ("歯みがき", "靴"): BASS.bar(b, bass_line(S, b, "oct8" if i % 4 != 3 else "root8")); continue
    if n == "着替え": BASS.bar(b, bass_line(S, b, "push")); continue
    if n == "トースト": BASS.bar(b, bass_line(S, b, "walk")); continue
BASS.bar(S.sc("靴")[-1], "E1:0.25! R:3.75")

# ---------- 和音 ----------
pv = chord_voices(S, range(S.nb), center=59, n=3)
for b in range(S.nb):
    n, i, L, kind = S.scene_of(b)
    if n.startswith("夢") or n == "着替え":
        for j in range(3): PAD[j].bar(b, f"{nm(pv[b][j])}:4")
    if n in ("歯みがき", "靴", "トースト"):
        v = voice(S.chords[b], 66, 3)
        pat = "R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5" if n != "トースト" else "X:0.5 R:1 X:0.5 R:1 X:1"
        if n == "靴" and i >= 23: continue
        for j in range(3): STAB[j].bar(b, pat.replace("X", nm(v[j])))
for b in S.sc("歯みがき")[8:] + S.sc("靴")[:22]:
    t = tones(S.chords[b], "D5", "D7")
    ARP.bar(b, " ".join(f"{nm(t[k % len(t)])}:0.25" for k in [0, 1, 2, 3, 4, 3, 2, 1, 0, 2, 4, 5, 4, 2, 1, 3]))

for b in (S.sc("歯みがき")[0], S.sc("靴")[0]): riser(FX, b, 4, "C4"); cym_swell(CYM, b, 2, "C4")
cym_swell(CYM, S.sc("夢1")[0], 4, "E4"); cym_swell(CYM, S.sc("夢2")[0], 4, "E4")

# ---------- ドラム ----------
for b in range(S.nb):
    n, i, L, kind = S.scene_of(b)
    last = i == L - 1
    if n.startswith("ベル"):
        if n == "ベル1" and i == 0: D.set(b, "....X...........", "....X...........", "................"); continue
        if i >= 8:
            D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16)
            if i == 8: crash(D, b, "C2"); D.cym(b, "R:4")
            continue
        put_groove(D, b, ("X...X...X...X...", "....X.......X...", "x.x.x.x.x.x.x.x."), seed=b)
        if i == 0 or (n == "ベル1" and i == 1): crash(D, b)
        if i == 7: stop(D, b)       # 目覚ましを止める（バン）
        continue
    if n.startswith("夢"):
        if n == "夢2" and i >= 16:
            D.set(b, "X.........X.....", "........x.......", "x...x...x...x...")    # 夢の終わりが近づくと、遠くで足音
        continue
    if n == "歯みがき":
        put_groove(D, b, ("X...X...X...X...", "....X.......X...", "xoxoxoxoxoxoxoxo"), ghosts=0.4, seed=b)
        if i % 8 == 0: crash(D, b)
        if i % 8 == 7: put_fill(D, b, "snare16")
        continue
    if n == "着替え":
        put_groove(D, b, "pop16", ghosts=0.5, seed=b)
        if i == 0: crash(D, b, "G2")
        if i % 4 == 3: put_fill(D, b, "small" if i != 15 else "tomdown")
        continue
    if n == "トースト":
        put_groove(D, b, ("X..X..X.X.......", "....X.......X...", "x.x.x.x.x.x.x.x."), ghosts=0.3, seed=b)
        if i % 4 == 3: D.cym(b, "R:2 A2:2")
        if last: put_fill(D, b, "build")
        continue
    if n == "靴":
        put_groove(D, b, ("X...X...X...X...", "....X.......X...", "XoxoXoxoXoxoXoxo"), ghosts=0.5, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and i < 22: put_fill(D, b, "tomdown")
        if i == 22: D.set(b, "X...X...X...X...", "....X...X.X.XXXX", "x.x.x.x.........");
        if i == 23: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 1)
        continue

S.flags += " --space room --space-wet 0.1"
S.desc = ("仮: ボカロ曲のインスト25曲の03。テクノポップ。G長調（最後の支度で A長調）・140。主役の楽器はFMベル。目覚まし→二度寝の夢→目覚まし→夢→3つ目で飛び起き、"
          "歯みがき・着替え・トースト・靴と全力の支度で玄関を飛び出す（最後はカットアウト）。ベルは同じ音の16分の連打、夢は和音と旋律を2倍に引き延ばして半分の速さに聞かせる。自作")
S.write()
