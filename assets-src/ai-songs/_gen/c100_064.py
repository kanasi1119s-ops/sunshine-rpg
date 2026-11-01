# ケルト・フルート100曲「銀の笛と百の夜」064 子らの輪唱 The Children's Round — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 朝の村の広場で、子どもたちが手拍子をしながら遊び歌をうたっている。ひとりの子がブリキの笛（ホイッスル）で節を吹こうとするが、
#   何度やってもどこかでまちがえる。エイラが笛で正しい節を吹いてみせると、子はまた挑戦する。7回目、ついに正しく吹けて、
#   みんなで輪唱になる。最後はまた、手拍子だけが残る。
# 調べ: 喜び。形: 子どもの遊び歌（8小節の短い節のくり返し）。子の挑戦（8小節）と笛のお手本（8小節）×7 → 輪唱 → 手拍子遊び → もう一回 → 手拍子だけ。
# 拍子・速さ: 2/4・♩=124。旋法: C イオニアの5音（C・D・E・G・A。子のまちがいだけが F）。
# 主役は笛（お手本の笛）と、子どものホイッスル（ティン・ホイッスル）。伴奏の主役: 手拍子と木琴。
#   竪琴・ギター・ピアノ・パッド・弦・2本目の笛は使わない。
# この曲だけ: 子どものホイッスルが同じ短い節を何度もまちがえて（音・つまずき・終わり方・途中で忘れる…）、最後に正しく吹ける。
# 始まり: 手拍子だけ → 終わり: 手拍子だけ。
# 山: 中盤（正しく吹けて、輪唱になる所）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "064-the-childrens-round", "子らの輪唱", "The Children's Round", 124, 2, "C", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35})
K = Key("C", "major", 5)
CT = ["C", "C", "C", "C", "C", "Am", "G", "C"]
CU = ["Am", "C", "C", "Am", "C", "C", "G", "C"]
SC = [("手拍子", 4, "intro", ["C"] * 4)] + [(f"挑戦{k + 1}", 16, "verse", CT * 2) for k in range(7)] + \
     [("輪唱", 34, "chorus", CT * 4 + ["C", "C"]), ("手拍子遊び", 48, "verse", CU * 6), ("もう一回", 48, "chorus", CT * 6), ("手拍子だけ", 8, "outro", ["C"] * 8)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("手拍子", 0, 0.78), ("挑戦1", 0, 0.72), ("挑戦4", 0, 0.76), ("挑戦7", 0, 0.8), ("輪唱", 0, 0.88), ("輪唱", 33, 0.94), ("手拍子遊び", 0, 0.82),
          ("もう一回", 0, 0.88), ("もう一回", 47, 0.92), ("手拍子だけ", 0, 0.82)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="手拍子", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# ホイッスルは笛より約10dB 大きい（011: 0.015 で子鴨）→ 子どもは 0.02。手拍子は seasonFx の B4（015 と同じ 0.15）
WH = S.track("子どものホイッスル", "panflute", patch="tinWhistle", volume=0.02, pan=0.35, reverb=0.35, barGain=G)
CL = [S.track(f"手拍子{j + 1}", "pad", patch="seasonFx", volume=0.15, pan=-0.3 + 0.6 * j, reverb=0.25, barGain=G) for j in range(2)]
XY = [S.track(f"木琴{j + 1}", "xylophone", volume=0.06, pan=-0.15 + 0.3 * j, reverb=0.3, barGain=G) for j in range(2)]

# ---------- 節（8分＝0.5。お手本の笛は 1=C5、ホイッスルは1オクターブ上の 1=C6、木琴は 1=C5） ----------
TT = ["5:0.5 5:0.5 6:0.5 5:0.5", "3:1 1:1", "2:0.5 2:0.5 3:0.5 2:0.5", "1:1 5,:1", "5:0.5 5:0.5 6:0.5 1':0.5", "6:1 5:1", "3:0.5 2:0.5 3:0.5 5:0.5", "1:1 R:1"]
UU = ["1':0.5 6:0.5 5:0.5 6:0.5", "1':1 R:1", "6:0.5 5:0.5 3:0.5 5:0.5", "6:1 R:1", "5:0.5 3:0.5 2:0.5 3:0.5", "5:0.5 6:0.5 5:1", "3:0.5 2:0.5 1:0.5 2:0.5", "1:1 R:1"]
def var(**rep):
    x = list(TT)
    for k, v in rep.items(): x[int(k[1:])] = v
    return x
MISTAKE = [
    var(b2="2:0.5 2:0.5 4:0.5 2:0.5"),                                         # 1回目: 音をまちがえる（F）
    var(b4="5:0.5 5:0.5 R:0.5 5:0.5", b5="6:0.5 R:0.5 5:1"),                    # 2回目: つまずく
    var(b6="3:0.5 2:0.5 3:0.5 4:0.5", b7="4:1 R:1"),                           # 3回目: 終わりがまちがう
    TT[:4] + ["R:2", "R:2", "R:2", "R:2"],                                     # 4回目: 途中で忘れる
    var(b1="3:1 2:1", b5="5:1 6:1"),                                           # 5回目: あちこち少しずつ
    var(b5="6:0.5 6:0.5 5:1"),                                                 # 6回目: ほとんど正しい
    list(TT),                                                                  # 7回目: 正しく吹ける
]
def put(track, bars, key, oct_, b0, mk=""):
    ev = []
    for j, s_ in enumerate(bars): ev += mel_events(key, s_, oct_, (b0 + j) * B)
    play(track, [(round(t, 4), L, m, mk) for t, L, m in ev])
    return ev
for k in range(7):
    s0 = c.s0[f"挑戦{k + 1}"]
    put(WH, MISTAKE[k], K, 6, s0)
    play_melody(c, f"挑戦{k + 1}", ["R:2"] * 8 + TT, 5, "reel", key=K, density=0.2 + 0.03 * k, seed=6400 + k)
# 輪唱：笛 → 2小節遅れでホイッスル → 4小節遅れで木琴（4回）
s0 = c.s0["輪唱"]
play_melody(c, "輪唱", TT * 4 + ["R:2", "R:2"], 5, "reel", key=K, density=0.4, seed=6410)
put(WH, TT * 4, K, 6, s0 + 2)
for q in range(4):
    put(XY[0], TT, K, 5, s0 + 4 + 8 * q, ",") if q < 3 else put(XY[0], TT[:6], K, 5, s0 + 4 + 8 * q, ",")
# 手拍子遊び：笛とホイッスルが交互に2小節ずつ
s0 = c.s0["手拍子遊び"]
for q in range(24):
    bars = UU[(q * 2) % 8:(q * 2) % 8 + 2]
    if q % 2 == 0: play_melody(c, "手拍子遊び", ["R:2"] * (2 * q) + bars + ["R:2"] * (46 - 2 * q), 5, "reel", key=K, density=0.35, seed=6420 + q)
    else: put(WH, bars, K, 6, s0 + 2 * q)
# もう一回：全員で
s0 = c.s0["もう一回"]
play_melody(c, "もう一回", TT * 6, 5, "reel", key=K, density=0.5, seed=6430)
put(WH, TT * 6, K, 6, s0, ",")

# ---------- 手拍子（B4）と木琴 ----------
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b)
    cl = CL[b % 2]
    if n in ("手拍子", "手拍子だけ"):
        cl.bar(b, "B4:0.5! R:0.5 B4:0.5 R:0.5" if not (n == "手拍子だけ" and i >= 6) else "B4:0.5, R:1.5")
    elif n in ("輪唱", "もう一回"):
        cl.bar(b, "B4:0.5! B4:0.5, B4:0.5 B4:0.5,")
    elif n == "手拍子遊び":
        cl.bar(b, "B4:0.5! R:0.25 B4:0.25, B4:0.5 B4:0.5!" if i % 2 else "B4:0.5! R:0.5 B4:0.5! R:0.5")
    else:
        cl.bar(b, "B4:0.5! R:0.5 B4:0.5, R:0.5")
    ch = S.chords[b]
    if n.startswith("挑戦") or n in ("手拍子遊び", "もう一回"):
        k_ = int(n[2]) if n.startswith("挑戦") else 9
        if k_ >= 3:                                              # 木琴は3回目の挑戦から
            r = {"C": 60, "Am": 57, "G": 55}[ch]
            XY[1].bar(b, f"{nm(r)}:0.5 {nm(r + 7)}:0.5, {nm(r + (3 if ch == 'Am' else 4))}:0.5 {nm(r + 7)}:0.5,")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.18 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の064（第3版）。朝の村の広場で、子どもたちの遊び歌。2/4・♩=124、C の5音。手拍子だけで始まり、子どものホイッスルが8小節の短い節を吹こうとして、毎回どこかでまちがえる（音・つまずき・終わり方・途中で忘れる…）。そのたびにエイラの笛が正しいお手本を吹き、7回目についに正しく吹ける。そこから笛・ホイッスル・木琴の輪唱になり（山）、手拍子遊び、もう一回全員で歌って、最後はまた手拍子だけが残る。",
       harm_scenes=None, tail_scene="手拍子だけ", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 3.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -30, "delay": 0.15, "lp": 3000, "rt": 1.8}}}
json.dump(air, open("/tmp/cel/w/air064.json", "w"), ensure_ascii=False)
