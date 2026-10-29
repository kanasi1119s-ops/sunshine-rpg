# ケルト・フルート100曲「銀の笛と百の夜」009 星を数える Counting the Stars — 第3版（2026-10-29 作り直し。docs/sound/celtic-study/E-100-plan.md）
# 物語: 旅立ちの前の夜。眠れないエイラは、灯台の上で星を数える。祖父に教わった数え方で、ひとつ、ふたつ…。
#   数えるたびに星がひとつ増え、笛の節もひとつずつ長くなる。数えきれなくなったころ、空は星でいっぱいになり、エイラは眠る。
# 調べ: 眠り。形: 句ごとに音が1つずつ増える（数を数える歌）→ 星の川 → 満天 → 最後の星。
# 拍子・速さ: 9/8・付点4分＝58（8分＝174）。旋法: E リディア（A♯ が、夜空の少し浮いた明るさ）。
# 主役は笛: 高めでも柔らかく（E4〜C♯6。高い所は息を少なく）。装飾はほとんどなし。
# 伴奏: 竪琴の倍音のような高く小さな和音（響かせる）と、グロッケンの点（星）だけ。
#   ギター・ピアノ・弦・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 1句目は1音、2句目は2音…13句目は13音。句ごとに最初から数え直し、1音ずつ足していく。
#   グロッケンの星も、句ごとに1つずつ増える（1句目は1つ、13句目は13）。
# 始まり: グロッケンの1音（一番星）→ 満天 → 終わり: グロッケンの最後の1音。
# 山: 平原 → 終盤に満天（いちばん星が多く、笛がいちばん高い）。最初が大きい形にはしない。
import sys, json, random
from c100_common import *
from c100_v2 import *

BPM = 174
S = Song("C100", "009-counting-the-stars", "星を数える", "Counting the Stars", BPM, 9, "E", "lydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35, "rubato": 0.2})
K = Key("E", "lydian", 4)
# 数える歌（13音）。句 k はこの最初の k 音を、1音＝付点4分（8分3つ）で吹き、1音ぶん息をつく
M = ["5", "6", "5", "3", "2", "3", "5", "1'", "7", "6", "4", "5", "1"]
CNT_BARS = [-(-(3 * k + 3) // 9) for k in range(1, 14)]          # 句ごとの小節数（1,1,2,2,2,3,3,3,4,4,4,5,5）
NC = sum(CNT_BARS)
S.scene("一番星", 2, "intro", ["E", "E"])
S.scene("数える", NC, "verse", [("E" if j % 4 < 2 else "F#/E") for j in range(NC)])
S.scene("星の川", 20, "verse", ["E", "F#/E", "C#m", "B", "E", "F#/E", "G#m", "B", "A", "F#", "C#m", "B", "E", "F#/E", "C#m", "B", "A", "B", "E", "E"])
S.scene("満天", 12, "chorus", ["E", "F#", "G#m", "B", "A", "F#", "C#m", "B", "E", "F#/E", "E", "E"])
S.scene("最後の星", 4, "outro", ["E", "E", "E", "E"])
NAMES = ["一番星", "数える", "星の川", "満天", "最後の星"]
c = make(S, NAMES,
         [("一番星", 0, 0.62), ("数える", 0, 0.64), ("数える", NC - 1, 0.68), ("星の川", 0, 0.7), ("星の川", 19, 0.76),
          ("満天", 0, 0.8), ("満天", 6, 0.88), ("満天", 11, 0.78), ("最後の星", 0, 0.66), ("最後の星", 3, 0.6)],
         {}, flute_gain={n: 1.1 for n in NAMES}, intro="一番星", passing=True, tension=False)
S.fix_avoid = lambda t: 0      # リディアの A♯ を直されないように
B = S.beats
GLS = [S.track(f"グロッケン（星{j + 1}）", "strings", patch="glockenspiel", volume=0.05, pan=[0.45, -0.3, 0.15, -0.55][j], reverb=0.7,
              barGain=[round(x * (3.0 if c.scene_of_bar[b] in ("一番星", "最後の星") else 1.0), 3) for b, x in enumerate(c.g())]) for j in range(4)]   # 星が重なっても前の星を切らないよう、4つのパートに順に置く
# 竪琴の倍音は1オクターブ上（E4・B4・F♯5）。E3 からの低い和音は小さく、句の切れ目と前奏が -40〜-56dB に沈んだ（2回目）
HH = [S.track(f"竪琴の倍音{j + 1}", "harp", patch="folkHarp", volume=0.07, pan=-0.35 + 0.25 * (j % 3), reverb=0.7, sustain=3.0, barGain=c.g()) for j in range(6)]   # 句ごとに3つずつ交互に使い、前の句の響きを切らない
HA = S.track("竪琴（星の川の流れ）", "harp", patch="folkHarp", volume=0.06, pan=-0.2, reverb=0.65, sustain=2.0, barGain=c.g())
rg = random.Random(9)
STAR = [m for m in range(76, 96) if (m - 64) % 12 in (0, 2, 4, 6, 7, 9, 11)]   # 星の高さ（E5〜B6 のリディア）

_n = [0]
def star(t, m=None, soft=True):
    GL = GLS[_n[0] % 4]; _n[0] += 1
    GL.at(round(t, 3), f"{nm(m or rg.choice(STAR))}:3{',' if soft else ''}")

# ---------- 一番星 ----------
s0 = c.s0["一番星"]
star(0, 88, soft=False)                                     # E6 の1音
for j, m in enumerate([64, 71, 78]): HH[j].at(s0 * B + 1.5 + j * 0.4, f"{nm(m)}:16.5")
HA.at(s0 * B + 6, "B5:3,"); HA.at(s0 * B + 10.5, "E5:3,")              # 一番星のあと、竪琴が2つ小さく光る（前奏の 2〜6 秒が -48〜-65dB に沈んだ）   # 一番星のすぐあとに、竪琴の倍音（E・B・F♯）。前奏が沈まないように（layering-techniques.md）

# ---------- 数える ----------
_hs = [0]
t = c.s0["数える"] * B
for k, nb in enumerate(CNT_BARS, start=1):
    line = " ".join(f"{d}:3" for d in M[:k])
    for st, L, m in mel_events(K, line, 4, t):
        c.FLUTE.at(round(st, 3), f"{nm(m)}:{L}")
    span = nb * B
    # 数え終わって息をつく間（最大 3 秒）：竪琴が、いま数えた最後の音を高い所でこだまする（星が答える）。
    #   2〜3回目は、この間が -40dB 前後に沈んだ（竪琴の和音は数秒で消える）
    rest0 = t + 3 * k; last = mel_events(K, f"{M[k - 1]}:1", 5, 0)[0][2]
    if span - 3 * k >= 3: HA.at(round(rest0 + 0.4, 3), f"{nm(last)}:3,")
    if span - 3 * k >= 6: HA.at(round(rest0 + 3.4, 3), f"{nm(mel_events(K, '5:1', 5, 0)[0][2])}:3,")
    for q in range(k):                                         # 句 k には星が k 個（句の中にちらばる）
        star(t + rg.uniform(0, span - 1.5))
    for o_ in range(0, span, 18):                             # 竪琴の倍音（E・B・F♯ か G♯）を2小節ごとに。2組を交互に使い、前の響きを切らない
        _hs[0] += 1                                            # （1回目は句の切れ目と長い句の後半が -40dB 前後に沈んだ）
        for j, m in enumerate([64, 71, 78 if k % 2 else 80]):
            HH[j + 3 * (_hs[0] % 2)].at(round(t + o_ + j * 0.4, 3), f"{nm(m)}:{min(22.5, span - o_ + 4.5)}{',' if o_ else ''}")
    t += span

# ---------- 星の川：数えきれなくなって、節がつながる ----------
RIVER = ["5:3 6:3 1':3", "2':6 1':3", "7:3 6:3 5:3", "4:6 5:3",
         "5:3 6:3 1':3", "3':6 2':3", "1':3 7:3 5:3", "6:9",
         "6:3 5:3 4:3", "4:6 6:3", "5:3 3:3 2:3", "2:9",
         "3:3 5:3 1':3", "2':6 4':3", "3':3 2':3 7:3", "1':6 5:3",
         "6:3 1':3 4':3", "3':6 2':3", "1':3 7:3 5:3", "1':9"]
play_melody(c, "星の川", RIVER, 4, "air", key=K, density=0.15, seed=901)
MAN = ["5':6 3':3", "4':6 2':3", "3':9", "2':6 1':3", "1':6 7:3", "6:6 4':3", "3':6 2':3", "1':9",
       "5:3 6:3 1':3", "2':9", "1':9", "R:9"]                     # 満天：いちばん高い所で長く（息は少なく）
play_melody(c, "満天", MAN, 4, "air", key=K, density=0.1, seed=902)

for b in range(c.s0["星の川"], c.NB):
    n, i, Lb, kk = S.scene_of(b); ch = S.chords[b].split("/")[0]
    tn = [x for x in range(52, 76) if x % 12 in chord_pcs(ch)]
    if n == "星の川":                     # 星は小節に2〜4つ。竪琴が付点4分で上へ流れる
        for q in range(2 + i // 6): star(b * B + rg.uniform(0, 7.5))
        HA.bar(b, " ".join(f"{nm(tn[q + (i % 2)])}:3{',' if q else ''}" for q in range(3)))
    elif n == "満天":                     # 満天：星は小節に5〜7つ。竪琴の倍音を下から広げる
        for q in range(5 + (i % 3)): star(b * B + rg.uniform(0, 8))
        for j in range(3): HH[j].at(round(b * B + j * 0.35, 3), f"{nm(tn[j * 2 + 1] if j * 2 + 1 < len(tn) else tn[-1])}:9,")
        HA.at(b * B + 4.5, f"{nm(tn[0])}:4.5,")
    elif n == "最後の星":                 # 星が減っていき、最後の1音
        if i < 3:
            for q in range(3 - i): star(b * B + rg.uniform(0, 6))
            if i == 0:
                for j, m in enumerate([64, 71, 76]): HH[j].at(round(b * B + j * 0.4, 3), f"{nm(m)}:18,")
        else: star(b * B, 88, soft=False)

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.3 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の009（第3版）。眠れない夜、灯台の上で星を数える。数える歌の形で、1句目は1音、2句目は2音…13句目は13音。グロッケンの星も句ごとに1つずつ増える。9/8・付点4分＝58、E リディア。数えきれなくなると節がつながり（星の川）、満天でいちばん高くなって、最後はグロッケンの1音。伴奏は竪琴の倍音とグロッケンだけ。",
       harm_scenes=None, tail_scene="最後の星", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 8.0, "layers": [{"file": "0595", "db": -50, "hp": 200, "lp": 3000, "wide": 0.012, "duck": 0.4, "fade": 8}],
       "fx": {"far": {"db": -27, "delay": 0.3, "lp": 3200, "rt": 4.0}}}
json.dump(air, open("/tmp/cel/w/air009.json", "w"), ensure_ascii=False)
