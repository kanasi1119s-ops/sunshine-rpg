# ラウド26曲 23「Anthem for Ashes」（仮。もとの仮題「焼け野原の国歌」）。2026-10-24 素材から作り直し
# スタイル: ヘヴィな葬送行進（スネアの行進が主役のハーフタイム。速くしない）＋ピアノ。C 短調 → E♭ 長調・80・4/4
# 物語: 焼け野原に残ったピアノが、こわれかけた国歌を弾く。葬列が来るたびに、国歌は違う形に壊れていく。最後に一度だけ、全員で国歌を歌いきる。
# 形: 変奏（同じ国歌が6回現れ、毎回壊れ方が違う: 欠ける・前半だけ・短調で重く・決めの一撃だけ・灰の中のピアノ・全員で長調）。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ:
#   焼け跡のピアノ（0）: 国歌の音がところどころ欠ける
#   葬列（1）: スネアの行進と低いリフ。リードは国歌の前半だけ（後半は黙る）
#   短調の国歌（2）: 重いハーフタイムで、国歌を最後まで。でも抑えて
#   砕けた国歌（2→3）: 国歌のリズムだけが全員の決めの一撃になる
#   灰の中（0）: ピアノだけ、ゆっくり
#   国歌（3）: この曲で一度だけ、全員で長調の国歌を歌いきる
#   最後（0）: ピアノの最後の音
# 旋律の性格: 国歌（付点のリズムと、4度の上行）。変奏ごとに欠け方・リズムの崩れ方が違う
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 80, 4
bar = Bars(BEATS)
R4 = bar.rest()

ANTHEM = ["A#3:0.75 A#3:0.25 D#4:1.5 F4:0.5 G4:1", "G4:0.75 F4:0.25 D#4:1 A#3:1 R:1", "C4:0.75 C4:0.25 F4:1.5 G4:0.5 G#4:1", "G4:1.5 D#4:0.5 F4:1 R:1",
          "A#4:0.75 A#4:0.25 D#5:1.5 D5:0.5 C5:1", "A#4:0.75 G#4:0.25 G4:1 D#4:1 R:1", "G#4:0.75 G4:0.25 F4:1 A#4:0.75 G#4:0.25 G4:1", "F4:1.5 G4:0.5 D#4:1 R:1"]
MINOR_CH = ["Cm", "Cm", "Fm", "Cm", "D#", "Cm", "Fm", "G7"]
MAJOR_CH = ["D#", "D#", "Fm", "Cm", "D#", "Cm", "Fm", "D#"]
FORM = [("ruin", 8), ("march", 16), ("dark", 16), ("shards", 12), ("ash", 8), ("anthem", 20), ("last", 4)]
CH = {"ruin": MINOR_CH, "march": MINOR_CH * 2, "dark": MINOR_CH * 2, "shards": (MINOR_CH * 2)[:12], "ash": MINOR_CH,
      "anthem": MAJOR_CH * 2 + ["Fm", "A#", "D#", "D#"], "last": ["D#", "D#", "D#", "D#"]}
song = Song("焼け野原の国歌（仮）",
            "仮: ラウド26曲の23曲目（2026-10-24 素材から作り直し）。ヘヴィな葬送行進＋ピアノ。C 短調 → E♭ 長調・80。同じ国歌が6回、毎回ちがう形に壊れて現れ"
            "（欠ける・前半だけ・短調で重く・決めの一撃だけ・灰の中のピアノ）、最後に一度だけ全員で長調の国歌を歌いきる。自作",
            BPM, BEATS, FORM, CH)
song.flags = "--space hall --space-wet 0.12"
song.desc += " 物語: 焼け野原に残ったピアノと、こわれていく国歌。最後に一度だけ全員で歌いきる。"
song.kinds = {"ruin": "intro", "march": "verse", "dark": "pre", "shards": "break", "ash": "bridge", "anthem": "chorus", "last": "outro"}
SECS, NB = song.secs, song.nb


def broken(b_, drop):
    """国歌の小節から、drop 番目の音を休みに（欠ける）"""
    t = b_.split()
    idx = [k for k, x in enumerate(t) if not x.startswith("R")]
    for k in drop:
        if k < len(idx): j = idx[k]; t[j] = "R:" + t[j].split(":")[1]
    return bar(" ".join(t))


def rhythm_only(b_, note):
    """国歌のリズムだけを、決めの一撃にする"""
    return bar(" ".join(x if x.startswith("R") else f"{note}:{tok_beats(x):g}!" for x in b_.split()))


LOW = {"Cm": "C2", "G#": "G#1", "Fm": "F2", "G": "G1", "G7": "G1", "D#": "D#2", "A#": "A#1"}
P = {k: [] for k in ["riff", "rhy", "lead", "pr", "pl", "bass"]}
kit = Kit(BEATS)
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]
    riff = rhy = lead = pr = pl = R4
    g = LOW[ch]; root = root_note(ch); a = ANTHEM[i % 8]
    if name == "ruin":
        pr = broken(a, [1] if i % 2 == 0 else [0, 2]); pl = bar(f"{up(root, 1)}:4,")
        b = R4
    elif name == "march":
        riff = bar(f"{g}:2! R:1 {g}:0.5 {g}:0.5")
        lead = bar(a) if i % 8 < 4 else R4                   # 国歌の前半だけ
        pl = bar(f"{up(root, 1)}:2, R:2") if i % 2 == 0 else R4
        b = bar(f"{root}:2 R:1 {root}:0.5 {root}:0.5")
    elif name == "dark":
        riff = rhy = bar(f"{g}:3! {tr(g, 7)}:1")
        lead = bar(a)
        b = bar(f"{root}:3 {fifth_of(ch)}:1")
    elif name == "shards":
        riff = rhy = rhythm_only(a, g)
        lead = R4
        pr = broken(a, [0, 1, 2]) if i % 3 == 2 else R4
        b = unison_low(riff, -1, "B0")
    elif name == "ash":
        pr = bar(" ".join(x if x.startswith("R") else x.split(":")[0] + ":" + x.split(":")[1] for x in a.split()))
        pl = bar(f"{up(root, 1)}:4,")
        b = R4
    elif name == "anthem":
        aa = ANTHEM[i % 8] if i < 16 else ["G#4:0.75 G4:0.25 F4:1 A#4:0.75 G#4:0.25 G4:1", "F4:1.5 G4:0.5 A#4:1 R:1", "D#5:3 R:1", "D#4:2 R:2"][i - 16]
        lead = bar(aa); pr = bar(strip_marks(aa))
        riff = rhy = bar(f"{g}:1.5! {g}:0.5 {tr(g, 7)}:1 {g}:1")
        pl = bar(f"{up(root, 1)}:4")
        b = bar(f"{root}:1.5 {root}:0.5 {fifth_of(ch)}:1 {root}:1")
    else:   # last
        pr = bar("D#5:4,") if i == 0 else (bar("G4:2, A#4:2,") if i == 1 else R4)
        b = R4
    P["riff"].append(riff); P["rhy"].append(rhy); P["lead"].append(lead); P["pr"].append(pr); P["pl"].append(pl); P["bass"].append(b)
    if name == "march":    # スネアの行進（主役）
        kit.add("X.......X.......", "X..oX.o.X.ooX.o." if i % 4 != 3 else "X..oX.o.XoXoXXXX", "................")
    else:
        kit.add("X.......X.......", "........X.......", "x...x...x...x...")

J = lambda k: " ".join(P[k])
PIANO = dict(volume=0.14, reverb=0.35, fx=[{"type": "eq", "low": -2, "mid": 0, "midHz": 800, "high": 1}, {"type": "plate", "mix": 0.18}])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy")))
song.add(lead_part(J("lead")))
song.add(part("ピアノ（右手・国歌）", "piano", J("pr"), pan=0.05, **PIANO))
song.add(part("ピアノ（左手）", "piano", J("pl"), pan=-0.1, **{**PIANO, "volume": 0.13}))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.ref_tone = "wide-dark-wall"

from lm25_plans import apply_plan
apply_plan(song, "23")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-23-kokka.json"
    song.write(out)
    check_clash(song)
