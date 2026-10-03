"""フィールド（マップ）用キャラ 16×32・4方向×3コマの「型」（2026-10-03）。

王道のコマンドRPGのフィールドキャラに共通する作り（2頭身、大きな頭、1ドット幅の暗い外周、目は縦2ドットの点、
部位ごとに「地・影・光」の3段、光は左上から）を、文字の型で手描きしたもの。特定の作品のキャラクターの絵は写していない。

文字（役割）: O 外周・目／H h L 髪（地・影・光）／S s 肌／T t U 上着（地・影・光）／A a 目印（襟・袖口・帯・マント）／
B b 下（ズボン・スカート）／K k Y 靴（地・影・折り返し）／G g 金具（バックル・剣の柄）／M m N 金属（兜・盾のふち・刃）／D d 木（杖）／Q 杖の玉／W 白。'.' は透明。
色は field_sprite.py が、AIのデザイン画（または手で決めた色）から当てはめる。
髪型: spiky（とがった短髪）・short（ふつうの短髪）・long（長い髪）・hood（フード）
ひげ: beard=True（年配の人物）
飾り: decos=('band','cape','backsword','sword','shield','helmet','staff')（はちまき・マント・背中の剣・手に剣・盾・兜・杖）。服には、V字の襟・袖口・金のバックル・靴の折り返しが最初からつく
服: tunic（上着＋ズボン）・dress（ワンピース。下の色）・robe（ローブ。上着の色）
コマ: 0=立ち、1=画面の左の足を出す、2=右の足を出す（歩きは 0→1→0→2 または 1→0→2→0）。
"""
def M(half): return [r+r[::-1] for r in half]
E8="........"
# ---- 正面（下向き）の体: 頭は肌の丸、髪は上に重ねる ----
FRONT_TOP=M([E8,E8,E8,E8,E8,
"........", #5
"....OOOO", #6
"...OSSSS", #7
"..OSSSSS", #8
"..OSSSSS", #9
".OSSSSSS", #10
".OSSSSSS", #11
".OSSSSSS", #12
".OSSSSSS", #13
".OSSSESS", #14
".OSSSESS", #15
"..OSSSSS", #16
"..OOsSSS", #17
"....OOOs", #18
"..OOTTAA", #19
".OUTTTTA", #20
".OUOTTTT", #21
".OAOtTTT", #22
".OSOAAAG", #23
"..OOBBBB", #24
])
LEGS_F={ # 0=立ち 1=左足前（画面の左） 2=右足前
0:["...ObBBBBBBbO...","...ObBBOOBBbO...","...OKKKOOKKkO...","...OKKkOOKKkO...","....OOO..OOO....","................","................"],
1:["...ObBBBBBBbO...","...ObBBOOBBbO...","...ObBBOOKKkO...","...OKKKOOKKkO...","...OKKkO.OOO....","....OOO.........","................"],
2:["...ObBBBBBBbO...","...ObBBOOBBbO...","...OKKkOObBBO...","...OKKkOOKKkO...","....OOO.OKKkO...",".........OOO....","................"],
}
# ---- 後ろ（上向き）----
BACK_TOP=M([E8,E8,E8,E8,E8,"........","....OOOO","...OSSSS","..OSSSSS","..OSSSSS",".OSSSSSS",".OSSSSSS",".OSSSSSS",".OSSSSSS",".OSSSSSS",".OSSSSSS","..OSSSSS","..OOsSSS","....OOOs",
"..OOTTTT", #19
".OUTTTTT", #20
".OUOTTTT", #21
".OAOtTTT", #22
".OSOAAAA", #23
"..OOBBBB"]) #24
# ---- 横（右向き）。左向きは左右反転 ----
SIDE_TOP=[ "................"]*5+[
"................", #5
"......OOOO......", #6
".....OSSSSO.....", #7
"....OSSSSSSO....", #8
"....OSSSSSSO....", #9
"...OSSSSSSSSO...", #10
"...OSSSSSSSSO...", #11
"...OSSSSSSSSO...", #12
"...OSSSSSSSSO...", #13
"...OSSSSSSESO...", #14
"...OSSSSSSESO...", #15
"....OSSSSSSSO...", #16
"....OOsSSSSO....", #17
".....OOOssO.....", #18
".....OTTTTO.....", #19
"....OUTTTTtO....", #20
"....OUTTTTtO....", #21
"....OUUTTttO....", #22
"....OAAAAGaO....", #23
".....OBBBBO.....", #24
]
SIDE_ARM={0:[(23,8,'S')],1:[(22,10,'S'),(22,11,'O'),(21,10,'T')],2:[(23,5,'S'),(23,4,'O'),(22,5,'t')]}
LEGS_S={  # 歩幅は小さめ（前後に1〜2ドット）。大股にすると、小さなキャラではせかせかして見える
0:[".....ObBBbO.....",".....ObBBbO.....",".....OKKKKO.....",".....OKKKKKO....","......OOOOO.....","................","................"],
1:[".....ObBBBO.....","....ObBOObBO....","....OKKOOKKO....","....OKkOOKKKO...",".....OO..OOO....","................","................"],
2:[".....OBBbbO.....","....OBBOObbO....","....OKKOOkkO....","....OKKOOkkkO...",".....OO..OOO....","................","................"],
}
# 髪・頭のかぶり物（上に重ねる。'.'は重ねない）: 正面（左半分を書いて左右反転）・後ろ・横（右向き）
SP=["................"]
HAIR={
'spiky':{
'down':M([E8,E8,E8,".......O","...O..OL","..OHO.OL","..OHHOHL",".OHHHHHL",".OHHHHLL","OHHHHHHL","OHhHHHHH","OHhHHhHH","OhHhSHhH",".OhS....",".Oh.....",".O......"]+[E8]*16),
'up':M([E8,E8,E8,".......O","...O..OL","..OHO.OL","..OHHOHL",".OHHHHHL",".OHHHHLL","OHHHHHHL","OHHHHHHH","OHHHHHHH","OHHHHHHH",".OHHHHHH",".OhHHHHH",".OhhHHHH","..OhhhHH","..OOhhhh"]+[E8]*14),
'side':SP*4+[".....O..O.......","....OHO.OHO.....","...OHHHOHHLO....","..OHHHHHHHLLO...","..OHHHHHHHHHLO..",".OHHHHHHHHHHHO..",".OHHHHHHHHHhHO..",".OhHHHHHHHhShO..",".OhHHHHHh.......",".OhhHHHh........","..OhHHh.........","..OhhO..........","...OO..........."]+SP*15,
},
'short':{
'down':M([E8,E8,E8,E8,"....OOOO","...OHHLL","..OHHHLL",".OHHHHHL",".OHHHHHH",".OHHHHHH",".OHhHHHH",".OhHHhHH",".OhHhSHh",".Oh.....",E8,E8]+[E8]*16),
'up':M([E8,E8,E8,E8,"....OOOO","...OHHLL","..OHHHLL",".OHHHHHL",".OHHHHHH",".OHHHHHH",".OHHHHHH",".OHHHHHH",".OHHHHHH",".OHHHHHH",".OhHHHHH",".OhhHHHH","..OhhhHH","..OOhhhh"]+[E8]*14),
'side':SP*5+["......OOOO......","....OOHHLLO.....","...OHHHHHHLO....","..OHHHHHHHHHO...",".OHHHHHHHHHHHO..",".OHHHHHHHHHhHO..",".OhHHHHHHHhShO..",".OhHHHHHh.......",".OhhHHHh........","..OhHHh.........","..OhhO..........","...OO..........."]+SP*15,
},
'long':{
'down':M([E8,E8,E8,E8,"....OOOO","...OHHLL","..OHHHLL",".OHHHHHL",".OHHHHHH","OHHHHHHH","OHHHHHHH","OHhHHHHH","OHhHhSHh","OHhS....","OHh.....","OHh.....","OHh.....","OHhO....","OHhO....","OhhO....",".Ohh....",".OO....."]+[E8]*10),
'up':M([E8,E8,E8,E8,"....OOOO","...OHHLL","..OHHHLL",".OHHHHHL",".OHHHHHH"]+["OHHHHHHH"]*10+["OhHHHHHH",".OhhHHHH",".OhhhhHH","..OOOOOO"]+[E8]*9),
'side':SP*4+["......OOOO......","....OOHHLLO.....","...OHHHHHLLO....","..OHHHHHHHHLO...","..OHHHHHHHHHO...",".OHHHHHHHHHHHO..",".OHHHHHHHHHhHO..",".OHHHHHHHHhShO..",".OHHHHHHh.......",".OHHHHHh........",".OHHHHh.........",".OHHHHO.........",".OHHHhO.........",".OHHhO..........",".OHhhO..........",".OHhO...........",".OhhO...........","..OO............"]+SP*10,
},
'hood':{
'down':M([E8,E8,E8,E8,".....OOO","...OOTTU","..OTTTTU",".OTTTTTU",".OTTTTTT","OTTTTTTT","OTtOOOOO","OTtOhHHH","OTtOSSSS","OTtO....","OTtO....","OTtO....","OTtTO...","OTTtO...",".OTTO..."]+[E8]*13),
'up':M([E8,E8,E8,E8,".....OOO","...OOTTU","..OTTTTU",".OTTTTTU",".OTTTTTT"]+["OTTTTTTT"]*9+[".OtTTTTT"]+[E8]*13),
'side':SP*4+[".....OOOO.......","...OOTTTUO......","..OTTTTTTUO.....",".OTTTTTTTTUO....",".OTTTTTTTTTO....","OTTTTTTTTTTTO...","OTTTTTTOOOOOO...","OTTTTTOhHHH.....","OTTTTTO.........","OTTTTTO.........","OTTTTTO.........","OTTTTTO.........","OTTTTtO.........",".OTTttO.........","..OOtO.........."]+SP*13,
},
}
# ひげ（髪の色）。年配の人物に
BEARD={'down':M([E8]*16+["..OHHHHH","..OHHHHH","...OHHHH","....OHHH",".....OHH","......OO"]+[E8]*10),
       'side':SP*16+["........OHHHO...","........OHHHO...","........OHHO....",".........OHO....","..........O....."]+SP*11}
# 服の下（ローブ・ワンピース）: 24行目から下を置きかえる。X は塗る色（T=上着と同じ、B=下の色）
def robe_rows(dr,f,X):
    t={'T':'t','B':'b'}[X]
    if dr in ('down','up'):
        feet={0:".OOKKOOOOOOKKOO.",1:".OOKKOOOOOOOOO..",2:"..OOOOOOOOOKKOO."}[f]
        return ["..O"+X*10+"O..","..O"+X*10+"O..","..O"+X*10+"O..",".O"+X*12+"O.",".O"+X*11+t+"O.",feet,"................","................"]
    hem={0:"...OOKKOOKKOO...",1:"...OOOOOOKKKO...",2:"...OKKOOOOOOO..."}[f]
    return [".....O"+X*4+"O.....",".....O"+X*4+"O.....","....O"+X*5+t+"O....","....O"+X*5+t+"O....","...O"+X*7+t+"O...","...O"+X*7+t+"O...",hem,"................"]
def overlay(base,ov):
    g=[list(r) for r in base]
    for y,row in enumerate(ov):
        for x,ch in enumerate(row):
            if ch!='.': g[y][x]=ch
    return [''.join(r) for r in g]
SHADE={'H':'h','T':'t','S':'s','B':'b','K':'k','A':'a','U':'T'}
def light_left(g):
    """正面・後ろは左右対称に描いたので、右半分を影にする（光は左上から）。"""
    g=[list(r) for r in g]
    for y in range(32):
        for x in range(8,16):
            ch=g[y][x]
            if ch=='L': g[y][x]='H'
            elif ch=='U': g[y][x]='T'
            elif ch in SHADE and x+1<16 and g[y][x+1]=='O': g[y][x]=SHADE[ch]
    return [''.join(r) for r in g]
DECOS=('band','cape','backsword','sword','shield','helmet','staff')
def _decorate(g,view,decos):
    """飾り（view: down / up / side＝右向き）。g は文字の2次元リスト。"""
    H=set('HhL')
    if 'band' in decos:   # はちまき（額の高さの髪を目印の色に）
        y=11 if view!='up' else 10
        for x in range(16):
            if g[y][x] in H: g[y][x]='A'
    if 'cape' in decos:   # マント（目印の色）
        if view=='up':
            for y in range(20,28):
                for x in range(1,15):
                    if g[y][x] not in '.OHhL': g[y][x]='A' if x<8 else 'a'
            for y in range(24,28):
                if g[y][1]=='.': g[y][1]='O'
                if g[y][14]=='.': g[y][14]='O'
                if g[y][2] in '.': g[y][2]='A'
                if g[y][13] in '.': g[y][13]='a'
            for x in range(1,15):
                if g[28][x] in '.' and g[27][x] in 'Aa': g[28][x]='O'
        elif view=='down':
            for y in range(20,27):
                g[y][0]='O'; g[y][15]='O'; g[y][1]='A'; g[y][14]='a'
            g[27][1]='O'; g[27][14]='O'
            g[19][5]='G'; g[19][10]='G'
        else:
            for y in range(19,28):
                if g[y][3]=='.' or g[y][3]=='O': g[y][3]='a'
                if g[y][2]=='.': g[y][2]='O'
            g[28][3]='O'
    if 'backsword' in decos:  # 背中の剣（柄が肩の上に見える）
        if view=='down':
            for (y,x,ch) in ((15,14,'O'),(16,13,'O'),(16,14,'G'),(16,15,'O'),(17,14,'g'),(17,15,'O'),(18,14,'O')):
                if g[y][x] in '.O': g[y][x]=ch
        elif view=='up':
            for k in range(11):
                y,x=17+k,2+k
                if y<28 and x<15: g[y][x]='k'
            for (y,x,ch) in ((15,1,'O'),(15,2,'G'),(15,3,'O'),(16,1,'O'),(16,2,'g'),(16,3,'O'),(14,2,'O')):
                g[y][x]=ch
        else:
            for (y,x,ch) in ((15,2,'O'),(16,1,'O'),(16,2,'G'),(16,3,'O'),(17,2,'g'),(18,2,'O')):
                if g[y][x] in '.O': g[y][x]=ch
    if 'helmet' in decos:  # 兜（金属。ふちに金の帯）
        for y in range(0,6):
            for x in range(16):
                if g[y][x] in 'HhLO': g[y][x]='.'
        if view in ('down','up'):
            half=["....OOOO","...OMMNN","..OMMMMN",".OMMMMMM",".OMMMMMM",".OmMMMMM",".OmmmMMM",".OmGGGGG"]
            rows=[r+r[::-1] for r in half]
        else:
            rows=["......OOOO......","....OOMMNNO.....","...OMMMMMNNO....","..OMMMMMMMMNO...","..OMMMMMMMMMO...",".OmMMMMMMMMMMO..",".OmmMMMMMMMMMO..",".OGGGGGGGGGGGO.."]
        for k,row in enumerate(rows):
            for x,ch in enumerate(row):
                if ch!='.': g[4+k][x]=ch
    def stamp(pat,y0,x0):
        for k,row in enumerate(pat):
            for x,ch in enumerate(row):
                if ch not in ' .' and 0<=y0+k<32 and 0<=x0+x<16: g[y0+k][x0+x]=ch
    if 'staff' in decos:   # 杖（木の柄と、先に光る玉）
        col={'down':0,'up':15}.get(view,12)
        for y in range(13,29): g[y][col]='D' if y%3 else 'd'
        g[29][col]='O'; g[12][col]='O'; g[11][col]='Q'; g[10][col]='Q'; g[9][col]='O'
        if view=='side':
            g[10][col-1]='O'; g[11][col-1]='O'; g[10][col+1]='O'; g[11][col+1]='O'
    if 'sword' in decos:   # 手に持った剣（刃は下向き）
        if view in ('down','up'):
            c=1 if view=='down' else 14
            g[23][c]='G'; g[23][c-1 if c==1 else c+1]='O'
            for y in range(24,28): g[y][c]='N' if y<27 else 'M'
            g[28][c]='O'
        else:
            hand={0:(23,8),1:(22,10),2:(23,5)}
            # side の手の位置は SIDE_ARM と同じ。手から前へ斜め下に刃を出す
            hy,hx=hand.get(getattr(_decorate,'frame',0),(23,8))
            for k in range(1,5):
                if hy+k<32 and hx+k<16: g[hy+k][hx+k]='N' if k<4 else 'O'
            if hx+1<16: g[hy][hx+1]='G'
    if 'shield' in decos:  # 盾（目印の色に金の十字、金属のふち）
        if view=='down':
            stamp([" OOO ","OMMMO","OAGAO","OGGGO","OAGAO","OAGaO","OAaaO"," OaO ","  O  "],18,11)
        elif view=='up':
            stamp([" OOO ","OmmmO","OMmmO","OMmmO","OMmmO","OmmmO","OmmmO"," OmO ","  O  "],18,0)
        else:
            stamp([" OO ","OMMO","OAGO","OGGO","OAGO","OAaO"," OO "],19,10)
    return g
def _boot_cuffs(g):
    """靴の一番上の段を明るく（折り返し）。"""
    for x in range(16):
        for y in range(25,31):
            if g[y][x] in 'Kk':
                g[y][x]='Y'; break
    return g
def frame(dr,f,style='spiky',outfit='tunic',beard=False,decos=()):
    if dr=='down': g=FRONT_TOP+LEGS_F[f]; g=overlay(g,HAIR[style]['down'])
    elif dr=='up': g=BACK_TOP+LEGS_F[f]; g=overlay(g,HAIR[style]['up'])
    else:
        g=SIDE_TOP+LEGS_S[f]; g=overlay(g,HAIR[style]['side'])
        g=[list(r) for r in g]
        for (y,x,ch) in SIDE_ARM[f]: g[y][x]=ch
        g=[''.join(r) for r in g]
    side=dr in ('left','right')
    if outfit in ('robe','dress'):
        X='T' if outfit=='robe' else 'B'
        rr=robe_rows('side' if side else 'down',f,X)
        g=g[:24]+rr
    if beard and dr!='up':
        g=overlay(g,BEARD['side' if side else 'down'])
    g=[list(r) for r in g]
    if outfit=='tunic': g=_boot_cuffs(g)
    _decorate.frame=f
    g=_decorate(g,'side' if side else dr,decos)
    g=[''.join(r) for r in g]
    if dr=='left': g=[r[::-1] for r in g]
    if dr in ('down','up'): g=light_left(g)
    assert len(g)==32 and all(len(r)==16 for r in g),(dr,f,[len(r) for r in g])
    return g

def all_frames(style='spiky', outfit='tunic', beard=False, decos=()):
    """{"down0": [...32行], ...} の12コマ。decos: band（はちまき）・cape（マント）・backsword（背中の剣）・sword（手に剣）・shield（盾）・helmet（兜）・staff（杖）"""
    return {f"{d}{f}": frame(d, f, style, outfit, beard, decos) for d in ('down', 'up', 'left', 'right') for f in (0, 1, 2)}
