#!/usr/bin/env python3
"""音を1/3オクターブごとに測り、目標の形（既定: docs/sound/data/guitar-curve-5tracks.json）との差を出す。
使い方: python3 tools/audio-check/third-octave.py 書き出し.wav [目標.json]
差が + なら多すぎ、- なら足りない。ギターだけを書き出した wav で使う（音色合わせ用）。"""
import json, os, subprocess, sys
import numpy as np
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-ac", "1", "-ar", "44100", "-f", "f32le", "-"], capture_output=True, check=True).stdout
x = np.frombuffer(raw, dtype=np.float32)
spec = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
freq = np.fft.rfftfreq(len(x), 1 / 44100)
tot = spec.sum() + 1e-12
here = os.path.dirname(os.path.abspath(__file__))
tgt = json.load(open(sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "../../docs/sound/data/guitar-curve-5tracks.json")))["third_octave_dB"]
row = []
for c, t in tgt.items():
    c = float(c); m = (freq >= c / 2 ** (1 / 6)) & (freq < c * 2 ** (1 / 6))
    v = 10 * np.log10(spec[m].sum() / tot + 1e-12)
    row.append((int(c), round(float(v), 1), t, round(float(v - t), 1)))
print("Hz   ours  target  diff")
for r in row: print(f"{r[0]:>6} {r[1]:>6} {r[2]:>6} {r[3]:>+6}")
print("平均の絶対差 dB:", round(float(np.mean([abs(r[3]) for r in row])), 1))
