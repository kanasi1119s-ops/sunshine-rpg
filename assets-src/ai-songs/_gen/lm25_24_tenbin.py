# ラウド25曲（第2シリーズ）24「錆びた天秤」（仮）。イメージ: 罪と罰。B フリジアン・126・4/4。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: 鐘（判決の鐘）
#   ※ 設計表では F♯ フリジアン・7/4 だったが、02「白い螺旋」（F♯ フリジアン・7/4・スラップ・リニアのフィル）と似すぎるので、
#     B フリジアン・4/4 にして、「テンポの感じが天秤のように揺れる」曲にした（ハーフタイム ⇔ 倍のノリ ⇔ 付点4分の拍）。
# 物語: 天秤の片側は「罪」（ハーフタイムの重いリフ、B のペダルに ♭2 の C）、もう片側は「言い訳」（倍のノリ、スラップ、スウィープ、明るい和音）。
#   2つのAメロが交互に重くなり、サビで鐘が判決を告げる。間奏では拍そのものが傾く（付点4分の拍＝メトリック・モジュレーション）。
#   最後は演奏が止まり、鐘だけが鳴り、判決の一撃で終わる。
# しかけ（ほかの曲と変える）:
#   - Aメロが2種類（罪＝ハーフタイム／言い訳＝倍のノリ）で、交互に来る
#   - 間奏（12小節）は付点4分の拍で全員が打つ。3小節で一回りして元の拍に戻る
#   - ギターの技はスウィープ（言い訳の小節の終わりと、ソロの前半）。ベースは言い訳でスラップ、ほかはコードに沿う
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 126, 4
bar = Bars(BEATS)
R4 = bar.rest()

FORM = [("intro", 4), ("sin", 8), ("excuse", 8), ("verdict", 8), ("sin2", 8), ("excuse2", 8), ("verdict2", 8),
        ("weigh", 12), ("solo", 16), ("bell", 2), ("verdict3", 8), ("end", 4)]
SIN = ["Bm", "Bm", "C", "Bm", "Bm", "Bm", "Am", "C"]
EXC = ["G", "Bm", "Em", "D", "G", "Bm", "Am", "C"]
VER = ["Bm", "C", "G", "D", "Em", "Am", "C", "C"]
CH = {"intro": ["Bm", "Bm", "Bm", "C"], "sin": SIN, "excuse": EXC, "verdict": VER, "sin2": SIN, "excuse2": EXC, "verdict2": VER,
      "weigh": ["Bm", "Bm", "Bm", "C", "C", "C", "Am", "Am", "Am", "Em", "F#7", "F#7"],
      "solo": ["Bm", "G", "Em", "F#7", "Bm", "G", "C", "F#7", "Bm", "C", "G", "D", "Em", "C", "Am", "F#7"],
      "bell": ["Bm", "Bm"], "verdict3": VER, "end": ["C", "C", "Bm", "Bm"]}
song = Song("錆びた天秤（仮）",
            "仮: ラウド25曲（第2シリーズ）の24曲目。イメージは罪と罰。B フリジアン・126。罪（ハーフタイムの重いリフ、B のペダルに ♭2 の C）と"
            "言い訳（倍のノリ、スラップ、スウィープ）の2つのAメロが交互に来て、サビで鐘が判決を告げる。間奏は付点4分の拍で全員が打つ（拍が傾く）。"
            "最後は鐘だけが鳴り、判決の一撃。別の楽器は鐘。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 天秤の両側（罪と言い訳）が交互に重くなり、鐘が判決を告げる。"
song.kinds = {"sin": "verse", "excuse": "pre", "verdict": "chorus", "sin2": "verse", "excuse2": "pre", "verdict2": "chorus",
              "weigh": "bridge", "bell": "break", "verdict3": "chorus", "end": "outro"}
SECS, NB = song.secs, song.nb

RIFF = {"Bm": [bar("B1:1.5! B1:0.5 C2:1! B1:0.5 D2:0.5"), bar("B1:1.5! F#2:0.5 E2:1 D2:0.5 C2:0.5")],
        "C": [bar("C2:1.5! C2:0.5 D2:1! C2:0.5 B1:0.5"), bar("C2:1.5! G2:0.5 E2:1 D2:0.5 B1:0.5")],
        "Am": [bar("A2:1.5! A2:0.5 B2:1! A2:0.5 G2:0.5"), bar("A2:1.5! E2:0.5 G2:1 E2:0.5 C2:0.5")]}
SIN_MEL = [bar("R:2 F#4:1 B4:1"), bar("D5:2 B4:2"), bar("E5:1.5 D5:0.5 C5:2"), bar("B4:4"),
           bar("R:2 D5:1 B4:1"), bar("F#5:2 E5:1 D5:1"), bar("C5:2 A4:2"), bar("G4:2 E4:2")]
SIN2_MEL = [bar("R:2 D5:1 B4:1"), bar("F#5:2 D5:2"), bar("G5:1.5 E5:0.5 C5:2"), bar("D5:2 B4:2"),
            bar("R:2 D5:1 F#5:1"), bar("B5:2 A5:1 F#5:1"), bar("E5:2 C5:2"), bar("E5:2 G5:2")]
EXC_MEL = [bar("B4:0.5 D5:0.5 G5:1 F#5:0.5 E5:0.5 D5:1"), bar("A4:0.5 D5:0.5 F#5:1 E5:1 D5:1"),
           bar("E5:0.5 G5:0.5 B5:1 A5:0.5 G5:0.5 E5:1"), bar("F#5:2 R:2"),
           bar("B5:0.5 A5:0.5 G5:1 D5:1 B4:1"), bar("A5:0.5 F#5:0.5 D5:1 F#5:1 A5:1"), bar("C6:1 B5:0.5 A5:0.5 E5:2"), R4]
VER_MEL = [bar("B4:1 D5:1 F#5:2"), bar("G5:1.5 E5:0.5 C5:2"), bar("D5:1 G5:1 B5:2"), bar("A5:1.5 F#5:0.5 D5:2"),
           bar("E5:1 G5:1 B5:1 E6:1"), bar("E6:2 C6:1 A5:1"), bar("G5:1.5 C6:0.5 E5:2"), bar("G5:2^^ R:2")]
# 2回目のサビ: 前半4小節の音域とリズムを変える（同じ4小節を3回くり返さない）
VER2_MEL = [bar("B4:0.5 D5:0.5 F#5:1 B5:2"), bar("G5:1 C6:1 E5:2"), bar("D5:0.5 G5:0.5 B5:1 D6:2"), bar("A5:1 D6:1 F#5:2")] + VER_MEL[4:]
VER3_MEL = VER_MEL[:6] + [bar("A5:1 C6:1 E6:2!"), bar("E6:2^^ R:2")]
SOLO_MEL = [bar("F#5:1 B5:1 D6:2"), bar("E6:1.5 D6:0.5 C6:2"), bar("B5:1 D6:1 G5:2"), bar("F#5:1 A5:1 D6:2"),
            bar("G5:0.5 B5:0.5 E6:1 D6:1 B5:1"), bar("C6:1 E6:1 G5:2"), bar("A5:1 C6:1 E6:2^^"), bar("F#5:1 A#5:1 C#6:1 E6:1")]
SLAP = ["T.gPT.gP.TgPT.gP", "T..PgT.PT.gP.TgS", "TgP.T.gPTgP.T.SP", "T.gP.TgPT.gPTgP."]


def harm_below(line, ch, gap=3):
    """旋律の下で、和音の音からいちばん近い音を選ぶ（休みはそのまま）"""
    pcs = chord_pcs(ch)
    out = []
    for t in line.split():
        n = tok_note(t)
        if n == "R": out.append(t); continue
        m = midi(n) - gap
        while m % 12 not in pcs: m -= 1
        out.append(nm(m) + ":" + t.split(":", 1)[1].replace("!", "").replace("^", ""))
    return " ".join(out)


def split_slap(b):
    pt, mt = [], []
    for t in b.split():
        if t.endswith("'"): pt.append(t); mt.append("R:" + t.split(":")[1].rstrip("'"))
        else: pt.append("R:" + t.split(":")[1].rstrip("!'")); mt.append(t)
    return merge_rests(" ".join(mt)), merge_rests(" ".join(pt))


def dotted(note, j):
    """付点4分の拍（3小節で一回り）。j は一回りの中の小節番号"""
    return [bar(f"{note}:1.5! {note}:1.5! {note}:1!"), bar(f"R:0.5 {note}:1.5! {note}:1.5! {note}:0.5!"), bar(f"R:1 {note}:1.5! {note}:1.5!")][j]


P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "harm", "tech", "bass", "pop", "mute", "bell"]}
kit = Kit(BEATS)
RIDE, BELL, CR, CR2, CHINA = "D2", "F2", "C2", "G2", "B2"
g16 = lambda *pos, ch="X", base=None: kit.grid(pos, ch, base)
fill_seed = 0

for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    ch = song.chords[name][i]
    nxt = song.chord_at(idx + 1) if idx + 1 < NB else ch
    last = i == n - 1
    base_ch = ch.split("/")[0]
    root = root_note(ch)
    groot = up(root, 1) if midi(up(root, 1)) <= midi("D3") else root
    kind = name.rstrip("23")
    broot = root_note(ch, "C4", "B4")

    rf = s = si = lead = harm = tech = bl = R4
    b = R4; pop = mute = R4
    if kind == "intro":
        if i >= 2: rf = RIFF[base_ch][i % 2]
        if i < 2: bl = bar(f"{broot}:4")
    elif kind == "sin":
        rf = RIFF.get(base_ch, [bar(f"{groot}:2! {groot}:2")] * 2)[i % 2]
        lead = (SIN_MEL if name == "sin" else SIN2_MEL)[i]
        if last: bl = bar(f"{broot}:4")
    elif kind == "excuse":
        s = si = bar(f"{groot}:0.5'! R:1 {groot}:0.5' R:0.5 {groot}:0.5' R:1")
        lead = EXC_MEL[i]
        if name == "excuse2" and i not in (3, 7): harm = harm_below(lead, ch)
        if i == 3: tech = "R:2 " + sweep(ch, "B3", "B5", 2)
        if i == 7: tech = sweep(ch, "C4", "C6", 2) + " " + sweep(ch, "G3", "G5", 2); s = si = bar(f"{groot}:4!")
    elif kind == "verdict":
        s = si = bar(f"{groot}:2! {groot}:2") if not (last and name == "verdict3") else bar(f"{groot}:4!")
        lead = {"verdict": VER_MEL, "verdict2": VER2_MEL, "verdict3": VER3_MEL}[name][i]
        if name != "verdict": harm = harm_below(strip_marks(lead), ch)
        bl = bar(f"{broot}:4")
    elif kind == "weigh":
        rf = dotted(groot, i % 3); s = si = rf
        if i % 3 == 0: bl = bar(f"{broot}:4")
    elif kind == "solo":
        if i < 8:
            tech = sweep(ch, "B3", "B5", 2) + " " + sweep(ch, "F#3", "F#5", 2)
            s = si = bar(f"{groot}:2! {groot}:2")
        else:
            lead = SOLO_MEL[i - 8]; s = si = bar(f"{groot}:2! {groot}:2")
    elif kind == "bell":
        bl = bar(f"{broot}:4") if i == 0 else bar("F#4:4")
    elif kind == "end":
        s = si = bar(f"{groot}:1! R:3") if not last else bar(f"{groot}:4!")
        rf = s
        bl = bar(f"{broot}:4")
    P["riff"].append(rf); P["rhy"].append(s); P["rhy_in"].append(si); P["lead"].append(lead); P["harm"].append(harm)
    P["tech"].append(tech); P["bell"].append(bl)

    # ベース
    if kind in ("intro", "sin", "weigh", "end"): b = unison_low(rf, -1, "B0") if rf != R4 else R4
    elif kind == "excuse":
        bb, mute = bass_slap_bar(ch, BEATS, SLAP[i % 4]); b, pop = split_slap(bb)
    elif kind == "verdict": b = bass_root8(ch, 4, nxt) if not (last and name == "verdict3") else bar(f"{root}:4!")
    elif kind == "solo": b = bass_root8(ch, 4, nxt)
    P["bass"].append(b); P["pop"].append(pop); P["mute"].append(mute)

    # ドラム
    k = sn = h = None; tom = cym = None
    fill = last and kind in ("sin", "excuse", "verdict") and not (name == "verdict3")
    if kind == "intro":
        if i == 2: k = g16(0, 10); sn = g16(8); cym = f"{CR}:2! {RIDE}:1 {RIDE}:1"
        if i == 3: k = g16(0); sn = g16(8, 10, 12, 13, 14, 15); cym = f"{CHINA}:1! {RIDE}:1 R:2"
    elif kind == "sin":
        # 罪: ハーフタイム（スネアは3拍目）
        k = g16(0, 3, 10) if i % 2 == 0 else g16(0, 6, 7, 10); sn = g16(8); sn = g16(14, ch="o", base=sn)
        h = g16(0, 4, 8, 12, ch="x")
        if i == 0: cym = f"{CR}:2! R:2"; h = g16(8, 12, ch="x")
    elif kind == "excuse":
        # 言い訳: 倍のノリ（スネアは2・4拍目、ライドのベルで8分）
        k = g16(0, 3, 8, 11); sn = g16(4, 12); sn = g16(7, 15, ch="o", base=sn)
        cym = " ".join([f"{BELL}:0.5!" if j % 2 == 0 else f"{RIDE}:0.5" for j in range(8)])
        if i == 0: cym = f"{CR2}:0.5! " + " ".join([f"{BELL}:0.5!" if j % 2 == 0 else f"{RIDE}:0.5" for j in range(1, 8)])
    elif kind == "verdict":
        k = g16(0, 2, 8, 10, 11); sn = g16(4, 12)
        h = g16(*range(0, 16, 2), ch="x")
        if i % 2 == 0: cym = (f"{CR}:1! " if i % 4 == 0 else f"{CR2}:1! ") + "R:3"; h = g16(4, 6, 8, 10, 12, 14, ch="x")
        if name == "verdict3" and last: k = g16(0); sn = g16(0); h = None; cym = f"{CR}:4!"
    elif kind == "weigh":
        # 付点4分の拍: キックは全員の打点、スネアは1つおき、ライドは打点ごと
        j = i % 3
        hits = [(0, 6, 12), (2, 8, 14), (4, 10)][j]
        k = g16(*hits); sn = g16(*[(6,), (2, 14), (10,)][j])
        k = "".join("." if sn[x] != "." else c for x, c in enumerate(k))
        toks, t = [], 0.0
        for p in hits:
            if p / 4 > t: toks.append(f"R:{p / 4 - t:g}")
            toks.append(f"{CHINA if (j == 0 and p == 0) else RIDE}:1.5!" if p / 4 + 1.5 <= 4 else f"{RIDE}:{4 - p / 4:g}!")
            t = min(4, p / 4 + 1.5)
        if t < 4: toks.append(f"R:{4 - t:g}")
        cym = " ".join(toks)
        if last: k, sn, tom = linear_fill(kit, 2, 3); cym = None
    elif kind == "solo":
        if i < 8:
            k = "".join("X" if x % 4 == 0 else "x" for x in range(16)); sn = g16(4, 12)
            k = "".join("." if sn[x] != "." else c for x, c in enumerate(k))
            cym = f"{RIDE}:1! {RIDE}:1 {RIDE}:1! {RIDE}:1" if i % 4 else f"{CR}:1! {RIDE}:1 {RIDE}:1! {RIDE}:1"
        else:
            k = g16(0, 10); sn = g16(8); h = g16(0, 2, 4, 6, 8, 10, 12, 14, ch="x")
            if i == 8: cym = f"{CR}:2! R:2"; h = g16(8, 10, 12, 14, ch="x")
            if i == 11: tom = "R:2 " + tom_triplets_down(2); h = g16(0, 2, 4, 6, ch="x"); sn = g16()
        if last: k, sn, tom = linear_fill(kit, 2, 1); h = None; cym = f"{RIDE}:1! {RIDE}:1 R:2"
    elif kind == "bell":
        cym = f"R:2 E4:2".replace("E4", "R")
        cym = None
    elif kind == "end":
        k = g16(0); sn = g16(0); cym = f"{CR}:4!"
    if fill:
        k, sn, tom = linear_fill(kit, 2, fill_seed); fill_seed += 1
        k = g16(0, 3, base=k); sn = g16(4, base=sn) if kind != "sin" else sn
        h = None; cym = f"{CR2 if kind != 'sin' else CR}:1! R:3" if kind != "sin" else None
    kit.add(k, sn, h, tom, cym)

FX = []
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    nx = SECS[idx + 1][0] if idx + 1 < NB else ""
    if i == n - 1 and nx.startswith("verdict"): FX.append(bar("R:2 C4:2"))
    elif name == "solo" and i == n - 1: FX.append(bar("E4:4"))
    else: FX.append(R4)

J = lambda k: " ".join(P[k])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm"), vol=0.08, pan=0.3, role="リード（和音の音のハモリ）"))
song.add(tech_part(J("tech"), role="技のギター（スウィープ）"))
song.add(part("鐘（判決）", "bell", J("bell"), volume=0.15, pan=0.1, reverb=0.5, sustain=2.5, release=1.5,
              fx=[{"type": "eq", "low": -3, "mid": 0, "midHz": 800, "high": 0}, {"type": "reverb", "mix": 0.3}]))
song.add(bass_part(J("bass")))
song.add(slap_pop_part(J("pop")))
song.add(bassmute_part(J("mute")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

# 参考の音と追加の楽器（2026-10-23 人間「残り24曲、作った音源のどれかに合わせて」「プラスで何か楽器を追加」）
song.ref_tone = "dark-electro-rock"
add_layer(song, "synth-arp", "天秤の針が、時を刻むように揺れる。")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-24-tenbin.json"
    song.write(out)
    check_clash(song)
