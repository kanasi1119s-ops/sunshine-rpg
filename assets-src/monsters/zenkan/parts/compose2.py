"""全観を組み立てる（2026-10-06、人間の指示「神々しさと禍々しさを足して、千手観音みたいな顔を真ん中に入れて、大量の手のひらだけ宙に浮くように」）
金の輪（前の全観） + まん中に目を閉じたおだやかな顔（下絵 zenkan_2 から） + 浮かぶ手のひら（金・黒金） + 顔のうしろの光と黒いもや + 顔のひび・黒い涙"""
import json, math, random
import numpy as np
from PIL import Image, ImageDraw
Z='/tmp/monster-work/zk/'
rows=[r for r in open(Z+'ring_final.txt').read().split('\n') if r]; P=json.load(open(Z+'ring_final.json'))
W=H=256; cx=cy=128
base=np.zeros((H,W,4),'uint8')
for y,r in enumerate(rows):
    for x,c in enumerate(r):
        if c!='.':
            d=math.hypot(x-cx,y-cy)
            if d<84: continue                      # 輪の内側の光の筋は描き直す
            base[y,x,:3]=[int(P[c][q:q+2],16) for q in (1,3,5)]; base[y,x,3]=255
img=Image.fromarray(base,'RGBA')
rnd=random.Random(7)
# 1) 顔のうしろ: 黒紫のもや（点々）と、金の光背（細い輪と光の筋）
lay=Image.new('RGBA',(W,H)); px=lay.load()
for y in range(H):
    for x in range(W):
        d=math.hypot(x-cx,y-cy)
        if d<80:
            t=d/80
            if (x+y)%2==0 and rnd.random()<0.85-0.6*t: px[x,y]=(40,14,46,255) if rnd.random()<0.7 else (70,20,60,255)
dl=ImageDraw.Draw(lay)
for k in range(24):                                   # 光の筋
    a=k*math.pi/12+0.13
    for r in range(56,82):
        if r%2==0 or r<64:
            x=int(round(cx+r*math.cos(a))); y=int(round(cy+r*math.sin(a)))
            px[x,y]=(255,232,150,255) if r<70 else (210,160,70,255)
dl.ellipse((cx-54,cy-54,cx+54,cy+54),outline=(240,200,90,255),width=2)   # 光背の輪
dl.ellipse((cx-57,cy-57,cx+57,cy+57),outline=(120,70,20,255),width=1)
img=Image.alpha_composite(img,lay)
# 2) 浮かぶ手のひら
pg=Image.open('/tmp/monster-work/zk2/hand_gold.png'); pd=Image.open('/tmp/monster-work/zk2/hand_dark.png')
def palm(src,size,ang):
    h=size; w=int(size*src.width/src.height)
    s=src.resize((w,h),Image.LANCZOS)
    s=s.rotate(ang,resample=Image.NEAREST,expand=True)
    a=np.asarray(s).copy(); a[:,:,3]=np.where(a[:,:,3]>110,255,0)
    a=np.pad(a,((1,1),(1,1),(0,0)))
    from scipy import ndimage as nd
    ring=nd.binary_dilation(a[:,:,3]>0)&(a[:,:,3]==0)
    a[ring]=(28,12,10,255)                     # 細い暗い縁で、金の輪から手を分ける
    return Image.fromarray(a,'RGBA')
def put(p,x,y):
    img.alpha_composite(p,(int(x-p.width/2),int(y-p.height/2)))
# 輪の上の手（大きめ、金と黒金をまぜる。少しずつずらして、宙に浮いているように）
for k in range(12):
    a=-math.pi/2+k*2*math.pi/12+rnd.uniform(-0.08,0.08)
    r=104+rnd.randint(-6,6); x=cx+r*math.cos(a); y=cy+r*math.sin(a)
    put(palm(pd if rnd.random()<0.4 else pg,36+rnd.randint(-3,4),-math.degrees(a)-90+rnd.randint(-20,20)),x,y)
# 内側の手（顔のまわり、2重に。指を外へ）
for ring_r,n,sz in ((70,10,26),):
    for k in range(n):
        a=-math.pi/2+(k+0.5*(ring_r==78))*2*math.pi/n+rnd.uniform(-0.06,0.06)
        x=cx+ring_r*math.cos(a); y=cy+ring_r*math.sin(a)
        put(palm(pd if rnd.random()<0.35 else pg,sz+rnd.randint(-2,2),-math.degrees(a)-90+rnd.randint(-12,12)),x,y)
# 輪に赤く光るひび（禍々しさ）
for k in range(7):
    a=rnd.uniform(0,2*math.pi); r=rnd.uniform(92,116); x,y=cx+r*math.cos(a),cy+r*math.sin(a)
    for _ in range(rnd.randint(10,18)):
        a+=rnd.uniform(-0.6,0.6); x+=math.cos(a+math.pi/2)*0.9; y+=math.sin(a+math.pi/2)*0.9
        xi,yi=int(x),int(y)
        if 0<=xi<W and 0<=yi<H and img.getpixel((xi,yi))[3] and 86<math.hypot(xi-cx,yi-cy)<122:
            img.putpixel((xi,yi),(60,6,10,255))
            if 0<xi+1<W and img.getpixel((xi+1,yi))[3]: img.putpixel((xi+1,yi),(200,40,30,255))
# 3) 顔
face=Image.open('/tmp/monster-work/zk2/face.png')
img.alpha_composite(face,(cx-face.width//2,cy-face.height//2+2))
# 4) 禍々しさ: 顔のひびと黒い涙
dr=ImageDraw.Draw(img)
fx0=cx-face.width//2; fy0=cy-face.height//2+2
def crack(x,y,n,dx):
    for _ in range(n):
        x+=dx+rnd.choice((-1,0,0,1)); y+=1
        if img.getpixel((x,y))[3]: dr.point((x,y),fill=(30,12,16,255))
crack(fx0+50,fy0+8,22,0.4); crack(fx0+22,fy0+30,16,-0.3); crack(fx0+60,fy0+60,14,0.2)
for ex in (fx0+24,fx0+56):                       # 閉じた目から黒い涙
    for t in range(14):
        y=fy0+54+t; x=ex+(1 if t>7 else 0)
        if img.getpixel((x,y))[3]: dr.point((x,y),fill=(24,8,14,255)); dr.point((x,y+1),fill=(90,20,30,255))
Z='/tmp/monster-work/zk2/'; img.save(Z+'zenkan_new.png')
# 5) 色を62色にまとめて、文字グリッドに
a=np.asarray(img); al=a[:,:,3]>0
q=Image.fromarray(a[:,:,:3]).quantize(60,method=Image.Quantize.MEDIANCUT)
pal=q.getpalette()[:60*3]; qi=np.asarray(q)
syms='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
used=sorted(set(qi[al].tolist()))
m={u:syms[n] for n,u in enumerate(used)}
out=[''.join(m[qi[y,x]] if al[y,x] else '.' for x in range(W)) for y in range(H)]
P2={m[u]:'#%02x%02x%02x'%tuple(pal[u*3:u*3+3]) for u in used}
open(Z+'zenkan_new.txt','w').write('\n'.join(out)+'\n'); json.dump(P2,open(Z+'zenkan_new.json','w'))
v=Image.new('RGBA',(W,H),(40,36,52,255)); v.alpha_composite(img); v.resize((512,512),Image.NEAREST).save(Z+'zenkan_view.png')
print(len(P2),'色')
