# ケルト・フルート100曲「銀の笛と百の夜」036 迷いの道 The Wandering Path — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 光る茸の夜が明けると、森の道がいくつにも分かれている。エイラは歩きながら笛を吹くが、道は思った所で曲がらず、
#   思いがけない所で曲がる。同じ場所に戻ってきたような気がする。最後まで出口は見つからず、迷ったまま歩き続ける。
# 調べ: あいだ。形: 不規則な長さの部（アイルランドのセット・ダンス型）。A 部は8小節だが、B 部は 11 小節（4+4+3）。
# 拍子・速さ: 4/4・♩=80。旋法: A ドリア（B 部の9小節目だけ、C の和音で道が曲がる）。
# 主役は笛（迷う笛）。伴奏の主役: チェンバロの歩み（左手の4分の低音が歩き、右手が2・4拍目で和音）。
#   竪琴・ギター・ピアノ・弦・パッド・打楽器・2本目の笛は使わない。
# この曲だけ: A 部は8小節だが B 部は 11 小節で、予想と違う所で曲がる（3小節目の句が途中で切れて、次の A が早く来る）。
# 始まり: 旋律から（前奏なし）→ 終わり: 迷ったまま終わる（主音に着かない。2度の音で止まる）。
# 山: 2つ（2周目と4周目の B）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "036-the-wandering-path", "迷いの道", "The Wandering Path", 80, 4, "A", "dorian", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4})
K = Key("A", "dorian", 4)
CA = ["Am", "G", "Am", "Em", "D", "Am", "D", "Em"]
CBn = ["Em", "D", "G", "Em", "Am", "D", "G", "Bm", "C", "Am", "D"]       # 11小節。9小節目の C で道が曲がる
SC = []
for r in range(1, 5):
    SC += [(f"{r}周目A", 8, "verse", CA), (f"{r}周目B", 11, "chorus" if r in (2, 4) else "verse", CBn)]
    if r == 2: SC.append(("迷い", 6, "verse", ["Am", "Em", "D", "Am", "G", "D"]))
SC.append(("迷ったまま", 8, "outro", CA))
for n, L, kd, ch in SC: S.scene(n, L, kd, ch)
NAMES = [x[0] for x in SC]
DYN = {1: 0.7, 2: 0.82, 3: 0.72, 4: 0.86}
pts = []
for r in range(1, 5):
    pts += [(f"{r}周目A", 0, DYN[r] - 0.04), (f"{r}周目B", 6, DYN[r]), (f"{r}周目B", 10, DYN[r] - 0.02)]
pts += [("迷い", 0, 0.66), ("迷ったまま", 0, 0.72), ("迷ったまま", 7, 0.64)]
c = make(S, NAMES, pts, {}, flute_gain={n: 1.15 for n in NAMES}, intro="1周目A", passing=True, tension=False)
S.fix_avoid = lambda t: 0
B = S.beats
G = c.g()
# 試し書き出し: チェンバロの左手（0.14）も右手の和音（0.06×3）も笛より約5dB 小さい（丁度よい）
HL = S.track("チェンバロ（左手の歩み）", "harpsichord", volume=0.14, pan=-0.2, reverb=0.35, barGain=G)
HR = [S.track(f"チェンバロ（右手の和音{j + 1}）", "harpsichord", volume=0.06, pan=0.15 + 0.05 * j, reverb=0.35, barGain=G) for j in range(3)]

# ---------- 旋律（A ドリア。1=A4） ----------
A = ["1:1 2:0.5 3:0.5 5:1 3:1", "4:1 3:1 2:1 7,:1", "1:0.5 2:0.5 3:1 4:1 6:1", "5:2 3:2",
     "4:1 5:0.5 6:0.5 5:1 4:1", "3:1 2:1 1:1 7,:1", "6,:1 7,:1 1:1 3:1", "2:2 1:2"]
Bn = ["5:1 6:1 7:1 1':1", "2':2 1':1 7:1", "6:1 5:1 4:1 6:1", "5:4",
      "1':1 7:1 6:1 5:1", "4:1 6:1 5:1 3:1", "2:1 3:1 4:1 5:1", "6:4",
      "7:1 5:1 3:1 7,:1", "1:1 3:1 6:2", "4:3 R:1"]                      # 3つ目の句は3小節で切れる（曲がる）
DENS = {1: 0.25, 2: 0.45, 3: 0.3, 4: 0.5}
for r in range(1, 5):
    play_melody(c, f"{r}周目A", A, 4, "march", key=K, density=DENS[r], seed=3600 + r)
    play_melody(c, f"{r}周目B", Bn, 4, "march", key=K, density=DENS[r], seed=3610 + r)
play_melody(c, "迷い", ["5:2 R:1 3:1", "2:3 R:1", "6,:2 7,:2", "1:1 R:1 5,:2", "3:2 4:2", "5:4"], 4, "air", key=K, density=0.2, seed=3620)
play_melody(c, "迷ったまま", A[:6] + ["6,:1 7,:1 1:1 3:1", "2:4"], 4, "march", key=K, density=0.3, seed=3621)   # 主音に着かず、2度（B）で止まる

# ---------- チェンバロの歩み ----------
ROOT = {"Am": 45, "G": 43, "Em": 40, "D": 38, "Bm": 47, "C": 48}
def tri(ch):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    return sorted(57 + (p - 57) % 12 for p in (r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12))
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r = ROOT[ch]
    nxt = ROOT.get(S.chords[b + 1], r) if b + 1 < c.NB else r
    if n == "迷い":                                                   # 迷い：歩みが止まり、1音ずつ
        HL.bar(b, f"{nm(r)}:2, R:2" if i % 2 == 0 else f"R:2 {nm(r + 7)}:2,")
        continue
    last = n == "迷ったまま" and i == 7
    if last:
        HL.bar(b, f"{nm(47)}:4"); continue                            # 低音も B で止まる（主音に着かない）
    HL.bar(b, f"{nm(r)}:1 {nm(r + 7)}:1, {nm(r + 12)}:1 {nm(nxt + (1 if nxt < r else -1))}:1,")
    for j, x in enumerate(tri(ch)): HR[j].bar(b, f"R:1 {nm(x)}:1, R:1 {nm(x)}:1,")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.24 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の036（第3版）。いくつにも分かれる森の道で迷う。アイルランドのセット・ダンス型（4/4・♩=80）、A ドリア。A 部は8小節だが B 部は 11 小節（4+4+3）で、思いがけない所で曲がり（9小節目の C の和音）、次の A が早く来る。伴奏はチェンバロの歩み。山は2周目と4周目、最後は主音に着かずに迷ったまま止まる。",
       harm_scenes=None, tail_scene="迷ったまま", double=False, fill=False, pads=False)
air = {"pre": 0.2, "tail": 4.5, "layers": [{"file": "0595", "db": -46, "hp": 200, "lp": 3800, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -28, "delay": 0.24, "lp": 2800, "rt": 3.0}}}
json.dump(air, open("/tmp/cel/w/air036.json", "w"), ensure_ascii=False)
