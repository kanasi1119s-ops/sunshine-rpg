# 曲全体の音の高さのバランスを、最後にまとめて整える（2026-10-26 人間「ミックスのバランスをよくするのが大事」
#   「パートごとに数値化して調整し、最後にまとめて調整」）。使い方: python3 vb25_tone.py <wav（上書き）>
# 品質チェック（vb25_qc.py）で、後半の曲に「こもり（200〜500Hz が多い）」「高域が暗い」「低音が出すぎ／細い」が多かった。
# 全体に対する帯域の割合（dB）を測り、目安の範囲から外れた分だけ、ゆるいイコライザーで寄せる（1つあたり最大 ±3dB。範囲内なら何もしない）:
#   こもり 200〜500Hz: −6.5 より多ければ 320Hz を下げる
#   低音 40〜120Hz: −9 より少なければ 70Hz の棚で上げる／−3 より多ければ下げる
#   空気 6〜10kHz: −17 より少なければ 7kHz からの棚で上げる／−10 より多ければ下げる
import sys, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, lfilter

p = sys.argv[1]
x, sr = sf.read(p, always_2d=True)
m = x.mean(1)
def db(v): return 10 * np.log10(np.mean(v ** 2) + 1e-12)
def band(v, lo, hi): return sosfilt(butter(4, [lo, hi], "bandpass", fs=sr, output="sos"), v)
tot = db(m)
mud, low, air = db(band(m, 200, 500)) - tot, db(band(m, 40, 120)) - tot, db(band(m, 6000, 10000)) - tot


def biquad(kind, f0, gain_db, q=0.7):
    A = 10 ** (gain_db / 40); w = 2 * np.pi * f0 / sr; c, s = np.cos(w), np.sin(w); al = s / (2 * q)
    if kind == "peak":
        b = [1 + al * A, -2 * c, 1 - al * A]; a = [1 + al / A, -2 * c, 1 - al / A]
    elif kind == "low":
        sq = 2 * np.sqrt(A) * al
        b = [A * ((A + 1) - (A - 1) * c + sq), 2 * A * ((A - 1) - (A + 1) * c), A * ((A + 1) - (A - 1) * c - sq)]
        a = [(A + 1) + (A - 1) * c + sq, -2 * ((A - 1) + (A + 1) * c), (A + 1) + (A - 1) * c - sq]
    else:
        sq = 2 * np.sqrt(A) * al
        b = [A * ((A + 1) + (A - 1) * c + sq), -2 * A * ((A - 1) + (A + 1) * c), A * ((A + 1) + (A - 1) * c - sq)]
        a = [(A + 1) - (A - 1) * c + sq, 2 * ((A - 1) - (A + 1) * c), (A + 1) - (A - 1) * c - sq]
    return np.array(b) / a[0], np.array(a) / a[0]


eqs = []
if mud > -6.5: eqs.append(("peak", 320, -min(3.0, mud + 6.5 + 0.5), 0.9))
if low < -9: eqs.append(("low", 70, min(3.0, -9 - low), 0.7))
elif low > -3: eqs.append(("low", 70, -min(3.0, low + 3), 0.7))
if air < -17: eqs.append(("high", 7000, min(3.0, -17 - air + 1), 0.7))
elif air > -10: eqs.append(("high", 7000, -min(3.0, air + 10), 0.7))
if not eqs:
    print(f"全体の音の高さのバランス: そのまま（こもり {mud:+.1f}・低音 {low:+.1f}・空気 {air:+.1f}）"); sys.exit(0)
y = x.copy()
for k, f0, g, q in eqs:
    b, a = biquad(k, f0, g, q)
    y = lfilter(b, a, y, axis=0)
pk = np.abs(y).max()
if pk > 0.97: y *= 0.97 / pk
sf.write(p, y, sr, subtype=sf.info(p).subtype)
print("全体の音の高さのバランス: " + "・".join(f"{f0}Hz {g:+.1f}dB" for k, f0, g, q in eqs) + f"（前 こもり {mud:+.1f}・低音 {low:+.1f}・空気 {air:+.1f}）")
