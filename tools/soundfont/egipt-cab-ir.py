#!/usr/bin/env python3
"""EG-IPT（CC BY 4.0）の「同じ演奏の DI 録音」と「アンプ→4x12 キャビネット（V30）をマイクで録った音」の組から、
キャビネットIR（アンプの線形な音色＋箱＋マイク）を計算で作る（デコンボリューション）。

使い方: python3 -I tools/soundfont/egipt-cab-ir.py <egipt-fetch.py で取り出したフォルダ> [--out assets-src/ir/egipt]
  取り出し例: python3 -I tools/soundfont/egipt-fetch.py /tmp/egipt/ir \
     'HB-bridge/(DI|dyn|cond|rib)/ordinario/HB-bridge_ordinario_1[3-8]-(06|16|26|36)_' \
     'HB-bridge/(DI|dyn|cond|rib)/scratch/HB-bridge_scratch-card_172-(50|52|54|56|65)_' \
     'HB-bridge/(DI|dyn|cond|rib)/palmstrike/HB-bridge_palmstrike-strings_175-0[468]_'

作り方:
 1. 組ごとに、長い窓（65536点・半分ずつ重ねる・ハン窓）で DI のパワー Sxx、DI とマイクの相互スペクトル Sxy、マイクのパワー Syy を足し合わせる
    （数十の録音を平均するので、雑音やアンプのわずかな歪みは打ち消し合う＝ウィーナーの推定 H = Sxy / Sxx）。
 2. 大きさ |H| を、低い所は 1/12 オクターブ、高い所ほど広く（最大 1/3 オクターブ）、確からしさ（コヒーレンス）の重みでならす。
 3. コヒーレンスが 0.5 を下回る高い所（DI に音が少なく推定が不安定。ふつう 5〜8kHz より上）は、その手前の値から −24dB/オクターブで下げる。
    80Hz より下も同様に −12dB/オクターブ（ギターの最低音より下は測れないため）。＝端の処理
 4. 大きさから最小位相の IR を作る（ケプストラム）。マイクまでの距離の遅れ（2〜4ms）は消え、頭が 0 にそろう。
 5. 48kHz に直し、100ms（4800点）で切り、終わり 20% をなめらかに消し、山を 1 にそろえる。
 6. 確かめ: DI にこの IR を畳み込んだ音と、本物のマイク録音の大きさを 1/3 オクターブごとに比べ、差（dB）を表示する。
"""
import glob, os, re, sys
import numpy as np, soundfile as sf
from scipy.signal import resample_poly, fftconvolve

NFFT = 65536
args = sys.argv[1:]
src = args[0]
out = args[args.index("--out") + 1] if "--out" in args else os.path.join(os.path.dirname(__file__), "..", "..", "assets-src", "ir", "egipt")
os.makedirs(out, exist_ok=True)
MICS = {"dyn": "ダイナミックマイク（SM57 系）", "cond": "コンデンサーマイク（C414 系）", "rib": "リボンマイク"}


def pairs(mic):
    for di in sorted(glob.glob(os.path.join(src, "*__DI__*_DI.wav"))):
        m = di.replace("__DI__", f"__{mic}__").replace("_DI.wav", f"_{mic}.wav")
        if os.path.exists(m):
            yield di, m


def spectra(mic):
    w = np.hanning(NFFT)
    Sxx = np.zeros(NFFT // 2 + 1); Syy = np.zeros_like(Sxx); Sxy = np.zeros(NFFT // 2 + 1, complex)
    n = 0
    for di, mf in pairs(mic):
        x, sr = sf.read(di, dtype="float64"); y, sr2 = sf.read(mf, dtype="float64")
        if x.ndim > 1: x = x.mean(1)
        if y.ndim > 1: y = y.mean(1)
        L = min(len(x), len(y))
        x, y = x[:L], y[:L]
        for a in range(0, L - NFFT, NFFT // 2):
            X = np.fft.rfft(x[a:a + NFFT] * w); Y = np.fft.rfft(y[a:a + NFFT] * w)
            Sxx += np.abs(X) ** 2; Syy += np.abs(Y) ** 2; Sxy += np.conj(X) * Y
        n += 1
    return Sxx, Syy, Sxy, sr, n


def smooth(f, mag_db, coh):
    out = np.empty_like(mag_db)
    for i, fc in enumerate(f):
        if fc <= 0:
            out[i] = mag_db[i]; continue
        frac = 1 / 12 if fc < 2000 else min(1 / 3, 1 / 12 + (np.log2(fc / 2000)) * 0.12)
        lo, hi = fc * 2 ** (-frac / 2), fc * 2 ** (frac / 2)
        sel = (f >= lo) & (f <= hi)
        wgt = coh[sel] + 1e-6
        out[i] = (mag_db[sel] * wgt).sum() / wgt.sum()
    return out


def min_phase(mag):
    """大きさ（rfft の並び）から最小位相の IR（NFFT 点）を作る。"""
    full = np.concatenate([mag, mag[-2:0:-1]])
    cep = np.fft.ifft(np.log(np.maximum(full, 1e-9))).real
    fold = np.zeros_like(cep); fold[0] = cep[0]; fold[1:NFFT // 2] = 2 * cep[1:NFFT // 2]; fold[NFFT // 2] = cep[NFFT // 2]
    return np.fft.ifft(np.exp(np.fft.fft(fold))).real


def third_octave_err(h48, mic):
    """DI に IR を畳み込んだ音と、マイク録音の 1/3 オクターブごとの大きさの差（全体の大きさはそろえる）。"""
    errs = {}
    centers = [100, 160, 250, 400, 630, 1000, 1600, 2500, 4000, 6300]
    acc_a = np.zeros(len(centers)); acc_b = np.zeros(len(centers))
    for di, mf in list(pairs(mic))[:12]:
        x, sr = sf.read(di, dtype="float64"); y, _ = sf.read(mf, dtype="float64")
        x = resample_poly(x, 1, 2); y = resample_poly(y, 1, 2)
        z = fftconvolve(x, h48)[:len(x)]
        for k, (sig, acc) in enumerate([(z, acc_a), (y, acc_b)]):
            S = np.abs(np.fft.rfft(sig)) ** 2; f = np.fft.rfftfreq(len(sig), 1 / 48000)
            for j, c in enumerate(centers):
                acc[j] += S[(f >= c / 2 ** (1 / 6)) & (f < c * 2 ** (1 / 6))].sum()
    da = 10 * np.log10(acc_a + 1e-20); db = 10 * np.log10(acc_b + 1e-20)
    # 全体の大きさは 100Hz〜4kHz でそろえる（6.3kHz はマイク側がほぼ雑音の帯域なので、そろえる計算に入れない）
    d = (da - da[:-1].mean()) - (db - db[:-1].mean())
    return {c: float(v) for c, v in zip(centers, np.round(d, 1))}


made = {}
for mic, label in MICS.items():
    Sxx, Syy, Sxy, sr, n = spectra(mic)
    f = np.fft.rfftfreq(NFFT, 1 / sr)
    H = Sxy / (Sxx + 1e-6 * Sxx.mean())
    coh = np.abs(Sxy) ** 2 / (Sxx * Syy + 1e-30)
    mag_db = 20 * np.log10(np.abs(H) + 1e-12)
    sm = smooth(f, mag_db, coh)
    # 確からしさの高い範囲（コヒーレンスをならしたもの > 0.5）
    coh_s = np.convolve(coh, np.ones(64) / 64, mode="same")
    good = (coh_s > 0.5) & (f > 70)
    f_hi = f[good].max() if good.any() else 6000
    f_hi = float(min(max(f_hi, 4000), 9000))
    f_lo = 80.0
    i_hi = np.searchsorted(f, f_hi); i_lo = np.searchsorted(f, f_lo)
    sm[i_hi:] = sm[i_hi] - 24 * np.log2(np.maximum(f[i_hi:], f_hi) / f_hi)
    sm[:i_lo] = sm[i_lo] - 12 * np.log2(f_lo / np.maximum(f[:i_lo], 1.0))
    h = min_phase(10 ** (sm / 20))
    h48 = resample_poly(h[:NFFT // 4], 1, 2)[:4800]
    k = int(4800 * 0.2); h48[-k:] *= np.linspace(1, 0, k) ** 2
    h48 /= np.abs(h48).max()
    name = f"412-v30-{mic}"
    sf.write(os.path.join(out, name + ".wav"), h48.astype("float32"), 48000, subtype="FLOAT")
    made[mic] = h48
    print(f"{name}: 組 {n}・確かな範囲 80Hz〜{f_hi:.0f}Hz・コヒーレンス（300〜3000Hz の平均）{coh[(f > 300) & (f < 3000)].mean():.2f}")
    print("   DI＊IR とマイク録音の差（dB、1/3 オクターブ）:", third_octave_err(h48, mic))

# ダイナミックとリボンを半分ずつ（よく使う2本立ての組み合わせ）。位相がそろうよう、どちらも最小位相の IR を足す
mix = 0.5 * made["dyn"] / np.sqrt((made["dyn"] ** 2).sum()) + 0.5 * made["rib"] / np.sqrt((made["rib"] ** 2).sum())
mix /= np.abs(mix).max()
sf.write(os.path.join(out, "412-v30-mix.wav"), mix.astype("float32"), 48000, subtype="FLOAT")
print("412-v30-mix: dyn と rib を半分ずつ")
