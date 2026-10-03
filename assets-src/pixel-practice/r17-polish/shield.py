import sys, json, math; sys.path.insert(0,"../../../tools/pixel-practice")
from shapes import Canvas
import numpy as np
W,H=34,38
def mask_fn(x,y):
    # 盾の形: 上は平ら＋角が少し丸い、下は尖る曲線
    nx=(x+.5-17)/14.2; yy=(y+.5-3)/32
    if yy<0 or yy>1: return False
    half = 1.0 if yy<0.45 else math.sqrt(max(0,1-((yy-0.45)/0.55)**1.7))
    if yy<0.06: half=min(half, 0.9+yy*1.6)
    return abs(nx)<=half
def dist(m):
    d=np.full(m.shape,99.0)
    h,w=m.shape
    for y in range(h):
        for x in range(w):
            if m[y,x]:
                best=99
                for r in range(1,8):
                    found=False
                    for dy in range(-r,r+1):
                        for dx in range(-r,r+1):
                            if max(abs(dx),abs(dy))!=r: continue
                            yy,xx=y+dy,x+dx
                            if not(0<=yy<h and 0<=xx<w) or not m[yy,xx]: found=True; best=min(best,math.hypot(dx,dy))
                    if found: break
                d[y,x]=best
    return d
def shield(ver):
    m=np.array([[mask_fn(x,y) for x in range(W)] for y in range(H)])
    d=dist(m)
    c=Canvas(W,H)
    # 影
    for y in range(H-4,H):
        for x in range(8,27):
            dd=((x+.5-17)/9)**2+((y+.5-(H-2))/1.8)**2
            if dd<=1 and (dd<.5 or (x+y)%2==0): c.put(x,y,'S')
    for y in range(H):
        for x in range(W):
            if not m[y,x]: continue
            dd=d[y,x]
            nx=(x+.5-17)/14; ny=(y+.5-18)/17
            if dd<=3.2:            # 縁（金属の斜面）: 位置で明るさが変わる
                ang=-nx*0.7-ny*0.7
                k=['5','4','3','2','1'][min(4,max(0,int((0.75-ang)/0.3)))] if False else None
                lum=ang
                t='m5' if lum>0.55 else 'm4' if lum>0.2 else 'm3' if lum>-0.15 else 'm2' if lum>-0.5 else 'm1'
                if dd<=1.6 and lum<0: t={'m3':'m2','m2':'m1'}.get(t,t)      # 外側は少し暗く
                if dd>2.4 and lum>0.2: t='m5'                              # 内側の斜面は明るい線
                c.put(x,y,t)
            else:                   # 盾面（赤）。中央が少しふくらむ
                lum=-nx*0.5-ny*0.55+0.5*(1-min(1,nx*nx+ny*ny))
                t='r5' if lum>0.85 else 'r4' if lum>0.55 else 'r3' if lum>0.25 else 'r2' if lum>-0.05 else 'r1'
                c.put(x,y,t)
    # 紋章: 金の十字＋中央の宝石
    for y in range(8,29):
        for x in (16,17,18):
            if c.get(x,y).startswith('r'): c.put(x,y,'y2' if x==16 else 'y3' if x==17 else 'y1')
    for x in range(10,25):
        for y in (14,15,16):
            if c.get(x,y).startswith('r') or c.get(x,y).startswith('y'): c.put(x,y,'y2' if y==14 else 'y3' if y==15 else 'y1')
    for dx in range(-2,3):
        for dy in range(-2,3):
            if abs(dx)+abs(dy)<=3: c.put(17+dx,15+dy,'b3' if dx+dy<0 else 'b2' if dx+dy<2 else 'b1')
    c.put(16,14,'W'); c.put(15,13,'w')
    # 縁のリベット（4か所）
    for x,y in [(17,5),(6,13),(28,13),(17,31)]:
        c.put(x,y,'W'); c.put(x+1,y,'m1') if c.get(x+1,y)!='.' else None
    c.outline('A',skip=('S',))
    # 金属の縁の外側の輪郭を、明るい側だけ中間色の縁に
    if ver>=2:
        for y in range(H):
            for x in range(W):
                if c.get(x,y)=='A' and (x+y)<24 and c.get(x+1,y+1)!='.': c.put(x,y,'a2')
    for y in range(H):
        for x in range(W):
            if c.get(x,y)=='S' and not any(c.get(x+dx,y+dy)=='S' for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): c.put(x,y,'.')
    return c
pal={"A":"#1a1a26","a2":"#3a4060","S":"#3a2a46","W":"#ffffff","w":"#ffe0e0",
 "m1":"#4a5272","m2":"#6a7494","m3":"#9aa4be","m4":"#c4cce0","m5":"#eef2fa",
 "r1":"#7a1a2e","r2":"#a82838","r3":"#cc3c44","r4":"#e45a52","r5":"#f48068",
 "y1":"#a86a18","y2":"#e0a030","y3":"#ffd860","b1":"#2a56b0","b2":"#4a84e8","b3":"#9acaff"}
sym={}
def conv(c):
    names=sorted(set(ch for ch in pal))
    letters="BCDEFGHIJKLMNOPQRTUVWXYZabcdefghijklmnopqrstuvwxyz"
    mp={}
    for i,n in enumerate(pal): mp[n]=letters[i] if n not in ("A","W","S") else n
    return mp
mp=conv(None)
for v in (1,2):
    c=shield(v)
    # 2文字キーを1文字に変換
    rows=[]
    for r in c.g:
        rows.append("".join(("." if ch=="." else mp.get(ch,ch)) if len(ch)==1 else mp[ch] for ch in r))
    open(f"shield{v}.txt","w").write("\n".join(rows)+"\n")
json.dump({mp[k]:v for k,v in pal.items()},open("pal-shield.json","w"))
