#!/usr/bin/env python3
"""歌（WAV）と伴奏（WAV）を混ぜて、1曲に仕上げる。
歌の音作り（ボーカルのよくある順番）:
  低い音のカット（100Hz）→ こもりを少し減らす（250Hz）→ 言葉をはっきり（3kHz）→ 歯擦音を少し抑える（7kHz）→ 空気感（10kHz〜）
  → コンプレッサー（大小の差をならす）→ 送りのリバーブ（広がり）と 8分のディレイ（うすく）
伴奏は、歌とぶつかる帯域（2.5kHz あたり）をほんの少しへこませる。
音量: 歌の大きさを、伴奏の大きさ（LUFS）からの差 --vocal-lu で決める。最後に全体を -13.5 LUFS（作曲ソフトの「B」）にそろえ、リミッターで頭をおさえる。

使い方: python3 tools/vocal/vocal-mix.py <伴奏.wav> <歌.wav> --out <完成.wav> --bpm 150 [--vocal-lu 0] [--target -13.5]
"""
import argparse
import numpy as np, soundfile as sf, pyloudnorm as pyln
from pedalboard import (Pedalboard, HighpassFilter, PeakFilter, HighShelfFilter, Compressor, Reverb, Delay, LowpassFilter, Gain)
from scipy.ndimage import minimum_filter1d, uniform_filter1d

def limit(x, fs, ceil_db=-1.0, look_ms=5.0):
    """先読みのピーク・リミッター（頭を ceil_db でおさえる。音量は上げない）。x: (2, n)"""
    c = 10 ** (ceil_db / 20); L = max(1, int(fs * look_ms / 1000))
    g = np.minimum(1.0, c / (np.abs(x).max(axis=0) + 1e-9))
    g = minimum_filter1d(g, 2 * L + 1)
    g = uniform_filter1d(g, L)
    g = np.minimum(g, minimum_filter1d(np.minimum(1.0, c / (np.abs(x).max(axis=0) + 1e-9)), L))
    return x * g

def deess(x, fs, lo=5500, thr_db=-30.0, max_cut_db=8.0):
    """ディエッサー: 5.5kHz より上（さ・し・つ の「シー」）が強いときだけ、その帯域を下げる。x: (n,)"""
    from scipy.signal import butter, sosfiltfilt
    hi = sosfiltfilt(butter(4, lo, "highpass", fs=fs, output="sos"), x)
    w = int(0.005 * fs)
    env = 10 * np.log10(uniform_filter1d(hi ** 2, w) + 1e-12)
    cut = np.clip(env - thr_db, 0, max_cut_db) * 0.6
    g = 10 ** (-uniform_filter1d(cut, int(0.01 * fs)) / 20)
    return (x - hi + hi * g).astype(np.float32)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("backing"); ap.add_argument("vocal"); ap.add_argument("--out", required=True)
    ap.add_argument("--bpm", type=float, required=True); ap.add_argument("--vocal-lu", type=float, default=0.0)
    ap.add_argument("--target", type=float, default=-13.5); ap.add_argument("--reverb", type=float, default=0.16)
    ap.add_argument("--stems", default=""); ap.add_argument("--deess-db", type=float, default=-32.0)
    a = ap.parse_args()
    bk, fs = sf.read(a.backing, dtype="float32", always_2d=True)
    vx, fs2 = sf.read(a.vocal, dtype="float32", always_2d=True)
    vx = vx.mean(axis=1)
    if fs2 != fs:   # 歌の WAV を伴奏の周波数にそろえる
        from math import gcd
        from scipy.signal import resample_poly
        g = gcd(fs, fs2); vx = resample_poly(vx, fs // g, fs2 // g).astype(np.float32)
    n = max(len(bk), len(vx))
    bk = np.pad(bk, ((0, n - len(bk)), (0, 0))); vx = np.pad(vx, (0, n - len(vx)))
    # 透き通る声に（2026-10-15、人間の指示「ノイズを少なく、透き通る声に」）: 高域の持ち上げは控えめ（12kHz +1dB。かすれ・サーッも一緒に上がるため）、
    # ディエッサーで「シー」をおさえ、こもり（250Hz）を少し減らし、2.5kHz で言葉の輪郭を出す
    dry = Pedalboard([HighpassFilter(110), PeakFilter(250, -2.5, 1.0), PeakFilter(2500, 1.5, 0.9),
                      HighShelfFilter(9000, -2.0, 0.7), LowpassFilter(16000),   # 合成のサーッという高域をおさえる（2026-10-15「マイクのノイズ」）
                      Compressor(threshold_db=-20, ratio=3.0, attack_ms=4, release_ms=70), Gain(3.0)])
    v = dry(vx[None, :], fs)[0]
    v = deess(v, fs, thr_db=a.deess_db)
    st = np.stack([v, v])
    eighth = 60.0 / a.bpm / 2
    rv = Pedalboard([HighpassFilter(250), Reverb(room_size=0.55, damping=0.55, wet_level=1.0, dry_level=0.0, width=1.0), LowpassFilter(9000)])(st, fs)
    dl = Pedalboard([HighpassFilter(300), LowpassFilter(6000), Delay(delay_seconds=eighth * 1.5, feedback=0.25, mix=1.0)])(st, fs)
    dl[0] = np.roll(dl[0], int(0.012 * fs))   # 左右で少しずらして広げる
    vocal_bus = st + a.reverb * rv + 0.08 * dl
    bk2 = Pedalboard([PeakFilter(2500, -1.5, 0.8)])(bk.T.copy(), fs)
    meter = pyln.Meter(fs)
    lb = meter.integrated_loudness(bk2.T); lv = meter.integrated_loudness(vocal_bus.T)
    vocal_bus *= 10 ** ((lb + a.vocal_lu - lv) / 20)
    mix = bk2 + vocal_bus
    lm = meter.integrated_loudness(mix.T)
    gall = 10 ** ((a.target - lm) / 20)
    for _ in range(3):   # リミッターで少し下がるぶんを足して、目標の大きさにそろえる
        out = limit(mix * gall, fs)
        gall *= 10 ** ((a.target - meter.integrated_loudness(out.T)) / 20)
    mix = limit(mix * gall, fs).astype(np.float32)
    if a.stems:
        g = gall
        sf.write(a.stems + "-歌のみ.wav", (vocal_bus * g).T.astype(np.float32), fs, subtype="PCM_16")
    sf.write(a.out, mix.T, fs, subtype="PCM_16")
    # 雑音の検知（音割れ・直流・超低域・プチッ）。歌だけの雑音は utau-render.py の最後に出る
    import subprocess, sys, os
    chk = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audio-check", "noise-check.py")
    r = subprocess.run([sys.executable, chk, a.out, "--bpm", str(a.bpm)], capture_output=True, text=True)
    print("雑音:", r.stdout.strip() or r.stderr.strip()[-300:])
    print(f"伴奏 {lb:.1f} LUFS / 歌 {lv:.1f} → 歌を伴奏{a.vocal_lu:+.1f}LU に / 完成 {meter.integrated_loudness(mix.T):.1f} LUFS → {a.out}")

if __name__ == "__main__":
    main()
