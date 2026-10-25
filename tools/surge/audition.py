#!/usr/bin/env python3
"""ふるいの点数（PQ）の上位のプリセットを、ステレオで同じフレーズで鳴らして、1本の聴き比べ（mp3）にする。
曲に入れるときと同じ条件（プリセットの中のリバーブ・ディレイを切る→同じ小さな部屋の響きを少し）で鳴らす。
使い方: python3 tools/surge/audition.py ふるいのフォルダ 役割 上位の数 出力.mp3
"""
import ast, csv, os, re, subprocess, sys
import numpy as np, soundfile as sf, pedalboard
from scipy.signal import butter, sosfilt, fftconvolve
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import surgestate as S, screen
from sample import strip_space

SR = 44100


def ranked(d, cat):
    idx = {r[0]: r[1] for r in csv.reader(open(os.path.join(d, cat, "index.csv"), encoding="utf-8"))}
    sc = []
    for line in open(os.path.join(d, cat, "scores.txt"), encoding="utf-8"):
        m = re.match(r"(\S+\.wav) (\{.*\})", line.strip())
        if m and m.group(1) in idx: sc.append((ast.literal_eval(m.group(2))["PQ"], idx[m.group(1)]))
    sc.sort(reverse=True)
    # 似た名前（同じ作者の連番など）は1つだけ
    out, seen = [], set()
    for pq, rel in sc:
        key = re.sub(r"[\s_\-]*\d+$", "", os.path.splitext(os.path.basename(rel))[0]).lower()
        if key in seen: continue
        seen.add(key); out.append((pq, rel))
    return out


def main():
    d, cat, n, outp = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
    top = ranked(d, cat)[:n]
    p = pedalboard.load_plugin(screen.VST)
    ir_n = int(0.8 * SR); rng = np.random.default_rng(3)
    ir = rng.standard_normal((ir_n, 2)) * np.exp(-np.arange(ir_n) / (0.22 * SR))[:, None]
    ir = sosfilt(butter(2, 6500, "low", fs=SR, output="sos"), ir, axis=0); ir /= np.abs(ir).sum(0) / 5
    notes = screen.seq(cat); dur = max(s + dd for _, s, dd, _ in notes) * screen.BEAT + 1.8
    msgs = screen.messages(notes)
    pieces = []; listing = []
    for i, (pq, rel) in enumerate(top, 1):
        S.load_fxp(p, os.path.join(screen.DATA, rel)); p([], duration=0.3, sample_rate=SR, reset=False)
        strip_space(p); p([], duration=0.3, sample_rate=SR, reset=False)
        a = p(msgs, duration=dur, sample_rate=SR, reset=False).T.astype(np.float64)
        p([pedalboard_cc()], duration=1.0, sample_rate=SR, reset=False)
        wet = np.stack([fftconvolve(a[:, c], ir[:, c])[:len(a)] for c in (0, 1)], 1)
        a = a + wet * 0.1
        a = a / (np.sqrt(np.mean(a ** 2)) + 1e-9) * 0.12          # 大きさをそろえる（耳で比べやすく）
        a = np.clip(a, -0.98, 0.98)
        # 番号の合図: 短いクリックを番号の数だけ（10 以上は長いクリック＋残り）
        pieces.append(click_count(i)); pieces.append(a); pieces.append(np.zeros((int(0.5 * SR), 2)))
        listing.append(f"{i}. {os.path.splitext(os.path.basename(rel))[0]}（{rel.split('/')[1] if rel.startswith('patches_3rdparty') else '標準'}・PQ {pq}）")
        print(listing[-1], flush=True)
    x = np.concatenate(pieces)
    wav = outp.rsplit(".", 1)[0] + ".wav"
    sf.write(wav, x.astype(np.float32), SR, subtype="FLOAT")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-c:a", "libmp3lame", "-b:a", "256k", outp]); os.remove(wav)
    open(outp.rsplit(".", 1)[0] + ".txt", "w", encoding="utf-8").write("\n".join(listing) + "\n")


def pedalboard_cc():
    from mido import Message
    return Message("control_change", control=123, value=0)


def click_count(i):
    """番号の合図（高い「ピッ」を番号の数だけ。5ごとに低い「ポッ」）"""
    out = []
    t = np.arange(int(0.03 * SR)) / SR
    hi = np.sin(2 * np.pi * 2000 * t) * np.exp(-t / 0.008) * 0.25
    lo = np.sin(2 * np.pi * 700 * t) * np.exp(-t / 0.015) * 0.35
    fives, ones = divmod(i, 5)
    for _ in range(fives): out += [lo, np.zeros(int(0.12 * SR))]
    for _ in range(ones): out += [hi, np.zeros(int(0.09 * SR))]
    out.append(np.zeros(int(0.35 * SR)))
    m = np.concatenate(out); return np.stack([m, m], 1)


if __name__ == "__main__":
    main()
