#!/usr/bin/env python3
"""分析ソフトの答え合わせ: 自分の曲（JSON があるので正解が分かる）で、カルテがどれだけ当たっているかを測る。
使い方: python3 tools/song-analyzer/eval_own.py <カルテ.json> <曲の.json>   （曲の .json.secs があれば場面の区切りも見る）"""
import sys, os, re, json, numpy as np
k = json.load(open(sys.argv[1])); js = json.load(open(sys.argv[2])); bpm = js["bpm"]; spb = 60 / bpm
CLS = lambda p: ("drums" if p.get("instrument") in ("kick", "snare", "hihat", "crash", "tom", "ride", "cymbal") else "bass" if p.get("instrument") == "bass" else
                 "guitar" if "uitar" in str(p.get("instrument")) and p.get("patch") not in ("kawaiiFx", "cymbalFx") else "piano" if p.get("instrument") == "piano" else "other")
def spans(notes):
    if notes.startswith("g:"): return [(i * 0.25, i * 0.25 + 0.25) for i, c in enumerate(notes[2:]) if c not in ". "]
    t = 0; out = []
    for tok in notes.split():
        q = tok.split(":"); m = re.match(r"[0-9.]+", q[1]) if len(q) > 1 else None
        if not m: continue
        L = float(m.group(0))
        if q[0] != "R": out.append((t, t + L))
        t += L
    return out
T = {c: [] for c in ("vocals", "drums", "bass", "guitar", "piano", "other")}
for p in js["parts"]: T[CLS(p)] += spans(p["notes"])
for v in js.get("vocals", []): T["vocals"] += spans(v["notes"])
T = {"vocals": T["vocals"], "drums": T["drums"], "bass": T["bass"], "chordal": T["guitar"] + T["piano"] + T["other"]}
times = np.array(k["per_bar"]["time"]); nb = len(times); barlen = float(np.median(np.diff(times)))
def truth(c, off):
    out = np.zeros(nb)
    for i in range(nb):
        a, b = (times[i] - off) / spb, (times[i] + barlen - off) / spb; cov = sum(max(0, min(e, b) - max(s, a)) for s, e in T[c]); out[i] = min(1, cov / (b - a))
    return out
best = max(np.arange(0, 1.6, 0.05), key=lambda o: np.corrcoef(truth("drums", o), k["per_bar"]["active"]["drums"])[0, 1] if np.std(truth("drums", o)) > 0 else -1)
print(f"テンポ: カルテ {k['tempo']}・正解 {bpm}（{'合っている' if abs(k['tempo'] - bpm) < 3 else ('半分' if abs(k['tempo'] * 2 - bpm) < 5 else ('2倍' if abs(k['tempo'] / 2 - bpm) < 3 else 'ちがう'))}）  頭のずれ {best:.2f}秒")
print("楽器が鳴っているか（小節ごと。正解＝その小節の 30% 以上で音がある）:")
for c in T:
    tr = truth(c, best) > 0.3; pr = np.array(k["per_bar"]["active"][c]) > 0.3
    if not tr.any() and not pr.any(): print(f"  {c:7s} 正解も答えも「なし」"); continue
    tp = (tr & pr).sum(); print(f"  {c:7s} 正解 {tr.mean() * 100:3.0f}%・答え {pr.mean() * 100:3.0f}%  当たり {(tr == pr).mean() * 100:3.0f}%  （見のがし {(tr & ~pr).sum()} 小節・空ぶり {(~tr & pr).sum()} 小節）")
sf = sys.argv[2] + ".secs"
if os.path.exists(sf):
    secs = json.load(open(sf)); tb = [x["t"] + best for x in secs][1:]; pb = [s["start_sec"] for s in k["sections"]][1:]; tol = 2 * spb * 2 + 0.3
    hit = sum(1 for t in tb if any(abs(t - p) <= tol for p in pb)); good = sum(1 for p in pb if any(abs(t - p) <= tol for t in tb))
    print(f"場面の区切り（±{tol:.1f}秒）: 正解 {len(tb)} か所のうち {hit} か所を見つけた・答え {len(pb)} か所のうち {good} か所が正しい")
    print("  正解:", " ".join(f"{t:.0f}" for t in tb)); print("  答え:", " ".join(f"{p:.0f}" for p in pb))
