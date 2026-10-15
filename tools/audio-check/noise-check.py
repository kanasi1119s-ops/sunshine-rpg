#!/usr/bin/env python3
"""雑音の検知（2026-10-16、人間の指示「雑音検知する項目欲しいかも」）。耳の代わりではなく、場所の候補を出す道具。
書き出した WAV（曲・歌だけ）から、雑音の種類ごとに ○／要直し と、起きた時刻（と小節）を出す。

  python3 tools/audio-check/noise-check.py <WAV> [--vocal] [--notes <歌.py>] [--bpm N] [--json] [--top 5]
    --vocal  : 歌だけの WAV として見る（低い「ボッ」・休みのサー・声の中のザッ・高い所のジリッも見る）
    --notes  : 歌の旋律と歌詞（vocal モジュール: notes() を持つ .py）。声の中の「ザッ」を音符ごとに見る（--vocal と一緒に）
    --bpm    : 時刻に小節番号を添える
    --json   : 結果を JSON で出す（作曲ソフトの合否表に入れるとき）

見る項目:
  プチッ   : 波形がとぎれる・飛ぶ（クリック）。予測の外れ（LPC の残差）が、まわりの 12 倍を超える短い点
  音割れ   : 天井に張りつく（3サンプル以上続けて 0.999 以上）
  直流     : 波形が片側にずれている（直流成分が -50dB を超える）
  超低域   : 20Hz より下のゴー（曲全体に対して -25dB を超える）
  ボッ     : （歌）声のいちばん低い音より下の短い塊（-55dBFS を超える）
  サー     : （歌）休みの所の雑音（声の大きさより 45dB 小さい所より大きく、音の形が平ら＝雑音）
  ザッ     : （歌）音符の中（子音を除く）で、音の形が平ら＝雑音になっている所（30ms 以上）。--notes が要る
  かすれ   : （歌）母音のきれいさ（HNR）が 10dB より下の音。--notes が要る（praat-parselmouth）
  ジリッ   : （歌）8kHz より上が一瞬だけ跳ね上がる所（まわりより 18dB 以上。子音の「さ・し」は除く）
"""
import argparse, json, sys, importlib.util
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfiltfilt, lfilter
from scipy.linalg import solve_toeplitz
from scipy.ndimage import uniform_filter1d, median_filter

def db(x): return 20 * np.log10(np.maximum(x, 1e-12))

def events(mask, fs, min_gap_s=0.02):
    """真偽の並び（サンプルかフレーム）→ 塊の (開始, 終わり) の並び（近いものはまとめる）"""
    idx = np.flatnonzero(mask)
    if not len(idx): return []
    gap = max(1, int(min_gap_s * fs)); out = []; a = b = idx[0]
    for i in idx[1:]:
        if i - b > gap: out.append((a, b)); a = i
        b = i
    out.append((a, b)); return out

def lpc_residual(x, fs, order=16, block_s=0.5):
    """短い区間ごとに LPC で予測し、外れ（残差）を返す。クリックは予測から大きく外れる1〜数サンプルの点になる。"""
    n = len(x); B = int(block_s * fs); r = np.zeros(n)
    for s in range(0, n, B):
        e_ = min(n, s + B); a0 = max(0, s - order); seg = x[a0:e_]
        if e_ - s <= order * 4 or np.max(np.abs(seg)) < 1e-6: continue
        ac = np.array([np.dot(seg[:len(seg) - k], seg[k:]) for k in range(order + 1)])
        if ac[0] <= 0: continue
        ac[0] *= 1.0001
        try: a = solve_toeplitz(ac[:order], ac[1:order + 1])
        except Exception: continue
        e = lfilter(np.concatenate([[1.0], -a]), [1.0], seg)
        r[s:e_] = e[s - a0:]
    return r

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wav"); ap.add_argument("--vocal", action="store_true"); ap.add_argument("--notes", default="")
    ap.add_argument("--bpm", type=float, default=0); ap.add_argument("--json", action="store_true"); ap.add_argument("--top", type=int, default=5)
    a = ap.parse_args()
    x2, fs = sf.read(a.wav, dtype="float64", always_2d=True)
    mono = x2.mean(axis=1)
    bar_s = 240.0 / a.bpm if a.bpm else 0
    def where(t): return f"{t:.2f}秒" + (f"（{int(t / bar_s) + 1}小節目）" if bar_s else "")
    R = []   # (項目, ok, 数, 時刻の並び, 説明)

    # ---- 音割れ（天井に張りつく）----
    clip_ev = []
    for ch in range(x2.shape[1]):
        m = np.abs(x2[:, ch]) >= 0.999
        if m.any():
            run = np.convolve(m.astype(int), np.ones(3, int), "same") >= 3
            clip_ev += [s for s, e in events(run, fs)]
    clip_ev = sorted(set(clip_ev))
    R.append(("音割れ", len(clip_ev) == 0, len(clip_ev), [s / fs for s in clip_ev], "天井に張りついた所"))

    # ---- 直流・超低域 ----
    dc = db(abs(np.mean(mono)))
    R.append(("直流", dc < -50, round(float(dc), 1), [], f"直流成分 {dc:.1f}dB（-50dB 以下で○）"))
    tot = np.sqrt(np.mean(mono ** 2)) + 1e-12
    sub = sosfiltfilt(butter(4, 20, "lowpass", fs=fs, output="sos"), mono - np.mean(mono))
    subdb = db(np.sqrt(np.mean(sub ** 2)) / tot)
    R.append(("超低域", subdb < -25, round(float(subdb), 1), [], f"20Hz より下が全体の {subdb:.1f}dB（-25dB 以下で○）"))

    # ---- プチッ（クリック）----
    hp = sosfiltfilt(butter(2, 1000, "highpass", fs=fs, output="sos"), mono)
    res = lpc_residual(hp, fs)
    ar = np.abs(res)
    loc = median_filter(ar[::4], size=int(0.02 * fs / 4) | 1)       # まわり 20ms の残差の大きさ（中央値）
    loc = np.repeat(loc, 4)[:len(ar)]
    cand = (ar > 12 * (loc + 1e-7)) & (ar > 10 ** (-40 / 20))
    clicks = []
    w = int(0.015 * fs); g = max(2, int(0.0005 * fs))
    for s, e in events(cand, fs, 0.005):
        if e - s > int(0.0006 * fs): continue            # 0.6ms より長いもの（打楽器の立ち上がり・子音）は除く
        i = s + int(np.argmax(ar[s:e + 1]))
        around = np.concatenate([ar[max(0, i - w):max(0, i - g)], ar[i + g:i + w]])
        # 声の「声帯の1回ごとのパルス」や連打は、まわり ±15ms に同じくらいの山がくり返す。ぽつんと1つだけ飛び出すものがクリック
        if len(around) and ar[i] > 4 * around.max(): clicks.append(i)
    # きれいな曲（『スパーク・フロア』の伴奏）と歌では 0 個。わざと入れた 10 個は 10 個とも見つけた（2026-10-16 の確かめ）
    R.append(("プチッ", len(clicks) == 0, len(clicks), [s / fs for s in clicks], "波形の飛び（クリック）"))

    if a.vocal:
        hop = int(0.005 * fs); nfr = len(mono) // hop
        fr_db = db(np.sqrt(np.maximum(0, uniform_filter1d(mono ** 2, hop))[::hop][:nfr]))
        act = fr_db[fr_db > fr_db.max() - 40]; voice_lvl = float(np.median(act)) if len(act) else -20.0
        notes = []
        if a.notes:
            spec = importlib.util.spec_from_file_location("vocal", a.notes); v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
            beat = 60.0 / a.bpm if a.bpm else 0.5
            notes = [(s * beat, d * beat, p) for s, d, p, k in v.notes()]
        # ---- ボッ（声より低い所の塊）----
        low_cut = 180.0
        if notes:
            N = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
            def md(n):
                n = n.replace("Bb", "A#").replace("Eb", "D#").replace("Ab", "G#").replace("Db", "C#").replace("Gb", "F#")
                i = 2 if len(n) > 2 and n[1] == "#" else 1
                return N.index(n[:i]) + 12 * (int(n[i:]) + 1)
            low_cut = min(180.0, 0.7 * 440 * 2 ** ((min(md(p) for _, _, p in notes) - 69) / 12))
        lo = sosfiltfilt(butter(4, [30, low_cut], "bandpass", fs=fs, output="sos"), mono)
        le = db(np.sqrt(np.maximum(0, uniform_filter1d(lo ** 2, int(0.01 * fs)))[::hop][:nfr]))
        thr = voice_lvl - 30
        thumps = [s * 0.005 for s, e in events(le > thr, 200)]
        thump_pk = [float(le[int(t / 0.005):int(t / 0.005) + 20].max()) for t in thumps]
        R.append(("ボッ", len(thumps) <= 3, len(thumps), thumps, f"{low_cut:.0f}Hz より下の短い塊（声より30dB 小さい {thr:.0f}dBFS を超えるもの。いちばん大きい所 {max(thump_pk) if thump_pk else -120:.0f}dBFS）。3か所まで○"))
        # ---- サー（休みの雑音）----
        N2 = 2048; win = np.hanning(N2); hiss = []
        quiet = (fr_db < voice_lvl - 25) & (fr_db > voice_lvl - 90)
        for s, e in events(quiet, 200, 0.0):
            if e - s < 40: continue                      # 0.2秒以上続く静かな所（子音・息つぎは短い）
            c = (s + e) // 2 * hop; seg = mono[c:c + N2]
            if len(seg) < N2: continue
            P = np.abs(np.fft.rfft(seg * win)) ** 2 + 1e-20
            flat = np.exp(np.mean(np.log(P))) / np.mean(P)
            lvl = 10 * np.log10(np.mean(seg ** 2) + 1e-20)
            if flat > 0.3 and lvl > voice_lvl - 75: hiss.append(s * 0.005)
        R.append(("サー", len(hiss) == 0, len(hiss), hiss, "0.2秒以上続く静かな所の、音の形が平らな雑音（声より 75dB 小さい所より大きいもの）"))
        # ---- ジリッ（8kHz より上の一瞬の跳ね上がり）----
        hi = sosfiltfilt(butter(4, 8000, "highpass", fs=fs, output="sos"), mono)
        he = db(np.sqrt(np.maximum(0, uniform_filter1d(hi ** 2, hop))[::hop][:nfr]))
        base = median_filter(he, size=41)
        spike = (he > base + 18) & (he > voice_lvl - 30)
        zz = [s * 0.005 for s, e in events(spike, 200, 0.01) if (e - s) <= 4]   # 20ms 以下だけ（子音の「さ・し」はもっと長い）
        if notes:   # 「か・た・ぱ」などの破裂音（子音）も短く跳ねるので、音符の頭のまわり（前 0.2 秒〜後 0.08 秒）は除く
            zz = [z for z in zz if not any(st - 0.2 <= z <= st + 0.08 for st, d, p in notes)]
        R.append(("ジリッ", len(zz) == 0, len(zz), zz, "8kHz より上が一瞬跳ねる所（20ms 以下。子音の所は除く）"))
        # ---- ザッ（音符の中で声が取れない）----
        if notes:
            # 音符の中（頭の子音と、次の音の子音を除く）で、音の形が平ら（雑音）な所。母音はほぼ 0、子音は 0.2、白い雑音は 0.6 くらい
            starts = sorted(st for st, _, _ in notes)
            win2 = np.hanning(2048); step_s = 0.01; zs_mask = []
            for s, d, p in notes:
                nx = next((st for st in starts if st > s + 1e-6), s + d + 1)
                t = s + 0.12; t1 = min(s + d, nx - 0.25)
                while t < t1:
                    c = int(t * fs); seg = mono[c:c + 2048]
                    if len(seg) == 2048 and 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-12) > voice_lvl - 20:
                        P = np.abs(np.fft.rfft(seg * win2)) ** 2 + 1e-20
                        if np.exp(np.mean(np.log(P))) / np.mean(P) > 0.1: zs_mask.append(t)
                    t += step_s
            zs = []
            for t in zs_mask:   # 30ms 以上続くもの（3フレーム）を1か所に
                if sum(1 for u in zs_mask if t <= u < t + 0.035) >= 3 and (not zs or t - zs[-1] > 0.1): zs.append(t)
            # かすれ: 音ごとの母音のきれいさ（HNR。頭の 0.06 秒と終わりの 0.05 秒を除いた中央値）が 10dB より下の音
            try:
                import parselmouth
                hh = parselmouth.Sound(mono, fs).to_harmonicity_cc(time_step=0.01, minimum_pitch=200)
                kasure = []
                for s, d, p in notes:
                    a_, e_ = s + 0.06, s + d - 0.05
                    if e_ - a_ < 0.06: continue
                    vals = [hh.get_value(t) for t in np.arange(a_, e_, 0.01)]
                    vals = [q for q in vals if q is not None and np.isfinite(q) and q > -100]
                    if vals and np.median(vals) < 10: kasure.append(s)
                R.append(("かすれ", len(kasure) == 0, len(kasure), kasure, "母音のきれいさ（HNR）が 10dB より下の音（息の雑音が多く、ザラついて聞こえる）"))
            except ImportError:
                pass
            R.append(("ザッ", len(zs) == 0, len(zs), zs, "音符の中（子音を除く）で、音の形が平らな雑音になっている所（30ms 以上）"))

    ok = all(r[1] for r in R)
    if a.json:
        print(json.dumps({"ok": ok, "items": [{"name": n, "ok": bool(o), "value": v, "times": [round(float(t), 3) for t in ts[:50]], "note": d} for n, o, v, ts, d in R]}, ensure_ascii=False))
        return
    print(("○ 雑音なし" if ok else "要直し 雑音の疑い") + "  " + " / ".join(f"{n} {'○' if o else '要直し'}({v})" for n, o, v, ts, d in R))
    for n, o, v, ts, d in R:
        if not o:
            print(f"  ・{n}: {d}。{len(ts) if ts else v}か所" + (" 例: " + "、".join(where(t) for t in ts[:a.top]) if ts else ""))

if __name__ == "__main__":
    main()
