"""画像生成AIで「ドット絵風」の下絵を作る（試作、2026-10-03）。

使い方: MODEL=PublicPrompts/All-In-One-Pixel-Model python3 tools/pixel-art/ai-gen/generate.py 指示.json
  指示.json は [{"name":..., "seed":..., "steps":6, "cfg":1.5, "prompt":"...", "neg":"...", "w":512, "h":512}] の形（例: example-jobs.json）。
  種類ごとの雛形から作るときは make_jobs.py（prompts.json）を使う。
  出力は raw/<name>.png（512×512）。続けて pixelize.py で本物のドット絵に仕上げる。
モデル: PublicPrompts/All-In-One-Pixel-Model（CreativeML OpenRAIL-M）＋ latent-consistency/lcm-lora-sdv1-5（openrail++）。
CPU（2コア）で1枚約56秒。GPU があれば速い。必要なもの: torch（CPU版で可）、diffusers、transformers、accelerate、safetensors、peft。
絵画風の下絵（重厚な敵グラフィック用、2026-10-03 追加）:
  MODEL=stable-diffusion-v1-5/stable-diffusion-v1-5 VARIANT=fp16 STYLE=painterly python3 generate.py example-jobs-painterly.json
  （CreativeML OpenRAIL-M。続けて sfcize.py でドット絵にする。手順は docs/design/heavy-enemy-workflow.md）
**メモリ7GBほどの環境では、生成と同時に rembg やブラウザ（エディタ）を動かさない（メモリ不足で止まる）。**
**作った絵は、既存作品に似ていないかを必ず目で確かめる（CLAUDE.md 1-1）。ゲームに入れる前に人間の確認を受ける。**
"""
import torch,time,sys,json,os
from diffusers import StableDiffusionPipeline, LCMScheduler
torch.set_num_threads(2)
kw=dict(variant=os.environ["VARIANT"],torch_dtype=torch.float16) if os.environ.get("VARIANT") else dict(torch_dtype=torch.float32)
pipe=StableDiffusionPipeline.from_pretrained(os.environ.get("MODEL","PublicPrompts/All-In-One-Pixel-Model"),safety_checker=None,requires_safety_checker=False,**kw)
pipe=pipe.to(torch.float32)  # CPUでは float32 で計算する
pipe.enable_attention_slicing(1); pipe.vae.enable_slicing(); pipe.vae.enable_tiling()  # メモリを節約（縦長 512×768 でも止まらないように）
pipe.load_lora_weights("latent-consistency/lcm-lora-sdv1-5"); pipe.fuse_lora()
pipe.scheduler=LCMScheduler.from_config(pipe.scheduler.config)
NEG_PIXEL="drop shadow, blurry, 3d, anti aliasing, gradient, textures, depth of field, anime style, modern cartoon, skewed, perspective, text, watermark, photo, realistic"
NEG_PAINT="photo, 3d render, anime, cartoon, chibi, text, watermark, frame, border, multiple creatures, cropped, blurry"
NEG=os.environ.get("NEG") or (NEG_PAINT if os.environ.get("STYLE")=="painterly" else NEG_PIXEL)
jobs=json.load(open(sys.argv[1]))
os.makedirs('raw',exist_ok=True)
for j in jobs:
  t=time.time()
  g=torch.Generator().manual_seed(j['seed'])
  im=pipe(prompt=j['prompt'],negative_prompt=j.get('neg',NEG),num_inference_steps=j.get('steps',6),guidance_scale=j.get('cfg',1.5),width=j.get('w',512),height=j.get('h',512),generator=g).images[0]
  im.save(f"raw/{j['name']}.png"); print(j['name'],round(time.time()-t,1),flush=True)
