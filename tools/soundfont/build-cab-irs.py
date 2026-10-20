#!/usr/bin/env python3
"""録音のキャビネットIR（assets-src/ir/）を短く切り、作曲ソフト用の tools/composer/cab-irs.ts に書き出す。
使い方: python3 tools/soundfont/build-cab-irs.py
各IRはモノラルにまとめ、最初の 4096 サンプル（44.1kHz で約93ミリ秒）に切って、終わり 20% をなめらかに消す。
データは Float32 を base64 にしたもの。ゲーム本体には入れない（作曲ソフトの entry.ts だけが読み込む）。"""
import base64, os, numpy as np, soundfile as sf
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SETS = {"david-fau-casquel": ("dfc", "David Fau Casquel (CC BY 3.0)"),
        # 2026-10-20 ラウドロック: 作者が自分で録ったキャビネットIR（docs/assets-credits.md）
        "darkdays": ("dd", "Dark Days - https://darkdays.net (CC BY 4.0)"),
        "jester-dyne": ("jd", "Jester Dyne Productions (CC0)")}
N = 4096
lines = ["// 自動生成（tools/soundfont/build-cab-irs.py）。手で書きかえない。",
         "// 録音のキャビネットIR。出どころと規約は docs/assets-credits.md と assets-src/ir/*/README.txt。", "",
         "export const CAB_IRS: { name: string; credit: string; rate: number; b64: string }[] = ["]
for folder, (prefix, credit) in SETS.items():
    d = os.path.join(ROOT, "assets-src/ir", folder)
    for f in sorted(os.listdir(d)):
        if not f.lower().endswith(".wav"): continue
        x, sr = sf.read(os.path.join(d, f), dtype="float32", always_2d=True)
        m = x.mean(1)[:N].copy()
        if len(m) < N: m = np.pad(m, (0, N - len(m)))
        k = int(N * 0.2); m[-k:] *= np.linspace(1, 0, k) ** 2
        name = f"{prefix}-" + os.path.splitext(f)[0].lower().replace(" ", "-")
        lines.append(f'  {{ name: "{name}", credit: "{credit}", rate: {sr}, b64: "{base64.b64encode(m.astype("<f4").tobytes()).decode()}" }},')
        print(name, sr, len(m))
lines.append("];")
open(os.path.join(ROOT, "tools/composer/cab-irs.ts"), "w").write("\n".join(lines) + "\n")
