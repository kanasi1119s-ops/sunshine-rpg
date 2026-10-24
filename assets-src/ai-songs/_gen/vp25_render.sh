#!/bin/bash
# ボカロ曲のインスト25曲（vp25）を1曲ずつ書き出して採点し、mp3 にする（順番に）。
# 使い方: bash vp25_render.sh <曲の生成.py>...  → /tmp/vp25/out/<名前>.wav・$VP25_MP3/<番号> <曲名>.mp3・scores.tsv
#   仕上げ: --master -13.5 --widen 1.0（人間の標準「B」）。ドラムは曲ごと（.flags）
ARGS=(); for a in "$@"; do ARGS+=("$(cd "$(dirname "$a")" && pwd)/$(basename "$a")"); done
cd "$(dirname "$0")/../../.." || exit 1
set -- "${ARGS[@]}"
OUT="${VP25_MP3:-/mnt/user-data/outputs/vp25}"
mkdir -p "$OUT" /tmp/vp25/out
for py in "$@"; do
  base=$(basename "$py" .py)                     # vp25_01_domino
  no=$(echo "$base" | cut -d_ -f2)
  json="/tmp/vp25/${base//_/-}.json"
  python3 "$py" "$json" > "/tmp/vp25/$base.gen.log" 2>&1 || { echo "生成失敗 $py"; cat "/tmp/vp25/$base.gen.log" | tail -5; continue; }
  python3 "$(dirname "$py")/lm25_channels.py" "$json" > "/tmp/vp25/$base.ch.log" 2>&1 || { echo "チャンネルの直しの失敗 $py"; continue; }
  name=$(basename "$json" .json)
  title=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['title'])" "$json"); title=${title//\//／}
  flags="$(cat "$json.flags")"
  grep -qE '"instrument": ?"piano"' "$json" && flags="$flags --piano salamander"
  grep -qE '"patch": ?"(violin|viola|cello|contrabass|pizzicato|stringEnsemble|slowStrings|trumpet|trombone|tuba|horn|brassSection|oboe|bassoon|clarinet|piccolo|flute|timpani|marimba|churchOrgan|reedOrgan|glockenspiel)"' "$json" && flags="$flags --orchestra vsco"
  rm -f "/tmp/vp25/out/$name.wav"
  for try in 1 2; do
    node tools/composer/song.mjs build "$json" --wav $flags --out /tmp/vp25/out > "/tmp/vp25/$base.build.log" 2>&1 && [ -f "/tmp/vp25/out/$name.wav" ] && break
  done
  if [ ! -f "/tmp/vp25/out/$name.wav" ]; then echo -e "$no\t$title\t書き出し失敗" >> "$OUT/scores.tsv"; echo "失敗 $no"; continue; fi
  if [ -s "$json.fade" ]; then
    read fi fo < "$json.fade"
    if [ "$fi" != "0" ] || [ "$fo" != "0" ]; then
      dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "/tmp/vp25/out/$name.wav")
      st=$(python3 -c "print(max(0,float('$dur')-float('$fo')-0.3))")
      af="afade=t=in:st=0:d=${fi}"; [ "$fi" = "0" ] && af="anull"
      [ "$fo" != "0" ] && af="$af,afade=t=out:st=${st}:d=${fo}:curve=qsin"
      ffmpeg -v error -y -i "/tmp/vp25/out/$name.wav" -af "$af" "/tmp/vp25/out/$name.fade.wav" && mv "/tmp/vp25/out/$name.fade.wav" "/tmp/vp25/out/$name.wav"
    fi
  fi
  python3 "$(dirname "$py")/lm25_intro_lift.py" "/tmp/vp25/out/$name.wav" | tee -a "/tmp/vp25/$base.build.log"
  pq=""
  for t in 1 2 3; do
    sleep 10
    pq=$(HF_HOME=/tmp/hf python3 tools/audio-check/aes-score-lowmem.py "/tmp/vp25/out/$name.wav" 2>/dev/null | tail -1 | python3 -c "import sys,ast;l=sys.stdin.read();print(ast.literal_eval(l[l.index('{'):])['PQ'])" 2>/dev/null)
    [ -n "$pq" ] && break
  done
  ffmpeg -v error -y -i "/tmp/vp25/out/$name.wav" -b:a 256k "$OUT/${no} ${title}.mp3"
  echo -e "$no\t$title\t$pq\t$(date +%H:%M)" >> "$OUT/scores.tsv"
  echo "完了 $no $title PQ=$pq"
done
echo "全部完了"
