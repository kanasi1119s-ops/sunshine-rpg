#!/usr/bin/env python3
"""Groove MIDI Dataset（プロのドラマーの演奏。CC BY 4.0、Google Magenta）から、「テンポが速いとき、ドラマーはどれだけ叩くか」の統計を出す（2026-11-15）。
人間「テンポ200だけどドラムをテンポ200に合わせて手数多く入れる必要性はないよ。そういうのも勉強してきて。」
使い方: python3 tools/audio-check/gmd-density.py <groove のフォルダ（info.csv がある所）> [--out 結果.json]   … 演奏（beat。fill は別）をテンポ帯ごとにまとめる"""
import sys, os, csv, json, numpy as np, mido
root = sys.argv[1]; out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
KICK = {35, 36}; SNARE = {37, 38, 40}; HAT = {42, 44, 46, 22, 26}; RIDE = {51, 53, 59}; TOM = {41, 43, 45, 47, 48, 50, 58}; CRASH = {49, 52, 55, 57}
BANDS = [(60, 90), (90, 110), (110, 130), (130, 150), (150, 175), (175, 215), (215, 300)]
R = {b: {} for b in BANDS}
for row in csv.DictReader(open(os.path.join(root, "info.csv"))):
    if row["beat_type"] != "beat" or row["time_signature"] != "4-4": continue
    bpm = float(row["bpm"]); band = next((b for b in BANDS if b[0] <= bpm < b[1]), None)
    if not band: continue
    try: m = mido.MidiFile(os.path.join(root, row["midi_filename"]))
    except Exception: continue
    ev = []; 
    for tr in m.tracks:
        t = 0
        for msg in tr:
            t += msg.time
            if msg.type == "note_on" and msg.velocity > 0: ev.append((t / m.ticks_per_beat, msg.note, msg.velocity))
    if len(ev) < 64: continue
    beats = max(e[0] for e in ev) - min(e[0] for e in ev)
    if beats < 16: continue
    def per(s): return sum(1 for e in ev if e[1] in s) / beats
    d = R[band]
    cym = [e for e in ev if e[1] in HAT | RIDE]; 
    vals = {"全部の打数（1拍あたり）": len(ev) / beats, "全部の打数（1秒あたり）": len(ev) / beats * bpm / 60, "キック（1拍あたり）": per(KICK), "スネア（1拍あたり。ゴースト込み）": per(SNARE),
            "スネアの強い打（1拍あたり）": sum(1 for e in ev if e[1] in SNARE and e[2] >= 90) / beats, "ゴーストノート（弱いスネア。1拍あたり）": sum(1 for e in ev if e[1] in SNARE and e[2] < 50) / beats,
            "ハイハット・ライドの刻み（1拍あたり）": len(cym) / beats, "タム（1拍あたり）": per(TOM)}
    for k, v in vals.items(): d.setdefault(k, []).append(v)
    d.setdefault("_style", []).append(row["style"].split("/")[0])
res = {}
for b, d in R.items():
    if not d: continue
    n = len(d["_style"]); res[f"テンポ {b[0]}〜{b[1]}"] = {"演奏の数": n, **{k: [round(float(np.percentile(v, p)), 2) for p in (25, 50, 75)] for k, v in d.items() if not k.startswith("_")},
                                         "刻みが4分（1拍に1.2打より少ない）の演奏の割合": round(float(np.mean([x < 1.2 for x in d["ハイハット・ライドの刻み（1拍あたり）"]])), 2),
                                         "刻みが16分（1拍に3打より多い）の演奏の割合": round(float(np.mean([x > 3 for x in d["ハイハット・ライドの刻み（1拍あたり）"]])), 2)}
print(json.dumps(res, ensure_ascii=False, indent=0))
if out: json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
