# ケルト・フルート100曲「銀の笛と百の夜」015 麦のゆりかご Cradle of Barley — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 子羊を連れ帰った夜。麦畑のそばの農家で、おばあさんが足踏みオルガンを踏みながら、孫に子守歌を歌っている。
#   エイラは戸口で笛を低く合わせる。言葉のない「ルー・ラ・ルー」のくり返しの句で、子どもは眠りにつく。
# 調べ: 眠り。形: 子守歌（3/4。歌の番と、意味のない音のくり返しの句が交互）。3/4・♩=58 → 終わりで 46 までゆるむ。旋法: E♭ イオニア。
# 主役は笛（低め・ささやく。E♭4〜C5 が中心。装飾はごく少し）。
# 伴奏の主役: リードオルガン（足踏みオルガン）の和音。2番からオルガンの足（低い音）。ほかの楽器は使わない（竪琴・ギター・ピアノ・弦・打楽器なし）。
# この曲だけ: オルガンの和音が、ふいごのように強弱で呼吸する（1小節吸って1小節吐く。3番からは2小節ずつの深い呼吸に）。
# 始まり: オルガンの和音だけ → 終わり: 小さく遅く消える（オルガンの息が長くなって止まる）。
# 山: 小さな波（2回目のくり返しの句が少しだけ大きい）。最初が大きく、だんだん小さくなる形にはしない（始まりはオルガン1つ）。
import sys, json, math
from c100_common import *
from c100_v2 import *

S = Song("C100", "015-cradle-of-barley", "麦のゆりかご", "Cradle of Barley", 58, 3, "Eb", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35, "rubato": 0.2})
K = Key("Eb", "major", 4)
VC1 = ["Eb", "Ab", "Eb", "Bb", "Cm", "Ab", "Bb", "Eb"] * 2
RF = ["Eb", "Gm", "Ab", "Eb", "Eb", "Gm", "Ab", "Eb"]
V3 = ["Ab", "Eb", "Fm", "Bb", "Ab", "Eb", "Bb", "Eb", "Ab", "Fm", "Bb", "Eb"]
SC = [("オルガン", 4, "intro", ["Eb", "Ab", "Eb", "Eb"]), ("1番", 16, "verse", VC1), ("ルーラ1", 8, "verse", RF),
      ("2番", 16, "verse", VC1), ("ルーラ2", 8, "chorus", RF), ("3番", 12, "verse", V3), ("ルーラ3", 8, "verse", RF),
      ("消える", 6, "outro", ["Eb", "Ab", "Eb", "Eb", "Eb", "Eb"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("オルガン", 0, 0.6), ("1番", 0, 0.64), ("ルーラ1", 0, 0.68), ("2番", 0, 0.68), ("ルーラ2", 0, 0.74), ("ルーラ2", 7, 0.72),
          ("3番", 0, 0.66), ("ルーラ3", 0, 0.64), ("消える", 0, 0.6), ("消える", 5, 0.52)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="オルガン", passing=True, tension=False)
B = S.beats
# 終わりの2つの場面でゆっくりになる（58 → 46）
st3 = c.s0["ルーラ3"]
S.tempo = [{"bar": 1, "bpm": 58}, {"bar": c.s0["3番"] + 1, "bpm": 55, "ramp": 4}, {"bar": st3 + 1, "bpm": 52, "ramp": 4},
           {"bar": c.s0["消える"] + 1, "bpm": 46, "ramp": 6}]

# ---------- オルガンの呼吸（ふいご） ----------
# 試し書き出し（probe.py）: オルガン1音で笛とほぼ同じ大きさ → 3音の和音は笛より大きくなるので volume 0.06→0.035、足は 0.04
def breath(b):
    n = S.scene_of(b)[0]; i = S.scene_of(b)[1]
    if n in ("3番", "ルーラ3", "消える"):
        return [0.8, 1.05, 1.3, 1.05][i % 4]          # 深くゆっくり（2小節吸って2小節吐く）
    return [1.25, 0.82][i % 2]                       # 1小節吸って、1小節吐く
G = c.g()
ORG = [S.track(f"足踏みオルガン{j + 1}", "pad", patch="reedOrgan", volume=0.035, pan=-0.2 + 0.2 * j, reverb=0.5,
               barGain=[round(G[b] * breath(b), 3) for b in range(c.NB)]) for j in range(3)]
PED = S.track("オルガンの足（低い音）", "pad", patch="reedOrgan", volume=0.04, pan=0.0, reverb=0.45,
              barGain=[round(G[b] * breath(b), 3) for b in range(c.NB)])

def triad(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    pcs = [r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12]
    out = []
    for p in pcs:
        x = 55 + (p - 55) % 12                       # G3〜F#4 のあいだに（温かい真ん中の高さ）
        out.append(x)
    return sorted(out), 36 + (r - 36) % 12          # 和音・足の音（C2〜B2）

for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    tones, root = triad(ch)
    if n == "消える" and i >= 4:                      # 最後の2小節：1回だけ長く吸って、止まる
        if i == 4:
            for j, t in enumerate(tones): ORG[j].at(b * B, f"{nm(t)}:6,")
            PED.at(b * B, f"{nm(root)}:6,")
        continue
    for j, t in enumerate(tones):
        ORG[j].at(round(b * B + 0.03 * j, 3), f"{nm(t)}:{B}")
    if n not in ("オルガン", "1番", "ルーラ1"):
        PED.at(b * B, f"{nm(root)}:{B}")

# ---------- 笛（低め・ささやく） ----------
VA = ["3:2 2:1", "1:2 2:1", "3:1 4:1 5:1", "3:3", "6:2 5:1", "4:2 3:1", "2:1 3:1 2:1", "6,:3",
      "3:2 2:1", "1:2 3:1", "5:1 6:1 5:1", "4:3", "3:1 2:1 1:1", "2:2 3:1", "2:1 1:1 7,:1", "1:3"]
VB = VA[:8] + ["5:2 6:1", "1':2 7:1", "6:1 5:1 4:1", "5:3", "3:1 2:1 1:1", "2:2 3:1", "2:1 1:1 7,:1", "1:3"]
RA = ["5:1 3:1 5:1", "6:2 5:1", "5:1 3:1 5:1", "2:3", "5:1 3:1 5:1", "6:2 1':1", "7:1 6:1 5:1", "1:3"]   # ルー・ラ・ルー
RB = ["5:1 3:1 5:1", "6:2 5:1", "5:1 3:1 5:1", "2:3", "5:1 3:1 5:1", "6:1 5:1 3:1", "2:1 3:1 2:1", "1:3"]
V3M = ["3:2 2:1", "1:3", "6,:2 7,:1", "1:3", "4:2 3:1", "2:3", "3:1 2:1 1:1", "6,:3", "2:2 3:1", "2:1 1:1 7,:1", "1:3", "1:3"]
END = ["5:1 3:1 5:1", "6:2 5:1", "3:3", "1:3", "1:3", "R:3"]
for n, mel, d in (("1番", VA, 0.15), ("ルーラ1", RA, 0.1), ("2番", VB, 0.25), ("ルーラ2", RB, 0.2), ("3番", V3M, 0.15),
                  ("ルーラ3", RA, 0.1), ("消える", END, 0.0)):
    play_melody(c, n, mel, 4, "air", key=K, density=d, seed=1500 + len(n) * 7)

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.3 --master -15 --widen 1.1 --side-hpf 200",
       "ケルト・フルート100曲の015（第3版）。子羊を連れ帰った夜、麦畑のそばの農家の子守歌。足踏みオルガンの和音がふいごのように強弱で呼吸し、エイラの笛が低くささやくように歌う。3/4・♩=58 → 46、E♭ イオニア。歌の番と、言葉のない「ルー・ラ・ルー」のくり返しの句が交互に来て、最後はオルガンの息が長くなって止まる。",
       harm_scenes=None, tail_scene="消える", double=False, fill=False, pads=False)
air = {"pre": 0.4, "tail": 6.0, "layers": [{"file": "0595", "db": -46, "hp": 180, "lp": 3600, "wide": 0.012, "duck": 0.4, "fade": 8}],
       "fx": {"far": {"db": -28, "delay": 0.3, "lp": 2800, "rt": 3.6}}}
json.dump(air, open("/tmp/cel/w/air015.json", "w"), ensure_ascii=False)
