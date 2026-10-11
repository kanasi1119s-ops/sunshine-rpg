#!/usr/bin/env python3
"""曲の「和声のくせ」を数値で測る道具（2026-10-11）。参考にしたい録音から、コード進行の作り方を学ぶための分析。

使い方:
    python3 tools/audio-check/analyze-chords.py 曲1.mp3 [曲2.mp3 ...] [--out 結果.json] [--bpm 160]

測るもの（統計だけ。曲ごとのコードの並びは出さない・保存しない）:
- キー（主音と長調/短調）の推定
- コードチェンジの細かさ（1小節に何回変わるか）
- 度数ごとの使用割合（主音を I/i として、I・ii・IV・V・♭VII など。時間の割合）
- コードの種類の割合（長3和音・短3和音・属7）
- 度数の移り変わりの割合（例: IV→I が全体の何%）。複数曲を渡すと、全部を合算した割合も出す
著作権: 「曲のコード進行をそのまま写す」ためではなく、「こういう和声の作りが多い」という傾向を知るため。
        曲ごとのコードの並び（進行そのもの）は、結果に含めない（CLAUDE.md 1-1）。
必要なもの: ffmpeg、numpy、scipy。
精度: 録音からの自動推定なので、3和音への当てはめ（テンション・転回は区別しない）。歪んだギターが厚い曲は、5度（パワーコード）が多く、長/短の判定がぶれる。目安として使う。
"""
import importlib.util, json, os, subprocess, sys
import numpy as np
from scipy.signal import stft

NAMES = ["I", "♭II", "II", "♭III", "III", "IV", "♯IV", "V", "♭VI", "VI", "♭VII", "VII"]
KS_MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
KS_MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


def load(path, sr=22050):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32), sr


def rhythm_mod():
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location("analyze_rhythm", os.path.join(here, "analyze-rhythm.py"))
    m = importlib.util.module_from_spec(spec)
    sys.argv_backup = sys.argv; spec.loader.exec_module(m)
    return m


def chroma_frames(x, sr, frame_sec):
    """ビート1つ分ごとの12音のクロマ（音名ごとの強さ）。ドラムの打撃音をさけるため、低い音と高すぎる音は使わない。"""
    n = 8192
    f, t, Z = stft(x, sr, nperseg=n, noverlap=n - 2048)
    mag = np.abs(Z)
    sel = (f >= 80) & (f <= 2000)
    f2 = f[sel]
    # 周波数 → 音名（0=C）。倍音で4度/5度がにごらないよう、帯域ごとに平均を引く
    midi = 69 + 12 * np.log2(np.maximum(f2, 1e-3) / 440.0)
    pc = np.round(midi).astype(int) % 12
    C = np.zeros((12, mag.shape[1]))
    m2 = np.log1p(mag[sel] * 20)
    m2 = m2 - np.median(m2, axis=0, keepdims=True)
    m2 = np.maximum(m2, 0)
    for k in range(12):
        C[k] = m2[pc == k].sum(axis=0)
    hop_sec = 2048 / sr
    per = max(1, int(round(frame_sec / hop_sec)))
    nf = C.shape[1] // per
    out = np.stack([C[:, i * per:(i + 1) * per].mean(axis=1) for i in range(nf)])
    out /= np.linalg.norm(out, axis=1, keepdims=True) + 1e-9
    return out


def templates():
    T, lab = [], []
    for r in range(12):
        for q, iv in (("", (0, 4, 7)), ("m", (0, 3, 7)), ("7", (0, 4, 7, 10))):
            v = np.zeros(12)
            for j, i in enumerate(iv):
                v[(r + i) % 12] = 1.0 if j < 3 else 0.55
            T.append(v / np.linalg.norm(v)); lab.append((r, q))
    return np.array(T), lab


def viterbi(sc, stay=0.85):
    n, k = sc.shape
    lp_stay, lp_move = np.log(stay), np.log((1 - stay) / (k - 1))
    dp = sc[0].copy(); bp = np.zeros((n, k), dtype=int)
    for i in range(1, n):
        best = dp.argmax(); move = dp[best] + lp_move
        stay_s = dp + lp_stay
        use_stay = stay_s >= move
        bp[i] = np.where(use_stay, np.arange(k), best)
        dp = np.where(use_stay, stay_s, move) + sc[i]
    path = np.zeros(n, dtype=int); path[-1] = dp.argmax()
    for i in range(n - 1, 0, -1): path[i - 1] = bp[i, path[i]]
    return path


def estimate_key(chroma):
    prof = chroma.mean(axis=0)
    best = (-9, 0, "major")
    for r in range(12):
        for mode, ks in (("major", KS_MAJ), ("minor", KS_MIN)):
            c = np.corrcoef(prof, np.roll(ks, r))[0, 1]
            if c > best[0]: best = (c, r, mode)
    return best[1], best[2], best[0]


def analyze(path, bpm=None):
    x, sr = load(path)
    rm = rhythm_mod()
    if bpm is None:
        on, _, hop = rm.band_onsets(x, sr)
        bpm = rm.tempo_of(on, sr, hop)
    beat = 60.0 / bpm
    ch = chroma_frames(x, sr, beat)
    T, lab = templates()
    sc = ch @ T.T * 6.0
    path = viterbi(sc)
    tonic, mode, kc = estimate_key(ch)
    # 同じコードが続く区間にまとめる（最短1拍）
    seg = []
    for i, s in enumerate(path):
        if seg and seg[-1][0] == s: seg[-1][1] += 1
        else: seg.append([s, 1])
    total = sum(d for _, d in seg)
    use, qual, trans = {}, {"長3和音": 0.0, "短3和音": 0.0, "属7": 0.0}, {}
    prev = None
    for s, d in seg:
        r, q = lab[s]
        deg = NAMES[(r - tonic) % 12]
        name = deg + {"": "", "m": "m", "7": "7"}[q]
        use[name] = use.get(name, 0) + d
        qual[{"": "長3和音", "m": "短3和音", "7": "属7"}[q]] += d
        if prev is not None and prev != name:
            key = f"{prev}→{name}"; trans[key] = trans.get(key, 0) + 1
        prev = name
    changes = len(seg) - 1
    bars = total / 4.0
    return {
        "bpm": round(float(bpm), 1), "key_tonic": int(tonic), "mode": mode, "key_confidence": round(float(kc), 2),
        "seconds": round(len(x) / sr, 1), "bars": round(bars, 1),
        "changes_per_bar": round(changes / bars, 2),
        "degree_use_percent": {k: round(100 * v / total, 1) for k, v in sorted(use.items(), key=lambda kv: -kv[1]) if v / total >= 0.01},
        "quality_percent": {k: round(100 * v / total, 1) for k, v in qual.items()},
        "_trans": trans,
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = None; bpm = None
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]; args = [a for a in args if a != out]
    if "--bpm" in sys.argv:
        bpm = float(sys.argv[sys.argv.index("--bpm") + 1]); args = [a for a in args if a != sys.argv[sys.argv.index("--bpm") + 1]]
    res = {}
    all_tr, all_use, n = {}, {}, 0
    for p in args:
        r = analyze(p, bpm)
        tr = r.pop("_trans")
        for k, v in tr.items(): all_tr[k] = all_tr.get(k, 0) + v
        for k, v in r["degree_use_percent"].items(): all_use[k] = all_use.get(k, 0) + v
        n += 1
        res[os.path.basename(p)] = r
        print(os.path.basename(p), json.dumps(r, ensure_ascii=False))
    if n > 1:
        tot = sum(all_tr.values()) or 1
        res["_まとめ（曲ごとの並びは含まない）"] = {
            "曲数": n,
            "度数の使用割合の平均": {k: round(v / n, 1) for k, v in sorted(all_use.items(), key=lambda kv: -kv[1])[:12]},
            "度数の移り変わり（全体に対する割合）": {k: round(100 * v / tot, 1) for k, v in sorted(all_tr.items(), key=lambda kv: -kv[1])[:12]},
        }
        print(json.dumps(res["_まとめ（曲ごとの並びは含まない）"], ensure_ascii=False, indent=1))
    if out:
        json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
