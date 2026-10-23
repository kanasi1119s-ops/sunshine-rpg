# ラウド26曲 10「Airmail to Nowhere」（仮。もとの仮題「成層圏の手紙」）。2026-10-24 素材から作り直し
# スタイル: ポストハードコア（語りかけるクリーンと、感情が決壊する歪みの往復）＋馬頭琴風のチェロ。A ミクソリディアン・100・4/4
# 物語: 宛先のない航空便。空の上の誰かへの手紙を読む。読み上げる「いま」と、思い出す「あの日」が交互に来る。
#       三通目でとうとう言えなかった一言にたどり着き、最後の一回だけ、全部をぶちまける（サビは最後に一度だけ）。追伸は馬頭琴だけ。
# 形: 手紙と回想の交互（読む → 思い出す ×3）→ 一度だけのサビ → 追伸。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ:
#   読む1（1）: 素朴で軽い。クリーンのギターとベース、リードは話すような早口
#   回想1（1→2）: 広く遠い。馬頭琴がすべって歌い、歪みの和音が遠くで鳴る
#   読む2（1）／回想2（2）
#   読む3（0）: いちばん近い。馬頭琴とリードだけ
#   回想3（2→3）: 少しずつ決壊していく
#   サビ（3）: 初めての全開。この一回だけ
#   追伸（0）: 馬頭琴だけ
# 旋律の性格: 読むは「話す」（16分の言いかけと、語尾が上がる問いかけ）。回想は大きく跳ぶ呼びかけ（6度・オクターブ）。小節の終わりで伸ばさない
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 100, 4
bar = Bars(BEATS)
R4 = bar.rest()

READ = ["A", "G/A", "A", "D/A", "A", "G/A", "F#m", "E7sus4", "A", "A"]
MEM = ["D", "A/C#", "Bm", "G", "D", "A/C#", "G", "A", "D", "A/C#", "Bm", "G", "Em", "A"]
FORM = [("read1", 10), ("mem1", 14), ("read2", 10), ("mem2", 14), ("read3", 8), ("mem3", 16), ("chorus", 20), ("ps", 8)]
CH = {"read1": READ, "read2": READ, "read3": READ[:8], "mem1": MEM, "mem2": MEM, "mem3": MEM + ["F", "G"],
      "chorus": ["G", "D", "A", "A", "G", "D", "E7sus4", "A", "F", "G", "D", "A", "F", "G", "A", "A", "G", "D", "A", "A"], "ps": ["A", "G/A", "D/A", "A", "A", "G/A", "A", "A"]}
song = Song("成層圏の手紙（仮）",
            "仮: ラウド26曲の10曲目（2026-10-24 素材から作り直し）。ポストハードコア＋馬頭琴風のチェロ。A ミクソリディアン・100。"
            "手紙を読む（話すような早口）と回想（大きく跳ぶ呼びかけ）が交互に3回、サビは最後に一度だけ全開、追伸は馬頭琴だけ。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 宛先のない航空便を読む。いまとあの日が交互に来て、三通目で言えなかった一言にたどり着き、一度だけ全部をぶちまける。"
song.kinds = {"read1": "verse", "read2": "verse", "read3": "verse", "mem1": "bridge", "mem2": "bridge", "mem3": "pre", "chorus": "chorus", "ps": "outro"}
SECS, NB = song.secs, song.nb
MIX = scale_pcs("A", "mixolydian")

# 読む: 話すような早口と、語尾が上がる問いかけ
SPEAK = [[-0.25, 0.25, 0.25, 0.25, 0.5, 0.5, -0.5, 0.25, 0.25, 0.5, -0.5], [0.25, 0.25, 0.25, 0.25, 0.75, -1.25, 0.25, 0.25, 0.5],
         [-1, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 0.25, -1], [0.5, 0.25, 0.25, -0.5, 0.25, 0.25, 0.25, 0.25, 0.75, -0.75],
         [-0.5, 0.25, 0.25, 0.5, -0.5, 0.25, 0.25, 0.25, 0.25, -1]]
READ_MEL = {k: [bar(x) for x in melody_walk(MIX, a, b, SPEAK, k, CH[f"read{k}"], contour=(0, 0, 1, -1, 0, 2, -2, 1), lo="E4", hi="E5")]
            for k, (a, b) in {1: ("A4", "C#5"), 2: ("C#5", "E5"), 3: ("E5", "A4")}.items()}
# 回想: 大きく跳ぶ呼びかけ（下の音 → 6度・オクターブ上）
CALL = {"D": ("F#4", "D5"), "A/C#": ("E4", "C#5"), "Bm": ("F#4", "D5"), "G": ("D4", "B4"), "Em": ("E4", "B4"), "A": ("E4", "E5"), "F": ("F4", "C5"), "F#m": ("F#4", "C#5"), "E7sus4": ("E4", "B4")}


def call_bar(ch, i):
    lo, hi = CALL[ch]
    pats = [f"R:0.5 {lo}:0.5 {hi}:1.5 R:0.5 {lo}:0.5 R:0.5", f"{lo}:0.25 {hi}:1.25 R:1 {hi}:0.25 {lo}:0.25 R:1", f"R:1 {lo}:0.5 {hi}:0.5 R:0.5 {hi}:0.5 {lo}:1",
            f"{hi}:0.75 {lo}:0.25 R:1 {lo}:0.25 {hi}:0.75 R:1"]
    return bar(pats[i % 4])


# 馬頭琴: すべり込む長い音（回想・追伸）
def morin(ch, i):
    lo, hi = CALL[ch]
    return bar(f"{hi}:2/ {lo}:2") if i % 2 == 0 else bar(f"R:1 {up(lo, 0)}:3/")


# サビ（20小節）: 呼びかけの跳躍を旋律にした、一度だけの全開
CHORUS = [bar("R:0.5 D4:0.5 B4:1 R:0.5 B4:0.25 A4:0.25 G4:0.5 D4:0.5"), bar("R:0.5 F#4:0.5 D5:1.5 R:0.5 A4:0.5 R:0.5"),
          bar("R:0.25 E4:0.25 C#5:0.5 E5:1 R:0.5 C#5:0.5 A4:0.5 E4:0.5"), bar("A4:0.75 C#5:0.25 R:1 E4:0.5 A4:0.5 R:1"),
          bar("R:0.5 D4:0.5 B4:1 R:0.5 D5:0.25 B4:0.25 G4:0.5 B4:0.5"), bar("R:0.5 A4:0.5 F#5:1 R:0.5 D5:0.5 A4:0.5 R:0.5"),
          bar("R:0.25 E4:0.25 B4:0.5 E5:1 R:0.5 D5:0.5 B4:0.5 A4:0.5"), bar("C#5:0.75 A4:0.25 R:1 E5:0.5 C#5:0.5 R:1"),
          bar("R:0.5 F4:0.5 C5:1 R:0.5 C5:0.25 A4:0.25 F4:0.5 A4:0.5"), bar("R:0.5 G4:0.5 D5:1 R:0.5 B4:0.5 G4:0.5 R:0.5"),
          bar("R:0.25 F#4:0.25 D5:0.5 F#5:1 R:0.5 D5:0.5 A4:0.5 F#4:0.5"), bar("E5:0.75 C#5:0.25 R:1 A4:0.5 E5:0.5 R:1"),
          bar("R:0.5 A4:0.5 F5:1 R:0.5 C5:0.5 A4:0.5 R:0.5"), bar("R:0.5 B4:0.5 G5:1 R:0.5 D5:0.5 B4:0.5 R:0.5"),
          bar("R:0.25 E4:0.25 A4:0.5 E5:1 R:0.5 C#5:0.25 E5:0.25 A4:1"), bar("R:1 E5:0.5 C#5:0.5 A4:0.5 R:1.5"),
          bar("R:0.5 D5:0.5 B4:1 R:0.5 D5:0.5 G4:0.5 R:0.5"), bar("R:0.5 F#5:0.5 D5:1 R:0.5 A4:0.5 F#4:0.5 R:0.5"),
          bar("R:0.25 C#5:0.25 E5:0.5 A4:1 R:2"), bar("R:4")]

LOW = {"A": "A1", "G/A": "A1", "D/A": "A1", "F#m": "F#1", "E7sus4": "E2", "D": "D2", "A/C#": "C#2", "Bm": "B1", "G": "G1", "Em": "E2", "F": "F2"}
P = {k: [] for k in ["riff", "rhy", "lead", "clean", "morin", "bass"]}
kit = Kit(BEATS)
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]
    riff = rhy = lead = clean = mo = R4
    g = LOW[ch]; root = root_note(ch.split("/")[-1] if "/" in ch else ch)
    tones = (chord_tones(ch.split("/")[0], "A3", "A4") * 2)[:4]
    if name.startswith("read"):
        k = int(name[4:])
        lead = READ_MEL[k][i]
        if k < 3: clean = bar(f"{tones[0]}:0.5 {tones[1]}:0.5 {tones[2]}:0.5 {tones[1]}:0.5 {tones[3]}:0.5 {tones[1]}:0.5 {tones[2]}:1")
        else: mo = bar(f"{CALL.get(ch.split('/')[0], CALL['A'])[0]}:4,") if i % 2 == 0 else R4
        b = bar(f"{root}:1.5 R:0.5 {root}:0.5 {root}:1.5") if k < 3 else R4
    elif name.startswith("mem"):
        k = int(name[3:])
        lead = call_bar(ch, i) if (k > 1 or i >= 6) else R4
        mo = morin(ch, i) if i % 4 in (0, 1) or k == 3 else R4
        riff = bar(f"{g}:4") if k == 1 else (bar(f"{g}:2! {g}:1 {tr(g, 7)}:1") if k == 2 or i < 8 else bar(f"{g}:0.5! {g}:0.5 {g}:0.5 {g}:0.5 {g}:0.5! {g}:0.5 {tr(g, 7)}:0.5 {g}:0.5"))
        rhy = riff if (k >= 2) else R4
        b = bar(f"{root}:4") if k == 1 else unison_low(riff, -1, "B0")
    elif name == "chorus":
        lead = CHORUS[i]; mo = shift_oct(strip_marks(CHORUS[i]), -1) if i >= 8 else R4
        riff = rhy = bar(f"{g}:0.75! {g}:0.75 {g}:0.5 {g}:0.75! {g}:0.75 {tr(g, 7)}:0.5") if i < n - 1 else bar(f"{g}:4!")
        b = unison_low(riff, -1, "B0")
    else:   # ps
        mo = morin(ch.split("/")[0] if ch.split("/")[0] in CALL else "A", i) if i < 6 else (bar("A4:4/") if i == 6 else R4)
        b = R4
    P["riff"].append(riff); P["rhy"].append(rhy); P["lead"].append(lead); P["clean"].append(clean); P["morin"].append(mo); P["bass"].append(b)
    kit.add("X.......X.......", "....X.......X...", "x.x.x.x.x.x.x.x.")

J = lambda k: " ".join(P[k])
MORIN_FX = [{"type": "eq", "low": -1, "mid": 2.5, "midHz": 1200, "high": 0.5}, {"type": "delay", "beats": 0.75, "mix": 0.12, "feedback": 0.25}, {"type": "reverb", "mix": 0.3}]
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy")))
song.add(lead_part(J("lead")))
song.add(clean_part(J("clean"), vol=0.08, pan=0.25, role="クリーンの分散和音（読む）"))
song.add(part("馬頭琴の代わり（チェロの録音）", "strings", J("morin"), patch="cello", volume=0.19, pan=-0.12, reverb=0.5, attack=0.12, release=0.7, phrase=8, fx=MORIN_FX))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.screams = [10 + 14 + 10 + 14 + 8 + 16 + 13]       # サビの頂点（G の跳躍のあと）に一度だけ
song.ref_tone = "bright-pop-rock"

from lm25_plans import apply_plan
apply_plan(song, "10")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-10-seisouken.json"
    song.write(out)
    check_clash(song)
