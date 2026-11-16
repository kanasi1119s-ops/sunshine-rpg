#!/usr/bin/env python3
"""GuitarSet（プロのギタリスト6人の演奏を弦ごとに記録したデータ。CC BY 4.0。https://zenodo.org/records/3371780 ）の「ソロ」の演奏から、
単音（リード）の弾き方の統計を出す（2026-11-16）。人間「調べてないことを調べよう。」→ リードギター・単音の弾き方は、まだ学んでいなかった。
使い方: python3 -I tools/audio-check/guitarset-lead.py <annotation のフォルダ> [--out 結果.json]
ソロ（solo）の演奏だけを使う。1つ1つの演奏は出さない・保存しない（ジャンルごとの統計だけ）。
見るもの: 手数／音の長さ／音をつなげる割合（同じ弦でつなぐ＝ハンマリング・プリング・スライドらしい）／音程の動き／句の長さと休み／句の最後の音／
          拍のどこで弾くか・句をどこから始めるか／和音の音を弾く割合／チョーキング（音の中で高さが上がる）・ビブラート／2本の弦を同時に弾く割合／音域"""
import sys, os, json, glob, collections, numpy as np
root = sys.argv[1]; out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
STYLE = {"BN": "ボサノバ", "Funk": "ファンク", "Jazz": "ジャズ", "Rock": "ロック", "SS": "弾き語り"}
PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
QI = {"maj": (0, 4, 7), "min": (0, 3, 7), "7": (0, 4, 7, 10), "maj7": (0, 4, 7, 11), "min7": (0, 3, 7, 10), "hdim7": (0, 3, 6, 10), "dim": (0, 3, 6), "sus4": (0, 5, 7)}
def pc(n): return (PC[n[0]] + n.count("#") - n.count("b")) % 12
G = collections.defaultdict(lambda: collections.defaultdict(list)); IV = collections.defaultdict(collections.Counter); POS = collections.defaultdict(collections.Counter); START = collections.defaultdict(collections.Counter); NF = collections.Counter()
for f in sorted(glob.glob(os.path.join(root, "*_solo.jams"))):
    st = STYLE[[k for k in STYLE if os.path.basename(f).split("_")[1].startswith(k)][0]]; d = json.load(open(f)); notes = []; cont = {}; beats = []; chords = []; tempo = 120
    for a in d["annotations"]:
        ns = a["namespace"]; src = a["annotation_metadata"].get("data_source")
        if ns == "note_midi":
            for x in a["data"]: notes.append((x["time"], x["duration"], x["value"], int(src)))
        elif ns == "pitch_contour": cont[int(src)] = (np.array(a["data"]["time"]), np.array([v["frequency"] if v["voiced"] else np.nan for v in a["data"]["value"]]))
        elif ns == "beat_position": beats = [x["time"] for x in a["data"]]
        elif ns == "tempo": tempo = a["data"][0]["value"]
        elif ns == "chord" and not src: chords = [(x["time"], x["duration"], x["value"]) for x in a["data"]]
    if len(notes) < 20 or len(beats) < 8: continue
    notes.sort(); spb = 60.0 / tempo; NF[st] += 1; g = G[st]; dur = notes[-1][0] + notes[-1][1] - notes[0][0]
    # 同時に弾いた音をまとめる（30ミリ秒以内）
    ev = []
    for n in notes:
        if ev and n[0] - ev[-1][0][0] < 0.03: ev[-1].append(n)
        else: ev.append([n])
    g["1秒の音の数"].append(len(ev) / dur); g["1拍の音の数"].append(len(ev) / (dur / spb)); g["2本以上の弦を同時に弾く割合"].append(np.mean([len(e) > 1 for e in ev]))
    top = [max(e, key=lambda n: n[2]) for e in ev]; t = np.array([n[0] for n in top]); du = np.array([n[1] for n in top]); mi = np.array([n[2] for n in top]); sg = np.array([n[3] for n in top])
    g["音の長さ（拍・中央値）"].append(np.median(du) / spb); g["16分より短い音の割合"].append(np.mean(du / spb < 0.2)); g["1拍以上の音の割合"].append(np.mean(du / spb >= 1)); g["音域（半音）"].append(np.percentile(mi, 97) - np.percentile(mi, 3))
    gap = t[1:] - (t[:-1] + du[:-1]); conn = gap < 0.03; same = sg[1:] == sg[:-1]; d_iv = np.round(mi[1:]) - np.round(mi[:-1])
    g["次の音とつながっている割合"].append(np.mean(conn)); g["同じ弦でつないで次の音へ（ハンマリング・プリング・スライドらしい）の割合"].append(np.mean(conn & same & (d_iv != 0))); g["弦を変える割合"].append(np.mean(~same))
    for x in np.abs(d_iv): IV[st]["同じ音" if x == 0 else "となり（1〜2半音）" if x <= 2 else "3〜4半音" if x <= 4 else "5〜7半音" if x <= 7 else "8半音以上"] += 1
    g["上がる動きの割合"].append(np.mean(d_iv[d_iv != 0] > 0) if np.any(d_iv != 0) else 0.5)
    # 句（半拍以上の休みで切る）
    cut = np.where(gap >= 0.5 * spb)[0]; seg = np.split(np.arange(len(top)), cut + 1); seg = [s for s in seg if len(s)]
    g["句の音の数（中央値）"].append(np.median([len(s) for s in seg])); g["句の長さ（拍・中央値）"].append(np.median([(t[s[-1]] + du[s[-1]] - t[s[0]]) / spb for s in seg])); g["休んでいる時間の割合"].append(1 - min(1, np.sum(du) / dur))
    lastd = [du[s[-1]] / spb for s in seg if len(s) >= 3]; midd = [np.median(du[s[:-1]]) / spb for s in seg if len(s) >= 3]
    if lastd: g["句の最後の音の長さ（拍）"].append(np.median(lastd)); g["句の途中の音の長さ（拍）"].append(np.median(midd)); g["句の最後が下がって終わる割合"].append(np.mean([mi[s[-1]] < mi[s[-2]] for s in seg if len(s) >= 3]))
    b = np.array(beats)
    def bpos(x):
        i = max(0, min(len(b) - 2, np.searchsorted(b, x) - 1)); return (x - b[i]) / (b[i + 1] - b[i])
    for x in t:
        p = int(round(bpos(x) * 4)) % 4; POS[st][("拍の頭", "16分のウラ", "8分のウラ", "16分のウラ")[p]] += 1
    for s in seg:
        p = int(round(bpos(t[s[0]]) * 4)) % 4; START[st][("拍の頭", "16分のウラ", "8分のウラ", "16分のウラ")[p]] += 1
    # 和音の音か
    def chord_at(x):
        for c in chords:
            if c[0] <= x < c[0] + c[1]: return c[2]
        return None
    ct = []; ctl = []; cte = []; ends = {s[-1] for s in seg}
    for i in range(len(top)):
        c = chord_at(t[i])
        if not c or ":" not in c: continue
        r, q = c.split(":"); q = q.split("/")[0]; tones = {(pc(r) + x) % 12 for x in QI.get(q, QI["maj"] if not q.startswith("min") else QI["min"])}; ok = int(round(mi[i])) % 12 in tones; ct.append(ok)
        if du[i] / spb >= 1: ctl.append(ok)
        if i in ends: cte.append(ok)
    if ct: g["和音の音を弾いている割合"].append(np.mean(ct))
    if len(ctl) >= 3: g["長い音（1拍以上）が和音の音である割合"].append(np.mean(ctl))
    if len(cte) >= 3: g["句の最後の音が和音の音である割合"].append(np.mean(cte))
    # 音の中の高さの動き（チョーキング・ビブラート）
    bend = []; vib = []; glide = []
    for n in top:
        if n[1] < 0.18 or n[3] not in cont: continue
        ct_, cf = cont[n[3]]; a, e = np.searchsorted(ct_, n[0]), np.searchsorted(ct_, n[0] + n[1]); c = cf[a:e]; c = c[~np.isnan(c)]
        if len(c) < 12: continue
        cents = 1200 * np.log2(c / c[0]); k = max(3, len(cents) // 8); head, tail = np.median(cents[:k]), np.median(cents[-k:]); bend.append(np.max(cents) - head >= 70 and np.argmax(cents) > k); glide.append(abs(tail - head) >= 70)
        if n[1] >= 0.35:
            x = cents[len(cents) // 3:]; x = x - np.convolve(x, np.ones(9) / 9, mode="same"); vib.append(np.std(x[4:-4]) >= 12 if len(x) > 16 else False)
    if len(bend) >= 5: g["音の中で高さが上がる（チョーキングらしい）音の割合（0.18秒以上の音のうち）"].append(np.mean(bend)); g["音の頭と終わりで高さがちがう（スライド・チョーキング）音の割合"].append(np.mean(glide))
    if len(vib) >= 3: g["のばした音（0.35秒以上）にビブラートがある割合"].append(np.mean(vib))
R = {}
def norm(c): s = sum(c.values()) or 1; return {k: round(v / s, 3) for k, v in c.most_common()}
print("演奏の数:", dict(NF))
for st in list(STYLE.values()):
    if st not in G: continue
    R[st] = {k: [round(float(np.percentile(v, 25)), 2), round(float(np.median(v)), 2), round(float(np.percentile(v, 75)), 2)] for k, v in G[st].items()}
    R[st]["音程の動き"] = norm(IV[st]); R[st]["拍のどこで弾くか"] = norm(POS[st]); R[st]["句をどこから始めるか"] = norm(START[st])
keys = list(G["ロック"].keys()); sts = [s for s in STYLE.values() if s in R]
print("| 項目 | " + " | ".join(sts) + " |"); print("|---|" + "---|" * len(sts))
for k in keys: print(f"| {k} | " + " | ".join(f"{R[s][k][1]}（{R[s][k][0]}〜{R[s][k][2]}）" if k in R[s] else "—" for s in sts) + " |")
for nm in ("音程の動き", "拍のどこで弾くか", "句をどこから始めるか"):
    print(f"\n{nm}:")
    for s in sts: print(f"  {s}: " + "／".join(f"{a} {int(b * 100)}%" for a, b in R[s][nm].items()))
if out: json.dump({"演奏の数": dict(NF), "ジャンルごと": R}, open(out, "w"), ensure_ascii=False, indent=1)
