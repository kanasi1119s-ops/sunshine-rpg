# ケルト・フルート100曲「銀の笛と百の夜」005 小舟の鈴 The Little Boat Bell — 第3版（2026-10-29 作り直し。docs/sound/celtic-study/E-100-plan.md）
# 物語: 旅立ちの前の夜。港の小舟の中で、エイラは毛布にくるまって眠ろうとする。舳先の小さな鈴が、波に合わせて鳴る。
#   エイラは母がうたってくれた子守歌を、笛で小さく吹く。舟は少しずつ岸から離れ、波は小さくなっていき、歌は途中で眠りに消える。
# 調べ: 眠り。形: 子守歌（ゆりかごの揺れ・同じ節のくり返し）。6/8・付点4分＝50（8分＝150）。B♭ イオニアの5音（B♭・C・D・F・G）。
# 主役は笛: 柔らかい中音域、狭い音域（F4〜D5 の6度ほど）。装飾はほとんどなし。
# 伴奏: ナイロン弦の竪琴の揺れ（低い音→上の2音の「ゆりかご」）と、小さな鈴（本物の録音を和音の音に合わせる）だけ。
#   弦・チェロ・パッド・ギター・ピアノ・打楽器・2本目の笛は使わない。
# この曲だけ: 鈴の鳴る位置が、波（8小節）ごとに8分音符1つずつ後ろへずれていく（舟が少しずつ流されていく）。
# 始まり: 鈴の1音だけ → 終わり: 子守歌が句の途中で消え、竪琴の揺れと最後の鈴が残る。
# 山: 波（8小節ごとに小さくふくらむ）。6つめの波が少しだけ大きく、そこから眠りへ向かって小さく。最初が大きい形にはしない。
import sys, json, math
from c100_common import *
from c100_v2 import *

BPM = 150   # 8分音符＝150（付点4分＝50）
S = Song("C100", "005-little-boat-bell", "小舟の鈴", "The Little Boat Bell", BPM, 6, "Bb", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35})
CA = ["Bb", "Eb", "Bb", "Gm", "Bb", "Gm", "Eb", "Bb"]
CB = ["Gm", "Eb", "Bb", "F", "Eb", "Bb", "Eb", "F"]
WAVES = ["A", "A2", "B", "A", "休", "B", "A", "A2", "B", "A", "A", "消"]   # 波ごとの節（休＝笛は長い音だけ。消＝途中で消える）
S.scene("鈴", 2, "intro", ["Bb", "Bb"])
for k, w in enumerate(WAVES):
    S.scene(f"波{k + 1}", 8, "chorus" if k == 5 else "verse", CB if w == "B" else CA)
S.scene("眠り", 3, "outro", ["Bb", "Bb", "Bb"])
NAMES = ["鈴"] + [f"波{k + 1}" for k in range(len(WAVES))] + ["眠り"]
S.fix_avoid = lambda t: 0      # 5音の子守歌のまま（B♭ を A に直されないように）。和音のほうを旋律に合わせて選んだ
WV = [0.66, 0.68, 0.7, 0.7, 0.66, 0.76, 0.72, 0.7, 0.68, 0.64, 0.6, 0.56]   # 波ごとの大きさ（6つめが少しだけ大きい）
pts = [("鈴", 0, 0.64)]
for k, v in enumerate(WAVES):
    pts += [(f"波{k + 1}", 0, WV[k] - 0.03), (f"波{k + 1}", 4, WV[k] + 0.02), (f"波{k + 1}", 7, WV[k] - 0.02)]
pts += [("眠り", 0, 0.52), ("眠り", 2, 0.46)]
c = make(S, NAMES, pts, {}, flute_gain={n: 1.1 for n in NAMES}, intro="鈴", passing=True, tension=False)
B = S.beats
HL = S.track("竪琴（揺れの低い音）", "harp", patch="folkHarp", volume=0.12, pan=-0.15, reverb=0.5, sustain=2.2, barGain=c.g())
HU = [S.track(f"竪琴（揺れの上{j + 1}）", "harp", patch="folkHarp", volume=0.075, pan=0.1 + 0.12 * j, reverb=0.5, sustain=1.6, barGain=c.g()) for j in range(2)]
HA = S.track("竪琴（流れる分散和音）", "harp", patch="folkHarp", volume=0.07, pan=0.3, reverb=0.55, sustain=1.4, barGain=c.g())

# ---------- 子守歌（B♭ の5音。1=B♭4。F4〜D5） ----------
A = ["1:2 2:1 3:3", "2:2 1:1 6,:3", "5,:2 6,:1 1:2 2:1", "1:6",
     "3:2 2:1 1:2 6,:1", "5,:3 6,:3", "1:2 6,:1 5,:2 6,:1", "1:6"]
A2 = ["1:2 2:1 3:3", "2:2 1:1 6,:3", "5,:2 6,:1 1:2 2:1", "2:6",
      "3:2 2:1 1:2 2:1", "3:3 2:3", "1:2 6,:1 5,:2 6,:1", "1:6"]
Bm = ["6,:3 1:2 2:1", "3:3 2:2 1:1", "1:2 2:1 3:3", "2:6",
      "3:2 2:1 1:3", "6,:2 1:1 2:3", "1:2 6,:1 5,:2 6,:1", "5,:6"]          # 5（F）で止まる：開いたまま、次の波へ
REST = ["R:6", "1:6", "6,:6", "5,:6", "R:6", "3:6", "2:6", "1:6"]        # 休の波：笛は長い音だけ（眠りかけ）
STOP = ["1:2 2:1 3:3", "2:2 1:1 6,:3", "5,:2 6,:1 1:2 2:1", "1:6", "3:2 2:1 R:3", "R:6", "R:6", "R:6"]   # 5小節目の途中で消える
MEL = {"A": A, "A2": A2, "B": Bm, "休": REST, "消": STOP}
for k, w in enumerate(WAVES):
    play_melody(c, f"波{k + 1}", MEL[w], 4, "air", density=0.12 if w != "休" else 0.0, seed=500 + k)

# ---------- 竪琴の揺れ（波ごとに少しずつ弾き方を変える） ----------
for b in range(c.NB):
    n, i, Lb, kk = S.scene_of(b); ch = S.chords[b]
    root = re.match(r"^([A-G][#b]?)", ch).group(1)
    r = 41 + (PC[root] - 5) % 12                          # F2〜E3
    up = [x for x in range(58, 72) if x % 12 in chord_pcs(ch)][:3]
    if n == "鈴":
        if i == 1: HL.at(b * B, f"{nm(r)}:3"); HU[0].at(b * B + 3, f"{nm(up[0])}:3,"); HU[1].at(b * B + 3.05, f"{nm(up[1])}:3,")
        continue
    if n == "眠り":
        if i < 2:
            HL.at(b * B, f"{nm(r)}:3{',' if i else ''}"); HU[0].at(b * B + 3, f"{nm(up[0])}:3,")
        continue
    k = int(n[1:]) - 1; w = WAVES[k]
    HL.at(b * B, f"{nm(r)}:3")                                       # ゆりかごの低い音（1拍目）
    if k in (2, 5, 8) and w != "休":                                 # B の波：上が8分で流れる（舟が少し大きく揺れる）
        seq = [up[0], up[1], up[2], up[1]] if i % 2 == 0 else [up[1], up[2], up[1], up[0]]
        HA.at(b * B + 2, f"{nm(seq[0])}:1,")
        for q, x in enumerate(seq[1:]): HA.at(b * B + 3 + q, f"{nm(x)}:1{',' if q else ''}")
    else:                                                            # ふつうの揺れ：4拍目に上の2音（少しずらして）
        HU[0].at(b * B + 3, f"{nm(up[0])}:3,"); HU[1].at(b * B + 3.06, f"{nm(up[1])}:3,")
    if w == "休" and i % 2 == 1: HA.at(b * B + 5, f"{nm(up[2] + 12)}:1,")   # 休の波：高い1音が水面に落ちる
    if w == "消" and i >= 5: HU[1].at(b * B + 4.5, f"{nm(up[2])}:1.5,")      # 笛が消えたあとも、竪琴は揺れ続ける

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space hall --space-wet 0.32 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の005（第3版）。小舟の中で眠る夜の子守歌。6/8・付点4分＝50、B♭ の5音。主役は柔らかい笛で、狭い音域の同じ節をくり返す。伴奏はナイロン弦の竪琴のゆりかごの揺れと、舳先の小さな鈴（本物の録音）だけ。鈴の鳴る位置は波（8小節）ごとに8分音符1つずつずれていく（舟が流されていく）。歌は最後の波の途中で眠りに消える。",
       harm_scenes=None, tail_scene="眠り", double=False, fill=False, pads=False)

# ---------- 鈴（本物の録音 0292 を、和音の音に合わせて置く） ----------
SEC8 = 60 / BPM
F0 = 2716.0
HZ = {"Bb": 1864.7, "Eb": 1244.5, "Gm": 1568.0, "F": 1396.9}
def bell(b, eighth, db=-21, ln=5.0, lp=9000, pan=0.35):
    h = HZ.get(S.chords[b].split("|")[0], 1864.7)
    return {"t": round((b * B + eighth) * SEC8, 2), "file": "0292", "db": db, "len": ln, "pan": pan, "seek": 0.0,
            "semi": round(12 * math.log2(h / F0), 2), "hp": 200, "lp": lp}
ev = [bell(0, 0, -18)]                                              # 始まり：鈴の1音だけ
for k in range(len(WAVES)):
    s0 = c.s0[f"波{k + 1}"]; pos = k % 6                               # 波ごとに8分1つずつ後ろへ
    far = max(0, k - 8)
    for j in (0, 4):
        ev.append(bell(s0 + j, pos, -21 - 1.5 * far - (2 if j else 0), lp=int(9000 - 1200 * far), pan=0.3 + 0.04 * far))
ev.append(bell(c.s0["眠り"] + 1, 3, -26, lp=5000, pan=0.5))           # 最後の鈴
air = {"pre": 0.3, "tail": 7.0, "layers": [{"file": "1046", "db": -40, "hp": 110, "lp": 4500, "lfo": [round(6 * 8 * SEC8, 1), 0.3], "wide": 0.012, "duck": 0.4, "fade": 8}],
       "events": ev, "fx": {"far": {"db": -28, "delay": 0.2, "lp": 2800, "rt": 3.0}}}
json.dump(air, open("/tmp/cel/w/air005.json", "w"), ensure_ascii=False)
print("鈴の録音を置いた回数:", len(ev))
