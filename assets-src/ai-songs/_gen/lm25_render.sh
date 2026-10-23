#!/bin/bash
# ラウド25曲（第2シリーズ）を1曲ずつ書き出して採点し、mp3 にする（2曲同時はメモリが足りないので順番に）。
# 使い方: bash lm25_render.sh <曲の生成.py>...   → /tmp/lm25/out/<名前>.wav・<mp3の出力フォルダ>/<番号> <曲名>.mp3・scores.tsv
#   書き出しの設定は「白い分岐点」と同じ: --drums naked --bass bnb-loud --master -13.5 --widen 1.0（ピアノがあれば --piano salamander）
ARGS=(); for a in "$@"; do ARGS+=("$(cd "$(dirname "$a")" && pwd)/$(basename "$a")"); done
cd "$(dirname "$0")/../../.." || exit 1
set -- "${ARGS[@]}"
OUT="${LM25_MP3:-/mnt/user-data/outputs/lm25}"
mkdir -p "$OUT" /tmp/lm25/out
for py in "$@"; do
  base=$(basename "$py" .py)                     # lm25_01_rojiura
  no=$(echo "$base" | cut -d_ -f2)
  json="/tmp/lm25/${base//_/-}.json"
  python3 "$py" "$json" > "/tmp/lm25/$base.gen.log" 2>&1 || { echo "生成失敗 $py"; continue; }
  # 参考の音（曲の .py で song.ref_tone）を、書き出しの前に JSON へ当てる
  if [ -s "$json.reftone" ]; then npx tsx tools/composer/apply-ref-tone.mts "$json" "$(cat "$json.reftone")" > /dev/null || { echo "参考の音の失敗 $py"; continue; }; fi
  name=$(basename "$json" .json)
  title=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['title'])" "$json")
  flags="--drums naked --bass bnb-loud --master -13.5 --widen 1.0"
  grep -qE '"instrument": ?"piano"' "$json" && flags="$flags --piano salamander"
  grep -qE '"patch": ?"(violin|viola|cello|contrabass|pizzicato|stringEnsemble|slowStrings|trumpet|trombone|tuba|horn|brassSection|oboe|bassoon|clarinet|piccolo|flute|timpani|marimba|churchOrgan|reedOrgan)"' "$json" && flags="$flags --orchestra vsco"
  [ -f "$json.flags" ] && flags="$flags $(cat "$json.flags")"
  rm -f "/tmp/lm25/out/$name.wav"
  for try in 1 2; do
    node tools/composer/song.mjs build "$json" --wav $flags --out /tmp/lm25/out > "/tmp/lm25/$base.build.log" 2>&1 && [ -f "/tmp/lm25/out/$name.wav" ] && break
  done
  if [ ! -f "/tmp/lm25/out/$name.wav" ]; then echo -e "$no\t$title\t書き出し失敗" >> "$OUT/scores.tsv"; echo "失敗 $no"; continue; fi
  # フェードイン・フェードアウト（曲の .py で song.fade_in / song.fade_out 秒）
  if [ -s "$json.fade" ]; then
    read fi fo < "$json.fade"
    if [ "$fi" != "0" ] || [ "$fo" != "0" ]; then
      dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "/tmp/lm25/out/$name.wav")
      st=$(python3 -c "print(max(0,float('$dur')-float('$fo')-0.3))")
      af="afade=t=in:st=0:d=${fi}"; [ "$fi" = "0" ] && af="anull"
      [ "$fo" != "0" ] && af="$af,afade=t=out:st=${st}:d=${fo}:curve=qsin"
      ffmpeg -v error -y -i "/tmp/lm25/out/$name.wav" -af "$af" "/tmp/lm25/out/$name.fade.wav" && mv "/tmp/lm25/out/$name.fade.wav" "/tmp/lm25/out/$name.wav"
    fi
  fi
  pq=""
  for t in 1 2 3; do
    sleep 15
    pq=$(HF_HOME=/tmp/hf python3 tools/audio-check/aes-score-lowmem.py "/tmp/lm25/out/$name.wav" 2>/dev/null | tail -1 | python3 -c "import sys,ast;l=sys.stdin.read();print(ast.literal_eval(l[l.index('{'):])['PQ'])" 2>/dev/null)
    [ -n "$pq" ] && break
  done
  ffmpeg -v error -y -i "/tmp/lm25/out/$name.wav" -b:a 256k "$OUT/${no} ${title}.mp3"
  echo -e "$no\t$title\t$pq\t$(date +%H:%M)" >> "$OUT/scores.tsv"
  echo "完了 $no $title PQ=$pq"
done
echo "全部完了"
