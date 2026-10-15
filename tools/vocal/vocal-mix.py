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

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("backing"); ap.add_argument("vocal"); ap.add_argument("--out", required=True)
    ap.add_argument("--bpm", type=float, required=True); ap.add_argument("--vocal-lu", type=float, default=0.0)
    ap.add_argument("--target", type=float, default=-13.5); ap.add_argument("--reverb", type=float, default=0.16)
    ap.add_argument("--stems", default="")
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
    dry = Pedalboard([HighpassFilter(100), PeakFilter(250, -2.0, 1.0), PeakFilter(3000, 2.0, 0.9),
                      PeakFilter(7200, -2.5, 2.0), HighShelfFilter(10000, 2.0, 0.7),
                      Compressor(threshold_db=-20, ratio=3.0, attack_ms=4, release_ms=70), Gain(3.0)])
    v = dry(vx[None, :], fs)[0]
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
    print(f"伴奏 {lb:.1f} LUFS / 歌 {lv:.1f} → 歌を伴奏{a.vocal_lu:+.1f}LU に / 完成 {meter.integrated_loudness(mix.T):.1f} LUFS → {a.out}")

if __name__ == "__main__":
    main()
