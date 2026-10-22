# テスト曲の WAV を数値で確かめる: 無音でない（区間ごとの大きさ）・クリップしない（ピーク）・音程が合う（ベースのステムの基本周波数）
#   python3 check_test_wav.py <曲.json> <全体.wav> [<ベースのステム.wav>]
import sys, json, re
import numpy as np
from scipy.io import wavfile

def load(p):
    sr, x = wavfile.read(p)
    x = x.astype(np.float64)
    if x.dtype.kind == "i" or np.abs(x).max() > 2: x /= 32768.0
    if x.ndim > 1: x = x.mean(axis=1) if x.shape[1] <= 2 else x
    return sr, x

def db(v): return 20 * np.log10(max(v, 1e-12))

def f0(seg, sr, lo=28.0, hi=420.0):
    """自己相関（YIN の差分関数）で基本周波数"""
    seg = seg - seg.mean()
    n = len(seg); tmin = int(sr / hi); tmax = int(sr / lo)
    if n < tmax * 2: return None
    d = np.array([np.sum((seg[:n - tmax] - seg[t:n - tmax + t]) ** 2) for t in range(tmin, tmax)])
    cm = d * np.arange(1, len(d) + 1) / np.maximum(np.cumsum(d), 1e-12)
    cand = np.where(cm < 0.25)[0]
    i = cand[0] if len(cand) else int(np.argmin(cm))
    while i + 1 < len(cm) and cm[i + 1] < cm[i]: i += 1
    return sr / (i + tmin)

def main(js, wav, bass_wav=None):
    song = json.load(open(js)); bpm = song["bpm"]; spb = 60 / bpm
    sr, x = load(wav)
    print(f"全体: 長さ {len(x)/sr:.1f}秒・ピーク {db(np.abs(x).max()):.2f} dBFS・クリップ（|x|≥0.999）{int(np.sum(np.abs(x) >= 0.999))} 標本")
    names = ["前奏", "Aメロ", "サビ", "ブレイクダウン"]
    for k, nm in enumerate(names):
        a, b = int(k * 16 * spb * sr), int((k + 1) * 16 * spb * sr)
        print(f"  {nm}: RMS {db(np.sqrt(np.mean(x[a:b] ** 2))):.1f} dBFS")
    if not bass_wav: return
    sr, y = load(bass_wav)
    bass = [p for p in song["parts"] if p["instrument"] == "bass"][0]["notes"]
    # 書き出しは頭の無音を詰めることがあるので、最初の音の立ち上がりで時刻を合わせる
    first = 0.0
    for tk in bass.split():
        if tk.startswith("R:"): first += float(tk[2:])
        else: break
    hop = int(sr * 0.005)
    env = np.array([np.sqrt(np.mean(y[i:i + hop] ** 2)) for i in range(0, len(y) - hop, hop)])
    shift = np.where(env > env.max() * 0.05)[0][0] * hop / sr - first * spb
    print(f"ベースのステムの時刻合わせ: {shift:+.3f} 秒")
    t = 0.0; res = []
    for tk in bass.split():
        m = re.match(r"^([A-G]#?)(-?\d):([\d.]+)", tk)
        d = float(re.match(r"^[^:]*:([\d.]+)", tk).group(1))
        if m and d >= 0.5:
            midi = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"].index(m.group(1)) + (int(m.group(2)) + 1) * 12
            a = int((t * spb + shift + 0.06) * sr); b = int((t * spb + shift + min(d * spb, 0.35)) * sr)
            f = f0(y[a:b], sr)
            if f:
                est = 69 + 12 * np.log2(f / 440)
                # 1オクターブ違い（倍音を拾った）を許す
                err = min(abs(est - midi), abs(est - midi - 12), abs(est - midi + 12))
                res.append((tk, midi, round(est, 2), round(err * 100)))
        t += d
    errs = np.array([r[3] for r in res])
    ok = np.sum(errs <= 50)
    print(f"ベースの音程: {len(res)} 音を測定、半音の半分（50セント）以内 {ok}（{100*ok/max(1,len(res)):.0f}%）、中央値のずれ {np.median(errs):.0f} セント")
    for r in res:
        if r[3] > 50: print("   ずれ:", r)

if __name__ == "__main__":
    main(*sys.argv[1:])
