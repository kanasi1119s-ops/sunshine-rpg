#!/usr/bin/env python3
"""カルテのまとめ: お手本（ジャンルごと）と自分の曲を並べて、どこが違うかを出す（学習用）。
使い方: python3 tools/song-analyzer/summarize.py <カルテのフォルダ> [--md 出力.md]
  名前が ref- で始まるカルテ＝お手本、own で始まるカルテ＝自分の曲。"""
import sys, os, json, glob, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compare import feats
d = sys.argv[1]; md = sys.argv[sys.argv.index("--md") + 1] if "--md" in sys.argv else None
GJ = {"rock": "ロック", "metal": "メタル", "funk": "ファンク", "dance": "ダンス", "electronic": "エレクトロニクス", "vocaloid": "ボカロ", "jpop": "J-POP", "kpop": "K-POP", "other": "そのほか"}
ref, own = {}, {}
for f in sorted(glob.glob(os.path.join(d, "*.karte.json"))):
    k = json.load(open(f)); n = os.path.basename(f)
    if n.startswith("own"): own[k["name"]] = feats(k)
    elif n.startswith("ref-"): ref.setdefault(GJ.get(k.get("source", {}).get("genre", "other"), "そのほか"), {})[k["name"]] = (feats(k), k.get("source", {}))
allref = [v[0] for g in ref.values() for v in g.values()]; keys = [k for k in allref[0] if all(k in x for x in allref)]
med = lambda xs: float(np.median(xs))
L = [f"# カルテのまとめ（お手本 {len(allref)} 曲・自分の曲 {len(own)} 曲）", "", "## お手本の曲", "", "| ジャンル | 作者「曲名」 | ライセンス | 出どころ |", "|---|---|---|---|"]
for g, songs in ref.items():
    for n, (f, s) in songs.items(): L.append(f"| {g} | {s.get('creator', '?')}「{s.get('title', n)}」 | {str(s.get('license', '')).split('org/')[-1].strip('/')} | {s.get('url', '')} |")
L += ["", "## 自分の曲と、お手本の違い（違いが大きい順）", "", "| 項目 | 自分（中央値） | お手本（中央値） | お手本の幅（小さい方〜大きい方） | |", "|---|---|---|---|---|"]
rows = []
for k in keys:
    if not all(k in x for x in own.values()): continue
    o = med([x[k] for x in own.values()]); r = [x[k] for x in allref]; lo, hi = float(np.percentile(r, 20)), float(np.percentile(r, 80)); m = med(r)
    sc = max(hi - lo, 0.15 * abs(m), 1e-6); dist = 0 if lo <= o <= hi else min(abs(o - lo), abs(o - hi)) / sc; rows.append((dist, k, o, m, lo, hi))
for dist, k, o, m, lo, hi in sorted(rows, reverse=True): L.append(f"| {k} | {o:.1f} | {m:.1f} | {lo:.1f}〜{hi:.1f} | {'★ 幅の外' if dist > 0 else ''} |")
L += ["", "## ジャンルごとの中央値", "", "| 項目 | " + " | ".join(f"{g}（{len(v)}）" for g, v in ref.items()) + " | 自分 |", "|---|" + "---|" * (len(ref) + 1)]
for k in keys: L.append(f"| {k} | " + " | ".join(f"{med([x[0][k] for x in v.values()]):.1f}" for v in ref.values()) + f" | {med([x[k] for x in own.values()]) if own and all(k in x for x in own.values()) else float('nan'):.1f} |")
txt = "\n".join(L); print(txt)
if md: open(md, "w").write(txt + "\n")
