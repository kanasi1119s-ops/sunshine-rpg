# 句ごとの音の数と歌詞の拍の数を並べる: python3 lc.py <台本> <行の変数式> <歌詞の変数式>
import sys, os
sys.path.insert(0, os.getcwd())
from vb25_lib import phrase_counts, morae
src = open(sys.argv[1]).read()
ns = {}
code = src.split("LY = Lyrics(S)")[0]
code = code[code.index("# ================= 歌"):]
exec("from vb25_lib import *\n" + code, ns)
for spec in sys.argv[2:]:
    lines_expr, text_expr = spec.split("|")
    lines = eval(lines_expr, ns); text = eval(text_expr, ns)
    pc = phrase_counts(lines); tc = [len(morae(t)) for t in text.split("/")]
    print(spec, "音", pc, "詞", tc, "OK" if pc == tc else "×")
