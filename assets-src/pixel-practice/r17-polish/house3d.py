"""斜め上から見た家の生成器（正面の壁＋奥へ引く側面の壁＋2面の屋根）。パラメータで小屋（1階）から屋敷（2階）まで作る。"""
import sys, json, math, random; sys.path.insert(0,"../../../tools/pixel-practice")
from shapes import Canvas
SL=0.45
pal={"A":"#1e1620","S":"#3c3050",
 "R1":"#4a1820","R2":"#7a2a2c","R3":"#a8402e","R4":"#cc5c3c","R5":"#ec8452","R6":"#ffb078",
 "P1":"#b49c78","P2":"#e8d8b4","P3":"#f8f0d8","Q":"#c4ae88",
 "B2":"#5c3a1c","B3":"#845428",
 "K1":"#585468","K2":"#807c94","K3":"#aaa8bc",
 "D1":"#4a2a14","D2":"#7a4a22","D3":"#a8703a",
 "G1":"#7ab8e0","G2":"#aee0f8","F1":"#3a8a3a","F2":"#68c048","F3":"#e84a5a","Y":"#f4cc50",
 "M1":"#4a7a38","M2":"#6a9a48","CUR":"#d86a5a","L1":"#ffe8a0","W1":"#c4905a","W2":"#a8703a"}
def build(W,H,FW,SW,floors,FH=18,roofH=16,ox=3,door=0.5,nwin=3,porch=True,dormer=False,wall='plaster',chimney=0.7,seed=1,ivy=True,roof=None,fullside=False):
    rnd=random.Random(seed)
    c=Canvas(W,H)
    x0=ox; x1=ox+FW; x2=x1+SW
    bot=H-9; top=bot-floors*FH
    def sideY(x,y): return int(round(y-(x-x1)*SL))
    base=[('R6','R5','R4','R3','R2'),('R5','R4','R3','R2','R1')]
    if roof: base=roof
    # 地面の影（右奥へ）
    for y in range(bot+1,H):
        for x in range(x0+3,W):
            if y>=bot+1-int(max(0,x-x1)*SL)+3 and ((x+y)%2==0 or y<H-2): c.put(x,y,'S')
    # 側面の壁
    for x in range(x1,x2):
        for y in range(sideY(x,top),sideY(x,bot)+1):
            if wall=='stone':
                row=(y-sideY(x,top))//4; off=(row%2)*4
                k='K2' if (x+off)%8<7 else 'K1'
                if (x-x1)<6: k='K3' if k=='K2' else 'K2'
            elif wall=='wood':
                k='W2' if (x-x1)%4 else 'B2'
            else:
                k='Q' if x<x1+8 else 'P1'
            if y<=sideY(x,top)+2 and wall!='stone': k='P1' if wall=='plaster' else 'B2'
            if wall=='plaster' and (x*5+y*3)%31==0: k='P1'
            c.put(x,y,k)
    # 正面の壁
    for y in range(top,bot+1):
        for x in range(x0,x1+1):
            if wall=='stone':
                row=(y-top)//4; off=(row%2)*4
                k='K3' if (x+off)%8<7 else 'K2'
                if (y-top)%4==3 and True: k='K2'
                if rnd.random()<0.06: k='K2' if k=='K3' else 'K3'
            elif wall=='wood':
                k='W1' if (x-x0)%4 else 'W2'
                if (y*3+x)%17==0: k='W2'
            else:
                k='P3' if x<x0+FW*0.5 else 'P2'
                if y<=top+1: k='P2' if k=='P3' else 'Q'
                if (x*7+y*3)%29==0: k='P2' if k=='P3' else 'Q'
            c.put(x,y,k)
    # 土台
    for y in range(bot+1,bot+7):
        for x in range(x0-1,x1+2):
            row=y-bot-1; off=(row%2)*3
            k='K3' if row==0 else 'K2'
            if (x+off)%6==5 or row==5: k='K1'
            elif (x+off)%6==0 and row>0: k='K3'
            c.put(x,y,k)
    for x in range(x1+2,x2):
        yb=sideY(x,bot)
        for y in range(yb+1,yb+7):
            row=y-yb-1; k='K2' if row<2 else 'K1'
            if (x+row*3)%6==5: k='K1'
            c.put(x,y,k)
    # 梁（漆喰の家のみ）
    if wall=='plaster':
        xs=[x0, x1-1]+[x0+int(FW*f) for f in (0.33,0.66)]
        for x in xs:
            for y in range(top,bot+1): c.put(x,y,'B3'); c.put(x+1,y,'B2')
        for f in range(floors+1):
            y=top+f*FH if f<floors else bot-1
            for x in range(x0,x1+1): c.put(x,y,'B3'); c.put(x,y+1,'B2')
        for x in range(x1,x2):
            for f in range(floors+1):
                y=top+f*FH if f<floors else bot-1
                c.put(x,sideY(x,y),'B2')
        for xx in (x1+SW//2,):
            for y in range(sideY(xx,top),sideY(xx,bot)+1): c.put(xx,y,'B2')
        if floors>=2:
            for k in range(FH-6): c.put(x0+1+k,top+FH-3-k,'B3'); c.put(x0+2+k,top+FH-3-k,'B2')
    # 窓
    def window(wx,wy,w,h):
        for y in range(wy,wy+h):
            for x in range(wx,wx+w): c.put(x,y,'G1' if (x+y)%7 else 'G2')
        for x in range(wx-1,wx+w+1): c.put(x,wy-1,'B3'); c.put(x,wy+h,'B2')
        for y in range(wy-1,wy+h+1): c.put(wx-1,y,'B3'); c.put(wx+w,y,'B2')
        for y in range(wy,wy+h): c.put(wx+w//2,y,'B2')
        for x in range(wx,wx+w): c.put(x,wy+h//2,'B2')
        c.put(wx+1,wy+1,'G2'); c.put(wx+2,wy+2,'G2')
        for y in range(wy,wy+3):
            for x in (wx,wx+w-1):
                if c.get(x,y) in ('G1','G2'): c.put(x,y,'CUR')
    def sidewin(sx,w,ytop,h):
        for dx in range(w):
            x=sx+dx; yt=sideY(x,ytop)
            for y in range(yt,yt+h): c.put(x,y,'G1' if (dx+y)%7 else 'G2')
            c.put(x,yt-1,'B2'); c.put(x,yt+h,'B2')
        for y in range(sideY(sx,ytop)-1,sideY(sx,ytop)+h+1): c.put(sx-1,y,'B2')
    doorx=x0+int(FW*door)
    # 正面の窓（ドアの位置を避ける）
    for fl in range(floors):
        wy=top+fl*FH+4; wh=FH-9
        slots=[x0+int(FW*(i+0.5)/nwin)-3 for i in range(nwin)]
        for sx in slots:
            if fl==floors-1 and abs((sx+3)-doorx)<9 and True and floors==1: continue
            if fl==floors-1 and abs((sx+3)-doorx)<9: continue
            window(sx,wy,7,wh)
            if fl==floors-1:
                for xx in range(sx-2,sx+10): c.put(xx,wy+wh+1,'B2'); c.put(xx,wy+wh+2,'B3')
                for xx in range(sx-1,sx+9): c.put(xx,wy+wh,'F1'); 
                for xx in (sx,sx+3,sx+6): c.put(xx,wy+wh-1,'F3')
        if fl==0 and floors==2:
            pass
        sidewin(x1+3,7,top+fl*FH+4-int(3*SL),FH-9)
    # 玄関
    dh=min(FH-4,13)
    for y in range(bot-dh,bot+1):
        for x in range(doorx-5,doorx+6):
            tp=bot-dh+(2 if abs(x-doorx)==5 else 1 if abs(x-doorx)==4 else 0)
            if y<tp: continue
            k='D3' if x<doorx else 'D2'
            if (x-doorx+5)%3==2: k='D1'
            c.put(x,y,k)
    for y in range(bot-dh,bot+1): c.put(doorx,y,'D1')
    c.put(doorx-2,bot-4,'Y'); c.put(doorx+2,bot-4,'Y')
    for x in range(doorx-7,doorx+8): c.put(x,bot+1,'K3'); c.put(x,bot+2,'K2')
    # ポーチの庇と柱
    if porch:
        py=bot-dh-4
        for x in range(doorx-9,doorx+10):
            for k in range(3): c.put(x,py+k,'R5' if k==0 else 'R4' if k==1 else 'R3')
            c.put(x,py+3,'R1')
        for px in (doorx-8,doorx+7):
            for y in range(py+4,bot+1): c.put(px,y,'B3'); c.put(px+1,y,'B2')
        for y in range(py+4,py+8):
            for x in range(doorx-6,doorx+6):
                if c.get(x,y) in ('P3','P2','Q'): c.put(x,y,'Q')
    # 屋根
    rl=x0+roofH*0.55; rr=x1-roofH*0.5
    ridge_y=top-roofH
    def jit(row,cid):
        h=(row*7919+cid*104729)%11
        return 1 if h<2 else -1 if h>8 else 0
    def front_roof(x,y):
        row=(y-ridge_y)//3; ly=(y-ridge_y)%3; off=2 if row%2 else 0
        cell=(x+off)%4; cid=(x+off)//4; pal_=base[0]
        if cell==3: return pal_[4]
        if ly==0: return pal_[0] if row%2==0 else pal_[1]
        if ly==2: return pal_[3]
        return pal_[max(1,min(3,2+jit(row,cid)))]
    def side_roof(x,y):
        yy=y+(x-x1)*SL
        row=int((yy-ridge_y)//3); ly=int((yy-ridge_y)%3); off=2 if row%2 else 0
        cell=(x+off)%4; cid=(x+off)//4; pal_=base[1]
        if cell==3: return pal_[3]
        if ly==0: return pal_[1]
        if ly==2: return pal_[3]
        return pal_[max(1,min(3,2+jit(row,cid)))]
    c.poly([(x0-4,top),(rl,ridge_y+1),(rr,ridge_y+1),(x1+4,top)],front_roof)
    far_eave=top-(x2+2-x1)*SL
    if fullside:
        # 側面の屋根を、奥（右）まで厚みを保って伸ばす（右端が薄い帯になって足りなく見えた）
        far_top=min(ridge_y+1, far_eave-roofH*0.6)
        c.poly([(rr,ridge_y+1),(x1+4,top),(x2+2,far_eave),(x2+2,far_top),(rr+SW*0.5,(ridge_y+1+far_top)/2)],side_roof)
        for x in range(int(rr+SW*0.5),x2+3):
            yy=(ridge_y+1+far_top)/2+(x-(rr+SW*0.5))*(far_top-(ridge_y+1+far_top)/2)/max(1,(x2+2-(rr+SW*0.5)))
            c.put(x,int(round(yy)),'R6')
    else:
        c.poly([(rr,ridge_y+1),(x1+4,top),(x2+2,far_eave),(rr+SW*0.8+4,ridge_y+SW*0.8*0.45+3)],side_roof)
    for x in range(int(rl),int(rr)+1): c.put(x,ridge_y,'R6'); c.put(x,ridge_y+1,'R5')
    for y in range(ridge_y+1,top):
        x=rr+(y-ridge_y)*((x1+4)-rr)/(top-ridge_y); c.put(x,y,'R6'); c.put(x+1,y,'R5')
    for x in range(x0-4,x1+5): c.put(x,top,'R1'); c.put(x,top+1,'R1') if x%2 else None
    for x in range(x1+4,x2+3): yy=top-(x-x1)*SL; c.put(x,int(round(yy)),'R1')
    # 屋根窓
    if dormer:
        cx=x0+int(FW*0.5); dy=top-4
        c.poly([(cx-6,dy),(cx-6,dy-9),(cx,dy-14),(cx+6,dy-9),(cx+6,dy)],lambda x,y:'P3' if x<cx else 'P2')
        for y in range(dy-8,dy-1):
            for x in range(cx-3,cx+4): c.put(x,y,'G1' if (x+y)%6 else 'G2')
        for x in range(cx-4,cx+5): c.put(x,dy-9,'B3'); c.put(x,dy-1,'B2')
        for y in range(dy-9,dy): c.put(cx-4,y,'B3'); c.put(cx+4,y,'B2'); c.put(cx,y,'B2')
        for k in range(7): c.put(cx-6+k,dy-9-k if k<6 else dy-15,'R5'); c.put(cx+6-k,dy-9-k,'R3')
    # 煙突
    chx=int(x0+FW*chimney)
    c.poly([(chx-3,ridge_y-6),(chx+3,ridge_y-6),(chx+3,ridge_y+8),(chx-3,ridge_y+8)],lambda x,y:'K3' if x<chx else 'K2' if (x+y)%5 else 'K1')
    for x in range(chx-4,chx+5): c.put(x,ridge_y-7,'K2'); c.put(x,ridge_y-6,'K1')
    # 写実の追加: 屋根のコケ、しみ、ひび、つた、草、樽
    for _ in range(int(FW*0.5)):
        x=rnd.randint(x0,x1); y=rnd.randint(top-6,top-1)
        if c.get(x,y) in ('R3','R4','R5','R2'): c.put(x,y,'M2'); c.put(x+1,y,'M1') if rnd.random()<0.6 else None
    for xx in [x0+int(FW*f) for f in (0.2,0.5,0.8)]:
        for k in range(rnd.randint(3,6)):
            y=top+14+k
            if c.get(xx,y) in ('P3','P2'): c.put(xx,y,'P1')
    for _ in range(4):
        x=rnd.randint(x0+3,x1-4); y=rnd.randint(top+4,bot-3)
        if c.get(x,y) in ('P3','P2'):
            for k in range(3): c.put(x+k,y+k,'B2') if c.get(x+k,y+k) in ('P3','P2') else None
    if ivy:
        for t in range(0,int(floors*FH*1.2)):
            x=x0+1+int(1.6*math.sin(t*0.55)); y=bot-t*0.85
            c.put(int(x),int(y),'F1')
            if t%3==0: c.put(int(x)+1,int(y)-1,'F2'); c.put(int(x)-1,int(y),'F2')
    c.outline('A',skip=('S',))
    # 草（土台の足元）・飛び石・樽
    for x in range(x0-2,x2):
        yb=(bot+7) if x<=x1 else sideY(x,bot)+7
        if rnd.random()<0.55:
            h=rnd.randint(1,3)
            for k in range(h): c.put(x,yb-k,'F1' if k==0 else 'F2')
    for i,(dx,dy) in enumerate(((0,3),(4,4),(1,5),(5,6))):
        if bot+dy+2<H:
            for k in range(3): c.put(doorx-2+dx+k,bot+dy,'K3'); c.put(doorx-2+dx+k,bot+dy+1,'K2')
    for dy in range(8):
        for dx in range(6): c.put(x1+SW-4+dx,bot-2+dy,'W1' if dx<3 else 'W2') if floors>=1 and False else None
    for y in range(H):
        for x in range(W):
            if c.get(x,y)=='S' and not any(c.get(x+dx,y+dy)=='S' for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): c.put(x,y,'.')
    return c
letters="BCDEFGHIJKLMNOPQRTUVXYZabcdefghijklmnopqrstuvwxyz0123456789"
names=list(pal); mp={n:(n if n in ("A","S") else letters[i]) for i,n in enumerate(names)}
def save(name,c,palette=None):
    open(name+".txt","w").write("\n".join("".join("." if ch=="." else mp[ch] for ch in r) for r in c.g)+"\n")
    p={mp[k]:v for k,v in (palette or pal).items()}
    json.dump(p,open("pal-"+name+".json","w"))
BLUE={"R1":"#1c2850","R2":"#2c4a88","R3":"#3a64b0","R4":"#4e80d0","R5":"#78a8ec","R6":"#a8ccff"}
GREEN={"R1":"#183a28","R2":"#2a6040","R3":"#3a8a52","R4":"#52aa66","R5":"#80d090","R6":"#b0f0b8"}
def variants(name,c):
    save(name,c)
    for nm,vv in (("blue",BLUE),("green",GREEN)):
        save(name+"-"+nm,c,{**pal,**vv})
if __name__=="__main__":
    variants("cottage",build(48,56,FW=30,SW=11,floors=1,FH=19,roofH=15,ox=3,door=0.5,nwin=3,porch=False,wall='plaster',chimney=0.75,seed=3))
    variants("manor4",build(80,80,FW=54,SW=19,floors=2,FH=18,roofH=17,ox=3,door=0.45,nwin=3,porch=True,dormer=True,wall='plaster',chimney=0.8,seed=8,fullside=True))
    variants("stonehouse",build(64,64,FW=40,SW=15,floors=1,FH=22,roofH=17,ox=3,door=0.35,nwin=2,porch=False,wall='stone',chimney=0.7,seed=6))
