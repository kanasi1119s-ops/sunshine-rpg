"""一音一音の表現を測る: 歌（音の出だしのずり上げ・終わりの動き・ビブラート・大きさの形・音どうしの強弱）、和音のシンセ（立ち上がり・のび・明るさの動き・切り方・強弱）、ベース（音のつなぎ方・すべり・形）"""
import numpy as np, librosa, sys, json
SR=44100
def med(a): a=[x for x in a if x is not None and np.isfinite(x)]; return round(float(np.median(a)),2) if a else None
def pct(a,q): a=[x for x in a if x is not None and np.isfinite(x)]; return round(float(np.percentile(a,q)),2) if a else None
def share(a,f): a=[x for x in a if x is not None and np.isfinite(x)]; return round(float(np.mean([f(x) for x in a])),2) if a else None
def f0track(y, lo, hi):
    y2=librosa.resample(y,orig_sr=SR,target_sr=22050); f0,v,_=librosa.pyin(y2,fmin=lo,fmax=hi,sr=22050,frame_length=2048,hop_length=128)
    e=librosa.feature.rms(y=y2,frame_length=1024,hop_length=128)[0][:len(f0)]; return 1200*np.log2(f0/440.0), v, 20*np.log10(e+1e-6), 128/22050
def notes_from(cents, voiced, db, dt, minlen=0.09):
    """高さが半音の6割より大きく動いたら、次の音。声が切れても、次の音"""
    out=[]; s=None; ref=None
    for i in range(len(cents)):
        ok=voiced[i] and np.isfinite(cents[i])
        if ok and s is None: s=i; ref=cents[i]
        elif ok and s is not None:
            m=np.nanmedian(cents[max(s,i-6):i+1])
            if abs(cents[i]-np.nanmedian(cents[s:i]))>60 and abs(m-np.nanmedian(cents[s:max(s+1,i-3)]))>60 and i-s>4:
                if (i-s)*dt>=minlen: out.append((s,i))
                s=i
        elif (not ok) and s is not None:
            if (i-s)*dt>=minlen: out.append((s,i))
            s=None
    return out
for k in (5,):
    z=np.load(f'/tmp/kfbref/cache/ref-user-kfb{k}.stems.npz'); st={a:z[a].astype(np.float32).mean(0) for a in z.files}
    R={}
    # ---- 歌
    c,v,db,dt=f0track(st['vocals'],150,1000); ns=notes_from(c,v,db,dt)
    sc=[];en=[];vib=[];att=[];pk=[];tail=[];lv=[];gap=[];ln=[];drift=[]
    for j,(a,b) in enumerate(ns):
        seg=c[a:b]; L=(b-a)*dt; mid=np.nanmedian(seg[len(seg)//3:]) ; ln.append(L)
        n6=max(2,int(0.06/dt)); sc.append(np.nanmedian(seg[:n6])-mid); en.append(np.nanmedian(seg[-n6:])-mid)
        d=db[a:b]; p=int(np.argmax(d)); pk.append(p/max(1,len(d)-1)); lv.append(float(np.max(d)))
        th=d.max()-3; up=np.where(d>=th)[0]; att.append(up[0]*dt*1000); tail.append((len(d)-1-up[-1])*dt*1000)
        if L>=0.35:
            x=seg[len(seg)//4:]-np.nanmean(seg[len(seg)//4:]); x=np.nan_to_num(x); vib.append(float(np.std(x)))
        if j+1<len(ns): gap.append((ns[j+1][0]-b)*dt)
        drift.append(float(np.nanmedian(seg[-len(seg)//3:])-np.nanmedian(seg[:max(1,len(seg)//3)])))
    dl=np.diff(lv)
    R['歌']={'音の数':len(ns),'長さの中央値(秒)':med(ln),
      '出だしの高さのずれ(セント・中央値)':med(sc),'出だしを下からずり上げる音(−30セントより下)の割合':share(sc,lambda x:x<-30),'出だしを上から入る音(+30より上)の割合':share(sc,lambda x:x>30),'ずり上げる深さ(ずり上げる音の中央値)':med([x for x in sc if x<-30]),
      '終わりで下がる音(−30より下)の割合':share(en,lambda x:x<-30),'終わりで上がる音(+30より上)の割合':share(en,lambda x:x>30),'終わりの下がる深さ(中央値)':med([x for x in en if x<-30]),
      '長い音(0.35秒〜)の高さのゆれ(セント・中央値)':med(vib),'長い音でゆれが25セントより大きい割合':share(vib,lambda x:x>25),
      'いちばん大きくなる位置(0=頭,1=終わり・中央値)':med(pk),'頭がいちばん大きい音(位置0.25より前)の割合':share(pk,lambda x:x<0.25),'あとからふくらむ音(位置0.6より後ろ)の割合':share(pk,lambda x:x>0.6),
      '立ち上がり(ミリ秒・中央値)':med(att),'終わりのしぼみ(ミリ秒・中央値)':med(tail),
      'となりの音との大きさの差(dB・中央値)':med(np.abs(dl)),'差が3dBより大きい割合':share(np.abs(dl),lambda x:x>3),'音の大きさのばらつき(dB・10%〜90%の幅)':round(pct(lv,90)-pct(lv,10),1),
      '次の音までのすき間(秒・中央値)':med(gap),'すき間なし(0.03秒より短い)の割合':share(gap,lambda x:x<0.03),'0.15秒より長い休みの割合':share(gap,lambda x:x>0.15)}
    # ---- ベース
    c,v,db,dt=f0track(st['bass'],30,200); ns=notes_from(c,v,db,dt,0.12)
    sc=[];pk=[];att=[];gap=[];ln=[];glide=[];endl=[]
    for j,(a,b) in enumerate(ns):
        seg=c[a:b]; mid=np.nanmedian(seg[len(seg)//3:]); n6=max(2,int(0.06/dt)); sc.append(np.nanmedian(seg[:n6])-mid); ln.append((b-a)*dt)
        d=db[a:b]; pk.append(int(np.argmax(d))/max(1,len(d)-1)); up=np.where(d>=d.max()-3)[0]; att.append(up[0]*dt*1000); endl.append(float(d[-1]-d.max()))
        if j+1<len(ns):
            g=(ns[j+1][0]-b)*dt; gap.append(g)
            if g<0.03: glide.append(abs(np.nanmedian(c[ns[j+1][0]:ns[j+1][0]+n6])-np.nanmedian(c[ns[j+1][0]+n6:ns[j+1][1]])))
    R['ベース']={'音の数':len(ns),'長さの中央値(秒)':med(ln),'出だしの高さのずれ(セント・中央値)':med(sc),'出だしが上から落ちてくる音(+40より上)の割合':share(sc,lambda x:x>40),'下からすべり上がる音(−40より下)の割合':share(sc,lambda x:x<-40),
      'つながった音のうち、すべって移る(出だしのずれ40セントより大きい)割合':share(glide,lambda x:x>40),'すき間なしの割合':share(gap,lambda x:x<0.03),'0.15秒より長い休みの割合':share(gap,lambda x:x>0.15),
      '立ち上がり(ミリ秒・中央値)':med(att),'いちばん大きくなる位置(中央値)':med(pk),'終わりの大きさ(頭の山からのdB・中央値)':med(endl)}
    # ---- 和音のシンセ
    y=st['other']+st['guitar']+st['piano']; hop=256; e=librosa.feature.rms(y=y,frame_length=1024,hop_length=hop)[0]; d=20*np.log10(e+1e-6)
    on=librosa.onset.onset_detect(y=y,sr=SR,hop_length=hop,backtrack=True,delta=0.12,wait=int(0.1*SR/hop)); S_=np.abs(librosa.stft(y,n_fft=2048,hop_length=hop)); fr=librosa.fft_frequencies(sr=SR,n_fft=2048)
    cen=(S_*fr[:,None]).sum(0)/(S_.sum(0)+1e-9); dt2=hop/SR
    att=[];sus=[];cmov=[];lv=[];ioi=[];gate=[];pk=[]
    for j in range(len(on)-1):
        a,b=on[j],on[j+1]; L=(b-a)*dt2
        if L<0.1 or d[a:b].max()<np.percentile(d,40): continue
        seg=d[a:b]; p=int(np.argmax(seg)); att.append(p*dt2*1000); pk.append(p/max(1,len(seg)-1)); lv.append(float(seg.max())); ioi.append(L)
        sus.append(float(seg[min(len(seg)-1,p+int(0.5*(len(seg)-p)))]-seg.max()))
        below=np.where(seg[p:]<seg.max()-12)[0]; gate.append(((p+below[0]) if len(below) else len(seg))/len(seg))
        c0=np.median(cen[a:a+max(2,len(seg)//5)]); c1=np.median(cen[a+len(seg)*2//5:a+len(seg)*3//5+1]); c2=np.median(cen[b-max(2,len(seg)//5):b]); cmov.append((12*np.log2(c1/c0),12*np.log2(c2/c1)))
    R['和音のシンセ']={'音の数':len(att),'音の間かく(秒・中央値)':med(ioi),'立ち上がり(山までのミリ秒・中央値)':med(att),'立ち上がりが60ミリ秒より遅い(ふくらむ)音の割合':share(att,lambda x:x>60),
      'まん中での大きさ(山からのdB・中央値)':med(sus),'すぐ減る音(−6dBより下)の割合':share(sus,lambda x:x<-6),'のびる音(−2dBより上)の割合':share(sus,lambda x:x>-2),
      '鳴っている長さ／次の音までの長さ(中央値)':med(gate),'短く切る音(0.6より短い)の割合':share(gate,lambda x:x<0.6),
      '明るさの動き: 頭→まん中(半音・中央値)':med([x[0] for x in cmov]),'頭より明るくなる音(+2半音より上)の割合':share([x[0] for x in cmov],lambda x:x>2),'頭より暗くなる音(−2より下)の割合':share([x[0] for x in cmov],lambda x:x<-2),
      '明るさの動き: まん中→終わり(半音・中央値)':med([x[1] for x in cmov]),'となりの音との大きさの差(dB・中央値)':med(np.abs(np.diff(lv))),'音の大きさのばらつき(dB・10%〜90%の幅)':round(pct(lv,90)-pct(lv,10),1)}
    json.dump(R,open(f'/tmp/kfbref/notes{k}.json','w'),ensure_ascii=False,indent=1); print(f"曲{k} できた", flush=True)
