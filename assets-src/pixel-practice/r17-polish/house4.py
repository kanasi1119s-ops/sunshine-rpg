import sys, json, math, random; sys.path.insert(0,"../../../tools/pixel-practice")
from shapes import Canvas
W,H=48,48
pal={"A":"#1e1620","S":"#3c3050",
 "R1":"#4a1820","R2":"#7a2a2c","R3":"#a8402e","R4":"#cc5c3c","R5":"#ec8452","R6":"#ffb078",
 "P1":"#c8b08a","P2":"#e8d8b4","P3":"#f8f0d8",
 "B2":"#5c3a1c","B3":"#845428",
 "K1":"#585468","K2":"#807c94","K3":"#aaa8bc",
 "D1":"#4a2a14","D2":"#7a4a22","D3":"#a8703a",
 "G1":"#7ab8e0","G2":"#aee0f8","F1":"#3a8a3a","F3":"#e84a5a","Y":"#f4cc50","F2":"#68c048","M1":"#4a7a38","M2":"#6a9a48","CUR":"#d86a5a"}
def real(c):
    rnd=random.Random(13)
    for _ in range(14):
        x=rnd.randint(3,44); y=rnd.randint(16,21)
        if c.get(x,y) in ('R3','R4','R5','R2'): c.put(x,y,'M2'); c.put(x+1,y,'M1') if rnd.random()<0.6 else None
    for y in range(32,36):
        if c.get(37,y) in ('P2','P1','P3'): pass
    for k in range(3):
        if c.get(12,30+k) in ('P3','P2','P1'): c.put(12,30+k,'P1')
    for (x,y) in ((20,34),(21,35),(10,28),(11,29)):
        if c.get(x,y) in ('P3','P2','P1'): c.put(x,y,'B2')
    for y in range(25,28):
        for x in (35,36,39,40):
            if c.get(x,y) in ('G1','G2'): c.put(x,y,'CUR')
    for t in range(0,16):
        x=7+int(1.5*math.sin(t*0.6)); y=36-t*0.8
        c.put(int(x),int(y),'F1')
        if t%3==0: c.put(int(x)+1,int(y)-1,'F2')
def base_grass(c):
    rnd=random.Random(2)
    for x in range(5,44):
        if rnd.random()<0.5:
            h=rnd.randint(1,2)
            for k in range(h): c.put(x,42-k,'F1' if k==0 else 'F2')
def house(ver,roof=None):
    random.seed(5)
    c=Canvas(W,H)
    # 影
    for y in range(43,47):
        for x in range(6,48):
            if (x+y)%2==0 or y<45: c.put(x,y,'S')
    # 石の土台（石積み）
    for y in range(37,43):
        for x in range(6,43):
            row=y-37; off=(row%2)*3
            k='K3' if row==0 else 'K2'
            if (x+off)%6==5 or row==5: k='K1'
            elif (x+off)%6==0 and row>0: k='K3'
            if x>=34 and k!='K1': k={'K3':'K2','K2':'K1'}[k]
            c.put(x,y,k)
    # 壁（漆喰）: 軒の影が上に落ち、右は陰
    for y in range(22,37):
        for x in range(7,42):
            k='P3' if x<18 else 'P2' if x<34 else 'P1'
            if y<=23: k={'P3':'P2','P2':'P1','P1':'B3'}[k] if False else {'P3':'P2','P2':'P1','P1':'P1'}[k]   # 軒の影
            if ver>=2 and (x*7+y*3)%23==0: k={'P3':'P2','P2':'P1','P1':'P1'}[k]
            c.put(x,y,k)
    # 梁（光る面＋影の面の2ドット幅）
    def beam(x0,y0,x1,y1):
        n=max(abs(x1-x0),abs(y1-y0))
        for i in range(n+1):
            x=x0+(x1-x0)*i/n; y=y0+(y1-y0)*i/n
            c.put(x,y,'B3'); c.put(x+1,y,'B2') if x1==x0 else c.put(x,y+1,'B2')
    for x in (7,41): beam(x,22,x,36)
    for x in (24,):  beam(x,22,x,36)
    beam(7,36,41,36); beam(7,22,41,22) if False else None
    for x in range(7,42): c.put(x,22,'B2'); c.put(x,26,'B3') if False else None
    if ver>=2:
        beam(8,35,16,24); beam(16,35,8,24)                       # ×の筋交い（左）
    # 扉（アーチ）: 板、鉄の蝶番、取っ手、石の段
    for y in range(25,37):
        for x in range(26,33):
            top=25+ (1 if x in (26,32) else 0)
            if y<top: continue
            k='D3' if x<28 else 'D2' if x<31 else 'D1'
            if (x-26)%2==1: k='D1' if k!='D1' else 'A'
            c.put(x,y,k)
    for x in range(27,32): c.put(x,24,'D2')
    c.put(28,23,'D2'); c.put(29,23,'D3'); c.put(30,23,'D2')
    c.put(31,31,'Y'); c.put(31,32,'Y')
    for x in range(25,34): c.put(x,37,'K3')
    # 窓（右）: 木枠・雨戸・ガラスの反射・花箱
    for y in range(25,32):
        for x in range(35,40): c.put(x,y,'G1' if (x+y)%7 else 'G2')
    for x in range(34,41): c.put(x,24,'B3'); c.put(x,32,'B2')
    for y in range(24,33): c.put(34,y,'B3'); c.put(40,y,'B2'); c.put(37,y,'B2')
    for x in range(34,41): c.put(x,28,'B2')
    c.put(35,25,'G2'); c.put(36,26,'G2')
    for x in range(33,42): c.put(x,33,'B2') ; c.put(x,34,'A')
    for x in range(34,41):
        c.put(x,32,'F1' if x%2 else 'F1'); 
    for x,y in [(35,31),(37,31),(39,31)]: c.put(x,y,'F3')
    # 左の窓（小さな丸窓）
    for dx in range(-2,3):
        for dy in range(-2,3):
            if dx*dx+dy*dy<=5: c.put(18+dx,28+dy,'G1' if dx+dy>-1 else 'G2')
    c.put(17,27,'G2')
    for dx in range(-3,4):
        for dy in range(-3,4):
            if 7<=dx*dx+dy*dy<=10: c.put(18+dx,28+dy,'B2')
    # 屋根: 台形、瓦の段（左が明るく右が暗い）、上端の光・下端の影
    base=[('R6','R5','R4','R3','R2'),('R5','R4','R3','R2','R1')]
    if roof: base=[roof[0],roof[1]]
    def roofk(x,y):
        row=(y-8)//3; ly=(y-8)%3; off=2 if row%2 else 0
        cell=(x+off)%4; cid=(x+off)//4
        side=0 if x<27 else 1
        pal_=base[side]
        if cell==3: return pal_[4]
        h=(row*7919+cid*104729)%11; j=1 if h<2 else -1 if h>8 else 0
        if ly==0: return pal_[0] if row%2==0 else pal_[1]
        if ly==2: return pal_[3]
        return pal_[max(1,min(3,2+j))]
    c.poly([(1,22),(9,8),(39,8),(47,22)],roofk)
    for x in range(9,40): c.put(x,7,'R6' if x<27 else 'R4'); c.put(x,8,'R5' if x<27 else 'R3')      # 棟
    for x in range(1,48): c.put(x,22,'R1'); c.put(x,26,'R1') if False else None
    for x in range(2,47):
        if x%2: c.put(x,23,'S')
    # 煙突
    c.poly([(32,2),(38,2),(38,11),(32,11)],lambda x,y:'K3' if x<35 else 'K2' if (x+y)%5 else 'K1')
    for x in range(31,40): c.put(x,1,'K3'); c.put(x,2,'K2')
    for x,y in [(34,0),(35,0)]: c.put(x,y,'K3')
    real(c)
    c.outline('A',skip=('S','K3'))
    base_grass(c)
    for y in range(H):
        for x in range(W):
            if c.get(x,y)=='S' and not any(c.get(x+dx,y+dy)=='S' for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): c.put(x,y,'.')
    return c
letters="BCDEFGHIJKLMNOPQRTUVXYZabcdefghijklmnopqrstuvwxyz0123456789"
names=list(pal)
mp={n:(n if n in ("A","S") else letters[i]) for i,n in enumerate(names)}
def save(name,c): open(name,"w").write("\n".join("".join("." if ch=="." else mp[ch] for ch in r) for r in c.g)+"\n")
for v in (1,2): save(f"house4-{v}.txt",house(v))
json.dump({mp[k]:v for k,v in pal.items()},open("pal-house4.json","w"))
blue={"R1":"#1c2850","R2":"#2c4a88","R3":"#3a64b0","R4":"#4e80d0","R5":"#78a8ec","R6":"#a8ccff"}
green={"R1":"#183a28","R2":"#2a6040","R3":"#3a8a52","R4":"#52aa66","R5":"#80d090","R6":"#b0f0b8"}
for nm,vv in (("blue",blue),("green",green)):
    d={mp[k]:v for k,v in pal.items() if k in mp}
    for k,col in vv.items(): d[mp[k]]=col
    json.dump(d,open(f"pal-house4-{nm}.json","w"))
print(len(pal))
