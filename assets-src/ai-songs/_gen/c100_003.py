# ケルト・フルート100曲「銀の笛と百の夜」003 祖父の手紙 Grandfather's Letter — 第2版（2026-10-28）
# イメージ: 机の引き出しから、祖父の手紙が出てくる。ピアノが祖父の声のように手紙の節を語り（笛はまだ聞いているだけ）、
#   2回目にエイラの笛がその節をなぞって答える。読み終えて、しばらく黙る（ピアノの和音だけが残る）。
#   そして「旅に出よう」と決める所で、同じ節が長調に変わって明るむ。最後は笛の長い音。
# 形（台帳）: ピアノ組曲（笛は2周目から）・短調→最後に長調。4/4・♩=52。D エオリア→D イオニア。山なし・最後に明るむ。
# 編曲の表:
#   前置き : ピアノの低音（D のオクターブと5度）。紙をめくる音（空気の層）
#   語り1  : ピアノだけ（右手が旋律、左手は5度とオクターブ）
#   語り2  : 笛が同じ節で答える。ピアノは右手を3度・6度の長い和音に、左手はそのまま。B で竪琴の根音
#   沈黙   : 笛は休み、ピアノの和音と弦がのびるだけ（読み終えて黙る）
#   決意   : 同じ節が長調に。弦・竪琴の分散和音・チェロ。笛は少し高い所で
#   終わり : 笛の長い音とピアノの和音
import sys
from c100_common import *
from c100_v2 import *

S = Song("C100", "003-grandfathers-letter", "祖父の手紙", "Grandfather's Letter", 52, 4, "D", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"rubato": 0.35, "human": 0.4})
TA = ["Dm", "Bb", "Gm", "A", "Dm", "Bb", "C", "Dm"]
TB = ["F", "C", "Bb", "F", "Gm", "Dm", "C", "Dm"]
MA = ["D", "G", "Em", "A", "D", "G", "A", "D"]
S.scene("前置き", 2, "intro", ["Dm", "Dm"])
S.scene("語り1", 16, "verse", TA + TA)
S.scene("語り2", 16, "verse", TA + TB)
S.scene("沈黙", 2, "break", ["Bb", "A"])
S.scene("決意", 16, "chorus", MA + ["G", "D", "Em", "A", "G", "D", "A", "D"])
S.scene("終わり", 4, "outro", ["D", "G", "D", "D"])
NAMES = ["前置き", "語り1", "語り2", "沈黙", "決意", "終わり"]

c = make(S, NAMES,
         [("前置き", 0, 0.6), ("語り1", 0, 0.62), ("語り1", 15, 0.62), ("語り2", 0, 0.64), ("語り2", 12, 0.72), ("沈黙", 0, 0.58),
          ("決意", 0, 0.66), ("決意", 12, 0.8), ("終わり", 0, 0.66), ("終わり", 3, 0.45)],
         {}, flute_gain={n: 1.25 for n in NAMES}, intro="前置き", passing=True, tension=False)
PR = S.track("ピアノ（右手）", "piano", volume=0.13, pan=-0.12, reverb=0.45, barGain=c.g())
PR2 = S.track("ピアノ（右手の和音）", "piano", volume=0.1, pan=-0.08, reverb=0.45, barGain=c.g())
PL = S.track("ピアノ（左手）", "piano", volume=0.11, pan=-0.2, reverb=0.45, barGain=c.g())
PL2 = S.track("ピアノ（左手の上）", "piano", volume=0.08, pan=-0.16, reverb=0.45, barGain=c.g())
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.08, pan=0.25, reverb=0.45, barGain=c.g())

TH = ["5,:1 1:1 2:1 3:1", "4:2 3:1 2:1", "3:1.5 2:0.5 1:1 7,:1", "5,:4",
      "5,:1 1:1 2:1 3:1", "5:2 4:1 3:1", "2:1 3:1 4:1 2:1", "1:4"]
TH2 = ["3:1 4:1 5:1 6:1", "7:2 6:1 5:1", "4:1 5:1 6:1 4:1", "5:4",
       "6:1 5:1 4:1 3:1", "4:2 3:1 2:1", "3:1 2:1 7,:1 2:1", "1:4"]
# 語り1：ピアノの右手が節を語る（祖父の声）
for t, L, m in section_events(c, "語り1", TH + TH[:7] + ["1:4"], 4):
    PR.at(t, f"{nm(m)}:{L}")
# 語り2：笛が答える
play_melody(c, "語り2", TH + TH2, 4, "air", density=0.8, seed=301)
# 決意：同じ節が長調に（D イオニア）。少し高い所で
KM = S.key.__class__("D", "major", 5)
play_melody(c, "決意", TH + TH2[:7] + ["1:4"], 4, "air", key=KM, density=1.0, seed=302)
play_melody(c, "終わり", ["5:2 3:2", "1:4", "1:4", "R:4"], 4, "air", key=KM, density=0)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    if n == "前置き":
        PL.at(b * B, "D2:4"); PL2.at(b * B, "D3:2"); PL2.at(b * B + 2, "A3:2")
        continue
    # 左手：5度とオクターブをゆっくり
    PL.at(b * B, f"{nm(r)}:4"); PL2.at(b * B + 1, f"{nm(r + 7)}:1"); PL2.at(b * B + 2, f"{nm(r + 12)}:2")
    if n in ("語り2", "決意", "終わり", "沈黙"):
        hi = [x for x in range(62, 76) if x % 12 in chord_pcs(ch)][:3]
        PR2.at(b * B, f"{nm(hi[0])}:4")                      # 右手：3度・6度の長い和音（2つのパートに分ける）
        if n != "語り1": PR.at(b * B, f"{nm(hi[1])}:4")
    if n == "語り2" and i >= 8: c.HARP.bar(b, f"{nm(r)}:4")
    if n == "沈黙":
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
    if n in ("決意", "終わり"):
        v = voice(ch, 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        t = tones(ch, "D3", "D5")
        if n == "決意": c.HARP.bar(b, " ".join(f"{nm(x)}:0.5" for x in (t[0], t[2], t[4 % len(t)], t[2]) * 2))
        CELLO.bar(b, f"{nm(r)}:4")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.34 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の003（第2版）。祖父の手紙を読む。D・4/4・♩=52。ピアノが祖父の声のように節を語り、2回目に笛が答える。読み終えて黙り、旅に出ると決める所で同じ節が長調に明るむ。最後は笛の長い音。",
       harm_scenes=None, tail_scene="終わり", fill=False, pads=True, pad_scenes=["語り2", "決意", "終わり"])
