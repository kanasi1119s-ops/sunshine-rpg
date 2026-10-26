#!/bin/bash
# PC で書き出した BGM の WAV を仕上げる: vb_pcfin.sh <vb25-NN-slug-vX> <書き出しの曲名>
f=$1; name=$2; w=/mnt/user-data/uploads/sunshine-rpg/pc3/done/$f.wav
for i in 1 2 3 4 5; do [ -s $w ] && break; sleep 3; done
mkdir -p /tmp/vp25/cl; cp $w /tmp/vp25/cl/$f.wav
bash /tmp/vp25/tools/vb_finish.sh /tmp/vp25/cl/$f.wav 2>&1 | tail -1
ffmpeg -v error -y -i /mnt/user-data/outputs/vb25/all/$f.mp3 -af "highshelf=f=5000:g=3.5:t=s:w=0.6,highshelf=f=11000:g=1.5:t=s:w=0.6,alimiter=limit=0.89:level=false" -c:a libmp3lame -b:a 256k "/mnt/user-data/outputs/vb25/all/$name.mp3"
rm -f /tmp/vp25/cl/$f.wav /tmp/vp25/out/$f.wav $w
echo "書き出し: $name"
