# 蝶々のメロコア 4（B マイナー版の butterfly-3 から、調・コード進行・テンポを大きく変えた明るい版。E メジャー、BPM200、184小節）。フロアタムの「ドン！」つき。
# （以下は 3 の説明）蝶々のメロコア 3。「もっと自然な音楽に」: 機械的なくり返し（自動の羽ばたき・同じ4小節の貼りつけ）をやめ、全部手で歌わせる。
# 旋律は問いと答え・息つぎ・くり返しの変化つき。ギター・ベース・ドラムは、場面と小節の位置で型を選ぶ（同じ型を機械的に回さない）。
# B マイナー、BPM176、168小節。最後の2回のサビは全音上げ。音は melocore と同じ（pluck-deepair / pick / rock-clean）。
import json,re,random
NAMES=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
def midi(n):
    m=re.match(r"^([A-G]#?)(-?\d)$",n); return NAMES.index(m.group(1))+12*(int(m.group(2))+1)
def nn(m): return f"{NAMES[m%12]}{m//12-1}"
def tr(notes,semi):
    out=[]
    for t in notes.split():
        m=re.match(r"^([A-G]#?)(-?\d)(:.*)$",t)
        out.append(t if not m else nn(midi(m.group(1)+m.group(2))+semi)+m.group(3))
    return " ".join(out)
def fold(notes,hi=88):
    out=[]
    for t in notes.split():
        m=re.match(r"^([A-G]#?)(-?\d)(:.*)$",t)
        if not m: out.append(t); continue
        n=midi(m.group(1)+m.group(2))
        while n>hi: n-=12
        out.append(nn(n)+m.group(3))
    return " ".join(out)
def harm(notes):
    out=[]
    for t in notes.split():
        m=re.match(r"^([A-G]#?)(-?\d)(:.*)$",t)
        if not m: out.append(t); continue
        n=midi(m.group(1)+m.group(2))
        if n%12 in SCALE:
            k=0
            while k<2:
                n+=1
                if n%12 in SCALE: k+=1
        else: n+=3
        out.append(nn(n)+m.group(3))
    return " ".join(out)
def beats(s): return sum(float(x.split(":")[1].rstrip("~^_!'")) for x in s.split())
def bars(*b):
    for x in b: assert abs(beats(x)-4)<1e-9,(x,beats(x))
    return " ".join(b)
PC={"E":4,"B":11,"C#m":1,"A":9,"F#m":6,"G#m":8,"F#":6,"C#":1,"A#m":10,"D#m":3}
QUAL={"C#m":"m","F#m":"m","G#m":"m","A#m":"m","D#m":"m"}
def root_g(c):
    m=36+PC[c]
    while m<40: m+=12
    return m
def root_b(c):
    m=24+PC[c]
    while m<28: m+=12
    return m
def third(c): return 3 if QUAL.get(c)=="m" else 4
# ================= 旋律（E メジャー／C#マイナーの明るい曲）=================
INTRO=bars("R:1 G#4:0.5 C#5:0.5 E5:1 G#5:1","A5:0.5 G#5:0.5 E5:1 C#5:0.5 E5:0.5 A4:1","B4:0.5 E5:0.5 G#5:1 B5:1.5 G#5:0.5","F#5:1 D#5:1 B4:1 D#5:0.5 F#5:0.5",
  "E5:0.5 G#5:0.5 C#6:1.5 B5:0.5 G#5:1","C#6:0.5 A5:0.5 E5:1 A5:0.5 C#6:0.5 E6:1","C#6:1 A5:1 F#5:1 A5:0.5 C#6:0.5","B5:0.5 D#6:0.5 B5:1 F#5:2~")
Va=bars("R:1 B4:0.5 E5:0.5 G#5:1.5 E5:0.5","D#5:0.5 F#5:0.5 B5:1 F#5:1 D#5:1","E5:1 G#5:1 C#6:1.5 B5:0.5","G#5:2 R:1 D#5:0.5 B4:0.5")
Vb=bars("C#5:0.5 E5:0.5 A5:1 G#5:0.5 E5:0.5 C#5:1","B4:1 E5:1 G#5:2~","A5:1.5 F#5:0.5 C#5:1 F#5:1","D#5:1 F#5:1 B5:2~")
Vc=bars("R:0.5 B4:0.5 E5:1 G#5:1 B5:1","A5:1 F#5:0.5 D#5:0.5 B4:1 D#5:1","G#5:1 E5:0.5 C#5:0.5 E5:1 G#5:1","B5:1.5 G#5:0.5 D#5:2~")
Vd=bars("C#6:1 A5:1 E5:2~","F#5:1 B5:1 D#6:2~","E6:1 C#6:1 G#5:1 E5:1","D#5:2~ F#5:1 R:1")
VERSE1=Va+" "+Vb+" "+Vc+" "+Vd
VERSE2=Vc+" "+Vb+" "+Va+" "+Vd
PRE=bars("E5:1 A5:1 C#6:2~","D#6:1 B5:1 F#5:2","G#5:1 B5:1 D#6:2~","E6:1 C#6:1 G#5:1 E5:1","A5:1 C#6:1 A5:1 F#5:1","B5:1 D#6:1 B5:1 G#5:1","C#6:1 E6:1 C#6:1 A5:1","D#6:3~ R:1")
CP1=bars("E5:1 A5:1 C#6:2~","D#6:1.5 B5:0.5 F#5:2","G#5:1 B5:1 D#6:2~","E6:1 C#6:0.5 B5:0.5 G#5:1 E5:1")
CP2=bars("A5:0.5 C#6:0.5 E6:1 C#6:2~","D#6:1 B5:1 F#5:1 B5:1","G#5:1 B5:1 E6:2~","D#6:1.5 B5:0.5 G#5:2")
CP3=bars("E5:0.5 A5:0.5 C#6:1 E6:2~","D#6:1 B5:1 D#6:2~","B5:1 D#6:1 B5:1 G#5:1","E5:1 G#5:1 C#6:2~")
CP3b=bars("E5:0.5 A5:0.5 C#6:1 E6:1 C#6:1","D#6:0.5 B5:0.5 D#6:1 F#5:2","B5:1 D#6:1 B5:1 G#5:1","E5:1 G#5:1 C#6:2~")
CP4=bars("A5:1 C#6:1 E6:2~","C#6:1 A5:1 E5:2","D#6:1 F#5:1 B5:2~","B5:3~ R:1")
CP4x=bars("A5:1 C#6:1 E6:2~","C#6:1 A5:1 E5:2","D#6:1 F#5:1 B5:2~","B5:4~")
CH1=CP1+" "+CP2+" "+CP3+" "+CP4
CH2=CP1+" "+CP2+" "+CP3b+" "+CP4
CH3=CP1+" "+CP2+" "+CP3b+" "+CP4x
INTER=bars("R:2 G#4:1 B4:1","D#5:3~ F#5:1","E5:1 A5:1 C#6:2~","B5:1.5 G#5:0.5 E5:2~","R:1 G#4:1 C#5:1 E5:1","D#5:2~ B4:2~","C#5:1 E5:1 A5:2","D#6:2~ B5:1 F#5:1")
SOLO=bars("G#4:0.5 C#5:0.5 E5:1 G#5:1.5 E5:0.5","A5:0.25 G#5:0.25 E5:0.25 C#5:0.25 E5:0.5 A5:0.5 C#6:1 A5:1","B5:0.5 G#5:0.5 E5:1 G#5:0.25 B5:0.25 E6:0.5 B5:1","D#6:1.5 B5:0.5 F#5:2^~",
  "C#5:0.25 E5:0.25 G#5:0.25 E5:0.25 C#5:0.25 E5:0.25 G#5:0.25 E5:0.25 C#6:2","A5:0.5 E5:0.5 C#6:1 A5:0.5 E5:0.5 A5:1","C#6:0.25 A5:0.25 F#5:0.25 A5:0.25 C#6:0.25 A5:0.25 F#5:0.25 A5:0.25 E6:2^~","D#6:1 B5:1 F#5:1 D#5:1",
  "G#5:0.5 B5:0.5 E6:1 B5:0.5 G#5:0.5 E5:1","D#6:0.25 B5:0.25 F#5:0.25 B5:0.25 D#6:0.25 B5:0.25 F#5:0.25 B5:0.25 D#6:2","E6:1 C#6:0.5 G#5:0.5 E5:1 G#5:1","A5:1 C#6:1 E6:2^~",
  "F#5:0.25 A5:0.25 C#6:0.25 A5:0.25 F#5:0.25 A5:0.25 C#6:0.25 A5:0.25 C#6:1 A5:1","C#6:0.5 E6:0.5 C#6:0.5 A5:0.5 E5:2","D#6:1 B5:0.5 F#5:0.5 B5:2^~","B5:3~ R:1")
DRIVE=bars("E5:0.5 E5:0.5 G#5:1 B5:2","F#5:0.5 F#5:0.5 B5:1 D#6:2~","E5:0.5 E5:0.5 G#5:1 C#6:2~","C#6:1 A5:1 E5:2","E5:0.5 G#5:0.5 B5:1 E6:2~","D#6:1 B5:1 F#5:2","A5:1 C#6:1 E6:2~","D#6:2~ F#5:1 R:1")
BREAK=bars("E5:2~ C#5:2~","B4:2~ G#4:2~","A4:3~ C#5:1","G#4:4~","C#5:2~ E5:2~","G#5:2~ E5:2~","D#5:3~ F#5:1","B4:2~ F#4:2~",
           "C#5:1 F#5:1 A5:2","B5:2 D#6:2","C#6:2~ E6:1 C#6:1","D#6:3~ R:1","A5:1 C#6:1 A5:1 F#5:1","B5:1 D#6:1 B5:1 G#5:1","F#5:1 D#6:1 B5:2~","B5:2 R:2")
OUTRO=CP1+" "+CP2+" "+bars("C#6:1 A5:1 E5:2~","D#6:1 B5:1 F#5:2~","E5:1 G#5:1 B5:2~","E5:2~ R:2","A5:2~ E5:2~","B5:2~ F#5:2~","G#5:2~ E5:2~","E5:3~ R:1")
INP=["C#m","A","E","B","C#m","A","F#m","B"]
VP=["E","B","C#m","G#m","A","E","F#m","B","E","B","C#m","G#m","A","B","C#m","B"]
PREP=["A","B","G#m","C#m","F#m","G#m","A","B"]
CP=["A","B","G#m","C#m","A","B","E","G#m","A","B","G#m","C#m","F#m","A","B","B"]
CPU=["B","C#","A#m","D#m","B","C#","F#","A#m","B","C#","A#m","D#m","G#m","B","C#","C#"]
IP=["E","B","A","E","C#m","G#m","A","B"]
SOP=["C#m","A","E","B","C#m","A","F#m","B","E","B","C#m","A","F#m","A","B","B"]
DRP=["E","B","C#m","A","E","B","A","B"]
BRP=["A","E","F#m","C#m","A","E","B","B","F#m","G#m","A","B","F#m","G#m","B","B"]
OUP=["A","B","G#m","C#m","A","B","E","G#m","A","B","E","E","A","B","E","E"]
SCALE=[4,6,8,9,11,1,3]
S=[("intro",INP,0,INTRO,None,0),("verse",VP,0,VERSE1,None,0),("pre",PREP,0,PRE,None,0),("chorus",CP,0,CH1,None,0),
   ("inter",IP,0,INTER,None,0),("verse",VP,1,VERSE2,None,0),("pre",PREP,1,PRE,None,0),("chorus",CP,1,CH2,harm,0),
   ("solo",SOP,0,SOLO,harm,0),("drive",DRP,0,DRIVE,None,0),("bridge",BRP,0,BREAK,None,0),("chorus",CPU,2,CH3,harm,2),("chorus",CPU,3,CH3,harm,2),("outro",OUP,0,OUTRO,None,0)]
rnd=random.Random(1011)
# ================= ドラム =================
def slots(sym): return " ".join("R:0.25" if c=="." else f"{c}:0.25" for c in sym)
def tomslots(l): return " ".join("R:0.25" if t is None else f"{t}:0.25" for t in l)
VK=["X.......x.x.....","X.....x.x.......","X.......x.....x.","X..x....x.x.....","X.x.....x.....x.","X.......X.x...x."]
CK=["X.x.X.x.X.x...x.","X.x.X.x.X.x.x.x.","X.x.X.x.X.x...x.","X.x.X.x.X.x.x.xx","X...X.x.X.x.X.x."]
DK=["XxxxXxxxXxxxXxxx","XxxxXxxxXxxxxxXx","X.xxx.xxX.xxx.xx","XxxxXx.xXxxxXxxx"]
SNV=["....X.......X...","....X..o....X...","....X.......X..o","....X..o....X.o."]
FL="A2"  # フロアタム（重く低い）
FILLS=[("X.......X.......","....X...ooxxxXXX",[None]*16),
       ("X.......X.......","....X...........",[None]*8+["C4","C4","A3","A3","G3","G3",FL,FL]),
       ("X.......X.......","....X...xxXX....",[None]*12+["A3","G3",FL,FL]),
       ("X.......X...X...","....X.......XXXX",[None]*16),
       ("X.......X.......","....X.......x.xX",[None]*12+["C4",None,FL,FL])]
after_fill=[False]
def drum_bar(kind,idx,i,n):
    K="X..............."; Sn="................"; Ht="................"; tom=[None]*16; cr=False; fl=None
    if kind=="intro":
        if i>=4:
            K=rnd.choice(VK); Sn=rnd.choice(SNV); Ht="x.x.x.x.x.x.x.x."; cr=(i==4)
            if i==7: K="X..............."; Sn="xxxxxxxxxxxxXXXX"; Ht="................"
    elif kind=="verse":
        K=rnd.choice(VK); Sn=rnd.choice(SNV) if not(idx==0 and i<4) else "............x..."
        Ht=rnd.choice(["x.x.x.x.x.x.x.x.","X.x.x.x.X.x.x.x.","x.x.x.x.x.x.x.xo"]) if idx==1 else ("x...x...x...x..." if i<4 else "x.x.x.x.x.x.x.x.")
        cr=(i==0 and idx==1)
        if i in(7,15) : fl=rnd.randrange(5)
        elif i==3 and idx==1: fl=1
    elif kind=="pre":
        K="X...X...X...X..." if i>=4 else rnd.choice(VK)
        Sn="....x.......x..." if i<4 else ("x...x...x...x..." if i<7 else "xxxxxxxxXXXXXXXX"); Ht="x.x.x.x.x.x.x.x."
        if i==7: K="X.......X......."
    elif kind=="chorus":
        K=(DK if (idx>=2 and i>=8) else CK)[rnd.randrange(5 if idx<2 else 4)] if (idx>=2 and i>=8) else rnd.choice(CK)
        Sn="....X.......X..."; Ht=rnd.choice(["X.x.x.x.X.x.x.x.","X.x.x.x.X.x.X.x.","X.x.x.xoX.x.x.x."]); cr=(i%4==0) or (i==8)
        if i in(3,7,11): fl=rnd.randrange(5) if i!=3 else None
        if i==7 or i==15: fl=3 if i==7 else None
        if i==3 and idx==3: fl=2
    elif kind=="inter":
        K="X..............." if i%2==0 else "X.......x......."; Ht="x...x...x...x..."; Sn="............o..." if i%4==3 else "................"
        if i==7: Sn="xxxxxxxxXXXXXXXX"; K="X.......X......."; Ht="................"
    elif kind=="solo":
        K=rnd.choice(VK) if i<8 else rnd.choice(CK); Sn="....X.......X..."; Ht="X.x.X.x.X.x.X.x."; cr=(i%8==0)
        if i in(7,): fl=rnd.randrange(5)
        if i==15: Sn="xxxxxxxxxxxxXXXX"; K="X.......X......."; Ht="................"
    elif kind=="bridge":
        if i<8: K="X..............." if i%2==0 else "X.......x......."; Ht="o...o...o...o..."
        elif i<15: K="X...X...X...X..."; Sn="....x.......x..." if i<12 else "x.x.x.x.x.x.x.x."; Ht="x.x.x.x.x.x.x.x."
        else: K="X.......X......."; Sn="xxxxxxxxxxxxXXXX"
    elif kind=="outro":
        if i<4: K=rnd.choice(CK); Sn="....X.......X..."; Ht="X.x.x.x.X.x.x.x."; cr=(i%2==0)
        elif i<7: K="X.......X......."; Sn="........X......."; Ht="x...x...x...x..."; cr=(i==4)
        else: K="X..............."; Sn="X..............."; Ht="X..............."; cr=True
    if kind=="chorus" and i in(0,8) and idx>=0: tom[0]=FL; cr=True  # サビの頭は、キック・クラッシュ・フロアタムの「ドン！」
    if kind=="drive":
        K="X...X...X...X..."; Sn="....X.......X..."; Ht="X.x.X.x.X.x.X.x."; cr=(i%4==0)
        tom=[FL,None,None,None,None,None,FL,None,FL,None,None,None,None,None,FL,FL] if i%2==0 else [FL,None,None,FL,None,None,FL,None,None,None,FL,None,FL,None,FL,FL]
        if i==7: Sn="xxxxxxxxxxxxXXXX"; K="X..............."; tom=[None]*16
    if after_fill[0] and i>0 and kind!="drive":  # フィルの次の小節の頭は、ドン！と入る
        tom[0]=FL; cr=True
    after_fill[0]=False
    if fl is not None:
        k,s,t=FILLS[fl]; K=K[:8]+k[8:]; Sn=Sn[:8]+s[8:]; Ht=Ht[:8]+"........"; tom=t; after_fill[0]=True
    return K,Sn,Ht,tom,cr
# ================= ベース =================
def bass_bar(kind,idx,i,c,n):
    r=root_b(c); t=third(c)
    def seq(l):
        out=[]
        for d,b in l:
            m=r+d
            while m>50: m-=12
            out.append(f"{nn(m)}:{b}")
        return " ".join(out)
    P8=[(0,.5)]*8
    PUMP=[(0,.5),(0,.5),(12,.5),(0,.5),(0,.5),(0,.5),(12,.5),(7,.5)]
    DRV=[(0,.5),(0,.5),(0,.5),(0,.5),(0,.5),(0,.5),(7,.5),(0,.5)]
    SYN=[(0,1),(0,.5),(0,.5),(0,1),(7,.5),(12,.5)]
    MEL=[(0,1),(t,.5),(7,.5),(12,1),(7,1)]
    MEL2=[(0,1.5),(7,.5),(12,1),(t+12,1)]
    WALK=[(0,.5),(0,.5),(t,.5),(7,.5),(12,.5),(7,.5),(t,.5),(0,.5)]
    END=[(0,1),(0,.5),(7,.5),(12,.5),(7,.25),(t,.25),(0,1)]
    LONG=[(0,2),(7,1),(t,1)]
    UP=[(0,.5),(0,.5),(t,.5),(t,.5),(7,.5),(7,.5),(12,.5),(14,.5)]
    end=(i%4==3)
    if kind=="intro": return "R:4" if i<4 else seq(END if end else SYN)
    if kind=="verse": return seq(END if (i%8==7) else rnd.choice([MEL,MEL2,SYN,WALK] if idx else [MEL,MEL2,SYN]))
    if kind=="pre": return seq(WALK if i==7 else UP)
    if kind=="chorus": return seq(END if (i%8==7) else (rnd.choice([P8,PUMP,DRV]) if not end else MEL2))
    if kind=="drive": return seq(rnd.choice([PUMP,DRV]) if i%4!=3 else END)
    if kind=="inter": return seq(LONG) if i%2==0 else seq(MEL2)
    if kind=="solo": return seq(rnd.choice([PUMP,DRV,P8]) if not end else MEL)
    if kind=="bridge": return seq(LONG) if i<15 else "R:4"
    if kind=="outro": return seq(PUMP) if i<4 else (seq(LONG) if i<7 else f"{nn(r)}:1 R:3")
# ================= ギター =================
def gt(c,kind,idx,i,n):
    r=root_g(c); f=r+7
    def cell(m,name):
        a=nn(m)
        return {"e8":" ".join(f"{a}:0.5"+("!" if k in(0,4) else "")+"'" for k in range(8)),
                "e8o":" ".join(f"{a}:0.5"+("!" if k in(0,4) else "") for k in range(8)),
                "sync":f"{a}:1! {a}:0.5 {a}:0.5 {a}:1 {a}:0.5 {a}:0.5",
                "push":f"{a}:0.5! {a}:0.5 R:0.5 {a}:0.5 {a}:1! {a}:0.5 {a}:0.5",
                "ring":f"{a}:2! {a}:1 {a}:0.5 {a}:0.5",
                "hit":f"{a}:1! R:3",
                "s16":" ".join(f"{a}:0.25"+("!" if k%4==0 else "") for k in range(16)),
                "whole":f"{a}:4",
                "rest":"R:4"}[name]
    def pick(opts): return rnd.choice(opts)
    last=(i==n-1)
    if kind=="intro":
        nm=("rest","rest") if i<4 else (("e8","e8") if i<7 else ("s16","s16"))
    elif kind=="verse":
        x=pick(["e8","e8","push"]); nm=(x,pick(["rest","e8"]) if idx==0 and i<8 else x)
        if last: nm=("hit","hit")
    elif kind=="pre": nm=("e8","e8") if i<7 else ("s16","s16")
    elif kind=="chorus":
        x=pick(["sync","push","sync","ring"]) if i%4!=3 else pick(["e8o","push"]); nm=(x,x)
        if i==15: nm=("hit","hit")
    elif kind=="drive": nm=(("push","push") if i<7 else ("hit","hit"))
    elif kind=="inter": nm=("rest","rest")
    elif kind=="solo":
        x=pick(["sync","push","e8o"]); nm=(x,x)
        if last: nm=("hit","hit")
    elif kind=="bridge":
        if i<8: nm=("rest","whole")
        elif i<12: nm=("whole","whole")
        elif i<15: nm=("e8o","e8o")
        else: nm=("rest","rest")
    elif kind=="outro":
        nm=(("sync","sync") if i<4 else (("whole","whole") if i<7 else ("hit","hit")))
    return cell(r,nm[0]),cell(f,nm[1])
chords=[];lead=[];lead2=[];gl=[];gr=[];bass=[];kick=[];snare=[];hat=[];tomp=[];crashp=[]
for kind,ch,idx,ld,hf,up in S:
    n=len(ch)
    assert abs(beats(ld)-4*n)<1e-6,(kind,beats(ld),4*n)
    l1=fold(tr(ld,up) if up else ld)
    lead.append(l1)
    lead2.append(fold(tr(hf(ld),up) if up else hf(ld)) if hf else f"R:{4*n}")
    for i,c in enumerate(ch):
        chords.append(c)
        L,R=gt(c,kind,idx,i,n); gl.append(L); gr.append(R)
        bass.append(bass_bar(kind,idx,i,c,n))
        K,Sn,Ht,tom,cr=drum_bar(kind,idx,i,n)
        kick.append(slots(K)); snare.append(slots(Sn)); hat.append(slots(Ht)); tomp.append(tomslots(tom)); crashp.append(slots("X..............." if cr else "................"))
def part(inst,role,notes,vol,pan,patch,amp,extra):
    d={"instrument":inst,"role":role,"volume":vol,"pan":pan,"amp":amp,"notes":" ".join(notes)}
    if patch: d["patch"]=patch
    d.update(extra); return d
G={"noRestrike":True,"chorus":0}
song={"title":"butterfly-4","description":"蝶々をイメージしたメロコアパンク（仮・試作）。明るい E メジャー（C#マイナー）、BPM200、フロアタムのドン！つき。手で歌わせた旋律と、場面で型を選ぶ演奏。最後の2回のサビは全音上げ。ギターは弦モデル pluck-deepair",
 "bpm":200,"beats":4,"chords":" ".join(chords),"barsPerChord":1,"repeats":1,"feel":"rock","tone":"rock",
 "autoAccompaniment":False,"dynamics":"natural","human":0.7,"drumMix":{"tom":{"tune":-4,"level":1.4,"spread":0.5}},"fills":False,
 "parts":[
  part("leadGuitar","メロディ／ソロ",lead,0.3,0,"cleanGuitar","clean",{**G,"reverb":0.2}),
  part("leadGuitar","ハモリ（3度上）",lead2,0.2,0.25,"cleanGuitar","clean",{**G,"reverb":0.2}),
  part("leadGuitar","リフ（左・ルート）",gl,0.16,-0.6,"cleanGuitar","overdrive",{**G,"reverb":0.08}),
  part("leadGuitar","リフ（右・5度）",gr,0.16,0.6,"cleanGuitar","overdrive",{**G,"reverb":0.08}),
  part("bass","ベース（旋律）",bass,0.6,0,None,"auto",{"bright":0.3}),
  part("kick","キック",kick,0.26,0,None,"auto",{}),part("snare","スネア",snare,0.2,0,None,"auto",{}),part("hihat","ハイハット",hat,0.09,0.3,None,"auto",{}),
  part("tom","タム",tomp,0.3,0,None,"auto",{}),part("crash","クラッシュ",crashp,0.16,0.2,None,"auto",{})]}
print(json.dumps(song,ensure_ascii=False))
