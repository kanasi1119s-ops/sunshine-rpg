#!/usr/bin/env python3
"""曲（JSON）の「音の伸ばし方」を、プロの編曲909曲（POP909。docs/sound/reference-pop909.md）の幅とくらべる（2026-11-15）。
使い方: python3 tools/vt3/sustain_check.py <曲.json>   … 幅（下から25%〜75%）の外に「←」を付ける。外でもよいが、わざと外したと言えること"""
import sys, os, re, json, importlib.util
here = os.path.dirname(os.path.abspath(__file__)); argv = sys.argv[:]; sys.argv = ["x", "/nonexistent"]
spec = importlib.util.spec_from_file_location("ps", os.path.join(here, "..", "audio-check", "pop909-sustain.py")); ps = importlib.util.module_from_spec(spec); spec.loader.exec_module(ps)
ref = json.load(open(os.path.join(here, "..", "..", "docs", "sound", "data", "pop909-sustain.json")))["中央値と幅（下から25%〜75%）"]
PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

def toks(s):
    t = 0; out = []
    for tok in s.split():
        q = tok.split(":"); m = re.match(r"[0-9.]+", q[1]) if len(q) > 1 else None
        if not m: continue
        L = float(m.group(0)); n = re.match(r"[A-G][#b]?-?\d", q[0])
        if n:
            n = n.group(0); out.append((t, t + L, PC[n[0]] + n.count("#") - n.count("b") + 12 * (int(n[-1]) + 1), 80))
        t += L
    return out

js = json.load(open(argv[1])); mel = []
for v in js.get("vocals", []):
    if v.get("volume", 1) >= 0.99: mel += toks(v["notes"])
acc = []
for p in js["parts"]:
    if p.get("instrument") in ("kick", "snare", "hihat", "crash") or p.get("patch") in ("kawaiiFx", "cymbalFx"): continue
    acc += toks(p["notes"])
r = ps.measure(sorted(mel), sorted(acc))
long_ = [(s, e) for s, e, *_ in mel if e - s >= 1.9]
if long_: r["長い音が拍のウラ（食って入る）で始まる割合"] = sum(1 for s, e in long_ if 0.1 < (s % 1) < 0.9) / len(long_)
ref["長い音が拍のウラ（食って入る）で始まる割合"] = [0.2, 0.34, 0.6]     # 拍の位置を合わせて測り直した値（pop909-onset-position.json: 8分ウラ＋16分ウラ）
SKIP = ("歌が伸ばしている間", "長い音が小節の頭", "句の中でいちばん長い音", "句の途中")
for k, v in r.items():
    if k not in ref or k.startswith(SKIP): continue
    lo, md, hi = ref[k]; mark = "" if lo - 1e-9 <= v <= hi + 1e-9 else ("  ← 少ない／短い" if v < lo else "  ← 多い／長い")
    print(f"  {k}: {v:.2f}（プロ {md:g}、幅 {lo:g}〜{hi:g}）{mark}")
