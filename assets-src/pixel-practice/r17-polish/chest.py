import sys, json, math; sys.path.insert(0,"../../../tools/pixel-practice")
from shapes import Canvas
W,H=40,34
pal={"A":"#1e1210","S":"#3a2a46","W":"#fff4d8",
 "w1":"#3a1c10","w2":"#5a2c14","w3":"#7e4220","w4":"#a05a2c","w5":"#c47a3c","w6":"#e49c58",
 "m1":"#4a5272","m2":"#6a7494","m3":"#9aa4be","m4":"#c4cce0","m5":"#eef2fa",
 "g1":"#a86a18","g2":"#e0a030","g3":"#ffd860","k":"#2a1608"}
def chest(open_):
    c=Canvas(W,H)
    for y in range(H-4,H):
        for x in range(4,36):
            dd=((x+.5-20)/16)**2+((y+.5-(H-2))/1.8)**2
            if dd<=1 and (dd<.55 or (x+y)%2==0): c.put(x,y,'S')
    # 前面（板）: 4段の横板。各板の上端が明るく、下端が暗い
    top,bot=15,30
    for y in range(top,bot+1):
        row=(y-top)//4; ry=(y-top)%4
        for x in range(4,36):
            lum=-(x-20)*0.012
            base=['w5','w4','w4','w3'][row] if True else 'w4'
            if x>=28: base={'w5':'w4','w4':'w3','w3':'w2'}.get(base,base)   # 右側は影
            k=base
            if ry==0: k={'w5':'w6','w4':'w5','w3':'w4','w2':'w3'}[base]     # 板の上端の光
            if ry==3 and row<3: k={'w5':'w4','w4':'w3','w3':'w2','w2':'w1','w6':'w5'}[base]   # 下端の影
            # 木目（短い線）
            if ry in (1,2) and (x*5+row*7)%17==0: k={'w5':'w4','w4':'w3','w3':'w2','w2':'w1'}.get(k,k)
            c.put(x,y,k)
    # ふた: 円筒（上が丸い）。y=7..14 を縦に円筒シェーディング
    lid_top=5
    for y in range(lid_top,top):
        t=(y-lid_top)/(top-lid_top-1)         # 0=上 1=下
        for x in range(4,36):
            edge=min(x-4,35-x)
            if edge<(1-math.sqrt(max(0,1-(1-t)**2)))*5: continue    # 角を丸める
            lum=0.9-t*1.5 - (x-20)*0.012
            k='w6' if lum>0.7 else 'w5' if lum>0.3 else 'w4' if lum>-0.1 else 'w3' if lum>-0.5 else 'w2'
            if x>=28 and k in ('w6','w5','w4','w3'): k={'w6':'w5','w5':'w4','w4':'w3','w3':'w2'}[k]
            if (x*3+y*5)%13==0 and k in ('w4','w5'): k='w3' if k=='w4' else 'w4'
            c.put(x,y,k)
    if open_:
        # 開いたふた: 本体の上に、中の暗がりと金貨の山
        for y in range(lid_top,top):
            for x in range(4,36): c.put(x,y,'.')
        c.poly([(6,3),(34,3),(35,9),(5,9)],lambda x,y:'w3' if y<5 else 'w2')
        c.poly([(8,5),(32,5),(33,9),(7,9)],lambda x,y:'k')
        c.poly([(5,10),(35,10),(34,15),(6,15)],lambda x,y:'w2')
        c.poly([(7,11),(33,11),(32,15),(8,15)],lambda x,y:'g1' if y>13 else 'g2')
        for x,y in [(10,12),(14,11),(18,12),(23,11),(27,12),(30,11),(16,13),(25,13)]: c.put(x,y,'g3'); c.put(x+1,y,'g2')
        c.put(12,11,'W'); c.put(24,12,'W')
    # 金具: 縦の帯2本（円筒の明暗）、横の帯、四隅の鋲
    for bx in (9,28):
        for y in range(lid_top if not open_ else 3,bot+1):
            if open_ and 9<y<15: continue
            for i,k in enumerate(['m2','m4','m5','m3','m2']):
                x=bx+i
                if y>=top and False: pass
                kk=k
                if x>=28: kk={'m5':'m4','m4':'m3','m3':'m2','m2':'m1'}[k]
                c.put(x,y,kk)
    for x in range(4,36): c.put(x,top,'m3' if x<28 else 'm2'); c.put(x,top+1,'m2' if x<28 else 'm1')
    for x,y in [(11,18),(30,18),(11,27),(30,27)]: c.put(x,y,'m5'); c.put(x+1,y,'m2')
    # 錠前（金）と鍵穴
    for y in range(top-1,top+9):
        for x in range(17,24):
            k='g3' if (x<19 and y<top+3) else 'g2' if x<22 else 'g1'
            c.put(x,y,k)
    c.put(20,top+3,'k'); c.put(20,top+4,'k'); c.put(19,top+3,'k'); c.put(21,top+3,'k'); c.put(20,top+5,'k')
    c.put(18,top,'W')
    c.outline('A',skip=('S',))
    for y in range(H):
        for x in range(W):
            if c.get(x,y)=='S' and not any(c.get(x+dx,y+dy)=='S' for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): c.put(x,y,'.')
    return c
letters="BCDEFGHIJKLMNOPQRTUVXYZabcdefghijklmnopqrstuvwxyz"
mp={n:(n if n in ("A","S","W") else letters[i]) for i,n in enumerate(pal)}
for name,o in (("chest-closed",False),("chest-open",True)):
    c=chest(o)
    open(name+"-v2.txt","w").write("\n".join("".join("." if ch=="." else mp[ch] for ch in r) for r in c.g)+"\n")
json.dump({mp[k]:v for k,v in pal.items()},open("pal-chest.json","w"))
