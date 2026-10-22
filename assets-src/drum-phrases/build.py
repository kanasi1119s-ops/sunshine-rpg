# phrases.json.gz（GMD の8小節＋自作のラウド向け8小節）と fills.json.gz（GMD の短いフィル）を作り直す（2026-10-22）
# 使い方: python3 -I build.py <GMD の groove フォルダ>
#   GMD: https://storage.googleapis.com/magentadata/datasets/groove/groove-v1.0.0-midionly.zip（3.3MB。CC BY 4.0）
import json, os, sys, subprocess, tempfile, gzip
here = os.path.dirname(os.path.abspath(__file__))
tmp = tempfile.mkdtemp()
subprocess.run([sys.executable, "-I", os.path.join(here, "extract_gmd.py"), sys.argv[1], tmp], check=True)
subprocess.run([sys.executable, "-I", os.path.join(here, "make_loud.py"), os.path.join(tmp, "loud.json")], check=True)
G = json.load(open(os.path.join(tmp, "gmd_phrases.tmp.json"))); L = json.load(open(os.path.join(tmp, "loud.json")))
F = json.load(open(os.path.join(tmp, "gmd_fills.tmp.json")))
def dump(path, arr):
    with gzip.open(path, "wt", compresslevel=9) as f:   # 3.7MB → 0.33MB
        f.write("[\n" + ",\n".join(json.dumps(x, ensure_ascii=False, separators=(",", ":")) for x in arr) + "\n]\n")
dump(os.path.join(here, "phrases.json.gz"), G + L)
dump(os.path.join(here, "fills.json.gz"), F)
print("phrases.json", len(G) + len(L), "(GMD", len(G), "/ 自作", len(L), ")  fills.json", len(F))
