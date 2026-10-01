exec(open('assets-src/ai-songs/gen/gen.py').read())
S=['intro','A','A','B','A2','solo','B','A','outro']
Z="................"
def eight(b,last=None): return gbars(*([b]*7+[last or b]))
drone=seq(bar("D3:4"),bar("D3:4"),bar("D3:2 A3:2"),bar("D3:4"),bar("D3:4"),bar("D3:4"),bar("D3:2 Eb3:2"),bar("D3:4"))
koto_bars=["D4:0.5 F#4:0.5 A4:0.5 Bb4:0.5 A4:0.5 F#4:0.5 Eb4:0.5 D4:0.5","D4:0.5 Eb4:0.5 F#4:0.5 A4:0.5 C5:0.5 A4:0.5 F#4:0.5 Eb4:0.5","D4:0.5 F#4:0.5 A4:0.5 D5:0.5 C5:0.5 A4:0.5 F#4:0.5 D4:0.5","Eb4:0.5 F#4:0.5 A4:0.5 Bb4:0.5 A4:0.5 F#4:0.5 Eb4:0.5 D4:0.5"]
koto=seq(*[bar(koto_bars[i%4]) for i in range(8)])
shaku=seq(bar("A4:2 Bb4:1 A4:1"),bar("F#4:3 G4:1"),bar("A4:1 Bb4:1 C5:2"),bar("Bb4:2 A4:2"),bar("G4:1 F#4:1 Eb4:2"),bar("F#4:2 D4:2"),bar("Eb4:1 F#4:1 G4:2"),bar("D4:4"))
pan=seq(bar("D5:2 C5:1 Bb4:1"),bar("A4:2 Bb4:1 C5:1"),bar("D5:1 Eb5:1 F#5:2"),bar("Eb5:2 D5:2"),bar("C5:1 Bb4:1 A4:2"),bar("Bb4:2 C5:2"),bar("D5:2 Eb5:1 D5:1"),bar("D5:4"))
sA="D5:0.25 Eb5:0.25 F#5:0.25 G5:0.25 A5:0.5 G5:0.5 F#5:0.5 Eb5:0.5 D5:1"
sB="A5:0.5 Bb5:0.5 A5:0.5 G5:0.5 F#5:1 Eb5:1"
sC="C6:0.25 Bb5:0.25 A5:0.25 G5:0.25 F#5:0.5 G5:0.5 A5:2"
sD="Bb5:1 A5:1 G5:1 F#5:1"
solo=seq(bar(sA),bar(sB),bar(sC),bar(sD),bar(sA),bar(sC),bar(sB),bar("D5:4"))
harp=seq(*[bar("D3:0.5 A3:0.5 D4:0.5 F#4:0.5 A4:0.5 F#4:0.5 D4:0.5 A3:0.5") if i%2==0 else bar("Eb3:0.5 Bb3:0.5 Eb4:0.5 G4:0.5 Bb4:0.5 G4:0.5 Eb4:0.5 Bb3:0.5") for i in range(8)])
kal=seq(*[bar("D5:0.5 A5:0.5 F#5:0.5 A5:0.5 Eb5:0.5 A5:0.5 F#5:0.5 A5:0.5") for i in range(8)])
fiddle=pan
padl=seq(*[bar(f"{n}:4") for n in ['D3','D3','Eb3','D3','D3','G3','Eb3','D3']])
tomA=eight("X.....x.....x...","X.....x...x.x.xx")
tomB=eight("X..x..x.X..x.x..","X..x..x.xxxxXXXX")
tomS=eight("X.......o.......")
hat=eight("o.o.o.o.o.o.o.o.")
parts=[
 P("sitar","ドローン",0.07,0,"delicate",{k:drone for k in S}),
 P("koto","琴",0.1,-0.5,"delicate",{k:koto for k in['A','B','A2','solo']},sustain=2),
 P("shakuhachi","尺八",0.11,0.3,"delicate",{'A':shaku,'A2':shaku}),
 P("panflute","笛",0.1,0.3,"delicate",{'B':pan,'solo':solo}),
 P("fiddle","フィドル",0.05,-0.3,"delicate",{'B':fiddle}),
 P("harp","ハープ",0.09,-0.6,"delicate",{'A2':harp,'solo':harp},sustain=2),
 P("kalimba","カリンバ",0.07,0.6,"delicate",{k:kal for k in['intro','A','B','outro']},sustain=2),
 D("tom","太鼓",0.1,0,{'A':tomA,'A2':tomA,'B':tomB,'solo':tomB}),D("tom","小さな太鼓",0.05,0.4,{'intro':tomS,'outro':tomS}),
 D("hihat","シェイカー",0.04,0.5,{k:hat for k in['A','A2','B','solo']},push=-0.01),
 P("pad","パッド",0.05,0.8,"auto",{k:padl for k in S}),
]
build('assets-src/ai-songs/caravan-hijaz.json',dict(title="砂漠の隊商",description="中東風（ヒジャーズ音階）の民族音楽。シタールのドローンに、琴・尺八・笛・カリンバ・フィドルが重なる。最後は導入に戻ってループできる",bpm=96,chords="Dm Dm Eb Dm Dm Gm Eb Dm",feel="rock",tone="rock"),S,parts)
