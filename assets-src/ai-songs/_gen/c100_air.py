#!/usr/bin/env python3
# ケルト100曲の「場面の空気」: 本物の環境音の録音（BigSoundBank・CC0相当）を音楽の下に薄く敷く。
# 使い方: python3 c100_air.py 音楽.wav 空気.json 出力.wav
#   空気.json: {"pre": 3.0, "tail": 6.0, "layers": [{"file": "1046", "db": -20, "hp": 80, "lp": 9000, "lfo": [40, 0.35], "pan": 0.0, "wide": 0.012,
#                 "duck": 0.5, "start": 0, "end": null, "fade": 4}], "events": [{"t": 120, "file": "0222", "db": -24, "len": 8, "pan": 0.3, "seek": 10}]}
#   db = 音楽の大きさ（RMS）より何dB小さいか。duck = 音楽が大きいほど空気を下げる強さ（0〜1）。lfo = [周期秒, 深さ]
import sys, json, subprocess, os
import numpy as np
from scipy.signal import butter, sosfilt
SR = 44100
AMB = os.environ.get("AMB_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "ambience"))

def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)

def clip(name):
    for ext in ("mp3", "wav", "ogg"):
        p = os.path.join(AMB, f"{name}.{ext}")
        if os.path.exists(p): return load(p)
    raise FileNotFoundError(name)

def loop_to(x, n, xf=3.0):
    """つなぎ目を等電力でクロスフェードして、n サンプルまで繰り返す"""
    L = len(x); k = int(min(xf * SR, L // 3))
    if L >= n: return x[:n]
    fi = np.sin(np.linspace(0, np.pi / 2, k))[:, None]; fo = np.cos(np.linspace(0, np.pi / 2, k))[:, None]
    out = x.copy()
    while len(out) < n:
        out = np.concatenate([out[:-k], out[-k:] * fo + x[:k] * fi, x[k:]])
    return out[:n]

def filt(x, hp=None, lp=None):
    if hp: x = sosfilt(butter(2, hp, "high", fs=SR, output="sos"), x, axis=0)
    if lp: x = sosfilt(butter(2, lp, "low", fs=SR, output="sos"), x, axis=0)
    return x

def rms_db(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)

def env_db(x, win=3.0):
    m = np.abs(x).mean(1); k = int(win * SR)
    e = np.sqrt(np.convolve(m ** 2, np.ones(k) / k, "same") + 1e-12)
    return 20 * np.log10(e)

def verb_ir(rt=4.0, hp=600, seed=1):
    """低音を含まない、左右で違う長い残響の形（雑音の指数減衰）"""
    rng = np.random.default_rng(seed); n = int(rt * 1.2 * SR); t = np.arange(n) / SR
    ir = rng.standard_normal((n, 2)) * np.exp(-6.9 * t / rt)[:, None]
    ir = filt(ir, hp, 9000); ir[: int(0.03 * SR)] *= np.linspace(0, 1, int(0.03 * SR))[:, None]
    return ir / np.sqrt(np.sum(ir ** 2, axis=0, keepdims=True) + 1e-9)

# 2026-10-29 人間の指示：「空間を支配する」は、空間の音（効果・環境音）で支配するのではなく、
#   音楽の音そのもので耳を気持ちよくして支配すること。→ 作った効果音（glass の倍音・band の息の雑音）は使わない。
#   shimmer・haze はひかえめに。far（音楽そのものの遠い響き）は残す。環境音・録音の出来事は 6dB 下げて、景色の気配にとどめる。
MUSIC_FIRST = {"drop": ("glass", "band"), "fx_db": {"shimmer": -5, "haze": -5, "far": 0}, "air_db": -6, "ramp_max": 1.2}
def fx_layers(M, N, pre, ref, fx):
    """透明な空間音。glass＝高い倍音がゆっくりふくらんで消える（長い残響つき）／shimmer＝音楽の高域を1オクターブ上げて長い残響へ"""
    from scipy.signal import fftconvolve
    out = np.zeros((N, 2)); t = np.arange(N) / SR
    if fx.get("glass"):
        g = fx["glass"]; x = np.zeros((N, 2)); rng = np.random.default_rng(7)
        for k, f in enumerate(g["hz"]):
            for det, pan in ((-0.6, -0.5), (0.7, 0.5)):
                per = 9 + 5 * rng.random(); ph = rng.random() * 6.28
                a = (0.5 + 0.5 * np.sin(2 * np.pi * t / per + ph)) ** 2
                v = np.sin(2 * np.pi * (f + det) * t) * a
                x[:, 0] += v * (1 - pan) * 0.5; x[:, 1] += v * (1 + pan) * 0.5
        x = fftconvolve(x, verb_ir(g.get("rt", 5.0), 500, 3)[:, :1].repeat(2, 1)[:, :], mode="full", axes=0)[:N] if False else x
        L = fftconvolve(x[:, 0], verb_ir(g.get("rt", 5.0), 500, 3)[:, 0])[:N]; R = fftconvolve(x[:, 1], verb_ir(g.get("rt", 5.0), 500, 4)[:, 1])[:N]
        y = np.stack([L, R], 1); y *= 10 ** ((ref + g.get("db", -24) - rms_db(y)) / 20)
        out += y * np.clip((t - g.get("start", 0)) / 6, 0, 1)[:, None]
    if fx.get("shimmer"):
        g = fx["shimmer"]; hi = filt(M, 1500, None)
        import soundfile as sf, tempfile
        tf = tempfile.mktemp(suffix=".wav"); sf.write(tf, hi.astype(np.float32), SR)
        up = load_cmd(["-i", tf, "-af", "asetrate=88200,atempo=0.5,aresample=44100"]); os.remove(tf)
        up = np.concatenate([up, np.zeros((max(0, len(M) - len(up)), 2))])[:len(M)]
        ir = verb_ir(g.get("rt", 6.0), 800, 5)
        y = np.stack([fftconvolve(up[:, 0], ir[:, 0])[:len(M) + 3 * SR], fftconvolve(up[:, 1], ir[:, 1])[:len(M) + 3 * SR]], 1)
        y = y * 10 ** ((ref + g.get("db", -26) - rms_db(y)) / 20)
        z = np.zeros((N, 2)); z[pre:pre + min(len(y), N - pre)] = y[:N - pre]; out += z
    if fx.get("band"):      # 空気の帯: 高域だけの息のようなノイズを、ゆっくり動くバンドパスで揺らす（広さ担当）
        g = fx["band"]; rng = np.random.default_rng(11); n = rng.standard_normal((N, 2))
        fc = g.get("hz", 6500); per = g.get("per", 23)
        lo = fc * (1 + 0.25 * np.sin(2 * np.pi * t / per)); y = np.zeros((N, 2)); blk = SR // 2
        for a in range(0, N, blk):
            f0 = float(lo[min(a, N - 1)]); seg = n[a:a + blk]
            y[a:a + blk] = filt(seg, f0 * 0.7, min(f0 * 1.4, 18000))
        y *= (0.5 + 0.5 * np.sin(2 * np.pi * t / (per * 1.7) + 1.0)) [:, None]
        y *= 10 ** ((ref + g.get("db", -34) - rms_db(y)) / 20); out += y
    if fx.get("far"):       # 遠い反射: 音楽を遅らせて暗くし、遠い壁から返る響きにする（遠さ担当）
        g = fx["far"]; d = int(g.get("delay", 0.18) * SR)
        y = filt(np.roll(M, d, axis=0), 200, g.get("lp", 3000))
        ir = verb_ir(g.get("rt", 3.0), 300, 9)
        y = np.stack([fftconvolve(y[:, 0], ir[:, 0])[:len(M)], fftconvolve(y[:, 1], ir[:, 1])[:len(M)]], 1)[:, ::-1]
        y *= 10 ** ((ref + g.get("db", -22) - rms_db(y)) / 20)
        z = np.zeros((N, 2)); z[pre:pre + len(y)] = y; out += z
    if fx.get("haze"):      # 和音の霞: 音楽の中域をぼかして伸ばし、霧のような層にする
        g = fx["haze"]; y = filt(M, 250, 2500); k = int(g.get("smooth", 1.5) * SR)
        y = np.stack([np.convolve(np.abs(y[:, c]), np.ones(k) / k, "same") * np.sign(np.roll(y[:, c], 0)) for c in (0, 1)], 1) if False else y
        ir = verb_ir(g.get("rt", 8.0), 250, 13)
        y = np.stack([fftconvolve(y[:, 0], ir[:, 0])[:len(M)], fftconvolve(y[:, 1], ir[:, 1])[:len(M)]], 1)
        y *= 10 ** ((ref + g.get("db", -24) - rms_db(y)) / 20)
        z = np.zeros((N, 2)); z[pre:pre + len(y)] = y; out += z
    for sw in fx.get("swells", []):   # 逆再生の吸い込み: 山の直前に、音楽の高域を逆再生して置く（t=山の頭の秒）
        a = int((sw["t"] - sw.get("len", 4)) * SR) + pre; n_ = int(sw.get("len", 4) * SR)
        seg = filt(M[max(0, a - pre):max(0, a - pre) + n_], 600, 9000)[::-1].copy()
        seg *= np.linspace(0, 1, len(seg))[:, None] ** 2
        seg *= 10 ** ((ref + sw.get("db", -20) - rms_db(seg + 1e-9)) / 20)
        out[a:a + len(seg)] += seg
    return out

def load_cmd(args):
    raw = subprocess.run(["ffmpeg", "-v", "error"] + args + ["-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)

def main(mus, spec, outp):
    M = load(mus); pre = int(spec.get("pre", 3.0) * SR); tail = int(spec.get("tail", 6.0) * SR)
    N = pre + len(M) + tail
    music = np.zeros((N, 2)); music[pre:pre + len(M)] = M
    mf = int(spec.get("music_fade", 7.0) * SR)   # 曲の最後を、ぷつっと切らず、なめらかに消す（品質検査の「段差大」の対策。2026-10-28）
    if mf > 0: music[pre + len(M) - mf:pre + len(M)] *= np.linspace(1, 0, mf)[:, None] ** 1.5
    ref = rms_db(M)
    e = env_db(music[::1]) ; med = np.median(e[pre:pre + len(M)])
    air = np.zeros((N, 2))
    for ly in spec["layers"]:
        x = loop_to(clip(ly["file"]), N)
        x = filt(x, ly.get("hp", 80), ly.get("lp", 9000))
        if ly.get("wide"):   # 左右を少しずらして、頭の外に広げる
            d = int(ly["wide"] * SR); x[:, 1] = np.roll(x[:, 1], d)
        pan = ly.get("pan", 0.0)
        x[:, 0] *= min(1, 1 - pan); x[:, 1] *= min(1, 1 + pan)
        x *= 10 ** ((ref + ly.get("db", -20) - rms_db(x)) / 20)
        t = np.arange(N) / SR
        g = np.ones(N)
        if ly.get("lfo"):
            per, dep = ly["lfo"]; g *= 1 - dep + dep * (0.5 + 0.5 * np.sin(2 * np.pi * t / per + ly.get("phase", 0)))
        du = ly.get("duck", 0.5)
        if du: g *= 10 ** (-du * np.clip(e - med, -6, 8) / 20)
        s0 = ly.get("start", 0) * SR; s1 = (ly.get("end") or (N / SR)) * SR; fd = ly.get("fade", 4) * SR
        w = np.clip((np.arange(N) - s0) / fd, 0, 1) * np.clip((s1 - np.arange(N)) / fd, 0, 1)
        air += x * (g * w)[:, None]
    for ev in spec.get("events", []):
        if ev.get("breath"):   # 息の音（笛を口に当てる前の、やわらかい息）：雑音を息の帯域に絞り、ふくらんで消える形にする
            n = int(ev.get("len", 1.4) * SR); rng = np.random.default_rng(int(ev["t"] * 10))
            x = filt(rng.standard_normal((n, 2)) * 0.3, ev.get("hp", 500), ev.get("lp", 3200))
            env = np.sin(np.linspace(0, np.pi, n)) ** 1.6
            x *= env[:, None]; x *= 10 ** ((ref + ev.get("db", -26) - rms_db(x)) / 20)
            pan = ev.get("pan", -0.05); x[:, 0] *= min(1, 1 - pan); x[:, 1] *= min(1, 1 + pan)
            s = pre + int(ev["t"] * SR); air[s:s + len(x)] += x[:max(0, N - s)]
            continue
        if ev.get("pulse"):    # 虫の拍：高い音の短いさえずりを、拍ごとに置く（虫の声が拍を刻む）
            g = ev["pulse"]; rng = np.random.default_rng(5)
            t0, t1, per = g["from"], g["to"], g["every"]; hz = g.get("hz", 4300)
            burst = g.get("burst", 0.045); nb = g.get("n", 3)
            one = int(burst * SR); tt = np.arange(one) / SR
            chirp = np.sin(2 * np.pi * hz * tt) * np.sin(np.pi * tt / burst) ** 2
            unit = np.zeros(int((burst * 1.6) * nb * SR) + one)
            for q in range(nb): a0 = int(q * burst * 1.6 * SR); unit[a0:a0 + one] += chirp * (0.8 + 0.2 * rng.random())
            x = np.zeros((N, 2)); k = 0
            for tb in np.arange(t0, t1, per):
                s0 = pre + int((tb + rng.uniform(-0.01, 0.01)) * SR)
                if s0 + len(unit) >= N: break
                pan = g.get("pan", 0.4) * (1 if k % 2 == 0 else -0.6)
                x[s0:s0 + len(unit), 0] += unit * (1 - pan) * 0.5; x[s0:s0 + len(unit), 1] += unit * (1 + pan) * 0.5; k += 1
            x *= 10 ** ((ref + g.get("db", -30) - rms_db(x[pre + int(t0 * SR):pre + int(t1 * SR)] + 1e-12)) / 20)
            air += x
            continue
        x = clip(ev["file"]); a = int(ev.get("seek", 0) * SR); n = int(ev.get("len", 8) * SR)
        if ev.get("semi"):   # 音の高さを変える（録音の鈴を曲の和音の音に合わせる。再生の速さも変わる）
            r = 2 ** (ev["semi"] / 12.0); idx = np.arange(0, (len(x) - 1), r)
            x = np.stack([np.interp(idx, np.arange(len(x)), x[:, k]) for k in range(2)], axis=1)
        x = filt(x[a:a + n], ev.get("hp", 120), ev.get("lp", 12000))
        x *= 10 ** ((ref + ev.get("db", -24) - rms_db(x)) / 20)
        f = min(len(x) // 3, int(1.5 * SR)); x[:f] *= np.linspace(0, 1, f)[:, None]; x[-f:] *= np.linspace(1, 0, f)[:, None]
        pan = ev.get("pan", 0.0); x[:, 0] *= min(1, 1 - pan); x[:, 1] *= min(1, 1 + pan)
        s = pre + int(ev["t"] * SR); air[s:s + len(x)] += x[:max(0, N - s)]
    air *= 10 ** (MUSIC_FIRST["air_db"] / 20)
    if spec.get("fx"):
        fx = {k: (dict(v, db=v.get("db", -28) + MUSIC_FIRST["fx_db"].get(k, 0)) if isinstance(v, dict) else v)
              for k, v in spec["fx"].items() if k not in MUSIC_FIRST["drop"]}
        fxo = fx_layers(M, N, pre, ref, fx)
        rp = fx.get("ramp")
        if rp: rp = [min(rp[0], MUSIC_FIRST["ramp_max"]), min(rp[1], MUSIC_FIRST["ramp_max"])]
        if rp:   # 曲が進むほど空間の層を深くする（例: [0.3, 2.5]＝始めは弱く、終わりは強く）
            fxo *= np.linspace(rp[0], rp[1], N)[:, None]
        air += fxo
    ig = spec.get("intro_db", 0)
    if ig:   # 前奏が小さすぎないように、はじめの数十秒だけ音楽を持ち上げる（なめらかに戻す）
        tt = np.arange(N) / SR; hold = spec.get("intro_hold", 22); ramp = spec.get("intro_ramp", 10)
        music = music * (10 ** (ig * np.clip(1 - (tt - hold) / ramp, 0, 1) / 20))[:, None]
    out = music + air
    pk = np.abs(out).max()
    if pk > 0.98: out *= 0.98 / pk
    # 書き出し（16bit）
    import soundfile as sf
    sf.write(outp, out.astype(np.float32), SR, subtype="PCM_16")
    print(f"空気を重ねた: {outp}  音楽 {ref:.1f}dB・空気は音楽より約{ref - rms_db(air):.1f}dB 小さい・前 {pre / SR:g}秒・後 {tail / SR:g}秒")

if __name__ == "__main__":
    main(sys.argv[1], json.load(open(sys.argv[2])), sys.argv[3])
