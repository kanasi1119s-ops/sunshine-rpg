# 前奏が小さすぎるのを直す（2026-10-23 人間「前奏が小さすぎる曲があるから、作るときチェックして」）。使い方: python3 lm25_intro_lift.py <wav>（上書き）
# 曲の頭から、3秒ごとの大きさ（RMS）が「曲の真ん中の大きさ − GAP dB」に届くまでを前奏とみなし、そこが小さすぎれば
# 足りない分（最大 +MAX dB）を持ち上げ、前奏の終わりの2秒でなめらかに元へ戻す。わざと静かな始まりは残す（真ん中より GAP dB 下までは上げない）。
# 2026-10-23 人間「01の前奏、音量マックスでも最初ほとんど聞こえない」（ベースだけの前奏。数字の RMS では -11dB だったが、
#   低い音は耳に小さく聞こえるので、もっと小さく感じる）→ 耳の感じ方に近い重み（K特性のまね: 100Hz より下を削り、高い方を少し足す）で測り、
#   GAP 9→6dB、MAX 9→12dB に。上げすぎて音が割れないよう、前奏の山（ピーク）が 0.97 を超えない所までにする
import sys, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
GAP, MAX = 6.0, 15.0   # 2026-10-24: 12 では、ハープだけの前奏（07）がまだ小さかった
p = sys.argv[1]
x, sr = sf.read(p, always_2d=True)
m0 = x.mean(1); hop = sr * 3
m = sosfilt(butter(2, 100, "highpass", fs=sr, output="sos"), m0)
m = m + 0.6 * sosfilt(butter(1, 2000, "highpass", fs=sr, output="sos"), m0)
rms = np.array([20 * np.log10(np.sqrt(np.mean(m[i:i + hop] ** 2)) + 1e-9) for i in range(0, len(m) - hop, hop)])
med = float(np.median(rms)); target = med - GAP
end = next((i for i, r in enumerate(rms) if r >= target), 0)
if end == 0:
    print(f"前奏の大きさ: そのまま（真ん中 {med:.1f} dB）"); sys.exit(0)
intro = float(np.mean(rms[:end])); gain = min(MAX, target - intro)
# 2026-10-24: 山（ピーク）で上げ幅を止めると、雨粒のような粒の立った前奏は +4dB ほどしか上がらず、まだ聞こえにくかった。
#   上げ幅は止めず、前奏の山だけをやわらかく丸める（tanh のソフトクリップ。0.9 を超える所だけ）
if gain < 1.0:
    print(f"前奏の大きさ: そのまま（前奏 {intro:.1f} / 真ん中 {med:.1f} dB）"); sys.exit(0)
# 2026-10-24: 3秒の窓だけで前奏の終わりを決めると、窓の途中でバンドが入った所まで +15dB 上がり、そこだけ大きく飛び出した（05）。
#   前奏の終わりは 0.25 秒の細かい窓で探し直し（目安より 3dB 小さい所に届いた瞬間）、そこまでに上げ幅を戻す
fine = int(sr * 0.25)
a = end * hop
for k in range(max(0, (end - 1) * hop), end * hop + hop, fine):
    seg_ = m[k:k + fine]
    if len(seg_) and 20 * np.log10(np.sqrt(np.mean(seg_ ** 2)) + 1e-9) >= target - 3:
        a = k; break
g = np.ones(len(m)); ramp = int(0.75 * sr)
g[:a] = 10 ** (gain / 20)
r0 = max(0, a - ramp); g[r0:a] = np.linspace(10 ** (gain / 20), 1.0, a - r0)
y = x * g[:, None]
seg = y[:a]
lim = 0.9
over = np.abs(seg) > lim
if over.any():
    seg[over] = np.sign(seg[over]) * (lim + (1 - lim) * np.tanh((np.abs(seg[over]) - lim) / (1 - lim)))
    y[:a] = seg
peak = np.abs(y).max()
if peak > 0.98: y *= 0.98 / peak
sf.write(p, y, sr, subtype="PCM_16")
print(f"前奏を持ち上げました: 最初の {a / sr:.0f}秒 +{gain:.1f} dB（前奏 {intro:.1f} → 真ん中 {med:.1f} dB）")
