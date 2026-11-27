#!/usr/bin/env python3
"""パートごとの本当の大きさのつり合いを測る（2026-11-27）。
なぜ要るか: `song.mjs build` は、書き出すたびに全体の大きさをそろえる（--stems でも、パートをぬいた JSON でも）。だから「ギターだけ」「ピアノだけ」を別々に書き出して大きさをくらべても、意味がない
  （volume を2倍にしても同じ大きさで出てくる。2026-11-26〜27 に、これで何度も読みちがえた）。
やり方: 曲の最後に1小節足して、そこで目印の音（同じ volume のシンセの A4）だけを鳴らす。グループごとに「そのグループ＋目印」を書き出し、目印の大きさを 0 として、グループの大きさを読む。
使い方: python3 tools/vt3/balance_check.py <曲.json（切り出しでよい。歌は使わない）> <作業フォルダ> [song.mjs に渡すフラグ…]
  グループは、役の名前で分ける: 左ギター・右ギター・旋律のギター・ピアノ・ベース・ドラム・そのほか。"""
import json, sys, os, copy, subprocess, numpy as np, soundfile as sf
src, work = sys.argv[1], sys.argv[2]; flags = sys.argv[3:]; os.makedirs(work, exist_ok=True)
js = json.load(open(src)); js["vocals"] = []; js.pop("lyrics", None); beats = js.get("beats", 4); nb = len(js["chords"].split()); bar = 60 / js["bpm"] * beats
DR = ("kick", "snare", "hihat", "tom", "crash", "ride", "openhat", "clap", "perc")
def group(p):
    r, i = p["role"], p["instrument"]
    if i in DR or p["notes"].startswith("g:"): return "ドラム"
    if i == "bass": return "ベース"
    if "Lギター" in r: return "左ギター"
    if "Rギター" in r: return "右ギター"
    if "ギター" in r: return "旋律のギター"
    if "ピアノ" in r: return "ピアノ"
    return "そのほか"
for p in js["parts"]:
    p["_g"] = group(p); p["notes"] = p["notes"] + ("." * 16 if p["notes"].startswith("g:") else f" R:{beats}")
    if "barGain" in p: p["barGain"] = list(p["barGain"]) + [1]
    p.pop("phrase", None)
js["chords"] += " " + js["chords"].split()[-1]
if js.get("sections"): js["sections"][-1]["bars"] += 1
pilot = {"role": "目印", "instrument": "lead", "patch": "squareLead", "volume": 0.1, "pan": 0, "notes": f"R:{nb * beats} A4:{beats}"}
res = {}
for g in sorted({p["_g"] for p in js["parts"]}):
    j = copy.deepcopy(js); j["parts"] = [{k: v for k, v in p.items() if k != "_g"} for p in j["parts"] if p["_g"] == g] + [pilot]; j["title"] = "bal"
    f = os.path.join(work, "bal.json"); json.dump(j, open(f, "w"), ensure_ascii=False)
    subprocess.run(["node", "tools/composer/song.mjs", "build", f, "--wav", *flags, "--out", work], stdout=open(os.path.join(work, "bal.log"), "w"), stderr=subprocess.STDOUT)
    y, sr = sf.read(os.path.join(work, "bal.wav")); m = y.mean(1) if y.ndim > 1 else y
    db = lambda x: 20 * np.log10(max(1e-9, float(np.sqrt(np.mean(x ** 2)))))
    body = m[:int(nb * bar * sr)]; pl = m[int((nb + 0.1) * bar * sr):int((nb + 0.9) * bar * sr)]
    # 鳴っている所だけ（50ミリ秒ごとの大きさが、いちばん大きい所から 25dB 以内）の平均
    h = int(sr * 0.05); e = np.array([db(body[i:i + h]) for i in range(0, len(body) - h, h)]); act = e[e > e.max() - 25]
    res[g] = (db(body) - db(pl), float(np.mean(act)) - db(pl), db(y[:int(nb * bar * sr), 0]) - db(y[:int(nb * bar * sr), 1]) if y.ndim > 1 else 0)
print("■ 大きさのつり合い（目印の音を 0dB として。大きい順）")
for g, (a, b, lr) in sorted(res.items(), key=lambda x: -x[1][0]):
    if a > 100: print(f"  {g:8s} （この範囲では弾いていない）"); continue
    print(f"  {g:8s} 全体 {a:+6.1f}dB  鳴っている所 {b:+6.1f}dB  左−右 {lr:+5.1f}dB")
