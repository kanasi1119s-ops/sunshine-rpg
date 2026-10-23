# ラウド26曲 06「偶像崩落」（仮。もとの仮題「鐘と偶像」）。2026-10-24 素材から作り直し
# スタイル: シンフォニックなドゥーム（遅く重い行進とパイプオルガン）→ 崩落でブラストビートの倍の速さ。B 短調・72 → 144 → 72・6/4（3+3）
# 物語: 巡礼者の行列が偶像の前へ進む。説教。もう一度の行進。ひびが入り、偶像が崩れ落ちる。瓦礫の中にオルガンの1音だけ。
# 形: 前半は聖歌の行進（遅い）、後半の崩落で倍の速さ、最後は瓦礫。サビという区切りなし。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ:
#   鐘（0）: オルガンの和音だけ
#   行進（2）: 荘厳で重い。速くない。大きいけれど、全開ではない（行列は叫ばない）
#   説教（1）: オルガンとベースと、ささやくリード
#   二度目の行進（2）: 聖歌を高い所で
#   ひび（2→3）: リフがつかえ、オルガンが濁る
#   崩落（3）: 144 の倍の速さ、ブラスト。聖歌の欠片が速い刻みに砕ける
#   瓦礫（0）: オルガンの B の1音だけ
# 旋律の性格: 聖歌（順に進む音・同じ音を歌い直す・3+3 の区切りに沿う）。句の終わりは小節の真ん中に置き、小節の終わりは次へ動く
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 72, 6
bar = Bars(BEATS)
R6 = bar.rest()

HYMN = ["Bm", "G", "D", "A", "Bm", "Em", "F#", "Bm", "G", "D", "Em", "Bm", "G", "A", "F#sus4", "F#"]
FORM = [("bells", 4), ("procession", 16), ("sermon", 8), ("procession2", 12), ("crack", 4), ("collapse", 12), ("rubble", 4)]
CH = {"bells": ["Bm", "G", "Bm", "F#"], "procession": HYMN, "sermon": ["Bm", "Em", "Bm", "F#", "G", "Em", "F#sus4", "F#"],
      "procession2": HYMN[:12], "crack": ["Bm", "C", "Bm", "C"],
      "collapse": ["Bm", "Bm", "C", "C", "Bm", "Bm", "G", "F#", "Bm", "C", "Bm", "F#"], "rubble": ["Bm"] * 4}
song = Song("鐘と偶像（仮）",
            "仮: ラウド26曲の6曲目（2026-10-24 素材から作り直し）。シンフォニックなドゥーム＋パイプオルガン。B 短調・72・6/4（3+3）。聖歌の行進、説教、二度目の行進、"
            "ひび、144 の倍の速さで崩落、瓦礫にオルガンの1音。旋律は聖歌のように順に進み、同じ音を歌い直す。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 巡礼の行列が偶像の前へ進み、説教のあと、偶像にひびが入って崩れ落ち、瓦礫の中にオルガンの1音だけが残る。"
song.kinds = {"bells": "intro", "procession": "chorus", "sermon": "verse", "procession2": "chorus", "crack": "pre", "collapse": "break", "rubble": "outro"}
SECS, NB = song.secs, song.nb

# 聖歌（16小節）。3+3 の区切りに沿って、句の終わりを小節の真ん中に置く
HYMN_MEL = [
    bar("B4:2 C#5:1 D5:1 C#5:1 B4:1"), bar("B4:1 B4:1 D5:1 G4:2 A4:1"),
    bar("A4:2 F#4:1 A4:1 B4:1 D5:1"), bar("C#5:3 E5:1 C#5:1 A4:1"),
    bar("B4:2 C#5:1 D5:1 E5:1 F#5:1"), bar("E5:1 D5:1 E5:1 B4:2 G4:1"),
    bar("A#4:2 C#5:1 E5:2 D5:0.5 C#5:0.5"), bar("B4:3 R:1 F#4:1 A4:1"),
    bar("G4:2 A4:1 B4:1 D5:1 B4:1"), bar("A4:1 A4:1 F#4:1 D5:2 E5:1"),
    bar("B4:2 G4:1 E4:1 G4:1 B4:1"), bar("D5:3 C#5:1 B4:1 F#4:1"),
    bar("G4:1 B4:1 D5:1 E5:2 D5:1"), bar("C#5:1 A4:1 C#5:1 E5:2 C#5:1"),
    bar("B4:2 C#5:1 E5:1 C#5:1 B4:1"), bar("A#4:3 R:3"),
]
# 二度目の行進: 1オクターブ上ではなく、3度上の別の線（同じ聖歌の続きのように）
HYMN2 = [
    bar("D5:2 E5:1 F#5:1 E5:1 D5:1"), bar("D5:1 D5:1 B4:1 B4:2 A4:1"),
    bar("D5:2 A4:1 D5:1 E5:1 F#5:1"), bar("E5:3 C#5:1 E5:1 C#5:1"),
    bar("D5:2 E5:1 F#5:1 F#5:1 D5:1"), bar("B4:1 B4:1 C#5:1 E5:2 D5:1"),
    bar("C#5:2 E5:1 F#5:2 E5:0.5 C#5:0.5"), bar("D5:3 R:1 B4:1 D5:1"),
    bar("B4:2 D5:1 E5:1 D5:1 B4:1"), bar("D5:1 D5:1 A4:1 F#5:2 E5:1"),
    bar("E5:2 B4:1 G4:1 B4:1 E5:1"), bar("F#5:3 R:3"),
]
# 説教: ささやき（同じ音の8分）
SERMON = [bar("R:3 F#4:0.5 F#4:0.5 F#4:0.5 G4:0.5 F#4:1"), bar("R:3 G4:0.5 G4:0.5 B4:0.5 G4:0.5 E4:1"),
          bar("R:3 B4:0.5 B4:0.5 B4:0.5 C#5:0.5 D5:1"), bar("C#5:1 A#4:1 R:4"),
          bar("R:3 D5:0.5 D5:0.5 D5:0.5 B4:0.5 G4:1"), bar("R:3 E5:0.5 E5:0.5 D5:0.5 B4:0.5 G4:1"),
          bar("R:3 C#5:0.5 B4:0.5 A4:0.5 B4:0.5 C#5:1"), bar("A#4:2 R:4")]
# 崩落: 聖歌の欠片が16分に砕ける
def shard(i):
    seeds = [("B4", "C#5", "D5"), ("D5", "C5", "B4"), ("E5", "D5", "C#5"), ("F#5", "E5", "D5")]
    a, b, c = seeds[i % 4]
    pats = [f"{a}:0.25! {b}:0.25 {c}:0.25 {b}:0.25 " * 3 + "R:3", f"R:3 " + f"{c}:0.25! {b}:0.25 {a}:0.25 {b}:0.25 " * 3,
            f"{a}:1.5! {b}:0.25 {c}:0.25 R:1 {a}:0.25 {b}:0.25 {c}:0.25 {a}:0.25 R:2", f"{c}:0.5! {b}:0.5 {a}:0.5 R:1.5 {a}:0.5 {b}:0.5 {c}:0.5 R:1.5"]
    return bar(pats[i % 4].strip())


VOICE = {"Bm": ["F#3", "B3", "D4"], "G": ["G3", "B3", "D4"], "D": ["F#3", "A3", "D4"], "A": ["E3", "A3", "C#4"], "Em": ["G3", "B3", "E4"],
         "F#": ["F#3", "A#3", "C#4"], "F#sus4": ["F#3", "B3", "C#4"], "C": ["G3", "C4", "E4"]}
LOW = {"Bm": "B1", "G": "G1", "D": "D2", "A": "A1", "Em": "E2", "F#": "F#1", "F#sus4": "F#1", "C": "C2"}

P = {k: [] for k in ["riff", "rhy", "lead", "o0", "o1", "o2", "bass"]}
kit = Kit(BEATS)
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]
    riff = rhy = lead = R6
    v = VOICE[ch]; g = LOW[ch]; root = root_note(ch)
    org = [f"{x}:6" for x in v]
    if name == "bells":
        b = R6
    elif name in ("procession", "procession2"):
        riff = rhy = bar(f"{g}:2! {g}:1 {tr(g, 7)}:2! {g}:1")               # 行進: 3+3 の頭を重く
        lead = (HYMN_MEL if name == "procession" else HYMN2)[i]
        b = bar(f"{root}:2! {root}:1 {fifth_of(ch)}:2 {root}:1")
    elif name == "sermon":
        lead = SERMON[i]; b = bar(f"{root}:6,")
        if i % 2: org = [f"{x}:3," for x in v]; org = [o + " R:3" for o in org]
    elif name == "crack":
        riff = rhy = bar(f"{g}:1.5! R:0.5 {g}:0.5! {g}:0.5 R:1 {tr(g, 1)}:1! R:1") if ch == "Bm" else bar(f"{g}:0.75! {g}:0.75! R:1.5 {g}:3!")
        b = unison_low(riff, -1, "B0")
    elif name == "collapse":
        riff = rhy = bar(" ".join(f"{g}:0.25{'!' if j % 6 == 0 else ''}" for j in range(24)))
        lead = shard(i)
        b = bar(" ".join(f"{root}:0.5{'!' if j % 3 == 0 else ''}" for j in range(12)))
        org = [f"{x}:6" for x in v] if i % 2 == 0 else ["R:6"] * 3
    else:   # rubble
        org = ["B3:6," if i < 3 else "R:6", "R:6", "R:6"]
        b = R6
    P["riff"].append(riff); P["rhy"].append(rhy); P["lead"].append(lead); P["bass"].append(b)
    for j in range(3): P[f"o{j}"].append(bar(org[j]))
    kit.add("X" + "." * 23, "." * 12 + "X" + "." * 11, "".join("x" if j % 4 == 0 else "." for j in range(24)))

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy")))
song.add(lead_part(J("lead")))
song.add([part(f"オルガン（{['上', '中', '下'][j]}）", "keys", J(f"o{j}"), patch="churchOrgan", volume=0.07, pan=[-0.25, 0.25, 0][j], reverb=0.4, attack=0.06, release=0.6,
               fx=[{"type": "eq", "low": -4, "mid": -1, "midHz": 600, "high": 0}, {"type": "reverb", "mix": 0.25}]) for j in range(3)])
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.screams = [4 + 16 + 8 + 12 + 3]          # ひびの最後（崩れる直前）に一度だけ
song.ref_tone = "wide-dark-wall"

from lm25_plans import apply_plan
apply_plan(song, "06")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-06-kane.json"
    song.write(out)
    check_clash(song)
