#!/bin/bash
# ラウドロック・ラウドメタル25曲を、1曲ずつ書き出して採点し、mp3 にする（同時に2曲書き出すとメモリが足りないので順番に）。
# 使い方: bash loud25_render.sh <JSONのフォルダ> <mp3の出力フォルダ> [番号...]
#   結果の一覧: <mp3の出力フォルダ>/scores.tsv（番号・曲名・点数）
cd "$(dirname "$0")/../../.." || exit 1
IN="$1"; OUT="$2"; shift 2
mkdir -p "$OUT"
for f in "$IN"/loud25-*.json; do
  no=$(basename "$f" | cut -d- -f2)
  if [ $# -gt 0 ]; then ok=0; for w in "$@"; do [ "$(printf %02d "$w")" = "$no" ] && ok=1; done; [ $ok = 1 ] || continue; fi
  name=$(basename "$f" .json)
  title=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['title'])" "$f")
  flags="--drums muldjord --bass finger --master-preset rock-clean"
  grep -q '"instrument": "piano"' "$f" && flags="$flags --piano salamander"
  for try in 1 2; do
    node tools/composer/song.mjs build "$f" --wav $flags --out /tmp/loud25-out > "/tmp/loud25-out-$name.log" 2>&1 && [ -f "/tmp/loud25-out/$name.wav" ] && break
  done
  if [ ! -f "/tmp/loud25-out/$name.wav" ]; then echo -e "$no\t$title\t書き出し失敗" >> "$OUT/scores.tsv"; continue; fi
  pq=$(HF_HOME=/tmp/hf python3 tools/audio-check/aes-score.py "/tmp/loud25-out/$name.wav" 2>/dev/null | tail -1 | python3 -c "import sys,ast;l=sys.stdin.read();print(ast.literal_eval(l[l.index('{'):])['PQ'])" 2>/dev/null)
  ffmpeg -v error -y -i "/tmp/loud25-out/$name.wav" -b:a 256k "$OUT/${no} ${title}.mp3"
  echo -e "$no\t$title\t$pq" >> "$OUT/scores.tsv"
  echo "完了 $no $title PQ=$pq"
  rm -f "/tmp/loud25-out/$name.wav"
done
echo "全部完了"
