import sys, json, math, random
sys.path.insert(0,".")
from chargen import *
from yuri import ramps, fixed, EDGE
def yuri(ver=2):
    W,H=64,104
    im=Img(W,H)
    # --- 脚（長め）とブーツ
    for sx,hx,kx,ax in ((-1,28.5,27.5,27),(1,35.5,36.5,37.5)):
        n='L' if sx<0 else 'R'
        capsule(im,(hx,66),(kx,81),4.6,3.8,'pants','leg'+n,bulge=0.3)
        capsule(im,(kx,81),(ax,95),3.8,3.0,'pants','leg2'+n)
    poly(im,[(22.5,91),(30.5,91),(31.5,98),(33.5,101),(21,101),(21.5,96)],'boots','bootL')
    poly(im,[(33.5,91),(41.5,91),(42.5,96),(43,101),(30.5,101),(32.5,98)],'boots','bootR')
    for x in range(21,34): im.set(x,101,'boots',-1.0,'bootL')
    for x in range(31,44): im.set(x,101,'boots',-1.0,'bootR')
    for x in range(23,31): im.set(x,92,'leather',0.6,'cuffL'); im.set(x,93,'leather',-0.2,'cuffL')
    for x in range(34,42): im.set(x,92,'leather',0.6,'cuffR'); im.set(x,93,'leather',-0.2,'cuffR')
    # --- 右腕（奥）
    capsule(im,(40.5,43),(44,56),3.5,3.0,'jacket','armR',bulge=0.4)
    capsule(im,(44,56),(42.5,66),3.0,2.6,'jacket','armR2')
    ellipse(im,42.5,68.5,3.0,3.0,'skin','handR')
    # --- 胴（ジャケット: 肩が細く、腰で絞り、裾が広がる）
    poly(im,[(23,41),(41,41),(41.5,52),(40,64),(24,64),(22.5,52)],'jacket','torso',shade=lambda x,y,nx,ny:(nx*LIGHT[0]+ny*LIGHT[1])*-0.7+0.28)
    poly(im,[(24,63),(40,63),(44,72),(20,72)],'jacket','skirt',shade=lambda x,y,nx,ny:(nx*LIGHT[0])*-0.6+0.12)
    # 裾のひだ（縦の暗い線）
    for x,y0,y1 in ((26,66,72),(30,65,72),(35,65,72),(39,66,72)): 
        for y in range(y0,y1): im.set(x,y,'jacketD',-1.0,'skirt')
    # シャツ（胸元）
    poly(im,[(29.5,41),(34.5,41),(34,54),(30,54)],'shirt','shirt')
    # ジャケットの前を留める紐（斜め）
    for k in range(5): im.set(30+k//2,45+k*2,'leather',0.2,'shirt'); im.set(34-k//2,45+k*2,'leather',0.2,'shirt')
    # ベルト・バックル・ポーチ
    poly(im,[(22,60),(42,60),(42,63.5),(22,63.5)],'leather','belt',shade=lambda x,y,nx,ny:(ny*-0.5+0.3))
    ellipse(im,32,61.7,2.6,2.2,'gold','buckle')
    poly(im,[(35.5,63),(42,63),(42,70),(35.5,70)],'leather','pouch')
    for x,y,l in ((38,66,0.8),(39,66,0.8),(38,67,0.2)): im.set(x,y,'gold',l,'pouch')
    # --- 左腕（手前）
    capsule(im,(23.5,43),(19.5,56),3.5,3.0,'jacket','armL',bulge=0.4)
    capsule(im,(19.5,56),(21,66),3.0,2.6,'jacket','armL2')
    poly(im,[(17.5,63),(24.5,63),(24.5,66.5),(17.5,66.5)],'cuff','cuffA')
    poly(im,[(39,63),(46,63),(46,66.5),(39,66.5)],'cuff','cuffB')
    ellipse(im,21,69,3.0,3.0,'skin','handL')
    ellipse(im,42.5,65,3.3,1.6,'gold','brace'); ellipse(im,42.5,65.4,1.3,1.3,'glow','gem')
    # --- 首・スカーフ
    capsule(im,(32,33),(32,41),3.2,3.6,'skin','neck')
    poly(im,[(24.5,37),(39.5,37),(41,42),(32,47),(23,42)],'scarf','scarf')
    poly(im,[(33,43),(39,43),(40,57),(36,60),(33,55)],'scarf','scarfTail')
    for k in range(5): im.set(35+(k%2),46+k*2,'scarfD',-1.0,'scarfTail')
    poly(im,[(23,39),(29,38),(30,45),(24.5,46)],'jacketD','collarL')
    poly(im,[(41,39),(35,38),(34,45),(39.5,46)],'jacketD','collarR')
    # --- 頭
    ellipse(im,32,24,10.6,11.4,'skin','head',light_bias=0.15)
    ellipse(im,21.6,25.5,1.7,2.4,'skin','earL'); ellipse(im,42.4,25.5,1.7,2.4,'skin','earR')
    # --- 髪: 1つの大きな塊（先がとがるぎざぎざの輪郭）＋房の筋＋左上のツヤ
    outer=[(21,27),(19.5,19),(11.5,17.5),(17.5,14),(9.5,9),(19,10.5),(14.5,2.5),(24,8),(25,1.5),(29.5,7),(33,0.5),(36,7),(41,1.5),(40.5,8),(49.5,2.5),(45,10.5),(54.5,9),(46.5,14),(52.5,17.5),(44.5,19),(43,27)]
    inner=[(41.5,21),(40,26.5),(37,19.5),(34.5,25),(32,18.5),(29,24.5),(26.5,19),(24.5,27),(22,21)]
    cx,cy=32,17
    def hairshade(x,y,nx,ny):
        th=math.atan2(y+.5-cy,x+.5-cx); r=math.hypot(x+.5-cx,y+.5-cy)
        stripe=math.sin(th*7.0+r*0.15)*0.22
        base=-(nx*LIGHT[0]+ny*LIGHT[1])*0.5+0.18
        d=math.hypot((x+.5-26)/9,(y+.5-8)/6)
        shine=0.6*max(0,1-d)
        return base+stripe+shine
    poly(im,outer+inner,'hair','hairMass',shade=hairshade)
    # 房の根元から先へ向かう暗い筋
    notches=[(17.5,14),(19,10.5),(24,8),(29.5,7),(36,7),(40.5,8),(45,10.5),(46.5,14)]
    for (nx_,ny_) in notches:
        dx,dy=cx-nx_,cy-ny_; L=math.hypot(dx,dy)
        for t in range(0,7):
            x=nx_+dx/L*t; y=ny_+dy/L*t
            if im.part[int(y)][int(x)]=='hairMass': im.set(int(x),int(y),'hair',-1.0,'hairMass')
    # ヘッドバンド（前髪の根元をぐるり）
    poly(im,[(20.5,16.5),(43.5,16.5),(44,19.5),(20,19.5)],'band','band',shade=lambda x,y,nx,ny:(ny*-0.4+0.3))
    for k in range(3): im.set(40+k,18,'bandD',-1.0,'band')
    # 前髪（バンドの上に3房がかかる）
    poly(im,[(22,19),(29,17.5),(27.5,25),(24.5,27.5),(21.5,23)],'hair','fringeL',shade=hairshade)
    poly(im,[(42,19),(35,17.5),(36.5,22),(39.5,26.5),(42.5,23)],'hair','fringeR',shade=hairshade)
    poly(im,[(29,17.5),(35,17.5),(34,24),(31,24)],'hair','fringeM',shade=hairshade)
    # --- 顔
    for ex,sign in ((26.8,1),(37.2,-1)):
        for dy in range(6):
            for dx in range(5):
                xx=int(ex-2.5+dx); yy=int(24+dy); nx=(dx-2)/2.5; ny=(dy-2.5)/3
                if nx*nx+ny*ny<=1.1: im.fixed(xx,yy,'eyeW','eye')
        for dy in range(5):
            for dx in range(4):
                xx=int(ex-2+dx); yy=int(25+dy); nx=(dx-1.5)/2.1; ny=(dy-2)/2.6
                if nx*nx+ny*ny<=1.0: im.fixed(xx,yy,'iris1' if dy<2 else 'iris2' if dy<4 else 'iris3','eye')
        for dy in (26,27,28): im.fixed(int(ex-0.5),dy,'pupil','eye')
        im.fixed(int(ex-1.5),25,'white','eye'); im.fixed(int(ex-1.5),26,'white','eye'); im.fixed(int(ex+0.5),28,'iris4','eye')
        for dx in range(-3,3): im.fixed(int(ex-0.5+dx),23,'lash','eye')
        im.fixed(int(ex-3.5 if sign>0 else ex+2.5),24,'lash','eye')
    for k in range(5): im.fixed(24+k,21-(1 if k>=3 else 0),'brow','brow'); im.fixed(36+k,21-(1 if k<=1 else 0),'brow','brow')
    im.fixed(32,30,'skinD','nose'); im.fixed(32,31,'skinD','nose')
    for k in range(4): im.fixed(30+k,34-(1 if k in (0,3) else 0),'mouth','mouth')
    for x in (27,28,36,37): im.fixed(x,31,'blush','blush')
    return im
if __name__=="__main__":
    im=yuri()
    R={**ramps}
    for k,v in fixed.items(): R[k]=[v]*4
    sp=['hairMass','fringeL','fringeR','fringeM','head','band']
    seps=[('torso','armL'),('torso','armR'),('armL2','torso'),('armL','skirt'),('armR','skirt'),('legL','skirt'),('legR','skirt'),('handL','cuffA'),('handR','cuffB'),('scarf','torso'),('scarfTail','torso'),('collarL','torso'),('collarR','torso'),('neck','scarf'),('boots','legL2'),('bootL','leg2L'),('bootR','leg2R'),('cuffL','leg2L'),('cuffR','leg2R'),('shirt','torso'),('belt','torso'),('belt','skirt'),('pouch','skirt')]
    for i,a in enumerate(sp):
        for b in sp[i+1:]: seps.append((a,b))
    out,colors=render(im,R,EDGE,seps)
    txt,pal=to_text(out,colors)
    open("yuri3.txt","w").write(txt); json.dump(pal,open("pal-yuri3.json","w")); print(len(pal))
