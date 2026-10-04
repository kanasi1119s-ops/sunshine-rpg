"""横長の見本の動画を、インスタグラムのリール（縦 9:16、1080×1920）に作りかえる（2026-10-04、人間の指示「この4つの動画すべてインスタに投稿できるようにして」）。

使い方: python3 insta_reel.py 入力.mp4 出力.mp4 --title "大きな見出し" --sub "小さな見出し" [--bg 背景の絵] [--audio 音.wav|mp3]
- 画面: 背景の絵（9:16に切ってドット絵にし、暗くする）の上に、見本の動画を横いっぱい（1080）で、まん中に置く。
  文字は、インスタの上下の飾り（名前・ボタン）にかぶらない所（上から260〜、下は1670まで）に置く。
- 映像: H.264・30コマ/秒・yuv420p（どの端末でも再生できる形）。音: AAC 48kHz ステレオ・192kbps、大きさを -14 LUFS にそろえる。
- 長さはリールの目安（3分）に収める（入力が長いときは、そのまま。切るのは呼ぶ側で）。
"""
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
W, H = 1080, 1920


def opt(a, k, d=None):
    return a[a.index(k) + 1] if k in a else d


def outlined(d, xy, text, font, fill, stroke=(16, 10, 30), sw=6, anchor="mm"):
    d.text(xy, text, font=font, fill=fill, stroke_width=sw, stroke_fill=stroke, anchor=anchor)


def make_card(bg_path, title, sub, foot1, foot2, vid_h, path):
    im = Image.open(bg_path).convert("RGB")
    # 9:16 に切って、180×320 のドット絵にしてから6倍（ドット絵の見た目）
    tw = round(im.height * 9 / 16)
    x0 = max(0, (im.width - tw) // 2)
    im = im.crop((x0, 0, x0 + tw, im.height)).resize((180, 320), Image.LANCZOS)
    im = im.quantize(48, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB").resize((W, H), Image.NEAREST)
    dark = Image.new("RGB", (W, H), (10, 6, 22))
    im = Image.blend(im, dark, 0.55)
    d = ImageDraw.Draw(im, "RGBA")
    vy = (H - vid_h) // 2
    # 動画のまわりに細い金の枠
    d.rectangle((0, vy - 6, W, vy + vid_h + 5), fill=(242, 193, 78, 255))
    f1 = ImageFont.truetype(FONT, 92); f2 = ImageFont.truetype(FONT, 46)
    f3 = ImageFont.truetype(FONT, 50); f4 = ImageFont.truetype(FONT, 34)
    sz = 92
    while sz > 40 and d.textlength(title, font=ImageFont.truetype(FONT, sz)) > W - 100:   # 横からはみ出さない大きさに
        sz -= 4
    f1 = ImageFont.truetype(FONT, sz)
    outlined(d, (W // 2, vy - 230), title, f1, (242, 193, 78))
    outlined(d, (W // 2, vy - 110), sub, f2, (240, 236, 250), sw=5)
    outlined(d, (W // 2, vy + vid_h + 110), foot1, f3, (240, 236, 250), sw=5)
    outlined(d, (W // 2, vy + vid_h + 185), foot2, f4, (200, 190, 230), sw=4)
    im.save(path)
    return vy


def main():
    a = sys.argv[1:]
    src, out = a[0], a[1]
    title, sub = opt(a, "--title", ""), opt(a, "--sub", "")
    foot1 = opt(a, "--foot1", "サンシャインRPG（仮題）制作中")
    foot2 = opt(a, "--foot2", "ドット絵・動き・エフェクト・効果音を一から作っています")
    bg = opt(a, "--bg", os.path.join(os.path.dirname(__file__), "..", "..", "assets-src", "backgrounds", "star-shrine", "original.jpg"))
    audio = opt(a, "--audio")
    sw, sh = map(int, subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", src],
                                     capture_output=True, text=True).stdout.strip().split(","))
    vh = round(W * sh / sw / 2) * 2
    tmp = tempfile.mkdtemp()
    card = os.path.join(tmp, "card.png")
    vy = make_card(bg, title, sub, foot1, foot2, vh, card)
    ain = ["-i", audio] if audio else []
    amap = "2:a" if audio else "1:a"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", card, "-i", src] + ain + [
        "-filter_complex",
        f"[1:v]scale={W}:{vh}:flags=lanczos,fps=30[v];[0:v][v]overlay=0:{vy}:shortest=1,format=yuv420p[o];"
        f"[{amap}]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[au]",
        "-map", "[o]", "-map", "[au]", "-c:v", "libx264", "-profile:v", "high", "-level", "4.1", "-preset", "slow", "-crf", "19",
        "-maxrate", "12M", "-bufsize", "24M", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-movflags", "+faststart", "-shortest", out]
    subprocess.run(cmd, check=True)
    print("リール:", out)


if __name__ == "__main__":
    main()
