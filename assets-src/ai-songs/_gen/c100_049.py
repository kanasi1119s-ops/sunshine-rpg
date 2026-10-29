# ケルト・フルート100曲「銀の笛と百の夜」049 蔦の窓 Window of Ivy（2026-10-29）
# イメージ: 秘密の入口の先の、薄暗い小部屋。壁いっぱいの蔦の間に、小さな窓がある。日が昇るにつれて、葉のすき間から光がもれ、
#   光の帯がだんだん部屋の奥まで届く。最後に、窓からまっすぐ一筋の光が射しこむ。
# 形: 影から光へ、ゆっくり上がっていく（旋律の音域も、竪琴の音域も、場面ごとに上へ）。3/4・♩=54。A リディア（D♯の光）。山なし。
# ただひとつ: 最後に、笛のいちばん高い長い音が4小節のびて、光の筋になる（その下で竪琴とグロッケンの粒が光る）。
# 編曲の表:
#   影        : 低い弦とチェロ、竪琴の低い3音のオスティナート（はじまりから厚く）
#   影から    : 笛が低い所で
#   葉のすき間: 笛が中ほどへ。グロッケンが葉のすき間の光の粒
#   光の帯    : 笛が高い所へ。竪琴のオスティナートも1オクターブ上へ。弦が上の音域へ。内声
#   一筋      : 笛のいちばん高い長い音。高い弦、グロッケン
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 54
S = Song("C100", "049-window-of-ivy", "蔦の窓", "Window of Ivy", BPM, 3, "A", "lydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.2})
LC = ["A", "B", "C#m", "B", "A", "F#m", "E", "A"]
S.scene("影", 4, "intro", ["F#m", "E", "F#m", "E"])
S.scene("影から", 16, "verse", ["F#m", "E", "D", "E", "F#m", "B", "E", "A"] * 2)
S.scene("葉のすき間", 16, "verse", LC * 2)
S.scene("光の帯", 24, "verse", LC * 3)
S.scene("一筋", 12, "chorus", ["A", "B", "A", "B", "A", "B", "C#m", "B", "A", "A", "A", "A"])
NAMES = ["影", "影から", "葉のすき間", "光の帯", "一筋"]
LEVEL = {"影": 0, "影から": 0, "葉のすき間": 1, "光の帯": 2, "一筋": 3}

c = make(S, NAMES,
         [("影", 0, 0.6), ("影から", 0, 0.62), ("葉のすき間", 0, 0.66), ("光の帯", 0, 0.72), ("光の帯", 23, 0.78), ("一筋", 0, 0.8), ("一筋", 8, 0.74), ("一筋", 11, 0.5)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="影", passing=True, tension=False)
GLOCK = S.track("光の粒（グロッケン）", "bell", patch="glockenspiel", volume=0.04, pan=0.4, reverb=0.7, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.08, pan=0.12, reverb=0.45, barGain=c.g())

M0 = ["1:2 2:1", "3:3", "2:2 1:1", "7,:3", "1:2 3:1", "4:3", "3:2 2:1", "1:3"]
M1 = ["3:2 4:1", "5:3", "4:2 3:1", "2:3", "3:2 5:1", "6:3", "5:2 4:1", "3:3"]
M2 = ["5:2 6:1", "7:3", "6:2 5:1", "4:3", "5:2 7:1", "1':3", "7:2 6:1", "5:3"]
play_melody(c, "影から", M0 * 2, 4, "air", density=0.4, seed=4901)
play_melody(c, "葉のすき間", M1 * 2, 4, "air", density=0.6, seed=4902)
play_melody(c, "光の帯", M2 * 3, 4, "air", density=0.7, seed=4903)
play_melody(c, "一筋", ["5:2 6:1", "7:2 1':1", "2':3", "2':3", "2':3", "2':3", "1':2 7:1", "6:3", "5:3", "5:3", "R:3", "R:3"], 4, "air", density=0.2, seed=4904)

B = S.beats
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    lv = LEVEL[n]
    if n == "一筋" and i >= 11: continue
    base = ["A2", "A3", "A4", "A4"][lv]
    harp_ostinato(c.HARP, b, B, tones(ch, base, "A6")[:3])          # 竪琴の3音のオスティナート（場面ごとに上へ）
    CELLO.bar(b, f"{nm(r)}:3")
    v = voice(ch, [50, 53, 57, 62][lv], 3, spread=True)
    for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:3")
    if lv >= 1 and (i % 2 == 1 or lv >= 3):                          # 葉のすき間の光の粒
        hi = tones(ch, "A5", "A7")
        GLOCK.bar(b, f"R:{1 + (i % 2)} {nm(hi[(i + lv) % len(hi)])}:{2 - (i % 2)}")
rich(c, choir_scenes=["光の帯"], pulse_scenes=["葉のすき間", "光の帯", "一筋"], guitar=False, pizz=False, inner=True, choir_vol=0.1)
sparkle(c)   # 2026-10-29: 高いきらめきの層（017 で 7.05→7.27。合格した静かな曲には、どれもこの層がある）
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.36 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の049。蔦におおわれた窓から、光が射しこむ。3/4・♩=54、A リディア。影から光へ、旋律も竪琴の3音のオスティナートも場面ごとに上へ上がっていく。最後に、笛のいちばん高い長い音が4小節のびて、光の筋になる。",
       harm_scenes=None, tail_scene="一筋", fill=False, pads=True, pad_scenes=["影から", "葉のすき間", "光の帯", "一筋"], floor=True)
air = {"pre": 0.8, "tail": 7.0, "layers": [{"file": "0904", "db": -38, "hp": 150, "lp": 6000, "wide": 0.014, "duck": 0.35, "fade": 8},
                                           {"file": "0222", "db": -41, "hp": 400, "lp": 9000, "wide": 0.012, "pan": 0.3, "duck": 0.35, "start": 90, "fade": 25}],
       "fx": {"shimmer": {"db": -27, "rt": 8.0}, "far": {"db": -25, "delay": 0.25, "lp": 2600, "rt": 4.5}}, "intro_db": 6.0}
json.dump(air, open("/tmp/cel/w/air049.json", "w"), ensure_ascii=False)
