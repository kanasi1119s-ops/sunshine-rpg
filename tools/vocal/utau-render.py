#!/usr/bin/env python3
"""UTAU 音源（oto.ini つきの声の素材）で、歌の旋律と歌詞（vocal モジュール）を歌わせて WAV にする。
UTAU の「リサンプラー（音の高さと長さを変える）」と「wavtool（音をつなぐ）」と同じ考え方を、WORLD（声の分析・合成）で行う。

  - 連続音（「a か」のように、前の母音から次の音へのつながりを録った素材）でつなぐ。
  - 息つぎのあとの歌い出しは、単独音（「- か」）を使う（連続音に歌い出しの素材がないため）。
  - フレーズの終わりには「a R」（母音を自然に切る素材）を付ける。
  - 音の高さの線: 音と音のあいだはなめらかに移る（大きく跳ぶほど少し長く）。長い音にだけビブラート。ほんの少しの揺らぎ。
  - 音源そのものは持ち込まない（規約で再配布が禁止されていることが多い）。--vb で手元のフォルダを指定する。

使い方:
  python3 tools/vocal/utau-render.py <vocal.py> --vb <連続音フォルダ> --head-vb <単独音フォルダ> --bpm 150 --out 歌.wav
     [--gain "0-8:0.9,32-48:1.0"]（小節ごとの音量。0始まり、終わりは含まない）[--cache <分析の置き場>]
"""
import argparse, hashlib, importlib.util, os
import numpy as np, pyworld as pw, soundfile as sf

FS = 44100
FP = 5.0  # WORLD のフレーム間隔（ミリ秒）

VOWEL = {}
for v, ks in {"a": "あかがさざただなはばぱまやらわゃぁ", "i": "いきぎしじちぢにひびぴみりぃ", "u": "うくぐすずつづぬふぶぷむゆるゅぅ",
              "e": "えけげせぜてでねへべぺめれぇ", "o": "おこごそぞとどのほぼぽもよろをょぉ"}.items():
    for k in ks: VOWEL[k] = v
VOWEL["ん"] = "n"

def vowel_of(kana):
    return VOWEL.get(kana[-1], "a")

def load_oto(d):
    raw = open(os.path.join(d, "oto.ini"), "rb").read()
    for enc in ("utf-8", "cp932"):
        try: txt = raw.decode(enc); break
        except UnicodeDecodeError: continue
    out = {}
    for line in txt.splitlines():
        if "=" not in line: continue
        f, rest = line.split("=", 1); p = rest.split(",")
        if len(p) < 6: continue
        alias = p[0] or os.path.splitext(f)[0]
        if alias in out: continue
        out[alias] = dict(wav=os.path.join(d, f), off=float(p[1]), con=float(p[2]), cut=float(p[3]), pre=float(p[4]), ovl=float(p[5]))
    return out

class Analyzer:
    def __init__(self, cache):
        self.cache = cache; self.mem = {}
        if cache: os.makedirs(cache, exist_ok=True)
    def get(self, wav):
        if wav in self.mem: return self.mem[wav]
        key = os.path.join(self.cache, hashlib.md5(wav.encode()).hexdigest() + ".npz") if self.cache else None
        if key and os.path.exists(key):
            z = np.load(key); r = (z["f0"], z["sp"], z["ap"])
        else:
            x, fs = sf.read(wav, dtype="float64")
            if x.ndim > 1: x = x.mean(axis=1)
            assert fs == FS, (wav, fs)
            f0, t = pw.harvest(x, fs, f0_floor=80, f0_ceil=900, frame_period=FP)
            sp = pw.cheaptrick(x, f0, t, fs); ap = pw.d4c(x, f0, t, fs)
            r = (f0, sp, ap)
            if key: np.savez(key, f0=f0, sp=sp, ap=ap)
        self.mem[wav] = r
        return r

def midi_of(p):
    pc = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[p[0]]; i = 1
    if p[1] in "#b": pc += 1 if p[1] == "#" else -1; i = 2
    return pc + 12 * (int(p[i:]) + 1)

def pitch_curve(notes, total_ms, seed=7):
    """5ミリ秒ごとの音の高さ（MIDI 単位、小数）。notes: [(開始ms, 長さms, midi)]"""
    n = int(total_ms / FP) + 2
    t = np.arange(n) * FP
    cur = np.full(n, float(notes[0][2]))
    # 階段（音の高さ）を置き、休みは前の音の高さのまま
    for i, (s, d, m) in enumerate(notes):
        e = notes[i + 1][0] if i + 1 < len(notes) else total_ms
        cur[(t >= s) & (t < e)] = m
    out = cur.copy()
    for i in range(1, len(notes)):
        ps, pd, pm = notes[i - 1]; s, d, m = notes[i]
        if s - (ps + pd) > 1: # 休みのあと: 少し下からそっと入る（30セント）
            k = (t >= s) & (t < s + 70)
            out[k] = m - 0.3 * (1 - (t[k] - s) / 70) ** 2
            continue
        iv = m - pm
        if iv == 0: continue
        w = min(130.0, 55 + 12 * abs(iv))          # 移り変わりの長さ（ms）
        c = s - 0.25 * w                            # 少し早めに動き始める
        k = (t >= c - w / 2) & (t < c + w / 2)
        x = (t[k] - (c - w / 2)) / w
        out[k] = pm + iv * (0.5 - 0.5 * np.cos(np.pi * x))
        if abs(iv) >= 3:                            # 大きく跳んだときだけ、ほんの少し行き過ぎて戻る
            k2 = (t >= c + w / 2) & (t < c + w / 2 + 90)
            y = (t[k2] - (c + w / 2)) / 90
            out[k2] += np.sign(iv) * 0.12 * np.sin(np.pi * y) * (1 - y)
    # ビブラート（長い音だけ。後半からゆっくりかける）
    for s, d, m in notes:
        if d < 330: continue
        vs = s + max(160, d * 0.4); ve = s + d
        k = (t >= vs) & (t < ve)
        tt = t[k] - vs
        amp = 0.28 * np.minimum(1, tt / 180) * np.minimum(1, (ve - t[k]) / 60)
        out[k] += amp * np.sin(2 * np.pi * 5.6 * tt / 1000)
    # ほんの少しの揺らぎ（ゆっくりした ±6 セント）
    rng = np.random.default_rng(seed)
    drift = np.convolve(rng.standard_normal(n), np.hanning(81) / np.hanning(81).sum(), mode="same")
    out += 0.06 * drift / (np.abs(drift).max() + 1e-9)
    return out

def render_seg(an, o, length_ms, pcurve, seg_start_ms, gain=1.0, keep_tail=False):
    """oto の1行を、長さ length_ms に伸ばし、pcurve の高さで鳴らす。"""
    f0, sp, ap = an.get(o["wav"])
    nfr = len(f0)
    a = int(o["off"] / FP)
    if o["cut"] < 0: b = int((o["off"] - o["cut"]) / FP)
    else: b = nfr - int(o["cut"] / FP)
    b = max(a + 4, min(nfr, b))
    seg_len = (b - a) * FP
    fixed = min(o["con"], seg_len - 10)
    m = max(2, int(length_ms / FP))
    j = np.arange(m) * FP
    if keep_tail or length_ms <= fixed or length_ms <= seg_len:
        src = np.minimum(j, seg_len - FP)
    else:
        src = np.where(j < fixed, j, fixed + (j - fixed) * (seg_len - fixed - FP) / (length_ms - fixed))
    fi = a + src / FP
    i0 = np.floor(fi).astype(int); fr = (fi - i0)[:, None]; i1 = np.minimum(i0 + 1, nfr - 1)
    sp2 = sp[i0] * (1 - fr) + sp[i1] * fr
    ap2 = ap[i0] * (1 - fr) + ap[i1] * fr
    voiced = f0[np.rint(fi).astype(int).clip(0, nfr - 1)] > 0
    ti = ((seg_start_ms + j) / FP).astype(int).clip(0, len(pcurve) - 1)
    hz = 440.0 * 2 ** ((pcurve[ti] - 69) / 12)
    f0t = np.where(voiced, hz, 0.0)
    y = pw.synthesize(np.ascontiguousarray(f0t), np.ascontiguousarray(sp2), np.ascontiguousarray(ap2), FS, FP)
    return y[: int(length_ms * FS / 1000)] * gain

def fade(y, fin_ms, fout_ms):
    n = len(y); a = min(n, int(fin_ms * FS / 1000)); b = min(n, int(fout_ms * FS / 1000))
    if a > 0: y[:a] *= np.linspace(0, 1, a) ** 0.8
    if b > 0: y[n - b:] *= np.linspace(1, 0, b) ** 0.8
    return y

def main():
    ap_ = argparse.ArgumentParser()
    ap_.add_argument("vocal"); ap_.add_argument("--vb", required=True); ap_.add_argument("--head-vb", required=True)
    ap_.add_argument("--bpm", type=float, required=True); ap_.add_argument("--out", required=True)
    ap_.add_argument("--gain", default=""); ap_.add_argument("--cache", default="")
    ap_.add_argument("--total-bars", type=int, default=0)
    a = ap_.parse_args()
    spec = importlib.util.spec_from_file_location("vocal", a.vocal); vocal = importlib.util.module_from_spec(spec); spec.loader.exec_module(vocal)
    oto = load_oto(a.vb); head = load_oto(a.head_vb); an = Analyzer(a.cache)
    beat = 60000.0 / a.bpm
    raw = vocal.notes()
    bars = a.total_bars or len(vocal.bars())
    total_ms = bars * 4 * beat + 2000
    gains = []
    for g in [x for x in a.gain.split(",") if x]:
        r, v = g.split(":"); s, e = r.split("-"); gains.append((int(s), int(e), float(v)))
    def bar_gain(start_beat):
        b = int(start_beat // 4)
        for s, e, v in gains:
            if s <= b < e: return v
        return 1.0
    notes = [(s * beat, d * beat, midi_of(p), k, bar_gain(s)) for s, d, p, k in raw]
    pc = pitch_curve([(s, d, m) for s, d, m, k, g in notes], total_ms)
    out = np.zeros(int(total_ms * FS / 1000) + FS)
    missing = set()
    for i, (s, d, m, k, g) in enumerate(notes):
        prev = notes[i - 1] if i else None
        nxt = notes[i + 1] if i + 1 < len(notes) else None
        connected_prev = prev is not None and s - (prev[0] + prev[1]) < 1
        connected_next = nxt is not None and nxt[0] - (s + d) < 1
        if connected_prev:
            o = oto.get(f"{vowel_of(prev[3])} {k}")
        else:
            o = head.get(f"- {k}") or head.get(k)
        if o is None:
            o = head.get(f"- {k}") or head.get(k); missing.add(k)
        start = s - o["pre"]
        # 次の音とのつなぎ
        if connected_next:
            no = oto.get(f"{vowel_of(k)} {nxt[3]}") or head.get(nxt[3])
            end = nxt[0] - no["pre"] + no["ovl"]; fout = max(10, no["ovl"])
        else:
            end = s + d - 30; fout = 40
        y = render_seg(an, o, end - start, pc, start, g)
        if not connected_prev:
            # 歌い出し（単独音）は連続音より少し小さいので 1.5dB 上げ、子音を 3dB 強めて言葉をはっきりさせる
            y *= 1.19
            nc = int((o["pre"] + 30) * FS / 1000); nr = int(0.03 * FS)
            env = np.ones(len(y)); env[:nc] = 1.41
            env[nc:nc + nr] = np.linspace(1.41, 1.0, len(env[nc:nc + nr]))
            y *= env
        y = fade(y, (o["ovl"] if connected_prev else 8), fout)
        p0 = int(start * FS / 1000)
        if p0 < 0: y = y[-p0:]; p0 = 0
        out[p0:p0 + len(y)] += y
        # フレーズの終わり: 母音を自然に切る素材（「a R」）
        if not connected_next:
            r = oto.get(f"{vowel_of(k)} R")
            if r:
                rs = s + d - 30 - r["ovl"]
                yr = render_seg(an, r, 260, pc, rs, g * 0.9, keep_tail=True)
                yr = fade(yr, r["ovl"], 120)
                q = int(rs * FS / 1000); out[q:q + len(yr)] += yr
    if missing: print("連続音が見つからず単独音で代用:", "".join(sorted(missing)))
    out = out[: int(total_ms * FS / 1000)]
    out *= 0.5 / (np.abs(out).max() + 1e-9)
    sf.write(a.out, out.astype(np.float32), FS, subtype="FLOAT")
    print("書き出し:", a.out, f"{len(out) / FS:.1f}秒", len(notes), "音")

if __name__ == "__main__":
    main()
