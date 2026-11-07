"""録音のサンプルを1つずつ測って、ちょうどの音程に直す（2026-11-07）。

人間「（割れは）歪みを抑えるってより、音自体に原因がありそう」:
  Emily の直接録音は、サンプルごとに −3〜+15 セントずれていた（平均 +3、ばらつき 4）。
  和音を歪ませると、このずれがうなり（濁り・割れ）として大きく聞こえる。
使い方: python3 tools/soundfont/retune-samples.py <元の notes フォルダ> <書き出す notes フォルダ>
  ファイル名の音名（例 eb3_mf_rr1.wav）を正しい高さとして、0.12〜0.9 秒の音程（YIN の中央値）に合わせて細かく伸び縮みさせる。
  そのあと sfz-to-sf3.mjs で SF3 にする（例: --q 10 --rr 3。圧縮の雑音も歪みで目立つので、高い品質で）。
"""
import sys, os, re, glob
import numpy as np, soundfile as sf, librosa
N = {'c': 0, 'd': 2, 'e': 4, 'f': 5, 'g': 7, 'a': 9, 'b': 11}
src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
for f in sorted(glob.glob(f"{src}/*.wav")):
    b = os.path.basename(f); m = re.match(r'([a-g])([b#]?)(\d)', b)
    midi = N[m[1]] + (-1 if m[2] == 'b' else 1 if m[2] == '#' else 0) + (int(m[3]) + 1) * 12
    y, sr = sf.read(f); seg = y[int(0.12 * sr):int(0.9 * sr)]
    f0 = librosa.yin(seg if seg.ndim == 1 else seg.mean(1), fmin=60, fmax=1400, sr=sr)
    c = 1200 * np.log2(np.median(f0[np.isfinite(f0)]) / (440 * 2 ** ((midi - 69) / 12)))
    if abs(c) > 40: c = 0
    out = librosa.resample(y.T if y.ndim > 1 else y, orig_sr=sr, target_sr=sr * 2 ** (c / 1200), res_type='soxr_vhq') if abs(c) > 0.5 else (y.T if y.ndim > 1 else y)
    sf.write(f"{dst}/{b}", out.T if out.ndim > 1 else out, sr, subtype='PCM_24')
    print(b, f"{c:+.1f} セント")
