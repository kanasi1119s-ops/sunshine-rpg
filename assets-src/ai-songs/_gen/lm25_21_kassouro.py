# ラウド26曲 21「V1, Rotate」（仮。もとの仮題「群青の滑走路」）。2026-10-24 素材から作り直し
# スタイル: パワーメタル（明るい長調・ギャロップの刻み・上へ伸びる旋律）＋バイオリン。D 長調 → E♭ → E・120・4/4
# 物語: 滑走路からの離陸。エンジン → 滑走（V1: もう止まれない速さ）→ 機首上げ（Rotate）→ 雲の中 → 雲の上 → さらに高く。降りてこない。
# 形: 止まらない一本道（同じ区間に戻らず、調が2回上がり、ずっと上り続ける。静かなのは雲の中だけ）。ほかの曲と骨組みを変える
#      07（落ちる）・08（速さが変わる）とは逆で、速さは変えず、音域と調が上がり続ける
# 場面と、そこで必要な強さ:
#   エンジン（1）: ベースの8分とバイオリンの長い音
#   滑走（2）: ギャロップの刻みが積み上がる
#   機首上げ（3）: 伸びやかな旋律が上へ
#   雲の中（0）: ドラムなし。バイオリンときれいなギターだけ
#   雲の上（2）: 半音上。バイオリンが歌う
#   さらに高く（3）: もう半音上。旋律がいちばん高い所へ
#   空（1）: バイオリンと和音が残って、消える
# 旋律の性格: 長く伸びやかで、句ごとに少しずつ上へ（最後の音は前の句より高い）。「4分4分2分」の型は使わない
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 120, 4
bar = Bars(BEATS)
R4 = bar.rest()

FLY = ["D", "A", "Bm", "G", "D", "A", "G", "A"]
FORM = [("taxi", 8), ("runway", 20), ("rotate", 24), ("cloud", 12), ("above", 24), ("higher", 24), ("sky", 8)]
CH = {"taxi": ["D"] * 8, "runway": ["D", "D", "G", "A"] * 5, "rotate": FLY * 3, "cloud": ["Bm", "G", "D", "A"] * 3,
      "above": FLY * 3, "higher": FLY * 3, "sky": ["D", "G", "D", "D", "G", "A", "D", "D"]}
song = Song("群青の滑走路（仮）",
            "仮: ラウド26曲の21曲目（2026-10-24 素材から作り直し）。パワーメタル＋バイオリン。D 長調 → E♭ → E・120。エンジン・滑走・機首上げ・雲の中・雲の上・さらに高く。"
            "同じ区間に戻らず、調が2回上がって上り続ける。旋律は長く伸びやかに、句ごとに上へ。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 滑走路からの離陸。もう止まれない速さで機首を上げ、雲を抜け、さらに高くへ。降りてこない。"
song.kinds = {"taxi": "intro", "runway": "pre", "rotate": "chorus", "cloud": "bridge", "above": "verse", "higher": "chorus", "sky": "outro"}
SECS, NB = song.secs, song.nb
DMAJ = scale_pcs("D", "ionian")

SOAR = [[2.5, 0.5, 1], [-1, 3], [1.5, 1.5, 1], [3.5, -0.5], [0.5, 3, -0.5], [-0.5, 1.5, 2]]
ROT = [bar(x) for x in melody_walk(DMAJ, "A4", "D5", SOAR, 1, CH["rotate"], contour=(1, 2, -1, 1, 1, -2), lo="F#4", hi="E5")]
ABOVE = [bar(x) for x in melody_walk(DMAJ, "D5", "F#5", SOAR, 2, CH["above"], contour=(2, -1, 1, 2, -2), lo="A4", hi="F#5")]
HIGH = [bar(x) for x in melody_walk(DMAJ, "E5", "F#5", SOAR, 3, CH["higher"], contour=(1, 1, -2, 2, 1, -1), lo="B4", hi="F#5")]
VCLOUD = ["R:1 F#5:3", "D5:2.5 R:1.5", "R:0.5 A4:3.5", "C#5:3 R:1", "R:1 B4:3", "G4:2.5 R:1.5", "R:0.5 F#4:3.5", "E4:3 R:1", "R:1 D5:3", "B4:2.5 R:1.5", "R:0.5 A4:3.5", "C#5:4"]

LOW = {"D": "D2", "A": "A1", "Bm": "B1", "G": "G1"}
P = {k: [] for k in ["riff", "rhy", "lead", "clean", "vln", "bass"]}
kit = Kit(BEATS)
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]
    riff = rhy = lead = clean = vln = R4
    g = LOW[ch]; root = root_note(ch)
    gallop = bar(" ".join(f"{g}:0.5! {g}:0.25 {g}:0.25" for _ in range(4)))
    if name == "taxi":
        b = bar(" ".join(f"D1:0.5{'!' if j % 4 == 0 else ''}" for j in range(8)))
        vln = bar("A4:4") if i % 2 == 0 else bar("A4:2 F#4:2")
    elif name == "runway":
        riff = gallop if i >= 4 else bar(f"{g}:0.5! R:3.5")
        rhy = gallop if i >= 10 else R4
        vln = bar(f"{chord_tones(ch, 'D5', 'D6')[0]}:4") if i >= 12 else R4
        b = bar(" ".join(f"{root}:0.5{'!' if j % 2 == 0 else ''}" for j in range(8)))
    elif name in ("rotate", "above", "higher"):
        riff = rhy = gallop
        lead = {"rotate": ROT, "above": ABOVE, "higher": HIGH}[name][i]
        if name == "above": vln = bar(strip_marks(lead)) if i < 12 else R4
        if name == "higher": vln = bar(shift_oct(strip_marks(lead), -1)) if i >= 8 else R4
        b = bar(f"{root}:1.5! {root}:0.5 {fifth_of(ch)}:1 {root}:1")
    elif name == "cloud":
        vln = bar(VCLOUD[i])
        tones = (chord_tones(ch, "D4", "D5") * 2)[:4]
        clean = bar(" ".join(f"{t}:0.5" for t in (tones + tones[::-1])))
        b = bar(f"{root}:4,") if i % 2 == 0 else R4
    else:   # sky
        vln = bar(["D5:4", "B4:4", "A4:4", "F#4:4", "G4:4", "A4:4", "D5:4", "R:4"][i])
        riff = bar(f"{g}:4,") if i < 7 else R4
        b = bar(f"{root}:4,") if i < 7 else R4
    P["riff"].append(riff); P["rhy"].append(rhy); P["lead"].append(lead); P["clean"].append(clean); P["vln"].append(vln); P["bass"].append(b)
    kit.add("X.......X.......", "....X.......X...", "x.x.x.x.x.x.x.x.")

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy")))
song.add(lead_part(J("lead")))
song.add(clean_part(J("clean"), vol=0.08, pan=0.25, role="クリーンの分散和音（雲の中）"))
song.add(part("バイオリン", "strings", J("vln"), patch="violin", volume=0.15, pan=-0.18, reverb=0.5, gainDb=3, bright=-0.15, attack=0.35, release=0.7,
              doubleDetune={"cents": 5, "spread": 0.3}, phrase=8,
              fx=[{"type": "eq", "low": 2, "mid": -2.5, "midHz": 2800, "high": 0}, {"type": "delay", "beats": 1, "mix": 0.08, "feedback": 0.2},
                  {"type": "reverb", "mix": 0.22}, {"type": "plate", "mix": 0.12}]))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.screams = [8 + 20 + 24 + 12 + 24 + 23]     # いちばん高い所（さらに高くの最後）に一度だけ
song.ref_tone = "glossy-jrock"

from lm25_plans import apply_plan
apply_plan(song, "21")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-21-kassouro.json"
    song.write(out)
    check_clash(song)
