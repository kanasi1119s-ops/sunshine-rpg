#!/usr/bin/env python3
"""曲の「リズム」を数値で測る道具（2026-10-11）。参考にしたい録音を聴かずに調べるための、勉強用の分析。

使い方:
    python3 tools/audio-check/analyze-rhythm.py 曲.wav|mp3 [--bars 8-24]
測るもの（旋律・和音は測らない。曲を写すためではなく、リズムの作りと音の厚みを知るため）:
- テンポ（BPM）と、拍の位置のずれ
- ドラムの型: 帯域ごとの打点を、1小節16個の格子に当てはめる（low＝キック、mid＝スネア、high＝ハイハット・シンコペ）。
  ※ギターやベースの音も混ざるので、あくまで目安。x＝はっきり、o＝弱め
- 小節ごとの打点の例（--bars で範囲指定）と、全体でよく出る型（多数決）
- 4小節ごとの音量の起伏（セクションの強さの目安）
必要なもの: ffmpeg、numpy、scipy。
"""
import subprocess, sys
import numpy as np
from scipy.signal import stft

def load(path, sr=22050):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32), sr

def band_onsets(x, sr, hop=128):
    f, t, Z = stft(x, sr, nperseg=1024, noverlap=1024 - hop)
    S = np.log1p(np.abs(Z) * 30)
    out = {}
    for name, (lo, hi) in {"low": (35, 110), "mid": (1500, 5000), "high": (7000, 11000)}.items():
        m = (f >= lo) & (f < hi)
        e = S[m].mean(axis=0)
        d = np.maximum(0, np.diff(e, prepend=e[0]))
        out[name] = d
    return out, t, hop

def tempo_of(on, sr, hop):
    env = on["low"] + on["mid"] + on["high"]
    env = env - env.mean()
    ac = np.correlate(env, env, "full")[len(env) - 1:]
    fps = sr / hop
    best, bs = None, -1
    for bpm in np.arange(90, 240, 0.5):
        lag = fps * 60 / bpm
        i = int(round(lag))
        if i + 1 >= len(ac): continue
        s = ac[i] + 0.5 * ac[min(len(ac) - 1, 2 * i)]
        if s > bs: best, bs = bpm, s
    return best

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    rng = None
    if "--bars" in sys.argv:
        a, b = sys.argv[sys.argv.index("--bars") + 1].split("-"); rng = (int(a), int(b))
        args = [a for a in args if "-" not in a or "." in a]
    path = args[0]
    x, sr = load(path)
    on, t, hop = band_onsets(x, sr)
    fps = sr / hop
    bpm0 = tempo_of(on, sr, hop)
    n = len(on["low"])
    tot = on["low"] / (on["low"].std() + 1e-9) + on["mid"] / (on["mid"].std() + 1e-9)
    from scipy.ndimage import maximum_filter1d
    tm = maximum_filter1d(tot, 3)
    # 曲全体で拍の位置がいちばんよく合うテンポと開始位置を、細かく探す
    best_s, bpm, best = -1, bpm0, 0
    for cand in np.arange(bpm0 - 4, bpm0 + 4, 0.05):
        sb = fps * 60 / cand
        for off in np.arange(0, sb, 0.5):
            idx = (off + np.arange(0, int((n - off) / sb)) * sb).astype(int)
            sc = tm[idx[idx < n]].mean()
            if sc > best_s: best_s, bpm, best = sc, cand, off
    step = fps * 60 / bpm / 4
    bars = int((n - best) / step // 16)
    grid = {}
    for k, d in on.items():
        g = np.zeros((bars, 16))
        for b in range(bars):
            for i in range(16):
                c = int(best + (b * 16 + i) * step)
                g[b, i] = d[max(0, c - 2):c + 3].max() if c + 3 <= n else 0
        g /= np.percentile(g, 95) + 1e-9
        grid[k] = g
    print(f"曲: {path}\nテンポ: 約{bpm:.1f} BPM　小節数: 約{bars}　長さ: {len(x)/sr:.0f}秒")
    label = {"low": "low  (キック寄り)", "mid": "mid  (スネア寄り)", "high": "high (ハット寄り)"}
    def row(v): return "".join("x" if p > 0.55 else ("o" if p > 0.3 else ".") for p in v)
    print("\n== よく出る型（全小節の平均。目安）==")
    for k in ("low", "mid", "high"):
        print(f"{label[k]}  {row(grid[k].mean(axis=0) * 1.4)}")
    print("   拍:            1   2   3   4")
    lo, hi = rng if rng else (min(8, bars - 1), min(16, bars))
    print(f"\n== {lo}〜{hi}小節目の打点 ==")
    for b in range(lo, min(hi, bars)):
        print(f"{b+1:>3}小節  " + "  ".join(f"{k[0]}:{row(grid[k][b])}" for k in ("low", "mid", "high")))
    print("\n== 4小節ごとの音量（最大を0dB）==")
    spb = len(x) / sr / max(bars, 1)
    seg = []
    for b in range(0, bars, 4):
        a, c = int((best / fps + b * spb) * sr), int((best / fps + (b + 4) * spb) * sr)
        seg.append(20 * np.log10(np.sqrt(np.mean(x[a:c] ** 2)) + 1e-9))
    mx = max(seg)
    print(" ".join(f"{v - mx:+.0f}" for v in seg))

main()
