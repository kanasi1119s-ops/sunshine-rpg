# ケルト・フルート100曲「銀の笛と百の夜」037 森の主 The Old One of the Wood — 第2版（2026-10-28）
# イメージ: 森のいちばん奥に立つ、千年の古木。森の主。近づくほど、空気が重く、深くなる（低い弦・コントラバス・ホルン）。
#   主の前で、低いホルンの声に、エイラの笛がたった一度だけ重なる（いちばん深い山）。そのとき、主はエイラを認める。
#   重さがやわらぎ、最後は笛のやさしい長い音。
# 形（台帳）: 荘厳な行進（畏れ→認められる）。4/4・♩=50。C エオリア→最後は C ドリア（A♮の光）。始め：低い弦／終わり：やさしい長音。中盤に深い山。
# 編曲の表:
#   畏れ     : 低い弦とコントラバス、遠いティンパニのロール
#   近づく   : チェロとコントラバスの歩み（2分音符）、低いホルンの長い音。笛は小さく、慎重に
#   森の主   : ホルン2本・ティンパニ・弦のうねり。後半で、ホルンの旋律に笛が一度だけ同じ音で重なる（山）
#   認められる: C ドリアへ（A♮）。竪琴の分散和音、弦のあたたかい和音
#   長音     : 笛のやさしい長い音
import sys, json
from c100_common import *
from c100_v2 import *

S = Song("C100", "037-the-old-one-of-the-wood", "森の主", "The Old One of the Wood", 50, 4, "C", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35, "rubato": 0.2})
S.scene("畏れ", 4, "intro", ["Cm", "Cm", "Ab", "Cm"])
S.scene("近づく", 16, "verse", ["Cm", "Ab", "Eb", "Bb", "Cm", "Fm", "G", "Cm", "Ab", "Eb", "Fm", "Cm", "Ab", "Bb", "G", "G"])
S.scene("森の主", 16, "chorus", ["Cm", "Ab", "Bb", "Eb", "Fm", "Cm", "G", "G", "Ab", "Bb", "Cm", "Ab", "Fm", "G", "Cm", "Cm"])
S.scene("認められる", 12, "verse", ["Cm", "F", "Cm", "Bb", "F", "Cm", "Gm", "Cm", "F", "Bb", "F", "C"])
S.scene("長音", 4, "outro", ["C", "C", "C", "C"])
NAMES = ["畏れ", "近づく", "森の主", "認められる", "長音"]

c = make(S, NAMES,
         [("畏れ", 0, 0.62), ("近づく", 0, 0.64), ("近づく", 15, 0.72), ("森の主", 0, 0.78), ("森の主", 10, 0.95), ("森の主", 15, 0.76),
          ("認められる", 0, 0.66), ("長音", 0, 0.58), ("長音", 3, 0.38)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="畏れ", passing=True, tension=False)
CB = S.track("コントラバス", "strings", patch="contrabass", volume=0.11, pan=0.0, reverb=0.45, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.09, pan=0.15, reverb=0.45, barGain=c.g())
HORN = S.track("ホルン（主の声）", "brass", patch="horn", volume=0.09, pan=-0.2, reverb=0.6, breath=False, attack=0.2, release=0.9, bright=-0.4, barGain=c.g())
HORN2 = S.track("ホルン2", "brass", patch="horn", volume=0.065, pan=-0.3, reverb=0.6, breath=False, attack=0.25, release=0.9, bright=-0.5, barGain=c.g())
TIMP = S.track("ティンパニ", "strings", patch="timpani", volume=0.08, pan=0.0, reverb=0.5, gainDb=-4, barGain=c.g())

play_melody(c, "近づく", ["R:4", "R:2 5:2", "4:2 3:2", "R:4", "R:4", "R:2 3:2", "2:2 7,:2", "R:4",
                         "R:2 1:1 2:1", "3:3 R:1", "4:2 3:1 2:1", "1:4", "R:2 6,:1 7,:1", "1:2 2:2", "7,:4", "R:4"], 4, "air", density=0.5, seed=3701)
# 森の主：前半は笛が休み、ホルンが主の旋律。後半（9〜12小節）で笛が一度だけホルンと同じ音で重なる
HM = ["1:2 3:2", "4:3 3:1", "2:2 4:2", "5:4", "6:2 5:1 4:1", "3:2 2:2", "7,:3 2:1", "1:4",
      "3:2 5:2", "6:3 5:1", "4:2 3:1 2:1", "3:4", "4:2 3:2", "2:2 7,:2", "1:4", "R:4"]
for t, L, m in section_events(c, "森の主", HM, 3): HORN.at(t, f"{nm(m)}:{L}")
play_melody(c, "森の主", ["R:4"] * 8 + HM[8:12] + ["R:4"] * 4, 4, "air", density=0.3, seed=3702)
KD = S.key.__class__("C", "dorian", 4)
play_melody(c, "認められる", ["5:2 6:1 5:1", "4:2 3:2", "2:1 3:1 4:2", "5:4", "6:2 5:1 4:1", "3:2 2:2", "4:3 3:1", "2:4",
                             "3:2 4:1 5:1", "6:2 4:2", "5:3 4:1", "3:4"], 4, "air", key=KD, density=0.7, seed=3703)
play_melody(c, "長音", ["5:4", "5:4", "R:4", "R:4"], 4, "air", key=S.key.__class__("C", "major", 4), density=0)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2")
    if n == "長音" and i >= 3: continue
    CB.bar(b, f"{nm(r if r >= 28 else r + 12)}:4")
    v = voice(ch, 48 if n in ("畏れ", "近づく") else 55, 3, spread=True)
    for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4" if n != "森の主" else " ".join(f"{nm(v[j])}:0.5" for _ in range(8)))
    if n == "畏れ" and i % 2 == 1: TIMP.bar(b, "R:2 " + " ".join(f"{nm(r + 12)}:0.25" for _ in range(8)))
    if n == "近づく":
        CELLO.bar(b, f"{nm(r + 12)}:2 {nm(r + 19)}:2")
        HORN2.bar(b, f"{nm(tones(ch, 'C3', 'C4')[0])}:4")                       # 主の気配は途切れない
        if i % 4 in (0, 3): c.HARP.bar(b, " ".join(f"{nm(x)}:{0.3 if j < 3 else 3.1}" for j, x in enumerate(tones(ch, "C3", "C5")[:4])))   # 足もとの枝
        if i % 4 == 3: c.HARP2.bar(b, "R:2 " + " ".join(f"{nm(x)}:0.5" for x in tones(ch, "C5", "C6")[:4]))
    if n == "森の主":
        CELLO.bar(b, f"{nm(r + 12)}:4"); HORN2.bar(b, f"{nm(tones(ch, 'C3', 'C4')[0])}:4")
        if i % 4 == 0: TIMP.bar(b, f"{nm(r + 12)}:2 R:2")
        if i == 11: TIMP.bar(b, "R:2 " + " ".join(f"{nm(r + 12)}:0.25" for _ in range(8)))
    if n in ("認められる", "長音"):
        CELLO.bar(b, f"{nm(r + 12)}:4")
        c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in tones(ch, "C3", "C5")[:4]))
rich(c, choir_scenes=["認められる"], pulse_scenes=["近づく", "森の主", "認められる"], guitar=False, pizz=False, inner=True, choir_vol=0.1)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.4 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の037（第2版）。森の奥の千年の古木、森の主。4/4・♩=50、C エオリア→C ドリア。荘厳な行進。主の声（低いホルン）の旋律に、笛が一度だけ同じ音で重なる所がいちばん深い山。主に認められて重さがやわらぎ、笛のやさしい長い音で終わる。",
       harm_scenes=None, tail_scene="長音", fill=False, pads=True, pad_scenes=["近づく", "森の主", "認められる", "長音"], floor=True)
json.dump({"pre": 1.0, "tail": 8.0, "layers": [{"file": "0136", "db": -33, "hp": 80, "lp": 4000, "wide": 0.018, "duck": 0.3, "fade": 8}],
           "fx": {"glass": {"hz": [261.6, 523.3, 784.0], "db": -29, "rt": 7.0, "start": 4}, "shimmer": {"db": -28, "rt": 9.0}, "far": {"db": -23, "delay": 0.35, "lp": 2000, "rt": 6.0},
                  "haze": {"db": -25, "rt": 10.0}, "band": {"db": -38, "hz": 5000, "per": 31}}, "intro_db": 8.5}, open("/tmp/cel/w/air037.json", "w"))
