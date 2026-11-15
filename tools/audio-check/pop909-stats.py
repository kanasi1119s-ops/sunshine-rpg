#!/usr/bin/env python3
"""POP909（プロが編曲したポップス909曲の MIDI。MIT ライセンス。https://github.com/music-x-lab/POP909-Dataset）から、
「休符の使い方・音の詰まり具合・和音の使い方」の統計だけを出す（2026-11-15。人間「使ってOKなフリー曲で確認してみて」「和音は今後使うようにして」）。
曲ごとの旋律・コードの並びは出さない・保存しない（CLAUDE.md 1-1）。出すのは全曲を合わせた割合だけ。
使い方: python3 tools/audio-check/pop909-stats.py <POP909 のフォルダ> [--out 結果.json]"""
import sys, os, json, collections, statistics as st
import mido, numpy as np

root = sys.argv[1]; out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def pc(n): return (PC[n[0]] + n.count("#") - n.count("b")) % 12
DEG = {0: "I", 1: "♭II", 2: "II", 3: "♭III", 4: "III", 5: "IV", 6: "♯IV", 7: "V", 8: "♭VI", 9: "VI", 10: "♭VII", 11: "VII"}

def notes(track, tpb):
    t = 0; on = {}; res = []
    for m in track:
        t += m.time
        if m.type == "note_on" and m.velocity > 0: on[m.note] = t
        elif m.type in ("note_off", "note_on") and m.note in on: res.append((on.pop(m.note) / tpb, t / tpb, m.note))
    return sorted(res)

R = collections.defaultdict(list); qual = collections.Counter(); deg = collections.Counter(); trans = collections.Counter(); nsong = 0
for d in sorted(os.listdir(root)):
    f = os.path.join(root, d, d + ".mid")
    if not os.path.exists(f): continue
    try: m = mido.MidiFile(f)
    except Exception: continue
    tr = {t.name: t for t in m.tracks}
    if "MELODY" not in tr: continue
    mel = notes(tr["MELODY"], m.ticks_per_beat); pn = notes(tr.get("PIANO", []), m.ticks_per_beat)
    if len(mel) < 40: continue
    nsong += 1
    a, b = mel[0][0], mel[-1][1]; nb = int((b - a) // 4)
    if nb < 16: continue
    # 16分のマスで、旋律が鳴っているか
    g = np.zeros(int((b - a) * 4) + 1, bool); g2 = np.zeros_like(g)
    for s, e, n in mel: g[int((s - a) * 4):max(int((s - a) * 4) + 1, int(round((e - a) * 4)))] = True
    for s, e, n in pn:
        if a <= s < b: g2[int((s - a) * 4):max(int((s - a) * 4) + 1, int(round((e - a) * 4)))] = True
    R["旋律が休んでいる時間の割合"].append(1 - g.mean()); R["伴奏が休んでいる時間の割合"].append(1 - g2.mean()); R["旋律も伴奏も休んでいる割合"].append((~g & ~g2).mean())
    per = [sum(1 for s, e, n in mel if a + 4 * k <= s < a + 4 * k + 4) for k in range(nb)]
    R["旋律がまるごと休みの小節の割合"].append(sum(1 for x in per if x == 0) / nb); act = [x for x in per if x]
    R["歌っている小節の音の数（中央値）"].append(st.median(act)); R["歌っている小節の音の数（多い方10%）"].append(float(np.percentile(act, 90)))
    R["小節ごとの音の数のばらつき（標準偏差÷平均）"].append(float(np.std(act) / np.mean(act)))
    # 休みの長さ（拍）・句の長さ
    gaps = [mel[i + 1][0] - mel[i][1] for i in range(len(mel) - 1)]; big = [x for x in gaps if x >= 1.0]
    R["1拍以上の休みの回数（8小節あたり）"].append(len(big) / nb * 8); R["2拍以上の休みの回数（8小節あたり）"].append(sum(1 for x in gaps if x >= 2) / nb * 8)
    ph = []; s0 = mel[0][0]
    for i, x in enumerate(gaps):
        if x >= 1.0: ph.append(mel[i][1] - s0); s0 = mel[i + 1][0]
    if ph: R["句の長さ（拍・中央値）"].append(st.median(ph))
    pos = collections.Counter(round(((s - a) % 4) * 4) % 16 for s, e, n in mel)
    R["小節の頭（1拍目）から始まる音の割合"].append(pos[0] / len(mel)); R["拍のウラ（16分でずれた所）の音の割合"].append(sum(v for k, v in pos.items() if k % 2) / len(mel))
    R["8分のウラの音の割合"].append(sum(v for k, v in pos.items() if k % 4 == 2) / len(mel))
    iv = [abs(mel[i + 1][2] - mel[i][2]) for i in range(len(mel) - 1)]
    R["跳ぶ音程（5半音以上）の割合"].append(sum(1 for x in iv if x >= 5) / len(iv)); R["音域（半音）"].append(max(n for s, e, n in mel) - min(n for s, e, n in mel))
    # 和音
    try:
        key = open(os.path.join(root, d, "key_audio.txt")).read().split("\n")[0].split("\t")[2]; kt = pc(key.split(":")[0]); minor = "min" in key
        ch = [l.split("\t") for l in open(os.path.join(root, d, "chord_midi.txt")).read().strip().split("\n")]
        bt = [float(l.split()[0]) for l in open(os.path.join(root, d, "beat_midi.txt")).read().strip().split("\n")]
    except Exception: continue
    spb = float(np.median(np.diff(bt))); seq = []
    for s, e, c in ch:
        if c == "N" or ":" not in c: continue
        r, q = c.split(":"); q = q.split("/")[0]; L = (float(e) - float(s)) / spb
        dg = DEG[(pc(r) - kt) % 12] + ("m" if q.startswith("min") or q.startswith("dim") else "")
        qual[q] += L; deg[("短調 " if minor else "長調 ") + dg] += L
        if not seq or seq[-1] != (dg, q): seq.append((dg, q))
    for x, y in zip(seq, seq[1:]): trans[("短調 " if minor else "長調 ") + x[0] + " → " + y[0]] += 1
    tot = sum((float(e) - float(s)) for s, e, c in ch if c != "N") / spb / 4
    if tot > 8: R["和音が変わる回数（1小節あたり）"].append(len(seq) / tot)

res = {"曲数": nsong, "中央値と幅（下から25%〜75%）": {k: [round(float(np.percentile(v, p)), 3) for p in (25, 50, 75)] for k, v in R.items()}}
tq = sum(qual.values()); res["和音の種類（時間の割合%）"] = {k: round(v / tq * 100, 1) for k, v in qual.most_common(14)}
for mode in ("長調", "短調"):
    dd = {k: v for k, v in deg.items() if k.startswith(mode)}; t = sum(dd.values())
    res[f"{mode}の度数（時間の割合%）"] = {k[3:]: round(v / t * 100, 1) for k, v in sorted(dd.items(), key=lambda x: -x[1])[:12]}
    tt = {k: v for k, v in trans.items() if k.startswith(mode)}; t = sum(tt.values())
    res[f"{mode}の和音の移り方（回数の割合%）"] = {k[3:]: round(v / t * 100, 1) for k, v in sorted(tt.items(), key=lambda x: -x[1])[:14]}
print(json.dumps(res, ensure_ascii=False, indent=1))
if out: json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
