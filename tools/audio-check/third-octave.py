#!/usr/bin/env python3
"""音を1/3オクターブごとに測り、目標の形（既定: docs/sound/data/guitar-curve-5tracks.json）との差を出す。
使い方: python3 tools/audio-check/third-octave.py 書き出し.wav [目標.json]
        python3 tools/audio-check/third-octave.py 書き出し.wav --tilt -1.5      # 傾き(dB/オクターブ、1kHz=0)から目標を作って比べる
        python3 tools/audio-check/third-octave.py 書き出し.wav --family rock    # 家族別の傾き（docs/sound/data/mix-targets.json。pop・metal・orch なども別名で可）
差が + なら多すぎ、- なら足りない。ギターだけを書き出した wav で使う（音色合わせ用）。
--tilt／--family のときは、曲の各帯域を 1kHz の帯域に対する dB にして、目標（傾き × log2(f/1000)）と比べる（全体の帯域バランスの確認用。式は docs/sound/mix-patterns.md §3.0）。"""
import json, os, subprocess, sys
import numpy as np
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", sys.argv[1], "-ac", "1", "-ar", "44100", "-f", "f32le", "-"], capture_output=True, check=True).stdout
x = np.frombuffer(raw, dtype=np.float32)
spec = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
freq = np.fft.rfftfreq(len(x), 1 / 44100)
tot = spec.sum() + 1e-12
here = os.path.dirname(os.path.abspath(__file__))
if "--tilt" in sys.argv or "--family" in sys.argv:
    if "--family" in sys.argv:
        d = json.load(open(os.path.join(here, "../../docs/sound/data/mix-targets.json"), encoding="utf-8"))
        fam = sys.argv[sys.argv.index("--family") + 1]
        tilt = d["families"][d.get("aliases", {}).get(fam, fam)]["tilt_dB_oct"]
    else:
        tilt = float(sys.argv[sys.argv.index("--tilt") + 1])
    cs = [63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000]
    meas = {}
    for c in cs:
        m = (freq >= c / 2 ** (1 / 6)) & (freq < c * 2 ** (1 / 6))
        meas[c] = 10 * np.log10(spec[m].sum() / tot + 1e-12)
    print(f"目標の傾き {tilt} dB/oct（1kHz=0）\nHz   ours(1kHz基準)  target  diff")
    diffs = []
    for c in cs:
        t = tilt * np.log2(c / 1000.0)
        v = meas[c] - meas[1000]
        diffs.append(abs(v - t))
        print(f"{c:>6} {v:>10.1f} {t:>8.1f} {v - t:>+6.1f}")
    print("平均の絶対差 dB:", round(float(np.mean(diffs)), 1))
    sys.exit(0)
tgt = json.load(open(sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else os.path.join(here, "../../docs/sound/data/guitar-curve-5tracks.json")))["third_octave_dB"]
row = []
for c, t in tgt.items():
    c = float(c); m = (freq >= c / 2 ** (1 / 6)) & (freq < c * 2 ** (1 / 6))
    v = 10 * np.log10(spec[m].sum() / tot + 1e-12)
    row.append((int(c), round(float(v), 1), t, round(float(v - t), 1)))
print("Hz   ours  target  diff")
for r in row: print(f"{r[0]:>6} {r[1]:>6} {r[2]:>6} {r[3]:>+6}")
print("平均の絶対差 dB:", round(float(np.mean([abs(r[3]) for r in row])), 1))
