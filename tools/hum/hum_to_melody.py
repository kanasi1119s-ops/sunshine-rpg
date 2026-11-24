#!/usr/bin/env python3
"""鼻歌の録音から、旋律を読み取る（2026-11-25 人間「スマホでも鼻歌で曲が作れるようにして」→ 録音をチャットに送ってもらい、ここで読む）。

使い方:
  python3 tools/hum/hum_to_melody.py <録音（m4a・mp3・wav など）> [--bpm 120] [--out <フォルダ>] [--grid 0.5] [--title 名前]
出すもの（<フォルダ>/<名前>.*）:
  .melody.json … テンポ・調・音の並び（音名:拍）・小節ごとの旋律（音名と、調の度数の両方）・和音の案
  .preview.json … 作曲ソフトで鳴らせる下書き（旋律＋自動の伴奏）。node tools/composer/song.mjs build <これ> --wav で聴ける
  画面には、読み取った結果を日本語で出す（どこがあやしいかも）

しくみ: 声の高さを pYIN で読む → 全体の音程のずれ（鼻歌は基準より高め・低めになる）を直す → 半音に丸めて音に分ける（短いゆれ・しゃくりはまとめる）
  → テンポを決める（--bpm が無ければ、音の頭がいちばんマス目に合う速さを探す）→ マス目（既定は8分）にそろえる → 調を決める → 小節に分ける → 小節ごとに和音の案を出す。
読み取りは「下書き」。鼻歌は音程がゆれるので、まちがいは出る。出た旋律を人が聞いて直す前提。"""
import argparse, json, os, subprocess, sys, tempfile
import numpy as np

NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]); MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
nm = lambda m: f"{NAMES[m % 12]}{m // 12 - 1}"


def load(path, sr=22050):
    import soundfile as sf
    tmp = tempfile.mktemp(suffix=".wav"); subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-ac", "1", "-ar", str(sr), tmp], check=True)
    x, _ = sf.read(tmp); os.remove(tmp); return x.astype(np.float32), sr


def track(x, sr):
    """声の高さ（MIDI の小数）と、声が出ているか。10ms ごと"""
    import librosa
    hop = 256; f0, vf, vp = librosa.pyin(x, fmin=70, fmax=1100, sr=sr, frame_length=2048, hop_length=hop, fill_na=np.nan)
    rms = librosa.feature.rms(y=x, frame_length=2048, hop_length=hop)[0][:len(f0)]
    midi = 69 + 12 * np.log2(f0 / 440.0); ok = vf & (vp > 0.25) & (rms > max(1e-4, np.percentile(rms, 90) * 0.06))
    fine = librosa.feature.rms(y=x, frame_length=512, hop_length=hop)[0][:len(f0)]                  # 音の切れ目を見るための、細かい大きさ
    return midi, ok, hop / sr, fine


def tuning(midi, ok):
    """全体の音程のずれ（半音の小数）。半音からのずれの、円のうえの平均"""
    d = (midi[ok] % 1.0) * 2 * np.pi; return float(np.angle(np.mean(np.exp(1j * d))) / (2 * np.pi))


def segment(midi, ok, dt, rms=None, min_len=0.09):
    """半音に丸めて、音に分ける。返すのは [(始まり秒, 長さ秒, MIDI)]"""
    from scipy.signal import medfilt
    m = np.where(ok, midi, np.nan); k = 7
    filled = np.where(np.isnan(m), -1, m); sm = medfilt(filled, k); sm = np.where(filled < 0, np.nan, sm)
    notes = []; cur = None
    for i, v in enumerate(sm):
        if np.isnan(v):
            if cur: notes.append(cur); cur = None
            continue
        if cur and abs(v - np.median(cur[2])) < 0.7: cur[2].append(v); cur[1] = i
        else:
            if cur: notes.append(cur)
            cur = [i, i, [v]]
    if cur: notes.append(cur)
    if rms is not None:                                                   # 同じ高さを続けて歌った所（ん・ん）: 声の大きさの谷で切る
        cut = []; ecut = set()
        for a, b, vs in notes:
            e = rms[a:b + 1]; i0 = 0; w = max(2, int(0.05 / dt))
            if len(e) > 4 * w:
                for i in range(w, len(e) - w):
                    if e[i] == e[max(0, i - w):i + w + 1].min() and e[i] < 0.45 * min(e[max(0, i - 3 * w):i].max(), e[i + 1:i + 3 * w + 1].max()) and (i - i0) * dt >= min_len:
                        cut.append([a + i0, a + i - 1, vs[i0:i]]); i0 = i; ecut.add(a + i)
            cut.append([a + i0, b, vs[i0:]])
        notes = [c for c in cut if len(c[2])]
    else: ecut = set()
    out = [[a * dt, (b - a + 1) * dt, float(np.median(vs)), a in ecut] for a, b, vs in notes]
    # 短すぎる音（しゃくり・ゆれ）は、となりの音にまとめる
    merged = []
    for n in out:
        if merged and n[1] < min_len and n[0] - (merged[-1][0] + merged[-1][1]) < 0.06: merged[-1][1] = n[0] + n[1] - merged[-1][0]; continue
        merged.append(n)
    merged = [n for n in merged if n[1] >= min_len]
    for a, b in zip(merged, merged[1:]):                                   # 前の音の頭のしゃくり（短い低い音 → 本当の音）をまとめる
        if a[1] < 0.12 and 0 < b[2] - a[2] <= 2.2 and b[0] - (a[0] + a[1]) < 0.04: b[1] += b[0] - a[0]; b[0] = a[0]; a[1] = 0
    return [(n[0], n[1], float(n[2]), bool(n[3])) for n in merged if n[1] > 0]


def find_bpm(notes, grid, lo=60, hi=200):
    """音の頭が、いちばんマス目に合う速さ。鼻歌は走ったり遅れたりするので、目安"""
    on = np.array([n[0] for n in notes]) - notes[0][0]; best = None
    for bpm in np.arange(lo, hi + 0.5, 1.0):
        step = 60 / bpm * grid; e = np.abs(on / step - np.round(on / step)); ioi = np.diff(on) / (60 / bpm)
        pen = np.mean(e) + 0.15 * np.mean(ioi < grid * 0.75) + 0.02 * abs(np.log2(np.median(ioi) / 1.0)) if len(ioi) else np.mean(e)      # 音の間は、1拍くらいがふつう
        if best is None or pen < best[0]: best = (pen, bpm)
    return float(best[1]), float(best[0])


def find_key(notes):
    h = np.zeros(12)
    for s, L, m in notes: h[int(round(m)) % 12] += L
    best = None
    for k in range(12):
        for mode, prof in (("major", MAJ), ("minor", MIN)):
            c = np.corrcoef(np.roll(prof, k), h)[0, 1]
            if best is None or c > best[0]: best = (c, k, mode)
    return NAMES[best[1]], best[2], float(best[0])


def fit_scale(notes):
    """鼻歌は音程があいまいなので、「全体のずれ」と「調」をいっしょに探し、音を調の音階に寄せる。
    返すのは (ずれ（半音）, 調の主音の番号, 長調か短調か, 合い具合)。合い具合＝音の長さで重みを付けた、音階の音への近さ"""
    best = None; ps = np.array([n[2] for n in notes]); ws = np.array([min(n[1], 1.0) for n in notes])
    for off in np.arange(-0.5, 0.5, 0.05):
        q = ps - off; h = np.zeros(12)
        for x, w in zip(q, ws): h[int(round(x)) % 12] += w
        for k in range(12):
            for mode, sc, prof in (("major", (0, 2, 4, 5, 7, 9, 11), MAJ), ("minor", (0, 2, 3, 5, 7, 8, 10), MIN)):
                tones = np.array([(k + t) % 12 for t in sc]); d = np.min(np.abs(((q[:, None] - tones[None, :] + 6) % 12) - 6), axis=1)
                fit = float(np.sum(ws * np.exp(-(d / 0.4) ** 2)) / ws.sum()); c = np.corrcoef(np.roll(prof, k), h)[0, 1]; sc_ = fit + 0.25 * c
                if best is None or sc_ > best[0]: best = (sc_, off, k, mode, fit)
    return float(best[1]), best[2], best[3], float(best[4])


def snap(m, k, mode):
    """高さ（小数）を、調の音階のいちばん近い音へ。音階の音から遠く、半音にとても近い時だけ、音階の外の音を残す"""
    sc = (0, 2, 4, 5, 7, 9, 11) if mode == "major" else (0, 2, 3, 5, 7, 8, 10); r = int(round(m)); cand = [x for x in range(r - 2, r + 3) if (x - k) % 12 in sc]
    near = min(cand, key=lambda x: abs(x - m))
    return r if (abs(near - m) > 0.6 and abs(r - m) < 0.15) else near


def degree(m, key, mode):
    sc = [0, 2, 4, 5, 7, 9, 11] if mode == "major" else [0, 2, 3, 5, 7, 8, 10]; k = NAMES.index(key); rel = (m - k) % 12; octv = (m - k) // 12
    if rel in sc: d = str(sc.index(rel) + 1)
    elif (rel - 1) % 12 in sc: d = "#" + str(sc.index((rel - 1) % 12) + 1)
    else: d = "b" + str(sc.index((rel + 1) % 12) + 1)
    return d, octv


def chords_for(bars, key, mode):
    """小節ごとの和音の案（I・IV・V・vi・ii・iii から、その小節の音にいちばん合うもの。強い拍の音を重く見る）"""
    k = NAMES.index(key)
    cand = ([(0, ""), (5, ""), (7, ""), (9, "m"), (2, "m"), (4, "m")] if mode == "major" else [(0, "m"), (5, "m"), (7, ""), (8, ""), (3, ""), (10, "")])
    out = []; prev = None
    for bar in bars:
        best = None
        for off, q in cand:
            tones = {(k + off) % 12, (k + off + (3 if q == "m" else 4)) % 12, (k + off + 7) % 12}; sc = 0.0; t = 0.0
            for name, L in bar:
                if name is not None: sc += (L * (1.5 if abs(t - round(t)) < 1e-6 and int(round(t)) % 2 == 0 else 1.0)) * (1.0 if name % 12 in tones else -0.4)
                t += L
            sc += 0.15 if off == 0 else 0; sc -= 0.1 if (off, q) == prev else 0
            if best is None or sc > best[0]: best = (sc, off, q)
        out.append(NAMES[(k + best[1]) % 12] + best[2]); prev = (best[1], best[2])
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("audio"); ap.add_argument("--bpm", type=float); ap.add_argument("--out", default="."); ap.add_argument("--grid", type=float, default=0.5)
    ap.add_argument("--title"); ap.add_argument("--beats", type=int, default=4); ap.add_argument("--bpm-lo", dest="bpm_lo", type=float, default=70); ap.add_argument("--bpm-hi", dest="bpm_hi", type=float, default=150); a = ap.parse_args()
    x, sr = load(a.audio); midi, ok, dt, rms = track(x, sr)
    if ok.sum() < 20: sys.exit("声が読み取れませんでした（小さすぎる・雑音が大きい・短すぎる）")
    notes = segment(midi, ok, dt, rms)
    if len(notes) < 3: sys.exit("音が3つより少ないです。もう少し長く、はっきり歌ってください")
    off, kroot_, mode, kc = fit_scale(notes); key = NAMES[kroot_]
    sn = []
    for s_, L_, m_, cut_ in notes:                                           # 音階に寄せる。寄せたら同じ高さになった となりの音は、1つにまとめる（声の大きさの谷で切った所は、まとめない）
        m2 = snap(m_ - off, kroot_, mode)
        if sn and sn[-1][2] == m2 and not cut_ and s_ - (sn[-1][0] + sn[-1][1]) < 0.08: sn[-1][1] = s_ + L_ - sn[-1][0]
        else: sn.append([s_, L_, m2])
    notes = [tuple(n) for n in sn]
    bpm, err = (a.bpm, 0.0) if a.bpm else find_bpm(notes, a.grid, a.bpm_lo, a.bpm_hi)
    beat = 60 / bpm; t0 = notes[0][0]; g = a.grid; q = []
    for s, L, m in notes:
        qs = round((s - t0) / beat / g) * g; qe = max(qs + g, round((s + L - t0) / beat / g) * g)
        if q and qs < q[-1][1]: q[-1][1] = qs                                  # 前の音と重なる → 前を縮める
        if q and q[-1][1] <= q[-1][0]: q.pop()
        q.append([qs, qe, m])
    for i in range(len(q) - 1):                                              # 短いすき間（マス1つ）は、前の音をのばしてうめる（息つぎでない切れ目）
        if 0 < q[i + 1][0] - q[i][1] <= g and (q[i + 1][0] - q[i][1]) * beat < 0.25: q[i][1] = q[i + 1][0]
    total = int(np.ceil(q[-1][1] / a.beats)) * a.beats; seq = []; t = 0.0
    for qs, qe, m in q:
        if qs > t: seq.append((None, qs - t))
        seq.append((m, qe - qs)); t = qe
    if total > t: seq.append((None, total - t))
    bars = [[] for _ in range(total // a.beats)]; t = 0.0                       # 小節に分ける（小節をまたぐ音は切る）
    for m, L in seq:
        while L > 1e-9:
            b = int(t // a.beats); room = (b + 1) * a.beats - t; d = min(L, room); bars[b].append((m, d)); t += d; L -= d
    tok = lambda m, L: f"{'R' if m is None else nm(m)}:{L:g}"
    lo, hi = min(m for _, _, m in q), max(m for _, _, m in q); kroot = NAMES.index(key); base_oct = (int(np.median([m for _, _, m in q])) - kroot) // 12

    def dtok(m, L):
        if m is None: return f"R:{L:g}"
        d, o = degree(m, key, mode); o -= base_oct; return f"{d}{chr(39) * o if o > 0 else ',' * (-o)}:{L:g}"
    chords = chords_for(bars, key, mode); name = a.title or os.path.splitext(os.path.basename(a.audio))[0]; os.makedirs(a.out, exist_ok=True)
    res = {"source": os.path.basename(a.audio), "bpm": bpm, "bpm_given": bool(a.bpm), "beats": a.beats, "grid": g, "key": key, "mode": mode, "key_confidence": round(kc, 2), "tuning_offset_cents": round(off * 100),
           "range": [nm(lo), nm(hi)], "note_count": len(q), "bars": [{"notes": " ".join(tok(m, L) for m, L in b), "degrees": " ".join(dtok(m, L) for m, L in b), "chord": c} for b, c in zip(bars, chords)],
           "degree_octave_note": f"度数の 1 は {nm(kroot + 12 * (base_oct + 1))}"}
    json.dump(res, open(f"{a.out}/{name}.melody.json", "w"), ensure_ascii=False, indent=1)
    prev = {"title": f"鼻歌の下書き（{name}）", "description": "仮: 鼻歌から読み取った旋律に、自動の伴奏を付けた下書き", "bpm": int(round(bpm)), "beats": a.beats, "chords": " ".join(chords), "barsPerChord": 1, "repeats": 1,
            "autoAccompaniment": True, "feel": "pop", "tone": "natural", "parts": [{"role": "鼻歌の旋律", "instrument": "lead", "patch": "kfbSineLead", "volume": 0.2, "notes": " ".join(tok(m, L) for b in bars for m, L in b)}]}
    json.dump(prev, open(f"{a.out}/{name}.preview.json", "w"), ensure_ascii=False)
    print(f"■ 鼻歌の読み取り: {os.path.basename(a.audio)}（{len(x) / sr:.1f}秒）")
    print(f"  テンポ {bpm:g}{'（指定）' if a.bpm else f'（自動。マス目とのずれ {err:.2f}。0.15 より大きいと、あやしい）'}・{a.beats}拍子・{len(bars)}小節・マス目 {g}拍")
    print(f"  調 {key} {'長調' if mode == 'major' else '短調'}（音階への合い具合 {kc:.2f}。0.6 より小さいと、あやしい）・音域 {nm(lo)}〜{nm(hi)}・音 {len(q)}こ・全体の音程のずれ {off * 100:+.0f} セント（直して読んだ）")
    for i, b in enumerate(res["bars"]): print(f"  {i + 1:>3}小節め [{b['chord']:>4}] {b['notes']}    （度数: {b['degrees']}）")
    print(f"  → {a.out}/{name}.melody.json ／ 下書き {a.out}/{name}.preview.json")


if __name__ == "__main__": main()
