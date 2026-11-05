#!/usr/bin/env python3
"""区間ごとの点数（Audiobox の PQ を10秒ずつ）。どの場面で点数が下がっているかを見る（2026-11-06）。
使い方: HF_HOME=/tmp/hf python3 segscore.py <wav か mp3> [場面の秒 .secs]"""
import sys, json, subprocess, tempfile, os
import soundfile as sf, torch, torchaudio
def _load(path, *a, **k):
    d, sr = sf.read(path, dtype='float32', always_2d=True)
    return torch.from_numpy(d.T.copy()), sr
torchaudio.load = _load
torchaudio.info = lambda p: type('I', (), {'sample_rate': sf.info(p).samplerate})()
from audiobox_aesthetics.infer import initialize_predictor, make_inference_batch

src = sys.argv[1]; secs = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else []
if not src.endswith(".wav"):
    tmp = tempfile.mktemp(suffix=".wav"); subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, tmp], check=True); src = tmp
pred = initialize_predictor(); torch.set_num_threads(2)
with torch.inference_mode():
    wavs = pred.audio_resample_mono([{"path": src}])
    ws, ms, wts, bids = make_inference_batch(wavs, 10, 10, sample_rate=pred.sample_rate)
    pq = []
    for k in range(0, len(ws), 4):
        out = pred.model({"wav": torch.stack(ws[k:k + 4]), "mask": torch.stack(ms[k:k + 4])})
        pq += [float(x) for x in pred.target_transform["PQ"].inverse(out["PQ"]).float().cpu()]


def scene_at(t):
    name = ""
    for s in secs:
        if s["t"] <= t: name = s["name"]
    return name


for i, v in enumerate(pq):
    t = i * 10
    print(f"{t // 60:2.0f}:{t % 60:02.0f}  {v:5.2f}  {scene_at(t + 5)}")
print("平均", round(sum(pq) / len(pq), 2))
