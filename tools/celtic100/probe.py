# 楽器の大きさを、笛と並べて試しに書き出して測る（F-process.md の 3）。
# 使い方: python3 tools/celtic100/probe.py <曲.json> "<パート名>:<音の並び>[:gainDb[:barGain]]" ... [--bpm 60] [--beats 4]
#   例: python3 tools/celtic100/probe.py /tmp/cel/w/c004.json "ドローン（G3）:G3:3 R:1 G3:3 R:9:10:0.7" "フルート:R:8 G4:3 R:5"
#   音の並びの中の「:」と区切りの「:」がまざらないよう、区切りは「|」でもよい: "ドローン（G3）|G3:3 R:13|10|0.7"
# 1秒ごとの音量（dB）を出す。曲の書き出しの設定（cNNN.json.flags）をそのまま使う。
import json, os, subprocess, sys
import numpy as np, soundfile as sf

src = sys.argv[1]; args = sys.argv[2:]
bpm, beats = 60, 4
if "--bpm" in args: i = args.index("--bpm"); bpm = float(args[i + 1]); del args[i:i + 2]
if "--beats" in args: i = args.index("--beats"); beats = int(args[i + 1]); del args[i:i + 2]
s = json.load(open(src))
d = {k: v for k, v in s.items() if k != "parts"}
parts = []
for a in args:
    f = a.split("|")
    role, notes = f[0], f[1]
    base = next(p for p in s["parts"] if p["role"] == role)
    p = dict(base); p["notes"] = notes; p["barGain"] = [float(f[3]) if len(f) > 3 else 0.7] * 64
    if len(f) > 2 and f[2] != "": p["gainDb"] = float(f[2])
    p["role"] = f"{role}・{len(parts)}"; p["pan"] = (p.get("pan") or 0) + 0.001 * len(parts)   # 同じパートを2回使っても別のチャンネルに
    parts.append(p)
d["parts"] = parts; d["bpm"] = bpm; d["beats"] = beats; d["tempo"] = [{"bar": 1, "bpm": bpm}]; d["sections"] = []
d["chords"] = " ".join([s["chords"].split()[0]] * 16)
os.makedirs("/tmp/probe", exist_ok=True)
json.dump(d, open("/tmp/probe/p.json", "w"), ensure_ascii=False)
flags = open(src + ".flags").read().split() if os.path.exists(src + ".flags") else []
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
subprocess.run(["node", "tools/composer/song.mjs", "build", "/tmp/probe/p.json", "--wav", *flags, "--out", "/tmp/probe"], cwd=root, capture_output=True, timeout=600)
x, sr = sf.read("/tmp/probe/p.wav"); x = x.mean(1) if x.ndim > 1 else x
print("1秒ごとの音量(dB):", [round(20 * np.log10(np.sqrt((x[i * sr:(i + 1) * sr] ** 2).mean()) + 1e-9)) for i in range(len(x) // sr)])
