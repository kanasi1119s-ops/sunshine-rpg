# 使い方: python3 -I tools/soundfont/gen-vcsl-sfz.py ROOT OUTNAME "ファイル名の正規表現" "音名の正規表現(group1)" "強さ層の正規表現(group1)か-" 層1,層2,...|- [オクターブ補正]
# VCSL（CC0）の WAV 一式から、sfz-to-sf3.mjs に渡す SFZ を作る。音名のオクターブは実測で補正する（VCSL の名前は 1〜2 オクターブ低い）。各ファイルの最大音量を測り、層ごとに -2dB（層が下がるごとに -5dB）へそろえる volume を付ける。
import re,sys,os,subprocess
root,out,fre,nre,lre,layers=sys.argv[1:7]
off=int(sys.argv[7]) if len(sys.argv)>7 else 0
N={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def num(n):
    m=re.match(r'([A-G])(#?)(-?\d)$',n); return 12*(int(m[3])+1+off)+N[m[1]]+(1 if m[2] else 0)
files=[]
for dp,dn,fn in os.walk(root):
    for f in fn:
        if f.endswith('.wav'):
            rel=os.path.relpath(os.path.join(dp,f),root)
            if re.search(fre,rel): files.append(rel)
layers=layers.split(',') if layers!='-' else ['all']
bylayer={l:{} for l in layers}
for rel in sorted(files):
    b=os.path.basename(rel)
    nm=re.search(nre,b)
    if not nm: continue
    n=num(nm[1])
    if lre=='-': l='all'
    else:
        lm=re.search(lre,rel)
        if not lm or lm[1] not in bylayer: continue
        l=lm[1]
    bylayer[l].setdefault(n,[]).append(rel)
def vol(p):
    o=subprocess.run(['ffmpeg','-i',p,'-af','volumedetect','-f','null','-'],capture_output=True,text=True).stderr
    m=re.search(r'max_volume: (-?[\d.]+) dB',o); return float(m[1]) if m else 0.0
L=len(layers); lines=[]
for i,l in enumerate(layers):
    lo=1 if i==0 else round(127*i/L)+1; hi=127 if i==L-1 else round(127*(i+1)/L)
    ns=sorted(bylayer[l])
    for j,n in enumerate(ns):
        lk=0 if j==0 else (ns[j-1]+n)//2+1
        hk=127 if j==len(ns)-1 else (n+ns[j+1])//2
        for rel in bylayer[l][n]:
            mv=vol(os.path.join(root,rel)); g=(-2-5*(L-1-i))-mv; g=max(-6,min(45,g))
            lines.append(f"<region> sample={rel} pitch_keycenter={n} lokey={lk} hikey={hk} lovel={lo} hivel={hi} volume={g:.1f}")
open(os.path.join(root,out+'.sfz'),'w').write('\n'.join(lines)+'\n')
print(out,len(lines),'regions',[(l,len(bylayer[l])) for l in layers])
