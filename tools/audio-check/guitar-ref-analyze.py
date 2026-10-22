# 使い方: python3 tools/audio-check/guitar-ref-analyze.py <参考の guitar.wav> <こちらの guitar.wav>（音源分離: python3 -m demucs -n htdemucs_6s -j 1 --segment 7 -d cpu -o sep <曲.wav>）
# ギターの音を数字で比べる（参考の曲と、こちらの曲。どちらも音源分離した guitar を使う）
# 出すもの: 1/3オクターブごとの平均の大きさ（全体の大きさをそろえた差）、左右の広がり、音の粒の立ち方（波高率）、明るさ（重心）
import sys, numpy as np, soundfile as sf

BANDS = [63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000]


def load(p):
    x, sr = sf.read(p, always_2d=True)
    return x.astype(np.float64), sr


def active(x, sr, thr_db=-40):
    """鳴っている所だけ（ギターが休んでいる所を除く）"""
    m = x.mean(1)
    hop = sr // 10
    rms = np.array([np.sqrt(np.mean(m[i:i + hop] ** 2) + 1e-12) for i in range(0, len(m) - hop, hop)])
    db = 20 * np.log10(rms)
    keep = db > db.max() + thr_db
    idx = np.concatenate([np.arange(i * hop, i * hop + hop) for i in np.where(keep)[0]])
    return x[idx]


def spectrum(x, sr):
    m = x.mean(1)
    n = 8192
    win = np.hanning(n)
    acc = np.zeros(n // 2 + 1); k = 0
    for i in range(0, len(m) - n, n // 2):
        acc += np.abs(np.fft.rfft(m[i:i + n] * win)) ** 2; k += 1
    acc /= max(k, 1)
    f = np.fft.rfftfreq(n, 1 / sr)
    out = []
    for c in BANDS:
        lo, hi = c / 2 ** (1 / 6), c * 2 ** (1 / 6)
        sel = (f >= lo) & (f < hi)
        out.append(10 * np.log10(acc[sel].mean() + 1e-20))
    out = np.array(out)
    return out - out.max()


def stats(p):
    x, sr = load(p)
    x = active(x, sr)
    L, R = x[:, 0], x[:, 1]
    M, S = (L + R) / 2, (L - R) / 2
    corr = np.corrcoef(L, R)[0, 1]
    side = 20 * np.log10(np.sqrt(np.mean(S ** 2)) / np.sqrt(np.mean(M ** 2)) + 1e-12)
    crest = 20 * np.log10(np.max(np.abs(M)) / np.sqrt(np.mean(M ** 2)))
    hop = sr // 20
    st = np.array([np.sqrt(np.mean(M[i:i + hop] ** 2)) for i in range(0, len(M) - hop, hop)])
    st_db = 20 * np.log10(st + 1e-9)
    dyn = np.percentile(st_db, 95) - np.percentile(st_db, 10)
    F = np.abs(np.fft.rfft(M[: sr * 30] if len(M) > sr * 30 else M))
    fr = np.fft.rfftfreq(len(M[: sr * 30] if len(M) > sr * 30 else M), 1 / sr)
    cent = float((F * fr).sum() / F.sum())
    return spectrum(x, sr), dict(corr=round(corr, 3), side_db=round(side, 1), crest_db=round(crest, 1), dyn_db=round(dyn, 1), centroid_hz=round(cent))


if __name__ == "__main__":
    a, b = sys.argv[1], sys.argv[2]
    sa, ia = stats(a); sb, ib = stats(b)
    print("参考:", ia); print("こちら:", ib)
    print(f"{'帯域Hz':>7} {'参考':>6} {'こちら':>6} {'差':>6}")
    for c, x, y in zip(BANDS, sa, sb):
        print(f"{c:>7} {x:6.1f} {y:6.1f} {y - x:+6.1f}")
