# 回廊の螺旋（プログレッシブメタル）。5つのコード進行（chord-patterns-100 から）を場面ごとに組み合わせる。
# 技: 4/4に重ねた7/8の周期(クロスリズム)・ユニゾンの走句・スウィープ・タッピング・三度のハモり・ダブルバス・タムの5拍フィル・キーボードソロ
# （見本・仮。耳では確かめていない）
import json,sys,random
def fmt(x):
    s=("%.4f"%x).rstrip("0").rstrip("."); return s
N=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
def nm(m): return f"{N[m%12]}{m//12-1}"
PCN={"C":0,"D":2,"E":4,"F":5,"G":7,"A":9,"B":11}
def pcof(s):
    r=PCN[s[0]]
    if len(s)>1 and s[1]=="#": r+=1
    if len(s)>1 and s[1]=="b": r-=1
    return r%12
# ── 5つの進行 ──
P1="Em7 Em7/D C C/B".split()   # 短調の下降7th（静）
P2="Em D C B".split()          # アンダルシア（重いリフ）
P3="Em C G D".split()          # 短調の王道（サビ）
P4="Em Am B C".split()         # ハーモニックマイナー（キーボード）
P5="Em F G F".split()          # フリジアン（ギターソロ）
SEC=[("intro",8,P1),("riff",16,P2),("verse",16,P1),("chorus",16,P3),("inter",12,P2),("kbsolo",8,P4),("gsolo",16,P5),("bridge",8,P1),("final",16,P3),("outro",8,P2)]
chords=[]
for _,n,pr in SEC:
    for i in range(n): chords.append(pr[i%4])
TOTAL=len(chords)
TRI={"":[0,4,7],"m":[0,3,7],"m7":[0,3,7,10]}
def tones(ch):
    base=ch.split("/")[0]; r=pcof(base); q=base[1:] if len(base)>1 and base[1] not in "#b" else base[2:]
    q={"":"","m":"m","m7":"m7"}.get(q,"")
    return r,[(r+i)%12 for i in TRI[q]]
def scale_pcs(ch):
    base=ch.split("/")[0]; r=pcof(base)
    if base=="B": return [4,6,7,9,11,0,3]      # ハーモニックマイナー
    if base=="F": return [4,5,7,9,11,0,2]      # フリジアン
    return [4,6,7,9,11,0,2]                    # ナチュラルマイナー
def smidis(pcs): return [m for m in range(28,100) if m%12 in pcs]
def nearest(ms,m): return min(range(len(ms)),key=lambda i:abs(ms[i]-m))
def rootmidi(ch,low=40):   # E2(40)〜D#3 の範囲に収めたルート
    r=tones(ch)[0]; m=low+((r-low)%12); return m
def rootbass(ch):
    r=tones(ch)[0]; return 28+((r-28)%12)   # E1(28)〜D#2
def barsum(toks):
    t=0
    for x in toks:
        if x.startswith("g:"):
            assert len(x)==18,x
            t+=4; continue
        d=x.split(":")[1]; d="".join(c for c in d if c.isdigit() or c==".")
        t+=float(d)
    return t
def cat(secs,name):   # 場面ごとの文字列を結合し、拍の合計を確かめる
    out=[];
    for (s,n,_),toks in zip(SEC,secs):
        if isinstance(toks,str): toks=toks.split()
        tot=barsum(toks)
        assert abs(tot-4*n)<1e-6,(name,s,tot,4*n)
        out+=toks
    return " ".join(out)
def R(b): return [f"R:{fmt(b)}"]
def silent(n): return R(4*n)
# ── リフ(7/8の周期を4/4に重ねる)。4小節=16拍=3.5拍×4+2拍 ──
CELL=[1.0,1.0,1.5]  # 2+2+3 (8分)
def riff_events(prog_bars,sec_bars):
    """各4小節のかたまりについて (開始拍,長さ,音型番号,セル番号) を返す。"""
    ev=[]
    for ph in range(sec_bars//4):
        b0=ph*16; t=b0
        for c in range(4):
            for g,L in enumerate(CELL):
                ev.append((t,L,g,c,ph)); t+=L
        ev.append((t,2.0,9,0,ph))   # 最後の2拍はユニゾン走句
    return ev
OFF={0:[0,0,1],1:[0,0,7],2:[0,3,1],3:[0,0,6]}
def riff_gtr(sec_bars,prog,octave=0,bass=False):
    toks=[]
    for (t,L,g,c,ph) in riff_events(prog,sec_bars):
        bar=int(t//4); ch=prog[bar%4]
        if g==9:
            toks+=unison_run(ch,2.0,bass=bass,octave=octave); continue
        r=(rootbass(ch) if bass else rootmidi(ch))+12*octave
        off=OFF[(c+ph)%4][g]
        if g==2:   # 長い群は2分割して動かす
            toks+=[f"{nm(r)}:0.5",f"{nm(r+off)}:0.5",f"{nm(r)}:0.5"]
        elif g==0:
            toks+=[f"{nm(r)}:0.5",f"{nm(r)}:0.5"]
        else:
            toks+=[f"{nm(r+off)}:1.0"] if off else [f"{nm(r)}:0.5",f"{nm(r+(1 if c%2 else 0))}:0.5"]
    return toks
def unison_run(ch,beats,bass=False,octave=0,start=None):
    ms=smidis(scale_pcs(ch)); base=(rootbass(ch)+12 if bass else rootmidi(ch)+12*octave+12)
    i0=nearest(ms,base); toks=[]; n=int(beats/0.25)
    for k in range(n):
        g,j=divmod(k,4); b=i0+g
        seq=[0,1,2,0][j]; toks.append(f"{nm(ms[b+seq])}:0.25")
    return toks
def shred_bar(ch,base,var,dir_=1,step=0.25):
    ms=smidis(scale_pcs(ch)); i0=nearest(ms,base); toks=[]
    seqs=[[0,1,2,0],[0,2,1,3],[2,1,0,1],[0,1,3,2]]
    for g in range(int(4/step/4)):
        b=i0+dir_*g
        for s in seqs[(var+g//2)%4]: toks.append(f"{nm(ms[b+s])}:{fmt(step)}")
    return toks
def sweep_bar(ch,lowroot=52):
    r,tn=tones(ch)
    ms=sorted(m for m in range(40,100) if m%12 in tn)
    i0=min((i for i,m in enumerate(ms) if m>=lowroot and m%12==r),default=0)
    seq=[]
    for j in (0,1):
        up=ms[i0+j:i0+j+8]; seq+=up+list(reversed(up))
    return [f"{nm(m)}:0.125"+("_" if (i%16)!=15 else "") for i,m in enumerate(seq)]
def tap_bar(ch,top0,var=0):
    ms=smidis(scale_pcs(ch)); r,tn=tones(ch)
    lowt=sorted(m for m in range(52,70) if m%12 in tn)[:3]
    it=nearest(ms,top0); toks=[]
    for k in range(10):
        top=ms[it+(k%5)*(1 if var==0 else -1)+ (2 if k>=5 else 0)]
        toks+= [f"{nm(top)}:0.125_",f"{nm(lowt[k%3])}:0.125_",f"{nm(lowt[(k+1)%3])}:0.125" + ("_" if k<9 else "")]
    toks+=[f"{nm(ms[it+4])}:0.125_",f"{nm(lowt[0])}:0.125"]
    return toks
# ── ドラム ──
def grid(p): return "g:"+p
def drum_bar(sec,k,n,ch,rnd):
    z="................"
    cr="R:4"; tm=None
    if sec=="intro":
        kk=z;sn=z;hh="................"
        if k>=6: kk="X..x..X.x.X.....";sn="....X.......XXXX" if k==7 else "....X..........."; hh="x.x.x.x.x.x.x.x."
        if k==7: tm="............xxXX"
    elif sec in("riff","outro","inter"):
        base=["X.xxX..xX.xX..x.","X..xX.x.X..xXx..","X.x.X.xxX...X.xx","X.xxX.xxX.xxX.xx"]
        kk=base[(k+rnd.randint(0,1))%4]
        sn=rnd.choice(["....X.......X...","....X..o....X..o","....X.o.....X.o."])
        hh=rnd.choice(["X.x.O.x.X.x.O.x.","x.x.x.x.x.x.x.x.","X.xoX.x.X.xoX.x."])
        if k%4==0: cr="g:X..............."
        if k%4==3: 
            sn=rnd.choice(["....X...x.x.xXXX","....X..oX.x.XxXX"]); tm=rnd.choice(["............xxXX","........xxXXxxXX"])
        if sec=="outro" and k==n-1: kk=sn="X..............."; hh=z; tm=None; cr="g:X..............."
    elif sec=="verse":
        kk=rnd.choice(["X.......X..o....","X.....o.X.......","X.......X.....o."]); sn="........X......." if k<8 else rnd.choice(["....X.......X...","....o...X.....o."])
        hh=rnd.choice(["x...x...x...x...","x.o.x.o.x.o.x.o."]); 
        if k%4==0: cr="g:X..............." if k==0 else "R:4"
        if k%4==3: sn="....X.o.o.x.xxXX" if k%8==7 else sn; tm="..............XX" if k%8==7 else None
    elif sec in("chorus","final"):
        base=["X.xxX.xxX.xxX.xx","X.x.X.x.X.xxX.x.","XxxxXxxxXxxxXxxx","X.xxX.x.X.xxXxxx"]
        kk=base[(k+(2 if sec=="final" else 0))%4]; sn="....X.......X..." 
        hh="X.O.x.O.X.x.O.x." if sec=="chorus" else "O.x.O.x.O.x.O.x."
        if k%2==0: cr="g:X..............." 
        if k%8==7: sn="....X...x.xoxXXX"; tm="........xxXXxxXX"; kk="X.......X.x....."; cr="R:4"
        if sec=="final" and k==n-1: sn="x.x.x.x.xxxxXXXX"; tm="........xxxxXXXX"
    elif sec=="kbsolo":
        kk=rnd.choice(["X..x..X.x...X...","X.......X.x.X.x."]); sn="....X.......X..."; hh="x.x.x.x.x.x.x.x."
        if k%4==3: kk="X...X...X..xX.xX"; sn="o.o.x.x.xxxxXXXX"; tm="..........xxXXXX"
        if k==0: cr="g:X..............."
    elif sec=="gsolo":
        kk=["X.xxX.xxX.xxX.xx","XxxxXxxxXxxxXxxx"][(k//2)%2]; sn="....X.......X..."; hh="X.x.x.x.X.x.x.x."
        if k%4==0: cr="g:X..............."
        if k%4==3: sn="....X..oX.x.XxXX"; tm="..........xxXXXX"
    else: # bridge
        kk=["X...............","................","X.......X.......","........X.x....."][k%4]; sn=z if k<4 else "........X......."; hh=z
        tm=None
    return "g:"+kk,"g:"+sn,"g:"+hh,cr,tm
def tomtok(tm,pit):
    hits=[j for j,c in enumerate(tm) if c in "xX"]; toks=[]; kk=0
    for j,c in enumerate(tm):
        if c in "xX": toks.append(pit[min(len(pit)-1,kk*len(pit)//len(hits))]+":0.25"+("!" if c=="X" else "")); kk+=1
        else: toks.append("R:0.25")
    return toks
# ── 組み立て ──
kick=[];snare=[];hat=[];crash=[];tom=[];ride=[]
for si,(sec,n,pr) in enumerate(SEC):
    rnd=random.Random(77+si*13)
    ks=[];ss=[];hs=[];cs=[];ts=[]
    for k in range(n):
        a,b,c,d,e=drum_bar(sec,k,n,pr[k%4],rnd)
        ks.append(a);ss.append(b);hs.append(c);cs.append(d);ts+=tomtok(e,["C4","A3","G3","E3","C3","A2"]) if e else ["R:4"]
    kick.append(ks);snare.append(ss);hat.append(hs);crash.append(cs);tom.append(ts)
    # ライド: リフ/間奏は7/8の周期(3.5拍)にライドのベル、ソロとサビはライド、ブリッジ/イントロはベルをゆっくり
    if sec in("riff","inter","outro"):
        rt=[]
        for ph in range(n//4): rt+=["F2:3.5"]*4+["R:2"]
    elif sec in("chorus","final"):
        rt=[]
        for k in range(n):
            rt+= ["D2:0.5"]*8 if k%4 in(1,2) else R(4)
    elif sec=="gsolo": rt=["D2:0.5"]*(8*n)
    elif sec in("intro","bridge"): rt=["F2:4"]*(n)
    elif sec=="kbsolo": rt=["D2:1"]*(4*n)
    else: rt=R(4*n)
    ride.append(rt)
def flat(L): return [t for x in L for t in x]
# 場面ごとのパートを作る
def per_sec(fn): return [fn(si,sec,n,pr) for si,(sec,n,pr) in enumerate(SEC)]
def chordroots(pr,n,bass=False,oct_=0,dur=4): return [f"{nm((rootbass if bass else rootmidi)(pr[k%4])+12*oct_)}:{dur}" for k in range(n)]
# ベース
def f_bass(si,sec,n,pr):
    if sec in("riff","inter","outro"): return riff_gtr(n,pr,bass=True)
    if sec=="intro":
        r6=nm(rootbass(pr[2])); r7=nm(rootbass(pr[3]))
        return R(16)+[f"{nm(rootbass(pr[0]))}:4",f"{nm(rootbass(pr[1]))}:4",f"{r6}:1.5",f"{r6}:0.5",f"{r6}:1","R:1",f"{r7}:1.5",f"{r7}:0.5",f"{r7}:2"]
    if sec in("chorus","final","gsolo"): return [t for k in range(n) for t in (f"{nm(rootbass(pr[k%4]))}:0.5",f"{nm(rootbass(pr[k%4]))}:0.5",f"{nm(rootbass(pr[k%4])+(7 if k%2 else 0))}:1",f"{nm(rootbass(pr[k%4]))}:0.5",f"{nm(rootbass(pr[k%4]))}:0.5",f"{nm(rootbass(pr[k%4]))}:1")]
    if sec=="kbsolo": return [t for k in range(n) for t in (f"{nm(rootbass(pr[k%4]))}:1.5",f"{nm(rootbass(pr[k%4]))}:0.5",f"{nm(rootbass(pr[k%4]))}:2")]
    if sec=="verse": return [t for k in range(n) for t in ([f"{nm(rootbass(pr[k%4]))}:4"] if k<4 else [f"{nm(rootbass(pr[k%4]))}:2",f"{nm(rootbass(pr[k%4])+7)}:1",f"{nm(rootbass(pr[k%4])+10 if k%4<2 else rootbass(pr[k%4])+12)}:1"])]
    return [f"{nm(rootbass(pr[k%4]))}:4" for k in range(n)]
# リズムギター(L/R): リフ=7/8周期。サビ=パワーコード長音。ほかは休みか長音
def f_gtr(si,sec,n,pr,side):
    if sec in("riff","inter","outro"): return riff_gtr(n,pr,octave=0)
    if sec=="intro": return R(24)+[f"{nm(rootmidi(pr[2]))}:1.5",f"{nm(rootmidi(pr[2]))}:0.5",f"{nm(rootmidi(pr[2]))}:1",f"R:1",f"{nm(rootmidi(pr[3]))}:1.5",f"{nm(rootmidi(pr[3]))}:0.5",f"{nm(rootmidi(pr[3]))}:2"]
    if sec in("chorus","final"): return [t for k in range(n) for t in (f"{nm(rootmidi(pr[k%4]))}:1.5",f"{nm(rootmidi(pr[k%4]))}:0.5",f"{nm(rootmidi(pr[k%4]))}:2")]
    if sec in("kbsolo","gsolo"): return [t for k in range(n) for t in (f"{nm(rootmidi(pr[k%4]))}:3",f"{nm(rootmidi(pr[k%4])+(7 if side else 0))}:1")]
    return silent(n)
# クリーン アルペジオ
def f_arp(si,sec,n,pr):
    if sec in("intro","verse","bridge"):
        toks=[]
        for k in range(n):
            if sec=="intro" and k>=6: toks+=R(4); continue
            r,tn=tones(pr[k%4]); b=48+((r-48)%12)
            ch=[b,b+7,b+12,b+16 if (r in(0,)) else b+15,b+12,b+7,b+(4 if r==0 else 3),b+7]
            toks+= [f"{nm(m)}:0.5" for m in ch]
        return toks
    return silent(n)
def f_piano(si,sec,n,pr):
    if sec in("verse","bridge") :
        toks=[]
        for k in range(n):
            if sec=="verse" and k<4: toks+=R(4); continue
            r,tn=tones(pr[k%4]); b=60+((r-60)%12)
            toks+=[f"{nm(b)}:0.5",f"{nm(b+7)}:0.5",f"{nm(b+12)}:0.5",f"{nm(b+(4 if r==0 else 3)+12)}:0.5",f"{nm(b+7+12)}:1",f"{nm(b+12)}:0.5",f"{nm(b+7)}:0.5"]
        return toks
    return silent(n)
def f_strings(si,sec,n,pr):
    if sec in("intro","verse","chorus","final","bridge","kbsolo"):
        return [f"{nm(rootmidi(pr[k%4])+12)}:4" if not (sec=="intro" and k>=6) else "R:4" for k in range(n)]
    return silent(n)
# キーボードのリード(シンセ): 旋律・ユニゾン走句・ソロ
VERSE_MEL=[ "R:1 B4:1 D5:1 E5:1","F#5:1.5 E5:0.5 D5:2","E5:1 G5:1 E5:1 C5:1","B4:3 R:1" ]
VERSE_MEL2=[ "B4:1 D5:1 E5:1 G5:1","F#5:1 A5:1 F#5:1 D5:1","G5:1.5 E5:0.5 C5:2","D5:2 B4:1 R:1" ]
CH_A=[ "B4:1 G4:0.5 E5:1.5 D5:1","E5:1 C5:0.5 G4:0.5 E5:2","D5:1 B4:0.5 G4:0.5 D5:1.5 B4:0.5","A4:1 F#4:0.5 A4:0.5 D5:2" ]
CH_B=[ "B4:1 E5:1 G5:1 F#5:1","E5:1.5 G5:0.5 E5:1 C5:1","D5:1 G5:1 B5:1.5 A5:0.5","F#5:2 A5:1 F#5:1" ]
BR_MEL=[ "E5:4","D5:2 B4:2","C5:4","B4:4" ]
def lst(s): return s.split()
def f_key(si,sec,n,pr):
    if sec=="intro": return R(16)+lst(" ".join(VERSE_MEL))
    if sec=="verse": return lst(" ".join(VERSE_MEL))+lst(" ".join(VERSE_MEL2))+lst(" ".join(VERSE_MEL))+lst(" ".join(VERSE_MEL2))
    if sec=="chorus" or sec=="final":
        return lst(" ".join(CH_A))+lst(" ".join(CH_B))+lst(" ".join(CH_A))+lst(" ".join(CH_B if sec=="chorus" else CH_B))
    if sec=="bridge": return lst(" ".join(BR_MEL))+lst(" ".join(BR_MEL))
    if sec in("riff","inter","outro"):
        toks=[]
        for ph in range(n//4):
            toks+=R(14)
            ch=pr[3]; toks+=unison_run(ch,2.0,octave=1)
        return toks
    if sec=="kbsolo":
        toks=[]
        for k in range(n):
            ch=pr[k%4]
            if k%4==3 and k>=4: toks+=sweep_bar(ch,lowroot=60); continue
            toks+=shred_bar(ch,64+ (k%4)*2,k,1 if k%2==0 else -1)
        return toks
    if sec=="gsolo":
        return [t for k in range(n) for t in (R(4) if k<8 else (unison_run(pr[k%4],2.0,octave=1)+unison_run(pr[k%4],2.0,octave=2) if k<15 else shred_bar(pr[k%4],72,k)))]
    return silent(n)
# ハモり(三度上)
def third_above(tok_list,ch_for_bar):
    ms=smidis([4,6,7,9,11,0,2]); out=[]
    for t in tok_list:
        n,d=t.split(":")
        if n=="R": out.append(t); continue
        base=n; midi=None
        # 音名→MIDI
        import re
        m=re.match(r"([A-G])(#?)(-?\d)(.*)$",n); 
        pc=PCN[m.group(1)]+(1 if m.group(2) else 0); midi=(int(m.group(3))+1)*12+pc
        i=nearest(ms,midi)
        if ms[i]!=midi: out.append(t); continue
        out.append(f"{nm(ms[i+2])}:{d}")
    return out
def f_harm(si,sec,n,pr):
    if sec in("chorus","final"):
        k=f_key(si,sec,n,pr)
        half=len(lst(" ".join(CH_A+CH_B)))
        if sec=="chorus": return R(32)+third_above(k[half:],None)
        return third_above(k,None)
    return silent(n)
# ギターリード(録音ギター+lead): ソロ
def f_lead(si,sec,n,pr):
    if sec=="gsolo":
        toks=[]
        for k in range(n):
            ch=pr[k%4]
            if k<4:
                phr=[["B4:1.5!^^~","E5:0.5","G5:1","F#5:1~~"],["C5:1!","E5:1","G5:1.5^~","F5:0.5"],["D5:1.5!^~","B4:0.5","G5:2~~"],["A4:1!","C5:1","E5:2~~"]][k%4]; toks+=phr
            elif k<8: toks+=sweep_bar(ch)
            elif k<12: toks+=tap_bar(ch,76,k%2)
            elif k<15: toks+=shred_bar(ch,69+k,k,1 if k%2==0 else -1,step=0.125) if False else shred_bar(ch,69+(k-12)*2,k,1)
            else: toks+=["E5:0.5","B5:0.5","E6:1~~","E5:2~~"] if False else ["E6:3!^^~~","R:1"]
        return toks
    if sec=="bridge": return lst("E5:3!~ D5:1 C5:4~ B4:3~ G4:1 E4:4~~ G4:3~ A4:1 B4:4~ D5:2~ E5:2~~ E5:4~~")
    if sec=="outro": return R(28)+["E5:4!^~~"]
    return silent(n)
PARTS=[]
def add(inst,role,vol,pan,secs,**kw):
    d={"instrument":inst,"role":role,"volume":vol,"pan":pan,"notes":cat(secs,role)}; d.update(kw); PARTS.append(d)
add("kick","キック",0.18,0,kick); add("snare","スネア",0.16,0,snare); add("hihat","ハイハット",0.07,0,hat)
add("crash","クラッシュ",0.09,0,crash); add("crash","ライド・ベル",0.07,0.15,ride); add("tom","タム",0.2,0,tom)
add("bass","ベース",0.2,0,per_sec(f_bass))
add("distGuitar","リフ（左）",0.12,-0.75,per_sec(lambda s,sec,n,pr:f_gtr(s,sec,n,pr,0)),amp="loudmetal",humanPitch=0,chorus=0,reverb=0.1)
add("distGuitar","リフ（右）",0.12,0.75,per_sec(lambda s,sec,n,pr:f_gtr(s,sec,n,pr,1)),amp="loudmetal",humanPitch=0,chorus=0,reverb=0.1,push=0.006)
add("guitar","クリーンのアルペジオ",0.2,-0.3,per_sec(f_arp),amp="crystal",humanPitch=0,chorus=0,reverb=0.3)
add("piano","ピアノのアルペジオ",0.12,0.25,per_sec(f_piano),reverb=0.3)
add("strings","弦のパッド",0.1,0,per_sec(f_strings),reverb=0.3,sustain=1.5)
add("lead","キーボード・リード",0.14,0.1,per_sec(f_key),patch="sawLead",reverb=0.25,fx=[{"type":"delay","beats":0.75,"mix":0.12,"feedback":0.25}])
add("lead","キーボード・三度上のハモり",0.1,-0.1,per_sec(f_harm),patch="sawLead",reverb=0.25)
add("guitar","リードギター（ソロ・ブリッジ）",0.35,0.05,per_sec(f_lead),amp="lead",humanPitch=0,chorus=0,reverb=0.25,fx=[{"type":"delay","beats":0.75,"mix":0.18,"feedback":0.3}])
song={"title":"回廊の螺旋（プログレッシブメタル）","description":"（見本・仮）プログレッシブメタル。コード進行5つ（下降7th・アンダルシア・短調の王道・ハーモニックマイナー・フリジアン）を場面ごとに組み合わせた。4/4に7/8の周期を重ねたリフ、ユニゾンの走句、キーボードソロ、スウィープ・タッピング・速弾きのギターソロ、三度のハモり、ダブルバス。歌なし。Eマイナー・bpm140・約3分半。","bpm":140,"beats":4,"chords":" ".join(chords),"barsPerChord":1,"repeats":1,"tone":"metal","feel":"rock","human":0.12,"autoScoop":False,"instrumentCheck":False,"dynamics":"natural","parts":PARTS}
json.dump(song,open(sys.argv[1],"w"),ensure_ascii=False,indent=1)
print("ok",len(PARTS),"parts",TOTAL,"bars")
