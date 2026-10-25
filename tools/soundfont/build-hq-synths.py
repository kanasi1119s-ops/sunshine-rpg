#!/usr/bin/env python3
"""高品質な電子音（2026-10-25 人間「電子音ももっとクオリティ高いのが欲しいな。作り方学んできて」）。

build-modern-synths.py の音色のレシピ（音の中身）はそのまま使い、学んだ作り方で「作り方の質」を上げて作り直す。
調べたことと測った結果は docs/sound/hq-synth-study.md。

  1) 4倍の細かさ（176.4kHz）で作ってから 44.1kHz に戻す。歪み・鋭い波形の高い倍音が折り返して出る
     「ザラザラしたにごり」を消す（測った結果: 今までの音は 4倍で作った音と −27〜−38dB のちがい）。
  2) 1本ずつの音程が、ゆっくり ±数セントゆれる（アナログのシンセのような「生きている」音）。
     ゆれはループの長さの中でちょうど1〜3周するので、ループのつなぎ目は切れない。
  3) ループを 2秒 → 3秒に（くり返しが目立たない）。
  4) 空気の層（7〜14kHz の薄いノイズ。音の大きさについていく）を、伸ばす音にだけ少し。
  5) 180Hz より下は左右をそろえて真ん中に（広がりは中〜高い所で）。
  6) 3帯域の上向きの圧縮を少しだけ（OTT を薄く混ぜる使い方）。
  7) 保存の圧縮を弱く（Vorbis q5 → q7）。

使い方:
  python3 tools/soundfont/build-hq-synths.py [作業フォルダ] [--only 正規表現]   … SF3 を作る（作曲ソフトの音を差しかえる）
  python3 tools/soundfont/build-hq-synths.py [作業フォルダ] --demo 出力.wav    … 前の音と新しい音の聴き比べを作る（SF3 は作らない）
"""
import math, os, re, subprocess, sys
import numpy as np
import soundfile as sf
from numba import njit
from scipy.signal import resample_poly, butter, sosfilt, lfilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OS = 4                      # 何倍の細かさで作るか
BASE = 44100
LOOP_SEC = 3.0

args = sys.argv[1:]
WORK = os.path.abspath(args[0]) if args and not args[0].startswith("--") else "/tmp/hq-synths"
ONLY = re.compile(args[args.index("--only") + 1]) if "--only" in args else None
DEMO = args[args.index("--demo") + 1] if "--demo" in args else None

# ---- 前のレシピを読みこむ（下の「全部作る」部分は使わない） ----
_src = open(os.path.join(HERE, "build-modern-synths.py"), encoding="utf-8").read()
_src = _src[:_src.index("done = []")]
_argv = sys.argv; sys.argv = ["x", "/tmp/hq-synths-unused"]
G = {"__file__": os.path.join(HERE, "build-modern-synths.py"), "__name__": "modern_synths"}
exec(compile(_src, "build-modern-synths.py", "exec"), G)
sys.argv = _argv
INSTR, R, hz = G["INSTR"], G["R"], G["hz"]
_osc0, _lp0 = G["osc"], G["lp"]

# 音色ごとの設定: drift＝音程のゆれ（セント）、air＝空気の層（dB。None でなし）、ott＝圧縮の混ぜる量
CFG = {
    "synth-modern-lead": dict(drift=2.5, air=-34, ott=0.2),
    "synth-modern-supersaw": dict(drift=4.0, air=-32, ott=0.15),
    "synth-modern-fbchord": dict(drift=3.0, air=-33, ott=0.15),
    "synth-modern-pad": dict(drift=4.0, air=-30, ott=0.1),
    "synth-modern-bass": dict(drift=1.0, air=None, ott=0.2),
    "synth-modern-brightlead": dict(drift=3.0, air=-34, ott=0.2),
    "synth-clear-lead": dict(drift=0.8, air=-38, ott=0.1),          # 人間「クリアで揺れの少ない」→ ゆれはごく少し
    "synth-clear-pad": dict(drift=1.2, air=-34, ott=0.1),
    "synth-voice-lead-a": dict(drift=2.0, air=-34, ott=0.15),
    "synth-voice-lead-u": dict(drift=2.0, air=-34, ott=0.15),
    "synth-voice-lead-modern": dict(drift=2.0, air=-36, ott=0.1),
    "synth-pop-lead": dict(drift=1.5, air=-36, ott=0.2),
    "synth-pop-lead-clear": dict(drift=0.8, air=-38, ott=0.15),
    "synth-pico-lead": dict(drift=0.8, air=None, ott=0.15),
    "synth-pico-lead-round": dict(drift=0.8, air=None, ott=0.15),
}
DEFAULT = dict(drift=0.0, air=None, ott=0.0)    # 短い音（プラック・ベル・スタブなど）は 4倍の細かさと左右・保存の改善だけ
STATE = {"drift": 0.0}


def SR(): return G["SR"]


# ---- 速いフィルター（4倍の細かさでも時間がかからないように） ----
@njit(cache=True)
def _svf(x, g, k):
    y = np.zeros_like(x); ic1 = 0.0; ic2 = 0.0
    for i in range(x.shape[0]):
        a1 = 1.0 / (1.0 + g[i] * (g[i] + k)); a2 = g[i] * a1; a3 = g[i] * a2
        v3 = x[i] - ic2
        v1 = a1 * ic1 + a2 * v3
        v2 = ic2 + a2 * ic1 + a3 * v3
        ic1 = 2 * v1 - ic1; ic2 = 2 * v2 - ic2
        y[i] = v2
    return y


def svf_lp(x, fc, q=0.707):
    fc = np.broadcast_to(np.asarray(fc, dtype=np.float64), x.shape)
    g = np.tan(np.pi * np.clip(fc, 20, SR() * 0.45) / SR())
    return _svf(np.ascontiguousarray(x, dtype=np.float64), np.ascontiguousarray(g), 1.0 / q)


def blep_v(p, dt):
    """polyBLEP（dt が配列でもよい版）"""
    y = np.zeros_like(p)
    a = p < dt; t = p[a] / dt[a]; y[a] = t + t - t * t - 1
    b = p > 1 - dt; t = (p[b] - 1) / dt[b]; y[b] = t * t + t + t + 1
    return y


def osc(kind, cyc, L, n, ph0=0.0, pw=0.5):
    """前の osc に「ゆっくりした音程のゆれ」を足したもの。ゆれはループ（L サンプル）の中で 1・2・3 周ちょうど＝つなぎ目が切れない"""
    d = STATE["drift"]
    if d <= 0:
        return _osc0(kind, cyc, L, n, ph0, pw)
    rng = np.random.default_rng((int(cyc) * 1009 + int(ph0 * 1e6)) & 0x7fffffff)
    i = np.arange(n, dtype=np.float64)
    f0 = cyc / L * SR(); Lsec = L / SR()
    wob = np.zeros(n)
    for m in (1, 2, 3):
        c = d * rng.uniform(0.35, 1.0) / m                         # 遅いゆれほど大きく（ピンクノイズ寄り）
        a = f0 * (2 ** (c / 1200) - 1) * Lsec / (2 * np.pi * m)    # 音程のゆれ（Hz）→ 位相のゆれ（周）
        wob += a * np.sin(2 * np.pi * m * i / L + rng.uniform(0, 2 * np.pi))
    p = (ph0 + cyc * i / L + wob) % 1.0
    inc = cyc / L + np.gradient(wob)
    if kind == "saw": return 2 * p - 1 - blep_v(p, inc)
    if kind == "sq": return np.where(p < pw, 1.0, -1.0) + blep_v(p, inc) - blep_v((p - pw) % 1.0, inc)
    if kind == "tri": return 4 * np.abs(p - 0.5) - 1
    if kind == "sin": return np.sin(2 * np.pi * p)
    raise ValueError(kind)


def _ott(x, amt=0.6):
    """前と同じ OTT 風の上向きの圧縮（帯域の分け目は 300Hz・3kHz。細かさに合わせて包絡の速さを直した）"""
    bands = [_lp0(x, 300), G["hp"](_lp0(x, 3000), 300), G["hp"](x, 3000)]
    a = 0.002 * BASE / SR()
    out = np.zeros_like(x)
    for b in bands:
        env = np.sqrt(lfilter([a], [1, -(1 - a)], b * b) + 1e-9)
        g = (np.clip(env, 1e-4, None) / (np.max(env) + 1e-9)) ** (-0.5 * amt)
        out += b * np.minimum(g, 6.0)
    return out


G["svf_lp"] = svf_lp; G["osc"] = osc; G["_ott"] = _ott


def post(l, r, cfg, loop_len):
    """4倍の細かさのまま: 空気の層・低い所を真ん中に・薄い圧縮"""
    s = SR()
    if cfg["air"] is not None:
        rng = np.random.default_rng(len(l))
        L = loop_len or len(l)
        for ch in (0, 1):
            nz = np.resize(rng.standard_normal(L), len(l))            # ループの長さでくり返すノイズ（つなぎ目が切れない）
            nz = sosfilt(butter(2, [7000, 14000], "band", fs=s, output="sos"), nz)
            x = l if ch == 0 else r
            env = np.sqrt(lfilter([200 / s], [1, -(1 - 200 / s)], x * x) + 1e-12)
            rms_n = np.sqrt(np.mean(nz ** 2)) + 1e-12
            add = nz / rms_n * env * 10 ** (cfg["air"] / 20)
            if ch == 0: l = l + add
            else: r = r + add
    m = (l + r) / 2; sd = (l - r) / 2
    sd = sosfilt(butter(2, 180, "high", fs=s, output="sos"), sd)    # 180Hz より下の左右の差をなくす
    l, r = m + sd, m - sd
    if cfg["ott"] > 0:
        l = l * (1 - cfg["ott"]) + _ott(l, 0.6) * cfg["ott"] * 0.5
        r = r * (1 - cfg["ott"]) + _ott(r, 0.6) * cfg["ott"] * 0.5
    return l, r


def render_hq(name, f0, n_base, loop_base, seed):
    """4倍の細かさで作って、44.1kHz に戻す。loop_base: ループの長さ（44.1kHz のサンプル数）か None"""
    d = INSTR[name]; cfg = CFG.get(name, DEFAULT)
    G["SR"] = BASE * OS; STATE["drift"] = cfg["drift"]
    try:
        L = loop_base * OS if loop_base else n_base * OS
        l, r = d["render"](f0, L, n_base * OS, R(seed))
        l, r = post(np.asarray(l, float), np.asarray(r, float), cfg, L if loop_base else None)
    finally:
        G["SR"] = BASE; STATE["drift"] = 0.0
    return resample_poly(l, 1, OS)[:n_base], resample_poly(r, 1, OS)[:n_base]


def render_old(name, f0, n_base, loop_base, seed):
    d = INSTR[name]; G["SR"] = BASE; STATE["drift"] = 0.0
    L = loop_base if loop_base else n_base
    l, r = d["render"](f0, L, n_base, R(seed))
    return np.asarray(l, float), np.asarray(r, float)


# ---------------- 聴き比べ ----------------
def demo(out_path):
    """前の音（2秒ループ・1倍）と新しい音を、同じフレーズで続けて鳴らす。どちらも同じ短い響き（部屋）を少しだけ"""
    sr = BASE
    ir_n = int(0.9 * sr); rng = np.random.default_rng(3)
    ir = rng.standard_normal((ir_n, 2)) * np.exp(-np.arange(ir_n) / (0.25 * sr))[:, None]
    ir = sosfilt(butter(2, 7000, "low", fs=sr, output="sos"), ir, axis=0); ir /= np.abs(ir).sum(0) / 6
    bpm = 128; beat = 60 / bpm
    def note(k): return 440 * 2 ** ((k - 69) / 12)
    # (音色, [(MIDI, 拍)], 和音で鳴らすか)
    lead = [(72, 1), (74, 0.5), (76, 0.5), (79, 1), (84, 1), (83, 0.5), (79, 0.5), (88, 1), (86, 0.5), (84, 0.5), (79, 4)]
    chords = [([60, 64, 67, 71], 4), ([57, 60, 64, 67], 4)]
    arp = [(k, 0.5) for k in (72, 76, 79, 84, 88, 84, 79, 76, 74, 77, 81, 86, 89, 86, 81, 77)]
    bass = [(36, 1.5), (36, 0.5), (43, 1), (41, 1), (33, 2), (40, 2)]
    plan = [("synth-pico-lead-round", lead, False), ("synth-pop-lead-clear", lead, False), ("synth-voice-lead-modern", lead, False),
            ("synth-modern-supersaw", chords, True), ("synth-modern-pluck", arp, False), ("synth-modern-bass", bass, False)]
    pieces = []
    for name, seq, is_chord in plan:
        d = INSTR[name]
        for ver, fn in (("前", render_old), ("新", render_hq)):
            total = sum(b for _, b in seq) * beat + 1.2
            buf = np.zeros((int(total * sr), 2)); t0 = 0.0
            for ks, b in seq:
                dur = b * beat * 0.92
                for k in (ks if is_chord else [ks]):
                    if d.get("loop"):
                        lb = int((LOOP_SEC if ver == "新" else 2.0) * sr); nb = int(d["pre"] * sr) + lb + 2205
                    else:
                        lb = None; nb = int(d["total"] * sr)
                    l, r = fn(name, note(k), nb, lb, k * 7919 + len(name))
                    x = np.stack([l, r], 1)
                    m = min(len(x), int(dur * sr) + int(d["release"] * sr))
                    x = x[:m].copy()
                    rel = int(d["release"] * sr); s0 = max(0, int(dur * sr))
                    if s0 < m: x[s0:] *= np.linspace(1, 0, m - s0)[:, None] ** 2
                    i0 = int(t0 * sr); buf[i0:i0 + m] += x[:len(buf) - i0] * (0.6 / (len(ks) if is_chord else 1) ** 0.5)
                t0 += b * beat
            wet = np.stack([np.convolve(buf[:, c], ir[:, c])[:len(buf)] for c in (0, 1)], 1)
            buf = buf + wet * 0.12
            pieces.append(buf / (np.abs(buf).max() + 1e-9) * 0.8)
            pieces.append(np.zeros((int(0.6 * sr), 2)))
            print(name, ver, flush=True)
        pieces.append(np.zeros((int(0.8 * sr), 2)))
    sf.write(out_path, np.concatenate(pieces).astype(np.float32), sr, subtype="FLOAT")


def build():
    os.makedirs(WORK, exist_ok=True)
    done = []
    for name, d in INSTR.items():
        if ONLY and not ONLY.search(name): continue
        dirp = os.path.join(WORK, name); os.makedirs(dirp, exist_ok=True)
        keys = list(range(d["keys"][0], d["keys"][1] + 1, d["step"]))
        loop = d.get("loop"); lines = []
        for k in keys:
            f0 = hz(k)
            if loop:
                Lb = int(LOOP_SEC * BASE); pre = int(d["pre"] * BASE); nb = pre + Lb + 2205
                l, r = render_hq(name, f0, nb, Lb, k * 7919 + len(name))
                c = round(f0 * Lb * OS / (BASE * OS)); f_eff = c * BASE / Lb
                tune = round(-1200 * math.log2(f_eff / f0))
            else:
                Lb = None; pre = 0; nb = int(d["total"] * BASE)
                l, r = render_hq(name, f0, nb, None, k * 7919 + len(name)); tune = 0
            x = np.stack([l, r], 1)
            if not loop: x -= x.mean(0)
            pk = np.abs(x).max(); assert pk > 1e-6, (name, k)
            x = x / pk * d["level"]
            fade = int(0.003 * BASE); x[:fade] *= np.linspace(0, 1, fade)[:, None]
            sf.write(os.path.join(dirp, f"{name}_{k}.wav"), x.astype(np.float32), BASE, subtype="FLOAT")
            st = d["step"]
            lo = 0 if k == keys[0] else k - st // 2
            hi = 127 if k == keys[-1] else k + (st - st // 2) - 1
            lines.append(f"<region> sample={name}_{k}.wav pitch_keycenter={k} lokey={lo} hikey={hi} tune={tune}" +
                         (f" loop_mode=loop_continuous loop_start={pre} loop_end={pre + Lb}" if loop else ""))
        sfz = os.path.join(dirp, f"{name}.sfz"); open(sfz, "w").write("\n".join(lines) + "\n")
        secs = ((pre + Lb + 2205) / BASE + 0.1) if loop else d["total"]
        cmd = ["node", "tools/soundfont/sfz-to-sf3.mjs", sfz, name, "--program", str(d["program"]), "--seconds", f"{secs:.2f}", "--rr", "1", "--q", "7",
               "--release", str(d["release"]), "--fade", "0.05" if loop else "0.2", "--stereo"]
        if loop: cmd.append("--loop")
        o = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        print(name, (o.stdout.strip().splitlines() or [""])[-1], o.stderr.strip()[-300:], flush=True)
        done.append(name)
    print("作った音色:", ", ".join(done))


if __name__ == "__main__":
    if DEMO: demo(DEMO)
    else: build()
