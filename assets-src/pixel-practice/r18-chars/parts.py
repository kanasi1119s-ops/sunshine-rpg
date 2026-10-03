import math
from chargen import *
def face(im, cx=32, cy=24, iris=('iris1','iris2','iris3','iris4'), brow='brow', lash='lash', mouth='mouth', blush=True, eyeW=5, gap=5.2, smile=True, lashes=True):
    for sign in (1,-1):
        ex = cx - sign*gap/1.0*1.0
        ex = cx + (-gap if sign>0 else gap) + (0.5 if sign<0 else -0.5)
        ex = cx - 5.2 if sign>0 else cx + 5.2
        for dy in range(6):
            for dx in range(5):
                xx=int(ex-2.5+dx); yy=int(cy+dy); nx=(dx-2)/2.5; ny=(dy-2.5)/3
                if nx*nx+ny*ny<=1.1: im.fixed(xx,yy,'eyeW','eye')
        for dy in range(5):
            for dx in range(4):
                xx=int(ex-2+dx); yy=int(cy+1+dy); nx=(dx-1.5)/2.1; ny=(dy-2)/2.6
                if nx*nx+ny*ny<=1.0: im.fixed(xx,yy,iris[0] if dy<2 else iris[1] if dy<4 else iris[2],'eye')
        for dy in (cy+2,cy+3,cy+4): im.fixed(int(ex-0.5),int(dy),'pupil','eye')
        im.fixed(int(ex-1.5),int(cy+1),'white','eye'); im.fixed(int(ex-1.5),int(cy+2),'white','eye'); im.fixed(int(ex+0.5),int(cy+4),iris[3],'eye')
        for dx in range(-3,3): im.fixed(int(ex-0.5+dx),int(cy-1),lash,'eye')
        if lashes: im.fixed(int(ex-3.5 if sign>0 else ex+2.5),int(cy),lash,'eye')
    for k in range(5): im.fixed(int(cx-8+k),int(cy-3-(1 if k>=3 else 0)),brow,'brow'); im.fixed(int(cx+4+k),int(cy-3-(1 if k<=1 else 0)),brow,'brow')
    im.fixed(int(cx),int(cy+6),'skinD','nose'); im.fixed(int(cx),int(cy+7),'skinD','nose')
    for k in range(4): im.fixed(int(cx-2+k),int(cy+10-(1 if (k in (0,3) and smile) else 0)),mouth,'mouth')
    if blush:
        for x in (cx-5,cx-4,cx+4,cx+5): im.fixed(int(x),int(cy+7),'blush','blush')
def legs(im, hip_y=66, knee_y=81, ankle_y=95, mat='pants', xs=((28.5,27.5,27),(35.5,36.5,37.5)), r=(4.6,3.8,3.0)):
    for i,(hx,kx,ax) in enumerate(xs):
        n='LR'[i]
        capsule(im,(hx,hip_y),(kx,knee_y),r[0],r[1],mat,'leg'+n,bulge=0.3)
        capsule(im,(kx,knee_y),(ax,ankle_y),r[1],r[2],mat,'leg2'+n)
def boots(im, mat='boots', cuff='leather', top=91):
    poly(im,[(22.5,top),(30.5,top),(31.5,top+7),(33.5,top+10),(21,top+10),(21.5,top+5)],mat,'bootL')
    poly(im,[(33.5,top),(41.5,top),(42.5,top+5),(43,top+10),(30.5,top+10),(32.5,top+7)],mat,'bootR')
    for x in range(21,34): im.set(x,top+10,mat,-1.0,'bootL')
    for x in range(31,44): im.set(x,top+10,mat,-1.0,'bootR')
    for x in range(23,31): im.set(x,top+1,cuff,0.6,'cuffL'); im.set(x,top+2,cuff,-0.2,'cuffL')
    for x in range(34,42): im.set(x,top+1,cuff,0.6,'cuffR'); im.set(x,top+2,cuff,-0.2,'cuffR')
    # つま先の光
    im.set(22,top+8,mat,0.9,'bootL'); im.set(23,top+8,mat,0.9,'bootL'); im.set(42,top+8,mat,0.9,'bootR')
def head(im, cx=32, cy=24, rx=10.6, ry=11.4):
    ellipse(im,cx,cy,rx,ry,'skin','head',light_bias=0.15)
    ellipse(im,cx-10.4,cy+1.5,1.7,2.4,'skin','earL'); ellipse(im,cx+10.4,cy+1.5,1.7,2.4,'skin','earR')
def neck(im, y0=33, y1=41, x=32): capsule(im,(x,y0),(x,y1),3.2,3.6,'skin','neck')
def finish(im, ramps, fixed, edge, seps_extra=(), name="out"):
    import json
    R={**ramps}
    for k,v in fixed.items(): R[k]=[v]*4
    parts=sorted({p for row in im.part for p in row if p})
    hair_like=[p for p in parts if p.startswith('hair') or p.startswith('fringe') or p in ('head','band','brim')]
    seps=[]
    for i,a in enumerate(hair_like):
        for b in hair_like[i+1:]: seps.append((a,b))
    seps+=list(seps_extra)
    out,colors=render(im,R,edge,seps)
    txt,pal=to_text(out,colors)
    open(name+".txt","w").write(txt); json.dump(pal,open("pal-"+name+".json","w"))
    return len(pal)
