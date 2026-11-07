"""曲の音を、ノイズがないか最初から最後まで調べる（2026-11-07 人間「ノイズは曲全部チェックしないとダメだよ？」）。

使い方: python3 tools/audio-check/noise_scan.py <wav か mp3> [--vocal] [--bpm 88] [--label 名前]
  パートごと（ステム）でも、仕上がった曲でもよい。--vocal を付けると、歌だけの音として「母音のかすれ」も調べる。
調べること（どれも、見つけた時刻と「小節.拍」を出す）:
  1. プチッ（クリック）: となりのサンプルとの差が、まわりの大きさに比べて飛びぬけている所
  2. 音の途切れ: 鳴っている音が 5ms 以内に 30dB 以上落ちる所（音を急に切った）
  3. 音割れ: 振幅が 0.99 をこえる所が続く
  4. 無音の所の雑音: 鳴っていない所の音の大きさ（-70dB より大きいと「サー」が聞こえる）
  5. パチパチ（細かい雑音の粒）: 6kHz より上を取り出し、20ms ごとのとがり具合（尖度）が大きい所
  6. （--vocal）母音のかすれ: 声が出ている所の 5〜12kHz で、倍音と倍音のすきまの雑音が倍音に近い所
"""
import sys, numpy as np, soundfile as sf
from scipy import signal
from scipy.ndimage import uniform_filter1d

a = sys.argv[1:]
path = a[0]; vocal = "--vocal" in a
bpm = float(a[a.index("--bpm") + 1]) if "--bpm" in a else 88.0
label = a[a.index("--label") + 1] if "--label" in a else path.split("/")[-1]
y, sr = sf.read(path, always_2d=True)
m = y.mean(1)
def pos(t):
    b = t * bpm / 60.0; return f"{t:6.2f}秒（{int(b // 4) + 1}小節 {b % 4 + 1:.1f}拍）"
rep = []
# 1. クリック
d = np.abs(np.diff(m)); loc = uniform_filter1d(d, int(0.004 * sr)) + 1e-6
hp = signal.lfilter(*signal.butter(2, 3000 / (sr / 2), "high"), m)
hd = np.abs(np.diff(hp)); hloc = uniform_filter1d(hd, int(0.01 * sr)) + 1e-7
cl = np.where((hd > 0.02) & (hd > 18 * hloc))[0]
if len(cl):
    groups = np.split(cl, np.where(np.diff(cl) > int(0.05 * sr))[0] + 1)
    for g in groups[:40]: rep.append(("プチッ", g[0] / sr, f"強さ {hd[g].max():.3f}"))
# 2. 途切れ
fr = int(0.005 * sr); n = len(m) // fr
rms = np.sqrt(np.mean(m[: n * fr].reshape(n, fr) ** 2, 1)) + 1e-9; db = 20 * np.log10(rms)
for i in range(1, n - 1):
    if db[i - 1] > -35 and db[i] < db[i - 1] - 30:
        rep.append(("音の途切れ", i * fr / sr, f"{db[i-1]:.0f}→{db[i]:.0f}dB"))
# 3. 音割れ
clip = np.where(np.abs(y).max(1) > 0.99)[0]
if len(clip): rep.append(("音割れ", clip[0] / sr, f"{len(clip)}サンプル"))
# 4. 無音の雑音
w = int(0.1 * sr); nn = len(m) // w
r100 = 20 * np.log10(np.sqrt(np.mean(m[: nn * w].reshape(nn, w) ** 2, 1)) + 1e-12)
gaps = r100[(r100 < -45)]
floor = float(np.median(gaps)) if len(gaps) else None
noisy_gap = [(i * 0.1, r100[i]) for i in range(nn) if -70 < r100[i] < -45 and (i == 0 or r100[i - 1] < -45) and (i + 1 >= nn or r100[i + 1] < -45)]
for t, v in noisy_gap[:20]: rep.append(("無音の所の雑音", t, f"{v:.0f}dB"))
# 5. パチパチ
h6 = signal.lfilter(*signal.butter(4, 6000 / (sr / 2), "high"), m)
w2 = int(0.02 * sr); n2 = len(h6) // w2
blk = h6[: n2 * w2].reshape(n2, w2)
k = (np.mean(blk ** 4, 1) / (np.mean(blk ** 2, 1) ** 2 + 1e-20))
lvl = 20 * np.log10(np.sqrt(np.mean(blk ** 2, 1)) + 1e-12)
cr = np.where((k > 25) & (lvl > -55))[0]
if len(cr):
    groups = np.split(cr, np.where(np.diff(cr) > 5)[0] + 1)
    for g in groups[:30]: rep.append(("パチパチ", g[0] * w2 / sr, f"尖度 {k[g].max():.0f}"))
# 6. 母音のかすれ
if vocal:
    import librosa
    S = np.abs(librosa.stft(m, n_fft=4096, hop_length=1024)) ** 2; fq = librosa.fft_frequencies(sr=sr, n_fft=4096)
    f0, vf, _ = librosa.pyin(m, fmin=150, fmax=900, sr=sr, frame_length=4096, hop_length=1024)
    band = (fq > 5000) & (fq < 12000); vals = []
    for i in range(min(S.shape[1], len(f0))):
        if not vf[i] or np.isnan(f0[i]): continue
        hm = np.abs(fq / f0[i] - np.round(fq / f0[i])) < 0.12
        hn = 10 * np.log10(S[band & hm, i].sum() / (S[band & ~hm, i].sum() + 1e-12) + 1e-12)
        vals.append((hn, i * 1024 / sr))
    if vals:
        arr = np.array([v for v, _ in vals])
        print(f"  母音のかすれ（5〜12kHz の倍音とすきまの差。大きいほどきれい）: 中央 {np.median(arr):.1f}dB・悪い所の1割 {np.percentile(arr, 10):.1f}dB")
        bad = sorted(vals)[:10]
        for v, t in bad:
            if v < 6: rep.append(("母音のかすれ", t, f"{v:.1f}dB"))
print(f"■ {label}: 長さ {len(m)/sr:.1f}秒・ピーク {20*np.log10(np.abs(y).max()+1e-12):.1f}dB・無音の所の雑音 {floor if floor is None else round(floor,1)}dB")
kinds = {}
for k_, t, info in sorted(rep, key=lambda x: x[1]): kinds.setdefault(k_, []).append((t, info))
if not kinds: print("  見つかった問題: なし")
for k_, lst in kinds.items():
    print(f"  {k_}: {len(lst)}か所")
    for t, info in lst[:12]: print(f"     {pos(t)}  {info}")
