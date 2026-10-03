import sys, math; sys.path.insert(0,".")
from parts import *
from yuri import ramps as BASE, fixed as FIXED, EDGE as BEDGE
def mk(extra_r, extra_f, extra_e):
    return {**BASE,**extra_r},{**FIXED,**extra_f},{**BEDGE,**extra_e}
def hairshade_factory(cx=32,cy=17,hx=26,hy=8):
    def f(x,y,nx,ny):
        th=math.atan2(y+.5-cy,x+.5-cx); r=math.hypot(x+.5-cx,y+.5-cy)
        return -(nx*LIGHT[0]+ny*LIGHT[1])*0.5+0.18+math.sin(th*7.0+r*0.15)*0.22+0.6*max(0,1-math.hypot((x+.5-hx)/9,(y+.5-hy)/6))
    return f
def spiky(im, mat, outer, inner, notches, shade, cx=32, cy=17):
    poly(im,outer+inner,mat,'hairMass',shade=shade)
    for (nx_,ny_) in notches:
        dx,dy=cx-nx_,cy-ny_; L=math.hypot(dx,dy)
        for t in range(0,7):
            x=nx_+dx/L*t; y=ny_+dy/L*t
            if im.part[int(y)][int(x)]=='hairMass': im.set(int(x),int(y),mat,-1.0,'hairMass')
def torso_basic(im, top=41, mat='jacket', w=(23,41), hem=72, flare=2):
    poly(im,[(w[0],top),(w[1],top),(w[1]+0.5,top+11),(w[1]-1,top+23),(w[0]+1,top+23),(w[0]-0.5,top+11)],mat,'torso',shade=lambda x,y,nx,ny:(nx*LIGHT[0]+ny*LIGHT[1])*-0.7+0.28)
    poly(im,[(w[0]+1,top+22),(w[1]-1,top+22),(w[1]+flare+1,hem),(w[0]-flare-1,hem)],mat,'skirt',shade=lambda x,y,nx,ny:(nx*LIGHT[0])*-0.6+0.12)
def arms(im, mat='jacket', cuff='cuff', ls=(23,43), le=(17.5,56), lw=(18.5,66), rs=(41,43), re=(46.5,56), rw=(45.5,66), r=(3.4,2.9,2.5), glove=None):
    capsule(im,rs,re,r[0],r[1],mat,'armR',bulge=0.4); capsule(im,re,rw,r[1],r[2],mat,'armR2')
    ellipse(im,rw[0],rw[1]+2.5,3.0,3.0,glove or 'skin','handR')
    capsule(im,ls,le,r[0],r[1],mat,'armL',bulge=0.4); capsule(im,le,lw,r[1],r[2],mat,'armL2')
    poly(im,[(lw[0]-3.5,lw[1]-3),(lw[0]+3.5,lw[1]-3),(lw[0]+3.5,lw[1]+0.5),(lw[0]-3.5,lw[1]+0.5)],cuff,'cuffA')
    poly(im,[(rw[0]-3.5,rw[1]-3),(rw[0]+3.5,rw[1]-3),(rw[0]+3.5,rw[1]+0.5),(rw[0]-3.5,rw[1]+0.5)],cuff,'cuffB')
    ellipse(im,lw[0],lw[1]+3,3.0,3.0,glove or 'skin','handL')
SEPS=[('torso','armL'),('torso','armR'),('armL2','torso'),('armL','skirt'),('armR','skirt'),('legL','skirt'),('legR','skirt'),('handL','cuffA'),('handR','cuffB'),('scarf','torso'),('scarfTail','torso'),('collarL','torso'),('collarR','torso'),('neck','scarf'),('bootL','leg2L'),('bootR','leg2R'),('cuffL','leg2L'),('cuffR','leg2R'),('shirt','torso'),('belt','torso'),('belt','skirt'),('pouch','skirt'),('vest','torso'),('vest','armL'),('vest','armR'),('vest','shirt')]
# ---------------- レト ----------------
def reto():
    R,F,E=mk({'hairR':['#3a1410','#6a2418','#9a3c24','#cc6a3c'],'coat':['#1e2430','#363e50','#566074','#8090a8'],'coatD':['#141a24']*4,'red':['#7a1418','#b02a2a','#d84a40','#f88068'],'blade':['#707a90','#a0aab8','#d0d8e4','#ffffff']},
             {'iris1':'#6a3c1c','iris2':'#a8682c','iris3':'#e0a860','iris4':'#fff0c8','brow':'#3a1410','lash':'#1c0c08','mouth':'#a05040','blush':'#f0a090'},{'hairR':'#2a0c08','coat':'#10141c','coatD':'#10141c','red':'#4a0c10','blade':'#3a4054'})
    im=Img(64,104)
    legs(im,mat='pants',xs=((28.5,28,27.5),(35.5,36,37)),r=(4.2,3.5,2.9)); boots(im)
    arms(im,mat='coat',cuff='leather',le=(18,55),lw=(20,65),re=(46,55),rw=(44,65))
    # 長いコート（膝の上まで）
    poly(im,[(22.5,41),(41.5,41),(42,52),(41,64),(23,64),(22,52)],'coat','torso',shade=lambda x,y,nx,ny:(nx*LIGHT[0]+ny*LIGHT[1])*-0.7+0.28)
    poly(im,[(23,62),(41,62),(46,92),(18,92)],'coat','skirt',shade=lambda x,y,nx,ny:(nx*LIGHT[0])*-0.6+0.12+0.1*math.sin(nx*8))
    for x in (24,28,36,40):
        for y in range(70,92):
            if im.part[y][x]=='skirt': im.set(x,y,'coatD',-1.0,'skirt')
    for y in range(41,92): im.set(32,y,'coatD',-1.0,'torso' if y<62 else 'skirt')
    for k in range(5): im.set(34,46+k*5,'blade',0.8,'torso'); im.set(34,47+k*5,'blade',0.2,'torso')       # ボタン
    poly(im,[(22,61),(42,61),(42,64.5),(22,64.5)],'leather','belt',shade=lambda x,y,nx,ny:(ny*-0.5+0.3))
    ellipse(im,32,62.7,2.4,2.0,'gold','buckle')
    # 腰の短剣
    capsule(im,(22,66),(15,84),1.6,1.4,'blade','dagger'); ellipse(im,22.5,65.5,2.2,2.2,'gold','hilt')
    neck(im,33,41)
    # 赤いマフラー（ゆるく巻く）
    poly(im,[(24,37),(40,37),(42,42),(32,46),(22,42)],'red','scarf')
    poly(im,[(25,42),(31,44),(28,60),(23,57)],'red','scarfTail')
    for k in range(5): im.set(25+(k%2),46+k*2,'red',-1.0,'scarfTail')
    poly(im,[(22,38),(28,37),(30,43),(23,44)],'coat','collarL'); poly(im,[(42,38),(36,37),(34,43),(41,44)],'coat','collarR')
    head(im)
    sh=hairshade_factory()
    outer=[(21,27),(19.5,19),(12,18),(17.5,13),(10.5,8),(19,10.5),(15.5,2.5),(24,8),(26,2),(30,7),(34,1),(37,7),(42.5,2.5),(41,9),(49,5),(45,11),(53.5,13),(46,15),(52,19),(44.5,19.5),(43,27)]
    inner=[(41.5,22),(38.5,20),(35,26.5),(32,19),(28,24),(25,19.5),(22.5,23)]
    spiky(im,'hairR',outer,inner,[(17.5,13),(19,10.5),(24,8),(30,7),(37,7),(41,9),(45,11),(46,15)],sh)
    # 前髪が片目（右目側）にかかる
    poly(im,[(35,19.5),(43,19),(43.5,26),(40,24.5),(37.5,22.5)],'hairR','fringeR',shade=sh)
    for (x,y) in ((39,21),(40,22),(41,23),(42,24)): im.set(x,y,'hairR',-1.0,'fringeR')
    poly(im,[(22,19.5),(29,19),(27.5,25.5),(24.5,27.5),(21.5,23.5)],'hairR','fringeL',shade=sh)
    face(im,iris=('iris1','iris2','iris3','iris4'),smile=False)
    # 片側の目を隠す髪の上から目を描き直さない（右目は髪の下）
    return im,R,F,E
# ---------------- ガイド ----------------
def guide():
    R,F,E=mk({'hairG':['#7a5a14','#b88a24','#e0b84a','#fff0a0'],'vest':['#4a2c14','#6a4222','#8a5c34','#b0804a'],'shirtG':['#d8d0c0','#f0e8d8','#fffaf0','#ffffff'],'green':['#1c6a3c','#2a9a58','#52c878','#98f0b0'],'goggle':['#5a3a10','#8a6420','#c09030','#f0cc50'],'lens':['#2a6aa0','#58a8e0','#98d8ff','#e0f4ff'],'bow':['#4a2c14','#6a4222','#8a5c34','#b0804a'],'stripe_string':['#e8e0c8']*4},
             {'iris1':'#2a6a40','iris2':'#48a468','iris3':'#98e0a8','iris4':'#e8ffe8','brow':'#7a5a14','lash':'#2a1c08','mouth':'#b0584c','blush':'#f4a898'},{'hairG':'#4a340a','vest':'#2a160c','shirtG':'#8a8070','green':'#0c3a20','goggle':'#3a2408','lens':'#1c4a70','bow':'#2a160c'})
    im=Img(64,104)
    # 背中の弓
    pts=[(51+5.5*math.sin(t*math.pi),28+t*52) for t in [i/16 for i in range(17)]]
    for i in range(len(pts)-1): capsule(im,pts[i],pts[i+1],1.6,1.6,'bow','bow%d'%i)
    for y in range(29,80): im.set(50,y,'stripe_string',0.5,'bowstring')
    legs(im,mat='pants',xs=((28.5,28,27.5),(35.5,36,37)),r=(4.2,3.5,2.9)); boots(im,mat='boots')
    arms(im,mat='shirtG',cuff='leather',le=(17.5,56),lw=(19,66),re=(46.5,56),rw=(45,66))
    # シャツ＋ベスト
    poly(im,[(23,41),(41,41),(41.5,52),(40,64),(24,64),(22.5,52)],'shirtG','torso',shade=lambda x,y,nx,ny:(nx*LIGHT[0]+ny*LIGHT[1])*-0.7+0.28)
    poly(im,[(23,42),(30,42),(29,64),(24,64),(22.5,52)],'vest','vest',shade=lambda x,y,nx,ny:(nx*LIGHT[0]+ny*LIGHT[1])*-0.7+0.28)
    poly(im,[(41,42),(34,42),(35,64),(40,64),(41.5,52)],'vest','vest',shade=lambda x,y,nx,ny:(nx*LIGHT[0]+ny*LIGHT[1])*-0.7+0.1)
    poly(im,[(24,63),(40,63),(44,72),(20,72)],'pants','skirt',shade=lambda x,y,nx,ny:(nx*LIGHT[0])*-0.6+0.12)
    poly(im,[(22,60),(42,60),(42,63.5),(22,63.5)],'leather','belt',shade=lambda x,y,nx,ny:(ny*-0.5+0.3))
    ellipse(im,32,61.7,2.4,2.0,'gold','buckle')
    # 商人の鞄とペンダント
    poly(im,[(34.5,64),(42,64),(42,72),(34.5,72)],'vest','pouch'); im.set(38,67,'gold',0.8,'pouch')
    neck(im,33,41)
    # 緑のスカーフ
    poly(im,[(24.5,37),(39.5,37),(41,42),(32,46),(23,42)],'green','scarf')
    poly(im,[(25,42),(31,44),(28,58),(24,55)],'green','scarfTail')
    ellipse(im,32,50,1.8,2.0,'gold','pendant')
    head(im)
    sh=hairshade_factory(hx=27,hy=9)
    # ゴーグル用に額を空ける、金髪のくせ毛
    outer=[(21,27),(19.5,19),(13,17),(18,13),(12,8),(20,10.5),(18,3.5),(25,8),(28,2.5),(31,7),(35,2),(38,7),(44,3),(42,9.5),(51,7),(45.5,13.5),(51,17.5),(44.5,19.5),(43,27)]
    inner=[(41.5,22),(38.5,20.5),(35,25),(32,19.5),(29,25),(26,20.5),(22.5,23)]
    spiky(im,'hairG',outer,inner,[(18,13),(20,10.5),(25,8),(31,7),(38,7),(42,9.5),(45.5,13.5)],sh)
    # ゴーグル（額の上、2つのレンズ）
    poly(im,[(20.5,13.5),(43.5,13.5),(44,18),(20,18)],'goggle','goggleBand',shade=lambda x,y,nx,ny:(ny*-0.5+0.35))
    ellipse(im,26.5,15.8,4.8,4.0,'goggle','gogL'); ellipse(im,37.5,15.8,4.8,4.0,'goggle','gogR')
    ellipse(im,26.5,15.8,3.2,2.6,'lens','lensL'); ellipse(im,37.5,15.8,3.2,2.6,'lens','lensR')
    im.set(25,15,'lens',1.3,'lensL'); im.set(36,15,'lens',1.3,'lensR')
    poly(im,[(22,19.5),(29,19.5),(27.5,25),(24.5,27),(21.5,23)],'hairG','fringeL',shade=sh)
    poly(im,[(42,19.5),(35,19.5),(36.5,23),(39.5,26.5),(42.5,23)],'hairG','fringeR',shade=sh)
    face(im,iris=('iris1','iris2','iris3','iris4'))
    return im,R,F,E
# ---------------- オルカ ----------------
def orca():
    R,F,E=mk({'hairO':['#3a2c20','#5a4630','#7a6244','#a08a64'],'helmet':['#586070','#8890a0','#b8c0cc','#e8eef4'],'vestO':['#a84a0c','#d8701c','#f89c34','#ffc860'],'stripe':['#a8a090','#d8d4c0','#f8f4e0','#ffffff'],'shirtO':['#4a4e5a','#6a707e','#8a90a0','#b0b8c8'],'beard':['#3a2c20','#5a4630','#7a6244','#a08a64'],'lamp':['#c09030','#f0cc50','#fff0a0','#ffffff'],'pick':['#4a2c14','#6a4222','#8a5c34','#b0804a'],'steel':['#586070','#8890a0','#b8c0cc','#e8eef4']},
             {'iris1':'#4a3820','iris2':'#7a5a30','iris3':'#c09860','iris4':'#f0e0b8','brow':'#3a2c20','lash':'#1c1008','mouth':'#8a4438','blush':'#e09880','bowstring':'#e8e0c8'},{'hairO':'#1c140c','helmet':'#2c323c','vestO':'#6a2c08','stripe':'#6a6458','shirtO':'#262a32','beard':'#1c140c','lamp':'#6a4a10','pick':'#2a160c','steel':'#2c323c'})
    im=Img(72,104)  # 肩幅が広いので少し広い枠
    legs(im,mat='pants',xs=((29,28.5,28),(43,43.5,44)),r=(5.2,4.4,3.6),hip_y=66); 
    # ブーツ（大きい）
    poly(im,[(23,90),(34,90),(35,98),(37,101),(22,101),(22.5,96)],'boots','bootL'); poly(im,[(37,90),(48,90),(49.5,96),(50,101),(35,101),(36.5,98)],'boots','bootR')
    for x in range(22,38): im.set(x,101,'boots',-1.0,'bootL')
    for x in range(35,51): im.set(x,101,'boots',-1.0,'bootR')
    for x in range(24,34): im.set(x,91,'leather',0.6,'cuffL'); im.set(x,92,'leather',-0.2,'cuffL')
    for x in range(38,47): im.set(x,91,'leather',0.6,'cuffR'); im.set(x,92,'leather',-0.2,'cuffR')
    # 右手のつるはし（背面に大きく）
    capsule(im,(57,20),(58,98),2.0,2.0,'pick','pickShaft')
    poly(im,[(48,16),(58,12),(67,18),(65,22),(58,17),(50,21)],'steel','pickHead',shade=lambda x,y,nx,ny:(ny*-0.6+0.3))
    arms(im,mat='shirtO',cuff='leather',ls=(21,44),le=(13,58),lw=(15,68),rs=(51,44),re=(58,58),rw=(56,68),r=(5.0,4.2,3.6))
    ellipse(im,56,70.5,3.8,3.8,'skin','handR')
    # 胴: 広い肩・厚い胸（オレンジのベスト＋反射の帯）
    poly(im,[(21,41),(51,41),(52,54),(49,66),(23,66),(20,54)],'shirtO','torso',shade=lambda x,y,nx,ny:(nx*LIGHT[0]+ny*LIGHT[1])*-0.7+0.28)
    poly(im,[(22,41),(50,41),(50.5,54),(47.5,66),(24.5,66),(21.5,54)],'vestO','vest',shade=lambda x,y,nx,ny:(nx*LIGHT[0]+ny*LIGHT[1])*-0.7+0.3)
    for yy in (50,58):
        for x in range(22,51): 
            if im.part[yy][x]=='vest': im.set(x,yy,'stripe',0.8,'vest'); im.set(x,yy+1,'stripe',0.1,'vest')
    for y in range(41,66): im.set(36,y,'vestO',-1.0,'vest')
    poly(im,[(22,64),(50,64),(48,74),(24,74)],'pants','skirt',shade=lambda x,y,nx,ny:(nx*LIGHT[0])*-0.6+0.12)
    poly(im,[(22,63),(50,63),(50,66.5),(22,66.5)],'leather','belt',shade=lambda x,y,nx,ny:(ny*-0.5+0.3))
    ellipse(im,36,64.7,2.6,2.2,'steel','buckle')
    capsule(im,(36,32),(36,41),4.2,4.8,'skin','neck')
    head(im,cx=36,cy=24,rx=11.4,ry=11.4)
    # ひげ（頬から顎を覆う）
    poly(im,[(25.5,28),(46.5,28),(47,32),(43,40),(36,43),(29,40),(25,32)],'beard','beard',shade=lambda x,y,nx,ny:(nx*LIGHT[0]+ny*LIGHT[1])*-0.6+0.25+0.12*math.sin(x*1.8+y*0.5))
    # ヘルメット（灰色、ひさし、ランプ）
    poly(im,[(23,19),(24,10),(30,3),(36,1.5),(42,3),(48,10),(49,19),(46,16.5),(26,16.5)],'helmet','helmet',shade=lambda x,y,nx,ny:(nx*LIGHT[0]+ny*LIGHT[1])*-0.7+0.35)
    poly(im,[(21,16.5),(51,16.5),(52,20),(20,20)],'helmet','brim',shade=lambda x,y,nx,ny:(ny*-0.5+0.25))
    ellipse(im,36,8,3.6,3.0,'lamp','lamp'); im.set(35,6,'lamp',1.3,'lamp')
    for x in range(26,47): im.set(x,10,'helmet',0.9,'helmet') if x%3 else None
    face(im,cx=36,iris=('iris1','iris2','iris3','iris4'),smile=False,blush=False)
    # 太い眉
    for k in range(7): im.fixed(26+k,21,'brow','brow'); im.fixed(40+k,21,'brow','brow')
    return im,R,F,E
if __name__=="__main__":
    for name,fn in (("reto",reto),("guide",guide),("orca",orca)):
        im,R,F,E=fn()
        n=finish(im,R,F,E,SEPS+[('helmet','brim'),('lamp','helmet'),('beard','head'),('vestO','torso'),('goggleBand','hairMass'),('gogL','goggleBand'),('gogR','goggleBand'),('lensL','gogL'),('lensR','gogR')],name+"1")
        print(name,n)
