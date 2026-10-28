# ケルト・フルート100曲「銀の笛と百の夜」028 夕もやの川 River in the Dusk Haze — 第2版（2026-10-28）
# イメージ: 日が沈むころの川。はじめは対岸の木々までくっきり見えているのに、川霧がだんだん濃くなって、すべての輪郭がぼやけていく。
#   ピアノの音も、はじめは一粒ずつはっきりしているのが、ペダルをふんだまま重なっていき、最後は残響の霞だけが残る。
# 形（台帳）: スロー・エア・曲が進むほど残響が深くなり、輪郭がぼやける。4/4・♩=52。A ドリア。始め：はっきりしたピアノ／終わり：霞。山なし。
# 編曲の表:
#   鮮明   : ピアノの分散和音だけ（短く、粒がはっきり）
#   川1    : ＋笛。ピアノの音が少し長くなる
#   川2    : 笛の音が長くなる。弦がうすく。ピアノはペダルで重なる
#   もや   : 同じ節を倍の長さで。ピアノは長い音が重なり合う。霞の層が濃くなる
#   霞     : 笛の最後の音が霞に溶け、残響だけが残る
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 52
S = Song("C100", "028-river-in-the-dusk-haze", "夕もやの川", "River in the Dusk Haze", BPM, 4, "A", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.3})
MC = ["Am", "Am", "G", "D", "Am", "Em", "G", "Am", "C", "G", "D", "Am", "C", "G", "Em", "Am"]
S.scene("鮮明", 4, "intro", MC[:4])
S.scene("川1", 16, "verse", MC)
S.scene("川2", 16, "verse", MC)
S.scene("もや", 16, "verse", ["Am", "Am", "Am", "Am", "G", "G", "D", "D", "Am", "Am", "Em", "Em", "G", "G", "Am", "Am"])
S.scene("霞", 8, "outro", ["Am", "G", "Am", "Am", "Am", "Am", "Am", "Am"])
NAMES = ["鮮明", "川1", "川2", "もや", "霞"]

c = make(S, NAMES,
         [("鮮明", 0, 0.66), ("川1", 0, 0.64), ("川2", 0, 0.64), ("もや", 0, 0.62), ("霞", 0, 0.56), ("霞", 7, 0.32)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="鮮明", passing=True, tension=False)
PB = S.track("ピアノ（左手の低音）", "piano", volume=0.5, pan=-0.15, reverb=0.5, barGain=c.g())
CELLO = S.track("チェロ（川の深さ）", "strings", patch="cello", volume=0.075, pan=0.15, reverb=0.5, barGain=c.g())
P = [S.track(f"ピアノ{i + 1}", "piano", volume=[0.6, 0.54, 0.48][i], pan=[-0.2, -0.1, 0.0][i], reverb=0.5, barGain=c.g()) for i in range(3)]
M1 = ["5:2 4:1 3:1", "2:2 1:2", "7,:1 1:1 2:1 3:1", "4:4", "5:2 6:1 5:1", "4:1 3:1 2:2", "3:3 2:1", "1:4"]
M2 = ["3:2 5:2", "6:3 5:1", "4:2 3:2", "2:4", "3:2 4:1 5:1", "6:2 7:2", "6:3 5:1", "5:4"]
def stretch(bars):
    out = []
    for s in bars:
        a, b_, acc = [], [], 0
        for tok in s.split():
            d, L = tok.split(":"); L2 = float(L) * 2
            if acc + L2 <= 4 + 1e-6: a.append(f"{d}:{L2:g}"); acc += L2
            elif acc < 4 - 1e-6: a.append(f"{d}:{4 - acc:g}"); b_.append(f"{d}:{L2 - (4 - acc):g}"); acc = 4
            else: b_.append(f"{d}:{L2:g}")
        out += [" ".join(a), " ".join(b_)]
    return out
play_melody(c, "川1", M1 + M2, 4, "air", density=0.7, seed=2801)
play_melody(c, "川2", M2 + M1, 4, "air", density=0.7, seed=2802)
play_melody(c, "もや", stretch(M1), 4, "air", density=0.4, seed=2803)
play_melody(c, "霞", ["3:4", "2:4", "1:4", "1:4", "R:4", "R:4", "R:4", "R:4"], 4, "air", density=0)

B = S.beats
LEN = {"鮮明": 0.5, "川1": 1.0, "川2": 2.0, "もや": 4.0, "霞": 6.0}     # ピアノの音の長さ（ペダルで重なっていく）
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    t = tones(ch, "A2", "A5")
    if n == "霞" and i >= 3: continue
    seq = (t[0], t[2], t[4 % len(t)], t[3 % len(t)])
    for q, x in enumerate(seq):
        P[q % 3].at(b * B + q, f"{nm(x)}:{LEN[n]}")
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    PB.at(b * B, f"{nm(r)}:{max(2, LEN[n])}")
    if n != "鮮明": CELLO.bar(b, f"{nm(r)}:4")
    if n in ("鮮明", "川1", "川2", "もや") or (n == "霞" and i < 6):
        v = voice(ch, 52 if n in ("鮮明", "川1") else 55, 3 if n not in ("鮮明",) else 2, spread=True)
        for j in range(len(v)): c.STR[j].bar(b, f"{nm(v[j])}:4")
rich(c, choir_scenes=[], pulse_scenes=["川1", "川2"], guitar=False, pizz=False, inner=True)
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.4 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の028（第2版）。夕暮れの川に川霧が濃くなる。4/4・♩=52、A ドリア。スロー・エア。ピアノの音ははじめ一粒ずつはっきりしているのが、ペダルで重なってぼやけ、空間の霞がだんだん深くなる。最後は残響の霞だけ。",
       harm_scenes=None, tail_scene="霞", fill=False, pads=True, pad_scenes=["川1", "川2", "もや", "霞"])
air = {"pre": 0.4, "tail": 9.0, "layers": [{"file": "0864", "db": -37, "hp": 150, "lp": 5000, "wide": 0.014, "duck": 0.35, "fade": 8},
                                           {"file": "0114", "db": -39, "hp": 200, "lp": 6000, "wide": 0.012, "pan": 0.2, "duck": 0.3, "start": 120, "fade": 30}],
       "fx": {"glass": {"hz": [440.0, 880.0, 1318.5], "db": -28, "rt": 8.0, "start": 4}, "shimmer": {"db": -26, "rt": 10.0}, "far": {"db": -24, "delay": 0.35, "lp": 2200, "rt": 6.0},
              "haze": {"db": -24, "rt": 10.0}, "band": {"db": -37, "hz": 6000, "per": 29}, "ramp": [0.35, 1.5]}, "intro_db": 8.5}
json.dump(air, open("/tmp/cel/w/air028.json", "w"), ensure_ascii=False)
