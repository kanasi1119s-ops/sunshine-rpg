#!/usr/bin/env python3
"""「本物らしさ」の数字を測る道具（2026-10-11）。曲（mp3/wav）から、人が演奏した曲と機械的な曲で差が出る数字だけを出す。
使い方: python3 realism.py 曲1.mp3 [曲2.wav ...] [--out 結果.json]
出す数字:
  lra_LU        ラウドネスレンジ（曲の中の強弱の幅）。市販の曲は 4〜8 LU くらい。1以下だと平ら
  range3s_dB    3秒ごとの大きさの、大きい所と小さい所の差（95%点 − 10%点）
  crest_dB      ピークと平均の差。小さいほど潰れている
  width         左右の広がり（0=真ん中のみ）
  timing_ms     音の出だしが16分のグリッドからずれる量の標準偏差。小さすぎる（<5ms）と機械的
  onset_var     出だしの強さのばらつき（変動係数）。小さすぎると機械的
必要なもの: ffmpeg, numpy。著作権: 数字だけを出す（CLAUDE.md 1-1）。
"""
import json, os, re, subprocess, sys
import numpy as np

SR = 22050


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2)


def lra(path):
    r = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.findall(r"LRA:\s+([\d.]+) LU", r)
    i = re.findall(r"\bI:\s+(-?[\d.]+) LUFS", r)
    return (float(m[-1]) if m else None), (float(i[-1]) if i else None)


def tempo_and_onsets(mono):
    hop = 256
    n = len(mono) // hop
    e = np.sqrt((mono[: n * hop].reshape(n, hop) ** 2).mean(axis=1))
    d = np.maximum(np.diff(np.log(e + 1e-5)), 0)
    thr = max(0.25, float(np.percentile(d, 92)))
    pk = [i for i in range(1, len(d) - 1) if d[i] > thr and d[i] >= d[i - 1] and d[i] >= d[i + 1]]
    t = np.array(pk) * hop / SR
    strengths = d[pk] if pk else np.array([])
    return t, strengths


def timing_jitter(t):
    if len(t) < 40:
        return None
    # テンポ候補ごとに、16分グリッドへの当てはまりを見る
    best = None
    for bpm in np.arange(70, 200, 0.5):
        g = 60.0 / bpm / 4
        ph = ((t / g) % 1.0)
        r = np.abs(np.mean(np.exp(2j * np.pi * ph)))
        if best is None or r > best[0]:
            best = (r, bpm, np.angle(np.mean(np.exp(2j * np.pi * ph))))
    _, bpm, ang = best
    g = 60.0 / bpm / 4
    off = ((t / g - ang / (2 * np.pi) + 0.5) % 1.0 - 0.5) * g * 1000
    off = off[np.abs(off) < g * 1000 * 0.45]
    return float(np.std(off)), float(bpm)


def measure(path):
    y = load(path)
    mono = y.mean(axis=1)
    out = {}
    out["lra_LU"], out["lufs"] = lra(path)
    win = 3 * SR
    lv = []
    for s in range(0, len(mono) - win, win):
        rms = np.sqrt(np.mean(mono[s:s + win] ** 2))
        lv.append(20 * np.log10(rms + 1e-9))
    lv = [v for v in lv if v > -60]
    if len(lv) >= 4:
        out["range3s_dB"] = round(float(np.percentile(lv, 95) - np.percentile(lv, 10)), 1)
    rms = np.sqrt(np.mean(mono ** 2))
    out["crest_dB"] = round(float(20 * np.log10(np.max(np.abs(mono)) / (rms + 1e-9))), 1)
    mid, side = (y[:, 0] + y[:, 1]) / 2, (y[:, 0] - y[:, 1]) / 2
    out["width"] = round(float(np.sqrt(np.mean(side ** 2)) / (np.sqrt(np.mean(mid ** 2)) + 1e-9)), 2)
    t, st = tempo_and_onsets(mono)
    tj = timing_jitter(t)
    if tj:
        out["timing_ms"], out["grid_bpm"] = round(tj[0], 1), tj[1]
    if len(st) > 20:
        out["onset_var"] = round(float(np.std(st) / (np.mean(st) + 1e-9)), 2)
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = None
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
        args = [a for a in args if a != out]
    res = {}
    for p in args:
        res[os.path.basename(p)] = measure(p)
        print(os.path.basename(p), json.dumps(res[os.path.basename(p)], ensure_ascii=False), flush=True)
    if out:
        json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
