# ケルト（アイルランド・スコットランドの伝統音楽風）の曲を書くための共通の部品（2026-10-16、人間の依頼「ケルト音楽5曲ぐらい作って」）。
# hinowa-op.py（ジグ）で調べて入れた決まりを、拍子の違う曲でも使えるようにまとめた:
#  - 旋律は「1小節＝U 個の細かい単位」で書く（ジグ・スリップジグは1拍を3つ、リール・ホーンパイプ・ポルカは1拍を2つ）。
#  - 飾り: カット（上の音を一瞬）、タップ（下の音を一瞬）、ロール（主音→上→主音→下→主音）。音階の上でとなりの音を使う。
#  - 形: 8小節の A（tune）と B（turn）を、AABB でくり返す。くり返すたびに楽器と飾りを変える。
# 既存の曲のメロディは使わない（CLAUDE.md 1-1）。旋律はすべてこの曲のために書いたもの。
import json, random

N = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def fmt(x): return ("%.6f" % x).rstrip("0").rstrip(".")
def nm(m): return f"{N[m % 12]}{m // 12 - 1}"
def md(n):
    i = 2 if len(n) > 2 and n[1] == "#" else 1
    return N.index(n[:i]) + 12 * (int(n[i:]) + 1)

class Song:
    def __init__(self, beats, sub, nbars, scale):
        """beats: 1小節の拍数、sub: 1拍の細かい単位の数、scale: 音階の音（0〜11）"""
        self.B, self.S, self.U, self.NB, self.scale = beats, sub, beats * sub, nbars, scale
        self.parts, self.order = {}, []
        self.G = 0.06   # 飾りの一瞬の音（拍）

    def nb(self, m, d):
        x = m + d
        while x % 12 not in self.scale: x += d
        return x

    def seq(self, s):
        out = [(t.rsplit(":", 1)[0], int(t.rsplit(":", 1)[1])) for t in s.split()]
        assert sum(k for _, k in out) == self.U, (s, sum(k for _, k in out), self.U)
        return out

    def check(self, *mels):
        for group in mels:
            for m in group: self.seq(m)

    def ornament(self, seq, style, seed, shift=0, dens=1.0, legato=True):
        """style: "roll"（フィドル: 長い音にロール）、"cut"（笛: カット多め）、"plain"（飾りなし）。"""
        r = random.Random(seed); ev = []; u = 1 / self.S; G = self.G
        for j, (n, k) in enumerate(seq):
            d = k * u
            if n == "R": ev.append(("R", d)); continue
            m = md(n) + shift; prev = seq[j - 1][0] if j else None
            if style == "plain": ev.append((m, d)); continue
            if k >= 3 and style == "roll" and d >= 0.75 and r.random() < 0.8 * dens:
                a = d / 3
                ev += [(m, a), (self.nb(m, 1), G), (m, a - G), (self.nb(m, -1), G), (m, a - G)]
            elif k >= 2 and (prev == n or r.random() < (0.45 if style == "cut" else 0.25) * dens):
                ev += [(self.nb(m, 1), G), (m, d - G)]
            elif k >= 2 and r.random() < 0.12 * dens:
                ev += [(m, d - G), (self.nb(m, -1), G)] if False else [(self.nb(m, -1), G), (m, d - G)]
            else: ev.append((m, d))
        return self._toks(ev, legato)

    def plain(self, seq, shift=0, legato=True):
        u = 1 / self.S; ev = [("R" if n == "R" else md(n) + shift, k * u) for n, k in seq]
        return self._toks(ev, legato)

    def _toks(self, ev, legato=True):
        toks = []
        for j, (m, d) in enumerate(ev):
            if m == "R": toks.append(f"R:{fmt(d)}"); continue
            nxt = ev[j + 1][0] if j + 1 < len(ev) else "R"
            # 同じ高さの音へはつながない（つなぐと録音音源の弾き直しでプチッと鳴った）
            toks.append(f"{nm(m)}:{fmt(d)}" + ("_" if legato and nxt != "R" and nxt != m else ""))
        return toks

    def part(self, key, inst, role, vol, pan, **kw):
        self.parts[key] = dict(meta=dict(instrument=inst, role=role, volume=vol, pan=pan, **kw), bars=[None] * self.NB); self.order.append(key)

    def put(self, key, bi, toks):
        if isinstance(toks, str): toks = toks.split()
        t = sum(float("".join(c for c in x.split(":")[1] if c.isdigit() or c == ".")) for x in toks)
        assert abs(t - self.B) < 1e-4, (key, bi, t, toks)
        self.parts[key]["bars"][bi] = " ".join(toks)

    def rest(self, key, bi): self.put(key, bi, [f"R:{self.B}"])

    def grid(self, s, note="x"):
        """1文字＝1単位（U 文字）。X 強・x ふつう・o 弱・. 休み"""
        assert len(s) == self.U, (s, self.U)
        toks = []; i = 0
        while i < self.U:
            c = s[i]; j = i + 1
            while j < self.U and s[j] == ".": j += 1
            d = fmt((j - i) / self.S)
            if c == ".": toks.append(f"R:{d}")
            elif c in "XxoO": toks.append(f"{note}:{d}" + ("!" if c == "X" else ("," if c == "o" else "")))
            else: toks.append(f"{c if False else note}:{d}")
            i = j
        return toks

    def pgrid(self, s, notes):
        """音程つきの刻み。s の文字が notes の鍵（例: {"X": "A2!", "x": "C3", "o": "C3,"}）"""
        assert len(s) == self.U, s
        toks = []; i = 0
        while i < self.U:
            c = s[i]; j = i + 1
            while j < self.U and s[j] == ".": j += 1
            d = fmt((j - i) / self.S)
            if c == ".": toks.append(f"R:{d}")
            else:
                v = notes[c]; acc = v[-1] if v[-1] in "!," else ""; p = v.rstrip("!,")
                toks.append(f"{p}:{d}{acc}")
            i = j
        return toks

    def fill_rest(self):
        for k in self.order:
            for bi in range(self.NB):
                if self.parts[k]["bars"][bi] is None: self.rest(k, bi)

    def dump(self, out, title, desc, bpm, chords, arc, extra=None):
        self.fill_rest()
        parts = []
        for key in self.order:
            p = self.parts[key]
            if all(b == f"R:{self.B}" for b in p["bars"]): continue
            d = dict(p["meta"]); d["notes"] = " ".join(p["bars"]); d["barGain"] = arc; parts.append(d)
        song = {"guitarWobble": False, "title": title, "description": desc, "bpm": bpm, "beats": self.B, "chords": " ".join(chords),
                "barsPerChord": 1, "repeats": 1, "tone": "rock", "feel": "rock", "human": 0.2, "dynamics": "natural",
                "autoAccompaniment": False, "autoScoop": False, "parts": parts}
        if extra: song.update(extra)
        json.dump(song, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("ok", out, len(parts), "parts", self.NB, "bars", round(self.NB * self.B * 60 / bpm, 1), "sec")
