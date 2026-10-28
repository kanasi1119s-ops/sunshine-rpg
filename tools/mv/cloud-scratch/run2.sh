#!/bin/bash
until grep -q "全部おわり" /tmp/yt/render.log; do sleep 30; done
SKIP="01 03 04 05 06 10 11 12 13 14 15 16 18 21 22 23 24" /tmp/yt/render_all.sh > /tmp/yt/render2.log 2>&1
