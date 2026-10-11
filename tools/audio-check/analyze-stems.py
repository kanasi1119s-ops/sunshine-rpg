#!/usr/bin/env python3
"""楽器ごとの分析（音の分離 → 数字だけを出す）。あなたのパソコンで動かす道具。

使い方（Demucs が入った Python で）:
    python analyze-stems.py 曲1.mp3 [曲2.mp3 ...] --out 結果.json [--keep]

やること:
  0. 長い曲は --start 秒 --dur 秒 で一部だけ測れる（このパソコンでは曲の長さと同じ時間がかかる）。
  1. Demucs（htdemucs_6s）で、ドラム・ベース・ギター・ピアノ・ボーカル・その他に分ける。
     メモリが少ないパソコンでも動くよう、短く区切って処理する（--segment 7）。
  2. 分けた音ごとに「数字」だけを測る（音量の割合・帯域・明るさ・左右の広がり・ぶ厚さ）。
  3. 分けた音の wav は、数字を出したら消す（--keep を付けたときだけ残す）。音そのものは持ち出さない。

出す数字（楽器ごと）:
  share_dB   その楽器が、曲全体の音量に対して何dBか（0に近いほど大きい）
  band_dB    帯域ごとの量（その楽器の中での割合。sub 20-60 / bass 60-250 / lowmid 250-1k / mid 1-4k / presence 4-8k / air 8-16k）
  centroid_Hz 音の重心（高いほど明るい）
  width      左右の広がり（0=真ん中だけ、1=左右が別の音）
  crest_dB   ピークと平均の差（小さいほど潰れている）
  onsets_per_s 1秒あたりの音の出だしの数（刻みの細かさ）

著作権: 数字だけを記録する。分けた音・メロディ・コードは保存しない（CLAUDE.md 1-1、docs/sound/punk-guide.md）。
"""
import argparse, json, os, shutil, subprocess, sys, tempfile
import numpy as np
import soundfile as sf

BANDS = [("sub", 20, 60), ("bass", 60, 250), ("lowmid", 250, 1000), ("mid", 1000, 4000), ("presence", 4000, 8000), ("air", 8000, 16000)]
STEMS = ["drums", "bass", "guitar", "piano", "vocals", "other"]


def db(x):
    return float(20 * np.log10(max(x, 1e-9)))


def measure(y, sr, total_rms):
    """y: (サンプル数, チャンネル) の配列。数字の辞書を返す。"""
    mono = y.mean(axis=1)
    rms = float(np.sqrt(np.mean(mono ** 2)))
    out = {"share_dB": round(db(rms / total_rms), 1)}
    if rms < 1e-5:
        out["silent"] = True
        return out
    spec = np.abs(np.fft.rfft(mono * np.hanning(len(mono)))) ** 2
    freq = np.fft.rfftfreq(len(mono), 1 / sr)
    tot = spec.sum() + 1e-12
    out["band_dB"] = {n: round(10 * np.log10(spec[(freq >= lo) & (freq < hi)].sum() / tot + 1e-12), 1) for n, lo, hi in BANDS}
    # 1/3オクターブごとの量（その楽器の中での割合 dB）。音色を細かく写し取るための数字
    centers = [100 * 2 ** (i / 3) for i in range(21)]  # 100Hz〜約12.7kHz
    th = []
    for c in centers:
        m = (freq >= c / 2 ** (1 / 6)) & (freq < c * 2 ** (1 / 6))
        th.append(round(float(10 * np.log10(spec[m].sum() / tot + 1e-12)), 1))
    out["third_octave_dB"] = dict(zip([str(round(c)) for c in centers], th))
    out["centroid_Hz"] = round(float((freq * spec).sum() / tot))
    peak = float(np.max(np.abs(mono)))
    out["crest_dB"] = round(db(peak / rms), 1)
    if y.shape[1] == 2:
        mid, side = (y[:, 0] + y[:, 1]) / 2, (y[:, 0] - y[:, 1]) / 2
        out["width"] = round(float(np.sqrt(np.mean(side ** 2)) / (np.sqrt(np.mean(mid ** 2)) + 1e-9)), 2)
    # 音の出だし: 10ms ごとの音量の上がり方を数える
    hop = int(sr * 0.01)
    env = np.sqrt(np.convolve(mono ** 2, np.ones(hop) / hop, mode="same"))[::hop]
    d = np.diff(np.log(env + 1e-6))
    thr = max(0.35, float(np.percentile(d, 97)))
    hits = np.where((d[1:-1] > thr) & (d[1:-1] >= d[:-2]) & (d[1:-1] >= d[2:]))[0]
    out["onsets_per_s"] = round(len(hits) / (len(mono) / sr), 2)
    return out


def separate(path, workdir):
    cmd = [sys.executable, "-m", "demucs", "-n", "htdemucs_6s", "--segment", "7", "-d", "cpu", "-j", "1", "--float32", "-o", workdir, path]
    subprocess.run(cmd, check=True)
    name = os.path.splitext(os.path.basename(path))[0]
    return os.path.join(workdir, "htdemucs_6s", name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--start", type=float, default=0, help="何秒目から測るか（長い曲は一部だけ測ると早い）")
    ap.add_argument("--dur", type=float, default=0, help="何秒ぶん測るか（0=最後まで）")
    ap.add_argument("--keep", action="store_true", help="分けた音の wav を残す（既定は消す）")
    a = ap.parse_args()
    result = {}
    for f in a.files:
        work = tempfile.mkdtemp(prefix="stems-")
        try:
            src = f
            if a.start or a.dur:
                src = os.path.join(work, os.path.splitext(os.path.basename(f))[0] + ".wav")
                cut = ["ffmpeg", "-y", "-loglevel", "error", "-ss", str(a.start)] + (["-t", str(a.dur)] if a.dur else []) + ["-i", f, src]
                subprocess.run(cut, check=True)
            d = separate(src, work)
            mix = None
            stems = {}
            for s in STEMS:
                y, sr = sf.read(os.path.join(d, s + ".wav"), always_2d=True)
                stems[s] = y
                mix = y if mix is None else mix + y
            total = float(np.sqrt(np.mean(mix.mean(axis=1) ** 2)))
            result[os.path.basename(f) + (f"@{a.start:g}s" if a.start or a.dur else "")] = {"seconds": round(len(mix) / sr, 1), "stems": {s: measure(y, sr, total) for s, y in stems.items()}}
            if a.keep:
                shutil.copytree(d, os.path.splitext(a.out)[0] + "-" + os.path.basename(d), dirs_exist_ok=True)
        finally:
            shutil.rmtree(work, ignore_errors=True)
        json.dump(result, open(a.out, "w"), ensure_ascii=False, indent=1)
        print("測定:", f, flush=True)


if __name__ == "__main__":
    main()
