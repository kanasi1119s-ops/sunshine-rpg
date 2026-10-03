"""フィールド（マップ）用キャラ 16×32・4方向×3コマの「型」（2026-10-03）。

王道のコマンドRPGのフィールドキャラに共通する作り（2頭身、大きな頭、1ドット幅の暗い外周、目は縦2ドットの点、
部位ごとに「地・影・光」の3段、光は左上から）を、文字の型で手描きしたもの。特定の作品のキャラクターの絵は写していない。

文字（役割）: O 外周／E 目／P ほお／X 口／V ひざの光／H h L 髪（地・影・光）／S s 肌／T t U 上着（地・影・光）／A a 目印（襟・袖口・帯・マント）／
B b 下（ズボン・スカート）／K k Y 靴（地・影・折り返し）／G g 金具（バックル・剣の柄）／M m N 金属（兜・盾のふち・刃）／D d 木（杖）／Q 杖の玉／W 白。'.' は透明。
色は field_sprite.py が、AIのデザイン画（または手で決めた色）から当てはめる。
髪型: spiky（とがった短髪）・short（ふつうの短髪）・long（長い髪）・hood（フード）
ひげ: beard=True（年配の人物）
飾り: decos=('band','cape','backsword','sword','shield','helmet','staff','scarf','goggles','twintails','ponytail','circlet','bracelet','pickaxe')（はちまき・マント・背中の剣・手に剣・盾・兜・杖・マフラー・ゴーグル・ふたつ結び）。服には、V字の襟・袖口・金のバックル・靴の折り返しが最初からつく
服: tunic（上着＋ズボン）・coat（ひざまでの長い上着）・dress（ワンピース。下の色）・robe（ローブ。上着の色）
コマ: 0=立ち、1=画面の左の足を出す、2=右の足を出す（歩きは 0→1→0→2 または 1→0→2→0）。
歩きのコマでは、出した足と反対の腕が前に振れ（手が1ドット上がる）、もう一方の腕は後ろに振れる（手が1ドット下がる）。
物を持った手（剣・杖・ランタン・つるはし・盾）は振らない。髪の先（長い髪・ふたつ結び・ポニーテール・横向きの後ろ髪）と、
はちまきの端・マフラーの端・マントのすそも、歩きのコマで1ドット揺れる（人間の指示 2026-10-03）。
男性の人物は髪を揺らさない（hair_sway=False、field_sprite.py の --still-hair。人間の指示 2026-10-04）。布の揺れと腕の振りはそのまま。
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
DECOS=('backpick','lantern','bow','band','cape','backsword','sword','shield','helmet','staff','scarf','goggles','twintails')
def _decorate(g,view,decos):
    """飾り（view: down / up / side＝右向き）。g は文字の2次元リスト。"""
    H=set('HhL')
    f=getattr(_decorate,'frame',0); hf=getattr(_decorate,'hairf',f); armdy=getattr(_decorate,'armdy',{2:0,13:0})
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
            flare={0:99,1:24,2:26}[f]   # 歩くと、すそが後ろへ広がる
            for y in range(19,28):
                if g[y][3]=='.' or g[y][3]=='O': g[y][3]='a'
                if y>=flare:
                    g[y][2]='a'; g[y][1]='O'
                elif g[y][2]=='.': g[y][2]='O'
            g[28][3]='O'
            if f: g[28][2]='O'
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
    if 'twintails' in decos:   # 左右に結んだ髪。歩きのコマで房の先が上下に揺れる
        sides=(0,15) if view in ('down','up') else (0,)
        for x0 in sides:
            inner=1 if x0==0 else 14
            d=0 if hf==0 else ((-1 if x0==0 else 1) if hf==1 else (1 if x0==0 else -1))
            if view=='side': d=(-1 if hf==1 else 1) if hf else 0
            for y in range(11,20+d):
                g[y][x0]='O'; g[y][inner]='H' if x0==0 else 'h'
            g[20+d][inner]='O'; g[11][inner]='A'
    if 'scarf' in decos:       # 首に巻いた布（目印の色）。端が後ろへなびく
        if view in ('down','up'):
            for x in range(4,12): g[18][x]='A'
            g[18][3]='O'; g[18][12]='O'
            for x in range(3,13):
                if g[19][x] not in '.O': g[19][x]='a' if x>=10 else 'A'
            if view=='down':
                for y in (20,21): g[y][10]='a'
                g[22][10]='O'
        else:
            for x in range(5,11): g[18][x]='A'
            dy=-1 if f==1 else 0   # 歩くと端がはためく
            for (y,x) in ((19,4),(19,3),(20,3),(20,2),(21,2)): g[y+(dy if x<4 else 0)][x]='a'
            for (y,x) in ((18,3),(18,2),(19,2),(20,1),(21,1),(22,2)):
                if g[y+dy][x]=='.': g[y+dy][x]='O'
    if 'goggles' in decos:     # 額の上のゴーグル
        if view=='down':
            for (x,ch) in ((3,'G'),(4,'Q'),(5,'Q'),(6,'G'),(9,'G'),(10,'Q'),(11,'Q'),(12,'G')): g[9][x]=ch
            for x in (4,5,10,11): g[10][x]='G'
        elif view=='up':
            for x in range(2,14):
                if g[10][x] in 'HhL': g[10][x]='g'
        else:
            for (x,ch) in ((9,'G'),(10,'Q'),(11,'Q'),(12,'G')): g[9][x]=ch
            for x in range(3,9):
                if g[9][x] in 'HhL': g[9][x]='g'
    if 'ponytail' in decos:    # 後ろで結んだ髪
        if view=='up':   # 歩きのコマで、房の先（下の半分）が左右に揺れる
            for y in range(11,20):
                d=0 if (hf==0 or y<15) else (-1 if hf==1 else 1)
                for x in (7,8): g[y][x+d]='H' if x==7 else 'h'
                g[y][6+d]='O'; g[y][9+d]='O'
            d=0 if hf==0 else (-1 if hf==1 else 1)
            g[20][7+d]='O'; g[20][8+d]='O'; g[11][7]='A'; g[11][8]='A'
        elif view=='side':   # 後ろへなびく（コマ1は大きく、コマ2は小さく）
            for y in range(9,17):
                d=-1 if (hf==1 and y>=12) or (hf==2 and y>=14) else 0
                g[y][1+d]='O'; g[y][2+d]='H'
                if d: g[y][2]='O' if g[y][3] in 'SsO' else g[y][2]
            d=-1 if hf else 0
            g[17][2+d]='O'; g[9][2]='A'
        else:
            for x in (7,8): g[3][x]='H'
            g[2][7]='O'; g[2][8]='O'
    if 'circlet' in decos:     # 額の飾り（銀の輪と宝石）
        y=11 if view!='up' else 10
        for x in range(16):
            if g[y][x] in 'HhLD': g[y][x]='N'
        if view=='down': g[y][7]='A'; g[y][8]='A'
        elif view=='side': g[y][11]='A'
    if 'bracelet' in decos:    # 手首の光る腕輪
        if view=='down': g[22+armdy[13]][13]='Q'
        elif view=='up': g[22+armdy[2]][2]='Q'
        else:
            for y in range(19,25):
                for x in range(16):
                    if g[y][x]=='S' and y>=21: g[y][x]='Q'; break
    def px2(y,x,ch):
        if 0<=y<32 and 0<=x<16: g[y][x]=ch
    if 'band' in decos:        # はちまきの結び目と、なびく端
        if view=='down':
            for x in range(16):
                if g[12][x]=='A': g[12][x]='a'
        elif view=='up':
            ex=7+(0 if f==0 else (-1 if f==1 else 1))
            for (y,x,ch) in ((10,7,'a'),(10,8,'a'),(11,7,'A'),(12,ex,'A'),(11,8,'a')): px2(y,x,ch)   # 結び目と垂れた端（歩くと揺れる）
        else:
            dy=-1 if f==1 else 0   # 歩くと端がはためく
            for (y,x,ch) in ((11,1,'A'),(12,0,'A'),(12,1,'a'),(13,0,'a'),(10,1,'O'),(11,0,'O'),(14,0,'O'),(13,1,'O')): px2(y+dy,x,ch)
    if 'scarf' in decos and view=='down':   # マフラーのしわと房
        for x in (5,8,11):
            if g[19][x]=='A': g[19][x]='a'
        px2(22,9,'A'); px2(23,10,'a'); px2(23,9,'O'); px2(24,10,'O')
    if 'goggles' in decos and view in ('down','side'):   # レンズの光
        for x in ((4,10) if view=='down' else (10,)): px2(9,x,'W')
    if 'lantern' in decos:     # 手に下げたランタン（灯りが光る）
        pat=[" O ","OGO","OWO","OQO"," O "]
        x0={'down':0,'up':13}.get(view,10); y0=24 if view!='side' else 23
        for k,row in enumerate(pat):
            for j,ch in enumerate(row):
                if ch!=' ': px2(y0+k,x0+j,ch)
    if 'bow' in decos:         # 背中の弓（後ろ向きと横向きで見える。正面では肩の後ろと腰の横に先がのぞく）
        if view=='down':
            for (y,x) in ((14,14),(15,14),(16,15),(17,15),(18,15),(24,15),(25,15),(26,14),(27,14)):
                if g[y][x]=='.': g[y][x]='D'
            for (y,x) in ((13,14),(28,14)):
                if g[y][x]=='.': g[y][x]='O'
        if view=='up':
            for k in range(10): px2(13+k,3+(1 if 2<k<7 else 0),'D')
            for y in range(13,23): px2(y,6,'N')
        elif view=='side':
            for k in range(9): px2(14+k,2 if 2<k<6 else 3,'D')
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
    if 'helmet' in decos:      # ヘッドランプ（光る灯り）と鋲
        if view=='down':
            for (y,x,ch) in ((5,7,'G'),(5,8,'G'),(6,6,'G'),(6,7,'W'),(6,8,'Q'),(6,9,'G'),(7,7,'G'),(7,8,'G')): px2(y,x,ch)
            for x in (3,12): px2(9,x,'N')
        elif view=='side':
            for (y,x,ch) in ((6,11,'G'),(7,11,'W'),(7,12,'Q'),(8,11,'G')): px2(y,x,ch)
    def stamp(pat,y0,x0):
        for k,row in enumerate(pat):
            for x,ch in enumerate(row):
                if ch not in ' .' and 0<=y0+k<32 and 0<=x0+x<16: g[y0+k][x0+x]=ch
    if 'staff' in decos:   # 杖（木の柄と、先に光る玉。玉は中心が白く光る）。歩くと、持った手といっしょに上下する
        col={'down':1,'up':14}.get(view,12)
        sd={'down':armdy[2],'up':armdy[13]}.get(view,{0:0,1:-1,2:1}[f])
        for y in range(13+sd,29+sd): g[y][col]='D' if y%3 else 'd'
        px2(29+sd,col,'O')
        if sd<0: px2(29,col,'.')
        for (dy,dx,ch) in ((-5,0,'O'),(-4,-1,'O'),(-4,0,'Q'),(-4,1,'O'),(-3,-1,'Q'),(-3,0,'W'),(-3,1,'Q'),(-2,-1,'O'),(-2,0,'Q'),(-2,1,'O'),(-1,0,'O')):
            px2(13+sd+dy,col+dx,ch)
    if 'backpick' in decos:    # 背中に背負ったつるはし（柄は右肩から左の腰へ斜め。頭は右肩の上）
        def behind(y,x,ch):
            if 0<=y<32 and 0<=x<16 and g[y][x]=='.': g[y][x]=ch
        if view=='up':
            for k in range(12):
                y,x=13+k,12-k
                if 0<=x<16: g[y][x]='D' if k%3 else 'd'
            for (y,x) in ((11,11),(11,12),(11,13),(11,14),(12,14),(12,15),(10,11),(12,10)): px2(y,x,'M' if (x+y)%3 else 'm')
        elif view=='down':
            for (y,x) in ((13,14),(13,15),(14,15),(12,13),(12,14),(14,13),(15,13)): behind(y,x,'M' if (x+y)%3 else 'm')
            for (y,x) in ((25,1),(26,1)): behind(y,x,'D')
        else:   # 右向き: 背中（左）に柄、頭は肩の上
            for y in range(19,26): behind(y,2,'D' if y%3 else 'd')          # 柄（背中の後ろ）
            for (y,x,ch) in ((17,0,'O'),(17,1,'M'),(17,2,'M'),(17,3,'M'),(18,0,'m'),(18,1,'m'),(18,2,'M'),(16,1,'O'),(16,2,'O'),(16,3,'O'),(19,0,'O'),(19,1,'O')):
                behind(y,x,ch)                                               # 頭（背中から後ろへ突き出る）
    if 'pickaxe' in decos:     # 肩にかついだつるはし
        col={'down':1,'up':14}.get(view,3)
        for y in range(6,24): g[y][col]='D' if y%3 else 'd'
        hd={'down':[(5,0),(5,1),(5,2),(5,3),(6,0),(4,2),(4,3),(4,4),(3,4)],'up':[(5,15),(5,14),(5,13),(5,12),(6,15),(4,13),(4,12),(4,11),(3,11)],
            'side':[(6,0),(6,1),(6,2),(6,3),(6,4),(7,0),(5,4),(4,5)]}[view]
        if view=='side':
            for y in range(6,24): g[y][col]='D' if y%3 else 'd'
        for (y,x) in hd: g[y][x]='M' if (x+y)%3 else 'm'
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
def _details(g,view):
    """細部の描き込み（ほお・口・髪のすじ・肩の光・服のしわ・腰の袋・ズボンの縫い目・ひざと靴先の光）。型の上から重ねる。目は型のまま。"""
    def put(y,x,ch,only=None):
        if 0<=y<32 and 0<=x<16 and (only is None or g[y][x] in only): g[y][x]=ch
    if view=='down':
        put(16,3,'P','Ss'); put(16,12,'P','Ss')       # ほお
        put(17,7,'X','Ss'); put(17,8,'X','Ss')        # 口
        for (y,x) in ((7,4),(7,5)): put(y,x,'L','H')
        for (y,x) in ((20,3),(20,4)): put(y,x,'U','T')                     # 肩の光
        for (y,x) in ((21,5),(21,9),(22,6),(22,10)): put(y,x,'t','T')     # 服のしわ
        for (y,x) in ((20,6),(21,6)): put(y,x,'G','T')                     # ボタン
        put(24,4,'K','B'); put(24,5,'K','B'); put(25,4,'k','Bb')           # 腰の袋
        put(25,9,'V','B'); put(26,5,'V','B')                                # ひざの光
        for x in (5,10): put(28,x,'Y','Kk')                                 # 靴先の光
    elif view=='up':
        for (y,x) in ((7,4),(7,5),(8,4),(9,4),(8,6),(9,6),(10,6)): put(y,x,'L','H')   # 後ろ髪のつや（明るいすじ）
        for (y,x) in ((20,3),(20,4)): put(y,x,'U','T')
        for (y,x) in ((21,6),(21,9),(20,7),(22,7),(22,8)): put(y,x,'t','T')   # 背中のしわと縫い目
        put(24,10,'K','B'); put(24,11,'K','Bb'); put(25,11,'k','Bb')
        put(25,5,'V','B'); put(25,9,'V','B')
    else:
        put(16,9,'P','Ss'); put(16,11,'X','Ss')
        for (y,x) in ((6,6),(7,6)): put(y,x,'L','H')
        put(20,6,'U','T')
        for (y,x) in ((21,7),(22,8)): put(y,x,'t','T')
        put(24,5,'K','B'); put(25,5,'k','Bb')
        put(25,7,'V','B')
        for x in range(16):
            if g[28][x] in 'Kk' and (x+1>=16 or g[28][x+1] in '.O'): g[28][x]='Y'; break
    return g
def _boot_cuffs(g):
    """靴の一番上の段を明るく（折り返し）。"""
    for x in range(16):
        for y in range(25,31):
            if g[y][x] in 'Kk':
                g[y][x]='Y'; break
    return g
def _shift(ov,y0,y1,dx,xlo=0,xhi=16):
    """重ねる型（髪）の y0〜y1 行の xlo〜xhi の範囲を、横に dx ずらす（空いたところは透明）。"""
    ov=list(ov)
    for y in range(y0,min(y1,len(ov)-1)+1):
        r=list(ov[y]); seg=r[xlo:xhi]
        seg=(['.']*dx+seg[:len(seg)-dx]) if dx>0 else (seg[-dx:]+['.']*(-dx))
        r[xlo:xhi]=seg; ov[y]=''.join(r)
    return ov
def _hair_sway(ov,view,style,f):
    """歩きのコマで髪の先を1ドット揺らす。正面・後ろは、コマ1で左の房、コマ2で右の房が内側へ揺れる。横は後ろへなびく。"""
    if f==0: return ov
    if view in ('down','up'):
        if style=='long':
            y0=17 if view=='down' else 18
            ov=_shift(ov,y0,23,1,0,8) if f==1 else _shift(ov,y0,23,-1,8,16)
        return ov
    # 横（右向き）: 後ろ髪の先が後ろ（左）へ
    if style=='long': ov=_shift(ov,17 if f==1 else 19,23,-1,0,7)
    elif style in ('spiky','short'): ov=_shift(ov,14 if f==1 else 15,16,-1,0,6)
    elif style=='hood': ov=_shift(ov,16 if f==1 else 17,19,-1,0,6)
    return ov
HELD=('sword','lantern','pickaxe')   # 杖は腕といっしょに振る（人間の指示 2026-10-04）
def _arm_swing(g,view,f,decos):
    """正面・後ろの腕振り。手の位置のずれ（{2:dy,13:dy}）を返す。"""
    dys={2:0,13:0}
    if f==0 or view not in ('down','up'): return dys
    # 物を持つ手: 正面は画面の左の腕、後ろ向きは画面の右の腕。盾は反対の腕
    held=set()
    if any(d in decos for d in HELD): held.add(2 if view=='down' else 13)
    if 'shield' in decos: held.add(13 if view=='down' else 2)
    fwd=13 if f==1 else 2          # 出した足と反対の腕が前へ
    for col in (2,13):
        if col in held: continue
        ol=col-1 if col==2 else col+1
        if any(g[y][col] in 'HhL' for y in range(20,24)): continue   # 髪で隠れている腕は動かさない
        sleeve=g[21][col]
        if col==fwd:
            g[21][col]='A'; g[22][col]='S'; g[23][col]='O'; g[23][ol]='.'; dys[col]=-1
        else:
            g[22][col]=sleeve; g[23][col]='A'; g[24][col]='S'; g[24][ol]='O'
            if g[25][col] in '.BbTt': g[25][col]='O'
            dys[col]=1
    return dys
def frame(dr,f,style='spiky',outfit='tunic',beard=False,decos=(),hair_sway=True):
    hf=f if hair_sway else 0   # 髪を揺らさない人物（男性、人間の指示 2026-10-04）
    if dr=='down': g=FRONT_TOP+LEGS_F[f]; g=overlay(g,_hair_sway(HAIR[style]['down'],'down',style,hf))
    elif dr=='up': g=BACK_TOP+LEGS_F[f]; g=overlay(g,_hair_sway(HAIR[style]['up'],'up',style,hf))
    else:
        g=SIDE_TOP+LEGS_S[f]; g=overlay(g,_hair_sway(HAIR[style]['side'],'side',style,hf))
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
    if outfit in ('tunic','coat'): g=_boot_cuffs(g)
    if outfit=='coat':   # 長い上着（すそがひざまで）
        if not side:
            for y in range(24,28):
                for x in (3,4): g[y][x]='T' if x==3 else 't'
                for x in (11,12): g[y][x]='t'
                g[y][2]='O'; g[y][13]='O'
            for x in range(2,14):
                if g[28][x] in '.': pass
            g[28][3]='O'; g[28][4]='O'; g[28][11]='O'; g[28][12]='O'
        else:
            for y in range(24,28):
                g[y][4]='O'; g[y][5]='T'
            g[28][5]='O'
    g=_details(g,'side' if side else dr)
    _decorate.armdy=_arm_swing(g,'side' if side else dr,f,decos)
    _decorate.frame=f; _decorate.hairf=hf
    g=_decorate(g,'side' if side else dr,decos)
    g=[''.join(r) for r in g]
    if dr=='left': g=[r[::-1] for r in g]
    if dr in ('down','up'): g=light_left(g)
    assert len(g)==32 and all(len(r)==16 for r in g),(dr,f,[len(r) for r in g])
    return g

def all_frames(style='spiky', outfit='tunic', beard=False, decos=(), hair_sway=True):
    """{"down0": [...32行], ...} の12コマ。decos: band（はちまき）・cape（マント）・backsword（背中の剣）・sword（手に剣）・shield（盾）・helmet（兜）・staff（杖）・scarf（マフラー）・goggles（ゴーグル）・twintails（ふたつ結び）・ponytail（ポニーテール）・circlet（額の飾り）・bracelet（光る腕輪）・pickaxe（つるはし）"""
    return {f"{d}{f}": frame(d, f, style, outfit, beard, decos, hair_sway) for d in ('down', 'up', 'left', 'right') for f in (0, 1, 2)}
