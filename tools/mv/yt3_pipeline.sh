#!/bin/bash
# 第3弾 HUMMING RELAY: 舞台の動画（YouTube 用・1曲ずつ）と、Instagram 用（各曲の 0:50 から 60秒・縦）を作り、置き場へ移す
# （第2弾の yt2_render_all.sh ＋ ig_second_signal.sh と同じ作り。2026-11-08 人間「こないだの25曲の動画もいつもと同じように頼むね」）
# 作業場所の容量が少ないので、1曲できるたびに置き場（/mnt/user-data/outputs/humming_relay）へ移して、手元のものは消す
cd /home/claude/wt-mix
DST=/mnt/user-data/outputs/humming_relay; mkdir -p "$DST/YouTube用（1曲ずつ）" "$DST/Instagram用" /tmp/yt3/out
while IFS=$'\t' read no b a; do
  [ -f "$DST/.done_$no" ] && continue
  [ -f /tmp/yt3/stop ] && break
  jp=$(awk -F'\t' -v n=$no '$1==n{print $2}' /tmp/yt3/songs.tsv)
  echo "== $no $jp $(date +%H:%M)"
  MV_ALBUM_J="ハミング・リレー" MV_ALBUM_E="HUMMING RELAY" MV_KANA=/mnt/user-data/outputs/vbq/$b.json.kana MV_EN=/tmp/yt3/en/$no.json MV_SMOOTH=1 MV_FPS=48 nice -n 5 \
    python3 tools/mv/stage_mv.py $no /tmp/yt3/songs.tsv "$a" /mnt/user-data/outputs/vbq/$b.json /tmp/vp25/cl/$b-vocal.ust /tmp/yt3/seq/$no.mp4.seq.json /tmp/yt2/tm /tmp/yt2/stage.png /tmp/yt3/out/$no.mp4 2>&1 | grep -v -i "warn\|pkg_res" | tail -2
  vd=$(ffprobe -v error -show_entries format=duration -of csv=p=0 /tmp/yt3/out/$no.mp4); ad=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$a")
  python3 -c "import sys;sys.exit(0 if abs(float('${vd:-0}')-float('$ad'))<0.6 else 1)" || { echo "× $no 長さがちがう（映像 $vd・音 $ad）"; continue; }
  # Instagram 用（前回と同じ: 0:50 から 60秒・縦1080×1920・歌詞ボードと舞台のテトを上下に）
  ig="/tmp/yt3/out/$no.ig.mp4"
  ffmpeg -nostdin -y -v error -ss 50 -t 60 -i /tmp/yt3/out/$no.mp4 -filter_complex \
   "[0:v]split=3[a][b][c];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,scale=108:192,boxblur=3:1,scale=1080:1920,eq=brightness=-0.15[bg];[b]crop=889:951:71:60,scale=-2:880[p];[c]crop=960:1080:960:0,scale=-2:880[t];[bg][p]overlay=(W-w)/2:100[x];[x][t]overlay=(W-w)/2:980,fade=t=in:d=0.6,fade=t=out:st=59.2:d=0.8[v];[0:a]afade=t=in:d=0.6,afade=t=out:st=58.5:d=1.5[a]" \
   -map "[v]" -map "[a]" -c:v libx264 -preset veryfast -crf 23 -r 24 -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart "$ig" || { echo "× $no インスタ用"; continue; }
  if cp /tmp/yt3/out/$no.mp4 "$DST/YouTube用（1曲ずつ）/$no $jp.mp4" && cp "$ig" "$DST/Instagram用/$no $jp（Instagram）.mp4"; then
    cp /tmp/yt3/out/$no.mp4.lyrics.json "$DST/YouTube用（1曲ずつ）/.$no.lyrics.json" 2>/dev/null
    rm -f /tmp/yt3/out/$no.mp4 "$ig"; touch "$DST/.done_$no"; echo "ok $no"
  else echo "× $no 置き場へ移せない"; fi
done < /tmp/yt3/songs.txt
echo ALL_DONE $(date +%H:%M)
