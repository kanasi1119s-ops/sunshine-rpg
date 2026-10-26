#!/bin/bash
# 使い方: vb_render.sh <JSONの名前（vb25-NN-slug-vX）> <書き出しの曲名（例: 02 サイダーカウントダウン（歌：重音テト・仮）v4）>
cd /home/claude/wt-mix
f=$1; name=$2; j=/mnt/user-data/outputs/vbq/$f.json
timeout 3600 node tools/composer/song.mjs build $j --wav $(cat $j.flags) --out /tmp/vp25/cl > /tmp/vp25/cl-$f.log 2>&1
grep -A3 "^×" /tmp/vp25/cl-$f.log | head -4
if grep -q "^×" /tmp/vp25/cl-$f.log || [ ! -f /tmp/vp25/cl/$f.wav ]; then echo "× 書き出し失敗（送らない）: $name"; sed -i "/^$f|/d" /tmp/vp25/cq.done; exit 1; fi   # 失敗した書き出しは仕上げない（歌なしの版ができてしまうため）。待ち行列に戻す
bash /tmp/vp25/tools/vb_finish.sh /tmp/vp25/cl/$f.wav 2>&1 | tail -1
case "$f" in *vo) af="highshelf=f=5000:g=2:t=s:w=0.6,alimiter=limit=0.89:level=false";; *) af="highshelf=f=5000:g=3.5:t=s:w=0.6,highshelf=f=11000:g=1.5:t=s:w=0.6,alimiter=limit=0.89:level=false";; esac
ffmpeg -v error -y -i /mnt/user-data/outputs/vb25/all/$f.mp3 -af "$af" -c:a libmp3lame -b:a 256k "/mnt/user-data/outputs/vb25/all/$name.mp3"
rm -f /tmp/vp25/cl/$f.wav /tmp/vp25/out/$f.wav
echo "書き出し: $name"
