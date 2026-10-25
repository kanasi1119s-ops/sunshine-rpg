#!/usr/bin/env python3
"""Surge XT のプリセットを、作曲ソフトで鳴らせる SF3 にする（3半音ごとに録る。伸ばす音はループ、減っていく音は1回きり）。
2026-10-25 人間「プロ仕様のシンセ入ってると思ってたよ」→ Surge XT の音を作曲ソフトの音源にする。

使い方: python3 tools/surge/sample.py <プリセット(.fxp。DATA からの相対パスでもよい)> <出力名> --program N [--lo 36 --hi 96 --step 3]
        [--keep-space]（プリセットの中のリバーブ・ディレイを残す。ふだんは切る＝空間は曲の側でつける）
出力: assets-src/soundfont/extra/<出力名>.sf3（sfz-to-sf3.mjs を使う）
"""
import argparse, os, subprocess, sys
import numpy as np, soundfile as sf, pedalboard
from mido import Message
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import surgestate as S

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VST = os.environ.get("SURGE_VST3", "/opt/surge-xt/lib/vst3/Surge XT.vst3")
DATA = os.environ.get("SURGE_DATA", "/usr/share/surge-xt")
SR = 44100
SPACE_FX = ("reverb", "delay", "echo")


def strip_space(p):
    """FX のうち、リバーブ・ディレイの種類のものを切る（音色の歪み・コーラス・EQ などは残す）"""
    off = []
    for k, prm in p.parameters.items():
        if k.endswith("_fx_type"):
            v = str(getattr(p, k)).lower()
            if any(s in v for s in SPACE_FX):
                setattr(p, k, "Off"); off.append(f"{k}={v}")
    return off


def render_note(p, k, hold, tail, vel=100):
    p([Message("control_change", control=123, value=0)], duration=0.6, sample_rate=SR, reset=False)
    a = p([Message("note_on", note=k, velocity=vel, time=0.0), Message("note_off", note=k, velocity=0, time=hold)],
          duration=hold + tail, sample_rate=SR, reset=False)
    return a.T.astype(np.float64)


def find_loop(x, a, b, min_len):
    """a〜b の間で、ループの終わりの手前と始まりがいちばん似ている長さを探す（自己相関）。戻り値 (始まり, 終わり)"""
    m = x.mean(1)
    seg = m[a:b]
    best, bl = -1e9, None
    w = int(0.05 * SR)
    end = b - w
    for L in range(min_len, end - a - w, int(0.002 * SR)):
        s = end - L
        c = np.dot(seg[end - a - w:end - a], seg[s - a - w:s - a]) / (np.linalg.norm(seg[end - a - w:end - a]) * np.linalg.norm(seg[s - a - w:s - a]) + 1e-12)
        if c > best: best, bl = c, L
    return end - bl, end, best


def crossfade_loop(x, ls, le, xf):
    """ループの終わりの前 xf サンプルに、ループの始まりの前の音を等しい力で重ねる（つなぎ目が切れない）"""
    y = x.copy()
    t = np.linspace(0, 1, xf)[:, None]
    y[le - xf:le] = x[le - xf:le] * np.cos(t * np.pi / 2) + x[ls - xf:ls] * np.sin(t * np.pi / 2)
    return y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("preset"); ap.add_argument("name")
    ap.add_argument("--program", type=int, required=True)
    ap.add_argument("--lo", type=int, default=36); ap.add_argument("--hi", type=int, default=96); ap.add_argument("--step", type=int, default=3)
    ap.add_argument("--keep-space", action="store_true")
    ap.add_argument("--q", default="7")
    ap.add_argument("--work", default="/tmp/surge-sample")
    a = ap.parse_args()
    path = a.preset if os.path.exists(a.preset) else os.path.join(DATA, a.preset)
    p = pedalboard.load_plugin(VST)
    S.load_fxp(p, path); p([], duration=0.3, sample_rate=SR, reset=False)
    if not a.keep_space:
        print("切った FX:", strip_space(p) or "なし")
    p([], duration=0.3, sample_rate=SR, reset=False)
    # 伸ばす音か、減っていく音かを決める（真ん中の音を 4 秒のばして、終わりの大きさを見る）
    t = render_note(p, 60, 4.0, 0.5)
    env = np.sqrt(np.convolve(t.mean(1) ** 2, np.ones(2205) / 2205, "same"))
    sustain = env[int(3.4 * SR):int(3.9 * SR)].mean() > env.max() * 10 ** (-24 / 20)
    print("伸ばす音" if sustain else "減っていく音", f"（4秒後の大きさ {20 * np.log10(env[int(3.6 * SR)] / env.max() + 1e-9):.1f}dB）")
    d = os.path.join(a.work, a.name); os.makedirs(d, exist_ok=True)
    keys = list(range(a.lo, a.hi + 1, a.step)); lines = []
    for k in keys:
        if sustain:
            hold, tail = 5.0, 1.5
            x = render_note(p, k, hold, tail)
            ls, le, c = find_loop(x, int(2.0 * SR), int(4.8 * SR), int(1.2 * SR))
            xf = int(0.12 * SR)
            x = crossfade_loop(x, ls, le, xf)
            y = x[:le + 2205]                                           # ループの後ろは使われない（離した音はエンベロープで消す）
            loop = (ls, le)
            print(k, f"ループ {ls / SR:.2f}〜{le / SR:.2f}秒（似ている度合い {c:.3f}）", flush=True)
        else:
            x = render_note(p, k, 6.0, 1.0)
            e = np.sqrt(np.convolve(x.mean(1) ** 2, np.ones(2205) / 2205, "same"))
            cut = np.where(e > e.max() * 10 ** (-60 / 20))[0]
            n = min(len(x), (cut[-1] if len(cut) else len(x)) + 2205)
            y = x[:n].copy(); y[-2205:] *= np.linspace(1, 0, 2205)[:, None]
            loop = None
        # 鳴り始めの遅れを削る（最初の音の手前を 1ms 残す）
        on = np.where(np.abs(y).max(1) > np.abs(y).max() * 0.003)[0]
        s0 = max(0, (on[0] if len(on) else 0) - 44)
        y = y[s0:]
        if loop: loop = (loop[0] - s0, loop[1] - s0)
        y = y / (np.abs(y).max() + 1e-12) * 0.8
        fn = f"{a.name}_{k}.wav"; sf.write(os.path.join(d, fn), y.astype(np.float32), SR, subtype="FLOAT")
        lo = 0 if k == keys[0] else k - a.step // 2
        hi = 127 if k == keys[-1] else k + (a.step - a.step // 2) - 1
        lines.append(f"<region> sample={fn} pitch_keycenter={k} lokey={lo} hikey={hi}" +
                     (f" loop_mode=loop_continuous loop_start={loop[0]} loop_end={loop[1]}" if loop else ""))
        secs = len(y) / SR
    sfz = os.path.join(d, f"{a.name}.sfz"); open(sfz, "w").write("\n".join(lines) + "\n")
    cmd = ["node", "tools/soundfont/sfz-to-sf3.mjs", sfz, a.name, "--program", str(a.program), "--seconds", f"{secs + 0.2:.2f}",
           "--rr", "1", "--q", a.q, "--release", "0.3" if sustain else "0.4", "--fade", "0.05" if sustain else "0.2", "--stereo"]
    if sustain: cmd.append("--loop")
    o = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    print((o.stdout.strip().splitlines() or [""])[-1], o.stderr.strip()[-400:])


if __name__ == "__main__":
    main()
