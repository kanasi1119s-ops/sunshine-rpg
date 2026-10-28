#!/bin/bash
# 使い方: cl_rt.sh <番号-名前> <元の版> <新しい版>  … 参考の音を足して雲で書き出し→低域の掃除→仕上げ
Q=/mnt/user-data/outputs/vpq
for spec in "$@"; do
  IFS=: read n src dst <<<"$spec"
  for e in "" .fade .meta; do [ -f $Q/vp25-$n-$src.json$e ] && cp $Q/vp25-$n-$src.json$e $Q/vp25-$n-$dst.json$e; done
  f=$(cat $Q/vp25-$n-$src.json.flags); [[ "$f" == *ref-tone* ]] || f="$f --ref-tone glossy-jrock"; echo "$f" > $Q/vp25-$n-$dst.json.flags
  cd /home/claude/wt-mix && timeout 1800 node tools/composer/song.mjs build $Q/vp25-$n-$dst.json --wav $f --out /tmp/vp25/cl > /tmp/vp25/cl-$n.log 2>&1
  python3 - /tmp/vp25/cl/vp25-$n-$dst.wav /tmp/vp25/hp/vp25-$n-$dst.wav <<'P'
import sys, soundfile as sf, numpy as np
from scipy.signal import butter, sosfiltfilt
d,sr=sf.read(sys.argv[1]); st=sf.info(sys.argv[1]).subtype
d=d-d.mean(0); y=sosfiltfilt(butter(2,24,'hp',fs=sr,output='sos'),d,axis=0)
pk=np.abs(y).max(); y=y*(0.97/pk) if pk>0.97 else y
sf.write(sys.argv[2],y,sr,subtype=st)
P
  rm -f /tmp/vp25/cl/vp25-$n-$dst.wav; bash /tmp/vp25/tools/vp_finish.sh /tmp/vp25/hp/vp25-$n-$dst.wav 2>&1 | tail -1; rm -f /tmp/vp25/hp/vp25-$n-$dst.wav
done
