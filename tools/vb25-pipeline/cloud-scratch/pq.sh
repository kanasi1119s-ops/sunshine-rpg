#!/bin/bash
# 使い方: pq.sh <wav>... → PQ（と CE・CU・PC）
cd /home/claude/wt-mix
for w in "$@"; do
  r=$(HF_HOME=/tmp/hf python3 tools/audio-check/aes-score-lowmem.py "$w" 2>/dev/null | tail -1)
  echo "$(basename $w) $r"
done
