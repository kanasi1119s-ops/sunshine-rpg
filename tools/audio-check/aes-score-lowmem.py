#!/usr/bin/env python3
"""aes-score.py と同じ点数（Audiobox Aesthetics）を、少ないメモリで出す（2026-10-19。メモリ 4GB のパソコンで5分の曲を採点するため）。
モデルは曲を10秒ずつに分けて一度にまとめて計算する。ここでは同じ10秒の区切りを、数個ずつに分けて計算し、同じ重みで平均する（結果は同じ）。
使い方: HF_HOME=... python3 aes-score-lowmem.py a.wav b.wav ...   （--group 4 で一度に計算する区切りの数）"""
import sys, soundfile as sf, torch, torchaudio
def _load(path, *a, **k):
    d, sr = sf.read(path, dtype='float32', always_2d=True)
    return torch.from_numpy(d.T.copy()), sr
torchaudio.load = _load
torchaudio.info = lambda p: type('I', (), {'sample_rate': sf.info(p).samplerate})()
from audiobox_aesthetics.infer import initialize_predictor, make_inference_batch, AXES_NAME

args = sys.argv[1:]; group = 4
if "--group" in args:
    i = args.index("--group"); group = int(args[i + 1]); del args[i:i + 2]
pred = initialize_predictor()
torch.set_num_threads(2)
for p in args:
    with torch.inference_mode():
        wavs = pred.audio_resample_mono([{"path": p}])
        ws, ms, wts, bids = make_inference_batch(wavs, 10, 10, sample_rate=pred.sample_rate)
        acc = {a: 0.0 for a in AXES_NAME}; wsum = 0.0
        for k in range(0, len(ws), group):
            out = pred.model({"wav": torch.stack(ws[k:k + group]).to(pred.device), "mask": torch.stack(ms[k:k + group]).to(pred.device)})
            w = torch.tensor(wts[k:k + group], dtype=torch.float32)
            for a in AXES_NAME:
                acc[a] += float((pred.target_transform[a].inverse(out[a]).float().cpu() * w).sum())
            wsum += float(w.sum())
    print(p.split('/')[-1], {a: round(acc[a] / wsum, 2) for a in AXES_NAME}, flush=True)
