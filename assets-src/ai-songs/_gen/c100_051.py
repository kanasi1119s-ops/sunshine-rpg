# ケルト・フルート100曲「銀の笛と百の夜」051 湖への道 Down to the Lake（2026-10-29。第6章 霧の湖）
# イメージ: 石の塔をあとにしたエイラは、霧の中、草の斜面を湖へ下りていく。足もとはしめり、坂を一歩下りるごとに、
#   湖の気配が近くなる。坂の下で霧がひらけ、灰色の水面が広がる。
# 形: 坂を下る旋律（16小節）。回るたびに3度ずつ低い所から歌いだす（坂1＝A5から、坂2＝F5から、坂3＝D5から）。
#   坂1・坂2は主音に着かずに終わり（まだ坂の途中）、坂3で初めて主音 D に着く（湖に着いた）。
#   水辺では、笛は低い音域で静かに歌い、伴奏は逆に上へ開く（湖の上の広い空）。3/4・♩=52・D エオリア。山なし。
# ただひとつ: 旋律が下りていくほど、伴奏が上へ開いていく（笛と伴奏が反対へ動く）。
# 編曲の表:
#   霧の丘: 竪琴のローヴィング・サム（坂を歩く足どり）＋低い弦とチェロ
#   坂1   : 笛（高い）。弦は低い 2声、チェロ
#   坂2   : 笛（3度下）。弦3声が少し上へ。内声の動き
#   坂3   : 笛（5度下）。弦がさらに上へ、笛の和声
#   水辺  : 笛は低い音域の新しい節。弦は高い音域、竪琴の高い響き。ピアノの低い和音がひとつずつ
#   水面  : 低い D の長い音と、高く開いた弦
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 52
S = Song("C100", "051-down-to-the-lake", "湖への道", "Down to the Lake", BPM, 3, "D", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.22})
P = ["Dm", "Dm", "C", "C", "Bb", "Bb", "Am", "Am", "Gm", "Gm", "Dm", "Dm", "Bb", "C", "Dm", "Dm"]
S.scene("霧の丘", 4, "intro", ["Dm", "C", "Bb", "Am"])
S.scene("坂1", 16, "verse", P)
S.scene("坂2", 16, "verse", P)
S.scene("坂3", 16, "verse", P)
S.scene("水辺", 16, "chorus", ["Bb", "F", "C", "Dm", "Bb", "F", "Gm", "A", "Bb", "F", "C", "Dm", "Gm", "C", "Dm", "Dm"])
S.scene("水面", 5, "outro", ["Dm", "Bb", "Dm", "Dm", "Dm"])
NAMES = ["霧の丘", "坂1", "坂2", "坂3", "水辺", "水面"]

c = make(S, NAMES,
         [("霧の丘", 0, 0.62), ("坂1", 0, 0.64), ("坂2", 0, 0.68), ("坂3", 0, 0.7), ("坂3", 15, 0.72), ("水辺", 0, 0.74), ("水辺", 12, 0.74),
          ("水面", 0, 0.68), ("水面", 4, 0.5)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="霧の丘", passing=True, tension=False)
CELLO = S.track("チェロ（深い）", "strings", patch="cello", volume=0.08, pan=0.15, reverb=0.5, barGain=c.g())
PL = S.track("ピアノ（低い和音）", "piano", volume=0.8, pan=-0.2, reverb=0.55, barGain=c.g())

# 坂を下る旋律（A5→A4。最後は5度 A で、まだ坂の途中）
M = ["5':2 4':1", "3':1.5 2':0.5 1':1", "7:2 1':1", "5:2 6:1",
     "6:2 5:1", "6:1 7:1 1':1", "2':2 7:1", "7:3",
     "1':1.5 7:0.5 6:1", "6:2 7:1", "1':2 2':1", "3':3",
     "4':1 3':1 1':1", "7:1.5 1':0.5 6:1", "5:2 6:1", "5:3"]
play_melody(c, "坂1", M, 4, "air", density=0.45, seed=5101)
play_melody(c, "坂2", [dshift(x, -2) for x in M], 4, "air", density=0.6, seed=5102)
M3 = [dshift(x, -4) for x in M]; M3[-1] = "1:3"                       # 坂3：最後に初めて主音 D に着く
play_melody(c, "坂3", M3, 4, "air", density=0.7, seed=5103)
# 水辺：低い音域の新しい節（D4〜A4 のあたり。湖の静けさ）
W = ["4:2 3:1", "3:1.5 4:0.5 5:1", "5:2 3:1", "2:1 1:2",
     "2:2 1:1", "1:1.5 2:0.5 3:1", "4:2 2:1", "#7,:3",
     "4:1 5:1 6:1", "5:2 3:1", "3:1 2:1 3:1", "4:2 5:1",
     "4:1.5 3:0.5 2:1", "3:1 2:1 7,:1", "1:3", "1:3"]
play_melody(c, "水辺", W, 4, "air", density=0.5, seed=5104)
play_melody(c, "水面", ["5:2 4:1", "4:3", "1:3", "1:3", "R:3"], 4, "air", density=0.2, seed=5105)

B = S.beats
LIFT = {"霧の丘": 48, "坂1": 50, "坂2": 54, "坂3": 58, "水辺": 64, "水面": 67}   # 笛が下りるほど、弦は上へ
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    nv = 2 if n == "坂1" else 3
    v = voice(ch, LIFT[n], nv, spread=True)
    if not (n == "水面" and i == 4):
        for j in range(nv): c.STR[j].bar(b, f"{nm(v[j])}:3")
    else:
        for j in range(nv): c.STR[j].bar(b, f"{nm(v[j])}:2 R:1")
    CELLO.bar(b, f"{nm(r)}:3")
    if n in ("霧の丘", "坂1", "坂2", "坂3"):
        roving_thumb(c.HARP, b, B, ch, up=(i % 2 == 0))
    if n == "水辺":
        hi = tones(ch, "D5", "D6")
        c.HARP2.bar(b, " ".join(f"{nm(hi[q % len(hi)])}:1" for q in ((0, 2, 1) if i % 2 == 0 else (2, 1, 3))))
        if i % 2 == 0: PL.bar(b, f"{nm(r)}:3")
        else: PL.bar(b, f"{nm(r + 7)}:1.5 {nm(r + 12)}:1.5")
    if n == "水面" and i < 4:
        c.HARP2.bar(b, f"{nm(tones(ch, 'D5', 'D6')[1])}:3")
        PL.bar(b, f"{nm(r)}:3")
rich(c, choir_scenes=["坂3"], pulse_scenes=["坂2", "坂3", "水辺"], guitar=False, pizz=False, inner=True)
sparkle(c)   # 2026-10-29: 高いきらめきの層（017 で 7.05→7.27。合格した静かな曲には、どれもこの層がある）
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.38 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の051。霧の中、草の斜面を湖へ下りていく。3/4・♩=52、D エオリア。坂を下る旋律が、回るたびに3度ずつ低い所から歌いだし、3回目で初めて主音に着く（湖に着く）。笛が下りるほど弦は上へ開き、水辺では笛は低く、空は高く広がる。",
       harm_scenes=None, tail_scene="水面", fill=False, pads=True, pad_scenes=["坂1", "坂2", "坂3", "水辺", "水面"], floor=True)
air = {"pre": 0.6, "tail": 7.0, "layers": [{"file": "0691", "db": -38, "hp": 150, "lp": 5000, "wide": 0.014, "duck": 0.35, "fade": 8}],
       "fx": {"shimmer": {"db": -29, "rt": 7.0}, "far": {"db": -25, "delay": 0.25, "lp": 2800, "rt": 4.5}}, "intro_db": 6.0}
json.dump(air, open("/tmp/cel/w/air051.json", "w"), ensure_ascii=False)
