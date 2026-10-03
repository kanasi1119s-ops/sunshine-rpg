import sys, json, math, random; sys.path.insert(0,"../../../tools/pixel-practice")
from shapes import Canvas
def apple(ver):
    random.seed(2)
    W,H=34,34
    c=Canvas(W,H)
    # 影（地面）
    for y in range(29,33):
        for x in range(5,29):
            d=((x+.5-17)/12)**2+((y+.5-31)/2.2)**2
            if d<=1 and (d<0.5 or (x+y)%2==0): c.put(x,y,'S')
    # 林檎の形: 上が2つのふくらみ、下はやや細い。signed distance 風に左右2つの円＋中央の円を合成
    def inside(x,y):
        a=((x+.5-11.5)/8.6)**2+((y+.5-18)/9.6)**2
        b=((x+.5-22.5)/8.6)**2+((y+.5-18)/9.6)**2
        m=((x+.5-17)/9.8)**2+((y+.5-20)/9.4)**2
        dip = (y<13 and abs(x+.5-17)<(1.3+(13-y)*0.18 if ver<4 else 0.9+(12-y)*0.12))
        return (a<=1 or b<=1 or m<=1) and not dip
    ramp=['1','2','3','4','5','6','7']
    for y in range(H):
        for x in range(W):
            if not inside(x,y): continue
            nx=(x+.5-17)/11.5; ny=(y+.5-19)/10.5
            r2=nx*nx+ny*ny
            z=math.sqrt(max(0,1-min(1,r2)))
            L=(-0.55*nx-0.65*ny+0.55*z)          # 光（左上手前）
            bounce=max(0,(nx*0.5+ny*0.6)-0.55)*0.5 # 右下の照り返し（暗部を少し持ち上げる）
            v=L+bounce
            t=(v+0.35)/1.3*7
            if ver==4:
                frac=t-math.floor(t)
                if frac>0.8 and (x+y)%2==0: t+=1
            if 2<=ver<4:
                # 段の境目に市松ディザ
                frac=t-math.floor(t)
                if frac>0.62 and (x+y)%2==0: t+=1
                if frac<0.18 and (x+y)%2==1: t-=1
            idx=int(max(0,min(6,math.floor(t))))
            # 縦の縞（林檎の模様）をうっすら
            if ver>=3 and (x*7+y)%9==0 and idx>1: idx-=1
            c.put(x,y,ramp[idx])
    # 照り（鏡面）: 左上に楕円の白い塊
    for x,y in [(9,10),(10,10),(8,11),(9,11),(8,12),(9,12),(8,13)]: c.put(x,y,'W')
    if ver>=2:
        for x,y in [(11,9),(12,9),(7,14)]: c.put(x,y,'w')
    # ヘタ（くぼみの暗さ）と軸
    for y in range(7,13):
        c.put(17,y,'T'); 
        if y>8: c.put(16,y,'t')
    c.put(17,12,'D'); c.put(16,12,'D'); c.put(18,12,'D')
    # 葉（3段＋葉脈）
    leaf=[(18,7),(19,6),(20,5),(21,5),(22,5),(23,6),(23,7),(22,8),(21,9),(20,9),(19,8)]
    c.poly(leaf,lambda x,y:'f' if (x+y)<27 else 'F' if (x+y)<29 else 'G')
    if ver>=2:
        for k in range(5): c.put(19+k,8-k//2,'V') if k%1==0 else None
    c.outline('A',skip=('S',))
    # 縁取りを、明るい側では少し明るい赤茶に（selective outline）
    if ver>=3:
        for y in range(H):
            for x in range(W):
                if c.get(x,y)=='A' and x+y<22 and c.get(x+1,y+1) in '4567': c.put(x,y,'B')
    for y in range(H):
        for x in range(W):
            if c.get(x,y)=='S' and not any(c.get(x+dx,y+dy)=='S' for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): c.put(x,y,'.')
    return c
pal={"A":"#2a0e14","B":"#5a1a20","1":"#6a1428","2":"#901c30","3":"#bc2c3a","4":"#dc4642","5":"#f06a4c","6":"#ff9660","7":"#ffc47c","W":"#fff8e8","w":"#ffd8b0",
     "T":"#6a4020","t":"#8a5c30","D":"#3a1a10","f":"#7ad060","F":"#4aa048","G":"#2c7040","V":"#b4f090","S":"#3a2a46"}
for v in (1,2,3,4): open(f"apple{v}.txt","w").write(str(apple(v))+"\n")
json.dump(pal,open("pal-apple.json","w"))
