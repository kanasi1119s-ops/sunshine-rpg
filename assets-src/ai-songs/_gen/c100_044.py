# ケルト・フルート100曲「銀の笛と百の夜」044 若き日の祖父 Grandfather, Young — 明るく速めの曲（2026-10-29）
# イメージ: 塔で見つけた古い記録。そこには、若い日の祖父が書いた日記と、走り書きの楽譜。
#   読むと、草原を走り回り、笛を吹きながら石の輪まで駆けてくる青年の姿が浮かぶ。最後の一行で、時が今に戻る。
# 形: 跳ねるリール（AABB を3周、だんだんにぎやかに）。最後に同じ旋律が半分の速さで鳴る（年をとった今の祖父）。4/4・♩=104。E ドリア。中盤〜終盤に明るい山。
# ただひとつ: 最後の8小節で、同じ旋律が半分の速さになる（伴奏も太鼓が抜け、ゆったりした竪琴と弦だけ）。
# 編曲の表:
#   駆け出す: いきなりギターのストロークとボーラン（2小節）
#   1周目   : 笛＋ボーラン（軽く）＋ギター＋チェロ
#   2周目   : ＋竪琴の3音オスティナート＋弦。笛の装飾が増える
#   3周目   : 山。＋笛の和声・ピチカート・内声
#   今      : 同じ旋律を半分の速さで。竪琴のゆったりした分散和音と弦だけ
import sys, json
from c100_common import *
from c100_v2 import *

S = Song("C100", "044-grandfather-young", "若き日の祖父", "Grandfather, Young", 104, 4, "E", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3})
AC = ["Em", "Em", "A", "D", "Em", "D", "A", "Em"]
BC = ["G", "Bm", "A", "A", "G", "Bm", "D", "Em"]
S.scene("駆け出す", 2, "intro", ["Em", "Em"])
for nm_ in ("1周目", "2周目", "3周目"): S.scene(nm_, 32, "verse" if nm_ != "3周目" else "chorus", AC * 2 + BC * 2)
S.scene("今", 8, "outro", ["Em", "Em", "Em", "Em", "A", "A", "D", "D"])
NAMES = ["駆け出す", "1周目", "2周目", "3周目", "今"]

c = make(S, NAMES,
         [("駆け出す", 0, 0.72), ("1周目", 0, 0.72), ("2周目", 0, 0.8), ("3周目", 0, 0.88), ("3周目", 24, 0.96), ("3周目", 31, 0.9), ("今", 0, 0.66), ("今", 7, 0.5)],
         {}, flute_gain={n: 1.1 for n in NAMES}, intro="駆け出す", passing=True, tension=False)
PIZZ = S.track("ピチカート", "strings", patch="pizzicato", volume=0.06, pan=-0.35, reverb=0.35, barGain=c.g())

A = ["1:0.5 2:0.5 3:0.5 5:0.5 4:0.5 3:0.5 2:0.5 3:0.5", "5:1 1':0.5 7:0.5 6:0.5 5:0.5 4:0.5 3:0.5",
     "4:0.5 5:0.5 6:0.5 4:0.5 3:0.5 4:0.5 5:0.5 3:0.5", "2:1 7,:0.5 2:0.5 5:1 4:1",
     "1:0.5 2:0.5 3:0.5 5:0.5 4:0.5 3:0.5 2:0.5 3:0.5", "5:0.5 6:0.5 7:0.5 1':0.5 2':1 7:1",
     "6:0.5 5:0.5 4:0.5 6:0.5 5:0.5 3:0.5 2:0.5 7,:0.5", "1:2 1:1 R:1"]
Bm = ["5:0.5 6:0.5 7:0.5 5:0.5 1':1 7:0.5 6:0.5", "5:0.5 7:0.5 2':0.5 7:0.5 1':1 6:1",
      "4:0.5 5:0.5 6:0.5 4:0.5 5:0.5 6:0.5 7:0.5 5:0.5", "6:1 4:0.5 6:0.5 5:2",
      "5:0.5 6:0.5 7:0.5 5:0.5 1':1 7:0.5 6:0.5", "5:0.5 7:0.5 2':0.5 7:0.5 1':0.5 7:0.5 6:0.5 5:0.5",
      "4:0.5 6:0.5 5:0.5 3:0.5 2:0.5 3:0.5 7,:0.5 2:0.5", "1:2 1:1 R:1"]
TUNE = A + A + Bm + Bm
def half(bars):   # 同じ旋律を半分の速さで（1小節が2小節に）
    out = []
    for s in bars:
        a, b_, acc = [], [], 0.0
        for tok in s.split():
            d, L = tok.split(":"); L2 = float(L) * 2
            if acc + L2 <= 4 + 1e-6: a.append(f"{d}:{L2:g}"); acc += L2
            elif acc < 4 - 1e-6: a.append(f"{d}:{4 - acc:g}"); b_.append(f"{d}:{L2 - (4 - acc):g}"); acc = 4
            else: b_.append(f"{d}:{L2:g}")
        out += [" ".join(a), " ".join(b_)]
    return out
play_melody(c, "1周目", TUNE, 4, "reel", density=0.5, seed=4401)
play_melody(c, "2周目", TUNE, 4, "reel", density=0.9, seed=4402)
play_melody(c, "3周目", TUNE, 4, "reel", density=1.1, seed=4403)
play_melody(c, "今", half(A[:3]) + ["2:4", "1:4"], 4, "air", density=0.4, seed=4404)

drive(c, ["駆け出す", "1周目", "2周目", "3周目"], kind="reel", soft_scenes=["駆け出す", "1周目"])
B = S.beats
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    if n == "今":   # 今の祖父：太鼓とギターは抜け、ゆったりした竪琴と弦
        t = tones(ch, "E3", "E5")
        c.HARP.bar(b, " ".join(f"{nm(x)}:1" for x in (t[0], t[2], t[4 % len(t)], t[2])))
        v = voice(ch, 55, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
        c.LOW.bar(b, f"{nm(r)}:4")
        continue
    c.LOW.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2" if n != "駆け出す" else f"{nm(r)}:4")
    if n in ("2周目", "3周目"):
        harp_ostinato(c.HARP, b, B, tones(ch, "E4", "E5")[:3])
        v = voice(ch, 55 if n == "2周目" else 59, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:4")
    if n == "3周目": PIZZ.bar(b, f"{nm(r + 12)}:1 R:1 {nm(r + 19)}:1 R:1")
    if n == "1周目":
        v = voice(ch, 52, 2, spread=True)
        for j in range(2): c.STR[j].bar(b, f"{nm(v[j])}:4")
rich(c, choir_scenes=["3周目"], pulse_scenes=["2周目", "3周目"], guitar=False, pizz=False, inner=True)
thick(c); sparkle(c)   # 2026-10-29: 速い曲の厚さ（023 7.27→7.53・025 7.26→7.66）＋高いきらめき
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.28 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の044（明るく速めの曲）。古い記録の中の、若い日の祖父。リール AABB を3周、4/4・♩=104、E ドリア。いきなりギターとボーランで駆け出し、だんだんにぎやかに。最後の8小節で、同じ旋律が半分の速さになり、時が今に戻る。",
       harm_scenes=None, tail_scene="今", fill=False, pads=True, pad_scenes=["1周目", "2周目", "3周目", "今"], floor=True)
air = {"pre": 0.2, "tail": 6.0, "layers": [{"file": "0908", "db": -37, "hp": 150, "lp": 6000, "wide": 0.014, "duck": 0.4, "fade": 6}],
       "fx": {"shimmer": {"db": -29, "rt": 6.0}, "far": {"db": -26, "delay": 0.2, "lp": 3000, "rt": 3.5}}, "intro_db": 6.0}
json.dump(air, open("/tmp/cel/w/air044.json", "w"), ensure_ascii=False)
