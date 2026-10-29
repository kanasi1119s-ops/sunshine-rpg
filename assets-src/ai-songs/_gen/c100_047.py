# ケルト・フルート100曲「銀の笛と百の夜」047 夜の見張り台 The Watchtower at Night（2026-10-29）
# イメージ: 塔のいちばん上の見張り台。夜の海と、遠くの岬を、じっと見ている。長い音で遠くへ呼びかけると、
#   はるか向こうの見張り台から、同じ音が小さく返ってくる（ほんとうに誰かいるのか、こだまなのか）。最後は、二つの灯がそっと寄りそう。
# 形: 遠くを見る長い音。見張り2では、笛の長い音のあとに、遠くの笛が同じ音で返事をする。遠い灯では二人が和音で寄りそう。4/4・♩=46。B エオリア。山なし。
# ただひとつ: 遠くの笛（小さく・右の遠く・深い響き）が、笛の呼びかけに同じ音で答える。
# 編曲の表:
#   夜風    : 低い弦の和音とチェロ、竪琴の低い音（はじまりから厚く）
#   見張り1 : 笛の長い呼びかけ。休む小節は竪琴が星のように答える
#   見張り2 : 休む小節に、遠くの笛が同じ音で返事をする。弦3声
#   遠い灯  : 遠くの笛が3度下で寄りそい、二人の和音になる。内声の動き
#   夜明け前: 弦の和音が残る
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 46
S = Song("C100", "047-the-watchtower-at-night", "夜の見張り台", "The Watchtower at Night", BPM, 4, "B", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.25})
WC = ["Bm", "G", "F#m", "F#m", "G", "D", "Bm", "Bm", "A", "Em", "Em", "Em", "Bm", "A", "Bm", "Bm"]
S.scene("夜風", 3, "intro", ["Bm", "Bm", "Em"])
S.scene("見張り1", 16, "verse", WC)
S.scene("見張り2", 16, "verse", WC)
S.scene("遠い灯", 8, "verse", ["G", "D", "Em", "Bm", "G", "A", "Bm", "Bm"])
S.scene("夜明け前", 5, "outro", ["G", "Em", "Bm", "Bm", "Bm"])
NAMES = ["夜風", "見張り1", "見張り2", "遠い灯", "夜明け前"]

c = make(S, NAMES,
         [("夜風", 0, 0.62), ("見張り1", 0, 0.64), ("見張り2", 0, 0.68), ("遠い灯", 0, 0.72), ("遠い灯", 7, 0.68), ("夜明け前", 0, 0.62), ("夜明け前", 4, 0.45)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="夜風", passing=True, tension=False)
FAR = S.track("遠くの見張り台の笛", "panflute", patch="flute", volume=0.2, bright=-1.0, pan=0.6, reverb=0.85, breath=False,
              noRestrike=True, mono=True, sustain=1.15, phrase=16, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.085, pan=0.1, reverb=0.5, barGain=c.g())
CB = S.track("コントラバス", "strings", patch="contrabass", volume=0.07, pan=0.0, reverb=0.5, barGain=c.g())

M = ["5:4", "4:2 3:2", "2:4", "R:4", "3:4", "4:2 5:2", "1':4", "R:4", "7:4", "6:2 5:2", "4:4", "R:4", "5:2 4:2", "3:2 2:2", "1:4", "R:4"]
ECHO = ["R:4"] * 3 + ["R:1 2:3"] + ["R:4"] * 3 + ["R:1 1':3"] + ["R:4"] * 3 + ["R:1 4:3"] + ["R:4"] * 3 + ["R:1 1:3"]
LIGHT = ["5:2 6:2", "5:4", "4:2 5:2", "3:4", "4:2 5:2", "6:2 7:2", "1':4", "1':4"]
play_melody(c, "見張り1", M, 4, "air", density=0.4, seed=4701)
play_melody(c, "見張り2", M, 4, "air", density=0.6, seed=4702)
play_melody(c, "見張り2", ECHO, 4, "air", density=0.0, track=FAR)
play_melody(c, "遠い灯", LIGHT, 4, "air", density=0.6, seed=4703)
play_melody(c, "夜明け前", ["5:4", "4:2 3:2", "1:4", "R:4", "R:4"], 4, "air", density=0.2, seed=4704)
# 遠い灯：遠くの笛が3度下（和音の音）で寄りそう
B = S.beats
a, z = c.s0["遠い灯"] * B, (c.s0["遠い灯"] + 8) * B
for st, Ln, x in list(c.FLUTE.ev):
    p = midi_of(x)
    if p is None or not (a <= st < z) or Ln < 0.9: continue
    pcs = chord_pcs(S.chords[int(st // B)])
    h = next((q for q in range(p - 3, p - 6, -1) if q % 12 in pcs), p - 3)
    if h >= 60: FAR.at(st + 0.04, f"{nm(h)}:{x.split(':', 1)[1]}")

for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "B2", "B5")
    if n == "夜明け前" and i == 4: continue
    CELLO.bar(b, f"{nm(r)}:4"); CB.bar(b, f"{nm(r - 12 if r - 12 >= 28 else r)}:4")
    nv = 2 if n == "見張り1" else 3
    v = voice(ch, 52 if n in ("夜風", "見張り1") else 55, nv, spread=True)
    for j in range(nv): c.STR[j].bar(b, f"{nm(v[j])}:4")
    if n == "夜風": c.HARP.bar(b, f"{nm(t[0])}:2 {nm(t[2])}:2")
    if n in ("見張り1", "見張り2") and i % 4 == 3:   # 呼びかけのあと：竪琴が星のように
        hi = tones(ch, "B5", "B6"); c.HARP2.bar(b, " ".join(f"{nm(hi[q % len(hi)])}:1" for q in (0, 2, 1, 3)))
    if n in ("見張り1", "見張り2") and i % 4 != 3: c.HARP.bar(b, f"{nm(t[0])}:2 {nm(t[2])}:1 {nm(t[4 % len(t)])}:1")
    if n == "遠い灯": c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in (t[0], t[2], t[4 % len(t)], t[5 % len(t)])))
rich(c, choir_scenes=[], pulse_scenes=["見張り2", "遠い灯"], guitar=False, pizz=False, inner=True)
sparkle(c)   # 2026-10-29: 高いきらめきの層（017 で 7.05→7.27。合格した静かな曲には、どれもこの層がある）
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.4 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の047。塔の上の見張り台から、夜の海を見る。4/4・♩=46、B エオリア。笛が長い音で遠くへ呼びかけると、はるか向こうの見張り台の笛が同じ音で小さく返事をする。最後は二人の笛が和音で寄りそう。山なし。",
       harm_scenes=None, tail_scene="夜明け前", fill=False, pads=True, pad_scenes=["見張り1", "見張り2", "遠い灯", "夜明け前"], floor=True)
air = {"pre": 0.8, "tail": 8.0, "layers": [{"file": "0110", "db": -36, "hp": 150, "lp": 6000, "wide": 0.014, "duck": 0.35, "fade": 8},
                                           {"file": "0266", "db": -40, "hp": 100, "lp": 3000, "wide": 0.016, "pan": -0.2, "duck": 0.35, "fade": 10}],
       "fx": {"shimmer": {"db": -28, "rt": 9.0}, "far": {"db": -24, "delay": 0.35, "lp": 2400, "rt": 5.5}}, "intro_db": 6.0}
json.dump(air, open("/tmp/cel/w/air047.json", "w"), ensure_ascii=False)
