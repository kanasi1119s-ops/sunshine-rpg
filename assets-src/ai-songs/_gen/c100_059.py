# ケルト・フルート100曲「銀の笛と百の夜」059 睡蓮 Water Lilies — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 霧が晴れかけた湖の入り江に、睡蓮が一面に咲いている。花は水に映って、上と下に二つずつ咲いて見える。
#   舟はゆっくり揺れ、エイラは揺れに合わせて笛を吹く。水に映る花のように、ピアノが笛の旋律を上下さかさまにして、同時に弾く。
# 調べ: 眠り。形: 鏡の旋律（笛の旋律を、ピアノが B♭ を軸に上下さかさまにして、1オクターブ上で同時に弾く）。
# 拍子・速さ: 12/8・付点4分＝50（1拍＝付点4分、1小節＝4拍。8分は 1/3 拍）。旋法: E♭ イオニア。
# 主役は笛（揺れる笛。付点のゆれ）。伴奏の主役: ピアノの高い音（鏡の旋律）。脇: 竪琴の低い分散和音。
#   ギター・パッド・弦・打楽器・2本目の笛は使わない。
# この曲だけ: ピアノが笛の旋律を上下さかさまにして同時に弾く（笛が上がるとピアノは下がる。リズムは同じ）。
# 始まり: 竪琴の低い音 → 終わり: 和音のロール（竪琴が低い所から高い所まで、ゆっくり和音を広げる）。
# 山: 終盤に1つ（花ひらく）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "059-water-lilies", "睡蓮", "Water Lilies", 50, 4, "Eb", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3, "rubato": 0.15})
K = Key("Eb", "major", 4)
T3 = 1 / 3
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()) for s_ in bars]
CA = ["Eb", "Bb", "Eb", "Ab", "Cm", "Ab", "Bb", "Eb"]
CB = ["Eb", "Cm", "Bb", "Bb", "Ab", "Eb", "Bb", "Eb"]
SC = [("竪琴の低い音", 2, "intro", ["Eb", "Eb"]), ("水面1", 16, "verse", CA + CB), ("水面2", 16, "verse", CA + CB), ("花ひらく", 16, "chorus", CB + CA),
      ("和音のロール", 3, "outro", ["Eb"] * 3)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("竪琴の低い音", 0, 0.66), ("水面1", 0, 0.66), ("水面2", 0, 0.7), ("花ひらく", 0, 0.78), ("花ひらく", 12, 0.86), ("和音のロール", 0, 0.72), ("和音のロール", 2, 0.66)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="竪琴の低い音", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# ピアノ1音は ×1.4 で笛とほぼ同じ（016）→ 鏡は少し小さく 0.13。竪琴の低い音だけの始まりは別のパートで大きく
PM = S.track("ピアノ（鏡の旋律）", "piano", volume=0.13, pan=0.25, reverb=0.6, sustain=1.3, barGain=G)
HP = [S.track(f"竪琴（低い分散和音{j + 1}）", "harp", patch="folkHarp", volume=0.075, pan=-0.3 + 0.12 * j, reverb=0.6, sustain=1.6, barGain=G) for j in range(2)]
HPI = S.track("竪琴（始まりの低い音）", "harp", patch="folkHarp", volume=0.2, pan=-0.25, reverb=0.6, sustain=2.0)

# ---------- 笛の旋律（8分＝1、1小節＝12。1=E♭4） ----------
A = ["5:2 6:1 5:2 3:1 4:2 5:1 3:3", "2:2 3:1 4:2 2:1 1:6", "3:2 4:1 5:2 6:1 7:2 6:1 5:3", "6:6 5:6",
     "5:2 6:1 1':2 6:1 5:2 4:1 3:3", "4:2 5:1 6:2 4:1 3:6", "2:2 3:1 4:2 5:1 3:2 2:1 7,:3", "1:12"]
Bm = ["1':3 7:2 6:1 5:6", "6:2 7:1 1':2 2':1 1':6", "7:3 6:2 5:1 4:6", "5:2 6:1 7:2 5:1 6:6",
      "1':3 2':2 1':1 7:3 6:3", "5:2 4:1 3:2 4:1 5:6", "4:2 3:1 2:2 3:1 7,:3 2:3", "1:12"]
SCL = sorted({(3 + x) % 12 for x in (0, 2, 4, 5, 7, 9, 11)})          # E♭ の長調
LADDER = [m for m in range(36, 100) if m % 12 in SCL]
AXIS = LADDER.index(70)                                               # B♭4 が鏡の軸
def mirror(m):
    i = LADDER.index(m) if m in LADDER else min(range(len(LADDER)), key=lambda j: abs(LADDER[j] - m))
    return LADDER[2 * AXIS - i + 7]                                   # さかさまにして、1オクターブ上
for k, (sc, bars) in enumerate((("水面1", A + Bm), ("水面2", A + Bm), ("花ひらく", Bm + A))):
    s0 = c.s0[sc]; ev = []
    for j, s_ in enumerate(e2b(bars)): ev += mel_events(K, s_, 4, (s0 + j) * B)
    ev = [[round(t, 4), L, m] for t, L, m in ev]
    play(c.FLUTE, ornament(ev, K, 50, "air", B, density=(0.12, 0.18, 0.25)[k], seed=5900 + k))
    play(PM, [(t, L, mirror(m), "" if L >= 1 else ",") for t, L, m in ev])          # 鏡の旋律：同じリズム、さかさまの高さ
s0 = c.s0["和音のロール"]
c.FLUTE.at(s0 * B, "G5:8"); PM.at(s0 * B, "Bb5:8,")

# ---------- 竪琴の低い分散和音（1拍に8分3つ：根音・5度・10度。花ひらくでは上へ6音） ----------
ROOT = {"Eb": 39, "Bb": 46, "Ab": 44, "Cm": 48}
HPI.at(0, "Eb2:2"); HPI.at(1.0, "Bb2:2,"); HPI.at(2.0, "Eb3:2,"); HPI.at(3.0, "G3:3,"); HPI.at(4.0, "Eb2:2"); HPI.at(5.0, "Bb2:2,"); HPI.at(6.0, "G3:2,")
for b in range(c.s0["水面1"], c.s0["和音のロール"]):
    n = S.scene_of(b)[0]; ch = S.chords[b]; r = ROOT[ch]; th = r + (3 if ch.endswith("m") else 4)
    for q in range(4):
        t0 = b * B + q
        if n == "花ひらく" and q % 2 == 1:
            notes = (r + 12, r + 19, th + 24)
        else:
            notes = (r, r + 7, th + 12)
        for k2, m in enumerate(notes):
            HP[k2 % 2].at(round(t0 + k2 * T3, 4), f"{nm(m)}:{round(T3 * 2, 4)}{'' if (q == 0 and k2 == 0) else ','}")
# 和音のロール：低い E♭ から高い G まで、ゆっくり広げる
for k2, m in enumerate((39, 46, 51, 55, 58, 63, 67, 70, 75, 79)):
    HP[k2 % 2].at(round(s0 * B + k2 * 0.4, 3), f"{nm(m)}:{round(10 - k2 * 0.4, 2)}{'' if k2 == 0 else ','}")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.34 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の059（第3版）。霧が晴れかけた入り江に、睡蓮が一面に咲き、水に映っている。12/8・付点4分＝50、E♭ の長調。舟の揺れに合わせて笛が付点のゆれで歌い、ピアノがその旋律を B♭ を軸に上下さかさまにして、1オクターブ上で同時に弾く（水に映る花）。下では竪琴の低い分散和音。終盤の花ひらく所が山で、最後は竪琴が低い所から高い所まで和音をゆっくり広げる。",
       harm_scenes=None, tail_scene="和音のロール", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3800, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 2800, "rt": 3.8}}}
json.dump(air, open("/tmp/cel/w/air059.json", "w"), ensure_ascii=False)

_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
