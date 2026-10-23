# ラウド26曲 24「Guilty Until Proven」（仮。もとの仮題「錆びた天秤」）。2026-10-24 素材から作り直し
# スタイル: デスコア寄りのメタルコア（低い刻みとブレイクダウン）＋鐘。B フリジアン・126・4/4
# 物語: 裁判。鐘、起訴（検事の早口）、三人の証人（友・見知らぬ男・母）、評議、判決の前の無音、判決の鐘、刑。
# 形: 裁判の手続き（起訴 → 証人3人＝3つの違う場面 → 評議 → 無音 → 判決 → 刑）。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ:
#   鐘（1）: 法廷の鐘だけ
#   起訴（2）: 低い刻みの上で、リードが検事の早口（同じ音の16分の連打）
#   証人1・友（1）: クリーンの悲しい歌
#   証人2・見知らぬ男（2）: ずれたうねり（シンコペーション）
#   証人3・母（0）: 鐘とクリーンだけ
#   評議（2→3）: だんだん詰まる
#   判決の前（0）: 2小節の無音
#   判決（3）: 鐘と全員の一撃
#   刑（3）: いちばん重いブレイクダウン。リードは判決の長い音
#   鐘（1）: 鐘だけが残る
# 旋律の性格: 検事＝同じ音の16分の連打（早口）、判決＝長い音、証人ごとに歌い方が違う
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 126, 4
bar = Bars(BEATS)
R4 = bar.rest()

FORM = [("bells", 4), ("charge", 20), ("friend", 16), ("stranger", 16), ("mother", 16), ("jury", 16), ("hush", 2), ("verdict", 4), ("sentence", 28), ("toll", 6)]
CH = {"bells": ["Bm"] * 4, "charge": ["Bm", "C", "Bm", "A"] * 5, "friend": ["G", "D", "Em", "Bm"] * 4, "stranger": ["Bm", "C", "D", "C"] * 4,
      "mother": ["Em", "Bm", "C", "Bm"] * 4, "jury": ["Bm", "C"] * 8, "hush": ["Bm", "Bm"], "verdict": ["C", "C", "Bm", "Bm"],
      "sentence": ["Bm", "Bm", "C", "Bm"] * 7, "toll": ["Bm"] * 6}
song = Song("錆びた天秤（仮）",
            "仮: ラウド26曲の24曲目（2026-10-24 素材から作り直し）。デスコア寄りのメタルコア＋鐘。B フリジアン・126。鐘、起訴（検事の早口）、証人3人（友・見知らぬ男・母）、"
            "評議、判決の前の無音、判決の鐘、刑（いちばん重いブレイクダウン）。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 裁判。起訴、三人の証人、評議、判決の前の無音、判決の鐘、刑。"
song.kinds = {"bells": "intro", "charge": "verse", "friend": "bridge", "stranger": "pre", "mother": "bridge", "jury": "pre", "hush": "break", "verdict": "break", "sentence": "chorus", "toll": "outro"}
SECS, NB = song.secs, song.nb
BP = scale_pcs("B", "phrygian")


def rapid(note, pattern):
    """検事の早口: 同じ音の16分の連打と休み（pattern の 1＝音・0＝休み、16個）"""
    toks = []
    for j, c in enumerate(pattern):
        if c != "1": toks.append("R:0.25"); continue
        last = j == 15 or pattern[j + 1] == "0"          # 連打の終わりは、隣の音へ突く（半音上・3度下と交互）
        nn = (tr(note, 1) if (j // 4) % 2 == 0 else tr(note, -3)) if last else note
        toks.append(f"{nn}:0.25{'!' if j % 4 == 0 or last else ''}")
    return bar(merge_rests(" ".join(toks)))


CHARGE_PAT = ["1111000011110000", "0011110000111100", "1111111100000000", "0000111111110000", "1010111100001111"]
CHARGE_NOTES = {"Bm": ["B4", "D5", "F#4"], "C": ["C5", "E5", "G4"], "A": ["A4", "C#5", "E4"]}
FRIEND = [bar(x) for x in melody_walk(scale_pcs("B", "aeolian"), "F#4", "D5", [[-1, 1.5, 0.5, 1], [2, -0.5, 0.5, 1], [-0.5, 0.5, 1.5, 0.5, -1]], 1, CH["friend"],
                                       contour=(1, 1, -1, 2, -1), lo="D4", hi="E5")]
STRANGER = [bar(x) for x in melody_walk(BP, "B4", "F#4", [[-0.75, 0.75, 0.5, -0.25, 0.75, 1], [0.75, 0.75, -0.5, 0.75, 0.25, -1], [-0.25, 0.75, 0.75, 0.25, -0.5, 0.5, -1]], 2,
                                         CH["stranger"], contour=(-1, 2, -2, 1), lo="D4", hi="D5")]
SENT = [bar(x) for x in melody_walk(BP, "F#5", "B4", [[3, -1], [-1, 3], [2.5, -1.5], [4]], 3, CH["sentence"], contour=(-1, 1, -2, -1), lo="B4", hi="F#5")]

LOW = {"Bm": "B1", "C": "C2", "A": "A1", "G": "G1", "D": "D2", "Em": "E2"}
P = {k: [] for k in ["riff", "rhy", "lead", "clean", "bell", "bass", "mute"]}
kit = Kit(BEATS)
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]
    riff = rhy = lead = clean = bell = mute = R4
    g = LOW[ch]; root = root_note(ch)
    chug = bar(f"{g}:0.25! {g}:0.25 R:0.5 {g}:0.25 {g}:0.25 R:0.5 {g}:0.5! R:0.25 {g}:0.25 {tr(g, 1)}:0.5 R:0.5")
    if name == "bells":
        bell = bar("B4:4") if i % 2 == 0 else bar("F#4:4")
        b = bar("B0:4,") if i >= 2 else R4
    elif name == "charge":
        riff = rhy = chug if i >= 4 else bar(f"{g}:0.5! R:3.5")
        lead = rapid(CHARGE_NOTES[ch][i % 3], CHARGE_PAT[i % 5]) if i >= 4 else R4
        b = unison_low(chug, -1, "B0")
    elif name == "friend":
        lead = FRIEND[i]
        tones = (chord_tones(ch, "D3", "D4") * 2)[:4]
        clean = bar(" ".join(f"{t}:0.5" for t in tones + tones[::-1]))
        b = bar(f"{root}:4,") if i >= 4 else R4
    elif name == "stranger":
        riff = rhy = bar(f"R:0.25 {g}:0.5! {g}:0.25 R:0.75 {g}:0.75! R:0.5 {g}:0.5 R:0.5")
        lead = STRANGER[i]
        b = unison_low(riff, -1, "B0")
        mute = bar("R:2.25 B1:0.25, R:1.5") if i % 2 else R4
    elif name == "mother":
        bell = bar(f"{chord_tones(ch, 'B4', 'B5')[0]}:4") if i % 4 == 0 else R4
        tones = (chord_tones(ch, "E3", "E4") * 2)[:3]
        clean = bar(f"{tones[0]}:2 {tones[1]}:1 {tones[2]}:1")
        b = bar(f"{root}:4,") if i % 2 == 0 else R4
    elif name == "jury":
        riff = rhy = chug if i >= 8 else bar(f"{g}:1! R:1 {g}:1! R:1")
        bell = bar(f"{chord_tones(ch, 'B4', 'B5')[0]}:2 R:2") if i % 4 == 3 else R4
        b = unison_low(riff, -1, "B0")
    elif name == "hush":
        b = R4
    elif name == "verdict":
        bell = bar("C5:4") if i == 0 else (bar("B4:4") if i == 2 else R4)
        riff = rhy = bar(f"{g}:1! R:3") if i in (0, 2) else R4
        b = bar(f"{root}:1! R:3") if i in (0, 2) else R4
    elif name == "sentence":
        riff = rhy = bar(f"{g}:0.75! {g}:0.75! {g}:0.5! R:0.5 {g}:0.5! {tr(g, 1)}:0.5! {g}:0.5!")
        lead = SENT[i] if i >= 8 else R4
        b = unison_low(riff, -1, "B0")
    else:   # toll
        bell = bar("B4:4") if i in (0, 2, 4) else R4
        b = R4
    P["riff"].append(riff); P["rhy"].append(rhy); P["lead"].append(lead); P["clean"].append(clean); P["bell"].append(bell); P["bass"].append(b); P["mute"].append(mute)
    kit.add("X.......X.......", "....X.......X...", "x.x.x.x.x.x.x.x.")

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy")))
song.add(lead_part(J("lead")))
song.add(clean_part(J("clean"), vol=0.08, pan=0.25, role="クリーンの和音（証人）"))
song.add(part("鐘（判決）", "bell", J("bell"), volume=0.15, pan=0.1, reverb=0.5, sustain=2.5, release=1.5,
              fx=[{"type": "eq", "low": -3, "mid": 0, "midHz": 800, "high": 0}, {"type": "reverb", "mix": 0.3}]))
song.add(bass_part(J("bass")))
song.add(bassmute_part(J("mute")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.ref_tone = "dark-electro-rock"

from lm25_plans import apply_plan
apply_plan(song, "24")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-24-tenbin.json"
    song.write(out)
    check_clash(song)
