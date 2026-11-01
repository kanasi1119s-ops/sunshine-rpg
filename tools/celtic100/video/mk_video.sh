#!/bin/bash
# 「銀の笛と百の夜」全100曲の動画を作る（2026-11-02）。PC の Downloads/銀の笛と百の夜/動画用/ に置いて、PC の中で動かす。
#   曲のあいだに2秒の無音。20秒のループ映像（anim.py で作った loop.mp4）を全体の長さまでくり返す。
# 出力: 動画用/銀の笛と百の夜.mp4・starts.txt（各曲の開始秒。mk_desc.py に渡す）・total.txt（全体の秒）
set -e
D="$HOME/mnt/Downloads/銀の笛と百の夜"; V="$D/動画用"; W="$HOME/vidwork"; mkdir -p "$W"; cd "$D"
ffmpeg -v error -y -f lavfi -i anullsrc=r=44100:cl=stereo -t 2 -c:a pcm_s16le "$W/gap.wav"
: > "$W/list.txt"; : > "$V/starts.txt"; t=0; i=0
for n in $(seq -f %03g 1 100); do
  f=$(ls ${n}_*.mp3 | head -1); d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  echo "$t" >> "$V/starts.txt"
  echo "file '$D/$f'" >> "$W/list.txt"; t=$(python3 -c "print($t+$d)")
  if [ $n != 100 ]; then echo "file '$W/gap.wav'" >> "$W/list.txt"; t=$(python3 -c "print($t+2)"); fi
done
echo "$t" > "$V/total.txt"
ffmpeg -v error -y -f concat -safe 0 -i "$W/list.txt" -c:a aac -b:a 192k "$W/audio.m4a"
ffmpeg -v error -y -stream_loop -1 -i "$V/loop.mp4" -i "$W/audio.m4a" -map 0:v -map 1:a -c:v copy -c:a copy -shortest -movflags +faststart "$W/out.mp4"
mv "$W/out.mp4" "$V/銀の笛と百の夜.mp4"
touch "$V/done.txt"
