#!/bin/bash
# 仕上げだけやり直す（場面ごとの大きさ .gain を変えたとき）。使い方: v3_refinish.sh <スクリプト> <slug> <版> "<NN 曲名>"
#   .gain を書き直すために曲のスクリプトをもう一度走らせ（JSON は同じ内容で上書き）、残してある仕上げ前の音（/tmp/vp25/raw/*.flac）から仕上げる
cd /home/claude/wt-mix/assets-src/ai-songs/_gen
VB_VOCAL=1 python3 $1 /mnt/user-data/outputs/vbq/$2-$3vo.json > /dev/null 2>&1; python3 $1 /mnt/user-data/outputs/vbq/$2-$3.json > /dev/null 2>&1
cd /home/claude/wt-mix
for suf in vo ""; do f=$2-$3$suf
  [ -f /tmp/vp25/raw/$f.flac ] || { echo "仕上げ前の音がない: $f"; continue; }
  mkdir -p /tmp/vp25/cl; ffmpeg -v error -y -i /tmp/vp25/raw/$f.flac /tmp/vp25/cl/$f.wav
  bash /tmp/vp25/tools/v3_finish.sh /tmp/vp25/cl/$f.wav 2>&1 | tail -1
  if [ "$suf" = "vo" ]; then nm="$4（歌：重音テト・仮）$3"; af="highshelf=f=5000:g=2:t=s:w=0.6,alimiter=limit=0.89:level=false"; else nm="$4（BGM・仮）$3"; af="highshelf=f=5000:g=3.5:t=s:w=0.6,highshelf=f=11000:g=1.5:t=s:w=0.6,alimiter=limit=0.89:level=false"; fi
  ffmpeg -v error -y -i /mnt/user-data/outputs/vt3/all/$f.mp3 -af "$af" -c:a libmp3lame -b:a 256k "/mnt/user-data/outputs/vt3/all/$nm.mp3"
  rm -f /tmp/vp25/cl/$f.wav /tmp/vp25/out/$f.wav
done
python3 /tmp/vp25/tools/v3_check.py $2 $3 "$4"
