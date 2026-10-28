#!/bin/bash
# 次に仕上がった曲を待って、検査結果を出す（まだ見ていないもの）
seen=/tmp/cel/seen.txt; touch $seen
while true; do
  for f in $(ls -t /tmp/cel/w/done[0-9][0-9][0-9] 2>/dev/null); do
    n=$(basename $f | sed 's/done//')
    key="$n $(stat -c %Y $f)"
    if ! grep -qx "$key" $seen; then
      echo "$key" >> $seen
      echo "== $n"; /tmp/cel/chk.sh $n
      exit 0
    fi
  done
  sleep 15
done
