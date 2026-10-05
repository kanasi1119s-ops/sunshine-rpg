"""全環の手直し: 輪の中に、おだやかな大きな目と光の筋、輪のひび（2026-10-05）"""
import json, math, random
from PIL import Image
n='zenkan'
rows=[list(r) for r in open(n+'.txt').read().split('\n') if r]
H,W=len(rows),len(rows[0])
pal=json.load(open(n+'.json'))
cols={'q':'#2a1a08','r':'#fff4d8','s':'#e2cf9c','t':'#a88c50','u':'#ffc23a','v':'#d27a08','w':'#120804','x':'#ffffff','y':'#5a3c0c','z':'#fff0a8','o':'#8a5a10','p':'#ffe27a'}
assert not set(cols) & set(pal)
pal.update(cols)
cx,cy=128,128
for k in range(12):
  a=k*math.pi/6+0.26
  for r in range(44,80):
    x,y=int(round(cx+r*math.cos(a))),int(round(cy+r*math.sin(a)))
    if rows[y][x]=='.' and (r%2==0 or r<58) and not (r>70 and r%3): rows[y][x]='z' if r<60 else 'p'
A,B=60,27
for y in range(cy-B-6,cy+B+3):
  for x in range(cx-A-2,cx+A+3):
    u=(x-cx)/A
    if abs(u)>1: continue
    h=B*(1-u*u)**0.85; hu=h*0.78
    top=cy-hu; bot=cy+h
    if top+1.2<=y<=bot-1.2:
      t=(y-top)/(bot-top); e=abs(u)
      rows[y][x]='t' if (t<0.18 or e>0.82) else ('s' if (t<0.32 or e>0.6 or t>0.8) else 'r')
    elif top-4<=y<top+1.2: rows[y][x]='q' if y>=top-0.5 else ('o' if y>=top-2.5 else 'y')
    elif bot-1.2<y<=bot+1.0: rows[y][x]='q'
for y in range(cy-30,cy+31):
  for x in range(cx-30,cx+31):
    d=math.hypot(x-cx,y-cy)
    if rows[y][x] in 'rst' and d<=23:
      ang=math.atan2(y-cy,x-cx)
      if d<=8.5: c='w'
      elif d>=21: c='q'
      else:
        streak=(int((ang+math.pi)*14/math.pi))%2
        c='u' if (d<15 and streak) or (y<cy-2 and d<19) else ('v' if streak or d>17 else 'u')
        if y<cy-12: c='v'
      rows[y][x]=c
for p in ((-5,-6),(-4,-6),(-5,-5),(-4,-5),(-3,-6),(4,3)): rows[cy+p[1]][cx+p[0]]='x'
random.seed(3)
for k in range(9):
  a=random.uniform(0,2*math.pi); r=random.uniform(88,118)
  x,y=cx+r*math.cos(a),cy+r*math.sin(a)
  for s in range(random.randint(8,16)):
    a+=random.uniform(-0.5,0.5); x+=math.cos(a+math.pi/2)*0.9+random.uniform(-.6,.6); y+=math.sin(a+math.pi/2)*0.9
    xi,yi=int(x),int(y)
    if 0<=xi<W and 0<=yi<H and rows[yi][xi]!='.' and math.hypot(xi-cx,yi-cy)>80: rows[yi][xi]='y'
open(n+'_fix.txt','w').write('\n'.join(''.join(r) for r in rows)+'\n')
used={c for r in rows for c in r}-{'.'}
P={k:v for k,v in pal.items() if k in used}; json.dump(P,open(n+'_fix.json','w'))
im=Image.new('RGBA',(W,H))
for y,r in enumerate(rows):
  for x,c in enumerate(r):
    if c!='.': im.putpixel((x,y),tuple(int(P[c][i:i+2],16) for i in (1,3,5))+(255,))
im.save(n+'_fix.png'); print(len(P),'色')
