import sys, json, math
sys.path.insert(0,".")
from chargen import *
W,H=16,32
def ramp3(d,m,l): return [d,m,m,m]   # つや消し: 影と地の2段だけ（ハイライトなし）
# キャラごとの設定: 色・髪型・小物
CHARS={
 "ユーリ":dict(hair=('#5a2e18','#8a4a24','#c0782c'),skin=('#d49a76','#f0c49c','#ffdcbc'),top=('#1c5058','#2a7c88','#58bcc0'),bottom=('#4a2c1a','#6a4228','#8a5c38'),boot=('#2a1a12','#4a2c1a','#6a4228'),acc=('#a8480c','#e07a20','#ffb048'),eye='#1c7a50',style='spiky',scarf=True,band=True),
 "レト":dict(hair=('#3a1410','#7a2c1c','#b4502c'),skin=('#d49a76','#f0c49c','#ffdcbc'),top=('#1e2430','#40485c','#7080a0'),bottom=('#262a34','#3a4050','#586070'),boot=('#2a1a12','#4a2c1a','#6a4228'),acc=('#7a1418','#c83c34','#f87060'),eye='#a8682c',style='spiky',scarf=True,coat=True),
 "ミナ":dict(hair=('#2a5a9a','#4a8ad0','#9ad0ff'),skin=('#d49a76','#f4cca8','#ffe0c4'),top=('#a8bcd8','#e8f0fc','#ffffff'),bottom=('#7a90b4','#d0e0f4','#eef6ff'),boot=('#3a2418','#5a3a24','#7a5238'),acc=('#1c4a8a','#3a80d8','#88ccff'),eye='#1c4aa0',style='long',dress=True),
 "ガイド":dict(hair=('#7a5a14','#c8982c','#fff0a0'),skin=('#d49a76','#f0c49c','#ffdcbc'),top=('#d8d0c0','#f4ecdc','#ffffff'),bottom=('#2a5a3a','#3a8a50','#6ac088'),boot=('#3a2418','#5a3a24','#7a5238'),acc=('#1c6a3c','#34a45c','#8af0a8'),eye='#2a6a40',style='twin',skirt=True,goggle=True,vest=('#4a2c14','#6a4222','#9a6c3c')),
 "オルカ":dict(hair=('#2a1c14','#4a3020','#7a5a40'),skin=('#b07850','#d49a70','#eab890'),top=('#a84a0c','#e07a20','#ffb048'),bottom=('#4a2c1a','#6a4228','#8a5c38'),boot=('#2a1a12','#4a2c1a','#6a4228'),acc=('#586070','#8890a0','#d8e0ec'),eye='#4a3820',style='helmet',vestorange=True,shirt=('#4a4e5a','#6a707e','#9aa0b0')),
}
def eye_light(h):
    # 目のハイライトは白ではなく、目の色を35%だけ明るくした近い色にする
    r,g,b=[int(h[i:i+2],16) for i in (1,3,5)]
    return '#%02x%02x%02x'%tuple(int(v+(255-v)*0.35) for v in (r,g,b))
def S(i): return '#10%02x%02x'%(16+i,16+i)   # 役割色（実行時に置き換える目印）
ARCH_BASE=dict(hair=(S(0),S(1),S(2)),skin=(S(3),S(4),S(5)),top=(S(6),S(7),S(8)),bottom=(S(9),S(10),S(11)),boot=(S(12),S(13),S(14)),acc=(S(15),S(16),S(17)),eye='#1a1420')
CHARS['素体-short']=dict(ARCH_BASE,style='spiky')
CHARS['素体-long']=dict(ARCH_BASE,style='long',skirt=True)
CHARS['素体-twin']=dict(ARCH_BASE,style='twin',skirt=True)
def mats(c):
    R={}
    R['hair']=ramp3(*c['hair']); R['skin']=ramp3(*c['skin']); R['top']=ramp3(*c['top']); R['bottom']=ramp3(*c['bottom']); R['boot']=ramp3(*c['boot']); R['acc']=ramp3(*c['acc'])
    R['eye']=[c['eye']]*4; R['dark']=['#1a1420']*4; R['white']=['#ffffff']*4; R['gold']=ramp3('#a8701c','#e0a830','#e0a830')
    if 'vest' in c: R['vest']=ramp3(*c['vest'])
    if 'shirt' in c: R['shirt']=ramp3(*c['shirt'])
    R['steel']=ramp3('#586070','#8890a0','#8890a0')
    return R
def draw(name,dr,fr):
    c=CHARS[name]; im=Img(W,H)
    side = dr in ('left','right'); sgn = 1 if dr!='left' else -1
    cx=8
    # 歩きの揺れ: 0=立ち、1=右足前、2=左足前。体が1ドット上下する
    bob = 0 if fr==0 else -1 if False else 0
    legL = 0 if fr==0 else (-2 if fr==1 else 2)
    legR = 0 if fr==0 else (2 if fr==1 else -2)
    # 脚
    if not side:
        for sx,off in ((-1,legL),(1,legR)):
            x=cx+sx*2.3
            capsule(im,(x,23.5),(x,26+max(0,-off)*0),2.2,1.9,'bottom','leg%d'%sx)
            # 足を前後に（正面/背面は上下にずらす: 前の足が1ドット低く）
            y1=27+(1 if off>0 else 0)-(1 if off<0 else 0)
            poly(im,[(x-2.3,y1-1),(x+2.3,y1-1),(x+2.6,y1+2),(x-2.6,y1+2)],'boot','boot%d'%sx)
    else:
        for k,(off,z) in enumerate(((legL,'a'),(legR,'b'))):
            x=cx+off*0.9
            capsule(im,(cx,23.5),(x,27),2.4,2.0,'bottom','legS'+z)
            poly(im,[(x-2.2+ (sgn*0.8),26),(x+2.6*sgn+ (0),26),(x+3.2*sgn,29.5),(x-2.6,29.5)] if sgn>0 else [(x+2.2,26),(x-2.6,26),(x-3.2,29.5),(x+2.6,29.5)],'boot','bootS'+z)
    # 胴
    if name=="ミナ":
        poly(im,[(4.5,15),(11.5,15),(12.5,26),(3.5,26)],'top','body',shade=lambda x,y,nx,ny:-nx*0.35-ny*0.25+0.3)
        for x in (5,8,11): 
            for y in range(20,26):
                if im.part[y][x]=='body': im.set(x,y,'bottom',-1,'body')
        for x in range(3,13): im.set(x,25,'acc',0.4,'hem')
    elif c.get('skirt'):
        poly(im,[(5,15),(11,15),(11.5,21),(4.5,21)],'top','body',shade=lambda x,y,nx,ny:-nx*0.4+0.25)
        poly(im,[(4,20),(12,20),(13,25),(3,25)],'bottom','skirt',shade=lambda x,y,nx,ny:-nx*0.4+0.2)
    elif c.get('coat'):
        poly(im,[(4.5,15),(11.5,15),(12,27),(4,27)],'top','body',shade=lambda x,y,nx,ny:-nx*0.35+0.25)
        for y in range(15,27): im.set(8,y,'dark',-1,'body') if dr=='down' else None
    else:
        poly(im,[(4.5,15),(11.5,15),(12,24),(4,24)],'top','body',shade=lambda x,y,nx,ny:-nx*0.4-ny*0.2+0.3)
    if name=="オルカ":
        poly(im,[(5,15.5),(11,15.5),(11,23.5),(5,23.5)],'top','vest')
        for y in (18,21):
            for x in range(5,11): im.set(x,y,'white',0.8,'vest')
        if side:
            for y in range(15,24): im.set(8,y,'shirt',0.2,'vest') if False else None
    if name=="ガイド":
        poly(im,[(5,15.5),(7.2,15.5),(7.2,21),(5,21)],'vest','vestL'); poly(im,[(8.8,15.5),(11,15.5),(11,21),(8.8,21)],'vest','vestR')
    # ベルト
    if name not in ("ミナ",):
        for x in range(4,12): im.set(x,22 if not c.get('coat') else 22,'dark',-1,'belt')
    # 腕
    if not side:
        swing={0:(0,0),1:(1,-1),2:(-1,1)}[fr]
        for sx,sw in ((-1,swing[0]),(1,swing[1])):
            x=cx+sx*5.6
            capsule(im,(x,16),(x+sx*0.4,22+sw*0.8),1.7,1.5,'top','arm%d'%sx)
            ellipse(im,x+sx*0.4,23.2+sw*0.8,1.5,1.5,'skin','hand%d'%sx)
    else:
        sw={0:0,1:2,2:-2}[fr]
        capsule(im,(cx,16),(cx+sw*sgn*0.9,22.5),1.9,1.6,'top','armS')
        ellipse(im,cx+sw*sgn*0.9,23.6,1.5,1.5,'skin','handS')
    # 小物（スカーフ・ストール）
    if c.get('scarf') and dr in ('down','up'):
        poly(im,[(4.5,14),(11.5,14),(11,17),(5,17)],'acc','scarf')
        if dr=='down': poly(im,[(8.6,16),(11,16),(11,21),(9,21)],'acc','scarfTail')
    if c.get('scarf') and side:
        poly(im,[(5,14),(11,14),(10.5,17),(5.5,17)],'acc','scarf')
    if name=="ガイド" and dr in ('down','up'): poly(im,[(5,14),(11,14),(10.5,17),(5.5,17)],'acc','scarf')
    # 頭
    ellipse(im,cx,8.2,6.3,6.4,'skin','head',light_bias=0.2)
    style=c['style']
    if dr=='down':
        # 顔: 目2×2、口
        for ex in (5,9):
            im.fixed(ex,9,'eyeC','eye'); im.fixed(ex+1,9,'eyeC','eye'); im.fixed(ex,10,'eyeC','eye'); im.fixed(ex+1,10,'eyeC','eye')
            im.fixed(ex,9,'eyeL','eye')
        im.fixed(7,12,'mouth','mouth'); im.fixed(8,12,'mouth','mouth')
        for x in (4,11): im.fixed(x,11,'blush','blush')
    elif dr!='up':
        ex = 10 if dr=='right' else 5
        im.fixed(ex,9,'eyeC','eye'); im.fixed(ex,10,'eyeC','eye'); im.fixed(ex+(1 if dr=='right' else -1),9,'eyeC','eye') if False else None
        im.fixed(ex+(-1 if dr=='right' else 1),9,'eyeL','eye')
        im.fixed(ex+(1 if dr=='right' else -1),12,'mouth','mouth')
    # 髪
    def hs(x,y,nx,ny): return -nx*0.4-ny*0.5+0.25+(0.2 if (x*3+y)%5==0 else 0)
    if style=='spiky':
        if dr=='up':
            poly(im,[(1.5,11),(1.5,6),(3,2),(5,3.5),(6.5,0.5),(8,3),(10,0.5),(11,3.5),(13,2),(14.5,6),(14.5,11),(12,13),(4,13)],'hair','hairBack',shade=hs)
        else:
            outer=[(1.5,10),(1.5,6),(3,2),(5,3.5),(6.5,0.5),(8,3),(10,0.5),(11,3.5),(13,2),(14.5,6),(14.5,10),(12.5,7),(10.5,6),(8.5,8),(7,6),(5.5,7.5),(3.5,6.5)] if dr=='down' else None
            if dr=='down': poly(im,outer,'hair','hairMass',shade=hs)
            else:
                # 横顔: 後ろ髪が長く、前髪は額にかかる
                if sgn>0: pts=[(2,11),(1.5,6),(3,2),(5,3.5),(6.5,0.5),(8,3),(10,0.5),(11.5,3),(13.5,5),(13,7.5),(10.5,7),(8.5,8.5),(7,6.5),(5,10)]
                else: pts=[(14,11),(14.5,6),(13,2),(11,3.5),(9.5,0.5),(8,3),(6,0.5),(4.5,3),(2.5,5),(3,7.5),(5.5,7),(7.5,8.5),(9,6.5),(11,10)]
                poly(im,pts,'hair','hairMassS',shade=hs)
        if c.get('band') and dr!='up': 
            for x in range(2,15): im.set(x,6,'acc',0.5,'band') if im.mat[6][x] is not None else None
    elif style=='long':
        if dr=='up':
            poly(im,[(1.5,13),(1.5,5),(4,1),(12,1),(14.5,5),(14.5,13),(14,26),(2,26)],'hair','hairBack',shade=hs)
        elif dr=='down':
            poly(im,[(1.5,16),(1.5,5),(4,1),(12,1),(14.5,5),(14.5,16),(13,12),(12.5,7.5),(10.5,6),(8,7.5),(5.5,6),(3.5,7.5),(3,12)],'hair','hairMass',shade=hs)
            for sx in (0,1): capsule(im,(2.2+sx*11.6,12),(2.4+sx*11.2,22),1.6,1.2,'hair','lock%d'%sx)
        else:
            poly(im,[(2,22) if sgn>0 else (14,22),(1.5,5) if sgn>0 else (14.5,5),(4,1) if sgn>0 else (12,1),(11,1) if sgn>0 else (5,1),(14,5) if sgn>0 else (2,5),(13,8) if sgn>0 else (3,8),(9,7) if sgn>0 else (7,7),(7,12) if sgn>0 else (9,12),(5,16) if sgn>0 else (11,16)],'hair','hairMassS',shade=hs)
    elif style=='twin':
        for sx in (0,1):
            if dr!='up' or True:
                xt=1.5+sx*13
                if dr in ('down','up'):
                    capsule(im,(xt+(0.5 if sx==0 else -0.5),7),(xt+(-0.5 if sx==0 else 0.5),17),2.2,1.2,'hair','tail%d'%sx)
        if dr=='up':
            poly(im,[(1.5,11),(1.5,5),(4,1),(12,1),(14.5,5),(14.5,11),(12,13),(4,13)],'hair','hairBack',shade=hs)
        elif dr=='down':
            poly(im,[(1.5,10),(1.5,5),(4,1),(12,1),(14.5,5),(14.5,10),(12.5,7.5),(10.5,6.5),(8,8),(5.5,6.5),(3.5,7.5)],'hair','hairMass',shade=hs)
        else:
            pts=[(2,10),(1.5,5),(4,1),(11,1),(14,5),(13,8),(9,7),(7,9),(4,12)] if sgn>0 else [(14,10),(14.5,5),(12,1),(5,1),(2,5),(3,8),(7,7),(9,9),(12,12)]
            poly(im,pts,'hair','hairMassS',shade=hs)
            capsule(im,(4 if sgn>0 else 12,9),(2 if sgn>0 else 14,17),2.2,1.2,'hair','tailS')
        if c.get('goggle'):
            for x in range(2,15): im.set(x,5,'gold',0.4,'goggle') if im.mat[5][x] is not None and dr!='up' else None
            if dr=='down':
                for x in (4,5,10,11): im.set(x,4,'lens',0.8,'goggle')
    elif style=='helmet':
        poly(im,[(1.5,8),(2,4),(5,1),(11,1),(14,4),(14.5,8),(15,9),(1,9)],'steel','helmet',shade=lambda x,y,nx,ny:-nx*0.4-ny*0.5+0.3)
        im.set(8,2,'gold',1.0,'lamp'); im.set(7,2,'gold',0.5,'lamp'); im.set(9,2,'gold',0.5,'lamp')
        if dr=='down':
            for x in (3,4,11,12): im.set(x,10,'hair',0.1,'hairside'); im.set(x,11,'hair',0.1,'hairside')
        if dr=='up':
            poly(im,[(3,9),(13,9),(12,14),(4,14)],'hair','hairBack',shade=hs)
            capsule(im,(8,12),(8.5,22),1.8,1.4,'hair','braid')
        if side:
            capsule(im,(7 if sgn>0 else 9,11),(5 if sgn>0 else 11,20),1.8,1.4,'hair','braidS')
    return im
def render_sprite(name,dr,fr):
    im=draw(name,dr,fr); c=CHARS[name]
    R=mats(c)
    R['eyeC']=[c['eye']]*4; R['eyeL']=[eye_light(c['eye'])]*4; R['mouth']=['#b0584c']*4; R['blush']=['#f4a898']*4; R['lens']=['#58b0e8']*4
    EDGE={'hair':'#2a1410','skin':'#7a4a3a','top':'#1a1424','bottom':'#1a1424','boot':'#140c08','acc':'#3a1010','steel':'#2a3040','gold':'#6a4010','vest':'#2a1608','shirt':'#2a2e3a','dark':'#1a1420'}
    if name.startswith('素体'): EDGE.update({'hair':S(18),'skin':S(19),'top':S(20),'bottom':S(21),'boot':S(22),'acc':S(23)})
    out,colors=render(im,R,EDGE,[('head','hairMass'),('head','hairMassS'),('head','hairBack'),('head','helmet'),('head','band'),('body','scarf'),('legS','legS')],merge=not name.startswith('素体'))
    return out,colors
if __name__=="__main__":
    from PIL import Image
    Z=8
    names=list(CHARS)
    sheet=Image.new("RGB",(len(names)*(3*(16*Z+6)+20),4*(32*Z+6)),(61,49,96))
    for ci,n in enumerate(names):
        for r,dr in enumerate(['down','up','left','right']):
            for f in range(3):
                out,colors=render_sprite(n,dr,f)
                for y,row in enumerate(out):
                    for x,v in enumerate(row):
                        if v is None: continue
                        col=tuple(int(colors[v][i:i+2],16) for i in (1,3,5))
                        for dy in range(Z):
                            for dx in range(Z): sheet.putpixel((ci*(3*(16*Z+6)+20)+f*(16*Z+6)+x*Z+dx,r*(32*Z+6)+y*Z+dy),col)
    sheet.save("/tmp/claude-0-s/walkers.png"); print(sheet.size)
