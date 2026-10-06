"""インスタ用の滝の動画の音（30秒）。雨・大滝のとどろき・雷を、乱数のざわめきから作る（素材は使わない）。
雷は、絵の稲妻と同じ時間に鳴る: 地面へ落ちる稲妻（5.2秒ごと）は近い雷鳴、雲の中の雷（3.3秒ごと）は遠いゴロゴロ。
絵の時間は now = 200 + 経過ミリ秒（reel.mjs と同じ）。"""
import numpy as np
from scipy.signal import butter, lfilter
from scipy.io import wavfile

SR = 48000
DUR = 30.0
N = int(SR * DUR)
rng = np.random.default_rng(2026)


def lp(x, hz, order=2):
    b, a = butter(order, hz / (SR / 2), "low")
    return lfilter(b, a, x)


def hp(x, hz, order=2):
    b, a = butter(order, hz / (SR / 2), "high")
    return lfilter(b, a, x)


def bp(x, lo, hi, order=2):
    b, a = butter(order, [lo / (SR / 2), hi / (SR / 2)], "band")
    return lfilter(b, a, x)


t = np.arange(N) / SR
out = np.zeros((N, 2))
# 大滝のとどろき（低い、ゆっくり波うつ）
for ch in range(2):
    roar = lp(rng.standard_normal(N), 380, 3) * (0.85 + 0.15 * np.sin(2 * np.pi * 0.07 * t + ch))
    out[:, ch] += roar * 0.55
# 雨（高めのざわめき＋ぱらぱら）
for ch in range(2):
    rain = bp(rng.standard_normal(N), 1500, 7000) * 0.22
    drops = np.zeros(N)
    idx = rng.integers(0, N, 2600)
    drops[idx] = rng.uniform(0.3, 1.0, idx.size) * rng.choice([-1, 1], idx.size)
    drops = hp(lp(drops, 6000), 1800) * 0.9
    out[:, ch] += rain + drops


def thunder(at_s, strength, far):
    """at_s 秒から鳴る雷。far なら、はじめの割れる音なしで、低いゴロゴロだけ。"""
    L = int(SR * (4.5 if not far else 3.2))
    s = int(at_s * SR)
    if s >= N:
        return
    e = min(N, s + L)
    k = np.arange(e - s) / SR
    noise = rng.standard_normal(e - s)
    rumble = lp(noise, 160 if far else 260, 3)
    env = np.exp(-k / (1.4 if not far else 1.1)) * (1 - np.exp(-k / 0.05))
    env *= 0.75 + 0.25 * np.sin(2 * np.pi * 1.7 * k)
    sig = rumble * env * strength * (2.2 if not far else 1.4)
    if not far:
        crack = hp(noise, 900) * np.exp(-k / 0.09) * strength * 0.8
        sig = sig + crack
    pan = rng.uniform(0.35, 0.65)
    out[s:e, 0] += sig * (1 - pan) * 1.6
    out[s:e, 1] += sig * pan * 1.6


now0 = 200
# 地面へ落ちる稲妻: now % 5200 == 0 のとき（光ってから少し遅れて鳴る）
k = (now0 // 5200) + 1
while True:
    at = (k * 5200 - now0) / 1000 + 0.25
    if at > DUR:
        break
    thunder(at, 1.0, False)
    k += 1
# 雲の中の雷: now % 3300 == 60（稲妻のコマ）のあたり
k = (now0 // 3300)
while True:
    at = (k * 3300 + 60 - now0) / 1000 + 0.6
    if at > DUR:
        break
    if at > 0:
        thunder(at, 0.45, True)
    k += 1
# はじめと終わりは、ゆっくり大きく・小さく
fade = np.minimum(1, np.minimum(t / 1.2, (DUR - t) / 1.5))[:, None]
out *= fade
out /= np.max(np.abs(out)) * 1.05
wavfile.write("storm.wav", SR, (out * 32767).astype(np.int16))
print("ok")
