#!/bin/bash
# 使い方: run.sh 002   （/tmp/cel/w/c002.json と air002.json が必要）
N=$1
cd /home/claude/wt-mix
rm -f /tmp/cel/w/done$N /tmp/cel/w/b$N.log /tmp/cel/out/c$N.wav /tmp/cel/out/c$N.final.wav   # 古い書き出しを点数にしない（2026-10-29 再起動後に失敗が古い点で出た）
node tools/composer/song.mjs build /tmp/cel/w/c$N.json --wav $(cat /tmp/cel/w/c$N.json.flags) --out /tmp/cel/out > /tmp/cel/w/b$N.log 2>&1
cd assets-src/ai-songs/_gen && python3 c100_air.py /tmp/cel/out/c$N.wav /tmp/cel/w/air$N.json /tmp/cel/out/c$N.final.wav > /tmp/cel/w/air$N.log 2>&1
cd /home/claude/wt-mix
rm -f /tmp/cel/out/c$N.wav   # 空気を重ねる前の wav は消す（ディスクの節約）
python3 /tmp/bar/qc.py /tmp/cel/out/c$N.final.wav > /tmp/cel/w/qc$N.log 2>&1
HF_HOME=/tmp/hf python3 tools/audio-check/aes-score-lowmem.py /tmp/cel/out/c$N.final.wav > /tmp/cel/w/pq$N.log 2>&1
touch /tmp/cel/w/done$N
