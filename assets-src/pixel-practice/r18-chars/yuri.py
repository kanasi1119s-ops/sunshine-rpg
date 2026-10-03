import sys, json, math, random
sys.path.insert(0,".")
from chargen import *
def ramp(dark, mid, light, hi=None):
    # 色相シフト: 暗→青紫寄り、明→黄寄り（手で指定）
    return [dark, mid, light, hi or light]
def yuri(ver=1):
    random.seed(3)
    W,H=64,96
    im=Img(W,H)
    # 影（地面）
    # --- 脚
    capsule(im,(27,58),(26.5,73),5.2,4.0,'pants','legL',bulge=0.4)
    capsule(im,(26.5,73),(26,86),4.0,3.2,'pants','legL2')
    capsule(im,(37,58),(37.5,73),5.2,4.0,'pants','legR',bulge=0.4)
    capsule(im,(37.5,73),(39,86),4.0,3.2,'pants','legR2')
    # ブーツ（足首まで覆う、つま先は外向き）
    poly(im,[(22,82),(30,82),(31,90),(33,92),(21,92),(21,88)],'boots','bootL')
    poly(im,[(34,82),(42,82),(43,88),(44,92),(32,92),(33,90)],'boots','bootR')
    for x in range(21,34): im.set(x,92,'boots',-1.0,'bootL')
    for x in range(32,45): im.set(x,92,'boots',-1.0,'bootR')
    # ブーツの折り返し（革の帯）
    for x in range(22,31): im.set(x,83,'leather',0.5,'cuffL'); im.set(x,84,'leather',-0.2,'cuffL')
    for x in range(34,43): im.set(x,83,'leather',0.5,'cuffR'); im.set(x,84,'leather',-0.2,'cuffR')
    # --- 腕（後ろの腕を先に）
    capsule(im,(43,40),(47.5,51),4.4,3.8,'jacket','armR',bulge=0.5)
    capsule(im,(47.5,51),(45,61),3.8,3.2,'jacket','armR2')
    ellipse(im,45,63.5,3.6,3.4,'skin','handR')
    # --- 胴（ジャケット）
    poly(im,[(22,38),(42,38),(44,50),(45,62),(19,62),(20,50)],'jacket','torso',shade=lambda x,y,nx,ny:(nx*LIGHT[0]+ny*LIGHT[1])*-0.75+0.25)
    # ジャケットの前合わせ（中心線）と下の裾の広がり
    for y in range(40,62): im.set(32,y,'jacketD',-1.0,'torso') if y>42 else None
    # 内側のシャツ（開いた胸元）
    poly(im,[(29,38),(35,38),(34,48),(30,48)],'shirt','shirt')
    # 腰のベルト・バックル・ポーチ
    poly(im,[(20,55),(44,55),(44,59),(20,59)],'leather','belt',shade=lambda x,y,nx,ny:(ny*-0.5+0.3))
    ellipse(im,32,57,2.8,2.4,'gold','buckle')
    poly(im,[(36,58),(44,58),(44,66),(36,66)],'leather','pouch')
    im.set(40,62,'gold',0.8,'pouch'); im.set(41,62,'gold',0.8,'pouch'); im.set(40,63,'gold',0.2,'pouch')
    # 裾（ジャケットの下の広がり。ひだ）
    poly(im,[(19,60),(45,60),(47,69),(17,69)],'jacket','skirt',shade=lambda x,y,nx,ny:(nx*LIGHT[0]*-1*0.0)+(nx*LIGHT[0])*-0.7+0.15)
    # --- 左腕（手前、少し腰に）
    capsule(im,(21,40),(16.5,51),4.4,3.8,'jacket','armL',bulge=0.5)
    capsule(im,(16.5,51),(19,61),3.8,3.2,'jacket','armL2')
    # 袖口
    poly(im,[(15,58),(22,58),(22,62),(15,62)],'cuff','cuffA')
    poly(im,[(42,58),(49,58),(49,62),(42,62)],'cuff','cuffB')
    ellipse(im,19.5,64,3.7,3.5,'skin','handL')
    # 腕輪（右手首、光る灯り石）
    ellipse(im,45,61.5,3.9,1.8,'gold','brace')
    ellipse(im,45,62,1.4,1.4,'glow','gem')
    # --- 首・スカーフ（オレンジ）
    capsule(im,(32,30),(32,38),3.6,4.0,'skin','neck')
    poly(im,[(24,34),(40,34),(42,40),(32,44),(22,40)],'scarf','scarf')
    # スカーフの垂れ（右肩から胸へ）
    poly(im,[(34,40),(40,40),(41,54),(37,57),(34,52)],'scarf','scarfTail')
    for k in range(5): im.set(35+(k%2),43+k*2,'scarfD',-1.0,'scarfTail')
    # 襟
    poly(im,[(22,36),(28,35),(30,42),(24,44)],'jacketD','collarL')
    poly(im,[(42,36),(36,35),(34,42),(40,44)],'jacketD','collarR')
    # --- 頭
    ellipse(im,32,19.5,11.5,12.2,'skin','head',light_bias=0.15)
    # 耳
    ellipse(im,20.3,21,1.8,2.6,'skin','earL'); ellipse(im,43.7,21,1.8,2.6,'skin','earR')
    # --- 髪: 後ろ髪（頭の後ろ）→ ツンツンの房 → 前髪
    for (x0,y0,x1,y1,w) in [(32,3,32,-4,5.0),(25,5,18,-3,4.6),(39,5,46,-3,4.6),(20,10,10,6,4.2),(44,10,54,7,4.2),(23,14,14,19,3.8),(41,14,50,19,3.8)]:
        capsule(im,(x0,y0),(x1,y1),w,0.6,'hair','spike',bulge=0.6)
    ellipse(im,32,12,12.2,8.5,'hair','hairCap',light_bias=0.2)
    # 前髪（額にかかる房3本）
    poly(im,[(21,13),(29,10),(28,19),(24,22),(20,18)],'hair','fringeL')
    poly(im,[(43,13),(36,10),(36,16),(39,20),(44,18)],'hair','fringeR')
    poly(im,[(29,10),(36,10),(34,17),(31,17)],'hair','fringeM')
    # ヘッドバンド
    poly(im,[(20,14),(44,14),(44.5,17),(19.5,17)],'band','band',shade=lambda x,y,nx,ny:(ny*-0.4+0.3))
    for k in range(3): im.set(40+k,16,'bandD',-1.0,'band')
    # --- 顔の部品
    # 目（左右）: 白目＋虹彩（緑）＋瞳孔＋反射
    for ex,sign in ((26.3,1),(37.7,-1)):
        for dy in range(6):
            for dx in range(5):
                xx=int(ex-2.5+dx); yy=int(19+dy)
                nx=(dx-2)/2.5; ny=(dy-2.5)/3
                if nx*nx+ny*ny<=1.1: im.fixed(xx,yy,'eyeW','eye')
        for dy in range(5):
            for dx in range(4):
                xx=int(ex-2+dx+ (0 if sign>0 else 0)); yy=int(20+dy)
                nx=(dx-1.5)/2.1; ny=(dy-2)/2.6
                if nx*nx+ny*ny<=1.0: im.fixed(xx,yy,'iris1' if dy<2 else 'iris2' if dy<4 else 'iris3','eye')
        for dy in (21,22,23): im.fixed(int(ex-0.5+(0 if sign>0 else 0)),dy,'pupil','eye')
        im.fixed(int(ex-1.5),20,'iris1','eye'); im.fixed(int(ex-1.5),21,'iris1','eye'); im.fixed(int(ex+0.5),23,'iris4','eye')
        # 上まぶた（太い線）とまつげ
        for dx in range(-3,3): im.fixed(int(ex-0.5+dx),18,'lash','eye')
        im.fixed(int(ex-3.5 if sign>0 else ex+2.5),19,'lash','eye')
    # 眉（少し上がり気味）
    for k in range(5): im.fixed(23+k,16-(1 if k>=3 else 0),'brow','brow'); im.fixed(36+k,16-(1 if k<=1 else 0),'brow','brow')
    # 鼻・口・頬
    im.fixed(32,25,'skinD','nose'); im.fixed(32,26,'skinD','nose')
    for k in range(4): im.fixed(30+k,29-(1 if k in (0,3) else 0),'mouth','mouth')
    im.fixed(27,26,'blush','blush'); im.fixed(28,26,'blush','blush'); im.fixed(36,26,'blush','blush'); im.fixed(37,26,'blush','blush')
    return im
ramps={
 'skin':['#b8785a','#e0a07c','#f4c8a0','#ffdcbc'],
 'hair':['#5a2e18','#8a4a24','#b8702c','#e0a050'],
 'jacket':['#1c5058','#2a7c88','#40a8b0','#78d4d0'],
 'jacketD':['#143c44','#1c5058','#2a7c88','#2a7c88'],
 'shirt':['#c8c0b0','#e8e0d0','#f8f4e8','#ffffff'],
 'scarf':['#a8480c','#d8701c','#f89c34','#ffc860'],
 'scarfD':['#7a3008','#a8480c','#d8701c','#d8701c'],
 'pants':['#4a2c1a','#6a4228','#8a5c38','#a87848'],
 'boots':['#2a1a12','#4a2c1a','#6a4228','#8a5c38'],
 'leather':['#3a2214','#5a3a20','#7a5030','#a07448'],
 'gold':['#a8701c','#d8a030','#f8d058','#fff0a0'],
 'cuff':['#8a4a1c','#b87030','#d89848','#f0b868'],
 'band':['#a8480c','#d8701c','#f89c34','#ffc860'],
 'bandL':['#ffc860']*4,
 'pantsD':['#2a160c']*4,
 'jacketD2':['#0c2c34']*4,
 'bandD':['#7a3008','#7a3008','#7a3008','#7a3008'],
 'glow':['#78e8ff','#a8f4ff','#d8fcff','#ffffff'],
}
fixed={'eyeW':'#fdfcf8','iris1':'#1c7a50','iris2':'#34b070','iris3':'#7ae0a0','iris4':'#d8ffe8','pupil':'#0c2a24','white':'#ffffff','lash':'#2a1210','brow':'#5a2e18','skinD':'#c88866','mouth':'#a8483c','blush':'#f0907c'}
EDGE={'skin':'#7a4638','hair':'#3a1c10','jacket':'#0c2c34','jacketD':'#0c2c34','shirt':'#7a7060','scarf':'#6a2808','scarfD':'#6a2808','pants':'#2a160c','boots':'#160c08','leather':'#241408','gold':'#6a4010','cuff':'#5a2c10','band':'#6a2808','bandD':'#6a2808','glow':'#2a7a90'}
if __name__=="__main__":
    im=yuri()
    # ramps に固定色を追加して render
    for k,v in fixed.items(): ramps[k]=[v]*4
    seps=[('torso','armL'),('torso','armR'),('armL2','torso'),('armL','skirt'),('armR','skirt'),('legL','skirt'),('legR','skirt'),('handL','cuffA'),('handR','cuffB'),('head','hairCap'),('head','fringeL'),('head','fringeR'),('head','fringeM'),('scarf','torso'),('scarfTail','torso'),('collarL','torso'),('collarR','torso'),('head','band'),('hairCap','band'),('neck','scarf'),('boots','legL2'),('bootL','legL2'),('bootR','legR2')]
    out,colors=render(im,{**ramps},EDGE,seps)
    txt,pal=to_text(out,colors)
    open("yuri1.txt","w").write(txt); json.dump(pal,open("pal-yuri.json","w"))
    print(len(pal))
