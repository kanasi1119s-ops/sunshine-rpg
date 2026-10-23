# ラウド26曲 25「Last Deal Before Sunrise」（仮。もとの仮題「夜明けの闇市」）。2026-10-24 素材から作り直し
# スタイル: ダークなハードロック／メタル（ハーフタイムの重さ・シャッフル・タムの太鼓）＋バイオリン。E 短調 → E 長調・112 → 120・4/4
# 物語: 夜明け前の闇市。流しのバイオリン弾きが、夜明けまでに最後の取引をまとめようとする。時計が鳴るたびに、残り時間が短くなる。
# 形: 秒読み（1時・2時・3時・4時の場面が、24 → 20 → 12 → 8 小節とだんだん短くなり、せき立てられる。取引がまとまった瞬間に夜が明け、
#      夜の旋律が長調になって、いちばん長い場面になる）。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ:
#   時計（1）: 時計の音とバイオリン。鐘が時刻の数だけ鳴る（各場面の頭）
#   1時（1→2）: 重いハーフタイム。バイオリンが夜の旋律（付点のタンゴの足どり）。後半はリードが受けつぐ
#   2時（2）: シャッフルの酒場。リードとバイオリンが2小節ずつ値段の掛け合い
#   3時（0）: 人の消えた市場。ドラムなし。バイオリンのはじく音と、クリーンのギター
#   4時（3）: タムの太鼓。バイオリンとリードが16分で同じ速い旋律（急ぐ）
#   取引（3）: 決めの一撃と無音を交互に。手を打つ
#   夜明け（2→3）: 120 に上がり、長調。夜の旋律が明るくなって、バイオリンとリードで歌いきる
#   朝（0）: バイオリンとクリーンが残る
# 旋律の性格: 夜の旋律＝付点で引きずるタンゴの足どり（E 和声的短音階）。夜明けは同じ旋律を長調に
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 112, 4
bar = Bars(BEATS)
R4 = bar.rest()

NIGHT = ["E5:1.5 D#5:0.5 E5:1 B4:1", "C5:2 B4:0.5 A4:0.5 G4:1", "A4:1.5 B4:0.5 C5:1 E5:1", "D#5:3 R:1",
         "E5:1.5 F#5:0.5 G5:1 E5:1", "C5:1.5 E5:0.5 A5:1 F#5:1", "F#5:1 E5:1 D#5:1 C5:0.5 B4:0.5", "E5:3 R:1"]
NIGHT_CH = ["Em", "C", "Am", "B7", "Em", "Am", "B7", "Em"]
DAWN_CH = ["E", "C#m", "A", "B", "E", "A", "B", "E"]


def to_major(s):
    """夜の旋律を E 長調に（G→G#、C→C#、D→D#）"""
    out = []
    for t in s.split():
        if t.startswith("R"): out.append(t); continue
        n, rest = t.split(":", 1)
        for a, b in (("G", "G#"), ("C", "C#"), ("D", "D#")):
            if n[0] == a and n[1] != "#": n = b + n[1:]
        out.append(n + ":" + rest)
    return " ".join(out)


DAWN = [to_major(x) for x in NIGHT]
FORM = [("clock", 4), ("h1", 24), ("h2", 20), ("h3", 12), ("h4", 8), ("deal", 4), ("dawnA", 8), ("dawnB", 28), ("morning", 8)]
CH = {"clock": ["Em"] * 4, "h1": NIGHT_CH * 3, "h2": ["Em", "Am", "B7", "Em"] * 5, "h3": ["Em", "C", "Am", "B7"] * 3, "h4": ["Em", "C", "B7", "Em"] * 2,
      "deal": ["C", "B7", "C", "B7"], "dawnA": DAWN_CH, "dawnB": DAWN_CH * 3 + ["A", "B", "E", "E"], "morning": ["E", "A", "E", "E"] * 2}
song = Song("夜明けの闇市（仮）",
            "仮: ラウド26曲の25曲目（2026-10-24 素材から作り直し）。ダークなメタル＋バイオリン。E 短調 → E 長調・112 → 120。夜明け前の闇市の秒読み: 1時・2時・3時・4時の場面が"
            "だんだん短くなってせき立て、取引の一撃のあと夜が明け、夜の旋律が長調になって歌いきる。自作",
            BPM, BEATS, FORM, CH)
song.flags = "--space hall --space-wet 0.12"
song.desc += " 物語: 夜明けまでに最後の取引をまとめる流しのバイオリン弾き。時計が鳴るたびに残り時間が短くなる。"
song.kinds = {"clock": "intro", "h1": "verse", "h2": "pre", "h3": "bridge", "h4": "solo", "deal": "break", "dawnA": "verse", "dawnB": "chorus", "morning": "outro"}
SECS, NB = song.secs, song.nb
EH = scale_pcs("E", "harmonic")
EM = scale_pcs("E", "ionian")

H1_LEAD = [bar(x) for x in melody_walk(EH, "B4", "E5", [[1.5, 0.5, 1, 1], [-0.5, 1, 0.5, 2], [0.75, 0.75, 0.5, 2], [3, -1]], 1, CH["h1"][16:],
                                        contour=(1, -2, 1, 2, -1), lo="G4", hi="G5")]
H2_CALL = [bar(x) for x in melody_walk(EH, "G4", "B4", [[-0.6667, 0.3333, 0.6667, 0.3333, 1, -1], [0.6667, 0.3333, 0.6667, 0.3333, 2]], 2, CH["h2"],
                                        contour=(2, -1, -1, 1), lo="E4", hi="E5")]
H2_ANS = [bar(x) for x in melody_walk(EH, "E5", "B4", [[1, 0.6667, 0.3333, 1, -1], [-1, 0.6667, 0.3333, 2]], 3, CH["h2"],
                                       contour=(-1, -1, 2, -2), lo="G4", hi="A5")]
DAWN_SOAR = [bar(x) for x in melody_walk(EM, "B5", "E5", [[2.5, 0.5, 1], [-0.5, 1.5, 2], [3, -1], [1, 1, 2]], 4, CH["dawnB"][16:],
                                          contour=(1, -1, 2, -2, 1), lo="E5", hi="E6")]
RUN_SC = scale_notes("E", "harmonic", "E4", "E6")


def run16(ch, up_first):
    """4時: 和音の根音から16分で上がって下りる（急ぐ）"""
    r = root_note(ch, "E4", "D#5")
    k = min(range(len(RUN_SC)), key=lambda j: abs(midi(RUN_SC[j]) - midi(r)))
    seq = [RUN_SC[min(k + j, len(RUN_SC) - 1)] for j in range(8)]
    if up_first:
        return bar(" ".join(f"{n}:0.25{'!' if j % 4 == 0 else ''}" for j, n in enumerate(seq + seq[::-1])))
    # 次の小節は、上がりきって突く（16分 8つ → 8分 2つ → 4分）
    return bar(" ".join(f"{n}:0.25{'!' if j % 4 == 0 else ''}" for j, n in enumerate(seq)) + f" {seq[-1]}:0.5! {seq[4]}:0.5 {seq[0]}:1!")


def strikes(n):
    """時計の鐘: 時刻の数だけ"""
    return bar(" ".join(["E5:1"] * n + ["R:1"] * (4 - n))) if n < 4 else bar("E5:1 E5:1 E5:1 E5:1")


LOW = {"Em": "E2", "C": "C2", "Am": "A1", "B7": "B1", "E": "E2", "C#m": "C#2", "A": "A1", "B": "B1"}
P = {k: [] for k in ["riff", "rhy", "lead", "clean", "vln", "bell", "bass"]}
kit = Kit(BEATS)
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]
    riff = rhy = lead = clean = vln = bell = R4
    g = LOW[ch]; root = root_note(ch)
    if name == "clock":
        clean = bar("E5:0.25 R:0.75 B4:0.25 R:0.75 E5:0.25 R:0.75 B4:0.25 R:0.75")      # 時計の音
        vln = bar("B4:4") if i == 2 else (bar("B4:2 D#5:2") if i == 3 else R4)
        b = R4
    elif name == "h1":
        if i == 0: bell = strikes(1)
        riff = rhy = bar(f"{g}:1.5! {g}:0.5 R:1 {tr(g, 1)}:0.5 {g}:0.5") if i >= 4 else bar(f"{g}:4!")
        if i < 8: vln = bar(NIGHT[i])
        elif i < 16: lead = bar(NIGHT[i % 8]); vln = bar(f"{chord_tones(ch, 'G4', 'G5')[0]}:4")
        else: lead = H1_LEAD[i - 16]
        b = bar(f"{root}:1.5 {root}:0.5 R:1 {root}:1")
    elif name == "h2":
        if i == 0: bell = strikes(2)
        riff = rhy = bar(f"{g}:0.6667! {g}:0.3333 R:0.6667 {g}:0.3333 {tr(g, 7)}:0.6667! {g}:0.3333 {tr(g, 10)}:0.6667 {g}:0.3333")
        if (i // 2) % 2 == 0: lead = H2_CALL[i]
        else: vln = H2_ANS[i]
        b = unison_low(riff, -1, "B0")
    elif name == "h3":
        if i == 0: bell = strikes(3)
        tones = (chord_tones(ch, "E3", "E4") * 2)[:4]
        clean = bar(" ".join(f"{t}:0.5" for t in tones + tones[::-1]))
        # バイオリンのはじく音（夜の旋律の音だけを短く）
        vln = bar(" ".join(x if x.startswith("R") else x.split(":")[0] + ":0.25 R:" + f"{tok_beats(x) - 0.25:g}" for x in NIGHT[i % 8].split()).replace(" R:0 ", " "))
        b = bar(f"{root}:2, R:2") if i % 2 == 0 else R4
    elif name == "h4":
        if i == 0: bell = strikes(4)
        riff = rhy = bar(" ".join(f"{g}:0.25{'!' if j % 4 == 0 else ''}" for j in range(16)))
        lead = run16(ch, i % 2 == 0); vln = lead
        b = unison_low(riff, -1, "B0")
    elif name == "deal":
        riff = rhy = bar(f"{g}:0.5! R:3.5") if i % 2 == 0 else bar(f"R:2 {g}:0.5! {g}:0.5! R:1")
        b = riff if False else (bar(f"{root}:0.5! R:3.5") if i % 2 == 0 else bar(f"R:2 {root}:0.5! {root}:0.5! R:1"))
        vln = bar("B5:4") if i == 3 else R4
    elif name == "dawnA":
        vln = bar(DAWN[i])
        tones = (chord_tones(ch, "E3", "E4") * 2)[:4]
        clean = bar(" ".join(f"{t}:0.5" for t in tones + tones[::-1]))
        riff = bar(f"{g}:4,") if i >= 4 else R4
        b = bar(f"{root}:2 {fifth_of(ch)}:2")
    elif name == "dawnB":
        riff = rhy = bar(f"{g}:1.5! {g}:0.5 {tr(g, 7)}:1 {g}:1")
        if i < 16:
            lead = bar(DAWN[i % 8])
            vln = bar(shift_oct(strip_marks(DAWN[i % 8]), 1)) if i >= 8 else bar(f"{chord_tones(ch, 'G#5', 'G#6')[0]}:4")
        else:
            lead = DAWN_SOAR[i - 16]
            vln = bar(DAWN[i % 8]) if i < 24 else bar(f"{chord_tones(ch, 'E5', 'E6')[0]}:4")
        b = bar(f"{root}:1.5 {root}:0.5 {fifth_of(ch)}:1 {root}:1")
    else:   # morning
        vln = bar(["G#5:4", "A5:2 F#5:2", "G#5:3 E5:1", "E5:4", "B4:4", "C#5:2 A4:2", "B4:4", "E5:4,"][i])
        tones = (chord_tones(ch, "E3", "E4") * 2)[:3]
        clean = bar(f"{tones[0]}:2 {tones[1]}:1 {tones[2]}:1") if i < 7 else bar(f"{tones[0]}:4,")
        b = bar(f"{root}:4,") if i in (0, 4) else R4
    P["riff"].append(riff); P["rhy"].append(rhy); P["lead"].append(lead); P["clean"].append(clean); P["vln"].append(vln); P["bell"].append(bell); P["bass"].append(b)
    if name == "deal":
        kit.add("X......." + "........" if i % 2 == 0 else "........X...X...", "X......." + "........" if i % 2 == 0 else "........X...X...", "................")
    else:
        kit.add("X.......X.......", "....X.......X...", "x.x.x.x.x.x.x.x.")

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy")))
song.add(lead_part(J("lead")))
song.add(clean_part(J("clean"), vol=0.09, pan=0.25, role="クリーンのギター（時計・3時・朝）"))
song.add(part("バイオリン", "strings", J("vln"), patch="violin", volume=0.15, pan=-0.18, reverb=0.5, gainDb=3, bright=-0.15, attack=0.3, release=0.7,
              doubleDetune={"cents": 5, "spread": 0.3}, phrase=8,
              fx=[{"type": "eq", "low": 2, "mid": -2.5, "midHz": 2800, "high": 0}, {"type": "delay", "beats": 1, "mix": 0.08, "feedback": 0.2},
                  {"type": "reverb", "mix": 0.22}, {"type": "plate", "mix": 0.12}]))
song.add(part("時計の鐘", "bell", J("bell"), volume=0.12, pan=0.15, reverb=0.5, sustain=1.5, release=1.2,
              fx=[{"type": "eq", "low": -3, "mid": 0, "midHz": 800, "high": 0}, {"type": "reverb", "mix": 0.3}]))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.ref_tone = "bright-pop-rock"

from lm25_plans import apply_plan
apply_plan(song, "25")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-25-yoake.json"
    song.write(out)
    check_clash(song)
