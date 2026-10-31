# ケルト・フルート100曲「銀の笛と百の夜」016 石垣の道 The Stone-Wall Lane — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 翌朝、エイラは石垣にはさまれた細い道を、村の市場へ歩く。道は何度も直角に曲がり、角ごとに石垣の上で
#   村の子どもたちが足を踏み鳴らして遊んでいる。曲がるたびに足音だけが聞こえ、また笛とピアノが戻ってくる。
# 調べ: 喜び。形: ホーンパイプ（A 8小節・B 8小節。各部の最後を「タン・タン・タン」の3つの4分音符で決める）を5周。
# 拍子・速さ: 4/4・♩=80（8分は付点のはずみ）。旋法: C イオニア。
# 主役は笛（重心の低い笛。C4〜E5 が中心、装飾は少なめ）。
# 伴奏の主役: ピアノ（ケープブレトン式：左手が4分で歩く低音、右手が裏拍の和音）。打楽器なし（足音は曲がり角とタン・タン・タンだけ）。
# この曲だけ: 曲がり角（2周目B・3周目A・4周目B の4小節目）で1小節だけ全員が止まり、足拍子だけが鳴る。
# 始まり: ピアノの左手だけ → 終わり: 全員と足で「タン・タン・タン」。
# 山: 3周目（ピアノの左手がオクターブになり、右手もすべての裏拍に。タン・タン・タンに足が入る）。4周目は一度静かに（右手が A で休む）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "016-the-stone-wall-lane", "石垣の道", "The Stone-Wall Lane", 80, 4, "C", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
K = Key("C", "major", 4)
CA = ["C", "F", "Dm", "G", "C", "F", "G", "C"]
CB = ["G", "Am", "G", "C", "Am", "F", "G", "C"]
S.scene("左手", 4, "intro", ["C", "F", "G", "C"])
for r in range(1, 6):
    S.scene(f"{r}周目A", 8, "chorus" if r == 3 else "verse", CA)
    S.scene(f"{r}周目B", 8, "chorus" if r == 3 else "verse", CB)
S.scene("おわり", 2, "outro", ["C", "C"])
NAMES = ["左手"] + [f"{r}周目{p}" for r in range(1, 6) for p in "AB"] + ["おわり"]
DYN = {1: 0.66, 2: 0.74, 3: 0.88, 4: 0.7, 5: 0.82}
pts = [("左手", 0, 0.62)]
for r in range(1, 6):
    pts += [(f"{r}周目A", 0, DYN[r]), (f"{r}周目B", 7, DYN[r] + 0.02)]
pts += [("おわり", 0, 0.86), ("おわり", 1, 0.8)]
c = make(S, NAMES, pts, {}, flute_gain={n: 1.15 for n in NAMES}, intro="左手", passing=True, tension=False)
B = S.beats
G = c.g()
pg = [round(x * 1.0, 3) for x in G]                 # 試し書き出し: 左手1音・右手1音で笛とほぼ同じ大きさ（×1.4 のとき）→ 笛が主役なので ×1.0、右手は3音重なるので volume 0.08
LH = S.track("ピアノ（左手の歩く低音）", "piano", volume=0.3, pan=-0.15, reverb=0.35, sustain=1.0, barGain=pg)
LH8 = S.track("ピアノ（左手のオクターブ）", "piano", volume=0.2, pan=-0.18, reverb=0.35, sustain=1.0, barGain=pg)
RH = [S.track(f"ピアノ（右手の裏拍{j + 1}）", "piano", volume=0.08, pan=0.05 + 0.06 * j, reverb=0.35, sustain=0.8, barGain=pg) for j in range(3)]
FT = S.track("足拍子", "guitar", patch="frameDrum", volume=0.35, gainDb=18, pan=0.1, reverb=0.25, barGain=[round(x * 1.3, 3) for x in G])   # 足拍子は笛より約8dB小さい（止まった角で足音だけになる所なので少し上げる）

# ---------- 旋律（C イオニア。1=C4。各部の最後はタン・タン・タン） ----------
A = ["1:0.5 3:0.5 5:0.5 1':0.5 7:0.5 5:0.5 3:0.5 5:0.5", "4:0.5 6:0.5 1':0.5 6:0.5 5:0.5 3:0.5 1:0.5 3:0.5",
     "2:0.5 4:0.5 6:0.5 4:0.5 3:0.5 5:0.5 1':0.5 5:0.5", "4:0.5 3:0.5 2:0.5 1:0.5 7,:0.5 2:0.5 5,:1",
     "1:0.5 3:0.5 5:0.5 1':0.5 7:0.5 5:0.5 3:0.5 5:0.5", "6:0.5 5:0.5 4:0.5 6:0.5 5:0.5 4:0.5 3:0.5 2:0.5",
     "3:0.5 5:0.5 4:0.5 2:0.5 7,:0.5 2:0.5 4:0.5 2:0.5", "1:1 3:1 1:1 R:1"]
Bm = ["5:0.5 6:0.5 7:0.5 1':0.5 2':0.5 1':0.5 7:0.5 5:0.5", "6:0.5 1':0.5 3':0.5 1':0.5 6:0.5 4:0.5 2:0.5 4:0.5",
      "5:0.5 7:0.5 2':0.5 7:0.5 5:0.5 4:0.5 3:0.5 2:0.5", "3:0.5 5:0.5 1':0.5 5:0.5 3:1 5,:1",
      "6,:0.5 1:0.5 3:0.5 6:0.5 5:0.5 3:0.5 1:0.5 3:0.5", "4:0.5 6:0.5 1':0.5 6:0.5 5:0.5 7:0.5 2':0.5 7:0.5",
      "1':0.5 7:0.5 6:0.5 5:0.5 4:0.5 3:0.5 2:0.5 7,:0.5", "1:1 5:1 1':1 R:1"]
CORNER = {("2周目B", 3), ("3周目A", 3), ("4周目B", 3)}      # 曲がり角：1小節だけ全員が止まる
def with_corner(name, bars):
    return [("R:4" if (name, j) in CORNER else s_) for j, s_ in enumerate(bars)]
DENS = {1: 0.15, 2: 0.2, 3: 0.32, 4: 0.12, 5: 0.25}
for r in range(1, 6):
    play_melody(c, f"{r}周目A", with_corner(f"{r}周目A", A), 4, "hornpipe", key=K, density=DENS[r], seed=1600 + r)
    play_melody(c, f"{r}周目B", with_corner(f"{r}周目B", Bm), 4, "hornpipe", key=K, density=DENS[r], seed=1650 + r)
play_melody(c, "おわり", ["1:1 3:1 1:1 R:1", "R:4"], 4, "hornpipe", key=K, density=0.0)

# ---------- ピアノ（ケープブレトン式） ----------
ROOT = {"C": 36, "F": 41, "Dm": 38, "G": 43, "Am": 45}
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    pcs = [r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12]
    return sorted(60 + (p - 60) % 12 for p in pcs)                # C4〜B4
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r = ROOT[ch]
    corner = (n, i) in CORNER
    nxt = ROOT.get(S.chords[b + 1], 36) if b + 1 < c.NB else 36
    tan = n != "左手" and n != "おわり" and i == 7                  # 各部の最後の小節（タン・タン・タン）
    rd = int(n[0]) if n[0].isdigit() else 0
    if corner:                                                    # 曲がり角：足拍子だけ
        FT.bar(b, "C#3:1! C#3:1, C#3:0.5 C#3:0.5 C#3:1!")
        continue
    if n == "おわり":
        if i == 0:
            LH.bar(b, f"{nm(r)}:1 {nm(r + 4)}:1 {nm(r)}:1 R:1"); LH8.bar(b, f"{nm(r - 12)}:1 {nm(r - 8)}:1 {nm(r - 12)}:2")
            for j, t in enumerate(tri(ch)): RH[j].bar(b, f"{nm(t)}:1 {nm(t)}:1 {nm(t)}:2")
            FT.bar(b, "C#3:1! C#3:1! C#3:1! R:1")
        continue
    # 左手：4分で歩く（根音・5度・オクターブ・次の根音の半音下）。タン・タン・タンの小節は旋律と同じ3つ
    if tan:
        LH.bar(b, f"{nm(r)}:1 {nm(r + 7)}:1 {nm(r)}:1 R:1")
        if rd in (3, 5): FT.bar(b, "C#3:1! C#3:1! C#3:1! R:1")
    else:
        LH.bar(b, f"{nm(r)}:1 {nm(r + 7)}:1 {nm(r + 12)}:1 {nm(nxt - 1 if nxt > r else nxt + 1)}:1")
    if rd == 3 and not tan:
        LH8.bar(b, f"{nm(r - 12)}:1 R:1 {nm(r - 12)}:1 R:1")
    # 右手：裏拍の和音。1周目は2・4拍目の裏だけ、4周目の A は休む
    if n == "左手" or (rd == 4 and n.endswith("A")): continue
    pat = "R:1 R:0.5 X:0.5 R:1 R:0.5 X:0.5" if rd == 1 else "R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5"
    if tan: pat = "X:1 X:1 X:1 R:1"
    for j, t in enumerate(tri(ch)):
        RH[j].bar(b, pat.replace("X", nm(t)))

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.2 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の016（第3版）。石垣にはさまれた細い道を、村の市場へ。ホーンパイプ（4/4・♩=80・付点のはずみ）、C イオニア。各部の最後を「タン・タン・タン」で決める。ピアノはケープブレトン式（左手が4分で歩き、右手が裏拍の和音）。曲がり角では1小節だけ全員が止まって、子どもたちの足拍子だけが鳴る。山は3周目、終わりは全員と足でタン・タン・タン。",
       harm_scenes=None, tail_scene="おわり", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 4.0, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 4000, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -29, "delay": 0.2, "lp": 3000, "rt": 2.4}}}
json.dump(air, open("/tmp/cel/w/air016.json", "w"), ensure_ascii=False)
