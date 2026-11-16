#!/usr/bin/env python3
"""ドラムの入り方を、カルテ（小節ごとのキック・スネア・刻みの打数）から調べる（2026-11-17）。人間「ドラムの始まり方いつも同じだよなー」「そういうのも学習してきて欲しかったなー」
使い方: python3 tools/song-analyzer/drum_entry.py <カルテのフォルダ> [--md 出力.md] [--json 出力.json]
見るもの（お手本＝ref-、自分＝own）:
  ・ドラムが最初に入るのは何小節目か。その前に何が鳴っているか（ドラムから始まる／ほかの楽器が先／全員いっしょ）
  ・入り方の型: 入った最初の2小節で、キック・スネア・刻みのどれがそろっているか（ふつうの所＝入ってから5〜12小節目の平均とくらべる）
      全部そろって入る／キックだけ／刻みだけ／キックと刻み（スネアなし）／スネアなしで入ってあとから足す／フィルで入る（最初の小節だけスネアが多い）／だんだん増える
  ・曲の途中でドラムが抜ける回数・抜ける長さ・戻り方の型
聞き取りは粗い（帯の強さから数えた打数）ので、割合は目安。"""
import sys, os, json, glob, collections
import numpy as np

kd = sys.argv[1]; md = sys.argv[sys.argv.index("--md") + 1] if "--md" in sys.argv else None; jp = sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv else None
GJ = {"pop": "ポップ", "rock": "ロック", "metal": "メタル", "funk": "ファンク", "dance": "ダンス", "electronic": "エレクトロニクス", "vocaloid": "ボカロ", "other": "そのほか"}


def study(k):
    p = k.get("per_bar") or {}; d = p.get("drums") or {}; names = list(d)
    if len(names) < 3: return None
    K, Sn, H = (np.array(d[n], float) for n in names[:3]); act = p.get("active") or {}; n = len(K)
    if n < 24: return None
    da = np.array(act.get("drums", [0] * n), float)[:n]; tot = K + Sn + H; on = (da >= 0.3) & (tot >= 0.5)      # その小節でドラムが鳴っているか
    if on.sum() < 12: return {"ドラムなし": True}
    others = {s: np.array(act.get(s, [0] * n), float)[:n] >= 0.3 for s in ("vocals", "bass", "chordal")}
    # 続けて鳴っている区間（2小節以上の切れ目で分ける）
    runs = []; i = 0
    while i < n:
        if not on[i]: i += 1; continue
        j = i
        while j < n and (on[j] or (j + 1 < n and on[j + 1])): j += 1
        if j - i >= 4: runs.append((i, j))
        i = j + 1
    if not runs: return {"ドラムなし": True}
    def kind(a, b):
        st = slice(min(b - 1, a + 4), min(b, a + 12)); ref = [max(1e-6, float(np.median(x[st]))) for x in (K, Sn, H)]
        r1 = [float(x[a]) / r for x, r in zip((K, Sn, H), ref)]; r2 = [float(np.mean(x[a:a + 2])) / r for x, r in zip((K, Sn, H), ref)]; r4 = [float(np.mean(x[a + 2:a + 4])) / r for x, r in zip((K, Sn, H), ref)]
        has = [v >= 0.45 for v in r2]; steady_sn = ref[1] >= 0.15
        if steady_sn and r1[1] >= 1.8 and r4[1] < 1.4: return "フィルで入る（最初の小節だけスネアが多い）"
        if all(has) or (not steady_sn and has[0] and has[2]): return "全部そろって入る"
        if has[0] and not has[1] and not has[2]: return "キックだけで入る"
        if has[2] and not has[0] and not has[1]: return "刻みだけで入る"
        if has[0] and has[2] and not has[1]: return "キックと刻みで入る（スネアはあとから）"
        if has[1] and not has[0]: return "スネアから入る（キックはあとから）"
        return "だんだん増える"
    a0, b0 = runs[0]; before = [s for s, v in others.items() if a0 > 0 and v[max(0, a0 - 4):a0].mean() >= 0.5]; same = [s for s, v in others.items() if a0 > 0 and v[max(0, a0 - 4):a0].mean() < 0.25 and v[a0:a0 + 2].mean() >= 0.5]
    lead = "ドラムから始まる（1小節目から）" if a0 <= 0 and not any(v[:1].mean() >= 0.5 and v[1:3].mean() >= 0.5 for v in others.values()) and all(v[:2].mean() < 0.5 for v in others.values()) else \
           "全員いっしょに始まる（1小節目から）" if a0 <= 0 else "ほかの楽器が鳴っている所へ、ドラムだけが足される" if before and not same else "ドラムと同時に、ほかの楽器も入る" if same else "無音のあとにドラムが入る"
    spb = 60.0 / k["tempo"]; gaps = [(runs[i + 1][0] - runs[i][1]) for i in range(len(runs) - 1)]
    return {"最初に入る小節": int(a0 + 1), "最初に入るまでの秒": round(float(a0 * 4 * spb), 1), "始まり方": lead, "最初の入り方": kind(a0, b0), "戻り方": [kind(a, b) for a, b in runs[1:]],
            "途中で抜ける回数": len(gaps), "抜ける長さ（小節）": [int(g) for g in gaps], "小節の数": n}


R = collections.defaultdict(list)
for f in sorted(glob.glob(os.path.join(kd, "*.karte.json"))):
    k = json.load(open(f)); nm = os.path.basename(f)[:-len(".karte.json")]; s = study(k)
    if not s: continue
    g = "自分" if nm.startswith("own") else GJ.get((k.get("source") or {}).get("genre", "other"), "そのほか"); s["name"] = nm; R[g].append(s)
    if g != "自分": R["お手本ぜんぶ"].append(s)


def summ(L):
    w = [x for x in L if not x.get("ドラムなし")]; c = lambda key: collections.Counter(x[key] for x in w); pc = lambda cnt: {a: round(b / max(1, sum(cnt.values())), 3) for a, b in cnt.most_common()}
    back = collections.Counter(t for x in w for t in x["戻り方"]); gl = [g for x in w for g in x["抜ける長さ（小節）"]]
    return {"曲の数": len(L), "ドラムのある曲": len(w), "始まり方": pc(c("始まり方")), "最初の入り方": pc(c("最初の入り方")), "最初に入る小節（25%・まん中・75%）": [int(np.percentile([x["最初に入る小節"] for x in w], q)) for q in (25, 50, 75)] if w else None,
            "最初に入るまでの秒（まん中）": round(float(np.median([x["最初に入るまでの秒"] for x in w])), 1) if w else None, "途中で抜ける回数（25%・まん中・75%）": [float(np.percentile([x["途中で抜ける回数"] for x in w], q)) for q in (25, 50, 75)] if w else None,
            "抜ける長さ（小節・まん中）": float(np.median(gl)) if gl else None, "戻り方": pc(back), "戻った回数": int(sum(back.values()))}


OUT = {g: summ(L) for g, L in R.items()}
if jp: json.dump(OUT, open(jp, "w"), ensure_ascii=False, indent=1)
order = ["お手本ぜんぶ"] + [g for g in GJ.values() if g in OUT] + (["自分"] if "自分" in OUT else [])
T = ["# ドラムの入り方（お手本のカルテから）", "", "小節ごとのキック・スネア・刻みの打数から、ドラムが「いつ・どう入るか」を調べた。聞き取りは粗いので、割合は目安。", ""]
for g in order:
    o = OUT[g]; T += [f"## {g}（{o['曲の数']}曲・ドラムのある曲 {o['ドラムのある曲']}）", ""]
    if not o["ドラムのある曲"]: continue
    T.append(f"- 最初に入る小節: まん中 {o['最初に入る小節（25%・まん中・75%）'][1]}小節目（{o['最初に入る小節（25%・まん中・75%）'][0]}〜{o['最初に入る小節（25%・まん中・75%）'][2]}）・曲が始まって {o['最初に入るまでの秒（まん中）']}秒")
    T.append("- 始まり方: " + "／".join(f"{a} {int(b * 100)}%" for a, b in o["始まり方"].items()))
    T.append("- 最初の入り方: " + "／".join(f"{a} {int(b * 100)}%" for a, b in o["最初の入り方"].items()))
    T.append(f"- 途中で抜ける回数: まん中 {o['途中で抜ける回数（25%・まん中・75%）'][1]:.0f}回（{o['途中で抜ける回数（25%・まん中・75%）'][0]:.0f}〜{o['途中で抜ける回数（25%・まん中・75%）'][2]:.0f}）・抜ける長さ まん中 {o['抜ける長さ（小節・まん中）']}小節")
    if o["戻った回数"]: T.append(f"- 戻り方（{o['戻った回数']}回）: " + "／".join(f"{a} {int(b * 100)}%" for a, b in o["戻り方"].items()))
    T.append("")
if "自分" in R: T += ["## 自分の曲（1曲ずつ）", ""] + [f"- {x['name']}: {x.get('最初に入る小節', '—')}小節目・{x.get('始まり方', '')}・{x.get('最初の入り方', '')}・抜ける {x.get('途中で抜ける回数', 0)}回・戻り方 {x.get('戻り方', [])}" for x in R["自分"] if not x.get("ドラムなし")]
txt = "\n".join(T)
if md: open(md, "w").write(txt + "\n")
print(txt)
