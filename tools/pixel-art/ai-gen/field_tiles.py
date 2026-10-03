"""フィールド（世界地図）の絵を作る（2026-10-03、v2）。

人間が見せた参考画像（スーファミ後期の王道RPGの世界地図）の「質の要素」を、手描きの型と規則で作る。絵そのものは写していない（CLAUDE.md 1-1）。
- 草地: 2〜3色の細かい点（市松に近い揺らぎ）
- 山: 丸い小山（左上が明るく、右下に暗いふち）を、段ごとに半分ずらして重ねた連なり。塊の中心が山のマスにあるものだけ描くので、ふちが丸くでこぼこになる
- 森: 丸い木をぎっしり重ねる（同じ方法）
- 段差: 高い草地（,）のふちに茶色のぎざぎざの線
- 低い木の茂み（%）、海岸の砂と白い泡、雪山（A）
- 町・城・ほこら・洞窟・橋・道は、16×16の型を重ねる
地図の文字: ~ 海／. 草原／, 高い草地／T 森／^ 山／A 雪山／h 丘／: 砂漠／= 道／s 沼／* 雪原／V 町／C 城／b 橋／c 洞窟／S ほこら／% 低い茂み
使い方:
  python3 tools/pixel-art/ai-gen/field_tiles.py 出力フォルダ [地図.txt]
  出力: map.png（地図・3倍）、crop.txt / crop.json（左上から96×96を切り出した、ドット絵エディタで描く用の文字グリッドとパレット）
"""
import random
from PIL import Image
T=16
PAL={'O':'#141a10',
 'G':'#58b040','g':'#3e8a30','q':'#80d058',          # 草原
 'F':'#2e8a3a','f':'#1c5e28','l':'#5cc050','k':'#6a4220',  # 森
 'M':'#b88a50','m':'#7a5630','n':'#e0c088','X':'#f4f4f4',   # 山
 'W':'#2c5cd0','w':'#1e3c98','v':'#7aa8f8','Z':'#d8e8ff',   # 海
 'D':'#e8cc80','d':'#c8a058','e':'#fff0b0',                # 砂漠
 'R':'#c89a58','r':'#9a7038',                               # 道
 'S':'#6a7a4a','s':'#4a5a30','p':'#8a6aa0',                 # 沼
 'N':'#f0f4ff','n2':'#c0cce8',
 'C':'#f0e0c0','c':'#c0a880','A':'#c8603a','a':'#8a3a20','B':'#9098a8','b':'#5a6070','U':'#4a70d8','u':'#2a4898','Y':'#f0c040','K':'#2a1a10'}
def new(fill): return [[fill]*T for _ in range(T)]
def rnd(seed): r=random.Random(seed); return r
def grass(seed=1):
    g=new('G'); r=rnd(seed)
    for _ in range(7):
        x,y=r.randrange(1,15),r.randrange(2,15)
        g[y][x]='g'; g[y-1][x]='q' if r.random()<0.5 else 'g'
        if x+1<T: g[y][x+1]='g'
    return g
def crown(g,cx,cy,rad=3.6):
    for y in range(T):
        for x in range(T):
            d=((x-cx)**2+((y-cy)*1.1)**2)**0.5
            if d<=rad+0.6:
                if d>rad-0.5: g[y][x]='O'
                else:
                    lit=(x-cx)+(y-cy)
                    g[y][x]='l' if lit<-2.5 else ('F' if lit<1.5 else 'f')
def forest(seed=2):
    g=grass(seed)
    # 幹
    for (cx,cy) in ((4,4.2),(11.5,4.6),(7.5,10.6)):
        for y in range(int(cy)+3,int(cy)+5):
            if y<T:
                g[y][int(cx)]='k'; g[y][int(cx)+1]='f'
    for (cx,cy) in ((4,4.2),(11.5,4.6),(7.5,10.6)): crown(g,cx,cy)
    return g
def mountain(snow=False):
    g=grass(5)
    for y in range(1,T):
        hw=(y-1)*0.62+0.5
        for x in range(T):
            dx=x-7.5
            if abs(dx)<=hw+0.5:
                if abs(dx)>hw-0.6 or y==T-1: g[y][x]='O'
                else:
                    if dx<-0.3: g[y][x]='n' if (abs(dx)>hw-1.8 and y<9) else 'M'
                    else: g[y][x]='m'
    # 稜線のすじ
    for y in range(5,14,3):
        for x in range(4,7):
            if g[y][x]=='M' and (x+y)%2==0: g[y][x]='m'
    if snow:
        for y in range(2,6):
            for x in range(T):
                if g[y][x] in 'Mmn': g[y][x]='X' if x<8 else 'n'
    return g
def sea(seed=3):
    g=new('W'); r=rnd(seed)
    for (x,y) in ((2,3),(10,6),(5,11),(12,13)):
        for dx in range(3): g[y][(x+dx)%T]='v' if dx!=1 else 'v'
        g[y-1][(x+1)%T]='Z'
    for (x,y) in ((7,1),(1,8),(13,9)):
        g[y][x]='w'; g[y][(x+1)%T]='w'
    return g
def desert(seed=4):
    g=new('D'); r=rnd(seed)
    for (x,y) in ((3,4),(10,3),(6,10),(12,12)):
        for dx in range(4): g[y][(x+dx)%T]='d'
        for dx in range(1,3): g[y-1][(x+dx)%T]='e'
    for _ in range(5):
        g[r.randrange(T)][r.randrange(T)]='d'
    return g
def road():
    g=grass(6)
    for y in range(T):
        for x in range(4,12):
            g[y][x]='R' if 5<=x<=10 else 'r'
        if y%4==1: g[y][7]='r'
    return g
def swamp():
    g=new('S')
    for (x,y) in ((2,3),(9,5),(4,10),(12,12)):
        for dx in range(3): g[y][x+dx]='s'
        g[y-1][x+1]='p'
    return g
def town():
    g=grass(7)
    def house(x0,y0):   # 幅8の家。三角の屋根（ひさしが出る）、壁・戸・窓
        rows=["...OO...","..OAAO..",".OAAAaO.","OAAAAAaO","OOOOOOOO",".OCCcCO.",".OKCcYO.",".OKCcCO.",".OOOOOO."]
        for k,row in enumerate(rows):
            for j,ch in enumerate(row):
                if ch!='.' and 0<=y0+k<T and 0<=x0+j<T: g[y0+k][x0+j]=ch
    house(0,0); house(8,1); house(4,7)
    return g
def castle():
    g=grass(8)
    for y in range(5,15):
        for x in range(2,14):
            g[y][x]='O' if x in (2,13) or y==14 else ('B' if x<8 else 'b')
    for x in range(2,14,2): g[5][x]='O'
    for tx in (1,12):
        for y in range(2,15):
            for x in range(tx,tx+3):
                g[y][x]='O' if x in (tx,tx+2) or y==14 else 'B'
        g[1][tx+1]='O'; g[2][tx+1]='U'; g[2][tx]='O';g[2][tx+2]='O'
        g[3][tx+1]='U'
    for y in range(3,6):
        for x in range(6,10): g[y][x]='O' if x in (6,9) else 'U'
    g[2][7]='O'; g[2][8]='O'; g[1][7]='Y'
    for y in range(10,15):
        for x in range(7,9): g[y][x]='K'
    for y in (8,): g[y][4]='K'; g[y][11]='K'
    return g
def bridge():
    g=sea(9)
    for y in range(T):
        for x in range(3,13):
            g[y][x]='O' if x in (3,12) else ('R' if y%3 else 'r')
    return g
def snow():
    g=new('N')
    for (x,y) in ((3,4),(11,7),(6,12)):
        g[y][x]='n2'; g[y][x+1]='n2'
    return g
def hills():
    g=grass(12)
    mound=["...OOOO...","..OqqqGO..",".OqqGGGGO.","OqGGGGGggO","GGGGGGggGG"]
    for (x0,y0) in ((0,2),(6,9)):
        for k,row in enumerate(mound):
            for j,ch in enumerate(row):
                if ch!='.' and 0<=y0+k<T and 0<=x0+j<T: g[y0+k][x0+j]=ch
    return g
def cave():
    g=mountain()
    for y in range(10,15):
        for x in range(6,10):
            g[y][x]='O' if (y==10 or x in (6,9)) else 'K'
    return g
def shrine():
    g=grass(13)
    rows=["......OO........",".....OYYO.......","....OUUUUO......","...OUUUUUUO.....","..OOOOOOOOOO....","...OCCCCCCO.....","...OCKCCKCO.....","...OCCCCCCO.....","...OCCKKCCO.....","...OCCKKCCO.....","..OOOOOOOOOO....","..ObbbbbbbbO...."]
    for k,row in enumerate(rows):
        for j,ch in enumerate(row):
            if ch!='.': g[2+k][j+1]=ch
    return g
TILES={'grass':grass(),'grass2':grass(11),'forest':forest(),'mountain':mountain(),'snowpeak':mountain(True),'sea':sea(),'desert':desert(),'road':road(),
 'swamp':swamp(),'snow':snow(),'town':town(),'castle':castle(),'bridge':bridge(),'hills':hills(),'cave':cave(),'shrine':shrine()}
T=16
OLD=TILES; PAL=dict(PAL)
PAL.update({'G':'#5cb83a','g':'#4aa22e','q':'#86d454',
 'Mn':'#ecd690','Mm':'#cdae5c','Ms':'#a07e3c','Mo':'#6e5022','MO':'#3a2810',
 'Fl':'#8ad85c','Fm':'#4cae3c','Fs':'#2e8030','Fd':'#1c5020','Fk':'#6a4a20',
 'Bb':'#8a6a32','Bc':'#5a4018','Rr':'#7a5a2a','Rl':'#b09050'})
MAPM={'n':'Mn','M':'Mm','m':'Ms','o':'Mo','O':'MO'}
MAPF={'l':'Fl','F':'Fm','f':'Fs','d':'Fd','k':'Fk'}
def h(x,y,s=0): return (((x*73856093) ^ (y*19349663) ^ (s*83492791)) & 0xffffff)/0xffffff
MOUND=["..nnn...",
       ".nnnMM..",
       "nnnMMMm.",
       "nnMMMMmm",
       "nMMMMmmo",
       "MMMMmmoo",
       "MMmmmooo",
       "oooooooO"]
TREE=["..lll...",
      ".llFFF..",
      "lllFFFf.",
      "llFFFFff",
      "lFFFFfff",
      ".FFFffd.",
      "..ddkd..",
      "...kk..."]
def grass_px(x,y):
    v=h(x,y)
    if v<0.22: return 'g'
    if v<0.27: return 'q'
    return 'G'
MOUND2=["...nn...",
        "..nnMM..",
        ".nnMMMm.",
        "nnMMMMmm",
        "nMMMMmmo",
        "MMMmmmoo",
        "MMmmmooo",
        "OoooooOO"]
MOUND3=[".nnn....",
        "nnnMMm..",
        "nnMMMMm.",
        "nMMMMMmm",
        "MMMMMmmo",
        "MMMmmmoo",
        "MmmmmooO",
        "oooooOO."]
TREE2=["...ll...",
       "..llFF..",
       ".llFFFf.",
       "llFFFFff",
       "lFFFFfff",
       "lFFFfffd",
       ".dFffdd.",
       "...kk..."]

def blob(w,hgt,tones,outline,seed=0,squash=1.0,peak=0.0):
    """丸い塊（小山・木の葉）を作る。左上から光、トーンの境目は市松でなじませる、右下に暗いふち。"""
    rows=[]
    cx,cy=(w-1)/2,(hgt-1)/2
    for y in range(hgt):
        r=''
        for x in range(w):
            nx=(x-cx)/(w/2); ny=(y-cy)/(hgt/2)
            ny2=ny*squash - peak*(1-abs(nx))   # peak>0 で頭がとがる
            d=nx*nx+ny*ny if ny>0 else nx*nx+ny2*ny2*0.9+ max(0,ny2)*0
            d=nx*nx+(ny if ny>0 else ny*squash)**2
            if d>1.0: r+='.'; continue
            nz=max(0,1-d)**0.5
            lum=-0.45*nx-0.55*ny+0.25*nz
            th=[-0.2,0.12,0.55]
            ti=sum(1 for v in th if lum>v)
            near=min(abs(lum-v) for v in th)
            if near<0.07 and (x+y)%2==0: ti=max(0,ti-1)   # 境目を市松に
            ti=max(0,min(len(tones)-1,ti))
            ch=tones[ti]
            if (d>0.72 and (nx+ny)>0.25) or (ny>0.78): ch=outline
            r+=ch
        rows.append(r)
    return rows
MOUNDS=[blob(16,12,['o','m','M','n'],'O'),blob(15,11,['o','m','M','n'],'O'),blob(17,12,['o','m','M','n'],'O')]
TREES=[blob(9,10,['d','f','F','l'],'d'),blob(8,9,['d','f','F','l'],'d')]
def scatter(pats,x,y,sx,sy,seed,ok=None):
    """形を、横 sx・縦 sy の間かくで、段ごとに半分ずらして並べる（下の段ほど手前）。"""
    best=None
    for row in range(-3,1):
        r=(y//sy)+row; oy=r*sy
        off=(sx//2) if r%2 else 0
        for col in range(-2,1):
            c=((x-off)//sx)+col
            pat=pats[int(h(c,r,seed)*len(pats))]
            jx=int(h(c,r,seed+1)*3)-1; jy=int(h(c,r,seed+2)*2)
            ox=c*sx+off+jx; oyy=oy+jy
            py,px=y-oyy,x-ox
            if 0<=py<len(pat) and 0<=px<len(pat[0]):
                if ok is not None and not ok(ox+len(pat[0])//2, oyy+len(pat)//2): continue
                ch=pat[py][px]
                if ch!='.': best=(ch, ox+len(pat[0])//2, oyy+len(pat)//2)
    return best
def pattern_var(pats,x,y):
    best=None
    for row in range(-1,2):
        r=(y//4)-row; oy=r*4
        off=4 if r%2 else 0
        cx=(x-off)//8
        jx=int(h(cx,r,11)*3)-1          # 横に -1〜1 ずらす
        ox=cx*8+off+jx
        pat=pats[int(h(cx,r,12)*len(pats))]
        py,px=y-oy,x-ox
        if 0<=py<8 and 0<=px<8:
            ch=pat[py][px]
            if ch!='.': best=ch
    return best
def pattern_px(pat,x,y):
    """8×8の形を、4ドットごとに段をずらして敷きつめる（下の段が上の段に重なる＝うろこ）。"""
    best=None
    for row in range(-1,2):
        oy=((y//4)-row)*4
        off=4 if ((y//4)-row)%2 else 0
        ox=((x-off)//8)*8+off
        py,px=y-oy,x-ox
        if 0<=py<8 and 0<=px<8:
            ch=pat[py][px]
            if ch!='.': best=ch   # 下の段（あとの行）ほど手前
    return best
KEY={'~':'sea','.':'grass',',':'high','T':'forest','^':'mountain','A':'snowpeak','h':'hills',':':'desert','=':'road','s':'swamp','*':'snow','V':'town','C':'castle','b':'bridge','c':'cave','S':'shrine','%':'brush'}
def render(MAP):
    H=len(MAP)*T; W=len(MAP[0])*T
    tn=lambda x,y: KEY[MAP[min(len(MAP)-1,max(0,y//T))][min(len(MAP[0])-1,max(0,x//T))]]
    g=[[None]*W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            t=tn(x,y)
            if t in ('grass','high','mountain','forest','snowpeak','hills','brush','road','town','castle','cave','shrine'):
                c=grass_px(x,y)
                if t=='brush' and h(x//2,y//2,3)<0.35: c='Bb' if h(x,y,4)<0.6 else 'Bc'
                g[y][x]=c
            else:
                tile=OLD[{'sea':'sea','desert':'desert','swamp':'swamp','snow':'snow','bridge':'bridge'}[t]]
                g[y][x]=tile[y%T][x%T]
    # 山と森（地図全体の座標で敷きつめる。塊の中心が山・森のタイルにあるものだけ描くので、ふちが丸くでこぼこになる）
    MT=('mountain','snowpeak','cave')
    for y in range(H):
        for x in range(W):
            if tn(x,y) in ('sea','bridge'): continue
            r=scatter(MOUNDS,x,y,14,9,20,lambda cx,cy: tn(cx,cy) in MT)
            if r:
                ch,cx,cy=r
                if tn(cx,cy)=='snowpeak' and ch in 'nMm':
                    g[y][x]={'n':'X','M':'N','m':'n2'}[ch]
                else: g[y][x]=MAPM[ch]
                continue
            r=scatter(TREES,x,y,8,7,30,lambda cx,cy: tn(cx,cy)=='forest')
            if r: g[y][x]=MAPF[r[0]]
    # 特別なタイル（町・城・ほこら・洞窟の入口・道）は前の型を重ねる（草の部分は重ねない）
    for y in range(H):
        for x in range(W):
            t=tn(x,y)
            if t in ('town','castle','shrine','road'):
                ch=OLD[t][y%T][x%T]
                if ch not in ('G','g','q'): g[y][x]=ch
            if t=='cave' and 8<=y%T<=13 and 5<=x%T<=10:
                yy,xx=y%T-8,x%T-5
                cave=["..OO..",".OKKO.","OKKKKO","OKKKKO","OKKKKO","OOOOOO"]
                if cave[yy][xx]!='.': g[y][x]=cave[yy][xx]
    # 段差の線: 高い草地（,）のふちに、茶色のぎざぎざの線
    for y in range(H):
        for x in range(W):
            if tn(x,y)!='high': continue
            for dx,dy in ((0,1),(1,0),(-1,0),(0,-1)):
                if tn(x+dx*3,y+dy*3)=='grass':
                    j=int(h(x//3,y//3,7)*3)
                    if (dy and (y%T)==(T-3+j if dy>0 else j)) or (dx and (x%T)==(T-3+j if dx>0 else j)):
                        g[y][x]='Rr' if h(x,y,9)<0.7 else 'Rl'
    # 海岸
    land=[[tn(x,y) not in ('sea','bridge') for x in range(W)] for y in range(H)]
    out=[r[:] for r in g]
    for y in range(H):
        for x in range(W):
            nb=[(y+a,x+b) for a,b in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+a<H and 0<=x+b<W]
            if land[y][x] and any(not land[a][b] and tn(b,a)=='sea' for a,b in nb): out[y][x]='D'
            elif tn(x,y)=='sea' and any(land[a][b] for a,b in nb): out[y][x]='Z'
    return out
def save(g,path,Z=3):
    H=len(g);W=len(g[0]); im=Image.new('RGB',(W,H)); px=im.load()
    for y in range(H):
        for x in range(W):
            c=PAL[g[y][x]]; px[x,y]=tuple(int(c[i:i+2],16) for i in (1,3,5))
    im.resize((W*Z,H*Z),Image.NEAREST).save(path)
MAP=[
"~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~..TTTT^^^^^^~~~~~~~~",
"~~~..,TTTT^^^^^^c~~**~~~",
"~~..,,,TT^^^^AA^^~~**A*~",
"~~.V==,,,,^^^^^^~~***~~~",
"~~..,=,,,,..^^..b=.S.,~~",
"~~~..=..TTT.....~~.TT.~~",
"~~~%%=.TTTTT.:::~~~~~~~~",
"~~.%%C..TTTT::::::~~~~~~",
"~~~%%....TT.:::::::~~~~~",
"~~~~..ss.,,.:::V:::~~~~~",
"~~~~.sss.,,..::::~~~~~~~",
"~~~~~.ss......~~~~~~~~~~",
"~~~~~~......~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~",
"~~~~~~~~~~~~~~~~~~~~~~~~"]

if __name__=='__main__':
    import sys, os, json
    out=sys.argv[1]; os.makedirs(out,exist_ok=True)
    if len(sys.argv)>2:
        MAP[:]=[l.rstrip(chr(10)) for l in open(sys.argv[2]) if l.strip()]
    g=render(MAP); save(g,out+'/map.png',3)
    L="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    m={};P2={};rows=[]
    for r in g[:96]:
        s=''
        for ch in r[:96]:
            col=PAL[ch]
            if col not in m: m[col]=L[len(m)]; P2[m[col]]=col
            s+=m[col]
        rows.append(s)
    open(out+'/crop.txt','w').write(chr(10).join(rows)+chr(10)); json.dump(P2,open(out+'/crop.json','w'))
    print('地図:', out+'/map.png', '切り出し:', len(P2), '色')
