# 蝶々のメロコア 2。作り方を変えた版: すべて作曲ソフトの中で完結（外で作った音を重ねない）。B マイナー、BPM176、全168小節。
# 羽ばたきの16分アルペジオ（コードの音を行き来）が曲の芯。最後の2回のサビは全音上げ（C#マイナー）。
# 使い方: python3 butterfly-2.py > ../butterfly-2.json
import json,re,sys
NAMES=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
def midi(n):
    m=re.match(r"^([A-G]#?)(-?\d)$",n); return NAMES.index(m.group(1))+12*(int(m.group(2))+1)
def nn(m): return f"{NAMES[m%12]}{m//12-1}"
def tr(notes,semi):
    out=[]
    for t in notes.split():
        m=re.match(r"^([A-G]#?)(-?\d)(:.*)$",t)
        if not m: out.append(t); continue
        out.append(nn(midi(m.group(1)+m.group(2))+semi)+m.group(3))
    return " ".join(out)
SCALE=[11,1,2,4,6,7,9]
def harm(notes):  # 3度上のハモリ（Bマイナーの音階で2つ上。音階外の A# は +3）
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
def fold(notes,hi=88):  # 出せない高い音は1オクターブ下げる（E6 = 88 まで）
    out=[]
    for t in notes.split():
        m=re.match(r"^([A-G]#?)(-?\d)(:.*)$",t)
        if not m: out.append(t); continue
        n=midi(m.group(1)+m.group(2))
        while n>hi: n-=12
        out.append(nn(n)+m.group(3))
    return " ".join(out)
def beats(s): return sum(float(x.split(":")[1].rstrip("~^_!'")) for x in s.split())
# ---- コード ----
PC={"Bm":11,"G":7,"D":2,"A":9,"Em":4,"F#":6,"C#m":1,"E":4,"B":11}  # 根音の音名番号
QUAL={"Bm":"m","Em":"m","C#m":"m"}
def root_g(c):  # ギターの根音 E2〜D#3
    m=36+PC[c]
    while m<40: m+=12
    return m
def root_b(c):  # ベース E1〜D#2
    m=24+PC[c]
    while m<28: m+=12
    return m
def third(c): return 3 if QUAL.get(c)=="m" else 4
def hi_root(c):
    m=60+PC[c]
    while m>68: m-=12
    return m
def flutter(c,variant):
    r=hi_root(c); t=third(c)
    ct=[r,r+t,r+7,r+12,r+12+t,r+19]
    pat={0:[0,1,0,2,1,2,1,3,2,3,2,4,3,4,3,5],
         1:[5,4,5,3,4,3,4,2,3,2,3,1,2,1,2,0],
         2:[0,2,1,3,2,4,3,5,5,3,4,2,3,1,2,0],
         3:[0,1,2,3,2,1,2,3,4,3,2,3,4,5,4,3]}[variant]
    return " ".join(f"{nn(ct[k])}:0.25"+("!" if i%4==0 else "") for i,k in enumerate(pat))
def bars(*b):
    for x in b: assert abs(beats(x)-4)<1e-9,(x,beats(x))
    return " ".join(b)
# ---- 手書きの旋律（Bマイナーで書く。最後のサビは tr で +2）----
HOOK=bars("F#5:1 B5:1 D6:2~","B5:1 G5:1 D5:2~","F#5:1 A5:1 D6:2~","E5:1 A5:1 C#6:2~")
Va=bars("R:1 F#4:0.5 B4:0.5 D5:1 B4:1","D5:1.5 B4:0.5 G4:1 B4:1","A4:0.5 D5:0.5 F#5:1 E5:1 D5:1","C#5:1 E5:1 A4:2~")
Vb=bars("R:1 F#4:0.5 B4:0.5 D5:1 F#5:1","E5:1.5 D5:0.5 B4:1 D5:1","F#5:0.5 A5:0.5 F#5:1 D5:1 A4:1","E5:1 C#5:1 A4:1 C#5:1")
Vc=bars("D5:0.5 F#5:0.5 B5:1 A5:1 F#5:1","G5:1 B5:1 D6:2~","A5:0.5 F#5:0.5 D5:1 F#5:1 A5:1","E5:1 A5:1 C#6:2~")
C1=bars("D5:1 G5:1 B5:2~","A5:1 F#5:1 D5:2~","E5:1 A5:1 C#6:2~","B5:1 A5:1 F#5:1 D5:1")
C2=bars("D5:0.5 G5:0.5 B5:1 D6:1 B5:1","A5:0.5 F#5:0.5 D5:1 F#5:0.5 A5:0.5 D6:1","C#6:1 E6:1 C#6:1 A5:1","B5:2~ F#5:1 B5:1")
C3=bars("E5:1 G5:1 B5:2~","D6:1 B5:1 G5:2~","F#5:1 A5:1 D6:2~","C#6:1 E6:1 A5:2~")
C4=bars("G5:1 B5:1 E6:2~","D6:1 B5:1 D6:2","C#6:1 A#5:1 F#5:2~","R:1 F#5:0.5 A#5:0.5 C#6:1 A#5:1")
CH=C1+" "+C2+" "+C3+" "+C4
B1=bars("F#5:4~","E5:4~","D5:4~","C#5:4~")
SOLO_A=bars("B4:0.5 D5:0.5 F#5:1 E5:0.25 F#5:0.25 E5:0.25 D5:0.25 B4:1","G5:0.5 B5:0.5 D6:1 B5:0.5 G5:0.5 D5:1","F#5:0.25 A5:0.25 D6:0.25 A5:0.25 F#5:0.25 A5:0.25 D6:0.25 A5:0.25 D6:1 A5:0.5 F#5:0.5","E5:0.25 A5:0.25 C#6:0.25 A5:0.25 E5:0.25 A5:0.25 C#6:0.25 A5:0.25 C#6:2^~")
SOLO_B=bars("F#5:0.25 B5:0.25 D6:0.25 B5:0.25 F#5:0.25 B5:0.25 D6:0.25 B5:0.25 D6:1 B5:0.5 F#5:0.5","D6:0.5 B5:0.5 G5:0.5 B5:0.5 D6:1 G5:1","A5:0.25 D6:0.25 A5:0.25 F#5:0.25 A5:0.25 D6:0.25 A5:0.25 F#5:0.25 D6:1 F#6:1".replace("F#6","E6"),"E6:1 C#6:1 A5:2^~")
OUTRO=bars("D5:1 G5:1 B5:2~","A5:1 F#5:1 D5:2~","E5:1 A5:1 C#6:2~","B5:2~ F#5:2~","D5:1 G5:1 B5:2~","A5:1 F#5:1 D5:2~","B5:2~ F#5:2~","B4:3~ R:1")
# ---- 構成 ----
VP=["Bm","G","D","A"]
CP=["G","D","A","Bm","G","D","A","Bm","Em","G","D","A","Em","G","F#","F#"]
CP_UP=["A","E","B","C#m","A","E","B","C#m","F#m","A","E","B","F#m","A","G#","G#"]
PC["F#m"]=6; QUAL["F#m"]="m"; PC["G#"]=8
PREP=["Em","G","A","F#","Em","G","A","F#"]
BRP=["Em","A","Bm","F#","Em","A","Bm","F#","G","A","Bm","Bm","G","A","F#","F#"]
S=[("intro",VP*2,0),("verse",VP*4,0),("pre",PREP,0),("chorus",CP,0),("inter",VP*2,0),("verse",VP*4,1),("pre",PREP,1),("chorus",CP,1),
   ("solo",VP*4,0),("bridge",BRP,0),("chorus",CP_UP,2),("chorus",CP_UP,3),("outro",["G","D","A","Bm","G","D","Bm","Bm"],0)]
def lead_for(kind,idx):
    """(主旋律, ハモリ, 半音ずらし)"""
    if kind=="intro":
        fl=" ".join(flutter(c,0 if i<2 else 2) for i,c in enumerate(VP))
        return fl+" "+HOOK, None, 0
    if kind=="verse":
        v=[Va,Vb,Va,Vc] if idx==0 else [Vb,Va,Vc,Va]
        return " ".join(v),None,0
    if kind=="pre":
        return " ".join(flutter(c,(0,3)[i//4]) for i,c in enumerate(PREP)),None,0
    if kind=="chorus":
        up=2 if idx>=2 else 0
        return CH,(harm(CH) if idx>=1 else None),up
    if kind=="inter": return "R:32",None,0
    if kind=="solo":
        s=SOLO_A+" "+SOLO_B+" "+SOLO_A+" "+SOLO_B
        return s,harm(s),0
    if kind=="bridge":
        rest=" ".join(flutter(c,(1,2)[i//4%2]) for i,c in enumerate(BRP[8:]))
        return B1+" "+B1.replace("F#5","A5").replace("E5","G5").replace("D5","F#5").replace("C#5","E5")+" "+rest,None,0
    if kind=="outro": return OUTRO,None,0
# ---- ドラム ----
def slots(sym): return " ".join("R:0.25" if c=="." else f"{c}:0.25" for c in sym)
def tomslots(l): return " ".join("R:0.25" if t is None else f"{t}:0.25" for t in l)
VK=["X.......x.x.....","X.....x.x.......","X.......x.....x.","X..x....x.x....."]
CK=["X.x.X.x.X.x...x.","X.x.X.x.X.x.x.x.","X.x.X.x.X.x...x.","X.x.X.x.X.x.x.xx"]
DK=["XxxxXxxxXxxxXxxx","XxxxXxxxXxxxxxXx","X.xxx.xxX.xxx.xx","XxxxXx.xXxxxXxxx"]
FILL=[("X.......X.......","....X...ooxxxXXX",[None]*16),
      ("X.......X.......","....X...........",[None]*8+["C4","C4","A3","A3","G3","G3","E3","E3"]),
      ("X.......X.......","....X...xxXX....",[None]*12+["A3","G3","E3","A2"]),
      ("X.......X...X...","....X.......XXXX",[None]*16)]
fk=[0]
def drum_bar(kind,idx,i,n):
    K="X..............."; Sn="................"; Ht="................"; tom=[None]*16; cr=False; fill=False
    if kind=="intro":
        if i>=4:
            K=VK[i%4]; Sn="....X.......X..."; Ht="x.x.x.x.x.x.x.x."; cr=(i==4)
            if i==7: K="X..............."; Sn="xxxxxxxxxxxxXXXX"; Ht="................"
    elif kind=="verse":
        K=VK[i%4]; Ht="x.x.x.x.x.x.x.x." if idx==0 else "X.x.x.x.X.x.x.x."
        Sn="............x..." if (idx==0 and i<8 and i%2) else ("....o.......x..." if idx==0 and i<8 else "....X..o....X...")
        cr=(i==0 and idx==1)
        fill=(i%8==7 and i!=n-1)
    elif kind=="pre":
        K="X...X...X...X..." if i>=4 else VK[i%4]
        Sn="....x.......x..." if i<4 else ("x...x...x...x..." if i<7 else "xxxxxxxxXXXXXXXX"); Ht="x.x.x.x.x.x.x.x."
        if i==7: K="X.......X.......";
    elif kind=="chorus":
        last=idx>=2
        K=(DK if (last and i>=8) else CK)[i%4]; Sn="....X.......X..."; Ht="X.x.x.x.X.x.x.x." if i%2==0 else "X.x.x.x.X.x.X.x."; cr=(i%2==0)
        fill=(i%8==7 and not(i==n-1))
    elif kind=="inter":
        K="X..............." if i%2==0 else "X.......x......."; Ht="x...x...x...x..."; Sn="............o..." if i%4==3 else "................"
        if i==n-1: Sn="xxxxxxxxXXXXXXXX"; K="X.......X......."
    elif kind=="solo":
        K=VK[i%4] if i<8 else CK[i%4]; Sn="....X.......X..."; Ht="X.x.X.x.X.x.X.x."; cr=(i%4==0)
        fill=(i%8==7 and i!=n-1)
        if i==n-1: Sn="xxxxxxxxxxxxXXXX"; K="X.......X......."
    elif kind=="bridge":
        if i<8: K="X..............." if i%2==0 else "X.......x......."; Ht="o...o...o...o..."; Sn="................"
        elif i<15:
            K="X...X...X...X..."; Sn="....x.......x..." if i<12 else "x.x.x.x.x.x.x.x."; Ht="x.x.x.x.x.x.x.x."
        else: K="X.......X......."; Sn="xxxxxxxxxxxxXXXX"
    elif kind=="outro":
        if i<4: K=CK[i%4]; Sn="....X.......X..."; Ht="X.x.x.x.X.x.x.x."; cr=(i%2==0)
        elif i<7: K="X.......X......."; Sn="........X......."; Ht="x...x...x...x..."; cr=(i==4)
        else: K="X..............."; Sn="X..............."; Ht="X..............."; cr=True
    if fill:
        k,s,t=FILL[fk[0]%4]; fk[0]+=1
        K=K[:8]+k[8:]; Sn=Sn[:8]+s[8:]; Ht=Ht[:8]+"........"; tom=t
    return K,Sn,Ht,tom,cr
# ---- ベース ----
def bass_bar(kind,idx,i,c,n):
    r=root_b(c); t=third(c)
    def seq(l): 
        out=[]
        for d,b in l:
            m=r+d
            while m>50: m-=12
            out.append(f"{nn(m)}:{b}")
        return " ".join(out)
    PUMP=[(0,.5),(0,.5),(12,.5),(0,.5),(0,.5),(0,.5),(12,.5),(7,.5)]
    MEL=[(0,1),(t,.5),(7,.5),(12,1),(7,1)]
    MEL2=[(0,1.5),(7,.5),(12,1),(t+12,1)]
    RUN=[(0,.25),(t,.25),(7,.25),(12,.25),(7,.25),(t,.25),(7,.25),(12,.25),(12,.25),(t+12,.25),(12,.25),(7,.25),(12,.25),(t+12,.25),(19,.25),(t+12,.25)]
    LONG=[(0,2),(7,1),(t,1)]
    UP=[(0,.5),(0,.5),(t,.5),(t,.5),(7,.5),(7,.5),(12,.5),(14,.5)]
    if kind=="intro": return "R:4" if i<4 else seq(MEL if i%2==0 else MEL2)
    if kind=="verse": return seq(RUN if (i==n-1) else [MEL,MEL2,MEL,MEL2][(i+2*idx)%4])
    if kind=="pre": return seq(RUN if i==7 else UP)
    if kind=="chorus": return seq(RUN if (idx>=2 and i%8==7) else (MEL2 if i%4==3 else PUMP))
    if kind=="inter": return seq(LONG) if i%2==0 else seq(MEL2)
    if kind=="solo": return seq(MEL if i%2 else PUMP)
    if kind=="bridge": return seq(LONG) if i<15 else "R:4"
    if kind=="outro": return seq(PUMP) if i<4 else (seq(LONG) if i<7 else f"{nn(r)}:1 R:3")
# ---- ギター ----
def gt(c,kind,idx,i,n):
    r=root_g(c); f=r+7
    def e8(m,short=True): return " ".join(f"{nn(m)}:0.5"+("!" if k in(0,4) else "")+("'" if short else "") for k in range(8))
    def sx(m): return f"{nn(m)}:1 {nn(m)}:0.5 {nn(m)}:0.5 {nn(m)}:1 {nn(m)}:0.5 {nn(m)}:0.5"
    def s16(m): return " ".join(f"{nn(m)}:0.25"+("!" if k%4==0 else "") for k in range(16))
    if kind=="intro": return ("R:4","R:4") if i<4 else (e8(r),e8(f))
    if kind=="verse": return (e8(r),(" ".join(f"R:0.5 {nn(f)}:0.5" for _ in range(4))))
    if kind=="pre": return (e8(r),e8(f)) if i<7 else (s16(r),s16(f))
    if kind=="chorus": return (sx(r),sx(f)) if i%4!=3 else (e8(r,False),e8(f,False))
    if kind=="inter": return ("R:4","R:4")
    if kind=="solo": return (sx(r),sx(f))
    if kind=="bridge":
        if i<8: return ("R:4",f"{nn(f)}:4")
        if i<15: return (f"{nn(r)}:4",f"{nn(f)}:4") if i<12 else (e8(r,False),e8(f,False))
        return ("R:4","R:4")
    if kind=="outro":
        if i<4: return (sx(r),sx(f))
        if i<7: return (f"{nn(r)}:4",f"{nn(f)}:4")
        return (f"{nn(r)}:1 R:3",f"{nn(f)}:1 R:3")
def flut_for(c,kind,idx,i,n):
    if kind in("pre",) : return flutter(c,0)
    if kind=="inter": return flutter(c,(0,2,1,3)[i%4])
    if kind=="chorus": return flutter(c,3) if idx>=1 else "R:4"
    if kind=="bridge": return flutter(c,1) if i>=8 else "R:4"
    if kind=="solo": return "R:4"
    return "R:4"
chords=[];lead=[];lead2=[];fl=[];gl=[];gr=[];bass=[];kick=[];snare=[];hat=[];tomp=[];crashp=[]
for kind,ch,idx in S:
    n=len(ch)
    ld,hm,up=lead_for(kind,idx)
    ld=fold(tr(ld,up) if up else ld)
    assert abs(beats(ld)-4*n)<1e-6,(kind,beats(ld),4*n)
    lead.append(ld)
    if hm: 
        hm=fold(tr(hm,up) if up else hm); lead2.append(hm)
    else: lead2.append(f"R:{4*n}")
    for i,c in enumerate(ch):
        chords.append(c)
        L,R=gt(c,kind,idx,i,n); gl.append(L); gr.append(R)
        fl.append(flut_for(c,kind,idx,i,n))
        bass.append(bass_bar(kind,idx,i,c,n))
        K,Sn,Ht,tom,cr=drum_bar(kind,idx,i,n)
        kick.append(slots(K)); snare.append(slots(Sn)); hat.append(slots(Ht)); tomp.append(tomslots(tom)); crashp.append(slots("X..............." if cr else "................"))
def part(inst,role,notes,vol,pan,patch,amp,extra):
    d={"instrument":inst,"role":role,"volume":vol,"pan":pan,"amp":amp,"notes":" ".join(notes)}
    if patch: d["patch"]=patch
    d.update(extra); return d
G={"noRestrike":True,"chorus":0}
song={"title":"butterfly-2","description":"蝶々をイメージしたメロコアパンク（仮・試作）。羽ばたきの16分アルペジオが芯。Bマイナー、最後の2回のサビは全音上げ。作曲ソフトの中だけで完結。ギターは弦モデル pluck-deepair",
 "bpm":176,"beats":4,"chords":" ".join(chords),"barsPerChord":1,"repeats":1,"feel":"rock","tone":"rock",
 "autoAccompaniment":False,"dynamics":"natural","human":0.25,"fills":False,
 "parts":[
  part("leadGuitar","メロディ／ソロ",lead,0.3,0,"cleanGuitar","clean",{**G,"reverb":0.2}),
  part("leadGuitar","ハモリ（3度上）",lead2,0.2,0.25,"cleanGuitar","clean",{**G,"reverb":0.2}),
  part("leadGuitar","羽ばたき（16分アルペジオ）",fl,0.17,-0.3,"cleanGuitar","clean",{**G,"reverb":0.3,"echo":{"repeats":1,"time":"dotted8","decay":0.3}}),
  part("leadGuitar","リフ（左・ルート）",gl,0.16,-0.6,"cleanGuitar","overdrive",{**G,"reverb":0.08}),
  part("leadGuitar","リフ（右・5度）",gr,0.16,0.6,"cleanGuitar","overdrive",{**G,"reverb":0.08}),
  part("bass","ベース（旋律）",bass,0.6,0,None,"auto",{"bright":0.3}),
  part("kick","キック",kick,0.26,0,None,"auto",{}),part("snare","スネア",snare,0.2,0,None,"auto",{}),part("hihat","ハイハット",hat,0.09,0.3,None,"auto",{}),
  part("tom","タム",tomp,0.2,0,None,"auto",{}),part("crash","クラッシュ",crashp,0.16,0.2,None,"auto",{})]}
print(json.dumps(song,ensure_ascii=False))
