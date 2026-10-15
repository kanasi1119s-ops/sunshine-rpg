# 『灯台守の祈り』（仮）: ケルト音楽5曲の3曲目。「スロー・エア」（踊らない、ゆっくり歌うように吹く曲）。
# BPM66・イ短調（エオリアン。終わりの手前だけ G# を借りる）・4/4。笛はロー・ホイッスルのように低めの音域で、長い音の頭に軽いカット。
# 形: 前奏2（バグパイプのドローンとハープ）→ A（笛）→ B（フィドル）→ C（笛とフィドルの重ね・弦・ティンパニ風のタムとシンバルのふくらみで一番高く）
#   → A'（笛ひとりに戻る・ハープ）→ 後奏2（ドローンとハープで消える）。
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from celtic_lib import Song, nm, md, fmt

AEOL = [9, 11, 0, 2, 4, 5, 7]
A = ["E5:4 D5:2 C5:2", "A4:6 C5:2", "G4:2 C5:2 D5:2 E5:2", "D5:6 B4:2",
     "E5:4 G5:2 A5:2", "C6:3 B5:1 A5:4", "F5:2 E5:2 D5:2 C5:2", "B4:4 A4:4"]
B = ["A5:4 C6:2 A5:2", "G5:6 E5:2", "F5:2 A5:2 D6:3 C6:1", "C6:4 B5:2 A5:2",
     "A5:3 G5:1 F5:2 A5:2", "G5:4 D5:2 G5:2", "A5:4 E5:4", "G#5:2 B5:2 E5:4"]
C = ["E6:4 D6:2 C6:2", "B5:4 D6:4", "C6:3 B5:1 A5:4", "A5:2 C6:2 F6:4",
     "F5:2 A5:2 D6:4", "E6:6 C6:2", "B5:4 G#5:4", "A5:8"]
CA = "Am F C G Am F Dm Esus4".split(); CB = "F C Dm Am F G Am E".split(); CC = "C G Am F Dm Am E7 Am".split()
plan = [("intro", "-", i) for i in range(2)] + [("A", "A", i) for i in range(8)] + [("B", "B", i) for i in range(8)] \
     + [("C", "C", i) for i in range(8)] + [("A2", "A", i) for i in range(8)] + [("out", "-", i) for i in range(3)]
S = Song(4, 2, len(plan), AEOL); S.check(A, B, C); S.G = 0.09   # BPM66 で約80ms（ゆっくりの曲なので、すべり込むような飾り。短いと笛の録音がプチッと鳴った）
MEL = {"A": A, "B": B, "C": C}
CHS = {"A": CA, "B": CB, "C": CC}
chords = [("Am" if k in ("intro", "out") else CHS[p][i]) for k, p, i in plan]
CH = {"Am": [45, 52, 57, 60, 64], "F": [41, 48, 53, 57, 60], "C": [48, 52, 55, 60, 64], "G": [43, 50, 55, 59, 62], "Dm": [50, 53, 57, 62, 65],
      "Esus4": [40, 47, 52, 57, 59], "E": [40, 47, 52, 56, 59], "E7": [40, 47, 50, 56, 59]}
ROOT = {"Am": 33, "F": 29, "C": 36, "G": 31, "Dm": 38, "Esus4": 28, "E": 28, "E7": 28}

S.part("flute", "panflute", "笛（ロー・ホイッスル風の旋律）", 0.22, 0.15, patch="flute", reverb=0.45, gainDb=2)
S.part("fiddle", "fiddle", "フィドル（旋律・対旋律）", 0.18, -0.2, patch="violin", reverb=0.45, gainDb=1)
S.part("cello", "strings", "チェロ（低い対旋律）", 0.12, -0.35, patch="cello", reverb=0.4)
S.part("harp", "harp", "ハープ（ゆっくりした分散和音）", 0.13, 0.4, reverb=0.45, bright=-0.4, attack=0.3)
S.part("pipe", "strings", "低い弦のドローン（A）", 0.06, -0.3, patch="cello", reverb=0.45)
S.part("pipe5", "strings", "低い弦のドローン（E）", 0.05, 0.3, patch="viola", reverb=0.45)
S.part("sth", "strings", "弦（上・のばす）", 0.08, 0.55, patch="slowStrings", reverb=0.45)
S.part("stl", "strings", "弦（下・のばす）", 0.08, -0.55, patch="slowStrings", reverb=0.45)
S.part("bass", "bass", "コントラバス", 0.16, 0, patch="contrabass", reverb=0.35)
S.part("tom", "tom", "タム（ティンパニのように低く）", 0.12, 0, reverb=0.3, gainDb=-8)
S.part("ride", "crash", "シンバル（ふくらませる）", 0.05, 0.2, gainDb=-8)
S.part("crash", "crash", "クラッシュ", 0.08, 0, gainDb=-8)

arc = []
for bi, (k, p, i) in enumerate(plan):
    ch = chords[bi]; v = CH[ch]
    sq = S.seq(MEL[p][i]) if p in MEL else None
    if k in ("A", "A2"): S.put("flute", bi, S.ornament(sq, "cut", bi, dens=0.5, legato=False))
    if k == "B": S.put("fiddle", bi, S.ornament(sq, "plain", 0, legato=True))
    if k == "C":
        S.put("flute", bi, S.ornament(sq, "cut", bi, dens=0.5, legato=False))
        h = []
        pcs = {x % 12 for x in v}
        for n, kk in sq:   # フィドルは旋律の下の、和音の音（3度以上下で一番近い音）
            m = md(n); c = m - 3
            while c % 12 not in pcs: c -= 1
            h.append((nm(c), kk))
        S.put("fiddle", bi, S.ornament(h, "plain", 0, legato=True))
    if k == "out" and i == 0: S.put("flute", bi, ["E5:2", "C5:1", "A4:1"])
    if k == "out" and i == 1: S.put("flute", bi, ["A4:4"])
    # チェロ（B と A2 で、根音から上へゆっくり動く）
    if k in ("B", "A2"):
        r = ROOT[ch] + 12 if ROOT[ch] + 12 >= 36 else ROOT[ch] + 24
        S.put("cello", bi, [f"{nm(r)}:2_", f"{nm(r + (3 if ch.endswith('m') else 4))}:2"] if i % 2 == 0 else [f"{nm(r + 7)}:3_", f"{nm(r)}:1"])
    # ハープ（8分の分散和音。C の山では休む）
    arp = [v[0] + 12, v[1] + 12, v[2] + 12, v[3] + 12, v[4] + 12]
    if k in ("intro", "A", "B", "A2", "out") and not (k == "out" and i == 2):
        pat = [0, 2, 3, 4, 3, 2, 1, 2] if i % 2 == 0 else [0, 1, 2, 4, 3, 1, 2, 3]
        S.put("harp", bi, [f"{nm(arp[j])}:0.5" for j in pat])
    if k == "out" and i == 2: S.put("harp", bi, [f"{nm(x)}:0.5" for x in arp] + [f"{nm(arp[2] + 12)}:1.5"])
    # ドローン
    if k in ("intro", "A", "out"):
        pass   # ドローンは入れない（バグパイプ・弦のドローンとも、入れると音質の点が下がった）
    # 弦（B の後半から C、A2 は薄く）
    if k in ("A", "B", "C", "A2") or (k == "out" and i < 2):
        S.put("sth", bi, [f"{nm(v[3] + 12)}:4"]); S.put("stl", bi, [f"{nm(v[1])}:4"])
    # コントラバス
    if k in ("A", "B", "C", "A2") or (k == "out" and i < 2):
        S.put("bass", bi, [f"{nm(ROOT[ch] + 12)}:4"])
    # タムとシンバル（C で山を作る。ふくらませるシンバルは小さな連打）
    if k == "B" and i == 7: S.put("tom", bi, ["A2:1,", "A2:1", "A2:0.5", "A2:0.5", "C3:0.5", "A2:0.5!"])
    if k == "C":
        S.put("tom", bi, ["A2:2!", "R:1", "A2:1,"] if i % 2 == 0 else ["A2:2", "R:1.5", "C3:0.5,"])
        if i == 7: S.put("tom", bi, ["A2:4!"])
        if i in (3, 6): S.put("ride", bi, ["D2:0.5,,"] * 4 + ["D2:0.5,", "D2:0.5,", "D2:0.5", "D2:0.5!"])
        if i in (0, 4): S.put("crash", bi, ["x:4"])
    if k == "A2" and i == 0: S.put("crash", bi, ["x:4,"])
    arc.append({"intro": 0.7, "A": 0.78, "B": 0.86, "C": 1.0, "A2": 0.84, "out": 0.72}[k])

out = sys.argv[1] if len(sys.argv) > 1 else "assets-src/ai-songs/celtic-air-lighthouse.json"
S.dump(out, "灯台守の祈り（仮）",
       "（仮）ケルト音楽5曲の3曲目。踊らない、ゆっくり歌う「スロー・エア」。BPM66・イ短調・約2分。ロー・ホイッスル風の低い笛で始まり、"
       "B はフィドル、C で笛とフィドルが重なって一番高くなり（弦・ティンパニ風のタム・ふくらむシンバル）、最後は笛ひとりとハープに戻って消える。バグパイプのドローン、チェロの対旋律。",
       66, chords, arc)
