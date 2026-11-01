# ケルト・フルート100曲「銀の笛と百の夜」074 真相 The Truth — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 嵐のあと、岬の灯台の下でまどろんだエイラは、夢を見る（アシュリング＝夢の中の幻の歌）。光の中に若い祖父が現れ、
#   「鐘を止めたのはわたしだ」と告げる。エイラは問う（なぜ）。祖父は答えず、ただ「おまえが鳴らしてくれ」と約束を託す。
#   目がさめると、また低い1音だけが残っている。
# 調べ: 悲しみ。形: アシュリング（まどろみ → 輝き → 問い → 約束 → 目覚め）。
# 拍子・速さ: 3/4。まどろみと目覚めは ♩=60（ゆれを大きく）、輝き・問い・約束は ♩=76。旋法: F ドリア → A♭ イオニア → F ドリア。
# 主役は笛（低い笛 → 高い笛 → 低い笛）。伴奏の主役: 竪琴と弦。問いの場面はチェロ（チェロが2小節で問い、笛が2小節で答える）。
#   ギター・ピアノ・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: 「輝き」の瞬間に音域が一気に2オクターブ開く（それまで F2〜C5 にいた音が、A♭1〜E♭6 に広がる）。
# 始まり: 低い1音 → 終わり: 冒頭の低い1音に戻る。
# 山: 輝きの所。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "074-the-truth", "真相", "The Truth", 76, 3, "F", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.3, "rubato": 0.2})
KF, KA = Key("F", "dorian", 4), Key("Ab", "major", 4)
CM = ["Fm", "Eb", "Fm", "Eb", "Fm", "Bb", "Bb", "Fm", "Cm", "Bb", "Eb", "Bb", "Cm", "Bb", "Eb", "Fm"]
P1C = ["Ab", "Db", "Eb", "Ab", "Fm", "Bbm", "Eb", "Ab"]; P2C = ["Ab", "Db", "Fm", "Eb", "Db", "Bbm", "Eb", "Ab"]
CQ = ["Fm", "Fm", "Bb", "Bb", "Cm", "Cm", "Eb", "Eb", "Fm", "Fm", "Bb", "Bb", "Db", "Db", "Cm", "Cm", "Fm", "Fm", "Eb", "Eb", "Bb", "Bb", "Fm", "Fm"]
SC = [("まどろみ", 16, "intro", CM), ("輝き", 24, "chorus", P1C + P2C + P1C), ("問い", 24, "verse", CQ), ("約束", 16, "verse", P1C + P2C),
      ("目覚め", 16, "outro", CM[:12] + ["Bb", "Eb", "Fm", "Fm"])]
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("まどろみ", 0, 0.68), ("輝き", 0, 0.9), ("輝き", 20, 0.94), ("問い", 0, 0.74), ("約束", 0, 0.8), ("目覚め", 0, 0.7), ("目覚め", 15, 0.64)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="まどろみ", passing=True, tension=False)
S.fix_avoid = lambda t: 0
s = c.s0
S.tempo = [{"bar": 1, "bpm": 60}, {"bar": s["輝き"] + 1, "bpm": 76}, {"bar": s["目覚め"] + 1, "bpm": 60, "ramp": 4}]
B = S.beats
G = c.g()
# チェロの旋律（043: 0.025・gainDb 4・×1.4 で笛と同じくらい）。低い弦だけの所は始まり用に大きく（047）
VCM = S.track("チェロ（問う声）", "strings", patch="cello", volume=0.025, gainDb=4, pan=-0.2, reverb=0.6, release=0.4, barGain=[round(x * 1.4, 3) for x in G])
VCD = S.track("チェロ（低い持続）", "strings", patch="cello", volume=0.03, gainDb=8, pan=-0.15, reverb=0.7, release=1.0, barGain=G)
CBL = S.track("コントラバス（輝きの底）", "strings", patch="contrabass", volume=0.04, gainDb=6, pan=-0.05, reverb=0.8, release=1.0, barGain=G)
VN = [S.track(f"バイオリン（輝きの空{j + 1}）", "strings", patch="violin", volume=0.025, gainDb=4, pan=0.3 + 0.1 * j, reverb=0.85, release=1.0, barGain=G) for j in range(2)]
HP = [S.track(f"竪琴{j + 1}", "harp", patch="folkHarp", volume=0.07, pan=-0.3 + 0.2 * j, reverb=0.7, sustain=1.8, barGain=G) for j in range(4)]

def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12
def near(pc, lo):
    return lo + (pc - lo) % 12

# ---------- 笛 ----------
DOZE = ["1:3", "2:2 1:1", "3:3", "2:3", "1:2 3:1", "4:3", "3:2 2:1", "1:3", "5:3", "4:2 3:1", "2:3", "3:2 4:1", "5:2 4:1", "3:2 2:1", "2:3", "1:3"]
P1 = ["5:2 6:1", "1':3", "7:2 6:1", "5:3", "6:2 1':1", "2':3", "1':2 7:1", "1':3"]
P2 = ["3':2 2':1", "1':3", "6:2 1':1", "5:3", "4:2 5:1", "6:3", "5:2 4:1", "3:3"]
c.FLUTE.at(0, "F4:3")
play_melody(c, "まどろみ", ["R:3"] + DOZE[1:], 4, "air", key=KF, density=0.12, seed=7401)
play_melody(c, "輝き", P1 + P2 + P1, 4, "air", key=KA, density=0.3, seed=7402)
# 問い：チェロが2小節で問い（上がって止まる）、笛が2小節で答える（下りる）
QC = [["1:1 3:1 5:1", "4:3"], ["5:1 4:1 5:1", "7:3"], ["3:1 5:1 7:1", "1':3"], ["5:2 4:1", "5:3"], ["1:1 2:1 3:1", "5:3"], ["4:1 5:1 6:1", "5:3"]]
QF = [["5:2 4:1", "3:3"], ["7:2 6:1", "5:3"], ["2':2 1':1", "7:3"], ["4:2 3:1", "2:3"], ["6:2 5:1", "4:3"], ["3:2 2:1", "1:3"]]
s0 = s["問い"]
for q in range(6):
    ev = []
    for j, s_ in enumerate(QC[q]): ev += mel_events(KF, s_, 3, (s0 + 4 * q + j) * B)
    play(VCM, [(round(t, 4), L, m, "") for t, L, m in ev])
    ev = []
    for j, s_ in enumerate(QF[q]): ev += mel_events(KF, s_, 4, (s0 + 4 * q + 2 + j) * B)
    play(c.FLUTE, ornament([[round(t, 4), L, m] for t, L, m in ev], KF, 76, "air", B, density=0.2, seed=7410 + q))
play_melody(c, "約束", P1 + P2[:7] + ["1':3"], 4, "air", key=KA, density=0.25, seed=7403)
play_melody(c, "目覚め", DOZE[:12] + ["2:3", "1:3", "R:3", "R:3"], 4, "air", key=KF, density=0.08, seed=7404)
c.FLUTE.at((s["目覚め"] + 14) * B, "F4:6")                          # 冒頭の低い1音に戻る

# ---------- 伴奏 ----------
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r, th, fi = tri(ch)
    if n in ("まどろみ", "目覚め"):                                     # 低い所だけ（F2〜C5）
        if i % 2 == 0: VCD.at(b * B, f"{nm(near(r, 41))}:{2 * B + 0.2}{',' if i % 4 else ''}")
        if i % 2 == 1: HP[0].at(round(b * B + 1, 3), f"{nm(near(fi, 53))}:2,"); HP[1].at(round(b * B + 2, 3), f"{nm(near(th, 60))}:1,")
    elif n in ("輝き", "約束"):                                         # 一気に開く（A♭1〜E♭6）
        wide = (n == "輝き")
        seq = [near(r, 32 if wide else 44), near(fi, 39 if wide else 51), near(r, 44), near(th, 48), near(fi, 51), near(r, 56), near(th, 60), near(fi, 63),
               near(r, 68), near(th, 72)] if wide else [near(r, 44), near(fi, 51), near(r, 56), near(th, 60), near(fi, 63), near(r, 68)]
        step = 3 / len(seq)
        for q, m in enumerate(seq):
            HP[q % 4].at(round(b * B + q * step, 3), f"{nm(m)}:{round(3 - q * step + 0.5, 2)}{'' if q == 0 else ','}")
        if i % 2 == 0:
            if wide: CBL.at(b * B, f"{nm(near(r, 32))}:{2 * B + 0.2}")
            VCD.at(b * B, f"{nm(near(r, 44))}:{2 * B + 0.2},")
            VN[0].at(round(b * B + 0.05, 3), f"{nm(near(th, 79 if wide else 67))}:{2 * B + 0.1},"); VN[1].at(round(b * B + 0.1, 3), f"{nm(near(fi, 84 if wide else 72))}:{2 * B},")
    else:                                                             # 問い：竪琴はそっと、チェロの持続は休み
        HP[2].at(round(b * B, 3), f"{nm(near(r, 53))}:2,"); HP[3].at(round(b * B + 1, 3), f"{nm(near(th, 57))}:1.5,")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.34 --master -15 --widen 1.2 --side-hpf 200",
       "ケルト・フルート100曲の074（第3版）。嵐のあと、岬でまどろんだエイラが夢を見る（アシュリング）。3/4。F ドリアのまどろみは F2〜C5 の低い所だけで、笛は低く。光の中に若い祖父が現れる「輝き」で A♭ の長調になり、音域が一気に2オクターブ開く（コントラバスの A♭1 から、バイオリンの E♭6 まで。山）。「問い」ではチェロが2小節で問い、笛が2小節で答える。「約束」をへて、目覚めでは冒頭の低い F の1音に戻る。",
       harm_scenes=None, tail_scene="目覚め", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 160, "lp": 3600, "wide": 0.012, "duck": 0.4, "fade": 7}],
       "fx": {"far": {"db": -26, "delay": 0.34, "lp": 2800, "rt": 4.2}}}
json.dump(air, open("/tmp/cel/w/air074.json", "w"), ensure_ascii=False)
