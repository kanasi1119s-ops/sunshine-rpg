#!/usr/bin/env python3
"""段3の答え合わせ: 中身の分かっている音を作って測り、数字が合うかを見る。使い方: python3 tools/song-analyzer/eval3.py"""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stage3 as S3
SR = 44100; rng = np.random.default_rng(1)
def note(f, dur, wave, att=0.005, dec=None, vib=None):
    t = np.arange(int(dur * SR)) / SR; ph = 2 * np.pi * f * t
    if vib: ph = 2 * np.pi * np.cumsum(f * 2 ** (vib[1] / 1200 * np.sin(2 * np.pi * vib[0] * t))) / SR
    n = int(SR / 2 / f); hs = range(1, n + 1)
    if wave == "saw": y = sum(np.sin(h * ph) / h for h in hs)
    elif wave == "square": y = sum(np.sin(h * ph) / h for h in hs if h % 2)
    else: y = np.sin(ph)
    e = np.minimum(1, t / att)
    if dec: e = e * np.exp(-t / dec)
    e[-200:] *= np.linspace(1, 0, 200); return y * e / np.abs(y).max()
def line(wave, **kw): return np.concatenate([np.concatenate([note(f, 0.5, wave, **kw), np.zeros(int(0.1 * SR))]) for f in [82.4, 98, 110, 82.4, 73.4, 98, 123.5, 110] * 3])
print("■ 倍音の形（ベースの高さ）")
for w, want in (("saw", "のこぎり波 −6dB／オクターブ"), ("square", "四角い波・奇数が強い"), ("sine", "サイン波")):
    y = line(w).astype(np.float32); f0 = np.concatenate([np.concatenate([np.full(int(0.5 * SR / 256), f), np.full(int(0.1 * SR / 256) + 1, np.nan)]) for f in [82.4, 98, 110, 82.4, 73.4, 98, 123.5, 110] * 3]); tf = np.arange(len(f0)) * 256 / SR
    h = S3.harmonics(y, f0, tf); print(f"  {w}: {h['波の形（たぶん）']}・下がり方 {h['倍音の下がり方（dB／オクターブ）']}・奇数−偶数 {h['奇数の倍音 − 偶数の倍音（dB）']}  （正解: {want}）")
print("■ 立ち上がりと余韻")
for att, dec in ((0.005, 0.08), (0.06, None), (0.15, None), (0.005, 0.3)):
    y = line("saw", att=att, dec=dec).astype(np.float32); on = [k * 0.6 for k in range(24)]; e = S3.envelope(y, on)
    print(f"  立ち上がり {att * 1000:.0f}ミリ秒・余韻 {'のばす' if not dec else f'{dec * 1000 * 1.15:.0f}ミリ秒で −10dB'} → 測った: {e['立ち上がり（ミリ秒・10%→90%。20より短くは測れない）']}ミリ秒・{list(e.values())[1]}ミリ秒・0.2秒あと {e['頭から0.2秒あとの大きさ（dB・頭を0として）']}dB")
print("■ ビブラート")
for rate, depth in ((5.5, 30), (6.5, 60), (0, 0)):
    y = np.concatenate([np.concatenate([note(f, 1.2, "saw", vib=(rate, depth) if rate else None), np.zeros(int(0.2 * SR))]) for f in [330, 392, 440, 349] * 4]); tf = np.arange(len(y) // 128) * 128 / SR
    f0 = np.concatenate([np.concatenate([f * 2 ** (depth / 1200 * np.sin(2 * np.pi * rate * np.arange(int(1.2 * SR / 128)) * 128 / SR)), np.full(int(0.2 * SR / 128), np.nan)]) for f in [330, 392, 440, 349] * 4]); f0 = f0[:len(tf)]; tf = tf[:len(f0)]
    v = S3.vibrato(f0, tf); print(f"  速さ {rate}Hz・深さ {depth}セント → 測った: 速さ {v['ビブラートの速さ（Hz）']}・深さ {v['ビブラートの深さ（セント・片側）']}・ある割合 {v['そのうちビブラートがある割合']}")
print("■ ポンプ（拍の頭でへこむ）")
for depth_db in (0, 6, 12):
    bpm = 128; beats = np.arange(0, 20, 60 / bpm); t = np.arange(int(20 * SR)) / SR; ph = (t % (60 / bpm)) / (60 / bpm); g = 10 ** (-depth_db / 20) + (1 - 10 ** (-depth_db / 20)) * np.minimum(1, ph / 0.6)
    y = (rng.standard_normal(len(t)) * 0.2 * g).astype(np.float32); p = S3.pump(y, beats); print(f"  深さ {depth_db}dB → 測った: 深さ {p['へこみの深さ（dB）']}dB・場所 {p['いちばんへこむ場所（1拍を0〜1として）']}・ポンプ {p['拍の頭でへこんで、あとから戻る（ポンプ）']}")
print("■ 左右の広がり")
for w in (0.0, 0.5, 1.0):
    a, b = rng.standard_normal(SR * 5), rng.standard_normal(SR * 5); st = np.stack([a + w * b, a - w * b]).astype(np.float32) * 0.1; r = S3.tone(st); print(f"  左右の差 ÷ まん中 ＝ {w} → 測った: 中 {r['左右の広がり（中 250Hz〜2kHz）']}・高い所 {r['左右の広がり（高い所 2kHz〜）']}")
