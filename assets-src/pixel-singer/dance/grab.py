from PIL import Image
import numpy as np, cv2
from collections import deque
im=Image.open('/mnt/user-data/uploads/b96b13b5-image.jpg').convert('RGB'); A=np.asarray(im).astype(float)
BOX=[(78,250),(321,465),(562,734),(804,947)]; Y0,Y1=44,512
hls=cv2.cvtColor(A.astype(np.uint8),cv2.COLOR_RGB2HLS).astype(float)
def sc1(c,ax,s,p):
    arr=c if ax==1 else c.transpose(1,0,2)
    n=arr.shape[1]; idx=np.floor((np.arange(n)-p)/s).astype(int); tot=0;cnt=0
    for k in np.unique(idx):
        blk=arr[:,idx==k]
        if blk.shape[1]>1: tot+=((blk-blk.mean(1,keepdims=True))**2).sum(); cnt+=blk.size
    return tot/cnt
for k,(x0,x1) in enumerate(BOX):
    c=A[Y0:Y1,x0:x1]; hc=hls[Y0:Y1,x0:x1]
    bgc0=np.median(c[:6].reshape(-1,3),axis=0)
    bgm=(np.abs(c-bgc0).sum(2)<70)
    halo=(hc[...,2]<0.2*255)&(hc[...,1]>0.42*255)            # 白っぽい灰色（にじみになりうる色）
    for _ in range(0):                                         # 背景から、にじみの色をたどって4ピクセルまで広げる
        grow=cv2.dilate(bgm.astype(np.uint8),np.ones((3,3),np.uint8)).astype(bool)
        bgm=bgm|(grow&halo)
    sx,px=min(((sc1(c,1,s,p),s,p) for s in np.arange(2.70,2.83,0.005) for p in np.arange(0,2.8,0.25)))[1:]
    sy,py=min(((sc1(c,0,s,p),s,p) for s in np.arange(2.74,2.84,0.005) for p in np.arange(0,2.8,0.25)))[1:]
    nx=int((c.shape[1]-px)/sx); ny=int((c.shape[0]-py)/sy); g=np.zeros((ny,nx,3)); fr=np.zeros((ny,nx))
    for j in range(ny):
        for i in range(nx):
            xa=px+i*sx; ya=py+j*sy
            ys,xs=slice(int(ya),max(int(ya)+1,int(np.ceil(ya+sy)))),slice(int(xa),max(int(xa)+1,int(np.ceil(xa+sx))))
            blk=c[ys,xs].reshape(-1,3); bb=bgm[ys,xs].reshape(-1)
            fr[j,i]=bb.mean()
            core=c[int(ya+0.6):max(int(ya+0.6)+1,int(ya+sy-0.6)), int(xa+0.6):max(int(xa+0.6)+1,int(xa+sx-0.6))].reshape(-1,3)
            cb=bgm[int(ya+0.6):max(int(ya+0.6)+1,int(ya+sy-0.6)), int(xa+0.6):max(int(xa+0.6)+1,int(xa+sx-0.6))].reshape(-1)
            src=core[~cb] if (~cb).any() else blk[~bb] if (~bb).any() else core
            g[j,i]=np.median(src,axis=0)
    white=fr>0.45
    bg=np.zeros(white.shape,bool); q=deque([(j,i) for j in range(ny) for i in (0,nx-1)]+[(j,i) for i in range(nx) for j in (0,ny-1)])
    while q:
        j,i=q.popleft()
        if 0<=j<ny and 0<=i<nx and white[j,i] and not bg[j,i]: bg[j,i]=True; q.extend([(j+1,i),(j-1,i),(j,i+1),(j,i-1)])
    print(k,"マス",round(sx,3),round(sy,3),"大きさ",nx,ny)
    np.save(f'g{k}.npy',g); np.save(f'b{k}.npy',bg)
