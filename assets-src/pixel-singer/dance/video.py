"""1000コマの作品から、見本の動画（24コマ/秒・4倍）と、等倍のシートを作る"""
import json, subprocess, sys
from PIL import Image
d = json.load(open(sys.argv[1])); OUT = sys.argv[2]; W, H = d['width'], d['height']
col = {s['sym']: tuple(int(s['color'][i:i + 2], 16) for i in (1, 3, 5)) for s in d['symbols']}
z = 4; BG = (236, 232, 222)
p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W * z}x{H * z}", "-r", "24", "-i", "-",
                      "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", OUT + ".tmp.mp4"], stdin=subprocess.PIPE)
for g in d['cels'][0]:
    im = Image.new('RGB', (W, H), BG)
    for y, r in enumerate(g):
        for x, ch in enumerate(r):
            if ch in col: im.putpixel((x, y), col[ch])
    p.stdin.write(im.resize((W * z, H * z), Image.NEAREST).tobytes())
p.stdin.close(); p.wait()
import os; os.replace(OUT + ".tmp.mp4", OUT); print("ok", OUT)
