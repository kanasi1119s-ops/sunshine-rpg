#!/bin/bash
cd /home/claude/wt-mix
for k in "$@"; do
  j=/tmp/vp25/xc/vp00x-09k$k.json
  while ps -eo args | grep -q "^node tools/composer/song.mjs build"; do sleep 15; done
  timeout 1200 node tools/composer/song.mjs build "$j" --wav --drums $k --bass bnb-loud --master -13.5 --widen 1.0 --piano salamander --orchestra vsco --out /tmp/vp25/xc > /tmp/vp25/xc/k$k.log 2>&1
  bash /tmp/vp25/tools/pq.sh /tmp/vp25/xc/vp00x-09k$k.wav >> /tmp/vp25/xc/pq.txt
done
