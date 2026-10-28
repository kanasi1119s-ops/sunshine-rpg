# ケルト・フルート100曲「銀の笛と百の夜」056 祖父の幻 The Shape of Grandfather（2026-10-29。第6章 霧の湖）
# イメージ: 湖のまんなかで、霧がふたたび濃くなる。その向こうに、笛を吹く人の影が立っている。聞こえてくる節は、
#   祖父がよく吹いていた歌。エイラは夢中で、その節を1小節遅れで追いかける。影はやがて薄れ、エイラの笛だけが残って、
#   祖父が吹き終えなかった最後の句を、自分で吹き終える。
# 形: 呼びかけ（祖父の節だけ）→ 追う1・追う2（1小節遅れのカノン）→ 影が薄れる（祖父が先に消える）→ 笛だけ（最後の句・余白で止まる）。
#   4/4・♩=56・F# エオリア。2つの小さな山（追う2の終わり／影が薄れる所）。
# ただひとつ: 祖父の節は、霧の向こうの遠いホルン（深い響き・小さめ・左の遠く）。笛はそれを1小節遅れでなぞる。
#   祖父が消えたあと、笛が残りの句を自分で吹き終える。
# 編曲の表:
#   霧    : 弦のドローン（F# と C#）とチェロ
#   呼びかけ: 遠いホルンが祖父の節を吹く。笛はまだ吹かない。竪琴の低い音
#   追う1 : 笛が1小節遅れで追う。弦2声
#   追う2 : 弦3声・内声の動き。ホルンは少し飾った節。山
#   影が薄れる: ホルンは4小節で消える。笛は残りを自分で。弦が少しふくらむ
#   笛だけ: 笛の最後の句。終わりは5度の音で止まり、弦が主和音で受けとめる
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 56
S = Song("C100", "056-the-shape-of-grandfather", "祖父の幻", "The Shape of Grandfather", BPM, 4, "F#", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.22})
C1 = ["F#m", "F#m", "E", "E", "D", "D", "F#m", "F#m"]
C2 = ["Bm", "Bm", "D", "E", "F#m", "F#m", "C#m", "C#m"]
S.scene("霧", 3, "intro", ["F#m", "F#m", "F#m"])
S.scene("呼びかけ", 8, "verse", C1)
S.scene("追う1", 16, "verse", C1 + C2)
S.scene("追う2", 16, "chorus", C1 + C2)
S.scene("影が薄れる", 8, "verse", C1)
S.scene("笛だけ", 7, "outro", ["F#m", "D", "E", "F#m", "Bm", "C#m", "F#m"])
NAMES = ["霧", "呼びかけ", "追う1", "追う2", "影が薄れる", "笛だけ"]

c = make(S, NAMES,
         [("霧", 0, 0.6), ("呼びかけ", 0, 0.62), ("追う1", 0, 0.66), ("追う2", 0, 0.72), ("追う2", 13, 0.84), ("追う2", 15, 0.74),
          ("影が薄れる", 0, 0.72), ("影が薄れる", 4, 0.82), ("影が薄れる", 7, 0.7), ("笛だけ", 0, 0.66), ("笛だけ", 6, 0.52)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="霧", passing=True, tension=False)
HORN = S.track("祖父の笛（遠いホルン）", "brass", patch="horn", volume=0.075, pan=-0.45, reverb=0.85, breath=False,
               attack=0.3, release=1.2, bright=-0.6, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.08, pan=0.15, reverb=0.5, barGain=c.g())

S1 = ["1:2 3:1 5:1", "4:3 3:1", "2:2 4:1 3:1", "2:4", "3:1.5 2:0.5 1:2", "6,:2 7,:2", "1:3 5,:1", "1:4"]
S2 = ["4:2 5:1 6:1", "7:2 6:1 5:1", "6:3 5:1", "4:2 5:2", "5:1.5 6:0.5 5:1 3:1", "1:4", "2:2 3:1 4:1", "5:4"]
S1v = ["1:1 2:1 3:1 5:1", "4:2 5:1 3:1", "2:2 4:1 3:1", "2:4", "3:1.5 2:0.5 1:1 7,:1", "6,:2 7,:2", "1:3 5,:1", "1:4"]
# 祖父（ホルン）：呼びかけ8 ＋ 追う1・追う2・影の4小節
H = S1 + S1 + S2 + S1v + S2 + S1[:4]
play_melody(c, "呼びかけ", H[:8], 3, "air", density=0.0, track=HORN)
play_melody(c, "追う1", H[8:24], 3, "air", density=0.0, track=HORN)
play_melody(c, "追う2", H[24:40], 3, "air", density=0.0, track=HORN)
play_melody(c, "影が薄れる", H[40:44] + ["R:4"] * 4, 3, "air", density=0.0, track=HORN)
# エイラ（笛）：1小節遅れ。影が薄れたあとも、祖父の節を最後まで吹き終える
seq = S1 + S2 + S1v + S2 + S1
F = ["R:4"] + seq[:39]
play_melody(c, "追う1", F[0:16], 4, "air", density=0.4, seed=5601)
play_melody(c, "追う2", F[16:32], 4, "air", density=0.6, seed=5602)
play_melody(c, "影が薄れる", F[32:40], 4, "air", density=0.6, seed=5603)
play_melody(c, "笛だけ", [seq[39], "3:2 5:2", "4:2 3:1 2:1", "3:1.5 2:0.5 1:2", "4:2 5:1 6:1", "5:4", "R:4"], 4, "air", density=0.5, seed=5604)

B = S.beats
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "F#2", "F#5")
    CELLO.bar(b, f"{nm(r)}:4")
    if n in ("霧", "呼びかけ"):   # 霧：F# と C# のドローンの上に和音がうすく
        drone(c.STR[:2], b, B, 54)
        v = voice(ch, 57, 1, spread=True); c.STR[2].bar(b, f"{nm(v[0])}:4")
        if n == "呼びかけ": c.HARP.bar(b, f"{nm(t[0])}:2 {nm(t[2])}:2")
        continue
    nv = 2 if n == "追う1" else 3
    v = voice(ch, 54 if n == "追う1" else 57, nv, spread=True)
    for j in range(nv): c.STR[j].bar(b, f"{nm(v[j])}:4")
    if n in ("追う1", "追う2"): c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in (t[0], t[2], t[4 % len(t)], t[2])))
    if n == "影が薄れる": c.HARP.bar(b, " ".join(f"{nm(x)}:0.5" for x in (t[0], t[2], t[4 % len(t)], t[5 % len(t)], t[4 % len(t)], t[2], t[3 % len(t)], t[2])))
    if n == "笛だけ": c.HARP.bar(b, f"{nm(t[0])}:4" if i == 6 else f"{nm(t[0])}:2 {nm(t[2])}:2")
rich(c, choir_scenes=["追う2"], pulse_scenes=["追う2", "影が薄れる"], guitar=False, pizz=False, inner=True)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.4 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の056。霧の向こうに、笛を吹く祖父の影。4/4・♩=56、F# エオリア。遠いホルンが祖父の節を吹き、エイラの笛が1小節遅れで追いかける。影が薄れて祖父の節が消えると、笛だけが残りの句を吹き終え、5度の音で止まる。",
       harm_scenes=None, tail_scene="笛だけ", fill=False, pads=True, pad_scenes=["呼びかけ", "追う1", "追う2", "影が薄れる", "笛だけ"], floor=True)
air = {"pre": 0.8, "tail": 8.0, "layers": [{"file": "0621", "db": -39, "hp": 150, "lp": 5000, "wide": 0.014, "duck": 0.35, "fade": 8}],
       "fx": {"shimmer": {"db": -28, "rt": 8.0}, "far": {"db": -24, "delay": 0.3, "lp": 2600, "rt": 5.0}}, "intro_db": 6.0}
json.dump(air, open("/tmp/cel/w/air056.json", "w"), ensure_ascii=False)
