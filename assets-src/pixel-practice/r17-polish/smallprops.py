import sys, json, math, random; sys.path.insert(0,"../../../tools/pixel-practice")
from shapes import Canvas
tpal={"A":"#14240c","S":"#3a4a2e","l1":"#1f4a1c","l2":"#2d6a24","l3":"#44902c","l4":"#68b838","l5":"#96dc54","l6":"#c8f27c","r":"#d8344c","R":"#9a2234"}
def bush():
    random.seed(3)
    c=Canvas(30,18)
    for y in range(14,18):
        for x in range(2,28):
            dd=((x+.5-15)/12)**2+((y+.5-16)/1.8)**2
            if dd<=1 and (dd<.55 or (x+y)%2==0): c.put(x,y,'S')
    for (cx,cy,rx,ry) in [(15,8,9,6),(8,10,7,5),(22,10,7,5),(11,6,6,4),(19,6,6,4)]:
        for y in range(int(cy-ry-2),int(cy+ry+3)):
            for x in range(int(cx-rx-2),int(cx+rx+3)):
                ang=math.atan2(y+.5-cy,x+.5-cx); bump=1+0.1*math.sin(ang*6+cx)
                nx=(x+.5-cx)/(rx*bump); ny=(y+.5-cy)/(ry*bump); r2=nx*nx+ny*ny
                if r2>1: continue
                z=math.sqrt(1-r2); lum=-nx*0.55-ny*0.75+0.5*z-0.15-0.4*max(0,ny)+(0.1 if (x*5+y*3)%6==0 else 0)
                k='l6' if lum>1.0 else 'l5' if lum>0.7 else 'l4' if lum>0.4 else 'l3' if lum>0.1 else 'l2' if lum>-0.25 else 'l1'
                if r2>0.72 and (nx*0.5+ny)>0.25: k={'l6':'l4','l5':'l3','l4':'l2','l3':'l1','l2':'l1','l1':'l1'}[k]
                c.put(x,y,k)
    for x,y in [(12,7),(19,9),(8,10),(23,8)]: c.put(x,y,'r'); c.put(x+1,y+1,'R')
    c.outline('A',skip=('S',))
    return c
rpal={"A":"#2a2630","S":"#4a3a58","g1":"#3a3644","g2":"#5a5668","g3":"#807c92","g4":"#aaa6ba","g5":"#d6d2e0","m":"#5a9a48","M":"#3a7034","K":"#2a2832"}
def rock():
    c=Canvas(28,20)
    for y in range(16,20):
        for x in range(2,26):
            dd=((x+.5-14)/12)**2+((y+.5-18)/1.8)**2
            if dd<=1 and (dd<.55 or (x+y)%2==0): c.put(x,y,'S')
    pts=[(3,16),(2,11),(6,6),(12,3),(19,5),(24,10),(25,16)]
    faces=[([(6,6),(12,3),(14,9),(8,11)],'g5'),([(12,3),(19,5),(17,10),(14,9)],'g4'),([(19,5),(24,10),(21,13),(17,10)],'g3'),
           ([(2,11),(6,6),(8,11),(4,16),(3,16)],'g4'),([(8,11),(14,9),(17,10),(21,13),(25,16),(4,16)],'g3'),([(17,10),(21,13),(25,16),(18,16)],'g2')]
    c.poly(pts,lambda x,y:'g3')
    for poly_,k in faces: c.poly(poly_,lambda x,y,k=k:k)
    # 下の暗がりと割れ目、苔
    for x in range(4,25): c.put(x,16,'g1'); c.put(x,15,'g2') if x>10 else None
    for k in range(5): c.put(12+k//2,9+k,'K')
    for k in range(4): c.put(18+k//2,11+k,'K')
    for x,y in [(5,13),(6,14),(7,14),(21,15),(22,14),(8,15)]: c.put(x,y,'m'); 
    for x,y in [(5,14),(6,15)]: c.put(x,y,'M')
    for x,y in [(9,5),(10,5),(8,6)]: c.put(x,y,'g5')
    c.outline('A',skip=('S',))
    return c
letters="BCDEFGHIJKLMNOPQRTUVXYZabcdefghijklmnopqrstuvwxyz"
def save(name,c,pal):
    mp={n:(n if n in ("A","S") else letters[i]) for i,n in enumerate(pal)}
    open(name+".txt","w").write("\n".join("".join("." if ch=="." else mp[ch] for ch in r) for r in c.g)+"\n")
    json.dump({mp[k]:v for k,v in pal.items()},open("pal-"+name+".json","w"))
save("bush2",bush(),tpal); save("rock2",rock(),rpal)
