# 歌の WAV から「ノイズっぽい所」を探す: 音のある（-50dBFS 超）フレームのうち、声の高さが取れない（無声）か、
# 高域（4kHz〜）のザラつきが声より強い所。音符の頭の子音（0〜120ms）は除く。
import sys, importlib.util, numpy as np, soundfile as sf, pyworld as pw
wav, vocpy, bpm = sys.argv[1], sys.argv[2], float(sys.argv[3])
x, fs = sf.read(wav, dtype="float64", always_2d=True); x = x.mean(1)
spec = importlib.util.spec_from_file_location("v", vocpy); v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
beat = 60 / bpm; notes = v.notes()
f0, t = pw.harvest(x, fs, frame_period=5.0, f0_floor=120, f0_ceil=900)
hop = int(fs * 0.005); n = len(f0)
rms = np.array([np.sqrt(np.mean(x[i*hop:(i+1)*hop+hop]**2) + 1e-12) for i in range(n)]); db = 20*np.log10(rms)
# 各フレームが「音符の中（頭から120ms以降、終わりまで）」か、「音符の外（休み）」か
inside = np.zeros(n, bool); head = np.zeros(n, bool); rest = np.ones(n, bool)
for s, d, p, k in notes:
    a, b = s*beat, (s+d)*beat
    i0, i1 = int(a/0.005), int(b/0.005)
    rest[max(0,i0-10):i1+20] = False   # 前の子音と、終わりの尾は休みに数えない
    head[i0-25:i0+24] = True
    inside[i0+24:i1] = True
uv_in = inside & ~head & (f0 == 0) & (db > -50)
print(f"音符の中で声の高さが取れない（無声＝ノイズ）フレーム: {uv_in.sum()} / {(inside & ~head).sum()}  ({uv_in.sum()*5/1000:.2f}秒)")
# 連続した区間に
segs = []; i = 0
while i < n:
    if uv_in[i]:
        j = i
        while j < n and uv_in[j]: j += 1
        if j - i >= 3: segs.append((i*0.005, (j-i)*5, db[i:j].max()))
        i = j
    else: i += 1
print("無声の区間（3フレーム以上）:", len(segs))
for s, L, m in sorted(segs, key=lambda z: -z[1])[:15]:
    b = s / (4*beat)
    k = [nn for nn in notes if nn[0]*beat <= s < (nn[0]+nn[1])*beat]
    print(f"  {s:7.2f}秒（{int(b)+1}小節目） {L:4.0f}ms 最大{m:5.1f}dB  音: {k[0][3] if k else '-'} {k[0][2] if k else ''}")
r = rest & (db > -200)
print(f"休みの所の大きさ: 中央 {np.median(db[rest]):.1f}dB / 90% {np.percentile(db[rest],90):.1f}dB / 最大 {db[rest].max():.1f}dB")
loud_rest = rest & (db > -55)
print("休みなのに -55dB を超えるフレーム:", loud_rest.sum())
# 休みの中で鳴っている所を、「前の音の終わりからの時間」「次の音までの時間」で分ける
starts = np.array([s*beat for s,d,p,k in notes]); ends = np.array([(s+d)*beat for s,d,p,k in notes])
idx = np.where(loud_rest)[0]
cat = {"次の音の直前0.35秒以内（子音・息）": 0, "前の音の終わりから0.6秒以内（尾）": 0, "どちらでもない": 0}
other = []
for i in idx:
    tt = i * 0.005
    nx = starts[starts > tt]; pv = ends[ends <= tt]
    if len(nx) and nx[0] - tt < 0.35: cat["次の音の直前0.35秒以内（子音・息）"] += 1
    elif len(pv) and tt - pv[-1] < 0.6: cat["前の音の終わりから0.6秒以内（尾）"] += 1
    else: cat["どちらでもない"] += 1; other.append(tt)
print(cat)
if other: print("どちらでもない所の例:", [round(o,2) for o in other[:20]])
# 尾の所のスペクトルの平らさ（ノイズほど 1 に近い）
def flat(seg):
    S_ = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) + 1e-12
    return np.exp(np.mean(np.log(S_))) / np.mean(S_)
tails = []
for e in ends:
    i0 = int(e * fs); seg = x[i0:i0 + int(0.3 * fs)]
    if len(seg) > 2048 and 20*np.log10(np.sqrt(np.mean(seg**2))+1e-12) > -55:
        tails.append((e, 20*np.log10(np.sqrt(np.mean(seg**2))+1e-12), flat(seg[:4096])))
print("音の終わりの後0.3秒に音が残る所:", len(tails), "平らさの中央", round(float(np.median([z[2] for z in tails])),3) if tails else "-")
