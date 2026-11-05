#!/bin/bash
# 前回（SCARLET FREQUENCY の ig.sh）と同じ作り: 各曲の 0:50 から 60秒・縦1080×1920・24コマ
OUT="/tmp/ig/SECOND SIGNAL Instagram用"
for n in "$@"; do
  jp=$(awk -F'\t' -v n=$n '$1==n{print $2}' /tmp/yt2/songs.tsv)
  f="$OUT/$n $jp（Instagram）.mp4"; [ -s "$f" ] && continue
  [ -f /tmp/yt2/out/$n.done ] || { echo "まだ $n"; continue; }
  ffmpeg -nostdin -y -v error -ss 50 -t 60 -i /tmp/yt2/out/$n.mp4 -filter_complex \
   "[0:v]split=3[a][b][c];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,scale=108:192,boxblur=3:1,scale=1080:1920,eq=brightness=-0.15[bg];[b]crop=889:951:71:60,scale=-2:880[p];[c]crop=960:1080:960:0,scale=-2:880[t];[bg][p]overlay=(W-w)/2:100[x];[x][t]overlay=(W-w)/2:980,fade=t=in:d=0.6,fade=t=out:st=59.2:d=0.8[v];[0:a]afade=t=in:d=0.6,afade=t=out:st=58.5:d=1.5[a]" \
   -map "[v]" -map "[a]" -c:v libx264 -preset veryfast -crf 23 -r 24 -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart "$f.tmp.mp4" && mv "$f.tmp.mp4" "$f" && echo "ok $n $jp"
done
