#!/usr/bin/env python3
"""雑音の点検（noise_scan.py）が「パチパチ」「プチッ」と言った所で、どの楽器が鳴っていたかを調べる（2026-11-16）。
使い方: python3 tools/vt3/noise_who.py <曲.mp3> --bpm 112
やり方: 曲を楽器ごとに分け（Demucs）、言われた時刻の前後 30ミリ秒で、6kHz より上の音がどの楽器から来ているかの割合を出す。
ドラムや歌の子音から来ていれば、雑音ではなく「打った音・子音の立ち上がり」。どの楽器にも入らない（分けた音を足しても元に戻らない）なら、ほんとうの雑音のうたがい。"""
import sys, os, re, subprocess, collections, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "song-analyzer"))
import analyze as A
from scipy import signal
path = sys.argv[1]; bpm = sys.argv[sys.argv.index("--bpm") + 1] if "--bpm" in sys.argv else "120"
o = subprocess.run(["python3", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audio-check", "noise_scan.py"), path, "--bpm", bpm], capture_output=True, text=True).stdout
ev = []; kind = None
for l in o.splitlines():
    m = re.match(r"\s+(パチパチ|プチッ|音の途切れ|音割れ)", l)
    if m: kind = m.group(1); continue
    if re.match(r"\s+無音", l): kind = None; continue
    m = re.match(r"\s+([\d.]+)秒（(.*?)）", l)
    if m and kind: ev.append((kind, float(m.group(1)), m.group(2)))
wav = A.load_audio(path); st = A.separate(wav); sos = signal.butter(4, 6000 / (A.SR / 2), "high", output="sos"); hp = {k: signal.sosfilt(sos, v.mean(0)) for k, v in st.items()}; mix = signal.sosfilt(sos, wav.mean(0)); tot = collections.Counter(); who = collections.Counter()
NJ = {"drums": "ドラム", "vocals": "歌", "bass": "ベース", "guitar": "ギター", "piano": "ピアノ", "other": "そのほか（シンセなど）"}
print(f"■ {os.path.basename(path)}: 点検が言った所 {len(ev)}か所")
for kind, t, p in ev:
    a, b = int((t - 0.03) * A.SR), int((t + 0.05) * A.SR); e = {k: float(np.sum(v[a:b] ** 2)) for k, v in hp.items()}; s = sum(e.values()) + 1e-12; res = float(np.sum((mix[a:b] - sum(v[a:b] for v in hp.values())) ** 2)) / (float(np.sum(mix[a:b] ** 2)) + 1e-12)
    top = max(e, key=e.get); who[(kind, NJ[top])] += 1; tot[kind] += 1
    print(f"  {kind} {t:7.2f}秒（{p}）: " + "・".join(f"{NJ[k]} {int(v / s * 100)}%" for k, v in sorted(e.items(), key=lambda kv: -kv[1])[:2]) + f"／分けた音に入らない分 {int(res * 100)}%")
print("まとめ: " + "／".join(f"{k[0]}→{k[1]} {v}か所" for k, v in who.most_common()))
