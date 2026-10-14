# 『稲妻ダッシュ』（パンク）v2: ギターはリフ中心。E長調・bpm200。ギター（歪みのリフを左右に重ねる。リードギターの音色は使わない）・メロディベース・ドラムの3人編成。(見本・仮。耳では確かめていない)
# 方針: ドラムは小節ごとに型を変え barGain で強弱の曲線＋間（ストップ）＋ハーフタイム。ギターは `~` なし・短く切らない。
#       タムは低め(E3・C3・A2)の少数・残響0（banned-sounds 12・13）。弦アンサンブルは使わない。
import json,sys,random,re,os
def fmt(x): return ("%.4f"%x).rstrip("0").rstrip(".")
N=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
def nm(m): return f"{N[m%12]}{m//12-1}"
PCN={"C":0,"D":2,"E":4,"F":5,"G":7,"A":9,"B":11}
def pcof(s):
    r=PCN[s[0]]
    if len(s)>1 and s[1]=="#": r+=1
    if len(s)>1 and s[1]=="b": r-=1
    return r%12
def minor(ch): return ch.endswith("m")
VERSE="E B C#m A".split(); PRE="A B A B".split(); CHO="A B E C#m".split(); BRI="C#m A E B".split()
SEC=[("intro",4,VERSE),("dstart",4,VERSE),("verse",8,VERSE),("pre",4,PRE),("chorus",8,CHO),("inter",4,VERSE),("verse",8,VERSE),("pre",4,PRE),("chorus",8,CHO),
     ("bridge",8,BRI),("solo",8,VERSE),("chorus",8,CHO),("chorus",8,CHO),("outro",4,VERSE)]
chords=[]
for _,n,pr in SEC: chords+=[pr[i%4] for i in range(n)]
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
def root_in(ch,lo): r=pcof(ch.split("/")[0]); return lo+((r-lo)%12)
# ---------------- ドラム ----------------
Z="................"
def tomtok(tm):
    pit=["E3","E3","C3","C3","A2","A2"]; hits=[j for j,c in enumerate(tm) if c in "xX"]; toks=[]; kk=0
    for j,c in enumerate(tm):
        if c in "xX": toks.append(pit[min(5,kk*6//len(hits))]+":0.25"+("!" if c=="X" else "")); kk+=1
        else: toks.append("R:0.25")
    return toks
def drum(sec,k,n,rnd,si):
    cr="R:4"; tm=None; ride=None; ph=k%4; last=(k==n-1)
    two_k="X...X...X...X..."; two_s="..x...x...x...x."
    if sec=="intro": kk=Z; sn=Z; hh=Z   # ギターだけで4小節
    elif sec=="dstart":
        # ドラムの始まり: フロアタムとスネアを同時に「だっだっだっだ」と、だんだん強く（1小節目は4分、2小節目は8分）。そのあと2ビート→フィルでAメロへ（ブラストビートは使わない）
        if k==0: kk=Z; sn="x...x...x...X..."; hh=Z
        elif k==1: kk=Z; sn="x.x.x.x.x.x.x.X."; hh=Z
        elif k==2: kk="X...X...X...X..."; sn="..x...x...x...x."; hh="x.x.x.x.x.x.x.x."; cr="g:X..............."   # 2ビートで走り出す
        else: kk="X...X...X.x.X.x."; sn="....X...x.x.xXXX"; hh="x.x.x.x.x.x.x.x."; tm="............xxXX"
    elif sec=="verse":
        kk=rnd.choice(["X..xX..xX..xX..x","X.x.X..xX.x.X..x","X.......X.x.X..."]); sn="....X.......X..."
        hh=rnd.choice(["x.x.x.x.x.x.x.x.","X.x.x.x.X.x.x.x."])
        if si>=5 and k>=4: kk=two_k; sn=two_s   # 2回目のAメロは後半から2ビートに
        if k==0: cr="g:X..............."
        if k==3: sn="....X.o.....X.xX"
        if last: sn="....X.o.o.x.xxXX"; tm="..............XX"; kk="X.......X.x.X..."
    elif sec=="pre":
        kk=["X.......X.......","X.x.....X.x.....","X.x.X.x.X.x.X.x.","X.X.X.X.X......."][ph]
        sn=["....X.......X...","....X.......X.x.","....X.x.X.x.X.x.","xxxxxxxxXXx....."][ph]
        hh=["x.x.x.x.x.x.x.x.","x.x.x.x.x.x.x.x.","xxxxxxxxxxxxxxxx","x.x.x.x.x......."][ph]
        if ph==3: tm=None
    elif sec=="chorus":
        kk=two_k if ph!=3 else "X...X...X..xX.xX"; sn=two_s; hh="O.x.O.x.O.x.O.x." if si<10 else "x.x.x.x.x.x.x.x."
        if k%2==0: cr="g:X..............."
        if si>=10: ride="D2" if ph in(1,2) else None
        if last: sn="..x...x.xxxxXXXX" if si<11 else "xxxxxxxxxxxxXXXX"; tm="........xxXXxxXX" if si>=10 else "............xxXX"; kk="X...X...X.x.X.x."; cr="R:4" if si!=11 else "R:4"
        if si==11 and last: kk=sn=hh=Z
    elif sec=="inter":
        if k==0: kk="X..............."; sn=Z; hh=Z; cr="g:X..............."   # ストップ（間）
        elif k==1: kk=Z; sn=Z; hh=Z
        elif k==2: kk="X...X...X...X..."; sn="....X.......X..."; hh="x.x.x.x.x.x.x.x."
        else: kk="X...X...X.x.X.x."; sn="....X...xxxxXXXX"; hh="x.x.x.x.x.x.x.x."; tm="............xxXX"
    elif sec=="bridge":   # ハーフタイム。スネアは3拍目だけ
        kk=["X...............","................","X.......X.......","X.......X.x....."][ph]; sn="........X......." if k>=2 else Z; hh=Z
        ride="F2" if k<6 else None
        if last: sn="....X.o.o.x.xXXX"; tm="........xxxxXXXX"; kk="X...X...X...X..."
    elif sec=="solo":
        kk=rnd.choice(["X.x.X.x.X.x.X.x.",two_k,"X..xX..xX..xX..x"]); sn=two_s if ph!=1 else "....X.......X..."; hh="x.x.x.x.x.x.x.x."
        if k==0: cr="g:X..............."
        if ph==3: sn="....X..oX.x.XxXX"; tm="..........xxXXXX"
        if last: sn="xxxxxxxxxxxxXXXX"; tm=None
    else: # outro
        kk=two_k; sn=two_s; hh="O.x.O.x.O.x.O.x."
        if k==0: cr="g:X..............."
        if k==2: kk="X.......X.......";sn="....X.......X...";hh="x.x.x.x.x.x.x.x."
        if last: kk=sn="X..............."; hh=Z; cr="g:X..............."
    return "g:"+kk,"g:"+sn,"g:"+hh,cr,tm,ride
def arc(sec,si,k,n):
    f=k/max(1,n-1)
    return {"intro":0.95,"dstart":[0.55,0.82,1.0,1.0][min(k,3)],"verse":0.8+0.1*f,"pre":0.88+0.14*f,"chorus":1.05-(0.05 if k%4==3 else 0),"inter":0.85,"solo":0.97,"bridge":0.55+0.3*f,"outro":1.0-0.15*f}[sec]
kick=[];snare=[];hat=[];crash=[];tom=[];rideL=[];ARC=[]
for si,(sec,n,pr) in enumerate(SEC):
    rnd=random.Random(900+si*13); ks=[];ss=[];hs=[];cs=[];ts=[];rs=[]
    for k in range(n):
        a,b,c,d,e,r=drum(sec,k,n,rnd,si); ks.append(a);ss.append(b);hs.append(c);cs.append(d)
        if sec=="dstart" and k==0: ts+=["A2:1","A2:1","A2:1","A2:1!"]
        elif sec=="dstart" and k==1: ts+=["A2:0.5"]*7+["A2:0.5!"]
        else: ts+= tomtok(e) if e else ["R:4"]
        if sec=="bridge": rs+= (["F2:4"] if r else ["R:4"])
        elif sec=="chorus" and r: rs+=["D2:0.5"]*8
        elif sec=="solo" and k%4 in(1,2): rs+=["D2:0.5"]*8
        else: rs+=["R:4"]
        ARC.append(arc(sec,si,k,n))
    kick.append(ks);snare.append(ss);hat.append(hs);crash.append(cs);tom.append(ts);rideL.append(rs)
# ---------------- ベース（メロディベース）----------------
BPAT=[
 lambda t3:[(0,.5),(0,.5),(7,.5),(0,.5),(12,.5),(0,.5),(7,.5),(t3,.5)],
 lambda t3:[(0,1),(7,.5),(12,.5),(10,.5),(7,.5),(5,.5),(7,.5)],
 lambda t3:[(0,.5),(0,.5),(12,.5),(0,.5),(7,1),(5,.5),(7,.5)],
 lambda t3:[(0,1.5),(7,.5),(12,1),(7,.5),(5,.5)],
 lambda t3:[(12,.5),(7,.5),(0,.5),(7,.5),(t3,.5),(7,.5),(12,1)],
]
def bass_bar(ch,nch,k,sec,idx,stop=False):
    r=root_in(ch,29); nr=root_in(nch,29); t3=3 if minor(ch) else 4
    pat=BPAT[idx%len(BPAT)](t3); toks=[]; t=0
    if k%4==3 or stop:
        lim=3.0
        for iv,d in pat:
            if t+d>lim+1e-9: break
            toks.append((r+iv,d)); t+=d
        if t<lim: toks.append((toks[-1][0],lim-t)); t=lim
        if stop: toks.append(None)       # 最後の1拍は休み（間）
        else: toks+=[(nr-2,.5),(nr-1,.5)]  # 半音で次の根音へ
    else: toks=[(r+iv,d) for iv,d in pat]
    return [("R:1" if x is None else f"{nm(x[0])}:{fmt(x[1])}") for x in toks]
def f_bass(si,sec,n,pr):
    out=[]; rnd=random.Random(70+si)
    for k in range(n):
        ch=pr[k%4]; nch=pr[(k+1)%4]
        if sec=="bridge":
            BR=["C#3:1.5 E3:0.5 G#2:1 B2:1","A2:1.5 C#3:0.5 E3:1 C#3:1","E3:1.5 G#2:0.5 B2:1 E3:1","B2:1 D#3:1 F#3:1 D#3:1"]
            BR2=["C#3:1 E3:1 G#2:1 C#3:1","A2:1 C#3:1 E3:1 A2:1","E3:1 B2:1 G#2:1.5 B2:0.5","B2:1.5 F#3:0.5 B2:2"]
            out+=(BR if k<4 else BR2)[k%4].split(); continue
        if sec=="intro":
            out+=R(4); continue
        if sec=="dstart":
            out+= bass_bar(ch,nch,k,sec,k); continue
        if sec=="inter" and k<2: out+=[f"{nm(root_in(ch,29))}:4"]; continue
        if sec=="outro" and k==n-1: out+=[f"{nm(root_in(ch,29))}:4"]; continue
        stop=(sec=="pre" and k==n-1)
        out+=bass_bar(ch,nch,k,sec,rnd.randrange(5) if sec!="chorus" else (k+si)%5,stop)
    return out
# ---------------- リードギター ----------------
def rootg(ch): return root_in(ch,52)
RIFF=[[0,0,12,0,0,12,7,12],[0,12,0,12,7,12,0,7],[0,0,7,7,12,12,7,0]]
def riff_bar(ch,var,fill=False):
    r=rootg(ch)+12; t3=3 if minor(ch) else 4
    iv=[0,12,7,12,12+t3,19,12+t3,12] if fill else RIFF[var%3]
    return [f"{nm(r+x-12 if x>=12 and not fill else r+x)}:0.5"+("!" if i==0 else "") for i,x in enumerate(iv)]
CHO1="C#5:1 E5:1 A5:1 G#5:0.5 F#5:0.5|F#5:1 B5:1 A5:1 G#5:1|G#5:1.5 B5:0.5 G#5:1 E5:1|E5:1 G#5:1 C#6:2^"
CHO2="A5:1 G#5:0.5 F#5:0.5 E5:1 C#5:1|D#5:1 F#5:1 B5:2^|E5:1 G#5:1 B5:1 E6:1|C#6:1.5 B5:0.5 G#5:1 E5:1"
CHOH="E6:1 C#6:0.5 E6:0.5 A5:1 C#6:1|D#6:1 B5:1 F#5:1 B5:1|G#5:1 B5:1 E6:2^|C#6:1 B5:1 G#5:1 E5:1"
PRE="A5:1 C#6:1 B5:1 A5:1|B5:2 F#5:1 D#5:1|A5:1 C#6:1 E6:1 C#6:1|B5:1 F#5:1 D#5:1 R:1"
def lst(s): return s.replace("|"," ").split()
SCALE=[m for m in range(55,89) if m%12 in (4,6,8,9,11,1,3)]
def solo_bar(k,var):
    i0=min(range(len(SCALE)),key=lambda i:abs(SCALE[i]-(64+(k%4)*3))); seqs=[[0,1,2,0],[0,2,1,3],[2,1,0,1],[0,1,3,2]]; toks=[]
    for g in range(4):
        b=i0+(g if var%2==0 else -g)
        for s in seqs[(var+g//2)%4]: toks.append(f"{nm(SCALE[max(0,min(len(SCALE)-1,b+s))])}:0.25")
    return toks
def toks_from(r,ch,pat,accent=True):
    t3=3 if minor(ch) else 4
    out=[]
    for i,(iv,d) in enumerate(pat(t3)):
        out.append(f"{nm(r+iv)}:{fmt(d)}"+("!" if (i==0 and accent) else ""))
    return out
CHR=[lambda t3:[(0,.5),(12,.5),(0,.5),(12,.5),(12+t3,1),(19,.5),(12+t3,.5)],
     lambda t3:[(0,1),(12,.5),(12,.5),(19,1),(12+t3,.5),(12,.5)]]
PRER=lambda t3:[(0,.5),(0,.5),(7,.5),(7,.5),(12,.5),(12,.5),(19,.5),(19,.5)]
BRR=[lambda t3:[(12,1.5),(7,.5),(0,2)], lambda t3:[(0,2),(7,1),(12,1)]]
S16=lambda t3:[(x,.25) for x in (0,7,12,7,0,7,12,12+t3,12,7,12,12+t3,19,12+t3,12,7)]
def cut3(toks_pat,t3):
    out=[];t=0
    for iv,d in toks_pat(t3):
        if t+d>3+1e-9: break
        out.append((iv,d)); t+=d
    if t<3: out[-1]=(out[-1][0],out[-1][1]+3-t)
    return out
def f_lead(si,sec,n,pr):
    out=[]
    for k in range(n):
        ch=pr[k%4]; fill=(k%4==3); r=rootg(ch)
        if sec=="intro": out+= riff_bar(ch,k,fill=(k==3))
        elif sec=="dstart": out+= riff_bar(ch,k+1,fill=(k==3))
        elif sec=="verse": out+= riff_bar(ch,(k//2+si),fill=fill)
        elif sec=="pre":
            if k==n-1:
                pat=cut3(PRER,3 if minor(ch) else 4); out+=[f"{nm(r+iv)}:{fmt(d)}"+("!" if i==0 else "") for i,(iv,d) in enumerate(pat)]+["R:1"]
            else: out+=toks_from(r,ch,PRER)
        elif sec=="chorus":
            if k==n-1 and si==11: out+=[f"{nm(r+12)}:2!",f"{nm(r+19)}:2^"]
            elif k==3 and si>=10: out+=toks_from(r,ch,CHR[0])
            else: out+=toks_from(r,ch,CHR[(k+si)%2])
        elif sec=="inter": out+= (R(4) if k<2 else riff_bar(ch,k,fill=(k==3)))
        elif sec=="bridge": out+=toks_from(r,ch,BRR[(k//2)%2])
        elif sec=="solo":
            if k==n-1: out+=[f"{nm(r+12)}:4!"]
            else: out+=toks_from(r,ch,S16,accent=False)
        elif sec=="outro": out+= [f"{nm(r+12)}:4"] if k==n-1 else riff_bar(ch,k+1)
    return out
PARTS=[]
def add(inst,role,vol,pan,secs,**kw):
    d={"instrument":inst,"role":role,"volume":vol,"pan":pan,"notes":cat(secs,role)}; d.update(kw); PARTS.append(d)
ARCL=[round(x,3) for x in ARC]
add("kick","キック",0.17,0,kick,barGain=ARCL); add("snare","スネア",0.15,0,snare,barGain=ARCL,push=0.02); add("hihat","ハイハット",0.05,0,hat,barGain=ARCL,push=-0.008)
add("crash","クラッシュ",0.06,0,crash,barGain=ARCL); add("crash","ライド",0.05,0.15,rideL,barGain=ARCL); add("tom","タム",0.09,0,tom,barGain=ARCL,reverb=0)
add("bass","メロディベース",0.38,0,per(f_bass),barGain=ARCL)
GI=os.environ.get('PUNK_INST','crunch'); GA=os.environ.get('PUNK_AMP','hardrock'); GD=float(os.environ.get('PUNK_DRIVE','1.2')); CLAMP_HI=76 if GI=='guitar' else 64
def gclamp(secs):
    # ディストーションギター（刻み）の音域は E2〜E4。高い音は1オクターブ下げ、低い音は上げる
    def fix(t):
        m=re.match(r"^([A-G]#?)(-?\d)(:.*)$",t)
        if not m: return t
        v=PCN[m.group(1)[0]]+(1 if m.group(1).endswith("#") else 0)+(int(m.group(2))+1)*12
        while v>CLAMP_HI: v-=12
        while v<40: v+=12
        return nm(v)+m.group(3)
    return [[fix(t) for t in (sec.split() if isinstance(sec,str) else sec)] for sec in secs]
GT=gclamp(per(f_lead))
def octdown(secs):
    out=[]
    for sec in secs:
        r=[]
        for t in sec:
            m=re.match(r"^([A-G]#?)(-?\d)(:.*)$",t)
            if not m: r.append(t); continue
            v=PCN[m.group(1)[0]]+(1 if m.group(1).endswith("#") else 0)+(int(m.group(2))+1)*12-12
            while v<40: v+=12
            r.append(nm(v)+m.group(3))
        out.append(r)
    return out
GT2=octdown(GT)
# 重く・歪みを少し足す: ampDrive 1.4。右のギターは1オクターブ下げて低域の厚みを足す
add(GI,"リフギター（左）",0.2 if GI=="guitar" else 0.12,-0.7,GT,amp=GA,ampDrive=GD,humanPitch=0,chorus=0,reverb=0.16,barGain=ARCL)
add(GI,"リフギター（右・1オクターブ下）",0.2 if GI=="guitar" else 0.12,0.7,GT2,amp=GA,ampDrive=GD,humanPitch=0,chorus=0,reverb=0.16,push=0.006,barGain=ARCL)
add(GI,"リフギター（中央・厚み用）",0.07,0.0,GT2,amp=GA,ampDrive=GD*0.9,humanPitch=0,chorus=0,reverb=0.22,push=0.012,barGain=ARCL)
song={"title":"稲妻ダッシュ（パンク）","description":"（見本・仮）bpm200・E長調・約1分40秒の疾走パンク。ギター（歪みのリフを左右に重ねる。リードギターの音色は使わない）・メロディベース・ドラムの3人編成。Aメロはオクターブのリフ、サビは厚いオクターブのリフ、間奏のストップ（間）、ハーフタイムのブリッジ（ベースが旋律）、リフで押すソロ。ギターはずっとリフ中心。ドラムは小節ごとに型を変えて強弱をつけた。ギターにビブラートなし。","bpm":200,"beats":4,"chords":" ".join(chords),"barsPerChord":1,"repeats":1,"tone":"rock","feel":"rock","human":0.3,"autoScoop":False,"instrumentCheck":False,"dynamics":"natural","drumMix":{"kick":{"level":1.05,"tune":-2},"snare":{"level":1.05,"tune":-2,"reverb":0.15},"tom":{"reverb":0.0,"spread":0.5,"level":1.05,"tune":-4}},"parts":PARTS}
json.dump(song,open(sys.argv[1],"w"),ensure_ascii=False,indent=1)
print("ok",len(PARTS),len(chords),"bars")
