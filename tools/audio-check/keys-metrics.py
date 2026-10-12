#!/usr/bin/env python3
"""鍵盤・シンセの短いフレーズの WAV を、音の数値にする道具（2026-10-11）。keys-measure.mjs が呼ぶ。単独でも使える。
使い方: python3 tools/audio-check/keys-metrics.py 1.wav 2.wav ... [--table]   → JSON（ファイル名 → 数値）を標準出力に出す。--table は 1 行 1 音の表
測るもの:
- I（LUFS）・TP（dBTP）・PLR（TP − I。6 未満はつぶれ）・clip（|x|≥0.999 のサンプル数。0 でなければ割れ）
- bands: 帯域ごとの量（全体を 0dB とした dB）。sub 20-60 / bass 60-250 / lowmid 250-1k / mid 1k-4k / presence 4k-8k / air 8k-16k
- hi6k・hi10k: 6kHz 以上・10kHz 以上の量（全体に対する dB。−30 より大きいと高域が多い）
- harsh: 2〜5kHz の量 − 200Hz〜1kHz の量（dB。+3 を超えると刺さりやすい／−18 を下回るとこもりやすい）
- mud: 200〜500Hz の量 − 1〜4kHz の量（dB。+6 を超えるとこもりやすい）
- centroid: 音の重心（Hz）
- corr: 左右の相関（1＝モノ）、side_mid_dB: 横成分 − 中央成分（dB。−10 より大きいと広い）
- attack_ms: 最初の音の立ち上がり（10% → 最大までの ms）、decay_dBs: 最大の 0.1〜0.9 秒後の dB/秒の傾き（0 に近いほど伸びる）
"""
import json, re, subprocess, sys
import numpy as np

SR = 44100


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "quiet", "-i", path, "-map", "0:a:0", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)


def loudness(path):
    r = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    tail = r[r.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", tail)
    tp = re.search(r"Peak:\s+(-?[\d.]+) dBFS", tail)
    return (float(i.group(1)) if i else None), (float(tp.group(1)) if tp else None)


def band_db(spec, freq, lo, hi, tot):
    m = (freq >= lo) & (freq < hi)
    return 10 * np.log10(spec[m].sum() / tot + 1e-12)


def measure(path):
    x = load(path)
    mono = x.mean(axis=1)
    n = len(mono)
    spec = np.abs(np.fft.rfft(mono * np.hanning(n))) ** 2
    freq = np.fft.rfftfreq(n, 1 / SR)
    tot = spec.sum() + 1e-12
    bands = {k: round(float(band_db(spec, freq, lo, hi, tot)), 1) for k, (lo, hi) in {"sub": (20, 60), "bass": (60, 250), "lowmid": (250, 1000), "mid": (1000, 4000), "presence": (4000, 8000), "air": (8000, 16000)}.items()}
    e = lambda lo, hi: spec[(freq >= lo) & (freq < hi)].sum() + 1e-12
    I, TP = loudness(path)
    left, right = x[:, 0], x[:, 1]
    mid, side = (left + right) / 2, (left - right) / 2
    corr = float(np.corrcoef(left, right)[0, 1]) if left.std() > 0 and right.std() > 0 else 1.0
    # 立ち上がりと減衰（5ms の RMS の包絡線。最初の音）
    hop = int(SR * 0.005)
    env = np.sqrt(np.convolve(mono ** 2, np.ones(hop) / hop, mode="same"))[::hop]
    first = env[: int(0.9 / 0.005)]
    pk = int(np.argmax(first)) if len(first) else 0
    peak = first[pk] if len(first) else 0
    attack_ms = decay = None
    if peak > 1e-5:
        on = int(np.argmax(first >= 0.1 * peak))
        attack_ms = round((pk - on) * 5.0, 1)
        a, b = pk + int(0.1 / 0.005), min(pk + int(0.7 / 0.005), int(0.97 / 0.005))
        if b - a > 20:
            seg = 20 * np.log10(env[a:b] + 1e-9)
            decay = round(float(np.polyfit(np.arange(len(seg)) * 0.005, seg, 1)[0]), 1)
    return {
        "I": I, "TP": TP, "PLR": round(TP - I, 1) if I is not None and TP is not None else None,
        "clip": int((np.abs(x) >= 0.999).sum()), "seconds": round(n / SR, 1),
        "bands": bands,
        "hi6k": round(float(10 * np.log10(e(6000, 22000) / tot)), 1), "hi10k": round(float(10 * np.log10(e(10000, 22000) / tot)), 1),
        "harsh": round(float(10 * np.log10(e(2000, 5000) / e(200, 1000))), 1),
        "mud": round(float(10 * np.log10(e(200, 500) / e(1000, 4000))), 1),
        "centroid": int((freq * spec).sum() / spec.sum()),
        "corr": round(corr, 2), "side_mid_dB": round(float(10 * np.log10(((side ** 2).sum() + 1e-12) / ((mid ** 2).sum() + 1e-12))), 1),
        "attack_ms": attack_ms, "decay_dBs": decay,
    }


def table(results):
    """1 行 1 音の表（人が読む用）。"""
    head = f"{'id':16s} {'I':>6s} {'PLR':>5s} {'clip':>4s} {'cen':>5s} {'harsh':>6s} {'mud':>5s} {'hi6k':>6s} {'hi10k':>6s} {'corr':>5s} {'s-m':>5s} {'atk':>6s} {'dec':>6s} | sub  bass lowm  mid  pres  air"
    rows = [head]
    for k, m in results.items():
        b = m["bands"]
        f = lambda v, w, p=1: (f"{v:{w}.{p}f}" if v is not None else " " * (w - 1) + "-")
        rows.append(f"{k:16s} {f(m['I'], 6)} {f(m['PLR'], 5)} {m['clip']:4d} {m['centroid']:5d} {f(m['harsh'], 6)} {f(m['mud'], 5)} {f(m['hi6k'], 6)} {f(m['hi10k'], 6)} {f(m['corr'], 5, 2)} {f(m['side_mid_dB'], 5)} {f(m['attack_ms'], 6)} {f(m['decay_dBs'], 6)} | " + " ".join(f"{b[n]:5.1f}" for n in ("sub", "bass", "lowmid", "mid", "presence", "air")))
    return "\n".join(rows)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--table"]
    out = {}
    for p in args:
        out[p.split("/")[-1].rsplit(".", 1)[0]] = measure(p)
    print(table(out) if "--table" in sys.argv else json.dumps(out, ensure_ascii=False, indent=1))
