#!/usr/bin/env python3
"""プチッ（1〜2サンプルだけ波形が飛ぶ点）を、前後の波形からなめらかに埋めて消す（2026-10-17、人間の指示「雑音とれない？」）。

  python3 tools/audio-check/declick.py <入力.wav> [出力.wav]   （出力を省くと上書き）

調べて分かったこと: 作曲ソフトの書き出しで、オーケストラ（VSCO）のホルン・コントラバス・チェロ・弦・鉄琴などに、
音の切りかわりで 1 サンプルだけ波形がへこむ点が出る（左右とも同じ形。録音の頭をなめらかにしても消えない）。
音楽の中身には関係のない、ごく短い飛びなので、前後の 4 サンプルずつから 3 次の式で埋める。
見つけ方: 2 階差分が、前後 10ms の 2 階差分の中央値の 12 倍を超え、しかも 1〜2 サンプルで元にもどる点。
"""
import sys
import numpy as np
import soundfile as sf


HERE = __import__("os").path.dirname(__import__("os").path.abspath(__file__))
_spec = __import__("importlib.util").util.spec_from_file_location("noise", HERE + "/noise-check.py")
noise = __import__("importlib.util").util.module_from_spec(_spec); _spec.loader.exec_module(noise)


def find(m, fs):
    """noise-check.py の「プチッ」と同じ見つけ方（LPC の残差が、まわりの 12 倍を超え、ぽつんと 1 つだけ飛び出す 0.6ms 以下の点）"""
    from scipy.signal import butter, sosfiltfilt
    from scipy.ndimage import median_filter
    hp = sosfiltfilt(butter(2, 1000, "highpass", fs=fs, output="sos"), m)
    ar = np.abs(noise.lpc_residual(hp, fs))
    loc = np.repeat(median_filter(ar[::4], size=int(0.02 * fs / 4) | 1), 4)[:len(ar)]
    cand = (ar > 12 * (loc + 1e-7)) & (ar > 10 ** (-40 / 20))
    out = []; w = int(0.015 * fs); g = max(2, int(0.0005 * fs))
    for s0, e in noise.events(cand, fs, 0.005):
        if e - s0 > int(0.0006 * fs): continue
        i = s0 + int(np.argmax(ar[s0:e + 1]))
        around = np.concatenate([ar[max(0, i - w):max(0, i - g)], ar[i + g:i + w]])
        if len(around) and ar[i] > 4 * around.max(): out.append(i)
    return out


def repair(x, idx):
    n = len(x)
    for i in idx:
        a, b = max(0, i - 6), min(n, i + 7)
        t = np.r_[np.arange(a, i - 1), np.arange(i + 2, b)]
        if len(t) < 6:
            continue
        for ch in range(x.shape[1]):
            c = np.polyfit(t - i, x[t, ch], 3)
            for j in range(i - 1, i + 2):  # とがった点と、その前後 1 サンプル
                x[j, ch] = np.polyval(c, j - i)
    return x


def main():
    src = sys.argv[1]; dst = sys.argv[2] if len(sys.argv) > 2 else src
    x, fs = sf.read(src, dtype="float64", always_2d=True)
    tot = 0
    for _ in range(3):  # 埋めたあとに、となりの点が目立つことがあるので 3 回まで
        idx = find(x.mean(1), fs)
        if not idx: break
        # LPC の残差は、飛びの少しあとに山が出ることがあるので、山の手前 3 サンプルの中で、波形がいちばんとがった点を埋める
        m = x.mean(1); fixed = []
        for i in idx:
            a = max(3, i - 3); seg = np.abs(np.diff(m[a - 2:i + 3], 2)); fixed.append(a - 1 + int(np.argmax(seg)))
        x = repair(x, fixed); tot += len(fixed)
    info = sf.info(src)
    sf.write(dst, x, fs, subtype=info.subtype)
    print(f"プチッを {tot} か所埋めた: {dst}")


if __name__ == "__main__":
    main()
