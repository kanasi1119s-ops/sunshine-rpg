# ケルト・フルート100曲「銀の笛と百の夜」099 灯台に戻る Back to the Lighthouse — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 鐘が鳴り、島が目覚めた日の夕方。エイラは旅の始まりの灯台の部屋に戻る。古い竪琴が、001 と同じように笛を呼ぶ。
#   エイラは 001 の旋律を吹く。同じ節なのに、旅をした分だけ、少し大人の吹き方になっている。
#   途中で、旅の各章で吹いた節が、一瞬ずつ思い出される。最後に、竪琴が最初に呼んだ問いの3音（レ・ミ・ラ）が、もう一度戻ってくる。
# 調べ: あいだ。形: 001 の旋律が帰ってくる（主題に戻るピーブロック型）：竪琴の前奏 → 001 の歌A → 歌B（チェロが加わる）→ 旅の思い出（6つの節を4小節ずつ）→ 001 の語り → 問いの3音。
# 拍子・速さ: 3/4・♩=60（001 は ♩=54。少し前へ）。旋法: D イオニア。
# 主役は笛（001 と同じ笛、少し大人の吹き方：飾りを少し多く、長い音をのびやかに）。
# 伴奏の主役: 金属弦の竪琴（001 と同じ：長く鳴らす手・止める手・高い鐘。3度を抜いた和音）。脇: チェロ（歌B と語り）。
#   ギター・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 旅の各章の音型が一瞬ずつ呼び戻される（水車の転がる分散音・妖精のオクターブの跳躍・羊飼いの長い音・子らの遊び歌・積み上がる鐘・087 の答えの3音）。
# 始まり: 竪琴の前奏 → 終わり: 001 の最初の3音（問いの3音）。
# 山: 前半（歌B）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "099-back-to-the-lighthouse", "灯台に戻る", "Back to the Lighthouse", 60, 3, "D", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3, "rubato": 0.2})
K = Key("D", "major", 4)
SC = [("竪琴の前奏", 4, "intro", ["D", "G", "D", "D"]), ("歌A", 16, "verse", ["D"] * 16), ("歌B", 20, "chorus", ["D"] * 20), ("旅の思い出", 24, "verse", ["D"] * 24),
      ("語り", 16, "verse", ["D"] * 16), ("問いの3音", 4, "outro", ["D"] * 4)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("竪琴の前奏", 0, 0.7), ("歌A", 0, 0.72), ("歌B", 0, 0.8), ("歌B", 14, 0.9), ("旅の思い出", 0, 0.76), ("語り", 0, 0.72), ("問いの3音", 0, 0.66)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="竪琴の前奏", passing=True, tension=False)
S.fix_avoid = lambda t: 0
s = c.s0
S.tempo = [{"bar": 1, "bpm": 50}, {"bar": s["歌A"] + 1, "bpm": 60, "ramp": 2}]
B = S.beats
G = c.g()
HR = S.track("竪琴（響かせる）", "harp", patch="folkHarp", volume=0.13, pan=-0.18, reverb=0.55, sustain=2.6, barGain=G)
HD = S.track("竪琴（止める）", "harp", patch="folkHarp", volume=0.11, pan=-0.05, reverb=0.4, sustain=0.45, barGain=G)
HB = S.track("竪琴（高い鐘）", "harp", patch="folkHarp", volume=0.06, pan=0.35, reverb=0.7, sustain=3.0, barGain=G)
VC = S.track("チェロ", "strings", patch="cello", volume=0.022, gainDb=3, pan=-0.3, reverb=0.65, release=0.6, barGain=G)
def roll(tr, b, notes, start=0.0, step=0.22, L=3.0, soft=True):
    for k, m in enumerate(notes): tr.at(round(b * B + start + k * step, 3), f"{nm(m)}:{L}{',' if (k and soft) else ''}")

# ---------- 001 の旋律（そのまま。問いの3音「1・2・5」＝レ・ミ・ラ） ----------
Q = "1:1 2:1 5:1"
A = [Q, "5:2 6:1", "5:1 4:0.5 3:0.5 2:1", "2:3", Q, "6:1 1':1.5 7:0.5", "6:1 5:1 3:1", "5:3",
     "3:1.5 4:0.5 5:1", "6:1 5:1 4:1", "3:1 2:1 1:1", "3:2 2:1", "1:1 2:1 3:1", "5:2 4:1", "3:1.5 2:0.5 1:1", "1:3"]
Bm_ = ["5:1 1':1 2':1", "3':2 2':1", "1':1 7:1 6:1", "5:3", "6:1 1':1 3':1", "5':2 4':1", "3':1 2':1 1':1", "2':3",
       "1':1 6:1 5:1", "6:1.5 5:0.5 3:1", "2:1 3:1 5:1", "5:3", "3:1 2:1 1:1", "2:2 3:1", "5:1 3:1 2:1", "1:3",
       "5:1 1':1 2':1", "2':3", "1':1 6:1 5:1", "5:3"]
A2 = [Q, "5:3", "5:1 3:1 2:1", "2:3", Q, "6:1 5:2", "3:1 2:1 1:1", "2:3", "3:2 5:1", "6:2 5:1", "3:1 2:1 1:1", "2:3", "1:1 2:1 3:1", "5:3", "3:1.5 2:0.5 1:1", "1:3"]
# 旅の思い出（4小節ずつ）
MEM = ["1:0.5 3:0.5 5:0.5 3:0.5 1:0.5 3:0.5", "2:0.5 4:0.5 6:0.5 4:0.5 2:0.5 4:0.5", "3:0.5 5:0.5 1':0.5 5:0.5 3:0.5 5:0.5", "1:3",      # 水車の転がる分散音
       "1:1 1':1 R:1", "5:1 5':1 R:1", "2:1 2':1 R:1", "1:3",                                                                            # 妖精のオクターブの跳躍
       "5:2 6:1", "5:2 3:1", "2:2 3:1", "1:3",                                                                                           # 羊飼いの長い音
       "5:0.5 5:0.5 6:0.5 5:0.5 3:1", "1:1 2:1 3:1", "2:1 1:1 R:1", "1:3",                                                               # 子らの遊び歌
       "1:3", "3:3", "5:3", "1':3",                                                                                                      # 積み上がる鐘
       "5:1 2:1 1:1", "1:3", "5:1 2:1 1:1", "1:3"]                                                                                      # 087 の答えの3音
play_melody(c, "歌A", A, 4, "air", key=K, density=0.3, seed=9901)                 # 少し大人の吹き方：飾りを少し多く
play_melody(c, "歌B", Bm_, 4, "air", key=K, density=0.35, seed=9902)
play_melody(c, "旅の思い出", MEM, 4, "air", key=K, density=0.15, seed=9903)
play_melody(c, "語り", A2, 4, "air", key=K, density=0.2, seed=9904)
play_melody(c, "問いの3音", [Q, "5:3", "R:3", "R:3"], 4, "air", key=K, density=0.0)    # 最後は、001 の最初の3音

# ---------- 竪琴（001 と同じ弾き方。3度を抜いた和音） ----------
D2, A2_, D3, E3, A3, G2, B2, G3 = 38, 45, 50, 52, 57, 43, 47, 55
roll(HR, 0, [D2, A2_, D3, E3, A3], step=0.3)
HD.bar(1, "D4:1 E4:1 A4:1"); HR.at(1 * B + 2, "A4:3")                       # 001 と同じ問いの3音で呼ぶ
roll(HR, 2, [G2, D3, A3, 59], step=0.3)
roll(HR, 3, [D2, A2_, D3, A3], step=0.4, soft=False)
ROOTOF = {"1": 38, "2": 45, "3": 38, "4": 43, "5": 38, "6": 43, "7": 45}
def chord_for(bar):
    tok = bar.split()[0].split(":")[0].replace("'", "").replace(",", "")
    r = ROOTOF.get(tok, 38)
    return [r, r + 7, r + 12, r + 14] if r != 45 else [r, r + 7, r + 12, r + 19]
for sc, bars in (("歌A", A), ("歌B", Bm_), ("旅の思い出", MEM), ("語り", A2)):
    s0 = s[sc]
    for i, bar in enumerate(bars):
        b = s0 + i; d = chord_for(bar)
        if sc == "歌A":
            roll(HR, b, d[:3], step=0.25) if i % 2 == 0 else HD.bar(b, f"R:1 {nm(d[2])}:1, {nm(d[3])}:1,")
        elif sc == "歌B":
            roll(HR, b, d, step=0.2)
            if i % 4 == 0: HB.at(b * B, f"{nm(d[1] + 24)}:4,")
            if i % 2 == 0: VC.at(b * B, f"{nm(d[0])}:{2 * B + 0.2}")
        elif sc == "旅の思い出":
            if i % 4 == 0: roll(HR, b, d[:3], step=0.35, L=6)
        else:
            roll(HR, b, d[:3], step=0.3)
            if i % 4 == 0: VC.at(b * B, f"{nm(d[0])}:{4 * B}")
s0 = s["問いの3音"]
roll(HR, s0, [D2, A2_, D3, A3], step=0.4, L=9)

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.3 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の099（第3版）。島が目覚めた日の夕方、旅の始まりの灯台の部屋に戻る。3/4・♩=60、D の長調。001 と同じ金属弦の竪琴が、同じ問いの3音（レ・ミ・ラ）で笛を呼び、笛が 001 の旋律（歌A・歌B）を、少し大人の吹き方で吹く（歌B が山。チェロが加わる）。続いて、旅の各章の節（水車の転がる分散音・妖精のオクターブの跳躍・羊飼いの長い音・子らの遊び歌・積み上がる鐘・087 の答えの3音）が4小節ずつ思い出される。001 の語りのあと、最後は問いの3音がもう一度戻ってくる。",
       harm_scenes=None, tail_scene="問いの3音", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 6.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3600, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 2800, "rt": 3.8}}}
json.dump(air, open("/tmp/cel/w/air099.json", "w"), ensure_ascii=False)
