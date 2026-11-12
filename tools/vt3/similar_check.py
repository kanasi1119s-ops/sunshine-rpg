#!/usr/bin/env python3
# 似た曲を作らないための確かめ（2026-11-12 人間「絶対条件でここで作った曲で似た曲を作らない。過去の物も含めて」）。
# 使い方: python3 tools/vt3/similar_check.py <曲の JSON（歌入りの版がよい）> [ほかの JSON を探すフォルダ ...]
#   歌（旋律）とベースを、これまでに作った全部の曲（既定: /mnt/user-data/outputs の下の全部と、assets-src/ai-songs・src/audio/songs・src/audio/songs-archive・dist-songs。索引は /tmp/vp25/similar-index.pkl）とくらべる。
#   くらべ方: ①小節ごとのリズムの形 ②「音程の動き＋長さ」の4つ続き（調がちがっても同じ動きなら同じとみなす）
#   ベースは、小節の最初の音からの音程で見る（和音がちがっても同じ型なら同じ）。
#   目安: 旋律の動きの重なり 25% 以上、リズムの重なり 60% 以上、ベースの型の重なり 50% 以上は「似ている」→ 作る前に直す。
import sys, os, re, json, glob, collections

NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def midi(n):
    m = re.match(r"([A-G])([b#]?)(-?\d)", n)
    return NOTE[m.group(1)] + {"b": -1, "#": 1, "": 0}[m.group(2)] + 12 * (int(m.group(3)) + 1)


def events(notes):
    """[(始まりの拍, 長さ, 高さ か None)]"""
    out, t = [], 0.0
    for tok in notes.split():
        a = tok.split(":")
        if len(a) < 2: continue
        m = re.match(r"[0-9.]+", a[1])
        if not m: continue
        L = float(m.group(0)); p = re.match(r"[A-G][b#]?-?\d", a[0])
        out.append((t, L, midi(p.group(0)) if p else None)); t += L
    return out


def pick(js):
    mel = None
    v = js.get("vocals") or []
    if v and v[0].get("notes"): mel = v[0]["notes"]
    if mel is None:
        for p in js.get("parts", []):
            r = p.get("role", "")
            if "歌の役" in r or "メロディ" in r or "旋律" in r: mel = p["notes"]; break
    if mel is None:
        for p in js.get("parts", []):
            if p.get("instrument") == "lead" and len(p.get("notes", "")) > 400: mel = p["notes"]; break
    bass = None
    for p in js.get("parts", []):
        if p.get("instrument") == "bass" and "サブ" not in p.get("role", "") and len(p.get("notes", "")) > 200: bass = p["notes"]; break
    return mel, bass


def q(x): return round(x * 4) / 4


def feats(notes, beats, rel_root=False):
    ev = events(notes); bars = collections.defaultdict(list)
    for t, L, p in ev:
        if p is None: continue
        bars[int(t // beats + 1e-6)].append((q(t % beats), q(L), p))
    rh, shape = [], []
    for b in sorted(bars):
        x = bars[b]
        if len(x) < 2: continue
        rh.append(" ".join(f"{t:g}/{L:g}" for t, L, p in x))
        if rel_root: shape.append(" ".join(f"{t:g}/{p - x[0][2]}" for t, L, p in x))
    seq = [(p, q(L)) for t, L, p in ev if p is not None]
    sh = set()
    for i in range(len(seq) - 4):
        w = seq[i:i + 5]
        sh.add(tuple((w[k + 1][0] - w[k][0], w[k][1]) for k in range(4)))
    return rh, sh, shape


def share(a, b):
    if not a: return 0.0
    sb = set(b); return sum(1 for x in a if x in sb) / len(a)


SLUG = r"-(v|t|r|j)\d+[a-z]*(vo|full|solo)?\.json$|\.sunshine-song\.json$|\.json$"
ROOTS = ["/mnt/user-data/outputs", "assets-src/ai-songs", "src/audio/songs", "src/audio/songs-archive", "dist-songs"]
CACHE = "/tmp/vp25/similar-index.pkl"


def build_index(dirs):
    """これまでに作った全部の曲（dirs の下を全部たどる）の、旋律とベースの形の索引。曲（slug）ごとにいちばん新しい版を1つ。結果は CACHE に置く"""
    import pickle
    try: idx = pickle.load(open(CACHE, "rb"))
    except Exception: idx = {}
    seen = set()
    for d0 in dirs:
        for d, _, fs in os.walk(d0):
            for base in fs:
                if not base.endswith(".json"): continue
                p = os.path.join(d, base)
                try: st = os.stat(p)
                except OSError: continue
                if st.st_size > 30e6 or st.st_size < 2000: continue
                seen.add(p)
                if p in idx and idx[p][0] == st.st_mtime: continue
                try:
                    j2 = json.load(open(p))
                    if not isinstance(j2, dict) or not isinstance(j2.get("parts"), list): idx[p] = (st.st_mtime, None); continue
                    m2, b2 = pick(j2); bt = j2.get("beats", 4) or 4
                    r2, s2, _ = feats(m2, bt) if m2 else ([], set(), [])
                    _, _, bs2 = feats(b2, bt, True) if b2 else ([], set(), [])
                    idx[p] = (st.st_mtime, (set(r2), s2, set(bs2), j2.get("title", "")))
                except Exception: idx[p] = (st.st_mtime, None)
    idx = {p: v for p, v in idx.items() if p in seen}
    os.makedirs(os.path.dirname(CACHE), exist_ok=True); pickle.dump(idx, open(CACHE, "wb"))
    best = {}
    for p, (mt, ft) in idx.items():
        if ft is None: continue
        base = os.path.basename(p); slug = re.sub(SLUG, "", base)
        key = (("vo.json" in base), mt)
        if slug not in best or key > best[slug][0]: best[slug] = (key, ft)
    return {s: ft for s, (k, ft) in best.items()}


def main():
    target = sys.argv[1]; dirs = sys.argv[2:] or ROOTS
    js = json.load(open(target)); beats = js.get("beats", 4); mel, bass = pick(js)
    slug = re.sub(SLUG, "", os.path.basename(target))
    mr, ms, _ = feats(mel, beats) if mel else ([], set(), [])
    br, _, bshape = feats(bass, beats, True) if bass else ([], set(), [])
    rows = []
    for s, (r2, s2, bs2, title) in build_index(dirs).items():
        if s == slug: continue
        rows.append((f"{s}（{title}）" if title else s, share(mr, r2), (len(ms & s2) / len(ms)) if ms else 0.0, share(bshape, bs2)))
    print(f"■ {js.get('title', slug)}: 旋律 {len(mr)} 小節・ベース {len(bshape)} 小節を、これまでの {len(rows)} 曲とくらべた")
    bad = 0
    for name, idx, lim in (("旋律の動き（音程＋長さの4つ続き）", 2, 0.25), ("旋律のリズム（小節の形）", 1, 0.60), ("ベースの型（小節の形）", 3, 0.50)):
        top = sorted(rows, key=lambda r: -r[idx])[:5]
        print(f"  {name}: 目安 {int(lim * 100)}% 未満")
        for r in top:
            flag = "  ← 似ている" if r[idx] >= lim else ""
            bad += bool(flag); print(f"    {r[idx] * 100:5.1f}%  {r[0]}{flag}")
    print("  →", "似ている曲があります。作る前に直す" if bad else "目安をこえる曲はありません（最後は耳で確かめる）")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
