#!/bin/bash
# 第3弾 HUMMING RELAY: 各曲のテトのコマ並び（口の動き）を作る（第2弾の mkseq.sh と同じ。置き場だけ /tmp/yt3）
cd /home/claude/wt-mix
while IFS=$'\t' read no b a; do
  [ -f /tmp/yt3/seq/$no.mp4.seq.json ] && continue
  ffmpeg -nostdin -v error -y -i "$a" -ac 1 -ar 24000 /tmp/yt3/voc.wav
  MV_DRY=1 MV_REV=6 MV_JUMP=4 nice -n 5 python3 tools/mv/teto_mv.py /tmp/yt2/fr tools/mv/track_teto_a.json /tmp/yt3/voc.wav "$a" "$no" /tmp/yt3/seq/$no.mp4 /mnt/user-data/outputs/vbq/$b.json /tmp/vp25/cl/$b-vocal.ust 2>&1 | grep -E "閉じている|×|Error|Trace" | head -3 | sed "s/^/$no /"
done < /tmp/yt3/songs.txt
echo SEQ_DONE
