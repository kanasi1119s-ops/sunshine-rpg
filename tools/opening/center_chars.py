# 元の立ち絵シートから、体と顔のまん中を rembg（背景の切り抜き）で測る
import json, numpy as np
from PIL import Image
from rembg import remove, new_session
names=["ユーリ","レト","ミナ","ガイド","オルカ","アヤメ"]
FACE=[(0.716,0.016,0.98,0.82),(0.04,0.016,0.275,0.82),(0.716,0.47,0.95,0.935),(0.716,0.006,0.99,0.855),(0.716,0.006,0.985,0.875),(0.716,0.006,0.98,0.875)]
L,R=0.28,0.705
ses=new_session("isnet-general-use")
out={}
for k,n in enumerate(names):
    sh=Image.open(f"chars/{n}.jpg").convert("RGB"); Wd,Ht=sh.size
    x0,x1=int(L*Wd),int(R*Wd)
    m=np.array(remove(sh.crop((x0,0,x1,Ht)),session=ses,only_mask=True))>128
    ys,xs=np.nonzero(m); top,bot=ys.min(),ys.max()
    # 体: 胴から脚（全体の高さの 25%〜90%）の列ごとの中央値の中央値
    band=(ys>top+0.25*(bot-top))&(ys<top+0.9*(bot-top))
    cx=[]
    for y in range(int(top+0.25*(bot-top)),int(top+0.9*(bot-top)),4):
        r=np.nonzero(m[y])[0]
        if len(r): cx.append((r.min()+r.max())/2)
    body=(x0+np.median(cx))/Wd
    # 頭: 上から 6%〜16% の行の左右のまん中
    hx=[]
    for y in range(int(top+0.02*(bot-top)),int(top+0.12*(bot-top)),2):
        r=np.nonzero(m[y])[0]
        if len(r): hx.append((r.min()+r.max())/2)
    head=(x0+np.median(hx))/Wd
    fb=FACE[k]; fc=sh.crop((int(fb[0]*Wd),int(fb[1]*Ht),int(fb[2]*Wd),int(fb[3]*Ht)))
    fm=np.array(remove(fc,session=ses,only_mask=True))>128
    fys,fxs=np.nonzero(fm); ft,fbm=fys.min(),fys.max()
    fx=[]
    for y in range(int(ft+0.05*(fbm-ft)),int(ft+0.35*(fbm-ft)),2):
        r=np.nonzero(fm[y])[0]
        if len(r): fx.append((r.min()+r.max())/2)
    face=(int(fb[0]*Wd)+np.median(fx))/Wd
    out[n]=dict(body=round(float(body),4),head=round(float(head),4),face=round(float(face),4))
    Image.fromarray((fm*255).astype(np.uint8)).save(f"stills4/fm_{k}.png"); Image.fromarray((m*255).astype(np.uint8)).save(f"stills4/bm_{k}.png")
    print(n,out[n],flush=True)
json.dump(out,open("char-centers.json","w"),ensure_ascii=False,indent=1)
