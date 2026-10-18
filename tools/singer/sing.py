#!/usr/bin/env python3
"""歌声エンジン（UTAU 式の音源を、WORLD で音程と長さを変えてつなぐ）。

曲の JSON の "vocals" に書いた歌（音符＋歌詞）から、歌声の WAV を作る。
  python3 tools/singer/sing.py render <曲.json> <出力.wav> [--sr 48000] [--dry]
  python3 tools/singer/sing.py mix <曲.json> <伴奏.wav>        … 伴奏の WAV に歌を混ぜて上書き（作曲ソフトの書き出しが呼ぶ）
  python3 tools/singer/sing.py ust <曲.json> <出力.ust> [--index 0]  … UTAU / OpenUtau / Synthesizer V で読める UST
  python3 tools/singer/sing.py check <曲.json>                  … 音源にない歌詞・音域を調べる

歌の書き方（"vocals" の 1 つ）:
  {"voice": "teto", "notes": "R:4 D4:1:よ E4:1:る F4:2:の ー:1@G4 R:1 ...", "volume": 1.0, "pan": 0, "reverb": 0.22}
  - 「音名:拍:歌詞」。歌詞はひらがな 1 音（「きゃ」「しゅ」のような小さい字つきも 1 音）。
  - 「R:拍」は休み。休みのあとは息つぎとして、歌い出しの音（単独音）から入る。
  - 「音名:拍:ー」は、前の音の母音のまま音程だけ変える（こぶし・メリスマ）。
  - 音名のあとに「!」で強く、「?」で弱く（例 "A4!:1:な"）。
音源は配布できない（重音テトの規約で、音源の再配布は禁止）。リポジトリには入れず、
環境変数 SUNSHINE_VOICEBANKS（既定は assets-src/voicebanks と ~/voicebanks）に置く。
"""
import sys, os, json, re, math, hashlib
import numpy as np
import soundfile as sf
import pyworld as pw
from scipy import signal

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FP = 5.0  # WORLD のフレーム間隔（ミリ秒）
CACHE = os.path.expanduser("~/.cache/sunshine-singer")

VOICES = {
    # 声の名前 → 音源のフォルダ（SUNSHINE_VOICEBANKS の下）と、つなぎ方
    "teto": {"dir": "teto/重音テト音声ライブラリー", "vcv": "重音テト連続音", "cv": "重音テト単独音", "extra": "重音テトエクストラ", "suffix": ""},
    # 弱音源（通常とささやきの中間。やわらかく息まじり）。歌詞のうしろに「弱」がついた名前で入っている
    "teto-soft": {"dir": "teto/重音テト音声ライブラリー", "vcv": "重音テト弱連続音", "cv": "重音テト弱単独音", "suffix": "弱"},
}

def bank_roots():
    env = os.environ.get("SUNSHINE_VOICEBANKS")
    roots = [env] if env else []
    roots += [os.path.join(ROOT, "assets-src/voicebanks"), os.path.expanduser("~/voicebanks"), "/home/claude/voicebanks"]
    return [r for r in roots if r and os.path.isdir(r)]

# ---------- かな → 母音 ----------
VOWEL_OF = {}
for v, chars in {"a": "あかさたなはまやらわがざだばぱぁゃゎ", "i": "いきしちにひみりぎじぢびぴぃ", "u": "うくすつぬふむゆるぐずづぶぷぅゅゔ",
                 "e": "えけせてねへめれげぜでべぺぇ", "o": "おこそとのほもよろをごぞどぼぽぉょ", "n": "ん"}.items():
    for c in chars: VOWEL_OF[c] = v

def vowel_of(kana, prev="a"):
    for c in reversed(kana):
        if c in VOWEL_OF: return VOWEL_OF[c]
        if c == "ー": return prev
    return prev

# ---------- 原音設定 ----------
class Bank:
    def __init__(self, voice):
        conf = VOICES[voice]
        base = None
        for r in bank_roots():
            p = os.path.join(r, conf["dir"])
            if os.path.isdir(p): base = p; break
        if not base:
            raise SystemExit(f"歌声の音源「{voice}」が見つかりません。SUNSHINE_VOICEBANKS に置き場所を書いてください（探した場所: {bank_roots()}）")
        self.base = base
        self.suf = conf.get("suffix", "")
        self.vcv = self.read_oto(os.path.join(base, conf["vcv"])) if conf.get("vcv") else {}
        self.cv = self.read_oto(os.path.join(base, conf["cv"])) if conf.get("cv") else {}
        self.extra = self.read_oto(os.path.join(base, conf["extra"])) if conf.get("extra") else {}

    @staticmethod
    def read_oto(d):
        out = {}
        p = os.path.join(d, "oto.ini")
        if not os.path.exists(p): return out
        raw = open(p, "rb").read()
        try: txt = raw.decode("cp932")
        except UnicodeDecodeError: txt = raw.decode("utf-8", "replace")
        for line in txt.splitlines():
            if "=" not in line: continue
            wav, rest = line.split("=", 1)
            f = rest.split(",")
            if len(f) < 6: continue
            alias = f[0] or os.path.splitext(wav)[0]
            try: nums = [float(x) if x.strip() else 0.0 for x in f[1:6]]
            except ValueError: continue
            if alias not in out:
                out[alias] = {"wav": os.path.join(d, wav), "offset": nums[0], "consonant": nums[1], "cutoff": nums[2], "pre": nums[3], "ovl": nums[4]}
        return out

    def pick(self, lyric, prev_vowel):
        """前の母音（None は歌い出し）と歌詞から、使う音を決める"""
        s = self.suf
        if prev_vowel:
            a = self.vcv.get(f"{prev_vowel} {lyric}{s}")
            if a: return a, "vcv"
        for k in (f"- {lyric}{s}", f"{lyric}{s}"):
            a = self.cv.get(k)
            if a: return a, "cv"
        a = self.vcv.get(f"- {lyric}{s}")
        if a: return a, "vcv"
        return None, None

    def tail(self, vowel):
        s = self.suf
        for k in (f"{vowel} R{s}", f"{vowel} -{s}", f"{vowel} R", f"{vowel} -"):
            a = self.vcv.get(k)
            if a: return a
        return None

# ---------- WORLD の分析（キャッシュ） ----------
_ANA = {}
SP_DIM = 120  # スペクトル包絡を縮めて保存する次元（ディスクを節約。歌声には十分）
def analyze(path):
    """WORLD の分析（f0・スペクトル包絡・非周期性）。縮めた形で ~/.cache に保存して、次からはすぐ読む"""
    if path in _ANA: return _ANA[path]
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.md5((path + str(os.path.getmtime(path)) + f"v2-{SP_DIM}").encode()).hexdigest()
    cp = os.path.join(CACHE, key + ".npz")
    if os.path.exists(cp):
        z = np.load(cp); f0 = z["f0"].astype(np.float64); sr = int(z["sr"])
        csp = z["csp"].astype(np.float64); cap = z["cap"].astype(np.float64)
    else:
        x, sr = sf.read(path, dtype="float64")
        if x.ndim > 1: x = x.mean(axis=1)
        f0, t = pw.harvest(x, sr, f0_floor=90, f0_ceil=900, frame_period=FP)
        f0 = pw.stonemask(x, f0, t, sr)
        sp = pw.cheaptrick(x, f0, t, sr)
        ap = pw.d4c(x, f0, t, sr)
        csp = pw.code_spectral_envelope(sp, sr, SP_DIM)
        cap = pw.code_aperiodicity(ap, sr)
        np.savez_compressed(cp, f0=f0.astype(np.float32), csp=csp.astype(np.float16), cap=cap.astype(np.float16), sr=sr)
        csp = csp.astype(np.float16).astype(np.float64); cap = cap.astype(np.float16).astype(np.float64)
    fft = pw.get_cheaptrick_fft_size(sr)
    sp = pw.decode_spectral_envelope(np.ascontiguousarray(csp), sr, fft).astype(np.float32)
    ap = pw.decode_aperiodicity(np.ascontiguousarray(cap), sr, fft).astype(np.float32)
    r = (f0, sp, ap, sr)
    if len(_ANA) > 160: _ANA.pop(next(iter(_ANA)))
    _ANA[path] = r
    return r

# ---------- 楽譜を読む ----------
NOTE_RE = re.compile(r"^([A-G])(#|b)?(-?\d)([!?]*)$")
def midi_of(name):
    m = NOTE_RE.match(name)
    if not m: raise ValueError(f"音名が読めません「{name}」")
    n = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[m.group(1)] + {"#": 1, "b": -1, None: 0}[m.group(2)]
    vel = 1.0 + 0.18 * m.group(4).count("!") - 0.2 * m.group(4).count("?")
    return 12 * (int(m.group(3)) + 1) + n, vel

def parse_notes(text):
    """"D4:1:よ R:1 E4:1:ー" → [{"beat","len","midi","lyric","vel"}]（休みは lyric=None）"""
    out, beat = [], 0.0
    for tok in text.split():
        parts = tok.split(":")
        if parts[0] == "R":
            ln = float(parts[1]); out.append({"beat": beat, "len": ln, "midi": None, "lyric": None, "vel": 1}); beat += ln; continue
        if len(parts) < 3: raise ValueError(f"「音名:拍:歌詞」の形ではありません「{tok}」")
        midi, vel = midi_of(parts[0]); ln = float(parts[1]); ly = parts[2]
        out.append({"beat": beat, "len": ln, "midi": midi, "lyric": ly, "vel": vel}); beat += ln
    return out

# ---------- 音程の線 ----------
def pitch_curve(events, total, rng, vib):
    """events: [(start, end, midi)]（秒）。5ms ごとの半音の値を返す。音の切りかわりはなめらかに、長い音には控えめなビブラート"""
    n = int(total * 1000 / FP) + 2
    t = np.arange(n) * FP / 1000
    cur = np.full(n, np.nan)
    for s, e, m in events:
        cur[(t >= s) & (t < e)] = m
    # 休みのところは近い音で埋める（息つぎの子音などのため）
    idx = np.where(~np.isnan(cur))[0]
    if len(idx) == 0: return t, np.full(n, 60.0)
    cur = np.interp(np.arange(n), idx, cur[idx])
    out = cur.copy()
    for i in range(1, len(events)):
        ps, pe, pm = events[i - 1]; s, e, m = events[i]
        if s - pe > 0.25 or pm == m: continue
        g = min(0.13, 0.45 * (e - s), 0.45 * (pe - ps)) * (1.0 + 0.04 * min(abs(m - pm), 7))
        a, b = s - 0.45 * g, s + 0.55 * g
        sel = (t >= a) & (t < b + 0.12)
        x = np.clip((t[sel] - a) / (b - a), 0, 1)
        sm = x * x * (3 - 2 * x)
        # 少しだけ行きすぎて戻る（声らしさ）。大きく跳ぶほど少し大きく
        over = 0.06 * (m - pm) * np.exp(-np.clip((t[sel] - b), 0, None) / 0.05) * (t[sel] > b)
        out[sel] = pm + (m - pm) * sm + over
    # ビブラート: 0.45 秒より長い音の、後ろ半分にだけ。深さは ±vib セント
    if vib > 0:
        for s, e, m in events:
            d = e - s
            if d < 0.45: continue
            st = s + max(0.22, 0.38 * d)
            sel = (t >= st) & (t < e)
            if not sel.any(): continue
            tt = t[sel] - st
            ramp = np.clip(tt / 0.35, 0, 1) * np.clip((e - t[sel]) / 0.08, 0, 1)
            rate = 5.3 + 0.25 * np.sin(2 * np.pi * 0.7 * tt)
            out[sel] += (vib / 100.0) * ramp * np.sin(2 * np.pi * np.cumsum(rate) * FP / 1000)
    # ゆっくりしたゆらぎ（±4 セントほど）
    drift = np.convolve(rng.standard_normal(n), np.ones(80) / 80, mode="same") * 0.35
    return t, out + drift

# ---------- 1 音分をつくる ----------
def _frames(oto, tau, L, P_out, C_out):
    """oto の音を出力の時刻 tau（ms）へ写す。先行発声の点（母音の頭）と子音の終わりを、出力の P_out・C_out にそろえる"""
    f0o, sp, ap, sr = analyze(oto["wav"])
    nfr = len(f0o); total_ms = nfr * FP
    s0 = oto["offset"]; C = oto["consonant"]; P = min(oto["pre"], C)
    end = s0 - oto["cutoff"] if oto["cutoff"] < 0 else total_ms - oto["cutoff"]
    end = min(max(end, s0 + C + 20), total_ms - FP)
    if L <= C_out + 10:
        src = s0 + tau * (C / max(L, 1))
    else:
        xo = [0.0, P_out, C_out, L]; xs = [s0, s0 + P, s0 + C, end]
        if not (P_out < C_out): xo = [0.0, C_out, L]; xs = [s0, s0 + C, end]
        src = np.interp(tau, xo, xs)
    fi = np.clip(src / FP, 0, nfr - 1.001)
    i0 = fi.astype(int); w = (fi - i0)[:, None]
    lsp = np.log(np.maximum(sp, 1e-12))
    lsp2 = lsp[i0] * (1 - w) + lsp[i0 + 1] * w
    ap2 = ap[i0] * (1 - w) + ap[i0 + 1] * w
    fo = f0o[np.round(fi).astype(int)]
    return lsp2, ap2, fo, sr

def render_piece(oto, out_len, f0_target, vel, sr_out, opts=None):
    """oto の音を、出力の長さ out_len 秒に合わせて伸ばし、f0_target（Hz の配列、5ms ごと）の音程で作る。
    oto に "_blend": (別の声の oto, 重み) があれば、2つの声の「声の形（スペクトル包絡）」を混ぜてから 1 回だけ作る
    （波形を2本重ねると、子音が二重になって雑音のように聞こえるため）"""
    C = oto["consonant"]
    L = out_len * 1000
    k = len(f0_target)
    tau = np.arange(k) * FP
    P_out = min(oto["pre"], C)
    lsp2, ap2, fo, sr = _frames(oto, tau, L, P_out, C)
    bl = oto.get("_blend")
    if bl:
        o2, wgt = bl
        l2, a2, f2, sr2 = _frames(o2, tau, L, P_out, C)
        if sr2 == sr and l2.shape == lsp2.shape:
            # 2つの声の大きさの差は、母音のところの平均でそろえてから混ぜる
            vm = (fo > 0) & (f2 > 0)
            if vm.any():
                d = np.mean(l2[vm]) - np.mean(lsp2[vm]); l2 = l2 - d * 0.6
            lsp2 = lsp2 * (1 - wgt) + l2 * wgt
            ap2 = ap2 * (1 - wgt) + a2 * wgt
            fo = np.where(fo > 0, fo, np.where(f2 > 0, 0, 0))
    sp2 = np.exp(lsp2)
    # 連続音の頭（前の母音の部分）が、録音で「ひ」などのあとのため、かすれた息の音になっていることがある
    #   （例: 「い み」は「いひみ」から切り出していて、頭の「い」が息まじり）。重ねたときに「ザー」と雑音に聞こえるので、
    #   頭の部分の「かすれ」を、この音の母音（伸ばす部分）と同じくらいまでに抑える
    head = (tau < min(oto["ovl"] + 50, max(P_out - 20, 0))) & (fo > 0)
    tailv = (tau >= C) & (fo > 0)
    if head.any() and tailv.sum() >= 3:
        ref = np.median(ap2[tailv], axis=0)
        ap2 = np.where(head[:, None], np.minimum(ap2, ref[None, :] + 0.12), ap2)
    voiced = fo > 0
    # 母音の「かすれ」の整理: WORLD の分析では、テトの「い」などで高い音のかすれ（非周期性）が 1 コマごとにばらつき、
    #   作り直すと「サー」というザラついた雑音に聞こえる（2026-10-18、人間「空のあとに雑音」）。
    #   有声のところだけ、時間方向にならし（約 45ms）、周波数ごとの上限で抑える。clean=0 で止める
    cl = float((opts or {}).get("clean", 1.0))
    if cl > 0 and voiced.sum() > 3:
        nb0 = ap2.shape[1]; fq = np.arange(nb0) * (sr / 2) / (nb0 - 1)
        from scipy.ndimage import uniform_filter1d
        sm = uniform_filter1d(ap2, 9, axis=0, mode="nearest")
        capf = 0.06 + 0.5 * np.clip((fq - 1500) / 6500, 0, 1)
        cleaned = np.minimum(sm, capf[None, :])
        ap2 = np.where(voiced[:, None], ap2 * (1 - cl) + cleaned * cl, ap2)
    # 元の録音の細かい揺れを、少しだけ残す
    med = np.median(fo[voiced]) if voiced.any() else 0
    jit = np.ones(k)
    if med > 0:
        r = np.where(voiced, fo / med, 1.0)
        r = r / np.convolve(r, np.ones(15) / 15, mode="same")
        jit = np.clip(r, 0.985, 1.015) ** 0.6
    f0 = np.where(voiced, f0_target * jit, 0.0)
    o = opts or {}
    nb = sp2.shape[1]; freqs = np.arange(nb) * (sr / 2) / (nb - 1)
    # 声の明るさ（フォルマント）: 1.0=そのまま。1.04〜1.08 で、のどの響きが少し高く・軽く、透き通った声になる
    fm = float(o.get("formant", 1.0))
    if abs(fm - 1.0) > 1e-3:
        src_bins = np.clip(np.arange(nb) / fm, 0, nb - 1)
        lo = np.floor(src_bins).astype(int); hi = np.minimum(lo + 1, nb - 1); ww = src_bins - lo
        lsp2 = np.log(np.maximum(sp2, 1e-12))
        sp2 = np.exp(lsp2[:, lo] * (1 - ww) + lsp2[:, hi] * ww)
        ap2 = ap2[:, lo] * (1 - ww) + ap2[:, hi] * ww
    # 息まじり（breathy）: 0〜0.5。2kHz より上の「かすれ」を少し増やして、ふわっと抜ける声に
    br = float(o.get("breathy", 0.0))
    if br > 0:
        wgt = np.clip((freqs - 1500) / 4000, 0, 1) * br
        ap2 = ap2 + (1 - ap2) * wgt[None, :] * 0.6
    # 子音の強さ: 子音（伸ばさない部分）だけ大きく。「ぶ」「ば」などが埋もれないように
    cg = float(o.get("consonant", 1.0))
    if abs(cg - 1.0) > 1e-3:
        cmask = (tau < min(C, L)).astype(float)
        cmask = np.convolve(cmask, np.ones(5) / 5, mode="same")
        # 高い帯域（サ行の「スー」）は強めない（強めると、かすれた雑音に聞こえる）
        fw = np.clip((6000 - freqs) / 3000, 0, 1)
        sp2 = sp2 * (1 + (cg ** 2 - 1) * cmask[:, None] * fw[None, :])
    y = pw.synthesize(np.ascontiguousarray(f0, dtype=np.float64), np.ascontiguousarray(sp2, dtype=np.float64), np.ascontiguousarray(np.clip(ap2, 0, 1), dtype=np.float64), sr, FP)
    if sr != sr_out:
        y = signal.resample_poly(y, sr_out, sr)
    return y * vel

def build_vocal(vdef, bpm, bank, sr_out, total_sec=None, seed=1):
    notes = parse_notes(vdef["notes"])
    spb = 60.0 / bpm
    rng = np.random.default_rng(seed)
    # 1) 歌う音を「ひとかたまり（ピース）」にまとめる（「ー」は前の音のピースに足す）
    pieces = []  # {lyric, start, end, events:[(s,e,midi,vel)], phrase_start}
    prev_rest = True
    for n in notes:
        s, e = n["beat"] * spb, (n["beat"] + n["len"]) * spb
        if n["lyric"] is None:
            prev_rest = True; continue
        if n["lyric"] in ("ー", "-", "~") and pieces and not prev_rest:
            pieces[-1]["end"] = e; pieces[-1]["events"].append((s, e, n["midi"], n["vel"])); continue
        pieces.append({"lyric": n["lyric"], "start": s, "end": e, "events": [(s, e, n["midi"], n["vel"])], "head": prev_rest})
        prev_rest = False
    if not pieces: return np.zeros((int(sr_out * (total_sec or 1)), 2))
    # 2) 音を選ぶ・前の母音（blend があれば、もう1つの声の同じ音も選んでおく）
    bl = vdef.get("blend")
    bank2 = Bank(bl.get("voice", "teto-soft")) if bl else None
    bamt = float(bl.get("amount", 0.5)) if bl else 0.0
    pv = None
    for p in pieces:
        if p["head"]: pv = None
        oto, kind = bank.pick(p["lyric"], pv)
        if oto is None:
            print(f"注意: 音源に「{(pv + ' ') if pv else ''}{p['lyric']}」がありません。「あ」で代わりに歌います", file=sys.stderr)
            oto, kind = bank.pick("あ", pv)
        if bank2 is not None:
            o2, _ = bank2.pick(p["lyric"], pv)
            if o2: oto = {**oto, "_blend": (o2, bamt)}
        p["oto"] = oto; p["kind"] = kind
        pv = vowel_of(p["lyric"], pv or "a")
        p["vowel"] = pv
    # 3) 先行発声・オーバーラップを、前の音の長さに合わせて縮める（UTAU と同じ考え方）
    for i, p in enumerate(pieces):
        pre, ovl = p["oto"]["pre"] / 1000, p["oto"]["ovl"] / 1000
        if i > 0 and not p["head"]:
            q = pieces[i - 1]; room = (q["end"] - q["start"]) * 0.5
            if pre - ovl > room > 0:
                f = room / (pre - ovl); pre *= f; ovl *= f
        p["pre"], p["ovl"] = pre, max(ovl, 0.004)
    last_end = max(p["end"] for p in pieces)
    total = max(total_sec or 0, last_end + 1.5)
    events = [(s, e, m) for p in pieces for (s, e, m, v) in p["events"]]
    vib = float(vdef.get("vibrato", 16))
    t, semis = pitch_curve(events, total, rng, vib)
    semis = semis + float(vdef.get("transpose", 0))
    hz = 440.0 * 2 ** ((semis - 69) / 12)
    out = np.zeros(int(total * sr_out) + sr_out)
    # 4) ピースごとに作って、重ねる
    for i, p in enumerate(pieces):
        a = p["start"] - p["pre"]
        nxt = pieces[i + 1] if i + 1 < len(pieces) else None
        joined = nxt is not None and not nxt["head"]
        if joined: b = nxt["start"] - nxt["pre"] + nxt["ovl"]
        else: b = p["end"] + 0.03
        b = max(b, a + 0.05)
        k0 = int(a * 1000 / FP); k1 = int(b * 1000 / FP)
        ft = hz[np.clip(np.arange(k0, k1), 0, len(hz) - 1)]
        vel = np.mean([v for (_, _, _, v) in p["events"]])
        y = render_piece(p["oto"], b - a, ft, vel, sr_out, vdef)
        n0 = int(a * sr_out); y = y[: max(0, int((b - a) * sr_out))]
        env = np.ones(len(y))
        fi = min(len(y), int(p["ovl"] * sr_out)) if not p["head"] else min(len(y), int(0.006 * sr_out))
        if fi > 0: env[:fi] = np.sin(np.linspace(0, np.pi / 2, fi)) ** 2
        fo = min(len(y), int(nxt["ovl"] * sr_out)) if joined else min(len(y), int(0.07 * sr_out))
        if fo > 0: env[-fo:] *= np.cos(np.linspace(0, np.pi / 2, fo)) ** 2
        if n0 < 0: y, env, n0 = y[-n0:], env[-n0:], 0
        out[n0:n0 + len(y)] += (y * env)[: len(out) - n0]
        # フレーズの終わり: 「母音 R」で自然に息を抜く
        if not joined:
            tl = bank.tail(p["vowel"])
            if tl and bank2 is not None:
                t2 = bank2.tail(p["vowel"])
                if t2: tl = {**tl, "_blend": (t2, bamt)}
            if tl:
                ta = p["end"] - tl["pre"] / 1000; tb = p["end"] + 0.22
                kk0, kk1 = int(ta * 1000 / FP), int(tb * 1000 / FP)
                ft2 = hz[np.clip(np.arange(kk0, kk1), 0, len(hz) - 1)]
                y2 = render_piece(tl, tb - ta, ft2, vel * 0.9, sr_out, vdef)[: int((tb - ta) * sr_out)]
                e2 = np.ones(len(y2)); f2 = min(len(y2), int(max(tl["ovl"], 30) / 1000 * sr_out) + int(0.03 * sr_out))
                e2[:f2] = np.sin(np.linspace(0, np.pi / 2, f2)) ** 2
                g2 = min(len(y2), int(0.06 * sr_out)); e2[-g2:] *= np.linspace(1, 0, g2)
                m0 = int(ta * sr_out)
                out[m0:m0 + len(y2)] += (y2 * e2)[: len(out) - m0]
    return out[: int(total * sr_out)]

# ---------- 声の仕上げ（EQ・コンプ・残響） ----------
def biquad(kind, f, sr, q=0.707, db=0.0):
    A = 10 ** (db / 40); w = 2 * np.pi * f / sr; al = np.sin(w) / (2 * q); c = np.cos(w)
    if kind == "hp":
        b = [(1 + c) / 2, -(1 + c), (1 + c) / 2]; a = [1 + al, -2 * c, 1 - al]
    elif kind == "peak":
        b = [1 + al * A, -2 * c, 1 - al * A]; a = [1 + al / A, -2 * c, 1 - al / A]
    elif kind == "hshelf":
        sq = 2 * np.sqrt(A) * al
        b = [A * ((A + 1) + (A - 1) * c + sq), -2 * A * ((A - 1) + (A + 1) * c), A * ((A + 1) + (A - 1) * c - sq)]
        a = [(A + 1) - (A - 1) * c + sq, 2 * ((A - 1) - (A + 1) * c), (A + 1) - (A - 1) * c - sq]
    return np.array(b) / a[0], np.array(a) / a[0]

def polish(x, sr, vdef):
    air = float(vdef.get("air", 1.5))
    for kind, f, q, db in [("hp", 110, 0.7, 0), ("peak", 280, 1.0, -2.5 - 0.5 * air), ("peak", 3000, 0.9, 2.0), ("peak", 7200, 3.0, -2.5), ("hshelf", 10500, 0.7, air)]:
        b, a = biquad(kind, f, sr, q, db); x = signal.lfilter(b, a, x)
    # ディエッサー: サ行・シ・ツの「シー」が強すぎる所だけ、4.5kHz より上を下げる（最大 -9dB）
    b, a = signal.butter(4, 4500 / (sr / 2), "high"); hi = signal.lfilter(b, a, x); lo = x - hi
    w5 = int(0.005 * sr)
    eh = np.sqrt(np.convolve(hi * hi, np.ones(w5) / w5, mode="same") + 1e-12)
    ea = np.sqrt(np.convolve(x * x, np.ones(w5 * 8) / (w5 * 8), mode="same") + 1e-12)
    ratio_db = 20 * np.log10(eh / ea)
    red = np.clip(ratio_db - (-6.0), 0, 9)
    red = np.convolve(red, np.ones(w5) / w5, mode="same")
    x = lo + hi * 10 ** (-red / 20)
    # なめらかなコンプ（RMS・比 3:1）
    win = int(0.02 * sr)
    rms = np.sqrt(np.convolve(x * x, np.ones(win) / win, mode="same") + 1e-12)
    lv = 20 * np.log10(rms + 1e-9)
    thr = -24.0
    gr = np.where(lv > thr, (thr - lv) * (1 - 1 / 3.0), 0.0)
    gr = signal.lfilter([0.002], [1, -0.998], gr) if False else gr
    sm = np.zeros_like(gr); g = 0.0
    att, rel = np.exp(-1 / (0.008 * sr)), np.exp(-1 / (0.12 * sr))
    for i in range(0, len(gr), 32):
        tgt = gr[i]; c = att if tgt < g else rel
        g = tgt + (g - tgt) * c ** 32; sm[i:i + 32] = g
    x = x * 10 ** (sm / 20)
    return x

def reverb(x, sr, wet, seed=3):
    if wet <= 0: return np.stack([x, x], 1)
    rng = np.random.default_rng(seed)
    n = int(2.4 * sr); t = np.arange(n) / sr
    out = []
    for ch in range(2):
        ir = rng.standard_normal(n) * np.exp(-t * 6.9 / 2.1)
        ir[: int(0.022 * sr)] = 0  # プリディレイ
        b, a = biquad("hp", 300, sr); ir = signal.lfilter(b, a, ir)
        b, a = signal.butter(1, 6500 / (sr / 2)); ir = signal.lfilter(b, a, ir)
        ir /= np.sqrt(np.sum(ir ** 2))
        out.append(signal.fftconvolve(x, ir)[: len(x)])
    w = np.stack(out, 1) * wet
    return np.stack([x, x], 1) * (1 - 0.35 * wet) + w

def render_song(song, sr_out, total_sec=None, dry=False):
    bpm = float(song["bpm"])
    mix = None
    for i, vd in enumerate(song.get("vocals", [])):
        bank = Bank(vd.get("voice", "teto"))
        v = build_vocal(vd, bpm, bank, sr_out, total_sec, seed=11 + i)
        v = polish(v, sr_out, vd)
        pk = np.max(np.abs(v)) + 1e-9
        v = v / pk * 0.5
        st = reverb(v, sr_out, 0 if dry else float(vd.get("reverb", 0.22)), seed=5 + i)
        pan = float(vd.get("pan", 0)); g = float(vd.get("volume", 1.0))
        st[:, 0] *= g * math.cos((pan + 1) * math.pi / 4) * math.sqrt(2)
        st[:, 1] *= g * math.sin((pan + 1) * math.pi / 4) * math.sqrt(2)
        if mix is None: mix = st
        else:
            n = max(len(mix), len(st)); m2 = np.zeros((n, 2)); m2[: len(mix)] += mix; m2[: len(st)] += st; mix = m2
    return mix

# ---------- UST（UTAU の楽譜）に書き出す ----------
def write_ust(song, path, index=0):
    vd = song["vocals"][index]
    notes = parse_notes(vd["notes"])
    lines = ["[#VERSION]", "UST Version1.2", "[#SETTING]", f"Tempo={float(song['bpm']):.2f}", "Tracks=1",
             f"ProjectName={song.get('title', 'song')}", "VoiceDir=%VOICE%重音テト", "OutFile=", "CacheDir=", "Tool1=wavtool.exe", "Tool2=resampler.exe", "Mode2=True"]
    prev_v = None; k = 0
    for n in notes:
        ln = int(round(n["len"] * 480))
        lines.append(f"[#{k:04d}]"); k += 1
        lines.append(f"Length={ln}")
        if n["lyric"] is None:
            lines += ["Lyric=R", "NoteNum=60"]; prev_v = None; continue
        ly = n["lyric"]
        if ly in ("ー", "-", "~"): ly = prev_v_kana(prev_v)
        lines += [f"Lyric={ly}", f"NoteNum={n['midi']}", f"Intensity={int(100 * n['vel'])}"]
        prev_v = vowel_of(n["lyric"], prev_v or "a")
    lines.append("[#TRACKEND]")
    open(path, "w", encoding="cp932", newline="\r\n").write("\n".join(lines) + "\n")

def prev_v_kana(v):
    return {"a": "あ", "i": "い", "u": "う", "e": "え", "o": "お", "n": "ん"}.get(v or "a", "あ")

def check(song):
    bad = 0
    for i, vd in enumerate(song.get("vocals", [])):
        bank = Bank(vd.get("voice", "teto"))
        notes = parse_notes(vd["notes"])
        pv = None; lo, hi = 999, 0
        for n in notes:
            if n["lyric"] is None: pv = None; continue
            lo, hi = min(lo, n["midi"]), max(hi, n["midi"])
            if n["lyric"] in ("ー", "-", "~"): continue
            o, _ = bank.pick(n["lyric"], pv)
            if o is None: print(f"× 歌 {i}: 「{n['lyric']}」が音源にありません（{n['beat']} 拍目）"); bad += 1
            pv = vowel_of(n["lyric"], pv or "a")
        beats = sum(n["len"] for n in notes)
        print(f"歌 {i}: {sum(1 for n in notes if n['lyric'])} 音・{beats:g} 拍・音域 MIDI {lo}〜{hi}")
    return bad

def main():
    a = sys.argv[1:]
    if len(a) < 2: print(__doc__); sys.exit(1)
    cmd, sp = a[0], a[1]
    song = json.load(open(sp, encoding="utf-8"))
    def opt(k, d=None):
        return a[a.index(k) + 1] if k in a else d
    if cmd == "check": sys.exit(1 if check(song) else 0)
    if cmd == "ust": write_ust(song, a[2], int(opt("--index", 0))); print("ok", a[2]); return
    if cmd == "render":
        sr = int(opt("--sr", 48000))
        v = render_song(song, sr, dry="--dry" in a)
        sf.write(a[2], v.astype(np.float32), sr, subtype="PCM_24"); print("ok", a[2]); return
    if cmd == "mix":
        acc, sr = sf.read(a[2], dtype="float64", always_2d=True)
        v = render_song(song, sr, total_sec=len(acc) / sr)
        n = len(acc)
        if len(v) < n: v = np.vstack([v, np.zeros((n - len(v), 2))])
        g = float(song.get("vocalLevel", 1.0))
        v = v[:n]
        # 歌の大きさを、伴奏の大きさに合わせて場所ごとに乗せる（ミックスのフェーダー操作のかわり）:
        #   2 秒ごとに「歌 − 伴奏」の差が +3dB（vocalLevel で上下）になるよう合わせ、なめらかにつなぐ
        win = int(2.0 * sr); hop = int(0.25 * sr)
        vm = np.abs(v).max(1); am = acc.mean(1); vv = v.mean(1)
        act = np.convolve((vm > 1e-3).astype(float), np.ones(int(0.05 * sr)), mode="same") > 0
        gains = []
        for i in range(0, n, hop):
            seg = slice(max(0, i - win // 2), min(n, i + win // 2))
            m = act[seg]
            if m.sum() < 0.2 * sr: gains.append(np.nan); continue
            ra = np.sqrt(np.mean(am[seg][m] ** 2)) + 1e-9; rv = np.sqrt(np.mean(vv[seg][m] ** 2)) + 1e-9
            gains.append(20 * np.log10(ra / rv) + 3.0 + 20 * math.log10(g))
        gd = np.array(gains)
        ok = ~np.isnan(gd)
        if ok.any():
            med = np.median(gd[ok]); gd = np.where(ok, np.clip(gd, med - 6, med + 6), np.interp(np.arange(len(gd)), np.where(ok)[0], gd[ok]))
            gd = np.convolve(np.pad(gd, 3, mode="edge"), np.ones(7) / 7, mode="valid")
            curve = np.interp(np.arange(n), np.arange(len(gd)) * hop, gd)
            v = v * (10 ** (curve / 20))[:, None]
        # 歌のすき間を空ける: 歌っている間だけ、伴奏の 1.5〜4kHz（言葉が聞こえる帯域）を少し下げる（最大 -3dB）
        b1, a1 = signal.butter(2, [1500 / (sr / 2), 4000 / (sr / 2)], "band")
        mid = signal.lfilter(b1, a1, acc, axis=0)
        env = np.convolve(act.astype(float), np.ones(int(0.15 * sr)) / int(0.15 * sr), mode="same")
        acc = acc - mid * (1 - 10 ** (-3 / 20)) * env[:, None]
        out = acc + v[:n]
        pk = np.max(np.abs(out))
        if pk > 0.98: out *= 0.98 / pk
        info = sf.info(a[2])
        sf.write(a[2], out, sr, subtype=info.subtype); print("ok 歌を混ぜました", a[2]); return
    print(__doc__); sys.exit(1)

if __name__ == "__main__":
    main()
