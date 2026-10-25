# 場面ごとの大きさの段差を直す（2026-10-26 人間「不自然に曲の音が小さくなるところがあって気になる」「前奏から Aメロに入るタイミングで多い」）。
# 使い方: python3 vb25_level.py <wav（上書き）> <secs（vwrite が書く場面の始まりの秒）>
# 場面ごとの大きさ（耳の感じ方に近い重み）を測り、前の場面より DROP dB 以上小さくなる場面（Aメロ・Bメロ・サビ・間奏など）は、
# 段差が KEEP dB になるまで持ち上げる（最大 MAX dB）。わざと静かにする場面（break・bridge・outro）と、止め・無音はそのまま。
# 場面の頭は 0.6 秒、終わりは 0.8 秒でなめらかに戻す（ミックスの人がフェーダーを動かすのと同じ）
import sys, json, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
DROP, KEEP, MAX = 3.5, 2.0, 8.0
LIFT = ("verse", "pre", "chorus", "solo", "interlude", "build", "drop")
p, sp = sys.argv[1], sys.argv[2]
x, sr = sf.read(p, always_2d=True)
secs = json.load(open(sp))
m0 = x.mean(1)
m = sosfilt(butter(2, 100, "highpass", fs=sr, output="sos"), m0) + 0.6 * sosfilt(butter(1, 2000, "highpass", fs=sr, output="sos"), m0)
def loud(a, b):
    a, b = int(a * sr), int(b * sr)
    seg = m[a:b]
    if len(seg) < sr: return None
    # 止めや無音（とても小さい所）は除いて測る
    w = int(0.1 * sr); rr = [np.mean(seg[i:i + w] ** 2) for i in range(0, len(seg) - w, w)]
    rr = np.array(rr); top = np.max(rr) if len(rr) else 0
    rr = rr[rr > top * 10 ** (-30 / 10)]
    return 10 * np.log10(np.mean(rr) + 1e-12) if len(rr) else None
L = []
for i in range(len(secs) - 1):
    a, b = secs[i]["t"], secs[i + 1]["t"]
    L.append(loud(a + 0.3, b - 0.3))
g = np.ones(len(m)); notes = []
for i in range(1, len(L)):
    k = secs[i]["kind"]
    if k not in LIFT or L[i] is None or L[i - 1] is None: continue
    drop = L[i - 1] - L[i]
    if drop <= DROP: continue
    gain = min(MAX, drop - KEEP)
    a, b = int(secs[i]["t"] * sr), int(secs[i + 1]["t"] * sr)
    up = 10 ** (gain / 20); ri, ro = int(0.6 * sr), int(0.8 * sr)
    seg = np.full(b - a, up)
    seg[:ri] = np.linspace(1.0, up, ri)                       # 頭: 前の場面の終わりから少しずつ
    seg[-ro:] = np.minimum(seg[-ro:], np.linspace(up, 1.0, ro))
    g[a:b] *= seg
    notes.append(f"{secs[i]['name']}+{gain:.1f}dB")
# 場面の変わり目: 前の場面の終わり4秒より、次の場面の頭4秒が DROP dB 以上小さいときも、頭を持ち上げて4秒かけて戻す
for i in range(1, len(secs) - 1):
    k = secs[i]["kind"]
    if k not in LIFT: continue
    t = secs[i]["t"]; nxt = secs[i + 1]["t"]
    if nxt - t < 6: continue
    pre_, head = loud(max(0, t - 4.2), t - 0.2), loud(t + 0.1, t + 4.1)
    if pre_ is None or head is None: continue
    a = int(t * sr)
    cur = 20 * np.log10(np.mean(g[a:a + int(4 * sr)]) + 1e-9)
    drop = pre_ - (head + cur)
    if drop <= DROP: continue
    gain = min(MAX, drop - KEEP)
    up = 10 ** (gain / 20); ri, ro = int(0.4 * sr), int(4.0 * sr)
    env = np.ones(ri + ro + int(2 * sr)); env[:ri] = np.linspace(1, up, ri); env[ri:ri + int(2 * sr)] = up
    env[ri + int(2 * sr):] = np.linspace(up, 1, ro)
    a0 = a; n_ = min(len(env), len(g) - a0); g[a0:a0 + n_] *= env[:n_]
    notes.append(f"{secs[i]['name']}の頭+{gain:.1f}dB")
y = x * g[:, None]
over = np.abs(y) > 0.9
if over.any():
    y = np.where(over, np.sign(y) * (0.9 + 0.08 * np.tanh((np.abs(y) - 0.9) / 0.08)), y)
sf.write(p, y, sr, subtype=sf.info(p).subtype)
print("場面の段差:", "、".join(notes) if notes else "直しなし")
