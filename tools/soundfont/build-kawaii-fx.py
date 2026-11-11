# 使い方: python3 tools/soundfont/build-kawaii-fx.py [作業フォルダ]
# カワイイ・フューチャーベースの「かわいい効果音」と「電子ドラム」（2026-11-11 人間「電子系音源は Kawaii future bass 系に」「足しましょう」）。
# このプログラム自身で合成する（録音は使わない。CC0 扱い）。1つの音源（patch "kawaiiFx"・バンク1の 203）の、鍵盤ごとに別の音。
# 音程は変わらない（書いた鍵盤の音がそのまま鳴る）。パートには modulate: false を付ける。
#   効果音:  C4 泡の「ぽこ」  C#4 水滴の「ぴちょん」  D4 きらきら（上がる）  D#4 きらきら（下がる）  E4 「きゅっ」  F4 「ぴょん」（跳ねる）
#           F#4 白いノイズの上がる音（2秒）  G4 下がる音（2秒）  G#4 逆再生のシンバル風（1秒）
#   ドラム:  A4 キック（短く はじけて、低い尾）  A#4 スネア（明るい）  B4 クラップ（重ねた手拍子）  C5 指パッチン
#           C#5 閉じたハイハット  D5 開いたハイハット  D#5 リム（カチ）  E5 高いタム（ぽん）  F5 低いタム
#   2026-11-11 追加（人間「ブルーアーカイブで使われてそうなの追加して」＝学園もののゲームに多い、かわいい日常の曲と、激しい電子の戦いの曲の音）:
#           F#5 ハードなキック（歪ませた長い尾）  G5 インパクト（ドーン）  G#5 サブドロップ（低い音が落ちる）  A5 レーザー（ピュン）
#           A#5 レコードのパチパチ（3秒）  B5 タンバリン  C6 シェイカー  C#6 ウッドブロック（高い）  D6 ウッドブロック（低い）  D#6 グリッチ（細かく刻む）
import os, sys, subprocess
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

SR = 44100
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
WORK = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else "/tmp/kawaii-fx"
os.makedirs(WORK, exist_ok=True)
rng = np.random.default_rng(1111)


def t_(sec): return np.arange(int(sec * SR)) / SR
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], "band", fs=SR, output="sos"), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, "low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, "high", fs=SR, output="sos"), x)
def noise(n): return rng.standard_normal(n)
def sweep(f0, f1, t, curve=1.0):
    """f0 → f1 へ動く正弦波（curve<1 で はじめに速く動く）"""
    x = (t / t[-1]) ** curve; f = f0 * (f1 / f0) ** x
    return np.sin(2 * np.pi * np.cumsum(f) / SR)
def stereo(fn): return np.stack([fn(0), fn(1)], 1)


def bubble(side):                 # 泡: 短い正弦波が、下から上へ「ぽこ」
    t = t_(0.16); f0 = 420 + 30 * side
    return sweep(f0, f0 * 2.6, t, 0.7) * np.exp(-t / 0.035) * (1 - np.exp(-t / 0.002))

def drop(side):                   # 水滴: 高い音が少し下がってから上がる「ぴちょん」＋小さな残り
    t = t_(0.5); n = len(t)
    a = sweep(1500, 900, t_(0.03), 1.0) * np.exp(-t_(0.03) / 0.02)
    b = sweep(900 + 40 * side, 2400, t_(0.12), 0.6) * np.exp(-t_(0.12) / 0.04)
    x = np.zeros(n); x[:len(a)] += a; x[int(0.035 * SR):int(0.035 * SR) + len(b)] += b
    x[int(0.11 * SR):] += 0.25 * np.sin(2 * np.pi * 2400 * t[:n - int(0.11 * SR)]) * np.exp(-t[:n - int(0.11 * SR)] / 0.08)
    return x

def sparkle(up):
    def f(side):                  # きらきら: 高いベルの粒が、音階をかけ上がる（下りる）。左右で粒の時刻を少しずらす
        t = t_(1.4); n = len(t); x = np.zeros(n)
        notes = [1568, 1760, 2093, 2349, 2637, 3136, 3520, 4186, 4699, 5274]
        if not up: notes = notes[::-1]
        for i, fr in enumerate(notes):
            s0 = int((0.02 + i * 0.055 + 0.012 * side + rng.uniform(0, 0.008)) * SR); tt = t[:n - s0]
            g = np.sin(2 * np.pi * fr * tt) + 0.35 * np.sin(2 * np.pi * fr * 2.76 * tt) * np.exp(-tt / 0.05)
            x[s0:] += g * np.exp(-tt / 0.22) * (0.6 + 0.4 * i / 9 if up else 1.0 - 0.4 * i / 9)
        return x
    return f

def squeak(side):                 # きゅっ: 細い矩形波に近い音が、すばやく上がって止まる
    t = t_(0.14); ph = 2 * np.pi * np.cumsum(900 * (2400 / 900) ** ((t / t[-1]) ** 0.5)) / SR
    return np.tanh(3 * np.sin(ph + 0.2 * side)) * np.exp(-((t - 0.07) / 0.05) ** 2) * 0.8

def boing(side):                  # ぴょん: 上がりながら細かく揺れる
    t = t_(0.32); f = 300 * (1500 / 300) ** ((t / t[-1]) ** 0.8) * (1 + 0.06 * np.sin(2 * np.pi * 28 * t))
    return np.sin(2 * np.pi * np.cumsum(f) / SR + 0.3 * side) * np.exp(-t / 0.16) * (1 - np.exp(-t / 0.004))

def riser(side):                  # 上がる音: 白いノイズの帯が、低い所から高い所へ。だんだん大きく
    t = t_(2.0); n = len(t); x = noise(n); out = np.zeros(n); B = 16
    for i in range(B):
        a, b = i * n // B, (i + 1) * n // B; fc = 400 * (9000 / 400) ** (i / (B - 1))
        seg = bp(x[max(0, a - 2000):b], fc * 0.7, min(fc * 1.5, 18000))[-(b - a):]
        out[a:b] = seg
    return out * (t / 2.0) ** 2 * (1 - np.clip((t - 1.97) / 0.03, 0, 1))

def downer(side):                 # 下がる音: 正弦波が高い所から低い所へ落ちる＋ノイズが閉じる
    t = t_(2.0); n = len(t)
    return sweep(1400, 45, t, 0.5) * np.exp(-t / 0.9) * 0.9 + lp(noise(n), 1200) * np.exp(-t / 0.35) * 0.25

def revcym(side):                 # 逆再生のシンバル風: 高いノイズがふくらんで、ぴたりと止まる
    t = t_(1.0); n = len(t); x = hp(noise(n), 3500) + 0.5 * bp(noise(n), 6000, 11000)
    return x * (t / 1.0) ** 3

def kick(side):                   # キック: はじける頭（180→48Hz）と、短い低い尾。カワイイ系は短く軽め
    t = t_(0.42); body = sweep(180, 48, t, 0.25) * np.exp(-t / 0.14)
    click = hp(noise(len(t)), 2500) * np.exp(-t / 0.004) * 0.35
    return np.tanh(1.6 * body) + click

def snare(side):                  # スネア: 高めの胴（210Hz）と、明るいノイズ
    t = t_(0.3); n = len(t)
    tone = (np.sin(2 * np.pi * 210 * t) + 0.5 * np.sin(2 * np.pi * 330 * t)) * np.exp(-t / 0.06)
    nz = bp(noise(n), 1500, 9500) * np.exp(-t / 0.09)
    return tone * 0.7 + nz * 0.9

def clap(side):                   # クラップ: 3回の小さな打ち＋尾
    t = t_(0.35); n = len(t); x = np.zeros(n)
    for d in (0.0, 0.011, 0.023):
        s0 = int((d + 0.002 * side) * SR); tt = t[:n - s0]
        x[s0:] += bp(noise(n - s0), 1100, 6500) * np.exp(-tt / 0.008)
    return x + bp(noise(n), 1100, 6500) * np.exp(-t / 0.07) * 0.5 * (t > 0.03)

def snap(side):                   # 指パッチン
    t = t_(0.2); n = len(t)
    return bp(noise(n), 1900, 4200) * np.exp(-t / 0.014) + np.sin(2 * np.pi * 1500 * t) * np.exp(-t / 0.012) * 0.5

def hat_c(side):                  # 閉じたハイハット: とても短い高いノイズ
    t = t_(0.08); return hp(noise(len(t)), 7000) * np.exp(-t / 0.014)

def hat_o(side):                  # 開いたハイハット
    t = t_(0.5); return hp(noise(len(t)), 6000) * np.exp(-t / 0.13)

def rim(side):                    # リム: 「カチ」
    t = t_(0.08); return (np.sin(2 * np.pi * 1700 * t) + 0.6 * np.sin(2 * np.pi * 820 * t)) * np.exp(-t / 0.008) + hp(noise(len(t)), 5000) * np.exp(-t / 0.003) * 0.3

def tom(f0):
    def f(side):                  # タム: 音程が少し下がる「ぽん」
        t = t_(0.4); return sweep(f0 * 1.5, f0, t, 0.3) * np.exp(-t / 0.13) + hp(noise(len(t)), 3000) * np.exp(-t / 0.003) * 0.15
    return f


def hardkick(side):               # ハードなキック: 頭ははじけ、歪ませた低い尾が長くのびる（激しい電子の曲用）
    t = t_(0.6); body = sweep(260, 52, t, 0.2) * np.exp(-t / 0.3)
    return np.tanh(5.0 * body) * 0.8 + hp(noise(len(t)), 3000) * np.exp(-t / 0.003) * 0.4

def impact(side):                 # インパクト: 低い「ドーン」と、広がるノイズ
    t = t_(2.5); n = len(t)
    return sweep(90, 34, t, 0.3) * np.exp(-t / 0.7) * 1.2 + lp(noise(n), 2500 - 800 * side) * np.exp(-t / 0.5) * 0.5 + hp(noise(n), 4000) * np.exp(-t / 0.08) * 0.4

def subdrop(side):                # サブドロップ: 低い正弦波が、ゆっくり落ちていく
    t = t_(1.6); return sweep(110, 30, t, 0.8) * np.exp(-t / 0.9) * (1 - np.exp(-t / 0.01))

def laser(side):                  # レーザー: 高い所からすばやく落ちる「ピュン」
    t = t_(0.25); return np.tanh(2 * sweep(5200 - 200 * side, 380, t, 0.35)) * np.exp(-t / 0.09)

def vinyl(side):                  # レコードのパチパチ: 小さな粒のノイズと、うすいサー
    t = t_(3.0); n = len(t); x = np.zeros(n)
    for _i in range(150):
        s0 = int(rng.uniform(0, 2.95) * SR); L = int(rng.uniform(0.0004, 0.002) * SR)
        x[s0:s0 + L] += rng.uniform(0.2, 1.0) * rng.choice([-1, 1]) * np.hanning(L)
    return hp(x, 1200) + bp(noise(n), 300, 6000) * 0.02

def tamb(side):                   # タンバリン: 金属のじゃらっとした短い音
    t = t_(0.25); n = len(t); x = hp(noise(n), 5500) * (np.exp(-t / 0.05) + 0.5 * np.exp(-((t - 0.03) / 0.012) ** 2))
    return x + 0.25 * sum(np.sin(2 * np.pi * f * t) for f in (6200, 7400, 8900, 10300)) * np.exp(-t / 0.06)

def shaker(side):                 # シェイカー
    t = t_(0.12); return bp(noise(len(t)), 4000, 12000) * np.exp(-((t - 0.035) / 0.03) ** 2)

def wood(f0):
    def f(side):                  # ウッドブロック: 「コッ」
        t = t_(0.12); return (np.sin(2 * np.pi * f0 * t) + 0.4 * np.sin(2 * np.pi * f0 * 2.4 * t)) * np.exp(-t / 0.018) + hp(noise(len(t)), 4000) * np.exp(-t / 0.002) * 0.2
    return f

def glitch(side):                 # グリッチ: 同じ短い音を、だんだん細かく刻む
    t = t_(0.5); n = len(t); x = np.zeros(n); pos = 0.0; gap = 0.06
    while pos < 0.48:
        s0 = int(pos * SR); L = int(min(gap * 0.6, 0.03) * SR); tt = np.arange(L) / SR
        x[s0:s0 + L] += np.tanh(2 * np.sin(2 * np.pi * (880 + 220 * side) * tt)) * np.hanning(L)
        pos += gap; gap = max(0.014, gap * 0.84)
    return x


SOUNDS = [(60, "bubble", bubble), (61, "drop", drop), (62, "sparkle-up", sparkle(True)), (63, "sparkle-down", sparkle(False)), (64, "squeak", squeak),
          (65, "boing", boing), (66, "riser", riser), (67, "downer", downer), (68, "revcym", revcym),
          (69, "kick", kick), (70, "snare", snare), (71, "clap", clap), (72, "snap", snap), (73, "hat-closed", hat_c), (74, "hat-open", hat_o),
          (75, "rim", rim), (76, "tom-hi", tom(330)), (77, "tom-lo", tom(170)),
          (78, "hardkick", hardkick), (79, "impact", impact), (80, "subdrop", subdrop), (81, "laser", laser), (82, "vinyl", vinyl), (83, "tamb", tamb),
          (84, "shaker", shaker), (85, "wood-hi", wood(1250)), (86, "wood-lo", wood(820)), (87, "glitch", glitch)]
lines = []; longest = 0
for key, name, fn in SOUNDS:
    x = stereo(fn); x -= x.mean(0)
    x = x / (np.abs(x).max() + 1e-9) * 0.8
    f = int(0.004 * SR); x[-f:] *= np.linspace(1, 0, f)[:, None]
    sf.write(os.path.join(WORK, f"kawaii_{key}_{name}.wav"), x.astype(np.float32), SR, subtype="FLOAT")
    longest = max(longest, len(x) / SR)
    lines.append(f"<region> sample=kawaii_{key}_{name}.wav pitch_keycenter={key} lokey={key} hikey={key}")
open(os.path.join(WORK, "kawaii-fx.sfz"), "w").write("\n".join(lines) + "\n")
o = subprocess.run(["node", "tools/soundfont/sfz-to-sf3.mjs", os.path.join(WORK, "kawaii-fx.sfz"), "kawaii-fx", "--program", "203", "--seconds", f"{longest + 0.1:.1f}",
                    "--rr", "1", "--q", "6", "--release", "0.5", "--fade", "0.03", "--stereo"], cwd=ROOT, capture_output=True, text=True)
print((o.stdout.strip().splitlines() or [""])[-1], o.stderr[-300:])
