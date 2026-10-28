# ケルト・フルート100曲「銀の笛と百の夜」019 夕べの笛吹き The Evening Piper — 第2版（2026-10-28）
# イメージ: 夕方、年老いた羊飼いが、エイラに笛を教える。先生が吹き、エイラがあとから同じ節をまねる。
#   はじめは1小節遅れて、たどたどしく（飾りなし）。回を重ねるごとに遅れが縮まり（2拍→1拍→半拍）、最後はぴったりそろう（山）。
#   そろったあと、エイラが3度下でハモって、二人の笛がひとつの和音になる。
# 形（台帳）: 2本の笛のずれた輪唱→最後にそろう。3/4・♩=58。E ドリア。始め：二声のずれ／終わり：二声がそろう。
# 編曲の表:
#   夕べ   : 竪琴のローヴィング・サム
#   教える1: 先生（左・装飾あり）→エイラ（右・3拍遅れ・飾りなし）。竪琴
#   教える2: 2拍遅れ。チェロが低く
#   教える3: 1拍遅れ。エイラにも少し装飾。弦がうすく
#   教える4: 半拍遅れ（ほとんど重なる）
#   そろう : 遅れなし（ぴったり）→後半はエイラが3度下でハモる（山）
#   夕暮れ : 二人の長い音、竪琴
import sys
from c100_common import *
from c100_v2 import *

S = Song("C100", "019-the-evening-piper", "夕べの笛吹き", "The Evening Piper", 58, 3, "E", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
MC = ["Em", "D", "Em", "A", "Em", "D", "Bm", "Em", "G", "D", "Em", "D", "A", "Em", "D", "Em"]
S.scene("夕べ", 2, "intro", ["Em", "Em"])
for k in range(1, 5): S.scene(f"教える{k}", 16, "verse", MC)
S.scene("そろう", 16, "chorus", MC)
S.scene("夕暮れ", 6, "outro", ["Em", "D", "Em", "Em", "Em", "Em"])
NAMES = ["夕べ", "教える1", "教える2", "教える3", "教える4", "そろう", "夕暮れ"]

c = make(S, NAMES,
         [("夕べ", 0, 0.6), ("教える1", 0, 0.62), ("教える2", 0, 0.64), ("教える3", 0, 0.68), ("教える4", 0, 0.72), ("そろう", 0, 0.8), ("そろう", 10, 0.9),
          ("そろう", 15, 0.78), ("夕暮れ", 0, 0.64), ("夕暮れ", 5, 0.4)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="夕べ", passing=True, tension=False)
c.FLUTE.spec["pan"] = -0.3
PUP = S.track("エイラの笛", "panflute", patch="flute", volume=0.36, bright=-0.45, pan=0.32, reverb=0.55, breath=True, noRestrike=True, mono=True,
              sustain=1.1, phrase=16, gainDb=3, barGain=[round(max(d, 0.8) * 1.1, 3) for d in c.DYN])
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.075, pan=0.0, reverb=0.45, barGain=c.g())

M = ["1:1 2:1 3:1", "5:2 4:1", "3:1 2:1 1:1", "2:3", "3:1 4:1 5:1", "6:1.5 5:0.5 4:1", "3:1 2:1 7,:1", "1:3",
     "5:1 6:1 7:1", "1':2 7:1", "6:1 5:1 4:1", "5:3", "6:1 5:1 4:1", "3:1.5 4:0.5 5:1", "4:1 3:1 2:1", "1:3"]
DELAY = {"教える1": 3, "教える2": 2, "教える3": 1, "教える4": 0.5, "そろう": 0}
DENS = {"教える1": 0.9, "教える2": 0.9, "教える3": 1.0, "教える4": 1.0, "そろう": 1.0}
PDENS = {"教える1": 0, "教える2": 0.2, "教える3": 0.5, "教える4": 0.7, "そろう": 0}
for k, (sc, d) in enumerate(DELAY.items()):
    play_melody(c, sc, M, 4, "air", density=DENS[sc], seed=1900 + k)
    ev = section_events(c, sc, M, 4)
    if sc != "そろう":
        notes = ornament(ev, S.key, S.bpm, "air", S.beats, density=PDENS[sc], seed=1950 + k)
        for t, L, m, mk in notes: PUP.at(round(t + d, 4), f"{nm(m)}:{round(L, 4)}{mk}")
    else:   # そろう：前半はぴったり同じ、後半は3度下でハモる
        for t, L, m in ev:
            bar = int(t // S.beats) - c.s0[sc]
            if bar >= 8:
                pcs = chord_pcs(S.chords[int(t // S.beats)]); h = [x for x in range(m - 5, m - 2) if x % 12 in pcs]
                m = h[-1] if h else m
            PUP.at(round(t + 0.03, 4), f"{nm(m)}:{L}")
play_melody(c, "夕暮れ", ["5:3", "4:3", "1:3", "1:3", "R:3", "R:3"], 4, "air", density=0)
for t, L, m in section_events(c, "夕暮れ", ["3:3", "2:3", "5,:3", "5,:3", "R:3", "R:3"], 4): PUP.at(round(t + 0.03, 3), f"{nm(m)}:{L}")

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    if n != "夕暮れ" or i < 4: roving_thumb(c.HARP, b, B, ch, up=(i % 2 == 0))
    if n in ("教える2", "教える3", "教える4", "そろう") or (n == "夕暮れ" and i < 5): CELLO.bar(b, f"{nm(r)}:3")
    if n in ("教える3", "教える4", "そろう", "夕暮れ") and not (n == "夕暮れ" and i == 5):
        v = voice(ch, 55, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:3")
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.34 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の019（第2版）。夕方、老いた羊飼いがエイラに笛を教える。3/4・♩=58、E ドリア。先生の笛（左）をエイラの笛（右）があとからまねる。遅れは3拍→2拍→1拍→半拍と縮まり、最後はぴったりそろって、エイラが3度下でハモる。",
       harm_scenes=None, tail_scene="夕暮れ", fill=False, pads=True, pad_scenes=["教える3", "教える4", "そろう"], double=False)
