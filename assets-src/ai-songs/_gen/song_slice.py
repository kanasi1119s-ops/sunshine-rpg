# 曲の JSON を小節の範囲で切り出す（長い曲を、いくつかに分けて別のパソコンで書き出すため。2026-10-19）。
# 使い方: python3 song_slice.py <曲.json> <はじめの小節（0から）> <おわりの小節（含まない）> <前の助走の小節> <出力.json>
#  - 助走（pre）の小節も一緒に書き出し、あとで切ってつなぐ。助走より前から鳴っている音は、助走の頭から鳴らし直す。
#  - 終わりは、残響のために 2 小節ぶん余分に入れる（その中の音は、範囲の終わりで切る）。
#  - テンポは曲の頭のテンポ（終わりのゆっくりは、範囲に入るときだけ、ずらして入れる）。
import json, sys
TOL = 1e-6

def parse(tok):
    name, rest = tok.split(":", 1)
    i = 0
    while i < len(rest) and (rest[i].isdigit() or rest[i] == "."): i += 1
    return name, float(rest[:i]), rest[i:]

def fmt(x): return ("%.6f" % x).rstrip("0").rstrip(".")

def R(d):
    out = []
    while d > TOL:
        k = min(d, 8.0); out.append(f"R:{fmt(k)}"); d -= k
    return out

def slice_song(j, a, b, pre, post=2):
    beats = j["beats"]; s0 = (a - pre) * beats; s1 = b * beats; s2 = (b + post) * beats
    out = dict(j); parts = []
    for p in j["parts"]:
        t = 0.0; toks = []; cur = s0
        for tok in p["notes"].split():
            name, d, mk = parse(tok)
            st, en = t, t + d; t = en
            if en <= s0 + TOL or st >= s1 - TOL: continue
            if name == "R": continue
            st2 = max(st, s0); en2 = min(en, s2)
            if st2 > cur + TOL: toks += R(st2 - cur)
            toks.append(f"{name}:{fmt(en2 - st2)}{mk}"); cur = en2
        if cur < s2 - TOL: toks += R(s2 - cur)
        q = dict(p); q["notes"] = " ".join(toks) if toks else " ".join(R(s2 - s0))
        if isinstance(p.get("barGain"), list):
            g = p["barGain"]; q["barGain"] = [g[min(len(g) - 1, k)] for k in range(a - pre, b + post)]
        parts.append(q)
    out["parts"] = parts
    nb = b + post - (a - pre)
    out["chords"] = " ".join((j["chords"].split() + [j["chords"].split()[-1]] * 4)[a - pre:b + post])
    out["dynamics"] = False
    out["tempo"] = [dict(x, bar=x["bar"] - (a - pre)) for x in j.get("tempo", []) if a - pre <= x["bar"] < b + post]
    out["title"] = j["title"] + f"［{a}-{b}］"
    return out

if __name__ == "__main__":
    src, a, b, pre, dst = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    j = json.load(open(src, encoding="utf-8"))
    json.dump(slice_song(j, a, b, pre), open(dst, "w", encoding="utf-8"), ensure_ascii=False)
