#!/bin/bash
# 使い方: chk.sh 006  … 点数・検査・2秒ごとの大きさ
N=$1
tail -n1 /tmp/cel/w/pq$N.log; tail -n3 /tmp/cel/w/qc$N.log | head -2
python3 -c "
import numpy as np, soundfile as sf
x,sr=sf.read('/tmp/cel/out/c$N.final.wav'); x=x.mean(1); w=sr*2; n=len(x)//w
r=[round(20*np.log10(np.sqrt(np.mean(x[i*w:(i+1)*w]**2))+1e-9)) for i in range(n)]
print(r)
import statistics; m=statistics.median(r[3:-6])
print('急に小さい所(中央値-9dB以下・前奏と終わり除く):',[(2*i,v) for i,v in enumerate(r) if 3<=i<len(r)-6 and v<m-9])"
