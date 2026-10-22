# ラウド25曲（第2シリーズ）23「焼け野原の国歌」（仮）。イメージ: 戦争（焼け跡で鳴る国歌）。C 短調 → E♭ 長調・80・4/4。インスト
# 設計表: docs/sound/lm25-plan.md。別の楽器: ピアノ（焼け跡に残ったピアノ。国歌の旋律を一人で弾く）
# 物語: 焼け野原に残ったピアノが、こわれかけた国歌を一人で弾く → 葬送の行進（スネアの行進とハーフタイムのリフ）
#   → 国歌は短調のまま、ギター二本で歌われる → 点呼（スネアと床タムだけ。名前を呼ぶたび、リードが大きなチョーキングで泣く）
#   → 大きなチョーキングのソロ → 国歌が E♭ 長調で、全員で堂々と鳴る → 最後はまたピアノ一人、短調の最初の4小節を弾き、G で止まる（答えのない終わり）
# しかけ（ほかの曲と変える）:
#   - 主題（国歌）は1つだけ。ピアノ（短調）→ ギター二本（短調）→ 全員（長調）→ ピアノ（短調・途中で止まる）と、同じ旋律の着る服が変わる
#   - ハモリは機械的な3度ではなく、その小節の和音の音から「旋律の下でいちばん近い音」を選ぶ（和音の外に出ない）
#   - リードは大きなチョーキング（全音・1音半を保つ）。速弾きはしない。ビブラートなし
#   - ベースはコードに沿う（根音・5度・オクターブ・経過音）
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 80, 4
bar = Bars(BEATS)
R4 = bar.rest()

THEME_CH = ["Cm", "Ab", "Eb", "Bb", "Fm", "Cm/G", "G7", "Cm"]
FORM = [("intro", 8), ("march", 4), ("verse", 8), ("chorus", 8), ("inter", 2), ("verse2", 8), ("chorus2", 8),
        ("roll", 8), ("solo", 8), ("anthem", 8), ("outro", 4)]
VERSE = ["Cm", "Cm", "Ab", "Ab", "Fm", "Fm", "G", "G"]
CH = {"intro": THEME_CH, "march": ["Cm"] * 4, "verse": VERSE, "chorus": THEME_CH, "inter": ["Cm", "G"], "verse2": VERSE, "chorus2": THEME_CH,
      "roll": ["Ab", "Ab", "Fm", "Fm", "Db", "Db", "G", "G"], "solo": ["Cm", "Ab", "Fm", "G", "Cm", "Ab", "Db", "Bb7"],
      "anthem": ["Eb", "Cm", "Ab", "Bb", "Gm", "Ab", "Bb", "Eb"], "outro": ["Cm", "Ab", "Fm", "G"]}
song = Song("焼け野原の国歌（仮）",
            "仮: ラウド25曲（第2シリーズ）の23曲目。イメージは戦争（焼け跡で鳴る国歌）。C 短調 → E♭ 長調・80。焼け跡のピアノが一人で弾く国歌、"
            "スネアの葬送行進とハーフタイムのリフ、ギター二本の短調の国歌、スネアと床タムだけの点呼、大きなチョーキングのソロ、E♭ 長調の堂々とした国歌、"
            "最後はまたピアノ一人で G で止まる。別の楽器はピアノ。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 焼け野原のピアノ、葬送の行進、点呼、そして国歌は長調に。けれど最後のピアノは答えを出さない。"
song.kinds = {"march": "interlude", "inter": "interlude", "roll": "bridge", "solo": "solo", "anthem": "chorus"}
song.flags = "--space hall --space-wet 0.12"
SECS, NB = song.secs, song.nb

# 国歌（主題）。短調と長調
THEME = [bar("G4:1.5 G4:0.5 C5:1 D5:1"), bar("Eb5:2 C5:1 Ab4:1"), bar("Bb4:1.5 Eb5:0.5 G5:1 F5:1"), bar("F5:2 D5:2"),
         bar("C5:1 F5:1 Ab5:1.5 G5:0.5"), bar("G5:1 Eb5:1 C5:2"), bar("D5:1.5 F5:0.5 B4:1 D5:1"), bar("C5:4")]
THEME_MAJ = [bar("Bb4:1.5 Bb4:0.5 Eb5:1 F5:1"), bar("G5:2 Eb5:1 C5:1"), bar("C5:1.5 Eb5:0.5 Ab5:2"), bar("F5:1 Bb5:1 D6:2!"),
             bar("D5:1 G5:1 Bb5:2"), bar("C6:1 Ab5:1 Eb5:2"), bar("F5:1.5 Ab5:0.5 D5:1 F5:1"), bar("Eb5:4!")]
OUTRO_MEL = [THEME[0], THEME[1], bar("Ab4:1 C5:1 F4:2"), bar("G4:4")]
VERSE_MEL = [bar("R:2 G4:1 C5:1"), bar("Eb5:1.5 D5:0.5 C5:2"), bar("R:2 Ab4:1 C5:1"), bar("Eb5:1.5 F5:0.5 Eb5:2"),
             bar("R:1 F4:1 Ab4:1 C5:1"), bar("F5:2 Eb5:1 C5:1"), bar("D5:1.5 B4:0.5 G4:2"), R4]
VERSE2_MEL = [bar("R:2 C5:1 Eb5:1"), bar("G5:1.5 F5:0.5 Eb5:2"), bar("R:2 C5:1 Eb5:1"), bar("Ab5:1.5 G5:0.5 Eb5:2"),
              bar("R:1 Ab4:1 C5:1 F5:1"), bar("Ab5:2 F5:1 C5:1"), bar("B4:1.5 D5:0.5 G5:2"), R4]
# 点呼: 名前を呼ぶたびに大きなチョーキング（保つ）
ROLL_LEAD = [R4, R4, R4, R4, bar("Ab5:4^^"), bar("R:2 Db6:2^^"), bar("D6:3^^ R:1"), bar("B5:2 G5:2")]
# ソロ: 大きなチョーキング（全音・1音半）。速弾きしない
SOLO = [bar("R:1 G5:1 Bb5:2^^"), bar("C6:1.5 Bb5:0.5 Ab5:1 Eb5:1"), bar("F5:1 Ab5:1 C6:2"), bar("R:0.5 D5:0.5 G5:1 A5:2^^"),
        bar("R:1 F5:1 G5:2^^^"), bar("Ab5:1.5 C6:0.5 Eb6:2"), bar("F5:1 Ab5:1 Db6:2^^"), bar("Ab5:4^^")]
RIFF = [bar("C2:2! Eb2:1 D2:1"), bar("C2:1.5! G2:0.5 Ab2:1 G2:1")]


def harm_below(line, ch, gap=3):
    """旋律の下で、和音の音からいちばん近い音を選ぶ（休みはそのまま）"""
    pcs = chord_pcs(ch)
    out = []
    for t in line.split():
        n = tok_note(t)
        if n == "R": out.append(t); continue
        m = midi(n) - gap
        while m % 12 not in pcs: m -= 1
        out.append(nm(m, True) + ":" + t.split(":", 1)[1].replace("!", "").replace("^", ""))
    return " ".join(out)


P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "harm", "bass", "pr", "pl", "p0", "p1", "p2"]}
kit = Kit(BEATS)
RIDE, BELL, CR, CR2, CHINA = "D2", "F2", "C2", "G2", "B2"
g16 = lambda *pos, ch="X", base=None: kit.grid(pos, ch, base)

for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    ch = song.chords[name][i]
    nxt = song.chord_at(idx + 1) if idx + 1 < NB else ch
    last = i == n - 1
    base_ch = ch.split("/")[0]
    root = root_note(ch)
    groot = up(root, 1)
    tones = chord_tones(ch, "C4", "B4", True)[:3]
    while len(tones) < 3: tones.append(tones[-1])

    # ギター
    rf = R4
    if name in ("march", "inter"): rf = RIFF[i % 2] if not (name == "inter" and last) else bar("G2:2! R:2")
    elif name in ("verse", "verse2") and i in (0, 1): rf = RIFF[i % 2]
    P["riff"].append(rf)
    s = si = R4
    if name in ("verse", "verse2") and i >= 2: s = si = bar(f"{groot}:2! {groot}:2") if not last else bar(f"{groot}:1! R:3")
    elif name in ("chorus", "chorus2"): s = si = bar(f"{groot}:1! {groot}:1 {groot}:1 {groot}:0.5 {groot}:0.5") if not last else bar(f"{groot}:4!")
    elif name == "roll" and i >= 4: s = si = bar(f"{groot}:4!")
    elif name == "solo": s = si = bar(f"{groot}:2! {groot}:2") if not last else bar(f"{groot}:4!")
    elif name == "anthem": s = si = bar(f"{groot}:1! {groot}:1 {groot}:1 {groot}:1") if not last else bar(f"{groot}:4!")
    P["rhy"].append(s); P["rhy_in"].append(si)

    lead = harm = R4
    if name == "verse": lead = VERSE_MEL[i]
    elif name == "verse2": lead = VERSE2_MEL[i]
    elif name in ("chorus", "chorus2"):
        lead = THEME[i]; harm = harm_below(lead, ch) if name == "chorus2" or i >= 4 else R4
    elif name == "roll": lead = ROLL_LEAD[i]
    elif name == "solo": lead = SOLO[i]
    elif name == "anthem": lead = THEME_MAJ[i]; harm = harm_below(lead, ch)
    P["lead"].append(lead); P["harm"].append(harm)

    # ピアノ
    pr = pl = R4; pc = [R4] * 3
    if name in ("intro", "outro"):
        pr = THEME[i] if name == "intro" else OUTRO_MEL[i]
        pl = bar(f"{up(root, 2)}:4"); pc = [bar(f"{t}:4") for t in tones]
        if name == "intro" and i < 2: pc = [R4] * 3
    elif name == "march": pl = bar(f"{root}:1! R:3")
    elif name in ("verse", "verse2"): pl = bar(f"{up(root, 2)}:2 R:2"); pc = [bar(f"{t}:2 R:2") for t in tones]
    elif name in ("chorus", "chorus2"): pr = shift_oct(strip_marks(THEME[i]), 1); pl = bar(f"{up(root, 2)}:4")
    elif name == "roll": pl = bar(f"{up(root, 2)}:4"); pc = [bar(f"{t}:4") for t in tones]
    elif name == "anthem": pr = shift_oct(strip_marks(THEME_MAJ[i]), 1); pl = bar(f"{up(root, 2)}:2 {up(root, 2)}:2"); pc = [bar(f"{t}:1 {t}:1 {t}:1 {t}:1") for t in tones]
    P["pr"].append(pr); P["pl"].append(pl)
    for v in range(3): P[f"p{v}"].append(pc[v])

    # ベース（コードに沿う）
    f5 = fifth_of(base_ch)
    b = R4
    if name == "intro" and i >= 4: b = bar(f"{root}:4")
    elif name in ("march", "inter"): b = unison_low(rf, -1, "B0") if rf != R4 else R4
    elif name in ("verse", "verse2"):
        b = unison_low(rf, -1, "B0") if i < 2 else bar(f"{root}:1.5! {root}:0.5 {f5}:1 {up(root, 1)}:1")
        if last: b = bar(f"{root}:1! R:3")
    elif name in ("chorus", "chorus2", "anthem"):
        b = bar(f"{root}:1! {up(root, 1)}:1 {f5}:1 {approach_note(ch, nxt)}:1") if not last else bar(f"{root}:4!")
    elif name == "roll": b = bar(f"{root}:2 {f5}:2")
    elif name == "solo": b = bar(" ".join([f"{root}:0.5"] * 7 + [f"{approach_note(ch, nxt)}:0.5"])) if not last else bar(f"{root}:4!")
    P["bass"].append(b)

    # ドラム
    k = s = h = None; tom = cym = None
    if name == "march" or (name == "roll" and i < 4):
        # 葬送の行進: スネアの行進（強弱）と床タム
        k = g16(0, 8); s = g16(0, 8, ch="X"); s = g16(3, 4, 6, 11, 12, 14, 15, ch="o", base=s)
        tom = "A2:1! R:1 A2:1! R:1"
        if name == "march" and i == 0: cym = f"{CR}:4!"; tom = "R:2 A2:1! R:1"
    elif name == "roll":
        k = g16(0, 8); s = g16(8); h = None; cym = f"{RIDE}:1! {RIDE}:1, {RIDE}:1! {RIDE}:1,"
        if i == 4: cym = f"{CR}:4!"
        if last: s = g16(8, 10, 12, 13, 14, 15); cym = None
    elif name in ("verse", "verse2"):
        k = g16(0, 3, 10) if i % 2 == 0 else g16(0, 6, 10); s = g16(8); s = g16(14, ch="o", base=s)
        h = g16(*range(0, 16, 2), ch="x")
        if i == 0: cym = f"{CR2}:4!"; h = g16(4, 6, 8, 10, 12, 14, ch="x")
        if last: k = g16(0); s = g16(); h = None; tom = "R:2 " + tom_triplets_down(2)
    elif name in ("chorus", "chorus2"):
        k = g16(0, 2, 6, 8, 10, 14); s = g16(4, 12)
        cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if i % 2 == 0: cym = (f"{CR}:1! " if i % 4 == 0 else f"{CR2}:1! ") + f"{RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {BELL}:0.5 {RIDE}:0.5"
        if last: k = g16(0); s = g16(); cym = f"{CR}:4!"
    elif name == "inter":
        k = g16(0, 8); s = g16(4, 12)
        if last: k = g16(0); s = g16(); tom = "R:1 " + tom_16_down(1) + " " + tom_triplets_down(2)
        else: cym = f"{CHINA}:1! R:3"
    elif name == "solo":
        k = g16(*range(0, 16, 2)); s = g16(8); k = "".join("." if s[j] != "." else c for j, c in enumerate(k))
        cym = f"{BELL}:1! {RIDE}:1 {BELL}:1! {RIDE}:1"
        if i == 0 or i == 4: cym = f"{CR}:1! {RIDE}:1 {BELL}:1! {RIDE}:1"
        if last: k = g16(0); s = g16(); cym = None; tom = None
    elif name == "anthem":
        k = g16(*range(0, 16, 2)); s = g16(4, 12); k = "".join("." if s[j] != "." else c for j, c in enumerate(k))
        cym = f"{CR}:1! {RIDE}:1 {RIDE}:1 {RIDE}:1" if i % 2 == 0 else f"{CR2}:1! {RIDE}:1 {CHINA}:1! {RIDE}:1"
        if i == 3: tom = "R:3 " + tom_16_down(1); s = g16(4); cym = f"{CR2}:1! {RIDE}:1 {CHINA}:1! R:1"
        if last: k = g16(0); s = g16(0); cym = f"{CR}:4!"
    kit.add(k, s, h, tom, cym)

FX = []
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    nx = SECS[idx + 1][0] if idx + 1 < NB else ""
    if i == n - 1 and nx in ("chorus", "chorus2"): FX.append(bar("R:2 C4:2"))
    elif name == "solo" and i == n - 1: FX.append(bar("E4:4"))
    elif name == "intro" and i == n - 1: FX.append(bar("R:1 D4:3"))
    else: FX.append(R4)

J = lambda k: " ".join(P[k])
PIANO = dict(volume=0.14, reverb=0.35, fx=[{"type": "eq", "low": -2, "mid": 0, "midHz": 800, "high": 1}, {"type": "plate", "mix": 0.18}])
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("harm"), vol=0.09, pan=0.3, role="リード（和音の音のハモリ）"))
song.add(part("ピアノ（右手・国歌）", "piano", J("pr"), pan=0.05, **PIANO))
song.add(part("ピアノ（左手）", "piano", J("pl"), pan=-0.1, **{**PIANO, "volume": 0.13}))
song.add([part(f"ピアノ（右手の和音{v + 1}）", "piano", J(f"p{v}"), pan=0.1, **{**PIANO, "volume": 0.08}) for v in range(3)])
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-23-kokka.json"
    song.write(out)
    check_clash(song)
