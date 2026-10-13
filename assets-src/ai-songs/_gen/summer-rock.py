import json,sys
# 夏を感じるロック（仮）。A長調・bpm148。ギターのミュートは、ブロックの頭から終わりまで通す（弾いた直後に急にミュートへ変えない）。
SEC=[("intro",4),("verse",8),("pre",4),("chorus",8),("inter",4),("verse",8),("pre",4),("chorus",8),("solo",8),("bridge",4),("chorus",8),("chorus",8),("outro",4)]
CH={"intro":"A D A E","verse":"A C#m7 D E A C#m7 D Esus4","pre":"F#m7 E D B","chorus":"A E F#m D A E D E","inter":"A E D E","solo":"A E F#m D A E D B","bridge":"D A Bm7 E","outro":"A E D A"}
ROOT={"A":("A3","E4","A1"),"E":("E3","B3","E1"),"D":("D3","A3","D2"),"F#m":("F#3","C#4","F#1"),"F#m7":("F#3","C#4","F#1"),"C#m7":("C#3","G#3","C#2"),"B":("B2","F#3","B1"),"Bm7":("B2","F#3","B1"),"Esus4":("E3","B3","E1")}
TONES={"A":["A3","E4","A4","C#5"],"E":["E3","B3","E4","G#4"],"D":["D3","A3","D4","F#4"],"F#m":["F#3","C#4","F#4","A4"],"F#m7":["F#3","C#4","F#4","A4"],"C#m7":["C#4","E4","G#4","B4"],"B":["B3","F#4","B4","D#5"],"Bm7":["B3","F#4","A4","D5"],"Esus4":["E3","B3","E4","A4"]}
STAB={"A":"C#4","E":"B3","D":"A3","F#m":"A3","B":"D#4","Esus4":"A3"}
bars=[]  # (section, chord, indexInSection)
SECI=[]
for si,(s,n) in enumerate(SEC):
    cs=CH[s].split()
    for i in range(n): bars.append((s,cs[i%len(cs)],i,n)); SECI.append(si)
N=len(bars)
M={ # メロディ（各小節の拍の合計は4）
 "intro":["E5:1 A5:1 C#6:2","D6:1 B5:1 A5:2","C#6:1 A5:1 E5:2","G#5:2 B5:2"],
 "verse":["R:1 A4:0.5 B4:0.5 C#5:1 E5:1","E5:1.5 C#5:0.5 B4:2","A4:0.5 B4:0.5 D5:1 C#5:1 B4:1","G#4:1 B4:1 E5:2","R:1 A4:0.5 B4:0.5 C#5:1 E5:1","E5:1 F#5:1 E5:1 C#5:1","D5:1 C#5:1 B4:1 A4:1","B4:2 A4:1 B4:1"],
 "pre":["C#5:1 C#5:1 E5:1 F#5:1","G#5:1 G#5:1 B5:2","A5:1 A5:1 F#5:1 A5:1","B5:2 R:2"],
 "chorus":["E5:0.5 E5:0.5 C#5:1 E5:1 A5:1","G#5:1.5 B5:0.5 G#5:1 E5:1","F#5:0.5 F#5:0.5 A5:1 C#6:1 A5:1","B5:1.5 A5:0.5 F#5:2","E5:0.5 E5:0.5 C#5:1 E5:1 A5:1","G#5:0.5 B5:0.5 E6:1 D6:1 B5:1","A5:1 B5:1 C#6:1 D6:1","E6:2.5 R:1.5"],
 "inter":["A5:0.5 C#6:0.5 E6:1 C#6:1 A5:1","B5:0.5 G#5:0.5 E5:1 G#5:1 B5:1","A5:0.5 F#5:0.5 D5:1 F#5:1 A5:1","B5:2 G#5:2"],
 "solo":["A5:0.25 B5:0.25 C#6:0.25 E6:0.25 D6:0.25 C#6:0.25 B5:0.25 A5:0.25 C#6:1 E6:1","G#5:0.25 B5:0.25 E6:0.25 B5:0.25 G#5:0.25 B5:0.25 E6:0.25 D6:0.25 E6:2","F#5:0.25 A5:0.25 C#6:0.25 A5:0.25 F#5:0.25 A5:0.25 C#6:0.25 E6:0.25 C#6:1 A5:1","D6:0.25 C#6:0.25 B5:0.25 A5:0.25 B5:0.25 C#6:0.25 D6:0.25 B5:0.25 A5:2","E6:0.25 D6:0.25 C#6:0.25 B5:0.25 A5:0.25 B5:0.25 C#6:0.25 E6:0.25 C#6:1 E6:1","G#5:0.25 B5:0.25 E6:0.25 D6:0.25 B5:0.25 G#5:0.25 B5:0.25 E6:0.25 B5:2","A5:0.25 B5:0.25 D6:0.25 C#6:0.25 B5:0.25 A5:0.25 F#5:0.25 A5:0.25 D6:2","D#6:0.25 B5:0.25 F#5:0.25 B5:0.25 D#6:0.25 B5:0.25 F#5:0.25 D#5:0.25 B5:2"],
 "chorus_b":["E5:1 E5:0.5 C#5:0.5 E5:1 A5:1","G#5:1 B5:1 G#5:1 E5:1","F#5:1 A5:1 C#6:1 A5:1","B5:1 A5:1 F#5:1 D5:1","E5:0.5 E5:0.5 C#5:1 E5:1 A5:1","G#5:1 B5:1 E6:1 B5:1","A5:0.5 B5:0.5 C#6:1 D6:1 E6:1","E6:3 R:1"],
 "bridge":["F#5:2 A5:2","E5:2 C#5:2","D5:1 F#5:1 A5:2","G#5:2 B5:2"],
 "outro":["E5:0.5 E5:0.5 C#5:1 E5:1 A5:1","G#5:1.5 B5:0.5 G#5:2","A5:1 F#5:1 D5:2","A5:4"]}
def pat(chord,kind):
    r,f,_=ROOT[chord]
    return r,f
def build():
    gl,gr,bass,lead,arp,brass=[],[],[],[],[],[]
    kick,snare,hat,crash=[],[],[],[]
    chordsList=[]
    idx={}
    for b,(s,c,i,n) in enumerate(bars):
        chordsList.append(c)
        base=c.replace("m7","").replace("sus4","")  # 表引き用
        r,f,br=ROOT[c]
        last4=(i%4==3)  # 4小節ごとの最後
        fill=(i==n-1) or (n>=8 and i==3 and s=="verse")
        # ドラム
        full=s in("pre","chorus","solo","outro")
        if s=="intro": k="X.......X.......";sn="................" if b<2 else "............x.xX";h="x...x...x...x..."
        elif s=="bridge": k="X...............";sn="....o.......o...";h="x...x...x...x..."
        elif s=="inter": k="X.....x.X.......";sn="....X.......X...";h="x.x.x.x.x.x.x.x."
        elif s=="verse": k="X.....x...x.....";sn="....X.......X...";h="x.x.x.x.x.x.x.x."
        elif s=="pre": k="X.....x.X.x...x.";sn="....X.......X.x.";h="x.x.x.x.x.x.x.xx"
        else: k="X.....x.X.x...x.";sn="....X.......X...";h="x.X.x.X.x.X.x.X."
        if fill and s!="bridge": sn="....X...x.x.xXXX" if s!="verse" else "....X.......xXxX"; k="X.......X.x.x..." 
        if s=="solo" and i==n-1: sn="x.x.x.x.xxxxXXXX"
        if i==0 and s not in("intro","bridge","inter"): h="."+h[1:]
        if s=="outro" and i==0: h="."+h[1:]
        kick.append("g:"+k);snare.append("g:"+sn);hat.append("g:"+h)
        crash.append("g:X..............." if i==0 and s not in("intro","bridge","inter") or (s=="outro" and i==0) else "R:4")
        if s=="outro" and i==n-1:
            kick[-1]="g:X...............";snare[-1]="g:X...............";hat[-1]="R:4";crash[-1]="g:X..............."
        # ベース
        if s=="bridge": bass.append(f"{br}:2 {br}:2" if True else "")
        elif s=="intro" and b<2: bass.append("R:4")
        elif s in("verse","inter"): bass.append(f"{br}:1 {br}:0.5 {br}:0.5 {br}:1 {br}:0.5 {br}:0.5")
        elif s=="outro" and i==n-1: bass.append(f"{br}:4")
        else: bass.append(" ".join([f"{br}:0.5"]*8))
        # リズムギター（左＝根音、右＝5度）。verse だけ通してミュート。ブロックの途中で奏法を変えない
        if s in("intro","bridge","inter"): gl.append("R:4"); gr.append("R:4")
        elif s=="verse":
            gl.append(" ".join([f"{r}:0.5'"]*8)); gr.append(" ".join([f"{f}:0.5'"]*8))
        elif s=="pre":
            gl.append(" ".join([f"{r}:0.5!" if j%2==0 else f"{r}:0.5" for j in range(8)])); gr.append(" ".join([f"{f}:0.5!" if j%2==0 else f"{f}:0.5" for j in range(8)]))
        elif s=="solo":
            gl.append(f"{r}:1.5! {r}:0.5 {r}:2"); gr.append(f"{f}:1.5! {f}:0.5 {f}:2")
        elif s=="outro" and i==n-1:
            gl.append(f"{r}:4!"); gr.append(f"{f}:4!")
        else:
            gl.append(f"{r}:1.5! {r}:0.5 {r}:0.5 {r}:0.5 {r}:0.5 {r}:0.5"); gr.append(f"{f}:1.5! {f}:0.5 {f}:0.5 {f}:0.5 {f}:0.5 {f}:0.5")
        # リード
        key=s
        if s=="chorus":
            cnum=sum(1 for q in SEC[:SECI[b]] if q[0]=="chorus")  # 何回目のサビか(0始まり)
            if cnum==2 or (cnum==3 and i<4): key="chorus_b"
        lead.append(M[key][i % len(M[key])])
        # クリーンのアルペジオ（intro・bridge・outro・verse裏・inter）
        t=TONES[c]
        if s in("intro","bridge","outro","inter","verse"):
            order=[0,1,2,3,2,1,2,3]
            arp.append(" ".join(f"{t[o]}:0.5" for o in order) if not(s=="outro" and i==n-1) else f"{t[0]}:4")
        else: arp.append("R:4")
        # ブラス（サビの2回目以降、裏拍の合いの手）
        cc=c if c in STAB else c.replace("m7","m") 
        st=STAB.get(c) or STAB.get(c.replace("7",""))
        if s=="chorus" and b>=SEC_START_C2 and st:
            brass.append(f"R:1.5 {st}:0.5 R:1.5 {st}:0.5")
        else: brass.append("R:4")
    return chordsList,dict(kick=kick,snare=snare,hat=hat,crash=crash,bass=bass,gl=gl,gr=gr,lead=lead,arp=arp,brass=brass)
SEC_START_C2=sum(n for s,n in SEC[:7])  # 2回目のサビから
chords,P=build()
def part(inst,role,vol,pan,key,**kw):
    d={"instrument":inst,"role":role,"volume":vol,"pan":pan,"notes":" ".join(P[key])}; d.update(kw); return d
song={"title":"まぶしい夏の入口（ロック）","description":"（見本・仮）夏を感じる明るいロック。A長調・bpm148・8ビート。サビはスネアを強く、2回目以降はブラスの合いの手。ギターのミュートは、Aメロのブロックを通して使い、弾いた直後に急に切りかえない。","bpm":148,"beats":4,"chords":" ".join(chords),"barsPerChord":1,"repeats":1,"autoAccompaniment":False,"feel":"rock","tone":"rock","human":0.2,"dynamics":"natural",
"parts":[
 part("kick","キック",0.14,0,"kick"),part("snare","スネア",0.1,0,"snare"),part("hihat","ハイハット",0.05,0,"hat"),part("crash","クラッシュ",0.06,0,"crash"),
 part("bass","ベース（根音の8分）",0.12,0,"bass"),
 part("distGuitar","リズムギター左（根音）",0.07,-0.75,"gl",amp="loudrock"),
 part("distGuitar","リズムギター右（5度）",0.07,0.75,"gr",amp="loudrock"),
 part("leadGuitar","リード（メロディ・ソロ）",0.11,0.1,"lead",amp="lead",noRestrike=True,fx=[{"type":"delay","beats":0.75,"mix":0.15,"feedback":0.3},{"type":"plate","mix":0.15}]),
 part("guitar","クリーンのアルペジオ",0.07,-0.35,"arp",amp="crystal",chorus=0,sustain=1.8,reverb=0.3),
 part("brass","ブラスの合いの手",0.08,0.3,"brass",patch="brassSection",reverb=0.25)]}
json.dump(song,open(sys.argv[1],"w"),ensure_ascii=False,indent=1)
print("小節",N,"拍",N*4,"秒",round(N*4*60/148))
