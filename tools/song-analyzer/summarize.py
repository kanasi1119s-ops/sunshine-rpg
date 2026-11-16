#!/usr/bin/env python3
"""カルテのまとめ: お手本（ジャンルごと）と自分の曲を並べて、どこが違うかを出す（学習用）。
使い方: python3 tools/song-analyzer/summarize.py <カルテのフォルダ> [--md 出力.md]
  名前が ref- で始まるカルテ＝お手本、own で始まるカルテ＝自分の曲。"""
import sys, os, json, glob, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compare import feats
d = sys.argv[1]; md = sys.argv[sys.argv.index("--md") + 1] if "--md" in sys.argv else None
GJ = {"pop": "ポップ", "rock": "ロック", "metal": "メタル", "funk": "ファンク", "dance": "ダンス", "electronic": "エレクトロニクス", "vocaloid": "ボカロ", "jpop": "J-POP", "kpop": "K-POP", "other": "そのほか"}
ref, own, frag = {}, {}, {}
def addfrag(g, k):
    c = (k.get("stage2") or {}).get("和音") or {}
    for n, lst in (c.get("短いコード進行（多い順）") or {}).items():
        for e in lst: frag.setdefault(g, {}).setdefault(n, {}).setdefault(e["進行"], []).append(e["回数"])
for f in sorted(glob.glob(os.path.join(d, "*.karte.json"))):
    k = json.load(open(f)); n = os.path.basename(f)
    if n.startswith("own"): own[k["name"]] = feats(k); addfrag("自分", k)
    elif n.startswith("ref-"): ref.setdefault(GJ.get(k.get("source", {}).get("genre", "other"), "そのほか"), {})[k["name"]] = (feats(k), k.get("source", {})); addfrag(GJ.get(k.get("source", {}).get("genre", "other"), "そのほか"), k); addfrag("お手本ぜんぶ", k)
allref = [v[0] for g in ref.values() for v in g.values()]; keys = sorted({k for x in allref for k in x}, key=lambda k: [k for x in allref for k in x].index(k))
med = lambda xs: float(np.median(xs))
L = [f"# カルテのまとめ（お手本 {len(allref)} 曲・自分の曲 {len(own)} 曲）", "", "## お手本の曲", "", "| ジャンル | 作者「曲名」 | ライセンス | 出どころ |", "|---|---|---|---|"]
for g, songs in ref.items():
    for n, (f, s) in songs.items(): L.append(f"| {g} | {s.get('creator', '?')}「{s.get('title', n)}」 | {str(s.get('license', '')).split('org/')[-1].strip('/')} | {s.get('url', '')} |")
L += ["", "## 自分の曲と、お手本の違い（違いが大きい順）", "", "| 項目 | 自分（中央値） | お手本（中央値） | お手本の幅（小さい方〜大きい方） | |", "|---|---|---|---|---|"]
rows = []
for k in keys:
    if not all(k in x for x in own.values()): continue
    if not own or sum(k in x for x in allref) < 4: continue
    o = med([x[k] for x in own.values()]); r = [x[k] for x in allref if k in x]; lo, hi = float(np.percentile(r, 20)), float(np.percentile(r, 80)); m = med(r)
    sc = max(hi - lo, 0.15 * abs(m), 1e-6); dist = 0 if lo <= o <= hi else min(abs(o - lo), abs(o - hi)) / sc; rows.append((dist, k, o, m, lo, hi))
for dist, k, o, m, lo, hi in sorted(rows, reverse=True): L.append(f"| {k} | {o:.1f} | {m:.1f} | {lo:.1f}〜{hi:.1f} | {'★ 幅の外' if dist > 0 else ''} |")
L += ["", "## ジャンルごとの中央値", "", "| 項目 | " + " | ".join(f"{g}（{len(v)}）" for g, v in ref.items()) + " | 自分 |", "|---|" + "---|" * (len(ref) + 1)]
mm = lambda xs: f"{med(xs):.1f}" if xs else "—"
for k in keys: L.append(f"| {k} | " + " | ".join(mm([x[0][k] for x in v.values() if k in x[0]]) for v in ref.values()) + f" | {med([x[k] for x in own.values()]) if own and all(k in x for x in own.values()) else float('nan'):.1f} |")
L += ["", "## 短いコード進行（一部だけ。1曲ぶんは保存しない）", "", "度数（I＝その調の1番目の和音）で書く。「曲数」＝その進行が出てきた曲の数。耳で確かめた正解ではなく、機械の聞き取り（自分の1曲で答え合わせして、根音 87%・長短 73% の当たり方）なので、目安。同じ根音で長と短が入れかわるゆれは、その曲で多い方にそろえてある。", ""]
for g in ["お手本ぜんぶ"] + [x for x in frag if x not in ("お手本ぜんぶ", "自分")] + ["自分"]:
    if g not in frag: continue
    L.append(f"### {g}"); L.append("")
    for n in sorted(frag[g]):
        top = sorted(frag[g][n].items(), key=lambda kv: (-len(kv[1]), -sum(kv[1])))[:8 if g in ("お手本ぜんぶ", "自分") else 4]
        L.append(f"- 和音{n}つ: " + "／".join(f"{p}（{len(c)}曲・{sum(c)}回）" for p, c in top))
    L.append("")
if "お手本ぜんぶ" in frag and "自分" in frag:
    L += ["### お手本に多くて、自分の曲に出てこない進行", ""]
    for n in sorted(frag["お手本ぜんぶ"]):
        miss = [(p, c) for p, c in sorted(frag["お手本ぜんぶ"][n].items(), key=lambda kv: (-len(kv[1]), -sum(kv[1]))) if len(c) >= 2 and p not in frag["自分"].get(n, {})][:8]
        if miss: L.append(f"- 和音{n}つ: " + "／".join(f"{p}（{len(c)}曲）" for p, c in miss))
txt = "\n".join(L); print(txt)
if md: open(md, "w").write(txt + "\n")
