# 仕上げのエフェクト（2026-11-04）。人間が見せてくれた無料のエフェクト（T-Saturator・OTT・Wider・Tape Stop）は Windows と Mac 用で、
#   こちらの書き出しでは動かせないので、同じ働きのものを作った。曲の台本が S.fx に書いた所だけに使う（全曲に一律には入れない）。
#   ボーカルダブラーは歌の合成の中（tools/singer/sing.py の vocalDouble）にある。
# 使い方: python3 vt25_fx.py <wav（上書き）> <場面の秒 .secs> <エフェクト .fx（JSON）>
#   .fx の例: [{"type": "sat", "scenes": ["サビ1"], "drive": 0.4},
#              {"type": "ott", "scenes": "*", "depth": 0.3},
#              {"type": "width", "scenes": ["Aメロ1"], "mode": "left"},   # left＝左だけに寄せる／wide＝広げる（amount）
#              {"type": "tapestop", "at": "end", "dur": 1.6}]            # 最後の dur 秒で、テープが止まるように音程と速さが下がる
import sys, json
import numpy as np
import soundfile as sf
from scipy import signal

wav, secs_p, fx_p = sys.argv[1:4]
x, sr = sf.read(wav, always_2d=True); sub = sf.info(wav).subtype
secs = json.load(open(secs_p)); fx = json.load(open(fx_p))
n = len(x)


def env_for(scenes, ramp=0.25):
    """場面の名前の一覧（"*" は全部）→ 0〜1 の時間の重み（境目は ramp 秒でなめらかに）"""
    e = np.zeros(n)
    for i, s in enumerate(secs[:-1]):
        if scenes == "*" or s["name"] in scenes:
            a, b = int(s["t"] * sr), int(secs[i + 1]["t"] * sr)
            e[max(0, a):min(n, b)] = 1.0
    k = max(1, int(ramp * sr))
    return np.convolve(e, np.ones(k) / k, mode="same")


def sat(y, drive):
    """温かい歪み（T-Saturator のかわり）: 偶数の倍音が少し出る非対称の tanh。低い所は歪ませず、200Hz〜6kHz だけ"""
    b, a = signal.butter(2, [200 / (sr / 2), 6000 / (sr / 2)], "band")
    band = signal.lfilter(b, a, y, axis=0)
    k = 1 + 6 * drive
    w = np.tanh(k * band + 0.08 * drive) / np.tanh(k) - np.tanh(0.08 * drive) / np.tanh(k)
    return y - band + w * (np.sqrt(np.mean(band ** 2)) / (np.sqrt(np.mean(w ** 2)) + 1e-12))


def ott(y, depth):
    """3つの音域に分けて、小さい音を持ち上げ・大きい音を押さえる（OTT のかわり）。depth 0〜1"""
    lo_b, lo_a = signal.butter(4, 120 / (sr / 2), "low"); hi_b, hi_a = signal.butter(4, 2500 / (sr / 2), "high")
    low = signal.filtfilt(lo_b, lo_a, y, axis=0); high = signal.filtfilt(hi_b, hi_a, y, axis=0); mid = y - low - high
    out = np.zeros_like(y)
    for band, up, down in ((low, 4.0, 3.0), (mid, 6.0, 3.0), (high, 8.0, 3.0)):
        lv = np.sqrt(signal.lfilter([0.002], [1, -0.998], (band ** 2).mean(1)) + 1e-12)   # 約 10ms の大きさ
        db = 20 * np.log10(lv); ref = np.percentile(db[db > -80], 70) if (db > -80).any() else -30
        g = np.where(db < ref - 12, np.minimum(up * 1.0, (ref - 12 - db) * 0.5), 0.0)       # 小さい音を持ち上げる
        g = g - np.where(db > ref, (db - ref) * (1 - 1 / down), 0.0)                          # 大きい音を押さえる
        g = signal.lfilter([0.01], [1, -0.99], g)
        out += band * (10 ** (g * depth / 20))[:, None]
    return out


def width(y, mode, amount=0.5):
    m = y.mean(1); s = (y[:, 0] - y[:, 1]) / 2
    if mode == "left":                       # 片耳だけ: 左に寄せる（右は少しだけ残して、片耳のイヤホンの感じ）
        return np.stack([m * 1.25, m * 0.18], 1)
    # 広げる（Wider のかわり）: 横の成分を足し、真ん中の成分の高い所を少しずらした写しで左右に広げる（モノにしても消えない程度）
    b, a = signal.butter(2, 1500 / (sr / 2), "high"); mh = signal.lfilter(b, a, m)
    d = int(0.011 * sr); mh_d = np.concatenate([np.zeros(d), mh[:-d]])
    s2 = s * (1 + amount) + (mh - mh_d) * 0.25 * amount
    return np.stack([m + s2, m - s2], 1)


for f in fx:
    t = f["type"]
    if t == "noise":
        # 01: 街の雑音（ピンクの雑音を 300Hz〜5kHz に）が鳴っていて、場面の終わりで「すっと」消える（ノイズキャンセルが入る瞬間）
        s_ = [s for s in secs if s["name"] == f["scene"]][0]; i_ = secs.index(s_)
        a, b = int(s_["t"] * sr), int(secs[i_ + 1]["t"] * sr)
        w = np.random.default_rng(1).standard_normal((b - a, 2))
        bb, ab = signal.butter(1, [300 / (sr / 2), 5000 / (sr / 2)], "band"); w = signal.lfilter(bb, ab, w, axis=0)
        w = signal.lfilter([1, -0.97], [1, -0.995], w, axis=0)
        w *= 10 ** (float(f.get("db", -22)) / 20) / (np.sqrt(np.mean(w ** 2)) + 1e-12) * np.sqrt(np.mean(x ** 2) + 1e-12) * 3
        L_ = b - a; cut = int(L_ * float(f.get("cut", 0.85)))
        envn = np.ones(L_); envn[cut:] = np.linspace(1, 0, L_ - cut) ** 3; envn[:int(0.6 * sr)] = np.linspace(0, 1, int(0.6 * sr))
        x[a:b] += w * envn[:, None]
        continue
    if t == "tapestop":
        dur = float(f.get("dur", 1.5)); L = int(dur * sr); st = n - L if f.get("at", "end") == "end" else int(float(f["at"]) * sr)
        st = max(0, st); seg = x[st:]
        sp = np.linspace(1.0, 0.0, len(seg)) ** 1.6              # 速さが 1 → 0 へ（はじめはゆっくり、最後に急に止まる）
        pos = np.cumsum(sp); pos = pos - pos[0]
        idx = np.clip(pos, 0, len(seg) - 1); i0 = np.floor(idx).astype(int); fr = idx - i0
        new = seg[i0] * (1 - fr)[:, None] + seg[np.clip(i0 + 1, 0, len(seg) - 1)] * fr[:, None]
        new *= np.linspace(1, 0.0, len(new))[:, None] ** 0.5
        x = np.concatenate([x[:st], new]); n = len(x)
        continue
    e = env_for(f.get("scenes", "*"))[:, None]
    if t == "sat": y = sat(x, float(f.get("drive", 0.4)))
    elif t == "ott": y = ott(x, float(f.get("depth", 0.3)))
    elif t == "width": y = width(x, f.get("mode", "wide"), float(f.get("amount", 0.5)))
    else: continue
    x = x * (1 - e) + y * e
pk = np.abs(x).max()
if pk > 0.97: x *= 0.97 / pk
sf.write(wav, x, sr, subtype=sub)
print("エフェクト:", ", ".join(f["type"] for f in fx))
