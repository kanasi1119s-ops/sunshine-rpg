# 使い方: python3 v3_check.py <slug 例 vt3-02-radio> <版 例 v5> "<曲名>" … 歌入りと BGM の 点・場面ごとの大きさ・雑音の数 を短く出す
import sys, json, subprocess, numpy as np, soundfile as sf, os, glob
slug, ver, title = sys.argv[1:4]
sc = {l.split("\t")[4].strip(): l.split("\t")[2] for l in open("/mnt/user-data/outputs/vt3/scores.tsv") if l.count("\t") >= 4}
for tag, suf, nm in (("歌", "vo", f"（歌：重音テト・仮）{ver}"), ("BGM", "", f"（BGM・仮）{ver}")):
    f = f"/mnt/user-data/outputs/vt3/all/{title}{nm}.mp3"
    if not os.path.exists(f): print(tag, "なし"); continue
    w = f"/tmp/kfb/chk-{slug}-{ver}{suf}.wav"; subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f, w]); x, sr = sf.read(w); m = x.mean(1)
    secs = json.load(open(f"/mnt/user-data/outputs/vbq/{slug}-{ver}{suf}.json.secs"))
    print(tag, "点", sc.get(f"{slug}-{ver}{suf}"), "|", " ".join(f'{a["name"]}{20 * np.log10(np.sqrt((m[int(a["t"] * sr):int(b["t"] * sr)] ** 2).mean()) + 1e-9):.1f}' for a, b in zip(secs, secs[1:])))
    bpm = json.load(open(f"/mnt/user-data/outputs/vbq/{slug}-{ver}{suf}.json"))["bpm"]
    o = subprocess.run(["python3", "tools/audio-check/noise_scan.py", w, "--bpm", str(bpm)], capture_output=True, text=True, cwd="/home/claude/wt-mix").stdout
    os.remove(w); print("   雑音:", " ".join(l.strip() for l in o.splitlines() if "か所" in l or "■" in l)[:200])
