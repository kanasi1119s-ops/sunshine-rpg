#!/usr/bin/env python3
# 歌声の「息のような音」を、曲の最初から最後まで全部さがす（2026-11-12 人間「吐息のノイズあるね」「似たようなの他にもないかチェックして」）。
# 使い方: python3 tools/vt3/breath_check.py <歌入りの JSON> [声の番号（既定 0＝主旋律）]
#   その声だけを響きなしで歌わせ（tools/singer/sing.py）、音程のない部分（息・子音のザーッという音）を全部さがして、
#   近くの母音とくらべた大きさを出す。母音との差が −12dB より大きい所が「息のノイズ」に聞こえやすい。
#   目安: −6dB より大きい所は 0 か所、−12dB より大きい所は 全体の1割まで。こえたら debreath を上げる（主旋律・ハモリ・チョップの vocals に "debreath": 1.6 など）。
import sys, os, re, json, subprocess, tempfile
import numpy as np, soundfile as sf


def scan(wav, notes, bpm):
    x, sr = sf.read(wav); x = x.mean(1) if x.ndim > 1 else x
    spb = 60 / bpm; ev = []; t = 0.0
    for tok in notes.split():
        a = tok.split(":"); L = float(re.match(r"[0-9.]+", a[1]).group(0))
        if not tok.startswith("R"): ev.append((t * spb, (t + L) * spb, a[2] if len(a) > 2 else "?"))
        t += L
    N, H = 1024, 240; n = 1 + (len(x) - N) // H
    idx = np.arange(N)[None, :] + (np.arange(n) * H)[:, None]
    per = np.zeros(n); tot = np.zeros(n); hf = np.zeros(n); fq = np.fft.rfftfreq(N, 1 / sr)
    for a in range(0, n, 4000):
        fr = x[idx[a:a + 4000]]; fr = fr - fr.mean(1, keepdims=True); X = np.abs(np.fft.rfft(fr, axis=1)) ** 2
        ac = np.fft.irfft(X, axis=1); ac /= (ac[:, :1] + 1e-12)
        per[a:a + 4000] = ac[:, int(sr / 700):int(sr / 150)].max(1); tot[a:a + 4000] = X.sum(1) + 1e-15; hf[a:a + 4000] = X[:, fq >= 4000].sum(1) / (X.sum(1) + 1e-15)
    db = 10 * np.log10(tot / tot.max()); tt = (np.arange(n) * H + N / 2) / sr
    voiced = (per >= 0.6) & (db > -35); nz = (per < 0.5) & (db > -45)
    segs = []; i = 0
    while i < n:
        if nz[i]:
            k = i
            while k + 1 < n and (nz[k + 1] or (k + 2 < n and nz[k + 2])): k += 1
            d = tt[k] - tt[i] + H / sr
            if d >= 0.03:
                w = voiced & (np.abs(tt - tt[i]) < 0.6); ref = np.median(db[w]) if w.any() else -15
                lab = "?"
                for s0, s1, ly in ev:
                    if s0 - 0.16 <= tt[i] < s0 + 0.05: lab = f"「{ly}」の出だし"; break
                    if s0 + 0.05 <= tt[i] < s1 - 0.02: lab = f"「{ly}」の中"; break
                    if s1 - 0.02 <= tt[i] < s1 + 0.3: lab = f"「{ly}」の終わり"
                segs.append((tt[i], d, db[i:k + 1].max() - ref, hf[i:k + 1].mean(), lab))
            i = k + 1
        else: i += 1
    return segs


def main():
    p = sys.argv[1]; which = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    j = json.load(open(p)); v = j["vocals"][which]
    d = tempfile.mkdtemp(prefix="breath-"); k = dict(j); k["vocals"] = [dict(v, reverb=0, volume=1.0, pan=0)]
    json.dump(k, open(f"{d}/v.json", "w"), ensure_ascii=False)
    here = os.path.dirname(os.path.abspath(__file__))
    subprocess.run([sys.executable, os.path.join(here, "..", "singer", "sing.py"), "render", f"{d}/v.json", f"{d}/v.wav"], check=True, capture_output=True)
    S = scan(f"{d}/v.wav", v["notes"], j["bpm"]); r = np.array([s[2] for s in S]) if S else np.array([])
    big, mid = int((r > -6).sum()), int(((r <= -6) & (r > -12)).sum())
    print(f"■ {j.get('title', '')} 声{which}（debreath {v.get('debreath', 0)}）: 音程のない部分 {len(S)} か所")
    print(f"  母音との差 −6dB より大きい: {big} か所 ／ −6〜−12dB: {mid} か所 ／ −12dB より小さい: {len(S) - big - mid} か所")
    for t0, dd, rel, h, lab in sorted(S, key=lambda s: -s[2])[:12]:
        print(f"    {int(t0 // 60)}:{t0 % 60:05.2f}  長さ {dd:.2f}秒  母音との差 {rel:+5.1f}dB  {'高い息の音' if h > 0.5 else '低めのざらつき'}  {lab}")
    ok = big == 0 and (big + mid) <= max(3, len(S) // 10)
    print("  →", "目安の内" if ok else "息の音が大きい所があります（debreath を上げるか、その言葉を見直す）")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
