"""顔のアイコン（512×512）の下ごしらえ: イメージ画像の「顔のアップ」の枠で頭が切れているとき、枠の外（頭の上・横）を描き足す（2026-10-04）。
人間の指示「アイコンは顔が切れないように」。元の絵の部分はそのまま残し、枠の外だけを Stable Diffusion の inpainting（＋LCM）で描く。
使い方: python3 icon_outpaint.py [名前...]  → src_<名前>.png（1024×1024）。下の C に、枠の内側と作りたい正方形（1000幅の座標）を書く。
続けて rembg（isnet-anime）で切り抜き → sfcize.py と同じ処理を正方形のまま 512 で（character.md の「顔のアイコン」）。
メモリ7GBほどの環境では、ブラウザ（エディタ）や rembg と同時に動かさない。1枚 約2.5分（CPU）。
"""
import torch, sys, gc, numpy as np
from PIL import Image, ImageFilter
from diffusers import StableDiffusionInpaintPipeline, LCMScheduler
torch.set_num_threads(2)
SRC='./'  # イメージ画像（<名前>.jpg）の置き場所
# 1000幅の座標: 枠の内側 (x0,y0,x1,y1) と、作りたい正方形 (x0,y0,一辺)
C={
 'レト':((37,2,277,453),(5,-50,300),'man with messy dark red hair, brown eyes, dark gray coat collar, red scarf'),
 'ユーリ':((713,2,998,463),(660,-50,290),'boy with spiky orange red hair, orange headband, green eyes, orange scarf'),
 'コハク':((713,2,998,463),(690,-45,300),'girl with golden brown ponytail hair, brown goggles on head, green eyes, green scarf'),
 'オルカ':((713,2,962,463),(670,-45,300),'tanned man with dark brown hair, brown miner helmet with lamp, gray shirt, orange vest'),
 'アヤメ':((713,8,968,463),(655,-30,290),'woman with long wavy lavender hair, silver circlet, violet eyes, purple robe'),
 'ミナ':((713,278,953,508),(705,215,250),'girl with long light blue hair, blue and white ribbon, braid, blue eyes, white dress'),
}
pipe=StableDiffusionInpaintPipeline.from_pretrained('stable-diffusion-v1-5/stable-diffusion-inpainting',variant='fp16',torch_dtype=torch.float16,safety_checker=None,requires_safety_checker=False)
pipe=pipe.to(torch.float32)
pipe.enable_attention_slicing(1); pipe.vae.enable_slicing(); pipe.vae.enable_tiling()
pipe.load_lora_weights('latent-consistency/lcm-lora-sdv1-5'); pipe.fuse_lora()
pipe.scheduler=LCMScheduler.from_config(pipe.scheduler.config)
names=sys.argv[1:] or list(C)
for n in names:
    (ix0,iy0,ix1,iy1),(sx,sy,side),desc=C[n]
    im=Image.open(SRC+n+'.jpg').convert('RGB'); k=im.size[0]/1000
    box=[round(v*k) for v in (sx,sy,sx+side,sy+side)]
    canvas=Image.new('RGB',(box[2]-box[0],box[3]-box[1]),(128,110,120))
    ins=im.crop([round(v*k) for v in (ix0,iy0,ix1,iy1)])
    canvas.paste(ins,(round((ix0-sx)*k),round((iy0-sy)*k)))
    S=canvas.size[0]; c512=canvas.resize((512,512),Image.LANCZOS)
    m=np.ones((512,512),np.uint8)*255
    f=512/S; a=[round((ix0-sx)*k*f)+3,round((iy0-sy)*k*f)+3,round((ix1-sx)*k*f)-3,round((iy1-sy)*k*f)-3]
    m[max(a[1],0):a[3],max(a[0],0):a[2]]=0
    mask=Image.fromarray(m).filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(2))
    g=torch.Generator().manual_seed(7)
    out=pipe(prompt=f'anime style portrait illustration of a {desc}, full head visible, detailed hair, warm dusk town street background, clean lineart, cel shading',
             negative_prompt='cropped head, frame, border, text, extra face, blurry, deformed',
             image=c512,mask_image=mask,num_inference_steps=8,guidance_scale=1.5,generator=g).images[0]
    # 元の部分はそのまま残す
    keep=Image.fromarray(255-np.array(mask)); res=Image.composite(c512,out,keep)
    # 高い解像度の元を優先して大きく保存
    big=res.resize((1024,1024),Image.LANCZOS); cb=canvas.resize((1024,1024),Image.LANCZOS)
    big=Image.composite(cb,big,keep.resize((1024,1024)))
    big.save(f'src_{n}.png'); print(n,'ok',S)
    del out; gc.collect()
