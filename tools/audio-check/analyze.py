#!/usr/bin/env python3
"""曲の「音の作り」を数値で測る道具（2026-09-30）。

使い方:
    python3 tools/audio-check/analyze.py 曲1.wav 曲2.mp3 ... > 結果.json
    python3 tools/audio-check/analyze.py --compare 結果.json   # 目安（docs/sound/reference-nihonichi-bgm.md）と比べて表示
    python3 tools/audio-check/analyze.py --bands 結果.json     # 帯域の偏りを診断し、直し方（どのパラメータを触るか）まで表示
    python3 tools/audio-check/analyze.py --bands 結果.json --family rock
        # 参考37曲の平均ではなく、家族別の目標（docs/sound/data/mix-targets.json。rock・punk・edm・hiphop・jazz・lofi・ambient・game-battle。pop・metal・orch なども別名で可）との差を表示
    python3 tools/audio-check/analyze.py --roles 曲.sunshine-song.json
        # 楽譜（作曲ソフトのプロジェクト）から、パートごとの音域と重心(Hz)を出し、席の重なり（200〜500Hz に持続音が複数・キックとベースの重心が近い・低域のパートが多い・低域が中央にない）を警告する
    python3 tools/audio-check/analyze.py --mono-low 曲1.wav [曲2.wav ...]
        # 150Hz 以下の左右の相関を測り、0.9 を下回ったら警告（モノで低音が痩せる）

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


MIX_TARGETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../docs/sound/data/mix-targets.json")


def family_target(family):
    """家族別の帯域の目標（mix-targets.json）。BAND_REF のうち bass・lowmid・mid・presence を置きかえた辞書と、許す幅を返す。"""
    data = json.load(open(MIX_TARGETS, encoding="utf-8"))
    key = data.get("aliases", {}).get(family, family)
    if key not in data["families"]:
        raise SystemExit(f"家族名がありません: {family}（{', '.join(data['families'])}）")
    fam = data["families"][key]
    ref = dict(BAND_REF)
    tol = dict(BAND_TOL)
    for b in ("bass", "lowmid", "mid", "presence"):
        ref[b] = fam[b]
        tol[b] = data["tolerance_dB"][b]
    return ref, tol, fam["label"]


def bands(result_file, family=None):
    """帯域の量・広がり・重心を、目安と比べて、直し方つきで表示する。family を指定すると、その家族の目標との差を出す。"""
    data = json.load(open(result_file, encoding="utf-8"))
    ref_all, tol_all, label = (BAND_REF, BAND_TOL, "参考37曲の平均") if not family else family_target(family)
    for name, v in data.items():
        print("■ " + name + f"  [目標: {label}]")
        bad = 0
        for b, ref in ref_all.items():
            d = round(v["band_dB"][b] - ref, 1)
            mark = "○" if abs(d) <= tol_all[b] else "△"
            print(f"  {mark} {b:8s} {v['band_dB'][b]:6.1f}dB（目安 {ref}、差 {d:+}）")
            if mark == "△":
                bad += 1
                print("      → " + BAND_HINT[(b, 1 if d > 0 else -1)])
        lo, hi = TARGET["corr"]
        c = v["corr"]
        print(f"  {'○' if lo <= c <= hi else '△'} 左右の相関 {c}（目安 {lo}〜{hi}）" + ("" if lo <= c <= hi else "  → " + ("狭い: アルペジオ・パッドの pan を左右に振る。chorus を足す" if c > hi else "広すぎる／位相が怪しい: 低音と主旋律を中央に。モノにして確認")))
        print(f"  重心 {v['centroid_Hz']}Hz（参考の全体 約390Hz。しっとり 220〜400／町 350〜550／戦闘 550〜900）")
        print("  → 帯域のバランスは、目安に収まっています" if not bad else f"  → {bad}か所が目安から外れています（上の → を参考に。最後は耳で）")


# ── 楽譜から見るパートの席（--roles） ──
NOTE_BASE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
NO_PITCH = {"kick", "snare", "hihat", "crash", "tom", "cowbell", "sfxDown", "sfxUp", "impact", "swoosh", "pierce", "wind", "rain", "stream", "bird", "crickets"}
LOW_ROLES = {"kick", "bass", "sub808", "slap"}
SUSTAIN = {"piano", "guitar", "echoGuitar", "crunch", "distGuitar", "strings", "pad", "choir", "keys", "brass", "harp", "leadGuitar", "lead"}


def note_midi(name):
    """音名（A2・C#4・Bb3 など）を MIDI 番号に。読めなければ None（休符など）。"""
    m = re.fullmatch(r"([A-Ga-g])([#b♯♭]?)(-?\d)", str(name))
    if not m:
        return None
    n = NOTE_BASE[m.group(1).upper()] + (1 if m.group(2) in "#♯" else -1 if m.group(2) in "b♭" else 0)
    return 12 * (int(m.group(3)) + 1) + n


def midi_hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def roles(project_file):
    """作曲ソフトのプロジェクト（.sunshine-song.json）のパートごとに、音域・重心(Hz)・席を出し、重なりを警告する。EQ が無いので、直し方は編曲（音域・音量・左右）。"""
    data = json.load(open(project_file, encoding="utf-8"))
    score = data.get("score", data)
    rows = []
    for i, t in enumerate(score["tracks"]):
        inst = t.get("instrument", t.get("waveform", ""))
        ms = [x for x in (note_midi(n.get("note")) for n in t.get("notes", [])) if x is not None]
        if inst in NO_PITCH or t.get("gmDrum") or not ms:
            rows.append({"i": i, "inst": inst, "pan": t.get("pan", 0), "vol": t.get("volume", 0), "rev": t.get("reverb", 0), "lo": None, "hi": None, "hz": None, "mid": None})
            continue
        med = float(np.median(ms))
        rows.append({"i": i, "inst": inst, "pan": t.get("pan", 0), "vol": t.get("volume", 0), "rev": t.get("reverb", 0), "lo": min(ms), "hi": max(ms), "hz": round(midi_hz(med)), "mid": med})
    print("■ " + os.path.basename(project_file))
    names = "C C# D D# E F F# G G# A A# B".split()
    nm = lambda m: f"{names[int(m) % 12]}{int(m) // 12 - 1}"
    for r in rows:
        rng = f"{nm(r['lo'])}〜{nm(r['hi'])}（重心 約{r['hz']}Hz）" if r["lo"] is not None else "（音程なし）"
        print(f"  {r['i'] + 1:>2} {r['inst']:11s} vol {r['vol']:.3f} pan {r['pan']:+.2f}  {rng}")
    warn = []
    body = [r for r in rows if r["inst"] in SUSTAIN and r["mid"] is not None and 250 <= midi_hz(r["mid"]) <= 500]
    kinds = sorted({r["inst"] for r in body})
    if len(kinds) >= 2:
        warn.append(f"200〜500Hz（体の席）に持続音が {len(kinds)} 種類（{'・'.join(kinds)}）。席は 1 つにして、ほかは音域を C4 以上へ上げるか volume を ×0.8（M09）")
    kick = [r for r in rows if r["inst"] == "kick"]
    bass = [r for r in rows if r["inst"] in ("bass", "slap") and r["mid"] is not None]
    if kick and bass and bass[0]["hz"] < 62:
        warn.append(f"ベースの重心が約{bass[0]['hz']}Hz でキック(50〜100Hz)と近い。ベースを 80〜120Hz 以上へ上げるか duck 0.25〜0.35 を足す")
    lows = [r for r in rows if r["inst"] in LOW_ROLES]
    if len(lows) > 3:
        warn.append(f"低域を担うパートが {len(lows)} 個（3 個まで）")
    for r in lows:
        if abs(r["pan"]) > 0.1:
            warn.append(f"{r['inst']}（{r['i'] + 1}番目）が中央でない（pan {r['pan']:+.2f}）。150Hz 以下はモノ")
        if r["rev"] > 0.1:
            warn.append(f"{r['inst']}（{r['i'] + 1}番目）の reverb が {r['rev']}。低音の残響は濁る")
    mids = [r for r in rows if r["mid"] is not None and r["inst"] in SUSTAIN and 1000 <= midi_hz(r["mid"]) <= 4000]
    mk = sorted({r["inst"] for r in mids})
    if len(mk) >= 3:
        warn.append(f"1〜4kHz（輪郭の席）に {len(mk)} 種類（{'・'.join(mk)}）。主役以外は b-0.15 と volume ×0.8（M09）")
    print("  → 席の重なりは見つかりませんでした" if not warn else "\n".join("  △ " + w for w in warn))


def mono_low(paths, cutoff=150):
    """cutoff(Hz) 以下の左右の相関。0.9 を下回ったら警告（モノで低音が痩せる）。"""
    for p in paths:
        raw = subprocess.run(["ffmpeg", "-v", "quiet", "-i", p, "-af", f"lowpass=f={cutoff}:poles=2", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
        x = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
        if len(x) == 0 or np.sum(x[:, 0] ** 2) < 1e-9 or np.sum(x[:, 1] ** 2) < 1e-9:
            c = 1.0
        else:
            c = float(np.corrcoef(x[:, 0], x[:, 1])[0, 1])
        print(("○ " if c >= 0.9 else "△ ") + os.path.basename(p) + f"  {cutoff}Hz 以下の左右の相関 {c:.3f}" + ("" if c >= 0.9 else "（0.9 未満: キック・ベースを pan 0 に。chorus・ダブルを低音パートから外す。広げるのは書き出しの --side-hpf で高域だけに）"))


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--roles":
        roles(sys.argv[2])
        sys.exit(0)
    if len(sys.argv) >= 3 and sys.argv[1] == "--mono-low":
        mono_low(sys.argv[2:])
        sys.exit(0)
    if len(sys.argv) >= 3 and sys.argv[1] == "--bands":
        fam = sys.argv[sys.argv.index("--family") + 1] if "--family" in sys.argv else None
        bands(sys.argv[2], fam)
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
