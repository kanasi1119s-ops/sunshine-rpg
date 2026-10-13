import json,sys
# 夏のロック v3: 人間の指摘「ロック感が全くない」→ 歪みギターを主役に左右で重ね、ドラム・ベースを前に出し、全体を押し出す。
# （v2の注記） 人間の指摘（2026-10-14）「ギターの単音（メロディ・アルペジオ）は電子の音にしか聞こえない。コードをそのまま弾くのはよい。刻みの音の途切れ方が不自然」に合わせた作り直し。
#   - ギターは単音を弾かない。和音のストローク（strum）だけ。音は伸ばして自然に消える（ミュート・短い切りは使わない）
#   - メロディはトランペット（VSCO 録音）、ソロはグランドピアノ（Salamander 録音）、アルペジオもピアノ
src=open(__file__.replace("summer-rock3.py","summer-rock.py")).read().split("chords,P=build()")[0]
sys.argv=[sys.argv[0]]+sys.argv[1:]
exec(src)
chords,P=build()

# ── ドラムを毎小節ちがう形に（人間の指摘「ドラムが毎回単調」2026-10-14）──
import random
def varied_drums():
    K,S,H,C,T=[],[],[],[],[]
    ncho=0
    for b,(sec,c,i,n) in enumerate(bars):
        rnd=random.Random(1000+b*7+i)
        si=SECI[b]; cn=sum(1 for q in SEC[:si] if q[0]=="chorus")  # 何回目のサビか
        last=(i==n-1); half=(n>=8 and i==3); ph=i%4
        k=s_="................"; h=k; cr="R:4"; tm=None
        sn="................"
        if sec=="intro":
            h="x...x...x...x..." if b>1 else "x...x...x.x.x.x."
            k="X.......X.......X.." if False else ("X.......X..o...." if b>=2 else "................")
            sn="................" if b<3 else ("....X.......X..." if last is False else "....x...x.x.xXXX")
            if last: tm="............xxXX"
        elif sec=="verse":
            kp=["X.....x...x.....","X.....x..x......","X......xx.x.....","X.....x...x...x."]
            k=kp[(ph+ (1 if si>5 else 0))%4]
            h=rnd.choice(["x.x.x.x.x.x.x.x.","x.xox.x.x.xox.x.","x.x.x.xox.x.x.xo"])
            sn=rnd.choice(["....X.......X...","....X.o.....X...","....X.......X..o","....X..o....X..."])
            if ph==3 and i%8==3 or last:
                sn=rnd.choice(["....X.......xxXX","....X.....x.xXXx","....X..o..o.xxXX"]); k="X.....x.X......."
            if si>5 and ph==1: sn=sn[:12]+"x.xo" if last else sn
            if i==0: cr="g:X..............."
        elif sec=="pre":
            ramp=[("....X.......X...","x.......x.......") , ("....X.......X.x.","x...x...x...x..."),("..x.X.x.X.x.X.x.","x.x.x.x.x.x.x.x."),("xxxxxxxxxxxxXXXX","xxxxxxxxxxxxxxxx")]
            sn,h=ramp[min(ph,3)] if n==4 else ramp[min(i//1,3)]
            h="x.x.x.x.x.x.x.x." if ph<3 else "xxxxxxxxxxxxxxxx"
            k="X.....x.X.....x." if ph<3 else "X...X...X..xX.xX"
            if ph==3: tm="........x.x.xxXX"
        elif sec=="chorus":
            kp=["X.....x.X.x...x.","X..x..x.X.x.x...","X.x...x.X.x...x.","X.....xxX..x..x."]
            k=kp[(ph+cn)%4]
            if cn>=2: h=rnd.choice(["O.x.O.x.O.x.O.x.","x.O.x.O.x.O.x.O.","x.x.O.x.x.x.O.x."])
            else: h=rnd.choice(["x.X.x.X.x.X.x.X.","x.X.x.X.x.X.xoX.","x.X.xoX.x.X.x.X."])
            sn=rnd.choice(["....X.......X...","....X.o.....X...","....X.......X.o."])
            if i%4==0: cr="g:X..............."
            if i==n-1 or (n>=8 and i==3):
                fl=rnd.choice([("....X...x.x.xXXX","............xxXX"),("....X.....x.xxXX","........xxXXxxXX"),("....X..oX.x.XxXX","..........xxxXXX")])
                sn,tm=fl
                k="X.......X.x....."
                if i==n-1: cr="R:4"
        elif sec=="inter":
            k=rnd.choice(["X.....x.X.......","X.......X..x...."]); h="x.x.x.x.x.x.x.x."; sn="....X.......X..."
            if last: sn="....X...x.x.xXXX"; tm="............xxXX"
        elif sec=="solo":
            k=rnd.choice(["X.x...x.X.x...x.","X.x.x...X.x.x...","X..xX.x.X.x.X.x."]); h=rnd.choice(["x.O.x.O.x.O.x.O.","x.x.x.x.x.x.x.x."]); sn=rnd.choice(["....X.......X...","....X.o...o.X..."])
            if ph==3: sn="....X...x.xoxXXX"; tm="........xx..xXXX"
            if i==0: cr="g:X..............."
            if last: sn="x.x.x.x.xxxxXXXX"; tm="........xxxxXXXX"
        elif sec=="bridge":
            k=["X...............","X.......X.......","X.....x.........","X.......X..x...."][ph]
            sn="........X......." if ph<3 else "........X.......".replace("X","x")
            h="x...x...x...x..." if ph<2 else "x.x.x.x.x.x.x.x."
            tm="............x.x." if ph==1 else ("..............xX" if last else None)
            if last: sn="........X..x.xXX"
        else: # outro
            k=rnd.choice(["X.....x.X.x...x.","X..x..x.X.x.x..."]); h="x.O.x.O.x.O.x.O."; sn="....X.......X..."
            if i==0: cr="g:X..............."
            if last: k=sn=h="g:X..............."; h="R:4"; cr="g:X..............."
        for a,v in ((K,k),(S,sn),(H,h)): a.append(v if v.startswith(("g:","R:")) else "g:"+v)
        C.append(cr); T.append("g:"+tm if tm else "R:4")
    return K,S,H,C,T
_k,_s,_h,_c,_t=varied_drums()
P["kick"],P["snare"],P["hat"],P["crash"],P["tom"]=_k,_s,_h,_c,_t
KIND={"intro":"intro","verse":"verse","pre":"pre","chorus":"chorus","inter":"interlude","solo":"solo","bridge":"bridge","outro":"outro"}
sections=[{"kind":KIND[s],"bars":n} for s,n in SEC]
sections[11]["from"]="stopBeat"  # 2つ目のサビの前で一瞬止める
sections[11]["crash"]=True
def part(inst,role,vol,pan,key,**kw):
    d={"instrument":inst,"role":role,"volume":vol,"pan":pan,"notes":" ".join(P[key])}; d.update(kw); return d
OCT={"gain":1,"octave":-1}
song={"title":"まぶしい夏の入口 v3（ロック）","description":"（見本・仮）夏を感じる明るいロック。A長調・bpm160・8ビート。ギターは和音のストロークだけ（単音は弾かない）。メロディはトランペット、ソロとアルペジオはピアノ（録音音源）。","bpm":160,"beats":4,"chords":" ".join(chords),"barsPerChord":1,"repeats":1,"autoAccompaniment":False,"feel":"rock","tone":"rock","human":0.2,"dynamics":"natural","instrumentCheck":False,"sections":sections,
"parts":[
 part("kick","キック",0.22,0,"kick"),part("snare","スネア",0.18,0,"snare"),part("hihat","ハイハット",0.07,0,"hat"),part("tom","タム（フィル）",0.16,0.0,"tom"),part("crash","クラッシュ",0.09,0,"crash"),
 part("bass","ベース（根音の8分）",0.18,0,"bass"),
 {"instrument":"guitar","role":"歪みギターL（8分刻み）","volume":0.17,"pan":-0.7,"amp":"loudrock","notes":"","strum":{"pattern":"D.DDD.DD","spreadMs":9,"strings":4},"sections":{"intro":0,"verse":0.8,"pre":0.9,"interlude":0.8,"chorus":1,"solo":0.9,"bridge":0.6,"outro":1}},
 {"instrument":"guitar","role":"歪みギターR（8分刻み）","volume":0.17,"pan":0.7,"amp":"loudrock","notes":"","strum":{"pattern":"D.DDD.DD","spreadMs":11,"strings":4},"sections":{"intro":0,"verse":0.8,"pre":0.9,"interlude":0.8,"chorus":1,"solo":0.9,"bridge":0.6,"outro":1}},
 {"instrument":"guitar","role":"クリーンのストローク（きらめき）","volume":0.1,"pan":0,"amp":"crystal","chorus":0,"reverb":0.25,"notes":"","strum":{"pattern":"D.DU.UDU","spreadMs":14,"strings":5},"sections":{"intro":1,"verse":0.5,"pre":0,"interlude":1,"chorus":0.5,"solo":0,"bridge":1,"outro":0}},
 {"instrument":"brass","patch":"trumpet","role":"メロディ（トランペット）","volume":0.22,"pan":0.05,"reverb":0.3,"breath":True,"notes":" ".join(P["lead"]),"fx":[{"type":"delay","beats":0.75,"mix":0.12,"feedback":0.25}],"sections":{"intro":OCT,"verse":1,"pre":1,"interlude":OCT,"chorus":OCT,"solo":0,"bridge":OCT,"outro":OCT}},
 {"instrument":"piano","role":"ソロ（ピアノ）","volume":0.2,"pan":0.1,"reverb":0.25,"notes":" ".join(P["lead"]),"sections":{"intro":0,"verse":0,"pre":0,"interlude":0,"chorus":0,"solo":1,"bridge":0,"outro":0}},
 {"instrument":"piano","role":"ピアノのアルペジオ","volume":0.08,"pan":-0.2,"reverb":0.3,"notes":" ".join(P["arp"]),"sections":{"intro":1,"verse":0,"pre":0,"interlude":1,"chorus":0,"solo":0,"bridge":1,"outro":0}},
 part("brass","ブラスの合いの手（Aメロ・アウトロだけ）",0.08,0.3,"brass",patch="brassSection",reverb=0.25,sections={"intro":0,"verse":0.6,"pre":0,"interlude":0,"chorus":0,"solo":0,"bridge":0,"outro":1})]}
json.dump(song,open(sys.argv[1],"w"),ensure_ascii=False,indent=1)
print("ok",len(song["parts"]))
