#!/usr/bin/env python3
"""ゲームBGMの「曲ごとの音量補正」の表（src/audio/bgm-trim.ts）を、測定結果から作る。

使い方:
    node tools/composer/build.mjs                                   # 作曲ソフトの再ビルド
    node tools/audio-check/render-catalog.mjs --raw /tmp/catraw     # ピークをそろえず全曲を書き出す
    python3 tools/audio-check/analyze.py /tmp/catraw/*.wav > /tmp/catraw.json
    python3 tools/audio-check/make-bgm-trim.py /tmp/catraw.json            # 1回目: 入口の補正（pre）を決める
    # bgm-trim.ts を更新したら、もう一度 render-catalog --raw（pre 込みで書き出される）→ analyze → 次を実行:
    python3 tools/audio-check/make-bgm-trim.py /tmp/catraw.json /tmp/catraw-pre.json   # 出口の補正（trim）を決める

補正量 = 目標ラウドネス（-15 LUFS）− その曲の統合ラウドネス。ただし
- 上げるときは、True Peak が -1dBTP を超えない範囲まで（TP の余裕ぶんだけ）
- 補正は ±12dB まで
入口の補正（pre）: 目標より大きい曲は、必要な下げ幅の全部 を出口のリミッターの手前で下げる
（リミッターで頭を押さえつけるより、手前で小さくするほうがつぶれにくい）。残りは出口の補正（trim）で合わせる。
曲を作り直したり足したりしたら、同じ手順で作り直す。
"""
import json
import sys

TARGET_LUFS = -15.0
MAX_DB = 12.0
CEILING_TP = -1.0

PRE_RATIO = 1.0
base = json.load(open(sys.argv[1], encoding="utf-8"))
after = json.load(open(sys.argv[2], encoding="utf-8")) if len(sys.argv) > 2 else None
name_of = lambda n: n[:-4] if n.endswith(".wav") else n
pre = {}
for name, v in base.items():
    need = TARGET_LUFS - v["I"]
    pre[name_of(name)] = round(max(-MAX_DB, min(0.0, need * PRE_RATIO)), 1)
rows = {}
for name, v in (after or base).items():
    song = name_of(name)
    gain = TARGET_LUFS - v["I"]
    gain = min(gain, CEILING_TP - v["TP"])  # 上げすぎてピークが天井を超えないように
    gain = max(-MAX_DB, min(MAX_DB, gain))
    rows[song] = round(gain, 1)
if after is None:  # 1回目: pre を掛けたあとの出口の補正はまだ分からないので、残りの下げ幅だけ入れる
    rows = {k: round(max(-MAX_DB, min(MAX_DB, TARGET_LUFS - base[k + ".wav" if k + ".wav" in base else k]["I"] - pre[k])), 1) for k in rows}

lines = [
    "// 曲ごとの音量補正（dB）。`tools/audio-check/make-bgm-trim.py` が測定結果から作る（手で書き換えない）。",
    f"// 目標 {TARGET_LUFS} LUFS、補正は ±{MAX_DB:g}dB まで、上げるときは True Peak が {CEILING_TP}dBTP を超えない範囲まで。",
    "// 曲どうしの音量差（測定で最大 約22dB）を縮めて、場面が変わるたびの音量の飛びをなくす。",
    "// BGM_PRE_DB: 入口（リミッターの手前）の補正。BGM_TRIM_DB: 出口の補正。",
    "export const BGM_PRE_DB: Record<string, number> = {",
]
for k in sorted(pre):
    lines.append(f'  "{k}": {pre[k]},')
lines += ["};", "export const BGM_TRIM_DB: Record<string, number> = {"]
for k in sorted(rows):
    lines.append(f'  "{k}": {rows[k]},')
lines.append("};")
open("src/audio/bgm-trim.ts", "w", encoding="utf-8").write("\n".join(lines) + "\n")
print(f"{len(rows)}曲の補正表を src/audio/bgm-trim.ts に書きました（pre 最小 {min(pre.values())}dB、trim 最小 {min(rows.values())}dB／最大 {max(rows.values())}dB）")
