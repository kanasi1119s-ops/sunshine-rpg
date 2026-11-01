# ケルト・フルート100曲「銀の笛と百の夜」100 百の夜のおわり The End of a Hundred Nights — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 最後の夜。灯台の上で、エイラはひとりで、ゆっくりした「地」の節を吹く。すると、旅で出会った人たち、島の人たちが、
#   ひとりずつ、自分の楽器で一音だけを足していく。音は重なって一つの大きな和音になり、最後にエイラの笛の息が、夜空に消えていく。
# 調べ: 喜び。形: ゆっくりの「地」だけの独奏（16小節）→ 同じ地を2回くり返すあいだに、各章の楽器が2小節ごとに一音ずつ加わる（15の楽器）
#   → 全員の一つの和音 → 笛の息が消える。
# 拍子・速さ: 4/4。独奏は ♩=52（ゆれを大きく）→ ♩=60。旋法: D イオニア。
# 主役は笛（独奏の笛）。伴奏: これまでの章で使った楽器が一つずつ（竪琴・ギター・チェロ・フィドル・アコーディオン・ティン・ホイッスル・マリンバ・ホルン・
#   コントラバス・グロッケン・ビオラ・リードオルガン・ピチカート・木琴・枠太鼓）。どの楽器も、自分の一音（D の和音の音）だけを鳴らす。
# この曲だけ: これまでの章で使った楽器が、一音ずつ加わって一つの和音（D・A・F♯・E）になる。ティン・ホイッスルは自然な音域の中の E5（E6 は音域の外）。
# 始まり: 笛ひとり → 終わり: 笛の息が消える。
# 山: 終盤（全員の和音）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "100-the-end-of-a-hundred-nights", "百の夜のおわり", "The End of a Hundred Nights", 60, 4, "D", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3, "rubato": 0.2})
K = Key("D", "major", 4)
CG = ["D", "D", "G", "D", "D", "G", "D", "A", "D", "G", "D", "A", "G", "A", "D", "D"]
SC = [("独奏", 16, "intro", CG), ("一音ずつ", 32, "verse", CG * 2), ("一つの和音", 8, "chorus", ["D"] * 8), ("息が消える", 6, "outro", ["D"] * 6)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES, [("独奏", 0, 0.72), ("一音ずつ", 0, 0.7), ("一音ずつ", 31, 0.84), ("一つの和音", 0, 0.88), ("一つの和音", 7, 0.9), ("息が消える", 0, 0.76), ("息が消える", 5, 0.6)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="独奏", passing=True, tension=False)
S.fix_avoid = lambda t: 0
s = c.s0
S.tempo = [{"bar": 1, "bpm": 52}, {"bar": s["一音ずつ"] + 1, "bpm": 60, "ramp": 2}]
B = S.beats
G = c.g()

# ---------- 地（16小節。1=D4） ----------
GR = ["1:2 3:2", "5:3 4:1", "3:2 2:2", "1:4", "3:2 5:2", "6:3 5:1", "4:2 3:2", "2:4", "5:2 1':2", "7:2 6:2", "5:2 4:1 3:1", "2:4", "3:2 2:1 1:1", "7,:2 2:2", "1:4", "1:4"]
play_melody(c, "独奏", GR, 4, "air", key=K, density=0.25, seed=10001)
play_melody(c, "一音ずつ", GR + GR, 4, "air", key=K, density=0.2, seed=10002)
play_melody(c, "一つの和音", ["5:2 6:2", "1':4", "2':2 1':2", "7:2 6:2", "5:4", "3':4", "2':4", "1':4"], 4, "air", key=K, density=0.2, seed=10003)
c.FLUTE.at(s["息が消える"] * B, "D5:20")

# ---------- 各章の楽器が、一音ずつ（2小節ごとに1つ。減る音の楽器は2小節ごとにそっと打ちなおす） ----------
# (名前, instrument, patch, volume, gainDb, 音, 減る音か)  ※音量は各章で測った値（004・044・047・049・060・063 など）を元に、和音の1音として小さめに
JOIN = [("竪琴（第1章）", "harp", "folkHarp", 0.09, 0, "D3", True),
        ("ナイロン弦ギター（第3章）", "guitar", "nylonGuitar", 0.014, 0, "A3", True),
        ("チェロ（第2章）", "strings", "cello", 0.02, 2, "D2", False),
        ("フィドル（第4章）", "strings", "violin", 0.022, 3, "F#4", False),
        ("アコーディオン（第6章）", "accordion", None, 0.03, 0, "A4", False),
        ("ティン・ホイッスル（第7章）", "panflute", "tinWhistle", 0.008, 0, "E5", False),
        ("マリンバ（第5章）", "strings", "marimba", 0.045, 0, "D5", True),
        ("ホルン（第5章）", "brass", "horn", 0.09, 6, "A3", False),
        ("コントラバス（第6章）", "strings", "contrabass", 0.025, 3, "D2", False),
        ("グロッケン（第6章）", "bell", "glockenspiel", 0.022, 0, "F#6", True),
        ("ビオラ（第8章）", "strings", "viola", 0.017, 0, "F#3", False),
        ("リードオルガン（第7章）", "pad", "reedOrgan", 0.1, 6, "A3", False),
        ("ピチカート（第3章）", "strings", "pizzicato", 0.1, 5, "E4", True),
        ("木琴（第9章）", "xylophone", None, 0.05, 0, "A5", True),
        ("枠太鼓（第8章）", "guitar", "frameDrum", 0.3, 18, "C3", True)]
end = s["息が消える"] * B + 8                                             # 息が消える所で、楽器は2小節かけて抜ける
for k, (name, inst, patch, vol, gd, note, decay) in enumerate(JOIN):
    kw = dict(volume=vol, pan=round(-0.6 + 1.2 * k / (len(JOIN) - 1), 2), reverb=0.6, barGain=G)
    if patch: kw["patch"] = patch
    if gd: kw["gainDb"] = gd
    if inst in ("strings", "brass", "pad", "accordion"): kw["release"] = 1.2
    tr = S.track(name, inst, **kw)
    t0 = (s["一音ずつ"] + 2 * k) * B
    stop = end - 0.5 * (len(JOIN) - k)                                    # 後から来た楽器ほど長く残る
    if decay:
        t = t0; first = True
        while t < stop - 0.5:
            L = 8 if note != "C3" else 1
            tr.at(round(t, 3), f"{note}:{min(L, round(stop - t, 2))}{'' if first else ','}")
            t += 8; first = False
    else:                                                                 # のばす楽器は16拍ずつ、そっと弾きなおす（1つの音は長すぎると読めない。1回目の書き出しで失敗）
        t = t0; first = True
        while t < stop - 0.5:
            tr.at(round(t, 3), f"{note}:{min(16, round(stop - t, 2))}{'' if first else ','}")
            t += 16; first = False

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.34 --master -15 --widen 1.25 --side-hpf 200",
       "ケルト・フルート100曲の100（第3版）。最後の夜、灯台の上。笛ひとりが、ゆっくりした「地」の節（♩=52、ゆれを大きく）を吹く。同じ地を2回くり返すあいだに、これまでの章で使った15の楽器（竪琴・ギター・チェロ・フィドル・アコーディオン・ティン・ホイッスル・マリンバ・ホルン・コントラバス・グロッケン・ビオラ・リードオルガン・ピチカート・木琴・枠太鼓）が、2小節ごとに一つずつ、自分の一音だけを足していき、D・A・F♯・E の一つの和音になる（山）。最後は楽器がひとつずつ抜けて、笛の長い D の息が夜空に消える。",
       harm_scenes=None, tail_scene="息が消える", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 8.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3600, "wide": 0.012, "duck": 0.4, "fade": 8}],
       "fx": {"far": {"db": -26, "delay": 0.34, "lp": 2800, "rt": 4.6}}}
json.dump(air, open("/tmp/cel/w/air100.json", "w"), ensure_ascii=False)
