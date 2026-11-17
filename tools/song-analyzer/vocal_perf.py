#!/usr/bin/env python3
"""歌い方の測定（楽譜なし）: 歌だけの音から、音の終わり方（余韻）・音程の動き方・ビブラートを数字にする（2026-11-17）。
人間「歌の余韻とか音程が素人っぽく」を受けて、お手本の歌（Demucs で分けた歌）と自分の歌を、同じ物差しで比べるために作った。
使い方:
  python3 tools/song-analyzer/vocal_perf.py wav <歌だけの wav> [名前]        … 1つ測る（自分の歌の書き出しなど）
  python3 tools/song-analyzer/vocal_perf.py ia <出力 JSON> 識別子 [識別子 …]  … Internet Archive のネットレーベルの曲を取ってきて、歌を分けて測り、音は消す
決まり（collect_ia.py と同じ）: CC BY・CC BY-SA・CC0 で、netlabels の集まりに入っている作品だけ。音のファイルは測ったら消す。旋律そのものは保存しない（形の数字だけ）。"""
import sys, os, json, warnings
warnings.filterwarnings("ignore")
import numpy as np, soundfile as sf, pyworld as pw
from scipy import signal, ndimage
FP = 0.005

def measure(x, sr):
    x = x.mean(1) if x.ndim > 1 else x
    if sr != 24000: x = signal.resample_poly(x, 24000, sr); sr = 24000
    x = x / (np.abs(x).max() + 1e-9) * 0.9
    f0s = []                                   # 30 秒ずつ測る（長い曲を一度に測るとメモリが足りなくなる）
    for a_ in range(0, len(x), 30 * sr):
        f_, _ = pw.harvest(x[a_:a_ + 30 * sr].astype(np.float64), sr, f0_floor=120, f0_ceil=1100, frame_period=FP * 1000); f0s.append(f_[:int(30 / FP)])
    f0 = np.concatenate(f0s); tt = np.arange(len(f0)) * FP
    w = int(sr * 0.02); env = np.sqrt(np.convolve(x ** 2, np.ones(w) / w, "same")); edb = 20 * np.log10(env[(tt * sr).astype(int).clip(0, len(x) - 1)] + 1e-9)
    loud = np.percentile(edb, 95); voiced = (f0 > 0) & (edb > loud - 35)
    semi = np.where(voiced, 69 + 12 * np.log2(np.maximum(f0, 1) / 440), np.nan)
    n = len(semi); out = {"voiced_share": float(voiced.mean())}
    # 句: 声のある所を、0.12 秒までのすきまはつないで 1 つに
    v2 = ndimage.binary_closing(voiced, np.ones(int(0.12 / FP))); lab, k = ndimage.label(v2); phr = [(np.where(lab == i)[0][0], np.where(lab == i)[0][-1] + 1) for i in range(1, k + 1)]
    phr = [(a, b) for a, b in phr if (b - a) * FP >= 0.4]
    # 音: 中央値フィルターでならした高さが、今の音の平均から 0.7 半音より大きく、0.04 秒以上はなれたら次の音
    segs = []
    for a, b in phr:
        s = semi[a:b]; ok = np.isfinite(s)
        if ok.sum() < 20: continue
        s = np.interp(np.arange(len(s)), np.where(ok)[0], s[ok]); sm = ndimage.median_filter(s, 11)
        st = 0; acc = [sm[0]]; cnt = 0
        for i in range(1, len(sm)):
            if abs(sm[i] - np.median(acc)) > 0.7:
                cnt += 1
                if cnt >= 8:
                    segs.append((a + st, a + i - 8, float(np.median(acc)), a, b)); st = i - 8; acc = list(sm[i - 8:i + 1]); cnt = 0
            else:
                cnt = 0; acc.append(sm[i])
        segs.append((a + st, b, float(np.median(acc)), a, b))
    D = np.array([(e - s) * FP for s, e, _, _, _ in segs])
    if len(segs) < 30: out["too_few"] = True; return out
    out["notes"] = len(segs); out["note_sec_median"] = float(np.median(D)); out["note_ge_0.5s_pct"] = float(100 * np.mean(D >= 0.5)); out["note_ge_1s_pct"] = float(100 * np.mean(D >= 1.0))
    # 余韻: 句の終わり
    rel, fade, lastlen, fall = [], [], [], []
    for a, b in phr:
        if b + int(0.3 / FP) >= n or voiced[b + 2:b + int(0.25 / FP)].any(): continue
        mine = [g for g in segs if g[3] == a]; 
        if not mine: continue
        ls, le, lm = mine[-1][0], mine[-1][1], mine[-1][2]; L = (le - ls) * FP; lastlen.append(L)
        mid = edb[ls + int(0.2 * (le - ls)):ls + int(0.7 * (le - ls)) + 1]
        if len(mid) == 0: continue
        ref = np.median(mid); tail = edb[b - int(0.03 / FP):b + int(1.5 / FP)]; w_ = np.where(tail < ref - 20)[0]; rel.append((w_[0] * FP - 0.03) if len(w_) else 1.5)
        fade.append(float(np.mean(edb[max(ls, b - int(0.1 / FP)):b]) - ref))
        s1 = semi[b - int(0.1 / FP):b]; 
        if np.isfinite(s1).sum() >= 8 and L >= 0.3: fall.append(100 * (np.nanmedian(s1) - lm))
    q = lambda v: [float(np.percentile(v, p)) for p in (25, 50, 75)] if len(v) else None
    out["phrases"] = len(phr); out["release_ms_-20dB"] = [1000 * z for z in q(rel)] if rel else None; out["end_fade_db"] = q(fade); out["last_note_sec"] = q(lastlen); out["end_pitch_cents"] = q(fall)
    out["last_note_ge_0.5s_pct"] = float(100 * np.mean(np.array(lastlen) >= 0.5)) if lastlen else None
    # 音程の移り
    tr, ov, tri = [], [], []
    for i in range(1, len(segs)):
        A_, B_ = segs[i - 1], segs[i]
        if A_[3] != B_[3] or abs(B_[2] - A_[2]) < 1.0 or (A_[1] - A_[0]) < 16 or (B_[1] - B_[0]) < 16: continue
        iv = B_[2] - A_[2]; lo = max(A_[0], B_[0] - 60); hi = min(B_[1], B_[0] + 60); s = semi[lo:hi]
        if np.isfinite(s).mean() < 0.9: continue
        s = np.interp(np.arange(len(s)), np.where(np.isfinite(s))[0], s[np.isfinite(s)]); z = (s - A_[2]) / iv
        i8 = np.where(z >= 0.8)[0]
        if not len(i8): continue
        i8 = i8[0]; i2 = np.where(z[:i8] <= 0.2)[0]
        if not len(i2): continue
        tr.append((i8 - i2[-1]) * FP); tri.append(abs(iv))
        after = z[i8:i8 + int(0.15 / FP)]; ov.append(float(100 * max(0.0, after.max() - 1)))
    out["transition_ms_20_80"] = [1000 * z for z in q(tr)] if tr else None; out["overshoot_pct"] = q(ov); out["transitions"] = len(tr)
    # 音の中の動き
    wob, drift, scoop, vib_n, vib_d, vib_r, vib_on, longn = [], [], [], 0, [], [], [], 0
    for s0, e0, m, a, b in segs:
        L = (e0 - s0) * FP; c = 100 * (semi[s0:e0] - m); ok = np.isfinite(c)
        if ok.sum() < 30: continue
        c = np.interp(np.arange(len(c)), np.where(ok)[0], c[ok])
        if L >= 0.25:
            core = c[8:-6]; tr_ = ndimage.uniform_filter1d(core, 31); wob.append(float(np.std(core - tr_))); th = len(core) // 3; drift.append(float(np.median(core[-th:]) - np.median(core[:th])))
        if s0 == a and L >= 0.2: scoop.append(float(np.median(c[:8]) - np.median(c[len(c) // 2:])))
        if L >= 0.5:
            longn += 1; z = c - ndimage.uniform_filter1d(c, 41); z = z[6:-4]
            sp = np.abs(np.fft.rfft(z * np.hanning(len(z)), 2048)); fr = np.fft.rfftfreq(2048, FP); band = (fr >= 4) & (fr <= 8)
            pk = sp[band].max(); half = z[len(z) // 2:]; dep = float(np.std(half) * 1.414)
            if pk > 3.5 * np.median(sp[(fr > 1) & (fr < 25)]) and dep >= 10:
                vib_n += 1; vib_d.append(dep); vib_r.append(float(fr[band][sp[band].argmax()]))
                amp = np.sqrt(ndimage.uniform_filter1d(z ** 2, 30)) * 1.414; on = np.where(amp >= 0.5 * dep)[0]; vib_on.append(float(on[0] * FP + 0.03) if len(on) else 0.0)
    out["wobble_cents"] = q(wob); out["drift_cents"] = q(drift); out["scoop_cents"] = q(scoop)
    out["long_notes"] = longn; out["vibrato_share_pct"] = float(100 * vib_n / max(1, longn)); out["vibrato_depth_cents"] = q(vib_d); out["vibrato_rate_hz"] = q(vib_r); out["vibrato_onset_sec"] = q(vib_on)
    return out

def show(name, o):
    f = lambda v, u="": "—" if v is None else f"{v[1]:.0f}{u}（{v[0]:.0f}〜{v[2]:.0f}）"
    if o.get("too_few"): print(f"■ {name}: 歌として測れる所が少ない（声のある時間 {100*o['voiced_share']:.0f}%）"); return
    print(f"■ {name}: 声のある時間 {100*o['voiced_share']:.0f}%・音 {o['notes']}・句 {o['phrases']}")
    print(f"  音の長さ 中央値 {o['note_sec_median']:.2f}秒／0.5秒以上 {o['note_ge_0.5s_pct']:.0f}%／1秒以上 {o['note_ge_1s_pct']:.0f}%／句の最後の音 {o['last_note_sec'][1]:.2f}秒（0.5秒以上 {o['last_note_ge_0.5s_pct']:.0f}%）")
    print(f"  余韻: −20dB まで {f(o['release_ms_-20dB'],'ms')}／終わり 0.1秒の大きさ {f(o['end_fade_db'],'dB')}／終わりの音程 {f(o['end_pitch_cents'],'c')}")
    print(f"  音程の移り: {f(o['transition_ms_20_80'],'ms')}／行きすぎ {f(o['overshoot_pct'],'%')}（{o['transitions']}回）／音の中のゆれ {f(o['wobble_cents'],'c')}／音の中の流れ {f(o['drift_cents'],'c')}／句の頭 {f(o['scoop_cents'],'c')}")
    print(f"  ビブラート: 長い音 {o['long_notes']} のうち {o['vibrato_share_pct']:.0f}%／深さ {f(o['vibrato_depth_cents'],'c')}／速さ {('%.1f' % o['vibrato_rate_hz'][1]) if o['vibrato_rate_hz'] else '—'}Hz／かかり始め {('%.2f' % o['vibrato_onset_sec'][1]) if o['vibrato_onset_sec'] else '—'}秒")

if __name__ == "__main__":
    if sys.argv[1] == "wav":
        x, sr = sf.read(sys.argv[2]); o = measure(x, sr); show(sys.argv[3] if len(sys.argv) > 3 else os.path.basename(sys.argv[2]), o)
        if len(sys.argv) > 4: json.dump(o, open(sys.argv[4], "w"), ensure_ascii=False, indent=1)
    elif sys.argv[1] == "mix":    # 仕上がった曲（mp3 など）から歌を分けて測る: mix <曲> [名前] [出力 JSON]
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import analyze as A
        st = A.separate(A.load_audio(sys.argv[2])); vv = np.array(st["vocals"]); del st; import gc; gc.collect()
        o = measure(vv.T if vv.ndim > 1 and vv.shape[0] < vv.shape[1] else vv, A.SR); show(sys.argv[3] if len(sys.argv) > 3 else os.path.basename(sys.argv[2]), o)
        if len(sys.argv) > 4: json.dump(o, open(sys.argv[4], "w"), ensure_ascii=False, indent=1)
    else:
        import urllib.request, urllib.parse
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import analyze as A
        OK = ("creativecommons.org/licenses/by/", "creativecommons.org/licenses/by-sa/", "creativecommons.org/publicdomain/zero/")
        outp = sys.argv[2]; res = json.load(open(outp)) if os.path.exists(outp) else {}; os.makedirs("/tmp/sa/ref", exist_ok=True)
        for ident in sys.argv[3:]:
            if ident in res: continue
            try:
                d = json.load(urllib.request.urlopen(f"https://archive.org/metadata/{ident}", timeout=60)); m = d["metadata"]; lic = str(m.get("licenseurl", "")); col = m.get("collection", []); col = [col] if isinstance(col, str) else col
                if not any(o in lic for o in OK) or "netlabels" not in col: print(f"× {ident}: 条件に合わない"); continue
                def secs(x):
                    try:
                        if ":" in str(x): p = [float(q) for q in str(x).split(":")]; return sum(v * 60 ** i for i, v in enumerate(reversed(p)))
                        return float(x)
                    except Exception: return 0
                c = [f for f in d["files"] if f["name"].lower().endswith(".mp3") and "_64kb" not in f["name"] and 110 <= secs(f.get("length", 0)) <= 400]
                if not c: print(f"× {ident}: 曲がない"); continue
                f = c[min(1, len(c) - 1)] if len(c) > 2 else c[0]      # collect_ia.py と同じ曲（アルバムの2曲目）
                path = f"/tmp/sa/ref/{ident}.mp3"; urllib.request.urlretrieve(f"https://archive.org/download/{ident}/" + urllib.parse.quote(f["name"]), path)
                wav = A.load_audio(path); st = A.separate(wav); os.remove(path)
                vv = np.array(st["vocals"]); del st, wav; import gc; gc.collect()
                o = measure(vv.T if vv.ndim > 1 and vv.shape[0] < vv.shape[1] else vv, A.SR)
                o["source"] = dict(title=str(f.get("title") or f["name"]), creator=str(f.get("creator") or m.get("creator")), license=lic, url=f"https://archive.org/details/{ident}")
                res[ident] = o; json.dump(res, open(outp, "w"), ensure_ascii=False, indent=1); show(ident, o); sys.stdout.flush()
            except Exception as e: print(f"× {ident}: {type(e).__name__} {e}"); sys.stdout.flush()
