# ケルト・フルート100曲「銀の笛と百の夜」047 夜の見張り台 The Night Watchtower — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 塔のてっぺんの見張り台で、エイラは夜通し番をする。暗い谷に向かって笛で長く呼びかけると、遠い向こうの見張り台から、
#   だれかが同じ音で、小さく返事をする（祖父の時代から続く、見張り同士の合図）。夜明け前、ふたつの笛は和音で寄りそう。
# 調べ: あいだ。形: 遠い返事（呼びかけの最後の音を、遠くの笛が同じ音で小さく返す）を20回 → 寄りそう。
# 拍子・速さ: 4/4・♩=46。旋法: B エオリア。
# 主役は笛（長い呼びかけ）。伴奏の主役: 遠い2本目の笛（小さく、響きが多く、右の遠く）と、コントラバスの低い持続。
#   竪琴・ギター・ピアノ・パッド・打楽器・ほかの弦は使わない（019 の「受け渡し」とちがい、遠い笛は1音だけを返す）。
# この曲だけ: 遠くの笛が、呼びかけの最後の音と同じ音で、小さく返事をする。
# 始まり: 低い弦 → 終わり: 2つの笛が和音（3度）で寄りそう。
# 山: なし。
import sys, json, re
from c100_common import *
from c100_v2 import *
from c100_v2 import _dia

S = Song("C100", "047-the-night-watchtower", "夜の見張り台", "The Night Watchtower", 46, 4, "B", "minor", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.35, "rubato": 0.25})
K = Key("B", "minor", 4)
SC = [("低い弦", 2, "intro", ["Bm", "Bm"]), ("呼びかけ", 40, "verse", (["Bm", "Bm", "G", "G", "Em", "Em", "F#m", "F#m"] * 5)),
      ("寄りそう", 8, "verse", ["Bm", "G", "Em", "F#m", "Bm", "G", "F#m", "Bm"]), ("夜明け前", 2, "outro", ["Bm", "Bm"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES, [("低い弦", 0, 0.66), ("呼びかけ", 0, 0.7), ("呼びかけ", 39, 0.72), ("寄りそう", 0, 0.72), ("夜明け前", 0, 0.68)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="低い弦", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 試し書き出し: 遠い笛（0.1）は笛と同じくらい → 0.05（小さく返す）。コントラバスも笛と同じくらい → 0.018
FAR = S.track("遠い見張りの笛", "panflute", patch="flute", volume=0.05, bright=-0.7, pan=0.55, reverb=0.9, breath=False, barGain=G)
CB = [S.track(f"コントラバス（低い持続{j + 1}）", "strings", patch="contrabass", volume=0.018, pan=-0.05, reverb=0.65, release=0.6, barGain=[round(x * 1.5, 3) for x in G]) for j in range(2)]

# ---------- 呼びかけ（2小節。最後の音は2小節目の2拍目で終わり、3拍目から遠い返事） ----------
CALLS = [["1:4", "5,:2 R:2"], ["3:2 2:2", "1:2 R:2"], ["5:4", "4:2 R:2"], ["3:4", "2:2 R:2"], ["6,:2 7,:2", "1:2 R:2"],
         ["5:3 4:1", "3:2 R:2"], ["2:2 3:2", "4:2 R:2"], ["5:2 7:2", "1':2 R:2"], ["7:2 5:2", "6:2 R:2"], ["4:4", "3:2 R:2"],
         ["1:4", "7,:2 R:2"], ["3:2 4:2", "5:2 R:2"], ["1':4", "7:2 R:2"], ["5:2 4:2", "3:2 R:2"], ["2:4", "1:2 R:2"],
         ["5,:2 7,:2", "1:2 R:2"], ["3:2 5:2", "4:2 R:2"], ["3:4", "2:2 R:2"], ["7,:2 1:2", "2:2 R:2"], ["1:4", "1:2 R:2"]]
s0 = c.s0["呼びかけ"]
for q, call in enumerate(CALLS):
    b0 = s0 + 2 * q
    ev = []
    for j, s_ in enumerate(call): ev += mel_events(K, s_, 4, (b0 + j) * B)
    ev = [[round(t, 4), L, m] for t, L, m in ev]
    play(c.FLUTE, ornament(ev, K, 46, "air", B, density=0.2, seed=4700 + q))
    last = ev[-1][2]
    FAR.at(round((b0 + 1) * B + 2.15, 3), f"{nm(last)}:1.8{',' if q % 3 else ''}")     # 遠い返事：同じ音で、小さく
# 寄りそう：同じ節を2本で、遠い笛が3度下で
s0 = c.s0["寄りそう"]
HYM = ["3:2 4:2", "5:4", "4:2 3:2", "2:4", "3:2 5:2", "4:2 3:2", "2:2 1:1 7,:1", "1:4"]
ev = []
for j, s_ in enumerate(HYM): ev += mel_events(K, s_, 4, (s0 + j) * B)
play(c.FLUTE, ornament([[round(t, 4), L, m] for t, L, m in ev], K, 46, "air", B, density=0.15, seed=4730))
play(FAR, [(round(t, 4), L, _dia(K, m, -2), "") for t, L, m in ev])
s0 = c.s0["夜明け前"]
c.FLUTE.at(s0 * B, "D5:6"); FAR.at(s0 * B, "B4:6,")
# コントラバス：B と F♯ を4小節ずつ
# 1回目（7.35）: コントラバスだけの始まり（約10秒）が本編より約20dB 小さかった → 始まり用の低い弦を別に（大きく）
CBI = [S.track(f"コントラバス（始まり{j + 1}）", "strings", patch=("contrabass" if j == 0 else "cello"), volume=(0.07 if j == 0 else 0.03), gainDb=8, pan=-0.1 + 0.2 * j, reverb=0.65, release=1.2) for j in range(2)]
CBI[0].at(0, "B1:8.5"); CBI[1].at(0.05, "F#2:8.4,")
for b in range(2, c.NB - 1, 4):
    CB[(b // 4) % 2].at(b * B, f"{'B1' if (b // 4) % 2 == 0 else 'F#2'}:{min(16, (c.NB - b) * B)},")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.36 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の047（第3版）。塔のてっぺんの見張り台で、夜通しの番。4/4・♩=46、B エオリア。エイラの笛が暗い谷へ長く呼びかけると、遠い向こうの見張りの笛が、呼びかけの最後の音と同じ音で小さく返事をする（20回）。伴奏はコントラバスの低い持続だけ。夜明け前、ふたつの笛は3度で寄りそう。",
       harm_scenes=None, tail_scene="夜明け前", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 160, "lp": 3400, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -26, "delay": 0.34, "lp": 2600, "rt": 4.4}}}
json.dump(air, open("/tmp/cel/w/air047.json", "w"), ensure_ascii=False)
