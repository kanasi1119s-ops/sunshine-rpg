# メロコアパンク（長め・低め・ほんの少し歪み）。使い方: python3 melocore-pluck-long.py > ../melocore-pluck-long.json
# 旋律は A のキーで書いて、書き出しの時に半音で下げる（リード -5、ソロ -17、リフ・ベースは根音の表で -5）
import json,re
NAMES=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
def tr(notes,semi):
    out=[]
    for t in notes.split():
        m=re.match(r"^([A-G]#?)(-?\d)(:.*)$",t)
        if not m: out.append(t); continue
        n=NAMES.index(m.group(1))+12*(int(m.group(2))+1)+semi
        out.append(f"{NAMES[n%12]}{n//12-1}{m.group(3)}")
    return " ".join(out)
A,E,F,D,B,C="A","E","F#m","D","B","C"
prog=[A,E,F,D]
intro="A5:1 C#6:1 B5:1 A5:1 G#5:1 B5:1 E6:2 F#5:1 A5:1 C#6:1 A5:1 F#5:1 A5:1 D6:2"
intro2="A5:1 C#6:1 E6:2 B5:1 G#5:1 E5:2 F#5:1 A5:1 C#6:2~ D6:1 C#6:1 A5:2~"
V1="R:1 A4:0.5 B4:0.5 C#5:1 B4:1 R:1 B4:0.5 C#5:0.5 E5:1 C#5:1 A4:1 C#5:1 F#5:1 E5:1 D5:1 A4:1 D5:2"
V2="R:1 A4:0.5 B4:0.5 C#5:1 B4:1 R:1 B4:0.5 C#5:0.5 E5:1 G#5:1 F#5:1 E5:1 C#5:1 A4:1 D5:1 F#5:1 A5:2~"
V3="A4:0.5 B4:0.5 C#5:0.5 E5:0.5 C#5:1 B4:1 B4:0.5 C#5:0.5 E5:0.5 G#5:0.5 E5:1 B4:1 C#5:0.5 E5:0.5 F#5:0.5 A5:0.5 F#5:1 E5:1 D5:1 F#5:1 A5:2~"
pre_prog=[D,E,F,E]*2
P1="D5:1 F#5:1 A5:2 B5:1 G#5:1 E5:2 C#5:1 F#5:1 A5:2 B5:1 G#5:1 B5:2~"
P2="A5:0.5 B5:0.5 A5:0.5 F#5:0.5 D5:1 F#5:1 B5:0.5 G#5:0.5 E5:0.5 G#5:0.5 B5:2 C#6:0.5 A5:0.5 F#5:0.5 A5:0.5 C#6:1 A5:1 B5:2 G#5:2"
chorus_prog=[F,D,A,E]*2
c1="C#5:1 E5:1 F#5:2~ D5:1 F#5:1 A5:2~ E5:1 A5:1 C#6:2~ B5:1 G#5:1 E5:2 C#5:0.5 E5:0.5 F#5:1 A5:1 F#5:1 D5:0.5 F#5:0.5 A5:1 B5:2 C#6:1 B5:0.5 A5:0.5 E5:2 G#5:1 B5:1 E6:2~"
c3="E5:1 F#5:1 A5:2~ F#5:1 A5:1 D6:2~ C#6:1 A5:1 E6:2~ D6:1 B5:1 G#5:2 C#5:0.5 E5:0.5 F#5:1 A5:1 F#5:1 D5:0.5 F#5:0.5 A5:1 B5:2 C#6:1 B5:0.5 A5:0.5 E5:2 G#5:1 B5:1 E6:2~"
c4="E5:1 F#5:1 A5:2~ F#5:1 A5:1 D6:2~ C#6:1 A5:1 E6:2~ D6:1 B5:1 G#5:2 C#6:0.5 B5:0.5 A5:1 F#5:1 A5:1 D6:1 C#6:1 A5:2 C#6:1 E6:1 C#6:2 B5:2 G#5:1 E5:1"
br_prog=[D,A,F,E]*4
B1="F#5:4~ E5:4~ C#5:4~ B4:4~"
B2="A5:2~ F#5:2 E5:2~ C#5:2 C#6:2~ A5:2 B5:2~ G#5:2"
solo1=("C#6:0.5 E6:0.5 C#6:0.5 A5:0.5 C#6:1 E6:1 B5:0.5 G#5:0.5 B5:0.5 E6:0.5 D6:1 B5:1 "
 "F#5:0.25 A5:0.25 C#6:0.25 A5:0.25 F#5:0.25 A5:0.25 C#6:0.25 E6:0.25 D6:1 C#6:1 D6:0.5 A5:0.5 F#5:0.5 A5:0.5 D6:2~ "
 "A5:0.25 C#6:0.25 E6:0.25 C#6:0.25 A5:0.25 C#6:0.25 E6:0.25 C#6:0.25 A5:0.25 C#6:0.25 E6:0.25 C#6:0.25 A5:0.25 C#6:0.25 E6:0.25 C#6:0.25 "
 "G#5:0.25 B5:0.25 E6:0.25 B5:0.25 G#5:0.25 B5:0.25 E6:0.25 B5:0.25 E6:1 D6:0.5 B5:0.5 "
 "C#6:0.5 E6:0.5 C#6:0.5 A5:0.5 F#5:0.5 A5:0.5 C#6:0.5 E6:0.5 E6:2^~ D6:1 A5:1")
solo2=("E6:0.5 C#6:0.5 A5:0.5 C#6:0.5 E6:1 C#6:1 G#5:0.5 B5:0.5 E6:0.5 B5:0.5 G#5:1 B5:1 "
 "F#5:0.25 A5:0.25 C#6:0.25 A5:0.25 F#5:0.25 A5:0.25 C#6:0.25 A5:0.25 D6:0.25 C#6:0.25 A5:0.25 F#5:0.25 A5:1 A5:0.5 D6:0.5 A5:0.5 F#5:0.5 D6:2~ "
 "C#6:1 E6:1 C#6:0.5 A5:0.5 C#6:1 B5:1 E6:1 B5:0.5 G#5:0.5 B5:1 "
 "A5:0.25 C#6:0.25 E6:0.25 C#6:0.25 A5:0.25 C#6:0.25 E6:0.25 C#6:0.25 F#5:0.5 A5:0.5 C#6:1 D6:3~ A5:1")
outro="C#6:1 B5:1 A5:2 G#5:2 B5:2 F#5:1 A5:1 C#6:2~ D6:2 C#6:2 B5:1 A5:1 G#5:2 B5:2 E6:2~ A5:4~ R:4"
# (名前, 和音, [リード旋律, シフト])
S=-5; SS=-17
secs=[("intro",prog*2,[(intro,S),(intro2,S)]),
 ("verse",prog*4,[(V1,S),(V2,S),(V1,S),(V3,S)]),
 ("pre",pre_prog,[(P1,S),(P2,S)]),
 ("chorus",chorus_prog*2,[(c1,S),(c3,S)]),
 ("verse",prog*4,[(V2,S),(V3,S),(V3,S),(V1,S)]),
 ("pre",pre_prog,[(P1,S),(P2,S)]),
 ("chorus",chorus_prog*2,[(c3,S),(c4,S)]),
 ("intro",prog*2,[(intro,S),(intro2,S)]),
 ("bridge",br_prog,[(B1,S),(B2,S),(B1,S-12),(B2,S)]),
 ("solo",prog*4,[(solo1,SS),(solo2,SS)]),
 ("pre",pre_prog,[(P1,S),(P2,S)]),
 ("chorus",chorus_prog*2,[(c1,S),(c4,S)]),
 ("outro",prog+[A,E,A,A],[(outro,S)])]
root={A:("A2","A1"),E:("E3","E2"),F:("F#3","F#2"),D:("D3","D2")}
fifth={A:"E3",E:"B3",F:"C#4",D:"A3"}
chords=[];lead=[];gl=[];gr=[];bass=[];kick=[];snare=[];hat=[]
for name,ch,lds in secs:
    chords+=ch
    for ld,sh in lds: lead.append(tr(ld,sh))
    n=len(ch)
    for i,c in enumerate(ch):
        r0,r1=root[c]
        q=name=="bridge" and i<8
        step="1" if q else "0.5"; cnt=4 if q else 8
        gl.append(tr(" ".join([f"{r0}:{step}"]*cnt),S)); gr.append(tr(" ".join([f"{fifth[c]}:{step}"]*cnt),S)); bass.append(tr(" ".join([f"{r1}:0.5"]*8),S))
        last=(i==n-1) or i%8==7
        if name=="outro" and i==n-1:
            kick.append("x:1 R:3"); snare.append("x:1 R:3"); hat.append("x:1 R:3"); continue
        if name=="bridge" and i<8:
            kick.append("x:1 R:1 x:1 R:1"); snare.append("R:1 x:1 R:1 x:1"); hat.append("x:1 x:1 x:1 x:1"); continue
        kick.append("x:0.5 x:0.5 R:0.5 R:0.5 x:0.5 x:0.5 R:0.5 R:0.5")
        if name=="pre": snare.append("x:0.25 x:0.25 x:0.25 x:0.25 x:0.25 x:0.25 x:0.25 x:0.25 x:0.25 x:0.25 x:0.25 x:0.25 x:0.25 x:0.25 x:0.25 x:0.25" if i==n-1 else "x:1 x:1 x:1 x:1")
        else: snare.append("R:1 x:1 R:1 x:0.25 x:0.25 x:0.25 x:0.25" if last else "R:1 x:1 R:1 x:1")
        hat.append(" ".join(["x:0.5"]*8))
gl[-1]=tr("A2:1 R:3",S); gr[-1]=tr("E3:1 R:3",S); bass[-1]=tr("A1:1 R:3",S)
def part(inst,role,notes,vol,pan,patch,amp,extra):
    d={"instrument":inst,"role":role,"volume":vol,"pan":pan,"amp":amp,"notes":" ".join(notes)}
    if patch: d["patch"]=patch
    d.update(extra); return d
song={"title":"melocore-pluck-long","description":"メロコアパンク（長め・低め）。弦モデル pluck-deepair のギター。リフにだけほんの少し歪み（overdrive）",
 "bpm":172,"beats":4,"chords":" ".join(chords),"barsPerChord":1,"repeats":1,"feel":"rock","tone":"rock",
 "autoAccompaniment":False,"dynamics":"natural","human":0.25,
 "parts":[
  part("leadGuitar","リフ（左・ルート）",gl,0.16,-0.6,"cleanGuitar","overdrive",{"reverb":0.08,"chorus":0}),
  part("leadGuitar","リフ（右・5度）",gr,0.16,0.6,"cleanGuitar","overdrive",{"reverb":0.08,"chorus":0}),
  part("leadGuitar","メロディ／ソロ",lead,0.3,0,"cleanGuitar","clean",{"reverb":0.18,"chorus":0}),
  part("bass","ベース",bass,0.2,0,None,"auto",{}),
  part("kick","キック",kick,0.22,0,None,"auto",{}),part("snare","スネア",snare,0.18,0,None,"auto",{}),part("hihat","ハイハット",hat,0.08,0.3,None,"auto",{})]}
print(json.dumps(song,ensure_ascii=False))
