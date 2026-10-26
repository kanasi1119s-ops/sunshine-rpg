# 仕上がった mp3 の「前奏 → Aメロ」と「場面の段差」を、品質チェック（vb25_qc.py）と同じ測り方で見て、なだらかに直す
# （2026-10-26 人間「Aメロ入るタイミングで違和感あるぐらい音が小さくなる」「曲の途中で不自然に音が小さくなるのは気になる」）。
# 使い方: python3 vb25_fixlevel.py <版の名前（vb25-NN-slug-vX[vo]）> <聞く用の mp3 の名前（拡張子なし）>
#   ・前奏の最後の10秒で、2秒ごとの大きさが Aメロの頭（6秒）より 2dB 以上大きい所だけを下げる（0.5秒でなめらかに）
#   ・前の場面より 3.5dB 以上小さい場面（静かな場面の種類を除く）は、差が 3dB になるまで持ち上げる（場面の頭と終わり 0.8秒でなめらかに）
#   ・直したら、点数用の mp3 と、聞く用の mp3（vb_render.sh と同じ仕上げの EQ）を作り直す
import sys, json, subprocess, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
OUT = "/mnt/user-data/outputs/vb25/all"; Q = "/mnt/user-data/outputs/vbq"; SR = 48000
base, name = sys.argv[1], sys.argv[2]
r = subprocess.run(["ffmpeg", "-v", "error", "-i", f"{OUT}/{base}.mp3", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True, stdin=subprocess.DEVNULL)
x = np.frombuffer(r.stdout, np.float32).reshape(-1, 2).astype(np.float64)
m0 = x.mean(1)
m = sosfilt(butter(2, 100, "highpass", fs=SR, output="sos"), m0) + 0.6 * sosfilt(butter(1, 2000, "highpass", fs=SR, output="sos"), m0)
def db(v): return 10 * np.log10(np.mean(v ** 2) + 1e-12)
secs = json.load(open(f"{Q}/{base}.json.secs"))
g = np.zeros(len(m))   # dB
notes = []
T = next((s["t"] for s in secs if s["kind"] != "intro"), 0)
if T > 4:
    head = db(m[int((T + 0.2) * SR):int((T + 6) * SR)])
    lim = head + 2.0
    hop = int(0.25 * SR)
    for t0 in np.arange(max(0, T - 10), T - 1.9, 0.25):
        a = int(t0 * SR); lv = db(m[a:a + 2 * SR])
        if lv > lim:
            g[a:a + 2 * SR] = np.minimum(g[a:a + 2 * SR], lim - lv)
    if g.min() < -0.05: notes.append(f"前奏の後半を最大 {g.min():.1f}dB 下げた")
quiet = ("break", "bridge", "outro", "intro")
L = []
for s, n in zip(secs, secs[1:]):
    a, z = int((s["t"] + 0.3) * SR), int((n["t"] - 0.3) * SR)
    seg = m[a:z]
    if len(seg) < SR: L.append(None); continue
    w = int(0.1 * SR); rr = np.array([np.mean(seg[i:i + w] ** 2) for i in range(0, len(seg) - w, w)]); rr = rr[rr > rr.max() * 1e-3]
    L.append(10 * np.log10(rr.mean() + 1e-12))
for i in range(1, len(L)):
    if secs[i]["kind"] in quiet or L[i] is None or L[i - 1] is None: continue
    d = L[i - 1] - L[i]
    if d > 3.5:
        up = d - 3.0; a, z = int(secs[i]["t"] * SR), int(secs[i + 1]["t"] * SR)
        g[a:z] = np.maximum(g[a:z], up) if g[a:z].max() <= 0 else g[a:z] + up
        notes.append(f"{secs[i]['name']} を +{up:.1f}dB")
if not notes:
    print(base, "直す所なし"); sys.exit(0)
k = int(0.5 * SR); g = np.convolve(np.pad(g, (k, k), mode="edge"), np.ones(k) / k, mode="same")[k:-k]
y = x * (10 ** (g / 20))[:, None]
pk = np.abs(y).max()
if pk > 0.97: y *= 0.97 / pk
tmp = f"/tmp/vp25/fix-{base}.wav"; sf.write(tmp, y.astype(np.float32), SR, subtype="PCM_24")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-c:a", "libmp3lame", "-b:a", "256k", f"{OUT}/{base}.mp3"], check=True, stdin=subprocess.DEVNULL)
af = "highshelf=f=5000:g=2:t=s:w=0.6,alimiter=limit=0.89:level=false" if base.endswith("vo") else \
     "highshelf=f=5000:g=3.5:t=s:w=0.6,highshelf=f=11000:g=1.5:t=s:w=0.6,alimiter=limit=0.89:level=false"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", af, "-c:a", "libmp3lame", "-b:a", "256k", f"{OUT}/{name}.mp3"], check=True, stdin=subprocess.DEVNULL)
subprocess.run(["rm", "-f", tmp])
print(base, "・".join(notes))
