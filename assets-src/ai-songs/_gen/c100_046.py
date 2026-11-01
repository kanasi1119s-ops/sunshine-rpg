# ケルト・フルート100曲「銀の笛と百の夜」046 朽ちた礼拝堂 The Ruined Chapel — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 塔のふもとに、屋根の落ちた古い礼拝堂がある。祖父の日記には「鐘の秘密の入口は、祈りの歌の中にある」と書いてあった。
#   エイラが朽ちた祭壇の前で笛を吹くと、壁にしみこんだ昔の聖歌隊の声（弦の4声）がよみがえる。はじめは狭い部屋に寄りそう声、
#   歌うたびに声が広がり、最後は落ちた屋根から見える空へ、4オクターブに開いていく。
# 調べ: 悲しみ。形: 讃美歌のような4声（ウェールズの聖歌の形。16小節の歌を3節）の上で、笛が長い息の句を歌う。
# 拍子・速さ: 4/4・♩=50。旋法: F イオニア。
# 主役は笛（長い息の句）。伴奏の主役: 弦の4声のコラール（バイオリン・ビオラ・チェロ・コントラバス。2分音符で）。
#   竪琴・ギター・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 和音の並べ方が「狭い → 広い」へ（1節は1オクターブの中に4声、2節は2オクターブ、3節は4オクターブに開く）。
# 始まり: 弦の合唱（4声だけ）→ 終わり: 空（高い弦と笛だけが残る）。
# 山: 終盤に1つ（3節）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "046-the-ruined-chapel", "朽ちた礼拝堂", "The Ruined Chapel", 50, 4, "F", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3, "rubato": 0.2})
K = Key("F", "major", 4)
HC = ["F", "C", "Dm", "Bb", "F", "C", "F", "F", "Bb", "F", "Gm", "C", "F", "Dm", "Gm", "C",
      "F", "Am", "Bb", "F", "Gm", "F", "C", "C", "Dm", "Bb", "F", "C", "Bb", "C", "F", "F"]        # 2分音符ごとの和音（16小節）
SC = [("聖歌隊", 4, "intro", ["F", "Bb", "C", "F"]), ("1節", 16, "verse", HC[::2]), ("2節", 16, "verse", HC[::2]), ("3節", 16, "chorus", HC[::2]),
      ("空", 4, "outro", ["F"] * 4)]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("聖歌隊", 0, 0.66), ("1節", 0, 0.68), ("2節", 0, 0.74), ("3節", 0, 0.82), ("3節", 12, 0.9), ("空", 0, 0.74), ("空", 3, 0.66)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="聖歌隊", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 1回目（7.69）: 弦だけの聖歌隊（約19秒）が本編より約12dB 小さかった → 始まりの4小節だけ強く。
# 試し書き出し: バイオリン（0.03・gainDb 4）は笛より約4dB 小さい。ビオラとチェロは2声で笛より約4dB 大きい → 0.013。コントラバスは約8dB 小さい → 0.04
V = {
    "S": [S.track(f"バイオリン（ソプラノ{j + 1}）", "strings", patch="violin", volume=0.03, gainDb=4, pan=0.3, reverb=0.7, release=0.5, barGain=[round(x * (2.0 if b < 4 else 1.4), 3) for b, x in enumerate(G)]) for j in range(2)],
    "A": [S.track(f"ビオラ（アルト{j + 1}）", "strings", patch="viola", volume=0.013, gainDb=1, pan=0.1, reverb=0.7, release=0.5, barGain=[round(x * (2.0 if b < 4 else 1.4), 3) for b, x in enumerate(G)]) for j in range(2)],
    "T": [S.track(f"チェロ（テノール{j + 1}）", "strings", patch="cello", volume=0.013, gainDb=2, pan=-0.1, reverb=0.7, release=0.5, barGain=[round(x * (2.0 if b < 4 else 1.4), 3) for b, x in enumerate(G)]) for j in range(2)],
    "B": [S.track(f"コントラバス（バス{j + 1}）", "strings", patch="contrabass", volume=0.04, pan=-0.3, reverb=0.7, release=0.6, barGain=[round(x * (1.8 if b < 4 else 1.2), 3) for b, x in enumerate(G)]) for j in range(2)],
}

# ---------- 4声のコラール（狭い → 広い） ----------
def chord_pcs(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, [(r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12]
RANGE = {"聖歌隊": (53, 0), "1節": (53, 0), "2節": (41, 1), "3節": (29, 2)}      # バスの下限と、声のあいだを何オクターブ広げるか
def near(pc, lo):
    return lo + (pc - lo) % 12
for sc in ("聖歌隊", "1節", "2節", "3節"):
    s0 = c.s0[sc]; lo, spread = RANGE[sc]
    seq = (["F", "Bb", "C", "F", "F", "Dm", "C", "F"] if sc == "聖歌隊" else HC)
    for q, ch in enumerate(seq):
        t = s0 * B + q * 2
        r, (th, fi) = chord_pcs(ch)
        bass = near(r, lo if spread else 41)
        tenor = near(fi, bass + 1 + 12 * (spread >= 2))
        alto = near(th, tenor + 1 + 12 * (spread >= 1))
        sop = near(r, alto + 1 + 12 * (spread >= 2))
        if spread == 0:                                           # 1節：1オクターブの中に寄りそう（A3〜A4 あたり）
            bass, tenor, alto, sop = sorted([near(r, 53), near(th, 53), near(fi, 53), near(r, 53) + 12])
        for v, m in (("B", bass), ("T", tenor), ("A", alto), ("S", sop)):
            V[v][q % 2].at(round(t + 0.02 * "BTAS".index(v), 3), f"{nm(m)}:2{',' if q % 2 else ''}")

# ---------- 笛（長い息の句。F イオニア。1=F4） ----------
M = ["5:2 6:2", "5:2 3:2", "4:2 6:2", "5:4", "1':2 7:2", "6:2 5:2", "4:2 2:2", "3:4",
     "4:2 3:2", "2:2 5:2", "6:2 7:2", "1':4", "6:2 5:2", "4:2 3:2", "2:2 1:1 2:1", "1:4"]
play_melody(c, "1節", M, 4, "air", key=K, density=0.15, seed=4601)
play_melody(c, "2節", M, 4, "air", key=K, density=0.25, seed=4602)
play_melody(c, "3節", M[:12] + ["1':2 2':2", "3':4", "2':2 1':1 7:1", "1':4"], 4, "air", key=K, density=0.25, seed=4603)
play_melody(c, "空", ["5:4", "6:4", "3':4", "R:4"], 4, "air", key=K, density=0.0)
# 空：高い弦（バイオリンの F5 と A5）だけが残る
s0 = c.s0["空"]
V["S"][0].at(s0 * B, "F5:14"); V["S"][1].at(round(s0 * B + 0.1, 3), "A5:13.9,"); V["A"][0].at(s0 * B, "C5:12,")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.38 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の046（第3版）。屋根の落ちた古い礼拝堂。ウェールズの聖歌のような弦の4声のコラール（4/4・♩=50、F イオニア）の上で、笛が長い息の句を歌う。1節は1オクターブの中に寄りそう狭い和音、2節は2オクターブ、3節は4オクターブに開き、最後は落ちた屋根から見える空のように、高い弦と笛だけが残る。",
       harm_scenes=None, tail_scene="空", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 160, "lp": 3600, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -26, "delay": 0.34, "lp": 2800, "rt": 4.4}}}
json.dump(air, open("/tmp/cel/w/air046.json", "w"), ensure_ascii=False)
