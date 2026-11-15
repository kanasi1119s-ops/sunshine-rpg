#!/usr/bin/env python3
"""曲の分析ソフト・段3: 分けた音ごとに「音の性格」（音色）を測る（2026-11-16）。analyze.py から呼ばれる。
測るもの（音そのものは保存しない。数字だけ）:
  ・明るさ（音の重心・高い音の割合）と、帯ごとの大きさ
  ・倍音の形（ベース・歌）: 倍音の下がり方（のこぎり波は1オクターブで約 −6dB）、奇数の倍音と偶数の倍音の差（四角い波は奇数が強い）
  ・ざらつき（音程のない成分の割合）
  ・立ち上がり（10% → 90% にかかる時間）と、余韻（頭から −10dB まで落ちる時間）、のばしている間の大きさ
  ・ゆれ: 拍に合わせたへこみ（キックでへこませるポンプ）の深さ、歌のビブラート（速さ・深さ）
  ・左右の広がり（低い所・高い所）
  ・つぶし具合（いちばん大きい所と、ふだんの大きさの差）
  ・ドラム: キックの高さと長さと「カチッ」の強さ、スネアの胴の高さ・明るさ・余韻、ハイハットの明るさ
最後に、作曲ソフトの音づくりの言葉（波形・フィルター・立ち上がり・ポンプ・広げ方）に直した「音づくりのヒント」を出す。
答え合わせ: tools/song-analyzer/eval3.py（中身の分かっている音を作って測る）。"""
import numpy as np

SR = 44100
BANDS = [("とても低い（〜60Hz）", 20, 60), ("低い（60〜120Hz）", 60, 120), ("低めの中（120〜250Hz）", 120, 250), ("中の下（250〜500Hz）", 250, 500), ("中（500Hz〜1kHz）", 500, 1000),
         ("中の上（1〜2kHz）", 1000, 2000), ("高め（2〜4kHz）", 2000, 4000), ("高い（4〜8kHz）", 4000, 8000), ("とても高い（8kHz〜）", 8000, 20000)]


def _db(x): return 20 * np.log10(np.maximum(x, 1e-9))


def _env(x, win=1024, hop=128):
    """大きさの線（win の長さでならした RMS）。低い音は波の1周期が長い（ミ1 で 24ミリ秒）ので、短い窓だと波の形そのものを拾ってしまう"""
    c = np.cumsum(np.concatenate([[0.0], x.astype(np.float64) ** 2])); i = np.arange(0, max(1, len(x) - win), hop); return np.sqrt((c[i + win] - c[i]) / win + 1e-12)


def _spec(mono, n_fft=4096, hop=1024):
    import librosa
    S = np.abs(librosa.stft(mono, n_fft=n_fft, hop_length=hop)); f = librosa.fft_frequencies(sr=SR, n_fft=n_fft); e = np.sqrt((S ** 2).mean(0)); act = e > np.percentile(e, 95) * 0.1
    return S, f, act


def tone(st):
    """明るさ・帯ごとの大きさ・ざらつき・左右の広がり・つぶし具合。st: (2, n) の音"""
    import librosa
    mono = st.mean(0); S, f, act = _spec(mono)
    if act.sum() < 20: return None
    P = (S[:, act] ** 2).mean(1); tot = P.sum() + 1e-12; cen = float((f * P).sum() / tot); cum = np.cumsum(P) / tot; roll = float(f[np.searchsorted(cum, 0.85)])
    bands = {n: round(float(10 * np.log10(P[(f >= a) & (f < b)].sum() / tot + 1e-12)), 1) for n, a, b in BANDS}
    flat = float(np.median(librosa.feature.spectral_flatness(S=S[:, act] + 1e-9)))
    H, Pp = librosa.decompose.hpss(S[:, act][:, ::2]); noise = float((Pp ** 2).sum() / ((H ** 2).sum() + (Pp ** 2).sum() + 1e-12))
    mid, side = st.mean(0), (st[0] - st[1]) / 2
    def width(a, b):
        import scipy.signal as ss
        sos = ss.butter(4, [a, b], btype="band", fs=SR, output="sos"); m, s = ss.sosfilt(sos, mid), ss.sosfilt(sos, side); return round(float(np.sqrt((s ** 2).mean()) / (np.sqrt((m ** 2).mean()) + 1e-9)), 2)
    hop = 2048; n = len(mono) // hop; r = np.sqrt((mono[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12); ra = r[r > np.percentile(r, 95) * 0.1]
    return {"音の重心（Hz）": round(cen), "高い音の境目（85%がこれより下・Hz）": round(roll), "帯ごとの大きさ（dB・全体を0として）": bands, "ざらつき（0〜1）": round(flat, 4), "打つ音の成分の割合": round(noise, 3),
            "左右の広がり（低い所 〜250Hz）": width(40, 250), "左右の広がり（中 250Hz〜2kHz）": width(250, 2000), "左右の広がり（高い所 2kHz〜）": width(2000, 12000),
            "いちばん大きい所とふだんの差（dB）": round(float(_db(np.abs(mono).max()) - _db(np.sqrt((mono ** 2).mean()))), 1), "大きさのゆれ幅（dB・鳴っている所）": round(float(np.percentile(_db(ra), 90) - np.percentile(_db(ra), 10)), 1)}


def harmonics(mono, f0, t_f0, n_h=10):
    """倍音の形（音程のある単音の楽器: ベース・歌）。f0: 音の高さ（Hz、無い所は NaN）、t_f0: その時刻"""
    import librosa
    n_fft = 8192; hop = 2048; S = np.abs(librosa.stft(mono, n_fft=n_fft, hop_length=hop)); t = np.arange(S.shape[1]) * hop / SR; fr = SR / n_fft; amps = []
    for j in range(S.shape[1]):
        i = np.searchsorted(t_f0, t[j]);
        if i >= len(f0) or np.isnan(f0[i]) or f0[i] * n_h > SR / 2 - 200: continue
        a = []
        for h in range(1, n_h + 1):
            k = int(round(f0[i] * h / fr)); a.append(S[max(0, k - 2):k + 3, j].max())
        if a[0] > 1e-4 or max(a) > 1e-3: amps.append(a)
    if len(amps) < 30: return None
    A = np.array(amps); A = A / (np.sqrt((A ** 2).sum(1, keepdims=True)) + 1e-12); m = _db(np.sqrt((A ** 2).mean(0))); m = m - m.max()
    x = np.log2(np.arange(1, n_h + 1)); slope = float(np.polyfit(x, m, 1)[0]); odd = float(np.mean(m[[2, 4, 6, 8]])); even = float(np.mean(m[[1, 3, 5, 7]]))
    kind = ("のこぎり波に近い" if -9 < slope < -3.5 and abs(odd - even) < 5 else "四角い波に近い（奇数の倍音が強い）" if odd - even >= 5 else "サイン波に近い（倍音が少ない）" if slope <= -9
            else "倍音がとても多い（歪み・FM・ブラスのような音）" if slope >= -3.5 else "まざった形")
    return {"倍音の大きさ（dB・いちばん大きい倍音を0として・1番目〜10番目）": [round(float(v), 1) for v in m], "倍音の下がり方（dB／オクターブ）": round(slope, 1), "奇数の倍音 − 偶数の倍音（dB）": round(odd - even, 1),
            "基音がいちばん大きい": bool(np.argmax(m) == 0), "波の形（たぶん）": kind}


def envelope(mono, onsets_t, max_len=1.2):
    """立ち上がりと余韻: 音の頭（onsets_t・秒）にそろえて、大きさの線の平均をとる"""
    hop = 128; e = _env(mono, 1024, hop); n = len(e); L = int(max_len * SR / hop); pre = int(0.04 * SR / hop); segs = []      # 窓が 23ミリ秒なので、立ち上がりは 20ミリ秒より短くは測れない
    ot = np.sort(np.array(onsets_t))
    for k, t in enumerate(ot):
        i = int(t * SR / hop); nx = int(ot[k + 1] * SR / hop) if k + 1 < len(ot) else n
        if i - pre < 0 or i + 8 >= n: continue
        s = e[i - pre:min(i + L, nx, n)]
        if len(s) < pre + 12 or s.max() < np.percentile(e, 60): continue
        segs.append(s / s.max())
    if len(segs) < 8: return None
    att, dec, sus = [], [], []
    for s in segs:
        p = int(np.argmax(s[:pre + int(0.25 * SR / hop)])); a10 = np.where(s[:p + 1] >= 0.1)[0]; a90 = np.where(s[:p + 1] >= 0.9)[0]
        if len(a10) and len(a90): att.append((a90[0] - a10[0]) * hop / SR * 1000)
        after = s[p:] / s[p]; d = np.where(after <= 10 ** (-10 / 20))[0]; dec.append((d[0] if len(d) else len(after)) * hop / SR * 1000); full = not len(d)
        j = p + int(0.2 * SR / hop)
        if j < len(s): sus.append(float(_db(s[j])))
    return {"立ち上がり（ミリ秒・10%→90%。20より短くは測れない）": round(float(np.median(att)), 1) if att else None, "頭から −10dB まで落ちる時間（ミリ秒・中央値。次の音まで落ちなければ、次の音までの長さ）": round(float(np.median(dec))),
            "頭から0.2秒あとの大きさ（dB・頭を0として）": round(float(np.median(sus)), 1) if sus else None, "測った音の数": len(segs)}


def pump(mono, beats):
    """拍に合わせたへこみ（キックで伴奏をへこませる「ポンプ」）: 1拍を16に分けて、大きさの平均の形を出す"""
    hop = 256; n = len(mono) // hop; e = np.sqrt((mono[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12); t = np.arange(n) * hop / SR; thr = np.percentile(e, 95) * 0.15; shapes = []
    for a, b in zip(beats[:-1], beats[1:]):
        i, j = np.searchsorted(t, a), np.searchsorted(t, b)
        if j - i < 16: continue
        s = e[i:j]
        if np.median(s) < thr: continue
        q = np.array([s[int(k * len(s) / 16):int((k + 1) * len(s) / 16) or None].mean() for k in range(16)]); shapes.append(_db(q / q.max()))
    if len(shapes) < 16: return None
    m = np.median(np.array(shapes), 0); m = m - m.max(); lo = int(np.argmin(m))
    return {"1拍の中の大きさの形（dB・16に分けて）": [round(float(v), 1) for v in m], "へこみの深さ（dB）": round(float(-m.min()), 1), "いちばんへこむ場所（1拍を0〜1として）": round(lo / 16, 2),
            "拍の頭でへこんで、あとから戻る（ポンプ）": bool(-m[:3].min() >= 3 and m[8:].max() > m[:3].min() + 3)}


def vibrato(f0, t_f0):
    """歌のビブラート: のばしている音の高さのゆれの速さ（Hz）と深さ（セント）"""
    cents = 1200 * np.log2(f0 / 440.0); dt = float(np.median(np.diff(t_f0))); runs = []; i = 0
    while i < len(cents):
        if np.isnan(cents[i]): i += 1; continue
        j = i
        while j < len(cents) and not np.isnan(cents[j]) and abs(cents[j] - np.nanmedian(cents[i:j + 1])) < 120: j += 1
        if (j - i) * dt >= 0.5: runs.append(cents[i:j])
        i = max(j, i + 1)
    rate, depth = [], []
    for r in runs:
        r = r[int(0.15 / dt):]
        if len(r) < int(0.35 / dt): continue
        x = r - np.convolve(r, np.ones(int(0.25 / dt)) / int(0.25 / dt), mode="same"); x = x[int(0.12 / dt):-int(0.12 / dt)]
        if len(x) < 8: continue
        F = np.abs(np.fft.rfft(x * np.hanning(len(x)), 4096)); fq = np.fft.rfftfreq(4096, dt); band = (fq >= 3.5) & (fq <= 8.5); k = np.argmax(F[band]); amp = float(np.sqrt(2) * np.std(x))
        if F[band][k] > 2.5 * np.median(F[(fq >= 1) & (fq <= 12)]) and amp >= 8: rate.append(float(fq[band][k])); depth.append(amp)
    return {"のばしている音の数（0.5秒以上）": len(runs), "そのうちビブラートがある割合": round(len(rate) / max(1, len(runs)), 2), "ビブラートの速さ（Hz）": round(float(np.median(rate)), 1) if rate else None,
            "ビブラートの深さ（セント・片側）": round(float(np.median(depth))) if depth else None}


def drum_sounds(mono, hits):
    """キック・スネア・ハイハットの音の性格。hits: {"kick": [秒…], "snare": […], "hat": […]}"""
    import scipy.signal as ss
    out = {}
    def clips(ts, L):
        c = [mono[int(t * SR) - 220:int(t * SR) - 220 + int(L * SR)] for t in ts if int(t * SR) - 220 >= 0 and int(t * SR) + int(L * SR) < len(mono)]
        c = [x for x in c if np.abs(x).max() > 1e-3]; return c
    def spec_avg(c, n):
        return np.mean([np.abs(np.fft.rfft(x[:n] * np.hanning(n))) ** 2 for x in c if len(x) >= n], 0), np.fft.rfftfreq(n, 1 / SR)
    def tail(c, floor=-20):
        v = []
        for x in c:
            hop = 64; e = _env(x, 768, hop); n = len(e); p = int(np.argmax(e[:n // 2 + 1])); d = np.where(_db(e[p:] / e[p]) <= floor)[0]; v.append((d[0] if len(d) else n - p) * hop / SR * 1000)
        return round(float(np.median(v))) if v else None
    k = clips(hits.get("kick", []), 0.35)
    if len(k) >= 6:
        P, f = spec_avg(k, 8192); lo = (f >= 30) & (f <= 150); tot = P.sum() + 1e-12
        out["キック"] = {"いちばん強い高さ（Hz）": round(float(f[lo][np.argmax(P[lo])])), "長さ（ミリ秒・−20dB まで）": tail(k), "「カチッ」の強さ（2〜6kHz の割合・dB）": round(float(10 * np.log10(P[(f >= 2000) & (f <= 6000)].sum() / tot + 1e-12)), 1),
                      "低い所（〜100Hz）の割合（dB）": round(float(10 * np.log10(P[f <= 100].sum() / tot + 1e-12)), 1), "測った数": len(k)}
    s = clips(hits.get("snare", []), 0.4)
    if len(s) >= 6:
        P, f = spec_avg(s, 8192); body = (f >= 120) & (f <= 400); tot = P.sum() + 1e-12
        out["スネア"] = {"胴の高さ（Hz）": round(float(f[body][np.argmax(P[body])])), "余韻（ミリ秒・−20dB まで）": tail(s), "明るさ（4kHz より上の割合・dB）": round(float(10 * np.log10(P[f >= 4000].sum() / tot + 1e-12)), 1),
                      "胴（120〜400Hz）の割合（dB）": round(float(10 * np.log10(P[body].sum() / tot + 1e-12)), 1), "測った数": len(s)}
    h = clips(hits.get("hat", []), 0.12)
    if len(h) >= 6:
        P, f = spec_avg(h, 2048); hi = f >= 3000; tot = P[hi].sum() + 1e-12
        out["ハイハット"] = {"音の重心（Hz・3kHz より上）": round(float((f[hi] * P[hi]).sum() / tot)), "長さ（ミリ秒・−20dB まで）": tail(h), "測った数": len(h)}
    return out


def hints(r):
    """測った数字を、作曲ソフトの音づくりの言葉に直す（目安）"""
    H = {}
    b = r.get("ベース")
    if b:
        t = []; hm = b.get("倍音の形")
        if hm: t.append(f"波形: {hm['波の形（たぶん）']}（下がり方 {hm['倍音の下がり方（dB／オクターブ）']}dB／オクターブ）")
        t.append(f"フィルター: 高い音の境目 {b['高い音の境目（85%がこれより下・Hz）']}Hz くらいまで出す")
        if b.get("立ち上がりと余韻"): e = b["立ち上がりと余韻"]; t.append(f"立ち上がり {e['立ち上がり（ミリ秒・10%→90%。20より短くは測れない）']}ミリ秒・0.2秒あと {e['頭から0.2秒あとの大きさ（dB・頭を0として）']}dB（0 に近いほど、のばす音。−10 より下は、はじく音）")
        if b.get("拍に合わせたへこみ") and b["拍に合わせたへこみ"]["拍の頭でへこんで、あとから戻る（ポンプ）"]: t.append(f"キックでへこませる（深さ {b['拍に合わせたへこみ']['へこみの深さ（dB）']}dB）")
        t.append(f"左右: 低い所の広がり {b['左右の広がり（低い所 〜250Hz）']}（0.1 より小さければ、まん中に置く）"); H["ベース"] = t
    c = r.get("和音の楽器")
    if c:
        t = [f"明るさ: 音の重心 {c['音の重心（Hz）']}Hz・高い音の境目 {c['高い音の境目（85%がこれより下・Hz）']}Hz"]
        p = c.get("拍に合わせたへこみ")
        if p: t.append(f"ポンプ: {'あり' if p['拍の頭でへこんで、あとから戻る（ポンプ）'] else 'なし（か、浅い）'}（深さ {p['へこみの深さ（dB）']}dB・いちばんへこむ場所 {p['いちばんへこむ場所（1拍を0〜1として）']}）")
        t.append(f"広げ方: 中 {c['左右の広がり（中 250Hz〜2kHz）']}・高い所 {c['左右の広がり（高い所 2kHz〜）']}（0.5 より大きければ、左右に大きく広げた重ね）")
        t.append(f"打つ音の成分 {c['打つ音の成分の割合']}（大きいほど、はじく・かき鳴らす音。小さいほど、のばす音）"); H["和音の楽器"] = t
    v = r.get("歌")
    if v:
        t = [f"明るさ: 音の重心 {v['音の重心（Hz）']}Hz・とても高い所（8kHz〜）{v['帯ごとの大きさ（dB・全体を0として）']['とても高い（8kHz〜）']}dB（息・サ行のきらきら）"]
        vb = v.get("ビブラート")
        if vb and vb["ビブラートの速さ（Hz）"]: t.append(f"ビブラート: 速さ {vb['ビブラートの速さ（Hz）']}Hz・深さ {vb['ビブラートの深さ（セント・片側）']}セント・のばす音の {int(vb['そのうちビブラートがある割合'] * 100)}% にある")
        t.append(f"つぶし具合: 大きさのゆれ幅 {v['大きさのゆれ幅（dB・鳴っている所）']}dB（小さいほど、強くつぶしてそろえてある）"); H["歌"] = t
    d = r.get("ドラムの音")
    if d:
        t = []
        if "キック" in d: k = d["キック"]; t.append(f"キック: 高さ {k['いちばん強い高さ（Hz）']}Hz・長さ {k['長さ（ミリ秒・−20dB まで）']}ミリ秒・カチッ {k['「カチッ」の強さ（2〜6kHz の割合・dB）']}dB")
        if "スネア" in d: s = d["スネア"]; t.append(f"スネア: 胴 {s['胴の高さ（Hz）']}Hz・余韻 {s['余韻（ミリ秒・−20dB まで）']}ミリ秒・明るさ {s['明るさ（4kHz より上の割合・dB）']}dB")
        if "ハイハット" in d: h = d["ハイハット"]; t.append(f"ハイハット: 重心 {h['音の重心（Hz・3kHz より上）']}Hz・長さ {h['長さ（ミリ秒・−20dB まで）']}ミリ秒")
        H["ドラム"] = t
    return H


def run(stems, beats, bar_t, raw2, present, librosa):
    """stems: {名前: (2, n)}（chordal＝guitar＋piano＋other）。raw2: 段2の書き起こし（ドラムの打った場所・ベースの音）。返すのはカルテに入れる数字"""
    out = {}; st16 = np.concatenate([np.linspace(bar_t[i], bar_t[i + 1], 17)[:-1] for i in range(len(bar_t) - 1)])
    def onset_times(mono):
        y = librosa.resample(mono, orig_sr=SR, target_sr=22050); o = librosa.onset.onset_detect(y=y, sr=22050, hop_length=256, backtrack=True, units="time", delta=0.1); return list(o)
    if present.get("bass"):
        m = stems["bass"].mean(0); r = tone(stems["bass"])
        if r:
            y = librosa.resample(m, orig_sr=SR, target_sr=11025); f0, vo, _ = librosa.pyin(y, fmin=30, fmax=330, sr=11025, frame_length=2048, hop_length=256); f0 = np.where(vo, f0, np.nan); tf = np.arange(len(f0)) * 256 / 11025
            r["倍音の形"] = harmonics(m, f0, tf); r["立ち上がりと余韻"] = envelope(m, onset_times(m)); r["拍に合わせたへこみ"] = pump(m, beats); out["ベース"] = r
    r = tone(stems["chordal"])
    if r: m = stems["chordal"].mean(0); r["立ち上がりと余韻"] = envelope(m, onset_times(m)); r["拍に合わせたへこみ"] = pump(m, beats); out["和音の楽器"] = r
    if present.get("vocals"):
        m = stems["vocals"].mean(0); r = tone(stems["vocals"])
        if r:
            y = librosa.resample(m, orig_sr=SR, target_sr=22050); f0, vo, _ = librosa.pyin(y, fmin=130, fmax=1050, sr=22050, frame_length=2048, hop_length=128); f0 = np.where(vo, f0, np.nan); tf = np.arange(len(f0)) * 128 / 22050
            r["倍音の形"] = harmonics(m, f0, tf); r["ビブラート"] = vibrato(f0, tf); out["歌"] = r
    if present.get("drums"):
        r = tone(stems["drums"])
        if r: out["ドラム"] = r
        d = (raw2 or {}).get("drums")
        if d:
            hit = lambda P, strong: [float(st16[b * 16 + j]) for b, p in enumerate(P) for j, c in enumerate(p) if c in strong and b * 16 + j < len(st16)]
            out["ドラムの音"] = drum_sounds(stems["drums"].mean(0), {"kick": hit(d["kick"], "Xx"), "snare": hit(d["snare"], "X"), "hat": hit(d["hat"], "Xx")})
    out["音づくりのヒント"] = hints(out)
    return out
