"""画像生成AIで「ドット絵風」の下絵を作る（試作、2026-10-03）。

使い方: MODEL=PublicPrompts/All-In-One-Pixel-Model python3 tools/pixel-art/ai-gen/generate.py 指示.json
  指示.json は [{"name":..., "seed":..., "steps":6, "cfg":1.5, "prompt":"..., in pixelsprite style, ..."}] の形（例: example-jobs.json）。
  出力は raw/<name>.png（512×512）。続けて pixelize.py で本物のドット絵に仕上げる。
モデル: PublicPrompts/All-In-One-Pixel-Model（CreativeML OpenRAIL-M）＋ latent-consistency/lcm-lora-sdv1-5（openrail++）。
CPU（2コア）で1枚約56秒。GPU があれば速い。必要なもの: torch（CPU版で可）、diffusers、transformers、accelerate、safetensors、peft。
**作った絵は、既存作品に似ていないかを必ず目で確かめる（CLAUDE.md 1-1）。ゲームに入れる前に人間の確認を受ける。**
"""
import torch,time,sys,json,os
from diffusers import StableDiffusionPipeline, LCMScheduler
torch.set_num_threads(2)
pipe=StableDiffusionPipeline.from_pretrained(os.environ.get("MODEL","PublicPrompts/All-In-One-Pixel-Model"),torch_dtype=torch.float32,safety_checker=None,requires_safety_checker=False)
pipe.load_lora_weights("latent-consistency/lcm-lora-sdv1-5"); pipe.fuse_lora()
pipe.scheduler=LCMScheduler.from_config(pipe.scheduler.config)
NEG="drop shadow, blurry, 3d, anti aliasing, gradient, textures, depth of field, anime style, modern cartoon, skewed, perspective, text, watermark, photo, realistic"
jobs=json.load(open(sys.argv[1]))
os.makedirs('raw',exist_ok=True)
for j in jobs:
  t=time.time()
  g=torch.Generator().manual_seed(j['seed'])
  im=pipe(prompt=j['prompt'],negative_prompt=NEG,num_inference_steps=j.get('steps',6),guidance_scale=j.get('cfg',1.5),width=512,height=512,generator=g).images[0]
  im.save(f"raw/{j['name']}.png"); print(j['name'],round(time.time()-t,1),flush=True)
