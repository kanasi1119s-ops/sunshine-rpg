# ケルト・フルート100曲「銀の笛と百の夜」003 祖父の手紙 Grandfather's Letter（2026-10-28）。表は docs/sound/celtic-flute-100-plan.md
# 物語: 机の引き出しの奥から祖父の手紙が出てくる。読み始める（語り）→声がつまる→静かな沈黙→「行こう」と決める。最後にほんの少し明るむ。
# 型: 語りかけるような、息継ぎの多い旋律。ピアノは語り手の相づち。始め：低いピアノ／終わり：笛の長音。山なし。
# 強さ: 前奏(pp)→語り1(p)→語り2(p→mp)→沈黙(ppp。ピアノと弦だけ)→決意(mp)→終わり(pp。最後に D 長調へ明るむ)
import sys
from c100_common import *

S = Song("C100", "003-grandfathers-letter", "祖父の手紙", "Grandfather's Letter", 52, 4, "D", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.scene("前奏", 4, "intro", ["Dm", "Dm", "Bb", "Gm"])
S.scene("語り1", 12, "verse", ["Dm", "Bb", "F", "C", "Dm", "Gm", "Bb", "F", "Gm", "Dm", "C", "Dm"])
S.scene("語り2", 12, "verse", ["Bb", "F", "C", "Dm", "Gm", "Dm", "Bb", "C", "F", "C", "Dm", "Am"])
S.scene("沈黙", 6, "break", ["Dm", "Dm", "Gm", "Dm", "Am", "Dm"])
S.scene("決意", 12, "chorus", ["Bb", "F", "C", "Dm", "Gm", "Bb", "F", "C", "Dm", "Bb", "C", "Dm"])
S.scene("終わり", 8, "outro", ["Dm", "Dm", "Dm", "Dm", "D", "D", "D", "D"])
NAMES = ["前奏", "語り1", "語り2", "沈黙", "決意", "終わり"]

c = make(S, NAMES,
         [("前奏", 0, 0.72), ("語り1", 0, 0.66), ("語り2", 0, 0.7), ("語り2", 10, 0.8), ("沈黙", 0, 0.45), ("沈黙", 5, 0.4),
          ("決意", 0, 0.7), ("決意", 9, 0.92), ("終わり", 0, 0.55), ("終わり", 7, 0.35)],
         {"語り1": 0.55, "語り2": 0.55, "決意": 0.6, "終わり": 0.8},
         flute_gain={"語り1": 1.4, "語り2": 1.3, "決意": 1.2, "終わり": 1.1}, intro="前奏", passing=True)
PIANO = S.track("ピアノ", "piano", volume=0.13, pan=-0.1, reverb=0.4, barGain=c.g())

# ---------- 旋律（D エオリアン。語りかけるように、息継ぎを多く） ----------
put_melody(c, "語り1", [
    ["R:1 5,:1 1:2", "3:1.5 2:0.5 1:2", "R:2 2:1 3:1", "1:3 R:1"],
    ["R:1 3:1 5:2", "4:1.5 3:0.5 2:2", "R:1 3:1 2:1 1:1", "7,:3 R:1"],
    ["R:2 5,:1 7,:1", "1:2 2:1 3:1", "2:3 R:1", "1:4"]], 5)
put_melody(c, "語り2", [
    ["R:1 1:1 3:2", "5:2 R:1 4:1", "3:1 4:1 5:2", "6:3 R:1"],
    ["R:2 5:1 6:1", "7:1.5 6:0.5 5:2", "R:1 4:1 3:1 2:1", "1:3 R:1"],
    ["R:1 1:1 2:1 3:1", "5:3 R:1", "4:1 3:1 2:1 1:1", "7,:4"]], 5)
put_melody(c, "決意", [
    ["1:2 3:2", "5:2 3:2", "4:2 2:2", "1:3 R:1"],
    ["3:2 5:2", "6:2 5:2", "4:1 3:1 2:2", "3:3 R:1"],
    ["5:2 6:1 5:1", "3:2 2:2", "1:2 7,:2", "1:4"]], 5)
put_bars(c, "終わり", ["R:4", "3:4", "R:4", "5:4", "R:4", "5:4", "5:4", "5:4"], 5)

# ---------- 伴奏 ----------
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    lo = low(ch, "C2"); t = tones(ch, "D3", "D6")
    if n == "前奏":
        PIANO.bar(b, f"{nm(lo)}:2 {nm(lo + 7)}:2")
        if i >= 1: c.HARP2.bar(b, f"R:2 {nm(t[-3])}:2")
        v = voice(ch, 62, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
    elif n in ("語り1", "語り2"):
        PIANO.bar(b, f"{nm(lo)}:2 {nm(lo + 7)}:1 {nm(lo + 12)}:1")                       # 左手：根音・5度・オクターブ
        if i % 4 == 3: c.HARP2.bar(b, f"R:2 {nm(t[-2])}:2")
        if n == "語り2" or i >= 4:
            v = voice(ch, 62, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        if n == "語り2" and i >= 4: c.LOW.bar(b, f"{nm(lo + 12 if lo < 40 else lo)}:4")
    elif n == "沈黙":
        PIANO.bar(b, f"{nm(lo)}:4" if i % 2 == 0 else f"{nm(lo + 7)}:4")                # ピアノだけが、ひとつずつ
        v = voice(ch, 60, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
    elif n == "決意":
        PIANO.bar(b, f"{nm(lo)}:2 {nm(lo + 7)}:1 {nm(lo + 12)}:1")
        c.HARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:1" for q in (0, 2, 4, 2)))
        c.LOW.bar(b, f"{nm(lo + 12 if lo < 40 else lo)}:4")
        v = voice(ch, 62, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
    elif n == "終わり":
        if i in (0, 2, 4): PIANO.bar(b, f"{nm(lo)}:4")
        if i < 6:
            v = voice(ch, 62, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        if i == 4: c.HARP2.bar(b, f"{nm(t[-3])}:4")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.3 --master -15 --widen 1.0",
       "ケルト・フルート100曲の003。祖父の手紙を読む。D エオリアン・52。語りかけるような旋律、沈黙、決意。最後にほんの少し明るむ。",
       harm_scenes=["語り2", "決意"], tail_scene="終わり", tail_keep=8)
