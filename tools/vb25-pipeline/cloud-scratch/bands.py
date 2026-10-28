import sys,subprocess,numpy as np
for f in sys.argv[1:]:
    d=subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","22050","-f","f32le","-"],capture_output=True).stdout
    x=np.frombuffer(d,np.float32); sr=22050
    w=44100; segs=[x[i:i+w] for i in range(0,len(x)-w,w)]
    e=np.array([np.mean(s**2) for s in segs]); idx=np.argsort(e)[-int(len(e)*0.4):]
    S=np.zeros(w//2+1)
    for i in idx: S+=np.abs(np.fft.rfft(segs[i]*np.hanning(w)))**2
    fr=np.fft.rfftfreq(w,1/22050); b=lambda a,c: round(10*np.log10(S[(fr>=a)&(fr<c)].sum()/S.sum()),1)
    r=lambda a,c: round(20*np.log10(np.sqrt(np.mean(x[int(a*sr):int(c*sr)]**2))+1e-9),1)
    print(f.split('/')[-1][:30], " 40-100:",b(40,100)," 100-250:",b(100,250)," 250-600:",b(250,600)," 600-1.5k:",b(600,1500)," 1.5-3k:",b(1500,3000)," 3-6k:",b(3000,6000), " 6k+:",b(6000,11000), "| intro3s:", [r(t,t+3) for t in range(0,15,3)])
