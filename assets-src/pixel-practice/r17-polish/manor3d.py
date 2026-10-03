import sys, json, math, random; sys.path.insert(0,"../../../tools/pixel-practice")
from shapes import Canvas
W,H=80,80
pal={"A":"#1e1620","S":"#3c3050",
 "R1":"#4a1820","R2":"#7a2a2c","R3":"#a8402e","R4":"#cc5c3c","R5":"#ec8452","R6":"#ffb078",
 "P1":"#b49c78","P2":"#e8d8b4","P3":"#f8f0d8","Q2":"#c4ae88",
 "B2":"#5c3a1c","B3":"#845428",
 "K1":"#585468","K2":"#807c94","K3":"#aaa8bc",
 "D1":"#4a2a14","D2":"#7a4a22","D3":"#a8703a",
 "G1":"#7ab8e0","G2":"#aee0f8","F1":"#3a8a3a","F3":"#e84a5a","Y":"#f4cc50"}
SL=0.45     # 側面の傾き（右へ行くほど上がる = 奥へ遠ざかる）
def manor(roof=None):
    random.seed(8)
    c=Canvas(W,H)
    FX0,FX1=4,58            # 正面の壁 x
    SX1=78                  # 側面の壁の右端
    top,bot=36,70           # 正面の壁の上端・下端（足元の石の上）
    # 地面の影（右奥へ伸びる平行四辺形）
    for y in range(70,79):
        for x in range(8,80):
            if (x+y)%2==0 or y<77: 
                if y>= 70-(max(0,x-FX1))*SL+4 and y<=78: c.put(x,y,'S')
    # 側面の壁（暗い。上端と下端が右へ向かって上がる）
    for x in range(FX1,SX1):
        yt=top-(x-FX1)*SL; yb=bot-(x-FX1)*SL
        for y in range(int(round(yt)),int(round(yb))+1):
            k='Q2' if x<FX1+8 else 'P1' if x<FX1+16 else 'P1'
            if y<=yt+2: k='P1' if k=='Q2' else 'P1'   # 軒の影
            if (x*5+y*3)%31==0: k='P1'
            c.put(x,y,k)
    # 正面の壁（明るい）
    for y in range(top,bot+1):
        for x in range(FX0,FX1+1):
            k='P3' if x<30 else 'P2'
            if y<=top+1: k='P2' if k=='P3' else 'Q2'          # 軒の影
            if (x*7+y*3)%29==0: k='P2' if k=='P3' else 'Q2'
            c.put(x,y,k)
    # 正面の足元（石の土台）と側面の土台（斜め）
    for y in range(bot+1,bot+7):
        for x in range(FX0-1,FX1+2):
            row=y-bot-1; off=(row%2)*3
            k='K3' if row==0 else 'K2'
            if (x+off)%6==5 or row==5: k='K1'
            elif (x+off)%6==0 and row>0: k='K3'
            c.put(x,y,k)
    for x in range(FX1+2,SX1):
        yb=bot-(x-FX1)*SL
        for y in range(int(round(yb))+1,int(round(yb))+7):
            row=y-int(round(yb))-1
            k='K2' if row<2 else 'K1'
            if (x+row*3)%6==5: k='K1'
            c.put(x,y,k)
    # 梁（正面・側面）
    def vbeam(x,y0,y1,h='B3'):
        for y in range(y0,y1+1): c.put(x,y,h); c.put(x+1,y,'B2')
    for x in (FX0,18,34,46,FX1-1): vbeam(x,top,bot)
    for x in range(FX0,FX1+1): c.put(x,top,'B3'); c.put(x,top+1,'B2'); c.put(x,53,'B3'); c.put(x,54,'B2'); c.put(x,bot-1,'B3'); c.put(x,bot,'B2')
    for x in range(FX1,SX1):         # 側面の梁（横）
        d=(x-FX1)*SL
        for yy in (top,53,bot-1): c.put(x,int(round(yy-d)),'B2')
    for x in (FX1+8,FX1+16):
        d=(x-FX1)*SL
        for y in range(int(round(top-d)),int(round(bot-d))+1): c.put(x,y,'B2')
    # 窓
    def window(x0,y0,w,h):
        for y in range(y0,y0+h):
            for x in range(x0,x0+w): c.put(x,y,'G1' if (x+y)%7 else 'G2')
        for x in range(x0-1,x0+w+1): c.put(x,y0-1,'B3'); c.put(x,y0+h,'B2')
        for y in range(y0-1,y0+h+1): c.put(x0-1,y,'B3'); c.put(x0+w,y,'B2')
        for y in range(y0,y0+h): c.put(x0+w//2,y,'B2')
        for x in range(x0,x0+w): c.put(x,y0+h//2,'B2')
        c.put(x0+1,y0+1,'G2'); c.put(x0+2,y0+2,'G2')
    def sidewin(x0,w,yTopAtX0,h):       # 側面の窓: 斜めに傾く平行四辺形
        for dx in range(w):
            x=x0+dx; yt=int(round(yTopAtX0-dx*SL))
            for y in range(yt,yt+h): c.put(x,y,'G1' if (dx+y)%7 else 'G1')
            c.put(x,yt-1,'B2'); c.put(x,yt+h,'B2')
        for y in range(int(round(yTopAtX0))-1,int(round(yTopAtX0))+h+1): c.put(x0-1,y,'B2')
        for dx in range(w): c.put(x0+dx,int(round(yTopAtX0-dx*SL))+h//2,'B2')
    for x in (9,38):        # 2階の窓（正面）
        window(x,40,8,9)
    window(23,40,8,9)
    for x in (9,):          # 1階の窓＋花箱
        window(x,58,8,8)
        for xx in range(x-2,x+10): c.put(xx,68,'B3')
        for xx in range(x-1,x+9): c.put(xx,67,'F1')
        for xx in (x,x+3,x+6): c.put(xx,66,'F3')
    sidewin(FX1+3,8,int(top+6-3*SL),10); sidewin(FX1+3,8,int(top+24-3*SL),9)
    sidewin(FX1+12,6,int(top+6-12*SL),10); 
    # 玄関（左中央寄り）: アーチ扉、ポーチの屋根と柱、石段
    for y in range(56,bot+1):
        for x in range(27,38):
            tp=56+(2 if x in (27,37) else 1 if x in (28,36) else 0)
            if y<tp: continue
            k='D3' if x<32 else 'D2'
            if (x-27)%3==2: k='D1'
            c.put(x,y,k)
    for y in range(56,bot+1): c.put(32,y,'D1')
    c.put(30,64,'Y'); c.put(34,64,'Y')
    # ポーチ: 手前に張り出す小さな屋根と2本の柱（奥行き）
    for x in range(22,43):
        for y in range(50,53): c.put(x,y,'R5' if y==50 else 'R4' if y==51 else 'R3')
        c.put(x,53,'R1')
    for x in range(21,44): c.put(x,49,'R6') if x%2==0 else None
    for px in (24,40):
        for y in range(54,bot+1): c.put(px,y,'B3'); c.put(px+1,y,'B2')
    for x in range(22,43): c.put(x,bot+1,'K3'); c.put(x,bot+2,'K2')
    for x in range(24,41): c.put(x,bot+3,'K2')
    for y in range(54,58):                       # ポーチの屋根の影が壁に落ちる
        for x in range(26,38):
            if c.get(x,y) in ('P3','P2'): c.put(x,y,'Q2')
    # 屋根（前面）: 台形、瓦の段。右の面は暗く、斜めに傾く
    base=[('R6','R5','R4','R3','R2'),('R5','R4','R3','R2','R1')]
    if roof: base=[roof[0],roof[1]]
    def front_roof(x,y):
        row=(y-12)//3; ly=(y-12)%3; off=2 if row%2 else 0
        cell=(x+off)%4; pal_=base[0]
        if cell==3: return pal_[4]
        if ly==0: return pal_[0] if row%2==0 else pal_[1]
        if ly==2: return pal_[3]
        return pal_[2]
    c.poly([(0,top),(9,13),(50,13),(FX1+6,top)],front_roof)
    def side_roof(x,y):
        yy=y+(x-FX1)*SL
        row=int((yy-12)//3); ly=int((yy-12)%3); off=2 if row%2 else 0
        cell=(x+off)%4; pal_=base[1]
        if cell==3: return pal_[3]
        if ly==0: return pal_[1]
        if ly==2: return pal_[3]
        return pal_[2]
    c.poly([(50,13),(FX1+6,top),(SX1+2,top-(SX1+2-FX1)*SL),(66,18)],side_roof)
    for x in range(9,51): c.put(x,12,'R6'); c.put(x,13,'R5')       # 棟
    for y in range(13,top):                                       # 隅棟（前と側の境の稜線）を明るく
        x=50+(y-13)*(FX1+6-50)/(top-13); c.put(x,y,'R6'); c.put(x+1,y,'R5')
    # 軒先の影（壁側へ）と側面の軒
    for x in range(0,FX1+7): c.put(x,top,'R1'); c.put(x,top+1,'R1') if x%2 else None
    for x in range(FX1+6,SX1+3):
        y=top-(x-FX1)*SL; c.put(x,int(round(y)),'R1'); c.put(x,int(round(y))+1,'R1') if x%2 else None
    # ドーマー（前面の屋根窓、奥行きを出すため側面にも小さな屋根窓）
    cx=29
    c.poly([(cx-7,32),(cx-7,22),(cx,16),(cx+7,22),(cx+7,32)],lambda x,y:'P3' if x<cx else 'P2')
    for y in range(23,32):
        for x in range(cx-4,cx+5): c.put(x,y,'G1' if (x+y)%6 else 'G2')
    for x in range(cx-5,cx+6): c.put(x,22,'B3'); c.put(x,32,'B2')
    for y in range(22,33): c.put(cx-5,y,'B3'); c.put(cx+5,y,'B2'); c.put(cx,y,'B2')
    for k in range(8): c.put(cx-7+k,22-k if k<7 else 15,'R5'); c.put(cx+7-k,22-k,'R3')
    # 煙突（奥の屋根の上）
    c.poly([(40,2),(47,2),(47,16),(40,16)],lambda x,y:'K3' if x<43 else 'K2' if (x+y)%5 else 'K1')
    for x in range(39,49): c.put(x,1,'K2'); c.put(x,2,'K1')
    c.outline('A',skip=('S',))
    for y in range(H):
        for x in range(W):
            if c.get(x,y)=='S' and not any(c.get(x+dx,y+dy)=='S' for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): c.put(x,y,'.')
    return c
letters="BCDEFGHIJKLMNOPQRTUVXYZabcdefghijklmnopqrstuvwxyz0123456789"
mp={n:(n if n in ("A","S") else letters[i]) for i,n in enumerate(pal)}
def save(name,c): open(name,"w").write("\n".join("".join("." if ch=="." else mp[ch] for ch in r) for r in c.g)+"\n")
save("manor2.txt",manor())
json.dump({mp[k]:v for k,v in pal.items()},open("pal-manor2.json","w"))
blue={"R1":"#1c2850","R2":"#2c4a88","R3":"#3a64b0","R4":"#4e80d0","R5":"#78a8ec","R6":"#a8ccff"}
green={"R1":"#183a28","R2":"#2a6040","R3":"#3a8a52","R4":"#52aa66","R5":"#80d090","R6":"#b0f0b8"}
for nm,vv in (("blue",blue),("green",green)):
    d={mp[k]:v for k,v in pal.items()}
    for k,col in vv.items(): d[mp[k]]=col
    json.dump(d,open(f"pal-manor2-{nm}.json","w"))
print(len(pal))
