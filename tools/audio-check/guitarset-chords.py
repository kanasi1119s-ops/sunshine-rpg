#!/usr/bin/env python3
"""GuitarSet（プロのギタリスト6人の伴奏の演奏を、弦ごとに記録したデータ。CC BY 4.0。https://zenodo.org/records/3371780 ）から、
「和音の弾き方」の統計を出す（2026-11-15）。人間「ギターは和音の弾き方を学んだ方がいい。」
使い方: python3 tools/audio-check/guitarset-chords.py <annotation のフォルダ> [--out 結果.json]
伴奏（comp）の演奏だけを使う。曲ごとの演奏は出さない・保存しない（ジャンルごとの統計だけ）。
見るもの: 1回のストロークで何本の弦を鳴らすか／どの弦か／弦から弦へのずれ（ミリ秒）と向き（ダウン・アップ）／拍のどこで弾くか／
          音をどれだけのばすか／和音の形（いちばん低い音からの音程）／いちばん低い音は根音か／音域の広さ"""
import sys, os, json, glob, collections, numpy as np
root = sys.argv[1]; out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
STYLE = {"BN": "ボサノバ", "Funk": "ファンク", "Jazz": "ジャズ", "Rock": "ロック", "SS": "弾き語り"}
PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def pc(n): return (PC[n[0]] + n.count("#") - n.count("b")) % 12
G = collections.defaultdict(lambda: collections.defaultdict(list)); SHAPE = collections.defaultdict(collections.Counter); STR = collections.defaultdict(lambda: np.zeros(6))
POSD = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0])); NF = collections.Counter(); NSTR = collections.defaultdict(collections.Counter)
for f in sorted(glob.glob(os.path.join(root, "*_comp.jams"))):
    st = STYLE[os.path.basename(f).split("_")[1].rstrip("0123456789-ABCDEFGb#").rstrip("-")] if False else STYLE[[k for k in STYLE if os.path.basename(f).split("_")[1].startswith(k)][0]]
    d = json.load(open(f)); notes = []; beats = []; chords = []; tempo = 120
    for a in d["annotations"]:
        if a["namespace"] == "note_midi":
            s = int(a["annotation_metadata"]["data_source"])
            for x in a["data"]: notes.append((x["time"], x["duration"], round(x["value"]), s))
        elif a["namespace"] == "beat_position": beats = [(x["time"], x["value"]["position"]) for x in a["data"]]
        elif a["namespace"] == "tempo": tempo = a["data"][0]["value"]
        elif a["namespace"] == "chord" and not a["annotation_metadata"].get("data_source"): chords = [(x["time"], x["time"] + x["duration"], x["value"]) for x in a["data"]]
    if len(notes) < 20 or len(beats) < 8: continue
    NF[st] += 1; g = G[st]; notes.sort(); spb = 60 / tempo; bt = np.array([b[0] for b in beats])
    # ストローク: 始まりが 60ミリ秒以内につづく音をまとめる
    strums = []; cur = [notes[0]]
    for n in notes[1:]:
        if n[0] - cur[-1][0] <= 0.06 and n[0] - cur[0][0] <= 0.15: cur.append(n)
        else: strums.append(cur); cur = [n]
    strums.append(cur)
    g["1小節あたりのストロークの数"].append(len(strums) / (len(beats) / 4))
    for k, sm in enumerate(strums):
        ns = len({x[3] for x in sm}); NSTR[st][min(ns, 6)] += 1
        t0 = sm[0][0]; i = int(np.searchsorted(bt, t0 + 0.02)) - 1
        if i < 0: continue
        fr = (t0 - bt[i]) / spb; q = int(round(fr * 4)) % 4; where = ["拍の頭", "16分ウラ", "8分ウラ", "16分ウラ"][q]
        g["位置: " + where].append(1); 
        for w in ("拍の頭", "8分ウラ", "16分ウラ"):
            if w != where: g["位置: " + w].append(0)
        nxt = strums[k + 1][0][0] if k + 1 < len(strums) else t0 + 2 * spb
        ring = np.median([min(1.5, x[1] / max(0.05, nxt - t0)) for x in sm]); g["次のストロークまでのうち、鳴らしている割合"].append(ring)
        g["音の長さ（拍）"].append(np.median([x[1] for x in sm]) / spb)
        if ns >= 3:
            ts = np.array([x[0] for x in sm]); ss = np.array([x[3] for x in sm]); spread = (ts.max() - ts.min()) * 1000
            g["3本以上のストローク: 最初の弦から最後の弦までのずれ（ミリ秒）"].append(spread); g["3本以上のストローク: 弦1本あたりのずれ（ミリ秒）"].append(spread / (ns - 1))
            if spread > 4:
                down = np.corrcoef(ts, ss)[0, 1] > 0; POSD[st][where][0 if down else 1] += 1
            ps = sorted({x[2] for x in sm}); g["音域の広さ（半音）"].append(ps[-1] - ps[0]); g["ちがう音の名前の数"].append(len({p % 12 for p in ps}))
            SHAPE[st][" ".join(str(p - ps[0]) for p in ps)] += 1
            ch = next((c for c in chords if c[0] <= t0 < c[1]), None)
            if ch and ch[2] != "N": g["いちばん低い音が根音"].append(float(ps[0] % 12 == pc(ch[2].split(":")[0])))
            for x in sm: STR[st][x[3]] += 1
            g["低い弦（6〜4弦）だけ"].append(float(max(ss) <= 2)); g["高い弦（3〜1弦）だけ"].append(float(min(ss) >= 3))
res = {}
for st, n in NF.items():
    g = G[st]; r = {"演奏の数": n}
    tot = sum(NSTR[st].values()); r["1回に鳴らす弦の数（割合%）"] = {f"{k}本": round(v / tot * 100) for k, v in sorted(NSTR[st].items())}
    for k, v in g.items():
        r[k] = round(float(np.mean(v)), 2) if k.startswith("位置") or k.startswith("いちばん低い") or k.endswith("だけ") else [round(float(np.percentile(v, p)), 2) for p in (25, 50, 75)]
    r["向き（ダウンの割合%）"] = {w: round(a / max(1, a + b) * 100) for w, (a, b) in POSD[st].items()}
    s = STR[st]; r["弦ごとの使われ方（6弦→1弦。割合%）"] = [round(x / s.sum() * 100) for x in s]
    t = sum(SHAPE[st].values()); r["和音の形（いちばん低い音からの半音。多い順）"] = {k: f"{v / t * 100:.1f}%" for k, v in SHAPE[st].most_common(10)}
    res[st] = r
print(json.dumps(res, ensure_ascii=False, indent=1))
if out: json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
