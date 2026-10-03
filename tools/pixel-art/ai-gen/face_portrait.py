"""アニメ調の顔のドット絵（64×64、会話の顔）を作る型（2026-10-03）。

手描きの型（大きな目・房に分かれた前髪・頭の丸みに沿った髪のつや・頬の赤み・とがったあご）に、
人物ごとの髪型・色・飾りを組み合わせる。特定の漫画家・イラストレーターの絵柄には寄せていない（CLAUDE.md 1-1）。
髪型: spiky（とがった短髪）・messy（ぼさぼさの短髪）・long（長い髪）・twin（ふたつ結び）・short（ふつうの短髪）
飾り（extras）: band はちまき・scarf マフラー・lid 落ち着いた目（まぶたを下ろす）・clip 髪留め・ribbon 胸のリボン・
  goggles ゴーグル・vest ベスト・collar 襟・helmet 兜（鉱山のヘルメット）
文字: O 外周／K 肌の外周／S s 肌／P 頬／E まつげ・瞳の縁／I i J 瞳（地・影・光）／W 白／m 口／H h D L 髪（地・影・すじ・光）／
  T t 服／A a 目印／M Y N 金属（兜）／G 金具／Q レンズ・灯り／V ベスト
使い方:
  python3 tools/pixel-art/ai-gen/face_portrait.py 出力フォルダ            # CHARS の全員
  python3 tools/pixel-art/ai-gen/face_portrait.py 出力フォルダ yuri mina  # 選んだ人だけ
  出力: <名前>.png（8倍の確認用）・<名前>.txt / .json（ドット絵エディタで描く用の文字グリッドとパレット）
  新しい人物は CHARS に1行足す（style・extras・色）。
"""
from PIL import Image
N=64; CX=31.5
EYE=[
"..EEEEEEE.",
".EEEEEEEEE",
"EEiiiiiiEE",
".EiWWiiiiE",
".WiWWiiIiW",
".WiiiiIIiW",
".WIIIIIIIW",
".WIJJJJJIW",
"..WJJJJJW.",
"...WWWWW..",
"....EEE..."]
def face_hw(y):
    if y<17: return None
    if y<=34: return 12.5-max(0,(22-y))*0.7
    if y<=44: return 12.5-(y-34)*0.45
    if y<=52: return 8.0-(y-44)*0.95
    return None
def tri(g,cx,y0,y1,w0,c,lean=0.0):
    """y0（根元・幅w0）から y1（先）へ細くなる房。lean で先が横にずれる。"""
    n=max(1,y1-y0)
    for k in range(n+1):
        y=y0+k; t=k/n; w=w0*(1-t); x0=cx+lean*t
        for x in range(int(round(x0-w/2)),int(round(x0+w/2))+1):
            if 0<=y<N and 0<=x<N: g[y][x]=c
def draw(sp):
    g=[['.']*N for _ in range(N)]
    def put(y,x,c):
        if 0<=y<N and 0<=x<N: g[y][x]=c
    st=sp['style']
    # 後ろ髪
    if st=='long':
        for y in range(16,64):
            hw=18.5+max(0,y-36)*0.12
            for x in range(int(CX-hw),int(CX+hw)+1): put(y,x,'h')
    # 服・首
    for y in range(55,64):
        hw=9+(y-55)*2.7
        for x in range(int(CX-hw),int(CX+hw)+1): put(y,x,'T' if x<CX+hw*0.45 else 't')
    for y in range(47,58):
        for x in range(28,36): put(y,x,'s' if (y<51 or x>=34) else 'S')
    # 顔
    for y in range(17,53):
        hw=face_hw(y)
        if hw is None: continue
        for x in range(int(round(CX-hw)),int(round(CX+hw))+1):
            put(y,x,'S' if x<CX+hw-2.5 else 's')
    for y in range(33,40): put(y,18,'S'); put(y,45,'s')
    # 目（左右）
    for k,row in enumerate(EYE):
        for j,ch in enumerate(row):
            if ch=='.': continue
            put(29+k,19+j,ch)
            put(29+k,44-j,ch)
    # 右目のハイライトを左上へ（左右反転で右に寄ったのを直す）
    for y in (32,33):
        for x in (39,40): put(y,x,'i')
        for x in (36,37): put(y,x,'W')
    # 眉
    for x in range(20,28): put(26 if 22<x<27 else 27,x,'D')
    for x in range(36,44): put(26 if 36<x<41 else 27,x,'D')
    # 鼻・口・ほお
    put(41,32,'s'); put(42,31,'s')
    for x in range(30,34): put(46,x,'m')
    put(45,29,'m'); put(45,34,'m')
    for x in (20,22,24,39,41,43): put(41,x,'P')
    # 頭（髪の地）
    for y in range(8,30):
        for x in range(10,54):
            dx=(x-CX)/20.5; dy=(y-25)/16.5
            if dx*dx+dy*dy<=1 and y<19: put(y,x,'H' if x<CX+9 else 'h')
    # 前髪の房（cx, 先のy, 根元の幅, 先のずれ）
    bangs={'spiky':[(14,42,9,-2),(20,32,11,-1),(26,30,10,1),(32,33,10,0),(38,30,10,1),(44,34,11,2),(50,42,9,2)],
           'messy':[(14,46,9,-1),(20,34,11,2),(27,37,11,3),(33,31,10,0),(39,35,11,-2),(45,38,10,1),(50,46,8,1)],
           'long':[(14,60,10,-1),(20,33,11,1),(26,29,10,0),(32,31,10,0),(38,29,10,0),(44,33,11,-1),(50,60,10,1)],
           'twin':[(15,42,9,-1),(21,31,11,1),(28,29,10,0),(34,30,10,0),(40,31,11,-1),(48,42,9,1)],
           'short':[(15,40,9,-1),(21,29,11,1),(28,28,11,0),(35,29,11,0),(42,31,11,-1),(48,40,9,1)]}[st]
    for cx,tip,w,lean in bangs:
        tri(g,cx,17,tip,w,'H' if cx<CX+9 else 'h',lean)
    # 房の先の影（下2ドット）
    for y in range(N):
        for x in range(N):
            if g[y][x] in 'Hh' and y+1<N and g[y+1][x] in 'SsWEiIJ' and y>20: g[y][x]='D'
    # とがった頭頂
    if st=='spiky':
        def captop(x):
            dx=(x-CX)/20.5
            return 25-16.5*(max(0,1-dx*dx))**0.5
        for x0,w,h,lean in ((13,8,6,-4),(20,8,7,-2),(27,8,8,0),(34,8,7,2),(41,8,6,3),(47,7,5,4)):
            base=int(captop(x0+w/2))+3
            for k in range(h+4):
                y=base-k; t=max(0,(k-3))/h; ww=w*(1-t); xc=x0+w/2+lean*t
                for x in range(int(round(xc-ww/2)),int(round(xc+ww/2))+1): put(y,x,'H' if x<CX+9 else 'h')
    # つや: 頭の丸みに沿った2段の光の帯（左寄り。房の境で切れる）
    cuts={int(round(cx-w/2)) for cx,tip,w,lean in bangs}
    for x in range(15,int(CX+8)):
        if x in cuts or x+1 in cuts: continue
        y=14+int(round(((x-29)/14)**2*3))
        for yy in (y,y+1):
            if 0<=yy<N and g[yy][x] in 'Hh': g[yy][x]='L'
    # 房のすじ（左の縁に暗い線）
    for cx,tip,w,lean in bangs:
        for y in range(20,tip-2):
            t=(y-17)/max(1,tip-17); xl=int(round(cx+lean*t-w*(1-t)/2))
            if 0<=xl<N and g[y][xl] in 'Hh': g[y][xl]='D'
    # ツインテール
    if st=='twin':
        for side in (-1,1):
            for y in range(14,52):
                cx=CX+side*(23+ (y-14)*0.15); hw=4.5 if y<44 else 4.5-(y-44)*0.55
                for x in range(int(round(cx-hw)),int(round(cx+hw))+1): put(y,x,'H' if side<0 else 'h')
    ex=sp.get('extras',())
    if 'twin' == st:
        for side in (-1,1):
            cx=int(round(CX+side*23))
            for x in range(cx-4,cx+5):
                for y in (15,16): put(y,x,'A' if y==15 else 'a')
    if 'band' in ex:
        for y in (18,19,20):
            for x in range(int(CX-19),int(CX+20)):
                if g[y][x] in 'HhDL': g[y][x]='A' if y<20 else 'a'
        for (y,x) in ((19,51),(20,52),(21,53),(22,54),(20,51),(21,52),(22,53),(23,54),(23,53),(24,54)):
            put(y,x,'A' if x<53 else 'a')
    if 'helmet' in ex:
        for y in range(4,21):
            for x in range(8,56):
                dx=(x-CX)/21; dy=(y-21)/16.5
                if dx*dx+dy*dy<=1: put(y,x,'M' if x<CX+8 else 'Y')
        for x in range(9,55): put(20,x,'Y'); put(21,x,'Y')
        for x in range(14,24): put(9 if x<19 else 8,x,'N')
        for y in range(8,14):
            for x in range(29,35): put(y,x,'Q' if 9<=y<=12 and 30<=x<=33 else 'G')
    if 'goggles' in ex:
        for x in range(12,52):
            if g[18][x] != '.': put(18,x,'a')
        for cx0 in (24,39):
            for y in range(14,23):
                for x in range(cx0-5,cx0+6):
                    d=((x-cx0)**2+(y-18)**2)**0.5
                    if d<=4.9: put(y,x,'G' if d>3.3 else ('Q' if (x+y)%5 else 'W'))
    if 'clip' in ex:
        for (y,x) in ((19,19),(19,20),(19,21),(20,20),(18,20)): put(y,x,'A')
    if 'lid' in ex:   # 落ち着いた目（まぶたを下ろす）
        for k,row in enumerate(EYE[:3]):
            for j,ch in enumerate(row):
                if ch=='.': continue
                for xx in (19+j,44-j):
                    if k==0: put(29,xx,'S')
                    elif k==1: put(30,xx,'E' if j>0 else 'S')
                    else: put(31,xx,'E')
    if 'scarf' in ex:
        for y in range(52,58):
            hw=6+(y-52)*1.3
            for x in range(int(CX-hw),int(CX+hw)+1): put(y,x,'A' if y<56 else 'a')
        for (y,x) in ((56,34),(57,34),(58,35),(59,35),(58,34),(59,34)): put(y,x,'a')
    if 'ribbon' in ex:
        for (y,x) in ((56,29),(56,30),(57,30),(57,31),(57,32),(56,33),(56,34),(57,33),(58,31),(58,32)): put(y,x,'A')
    if 'vest' in ex:
        for y in range(57,64):
            for x in range(N):
                if g[y][x] in 'Tt' and abs(x-CX)>5+(y-57)*0.8: g[y][x]='V'
    if 'collar' in ex:
        for (y,x) in ((55,28),(56,29),(57,30),(55,35),(56,34),(57,33)): put(y,x,'A')
    # 外周の縁取り
    out=[r[:] for r in g]
    edgecol={'H':'O','h':'O','D':'O','L':'O','S':'K','s':'K','T':'O','t':'O','P':'K','A':'O','a':'O','M':'O','Y':'O','N':'O','G':'O','V':'O'}
    for y in range(N):
        for x in range(N):
            if g[y][x]=='.': continue
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                yy,xx=y+dy,x+dx
                if not(0<=yy<N and 0<=xx<N) or g[yy][xx]=='.':
                    out[y][x]=edgecol.get(g[y][x],g[y][x]); break
    return [''.join(r) for r in out]
P={'O':'#2a1418','K':'#8a4a3a','S':'#ffdcc0','s':'#eab496','P':'#f4a0a0','H':'#a8522a','h':'#7a3416','D':'#4a1c10','L':'#e08850',
   'E':'#1a1020','W':'#ffffff','I':'#2a9a68','i':'#145040','J':'#7ad8a8','m':'#b0505a','T':'#2a7c88','t':'#1c5058'}
def render(list_rows,path,Z=6):
    im=Image.new('RGB',(len(list_rows)*(N*Z+8),N*Z),(70,60,100))
    for i,rows in enumerate(list_rows):
        for y,r in enumerate(rows):
            for x,ch in enumerate(r):
                if ch=='.':continue
                c=tuple(int(P[ch][k:k+2],16) for k in (1,3,5))
                for dy in range(Z):
                    for dx in range(Z): im.putpixel((i*(N*Z+8)+x*Z+dx,y*Z+dy),c)
    im.save(path)
CHARS={
 'yuri': dict(style='spiky',extras=('band','scarf'),pal={'H':'#a8582c','h':'#7a3c1c','D':'#4a2010','L':'#e0904c','I':'#2a9a68','i':'#14503c','J':'#80dcae','T':'#2a7c88','t':'#1c5058','A':'#e07a20','a':'#a8480c'}),
 'reto': dict(style='messy',extras=('lid','scarf'),pal={'H':'#8a3020','h':'#5e1c12','D':'#3a0e08','L':'#c8583c','I':'#c8862c','i':'#6a3e10','J':'#f0c070','T':'#4a5268','t':'#2e3446','A':'#c83c34','a':'#7a1418'}),
 'mina': dict(style='long',extras=('clip','ribbon'),pal={'H':'#4a8ad0','h':'#2a5a9a','D':'#1a3a6a','L':'#9ad0ff','I':'#3a70d0','i':'#1c3a80','J':'#9ac8ff','T':'#eef4fc','t':'#b8c8e0','A':'#3a80d8','a':'#1c4a8a'}),
 'guide': dict(style='twin',extras=('goggles','vest','collar'),pal={'H':'#e0b040','h':'#b07a1c','D':'#6a4410','L':'#fff0a0','I':'#3a9a5a','i':'#1c5a30','J':'#9ae0a8','T':'#f4ecdc','t':'#c8bca0','A':'#34a45c','a':'#1c6a3c','G':'#8890a0','Q':'#58b0e8','V':'#6a4222'}),
 'orca': dict(style='short',extras=('helmet','collar'),pal={'H':'#5a3a26','h':'#3a2416','D':'#20120a','L':'#8a6a50','S':'#d8a478','s':'#b07a50','K':'#6a3a20','P':'#d88a70','I':'#7a5030','i':'#3a2410','J':'#c09060','T':'#e07a20','t':'#a84a0c','A':'#586070','a':'#3a4050','M':'#9aa2b0','Y':'#5a6070','N':'#e0e8f0','G':'#c8a040','Q':'#ffe070'}),
}
BASE={'O':'#2a1418','K':'#8a4a3a','S':'#ffdcc0','s':'#eab496','P':'#f4a0a0','E':'#1a1020','W':'#ffffff','m':'#b0505a'}
def palette(name):
    p=dict(BASE); p.update(CHARS[name]['pal'])
    if 'M' in p and name=='orca': pass
    return p
def render_all(path,Z=5):
    global P
    names=list(CHARS)
    im=Image.new('RGB',(len(names)*(N*Z+8),N*Z),(70,60,100))
    for i,n in enumerate(names):
        rows=draw(CHARS[n]); P=palette(n)
        for y,r in enumerate(rows):
            for x,ch in enumerate(r):
                if ch=='.':continue
                c=tuple(int(P[ch][k:k+2],16) for k in (1,3,5))
                for dy in range(Z):
                    for dx in range(Z): im.putpixel((i*(N*Z+8)+x*Z+dx,y*Z+dy),c)
    im.save(path)
L="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
def export(name, outdir):
    import json, os
    os.makedirs(outdir, exist_ok=True)
    rows=draw(CHARS[name]); pal=palette(name); m={}; P2={}; out=[]
    for r in rows:
        s2=''
        for ch in r:
            if ch=='.': s2+='.'; continue
            c=pal[ch]
            if c not in m: m[c]=L[len(m)]; P2[m[c]]=c
            s2+=m[c]
        out.append(s2)
    open(f'{outdir}/{name}.txt','w').write(chr(10).join(out)+chr(10)); json.dump(P2,open(f'{outdir}/{name}.json','w'))
    Z=8; im=Image.new('RGBA',(N*Z,N*Z),(0,0,0,0)); px=im.load()
    for y,r in enumerate(rows):
        for x,ch in enumerate(r):
            if ch=='.': continue
            c=tuple(int(pal[ch][k:k+2],16) for k in (1,3,5))+(255,)
            for dy in range(Z):
                for dx in range(Z): px[x*Z+dx,y*Z+dy]=c
    im.save(f'{outdir}/{name}.png'); return len(P2)
if __name__=='__main__':
    import sys
    outdir=sys.argv[1]; names=sys.argv[2:] or list(CHARS)
    for n in names: print(n, export(n,outdir),'色')
