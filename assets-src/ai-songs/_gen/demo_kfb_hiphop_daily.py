import json, sys
sys.path.insert(0,'assets-src/ai-songs/_gen')
BARS=16
V={ 'Dbmaj9':['F3','C4','D#4','G#4'],'C7#9':['E3','A#3','D#4','G4'],'Fm9':['G#3','D#4','G4','C5'],'Bb13':['G#3','D4','G4','C5'],'Ebm9':['F#3','C#4','F4','A#4'],'Ab13':['F#3','C4','F4','A#4'],
    'Gb13':['E3','A#3','D#4','G#4'],'E9':['G#3','D4','F#4','B4'],'D9':['F#3','C4','E4','A4'],'Bmaj7':['A#3','D#4','F4','A#4'],'Bbm11':['G#3','C#4','D#4','G#4']}
CH=['Dbmaj9','C7#9','Fm9','Bb13','Ebm9','Ab13','Dbmaj9','Gb13','Fm9','E9','Ebm9','D9','Dbmaj9','C7#9','Bmaj7','Bbm11']
ROOT={'Dbmaj9':'C#2','C7#9':'C2','Fm9':'F2','Bb13':'A#1','Ebm9':'D#2','Ab13':'G#1','Gb13':'F#1','E9':'E2','D9':'D2','Bmaj7':'B1','Bbm11':'A#1'}
def up(n,k=1): return f"{n[:-1]}{int(n[-1])+k}"
def toks(events,total=BARS*4):
    """events: (拍, 音, 長さ, 強さ) → 'R:.. 音:長さ%強さ'"""
    out=[]; t=0
    for b,n,d,v in sorted(events):
        if b>t+1e-6:
            g=b-t
            while g>16: out.append("R:16"); g-=16
            out.append(f"R:{g:.4f}")
        out.append(f"{n}:{d:.4f}%{v}"); t=b+d
    g=total-t
    while g>16: out.append("R:16"); g-=16
    if g>1e-6: out.append(f"R:{g:.4f}")
    return " ".join(out)
# ---- ギターの和音（4本の弦を少しずつずらして鳴らす＝ストローク）
GP={0:[(0,3.0,84,1),(3.5,0.4,62,-1)],1:[(0,2.5,80,1),(3.0,0.35,58,-1),(3.5,0.4,70,1)],
    'A':[(0,1.2,86,1),(2.5,0.35,60,-1),(3.5,0.45,72,1)],'B':[(0.5,1.3,82,-1),(2.0,1.2,78,1),(3.75,0.2,50,-1)],'C':[(0,0.4,84,1),(0.75,0.35,64,-1),(1.5,1.4,80,1),(3.5,0.4,66,-1)],
    'stop':[(0,3.6,88,1)],'arp':[(0,3.8,70,2)],'end':[(0,4.0,74,3)]}
PAT=[0,1,'A','B','A','C','A','stop','B','A','C','stop','A','B','arp','end']
gs=[[] for _ in range(4)]
for bar,(c,pt) in enumerate(zip(CH,PAT)):
    for (b,d,v,dirn) in GP[pt]:
        for j in range(4):
            jj=j if dirn>0 else 3-j; per={1:0.012,-1:0.009,2:0.5,3:0.06}[dirn]; lag=per*jj-(per*1.5 if dirn in (1,-1) and bar*4+b>0 else 0)   # ストロークの最後の弦が拍の頭に来る（遅れて聞こえない）
            gs[j].append((bar*4+b+lag, V[c][j], max(0.12,min(d-lag,(bar+1)*4-(bar*4+b+lag))), max(30,v-(3-j)*3 if dirn>0 else v-j*4)))
GT={"instrument":"distGuitar","di":"gretsch","sustain":1.6,"release":0.25,"chorus":0,"humanPitch":0,"noScoop":True,"stringNoise":True,"humanTiming":0,"double":False,"powerChord":False,"amp":"jpopClean","ampDrive":0.08,
    "fx":[{"type":"compressor","threshold":-20,"ratio":3,"attack":0.012,"release":0.15},{"type":"filter","kind":"highpass","freq":140,"q":0.7},{"type":"eq","low":-1,"mid":1.5,"midHz":1800,"high":-1},{"type":"filter","kind":"lowpass","freq":6200,"q":0.6},{"type":"room","mix":0.14}]}
parts=[dict(GT,role=f"ギターの和音・弦{j+1}",pan=-0.3,volume=0.125,notes=toks(gs[j]),swing=0) for j in range(4)]
# ---- ベース
BP={'A':[(0,1.4,96),(1.75,0.25,70),(2.5,1.0,90)],'B':[(0,0.9,96),(1.5,0.5,78),(2.5,0.7,88),(3.5,0.5,'o')],'C':[(0,1.9,96),(2.75,0.25,72),(3.0,0.9,'o')]}
bs=[]
for bar,c in enumerate(CH):
    if bar<2 or bar in (14,): continue
    if bar==15: bs.append((bar*4,ROOT[c],3.5,90)); continue
    if bar in (7,11): bs.append((bar*4,ROOT[c],1.0,96)); continue
    for b,d,v in BP['ABC'[bar%3]]:
        n=up(ROOT[c]) if v=='o' else ROOT[c]; bs.append((bar*4+b,n,d,80 if v=='o' else v))
parts.append(dict(role="はじく FM のベース",instrument="bass",patch="kfbFmBass",volume=0.06,pan=0,notes=toks(bs),swing=0))
# ---- ドラム（kawaiiFx: A4 キック A#4 スネア B4 クラップ C5 スナップ C#5/D5 ハット D#5 リム C6 シェイカー）
K=[];S=[];H=[];SH=[];RM=[]
KP={'A':[0,1.75,2.5],'B':[0,0.75,2.5,3.5],'C':[0,2.25,2.75]}
for bar in range(2,14):
    o=bar*4
    if bar in (7,11):
        K.append((o,'A4',0.5,100)); RM.append((o+1,'D#5',0.5,84))
        if bar==7: S+= [(o+3.0,'A#4',0.25,70),(o+3.25,'A#4',0.25,60),(o+3.5,'A#4',0.25,84),(o+3.75,'B4',0.25,96)]
        else: S+= [(o+3.5,'C5',0.25,80),(o+3.75,'C5',0.25,92)]
        continue
    for b in KP['ABC'[(bar+1)%3]]: K.append((o+b,'A4',0.25,100 if b==0 else 84))
    S.append((o+1,'C5' if bar<8 else 'B4',0.5,92)); S.append((o+3,'A#4',0.5,96)); RM.append((o+1,'D#5',0.4,70))
    if bar%2: RM.append((o+2.25,'D#5',0.25,48))
    for i in range(8):
        b=i*0.5
        if bar>=8 and i==7: H+= [(o+3.5,'C#5',0.125,62),(o+3.625,'C#5',0.125,54),(o+3.75,'C#5',0.125,66),(o+3.875,'D5',0.125,74)]; continue
        H.append((o+b,'D5' if (i==3 and bar%2==0) else 'C#5',0.25,78 if i%2==0 else 52))
    if bar>=8:
        for i in range(16): SH.append((o+i*0.25,'C6',0.2,[60,34,48,38][i%4]))
S.append((7.5,'C5',0.25,70)); S.append((7.75,'C5',0.25,84))
dr=lambda r,ev,vol,pan,rev,sw: dict(swing=0,role=r,instrument="lead",patch="kawaiiFx",modulate=False,volume=vol,pan=pan,reverb=rev,notes=toks(ev))
parts+=[dr("キック",K,0.11,0,0.03,0),dr("スネア・スナップ・リム",S,0.085,0.05,0.1,0.35),dr("リム",RM,0.06,-0.1,0.1,0.35),dr("ハイハット",H,0.045,0.25,0.06,0.45),dr("シェイカー",SH,0.028,-0.35,0.08,0.3)]
# ---- メロディ（ゆれる電子のリード）と、電子のサックス・バラフォン・筒の鉄琴のやりとり
R4="R:4"
lead=[R4,R4,"R:0.5 C5:0.5 D#5:0.5 F5:1 D#5:0.5 C5:1","G5:1.5 F5:0.5 D5:1 R:1",R4,R4,"R:0.5 G#5:0.5 F5:0.5 D#5:0.5 C5:1.5 D#5:0.5","E5:1 R:3",
      "R:0.5 C5:0.5 D#5:0.5 G5:1 G#5:0.5 G5:1","F#5:1.5 E5:0.5 B4:1 R:1","R:0.5 A#4:0.5 C#5:0.5 F5:1 F#5:0.5 F5:1","E5:1.5 R:2.5","R:0.5 C5:0.5 D#5:0.5 F5:0.5 G#5:1 C6:1","A#5:0.5 G5:0.5 E5:1 D#5:1 C5:1","A#4:2 R:2",R4]
sax=[R4]*4+["R:1 A#4:0.5 C#5:0.5 F5:1.5 D#5:0.5","C5:1 R:0.5 G#4:0.5 A#4:0.5 C5:0.5 R:1"]+[R4]*2+["R:3 D#5:0.5 F5:0.5",R4,"R:3 C#5:0.5 D#5:0.5",R4,"G#4:2 R:2","G4:2 R:2",R4,R4]
bal=[R4]*3+["R:3 A#4:0.25 D5:0.25 G5:0.5",R4,"R:3 C5:0.25 F5:0.25 A#5:0.5",R4,"R:1.5 A#4:0.25 D#5:0.25 G#5:0.5 R:1.5",R4,"R:3 B4:0.25 E5:0.25 F#5:0.5",R4,"R:2 A4:0.25 C5:0.25 E5:0.25 A5:0.25 R:1",R4,"R:3.5 G5:0.25 A#5:0.25","R:1 D#5:0.5 F5:0.5 A#5:1 R:1",R4]
glk=[R4]*8+["R:3.5 G6:0.5",R4,"R:3.5 F6:0.5",R4,"R:1.5 C7:0.5 G#6:0.5 R:1.5",R4,"R:2 A#6:0.5 F6:0.5 D#6:1","R:0.5 G#6:3.5"]
mk=lambda r,p,n,vol,pan,rev,**k: dict(role=r,instrument="lead",patch=p,notes=" ".join(n),volume=vol,pan=pan,reverb=rev,**k)
parts+=[mk("ゆれる電子のリード","kfbWobbleLead",lead,0.1,0.05,0.22,mono=True),mk("電子のサックス","kfbFutureSax",sax,0.06,0.35,0.2,mono=True),mk("バラフォン","balafon",bal,0.14,-0.45,0.18),mk("筒の鉄琴","tubeGlock",glk,0.1,0.4,0.3)]
# ---- 効果音: レコードのパチパチ（最初から）、小物（フレクサトーン・ラチェット・ウインドチャイム・フィンガーシンバル）
parts.append(dict(role="レコードのパチパチ",instrument="lead",patch="kawaiiFx",modulate=False,volume=0.05,pan=0,reverb=0.05,notes="A#5:12 A#5:12 A#5:12 A#5:12 A#5:12 R:4",swing=0))
parts.append(dict(role="おもちゃと小物",instrument="lead",patch="toysFx",modulate=False,volume=0.06,pan=0.2,reverb=0.2,notes=toks([(6.5,'G4',1.5,80),(29.5,'A#4',1.0,80),(45.5,'G#4',1.0,76),(56,'C#5',4,80),(60,'D#5',4,84)]),swing=0))
song={"title":"かわいい日常の音の試聴（ヒップホップ風）","bpm":86,"beats":4,"key":"G#","scale":"major","swing":0,"chords":" ".join(['C#maj7','C7','Fm7','A#7','D#m7','G#7','C#maj7','F#7','Fm7','E7','D#m7','D7','C#maj7','C7','Bmaj7','A#m7']),"barsPerChord":1,"repeats":1,"autoAccompaniment":False,"parts":parts}
json.dump(song,open('/tmp/kfb/demo4/hip.json','w'),ensure_ascii=False)
