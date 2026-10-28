# ケルト・フルート100曲「銀の笛と百の夜」055 湖底の鐘 The Bell Beneath（2026-10-29。第6章 霧の湖）
# イメージ: 雨が上がり、湖は鏡のように澄む。舟べりから水の底をのぞくと、ずっと下に、沈んだ鐘の影が見える気がする。
#   のぞきこむほど、心は水の中へ沈んでいき、気がつくと、水面は頭の上で光っている。
# 形: 水面 → のぞく → 沈む → 湖底（中盤の深い山）→ 浮かばないまま見上げる → 水面だけが残る。6/8・8分＝104・C エオリア。
# ただひとつ: 水面の上と下が入れかわる。前半は笛が高く、弦とチェロ・コントラバスが低い。沈むにつれて笛は下り、弦は上がり、
#   湖底では笛がいちばん低い音域（C4〜G4）で歌い、弦は高い音域（水面の光）にいる。最後は高い弦（水面）だけが残る。
# 編曲の表:
#   水面    : チェロとコントラバスの低い和音、竪琴の低い音
#   のぞく  : 笛（高い音域）。低い弦2声
#   沈む    : 笛の節が後半で3度下へ。弦は中ほどへ上がり3声。内声の動き
#   湖底    : 笛は低い音域の節。弦は高い音域、竪琴の高い響き、遠いティンパニのかすかなロール（沈んだ鐘の気配）
#   見上げる: 笛は低いまま、かけらになる。弦は高いまま
#   水面だけ: 高い弦の和音と竪琴の高い音
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 104   # 8分音符＝104
S = Song("C100", "055-the-bell-beneath", "湖底の鐘", "The Bell Beneath", BPM, 6, "C", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.25})
P = ["Cm", "Ab", "Eb", "Bb", "Cm", "Fm", "Gm", "Cm", "Ab", "Eb", "Fm", "Cm", "Ab", "Bb", "Cm", "Cm"]
D = ["Ab", "Fm", "Cm", "Gm", "Ab", "Fm", "Eb", "Bb", "Ab", "Bb", "Cm", "Cm"]
S.scene("水面", 4, "intro", ["Cm", "Ab", "Cm", "Bb"])
S.scene("のぞく", 16, "verse", P)
S.scene("沈む", 16, "verse", P)
S.scene("湖底", 12, "chorus", D)
S.scene("見上げる", 16, "verse", D + ["Ab", "Bb", "Cm", "Cm"])
S.scene("水面だけ", 8, "outro", ["Ab", "Eb", "Fm", "Cm", "Ab", "Cm", "Cm", "Cm"])
NAMES = ["水面", "のぞく", "沈む", "湖底", "見上げる", "水面だけ"]

c = make(S, NAMES,
         [("水面", 0, 0.6), ("のぞく", 0, 0.64), ("沈む", 0, 0.68), ("沈む", 15, 0.74), ("湖底", 0, 0.78), ("湖底", 5, 0.88), ("湖底", 11, 0.76),
          ("見上げる", 0, 0.68), ("水面だけ", 0, 0.64), ("水面だけ", 7, 0.5)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="水面", passing=True, tension=False)
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.085, pan=0.15, reverb=0.5, barGain=c.g())
CB = S.track("コントラバス", "strings", patch="contrabass", volume=0.07, pan=0.0, reverb=0.5, barGain=c.g())
TIMP = S.track("遠いティンパニ（沈んだ鐘の気配）", "strings", patch="timpani", volume=0.05, pan=-0.3, reverb=0.8, gainDb=-6, barGain=c.g())
HIGH = [S.track(f"高い弦（水面の光）{i + 1}", "strings", patch="slowStrings", volume=0.026, pan=[-0.6, 0.6, 0.0][i], reverb=0.7, barGain=c.g()) for i in range(3)]

HI = ["5':3 4':2 3':1", "1':4 3':2", "2':3 3':1 2':1 1':1", "7:6",
      "1':3 3':2 5':1", "4':4 3':2", "2':3 4':1 3':1 2':1", "1':6",
      "3':3 1':2 6:1", "5:4 7:2", "6:3 1':2 4':1", "3':6",
      "4':2 3':1 1':3", "2':3 7:3", "1':2 7:1 5:3", "1':6"]
LO = ["3:3 4:2 3:1", "1:6", "2:3 3:3", "5:6", "6:3 5:2 3:1", "4:6", "3:3 2:2 1:1", "2:6", "3:3 4:1 5:2", "4:3 2:3", "1:6", "1:6"]
play_melody(c, "のぞく", HI, 4, "air", density=0.45, seed=5501)
play_melody(c, "沈む", HI[:8] + [dshift(x, -2) for x in HI[8:15]] + ["6:6"], 4, "air", density=0.6, seed=5502)
play_melody(c, "湖底", LO, 4, "air", density=0.5, seed=5503)
play_melody(c, "見上げる", ["3:3 4:2 3:1", "1:6", "R:6", "5:6", "6:3 5:2 3:1", "4:6", "R:6", "2:6", "3:3 4:1 5:2", "4:3 2:3", "1:6", "R:6",
                            "3:3 1:3", "2:6", "1:6", "R:6"], 4, "air", density=0.3, seed=5504)

B = S.beats
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "C3", "C6")
    low_side = n in ("水面", "のぞく") or (n == "沈む" and i < 8)
    if n != "水面だけ":
        CELLO.bar(b, f"{nm(r)}:6")
        if low_side or n == "沈む": CB.bar(b, f"{nm(r - 12 if r - 12 >= 28 else r)}:6")
    if low_side:   # 水の下（低い和音）
        v = voice(ch, 46 if n != "沈む" else 50, 2 if n == "のぞく" else 3, spread=True)
        for j in range(len(v)): c.STR[j].bar(b, f"{nm(v[j])}:6")
        c.HARP.bar(b, f"{nm(t[0])}:3 {nm(t[2])}:3")
    elif n == "沈む":   # 弦が中ほどへ上がっていく
        v = voice(ch, 55 + (i - 8), 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:6")
        c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in (t[2], t[4], t[6 % len(t)], t[4], t[2], t[4])))
    else:   # 水面の光（高い弦）。笛は下にいる
        v = voice(ch, 72 if n != "水面だけ" else 74, 3, spread=True)
        for j in range(3): HIGH[j].bar(b, f"{nm(v[j])}:6")
        w = voice(ch, 57, 2, spread=True)
        if n != "水面だけ":
            for j in range(2): c.STR[j].bar(b, f"{nm(w[j])}:6")
        hi = tones(ch, "C6", "C7")
        c.HARP2.bar(b, f"{nm(hi[0])}:2 {nm(hi[1])}:2 {nm(hi[2 % len(hi)])}:2" if i % 2 == 0 else f"{nm(hi[1])}:3 {nm(hi[0])}:3")
    if n == "湖底" and i in (3, 4, 5): TIMP.bar(b, " ".join(f"{nm(r)}:0.5" for _ in range(12)) if i == 4 else f"{nm(r)}:6")
rich(c, choir_scenes=[], pulse_scenes=["沈む", "湖底"], guitar=False, pizz=False, inner=True)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.4 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の055。澄んだ湖の底に、沈んだ鐘の影を見る。6/8・8分＝104、C エオリア。水面の上と下が入れかわる：前半は笛が高く弦が低い。沈むにつれて笛は下り、弦は上がり、湖底では笛がいちばん低い音域で歌い、弦は高い所で水面の光になる。最後は高い弦だけが残る。",
       harm_scenes=None, tail_scene="水面だけ", fill=False, pads=True, pad_scenes=["のぞく", "沈む", "湖底", "見上げる", "水面だけ"], floor=True)
air = {"pre": 0.8, "tail": 8.0, "layers": [{"file": "0598", "db": -40, "hp": 120, "lp": 4000, "wide": 0.014, "duck": 0.35, "fade": 8}],
       "fx": {"shimmer": {"db": -28, "rt": 9.0}, "far": {"db": -24, "delay": 0.35, "lp": 2400, "rt": 5.5}}, "intro_db": 6.0}
json.dump(air, open("/tmp/cel/w/air055.json", "w"), ensure_ascii=False)
