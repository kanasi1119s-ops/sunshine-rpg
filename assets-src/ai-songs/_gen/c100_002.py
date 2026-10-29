# ケルト・フルート100曲「銀の笛と百の夜」002 灯室への階段 Stairway to the Lamp — 第3版（2026-10-29 作り直し。docs/sound/celtic-study/E-100-plan.md）
# 物語: 笛を手にしたエイラは、灯台のらせん階段を灯室まで上る。祖父がかつて30分ごとに上り下りし、灯を回すぜんまいを巻いた階段。
#   一つの階を上るごとに、ぜんまいを巻く「カチ、カチ、カチ、コン」が聞こえ、景色（調）が一段上がる。最後に灯室の扉を開けると、灯が明るくともる。
# 調べ: 喜び。形: アン・ドロ型（短い節を何度もくり返し、少しずつ足していく）。4/4・♩=80、はずむ付点。
# 旋法: ミクソリディア（♭7）。階ごとに全音上がる（G → A → B → C♯）。灯室で半音上の D イオニア（長調）に開ける。
# 笛: 中音域、カットで歯切れよく。階が上がるほど装飾が増える。4階の後半から2本目の笛が3度下で加わる。
# 伴奏の主役: 開いた和音（3度を抜いた）のナイロン弦ギター。足元＝指で1音ずつ、1階＝指弾き、2階から付点のストローク。
#   ピチカート（足音）は2階から、コントラバスのピチカートは3階から。打楽器・竪琴・弦の持続・パッドは使わない。
# この曲だけ: ぜんまいを巻く4音（ピチカートの高い音）が各階の8小節目・16小節目と踊り場で鳴り、そのたびに一段高い所から節が始まる。
# 山: 階段（階ごとに一段ずつ）。最後の灯室がいちばん明るい。
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 80
S = Song("C100", "002-stairway-to-the-lamp", "灯室への階段", "Stairway to the Lamp", BPM, 4, "G", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35})
FLOORS = [("1階", "G"), ("2階", "A"), ("3階", "B"), ("4階", "C#")]
def fl_chords(t):
    k = Key(t, "mixolydian", 4)
    T, VII, IV = t, k.up(10).tonic, k.up(5).tonic
    return [T, VII] * 6 + [IV, VII, T, T]
S.scene("足元", 4, "intro", ["G", "F", "G", "F"])
for idx, (nm_, t) in enumerate(FLOORS):
    S.scene(nm_, 16, "verse" if idx < 3 else "chorus", fl_chords(t))
    if idx < 3:
        nxt = FLOORS[idx + 1][1]
        S.scene(f"踊り場{idx + 1}", 2, "break", [t, nxt])
S.scene("灯室", 8, "outro", ["D", "A", "G", "D", "D", "G", "D", "D"])
NAMES = ["足元", "1階", "踊り場1", "2階", "踊り場2", "3階", "踊り場3", "4階", "灯室"]

c = make(S, NAMES,
         [("足元", 0, 0.62), ("1階", 0, 0.64), ("2階", 0, 0.7), ("3階", 0, 0.76), ("4階", 0, 0.82), ("4階", 15, 0.86),
          ("灯室", 0, 0.9), ("灯室", 4, 0.88), ("灯室", 7, 0.8)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="足元", passing=True, tension=False)
GTR = [S.track(f"ギター{i + 1}", "guitar", patch="nylonGuitar", volume=0.06, pan=-0.3 - 0.04 * i, reverb=0.3, barGain=c.g()) for i in range(5)]
GP = S.track("ギター（指で1音ずつ）", "guitar", patch="nylonGuitar", volume=0.075, pan=-0.25, reverb=0.32,
             barGain=[round(x * (2.4 if c.scene_of_bar[b] in ("足元", "1階") else 1.0), 3) for b, x in enumerate(c.g())])   # 指弾きだけの場面は大きく（1回目 -37〜-25dB で小さかった）
STEP = S.track("足音（ピチカート）", "strings", patch="pizzicato", volume=0.065, pan=0.35, reverb=0.3, barGain=c.g())
WIND = S.track("ぜんまい（ピチカートの高い音）", "strings", patch="pizzicato", volume=0.07, pan=0.55, reverb=0.45, barGain=c.g())
CB = S.track("コントラバス（ピチカート）", "strings", patch="contrabass", volume=0.075, pan=0.0, reverb=0.3, barGain=c.g())
F2 = S.track("2本目の笛", "panflute", patch="flute", volume=0.26, bright=-0.8, pan=0.3, reverb=0.55, breath=False,
             noRestrike=True, mono=True, sustain=1.1, phrase=16, barGain=c.g())

# ---------- 旋律（8小節。2小節ずつ4つの句。最後の句の後半2拍は休み＝ぜんまいの音） ----------
M = ["1:1 2:0.5 3:0.5 5:1 4:0.5 3:0.5", "2:1 1:0.5 2:0.5 3:2",
     "5:1 6:0.5 5:0.5 4:1 3:1", "2:1.5 3:0.5 1:2",
     "3:0.5 4:0.5 5:1 7:1 6:0.5 5:0.5", "4:1 5:1 6:2",
     "7:1 6:0.5 5:0.5 4:1 2:1", "1:2 R:2"]
M2 = M[:6] + ["7:0.5 1':0.5 7:0.5 6:0.5 5:1 4:0.5 2:0.5", "1:2 R:2"]     # くり返しの2回目は終わりの句を少し変える
DENS = [0.3, 0.6, 0.85, 1.05]
for idx, (nm_, t) in enumerate(FLOORS):
    k = Key(t, "mixolydian", 4)
    notes = play_melody(c, nm_, M + M2, 4, "hornpipe", key=k, density=DENS[idx], seed=200 + idx)
    if idx == 3:   # 4階の後半：2本目の笛が3度下で寄りそう
        a = (c.s0[nm_] + 8) * S.beats
        for st, L, m, mk in notes:
            if st >= a and L >= 0.4:
                h = m - 3 if (m - 3 - k.t) % 12 in [(x) % 12 for x in k.steps] else m - 4
                F2.at(round(st + 0.02, 3), f"{nm(h)}:{round(L, 3)}")
# 灯室：D イオニア。最後の句を長く、高い所で
KD = Key("D", "major", 4)
play_melody(c, "灯室", ["5:1 6:1 1':2", "2':2 1':1 6:1", "5:1 6:0.5 5:0.5 3:2", "2:2 1:2", "5:1 6:1 1':2", "3':4", "2':2 1':2", "1':4"],
            4, "air", key=KD, density=0.4, seed=210)
play_melody(c, "灯室", ["3:1 4:1 5:2", "6:2 5:1 3:1", "2:1 3:0.5 2:0.5 1:2", "7,:2 5,:2", "3:1 4:1 5:2", "1':4", "6:2 5:2", "5:4"],
            4, "air", key=KD, density=0.0, track=F2)

# ---------- 伴奏 ----------
B = S.beats
DOT = [(0, 0.75, "d", "!"), (0.75, 0.25, "u", ","), (1, 0.75, "d", ""), (1.75, 0.25, "u", ","), (2, 1, "d", ""), (3, 0.75, "d", ","), (3.75, 0.25, "u", ",")]
def wind(b, k, at=2.0):
    """ぜんまいを巻く4音：カチ・カチ・カチ・コン（その階の主音の2オクターブ上のあたり）"""
    r = 72 + (k.t - 72) % 12
    WIND.at(b * B + at, f"{nm(r)}:0.25"); WIND.at(b * B + at + 0.5, f"{nm(r + 2)}:0.25")
    WIND.at(b * B + at + 1.0, f"{nm(r)}:0.25"); WIND.at(b * B + at + 1.5, f"{nm(r + 7)}:0.5")
for b in range(c.NB):
    n, i, Lb, kk = S.scene_of(b); ch = S.chords[b]
    v = open_chord(ch)
    if n == "足元":   # ギターが指で1音ずつ（根音・5度・オクターブ・9度）、2小節目と4小節目にぜんまい
        GP.bar(b, " ".join(f"{nm(x)}:0.5{',' if q % 2 else ''}" for q, x in enumerate([v[0], v[1], v[2], v[3], v[2], v[1], v[2], v[3]])))
        if i % 2 == 1: wind(b, Key("G", "mixolydian", 4))
        continue
    if n.startswith("踊り場"):   # 踊り場：ぜんまいを巻く。2小節目で次の階の和音
        strum(GTR, b, B, ch, [(0, 2, "d", "!"), (2, 2, "d", "")])          # 1回目は全音符1つで、ここが急に小さくなった
        STEP.bar(b, f"{nm(v[1] + 12)}:1 R:1 {nm(v[1] + 12)}:1 R:1")
        if n == "踊り場1": GP.bar(b, " ".join(f"{nm(x)}:0.5," for x in [v[0], v[1], v[2], v[3], v[2], v[1], v[2], v[3]]))
        wind(b, Key(ch, "mixolydian", 4), at=0.0); wind(b, Key(ch, "mixolydian", 4), at=2.0)
        if n != "踊り場1": CB.bar(b, f"{nm(v[0] - 12 if v[0] - 12 >= 28 else v[0])}:4")
        continue
    if n == "灯室":
        if i < 7: strum(GTR, b, B, ch, DOT if i < 4 else [(0, 2, "d", "!"), (2, 2, "d", "")])
        else: strum(GTR, b, B, ch, [(0, 4, "d", "!")])
        CB.bar(b, f"{nm(v[0] - 12 if v[0] - 12 >= 28 else v[0])}:4")
        STEP.bar(b, f"{nm(v[2] + 12)}:1 R:1 {nm(v[1] + 12)}:1 R:1" if i < 7 else f"{nm(v[2] + 12)}:4")
        continue
    floor = int(n[0])
    k = Key(dict(FLOORS)[n], "mixolydian", 4)
    if floor == 1:   # 1階：指弾き（2拍ずつ、低い音と上の2音）。後半8小節から足音が小さく入る（上り始め）
        GP.bar(b, f"{nm(v[0])}:1 {nm(v[2])}:0.5, {nm(v[3])}:0.5, {nm(v[1])}:1 {nm(v[2])}:0.5, {nm(v[3])}:0.5,")
        if i >= 8: STEP.bar(b, f"{nm(v[1] + 12)}:1, R:1 {nm(v[1] + 12)}:1, R:1")
    else:            # 2階から：付点のストローク
        strum(GTR, b, B, ch, DOT)
        STEP.bar(b, f"{nm(v[1] + 12)}:1 R:1 {nm(v[1] + 12)}:1 R:1" if floor == 2 else f"{nm(v[1] + 12)}:1 R:0.5 {nm(v[2] + 12)}:0.5 {nm(v[1] + 12)}:1 R:1")
    if floor >= 3: CB.bar(b, f"{nm(v[0] - 12 if v[0] - 12 >= 28 else v[0])}:1.5 R:0.5 {nm(v[1] - 12 if v[1] - 12 >= 28 else v[1])}:2")
    if i in (7, 15): wind(b, k)   # 節の休み（後半2拍）にぜんまい
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.26 --master -15 --widen 1.25 --side-hpf 200",
       "ケルト・フルート100曲の002（第3版）。灯台のらせん階段を灯室まで上る。アン・ドロ型（短い節のくり返しに少しずつ足していく）、4/4・♩=80、付点のはずみ。G→A→B→C♯のミクソリディアで、階ごとに全音上がり、灯室で D の長調に開ける。伴奏は開いた和音のナイロン弦ギターと、ピチカートの足音。ぜんまいを巻く4音が各階で鳴り、そのたびに一段高い所から節が始まる。",
       harm_scenes=None, tail_scene="灯室", double=True, fill=False, pads=False)
air = {"pre": 0.3, "tail": 6.0, "layers": [{"file": "0595", "db": -44, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -29, "delay": 0.16, "lp": 3000, "rt": 2.4}}}
json.dump(air, open("/tmp/cel/w/air002.json", "w"), ensure_ascii=False)
