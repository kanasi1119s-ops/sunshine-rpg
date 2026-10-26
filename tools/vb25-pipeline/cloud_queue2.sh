#!/bin/bash
# 歌の版の書き出しを順番に（同時に2本まで。PC の仕上げ中＝/tmp/vp25/pcfin.lock があるときは1本まで）
Q=/tmp/vp25/cq.txt; DONE=/tmp/vp25/cq.done; touch $Q $DONE
while true; do
  [ -f /tmp/vp25/cq.stop ] && exit 0
  n=$(ps -eo args | grep -c "^node tools/composer/[s]ong.mjs build")
  max=2; { [ -f /tmp/vp25/pcfin.lock ] || pgrep -f "aes-score|sing.py mix" >/dev/null; } && max=1   # 2026-10-26: 仕上げや歌の合成の最中は1本だけ（メモリ不足を防ぐ）
  if [ "$n" -lt "$max" ]; then
    line=$(grep -vxF -f $DONE $Q | head -1)
    if [ -n "$line" ]; then
      echo "$line" >> $DONE
      f=${line%%|*}; t=${line#*|}
      nohup /tmp/vp25/tools/vb_render.sh "$f" "$t" >> /tmp/vp25/cq.log 2>&1 &
      sleep 20; continue
    fi
  fi
  [ -z "$(grep -vxF -f $DONE $Q)" ] && [ "$n" -eq 0 ] && ! pgrep -f "vb_render.sh" >/dev/null && { echo "待ち行列が空になりました（idle）"; exit 0; }
  sleep 30
done
