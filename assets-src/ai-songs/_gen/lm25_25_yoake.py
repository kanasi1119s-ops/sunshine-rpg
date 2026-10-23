# ラウド25曲（第2シリーズ）25「夜明けの闇市」（仮）。イメージ: 闇市×天使（全25曲の終曲）。E 短調 → E 長調・112・4/4。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: バイオリン（闇市の主題・通りすがりの引用・夜明けの旋律）
# 物語: 夜明け前の闇市。バイオリンが一人で 13「闇市の値札」のリフを弾き、バンドが入る。
#   市場の中ほど（ジャズの区間）では、これまでの曲の動機が通りすがりの人のように顔を出す
#   （22 難破船の舟歌 → 01 路地裏のサビ → 23 焼け野原の国歌 → 07 天使の羽のサビ。どれもこの曲の和音に合わせて形を変える）。
#   夜明け前の争い（タッピング）、ギターとバイオリンの掛け合い（スウィープ⇔バイオリン）、一瞬の静けさ、
#   そして E 長調の夜明け。最後はバイオリンが闇市のリフを長調で弾き、E の長三和音で朝になる。
# しかけ（ほかの曲と変える）:
#   - 終曲として「引用」で組み立てる。サビの旋律は、ほかの曲によくある「8分3つの上り＋長い音」の形を使わず、拍の頭の長い音から始める
#   - ギターの技はタッピング（間奏）とスウィープ（掛け合い）。ベースはジャズのウォーキング（市場）とコードに沿う8分
#   - ドラム: 市場はライドのレガート（付点8分＋16分）とスネアのゴースト、タッピングはツーバス、夜明けはシンバルだけ
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 112, 4
bar = Bars(BEATS)
R4 = bar.rest()

VERSE = ["Em7", "Cmaj7", "Am7", "B7", "Em7", "Cmaj7", "F#m7b5", "B7"]
PRE = ["Am7", "D7", "Gmaj7", "B7"]
CHORUS = ["Em", "C", "G", "D", "Am", "Em/G", "F", "B7"]
FORM = [("intro", 4), ("riff", 4), ("verse", 8), ("pre", 4), ("chorus", 8), ("market", 8), ("verse2", 8), ("pre2", 4), ("chorus2", 8),
        ("tap", 8), ("trade", 8), ("still", 2), ("dawn", 4), ("chorusM", 8), ("outro", 4)]
CH = {"intro": ["Em7", "Em7", "A9", "B7"], "riff": ["Em7", "Em7", "A9", "B7#9"], "verse": VERSE, "pre": PRE, "chorus": CHORUS,
      "market": ["Am7", "D7", "Gmaj7", "Cmaj7", "F#m7b5", "B7", "Em7", "B7"], "verse2": VERSE, "pre2": PRE, "chorus2": CHORUS,
      "tap": ["Em", "C", "Am", "B", "Em", "C", "D", "B7"], "trade": ["Em", "Em", "C", "C", "Am", "Am", "B7", "B7"],
      "still": ["B7", "B7"], "dawn": ["E", "A", "C#m", "B"], "chorusM": ["E", "C#m", "A", "B", "A", "E/G#", "F#m7", "B7"],
      "outro": ["E", "A", "E", "E"]}
song = Song("夜明けの闇市（仮）",
            "仮: ラウド25曲（第2シリーズ）の25曲目（終曲）。イメージは闇市と天使。E 短調 → E 長調・112。バイオリンが一人で闇市のリフを弾いて始まり、"
            "市場の中ほどのジャズの区間で、これまでの曲（難破船・路地裏・焼け野原の国歌・天使の羽）の動機が通りすがりに顔を出す。"
            "タッピングの争い、スウィープとバイオリンの掛け合い、一瞬の静けさのあと E 長調の夜明け。別の楽器はバイオリン。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 全25曲の終わり。闇市に朝が来る。"
song.kinds = {"riff": "interlude", "market": "bridge", "tap": "solo", "trade": "solo", "still": "break", "dawn": "interlude", "chorusM": "chorus"}
song.flags = "--space hall --space-wet 0.12"
SECS, NB = song.secs, song.nb
song.pickups = ['V1']   # 8分3つの上りの型を、この曲だけのリズムに（lm25_lib.vary_pickups）

# 13「闇市の値札」の看板リフ（B♭ → E へ移す）
RIFF = {"Em7": [bar("E2:0.5! R:0.25 E2:0.25 G2:0.5 A2:0.25 A#2:0.25 B2:0.5 R:0.5 D3:0.25 B2:0.25 E3:0.5"),
                bar("E2:0.5! R:0.25 E2:0.25 G2:0.5 A2:0.25 B2:0.25 D3:0.5 B2:0.5 A2:0.25 G2:0.25 E2:0.5")],
        "A9": [bar("A2:0.5! R:0.25 A2:0.25 C#3:0.5 E3:0.25 G3:0.25 B3:0.5 R:0.5 G3:0.25 E3:0.25 C#3:0.5")] * 2,
        "B7#9": [bar("B1:0.5! R:0.25 B1:0.25 D#2:0.5 F#2:0.25 A2:0.25 D3:0.5 R:0.5 D#3:0.25 D3:0.25 B2:0.5")] * 2}
VLN_INTRO = [transpose(RIFF["Em7"][0], 24), transpose(RIFF["Em7"][1], 24), bar("C#5:2 E5:1 G5:1"), bar("F#5:2 D#5:2")]

VERSE_MEL = [bar("E4:1 G4:0.5 B4:0.5 D5:1 B4:1"), bar("E5:1.5 D5:0.5 B4:1 G4:1"), bar("A4:0.5 C5:0.5 E5:0.5 G5:0.5 E5:2"), bar("D#5:1 F#5:1 A5:1 F#5:1"),
             bar("G5:1 F#5:0.5 E5:0.5 D5:1 B4:1"), bar("C5:1 E5:1 G5:1.5 E5:0.5"), bar("A5:1 C6:1 E5:1 F#5:1"), bar("D#5:2 B4:2")]
VERSE2_MEL = [bar("B4:0.5 E5:1 G5:0.5 B5:1 A5:1"), bar("G5:1.5 E5:0.5 B4:2"), bar("C5:0.5 E5:1 A5:0.5 C6:1 A5:1"), bar("B5:1 A5:1 F#5:1 D#5:1"),
              bar("E5:0.5 G5:1 B5:0.5 E6:2"), bar("D6:1 B5:1 G5:1 E5:1"), bar("C6:1.5 A5:0.5 F#5:1 E5:1"), bar("F#5:2 D#5:2")]
PRE_MEL = [bar("C5:2 E5:2"), bar("F#5:2 A5:2"), bar("B5:2 D6:2"), bar("D#6:3 R:1")]
PRE2_MEL = [bar("E5:1 C5:1 E5:1 A5:1"), bar("A5:1 F#5:1 A5:1 C6:1"), bar("D6:1 B5:1 F#5:1 D6:1"), bar("D#6:2^ R:2")]
# サビ（拍の頭の長い音から）
CHORUS_MEL = [bar("B5:3 G5:1"), bar("E5:1 G5:1 C6:2"), bar("B5:1.5 A5:0.5 G5:1 D5:1"), bar("F#5:3 A5:1"),
              bar("C6:2 B5:1 A5:1"), bar("G5:1 B5:1 E6:2"), bar("A5:1 C6:1 F5:2"), bar("D#6:2 B5:1 F#5:1")]
CHORUS2_MEL = CHORUS_MEL[:7] + [bar("D#6:1 F#6:1".replace("F#6", "B5") + " A5:1 F#5:1")]
CHORUSM_MEL = [bar("B5:3 G#5:1"), bar("E5:1 G#5:1 C#6:2"), bar("C#6:1.5 B5:0.5 A5:1 E5:1"), bar("F#5:3 D#6:1"),
               bar("C#6:2 B5:1 A5:1"), bar("G#5:1 B5:1 E6:2"), bar("A5:1 C#6:1 E6:2!"), bar("D#6:2 B5:1 F#5:1")]
# 市場: 通りすがりの引用（バイオリン）
MARKET_VLN = [bar("E5:1 F#5:0.5 G5:0.5 E5:1 C5:1"), bar("F#5:1 E5:0.5 D5:0.5 A4:2"),                # 22 難破船の舟歌
              bar("R:0.5 B4:0.5 D5:0.5 F#5:0.5 A5:2"), bar("C5:1 A4:0.5 B4:0.5 C5:2"),              # 01 路地裏のサビ
              bar("E5:1 A5:1 C6:1.5 B5:0.5"), bar("F#5:1.5 A5:0.5 D#5:1 F#5:1"),                     # 23 焼け野原の国歌
              bar("R:0.5 B4:0.5 E5:0.5 G5:0.5 B5:2"), bar("F#5:1 D#5:0.5 F#5:0.5 B5:2")]             # 07 天使の羽のサビ
DAWN_VLN = [bar("G#5:2 B5:2"), bar("C#6:3 B5:1"), bar("G#5:2 E5:2"), bar("F#5:2 D#5:1 B4:1")]
OUTRO_VLN = [bar("E5:0.5! R:0.25 E5:0.25 G#5:0.5 A5:0.25 B5:0.25 C#6:0.5 R:0.5 B5:0.25 G#5:0.25 E6:0.5"), bar("C#6:2 A5:2"), bar("B5:4"), bar("E6:4")]


def harm_below(line, ch, gap=3):
    pcs = chord_pcs(ch)
    out = []
    for t in line.split():
        n = tok_note(t)
        if n == "R": out.append(t); continue
        m = midi(n) - gap
        while m % 12 not in pcs: m -= 1
        out.append(nm(m) + ":" + t.split(":", 1)[1].replace("!", "").replace("^", ""))
    return " ".join(out)


def arp16(ch, lo="E4", hi="E6", beats_len=4):
    t = chord_tones(ch, lo, hi)
    seq = t + t[-2:0:-1]
    return " ".join(f"{seq[j % len(seq)]}:0.25{'!' if j % 4 == 0 else ''}" for j in range(int(beats_len * 4)))


P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "harm", "tech", "clean", "vln", "bass"]}
kit = Kit(BEATS)
RIDE, BELL, CR, CR2, CHINA = "D2", "F2", "C2", "G2", "B2"
g16 = lambda *pos, ch="X", base=None: kit.grid(pos, ch, base)
fseed = 0

for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    ch = song.chords[name][i]
    nxt = song.chord_at(idx + 1) if idx + 1 < NB else ch
    last = i == n - 1
    base_ch = ch.split("/")[0]
    root = root_note(ch)
    groot = up(root, 1)
    kind = name.rstrip("2")

    rf = s = si = lead = harm = tech = cl = vl = R4
    if name == "intro":
        vl = VLN_INTRO[i]
        t = chord_tones(ch, "E3", "E5"); cl = bar(" ".join(f"{t[j % len(t)]}:1" for j in (0, 2, 1, 3))) if i >= 2 else R4
    elif name == "riff":
        rf = RIFF[base_ch][i % 2]
        if i < 2: vl = shift_oct(strip_marks(rf), 2)
    elif kind == "verse":
        rf = RIFF["Em7"][i % 2] if base_ch == "Em7" else R4
        if rf == R4: s = si = bar(f"{groot}:2! {groot}:1.5 {groot}:0.5") if not last else bar(f"{groot}:2! R:2")
        lead = (VERSE_MEL if name == "verse" else VERSE2_MEL)[i]
        if name == "verse2" and i % 2 == 1: vl = bar(" ".join(f"{x}:2" for x in chord_tones(ch, "G4", "G5")[:2]))
    elif kind == "pre":
        s = si = bar(f"{groot}:1! {groot}:1 {groot}:1 {groot}:1") if not last else bar(f"{groot}:3! R:1")
        lead = (PRE_MEL if name == "pre" else PRE2_MEL)[i]
    elif kind == "chorus":
        s = si = bar(f"{groot}:1.5! {groot}:0.5 {groot}:1 {groot}:1") if not last else bar(f"{groot}:2! {groot}:2")
        lead = (CHORUS_MEL if name == "chorus" else CHORUS2_MEL)[i]
        if name == "chorus2":
            harm = harm_below(lead, ch)
            vl = bar(" ".join(f"{x}:2" for x in chord_tones(ch, "B4", "B5")[:2]))
    elif name == "market":
        vl = MARKET_VLN[i]
        t = chord_tones(ch, "E3", "D5")
        cl = bar(f"R:0.5 {t[1]}:1 R:1 {t[2]}:0.5 R:1") if i % 2 == 0 else bar(f"{t[0]}:1.5 R:1 {t[3 % len(t)]}:1 R:0.5")
    elif name == "tap":
        t = chord_tones(ch, "G4", "G6")
        tech = tap([t[0], t[1], t[3]], 2) + " " + tap([t[1], t[2], t[4]], 2)
        s = si = bar(f"{groot}:2! {groot}:2")
        if i >= 4: vl = bar(" ".join(f"{x}:2" for x in chord_tones(ch, "B4", "B5")[:2]))
    elif name == "trade":
        if i % 2 == 0: tech = sweep(ch, "E3", "E5", 2) + " " + sweep(ch, "B3", "B5", 2)
        else: vl = arp16(ch)
        s = si = bar(f"{groot}:4!")
    elif name == "still":
        if i == 0: s = si = bar(f"{groot}:1! R:3"); rf = bar("B1:1! R:3")
    elif name == "dawn":
        vl = DAWN_VLN[i]
        t = chord_tones(ch, "E3", "E5"); cl = bar(" ".join(f"{t[j % len(t)]}:0.5" for j in (0, 2, 4, 3, 1, 3, 2, 4)))
    elif name == "chorusM":
        s = si = bar(f"{groot}:1.5! {groot}:0.5 {groot}:1 {groot}:1")
        lead = CHORUSM_MEL[i]; harm = harm_below(strip_marks(lead), ch)
        vl = bar(" ".join(f"{x}:2" for x in chord_tones(ch, "B4", "B5")[:2]))
    elif name == "outro":
        vl = OUTRO_VLN[i]
        s = si = R4 if i < 2 else bar(f"{groot}:4!")
        if i == 1: s = si = bar(f"{groot}:4")
    P["riff"].append(rf); P["rhy"].append(s); P["rhy_in"].append(si); P["lead"].append(lead); P["harm"].append(harm)
    P["tech"].append(tech); P["clean"].append(cl); P["vln"].append(vl)

    # ベース
    b = R4
    if name == "intro" and i >= 2: b = bar(f"{root}:4")
    elif name == "riff" or (kind == "verse" and rf != R4): b = unison_low(rf, -1, "B0")
    elif kind == "verse": b = bass_root8(ch, 4, nxt) if not last else bar(f"{root}:2! R:2")
    elif name == "market": b = bass_walk(ch, nxt, 4)
    elif kind in ("pre", "chorus") or name in ("tap", "trade", "chorusM"): b = bass_root8(ch, 4, nxt)
    elif name == "still": b = bar(f"{root}:1! R:3") if i == 0 else R4
    elif name == "dawn": b = bar(f"{root}:4")
    elif name == "outro": b = bar(f"{root}:4") if i < 3 else bar(f"{root}:4!")
    if kind == "chorus" and last and name == "chorus": b = bass_root8(ch, 4, nxt)
    P["bass"].append(b)

    # ドラム
    k = sn = h = None; tom = cym = None
    if name == "intro":
        if i >= 2: cym = f"{RIDE}:1, {RIDE}:1, {RIDE}:1, {RIDE}:1," if i == 2 else f"{RIDE}:1, {RIDE}:1, R:1 {CR}:1"
        if i == 3: sn = g16(8, 10, 12, 13, 14, 15)
    elif name == "riff":
        k = g16(0, 3, 6, 10); sn = g16(4, 12); h = g16(*range(0, 16, 2), ch="x")
        if i == 0: cym = f"{CR}:1! R:3"; h = g16(4, 6, 8, 10, 12, 14, ch="x")
        if last: k, sn, tom = linear_fill(kit, 2, 0); h = g16(0, 2, 4, 6, ch="x")
    elif kind == "verse":
        k = g16(0, 3, 6, 10) if i % 2 == 0 else g16(0, 6, 10, 11); sn = g16(4, 12); h = g16(*range(0, 16, 2), ch="x")
        if i == 0: cym = f"{CR2}:1! R:3"; h = g16(4, 6, 8, 10, 12, 14, ch="x")
        if last: k = g16(0); sn = g16(4); h = g16(0, 2, ch="x"); tom = "R:2 " + tom_triplets_down(2)
    elif kind == "pre":
        k = g16(0, 2, 8, 10); sn = g16(4, 12)
        cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if last: k = g16(0, 12); sn = g16(4, 8, 9, 10, 11); cym = f"{RIDE}:1! R:3"
    elif kind == "chorus" or name == "chorusM":
        k = g16(0, 2, 6, 8, 10, 14); sn = g16(4, 12); h = g16(*range(0, 16, 2), ch="x")
        if i % 2 == 0: cym = (f"{CR}:1! " if i % 4 == 0 else f"{CR2}:1! ") + "R:3"; h = g16(4, 6, 8, 10, 12, 14, ch="x")
        if name == "chorusM" and i >= 4: k = "".join("X" if x % 2 == 0 else "x" for x in range(16)); k = "".join("." if sn[x] != "." else c for x, c in enumerate(k))
        if last and name != "chorusM": k, sn, tom = linear_fill(kit, 2, fseed); fseed += 1; h = g16(0, 2, 4, 6, ch="x")
        if last and name == "chorusM": k = g16(0, 8); sn = g16(4); h = None; cym = f"{CR}:1! R:3"; tom = "R:2 " + tom_16_down(2)
    elif name == "market":
        # ジャズ: ライドのレガート（付点8分＋16分）、キックはごく弱く、スネアのゴースト
        cym = f"{RIDE}:1! {RIDE}:0.75 {RIDE}:0.25, {RIDE}:1! {RIDE}:0.75 {RIDE}:0.25,"
        h = None; k = g16(0, 8, ch="o") if i % 2 == 0 else g16(0, ch="o")
        sn = g16(7, 14, ch="o") if i % 2 == 0 else g16(3, 11, 15, ch="o")
        if i == 3: sn = g16(3, 10, 11, ch="o"); sn = g16(12, ch="x", base=sn)
        if last: tom = "R:2 " + tom_16_down(2); cym = f"{RIDE}:1! {RIDE}:1 R:2"; sn = None
    elif name == "tap":
        k = "".join("X" if x % 4 == 0 else "x" for x in range(16)); sn = g16(4, 12); k = "".join("." if sn[x] != "." else c for x, c in enumerate(k))
        cym = f"{CHINA}:1! {RIDE}:1 {RIDE}:1! {RIDE}:1" if i % 4 == 0 else f"{RIDE}:1! {RIDE}:1 {RIDE}:1! {RIDE}:1"
        if last: k, sn, tom = linear_fill(kit, 2, 2); cym = f"{RIDE}:1! {RIDE}:1 R:2"
    elif name == "trade":
        # 掛け合い: ギターの小節はハーフタイム、バイオリンの小節は倍のノリ
        if i % 2 == 0: k = g16(0, 3, 10); sn = g16(8); h = g16(0, 4, 8, 12, ch="x"); cym = f"{CR}:1! R:3" if i == 0 else None
        else: k = g16(0, 3, 8, 11); sn = g16(4, 12); h = g16(*range(0, 16, 2), ch="x")
        if last: k = g16(0); sn = g16(0); h = None; cym = f"{CR}:1! R:3"
    elif name == "still":
        if i == 0: k = g16(0); sn = g16(0); cym = f"{CR}:4!"
    elif name == "dawn":
        cym = f"{RIDE}:2, {RIDE}:2," if i < 2 else f"{BELL}:1! {RIDE}:1, {BELL}:1! {RIDE}:1,"
        if i == 3: k = g16(0, 8); tom = "R:3 " + tom_16_down(1)
    elif name == "outro":
        if i < 2: cym = f"{RIDE}:1! {RIDE}:1, {BELL}:1! {RIDE}:1,"; k = g16(0, ch="x")
        else: k = g16(0); sn = g16(0); cym = f"{CR}:4!" if i == 2 else f"{CR2}:4!"
    kit.add(k, sn, h, tom, cym)

FX = []
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    nx = SECS[idx + 1][0] if idx + 1 < NB else ""
    if i == n - 1 and nx.startswith("chorus"): FX.append(bar("R:2 C4:2"))
    elif name == "still" and i == 1: FX.append(bar("E4:4"))
    else: FX.append(R4)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm"), vol=0.08, pan=0.3, role="リード（和音の音のハモリ）"))
song.add(tech_part(J("tech"), role="技のギター（タッピング・スウィープ）"))
song.add(clean_part(J("clean"), vol=0.09, pan=0.25, role="クリーンの和音"))
song.add(part("バイオリン", "strings", J("vln"), patch="violin", volume=0.15, pan=-0.18, reverb=0.5, gainDb=3, bright=-0.15, attack=0.3, release=0.7,
              fx=[{"type": "eq", "low": 1, "mid": -2, "midHz": 2800, "high": 0}, {"type": "reverb", "mix": 0.22}, {"type": "plate", "mix": 0.12}]))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

# 参考の音と追加の楽器（2026-10-23 人間「残り24曲、作った音源のどれかに合わせて」「プラスで何か楽器を追加」）
song.ref_tone = "bright-pop-rock"
add_layer(song, "piano", "夜明けの闇市に、朝のピアノが差しこむ。")

# 展開の型（2026-10-23 人間「展開が全曲同じ」「4分から5分」）。lm25_plans.py
from lm25_plans import apply_plan
apply_plan(song, "25")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-25-yoake.json"
    song.write(out)
    check_clash(song)
