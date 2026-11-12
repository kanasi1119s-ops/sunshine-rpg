#!/usr/bin/env python3
# 似た曲を作らないための確かめ（2026-11-12 人間「絶対条件でここで作った曲で似た曲を作らない。過去の物も含めて」）。
# 使い方: python3 tools/vt3/similar_check.py <曲の JSON（歌入りの版がよい）> [ほかの JSON を探すフォルダ ...]
#   歌（旋律）とベースを、これまでに作った全部の曲（既定: /mnt/user-data/outputs の下の全部と、assets-src/ai-songs・src/audio/songs・src/audio/songs-archive・dist-songs。索引は /tmp/vp25/similar-index.pkl）とくらべる。
#   くらべ方: ①小節ごとのリズムの形 ②「音程の動き＋長さ」の4つ続き（調がちがっても同じ動きなら同じとみなす）
#   ベースは、小節の最初の音からの音程で見る（和音がちがっても同じ型なら同じ）。
#   曲調（テンポ・音色の組み合わせ・和音の進み方・キックの型・場面の並び）もくらべる。作る前は --plan で、決めた曲調だけを先にくらべる。
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
            if any(w in r for w in ("歌の役", "メロディ", "主旋律", "旋律", "笛", "フルート", "ホイッスル", "フィドル", "リード", "ソロ")) and "対旋律" not in r and len(p.get("notes", "")) > 300: mel = p["notes"]; break
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


DRUMS = ("kick", "snare", "hihat", "tom", "crash")


def chord_grams(chords):
    """和音の進み方（調がちがっても同じ進み方なら同じ）: 根音の動き（半音）＋長・短・属の3つ続き"""
    seq = []
    for c in chords.split():
        c = c.split("|")[0]; m = re.match(r"([A-G])([b#]?)(.*)", c)
        if not m: continue
        pc = (NOTE[m.group(1)] + {"b": -1, "#": 1, "": 0}[m.group(2)]) % 12; q = m.group(3).split("/")[0]
        kind = "m" if re.match(r"m(?!aj)", q) else ("7" if re.match(r"(7|9|11|13)", q) else "M")
        if not seq or seq[-1] != (pc, kind): seq.append((pc, kind))
    return set(tuple(((seq[i + k + 1][0] - seq[i + k][0]) % 12, seq[i + k][1]) for k in range(3)) for i in range(len(seq) - 3))


def style(js):
    """曲調の特徴: テンポ・音色の組み合わせ・和音の進み方・キックの型・場面の並び"""
    pal = set((p.get("patch") or p.get("amp") or p.get("instrument") or "") for p in js.get("parts", []) if p.get("instrument") not in DRUMS)
    kick = set()
    for p in js.get("parts", []):
        if p.get("instrument") == "kick":
            x = "".join(p.get("notes", "").split()); kick |= set(x[i:i + 16] for i in range(0, len(x) - 15, 16) if "X" in x[i:i + 16] or "x" in x[i:i + 16])
    return {"bpm": js.get("bpm", 0), "pal": pal, "ch": chord_grams(js.get("chords", "")), "kick": kick,
            "form": tuple(x.get("kind", "") for x in js.get("sections", []))}


def jac(a, b): return len(a & b) / len(a | b) if (a or b) else 0.0


def style_rows(st, index, skip):
    rows = []
    for s_, ft in index.items():
        if s_ == skip or len(ft) < 5: continue
        o = ft[4]; near = st["bpm"] and o["bpm"] and abs(st["bpm"] - o["bpm"]) <= 6
        chs = (len(st["ch"] & o["ch"]) / len(st["ch"])) if st["ch"] else 0.0
        ks = (len(st["kick"] & o["kick"]) / len(st["kick"])) if st["kick"] else 0.0
        fm = 1.0 if st.get("form") and st["form"] == o["form"] else 0.0
        score = 0.35 * jac(st["pal"], o["pal"]) + 0.3 * chs + 0.15 * ks + 0.1 * (1.0 if near else 0.0) + 0.1 * fm
        rows.append((score, s_, ft[3], o["bpm"], jac(st["pal"], o["pal"]), chs, ks, fm))
    return sorted(rows, reverse=True)


def print_style(st, index, skip):
    print(f"  曲調（テンポ {st['bpm']}・音色 {len(st['pal'])}種・和音の進み方 {len(st['ch'])}通り）: いちばん近い5曲。目安: 近さ 50% 未満、音色の重なり 60% 未満、和音の進み方 60% 未満")
    bad = 0
    for sc, s_, title, bpm, pj, chs, ks, fm in style_rows(st, index, skip)[:5]:
        flag = "  ← 似ている" if (sc >= 0.5 or pj >= 0.6 or chs >= 0.6) else ""
        bad += bool(flag)
        print(f"    近さ {sc * 100:4.0f}%  {s_}（{title}）テンポ {bpm}・音色 {pj * 100:.0f}%・和音 {chs * 100:.0f}%・キック {ks * 100:.0f}%{'・場面の並びが同じ' if fm else ''}{flag}")
    return bad


SLUG = r"-(v|t|r|j)\d+[a-z]*(vo|full|solo)?\.json$|\.sunshine-song\.json$|\.json$"
ROOTS = ["/mnt/user-data/outputs", "assets-src/ai-songs", "src/audio/songs", "src/audio/songs-archive", "dist-songs"]
CACHE = "/tmp/vp25/similar-index2.pkl"


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
                    idx[p] = (st.st_mtime, (set(r2), s2, set(bs2), j2.get("title", ""), style(j2)))
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
    if sys.argv[1] == "--plan":
        # 作る前の確かめ: python3 tools/vt3/similar_check.py --plan bpm=122 chords="Ebmaj9 Dbmaj9 Cm9 Abm6 ..." patches=kfbGlassEp,kfbSub,bass,...
        kv = dict(a.split("=", 1) for a in sys.argv[2:])
        st = {"bpm": float(kv.get("bpm", 0)), "pal": set(x for x in kv.get("patches", "").split(",") if x), "ch": chord_grams(kv.get("chords", "")), "kick": set(), "form": ()}
        print("■ 作る前の確かめ（曲調が、今までの曲と似ていないか）")
        bad = print_style(st, build_index(ROOTS), None)
        print("  →", "似ている曲があります。曲調を決め直す" if bad else "目安をこえる曲はありません")
        return 1 if bad else 0
    target = sys.argv[1]; dirs = sys.argv[2:] or ROOTS
    js = json.load(open(target)); beats = js.get("beats", 4); mel, bass = pick(js)
    slug = re.sub(SLUG, "", os.path.basename(target))
    mr, ms, _ = feats(mel, beats) if mel else ([], set(), [])
    br, _, bshape = feats(bass, beats, True) if bass else ([], set(), [])
    rows = []
    index = build_index(dirs)
    for s, ft in index.items():
        r2, s2, bs2, title = ft[:4]
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
    bad += print_style(style(js), index, slug)
    print("  →", "似ている曲があります。作る前に直す" if bad else "目安をこえる曲はありません（最後は耳で確かめる）")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
