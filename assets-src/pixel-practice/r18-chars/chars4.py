import sys, math; sys.path.insert(0,".")
from parts import *
from chars3 import mk, hairshade_factory, spiky, SEPS
# ---------------- ガイド（女性）: 短めのくせ毛にゴーグル、ツインの短い房、ベスト、短いスカートとレギンス ----------------
def guide():
    R,F,E=mk({'hairG':['#7a5a14','#b88a24','#e0b84a','#fff0a0'],'vest':['#4a2c14','#6a4222','#8a5c34','#b0804a'],'shirtG':['#d8d0c0','#f0e8d8','#fffaf0','#ffffff'],'green':['#1c6a3c','#2a9a58','#52c878','#98f0b0'],'goggle':['#5a3a10','#8a6420','#c09030','#f0cc50'],'lens':['#2a6aa0','#58a8e0','#98d8ff','#e0f4ff'],'bow':['#4a2c14','#6a4222','#8a5c34','#b0804a'],'stripe_string':['#e8e0c8']*4,'skirtG':['#2a5a3a','#3a7a50','#5aa070','#88c898'],'tights':['#3a2418','#5a3a24','#7a5238','#9a6a48']},
             {'iris1':'#2a6a40','iris2':'#48a468','iris3':'#98e0a8','iris4':'#e8ffe8','brow':'#7a5a14','lash':'#2a1c08','mouth':'#c05a5a','blush':'#f8a8a8'},{'hairG':'#4a340a','vest':'#2a160c','shirtG':'#8a8070','green':'#0c3a20','goggle':'#3a2408','lens':'#1c4a70','bow':'#2a160c','skirtG':'#143a24','tights':'#241208'})
    im=Img(64,104)
    # ツインの短い房（後ろ）
    for sx in (-1,1):
        capsule(im,(32+sx*11,22),(32+sx*15,34),3.4,3.0,'hairG','tail'+str(sx),bulge=0.4)
        capsule(im,(32+sx*15,34),(32+sx*14,44),3.0,1.6,'hairG','tailB'+str(sx))
        ellipse(im,32+sx*12.5,24,3.2,1.5,'green','tie'+str(sx))
    # 背中の弓
    pts=[(51+5.5*math.sin(t*math.pi),28+t*52) for t in [i/16 for i in range(17)]]
    for i in range(len(pts)-1): capsule(im,pts[i],pts[i+1],1.6,1.6,'bow','bow%d'%i)
    for y in range(29,80): im.set(50,y,'stripe_string',0.5,'bowstring')
    # 脚: レギンス（細め）＋ブーツ
    legs(im,hip_y=68,mat='tights',xs=((29,28.5,28),(35,35.5,36)),r=(3.9,3.3,2.7)); boots(im,mat='boots')
    # 腕（細め、シャツの袖）
    capsule(im,(41,43),(46,56),3.0,2.6,'shirtG','armR',bulge=0.3); capsule(im,(46,56),(45,66),2.6,2.3,'shirtG','armR2')
    ellipse(im,45,68.5,2.8,2.8,'skin','handR')
    capsule(im,(23,43),(18,56),3.0,2.6,'shirtG','armL',bulge=0.3); capsule(im,(18,56),(19,66),2.6,2.3,'shirtG','armL2')
    poly(im,[(15.5,63),(22.5,63),(22.5,66.5),(15.5,66.5)],'leather','cuffA'); poly(im,[(41.5,63),(48.5,63),(48.5,66.5),(41.5,66.5)],'leather','cuffB')
    ellipse(im,19,69,2.8,2.8,'skin','handL')
    # 胴: 細い肩、くびれ。ブラウス＋ベスト
    poly(im,[(24,41),(40,41),(40.5,50),(38.5,60),(25.5,60),(23.5,50)],'shirtG','torso',shade=lambda x,y,nx,ny:(nx*LIGHT[0]+ny*LIGHT[1])*-0.7+0.3)
    poly(im,[(24,42),(30,42),(29.5,61),(25.5,61),(23.5,50)],'vest','vest',shade=lambda x,y,nx,ny:(nx*LIGHT[0]+ny*LIGHT[1])*-0.7+0.3)
    poly(im,[(40,42),(34,42),(34.5,61),(38.5,61),(40.5,50)],'vest','vest',shade=lambda x,y,nx,ny:(nx*LIGHT[0]+ny*LIGHT[1])*-0.7+0.12)
    # 短いスカート（ひらり）
    poly(im,[(25,59),(39,59),(45,76),(19,76)],'skirtG','skirt',shade=lambda x,y,nx,ny:(nx*LIGHT[0])*-0.6+0.25+0.12*math.sin(nx*8))
    for x in (24,29,35,40):
        for y in range(64,76):
            if im.part[y][x]=='skirt': im.set(x,y,'skirtG',-1.0,'skirt')
    poly(im,[(24,57.5),(40,57.5),(40,61),(24,61)],'leather','belt',shade=lambda x,y,nx,ny:(ny*-0.5+0.3))
    ellipse(im,32,59.2,2.4,2.0,'gold','buckle')
    poly(im,[(36.5,61),(43,61),(43,68),(36.5,68)],'vest','pouch'); im.set(40,64,'gold',0.8,'pouch')
    neck(im,33,41)
    poly(im,[(25,37),(39,37),(41,42),(32,46),(23,42)],'green','scarf')
    poly(im,[(25,42),(31,44),(28,57),(24,54)],'green','scarfTail')
    ellipse(im,32,50,1.8,2.0,'gold','pendant')
    head(im,rx=10.2,ry=11.2)
    sh=hairshade_factory(hx=27,hy=9)
    # 髪: ふわっと外に跳ねる短めのくせ毛（ボブ）
    outer=[(21.5,31),(19.5,22),(14,19),(17.5,14.5),(13,9),(20,11),(19,4.5),(25,8.5),(28,3),(31,7.5),(35,2.5),(38,7.5),(43,4),(43,10.5),(51,9),(46.5,14.5),(50,19),(44.5,22),(42.5,31)]
    inner=[(41,25),(39,21),(35.5,26),(32.5,20.5),(29,26),(26,21),(23,25)]
    spiky(im,'hairG',outer,inner,[(17.5,14.5),(20,11),(25,8.5),(31,7.5),(38,7.5),(43,10.5),(46.5,14.5)],sh)
    # ゴーグル（額の上）
    poly(im,[(20.5,13.5),(43.5,13.5),(44,18),(20,18)],'goggle','goggleBand',shade=lambda x,y,nx,ny:(ny*-0.5+0.35))
    ellipse(im,26.5,15.8,4.8,4.0,'goggle','gogL'); ellipse(im,37.5,15.8,4.8,4.0,'goggle','gogR')
    ellipse(im,26.5,15.8,3.2,2.6,'lens','lensL'); ellipse(im,37.5,15.8,3.2,2.6,'lens','lensR')
    im.set(25,15,'lens',1.3,'lensL'); im.set(36,15,'lens',1.3,'lensR')
    poly(im,[(22,19.5),(29,19.5),(27.5,26),(24.5,29),(21.5,24)],'hairG','fringeL',shade=sh)
    poly(im,[(42,19.5),(35,19.5),(36.5,24),(39.5,28),(42.5,24)],'hairG','fringeR',shade=sh)
    face(im,iris=('iris1','iris2','iris3','iris4'))
    return im,R,F,E
# ---------------- オルカ（女性）: 鉱山の組合代表。大柄でたくましい。ヘルメット、ひとつ結びの三つ編み、頬の傷 ----------------
def orca():
    R,F,E=mk({'hairO':['#2a1c14','#4a3020','#6a4a30','#8a6a48'],'helmet':['#586070','#8890a0','#b8c0cc','#e8eef4'],'vestO':['#a84a0c','#d8701c','#f89c34','#ffc860'],'stripe':['#a8a090','#d8d4c0','#f8f4e0','#ffffff'],'shirtO':['#4a4e5a','#6a707e','#8a90a0','#b0b8c8'],'lamp':['#c09030','#f0cc50','#fff0a0','#ffffff'],'pick':['#4a2c14','#6a4222','#8a5c34','#b0804a'],'steel':['#586070','#8890a0','#b8c0cc','#e8eef4'],'glove':['#3a2418','#5a3a24','#7a5238','#9a6a48'],'scar':['#a86a58']*4},
             {'iris1':'#4a3820','iris2':'#7a5a30','iris3':'#c09860','iris4':'#f0e0b8','brow':'#2a1c14','lash':'#1c1008','mouth':'#9a4a44','blush':'#d89078'},{'hairO':'#140c08','helmet':'#2c323c','vestO':'#6a2c08','stripe':'#6a6458','shirtO':'#262a32','lamp':'#6a4a10','pick':'#2a160c','steel':'#2c323c','glove':'#241208','scar':'#7a4a3c'})
    im=Img(72,104)
    # 背中のつるはし
    capsule(im,(57,22),(58,98),2.0,2.0,'pick','pickShaft')
    poly(im,[(48,18),(58,14),(67,20),(65,24),(58,19),(50,23)],'steel','pickHead',shade=lambda x,y,nx,ny:(ny*-0.6+0.3))
    # 三つ編み（右肩から胸へ）
    pts=[(48,30),(51,40),(50,52),(52,62),(51,72)]
    for i in range(len(pts)-1): capsule(im,pts[i],pts[i+1],3.6-i*0.3,3.4-i*0.3,'hairO','braid%d'%i,bulge=0.4)
    for (px,py) in ((51,40),(50,52),(52,62)): ellipse(im,px,py,4.0,1.5,'vestO','knot%d'%py)
    ellipse(im,51,75,2.6,3.0,'hairO','btip')
    legs(im,mat='pants',xs=((29.5,29,28.5),(42.5,43,43.5)),r=(4.9,4.1,3.3),hip_y=66)
    poly(im,[(23,90),(34,90),(35,98),(37,101),(22,101),(22.5,96)],'boots','bootL'); poly(im,[(37,90),(48,90),(49.5,96),(50,101),(35,101),(36.5,98)],'boots','bootR')
    for x in range(22,38): im.set(x,101,'boots',-1.0,'bootL')
    for x in range(35,51): im.set(x,101,'boots',-1.0,'bootR')
    for x in range(24,34): im.set(x,91,'leather',0.6,'cuffL'); im.set(x,92,'leather',-0.2,'cuffL')
    for x in range(38,47): im.set(x,91,'leather',0.6,'cuffR'); im.set(x,92,'leather',-0.2,'cuffR')
    # 腕（たくましい。手袋）
    capsule(im,(48,44),(55,57),3.8,3.3,'shirtO','armR',bulge=0.5); capsule(im,(55,57),(54,67),3.3,2.9,'shirtO','armR2')
    ellipse(im,55,70,3.6,3.6,'glove','handR')
    capsule(im,(24,44),(17,57),3.8,3.3,'shirtO','armL',bulge=0.5); capsule(im,(17,57),(18,67),3.3,2.9,'shirtO','armL2')
    poly(im,[(12.5,63),(20.5,63),(20.5,67),(12.5,67)],'leather','cuffA')
    ellipse(im,17,70,3.6,3.6,'glove','handL')
    # 胴: 広い肩、はっきりしたくびれ、オレンジのベスト＋反射の帯
    poly(im,[(23,41),(49,41),(47.5,50),(44.5,55),(47,62),(25,62),(27.5,55),(24.5,50)],'shirtO','torso',shade=lambda x,y,nx,ny:(nx*LIGHT[0]+ny*LIGHT[1])*-0.7+0.28)
    poly(im,[(24,41),(48,41),(46.5,50),(43.5,55),(46,62),(26,62),(28.5,55),(25.5,50)],'vestO','vest',shade=lambda x,y,nx,ny:(nx*LIGHT[0]+ny*LIGHT[1])*-0.7+0.3)
    for yy in (49,56):
        for x in range(23,49):
            if im.part[yy][x]=='vest': im.set(x,yy,'stripe',0.8,'vest'); im.set(x,yy+1,'stripe',0.1,'vest')
    for y in range(41,62): im.set(36,y,'vestO',-1.0,'vest')
    poly(im,[(25,60),(47,60),(50,76),(22,76)],'pants','skirt',shade=lambda x,y,nx,ny:(nx*LIGHT[0])*-0.6+0.15)
    poly(im,[(24,59),(48,59),(48,62.5),(24,62.5)],'leather','belt',shade=lambda x,y,nx,ny:(ny*-0.5+0.3))
    ellipse(im,36,60.7,2.6,2.2,'steel','buckle')
    capsule(im,(36,32),(36,41),3.2,3.8,'skin','neck')
    head(im,cx=36,cy=24,rx=10.8,ry=11.2)
    # ヘルメット（小さめ）とランプ、ひさし
    poly(im,[(24,19),(25,10),(30,3.5),(36,2),(42,3.5),(47,10),(48,19),(45,16.5),(27,16.5)],'helmet','helmet',shade=lambda x,y,nx,ny:(nx*LIGHT[0]+ny*LIGHT[1])*-0.7+0.35)
    poly(im,[(22,16.5),(50,16.5),(51,20),(21,20)],'helmet','brim',shade=lambda x,y,nx,ny:(ny*-0.5+0.25))
    ellipse(im,36,8,3.6,3.0,'lamp','lamp'); im.set(35,6,'lamp',1.3,'lamp')
    for x in range(27,46): im.set(x,10,'helmet',0.9,'helmet') if x%3 else None
    # 前髪（ヘルメットの下に短く）
    sh=hairshade_factory(cx=36,cy=17,hx=30,hy=12)
    poly(im,[(25,19.5),(33,19.5),(31,25),(27,27),(24.5,23)],'hairO','fringeL',shade=sh)
    poly(im,[(47,19.5),(39,19.5),(41,25),(45,27),(47.5,23)],'hairO','fringeR',shade=sh)
    poly(im,[(33,19.5),(39,19.5),(38,22.5),(34,22.5)],'hairO','fringeM',shade=sh)
    for sx in (-1,1):
        capsule(im,(36+sx*11.5,20),(36+sx*12,33),2.4,1.6,'hairO','side'+str(sx),bulge=0.3)
    face(im,cx=36,iris=('iris1','iris2','iris3','iris4'),smile=False,blush=True)
    for k in range(7): im.fixed(26+k,21,'brow','brow'); im.fixed(40+k,21,'brow','brow')
    # 頬の傷（右）
    for k in range(5): im.fixed(42+k//2,26+k,'scar','scar')
    return im,R,F,E
if __name__=="__main__":
    for name,fn in (("guide",guide),("orca",orca)):
        im,R,F,E=fn()
        n=finish(im,R,F,E,SEPS+[('helmet','brim'),('lamp','helmet'),('vestO','torso'),('goggleBand','hairMass'),('gogL','goggleBand'),('gogR','goggleBand'),('lensL','gogL'),('lensR','gogR'),('knot40','braid0')],name+"2")
        print(name,n)
