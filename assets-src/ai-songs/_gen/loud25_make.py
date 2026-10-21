# loud25.py の設計表から JSON を書き出す。使い方: python3 loud25_make.py <出力フォルダ> [番号...]
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from loud25 import SPECS
from loud25_arrange import build
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
want = set(int(x) for x in sys.argv[2:])
for sp in SPECS:
    if want and sp["no"] not in want: continue
    song, S = build(sp)
    p = os.path.join(out, f"loud25-{sp['no']:02d}-{sp['slug']}.json")
    json.dump(song, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sec = S.NB * S.beats * 60 / sp["bpm"]
    print(f"{p}  {S.NB}小節 {int(sec // 60)}分{int(sec % 60):02d}秒  パート{len(song['parts'])}")
