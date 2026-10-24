# vp25 05「ひまわり畑の真昼」Sunflower Field at High Noon（仮）— ダンス（ハウス）。A長調・124・4/4。主役の楽器: ピアノ
# 物語: 夜明けのひまわり畑。日が昇るにつれて花が顔を上げ、真昼にいっせいに太陽を向く。午後、夕方と少しずつうつむいて、日が沈む。
# 形: 日の出から日の入りまでの、一つの大きな弧。音の明るさがゆっくり開いて、ゆっくり閉じる（こもった音と開いた音を小節ごとに入れかえる）
# 場面と強さ: 夜明け＝こもって小さい／朝・午前＝だんだん明るく／正午の直前に1小節だけ4つ打ちが止まる／正午＝いちばん明るく長い／
#   午後・夕方＝閉じていく／日没＝キックだけ残ってフェードアウト
# 旋律の性格: ピアノの裏拍の和音（ハウスの刻み）が主役。歌の役は音数の少ない長い音
# 崩す所: 正午の直前に1小節だけ4つ打ちを止める（真上の太陽で、時間が止まる）
from vp25_lib import *

S = Song("05", "himawari", "ひまわり畑の真昼（仮）", "Sunflower Field at High Noon", 124, 4, "A", "major", "ダンス（ハウス）")
K = S.key
MORN = ["Amaj7", "Bm7/A", "C#m7", "Dmaj7"]
NOON = ["Amaj7", "G/A", "Dmaj7", "Dm6", "Amaj7", "C#7", "F#m7", "Bm7"]
AFT = ["Bm7", "C#m7", "Dmaj7", "E"]
EVE = ["Dmaj7", "Dm6", "Amaj7", "Amaj7"]
S.scene("夜明け", 8, "intro", ["Amaj7", "Amaj7", "Bm7/A", "Bm7/A"])
S.scene("朝", 24, "verse", MORN)
S.scene("午前", 24, "pre", MORN[:2] + ["F#m7", "E"] + MORN)
S.scene("止まる", 1, "break", ["E7sus4"])
S.scene("正午", 32, "chorus", NOON)
S.scene("午後", 24, "verse", AFT)
S.scene("夕方", 16, "bridge", EVE)
S.scene("日没", 9, "outro", ["Amaj7"] * 9)

# 太陽の高さ（0〜1）: 小節ごと
SUN = []
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    v = {"夜明け": 0.0 + 0.1 * i / L, "朝": 0.1 + 0.3 * i / L, "午前": 0.4 + 0.4 * i / L, "止まる": 0.85, "正午": 1.0,
         "午後": 1.0 - 0.35 * i / L, "夕方": 0.6 - 0.45 * i / L, "日没": 0.15 - 0.15 * i / L}[n]
    SUN.append(round(max(0.0, min(1.0, v)), 3))
OPEN = [round(0.15 + 0.85 * s, 3) for s in SUN]
DARK = [round(1.0 - 0.85 * s, 3) for s in SUN]

PI_FX = [{"type": "eq", "low": -4, "mid": -4, "midHz": 400, "high": 2}, {"type": "compressor", "threshold": -18, "ratio": 3, "attack": 0.003, "release": 0.1}]
PI_DARK = [{"type": "filter", "kind": "lowpass", "freq": 1200, "q": 0.8}, {"type": "eq", "low": -4, "mid": -4, "midHz": 400, "high": 0}]
PR = [S.track(f"主役: ピアノ（右手{i + 1}・開いた音）", "piano", volume=0.15, pan=[-0.15, 0.05, 0.2][i], reverb=0.22, gainDb=4, barGain=OPEN, fx=PI_FX) for i in range(3)]
PL = S.track("主役: ピアノ（左手）", "piano", volume=0.15, pan=-0.05, reverb=0.2, gainDb=3, barGain=OPEN, fx=PI_FX)
PD = [S.track(f"ピアノ（こもった音{i + 1}）", "piano", volume=0.15, pan=[-0.15, 0.05, 0.2][i], reverb=0.3, gainDb=3, barGain=DARK, fx=PI_DARK) for i in range(3)]
LEAD = S.track("リード（歌の役）", "lead", **lead_spec("calliope", vol=0.17, pan=0.0, delay=0.75,
                                                      extra_fx=[{"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.7}]))
BASS = S.track("シンセベース", "bass", **synth_bass_spec("synthBass1", vol=0.21, duck=0.35))
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("warmPad", vol=0.06, pan=[-0.55, 0.55, 0][i], duck=0.3)) for i in range(3)]
STR = [S.track(f"弦{i + 1}", "strings", patch="slowStrings", **strings_spec(vol=0.07, pan=[-0.6, 0.6][i])) for i in range(2)]
ARP = S.track("ガラスのアルペジオ", "pad", **pluck_spec("glassPluck", vol=0.07, pan=0.45, delay=0.75, sustain=0.9))
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()

# ---------- ピアノ: ハウスの裏拍の和音（右手3声）＋左手のオクターブ ----------
STAB_PATS = ["R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5", "R:0.5 X:0.5 R:0.5 X:0.75 X:0.25 R:0.5 X:0.5 R:0.5", "X:0.75 X:0.75 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5",
             "R:0.5 X:0.5 R:0.25 X:0.25 R:0.5 X:0.5 R:0.5 X:0.75 X:0.25"]
cv = chord_voices(S, range(S.nb), center=66, n=3)
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    v = cv[b]
    if n == "夜明け": pat = "X:4"
    elif n in ("朝",): pat = STAB_PATS[0] if i % 4 != 3 else STAB_PATS[1]
    elif n == "止まる": pat = "X:4"
    elif n == "正午": pat = STAB_PATS[(i // 2) % 4]
    elif n in ("午前", "午後"): pat = STAB_PATS[i % 2 * 2]
    elif n == "夕方": pat = STAB_PATS[0] if i < 8 else "X:2 X:2"
    else: pat = "X:4" if i < 4 else "R:4"
    for j in range(3):
        PR[j].bar(b, pat.replace("X", nm(v[j])))
        PD[j].bar(b, pat.replace("X", nm(v[j])))
    r = low(S.chords[b], "E2")
    if n in ("正午", "午前"):
        PL.bar(b, f"{nm(r)}:1 {nm(r + 12)}:0.5 {nm(r)}:0.5 R:0.5 {nm(r + 7)}:0.5 {nm(r + 12)}:1")
    elif n in ("朝", "午後"):
        PL.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2")
    elif n in ("夜明け", "夕方", "止まる"):
        PL.bar(b, f"{nm(r)}:4")

# ---------- 歌の役: 音数の少ない長い音 ----------
MA = ["R:4", "R:2 3:2", "5:3 3:1", "2:4", "R:2 1:1 2:1", "3:4", "2:2 7,:2", "1:4"]
MB = ["R:1 5:1 6:1 1':1", "7:3 6:1", "5:2 3:2", "4:4", "R:1 5:1 6:1 2':1", "1':3 7:1", "6:2 5:1 4:1", "5:4"]
HOOK = ["3':3 2':0.5 1':0.5", "2':4", "1':2 7:1 6:1", "6:2 4:2", "3':3 2':0.5 1':0.5", "5':2 #4':2", "3':2 2':1 1':1", "2':2 R:2",
        "3':3 5':1", "5':2 4':2", "6':2 5':1 3':1", "4':2 6:2", "1':1 2':1 3':1 5':1", "#5':2 7':2", "6':3 5':1", "5':4"]
AFTM = ["R:2 4:1 5:1", "6:4", "R:2 6:1 7:1", "1':4", "R:2 1':1 2':1", "3':4", "2':2 1':2", "7:4"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "朝" and i >= 8: LEAD.bar(b, K.mel(MA[i % 8], oct=5))
    if n == "午前": LEAD.bar(b, K.mel(MB[i % 8], oct=5))
    if n == "正午": LEAD.bar(b, K.mel(HOOK[i % 16], oct=4 if i < 16 else 5))
    if n == "午後" and i < 16: LEAD.bar(b, K.mel(AFTM[i % 8], oct=5))
    if n == "夕方" and i < 8: LEAD.bar(b, K.mel(["3:4", "4:4", "3:2 2:2", "1:4", "R:4", "R:4", "5,:4", "R:4"][i], oct=5))

# ---------- ベース（ハウスの裏の音） ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "夜明け" or n == "止まる": continue
    if n == "日没": continue
    if n == "朝" and i < 8: BASS.bar(b, f"{nm(low(S.chords[b]))}:4"); continue
    if n == "正午": BASS.bar(b, bass_line(S, b, "house") if i % 4 != 3 else bass_line(S, b, "push")); continue
    if n == "夕方" and i >= 8: BASS.bar(b, f"{nm(low(S.chords[b]))}:4" if i % 2 == 0 else "R:4"); continue
    BASS.bar(b, bass_line(S, b, "house"))

# ---------- パッド・弦・アルペジオ ----------
pv = chord_voices(S, range(S.nb), center=57, n=3)
sv = chord_voices(S, range(S.nb), center=69, n=2)
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n in ("夜明け", "朝", "夕方", "日没", "止まる") and not (n == "日没" and i > 4):
        for j in range(3): PAD[j].bar(b, f"{nm(pv[b][j])}:4")
    if n in ("正午", "午前") and not (n == "午前" and i < 12):
        for j in range(2): STR[j].bar(b, f"{nm(sv[b][j])}:4")
    if n == "正午" and i >= 8:
        t = tones(S.chords[b], "E5", "E7")
        ARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" for q in [0, 2, 4, 2, 1, 3, 5, 3, 2, 4, 6, 4, 3, 5, 4, 2]))

cym_swell(CYM, S.sc("正午")[0], 4, "E4"); cym_swell(CYM, S.sc("午前")[0], 2, "C4")

# ---------- ドラム（4つ打ち。正午の直前の1小節だけ止まる） ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "夜明け": continue
    if n == "止まる": D.set(b, "." * 16, "." * 16, "." * 16); continue
    if n == "朝":
        put_groove(D, b, ("X...X...X...X...", "................" if i < 8 else "....X.......X...", "................" if i < 4 else "..x...x...x...x."), seed=b, hat_vary=False)
        if i % 8 == 7 and i >= 8: put_fill(D, b, "small")
        continue
    if n == "午前":
        put_groove(D, b, ("X...X...X...X...", "....X.......X...", "..O...O...O...O." if i >= 8 else "xxOxxxOxxxOxxxOx".replace("O", "x")), ghosts=0.2, seed=b, hat_vary=False)
        if i == 0: crash(D, b, "G2")
        if i == 23: put_fill(D, b, "build")
        continue
    if n == "正午":
        put_groove(D, b, ("X...X...X...X...", "....X.......X...", "x.O.x.O.x.O.x.O."), ghosts=0.3, seed=b, hat_vary=False)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7: put_fill(D, b, "snare16" if i % 16 == 15 else "small")
        continue
    if n == "午後":
        put_groove(D, b, ("X...X...X...X...", "....X.......X...", "..x...x...x...x."), seed=b, hat_vary=False)
        if i == 0: D.cym(b, "D2:4")
        if i % 8 == 7: put_fill(D, b, "small")
        continue
    if n == "夕方":
        put_groove(D, b, ("X...X...X...X...", "................", "..x...x...x...x." if i < 8 else "................"), seed=b, hat_vary=False)
        continue
    if n == "日没":
        D.set(b, "X...X...X...X..." if i < 8 else "X...............", "." * 16, "." * 16)

S.fade_out = 12
S.flags += " --space hall --space-wet 0.12"
S.desc = ("仮: ボカロ曲のインスト25曲の05。ハウス。A長調・124。主役の楽器はピアノ（裏拍の和音の刻み）。ひまわり畑の一日。"
          "こもったピアノと開いたピアノを小節ごとに入れかえて、日が昇るほど音が明るく開き、日が傾くほど閉じる一つの大きな弧。"
          "正午の直前に1小節だけ4つ打ちが止まる。最後はキックだけ残ってフェードアウト。自作")
S.write()
