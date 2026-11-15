#!/usr/bin/env python3
"""段2の数字を、取っておいた書き起こし（raw）から計算し直す。物差し（stage2.py の stats）を直したあと、音を取り直さずにカルテを新しくするためのもの。
使い方: python3 tools/song-analyzer/restat.py <カルテのフォルダ> <raw のフォルダ>
  raw は、SA_RAW=<フォルダ> を付けて analyze.py や collect_ia.py を走らせるとできる。1曲ぶんの書き起こしが入っているので、リポジトリには入れず、使い終わったら消す。"""
import sys, os, json, glob, pickle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stage2
kd, rd = sys.argv[1], sys.argv[2]
for f in sorted(glob.glob(os.path.join(kd, "*.karte.json"))):
    n = os.path.basename(f)[:-len(".karte.json")]; rp = os.path.join(rd, n + ".raw.pkl")
    if not os.path.exists(rp): print("× raw がない:", n); continue
    k = json.load(open(f)); k["stage2"] = stage2.stats(pickle.load(open(rp, "rb"))["raw"]); json.dump(k, open(f, "w"), ensure_ascii=False); print("○", n)
