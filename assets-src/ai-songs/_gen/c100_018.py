# ケルト・フルート100曲「銀の笛と百の夜」018 干し草の匂い Scent of Hay — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 夕立がやんだあと、干し草を積んだ納屋の軒下。エイラと、ギターを抱えた年寄りの農夫が、雨上がりの昼下がりをのんびり過ごす。
#   話すことはとりとめがなく、笛が話せばギターが答え、チェロ（納屋の奥で寝そべる大男）が句の終わりに「うん、うん」とあいづちを打つ。
#   そのうち、みんなうとうとして、話がゆっくりになって止まる。
# 調べ: 眠り。形: 二人のデュエット（のんびりした世間話）。笛とギターが句を交互に話し、最後は三人とも眠ってしまう。
# 拍子・速さ: 6/8・付点4分＝44（8分＝132）→ 終わりで付点4分＝34（8分＝102）までゆるむ。1拍＝8分で書く（1小節＝6拍）。旋法: G ミクソリディア。
# 主役は笛（まどろむ笛。G4〜E5 が中心）。伴奏の主役: ナイロン弦ギターの指弾き（分散和音と、句の答え）。脇: チェロのあいづち（2音だけ）。
#   竪琴・ピアノ・弦の和音・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: チェロが句の終わりに2音だけ「うん、うん」と答える（話が進むほど、あいづちが遅れて眠そうになる）。
# 始まり: 鳥の気配の笛（雨上がりの小鳥）→ 終わり: テンポがゆるんで止まる。
# 山: なし（平ら。昼寝の所が少しだけ小さい）。
import sys, json, re
from c100_common import *
from c100_v2 import *
from c100_v2 import _dia
import c100_v2 as _v2
_oc = _v2.open_chord
_v2.open_chord = lambda ch, lo=52, hi=76: _oc(ch, lo, hi)

S = Song("C100", "018-scent-of-hay", "干し草の匂い", "Scent of Hay", 132, 6, "G", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.45, "rubato": 0.25})
K = Key("G", "mixolydian", 4)
CH = ["G", "F", "C", "G", "G", "Am", "F", "G"]
SC = [("鳥", 4, "intro"), ("話1", 20, "verse"), ("話2", 20, "verse"), ("昼寝", 12, "verse"), ("話3", 20, "chorus"), ("止まる", 8, "outro")]
for n, L, kd in SC: S.scene(n, L, kd, (CH * 3)[:L])
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("鳥", 0, 0.62), ("話1", 0, 0.68), ("話2", 0, 0.7), ("昼寝", 0, 0.62), ("話3", 0, 0.7), ("止まる", 0, 0.66), ("止まる", 7, 0.58)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="鳥", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
sz = c.s0["止まる"]
S.tempo = [{"bar": 1, "bpm": 132}, {"bar": c.s0["昼寝"] + 1, "bpm": 124, "ramp": 3}, {"bar": c.s0["話3"] + 1, "bpm": 130, "ramp": 3},
           {"bar": sz + 1, "bpm": 102, "ramp": 8}]
G = c.g()
# 試し書き出し: 指弾きは笛とほぼ同じ大きさ → 0.08→0.055。チェロの短い2音は笛より 5〜10dB 小さい → gainDb 6
GT = S.track("ギター（指弾き）", "guitar", patch="nylonGuitar", volume=0.055, pan=-0.25, reverb=0.35, barGain=G)
GM = S.track("ギター（句の答え）", "guitar", patch="nylonGuitar", volume=0.1, pan=-0.3, reverb=0.35, barGain=G)
VC = S.track("チェロ（あいづち）", "strings", patch="cello", volume=0.12, gainDb=6, pan=0.3, reverb=0.45, barGain=[round(x * 1.5, 3) for x in G])

def put(track, s_, start, dens=None, seed=1):
    ev = [[round(t, 4), L, m] for t, L, m in mel_events(K, s_, 4, start)]
    if dens is None: ev = [(t, L, m, "") for t, L, m in ev]
    else: ev = ornament(ev, K, 132, "air", B, density=dens, seed=seed)
    play(track, ev)

# ---------- 笛の句（G ミクソリディア。1=G4。8分＝1、1小節＝6） ----------
F = [["5:3 4:2 3:1", "2:4 R:2"], ["3:2 4:1 5:2 6:1", "5:5 R:1"], ["1':3 7:2 5:1", "6:4 R:2"], ["4:2 3:1 2:2 7,:1", "1:5 R:1"],
     ["6:2 5:1 6:2 1':1", "7:3 5:3"], ["5:1 4:1 3:1 2:3", "1:6"]]
# ギターの答え（1小節。高い弦で）
ANS = ["5:1 6:1 5:1 3:3", "2:2 3:1 1:3", "6,:1 1:1 2:1 3:3", "5:2 4:1 2:3", "1':1 7:1 6:1 5:3", "3:1 2:1 1:1 5,:3"]
# チェロの「うん、うん」（G3→D3 と、同じ高さの2回をまぜる）。話が進むほど遅れる
UN = ["G3:1, R:0.5 D3:1.5", "D3:1, R:0.5 D3:1.5", "C3:1, R:0.5 G2:1.5"]

def unun(b, late, k):
    VC.at(b * B + 3 + late, UN[k % 3].replace("1.5", str(round(1.5 - min(late, 1.0), 2))))

# 鳥：雨上がりの小鳥（G5〜B5 の高さで短く。休みが多い。D6 より上は硬いので使わない）
s0 = c.s0["鳥"]
for j, s_ in enumerate(["R:2 2':0.5 3':0.5 2':1 R:2", "R:3 7:0.5 2':0.5 7:2", "R:1 3':0.5 2':0.5 3':1 R:1 2':2", "7:3 6:1 5:2"]):
    put(c.FLUTE, s_, (s0 + j) * B, dens=0.25, seed=1800 + j)

# 話1：笛が2小節話し、3小節目は長い音でうなずき、4小節目の前半でギターが答え、後半でチェロが「うん、うん」
s0 = c.s0["話1"]
for q in range(5):
    b0 = s0 + 4 * q; ph = F[q % 6]
    put(c.FLUTE, ph[0], b0 * B, dens=0.25, seed=1810 + q); put(c.FLUTE, ph[1].replace("R:2", "R:0").replace("R:1", "R:0").replace(" R:0", ""), (b0 + 1) * B, dens=0.2, seed=1820 + q)
    put(c.FLUTE, ["3:6", "5:6", "2:6", "1:6", "3:6"][q], (b0 + 2) * B, dens=0.1, seed=1830 + q)
    put(GM, ANS[q % 6], (b0 + 3) * B)
    unun(b0 + 3, 0.0, q)
# 話2：役を入れかえる。ギターが2小節話し、笛が2小節で答える（あいづちは少し遅れる）
s0 = c.s0["話2"]
for q in range(5):
    b0 = s0 + 4 * q; ph = F[(q + 2) % 6]
    put(GM, ANS[(q + 1) % 6], b0 * B); put(GM, ANS[(q + 3) % 6], (b0 + 1) * B)
    put(c.FLUTE, "R:3 " + ph[0].split()[0].split(":")[0] + ":3", b0 * B + 0, dens=0.1, seed=1840 + q)     # ギターが話すあいだ、笛は相づちのように1音
    put(c.FLUTE, "R:6", (b0 + 1) * B)
    put(c.FLUTE, ph[0], (b0 + 2) * B, dens=0.3, seed=1850 + q); put(c.FLUTE, ph[1], (b0 + 3) * B, dens=0.2, seed=1860 + q)
    unun(b0 + 3, 0.5, q + 1)
# 昼寝：笛は低く長く。ギターはゆっくりの分散和音。あいづちは8小節に1回、さらに遅れて
s0 = c.s0["昼寝"]
for j, s_ in enumerate(["1:6", "1:3 2:3", "3:6", "2:6", "7,:6", "1:6", "5,:3 6,:3", "1:6", "3:6", "2:3 1:3", "7,:6", "1:6"]):
    put(c.FLUTE, s_, (s0 + j) * B, dens=0.08, seed=1870 + j)
unun(s0 + 7, 1.0, 0)
# 話3：また目をさまして、笛とギターが同じ句を3度ちがいで一緒に話す
s0 = c.s0["話3"]
for q in range(5):
    b0 = s0 + 4 * q; ph = F[(q + 4) % 6]
    put(c.FLUTE, ph[0], b0 * B, dens=0.3, seed=1880 + q); put(c.FLUTE, ph[1], (b0 + 1) * B, dens=0.2, seed=1890 + q)
    put(c.FLUTE, F[(q + 1) % 6][0], (b0 + 2) * B, dens=0.25, seed=1900 + q); put(c.FLUTE, "1:6" if q % 2 else "3:6", (b0 + 3) * B, dens=0.1, seed=1910 + q)
    for j, s_ in enumerate([ph[0], ph[1]]):                      # ギターは3度下で（句の前半だけ）
        ev = [[round(t, 4), L, _dia(K, m, -2)] for t, L, m in mel_events(K, s_, 4, (b0 + j) * B)]
        play(GM, [(t, L, m, ",") for t, L, m in ev])
    unun(b0 + 3, 0.3, q)
# 止まる：句のかけらがゆっくりになり、最後のあいづちで止まる
s0 = c.s0["止まる"]
for j, s_ in enumerate(["5:1 4:1 3:1 2:3", "1:6", "3:2 2:1 1:3", "2:6", "1:6", "R:6", "R:6", "R:6"]):
    put(c.FLUTE, s_, (s0 + j) * B, dens=0.1, seed=1920 + j)
unun(s0 + 4, 0.8, 2)

# ---------- ギターの指弾き（6/8 の分散和音。1小節に6つ） ----------
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    v = _v2.open_chord(ch)
    if n == "鳥" and i < 2: continue
    if n == "止まる":
        if i < 4: GT.bar(b, " ".join(f"{nm(v[q % len(v)])}:1{',' if q % 3 else ''}" for q in (0, 2, 3, 1, 2, 4)))
        elif i == 4: GT.bar(b, " ".join(f"{nm(x)}:6," for x in v[:1]))
        continue
    if n == "昼寝":
        GT.bar(b, " ".join(f"{nm(v[q % len(v)])}:2," for q in (0, 3, 2)))
        continue
    GT.bar(b, " ".join(f"{nm(v[q % len(v)])}:1{',' if q % 3 else ''}" for q in (0, 2, 3, 1, 2, 4)))

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.28 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の018（第3版）。夕立のあと、干し草の納屋の軒下で。二人のデュエット（のんびりした世間話）、6/8・付点4分＝44 → 34、G ミクソリディア。笛とナイロン弦ギターが句を交互に話し、納屋の奥のチェロが句の終わりに2音だけ「うん、うん」とあいづちを打つ（話が進むほど遅れて眠そうになる）。始まりは雨上がりの小鳥、最後はみんなうとうとして止まる。",
       harm_scenes=None, tail_scene="止まる", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 6.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3800, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -28, "delay": 0.26, "lp": 2800, "rt": 3.0}}}
json.dump(air, open("/tmp/cel/w/air018.json", "w"), ensure_ascii=False)
