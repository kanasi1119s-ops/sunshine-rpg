# ラウド26曲 22「Survivors Sing Off-Key」（仮。もとの仮題「難破船の歌」）。2026-10-24 素材から作り直し
# スタイル: ストーナー／スラッジ（重く揺れる 6拍子の舟歌、嵐では 2+2+2 のヘミオラ）＋フィドル。E 短調・96・6/4
# 物語: 甲板で船乗りたちが陽気に歌う → 嵐 → 難破（ほぼ無音、低い一撃だけ）→ 生き残った者が、調子はずれの小さな声で同じ歌を歌う。
# 形: 舟歌 → 嵐 → 難破 → 生き残りの歌。最後は小さく弱いまま終わる（盛り返さない）。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ:
#   甲板（2）: 陽気。重いギターが 3+3 で揺れ、フィドルが舟歌を
#   ジグ（2）: フィドルが速く回る
#   嵐（3）: 2+2+2 のヘミオラで拍がひっくり返る。いちばん大きい
#   難破（0）: ほぼ無音。低い一撃と、きしむ音
#   生き残り（0→1）: フィドルが同じ舟歌を、ずり上がる音（調子はずれ）で弱々しく。クリーンのギターがあとから寄りそう
# 旋律の性格: 舟歌の跳ねる 3+3（付点のゆれ）。嵐は 2+2+2。生き残りは同じ舟歌を、音の入りがずり上がる弱い声で
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 96, 6
bar = Bars(BEATS)
R6 = bar.rest()

SHANTY_CH = ["Em", "Em", "G", "D", "Em", "C", "D", "Em"]
FORM = [("deck", 16), ("jig", 8), ("storm", 20), ("wreck", 4), ("survivors", 16), ("last", 4)]
CH = {"deck": SHANTY_CH * 2, "jig": ["Em", "D", "Em", "D", "C", "D", "Em", "Em"], "storm": ["Em", "C", "D", "B7"] * 5,
      "wreck": ["Em"] * 4, "survivors": SHANTY_CH * 2, "last": ["Em"] * 4}
song = Song("難破船の歌（仮）",
            "仮: ラウド26曲の22曲目（2026-10-24 素材から作り直し）。ストーナー／スラッジの舟歌＋フィドル。E 短調・96・6/4。甲板の陽気な舟歌、フィドルのジグ、"
            "2+2+2 の嵐、難破の無音、生き残った者が調子はずれの小さな声で同じ歌を歌う。最後まで小さいまま。自作",
            BPM, BEATS, FORM, CH)
song.flags = "--space hall --space-wet 0.15"
song.desc += " 物語: 陽気な舟歌、嵐、難破、そして生き残った者が調子はずれの声で同じ歌を歌う。"
song.kinds = {"deck": "verse", "jig": "interlude", "storm": "chorus", "wreck": "break", "survivors": "bridge", "last": "outro"}
SECS, NB = song.secs, song.nb

# 舟歌（8小節。3+3 の付点のゆれ）
SHANTY = ["E5:1.5 D5:0.5 B4:1 G4:1.5 A4:0.5 B4:1", "E4:1.5 F#4:0.5 G4:1 B4:2 R:1", "D5:1.5 C5:0.5 B4:1 G4:1.5 B4:0.5 D5:1", "A4:1.5 F#4:0.5 D4:1 A4:2 R:1",
          "B4:1.5 C5:0.5 B4:1 G4:1.5 E4:0.5 G4:1", "E5:1.5 D5:0.5 C5:1 G4:2 R:1", "F#4:1.5 A4:0.5 D5:1 B4:1.5 A4:0.5 F#4:1", "E4:2 R:1 B4:0.5 A4:0.5 G4:1 F#4:1"]
JIG = ["E5:0.5 B4:0.5 G4:0.5 E5:0.5 B4:0.5 G4:0.5 D5:0.5 A4:0.5 F#4:0.5 D5:0.5 A4:0.5 F#4:0.5", "E5:0.5 F#5:0.5 E5:0.5 D5:0.5 B4:0.5 A4:0.5 B4:1.5 R:1.5",
       "G4:0.5 B4:0.5 E5:0.5 G4:0.5 B4:0.5 E5:0.5 F#4:0.5 A4:0.5 D5:0.5 F#4:0.5 A4:0.5 D5:0.5", "E5:0.5 D5:0.5 C5:0.5 B4:0.5 A4:0.5 G4:0.5 B4:1.5 R:1.5"]
# 嵐: 2+2+2 で叫ぶ（2拍ずつ）
STORM = ["E5:1 D5:1 B4:2 G4:1 E5:1", "C5:2 B4:1 G4:1 E4:2", "D5:0.5 D5:0.5 A4:1 F#4:2 R:2", "D#5:1 B4:1 F#4:1 D#4:1 B4:2",
         "E5:2 R:1 E5:0.5 D5:0.5 B4:2", "G4:1 C5:1 E5:2 C5:1 G4:1", "A4:1 D5:1 F#4:1 A4:1 D5:1 R:1", "B4:2 F#4:2 D#4:1 R:1"]

LOW = {"Em": "E2", "G": "G1", "D": "D2", "C": "C2", "B7": "B1"}
P = {k: [] for k in ["riff", "rhy", "lead", "clean", "fid", "bass"]}
kit = Kit(BEATS)
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]
    riff = rhy = lead = clean = fid = R6
    g = LOW[ch]; root = root_note(ch)
    sway = bar(f"{g}:1.5! {g}:0.5 {tr(g, 7)}:1 {g}:1.5! {tr(g, 3 if ch.endswith('m') else 4)}:0.5 {g}:1")
    if name == "deck":
        riff = rhy = sway if i >= 4 else bar(f"{g}:3! {g}:3")
        fid = bar(SHANTY[i % 8])
        lead = bar(strip_marks(SHANTY[i % 8])) if i >= 8 else R6
        b = bar(f"{root}:1.5 {root}:1.5 {fifth_of(ch)}:1.5 {root}:1.5")
    elif name == "jig":
        fid = bar(JIG[i % 4]); riff = rhy = sway
        b = bar(f"{root}:1.5 {fifth_of(ch)}:1.5 {root}:1.5 {fifth_of(ch)}:1.5")
    elif name == "storm":
        riff = rhy = bar(f"{g}:1! {g}:1 {tr(g, 7)}:1! {g}:1 {tr(g, 3 if ch.endswith('m') else 4)}:1! {g}:1")
        lead = bar(STORM[i % 8]) if i >= 4 else R6
        fid = bar(" ".join(f"{chord_tones(ch, 'E5', 'E6')[0]}:0.25" for _ in range(24))) if i >= 12 else R6
        b = unison_low(riff, -1, "B0")
    elif name == "wreck":
        riff = bar("E2:6!") if i == 0 else R6
        b = bar("E1:6!") if i == 0 else R6
        fid = bar("R:3 F5:0.25 E5:2.75,") if i == 2 else R6          # きしむ音
    elif name == "survivors":
        # 調子はずれ: 音の入りを下からずり上げ（/）、弱く（,）
        fid = bar(" ".join(x if x.startswith("R") else x + "/," for x in SHANTY[i % 8].split()))
        if i >= 8:
            tones = (chord_tones(ch, "E3", "E4") * 2)[:3]
            clean = bar(f"{tones[0]}:3 {tones[1]}:1.5 {tones[2]}:1.5")
        b = bar(f"{root}:6,") if i >= 12 else R6
    else:   # last
        fid = bar("E4:6/,") if i == 0 else R6
        b = R6
    P["riff"].append(riff); P["rhy"].append(rhy); P["lead"].append(lead); P["clean"].append(clean); P["fid"].append(fid); P["bass"].append(b)
    kit.add("X" + "." * 11 + "X" + "." * 11, "." * 6 + "X" + "." * 11 + "X" + "." * 5, "".join("x" if j % 2 == 0 else "." for j in range(24)))

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy")))
song.add(lead_part(J("lead")))
song.add(clean_part(J("clean"), vol=0.08, pan=0.25, role="クリーンの和音（生き残り）"))
song.add(part("フィドル", "fiddle", J("fid"), volume=0.16, pan=-0.15, reverb=0.5, gainDb=3, bright=-0.15, attack=0.2, release=0.7,
              doubleDetune={"cents": 5, "spread": 0.3}, phrase=8,
              fx=[{"type": "eq", "low": 2, "mid": -2.5, "midHz": 2800, "high": 0}, {"type": "delay", "beats": 1, "mix": 0.08, "feedback": 0.2},
                  {"type": "reverb", "mix": 0.22}, {"type": "plate", "mix": 0.12}]))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.ref_tone = "glossy-jrock"

from lm25_plans import apply_plan
apply_plan(song, "22")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-22-nanpasen.json"
    song.write(out)
    check_clash(song)
