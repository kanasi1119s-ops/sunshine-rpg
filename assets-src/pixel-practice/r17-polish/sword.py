import sys, json; sys.path.insert(0,"../../../tools/pixel-practice")
from shapes import Canvas
def sword(ver):
    c=Canvas(40,40)
    W=9
    # 刃: 45度。行yごとに x=y+a .. y+a+W-1。先端は細くなる
    a=-4
    for y in range(1,30):
        taper = 0
        if y<7: taper=(7-y)           # 先端: 上ほど細い
        x0=y+a+ (taper//2); x1=y+a+W-1-(taper-taper//2)
        for x in range(x0,x1+1):
            i=x-(y+a)               # 刃の幅方向の位置 0..8
            edge_l = (i==0+taper//2)
            k = {0:'1',1:'2',2:'3',3:'3',4:'f',5:'4',6:'4',7:'5',8:'6'}.get(min(8,max(0,i)),'4')
            if x+y<=19+27+1: c.put(x,y,k)           # 鍔の線より先（右下）は刃を出さない
    # 刃の細部（版が上がるほど増える）
    if ver>=2:
        for y in range(8,25):                       # 溝（フラー）の内側に細い明線
            c.put(y-4+5,y,'g') if y%3==0 else None
        for y in range(9,26,4):                     # 刃こぼれ・傷のような短い暗点
            c.put(y-4+7,y,'6')
        for y in range(3,10): c.put(y-4+1,y,'W')      # 切っ先の白い光（左の縁）
    if ver>=3:
        for y in range(10,26,2): c.put(y-4+2,y,'W') if y%4==0 else None   # 研いだ縁のきらめき
        c.put(3,2,'W'); c.put(4,3,'W')
    # 鍔（刃に直角、反り返る）
    def bar(cx,cy,half,w,fn):
        for t in range(-half,half+1):
            for k in range(w):
                c.put(cx+t+(k//2), cy-t+(k-(k//2)), fn(t,k))
    gx,gy=19,27
    bar(gx,gy,9,4,lambda t,k:'Y' if (k==0 and t%3==0) else 'G' if k==0 else 'O' if k in (1,2) else 'D')
    if ver>=2:
        for t in (-9,-8,9,8): c.put(gx+t,gy-t-1,'G'); c.put(gx+t,gy-t-2,'O')       # 鍔の先端を少し反らせる
        c.put(gx,gy,'B'); c.put(gx+1,gy,'B'); c.put(gx,gy+1,'b'); c.put(gx+1,gy+1,'b'); c.put(gx-1,gy,'b'); c.put(gx+2,gy,'b') if False else None   # 中央の宝石
    if ver>=3:
        c.put(gx-1,gy,'Y'); c.put(gx,gy-1,'Y'); c.put(gx+1,gy+1,'D')
        for t in (-5,-3,3,5): c.put(gx+t,gy-t,'Y')
    # 柄（細く、巻き革の縞）
    for t in range(1,8):
        x=gx+t+1; y=gy+t+1
        for k in (-1,0,1):
            kk='L' if (t%2==0) else 'l'
            if k==-1: kk='M' if t%2==0 else 'L'
            if k==1: kk='l' if t%2==0 else 'N'
            c.put(x+k,y-k,kk)
            if ver>=2: c.put(x+k+1,y-k,kk)
    # 柄頭
    px,py=gx+10,gy+10
    for dx in range(-2,3):
        for dy in range(-2,3):
            if dx*dx+dy*dy<=5: c.put(px+dx,py+dy,'G' if dx+dy<0 else 'D' if dx+dy>1 else 'O')
    if ver>=3: c.put(px-1,py-1,'Y')
    c.outline('A')
    # 落ち影
    if ver>=3:
        for t in range(0,12): 
            c.put(8+t,31+t//3,'S') if c.get(8+t,31+t//3)=='.' and t%2==0 else None
    return c
pal={"A":"#1a1a26","W":"#ffffff","1":"#f4f6fc","2":"#d8deee","3":"#b4bdd6","g":"#e8ecf8","f":"#7b86a8","4":"#8e9ac0","5":"#6a7698","6":"#4e5878",
     "G":"#f0c050","O":"#c88a2c","D":"#8a5418","Y":"#fff0a8","B":"#4a8af0","b":"#2a5ac0","L":"#9a5a2c","l":"#7a4220","M":"#b8743c","N":"#5a3018","S":"#3a3050"}
for v in (1,2,3,4):
    open(f"sword{v}.txt","w").write(str(sword(v))+"\n")
json.dump(pal,open("pal-sword.json","w"))
