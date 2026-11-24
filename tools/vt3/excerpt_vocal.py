#!/usr/bin/env python3
"""歌入りの曲の一部分だけを切り出した JSON を作る（サビだけ書き出して、声・伴奏の組み合わせを短い時間でくらべるため）。
使い方: python3 tools/vt3/excerpt_vocal.py <曲.json> <始まりの小節(0から)> <小節数> <出力.json>
  パートも歌も同じ窓で切る。歌の vibratoMap・dynamics（[拍, 値] の並び）は窓の頭を 0 にずらす。"""
import json, re, sys
src, b0, nb, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
js = json.load(open(src)); beats = js["beats"]; t0, t1 = b0 * beats, (b0 + nb) * beats


def cut(notes):
    if notes.startswith("g:"): return "g:" + notes[2:][b0 * 16:(b0 + nb) * 16]
    o = []; t = 0.0
    for tok in notes.split():
        m = re.match(r"^(.+?):([0-9.]+)(.*)$", tok); L = float(m[2]); a, b = max(t, t0), min(t + L, t1)
        if b - a > 1e-6: o.append(f"R:{b - a:g}" if (t < t0 - 1e-6 or m[1].startswith("R")) else f"{m[1]}:{b - a:g}{m[3]}")
        t += L
        if t >= t1: break
    return " ".join(o) or f"R:{t1 - t0:g}"


js["chords"] = " ".join(js["chords"].split()[b0:b0 + nb]); js["sections"] = [{"kind": "chorus", "bars": nb}]
for p in js["parts"]:
    p["notes"] = cut(p["notes"]); p.pop("phrase", None)
    if "barGain" in p: p["barGain"] = p["barGain"][b0:b0 + nb]
for v in js.get("vocals", []):
    v["notes"] = cut(v["notes"])
    for k in ("vibratoMap", "dynamics"):
        if isinstance(v.get(k), list): v[k] = [[max(0, x[0] - t0), x[1]] for x in v[k] if t0 - 1 <= x[0] <= t1 + 1]
js["vocals"] = [v for v in js.get("vocals", []) if re.search(r"(^| )[A-G]", v["notes"])]
js["title"] = "excerpt"; json.dump(js, open(out, "w"), ensure_ascii=False)
print(out, len(js["parts"]), "パート", len(js["vocals"]), "声")
