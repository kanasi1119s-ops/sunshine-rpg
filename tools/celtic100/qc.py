import sys, numpy as np, soundfile as sf
x, sr = sf.read(sys.argv[1], dtype='float32'); x = x.mean(1) if x.ndim > 1 else x
w = int(sr*4); n = len(x)//w
r = np.array([20*np.log10(np.sqrt(np.mean(x[i*w:(i+1)*w]**2))+1e-9) for i in range(n)])
steps = np.abs(np.diff(r)); med = np.median(r)
print(f"長さ{len(x)/sr:.0f}秒 中央値{med:.1f}dB 前奏(0-12s)平均{r[:3].mean():.1f}dB 最大段差{steps.max():.1f}dB(@{4*(steps.argmax()+1)}秒) 山{r.max():.1f} 谷(終わり除く){r[:-3].min():.1f}")
flag=[]
if r[:3].mean() < med-5: flag.append("前奏が小さい")
if steps[:-3].max() > 7: flag.append("段差大")
if r[:-3].max()-r[:-3].min() < 3: flag.append("強弱が少ない")
print("注意:", flag or "なし")
import numpy as np
seg=x[:sr*240]; seg=seg[:len(seg)//sr*sr]  # 1秒の整数倍に切る（半端だと reshape が落ちる）
S=np.abs(np.fft.rfft(seg.reshape(-1,sr)*np.hanning(sr)[None,:],axis=1)).mean(0)
f=np.fft.rfftfreq(sr,1/sr); cen=(f*S).sum()/S.sum(); hi=10*np.log10((S[(f>4000)&(f<12000)]**2).sum()/(S**2).sum())
print(f"明るさの重心{cen:.0f}Hz 4k-12k比{hi:.1f}dB")
