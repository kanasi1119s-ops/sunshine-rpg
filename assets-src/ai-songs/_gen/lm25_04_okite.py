# ラウド26曲 04「口を縫え」（仮。もとの仮題「沈黙の掟」）。2026-10-24 素材から作り直し
# スタイル: グルーヴメタル（遅く重い、間の多いうねり。刻みすぎない）＋ピアノ。A 和声的短音階・88・4/4
# 物語: 組織の葬儀 → 奥の部屋の密談 → 裏切りが知られる → 処刑 → 沈黙（誰も口をきかない）
# 形: 一筆書き（同じ区間を2度と使わない）。5小節ずつの句（4小節で区切らない）。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ:
#   葬儀（0）: ピアノだけ。左手のオクターブが鐘のように鳴り、右手はまばらな和音
#   密談（1）: ずっと押し殺した緊張。リードは同じ音のささやきと、半音でにじり寄る線。ギターは裏拍の低い突きだけ
#   裏切り（2）: 重いうねりのリフが入る。でもまだ全開にしない。ピアノが G♯ と F でぶつかる
#   処刑（3）: この曲で一度だけの爆発。速いブラストと決め。最後の2小節は全員黙る
#   沈黙（0）: ピアノの単音が数個だけ。ぷつりと切れる
# 旋律の性格: 同じ音のくり返し（ささやき）と半音のにじり寄り。5小節で1つの句。小節の終わりで伸ばさない
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 88, 4
bar = Bars(BEATS)
R4 = bar.rest()

FORM = [("funeral", 10), ("meeting", 30), ("betrayal", 25), ("execution", 15), ("silence", 10)]
MEET = ["Am", "Am", "Dm", "E7", "Am", "Am", "F", "Dm", "E7", "E7"]
CH = {"funeral": ["Am", "Am", "Dm", "E7", "Am", "F", "F", "Dm", "E7", "E7"],
      "meeting": MEET * 3,
      "betrayal": ["Am", "F", "G#dim", "Am", "E7"] * 5,
      "execution": ["A5"] * 6 + ["A#5", "A#5", "A5", "A5", "A#5", "E5", "A5", "A5", "A5"],
      "silence": ["Am"] * 10}
song = Song("沈黙の掟（仮）",
            "仮: ラウド26曲の4曲目（2026-10-24 素材から作り直し）。グルーヴメタル＋ピアノ。A 和声的短音階・88。葬儀・密談・裏切り・処刑・沈黙の一筆書き（くり返しなし）。"
            "5小節の句、旋律は同じ音のささやきと半音のにじり寄り。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 組織の葬儀、奥の部屋の密談、裏切りが知られ、処刑、そして誰も口をきかない。"
song.kinds = {"funeral": "intro", "meeting": "verse", "betrayal": "chorus", "execution": "break", "silence": "outro"}
SECS, NB = song.secs, song.nb

# 密談の旋律（6つの句 × 5小節）
MEET_MEL = [
    bar("R:1 E4:0.5 E4:0.5 E4:0.5 F4:0.5 E4:0.5 R:0.5"), bar("R:0.5 E4:0.5 E4:0.5 D#4:0.5 E4:0.75 C4:0.25 R:1"),
    bar("R:1.5 F4:0.5 F4:0.5 F4:0.5 E4:0.5 D4:0.5"), bar("R:0.5 D4:0.25 E4:0.25 G#4:0.75 F4:0.25 E4:0.5 R:1.5"), bar("A4:0.75 G#4:0.25 E4:0.5 R:2.5"),
    bar("R:1 C5:0.5 C5:0.5 C5:0.5 B4:0.5 A4:0.5 R:0.5"), bar("R:0.5 A4:0.5 A4:0.5 G#4:0.5 A4:0.75 E4:0.25 R:1"),
    bar("R:1.5 A4:0.5 C5:0.5 A4:0.5 F4:0.5 D4:0.5"), bar("R:0.5 D4:0.5 F4:0.5 G#4:0.5 B4:0.75 A4:0.25 R:1"), bar("G#4:0.5 E4:0.5 R:3"),
    bar("R:0.5 E4:0.25 E4:0.25 E4:0.5 E4:0.5 F4:0.5 G#4:0.5 A4:0.5 R:0.5"), bar("R:1 A4:0.25 G#4:0.25 F4:0.5 E4:0.5 R:1.5"),
    bar("R:0.5 F4:0.5 F4:0.25 F4:0.25 A4:0.5 R:0.5 D5:0.5 C5:0.5 R:0.5"), bar("R:1 B4:0.5 G#4:0.5 E4:0.5 D4:0.5 R:1"), bar("C4:0.5 B3:0.5 R:3"),
    bar("R:1 A4:0.5 A4:0.5 B4:0.5 C5:0.5 B4:0.5 R:0.5"), bar("R:0.5 A4:0.5 G#4:0.5 A4:0.5 E5:0.75 C5:0.25 R:1"),
    bar("R:1.5 F4:0.5 A4:0.5 C5:0.5 D5:0.5 C5:0.5"), bar("R:0.5 B4:0.5 D5:0.5 B4:0.5 G#4:0.75 F4:0.25 R:1"), bar("E4:0.75 D#4:0.25 E4:0.5 R:2.5"),
    bar("R:1 E5:0.5 E5:0.5 E5:0.5 F5:0.5 E5:0.5 R:0.5"), bar("R:0.5 C5:0.5 C5:0.5 B4:0.5 C5:0.75 A4:0.25 R:1"),
    bar("R:1.5 D5:0.5 D5:0.5 D5:0.5 C5:0.5 A4:0.5"), bar("R:0.5 G#4:0.25 A4:0.25 B4:0.75 D5:0.25 C5:0.5 R:1.5"), bar("B4:0.75 G#4:0.25 E4:0.5 R:2.5"),
    bar("R:1 A4:0.25 A4:0.25 A4:0.5 G#4:0.5 A4:0.5 R:1"), bar("R:0.5 C5:0.5 B4:0.5 A4:0.5 R:2"),
    bar("R:1 F4:0.5 E4:0.5 D4:0.5 C4:0.5 R:1"), bar("R:0.5 B3:0.5 D4:0.5 F4:0.5 G#4:0.5 R:1.5"), bar("R:4"),
]
# 裏切りの旋律（5つの句 × 5小節）: 同じ動機を上へ押し上げ、拍の裏から食う
BETRAY_MEL = [
    bar("R:0.5 E5:0.5 E5:0.25 E5:0.25 D5:0.5 C5:0.5 B4:0.5 A4:0.5 R:0.5"), bar("R:0.5 C5:0.25 C5:0.25 A4:0.5 F4:0.5 R:2"),
    bar("R:0.5 B4:0.5 D5:0.5 F5:0.5 E5:0.5 D5:0.5 R:1"), bar("R:0.5 C5:0.5 C5:0.5 B4:0.5 C5:0.5 E5:0.5 R:1"), bar("D5:0.5 B4:0.5 G#4:0.5 R:2.5"),
    bar("R:0.5 E5:0.5 F5:0.25 E5:0.25 C5:0.5 A4:0.5 C5:0.5 E5:0.5 R:0.5"), bar("R:0.5 F5:0.5 E5:0.5 C5:0.5 A4:0.5 R:1.5"),
    bar("R:1 D5:0.25 F5:0.25 G#4:0.5 B4:0.5 D5:0.5 R:1"), bar("R:0.5 E5:0.5 E5:0.5 E5:0.5 D#5:0.5 E5:0.5 R:1"), bar("R:0.5 B4:0.5 G#4:0.5 E4:0.5 R:2"),
    bar("A4:0.25 C5:0.25 E5:0.5 A4:0.25 C5:0.25 E5:0.5 R:0.5 D5:0.5 C5:0.5 R:0.5"), bar("R:0.5 C5:0.5 A4:0.5 F4:0.5 A4:0.5 R:1.5"),
    bar("R:0.5 F5:0.5 D5:0.5 B4:0.5 G#4:0.5 F4:0.5 R:1"), bar("R:1 E5:0.5 C5:0.5 A4:0.5 E4:0.5 R:1"), bar("B4:0.5 G#4:0.5 E4:0.5 R:2.5"),
    bar("R:0.5 A4:0.5 B4:0.5 C5:0.5 D5:0.5 E5:0.5 F5:0.5 R:0.5"), bar("R:0.5 F5:0.5 E5:0.5 C5:0.5 R:2"),
    bar("R:0.5 D5:0.5 F5:0.5 D5:0.5 B4:0.5 D5:0.5 R:1"), bar("R:0.5 C5:0.5 E5:0.5 C5:0.5 A4:0.5 E4:0.5 R:1"), bar("R:0.5 G#4:0.5 B4:0.5 E5:0.5 R:2"),
    bar("R:1 E5:0.5 E5:0.5 E5:0.5 E5:0.5 R:1"), bar("R:1 C5:0.5 C5:0.5 C5:0.5 R:1.5"),
    bar("R:1 B4:0.5 B4:0.5 B4:0.5 R:1.5"), bar("R:1 A4:0.5 A4:0.5 R:2"), bar("G#4:0.5 R:3.5"),
]
# 葬儀の鐘（左手のオクターブ）と、右手のまばらな和音
VOICE = {"Am": ["C4", "E4", "A4"], "Dm": ["D4", "F4", "A4"], "E7": ["D4", "G#4", "B4"], "F": ["C4", "F4", "A4"], "G#dim": ["D4", "F4", "B4"]}

P = {k: [] for k in ["riff", "rhy", "lead", "pl", "pr", "bass", "mute"]}
kit = Kit(BEATS)
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]; last = i == n - 1
    riff = rhy = lead = pl = pr = mute = R4
    root = root_note(ch); lo = root_note(ch, "E1", "D#2")
    if name == "funeral":
        pl = bar(f"{lo}:2! {up(lo, 1)}:2,") if i % 2 == 0 else bar(f"{up(lo, 1)}:3, R:1")
        v = VOICE.get(ch, VOICE["Am"])
        pr = bar(f"R:1 {v[0]}:0.5, {v[1]}:0.5, {v[2]}:2,") if i % 2 == 1 else R4
        b = R4
    elif name == "meeting":
        lead = MEET_MEL[i]
        riff = bar(f"R:0.5 {lo}:0.25, R:1.25 {lo}:0.25, R:1.75")    # 裏拍の低い突きだけ
        pl = bar(f"{lo}:4,") if i % 5 == 0 else R4
        b = bar(f"{root}:1.5, R:0.5 {root}:0.5, R:1.5") if i % 5 != 4 else bar(f"{root}:1 {tr(root, -1)}:1 R:2")
    elif name == "betrayal":
        g = root_note(ch, "F#1", "F2") if ch != "G#dim" else "G#1"
        riff = rhy = bar(f"{g}:0.75! {g}:0.25 R:0.5 {g}:0.25 {tr(g, 1)}:0.25 R:0.5 {up(g, 1)}:0.5! {tr(g, 11)}:0.25 {tr(g, 10)}:0.25 {g}:0.5") if i % 5 != 4 \
            else bar(f"{g}:1! R:0.5 {g}:0.5! R:2")
        lead = BETRAY_MEL[i]
        v = VOICE.get(ch, VOICE["Am"])
        pr = bar(f"{v[0]}:0.5! {v[1]}:0.5 {v[2]}:0.5 R:2.5") if i % 5 in (0, 2) else (bar("R:2 G#5:0.5, F5:0.5, R:1") if i % 5 == 3 else R4)
        pl = bar(f"{lo}:2 R:2") if i % 5 == 0 else R4
        b = unison_low(riff, -1, "B0")
        mute = bar("R:1.5 A1:0.25, R:2.25") if i % 2 else R4
    elif name == "execution":
        g = {"A5": "A1", "A#5": "A#1", "E5": "E2"}[ch]
        if i < 6: riff = bar(" ".join([f"{g}:0.25!" if j % 4 == 0 else f"{g}:0.25" for j in range(16)]))
        elif i < 13: riff = bar(f"{g}:0.75! {g}:0.75! {g}:0.5! R:0.5 {g}:0.5! {g}:0.5! R:0.5")
        else: riff = R4                                            # 全員黙る
        rhy = riff
        b = unison_low(riff, -1, "B0")
    else:   # silence
        pr = {0: bar("R:2 E5:2,"), 2: bar("R:1 C5:3,"), 5: bar("R:2 B4:2,"), 7: bar("A4:4,")}.get(i, R4)
        b = R4
    P["riff"].append(riff); P["rhy"].append(rhy); P["lead"].append(lead); P["pl"].append(pl); P["pr"].append(pr); P["bass"].append(b); P["mute"].append(mute)
    kit.add("X.......X.......", "........X.......", "x...x...x...x...")

J = lambda k: " ".join(P[k])
PIANO = dict(volume=0.13, reverb=0.3, fx=[{"type": "eq", "low": -2, "mid": 0, "midHz": 800, "high": 1}, {"type": "plate", "mix": 0.15}])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy")))
song.add(lead_part(J("lead")))
song.add(part("ピアノ（左手）", "piano", J("pl"), pan=-0.1, **{**PIANO, "volume": 0.14}))
song.add(part("ピアノ（右手）", "piano", J("pr"), pan=0.05, **PIANO))
song.add(bass_part(J("bass")))
song.add(bassmute_part(J("mute")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.screams = [10 + 30 + 25 + 5]           # 処刑の6小節目（ブラストの終わり）に一度だけ
song.ref_tone = "bright-nu-wall"

from lm25_plans import apply_plan
apply_plan(song, "04")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-04-okite.json"
    song.write(out)
    check_clash(song)
