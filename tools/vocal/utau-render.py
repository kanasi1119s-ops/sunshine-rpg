#!/usr/bin/env python3
"""UTAU 音源（oto.ini つきの声の素材）で、歌の旋律と歌詞（vocal モジュール）を歌わせて WAV にする。
UTAU の「リサンプラー（音の高さと長さを変える）」と「wavtool（音をつなぐ）」と同じ考え方を、WORLD（声の分析・合成）で行う。

  - 連続音（「a か」のように、前の母音から次の音へのつながりを録った素材）でつなぐ。音源は優先順に複数指定でき、
    見つからない音は次の音源で探す（例: 滑らか音源 → 通常の連続音）。歌い出しは単独音（「- か」）。
  - フレーズの終わりには「a R」（母音を自然に切る素材）、フレーズの前には息（--breath の音源）を入れる。
  - 自然に聞こえるための工夫（2026-10-15 版。人間の指示「強弱がありすぎて聞きにくい」「自然な歌声に」）:
      1) 音ごとの音量をそろえる（母音の部分の大きさを測って同じにする。素材ごとの録音の大小を消す）
      2) つなぎ目は「同じ力」のクロスフェード（足したときにふくらんだりへこんだりしない）
      3) 最後に「ボーカルライド」（20ミリ秒ごとの大きさを、なめらかに目標へ寄せる。±4dB まで）
      4) 長い音は「スローモーションの引きのばし」ではなく、母音の安定した部分を半分の速さで行き来させる（声の細かな揺れが残る）
      5) 元の声の細かな音程の揺れ（±25 セントまで）を残す
      6) ビブラートは長い音の後半だけ・浅め
  - 音源そのものは持ち込まない（規約で再配布が禁止されていることが多い）。--vb で手元のフォルダを指定する。

使い方:
  python3 tools/vocal/utau-render.py <vocal.py> --vb <滑らか音源>:滑 --vb <連続音> --head-vb <単独音> [--breath <エクストラ>]
     --bpm 150 --out 歌.wav [--gain "0-8:0.95,..."]（小節ごとの音量。0始まり、終わりは含まない）[--cache <分析の置き場>]
"""
import argparse, hashlib, importlib.util, os
import numpy as np, pyworld as pw, soundfile as sf
from scipy.ndimage import median_filter, uniform_filter1d

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

class Banks:
    """優先順の音源の並び。find('a か') は最初に見つかった音源の行を返す。"""
    def __init__(self, specs):
        self.banks = []
        for s in specs:
            path, _, suf = s.partition(":") if not os.path.isdir(s) else (s, "", "")
            self.banks.append((load_oto(path), suf))
    def find(self, alias):
        for oto, suf in self.banks:
            o = oto.get(alias + suf)
            if o: return o
        return None

class Analyzer:
    def __init__(self, cache):
        self.cache = cache; self.mem = {}
        if cache: os.makedirs(cache, exist_ok=True)
    def get(self, wav):
        if wav in self.mem: return self.mem[wav]
        key = os.path.join(self.cache, hashlib.md5(wav.encode()).hexdigest() + ".npz") if self.cache else None
        if key and os.path.exists(key):
            z = np.load(key); f0 = z["f0"]; sp = np.exp(z["lsp"].astype(np.float64)); ap = z["ap"].astype(np.float64)
        else:
            x, fs = sf.read(wav, dtype="float64")
            if x.ndim > 1: x = x.mean(axis=1)
            assert fs == FS, (wav, fs)
            f0, t = pw.harvest(x, fs, f0_floor=80, f0_ceil=900, frame_period=FP)
            sp = pw.cheaptrick(x, f0, t, fs); ap = pw.d4c(x, f0, t, fs)
            if key: np.savez_compressed(key, f0=f0, lsp=np.log(sp + 1e-16).astype(np.float16), ap=ap.astype(np.float16))
        # 元の声の細かな音程の揺れ（セント）。なめらかな線（150ms の中央値）からのずれ
        dev = np.zeros(len(f0)); v = f0 > 0
        if v.sum() > 10:
            lf = np.where(v, np.log2(np.maximum(f0, 1)), np.nan)
            idx = np.arange(len(f0)); lf_f = np.interp(idx, idx[v], lf[v])
            dev = np.where(v, 1200 * (lf_f - median_filter(lf_f, size=31)), 0.0)
            dev = np.clip(dev, -25, 25)
        r = (f0, sp, ap, dev)
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
    for i, (s, d, m) in enumerate(notes):
        e = notes[i + 1][0] if i + 1 < len(notes) else total_ms
        cur[(t >= s) & (t < e)] = m
    out = cur.copy()
    for i in range(1, len(notes)):
        ps, pd, pm = notes[i - 1]; s, d, m = notes[i]
        if s - (ps + pd) > 1:   # 休みのあと: ほんの少し下からそっと入る（20セント）
            k = (t >= s) & (t < s + 60)
            out[k] = m - 0.2 * (1 - (t[k] - s) / 60) ** 2
            continue
        iv = m - pm
        if iv == 0: continue
        w = min(140.0, 60 + 12 * abs(iv))
        c = s - 0.25 * w
        k = (t >= c - w / 2) & (t < c + w / 2)
        x = (t[k] - (c - w / 2)) / w
        out[k] = pm + iv * (0.5 - 0.5 * np.cos(np.pi * x))
    for s, d, m in notes:   # ビブラート（長い音の後半だけ・浅め）
        if d < 380: continue
        vs = s + max(200, d * 0.45); ve = s + d
        k = (t >= vs) & (t < ve)
        tt = t[k] - vs
        amp = 0.22 * np.minimum(1, tt / 220) * np.minimum(1, (ve - t[k]) / 80)
        out[k] += amp * np.sin(2 * np.pi * 5.4 * tt / 1000)
    rng = np.random.default_rng(seed)
    drift = np.convolve(rng.standard_normal(n), np.hanning(101) / np.hanning(101).sum(), mode="same")
    out += 0.05 * drift / (np.abs(drift).max() + 1e-9)
    return out

def seg_bounds(o, nfr):
    a = int(o["off"] / FP)
    b = int((o["off"] - o["cut"]) / FP) if o["cut"] < 0 else nfr - int(o["cut"] / FP)
    return a, max(a + 4, min(nfr, b))

def render_seg(an, o, length_ms, pcurve, seg_start_ms, keep_tail=False, micro=0.6, vel=1.0):
    """oto の1行を、長さ length_ms に伸ばし、pcurve の高さで鳴らす。返り値: (音, 母音が始まる位置[サンプル])
    vel < 1 のときは、子音までの部分（固定範囲）を vel 倍の長さに縮める（UTAU の「子音速度」と同じ）。"""
    f0, sp, ap, dev = an.get(o["wav"])
    nfr = len(f0)
    a, b = seg_bounds(o, nfr)
    seg_len = (b - a) * FP
    fixed = min(o["con"], seg_len - 10)
    m = max(2, int(length_ms / FP))
    jr = np.arange(m) * FP                      # 実際の時間
    fx = fixed * vel
    j = np.where(jr < fx, jr / vel, jr - fx + fixed)   # 素材の上の時間（子音部分だけ縮めた分をもどす）
    length_ms = length_ms - fx + fixed
    R = seg_len - FP - fixed   # 母音の安定した部分の長さ
    if keep_tail or length_ms <= seg_len:
        src = np.minimum(j, seg_len - FP)
    elif R >= 120:
        # 半分の速さで、安定した部分を行き来する（ピンポン）。声の細かな揺れが残る
        u = np.maximum(0, j - fixed) * 0.5
        ph = np.mod(u, 2 * R); tri = np.where(ph < R, ph, 2 * R - ph)
        src = np.where(j < fixed, j, fixed + tri)
    else:
        src = np.where(j < fixed, j, fixed + (j - fixed) * (seg_len - fixed - FP) / (length_ms - fixed))
    fi = a + src / FP
    i0 = np.floor(fi).astype(int).clip(0, nfr - 1); fr = (fi - i0)[:, None]; i1 = np.minimum(i0 + 1, nfr - 1)
    sp2 = sp[i0] * (1 - fr) + sp[i1] * fr
    ap2 = ap[i0] * (1 - fr) + ap[i1] * fr
    ir = np.rint(fi).astype(int).clip(0, nfr - 1)
    voiced = f0[ir] > 0
    ti = ((seg_start_ms + jr) / FP).astype(int).clip(0, len(pcurve) - 1)
    cents = pcurve[ti] * 100 + micro * dev[ir] * (j >= fixed)
    hz = 440.0 * 2 ** ((cents / 100 - 69) / 12)
    f0t = np.where(voiced, hz, 0.0)
    y = pw.synthesize(np.ascontiguousarray(f0t), np.ascontiguousarray(sp2), np.ascontiguousarray(ap2), FS, FP)
    return y[: int(m * FP * FS / 1000)], int(fx * FS / 1000)

def fade(y, fin_ms, fout_ms):
    """同じ力のクロスフェード（sin/cos）"""
    n = len(y); a = min(n, int(fin_ms * FS / 1000)); b = min(n, int(fout_ms * FS / 1000))
    if a > 0: y[:a] *= np.sin(np.linspace(0, np.pi / 2, a))
    if b > 0: y[n - b:] *= np.cos(np.linspace(0, np.pi / 2, b))
    return y

def rms_db(y):
    return 20 * np.log10(np.sqrt(np.mean(y ** 2)) + 1e-9) if len(y) else -120

def ride(x, target_db, max_db=4.0, win_ms=20, smooth_ms=120, floor_db=-30):
    """ボーカルライド: 声のある所の大きさを、なめらかに目標へ寄せる（息・無音は持ち上げない）"""
    w = int(win_ms * FS / 1000)
    env = 10 * np.log10(uniform_filter1d(x ** 2, w) + 1e-12)
    active = env > target_db + floor_db
    g = np.where(active, np.clip(target_db - env, -max_db, max_db), 0.0)
    g = uniform_filter1d(g, int(smooth_ms * FS / 1000))
    return x * 10 ** (g / 20)

def main():
    ap_ = argparse.ArgumentParser()
    ap_.add_argument("vocal"); ap_.add_argument("--vb", action="append", required=True); ap_.add_argument("--head-vb", required=True)
    ap_.add_argument("--breath", default=""); ap_.add_argument("--bpm", type=float, required=True); ap_.add_argument("--out", required=True)
    ap_.add_argument("--gain", default=""); ap_.add_argument("--cache", default="")
    ap_.add_argument("--total-bars", type=int, default=0); ap_.add_argument("--no-ride", action="store_true")
    a = ap_.parse_args()
    spec = importlib.util.spec_from_file_location("vocal", a.vocal); vocal = importlib.util.module_from_spec(spec); spec.loader.exec_module(vocal)
    vcv = Banks(a.vb); head = Banks([a.head_vb]); an = Analyzer(a.cache)
    breath = load_oto(a.breath) if a.breath else {}
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
    TARGET = -20.0   # 母音の大きさの目標（dBFS）
    used = {"vcv": 0, "fallback": 0}; bi = 0  # used: 1番目の音源で見つかった数 / ほかの音源で代用した数
    # 先に、音ごとの素材と「子音速度」を決める。前の音が短くて、次の音の子音（先行発声 − オーバーラップ）が
    # 前の音の半分より長くはみ出すときは、子音部分を縮めて収める（UTAU の自動調整と同じ考え方。最小 0.4 倍）
    choice = []
    for i, (s, d, m, k, g) in enumerate(notes):
        prev = notes[i - 1] if i else None
        cprev = prev is not None and s - (prev[0] + prev[1]) < 1
        o = vcv.find(f"{vowel_of(prev[3])} {k}") if cprev else None
        if o is None: o = head.find(f"- {k}") or head.find(k)
        vel = 1.0
        if cprev:
            need = o["pre"] - o["ovl"]; allow = prev[1] * 0.5
            if need > allow: vel = max(0.4, allow / need)
        choice.append((o, vel, dict(o, pre=o["pre"] * vel, ovl=o["ovl"] * vel)))
    for i, (s, d, m, k, g) in enumerate(notes):
        prev = notes[i - 1] if i else None
        nxt = notes[i + 1] if i + 1 < len(notes) else None
        cprev = prev is not None and s - (prev[0] + prev[1]) < 1
        cnext = nxt is not None and nxt[0] - (s + d) < 1
        o0, vel, o = choice[i]
        if cprev:
            b0, suf0 = vcv.banks[0]
            used["vcv" if (f"{vowel_of(prev[3])} {k}" + suf0) in b0 else "fallback"] += 1
        start = s - o["pre"]
        if cnext:
            no = choice[i + 1][2]
            end = nxt[0] - no["pre"] + no["ovl"]; fout = max(15, no["ovl"])
        else:
            end = s + d - 30; fout = 50
        y, vstart = render_seg(an, o0, end - start, pc, start, vel=vel)
        # 1) 音ごとの音量をそろえる（母音の部分で測る）
        body = y[max(vstart, int(o["pre"] * FS / 1000)): len(y) - int(fout * FS / 1000)]
        lvl = rms_db(body if len(body) > FS // 50 else y)
        gain_db = np.clip(TARGET - lvl, -12, 12) + 20 * np.log10(g)
        y *= 10 ** (gain_db / 20)
        y = fade(y, (max(15, o["ovl"]) if cprev else 8), fout)
        p0 = int(start * FS / 1000)
        if p0 < 0: y = y[-p0:]; p0 = 0
        out[p0:p0 + len(y)] += y
        if not cnext:   # フレーズの終わり: 母音を自然に切る
            r = vcv.find(f"{vowel_of(k)} R")
            if r:
                rs = s + d - 30 - max(15, r["ovl"])
                yr, _ = render_seg(an, r, 240, pc, rs, keep_tail=True)
                yr *= 10 ** ((gain_db - 2) / 20)
                yr = fade(yr, max(15, r["ovl"]), 140)
                q = int(rs * FS / 1000); out[q:q + len(yr)] += yr
        # 息: 次の歌い出しまで 250ms 以上あいていれば、歌い出しの直前に小さく吸う
        if breath and nxt is not None and not cnext:
            gap = nxt[0] - (s + d)
            if gap >= 250:
                bo = breath.get(["息2", "息3", "息1"][bi % 3]); bi += 1
                if bo:
                    x, fs = sf.read(bo["wav"], dtype="float64")
                    if x.ndim > 1: x = x.mean(axis=1)
                    x = x[int(bo["off"] * FS / 1000):]
                    if bo["cut"] > 0: x = x[: max(1, len(x) - int(bo["cut"] * FS / 1000))]
                    L = int(min(gap - 120, 380) * FS / 1000)
                    x = x[:L].copy()
                    x *= 10 ** ((TARGET - 16 - rms_db(x)) / 20)
                    x = fade(x, 60, 80)
                    nh = vcv.find(f"- {nxt[3]}") or head.find(f"- {nxt[3]}")
                    be = nxt[0] - (nh["pre"] if nh else 30) - 20
                    q = int(be * FS / 1000) - len(x)
                    if q > 0: out[q:q + len(x)] += x
    out = out[: int(total_ms * FS / 1000)]
    if not a.no_ride:
        out = ride(out, TARGET)
    out *= 0.5 / (np.abs(out).max() + 1e-9)
    sf.write(a.out, out.astype(np.float32), FS, subtype="FLOAT")
    print("書き出し:", a.out, f"{len(out) / FS:.1f}秒", len(notes), "音", used)

if __name__ == "__main__":
    main()
