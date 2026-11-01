# ケルト・フルート100曲「銀の笛と百の夜」048 鐘の秘密 The Secret of the Bell — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 塔の鐘の下に、祖父が見つけた秘密の扉がある。扉は「問い」には開かず、「答え」にだけ開く。
#   エイラの笛は、はじめ問うばかり（上がって、途中で止まる）。鐘を鳴らすと、鐘の響きの中に隠れた短3度の音が聞こえ、
#   弦がそれを1つずつ引き継いで和音にしていく。その和音に導かれて、笛の句は答え（下りて閉じる）に変わり、最後に扉が開く。
# 調べ: あいだ。形: 問い（上がって止まる）が、答え（下りて閉じる）に変わる。
# 拍子・速さ: 6/8・付点4分＝50（1拍＝付点4分、1小節＝2拍。8分は 1/3 拍）。旋法: D ドリア → 扉で D の長調（F が F♯ に）。
# 主役は笛（問う笛 → 答える笛）。伴奏の主役: ホルン（低い持続）。脇: 低い弦（チェロ・ビオラ。鐘の倍音を引き継ぐ）と竪琴、鐘。
#   ギター・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 鐘の倍音（打った音の短3度上）を弦が引き継いで和音にする（D の鐘 → F、F の上に A、…と積み重なる）。
# 始まり: 竪琴の問い（上がって止まる4音）→ 終わり: 扉が開く長調の和音（D・F♯・A）。
# 山: 終盤に1つ（扉）。
import sys, json, re
from c100_common import *
from c100_v2 import *

BPM = 50
S = Song("C100", "048-the-secret-of-the-bell", "鐘の秘密", "The Secret of the Bell", BPM, 2, "D", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35, "rubato": 0.2})
KD, KM = Key("D", "dorian", 4), Key("D", "major", 4)
T3 = 1 / 3
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()) for s_ in bars]
CQ = ["Dm", "Dm", "G", "C"] * 8
CA = ["F", "C", "Dm", "Dm", "Bb", "C", "Am", "Dm"] * 4
SC = [("竪琴の問い", 4, "intro", ["Dm"] * 4), ("問い", 32, "verse", CQ), ("鐘", 16, "verse", ["Dm"] * 16), ("答え", 32, "verse", CA),
      ("扉", 24, "chorus", (["D", "G", "A", "D", "Bm", "G", "A", "D"] * 3)), ("開いた扉", 4, "outro", ["D"] * 4)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("竪琴の問い", 0, 0.68), ("問い", 0, 0.7), ("鐘", 0, 0.72), ("答え", 0, 0.74), ("扉", 0, 0.82), ("扉", 20, 0.92), ("開いた扉", 0, 0.84), ("開いた扉", 3, 0.76)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="竪琴の問い", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
HN = S.track("ホルン（低い持続）", "brass", patch="horn", volume=0.12, gainDb=6, pan=-0.2, reverb=0.7, barGain=G)       # 037 で測った値より少し小さく
HP = S.track("竪琴", "harp", patch="folkHarp", volume=0.07, pan=0.3, reverb=0.6, sustain=2.0, barGain=[round(x * (1.8 if b < 4 else 1.0), 3) for b, x in enumerate(G)])
BELL = S.track("鐘", "bell", volume=0.12, pan=0.15, reverb=0.9, barGain=[1.2] * c.NB)
OV = [S.track(f"弦（鐘の倍音{j + 1}）", "strings", patch=("viola" if j % 2 else "cello"), volume=(0.017 if j % 2 else 0.02), gainDb=(0 if j % 2 else 2),
              pan=-0.3 + 0.2 * j, reverb=0.7, release=0.6, barGain=[round(x * 1.4, 3) for x in G]) for j in range(4)]

# ---------- 問いと答え（8分＝1、1小節＝6） ----------
Q = [["1:3 2:3", "4:3 5:3", "6:2 5:1 6:3", "7:6"], ["3:3 4:3", "5:2 6:1 7:3", "1':3 2':3", "3':6"],
     ["5,:3 7,:3", "1:2 2:1 3:3", "4:3 6:3", "5:6"], ["2:3 3:3", "4:2 5:1 6:3", "7:3 1':3", "2':6"]]
A = [["5:3 4:3", "3:2 2:1 1:3", "7,:3 2:3", "1:6"], ["1':3 7:3", "6:2 5:1 4:3", "3:3 2:3", "1:6"],
     ["3':3 2':3", "1':2 7:1 6:3", "5:3 2:3", "1:6"], ["6:3 5:3", "4:2 3:1 2:3", "3:2 2:1 7,:3", "1:6"]]
def phrase(bars, key, b0, dens, seed):
    ev = []
    for j, s_ in enumerate(e2b(bars)): ev += mel_events(key, s_, 4, (b0 + j) * B)
    play(c.FLUTE, ornament([[round(t, 4), L, m] for t, L, m in ev], key, BPM, "air", B, density=dens, seed=seed))
# 竪琴の問い：上がって止まる4音
HP.bar(0, "D4:0.6667 E4:0.6667 G4:0.6667"); HP.bar(1, "A4:2"); HP.bar(2, "D4:0.6667 E4:0.6667 G4:0.6667"); HP.bar(3, "A4:1.3333 R:0.6667")
s0 = c.s0["問い"]
for q in range(8): phrase(Q[q % 4], KD, s0 + 4 * q, 0.25, 4800 + q)
s0 = c.s0["鐘"]                                                    # 鐘：笛は長い音で聞く
phrase(["1:6", "1:6", "3:6", "3:6", "5:6", "5:6", "7:6", "7:6", "1':6", "7:6", "5:6", "3:6", "2:6", "1:6", "1:6", "1:6"], KD, s0, 0.1, 4810)
s0 = c.s0["答え"]
for q in range(8): phrase(A[q % 4], KD, s0 + 4 * q, 0.25, 4820 + q)
s0 = c.s0["扉"]
for q in range(6): phrase(A[(q + 1) % 4], KM, s0 + 4 * q, 0.35, 4830 + q)
phrase(["1:6", "3:6", "5:6", "1:6"], KM, c.s0["開いた扉"], 0.0, 4840)

# ---------- 鐘と、倍音を引き継ぐ弦 ----------
# 鐘を4小節ごとに打つ。打った音の短3度上を弦が引き継ぎ、次の鐘はその音を打つ（D → F → A♭ではなく、旋法の中で D → F → A → C）
STACK = [50, 53, 57, 60]                        # D3 F3 A3 C4（チェロ・ビオラが1つずつ積む）
s0 = c.s0["鐘"]
for k in range(4):
    BELL.at((s0 + 4 * k) * B, f"{nm(STACK[k] + 12)}:6")
    OV[k].at(round((s0 + 4 * k) * B + 0.5, 3), f"{nm((53, 57, 60, 64)[k])}:{(16 - 4 * k) * B - 0.5},")      # 鐘の音の3度上（旋法の中で）を引き継ぐ
# 問いの句の終わりにも、遠い鐘を1つ（4句に1回）
for q in range(0, 8, 2): BELL.at((c.s0["問い"] + 4 * q + 3) * B, "D5:4")
# 扉：弦が長調の和音に（D・F♯・A・D）
s0 = c.s0["扉"]
for k, m in enumerate((50, 54, 57, 62)):
    OV[k].at(round(s0 * B + 0.05 * k, 3), f"{nm(m)}:{(c.NB - s0) * B - 0.2}")
BELL.at(s0 * B, "D5:6")

# ---------- ホルン（低い持続）と竪琴 ----------
ROOT = {"Dm": 38, "G": 43, "C": 48, "F": 41, "Bb": 46, "Am": 45, "D": 38, "A": 45, "Bm": 47}
for b in range(4, c.NB, 2):
    n = S.scene_of(b)[0]; ch = S.chords[b]; r = ROOT[ch]
    if n == "鐘": continue
    HN.at(b * B, f"{nm(r + 12 if r + 12 <= 55 else r)}:4,")
    if n in ("答え", "扉"):
        th = r + (3 if ch.endswith("m") else 4)
        HP.bar(b, " ".join(f"{nm(x)}:{round(T3, 4)}," for x in (r + 12, r + 19, th + 24, r + 24, th + 24, r + 19)))

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.34 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の048（第3版）。塔の鐘の下の、祖父が見つけた秘密の扉。6/8・付点4分＝50、D ドリア。笛ははじめ問うばかり（上がって止まる）。鐘を4回鳴らすと、その響きの短3度上の音を弦が1つずつ引き継ぎ、D・F・A・C と和音が積み重なる。導かれて笛の句は答え（下りて閉じる）に変わり、最後は D の長調の和音で扉が開く。伴奏はホルンの低い持続と竪琴。",
       harm_scenes=None, tail_scene="開いた扉", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 160, "lp": 3600, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 2800, "rt": 4.0}}}
json.dump(air, open("/tmp/cel/w/air048.json", "w"), ensure_ascii=False)

_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
