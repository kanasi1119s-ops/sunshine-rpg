# ラウド26曲 01「灰皿にネオン」（仮）。2026-10-24 素材から作り直し（人間「似た曲を作らない。つまらない曲を作らない。曲として成り立っていない物を作らない。単調にならない」）
# スタイル: ニューメタルのうねり（低い C♯ の跳ねるリフ・ハーフタイムのグルーヴ）＋アルトサックス。C♯ ドリアン（♭5 の G をブルーノートに）・96・4/4
# 物語: 雨の路地に迷いこんだ旅人。何度角を曲がっても、同じネオンの看板（サビ）に出る。裏口の酒場、ケンカ、傷ついて看板の下へ、
#       サックス吹きの独奏、もう一度看板、夜明け前にサックスだけが残る。
# 形: ロンド（看板＝サビに4回戻る。毎回ようすが違う）。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ（区間の種類ではなく中身で決める）:
#   雨（0）: 遠いクリーンの雨粒とベースの低いうなりだけ。ドラムは後半にハットの気配
#   看板1（2）: 中くらい。看板は眩しいが、全開にはしない
#   路地（1）: ハーフタイムで低く。旋律は早口の同じ音（しゃべるよう）、サックスが返事をする
#   看板2（2）: サックスが旋律にオクターブ下で重なる
#   ケンカ（3）: この曲で一度だけの全開。3+3+2 でずれる刻み。最後は1小節の無音
#   看板3（1）: 傷ついた看板。半分の速さの感じ・リフは小節の頭だけ・旋律はとぎれとぎれ
#   裏口（1→2）: サックスの独奏。前半はウォーキングベースとライド、後半に歪みが戻る
#   看板4（2）: サックスとリードが同じ旋律（オクターブ）。最後の4小節だけ一段強く
#   夜明け（0）: サックスとクリーンだけ。フェードアウト
# 旋律の性格: 裏拍から入り、小節線を食い（シンコペーション）、句の終わりは早めに切って休む（小節の終わりで伸ばさない）。3連符・ブルーノート
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 96, 4
bar = Bars(BEATS)
R4 = bar.rest()

FORM = [("rain", 8), ("neon", 8), ("alley", 16), ("neon2", 8), ("fight", 12), ("neon3", 8), ("backdoor", 16), ("neon4", 12), ("dawn", 12)]
NEON = ["C#m7", "C#m7", "Amaj7", "B", "C#m7", "C#m7", "Amaj7", "G#7"]
ALLEY = ["C#m7", "F#7", "C#m7", "F#7", "Emaj7", "D#m7", "C#m7", "G#7"] * 2
CH = {"rain": ["C#m7", "C#m7", "C#m7", "C#m7", "Amaj7", "Amaj7", "B", "B"],
      "neon": NEON, "alley": ALLEY, "neon2": NEON,
      "fight": ["C#5"] * 6 + ["D5"] * 4 + ["C#5"] * 2,
      "neon3": NEON,
      "backdoor": ["C#m7", "F#7", "C#m7", "F#7", "Emaj7", "D#m7", "G#7", "C#m7"] * 2,
      "neon4": NEON + ["Amaj7", "B", "Amaj7", "G#7"],
      "dawn": ["C#m7", "C#m7", "Amaj7", "Amaj7", "C#m7", "C#m7", "Amaj7", "Amaj7", "C#m7", "C#m7", "C#m7", "C#m7"]}
song = Song("路地裏の灯（仮）",
            "仮: ラウド26曲の1曲目（2026-10-24 素材から作り直し）。ニューメタルのうねり＋アルトサックス。C♯ ドリアン・96。看板（サビ）に4回戻るロンド。"
            "旋律は裏拍から入って小節線を食い、句の終わりを早めに切る。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 雨の路地に迷いこんだ旅人が、何度も同じネオンの看板に出る。ケンカ、傷、サックスの独奏、夜明けにサックスだけが残る。"
song.kinds = {"rain": "intro", "neon": "chorus", "alley": "verse", "neon2": "chorus", "fight": "break", "neon3": "chorus",
              "backdoor": "solo", "neon4": "chorus", "dawn": "outro"}
SECS, NB = song.secs, song.nb

# ---------------- 看板のリフ（低い C♯ の跳ね。♭5 の G で一瞬ゆがむ） ----------------
RIFF = {
    "C#m7": [bar("C#2:0.75! C#2:0.25 R:0.5 C#3:0.25 B2:0.25 R:0.5 C#2:0.5! E2:0.5 F#2:0.25 G2:0.25"),
             bar("G#2:0.5! G2:0.25 F#2:0.25 E2:0.5 C#2:0.5! R:0.5 C#2:0.25 C#2:0.25 B1:1!")],
    "Amaj7": [bar("A1:0.75! A1:0.25 R:0.5 A2:0.25 G#2:0.25 R:0.5 A1:0.5! C#2:0.5 E2:0.5")],
    "B": [bar("B1:0.75! B1:0.25 R:0.5 B2:0.25 A2:0.25 R:0.5 B1:0.5! D#2:0.25 E2:0.25 F#2:0.5")],
    "G#7": [bar("G#1:0.75! G#1:0.25 R:0.5 G#2:0.25 F#2:0.25 R:0.5 G#1:0.5! C2:0.25 D#2:0.25 F#2:0.5")],
}
# 路地: 間を空けた突き（旋律の早口のじゃまをしない）
STAB = {"C#m7": bar("C#2:0.5! R:1.5 C#2:0.25 C#2:0.25 R:1.5"), "F#7": bar("F#1:0.5! R:1.75 F#1:0.25 R:0.5 E2:0.5 F#2:0.5"),
        "Emaj7": bar("E1:0.5! R:1.5 E2:0.25 E1:0.25 R:1.5"), "D#m7": bar("D#2:0.5! R:2 D#2:0.25 E2:0.25 F#2:0.5 G#2:0.5"),
        "G#7": bar("G#1:0.5! R:1 G#1:0.25 G#1:0.25 G2:0.5! F#2:0.5 E2:0.5 D#2:0.5")}
# ケンカ: 3+3+2 の16分でずれる刻み（拍の頭とずれて、殴り合いのように）
FIGHT = {"C#5": bar("C#2:0.75! C#2:0.75! C#2:0.5! C#2:0.75! C#2:0.75! G2:0.5!"),
         "D5": bar("D2:0.75! D2:0.75! D2:0.5! D2:0.75! G#2:0.75! G2:0.5!")}

# ---------------- 旋律 ----------------
NEON_MEL = [
    bar("R:0.5 G#4:0.25 B4:0.25 C#5:0.5 R:0.25 C#5:0.25 E5:0.75 C#5:0.25 B4:0.5 G#4:0.5"),
    bar("R:0.25 F#4:0.25 G#4:0.5 B4:0.75 G#4:0.25 R:2"),
    bar("R:0.5 A4:0.25 C#5:0.25 E5:0.5 R:0.25 E5:0.25 F#5:0.75 E5:0.25 C#5:0.5 B4:0.5"),
    bar("R:0.25 D#5:0.25 C#5:0.25 B4:0.25 R:0.5 F#4:0.5 R:2"),
    bar("R:0.5 G#4:0.25 B4:0.25 C#5:0.5 R:0.25 C#5:0.25 E5:0.75 C#5:0.25 B4:0.5 G#4:0.5"),
    bar("R:0.25 F#4:0.25 G#4:0.5 B4:0.25 C#5:0.5 B4:0.25 R:2"),
    bar("E5:0.75 C#5:0.25 R:0.5 C#5:0.25 B4:0.25 A4:0.5 E4:0.5 R:1"),
    bar("R:0.5 C5:0.25 D#5:0.25 F#5:0.5 R:0.5 G#4:1 R:1"),
]
# 傷ついた看板: 同じ旋律の、ところどころが欠ける
NEON3_MEL = [bar("R:0.5 G#4:0.25 B4:0.25 C#5:0.5 R:2.5"), R4, bar("R:0.5 A4:0.25 C#5:0.25 E5:0.5 R:2.5"), bar("R:1 C#5:0.25 B4:0.25 R:2.5"),
             bar("R:2 E5:0.75 C#5:0.25 B4:0.5 G#4:0.5"), bar("R:0.25 F#4:0.25 G#4:0.5 R:3"), bar("E5:0.75 C#5:0.25 R:3"), bar("R:2 G#4:1 R:1")]
# 看板4の最後の4小節（一段強く。小節線を食う）
NEON4_TAG = [bar("R:0.5 A4:0.25 C#5:0.25 E5:0.5 F#5:0.5 E5:0.25 C#5:0.25 B4:0.5 C#5:1"),
             bar("R:0.25 D#5:0.25 F#5:0.5 D#5:0.25 B4:0.25 R:0.5 F#4:0.25 G#4:0.25 B4:0.5 R:1"),
             bar("R:0.5 E5:0.333 F#5:0.333 E5:0.334 C#5:0.5 A4:0.5 R:0.5 C#5:0.5 E5:0.5"),
             bar("C5:0.5 D#5:0.5 R:0.25 C5:0.25 G#4:0.5 R:2")]
# 路地: 早口（同じ音の16分）と、3連符のため息
ALLEY_MEL = [
    bar("R:1 G#4:0.25 G#4:0.25 G#4:0.25 F#4:0.25 E4:0.5 R:0.25 E4:0.25 F#4:0.5 R:0.5"),
    bar("G#4:0.25 G#4:0.25 A#4:0.5 R:0.25 G#4:0.25 F#4:0.25 E4:0.25 C#4:1 R:1"),
    bar("R:0.5 E4:0.25 E4:0.25 E4:0.25 F#4:0.25 G#4:0.25 B4:0.25 R:0.5 B4:0.25 C#5:0.25 B4:0.5 R:0.5"),
    bar("A#4:0.75 G#4:0.25 E4:0.5 R:2.5"),
    bar("R:1 G#4:0.25 G#4:0.25 G#4:0.25 B4:0.25 D#5:0.5 R:0.5 C#5:0.25 B4:0.25 R:0.5"),
    bar("R:0.25 A#4:0.25 A#4:0.25 F#4:0.25 C#5:0.5 A#4:0.5 R:2"),
    bar("R:0.5 G#4:0.333 A4:0.333 B4:0.334 C#5:0.5 B4:0.5 R:1.5"),
    bar("C5:0.25 C5:0.25 B4:0.25 G#4:0.25 F#4:0.5 D#4:0.5 R:2"),
    bar("R:0.25 C#5:0.25 C#5:0.25 C#5:0.25 B4:0.25 G#4:0.25 R:0.5 E4:0.25 F#4:0.25 G#4:0.5 R:1"),
    bar("R:1 F#4:0.25 F#4:0.25 A#4:0.5 R:0.5 C#5:0.5 R:1"),
    bar("R:0.25 E4:0.25 G#4:0.25 B4:0.25 C#5:0.25 B4:0.25 G#4:0.25 E4:0.25 R:2"),
    bar("R:2 C#5:0.333 B4:0.333 A#4:0.334 F#4:1"),
    bar("R:0.5 B4:0.25 B4:0.25 B4:0.25 G#4:0.25 E4:0.5 R:2"),
    bar("R:0.25 D#5:0.25 C#5:0.25 A#4:0.25 F#4:0.5 R:2.5"),
    bar("R:0.5 E4:0.25 G#4:0.25 C#5:0.5 R:0.5 E5:0.25 C#5:0.25 B4:0.5 R:1"),
    bar("C5:0.75 R:0.25 G#4:0.25 F#4:0.25 D#4:0.5 R:2"),
]
# サックスの返事（路地の後半: 旋律の休みに答える）
ALLEY_SAX = [R4] * 8 + [bar("R:3 G#4:0.25 B4:0.25 C#5:0.5"), bar("R:3 E5:0.5 C#5:0.5"), bar("R:2.5 B4:0.5 G#4:0.5 E4:0.5"), R4,
                        bar("R:3 F#4:0.25 G#4:0.25 B4:0.5"), bar("R:3 A#4:0.5 C#5:0.5"), R4, bar("R:2 G#4:0.5 B4:0.5 D#5:1")]
# 裏口: サックスの独奏（16小節）
SAX_SOLO = [
    bar("R:0.5 E4:0.25 G#4:0.25 B4:0.5 C#5:0.75 E5:0.25 D#5:0.5 C#5:0.5 B4:0.5"),
    bar("A#4:1.5 R:0.5 C#5:0.333 D#5:0.333 E5:0.334 F#5:0.5 E5:0.5"),
    bar("D#5:0.25 C#5:0.25 B4:0.5 G#4:0.5 R:0.25 G4:0.25 F#4:0.5 E4:0.5 C#4:1"),
    bar("R:0.5 F#4:0.25 A#4:0.25 C#5:0.5 E5:1 D#5:0.25 C#5:0.25 R:1"),
    bar("R:0.25 G#4:0.25 B4:0.5 D#5:0.5 F#5:0.75 E5:0.25 D#5:0.5 B4:0.5 G#4:0.5"),
    bar("F#4:0.5 A#4:0.5 C#5:0.5 D#5:1 R:0.5 C#5:0.5 A#4:0.5"),
    bar("G#4:0.333 C5:0.333 D#5:0.334 F#5:1 G5:0.25 F#5:0.25 D#5:0.5 C5:0.5 R:0.5"),
    bar("C#5:1.5 R:0.5 G#4:0.25 B4:0.25 C#5:0.5 E5:1"),
    bar("D#5:0.25 E5:0.25 G#5:0.5 E5:0.5 C#5:0.5 R:0.25 C#5:0.25 B4:0.25 G#4:0.25 E4:1"),
    bar("R:0.5 A#4:0.25 C#5:0.25 E5:0.5 G5:0.5 F#5:1 R:1"),
    bar("E5:0.25 D#5:0.25 C#5:0.25 B4:0.25 G#4:0.5 E4:0.5 R:0.5 G#4:0.5 B4:0.5 C#5:0.5"),
    bar("E5:2 R:0.5 C#5:0.5 A#4:0.5 F#4:0.5"),
    bar("R:0.25 G#4:0.25 B4:0.25 D#5:0.25 F#5:0.5 G#5:0.5 F#5:0.25 D#5:0.25 B4:0.5 R:1"),
    bar("D#5:0.333 C#5:0.333 A#4:0.334 F#4:0.5 R:0.5 C#5:1 R:1"),
    bar("C5:0.5 D#5:0.5 F#5:0.5 G#5:1.5 R:1"),
    bar("C#5:0.5 B4:0.5 G#4:0.5 E4:0.5 C#4:1 R:1"),
]
# 夜明け: サックスがひとり（看板の旋律の欠片をゆっくり）
DAWN_SAX = [bar("R:1 G#4:1 B4:0.5 C#5:1.5"), bar("R:2 B4:0.5 G#4:0.5 E4:1"), bar("R:1 A4:0.5 C#5:0.5 E5:2"), bar("R:2 C#5:1 B4:1"),
            bar("R:1 G#4:0.5 B4:0.5 C#5:1 E5:1"), bar("C#5:2 R:2"), bar("R:1 E4:0.5 G#4:0.5 B4:2"), bar("A4:2 R:2"),
            bar("R:1 C#5:1 B4:1 G#4:1"), bar("E4:3 R:1"), bar("R:2 G#4:2"), bar("C#4:4")]
# 雨: クリーンの雨粒（高い2音を、やまびこでばらまく）
RAIN = [bar("R:1 G#4:0.5 R:1.5 B4:0.5 R:0.5"), bar("R:0.5 E5:0.5 R:2 D#5:0.5 R:0.5"), bar("R:1.5 C#5:0.5 R:1 G#4:0.5 R:0.5"), bar("R:0.5 B4:0.5 R:2.5 F#4:0.5"),
        bar("R:1 C#5:0.5 R:1.5 E5:0.5 R:0.5"), bar("R:0.5 G#4:0.5 R:2 B4:0.5 R:0.5"), bar("R:1 D#5:0.5 R:1 F#4:0.5 R:1"), bar("R:0.5 B4:0.5 A#4:0.5 F#4:0.5 R:2")]

# ---------------- 組み立て ----------------
P = {k: [] for k in ["riff", "rhy", "rhy_in", "clean", "lead", "sax", "bass", "mute"]}
kit = Kit(BEATS)
RIDE, BELL, CR, CHINA = "D2", "F2", "C2", "B2"
sec_i = {}
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    ch = song.chords[name][i]
    nxt = song.chord_at(idx + 1) if idx + 1 < NB else ch
    last = i == n - 1
    root = root_note(ch)
    riff = rhy = rhy_in = clean = lead = sax = mute = R4
    if name == "rain":
        clean = RAIN[i]
        b = bar(f"C#1:4,") if i < 4 else (bar(f"{root}:4") if not last else bar(f"{root}:2 R:1 C#2:0.5! C#2:0.5!"))
    elif name.startswith("neon"):
        seq = RIFF[ch]; riff = seq[i % len(seq)]
        if name == "neon3":                                  # 傷ついた看板: リフは小節の頭の一撃だけ
            riff = bar(f"{riff.split()[0].split(':')[0]}:2! R:2")
            lead = NEON3_MEL[i]
        elif name == "neon4" and i >= 8:
            lead = NEON4_TAG[i - 8]
            sax = shift_oct(strip_marks(lead), -1)
        else:
            lead = NEON_MEL[i % 8]
            if name in ("neon2", "neon4"): sax = shift_oct(strip_marks(lead), -1) if (name == "neon4" or i >= 4) else R4
        rhy = rhy_in = riff if name != "neon3" else R4
        if name == "neon3": b = bar(f"{root}:2! R:2")
        else: b = unison_low(riff, -1, "B0")
    elif name == "alley":
        riff = STAB[ch]; lead = ALLEY_MEL[i]; sax = ALLEY_SAX[i]
        b = bar(f"{root}:0.5! R:1.5 {root}:0.25 {root}:0.25 R:0.5 {up(root, 1)}:0.5 {fifth_of(ch)}:0.5") if not last else bar(f"{root}:1! R:1 G#1:0.5 G1:0.5 F#1:0.5 E1:0.5")
        mute = bar("R:1 C#2:0.25, R:0.75 C#2:0.25,, R:1.75") if i % 2 == 1 else R4
    elif name == "fight":
        riff = FIGHT[ch] if i < n - 1 else R4                # 最後の1小節は全員の無音
        rhy = rhy_in = riff
        b = unison_low(riff, -1, "B0") if i < n - 1 else R4
    elif name == "backdoor":
        sax = SAX_SOLO[i]
        if i < 8:
            b = bass_walk(ch, nxt, BEATS)
            v = chord_tones(ch, "G3", "E4")[:3]
            clean = bar(f"R:0.5 {v[0]}:0.5 R:1.5 {v[1]}:0.5 R:1")
        else:
            seq = RIFF.get(ch) or [STAB.get(ch, STAB["C#m7"])]
            riff = STAB.get(ch, seq[0]) if i < 12 else seq[0]
            rhy = bar(f"{root_note(ch, 'E2', 'D#3')}:4,")
            b = bass_root8(ch, BEATS, nxt)
    elif name == "dawn":
        sax = DAWN_SAX[i]
        v = chord_tones(ch, "E3", "C#4")[:2]
        clean = bar(f"{v[0]}:2 {v[1]}:2") if i < n - 2 else (bar(f"{v[0]}:4") if i == n - 2 else R4)
        b = bar(f"{root}:4,") if i < 8 else R4
    P["riff"].append(riff); P["rhy"].append(rhy); P["rhy_in"].append(rhy_in if rhy_in != R4 else R4)
    P["clean"].append(clean); P["lead"].append(lead); P["sax"].append(sax); P["bass"].append(b); P["mute"].append(mute)

    # ドラム（ライブラリを使わない場面だけ手で）
    k = s = h = None; tom = cym = None
    if name == "rain":
        if i >= 4: h = "....o.......o..." if i % 2 == 0 else "......o.....o..o"
        if last: k = "X.....X........."; s = "............X.X."; cym = f"R:3 {CR}:1!"
    elif name == "backdoor" and i < 8:
        k = "o.......o......." if i % 2 == 0 else "o.....o........."
        s = ["..o.....o.o.....", "....o.....o..o..", "..o..o....o.....", ".o......o...o..."][i % 4]
        cym = f"{RIDE}:1 {RIDE}:0.75 {RIDE}:0.25 {RIDE}:1 {RIDE}:0.75 {RIDE}:0.25"
    elif name == "dawn":
        if i < 6: cym = f"{RIDE}:2, R:2" if i % 2 == 0 else R4
    elif name == "fight" and last:
        cym = R4
    else:
        k = "X.......X......."; s = "....X.......X..."; h = "x.x.x.x.x.x.x.x."
    kit.add(k, s, h, tom, cym)

FX = []
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    nx = SECS[idx + 1][0] if idx + 1 < NB else ""
    FX.append(bar("R:2 E4:2") if (i == n - 1 and nx in ("neon", "neon4")) else (bar("R:3 C4:1") if (i == n - 1 and nx == "fight") else R4))

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(clean_part(J("clean"), vol=0.08, pan=0.25, role="クリーンの雨粒と和音"))
song.add(lead_part(J("lead")))
song.add(part("アルトサックス", "brass", J("sax"), patch="altoSax", volume=0.16, pan=0.12, reverb=0.3, phrase=8, attack=0.03, release=0.35,
              fx=[{"type": "eq", "low": -2, "mid": 1, "midHz": 1500, "high": 0}, {"type": "delay", "beats": 0.75, "mix": 0.1, "feedback": 0.2}, {"type": "plate", "mix": 0.18}]))
song.add(bass_part(J("bass")))
song.add(bassmute_part(J("mute")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

# 型を切る（ハモリ・最後のサビのオクターブ上・空気の層・自動の表情は、この曲では自分で書いたものだけ）
song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.screams = [int(sum(c for nm_, c in FORM[:4]) + 7)]      # ケンカの8小節目に「きーーーん！」（ここだけ）
song.ref_tone = "dark-electro-rock"
song.dance_air = True                                        # 人間が選んだ④（BBS 寄り＋ダンスの「サー」）

from lm25_plans import apply_plan
apply_plan(song, "01")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-01-rojiura.json"
    song.write(out)
    check_clash(song)
