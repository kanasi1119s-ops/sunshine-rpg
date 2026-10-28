#!/bin/bash
# 歌の版の書き出しを順番に（同時に2本まで）。/tmp/vp25/cq.txt に「JSONの名前|書き出しの曲名」を1行ずつ足す
Q=/tmp/vp25/cq.txt; DONE=/tmp/vp25/cq.done; touch $Q $DONE
while true; do
  [ -f /tmp/vp25/cq.stop ] && exit 0
  n=$(ps -eo args | grep -c "^node tools/composer/[s]ong.mjs build")
  if [ "$n" -lt 2 ]; then
    line=$(grep -vxF -f $DONE $Q | head -1)
    if [ -n "$line" ]; then
      echo "$line" >> $DONE
      f=${line%%|*}; t=${line#*|}
      nohup /tmp/vp25/tools/vb_render.sh "$f" "$t" >> /tmp/vp25/cq.log 2>&1 &
      sleep 20; continue
    fi
  fi
  sleep 30
done
