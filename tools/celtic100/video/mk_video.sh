#!/bin/bash
# 「銀の笛と百の夜」全100曲の動画を作った手順（2026-11-02。PC の中の作業用の Linux で、1回 180秒までの呼び出しに分けて動かした）
#   PC の作業用 Linux は、呼び出しが終わると裏で動かしたものも止まる（nohup・setsid も止まる）。だから段階に分ける。
# 1) 曲を作業場所へ写す（速い。100曲で約10秒）
#    for n in 001..100: cp Downloads/銀の笛と百の夜/${n}_*.mp3 ~/vidwork/s/$n.mp3
# 2) すき間は「mp3 の2秒の無音」にする（wav をまぜると concat で読めなくなる）。mp3 の無音は実際は 2.0376秒なので、開始秒はその長さで数える
#    ffmpeg -f lavfi -i anullsrc=r=44100:cl=stereo -t 2 -c:a libmp3lame -b:a 256k gap.mp3
#    list.txt に「曲・gap・曲・gap…・曲100」。starts.txt は awk で 曲の長さ＋gapの長さ を足していく
# 3) 音は25曲ずつ4つに分けて AAC 192k にする（1つ約50秒）→ -c copy でつなぐ
# 4) 映像: ffmpeg -stream_loop -1 -i loop.mp4 -i audio.m4a -map 0:v -map 1:a -c copy -shortest -movflags +faststart out.mp4（約30秒・3.9GB）
# 5) Downloads へ写すのは約7MB/秒で遅いので、dd の skip/seek（conv=notrunc）で続きから何回かに分けて写し、ところどころの md5 をくらべて確かめる
# 6) 説明文: python3 mk_desc.py starts.txt <全体の秒> 説明文.txt（タイトル100文字・本文5000文字まで）／サムネイル: python3 mk_thumb.py bg.png thumb.jpg "7h 23m"
