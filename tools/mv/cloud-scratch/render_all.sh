#!/bin/bash
# 舞台の動画を1曲ずつ書き出し、PC に送れる大きさ（30MB 未満）に切り分ける
cd /home/claude/wt-mix
while read slug v; do no=${slug%%_*}; s=${slug#*_}; jv=$v; [ $no = 02 ] && jv=v26
  [ -n "$ONLY" ] && [ "$ONLY" != "$no" ] && continue
  case " $SKIP " in *" $no "*) continue;; esac
  [ -f /tmp/yt/parts/$no.done ] && continue
  while [ ! -f /tmp/yt/seq/$no.mp4.seq.json ]; do sleep 20; done
  until ls "/mnt/user-data/outputs/vb25/all/" | grep -F "$no " | grep -qF "（歌：重音テト・仮）$v.mp3"; do sleep 30; done
  b=vb25-$no-$s-${jv}vo; A=$(ls "/mnt/user-data/outputs/vb25/all/" | grep -F "$no " | grep -F "（歌：重音テト・仮）$v.mp3" | head -1)
  echo "== $no $A $(date +%H:%M)"
  while [ ! -f /tmp/yt/en/$no.json ]; do sleep 20; done
  MV_EN=/tmp/yt/en/$no.json nice -n 5 python3 tools/mv/stage_mv.py $no /tmp/yt/songs.tsv "/mnt/user-data/outputs/vb25/all/$A" /mnt/user-data/outputs/vbq/$b.json /tmp/vp25/cl/$b-vocal.ust /tmp/yt/seq/$no.mp4.seq.json /tmp/yt/tm /tmp/yt/stage.png /tmp/yt/out/$no.mp4 2>&1 | grep -v Warning | grep -v "^ok" | tail -3
  vd=$(ffprobe -v error -select_streams v -show_entries stream=duration -of csv=p=0 /tmp/yt/out/$no.mp4); ad=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "/mnt/user-data/outputs/vb25/all/$A")
  python3 -c "import sys;sys.exit(0 if abs(float(\"${vd:-0}\")-float(\"$ad\"))<0.6 else 1)" || { echo "× $no 失敗（映像 $vd 秒・音 $ad 秒）"; continue; }
  ffmpeg -nostdin -v error -i /tmp/yt/out/$no.mp4 -c copy -map 0 -f segment -segment_time 70 -reset_timestamps 1 /tmp/yt/parts/${no}_%02d.mp4 && touch /tmp/yt/parts/$no.done
  ls -la /tmp/yt/parts/${no}_* | awk '{print $5, $9}'
done < /tmp/yt/songs.txt
echo 全部おわり $(date +%H:%M)
