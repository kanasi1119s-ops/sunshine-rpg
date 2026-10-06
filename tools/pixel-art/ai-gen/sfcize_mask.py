"""白い背景に白っぽい体（白いマント・白いドレス）の下絵を、AIの切り抜き（rembg）を使わずにドット絵化する（2026-10-06）。
rembg は白い布を背景といっしょに消してしまうことがある（無神・女神のマントが欠けた原因）。
先に、外側からつながった白い背景だけを消した切り抜き（透明つきPNG）を作っておき、それを sfcize.py にそのまま渡す。
使い方: python3 sfcize_mask.py 切り抜き.png 出力名 [大きさ] [色数]   （引数は sfcize.py と同じ）"""
import os, runpy, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pixelize
from PIL import Image
pixelize.remove_bg_ai = lambda im: Image.open(sys.argv[1]).convert("RGBA")
runpy.run_path(os.path.join(HERE, "sfcize.py"), run_name="__main__")
