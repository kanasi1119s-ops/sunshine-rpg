# ケルト・フルート100曲「銀の笛と百の夜」012 羊飼いの朝 Shepherd's Morning — 第3版（2026-10-30 作り直し。docs/sound/celtic-study/E-100-plan.md）
# 物語: 草原の夏の放牧小屋。夜明けに、エイラの笛が丘の向こうへ呼びかける。羊飼いたちが、フィドルと手拍子でいつもの短い句を返す。
#   呼べば答える。答えが返るたびに人が増え、やりとりはだんだん速くなり、最後は祭りのようになって、全員でぴたりと止まる。
#   （「笛が人に届く」章の、はじめて人が答えてくれる曲）
# 調べ: 喜び。形: 呼びかけと応答がだんだん速くなる（夏の放牧小屋の歌）。4/4・♩=92 → 120。A イオニアの5音（A・B・C♯・E・F♯）。
# 主役は笛（呼びかけ。毎回ちがう節）。伴奏の主役: フィドルの応答（いつも同じ短い句）と手拍子・木の打音（打）。
#   放牧から2本目のフィドル（1オクターブ下）と、呼びかけの下でフィドルの重音（A と E の長い音）。竪琴・ギター・ピアノ・パッド・低弦は使わない。
# この曲だけ: 応答はいつも同じ短い句。速くなるほど、その句の装飾だけが増えていく。最後は呼びかけと応答が1小節ずつになり、追いかけあう。
# 始まり: 笛ひとりの呼びかけ → 終わり: 加速の頂点で全員が1拍鳴らして止まる。
# 山: だんだん速く・だんだん大きく（最後が頂点）。
# 試しの書き出し（probe.py。笛と並べて）: バイオリンは立ち上がりが遅く笛より約8dB小さい → volume 0.16・gainDb 4。
#   手拍子（seasonFx の B4）は打つ所だけで笛より約8dB小さい（打楽器として丁度よい）。木の打音（surgeWoody）は笛より大きいので volume 0.07。
import sys, json
from c100_common import *
from c100_v2 import *

S = Song("C100", "012-shepherds-morning", "羊飼いの朝", "Shepherd's Morning", 92, 4, "A", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
K = Key("A", "major", 4)
CALL_C = ["A", "E", "D", "A"]
P1, P2, P3 = 8, 12, 20          # 夜明け（3小節×8）・放牧（3小節×12）・祭り（2小節×20）
S.scene("夜明け", P1 * 3, "verse", (["A", "D", "E"] * P1))
S.scene("放牧", P2 * 3, "verse", (["A", "D", "E"] * P2))
S.scene("祭り", P3 * 2, "chorus", (["A", "E"] * P3))
S.scene("止まる", 1, "outro", ["A"])
NAMES = ["夜明け", "放牧", "祭り", "止まる"]
n1, n2 = P1 * 3, P2 * 3
S.tempo = [{"bar": 1, "bpm": 92}, {"bar": 1 + n1, "bpm": 100, "ramp": n1}, {"bar": 1 + n1 + n2, "bpm": 110, "ramp": n2},
           {"bar": 1 + n1 + n2 + P3 * 2, "bpm": 120, "ramp": P3 * 2}]
c = make(S, NAMES,
         [("夜明け", 0, 0.66), ("夜明け", n1 - 1, 0.72), ("放牧", 0, 0.74), ("放牧", n2 - 1, 0.82), ("祭り", 0, 0.84), ("祭り", P3 * 2 - 1, 0.95), ("止まる", 0, 0.95)],
         {}, flute_gain={n: 1.1 for n in NAMES}, intro="夜明け", passing=True, tension=False)
B = S.beats
FD = S.track("フィドル（応答）", "strings", patch="violin", volume=0.16, gainDb=4, pan=0.3, reverb=0.4, barGain=c.g())
FD2 = S.track("2本目のフィドル（1オクターブ下）", "strings", patch="violin", volume=0.13, gainDb=4, pan=0.45, reverb=0.45, barGain=c.g())
DRN = [S.track(f"フィドルの重音{j + 1}", "strings", patch="violin", volume=0.08, pan=-0.3 + 0.1 * j, reverb=0.5, barGain=c.g()) for j in range(2)]
CL = S.track("手拍子", "pad", patch="seasonFx", volume=0.15, pan=-0.25, reverb=0.3, barGain=c.g())
WD = S.track("木の打音", "guitar", patch="surgeWoody", volume=0.07, pan=0.12, reverb=0.3, barGain=c.g())

# ---------- 呼びかけ（笛。毎回ちがう節）と応答（フィドル。いつも同じ句） ----------
M = [["1:1 2:0.5 3:0.5 5:2", "6:1 5:1 3:2"], ["5:1 6:0.5 5:0.5 3:1 2:1", "1:2 R:2"], ["3:0.5 5:0.5 6:1 1':2", "6:1 5:1 6:2"],
     ["1':1 6:1 5:1 3:1", "2:1 3:1 5:2"], ["6,:1 1:1 2:1 3:1", "5:3 R:1"], ["5:0.5 6:0.5 1':1 2':1 1':1", "6:2 5:2"],
     ["3:1 2:0.5 1:0.5 6,:1 1:1", "2:3 R:1"], ["1':1.5 6:0.5 5:1 6:1", "1':3 R:1"]]
RESP = "1':0.5 6:0.5 5:1 3:0.5 2:0.5 1:1"
def sub(name, start, n):
    c.s0[name] = start; c.sc_len[name] = n
u = 0
for ph, units, ln in (("夜明け", P1, 3), ("放牧", P2, 3), ("祭り", P3, 2)):
    for k in range(units):
        b0 = c.s0[ph] + k * ln
        mot = M[u % 8]
        call = mot if ln == 3 else [mot[0]]
        sub(f"呼{u}", b0, len(call)); sub(f"答{u}", b0 + len(call), 1)
        play_melody(c, f"呼{u}", call, 4 if not (ph == "放牧" and k % 3 == 2) else 5 if all("'" not in x for x in call) else 4,
                    "march", key=K, density=0.3 + 0.4 * u / 40, seed=1200 + u)
        dens = min(1.0, 0.05 + u / 40)             # 速くなるほど、応答の装飾だけが増える
        play_melody(c, f"答{u}", [RESP], 4, "march", key=K, density=dens, seed=1300 + u, track=FD)
        if ph != "夜明け":
            play_melody(c, f"答{u}", [RESP], 3, "march", key=K, density=dens * 0.6, seed=1400 + u, track=FD2)
        rb = b0 + len(call)
        # 手拍子：夜明けの4つ目の応答から、応答の2・4拍目。放牧から呼びかけの裏にも。祭りは8分で
        if ph == "夜明け" and k >= 3: CL.bar(rb, "R:1 B4:1 R:1 B4:1")
        if ph == "放牧":
            CL.bar(rb, "R:1 B4:1 R:1 B4:1")
            for j in range(len(call)): CL.bar(b0 + j, "R:0.5 B4:0.5, R:1 R:0.5 B4:0.5, R:1")
            WD.bar(rb, "A4:1 R:1 A4:1 R:1")
        if ph == "祭り":
            for j in range(2): CL.bar(b0 + j, " ".join(["B4:0.5, B4:0.5"] * 4)); WD.bar(b0 + j, "A4:1! R:1 E4:1 R:1")
        # 放牧と祭り：呼びかけの下でフィドルの重音（A と E）
        if ph != "夜明け":
            for j in range(len(call)):
                DRN[0].at((b0 + j) * B, "A3:4,"); DRN[1].at((b0 + j) * B, "E4:4,")
        u += 1
# 止まる：加速の頂点で、全員が1拍
sb = c.s0["止まる"]
c.FLUTE.at(sb * B, "A5:1!"); FD.at(sb * B, "A5:1!"); FD2.at(sb * B, "A4:1!"); CL.at(sb * B, "B4:1"); WD.at(sb * B, "A4:1!")
DRN[0].at(sb * B, "A3:1"); DRN[1].at(sb * B, "E4:1")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.24 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の012（第3版）。草原の夏の放牧小屋の朝。エイラの笛が呼びかけ、羊飼いたちがフィドルと手拍子でいつもの短い句を返す。呼びかけは毎回ちがい、応答はいつも同じ句で、速くなるほど装飾だけが増える。4/4・♩=92 → 120、A の5音。最後は呼びかけと応答が1小節ずつになり、加速の頂点で全員が1拍鳴らして止まる。",
       harm_scenes=None, tail_scene="止まる", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 4.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -29, "delay": 0.24, "lp": 3000, "rt": 2.6}}}
json.dump(air, open("/tmp/cel/w/air012.json", "w"), ensure_ascii=False)
