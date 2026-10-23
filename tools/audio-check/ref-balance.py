# 参考録音（音源分離）と、こちら（only-*.wav＝ほかのパートを休符にして書き出した1本ずつ）の楽器どうしの大きさの比を比べ、パートの音量に掛ける dB を出す（2026-10-23。作業用のパスは書きかえて使う）
# 参考の曲の「楽器どうしの大きさの比」（ギター基準）と、こちらの EQ 後の比を比べ、パートの音量に掛ける dB を出す
import sys, json, numpy as np, soundfile as sf
from scipy.signal import lfilter
sys.path.insert(0, "/tmp/ref")
from fit import biq

def fx_chain(fx):
    ch = []
    for f in fx:
        if f["type"] == "filter": ch.append((f["kind"], f["freq"], 0, f.get("q", 0.7)))
        elif f["type"] == "eq":
            if f.get("low"): ch.append(("lowshelf", 150, f["low"]))
            if f.get("mid"): ch.append(("peaking", min(max(f["midHz"], 200), 6000), f["mid"], 0.9))
            if f.get("high"): ch.append(("highshelf", 4500, f["high"]))
    return ch

def rms_db(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)

def level(path, fx=None):
    x, sr = sf.read(path, always_2d=True); m = x.mean(1)
    for k in fx_chain(fx or []):
        b, a = biq(*k); m = lfilter(b, a, m)
    return rms_db(m)

ours = {"gtr": "only-gtr", "bass": "only-bass", "drums": "only-drums", "vocal": "only-lead", "other": "only-other"}
stem = {"gtr": "guitar", "bass": "bass", "drums": "drums", "vocal": "vocals", "other": "other"}
eqk = {"gtr": "guitar", "bass": "bass", "drums": "drums", "vocal": "vocal", "other": "other"}
out = {}
for k in ["bmth", "mga", "mesh", "bbs", "lp", "tri"]:
    ref = {g: level(f"{k}/sep/htdemucs_6s/ref/{stem[g]}.wav") for g in ours}
    me = {g: level(f"/tmp/lm25/tone/only/{ours[g]}.wav", json.load(open(f"eq_{k}_{eqk[g]}.json"))) for g in ours}
    adj = {g: round((ref[g] - ref["gtr"]) - (me[g] - me["gtr"]), 1) for g in ours if g != "gtr"}
    # 大きく動かしすぎない（±12dB まで）
    adj = {g: max(-18.0, min(18.0, v)) for g, v in adj.items()}
    out[k] = adj
    print(k, "参考（ギター比）", {g: round(ref[g] - ref["gtr"], 1) for g in ours if g != "gtr"}, "→ 足す dB", adj)
json.dump(out, open("balance.json", "w"), ensure_ascii=False, indent=1)
