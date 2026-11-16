#!/usr/bin/env python3
"""曲の分析ソフト・段2: 分けた音から、ドラムの型・ベースの動き・和音・歌の旋律の形を書き起こす（2026-11-16）。analyze.py から呼ばれる。
保存するもの（人間の指示 2026-11-16）:
  ・リズムの型（ドラム・ベース・歌の、1小節16マスの型）と、そのくり返し方
  ・短いコード進行（度数で、2〜4個のつながり。多い順に数個だけ）。1曲ぶんの進行は保存しない
  ・旋律の「形」（音の長さ・休み・跳び方・食い方・音域・句の上がり下がり）。旋律そのもの（音の高さの並び）は保存しない
当たりやすさは README。書き起こしは「たぶん」で、テンポを半分にまちがえた曲では1マスが8分になる。"""
import os, sys, importlib.util, collections
import numpy as np

SR = 44100
DEG = ["I", "♭II", "II", "♭III", "III", "IV", "♯IV", "V", "♭VI", "VI", "♭VII", "VII"]
QUAL = {"": [0, 4, 7], "m": [0, 3, 7], "7": [0, 4, 7, 10], "maj7": [0, 4, 7, 11], "m7": [0, 3, 7, 10], "sus4": [0, 5, 7], "sus2": [0, 2, 7], "5": [0, 7]}
KS_MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]); KS_MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


def _steps(bar_t):
    return np.concatenate([np.linspace(bar_t[i], bar_t[i + 1], 17)[:-1] for i in range(len(bar_t) - 1)])


def _near(a, b, k=1):
    return sum(x != y for x, y in zip(a, b)) <= k


def repetition(pats, coarse=False):
    """型のくり返し方（単調さの物差し）: 前の小節と同じ・2小節前と同じ（1マスちがいまでは同じとみなす）割合、8小節の中の型の種類、変わる小節が4小節の区切りにある割合。
    coarse=True は、8分の細かさにまとめてからくらべる（書き起こしのゆれに強い）"""
    if coarse: pats = ["".join("x" if "x" in p[i:i + 2] or "X" in p[i:i + 2] else ("-" if "-" in p[i:i + 2] else ".") for i in range(0, 16, 2)) for p in pats]
    act = [(i, p) for i, p in enumerate(pats) if p.strip(".|")]
    if len(act) < 8: return None
    on = lambda i: i >= 0 and pats[i].strip(".|")
    same = [_near(pats[i], pats[i - 1]) for i, p in act if on(i - 1)]; same2 = [_near(pats[i], pats[i - 2]) for i, p in act if on(i - 2)]
    either = [_near(pats[i], pats[i - 1]) or _near(pats[i], pats[i - 2]) for i, p in act if on(i - 1) and on(i - 2)]
    kinds = []
    for a in range(0, len(pats) - 7, 8):
        seen = []
        for p in pats[a:a + 8]:
            if p.strip(".|") and not any(_near(p, q) for q in seen): seen.append(p)
        if seen: kinds.append(len(seen))
    ch = [i for i, p in act if on(i - 1) and on(i - 2) and not (_near(pats[i], pats[i - 1]) or _near(pats[i], pats[i - 2]))]
    cnt = collections.Counter(p for _, p in act); top = cnt.most_common(4)
    return {"前の小節と同じ型の割合": round(float(np.mean(same)), 3) if same else None, "2小節前と同じ型の割合": round(float(np.mean(same2)), 3) if same2 else None,
            "前か2小節前と同じ型の割合（くり返しの多さ）": round(float(np.mean(either)), 3) if either else None, "8小節の中の型の種類（平均）": round(float(np.mean(kinds)), 2) if kinds else None,
            "新しい型が出る小節が、4小節の区切りの最後にある割合": round(float(np.mean([i % 4 == 3 for i in ch])), 3) if ch else None,
            "いちばん多い型が占める割合": round(top[0][1] / len(act), 3), "多い型": [{"型": p, "割合": round(c / len(act), 3)} for p, c in top]}


def likeness(sets):
    """前の小節か2小節前の小節と、どれだけ似ているか（0〜1。同じなら1）。打った場所の重なり（重なった数 ÷ どちらかにある数）の平均。
    書き起こしが1〜2打まちがっていても大きくは変わらないので、「同じ型の割合」よりゆれに強い"""
    jac = lambda a, b: len(a & b) / len(a | b) if (a | b) else None
    v = []
    for i in range(2, len(sets)):
        if not sets[i]: continue
        c = [x for x in (jac(sets[i], sets[i - 1]) if sets[i - 1] else None, jac(sets[i], sets[i - 2]) if sets[i - 2] else None) if x is not None]
        if c: v.append(max(c))
    return round(float(np.mean(v)), 3) if len(v) >= 8 else None


def drums_tr(d, bar_t, librosa):
    y = librosa.resample(d, orig_sr=SR, target_sr=22050); hop = 128; S = np.abs(librosa.stft(y, n_fft=1024, hop_length=hop)); f = librosa.fft_frequencies(sr=22050, n_fft=1024); L = np.log1p(30 * S)
    def flux(a, b):
        e = np.maximum(0, np.diff(L[(f >= a) & (f < b)], axis=1, prepend=0)).sum(0); return e / (np.percentile(e, 99) + 1e-9)
    fk, fs, fh = flux(30, 140), flux(200, 2200), flux(6500, 11000); st = _steps(bar_t); nb = len(bar_t) - 1; sd = float(np.median(np.diff(st)))
    tfr = np.arange(L.shape[1]) * hop / 22050; tot = fk + fs + fh; gap = max(2, int(0.6 * sd * 22050 / hop))
    # 立ち上がり（音の頭）を先に見つけ、いちばん近いマスに入れる。低い音が中くらいの音より強ければキック、逆ならスネア。どちらも弱くて高い音だけならハイハット
    pk = librosa.util.peak_pick(tot, pre_max=gap, post_max=gap, pre_avg=gap * 3, post_avg=gap * 3, delta=0.12, wait=gap)
    K = [["."] * 16 for _ in range(nb)]; Sn = [["."] * 16 for _ in range(nb)]; H = [["."] * 16 for _ in range(nb)]
    for i in pk:
        t = tfr[i]; q = int(np.argmin(np.abs(st - t)))
        if sd < 0.09:      # 速い曲（16分が 0.09秒より短い）は、8分のマスに寄せる（人の演奏のゆれで、となりの16分にずれるため）
            ev = st[::2]; q = 2 * int(np.argmin(np.abs(ev - t)))
        if abs(st[q] - t) > (0.6 if sd >= 0.09 else 1.1) * sd or q >= nb * 16: continue
        w = slice(max(0, i - 3), i + 4); vk, vs, vh = float(fk[w].max()), float(fs[w].max()), float(fh[w].max()); b_, j = divmod(q, 16)
        if vk > 0.45 and vk >= 0.9 * vs: K[b_][j] = "X" if vk > 0.9 else "x"
        elif vs > 0.4: Sn[b_][j] = "X" if vs > 0.75 else ("x" if vs > 0.5 else "o")
        elif vh > 0.13: H[b_][j] = "X" if vh > 0.3 else "x"
        if (vk > 0.45 or vs > 0.4) and vh > 0.6 and H[b_][j] == ".": H[b_][j] = "x"      # キックやスネアと同時のハイハットは、高い音がとくに強いときだけ
    return {"kick": ["".join(x) for x in K], "snare": ["".join(x) for x in Sn], "hat": ["".join(x) for x in H]}


def drums_st(r):
    K, Sn, H = r["kick"], r["snare"], r["hat"]; nb = len(K); c8 = lambda p: "".join("x" if p[i:i + 2].strip(".") else "." for i in range(0, 16, 2))
    ks8 = [{("k", j) for j, c in enumerate(c8(K[b])) if c != "."} | {("s", j) for j, c in enumerate(c8(Sn[b])) if c != "."} for b in range(nb)]; h8 = [{j for j, c in enumerate(c8(H[b])) if c != "."} for b in range(nb)]
    comb = [K[i] + "|" + Sn[i] for i in range(nb)]
    hat_head = [1 for b in range(nb) for j in (0, 4, 8, 12) if H[b][j] == "X"]; hat_n = [H[b][j] for b in range(nb) for j in range(16) if H[b][j] != "."]
    pos = lambda P: [round(float(np.mean([p[j] != "." for p in P if p.strip(".")])), 2) if any(p.strip(".") for p in P) else 0 for j in range(16)]
    fills = [b for b in range(nb) if sum(c != "." for c in Sn[b][8:]) >= 5 and (b == 0 or sum(c != "." for c in Sn[b - 1][8:]) < 4)]
    return {"キックとスネアの型のくり返し": repetition(comb), "キックとスネアの型のくり返し（8分にまとめて）": repetition([c8(K[i]) + "|" + c8(Sn[i]) for i in range(nb)]), "刻みの型のくり返し": repetition(H),
            "前か2小節前との似かた（キックとスネア・8分にまとめて）": likeness(ks8), "前か2小節前との似かた（刻み・8分にまとめて）": likeness(h8),
            "位置ごとの割合": {"キック": pos(K), "スネア": pos(Sn), "刻み": pos(H)}, "刻みの細かさ（1小節の打数・中央値）": float(np.median([sum(c != "." for c in h) for h in H if h.strip(".")])) if any(h.strip(".") for h in H) else 0,
            "スネアの弱い打（ゴースト）の割合": round(float(np.mean([c == "o" for s in Sn for c in s if c != "."])), 3) if any(s.strip(".") for s in Sn) else 0,
            "フィルらしい小節の数（8小節あたり）": round(len(fills) / max(1, nb) * 8, 2), "フィルが4小節の区切りの最後にある割合": round(float(np.mean([b % 4 == 3 for b in fills])), 2) if fills else None}


def bass_tr(bs, bar_t, librosa):
    y = librosa.resample(bs, orig_sr=SR, target_sr=11025); hop = 256
    f0, vo, _ = librosa.pyin(y, fmin=30, fmax=330, sr=11025, frame_length=2048, hop_length=hop); rm = librosa.feature.rms(y=y, frame_length=1024, hop_length=hop)[0][:len(f0)]; gate = np.percentile(rm, 95) * 0.08
    tfr = np.arange(len(f0)) * hop / 11025; st = _steps(bar_t); nb = len(bar_t) - 1; notes = np.full(nb * 16, -1)
    for q in range(nb * 16):
        a, b = np.searchsorted(tfr, st[q]), np.searchsorted(tfr, st[q + 1] if q + 1 < len(st) else bar_t[-1])
        if b <= a: continue
        seg = f0[a:b]; ok = vo[a:b] & ~np.isnan(seg) & (rm[a:b] > gate)
        if ok.mean() >= 0.4: notes[q] = int(np.round(np.median(librosa.hz_to_midi(seg[ok]))))
    return {"notes": notes}


def bass_st(r):
    notes = np.array(r["notes"]); nb = len(notes) // 16; pats = []
    for b in range(nb):
        s = ""; prev = notes[b * 16 - 1] if b else -1
        for j in range(16):
            n = notes[b * 16 + j]; s += "." if n < 0 else ("x" if n != prev else "-"); prev = n
        pats.append(s)
    seq = [int(n) for i, n in enumerate(notes) if n >= 0 and (i == 0 or notes[i - 1] != n)]; iv = np.abs(np.diff(seq)) if len(seq) > 1 else np.array([])
    on8 = [{j // 2 for j, c in enumerate(p) if c == "x"} for p in pats]
    return {"型のくり返し": repetition(pats, coarse=True), "前か2小節前との似かた（音を出す場所・8分にまとめて）": likeness(on8), "1小節の音の数（中央値）": float(np.median([p.count("x") for p in pats if p.strip(".")])) if any(p.strip(".") for p in pats) else 0,
            "動き方": {"となりの音へ（1〜2半音）": round(float(np.mean((iv >= 1) & (iv <= 2))), 3) if len(iv) else 0, "3〜4半音": round(float(np.mean((iv >= 3) & (iv <= 4))), 3) if len(iv) else 0,
                    "5度・4度（5〜7半音）": round(float(np.mean((iv >= 5) & (iv <= 7))), 3) if len(iv) else 0, "オクターブ（12半音）": round(float(np.mean(iv == 12)), 3) if len(iv) else 0, "そのほかの跳び": round(float(np.mean((iv > 7) & (iv != 12))), 3) if len(iv) else 0},
            "音域（半音）": int(np.ptp(seq)) if seq else 0, "休みのマスの割合": round(float(np.mean(notes < 0)), 3)}


CHANGE_COST = 0.12      # 自分の3曲で答え合わせして決めた（根音の当たり 64・61・88%）


def chords_tr(harm, bs_notes, bar_t, librosa):
    y = librosa.resample(harm, orig_sr=SR, target_sr=22050); hop = 1024
    tun = float(librosa.estimate_tuning(y=y, sr=22050))                              # 調律のずれ（A=440 からのずれ）を先に測る。ずれたままだと、となりの半音にゆれる
    ch = librosa.feature.chroma_cqt(y=y, sr=22050, hop_length=hop, n_chroma=12, tuning=tun); tfr = np.arange(ch.shape[1]) * hop / 22050
    nb = len(bar_t) - 1; ht = np.concatenate([[bar_t[i], (bar_t[i] + bar_t[i + 1]) / 2] for i in range(nb)] + [[bar_t[-1]]]); T = {}
    for q, iv in QUAL.items():
        for r in range(12):
            v = np.zeros(12); v[[(r + i) % 12 for i in iv]] = 1; v[r] = 1.3; T[(r, q)] = v / np.linalg.norm(v)
    keys = list(T); TM = np.array([T[k] for k in keys]); PEN = np.array([{"": 0, "m": 0, "5": 0.03, "sus4": 0.06, "sus2": 0.08, "7": 0.08, "maj7": 0.1, "m7": 0.07}[k[1]] for k in keys]); KR = np.array([k[0] for k in keys])
    allc = np.zeros(12); SCO = np.full((nb * 2, len(keys)), np.nan)
    for h in range(nb * 2):
        a, b = np.searchsorted(tfr, ht[h]), np.searchsorted(tfr, ht[h + 1])
        if b <= a: continue
        c = ch[:, a:b].mean(1); e = float(np.linalg.norm(c))
        if e < 1e-6: continue
        c = c / e; allc += c; bn = [int(n) % 12 for n in bs_notes[h * 8:h * 8 + 3] if n >= 0]      # ベースは、その2拍の頭の音だけを手がかりにする（終わりの方は、次の和音へのつなぎの音が多い）
        sc = TM @ c - PEN
        if bn: sc = sc + 0.2 * (KR == bn[0])
        SCO[h] = sc
    # 和音を変えるたびに少し点を引いて、いちばん点の高い並びを選ぶ（2拍だけ別の和音にゆれるのをおさえる）
    CH = CHANGE_COST; ok = ~np.isnan(SCO[:, 0]); seq = [None] * (nb * 2); idx = np.where(ok)[0]
    if len(idx):
        dp = SCO[idx[0]].copy(); back = []
        for h in idx[1:]:
            m = int(np.argmax(dp)); stay = dp; move = dp[m] - CH; frm = np.where(stay >= move, np.arange(len(keys)), m); dp = np.maximum(stay, move) + SCO[h]; back.append(frm)
        k = int(np.argmax(dp)); path = [k]
        for frm in back[::-1]: k = int(frm[k]); path.append(k)
        for h, k in zip(idx, path[::-1]): seq[h] = keys[k]
    return {"seq": seq, "allc": allc, "tuning": tun}


def chords_st(r):
    seq, allc = r["seq"], np.array(r["allc"]); nb = len(seq) // 2
    # 調: 和音の根音と種類が、いちばんよく合う調
    best_key = max(((t, m) for t in range(12) for m in ("major", "minor")), key=lambda km: float(np.corrcoef(np.roll(KS_MAJ if km[1] == "major" else KS_MIN, km[0]), allc)[0, 1]))
    tonic, mode = best_key; name = lambda c: DEG[(c[0] - tonic) % 12] + c[1]
    dseq = [name(c) if c else None for c in seq]
    # 短いコード進行は、3和音の細かさ（長・短・sus4）にまとめ、2拍だけ出てすぐ消える和音（書き起こしのゆれ）をならしてから数える
    # 同じ根音で「長」と「短」が入れかわるのは、ほとんどが聞き取りのゆれ（歪んだギターの5度だけの和音など）。だから、根音ごとに、その曲でいちばん長く鳴っていた方（長か短）に決める
    mm = {}
    for c in seq:
        if c: mm.setdefault(c[0], collections.Counter())["m" if c[1] in ("m", "m7") else ""] += 1
    simp = lambda c: DEG[(c[0] - tonic) % 12] + mm[c[0]].most_common(1)[0][0] if c else None
    sq = [simp(c) for c in seq]; roots = [c[0] if c else None for c in seq]; rch = sum(1 for i in range(1, len(roots)) if roots[i] is not None and roots[i - 1] is not None and roots[i] != roots[i - 1])
    for i in range(1, len(sq) - 1):
        if sq[i] != sq[i - 1] and sq[i] != sq[i + 1] and sq[i - 1] == sq[i + 1]: sq[i] = sq[i - 1]
    col = [d for i, d in enumerate(sq) if d and (i == 0 or sq[i - 1] != d)]
    grams = {}
    for n in (2, 3, 4):
        cnt = collections.Counter(" → ".join(col[i:i + n]) for i in range(len(col) - n + 1) if len(set(col[i:i + n])) > 1)
        grams[str(n)] = [{"進行": k, "回数": v} for k, v in cnt.most_common(6) if v >= (3 if n < 4 else 2)]
    dur = collections.Counter(d for d in dseq if d); tot = sum(dur.values()) or 1; qd = collections.Counter(c[1] for c in seq if c)
    QJ = {"": "長3和音", "m": "短3和音", "7": "属7", "maj7": "長7", "m7": "短7", "sus4": "sus4", "sus2": "sus2", "5": "5度だけ（パワーコード）"}
    changes = sum(1 for i in range(1, len(dseq)) if dseq[i] and dseq[i - 1] and dseq[i] != dseq[i - 1])
    rs = [(r - tonic) % 12 for i, r in enumerate(roots) if r is not None and (i == 0 or roots[i - 1] != r)]; mv = collections.Counter((b - a) % 12 for a, b in zip(rs, rs[1:])); mt = sum(mv.values()) or 1
    MVJ = {5: "4度上（5度下）へ", 7: "5度上（4度下）へ", 2: "2度上へ", 10: "2度下へ", 1: "半音上へ", 11: "半音下へ", 3: "短3度上へ", 9: "短3度下へ", 4: "長3度上へ", 8: "長3度下へ", 6: "増4度へ"}
    return {"調（たぶん）": ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"][tonic] + ("長調" if mode == "major" else "短調"),
            "和音が変わる回数（1小節あたり）": round(changes / max(1, nb), 2), "根音が変わる回数（1小節あたり）": round(rch / max(1, nb), 2), "根音の動き方の割合": {MVJ[k]: round(v / mt, 3) for k, v in mv.most_common()},
            "使っている根音の数（全体の3%以上）": int(sum(1 for r in set(x for x in roots if x is not None) if roots.count(r) / max(1, sum(x is not None for x in roots)) >= 0.03)), "小節の途中で変わる小節の割合": round(float(np.mean([dseq[2 * i] != dseq[2 * i + 1] for i in range(nb) if dseq[2 * i] and dseq[2 * i + 1]])), 3) if nb else 0,
            "度数の割合": {k: round(v / tot, 3) for k, v in dur.most_common(10)}, "和音の種類の割合": {QJ[k]: round(v / sum(qd.values()), 3) for k, v in qd.most_common()},
            "使っている和音の種類の数": len(dur), "短いコード進行（多い順）": grams}


def melody_tr(v, bar_t, librosa):
    y = librosa.resample(v, orig_sr=SR, target_sr=22050); hop = 256
    f0, vo, _ = librosa.pyin(y, fmin=130, fmax=1050, sr=22050, frame_length=2048, hop_length=hop); tfr = np.arange(len(f0)) * hop / 22050; st = _steps(bar_t); nb = len(bar_t) - 1
    midi = np.full(nb * 16, -1.0); rm = librosa.feature.rms(y=y, frame_length=1024, hop_length=hop)[0][:len(f0)]; gate = np.percentile(rm, 95) * 0.2
    for q in range(nb * 16):
        a, b = np.searchsorted(tfr, st[q]), np.searchsorted(tfr, st[q + 1] if q + 1 < len(st) else bar_t[-1])
        if b <= a: continue
        seg = f0[a:b]; ok = vo[a:b] & ~np.isnan(seg) & (rm[a:b] > gate)
        if ok.mean() >= 0.5: midi[q] = float(np.round(np.median(librosa.hz_to_midi(seg[ok]))))
    return {"midi": midi}


def melody_st(r):
    midi = np.array(r["midi"]); nb = len(midi) // 16; notes = []; q = 0
    while q < len(midi):
        if midi[q] < 0: q += 1; continue
        e = q + 1
        while e < len(midi) and midi[e] == midi[q]: e += 1
        notes.append((q / 4, e / 4, int(midi[q]), 80)); q = e
    pats = []
    for b in range(nb):
        s = ""; prev = midi[b * 16 - 1] if b else -1
        for j in range(16):
            n = midi[b * 16 + j]; s += "." if n < 0 else ("x" if n != prev else "-"); prev = n
        pats.append(s)
    r["notes"] = notes
    if len(notes) < 20: return {}
    here = os.path.dirname(os.path.abspath(__file__)); argv = sys.argv[:]; sys.argv = ["x", "/nonexistent"]
    spec = importlib.util.spec_from_file_location("ps", os.path.join(here, "..", "audio-check", "pop909-sustain.py")); ps = importlib.util.module_from_spec(spec); spec.loader.exec_module(ps); sys.argv = argv
    m = {k: round(float(x), 3) for k, x in ps.measure(notes).items()}
    long_ = [(s, e) for s, e, *_ in notes if e - s >= 1.9]
    if long_: m["長い音が拍のウラ（食って入る）で始まる割合"] = round(sum(1 for s, e in long_ if 0.1 < (s % 1) < 0.9) / len(long_), 3)
    # 句（1拍以上の休みで区切る）の上がり下がり
    ph = []; cur = [notes[0]]
    for a, b in zip(notes, notes[1:]):
        if b[0] - a[1] >= 1.0: ph.append(cur); cur = [b]
        else: cur.append(b)
    ph.append(cur); shape = collections.Counter()
    for p in ph:
        if len(p) < 3: continue
        ps_ = [n[2] for n in p]; hi = int(np.argmax(ps_)) / (len(ps_) - 1); d = ps_[-1] - ps_[0]
        shape["山（まん中が高い）" if 0.25 < hi < 0.75 and max(ps_) - max(ps_[0], ps_[-1]) >= 2 else ("上がる" if d >= 2 else ("下がる" if d <= -2 else "平ら"))] += 1
    tot = sum(shape.values()) or 1; iv = np.diff([n[2] for n in notes])
    m["句の形の割合"] = {k: round(v / tot, 3) for k, v in shape.most_common()}; m["句の数"] = len(ph); m["句の長さ（拍・中央値）"] = round(float(np.median([p[-1][1] - p[0][0] for p in ph])), 2)
    m["音域（半音）"] = int(np.percentile([n[2] for n in notes], 98) - np.percentile([n[2] for n in notes], 2)); m["上がる動きの割合"] = round(float(np.mean(iv > 0)), 3); m.pop("同じ高さがつづく割合", None)
    big = np.abs(iv); m["跳ぶ動き（5半音以上）の割合"] = round(float(np.mean(big >= 5)), 3); m["となりの音へ動く（1〜2半音）割合"] = round(float(np.mean((big >= 1) & (big <= 2))), 3)
    m["歌のリズムの型のくり返し"] = repetition(pats, coarse=True); m["前か2小節前との似かた（音を出す場所・8分にまとめて）"] = likeness([{j // 2 for j, c in enumerate(p) if c == "x"} for p in pats])
    return m


BASS_MIX = 0.0      # 和音を聞くときは、ベースの音をまぜない（歩くベースやすべるベースにつられる）。ベースは「2拍の頭の音」だけを手がかりにする


def stats(raw):
    """書き起こし（raw）から、カルテに保存する数字を作る。物差しを直したとき、音を取り直さずに計算し直せる"""
    out = {}; d, b, c, m = raw.get("drums"), raw.get("bass"), raw.get("chords"), raw.get("melody")
    if d: out["ドラム"] = drums_st(d)
    if b:
        out["ベース"] = bass_st(b); rel = collections.Counter()      # ベースの音と、和音の根音の関係
        for q, n in enumerate(b["notes"]):
            ch = c["seq"][min(len(c["seq"]) - 1, q // 8)]
            if n < 0 or not ch: continue
            i = (int(n) - ch[0]) % 12; rel["根音" if i == 0 else ("5度" if i == 7 else ("3度" if i in (3, 4) else ("7度" if i in (10, 11) else "そのほか")))] += 1
        tot = sum(rel.values()) or 1; out["ベース"]["和音の根音との関係"] = {k: round(v / tot, 3) for k, v in rel.most_common()}
    out["和音"] = chords_st(c)
    if m:
        ms = melody_st(m)
        if ms: out["歌の旋律の形"] = ms
    return out


def run(sm, beats, bar_t, spb, present, librosa):
    d = drums_tr(sm["drums"], bar_t, librosa) if present.get("drums") else None
    b = bass_tr(sm["bass"], bar_t, librosa) if present.get("bass") else None
    c = chords_tr(sm["chordal"] + BASS_MIX * sm["bass"], b["notes"] if b else np.full((len(bar_t) - 1) * 16, -1), bar_t, librosa)
    m = melody_tr(sm["vocals"], bar_t, librosa) if present.get("vocals") else None
    raw = {"drums": d, "bass": b, "chords": c, "melody": m, "spb": spb}      # 書き起こしそのもの（カルテには入れない）
    return stats(raw), raw
