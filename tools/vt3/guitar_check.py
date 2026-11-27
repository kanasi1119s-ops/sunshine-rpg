#!/usr/bin/env python3
"""ギターの音がちゃんと出ているかを確かめる（2026-11-26 人間「ギターの音ちゃんと出てるかチェックして」）。
使い方: python3 tools/vt3/guitar_check.py <曲.json> <ギターだけ書き出した .wav> <役の名前に含まれる言葉> [bpm]
  先に、そのギターのパートだけ（歌は空）の JSON を作って `song.mjs build … --stems` で書き出しておく。
  ギターだけの書き出しは、頭の弾かない小節が詰められて音が前へずれることがあるので、音符の並びと音の並びを合わせて、ずれを先に求める。
見るもの: 場面ごとの大きさ／音符が4つ以上あるのに小さい小節（-33dB 未満）／小節の頭の1拍だけ小さい小節（-30dB 未満＝ゲートなどで出おくれている）"""
import json, sys, numpy as np, soundfile as sf
jf, wf, key = sys.argv[1:4]; js = json.load(open(jf)); bpm = float(sys.argv[4]) if len(sys.argv) > 4 else js["bpm"]; beats = js.get("beats", 4); bar = 60 / bpm * beats
secs = js.get("sections") or []; nb = sum(s["bars"] for s in secs) if secs else len(js["chords"].split())
cnt = [0] * nb; a = np.zeros(nb * 8)
for p in js["parts"]:
    if key not in p["role"]: continue
    t = 0
    for x in p["notes"].split():
        L = float(x.split(":")[1].split("%")[0].rstrip("!,"))
        if not x.startswith("R") and t < nb * beats:
            cnt[int(t // beats + 1e-6)] += 1; a[int(t * 2):min(len(a), int(np.ceil((t + L) * 2)))] = 1
        t += L
y, sr = sf.read(wf); m = y.mean(1) if y.ndim > 1 else y
def rms(t0, t1):
    i, j = max(0, int(t0 * sr)), max(1, int(t1 * sr)); return 20 * np.log10(max(1e-9, float(np.sqrt(np.mean(m[i:j] ** 2))))) if i < len(m) else -180
e = np.array([1.0 if rms(i * bar / 8, (i + 1) * bar / 8) > -38 else 0.0 for i in range(nb * 8)])
def miss(k):
    aa, ee = a[max(0, k):len(a) + min(0, k)], e[max(0, -k):len(e) - max(0, k)]; n = min(len(aa), len(ee)); return float(np.sum(np.abs(aa[:n] - ee[:n])) + np.sum(a[:k]) + np.sum(e[n:]))   # 切りすてた分に音符や音があれば、それも合わない数に入れる
k = min(range(0, min(len(a) - 8, 400)), key=miss); shift = k / 8                    # 頭の弾かない小節が長い時（ソロのギターなど）も合わせられるように、50小節まで見る
print(f"■ {key}: 音符 {sum(cnt)}個。書き出しのずれ {shift:g}小節（音が早い分をもどして合わせた。合わない8分 {int(miss(k))}/{int(a.sum())}）。全体 {rms(0, len(m) / sr):.1f}dB")
i = 0; bad = []; late = []
for s in (secs or [{"name": "全体", "bars": nb}]):
    n = s["bars"]; rows = [(j, rms((i + j - shift) * bar, (i + j + 1 - shift) * bar), rms((i + j - shift) * bar, (i + j + 0.25 - shift) * bar), cnt[i + j]) for j in range(n) if cnt[i + j] > 0]
    nm_ = s.get("name") or s.get("kind")
    if rows:
        print(f"  {nm_}: 音符のある小節 {len(rows)}/{n}  平均 {np.mean([r[1] for r in rows]):.1f}  最小 {min(r[1] for r in rows):.1f}  最大 {max(r[1] for r in rows):.1f}")
        bad += [(nm_, r[0] + 1, round(r[1]), r[3]) for r in rows if r[3] >= 4 and r[1] < -33]; late += [(nm_, r[0] + 1, round(r[2])) for r in rows if r[3] >= 4 and r[2] < -30 and r[1] >= -33]
    i += n
print("  音符が4つ以上あるのに小さい小節（-33dB 未満）:", bad or "なし"); print("  頭の1拍だけ小さい小節（-30dB 未満）:", late or "なし")
