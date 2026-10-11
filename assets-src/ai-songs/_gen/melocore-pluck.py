# メロコアパンクの見本（pluck-deepair の音で）。使い方: python3 melocore-pluck.py > ../melocore-pluck.json
import json
A,E,F,D="A","E","F#m","D"
prog=[A,E,F,D]
# セクション: (名前, 小節数, 和音, リードの音)
intro="A5:1 C#6:1 B5:1 A5:1 G#5:1 B5:1 E6:2 F#5:1 A5:1 C#6:1 A5:1 F#5:1 A5:1 D6:2"
verse1="R:1 A4:0.5 B4:0.5 C#5:1 B4:1 R:1 B4:0.5 C#5:0.5 E5:1 C#5:1 A4:1 C#5:1 F#5:1 E5:1 D5:1 A4:1 D5:2"
verse2="R:1 A4:0.5 B4:0.5 C#5:1 B4:1 R:1 B4:0.5 C#5:0.5 E5:1 G#5:1 F#5:1 E5:1 C#5:1 A4:1 D5:1 F#5:1 A5:2~"
chorus_prog=[F,D,A,E]*2
chorus="C#5:1 E5:1 F#5:2~ D5:1 F#5:1 A5:2~ E5:1 A5:1 C#6:2~ B5:1 G#5:1 E5:2 C#5:0.5 E5:0.5 F#5:1 A5:1 F#5:1 D5:0.5 F#5:0.5 A5:1 B5:2 C#6:1 B5:0.5 A5:0.5 E5:2 G#5:1 B5:1 E6:2~"
chorus3="E5:1 F#5:1 A5:2~ F#5:1 A5:1 D6:2~ C#6:1 A5:1 E6:2~ D6:1 B5:1 G#5:2 "+chorus.split(" ",16)[16] if False else "E5:1 F#5:1 A5:2~ F#5:1 A5:1 D6:2~ C#6:1 A5:1 E6:2~ D6:1 B5:1 G#5:2 C#5:0.5 E5:0.5 F#5:1 A5:1 F#5:1 D5:0.5 F#5:0.5 A5:1 B5:2 C#6:1 B5:0.5 A5:0.5 E5:2 G#5:1 B5:1 E6:2~"
solo=("C#6:0.5 E6:0.5 C#6:0.5 A5:0.5 C#6:1 E6:1 "
 "B5:0.5 G#5:0.5 B5:0.5 E6:0.5 D6:1 B5:1 "
 "F#5:0.25 A5:0.25 C#6:0.25 A5:0.25 F#5:0.25 A5:0.25 C#6:0.25 E6:0.25 D6:1 C#6:1 "
 "D6:0.5 A5:0.5 F#5:0.5 A5:0.5 D6:2~ "
 "A5:0.25 C#6:0.25 E6:0.25 C#6:0.25 A5:0.25 C#6:0.25 E6:0.25 C#6:0.25 A5:0.25 C#6:0.25 E6:0.25 C#6:0.25 A5:0.25 C#6:0.25 E6:0.25 C#6:0.25 "
 "G#5:0.25 B5:0.25 E6:0.25 B5:0.25 G#5:0.25 B5:0.25 E6:0.25 B5:0.25 E6:1 D6:0.5 B5:0.5 "
 "C#6:0.5 E6:0.5 C#6:0.5 A5:0.5 F#5:0.5 A5:0.5 C#6:0.5 E6:0.5 "
 "E6:2^~ D6:1 A5:1")
outro="C#6:1 B5:1 A5:2 G#5:2 B5:2 A5:4~ R:4"
secs=[("intro",prog,intro),("verse",prog*2,verse1),("chorus",chorus_prog,chorus),
      ("verse",prog*2,verse2),("chorus",chorus_prog,chorus),("solo",prog*2,solo),
      ("chorus",chorus_prog,chorus3),("outro",[A,E,A,A],outro)]
root={A:("A2","A1"),E:("E3","E2"),F:("F#2","F#1"),D:("D3","D2")}
fifth={A:"E3",E:"B3",F:"C#3",D:"A3"}
chords=[];lead=[];gl=[];gr=[];bass=[];kick=[];snare=[];hat=[]
for name,ch,ld in secs:
    chords+=ch; lead.append(ld)
    n=len(ch)
    for i,c in enumerate(ch):
        gl.append(" ".join([f"{root[c][0]}:0.5"]*8))
        gr.append(" ".join([f"{fifth[c]}:0.5"]*8))
        bass.append(" ".join([f"{root[c][1]}:0.5"]*8))
        last=(i==n-1)
        fill=last and name in("verse","chorus","solo") 
        end=(name=="outro" and i==n-1)
        if end:
            kick.append("x:1 R:3"); snare.append("x:1 R:3"); hat.append("x:1 R:3"); continue
        kick.append("x:0.5 x:0.5 R:0.5 R:0.5 x:0.5 x:0.5 R:0.5 R:0.5")
        snare.append("R:1 x:1 R:1 x:0.25 x:0.25 x:0.25 x:0.25" if fill else "R:1 x:1 R:1 x:1")
        hat.append(" ".join(["x:0.5"]*8))
# 末尾の小節（outro 最終）はギターも1音で止める
gl[-1]="A2:1 R:3"; gr[-1]="E3:1 R:3"; bass[-1]="A1:1 R:3"
def part(inst,role,notes,vol,pan,patch=None,amp="auto",extra=None):
    d={"instrument":inst,"role":role,"volume":vol,"pan":pan,"amp":amp,"notes":" ".join(notes)}
    if patch: d["patch"]=patch
    if extra: d.update(extra)
    return d
song={"title":"melocore-pluck","description":"メロコアパンク。ギターは弦モデル（pluck-deepair）のクリーンで、パワーコードを8分で刻む",
 "bpm":186,"beats":4,"chords":" ".join(chords),"barsPerChord":1,"repeats":1,"feel":"rock","tone":"rock",
 "autoAccompaniment":False,"dynamics":"natural","human":0.25,
 "parts":[
  part("leadGuitar","リフ（左・ルート）",gl,0.2,-0.8,"cleanGuitar","clean",{"reverb":0.08,"chorus":0}),
  part("leadGuitar","リフ（右・5度）",gr,0.2,0.8,"cleanGuitar","clean",{"reverb":0.08,"chorus":0}),
  part("leadGuitar","メロディ／ソロ",lead,0.3,0,"cleanGuitar","clean",{"reverb":0.18,"chorus":0}),
  part("bass","ベース",bass,0.2,0),
  part("kick","キック",kick,0.22,0),part("snare","スネア",snare,0.18,0),part("hihat","ハイハット",hat,0.08,0.3)]}
print(json.dumps(song,ensure_ascii=False))
