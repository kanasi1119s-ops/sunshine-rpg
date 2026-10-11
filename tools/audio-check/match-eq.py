#!/usr/bin/env python3
"""マッチング EQ: 曲の 1/3 オクターブごとの量を、家族別の目標の形（数字だけ）に寄せる firequalizer の gain_entry を出す。
使い方:
    python3 tools/audio-check/match-eq.py 曲.wav --family rock [--amount 0.4] [--tilt -1.5] [--table]
      --family  docs/sound/data/mix-targets.json の家族名（別名 pop・metal・orch なども可）
      --tilt    家族を使わず、傾き（dB/オクターブ、1kHz 基準）を直接指定する
      --amount  寄せる強さ（既定 0.4。0.5 を超えない＝1 にしない。参考録音の「真似」ではなく帯域の偏りを小さくする道具）
      --table   gain_entry ではなく、帯域ごとの 曲／目標／差／当てる量 の表を出す
出力（既定）: `entry(63,0);entry(80,0.4);...` の 1 行。tools/composer/master.mjs が firequalizer=gain_entry='...' に入れる。
制限: 当てるのは 80Hz〜12.5kHz だけ、1 帯域あたり ±3dB で切ってから amount を掛ける。端（63Hz 以下・16kHz 以上）は 0dB。
必要なもの: ffmpeg、numpy。参考録音は数字だけを使う（CLAUDE.md 1-1）。"""
import argparse, json, os, subprocess, sys
import numpy as np

SR = 44100
CENTERS = [63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500, 16000]
LO, HI = 80, 12500   # 当てる範囲
CLAMP = 3.0          # 差を切る幅（dB）
MAX_AMOUNT = 0.5
HERE = os.path.dirname(os.path.abspath(__file__))
TARGETS = os.path.join(HERE, "../../docs/sound/data/mix-targets.json")


def load_family(name):
    data = json.load(open(TARGETS, encoding="utf-8"))
    name = data.get("aliases", {}).get(name, name)
    if name not in data["families"]:
        raise SystemExit(f"家族名がありません: {name}（{', '.join(data['families'])}）")
    return data["families"][name]["tilt_dB_oct"]


def third_octave_db(path, seconds=150):
    """1/3 オクターブごとの量（dB）。曲の頭から seconds 秒まで。"""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-t", str(seconds), "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
    if len(x) < SR:
        raise SystemExit("短すぎて測れません（1 秒以上が必要）")
    spec = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
    freq = np.fft.rfftfreq(len(x), 1 / SR)
    out = {}
    for c in CENTERS:
        m = (freq >= c / 2 ** (1 / 6)) & (freq < c * 2 ** (1 / 6))
        out[c] = 10 * np.log10(spec[m].sum() + 1e-20)
    return out


def match_gains(measured, tilt, amount):
    """帯域ごとの当てる量（dB）。1kHz の帯域を基準に、目標の傾きとの差を amount 倍し、±3dB で切る。"""
    amount = max(0.0, min(MAX_AMOUNT, amount))
    ref = measured[1000]
    # 音程のある曲は帯域の量がでこぼこするので、差は隣の帯域と混ぜてなめらかにする（1:2:1）
    raw = [(measured[c] - ref) - tilt * np.log2(c / 1000.0) for c in CENTERS]   # + なら曲のほうが多い
    diffs = [(raw[max(i - 1, 0)] + 2 * raw[i] + raw[min(i + 1, len(raw) - 1)]) / 4 for i in range(len(raw))]
    rows = []
    for c, d0 in zip(CENTERS, diffs):
        target = tilt * np.log2(c / 1000.0)
        diff = d0
        gain = 0.0
        if LO <= c <= HI:
            gain = float(np.clip(-diff, -CLAMP, CLAMP) * amount)
        rows.append((c, measured[c] - ref, target, diff, gain))
    return rows


def entries(rows):
    parts = [f"entry({c},{g:.2f})" for c, _, _, _, g in rows]
    parts.append("entry(20000,0)")
    return ";".join(parts)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("wav")
    ap.add_argument("--family")
    ap.add_argument("--tilt", type=float)
    ap.add_argument("--amount", type=float, default=0.4)
    ap.add_argument("--table", action="store_true")
    a = ap.parse_args()
    if a.tilt is None and not a.family:
        raise SystemExit("--family か --tilt を指定してください")
    tilt = a.tilt if a.tilt is not None else load_family(a.family)
    rows = match_gains(third_octave_db(a.wav), tilt, a.amount)
    if a.table:
        print(f"目標の傾き {tilt} dB/oct、amount {min(MAX_AMOUNT, a.amount)}（1kHz=0 基準）")
        print("Hz     曲(dB)  目標(dB)  差     当てる量(dB)")
        for c, m, t, d, g in rows:
            print(f"{c:>6} {m:>7.1f} {t:>8.1f} {d:>+6.1f} {g:>+8.2f}")
    else:
        print(entries(rows))
