# ギターとベースのフレーズのライブラリ（2026-10-22 人間「ギターとベースも1000通りぐらいおねがいしたい」）
# ライブラリ: assets-src/guitar-phrases/phrases.json・assets-src/bass-phrases/phrases.json（度数＝根音からの半音で書いた型）
# 説明: docs/sound/guitar-bass-phrase-library.md
#
# 使い方（曲のファイルから）:
#   from loud25_phrases import pick, render, pick_pair
#   g = pick("guitar", role="リフ", section="看板リフ", energy=0.7, fits="m", bars=2, seed=3)
#   notes = render(g, ["Dm", "Bb"], key="D", mode="aeolian", low="D2")   # → "D2:0.25' D2:0.25' ..."（put() にそのまま渡せる）
#   pair = pick_pair("サビ", ["Bb", "C", "Dm", "Dm"], key="D", mode="aeolian", energy=0.8, low="D2", seed=1)
#   put(gtr, a, a + 16, pair["guitar"]["notes"]); put(bass, a, a + 16, pair["bass"]["notes"])
#
# 型の書き方（ev の1つ＝[始まり, 長さ, 音, 印]。時間は「刻み」＝1拍の12分の1。1小節＝48）:
#   音は「根音からの半音の数」の並び（和音なら複数）。根音は、その小節の和音の根音を ref（ギターは low＝いちばん低い弦）以上でいちばん低い所に置いた音。
#   rel が "first" の型は、1小節目の根音を基準にしたまま（ペダル）。ベースの "N"・"N-1"・"N+1"・"N-2"・"N+2"・"N-5" は次の小節の根音（への近づき）。"x" はデッドノート。
#   印は作曲ソフトの記号そのまま（! 強く・, 弱く・,, もっと弱く・' 短く・_ つなぐ・^^ 全音のチョーキング・//@0.1 下からすべって入る・>+2 音の中で2半音すべる）。
#   決まりごと（banned-sounds・人間の好み）: ~（ビブラート）は使わない。リードに / （しゃくり）は使わない。
import json, os, random, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
LIB_PATHS = {"guitar": os.path.join(ROOT, "assets-src", "guitar-phrases", "phrases.json"),
             "bass": os.path.join(ROOT, "assets-src", "bass-phrases", "phrases.json")}

TPB = 12            # 1拍の刻み
BAR = 48            # 4/4 の1小節
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
FLAT = {"Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#", "Bb": "A#", "Cb": "B", "Fb": "E"}
MODES = {
    "aeolian": [0, 2, 3, 5, 7, 8, 10], "phrygian": [0, 1, 3, 5, 7, 8, 10], "dorian": [0, 2, 3, 5, 7, 9, 10],
    "harmonic": [0, 2, 3, 5, 7, 8, 11], "ionian": [0, 2, 4, 5, 7, 9, 11], "lydian": [0, 2, 4, 6, 7, 9, 11],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10], "phrygdom": [0, 1, 4, 5, 7, 8, 10], "minpent": [0, 3, 5, 7, 10], "majpent": [0, 2, 4, 7, 9],
    "blues": [0, 3, 5, 6, 7, 10],
}
RANGE = {"guitar": (29, 88), "bass": (23, 55)}   # ギター F1〜E6・ベース B0〜G3

# 和音の種類 → 型の「合う和音」の分類（m 短三和音・M 長三和音・5 パワーコード・sus・7 属七・m7・maj7・dim）
QCLASS = [("m7b5", "dim"), ("dim", "dim"), ("maj7", "maj7"), ("madd9", "m"), ("m9", "m7"), ("m7", "m7"), ("m6", "m"), ("m", "m"),
          ("add9", "M"), ("sus2", "sus"), ("sus4", "sus"), ("7sus4", "sus"), ("sus", "sus"), ("9", "7"), ("7", "7"), ("6", "M"), ("5", "5"), ("", "M")]
COMPAT = {  # 和音の分類 → 使える型の fits（その和音の上で鳴らしてよい型）。短調の型は長三和音に、長調の型は短三和音に使わない
    "m": ("m", "m7"), "m7": ("m7", "m"), "M": ("M", "maj7"), "maj7": ("maj7", "M"), "7": ("7",),
    "5": ("5",), "sus": ("sus",), "dim": ("dim",),
}

def midi(n):
    p, o = (n[:2], n[2:]) if len(n) > 2 and n[1] in "#b" else (n[:1], n[1:])
    p = FLAT.get(p, p)
    return NAMES.index(p) + (int(o) + 1) * 12
def name(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"
def at_least(pc, low):
    return low + ((pc - low) % 12)

# ── 和音の読み取り ──
class Ch:
    def __init__(self, root, cls, sym=""):
        self.root, self.cls, self.sym = root % 12, cls, sym
    def __repr__(self): return f"Ch({NAMES[self.root]}{self.cls})"

def parse_chord(c, key=None, mode=None):
    """"Dm"・"Bb"・"F#5"・"Csus2"・"Ebmaj7"、整数（根音の 0〜11。パワーコード扱い）、loud25_lib の Chord、
    key と mode があれば度数の記号（"1m"・"b6"・"4sus4"）も読む"""
    if isinstance(c, Ch): return c
    if isinstance(c, int): return Ch(c, "5", str(c))
    if hasattr(c, "root") and hasattr(c, "iv"):   # loud25_lib.Chord
        iv = set(c.iv)
        cls = "dim" if 6 in iv and 7 not in iv else ("sus" if not ({3, 4} & iv) and ({2, 5} & iv) else
              ("5" if iv <= {0, 7, 12} else ("m7" if {3, 10} <= iv else "m" if 3 in iv else "maj7" if 11 in iv else "7" if 10 in iv else "M")))
        return Ch(c.root, cls, getattr(c, "sym", ""))
    s = str(c).split("/")[0]
    if s and (s[0].isdigit() or (s[0] in "b#" and len(s) > 1 and s[1].isdigit())):
        from loud25_lib import Chord
        return parse_chord(Chord(s, NAMES.index(FLAT.get(key, key)), mode or "aeolian"))
    m = re.match(r"^([A-G][#b]?)(.*)$", s)
    if not m: raise ValueError(f"和音が読めません: {c}")
    root = NAMES.index(FLAT.get(m.group(1), m.group(1)))
    q = m.group(2)
    for pre, cls in QCLASS:
        if q.startswith(pre) if pre else q == "":
            return Ch(root, cls, s)
    return Ch(root, "M", s)

def chord_pcs(ch):
    base = {"m": [0, 3, 7], "m7": [0, 3, 7, 10], "M": [0, 4, 7], "maj7": [0, 4, 7, 11], "7": [0, 4, 7, 10], "5": [0, 7], "sus": [0, 2, 5, 7], "dim": [0, 3, 6]}[ch.cls]
    return {(ch.root + x) % 12 for x in base}

# ── 型 → 音の並び ──
def _fmt(x):
    v = round(x, 6)
    return f"{v:g}" if abs(v - round(v, 2)) < 1e-9 else f"{v:.6f}".rstrip("0")

def _resolve(iv, root_m, next_root_pc, ref):
    if isinstance(iv, int): return root_m + iv
    if iv == "x": return None
    m = re.match(r"^N([+-]\d+)?$", iv)
    if m:
        nr = at_least(next_root_pc, ref)
        return nr + int(m.group(1) or 0)
    raise ValueError(iv)

def _snap(m, scale_pcs, chord_pc, prev):
    """曲の音階にも和音にもない音を、となりの音階の音へ（前の音から進んできた向きを優先）"""
    if scale_pcs is None or m % 12 in scale_pcs or m % 12 in chord_pc: return m
    up, dn = m + 1, m - 1
    ok_up, ok_dn = up % 12 in scale_pcs, dn % 12 in scale_pcs
    if ok_up and ok_dn: return up if (prev is not None and m > prev) else dn
    return up if ok_up else dn if ok_dn else m

def ref_of(ph, low):
    r = ph.get("ref", "low")
    return midi(low) if r == "low" else midi(r)

def render_voices(ph, chords, key=None, mode=None, low="E2", bars=None, snap=True):
    """型を音の並びにする。和音（複数の音）の型は、低い順に声部（パート1本ずつ）に分けて返す（list[str]）"""
    nb = bars or max(ph["bars"], len(chords) if isinstance(chords, (list, tuple)) else 1)
    chs = [parse_chord(c, key, mode) for c in (chords if isinstance(chords, (list, tuple)) else [chords])]
    chs = [chs[i % len(chs)] for i in range(nb + 1)]   # 最後の1つは「次の和音」（近づきの音に使う）
    ref = ref_of(ph, low)
    scale_pcs = None
    if snap and key is not None and mode is not None:
        k = NAMES.index(FLAT.get(key, key)); scale_pcs = {(k + x) % 12 for x in MODES[mode]}
    plen = ph["bars"] * BAR
    nvo = max((len(e[2]) for e in ph["ev"]), default=1)
    voices = [[] for _ in range(nvo)]   # [(start, dur, midi|None, mk)]
    reps = -(-nb * BAR // plen)
    prev = None
    for r in range(reps):
        for t, d, ivs, mk in ph["ev"]:
            T = r * plen + t
            if T >= nb * BAR: continue
            D = min(d, nb * BAR - T)
            bi = T // BAR
            base_bar = (r * ph["bars"]) if ph.get("rel") == "first" else bi
            ch = chs[min(base_bar, nb - 1)]
            nxt = chs[min(bi + 1, nb)]
            root_m = at_least(ch.root, ref)
            cp = chord_pcs(ch)
            ms = []
            cur_cp = chord_pcs(chs[min(bi, nb - 1)])   # その小節で実際に鳴っている和音
            if len(ivs) > 1 and all(isinstance(x, int) for x in ivs):
                # 和音（パワーコード・オクターブ）は形をくずさない: いちばん低い音だけ音階に合わせ、ほかは同じだけずらす
                lo_m = root_m + ivs[0]
                m0 = _snap(lo_m, scale_pcs, cp, prev) if (ph.get("rel") != "first" and ivs[0] % 12 != 0) else lo_m
                ms = [m0 + (x - ivs[0]) for x in ivs]
                prev = ms[0]
                for v in range(nvo):
                    voices[v].append((T, D, ms[v] if v < len(ms) else "rest", mk))
                continue
            for iv in ivs:
                m = _resolve(iv, root_m, nxt.root, ref)
                if m is not None and isinstance(iv, int):
                    if ph.get("rel") != "first" and iv % 12 != 0:
                        m = _snap(m, scale_pcs, cp, prev)
                    elif ph.get("snapct"):
                        # 旋律（リード）: 1小節目の根音を基準に書いた線を、曲の音階に合わせ、強拍の長い音はその小節の和音の音へ寄せる
                        m = _snap(m, scale_pcs, cur_cp, prev)
                        bend = 2 if "^^" in (mk or "") else 1 if "^" in (mk or "") else 0
                        if D >= TPB and (T % (2 * TPB)) == 0 and (m + bend) % 12 not in cur_cp:
                            c = [x for x in range(m - 2, m + 3) if (x + bend) % 12 in cur_cp]
                            if c: m = min(c, key=lambda x: (abs(x - m), x))
                ms.append(m)
            if ms and ms[0] is not None: prev = ms[0]
            for v in range(nvo):
                voices[v].append((T, D, ms[v] if v < len(ms) else "rest", mk))
    out = []
    for v in voices:
        out.append(_to_tokens(v, nb * BAR))
    return out

def _mk_str(mk, m):
    m2 = re.match(r"^(.*?)>([+-]\d+)(.*)$", mk or "")
    if m2 and m is not None:
        return m2.group(1) + m2.group(3) + ">" + name(m + int(m2.group(2)))
    return mk or ""

def _to_tokens(evs, total):
    toks = []; pos = 0
    def add(a, b, s, suf):
        toks.append(f"{s}:{_fmt(round(b / TPB, 6) - round(a / TPB, 6))}{suf}")
    for T, D, m, mk in sorted(evs, key=lambda e: e[0]):
        if T < pos: continue   # 重なりは前の音を優先
        if T > pos: add(pos, T, "R", "")
        if m == "rest": add(T, T + D, "R", "")
        elif m is None: add(T, T + D, "x", (mk or "").replace("'", "") + "'")
        else: add(T, T + D, name(m), _mk_str(mk, m))
        pos = T + D
    if pos < total: add(pos, total, "R", "")
    # 休み同士をまとめる
    out = []
    for t in toks:
        if t.startswith("R:") and out and out[-1].startswith("R:"):
            out[-1] = f"R:{_fmt(float(out[-1][2:]) + float(t[2:]))}"
        else: out.append(t)
    return " ".join(out)

def render(ph, chords, key=None, mode=None, low="E2", bars=None, voice=0, snap=True):
    """put() に渡せる1本の音の並び。voice=0 はいちばん低い声部（パワーコードのパートならこれだけでよい）"""
    vs = render_voices(ph, chords, key, mode, low, bars, snap)
    return vs[min(voice, len(vs) - 1)]

def total_beats(notes):
    return sum(float(re.match(r"^[^:]*:([\d.]+)", t).group(1)) for t in notes.split())

# ── 数える・確かめる ──
def onsets16(ph):
    return sorted({e[0] // 3 for e in ph["ev"]})

def is_chug(e):
    t, d, ivs, mk = e
    return d <= 3 and "'" in (mk or "") and all(isinstance(x, int) and x in (0, 7, 12) for x in ivs) and ivs[0] == 0

def chug_ratio(ph):
    """刻みの割合: 刻み（ミュートした短い根音）が2つ以上ある拍の数 ÷ 全部の拍の数"""
    beats = ph["bars"] * 4
    cnt = {}
    for e in ph["ev"]:
        if is_chug(e): cnt[e[0] // TPB] = cnt.get(e[0] // TPB, 0) + 1
    return round(sum(1 for v in cnt.values() if v >= 2) / beats, 3)

def iv_range(ph):
    xs = [x for e in ph["ev"] for x in e[2] if isinstance(x, int)]
    return [min(xs), max(xs)] if xs else [0, 0]

def check(ph, inst):
    """機械の確認。問題の一覧（空なら合格）"""
    bad = []
    plen = ph["bars"] * BAR
    pos = 0
    for e in ph["ev"]:
        t, d, ivs, mk = e
        if d <= 0: bad.append("長さが0"); break
        if t < pos: bad.append("音が重なる"); break
        pos = t + d
        if "~" in (mk or ""): bad.append("ビブラート（使わない）")
        if ph["role"] == "リード" and "/" in (mk or ""): bad.append("リードにしゃくり")
        if len(ivs) > 1:
            ints = sorted(x for x in ivs if isinstance(x, int))
            for a in range(len(ints)):
                for b in range(a + 1, len(ints)):
                    if (ints[b] - ints[a]) % 12 in (1, 11) and "不協和" not in ph.get("tech", []): bad.append("和音の中で半音がぶつかる")
    if pos > plen: bad.append(f"長さが小節をこえる {pos}>{plen}")
    # 音域（12の根音すべてで）
    lo, hi = RANGE[inst]
    r = iv_range(ph)
    # ギターの low（いちばん低い弦）は E2（ふつう）〜 F1（8弦）。高いほうは E2 のときがいちばん高くなる
    rfs = [midi("E2"), midi("F1")] if ph.get("ref", "low") == "low" else [midi(ph["ref"])]
    for rf in rfs:
        if rf + r[0] < lo or rf + 11 + r[1] > hi:
            bad.append(f"音域の外 ref={name(rf)} {name(rf + r[0])}〜{name(rf + 11 + r[1])}"); break
    return bad

def signature(ph):
    return json.dumps([ph["bars"], ph.get("rel"), ph.get("ref"), [[e[0], e[1], e[2], e[3] or ""] for e in ph["ev"]]], sort_keys=True)

# ── 選ぶ ──
_LIB = {}
def load(inst):
    if inst not in _LIB:
        _LIB[inst] = json.load(open(LIB_PATHS[inst]))["phrases"]
    return _LIB[inst]

def _fits(ph, cls_list):
    if not cls_list: return True
    for c in cls_list:
        if not any(f in COMPAT.get(c, (c,)) for f in ph["fits"]): return False
    return True

def pick(inst, role=None, section=None, energy=None, feel=None, fits=None, bars=None, avoid=(), max_chug=None, min_chug=None,
         tech=None, kind=None, chords=None, key=None, mode=None, seed=0, top=8, src=None):
    """条件に合う型を1つ選ぶ。
    role: ギター「リフ」「バッキング」「アルペジオ」「リード」／ベース「根音」「ユニゾン」「旋律」「グルーヴ」「ブレイクダウン」「ペダル」
    section: 「前奏」「Aメロ」「Bメロ」「サビ」「看板リフ」「ブリッジ」「ブレイクダウン」
    energy: 0〜1（近いものから選ぶ）／feel: 「ふつう」「ハーフ」「ダブル」／fits: "m" などの和音の分類（chords を渡せば自動）
    avoid: 前に使った型の id（同じ family＝同じ親から作った兄弟もさける）／tech: 入っていてほしい技（「スライド」など）
    src: "gen"（自作）か "GuitarSet"（実演）にしぼる"""
    lib = load(inst)
    cls = cls_first = None
    if chords is not None:
        cl = [parse_chord(c, key, mode).cls for c in (chords if isinstance(chords, (list, tuple)) else [chords])]
        cls = sorted(set(cl)); cls_first = cl[:1]
    elif fits:
        cls = cls_first = [fits] if isinstance(fits, str) else list(fits)
    avoid = set(avoid or ())
    fam_avoid = {p.get("family") for p in lib if p["id"] in avoid}
    cands = []
    for p in lib:
        if p["id"] in avoid or (p.get("family") and p.get("family") in fam_avoid): continue
        if role and p["role"] != role: continue
        if section and section not in p["sections"]: continue
        if feel and p["feel"] != feel: continue
        if bars and p["bars"] != bars and not (bars % p["bars"] == 0 and p["bars"] >= 1): continue
        if max_chug is not None and p.get("chug", 0) > max_chug: continue
        if min_chug is not None and p.get("chug", 0) < min_chug: continue
        if kind and p.get("kind") != kind: continue
        if src and not p["src"].startswith(src): continue
        if tech and not all(t in p.get("tech", []) for t in ([tech] if isinstance(tech, str) else tech)): continue
        # 1小節目の根音を基準にした型と、パワーコードの型（fits に "5"）は、1つ目の和音で合うかを見る（ほかの小節は曲の音階に合わせて鳴らす）
        if not _fits(p, cls_first if (p.get("rel") == "first" or "5" in p["fits"]) else cls): continue
        cands.append(p)
    if not cands: return None
    rng = random.Random(seed)
    if energy is not None:
        cands.sort(key=lambda p: (abs(p["energy"] - energy), rng.random()))
        cands = cands[:max(1, top)]
    return rng.choice(cands)

def unison_bass(gph):
    """ギターの型から、ユニゾンのベースの型を作る（ライブラリに無いときに使う）。
    ギターのいちばん低い声部の根音・5度・オクターブだけをなぞり、高い旋律の所は前の音を伸ばす"""
    ev = []
    for t, d, ivs, mk in gph["ev"]:
        x = ivs[0]
        if not isinstance(x, int): continue
        if x <= 12:
            ev.append([t, d, [x], (mk or "").replace("//@0.1", "").replace("///@0.1", "")])
        elif ev and ev[-1][0] + ev[-1][1] == t:
            ev[-1][1] += d
    return {"id": gph["id"] + "-uni", "inst": "bass", "role": "ユニゾン", "kind": "ユニゾン（その場で作成）", "bars": gph["bars"], "rel": gph.get("rel", "bar"),
            "ref": "E1", "fits": gph["fits"], "ev": ev, "sections": gph["sections"], "energy": gph.get("energy", 0.5), "feel": gph.get("feel", "ふつう"), "tech": ["ユニゾン"], "src": "gen:unison", "family": gph.get("family")}

def guitar_from_bass(bph, voicing=(0, 7, 12)):
    """ベースの型（ブレイクダウン・ペダルなど）と同じリズムで、パワーコードを弾くギターの型を作る（キック・ベース・ギターを一致させる）"""
    ev = [[t, d, [x + v for v in voicing] if isinstance(x, int) else [0], mk] for t, d, (x, *_), mk in bph["ev"]]
    return {"id": bph["id"] + "-gtr", "inst": "guitar", "role": "リフ", "kind": "ベースと一致（その場で作成）", "bars": bph["bars"], "rel": bph.get("rel", "bar"), "ref": "low",
            "fits": bph["fits"], "ev": ev, "sections": bph["sections"], "energy": bph.get("energy", 0.5), "feel": bph.get("feel", "ふつう"), "tech": ["キックと一致"],
            "src": "gen:from-bass", "family": bph.get("family"), "pc": True, "chug": 0, "kick": bph.get("kick")}

def attacks_per_bar(ph):
    return len(ph["ev"]) / ph["bars"]

GUITAR_ROLE_FOR = {"前奏": ["アルペジオ", "リフ", "バッキング"], "Aメロ": ["リフ", "アルペジオ"], "Bメロ": ["バッキング", "リフ"], "サビ": ["バッキング"],
                   "看板リフ": ["リフ"], "ブリッジ": ["アルペジオ", "バッキング"], "ブレイクダウン": ["リフ"]}

def pick_pair(section, chords, key=None, mode=None, energy=0.6, low="E2", bass_low="E1", how="auto", avoid=(), seed=0, bars=None, guitar_role=None, bass_role=None):
    """ギターとベースを合わせて選ぶ。how: "unison"（同じリズム・同じ根音）／"split"（すみ分け: ギターが忙しければベースは少なく、ギターが伸ばせばベースが動く）／"auto"
    返り値: {"guitar": {"phrase", "notes"（いちばん低い声部）, "voices"（全部の声部）}, "bass": {"phrase", "notes"}, "how"}"""
    nb = bars or len(chords)
    rng = random.Random(seed * 7919 + 13)
    if section == "ブレイクダウン" and how in ("auto", "unison") and not guitar_role:
        # ブレイクダウン: ベースの型（キックの位置つき）を先に選び、ギターを同じリズムのパワーコードにする
        b = pick("bass", role="ブレイクダウン", energy=energy, avoid=avoid, seed=rng.randrange(10 ** 6))
        if b:
            g = guitar_from_bass(b)
            gv = render_voices(g, chords, key, mode, low, nb)
            return {"how": "unison", "guitar": {"phrase": g, "notes": gv[0], "voices": gv, "powerChord": True},
                    "bass": {"phrase": b, "notes": render(b, chords, key, mode, bass_low, nb)}, "kick": (b.get("kick") or []) * max(1, nb // b["bars"])}
    roles = [guitar_role] if guitar_role else GUITAR_ROLE_FOR.get(section, ["リフ"])
    g = None
    for i, r in enumerate(roles if not guitar_role else roles):
        r = roles[(i + rng.randrange(len(roles))) % len(roles)] if not guitar_role else r
        g = pick("guitar", role=r, section=section, energy=energy, chords=chords, key=key, mode=mode, avoid=avoid, seed=rng.randrange(10 ** 6),
                 bars=None if nb % 4 == 0 else nb)
        if g: break
    if g is None: raise LookupError(f"ギターの型が見つかりません: {section}")
    if how == "auto":
        how = "unison" if g["role"] == "リフ" and section in ("看板リフ", "前奏", "ブレイクダウン", "Aメロ") and rng.random() < 0.7 else "split"
    b = None
    if how == "unison":
        lib = load("bass")
        cand = [p for p in lib if p.get("unison_of") == g["id"]]
        b = cand[0] if cand else unison_bass(g)
    else:
        dense = attacks_per_bar(g) >= 7
        if bass_role:
            broles = [bass_role]
        elif section == "ブレイクダウン":
            broles = ["ブレイクダウン"]
        elif dense:
            broles = ["ペダル", "根音"]
        elif g["role"] in ("バッキング",):
            broles = ["根音", "旋律"] if energy >= 0.5 else ["旋律", "根音"]
        else:
            broles = ["旋律", "根音", "グルーヴ"]
        for r in broles:
            b = pick("bass", role=r, section=section if r != "グルーヴ" else None, energy=(energy * 0.6 if dense else energy), chords=chords, key=key, mode=mode,
                     avoid=avoid, seed=rng.randrange(10 ** 6), bars=None if nb % 4 == 0 else nb)
            if b and dense and attacks_per_bar(b) > 6:
                b = pick("bass", role=r, energy=0.2, chords=chords, key=key, mode=mode, avoid=avoid, seed=rng.randrange(10 ** 6)) or b
            if b: break
        if b is None:
            b = unison_bass(g); how = "unison"
    gv = render_voices(g, chords, key, mode, low, nb)
    bn = render(b, chords, key, mode, bass_low, nb)
    return {"how": how, "guitar": {"phrase": g, "notes": gv[0], "voices": gv, "powerChord": g.get("pc", False)},
            "bass": {"phrase": b, "notes": bn}}

def describe(ph):
    return f"{ph['id']} {ph['role']}/{ph.get('kind','')} {ph['bars']}小節 強さ{ph['energy']} {ph['feel']} 刻み{ph.get('chug',0)} 区間{','.join(ph['sections'])} 技{','.join(ph.get('tech',[]))} 和音{','.join(ph['fits'])}"

if __name__ == "__main__":
    import sys
    g = pick("guitar", role="リフ", section="看板リフ", energy=0.7, chords=["Dm", "Dm"], seed=int(sys.argv[1]) if len(sys.argv) > 1 else 0)
    print(describe(g)); print(render(g, ["Dm", "Bb"], key="D", mode="aeolian", low="D2"))
    p = pick_pair("サビ", ["Bb", "C", "Dm", "Dm"], key="D", mode="aeolian", energy=0.8, low="D2", seed=1)
    print(p["how"], describe(p["guitar"]["phrase"])); print(p["guitar"]["notes"]); print(describe(p["bass"]["phrase"])); print(p["bass"]["notes"])
