# ケルト・フルート100曲「銀の笛と百の夜」013 丘の上の孤独 Alone on the Hill — 第3版（2026-10-30 作り直し。docs/sound/celtic-study/E-100-plan.md）
# 物語: 羊飼いたちと別れたあと、エイラはひとり丘の上に座る。祖父のこと、灯台のこと。だれもいない丘で、笛だけが歌い手になる。
# 調べ: 悲しみ。形: ショーン・ノース（アイルランドの無伴奏の歌い方）風。拍を感じさせない自由なリズムで、同じ旋律を3回、装飾だけを変えて歌う。
# 拍子・速さ: 4/4 だが ♩=50 前後で大きくゆれる（rubato）。旋法: E エオリア。
# 主役は笛（歌い手のように。番ごとに装飾＝メリスマを変える。1番はほぼ素、2番は長い音の前に回り込む装飾、3番は下からすくい上げる装飾と、句の中の間）。
# 伴奏: なし。3番だけ、低いチェロの長い1音（E）が下で鳴る。竪琴・ギター・ピアノ・弦の和音・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 同じ旋律を3回、装飾だけを変えて歌う。最後の句は、話すように1音ずつ置く。
# 始まり: 笛ひとりの「うなり」（低いミを長く、息をふくらませる）→ 終わり: 最後の句を話すように置く。
# 山: 前半に1つ（1番の3つ目の句）。3番はチェロが入って少しふくらむ（最初が大きくだんだん小さくなる形にはしない）。
import sys, json, random
from c100_common import *
from c100_v2 import *
from c100_v2 import _dia

S = Song("C100", "013-alone-on-the-hill", "丘の上の孤独", "Alone on the Hill", 50, 4, "E", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"rubato": 0.6, "human": 0.5})
K = Key("E", "minor", 4)
CH = ["Em"] * 16
S.scene("うなり", 3, "intro", ["Em"] * 3)
S.scene("1番", 16, "verse", CH)
S.scene("2番", 16, "verse", CH)
S.scene("3番", 16, "chorus", CH)
S.scene("話す", 4, "outro", ["Em"] * 4)
NAMES = ["うなり", "1番", "2番", "3番", "話す"]
# 自由なリズム：句ごとに速さをゆらす（句の頭で少し急ぎ、句の終わりで大きくゆるむ）
tp = [{"bar": 1, "bpm": 44}]
for v, s0 in (("1番", 4), ("2番", 20), ("3番", 36)):
    for q in range(4):
        b = s0 + 4 * q
        tp += [{"bar": b, "bpm": 52 + (2 if v == "1番" and q == 2 else 0)}, {"bar": b + 3, "bpm": 42, "ramp": 1}]
tp += [{"bar": 52, "bpm": 40}]
S.tempo = tp
c = make(S, NAMES,
         [("うなり", 0, 0.68), ("1番", 0, 0.72), ("1番", 8, 0.86), ("1番", 15, 0.74), ("2番", 0, 0.72), ("2番", 15, 0.72),
          ("3番", 0, 0.76), ("3番", 8, 0.8), ("3番", 15, 0.74), ("話す", 0, 0.7), ("話す", 3, 0.66)],
         {}, flute_gain={n: 1.25 for n in NAMES}, intro="うなり", passing=True, tension=False)
B = S.beats
# 3番の低いチェロ：長い音は立ち上がりが遅く小さく鳴るので、強さ 1.5 前後（007 で測った）。E3 で（E2 は小さすぎる）
VC = S.track("低いチェロ（3番だけ）", "strings", patch="cello", volume=0.09, pan=0.15, reverb=0.6, barGain=[1.5] * 60)

# ---------- 旋律（E エオリア。1=E4。4つの句。2つ目の句の F♯5 が一番高い所） ----------
L1 = ["1:1 3:1 5:1.5 4:0.5", "3:2 2:1 1:1", "7,:1 1:1 3:2", "2:4"]
L2 = ["5:1 7:1 1':1.5 7:0.5", "2':2 1':1 7:1", "5:1 7:1 1':1 5:1", "4:4"]
L3 = ["3:1 5:1 4:1 3:1", "2:1.5 3:0.5 5:2", "4:1 3:1 2:1 7,:1", "1:4"]
L4 = ["1:1 3:1 5:1.5 4:0.5", "3:2 2:1 1:1", "7,:1 2:1 1:2", "1:4"]
VERSE = L1 + L2 + L3 + L4

def melisma(ev, style, seed):
    """ショーン・ノースの装飾を、番ごとにちがう形で長い音に付ける。ev: (拍, 長さ, MIDI)
    style 'turn' ＝ 長い音の前に上から回り込む（上・その音・下・その音）／'scoop' ＝ 下の2音からすくい上げ、長い音の途中に1拍の間"""
    rg = random.Random(seed); out = []
    for t, L, m in ev:
        if L >= 1.5 and rg.random() < 0.75:
            g = 0.16
            if style == "turn":
                up, dn = _dia(K, m, 1), _dia(K, m, -1)
                out += [(t, g, up), (t + g, g, m), (t + 2 * g, g, dn), (t + 3 * g, L - 3 * g, m)]
            else:
                a, b_ = _dia(K, m, -2), _dia(K, m, -1)
                out += [(t, g, a), (t + g, g, b_), (t + 2 * g, L - 2 * g - (0.5 if L >= 2 else 0), m)]
                if L >= 2: out.append((t + L - 0.5, 0.5, None))     # 句の中の小さな間（息）
        else:
            out.append((t, L, m))
    return out

def put(ev):
    for t, L, m in ev:
        if m is not None: c.FLUTE.at(round(t, 4), f"{nm(m)}:{round(L, 4)}")

# うなり：低いミを長く、息をふくらませてから、旋律のかけら
put([(t, L, m) for t, L, m in section_events(c, "うなり", ["1:4", "1:2 2:1 3:1", "2:2 1:2"], 4, key=K)])
put(section_events(c, "1番", VERSE, 4, key=K))                                   # 1番：ほぼ素
put(melisma(section_events(c, "2番", VERSE, 4, key=K), "turn", 1302))           # 2番：回り込む装飾
put(melisma(section_events(c, "3番", VERSE, 4, key=K), "scoop", 1303))          # 3番：すくい上げと間
# 話す：最後の句を、1音ずつ置く（あいだに間）
put(section_events(c, "話す", ["1:1 R:0.5 3:0.5 R:0.5 5:1.5", "4:0.5 R:0.5 3:1 R:1 2:1", "R:0.5 7,:1 R:0.5 2:1 R:1", "1:4"], 4, key=K))

# 3番：低いチェロの長い1音（E3）。2小節ごとに弓を返す（つなぎ目が目立たないよう、少し重ねる）
s3 = c.s0["3番"]
for q in range(8):
    VC.at(round((s3 + 2 * q) * B + (0.05 if q else 0), 3), f"E3:{8 if q < 7 else 8}{',' if q % 2 else ''}")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.36 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の013（第3版）。羊飼いたちと別れたあと、ひとり丘の上で。アイルランドの無伴奏の歌い方（ショーン・ノース）のように、笛が歌い手になる。自由なリズム、E エオリア。同じ旋律を3回、装飾だけを変えて歌い（1番は素、2番は回り込み、3番はすくい上げと間）、3番だけ低いチェロの1音が下で鳴る。最後の句は話すように1音ずつ置く。",
       harm_scenes=None, tail_scene="話す", double=False, fill=False, pads=False)
air = {"pre": 0.4, "tail": 7.0, "layers": [{"file": "0595", "db": -42, "hp": 160, "lp": 3800, "wide": 0.014, "duck": 0.4, "fade": 8}],
       "fx": {"far": {"db": -25, "delay": 0.3, "lp": 2800, "rt": 4.0}}}
json.dump(air, open("/tmp/cel/w/air013.json", "w"), ensure_ascii=False)
