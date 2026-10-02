#!/usr/bin/env python3
"""ゲームBGMの「曲ごとの音量補正」の表（src/audio/bgm-trim.ts）を、測定結果から作る。

使い方:
    node tools/composer/build.mjs                                   # 作曲ソフトの再ビルド
    node tools/audio-check/render-catalog.mjs --raw /tmp/catraw     # ピークをそろえず全曲を書き出す
    python3 tools/audio-check/analyze.py /tmp/catraw/*.wav > /tmp/catraw.json
    python3 tools/audio-check/make-bgm-trim.py /tmp/catraw.json

補正量 = 目標ラウドネス（-15 LUFS）− その曲の統合ラウドネス。ただし
- 上げるときは、True Peak が -1dBTP を超えない範囲まで（TP の余裕ぶんだけ）
- 補正は ±12dB まで
曲を作り直したり足したりしたら、同じ手順で作り直す。
"""
import json
import sys

TARGET_LUFS = -15.0
MAX_DB = 12.0
CEILING_TP = -1.0

data = json.load(open(sys.argv[1], encoding="utf-8"))
rows = {}
for name, v in data.items():
    song = name[:-4] if name.endswith(".wav") else name
    gain = TARGET_LUFS - v["I"]
    gain = min(gain, CEILING_TP - v["TP"])  # 上げすぎてピークが天井を超えないように
    gain = max(-MAX_DB, min(MAX_DB, gain))
    rows[song] = round(gain, 1)

lines = [
    "// 曲ごとの音量補正（dB）。`tools/audio-check/make-bgm-trim.py` が測定結果から作る（手で書き換えない）。",
    f"// 目標 {TARGET_LUFS} LUFS、補正は ±{MAX_DB:g}dB まで、上げるときは True Peak が {CEILING_TP}dBTP を超えない範囲まで。",
    "// 曲どうしの音量差（測定で最大 約22dB）を縮めて、場面が変わるたびの音量の飛びをなくす。",
    "export const BGM_TRIM_DB: Record<string, number> = {",
]
for k in sorted(rows):
    lines.append(f'  "{k}": {rows[k]},')
lines.append("};")
open("src/audio/bgm-trim.ts", "w", encoding="utf-8").write("\n".join(lines) + "\n")
print(f"{len(rows)}曲の補正表を src/audio/bgm-trim.ts に書きました（最小 {min(rows.values())}dB、最大 {max(rows.values())}dB）")
