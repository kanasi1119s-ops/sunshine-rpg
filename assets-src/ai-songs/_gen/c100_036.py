# ケルト・フルート100曲「銀の笛と百の夜」036 迷いの道 Paths That Turn — 第2版（2026-10-28）
# イメージ: 森で、同じ道に何度も戻ってきてしまう。景色は同じなのに、そのたびに光の色や気分がちがって見える。
#   ＝同じ旋律を5回。毎回ちがう和音がつく（明るい・暗い・不安・やさしい…）。最後の6回目で、同じ旋律に初めて「出口」の和音（G の長三和音）がつく。
# 形（台帳）: 同じ旋律を5回、毎回ちがう和音で巡る（迷いの円環）。4/4・♩=56。G ドリア。始め：A（旋律）／終わり：A（違う和音で閉じる）。山なし。
# 編曲の表:
#   1回目 : 笛＋ピアノ（素直な和音）
#   分かれ目: ピアノの2小節（道が分かれる）
#   2回目 : 明るい和音（E♭・B♭）。弦がうすく
#   3回目 : 暗い和音（Cm・Gm）。チェロ
#   4回目 : 不安な和音（D の長三和音、半音ずれる響き）。ピチカートがためらう
#   5回目 : やさしい和音（maj7）。竪琴
#   出口   : 同じ旋律に、初めて G の長三和音が来る
import sys, json
from c100_common import *
from c100_v2 import *

S = Song("C100", "036-paths-that-turn", "迷いの道", "Paths That Turn", 56, 4, "G", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.25})
H = [["Gm", "Dm", "Gm", "F", "Gm", "C", "Dm", "F"],
     ["Eb", "Bb", "Eb", "Dm", "C", "Am", "Bb", "D"],
     ["Cm", "Gm", "Bb", "Bb", "Eb", "F", "Gm", "Dm"],
     ["C", "D", "Cm7", "Dm", "Cm", "Am", "F", "A"],
     ["Ebmaj7", "Bbmaj7", "Gm7", "F", "Cm7", "Fmaj7", "Bbmaj7", "F"],
     ["Gm", "Dm", "Eb", "F", "Cm", "C", "D", "G"]]
S.scene("1回目", 8, "verse", H[0])
for k in range(1, 5):
    S.scene(f"分かれ目{k}", 2, "break", [H[k - 1][-1], H[k][0]])
    S.scene(f"{k + 1}回目", 8, "verse", H[k])
S.scene("分かれ目5", 2, "break", ["F", "Gm"])
S.scene("出口", 8, "chorus", H[5])
S.scene("抜けた", 4, "outro", ["G", "C", "G", "G"])
NAMES = [n for n, *_ in S.scenes]

c = make(S, NAMES, [("1回目", 0, 0.62), ("3回目", 0, 0.66), ("4回目", 0, 0.68), ("5回目", 0, 0.66), ("出口", 0, 0.72), ("出口", 7, 0.76), ("抜けた", 3, 0.4)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro=None, passing=True, tension=False)
PR = S.track("ピアノ（右手）", "piano", volume=0.5, pan=-0.15, reverb=0.45, barGain=c.g())
PR2 = S.track("ピアノ（右手2）", "piano", volume=0.42, pan=-0.12, reverb=0.45, barGain=c.g())
PL = S.track("ピアノ（左手）", "piano", volume=0.5, pan=-0.2, reverb=0.45, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.08, pan=0.15, reverb=0.45, barGain=c.g())
PIZZ = S.track("ピチカート", "strings", patch="pizzicato", volume=0.06, pan=0.35, reverb=0.4, barGain=c.g())

M = ["1:2 3:1 4:1", "5:3 4:1", "3:2 2:1 1:1", "7,:2 5,:2", "1:1 2:1 3:2", "4:2 6:2", "5:2 4:1 3:1", "2:4"]
for k in range(5): play_melody(c, f"{k + 1}回目", M, 4, "air", density=0.3 + 0.15 * k, seed=3600 + k)
play_melody(c, "出口", M[:7] + ["1:4"], 4, "air", density=0.8, seed=3606, key=S.key.__class__("G", "dorian", 4))
play_melody(c, "抜けた", ["3:4", "1:4", "R:4", "R:4"], 4, "air", key=S.key.__class__("G", "major", 4), density=0)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    hi = [x for x in range(58, 74) if x % 12 in chord_pcs(ch)]
    if n == "抜けた" and i >= 3: continue
    PL.at(b * B, f"{nm(r)}:2"); PL.at(b * B + 2, f"{nm(r + 7)}:2")
    PR2.at(b * B, f"{nm(hi[0])}:4"); PR.at(b * B + (2 if n.startswith("分かれ目") else 0), f"{nm(hi[1])}:{2 if n.startswith('分かれ目') else 4}")
    if True:   # 弦は最初から最後まで（分かれ目で音が落ちないように）
        v = voice(ch, 52 if n == "1回目" else 55, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
    if n.startswith("分かれ目"):   # 道が分かれる：竪琴が上って下りる（どっちへ行こう）
        t = tones(ch, "G3", "G6"); c.HARP.bar(b, " ".join(f"{nm(x)}:0.5" for x in (t[0], t[2], t[4], t[6 % len(t)], t[7 % len(t)], t[6 % len(t)], t[4], t[2])))
    CELLO.bar(b, f"{nm(r)}:4")
    if False: CELLO.bar(b, f"{nm(r)}:4")
    if n == "4回目": PIZZ.bar(b, f"{nm(hi[0])}:1 R:1.5 {nm(hi[1])}:0.5 R:1")
    if n in ("5回目", "出口"): c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in tones(ch, "G3", "G5")[:4]))
rich(c, choir_scenes=["5回目", "出口"], pulse_scenes=["2回目", "3回目", "4回目", "5回目", "出口"], guitar=False, pizz=False, inner=True, choir_vol=0.1)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.36 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の036（第2版）。森で同じ道に何度も戻ってくる。4/4・♩=56、G ドリア。同じ旋律を5回、毎回ちがう和音（素直・明るい・暗い・不安・やさしい）で巡り、6回目で初めて出口の G の長三和音が来る。",
       harm_scenes=None, tail_scene="抜けた", fill=False, pads=True, pad_scenes=[n for n in NAMES if n != "抜けた"], floor=True)
json.dump({"pre": 1.0, "tail": 8.0, "layers": [{"file": "0905", "db": -35, "hp": 120, "lp": 6000, "wide": 0.016, "duck": 0.3, "fade": 6}],
           "fx": {"glass": {"hz": [392.0, 784.0, 1174.7], "db": -29, "rt": 6.0, "start": 4}, "shimmer": {"db": -28, "rt": 8.0}, "far": {"db": -25, "delay": 0.25, "lp": 2600, "rt": 4.5},
                  "haze": {"db": -27, "rt": 8.0}, "band": {"db": -37, "hz": 6500, "per": 23}}, "intro_db": 8.5}, open("/tmp/cel/w/air036.json", "w"))
