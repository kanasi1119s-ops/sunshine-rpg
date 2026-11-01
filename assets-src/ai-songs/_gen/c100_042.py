# ケルト・フルート100曲「銀の笛と百の夜」042 風の刻んだ文字 Letters Carved by the Wind — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 立つ石のひとつに、古い文字が刻まれている。風と雨で削れて、ところどころ読めない。それは若い日の祖父が刻んだ歌だった。
#   エイラは読める所だけを笛で吹く。何度もなぞるうちに、欠けた所が少しずつ分かってきて、最後はひと続きの歌になる。
# 調べ: あいだ。形: 欠けた旋律が回るたびに埋まる（16小節の歌を4回 → 最後の8小節）。
# 拍子・速さ: 3/4・♩=56。旋法: G ドリア → 4回目から C イオニア（B♭ が B になり、歌が明るく読める）。
# 主役は笛（欠けた笛）。伴奏の主役: ナイロン弦ギターの断片（分散和音のかけら。回るたびにつながっていく）。
#   竪琴・ピアノ・弦・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 1回目は旋律がところどころ休符で（約4割だけ読める）、回るたびに埋まる（6割 → 8割半 → 全部）。
#   欠けた所の休符は、前の音をのばさない（文字が削れて読めない所）。ギターのかけらは、回るたびにつながる。
# 始まり: ギターの断片 → 終わり: 完成した旋律がひと続きに。
# 山: なし。
import sys, json, re, random
from c100_common import *
from c100_v2 import *
import c100_v2 as _v2
_oc = _v2.open_chord
_v2.open_chord = lambda ch, lo=52, hi=76: _oc(ch, lo, hi)

S = Song("C100", "042-letters-carved-by-the-wind", "風の刻んだ文字", "Letters Carved by the Wind", 56, 3, "G", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.2})
KG, KC = Key("G", "dorian", 4), Key("C", "major", 4)
CHG = ["Gm", "F", "Gm", "Dm", "Eb", "F", "Gm", "Gm", "Bb", "F", "C", "Gm", "Eb", "Dm", "C", "Gm"]
CHC = ["C", "F", "C", "G", "Am", "F", "G", "C", "F", "C", "G", "Am", "F", "C", "G", "C"]
SC = [("かけら", 4, "intro", ["Gm"] * 4), ("1回目", 16, "verse", CHG), ("2回目", 16, "verse", CHG), ("3回目", 16, "verse", CHG),
      ("4回目", 16, "chorus", CHC), ("ひと続き", 8, "outro", CHC[8:])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("かけら", 0, 0.66), ("1回目", 0, 0.68), ("2回目", 0, 0.7), ("3回目", 0, 0.72), ("4回目", 0, 0.76), ("ひと続き", 0, 0.76), ("ひと続き", 7, 0.7)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="かけら", passing=False, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 試し書き出し: ギターのかけら（0.05）は笛より約4dB 大きい → 0.032
GT = [S.track(f"ギターのかけら{j + 1}", "guitar", patch="nylonGuitar", volume=0.032, pan=-0.25 + 0.5 * j, reverb=0.4, barGain=[round(x * 1.3, 3) for x in G]) for j in range(2)]

# ---------- 祖父の歌（16小節。1=G4 のドリア／1=C の長調で同じ度数の形） ----------
SONG = ["5:2 4:1", "3:1 2:1 1:1", "2:2 3:1", "5:3", "6:1 5:1 4:1", "3:2 2:1", "1:1 2:1 3:1", "2:3",
        "5:1 6:1 7:1", "1':2 7:1", "6:1 5:1 4:1", "5:3", "3:1 4:1 5:1", "4:2 2:1", "3:1 2:1 7,:1", "1:3"]
KEEP = {"1回目": 0.4, "2回目": 0.6, "3回目": 0.85, "4回目": 1.0}
rng = random.Random(4242)
MASK = [rng.random() for _ in range(64)]              # どの音が「読める」か（回によって割合だけ増える＝前に読めた音はずっと読める）
GAPS = {}
for n in ("1回目", "2回目", "3回目", "4回目"):
    key = KC if n == "4回目" else KG
    ev = section_events(c, n, SONG, 4, key=key)
    kept = []; gaps = []
    for q, (t, L, m) in enumerate(ev):
        if MASK[q % 64] < KEEP[n]: kept.append([t, L, m])
        else: gaps.append((t, L, m))
    play(c.FLUTE, ornament(kept, key, 56, "air", B, density=0.15, seed=4200 + len(kept)))
    GAPS[n] = gaps
play_melody(c, "ひと続き", SONG[8:], 4, "air", key=KC, density=0.2, seed=4210)

# ---------- ギターのかけら：欠けた所に、分散和音のかけら（その音を含む）が入る。回るたびにつながる ----------
def tones(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return sorted(48 + (p - 48) % 12 for p in (r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12))
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    v = tones(ch) + [tones(ch)[0] + 12]
    if n == "かけら":                                       # 断片：1小節に2〜3音、間をあけて
        GT[b % 2].bar(b, [f"{nm(v[0])}:1 R:1 {nm(v[2])}:1,", f"R:1 {nm(v[1])}:1, {nm(v[3])}:1,"][i % 2])
        continue
    cont = {"1回目": 0.35, "2回目": 0.6, "3回目": 0.85, "4回目": 1.0, "ひと続き": 1.0}[n]
    pat = []
    for q in range(6):                                    # 8分6つのうち、つながりの割合だけ鳴らす
        pat.append(f"{nm(v[(0, 2, 1, 3, 2, 1)[q]])}:0.5{',' if q % 2 else ''}" if (q * 0.17 + i * 0.07) % 1 < cont else "R:0.5")
    GT[b % 2].bar(b, " ".join(pat))
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.3 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の042（第3版）。立つ石に、若い日の祖父が刻んだ歌が、風と雨で削れて残っている。3/4・♩=56。笛は読める所だけを吹き（1回目は約4割）、回るたびに欠けた所が埋まっていく（6割 → 8割半 → 全部）。4回目で G ドリアが C の長調になって歌が明るく読め、最後はひと続きの歌になる。伴奏はナイロン弦ギターの断片で、回るたびにつながっていく。",
       harm_scenes=None, tail_scene="ひと続き", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3800, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -27, "delay": 0.28, "lp": 2800, "rt": 3.4}}}
json.dump(air, open("/tmp/cel/w/air042.json", "w"), ensure_ascii=False)
