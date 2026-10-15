# 体のまん中（見た目の軸）= 頭のまん中 0.4・胴の質量 0.3・足もとの左右のまん中 0.3
import json, numpy as np
from PIL import Image
from scipy import ndimage as ndi
names=["ユーリ","レト","ミナ","ガイド","オルカ","アヤメ"]
cc=json.load(open("char-centers.json",encoding="utf-8"))
for k,n in enumerate(names):
    Wd=Image.open(f"chars/{n}.jpg").size[0]; x0=int(0.28*Wd)
    m=np.array(Image.open(f"stills4/bm_{k}.png"))>128
    r=max(2,int(0.012*m.shape[0])); m=ndi.binary_opening(m,structure=np.ones((r,r)))
    lab,nl=ndi.label(m); sizes=ndi.sum(m,lab,range(1,nl+1)); m=lab==(np.argmax(sizes)+1)
    ys,xs=np.nonzero(m); top,bot=ys.min(),ys.max(); h=bot-top
    def band(a,b): s=(ys>=top+a*h)&(ys<=top+b*h); return xs[s]
    head=np.median(band(0.03,0.13)); torso=np.median(band(0.15,0.5)); f=band(0.93,1.0); feet=(f.min()+f.max())/2
    c=(x0+0.4*head+0.3*torso+0.3*feet)/Wd
    print(n, "head",round((x0+head)/Wd,4),"torso",round((x0+torso)/Wd,4),"feet",round((x0+feet)/Wd,4),"->",round(c,4))
    cc[n]["body"]=round(float(c),4)
json.dump(cc,open("char-centers.json","w"),ensure_ascii=False,indent=1)
