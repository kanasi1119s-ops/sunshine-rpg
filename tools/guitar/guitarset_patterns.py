#!/usr/bin/env python3
"""GuitarSet（6人のギタリストの演奏を、弦ごとに記録したデータ。CC BY 4.0）の伴奏の演奏から、「弾き方の型」を取り出す。
使い方: python3 -I tools/guitar/guitarset_patterns.py <注釈の .jams を置いたフォルダ> <出力.json> [--max 110]
取り出すもの（＝手の動き）: 2小節の中で、いつ（拍）・どの向きに（ダウン／アップ）・何本の弦を・形のどのあたり（低い側〜高い側）を・何ミリ秒かけて・どれだけのばして弾いたか。
取り出さないもの: 音の高さ・和音・旋律（元の演奏の曲は写さない。CLAUDE.md 1-1）。音声は使わない。
出典: Q. Xi, R. Bittner, J. Pauwels, X. Ye, J. P. Bello, "GuitarSet: A Dataset for Guitar Transcription", ISMIR 2018. https://zenodo.org/records/3371780 （CC BY 4.0）"""
import json, os, sys, collections, bisect
src, out = sys.argv[1], sys.argv[2]; MAX = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 110
STYLE = {"BN": "ボサノバ", "Funk": "ファンク", "Jazz": "ジャズ", "Rock": "ロック", "SS": "弾き語り風"}


def load(fn):
    j = json.load(open(os.path.join(src, fn))); notes = []; beats = []
    for a in j["annotations"]:
        if a["namespace"] == "note_midi":
            s = int(a["annotation_metadata"]["data_source"])
            for d in a["data"]: notes.append((d["time"], d["duration"], s))
        elif a["namespace"] == "beat_position":
            for d in a["data"]: beats.append((d["time"], d["value"]["measure"], d["value"]["position"], d["value"]["num_beats"]))
    return sorted(notes), sorted(beats)


def strokes_of(notes, beats):
    """音を「一打」にまとめる（50ミリ秒以内に続けて鳴った別の弦の音は、同じ一打）。返すのは (拍の位置, 向き, 弦の並び, わたる時間ms, のばす拍, 始まりの秒)"""
    bt = [b[0] for b in beats]; spb = (bt[-1] - bt[0]) / (len(bt) - 1)
    def pos(t):
        i = max(0, min(len(bt) - 2, bisect.bisect_right(bt, t) - 1)); return i + (t - bt[i]) / (bt[i + 1] - bt[i])
    groups = []; cur = []
    for n in notes:
        if cur and (n[0] - cur[-1][0] > 0.05 or n[2] in [x[2] for x in cur]): groups.append(cur); cur = []
        cur.append(n)
    if cur: groups.append(cur)
    res = []
    for g in groups:
        st = [x[2] for x in g]; t0 = g[0][0]; spread = (g[-1][0] - t0) * 1000
        if len(g) == 1: d = "s"
        else:
            up = sum(1 for a, b in zip(st, st[1:]) if b < a); dn = len(st) - 1 - up; d = "d" if dn >= up else "u"
        dur = sorted(x[1] for x in g)[len(g) // 2] / spb
        res.append((pos(t0), d, sorted(st), spread, dur, t0))
    return res, spb


def patterns(fn):
    notes, beats = load(fn)
    if len(beats) < 9 or not notes: return []
    nb = beats[0][3]
    if nb != 4: return []
    ss, spb = strokes_of(notes, beats); used = sorted({s for x in ss for s in x[2]}); lo, hi = used[0], used[-1]
    wins = collections.defaultdict(list)
    for p, d, st, spread, dur, t0 in ss:
        w = int(p // 8); q = p - w * 8; slot = round(q * 4)                    # 16分のマス（2小節で32マス）
        if slot >= 32: w += 1; slot = 0; q -= 8
        wins[w].append({"slot": slot, "off": round((q - slot / 4) * spb * 1000, 1), "dir": d, "n": len(st),
                        "lo": round((st[0] - lo) / max(1, hi - lo), 2), "hi": round((st[-1] - lo) / max(1, hi - lo), 2), "spread": round(spread, 1), "len": round(dur, 3)})
    res = []
    for w, sk in wins.items():
        if len(sk) < 3: continue
        key = tuple((s["slot"], s["dir"], 1 if s["n"] == 1 else 2 if s["n"] <= 3 else 3) for s in sk); res.append((key, sk))
    return res


files = sorted(f for f in os.listdir(src) if f.endswith("_comp.jams")); lib = []; seen = {}
for fn in files:
    ps = patterns(fn)
    if not ps: continue
    cnt = collections.Counter(k for k, _ in ps); player, rest = fn.split("_")[0], fn.split("_")[1]; sty = "".join(c for c in rest.split("-")[0] if c.isalpha()); tempo = int(rest.split("-")[1])
    for rank, (key, c) in enumerate(cnt.most_common(2)):                       # その演奏でよく出た型を2つまで
        rhythm = tuple((k[0], k[1]) for k in key)
        if rhythm in seen: seen[rhythm]["同じ型の演奏"] += 1; continue
        sk = next(s for k, s in ps if k == key)
        e = {"id": f"gs-{len(lib) + 1:03d}", "様式": STYLE.get(sty, sty), "テンポ": tempo, "奏者": player, "元の演奏": fn.replace(".jams", ""), "その演奏で出た回数": c, "同じ型の演奏": 1,
             "打数": len(sk), "ダウン": sum(1 for s in sk if s["dir"] == "d"), "アップ": sum(1 for s in sk if s["dir"] == "u"), "単音": sum(1 for s in sk if s["dir"] == "s"),
             "16分のウラ": sum(1 for s in sk if s["slot"] % 2), "strokes": sk}
        seen[rhythm] = e; lib.append(e)
# 100種類ほどにしぼる: 様式ごとにかたよらないよう、和音の打ち（単音でない打）が多い型から順に、様式を回しながら取る
by = collections.defaultdict(list)
for e in lib: by[e["様式"]].append(e)
for v in by.values(): v.sort(key=lambda e: -(e["ダウン"] + e["アップ"]) - e["その演奏で出た回数"])
pick = []
while len(pick) < MAX and any(by.values()):
    for k in sorted(by):
        if by[k] and len(pick) < MAX: pick.append(by[k].pop(0))
for i, e in enumerate(pick): e["id"] = f"gs-{i + 1:03d}"
json.dump({"_説明": "GuitarSet（CC BY 4.0）の伴奏の演奏から取り出した、ギターの弾き方の型（2小節・16分で32マス）。slot＝マス、off＝マスからのずれ（ミリ秒。＋はおくれ）、dir＝d ダウン・u アップ・s 単音、n＝弦の本数、lo〜hi＝その演奏で使った弦の中での位置（0＝いちばん低い弦、1＝いちばん高い弦）、spread＝弦をわたる時間（ミリ秒）、len＝のばす拍。音の高さ・和音は入れていない",
           "_出典": "Q. Xi, R. Bittner, J. Pauwels, X. Ye, J. P. Bello, \"GuitarSet: A Dataset for Guitar Transcription\", ISMIR 2018. https://zenodo.org/records/3371780 (CC BY 4.0)。型への変換: tools/guitar/guitarset_patterns.py",
           "patterns": pick}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=None, separators=(",", ":"))
print("伴奏の演奏", len(files), "本 → 型", len(lib), "種類 →", len(pick), "種類を保存:", dict(collections.Counter(e["様式"] for e in pick)))
