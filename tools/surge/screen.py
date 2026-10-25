#!/usr/bin/env python3
"""Surge XT のプリセットを、役割ごとの短いフレーズで鳴らして WAV にする（音質の点数でふるいにかけるため）。
2026-10-25 人間「プロ仕様のシンセ入ってると思ってたよ」→ Surge XT（GPL3・無料。鳴らした音は自由に使える）を入れた。
使い方: python3 tools/surge/screen.py 出力フォルダ [役割…]   役割: lead pluck pad keys poly bass
準備（雲）: Surge XT の Linux 版を /opt/surge-xt に展開し、/usr/share/surge-xt → /opt/surge-xt/share/surge-xt のリンク。pip の pedalboard・mido。
"""
import csv, glob, os, sys, time
import numpy as np, soundfile as sf, pedalboard
from mido import Message
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import surgestate as S

VST = os.environ.get("SURGE_VST3", "/opt/surge-xt/lib/vst3/Surge XT.vst3")
DATA = os.environ.get("SURGE_DATA", "/usr/share/surge-xt")
SR = 44100
BEAT = 0.5   # 120 BPM

CATS = {
    "lead": ["patches_factory/Leads", "patches_3rdparty/*/Leads", "patches_3rdparty/*/Lead*"],
    "pluck": ["patches_factory/Plucks", "patches_3rdparty/*/Plucks", "patches_3rdparty/*/Pluck*"],
    "pad": ["patches_factory/Pads", "patches_3rdparty/*/Pads", "patches_3rdparty/*/Pad*"],
    "keys": ["patches_factory/Keys", "patches_3rdparty/*/Keys"],
    "poly": ["patches_factory/Polysynths", "patches_factory/Chords", "patches_3rdparty/*/Synths", "patches_3rdparty/*/Poly*", "patches_3rdparty/*/Chords"],
    "bass": ["patches_factory/Basses", "patches_3rdparty/*/Basses", "patches_3rdparty/*/Bass*"],
}

# 役割ごとのフレーズ: [(MIDI の音, 始まりの拍, 長さの拍, 強さ)]
def seq(cat):
    if cat == "lead":
        m = [(72, 0, 1), (74, 1, 0.5), (76, 1.5, 0.5), (79, 2, 1), (81, 3, 2), (79, 5, 0.5), (76, 5.5, 0.5), (84, 6, 1), (83, 7, 0.5), (79, 7.5, 0.5), (88, 8, 1), (86, 9, 1), (84, 10, 3)]
        return [(k, s, d, 100) for k, s, d in m]
    if cat == "pluck":
        out = []; ch = [[60, 64, 67, 71, 72, 76], [57, 60, 64, 67, 69, 72], [53, 57, 60, 64, 65, 69], [55, 59, 62, 67, 71, 74]]
        for b in range(4):
            for i in range(8): out.append((ch[b][[0, 2, 4, 5, 3, 4, 2, 1][i]] + 12, b * 3.5 + i * 0.5 * 0.875, 0.4, 100))
        return out
    if cat in ("pad", "poly", "keys"):
        ch = [[48, 60, 64, 67, 71], [45, 57, 60, 64, 67], [41, 57, 60, 64, 69], [43, 55, 59, 62, 67]]
        if cat == "poly":   # 刻み（和音のスタブ）と伸ばし
            out = []
            for b in range(4):
                for s in (0, 0.75, 1.5, 2.5):
                    out += [(k, b * 3.5 + s, 0.5, 100) for k in ch[b][1:]]
            return out
        return [(k, b * 3.5, 3.3, 96) for b in range(4) for k in ch[b]]
    if cat == "bass":
        pat = [(36, 0, 0.75), (36, 0.75, 0.25), (36, 1, 0.5), (48, 1.5, 0.5), (36, 2, 1), (43, 3, 0.5), (46, 3.5, 0.5)]
        return [(k + d0, b * 4 + s, d, 105) for b, d0 in enumerate((0, -3, -7, -5)) for k, s, d in pat]
    raise ValueError(cat)


def messages(notes, lead_in=0.3):
    ev = []
    for k, s, d, v in notes:
        ev.append((lead_in + s * BEAT, Message("note_on", note=k, velocity=v)))
        ev.append((lead_in + (s + d) * BEAT, Message("note_off", note=k, velocity=0)))
    ev.sort(key=lambda e: (e[0], e[1].type == "note_on"))
    return [m.copy(time=t) for t, m in ev]


def presets(cat):
    out = []
    for pat in CATS[cat]:
        for d in glob.glob(os.path.join(DATA, pat)):
            out += sorted(glob.glob(os.path.join(d, "**", "*.fxp"), recursive=True))
    return sorted(set(out))


def main():
    outdir = sys.argv[1]; cats = sys.argv[2:] or list(CATS)
    p = pedalboard.load_plugin(VST)
    for cat in cats:
        os.makedirs(os.path.join(outdir, cat), exist_ok=True)
        idx = os.path.join(outdir, cat, "index.csv")
        done = set()
        if os.path.exists(idx):
            done = {r[1] for r in csv.reader(open(idx, encoding="utf-8"))}
        notes = seq(cat); dur = max(s + d for _, s, d, _ in notes) * BEAT + 2.3
        msgs = messages(notes)
        lst = presets(cat); t0 = time.time()
        with open(idx, "a", encoding="utf-8", newline="") as fo:
            w = csv.writer(fo)
            for i, path in enumerate(lst):
                rel = os.path.relpath(path, DATA)
                if rel in done: continue
                try:
                    S.load_fxp(p, path)
                    p([], duration=0.3, sample_rate=SR, reset=False)          # 読みこみを済ませる
                    a = p(msgs, duration=dur, sample_rate=SR, reset=False)
                    p([Message("control_change", control=123, value=0)], duration=1.5, sample_rate=SR, reset=False)   # 全部の音を止めて尾を流す
                except Exception as e:
                    print("×", rel, e, flush=True); continue
                pk = float(np.abs(a).max())
                if pk < 1e-4 or not np.isfinite(pk): print("無音", rel, flush=True); continue
                a = a / pk * 0.7
                name = f"{cat}{i:04d}.wav"
                sf.write(os.path.join(outdir, cat, name), a.mean(0).astype(np.float32), SR, subtype="PCM_16")   # ふるい用はモノ（点数はモノで出す）
                w.writerow([name, rel]); fo.flush()
                if i % 20 == 0: print(cat, i, len(lst), f"{time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
