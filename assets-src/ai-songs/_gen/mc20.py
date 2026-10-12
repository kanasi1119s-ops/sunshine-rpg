# メロコアパンク20曲の生成器。曲ごとに 調・長短・構成・テンポ・コード進行・転調の型・イントロ・ドラムのノリ・ギターの弾き方 を変える。
# 旋律は「動機（リズム＋音の動き）」を作って、問い→答え→くり返し（変化つき）→終止、の形で歌わせる。
# 使い方: python3 mc20.py <番号0〜19|all> [出力フォルダ]
import json,re,random,sys,os
NAMES=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
def nn(m): return f"{NAMES[m%12]}{m//12-1}"
MAJ=[0,2,4,5,7,9,11]; MIN=[0,2,3,5,7,8,10]
def cname(c): return NAMES[c[0]%12]+("m" if c[1]=="m" else "")
def cpcs(c): return [c[0]%12,(c[0]+(3 if c[1]=="m" else 4))%12,(c[0]+7)%12]
def root_g(c):
    m=36+c[0]%12
    while m<40: m+=12
    return m
def root_b(c):
    m=24+c[0]%12
    while m<28: m+=12
    return m
def third(c): return 3 if c[1]=="m" else 4
M,m_="M","m"
# ---- コード進行の型（主音からの半音数, 長短）----
MAJP={"I-V-vi-IV":[(0,M),(7,M),(9,m_),(5,M)],"vi-IV-I-V":[(9,m_),(5,M),(0,M),(7,M)],"I-vi-IV-V":[(0,M),(9,m_),(5,M),(7,M)],"IV-V-iii-vi":[(5,M),(7,M),(4,m_),(9,m_)],
 "I-IV-V-IV":[(0,M),(5,M),(7,M),(5,M)],"vi-V-IV-V":[(9,m_),(7,M),(5,M),(7,M)],"I-bVII-IV-I":[(0,M),(10,M),(5,M),(0,M)],"I-iii-IV-V":[(0,M),(4,m_),(5,M),(7,M)],
 "IV-I-V-vi":[(5,M),(0,M),(7,M),(9,m_)],"vi-IV-V-I":[(9,m_),(5,M),(7,M),(0,M)],"I-iv-I-V":[(0,M),(5,m_),(0,M),(7,M)],"I-V-IV-V":[(0,M),(7,M),(5,M),(7,M)]}
MINP={"i-VI-III-VII":[(0,m_),(8,M),(3,M),(10,M)],"i-VII-VI-VII":[(0,m_),(10,M),(8,M),(10,M)],"i-iv-VII-III":[(0,m_),(5,m_),(10,M),(3,M)],"i-VI-iv-V":[(0,m_),(8,M),(5,m_),(7,M)],
 "VI-VII-i-i":[(8,M),(10,M),(0,m_),(0,m_)],"i-III-VII-VI":[(0,m_),(3,M),(10,M),(8,M)],"i-iv-VI-V":[(0,m_),(5,m_),(8,M),(7,M)],"i-VII-VI-V":[(0,m_),(10,M),(8,M),(7,M)],"III-VII-i-VI":[(3,M),(10,M),(0,m_),(8,M)]}
PREM=[[(9,m_),(5,M),(7,M),(7,M)],[(5,M),(5,M),(7,M),(7,M)],[(2,m_),(7,M),(2,m_),(7,M)],[(4,m_),(9,m_),(5,M),(7,M)]]
PREN=[[(5,m_),(8,M),(10,M),(7,M)],[(8,M),(5,m_),(7,M),(7,M)],[(5,m_),(5,m_),(7,M),(7,M)]]
# ---- リズムの型（負＝休み）----
VR=[[-1,.5,.5,1.5,.5],[.5,.5,1,1,1],[1,.5,.5,2],[1.5,.5,1,1],[-.5,.5,.5,.5,1,1],[.5,.5,.5,.5,2],[2,1,.5,.5],[1,1,1,1],[-1,1,.5,.5,1]]
CR=[[1,1,2],[1.5,.5,2],[.5,.5,1,2],[1,.5,.5,1,1],[2,1,1],[.5,.5,.5,.5,1,1],[1,1,.5,.5,1],[.5,.5,1,.5,.5,1],[1,.5,.5,2],[3,1]]
PR=[[1,1,1,1],[.5,.5,.5,.5,1,1],[1,1,.5,.5,1],[.5,.5,1,.5,.5,1],[.5]*8]
SR=[[.25]*8+[1,1],[.5,.5]+[.25]*4+[1,1],[.25]*4+[.5,.5,1,1],[.25]*16,[.5]*4+[.25]*4+[1],[1]+[.25]*4+[1,1]]
CAD=[[2,1,-1],[1,1,2],[1.5,.5,2],[3,-1],[2,2],[1,.5,.5,2]]
STEPS={"verse":[-2,-1,-1,0,1,1,2],"chorus":[-2,-1,0,1,1,2,3,-3],"pre":[1,1,1,2,0,-1,3],"solo":[1,1,1,-1,-1,2,-2],"inter":[-1,-1,0,1,1],"bridge":[-1,0,1],"intro":[-1,1,1,2,-2],"outro":[-1,-1,0,1,2]}
HEIGHT={"verse":[.2,.35,.3,.4],"chorus":[.6,.8,.7,.5],"pre":[.4,.55,.7,.85],"solo":[.4,.7,.6,.5],"inter":[.3,.3,.35,.25],"bridge":[.35,.4,.3,.25],"intro":[.5,.6,.55,.5],"outro":[.6,.7,.5,.3]}
RHY={"verse":VR,"chorus":CR,"pre":PR,"solo":SR,"inter":VR,"bridge":VR,"intro":PR,"outro":CR}
class Song:
    def __init__(s,i):
        s.i=i; s.rng=random.Random(7000+i*31)
def step(p,n,sc,lo,hi):
    # sc: 音階の音（昇順）。p に近い音から n 音ぶん動く
    k=min(range(len(sc)),key=lambda j:abs(sc[j]-p))
    k=max(0,min(len(sc)-1,k+n)); return sc[k]
def scale_list(tonic,mode,lo,hi):
    S=MAJ if mode=="maj" else MIN
    return [m for m in range(lo,hi+1) if (m-tonic)%12 in S]
def chord_list(c,lo,hi): return [m for m in range(lo,hi+1) if m%12 in cpcs(c)]
def new_bar(rng,kind,cad):
    rh=list(rng.choice(CAD if cad else RHY[kind]))
    notes=[d for d in rh if d>0]
    st=[rng.choice(STEPS[kind]) for _ in range(max(0,len(notes)-1))]
    return {"rh":rh,"st":st,"cad":cad}
def new_phrase(rng,kind,copy_of=None):
    if copy_of and rng.random()<0.6:
        ph=[dict(b) for b in copy_of]
        j=rng.randrange(3); ph[j]=new_bar(rng,kind,False)  # 一部だけ変える
        ph[3]=new_bar(rng,kind,True); return ph
    ph=[new_bar(rng,kind,False),new_bar(rng,kind,False),None,new_bar(rng,kind,True)]
    ph[2]=dict(ph[0]) if rng.random()<0.6 else new_bar(rng,kind,False)
    return ph
def realize(b,chord,nextc,target,sc,lo,hi,rng,tag):
    ch=chord_list(chord,lo,hi)
    p=min(ch,key=lambda m:abs(m-target))
    out=[];first=True;si=0;pitches=[];toks=[]
    tpos=0.0
    for d in b["rh"]:
        if d<0: toks.append(("R",-d)); tpos+=-d; continue
        if first: first=False
        else:
            q=step(p,b["st"][si],sc,lo,hi); si+=1
            if q==p and rng.random()<0.75: q=step(p,rng.choice([-1,1]),sc,lo,hi)
            p=q
            # 拍の頭で1拍以上の長い音は、和音の音に寄せる（和音とぶつけない）
            if abs(tpos-round(tpos))<1e-9 and d>=1:
                cand=[m for m in chord_list(chord,lo,hi) if abs(m-p)<=2]
                if cand: p=min(cand,key=lambda m:abs(m-p))
        toks.append((p,d)); tpos+=d
    # 最後の音を和音の音へ寄せる
    idx=[i for i,t in enumerate(toks) if t[0]!="R"]
    if idx:
        li=idx[-1]; p=toks[li][0]
        if b["cad"] or True:
            tgt=chord if b["cad"] else (nextc or chord)
            cand=[m for m in chord_list(tgt,lo,hi) if abs(m-p)<=(5 if b["cad"] else 3)]
            if cand: toks[li]=(min(cand,key=lambda m:abs(m-p)),toks[li][1])
    res=[]
    for p,d in toks:
        if p=="R": res.append(f"R:{d:g}")
        else: res.append(f"{nn(p)}:{d:g}"+("~" if (tag=="chorus" and d>=2 and rng.random()<0.5) else ""))
    return " ".join(res)
def beats(s): return sum(float(x.split(":")[1].rstrip("~^_!'")) for x in s.split())
# ================= 曲の設計 =================
SONGS=[ # (slug, 日本語の題, 主音, 長短, 構成, 転調, イントロ, ドラム(Aメロ,サビ), ギター型, 進行ID(verse,chorus), 進行ID(bridge)) 
 ("dawn-rail","夜明けの線路",4,"maj","A","up2",0,("rock8","skate"),0,(0,3),5),
 ("bike-hill","坂道の自転車",9,"maj","C","none",1,("skate","skate"),1,(1,4),7),
 ("rain-after","雨あがりの交差点",11,"min","B","par",3,("rock8","rock8"),2,(0,2),3),
 ("last-summer","夏の終わりの海",2,"maj","E","ladder",4,("dbeat","skate"),3,(2,0),6),
 ("night-bus","終バスの窓",7,"min","D","up3",2,("rock8","dbeat"),0,(1,3),1),
 ("paper-plane","紙ひこうき",6,"maj","B","rel",0,("rock8","skate"),1,(3,5),8),
 ("blue-room","青い部屋",0,"maj","A","midup",1,("skate","rock8"),2,(4,2),9),
 ("ash-city","灰色の街",9,"min","C","up5",3,("dbeat","skate"),3,(2,4),0),
 ("stray-star","はぐれ星",4,"min","D","down2",4,("rock8","skate"),0,(0,5),3),
 ("noon-bell","正午のチャイム",5,"maj","E","up1",2,("skate","skate"),1,(6,8),2),
 ("cold-coffee","冷めたコーヒー",10,"maj","A","par",0,("rock8","rock8"),2,(7,9),4),
 ("rooftop","屋上の風",1,"min","B","rel",1,("rock8","dbeat"),3,(1,6),7),
 ("run-away","走り出す朝",7,"maj","D","ladder",3,("skate","skate"),0,(3,10),5),
 ("hollow-moon","からっぽの月",2,"min","C","none",4,("dbeat","rock8"),1,(5,2),0),
 ("kite-day","凧の日",8,"maj","E","up3",2,("rock8","skate"),2,(8,11),6),
 ("ferry-lights","フェリーの灯",11,"min","A","midup",0,("skate","dbeat"),3,(6,4),8),
 ("spring-gate","春の改札",0,"maj","B","par",1,("rock8","skate"),0,(2,0),1),
 ("whisper-wire","ささやく電線",6,"min","C","down2",3,("dbeat","skate"),1,(7,1),9),
 ("tailwind","追い風",3,"maj","D","up5",4,("rock8","rock8"),2,(4,6),2),
 ("long-way-home","遠回りの帰り道",5,"min","E","up1",2,("skate","skate"),3,(0,8),4)]
TEMPL={"A":[("intro",8),("verse",16),("pre",8),("chorus",16),("inter",8),("verse",16),("pre",8),("chorus",16),("solo",16),("bridge",16),("chorus",16),("chorus",16),("outro",8)],
 "B":[("intro",8),("verse",16),("pre",8),("chorus",16),("verse",16),("pre",8),("chorus",16),("solo",8),("bridge",16),("chorus",16),("chorus",16),("outro",8)],
 "C":[("intro",4),("chorus",8),("verse",16),("pre",8),("chorus",16),("inter",8),("verse",16),("pre",8),("chorus",16),("bridge",16),("solo",16),("chorus",16),("outro",8)],
 "D":[("intro",8),("verse",8),("pre",8),("chorus",16),("verse",8),("pre",8),("chorus",16),("solo",16),("inter",8),("bridge",8),("chorus",16),("chorus",16),("outro",8)],
 "E":[("intro",8),("verse",16),("chorus",16),("verse",16),("pre",8),("chorus",16),("bridge",16),("solo",16),("chorus",16),("chorus",8),("outro",8)]}
def plan_offsets(plan,secs,T,mode):
    # 各区間の (半音のずれ, 長短)。最後のサビ（とそのあと）に転調を当てる
    n=len(secs); offs=[(0,mode)]*n
    ch=[i for i,s in enumerate(secs) if s["kind"]=="chorus"]
    last=ch[-1]; last2=ch[-2] if len(ch)>1 else ch[-1]
    flip="min" if mode=="maj" else "maj"
    rel=(9,"min") if mode=="maj" else (3,"maj")
    def setr(a,b,v):
        for i in range(a,b): offs[i]=v
    if plan=="up1": setr(last2 if secs[last2]["bars"]>=16 and last2>last-3 else last,n,(1,mode))
    elif plan=="up2": setr(last2 if last2>last-3 else last,n,(2,mode))
    elif plan=="up3": setr(last,n,(3,mode))
    elif plan=="up5": setr(last,n,(5,mode))
    elif plan=="par": setr(last,n,(0,flip))
    elif plan=="rel":
        b=[i for i,s in enumerate(secs) if s["kind"]=="bridge"][0]; setr(b,last,rel)
    elif plan=="midup":
        b=[i for i,s in enumerate(secs) if s["kind"] in("solo","bridge")][0]; setr(b,n,(2,mode))
    elif plan=="down2":
        b=[i for i,s in enumerate(secs) if s["kind"] in("bridge",)][0]; setr(b,last,(-2,mode)); setr(last,n,(2,mode))
    elif plan=="ladder": setr(last,n,(2,mode))  # 最後のサビを半分に割って +2、+4（下で処理）
    return offs
BPMS=[196,178,162,176,168,186,204,172,164,190,182,166,200,170,188,176,198,184,194,168]
def build(i):
    slug,jp,T,mode,tpl,plan,intro_kind,(fv,fc),gprof,(pv,pc_),pb=SONGS[i]
    rng=random.Random(9100+i*17)
    secs=[{"kind":k,"bars":b,"ph0":0} for k,b in TEMPL[tpl]]
    if plan=="ladder":  # 最後のサビを 8+8 に割る
        li=max(j for j,s in enumerate(secs) if s["kind"]=="chorus")
        a=dict(secs[li]); a["bars"]=8; a["ph0"]=0; b=dict(secs[li]); b["bars"]=8; b["ph0"]=2; b["hi"]=True
        secs[li:li+1]=[a,b]
    offs=plan_offsets(plan,secs,T,mode)
    if plan=="ladder":
        li=max(j for j,s in enumerate(secs) if s.get("hi")); offs[li]=(4,mode)
    total=sum(s["bars"] for s in secs)
    bpm=BPMS[i]
    pools=MAJP if mode=="maj" else MINP
    names=list(pools); vkey=names[pv%len(names)]; ckey=names[pc_%len(names)]; bkey=names[pb%len(names)]
    PREPOOL=PREM if mode=="maj" else PREN; prekey=PREPOOL[i%len(PREPOOL)]
    fpools={"maj":MAJP,"min":MINP}
    def prog(poolname,mode_,off):
        p=(MAJP if mode_=="maj" else MINP)
        key=poolname if poolname in p else list(p)[names.index(poolname)%len(p)] if poolname in names else list(p)[0]
        return [((T+off+o)%12,q) for o,q in p[key]]
    def pre_prog(mode_,off):
        base=(PREM if mode_=="maj" else PREN)[i%(len(PREM) if mode_=="maj" else len(PREN))]
        return [((T+off+o)%12,q) for o,q in base]
    # ---- 区間ごとの和音 ----
    chords=[]; sec_chords=[]
    for si,s in enumerate(secs):
        off,md=offs[si]; k=s["kind"]; n=s["bars"]
        if k in("verse","intro","inter","outro","solo"): base=prog(vkey if k!="solo" else ckey,md,off) if True else None
        if k=="chorus": base=prog(ckey,md,off)
        if k=="pre": base=pre_prog(md,off)
        if k=="bridge": base=prog(bkey,md,off)
        if k=="intro" and intro_kind==3: base=prog(ckey,md,off)
        cs=[]
        for b in range(n):
            c=base[b%4]
            if k in("verse","chorus","solo") and b%8==7: c=((T+off+7)%12,"M")
            cs.append(c)
        if k=="outro": cs[-1]=((T+off)%12,"m" if md=="min" else "M"); cs[-2]=((T+off+7)%12,"M") if n>2 else cs[-2]
        sec_chords.append(cs)
    for si in range(len(secs)-1):  # 転調の手前はドミナント（新しい調のV）
        if offs[si+1]!=offs[si]:
            o2,_=offs[si+1]; sec_chords[si][-1]=((T+o2+7)%12,"M")
    # ---- 旋律 ----
    home_r0=60+T if T<=6 else 48+T
    material={}
    lead=[];lead2=[];gl=[];gr=[];bass=[];kick=[];snare=[];hat=[];tomp=[];crashp=[];allch=[]
    occ={}
    fillctr={}
    Wd=lambda a,b:rng.choice([a,b])
    for si,s in enumerate(secs):
        off,md=offs[si]; k=s["kind"]; n=s["bars"]; cs=sec_chords[si]
        tonic=T+off; r0=home_r0+off
        lo={"verse":r0-3,"chorus":r0+4,"pre":r0,"solo":r0+3,"inter":r0-3,"bridge":r0-3,"intro":r0,"outro":r0+2}[k]
        hi=min(86,lo+17); lo=max(50,min(lo,hi-14))
        sc=scale_list(tonic,md,lo,hi)
        occ[k]=occ.get(k,0)+1
        key=k
        nph=(n+3)//4
        if key not in material:
            mat=[]
            for p in range(max(4,nph+s["ph0"])):
                mat.append(new_phrase(rng,k if k in RHY else "verse",mat[p-1] if p>0 else None))
            material[key]=mat
        mat=material[key]
        if occ[k]>=2 and not s.get("hi"):  # 2回目以降は少し変える
            mat=[[dict(b) for b in ph] for ph in mat]
            for ph in mat:
                j=rng.randrange(4); ph[j]=new_bar(rng,k if k in RHY else "verse",ph[j]["cad"])
        mel=[]
        heights=HEIGHT[k]
        for b in range(n):
            ph=mat[s["ph0"]+b//4]; spec=ph[b%4]
            h=heights[b%4]+(0.08 if (s.get("hi") or (k=="chorus" and off>=2)) else 0)
            target=lo+h*(hi-lo)
            nextc=cs[b+1] if b+1<n else (sec_chords[si+1][0] if si+1<len(secs) else None)
            mel.append(realize(spec,cs[b],nextc,target,sc,lo,hi,rng,k))
        text=" ".join(mel)
        if k=="inter" or (k=="bridge" and md!="x"):
            pass
        lead.append(text)
        # ハモリ: サビの2回目以降・ソロ
        if (k=="chorus" and occ[k]>=2) or k=="solo":
            S=MAJ if md=="maj" else MIN
            def hm(t):
                mm=re.match(r"^([A-G]#?)(-?\d)(:.*)$",t)
                if not mm: return t
                p=NAMES.index(mm.group(1))+12*(int(mm.group(2))+1)
                if (p-tonic)%12 in S:
                    c=0
                    while c<2:
                        p+=1
                        if (p-tonic)%12 in S: c+=1
                else: p+=3
                while p>88: p-=12
                return nn(p)+mm.group(3)
            lead2.append(" ".join(hm(t) for t in text.split()))
        else: lead2.append(f"R:{4*n}")
        # ---- ギター・ベース・ドラム ----
        for b,c in enumerate(cs):
            allch.append(c)
            L,R=guitar_bar(rng,c,k,occ[k],b,n,gprof,intro_kind)
            gl.append(L); gr.append(R)
            bass.append(bass_bar(rng,c,k,occ[k],b,n,intro_kind))
            K,Sn,Ht,tom,cr=drum_bar(rng,k,occ[k],b,n,(fc if k in("chorus","solo","outro") else fv),intro_kind,fillctr,off,s)
            kick.append(slots(K)); snare.append(slots(Sn)); hat.append(slots(Ht)); tomp.append(tomslots(tom)); crashp.append(slots("X..............." if cr else "................"))
    G={"noRestrike":True,"chorus":0,"humanPitch":0}
    def part(inst,role,notes,vol,pan,patch,amp,extra):
        d={"instrument":inst,"role":role,"volume":vol,"pan":pan,"amp":amp,"notes":" ".join(notes)}
        if patch: d["patch"]=patch
        d.update(extra); return d
    mods={"none":"転調なし","up1":"最後のサビで半音上げ","up2":"サビ2回を全音上げ","up3":"最後のサビで短3度上げ","up5":"最後のサビで完全4度上げ","par":"最後のサビで同主調に切りかえ","rel":"Cメロとソロで平行調へ→主調にもどる","midup":"ソロから全音上げたまま","down2":"Cメロで全音下げ→最後のサビで全音上げ","ladder":"最後のサビを全音→長3度と2段上げ"}
    song={"title":slug,"description":f"メロコアパンク（仮・試作）「{jp}」。{'長調' if mode=='maj' else '短調'}、BPM{bpm}、{total}小節。{mods[plan]}。",
     "bpm":bpm,"beats":4,"chords":" ".join(cname(c) for c in allch),"barsPerChord":1,"repeats":1,"feel":"rock","tone":"rock",
     "autoAccompaniment":False,"dynamics":"natural","human":0.45,"humanProfile":"role","lockToKick":True,"autoScoop":False,"fills":False,
     "drumMix":{"tom":{"tune":-4,"level":1.4,"spread":0.5}},
     "parts":[part("leadGuitar","メロディ／ソロ",lead,0.3,0,"cleanGuitar","clean",{**G,"reverb":0.2}),
      part("leadGuitar","ハモリ（3度上）",lead2,0.2,0.25,"cleanGuitar","clean",{**G,"reverb":0.2}),
      part("leadGuitar","リフ（左・ルート）",gl,0.16,-0.6,"cleanGuitar","overdrive",{**G,"reverb":0.08}),
      part("leadGuitar","リフ（右・5度）",gr,0.16,0.6,"cleanGuitar","overdrive",{**G,"reverb":0.08}),
      part("bass","ベース（旋律）",bass,0.6,0,None,"auto",{"bright":0.3}),
      part("kick","キック",kick,0.26,0,None,"auto",{}),part("snare","スネア",snare,0.2,0,None,"auto",{}),part("hihat","ハイハット",hat,0.09,0.3,None,"auto",{}),
      part("tom","タム",tomp,0.3,0,None,"auto",{}),part("crash","クラッシュ",crashp,0.16,0.2,None,"auto",{})]}
    for p in song["parts"]:
        assert abs(beats(p["notes"])-4*total)<1e-6,(slug,p["role"],beats(p["notes"]),4*total)
    meta={"slug":slug,"jp":jp,"bpm":bpm,"bars":total,"mode":mode,"tonic":NAMES[T],"plan":mods[plan],"template":tpl,"verse":vkey,"chorus":ckey,"bridge":bkey,"intro":intro_kind,"drums":[fv,fc],"seconds":round(total*240/bpm)}
    return song,meta
# ================= 演奏 =================
def slots(sym): return " ".join("R:0.25" if c=="." else f"{c}:0.25" for c in sym)
def tomslots(l): return " ".join("R:0.25" if t is None else f"{t}:0.25" for t in l)
VK=["X.......x.x.....","X.....x.x.......","X.......x.....x.","X..x....x.x.....","X.x.....x.....x.","X.......X.x...x."]
CK=["X.x.X.x.X.x...x.","X.x.X.x.X.x.x.x.","X.x.X.x.X.x...x.","X.x.X.x.X.x.x.xx","X...X.x.X.x.X.x."]
DK=["XxxxXxxxXxxxXxxx","XxxxXxxxXxxxxxXx","X.xxx.xxX.xxx.xx","XxxxXx.xXxxxXxxx"]
SNV=["....X.......X...","....X..o....X...","....X.......X..o","....X..o....X.o."]
FL="A2"
FILLS=[("X.......X.......","....X...ooxxxXXX",[None]*16),("X.......X.......","....X...........",[None]*8+["C4","C4","A3","A3","G3","G3",FL,FL]),
       ("X.......X.......","....X...xxXX....",[None]*12+["A3","G3",FL,FL]),("X.......X...X...","....X.......XXXX",[None]*16),("X.......X.......","....X.......x.xX",[None]*12+["C4",None,FL,FL])]
def feel_pat(rng,feel,heavy):
    if feel=="skate": return ("X...X...X...X...","..X...X...X...X.","x.x.x.x.x.x.x.x.")
    if feel=="dbeat": return (rng.choice(["X.x.X...X.x.X...","X.xxX...X.x.X..."]),"....X.......X...","X.x.x.x.X.x.x.x.")
    return ((rng.choice(CK) if heavy else rng.choice(VK)),rng.choice(SNV),rng.choice(["x.x.x.x.x.x.x.x.","X.x.x.x.X.x.x.x.","X.x.x.xoX.x.x.x."]))
def drum_bar(rng,k,idx,i,n,feel,intro_kind,fc,off,s):
    K="X..............."; Sn="................"; Ht="................"; tom=[None]*16; cr=False; fl=None
    heavy=k in("chorus","solo","outro")
    if k=="intro":
        start={0:4,1:0,2:2,3:2,4:4}[intro_kind]
        if i>=start:
            K,Sn,Ht=feel_pat(rng,feel,False); cr=(i==start and intro_kind!=3)
            if intro_kind==3 and i<4: Sn="................"; K="X..............." if i%2==0 else "X.......x......."; Ht="x...x...x...x..."
        if i==n-1 and n>=4: K="X..............."; Sn="xxxxxxxxxxxxXXXX"; Ht="................"; tom=[None]*16
    elif k in("verse",):
        K,Sn,Ht=feel_pat(rng,feel,False)
        if idx==1 and rng.random()<0.5: Ht="X.x.x.x.X.x.x.x."
        if idx==1 and i==0: cr=True
        if i%8==7 and i!=n-1: fl=rng.randrange(5)
        elif i%4==3 and rng.random()<0.25: fl=rng.choice([1,4])
        if idx==1 and i<4 and feel!="skate" and False: pass
    elif k=="pre":
        K="X...X...X...X..." if i>=n//2 else rng.choice(VK)
        Sn="....x.......x..." if i<n//2 else ("x...x...x...x..." if i<n-1 else "xxxxxxxxXXXXXXXX"); Ht="x.x.x.x.x.x.x.x."
        if i==n-1: K="X.......X......."
    elif k in("chorus","outro"):
        K,Sn,Ht=feel_pat(rng,feel,True); cr=(i%4==0) or (i==8 and n>=16)
        if k=="chorus" and idx>=3 and feel!="skate" and i>=8: K=rng.choice(DK)
        if i in(3,7,11) and rng.random()<0.6: fl=rng.randrange(5)
        if k=="outro":
            if i<n-4: pass
            elif i<n-1: K="X.......X......."; Sn="........X......."; Ht="x...x...x...x..."; cr=(i==n-4)
            else: K="X..............."; Sn="X..............."; Ht="X..............."; cr=True
        if k=="chorus" and i==0: tom[0]=FL; cr=True
        if k=="chorus" and i==n-1 and not s.get("hi") and idx>=1: fl=3
    elif k=="inter":
        K="X..............." if i%2==0 else "X.......x......."; Ht="x...x...x...x..."; Sn="............o..." if i%4==3 else "................"
        if i==n-1: Sn="xxxxxxxxXXXXXXXX"; K="X.......X......."; Ht="................"
    elif k=="solo":
        K,Sn,Ht=feel_pat(rng,feel,i>=n//2); cr=(i%8==0)
        if i==7: fl=rng.randrange(5)
        if i==n-1: Sn="xxxxxxxxxxxxXXXX"; K="X.......X......."; Ht="................"
    elif k=="bridge":
        if i<n//2: K="X..............." if i%2==0 else "X.......x......."; Ht="o...o...o...o..."
        elif i<n-1:
            K="X...X...X...X..."; Sn="....x.......x..." if i<n-4 else "x.x.x.x.x.x.x.x."; Ht="x.x.x.x.x.x.x.x."
        else: K="X.......X......."; Sn="xxxxxxxxxxxxXXXX"
    if fc.get("after") and not(k=="intro") and i>0:
        tom[0]=FL; cr=True
    fc["after"]=False
    if fl is not None:
        kk,ss,tt=FILLS[fl]; K=K[:8]+kk[8:]; Sn=Sn[:8]+ss[8:]; Ht=Ht[:8]+"........"; tom=tt; fc["after"]=True
    return K,Sn,Ht,tom,cr
def bass_bar(rng,c,k,idx,i,n,intro_kind):
    r=root_b(c); t=third(c)
    def seq(l):
        out=[]
        for d,b in l:
            m=r+d
            while m>50: m-=12
            out.append(f"{nn(m)}:{b}")
        return " ".join(out)
    P8=[(0,.5)]*8; PUMP=[(0,.5),(0,.5),(12,.5),(0,.5),(0,.5),(0,.5),(12,.5),(7,.5)]; DRV=[(0,.5)]*6+[(7,.5),(0,.5)]
    SYN=[(0,1),(0,.5),(0,.5),(0,1),(7,.5),(12,.5)]; MEL=[(0,1),(t,.5),(7,.5),(12,1),(7,1)]; MEL2=[(0,1.5),(7,.5),(12,1),(t+12,1)]
    WALK=[(0,.5),(0,.5),(t,.5),(7,.5),(12,.5),(7,.5),(t,.5),(0,.5)]; END=[(0,1),(0,.5),(7,.5),(12,.5),(7,.25),(t,.25),(0,1)]
    LONG=[(0,2),(7,1),(t,1)]; UP=[(0,.5),(0,.5),(t,.5),(t,.5),(7,.5),(7,.5),(12,.5),(14,.5)]
    end=(i%4==3)
    if k=="intro":
        st={0:4,1:0,2:0,3:2,4:4}[intro_kind]
        if i<st: return "R:4"
        return seq(MEL2 if intro_kind==2 and i<4 else (END if i==n-1 else SYN))
    if k=="verse": return seq(END if i%8==7 else rng.choice([MEL,MEL2,SYN,WALK] if idx>1 else [MEL,MEL2,SYN]))
    if k=="pre": return seq(WALK if i==n-1 else UP)
    if k=="chorus": return seq(END if i%8==7 else (rng.choice([P8,PUMP,DRV]) if not end else MEL2))
    if k=="inter": return seq(LONG) if i%2==0 else seq(MEL2)
    if k=="solo": return seq(rng.choice([PUMP,DRV,P8]) if not end else MEL)
    if k=="bridge": return seq(LONG) if i<n-1 else "R:4"
    if k=="outro": return seq(PUMP) if i<n-4 else (seq(LONG) if i<n-1 else f"{nn(r)}:1 R:3")
def guitar_bar(rng,c,k,idx,i,n,prof,intro_kind):
    r=root_g(c); f=r+7
    def cell(m,name):
        a=nn(m)
        return {"e8":" ".join(f"{a}:0.5"+("!" if q in(0,4) else "")+"'" for q in range(8)),
                "e8o":" ".join(f"{a}:0.5"+("!" if q in(0,4) else "") for q in range(8)),
                "sync":f"{a}:1! {a}:0.5 {a}:0.5 {a}:1 {a}:0.5 {a}:0.5","push":f"{a}:0.5! {a}:0.5 R:0.5 {a}:0.5 {a}:1! {a}:0.5 {a}:0.5",
                "ring":f"{a}:2! {a}:1 {a}:0.5 {a}:0.5","hit":f"{a}:1! R:3","s16":" ".join(f"{a}:0.25"+("!" if q%4==0 else "") for q in range(16)),
                "whole":f"{a}:4","rest":"R:4","off":" ".join(f"R:0.5 {a}:0.5" for _ in range(4))}[name]
    VERSE=[["e8","e8","push"],["push","off","e8"],["e8","sync","e8"],["s16","e8","push"]][prof]
    CHOR=[["sync","push","ring"],["e8o","sync","ring"],["sync","e8o","push"],["push","sync","e8o"]][prof]
    last=(i==n-1)
    if k=="intro":
        st={0:4,1:0,2:2,3:4,4:4}[intro_kind]
        if intro_kind==4 and i<4: nm=("whole","rest")
        elif i<st: nm=("rest","rest")
        else: nm=("e8","e8") if i<n-1 else ("s16","s16")
    elif k=="verse":
        x=rng.choice(VERSE); nm=(x,rng.choice([x,"rest"]) if idx==1 and i<8 else x)
        if last: nm=("hit","hit")
    elif k=="pre": nm=("e8","e8") if i<n-1 else ("s16","s16")
    elif k in("chorus",):
        x=rng.choice(CHOR) if i%4!=3 else rng.choice(["e8o","push"]); nm=(x,x)
        if last and idx>=1: nm=("hit","hit")
    elif k=="inter": nm=("rest","rest")
    elif k=="solo":
        x=rng.choice(CHOR); nm=(x,x)
        if last: nm=("hit","hit")
    elif k=="bridge":
        if i<n//2: nm=("rest","whole")
        elif i<n-4: nm=("whole","whole")
        elif i<n-1: nm=("e8o","e8o")
        else: nm=("rest","rest")
    elif k=="outro": nm=(("sync","sync") if i<n-4 else (("whole","whole") if i<n-1 else ("hit","hit")))
    return cell(r,nm[0]),cell(f,nm[1])
if __name__=="__main__":
    arg=sys.argv[1]; out=sys.argv[2] if len(sys.argv)>2 else "."
    ids=range(20) if arg=="all" else [int(arg)]
    metas=[]
    for i in ids:
        song,meta=build(i)
        json.dump(song,open(os.path.join(out,f"{i+1:02d}-{meta['slug']}.json"),"w"),ensure_ascii=False)
        metas.append(meta); print(i+1,meta["slug"],meta["jp"],meta["tonic"],meta["mode"],meta["bpm"],meta["seconds"],meta["plan"],file=sys.stderr)
    json.dump(metas,open(os.path.join(out,"_meta.json"),"w"),ensure_ascii=False,indent=1)
