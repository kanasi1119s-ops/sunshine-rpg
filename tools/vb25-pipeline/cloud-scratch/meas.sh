#!/bin/bash
# 使い方: meas.sh 01 04 ...（lm25v3 の mp3 を測る）
cd /mnt/user-data/outputs/vp25
for n in "$@"; do f=$(ls "$n "*.mp3); echo "$f"; python3 - "$f" <<'E'
import sys,subprocess,numpy as np
d=subprocess.run(["ffmpeg","-v","error","-i",sys.argv[1],"-ac","1","-ar","22050","-f","f32le","-"],capture_output=True).stdout
x=np.frombuffer(d,np.float32); sr=22050
r=lambda a,b: float(round(20*np.log10(np.sqrt(np.mean(x[int(a*sr):int(b*sr)]**2))+1e-9),1))
print(" 全体",r(0,len(x)/sr),"| 3秒:",[r(t,t+3) for t in range(0,24,3)])
w=44100; segs=[x[i:i+w] for i in range(0,len(x)-w,w)]
e=np.array([np.mean(s**2) for s in segs]); idx=np.argsort(e)[-int(len(e)*0.4):]
S=np.zeros(w//2+1)
for i in idx: S+=np.abs(np.fft.rfft(segs[i]*np.hanning(w)))**2
fr=np.fft.rfftfreq(w,1/22050); b=lambda a,c: round(10*np.log10(S[(fr>=a)&(fr<c)].sum()/S.sum()),1)
print(" 帯域 40-100:",b(40,100)," 100-250:",b(100,250)," 600-1.5k:",b(600,1500)," 2-5k:",b(2000,5000))
E
done
