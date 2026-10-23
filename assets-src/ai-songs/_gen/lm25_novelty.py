# 似た曲・単調な曲を、書き出しの前に数字で見つける（2026-10-24）
# 人間「似た曲を作らない。つまらない曲を作らない。曲として成り立っていない物を作らない。単調にならない」
# 使い方: python3 lm25_novelty.py <調べる曲.json> [<比べる曲.json>...]
#   比べる曲を省くと、/tmp/lm25/ana/*.json（シリーズのほかの曲）と比べる。
# 見るもの:
#   1. 旋律（リード（旋律））の1小節のリズムの形: ほかの曲と同じ形の小節の割合。よく使われすぎた形（シリーズの多くの曲に出る形）の割合
#   2. 旋律の音程の4つ組の重なり（いちばん近い曲）
#   3. 骨組み（区間の種類の並び）の近さ（いちばん近い曲）
#   4. 単調さ: 同じリズムの形が何小節続くか・旋律の小節のうち長い音で終わる小節の割合
import json, glob, sys, os, re
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lm25_lib import tok_beats, tok_note

NAMES = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}


def midi(n):
    m = re.match(r'([A-G])([#b]?)(-?\d)', n or "")
    if not m: return None
    return NAMES[m.group(1)] + (1 if m.group(2) == '#' else -1 if m.group(2) == 'b' else 0) + 12 * (int(m.group(3)) + 1)


def melody_part(s):
    for role in ("リード（旋律）",):
        for p in s["parts"]:
            if p["role"] == role: return p
    cands = [p for p in s["parts"] if p["role"].startswith("リード")]
    return cands[0] if cands else None


def info(path):
    s = json.load(open(path)); B = s["beats"]
    p = melody_part(s)
    bars, notes, t = {}, [], 0.0
    if p:
        for x in p["notes"].split():
            d = tok_beats(x); b = int(t // B)
            if x.startswith("R"): bars.setdefault(b, []).append(f"r{d:g}")
            else:
                bars.setdefault(b, []).append(f"n{d:g}")
                m = midi(tok_note(x))
                if m is not None: notes.append(m)
            t += d
    cells = [" ".join(v) for k, v in sorted(bars.items()) if any(z[0] == "n" for z in v)]
    iv = [b - a for a, b in zip(notes, notes[1:])]
    iv4 = {tuple(iv[i:i + 4]) for i in range(len(iv) - 3)}
    kinds = [x.get("kind") or x.get("name") or "" for x in s.get("sections", [])]
    return dict(title=s.get("title", path), cells=cells, iv4=iv4, kinds=kinds, B=B)


def lev(a, b):
    d = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        prev, d[0] = d[0], i
        for j, y in enumerate(b, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (x != y))
    return d[len(b)]


def main():
    me = sys.argv[1]
    others = sys.argv[2:] or sorted(f for f in glob.glob("/tmp/lm25/ana/*.json") if os.path.abspath(f) != os.path.abspath(me))
    A = info(me); O = {f: info(f) for f in others}
    O = {f: o for f, o in O.items() if o["title"] != A["title"]}
    common = Counter(c for o in O.values() for c in set(o["cells"]))
    n_other = max(1, len(O))
    cells = A["cells"]
    worn = [c for c in cells if common[c] >= n_other * 0.4]
    shared = [c for c in cells if common[c] >= 1]
    print(f"「{A['title']}」 旋律の小節 {len(cells)}・リズムの形 {len(set(cells))} 種類")
    print(f"  ほかの曲と同じリズムの形の小節: {len(shared) / max(1, len(cells)):.0%}・使われすぎた形（{n_other}曲の4割以上に出る）の小節: {len(worn) / max(1, len(cells)):.0%}")
    for c, k in Counter(worn).most_common(5): print(f"    使われすぎ: {c}（この曲で {k} 小節・ほかの {common[c]} 曲）")
    J = lambda a, b: len(a & b) / max(1, len(a | b))
    near = sorted(((J(A["iv4"], o["iv4"]), o["title"]) for o in O.values()), reverse=True)[:3]
    print("  音程の4つ組の重なり（近い曲）:", "・".join(f"{t} {v:.2f}" for v, t in near))
    fk = sorted(((1 - lev(A["kinds"], o["kinds"]) / max(1, max(len(A["kinds"]), len(o["kinds"]))), o["title"]) for o in O.values() if o["kinds"]), reverse=True)[:3]
    print("  骨組みの近さ（1＝同じ）:", "・".join(f"{t} {v:.2f}" for v, t in fk))
    run, best = 1, 1
    for a, b in zip(cells, cells[1:]):
        run = run + 1 if a == b else 1; best = max(best, run)
    longend = sum(1 for c in cells if c.split()[-1].startswith("n") and float(c.split()[-1][1:]) >= 2) / max(1, len(cells))
    print(f"  同じリズムの形が続く最長: {best} 小節・長い音（2拍以上）で終わる小節: {longend:.0%}")
    bad = []
    if len(worn) / max(1, len(cells)) > 0.25: bad.append("使われすぎたリズムの形が多い")
    if near and near[0][0] > 0.12: bad.append(f"旋律が「{near[0][1]}」に近い")
    if fk and fk[0][0] > 0.7: bad.append(f"骨組みが「{fk[0][1]}」に近い")
    if best >= 4: bad.append("同じリズムの形が4小節以上続く")
    if longend > 0.5: bad.append("小節の終わりで伸ばす歌い方が多い")
    print("  判定:", "要直し（" + "・".join(bad) + "）" if bad else "○")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
