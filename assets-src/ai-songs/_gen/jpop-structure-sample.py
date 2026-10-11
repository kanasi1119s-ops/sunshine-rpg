#!/usr/bin/env python3
"""「ひかりの手前」（J-POPの組み立ての見本・仮）の生成スクリプト。
docs/sound/jpop-structure-guide.md の手順で作った試作。完全オリジナル（CLAUDE.md 1-1）。
- Gメジャー・BPM124・120小節（約3分52秒）。ラスサビで全音上げ（modulate、Aメジャー）。
- 旋律（lead・echoGuitar）は下の MEL_* に1小節ずつ手で書いてある。モチーフ H（裏拍の出だし→長い音→階段で下りる）を
  Aメロ・イントロ・サビ・落ちサビで形を変えて使い回す。
- 伴奏（ドラム・ベース・ピアノ・ギター・弦）は、コードと区間から小節ごとの型で並べる。
実行: python3 assets-src/ai-songs/_gen/jpop-structure-sample.py
"""
import json
import os
import re

BPM = 124
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def md(name):
    g = re.match(r"^([A-G][#b]?)(-?\d)$", name)
    n = g.group(1)
    if len(n) == 2 and n[1] == "b":
        base = NAMES.index(n[0]) - 1
    else:
        base = NAMES.index(n)
    return base + 12 * (int(g.group(2)) + 1)


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def beats(bar):
    """1小節の文字列の拍の合計（4拍になっているかの確認用）。"""
    t = 0.0
    for tok in bar.split():
        t += float(tok.split(":")[1].rstrip("!,'_~^/\\"))
    return t


# ───────── 構成（小節数）─────────
SECTIONS = [
    ("intro", 8), ("verse", 8), ("pre", 8), ("chorus", 16), ("interlude", 8),
    ("verse", 8), ("pre", 8), ("chorus", 16), ("bridge", 8), ("break", 8),
    ("chorus", 16), ("outro", 8),
]
TAGS = ["intro", "A1", "B1", "C1", "inter", "A2", "B2", "C2", "bridge", "ochi", "C3", "outro"]

# ───────── コード進行（Gメジャー、1小節1コード）─────────
INTRO = "Gadd9 Gadd9 Cmaj7 Cmaj7 Gadd9 Em7 Cmaj7 Dsus4".split()
A1 = "Gmaj7 D/F# Em7 Bm7 Cmaj7 G/B Am7 Dsus4".split()          # カノン系（ベースが下がる）
A2 = "Gmaj7 D/F# Em7 Bm7 Cmaj7 Cm6 Am7 Dsus4".split()          # 2番: 5〜6小節を借用 iv に差し替え
B1 = "Cmaj7 Bm7 Em7 E7 Am7 Cm6 Dsus4 D7".split()              # セカンダリードミナント＋借用 iv＋ドミナント溜め
B2 = "Cmaj7 B7 Em7 E7 Am7 Cm6 Dsus4 D7".split()                # 2番: 2小節目を B7（V7/vi）に
CH_X = "Cmaj7 D Bm7 Em7 Am7 Bm7 Cmaj7 D".split()               # サビ前半: 王道系（IV–V–iii–vi…）。V で止める
CH_Y = "Cmaj7 D G/B E7 Am7 D7 Gadd9 Gadd9".split()             # サビ後半: I/3 → V7/ii → V7 → I に着地
INTER = "Em7 Cmaj7 Gadd9 D/F# Em7 Cmaj7 Am7 Dsus4".split()      # 間奏: vi–IV–I–V 系
BRIDGE = "Em7 Em7/D Cmaj7 Cm6 Bm7 E7 Am7 Dsus4".split()        # Cメロ: vi 始まり、主音を避ける
OCHI = "Cmaj7 D Bm7 Em7 Am7 D7 B7 E7".split()                  # 落ちサビ: 最後は属七の連鎖（新しい調の V7 へ）
OUTRO = "Gadd9 D/F# Em7 Cmaj7 Gadd9 D/F# Cmaj7 Gadd9".split()

CHORDS = (INTRO + A1 + B1 + CH_X + CH_Y + INTER + A2 + B2 + CH_X + CH_Y + BRIDGE + OCHI + CH_X + CH_Y + OUTRO)
assert len(CHORDS) == sum(b for _, b in SECTIONS) == 120

# コードごとの音: bass=ベース, pool=分散和音の4音（低→高）, v=弦の2声（高, 低）
CH = {
    "Gadd9":   dict(bass="G2",  pool=["G3", "D4", "A4", "B4"],  v=("B4", "D4")),
    "Gmaj7":   dict(bass="G2",  pool=["G3", "D4", "F#4", "B4"], v=("B4", "F#4")),
    "D/F#":    dict(bass="F#2", pool=["A3", "D4", "F#4", "A4"], v=("A4", "F#4")),
    "Em7":     dict(bass="E2",  pool=["E3", "G3", "D4", "B4"],  v=("G4", "B3")),
    "Bm7":     dict(bass="B2",  pool=["B3", "F#4", "A4", "D5"], v=("A4", "D4")),
    "Cmaj7":   dict(bass="C2",  pool=["C4", "E4", "G4", "D5"],  v=("B4", "E4")),
    "G/B":     dict(bass="B2",  pool=["B3", "D4", "G4", "D5"],  v=("D5", "G4")),
    "Am7":     dict(bass="A2",  pool=["A3", "E4", "G4", "C5"],  v=("C5", "E4")),
    "Dsus4":   dict(bass="D2",  pool=["D4", "G4", "A4", "D5"],  v=("A4", "G4")),
    "D":       dict(bass="D2",  pool=["D4", "F#4", "A4", "D5"], v=("A4", "F#4")),
    "D7":      dict(bass="D2",  pool=["D4", "F#4", "A4", "C5"], v=("C5", "F#4")),
    "E7":      dict(bass="E2",  pool=["E4", "G#4", "B4", "D5"], v=("D5", "G#4")),
    "Cm6":     dict(bass="C2",  pool=["C4", "D#4", "G4", "A4"], v=("A4", "D#4")),
    "B7":      dict(bass="B2",  pool=["B3", "D#4", "F#4", "A4"], v=("A4", "D#4")),
    "Em7/D":   dict(bass="D3",  pool=["E4", "G4", "B4", "D5"],  v=("G4", "D4")),
}
ROOT_PC = {"Gadd9": 7, "Gmaj7": 7, "D/F#": 2, "Em7": 4, "Bm7": 11, "Cmaj7": 0, "G/B": 7, "Am7": 9, "Dsus4": 2,
           "D": 2, "D7": 2, "E7": 4, "Cm6": 0, "B7": 11, "Em7/D": 4}

# ───────── 旋律（手書き。1小節＝1要素、合計4拍）─────────
H = "R:0.5 G4:0.5 C5:1.5 B4:0.5 G4:0.5 A4:0.5"   # モチーフ H（サビの頭。イントロ・落ちサビにも出る）

MEL_A1 = [
    "R:0.5 D4:0.5 G4:0.5 G4:0.5 B4:1 A4:0.5 G4:0.5",
    "A4:0.5 F#4:0.5 D4:1 R:0.5 D4:0.5 F#4:0.5 A4:0.5",
    "G4:0.5 B4:0.5 B4:1 A4:0.5 G4:0.5 E4:1",
    "D4:0.5 F#4:0.5 A4:0.5 F#4:0.5 D4:2",
    "R:0.5 E4:0.5 G4:0.5 G4:0.5 C5:1 B4:0.5 A4:0.5",
    "B4:0.5 A4:0.5 G4:1 R:0.5 G4:0.5 B4:0.5 D5:0.5",
    "C5:0.5 B4:0.5 A4:1 G4:0.5 A4:0.5 B4:1",
    "A4:1 G4:0.5 A4:0.5 R:2",
]
MEL_A2 = MEL_A1[:4] + [
    "R:0.5 E4:0.5 G4:0.5 G4:0.5 C5:1.5 D5:0.5",
    "A4:0.5 G4:0.5 G4:1 R:0.5 G4:0.5 A4:0.5 C5:0.5",
    "D5:0.5 C5:0.5 A4:1 G4:0.5 A4:0.5 C5:1",
    "A4:1 G4:0.5 A4:0.5 B4:1 R:1",
]
MEL_B1 = [
    "E4:0.5 G4:0.5 C5:1 B4:0.5 G4:0.5 E4:0.5 G4:0.5",
    "F#4:0.5 A4:0.5 D5:1 B4:0.5 A4:0.5 F#4:0.5 A4:0.5",
    "G4:0.5 B4:0.5 D5:1 B4:0.5 A4:0.5 G4:0.5 B4:0.5",
    "B4:0.5 G#4:0.5 B4:1 D5:0.5 B4:0.5 G#4:1",
    "A4:0.5 C5:0.5 D5:1 C5:0.5 A4:0.5 C5:1",
    "C5:1 D5:0.5 D#5:0.5 D5:1 C5:1",
    "A4:1.5 B4:0.5 D5:2",
    "D5:0.5 C5:0.5 A4:1 A4:1 R:1",
]
MEL_B2 = MEL_B1[:1] + [
    "F#4:0.5 B4:0.5 D#5:1 F#5:0.5 D#5:0.5 B4:0.5 F#4:0.5",   # B7 の上: 導音 D# をきかせる
] + MEL_B1[2:]
# サビ前半（V で止める）。サビ2回目は最後の小節だけ変える
MEL_CH_X = [
    H,
    "R:0.5 A4:0.5 D5:1.5 C5:0.5 A4:0.5 B4:0.5",
    "R:0.5 B4:0.5 D5:1.5 C5:0.5 B4:0.5 D5:0.5",
    "G4:0.5 B4:0.5 B4:1.5 A4:0.5 R:1",
    "R:0.5 A4:0.5 C5:1 E5:2",
    "D5:1.5 C5:0.5 B4:1 A4:1",
    "R:0.5 G4:0.5 C5:1.5 B4:0.5 A4:0.5 B4:0.5",
    "A4:1.5 G4:0.5 F#4:1 R:1",
]
MEL_CH_X2 = (["R:0.5 G4:0.5 C5:1 C5:0.5 B4:0.5 G4:0.5 A4:0.5", MEL_CH_X[1], "R:0.5 B4:0.5 D5:1 E5:1 D5:0.5 B4:0.5", MEL_CH_X[3],
              "R:0.5 A4:0.5 C5:1 E5:1.5 D5:0.5"] + MEL_CH_X[5:7] + ["A4:1.5 G4:0.5 B4:1 R:1"])
MEL_CH_XL = [  # ラスサビ前半: 出だしを3度高く（頂点を先取りして景色を変える）
    "R:0.5 B4:0.5 E5:1.5 D5:0.5 B4:0.5 C5:0.5",
    "R:0.5 D5:0.5 F#5:1.5 E5:0.5 D5:0.5 E5:0.5",
] + ["R:0.5 D5:0.5 D5:1 E5:1 D5:0.5 B4:0.5"] + MEL_CH_X[3:7] + ["A4:1 B4:0.5 D5:1.5 R:1"]
# サビ後半（頂点 G5 は後半の3小節目、最後は主音で着地）
MEL_CH_Y = [
    H,
    "R:0.5 A4:0.5 D5:1.5 C5:0.5 A4:0.5 B4:0.5",
    "R:0.5 D5:0.5 G5:1.5 F#5:0.5 E5:0.5 D5:0.5",
    "E5:1 D5:0.5 B4:0.5 G#4:1 R:1",
    "R:0.5 A4:0.5 C5:1 E5:1.5 D5:0.5",
    "C5:1 A4:1 F#4:1 A4:1",
    "R:0.5 B4:0.5 D5:1.5 B4:0.5 A4:0.5 B4:0.5",
    "G4:3 R:1",
]
MEL_CH_Y2 = MEL_CH_Y[:2] + ["R:0.5 D5:0.5 G5:1 F#5:0.5 G5:0.5 E5:0.5 D5:0.5", "E5:1 D5:0.5 B4:0.5 G#4:0.5 B4:0.5 G#4:0.5 R:0.5"] + [MEL_CH_Y[4], "C5:1 A4:0.5 C5:0.5 F#4:1 A4:1"] + MEL_CH_Y[6:]
MEL_CH_YL = [
    "R:0.5 G4:0.5 C5:1 E5:1 D5:0.5 C5:0.5",
    "R:0.5 A4:0.5 D5:1 F#5:1 E5:0.5 D5:0.5",
] + MEL_CH_Y[2:7] + ["G4:4"]
MEL_INTER = [  # 間奏（echoGuitar）
    "R:0.5 G4:0.5 B4:1.5 A4:0.5 G4:0.5 B4:0.5",
    "R:0.5 G4:0.5 C5:1.5 B4:0.5 G4:0.5 E5:0.5",
    "R:0.5 B4:0.5 D5:1 E5:1.5 D5:0.5",
    "E5:1 D5:1 A4:1 F#4:1",
    "R:0.5 G4:0.5 B4:1 E5:1.5 D5:0.5",
    "C5:1 B4:0.5 G4:0.5 E4:1 G4:1",
    "A4:0.5 C5:0.5 E5:1 D5:0.5 C5:0.5 A4:1",
    "A4:1.5 G4:0.5 A4:1 R:1",
]
MEL_BRIDGE = [
    "R:1 B4:1 B4:1 A4:0.5 B4:0.5",
    "G4:2 E4:1 R:1",
    "R:1 E5:1 D5:1 C5:1",
    "D5:1.5 D#5:0.5 D5:1 R:1",
    "R:0.5 D5:0.5 F#5:1.5 E5:0.5 D5:1",
    "E5:1 B4:1 G#4:1 B4:1",
    "C5:0.5 D5:0.5 E5:1.5 D5:0.5 C5:1",
    "A4:1.5 G4:0.5 A4:1 R:1",
]
MEL_OCHI = [
    "R:1 G4:0.5 C5:1.5 B4:0.5 G4:0.5",
    "R:1 A4:0.5 D5:1.5 C5:0.5 A4:0.5",
    "R:1 B4:0.5 D5:1.5 C5:0.5 B4:0.5",
    "G4:1 B4:1 A4:1 R:1",
    "R:0.5 A4:0.5 C5:1 E5:2",
    "D5:1.5 C5:0.5 A4:1 F#4:1",
    "R:0.5 B4:0.5 D#5:1.5 E5:0.5 D#5:0.5 B4:0.5",
    "E5:2 D5:0.5 B4:0.5 R:1",
]
# イントロのフック（5〜8小節目）。1〜4小節目は分散和音だけ。アウトロでも使う
HOOK = [
    "R:0.5 B4:0.5 D5:1.5 C5:0.5 B4:0.5 G4:0.5",
    "R:0.5 B4:0.5 E5:1.5 D5:0.5 B4:0.5 D5:0.5",
    "R:0.5 G4:0.5 C5:1.5 B4:0.5 G4:0.5 A4:0.5",
    "A4:2 G4:1 R:1",
]
OUTRO_HOOK = [  # 転調後（+2）に鳴るので、書く音は低めにして E5 を超えないようにする
    "R:0.5 B4:0.5 D5:1.5 C5:0.5 B4:0.5 G4:0.5",
    "R:0.5 A4:0.5 D5:1.5 C5:0.5 A4:0.5 C5:0.5",
    "R:0.5 G4:0.5 C5:1.5 B4:0.5 G4:0.5 A4:0.5",
    "G4:4",
]

for blk in (MEL_A1, MEL_A2, MEL_B1, MEL_B2, MEL_CH_X, MEL_CH_X2, MEL_CH_XL, MEL_CH_YL, MEL_CH_Y2, MEL_CH_Y, MEL_INTER, MEL_BRIDGE, MEL_OCHI, HOOK, OUTRO_HOOK):
    assert len(blk) in (8, 4), blk
    for b in blk:
        assert abs(beats(b) - 4) < 1e-9, (b, beats(b))

R4 = "R:4"
# 区間ごとの小節の並び（旋律）。None＝休み
LEAD = (
    [R4] * 8 + MEL_A1 + MEL_B1 + MEL_CH_X + MEL_CH_Y + [R4] * 8
    + MEL_A2 + MEL_B2 + MEL_CH_X2 + MEL_CH_Y2 + MEL_BRIDGE + MEL_OCHI + MEL_CH_XL + MEL_CH_YL + [R4] * 8
)
ECHO = (
    [R4] * 4 + HOOK + [R4] * 8 + [R4] * 8 + [R4] * 16 + MEL_INTER
    + [R4] * 8 + [R4] * 8 + [R4] * 16 + [R4] * 8 + [R4] * 8 + [R4] * 16 + OUTRO_HOOK + [R4] * 4
)
assert len(LEAD) == len(ECHO) == 120, (len(LEAD), len(ECHO))


# ───────── 小節ごとの区間の名前 ─────────
def tag_of(bar):  # bar: 0始まり
    i = 0
    for tag, (_, n) in zip(TAGS, SECTIONS):
        if bar < i + n:
            return tag, bar - i
        i += n
    raise IndexError


def next_root(bar):
    if bar + 1 < 120:
        return ROOT_PC[CHORDS[bar + 1]]
    return ROOT_PC[CHORDS[bar]]


def approach_note(bar, octave_of):
    """次のコードの根音の半音下（経過音）。"""
    base = md(CH[CHORDS[bar]]["bass"])
    pc = (next_root(bar) - 1) % 12
    cand = [m for m in range(base - 7, base + 8) if m % 12 == pc]
    best = min(cand, key=lambda m: abs(m - base))
    while best > md("C3"):
        best -= 12
    return nm(best)


# ───────── ベース ─────────
def bass_bar(bar):
    tag, k = tag_of(bar)
    c = CH[CHORDS[bar]]
    r = c["bass"]
    r8 = nm(md(r) + 12) if md(r) + 12 <= md("C3") else r
    fifth = nm(md(r) + 7) if md(r) + 7 <= md("C3") else nm(md(r) - 5)
    ap = approach_note(bar, None)
    if tag == "intro":
        return R4 if k < 4 else f"{r}:4_"
    if tag in ("A1", "A2"):
        return f"{r}:3! {ap}:0.5 R:0.5" if k % 2 == 0 else f"{r}:2.5! {fifth}:0.5 {ap}:0.5 R:0.5"
    if tag in ("B1", "B2"):
        if k == 7:  # ドミナントの溜め: 最後の拍は止める
            return f"{r}:1! {r}:0.5 {r8}:0.5 {r}:1 R:1"
        return f"{r}:1! {r}:0.5 {r8}:0.5 {r}:1 {r}:0.5 {ap}:0.5"
    if tag in ("C1", "C2", "C3"):
        if k == 0 and tag != "C1" and False:
            pass
        return f"{r}:0.5! {r}:0.5 {r8}:0.5 {r}:0.5 {r}:0.5! {fifth}:0.5 {r8}:0.5 {ap}:0.5"
    if tag == "inter":
        return f"{r}:1.5! {r8}:0.5 {r}:1.5 {ap}:0.5"
    if tag == "bridge":
        if k == 7:
            return f"{r}:2! R:2"
        return f"{r}:3! R:1" if k % 2 == 0 else f"{r}:2! {fifth}:1 R:1"
    if tag == "ochi":
        return f"{r}:4_" if k < 7 else f"{r}:3! R:1"
    if tag == "outro":
        return f"{r}:4_" if k < 7 else f"{r}:4"
    raise ValueError(tag)


BASS = [bass_bar(i) for i in range(120)]
for b in BASS:
    assert abs(beats(b) - 4) < 1e-9, b


# ───────── ギター（sparkleClean）の分散和音 ─────────
def sorted_pool(chord):
    return sorted(CH[chord]["pool"], key=md)


P8 = [0, 1, 2, 3, 2, 1, 2, 3]
P16 = [0, 2, 1, 3, 2, 3, 1, 2, 0, 2, 1, 3, 2, 3, 1, 3]


def guitar_bar(bar):
    tag, k = tag_of(bar)
    pool = sorted_pool(CHORDS[bar])
    if tag in ("intro", "A1", "A2", "outro", "inter"):
        if ECHO[bar] != R4:  # エコーギターのフックが鳴る小節は、半音でぶつからないよう低い3音だけで回す
            low = pool[:3]
            return " ".join(f"{low[p]}:0.5{'!' if i % 4 == 0 else ''}" for i, p in enumerate([0, 1, 2, 1, 0, 1, 2, 1]))
        return " ".join(f"{pool[p]}:0.5{'!' if i % 4 == 0 else ''}" for i, p in enumerate(P8))
    if tag in ("B1", "B2"):
        if k == 7:
            return " ".join(f"{pool[p]}:0.5{'!' if i % 4 == 0 else ''}" for i, p in enumerate(P8[:6])) + " R:1"
        return " ".join(f"{pool[p]}:0.5{'!' if i % 2 == 0 else ''}" for i, p in enumerate(P8))
    if tag in ("C1", "C2", "C3"):
        return " ".join(f"{pool[p]}:0.25{'!' if i % 4 == 0 else ''}" for i, p in enumerate(P16))
    if tag == "bridge":
        return f"{pool[0]}:1! {pool[2]}:1 {pool[3]}:1 {pool[2]}:1"
    if tag == "ochi":
        return R4
    raise ValueError(tag)


GUITAR = [guitar_bar(i) for i in range(120)]
for i in range(8):  # イントロの前半は分散和音だけ（そのまま）
    pass
for b in GUITAR:
    assert abs(beats(b) - 4) < 1e-9, b


# ───────── ピアノ ─────────
def piano_bar(bar):
    tag, k = tag_of(bar)
    pool = sorted_pool(CHORDS[bar])
    if tag == "intro":
        if k < 4:
            return R4
        return f"{pool[3]}:1, R:1 {pool[2]}:1, R:1"
    if tag in ("A1", "A2"):
        return f"{pool[1]}:1, R:1 {pool[3]}:1, R:1"
    if tag in ("B1", "B2"):
        order = [0, 2, 1, 3, 0, 2, 1, 3]
        return " ".join(f"{pool[p]}:0.5{'!' if i % 2 == 0 else ','}" for i, p in enumerate(order))
    if tag in ("C1", "C2", "C3"):
        order = [1, 2, 3, 2, 1, 2, 3, 2]
        return " ".join(f"{pool[p]}:0.5{'!' if i % 2 == 0 else ','}" for i, p in enumerate(order))
    if tag == "inter":
        return f"{pool[2]}:1! {pool[3]}:1 {pool[2]}:1 {pool[1]}:1"
    if tag == "bridge":
        return f"{pool[1]}:1! {pool[2]}:1 {pool[3]}:2"
    if tag == "ochi":
        order = [0, 1, 2, 3, 2, 1, 2, 1]
        return " ".join(f"{pool[p]}:0.5{'!' if i % 4 == 0 else ','}" for i, p in enumerate(order))
    if tag == "outro":
        return f"{pool[1]}:2! {pool[3]}:2" if k < 7 else f"{pool[0]}:4"
    raise ValueError(tag)


PIANO = [piano_bar(i) for i in range(120)]
for b in PIANO:
    assert abs(beats(b) - 4) < 1e-9, b


# ───────── 弦（2声）─────────
def strings_bar(bar, hi):
    tag, k = tag_of(bar)
    v = CH[CHORDS[bar]]["v"]
    n = v[0] if hi else v[1]
    if tag == "intro":
        return R4 if k < 2 else f"{n}:4_"
    if tag in ("A1", "A2"):
        return R4
    if tag in ("B1", "B2"):
        return R4 if k < 2 else f"{n}:4_"
    if tag in ("C1", "C2", "C3"):
        return f"{n}:4_"
    if tag == "inter":
        return R4
    if tag == "bridge":
        return f"{n}:4_"
    if tag == "ochi":
        return R4
    if tag == "outro":
        return f"{n}:4_" if k < 6 else R4
    raise ValueError(tag)


# ───────── ドラム（16文字のグリッド）─────────
SIL = "g:................"


def drums_bar(bar):
    """(kick, snare, hat, crash) の4つのグリッド。"""
    tag, k = tag_of(bar)
    kick = snare = hat = crash = SIL
    if tag == "intro":
        if k == 6:
            hat = "g:x.x.x.x.x.x.x.x."
        if k == 7:
            kick = "g:x.......x......."
            snare = "g:........xxxxXXXX"[:18]
            snare = "g:..........xxxXXX"[:18]
            hat = "g:x.x.x.x........."
        return kick, snare, hat, crash
    if tag in ("A1", "A2"):
        kick = "g:x.......x......." if k % 2 == 0 else "g:x.....x.x......."
        snare = "g:....o.......o..."
        hat = "g:x.o.x.o.x.o.x.o."
        if k == 0:
            crash = "g:x..............."
        return kick, snare, hat, crash
    if tag in ("B1", "B2"):
        kick = "g:x.....x.x.....x." if k % 2 == 0 else "g:x.......x.x....."
        snare = "g:....x.......x..."
        hat = "g:X.x.X.x.X.x.X.x." if k < 4 else "g:X.xxX.xxX.xxX.xx"[:18]
        if k == 7:  # 3拍目までで止める（4拍目は全員休む）
            kick = "g:x.......x......."
            snare = "g:....x...x.x.x..."[:18]
            snare = "g:....x...xxxx...."
            hat = "g:X.x.X.x.X.x....."
        return kick, snare, hat, crash
    if tag in ("C1", "C2", "C3"):
        kick = "g:X.......x.x....." if k % 2 == 0 else "g:X.....x.x.x....."
        snare = "g:....X.......X..."
        hat = "g:X.x.x.x.X.x.x.x." if k % 4 != 3 else "g:X.x.x.x.X.x.xOx."[:18]
        if k in (0, 8):
            crash = "g:X..............."
        if k == 7 and tag != "C1":
            pass
        if k in (7, 15):  # 区切りのフィル
            snare = "g:....X...x.x.xxXX"
            kick = "g:X.......x.x.x.x."[:18]
            hat = "g:X.x.x.x.........."[:18]
        if k == 15:
            kick = "g:X.......x......."
        return kick, snare, hat, crash
    if tag == "inter":
        kick = "g:x.......x......." if k % 2 == 0 else "g:x.....x.x......."
        snare = "g:....x.......x..." if k >= 4 else "g:................"
        hat = "g:x.x.x.x.x.x.x.x."
        if k == 0:
            crash = "g:x..............."
        if k == 7:
            snare = "g:....x...x.x.xxxx"
        return kick, snare, hat, crash
    if tag == "bridge":
        hat = "g:x...o...x...o..." if k < 4 else "g:x.o.x.o.x.o.x.o."
        if k >= 4:
            kick = "g:x.......x......."
        if k == 7:
            kick = "g:x......."+"........"
            snare = "g:......x.x.x.xxXX"[:18]
            snare = "g:..........xxxXXX"[:18]
            hat = "g:x.o.x.o........."
        return kick, snare, hat, crash
    if tag == "ochi":
        if k == 7:  # 転調への助走: スネアを16分で強くしていく（ドラムは転調しない）
            snare = "g:ooooooooxxxxXXXX"[:18]
            kick = "g:x...x...x...x..."
        return kick, snare, hat, crash
    if tag == "outro":
        if k < 4:
            kick = "g:x.......x......." if k % 2 == 0 else "g:x.....x.x......."
            hat = "g:x.o.x.o.x.o.x.o."
            if k == 0:
                crash = "g:X..............."
        elif k == 4:
            kick = "g:x.......x......."
            hat = "g:x...x...x...x..."
        elif k == 7:
            kick = "g:x..............."
        return kick, snare, hat, crash
    raise ValueError(tag)


DR = [drums_bar(i) for i in range(120)]


def join_drum(idx):
    toks = []
    for d in DR:
        g = d[idx]
        toks.append("R:4" if g == SIL else g[:18] if len(g) > 18 else g)
    return " ".join(toks)


# グリッドは16文字ちょうどに整える
def fix(g):
    if g.startswith("g:"):
        body = g[2:]
        body = (body + "." * 16)[:16]
        return "g:" + body
    return g


DR = [tuple(fix(g) for g in d) for d in DR]


def no_hat_on_crash(d):
    k, sn, h, c = d
    if c != "g:................":
        hb = list(h[2:])
        for i, ch in enumerate(c[2:]):
            if ch != ".":
                hb[i] = "."
        h = "g:" + "".join(hb)
    return (k, sn, h, c)


DR = [no_hat_on_crash(d) for d in DR]


def drum_part(i):
    return " ".join("R:4" if d[i] == SIL else d[i] for d in DR)


def part(**kw):
    return kw


parts = [
    part(instrument="kick", role="キック（Aメロは小さく、サビで開く）", volume=0.18, pan=0, amp="auto", notes=drum_part(0)),
    part(instrument="snare", role="スネア（Bメロから。サビ前は止める）", volume=0.12, pan=0, amp="auto", notes=drum_part(1), push=0.025),
    part(instrument="hihat", role="ハイハット（A＝8分の弱め→B＝強弱→サビ＝オープン混じり）", volume=0.05, pan=0.3, amp="auto", notes=drum_part(2), push=-0.01),
    part(instrument="crash", role="クラッシュ（区間の頭）", volume=0.06, pan=-0.3, amp="auto", notes=drum_part(3)),
    part(instrument="bass", role="ベース（Aメロ＝長い音、Bメロ＝動く、サビ＝8分）", volume=0.15, pan=0, amp="auto", notes=" ".join(BASS), push=0.0, duck=0.2),
    part(instrument="piano", role="ピアノ", volume=0.09, pan=0.35, amp="auto", notes=" ".join(PIANO), sustain=1.8, phrase=4),
    part(instrument="guitar", role="クリーンギター（分散和音。sparkleClean）", volume=0.11, pan=-0.4, amp="sparkleClean", notes=" ".join(GUITAR), sustain=1.6, reverb=0.3, chorus=0),
    part(instrument="echoGuitar", role="エコーギター（イントロ・間奏・アウトロのフック）", volume=0.12, pan=0.1, amp="crystal", notes=" ".join(ECHO), echo={"repeats": 2, "time": "dotted8", "decay": 0.28}, reverb=0.35, sustain=1.3, phrase=4),
    part(instrument="lead", role="メロディ（歌のパート）", volume=0.18, pan=0, amp="auto", notes=" ".join(LEAD), sustain=0.95, phrase=4, breath=True, sections={"break": 0.7}),
    part(instrument="strings", role="弦（上の声）", volume=0.05, pan=-0.6, amp="auto", notes=" ".join(strings_bar(i, True) for i in range(120)), sustain=1.5),
    part(instrument="strings", role="弦（下の声）", volume=0.05, pan=0.6, amp="auto", notes=" ".join(strings_bar(i, False) for i in range(120)), sustain=1.5),
]

song = {
    "title": "ひかりの手前（J-POPの組み立ての見本・仮）",
    "description": (
        "（仮・試作）docs/sound/jpop-structure-guide.md の手順で作った J-POP の見本。Gメジャー・BPM124・120小節（約3分52秒）。"
        "イントロ8→Aメロ8→Bメロ8→サビ16→間奏8→Aメロ8→Bメロ8→サビ16→Cメロ8→落ちサビ8→ラスサビ16（全音上げでAメジャー）→アウトロ8。"
        "進行は区間ごとに変えた: Aメロ＝カノン系（ベースが下がる分数コード）、2番Aメロは借用iv（Cm6）に差し替え、"
        "Bメロ＝セカンダリードミナント（E7・2番はB7）＋借用iv＋Dsus4→D7のドミナント溜め（最後の1拍は全員止める）、"
        "サビ＝王道系（IV–V–iii–vi…）で前半はVで止め、後半はG/B→E7→Am7→D7→Gで着地、間奏＝vi–IV–I–V系、"
        "Cメロ＝vi始まりで主音を避ける、落ちサビ＝B7→E7の属七の連鎖で転調へ。"
        "旋律は手書き。モチーフ（裏拍の出だし→長い音→階段で下りる）をイントロのフック・Aメロ・サビ・落ちサビで形を変えて使い回した。"
        "サビの頂点は後半の3小節目（G5、転調後はA5）。ギターのクリーンは sparkleClean／crystal（jpopClean は使わない）。歌なし。"
    ),
    "bpm": BPM,
    "beats": 4,
    "chords": " ".join(CHORDS),
    "barsPerChord": 1,
    "repeats": 1,
    "autoAccompaniment": False,
    "feel": "pop",
    "tone": "pop",
    "synth": True,
    "human": 0.35,
    "fills": False,
    "sections": [{"kind": k, "bars": n} for k, n in SECTIONS],
    "modulate": {"at": "lastChorus", "semitones": 2},
    "drumMix": {"hat": {"level": 0.8, "pan": -0.3, "reverb": 0.08}, "snare": {"reverb": 0.18}, "crash": {"level": 0.85, "pan": 0.35, "reverb": 0.2}},
    "parts": parts,
}

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "jpop-structure-sample.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(song, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("wrote", os.path.normpath(out), "bars", len(CHORDS))
