# 使い方: crop.py <in.json> <out.json> <開始小節(0〜)> <小節数> [残すパートの役名の一部,...]
import json, sys, re
sys.path.insert(0, "/home/claude/wt-mix/assets-src/ai-songs/_gen")
from lm25_lib import tok_beats
src, dst, b0, nb = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
keep = sys.argv[5].split(",") if len(sys.argv) > 5 else None
s = json.load(open(src)); B = s["beats"]
t0, t1 = b0 * B, (b0 + nb) * B
def cut(notes):
    if notes.startswith("g:"):
        g = notes[2:]; return "g:" + g[t0 * 4:t1 * 4]
    out, t = [], 0.0
    for x in notes.split():
        L = tok_beats(x); a, b = t, t + L; t = b
        if b <= t0 + 1e-9 or a >= t1 - 1e-9: continue
        na, nbb = max(a, t0), min(b, t1)
        n, v = x.split(":", 1); m = re.match(r"^[0-9.]+", v)
        if na > a + 1e-9: n = "R"
        out.append(f"{n}:{nbb - na:.4f}" + (v[m.end():] if n != "R" else ""))
    return " ".join(out)
parts = []
for p in s["parts"]:
    if keep and not any(k in p["role"] for k in keep): continue
    p["notes"] = cut(p["notes"]); parts.append(p)
s["parts"] = parts
s["chords"] = " ".join(s["chords"].split()[b0:b0 + nb])
s["sections"] = [{"kind": "verse", "bars": nb}]
s.pop("tempo", None)
json.dump(s, open(dst, "w"), ensure_ascii=False)
print("ok", len(parts))
