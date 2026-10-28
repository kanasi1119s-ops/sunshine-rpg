# ケルト・フルート100曲「銀の笛と百の夜」017 夕立の予感 A Hint of Rain — 第2版（2026-10-28）
# イメージ: 明るい午後の草原。ふと西の空が暗くなる。同じ景色なのに、雲がかかると色が変わって見える。
#   ＝同じ旋律が、明るい長調から、くもったミクソリディア、影の短調へと移っていく。夕立の直前に短い影の山（遠い雷のようなティンパニ）、
#   そして雨の最初の粒が落ちはじめる所で、影の中に入って終わる。
# 形（台帳）: 主題と変奏（同じ旋律が長調→短調へ）。4/4・♩=56。D イオニア→D ミクソリディア→B エオリア→B（C♮の暗い影）。
#   始め：明るい笛ひとり／終わり：影に入る（短調のドローン）。終盤に短い影の山。
# 編曲の表:
#   晴れ1  : 笛ひとり（主題）
#   晴れ2  : ＋ピアノ（明るい和音）＋竪琴
#   雲     : ミクソリディア（C♮）。弦が入り、ピアノは低く
#   影     : 同じ音の並びを B の短調の和音で（同じ旋律なのに暗く聞こえる）。チェロ
#   夕立前 : 短い影の山。弦の刻み、低いチェロ、遠いティンパニのロール
#   影に入る: 短調のドローンだけ、笛のかけら、雨が降りはじめる
import sys
from c100_common import *
from c100_v2 import *

S = Song("C100", "017-a-hint-of-rain", "夕立の予感", "A Hint of Rain", 56, 4, "D", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.25})
TC = ["D", "G", "D", "A", "G", "D", "Em", "D"]
S.scene("晴れ1", 8, "intro", TC)
S.scene("晴れ2", 8, "verse", TC)
S.scene("雲", 16, "verse", ["D", "C", "D", "A", "G", "C", "Em", "D"] * 2)
S.scene("影", 16, "verse", ["Bm", "Em", "Bm", "F#m", "G", "D", "Em", "Bm"] * 2)
S.scene("夕立前", 8, "chorus", ["Bm", "C", "Bm", "F#m", "G", "C", "Em", "Bm"])
S.scene("影に入る", 8, "outro", ["Bm"] * 8)
NAMES = ["晴れ1", "晴れ2", "雲", "影", "夕立前", "影に入る"]

c = make(S, NAMES,
         [("晴れ1", 0, 0.62), ("晴れ2", 0, 0.66), ("雲", 0, 0.66), ("影", 0, 0.66), ("影", 15, 0.72), ("夕立前", 0, 0.78), ("夕立前", 5, 0.9),
          ("夕立前", 7, 0.74), ("影に入る", 0, 0.62), ("影に入る", 7, 0.36)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro=None, passing=True, tension=False)
PR = S.track("ピアノ（右手）", "piano", volume=0.2, pan=-0.15, reverb=0.45, barGain=c.g())
PR2 = S.track("ピアノ（右手2）", "piano", volume=0.17, pan=-0.12, reverb=0.45, barGain=c.g())
PL = S.track("ピアノ（左手）", "piano", volume=0.2, pan=-0.2, reverb=0.45, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.085, pan=0.2, reverb=0.45, barGain=c.g())
TIMP = S.track("遠いティンパニ", "strings", patch="timpani", volume=0.06, pan=0.3, reverb=0.7, gainDb=-6, barGain=c.g())

TH = ["3:1 5:1 6:1 5:1", "1':2 6:2", "5:1 3:1 2:1 3:1", "5:4", "6:1 5:1 3:1 2:1", "1:2 2:1 3:1", "2:1.5 1:0.5 6,:1 2:1", "1:4"]
THm = ["3:1 5:1 6:1 5:1", "1':2 6:2", "5:1 3:1 2:1 3:1", "5:4", "6:1 5:1 7:1 6:1", "5:2 4:1 3:1", "2:1.5 1:0.5 7,:1 2:1", "1:4"]   # ミクソリディア（C♮）
# B の短調：同じ音の並び（D 長調の音＝B 短調の音）で、終わりだけ B に落ちる
KB = S.key.__class__("B", "minor", 4)
TB = ["5:1 7:1 1':1 7:1", "3':2 1':2", "7:1 5:1 4:1 5:1", "7:4", "1':1 7:1 5:1 4:1", "3:2 4:1 5:1", "4:1.5 3:0.5 2:1 7,:1", "1:4"]
TP = ["5:1 7:1 1':1 7:1", "b2':2 1':2", "7:1 5:1 4:1 5:1", "7:4", "1':1 7:1 5:1 4:1", "3:2 b2:1 3:1", "4:1.5 3:0.5 b2:1 7,:1", "1:4"]
play_melody(c, "晴れ1", TH, 4, "air", density=0.6, seed=1701)
play_melody(c, "晴れ2", TH, 4, "air", density=0.9, seed=1702)
play_melody(c, "雲", THm + THm, 4, "air", key=S.key.__class__("D", "mixolydian", 4), density=0.8, seed=1703)
play_melody(c, "影", TB + TB, 4, "air", key=KB, density=0.8, seed=1704)
play_melody(c, "夕立前", TP, 4, "air", key=KB, density=1.0, seed=1705)
play_melody(c, "影に入る", ["5:2 4:2", "3:4", "R:4", "b2:2 1:2", "1:4", "R:4", "R:4", "R:4"], 4, "air", key=KB, density=0.4, seed=1706)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    hi = [x for x in range(60, 76) if x % 12 in chord_pcs(ch)]
    t = tones(ch, "D3", "D5")
    if n == "晴れ1": continue
    if n in ("晴れ2", "雲", "影"):
        PL.at(b * B, f"{nm(r if n != '晴れ2' else r + 12)}:2"); PL.at(b * B + 2, f"{nm(r + 7)}:2")
        PR.at(b * B, f"{nm(hi[1])}:2"); PR.at(b * B + 2, f"{nm(hi[2 % len(hi)])}:2"); PR2.at(b * B, f"{nm(hi[0])}:4")
    if n == "晴れ2": c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in (t[0], t[2], t[4 % len(t)], t[2])))
    if n in ("雲", "影", "夕立前"):
        v = voice(ch, 55 if n == "雲" else 52, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4" if n != "夕立前" else " ".join(f"{nm(v[j])}:0.5" for _ in range(8)))
    if n in ("影", "夕立前"): CELLO.bar(b, f"{nm(r)}:4" if n == "影" else f"{nm(r - 12 if r - 12 >= 36 else r)}:4")
    if n == "夕立前" and i in (3, 6): TIMP.bar(b, "R:2 " + " ".join(f"{nm(r)}:0.25" for _ in range(8)))
    if n == "影に入る":
        v = voice("Bm", 50, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4" if i < 7 else "R:4")
        if i < 7: CELLO.bar(b, "B1:4" if False else "B2:4")
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.36 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の017（第2版）。西の空が暗くなる午後。4/4・♩=56。主題と変奏：同じ旋律が D 長調→ミクソリディア→B 短調→C♮の影へ。夕立の前に短い影の山（遠いティンパニ）、雨が降りはじめる所で影の中に入って終わる。",
       harm_scenes=None, tail_scene="影に入る", fill=False, pads=True, pad_scenes=["雲", "影", "夕立前", "影に入る"])
