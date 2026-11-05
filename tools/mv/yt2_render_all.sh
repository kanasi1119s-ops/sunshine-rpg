cd /home/claude/wt-mix
while IFS=$'\t' read no b a; do
  [ -f /tmp/yt2/out/$no.done ] && continue
  [ -f /tmp/yt2/stop ] && break
  echo "== $no $(date +%H:%M)"
  MV_ALBUM_J="セカンド・シグナル" MV_ALBUM_E="SECOND SIGNAL" MV_KANA=/tmp/yt2/kana/$b.json.kana MV_EN=/tmp/yt2/en/$no.json MV_SMOOTH=1 MV_FPS=48 nice -n 5 python3 tools/mv/stage_mv.py $no /tmp/yt2/songs.tsv "$a" /mnt/user-data/outputs/vbq/$b.json /tmp/vp25/cl/$b-vocal.ust /tmp/yt2/seq/$no.mp4.seq.json /tmp/yt2/tm /tmp/yt2/stage.png /tmp/yt2/out/$no.mp4 2>&1 | grep -v -i "warn\|pkg_res" | tail -2
  vd=$(ffprobe -v error -show_entries format=duration -of csv=p=0 /tmp/yt2/out/$no.mp4); ad=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$a")
  python3 -c "import sys;sys.exit(0 if abs(float('${vd:-0}')-float('$ad'))<0.6 else 1)" && touch /tmp/yt2/out/$no.done || echo "× $no 長さがちがう（映像 $vd・音 $ad）"
done < /tmp/yt2/songs.txt
echo ALL_DONE $(date +%H:%M)
