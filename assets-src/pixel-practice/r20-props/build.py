"""全部の飾りを作り直し、確認画像 preview.png も作る。使い方: python3 build.py"""
import subprocess, sys, json, glob, os
for m in ("town.py", "town2.py", "dungeon.py", "dungeon2.py"):
    subprocess.run([sys.executable, m], check=True, stdout=subprocess.DEVNULL)
bad = 0
for t in sorted(glob.glob("*.txt")):
    n = t[:-4]
    rows = [r for r in open(t).read().split("\n") if r]
    pal = json.load(open(f"pal-{n}.json"))
    w = {len(r) for r in rows}
    chars = {c for r in rows for c in r} - {"."}
    ok = len(w) == 1 and chars <= set(pal) and len(pal) <= 16
    print(f"{n:16s} {max(w)}x{len(rows)} 色={len(pal)} {'OK' if ok else 'NG'}")
    bad += not ok
subprocess.run([sys.executable, "preview.py"], check=True)
sys.exit(bad)
