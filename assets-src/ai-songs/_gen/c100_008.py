# ケルト・フルート100曲「銀の笛と百の夜」008 港の別れ Parting at the Pier — 第3版（2026-10-29 作り直し。docs/sound/celtic-study/E-100-plan.md）
# 物語: 旅立ちの前の夜。港の酒場に村の人が集まる。いつもは速く踊る村のジグを、今夜はだれも速く弾けない。
#   アコーディオンのおじさんが、それをゆっくりのワルツにして弾きだす。みんな笑っているのに、泣いている。エイラも笛で加わる。
#   最後に、だれかが「また来いよ」と言う。曲は本来の速いジグに戻り、長調になって、みんなで踊る（帰る約束）。
# 調べ: 悲しみ。形: 速い踊りの節を遅いワルツで弾く → 最後に本来のジグ（長調）に戻る。
# 拍子・速さ: 3/4・♩=84（ワルツ）→ 最後の「約束」は 6/8 の弾み（付点4分＝72。1小節の中を 3+3 の8分で）。
# 旋法: A エオリア → 約束で A イオニア（同じ節が長調になる）。
# 主役は笛: 中音域で歌う。ワルツでは付点のゆったりした弾み、約束ではジグの装飾。
# 伴奏の主役: アコーディオン（左手の低音＋右手の和音のワルツ。始まりは1人でジグの節をゆっくり弾く）。脇: ナイロン弦ギター（語らいと約束だけ）。
#   竪琴・ピアノ・弦・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 同じ村のジグが、遅いワルツ（笑いながら泣く）→ 本来の速いジグ（長調）と、2つの顔で出てくる。
# 山: 2つ。中盤（ワルツB）と最後（約束）。最初が大きい形にはしない。
import sys, json
from c100_common import *
from c100_v2 import *

S = Song("C100", "008-parting-at-the-pier", "港の別れ", "Parting at the Pier", 84, 3, "A", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.45, "rubato": 0.25})
CA = ["Am", "Am", "G", "G", "Am", "F", "Em", "Am"]
CB = ["Am", "G", "F", "Em", "Am", "C", "Em", "Am"]
MA = ["A", "A", "E", "E", "A", "D", "E", "A"]
MB = ["A", "E", "D", "E", "A", "A", "E", "A"]
S.scene("ひとりで", 8, "intro", CA)
S.scene("ワルツA", 16, "verse", CA + CA)
S.scene("語らい", 16, "verse", CB[:4] + CA[4:] + CA[:4] + CB[4:])
S.scene("ワルツB", 16, "chorus", CB + CB)
S.scene("ワルツA2", 16, "verse", CA + CA)
S.scene("小さなB", 16, "verse", CB + CB)
S.scene("約束", 32, "chorus", MA + MA + MB + MB)
NAMES = ["ひとりで", "ワルツA", "語らい", "ワルツB", "ワルツA2", "小さなB", "約束"]
S.tempo = [{"bar": 1, "bpm": 80}, {"bar": 9, "bpm": 84, "ramp": 2}, {"bar": 88, "bpm": 80, "ramp": 2}, {"bar": 89, "bpm": 108}, {"bar": 120, "bpm": 100, "ramp": 1}]

c = make(S, NAMES,
         [("ひとりで", 0, 0.66), ("ワルツA", 0, 0.66), ("ワルツA", 15, 0.7), ("語らい", 0, 0.64), ("語らい", 15, 0.68),
          ("ワルツB", 0, 0.76), ("ワルツB", 4, 0.86), ("ワルツB", 12, 0.82), ("ワルツB", 15, 0.74), ("ワルツA2", 0, 0.7), ("ワルツA2", 15, 0.68),
          ("小さなB", 0, 0.6), ("小さなB", 15, 0.62), ("約束", 0, 0.74), ("約束", 16, 0.82), ("約束", 28, 0.92), ("約束", 31, 0.88)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="ひとりで", passing=True, tension=False)
B = S.beats
def gi(k=1.0): return [round(x * (k if c.scene_of_bar[b] == "ひとりで" else 1.0), 3) for b, x in enumerate(c.g())]   # 1回目は ×1.8 で前奏が -17dB、次のワルツA が -25dB と「最初が大きい」形になった
AM = S.track("アコーディオン（右手の節）", "accordion", volume=0.12, pan=-0.15, reverb=0.35, attack=0.05, release=0.35, barGain=gi())
AB = S.track("アコーディオン（左手の低音）", "accordion", volume=0.09, pan=-0.2, reverb=0.3, attack=0.03, release=0.3, barGain=gi())
AC = [S.track(f"アコーディオン（左手の和音{j + 1}）", "accordion", volume=0.05, pan=-0.2, reverb=0.3, attack=0.03, release=0.25, barGain=gi()) for j in range(3)]
GT = [S.track(f"ギター{i + 1}", "guitar", patch="nylonGuitar", volume=0.055, pan=0.35 + 0.04 * i, reverb=0.32, barGain=c.g()) for i in range(5)]
GA = S.track("ギター（分散和音）", "guitar", patch="nylonGuitar", volume=0.075, pan=0.4, reverb=0.35, barGain=c.g())

# ---------- 村のジグ（1小節＝8分6つ。「4分・8分・4分・8分」） ----------
JA = ["1:1 2:0.5 3:1 5:0.5", "6:1 5:0.5 3:1 1:0.5", "7,:1 2:0.5 4:1 2:0.5", "7,:1 6,:0.5 5,:1 7,:0.5",
      "1:1 2:0.5 3:1 5:0.5", "6:1 5:0.5 6:1 1':0.5", "7:1 5:0.5 4:1 2:0.5", "1:3"]
JB = ["3:1 5:0.5 1':1 5:0.5", "2':1 1':0.5 7:1 5:0.5", "6:1 1':0.5 3':1 1':0.5", "2':1 1':0.5 7:1 5:0.5",
      "3:1 5:0.5 1':1 2':0.5", "3':1 2':0.5 1':1 7:0.5", "5:1 7:0.5 2':1 7:0.5", "1':3"]
def waltz(bars):
    """ジグの1小節（4音）を、遅いワルツの付点の弾み（付点4分・8分・4分）にする。最後の音は捨てる"""
    out = []
    for s in bars:
        t = s.split()
        out.append(s if len(t) < 4 else f"{t[0].split(':')[0]}:1.5 {t[1].split(':')[0]}:0.5 {t[2].split(':')[0]}:1")
    return out
WA, WB = waltz(JA), waltz(JB)
# ひとりで：アコーディオンだけで、ワルツにした節をゆっくり
for t, L, m in section_events(c, "ひとりで", WA, 4):
    AM.at(t, f"{nm(m)}:{L}")
play_melody(c, "ワルツA", WA + WA[:7] + ["1:1.5 7,:0.5 1:1"], 4, "air", density=0.35, seed=801)
# 語らい：笛は低く、ジグの節のかけらを長くのばす（思い出話）。アコーディオンは長い和音
TALK = ["3:3", "2:1.5 1:1.5", "7,:3", "5,:3", "1:2 2:1", "3:3", "2:2 7,:1", "1:3",
        "R:3", "5:1.5 3:1.5", "2:3", "7,:3", "3:2 5:1", "1':2 7:1", "5:2 7,:1", "1:3"]
play_melody(c, "語らい", TALK, 4, "air", density=0.2, seed=802)
play_melody(c, "ワルツB", WB + WB, 4, "air", density=0.45, seed=803)
play_melody(c, "ワルツA2", WA + WA, 4, "air", density=0.55, seed=804)
SMALL = ["3:3", "2':3", "6:3", "5:3", "3:3", "R:3", "5:3", "1:3",
         "R:3", "2:1.5 1:1.5", "6,:3", "5,:3", "1:1.5 2:1.5", "3:3", "2:3", "R:3"]          # 小さなB：だれも歌わない。笛だけが小さく
play_melody(c, "小さなB", SMALL, 4, "air", density=0.1, seed=805)
KM = Key("A", "major", 4)
play_melody(c, "約束", JA + JA[:7] + ["1:1.5 5:1 7,:0.5"] + JB + JB[:7] + ["1':3"], 4, "march", key=KM, density=0.7, seed=806)   # 1拍＝4分なので、ジグの弾みは書いた「4分・8分」で出す（はずみの処理は使わない）

# ---------- 伴奏 ----------
def rt(ch, lo=40):
    r = PC[re.match(r"^([A-G][#b]?)", ch).group(1)]
    return lo + (r - lo) % 12                         # E2〜D#3
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = rt(ch); tn = [x for x in range(55, 68) if x % 12 in chord_pcs(ch)][:3]
    if n in ("ひとりで", "ワルツA", "ワルツB", "ワルツA2"):     # ワルツ：左手の低音（1拍目）と和音（2・3拍目）。2回目は5度の低音も
        AB.at(b * B, f"{nm(r if (i % 2 == 0 or n == 'ひとりで') else r + 7 - (12 if r + 7 > 52 else 0))}:1")
        for j in range(3):
            AC[j].at(b * B + 1, f"{nm(tn[j])}:0.8,"); AC[j].at(b * B + 2, f"{nm(tn[j])}:0.8,")
    elif n == "語らい":                                           # 蛇腹を長く引いた和音。ギターがゆっくり分散和音
        AB.at(b * B, f"{nm(r)}:3,")
        for j in range(3): AC[j].at(b * B, f"{nm(tn[j])}:3,")
        g = [x for x in range(48, 72) if x % 12 in chord_pcs(ch)]
        GA.bar(b, " ".join(f"{nm(g[q])}:0.5{',' if q % 2 else ''}" for q in (0, 2, 3, 4, 3, 2)))
    elif n == "小さなB":                                          # 小さく：低音と2拍目の和音だけ
        AB.at(b * B, f"{nm(r)}:1,")
        for j in range(2): AC[j].at(b * B + 1, f"{nm(tn[j])}:1.5,")
    elif n == "約束":                                             # ジグ：低音は1と4つ目の8分、和音は裏。ギターの付点のストローク
        AB.at(b * B, f"{nm(r)}:1"); AB.at(b * B + 1.5, f"{nm(r + 7 - (12 if r + 7 > 52 else 0))}:1,")
        for j in range(3):
            AC[j].at(b * B + 1, f"{nm(tn[j])}:0.5,"); AC[j].at(b * B + 2.5, f"{nm(tn[j])}:0.5,")
        if i < 31: strum(GT, b, B, ch, [(0, 1.5, "d", "!"), (1.5, 1, "d", ""), (2.5, 0.5, "u", ",")])
        else:
            strum(GT, b, B, ch, [(0, 3, "d", "!")]); AB.at(b * B, f"{nm(r)}:3")
            for j in range(3): AC[j].at(b * B, f"{nm(tn[j])}:3")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space room --space-wet 0.34 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の008（第3版）。旅立ちの前夜、港の酒場の集まり。村のジグを今夜はだれも速く弾けず、アコーディオンが遅いワルツにして弾く（笑いながら泣く）。3/4・♩=84、A エオリア。主役の笛が歌い、語らい・小さなBで静まり、最後に「また来いよ」で節が本来の速いジグ（A の長調）に戻って、みんなで踊る。伴奏はアコーディオンとナイロン弦ギター。",
       harm_scenes=None, tail_scene="約束", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "1046", "db": -48, "hp": 120, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -30, "delay": 0.14, "lp": 3000, "rt": 1.8}}}
json.dump(air, open("/tmp/cel/w/air008.json", "w"), ensure_ascii=False)
