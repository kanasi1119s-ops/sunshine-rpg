# ラウド26曲 19「Rewind My Last Breath」（仮。もとの仮題「最後の呼吸」）。2026-10-24 素材から作り直し
# スタイル: プログレッシブ（時代ごとに鳴り方が変わる: 現代のヘヴィ → 速いハードロック → 弦だけ）＋弦楽合奏。B 短調 → D 長調・104 → 132 → 96
# 物語: 最期の息から、人生を巻き戻す。大人の日々 → 若い頃 → 子どもの頃 → 最初の息（生まれた瞬間）で終わる。
# 形: 逆再生（いちばん大きい所から始まり、時代をさかのぼるほど小さく素朴になる）。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ:
#   最期（3）: いちばん大きい。弦のトレモロ、リードは高く広く。最後は長い吐く息（弦が下りていく）
#   大人（2）: 現代のヘヴィなうねり。旋律はシンコペーションで、追われるように
#   若い頃（2→1）: 132 の速いハードロック。まっすぐな8分、レガートの速弾き
#   子ども（0）: D 長調、弦だけ（ピチカートと素朴な歌）
#   最初の息（0）: 弦の1つの和音と、ピチカートの2音
# 旋律の性格: 時代ごとに歌い方が変わる（最期＝広い跳躍・大人＝シンコペーション・若い頃＝まっすぐの8分・子ども＝順に進む素朴な歌）
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 104, 4
bar = Bars(BEATS)
R4 = bar.rest()

FORM = [("last", 16), ("adult", 32), ("young", 32), ("child", 24), ("birth", 6)]
CH = {"last": ["Bm", "G", "D", "A", "Bm", "G", "Em", "F#"] * 2, "adult": ["Bm", "Bm", "G", "A"] * 8,
      "young": ["Bm", "A", "G", "A", "Bm", "D", "E", "F#"] * 4, "child": ["D", "G", "D", "A", "D", "G", "A", "D"] * 3, "birth": ["D", "D", "G", "D", "D", "D"]}
song = Song("最後の呼吸（仮）",
            "仮: ラウド26曲の19曲目（2026-10-24 素材から作り直し）。最期の息から人生を巻き戻す。最期（いちばん大きい）→ 大人（現代のヘヴィ）→ 若い頃（132 の速いハードロック）"
            "→ 子ども（D 長調・弦だけ）→ 最初の息。時代ごとに歌い方が変わる。別の楽器は弦楽合奏。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 最期の息から人生を巻き戻し、生まれた瞬間の最初の息で終わる。"
song.kinds = {"last": "chorus", "adult": "verse", "young": "solo", "child": "bridge", "birth": "outro"}
SECS, NB = song.secs, song.nb
BM = scale_pcs("B", "aeolian")

LAST = [bar(x) for x in melody_walk(BM, "F#5", "B4", [[1.5, 0.5, 2], [-0.5, 1.5, 1, 1], [2, 1, 0.5, 0.5], [1, -0.5, 0.5, 2]], 1, CH["last"],
                                     contour=(2, -1, 3, -2, -1), lo="B3", hi="F#5")]
# 最期の後半は、長く吐く息（下りていく）
for k, x in enumerate(["F#5:3 E5:1", "D5:3 B4:1", "G4:3 E4:1", "F#4:4"]): LAST[12 + k] = bar(x)
ADULT = [bar(x) for x in melody_walk(BM, "D5", "F#4", [[-0.5, 0.75, 0.25, 0.5, -0.5, 0.5, 1], [0.25, 0.5, 0.25, -0.5, 0.5, 0.5, -1.5], [-0.25, 0.25, 0.5, 0.5, 0.25, 0.75, -1.5]],
                                      2, CH["adult"], contour=(-1, 2, -1, -2, 3, -1), lo="D4", hi="E5")]
YOUNG = [bar(x) for x in melody_walk(BM, "B4", "D5", [[0.5] * 8, [0.5, 0.5, 0.5, 0.5, 1, -1], [-0.5] + [0.5] * 7], 3, CH["young"],
                                      contour=(1, 1, -1, 1, -2, 1), lo="F#4", hi="E5")]
DM = scale_pcs("D", "ionian")
CHILD = ["F#4:1 E4:1 D4:1 E4:1", "G4:1 G4:1 B4:2", "A4:1 G4:1 F#4:1 E4:1", "D4:1 E4:1 F#4:1 R:1",
         "A4:1 A4:1 B4:1 A4:1", "G4:2 B4:1 G4:1", "F#4:1 E4:1 D4:1 E4:1", "D4:3 R:1"]

P = {k: [] for k in ["riff", "rhy", "lead", "tech", "s0", "s1", "s2", "smel", "pizz", "bass"]}
kit = Kit(BEATS)
SV = {"Bm": ["B2", "F#3", "D4"], "G": ["G2", "D3", "B3"], "D": ["D3", "A3", "F#4"], "A": ["A2", "E3", "C#4"], "Em": ["E3", "B3", "G4"], "F#": ["F#2", "C#3", "A#3"], "E": ["E3", "B3", "G#4"]}
LOW = {"Bm": "B1", "G": "G1", "D": "D2", "A": "A1", "Em": "E2", "F#": "F#1", "E": "E2"}
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]
    riff = rhy = lead = tech = smel = pizz = R4; st = [R4] * 3
    g = LOW[ch]; root = root_note(ch); sv = SV[ch]
    if name == "last":
        lead = LAST[i]
        st = [bar(" ".join([f"{x}:0.25"] * 16)) for x in sv] if i < 12 else [bar(f"{x}:4") for x in sv]
        riff = rhy = bar(f"{g}:1! {g}:0.5 {g}:0.5 {g}:1! {tr(g, 7)}:1") if i < 12 else (bar(f"{g}:4!") if i == 12 else R4)
        b = unison_low(riff, -1, "B0") if i < 13 else bar(f"{root}:4,")
    elif name == "adult":
        lead = ADULT[i] if i >= 4 else R4
        riff = rhy = bar(f"{g}:0.75! {g}:0.25 R:0.5 {g}:0.25 {g}:0.25 R:0.5 {tr(g, 3)}:0.5! {g}:0.5 {tr(g, 1)}:0.5")
        st = [bar(f"{x}:4,") for x in sv] if i % 8 == 0 else [R4] * 3
        b = unison_low(riff, -1, "B0")
    elif name == "young":
        lead = YOUNG[i] if i % 8 < 6 else R4
        if i % 8 >= 6:
            tones = chord_tones(ch, "B3", "B5")
            tech = bar(" ".join(f"{tones[j % len(tones)]}:0.25" for j in [0, 1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 5, 4, 3, 2, 1]))
        g2 = root_note(ch, "E2", "D#3")
        riff = rhy = bar(" ".join(f"{g2}:0.5{'!' if j % 2 == 0 else ''}" for j in range(8)))
        b = bar(" ".join(f"{root}:0.5" for _ in range(8)))
    elif name == "child":
        smel = bar(CHILD[i % 8])
        pizz = bar(f"{sv[0]}:1 {sv[2]}:1 {sv[1]}:1 {sv[2]}:1")
        st = [bar(f"{sv[0]}:4,"), bar(f"{sv[1]}:4,"), R4] if i >= 8 else [R4] * 3     # 旋律と同じ高さを避けて、根音と5度だけ
        b = R4
    else:   # birth
        st = [bar(f"{x}:4,") for x in SV[ch]] if i in (2, 3) else [R4] * 3
        pizz = bar("D5:1 A4:1 R:2") if i == 4 else R4
        b = R4
    P["riff"].append(riff); P["rhy"].append(rhy); P["lead"].append(lead); P["tech"].append(tech); P["smel"].append(smel); P["pizz"].append(pizz)
    for j in range(3): P[f"s{j}"].append(st[j])
    P["bass"].append(b)
    kit.add("X.......X.......", "....X.......X...", "x.x.x.x.x.x.x.x.")

J = lambda k: " ".join(P[k])
STR = dict(reverb=0.5, attack=0.3, release=0.9, fx=[{"type": "eq", "low": 0, "mid": -1.5, "midHz": 2500, "high": 0}, {"type": "reverb", "mix": 0.25}])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy")))
song.add(lead_part(J("lead")))
song.add(tech_part(J("tech"), role="レガートのギター（若い頃）", vol=0.11, pan=0.05))
song.add([part(f"弦楽合奏（{['下', '中', '上'][j]}）", "strings", J(f"s{j}"), patch="stringEnsemble", volume=0.09, pan=[-0.3, 0.3, 0][j], **STR) for j in range(3)])
song.add(part("弦楽合奏（旋律）", "strings", J("smel"), patch="stringEnsemble", volume=0.14, pan=0, phrase=8, **STR))
song.add(part("弦のピチカート", "strings", J("pizz"), patch="pizzicato", volume=0.12, pan=0.2, reverb=0.4))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.screams = [11]          # 最期の頂点（吐く息の直前）に一度だけ
song.ref_tone = "bright-nu-wall"

from lm25_plans import apply_plan
apply_plan(song, "19")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-19-kokyu.json"
    song.write(out)
    check_clash(song)
