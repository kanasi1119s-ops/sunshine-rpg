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
    return part(role, "bass", notes, volume=vol, pan=0, amp="bassSplit", ampDrive=0.5, sustain=0.5, release=0.12,
                fx=[{"type": "filter", "kind": "highpass", "freq": 120, "q": 0.7}, {"type": "eq", "low": -4, "mid": 4, "midHz": 2500, "high": 6},
                    {"type": "compressor", "threshold": -18, "ratio": 4, "attack": 0.002, "release": 0.08}])


def bassmute_part(notes, vol=0.2, role="ベース（止めた音・ゴースト）"):
    return part(role, "bass", notes, volume=vol, pan=0, patch="bassMute", amp="bassSplit", ampDrive=0.5,
                fx=[{"type": "eq", "low": 0, "mid": 3, "midHz": 2200, "high": 2}])


def drum_parts(kit):
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
        kind = lambda n: re.sub(r"\d+$", "", n).replace("inter", "interlude").replace("breakdown", "break")
        KINDS = {"intro", "verse", "pre", "chorus", "interlude", "bridge", "break", "outro", "solo"}
        song = {"title": self.title, "description": self.desc, "bpm": self.bpm, "beats": self.beats, "barsPerChord": 1, "repeats": 1,
                "autoAccompaniment": False, "feel": "rock", "tone": "metal", "dynamics": "natural",
                "human": 0.35, "humanProfile": "role", "humanDist": "triangle", "diGuitar": "emily", "autoScoop": False, "guitarWobble": False,
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
