#!/usr/bin/env python3
"""Audiobox Aesthetics（Meta、公開モデル）で音楽を4つの点数にする。耳の代わりではなく比較の目安。
使い方: HF_HOME=/tmp/hf python3 aes-score.py a.wav b.wav ...
CE=楽しさ CU=役に立つ度 PC=複雑さ PQ=制作品質（各1〜10）"""
import sys, soundfile as sf, torch, torchaudio
def _load(path, *a, **k):
    d, sr = sf.read(path, dtype='float32', always_2d=True)
    return torch.from_numpy(d.T.copy()), sr
torchaudio.load = _load
torchaudio.info = lambda p: type('I', (), {'sample_rate': sf.info(p).samplerate})()
from audiobox_aesthetics.infer import initialize_predictor
pred = initialize_predictor()
for p in sys.argv[1:]:
    r = pred.forward([{"path": p}])[0]
    print(p.split('/')[-1], {k: round(v, 2) for k, v in r.items()})
