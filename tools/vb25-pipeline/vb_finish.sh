#!/bin/bash
# vb25: PC の WAV → 低域の掃除（24Hz より下・直流）→ フェード → 前奏の大きさ → 採点 → mp3。点数がいちばん高い版を「NN 曲名.mp3」に残す
cd /home/claude/wt-mix
OUT=/mnt/user-data/outputs/vb25; mkdir -p "$OUT/all" /tmp/vp25/out
for w in "$@"; do
  base=$(basename "$w" .wav); no=$(echo "$base" | cut -d- -f2)
  meta=/mnt/user-data/outputs/vbq/$base.json.meta; fadef=/mnt/user-data/outputs/vbq/$base.json.fade
  title=$(python3 -c "import json;print(json.load(open('$meta'))['title'])"); title=${title//\//／}
  tmp=/tmp/vp25/vbfin-$base.wav
  python3 - "$w" $tmp <<'P'
import sys, soundfile as sf, numpy as np
from scipy.signal import butter, sosfiltfilt
d,sr=sf.read(sys.argv[1]); st=sf.info(sys.argv[1]).subtype
d=d-d.mean(0); y=sosfiltfilt(butter(2,24,'hp',fs=sr,output='sos'),d,axis=0)
pk=np.abs(y).max(); y=y*(0.97/pk) if pk>0.97 else y
sf.write(sys.argv[2],y,sr,subtype=st)
P
  if [ -f "$fadef" ]; then read fi fo < "$fadef"
    if [ "$fo" != "0" ] || [ "$fi" != "0" ]; then
      dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $tmp); st=$(python3 -c "print(max(0,float('$dur')-float('$fo')-0.3))")
      af="anull"; [ "$fi" != "0" ] && af="afade=t=in:st=0:d=$fi"; [ "$fo" != "0" ] && af="$af,afade=t=out:st=$st:d=$fo:curve=qsin"
      ffmpeg -v error -y -i $tmp -af "$af" $tmp.f.wav && mv $tmp.f.wav $tmp; fi; fi
  # 2026-10-26: 場面の秒（.secs）がある曲は、前奏を「真ん中」ではなく最初の Aメロに合わせる（前奏の後半が大きすぎて Aメロでガクッと小さくなるのを防ぐ）
  if [ -f "/mnt/user-data/outputs/vbq/$base.json.secs" ]; then python3 assets-src/ai-songs/_gen/vb25_intro.py $tmp "/mnt/user-data/outputs/vbq/$base.json.secs"; else python3 assets-src/ai-songs/_gen/lm25_intro_lift.py $tmp; fi
  [ -f "/mnt/user-data/outputs/vbq/$base.json.secs" ] && python3 assets-src/ai-songs/_gen/vb25_level.py $tmp "/mnt/user-data/outputs/vbq/$base.json.secs"
  [ -f "/mnt/user-data/outputs/vbq/$base.json.secs" ] && python3 assets-src/ai-songs/_gen/vb25_tone.py $tmp   # 2026-10-26: 最後に全体の音の高さのバランスを整える
  pq=$(HF_HOME=/tmp/hf python3 tools/audio-check/aes-score-lowmem.py $tmp 2>/dev/null | tail -1 | python3 -c "import sys,ast;l=sys.stdin.read();print(ast.literal_eval(l[l.index('{'):])['PQ'])" 2>/dev/null)
  ffmpeg -v error -y -i $tmp -b:a 256k "$OUT/all/$base.mp3"
  best=$(awk -F'\t' -v n="$no" '$1==n{if($3>m)m=$3}END{print m+0}' "$OUT/scores.tsv" 2>/dev/null)
  if python3 -c "import sys;sys.exit(0 if float('${pq:-0}')>=float('${best:-0}') else 1)"; then cp "$OUT/all/$base.mp3" "$OUT/$no $title.mp3"; fi
  mv $tmp /tmp/vp25/out/$base.wav
  echo -e "$no\t$title\t$pq\t$(date +%H:%M)\t$base" >> "$OUT/scores.tsv"
  echo "完了 $no $title $pq（これまでの最高 $best）"
done
