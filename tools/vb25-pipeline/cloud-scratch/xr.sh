#!/bin/bash
cd /home/claude/wt-mix
for pair in "rt1:bright-pop-rock" "rt2:glossy-jrock"; do
  t=${pair%%:*}; r=${pair##*:}
  while ps -eo args | grep -q "^node tools/composer/song.mjs build"; do sleep 15; done
  timeout 1200 node tools/composer/song.mjs build /tmp/vp25/xc/vp00x-09$t.json --wav --drums jpop --bass bnb-loud --master -13.5 --widen 1.0 --piano salamander --orchestra vsco --ref-tone $r --out /tmp/vp25/xc > /tmp/vp25/xc/$t.log 2>&1
  bash /tmp/vp25/tools/pq.sh /tmp/vp25/xc/vp00x-09$t.wav >> /tmp/vp25/xc/pq.txt
done
