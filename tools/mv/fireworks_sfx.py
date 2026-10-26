#!/usr/bin/env python3
"""花火の効果音を合成で作る（2026-10-26 人間「花火の効果音って作れる？」）。録音の素材は使わない。
  launch … 打ち上げ「ヒュ〜」（笛のように上がる音＋火の粉のシュー）
  boom   … 開く「ドーン」（低い胴の音＋破裂の雑音＋遠くの山に返るこだま）
  crackle… 「パチパチ」（星が散るときの小さな破裂。左右にばらまく）
  full   … 3つを順に
使い方: python3 fireworks_sfx.py <出力フォルダ>"""
import sys, os, numpy as np, soundfile as sf
from scipy import signal
SR = 48000; rng = np.random.default_rng(7)
def bp(x, lo, hi, o=2): return signal.sosfilt(signal.butter(o, [lo, hi], "band", fs=SR, output="sos"), x, axis=0)
def lp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, "low", fs=SR, output="sos"), x, axis=0)
def hp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, "high", fs=SR, output="sos"), x, axis=0)
def env(n, a, d):
    t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
def reverb(x, sec=2.6, wet=0.35):
    n = int(sec * SR); t = np.arange(n) / SR
    ir = np.stack([rng.standard_normal(n), rng.standard_normal(n)], 1) * np.exp(-t / (sec / 5.5))[:, None]
    ir = lp(ir, 5000); ir[:int(0.02 * SR)] = 0; ir /= np.sqrt((ir ** 2).sum(0))
    y = np.stack([signal.fftconvolve(x[:, c], ir[:, c]) for c in range(2)], 1)
    out = np.zeros_like(y); out[:len(x)] = x
    return out * (1 - wet) + y * wet * 0.9
def resonate(src, fc, q):
    """雑音を、高さが動く細い共鳴（笛の管のような響き）に通す。fc と q はサンプルごとの配列"""
    y = np.zeros(len(src)); y1 = y2 = 0.0
    for i in range(len(src)):
        w = 2 * np.pi * fc[i] / SR; r = np.exp(-w / (2 * q[i]))
        y0 = src[i] * (1 - r) + 2 * r * np.cos(w) * y1 - r * r * y2
        y[i] = y0; y2, y1 = y1, y0
    return y
def launch(sec=2.0, kind="whistle"):
    """打ち上げの「ヒュ〜」。本物の笛（筒の中で火薬が燃える音）に近づけるため、
    きれいな正弦波ではなく、雑音を細い共鳴に通した「息の入った笛」の音にする。
      whistle … ヒュ〜〜（すっと上がる）
      warble  … ヒュルルル〜（回りながら上がるので、高さと大きさが細かくゆれる）
    最初に筒から出る小さな「ポン」、上がるにつれて遠くなる（高い音がこもり、小さくなる）"""
    n = int(sec * SR); t = np.arange(n) / SR; u = t / sec
    jit = lp(rng.standard_normal(n), 6) ; jit = jit / (np.abs(jit).max() + 1e-9)          # ゆっくりした揺らぎ（毎回少しちがう）
    f = 950 + 1550 * (1 - (1 - u) ** 1.6) + 25 * jit                                      # はじめ速く、上に行くほどゆっくり上がる
    am = np.ones(n)
    if kind == "warble":
        wr = 11 + 4 * u                                                                    # 回る速さが少しずつ上がる
        ph = 2 * np.pi * np.cumsum(wr) / SR
        f = f * (1 + 0.035 * np.sin(ph)); am = 0.62 + 0.38 * (0.5 + 0.5 * np.sin(ph + 0.6)) ** 1.5
    src = rng.standard_normal(n)
    tone = resonate(src, f, np.full(n, 70.0)) + 0.25 * resonate(src, 2 * f, np.full(n, 90.0))
    tone /= np.abs(tone).max() + 1e-9
    hiss = bp(rng.standard_normal(n), 2500, 8000) * 0.10                                   # 火の粉のかすかなシュー
    e = np.minimum(1, t / 0.12) ** 1.5 * (1 - 0.55 * u) * np.clip((sec - t) / 0.35, 0, 1) ** 1.3   # 遠ざかって小さく
    x = (tone * am * 0.8 + hiss) * e
    # 遠くなるほど高い音がこもる（前半はそのまま、後半ほど 9k→3.5k）
    k = np.clip((u - 0.35) / 0.6, 0, 1); x = x * (1 - k) + lp(x, 3800) * k
    pon = lp(rng.standard_normal(int(0.08 * SR)), 900) * env(int(0.08 * SR), 0.001, 0.018) * 0.9   # 筒から出る「ポン」
    x[:len(pon)] += pon
    pan = np.linspace(-0.2, 0.05, n)
    st = np.stack([x * np.sqrt(0.5 - pan / 2), x * np.sqrt(0.5 + pan / 2)], 1)
    return reverb(st, 2.2, 0.28)
def boom(sec=3.0):
    n = int(sec * SR); t = np.arange(n) / SR
    f = 46 + 30 * np.exp(-t / 0.06)                                                            # 胴の「ドン」
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.004, 0.45) * 0.9
    crack = lp(rng.standard_normal(n), 2500) * env(n, 0.001, 0.09) * 0.8                     # 破裂の「バン」
    rumble = lp(rng.standard_normal(n), 300) * env(n, 0.02, 0.9) * 0.6                        # 空気がふるえる低いゴロゴロ
    x = hp(body + crack + rumble, 32)
    st = np.stack([x, x], 1)
    echo = np.zeros_like(st); d = int(0.42 * SR); echo[d:] = lp(st[:-d], 900) * 0.35           # 山に返るこだま
    return reverb(st + echo, 3.2, 0.4)
def crackle(sec=2.2, count=170):
    n = int(sec * SR); x = np.zeros((n, 2))
    for _ in range(count):
        s = int(rng.beta(1.3, 2.6) * (n - 3000)); L = int(rng.uniform(0.002, 0.012) * SR)
        b = rng.standard_normal(L) * np.exp(-np.arange(L) / (L / 4)) * rng.uniform(0.2, 1.0)
        b = bp(b, rng.uniform(1500, 3500), 9000, 1)
        p = rng.uniform(-0.9, 0.9); x[s:s + L, 0] += b * np.sqrt(0.5 - p / 2); x[s:s + L, 1] += b * np.sqrt(0.5 + p / 2)
    x *= (1 - np.arange(n) / n)[:, None] ** 0.7
    return reverb(x * 0.9, 1.8, 0.3)
def norm(x, peak=0.8): return x / (np.abs(x).max() + 1e-9) * peak
out = sys.argv[1] if len(sys.argv) > 1 else "."; os.makedirs(out, exist_ok=True)
L, B, C = launch(), boom(), crackle(); LW = launch(kind="warble")
full = np.zeros((len(L) + int(0.1 * SR) + max(len(B), int(0.25 * SR) + len(C)), 2))
full[:len(L)] += norm(L, 0.35)
o = len(L) + int(0.1 * SR); full[o:o + len(B)] += norm(B, 0.85); full[o + int(0.25 * SR):o + int(0.25 * SR) + len(C)] += norm(C, 0.4)
for name, x in (("fireworks_launch", norm(L, 0.6)), ("fireworks_launch_warble", norm(LW, 0.6)), ("fireworks_boom", norm(B, 0.85)), ("fireworks_crackle", norm(C, 0.6)), ("fireworks_full", norm(full, 0.85))):
    sf.write(os.path.join(out, name + ".wav"), x.astype(np.float32), SR, subtype="PCM_24")
print("ok", out)
