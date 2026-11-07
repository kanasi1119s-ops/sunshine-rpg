# 2026-11-07 プロの弦の奏法（スピッカート・トレモロ）の SFZ を作る。VSCO 2 CE（CC0）の Strings を /tmp/vsco に置いて実行 → /tmp/strart/{spic,trem}/*.sfz
# そのあと: node tools/soundfont/sfz-to-sf3.mjs /tmp/strart/spic/spic.sfz strings-spiccato-vsco --program 189 --seconds 1.6 --rr 2 --fade 0.2 --release 0.25
#          node tools/soundfont/sfz-to-sf3.mjs /tmp/strart/trem/trem.sfz strings-tremolo-vsco --program 190 --seconds 5 --rr 1 --loop --fade 0.3 --release 0.45
# 音名はファイル名（VSCO は1オクターブ低く書かれている）を基準にし、録音から測ったずれ（パートごとの最頻値）でオクターブを直す。強さの層が1つしかない音は全部の強さで鳴らす
import os, re, sys, glob, numpy as np, soundfile as sf, pyworld as pw, subprocess
SRC="/tmp/vsco/Strings"; OUT="/tmp/strart"
ART={"spic":{"Violin":"Violin Section/Spic","Viola":"Viola Section/spic","Cello":"Cello Section/spic"},
     "trem":{"Violin":"Violin Section/Trem","Viola":"Viola Section/trem","Cello":"Cello Section/trem"}}
SPLIT={"Cello":(0,54),"Viola":(55,66),"Violin":(67,127)}
def load(f):
    x,sr=sf.read(f,always_2d=True); x=x.mean(1)
    if sr!=44100:
        import scipy.signal as ss; x=ss.resample_poly(x,44100,sr); sr=44100
    return x.astype(np.float64),sr
def f0midi(x,sr):
    seg=x[int(0.05*sr):int(1.0*sr)]
    if len(seg)<sr*0.2: seg=x
    f0,t=pw.harvest(seg,sr,f0_floor=50,f0_ceil=2000,frame_period=10)
    f0=f0[f0>0]
    return None if len(f0)<3 else 69+12*np.log2(np.median(f0)/440)
for art,dirs in ART.items():
    od=f"{OUT}/{art}"; os.makedirs(od,exist_ok=True)
    regions=[]
    for sec,d in dirs.items():
        items=[]; meas=[]
        for f in sorted(glob.glob(f"{SRC}/{d}/*.wav")):
            b=os.path.basename(f); v=re.search(r"_v(\d)",b); v=int(v.group(1)) if v else 2
            rr=re.search(r"(?:rr|RR|_)(\d)\.wav$",b); rr=int(rr.group(1)) if rr else 1
            x,sr=load(f)
            # 先頭の無音を切る
            th=np.max(np.abs(x))*0.02; i0=int(np.argmax(np.abs(x)>th)); x=x[max(0,i0-int(0.004*sr)):]
            nm_=re.search(r"_([A-G])(#|b)?(-?\d)_",b); PCN={"C":0,"D":2,"E":4,"F":5,"G":7,"A":9,"B":11}
            nom=12*(int(nm_.group(3))+1)+PCN[nm_.group(1)]+(1 if nm_.group(2)=="#" else -1 if nm_.group(2)=="b" else 0)
            m=f0midi(x,sr)
            meas.append((m-nom) if m is not None else None)
            root=nom; cents=0
            maxs=1.6 if art=="spic" else 5.0; x=x[:int(maxs*sr)]
            a=int(0.02*sr); b2=min(len(x),int((0.3 if art=="spic" else 1.4)*sr))
            r=np.sqrt(np.mean(x[a:b2]**2))+1e-9; tgt=0.06 if v==1 else 0.085
            x=x*min(tgt/r,0.97/np.max(np.abs(x)))
            n=len(x); fl=int(0.25*sr) if art=="spic" else int(0.05*sr)
            x[n-fl:]*=np.linspace(1,0,fl)
            ls=le=None
            if art=="trem" and n>sr*2:
                le=n-int(0.06*sr); ls=int(n*0.4); X=int(0.3*sr)
                for k in range(X):
                    t=k/X; x[le-X+k]=x[le-X+k]*np.cos(t*np.pi/2)+x[ls-X+k]*np.sin(t*np.pi/2)
            fn=f"{sec}_{root}_v{v}_rr{rr}.wav"; sf.write(f"{od}/{fn}",x.astype(np.float32),sr,subtype="PCM_16")
            items.append((root,v,rr,fn,cents,ls,le))
        offs=[round(d) for d in meas if d is not None]; off=max(set(offs),key=offs.count)
        fixed=[]
        for (root,v,rr,fn,cents,ls,le),d in zip(items,meas):
            c=0
            if d is not None and abs(d-off)<0.5: c=int(round((off-d)*100))
            fixed.append((root+off,v,rr,fn,c,ls,le))
        items=fixed; print(sec,"オクターブのずれ",off)
        roots=sorted({i[0] for i in items}); lo,hi=SPLIT[sec]
        vs={}
        for it in items: vs.setdefault(it[0],set()).add(it[1])
        for root,v,rr,fn,cents,ls,le in items:
            k=roots.index(root)
            a=lo if k==0 else int(np.ceil((roots[k-1]+root)/2+0.01)); bb=hi if k==len(roots)-1 else (root+roots[k+1])//2
            a=max(a,lo); bb=min(bb,hi)
            if a>bb: continue
            vel="lovel=1 hivel=127" if len(vs[root])==1 else ("lovel=1 hivel=90" if v==1 else "lovel=91 hivel=127")
            rrs="" if art=="trem" else f" seq_length=2 seq_position={rr}"
            loop=f" loop_mode=loop_continuous loop_start={ls} loop_end={le}" if ls else ""
            regions.append(f"<region> sample={fn} lokey={a} hikey={bb} pitch_keycenter={root} tune={cents} {vel}{rrs}{loop}")
        print(art,sec,"音域",roots)
    open(f"{od}/{art}.sfz","w").write("\n".join(regions)+"\n")
    print(art,len(regions),"領域")
