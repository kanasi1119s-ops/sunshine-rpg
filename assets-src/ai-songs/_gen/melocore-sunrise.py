# 夜明けのスプリント（メロコア）。D長調・bpm176。(見本・仮。耳では確かめていない)
# 方針: 8分のパワーコードを伸ばして鳴らす(短く切らない)、ドラムは小節ごとに変える+barGain、ビブラート・しゃくり・コーラスなし、メロはトランペット、ソロはピアノ
import json,sys,random
def fmt(x): return ("%.4f"%x).rstrip("0").rstrip(".")
N=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
def nm(m): return f"{N[m%12]}{m//12-1}"
PCN={"C":0,"D":2,"E":4,"F":5,"G":7,"A":9,"B":11}
def pcof(s):
    r=PCN[s[0]]
    if len(s)>1 and s[1]=="#": r+=1
    if len(s)>1 and s[1]=="b": r-=1
    return r%12
VERSE="D A C G".split(); PRE="Bm G D A".split(); CHO="G A F#m Bm".split(); BRI="D A/C# Bm G".split()
SEC=[("intro",4,CHO),("verse",8,VERSE),("pre",4,PRE),("chorus",8,CHO),("inter",4,CHO),("verse",8,VERSE),("pre",4,PRE),("chorus",8,CHO),("bridge",8,BRI),("solo",8,VERSE),("chorus",8,CHO),("chorus",8,CHO),("outro",4,CHO)]
chords=[]
for _,n,pr in SEC: chords+= [pr[i%4] for i in range(n)]
def root(ch,low=38):
    r=pcof(ch.split("/")[0]); return low+((r-low)%12)
def rootb(ch):
    r=pcof(ch.split("/")[0]); return 28+((r-28)%12)
def barsum(toks):
    t=0
    for x in toks:
        if x.startswith("g:"): assert len(x)==18,x; t+=4; continue
        d=x.split(":")[1]; d="".join(c for c in d if c.isdigit() or c=="."); t+=float(d)
    return t
def cat(secs,name):
    out=[]
    for (s,n,_),toks in zip(SEC,secs):
        if isinstance(toks,str): toks=toks.split()
        assert abs(barsum(toks)-4*n)<1e-6,(name,s,barsum(toks),4*n)
        out+=toks
    return " ".join(out)
def R(b): return [f"R:{fmt(b)}"]
def per(fn): return [fn(si,s,n,pr) for si,(s,n,pr) in enumerate(SEC)]
# ドラム
def drum(sec,k,n,rnd,si):
    z="................"; cr="R:4"; tm=None; ride=None
    ph=k%4; last=(k==n-1)
    if sec=="intro":
        kk=z if k<2 else "X.......X......."; sn=z if k<2 else "....X.......X..."; hh="x.x.x.x.x.x.x.x."
        if last: sn="....X...x.x.xXXX"; tm="............xxXX"; kk="X.......X.x....."
    elif sec in("verse",):
        kk=rnd.choice(["X..xX..xX..xX..x","X.x.X..xX.x.X..x","X..xX.x.X..xX.xx"]); sn="....X.......X..." if k<4 or si<5 else rnd.choice(["....X..o....X...","....X.......X..o"])
        hh=rnd.choice(["x.x.x.x.x.x.x.x.","X.x.x.x.X.x.x.x.","x.x.x.xox.x.x.xo"])
        if k==0: cr="g:X..............."
        if last: sn="....X.o.o.x.xxXX"; tm="..............XX"
    elif sec=="pre":
        kk=["X.......X.......","X.x.....X.x.....","X.x.X.x.X.x.X.x.","XxxxXxxxXxxxXxxx"][ph]; sn=["....X.......X...","....X.......X.x.","....X.x.X.x.X.x.","xxxxxxxxxxxxXXXX"][ph]; hh="x.x.x.x.x.x.x.x." if ph<3 else "xxxxxxxxxxxxxxxx"
        if ph==3: tm="............xxXX"; kk="X...X...X..xX.xX"
    elif sec in("chorus",):
        kk=rnd.choice(["X..xX..xX..xX..x","X.x.X.x.X.x.X.x.","X..xX.x.X..xX.x."]); sn="....X.......X..."; hh=rnd.choice(["O.x.O.x.O.x.O.x.","X.O.x.O.X.O.x.O."])
        if k%2==0: cr="g:X..............."
        if last or (n>=8 and k==3): sn=rnd.choice(["....X...x.x.xXXX","....X..oX.x.xxXX"]); tm=rnd.choice(["............xxXX","........xxXXxxXX"]); kk="X.......X.x....."; cr="R:4"
    elif sec=="inter":
        kk="X.......X..x...."; sn="....X.......X..."; hh="x.x.x.x.x.x.x.x."
        if last: sn="....X...xxxxXXXX"; tm="............xxXX"
    elif sec=="solo":
        kk=rnd.choice(["X.x.X.x.X.x.X.x.","X..xX..xX..xX..x"]); sn="....X.......X..."; hh="x.x.x.x.x.x.x.x."
        if k==0: cr="g:X..............."
        if ph==3: sn="....X..oX.x.XxXX"; tm="..........xxXXXX"
    elif sec=="bridge":
        kk=["X...............","................","X.......X.......","X.......X.x....."][ph]; sn="........X......." if k>=2 else z; hh=z
        ride="F2" if k<6 else None
        if last: sn="....X.o.o.x.xXXX"; tm="........xxxxXXXX"; kk="X...X...X...X..."
    else:
        kk=rnd.choice(["X..xX..xX..xX..x","X.x.X.x.X.x.X.x."]); sn="....X.......X..."; hh="O.x.O.x.O.x.O.x."
        if k==0: cr="g:X..............."
        if last: kk=sn="X..............."; hh=z; cr="g:X..............."
    return "g:"+kk,"g:"+sn,"g:"+hh,cr,tm,ride
def tomtok(tm):
    # 高いタムの「ポンポン」を避け、低めの2〜3本だけ使う
    pit=["E3","E3","C3","C3","A2","A2"]; hits=[j for j,c in enumerate(tm) if c in "xX"]; toks=[]; kk=0
    for j,c in enumerate(tm):
        if c in "xX": toks.append(pit[min(5,kk*6//len(hits))]+":0.25"+("!" if c=="X" else "")); kk+=1
        else: toks.append("R:0.25")
    return toks
kick=[];snare=[];hat=[];crash=[];tom=[];rideL=[];ARC=[]
def arc(sec,si,k,n):
    f=k/max(1,n-1)
    return {"intro":0.65+0.2*f,"verse":0.78+0.1*f,"pre":0.88+0.14*f,"chorus":1.05-(0.06 if k%4==3 else 0),"inter":0.8,"solo":0.95,"bridge":0.55+0.3*f,"outro":1.0-0.2*f}[sec]
for si,(sec,n,pr) in enumerate(SEC):
    rnd=random.Random(500+si*17); ks=[];ss=[];hs=[];cs=[];ts=[];rs=[]
    for k in range(n):
        a,b,c,d,e,r=drum(sec,k,n,rnd,si); ks.append(a);ss.append(b);hs.append(c);cs.append(d)
        ts+= tomtok(e) if e else ["R:4"]
        if sec=="bridge": rs+= ["F2:2","R:2"] if r else ["R:4"] if False else (["F2:4"] if r else ["R:4"])
        elif sec=="chorus" and si>=7 and k%4>=2 and not (k==n-1): rs+=["D2:0.5"]*8
        elif sec=="solo": rs+=["D2:1"]*4
        else: rs+=["R:4"]
        ARC.append(arc(sec,si,k,n))
    kick.append(ks);snare.append(ss);hat.append(hs);crash.append(cs);tom.append(ts);rideL.append(rs)
# ベース: 8分。ルートを伸ばす(次の音まで鳴る)
def f_bass(si,sec,n,pr):
    if sec in("intro",): return [t for k in range(n) for t in ([f"{nm(rootb(pr[k%4]))}:4"] if k<2 else [f"{nm(rootb(pr[k%4]))}:0.5"]*8)]
    if sec=="bridge": return [f"{nm(rootb(pr[k%4]))}:4" for k in range(n)] if False else [t for k in range(n) for t in (f"{nm(rootb(pr[k%4]))}:2",f"{nm(rootb(pr[k%4]))}:1",f"{nm(rootb(pr[k%4])+7)}:1")]
    toks=[]
    for k in range(n):
        r=rootb(pr[k%4]); last=(k==n-1)
        toks+= [f"{nm(r)}:0.5"]*6+[f"{nm(r)}:0.5",f"{nm(r+7 if k%2 else r)}:0.5"] if not last else [f"{nm(r)}:0.5"]*4+[f"{nm(r+7)}:0.5",f"{nm(r+7)}:0.5",f"{nm(r+12)}:1"]
    return toks
# ギター: 8分のパワーコード(伸ばす)
def f_gtr(si,sec,n,pr,side):
    toks=[]
    for k in range(n):
        r=root(pr[k%4])
        if sec=="intro": toks+=R(4); continue
        if sec=="bridge": toks+=[f"{nm(r)}:2",f"{nm(r)}:2"]; continue
        if sec=="outro" and k==n-1: toks+=[f"{nm(r)}:4"]; continue
        if k==n-1 and sec in("pre",): toks+=[f"{nm(r)}:0.5"]*4+[f"{nm(r)}:1",f"{nm(r+0)}:1"]; continue
        toks+= [f"{nm(r)}:0.5!"]+[f"{nm(r)}:0.5"]*7 if (k%4!=3 or side) else [f"{nm(r)}:0.5!"]+[f"{nm(r)}:0.5"]*5+[f"{nm(r)}:1"]
    return toks
# クリーンのアルペジオ(イントロ・ブリッジ・間奏)
def f_arp(si,sec,n,pr):
    if sec in("intro","inter","bridge"):
        toks=[]
        for k in range(n):
            ch=pr[k%4]; r=pcof(ch.split("/")[0]); b=57+((r-57)%12); minor="m" in ch
            t3=3 if minor else 4
            toks+=[f"{nm(m)}:0.5" for m in (b,b+7,b+12,b+12+t3,b+19,b+12+t3,b+12,b+7)]
        return toks
    return R(4*n)
MEL={}
MEL["verse1"]="F#5:1 A5:1 F#5:0.5 E5:0.5 D5:1|E5:1 A5:1 G5:0.5 F#5:0.5 E5:1|G5:1 E5:1 C5:1 E5:1|B4:1 D5:1 G5:1 F#5:0.5 E5:0.5"
MEL["verse2"]="A5:1 F#5:1 D5:1 F#5:1|E5:1.5 A5:0.5 C#6:1 A5:1|G5:1 C6:1 G5:1 E5:1|D5:1 B5:1 A5:1 G5:1"
MEL["pre"]="B4:1 D5:1 F#5:1 B5:1|D5:1 G5:1 B5:1 A5:1|A5:2 F#5:1 D5:1|E5:1 A5:1 C#6:2"
MEL["cho1"]="B4:1 D5:1 B4:1 G4:1|C#5:1 E5:1 C#5:1 A4:1|A4:1 C#5:1 F#5:1 E5:1|D5:2 B4:1 F#4:1"
MEL["cho2"]="B4:0.5 D5:0.5 G5:1 F#5:1 D5:1|E5:1 C#5:1 A4:1 E5:1|F#5:1.5 E5:0.5 C#5:1 A4:1|D5:1 B4:1 F#4:1 D5:1"
def lst(s): return s.replace("|"," ").split()
def f_lead(si,sec,n,pr):
    if sec=="verse": return lst(MEL["verse1"]+"|"+MEL["verse2"]) if si<4 else lst(MEL["verse2"]+"|"+MEL["verse1"])
    if sec=="pre": return lst(MEL["pre"])
    if sec=="chorus": return lst(MEL["cho1"]+"|"+MEL["cho2"])
    if sec=="outro": return R(12)+["D5:4"]
    if sec=="bridge": return lst("F#5:4|E5:2 C#5:2|D5:4|B4:2 D5:2|F#5:4|G5:2 A5:2|A5:4|F#5:2 D5:2")
    return R(4*n)
def f_lead_hi(si,sec,n,pr):   # 最後のサビの二重(オクターブ上)
    if sec=="chorus" and si==11: return [t if t.startswith("R") else nm(__import__("re") and (0))+"" for t in []] or [x for x in lst(MEL["cho1"]+"|"+MEL["cho2"])]
    return R(4*n)
# ソロ(ピアノ): D長調の音階の16分
def smid():
    return [m for m in range(55,96) if m%12 in (2,4,6,7,9,11,1)]
SC=smid()
def solo_bar(k,var):
    i0=min(range(len(SC)),key=lambda i:abs(SC[i]-(66+(k%4)*2)))
    seqs=[[0,1,2,0],[0,2,1,3],[2,1,0,1],[0,1,3,2]]; toks=[]
    for g in range(4):
        b=i0+(g if var%2==0 else -g)
        for s in seqs[(var+g//2)%4]: toks.append(f"{nm(SC[max(0,min(len(SC)-1,b+s))])}:0.25")
    return toks
def f_solo(si,sec,n,pr):
    if sec=="solo":
        toks=[]
        for k in range(n):
            if k in(0,4): toks+=["A5:1.5","D6:0.5","C#6:1","A5:1"] if k==0 else ["B5:1","A5:0.5","F#5:0.5","A5:2"]
            else: toks+=solo_bar(k,k)
        return toks
    return R(4*n)
def f_str(si,sec,n,pr):
    if sec in("verse","bridge","outro","intro","inter"): return [f"{nm(root(pr[k%4])+12)}:4" for k in range(n)] if sec!="intro" else R(4*n)
    return R(4*n)
PARTS=[]
def add(inst,role,vol,pan,secs,**kw):
    d={"instrument":inst,"role":role,"volume":vol,"pan":pan,"notes":cat(secs,role)}; d.update(kw)
    if inst=="brass":
        # トランペットが1音ずつ切れて「ポンポン」と聞こえたので、休みに挟まれていない音はつなげる（レガート）
        tk=d["notes"].split(); d["notes"]=" ".join(t+"_" if (not t.startswith("R:") and i+1<len(tk) and not tk[i+1].startswith("R:") and not t.endswith("_")) else t for i,t in enumerate(tk))
    PARTS.append(d)
ARCL=[round(x,3) for x in ARC]
add("kick","キック",0.2,0,kick,barGain=ARCL); add("snare","スネア",0.17,0,snare,barGain=ARCL,push=0.02); add("hihat","ハイハット",0.07,0,hat,barGain=ARCL,push=-0.008)
add("crash","クラッシュ",0.09,0,crash,barGain=ARCL); add("crash","ライド",0.08,0.15,rideL,barGain=ARCL); add("tom","タム",0.14,0,tom,barGain=ARCL,reverb=0)
add("bass","ベース（8分）",0.2,0,per(f_bass),barGain=ARCL)
add("distGuitar","リズムギター（左）",0.11,-0.8,per(lambda a,b,c,d:f_gtr(a,b,c,d,0)),amp="loudrock",humanPitch=0,chorus=0,reverb=0.1,barGain=ARCL)
add("distGuitar","リズムギター（右）",0.11,0.8,per(lambda a,b,c,d:f_gtr(a,b,c,d,1)),amp="loudrock",humanPitch=0,chorus=0,reverb=0.1,push=0.006,barGain=ARCL)
add("guitar","クリーンのアルペジオ",0.2,-0.3,per(f_arp),amp="crystal",humanPitch=0,chorus=0,reverb=0.3)
add("strings","弦",0.08,0,per(f_str),reverb=0.3,sustain=1.5,patch="cello")  # 弦アンサンブル(48)は出だしで音程が落ちる「ぽーん」があるので使わない
add("brass","メロディ（トランペット）",0.22,0.05,per(f_lead),patch="trumpet",breath=True,reverb=0.25,fx=[{"type":"delay","beats":0.75,"mix":0.1,"feedback":0.2}])
add("piano","ソロ（ピアノ）",0.2,0.1,per(f_solo),reverb=0.25)
song={"title":"夜明けのスプリント（メロコア）","description":"（見本・仮）メロディックハードコア。D長調・bpm176・約2分。8分のパワーコードを伸ばして鳴らし、ドラムは小節ごとに変えて緩急をつけた。メロディはトランペット、ソロはピアノ。歌なし。ギターにビブラート・しゃくり・コーラスなし。","bpm":176,"beats":4,"chords":" ".join(chords),"barsPerChord":1,"repeats":1,"tone":"rock","feel":"rock","human":0.25,"autoScoop":False,"instrumentCheck":False,"dynamics":"natural","drumMix":{"tom":{"reverb":0.0,"spread":0.5}},"parts":PARTS}
json.dump(song,open(sys.argv[1],"w"),ensure_ascii=False,indent=1)
print("ok",len(PARTS),len(chords),"bars")
