#!/bin/bash
# PC の WAV の仕上げを、クラウドの書き出しが1本以下のときだけ行う（メモリ不足を防ぐ）。引数: 名前 曲名 [名前 曲名 ...]
touch /tmp/vp25/pcfin.lock
while [ $# -ge 2 ]; do
  while [ "$(ps -eo args | grep -c '^node tools/composer/[s]ong.mjs build')" -gt 1 ]; do sleep 20; done
  /tmp/vp25/tools/vb_pcfin.sh "$1" "$2"; shift 2
done
rm -f /tmp/vp25/pcfin.lock
