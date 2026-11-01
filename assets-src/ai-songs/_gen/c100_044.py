# ケルト・フルート100曲「銀の笛と百の夜」044 若き日の祖父 Grandfather in His Youth — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 鐘守が語る、若い日の祖父。村いちばんの笛吹きで、夜通しの踊りでは、フィドル弾きの友と競うように速いリールを吹いた。
#   エイラの笛は、話の中の若い祖父になって走る。最後の8小節、同じ旋律が半分の速さになる。今の、年をとった祖父の笛。
# 調べ: 喜び。形: リール AABB を3周 → 最後に同じ旋律の A を半分の速さで。
# 拍子・速さ: 4/4・♩=104（最後の場面は音の長さを倍にして、半分の速さに聞かせる）。旋法: E ドリア。
# 主役は笛（若く走る笛）。伴奏の主役: フィドル（ドニゴール式の強い弓。旋律を一緒に弾き、長い音に3連の弓の飾り）とナイロン弦ギター。打楽器なし。
#   竪琴・ピアノ・弦の和音・パッド・2本目の笛は使わない。
# この曲だけ: 最後の8小節分の旋律で、同じ A が半分の速さになる（今の祖父）。フィドルとギターは止まり、笛ひとりで。
# 始まり: いきなりギターとフィドル（笛は A の2回目から）→ 終わり: 半分の速さの同じ旋律。
# 山: 中盤（2周目）。
import sys, json, re
from c100_common import *
from c100_v2 import *
import c100_v2 as _v2
_oc = _v2.open_chord
_v2.open_chord = lambda ch, lo=52, hi=76: _oc(ch, lo, hi)

S = Song("C100", "044-grandfather-in-his-youth", "若き日の祖父", "Grandfather in His Youth", 104, 4, "E", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
K = Key("E", "dorian", 4)
CA = ["Em", "D", "Em", "Bm", "Em", "D", "A", "Em"]
CB = ["Em", "A", "Em", "Bm", "Em", "D", "A", "Em"]
AB = CA + CA + CB + CB
SC = [("1周目", 32, "verse", AB), ("2周目", 32, "chorus", AB), ("3周目", 32, "verse", AB), ("今の祖父", 16, "outro", [x for x in CA for _ in (0, 1)])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("1周目", 0, 0.8), ("1周目", 31, 0.82), ("2周目", 0, 0.86), ("2周目", 24, 0.92), ("3周目", 0, 0.82), ("3周目", 31, 0.8), ("今の祖父", 0, 0.66), ("今の祖父", 15, 0.6)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="1周目", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 試し書き出し: フィドル（0.1）は笛より約8dB 大きい → 0.04。ギター1本（0.016）も笛より大きい（5本重なる）→ 0.008
FD = S.track("フィドル（ドニゴール式）", "strings", patch="violin", volume=0.04, gainDb=0, pan=0.3, reverb=0.35, barGain=G)
GT = [S.track(f"ギター{i + 1}", "guitar", patch="nylonGuitar", volume=0.008, pan=-0.3 - 0.05 * i, reverb=0.3, barGain=G) for i in range(5)]

# ---------- リール（E ドリア。1=E4。ドニゴール風に、同じ低い音を何度も弾き返す） ----------
A = ["1:0.5 1:0.5 5:0.5 1:0.5 6:0.5 1:0.5 5:0.5 4:0.5", "3:0.5 4:0.5 5:0.5 3:0.5 2:0.5 7,:0.5 5,:0.5 7,:0.5",
     "1:0.5 1:0.5 5:0.5 1:0.5 6:0.5 1:0.5 5:0.5 1':0.5", "7:0.5 5:0.5 6:0.5 4:0.5 5:1 3:0.5 2:0.5",
     "1:0.5 1:0.5 5:0.5 1:0.5 6:0.5 1:0.5 5:0.5 4:0.5", "3:0.5 4:0.5 5:0.5 6:0.5 7:0.5 1':0.5 2':0.5 7:0.5",
     "1':0.5 6:0.5 5:0.5 3:0.5 4:0.5 2:0.5 7,:0.5 2:0.5", "1:1 5,:0.5 7,:0.5 1:1 R:1"]
Bm = ["5:0.5 1':0.5 1':0.5 7:0.5 1':0.5 5:0.5 1':0.5 7:0.5", "6:0.5 2':0.5 2':0.5 1':0.5 2':0.5 6:0.5 4:0.5 6:0.5",
      "5:0.5 1':0.5 1':0.5 7:0.5 1':0.5 2':0.5 3':0.5 1':0.5", "7:0.5 5:0.5 6:0.5 4:0.5 5:1 R:1",
      "5:0.5 1':0.5 1':0.5 7:0.5 1':0.5 5:0.5 3:0.5 5:0.5", "6:0.5 4:0.5 2:0.5 4:0.5 6:0.5 1':0.5 7:0.5 6:0.5",
      "5:0.5 3:0.5 4:0.5 2:0.5 3:0.5 1:0.5 7,:0.5 2:0.5", "1:1 5,:0.5 7,:0.5 1:1 R:1"]
TUNE = A + A + Bm + Bm
s0 = c.s0["1周目"]
# 1周目：最初の A はフィドルだけ（いきなり）。笛は A の2回目から
nb = play_melody(c, "1周目", ["R:4"] * 8 + TUNE[8:], 4, "reel", key=K, density=0.35, seed=4401)
play_melody(c, "2周目", TUNE, 4, "reel", key=K, density=0.55, seed=4402)
play_melody(c, "3周目", TUNE, 4, "reel", key=K, density=0.45, seed=4403)
# 今の祖父：A を半分の速さで（音の長さを倍に）。笛ひとり、飾りはごく少し
SLOW = []
for s_ in A:
    for half in (0, 1):
        tk = s_.split(); acc, out = 0.0, []
        for t in tk:
            n, L = t.split(":"); L = float(L) * 2
            if half == 0 and acc + L <= 4.0001: out.append(f"{n}:{L:g}")
            elif half == 1 and acc >= 3.9999: out.append(f"{n}:{L:g}")
            elif half == 0 and acc < 4 < acc + L: out.append(f"{n}:{4 - acc:g}")
            elif half == 1 and acc < 4 < acc + L: out.append(f"{n}:{acc + L - 4:g}")
            acc += L
        SLOW.append(" ".join(out))
play_melody(c, "今の祖父", SLOW, 4, "air", key=K, density=0.1, seed=4404)

# ---------- フィドル：旋律を一緒に（1オクターブ下で少し小さく）、長い音に3連の弓の飾り ----------
for sc in ("1周目", "2周目", "3周目"):
    ev = section_events(c, sc, TUNE, 4, key=K)
    out = []
    for t, L, m in ev:
        mm = m - 12 if m >= 71 else m
        if L >= 1 - 1e-6:                                       # 3連の弓（その音・上・その音）
            up = mm + 2
            out += [(round(t, 4), 1 / 3, mm, "!"), (round(t + 1 / 3, 4), 1 / 3, up, ","), (round(t + 2 / 3, 4), round(L - 2 / 3, 4), mm, "")]
        else:
            out.append((round(t, 4), L, mm, "!" if abs(t % 2) < 1e-6 else ","))
    play(FD, out)
# ---------- ギター（リールのストローク。今の祖父では止まる） ----------
REEL = [(0, 1, "d", "!"), (1, 0.5, "d", ","), (1.5, 0.5, "u", ","), (2, 1, "d", ""), (3, 0.5, "d", ","), (3.5, 0.5, "u", ",")]
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]
    if n == "今の祖父":
        if i == 0: strum(GT, b, B, ch, [(0, 4, "d", ",")])
        continue
    strum(GT, b, B, ch, REEL)

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.22 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の044（第3版）。鐘守が語る、若い日の祖父。リール（4/4・♩=104）AABB を3周、E ドリア。いきなりギターとドニゴール式のフィドルで始まり、笛（若い祖父）は A の2回目から走りだす。フィドルは旋律を一緒に弾き、長い音に3連の弓の飾り。山は2周目。最後の場面で、同じ A が半分の速さになり、笛ひとりで吹く（今の、年をとった祖父）。",
       harm_scenes=None, tail_scene="今の祖父", double=False, fill=False, pads=False)
air = {"pre": 0.1, "tail": 5.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -29, "delay": 0.2, "lp": 3000, "rt": 2.6}}}
json.dump(air, open("/tmp/cel/w/air044.json", "w"), ensure_ascii=False)
