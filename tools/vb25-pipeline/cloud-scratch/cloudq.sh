#!/bin/bash
# クラウドの書き出しの列（/tmp/vp25/cq.txt の「番号」を上から）。ほかの書き出しが終わってから1つずつ
cd /home/claude/wt-mix/assets-src/ai-songs/_gen
while true; do
  while ps -eo args | grep -q "^node tools/composer/song.mjs build"; do sleep 20; done
  n=$(head -1 /tmp/vp25/cq.txt 2>/dev/null); [ -z "$n" ] && { sleep 30; [ -s /tmp/vp25/cq.txt ] || exit 0; continue; }
  sed -i 1d /tmp/vp25/cq.txt
  bash vp25_render.sh vp25_${n}_*.py 2>&1 | tail -1 >> /tmp/vp25/cloudq.log
done
