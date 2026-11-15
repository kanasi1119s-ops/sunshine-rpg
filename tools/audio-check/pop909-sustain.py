#!/usr/bin/env python3
"""POP909（MIT）から「音の伸ばし方」の統計だけを出す（2026-11-15。人間「音の伸ばし方とかを勉強するといいかも。」）。
曲ごとの旋律は出さない・保存しない（CLAUDE.md 1-1）。使い方: python3 tools/audio-check/pop909-sustain.py <POP909 のフォルダ> [--out 結果.json]"""
import sys, os, json, numpy as np, mido
root = sys.argv[1]; out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None

def notes(track, tpb):
    t = 0; on = {}; res = []
    for m in track:
        t += m.time
        if m.type == "note_on" and m.velocity > 0: on[m.note] = (t, m.velocity)
        elif m.type in ("note_off", "note_on") and m.note in on:
            s, v = on.pop(m.note); res.append((s / tpb, t / tpb, m.note, v))
    return sorted(res)

def measure(mel, acc=None):
    """mel: [(始まり, 終わり, 高さ, 強さ)]（拍）。返すのは1曲ぶんの数字"""
    r = {}; L = np.array([e - s for s, e, *_ in mel]); tot = L.sum()
    r["音の長さの中央値（拍）"] = float(np.median(L))
    for th, nm in ((0.3, "16分以下の音の数の割合"), ):
        r[nm] = float((L <= th).mean())
    r["1拍以上の音の数の割合"] = float((L >= 0.95).mean()); r["2拍以上の音の数の割合"] = float((L >= 1.9).mean()); r["4拍以上の音の数の割合"] = float((L >= 3.8).mean())
    r["2拍以上の音が、鳴っている時間に占める割合"] = float(L[L >= 1.9].sum() / tot)
    r["いちばん長い音（拍）"] = float(L.max())
    gaps = [mel[i + 1][0] - mel[i][1] for i in range(len(mel) - 1)]; ioi = [mel[i + 1][0] - mel[i][0] for i in range(len(mel) - 1)]
    art = [min(1.0, (mel[i][1] - mel[i][0]) / ioi[i]) for i in range(len(ioi)) if 0.05 < ioi[i] <= 2]
    r["次の音までの時間のうち、鳴らしている割合"] = float(np.median(art)); r["次の音とつながっている（すき間が16分の半分より短い）割合"] = float(np.mean([g < 0.125 for g in gaps]))
    r["短く切っている（半分以下しか鳴らさない）割合"] = float(np.mean([a <= 0.5 for a in art]))
    # 句（1拍以上の休みで区切る）
    ends = [i for i, g in enumerate(gaps) if g >= 1.0] + [len(mel) - 1]; st_ = 0; endL = []; inL = []; lastlong = 0; nph = 0; pos = []
    for e in ends:
        if e - st_ >= 2:
            nph += 1; endL.append(L[e]); inL.extend(L[st_:e]); lastlong += L[e] >= 1.9
            k = int(np.argmax(L[st_:e + 1])); pos.append(k / (e - st_))
        st_ = e + 1
    if nph >= 4:
        r["句の最後の音の長さ（拍）"] = float(np.median(endL)); r["句の途中の音の長さ（拍）"] = float(np.median(inL)); r["句の最後が2拍以上の割合"] = lastlong / nph
        r["句の中でいちばん長い音の位置（0＝頭・1＝最後）"] = float(np.median(pos))
    long_ = [(s, e, n) for s, e, n, *_ in mel if e - s >= 1.9]
    if long_:
        hi = np.percentile([n for s, e, n, *_ in mel], 66)
        r["長い音が高い音域（上3分の1）にある割合"] = float(np.mean([n >= hi for s, e, n in long_])); r["長い音が小節の頭（1拍目）で始まる割合"] = float(np.mean([(s % 4) < 0.13 or (s % 4) > 3.87 for s, e, n in long_]))
        r["長い音が拍のウラ（食って入る）で始まる割合"] = float(np.mean([0.13 < (s % 1) < 0.87 for s, e, n in long_]))
    if acc:
        A = np.array([e - s for s, e, *_ in acc])
        r["伴奏: 音の長さの中央値（拍）"] = float(np.median(A)); r["伴奏: 2拍以上の音の数の割合"] = float((A >= 1.9).mean()); r["伴奏: 4拍以上の音の数の割合"] = float((A >= 3.8).mean())
        r["伴奏: 16分以下の音の数の割合"] = float((A <= 0.3).mean())
        # 歌が伸ばしている間、伴奏は動くか（長い歌の音1つの間に始まる伴奏の音の数）
        if long_: r["歌が伸ばしている間に伴奏が打つ音の数（1拍あたり）"] = float(np.median([sum(1 for a in acc if s <= a[0] < e) / (e - s) for s, e, n in long_]))
        short_ = [(s, e) for s, e, n, *_ in mel if e - s <= 0.6]
    return r

if __name__ == "__main__":
    R = {}; n = 0
    for d in sorted(os.listdir(root)):
        f = os.path.join(root, d, d + ".mid")
        if not os.path.exists(f): continue
        try: m = mido.MidiFile(f)
        except Exception: continue
        tr = {t.name: t for t in m.tracks}
        if "MELODY" not in tr: continue
        mel = notes(tr["MELODY"], m.ticks_per_beat)
        if len(mel) < 40: continue
        n += 1
        for k, v in measure(mel, notes(tr.get("PIANO", []), m.ticks_per_beat)).items(): R.setdefault(k, []).append(v)
    res = {"曲数": n, "中央値と幅（下から25%〜75%）": {k: [round(float(np.percentile(v, p)), 3) for p in (25, 50, 75)] for k, v in R.items()}}
    print(json.dumps(res, ensure_ascii=False, indent=0))
    if out: json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
