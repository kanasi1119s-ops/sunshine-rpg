# 『星降る夏祭りの夜』（仮）: 夏祭りの夜。透き通った空に星が輝き、しんみりするような、楽しいような、思い出になるようなケルト音楽
#   （2026-10-16、人間の依頼「4分半から5分ほどのケルト音楽。夏祭のような感じで夜の透き通った空に輝く星々が、しんみりするような楽しいような思い出になるような曲」）。
# 6/8（1小節に2拍、1拍を3つに分ける）。テンポが動く: ゆっくりの歌は付点4分＝52、祭りのジグは112、思い出の歌は60、最後のジグは116、星の終わりは52。
# ニ長調 → 最後のジグで全音上のホ長調へ。190小節・約4分45秒。
# 形と、だれが鳴るか:
#   星8（ハープの分散和音と、ディレイのかかった鉄琴の星だけ → ピアノの右手と弦がそっと）
#   → 星空の歌16（笛。ピアノの左手と右手・ハープ・チェロ）→ 星空の歌の2回目16（フィドル。笛は3度下でハモり、アコーディオンが和音をのばす）
#   → 祭りの合図4（ボーランとアコギ。テンポが一気に上がる）
#   → 祭りのジグ32（笛。A A B B。アコギの6/8の刻み・指弾きのベース・ピアノの「ずん・ちゃっ」・ボーラン）
#   → 祭りのジグ2回目32（フィドルとアコーディオン。B では木琴が跳ね回り、ドラム・ライドも入る。B の終わりに ♭VI の B♭ で花火のように）
#   → 思い出の歌16（テンポを落として。フィドル・ピアノ・弦・鉄琴の星。ドラムなし）→ 戻る4（だんだん速く）
#   → 最後のジグ48（ホ長調。新しい旋律 C を笛とフィドルで → A・B を全音上で全員。鉄琴が旋律の1オクターブ上）
#   → 星の終わり14（だんだん遅くなって、星空の歌の頭をホ長調で。最後はマイナーの iv（Am6）を通って E に）
# 人間の指示（2026-10-16）: FX を使う／ピアノは左手と右手で弾く（右手は和音を同時に）／定番から外したコード進行。
#   進行: 星空の歌は D A/C# Bm7 Gmaj7 Em7 Gm6（マイナーの iv＝懐かしさ）D/A A7sus4、2回目は F#7/A#（III7）から Bm へ。
#   ジグの A は D C/D G/D（ミクソリディアン）、B は G A F#m Bm Em7 A7 B♭（♭VI＝花火）A7。思い出の歌は Gm/B♭ と E7（V/V）。
# MIDI のチャンネルは（ドラム以外で）15まで。同じ楽器のパートは pan・reverb・fx をそろえて共有させる。
# 既存の曲のメロディは使わない（CLAUDE.md 1-1）。旋律はすべてこの曲のために書いたもの。
# 使い方: python3 celtic-summer-night.py <出力.json>
# 書き出し: --drums muldjord --bass finger --orchestra vsco --piano salamander --guitar shiny-acoustic --master-preset rock-clean --master -13.5（点数 8.04）
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from celtic_lib import Song, nm, md, fmt

T3 = fmt(1 / 3)
# ---------------- 音階 ----------------
DMAJ = [2, 4, 6, 7, 9, 11, 1]; DMIX = [2, 4, 6, 7, 9, 11, 0]; DHM = [2, 4, 6, 7, 9, 10, 1]   # ニ長調・ミクソリディアン・和声的長音階（Gm6・B♭）
BHM = [11, 1, 2, 4, 6, 7, 10]                                                                # ロ短調（和声的。F#7 の上）
EMAJ = [4, 6, 8, 9, 11, 1, 3]; EMIX = [4, 6, 8, 9, 11, 1, 2]; EHM = [4, 6, 8, 9, 11, 0, 3]   # ホ長調・ミクソリディアン・和声的長音階（Am6・C）
def scale_of(ch, key):
    c = ch.split("/")[0]
    if key == "E":
        if c in ("D",): return EMIX
        if c.startswith("Am") or c == "C": return EHM
        return EMAJ
    if c == "C": return DMIX
    if c.startswith("Gm") or c == "Bb": return DHM
    if c.startswith("F#7") or c.startswith("E7"): return BHM if c.startswith("F#7") else [9, 11, 1, 2, 4, 6, 8]   # E7 の上は A の和声的（G#）
    return DMAJ

# ---------------- 旋律（すべてこの曲のために書いた） ----------------
AIR1 = ["F#5:3 E5:1 D5:2", "E5:4 C#5:2", "D5:2 F#5:1 A5:3", "B5:4 A5:1 F#5:1",
        "G5:3 F#5:1 E5:2", "D5:2 E5:1 A#4:3", "A4:2 D5:1 F#5:3", "E5:4 R:2"]
AIR2 = ["F#5:3 A5:1 D6:2", "C#6:3 A#5:1 F#5:2", "B5:4 A5:1 F#5:1", "F#5:2 E5:1 D5:3",
        "G5:2 B5:1 D6:3", "D6:2 A#5:1 G5:3", "A5:3 G5:1 E5:2", "D5:6"]
CAIR1 = "D A/C# Bm7 Gmaj7 Em7 Gm6 D/A A7sus4".split()
CAIR2 = "D F#7/A# Bm D/A G Gm6 A7sus4 D".split()
JA = ["A5:2 F#5:1 A5:2 D6:1", "E6:2 C6:1 G5:2 E5:1", "D5:1 G5:1 B5:1 D6:2 B5:1", "A5:2 F#5:1 D5:3",
      "F#5:2 B5:1 D6:2 B5:1", "G5:2 B5:1 D6:1 C#6:1 B5:1", "A5:2 C#6:1 E6:2 C#6:1", "D6:4 A5:1 F#5:1"]
JB = ["B5:2 D6:1 G6:3", "E6:2 C#6:1 A5:3", "C#6:2 A5:1 F#5:2 A5:1", "B5:2 F#5:1 D5:2 F#5:1",
      "G5:2 B5:1 E6:2 D6:1", "C#6:2 E6:1 G6:2 E6:1", "F6:3 D6:1 A#5:2", "A5:2 C#6:1 E6:3"]
CJA = "D C/D G/D D Bm G A D".split()
CJB = "G A F#m Bm Em7 A7 Bb A7".split()
SLOW = ["D6:3 C#6:1 B5:2", "B5:4 D6:2", "A5:3 F#5:1 A5:2", "G5:4 E5:2",
        "A#5:3 A5:1 G5:2", "F#5:4 A5:2", "G#5:3 B5:1 D6:2", "C#6:4 R:2",
        "B5:2 D6:1 F#6:3", "E6:3 D6:1 B5:2", "A5:2 D6:1 F#6:3", "E6:4 D6:2",
        "D6:3 A#5:1 G5:2", "A5:3 F#5:1 D5:2", "E5:2 G#5:1 B5:2 D6:1", "B5:3 D#6:3"]
CSLOW = "Bm G D/F# Em Gm/Bb D/A E7 A7 Bm G D/F# Em Gm/Bb D/A E7 B7".split()
JC = ["E6:2 B5:1 G#5:2 B5:1", "A5:2 F#5:1 D5:2 F#5:1", "E5:1 A5:1 C#6:1 E6:2 C#6:1", "B5:3 G#5:2 E5:1",
      "G#5:2 C#6:1 E6:2 C#6:1", "A5:2 C#6:1 B5:1 A5:1 G#5:1", "F#5:2 B5:1 D#6:2 B5:1", "E6:4 B5:2"]
CJC = "E D/E A/E E C#m A B E".split()
def up2(seq): return " ".join(x if x.startswith("R:") else f"{nm(md(x.split(':')[0]) + 2)}:{x.split(':')[1]}" for x in seq.split())
def upc(ch):   # コード名を全音上げる
    F = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]; PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
    def one(x):
        m = re.match(r"^([A-G])([#b]?)(.*)$", x); r = (PC[m.group(1)] + (1 if m.group(2) == "#" else -1 if m.group(2) == "b" else 0) + 2) % 12
        return F[r] + m.group(3)
    return "/".join(one(x) for x in ch.split("/"))
CODA_C = [upc(c) for c in CAIR1] + "E C#m Am6 E E E".split()
CODA_M = [up2(x) for x in AIR1] + ["G#5:3 F#5:1 E5:2", "E5:2 G#5:1 C#6:3", "C6:3 B5:1 A5:2", "G#5:6", "B5:6", "E6:6"]

# ---------------- 形（区間, 何番目の小節, コード, 旋律の素） ----------------
plan = []
def sec(name, chords, mel=None, key="D"):
    for i, c in enumerate(chords): plan.append(dict(k=name, i=i, ch=c, mel=(mel[i] if mel else None), key=key))
sec("intro", CAIR1)
sec("air1", CAIR1 + CAIR2, AIR1 + AIR2)
sec("air2", CAIR1 + CAIR2, AIR1 + AIR2)
sec("call", "D D C/D D".split())
sec("jig1", CJA + CJA + CJB + CJB, JA + JA + JB + JB)
sec("jig2", CJA + CJA + CJB + CJB, JA + JA + JB + JB)
sec("slow", CSLOW, SLOW)
sec("build", "E E D/E B7".split(), key="E")
sec("jigC", CJC + CJC, JC + JC, key="E")
sec("jigF", [upc(c) for c in CJA + CJA + CJB + CJB], [up2(x) for x in JA + JA + JB + JB], key="E")
sec("coda", CODA_C, CODA_M, key="E")
NB = len(plan)
start = {}
for bi, p in enumerate(plan): start.setdefault(p["k"], bi + 1)
chords = [p["ch"] for p in plan]
S = Song(2, 3, NB, DMAJ); S.G = 0.1

# ---------------- 和音の音 ----------------
PCN = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def pc(s): return (PCN[s[0]] + (1 if len(s) > 1 and s[1] == "#" else -1 if len(s) > 1 and s[1] == "b" else 0)) % 12
def chord_pcs(ch):
    m = re.match(r"^([A-G][#b]?)(.*)$", ch.split("/")[0]); r = pc(m.group(1)); q = m.group(2)
    if "sus4" in q: pcs = [r, (r + 5) % 12, (r + 7) % 12]
    elif "sus2" in q: pcs = [r, (r + 2) % 12, (r + 7) % 12]
    elif q.startswith("m") and not q.startswith("maj"): pcs = [r, (r + 3) % 12, (r + 7) % 12]
    else: pcs = [r, (r + 4) % 12, (r + 7) % 12]
    if "maj7" in q: pcs.append((r + 11) % 12)
    elif "7" in q: pcs.append((r + 10) % 12)
    elif "6" in q: pcs.append((r + 9) % 12)
    return pcs
def bass_pc(ch): return pc(ch.split("/")[1]) if "/" in ch else chord_pcs(ch)[0]
def low(x, lo): return lo + ((x - lo) % 12)
def diat(seq_str, ch, key, k):
    sc = scale_of(ch, key); out = []
    for x in seq_str.split():
        n_, d = x.split(":")
        if n_ == "R": out.append(x); continue
        m = md(n_); dd = 1 if k > 0 else -1
        for _ in range(abs(k)):
            m += dd
            while m % 12 not in sc: m += dd
        out.append(f"{nm(m)}:{d}")
    return " ".join(out)
def octv(seq_str, k): return " ".join(x if x.startswith("R:") else f"{nm(md(x.split(':')[0]) + 12 * k)}:{x.split(':')[1]}" for x in seq_str.split())

# ---------------- パート（チャンネル: 笛・フィドル・アコーディオン・鉄琴・木琴・ハープ・ピアノ・アコギ左・アコギ右・チェロ・ベース・弦上・弦下＝13）----------------
S.part("flute", "panflute", "笛（旋律・ハモり）", 0.21, 0.15, reverb=0.4, gainDb=2, breath=True,
       fx=[{"type": "delay", "beats": 1, "mix": 0.12, "feedback": 0.28}, {"type": "plate", "mix": 0.1}])
# 2026-10-17 人間の指示: フィドルは「柔らかく力強く、透き通るように響かせる」（2本重ね・2.8kHz -2.5dB・芯 +2dB・ホール残響）、アコギはやわらかく（強い弾きなし・高音をおさえる）、
#   音域を広く（ハープの分散和音を広げる）、自然を感じる曲は「その空間が感じられる」ように（全体をホールの残響に入れ、遠い楽器ほど深く）。
S.part("fiddle", "fiddle", "フィドル（旋律）", 0.19, -0.2, patch="violin", reverb=0.5, gainDb=3, bright=-0.15, attack=0.35, release=0.7, doubleDetune={"cents": 5, "spread": 0.3}, fx=[{"type": "eq", "low": 2, "mid": -2.5, "midHz": 2800, "high": 0}, {"type": "delay", "beats": 0.6667, "mix": 0.08, "feedback": 0.2}, {"type": "reverb", "mix": 0.22}, {"type": "plate", "mix": 0.12}])
S.part("acc", "accordion", "アコーディオン", 0.11, 0.3, reverb=0.28, fx=[{"type": "room", "mix": 0.12}])
S.part("glock", "glockenspiel", "鉄琴（星）", 0.07, 0.6, reverb=0.55, sustain=4, release=0.8, fx=[{"type": "pingpong", "beats": 0.6667, "mix": 0.2, "feedback": 0.35}])
S.part("xylo", "xylophone", "木琴（祭りの跳ね回り）", 0.09, -0.4, reverb=0.25, fx=[{"type": "room", "mix": 0.1}])
S.part("harp", "harp", "ハープ（6/8の分散和音）", 0.12, -0.35, reverb=0.38, bright=-0.4, sustain=4, release=0.8,
       fx=[{"type": "delay", "beats": 0.6667, "mix": 0.1, "feedback": 0.2}])
for _k in ("pno1", "pno2", "pno3"):
    S.part(_k, "piano", f"ピアノ右手（和音・{_k[3]}）", 0.09, 0.05, reverb=0.3, sustain=1.5, fx=[{"type": "plate", "mix": 0.15}])
S.part("pnoL", "piano", "ピアノ左手（低音）", 0.12, 0.05, reverb=0.3, sustain=1.4, fx=[{"type": "plate", "mix": 0.15}])
for _k, _pan in (("g1", -0.5), ("g2", 0.5), ("g3", -0.5), ("g4", 0.5)):
    S.part(_k, "guitar", f"アコギ（{_k[1]}本目）", 0.08, _pan, amp="crystal", chorus=0, sustain=1.0, reverb=0.22, autoScoop=False, humanPitch=0, push=0.008 * int(_k[1]), bright=-0.65, attack=0.58, release=0.6, fx=[{"type": "eq", "low": 1, "mid": -1.5, "midHz": 2600, "high": -4.5}, {"type": "compressor", "threshold": -20, "ratio": 2.5, "attack": 0.003, "release": 0.12}])   # 2026-10-17 人間の指示「強くていいけど柔らかい音」: 高音と弾く瞬間を抑え、低めを少し足す
S.part("cello", "strings", "チェロ", 0.13, -0.3, patch="cello", reverb=0.35, release=0.5)
S.part("bass", "bass", "ベース（指弾き）", 0.24, 0, fx=[{"type": "compressor", "threshold": -18, "ratio": 3, "attack": 0.02, "release": 0.15}])
S.part("sth", "strings", "弦（上・のばす）", 0.07, 0.35, patch="slowStrings", reverb=0.4, release=0.6)
S.part("stl", "strings", "弦（下・のばす）", 0.07, 0.35, patch="slowStrings", reverb=0.4, release=0.6)   # 上と同じ設定にしてチャンネルを共有（フィドルの2本重ねで1つ増えたため）
S.part("bodhran", "tom", "ボーラン風の刻み", 0.12, 0.1, reverb=0, gainDb=-8, bright=-0.4)
S.part("kick", "kick", "キック", 0.26, 0, gainDb=-8)
S.part("snare", "snare", "スネア", 0.18, 0, push=0.01, gainDb=-10)
S.part("ride", "crash", "ライド", 0.05, 0.2, gainDb=-9)
S.part("crash", "crash", "クラッシュ", 0.09, 0, gainDb=-8)

GAIN = {"intro": (0.6, 0.72), "air1": (0.74, 0.82), "air2": (0.82, 0.9), "call": (0.86, 0.95), "jig1": (0.9, 0.96), "jig2": (0.97, 1.02),
        "slow": (0.76, 0.86), "build": (0.85, 1.0), "jigC": (1.0, 1.02), "jigF": (1.02, 1.05), "coda": (0.8, 0.62)}
LEN = {}
for p in plan: LEN[p["k"]] = LEN.get(p["k"], 0) + 1
arc = []
def ornament(seq_str, style, seed, dens, legato):
    return S.ornament(S.seq(seq_str), style, seed, dens=dens, legato=legato)

for bi, p in enumerate(plan):
    k, i, ch, mel, key = p["k"], p["i"], p["ch"], p["mel"], p["key"]
    a, z = GAIN[k]; arc.append(round(a + (z - a) * i / max(1, LEN[k] - 1), 3))
    S.scale = scale_of(ch, key)
    pcs = chord_pcs(ch); br = low(bass_pc(ch), 40)
    last8 = i % 8 == 7
    slowk = k in ("intro", "air1", "air2", "slow", "coda")
    # ---- 旋律 ----
    if k == "air1": S.put("flute", bi, ornament(mel, "cut", bi, 0.35, True))
    if k == "air2":
        S.put("fiddle", bi, ornament(mel, "roll", bi, 0.4, True))
        S.put("flute", bi, S.plain(S.seq(diat(mel, ch, key, -2)), legato=True))
    if k == "jig1": S.put("flute", bi, ornament(mel, "cut", bi, 0.55, True))
    if k == "jig2":
        S.put("fiddle", bi, ornament(mel, "roll", bi, 0.5, True))
        S.put("acc", bi, S.plain(S.seq(diat(mel, ch, key, -2) if i < 16 else octv(mel, -1)), legato=True))
    if k == "slow": S.put("fiddle", bi, ornament(mel, "plain", bi, 0, True))
    if k == "build" and i >= 2: S.put("flute", bi, ["B4:" + T3, "D#5:" + T3, "F#5:" + T3, "B5:" + T3, "D#6:" + T3, "F#6:" + T3] if i == 3 else ["E5:1", "B5:1"])
    if k == "jigC":
        S.put("flute", bi, ornament(mel, "cut", bi, 0.5, True))
        S.put("fiddle", bi, S.plain(S.seq(octv(mel, -1)), legato=True))
    if k == "jigF":
        S.put("fiddle", bi, ornament(mel, "roll", bi, 0.5, True))
        S.put("flute", bi, ornament(mel, "cut", bi + 3, 0.4, True))
        S.put("acc", bi, S.plain(S.seq(diat(mel, ch, key, -2)), legato=True))
        if i >= 16: S.put("glock", bi, S.plain(S.seq(octv(mel, 1)), legato=False))
    if k == "coda":
        if i < 8: S.put("flute", bi, ornament(mel, "cut", bi, 0.3, True))
        elif i < 12: S.put("fiddle", bi, S.plain(S.seq(mel), legato=True))
        else: S.put("flute", bi, S.plain(S.seq(mel), legato=True))
    # ---- 鉄琴（星）: ゆっくりの所で、2小節に1回、和音の高い音を2つ ----
    if slowk and k != "air2" and (i % 2 == 1 or k == "intro") and not (k == "coda" and i >= 12):
        t1 = low(pcs[min(2, len(pcs) - 1)], 84); t2 = low(pcs[0], 88)
        S.put("glock", bi, [f"{nm(t1)}:1", f"{nm(t2)}:1"] if (bi % 4 in (0, 1)) else [f"{nm(t2)}:{fmt(2 / 3)}", f"{nm(t1)}:{fmt(4 / 3)}"])
    if k == "coda" and i == 13: S.put("glock", bi, ["E7:2"])
    # ---- 木琴（祭り: ジグ2の B と最後のジグの A で跳ね回る）----
    if (k == "jig2" and i >= 16) or (k == "jigF" and i < 16) or (k == "jigC" and i >= 8) or (k == "call" and i == 3):
        t = sorted(low(x, 72) for x in pcs[:3])
        pat = [t[0], t[1], t[2], t[0] + 12, t[2], t[1]] if i % 2 == 0 else [t[2], t[0] + 12, t[1] + 12, t[0] + 12, t[2], t[1]]
        S.put("xylo", bi, [f"{nm(x)}:{T3}" + ("!" if j in (0, 3) else ",") for j, x in enumerate(pat)])
    # ---- アコーディオン（星空の歌の2回目は和音の3度をのばす。祭りの合図は和音の刻み）----
    if k == "air2": S.put("acc", bi, [f"{nm(low(pcs[1], 57))}:2"])
    if k == "jig1" and i >= 16: S.put("acc", bi, [f"{nm(low(pcs[1], 60))}:{fmt(2 / 3)}", f"R:{T3}", f"{nm(low(pcs[1], 60))}:{fmt(2 / 3)}", f"R:{T3}"])
    if k == "coda" and 8 <= i < 12: S.put("acc", bi, [f"{nm(low(pcs[1], 57))}:2"])
    # ---- ハープ（6/8の分散和音。ゆっくりの所と、ジグ1の A）----
    if slowk:   # ジグでは鳴らさない（速い分散和音で音が切れてプチッと鳴った）
        r = low(pcs[0], 45); t3 = r + ((pcs[1] - pcs[0]) % 12); t5 = r + ((pcs[2] - pcs[0]) % 12)   # 音域を広く: A2 から 3 オクターブ
        S.put("harp", bi, [f"{nm(x)}:{T3}" for x in (r, t5 + 12, r + 24, t3 + 24, t5 + 12, r + 12)])
    # ---- ピアノ（左手と右手）----
    pv = sorted(low(x, 60) for x in pcs[:3]); lr = low(bass_pc(ch), 36)
    if (k == "intro" and i >= 4) or k in ("air1", "air2", "slow", "coda"):
        for vi, g in enumerate(("pno1", "pno2", "pno3")):
            S.put(g, bi, [f"{nm(pv[vi])}:2" + ("," if k in ("intro", "coda") else "")] if k != "slow" else [f"{nm(pv[vi])}:{fmt(4 / 3)}", f"{nm(pv[vi])}:{fmt(2 / 3)},"])
        if k == "intro": pass
        elif k == "slow": S.put("pnoL", bi, [f"{nm(x)}:{T3}" + ("!" if j == 0 else ",") for j, x in enumerate((lr, lr + 7, lr + 12, lr + 16 if (pcs[1] - pcs[0]) % 12 == 4 else lr + 15, lr + 12, lr + 7))])
        else: S.put("pnoL", bi, [f"{nm(lr)}:1", f"{nm(lr + 7)}:1,"] if not (k == "coda" and i >= 12) else [f"{nm(lr)}:2,"])
    if k in ("jig1", "jig2", "jigC", "jigF"):   # 「ずん・ちゃっ」: 左手が1拍目と2拍目の頭、右手の和音が裏（3つ目の8分）
        for vi, g in enumerate(("pno1", "pno2", "pno3")):
            S.put(g, bi, [f"R:{fmt(2 / 3)}", f"{nm(pv[vi])}:{T3},", f"R:{fmt(2 / 3)}", f"{nm(pv[vi])}:{T3},"])
        S.put("pnoL", bi, [f"{nm(lr)}:{fmt(2 / 3)}!", f"R:{T3}", f"{nm(lr + 7 if i % 2 == 0 else lr + 12)}:{fmt(2 / 3)}", f"R:{T3}"])
    # ---- アコギ（6/8の刻み: 低い2本はのばし、高い2本は「ダウン2/3・アップ1/3」）----
    if k in ("air2",) or (k == "call" and i >= 2) or k in ("jig1", "jig2", "build", "jigC", "jigF") or (k == "slow" and i >= 8):
        g0 = low(pcs[0], 45)
        v = [low(bass_pc(ch), 40), g0 + ((pcs[2] - pcs[0]) % 12), g0 + 12, g0 + 12 + ((pcs[1] - pcs[0]) % 12)]
        for gi, g in enumerate(("g1", "g2", "g3", "g4")):
            if gi < 2 or k in ("air2", "slow"): S.put(g, bi, [f"{nm(v[gi])}:2" + ("" if not slowk else ",")]); continue
            S.put(g, bi, [f"{nm(v[gi])}:{fmt(2 / 3)}", f"{nm(v[gi])}:{T3},", f"{nm(v[gi])}:{fmt(2 / 3)}", f"{nm(v[gi])}:{T3},"])
    # ---- 低音: チェロ（ゆっくりの所）とベース（ジグ）----
    if slowk and not (k == "intro" and i < 4):
        S.put("cello", bi, [f"{nm(low(bass_pc(ch), 43) + (12 if k == 'slow' else 0))}:2"])
    if k in ("jig1", "jig2", "build", "jigC", "jigF") or (k == "call" and i >= 2):
        nx = chords[bi + 1] if bi + 1 < NB else ch; rn = low(bass_pc(nx), 28); r = low(bass_pc(ch), 28)
        ap = (rn - 1 if rn > r else rn + 1) if rn != r else r + 7
        S.put("bass", bi, [f"{nm(r)}:1", f"{nm(r)}:1,"] if k != "build" else [f"{nm(r)}:2"])   # 根音だけ（2026-10-17 人間の指示）
    # ---- 弦（のばす）----
    if (k == "intro" and i >= 4) or k in ("air1", "air2", "slow", "jig2", "jigF", "coda", "build") or (k == "jigC" and i >= 8):
        S.put("sth", bi, [f"{nm(low(pcs[1], 66))}:2"]); S.put("stl", bi, [f"{nm(low(pcs[2], 57))}:2"])
    # ---- 打楽器 ----
    BOD = {"X": "A2!", "x": "C3", "o": "C3,,"}
    if k == "call":
        S.put("bodhran", bi, S.pgrid(["X.....", "X..x.o", "X.ox.o", "XxoXxX"][i], BOD))
        if i == 3: S.put("snare", bi, S.grid("..ooxX"))
    if k in ("jig1", "jig2", "jigC", "jigF"):
        S.put("bodhran", bi, S.pgrid("X.ox.o" if not last8 else "XxoXxX", BOD))
        if k != "jig1" or i >= 16: S.put("kick", bi, S.grid("X..x.." if k != "jig1" else "X....."))
        if k in ("jig2", "jigC", "jigF"):
            if last8: S.put("snare", bi, S.grid("..ooxX"))
            else: S.put("snare", bi, S.grid("...x.." if i % 2 == 0 else "...x.o"))
        if (k == "jig2" and i >= 16) or (k == "jigF" and i >= 16): S.put("ride", bi, ["D2:" + T3] * 6)
        if i % 8 == 0 and (k != "jig1" or i in (0, 16)): S.put("crash", bi, S.grid("X....."))
    if k == "build":
        S.put("bodhran", bi, S.pgrid(["X..x..", "X.xX.x", "XxxXxx", "XxXXxX"][i], BOD))
        S.put("snare", bi, S.grid(["......", "...x.x", "x.xx.x", "ooxxXX"][i]))
    if k == "slow" and i == 0: S.put("crash", bi, S.grid("x....."))
    if k == "coda" and i == 0: S.put("crash", bi, S.grid("X....."))

TEMPO = [{"bar": start["call"], "bpm": 112}, {"bar": start["slow"] - 2, "bpm": 60, "ramp": 2},
         {"bar": start["build"], "bpm": 116, "ramp": 4}, {"bar": start["coda"] - 2, "bpm": 52, "ramp": 2}]
out = sys.argv[1] if len(sys.argv) > 1 else "assets-src/ai-songs/celtic-summer-night.json"
S.dump(out, "星降る夏祭りの夜（仮）",
       "（仮）夏祭りの夜、透き通った空の星。しんみりするような、楽しいような、思い出になるようなケルト音楽。6/8、テンポが動く（ゆっくりの歌 52 → 祭りのジグ 112 → 思い出の歌 60 → 最後のジグ 116 → 星の終わり 52）。"
       "ニ長調 → 最後のジグで全音上のホ長調。約4分45秒。星空の歌（笛→フィドル）→ ボーランの合図 → 祭りのジグ（笛、アコギの刻み、ピアノの「ずん・ちゃっ」）→ "
       "フィドルとアコーディオンのジグ（木琴が跳ね回り、B♭ の花火）→ 思い出の歌 → ホ長調の新しい旋律と最後のジグ（鉄琴が旋律の上）→ 星空の歌でゆっくり終わる。"
       "ピアノは左手の低音と右手の和音。FX: 笛のディレイ、鉄琴のピンポンディレイ、ハープのディレイ、フィドルのプレート、アコギとベースのコンプ。"
       "進行: Gm6（マイナーの iv）、F#7/A#（III7）、C/D（ミクソリディアン）、B♭（♭VI）、E7（V/V）、最後は Am6 を通って E。入り方: 2（ハープと鉄琴だけ）。終わり方: 余韻を残して消える。",
       52, chords, arc, extra={"guitarWobble": False, "tempo": TEMPO})

# ---- 仕上げ: のばす楽器の「同じ高さの音の弾き直し」をつなぐ（弾き直すと前の音が切れてプチッと鳴る。『霧の森の予兆』で確かめた）----
import json as _json
def _merge(notes, legato):
    out = []
    for t in notes.split():
        n_, d = t.split(":", 1); mark = "".join(c for c in d if not (c.isdigit() or c == ".")); dv = float(d[:len(d) - len(mark)])
        if out and n_ != "R" and out[-1][0] == n_ and dv >= 1 and out[-1][1] >= 1 and "!" not in mark:
            out[-1][1] += dv; out[-1][2] = out[-1][2].replace("_", ""); continue
        out.append([n_, dv, mark.replace("_", "") if legato else mark])
    res = []
    for j, (n_, dv, mark) in enumerate(out):
        nxt = out[j + 1][0] if j + 1 < len(out) else "R"
        lg = "_" if legato and n_ != "R" and nxt not in ("R", n_) and dv >= 1 else ""
        res.append(f"{n_}:{fmt(dv)}{mark}{lg}")
    return " ".join(res)
_song = _json.load(open(out, encoding="utf-8"))
for _p in _song["parts"]:
    r = _p["role"]
    if r.startswith(("弦（", "チェロ", "アコーディオン")): _p["notes"] = _merge(_p["notes"], legato=r.startswith(("弦（", "チェロ")))
_json.dump(_song, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
