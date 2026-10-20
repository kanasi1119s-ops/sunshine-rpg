# 曲の大きさの「山」をなだらかにする（ゆっくりしたボリューム操作。ミックスの人がフェーダーを手で動かすのと同じ）。
# 2026-10-20 人間「一曲の後半に行くにつれて音量が大きくなりすぎる傾向があるので注意してください」:
#   測ると、出だしから曲の2/3あたりまで 6〜8dB 大きくなっていた（楽器が増えるぶん）。
#   20秒くらいの長さで見た大きさを、曲全体のまん中の大きさに近づける（差の6割だけ戻す。上げるのは +3dB まで、下げるのは -5dB まで）。
#   最初の8秒（入り）と最後の12秒（終わり）は動かさない（静かに入る・消える表情を残す）。全体の大きさは元と同じにそろえ、ピークは -1.5dBFS 以下。
# 使い方: python3 level-ride.py <入力.wav> <出力.wav>
import sys, subprocess
import numpy as np

src, dst = sys.argv[1], sys.argv[2]
SR = 48000
info = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=sample_rate,channels", "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip().split(",")
SR, CH = int(info[0]), int(info[1])
raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", src, "-f", "f32le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, np.float32).reshape(-1, CH).astype(np.float64)
n = len(x); hop = SR // 2
mono = x.mean(axis=1)
# 0.5秒ごとの大きさ（dB）
frames = np.array([np.sqrt(np.mean(mono[i:i + hop] ** 2) + 1e-12) for i in range(0, n, hop)])
db = 20 * np.log10(frames + 1e-9)
def smooth(v, w):
    k = np.ones(w) / w; p = w // 2
    return np.convolve(np.pad(v, (p, w - 1 - p), mode="edge"), k, mode="valid")
loud = smooth(db, 40)                                  # 20秒の窓
active = db > (db.max() - 30)                          # 無音に近い所は数えない
target = np.median(loud[active])
gain_db = np.clip((target - loud) * 0.6, -5.0, 3.0)
t = np.arange(len(db)) * hop / SR; dur = n / SR
gain_db[t < 8] = gain_db[np.searchsorted(t, 8)] if (t >= 8).any() else 0
gain_db = np.where(t > dur - 12, gain_db[max(0, np.searchsorted(t, dur - 12) - 1)], gain_db)
gain_db = smooth(gain_db, 16)                          # 8秒でなめらかに
g = 10 ** (np.interp(np.arange(n) / SR, t, gain_db) / 20)
y = x * g[:, None]
# 全体の大きさを元にそろえる（RMS）。ピークは -1.5dBFS をこえないよう、こえる所だけ短く下げる
y *= np.sqrt(np.mean(x ** 2) / (np.mean(y ** 2) + 1e-12))
lim = 10 ** (-1.5 / 20); pk = np.abs(y).max(axis=1)
over = np.maximum(pk / lim, 1.0)
if over.max() > 1.0:
    # こえた所のまわり 10ms をなめらかに下げる（移動平均は累積和で速く）
    w = SR // 100; e = np.pad(over, (w, w), mode="edge"); c = np.concatenate([[0], np.cumsum(e)])
    env = (c[2 * w + 1:] - c[:-2 * w - 1]) / (2 * w + 1)
    env = np.maximum(env[:n], over); y /= env[:, None]
p = subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", str(CH), "-i", "-", "-c:a", "pcm_s24le", dst], input=y.astype(np.float32).tobytes())
ym = y.mean(axis=1); before = smooth(db, 60)[active]; after_db = 20 * np.log10(np.array([np.sqrt(np.mean(ym[i:i + hop] ** 2) + 1e-12) for i in range(0, n, hop)]) + 1e-9)
print(f"level-ride: 30秒の窓での大きさの幅 {before.max() - before.min():.1f}dB → {smooth(after_db, 60)[active].max() - smooth(after_db, 60)[active].min():.1f}dB")
