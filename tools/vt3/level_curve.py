#!/usr/bin/env python3
"""曲の大きさを2小節ごとに測って、場面の中での上下と、場面のあいだの差を見る（人間「全体の音チェックして、小さかったり大きかったりして違和感感じるよ」2026-11-19）
使い方: python3 tools/vt3/level_curve.py <mp3か wav> <場面の秒.json.secs> <BPM> [拍子=4]
出す物: 場面ごとの 平均・いちばん小さい2小節・いちばん大きい2小節／となりの2小節で 3dB 以上変わる所／曲全体の幅"""
import sys, json, subprocess, tempfile, os, numpy as np, soundfile as sf
import pyloudnorm as pyln
p, secs, bpm = sys.argv[1], json.load(open(sys.argv[2])), float(sys.argv[3]); beats = int(sys.argv[4]) if len(sys.argv) > 4 else 4
t = tempfile.mktemp(suffix=".wav"); subprocess.run(["ffmpeg", "-v", "error", "-y", "i" and "-i", p, "-ar", "44100", t]); y, sr = sf.read(t); os.remove(t)
m = pyln.Meter(sr, block_size=0.4); W = 2 * beats * 60 / bpm
def lv(a, b):
    x = y[int(a * sr):int(b * sr)]
    return m.integrated_loudness(x) if len(x) > sr * 0.5 else float("nan")
T = [s["t"] for s in secs] + [len(y) / sr]; allv = []; print("場面 | 平均 | 小さい2小節 | 大きい2小節 | 幅")
jumps = []
for i, s in enumerate(secs):
    a, b = T[i], T[i + 1]; ws = []; x = a
    while x + W * 0.9 <= b + 1e-6: ws.append((x, lv(x, min(b, x + W)))); x += W
    v = [w[1] for w in ws if np.isfinite(w[1]) and w[1] > -60]
    if not v: continue
    allv += [(s["name"], *w) for w in ws if np.isfinite(w[1]) and w[1] > -60]
    print(f"{s['name']} | {lv(a, b):.1f} | {min(v):.1f} | {max(v):.1f} | {max(v) - min(v):.1f}")
for (n1, t1, v1), (n2, t2, v2) in zip(allv, allv[1:]):
    if abs(v2 - v1) >= 3: jumps.append(f"  {int(t2 // 60)}:{t2 % 60:04.1f}  {v2 - v1:+.1f}dB  {n1}{' → ' + n2 if n2 != n1 else '（同じ場面の中）'}")
vv = [v for _, _, v in allv]; print(f"曲全体: いちばん小さい2小節 {min(vv):.1f}・いちばん大きい2小節 {max(vv):.1f}・幅 {max(vv) - min(vv):.1f}dB")
print(f"となりの2小節で 3dB 以上変わる所: {len(jumps)} か所"); print("\n".join(jumps))
