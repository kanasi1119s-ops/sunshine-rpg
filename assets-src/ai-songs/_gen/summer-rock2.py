import json,sys
# 夏のロック v2: 人間の指摘（2026-10-14）「ギターの単音（メロディ・アルペジオ）は電子の音にしか聞こえない。コードをそのまま弾くのはよい。刻みの音の途切れ方が不自然」に合わせた作り直し。
#   - ギターは単音を弾かない。和音のストローク（strum）だけ。音は伸ばして自然に消える（ミュート・短い切りは使わない）
#   - メロディはトランペット（VSCO 録音）、ソロはグランドピアノ（Salamander 録音）、アルペジオもピアノ
src=open(__file__.replace("summer-rock2.py","summer-rock.py")).read().split("chords,P=build()")[0]
sys.argv=[sys.argv[0]]+sys.argv[1:]
exec(src)
chords,P=build()
KIND={"intro":"intro","verse":"verse","pre":"pre","chorus":"chorus","inter":"interlude","solo":"solo","bridge":"bridge","outro":"outro"}
sections=[{"kind":KIND[s],"bars":n} for s,n in SEC]
sections[11]["from"]="stopBeat"  # 2つ目のサビの前で一瞬止める
sections[11]["crash"]=True
def part(inst,role,vol,pan,key,**kw):
    d={"instrument":inst,"role":role,"volume":vol,"pan":pan,"notes":" ".join(P[key])}; d.update(kw); return d
OCT={"gain":1,"octave":-1}
song={"title":"まぶしい夏の入口 v2（ロック）","description":"（見本・仮）夏を感じる明るいロック。A長調・bpm148・8ビート。ギターは和音のストロークだけ（単音は弾かない）。メロディはトランペット、ソロとアルペジオはピアノ（録音音源）。","bpm":148,"beats":4,"chords":" ".join(chords),"barsPerChord":1,"repeats":1,"autoAccompaniment":False,"feel":"rock","tone":"rock","human":0.2,"dynamics":"natural","instrumentCheck":False,"sections":sections,
"parts":[
 part("kick","キック",0.14,0,"kick"),part("snare","スネア",0.1,0,"snare"),part("hihat","ハイハット",0.05,0,"hat"),part("crash","クラッシュ",0.06,0,"crash"),
 part("bass","ベース（根音の8分）",0.12,0,"bass"),
 {"instrument":"guitar","role":"クリーンのストローク","volume":0.13,"pan":-0.4,"amp":"crystal","chorus":0,"reverb":0.25,"notes":"","strum":{"pattern":"D.DU.UDU","spreadMs":14,"strings":5},"sections":{"intro":0,"verse":1,"pre":0.8,"interlude":0,"chorus":0.5,"solo":0.6,"bridge":1,"outro":0.8}},
 {"instrument":"crunch","role":"歪みのストローク","volume":0.1,"pan":0.45,"amp":"loudrock","notes":"","strum":{"pattern":"D.DUDUDU","spreadMs":10,"strings":5},"sections":{"intro":0,"verse":0,"pre":0.7,"interlude":0,"chorus":1,"solo":0.8,"bridge":0,"outro":1}},
 {"instrument":"brass","patch":"trumpet","role":"メロディ（トランペット）","volume":0.2,"pan":0.05,"reverb":0.3,"breath":True,"notes":" ".join(P["lead"]),"fx":[{"type":"delay","beats":0.75,"mix":0.12,"feedback":0.25}],"sections":{"intro":OCT,"verse":1,"pre":1,"interlude":OCT,"chorus":OCT,"solo":0,"bridge":OCT,"outro":OCT}},
 {"instrument":"piano","role":"ソロ（ピアノ）","volume":0.2,"pan":0.1,"reverb":0.25,"notes":" ".join(P["lead"]),"sections":{"intro":0,"verse":0,"pre":0,"interlude":0,"chorus":0,"solo":1,"bridge":0,"outro":0}},
 {"instrument":"piano","role":"ピアノのアルペジオ","volume":0.12,"pan":-0.2,"reverb":0.3,"notes":" ".join(P["arp"]),"sections":{"intro":1,"verse":0.7,"pre":0,"interlude":1,"chorus":0,"solo":0,"bridge":1,"outro":1}},
 part("brass","ブラスの合いの手",0.09,0.3,"brass",patch="brassSection",reverb=0.25)]}
json.dump(song,open(sys.argv[1],"w"),ensure_ascii=False,indent=1)
print("ok",len(song["parts"]))
