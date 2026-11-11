#!/bin/bash
# 使い方: v3_both.sh <スクリプト vt3_02_radio.py> <slug vt3-02-radio> <版 v5> "<NN 曲名>"  … 歌入りと BGM を作って書き出し、確かめの数字を出す
cd /home/claude/wt-mix/assets-src/ai-songs/_gen
VB_VOCAL=1 python3 $1 /mnt/user-data/outputs/vbq/$2-$3vo.json 2>&1 | grep -i "error\|Traceback\|×" | head -5
python3 $1 /mnt/user-data/outputs/vbq/$2-$3.json 2>&1 | grep -i "error\|Traceback\|×" | head -5
cd /home/claude/wt-mix
bash /tmp/vp25/tools/v3_render.sh $2-$3vo "$4（歌：重音テト・仮）$3" 2>&1 | grep "×" | head -3
bash /tmp/vp25/tools/v3_render.sh $2-$3 "$4（BGM・仮）$3" 2>&1 | grep "×" | head -3
python3 /tmp/vp25/tools/v3_check.py $2 $3 "$4"
