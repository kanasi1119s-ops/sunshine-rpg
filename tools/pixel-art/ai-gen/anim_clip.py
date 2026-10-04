"""boss_rig.py の動き（anim.json）を、決めたコマの長さどおりに再生する動画（MP4）にする（2026-10-04）。
エディタの中の再生は、コマが多いと描き直しが追いつかず遅くなるため、なめらかさを正しく見せるのに使う。
使い方: python3 anim_clip.py anim.json 出力.mp4 [--size 1280x800] [--title 名前]
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

a = sys.argv[1:]
A = json.load(open(a[0])); out = a[1]
opt = lambda k, d: a[a.index(k) + 1] if k in a else d
VW, VH = map(int, opt("--size", "1280x800").split("x")); title = opt("--title", "")
pal = A["palette"]
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"


def img(rows, scale):
    im = Image.new("RGBA", (256, 256), (0, 0, 0, 0)); px = im.load()
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch != ".":
                v = pal[ch]; px[x, y] = (int(v[1:3], 16), int(v[3:5], 16), int(v[5:7], 16), 255)
    return im.resize((256 * scale, 256 * scale), Image.NEAREST)


def card(rows, caption):
    bg = Image.new("RGB", (VW, VH), (28, 22, 44))
    d = ImageDraw.Draw(bg)
    # 床（足もと）と、キャプション
    s = max(1, (VH - 140) // 256)
    sp = img(rows, s)
    x0, y0 = (VW - sp.width) // 2, VH - 40 - sp.height
    d.rectangle((0, y0 + sp.height - 6, VW, VH), fill=(22, 17, 34))
    bg.paste(sp, (x0, y0), sp)
    f = ImageFont.truetype(FONT, 30)
    d.text((40, 30), (title + "　" if title else "") + caption, font=f, fill=(242, 193, 78))
    return bg


tmp = tempfile.mkdtemp()
seq = []   # (画像のパス, 秒)
cache = {}
def add(kind, i, ms, caption):
    key = (kind, i, caption)
    if key not in cache:
        p = os.path.join(tmp, f"{len(cache):04d}.png"); card(A[kind][i], caption).save(p); cache[key] = p
    seq.append((cache[key], ms / 1000))
def run(kind, ms_key, loops, caption, pause=0):
    for _ in range(loops):
        for i, ms in enumerate(A[ms_key]): add(kind, i, ms, caption)
        if pause: add(kind, len(A[ms_key]) - 1, pause, caption)

run("flat_walk", "walk_ms", 4, f"歩く（{len(A['walk_ms'])}コマ）")
run("flat_attack", "attack_ms", 3, f"攻撃・腕だけ（{len(A['attack_ms'])}コマ）", 500)
if "flat_attack2" in A:
    run("flat_attack2", "attack2_ms", 3, f"攻撃・体ごと（{len(A['attack2_ms'])}コマ）", 500)
if A.get("flat_attack3"):
    run("flat_attack3", "attack3_ms", 3, f"攻撃・両手（{len(A['attack3_ms'])}コマ）", 500)
for _ in range(2):
    run("flat_walk", "walk_ms", 2, "歩いてから攻撃")
    run("flat_attack2" if "flat_attack2" in A else "flat_attack", "attack2_ms" if "flat_attack2" in A else "attack_ms", 1, "歩いてから攻撃", 400)
    if A.get("flat_attack3"):
        run("flat_walk", "walk_ms", 1, "歩いてから攻撃")
        run("flat_attack3", "attack3_ms", 1, "歩いてから攻撃", 400)
lst = os.path.join(tmp, "list.txt")
with open(lst, "w") as fh:
    for p, sec in seq: fh.write(f"file '{p}'\nduration {sec:.3f}\n")
    fh.write(f"file '{seq[-1][0]}'\n")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-vf", "fps=60,format=yuv420p",
                "-c:v", "libx264", "-crf", "20", out], check=True)
print("動画:", out, f"{sum(s for _, s in seq):.1f}秒", len(cache), "枚")
