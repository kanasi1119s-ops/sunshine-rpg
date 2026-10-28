cd /home/claude/wt-mix
while read slug v; do no=${slug%%_*}; s=${slug#*_}; jv=$v; [ $no = 02 ] && jv=v24
  b=vb25-$no-$s-${jv}vo; A=$(ls "/mnt/user-data/outputs/vb25/all/" | grep -F "$no " | grep -F "（歌：重音テト・仮）$v.mp3" | head -1)
  [ -f /tmp/yt/seq/$no.mp4.seq.json ] && continue
  echo "== $no $A"
  MV_DRY=1 python3 tools/mv/teto_mv.py /tmp/mv/fr tools/mv/track_teto_a.json /tmp/yt/silent.wav "/mnt/user-data/outputs/vb25/all/$A" x /tmp/yt/seq/$no.mp4 /mnt/user-data/outputs/vbq/$b.json /tmp/vp25/cl/$b-vocal.ust 2>&1 | grep "閉じて\|Error\|error"
done < /tmp/yt/songs.txt
echo 全部おわり
