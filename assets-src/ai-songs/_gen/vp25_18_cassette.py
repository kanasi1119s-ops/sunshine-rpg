# vp25 18「カセットテープの夏休み」A Summer on Cassette Tape（仮）— ヒップホップ（ローファイ寄り）。D♭長調・84（早送りで上がり、最後に伸びて落ちる）・4/4。主役の楽器: ナイロン弦ギター
# 物語: 押し入れの奥から出てきた、子どものころの夏休みを録ったカセットテープ。再生ボタンを押す。A面の思い出、早送り、B面のいちばん大事な日。
#   最後はテープが伸びて、音がゆっくり落ちて止まる。
# 形: 古いテープを再生: A面→早送り→B面。テープの操作で場面が変わる
# 場面と強さ: A面＝なつかしく中くらい／早送り＝速く高い（テンポと音程が同時に上がる）／B面＝思い出が深まって大きい／
#   最後にテープが伸びて止まる（テンポも音程も落ちて、無音）
# 旋律の性格: 2小節のギターの句に、思い出すように1音ずつ増えていく
# 崩す所: 早送りで音程と速さを同時に上げる（そして最後は同時に下げる）
from vp25_lib import *

S = Song("18", "cassette", "カセットテープの夏休み（仮）", "A Summer on Cassette Tape", 84, 4, "Db", "major", "ヒップホップ（ローファイ）")
S.kit = "naked"
K = S.key
SIDE_A = ["Dbmaj7", "Bbm9", "Gbmaj7", "Ab13"]
SIDE_A2 = ["Gbmaj7", "Fm7", "Ebm9", "Ab13"]
SIDE_B = ["Gbmaj7", "Fm7", "Ebm9", "Ab13", "Dbmaj7", "Bb7", "Ebm7", "Ab7sus4"]
S.scene("再生", 2, "intro", ["Dbmaj7", "Dbmaj7"])
S.scene("A面", 24, "verse", SIDE_A)
S.scene("A面2", 16, "verse", SIDE_A2)
FF = [tr_chord(c, s) for c, s in zip(SIDE_A * 2, [0, 1, 2, 3, 4, 5, 6, 7])]
S.scene("早送り", 8, "pre", FF)
S.scene("B面", 24, "chorus", SIDE_B)
S.scene("B面の最後", 16, "chorus", SIDE_B)
STRETCH = [tr_chord(c, -s) for c, s in zip(["Dbmaj7", "Dbmaj7", "Gbmaj7", "Gbmaj7", "Dbmaj7", "Dbmaj7", "Dbmaj7", "Dbmaj7"], [0, 0, 1, 1, 2, 3, 4, 5])]
S.scene("テープが伸びる", 8, "outro", STRETCH)
b_ff, b_b, b_st = S.sc("早送り")[0], S.sc("B面")[0], S.sc("テープが伸びる")[0]
S.tempo = [{"bar": b_ff + 1, "bpm": 84}, {"bar": b_ff + 2, "bpm": 132, "ramp": 6}, {"bar": b_b + 1, "bpm": 84},
           {"bar": b_st + 1, "bpm": 84}, {"bar": b_st + 2, "bpm": 52, "ramp": 6}]
S.extra.update({"swing": 0.38})
S.flags = "--bass rubner " + S.flags
SHIFT = {}
for i, b in enumerate(S.sc("早送り")): SHIFT[b] = i
for i, b in enumerate(S.sc("テープが伸びる")): SHIFT[b] = -[0, 0, 1, 1, 2, 3, 4, 5][i]

NY = S.track("主役: ナイロン弦ギター", "guitar", patch="nylonGuitar", volume=0.25, pan=-0.12, amp="clean", chorus=0, reverb=0.25, gainDb=6, humanPitch=0, sustain=1.6,
             fx=[{"type": "eq", "low": -3, "mid": 2, "midHz": 2200, "high": 1}, {"type": "tape", "mix": 0.15}])
NY2 = S.track("ナイロン弦（和音）", "guitar", patch="nylonGuitar", volume=0.13, pan=0.35, amp="clean", chorus=0, reverb=0.25, humanPitch=0, sustain=1.8)
PI = [S.track(f"ピアノ{i + 1}", "piano", **piano_spec(0.11, [0.2, 0.3, 0.1][i], 0.3)) for i in range(3)]
LEAD = S.track("リード（歌の役）", "lead", **lead_spec("calliope", vol=0.16, pan=0.05, delay=0.75, extra_fx=[{"type": "filter", "kind": "lowpass", "freq": 5000, "q": 0.7}]))
BASS = S.track("ウッドベース", "bass", volume=0.22, pan=0)
STR = [S.track(f"弦{i + 1}", "strings", patch="slowStrings", **strings_spec(0.07, [-0.55, 0.55][i])) for i in range(2)]
FX = S.track("テープの音", "pad", patch="fxRiser", volume=0.06, pan=0, reverb=0.2)
D = S.drumkit()


def sh(b, s):
    """早送り・テープの伸びで音程をずらす"""
    return transpose(s, SHIFT.get(b, 0)) if SHIFT.get(b, 0) else s


# ---------- ギターの句（2小節）: 思い出すように1音ずつ増える ----------
PHR = ["5:0.5 3:0.5 2:0.5 1:0.5 6,:1 1:1", "2:0.5 3:0.5 5:1 3:0.5 2:0.5 1:1"]
FULL = ["5:0.5 3:0.5 2:0.5 1:0.5 6,:0.5 1:0.5 2:0.5 3:0.5", "2:0.5 3:0.5 5:0.5 6:0.5 5:0.5 3:0.5 2:0.5 1:0.5"]


def grow(i):
    """i 小節目までに思い出した音だけ鳴らす（音の数がだんだん増える）"""
    src = FULL[i % 2].split()
    n = min(len(src), 2 + i // 2)
    return " ".join(t if j < n else "R:" + t.split(":")[1] for j, t in enumerate(src))


for i, b in enumerate(S.sc("A面")): NY.bar(b, K.mel(grow(i), oct=4))
for i, b in enumerate(S.sc("A面2")): NY.bar(b, K.mel(FULL[i % 2] if i < 8 else seq_up(FULL[i % 2], K, 2), oct=4))
for i, b in enumerate(S.sc("早送り")): NY.bar(b, sh(b, K.mel(FULL[i % 2], oct=5)))
BM = ["3':1.5 2':0.5 1':1 5:1", "6:2 5:1 3:1", "2:1.5 3:0.5 5:1 6:1", "5:4", "3':1.5 2':0.5 1':1 6:1", "7:1.5 1':0.5 2':2", "4':1 3':1 2':1 1':1", "2':4"]
for i, b in enumerate(S.sc("B面")):
    NY.bar(b, K.mel(FULL[i % 2], oct=4) if i < 8 else K.mel(PHR[i % 2], oct=5))
    if i >= 8: LEAD.bar(b, K.mel(BM[i % 8], oct=4))
for i, b in enumerate(S.sc("B面の最後")):
    LEAD.bar(b, K.mel(BM[i % 8], oct=4 if i < 8 else 5))
    NY.bar(b, K.mel(FULL[i % 2], oct=4))
for i, b in enumerate(S.sc("テープが伸びる")):
    if i < 6: NY.bar(b, sh(b, K.mel(FULL[i % 2] if i < 4 else PHR[i % 2], oct=4)))
NY.bar(S.sc("再生")[1], K.mel("R:2 5:0.5 3:0.5 2:0.5 1:0.5", oct=4))

# ---------- 和音（ナイロン弦の和音・ピアノ・弦） ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "再生": continue
    v = voice(S.chords[b], 60, 3)
    if n in ("A面", "A面2", "早送り", "B面", "B面の最後") or (n == "テープが伸びる" and i < 7):
        NY2.bar(b, f"{nm(v[0], True)}:1 {nm(v[1], True)}:0.5 {nm(v[2], True)}:2.5" if i % 2 == 0 else f"R:0.5 {nm(v[1], True)}:1.5 {nm(v[2], True)}:2")
    if n in ("A面2", "B面", "B面の最後", "早送り") or (n == "A面" and i >= 12):
        pv = voice(S.chords[b], 67, 3)
        pat = "R:0.5 X:1 R:0.5 X:2" if n != "B面の最後" else "X:1.5 X:0.5 R:0.5 X:1.5"
        for j in range(3): PI[j].bar(b, pat.replace("X", nm(pv[j], True)))
    if n in ("B面", "B面の最後") and not (n == "B面" and i < 8):
        sv = voice(S.chords[b], 70, 2)
        for j in range(2): STR[j].bar(b, f"{nm(sv[j], True)}:4")

# ---------- ベース ----------
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    r = low(S.chords[b], "E1")
    if n == "再生" or (n == "A面" and i < 4): continue
    if n == "テープが伸びる" and i >= 7: continue
    BASS.bar(b, f"{nm(r, True)}:1.5 R:0.5 {nm(r + 7, True)}:1 {nm(r + 12, True)}:0.5 {nm(r + 10, True)}:0.5" if i % 2 == 0 else f"{nm(r, True)}:2 R:0.5 {nm(r, True)}:1.5")

FX.bar(S.sc("再生")[0], "A4:1 R:3")                 # 再生ボタンの「カチャ」
FX.bar(b_ff, "A4:0.5 R:3.5")
FX.bar(S.sc("テープが伸びる")[6], "E4:8")          # ダウンリフター（落ちていく）

# ---------- ドラム（ローファイのブーンバップ） ----------
LK = ["X.......x.X.....", "X..x......X.....", "X.........X..x..", "X.......X.x....."]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "再生" or (n == "A面" and i < 4): continue
    if n == "テープが伸びる":
        if i < 6: D.set(b, LK[i % 4], "....X.......X...", "x.x.x.x.x.x.x.x." if i < 4 else "x...x...x...x...")
        continue
    if n == "早送り":
        D.set(b, "X...X...X...X...", "....X.......X...", "xxxxxxxxxxxxxxxx"); continue
    put_groove(D, b, (LK[i % 4], "....X.......X...", "x.xox.xox.xox.xo" if n.startswith("B") else "x.x.x.x.x.x.x.x."), ghosts=0.5, seed=b, hat_vary=False)
    if n.startswith("B") and i % 8 == 0: D.cym(b, "D2:4")
    if i % 8 == 7: put_fill(D, b, "small")

S.desc = ("仮: ボカロ曲のインスト25曲の18。ローファイ寄りのヒップホップ。D♭長調・84。主役の楽器はナイロン弦ギター。押し入れから出てきた夏休みのカセットテープ。"
          "再生ボタン→A面（2小節のギターの句に、思い出すように1音ずつ増える）→早送り（テンポと音程が同時に上がる）→B面のいちばん大事な日→"
          "テープが伸びて、テンポも音程もゆっくり落ちて止まる。自作")
S.write()
