import numpy as np, json, cv2
from sklearn.cluster import KMeans
from PIL import Image
G=[np.load(f'g{k}.npy') for k in range(4)]; B=[np.load(f'b{k}.npy').copy() for k in range(4)]
def light_gray(p): return p.min()>185 and p.max()-p.min()<40
for g,b in zip(G,B):                        # まわりの白いにじみ（白っぽい灰色のふち）を外から何回かけずる
    H,W=b.shape
    for _ in range(0):
        kill=[(y,x) for y in range(H) for x in range(W) if not b[y,x] and light_gray(g[y,x]) and any((not(0<=y+dy<H and 0<=x+dx<W)) or b[y+dy,x+dx] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))]
        for y,x in kill: b[y,x]=True
    # 1マスだけ飛び出した点を消す
    for y in range(H):
        for x in range(W):
            if not b[y,x] and sum(1 for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+dy<H and 0<=x+dx<W and not b[y+dy,x+dx])<=1: b[y,x]=True
# 同じ大きさのキャンバスに並べる: 足もとをそろえ、横は真ん中に
CW,CH=64,168; canv=[]
for g,b in zip(G,B):
    ys,xs=np.where(~b); y0,y1,x0,x1=ys.min(),ys.max(),xs.min(),xs.max()
    ox=(CW-(x1-x0+1))//2-x0; oy=CH-2-y1
    cg=np.zeros((CH,CW,3)); cb=np.ones((CH,CW),bool)
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            if not b[y,x]: cg[y+oy,x+ox]=g[y,x]; cb[y+oy,x+ox]=False
    canv.append((cg,cb))
allpx=np.concatenate([cg[~cb] for cg,cb in canv])
lab=cv2.cvtColor(allpx.astype(np.uint8).reshape(-1,1,3),cv2.COLOR_RGB2LAB).reshape(-1,3).astype(float)
K=56; km=KMeans(K,n_init=6,random_state=2).fit(lab)
cen=np.array([allpx[km.labels_==k].mean(0) for k in range(K)]).round().astype(int)
order=np.argsort([c.sum() for c in cen]); rank={int(o):i for i,o in enumerate(order)}
syms="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
pal={syms[rank[k]]:"#%02x%02x%02x"%tuple(cen[k]) for k in range(K)}; pal=dict(sorted(pal.items(),key=lambda kv:syms.index(kv[0])))
grids=[]; i0=0
for cg,cb in canv:
    n=int((~cb).sum()); L=km.labels_[i0:i0+n]; i0+=n; it=iter(L)
    rows=["".join("." if cb[y,x] else syms[rank[int(next(it))]] for x in range(CW)) for y in range(CH)]
    grids.append(rows)
json.dump({"pal":pal,"grids":grids},open('sheet.json','w'),ensure_ascii=False)
rgb={k:tuple(int(v[i:i+2],16) for i in (1,3,5)) for k,v in pal.items()}
z=4; o=Image.new('RGB',((CW+6)*z*4,CH*z),(104,100,92))
for k,rows in enumerate(grids):
    for y,r in enumerate(rows):
        for x,ch in enumerate(r):
            if ch!=".": o.paste(rgb[ch],((CW+6)*z*k+x*z,y*z,(CW+6)*z*k+x*z+z,y*z+z))
o.save('q.png'); print(len(pal),"色")
