#!/usr/bin/env python3
"""お手本の曲に 4 段階目（聞き分け）をかけて、ジャンルごとの「楽器・声・音の種類・ふんいき」の出方を集める（2026-11-17）。
使い方: python3 tools/song-analyzer/stage4_refs.py collect <出力 JSON> [最大の曲数]   … カルテのあるお手本を 1 曲ずつ取ってきて聞かせ、音は消す（途中からやり直せる）
        python3 tools/song-analyzer/stage4_refs.py table <集めた JSON> [自分の曲の stage4 の結果 JSON …]   … ジャンルごとの表と、自分の曲がどのジャンルに近いか
決まりは collect_ia.py と同じ（CC BY・CC BY-SA・CC0、netlabels の集まり、音は聞かせたら消す）。保存するのは 527 種類のうち表に出す名前の「度合い」だけ。
速さのため、曲全体だけを 20 秒おきに 10 秒ずつ聞かせる（分けた音ごとの中身は stage4.py で 1 曲ずつ）。"""
import sys, os, json, glob, urllib.request, urllib.parse, warnings
warnings.filterwarnings("ignore")
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import stage4 as S
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."); KD = os.path.join(ROOT, "docs/sound/karte")
OK = ("creativecommons.org/licenses/by/", "creativecommons.org/licenses/by-sa/", "creativecommons.org/publicdomain/zero/")
NAMES = sorted({en for tb in S.GROUPS.values() for en in tb} | {"Music", "Musical instrument", "Music for children", "Song"})
GJ = {"pop": "ポップ", "rock": "ロック", "metal": "メタル", "funk": "ファンク", "dance": "ダンス", "electronic": "エレクトロニクス", "vocaloid": "ボカロ", "other": "そのほか"}
def secs(x):
    try:
        if ":" in str(x): p = [float(q) for q in str(x).split(":")]; return sum(v * 60 ** i for i, v in enumerate(reversed(p)))
        return float(x)
    except Exception: return 0
def vec(path):
    import librosa
    y, sr = librosa.load(path, sr=16000, mono=True); ts, P, lab, L = S.listen(y, 16000, hop=20.0)
    w = (L > L.max() - 25).astype(float); m = (P * w[:, None]).sum(0) / max(1.0, w.sum())
    return {en: round(float(m[lab.index(en)]), 4) for en in NAMES if en in lab}
def vec_stems(path, which=("drums", "guitar", "other")):
    """曲を分けて、分けた音ごとに聞かせる（20 秒おきに 10 秒ずつ。その音が鳴っている窓だけ）"""
    import gc, librosa, analyze as A
    st = A.separate(A.load_audio(path)); mono = {k: librosa.resample(np.asarray(st[k], dtype=np.float32).mean(0), orig_sr=A.SR, target_sr=16000) for k in which}; ref = max(float(np.sqrt(np.mean(v ** 2))) for v in st.values()); del st; gc.collect(); out = {}
    for k, y in mono.items():
        ts, P, lab, L = S.listen(y, 16000, hop=20.0); w = (L > 20 * np.log10(ref + 1e-9) - 30).astype(float)
        if w.sum() < 1: out[k] = {}; continue
        m = (P * w[:, None]).sum(0) / w.sum(); out[k] = {en: round(float(m[lab.index(en)]), 4) for en in NAMES if en in lab}
    return out
if sys.argv[1] == "stems-eval":   # stems-eval <曲全体の JSON> <分けた音の JSON>: 同じ曲で「曲全体だけ」と「曲全体＋分けた音」のジャンルの当たり具合をくらべる
    base = json.load(open(sys.argv[2])); st = json.load(open(sys.argv[3])); ids = [k for k in st if k in base]; y = [st[k]["genre"] for k in ids]
    BIG = {"dance": "電子・ダンス", "electronic": "電子・ダンス", "rock": "ロック・メタル", "metal": "ロック・メタル", "pop": "ポップ・ファンク", "funk": "ポップ・ファンク"}
    def lv(p): return np.log(np.array([p.get(en, 0) for en in NAMES]) + 0.005)
    def feats(k, use):
        v = [lv(base[k]["p"])] if "mix" in use else []
        for sname in ("drums", "guitar", "other"):
            if sname in use: v.append(lv(st[k]["stems"].get(sname) or {}))
        return np.concatenate(v)
    def loo(use):
        X = np.array([feats(k, use) for k in ids]); hit = hb = 0
        for i in range(len(ids)):
            gs = sorted({g for j, g in enumerate(y) if j != i}); cen = {g: np.mean([X[j] for j in range(len(ids)) if j != i and y[j] == g], axis=0) for g in gs}; am = np.mean(list(cen.values()), axis=0); a = X[i] - am
            best = max(gs, key=lambda g: np.dot(a, cen[g] - am) / (np.linalg.norm(a) * np.linalg.norm(cen[g] - am) + 1e-9)); hit += best == y[i]; hb += BIG.get(best) == BIG.get(y[i])
        return hit, hb
    from collections import Counter
    print(f"分けた音まで聞かせたお手本: {len(ids)} 曲（{dict(Counter(y))}）")
    for label, use in (("曲全体だけ", ("mix",)), ("曲全体＋ドラム", ("mix", "drums")), ("曲全体＋ギター", ("mix", "guitar")), ("曲全体＋そのほか", ("mix", "other")), ("曲全体＋ドラム＋ギター＋そのほか", ("mix", "drums", "guitar", "other")), ("分けた音だけ（ドラム＋ギター＋そのほか）", ("drums", "guitar", "other"))):
        h, hb = loo(use); print(f"  {label}: 6 種類 {h}/{len(ids)}（{100 * h / len(ids):.0f}%）・大きく 3 つ {hb}/{len(ids)}（{100 * hb / len(ids):.0f}%）")
    # 分けた音で、ジャンルごとによく出る名前
    for sname, ja in (("drums", "ドラム"), ("guitar", "ギター")):
        print(f"  分けた音「{ja}」でよく出る名前（度合い 0.03 以上の曲の数）:")
        for g in sorted(set(y)):
            c = Counter()
            for k in ids:
                if st[k]["genre"] == g:
                    for en, v in (st[k]["stems"].get(sname) or {}).items():
                        if v >= 0.03 and en not in ("Music", "Musical instrument"): c[en] += 1
            print(f"    {GJ.get(g, g)}: " + "・".join(f"{en} {n}" for en, n in c.most_common(5)))
elif sys.argv[1] == "stems":   # stems <集めた JSON（曲全体）> <出力 JSON> <ジャンルごとの曲数>
    base = json.load(open(sys.argv[2])); outp = sys.argv[3]; per = int(sys.argv[4]); res = json.load(open(outp)) if os.path.exists(outp) else {}; os.makedirs("/tmp/sa/ref", exist_ok=True)
    pick = []
    for g in ("pop", "rock", "metal", "funk", "dance", "electronic"): pick += sorted(k for k, r in base.items() if r["genre"] == g)[:per]
    for ident in pick:
        if ident in res: continue
        try:
            d = json.load(urllib.request.urlopen(f"https://archive.org/metadata/{ident}", timeout=60)); m = d["metadata"]; lic = str(m.get("licenseurl", "")); col = m.get("collection", []); col = [col] if isinstance(col, str) else col
            if not any(o in lic for o in OK) or "netlabels" not in col: continue
            c = [x for x in d["files"] if x["name"].lower().endswith(".mp3") and "_64kb" not in x["name"] and 110 <= secs(x.get("length", 0)) <= 400]; x = c[min(1, len(c) - 1)] if len(c) > 2 else c[0]; path = f"/tmp/sa/ref/{ident}.mp3"
            urllib.request.urlretrieve(f"https://archive.org/download/{ident}/" + urllib.parse.quote(x["name"]), path); v = vec_stems(path); os.remove(path)
            res[ident] = {"genre": base[ident]["genre"], "stems": v}; json.dump(res, open(outp, "w"), ensure_ascii=False); print(f"○ {base[ident]['genre']} {ident}"); sys.stdout.flush()
        except Exception as e: print(f"× {ident}: {type(e).__name__} {str(e)[:80]}"); sys.stdout.flush()
    print("STEMSDONE", len(res))
elif sys.argv[1] == "own":     # 自分の曲を同じやり方で聞かせる: own <曲のファイル> <名前> <出力 JSON>
    json.dump({"name": sys.argv[3], "p": vec(sys.argv[2])}, open(sys.argv[4], "w"), ensure_ascii=False); print("ok", sys.argv[3])
elif sys.argv[1] == "collect":
    outp = sys.argv[2]; lim = int(sys.argv[3]) if len(sys.argv) > 3 else 9999; res = json.load(open(outp)) if os.path.exists(outp) else {}; os.makedirs("/tmp/sa/ref", exist_ok=True); n = 0
    for f in sorted(glob.glob(os.path.join(KD, "ref-*.karte.json"))):
        src = json.load(open(f)).get("source")
        if not src: continue
        ident = src["url"].split("/")[-1]
        if ident in res: continue
        if n >= lim: break
        n += 1
        try:
            d = json.load(urllib.request.urlopen(f"https://archive.org/metadata/{ident}", timeout=60)); m = d["metadata"]; lic = str(m.get("licenseurl", "")); col = m.get("collection", []); col = [col] if isinstance(col, str) else col
            if not any(o in lic for o in OK) or "netlabels" not in col: print(f"× {ident}: 条件に合わない"); continue
            c = [x for x in d["files"] if x["name"].lower().endswith(".mp3") and "_64kb" not in x["name"] and 110 <= secs(x.get("length", 0)) <= 400]
            if not c: print(f"× {ident}: 曲がない"); continue
            x = c[min(1, len(c) - 1)] if len(c) > 2 else c[0]; path = f"/tmp/sa/ref/{ident}.mp3"
            urllib.request.urlretrieve(f"https://archive.org/download/{ident}/" + urllib.parse.quote(x["name"]), path)
            v = vec(path); os.remove(path)
            res[ident] = {"genre": src["genre"], "license": lic, "url": src["url"], "p": v}; json.dump(res, open(outp, "w"), ensure_ascii=False)
            print(f"○ {src['genre']} {ident}"); sys.stdout.flush()
        except Exception as e: print(f"× {ident}: {type(e).__name__} {str(e)[:80]}"); sys.stdout.flush()
    print("COLLECTDONE", len(res))
else:
    res = json.load(open(sys.argv[2])); gen = sorted({r["genre"] for r in res.values()}, key=lambda g: list(GJ).index(g) if g in GJ else 99)
    def med(g, en): return float(100 * np.mean([r["p"].get(en, 0) >= 0.03 for r in res.values() if r["genre"] == g]))   # その名前が出た曲の割合（度合い 0.03 以上）
    print(f"# お手本 {len(res)} 曲に聞き分けモデル（AST）を聞かせた結果\n")
    print("数字は「その名前が出た曲の割合（%）」。モデルの度合い（0〜1）は全体に小さく出るので、0.03 以上を「出た」と数えた。太字はいちばん多いジャンル。\n")
    for gname, tb in S.GROUPS.items():
        rows = [(ja, [med(g, en) for g in gen]) for en, ja in tb.items()]; rows = [r for r in rows if max(r[1]) >= 15]; rows.sort(key=lambda r: -max(r[1]))
        print(f"## {gname}\n\n| 名前 | " + " | ".join(f"{GJ.get(g, g)}（{sum(1 for r in res.values() if r['genre'] == g)}）" for g in gen) + " |\n|---|" + "---|" * len(gen))
        for ja, v in rows[:22]: print(f"| {ja} | " + " | ".join(("**%d**" % round(x)) if x == max(v) else "%d" % round(x) for x in v) + " |")
        print()
    # 自分の曲: どのジャンルのお手本に近いか（度合いの対数で、まん中の形とのコサインの近さ）
    def lv(p): return np.log(np.array([p.get(en, 0) for en in NAMES]) + 0.005)
    cen = {g: np.median([lv(r["p"]) for r in res.values() if r["genre"] == g], axis=0) for g in gen}; allm = np.mean(list(cen.values()), axis=0)
    def near(p):
        a = lv(p) - allm; return sorted(((float(np.dot(a, cen[g] - allm) / (np.linalg.norm(a) * np.linalg.norm(cen[g] - allm) + 1e-9)), g) for g in gen), reverse=True)
    # 当たり具合: お手本の 1 曲を抜いて、残りで作ったまん中に当てる
    BIG = {"dance": "電子・ダンス", "electronic": "電子・ダンス", "rock": "ロック・メタル", "metal": "ロック・メタル", "pop": "ポップ・ファンク", "funk": "ポップ・ファンク"}
    hit = 0; tot = 0; hb = 0; tb_ = 0
    for k, r in res.items():
        c2 = {g: np.median([lv(q["p"]) for kk, q in res.items() if q["genre"] == g and kk != k], axis=0) for g in gen if sum(1 for kk, q in res.items() if q["genre"] == g and kk != k) >= 3}
        if r["genre"] not in c2: continue
        am = np.mean(list(c2.values()), axis=0); a = lv(r["p"]) - am
        best = max(c2, key=lambda g: np.dot(a, c2[g] - am) / (np.linalg.norm(a) * np.linalg.norm(c2[g] - am) + 1e-9)); hit += best == r["genre"]; tot += 1
        if r["genre"] in BIG: tb_ += 1; hb += BIG.get(best) == BIG[r["genre"]]
    print(f"## ジャンルの当たり具合（お手本を 1 曲ずつ抜いて確かめた）\n\n{tot} 曲のうち {hit} 曲（{100 * hit / max(1, tot):.0f}%）で、つけてあるジャンルと同じ答えになった（でたらめに答えると 15% くらい）。\n\n大きく 3 つ（電子・ダンス／ロック・メタル／ポップ・ファンク）に分けると、{tb_} 曲のうち {hb} 曲（{100 * hb / max(1, tb_):.0f}%。でたらめだと 33%）。\n\nつけてあるジャンルは、ネットレーベルの分け方をそのまま使ったもので、曲ごとに確かめたものではない。\n")
    for jp in sys.argv[3:]:
        o = json.load(open(jp)); p = o.get("p") or {}
        if not p: continue
        print(f"## 自分の曲: {o.get('name', os.path.basename(jp))}\n\n近いジャンル: " + "・".join(f"{GJ.get(g, g)} {s:+.2f}" for s, g in near(p)[:4]) + "\n")
