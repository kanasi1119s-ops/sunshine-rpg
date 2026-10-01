exec(open('assets-src/ai-songs/gen/gen.py').read())
S=['intro','verse','verse','pre','chorus','verse','pre','chorus','break','solo','pre','chorus','chorus','outro']
gtr_root=['E2','E2','C3','D3','E2','E2','G2','D3']
bas_root=['E1','E1','C2','D2','E1','E1','G1','D2']
def r(note,pat):
    return ' '.join(f'{note}:{x}' for x in pat.split())
gallop="0.25 0.25 0.5 0.25 0.25 0.5 0.5 0.5 1"
chug8="0.5 0.5 0.5 0.5 0.5 0.5 0.5 0.5"
open_="1 0.5 0.5 1 1"
chunk="0.75 0.75 0.5 0.75 0.75 0.5"
def gl(pat): return seq(*[bar(r(n,pat)) for n in gtr_root])
def bl(pat): return seq(*[bar(r(n,pat)) for n in bas_root])
gtr={'verse':gl(gallop),'pre':gl(chug8),'chorus':gl(open_),'break':gl(chunk),'solo':gl(chug8)}
bas={k:bl(chug8) for k in['verse','pre','solo']}; bas['chorus']=bl(open_); bas['break']=bl(chunk); bas['outro']=bl("2 2"); bas['intro']=bl("2 2")
def eight(b,last=None): return gbars(*([b]*7+[last or b]))
Z="................"
kick={'intro':eight("X.......X......."),'outro':eight("X.......X......."),
 'verse':eight("Xx.xXx.xXx.xXx.x"),'pre':eight("X...X...X...X...","XxXxXxXxXxXxXxXx"),'chorus':eight("XxXxXxXxXxXxXxXx"),
 'break':eight("X..x..X..x..X..."),'solo':eight("XxXxXxXxXxXxXxXx")}
snare={'intro':eight("........X......."),
 'verse':eight("....X.......X..."),'pre':eight("....X.......X...","xxxxxxxxxxxxxxxx"),'chorus':eight("...oX..o...oX..o"),
 'break':eight("........X.......","....X.X.X.X.XXXX"),'solo':eight("....X.......X...")}
hat={'verse':eight("x.x.x.x.x.x.x.x."),'pre':eight("x.x.x.x.x.x.x.x."),'intro':eight("x...x...x...x..."),'outro':eight("x...x...x...x...")}
crash={'chorus':gbars("X...............",*[Z]*3,"X...............",*[Z]*2,"X..............."),'solo':gbars("X...............",*[Z]*7),'break':gbars("X...............",*[Z]*7),'pre':gbars(*[Z]*7,"X...............")}
strings_=seq(*[bar(f"{n}:4") for n in ['E3','E3','C3','D3','E3','E3','G3','D3']])
chorusmel=seq(bar("E5:1 G5:1 B5:2"),bar("A5:1 G5:1 E5:2"),bar("G5:1 E5:1 C5:1 E5:1"),bar("F#5:2 A5:2"),bar("B5:1 G5:1 E5:2"),bar("G5:1 A5:1 B5:2"),bar("D6:1 B5:1 G5:2"),bar("A5:2 F#5:1 D5:1"))
premel=seq(*[bar(f"{n}:4") for n in ['B4','B4','A4','A4','G4','G4','F#4','B4']])
solo=seq(bar("E5:0.25 G5:0.25 A5:0.25 B5:0.25 D6:0.5 B5:0.5 A5:0.5 G5:0.5 E5:1"),bar("G5:0.5 A5:0.5 B5:1 D6:1 E6:1"),bar("E5:0.25 G5:0.25 C6:0.5 B5:0.5 G5:0.5 E5:1 G5:1"),bar("A5:0.5 F#5:0.5 D5:1 F#5:1 A5:1"),
 bar("E5:0.25 G5:0.25 A5:0.25 B5:0.25 D6:0.5 B5:0.5 A5:0.5 G5:0.5 E5:1"),bar("B5:0.25 D6:0.25 E6:0.5 D6:0.5 B5:0.5 A5:0.5 G5:0.5 E5:1"),bar("D6:1 B5:1 G5:1 B5:1"),bar("A5:2 R:0.5 F#5:0.5 D5:1"))
breakmel=seq(*[bar(f"{n}:4") for n in ['E4','E4','E4','E4','E4','E4','B3','B3']])
lead={'pre':premel,'chorus':chorusmel,'solo':solo,'break':breakmel,'outro':seq(bar("E5:4"),*[bar("R:4")]*7)}
choir=seq(*[bar(f"{n}:4") for n in ['E4','E4','E4','F#4','G4','G4','B4','A4']])
parts=[
 P("distGuitar","刻み（左）",0.085,-0.9,"loudmetal",gtr),P("distGuitar","刻み（右）",0.085,0.9,"loudmetal",gtr),
 P("bass","ベース",0.17,0,"auto",bas),
 D("kick","キック",0.2,0,kick),D("snare","スネア",0.15,0,snare,push=0.02),D("hihat","ハイハット",0.06,0.3,hat,push=-0.01),D("crash","クラッシュ",0.07,-0.3,crash),
 P("leadGuitar","リード",0.12,0.1,"loudrock",lead),
 P("strings","弦",0.11,-0.5,"auto",{k:strings_ for k in['intro','verse','pre','chorus','break','outro']}),
 P("choir","合唱",0.09,0.4,"auto",{'chorus':choir})]
for _p in parts: _p['volume']=round(_p['volume']*0.4,4)  # 全パートの合計音量が大きいと、出口のリミッターが働きすぎて詰まる（crest 7.6→9.4dB）
build('assets-src/ai-songs/boss-crimson-gate.json',dict(title="紅蓮の門（ボス戦）",description="ラウドメタルのボス戦曲。ギャロップのリフ、サビで開く和音、間奏のブレイクとソロ。最後は導入に戻ってループできる",bpm=150,chords="Em Em C D Em Em G D",feel="rock",tone="metal"),S,parts)
