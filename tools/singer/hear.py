#!/usr/bin/env python3
"""歌声の聞き取りの点検: 音声認識（Whisper）で歌詞がどれくらい聞き取れるかを数える。
  python3 tools/singer/hear.py <歌.wav> [正しい歌詞（ひらがな）] [--model openai/whisper-base]
自分では音を聴けないので、「機械が歌詞を聞き取れるか」をはっきり歌えているかの目安にする。
"""
import sys, os, warnings
warnings.filterwarnings("ignore")
os.environ.setdefault("HF_HUB_OFFLINE", "1")
import numpy as np, soundfile as sf
from scipy import signal

def to_hira(s):
    return "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c for c in s)

def kana_only(s):
    s = to_hira(s)
    return "".join(c for c in s if "ぁ" <= c <= "ゖ" or c == "ー")

def hear(path, model="openai/whisper-base"):
    import torch
    from transformers import WhisperProcessor, WhisperForConditionalGeneration
    pr = WhisperProcessor.from_pretrained(model); m = WhisperForConditionalGeneration.from_pretrained(model)
    x, sr = sf.read(path, dtype="float32", always_2d=True); x = x.mean(1)
    x = signal.resample_poly(x, 16000, sr)
    outs = []
    for i in range(0, len(x), 16000 * 28):
        seg = x[i:i + 16000 * 28]
        f = pr(seg, sampling_rate=16000, return_tensors="pt").input_features
        with torch.no_grad():
            ids = m.generate(f, language="ja", task="transcribe")
        outs.append(pr.batch_decode(ids, skip_special_tokens=True)[0])
    return "".join(outs)

def kana_of(text):
    """漢字まじりの答えも、読み（ひらがな）に直して比べる（pykakasi があれば）"""
    try:
        import pykakasi
        k = pykakasi.kakasi()
        return "".join(w["hira"] for w in k.convert(text))
    except Exception:
        return to_hira(text)

def score(ref, hyp):
    import difflib
    a, b = kana_only(ref), kana_only(kana_of(hyp))
    return difflib.SequenceMatcher(None, a, b).ratio(), b

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    model = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else "openai/whisper-base"
    h = hear(a[0], model)
    print("聞き取り:", h)
    if len(a) > 1:
        r, k = score(a[1], h)
        print(f"読み: {k}\n一致: {r * 100:.0f}%")
