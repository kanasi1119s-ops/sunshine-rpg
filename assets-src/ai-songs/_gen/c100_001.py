# ケルト・フルート100曲「銀の笛と百の夜」001 銀の笛 The Silver Flute — 第3版（2026-10-29 作り直し。docs/sound/celtic-study/E-100-plan.md）
# 物語: 夕暮れの灯台の部屋。エイラが祖父の箱から銀の笛を取り出す。部屋の古い竪琴が、笛を呼ぶように鳴る。
#   2回呼んでも笛は黙ったまま。3回目に、エイラは初めて息を入れる。
# 調べ: あいだ。形: 古い竪琴の自由な前奏（呼ぶ×3）→ エア A・B・A' → 余韻。3/4・♩=56（前奏は♩=46）。D イオニア。
# 楽器は2つだけ: 笛（1本。重ねの笛なし）と、金属弦の竪琴（長く鳴らす手・止める手。歌Bだけ高い竪琴の鐘）。
#   弦・チェロ・パッド・グロッケン・打楽器は使わない。前奏の持ち上げも使わない。
# 竪琴の和音は3度を抜く（レとラ、ソとレ…）。長調とも短調とも決まらない響き。
# この曲だけ: 竪琴が3回呼び、3回目でやっと笛が答える。問いの3音「レ・ミ・ラ」は 087 で答えに、099 でふたたび戻る。
# 山: 歌Bの頭（曲の約半分の所）で一番高いラ。最初が大きくてだんだん小さくなる形にはしない。
import sys, json
from c100_common import *
from c100_v2 import *

S = Song("C100", "001-silver-flute", "銀の笛", "The Silver Flute", 54, 3, "D", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"rubato": 0.35, "human": 0.45})
S.tempo = [{"bar": 1, "bpm": 50}, {"bar": 11, "bpm": 54, "ramp": 2}]
S.scene("呼ぶ1", 4, "intro", ["D", "G", "D", "D"])
S.scene("呼ぶ2", 4, "intro", ["G", "A", "G", "G"])
S.scene("呼ぶ3", 4, "intro", ["D", "A", "D", "D"])
CA = ["D", "D", "G", "A", "D", "G", "Bm", "A", "Bm", "G", "D", "A", "D", "G", "A", "D"]
S.scene("歌A", 16, "verse", CA)
S.scene("歌B", 20, "chorus", ["D", "Bm", "G", "D", "Em", "D", "G", "A", "G", "D", "Em", "A", "D", "G", "A", "D", "D", "G", "A", "D"])
S.scene("語り", 16, "verse", CA)
S.scene("余韻", 8, "outro", ["D", "D", "D", "D", "D", "D", "D", "D"])
NAMES = ["呼ぶ1", "呼ぶ2", "呼ぶ3", "歌A", "歌B", "語り", "余韻"]

c = make(S, NAMES,
         [("呼ぶ1", 0, 0.58), ("呼ぶ2", 0, 0.6), ("呼ぶ3", 0, 0.62), ("歌A", 0, 0.66), ("歌A", 15, 0.72),
          ("歌B", 0, 0.8), ("歌B", 5, 0.9), ("歌B", 12, 0.8), ("歌B", 19, 0.7), ("語り", 0, 0.62), ("語り", 15, 0.6), ("余韻", 0, 0.58), ("余韻", 7, 0.5)],
         {}, flute_gain={n: 1.25 for n in NAMES}, intro="呼ぶ1", passing=True, tension=False)
# 金属弦の竪琴：長く鳴らす手（余韻3拍ほど）と、止める手（弾いてすぐ消す）
HR = S.track("竪琴（響かせる）", "harp", patch="folkHarp", volume=0.13, pan=-0.18, reverb=0.55, sustain=2.6, barGain=c.g())
HD = S.track("竪琴（止める）", "harp", patch="folkHarp", volume=0.11, pan=-0.05, reverb=0.4, sustain=0.45, barGain=c.g())
HB = S.track("竪琴（高い鐘）", "harp", patch="folkHarp", volume=0.06, pan=0.35, reverb=0.7, sustain=3.0, barGain=c.g())
B = S.beats
for tr in (HR, HD):
    bg = tr.spec["barGain"]
    for b in range(c.s0["歌A"]): bg[b] = round(bg[b] * 2.5, 3)

def roll(tr, b, notes, start=0.0, step=0.22, L=3.0, soft=True):
    """竪琴の和音を下からずらして鳴らす（上の音ほど少し遅く）"""
    for k, m in enumerate(notes): tr.at(round(b * B + start + k * step, 3), f"{nm(m)}:{L}{',' if (k and soft) else ''}")

# ---------- 前奏：竪琴が3回呼ぶ ----------
D2, A2, D3, E3, A3, G2, B2, G3 = 38, 45, 50, 52, 57, 43, 47, 55
s1 = c.s0["呼ぶ1"]
roll(HR, s1 + 0, [D2, A2, D3, E3, A3], step=0.3)
roll(HR, s1 + 1, [G2, D3, A3, 59])
HD.bar(s1 + 2, "D4:1 E4:1 A4:1"); HR.at((s1 + 2) * B + 2, "A4:3")          # 1回目の呼びかけ（レ・ミ・ラ）
roll(HR, s1 + 3, [D2, A2, D3, A3], step=0.4, soft=False)                     # 返事がない（低い D の響き。音は落とさない）
s2 = c.s0["呼ぶ2"]
roll(HR, s2 + 0, [G2, D3, A3, 62], step=0.3)
roll(HR, s2 + 1, [A2, E3, B2 + 12, 64], step=0.26)
HD.bar(s2 + 2, "G4:1 A4:1 D5:1"); HR.at((s2 + 2) * B + 2, "D5:3")          # 2回目（1段高い所から）
roll(HR, s2 + 3, [G2, D3, G3, D3 + 12], step=0.4, soft=False)
s3 = c.s0["呼ぶ3"]
roll(HR, s3 + 0, [D2, A2, D3, E3, A3], step=0.3)
HD.bar(s3 + 1, "A4:1 B4:1 E5:1"); HR.at((s3 + 1) * B + 2, "E5:3")          # 3回目
HR.at((s3 + 2) * B, "D2:3,"); HR.at((s3 + 3) * B, "A2:3,")

# ---------- 旋律（D イオニア・3/4。問いの3音「1・2・5」） ----------
Q = "1:1 2:1 5:1"
A = [Q, "5:2 6:1", "5:1 4:0.5 3:0.5 2:1", "2:3",
     Q, "6:1 1':1.5 7:0.5", "6:1 5:1 3:1", "5:3",
     "3:1.5 4:0.5 5:1", "6:1 5:1 4:1", "3:1 2:1 1:1", "3:2 2:1",
     "1:1 2:1 3:1", "5:2 4:1", "3:1.5 2:0.5 1:1", "1:3"]
Bm_ = ["5:1 1':1 2':1", "3':2 2':1", "1':1 7:1 6:1", "5:3",
       "6:1 1':1 3':1", "5':2 4':1", "3':1 2':1 1':1", "2':3",
       "1':1 6:1 5:1", "6:1.5 5:0.5 3:1", "2:1 3:1 5:1", "5:3",
       "3:1 2:1 1:1", "2:2 3:1", "5:1 3:1 2:1", "1:3",
       "5:1 1':1 2':1", "2':3", "1':1 6:1 5:1", "5:3"]
A2 = [Q, "5:3", "5:1 3:1 2:1", "2:3",
      Q, "6:1 5:2", "3:1 2:1 1:1", "2:3",
      "3:2 5:1", "6:2 5:1", "3:1 2:1 1:1", "2:3",
      "1:1 2:1 3:1", "5:3", "3:1.5 2:0.5 1:1", "1:3"]
play_melody(c, "呼ぶ3", ["R:3", "R:3", Q, "5:3"], 4, "air", density=0.0)
play_melody(c, "歌A", A, 4, "air", density=0.2, seed=101)
play_melody(c, "歌B", Bm_, 4, "air", density=0.3, seed=102)
play_melody(c, "語り", A2, 4, "air", density=0.1, seed=103)
play_melody(c, "余韻", [Q, "5:3", "R:3", Q, "5:3", "5:3", "R:3", "R:3"], 4, "air", density=0.0)

# ---------- 竪琴の伴奏（場面ごとに弾き方を変える） ----------
def dyad(ch, lo=38):
    """3度を抜いた和音：根音・5度・オクターブ・9度"""
    r = PC[re.match(r"^([A-G][#b]?)", ch).group(1)]
    m = lo + (r - lo) % 12
    return [m, m + 7, m + 12, m + 14]
for b in range(c.s0["歌A"], c.NB):   # 前奏（呼ぶ1〜3）は上で書いた
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    d = dyad(ch)
    if n == "歌A":   # 1拍目に低い2音を響かせ、3拍目に高い9度を止める手で。句の終わりは止めて間をあける
        HR.at(b * B, f"{nm(d[0])}:3"); HR.at(b * B + 0.12, f"{nm(d[1])}:3,")
        if i % 4 != 3: HD.at(b * B + 2, f"{nm(d[3] + 12)}:1,")
    elif n == "歌B":   # 下から上へ流れる6つの8分（開いた和音）。山の4小節は高い鐘
        seq = [d[0], d[1], d[2], d[3], d[2] + 7, d[3] + 12]
        HR.bar(b, " ".join(f"{nm(x)}:0.5{',' if q else ''}" for q, x in enumerate(seq)))
        if 4 <= i < 8: HB.at(b * B, f"{nm(d[2] + 24)}:3")
    elif n == "語り":   # 低音だけで語る（2小節に1つ）。句の終わりは止める手で1音
        if i % 2 == 0: HR.at(b * B, f"{nm(d[0])}:3")
        if i % 4 == 3: HD.at(b * B + 1, f"{nm(d[1] + 12)}:1,")
    elif n == "余韻":
        if i == 0: HR.at(b * B, f"{nm(d[0])}:3"); HR.at(b * B + 0.2, f"{nm(d[1])}:3,")
        if i == 2: roll(HR, b, [d[0], d[1], d[2]], step=0.35, soft=False)   # 笛が黙る小節も、竪琴の響きで音を落とさない
        if i == 3: HR.at(b * B, f"{nm(d[0] + 12)}:3,")
        if i in (6, 7): roll(HR, b, [d[0], d[1], d[2]] if i == 6 else [d[0], d[1]], step=0.4, soft=False)   # 息が消えたあとも、竪琴の低い響きが少し残る

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.32 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の001（第3版）。夕暮れの灯台の部屋、祖父の箱から銀の笛を取り出す。古い竪琴が自由な前奏で3回呼び、3回目に笛が初めて答える（問いの3音 レ・ミ・ラ）。エア A・B・A'、3/4・♩=56、D イオニア。楽器は笛と金属弦の竪琴だけ。最後は問いの3音をもう一度吹き、ラで息が消える。",
       harm_scenes=None, tail_scene="余韻", double=False, fill=False, pads=False)
air = {"pre": 0.4, "tail": 7.0, "layers": [{"file": "1046", "db": -42, "hp": 120, "lp": 4500, "wide": 0.012, "duck": 0.4, "fade": 8}],
       "fx": {"far": {"db": -27, "delay": 0.22, "lp": 2800, "rt": 3.2}}}
json.dump(air, open("/tmp/cel/w/air001.json", "w"), ensure_ascii=False)
