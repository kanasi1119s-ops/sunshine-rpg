#!/usr/bin/env python3
"""花火の効果音を合成で作る（2026-10-26 人間「花火の効果音って作れる？」）。録音の素材は使わない。

2版目（同日、人間「音の感じが花火の音と根本的に違う」）。1版目は「ドン」を 46Hz の正弦波で作っていたため、
バスドラムのような楽器の音に聞こえていた。本物の花火の音は、楽器のような「音の高さ」を持たない。
次の3つでできている（屋外の爆発音の性質に合わせて作り直した）。
  1. 衝撃波 … 一瞬の空気の押し（N の字の形の波。数ミリ秒）。高さのない「バンッ」
  2. 距離   … 空気は高い音ほど吸いこむので、遠くの花火は高い音が削れて「ドーン」と丸くなる
  3. 反射   … 地面・建物・山に何度も当たって、遅れて不規則に返ってくる「…ゴロゴロゴロ」。これがいちばんの特徴
打ち上げの笛「ヒュ〜」も、正弦波ではなく、倍音の多い（少しかすれた）笛の音にし、同じ屋外の響きに通す。

  launch        … 筒から出る「ポンッ（ドン）」＋笛の「ヒュ〜〜〜」
  launch_plain  … 笛なし（「ポンッ」＋昇っていくかすかな「シュルル」）
  boom          … 開く「ドーン…ゴロゴロ」
  crackle       … 「パチパチパチ」（星が細かくはじける。1つ1つは 1 ミリ秒もない破裂）
  full          … 打ち上げ→ドーン→パチパチを順に
使い方: python3 fireworks_sfx.py <出力フォルダ>"""
import sys, os, numpy as np, soundfile as sf
from scipy import signal
SR = 48000; rng = np.random.default_rng(11)
def lp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, "low", fs=SR, output="sos"), x, axis=0)
def hp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, "high", fs=SR, output="sos"), x, axis=0)
def bp(x, lo, hi, o=2): return signal.sosfilt(signal.butter(o, [lo, hi], "band", fs=SR, output="sos"), x, axis=0)

def nwave(ms, rough=0.15):
    """衝撃波（N の字）: 一気に押して、まっすぐ引いて、ぷつっと戻る。長さ ms ミリ秒"""
    n = max(4, int(ms / 1000 * SR)); w = np.linspace(1, -1, n)
    w += rough * rng.standard_normal(n) * np.linspace(1, 0.3, n)
    return np.concatenate([w, np.zeros(int(0.002 * SR))])

def outdoor_ir(sec=5.0, dist=1.0, roll=1.0, seed=0):
    """屋外の響き（左右2ch）。dist: 遠さ（大きいほど高い音が削れる）、roll: ゴロゴロの多さ
    直接の音 → 地面の反射（すぐ後ろ）→ 建物・山からの不規則なこだま → 低くうなる長い尾"""
    r = np.random.default_rng(seed); n = int(sec * SR); ir = np.zeros((n, 2))
    ir[0] = 1.0
    g = int(r.uniform(0.004, 0.009) * SR); ir[g] += 0.55                     # 地面の反射
    # 不規則なこだま: 0.15〜3.5 秒に、まばらに。遅いものほど小さく暗い
    for _ in range(int(60 * roll)):
        t = r.gamma(2.0, 0.55) + 0.12
        if t >= sec - 0.2: continue
        i = int(t * SR); a = r.uniform(0.04, 0.22) * np.exp(-t / 1.3) * (1 if r.random() < 0.8 else -1)
        L = int(r.uniform(0.01, 0.06) * SR)                                     # こだま1つも少しにじむ
        sm = r.standard_normal(L) * np.exp(-np.arange(L) / (L / 3)); sm /= np.abs(sm).max()
        sm = lp(sm, r.uniform(300, 1500) / (1 + t))                             # 遠回りしたものほど暗い
        p = r.uniform(-0.8, 0.8)
        ir[i:i + L, 0] += sm * a * np.sqrt(0.5 - p / 2); ir[i:i + L, 1] += sm * a * np.sqrt(0.5 + p / 2)
    # 低くうなる長い尾（ゴロゴロ）: ゆっくり大きさがゆれる低い雑音
    t = np.arange(n) / SR
    m = lp(r.standard_normal(n), 3.0); m /= m.std() + 1e-9
    am = np.clip(0.65 + 0.35 * m, 0.1, 1.5)
    tail = lp(r.standard_normal((n, 2)), 260, 3) * (am * np.minimum(1, t / 0.25) * np.exp(-t / (0.9 * roll + 0.4)))[:, None]
    tail /= np.sqrt((tail ** 2).sum(0)).max() + 1e-9
    ir += tail * 0.22 * roll
    ir = lp(ir, 9000 / dist, 1)                                                 # 空気が高い音を吸う
    return ir

def conv(x, ir):
    if x.ndim == 1: x = np.stack([x, x], 1)
    return np.stack([signal.fftconvolve(x[:, c], ir[:, c]) for c in range(2)], 1)

def boom(dist=1.4, roll=1.0, seed=1):
    """開く「ドーン…ゴロゴロ」。衝撃波を、遠さで丸くして、屋外の響きに通す"""
    src = np.zeros(int(0.08 * SR))
    for k in range(3):                                                          # 大玉は割れる瞬間が少しだけずれて重なる
        w = nwave(rng.uniform(5, 9)) * (1, 0.5, 0.3)[k]; o = int(rng.uniform(0, 0.006) * SR) * k
        src[o:o + len(w)] += w
    src = lp(src, 3500 / dist, 2) + 0.25 * hp(lp(src, 7000 / dist), 1500)    # 遠いほど高い音が削れる。破裂の「パ」も少し残す
    m = len(src); cr = hp(rng.standard_normal(m), 900) * np.exp(-np.arange(m) / (0.012 * SR)) * 0.35   # 破裂の「パンッ」（はじけた瞬間の乾いた音）
    src = src + lp(cr, 6000 / dist)
    y = conv(src, outdoor_ir(5.5, dist, roll, seed))
    y = hp(y, 28)
    # 星が飛び散る「シャー」（燃えながら散る火の粉）をうすく
    n = len(y); t = np.arange(n) / SR
    sh = bp(rng.standard_normal((n, 2)), 1500, 6000) * (np.minimum(1, t / 0.3) * np.exp(-t / 1.0))[:, None] * 0.012
    return y + sh

def whistle(sec=2.3):
    """笛の「ヒュ〜〜〜」。倍音が多く、少しかすれる。高さは、高い所から、はじめ速く・あとはゆっくり下がる"""
    n = int(sec * SR); t = np.arange(n) / SR; u = t / sec
    # 高い所から下がっていく（人間「このヒューが音逆なんじゃないかな」→ 1・2版目は上がっていたので逆にした。
    #   笛の筒は、燃えて空いた所が長くなるほど低く鳴り、遠ざかる玉の音も少し低く聞こえる）
    f0 = 2350 - 1350 * (1 - np.exp(-u * 1.8)) / (1 - np.exp(-1.8))
    f0 *= 1 + 0.006 * lp(rng.standard_normal(n), 25) / 0.02                    # 燃え方のむらで高さが細かくふるえる
    ph = 2 * np.pi * np.cumsum(f0) / SR
    tone = sum(np.sin(k * ph) / k ** 1.25 for k in range(1, 9))
    rasp = 1 + 0.35 * lp(rng.standard_normal(n), 900) / 0.1                    # かすれ（息の入った感じ）
    tone = tone * np.clip(rasp, 0, 2)
    tone = lp(tone, 7000) + 0.12 * bp(rng.standard_normal(n), 2000, 7000)
    e = np.minimum(1, t / 0.08) * (1 - 0.5 * u) * np.clip((sec - t) / 0.18, 0, 1)
    return tone * e / np.abs(tone).max()

def launch(kind="whistle"):
    """筒から出る「ポンッ」→（笛）→ 上がるにつれて遠く・暗く"""
    pon = lp(nwave(4.0, 0.3), 700, 2) * 1.0                                      # 筒の中から出るので、こもった低い「ポンッ」
    if kind == "whistle":
        w = whistle(); gap = int(0.05 * SR)
    else:                                                                        # 笛なし: 昇っていくかすかな「シュルル」
        sec = 2.0; n = int(sec * SR); t = np.arange(n) / SR
        w = bp(rng.standard_normal(n), 900, 4000) * (0.5 + 0.5 * np.sin(2 * np.pi * (7 + 3 * t / sec) * t)) ** 2
        w *= np.minimum(1, t / 0.1) * np.exp(-t / 0.9) * 0.35; gap = int(0.03 * SR)
    x = np.zeros(len(pon) + gap + len(w)); x[:len(pon)] += pon; x[len(pon) + gap:] += w * 0.5
    u = np.clip(np.arange(len(x)) / len(x), 0, 1)
    x = x * (1 - u * 0.6) + lp(x, 2500) * u * 0.6                               # 遠ざかるほど暗く
    y = conv(x, outdoor_ir(2.2, 1.0, 0.45, 2)); return y[:len(x) + int(1.2 * SR)] * np.clip((len(x) + int(1.2 * SR) - np.arange(len(x) + int(1.2 * SR)))[:, None] / (0.6 * SR), 0, 1)

def crackle(sec=2.4, count=420):
    """「パチパチ」: 1 ミリ秒もない小さな衝撃波を、空いっぱいにばらまく。はじめ多く、だんだんまばらに"""
    n = int(sec * SR); x = np.zeros((n, 2))
    for _ in range(count):
        s = int(rng.beta(1.2, 2.2) * (n - 400)); w = nwave(rng.uniform(0.25, 0.9), 0.4) * rng.uniform(0.15, 1.0) ** 1.5
        p = rng.uniform(-0.95, 0.95); L = len(w)
        x[s:s + L, 0] += w * np.sqrt(0.5 - p / 2); x[s:s + L, 1] += w * np.sqrt(0.5 + p / 2)
    x = hp(lp(x, 6500), 400)
    y = np.stack([signal.fftconvolve(x[:, c], outdoor_ir(3.0, 1.6, 0.35, 3)[:, c]) for c in range(2)], 1)
    return y

def norm(x, peak=0.8): return x / (np.abs(x).max() + 1e-9) * peak

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."; os.makedirs(out, exist_ok=True)
    L, LP, B, C = launch("whistle"), launch("plain"), boom(), crackle()
    tl = len(L) - int(0.85 * SR); full = np.zeros((tl + max(len(B), int(0.35 * SR) + len(C)), 2))
    full[:len(L)] += norm(L, 0.3); full[tl:tl + len(B)] += norm(B, 0.9)
    o = tl + int(0.35 * SR); full[o:o + len(C)] += norm(C, 0.28)
    for name, x in (("fireworks_launch", norm(L, 0.6)), ("fireworks_launch_plain", norm(LP, 0.6)),
                    ("fireworks_boom", norm(B, 0.9)), ("fireworks_crackle", norm(C, 0.6)), ("fireworks_full", norm(full, 0.9))):
        sf.write(os.path.join(out, name + ".wav"), x.astype(np.float32), SR, subtype="PCM_24")
    print("ok", out)
