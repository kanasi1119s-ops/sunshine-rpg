# vp25 06「シャボン玉工場」The Soap Bubble Factory（仮）— ダンス（フューチャーベース）。F長調・150（半分の速さで感じる）・4/4。主役の楽器: ガラスのプラック
# 物語: 町はずれの小さなシャボン玉工場。機械がふうっと玉を膨らませては、ぱちんと割れる。昼にはたくさんの小さな玉が窓から飛び出す。
#   夕方、いちばん大きな玉が膨らみ…最後の1個だけは割れずに、空の上へ上っていく。
# 形: 膨らむ→割れる、のくり返し。最後の1個だけは割れずに空へ
# 場面と強さ: 膨らむ＝だんだん（スネアが細かく、音が上がる）／割れる＝はじける最大、でもすぐ空っぽ（1小節の空白）／
#   たくさんの玉＝小さな粒が左右に散る（ドラムなし）／最後＝膨らむだけ膨らんで、割れずに無音へ
# 旋律の性格: 音程が上がる厚い和音の刻み、跳ねる3連の短い句（ガラスのプラックが「はじける」旋律）
# 崩す所: 最後のドロップを鳴らさない（割れないシャボン玉）
from vp25_lib import *

S = Song("06", "shabon", "シャボン玉工場（仮）", "The Soap Bubble Factory", 150, 4, "F", "major", "ダンス（フューチャーベース）")
K = S.key
DROP = ["Dm9", "Bbmaj7", "Fmaj7/A", "Gm9", "Dm9", "Bbmaj7", "Ebmaj7", "C7sus4"]
VERSE = ["Fmaj7", "Am7", "Bbmaj7", "C", "Fmaj7", "Am7", "Gm7", "Csus4"]
BUILD = ["Bbmaj7", "C", "Dm7", "Ebmaj7"]
BUB = ["Dbmaj7", "Ebmaj7", "Fmaj7", "Fmaj7"]
S.scene("はじけ", 4, "intro", DROP[:4])
S.scene("工場の朝", 20, "verse", VERSE)
S.scene("膨らむ1", 8, "pre", BUILD)
S.scene("割れる1", 16, "chorus", DROP)
S.scene("空っぽ", 4, "break", ["Bbmaj7", "Bbmaj7", "C", "C"])
S.scene("工場の昼", 16, "verse", VERSE)
S.scene("膨らむ2", 8, "pre", BUILD)
S.scene("割れる2", 16, "chorus", DROP)
S.scene("たくさんの玉", 20, "bridge", BUB)
S.scene("膨らむ3", 16, "pre", BUILD)
S.scene("割れる3", 16, "chorus", DROP)
S.scene("最後の一個", 16, "outro", BUILD + ["Bbmaj7", "C", "Dm7", "Ebmaj7", "Fmaj7", "Fmaj7", "Fmaj7", "Fmaj7"] + ["Fmaj7"] * 4)

T3 = "0.3333"; T3b = "0.3334"
GP = S.track("主役: ガラスのプラック（はじける旋律）", "pad", patch="glassPluck", volume=0.17, pan=0.0, sustain=0.9, reverb=0.3, gainDb=5,
             fx=[{"type": "filter", "kind": "highpass", "freq": 300, "q": 0.7}, {"type": "eq", "low": 0, "mid": 2, "midHz": 3000, "high": 1},
                 {"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
GP2 = S.track("ガラスのプラック（小さな玉）", "pad", patch="glassPluck", volume=0.11, pan=0.6, sustain=1.2, reverb=0.45, gainDb=2,
              fx=[{"type": "filter", "kind": "highpass", "freq": 400, "q": 0.7}, {"type": "pingpong", "beats": 1.0, "mix": 0.3, "feedback": 0.4}])
LEAD = S.track("リード（歌の役）", "lead", **lead_spec("squareLead", vol=0.18, pan=-0.05, delay=0.75))
SAW = [S.track(f"厚い和音{i + 1}", "pad", **pad_spec("supersawPad", vol=0.07, pan=[-0.55, 0.55, -0.2, 0.2][i], duck=0.55, sustain=0.9)) for i in range(4)]
SUB = S.track("808（重低音）", "sub808", **sub_spec(0.24))
BASS = S.track("シンセベース（うなり）", "bass", **synth_bass_spec("synthBass2", vol=0.12, duck=0.5))
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("halo", vol=0.06, pan=[-0.5, 0.5, 0][i], duck=0.3)) for i in range(3)]
FX = S.track("効果音（ライザー）", "pad", patch="fxRiser", volume=0.08, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()

# ---------- ドロップの旋律（ガラスのプラック）: 跳ねる3連と、はじける高い音 ----------
DH = [f"5:{T3} 6:{T3} 1':{T3b} 5:1 R:0.5 3:0.5 5:1", f"4:{T3} 5:{T3} 6:{T3b} 2':1.5 1':0.5 6:1", f"R:0.5 1':0.5 3':{T3} 2':{T3} 1':{T3b} 7:0.5 1':1.5", "5:1 4:1 2:1 R:1",
      f"5:{T3} 6:{T3} 1':{T3b} 5':1 R:0.5 3':0.5 5':1", f"4':{T3} 2':{T3} 1':{T3b} 2':1 R:0.5 6:0.5 1':1", f"b7:{T3} 1':{T3} 2':{T3b} b3':1.5 2':0.5 1':1", "2':2 R:2"]
DH2 = DH[:4] + [f"1':{T3} 2':{T3} 3':{T3b} 5':1 R:0.5 6':0.5 5':1", f"4':{T3} 5':{T3} 6':{T3b} 5':1 R:0.5 4':0.5 2':1",
                f"b3':{T3} 4':{T3} 5':{T3b} b7':1 R:0.5 5':0.5 4':0.5 b3':0.5", "2':1 5:1 2':1 R:1"]
for sc_, hook in (("割れる1", DH + DH), ("割れる2", DH + DH2), ("割れる3", DH2 + DH2)):
    for i, b in enumerate(S.sc(sc_)): GP.bar(b, K.mel(hook[i], oct=4))
for i, b in enumerate(S.sc("はじけ")): GP.bar(b, K.mel(DH[i], oct=4))

# ---------- 歌の役（工場の朝・昼）: 半分の速さに感じる、ゆったりした句 ----------
VA = ["R:1 3:1 5:1 6:1", "5:2 3:1 2:1", "R:1 4:1 6:1 1':1", "7:2 5:2", "R:1 3:1 5:1 6:1", "1':2 7:1 5:1", "4:1.5 5:0.5 6:1 5:1", "5:3 R:1",
      "R:1 1':1 7:1 6:1", "5:2 3:2", "R:1 4:1 5:1 6:1", "1':2 2':2", "R:1 3':1 2':1 1':1", "7:2 5:1 3:1", "4:2 5:1 6:1", "5:4"]
VB = ["R:0.5 3:0.5 5:1 6:1 5:1", "3:1.5 2:0.5 1:2", "R:0.5 4:0.5 6:1 1':1 6:1", "5:4", "R:0.5 3:0.5 5:1 1':1 7:1", "6:1.5 5:0.5 3:2",
      "R:0.5 2:0.5 4:1 5:1 4:1", "5:4", "R:0.5 5:0.5 6:1 1':1 2':1", "3':2 2':1 1':1", "R:0.5 6:0.5 1':1 2':1 1':1", "6:4",
      "R:0.5 3':0.5 2':1 1':1 6:1", "5:1.5 3:0.5 5:2", "4:1 6:1 1':1 2':1", "1':4"]
for i, b in enumerate(S.sc("工場の朝")):
    if i >= 4: LEAD.bar(b, K.mel(VA[(i - 4) % 16], oct=4))
for i, b in enumerate(S.sc("工場の昼")): LEAD.bar(b, K.mel(VB[i], oct=4))
BUILDM = ["1:2 2:2", "3:2 4:2", "5:2 6:2", "b7:2 1':2", "1':1 2':1 3':1 4':1", "5':4", "R:4", "R:4"]
for sc_ in ("膨らむ1", "膨らむ2"):
    for i, b in enumerate(S.sc(sc_)): LEAD.bar(b, K.mel(BUILDM[i], oct=4))
for i, b in enumerate(S.sc("膨らむ3")):
    LEAD.bar(b, K.mel(["1:4", "2:4", "3:4", "b3:4", "4:4", "5:4", "6:4", "b7:4", "1':2 2':2", "3':2 4':2", "5':4", "R:4", "R:4", "R:4", "R:4", "R:4"][i], oct=4))
# 最後の一個: 膨らんで、割れずに上っていく（ガラスのプラックが高い所へ、間をあけて）
LAST = ["1':2 2':2", "3':2 4':2", "5':2 6':2", "b7':2 1'':2", "R:4", "R:4", "R:4", "R:4",
        "5':4", "R:4", "1'':4", "R:4", "3'':4", "R:4", "R:4", "R:4"]
for i, b in enumerate(S.sc("最後の一個")):
    GP.bar(b, K.mel(LAST[i], oct=4) if i < 8 else K.mel(LAST[i], oct=4))

# 小さな玉（たくさんの玉・工場の朝の前半）: 左右に散る粒
rnd = random.Random(6)
for b in S.sc("たくさんの玉") + S.sc("工場の朝")[:4]:
    t = tones(S.chords[b], "C6", "C7")
    toks = []
    for q in range(8):
        toks.append(f"{nm(rnd.choice(t))}:0.5" if rnd.random() < (0.45 if b in S.sc("たくさんの玉") else 0.35) else "R:0.5")
    GP2.bar(b, merge_rests(" ".join(toks)))

# ---------- 厚い和音: ドロップでは和音の刻み（ドラムに合わせて）、膨らむでは伸ばす ----------
CHOP = ["X:0.75 X:0.75 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5", "X:0.5 R:0.25 X:0.25 R:0.5 X:0.5 R:0.5 X:1 X:0.5", "X:0.75 X:0.75 X:0.5 X:0.5 X:0.5 R:1"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    v = voice(S.chords[b], 64, 4)
    if n.startswith("割れる") or n == "はじけ":
        pat = CHOP[i % 3] if n != "はじけ" else CHOP[0]
        if n.startswith("割れる") and i == L - 1: pat = "X:1 R:3"           # 割れたあと、すぐ空っぽ
    elif n.startswith("膨らむ"):
        pat = "X:4" if i < L - 2 else ("X:0.5 X:0.5 X:0.5 X:0.5 X:0.25 X:0.25 X:0.25 X:0.25 X:0.25 X:0.25 X:0.25 X:0.25" if i == L - 2 else "R:4")
    elif n == "最後の一個" and i < 8:
        pat = "X:4" if i < 6 else "R:4"
    else: continue
    for j in range(4): SAW[j].bar(b, pat.replace("X", nm(v[j])))

# ---------- 低音 ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    r = low(S.chords[b], "E1")
    if n.startswith("割れる") or n == "はじけ":
        if n.startswith("割れる") and i == L - 1: SUB.bar(b, f"{nm(r)}:1 R:3"); continue
        SUB.bar(b, f"{nm(r)}:2.5 {nm(r)}:1 {nm(r + 12)}:0.5")
        BASS.bar(b, f"R:0.5 {nm(r + 12)}:0.25 R:0.75 {nm(r + 12)}:0.5 R:1 {nm(r + 19)}:0.5 R:0.5")
    elif n.startswith("工場"):
        if n == "工場の朝" and i < 8: continue
        SUB.bar(b, f"{nm(r)}:3 R:1" if i % 2 == 0 else f"{nm(r)}:1.5 R:0.5 {nm(r)}:2")
    elif n.startswith("膨らむ"):
        if i < L - 2: SUB.bar(b, f"{nm(r)}:4")
    elif n == "最後の一個" and i < 6:
        SUB.bar(b, f"{nm(r)}:4")

pv = chord_voices(S, range(S.nb), center=60, n=3)
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n.startswith("工場") or n == "空っぽ" or n == "たくさんの玉" or (n == "最後の一個" and i >= 8 and i < 14):
        for j in range(3): PAD[j].bar(b, f"{nm(pv[b][j])}:4")

for sc_ in ("割れる1", "割れる2", "割れる3"):
    b0 = S.sc(sc_)[0]; riser(FX, b0, 8, "D4"); cym_swell(CYM, b0, 2, "C4")
    FX.bar(b0, "G4:2 R:2")         # サブドロップ（はじける瞬間）
riser(FX, S.sc("最後の一個")[8], 8, "D4")

# ---------- ドラム（半分の速さ: キック1拍目・スネア3拍目。トラップのハット） ----------
TRAP_H = ["x.x.x.x.x.x.x.x.", "x.x.x.x.x.xxx.x.", "x.x.x.x.xxxxx.x.", "x.x.x.x.x.x.xxxx"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n.startswith("割れる") or n == "はじけ":
        if n.startswith("割れる") and last: D.set(b, "X" + "." * 15, "." * 16, "." * 16); crash(D, b, "C2", 1); continue
        put_groove(D, b, ("X.....X...X.....", "........X.......", TRAP_H[i % 4]), ghosts=0.2, seed=b, hat_vary=False)
        if i % 8 == 0: crash(D, b)
        if i % 4 == 3 and not last: D.S[b] = "........X...x.XX"
        continue
    if n.startswith("工場"):
        if n == "工場の朝" and i < 8: continue
        put_groove(D, b, ("X.........X.....", "........X.......", "x.x.x.x.x.x.x.x."), seed=b, hat_vary=False)
        if i % 8 == 7: put_fill(D, b, "small")
        continue
    if n.startswith("膨らむ"):
        # スネアがだんだん細かく（4分→8分→16分）
        frac = i / L
        sn = "x...x...x...x..." if frac < 0.5 else ("x.x.x.x.x.x.x.x." if frac < 0.75 else "xxxxxxxxXXXXXXXX")
        D.set(b, "X.......X......." if frac < 0.75 else "X...X...X...X...", sn, "." * 16)
        if last: D.set(b, "." * 16, "." * 16, "." * 16)            # はじける前の1小節の息
        continue
    if n == "たくさんの玉":
        D.set(b, "X.........X.....", "................", "..x...x...x...x." if i >= 4 else "................")
        continue
    if n == "最後の一個":
        if i < 6: D.set(b, "X.......X.......", "x...x...x...x..." if i < 4 else "xxxxxxxxxxxxxxxx", "." * 16)
        continue

S.flags += " --space hall --space-wet 0.14"
S.desc = ("仮: ボカロ曲のインスト25曲の06。フューチャーベース。F長調・150（半分の速さで感じる）。主役の楽器はガラスのプラック。"
          "シャボン玉工場の一日。膨らむ（スネアがだんだん細かく）→割れる（厚い和音の刻みと808、跳ねる3連の旋律）を3回。割れたあとはすぐ空っぽ。"
          "昼にはたくさんの小さな玉が左右に散る。最後の1個は膨らむだけ膨らんで、割れずに空へ上っていく（最後のドロップは鳴らさない）。自作")
S.write()
