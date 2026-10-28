# ケルト・フルート100曲「銀の笛と百の夜」053 霧の中の灯 A Lantern in the Mist（2026-10-29。第6章 霧の湖）
# イメージ: 舟を漕ぎ出すと、あたりは白い霧。どちらが岸かもわからない。そのとき、霧の奥に小さな灯がひとつ、ゆれている。
#   灯に向かって漕いでいくと、灯は杭の上のランタンだった。だれがともしたのかはわからない。そのそばを通りすぎ、灯はまた霧の中に残る。
# 形: 霧 → 灯が見える → 近づく → 灯のそば（中盤の山）→ 見送る → 霧に残る。6/8・8分＝112・A ドリア。
# ただひとつ: ピアノの高い2音の小さなゆらぎ（16分のトレモロ。ときどき息をつく）が灯の炎。笛の旋律は、その炎のまわりを回るように
#   中心の音（E5）のまわりを小さく行き来する。最後は灯（ゆらぎ）だけが霧の中に残る。
# 編曲の表:
#   霧        : 低い弦の和音とチェロ、ナイロンギターが1本ずつゆっくり鳴る
#   灯が見える: 笛（小さく回る旋律）。遠くにピアノのゆらぎがかすかに
#   近づく    : ゆらぎが近く（大きく）なる。弦3声、内声の動き
#   灯のそば  : 笛の2つ目の節（上の音域）。笛の和声。ギターの分散和音が細かくなる
#   見送る    : 最初の節に戻る。ゆらぎは少しずつ遠くへ
#   霧に残る  : 笛は2小節で去り、ゆらぎと低い弦だけが残る
import sys, json, random
from c100_common import *
from c100_v2 import *

BPM = 112   # 8分音符＝112（付点4分＝約37）
S = Song("C100", "053-a-lantern-in-the-mist", "霧の中の灯", "A Lantern in the Mist", BPM, 6, "A", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.2})
P = ["Am", "G", "D", "Am", "C", "G", "D", "Em", "Am", "G", "D", "Am", "C", "D", "Am", "Am"]
Q = ["C", "D", "Em", "Am", "C", "G", "Am", "D", "C", "D", "Em", "Am", "C", "G", "D", "Am"]
S.scene("霧", 4, "intro", ["Am", "Em", "G", "Am"])
S.scene("灯が見える", 16, "verse", P)
S.scene("近づく", 16, "verse", P)
S.scene("灯のそば", 16, "chorus", Q)
S.scene("見送る", 16, "verse", P)
S.scene("霧に残る", 8, "outro", ["Am", "G", "Am", "Em", "Am", "Am", "Am", "Am"])
NAMES = ["霧", "灯が見える", "近づく", "灯のそば", "見送る", "霧に残る"]

c = make(S, NAMES,
         [("霧", 0, 0.6), ("灯が見える", 0, 0.62), ("近づく", 0, 0.68), ("灯のそば", 0, 0.76), ("灯のそば", 10, 0.84), ("灯のそば", 15, 0.76),
          ("見送る", 0, 0.68), ("霧に残る", 0, 0.62), ("霧に残る", 7, 0.45)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="霧", passing=True, tension=False)
FLAME = S.track("灯のゆらぎ（ピアノ）", "piano", volume=0.5, pan=0.25, reverb=0.65, barGain=c.g())
GTR = S.track("ナイロンギター（1本ずつ）", "guitar", patch="nylonGuitar", volume=0.07, pan=-0.35, reverb=0.45, barGain=c.g())
CELLO = S.track("チェロ（霧の底）", "strings", patch="cello", volume=0.08, pan=0.1, reverb=0.5, barGain=c.g())

M = ["5:3 4:1 5:1 6:1", "5:2 4:1 3:3", "4:3 5:1 4:1 3:1", "3:6",
     "5:3 4:1 5:1 6:1", "5:2 6:1 7:3", "6:3 5:1 4:1 3:1", "2:6",
     "5:3 4:1 5:1 6:1", "7:2 6:1 5:3", "6:3 1':1 7:1 6:1", "5:6",
     "3:3 4:1 5:1 3:1", "4:2 5:1 6:3", "5:3 4:1 3:1 2:1", "1:6"]
N = ["1':3 2':1 1':1 7:1", "6:2 7:1 1':3", "2':3 1':1 7:1 6:1", "5:6",
     "1':3 3':1 2':1 1':1", "7:2 1':1 2':3", "3':3 2':1 1':1 7:1", "6:6",
     "1':3 2':1 1':1 7:1", "6:2 7:1 1':3", "2':3 1':1 7:1 6:1", "5:6",
     "1':3 3':1 2':1 1':1", "7:2 1':1 2':3", "7:3 6:1 5:1 4:1", "5:6"]
play_melody(c, "灯が見える", M, 4, "air", density=0.4, seed=5301)
play_melody(c, "近づく", M, 4, "air", density=0.7, seed=5302)
play_melody(c, "灯のそば", N, 4, "air", density=0.8, seed=5303)
play_melody(c, "見送る", M, 4, "air", density=0.5, seed=5304)
play_melody(c, "霧に残る", ["5:3 4:1 3:1 2:1", "1:6", "R:6", "R:6", "R:6", "R:6", "R:6", "R:6"], 4, "air", density=0.2, seed=5305)

B = S.beats
rg = random.Random(53)
def flame(b, ch, level):
    """灯の炎：和音の高い2音を16分で行き来する。ときどき息をつく（休む）。level 0〜1"""
    t = [x for x in tones(ch, "G5", "E6")][:3]
    if len(t) < 2: t = t + [t[0] + 12]
    a, z = t[0], t[1] if rg.random() < 0.6 else t[-1]
    toks = []; q = 0
    while q < 12:
        if rg.random() < 0.12 and q not in (0,):
            L = rg.choice((1, 2)); L = min(L, 12 - q); toks.append(f"R:{L * 0.5}"); q += L; continue
        mk = "," if (q % 3) else ""
        toks.append(f"{nm(a if q % 2 == 0 else z)}:0.5{mk}"); q += 1
    FLAME.bar(b, " ".join(toks))
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "E3", "E5")
    CELLO.bar(b, f"{nm(r)}:6")
    nv = 2 if n in ("霧", "灯が見える") else 3
    v = voice(ch, 50 if n in ("霧", "霧に残る") else 54, nv, spread=True)
    for j in range(nv): c.STR[j].bar(b, f"{nm(v[j])}:6")
    if n == "霧": GTR.bar(b, f"{nm(t[0])}:2 {nm(t[2])}:2 {nm(t[4 % len(t)])}:2")
    elif n in ("灯が見える", "見送る", "霧に残る"): GTR.bar(b, f"{nm(t[0])}:1 {nm(t[2])}:1 {nm(t[4 % len(t)])}:1 {nm(t[3 % len(t)])}:1 {nm(t[2])}:1 {nm(t[1])}:1")
    elif n == "近づく": GTR.bar(b, " ".join(f"{nm(t[q % len(t)])}:1" for q in (0, 2, 4, 5, 4, 2)))
    else:
        GTR.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 4, 2, 5, 4, 2, 4, 6, 4, 2, 1)))
        c.HARP.bar(b, f"{nm(t[0])}:3 {nm(t[2])}:3")
    # 炎：灯が見える（後半から・かすか）→ 近づく → そば → 見送る → 霧に残る（最後の小節で消える）
    if (n == "灯が見える" and i >= 4) or n in ("近づく", "灯のそば", "見送る") or (n == "霧に残る" and i < 7): flame(b, ch, 1)
# 炎の大きさ（近さ）を場面で変える
lv = {"霧": 0, "灯が見える": 0.55, "近づく": 0.85, "灯のそば": 1.0, "見送る": 0.8, "霧に残る": 0.65}
FLAME.spec["barGain"] = [round(g * lv[c.scene_of_bar[b]], 3) for b, g in enumerate(FLAME.spec["barGain"])]
rich(c, choir_scenes=["灯のそば"], pulse_scenes=["近づく", "灯のそば", "見送る"], guitar=False, pizz=False, inner=True)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.4 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の053。霧の湖に、小さな灯がひとつゆれている。6/8・8分＝112、A ドリア。ピアノの高い2音の小さなゆらぎが灯の炎で、笛はそのまわりを回るように中心の音のまわりを小さく行き来する。近づき、そばを通りすぎ、最後は灯だけが霧の中に残る。",
       harm_scenes=None, tail_scene="霧に残る", fill=False, pads=True, pad_scenes=["灯が見える", "近づく", "灯のそば", "見送る", "霧に残る"], floor=True)
air = {"pre": 0.8, "tail": 7.0, "layers": [{"file": "0621", "db": -39, "hp": 150, "lp": 5000, "wide": 0.014, "duck": 0.35, "fade": 8}],
       "fx": {"shimmer": {"db": -29, "rt": 8.0}, "far": {"db": -24, "delay": 0.3, "lp": 2600, "rt": 5.0}}, "intro_db": 6.0}
json.dump(air, open("/tmp/cel/w/air053.json", "w"), ensure_ascii=False)
