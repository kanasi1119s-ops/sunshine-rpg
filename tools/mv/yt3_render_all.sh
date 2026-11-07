#!/bin/bash
# 第3弾 HUMMING RELAY: 舞台の動画を1曲ずつ書き出す（第2弾 yt2_render_all.sh と同じ作り）
cd /home/claude/wt-mix
while IFS=$'\t' read no b a; do
  [ -f /tmp/yt3/out/$no.done ] && continue
  [ -f /tmp/yt3/stop ] && break
  echo "== $no $(date +%H:%M)"
  MV_ALBUM_J="ハミング・リレー" MV_ALBUM_E="HUMMING RELAY" MV_KANA=/mnt/user-data/outputs/vbq/$b.json.kana MV_EN=/tmp/yt3/en/$no.json MV_SMOOTH=1 MV_FPS=48 nice -n 5 python3 tools/mv/stage_mv.py $no /tmp/yt3/songs.tsv "$a" /mnt/user-data/outputs/vbq/$b.json /tmp/vp25/cl/$b-vocal.ust /tmp/yt3/seq/$no.mp4.seq.json /tmp/yt2/tm /tmp/yt2/stage.png /tmp/yt3/out/$no.mp4 2>&1 | grep -v -i "warn\|pkg_res" | tail -2
  vd=$(ffprobe -v error -show_entries format=duration -of csv=p=0 /tmp/yt3/out/$no.mp4); ad=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$a")
  python3 -c "import sys;sys.exit(0 if abs(float('${vd:-0}')-float('$ad'))<0.6 else 1)" && touch /tmp/yt3/out/$no.done || echo "× $no 長さがちがう（映像 $vd・音 $ad）"
done < /tmp/yt3/songs.txt
echo ALL_DONE $(date +%H:%M)
