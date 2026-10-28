#!/bin/bash
# 実験の列: 引数の JSON を順に書き出して採点（ほかの書き出しが終わってから）
cd /home/claude/wt-mix
FL="$1"; shift
for j in "$@"; do
  while ps -eo args | grep -q "^node tools/composer/song.mjs build"; do sleep 15; done
  timeout 1200 node tools/composer/song.mjs build "$j" --wav $FL --out /tmp/vp25/xc > /tmp/vp25/xc/$(basename $j .json).log 2>&1
  bash /tmp/vp25/tools/pq.sh /tmp/vp25/xc/$(basename $j .json).wav >> /tmp/vp25/xc/pq.txt
done
