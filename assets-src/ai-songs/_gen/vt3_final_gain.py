# 場面ごとの仕上げの大きさ（2026-11-12）。使い方: python3 vt3_final_gain.py <wav（上書き）> <secs> <gain（{"場面の名前": dB}）>
# 仕上げの最後に、場面ごとに全体（歌も伴奏も）を上げ下げする。場面の変わり目は 0.4 秒でなめらかにつなぐ。上げて 0.97 をこえたら、こえた所だけやわらかく抑える
import sys, json, numpy as np, soundfile as sf
p, sp, gp = sys.argv[1:4]
x, sr = sf.read(p, always_2d=True); st = sf.info(p).subtype; secs = json.load(open(sp)); G = json.load(open(gp))
g = np.ones(len(x))
for a, b in zip(secs, secs[1:]):
    db = G.get(a["name"], 0.0)
    if db: g[int(a["t"] * sr):int(b["t"] * sr)] = 10 ** (db / 20)
k = int(0.4 * sr); g = np.convolve(np.pad(g, k, mode="edge"), np.hanning(2 * k + 1) / np.hanning(2 * k + 1).sum(), "same")[k:-k]
y = x * g[:, None]; pk = np.abs(y).max()
if pk > 0.97:
    t = 0.85; a_ = np.abs(y); over = a_ > t
    y[over] = np.sign(y[over]) * (t + (0.97 - t) * np.tanh((a_[over] - t) / (0.97 - t)))
sf.write(p, y, sr, subtype=st)
print("  場面ごとの仕上げの大きさ:", {k_: v for k_, v in G.items() if v})
