# 前奏が小さすぎるのを直す（2026-10-23 人間「前奏が小さすぎる曲があるから、作るときチェックして」）。使い方: python3 lm25_intro_lift.py <wav>（上書き）
# 曲の頭から、3秒ごとの大きさ（RMS）が「曲の真ん中の大きさ − GAP dB」に届くまでを前奏とみなし、そこが小さすぎれば
# 足りない分（最大 +MAX dB）を持ち上げ、前奏の終わりの2秒でなめらかに元へ戻す。わざと静かな始まりは残す（真ん中より GAP dB 下までは上げない）。
import sys, numpy as np, soundfile as sf
GAP, MAX = 9.0, 9.0
p = sys.argv[1]
x, sr = sf.read(p, always_2d=True)
m = x.mean(1); hop = sr * 3
rms = np.array([20 * np.log10(np.sqrt(np.mean(m[i:i + hop] ** 2)) + 1e-9) for i in range(0, len(m) - hop, hop)])
med = float(np.median(rms)); target = med - GAP
end = next((i for i, r in enumerate(rms) if r >= target), 0)
if end == 0:
    print(f"前奏の大きさ: そのまま（真ん中 {med:.1f} dB）"); sys.exit(0)
intro = float(np.mean(rms[:end])); gain = min(MAX, target - intro)
if gain < 1.0:
    print(f"前奏の大きさ: そのまま（前奏 {intro:.1f} / 真ん中 {med:.1f} dB）"); sys.exit(0)
g = np.ones(len(m)); a = end * hop; ramp = 2 * sr
g[:a] = 10 ** (gain / 20)
r0 = max(0, a - ramp); g[r0:a] = np.linspace(10 ** (gain / 20), 1.0, a - r0)
y = x * g[:, None]
peak = np.abs(y).max()
if peak > 0.98: y *= 0.98 / peak
sf.write(p, y, sr, subtype="PCM_16")
print(f"前奏を持ち上げました: 最初の {a / sr:.0f}秒 +{gain:.1f} dB（前奏 {intro:.1f} → 真ん中 {med:.1f} dB）")
