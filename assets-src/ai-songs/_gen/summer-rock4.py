import json,sys
# 夏のロック v3: 人間の指摘「ロック感が全くない」→ 歪みギターを主役に左右で重ね、ドラム・ベースを前に出し、全体を押し出す。
# （v2の注記） 人間の指摘（2026-10-14）「ギターの単音（メロディ・アルペジオ）は電子の音にしか聞こえない。コードをそのまま弾くのはよい。刻みの音の途切れ方が不自然」に合わせた作り直し。
#   - ギターは単音を弾かない。和音のストローク（strum）だけ。音は伸ばして自然に消える（ミュート・短い切りは使わない）
#   - メロディはトランペット（VSCO 録音）、ソロはグランドピアノ（Salamander 録音）、アルペジオもピアノ
src=open(__file__.replace("summer-rock4.py","summer-rock.py")).read().split("chords,P=build()")[0]
sys.argv=[sys.argv[0]]+sys.argv[1:]
exec(src)
chords,P=build()

# ── ドラム v4: 緩急（曲全体の強弱曲線）・間（抜く小節、最後の拍の空白）・グルーブ（バックビートの遅れ）──
import random
def arc_level(sec,si,i,n,cn):
    """小節ごとの全体の強さ(0〜1.2)。場面ごとに上げ下げして、曲全体で山をつくる。"""
    f=i/max(1,n-1)
    if sec=="intro": return 0.6+0.2*f
    if sec=="verse": return (0.68+0.12*f) if si<5 else (0.8+0.1*f)
    if sec=="pre": return (0.85+0.15*f) if si<5 else (0.92+0.14*f)
    if sec=="chorus": return [1.0,1.05,1.1,1.14][min(cn,3)]*(0.93 if i%4==3 else 1.0)
    if sec=="inter": return 0.78
    if sec=="solo": return 0.9+0.1*f
    if sec=="bridge": return 0.55+0.3*f
    return 1.0-0.25*f  # outro
def varied_drums():
    K,S,H,C,T,R,G=[],[],[],[],[],[],[]
    for b,(sec,c,i,n) in enumerate(bars):
        rnd=random.Random(2000+b*13+i*3)
        si=SECI[b]; cn=sum(1 for q in SEC[:si] if q[0]=="chorus"); vi=sum(1 for q in SEC[:si] if q[0]=="verse")
        ph=i%4; last=(i==n-1)
        k=sn=h="................"; cr="R:4"; tm=None; ride=None
        if sec=="intro":
            h="x...o...x...o..." if b<2 else "x.o.x.o.x.o.x.o."
            k="................" if b<1 else ("X..............." if b==1 else "X.......X.o.....")
            sn="................" if b<2 else "........o......." if b==2 else "....X.......X..."
            if last: sn="....o...o.x.xxXX"; tm="..........xxXXXX"; h="x.x.x.x.x.x....."  # 最後の拍はタムだけ（ハットを抜く）
        elif sec=="verse":
            if vi==1 and i<4 or vi==2 and False: pass
            if si<5 and i<4:   # 1回目のAメロ前半: ハーフタイム＋四分ハット（間を大きく）
                k=["X.......X..o....","X.......X.......","X......oX.......","X.......X.....o."][ph]
                sn="........X......." if ph<3 else "........X.....o."
                h="X...x...x...x..." if ph!=2 else "X...x...x...o..."
            else:                # 後半: ふつうのバックビート、ハットは強弱つき8分
                kp=["X.....x..x......","X.......X.x.....","X..o..x.X.......","X.....x.X..x...."]
                k=kp[(ph+vi)%4]
                h=rnd.choice(["X.x.o.x.X.x.o.x.","X.x.x.o.X.x.x.o.","X.o.x.x.X.o.x.x."])
                sn=rnd.choice(["....X.......X...","....X..o....X...","....X.......X..o","....X.o.....X.o."])
            if si>=5 and i<2: h="X.x.x.x.X.x.x.x."
            if i==0: cr="g:X..............."
            if last:
                sn=rnd.choice(["....X.......xxXX","....X...o.o.xxXX","....X..oo.o.xXXX"]); k="X.....x.X......."; tm=rnd.choice(["..............XX","............xxXX"])
                if rnd.random()<0.5: h="x.x.x.x.x......."  # 最後の2拍はハットを抜く
        elif sec=="pre":
            k=["................","X.......X.......","X...X...X...X...","X.x.X.x.X.x.X.x."][ph]
            sn=["........X.......","....X.......X...","....X.x.X.x.X.x.","o.o.x.x.xxxxXXXX"][ph]
            h=["x.x.x.x.x.x.x.x.","x.x.x.x.x.x.x.x.","X.x.X.x.X.x.X.x.","xxxxxxxxxxxxxxxx"][ph]
            if ph==3 and si<5: sn="o.o.x.x.xxxXX..."; h="xxxxxxxxxx......"; tm="..........xxX..." # 1回目: 最後の1拍を空ける＝サビへの「ため」
            if ph==3 and si>=5: tm="........xx..xXXX"
            if ph==0: cr="R:4"
        elif sec=="chorus":
            kp=["X.....x.X.x...x.","X..x..x.X.x.x...","X.x...x.X.x...x.","X.....xxX..x..x."]
            k=kp[(ph+cn)%4]
            sn=rnd.choice(["....X.......X...","....X.o.....X...","....X.......X.o."])
            if cn==0: h=rnd.choice(["X.x.X.x.X.x.X.x.","X.x.X.o.X.x.X.x."])
            else: h=rnd.choice(["X.O.x.O.X.x.O.x.","X.x.O.x.X.O.x.O."]) if cn>=2 else "X.x.X.x.X.x.X.x."
            if ph==3 and not last:   # 4小節ごとの「息継ぎ」: 後半のキックとハットを抜いて間をつくる
                k="X.......X......."; h="X.x.x.x........."; sn="....X.......X..."
            if cn>=1 and ph>=2 and not last:
                ride="D2"; h="................"
            if i%2==0: cr="g:X..............." if (i==0 or cn>=2) else "R:4"
            if cn==3 and ph==1: cr="g:X..............."
            if i==n-1 or (n>=8 and i==3 and False):
                fl=rnd.choice([("....X...x.x.xXXX","............xxXX"),("....X.....x.xxXX","........xxXXxxXX"),("....X..oX.x.XxXX","..........xxxXXX")])
                sn,tm=fl; k="X.......X.x....."
                if cn==3: k="X.x.X.x.X.X.XXXX"; cr="R:4"
            if cn==3 and last and b==len(bars)-5: pass
        elif sec=="inter":
            k=rnd.choice(["X.....x.X.......","X.......X..x...."]); h="x.x.x.x.x.x.x.x."; sn="....X.......X..."
            if i>=2: ride="D2"; h="................"
            if last: sn="....X...x.x.xXXX"; tm="............xxXX"
        elif sec=="solo":
            if i<4:  # 前半は軽く（ライド＋リムショットふうのゴースト）
                k=["X.......X.......","X.....o.X.......","X.......X..o....","X.......X.......".replace("X.......X","X..o....X")][ph]; sn="....o.......X..." if ph%2==0 else "....X.......o..."
                ride="D2"
            else:    # 後半はキックを増やし、ハットもしくはライドで押す
                k=rnd.choice(["X.x...x.X.x...x.","X.x.x...X.x.x...","X..xX.x.X.x.X.x."]); sn="....X.......X..."
                h=rnd.choice(["X.O.x.O.X.x.O.x.","X.x.x.x.X.x.x.x."])
                if ph==3: sn="....X...x.xoxXXX"; tm="........xx..xXXX"
            if i==0: cr="g:X..............."
            if last: sn="x.x.x.x.xxxxXXXX"; tm="........xxxxXXXX"; h="................"; ride=None
        elif sec=="bridge":
            if ph<2:   # 低いタムと、ライドのカップだけ。キックもスネアも抜く
                k="X..............." if ph==0 else "................"; sn="................"
                tm="X.......x.....x." if ph==0 else "........X.......x"; ride="F2"
            elif ph==2: k="X.......X..........".replace("..........","........")[:16]; sn="........X......."; ride="D2"; h="................"
            else: k="X.......X.x.X.x."; sn="o.o.x.x.xxxxXXXX"; tm="......xx..xxxXXX"
        else:  # outro
            k=rnd.choice(["X.....x.X.x...x.","X..x..x.X.x.x..."]); h="X.O.x.O.X.x.O.x."; sn="....X.......X..."
            if i==0: cr="g:X..............."
            if i==n-2: k="X.......X......."; sn="........X......."; h="X...x...x......."
            if last: k=sn="g:X..............."; h="R:4"; cr="g:X..............."
        for a,v in ((K,k),(S,sn),(H,h)): a.append(v if v.startswith(("g:","R:")) else "g:"+v)
        C.append(cr)
        if tm:
            hits=[j for j,ch in enumerate(tm) if ch in "xX"]; pit=["C4","A3","G3","E3","C3","A2"]
            if sec=="bridge": pit=["A2","C3","A2","E3","C3","A2"]
            toks=[]; kk=0
            for j,ch in enumerate(tm):
                if ch in "xX": toks.append(pit[min(len(pit)-1,kk*len(pit)//max(1,len(hits)))]+":0.25"+("!" if ch=="X" else "")); kk+=1
                else: toks.append("R:0.25")
            T.append(" ".join(toks))
        else: T.append("R:4")
        if ride:
            rc=ride
            if sec=="bridge": R.append("F2:1 R:1 F2:1 R:1")  # カップを2拍ごとに、長く鳴らす
            else: R.append(" ".join([("F2:0.5" if (ph==2 and j==0) else rc+":0.5") for j in range(8)]))
        else: R.append("R:4")
        G.append(arc_level(sec,si,i,n,cn))
    return K,S,H,C,T,R,G
_k,_s,_h,_c,_t,_r,ARC=varied_drums()
P["kick"],P["snare"],P["hat"],P["crash"],P["tom"],P["ride"]=_k,_s,_h,_c,_t,_r
KIND={"intro":"intro","verse":"verse","pre":"pre","chorus":"chorus","inter":"interlude","solo":"solo","bridge":"bridge","outro":"outro"}
sections=[{"kind":KIND[s],"bars":n} for s,n in SEC]
sections[11]["from"]="stopBeat"  # 2つ目のサビの前で一瞬止める
sections[11]["crash"]=True
def part(inst,role,vol,pan,key,**kw):
    d={"instrument":inst,"role":role,"volume":vol,"pan":pan,"notes":" ".join(P[key])}; d.update(kw); return d
OCT={"gain":1,"octave":-1}
song={"title":"まぶしい夏の入口 v4（ロック）","description":"（見本・仮）夏を感じる明るいロック。A長調・bpm160・8ビート。ギターは和音のストロークだけ（単音は弾かない）。メロディはトランペット、ソロとアルペジオはピアノ（録音音源）。","bpm":160,"beats":4,"chords":" ".join(chords),"barsPerChord":1,"repeats":1,"autoAccompaniment":False,"feel":"rock","tone":"rock","human":0.2,"dynamics":"natural","instrumentCheck":False,"sections":sections,
"parts":[
 part("kick","キック",0.22,0,"kick"),part("snare","スネア",0.18,0,"snare"),part("hihat","ハイハット",0.07,0,"hat"),part("tom","タム（ハイ〜フロア）",0.2,0.0,"tom"),part("crash","ライドシンバル",0.07,0.15,"ride"),part("crash","クラッシュ",0.09,0,"crash"),
 part("bass","ベース（根音の8分）",0.18,0,"bass"),
 {"instrument":"guitar","role":"歪みギターL（8分刻み）","volume":0.17,"pan":-0.7,"amp":"loudrock","notes":"","strum":{"pattern":"D.DDD.DD","spreadMs":9,"strings":4},"sections":{"intro":0,"verse":0.8,"pre":0.9,"interlude":0.8,"chorus":1,"solo":0.9,"bridge":0.6,"outro":1}},
 {"instrument":"guitar","role":"歪みギターR（8分刻み）","volume":0.17,"pan":0.7,"amp":"loudrock","notes":"","strum":{"pattern":"D.DDD.DD","spreadMs":11,"strings":4},"sections":{"intro":0,"verse":0.8,"pre":0.9,"interlude":0.8,"chorus":1,"solo":0.9,"bridge":0.6,"outro":1}},
 {"instrument":"guitar","role":"クリーンのストローク（きらめき）","volume":0.1,"pan":0,"amp":"crystal","chorus":0,"reverb":0.25,"notes":"","strum":{"pattern":"D.DU.UDU","spreadMs":14,"strings":5},"sections":{"intro":1,"verse":0.5,"pre":0,"interlude":1,"chorus":0.5,"solo":0,"bridge":1,"outro":0}},
 {"instrument":"brass","patch":"trumpet","role":"メロディ（トランペット）","volume":0.22,"pan":0.05,"reverb":0.3,"breath":True,"notes":" ".join(P["lead"]),"fx":[{"type":"delay","beats":0.75,"mix":0.12,"feedback":0.25}],"sections":{"intro":OCT,"verse":1,"pre":1,"interlude":OCT,"chorus":OCT,"solo":0,"bridge":OCT,"outro":OCT}},
 {"instrument":"piano","role":"ソロ（ピアノ）","volume":0.2,"pan":0.1,"reverb":0.25,"notes":" ".join(P["lead"]),"sections":{"intro":0,"verse":0,"pre":0,"interlude":0,"chorus":0,"solo":1,"bridge":0,"outro":0}},
 {"instrument":"piano","role":"ピアノのアルペジオ","volume":0.08,"pan":-0.2,"reverb":0.3,"notes":" ".join(P["arp"]),"sections":{"intro":1,"verse":0,"pre":0,"interlude":1,"chorus":0,"solo":0,"bridge":1,"outro":0}},
 part("brass","ブラスの合いの手（Aメロ・アウトロだけ）",0.08,0.3,"brass",patch="brassSection",reverb=0.25,sections={"intro":0,"verse":0.6,"pre":0,"interlude":0,"chorus":0,"solo":0,"bridge":0,"outro":1})]}
ARCR=[round(x,3) for x in ARC]
SOFT=[round(0.82+0.18*x,3) for x in ARC]
for p in song["parts"]:
    ins=p["instrument"]
    if ins in("kick","snare","hihat","crash","tom") or p["role"]=="ライドシンバル": p["barGain"]=ARCR
    else: p["barGain"]=SOFT
    if p["role"]=="スネア": p["push"]=0.025
    if p["role"]=="ハイハット": p["push"]=-0.008
    if "タム" in p["role"]: p["push"]=0.01
    if p["role"].startswith("歪みギターR"): p["push"]=0.006
song["human"]=0.35
json.dump(song,open(sys.argv[1],"w"),ensure_ascii=False,indent=1)
print("ok",len(song["parts"]))
