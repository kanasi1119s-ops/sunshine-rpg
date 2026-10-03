import sys, math; sys.path.insert(0,".")
from parts import *
from yuri import ramps as BASE, fixed as FIXED, EDGE as BEDGE
ramps={**BASE,
 'hairB':['#2a5a9a','#4a8ad0','#7ab8f0','#c0e4ff'],
 'dress':['#a8bcd8','#d0e0f4','#eef6ff','#ffffff'],
 'dressD':['#7a90b4','#a8bcd8','#d0e0f4','#d0e0f4'],
 'trim':['#1c4a8a','#2e72c0','#52a0e8','#88ccff'],
 'orb':['#58b0ff','#98d8ff','#d0f0ff','#ffffff'],
 'wood':['#4a2c14','#6a4222','#8a5c34','#b0804a'],
 'iris_b1':['#1c4aa0']*4,
}
fixed={**FIXED,'iris1':'#1c4aa0','iris2':'#3a7ae0','iris3':'#8ac0ff','iris4':'#e0f0ff','brow':'#2a5a9a','lash':'#14284a','mouth':'#b8586c','blush':'#f4a0a4'}
edge={**BEDGE,'hairB':'#14305a','dress':'#6a7ea0','dressD':'#6a7ea0','trim':'#0c2a5a','orb':'#2a6aa8','wood':'#2a160c'}
def mina():
    im=Img(64,104)
    # 長い三つ編み（背面）
    for sx in (-1,1):
        x=32+sx*11; pts=[(x,30),(x+sx*3,44),(x+sx*2,58),(x+sx*4,72),(x+sx*3,84)]
        for i in range(len(pts)-1):
            capsule(im,pts[i],pts[i+1],5.0-i*0.5,4.6-i*0.5,'hairB','braid'+str(sx)+str(i),bulge=0.5)
        for (px,py) in ((x+sx*3,44),(x+sx*2,58),(x+sx*4,72)):
            ellipse(im,px,py,5.4,1.8,'trim','tie'+str(sx)+str(int(py)))
        ellipse(im,pts[-1][0],pts[-1][1]+3,3.4,3.6,'hairB','tip'+str(sx))
    # 脚（ドレスの下から少しだけ）
    legs(im,hip_y=84,knee_y=90,ankle_y=96,mat='dress',xs=((29,28.5,28),(35,35.5,36)),r=(3.4,2.8,2.4))
    boots(im,mat='boots',top=95)
    # 杖（右手側に、手前に長く）
    capsule(im,(49,26),(50,96),1.8,1.8,'wood','staff')
    ellipse(im,49.2,22,5.4,5.4,'orb','orb',light_bias=0.2)
    for (x,y) in ((47,20),(48,19),(47,21)): im.set(x,y,'orb',1.2,'orb')
    # 腕（スカートの横）
    capsule(im,(42,42),(46,52),3.0,2.6,'dress','armR',bulge=0.3); capsule(im,(46,52),(48,62),2.6,2.3,'dress','armR2')
    ellipse(im,48.4,64,2.8,2.8,'skin','handR')
    # ドレス上半身（細い肩）とスカート（ゆるやかな裾広がり、ひだ）
    poly(im,[(24.5,41),(39.5,41),(40.5,52),(39,62),(25,62),(23.5,52)],'dress','bodice',shade=lambda x,y,nx,ny:(nx*LIGHT[0]+ny*LIGHT[1])*-0.6+0.4)
    def skirt(x,y,nx,ny): return (nx*LIGHT[0])*-0.5+0.4+0.15*math.sin(nx*9)
    poly(im,[(24,61),(40,61),(47,88),(17,88)],'dress','skirt',shade=skirt)
    for k,x in enumerate(range(21,44,3)):
        for y in range(70+k%3,88): 
            if im.part[y][x]=='skirt': im.set(x,y,'dressD',-1.0,'skirt')
    # 裾の青い縁（波形）
    for x in range(17,48):
        yb=88-int(2*(0.5+0.5*math.sin(x*0.9)))
        for y in range(yb-3,yb+1):
            if im.part[y][x] in ('skirt',): im.set(x,y,'trim',0.2 if y<yb else -0.6,'hem')
    # 胸元の飾り（青い石）と帯
    poly(im,[(24,56),(40,56),(40,60),(24,60)],'trim','sash',shade=lambda x,y,nx,ny:(ny*-0.4+0.3))
    ellipse(im,32,49,2.0,2.2,'orb','pendant')
    # 襟
    poly(im,[(25,38),(39,38),(36,43),(32,45),(28,43)],'trim','collar')
    capsule(im,(32,33),(32,40),3.2,3.6,'skin','neck')
    # 左腕（手前）
    capsule(im,(22.5,42),(18.5,52),3.0,2.6,'dress','armL',bulge=0.3); capsule(im,(18.5,52),(20,62),2.6,2.3,'dress','armL2')
    poly(im,[(16.5,60),(23,60),(23,63),(16.5,63)],'trim','cuffA')
    ellipse(im,19.6,65,2.8,2.8,'skin','handL')
    head(im)
    # 髪: 前髪＋頭の髪（青）
    def hs(x,y,nx,ny):
        th=math.atan2(y+.5-17,x+.5-32); r=math.hypot(x+.5-32,y+.5-17)
        return -(nx*LIGHT[0]+ny*LIGHT[1])*0.5+0.2+math.sin(th*6+r*0.2)*0.18+0.5*max(0,1-math.hypot((x+.5-27)/9,(y+.5-9)/6))
    poly(im,[(20.5,30),(19,18),(21,9),(27,3),(37,3),(43,9),(45,18),(43.5,30),(41,22),(38,18),(35,25),(32,18),(29,25),(26,18),(23,22)],'hairB','hairMass',shade=hs)
    poly(im,[(21,17),(43,17),(43.5,20),(20.5,20)],'trim','band')
    poly(im,[(21.5,20),(29,19),(27,26),(24,27),(21,24)],'hairB','fringeL',shade=hs)
    poly(im,[(42.5,20),(35,19),(37,24),(40,26),(43,24)],'hairB','fringeR',shade=hs)
    poly(im,[(29,19),(35,19),(34,24),(31,24)],'hairB','fringeM',shade=hs)
    face(im,iris=('iris1','iris2','iris3','iris4'))
    # 髪飾り（小さな雫の飾り）
    ellipse(im,41,15,2,2,'orb','pin')
    return im
if __name__=="__main__":
    im=mina()
    seps=[('bodice','armL'),('bodice','armR'),('skirt','armL'),('skirt','armR'),('sash','bodice'),('collar','bodice'),('handL','cuffA'),('braid-10','bodice')]
    n=finish(im,ramps,fixed,edge,seps,'mina1'); print(n)
