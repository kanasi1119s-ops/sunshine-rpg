#!/bin/bash
# 書き出しの待ち行列: ほかの書き出しが終わるのを待ってから、引数の曲を書き出す。使い方: v3_q.sh <スクリプト> <slug> <版> "<NN 曲名>"
sleep $((RANDOM % 5))
while pgrep -f "v3_both.sh" >/dev/null || pgrep -f "v3_render.sh" >/dev/null; do sleep 15; done
bash /tmp/vp25/tools/v3_both.sh "$@"
