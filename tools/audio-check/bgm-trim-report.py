#!/usr/bin/env python3
"""ゲーム用の「曲ごとの音量補正」の計算表（docs/sound/mastering-guide.md 提案 11-①）。
docs/sound/bgm-loudness.json（曲ごとの I・TP）の数字から、-16 LUFS を軸にした補正量(dB)を計算して表にする。ファイルは書き換えない
（ゲームが使う表 src/audio/bgm-trim.ts は make-bgm-trim.py が作る。軸が -15 のまま）。

使い方:
    python3 tools/audio-check/bgm-trim-report.py [--target -16] [--json 出力.json] [--bgm-loudness 入力.json]
計算:
    補正 = 目標 − その曲の I。ただし上げるときは True Peak が -1dBTP を超えない範囲まで（TP の余裕ぶんだけ）。±12dB で切る。
    場面ごとの補正: 戦闘・ボスは +1.5、ダンジョン・静かな曲は -2（SCENE_OFFSET。曲名に battle / boss / dungeon / cave が入っていれば）。
    警告: 補正前の差が 3dB を超える曲（書き出しをやり直す目安）／TP の余裕で上げきれない曲／±12 で切られた曲。
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCENE_OFFSET = [("battle", 1.5), ("boss", 1.5), ("dungeon", -2.0), ("cave", -2.0)]


def scene_offset(name):
    for key, off in SCENE_OFFSET:
        if key in name:
            return off
    return 0.0


def compute(data, target=-16.0, max_db=12.0, ceiling=-1.0):
    rows = []
    for name in sorted(data):
        v = data[name]
        want = target + scene_offset(name) - v["I"]
        gain, limited = want, None
        if gain > ceiling - v["TP"]:
            gain, limited = ceiling - v["TP"], "tp"
        if abs(gain) > max_db:
            gain, limited = max(-max_db, min(max_db, gain)), "max"
        rows.append({"name": name, "I": v["I"], "TP": v["TP"], "want": round(want, 1), "gain": round(gain, 1), "limited": limited, "far": abs(want) > 3.0})
    return rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", type=float, default=-16.0)
    ap.add_argument("--json")
    ap.add_argument("--bgm-loudness", default=os.path.join(HERE, "../../docs/sound/bgm-loudness.json"))
    a = ap.parse_args()
    rows = compute(json.load(open(a.bgm_loudness, encoding="utf-8")), a.target)
    far = [r for r in rows if r["far"]]
    lim = [r for r in rows if r["limited"]]
    print(f"{len(rows)}曲（目標 {a.target} LUFS）: 補正の範囲 {min(r['gain'] for r in rows)}〜{max(r['gain'] for r in rows)}dB、差が 3dB を超える曲 {len(far)}、上限で止まる曲 {len(lim)}")
    for r in rows:
        mark = "△" if r["far"] or r["limited"] else "○"
        note = {"tp": "（TP の余裕で上げきれない）", "max": "（±12 で切った）", None: ""}[r["limited"]]
        print(f"{mark} {r['name']:28s} I {r['I']:6.1f}  TP {r['TP']:5.1f}  補正 {r['gain']:+5.1f}dB（欲しい量 {r['want']:+5.1f}）{note}")
    if a.json:
        json.dump({r["name"]: r["gain"] for r in rows}, open(a.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
