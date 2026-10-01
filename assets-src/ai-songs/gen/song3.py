exec(open('assets-src/ai-songs/gen/gen.py').read())
S=['intro','build','drop','drop','break','build','drop','drop','bridge','build','drop','outro']
Z="................"
def eight(b,last=None): return gbars(*([b]*7+[last or b]))
roots=['A','A','F','F','C','C','G','G']
def bass_bar(n,o): return bar(' '.join([f"R:0.5 {n}{o}:0.5"]*4))
bass=seq(*[bass_bar(n,{'A':1,'F':1,'C':2,'G':1}[n]) for n in roots])
arp={'A':"A3:0.25 C4:0.25 E4:0.25 A4:0.25",'F':"F3:0.25 A3:0.25 C4:0.25 F4:0.25",'C':"C4:0.25 E4:0.25 G4:0.25 C5:0.25",'G':"G3:0.25 B3:0.25 D4:0.25 G4:0.25"}
keys=seq(*[bar(rep(arp[n],4)) for n in roots])
melody=seq(bar("A4:0.5 C5:0.5 E5:1 D5:0.5 C5:0.5 A4:1"),bar("A4:0.5 C5:0.5 E5:1 G5:1 E5:1"),bar("F4:0.5 A4:0.5 C5:1 B4:0.5 A4:0.5 F4:1"),bar("A4:1 C5:1 F5:2"),
 bar("G4:0.5 C5:0.5 E5:1 D5:0.5 C5:0.5 G4:1"),bar("E5:1 G5:1 C6:2"),bar("D5:0.5 G5:0.5 B5:1 A5:0.5 G5:0.5 D5:1"),bar("B4:1 D5:1 G5:1 R:1"))
bell=seq(bar("E6:2 C6:2"),bar("A5:4"),bar("C6:2 A5:2"),bar("F5:4"),bar("E6:2 G6:2"),bar("C6:4"),bar("D6:2 B5:2"),bar("G5:4"))
padn={'A':'A3','F':'F3','C':'C4','G':'G3'}
pad=seq(*[bar(f"{padn[n]}:4") for n in roots])
four="X...X...X...X..."
kick={'intro':eight(four),'outro':eight(four),'build':eight(four,Z),'drop':eight(four)}
clap={'build':eight("....X.......X...","xxxxxxxxxxxxxxxx"),'drop':eight("....X.......X...","....X.......XxXx")}
# 2回目以降のビルドは、前半もスネアを細かくして盛り上げる
hat={'intro':eight("..x...x...x...x."),'outro':eight("..x...x...x...x."),'build':eight("..x...x...x...x."),'drop':eight("..x...x...x...x."),'break':eight("o.o.o.o.o.o.o.o."),'bridge':eight("o...o...o...o...")}
crash={'drop':gbars("X...............",*[Z]*7)}
parts=[
 D("kick","キック",0.2,0,kick),D("snare","クラップ",0.13,0,clap),D("hihat","ハイハット",0.06,0.3,hat,push=-0.005),D("crash","クラッシュ",0.06,-0.3,crash),
 P("sub808","ベース",0.17,0,"auto",{k:bass for k in['build','drop']},sustain=0.7),
 P("lead","リード",0.1,0,"auto",{'drop':melody}),
 P("keys","アルペジオ",0.08,0.7,"auto",{k:keys for k in['build','drop','bridge']},sustain=0.6),
 P("bell","きらめき",0.05,-0.6,"auto",{k:bell for k in['intro','break','bridge','outro']},sustain=1.5),
 P("pad","パッド",0.05,0.8,"auto",{k:pad for k in['intro','break','build','bridge','drop','outro']}),
]
build('assets-src/ai-songs/neon-circuit.json',dict(title="ネオン回路",description="4つ打ちのダンス曲。ビルド→ドロップ→ブレイクをくり返し、最後は導入に戻ってループできる",bpm=126,chords="Am Am F F C C G G",feel="dance",tone="rock"),S,parts)
