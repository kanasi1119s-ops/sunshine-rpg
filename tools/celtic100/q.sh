#!/bin/bash
# 使い方: q.sh 001 002 ...   空いた枠（同時2つまで）で順に作る。いくつ起動しても、ロックで1つずつ順番に動く
exec 9>/tmp/cel/q.lock; flock 9
for n in "$@"; do
  while [ $(ps aux | grep -c "[r]un.sh") -ge 1 ]; do sleep 20; done
  rm -f /tmp/cel/w/done$n
  setsid nohup /tmp/cel/run.sh $n > /dev/null 2>&1 &
  sleep 8
done
