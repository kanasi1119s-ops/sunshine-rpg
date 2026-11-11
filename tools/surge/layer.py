#!/usr/bin/env python3
"""Surge XT のプリセットを2つ以上重ねて、1つの音源（SF3）にする。
2026-11-11 人間「ハードコアのリードはなんかこもる感じの音がしてキレがない。もう少し繊細で透き通るような感じも入れた方がいい」
→ 芯になる明るいリードに、細くて透き通った音を小さく重ねる。

使い方: python3 tools/surge/layer.py <出力名> --program N --layer "<プリセット>:<大きさ>[:<半音のずらし>[:<低音を切る高さHz>]]" --layer ... [--air 3]
  プリセットは鍵盤とちがうオクターブで鳴ることがある（例: Cut Through は1オクターブ下）。<半音のずらし> を書かなければ自動で測るが、低い音の混じった音はまちがえるので、ふつうは測って書く
  --air: 8kHz から上を何dB持ち上げるか（空気感）
"""
import argparse, os, subprocess, sys
import numpy as np, soundfile as sf, pedalboard
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import surgestate as S, sample as SM
SR = 44100


def octave_of(x, k):
    m = x.mean(1)[int(0.05 * SR):int(0.8 * SR)]; sp = np.abs(np.fft.rfft(m * np.hanning(len(m)))); f = np.fft.rfftfreq(len(m), 1 / SR); exp = 440 * 2 ** ((k - 69) / 12)
    best = None
    for o in (-2, -1, 0, 1, 2):
        f0 = exp * 2 ** o; s = 0
        for h in range(1, 9):
            i = np.argmin(np.abs(f - f0 * h)); s += sp[max(0, i - 3):i + 4].max() / h ** 0.5
        i = np.argmin(np.abs(f - f0 / 2)); s -= 2 * sp[max(0, i - 3):i + 4].max()
        if best is None or s > best[0]: best = (s, o)
    return best[1]


def shelf(x, db, f0=8000):
    if not db: return x
    X = np.fft.rfft(x, axis=0); f = np.fft.rfftfreq(len(x), 1 / SR); g = 1 + (10 ** (db / 20) - 1) / (1 + (f0 / np.maximum(f, 1)) ** 4)
    return np.fft.irfft(X * g[:, None], n=len(x), axis=0)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("name"); ap.add_argument("--program", type=int, required=True); ap.add_argument("--layer", action="append", required=True)
    ap.add_argument("--lo", type=int, default=36); ap.add_argument("--hi", type=int, default=96); ap.add_argument("--step", type=int, default=3); ap.add_argument("--air", type=float, default=0)
    ap.add_argument("--work", default="/tmp/surge-sample"); a = ap.parse_args()
    L = []
    for spec in a.layer:
        q = spec.split(":"); path = q[0] if os.path.exists(q[0]) else os.path.join(SM.DATA, q[0])
        p = pedalboard.load_plugin(SM.VST); S.load_fxp(p, path, strip_space=False); p([], duration=0.3, sample_rate=SR, reset=False)
        SM.render_note(p, 60, 1.0, 0.5); t = SM.render_note(p, 60, 2.0, 0.5)
        sh = int(q[2]) if len(q) > 2 and q[2] != "" else -12 * int(np.median([octave_of(SM.render_note(p, k, 1.5, 0.5), k) for k in (48, 60, 72)]))
        L.append((p, float(q[1]), sh, np.sqrt((t ** 2).mean()), float(q[3]) if len(q) > 3 else 0))
        print(os.path.basename(path), "半音のずらし", sh, flush=True)
    d = os.path.join(a.work, a.name); os.makedirs(d, exist_ok=True); keys = list(range(a.lo, a.hi + 1, a.step)); lines = []
    for k in keys:
        x = 0
        for p, g, sh, rms, hp in L:
            kk = min(120, max(12, k + sh)); v = SM.render_note(p, kk, 5.0, 1.5) * (g * 0.1 / (rms + 1e-9))
            if hp:
                V = np.fft.rfft(v, axis=0); f = np.fft.rfftfreq(len(v), 1 / SR); v = np.fft.irfft(V * (1 / (1 + (hp / np.maximum(f, 1)) ** 6))[:, None], n=len(v), axis=0)
            x = x + v   # 重ねる前に、それぞれの大きさをそろえる
        x = shelf(x, a.air)
        ls, le, c = SM.find_loop(x, int(2.0 * SR), int(4.8 * SR), int(1.2 * SR)); x = SM.crossfade_loop(x, ls, le, int(0.45 * SR)); y = x[:le + 2205]
        on = np.where(np.abs(y).max(1) > np.abs(y).max() * 0.003)[0]; s0 = max(0, (on[0] if len(on) else 0) - 44); y = y[s0:]; ls -= s0; le -= s0
        y = y / (np.abs(y).max() + 1e-12) * 0.8
        fn = f"{a.name}_{k}.wav"; sf.write(os.path.join(d, fn), y.astype(np.float32), SR, subtype="FLOAT")
        lo = 0 if k == keys[0] else k - a.step // 2; hi = 127 if k == keys[-1] else k + (a.step - a.step // 2) - 1
        lines.append(f"<region> sample={fn} pitch_keycenter={k} lokey={lo} hikey={hi} loop_mode=loop_continuous loop_start={ls} loop_end={le}")
        print(k, f"つなぎ目の似ている度合い {c:.3f}", flush=True)
    sfz = os.path.join(d, f"{a.name}.sfz"); open(sfz, "w").write("\n".join(lines) + "\n")
    o = subprocess.run(["node", "tools/soundfont/sfz-to-sf3.mjs", sfz, a.name, "--program", str(a.program), "--seconds", f"{len(y) / SR + 0.2:.2f}", "--rr", "1", "--q", "7",
                        "--release", "0.3", "--fade", "0.05", "--stereo", "--loop"], cwd=SM.ROOT, capture_output=True, text=True)
    print((o.stdout.strip().splitlines() or [""])[-1], o.stderr.strip()[-300:])


if __name__ == "__main__":
    main()
