import json,sys,copy
sys.path.insert(0,'/home/claude/wt-mix/tools/composer')
from gset_to_parts import string_parts
s=json.load(open('gc2.json'))
base=[p for p in s['parts'] if 'strum' not in p]
tmpl={k:v for k,v in s['parts'][-1].items() if k not in ('strum','double','notes','role','volume','pan','chordGain')}
chords='F#m D E C#m F#m D E C#m D E C#m F#m Bm E A A'.split()
LO={"F#m":["F#2","C#3","F#3","A3","C#4","F#4"],"D":[None,"A2","D3","A3","D4","F#4"],"E":["E2","B2","E3","G#3","B3","E4"],
 "C#m":[None,"C#3","G#3","C#4","E4","G#4"],"Bm":[None,"B2","F#3","B3","D4","F#4"],"A":[None,"A2","E3","A3","C#4","E4"]}
HI={"F#m":[None,"F#3","C#4","F#4","A4","C#5"],"D":[None,"D3","A3","D4","F#4","A4"],"E":[None,"E3","B3","E4","G#4","B4"],
 "C#m":[None,"C#3","G#3","C#4","E4","G#4"],"Bm":["B2","F#3","B3","D4","F#4","B4"],"A":["A2","E3","A3","C#4","E4","A4"]}
def gtr(name,pan,segA,segS,voA,voS,velA,velS,vol,drive):
    a=string_parts(segA+[(None,0,8)],chords,voA,140,vel_scale=velA)
    b=string_parts([(None,0,8)]+segS,chords,voS,140,vel_scale=velS)
    out=[]
    for i in range(6):
        for tag,n in (('A',a[i]),('S',b[i])):
            if all(t.startswith('R:') for t in n.split()): continue
            p=copy.deepcopy(tmpl); p.update(instrument='distGuitar',role=f'{name}{tag}・弦{i+1}',volume=vol,pan=pan,notes=n,humanTiming=0,ampDrive=round(drive*0.4,3))
            out.append(p)
    return out
L=gtr('Lギター',-0.75,[('01_Rock3-117-Bb_comp',0,8)],[('00_Rock3-117-Bb_comp',8,8)],LO,LO,0.85,1.0,0.028,0.42)
R=gtr('Rギター',0.75,[('04_Rock3-148-C_comp',0,8)],[('00_Rock3-148-C_comp',0,8)],HI,HI,0.8,0.95,0.025,0.42)
s['parts']=base+L+R; s['title']='ギター聞き比べd'; s['description']='本物のギタリストの弾き方（GuitarSet）'
json.dump(s,open('gd.json','w'),ensure_ascii=False)
print(len(s['parts']))
