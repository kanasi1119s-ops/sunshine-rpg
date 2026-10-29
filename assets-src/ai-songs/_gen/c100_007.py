# ケルト・フルート100曲「銀の笛と百の夜」007 潮の呼び声 Call of the Tide — 第3版（2026-10-29 作り直し。docs/sound/celtic-study/E-100-plan.md）
# 物語: 夕方の浜。沖の岩で、アザラシが鳴いている。この海辺には「アザラシの民」の昔話がある（陸に上がると人になり、やがて海に帰っていく）。
#   エイラは舟歌を吹く。陸の節と、海の節が交互に来る。陸の節は長調、海の節は同じ形のまま暗い色（ドリア）に変わる。
#   やがて歌は沖へ引かれ、海の節だけになる。最後に陸の節に戻ろうとするが、主音に帰りきらずに、5度で止まる。
# 調べ: あいだ。形: 舟歌（4小節の陸の節と4小節の海の節が交互）。6/8・付点4分＝56（8分＝168）。
# 旋法: 陸＝D イオニア（F♯・C♯）、海＝D ドリア（F・C）。（表では「6度だけ変わる」と書いたが、イオニアとドリアは3度と7度が変わる。表を直した）
# 主役は笛: 低め・うねる（D4〜F♯5）。装飾は少なめ、すべり込みで。
# 伴奏: ビオラとチェロの二重奏だけ（波）。チェロは6つの8分で上がって下がる波、ビオラは付点4分2つの、もう1つの波。
#   竪琴・ギター・ピアノ・パッド・弦の和音の持続・打楽器・2本目の笛は使わない。
# 始まり: 低い弦のうねり（チェロとビオラの長い音がふくらむ）→ 終わり: 5度（ラ）で止まり、解決しない。
# 山: 小さなうねりのくり返し（4小節ごとにふくらむ）。舟歌B（真ん中）が少しだけ高い。最初が大きい形にはしない。
import sys, json
from c100_common import *
from c100_v2 import *

BPM = 168
S = Song("C100", "007-call-of-the-tide", "潮の呼び声", "Call of the Tide", BPM, 6, "D", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.2})
KL = Key("D", "major", 4); KS = Key("D", "dorian", 4)
L1C, S1C = ["D", "G", "Em", "A"], ["Dm", "C", "C", "Dm"]
L2C, S2C = ["D", "A", "Em", "D"], ["Am", "Dm", "C", "Dm"]
LBC, SBC = ["D", "G", "A", "D"], ["Dm", "Am", "G", "Am"]
OKI = ["Dm", "C", "Dm", "Am"] * 4
S.scene("うねり", 4, "intro", ["D", "D", "Dm", "Dm"])
S.scene("呼び声", 4, "verse", S1C)
S.scene("舟歌A", 32, "verse", (L1C + S1C + L2C + S2C) * 2)
S.scene("舟歌B", 32, "chorus", (LBC + SBC) * 4)
S.scene("沖", 16, "verse", OKI)
S.scene("舟歌A2", 16, "verse", L1C + S1C + L2C + S2C)
S.scene("引き潮", 8, "outro", ["D", "G", "Em", "A", "A", "A", "A", "A"])
NAMES = ["うねり", "呼び声", "舟歌A", "舟歌B", "沖", "舟歌A2", "引き潮"]
pts = [("うねり", 0, 0.6), ("呼び声", 0, 0.62)]
for n, base in [("舟歌A", 0.68), ("舟歌B", 0.76), ("沖", 0.66), ("舟歌A2", 0.72)]:
    for q in range(0, {"舟歌A": 32, "舟歌B": 32, "沖": 16, "舟歌A2": 16}[n], 4):   # 4小節ごとに小さくふくらむ（波）
        pts += [(n, q, base - 0.03), (n, q + 2, base + 0.04)]
pts += [("引き潮", 0, 0.66), ("引き潮", 4, 0.62), ("引き潮", 7, 0.56)]
c = make(S, NAMES, pts, {}, flute_gain={n: 1.15 for n in NAMES}, intro="うねり", passing=True, tension=False)
S.fix_avoid = lambda t: 0      # 海の節の F・C（ドリア）を和音に合わせて直されないように
B = S.beats
def gi(k): return [round(x * (k if c.scene_of_bar[b] == "うねり" else 1.8 if c.scene_of_bar[b] == "呼び声" else 1.0), 3) for b, x in enumerate(c.g())]   # 前奏と呼び声（笛が少ない）は大きめに。3回目まで -34〜-49dB   # 1回目は前奏が -47dB（長い音2つだけ）
VC = S.track("チェロ（波）", "strings", patch="cello", volume=0.1, pan=-0.3, reverb=0.5, barGain=gi(5.0))
VA = S.track("ビオラ（もう1つの波）", "strings", patch="viola", volume=0.075, pan=0.35, reverb=0.55, barGain=gi(5.0))

# ---------- 旋律（1＝D4。陸はイオニア、海はドリアで、同じ度数が別の音になる） ----------
L1 = ["1:2 2:1 3:2 5:1", "6:3 5:2 3:1", "2:2 3:1 5:2 6:1", "5:6"]
S1 = ["5:2 3:1 2:2 1:1", "7,:3 1:2 3:1", "4:2 3:1 2:2 7,:1", "1:6"]
L2 = ["3:2 5:1 6:2 1':1", "7:3 6:2 5:1", "6:2 5:1 3:2 2:1", "3:6"]
S2 = ["5:2 6:1 7:2 6:1", "5:3 3:3", "4:2 3:1 1:2 7,:1", "1:6"]
LB = ["5:2 6:1 1':3", "2':2 1':1 6:3", "5:2 6:1 1':2 2':1", "3':6"]
SB = ["3':2 2':1 1':3", "7:2 6:1 5:3", "4:2 5:1 7:2 6:1", "5:6"]
def sing(scene, blocks, dens, seed):
    """blocks: [(節, 'L' か 'S')] を4小節ずつ置く。陸はイオニア、海はドリアの鍵で"""
    s0 = c.s0[scene]; S_ = S
    for q, (bl, side) in enumerate(blocks):
        sub = f"{scene}_{q}"
        c.s0[sub] = s0 + 4 * q; c.sc_len[sub] = 4
        play_melody(c, sub, bl, 4, "air", key=KL if side == "L" else KS, density=dens, seed=seed + q)
sing("呼び声", [(["R:6", "R:3 5:3", "4:2 3:1 2:2 7,:1", "1:6"], "S")], 0.1, 700)        # アザラシの呼び声（海の節のかけら）
sing("舟歌A", [(L1, "L"), (S1, "S"), (L2, "L"), (S2, "S")] * 2, 0.25, 710)
sing("舟歌B", [(LB, "L"), (SB, "S")] * 4, 0.35, 730)
OK = ["5:6", "4:3 3:3", "1:6", "R:6", "7,:6", "1:3 3:3", "4:6", "R:6",
      "5:3 7:3", "1':6", "7:3 5:3", "R:6", "4:3 3:3", "1:6", "7,:6", "R:6"]           # 沖：海の節だけ。長い音で引かれていく
sing("沖", [(OK[q * 4:(q + 1) * 4], "S") for q in range(4)], 0.15, 750)
sing("舟歌A2", [(L1, "L"), (S1, "S"), (L2, "L"), (S2, "S")], 0.3, 760)
sing("引き潮", [(L1[:3] + ["5:6"], "L"), (["5:6", "R:6", "R:6", "R:6"], "L")], 0.2, 770)   # 陸の節に戻るが、5（ラ）で止まる

# ---------- ビオラとチェロの二重奏（波） ----------
def rt(ch, lo=38):
    r = PC[re.match(r"^([A-G][#b]?)", ch).group(1)]
    return lo + (r - lo) % 12
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    r = rt(ch); tn = [x for x in range(r, r + 26) if x % 12 in chord_pcs(ch)]
    if n == "うねり":       # 低い弦のうねり：はじめから、ゆっくり動く波で（チェロとビオラの長い音は立ち上がりが遅く小さい。1〜2回目は前奏の最初の4秒が -64dB）
        up = [x + 12 for x in tn[:3]]
        VC.bar(b, " ".join(f"{nm(x)}:2{',' if q else ''}" for q, x in enumerate(up if i % 2 == 0 else list(reversed(up)))))
        va = [x for x in range(57, 70) if x % 12 in chord_pcs(ch)]
        VA.at(b * B, f"{nm(va[1])}:3,"); VA.at(b * B + 3, f"{nm(va[0 if i % 2 else 2])}:3,")
        continue
    if n == "引き潮" and i >= 4:   # 5度で止まる：チェロは A と E、ビオラは E を長く
        if i == 4: VC.at(b * B, "A2:12"); VA.at(b * B, "E4:12")
        if i == 6: VC.at(b * B, "E3:9,"); VA.at(b * B, "A3:9,")
        continue
    # チェロ：6つの8分で上がって下がる波。沖では1小節に2つの長い音（ゆっくりした大きな波）
    if n == "沖":
        VC.at(b * B, f"{nm(r)}:3"); VC.at(b * B + 3, f"{nm(tn[1])}:3,")
    else:
        seq = [tn[0], tn[1], tn[2], tn[3], tn[2], tn[1]]
        if n == "呼び声": seq = [x + 12 for x in seq]        # 呼び声は笛が少ないので、チェロの波を1オクターブ上で（低い弦は小さく鳴る）
        VC.bar(b, " ".join(f"{nm(x)}:1{'' if q in (0, 3) else ','}" for q, x in enumerate(seq)))
    # ビオラ：付点4分2つ。旋律が長い音の所で動き、句の終わりの小節は休む（笛に場所をあける）
    vt = [x for x in range(55, 70) if x % 12 in chord_pcs(ch)]
    if n == "呼び声": VA.at(b * B, f"{nm(vt[0])}:6,"); continue
    if i % 4 == 3 and n != "沖": VA.at(b * B, f"{nm(vt[1])}:6,"); continue
    a, z = (vt[0], vt[1]) if (b // 2) % 2 == 0 else (vt[2] if len(vt) > 2 else vt[1], vt[0])
    VA.at(b * B, f"{nm(a)}:3"); VA.at(b * B + 3, f"{nm(z)}:3,")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.3 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の007（第3版）。夕方の浜で、アザラシの民の昔話を思いながら吹く舟歌。陸の節（D イオニア）と海の節（D ドリア）が4小節ずつ交互に来る。6/8・付点4分＝56。伴奏はチェロとビオラの二重奏の波だけ。沖では海の節だけになり、最後は陸の節に戻ろうとして5度（ラ）で止まる。",
       harm_scenes=None, tail_scene="引き潮", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 7.0, "layers": [{"file": "1046", "db": -40, "hp": 100, "lp": 5000, "lfo": [round(4 * 6 * 60 / BPM, 1), 0.3], "wide": 0.012, "duck": 0.4, "fade": 8}],
       "fx": {"far": {"db": -28, "delay": 0.22, "lp": 2800, "rt": 3.0}}}
json.dump(air, open("/tmp/cel/w/air007.json", "w"), ensure_ascii=False)
