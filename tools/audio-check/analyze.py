#!/usr/bin/env python3
"""曲の「音の作り」を数値で測る道具（2026-09-30）。

使い方:
    python3 tools/audio-check/analyze.py 曲1.wav 曲2.mp3 ... > 結果.json
    python3 tools/audio-check/analyze.py --compare 結果.json   # 目安（docs/sound/reference-nihonichi-bgm.md）と比べて表示
    python3 tools/audio-check/analyze.py --bands 結果.json     # 帯域の偏りを診断し、直し方（どのパラメータを触るか）まで表示

必要なもの: ffmpeg（読み込み・音量の測定）、numpy。
うちの曲の WAV は `node tools/composer/song.mjs build <曲.json> --wav` か、作曲ソフトの「WAVで書き出す」で作る。

測るもの（どれも、曲を聴かずに分かる「音の作り」の数値。旋律・和音は測らない）:
- I（LUFS）: 聞こえ方の音量。TP: いちばん高いピーク（dBTP）。LRA: 曲の中の音量の幅
- crest_dB: ピークと平均の差。小さいほど、つぶれて（圧縮されて）平らな音
- PLR: True Peak − 統合LUFS（ピーク対ラウドネス比）。9未満はつぶれ気味、10〜12がダイナミック（`--compare` で目安と比べる）
- corr: 左右の相関。1に近いほど真ん中に集まった（モノラルに近い）音
- band_dB: 帯域ごとの量（全体に対するdB）。sub 20-60Hz / bass 60-250 / lowmid 250-1k / mid 1k-4k / presence 4k-8k / air 8k-16k
- side_minus_mid_dB: 帯域ごとの広がり（左右の差の成分 − 中央の成分）。0に近いほど広い
- centroid_Hz: 音の重心（高いほど明るく硬い）。tilt_dB_oct: 100Hz〜10kHzの傾き
- flatness_2k8k: 2〜8kHzのざらつき（残響・空気感・シンバルなど、ノイズに近い成分の多さ）
- curve_dB: 5秒ごとの音量（いちばん大きい所を0dBとする）。intro_vs_max_dB: 曲の頭の音量
- tail_s: 最後の音が -20dB から -50dB まで消えるまでの秒数（残響の長さの目安）
"""
import json
import os
import re
import subprocess
import sys

import numpy as np

SR = 44100
BANDS = [(20, 60), (60, 250), (250, 1000), (1000, 4000), (4000, 8000), (8000, 16000)]
BAND_NAMES = ["sub", "bass", "lowmid", "mid", "presence", "air"]

# 参考（日本一フリーBGM 1000曲）の下位10%〜上位10%をもとにした、きれいに聞こえる範囲の目安。
# docs/sound/reference-nihonichi-bgm.md と reference-nihonichi-bgm-1000.md を参照
TARGET = {
    "I": (-15.5, -12.5),
    "TP": (-2.0, -0.8),
    "crest_dB": (12.5, 17.5),
    "PLR": (9.0, 14.5),  # True Peak − 統合LUFS（2026-10-02 追加。一般の目安は 9〜12。参考1000曲の目安からは約 11〜14）
    "LRA": (2.3, 9.0),
    "corr": (0.4, 0.88),
    "intro_vs_max_dB": (-13.0, -2.0),
}


def load(path):
    raw = subprocess.run(
        ["ffmpeg", "-v", "quiet", "-i", path, "-map", "0:a:0", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
        capture_output=True,
    ).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)


def ebur128(path):
    err = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-map", "0:a:0", "-af", "ebur128=peak=true", "-f", "null", "-"],
        capture_output=True,
        text=True,
    ).stderr
    summary = err[err.rfind("Summary"):]
    get = lambda key: float(re.search(key + r":\s+(-?[\d.]+)", summary).group(1))
    return {"I": get("I"), "LRA": get("LRA"), "TP": get("Peak")}


def analyze(path):
    x = load(path)
    mid = (x[:, 0] + x[:, 1]) / 2
    side = (x[:, 0] - x[:, 1]) / 2
    out = ebur128(path)
    out["PLR"] = round(out["TP"] - out["I"], 1)
    out["crest_dB"] = round(float(20 * np.log10(np.max(np.abs(x)) / (np.sqrt(np.mean(x ** 2)) + 1e-12))), 2)

    n, hop = 4096, 2048
    win = np.hanning(n)
    frames = (len(mid) - n) // hop
    idx = np.arange(n)[None, :] + hop * np.arange(frames)[:, None]
    M = np.abs(np.fft.rfft(mid[idx] * win, axis=1)) ** 2
    S = np.abs(np.fft.rfft(side[idx] * win, axis=1)) ** 2
    freq = np.fft.rfftfreq(n, 1 / SR)
    total = M.sum()
    out["band_dB"], out["side_minus_mid_dB"] = {}, {}
    for (lo, hi), name in zip(BANDS, BAND_NAMES):
        k = (freq >= lo) & (freq < hi)
        e = M[:, k].sum()
        out["band_dB"][name] = round(float(10 * np.log10(e / total + 1e-12)), 1)
        out["side_minus_mid_dB"][name] = round(float(10 * np.log10(S[:, k].sum() / (e + 1e-12) + 1e-12)), 1)
    out["corr"] = round(float(np.corrcoef(x[:, 0], x[:, 1])[0, 1]), 3)

    loud = M.sum(1)
    cen = (M * freq).sum(1) / (loud + 1e-12)
    out["centroid_Hz"] = int(np.median(cen[loud > np.percentile(loud, 30)]))
    spec = M.mean(0)
    k = (freq > 100) & (freq < 10000)
    out["tilt_dB_oct"] = round(float(np.polyfit(np.log2(freq[k]), 10 * np.log10(spec[k] + 1e-20), 1)[0]), 2)
    k = (freq > 2000) & (freq < 8000)
    P = M[:, k] + 1e-20
    out["flatness_2k8k"] = round(float(np.median(np.exp(np.log(P).mean(1)) / P.mean(1))), 4)

    seg_len = SR * 5
    seg = np.array([20 * np.log10(np.sqrt(np.mean(mid[i:i + seg_len] ** 2)) + 1e-9) for i in range(0, len(mid) - seg_len, seg_len)])
    out["curve_dB"] = [round(float(v - seg.max()), 1) for v in seg]
    out["intro_vs_max_dB"] = round(float(seg[0] - seg.max()), 1)
    out["end_vs_max_dB"] = round(float(seg[-1] - seg.max()), 1)

    env = 10 * np.log10(loud / loud.max() + 1e-12)
    out["tail_s"] = round(float((np.where(env > -50)[0].max() - np.where(env > -20)[0].max()) * hop / SR), 2)
    out["dur_s"] = round(len(mid) / SR, 1)
    return out


def compare(result_file):
    data = json.load(open(result_file, encoding="utf-8"))
    for name, v in data.items():
        notes = []
        for key, (lo, hi) in TARGET.items():
            if not lo <= v[key] <= hi:
                notes.append(f"{key}={v[key]}（目安 {lo}〜{hi}）")
        print(("○ " if not notes else "△ ") + name + ("" if not notes else "  " + " / ".join(notes)))


# 帯域の目安（参考37曲の全体: docs/sound/reference-nihonichi-bgm.md）。許す幅は±2.5dB（presence・air は±4dB）
BAND_REF = {"sub": -8.8, "bass": -3.3, "lowmid": -5.9, "mid": -11.5, "presence": -22.9, "air": -27.0}
BAND_TOL = {"sub": 2.5, "bass": 2.5, "lowmid": 2.5, "mid": 2.5, "presence": 4, "air": 4}
# 目安より多い／少ないときの直し方（曲JSONのどこを触るか）
BAND_HINT = {
    ("sub", 1): "超低音が多い: キックとベースの volume を下げる／ベースに duck（キックに合わせた凹み）を足す",
    ("sub", -1): "超低音が少ない: キックを足す。sub808 や低いベースの音域を使う（バラードや町の曲では少なくてよい）",
    ("bass", 1): "低音が多い: ベースの volume を下げる。ベースを短く切る（sustain を小さく）。duck 0.3 前後でキックの隙間に入れる",
    ("bass", -1): "低音が少ない: ベースの volume を上げる。ベースの音域を下げる",
    ("lowmid", 1): "250Hz〜1kHz が多い（こもり）: 重なる持続音（弦・パッド・ピアノ）の音域をずらす。パートの bright を下げる",
    ("lowmid", -1): "250Hz〜1kHz が少ない（薄い）: ギター・ピアノなど中域の楽器の volume を上げる、chorus や reverb を足して厚みを出す",
    ("mid", 1): "1〜4kHz が多い（硬い）: リード・歪みギターの volume を下げる。bright を -0.2〜-0.4 に",
    ("mid", -1): "1〜4kHz が少ない（こもる）: リード・アルペジオの volume を上げる。音域を上げる",
    ("presence", 1): "4〜8kHz が多い（刺さる）: drumMix で hat と crash の level を 0.6〜0.8 に。スネアの強さを下げる。シンバルの強いアクセントを減らす",
    ("presence", -1): "4〜8kHz が少ない（こもる）: hat の level を上げる。スネア・アルペジオの音域を上げる",
    ("air", 1): "8kHz 以上が多い: hat・crash を下げる。reverb を減らす",
    ("air", -1): "8kHz 以上が少ない: hat の level を上げる。高いきらめき（アルペジオの高い音）を足す",
}


def bands(result_file):
    """帯域の量・広がり・重心を、目安と比べて、直し方つきで表示する。"""
    data = json.load(open(result_file, encoding="utf-8"))
    for name, v in data.items():
        print("■ " + name)
        bad = 0
        for b, ref in BAND_REF.items():
            d = round(v["band_dB"][b] - ref, 1)
            mark = "○" if abs(d) <= BAND_TOL[b] else "△"
            print(f"  {mark} {b:8s} {v['band_dB'][b]:6.1f}dB（目安 {ref}、差 {d:+}）")
            if mark == "△":
                bad += 1
                print("      → " + BAND_HINT[(b, 1 if d > 0 else -1)])
        lo, hi = TARGET["corr"]
        c = v["corr"]
        print(f"  {'○' if lo <= c <= hi else '△'} 左右の相関 {c}（目安 {lo}〜{hi}）" + ("" if lo <= c <= hi else "  → " + ("狭い: アルペジオ・パッドの pan を左右に振る。chorus を足す" if c > hi else "広すぎる／位相が怪しい: 低音と主旋律を中央に。モノにして確認")))
        print(f"  重心 {v['centroid_Hz']}Hz（参考の全体 約390Hz。しっとり 220〜400／町 350〜550／戦闘 550〜900）")
        print("  → 帯域のバランスは、目安に収まっています" if not bad else f"  → {bad}か所が目安から外れています（上の → を参考に。最後は耳で）")


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--bands":
        bands(sys.argv[2])
        sys.exit(0)
    if len(sys.argv) >= 3 and sys.argv[1] == "--compare":
        compare(sys.argv[2])
        sys.exit(0)
    results = {}
    for f in sys.argv[1:]:
        try:
            results[os.path.basename(f)] = analyze(f)
            print("測定:", f, file=sys.stderr)
        except Exception as e:  # 1曲が読めなくても、ほかの曲は測る
            print("読めませんでした:", f, e, file=sys.stderr)
    json.dump(results, sys.stdout, ensure_ascii=False, indent=1)
