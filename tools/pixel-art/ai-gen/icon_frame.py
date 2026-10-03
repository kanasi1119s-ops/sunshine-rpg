"""顔アイコンの構図をそろえる（顔の大きさの統一、2026-10-04 人間の指示）。

決まり（512×512 のとき。128×128 は同じ構図を縮める）:
  - 顔の大きさ: √(目の高さ〜あご先 × 顔の幅) = 138px。顔の幅は、目の高さでの左右のほおの外側（髪はふくまない）。
    高さだけでそろえると、顔の細い大人の男性が小さく見えた（--width を省くと、目〜あご = 100px でそろえる）
  - 目の高さ: 上から 282px（画面の 55%）。左右は、両目の真ん中が画面の真ん中
  → 顔の大きさと位置が、どの人物でも同じになる。頭の上の余白は、髪型・帽子で変わる。
  元の絵に足りない所（首から下・横・頭の上）は、Stable Diffusion の inpainting（＋LCM）で描き足す。元の絵の部分は変えない。

使い方:
  python3 icon_frame.py 元の絵.png 出力.png --eyes 左目x,左目y,右目x,右目y --chin あごy --width 顔の幅 --desc "英語で人物の説明"
  （座標は元の絵のピクセル。目は黒目の中心、あごは先端）
  続けて: rembg（isnet-anime）で切り抜き → icon512.py 切り抜き.png 出力名 512 32（と 128 24）→ エディタで描く。
メモリ7GBほどの環境では、ブラウザ（エディタ）や rembg と同時に動かさない。1枚 約2.5分（CPU）。
"""
import argparse
import numpy as np
from PIL import Image, ImageFilter

FACE = 100 / 512      # 目〜あご ÷ 画面の高さ（--width がないとき）
SIZE = 138 / 512      # √(目〜あご × 顔の幅) ÷ 画面の高さ
EYE_Y = 282 / 512     # 目の高さ ÷ 画面の高さ
OUT = 1024            # 作業する大きさ（最後に 512・128 にする）

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--eyes", required=True); ap.add_argument("--chin", type=float, required=True)
ap.add_argument("--width", type=float, help="顔の幅（目の高さで、左右のほおの外側。元の絵のピクセル）")
ap.add_argument("--desc", required=True); ap.add_argument("--seed", type=int, default=7)
ap.add_argument("--no-ai", action="store_true", help="描き足さない（足りない所は透明のまま。確認用）")
a = ap.parse_args()
lx, ly, rx, ry = [float(v) for v in a.eyes.split(",")]
ex, ey = (lx + rx) / 2, (ly + ry) / 2
src = Image.open(a.src).convert("RGB")
s = (SIZE * OUT / ((a.chin - ey) * a.width) ** 0.5) if a.width else FACE * OUT / (a.chin - ey)   # 元の絵 → 作業画面 の倍率
sw, sh = round(src.size[0] * s), round(src.size[1] * s)
ox, oy = round(OUT / 2 - ex * s), round(EYE_Y * OUT - ey * s)
canvas = Image.new("RGB", (OUT, OUT), (128, 112, 120))
canvas.paste(src.resize((sw, sh), Image.LANCZOS), (ox, oy))
have = np.zeros((OUT, OUT), np.uint8)
x0, y0, x1, y1 = max(ox, 0), max(oy, 0), min(ox + sw, OUT), min(oy + sh, OUT)
have[y0 + 3:y1 - 3, x0 + 3:x1 - 3] = 255
print(f"倍率 {s:.3f}、元の絵が覆う範囲 x{x0}-{x1} y{y0}-{y1}")
if have.min() == 255 or a.no_ai:
    canvas.save(a.out); raise SystemExit
import torch
from diffusers import StableDiffusionInpaintPipeline, LCMScheduler
torch.set_num_threads(2)
pipe = StableDiffusionInpaintPipeline.from_pretrained("stable-diffusion-v1-5/stable-diffusion-inpainting", variant="fp16",
                                                      torch_dtype=torch.float16, safety_checker=None, requires_safety_checker=False)
pipe = pipe.to(torch.float32)
pipe.enable_attention_slicing(1); pipe.vae.enable_slicing(); pipe.vae.enable_tiling()
pipe.load_lora_weights("latent-consistency/lcm-lora-sdv1-5"); pipe.fuse_lora()
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
mask = Image.fromarray(255 - have).resize((512, 512)).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(2))
out = pipe(prompt=f"anime style chest-up portrait illustration of a {a.desc}, shoulders and upper body, clean lineart, cel shading, warm dusk town background",
           negative_prompt="cropped, frame, border, text, extra face, extra arms, blurry, deformed",
           image=canvas.resize((512, 512), Image.LANCZOS), mask_image=mask, num_inference_steps=8, guidance_scale=1.5,
           generator=torch.Generator().manual_seed(a.seed)).images[0]
keep = Image.fromarray(have).filter(ImageFilter.GaussianBlur(3))
Image.composite(canvas, out.resize((OUT, OUT), Image.LANCZOS), keep).save(a.out)
