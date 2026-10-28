#!/bin/bash
# パソコンの書き出し係に渡す JSON を作る。使い方: vp_pcq.sh <版 v1> <番号>...
V=$1; shift
G=/home/claude/wt-mix/assets-src/ai-songs/_gen
cd /home/claude/wt-mix || exit 1
mkdir -p /tmp/vp25/pcq /mnt/user-data/outputs/vpq
for n in "$@"; do
  py=$(ls $G/vp25_${n}_*.py | head -1); base=$(basename "$py" .py)
  json="/tmp/vp25/pcq/${base//_/-}.json"
  python3 "$py" "$json" > /dev/null 2>&1 || { echo "生成失敗 $n"; continue; }
  python3 $G/lm25_channels.py "$json" > /tmp/vp25/pcq/$base.ch.log 2>&1 || { echo "チャンネル失敗 $n"; continue; }
  name=$(basename "$json" .json)
  flags="$(cat $json.flags)"
  grep -qE '"instrument": ?"piano"' "$json" && flags="$flags --piano salamander"
  grep -qE '"patch": ?"(violin|viola|cello|contrabass|pizzicato|stringEnsemble|slowStrings|trumpet|trombone|tuba|horn|brassSection|oboe|bassoon|clarinet|piccolo|flute|timpani|marimba|churchOrgan|reedOrgan|glockenspiel)"' "$json" && flags="$flags --orchestra vsco"
  out=/mnt/user-data/outputs/vpq/$name-$V
  cp "$json" "$out.json"; echo "$flags" > "$out.json.flags"; cp "$json.fade" "$out.json.fade"; cp "$json.meta" "$out.json.meta"
  echo "できた $name-$V"
done
