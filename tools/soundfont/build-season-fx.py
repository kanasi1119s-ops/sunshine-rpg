# 使い方: python3 tools/soundfont/build-season-fx.py [作業フォルダ]
# 季節を感じる音と、小さな打楽器（2026-10-25 人間「季節を感じれる様な音も欲しい」）。このプログラム自身で合成する（録音は使わない。CC0 扱い）。
# 1つの音源（patch "seasonFx"・GM 105）の、鍵盤ごとに別の音。音程は変わらない（書いた鍵盤の音がそのまま鳴る）。長い音符で書くと最後まで鳴る。
#   C4 蝉（ミンミン系の鳴き声）  C#4 蝉（カナカナと下がる夕方の声）  D4 鈴虫（リーン）  D#4 コオロギ（コロコロ）
#   E4 雨（サーと降る雨と雨粒）  F4 風鈴  F#4 小鳥のさえずり  G4 波（寄せて返す）  G#4 雪の鈴（シャンシャン）
#   A4 秋風と落ち葉  A#4 春のそよ風  B4 手拍子  C5 カウベル  C#5 指パッチン  D5 花火（ドーン・パチパチ）
import os, sys, subprocess
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

SR = 44100
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
WORK = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else "/tmp/season-fx"
os.makedirs(WORK, exist_ok=True)
rng = np.random.default_rng(2026)


def t_(sec): return np.arange(int(sec * SR)) / SR
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], "band", fs=SR, output="sos"), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, "low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, "high", fs=SR, output="sos"), x)
def noise(n): return rng.standard_normal(n)
def stereo(fn):
    """左右で少し違う音（同じ作り方を2回、乱数を変えて）"""
    return np.stack([fn(0), fn(1)], 1)


def cicada(_):
    t = t_(6.0); n = len(t)
    # 「ミーン、ミンミン」: 0.35 秒の山を、少しずつ速くくり返す
    env = np.zeros(n); pos = 0.2
    while pos < 5.4:
        L = 0.42 if pos < 1.5 else 0.22
        k = (t > pos) & (t < pos + L); env[k] = np.sin(np.pi * (t[k] - pos) / L) ** 0.8
        pos += L + (0.12 if pos < 1.5 else 0.06)
    buzz = bp(noise(n), 3800, 6200, 2) * (0.6 + 0.4 * np.sin(2 * np.pi * 120 * t))
    tone = np.sin(2 * np.pi * (4300 + 300 * env) * t) * 0.4
    return (buzz + tone) * env * np.minimum(1, (5.8 - t) / 0.4).clip(0, 1)


def higurashi(_):
    t = t_(5.0); n = len(t); y = np.zeros(n)
    for i in range(10):
        st = 0.15 + i * 0.32; L = 0.26
        k = (t > st) & (t < st + L); tt = t[k] - st
        f = 4700 - i * 70
        y[k] += np.sin(2 * np.pi * f * tt) * (np.sin(2 * np.pi * 34 * tt) > -0.2) * np.exp(-tt / 0.18) * (1 - i / 14)
    return bp(y + bp(noise(n), 4000, 5500) * 0.05 * (y != 0), 3000, 7000)


def suzumushi(side):
    t = t_(6.0); n = len(t); y = np.zeros(n)
    st = 0.3 + 0.2 * side
    while st < 5.5:
        L = 0.55; k = (t > st) & (t < st + L); tt = t[k] - st
        y[k] += np.sin(2 * np.pi * 4450 * tt) * (0.55 + 0.45 * np.sin(2 * np.pi * 38 * tt)) * np.sin(np.pi * tt / L)
        st += L + 0.9 + 0.3 * rng.random()
    return y


def korogi(side):
    t = t_(6.0); n = len(t); y = np.zeros(n)
    st = 0.2 + 0.3 * side
    while st < 5.6:
        for j in range(3):
            s0 = st + j * 0.07; k = (t > s0) & (t < s0 + 0.045); tt = t[k] - s0
            y[k] += np.sin(2 * np.pi * 4900 * tt) * np.sin(np.pi * tt / 0.045)
        st += 0.55 + 0.25 * rng.random()
    return y


def rain(_):
    t = t_(8.0); n = len(t)
    pink = lp(noise(n), 5500, 1) * 0.5 + hp(noise(n), 3000) * 0.15
    drops = np.zeros(n)
    for _i in range(160):
        s0 = rng.random() * 7.8; f = 1800 + 2500 * rng.random(); k = (t > s0) & (t < s0 + 0.04); tt = t[k] - s0
        drops[k] += np.sin(2 * np.pi * f * (1 + 3 * tt) * tt) * np.exp(-tt / 0.008) * (0.3 + 0.7 * rng.random())
    e = np.minimum(1, t / 1.0) * np.minimum(1, (8 - t) / 1.0)
    return (pink + drops * 0.5) * e


def furin(side):
    t = t_(7.0); n = len(t); y = np.zeros(n)
    hits = [0.1, 1.6, 2.3, 4.1, 5.0] if side == 0 else [0.12, 1.62, 2.33, 4.12, 5.03]
    for i, s0 in enumerate(hits):
        k = t > s0; tt = t[k] - s0; g = (1.0, 0.6, 0.8, 0.5, 0.7)[i]
        for r, a, d in ((1, 1, 1.6), (2.76, 0.5, 0.9), (5.4, 0.25, 0.5), (8.93, 0.12, 0.3)):
            y[k] += np.sin(2 * np.pi * 2350 * r * (1 + 0.0007 * side) * tt) * a * np.exp(-tt / d) * g
    return y


def birds(side):
    t = t_(6.0); n = len(t); y = np.zeros(n)
    st = 0.3 + 0.4 * side
    while st < 5.5:
        for j in range(int(2 + 3 * rng.random())):
            s0 = st + j * 0.11; L = 0.07 + 0.04 * rng.random(); k = (t > s0) & (t < s0 + L); tt = t[k] - s0
            f0 = 3200 + 1800 * rng.random(); f = f0 + (1500 if rng.random() < 0.5 else -1200) * tt / L
            y[k] += np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / L)
        st += 0.8 + 0.8 * rng.random()
    return y


def waves(_):
    t = t_(8.0); n = len(t)
    sw = np.sin(np.pi * np.clip(t / 7.5, 0, 1)) ** 1.5
    x = noise(n); y = np.zeros(n)
    # カットオフが、寄せる波で上がり、返す波で下がる（ブロックごとに）
    B = 2048
    for i in range(0, n, B):
        fc = 300 + 2600 * sw[i]
        y[i:i + B] = lp(x[i:i + B], fc, 1)
    return y * (0.2 + 0.8 * sw)


def sleigh(_):
    t = t_(4.0); n = len(t); y = np.zeros(n)
    for i in range(16):
        s0 = 0.1 + i * 0.235 + 0.01 * rng.random(); k = t > s0; tt = t[k] - s0
        jing = sum(np.sin(2 * np.pi * f * tt) for f in (6200, 7400, 8900, 10300)) * np.exp(-tt / 0.08)
        y[k] += (jing * 0.25 + hp(noise(k.sum()), 6000) * np.exp(-tt / 0.03)) * (1.0 if i % 2 == 0 else 0.6)
    return y


def autumn(_):
    t = t_(8.0); n = len(t)
    wind = lp(noise(n), 600, 2) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.2 * t + rng.random()))
    rust = bp(noise(n), 1500, 4500) * (np.convolve((rng.random(n) < 0.0008).astype(float), np.exp(-np.arange(2000) / 300), "same")) * 3
    e = np.minimum(1, t / 1.5) * np.minimum(1, (8 - t) / 1.5)
    return (wind + rust * 0.4) * e


def breeze(_):
    t = t_(8.0); n = len(t)
    x = bp(noise(n), 400, 2500, 1) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.13 * t + rng.random())) ** 2
    return x * np.minimum(1, t / 2) * np.minimum(1, (8 - t) / 2)


def clap(_):
    t = t_(0.5); n = len(t); y = np.zeros(n)
    for j, s0 in enumerate((0, 0.009, 0.019)):
        k = t > s0; tt = t[k] - s0; y[k] += noise(k.sum()) * np.exp(-tt / (0.004 if j < 2 else 0.06))
    return bp(y, 900, 4500) + hp(y, 6000) * 0.2


def cowbell(_):
    t = t_(0.8)
    x = np.sign(np.sin(2 * np.pi * 540 * t)) + np.sign(np.sin(2 * np.pi * 800 * t))
    return bp(x, 500, 3500) * np.exp(-t / 0.18) * np.minimum(1, t / 0.001)


def snap(_):
    t = t_(0.3); n = len(t)
    return bp(noise(n), 1800, 4000) * np.exp(-t / 0.012) + np.sin(2 * np.pi * 1400 * t) * np.exp(-t / 0.01) * 0.5


def fireworks(side):
    t = t_(4.0); n = len(t)
    boom = lp(noise(n), 180, 2) * np.exp(-t / 0.5) * 6 + np.sin(2 * np.pi * (60 - 20 * t) * t) * np.exp(-t / 0.4)
    cr = np.zeros(n)
    for _i in range(220):
        s0 = 0.4 + 2.8 * rng.random() ** 0.7; k = (t > s0) & (t < s0 + 0.01); tt = t[k] - s0
        cr[k] += noise(k.sum()) * np.exp(-tt / 0.002)
    return boom + hp(cr, 2000) * 0.6


SOUNDS = [(60, "cicada", cicada), (61, "higurashi", higurashi), (62, "suzumushi", suzumushi), (63, "korogi", korogi),
          (64, "rain", rain), (65, "furin", furin), (66, "birds", birds), (67, "waves", waves), (68, "sleigh", sleigh),
          (69, "autumn", autumn), (70, "breeze", breeze), (71, "clap", clap), (72, "cowbell", cowbell), (73, "snap", snap), (74, "fireworks", fireworks)]
lines = []
longest = 0
for key, name, fn in SOUNDS:
    x = stereo(fn); x -= x.mean(0)
    x = x / (np.abs(x).max() + 1e-9) * 0.8
    f = int(0.004 * SR); x[-f:] *= np.linspace(1, 0, f)[:, None]
    sf.write(os.path.join(WORK, f"season_{key}_{name}.wav"), x.astype(np.float32), SR, subtype="FLOAT")
    longest = max(longest, len(x) / SR)
    lines.append(f"<region> sample=season_{key}_{name}.wav pitch_keycenter={key} lokey={key} hikey={key}")
open(os.path.join(WORK, "season-fx.sfz"), "w").write("\n".join(lines) + "\n")
o = subprocess.run(["node", "tools/soundfont/sfz-to-sf3.mjs", os.path.join(WORK, "season-fx.sfz"), "season-fx", "--program", "105", "--seconds", f"{longest + 0.1:.1f}",
                    "--rr", "1", "--q", "5", "--release", "0.8", "--fade", "0.05", "--stereo"], cwd=ROOT, capture_output=True, text=True)
print((o.stdout.strip().splitlines() or [""])[-1], o.stderr[-300:])
