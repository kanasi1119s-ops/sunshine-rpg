"""O'Neill's Music of Ireland（1903年・1850曲。ABC は O'Neill's Project の転写、GPL v2+。転写者に感謝）を分析して、
曲の種類ごとの「型」を数字でつかむ（旋律を写すためではなく、作り方を学ぶため）。"""
import glob, re, json, collections, statistics as st, sys, warnings
warnings.filterwarnings("ignore")
from music21 import converter, interval, key as m21key, note, meter

def kind_of(meta, ts):
    t = (meta.get("R", "") + " " + meta.get("N", "") + " " + meta.get("T", "")).lower()
    if "slip" in t: return "slip jig"
    if "hornpipe" in t: return "hornpipe"
    if "reel" in t: return "reel"
    if "jig" in t and ts in ("6/8",): return "jig"
    if "march" in t: return "march"
    if "set dance" in t or "long dance" in t: return "set dance"
    if "slow" in t or "air" in t or "lament" in t or "moderate" in t or "plaintive" in t or "tender" in t or "with expression" in t or "cheerful" in t:
        return "air"
    if ts == "9/8": return "slip jig"
    if ts == "6/8": return "jig?"
    if ts in ("4/4", "C", "2/2", "C|"): return "reel/hornpipe?"
    if ts in ("3/4", "3/8"): return "air?(3)"
    return "other"

def meta_of(txt):
    m = {}
    for line in txt.splitlines():
        mm = re.match(r"^([A-Za-z]):\s*(.*)$", line)
        if mm and mm.group(1) in "TMRNKLB" and mm.group(1) not in m: m[mm.group(1)] = mm.group(2)
        elif mm and mm.group(1) == "N": m["N"] = m.get("N", "") + " " + mm.group(2)
    return m

rows = []
files = sorted(glob.glob(sys.argv[1] + "/*.abc"))
for f in files:
    txt = open(f, errors="ignore").read()
    meta = meta_of(txt)
    try:
        s = converter.parse(txt, format="abc")
    except Exception as e:
        continue
    ns = [n for n in s.recurse().notes if isinstance(n, note.Note)]
    if len(ns) < 16: continue
    ts = meta.get("M", "?").strip()
    k = s.analyze("key") if not meta.get("K") else None
    K = meta.get("K", "").strip()
    ps = [n.pitch.midi for n in ns]
    durs = [float(n.quarterLength) for n in ns]
    ints = [b - a for a, b in zip(ps, ps[1:])]
    absi = [abs(x) for x in ints]
    try: tonic_pc = m21key.Key(re.sub(r"[^A-Ga-g#b]", "", K[:2]) or "C").tonic.pitchClass
    except Exception: tonic_pc = None
    hi_idx = max(range(len(ps)), key=lambda i: ps[i])
    rows.append(dict(file=f.split("/")[-1], title=meta.get("T", ""), kind=kind_of(meta, ts), meter=ts, K=K,
                     n=len(ps), range=max(ps) - min(ps), step=sum(1 for a in absi if a <= 2) / len(absi),
                     rep=sum(1 for a in absi if a == 0) / len(absi), leap4=sum(1 for a in absi if 5 <= a <= 7) / len(absi),
                     leap6=sum(1 for a in absi if a >= 8) / len(absi), up=sum(1 for a in ints if a > 0) / len(ints),
                     climax=hi_idx / len(ps), longest=max(durs) / (sum(durs) / len(durs)),
                     first_deg=(ps[0] - tonic_pc) % 12 if tonic_pc is not None else None,
                     last_deg=(ps[-1] - tonic_pc) % 12 if tonic_pc is not None else None,
                     mode=re.sub(r"^[A-G][#b]?", "", K.replace(" ", "")).lower() or "maj"))
json.dump(rows, open(sys.argv[2], "w"), ensure_ascii=False)
print(len(rows), "曲を分析")
