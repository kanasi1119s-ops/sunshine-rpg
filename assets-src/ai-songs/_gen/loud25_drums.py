# ドラムのフレーズ集（assets-src/drum-phrases/phrases.json.gz）から、曲の区間に合うフレーズを選んで当てはめる（2026-10-22）
# 人間「ドラムのフレーズ、8小節をビート、フィルも含めて1000通りぐらい学んできて」。説明は docs/sound/drum-phrase-library.md
#
# 使い方（例）:
#   from loud25_drums import Library, section_strings, apply_section
#   lib = Library(seed=3)
#   bars = lib.fit(10, kind="verse", bpm=150)                  # 10小節ぶん（最後の小節にフィル）
#   bars = lib.fit(8, kind="chorus", bpm=150, energy=(0.7, 1), styles=["metalcore", "rock"])
#   S = section_strings(bars)   # {"k": "g:...", "s": "g:...", "h": "g:...", "t": "C4:0.25! ...", "c": "C2:4 ..."}
#   apply_section(parts, start_beat, bars)   # loud25_hand.put() で kick/snare/hihat/tom/crash のパートを書きかえる
#
# 1小節 = {k,s,h,t,c}（どれも16文字。1文字＝16分）
#   k キック・s スネア: X 強・x ふつう・o ゴースト / h ハイハット: X x o（閉じ）・O（開き）
#   t タム: 1 ハイ（C4）・2 ミッド（A3）・3 ロー（F3）・4 フロア（D3）、強い打は A B C D
#   c シンバル: c クラッシュ1（C2）・g クラッシュ2（G2）・r ライド（D2）・u ライドのベル（F2）・n チャイナ（B2）・s スプラッシュ（A2）、大文字は強く
import gzip, json, os, random, collections

HERE = os.path.dirname(os.path.abspath(__file__))
LIB_PATH = os.path.normpath(os.path.join(HERE, "..", "..", "drum-phrases", "phrases.json.gz"))
FILL_PATH = os.path.normpath(os.path.join(HERE, "..", "..", "drum-phrases", "fills.json.gz"))
TOM = {"1": "C4", "2": "A3", "3": "F3", "4": "D3"}
CYM = {"c": "C2", "g": "G2", "r": "D2", "u": "F2", "n": "B2", "s": "A2"}

# 区間の種類 → ふだんの条件（energy の範囲・好むノリ・好むシンバル）
KIND = {
    "intro":  dict(energy=(0.15, 0.6)),
    "verse":  dict(energy=(0.3, 0.65)),
    "pre":    dict(energy=(0.45, 0.8)),
    "chorus": dict(energy=(0.65, 1.0), prefer_cym=("crash", "open", "ride")),
    "bridge": dict(energy=(0.3, 0.75), prefer_ride=True),
    "break":  dict(energy=(0.55, 1.0), feel="half", prefer_cym=("china", "crash")),
    "solo":   dict(energy=(0.55, 0.95)),
    "inter":  dict(energy=(0.4, 0.8)),
    "outro":  dict(energy=(0.2, 0.7)),
    "quiet":  dict(energy=(0.0, 0.4)),
}

def _load(path):
    with gzip.open(path, "rt") as f: return json.load(f)

def _perf(pid):
    """同じ演奏（GMD の1ファイル）の印。gmd:drummer1/session1/201:b17 → gmd:drummer1/session1/201"""
    return pid.rsplit(":b", 1)[0] if pid.startswith("gmd:") else pid.rsplit("-", 1)[0]

class Library:
    def __init__(self, seed=0, path=LIB_PATH):
        self.all = _load(path)
        self.by_id = {p["id"]: p for p in self.all}
        self.rnd = random.Random(seed)
        self.used = collections.Counter()      # 曲の中で使った回数（同じものを何度も使わない）
        self.last = None                        # 直前に使ったフレーズ
        self._fills = None

    # ── 選ぶ ──
    def candidates(self, energy=None, feel=None, kind=None, bpm=None, styles=None, sources=None,
                   need_ride=None, need_toms=None, fill_at=None, fill_kinds=None, max_ghost=None, avoid=()):
        """条件に合うフレーズの一覧。
        energy=(下, 上)・feel="normal"/"half"/"double"/"shuffle"（None なら shuffle 以外）・kind=区間の種類（KIND の既定を使う）・
        bpm=曲の速さ（フレーズの元の速さの 0.75〜1.3 倍に入るもの）・styles=["rock", "metalcore", ...]・sources=["GMD"] など・
        need_ride/need_toms=True/False・fill_at=8（その小節にフィルがあるもの）・fill_kinds=["タム下り", ...]・avoid=使わない id"""
        d = dict(KIND.get(kind, {}))
        energy = energy or d.get("energy"); feel = feel if feel is not None else d.get("feel")
        out = []
        for p in self.all:
            if p["id"] in avoid: continue
            if energy and not (energy[0] <= p["energy"] <= energy[1]): continue
            if feel is None and p["feel"] == "shuffle": continue
            if feel and feel != "any" and p["feel"] != feel: continue
            if bpm and not (0.75 <= bpm / p["bpm"] <= 1.3): continue
            if styles and p["style"] not in styles: continue
            if sources and not any(p["source"].startswith(s) for s in sources): continue
            if need_ride is not None and p["uses_ride"] != need_ride: continue
            if need_toms is not None and p["uses_toms"] != need_toms: continue
            if max_ghost is not None and p["ghost"] > max_ghost: continue
            if fill_at:
                fs = [f for f in p["fills"] if f["bar"] == fill_at]
                if not fs: continue
                if fill_kinds and not any(k in fill_kinds for f in fs for k in f["kinds"]): continue
            out.append(p)
        return out

    def _score(self, p, kind, bpm):
        d = KIND.get(kind, {}); s = 0.0
        s -= 2.0 * self.used[p["id"]] + 0.7 * self.used[_perf(p["id"])]
        if bpm: s -= abs(1 - bpm / p["bpm"]) * 2
        for c in d.get("prefer_cym", ()):
            if c in p["cymbals"]: s += 0.4
        if d.get("prefer_ride") and p["uses_ride"]: s += 0.6
        if self.last is not None:
            if p["id"] == self.last["id"]: s -= 100
            # 直前と同じフィルの種類で終わるものは少し下げる（同じ種類を続けない）
            lf = [f["kind"] for f in self.last["fills"] if f["bar"] == 8]
            pf = [f["kind"] for f in p["fills"] if f["bar"] == 8]
            if lf and pf and lf[0] == pf[0]: s -= 0.8
        return s + self.rnd.random() * 1.5     # 同じ条件でも毎回同じにならないように

    def pick(self, kind=None, bpm=None, relax=True, **cond):
        """条件に合うものから1つ選ぶ（直前と同じものは使わない）。見つからなければ条件をゆるめる"""
        avoid = set(cond.pop("avoid", ()))
        if self.last: avoid.add(self.last["id"])
        tries = [cond]
        if relax:
            tries += [dict(cond, fill_kinds=None), dict(cond, fill_kinds=None, styles=None),
                      dict(cond, fill_kinds=None, styles=None, energy=None, need_ride=None, need_toms=None), {}]
        for c in tries:
            for b in (bpm, None):
                cs = self.candidates(kind=kind, bpm=b, avoid=avoid, **c)
                if cs:
                    cs.sort(key=lambda p: -self._score(p, kind, bpm))
                    p = cs[0]; self._use(p); return p
        raise ValueError("フレーズが見つかりません")

    def _use(self, p):
        self.used[p["id"]] += 1; self.used[_perf(p["id"])] += 1; self.last = p

    def next_window(self, p):
        """同じ演奏の次の8小節（GMD のみ。区間の中で同じ叩き手のつながりを保つ）"""
        if not p["id"].startswith("gmd:"): return None
        base, b = p["id"].rsplit(":b", 1)
        return self.by_id.get(f"{base}:b{int(b) + 8}")

    # ── 区間に当てはめる ──
    def fit(self, n_bars, kind="verse", bpm=None, continuity=True, crash_start=True, end_fill=True,
            dynamics=None, **cond):
        """n_bars 小節（8の倍数でなくてよい）のドラムを返す（小節の辞書のリスト）。
        - 8小節ずつフレーズを並べる。区間の途中では、できれば同じ演奏の続き（continuity）を使う
        - 区間の最後のまとまりは、8小節目にフィルのあるフレーズから選び、n が8で割り切れないときはそのフレーズの後ろの小節を使う
          （→ 区間の最後の小節にフィルが来る）
        - crash_start: 区間の頭にクラッシュ（無ければ足す）／dynamics="soft": 一段弱く（繊細な場面）"""
        out = []; prev = None; left = n_bars
        while left > 0:
            take = min(8, left); last_chunk = left <= 8
            c = dict(cond)
            if last_chunk and end_fill: c.setdefault("fill_at", 8)
            p = None
            if continuity and prev is not None:
                q = self.next_window(prev)
                if q and (not c.get("fill_at") or any(f["bar"] == 8 for f in q["fills"])):
                    e = c.get("energy") or KIND.get(kind, {}).get("energy")
                    if not e or e[0] - 0.1 <= q["energy"] <= e[1] + 0.1:
                        p = q; self._use(p)
            if p is None: p = self.pick(kind=kind, bpm=bpm, **c)
            bars = [dict(b) for b in (p["bars"][8 - take:] if last_chunk else p["bars"][:take])]
            for b in bars: b["_id"] = p["id"]
            out += bars; prev = p; left -= take
        if crash_start and out:
            b = out[0]
            if b["c"][0] == "." and b["k"][0] != ".":
                b["c"] = "c" + b["c"][1:]; b["h"] = ("." if b["h"][0] != "o" else "o") + b["h"][1:]
        if dynamics == "soft": out = soften(out)
        elif dynamics == "hard": out = harden(out)
        return out

    # ── GMD の短いフィル（fills.json.gz）で最後の小節を入れかえる ──
    def gmd_fill_bar(self, kinds=None, bpm=None, energy=None):
        if self._fills is None: self._fills = _load(FILL_PATH)
        cs = []
        for p in self._fills:
            if p["feel"] == "shuffle": continue
            nb = len(p["bars"]); fs = [f for f in p["fills"] if f["bar"] == nb]
            if not fs: continue
            if kinds and not any(k in kinds for k in fs[0]["kinds"]): continue
            if bpm and not (0.75 <= bpm / p["bpm"] <= 1.3): continue
            if energy and not (energy[0] <= p["energy"] <= energy[1]): continue
            cs.append(p)
        if not cs: return None
        p = self.rnd.choice(cs); b = dict(p["bars"][-1]); b["_id"] = p["id"]; return b

def soften(bars):
    """一段弱く: X→x、ハイハットの x→o（ゴーストは残す）、シンバルの強打をふつうに"""
    out = []
    for b in bars:
        nb = dict(b)
        nb["k"] = b["k"].replace("X", "x"); nb["s"] = b["s"].replace("X", "x")
        nb["h"] = b["h"].replace("X", "x").replace("x", "o") if b["h"].count("x") + b["h"].count("X") > 4 else b["h"].replace("X", "x")
        nb["t"] = b["t"].translate(str.maketrans("ABCD", "1234")); nb["c"] = b["c"].lower()
        out.append(nb)
    return out

def harden(bars):
    """一段強く: スネアの2・4拍を X、小節頭のシンバルを強く（ゴーストは残す）"""
    out = []
    for b in bars:
        nb = dict(b)
        nb["s"] = "".join("X" if ch == "x" and i in (4, 12) else ch for i, ch in enumerate(b["s"]))
        nb["c"] = (b["c"][0].upper() + b["c"][1:]) if b["c"][0] != "." else b["c"]
        out.append(nb)
    return out

def _notes(g, table):
    """16文字の格子 → 音名の並び（loud25_arrange.to_notes と同じ形。大文字は !）"""
    toks = []; j = 0
    while j < 16:
        c = g[j]; m = j + 1
        while m < 16 and g[m] == ".": m += 1
        d = (m - j) * 0.25
        if c == ".": toks.append(f"R:{d:g}")
        else:
            key = c.lower() if c.lower() in table else "1234"["ABCD".index(c)] if c in "ABCD" else c
            toks.append(f"{table[key]}:{d:g}" + ("!" if c.isupper() else ""))
        j = m
    return " ".join(toks)

def bar_strings(b):
    """1小節 → (k, s, h の16文字, タムの音名の並び, シンバルの音名の並び)"""
    return b["k"], b["s"], b["h"], _notes(b["t"], TOM), _notes(b["c"], CYM)

def section_strings(bars):
    """小節のリスト → パートごとの文字列。k/s/h は "g:..."、t/c は音名の並び（loud25_hand.put() にそのまま渡せる）"""
    k = "".join(b["k"] for b in bars); s = "".join(b["s"] for b in bars); h = "".join(b["h"] for b in bars)
    t = " ".join(_notes(b["t"], TOM) for b in bars); c = " ".join(_notes(b["c"], CYM) for b in bars)
    return {"k": "g:" + k, "s": "g:" + s, "h": "g:" + h, "t": t, "c": c}

def apply_section(parts, a, bars):
    """parts（kick/snare/hihat/tom/crash のパートを含む）の a 拍目からを bars で書きかえる（loud25_hand.put を使う）"""
    from loud25_hand import put
    S = section_strings(bars); b = a + 4 * len(bars)
    find = lambda inst: [p for p in parts if p.get("instrument") == inst]
    for inst, key in (("kick", "k"), ("snare", "s"), ("hihat", "h")):
        for p in find(inst):
            if p["notes"].startswith("g:"): put(p, a, b, S[key][2:])
            else: raise ValueError(f"{inst} は g: の格子で書いてください")
    for inst, key in (("tom", "t"), ("crash", "c")):
        for p in find(inst): put(p, a, b, S[key])
    return S

def describe(bars):
    """選んだフレーズの出どころを短く（確かめ用）"""
    ids = []; [ids.append(b.get("_id")) for b in bars if b.get("_id") not in ids]
    return ids

if __name__ == "__main__":
    # 試し: 12小節の Aメロ（150bpm）と 8小節のサビ、6小節のブレイクダウン
    lib = Library(seed=1)
    for kind, n, kw in (("verse", 12, {}), ("chorus", 8, dict(styles=["rock", "metalcore", "loudrock", "metal"])), ("break", 6, {})):
        bars = lib.fit(n, kind=kind, bpm=150, **kw)
        print(kind, n, describe(bars))
        for b in bars: print("  ", b["k"], b["s"], b["h"], b["t"], b["c"])
