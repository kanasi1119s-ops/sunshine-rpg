# ラウドメタル・ラウドロック25曲（第2シリーズ）の共通部品。設計表は docs/sound/lm25-plan.md
# 土台は「白い分岐点」（loud25_02_bunkiten.py。人間「完成度は素晴らしかった」）の音作り:
#   ドラム Naked Drums の素直な版（--drums naked）・ベース bnb-loud の指弾き＋bassSplit・ギター distGuitar の明るい歪み＋透明感の層・
#   リード namJVM＋Greenback＋ピンポン＋プレート（ビブラートなし・チョーキングは保つ）。
# 曲のファイルは、この部品で「小節ごとの音」を作り、Song にパートを足して JSON に書き出す。
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
PC = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8,
      "A": 9, "A#": 10, "Bb": 10, "B": 11, "Cb": 11, "E#": 5, "B#": 0}
SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
FLAT = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
REST = "R"
MARKS = "!,'^/\\_~u()@>"


# ---------------- 音の高さ ----------------
def midi(n):
    """音名（C#4 など）→ MIDI 番号"""
    m = re.match(r"^([A-G][#b]?)(-?\d+)$", n)
    assert m, n
    return PC[m.group(1)] + 12 * (int(m.group(2)) + 1)


def nm(m, flat=False):
    """MIDI 番号 → 音名"""
    return (FLAT if flat else SHARP)[m % 12] + str(m // 12 - 1)


def tr(n, semi, flat=None):
    """音名を半音で動かす（flat を省くと元の書き方に合わせる）"""
    if flat is None: flat = "b" in n[1:2]
    return nm(midi(n) + semi, flat)


def up(n, octs):
    return tr(n, 12 * octs)


# ---------------- 拍と小節 ----------------
def tok_beats(t):
    """「音名:拍」の拍（奏法の記号を除く）"""
    v = t.split(":", 1)[1]
    v = re.split(r"[!,'^/\\_~u(@>]", v)[0]
    return float(v)


def tok_note(t):
    return t.split(":", 1)[0]


def tok_marks(t):
    v = t.split(":", 1)[1]
    m = re.match(r"^[0-9.]+", v)
    return v[m.end():]


def total(s):
    return sum(tok_beats(t) for t in s.split())


class Bars:
    """拍子（1小節の拍）を覚えておき、1小節ぶんの音を確かめて返す"""
    def __init__(self, beats):
        self.beats = beats

    def __call__(self, *toks):
        t = " ".join(toks).split()
        s = sum(tok_beats(x) for x in t)
        assert abs(s - self.beats) < 1e-3, ("小節の拍が合わない", toks, s, self.beats)
        return " ".join(t)

    def rest(self):
        return f"R:{self.beats:g}"


def shift_oct(s, octs):
    """音の列をまとめてオクターブ移動（休みはそのまま）"""
    return " ".join(t if t.startswith("R") else up(tok_note(t), octs) + ":" + t.split(":", 1)[1] for t in s.split())


def transpose(s, semi):
    return " ".join(t if t.startswith("R") else tr(tok_note(t), semi) + ":" + t.split(":", 1)[1] for t in s.split())


def strip_marks(s, keep="!"):
    out = []
    for t in s.split():
        n, v = t.split(":", 1)
        b = re.match(r"^[0-9.]+", v).group(0)
        rest = "".join(c for c in v[len(b):] if c in keep)
        out.append(f"{n}:{b}{rest}")
    return " ".join(out)


# ---------------- 和音 ----------------
QUAL = {
    "": [0, 4, 7], "m": [0, 3, 7], "5": [0, 7], "7": [0, 4, 7, 10], "maj7": [0, 4, 7, 11], "m7": [0, 3, 7, 10],
    "m9": [0, 3, 7, 10, 2], "9": [0, 4, 7, 10, 2], "maj9": [0, 4, 7, 11, 2], "add9": [0, 4, 7, 2], "madd9": [0, 3, 7, 2],
    "sus4": [0, 5, 7], "sus2": [0, 2, 7], "7sus4": [0, 5, 7, 10], "m7b5": [0, 3, 6, 10], "dim": [0, 3, 6], "dim7": [0, 3, 6, 9],
    "6": [0, 4, 7, 9], "m6": [0, 3, 7, 9], "aug": [0, 4, 8], "7b9": [0, 4, 7, 10, 1], "m11": [0, 3, 7, 10, 2, 5],
    "maj7#11": [0, 4, 7, 11, 6], "mmaj7": [0, 3, 7, 11], "13": [0, 4, 7, 10, 2, 9], "7#9": [0, 4, 7, 10, 3], "b5": [0, 6],
}


def parse_chord(ch):
    """'F#m7/C#' → (根音の音名, 種類, ベースの音名)"""
    base = None
    if "/" in ch: ch, base = ch.split("/")
    m = re.match(r"^([A-G][#b]?)(.*)$", ch)
    assert m, ch
    q = m.group(2)
    assert q in QUAL, ("和音の種類が分からない", ch)
    return m.group(1), q, base or m.group(1)


def tr_chord(ch, semi):
    """和音の名前を半音で動かす（シャープで書く）"""
    def one(x):
        m = re.match(r"^([A-G][#b]?)(.*)$", x)
        return SHARP[(PC[m.group(1)] + semi) % 12] + m.group(2)
    if "/" in ch:
        a, b = ch.split("/")
        return one(a) + "/" + SHARP[(PC[b] + semi) % 12]
    return one(ch)


def chord_pcs(ch):
    r, q, b = parse_chord(ch)
    s = {(PC[r] + i) % 12 for i in QUAL[q]}
    s.add(PC[b] % 12)
    return s


def chord_tones(ch, lo, hi, flat=None):
    """和音の音を lo〜hi（音名）の範囲で低い順に"""
    r, q, b = parse_chord(ch)
    if flat is None: flat = "b" in r
    pcs = chord_pcs(ch)
    return [nm(m, flat) for m in range(midi(lo), midi(hi) + 1) if m % 12 in pcs]


def root_note(ch, lo="E1", hi="D#2"):
    """和音の根音（スラッシュならベースの音）を lo〜hi のオクターブで"""
    r, q, b = parse_chord(ch)
    for m in range(midi(lo), midi(hi) + 1):
        if m % 12 == PC[b] % 12: return nm(m, "b" in b)
    raise ValueError(ch)


def fifth_of(ch, lo="E1", hi="D#2"):
    r, q, b = parse_chord(ch)
    iv = 6 if q in ("m7b5", "dim", "dim7", "b5") else 7
    pc = (PC[r] + iv) % 12
    for m in range(midi(lo), midi(hi) + 13):
        if m % 12 == pc and m >= midi(root_note(ch, lo, hi)): return nm(m, "b" in r)
    raise ValueError(ch)


# ---------------- 音階 ----------------
MODES = {
    "ionian": [0, 2, 4, 5, 7, 9, 11], "dorian": [0, 2, 3, 5, 7, 9, 10], "phrygian": [0, 1, 3, 5, 7, 8, 10],
    "lydian": [0, 2, 4, 6, 7, 9, 11], "mixolydian": [0, 2, 4, 5, 7, 9, 10], "aeolian": [0, 2, 3, 5, 7, 8, 10],
    "locrian": [0, 1, 3, 5, 6, 8, 10], "harmonic": [0, 2, 3, 5, 7, 8, 11], "phrygdom": [0, 1, 4, 5, 7, 8, 10],
    "melodic": [0, 2, 3, 5, 7, 9, 11],
}


def scale_notes(tonic, mode, lo, hi, flat=None):
    if flat is None: flat = "b" in tonic
    pcs = {(PC[tonic] + i) % 12 for i in MODES[mode]}
    return [nm(m, flat) for m in range(midi(lo), midi(hi) + 1) if m % 12 in pcs]


# ---------------- ギターの技 ----------------
def sweep(ch, lo, hi, beats_len=2, step=None, down=True, accent=True):
    """スウィープ（和音の音を1本ずつ上がって、てっぺんから下りる）。step は1音の長さ（既定は 6連＝1/6拍）"""
    t = chord_tones(ch, lo, hi)
    seq = t + (t[-2::-1] if down else [])
    step = step or (1 / 6 if beats_len * 6 >= len(seq) else 0.25)
    n = int(round(beats_len / step))
    out = []
    for i in range(n):
        note = seq[i % len(seq)]
        last = i == n - 1
        mark = "!" if (accent and (i % len(seq) == 0)) else ""
        out.append(f"{note}:{step:.4f}{mark}{'' if last else '_'}")
    return fix_len(" ".join(out), beats_len)


def tap(tri, beats_len=2, step=1 / 6, pattern=(2, 1, 0, 1)):
    """タッピング（右手で高い音をたたき、左手の2音へ引っかける）。tri は低い順の3音（音名）。6連か16分でくり返す"""
    n = int(round(beats_len / step))
    out = []
    for i in range(n):
        j = pattern[i % len(pattern)]
        mark = "!" if j == 2 else ""
        out.append(f"{tri[j]}:{step:.4f}{mark}{'' if i == n - 1 else '_'}")
    return fix_len(" ".join(out), beats_len)


def legato_run(tonic, mode, start, end, beats_len=1, step=0.25):
    """音階の上り・下り（ハンマリング・プルオフでつなぐ）"""
    sc = scale_notes(tonic, mode, "E2", "E7")
    i0, i1 = sc.index(start), sc.index(end)
    seq = sc[i0:i1 + 1] if i1 >= i0 else sc[i1:i0 + 1][::-1]
    n = int(round(beats_len / step))
    seq = (seq * (n // len(seq) + 1))[:n] if len(seq) < n else seq[:n]
    out = [f"{x}:{step:.4f}{'!' if k == 0 else ''}{'' if k == len(seq) - 1 else '_'}" for k, x in enumerate(seq)]
    return fix_len(" ".join(out), beats_len)


def fix_len(s, want):
    """浮動小数の端数を最後の音で合わせる"""
    toks = s.split()
    have = sum(tok_beats(t) for t in toks)
    d = want - have
    if abs(d) > 1e-9:
        n, v = toks[-1].split(":", 1)
        b = re.match(r"^[0-9.]+", v).group(0)
        toks[-1] = f"{n}:{float(b) + d:.4f}{v[len(b):]}"
    return " ".join(toks)


# ---------------- ベースの型 ----------------
def approach_note(ch, nxt, lo="E1", hi="D#2"):
    """次の根音へ近づく音（今の和音と半音でぶつからないものを、半音下・半音上・全音上・全音下・5度の順に）"""
    r = root_note(ch, lo, hi)
    nr = root_note(nxt, lo, hi)
    if nr == r: return fifth_of(ch, lo, hi)
    pcs = chord_pcs(ch)

    def rough(n):
        m = midi(n) % 12
        return m not in pcs and any((m - q) % 12 in (1, 11) for q in pcs)
    for c in (tr(nr, -1), tr(nr, 1), tr(nr, 2), tr(nr, -2), fifth_of(ch, lo, hi)):
        if not rough(c) and c != nr: return c
    return fifth_of(ch, lo, hi)


def bass_root8(ch, beats, nxt=None, accent=(0,), approach=True, lo="E1", hi="D#2"):
    """コードに沿う8分（根音にアクセント・最後の8分で次の根音へ近づく）"""
    r = root_note(ch, lo, hi)
    n = int(beats * 2)
    toks = [f"{r}:0.5{'!' if i * 0.5 in accent or (i * 0.5) % 2 == 0 else ''}" for i in range(n)]
    if approach and nxt:
        nr = root_note(nxt, lo, hi)
        if nr != r:
            toks[-1] = f"{approach_note(ch, nxt, lo, hi)}:0.5"
    return " ".join(toks)


def bass_walk(ch, nxt, beats, lo="E1", hi="D#2", swing_feel=True):
    """ジャズのウォーキング（1拍1音: 根音→和音の音→5度→次の根音へ半音で近づく）。1音ずつはっきり"""
    r = root_note(ch, lo, hi)
    tones = chord_tones(ch, r, up(r, 1))
    third = tones[1] if len(tones) > 1 else r
    fifth = fifth_of(ch, lo, hi)
    nr = root_note(nxt, lo, hi) if nxt else r
    pcs = chord_pcs(ch)
    def rough(n):   # 今の和音の音と半音でぶつかる（自分は和音の外）
        m = midi(n) % 12
        return m not in pcs and any((m - q) % 12 in (1, 11) for q in pcs)
    cands = [tr(nr, -1) if midi(nr) > midi(fifth) else tr(nr, 1), tr(nr, 1) if midi(nr) > midi(fifth) else tr(nr, -1),
             tr(nr, -2), tr(nr, 2), fifth]
    ap = next((c for c in cands if not rough(c) and c != r), fifth)
    seq = [r, third, fifth, ap]
    if beats == 3: seq = [r, fifth, ap]
    elif beats > 4: seq = [r, third, fifth] + [tones[min(3, len(tones) - 1)] if len(tones) > 3 else up(r, 1)] * (beats - 4) + [ap]
    return " ".join(f"{x}:1{'!' if i == 0 else ''}" for i, x in enumerate(seq[:beats]))


def bass_slap_bar(ch, beats, pattern, lo="E1", hi="D#2"):
    """スラップ風（親指＝根音の強い音 T、はじく＝オクターブ上の短い音 P、ゴースト＝休み g、5度 F、♭7 S）。
    pattern は 16分の文字列（T・P・F・S・g・.）。g は bassMute のパートに出すので、ここでは休み。
    戻り値: (ベースの音, 止めた音〔ゴースト〕の音)"""
    r = root_note(ch, lo, hi)
    f5 = fifth_of(ch, lo, hi)
    r8 = up(r, 1)
    rr, q, b = parse_chord(ch)
    s7 = tr(r8, -2 if q not in ("maj7", "maj9", "") else -1)
    assert len(pattern) == beats * 4, pattern
    main, mute = [], []
    for c in pattern:
        if c == "T": main.append(f"{r}:0.25!"); mute.append("R:0.25")
        elif c == "P": main.append(f"{r8}:0.25'"); mute.append("R:0.25")
        elif c == "F": main.append(f"{f5}:0.25"); mute.append("R:0.25")
        elif c == "S": main.append(f"{s7}:0.25'"); mute.append("R:0.25")
        elif c == "g": main.append("R:0.25"); mute.append(f"{r}:0.25,")
        else: main.append("R:0.25"); mute.append("R:0.25")
    return merge_rests(" ".join(main)), merge_rests(" ".join(mute))


def merge_rests(s):
    out = []
    for t in s.split():
        if t.startswith("R:") and out and out[-1].startswith("R:"):
            out[-1] = f"R:{tok_beats(out[-1]) + tok_beats(t):g}"
        else:
            out.append(t)
    return " ".join(out)


def unison_low(s, octs=-1, lo="B0"):
    """リフをベースへ（1オクターブ下。低すぎる音はそのまま）"""
    out = []
    for t in s.split():
        if t.startswith("R"): out.append(t); continue
        n = tok_note(t)
        n2 = up(n, octs)
        if midi(n2) < midi(lo): n2 = n
        out.append(n2 + ":" + t.split(":", 1)[1])
    return " ".join(out)


# ---------------- ドラム ----------------
class Kit:
    """ドラムを小節ごとに積む（キック・スネア・ハイハットは16分のグリッド、タムとシンバルは音符）"""
    def __init__(self, beats):
        self.beats = beats
        self.n = beats * 4
        self.K, self.S, self.H, self.T, self.C, self.FX = [], [], [], [], [], []

    def grid(self, pos=(), ch="X", base=None):
        r = list(base or "." * self.n)
        for p in pos: r[int(p) % self.n] = ch
        return "".join(r)

    def add(self, k=None, s=None, h=None, tom=None, cym=None, fx=None):
        b = self.beats
        k = k or "." * self.n; s = s or "." * self.n; h = h or "." * self.n
        for g in (k, s, h): assert len(g) == self.n, ("ドラムの文字数", g, self.n)
        tom = tom or f"R:{b:g}"; cym = cym or f"R:{b:g}"; fx = fx or f"R:{b:g}"
        for x in (tom, cym, fx): assert abs(total(x) - b) < 1e-3, ("ドラムの拍", x, b)
        # クラッシュ・チャイナを叩く瞬間は、右手でハイハットを叩けない
        hits = cym_hit_positions(cym)
        h = "".join("." if (i in hits and c != ".") else c for i, c in enumerate(h))
        self.K.append(k); self.S.append(s); self.H.append(h); self.T.append(tom); self.C.append(cym); self.FX.append(fx)


def cym_hit_positions(cym):
    pos, t = set(), 0.0
    for x in cym.split():
        if not x.startswith("R") and tok_note(x) in ("C2", "G2", "B2", "B3", "A2", "A3"):
            pos.add(int(round(t * 4)))
        t += tok_beats(x)
    return pos


TOMS = ["C4", "A3", "F3", "D3", "A2"]   # 高い→フロア（白い分岐点と同じ）


def tom_triplets_down(beats_len=2, start_rest=0):
    """3連16分でタムを下る（最後はフロアの強打）"""
    n = int(round(beats_len * 6))
    seq = []
    per = max(1, n // len(TOMS))
    for i in range(n):
        seq.append(TOMS[min(len(TOMS) - 1, i // per)])
    out = [f"{x}:{1 / 6:.4f}{'!' if i == n - 1 or i % per == 0 else ''}" for i, x in enumerate(seq)]
    s = fix_len(" ".join(out), beats_len)
    return (f"R:{start_rest:g} " + s) if start_rest else s


def tom_16_down(beats_len=1, start_rest=0):
    n = int(round(beats_len * 4))
    seq = [TOMS[min(len(TOMS) - 1, i * len(TOMS) // n)] for i in range(n)]
    s = " ".join(f"{x}:0.25{'!' if i in (0, n - 1) else ''}" for i, x in enumerate(seq))
    return (f"R:{start_rest:g} " + s) if start_rest else s


def linear_fill(kit, beats_len=2, seed=0):
    """リニアのフィル（手と足が重ならない）。最後の beats_len 拍に、キック・スネア・タムを1つずつ順番に置く。
    戻り値: (キックのグリッド, スネアのグリッド, タムの音符)"""
    n = kit.n
    L = int(beats_len * 4)
    start = n - L
    pats = ["KSTSKTST", "SSKTTKSK", "KTSKTSKS", "TSKTTSKT"]
    p = pats[seed % len(pats)]
    k = ["."] * n; s = ["."] * n
    tom_toks, last_t = [], 0.0
    ti = 0
    for j in range(L):
        c = p[j % len(p)]
        pos = start + j
        if c == "K": k[pos] = "X" if j == L - 1 else "x"
        elif c == "S": s[pos] = "X" if j in (0, L - 1) else ("o" if j % 3 == 1 else "x")
        else:
            t0 = pos / 4
            if t0 > last_t: tom_toks.append(f"R:{t0 - last_t:g}")
            tom_toks.append(f"{TOMS[min(4, ti)]}:0.25{'!' if j == L - 1 else ''}")
            ti += 1
            last_t = t0 + 0.25
    if kit.beats - last_t > 1e-9: tom_toks.append(f"R:{kit.beats - last_t:g}")
    return "".join(k), "".join(s), " ".join(tom_toks) if tom_toks else f"R:{kit.beats:g}"


# ---------------- パート（音作り） ----------------
LEAD_BASE = {"instrument": "distGuitar", "double": False, "noRestrike": True, "phrase": 8, "humanPitch": 0, "noScoop": True, "di": "emily", "chorus": 0,
             "amp": "namJVM", "ampDrive": 0.69, "ampGate": 10, "ampTight": 0.6, "ampTightHz": 150, "ampCabIr": "jd-greenback-4x12-01", "reverb": 0.12,
             "fx": [{"type": "eq", "low": -2, "mid": 2.5, "midHz": 1200, "high": 2}, {"type": "filter", "kind": "lowpass", "freq": 10000, "q": 0.7},
                    {"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.25}, {"type": "plate", "mix": 0.16}], "powerChord": False, "autoScoop": False}

DRUM_SET = {p["instrument"]: {k: v for k, v in p.items() if k not in ("notes", "role", "instrument")}
            for p in json.load(open(os.path.join(HERE, "..", "drum-refs", "prog100-naked.json")))["parts"]}


def part(role, inst, notes, **kw):
    d = {"role": role, "instrument": inst, "notes": notes}
    d.update(kw)
    if d.get("phrase", 1) is None: d.pop("phrase")
    return d


def riff_parts(notes, vol=0.11, drive=0.44, clear=True, clear_vol=0.07):
    """看板リフ（明るい歪み）＋透明感の層（浅い歪み）"""
    ps = [part("看板リフ", "distGuitar", notes, volume=vol, pan=0, guitarTone="loud-mid", gainDb=-3, powerChord=False, sustain=1.4, release=0.5, ampDrive=drive,
               fx=[{"type": "filter", "kind": "highpass", "freq": 85, "q": 0.7}, {"type": "eq", "low": 0, "mid": -5, "midHz": 320, "high": 0},
                   {"type": "eq", "low": 0, "mid": 2.5, "midHz": 1500, "high": 0}, {"type": "eq", "low": 0, "mid": 2, "midHz": 3500, "high": 4}, {"type": "plate", "mix": 0.08}])]
    if clear:
        ps.append(part("看板リフ（透明感の層）", "distGuitar", notes, **{**LEAD_BASE, "volume": clear_vol, "pan": 0, "ampDrive": 0.18, "phrase": None, "reverb": 0.1, "sustain": 1.4, "release": 0.5,
                       "fx": [{"type": "filter", "kind": "highpass", "freq": 140, "q": 0.7}, {"type": "eq", "low": -3, "mid": -3, "midHz": 400, "high": 3}, {"type": "plate", "mix": 0.12}]}))
    return ps


def rhythm_parts(outer, inner, drive=0.44):
    eq = [{"type": "eq", "low": 0, "mid": -3.5, "midHz": 300, "high": 0}, {"type": "eq", "low": 0, "mid": 2.5, "midHz": 1500, "high": 0}, {"type": "eq", "low": 0, "mid": 2, "midHz": 3200, "high": 3}]
    return [part("リズム（左右）", "distGuitar", outer, volume=0.1, pan=0, guitarTone="loud-mid", gainDb=-5, sustain=1.4, release=0.5, ampDrive=drive, fx=eq),
            part("リズム（内側の2本）", "distGuitar", inner, volume=0.1, pan=0, guitarTone="loud-mid-hs", gainDb=-10, sustain=1.4, release=0.5, ampDrive=drive, fx=eq)]


def arp_part(notes, vol=0.1, pan=-0.2, drive=0.34, role="分散和音のギター"):
    return part(role, "distGuitar", notes, **{**LEAD_BASE, "volume": vol, "pan": pan, "ampDrive": drive, "phrase": None, "sustain": 1.6, "release": 0.6,
                "fx": [{"type": "eq", "low": -3, "mid": 1.5, "midHz": 1000, "high": 1.5}, {"type": "filter", "kind": "lowpass", "freq": 9500, "q": 0.7},
                       {"type": "delay", "beats": 0.75, "mix": 0.22, "feedback": 0.35}, {"type": "plate", "mix": 0.24}]})


def clean_part(notes, vol=0.1, pan=0.2, role="クリーンの分散和音"):
    """歪みなしのクリーン（コーラスなし。人間「きゅいんきゅいん」は嫌い）"""
    return part(role, "distGuitar", notes, **{**LEAD_BASE, "volume": vol, "pan": pan, "ampDrive": 0.05, "phrase": None, "sustain": 1.8, "release": 0.8,
                "fx": [{"type": "eq", "low": -4, "mid": -1, "midHz": 500, "high": 2}, {"type": "filter", "kind": "lowpass", "freq": 9000, "q": 0.7},
                       {"type": "delay", "beats": 0.75, "mix": 0.24, "feedback": 0.35}, {"type": "plate", "mix": 0.3}]})


def lead_part(notes, vol=0.13, pan=-0.05, role="リード（旋律）", drive=0.69, delay_beats=0.75):
    fx = [dict(f) for f in LEAD_BASE["fx"]]
    fx[2]["beats"] = delay_beats
    return part(role, "distGuitar", notes, **{**LEAD_BASE, "volume": vol, "pan": pan, "ampDrive": drive, "fx": fx})


def tech_part(notes, vol=0.11, pan=0.1, role="技のギター（速弾き）"):
    """スウィープ・タッピング・レガート用（粒が見えるように中域を出し、ディレイは薄く）"""
    return part(role, "distGuitar", notes, **{**LEAD_BASE, "volume": vol, "pan": pan, "ampDrive": 0.6, "phrase": None, "sustain": 1.0, "release": 0.25,
                "fx": [{"type": "eq", "low": -3, "mid": 3, "midHz": 1400, "high": 1.5}, {"type": "filter", "kind": "lowpass", "freq": 9500, "q": 0.7},
                       {"type": "pingpong", "beats": 0.5, "mix": 0.1, "feedback": 0.15}, {"type": "plate", "mix": 0.12}]})


def bass_part(notes, vol=0.15, role="ベース", bright=0.0):
    return part(role, "bass", notes, volume=vol, pan=0, amp="bassSplit", ampDrive=0.6, duck=0.2,
                fx=[{"type": "eq", "low": 0, "mid": 3, "midHz": 2200, "high": 2 + bright}])


def slap_pop_part(notes, vol=0.12, role="ベース（はじく音）"):
    """スラップのはじく音（同じ bnb の指弾きの録音を、高域を出して短く。親指の音はふつうのベースのパートで）"""
    return part(role, "bass", notes, volume=vol, pan=0, amp="bassSplit", ampDrive=0.5, sustain=0.9, release=0.28,
                fx=[{"type": "filter", "kind": "highpass", "freq": 120, "q": 0.7}, {"type": "eq", "low": -4, "mid": 4, "midHz": 2500, "high": 6},
                    {"type": "compressor", "threshold": -18, "ratio": 4, "attack": 0.002, "release": 0.08}])


def bassmute_part(notes, vol=0.2, role="ベース（止めた音・ゴースト）"):
    return part(role, "bass", notes, volume=vol, pan=0, patch="bassMute", amp="bassSplit", ampDrive=0.5,
                fx=[{"type": "eq", "low": 0, "mid": 3, "midHz": 2200, "high": 2}])


LAST_KIT = []


def drum_parts(kit):
    LAST_KIT[:] = [kit]
    return [part("キック", "kick", "g:" + "".join(kit.K), **DRUM_SET["kick"]),
            part("スネア", "snare", "g:" + "".join(kit.S), **DRUM_SET["snare"]),
            part("ハイハット", "hihat", "g:" + "".join(kit.H), **DRUM_SET["hihat"]),
            part("タム", "tom", " ".join(kit.T), **DRUM_SET["tom"]),
            part("シンバル", "crash", " ".join(kit.C), **DRUM_SET["crash"])]


def cymfx_part(notes, vol=0.06):
    """本物のシンバルの効果音（C＝逆再生クラッシュ・E＝スウェル。音符の終わりに山）"""
    return part("シンバルの効果音", "guitar", notes, patch="cymbalFx", volume=vol, pan=0, modulate=False)   # 音名で種類を選ぶので転調させない


def gfx_part(notes, vol=0.06, role="ギターの効果音"):
    """ピックスクレイプ・ハーモニクスなど（EG-IPT の DI を歪ませて）"""
    return part(role, "distGuitar", notes, patch="guitarFx", volume=vol, pan=0, amp="namJVM", ampDrive=0.5, ampCabIr="jd-greenback-4x12-01",
                fx=[{"type": "plate", "mix": 0.2}])


# ---------------- 曲 ----------------
SIMPLE = {"maj7#11": "maj7", "7b9": "7", "m11": "m7", "7#9": "7", "b5": "5", "mmaj7": "m", "13": "9", "dim7": "dim"}


def simple_chord(ch):
    """作曲ソフトの和音の欄が読める書き方に（細かい種類を近いものへ）"""
    base = ch.split("/")
    r, q, b = parse_chord(ch)
    q2 = SIMPLE.get(q, q)
    return r + q2 + ("/" + base[1] if len(base) > 1 else "")


def _tok_starts(cym):
    out, t = [], 0.0
    for x in cym.split():
        out.append((t, x)); t += tok_beats(x)
    return out


def humanize_drums(kit, secs, kinds, seed=0, beats=4):
    """人が叩いたような強弱（2026-10-23、人間「人間っぽさ」「強弱・アクセント・ゴースト」「単調にしない」）。
    区間の種類で強さを変え、ハイハットは小節ごとに強弱の型を変え、スネアの間にゴーストを足し、フィルはだんだん強く。
    プログレの要素として、ブリッジ・ソロの一部の小節ではハイハットのアクセントを3つおき（4拍子の上に3のまとまり）にする。"""
    import random
    n = kit.n
    kindof = lambda nm_: kinds.get(nm_) or re.sub(r"\d+$", "", nm_)
    LEVEL = {"intro": 0, "verse": 0, "interlude": 1, "inter": 1, "pre": 1, "bridge": 1, "solo": 2, "chorus": 2, "break": 0, "outro": 1}
    for b, (sec, i) in enumerate(secs):
        rng = random.Random(seed * 1000 + b)
        kd = kindof(sec)
        lv = LEVEL.get(kd, 1)
        k, s, h = list(kit.K[b]), list(kit.S[b]), list(kit.H[b])
        tom_busy = [False] * n
        for t0, x in _tok_starts(kit.T[b]):
            if not x.startswith("R"): tom_busy[min(n - 1, int(round(t0 * 4)))] = True
        is_fill = any(tom_busy)
        cyms = _tok_starts(kit.C[b])
        cym_at = [False] * n
        ride_bar = False
        for t0, x in cyms:
            if not x.startswith("R"):
                cym_at[min(n - 1, int(round(t0 * 4)))] = True
                if tok_note(x) in ("D2", "F2"): ride_bar = True
        # キック: 拍の頭は強く、裏は少し弱く（連打の X/x はそのまま）
        hits_k = [j for j, c in enumerate(k) if c != "."]
        if len(hits_k) < 10:
            for j in hits_k:
                if k[j] in "Xx": k[j] = "X" if (j % 4 == 0 or j == 0) else "x"
        # ハイハット: 小節ごとに型を変える
        hh = [j for j, c in enumerate(h) if c in "xX"]
        if hh:
            three = kd in ("bridge", "solo") and len(hh) >= 6 and rng.random() < 0.35
            style = rng.choice(["down", "down", "push"] if lv == 2 else ["down", "soft"])
            for j in hh:
                if three: h[j] = "X" if (j % 12) % 3 == 0 and j % 2 == 0 or j % 6 == 0 else "x"
                elif j % 4 == 0: h[j] = "X" if (lv == 2 or j == 0 or style == "down") else "x"
                elif j % 2 == 0: h[j] = "X" if style == "push" else ("x" if lv >= 1 or style == "down" else "o")
                else: h[j] = "o"
            # 区間の4小節目の終わりでオープン
            last8 = n - 2
            if i % 4 == 3 and h[last8] != "." and not is_fill and rng.random() < 0.6: h[last8] = "O"
        # スネアのゴースト
        backs = [j for j, c in enumerate(s) if c == "X"]
        if backs and not is_fill and (hh or ride_bar) and kd not in ("break", "intro"):
            want = {0: 2, 1: 2, 2: 1}[lv] + (1 if rng.random() < 0.4 else 0)
            if len(hits_k) >= 10: want = 1
            want = max(0, want - sum(1 for c in s if c == "o"))
            cand = []
            for j in range(n):
                if s[j] != "." or cym_at[j] or tom_busy[j]: continue
                if h[j] in "xXoO" and cym_at[j]: continue
                if any(abs(j - q) == 1 and s[q] == "X" and j > q for q in backs): continue   # バックビートの直後は空ける
                w = 3 if any(q - j == 1 for q in backs) else (2 if j % 4 == 3 else (1 if j % 4 == 1 else 0))
                if w: cand += [j] * w
            got = set()
            while cand and len(got) < want:
                j = rng.choice(cand); got.add(j); cand = [c for c in cand if c != j]
            for j in got: s[j] = "o"
        # フィル（スネアの連打）はだんだん強く
        roll = [j for j, c in enumerate(s) if c != "." and j >= n // 2]
        adj = sum(1 for a_, b_ in zip(roll, roll[1:]) if b_ - a_ == 1)
        if len(roll) >= 4 and adj >= 2:
            for r_, j in enumerate(roll): s[j] = "o" if r_ < len(roll) // 3 else ("x" if r_ < len(roll) - 2 else "X")
        # ライドの裏は弱く
        new = []
        for t0, x in cyms:
            if not x.startswith("R") and tok_note(x) == "D2" and abs(t0 - round(t0)) > 1e-6 and "!" not in x and "," not in x: x = x + ","
            new.append(x)
        kit.K[b], kit.S[b], kit.H[b], kit.C[b] = "".join(k), "".join(s), "".join(h), " ".join(new)


def onsets(notes):
    out, t = [], 0.0
    for x in notes.split():
        if not x.startswith("R"): out.append(round(t, 4))
        t += tok_beats(x)
    return out


def let_ring(notes, maxlen=0.75, short=0.5, drop_staccato=False, stops=()):
    """短い音（short 拍以下）のあとの休みを、maxlen 拍まで音の伸びにする（2026-10-23、人間「スラップ・ミュートはもう少し音を伸ばす」）。
    stops（ほかのパートの音の出だし）の手前で止める（1本のベースなので重ねない）"""
    import bisect
    st = sorted(set(stops))
    toks = notes.split()
    out = []
    j = 0; t = 0.0
    while j < len(toks):
        x = toks[j]
        if not x.startswith("R") and tok_beats(x) <= short + 1e-9 and j + 1 < len(toks) and toks[j + 1].startswith("R"):
            d = tok_beats(x); r = tok_beats(toks[j + 1])
            k = bisect.bisect_right(st, round(t + 1e-6, 4))
            room = (st[k] - t) if k < len(st) else 1e9
            add = max(0.0, min(r, maxlen - d, room - d))
            t += d + r
            marks = tok_marks(x).replace("'", "") if drop_staccato else tok_marks(x)
            out.append(f"{tok_note(x)}:{d + add:g}{marks}")
            if r - add > 1e-9: out.append(f"R:{r - add:g}")
            j += 2
            continue
        out.append(x); t += tok_beats(x); j += 1
    return " ".join(out)


_TPL = re.compile(r"^[A-G][#b]?-?\d$")


def vary_pickups(notes, styles, beats):
    """「8分休み＋8分3つの上り＋2拍の長い音」（どの曲にも出てしまう型）を、曲ごとに決めた別のリズムへ置きかえる
    （2026-10-23、人間「曲調は似ないように」「単調にならないように」）。音の高さはそのまま。styles は小節番号でかわるがわる使う"""
    toks = notes.split()
    out, t, j = [], 0.0, 0
    while j < len(toks):
        x = toks[j]
        at_bar = abs(t / beats - round(t / beats)) < 1e-6
        win = toks[j:j + 5]
        if at_bar and len(win) == 5 and win[0] == "R:0.5" and all(tok_beats(y) == 0.5 and _TPL.match(tok_note(y)) for y in win[1:4]) \
                and tok_beats(win[4]) == 2 and _TPL.match(tok_note(win[4])):
            st = styles[int(round(t / beats)) % len(styles)]
            a_, b_, c_, d_ = win[1:5]
            na, nb, nc = (tok_note(y) for y in (a_, b_, c_))
            ma, mb, mc = (tok_marks(y) for y in (a_, b_, c_))
            rep = {"V0": win,
                   "V1": [f"{na}:1{ma}", f"{nb}:0.5{mb}", f"{nc}:0.5{mc}", d_],
                   "V2": ["R:0.25", f"{na}:0.25{ma}", f"{nb}:0.5{mb}", f"{nc}:1{mc}", d_],
                   "V3": [f"{na}:0.75{ma}", f"{nb}:0.75{mb}", f"{nc}:0.5{mc}", d_],
                   "V4": ["R:1", f"{nb}:0.5{mb}", f"{nc}:0.5{mc}", d_],
                   "V5": [f"{na}:0.5{ma}", "R:0.5", f"{nb}:0.5{mb}", f"{nc}:0.5{mc}", d_]}[st]
            out += rep; t += 4 * 0 + sum(tok_beats(y) for y in win); j += 5
            continue
        out.append(x); t += tok_beats(x); j += 1
    return " ".join(out)


def _events_full(notes):
    """(開始拍, 長さ, 音名 or None, 記号, 元の字句)"""
    out, t = [], 0.0
    for x in notes.split():
        L = tok_beats(x)
        out.append((t, L, None if x.startswith("R") else tok_note(x), "" if x.startswith("R") else tok_marks(x), x))
        t += L
    return out


def _join(evs):
    return " ".join(f"R:{L:g}" if n is None else f"{n}:{L:g}{m}" for _, L, n, m, _x in evs)


BMTH_EQ = [{"type": "filter", "kind": "highpass", "freq": 60.0, "q": 0.7}, {"type": "eq", "low": 0, "mid": 11.21, "midHz": 258.5, "high": 0}, {"type": "eq", "low": 0, "mid": -14.94, "midHz": 491.0, "high": 0}, {"type": "eq", "low": 0, "mid": 5.35, "midHz": 2500.0, "high": 0}, {"type": "eq", "low": 0, "mid": -14.95, "midHz": 4353.8, "high": 0}, {"type": "filter", "kind": "lowpass", "freq": 11989.0, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 11989.0, "q": 0.7}]
GUITAR_REF_EQ = {"bmth": BMTH_EQ}   # 参考の曲を測って計算した EQ（曲ごとに選ぶ）


def modernize_leads(song):
    """現代ラウドの決まりごと（docs/sound/modern-loud-rock/、2026-10-23 人間「ゲームの音っぽい」「音が高すぎる」）を、全曲のギターに当てる:
    1. リードの高さ: 区間ごとに、音の真ん中を歌の高さ（サビ B4・Aメロ G4・ほか A4）に近づける（1オクターブ下げるかどうか。一番上は A5 まで。ソロはそのまま）
    2. ハモリ: 1オクターブ下の重ねをやめ、和音の音から3度上あたりを選ぶ。サビの2回目以降の、区間の後半だけ
    3. 最後のサビだけ、1オクターブ上を薄く（帯域を絞って）重ねる
    4. 表情: フレーズの最初の長い音にすべり込み（/）、近い音へ動く短い音はレガート（_）でつなぐ
    5. リフ: 低いチューニング（ドロップC〜7弦・8弦の F#）の音域へ。区間の一番低い音が F2 以上なら、F#1 を下回らない範囲で1オクターブ下げる"""
    B = song.beats
    kindof = lambda n: song.kinds.get(n) or re.sub(r"\d+$", "", n).replace("inter", "interlude")
    secs, t = [], 0
    for n, c in song.form:
        secs.append((n, kindof(n), t * B, (t + c) * B)); t += c
    def sec_at(x):
        for sc in secs:
            if sc[2] - 1e-6 <= x < sc[3] - 1e-6: return sc
        return secs[-1]
    lead = next((p for p in song.parts if p["role"] == "リード（旋律）"), None)
    if not lead: return
    ev = _events_full(lead["notes"])
    shift = {}
    for sc in secs:
        ms = [midi(n) for st, L, n, m, x in ev if n and sc[2] - 1e-6 <= st < sc[3] - 1e-6]
        if not ms or sc[1] == "solo": shift[sc[0]] = 0; continue
        # 区間の音の真ん中を、歌の高さの目安へ（サビ B4・Aメロ G4・ほか A4）。一番上が A5 を超えるなら必ず下げる
        med = sorted(ms)[len(ms) // 2]
        tgt = {"chorus": midi("B4"), "verse": midi("G4")}.get(sc[1], midi("A4"))
        best = min((0, -12), key=lambda d: (max(ms) + d > midi("A5"), min(ms) + d < midi("E3"), abs(med + d - tgt)))
        shift[sc[0]] = best
    ev = [(st, L, (nm(midi(n) - 0 + shift[sec_at(st)[0]], "b" in n[1:2]) if n else None), m, x) for st, L, n, m, x in ev]
    # 表情
    out = []
    for i, (st, L, n, m, x) in enumerate(ev):
        if n:
            prev = ev[i - 1] if i else None
            nxt = ev[i + 1] if i + 1 < len(ev) else None
            if ">" in m or "(" in m or "@" in m: pass
            elif L >= 1 and (prev is None or prev[2] is None) and not re.search(r"[/^\\~_]", m): m = m + "/"
            elif L <= 0.5 and nxt and nxt[2] and abs(midi(nxt[2]) - midi(n)) <= 2 and "_" not in m and "'" not in m and nxt[0] - (st + L) < 1e-6: m = m + "_"
        out.append((st, L, n, m, x))
    lead["notes"] = _join(out)
    ev = out
    # ハモリ
    chorus_no = {}
    k = 0
    for sc in secs:
        if sc[1] == "chorus": k += 1; chorus_no[sc[0]] = k
    def harm_note(n, st):
        bar = min(int(st // B), song.nb - 1)
        pcs = chord_pcs(song.chord_at(bar))
        m0 = midi(n)
        for d in (3, 4, 5, 2, 6, 7):
            if (m0 + d) % 12 in pcs: return nm(m0 + d, "b" in n[1:2])
        return None
    for p in song.parts:
        if p["role"] in ("リード（オクターブ下）", "リード（和音の音のハモリ）"):
            hv = []
            for st, L, n, m, x in ev:
                sc = sec_at(st)
                use = n and sc[1] == "chorus" and chorus_no.get(sc[0], 1) >= 2 and st >= (sc[2] + sc[3]) / 2 - 1e-6
                h = harm_note(n, st) if use else None
                hv.append((st, L, h, m.replace("/", "") if h else "", x))
            p["notes"] = _join(hv)
            p["role"] = "リード（3度上のハモリ）"
            p["volume"] = round(lead.get("volume", 0.13) * 0.62, 3)
    last = [sc for sc in secs if sc[1] == "chorus"]
    if last:
        sc = last[-1]
        ov = [(st, L, (nm(midi(n) + 12) if n and sc[2] - 1e-6 <= st < sc[3] - 1e-6 and midi(n) + 12 <= midi("E6") else None), "", x) for st, L, n, m, x in ev]
        if any(n for _, _, n, _, _ in ov):
            q = dict(lead); q["role"] = "リード（最後のサビの1オクターブ上）"; q["notes"] = _join(ov); q["volume"] = round(lead.get("volume", 0.13) * 0.35, 3)
            q["fx"] = [{"type": "filter", "kind": "highpass", "freq": 1500, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 9000, "q": 0.7}] + [f for f in lead.get("fx", []) if f.get("type") == "room"]
            q.pop("double", None)
            song.parts.append(q)
    # 空気の層（2026-10-23 聞き比べ G を人間が採用）: サビ・Bメロ・ブリッジの後ろに、きれいな音の分散和音（根音・5度・9度・3度）を薄く。
    #   この層だけ、付点8分のやまびこと長めの残響を付ける（リードには付けない）
    amb, t = [], 0.0
    for sc in secs:
        bars = int(round((sc[3] - sc[2]) / B))
        for i in range(bars):
            bar_i = int(round(sc[2] / B)) + i
            if sc[1] not in ("chorus", "pre", "bridge") or bar_i >= song.nb:
                amb.append(f"R:{B:g}"); continue
            r, q, _b = parse_chord(song.chord_at(bar_i))
            root = next(m for m in range(midi("E3"), midi("E4")) if m % 12 == PC[r] % 12)
            fifth = 6 if q in ("dim", "dim7", "m7b5", "b5") else 7
            third = None if (q.startswith("sus") or q == "5") else (3 if (q.startswith("m") and not q.startswith("maj")) or q in ("dim", "dim7", "m7b5") else 4)
            ninth = None if q in ("dim", "dim7", "7b9") else 14
            voic = [root, root + fifth, root + (ninth or 12), root + 12 + (third if third is not None else fifth)]
            order = (0, 1, 2, 3, 2, 1)
            n8 = int(round(B * 2))
            amb.append(" ".join(f"{nm(voic[order[j % len(order)]], 'b' in r)}:0.5" for j in range(n8)) + (f" R:{B - n8 * 0.5:g}" if B - n8 * 0.5 > 1e-6 else ""))
    if any(not x.startswith("R") for x in " ".join(amb).split()):
        song.parts.append({"role": "きれいな音の分散和音（空気の層）", "instrument": "distGuitar", "notes": " ".join(amb), "volume": 0.055, "pan": 0.35,
                           "di": "emily", "amp": "namJVM", "ampDrive": 0.05, "ampCabIr": "jd-greenback-4x12-01", "noRestrike": True, "humanPitch": 0,
                           "noScoop": True, "chorus": 0, "sustain": 2.0, "release": 0.9, "attack": 0.5,
                           "fx": [{"type": "eq", "low": -4, "mid": -1, "midHz": 500, "high": 2}, {"type": "delay", "beats": 0.75, "mix": 0.25, "feedback": 0.35}, {"type": "reverb", "mix": 0.4}]})
    # ギターの帯域を BMTH の数値へ（2026-10-23 聞き比べ H を人間が採用「Hいいね」）。参考の曲と聞き比べ G のギターを音源分離して
    #   1/3オクターブごとに測り（/tmp/ref/analyze.py・fit.py）、差を埋める EQ を計算した: 低い中域を太く・箱っぽい中域と耳に刺さる帯域を深く削る。
    #   リフとリズムは左右いっぱいの別テイク（参考は左右の相関 -0.17 と広い）
    #   2026-10-23 人間「いいね＝25曲の基本の音ではない」→ 曲ごとに song.guitar_ref = "bmth" のように選んだ曲だけに当てる（既定は当てない＝聞き比べ G の音）
    ref_eq = GUITAR_REF_EQ.get(getattr(song, "guitar_ref", None) or "")
    for p in (song.parts if ref_eq else []):
        if p["instrument"] == "distGuitar" and p.get("patch") not in ("cymbalFx", "guitarFx") and "空気の層" not in p["role"]:
            p["fx"] = [dict(f) for f in ref_eq] + [f for f in p.get("fx", []) if f.get("type") == "room"]
            if p["role"].startswith("看板リフ"): p["double"] = {"spread": 1.0}
            elif p["role"].startswith("リズム"):
                p["double"] = {"spread": 1.0, "irR": "jd-greenback-4x12-01", **({"diR": "fsbs"} if p.get("guitarTone") == "loud-mid-hs" else {})}
    # リフを低いチューニングへ
    for p in song.parts:
        if p["role"] in ("看板リフ", "看板リフ（透明感の層）"):
            evr = _events_full(p["notes"])
            for sc in secs:
                ms = [midi(n) for st, L, n, m, x in evr if n and sc[2] - 1e-6 <= st < sc[3] - 1e-6]
                if ms and min(ms) >= midi("F2") and min(ms) - 12 >= midi("F#1"):
                    evr = [(st, L, (nm(midi(n) - 12, "b" in n[1:2]) if n and sc[2] - 1e-6 <= st < sc[3] - 1e-6 else n), m, x) for st, L, n, m, x in evr]
            p["notes"] = _join(evr)


class Song:
    def __init__(self, title, desc, bpm, beats, form, chords):
        """form: [(区間の名前, 小節数)]。chords: 区間の名前 → 小節ごとの和音のリスト"""
        self.title, self.desc, self.bpm, self.beats = title, desc, bpm, beats
        self.form = form
        self.chords = chords
        self.secs = [(n, i) for n, c in form for i in range(c)]
        for n, c in form: assert len(chords[n]) == c, ("和音の数", n, len(chords[n]), c)
        self.nb = len(self.secs)
        self.parts = []
        self.extra = {}
        self.flags = ""
        self.kinds = {}      # 区間の名前 → 作曲ソフトの区間の種類（intro・verse・pre・chorus・interlude・bridge・break・outro・solo）      # 書き出しに足す引数（例 "--space hall --space-wet 0.18"）。<json>.flags に書く

    def chord_at(self, idx):
        n, i = self.secs[idx]
        return self.chords[n][i]

    def add(self, *ps):
        for p in ps:
            if isinstance(p, list): self.parts += p
            else: self.parts.append(p)

    def check_lengths(self):
        want = self.nb * self.beats
        for p in self.parts:
            s = p["notes"]
            tot = (len(s) - 2) / 4 if s.startswith("g:") else total(s)
            assert abs(tot - want) < 0.05, ("パートの長さ", p["role"], tot, want)

    def to_json(self):
        self.check_lengths()
        if any(p["role"] == "ベース（はじく音）" for p in self.parts):
            bp = [p for p in self.parts if p["role"] in ("ベース", "ベース（はじく音）", "ベース（止めた音・ゴースト）")]
            on = {id(p): onsets(p["notes"]) for p in bp}
            for p in bp:
                others = [o for q in bp if q is not p for o in on[id(q)]]
                if p["role"] == "ベース（はじく音）": p["notes"] = let_ring(p["notes"], 0.75, 0.25, True, others)
                elif p["role"] == "ベース（止めた音・ゴースト）": p["notes"] = let_ring(p["notes"], 0.5, 0.25, False, others)
                else: p["notes"] = let_ring(p["notes"], 0.75, 0.25, False, others)
        # ギターの響かせ方（ディレイ・ピンポン・深い残響）は「ゲームっぽい」ので外す（2026-10-23、人間「ギターの響かせ方がゲームに近いから取っ払おう」）。
        # 残響はごく薄く（0.35倍）だけ残し、その場で鳴っている乾いた音にする
        for p in self.parts:
            if p["instrument"] in ("distGuitar", "guitar", "leadGuitar", "crunch", "echoGuitar") and p.get("patch") not in ("cymbalFx", "guitarFx"):
                fx = [dict(f) for f in p.get("fx", []) if f.get("type") not in ("delay", "pingpong")]
                for f in fx:
                    if f.get("type") in ("plate", "reverb"): f["mix"] = round(f["mix"] * 0.35, 3)
                # 厚みは「やまびこ」ではなく、小さな部屋の鳴り（ルーム）と、リードの重ね録り（左右に2回弾いたように）で出す
                lead = p["role"].startswith("リード（旋律）") or p["role"].startswith("技のギター")
                fx.append({"type": "room", "mix": 0.12 if lead else 0.08})
                p["fx"] = fx
                if "reverb" in p: p["reverb"] = round(p["reverb"] * 0.35, 3)
                if p["role"].startswith("リード（旋律）"): p["double"] = {"spread": 0.4}
        if getattr(self, "pickups", None):
            for p in self.parts:
                if p["instrument"] not in ("kick", "snare", "hihat", "tom", "crash") and not p["notes"].startswith("g:"):
                    p["notes"] = vary_pickups(p["notes"], self.pickups, self.beats)
        if not self.extra.get("_noModern"): modernize_leads(self)
        if LAST_KIT and not self.extra.get("_noHumanDrums"):
            kit = LAST_KIT[0]
            humanize_drums(kit, self.secs, self.kinds, seed=sum(map(ord, self.title)), beats=self.beats)
            names = {"kick": "K", "snare": "S", "hihat": "H"}
            for p in self.parts:
                if p["instrument"] in names: p["notes"] = "g:" + "".join(getattr(kit, names[p["instrument"]]))
                elif p["instrument"] == "crash" and p["role"] == "シンバル": p["notes"] = " ".join(kit.C)
            LAST_KIT.clear()
        kind = lambda n: re.sub(r"\d+$", "", n).replace("inter", "interlude").replace("breakdown", "break")
        KINDS = {"intro", "verse", "pre", "chorus", "interlude", "bridge", "break", "outro", "solo"}
        song = {"title": self.title, "description": self.desc, "bpm": self.bpm, "beats": self.beats, "barsPerChord": 1, "repeats": 1,
                "autoAccompaniment": False, "feel": "rock", "tone": "metal", "dynamics": "natural",
                "human": 0.42, "humanProfile": "role", "humanDist": "triangle", "diGuitar": "emily", "autoScoop": False, "guitarWobble": False,
                "drumMix": {"kick": {"level": 1.0}, "crash": {"level": 0.9}, "snare": {"level": 1.0}},
                "chords": " ".join(simple_chord(self.chord_at(i)) for i in range(self.nb)),
                "sections": [{"kind": self.kinds.get(n) or (kind(n) if kind(n) in KINDS else "verse"), "bars": c} for n, c in self.form],
                "parts": self.parts}
        song.update(self.extra)
        return song

    def write(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        json.dump(self.to_json(), open(path, "w"), ensure_ascii=False)
        open(path + ".flags", "w").write(self.flags)
        sec = self.nb * self.beats * 60 / self.bpm
        print(f"{self.title}: {self.nb}小節・{int(sec // 60)}分{int(sec % 60):02d}秒 → {path}")


# ---------------- 点検（不協和音） ----------------
def events(s, beats_per_bar):
    t = 0.0
    for x in s.split():
        b = tok_beats(x)
        if not x.startswith("R"):
            yield t, b, midi(tok_note(x))
        t += b


def check_clash(song, roles=None, min_len=1.0, verbose=True):
    """長い音（min_len 拍以上）が、その時の和音の音・音階に入っているか。
    和音の外の長い音と、ほかのパートの長い音との短2度・長7度・短9度のぶつかりを数える"""
    B = song.beats
    long_notes = []
    for p in song.parts:
        if p["instrument"] in ("kick", "snare", "hihat", "tom", "crash") or p.get("patch") in ("cymbalFx", "guitarFx", "bassMute"): continue
        if roles and p["role"] not in roles: continue
        for t, b, m in events(p["notes"], B):
            if b >= min_len - 1e-6: long_notes.append((t, t + b, m, p["role"]))
    outside, clash = [], []

    def ok_at(m, t):
        bar = min(int(t // B), song.nb - 1)
        ch = song.chord_at(bar)
        ext = chord_pcs(ch) | {(PC[parse_chord(ch)[0]] + i) % 12 for i in (2, 9)}   # 9度・13度は許す
        return m % 12 in ext, ch

    for t0, t1, m, r in long_notes:
        ok, ch = ok_at(m, t0)
        if not ok and (t1 - t0) > 1.0 + 1e-6: outside.append((int(t0 // B) + 1, nm(m), ch, r))
    for i, a in enumerate(long_notes):
        for b_ in long_notes[i + 1:]:
            if a[3] == b_[3]: continue
            ov = min(a[1], b_[1]) - max(a[0], b_[0])
            if ov >= 0.5:
                iv = abs(a[2] - b_[2]) % 12
                t = max(a[0], b_[0])
                if iv in (1, 11) and not (ok_at(a[2], t)[0] and ok_at(b_[2], t)[0]):
                    clash.append((int(t // B) + 1, nm(a[2]), a[3], nm(b_[2]), b_[3]))
    if verbose:
        print(f"和音の外の長い音: {len(outside)}  ぶつかり（短2度・長7度）: {len(clash)}")
        for x in outside[:12]: print("  外:", x)
        for x in clash[:12]: print("  ぶつかり:", x)
    return outside, clash
