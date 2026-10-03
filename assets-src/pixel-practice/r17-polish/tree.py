import sys, json, math, random; sys.path.insert(0,"../../../tools/pixel-practice")
from shapes import Canvas
W,H=44,48
pal={"A":"#14240c","S":"#3a4a2e",
 "l1":"#1f4a1c","l2":"#2d6a24","l3":"#44902c","l4":"#68b838","l5":"#96dc54","l6":"#c8f27c",
 "t1":"#2a1a0e","t2":"#4a2c14","t3":"#6a4220","t4":"#8c5c30","t5":"#b0804a"}
def tree(ver):
    random.seed(11)
    c=Canvas(W,H)
    # 地面の影
    for y in range(41,47):
        for x in range(4,42):
            dd=((x+.5-22)/18)**2+((y+.5-44.5)/2.8)**2
            if dd<=1 and (dd<.55 or (x+y)%2==0): c.put(x,y,'S')
    # 幹: 根元が広がり、上で細く、2本の枝が樹冠へ
    for y in range(26,45):
        t=(y-26)/18
        half=2.2+ t*1.2 + (max(0,t-0.8)*9)
        for x in range(int(22-half-1),int(22+half+2)):
            nx=(x+.5-22)/half
            if abs(nx)>1: continue
            lum=-nx*0.9
            k='t5' if lum>0.55 else 't4' if lum>0.1 else 't3' if lum>-0.4 else 't2'
            if abs(nx)>0.86: k='t1' if nx>0 else 't2'
            if ver>=2 and (y*3+x*5)%7==0 and k in ('t4','t3'): k='t3' if k=='t4' else 't2'
            if ver>=2 and nx>-0.6 and nx<0.3 and (y%5==0): k='t2'      # 樹皮の割れ目
            c.put(x,y,k)
    for sgn in (-1,1):                       # 枝
        for i in range(10):
            x=22+sgn*(2+i*0.9); y=28-i*1.2
            c.put(x,y,'t3' if sgn<0 else 't2'); c.put(x,y+1,'t2'); c.put(x+ (0 if sgn<0 else 1),y-1,'t4' if sgn<0 else 't3')
    # 葉の塊（奥→手前の順）
    clumps=[(22,13,11,9),(11,19,8,7),(33,19,8,7),(16,9,8,6),(28,9,8,6),(22,24,12,7),(8,26,6,5),(36,26,6,5),(15,27,7,5),(29,27,7,5)]
    for (cx,cy,rx,ry) in clumps:
        for y in range(int(cy-ry-2),int(cy+ry+3)):
            for x in range(int(cx-rx-2),int(cx+rx+3)):
                ang=math.atan2(y+.5-cy,x+.5-cx)
                bump=1+0.09*math.sin(ang*7+cx)+0.05*math.sin(ang*13+cy)      # 縁をぎざぎざに
                nx=(x+.5-cx)/(rx*bump); ny=(y+.5-cy)/(ry*bump)
                r2=nx*nx+ny*ny
                if r2>1: continue
                z=math.sqrt(1-r2)
                lum=-nx*0.55-ny*0.75+0.5*z
                lum+= (0.1 if (x*5+y*3)%6==0 else 0)
                # 全体の光: 左上の塊ほど明るい
                lum+= (-(cx-22)*0.012-(cy-16)*0.012)
                t=lum-0.18-0.45*max(0,ny)+ (0.0 if ver<4 else 0.0)
                k='l6' if t>1.0 else 'l5' if t>0.72 else 'l4' if t>0.42 else 'l3' if t>0.12 else 'l2' if t>-0.25 else 'l1'
                if r2>0.72 and (nx*0.5+ny)>0.25 and k not in ('l1',): k={'l6':'l4','l5':'l3','l4':'l2','l3':'l1','l2':'l1'}[k]   # 右下の縁は暗い（塊の分離）
                c.put(x,y,k)
    if ver>=2:
        # 葉の房: 明るい側に小さな2〜3ドットの光、暗い側に影の点
        for _ in range(70):
            x=random.randint(6,38); y=random.randint(3,32)
            k=c.get(x,y)
            if k in ('l4','l5'): c.put(x,y,'l6'); c.put(x+1,y,'l5') if c.get(x+1,y) in ('l4','l5') else None
            elif k in ('l2','l3'): c.put(x,y,'l1' if k=='l2' else 'l2')
    c.outline('A',skip=('S',))
    if ver>=3:
        for y in range(H):
            for x in range(W):
                if c.get(x,y)=='A' and c.get(x+1,y+1) in ('l5','l6','l4') and (x+y)<44: c.put(x,y,'l1')       # 明るい側の縁は緑の暗色
    for y in range(H):
        for x in range(W):
            if c.get(x,y)=='S' and not any(c.get(x+dx,y+dy)=='S' for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))): c.put(x,y,'.')
    return c
letters="BCDEFGHIJKLMNOPQRTUVXYZabcdefghijklmnopqrstuvwxyz"
mp={n:(n if n in ("A","S") else letters[i]) for i,n in enumerate(pal)}
for v in (1,2,3,4):
    c=tree(v)
    open(f"tree{v}.txt","w").write("\n".join("".join("." if ch=="." else mp[ch] for ch in r) for r in c.g)+"\n")
json.dump({mp[k]:v for k,v in pal.items()},open("pal-tree.json","w"))
