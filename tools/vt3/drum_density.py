#!/usr/bin/env python3
"""曲（JSON）のドラムの手数を、場面ごとに「1拍あたり」で出し、プロのドラマーの演奏（Groove MIDI。docs/sound/data/gmd-density-by-tempo.json）の同じテンポ帯とくらべる（2026-11-15）。
使い方: python3 tools/vt3/drum_density.py <曲.json>"""
import sys, os, re, json
here = os.path.dirname(os.path.abspath(__file__)); js = json.load(open(sys.argv[1])); bpm = js["bpm"]; beats = js.get("beats", 4)
ref = json.load(open(os.path.join(here, "..", "..", "docs", "sound", "data", "gmd-density-by-tempo.json")))
band = next((v for k, v in ref.items() if int(k.split()[1].split("〜")[0]) <= bpm < int(k.split("〜")[1])), None)
def onsets(p):
    if p["notes"].startswith("g:"): return [i * 0.25 for i, c in enumerate(p["notes"][2:]) if c not in ". "]     # ドラムの格子（1文字＝16分）
    t = 0; out = []
    for tok in p["notes"].split():
        q = tok.split(":"); m = re.match(r"[0-9.]+", q[1]) if len(q) > 1 else None
        if not m: continue
        if q[0] != "R": out.append(t)
        t += float(m.group(0))
    return out
D = {"キック": [], "スネア": [], "刻み": []}
for p in js["parts"]:
    k = {"kick": "キック", "snare": "スネア", "hihat": "刻み"}.get(p.get("instrument"))
    if k: D[k] += onsets(p)
secs = json.load(open(sys.argv[1] + ".secs")) if os.path.exists(sys.argv[1] + ".secs") else None
spb = 60 / bpm
if band: print(f"  プロ（テンポ {bpm} の帯・中央値）: キック {band['キック（1拍あたり）'][1]}・スネア {band['スネア（1拍あたり。ゴースト込み）'][1]}・刻み {band['ハイハット・ライドの刻み（1拍あたり）'][1]}・全部 {band['全部の打数（1拍あたり）'][1]}（幅 {band['全部の打数（1拍あたり）'][0]}〜{band['全部の打数（1拍あたり）'][2]}）")
rng = [(a["name"], a["t"] / spb, b["t"] / spb) for a, b in zip(secs, secs[1:])] if secs else [("全体", 0, max(max(v or [0]) for v in D.values()) + 1)]
for name, a, b in rng:
    L = b - a; c = {k: sum(1 for t in v if a <= t < b) / L for k, v in D.items()}; tot = sum(c.values())
    mark = "  ← 多い" if band and tot > band["全部の打数（1拍あたり）"][2] * 1.15 else ""
    print(f"  {name}: キック {c['キック']:.2f}・スネア {c['スネア']:.2f}・刻み {c['刻み']:.2f}・全部 {tot:.2f}{mark}")
