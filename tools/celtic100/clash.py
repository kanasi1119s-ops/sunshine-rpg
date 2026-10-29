# 笛と、伴奏の旋律（パート名を指定）がぶつかる所（同じ音・オクターブ・2度）を数える。使い方: python3 clash.py c003.json "ピアノ（祖父の節）"
import json, re, sys
d = json.load(open(sys.argv[1])); other = sys.argv[2]
N = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def m(t):
    g = re.match(r"([A-G])(#?)(-?\d)", t); return N[g.group(1)] + (1 if g.group(2) else 0) + 12 * (int(g.group(3)) + 1)
def evs(s):
    t = 0; o = []
    for tok in s.split():
        n, L = tok.split(":")[:2]; L = float(re.match(r"[\d.]+", L).group())
        if n not in ("R", "-"): o.append((t, L, m(n)))
        t += L
    return o
P = {p["role"]: evs(p["notes"]) for p in d["parts"]}
F = P["フルート"]; T = P[other]; B = d.get("beats") or 3
def at(ev, x):
    for t, L, mm in ev:
        if t <= x < t + L: return mm
bad = []
for t, L, mm in F:
    if L < 0.5: continue
    for x in (t, t + L / 2):
        p = at(T, x)
        if p is None: continue
        iv = abs(mm - p) % 12
        if iv in (0, 1, 11) or (iv in (2, 10) and abs(mm - p) < 3): bad.append((int(x // B) + 1, round(x % B, 2), mm, p, abs(mm - p)))
print(len(bad), bad)
