"""ボスの雷の術と攻撃の効果音を、一から合成して WAV に書き出す（2026-10-04）。

人間の指示「落雷に効果音をつけよう」「攻撃にも効果音を」。
既存作品の効果音は使わない・まねない。ノイズと正弦波を重ね、フィルター・包絡線・残響で形を作る（録音素材は使わない）。
音はきれいで現代的に（CLAUDE.md「レトロ風にこだわらず」）。48kHz・ステレオ・16ビット。

使い方: python3 se_synth.py 出力フォルダ [fire/ など、作りなおす名前の一部]
出力:
  雷: cast.wav（発動とため）・leader.wav（先がけの稲妻のジジッ）・strike.wav（落雷: 裂ける音＋どん＋ゴロゴロ）・
      restrike.wav（光りなおし）・crack1〜3.wav（嵐の1本ずつ）・storm-rumble.wav（嵐の低いうなり）
  攻撃: windup.wav（ため: 岩がきしむ）・whoosh.wav（振り下ろしの風切り）・impact.wav（当たり）・
        slam.wav（両手でたたきつける）・step.wav（重い足音）
  炎: cast.wav（発動とため）・whoosh.wav（火の玉が飛ぶ）・explode.wav（はじける）・erupt.wav（火柱）・rumble.wav（低いうなり）
"""
import math
import os
import sys
import wave

import numpy as np
from scipy import signal

SR = 48000
RNG = np.random.default_rng(20261004)


def t_axis(sec):
    return np.arange(int(SR * sec)) / SR


def white(n):
    return RNG.standard_normal(n)


def brown(n):
    x = np.cumsum(white(n)) * 0.02
    return x - signal.lfilter([1], [1, -0.995], x) * 0.005   # ゆっくり0へもどす


def lp(x, fc, order=2):
    return signal.sosfilt(signal.butter(order, min(fc, SR * 0.45), "low", fs=SR, output="sos"), x)


def hp(x, fc, order=2):
    return signal.sosfilt(signal.butter(order, fc, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, order=2):
    return signal.sosfilt(signal.butter(order, [lo, min(hi, SR * 0.45)], "band", fs=SR, output="sos"), x)


def expdec(n, tau, delay=0.0):
    t = np.arange(n) / SR - delay
    return np.where(t >= 0, np.exp(-np.maximum(t, 0) / tau), 0.0)


def attack_env(n, a):
    t = np.arange(n) / SR
    return np.clip(t / max(a, 1e-4), 0, 1)


def place(dst, src, at):
    """dst（ステレオ）の at 秒の所に src（モノかステレオ）を足す"""
    i = int(at * SR)
    if i >= dst.shape[0]:
        return
    if src.ndim == 1:
        src = np.stack([src, src], 1)
    m = min(len(src), dst.shape[0] - i)
    dst[i:i + m] += src[:m]


def pan(x, p):
    """p: -1（左）〜1（右）。等パワー"""
    a = (p + 1) * math.pi / 4
    return np.stack([x * math.cos(a), x * math.sin(a)], 1)


def reverb(st, sec=1.2, wet=0.25, dark=4000):
    n = int(SR * sec)
    out = np.zeros((st.shape[0] + n, 2))
    out[:st.shape[0]] += st * (1 - wet * 0.5)
    for ch in range(2):
        ir = lp(white(n), dark) * np.exp(-np.arange(n) / SR / (sec / 5))
        ir[: int(SR * 0.012)] *= np.linspace(0, 1, int(SR * 0.012))   # 早い反射を少しおくらせる
        ir /= np.sqrt((ir ** 2).sum())
        wetc = signal.fftconvolve(st[:, ch], ir)[: out.shape[0]]
        out[: len(wetc), ch] += wetc * wet
    return out


def tail(x, ms=25):
    """おわりを短く小さくしていく（音がぷつっと切れて「プチ」と鳴らないように）"""
    n = min(len(x), int(SR * ms / 1000))
    x = x.copy()
    ramp = np.linspace(1, 0, n)
    x[-n:] = x[-n:] * (ramp[:, None] if x.ndim == 2 else ramp)
    return x


def soft(x, drive=1.0):
    return np.tanh(x * drive) / np.tanh(drive)


def finish(st, peak_db=-1.0, fade=0.03):
    st = st - st.mean(0)
    n = int(SR * fade)
    st[-n:] *= np.linspace(1, 0, n)[:, None]
    pk = np.abs(st).max() or 1
    return st / pk * 10 ** (peak_db / 20)


def write(path, st):
    st = np.clip(st, -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype("<i2").tobytes())


# ------------------------------------------------------------------ 部品
def crackle_burst(dur, rate0, rate1, amp=1.0, lo=2500, hi=12000, width=0.9):
    """ぱちぱち（細かい放電）: ランダムな短いノイズの粒。rate は1秒あたりの粒の数（はじめ→終わり）"""
    n = int(SR * dur)
    st = np.zeros((n, 2))
    t = 0.0
    while t < dur:
        r = rate0 + (rate1 - rate0) * (t / dur)
        t += RNG.exponential(1 / max(r, 1))
        if t >= dur:
            break
        g = int(SR * RNG.uniform(0.0015, 0.006))
        grain = bp(white(g + 64), lo, hi)[64:] * np.exp(-np.arange(g) / (g * 0.3))
        place(st, pan(grain * amp * RNG.uniform(0.3, 1.0), RNG.uniform(-width, width)), t)
    return st


def crack(scale=1.0):
    """雷の裂ける音: とても短い白い音の立ち上がり＋高い音のざらつき＋ぱちぱちのかたまり（左右で別のノイズ＝広がり）"""
    n = int(SR * 0.25)
    chans = [hp(white(n), 1800) * expdec(n, 0.012) + white(n) * expdec(n, 0.0015) * 1.6 for _ in range(2)]
    st = np.stack(chans, 1) * 0.6
    place(st, crackle_burst(0.12, 900, 120, amp=0.9), 0.0)
    return st * scale


def boom(f0=75, f1=36, tau=0.38, noise_tau=0.22, scale=1.0, sec=1.6):
    """どん: 下がっていく低い正弦波＋低いノイズのかたまり（少しひずませて厚く）"""
    n = int(SR * sec)
    t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t / 0.18)
    ph = 2 * np.pi * np.cumsum(f) / SR
    sub = np.sin(ph) * np.exp(-t / tau) * attack_env(n, 0.004)
    thud = lp(white(n), 380, 4) * np.exp(-t / noise_tau) * 3.0 * attack_env(n, 0.003)
    x = tail(soft(sub * 0.9 + thud * 0.7, 1.8) * scale, 120)
    return np.stack([x, x], 1)


def rumble(sec=2.8, tau=0.9, fc=170, scale=1.0, att=0.18, roll=(3.0, 7.0)):
    """ゴロゴロ: 低いブラウンノイズを、ゆっくり波打つ大きさでころがす"""
    n = int(SR * sec)
    t = np.arange(n) / SR
    out = []
    for ch in range(2):
        x = lp(brown(n), fc, 4)
        x /= (np.abs(x).max() or 1)
        # ころがる感じ: ランダムなこぶ（3〜7回/秒）
        k = int(sec * RNG.uniform(*roll))
        bumps = np.zeros(n)
        for _ in range(k):
            c = RNG.uniform(0, sec); w = RNG.uniform(0.06, 0.25)
            bumps += RNG.uniform(0.4, 1.0) * np.exp(-0.5 * ((t - c) / w) ** 2)
        am = 0.45 + bumps / (bumps.max() or 1)
        out.append(x * am)
    st = np.stack(out, 1)
    env = attack_env(n, att) * np.exp(-np.maximum(t - att, 0) / tau)
    return tail(st * env[:, None] * scale, 400)


# ------------------------------------------------------------------ 雷
def se_cast():
    """発動とため（約1.4秒）: 低いうなりが上がっていき、高いきらめきと、ぱちぱちが増え、最後に「ビュン」とはじける"""
    sec = 1.45
    n = int(SR * sec); t = np.arange(n) / SR
    f = 48 * (110 / 48) ** (np.minimum(t, 1.2) / 1.2)
    hum = np.zeros(n)
    for det in (-0.006, 0.0, 0.006):
        ph = 2 * np.pi * np.cumsum(f * (1 + det)) / SR
        for h in range(1, 40):
            if 48 * h * 2.3 > 9000:
                break
            hum += np.sin(ph * h) / h        # のこぎり波（帯域を区切る）
    hum /= np.abs(hum).max()
    # だんだん明るく（フィルターを開いていく）: 区間ごとに切りかえて重ねる
    bright = np.zeros(n)
    edges = np.linspace(0, n, 13).astype(int)
    for a, b in zip(edges, edges[1:]):
        fc = 250 + 2600 * (a / n) ** 1.5
        seg = lp(hum, fc, 2)[a:b]
        bright[a:b] = seg
    bright *= (0.55 + 0.45 * np.sin(2 * np.pi * 31 * t) ** 2)      # ブーンという電気のふるえ
    env = attack_env(n, 0.3) * np.where(t > 1.25, np.exp(-(t - 1.25) / 0.06), 1)
    st = np.stack([bright * env * 0.55, np.roll(bright, 30) * env * 0.55], 1)
    # きらめき（高い倍音。少しずつずらして、ゆらぐ）
    sh = np.zeros(n)
    for fr, a in ((1760, 1), (2637, 0.7), (3529, 0.5), (5290, 0.35)):
        sh += a * np.sin(2 * np.pi * fr * t + 3 * np.sin(2 * np.pi * 5.5 * t))
    sh *= (0.5 + 0.5 * np.sin(2 * np.pi * 9 * t)) * (t / sec) ** 2 * np.where(t > 1.25, np.exp(-(t - 1.25) / 0.05), 1)
    st += pan(sh * 0.05, -0.3) + pan(np.roll(sh, 400) * 0.05, 0.3)
    place(st, crackle_burst(1.25, 6, 70, amp=0.35), 0.0)
    # 最後のはじける音
    z = int(SR * 0.12); tz = np.arange(z) / SR
    zap = np.sin(2 * np.pi * np.cumsum(500 + 5000 * (tz / 0.12) ** 2) / SR) * np.exp(-tz / 0.05)
    place(st, pan(zap * 0.25, 0), 1.22)
    place(st, crackle_burst(0.12, 400, 50, amp=0.6), 1.22)
    return finish(reverb(st, 1.0, 0.22), -3)


def se_leader():
    """先がけの稲妻（約0.25秒）: 高いジジッという放電が強くなる"""
    sec = 0.28; n = int(SR * sec); t = np.arange(n) / SR
    x = bp(white(n), 2800, 9500)
    gate = np.zeros(n); i = 0
    while i < n:
        on = int(SR * RNG.uniform(0.002, 0.009)); off = int(SR * RNG.uniform(0.001, 0.006))
        gate[i:i + on] = RNG.uniform(0.4, 1.0); i += on + off
    gate = lp(gate, 900, 1)
    x = x * gate * (t / sec) ** 0.7 * np.where(t > 0.24, np.exp(-(t - 0.24) / 0.01), 1)
    st = pan(x, 0.25) + pan(np.roll(x, 90), 0.6) * 0.6
    return finish(reverb(st, 0.6, 0.15), -6)


def se_strike():
    """落雷（約3.2秒）: 裂ける音 → どん → ゴロゴロと遠ざかる"""
    sec = 3.2; st = np.zeros((int(SR * sec), 2))
    place(st, crack(1.0), 0.0)
    place(st, boom(80, 34, 0.42, 0.25, 1.1, 1.8), 0.008)
    place(st, rumble(3.0, 0.85, 180, 0.75), 0.12)
    place(st, crackle_burst(0.8, 160, 8, amp=0.35), 0.05)       # 火花のぱちぱち
    return finish(reverb(st, 1.6, 0.3, 3500), -1)


def se_restrike():
    """光りなおし（約1.4秒）: 少し小さい裂ける音と、短いどん"""
    sec = 1.4; st = np.zeros((int(SR * sec), 2))
    place(st, crack(0.7), 0)
    place(st, boom(70, 40, 0.25, 0.15, 0.6, 1.0), 0.006)
    place(st, crackle_burst(0.5, 120, 10, amp=0.3), 0.03)
    return finish(reverb(st, 1.2, 0.28, 3500), -4)


def se_crack(seed):
    """嵐の1本（約1.2秒）: 裂ける音＋中くらいのどん（1本ずつ少し違う）"""
    global RNG
    keep = RNG; RNG = np.random.default_rng(seed)
    sec = 1.2; st = np.zeros((int(SR * sec), 2))
    p = RNG.uniform(-0.5, 0.7)
    c = crack(0.85)
    st_c = np.stack([c[:, 0] * (1 - p) * 0.8 + c[:, 1] * 0.2, c[:, 1] * (1 + p) * 0.8 + c[:, 0] * 0.2], 1)
    place(st, st_c, 0)
    place(st, boom(RNG.uniform(70, 90), RNG.uniform(38, 46), 0.22, 0.13, 0.7, 0.9), 0.006)
    place(st, crackle_burst(0.4, 140, 10, amp=0.3), 0.02)
    RNG = keep
    return finish(reverb(st, 1.0, 0.25, 3500), -3)


def se_storm_rumble():
    """嵐の低いうなり（約4秒）: 雲がうなり、ゴロゴロが続く"""
    st = rumble(4.0, 1.6, 140, 1.0, att=0.5, roll=(4, 8))
    return finish(reverb(st, 1.5, 0.3, 2500), -6)


# ------------------------------------------------------------------ 攻撃
def se_windup():
    """ため（約0.7秒）: 岩の体がきしむ・ごりごり＋低いふくらみ"""
    sec = 0.75; n = int(SR * sec); t = np.arange(n) / SR
    x = bp(brown(n) * 20, 140, 900, 2)
    grains = np.zeros(n)
    tt = 0.0
    while tt < sec:
        tt += RNG.exponential(1 / 60)
        g = int(SR * RNG.uniform(0.01, 0.03)); i = int(tt * SR)
        if i + g < n:
            grains[i:i + g] += RNG.uniform(0.3, 1.0) * np.hanning(g)
    x = x / (np.abs(x).max() or 1) * grains
    swell = np.sin(2 * np.pi * np.cumsum(55 + 25 * t / sec) / SR) * np.sin(np.pi * np.minimum(t / sec, 1)) ** 2
    env = attack_env(n, 0.15) * np.where(t > 0.6, np.exp(-(t - 0.6) / 0.05), 1)
    st = pan(x * env * 0.7, -0.2) + pan(np.roll(x, 300) * env * 0.5, 0.3) + pan(swell * env * 0.5, 0)
    return finish(reverb(st, 0.8, 0.2, 3000), -6)


def se_whoosh(dur=0.36, lo=320, peak=2300, end=700, pan_from=-0.6, pan_to=0.6):
    """振り下ろしの風切り: 帯を区切ったノイズの中心を、低→高→低へ動かす"""
    n = int(SR * dur); t = np.arange(n) / SR
    pk = 0.55
    u = t / dur
    center = np.where(u < pk, lo * (peak / lo) ** (u / pk), peak * (end / peak) ** ((u - pk) / (1 - pk)))
    bands = [250, 400, 650, 1000, 1600, 2500, 3800]
    x = np.zeros(n); nz = white(n)
    for b in bands:
        y = bp(nz, b / 1.35, b * 1.35)
        w = np.exp(-0.5 * (np.log(center / b) / 0.32) ** 2)
        x += y * w
    env = np.sin(np.pi * np.clip(u / 0.95, 0, 1)) ** 1.6
    x = x * env
    p = pan_from + (pan_to - pan_from) * u
    a = (p + 1) * math.pi / 4
    st = np.stack([x * np.cos(a), x * np.sin(a)], 1)
    whum = np.sin(2 * np.pi * 95 * t) * env * 0.35
    st += np.stack([whum, whum], 1)
    return finish(reverb(st, 0.7, 0.15), -4)


def debris(sec, count, amp=0.4):
    """当たったあとのかけら（小石が散る小さな音）"""
    st = np.zeros((int(SR * sec), 2))
    for _ in range(count):
        at = sec * RNG.uniform(0.02, 1) ** 2
        g = int(SR * RNG.uniform(0.004, 0.015)); f = RNG.uniform(1800, 6000)
        click = bp(white(g + 64), f / 1.6, f * 1.6)[64:] * np.exp(-np.arange(g) / (g * 0.25))
        place(st, pan(click * amp * RNG.uniform(0.3, 1.0) * (1 - at / sec), RNG.uniform(-0.8, 0.8)), at)
    return st


def se_impact(scale=1.0, low=1.0):
    """当たり（約1.5秒）: 重い打撃（下がる低音）＋つぶれる音＋かけら"""
    sec = 1.5; st = np.zeros((int(SR * sec), 2))
    place(st, boom(110 * low, 42 * low, 0.2, 0.07, 1.0, 1.0), 0)
    n = int(SR * 0.3); t = np.arange(n) / SR
    crunch = bp(white(n), 900, 4200) * np.exp(-t / 0.05)
    gr = np.zeros(n); i = 0
    while i < n:
        g = int(SR * RNG.uniform(0.002, 0.008)); gr[i:i + g] = RNG.uniform(0.3, 1); i += g + int(SR * RNG.uniform(0, 0.004))
    place(st, pan(crunch * gr * 0.55, -0.15) + pan(np.roll(crunch * gr, 120) * 0.4, 0.25), 0.002)
    place(st, debris(0.7, 22, 0.35), 0.03)
    return finish(reverb(st, 1.1, 0.22, 3500), -1) * scale


def se_slam():
    """両手でたたきつける（約2.2秒）: 打撃を2つ重ね（少しずらす）、地ひびきのゴロゴロとかけらを足す"""
    sec = 2.2; st = np.zeros((int(SR * sec), 2))
    a = se_impact(1.0, 0.85); b = se_impact(0.8, 0.95)
    place(st, a * np.array([1.0, 0.75]), 0)
    place(st, b * np.array([0.75, 1.0]), 0.018)
    place(st, rumble(2.0, 0.5, 120, 0.7, att=0.03), 0.02)
    place(st, debris(1.2, 40, 0.3), 0.05)
    return finish(st, -1)


def se_step():
    """重い足音（約0.5秒）"""
    sec = 0.5; st = np.zeros((int(SR * sec), 2))
    place(st, boom(72, 40, 0.09, 0.04, 1.0, 0.45), 0)
    place(st, debris(0.25, 5, 0.2), 0.01)
    return finish(reverb(st, 0.6, 0.15, 2500), -1)


# ------------------------------------------------------------------ 炎（人間の指示「では火の魔法のバージョンも作って」）
def flicker(n, lo=6, hi=18, depth=0.6):
    """炎のゆらぎ: なめらかな乱数で大きさを波打たせる"""
    k = max(4, int(n / SR * hi))
    pts = RNG.uniform(1 - depth, 1, k + 2)
    return np.interp(np.linspace(0, k, n), np.arange(k + 2), pts)


def roar(sec, lo=180, hi=1600, depth=0.55):
    """ごうごうと燃える音: 帯を区切ったノイズを、炎のゆらぎで波打たせる（左右は別のノイズ）"""
    n = int(SR * sec)
    return np.stack([bp(white(n) + lp(white(n), 400) * 2, lo, hi) * flicker(n, depth=depth) for _ in range(2)], 1)


def pops(sec, rate, amp=0.5):
    """ぱちっとはぜる音（炎の中の小さな破裂）。雷のぱちぱちより低く、丸い"""
    st = np.zeros((int(SR * sec), 2)); t = 0.0
    while True:
        t += RNG.exponential(1 / max(rate, 1))
        if t >= sec: break
        g = int(SR * RNG.uniform(0.004, 0.012)); f = RNG.uniform(700, 2600)
        click = bp(white(g + 64), f / 1.8, f * 1.8)[64:] * np.exp(-np.arange(g) / (g * 0.22))
        place(st, pan(click * amp * RNG.uniform(0.3, 1.0), RNG.uniform(-0.8, 0.8)), t)
    return st


def sweep_noise(sec, f0, f1, width=1.5):
    """中心が f0→f1 へ動く、帯を区切ったノイズ（ゴオッ・フォッ）"""
    n = int(SR * sec); t = np.arange(n) / SR
    center = f0 * (f1 / f0) ** (t / sec)
    nz = white(n); x = np.zeros(n)
    for b in (150, 250, 400, 650, 1000, 1600, 2500, 4000):
        w = np.exp(-0.5 * (np.log(center / b) / 0.35) ** 2)
        x += bp(nz, b / width, b * width) * w
    return x


def se_fire_cast():
    """炎の発動とため（約1.45秒）: ごうごうと燃える音がふくらみ、はぜる音が増え、最後に「ボッ」と火がつく"""
    sec = 1.45; n = int(SR * sec); t = np.arange(n) / SR
    st = roar(sec, 160, 1400) * (np.clip(t / 1.1, 0, 1) ** 1.5 * np.where(t > 1.25, np.exp(-(t - 1.25) / 0.08), 1))[:, None] * 0.9
    sw = tail(sweep_noise(1.25, 250, 1100) * np.linspace(0, 1, int(SR * 1.25)) ** 2, 120)
    place(st, pan(sw * 0.35, 0), 0)
    place(st, pops(1.25, 25, 0.45), 0)
    # 最後の「ボッ」
    m = int(SR * 0.4); tm = np.arange(m) / SR
    fwoomp = lp(white(m), 1800) * np.exp(-tm / 0.07) * 1.4
    thump = np.sin(2 * np.pi * np.cumsum(90 * np.exp(-tm / 0.1) + 45) / SR) * np.exp(-tm / 0.12)
    place(st, pan(fwoomp + thump * 0.8, 0), 1.2)
    return finish(reverb(st, 1.0, 0.2, 3000), -2)


def se_fire_whoosh():
    """火の玉が飛ぶ（約0.6秒）: ゴオッという炎の音が、左から右へ近づいて通りすぎる"""
    sec = 0.6; n = int(SR * sec); t = np.arange(n) / SR
    x = sweep_noise(sec, 400, 1500) * np.sin(np.pi * np.clip(t / 0.55, 0, 1)) ** 1.4 * flicker(n, 10, 25, 0.4)
    p = -0.7 + 1.4 * t / sec; a = (p + 1) * math.pi / 4
    st = np.stack([x * np.cos(a), x * np.sin(a)], 1)
    st += roar(sec, 120, 600) * np.sin(np.pi * np.clip(t / 0.55, 0, 1))[:, None] * 0.6
    place(st, pops(0.5, 30, 0.3), 0.05)
    return finish(reverb(st, 0.7, 0.15), -3)


def se_fire_explode():
    """火の玉がはじける（約2.6秒）: どん＋ばっと広がる音＋燃えさかる音が残り、はぜる音"""
    sec = 2.6; st = np.zeros((int(SR * sec), 2))
    place(st, boom(70, 30, 0.35, 0.2, 1.0, 1.4), 0)
    m = int(SR * 0.6); tm = np.arange(m) / SR
    blast = np.zeros(m); nz = white(m)
    for a, b in ((0, 0.05), (0.05, 0.15), (0.15, 0.6)):        # 明るい音 → こもった音へ
        i0, i1 = int(a * SR), int(b * SR)
        fc = 4000 if a == 0 else (1800 if a == 0.05 else 700)
        blast[i0:i1] = lp(nz, fc)[i0:i1]
    blast *= np.exp(-tm / 0.12) * 1.6
    place(st, np.stack([blast, np.roll(blast, 60)], 1), 0)
    tail = roar(2.2, 140, 1200) * np.exp(-np.arange(int(SR * 2.2)) / SR / 0.7)[:, None] * 0.7
    place(st, tail, 0.08)
    place(st, pops(1.6, 35, 0.4), 0.1)
    place(st, debris(0.8, 15, 0.25), 0.05)
    return finish(reverb(st, 1.3, 0.28, 3000), -1)


def se_fire_erupt():
    """火柱が立つ（約1.3秒）: 「ゴウッ」と下から吹き上がり、少し燃えて消える"""
    sec = 1.3; n = int(SR * sec); t = np.arange(n) / SR
    up = sweep_noise(0.35, 200, 2200) * np.minimum(np.arange(int(SR * 0.35)) / (SR * 0.03), 1) * np.exp(-np.arange(int(SR * 0.35)) / SR / 0.25)
    st = np.zeros((n, 2))
    place(st, pan(tail(up, 150) * 1.2, 0), 0)
    place(st, roar(1.1, 150, 1300) * np.exp(-np.arange(int(SR * 1.1)) / SR / 0.35)[:, None] * 0.8, 0.05)
    place(st, boom(80, 45, 0.12, 0.06, 0.6, 0.5), 0)
    place(st, pops(0.9, 25, 0.3), 0.1)
    return finish(reverb(st, 1.0, 0.22, 3000), -2)


def se_fire_rumble():
    """炎の低いうなり（約3.5秒）: 地面の下で火がうなる"""
    sec = 3.5; n = int(SR * sec); t = np.arange(n) / SR
    st = roar(sec, 50, 260, 0.7) * (np.clip(t / 0.6, 0, 1) * np.exp(-np.maximum(t - 1.5, 0) / 1.0))[:, None]
    return finish(reverb(tail(st, 300), 1.2, 0.25, 2000), -6)


if __name__ == "__main__":
    out = sys.argv[1]
    for sub in ("lightning", "boss-attack", "fire"):
        os.makedirs(f"{out}/{sub}", exist_ok=True)
    jobs = [("lightning/cast", se_cast), ("lightning/leader", se_leader), ("lightning/strike", se_strike),
            ("lightning/restrike", se_restrike), ("lightning/crack1", lambda: se_crack(1)), ("lightning/crack2", lambda: se_crack(2)),
            ("lightning/crack3", lambda: se_crack(3)), ("lightning/storm-rumble", se_storm_rumble),
            ("boss-attack/windup", se_windup), ("boss-attack/whoosh", se_whoosh), ("boss-attack/impact", se_impact),
            ("boss-attack/slam", se_slam), ("boss-attack/step", se_step),
            ("fire/cast", se_fire_cast), ("fire/whoosh", se_fire_whoosh), ("fire/explode", se_fire_explode),
            ("fire/erupt", se_fire_erupt), ("fire/rumble", se_fire_rumble)]
    only = sys.argv[2:]          # 名前の一部（例: fire/）を書くと、それだけ作りなおす
    jobs = [j for j in jobs if not only or any(o in j[0] for o in only)]
    for name, fn in jobs:
        st = fn()
        write(f"{out}/{name}.wav", st)
        print(f"{name}.wav  {len(st) / SR:.2f}秒")
