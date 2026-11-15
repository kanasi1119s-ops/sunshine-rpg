#!/usr/bin/env python3
"""Groove MIDI Dataset（プロのドラマーの演奏・CC BY 4.0）から、「アクセントの置き方」の統計を出す（2026-11-15）。
人間「もうちょいドラムの感じ勉強してみて。色々アクセントとかも勉強して。」
使い方: python3 tools/audio-check/gmd-accent.py <groove のフォルダ> [--out 結果.json]
出すもの（ジャンルごと。全演奏を合わせた統計だけ）:
  刻み（ハイハット・ライド）の強さ: 拍の頭／8分のウラ／16分のウラ、どこを強く叩くか
  スネア: 2・4拍目の強さ、ゴーストノート（弱い打）の割合と、小節のどの位置に入るか
  キック: 小節のどの位置に入るか
  オープンハイハット・クラッシュ: 小節のどの位置に入るか
  ずれ: スネアの2・4拍目が、拍より前か後ろか（ミリ秒）
  フィル: 長さ、何を叩くか、強さの上がり方、最後にクラッシュがあるか"""
import sys, os, csv, json, collections, numpy as np, mido
root = sys.argv[1]; out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
KICK = {35, 36}; SNARE = {37, 38, 40}; HATC = {42, 44, 22}; HATO = {46, 26}; RIDE = {51, 53, 59}; TOM = {41, 43, 45, 47, 48, 50, 58}; CRASH = {49, 52, 55, 57}
G = collections.defaultdict(lambda: collections.defaultdict(list)); POS = collections.defaultdict(lambda: collections.defaultdict(lambda: np.zeros(16)))
NB = collections.Counter(); FILL = collections.defaultdict(list)
def load(path):
    m = mido.MidiFile(path); ev = []
    for tr in m.tracks:
        t = 0
        for msg in tr:
            t += msg.time
            if msg.type == "note_on" and msg.velocity > 0: ev.append((t / m.ticks_per_beat, msg.note, msg.velocity))
    return sorted(ev)
for row in csv.DictReader(open(os.path.join(root, "info.csv"))):
    if row["time_signature"] != "4-4": continue
    try: ev = load(os.path.join(root, row["midi_filename"]))
    except Exception: continue
    st = row["style"].split("/")[0]; bpm = float(row["bpm"])
    if row["beat_type"] == "fill":
        if len(ev) < 3: continue
        L = ev[-1][0] - ev[0][0]; n = len(ev); v = [e[2] for e in ev]
        FILL["長さ（拍）"].append(L); FILL["打数"].append(n)
        FILL["スネアの割合"].append(sum(1 for e in ev if e[1] in SNARE) / n); FILL["タムの割合"].append(sum(1 for e in ev if e[1] in TOM) / n); FILL["キックの割合"].append(sum(1 for e in ev if e[1] in KICK) / n)
        FILL["最後がクラッシュ"].append(float(any(e[1] in CRASH for e in ev[-3:])))
        h = len(v) // 2
        if h >= 2: FILL["後半の強さ ÷ 前半の強さ"].append(np.mean(v[h:]) / np.mean(v[:h]))
        if L > 0.5: FILL["1拍あたりの打数"].append(n / L)
        continue
    if len(ev) < 64: continue
    beats = ev[-1][0] - ev[0][0]
    if beats < 16: continue
    NB[st] += 1; g = G[st]
    def q(t):
        s = int(round(t * 4)); return s % 16, (t * 4 - s) / 4      # 小節の中の16分の位置と、格子からのずれ（拍）
    cym = [e for e in ev if e[1] in HATC | RIDE]
    by = {"頭": [], "8ウラ": [], "16ウラ": []}
    for t, n, v in cym:
        s, d = q(t); by["頭" if s % 4 == 0 else ("8ウラ" if s % 4 == 2 else "16ウラ")].append(v)
    if len(by["頭"]) > 8 and len(by["8ウラ"]) > 8:
        g["刻み: 拍の頭の強さ"].append(np.mean(by["頭"])); g["刻み: 8分ウラの強さ"].append(np.mean(by["8ウラ"])); g["刻み: 頭 ÷ 8分ウラ"].append(np.mean(by["頭"]) / np.mean(by["8ウラ"]))
        g["刻み: 強さのばらつき（標準偏差）"].append(np.std([v for t, n, v in cym]))
    if len(by["16ウラ"]) > 8 and len(by["頭"]) > 8: g["刻み: 頭 ÷ 16分ウラ"].append(np.mean(by["頭"]) / np.mean(by["16ウラ"]))
    sn = [e for e in ev if e[1] in SNARE]
    if len(sn) > 8:
        back = [(t, v) for t, n, v in sn if q(t)[0] in (4, 12) and v >= 70]; gh = [(t, v) for t, n, v in sn if v < 50]
        if back:
            g["スネア: 2・4拍目の強さ"].append(np.mean([v for t, v in back])); g["スネア: 2・4拍目のずれ（ミリ秒。＋は後ろ）"].append(np.mean([q(t)[1] for t, v in back]) * 60000 / bpm)
        g["スネア: ゴーストの割合"].append(len(gh) / len(sn))
        if gh: g["スネア: ゴーストの強さ"].append(np.mean([v for t, v in gh]))
        for t, v in gh: POS[st]["ゴースト"][q(t)[0]] += 1
        for t, n, v in sn:
            if v >= 70: POS[st]["スネア（強）"][q(t)[0]] += 1
    for t, n, v in ev:
        s = q(t)[0]
        if n in KICK: POS[st]["キック"][s] += 1
        elif n in HATO: POS[st]["オープンハイハット"][s] += 1
        elif n in CRASH: POS[st]["クラッシュ"][s] += 1
    kv = [v for t, n, v in ev if n in KICK]
    if len(kv) > 8: g["キック: 強さのばらつき"].append(np.std(kv))
    g["オープンハイハット（1小節あたり）"].append(sum(1 for e in ev if e[1] in HATO) / beats * 4); g["クラッシュ（8小節あたり）"].append(sum(1 for e in ev if e[1] in CRASH) / beats * 32)
    g["ライドで刻む演奏"].append(float(sum(1 for e in ev if e[1] in RIDE) > sum(1 for e in ev if e[1] in HATC)))
res = {}
def bars16(a):
    a = a / max(1, a.sum()); return "".join("█" if x >= 0.15 else ("▓" if x >= 0.08 else ("░" if x >= 0.03 else "·")) for x in a) + "  " + " ".join(f"{i + 1}:{x * 100:.0f}%" for i, x in enumerate(a) if x >= 0.08)
for st, n in NB.most_common():
    if n < 8: continue
    r = {"演奏の数": n}
    for k, v in G[st].items(): r[k] = round(float(np.median(v)), 2) if k != "ライドで刻む演奏" else round(float(np.mean(v)), 2)
    for k, a in POS[st].items(): r["位置（16分×16）" + k] = bars16(a)
    res[st] = r
res["フィル"] = {"数": len(FILL["打数"]), **{k: [round(float(np.percentile(v, p)), 2) for p in (25, 50, 75)] if k != "最後がクラッシュ" else round(float(np.mean(v)), 2) for k, v in FILL.items()}}
print(json.dumps(res, ensure_ascii=False, indent=1))
if out: json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
