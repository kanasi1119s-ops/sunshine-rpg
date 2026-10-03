import sys, json, random; sys.path.insert(0,"../../../tools/pixel-practice")
from shapes import Canvas
def hero(ver):
    random.seed(4)
    c=Canvas(32,38)
    # --- 脚・ブーツ
    for x0 in (11,18):
        c.poly([(x0,29),(x0+4,29),(x0+4,34),(x0,34)],lambda x,y:'p' if x<x0+2 else 'P')
        c.poly([(x0-1,33),(x0+5,33),(x0+5,36),(x0-1,36)],lambda x,y:'t' if y==33 else 'u' if x<x0+2 else 'U')
        if ver>=2: c.put(x0,34,'T'); c.put(x0+1,35,'T')
    # --- 胴（チュニック）
    def tunic(x,y):
        lum=-(x-16)*0.07-(y-25)*0.06
        return 'a' if lum>0.25 else 'b' if lum>-0.05 else 'c' if lum>-0.35 else 'd'
    c.poly([(9,20),(23,20),(24,30),(8,30)],tunic)
    if ver>=2:
        for k in range(5): c.put(12+k,22+k//2,'a') if k%2==0 else None
        for y in range(24,30):
            c.put(15+(y%2),y,'c')         # 服のしわ（縦）
    # ベルトとバックル
    for x in range(8,25): c.put(x,26,'e'); c.put(x,27,'E') if ver>=2 else None
    c.put(15,26,'Y'); c.put(16,26,'Y'); c.put(15,27,'y'); c.put(16,27,'y')
    # マフラー（赤）
    c.poly([(9,19),(23,19),(23,22),(9,22)],lambda x,y:'r' if x<16 else 'R')
    if ver>=2:
        c.poly([(20,21),(25,21),(26,28),(22,28)],lambda x,y:'r' if x<24 else 'R')
        for y in range(22,28): c.put(23,y,'R') if y%2 else None
    # 腕と手
    c.poly([(6,20),(9,20),(8,28),(5,28)],lambda x,y:'a' if x<7 else 'b')
    c.poly([(23,20),(26,20),(27,28),(24,28)],lambda x,y:'b' if x<25 else 'c')
    for x in (5,6,7): c.put(x,29,'s'); c.put(x,30,'S')
    for x in (24,25,26): c.put(x,29,'s'); c.put(x,30,'S')
    # --- 頭（大きな丸い顔）
    def face(x,y):
        nx=(x+.5-16)/8.3; ny=(y+.5-13.5)/7.6
        return 'S' if (nx*0.8+ny*0.7)>0.95 or (ny>0.78 and abs(nx)<0.6) else 's'
    c.ellipse(16,13.5,8.3,7.6,face)
    # 頬の紅
    c.put(10,16,'k'); c.put(11,16,'k'); c.put(21,16,'k'); c.put(22,16,'k')
    # 目（幅3×高さ4。虹彩は2段、白い反射）
    for ex in (11,18):
        for dy in range(4):
            for dx in range(3):
                col = 'i' if dy<2 else 'j'
                if dy==0 and ver>=2: col='n'
                c.put(ex+dx,11+dy+1,col)
        if ver>=2: c.put(ex+(0 if ex<16 else 2),12,'W'); c.put(ex+1+(0 if ex<16 else 0),14,'q') if ver>=3 else None
        c.put(ex,11,'N'); c.put(ex+1,11,'N'); c.put(ex+2,11,'N')     # 上まぶた（太い線）
    c.put(16,17,'S')
    c.put(15,18,'m'); c.put(16,18,'m')                                # 口
    # --- 髪（立ち上がる前髪とハイライト）
    def hair(x,y):
        lum=-(x-14)*0.09-(y-6)*0.07
        base='h' if lum>0.15 else 'H' if lum>-0.2 else 'G'
        if ver>=2 and (x*3+y*5)%7==0: base='h' if base=='H' else base
        return base
    c.poly([(7,14),(7,8),(10,4),(16,2),(22,4),(25,8),(25,14),(23,11),(21,9),(18,10),(16,8),(13,10),(11,9),(9,11)],hair)
    for pts in ([(9,4),(7,1),(13,3)],[(15,3),(17,0),(20,3)],[(20,3),(24,1),(24,6)]):
        c.poly(pts,hair)
    if ver>=3:
        for x,y in [(11,5),(12,5),(18,4),(19,4),(10,7),(22,6)]: c.put(x,y,'w')   # 髪のツヤ
        for x,y in [(8,12),(8,13),(24,12),(24,13)]: c.put(x,y,'H')               # もみあげ
    c.outline('A')
    return c
pal={"A":"#2a1a24","s":"#f6d0a8","S":"#dca880","k":"#f0a090","i":"#3a5ab0","j":"#2a3a80","n":"#1a2050","N":"#2a1a24","W":"#ffffff","q":"#8aa8ff","m":"#b05848",
 "h":"#e07838","H":"#b8502a","G":"#8a3a22","w":"#ffd098",
 "a":"#5aa860","b":"#3e8a4c","c":"#2c6a3c","d":"#1e4a2c","e":"#7a4a28","E":"#5a3018","Y":"#f4d060","y":"#c09030",
 "r":"#d8403c","R":"#9a2a30","p":"#6a5a8a","P":"#4a3a6a","t":"#8a5a30","u":"#6a4020","U":"#4a2c14","T":"#3a2010"}
for v in (1,2,3,4): open(f"hero{v}.txt","w").write(str(hero(v))+"\n")
json.dump(pal,open("pal-hero.json","w"))
