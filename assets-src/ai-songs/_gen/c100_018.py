# ケルト・フルート100曲「銀の笛と百の夜」018 干し草の匂い Scent of Hay — 第2版（2026-10-28）
# イメージ: 昼下がりの納屋。干し草の上でうとうとする。外では鳥。笛とギターが、のんびり世間話をするように。
#   ときどき低いチェロが「うん、うん」と眠そうにあいづちを打つ。だんだんまぶたが重くなり、テンポがゆるんで眠りに近づいていく。
# 形（台帳）: 2つの楽器のデュエット（笛とギター）。6/8・付点4分＝40（のんびり）。G ミクソリディア。始め：鳥／終わり：眠気（テンポがゆるむ）。山なし。
# 編曲の表:
#   鳥      : 鳥の声→ギターの最初の和音
#   のんびり1: 笛とギター（低音の歩み＋指弾きの分散和音）だけ
#   のんびり2: ＋チェロの眠そうなあいづち（フレーズの終わりに2音）
#   のんびり3: 笛が少し高い所で、ギターは低音を休みがちに
#   昼寝    : 笛の音が長くなる（同じ節を倍の長さで）。ギターは付点4分の和音だけ
#   夢うつつ: 笛のかけら。テンポがゆるんで止まる
import sys
from c100_common import *
from c100_v2 import *

BPM = 120   # 8分音符＝120（付点4分＝40）
S = Song("C100", "018-scent-of-hay", "干し草の匂い", "Scent of Hay", BPM, 6, "G", "mixolydian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.45, "rubato": 0.3, "rit": {"bar": 3 + 16 * 3 + 16 + 6, "bars": 6, "to": 0.7, "aTempo": False}})
AC = ["G", "F", "C", "G", "Em", "F", "C", "G"]
BC = ["C", "G", "F", "G", "C", "Am", "F", "G"]
S.scene("鳥", 3, "intro", ["G", "G", "G"])
S.scene("のんびり1", 16, "verse", AC + BC)
S.scene("のんびり2", 16, "verse", AC + BC)
S.scene("のんびり3", 16, "verse", BC + AC)
S.scene("昼寝", 16, "verse", ["G", "G", "F", "F", "C", "C", "G", "G", "C", "C", "F", "F", "G", "G", "G", "G"])
S.scene("夢うつつ", 12, "outro", ["G", "F", "G", "G", "C", "G", "C", "G", "F", "G", "G", "G"])
NAMES = ["鳥", "のんびり1", "のんびり2", "のんびり3", "昼寝", "夢うつつ"]

c = make(S, NAMES,
         [("鳥", 0, 0.6), ("のんびり1", 0, 0.64), ("のんびり2", 0, 0.66), ("のんびり3", 0, 0.68), ("昼寝", 0, 0.62), ("夢うつつ", 0, 0.56), ("夢うつつ", 11, 0.32)],
         {}, flute_gain={n: 1.2 for n in NAMES}, intro="鳥", passing=True, tension=False)
GB = S.track("ギター（低音の歩み）", "guitar", patch="nylonGuitar", volume=0.1, pan=0.25, reverb=0.35, barGain=c.g())
GA = S.track("ギター（指弾き）", "guitar", patch="nylonGuitar", volume=0.085, pan=0.35, reverb=0.35, barGain=c.g())
CELLO = S.track("チェロ（あいづち）", "strings", patch="cello", volume=0.08, pan=-0.2, reverb=0.45, barGain=c.g())

A = ["1:3 2:1 3:2", "4:2 3:1 2:3", "3:3 5:1 3:2", "2:2 1:1 5,:3", "6,:2 7,:1 1:2 2:1", "3:2 4:1 5:3", "4:2 3:1 2:2 7,:1", "1:6"]
Bm = ["3:3 4:1 5:2", "6:2 5:1 4:3", "5:3 6:1 7:2", "1':6", "7:2 6:1 5:2 3:1", "4:2 3:1 2:3", "3:2 2:1 1:2 7,:1", "1:6"]
Bh = ["5:3 6:1 7:2", "1':2 7:1 6:3", "7:3 1':1 2':2", "1':6", "6:2 5:1 4:2 3:1", "4:2 3:1 2:3", "3:2 2:1 1:2 7,:1", "1:6"]
def slow(bars):   # 同じ節を倍の長さで（2小節に引きのばす）
    out = []
    for s in bars:
        toks = [x.split(":") for x in s.split()]
        tt = " ".join(f"{d}:{float(L) * 2:g}" for d, L in toks)
        # 12拍を2小節に分ける
        acc = 0; a = []; bb = []
        for d, L in toks:
            L2 = float(L) * 2
            if acc + L2 <= 6 + 1e-6: a.append(f"{d}:{L2:g}"); acc += L2
            else:
                if acc < 6 - 1e-6: a.append(f"{d}:{6 - acc:g}"); bb.append(f"{d}:{L2 - (6 - acc):g}"); acc = 6
                else: bb.append(f"{d}:{L2:g}")
        out += [" ".join(a), " ".join(bb)]
    return out
play_melody(c, "のんびり1", A + Bm, 4, "air", density=0.6, seed=1801)
play_melody(c, "のんびり2", A + Bm, 4, "air", density=0.8, seed=1802)
play_melody(c, "のんびり3", Bh + A, 4, "air", density=0.8, seed=1803)
play_melody(c, "昼寝", slow(A), 4, "air", density=0.5, seed=1804)
play_melody(c, "夢うつつ", ["1:3 2:1 3:2", "4:6", "3:3 2:3", "1:6", "R:3 5,:3", "1:6", "3:3 4:3", "3:6", "R:3 2:3", "1:6", "R:6", "R:6"], 4, "air", density=0.3, seed=1805)

B = S.beats
for b in range(c.NB):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]
    r = low(ch, "C2"); r = r + 12 if r < 40 else r
    t = tones(ch, "D3", "D5")
    if n == "鳥":
        if i == 2: GB.bar(b, f"R:3 {nm(r)}:3"); GA.bar(b, f"R:3 {nm(t[2])}:1 {nm(t[3])}:1 {nm(t[4 % len(t)])}:1")
        continue
    if n in ("のんびり1", "のんびり2", "のんびり3"):
        GB.bar(b, f"{nm(r)}:3 {nm(r + 7)}:3" if not (n == "のんびり3" and i % 2) else f"{nm(r)}:6")
        GA.bar(b, " ".join(f"{nm(t[x % len(t)])}:1" for x in (2, 3, 4, 2, 3, 4) if True))
        if n == "のんびり2" and i % 4 == 3: CELLO.bar(b, f"R:2 {nm(r)}:2 {nm(r - 5 if r - 5 >= 36 else r + 7)}:2")
    if n == "昼寝":
        GB.bar(b, f"{nm(r)}:6"); GA.bar(b, f"{nm(t[2])}:3 {nm(t[3])}:3")
        if i % 8 == 7: CELLO.bar(b, f"R:3 {nm(r)}:3")
    if n == "夢うつつ" and i < 11:
        GB.bar(b, f"{nm(r)}:6"); GA.bar(b, f"R:3 {nm(t[2])}:3" if i % 2 == 0 else f"{nm(t[3])}:6")
    if n in ("昼寝", "夢うつつ") and not (n == "夢うつつ" and i >= 11):   # 午後の光にまどろむ：うすい弦の和音
        v = voice(ch, 55, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:6")
        CELLO.bar(b, f"{nm(r)}:6") if n == "夢うつつ" else None
finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space dome --space-wet 0.34 --master -15 --widen 1.32 --side-hpf 200",
       "ケルト・フルート100曲の018（第2版）。昼下がりの納屋で、干し草の上でうとうと。6/8・付点4分＝40、G ミクソリディア。笛とギターのデュエット（ギターは低音の歩みと指弾き）、チェロが眠そうにあいづち。だんだんテンポがゆるんで眠りへ。",
       harm_scenes=None, tail_scene="夢うつつ", fill=False, pads=True, pad_scenes=["のんびり1", "のんびり2", "のんびり3", "昼寝", "夢うつつ"])
