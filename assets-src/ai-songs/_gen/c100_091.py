# ケルト・フルート100曲「銀の笛と百の夜」091 下山 Down the Mountain — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 第10章のはじまり。頂で祖父の思いを受け取ったエイラは、鐘のある故郷の島へ帰るため、山を下りる。
#   来た道とはちがい、帰りの足どりは軽い。下り坂では足が勝手に前へ出て、句がひと足早く次へ転がりこんでいく。
# 調べ: 喜び。形: バーンダンス（はずむ8分。AABB×3）。
# 拍子・速さ: 4/4・♩=88。旋法: G イオニア。
# 主役は笛（軽い足どり）。伴奏の主役: ナイロン弦ギター（1・3拍目の低音と2・4拍目の和音）とコントラバス。打楽器は足拍子（枠太鼓）。
#   竪琴・ピアノ・パッド・弓の弦・2本目の笛は使わない。
# この曲だけ: 下り坂で、句が1拍早く次へ転がりこむ（4小節ごとの句の頭の音が、前の小節の4拍目に食いこむ）。
# 始まり: 足拍子 → 終わり: 足拍子。
# 山: 中盤（2周目）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "091-down-the-mountain", "下山", "Down the Mountain", 88, 4, "G", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35})
K = Key("G", "major", 4)
CA = ["G", "C", "G", "D", "G", "D", "D", "G"]; CB = ["D", "D", "C", "G", "G", "D", "C", "G"]
T = CA * 2 + CB * 2
SC = [("足拍子", 2, "intro", ["G", "G"]), ("下り1", 32, "verse", T), ("下り2", 32, "chorus", T), ("下り3", 32, "verse", T), ("足拍子だけ", 2, "outro", ["G", "G"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("足拍子", 0, 0.8), ("下り1", 0, 0.76), ("下り2", 0, 0.86), ("下り2", 31, 0.92), ("下り3", 0, 0.8), ("足拍子だけ", 0, 0.78)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="足拍子", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
GT = [S.track(f"ギター{i + 1}", "guitar", patch="nylonGuitar", volume=0.008, pan=-0.3 - 0.05 * i, reverb=0.3, barGain=G) for i in range(5)]
CB_ = S.track("コントラバス", "strings", patch="contrabass", volume=0.03, gainDb=3, pan=-0.1, reverb=0.3, release=0.25, barGain=G)
FT = [S.track(f"足拍子{j + 1}", "guitar", patch="frameDrum", volume=0.35, gainDb=18, pan=0.05 + 0.1 * j, reverb=0.25,
              barGain=[round(x * (1.6 if S.scene_of(b)[0].startswith("足拍子") else 1.0), 3) for b, x in enumerate(G)]) for j in range(2)]

# ---------- バーンダンス（8分＝0.5。1=G4） ----------
A = ["1:0.5 2:0.5 3:0.5 5:0.5 6:1 5:1", "4:0.5 3:0.5 2:0.5 1:0.5 2:2", "3:0.5 5:0.5 1':0.5 5:0.5 6:1 5:1", "4:0.5 2:0.5 7,:0.5 2:0.5 1:2",
     "1:0.5 2:0.5 3:0.5 5:0.5 6:1 1':1", "7:0.5 6:0.5 5:0.5 4:0.5 3:2", "2:0.5 3:0.5 4:0.5 2:0.5 7,:1 2:1", "1:2 1:2"]
Bm = ["5:0.5 6:0.5 7:0.5 1':0.5 2':1 1':1", "7:0.5 6:0.5 5:0.5 6:0.5 7:2", "1':0.5 7:0.5 6:0.5 5:0.5 4:1 6:1", "5:0.5 4:0.5 3:0.5 2:0.5 3:2",
      "5:0.5 6:0.5 7:0.5 1':0.5 2':1 3':1", "2':0.5 1':0.5 7:0.5 6:0.5 5:2", "4:0.5 3:0.5 2:0.5 4:0.5 3:1 2:1", "1:2 1:2"]
for k in range(3):
    sc = f"下り{k + 1}"; s0 = c.s0[sc]; ev = []
    for j, s_ in enumerate(A + A + Bm + Bm): ev += mel_events(K, s_, 4, (s0 + j) * B)
    ev = [[round(t, 4), L, m] for t, L, m in ev]
    # 句が1拍早く転がりこむ：4小節ごとの句の頭の音を1拍前へ（前の音は短く）
    for q in range(1, 8):
        t0 = (s0 + 4 * q) * B
        for i, e in enumerate(ev):
            if abs(e[0] - t0) < 1e-6 and i > 0:
                prev = ev[i - 1]
                if prev[0] + 0.5 <= t0 - 1:
                    prev[1] = round(min(prev[1], t0 - 1 - prev[0]), 4)
                    e[0] = round(t0 - 1, 4); e[1] = round(e[1] + 1, 4)
                break
    play(c.FLUTE, ornament(ev, K, 88, "hornpipe", B, density=(0.35, 0.5, 0.4)[k], seed=9100 + k))

# ---------- ギター・コントラバス・足拍子 ----------
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12
BOOM = [(1, 0.6, "d", "!"), (1.5, 0.4, "u", ","), (3, 0.6, "d", ""), (3.5, 0.4, "u", ",")]
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r, th, fi = tri(ch)
    f = FT[b % 2]
    if n.startswith("足拍子"):
        f.bar(b, "C3:1! R:1 C3:1! R:1"); continue
    lo = near(r, 40)
    strum(GT, b, B, ch, BOOM)
    CB_.bar(b, f"{nm(lo)}:0.6! R:1.4 {nm(lo + 7 if lo + 7 <= 50 else lo - 5)}:0.6 R:1.4")
    f.bar(b, "C3:0.5! E3:0.5, C3:0.5 E3:0.5, C3:0.5! E3:0.5, C3:0.5 E3:0.5," if n == "下り2" else "C3:1! E3:0.5, E3:0.5, C3:1 E3:1,")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.22 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の091（第3版）。第10章のはじまり、故郷へ帰るために山を下りる。バーンダンス（4/4・♩=88、はずむ8分）、G の長調。足拍子で始まり、ナイロン弦ギターの低音と和音、コントラバス、足拍子に乗って、笛が軽い足どりで AABB を3回。下り坂なので、4小節ごとの句の頭の音が1拍早く、前の小節に食いこんで転がりこむ。山は2周目。最後は足拍子だけ。",
       harm_scenes=None, tail_scene="足拍子だけ", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 3.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -30, "delay": 0.15, "lp": 3000, "rt": 1.8}}}
json.dump(air, open("/tmp/cel/w/air091.json", "w"), ensure_ascii=False)
