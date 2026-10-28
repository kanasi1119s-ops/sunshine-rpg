# 10秒ごとの PQ（どの場面が点を下げているか）。使い方: HF_HOME=/tmp/hf python3 pq_chunks.py a.wav [b.wav...]
import sys, soundfile as sf, torch, torchaudio
def _load(path, *a, **k):
    d, sr = sf.read(path, dtype='float32', always_2d=True)
    return torch.from_numpy(d.T.copy()), sr
torchaudio.load = _load
torchaudio.info = lambda p: type('I', (), {'sample_rate': sf.info(p).samplerate})()
from audiobox_aesthetics.infer import initialize_predictor, make_inference_batch, AXES_NAME
pred = initialize_predictor(); torch.set_num_threads(2)
for p in sys.argv[1:]:
    with torch.inference_mode():
        wavs = pred.audio_resample_mono([{"path": p}])
        ws, ms, wts, bids = make_inference_batch(wavs, 10, 10, sample_rate=pred.sample_rate)
        vals = []
        for k in range(0, len(ws), 4):
            out = pred.model({"wav": torch.stack(ws[k:k + 4]).to(pred.device), "mask": torch.stack(ms[k:k + 4]).to(pred.device)})
            v = pred.target_transform["PQ"].inverse(out["PQ"]).float().cpu().tolist()
            vals += [float(x) for x in (v if isinstance(v, list) else [v])]
    print(p.split('/')[-1], " ".join(f"{i*10}s:{x:.1f}" for i, x in enumerate(vals)), flush=True)
