# ケルト・フルート100曲「銀の笛と百の夜」079 嵐の去った後 After the Storm — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 夜明け前、嵐が去る。灯台の小さな礼拝室に、岬の漁師たちが集まり、無事を感謝して古い詩篇を歌う。
#   先唱者（エイラの笛）が1行を歌うと、みんなが同じ行を、少しずつずれながら、ゆっくり重ねて歌う。
#   行を重ねるごとに、ずれは少しずつ小さくなり、最後は全員の声がそろう。
# 調べ: あいだ。形: 詩篇唱のずれた重なり（先唱の1行 → 全員が同じ行を少しずつずれて。4行の歌を3節）。和音は使わない。
# 拍子・速さ: 4/4・♩=40（とても遅い。1行＝2小節）。旋法: E ドリア。
# 主役は笛（先唱の笛）。伴奏: 2本目・3本目の笛、フィドル、チェロ（低い声のハミングのかわりに、1オクターブ下）。全員が同じ旋律だけを歌う。
#   竪琴・ギター・ピアノ・パッド・打楽器は使わない。
# この曲だけ: 和音を使わず、同じ旋律のずれた重なりだけで厚くする（ずれは節ごとに小さくなり、最後にそろう）。
# 始まり: 笛ひとりの1行 → 終わり: 全員がそろう。
# 山: 波（行ごとにふくらんで、しぼむ）。
import sys, json, re, random
from c100_common import *
from c100_v2 import *

S = Song("C100", "079-after-the-storm", "嵐の去った後", "After the Storm", 40, 4, "E", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3, "rubato": 0.15})
K = Key("E", "dorian", 4)
L = ["1:2 3:2 5:2 4:1 3:1", "5:2 6:2 5:2 3:2", "4:2 3:1 2:1 1:2 7,:2", "2:2 3:2 2:2 1:2"]            # 4行（1行＝8拍＝2小節）
# 節の並び：(先唱か全員か, 行の番号)
V1 = [("全", 0), ("先", 1), ("全", 1), ("先", 2), ("全", 2), ("先", 3), ("全", 3)]
V2 = [("先", 0), ("全", 0), ("先", 1), ("全", 1), ("先", 2), ("全", 2), ("先", 3), ("全", 3)]
V3 = [("全", 0), ("全", 1), ("全", 2), ("全", 3)]
SC = [("先唱", 2, "intro", ["Em"] * 2), ("1節", 14, "verse", ["Em"] * 14), ("2節", 16, "chorus", ["Em"] * 16), ("3節", 8, "verse", ["Em"] * 8),
      ("そろう", 2, "outro", ["Em"] * 2)]
for n, Ln, kd, ch in SC: S.scene(n, Ln, kd, ch)
NAMES = [x[0] for x in SC]
# 波：全員の行でふくらみ、先唱の行でしぼむ
ARC = [("先唱", 0, 0.7)]
for sc, plan in (("1節", V1), ("2節", V2), ("3節", V3)):
    for q, (who, li) in enumerate(plan):
        ARC.append((sc, 2 * q, 0.72 if who == "先" else (0.8 if sc == "1節" else 0.88 if sc == "2節" else 0.84)))
ARC += [("そろう", 0, 0.86), ("そろう", 1, 0.74)]
c = make(S, NAMES, ARC, {}, flute_gain={n: 1.15 for n in NAMES}, intro="先唱", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
F2 = S.track("2本目の笛", "panflute", patch="flute", volume=0.06, bright=-0.5, pan=0.35, reverb=0.7, breath=False, barGain=G)
F3 = S.track("3本目の笛", "panflute", patch="flute", volume=0.05, bright=-0.7, pan=-0.4, reverb=0.75, breath=False, barGain=G)
FD = S.track("フィドル", "strings", patch="violin", volume=0.028, gainDb=3, pan=0.15, reverb=0.7, release=0.5, barGain=G)
VC = S.track("チェロ（低い声のかわり）", "strings", patch="cello", volume=0.025, gainDb=4, pan=-0.2, reverb=0.7, release=0.5, barGain=[round(x * 1.3, 3) for x in G])

rng = random.Random(7901)
def line(li, b0, lag):
    """1行を、全員で少しずつずれて（lag＝ずれの大きさ。0 でそろう）"""
    ev = mel_events(K, L[li], 4, b0 * B)
    ev = [[round(t, 4), Ln, m] for t, Ln, m in ev]
    play(c.FLUTE, ornament(ev, K, 40, "air", B, density=0.15, seed=7900 + b0))
    for tr, d, sh, mk in ((F2, 0.35, 0, ","), (F3, 0.6, 0, ","), (FD, 0.2, 0, ""), (VC, 0.45, -12, "")):
        delay = round(lag * d * rng.uniform(0.6, 1.2), 3)
        evs = []
        for t, Ln, m in ev:
            dt = round(delay + lag * rng.uniform(-0.05, 0.12), 3)            # 音ごとにも少しずつずれる
            evs.append((round(t + max(0, dt), 4), round(max(0.3, Ln - max(0, dt) + min(delay, 0.4) * 0.5), 4), m + sh, mk))
        play(tr, evs)
ev = mel_events(K, L[0], 4, 0)
play(c.FLUTE, ornament([[round(t, 4), Ln, m] for t, Ln, m in ev], K, 40, "air", B, density=0.2, seed=7899))
for sc, plan, lag0, lag1 in (("1節", V1, 1.0, 0.8), ("2節", V2, 0.75, 0.5), ("3節", V3, 0.4, 0.0)):
    s0 = c.s0[sc]
    alls = [q for q, (w, _) in enumerate(plan) if w == "全"]
    for q, (who, li) in enumerate(plan):
        b0 = s0 + 2 * q
        if who == "先":
            ev = mel_events(K, L[li], 4, b0 * B)
            play(c.FLUTE, ornament([[round(t, 4), Ln, m] for t, Ln, m in ev], K, 40, "air", B, density=0.2, seed=7910 + b0))
        else:
            k = alls.index(q); lag = lag0 + (lag1 - lag0) * (k / max(1, len(alls) - 1))
            line(li, b0, lag)
s0 = c.s0["そろう"]
for tr, m in ((c.FLUTE, "E4:7"), (F2, "E4:7,"), (F3, "E4:7,"), (FD, "E4:7"), (VC, "E3:7")):
    tr.at(s0 * B, m)

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.36 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の079（第3版）。夜明け前、嵐が去り、灯台の小さな礼拝室で漁師たちが古い詩篇を歌う。4/4・♩=40（とても遅い）、E ドリア。先唱の笛が1行を歌うと、2本目・3本目の笛、フィドル、チェロ（1オクターブ下）が同じ行を少しずつずれながら重ねる。和音は使わず、同じ旋律のずれた重なりだけで厚くする。4行の歌を3節、行ごとに波のようにふくらみ、ずれは節ごとに小さくなって、最後に全員がそろう。",
       harm_scenes=None, tail_scene="そろう", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 6.0, "layers": [{"file": "0595", "db": -45, "hp": 160, "lp": 3400, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -26, "delay": 0.34, "lp": 2600, "rt": 4.6}}}
json.dump(air, open("/tmp/cel/w/air079.json", "w"), ensure_ascii=False)
