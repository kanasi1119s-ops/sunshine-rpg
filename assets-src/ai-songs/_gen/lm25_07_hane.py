# ラウド26曲 07「Terminal Velocity of a Feather」（仮。もとの仮題「羽の落ちる速さ」）。2026-10-24 素材から作り直し
# スタイル: ポストメタル（空気から始まり、層を重ねて押しつぶすような重さへ）＋ハープ。E リディアン・84 → 132・4/4
# 物語: 天使の羽が一枚、空の一番高い所から落ちていく。落ちるほど速く、重く、低くなり、地面の直前でいちばん重い。着地で無音。羽だけが残る。
# 形: 一本の長い落下（同じ区間に戻らない。テンポも音域も、場面ごとに下がり・速くなる）。ほかの曲と骨組みを変える
# 場面と、そこで必要な強さ:
#   成層圏（0）: ハープときれいな高い音だけ。いちばん高く、軽く、小さい（84）
#   雲（1）: ドラムが静かに入る。音域が少し下がる（96）
#   風（2）: 歪んだギターの壁が入る。3連の流れ（108）
#   急降下（3）: 16分。低く、密に（120）
#   地面の直前（3）: いちばん低く、いちばん重い（132）
#   着地: 1小節の無音
#   羽（0）: ハープだけ（84）
# 旋律の性格: 息つぎをしない、ゆれながら下りる線（3つ下りて1つ上がる＝羽のゆれ）。場面ごとに音の細かさが増す（8分 → 3連 → 16分）
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 84, 4
bar = Bars(BEATS)
R4 = bar.rest()

FORM = [("strato", 24), ("cloud", 20), ("wind", 20), ("dive", 20), ("ground", 8), ("impact", 1), ("feather", 8)]
CH = {"strato": ["E", "F#/E", "Emaj7", "F#/E"] * 6,
      "cloud": ["E", "F#/E", "C#m", "B", "E", "F#/E", "G#m", "B"] * 2 + ["C#m", "B", "A#dim", "B"],
      "wind": ["C#m", "B", "E", "F#", "G#m", "F#", "E", "B"] * 2 + ["C#m", "F#", "B", "B"],
      "dive": ["E", "F#", "G#m", "C#m"] * 4 + ["E", "F#", "B", "B"],
      "ground": ["E", "E", "F#", "F#", "E", "E", "F#", "E"], "impact": ["E"], "feather": ["E", "F#/E", "E", "F#/E", "E", "Emaj7", "E", "E"]}
song = Song("羽の落ちる速さ（仮）",
            "仮: ラウド26曲の7曲目（2026-10-24 素材から作り直し）。ポストメタル＋ハープ。E リディアン。84 から 132 まで、場面ごとに速く・低く・重くなる一本の落下。"
            "着地で無音、ハープだけが残る。旋律は息つぎのない、ゆれながら下りる線。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 天使の羽が一枚、空の一番高い所から落ち、地面の直前でいちばん重くなり、着地のあと羽だけが残る。"
song.kinds = {"strato": "intro", "cloud": "verse", "wind": "pre", "dive": "chorus", "ground": "solo", "impact": "interlude", "feather": "outro"}
SECS, NB = song.secs, song.nb

SCALE = [m for m in range(midi("B2"), midi("E6") + 1) if (m - midi("E2")) % 12 in (0, 2, 4, 6, 7, 9, 11)]


def fall_line(start, end, nbars, rhythms, seed, chords=None):
    """ゆれながら下りる線: 3つ下りて1つ上がる（羽のゆれ）をくり返し、start から end へ。小節ごとに rhythms から形を選ぶ"""
    import random
    rng = random.Random(seed)
    i0 = min(range(len(SCALE)), key=lambda j: abs(SCALE[j] - midi(start)))
    i1 = min(range(len(SCALE)), key=lambda j: abs(SCALE[j] - midi(end)))
    out = []; pos = i0; step = 0
    total_notes = sum(len([d for d in rhythms[b % len(rhythms)] if d > 0]) for b in range(nbars))
    k = 0
    for b in range(nbars):
        r = rhythms[(b + seed) % len(rhythms)]
        toks = []
        for d in r:
            if d < 0: toks.append(f"R:{-d:g}"); continue
            target = i0 + (i1 - i0) * k / max(1, total_notes - 1)
            sway = [-1, -1, -1, 2][step % 4]; step += 1
            pos = max(min(pos + sway, len(SCALE) - 1), 0)
            if pos > target + 2: pos -= 1
            if pos < target - 2: pos += 1
            if chords and d >= 1:                      # 1拍以上の音は和音の音に（長7度・半音でぶつからない）
                pcs = chord_pcs(chords[b].split("/")[0])
                pos = min((q for q in range(max(0, pos - 2), min(len(SCALE), pos + 3)) if SCALE[q] % 12 in pcs), key=lambda q: abs(q - pos), default=pos)
            toks.append(f"{nm(SCALE[pos])}:{d:g}"); k += 1
        out.append(bar(" ".join(toks)))
    return out


R8 = [[0.5] * 8, [1, 0.5, 0.5, 0.5, 0.5, 1], [0.5, 0.5, 1, 0.5, 0.5, 0.5, 0.5], [1.5, 0.5, 0.5, 0.5, 1]]
S16 = [[0.25] * 8 + [0.5] * 4, [0.5, 0.25, 0.25, 0.5, 0.25, 0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25], [0.25] * 16, [0.75, 0.25, 0.25, 0.25, 0.5] * 2]


def line_T3(start, end, nb, seed, chords=None):
    rs = [[1 / 3] * 3 + [0.5, 0.5] + [1 / 3] * 3 + [1], [1, 1 / 3, 1 / 3, 1 / 3, 1, 1 / 3, 1 / 3, 1 / 3], [0.5, 0.5] + [1 / 3] * 6 + [1]]
    rs = [[0.3333 if abs(x - 1 / 3) < 1e-6 else x for x in r] for r in rs]
    raw = fall_line_free(start, end, nb, rs, seed, chords)
    return [bar(fix_len(s, 4)) for s in raw]


def fall_line_free(start, end, nbars, rhythms, seed, chords=None):
    import random
    rng = random.Random(seed)
    i0 = min(range(len(SCALE)), key=lambda j: abs(SCALE[j] - midi(start)))
    i1 = min(range(len(SCALE)), key=lambda j: abs(SCALE[j] - midi(end)))
    out = []; pos = i0; step = 0; k = 0
    total_notes = sum(len(rhythms[b % len(rhythms)]) for b in range(nbars))
    for b in range(nbars):
        r = rhythms[(b + seed) % len(rhythms)]
        toks = []
        for d in r:
            target = i0 + (i1 - i0) * k / max(1, total_notes - 1)
            sway = [-1, -1, -1, 2][step % 4]; step += 1
            pos = max(min(pos + sway, len(SCALE) - 1), 0)
            if pos > target + 2: pos -= 1
            if pos < target - 2: pos += 1
            if chords and d >= 0.9:
                pcs = chord_pcs(chords[b].split("/")[0])
                pos = min((q for q in range(max(0, pos - 2), min(len(SCALE), pos + 3)) if SCALE[q] % 12 in pcs), key=lambda q: abs(q - pos), default=pos)
            toks.append(f"{nm(SCALE[pos])}:{d:g}"); k += 1
        out.append(" ".join(toks))
    return out


MEL = {"strato": fall_line("F#5", "C#5", 24, R8, 1, CH["strato"]), "cloud": fall_line("C#5", "G#4", 20, R8, 2, CH["cloud"])}
MEL["wind"] = line_T3("A4", "E4", 20, 3, CH["wind"])
MEL["dive"] = fall_line("E4", "G#3", 20, S16, 4, CH["dive"])
MEL["ground"] = fall_line("G#3", "E3", 7, S16, 5, CH["ground"]) + [bar("E3:4!")]

LOW = {"E": "E2", "F#/E": "E2", "Emaj7": "E2", "C#m": "C#2", "B": "B1", "A#dim": "A#1", "F#": "F#1", "G#m": "G#1"}


def harp_bar(ch, lo, hi, step=0.25):
    t = chord_tones(ch.split("/")[0], lo, hi)
    seq = t + t[-2:0:-1]
    n = int(round(4 / step))
    return bar(" ".join(f"{seq[j % len(seq)]}:{step:g}" for j in range(n)))


P = {k: [] for k in ["riff", "rhy", "lead", "clean", "harp", "bass"]}
kit = Kit(BEATS)
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]; ch = song.chords[name][i]
    riff = rhy = lead = clean = harp = R4
    root = root_note(ch); g = LOW[ch]
    if name == "strato":
        harp = harp_bar(ch, "E4", "E6", 0.5); lead = MEL["strato"][i] if i >= 4 else R4
        b = R4
    elif name == "cloud":
        harp = harp_bar(ch, "B3", "B5", 0.5) if i % 2 == 0 else R4
        lead = MEL["cloud"][i]
        clean = bar(" ".join(f"{t}:1" for t in chord_tones(ch.split('/')[0], 'G#3', 'E5')[:4]))
        b = bar(f"{root}:4,") if i >= 4 else R4
    elif name == "wind":
        riff = rhy = bar(f"{g}:1.5! {g}:1 {tr(g, 7)}:1.5")
        lead = MEL["wind"][i]
        harp = harp_bar(ch, "G#3", "G#5", 0.25) if i % 4 == 3 else R4
        b = bar(f"{root}:1.5! {root}:1 {fifth_of(ch)}:1.5")
    elif name == "dive":
        riff = rhy = bar(" ".join(f"{g}:0.25{'!' if j % 4 == 0 else ''}" for j in range(16)))
        lead = MEL["dive"][i]
        b = bar(" ".join(f"{root}:0.5{'!' if j % 2 == 0 else ''}" for j in range(8)))
    elif name == "ground":
        riff = rhy = bar(f"{g}:0.75! {g}:0.75! {g}:0.5! {g}:0.25 {g}:0.25 {g}:0.5! {tr(g, 1)}:0.5! {g}:0.5!") if i < 7 else bar(f"{g}:2! {g}:2!")
        lead = MEL["ground"][i]
        b = unison_low(riff, -1, "B0")
    elif name == "impact":
        b = R4                                                       # 着地: 1小節の無音
    else:   # feather
        harp = {0: bar("R:1 E5:0.5 B4:0.5 G#4:2"), 2: bar("R:1 F#5:0.5 D#5:0.5 B4:2"), 4: bar("R:2 E5:0.5 G#4:1.5"), 6: bar("B4:4"), 7: bar("E4:4")}.get(i, R4)
        b = R4
    P["riff"].append(riff); P["rhy"].append(rhy); P["lead"].append(lead); P["clean"].append(clean); P["harp"].append(harp); P["bass"].append(b)
    kit.add("X.......X.......", "....X.......X...", "x.x.x.x.x.x.x.x.")

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy")))
song.add(lead_part(J("lead")))
song.add(clean_part(J("clean"), vol=0.07, pan=0.25, role="クリーンの和音（雲）"))
song.add(part("ハープ", "harp", J("harp"), volume=0.13, pan=-0.3, reverb=0.45, attack=0.002, release=1.2,
              fx=[{"type": "eq", "low": -4, "mid": 0, "midHz": 1500, "high": 1.5}, {"type": "delay", "beats": 0.75, "mix": 0.15, "feedback": 0.3}, {"type": "plate", "mix": 0.25}]))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))

song.auto_harm = song.auto_oct = song.auto_air = song.auto_range = False
song.auto_scream = False
song.ref_tone = "bright-pop-rock"

from lm25_plans import apply_plan
apply_plan(song, "07")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-07-hane.json"
    song.write(out)
    check_clash(song)
