#!/usr/bin/env python3
"""音を「絵」にして目で確かめる道具（Claude Code が音を見るため）。
使い方: python3 tools/audio-check/see-audio.py <WAV> [--out 画像.png] [--start 秒] [--dur 秒] [--fmin 80] [--fmax 1400]
出すもの: (1) スペクトログラム（対数周波数） (2) ピッチ軌跡（自己相関。セントで表示） (3) 音量の動き
注意: 耳の代わりにはならない。「音程がどう揺れたか」「余韻が切れたか」など、数字で言えることを絵にするもの。"""
import sys, argparse, wave
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import signal

def load(path):
    import subprocess
    raw = subprocess.run(["ffmpeg","-v","error","-i",path,"-f","f32le","-ac","1","-ar","44100","-"],capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32), 44100

def pitch_track(x, sr, fmin, fmax, hop=441, win=4096):
    """正規化自己相関で基本周波数を追う（簡易 YIN 風）。返り値: 時間, 周波数(0=不明), 確信度"""
    n = (len(x) - win) // hop
    ts, fs, cs = [], [], []
    lo, hi = int(sr / fmax), int(sr / fmin)
    for i in range(max(n, 0)):
        seg = x[i*hop:i*hop+win] * np.hanning(win)
        if np.sqrt(np.mean(seg**2)) < 1e-4:
            ts.append(i*hop/sr); fs.append(0); cs.append(0); continue
        f = np.fft.rfft(seg, 2*win)
        ac = np.fft.irfft(np.abs(f)**2)[:hi+2]
        ac = ac / (ac[0] + 1e-12)
        k = lo + int(np.argmax(ac[lo:hi]))
        c = ac[k]
        if 1 <= k < len(ac)-1:  # 放物線補間
            a, b, d = ac[k-1], ac[k], ac[k+1]
            den = a - 2*b + d
            k = k + (0.5*(a-d)/den if den != 0 else 0)
        ts.append((i*hop+win/2)/sr); fs.append(sr/k if c > 0.5 else 0); cs.append(c)
    return np.array(ts), np.array(fs), np.array(cs)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav"); ap.add_argument("--out"); ap.add_argument("--start", type=float, default=0)
    ap.add_argument("--dur", type=float, default=12); ap.add_argument("--fmin", type=float, default=80)
    ap.add_argument("--fmax", type=float, default=1400); ap.add_argument("--title", default="")
    a = ap.parse_args()
    x, sr = load(a.wav)
    x = x[int(a.start*sr):int((a.start+a.dur)*sr)]
    t, f, c = pitch_track(x, sr, a.fmin, a.fmax)
    fig, ax = plt.subplots(3, 1, figsize=(13, 9), sharex=True, gridspec_kw={"height_ratios": [3, 2, 1]})
    fr, tt, S = signal.spectrogram(x, sr, nperseg=4096, noverlap=3584, window="hann")
    m = (fr > 60) & (fr < 8000)
    ax[0].pcolormesh(tt, fr[m], 10*np.log10(S[m]+1e-12), shading="auto", vmin=-110, vmax=-30, cmap="magma")
    ax[0].set_yscale("log"); ax[0].set_ylabel("Hz (log)"); ax[0].set_title(a.title or a.wav.split("/")[-1])
    ok = f > 0
    ref = np.nanmedian(f[ok]) if ok.any() else 440
    cents = np.where(ok, 1200*np.log2(np.where(ok, f, 1)/ref), np.nan)
    ax[1].plot(t, cents, ".", ms=3); ax[1].axhline(0, color="gray", lw=.5)
    ax[1].set_ylabel(f"cent (0={ref:.1f}Hz)"); ax[1].grid(alpha=.3)
    ax[1].set_ylim(-150, 150) if np.nanmax(np.abs(cents)) < 150 else None
    rms = np.sqrt(np.convolve(x**2, np.ones(1024)/1024, "same"))
    ax[2].plot(np.arange(len(x))/sr, 20*np.log10(rms+1e-6)); ax[2].set_ylabel("dBFS"); ax[2].set_xlabel("sec"); ax[2].grid(alpha=.3)
    plt.tight_layout(); out = a.out or a.wav.rsplit(".",1)[0] + ".see.png"
    plt.savefig(out, dpi=70); print(out)
    # 数字の要約
    if ok.sum() > 10:
        cc = cents[ok]
        print(f"基準 {ref:.1f}Hz  音程の振れ幅 p5〜p95: {np.nanpercentile(cc,5):.0f}〜{np.nanpercentile(cc,95):.0f} cent  標準偏差 {np.std(cc):.1f} cent  追えた割合 {ok.mean()*100:.0f}%")
main()
