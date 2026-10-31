# ケルト・フルート100曲「銀の笛と百の夜」020 星の草原 The Starlit Meadow — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 第2章の終わり。夕べの笛吹きと別れた夜、エイラは草原に寝ころんで星を見上げる。遠くで虫が2つの音で鳴いている。
#   笛で子守歌を吹いているうちにまぶたが重くなり、吹くたびに節から音が1つずつこぼれ落ちて、
#   最後は虫と同じ2つの音（シ♭とファ）だけになり、笛も止まって、虫の2音だけが残る。
# 調べ: 眠り。形: 同じ12小節の節を6周。1周ごとに、旋律から音（音階の音）が1つずつ消える（7→6→4→2→3 の順）。
# 拍子・速さ: 3/4・♩=56。旋法: B♭ ミクソリディア。
# 主役は笛（低く・細く。F4〜F5）。伴奏の主役: 竪琴（folkHarp）の2音の揺れ（遠い虫。F5 と B♭4）。
#   脇: 1〜3周目だけ竪琴の低い根音、2周目だけ竪琴の流れる分散和音（山）。ギター・ピアノ・弦・パッド・打楽器は使わない。
# この曲だけ: 1周ごとに旋律の音が1つずつ減り、最後は笛も虫と同じ2音（1と5）だけになり、竪琴の2音だけが残る。
#   消えた音は休みにせず、前の音をのばす（眠りに落ちるように、節が長い音になっていく）。
# 始まり: 竪琴の2音 → 終わり: 竪琴の2音だけ。
# 山: 前半に1つ（2周目）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "020-the-starlit-meadow", "星の草原", "The Starlit Meadow", 56, 3, "Bb", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35, "rubato": 0.2})
K = Key("Bb", "mixolydian", 4)
CH = ["Bb", "Bb", "Eb", "F", "Bb", "Eb", "Bb", "F", "Ab", "Bb", "Ab", "Bb"]
SC = [("虫", 4, "intro", ["Bb"] * 4)] + [(f"{r}周目", 12, "chorus" if r == 2 else "verse", CH) for r in range(1, 7)] + [("2つの音", 4, "outro", ["Bb"] * 4)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("虫", 0, 0.62), ("1周目", 0, 0.68), ("2周目", 0, 0.76), ("2周目", 8, 0.82), ("3周目", 0, 0.74), ("4周目", 0, 0.7),
          ("5周目", 0, 0.68), ("6周目", 0, 0.66), ("2つの音", 0, 0.64), ("2つの音", 3, 0.6)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="虫", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 試し書き出し: 虫の2音は笛より約8dB小さい（遠い虫として丁度よい。ただし竪琴だけの始まりと終わりは ×2）。低い根音は笛と同じくらい → 0.1→0.06
BUG = [S.track(f"竪琴（虫の2音・{x}）", "harp", patch="folkHarp", volume=0.07, pan=p, reverb=0.7, sustain=2.0,
                 barGain=[round(x * (2.0 if b < 4 or b >= c.NB - 4 else 1.0), 3) for b, x in enumerate(G)])
       for x, p in (("ファ", 0.4), ("シ♭", 0.25))]
LOW = S.track("竪琴（低い根音）", "harp", patch="folkHarp", volume=0.06, pan=-0.15, reverb=0.55, sustain=2.4, barGain=G)
ARP = S.track("竪琴（流れる分散和音）", "harp", patch="folkHarp", volume=0.06, pan=-0.3, reverb=0.6, sustain=1.6, barGain=G)

# ---------- 節（B♭ ミクソリディア。1=B♭4。12小節） ----------
TUNE = ["5,:2 1:1", "2:1 3:1 5:1", "4:2 3:1", "2:3", "1:1 2:1 3:1", "5:2 6:1", "5:1 4:1 3:1", "2:2 1:1",
        "7,:2 1:1", "3:1 2:1 1:1", "6,:2 7,:1", "1:3"]
DEG_PC = {1: 10, 2: 0, 3: 2, 4: 3, 5: 5, 6: 7, 7: 8}
GONE_ORDER = [7, 6, 4, 2, 3]                       # 2周目から1つずつ消える。6周目は 1 と 5 だけ
def gone(r): return {DEG_PC[d] for d in GONE_ORDER[:max(0, r - 1)]}
for r in range(1, 7):
    sc = f"{r}周目"
    ev = section_events(c, sc, TUNE, 4, key=K)
    kept = []
    for t, L, m in ev:
        if m % 12 in gone(r) and kept:              # 消えた音は、前の音をのばしてつなぐ
            kept[-1][1] = round(t + L - kept[-1][0], 4)
        elif m % 12 in gone(r):
            continue
        else:
            kept.append([t, L, m])
    play(c.FLUTE, ornament(kept, K, 56, "air", B, density=max(0.0, 0.3 - 0.06 * r), seed=2000 + r))

# ---------- 竪琴 ----------
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    # 遠い虫の2音（F5 と B♭4）。少しずつ揺れ方を変える（機械のようにしない）
    pat = [("F5:1, R:2", "R:1 Bb4:1, R:1"), ("F5:1.5, R:1.5", "R:1.5 Bb4:1.5,"), ("F5:1, R:1 F5:1,", "R:1 Bb4:1, R:1"),
           ("R:1 F5:1, R:1", "Bb4:1, R:1 Bb4:1,")][(b * 7) % 4]
    BUG[0].bar(b, pat[0])
    BUG[1].bar(b, pat[1])
    r = int(n[0]) if n[0].isdigit() else 0
    root = {"Bb": 46, "Eb": 39, "F": 41, "Ab": 44}[ch]
    if 1 <= r <= 3: LOW.bar(b, f"{nm(root)}:3,")
    if r == 2:
        v = [root + 12, root + 19, root + 24, root + 28 - (1 if ch in ("Bb",) else 0)]
        ARP.bar(b, " ".join(f"{nm(v[q])}:1{',' if q else ''}" for q in (0, 1, 2)))

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.34 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の020（第3版）。第2章の終わり、草原に寝ころんで星を見上げる夜。3/4・♩=56、B♭ ミクソリディア。遠くの虫のような竪琴の2音（ファとシ♭）の上で、笛が同じ12小節の節を6回吹く。1周ごとに旋律から音が1つずつこぼれ落ち（消えた音は前の音をのばしてつなぐ）、最後は笛も虫と同じ2音だけになって止まり、竪琴の2音だけが残る。",
       harm_scenes=None, tail_scene="2つの音", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 6.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3600, "wide": 0.012, "duck": 0.4, "fade": 8}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 2800, "rt": 3.8}}}
json.dump(air, open("/tmp/cel/w/air020.json", "w"), ensure_ascii=False)
