#!/usr/bin/env python3
# ケルト100曲の「場面の空気」: 本物の環境音の録音（BigSoundBank・CC0相当）を音楽の下に薄く敷く。
# 使い方: python3 c100_air.py 音楽.wav 空気.json 出力.wav
#   空気.json: {"pre": 3.0, "tail": 6.0, "layers": [{"file": "1046", "db": -20, "hp": 80, "lp": 9000, "lfo": [40, 0.35], "pan": 0.0, "wide": 0.012,
#                 "duck": 0.5, "start": 0, "end": null, "fade": 4}], "events": [{"t": 120, "file": "0222", "db": -24, "len": 8, "pan": 0.3, "seek": 10}]}
#   db = 音楽の大きさ（RMS）より何dB小さいか。duck = 音楽が大きいほど空気を下げる強さ（0〜1）。lfo = [周期秒, 深さ]
import sys, json, subprocess, os
import numpy as np
from scipy.signal import butter, sosfilt
SR = 44100
AMB = os.environ.get("AMB_DIR", "/home/claude/wt-mix/assets-src/ambience")

def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)

def clip(name):
    for ext in ("mp3", "wav", "ogg"):
        p = os.path.join(AMB, f"{name}.{ext}")
        if os.path.exists(p): return load(p)
    raise FileNotFoundError(name)

def loop_to(x, n, xf=3.0):
    """つなぎ目を等電力でクロスフェードして、n サンプルまで繰り返す"""
    L = len(x); k = int(min(xf * SR, L // 3))
    if L >= n: return x[:n]
    fi = np.sin(np.linspace(0, np.pi / 2, k))[:, None]; fo = np.cos(np.linspace(0, np.pi / 2, k))[:, None]
    out = x.copy()
    while len(out) < n:
        out = np.concatenate([out[:-k], out[-k:] * fo + x[:k] * fi, x[k:]])
    return out[:n]

def filt(x, hp=None, lp=None):
    if hp: x = sosfilt(butter(2, hp, "high", fs=SR, output="sos"), x, axis=0)
    if lp: x = sosfilt(butter(2, lp, "low", fs=SR, output="sos"), x, axis=0)
    return x

def rms_db(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)

def env_db(x, win=3.0):
    m = np.abs(x).mean(1); k = int(win * SR)
    e = np.sqrt(np.convolve(m ** 2, np.ones(k) / k, "same") + 1e-12)
    return 20 * np.log10(e)

def main(mus, spec, outp):
    M = load(mus); pre = int(spec.get("pre", 3.0) * SR); tail = int(spec.get("tail", 6.0) * SR)
    N = pre + len(M) + tail
    music = np.zeros((N, 2)); music[pre:pre + len(M)] = M
    ref = rms_db(M)
    e = env_db(music[::1]) ; med = np.median(e[pre:pre + len(M)])
    air = np.zeros((N, 2))
    for ly in spec["layers"]:
        x = loop_to(clip(ly["file"]), N)
        x = filt(x, ly.get("hp", 80), ly.get("lp", 9000))
        if ly.get("wide"):   # 左右を少しずらして、頭の外に広げる
            d = int(ly["wide"] * SR); x[:, 1] = np.roll(x[:, 1], d)
        pan = ly.get("pan", 0.0)
        x[:, 0] *= min(1, 1 - pan); x[:, 1] *= min(1, 1 + pan)
        x *= 10 ** ((ref + ly.get("db", -20) - rms_db(x)) / 20)
        t = np.arange(N) / SR
        g = np.ones(N)
        if ly.get("lfo"):
            per, dep = ly["lfo"]; g *= 1 - dep + dep * (0.5 + 0.5 * np.sin(2 * np.pi * t / per + ly.get("phase", 0)))
        du = ly.get("duck", 0.5)
        if du: g *= 10 ** (-du * np.clip(e - med, -6, 8) / 20)
        s0 = ly.get("start", 0) * SR; s1 = (ly.get("end") or (N / SR)) * SR; fd = ly.get("fade", 4) * SR
        w = np.clip((np.arange(N) - s0) / fd, 0, 1) * np.clip((s1 - np.arange(N)) / fd, 0, 1)
        air += x * (g * w)[:, None]
    for ev in spec.get("events", []):
        x = clip(ev["file"]); a = int(ev.get("seek", 0) * SR); n = int(ev.get("len", 8) * SR)
        x = filt(x[a:a + n], ev.get("hp", 120), ev.get("lp", 12000))
        x *= 10 ** ((ref + ev.get("db", -24) - rms_db(x)) / 20)
        f = min(len(x) // 3, int(1.5 * SR)); x[:f] *= np.linspace(0, 1, f)[:, None]; x[-f:] *= np.linspace(1, 0, f)[:, None]
        pan = ev.get("pan", 0.0); x[:, 0] *= min(1, 1 - pan); x[:, 1] *= min(1, 1 + pan)
        s = pre + int(ev["t"] * SR); air[s:s + len(x)] += x[:max(0, N - s)]
    out = music + air
    pk = np.abs(out).max()
    if pk > 0.98: out *= 0.98 / pk
    # 書き出し（16bit）
    import soundfile as sf
    sf.write(outp, out.astype(np.float32), SR, subtype="PCM_16")
    print(f"空気を重ねた: {outp}  音楽 {ref:.1f}dB・空気は音楽より約{ref - rms_db(air):.1f}dB 小さい・前 {pre / SR:g}秒・後 {tail / SR:g}秒")

if __name__ == "__main__":
    main(sys.argv[1], json.load(open(sys.argv[2])), sys.argv[3])
