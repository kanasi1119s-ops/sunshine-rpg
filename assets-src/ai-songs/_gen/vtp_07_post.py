"""ハニー・サワーの前奏の仕上げ（書き出した WAV にかける。2026-11-08 人間がえらんだ前奏「逆再生で吸い込む」）。
  python3 vtp_07_post.py <入力.wav> <出力.wav>
  1) 1〜4小節: 2番のポストサビ（65〜68小節）の4小節を逆再生にして重ねる。
     音量は -30dB から 0dB へ指数でふくらみ、こもった音（400Hz より上を切る）から 16kHz まで少しずつ開く ＝ 吸い込まれる感じ。
     最後の 30ms は短く消して、5小節目の頭（ドロップ）にぶつける
  2) 8小節目の前半2拍: テープが止まるように、再生の速さを 1 → 0 へ落とす（音の高さも一緒に下がる）。後半2拍（声だけの「はにさわ」）はそのまま
"""
import sys, numpy as np, soundfile as sf
from scipy import signal
BPM = 122.0; BEAT = 60 / BPM; BAR = 4 * BEAT
src, dst = sys.argv[1], sys.argv[2]
y, sr = sf.read(src, always_2d=True); y = y.astype(np.float64)
def S(t): return int(round(t * sr))
# 1) 逆再生
a0, a1 = S(64 * BAR), S(68 * BAR)
rev = y[a0:a1][::-1].copy(); n = len(rev); L = S(4 * BAR); rev = rev[:L]
x = np.linspace(0, 1, n)
gain = 10 ** ((-30 + 30 * x ** 1.6) / 20)
# 少しずつ開くローパス（ブロックごとに切りかえ、状態を引きつぐ）
out = np.zeros_like(rev); blk = 512; zi = None
for k in range(0, n, blk):
    fc = 400 * (16000 / 400) ** ((k / n) ** 1.3)
    b, a = signal.butter(2, min(fc, sr * 0.45) / (sr / 2))
    if zi is None: zi = np.stack([signal.lfilter_zi(b, a) * 0 for _ in range(rev.shape[1])], 1)
    seg = rev[k:k + blk]
    o = np.zeros_like(seg)
    for c in range(rev.shape[1]):
        o[:, c], zi[:, c] = signal.lfilter(b, a, seg[:, c], zi=zi[:, c])
    out[k:k + blk] = o
out *= gain[:, None]
fo = S(0.03); out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
fi = S(0.05); out[:fi] *= np.linspace(0, 1, fi)[:, None]
y[:n] += out
# 2) テープストップ（8小節目の前半2拍）
t0 = S(7 * BAR); T = S(2 * BEAT)
pos = np.cumsum(np.linspace(1, 0, T) ** 1.3)    # 読む位置（だんだん遅く）
pos = np.concatenate([[0], pos[:-1]])
seg = y[t0:t0 + T + S(1)].copy()
ts = np.empty((T, y.shape[1]))
for c in range(y.shape[1]): ts[:, c] = np.interp(pos, np.arange(len(seg)), seg[:, c])
# 止まる直前の高い音のザラつきを抑える（遅くなるほど上を切る）
env = np.ones(T); e = S(0.02); env[-e:] = np.linspace(1, 0, e)
y[t0:t0 + T] = ts * env[:, None]
# 後半2拍の頭は、楽器の残響の尾が急に戻らないよう 40ms でなじませる
k = S(0.04); y[t0 + T:t0 + T + k] *= np.linspace(0, 1, k)[:, None]
pk = np.abs(y).max()
if pk > 0.999: y *= 0.999 / pk
sf.write(dst, y, sr, subtype="PCM_24")
print(f"前奏の仕上げ: 逆再生 {n / sr:.2f}秒・テープストップ {T / sr:.2f}秒 → {dst}")
