#!/usr/bin/env python3
"""仕上げが「全体の音量」を急に下げていないかを調べる（2026-11-17 人間「17の前奏のタッピングが急激に小さい音になるのって不自然」「今後絶対にやらないように」）。
使い方: python3 tools/vt3/gain_step_check.py <仕上げ前の音（/tmp/vp25/raw/*.flac）> <仕上げたあとの音（mp3）> [場面の秒 .secs]
やり方: 0.5 秒ごとに「仕上げたあと ÷ 仕上げ前」の大きさ（dB）を出す。これが仕上げのかけた音量の線。
        鳴りつづけている楽器は、この線が下がった分だけ小さく聞こえる。2 秒のあいだに 1.5dB 以上下がる所を「★ 下り段差」として出す（音が止まっている所は数えない）。
目安: 下り段差は 0 か所。出たら、仕上げで持ち上げるのをやめて、その楽器そのものの音量（パートの volume）で作り直す。"""
import sys, json, subprocess, tempfile, os
import numpy as np, soundfile as sf
from scipy import signal
def load(p):
    if p.endswith(".mp3"):
        t = tempfile.mktemp(suffix=".wav"); subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-ac", "1", "-ar", "24000", t]); x, sr = sf.read(t); os.remove(t); return x, sr
    x, sr = sf.read(p); x = x.mean(1) if x.ndim > 1 else x; return signal.resample_poly(x, 24000, sr), 24000
raw, sr = load(sys.argv[1]); fin, _ = load(sys.argv[2]); n = min(len(raw), len(fin)); raw, fin = raw[:n], fin[:n]
secs = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else []
sos = signal.butter(4, [200 / (sr / 2), 4000 / (sr / 2)], "band", output="sos"); raw = signal.sosfilt(sos, raw); fin = signal.sosfilt(sos, fin)
H = sr // 2; k = n // H
pr = np.array([np.mean(raw[i * H:(i + 1) * H] ** 2) for i in range(k)]); pf = np.array([np.mean(fin[i * H:(i + 1) * H] ** 2) for i in range(k)])
g = 10 * np.log10((pf + 1e-14) / (pr + 1e-14)); lv = 10 * np.log10(pr + 1e-14); ok = lv > np.percentile(lv, 95) - 45
def scene(t):
    nm = ""
    for s in secs:
        if s["t"] <= t + 1e-6: nm = s["name"]
    return nm
bad = []
for i in range(k - 4):
    if not ok[i]: continue
    j = [q for q in range(i + 1, i + 5) if ok[q]]
    if not j: continue
    d = min(g[q] - g[i] for q in j)
    if d <= -1.5: bad.append((i * 0.5, d))
# となり合う所をまとめる
out = []
for t, d in bad:
    if out and t - out[-1][1] <= 1.0: out[-1] = (out[-1][0], t, min(out[-1][2], d))
    else: out.append((t, t, d))
print(f"■ 仕上げの音量の線: いちばん高い所 {g[ok].max():+.1f}dB・いちばん低い所 {g[ok].min():+.1f}dB（鳴っている所だけ）")
if not out: print("  下り段差（2秒で 1.5dB 以上）: 0 か所（目安の内）")
else:
    print(f"  ★ 下り段差（2秒で 1.5dB 以上）: {len(out)} か所")
    for a, b, d in out: print(f"    {int(a // 60)}:{a % 60:04.1f}〜{int(b // 60)}:{b % 60 + 0.5:04.1f}  {d:+.1f}dB  {scene(a)}{'→' + scene(b + 2) if scene(b + 2) != scene(a) else ''}")
sys.exit(1 if out else 0)
