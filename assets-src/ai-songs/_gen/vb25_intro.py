# 前奏の大きさを、最初の Aメロ（前奏のあとの場面）に合わせる（2026-10-26 人間（03）「Aメロ入るタイミングで違和感あるぐらい音が小さくなる。他の曲にもありそう」）。
# 使い方: python3 vb25_intro.py <wav（上書き）> <secs（vwrite が書く場面の始まりの秒）>
# これまでの lm25_intro_lift.py は「曲の真ん中の大きさ」を目安に、前奏の頭から決めた所までを同じ量だけ持ち上げていた。
#   歌の版は真ん中（歌入り）が大きいので上げ幅が大きくなり、前奏の後半（もともと大きい所）まで +7dB ほど上がって、
#   Aメロに入った所でガクッと小さくなっていた（03 で前奏の後半 −14dB → Aメロ −20dB）。
# ここでは、前奏のあとの場面（ふつうは Aメロ）の大きさを目安にし、0.1秒ごとの大きさ（3秒でならしたもの）を見て、
#   ・目安より UP dB 以上大きい所は、目安 + UP dB まで下げる（前奏から Aメロへの段差をなくす）
#   ・目安より LOW dB 以上小さい所は、目安 − LOW dB まで上げる（最大 MAX dB。わざと静かな始まりは少し静かなまま残す）
# 上げ下げは 1.5秒でなめらかにつなぎ、前奏の終わりの 1.2秒で元に戻す
import sys, json, numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt
UP, LOW, MAX, CUT = 1.0, 6.0, 15.0, 9.0   # 2026-10-26: 1.5 では 12・13・17・24 で前奏の後半が Aメロより 3〜5dB 大きいまま残った → 1.0 と、ならしを 3秒→1秒に
p, sp = sys.argv[1], sys.argv[2]
x, sr = sf.read(p, always_2d=True)
secs = json.load(open(sp))
T = next((s["t"] for s in secs if s["kind"] != "intro"), 0.0)
if T < 2.0:
    print("前奏の大きさ: 前奏なし（そのまま）"); sys.exit(0)
nxt = next((s["t"] for s in secs if s["t"] > T + 1e-3), T + 20)
m0 = x.mean(1)
m = sosfilt(butter(2, 100, "highpass", fs=sr, output="sos"), m0) + 0.6 * sosfilt(butter(1, 2000, "highpass", fs=sr, output="sos"), m0)
hop = int(0.1 * sr)
pw = np.array([np.mean(m[i:i + hop] ** 2) for i in range(0, len(m) - hop, hop)])
def gated(a, b):
    seg = pw[int(a / 0.1):int(b / 0.1)]
    if len(seg) == 0: return None
    seg = seg[seg > seg.max() * 1e-3]
    return 10 * np.log10(np.mean(seg) + 1e-12) if len(seg) else None
ref = gated(T + 0.3, min(nxt, T + 16) - 0.3)
if ref is None:
    print("前奏の大きさ: 目安を測れない（そのまま）"); sys.exit(0)
nI = int(T / 0.1)
k = 10                                            # 1秒でならす（3秒だと前奏の後半の山を見のがした）
sm = np.convolve(pw, np.ones(k) / k, mode="same")
E = 10 * np.log10(sm[:nI] + 1e-12)
gdb = np.zeros(nI)
hi_, lo_ = ref + UP, ref - LOW
gdb[E > hi_] = -(E[E > hi_] - hi_)
gdb[E < lo_] = np.minimum(MAX, lo_ - E[E < lo_])
gdb[E < ref - 45] = 0.0                           # 無音（曲の頭の空白など）は上げない
gdb = np.clip(gdb, -CUT, MAX)
# 2026-11-17 人間（17 v8）「前奏のタッピングが急激に小さい音になるのって不自然」「こういうの以前からあった」「今後絶対にやらないように」:
#   ひとりで始まる楽器を +15dB まで持ち上げ、ほかの楽器が入った所で持ち上げをやめていた（17 では 3 秒のあいだに 13.7dB 下げていた）。
#   鳴りつづけている楽器は、その分だけ急に小さく聞こえる。→ 仕上げの持ち上げは LIFT_MAX dB まで、しかも「あとで下げることになる持ち上げ」はしない
#   （前奏の中で、うしろの持ち上げより大きくは上げない）。下げるほうも、1 秒に 0.6dB より速くは下げない（手前から少しずつ）。
#   小さすぎる前奏は、仕上げではなく、その楽器そのものの音量（パートの volume）で直す。たしかめ: tools/vt3/gain_step_check.py
LIFT_MAX = 1.5
lift = np.minimum(np.maximum(gdb, 0), LIFT_MAX); lift = np.minimum.accumulate(lift[::-1])[::-1]
cut = np.minimum(gdb, 0)
for i in range(len(cut) - 2, -1, -1): cut[i] = min(cut[i], cut[i + 1] + 0.06)
cut = np.maximum(cut, -CUT)
gdb = lift + cut
s = 8
gdb = np.convolve(np.pad(gdb, (s, s), mode="edge"), np.ones(s) / s, mode="same")[s:-s]   # 1.5秒でなめらかに
r = min(nI, 4)   # 2026-10-26: 1.2秒かけて戻すと、前奏の最後の山がそのまま残った → 0.4秒
gdb[-r:] *= np.linspace(1, 0, r)                  # 前奏の終わり 0.4秒で元へ
g = np.ones(len(m))
t_hop = np.arange(nI) * hop
g[:nI * hop] = np.interp(np.arange(nI * hop), t_hop, 10 ** (gdb / 20))
y = x * g[:, None]
over = np.abs(y) > 0.9
if over.any():
    y = np.where(over, np.sign(y) * (0.9 + 0.08 * np.tanh((np.abs(y) - 0.9) / 0.08)), y)
sf.write(p, y, sr, subtype=sf.info(p).subtype)
print(f"前奏の大きさ: Aメロの目安 {ref:.1f} dB に合わせた（前奏 {T:.1f}秒・上げ最大 +{max(0, gdb.max()):.1f} dB・下げ最大 {min(0, gdb.min()):.1f} dB）")
