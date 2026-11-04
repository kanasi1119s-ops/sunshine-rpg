# 曲の中で極端に小さい場面（曲全体の平均より 9dB 以上小さい所）を、平均 −7dB まで持ち上げる（前後 0.6 秒でなめらかに）。
# 使い方: python3 liftq.py <入りの mp3> <場面の .secs> <出す mp3>
import sys, json, subprocess, numpy as np
src, secs_p, dst = sys.argv[1:4]
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-f", "f32le", "-ac", "2", "-ar", "44100", "-"], capture_output=True).stdout
x = np.frombuffer(raw, np.float32).reshape(-1, 2).copy(); sr = 44100
secs = json.load(open(secs_p)); secs.append({"t": len(x) / sr, "name": "end"})
m = x.mean(1); tot = 20 * np.log10(np.sqrt(np.mean(m ** 2)))
g = np.zeros(len(x)); done = []
for i, s in enumerate(secs[:-1]):
    a, b = int(s["t"] * sr), int(secs[i + 1]["t"] * sr)
    if b - a < sr * 2 or s["name"].startswith("_"): continue
    d = 20 * np.log10(np.sqrt(np.mean(m[a:b] ** 2)) + 1e-9) - tot
    if d < -9:
        up = min(12.0, -7 - d); g[a:b] = up; done.append(f"{s['name']} {d:+.0f}dB→+{up:.1f}dB")
# なめらかに（0.6秒）
k = int(0.6 * sr); c = np.cumsum(np.concatenate([np.zeros(k // 2), g, np.full(k - k // 2, g[-1])]))
g = (c[k:] - c[:-k])[:len(g)] / k
y = x * (10 ** (g / 20))[:, None]
p = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ac", "2", "-ar", "44100", "-i", "-", "-af", "alimiter=limit=0.89:level=false",
                    "-c:a", "libmp3lame", "-b:a", "256k", dst], input=y.astype(np.float32).tobytes())
print(" / ".join(done) if done else "直す所なし")
