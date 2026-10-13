#!/usr/bin/env python3
"""プログレッシブメタル・変拍子・テクニカルな曲（約4分）を書く。使い方: python3 assets-src/ai-songs/_gen/prog-tech.py assets-src/ai-songs/prog-tech-odd.json
1小節＝12拍（24個の8分）を、7+7+5+5・5+5+5+5+4・3×8・11+13 などに組み替えて、変拍子にする。
単位: 1拍＝8コマ（32分音符）。1小節＝96コマ。曲全体は50小節（600拍）。bpm 150 で約4分。"""
import json, sys

R = 8            # 1拍のコマ数
BAR = 96
NBARS = 50
N = NBARS * BAR
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def nm(m): return f"{NAMES[m % 12]}{m // 12 - 1}"
E2, E3, E4, E5 = 40, 52, 64, 76

# ── 構成（小節番号は0始まり） ──
SECT = [("intro", 0, 4), ("A1", 4, 12), ("B1", 12, 16), ("C1", 16, 24), ("inter", 24, 28), ("A2", 28, 36), ("solo", 36, 44), ("C2", 44, 48), ("outro", 48, 50)]
def sect_of(b):
    for n, a, z in SECT:
        if a <= b < z: return n
GROUPS = {  # 小節ごとの「8分」のまとまり（合計24）
    "intro": [[7, 7, 5, 5]] * 4,
    "A1": [[7, 7, 5, 5]] * 3 + [[7, 7, 3, 3, 4]] + [[5, 7, 7, 5]] * 3 + [[7, 7, 5, 3, 2]],
    "B1": [[5, 5, 5, 5, 4]] * 4,
    "C1": [[3] * 8] * 8,
    "inter": [[11, 13]] * 4,
    "A2": [[7, 7, 5, 5]] * 3 + [[7, 7, 3, 3, 4]] + [[5, 7, 7, 5]] * 3 + [[7, 7, 5, 3, 2]],
    "solo": [[3] * 8] * 4 + [[7, 7, 5, 5]] * 3 + [[7, 7, 5, 3, 2]],
    "C2": [[3] * 8] * 4,
    "outro": [[7, 7, 5, 5], [12, 12]],
}
CHORDS = ("Em Cmaj7 Em Bm7  Em Em Cmaj7 D Em Em Cmaj7 B  Am Cmaj7 G D  Em C G D Em C D B  Em Em Am B  Em Em Cmaj7 D Em Em Cmaj7 B  Em C G D Em C D B  F#m D A E  Em Em").split()
assert len(CHORDS) == NBARS, len(CHORDS)
ROOT = {"Em": 0, "Cmaj7": -4, "C": -4, "Bm7": -5, "D": -2, "G": -5, "B": -1, "Am": 5, "F#m": 2, "A": 5, "E": 0}  # Eからの半音（低い方のオクターブで）

def bar_groups(b):
    n = sect_of(b); a = [x for x in SECT if x[0] == n][0][1]
    return GROUPS[n][b - a]
def group_starts(b):  # 各まとまりの先頭コマ
    out = []; p = b * BAR
    for g in bar_groups(b):
        out.append((p, g * 4)); p += g * 4   # 8分1つ＝4コマ
    return out

def rests(n):  # 1つの休みは64拍まで。長いときは分ける
    out = []
    while n > 0:
        c = min(n, 32 * R); out.append(f"R:{c / R:g}"); n -= c
    return out

class Part:
    def __init__(self): self.ev = {}
    def add(self, slot, midi, dur, marks=""):
        self.ev[slot] = (midi, dur, marks)
    def tokens(self):
        out = []; pos = 0
        for s in sorted(self.ev):
            if s < pos: continue
            if s > pos: out += rests(s - pos)
            m, d, mk = self.ev[s]
            d = min(d, N - s)
            out.append(f"{nm(m)}:{d / R:g}{mk}")
            pos = s + d
        if pos < N: out += rests(N - pos)
        return " ".join(out)

# ── リフの型（16分＝2コマ×… 単位は「16分」。まとまりの長さ L（16分の数）ごと） ──
CELLS = {
    6: [[0, 2, 3, 5]],
    10: [[0, 1, 3, 4, 6, 7, 9], [0, 2, 3, 5, 6, 8, 9]],
    14: [[0, 1, 3, 4, 6, 7, 8, 10, 11, 12], [0, 2, 3, 5, 6, 8, 9, 10, 12, 13]],
    22: [[0, 1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20]],
    26: [[0, 1, 3, 4, 6, 7, 9, 10, 12, 13, 15, 16, 18, 19, 21, 22, 24]],
    12: [[0, 3, 6, 9], [0, 2, 3, 6, 8, 9]],
    8: [[0, 2, 4, 6]],
    2: [[0]], 4: [[0, 2]],
}
def cell_for(L, variant):
    cands = CELLS.get(L) or [[0, 2]]
    return cands[variant % len(cands)]
MOTIF = [0, 0, 1, 0, 3, 0, 6, 0, 5, 0, 1, 0, 7, 0, 3, 1]  # 根音からの半音（フリジアン風。頭は根音）

def riff_hits(b, variant):
    """小節bのリフの打つ位置（コマ番号）と、その音の高さ（根音からの半音）。"""
    hits = []; k = 0
    for gi, (st, ln) in enumerate(group_starts(b)):
        L = ln // 2  # 16分の数
        for h in cell_for(L, variant + gi):
            off = 0 if h == cell_for(L, variant + gi)[0] else MOTIF[(k + gi) % len(MOTIF)]
            hits.append((st + h * 2, off, h == 0)); k += 1
    return hits

parts = {}
def P(name): parts.setdefault(name, Part()); return parts[name]

def bars_of(name):
    return [b for b in range(NBARS) if sect_of(b) == name]

# ── 調（最後のサビは全音上げ） ──
def shift(b): return 2 if sect_of(b) == "C2" else 0
def root_of(b): return ROOT[CHORDS[b]]

# ── リズムギター2本とベース（リフ） ──
for b in range(NBARS):
    s = sect_of(b); sh = shift(b)
    r = root_of(b)
    if s in ("A1", "A2", "outro") and not (s == "outro" and b == 49):
        var = 0 if s == "A1" else 1
        hits = riff_hits(b, var)
        for i, (sl, off, head) in enumerate(hits):
            nxt = hits[i + 1][0] if i + 1 < len(hits) else (b + 1) * BAR
            for gname, base in (("rgL", E2), ("rgR", E2)):
                P(gname).add(sl, base + off + r + sh, 4, "!'" if head else "'")
            P("bass").add(sl, 28 + off + r + sh, min(nxt - sl, 8), "!" if head else "")
    elif s == "inter":
        # ユニゾンの音階ランニング（11+13）：フリジアン・ドミナント（E F G# A B C D）を3音ずつずらして上り下り
        sc = [0, 1, 4, 5, 7, 8, 10]
        def scale_note(i): return E3 + sc[i % 7] + 12 * (i // 7)
        k = 0
        for gi, (st, ln) in enumerate(group_starts(b)):
            L = ln // 2
            seq = []
            for j in range(L):
                tri = j // 3; pos = j % 3
                idx = (tri + pos) if gi == 0 else (14 - (tri + pos))
                seq.append(idx + (b - 24) % 2)
            for j, idx in enumerate(seq):
                sl = st + j * 2
                n = scale_note(max(idx, 0))
                P("rgL").add(sl, n, 2, "_" if j % 3 else "!")
                P("rgR").add(sl, n, 2, "_" if j % 3 else "!")
                P("lead").add(sl, n + 12, 2, "_" if j % 3 else "!")
                if j % 3 == 0: P("bass").add(sl, 28, 6, "!")
    elif s in ("C1", "C2", "solo") and (s != "solo" or b < 40):
        # 3拍まとめ（8分3つ）×8：根音と5度の二重の和音を、頭で強く
        for gi, (st, ln) in enumerate(group_starts(b)):
            P("rgL").add(st, E3 + r + sh, ln, "!")
            P("rgR").add(st, E3 + r + 7 + sh, ln, "!")
            P("bass").add(st, 28 + r + sh, ln, "!")
            if gi % 2 == 1 and s != "solo":
                P("rgL").add(st + ln - 4, E3 + r + sh + 3, 2, "'")
    elif s == "solo" and b >= 40:
        hits = riff_hits(b, 0)
        for i, (sl, off, head) in enumerate(hits):
            nxt = hits[i + 1][0] if i + 1 < len(hits) else (b + 1) * BAR
            for gname in ("rgL", "rgR"):
                P(gname).add(sl, E2 + off + r, 4, "!'" if head else "'")
            P("bass").add(sl, 28 + off + r, min(nxt - sl, 8), "!" if head else "")
    elif s == "B1":
        for gi, (st, ln) in enumerate(group_starts(b)):
            P("rgL").add(st, E3 + r, ln - 2, "!")
            P("rgR").add(st, E3 + r + 7, ln - 2, "!")
            P("bass").add(st, 28 + r, ln - 2, "")
    elif s == "outro" and b == 49:
        P("rgL").add(b * BAR, E2 + r, 64, "!")
        P("rgR").add(b * BAR, E2 + r + 7, 64, "!")
        P("bass").add(b * BAR, 28 + r, 64, "!")
    elif s == "intro" and b >= 2:
        P("bass").add(b * BAR, 28 + r, BAR - 8, "")

# ── クリーンギターのアルペジオ（イントロ・B・間奏のあとの落ち着き） ──
def arpeggio(b, part, base, pan_shift=0):
    r = root_of(b)
    chord = [0, 7, 12, 15, 19, 12, 7, 3] if CHORDS[b].startswith(("Em", "Am", "F#m", "Bm")) else [0, 7, 12, 16, 19, 12, 7, 4]
    k = 0
    for gi, (st, ln) in enumerate(group_starts(b)):
        for j in range(ln // 4):  # 8分ごと
            n = base + r + chord[(k + gi) % len(chord)] + pan_shift
            part.add(st + j * 4, n, 6 if j == 0 else 5, "!" if j == 0 else "")
            k += 1
for b in bars_of("intro") + bars_of("B1"):
    arpeggio(b, P("clean"), E3)
for b in bars_of("B1"):
    arpeggio(b, P("clean2"), E4, 0)
# ── 弦のパッド ──
for b in bars_of("intro") + bars_of("B1") + bars_of("C1") + bars_of("C2") + [48, 49]:
    sh = shift(b)
    P("strings").add(b * BAR, E3 + root_of(b) + 7 + sh, BAR if b != 49 else 64, "")
# ── リード（サビ：長い音の旋律） ──
def melody(bars, mel):
    for b, line in zip(bars, mel):
        pos = b * BAR
        for midi, beats, mk in line:
            d = int(beats * R)
            P("lead").add(pos, midi, d, mk); pos += d
B5, D6, E6 = 83, 86, 88
C1_MEL = [
    [(71, 3, "!"), (67, 1.5, ""), (71, 1.5, ""), (76, 6, "!~")],
    [(72, 3, "!"), (76, 1.5, ""), (79, 1.5, ""), (76, 3, ""), (74, 3, "")],
    [(74, 3, "!"), (79, 1.5, ""), (B5, 1.5, ""), (D6, 6, "!~~")],
    [(81, 3, "!"), (78, 1.5, ""), (74, 1.5, ""), (78, 6, "!~")],
    [(71, 3, "!"), (76, 1.5, ""), (79, 1.5, ""), (B5, 3, ""), (79, 3, "")],
    [(76, 3, "!"), (72, 1.5, ""), (76, 1.5, ""), (79, 6, "!^^~")],
    [(78, 3, "!"), (81, 1.5, ""), (D6, 1.5, ""), (85, 3, ""), (81, 3, "")],
    [(87, 3, "!"), (B5, 3, ""), (78 + 12, 3, ""), (75 + 12, 3, "!\\")],
]
melody(bars_of("C1"), C1_MEL)
# 最後のサビ：同じ旋律を全音上げ、最初の2小節は1オクターブ上
def up(m, k): return [[(n + k, d, mk) for n, d, mk in line] for line in m]
melody(bars_of("C2"), up(C1_MEL, 2)[:4])
# ── 太鼓 ──
def grid_for_bar(b):
    s = sect_of(b); gs = group_starts(b)
    kick = ["."] * 48; snare = ["."] * 48; hat = ["."] * 48; crash = ["."] * 48; tom = ["."] * 48
    var = 0 if s in ("A1", "intro") else 1
    last_bar = (b + 1 == [x for x in SECT if x[0] == s][0][2])
    first_bar = (b == [x for x in SECT if x[0] == s][0][1])
    for gi, (st, ln) in enumerate(gs):
        o = (st - b * BAR) // 2  # 16分の位置（0〜47）
        L = ln // 2
        if s in ("A1", "A2", "outro") or (s == "solo" and b >= 40):
            for h in cell_for(L, var + gi):
                kick[o + h] = "X" if h == 0 else "x"
            snare[o + (L // 2 if L >= 10 else 0)] = "X" if gi % 2 == 1 or L < 10 else "o"
            for j in range(0, L, 2): hat[o + j] = "X" if j == 0 else "x"
        elif s in ("C1", "C2", "solo"):
            kick[o] = "X"; kick[o + 3] = "x"
            if gi % 2 == 1: snare[o] = "X"
            for j in range(0, L, 1): hat[o + j] = "x" if j % 2 == 0 else "o"
            if s != "solo": hat[o] = "X"
        elif s == "B1":
            kick[o] = "X"; kick[o + 5] = "x"
            snare[o + L // 2] = "X"
            for j in range(0, L, 2): hat[o + j] = "x"
        elif s == "inter":
            for j in range(0, L, 3): kick[o + j] = "X" if j == 0 else "x"
            snare[o + L // 2] = "X"
            for j in range(0, L, 2): hat[o + j] = "x"
        elif s == "intro" and b >= 2:
            for j in range(0, L, 2): hat[o + j] = "x" if j else "X"
            if gi == 0: kick[o] = "X"
    if first_bar and s not in ("intro",): crash[0] = "X"
    if b == 2: crash[0] = "X"
    # 区切りのフィル（最後の小節の終わりの8分3つぶん）
    if last_bar and s not in ("outro",):
        for j in range(36, 48):
            snare[j] = "x" if j % 2 == 0 else "o"; tom[j] = "x" if j % 3 == 0 else "."
            kick[j] = "." 
        kick[36] = "X"; snare[36] = "X"
    if b == 49:
        kick = ["X"] + ["."] * 47; crash = ["X"] + ["."] * 47; snare = ["X"] + ["."] * 47; hat = ["."] * 48; tom = ["."] * 48
    return "".join(kick), "".join(snare), "".join(hat), "".join(crash), "".join(tom)

drum = {k: [] for k in ("kick", "snare", "hihat", "crash", "tom")}
for b in range(NBARS):
    k, s_, h, c, t = grid_for_bar(b)
    if b < 2:
        for key in drum: drum[key].append("R:12")
        continue
    drum["kick"].append("g:" + k); drum["snare"].append("g:" + s_); drum["hihat"].append("g:" + h); drum["crash"].append("g:" + c); drum["tom"].append("g:" + t)

# ── リード：間奏のあとのテクニカルなソロ（タッピング風のアルペジオとスケールの連続） ──
def solo_lines():
    # 前半4小節（3×8）：和音のアルペジオを3オクターブ上り下り（16分）。音数が多いので _ でつなぐ
    for b in bars_of("solo")[:4]:
        r = root_of(b)
        tones = [0, 3, 7, 12, 15, 19, 24, 27, 31] if CHORDS[b].startswith("Em") else [0, 4, 7, 12, 16, 19, 24, 28, 31]
        seq = tones + tones[-2::-1]            # 上って下りる（17音）
        p = b * BAR
        for gi, (st, ln) in enumerate(group_starts(b)):
            for j in range(ln // 2):
                n = E3 + 12 + r + seq[(j + gi * 3) % len(seq)] - (12 if r > 3 else 0)
                while n > 86: n -= 12
                P("lead").add(st + j * 2, n, 2, "_" if j % 3 else "!")
    # 後半4小節（7+7+5+5）：スケールの4音ずつの上昇列（32分に速くする山）
    sc = [0, 2, 3, 5, 7, 8, 10]  # Eナチュラルマイナー
    def sn(i): return E4 + sc[i % 7] + 12 * (i // 7)
    for bi, b in enumerate(bars_of("solo")[4:]):
        k = 0
        for gi, (st, ln) in enumerate(group_starts(b)):
            L = ln // 2
            fast = (bi == 2 and gi >= 1) or bi == 3
            step = 1 if fast else 2
            n_notes = (ln // step)
            for j in range(n_notes):
                idx = (j // 4) + (j % 4) + bi * 2 + gi
                if bi % 2: idx = 12 - idx
                n = sn(max(idx, 0))
                while n > 88: n -= 12
                P("lead").add(st + j * step, n, step, "_" if j % 4 else "!")
            k += 1
        if bi == 3:
            P("lead").add((b + 1) * BAR - 12, E5 + 7, 12, "!^^~~")
solo_lines()
# A2の後半4小節：リードがリフの合間にタッピング風の反復を重ねる（高い和音の分散）
for b in bars_of("A2")[4:]:
    r = root_of(b)
    for gi, (st, ln) in enumerate(group_starts(b)):
        pat = [0, 7, 12, 15, 12, 7]
        for j in range(ln // 2):
            n = E4 + 12 + r + pat[j % len(pat)] + (3 if gi % 2 else 0)
            while n > 86: n -= 12
            P("lead").add(st + j * 2, n, 2, "_" if j % 2 else "!")
# A1の後半にはハーモニクスのように高い単音で飾る
for b in bars_of("A1")[4:]:
    st = b * BAR
    P("lead").add(st + 24 * 2, E5 + 12 + root_of(b) % 12 + 7, 16, "!~")

def jp(name, instrument, role, vol, pan, amp="auto", extra=None, tok=None):
    d = {"instrument": instrument, "role": role, "volume": vol, "pan": pan, "amp": amp, "notes": tok if tok is not None else parts[name].tokens()}
    if extra: d.update(extra)
    return d

song = {
    "title": "歪んだ時計仕掛け（プログレッシブメタル・変拍子）",
    "description": "（見本・仮）プログレッシブメタル。12拍の1小節を、7+7+5+5・5+5+5+5+4・3拍×8・11+13（8分）などに組み替えた変拍子。刻みのリフ、音階のユニゾン走句、アルペジオ・音階列のテクニカルなソロ。最後のサビは全音上げ。歌なし。約4分。",
    "dynamics": "natural", "bpm": 150, "beats": 12, "chords": " ".join(CHORDS), "barsPerChord": 1, "repeats": 1,
    "autoAccompaniment": False, "feel": "rock", "tone": "metal", "human": 0.18, "instrumentCheck": False,
    "grouping": [7 // 7 * 0 + 3] * 0 or "auto",
    "parts": [
        jp("kick", "kick", "バスドラ（リフに合わせて）", 0.22, 0, tok=" ".join(drum["kick"])),
        jp("snare", "snare", "スネア（まとまりの頭）", 0.16, 0, tok=" ".join(drum["snare"]), extra={"push": 0.02}),
        jp("hihat", "hihat", "ハイハット", 0.065, 0.3, tok=" ".join(drum["hihat"]), extra={"push": -0.01}),
        jp("bass", "bass", "ベース（リフに合わせる）", 0.17, 0),
        jp("rgL", "distGuitar", "リフ（左）", 0.09, -0.9, amp="loudmetal"),
        jp("rgR", "distGuitar", "リフ（右）／和音の5度", 0.09, 0.9, amp="loudmetal"),
        jp("lead", "leadGuitar", "リード（旋律・走句・ソロ）", 0.11, 0.1, amp="loudrock", extra={"noRestrike": True}),
        jp("clean", "guitar", "クリーンのアルペジオ", 0.12, -0.4, amp="clean", extra={"sustain": 1.8, "chorus": 0, "reverb": 0.3}),
    ],
}
del song["grouping"]
# パートは1曲に最大8つなので、使用頻度の低いものを減らす（ここでは確認のみ）
out = sys.argv[1] if len(sys.argv) > 1 else "prog-tech-odd.json"
json.dump(song, open(out, "w"), ensure_ascii=False, indent=1)
print("書き出し:", out, "パート", len(song["parts"]))
