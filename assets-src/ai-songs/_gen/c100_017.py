# ケルト・フルート100曲「銀の笛と百の夜」017 夕立の予感 Before the Evening Rain — 第3版（2026-11-01。docs/sound/celtic-study/E-100-plan.md）
# 物語: 市場からの帰り道。晴れた午後の草原で、エイラはいつもの節を吹きながら歩く。けれど西の空に雲が出て、
#   吹くたびに光が少しずつかげっていく。同じ節なのに、1回ごとに1つずつ音が暗くなり、最後は雨の前の低い空だけが残る。
# 調べ: あいだ。形: 主題と変奏（同じ旋律を5回。変奏ごとに旋法の影が濃くなる）。
# 拍子・速さ: 4/4・♩=64。旋法: D イオニア（主題・変奏1）→ D ミクソリディア（変奏2: C♯→C）→ D ドリア寄り（変奏3: F♯→F も）
#   → D エオリア（変奏4: B→B♭ も）→ D エオリアのドローン。
# 主役は笛（中音域。D4〜D5 が中心）。伴奏の主役: クラリネットとファゴット（木管の色づけ。長い音と、句の終わりのあいづち）。
#   竪琴・ギター・ピアノ・弦・パッド・打楽器は使わない。
# この曲だけ: 同じ旋律が、変奏ごとに1音ずつ暗い音に置きかわる（C♯ → F♯ → B の順に半音下がる）。
# 始まり: 明るい笛ひとり → 終わり: 短調のドローン（ファゴットの D とクラリネットの A）。
# 山: 終盤の短い影（変奏4。クラリネットとファゴットが厚くなり、笛が1オクターブ上がる。短く）。
import sys, json, re
from c100_common import *
from c100_v2 import *

S = Song("C100", "017-before-the-evening-rain", "夕立の予感", "Before the Evening Rain", 64, 4, "D", "major", "ケルト（幻想）")
S.kit = "naked"; S.keep_old_synth = True
S.extra.update({"human": 0.4, "rubato": 0.15})
K = Key("D", "major", 4)
CH = ["D", "G", "D", "A", "D", "G", "Em", "A", "G", "D", "A", "D"]
SC = [("主題", 12, "verse"), ("変奏1", 12, "verse"), ("変奏2", 12, "verse"), ("変奏3", 12, "verse"),
      ("雲", 4, "verse"), ("変奏4", 12, "chorus"), ("ドローン", 8, "outro")]
for n, L, kd in SC: S.scene(n, L, kd, (CH * 2)[:L])
NAMES = [x[0] for x in SC]
c = make(S, NAMES,
         [("主題", 0, 0.66), ("変奏1", 0, 0.7), ("変奏2", 0, 0.72), ("変奏3", 0, 0.74), ("雲", 0, 0.7), ("変奏4", 0, 0.8),
          ("変奏4", 6, 0.88), ("変奏4", 11, 0.8), ("ドローン", 0, 0.7), ("ドローン", 7, 0.62)],
         {}, flute_gain={n: 1.15 for n in NAMES}, intro="主題", passing=True, tension=False)
S.fix_avoid = lambda t: 0          # 半音下げた音を「直さない」
B = S.beats
G = c.g()
# 試し書き出し: クラリネット1音は笛とほぼ同じ大きさ、ファゴット（D2）は約3dB小さい → 笛が主役なので 0.16→0.09、0.18→0.12
CL = [S.track(f"クラリネット{j + 1}", "panflute", patch="clarinet", volume=0.09, pan=0.25 + 0.1 * j, reverb=0.45, breath=True,
              attack=0.08, release=0.5, bright=-0.2, barGain=G) for j in range(2)]
BN = S.track("ファゴット", "strings", patch="bassoon", volume=0.12, pan=-0.2, reverb=0.45, barGain=G)

# どの音を半音下げるか（変奏ごとに1つずつ増える）。PC: C♯=1, F♯=6, B=11
DARK = {"主題": set(), "変奏1": set(), "変奏2": {1}, "変奏3": {1, 6}, "雲": {1, 6}, "変奏4": {1, 6, 11}, "ドローン": {1, 6, 11}}
def darken(m, sc): return m - 1 if m % 12 in DARK[sc] else m

# ---------- 主題（D イオニア。1=D4。12小節：4+4+4） ----------
TH = ["3:1 2:0.5 1:0.5 3:1 5:1", "6:1.5 5:0.5 4:1 3:1", "2:1 3:1 4:1 7,:1", "1:4",
      "5:1 6:0.5 7:0.5 1':1 7:1", "6:1 4:1 5:2", "3:1 4:0.5 3:0.5 2:1 6,:1", "7,:3 R:1",
      "4:1 6:1 1':1.5 7:0.5", "6:1 5:1 3:2", "2:1 7,:1 4:1 3:1", "1:4"]
def place(sc, bars, oct_, dens, seed):
    """旋律を置き、その場面の暗い音を半音下げてから鳴らす"""
    ev = section_events(c, sc, bars, oct_, key=K)
    ev = [[t, L, darken(m, sc)] for t, L, m in ev]
    notes = ornament(ev, K, S.bpm, "air", B, density=dens, seed=seed)
    play(c.FLUTE, [(t, L, darken(m, sc) if m % 12 in DARK[sc] else m, mk) for t, L, m, mk in notes])

place("主題", TH, 4, 0.15, 1701)
place("変奏1", TH, 4, 0.3, 1702)
place("変奏2", TH, 4, 0.3, 1703)
place("変奏3", TH, 4, 0.35, 1704)
TH_UP = ["3':1 2':0.5 1':0.5 3':1 5':1", "6':1.5 5':0.5 4':1 3':1", "2':1 3':1 4':1 7:1", "1':4"]   # 影：最初の4小節だけ1オクターブ上（D6 は硬いので越えない）
place("変奏4", TH_UP + TH[4:], 4, 0.4, 1705)
place("ドローン", ["3:2 2:1 1:1", "6,:4", "7,:2 1:2", "1:4", "R:4", "3:2 2:2", "1:4", "R:4"], 4, 0.1, 1706)   # 1回目（7.07）は最後の2小節が全員休みで、約12秒ほぼ無音だった

# ---------- 木管の色づけ ----------
ROOT = {"D": 38, "G": 43, "A": 45, "Em": 40}
def chord3(ch, sc):
    m = re.match(r"^([A-G][#b]?)(m?)", ch); r = PC[m.group(1)]
    pcs = [r, (r + (3 if m.group(2) else 4)) % 12, (r + 7) % 12]
    return [darken(55 + (p - 55) % 12, sc) for p in pcs]
for b in range(c.NB):
    n, i, Lb, k = S.scene_of(b); ch = S.chords[b]; r = ROOT[ch]
    if n == "主題": continue
    if n == "ドローン":
        BN.bar(b, f"{nm(38)}:4"); CL[0].bar(b, f"{nm(57)}:4")        # 最後の小節まで（切らない）       # 短調のドローン（D と A）
        continue
    tones = chord3(ch, n)
    if n == "変奏1":                                                   # クラリネット1本が、句の終わり（4小節目ごと）に3度下であいづち
        if i % 4 == 3: CL[0].bar(b, f"R:1 {nm(tones[1])}:1 {nm(tones[0])}:2")
        continue
    if n == "変奏2":                                                   # ファゴットが入る：低い根音を長く
        BN.bar(b, f"{nm(darken(r, n))}:4")
        if i % 4 == 3: CL[0].bar(b, f"R:1 {nm(tones[1])}:1 {nm(tones[0])}:2")
        continue
    if n in ("変奏3", "雲"):                                           # クラリネット2本が和音を長く
        BN.bar(b, f"{nm(darken(r, n))}:2 {nm(darken(r + 7, n))}:2")
        CL[0].bar(b, f"{nm(tones[1])}:4"); CL[1].bar(b, f"{nm(tones[2])}:4,")
        continue
    if n == "変奏4":                                                   # 影：厚く、2拍ずつ動く
        BN.bar(b, f"{nm(darken(r, n))}:2 {nm(darken(r - 5 + 12, n) - 12)}:2")
        CL[0].bar(b, f"{nm(tones[1])}:2 {nm(tones[2])}:2"); CL[1].bar(b, f"{nm(tones[0] + 12)}:4")

finish(c, "--sound celtic-fantasy --orchestra vsco --piano salamander --space vale --space-wet 0.3 --master -15 --widen 1.15 --side-hpf 200",
       "ケルト・フルート100曲の017（第3版）。市場からの帰り道、西の空に雲が出る。主題と変奏（4/4・♩=64）。同じ旋律を5回吹くたびに1つずつ音が半音下がり、D イオニア → ミクソリディア → ドリア寄り → エオリアと、光が少しずつかげっていく。伴奏はクラリネットとファゴット。終盤に短い影（笛が1オクターブ上がる）、最後は雨の前の短調のドローン。",
       harm_scenes=None, tail_scene="ドローン", double=False, fill=False, pads=False)
air = {"pre": 0.3, "tail": 5.0, "layers": [{"file": "0595", "db": -45, "hp": 180, "lp": 3800, "wide": 0.012, "duck": 0.4, "fade": 6}],
       "fx": {"far": {"db": -28, "delay": 0.26, "lp": 2800, "rt": 3.2}}}
json.dump(air, open("/tmp/cel/w/air017.json", "w"), ensure_ascii=False)
