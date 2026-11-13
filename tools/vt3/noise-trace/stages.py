import sys, json, numpy as np, pickle
sys.path.insert(0, "/home/claude/wt-mix/tools/singer")
import sing, pyworld as pw
from scipy import signal
R = {"syn": [], "post": [], "pol": None}
_syn = pw.synthesize
def syn(f0, sp, ap, sr, fp):
    y = _syn(f0, sp, ap, sr, fp); R["syn"].append((f0.copy(), y.astype(np.float32), sr)); return y
sing.pw.synthesize = syn
_rs = sing.signal.resample_poly
def rs(y, a, b, *k, **kw):
    R["post"].append(np.array(y, dtype=np.float32)); return _rs(y, a, b, *k, **kw)
sing.signal.resample_poly = rs
_pol = sing.polish
def pol(x, sr, vdef):
    y = _pol(x, sr, vdef); R["pol"] = (x.astype(np.float32), y.astype(np.float32)); return y
sing.polish = pol
song = json.load(open(sys.argv[1])); sing.render_song(song, 48000, dry=True)
xin, xout = R["pol"]
H = 240
def fl(x, n0, a, b):
    g = x[n0 + a * H:n0 + b * H].astype(np.float64); return 10 * np.log10(np.mean(g ** 2) + 1e-15)
PH = []
for (f0, y, sr), post in zip(R["syn"], R["post"]):
    p48 = signal.resample_poly(post.astype(np.float64), 48000, sr)
    c = signal.fftconvolve(xin.astype(np.float64), p48[::-1], "valid"); PH.append((int(np.argmax(c)), f0))
def census(x):
    out = []
    for n0, f0 in PH:
        vo = f0 > 0; n = len(f0)
        v = [fl(x, n0, a, a + 1) for a in range(n - 1) if vo[a]]; v = [q for q in v if q > -70]
        if not v: continue
        ref = np.median(v); a = 0
        while a < n - 1:
            if not vo[a]:
                b = a
                while b + 1 < n - 1 and not vo[b + 1]: b += 1
                if (b + 1 - a) >= 4 and fl(xin, n0, a, b + 1) > -75: out.append(fl(x, n0, a, b + 1) - ref)
                a = b + 1
            else: a += 1
    v = np.array(out); return f"声なしの所 {len(v)}  母音との差 中央 {np.median(v):+.1f}dB  大きい側1割 {np.percentile(v, 90):+.1f}dB  −6dB より大きい {int((v > -6).sum())} か所"
vd = song["vocals"][0]; X = xin.astype(np.float64)
def eq_only(x, vdef, base=True, extra=True):
    air = float(vdef.get("air", 1.5)); y = x.copy()
    if base:
        for kind, f, q, db in [("hp", 110, 0.7, 0), ("peak", 280, 1.0, -2.5 - 0.5 * air), ("peak", 3000, 0.9, 2.0), ("peak", 7200, 3.0, -2.5), ("hshelf", 10500, 0.7, air)]:
            b, a = sing.biquad(kind, f, 48000, q, db); y = signal.lfilter(b, a, y)
    if extra:
        for kind, f, q, db in vdef.get("eq", []):
            b, a = sing.biquad(kind, float(f), 48000, float(q), float(db)); y = signal.lfilter(b, a, y)
    return y
print("仕上げの前                      :", census(X))
print("＋基本のEQ（空気 air=%s）         :" % vd.get("air"), census(eq_only(X, vd, True, False)))
print("＋この声のEQ %s:" % vd.get("eq"), census(eq_only(X, vd, True, True)))
print("＋シー取り・コンプ（＝仕上げ全部）:", census(_pol(X, 48000, vd)))
print("  参考: この声のEQなしで仕上げ全部 :", census(_pol(X, 48000, dict(vd, eq=[]))))
print("  参考: EQなし・air 0 で仕上げ全部 :", census(_pol(X, 48000, dict(vd, eq=[], air=0.0))))
