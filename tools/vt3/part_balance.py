#!/usr/bin/env python3
"""仕上がった曲を分けて、場面ごとに「歌と、ほかのパートの大きさ」を出す（2026-11-18）。
人間（2026-10-14）「各パートごとに音を数値化して調整し、最後にまとめて調整して」、基本の学びなおし「音量はいちばん大事な音（歌）から決める」。
18 v3 のはじめの書き出しで、ベースが歌より 9dB 大きく、ハープがほとんど聞こえないのを、これで見つけた。
使い方: python3 tools/vt3/part_balance.py <曲（歌入りの mp3）> <場面の秒 .secs>
大きさは、耳の感じ方に近い重み（K 特性）をかけて測る。
目安: 歌は、伴奏ぜんぶの合計から −8〜+1dB の中（歌をのせるしくみの狙いは約 −5dB。2026-10-25 人間「伴奏より圧倒的に声が大きく聞こえる」で決めた）。
      どのパートも歌より 6dB 以上大きくならない。ベースは歌より大きくならない。
注意: Demucs の分け方は 歌・ドラム・ベース・ギター（はじく弦。ハープもここ）・ピアノ・そのほか（弦・笛・シンセ）。きれいには分かれない（±2dB くらいは誤差）。"""
import sys, os, json, warnings
warnings.filterwarnings("ignore")
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "song-analyzer")); import analyze as A
JA = {"vocals": "歌", "drums": "ドラム", "bass": "ベース", "guitar": "ギター・ハープ", "piano": "ピアノ", "other": "そのほか"}
secs = json.load(open(sys.argv[2])); st = A.separate(A.load_audio(sys.argv[1])); st = {k: np.asarray(v, dtype=np.float32) for k, v in st.items()}; n = min(v.shape[-1] for v in st.values())
from scipy import signal
def kw(x):
    """耳の感じ方に近い重み（K 特性: 100Hz より下を弱め、1.5kHz より上を +4dB）。歌をのせるしくみ（tools/singer/sing.py）と同じ。
    低い音の多い伴奏は、音の強さ（RMS）で測ると大きく出るが、耳には小さい（2026-10-25 人間「伴奏に対して声がでかすぎる」のときの学び）"""
    sr = A.SR; bh, ah = signal.butter(2, 100 / (sr / 2), "high"); y = signal.lfilter(bh, ah, x)
    w0 = 2 * np.pi * 1500 / sr; G = 10 ** (4 / 40); al = np.sin(w0) / 2 * np.sqrt(2); cs = np.cos(w0); sq = 2 * np.sqrt(G) * al
    bb = [G * ((G + 1) + (G - 1) * cs + sq), -2 * G * ((G - 1) + (G + 1) * cs), G * ((G + 1) + (G - 1) * cs - sq)]; aa = [(G + 1) - (G - 1) * cs + sq, 2 * ((G - 1) - (G + 1) * cs), (G + 1) - (G - 1) * cs - sq]
    return signal.lfilter(np.array(bb) / aa[0], np.array(aa) / aa[0], y)
st = {k: kw(v.mean(0) if v.ndim > 1 else v) for k, v in st.items()}
db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
print("場面 | " + " | ".join(JA[k] for k in JA) + " | 伴奏ぜんぶ | 歌 − 伴奏"); bad = []
for i, s in enumerate(secs):
    if s["name"].startswith("_"): continue
    a = int(s["t"] * A.SR); b = int(secs[i + 1]["t"] * A.SR) if i + 1 < len(secs) else n; b = min(b, n)
    if b - a < A.SR: continue
    lv = {k: db(st[k][..., a:b]) for k in JA}; rest = db(sum(st[k][..., a:b] for k in JA if k != "vocals")); d = lv["vocals"] - rest
    print(f"{s['name']} | " + " | ".join(f"{lv[k]:.1f}" if lv[k] > -60 else "—" for k in JA) + f" | {rest:.1f} | " + (f"{d:+.1f}" if lv["vocals"] > -45 else "（歌なし）"))
    if lv["vocals"] > -45:
        if not -8 <= d <= 1: bad.append(f"{s['name']}: 歌が伴奏より {d:+.1f}dB")
        for k in JA:
            if k != "vocals" and lv[k] > lv["vocals"] + 6: bad.append(f"{s['name']}: {JA[k]}が歌より {lv[k] - lv['vocals']:+.1f}dB 大きい")
        if lv["bass"] > lv["vocals"] and lv["bass"] > -60: bad.append(f"{s['name']}: ベースが大きい（歌 {lv['vocals']:.1f}・ベース {lv['bass']:.1f}）")
print("★ 目安の外: " + " ／ ".join(bad) if bad else "目安の外: なし")
