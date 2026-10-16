#!/usr/bin/env python3
"""楽器ごとの点検（2026-10-17、人間の指示「数値ってシステムチェックでさらに細かくできたりする？波形を種類別にするとか」）。
inspect.mjs が楽器の種類ごとに書き出した WAV（同じ尺度の音量）を受け取り、1つずつ数値にする。耳の代わりではなく、場所の候補を出す道具。

  python3 tools/audio-check/part-inspect.py <manifest.json> [--aes]

manifest.json: {"groups": [{"key": "g3", "label": "アコギ", "wav": "...", "parts": [..]}], "mix": "<全体の WAV>"}
測るもの（楽器ごと）:
  大きさ    : 鳴っている間の RMS（dBFS）と、いちばん大きい楽器との差
  帯域      : 低（<250Hz）・中低（250-800）・中（800-2.5k）・高（2.5k-6k）・空気（>6k）の割合（その楽器の全体を 0dB）
  重心      : 音の明るさ（Hz）。高いほど明るく硬い、低いほどこもる
  硬さ      : 音の出だしの鋭さ（10ms ごとの大きさの、上位0.5% と中央値の差 dB）。大きいほど「カツッ」と硬い
  プチッ    : 波形の飛び（tools/audio-check/noise-check.py と同じ方法）の数と時刻
  点数      : --aes のとき、楽器だけの音の Audiobox の点数（PQ）
  ぶつかり  : 2つの楽器が、同じ帯域・同じ時間に重なって鳴る度合い（0〜1）。大きい組み合わせを上から
"""
import sys, json, os, importlib.util
import numpy as np, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("noise", os.path.join(HERE, "noise-check.py")); noise = importlib.util.module_from_spec(spec); spec.loader.exec_module(noise)
BANDS = [("低", 20, 250), ("中低", 250, 800), ("中", 800, 2500), ("高", 2500, 6000), ("空気", 6000, 20000)]

def db(x): return 20 * np.log10(max(float(x), 1e-12))

def analyze(path):
    x, fs = sf.read(path, dtype="float32", always_2d=True)
    m = x.mean(1)
    hop = int(0.1 * fs); n = len(m) // hop
    rms = np.sqrt((m[: n * hop].reshape(n, hop) ** 2).mean(1) + 1e-20)
    active = rms > rms.max() * 10 ** (-35 / 20)
    act_rms = db(np.sqrt((rms[active] ** 2).mean())) if active.any() else -120
    # 帯域・重心（鳴っている所だけ、0.37秒の窓で）
    N = 16384; spec_sum = np.zeros(N // 2 + 1)
    win = np.hanning(N)
    for s in range(0, len(m) - N, N):
        seg = m[s:s + N]
        if np.sqrt((seg ** 2).mean()) < rms.max() * 10 ** (-35 / 20): continue
        spec_sum += np.abs(np.fft.rfft(seg * win)) ** 2
    f = np.fft.rfftfreq(N, 1 / fs); tot = spec_sum.sum() + 1e-20
    bands = {nm_: round(db(np.sqrt(spec_sum[(f >= a) & (f < b)].sum() / tot)), 1) for nm_, a, b in BANDS}
    cen = float((np.sqrt(spec_sum) * f).sum() / (np.sqrt(spec_sum).sum() + 1e-20))
    # 硬さ（10ms の大きさの上位0.5%と中央値の差。鳴っている所だけ）
    w = int(0.01 * fs); k = len(m) // w
    r10 = np.sqrt((m[: k * w].reshape(k, w) ** 2).mean(1) + 1e-20)
    on = r10 > r10.max() * 10 ** (-35 / 20)
    hard = db(np.percentile(r10[on], 99.5) / np.median(r10[on])) if on.sum() > 20 else 0
    # プチッ
    try:
        clicks = noise.check_clicks(x, fs) if hasattr(noise, "check_clicks") else None
    except Exception:
        clicks = None
    return dict(fs=fs, mono=m, active_rms=round(act_rms, 1), bands=bands, centroid=int(cen), hard=round(hard, 1), clicks=clicks, spec=spec_sum, f=f)

def clicks_of(path):
    import subprocess
    r = subprocess.run([sys.executable, os.path.join(HERE, "noise-check.py"), path, "--json", "--top", "6"], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
        for it in d["items"]:
            if it["name"] == "プチッ": return it["value"], it.get("times", [])[:6]
    except Exception:
        pass
    return None, []

def overlap(a, b):
    """2つの楽器の、時間と帯域の重なり（0〜1）。0.5秒ごと・1/3オクターブの帯域ごとに、両方が鳴っている力の割合"""
    fs = a["fs"]; L = min(len(a["mono"]), len(b["mono"])); N = 4096; hop = int(0.5 * fs)
    edges = 100 * 2 ** (np.arange(0, 21) / 3)   # 100Hz〜10kHz
    f = np.fft.rfftfreq(N, 1 / fs); idx = [np.where((f >= edges[i]) & (f < edges[i + 1]))[0] for i in range(len(edges) - 1)]
    num = den = 0.0; w = np.hanning(N)
    for s in range(0, L - N, hop):
        A = np.abs(np.fft.rfft(a["mono"][s:s + N] * w)) ** 2; B = np.abs(np.fft.rfft(b["mono"][s:s + N] * w)) ** 2
        ea = np.array([A[i].sum() for i in idx]); eb = np.array([B[i].sum() for i in idx])
        num += np.minimum(ea, eb).sum(); den += np.minimum(ea.sum(), eb.sum()) + 1e-20
    return num / den if den else 0.0

def main():
    man = json.load(open(sys.argv[1])); want_aes = "--aes" in sys.argv
    pred = None
    if want_aes:
        import torch, torchaudio
        def _load(p, *a, **k):
            d, sr = sf.read(p, dtype="float32", always_2d=True); return torch.from_numpy(d.T.copy()), sr
        torchaudio.load = _load
        torchaudio.info = lambda p: type("I", (), {"sample_rate": sf.info(p).samplerate})()
        from audiobox_aesthetics.infer import initialize_predictor
        pred = initialize_predictor()
    res = []
    for g in man["groups"]:
        a = analyze(g["wav"]); a["key"] = g["key"]; a["label"] = g["label"]
        a["clicks_n"], a["clicks_t"] = clicks_of(g["wav"])
        if pred:
            # 60秒ずつ切って平均（長いとメモリが足りない）
            x, fs = sf.read(g["wav"], dtype="float32", always_2d=True); L = 60 * fs; pqs = []
            for s in range(0, max(1, len(x) - 10 * fs), L):
                seg = x[s:s + L]
                if np.sqrt((seg ** 2).mean()) < 1e-4: continue
                import torch
                pqs.append(pred.forward([{"path": torch.from_numpy(seg.T.copy()), "sample_rate": fs}])[0]["PQ"])
            a["pq"] = round(float(np.mean(pqs)), 2) if pqs else None
        res.append(a)
    top = max(r["active_rms"] for r in res)
    print("■ 楽器ごとの点検（同じ尺度の音量。帯域はその楽器の全体を 0dB とした割合）")
    hdr = "  楽器" + " " * 14 + "大きさ(差)  重心Hz  硬さ  " + "  ".join(f"{b[0]:>3}" for b in BANDS) + "  プチッ" + ("  点数" if pred else "")
    print(hdr)
    for r in sorted(res, key=lambda r: -r["active_rms"]):
        import unicodedata
        wid = lambda t: sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in t)
        lab = r["label"]
        while wid(lab) > 20: lab = lab[:-1]
        lab = lab + " " * (20 - wid(lab))
        line = f"  {lab} {r['active_rms']:6.1f}({r['active_rms'] - top:+5.1f}) {r['centroid']:6d} {r['hard']:5.1f}  " + "  ".join(f"{r['bands'][b[0]]:5.1f}" for b in BANDS)
        line += f"  {r['clicks_n'] if r['clicks_n'] is not None else '-':>4}" + (f" {','.join(str(round(t)) for t in r['clicks_t'][:3])}秒" if r['clicks_n'] else "")
        if pred: line += f"  {r.get('pq')}"
        print(line)
    # ぶつかり（大きい楽器どうしだけ）
    big = [r for r in res if r["active_rms"] > top - 18]
    pairs = []
    for i in range(len(big)):
        for j in range(i + 1, len(big)):
            pairs.append((overlap(big[i], big[j]), big[i]["label"], big[j]["label"]))
    pairs.sort(reverse=True)
    print("■ ぶつかり（同じ帯域・同じ時間に重なる度合い。0.5 を超えると濁りやすい）")
    for v, a, b in pairs[:6]: print(f"  {v:.2f}  {a} × {b}")
    # 目安の注意
    print("■ 気づいたこと")
    for r in res:
        if r["clicks_n"]: print(f"  ・{r['label']}: プチッ {r['clicks_n']}か所（{', '.join(str(round(t, 1)) for t in r['clicks_t'][:4])}秒）")
        if r["hard"] > 14 and not any(w in r["label"] for w in ("ドラム", "鉄琴", "木琴", "ティンパニ", "大太鼓", "ボーラン")): print(f"  ・{r['label']}: 出だしが硬い（硬さ {r['hard']}dB）。強い音（!）を減らす・bright を下げる・eq の high を下げる")
        if r["bands"]["空気"] > -18 and "ドラム" not in r["label"] and "鉄琴" not in r["label"] and "シンバル" not in r["label"]: print(f"  ・{r['label']}: 6kHz より上が多い（{r['bands']['空気']}dB）。耳に強いかもしれない")
    json.dump([{k: v for k, v in r.items() if k not in ("mono", "spec", "f")} for r in res], open(os.path.splitext(sys.argv[1])[0] + ".result.json", "w"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
