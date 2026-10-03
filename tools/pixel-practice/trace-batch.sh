#!/bin/bash
# 使い方: trace-batch.sh 出力フォルダ 参考画像...  — 参考画像ごとに切り出し→エディタで下絵つきトレース→食い違い0マスを確認
OUT=$1; shift
for f in "$@"; do
  n=$(basename "$f" .png)
  python3 "$(dirname "$0")/prep-trace.py" "$f" "$OUT" "$n" >/dev/null 2>&1 || continue
  timeout 200 node "$(dirname "$0")/editor-draw.mjs" "$OUT/$n.txt" "$OUT/$n.json" "$OUT/$n-editor.png" --ref "$OUT/$n.png" --zoom 10 2>&1 | sed "s/^/$n: /"
done
