#!/bin/bash
# パソコンで書き出した WAV を仕上げる: フェード → 前奏の大きさ → 採点 → mp3。使い方: vp_finish.sh <wav>...
cd /home/claude/wt-mix
OUT="${VP25_MP3:-/mnt/user-data/outputs/vp25}"; mkdir -p "$OUT"
for w in "$@"; do
  base=$(basename "$w" .wav)                 # vp25-01-domino-v1
  no=$(echo "$base" | cut -d- -f2)
  meta=/mnt/user-data/outputs/vpq/$base.json.meta
  title=$(python3 -c "import json;print(json.load(open('$meta'))['title'])"); title=${title//\//／}
  fadef=/mnt/user-data/outputs/vpq/$base.json.fade
  tmp=/tmp/vp25/pcfin-$no.wav; cp "$w" $tmp
  if [ -f "$fadef" ]; then read fi fo < "$fadef"
    if [ "$fo" != "0" ] || [ "$fi" != "0" ]; then
      dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $tmp); st=$(python3 -c "print(max(0,float('$dur')-float('$fo')-0.3))")
      af="anull"; [ "$fi" != "0" ] && af="afade=t=in:st=0:d=$fi"; [ "$fo" != "0" ] && af="$af,afade=t=out:st=$st:d=$fo:curve=qsin"
      ffmpeg -v error -y -i $tmp -af "$af" $tmp.f.wav && mv $tmp.f.wav $tmp; fi; fi
  python3 assets-src/ai-songs/_gen/lm25_intro_lift.py $tmp
  pq=$(HF_HOME=/tmp/hf python3 tools/audio-check/aes-score-lowmem.py $tmp 2>/dev/null | tail -1 | python3 -c "import sys,ast;l=sys.stdin.read();print(ast.literal_eval(l[l.index('{'):])['PQ'])" 2>/dev/null)
  ffmpeg -v error -y -i $tmp -b:a 256k "$OUT/$no $title.mp3"
  cp $tmp /tmp/vp25/out/$base.wav
  echo -e "$no\t$title\t$pq\t$(date +%H:%M)\tPC $base" >> "$OUT/scores.tsv"
  rm -f $tmp; echo "完了 $no $title $pq"
done
