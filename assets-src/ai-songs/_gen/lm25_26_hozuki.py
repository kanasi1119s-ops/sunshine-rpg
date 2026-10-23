# ラウド25曲（第2シリーズ）＋1: 26「鬼灯の撥」（仮）。三味線が主役のラウドロック。E の都節（E F A B C）・128・4/4。インスト
# 2026-10-23 人間「三味線を入れたラウドロックもお願いします」「曲にはストーリーを持たせるように」。
# 別の楽器: 三味線（2本。祖母の撥＝遠い・残響が深い／孫の撥＝近い・粒が立つ）。追加の楽器: 尺八（祖母の息）。
# 物語: 盆の夜。鬼灯の灯りに導かれて、亡くなった三味線弾きの祖母の撥の音が、どこからか聞こえてくる（前奏の三味線ひとり）。
#   孫は祭の櫓に上がり、祖母の曲を弾きはじめる（看板リフと三味線の重ね）。Aメロは歌と三味線の掛け合い、サビは祭の熱。
#   間奏で三味線とギターが同じ速い旋律を走る。ブリッジで祖母の撥（遠い）と孫の撥（近い）が掛け合い、尺八が祖母の息のように流れる。
#   ソロは孫の津軽の叩き。最後のサビで二人の撥が重なり、送り火のように E の一撃が鳴り続けて終わる。
# しかけ（ほかの曲と変える）:
#   - 主役は三味線。津軽の「叩き」（同じ音の16分の連打に強弱）と、開放弦（E・B）の響きを旋律の間に置く
#   - 都節（♭2＝F・♭6＝C）の和の響きを、パワーコードのリフに混ぜる。刻み（16分のミュート）はしない
#   - ブリッジで三味線2本の掛け合い（左に遠い祖母、右に近い孫）。ドラムはタムを太鼓のように
#   - 参考の音は BMTH（wide-dark-wall。人間が「めっちゃいい」と言った音）
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import *

BPM, BEATS = 128, 4
bar = Bars(BEATS)
R4 = bar.rest()

FORM = [("intro", 8), ("riff", 4), ("verse", 8), ("pre", 4), ("chorus", 8), ("inter", 4), ("verse2", 8), ("pre2", 4), ("chorus2", 8),
        ("bridge", 8), ("solo", 8), ("chorus3", 8), ("outro", 4)]
VERSE = ["E5", "E5", "F5", "E5", "Am", "Am", "F", "E5"]
PRE = ["Am", "C", "F", "B5"]
CHORUS = ["Am", "F", "C", "G", "Am", "F", "E5", "E5"]
CH = {"intro": ["E5"] * 8, "riff": ["E5", "E5", "E5", "F5"], "verse": VERSE, "pre": PRE, "chorus": CHORUS, "inter": ["E5", "F5", "E5", "C5"],
      "verse2": VERSE, "pre2": PRE, "chorus2": CHORUS, "bridge": ["Am", "Am", "F", "F", "Am", "Am", "E5", "E5"],
      "solo": ["E5", "F5", "E5", "C5", "E5", "F5", "A5", "B5"], "chorus3": CHORUS, "outro": ["E5", "F5", "E5", "E5"]}
song = Song("鬼灯の撥（仮）",
            "仮: ラウド25曲（第2シリーズ）の26曲目。三味線が主役のラウドロック。E の都節（E F A B C）・128。前奏は三味線ひとりの津軽の叩き、"
            "都節のパワーコードのリフに三味線を重ね、Aメロは旋律と三味線の掛け合い、間奏は三味線とギターの同じ速い旋律、"
            "ブリッジは遠い三味線（祖母）と近い三味線（孫）の掛け合いと尺八、ソロは三味線の叩き、最後のサビで二人の撥が重なる。"
            "別の楽器は三味線（2本）、追加の楽器は尺八。インスト（歌は後日）。自作",
            BPM, BEATS, FORM, CH)
song.desc += " 物語: 盆の夜、鬼灯の灯りの向こうから亡き祖母の撥の音。孫は櫓で祖母の曲を受け継ぎ、最後に二人の撥が重なって送り火になる。"
song.kinds = {"riff": "interlude", "inter": "interlude", "bridge": "bridge", "solo": "solo"}
song.ref_tone = "wide-dark-wall"
SECS, NB = song.secs, song.nb

# ── 三味線（孫＝近い） ──
SHA_INTRO = [bar("E4:0.25! E4:0.25, E4:0.25 B3:0.25 E4:0.5! F4:0.25 E4:0.25 C5:1 B4:0.5 A4:0.5"),
             bar("E5:0.5! C5:0.25 B4:0.25 A4:0.5 F4:0.5 E4:1! R:1"),
             bar("A4:0.25! A4:0.25, A4:0.25, E4:0.25 A4:0.25 B4:0.25 C5:0.5 B4:0.25 A4:0.25 F4:0.5 E4:1"),
             bar("B4:0.25! C5:0.25 B4:0.25 A4:0.25 F4:0.25 E4:0.25 F4:0.25 A4:0.25 B4:2!"),
             bar("E5:0.25! E5:0.25, E5:0.25, C5:0.25 B4:0.5 A4:0.5 F4:0.25! F4:0.25, E4:0.5 B3:1"),
             bar("E4:0.5! F4:0.5 A4:0.5 B4:0.5 C5:0.5! B4:0.5 A4:1"),
             bar("C5:0.25! C5:0.25, B4:0.25 A4:0.25 B4:0.25! B4:0.25, A4:0.25 F4:0.25 A4:0.25! A4:0.25, F4:0.25 E4:0.25 F4:0.5 E4:0.5"),
             bar("E5:0.5! B4:0.5 E4:0.5 B3:0.5 E4:2!")]
RIFF = {"E5": [bar("E2:0.5! E2:0.5 F2:0.5 E2:0.5 A2:1! B2:0.5 C3:0.5"), bar("E2:0.5! E2:0.5 F2:0.5 E2:0.5 B2:1! A2:0.5 F2:0.5")],
        "F5": [bar("F2:0.5! F2:0.5 E2:0.5 F2:0.5 A2:1! C3:1")] * 2,
        "C5": [bar("C2:0.5! C2:0.5 E2:0.5 F2:0.5 B2:1! A2:0.5 F2:0.5")] * 2}
# Aメロの三味線の答え（2小節目ごと。旋律が休む所に）
SHA_ANS = [R4, bar("R:2 E5:0.25! C5:0.25 B4:0.25 A4:0.25 F4:0.5 E4:0.5"), R4, bar("R:2 B4:0.25! B4:0.25, A4:0.25 F4:0.25 E4:1"),
           R4, bar("R:2 C5:0.25! A4:0.25 E4:0.25 A4:0.25 C5:0.5 E5:0.5"), R4, bar("R:2 F4:0.25! E4:0.25 B3:0.25 E4:0.25 B4:1!")]
# 間奏: 三味線とギター（速弾き）が同じ速い旋律を走る
INTER_RUN = [bar("E5:0.25! C5:0.25 B4:0.25 A4:0.25 F4:0.25! E4:0.25 C4:0.25 B3:0.25 B3:0.25! E4:0.25 F4:0.25 A4:0.25 B4:0.25! C5:0.25 B4:0.25 A4:0.25"),
             bar("F4:0.25! A4:0.25 C5:0.25 F5:0.25 E5:0.25! C5:0.25 A4:0.25 F4:0.25 E4:0.5! F4:0.5 A4:0.5 C5:0.5"),
             bar("B4:0.25! C5:0.25 B4:0.25 A4:0.25 B4:0.25! E5:0.25 B4:0.25 A4:0.25 E4:0.25! F4:0.25 A4:0.25 F4:0.25 B4:0.5! E5:0.5"),
             bar("C5:0.5! B4:0.5 A4:0.5 E4:0.5 C5:1! R:1")]
# ブリッジ: 祖母（遠い）と孫（近い）の掛け合い
GRAN = [bar("A4:1! C5:1 E5:2"), R4, bar("F4:1! A4:1 C5:2"), R4, bar("E5:1! C5:0.5 A4:0.5 E4:2"), R4, bar("B4:2! E4:2"), bar("B3:4")]
CHILD = [R4, bar("A4:0.5! C5:0.5 E5:0.5 C5:0.5 A4:1 E4:1"), R4, bar("C5:0.5! A4:0.5 F4:0.5 A4:0.5 C5:2"), R4,
         bar("E5:0.25! E5:0.25, C5:0.5 A4:0.5 E4:0.5 A4:2"), R4, bar("E4:0.5! F4:0.5 A4:0.5 B4:0.5 E5:2!")]
# ソロ: 孫の津軽の叩き（同じ音の連打に強弱、開放弦の響き、速い下り）
SOLO = [bar("E5:0.25! E5:0.25, E5:0.25, E5:0.25 C5:0.25! C5:0.25, B4:0.25 A4:0.25 B4:1! E4:1"),
        bar("F4:0.25! F4:0.25, F4:0.25, A4:0.25 C5:0.5! A4:0.5 F4:0.25! F4:0.25, E4:0.5 F4:1"),
        bar("E5:0.25! C5:0.25 B4:0.25 A4:0.25 F4:0.25! E4:0.25 C4:0.25 B3:0.25 E4:0.5! B3:0.5 E4:1"),
        bar("C5:0.25! C5:0.25, C5:0.25, E5:0.25 C5:0.25! B4:0.25 A4:0.25 F4:0.25 E4:1! C4:1"),
        bar("B4:0.25! B4:0.25, B4:0.25, B4:0.25, C5:0.25! B4:0.25 A4:0.25 F4:0.25 E4:0.25! F4:0.25 A4:0.25 B4:0.25 E5:1!"),
        bar("F5:0.5! E5:0.5 C5:0.5 A4:0.5 F4:0.25! F4:0.25, A4:0.25 C5:0.25 F5:1!"),
        bar("E5:0.25! C5:0.25 A4:0.25 E4:0.25 A4:0.25! C5:0.25 E5:0.25 A4:0.25 C5:0.5! A4:0.5 E4:1"),
        bar("B4:0.25! B4:0.25, B4:0.25, B4:0.25, B4:0.25! B4:0.25, B4:0.25, B4:0.25, E5:2!")]

# ── 歌の代わりのリード（歌の高さ。modernize で区間ごとに高さを整える） ──
VERSE_MEL = [bar("R:1 B3:1 E4:1.5 F4:0.5"), bar("E4:2 B3:1 R:1"), bar("R:1 C4:1 E4:1 F4:1"), bar("E4:3 R:1"),
             bar("R:1 A3:1 C4:1 E4:1"), bar("E4:1.5 C4:0.5 A3:2"), bar("R:1 C4:1 F4:1 A4:1"), bar("B4:2 E4:2")]
VERSE2_MEL = [bar("R:1 E4:1 B4:1.5 C5:0.5"), bar("B4:2 E4:1 R:1"), bar("R:1 F4:1 A4:1 C5:1"), bar("B4:3 R:1"),
              bar("R:1 C4:1 E4:1 A4:1"), bar("C5:1.5 A4:0.5 E4:2"), bar("R:1 F4:1 A4:1 C5:1"), bar("B4:2 E5:2")]
PRE_MEL = [bar("A4:2 C5:2"), bar("E5:2 C5:2"), bar("F5:2 C5:2"), bar("B4:3^^ R:1")]
CHORUS_MEL = [bar("E4:1 A4:1 C5:2"), bar("C5:1.5 A4:0.5 F4:2"), bar("G4:1 C5:1 E5:2"), bar("D5:2 B4:2"),
              bar("C5:1 B4:1 A4:2"), bar("A4:1 C5:1 F5:2"), bar("E5:3 B4:1"), bar("B4:2 E5:2")]
CHORUS2_MEL = CHORUS_MEL[:6] + [bar("E5:2.5 F5:0.5 E5:1"), bar("B4:2 E5:2")]
# 最後のサビ: 前半を一段高く（二人の撥が重なる所）
CHORUS3_MEL = [bar("A4:1 C5:1 E5:2"), bar("F5:1.5 C5:0.5 A4:2"), bar("C5:1 E5:1 G5:2"), bar("G5:2 D5:2")] + CHORUS2_MEL[4:]

# ── 尺八（祖母の息）: Bメロとブリッジとアウトロ ──
# 息継ぎ（小節の終わりに半拍の休み）を入れる
SHAKU = {"pre": [bar("E5:3.5 R:0.5"), bar("G5:3.5 R:0.5"), bar("A5:2 F5:1.5 R:0.5"), bar("B4:3.5 R:0.5")],
         "bridge": [bar("A4:2 C5:1.5 R:0.5"), bar("E5:3.5 R:0.5"), bar("C5:2 A4:1.5 R:0.5"), bar("F5:3.5 R:0.5"), bar("E5:2 C5:1.5 R:0.5"), bar("A4:3.5 R:0.5"),
                    bar("B4:2 E5:1.5 R:0.5"), bar("E5:3.5 R:0.5")],
         "outro": [bar("E5:3.5 R:0.5"), bar("F5:3.5 R:0.5"), bar("E5:3.5 R:0.5"), bar("E5:4")]}

P = {k: [] for k in ["riff", "rhy", "rhy_in", "lead", "tech", "sha", "gran", "shaku", "bass"]}
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
    kind = name.rstrip("23")

    rf = s = si = lead = tech = sha = gran = shaku = R4
    if name == "intro":
        sha = SHA_INTRO[i]
    elif name == "riff" or name == "solo":
        rf = RIFF.get(base_ch, RIFF["E5"])[i % 2] if name == "riff" or base_ch in RIFF else bar(f"{groot}:2! {groot}:2")
        if name == "riff": sha = shift_oct(strip_marks(rf), 2)
        else:
            sha = SOLO[i]; rf = bar(f"{groot}:4!"); s = si = rf
    elif kind == "verse":
        rf = RIFF.get(base_ch, [bar(f"{groot}:2! {groot}:2")] * 2)[i % 2] if i < 4 else R4
        if i >= 4: s = si = bar(f"{groot}:2! {groot}:2") if not last else bar(f"{groot}:1! R:3")
        lead = (VERSE_MEL if name == "verse" else VERSE2_MEL)[i]
        sha = SHA_ANS[i]
    elif kind == "pre":
        s = si = bar(f"{groot}:1! {groot}:1 {groot}:1 {groot}:1") if not last else bar(f"{groot}:3! R:1")
        lead = PRE_MEL[i]; shaku = SHAKU["pre"][i]
    elif kind == "chorus":
        s = si = bar(f"{groot}:1.5! {groot}:0.5 {groot}:1 {groot}:1") if not last else bar(f"{groot}:2! {groot}:2")
        lead = {"chorus": CHORUS_MEL, "chorus2": CHORUS2_MEL, "chorus3": CHORUS3_MEL}[name][i]
        t = chord_tones(ch, "E4", "E5")
        sha = bar(" ".join(f"{t[j % len(t)]}:0.5{'!' if j % 2 == 0 else ''}" for j in (0, 2, 1, 2, 0, 2, 1, 2)))
        if name == "chorus3": gran = shift_oct(strip_marks(sha), -1)   # 二人の撥が重なる
    elif name == "inter":
        tech = INTER_RUN[i]; sha = INTER_RUN[i]
        s = si = bar(f"{groot}:1! R:1 {groot}:1! R:1") if i < 3 else bar(f"{groot}:2! R:2")
    elif name == "bridge":
        gran = GRAN[i]; sha = CHILD[i]; shaku = SHAKU["bridge"][i]
    elif name == "outro":
        s = si = bar(f"{groot}:1! R:1 {groot}:1! R:1") if i < 3 else bar(f"{groot}:4!")
        rf = s
        rn = "F" if base_ch.startswith("F") else "E"
        sha = bar(f"{rn}4:1! R:1 {rn}4:1! R:1") if i < 3 else bar("E4:4!")
        gran = bar(f"{rn}5:1! R:1 {rn}5:1! R:1") if i < 3 else bar("B4:4!")
        shaku = SHAKU["outro"][i] if i >= 2 else R4
    P["riff"].append(rf); P["rhy"].append(s); P["rhy_in"].append(si); P["lead"].append(lead); P["tech"].append(tech)
    P["sha"].append(sha); P["gran"].append(gran); P["shaku"].append(shaku)

    # ベース
    b = R4
    if name == "riff" or (kind == "verse" and i < 4): b = unison_low(rf, -1, "B0")
    elif kind in ("verse", "pre", "chorus"): b = bass_root8(ch, 4, nxt) if not last else bar(f"{root}:2! {root}:2")
    elif name == "inter": b = unison_low(s, -1, "B0")
    elif name == "solo": b = bar(f"{root}:1! {root}:1 {fifth_of(base_ch)}:1 {approach_note(ch, nxt)}:1")
    elif name == "bridge" and i >= 4: b = bar(f"{root}:4")
    elif name == "outro": b = unison_low(s, -1, "B0")
    P["bass"].append(b)

    # ドラム
    k = sn = h = None; tom = cym = None
    if name == "intro":
        if i >= 4:   # 太鼓のようなタム
            tom = "A2:1! D3:0.5 D3:0.5, A2:1! A2:0.5, D3:0.5" if i < 7 else tom_triplets_down(2) + " A2:1! R:1"
            if i == 7: k = g16(8); cym = f"R:2 {CR}:2!"
    elif name == "riff":
        k = g16(0, 2, 6, 8, 10, 14); sn = g16(4, 12); h = g16(*range(0, 16, 2), ch="x")
        if i == 0: cym = f"{CR}:1! R:3"; h = g16(4, 6, 8, 10, 12, 14, ch="x")
        if last: k, sn, tom = linear_fill(kit, 2, fseed); fseed += 1; h = g16(0, 2, 4, 6, ch="x")
    elif kind == "verse":
        k = g16(0, 3, 10) if i % 2 == 0 else g16(0, 6, 10); sn = g16(8); sn = g16(14, ch="o", base=sn)
        h = g16(0, 4, 8, 12, ch="x")
        if i == 0: cym = f"{CR2}:2! R:2"; h = g16(8, 12, ch="x")
        if last: k = g16(0); sn = g16(4, 8, 10, 12, 13, 14, 15); h = None
    elif kind == "pre":
        k = g16(0, 8); sn = g16(*([4, 12] if i < 2 else [2, 4, 6, 10, 12, 14] if i == 2 else range(0, 16)))
        h = g16(*range(0, 16, 2), ch="x") if i < 2 else None
        if i == 3: cym = None; sn = g16(*range(0, 12)); k = g16(0, 4, 8)
    elif kind == "chorus":
        k = g16(0, 2, 6, 8, 10, 14); sn = g16(4, 12)
        cym = f"{RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5"
        if i % 2 == 0: cym = (f"{CR}:1! " if i % 4 == 0 else f"{CR2}:1! ") + f"{RIDE}:0.5 {BELL}:0.5! {RIDE}:0.5 {RIDE}:0.5! {BELL}:0.5 {RIDE}:0.5"
        if name == "chorus3" and i >= 4: k = "".join("X" if x % 2 == 0 else "x" for x in range(16)); k = "".join("." if sn[x] != "." else c for x, c in enumerate(k))
        if last and name != "chorus3": k, sn, tom = linear_fill(kit, 2, fseed); fseed += 1; cym = f"{RIDE}:1! {RIDE}:1 R:2"
        if last and name == "chorus3": k = g16(0); sn = g16(0); cym = f"{CR}:4!"
    elif name == "inter":
        # 速い旋律の頭にキックとスネアを合わせる
        k = g16(0, 4, 8, 12); sn = g16(0, 8) if i < 3 else g16(0); cym = f"{CHINA}:1! R:3" if i == 0 else None
        if i == 3: tom = "R:2 " + tom_16_down(2)
    elif name == "bridge":
        if i >= 4: cym = f"{RIDE}:1! {RIDE}:1, {RIDE}:1! {RIDE}:1,"; tom = "A2:1! R:1 A2:1! R:1"
        if last: tom = "R:2 " + tom_triplets_down(2); cym = None
    elif name == "solo":
        # ハーフタイム（スネアは3拍目）と、タムの太鼓
        k = g16(0, 3, 6, 10); sn = g16(8); tom = "R:1 D3:0.5 D3:0.5, R:1 A2:1!" if i % 2 else None
        cym = f"{CHINA}:2! {RIDE}:1 {RIDE}:1" if i % 4 == 0 else f"{RIDE}:1! {RIDE}:1 {BELL}:1! {RIDE}:1"
        if tom: cym = f"{RIDE}:1! R:1 {RIDE}:1 R:1"
        if last: k, sn, tom = linear_fill(kit, 2, fseed); fseed += 1; cym = f"{RIDE}:1! {RIDE}:1 R:2"
    elif name == "outro":
        k = g16(0, 8) if i < 3 else g16(0); sn = g16(0, 8) if i < 3 else g16(0); cym = f"{CR}:2! {CR2}:2!" if i < 3 else f"{CR}:4!"
    kit.add(k, sn, h, tom, cym)

FX = []
for idx, (name, i) in enumerate(SECS):
    n = dict(FORM)[name]
    nx = SECS[idx + 1][0] if idx + 1 < NB else ""
    if i == n - 1 and nx.startswith("chorus"): FX.append(bar("R:2 C4:2"))
    elif name == "intro" and i == 7: FX.append(bar("E4:4"))
    else: FX.append(R4)

J = lambda k: " ".join(P[k])
SHA_FX = [{"type": "eq", "low": -3, "mid": 2, "midHz": 2500, "high": 1}, {"type": "room", "mix": 0.18}]
song.add(riff_parts(J("riff")))
song.add(rhythm_parts(J("rhy"), J("rhy_in")))
song.add(lead_part(J("lead")))
song.add(lead_part(J("lead"), vol=0.07, pan=0.3, role="リード（オクターブ下）"))   # modernize で3度上のハモリに置きかわる
song.add(tech_part(J("tech"), role="技のギター（三味線と同じ速い旋律）"))
song.add(part("三味線（孫・近い）", "shamisen", J("sha"), volume=0.16, pan=0.2, reverb=0.25, attack=0.002, release=0.5, fx=SHA_FX))
song.add(part("三味線（祖母・遠い）", "shamisen", J("gran"), volume=0.11, pan=-0.45, reverb=0.6, attack=0.002, release=0.7,
              fx=[{"type": "eq", "low": -4, "mid": 1, "midHz": 2000, "high": -2}, {"type": "reverb", "mix": 0.35}]))
song.add(part("追加の楽器: 尺八（祖母の息）", "shakuhachi", J("shaku"), volume=0.1, pan=-0.2, reverb=0.5, attack=0.3, release=0.6))
song.add(bass_part(J("bass")))
song.add(drum_parts(kit))
song.add(cymfx_part(" ".join(FX)))

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/lm25/lm25-26-hozuki.json"
    song.write(out)
    check_clash(song)
