# ケルト・フルート100曲「銀の笛と百の夜」041 立つ石 The Standing Stones — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 第5章のはじまり。森を抜けた丘の上に、石が輪になって立っている。言い伝えでは、安息日に踊った娘たちが石にされた姿だという。
#   エイラが石の前で笛を吹くと、凍りついた踊りがほんの少しずつ動きだし、だんだん本来の速さを取り戻す。途中、笛がやめても、
#   石の娘たちは音楽なしで踊り続ける。最後に全員がいちばん速く踊った頂点で、ぴたりと止まり、また石に戻る。
# 調べ: あいだ。形: 石になった踊り（とても遅いスリップ・ジグ → 本来の速さ）。A・B 8小節ずつ。
# 拍子・速さ: 9/8。付点4分＝40 → 120 へ、曲全体で速くなる（1拍＝付点4分、1小節＝3拍。8分は 1/3 拍）。旋法: G ドリア。
# 主役は笛（凍った笛 → 動く笛）。伴奏の主役: 低いドローン（チェロ G3・ビオラ D4）と、石を打つ乾いた音（枠太鼓の小さい太鼓）。打楽器あり。
#   竪琴・ギター・ピアノ・パッド・2本目の笛は使わない。
# この曲だけ: 中盤、旋律が抜けて伴奏（石の打音とドローン）だけが踊り続ける（音楽なしで踊る娘たち）。
# 始まり: 石の打音 → 終わり: 速い踊りの頂点で、ぴたりと止まる。
# 山: 最後に崖（いちばん速く、いちばん強い所で止まる）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "041-the-standing-stones", "立つ石", "The Standing Stones", 40, 3, "G", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
K = Key("G", "dorian", 4)
T3 = 1 / 3
def e2b(bars):
    return [" ".join(f"{t.split(':')[0]}:{round(float(t.split(':')[1]) / 3, 4)}" for t in s_.split()) for s_ in bars]
CA = ["Gm", "F", "Gm", "Dm", "Gm", "F", "C", "Gm"]
CB = ["Gm", "C", "F", "Dm", "Gm", "F", "C", "Gm"]
SC = [("石", 4, "intro", ["Gm"] * 4), ("凍った踊り", 16, "verse", CA + CB), ("溶ける", 16, "verse", CA + CB), ("動く", 32, "verse", CA + CA + CB + CB),
      ("踊る娘", 16, "verse", CA + CB), ("崖", 32, "chorus", CA + CA + CB + CB), ("石に戻る", 1, "outro", ["Gm"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("石", 0, 0.68), ("凍った踊り", 0, 0.68), ("溶ける", 0, 0.72), ("動く", 0, 0.76), ("踊る娘", 0, 0.78), ("崖", 0, 0.84), ("崖", 31, 0.96),
          ("石に戻る", 0, 0.96)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="石", passing=True, tension=False)
S.fix_avoid = lambda t: 0
s = c.s0
S.tempo = [{"bar": 1, "bpm": 40}, {"bar": s["凍った踊り"] + 1, "bpm": 40}, {"bar": s["溶ける"] + 1, "bpm": 55, "ramp": 16},
           {"bar": s["動く"] + 1, "bpm": 85, "ramp": 16}, {"bar": s["踊る娘"] + 1, "bpm": 110, "ramp": 32}, {"bar": s["崖"] + 1, "bpm": 110},
           {"bar": s["石に戻る"] + 1, "bpm": 120, "ramp": 32}]
B = S.beats
G = c.g()
# 長い弦（004 で笛と並べて測った値。笛の約5dB 下）。踊る娘の所は少し前に
DV = [S.track(f"ドローン（{nm_}）", "strings", patch=pt, volume=v, gainDb=gd, pan=p, reverb=0.6, release=0.15,
              barGain=[round(x * {"踊る娘": 1.6, "石": 2.0}.get(S.scene_of(b)[0], 1.4), 3) for b, x in enumerate(G)])   # 1回目（7.41）は石の所（約18秒）が -38dB だった
      for nm_, pt, v, gd, p in [("チェロ G3", "cello", 0.02, 2, -0.2), ("ビオラ D4", "viola", 0.017, 0, 0.22),
                                ("チェロ G3・弓返し", "cello", 0.02, 2, -0.2), ("ビオラ D4・弓返し", "viola", 0.017, 0, 0.22)]]
ST = [S.track(f"石の打音{j + 1}", "guitar", patch="frameDrum", volume=0.35, gainDb=18, pan=-0.15 + 0.3 * j, reverb=0.35, barGain=G) for j in range(2)]

# ---------- スリップ・ジグ（G ドリア。1=G4。8分＝1、1小節＝9） ----------
A = ["1:2 5:1 4:2 3:1 2:2 1:1", "7,:2 2:1 4:2 2:1 7,:3", "1:2 3:1 5:2 6:1 5:2 3:1", "4:3 2:3 7,:3",
     "1:2 5:1 4:2 3:1 2:2 1:1", "7,:2 2:1 5:2 4:1 3:3", "4:2 6:1 1':2 6:1 5:2 4:1", "3:3 2:3 1:3"]
Bm = ["5:2 1':1 7:2 6:1 5:2 4:1", "3:2 5:1 1':3 7:3", "6:2 4:1 2:2 4:1 6:2 1':1", "7:3 5:3 3:3",
      "5:2 1':1 2':2 1':1 7:2 5:1", "6:2 4:1 2:2 7,:1 2:3", "4:2 3:1 2:2 1:1 7,:2 2:1", "1:9"]
play_melody(c, "凍った踊り", e2b(A + Bm), 4, "air", key=K, density=0.0)                    # 凍った笛：飾りなし、遅いまま
play_melody(c, "溶ける", e2b(A + Bm), 4, "air", key=K, density=0.15, seed=4101)
play_melody(c, "動く", e2b(A + A + Bm + Bm), 4, "march", key=K, density=0.35, seed=4102)
play_melody(c, "崖", e2b(A + A + Bm + Bm), 4, "march", key=K, density=0.55, seed=4103)
s0 = c.s0["石に戻る"]
c.FLUTE.at(s0 * B, "G5:1!")

# ---------- 石の打音（乾いた小さい太鼓 E3・F#3 と、大きい太鼓の消音 C#3） ----------
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); tr = ST[b % 2]
    if n in ("石", "凍った踊り"):
        tr.bar(b, f"E3:1! R:2" if i % 2 == 0 else f"R:2 F#3:1,")              # 凍った石：1小節に1打だけ
    elif n == "溶ける":
        tr.bar(b, f"E3:1! F#3:1, R:1")
    elif n == "動く":
        tr.bar(b, "E3:1! F#3:1, E3:1," if i % 4 else "C#3:1! F#3:1, E3:1,")
    elif n == "踊る娘":                                                      # 旋律なしで踊り続ける：打音が8分で踊る
        tr.bar(b, " ".join(f"{x}:{round(T3, 4)}{mk}" for x, mk in (("C#3", "!"), ("F#3", ","), ("E3", ","), ("E3", ""), ("F#3", ","), ("E3", ","), ("E3", ""), ("F#3", ","), ("F#3", ","))))
    elif n == "崖":
        tr.bar(b, " ".join(f"{x}:{round(T3, 4)}{mk}" for x, mk in (("C#3", "!"), ("F#3", ","), ("E3", ","), ("E3", "!"), ("F#3", ","), ("E3", ","), ("C#3", "!"), ("F#3", ","), ("E3", ","))))
    elif n == "石に戻る":
        tr.bar(b, "C#3:1! R:2")

# ---------- ドローン（G と D。踊る娘では1拍ごとに弓を返して、ドローンも踊る） ----------
end = (c.NB - 1) * B
d0, d1 = c.s0["踊る娘"] * B, c.s0["崖"] * B
k = 0
def hold(t0, t1):
    global k
    t = t0
    while t < t1 - 0.01:
        en = min(t1, t + 6.2)
        DV[0 + 2 * (k % 2)].at(round(t, 3), f"G3:{round(en - t, 3)}{',' if t else ''}"); DV[1 + 2 * (k % 2)].at(round(t + 0.05, 3), f"D4:{round(en - t - 0.05, 3)},")
        t += 6; k += 1
hold(0.0, d0)
t = d0
while t < d1 - 0.01:                                  # 踊る娘：1拍ごとに弓を返す
    DV[0 + 2 * (k % 2)].at(round(t, 3), "G3:1!"); DV[1 + 2 * (k % 2)].at(round(t + 0.02, 3), "D4:0.98")
    t += 1; k += 1
hold(d1, end)
DV[0].at(end, "G3:1!"); DV[1].at(end, "D4:1!")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.26 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の041（第3版）。第5章のはじまり、丘の上の立つ石（踊った娘たちが石にされたという石の輪）。スリップ・ジグ（9/8）、G ドリア。凍った踊りは付点4分＝40 で、笛は飾りのない遅い節。少しずつ溶けて、曲全体で 120 まで速くなる。伴奏は低いドローン（G と D）と、石を打つ乾いた枠太鼓の音。中盤は笛が抜けて、石の打音とドローンだけが踊り続ける。最後はいちばん速い頂点で、ぴたりと止まる。",
       harm_scenes=None, tail_scene="石に戻る", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 4.5, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -28, "delay": 0.24, "lp": 3000, "rt": 3.0}}}
json.dump(air, open("/tmp/cel/w/air041.json", "w"), ensure_ascii=False)

_p = sys.argv[1] if len(sys.argv) > 1 else None
if _p:
    _d = json.load(open(_p))
    for _pt in _d["parts"]:
        if isinstance(_pt.get("notes"), str):
            _pt["notes"] = " ".join(t for t in _pt["notes"].split() if not re.match(r"^R:0(\.0*)?$", t))
    json.dump(_d, open(_p, "w"), ensure_ascii=False)
