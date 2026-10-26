#!/usr/bin/env python3
"""02 サイダーカウントダウンに花火の音を入れる（2026-10-26 人間「入れようか」→ 音は花火3版目で決定「この音だね」）。
曲（伴奏・歌）は v24 のまま変えず、仕上がった音に花火を重ねて v25 にする。
  ・縁側の時計（前奏）… 遠くでかすかに1発（今夜は花火大会、の合図）
  ・導火線の終わり   … 打ち上げの「ポンッ…ヒュ〜」
  ・打ち上げ（サビ）頭 … 「ドーン…ゴロゴロ」＋「パチパチ」
  ・打ち上げ 17小節目  … 笛なしで上がって、もう1発
  ・花火のあと        … 遠くで2発（祭りが終わっていく）
使い方: python3 mix_fireworks.py <入力 mp3/wav> <出力 wav> <場面の .secs>"""
import sys, os, json, subprocess, numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fireworks_sfx as F
inp, out, secs = sys.argv[1:4]
x, sr = sf.read(inp) if inp.endswith(".wav") else (None, None)
if x is None:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", inp, "-f", "f32le", "-ac", "2", "-ar", "48000", "-"], capture_output=True, stdin=subprocess.DEVNULL).stdout
    x = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64); sr = 48000
assert sr == F.SR
S = {s["name"]: s["t"] for s in json.load(open(secs))}
bar = 4 * 60 / 178
def rms(a): return np.sqrt(np.mean(a ** 2) + 1e-12)
music = rms(x[int(S["打ち上げ"] * sr):int((S["打ち上げ"] + 10) * sr)])
def duck(t, db, rel=0.7):
    """花火が鳴る瞬間だけ、曲を少し下げて（すぐ戻す）花火を前に出す"""
    i = int(t * sr); a = int(0.015 * sr); r = int(rel * sr); m = 10 ** (db / 20)
    env = np.concatenate([np.linspace(1, m, a), m + (1 - m) * (1 - np.exp(-np.arange(r) / (r / 4)))])
    n = min(len(env), len(x) - i); x[i - a // 2:i - a // 2 + n] *= env[:n, None]
def put(sig, t, db, sat=0):
    """sig を t 秒に、曲の打ち上げの大きさから db だけ下げて置く（頭 0.4 秒の大きさで合わせる）"""
    sig = F.hp(sig, 35)
    if sat: sig = np.tanh(sat * sig / np.abs(sig).max()) / np.tanh(sat)          # ドーンの一瞬のとがりを丸めて、割れずに大きく聞こえるように
    ref = rms(sig[:int(0.4 * sr)]); g = music * 10 ** (db / 20) / ref
    i = int(t * sr); n = min(len(sig), len(x) - i)
    if n <= 0: return
    g0 = g
    while np.abs(x[i:i + n] + sig[:n] * g).max() > 1.25 and g > g0 * 0.2: g *= 0.93   # 割れないように、その1発だけ下げる
    x[i:i + n] += sig[:n] * g
    print(f"  {t:7.2f}秒 {db:+d}dB" + (f" → 割れないよう {20 * np.log10(g / g0):+.1f}dB" if g < g0 else ""))
L = F.launch("whistle"); LP = F.launch("plain")
wl = len(L) - int(1.2 * F.SR)                                    # 打ち上げ音の、余韻を除いた長さ
t0 = S["打ち上げ"]
put(F.boom(dist=3.2, roll=0.7, seed=5), S["縁側の時計"] + 6.2, -24)        # 遠くでかすかに
put(L, t0 - wl / sr - 0.22, -10)
duck(t0, -4.5); put(F.boom(dist=1.4, roll=1.0, seed=1), t0, -3, sat=3.0)
put(F.crackle(), t0 + 0.35, -15)
t1 = t0 + 16 * bar; wp = len(LP) - int(1.2 * F.SR)
put(LP, t1 - wp / sr - 0.15, -16)
duck(t1, -3); put(F.boom(dist=1.7, roll=0.9, seed=7), t1, -6, sat=2.5)
put(F.crackle(sec=2.0, count=300), t1 + 0.4, -18)
put(F.boom(dist=2.6, roll=0.8, seed=9), S["花火のあと"] + 2.3, -14)
put(F.boom(dist=3.0, roll=0.7, seed=4), S["花火のあと"] + 6.8, -18)
peak = np.abs(x).max()
# 1.0 を超える分は、書き出しのリミッターでおさえる（曲全体は下げない）
sf.write(out, x.astype(np.float32), sr, subtype="FLOAT")   # 1.0 を超えても切れないように
print("ok", out, "最大", round(float(peak), 3))
