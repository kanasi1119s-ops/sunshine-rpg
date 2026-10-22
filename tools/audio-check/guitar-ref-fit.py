# 使い方: python3 tools/audio-check/guitar-ref-fit.py <参考の guitar.wav> <こちらの guitar.wav> [出力.json]（どちらも demucs htdemucs_6s で分けた guitar）
# 参考とこちらの帯域ごとの差を、作曲ソフトの fx（highpass・eq の peaking・lowpass。WebAudio の biquad と同じ式）で埋める数値を探す
import sys, os, json, numpy as np
from scipy.optimize import minimize
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module
stats = import_module("guitar-ref-analyze").stats; BANDS = import_module("guitar-ref-analyze").BANDS
# from analyze import stats, BANDS

SR = 44100
f = np.array(BANDS, float)


def biq(kind, f0, gain_db=0.0, q=0.9):
    A = 10 ** (gain_db / 40); w0 = 2 * np.pi * f0 / SR; cw, sw = np.cos(w0), np.sin(w0)
    if kind in ("lowpass", "highpass"):
        alpha = sw / (2 * q)
        if kind == "lowpass": b = [(1 - cw) / 2, 1 - cw, (1 - cw) / 2]
        else: b = [(1 + cw) / 2, -(1 + cw), (1 + cw) / 2]
        a = [1 + alpha, -2 * cw, 1 - alpha]
    elif kind == "peaking":
        alpha = sw / (2 * q)
        b = [1 + alpha * A, -2 * cw, 1 - alpha * A]; a = [1 + alpha / A, -2 * cw, 1 - alpha / A]
    elif kind in ("lowshelf", "highshelf"):
        alpha = sw / 2 * np.sqrt(2)   # S=1
        s = 1 if kind == "lowshelf" else -1
        b = [A * ((A + 1) - s * (A - 1) * cw + 2 * np.sqrt(A) * alpha), s * 2 * A * ((A - 1) - s * (A + 1) * cw), A * ((A + 1) - s * (A - 1) * cw - 2 * np.sqrt(A) * alpha)]
        a = [(A + 1) + s * (A - 1) * cw + 2 * np.sqrt(A) * alpha, -s * 2 * ((A - 1) + s * (A + 1) * cw), (A + 1) + s * (A - 1) * cw - 2 * np.sqrt(A) * alpha]
    return np.array(b) / a[0], np.array(a) / a[0]


def resp_db(chain, freqs):
    z = np.exp(-1j * 2 * np.pi * freqs / SR)
    h = np.ones_like(freqs, dtype=complex)
    for k in chain:
        b, a = biq(*k)
        h *= (b[0] + b[1] * z + b[2] * z ** 2) / (a[0] + a[1] * z + a[2] * z ** 2)
    return 20 * np.log10(np.abs(h) + 1e-12)


def chain_of(p):
    hp, g1, f1, g2, f2, g3, f3, g4, f4, lp = p
    return [("highpass", hp, 0, 0.7), ("peaking", f1, g1, 0.9), ("peaking", f2, g2, 0.9), ("peaking", f3, g3, 0.9), ("peaking", f4, g4, 0.9),
            ("lowpass", lp, 0, 0.7), ("lowpass", lp, 0, 0.7)]


def fit(ref, ours):
    sr_, _ = stats(ref); so, _ = stats(ours)
    target = sr_ - so                      # こちらに足すべき差（形だけ。全体の大きさは問わない）
    w = np.where((f >= 80) & (f <= 8000), 1.0, 0.3)
    def loss(p):
        r = resp_db(chain_of(p), f)
        d = (r - target); d = d - np.average(d, weights=w)
        bad = sum(max(0, abs(p[i]) - 15) for i in (1, 3, 5, 7))
        return float(np.average(d ** 2, weights=w)) + 10 * bad
    p0 = [110, 3, 230, -10, 550, -8, 800, -5, 1800, 3500]
    best = None
    for hp0 in (90, 120, 150):
        for lp0 in (2800, 3500, 4500):
            p0[0], p0[9] = hp0, lp0
            bnds = [(60, 200), (-15, 15), (200, 350), (-15, 15), (350, 900), (-15, 15), (700, 2500), (-15, 15), (1200, 6000), (2000, 12000)]
            r = minimize(loss, p0, method="Powell", bounds=bnds, options={"maxiter": 20000, "xtol": 0.1, "ftol": 1e-4})
            if best is None or r.fun < best.fun: best = r
    p = best.x
    r = resp_db(chain_of(p), f); d = r - target; d -= np.average(d, weights=w)
    print("残りの差（dB、帯域ごと）:", " ".join(f"{int(c)}:{x:+.1f}" for c, x in zip(f, d)))
    hp, g1, f1, g2, f2, g3, f3, g4, f4, lp = p
    fx = [{"type": "filter", "kind": "highpass", "freq": round(hp, 1), "q": 0.7},
          {"type": "eq", "low": 0, "mid": round(g1, 2), "midHz": round(f1, 1), "high": 0},
          {"type": "eq", "low": 0, "mid": round(g2, 2), "midHz": round(f2, 1), "high": 0},
          {"type": "eq", "low": 0, "mid": round(g3, 2), "midHz": round(f3, 1), "high": 0},
          {"type": "eq", "low": 0, "mid": round(g4, 2), "midHz": round(f4, 1), "high": 0},
          {"type": "filter", "kind": "lowpass", "freq": round(lp, 1), "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": round(lp, 1), "q": 0.7}]
    print(json.dumps(fx, ensure_ascii=False))
    return fx


if __name__ == "__main__":
    fx = fit(sys.argv[1], sys.argv[2])
    if len(sys.argv) > 3: json.dump(fx, open(sys.argv[3], "w"), ensure_ascii=False)
