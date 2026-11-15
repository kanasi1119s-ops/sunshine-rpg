#!/usr/bin/env python3
"""カルテの差分: お手本の曲と自分の曲のカルテを並べて、違いを出す（学習用）。
使い方: python3 tools/song-analyzer/compare.py <お手本.karte.json> <自分.karte.json>"""
import sys, json, numpy as np
JP = {"vocals": "歌", "drums": "ドラム", "bass": "ベース", "chordal": "和音の楽器"}
def feats(k):
    pb = k["per_bar"]; nb = k["bars"]; act = pb["active"]; f = {}
    f["伴奏が休んでいる時間（%）"] = k["rests"]["伴奏が休んでいる時間の割合"] * 100; f["全員が休んでいる時間（%）"] = k["rests"]["全員が休んでいる時間の割合"] * 100
    if k["rests"]["歌が休んでいる時間の割合"] is not None: f["歌が休んでいる時間（%）"] = k["rests"]["歌が休んでいる時間の割合"] * 100
    f["小節ごとの音量の幅（dB）"] = k["loudness"]["range_db"]; f["重なる楽器の数（平均）"] = k["layers"]["mean"]; f["重なる楽器の数が変わる回数（8小節あたり）"] = k["layers"]["changes_per_8bars"]
    f["重なる楽器が2つ以下の小節（%）"] = float(np.mean(np.array(pb["layers"]) <= 2) * 100)
    for c in JP:
        if k["stems_present"].get(c): f[f"{JP[c]}が休んでいる小節（%）"] = float(np.mean(np.array(act[c]) < 0.3) * 100)
    f["1場面の長さ（秒・中央値）"] = float(np.median([s.get("length_sec", s["bars"] * 240 / k["tempo"]) for s in k["sections"]])); f["場面の数（1分あたり）"] = len(k["sections"]) / k["seconds"] * 60
    ld = [s["loud_db"] for s in k["sections"]]; ld = [x for x in ld if x > max(ld) - 20]      # 無音に近い場面（曲の頭・終わりの余白）は除く
    f["場面ごとの音量の差（いちばん大きい − いちばん小さい・dB）"] = max(ld) - min(ld)
    spb_ = 60 / k["tempo"]
    for d, v in k["drums_hits_per_beat"].items(): f[f"ドラム: {d}（1秒あたり）"] = v / spb_
    f["低い音の割合（%）"] = k["loudness"]["low"] * 100; f["高い音の割合（%）"] = k["loudness"]["high"] * 100; f["左右の広がり"] = k["loudness"]["width"]
    return f
if __name__ == "__main__":
    a, b = (json.load(open(p)) for p in sys.argv[1:3])
    fa, fb = feats(a), feats(b); rows = []
    SCALE = {"（%）": 10, "（dB）": 3, "": 1}
    for key in fa:
        if key not in fb: continue
        x, y = fa[key], fb[key]; sc = 10 if "%" in key else (3 if "dB" in key else max(0.3, abs(x) * 0.3)); rows.append((abs(x - y) / sc, key, x, y))
    print(f"お手本: {a['name']}（テンポ {a['tempo']}・{a['seconds']}秒）   自分: {b['name']}（テンポ {b['tempo']}・{b['seconds']}秒）\n違いが大きい順:")
    for d, key, x, y in sorted(rows, reverse=True):
        print(f"  {'★' if d >= 1 else '・'} {key}: お手本 {x:.1f} ／ 自分 {y:.1f}")
