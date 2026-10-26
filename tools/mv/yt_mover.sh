#!/bin/bash
# 書き出しが終わった曲の切り分けを送る用の置き場へ移し、まるごとの mp4 を消す（容量のため）
while true; do
  for d in /tmp/yt/parts/*.done; do [ -f "$d" ] || continue; no=$(basename $d .done)
    mv /tmp/yt/parts/${no}_*.mp4 /mnt/user-data/outputs/ytparts/ 2>/dev/null; rm -f /tmp/yt/out/$no.mp4; mv $d /mnt/user-data/outputs/ytparts/; echo "移した $no"; done
  [ -f /tmp/yt/mover.stop ] && exit 0; sleep 20
done
