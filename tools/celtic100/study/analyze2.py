"""O'Neill's 1850曲（GPL の転写）から、曲の種類ごとの「型」をもっとくわしく数える。
- 本当の旋法（調号の主音から見た最後の音）
- 前半と後半（A部とB部）の高さの差
- 1拍の中のリズムの形（ジグ：8分3つの埋まり方、リール：8分2つ・4つ）
- 4小節ごとの句の終わり方（最後の音の度数、その前の音からの動き）
- エア：いちばん高い音へ入るときの跳躍の大きさ"""
import glob, re, json, collections, sys, warnings
warnings.filterwarnings("ignore")
from music21 import converter, note, key as m21key

MODE_BY_FINAL = {0: "イオニア（長調）", 2: "ドリア", 4: "フリギア", 5: "リディア", 7: "ミクソリディア", 9: "エオリア（短調）", 11: "ロクリア"}
def kind_of(txt, ts):
    t = txt.lower()
    for k in ("slip jig", "hornpipe", "reel", "march", "set dance", "long dance"):
        if k in t: return k
    if ts == "9/8": return "slip jig"
    if ts == "6/8": return "jig" if not re.search(r"slow|air|moderate|plaintive|tender|expression", t) else "air"
    if re.search(r"slow|air|lament|moderate|plaintive|tender|expression", t) or ts in ("3/4", "3/8"): return "air"
    if ts in ("C|", "2/2", "C", "4/4"): return "reel/hornpipe"
    return "other"

out = []
for f in sorted(glob.glob(sys.argv[1] + "/*.abc")):
    txt = open(f, errors="ignore").read()
    K = (re.search(r"^K:\s*(\S+)", txt, re.M) or [None, ""])[1]
    M = (re.search(r"^M:\s*(\S+)", txt, re.M) or [None, "?"])[1]
    head = " ".join(l for l in txt.splitlines() if re.match(r"^[TNR]:", l))
    kind = kind_of(head, M)
    try: s = converter.parse(txt, format="abc")
    except Exception: continue
    # 調号の長調の主音（短調の記号なら相対長調）
    try:
        ks = s.recurse().getElementsByClass("KeySignature")[0]
        maj_tonic = ks.asKey("major").tonic.pitchClass
    except Exception: continue
    ns = [n for n in s.recurse().notes if isinstance(n, note.Note)]
    if len(ns) < 24: continue
    ps = [n.pitch.midi for n in ns]; offs = [float(n.getOffsetInHierarchy(s)) for n in ns]; durs = [float(n.quarterLength) for n in ns]
    fin = ps[-1] % 12
    mode = MODE_BY_FINAL.get((fin - maj_tonic) % 12, "?")
    tonic = fin
    half = len(ps) // 2
    a_mean = sum(ps[:half]) / half; b_mean = sum(ps[half:]) / (len(ps) - half)
    # 拍の中のリズム（ジグ：付点4分＝1.5、リール：2分＝2.0 を1拍として、8分の格子の埋まり方）
    beat = 1.5 if M in ("6/8", "9/8", "12/8") else (2.0 if M in ("C|", "2/2", "C", "4/4") else 1.0)
    grid = 0.5 if beat in (1.5, 2.0) else 0.5
    cells = collections.Counter()
    by_beat = collections.defaultdict(list)
    for o, d in zip(offs, durs): by_beat[int(o // beat)].append(round((o % beat) / grid))
    nslot = int(beat / grid)
    for b, pos in by_beat.items():
        pat = "".join("x" if i in pos else "-" for i in range(nslot))
        cells[pat] += 1
    # 句の終わり（4小節ごと。小節の長さ）
    try: bar_len = s.recurse().getElementsByClass("TimeSignature")[0].barDuration.quarterLength
    except Exception: bar_len = beat * 2
    ends = []
    for k in range(1, int(offs[-1] // (bar_len * 4)) + 1):
        lim = k * bar_len * 4
        idx = [i for i, o in enumerate(offs) if o < lim]
        if len(idx) >= 2:
            i = idx[-1]; ends.append(((ps[i] - tonic) % 12, ps[i] - ps[i - 1]))
    hi = max(range(len(ps)), key=lambda i: ps[i]); leap_in = ps[hi] - ps[hi - 1] if hi else 0
    out.append(dict(kind=kind, meter=M, mode=mode, a_b=round(b_mean - a_mean, 2), cells=dict(cells), ends=ends, leap_in=leap_in,
                    range=max(ps) - min(ps), lo_rel=(min(ps) - tonic) % 12, start_beat_off=round(offs[0] % beat, 2)))
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False)
print(len(out))
