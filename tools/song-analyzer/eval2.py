#!/usr/bin/env python3
"""段2の答え合わせ（自分の曲だけ）: 書き起こし（ドラム・ベース・和音・歌）を、曲の JSON（正解）とくらべる。
使い方: SA_CACHE=<ためた音のフォルダ> python3 tools/song-analyzer/eval2.py <名前> <曲の.json> [--rerun]
  先に SA_CACHE と SA_RAW=<フォルダ>/<名前>.raw.pkl を付けて analyze.py を1回走らせておく。--rerun で、ためた音から段2だけをやり直す（調整用）。"""
import sys, os, re, json, pickle, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
name, jpath = sys.argv[1], sys.argv[2]; cache = os.environ.get("SA_CACHE", "/tmp/sa"); P = pickle.load(open(os.path.join(cache, name + ".raw.pkl"), "rb")); bar_t = P["bar_t"]; raw = P["raw"]
js = json.load(open(jpath)); bpm = js["bpm"]; spb = 60 / bpm
if "--rerun" in sys.argv:
    import librosa, stage2
    d = dict(np.load(os.path.join(cache, name + ".stems.npz"))); sm = {k: v.astype(np.float32).mean(0) for k, v in d.items()}; sm["chordal"] = sm["guitar"] + sm["piano"] + sm["other"]
    _, raw = stage2.run(sm, None, bar_t, float(np.median(np.diff(bar_t))) / 4, {"drums": True, "bass": True, "vocals": True}, librosa)
PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def midi(n): return PC[n[0]] + n.count("#") - n.count("b") + 12 * (int(re.search(r"-?\d+$", n).group(0)) + 1)
nsteps = int(len(js["chords"].split()) * 16) + 64
def grid(inst):
    g = np.zeros(nsteps, bool)
    for p in js["parts"]:
        if p.get("instrument") in inst and p["notes"].startswith("g:"):
            for i, c in enumerate(p["notes"][2:]):
                if c not in ". " and i < nsteps: g[i] = True
    return g
def pitched(parts):
    g = np.full(nsteps, -1)
    for p in parts:
        t = 0
        for tok in p["notes"].split():
            q = tok.split(":"); m = re.match(r"[0-9.]+", q[1]) if len(q) > 1 else None
            if not m: continue
            L = float(m.group(0)); nm_ = re.match(r"[A-G][#b]?-?\d", q[0])
            if nm_:
                for i in range(int(round(t * 4)), int(round((t + L) * 4))):
                    if i < nsteps: g[i] = midi(nm_.group(0))
            t += L
    return g
T = {"K": grid(("kick",)), "S": grid(("snare",)), "H": grid(("hihat",)), "B": pitched([p for p in js["parts"] if p.get("instrument") == "bass" and not p.get("patch")]),
     "V": pitched([v for v in js.get("vocals", []) if v.get("volume", 1) >= 0.99])}
st = np.concatenate([np.linspace(bar_t[i], bar_t[i + 1], 17)[:-1] for i in range(len(bar_t) - 1)])
det = {"K": np.array([c != "." for p in raw["drums"]["kick"] for c in p]), "S": np.array([c != "." for p in raw["drums"]["snare"] for c in p]), "H": np.array([c != "." for p in raw["drums"]["hat"] for c in p])}
def tidx(off): return np.round((st - off) / (spb / 4)).astype(int)
def f1(a, b): tp = (a & b).sum(); return 2 * tp / max(1, a.sum() + b.sum())
best = max(np.arange(-0.3, 1.5, 0.01), key=lambda o: f1(det["K"], T["K"][np.clip(tidx(o), 0, nsteps - 1)]))
ix = np.clip(tidx(best), 0, nsteps - 1); print(f"頭のずれ {best:.2f}秒・マス {len(st)}")
for k, nm_ in (("K", "キック"), ("S", "スネア"), ("H", "刻み")):
    a, b = det[k], T[k][ix]; tp = (a & b).sum(); print(f"  {nm_}: 正解 {b.sum()} 打・答え {a.sum()} 打  当たった割合（答えのうち） {tp / max(1, a.sum()) * 100:.0f}%・見つけた割合（正解のうち） {tp / max(1, b.sum()) * 100:.0f}%")
bn = np.array(raw["bass"]["notes"]); tb = T["B"][ix]; both = (bn >= 0) & (tb >= 0)
print(f"  ベース: 鳴っているかの一致 {((bn >= 0) == (tb >= 0)).mean() * 100:.0f}%・音の名前が合う {(bn[both] % 12 == tb[both] % 12).mean() * 100:.0f}%・高さまで合う {(bn[both] == tb[both]).mean() * 100:.0f}%")
mv = np.full(len(st), -1.0)
for s, e, p, _ in raw["melody"]["notes"]: mv[int(round(s * 4)):int(round(e * 4))] = p
tv = T["V"][ix]; both = (mv >= 0) & (tv >= 0)
print(f"  歌: 鳴っているかの一致 {((mv >= 0) == (tv >= 0)).mean() * 100:.0f}%（正解 {(tv >= 0).mean() * 100:.0f}%・答え {(mv >= 0).mean() * 100:.0f}%）・音の名前が合う {(mv[both] % 12 == tv[both] % 12).mean() * 100:.0f}%")
ch = [c for c in js["chords"].split()]; seq = raw["chords"]["seq"]; ok = okq = n = 0
def parse(c):
    m = re.match(r"([A-G][#b]?)(.*)", c); r = PC[m.group(1)[0]] + m.group(1).count("#") - m.group(1).count("b"); q = m.group(2); return r % 12, ("m" if q.startswith("m") and not q.startswith("maj") else "M")
for h, c in enumerate(seq):
    b = int(np.floor((st[min(len(st) - 1, h * 8)] - best) / (spb * 4) + 0.1)); 
    if c is None or b < 0 or b >= len(ch): continue
    parts = ch[b].split("|"); tr, tq = parse(parts[0] if (h % 2 == 0 or len(parts) == 1) else parts[-1]); n += 1; ok += c[0] == tr; okq += (c[0] == tr and (("m" if c[1] in ("m", "m7") else "M") == tq or c[1] in ("5", "sus4", "sus2")))
print(f"  和音（2拍ごと）: 根音が合う {ok / max(1, n) * 100:.0f}%・長短まで合う {okq / max(1, n) * 100:.0f}%")
