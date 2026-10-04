"""boss_rig.py の動き（anim.json）を、決めたコマの長さどおりに再生する動画（MP4）にする（2026-10-04）。
エディタの中の再生は、コマが多いと描き直しが追いつかず遅くなるため、なめらかさを正しく見せるのに使う。
使い方: python3 anim_clip.py anim.json 出力.mp4 [--size 1280x800] [--title 名前] [--bg 背景.png]
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


BG = None
if "--bg" in a:   # 背景のドット絵（人間の指示「ボスの攻撃動画の背景をこのドット画に変えよう」）。最近傍で画面いっぱいに広げる
    _b = Image.open(opt("--bg", "")).convert("RGB")
    _k = max(VW / _b.width, VH / _b.height)
    _b = _b.resize((round(_b.width * _k), round(_b.height * _k)), Image.NEAREST)
    BG = _b.crop(((_b.width - VW) // 2, (_b.height - VH) // 2, (_b.width - VW) // 2 + VW, (_b.height - VH) // 2 + VH))


def card(rows, caption):
    bg = BG.copy() if BG is not None else Image.new("RGB", (VW, VH), (28, 22, 44))
    d = ImageDraw.Draw(bg, "RGBA")
    # 床（足もと）と、キャプション
    s = max(1, (VH - 140) // 256)
    sp = img(rows, s)
    x0, y0 = (VW - sp.width) // 2, VH - 40 - sp.height
    if BG is None:
        d.rectangle((0, y0 + sp.height - 6, VW, VH), fill=(22, 17, 34))
    else:   # 足もとの影
        d.ellipse((x0 + sp.width * 0.18, y0 + sp.height - 14, x0 + sp.width * 0.82, y0 + sp.height + 10), fill=(0, 0, 0, 90))
    bg.paste(sp, (x0, y0), sp)
    f = ImageFont.truetype(FONT, 30)
    text = (title + "　" if title else "") + caption
    if BG is not None:   # 背景が明るい所でも読めるように、文字の下に暗い帯
        w = d.textlength(text, font=f)
        d.rounded_rectangle((26, 22, 54 + w, 70), 10, fill=(14, 10, 26, 200))
    d.text((40, 30), text, font=f, fill=(242, 193, 78))
    return bg


tmp = tempfile.mkdtemp()
seq = []   # (画像のパス, 秒)
cache = {}
timeline = []   # 効果音を合わせるための「いつ・どの動きの・何コマ目」（出力.timeline.json）
def add(kind, i, ms, caption, pause=False):
    timeline.append({"t": round(sum(x for _, x in seq), 3), "kind": kind, "i": i, "pause": pause})
    key = (kind, i, caption)
    if key not in cache:
        p = os.path.join(tmp, f"{len(cache):04d}.png"); card(A[kind][i], caption).save(p); cache[key] = p
    seq.append((cache[key], ms / 1000))
def run(kind, ms_key, loops, caption, pause=0):
    for _ in range(loops):
        for i, ms in enumerate(A[ms_key]): add(kind, i, ms, caption)
        if pause: add(kind, len(A[ms_key]) - 1, pause, caption, True)

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
json.dump(timeline, open(os.path.splitext(out)[0] + ".timeline.json", "w"))
print("動画:", out, f"{sum(s for _, s in seq):.1f}秒", len(cache), "枚")
