"""全環の手直し: 輪の中に光の筋、輪のひび（2026-10-05）。目は足さない（2026-10-06、人間の指示「ボスモンスターの追加された目は全部なくして」）"""
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
