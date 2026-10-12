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
leadin="E5:1 A5:1 C#6:2~ B5:1 G#5:1 E5:2~ C#6:1 A5:1 F#5:2~ A5:1 F#5:1 D5:2~"
secs=[("leadin",prog*2,[("R:4 "*8,S)]),
 ("intro",prog*2,[(intro,S),(intro2,S)]),
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

# ---------- ここから v2: ベースの旋律・ドラムのアレンジ・起伏 ----------
root={A:("A2","A1"),E:("E3","E2"),F:("F#3","F#2"),D:("D3","D2")}
fifth={A:"E3",E:"B3",F:"C#4",D:"A3"}
SC=[9,11,13,14,16,18,20]  # A長調 (A B C# D E F# G#) の半音番号（A=9, 以降は +半音）
def midi(n):
    m=re.match(r"^([A-G]#?)(-?\d)$",n); return NAMES.index(m.group(1))+12*(int(m.group(2))+1)
def scale_up(rootname,deg):
    r=midi(rootname); pcs=sorted({p%12 for p in [9,11,13,14,16,18,20]})
    # r から始めて、A長調の音を deg 個ぶん上がる
    n=r; k=0
    while k<deg:
        n+=1
        if n%12 in pcs: k+=1
    return n
def nn(m): return f"{NAMES[m%12]}{m//12-1}"
def bpat(r1,pat):  # pat=[(度数,拍)]
    return " ".join(f"{nn(scale_up(r1,d))}:{b}" for d,b in pat)
M1=[(0,1),(0,.5),(2,.5),(4,1),(2,1)]
M2=[(0,.5),(4,.5),(7,1),(4,.5),(2,.5),(0,1)]
M3=[(0,1.5),(2,.5),(4,1),(5,1)]
M4=[(0,1),(2,1),(4,1),(3,.5),(2,.5)]
PUMP=[(0,.5),(0,.5),(7,.5),(0,.5)]*2
PUMP2=[(0,.5),(7,.5),(0,.5),(7,.5),(4,.5),(7,.5),(5,.5),(4,.5)]
RISE=[(0,.5),(0,.5),(2,.5),(2,.5),(4,.5),(4,.5),(5,.5),(6,.5)]
RUN=[(0,.25),(2,.25),(4,.25),(7,.25),(4,.25),(2,.25),(4,.25),(7,.25),(9,.25),(7,.25),(4,.25),(7,.25),(9,.25),(11,.25),(9,.25),(7,.25)]
LONG=[(0,2),(4,1),(2,1)]
def S(ch,syms): return syms
def slots(sym,tok_map=None):
    out=[]
    for c in sym.replace(" ",""):
        out.append("R:0.25" if c=="." else f"{c}:0.25")
    return " ".join(out)
def tomslots(lst):  # lst: 16個。None=休み、音名=タム
    return " ".join("R:0.25" if t is None else f"{t}:0.25" for t in lst)
# キックの型
KP={"sparse":["X...........x...","X.......x.....x.","X.....x.x.......","X.........x...x."],
    "drive":["X.x...x.x.x...x.","X.x...x.x.....x.","X.x...x.x.x...xx","X.x...x.x.....x."],
    "chorus":["X.x.X.x.X.x...x.","X.x.X.x.X.x.x.x.","X.x.X.x.X.x...x.","X.x.X.x.X.x.x.xx"],
    "double":["XxxxXxxxXxxxXxxx","XxxxXxxxXxxxxxXx","X.xxx.xxX.xxx.xx","XxxxXx.xXxxxXxxx"],
    "floor":["X...X...X...X...","X...X...X...X..."]}
def hatp(kind,i):
    if kind=="quiet": return "x.o.x.o.x.o.x.o."
    if kind=="norm": return "X.x.x.x.X.x.x.x."
    if kind=="open": return "X.x.x.x.X.x.x.X." if i%2 else "X.x.x.x.X.x.X.x."
    if kind=="quarter": return "x...x...x...x..."
    if kind=="ride": return "X.x.X.x.X.x.X.x."
    return "x.x.x.x.x.x.x.x."
FILLS=[("snare",None),("tom",None),("mix",None),("stop",None)]
def fill(k):
    # 戻り値: (kick, snare, tom)  ※スネアとハットはこの小節の後半(8〜15)を置き換える
    if k%4==0:  return ("X.......X.......", "....X...ooxxxXXX", [None]*16)
    if k%4==1:  return ("X.......X.......", "....X...........", [None]*8+["C4","C4","A3","A3","G3","G3","E3","E3"])
    if k%4==2:  return ("X.......X.......", "....X...xxXX....", [None]*12+["A3","G3","E3","A2"])
    return ("X.......X...X...", "....X.......XXXX", [None]*16)
def drum_bar(sec,i,n):
    kick=snare=hat=crash=None; tom=[None]*16
    isl=(i==n-1) or (i%8==7)           # 8小節の最後
    first=(i==0)
    K=KP["drive"][i%4]; Sn="....X.......X..." ; Ht=hatp("norm",i); crash_on=False
    if sec=="intro":
        K=KP["drive"][i%4]; crash_on=first
    elif sec=="verse":
        half=i<8
        if sec_idx_hint.get("v",0)==0 and half:
            K=KP["sparse"][i%4]; Sn="............x..." if i%2 else "....o.......x..."; Ht=hatp("quiet",i)
        elif sec_idx_hint.get("v",0)==0:
            K=KP["drive"][i%4]; Sn="....x.......x..."; Ht=hatp("norm",i)
        else:
            K=KP["drive"][i%4]; Sn="....x..o....x..o"; Ht=hatp("norm",i); crash_on=first
    elif sec=="pre":
        K=KP["floor"][0] if i>=4 else KP["drive"][i%4]
        Sn="....x.......x..." if i<4 else ("x...x...x...x..." if i<7 else "xxxxxxxxXXXXXXXX")
        Ht=hatp("norm",i)
    elif sec=="chorus":
        K=KP["chorus"][i%4]; Sn="....X.......X..."; Ht=hatp("open",i); crash_on=(i%2==0)
        if sec_idx_hint.get("c",0)==2 and i>=8: K=KP["double"][i%4]; crash_on=True
    elif sec=="bridge":
        if i<8:
            K="X.......x..x...." if i%2==0 else "X...........x..."; Sn="............o..." if i%2 else "................"; Ht=hatp("quarter",i)
        elif i<12: K="X...X...X...X..."; Sn="....x.......x..."; Ht=hatp("ride",i)
        elif i<15: K="X...X...X...X..."; Sn="x.x.x.x.x.x.x.x."; Ht=hatp("ride",i)
        else: K="X..............."; Sn="xxxxxxxxxxXXXXXX"; Ht="................"
    elif sec=="solo":
        K=KP["drive"][i%4]; Ht=hatp("ride" if i>=8 else "norm",i); crash_on=(i%4==0)
    elif sec=="outro":
        if i<4: K=KP["chorus"][i%4]; Sn="....X.......X..."; Ht=hatp("open",i); crash_on=(i%2==0)
        elif i<7: K="X.......X......."; Sn="........X......."; Ht=hatp("quarter",i); crash_on=(i==4)
        else: K="X..............."; Sn="X..............."; Ht="X..............."; crash_on=True
    # フィル
    tk=None
    if isl and sec not in("outro",) and not(sec=="bridge" and i<15 and i!=7) and not(sec=="pre" and i==n-1) and not(sec=="bridge" and i==15):
        fk=sec_idx_hint.get("f",0); sec_idx_hint["f"]=fk+1
        fkk,fsn,ftom=fill(fk)
        K=K[:8]+fkk[8:]; Sn=Sn[:8]+fsn[8:]; Ht=Ht[:8]+"x.x....."+"" if False else Ht[:8]+"........"; tom=ftom
    return K,Sn,Ht,tom,crash_on
sec_idx_hint={}
sw1=[];sw2=[];sw3=[]
third={A:"C#4",E:"G#3",F:"A3",D:"F#4"}
def sw(c,i):
    # イントロの和音の重なり: 1〜2小節=1本、3〜4=2本、5〜6=3本、7〜8=3本（だんだん大きく）
    if i is None:
        for L in (sw1,sw2,sw3): L.append("R:4")
        return
    if i==7:   # 8小節目はドラムの入り。和音は休み、ディレイの尾だけが鳴る
        for L in (sw1,sw2,sw3): L.append("R:4")
        return
    sw1.append(tr(f"{root[c][0]}:4",-5))
    sw2.append(tr(f"{fifth[c]}:4",-5) if i>=2 else "R:4")
    sw3.append(tr(f"{third[c]}:4",-5) if i>=4 else "R:4")
chords=[];lead=[];lead2=[];gl=[];gr=[];bass=[];kick=[];snare=[];hat=[];tomp=[];crashp=[]
vcount=ccount=0
for name,ch,lds in secs:
    chords+=ch
    for ld,sh in lds:
        lead.append(tr(ld,sh))
        beats=sum(float(x.split(":")[1].rstrip("~^_!'")) for x in ld.split())
        lead2.append(tr(ld,sh-12) if (name=="chorus" and ccount==2) else f"R:{beats:g}")
    n=len(ch)
    if name=="verse": sec_idx_hint["v"]=vcount; vcount+=1
    if name=="chorus": sec_idx_hint["c"]=ccount; ccount+=1
    for i,c in enumerate(ch):
        r0,r1=root[c]
        if name!="leadin": sw(c,None)
        if name=="leadin":
            for L in (gl,gr,bass,kick,tomp,crashp): L.append("R:4")
            snare.append(slots("xxxxxxxxxxxxXXXX") if i==7 else "R:4")
            hat.append(slots(hatp("norm",0)) if i==7 else "R:4"); sw(c,i); continue
        # --- ギター ---
        def g8(note,acc=True,short=False,fx=""):
            t=[]
            for k in range(8):
                suf=("!" if acc and k in(0,4) else "")+("'" if short else "")
                t.append(f"{note}:0.5{suf}")
            return " ".join(t)
        def g16(note): return " ".join(f"{note}:0.25"+("!" if k in(0,4,8,12) else "") for k in range(16))
        L_=R_=None
        if name=="intro": L_=g8(r0); R_=g8(fifth[c])
        elif name=="verse":
            v=sec_idx_hint["v"]
            if v==0 and i<8: L_=g8(r0,True,True); R_="R:4"
            elif v==0: L_=g8(r0,True,True); R_=" ".join([f"{fifth[c]}:1"]*4)
            else: L_=g8(r0,True,True); R_=g8(fifth[c],True,True)
        elif name=="pre":
            if i<4: L_=g8(r0,True,True); R_=g8(fifth[c],True,True)
            elif i<7: L_=g8(r0); R_=g8(fifth[c])
            else: L_=g16(r0); R_=g16(fifth[c])
        elif name=="chorus":
            c_=sec_idx_hint["c"]
            if c_==2 and i>=8: L_=g16(r0) if i%2==1 else g8(r0); R_=g16(fifth[c]) if i%2==1 else g8(fifth[c])
            else: L_=g8(r0); R_=g8(fifth[c])
            if i%4==3 and not(c_==2 and i>=8): L_=" ".join([f"{r0}:0.5"]*6+[f"{r0}:0.25"]*4); R_=" ".join([f"{fifth[c]}:0.5"]*6+[f"{fifth[c]}:0.25"]*4)
        elif name=="bridge":
            if i<8: L_=f"{r0}:4"; R_=f"{fifth[c]}:4"
            elif i<15: L_=f"{r0}:2 {r0}:2"; R_=f"{fifth[c]}:2 {fifth[c]}:2"
            else: L_="R:4"; R_="R:4"
        elif name=="solo": L_=g8(r0); R_=g8(fifth[c])
        elif name=="outro":
            if i<4: L_=g8(r0); R_=g8(fifth[c])
            elif i<7: L_=f"{r0}:2 {r0}:2"; R_=f"{fifth[c]}:2 {fifth[c]}:2"
            else: L_="A2:1 R:3"; R_="E3:1 R:3"
        gl.append(tr(L_,S_) if False else tr(L_,-5)); gr.append(tr(R_,-5))
        # --- ベース（旋律） ---
        if name=="intro": b=bpat(r1,[M3,M2][i%2])
        elif name=="verse":
            v=sec_idx_hint["v"]; b=bpat(r1,[M1,M2,M3,M4][(i+(2*v))%4])
        elif name=="pre": b=bpat(r1,RUN if i==7 else RISE)
        elif name=="chorus":
            c_=sec_idx_hint["c"]; b=bpat(r1,PUMP)
            if i%4==3: b=bpat(r1,M4)
            if c_==2 and i%8==7: b=bpat(r1,RUN)
        elif name=="bridge": b=bpat(r1,LONG) if i<15 else "R:4"
        elif name=="solo": b=bpat(r1,PUMP2)
        elif name=="outro":
            if i<4: b=bpat(r1,PUMP)
            elif i<7: b=bpat(r1,LONG)
            else: b="A1:1 R:3"
        bt=tr(b,-5).split()
        def cap(t):
            m=re.match(r"^([A-G]#?)(-?\d)(:.*)$",t)
            if not m: return t
            v=midi(m.group(1)+m.group(2))
            while v>50: v-=12
            return f"{nn(v)}{m.group(3)}"
        bass.append(" ".join(cap(t) for t in bt))
        # --- ドラム ---
        Kk,Sn,Ht,tom,cr=drum_bar(name,i,n)
        kick.append(slots(Kk)); snare.append(slots(Sn)); hat.append(slots(Ht)); tomp.append(tomslots(tom))
        crashp.append(slots("X..............." if cr else "................"))
def part(inst,role,notes,vol,pan,patch,amp,extra):
    d={"instrument":inst,"role":role,"volume":vol,"pan":pan,"amp":amp,"notes":" ".join(notes)}
    if patch: d["patch"]=patch
    d.update(extra); return d
song={"title":"melocore-pluck-v2","description":"メロコアパンク v2。ベースが旋律を弾き、ドラムはアクセント・特殊フィル入り。静かな部分→盛り上がり→爆発の起伏つき。ギターは弦モデル pluck-deepair",
 "bpm":172,"beats":4,"chords":" ".join(chords),"barsPerChord":1,"repeats":1,"feel":"rock","tone":"rock",
 "autoAccompaniment":False,"dynamics":"natural","human":0.25,"fills":False,
 "parts":[
  part("leadGuitar","イントロの和音1（根音・エコー）",sw1,0.15,-0.4,"cleanGuitar","clean",{"reverb":0.5,"chorus":0,"echo":{"repeats":1,"time":"dotted8","decay":0.6}}),
  part("leadGuitar","イントロの和音2（5度・エコー）",sw2,0.15,0.4,"cleanGuitar","clean",{"reverb":0.5,"chorus":0,"echo":{"repeats":1,"time":"dotted8","decay":0.6}}),
  part("leadGuitar","イントロの和音3（3度・エコー）",sw3,0.16,0,"cleanGuitar","clean",{"reverb":0.5,"chorus":0,"echo":{"repeats":1,"time":"dotted8","decay":0.6}}),
  part("leadGuitar","リフ（左・ルート）",gl,0.16,-0.6,"cleanGuitar","overdrive",{"reverb":0.08,"chorus":0}),
  part("leadGuitar","リフ（右・5度）",gr,0.16,0.6,"cleanGuitar","overdrive",{"reverb":0.08,"chorus":0}),
  part("leadGuitar","メロディ／ソロ",lead,0.3,0,"cleanGuitar","clean",{"reverb":0.18,"chorus":0}),
  part("leadGuitar","メロディ（最後のサビだけオクターブ下を重ねる）",lead2,0.22,0.1,"cleanGuitar","clean",{"reverb":0.15,"chorus":0}),
  part("bass","ベース（旋律）",bass,0.6,0,None,"auto",{"bright":0.3}),
  part("kick","キック",kick,0.26,0,None,"auto",{}),part("snare","スネア",snare,0.2,0,None,"auto",{}),part("hihat","ハイハット",hat,0.09,0.3,None,"auto",{}),
  part("tom","タム",tomp,0.2,0,None,"auto",{}),part("crash","クラッシュ",crashp,0.16,0.2,None,"auto",{})]}
print(json.dumps(song,ensure_ascii=False))
