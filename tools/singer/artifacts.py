#!/usr/bin/env python3
"""歌声の「声でない音」（ひずみ・ザラつき・プチッ）を探して、どの歌詞の所かを出す。
  python3 tools/singer/artifacts.py <歌だけの.wav> <曲.json> [--top 25]
自分では音を聴けないので、数字で怪しい所を見つけて直すための道具。
- noise: 母音（声が出ているはずの所）なのに、高い帯域が雑音のように平ら（ザラつき・かすれ）
- click: 波形の急な飛び（プチッ）
- rough: 倍音の並びが乱れている（ガラガラした、ひずんだ声）。基本の高さの倍音の山がはっきりしない
"""
import sys, json, numpy as np, soundfile as sf
from scipy import signal
sys.path.insert(0, __import__("os").path.dirname(__file__))
import sing

def main():
    a = sys.argv[1:]
    wav, songp = a[0], a[1]
    top = int(a[a.index("--top") + 1]) if "--top" in a else 25
    x, sr = sf.read(wav, dtype="float64", always_2d=True); x = x.mean(1)
    song = json.load(open(songp, encoding="utf-8")); vd = song["vocals"][0]; spb = 60 / song["bpm"]
    notes = [n for n in sing.parse_notes(vd["notes"]) if n["lyric"]]
    # 歌詞の時刻
    lab = []
    for n in notes:
        lab.append((n["beat"] * spb, (n["beat"] + n["len"]) * spb, n["lyric"], n["midi"]))
    def where(t):
        for s, e, l, m in lab:
            if s - 0.05 <= t < e: return f"{l}({sing_name(m)})", t - s
        return "-", 0
    nper = 1024; hop = 256
    f, tt, Z = signal.stft(x, sr, nperseg=nper, noverlap=nper - hop)
    P = np.abs(Z) ** 2 + 1e-20
    en = 10 * np.log10(P.sum(0)); ref = np.percentile(en[en > en.max() - 60], 90)
    loud = en > ref - 18
    band = (f > 1500) & (f < 7000)
    flat = np.exp(np.mean(np.log(P[band]), 0)) / np.mean(P[band], 0)
    # 声の高さ（予定の音）での倍音のはっきりさ: 予定の f0 の倍音の位置のパワー ÷ その間のパワー
    hn = np.zeros(len(tt))
    for i, t in enumerate(tt):
        m = None
        for s, e, l, mm in lab:
            if s + 0.06 <= t < e - 0.03: m = mm; break
        if m is None or not loud[i]: hn[i] = np.nan; continue
        f0 = 440 * 2 ** ((m - 69) / 12)
        ks = np.arange(1, 13)
        on = sum(P[np.argmin(np.abs(f - k * f0)), i] for k in ks if k * f0 < 6000)
        off = sum(P[np.argmin(np.abs(f - (k + 0.5) * f0)), i] for k in ks if (k + 0.5) * f0 < 6000)
        hn[i] = 10 * np.log10(on / (off + 1e-20))
    # プチッ
    d2 = np.abs(np.diff(x, 2)); loc = np.sqrt(np.convolve(x * x, np.ones(441) / 441, mode="same"))[1:-1] + 1e-4
    cl = d2 / loc
    out = []
    in_vowel = np.zeros(len(tt), bool)
    for i, t in enumerate(tt):
        for s, e, l, mm in lab:
            if s + 0.07 <= t < e - 0.03: in_vowel[i] = True; break
    for i in np.where(loud & in_vowel & (flat > 0.25))[0]:
        out.append(("noise", tt[i], float(flat[i])))
    for i in np.where(loud & ~np.isnan(hn) & (hn < 6))[0]:
        out.append(("rough", tt[i], float(hn[i])))
    for j in np.where(cl > 3.5)[0][::50]:
        out.append(("click", j / sr, float(cl[j])))
    # 近いものをまとめる
    out.sort(key=lambda r: r[1])
    groups = []
    for r in out:
        if groups and r[0] == groups[-1][0] and r[1] - groups[-1][2] < 0.08:
            groups[-1][2] = r[1]; groups[-1][3].append(r[2])
        else: groups.append([r[0], r[1], r[1], [r[2]]])
    groups = [g for g in groups if g[2] - g[1] >= 0.02 or g[0] == "click"]
    print(f"有声の所の倍音のはっきりさ（中央値）: {np.nanmedian(hn):.1f} dB / ザラつき（中央値）: {np.median(flat[loud & in_vowel]):.3f}")
    print(f"見つかった所: noise {sum(g[0]=='noise' for g in groups)} / rough {sum(g[0]=='rough' for g in groups)} / click {sum(g[0]=='click' for g in groups)}")
    groups.sort(key=lambda g: -(g[2] - g[1] + 0.05) * (np.mean(g[3]) if g[0] != "rough" else (8 - np.mean(g[3]))))
    for g in groups[:top]:
        w, off = where(g[1])
        print(f"{g[0]:5s} {g[1]:7.2f}〜{g[2]:7.2f}s  {w:10s} 音の頭から{off:4.2f}s  値 {np.mean(g[3]):.2f}")

NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def sing_name(m): return f"{NAMES[m % 12]}{m // 12 - 1}"

if __name__ == "__main__":
    main()
