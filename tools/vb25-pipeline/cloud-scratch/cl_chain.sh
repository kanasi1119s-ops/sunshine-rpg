#!/bin/bash
# 雲で後ろの曲から書き出す（PC と同じ曲を2回書かないよう、PC の done は見られないので、雲の分は 25→ の順）
cd /home/claude/wt-mix
for n in "$@"; do
  j=/mnt/user-data/outputs/vbq/vb25-$n-v6.json
  [ -f /tmp/vp25/cl/vb25-$n-v6.wav ] && continue
  timeout 2400 node tools/composer/song.mjs build $j --wav $(cat $j.flags) --out /tmp/vp25/cl > /tmp/vp25/cl-$n.log 2>&1
  bash /tmp/vp25/tools/vb_finish.sh /tmp/vp25/cl/vb25-$n-v6.wav 2>&1 | tail -1
  rm -f /tmp/vp25/cl/vb25-$n-v6.wav
done
