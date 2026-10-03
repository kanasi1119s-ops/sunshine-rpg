import sys, json, math, random; sys.path.insert(0,"../../../tools/pixel-practice")
from shapes import Canvas
W,H=80,80
pal={"A":"#1e1620","S":"#3c3050",
 "R1":"#4a1820","R2":"#7a2a2c","R3":"#a8402e","R4":"#cc5c3c","R5":"#ec8452","R6":"#ffb078",
 "P1":"#c8b08a","P2":"#e8d8b4","P3":"#f8f0d8",
 "B2":"#5c3a1c","B3":"#845428",
 "K1":"#585468","K2":"#807c94","K3":"#aaa8bc",
 "D1":"#4a2a14","D2":"#7a4a22","D3":"#a8703a",
 "G1":"#7ab8e0","G2":"#aee0f8","F1":"#3a8a3a","F3":"#e84a5a","Y":"#f4cc50","Z":"#2a2438"}
def manor(roof=None):
    random.seed(8)
    c=Canvas(W,H)
    # 地面の影
    for y in range(74,79):
        for x in range(4,80):
            if (x+y)%2==0 or y<76: c.put(x,y,'S')
    # 石の土台と階段
    for y in range(66,74):
        for x in range(4,76):
            row=y-66; off=(row%2)*3
            k='K3' if row==0 else 'K2'
            if (x+off)%6==5 or row==7: k='K1'
            elif (x+off)%6==0 and row>0: k='K3'
            if x>=56 and k!='K1': k={'K3':'K2','K2':'K1'}[k]
            c.put(x,y,k)
    for i,(x0,x1) in enumerate([(30,50),(32,48)]):
        for x in range(x0,x1+1): c.put(x,74+i-1 if False else 72+i,'K3' if i==0 else 'K2')
    # 1階の壁・2階の壁（漆喰、右へ向かうほど陰）
    def wall(y0,y1):
        for y in range(y0,y1):
            for x in range(6,74):
                k='P3' if x<30 else 'P2' if x<54 else 'P1'
                if y<=y0+1: k={'P3':'P2','P2':'P1','P1':'P1'}[k]
                if (x*7+y*3)%29==0: k={'P3':'P2','P2':'P1','P1':'P1'}[k]
                c.put(x,y,k)
    wall(26,48); wall(48,66)
    def beam(x0,y0,x1,y1,two=True):
        n=max(abs(x1-x0),abs(y1-y0))
        for i in range(n+1):
            x=x0+(x1-x0)*i/n; y=y0+(y1-y0)*i/n
            c.put(x,y,'B3'); c.put(x+1,y,'B2') if x1==x0 else c.put(x,y+1,'B2')
    for x in (6,26,40,54,72):
        beam(x,26,x,65)
    for y in (26,47,64): 
        for x in range(6,74): c.put(x,y,'B3'); c.put(x,y+1,'B2')
    for k in range(11): c.put(7+k,45-k,'B3'); c.put(8+k,45-k,'B2'); c.put(25-k,45-k,'B3'); c.put(24-k,45-k,'B2')   # 2階の筋交い（左）
    for k in range(11): c.put(55+k,45-k,'B3'); c.put(56+k,45-k,'B2'); c.put(71-k,45-k,'B3'); c.put(70-k,45-k,'B2')   # 右
    # 窓を作る関数
    def window(x0,y0,w,h):
        for y in range(y0,y0+h):
            for x in range(x0,x0+w): c.put(x,y,'G1' if (x+y)%7 else 'G2')
        for x in range(x0-1,x0+w+1): c.put(x,y0-1,'B3'); c.put(x,y0+h,'B2')
        for y in range(y0-1,y0+h+1): c.put(x0-1,y,'B3'); c.put(x0+w,y,'B2')
        for y in range(y0,y0+h): c.put(x0+w//2,y,'B2')
        for x in range(x0,x0+w): c.put(x,y0+h//2,'B2')
        c.put(x0+1,y0+1,'G2'); c.put(x0+2,y0+2,'G2')
    for x in (10,60):   # 1階の窓
        window(x,52,7,9)
    window(37,30,7,9)   # 2階の中央（バルコニーの上）
    for x in (10,60):      # 1階の窓＋花箱
        window(x,30,7,9)
        for xx in range(x-2,x+10): c.put(xx,41,'B2'); c.put(xx,42,'B3')
        for xx in range(x-1,x+9): c.put(xx,40,'F1')
        for xx in (x,x+3,x+6): c.put(xx,39,'F3')
    # バルコニー（2階の中央）
    for x in range(28,53): c.put(x,48,'B3'); c.put(x,49,'B2')
    for x in range(29,52,3):
        for y in range(44,48): c.put(x,y,'B3')
    for x in range(28,53): c.put(x,44,'B3')
    # 大きな両開きの扉（アーチ）
    for y in range(52,66):
        for x in range(33,48):
            top=52+(2 if x in (33,47) else 1 if x in (34,46) else 0)
            if y<top: continue
            k='D3' if x<40 else 'D2'
            if (x-33)%3==2: k='D1'
            c.put(x,y,k)
    for y in range(52,66): c.put(40,y,'D1')
    c.put(38,60,'Y'); c.put(42,60,'Y'); c.put(38,61,'Y'); c.put(42,61,'Y')
    for x in range(32,49): c.put(x,51,'B3'); c.put(x,50,'B2') if x%2 else None
    # 屋根（2階の上）: 大きな台形、瓦の段、ドーマー（屋根窓）2つ
    base=[('R6','R5','R4','R3','R2'),('R5','R4','R3','R2','R1')]
    if roof: base=[roof[0],roof[1]]
    def roofk(x,y):
        row=(y-8)//3; ly=(y-8)%3; off=2 if row%2 else 0
        cell=(x+off)%4; pal_=base[0 if x<40 else 1]
        if cell==3: return pal_[4]
        if ly==0: return pal_[0] if row%2==0 else pal_[1]
        if ly==2: return pal_[3]
        return pal_[2]
    c.poly([(1,26),(14,8),(66,8),(79,26)],roofk)
    for x in range(14,67): c.put(x,7,'R6' if x<40 else 'R4'); c.put(x,8,'R5' if x<40 else 'R3')
    for x in range(1,80): c.put(x,26,'R1')
    for x in range(2,79):
        if x%2: c.put(x,27,'S')
    for cx in (22,58):   # ドーマー
        c.poly([(cx-6,24),(cx-6,16),(cx,11),(cx+6,16),(cx+6,24)],lambda x,y:'P3' if x<cx else 'P2')
        for y in range(17,24):
            for x in range(cx-3,cx+4): c.put(x,y,'G1' if (x+y)%6 else 'G2')
        for x in range(cx-4,cx+5): c.put(x,16,'B3'); c.put(x,24,'B2')
        for y in range(16,25): c.put(cx-4,y,'B3'); c.put(cx+4,y,'B2'); c.put(cx,y,'B2')
        for k in range(7): c.put(cx-6+k,16-k//1 if k<6 else 10,'R5' if cx<40 else 'R3')
        for k in range(7): c.put(cx+6-k,16-k,'R3')
    # 煙突2本
    for cx in (12,66):
        c.poly([(cx-3,1),(cx+3,1),(cx+3,12),(cx-3,12)],lambda x,y:'K3' if x<cx else 'K2' if (x+y)%5 else 'K1')
        for x in range(cx-4,cx+5): c.put(x,0,'K2'); c.put(x,1,'K1')
    c.outline('A',skip=('S',))
    for y in range(H):
        for x in range(W):
            if c.get(x,y)=='S' and not any(c.get(x+dx,y+dy)=='S' for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): c.put(x,y,'.')
    return c
letters="BCDEFGHIJKLMNOPQRTUVXYZabcdefghijklmnopqrstuvwxyz0123456789"
mp={n:(n if n in ("A","S") else letters[i]) for i,n in enumerate(pal)}
def save(name,c): open(name,"w").write("\n".join("".join("." if ch=="." else mp[ch] for ch in r) for r in c.g)+"\n")
save("manor1.txt",manor())
json.dump({mp[k]:v for k,v in pal.items()},open("pal-manor.json","w"))
blue={"R1":"#1c2850","R2":"#2c4a88","R3":"#3a64b0","R4":"#4e80d0","R5":"#78a8ec","R6":"#a8ccff"}
green={"R1":"#183a28","R2":"#2a6040","R3":"#3a8a52","R4":"#52aa66","R5":"#80d090","R6":"#b0f0b8"}
for nm,vv in (("blue",blue),("green",green)):
    d={mp[k]:v for k,v in pal.items()}
    for k,col in vv.items(): d[mp[k]]=col
    json.dump(d,open(f"pal-manor-{nm}.json","w"))
print(len(pal))
