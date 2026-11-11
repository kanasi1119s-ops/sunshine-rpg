"""歌詞の一音一音に口を合わせながら、動きは自然なままにするコマの並び（2026-11-08『白い息のリテイク』。
人間「今度は歌詞と口の動きが一致しないね」）。
  texture_select.py（自然さ優先）は、口が「歌っている所で動く・休みで閉じる」の区間しか見ていなかったので、
  一音ごとの口の開き閉じは合っていなかった。ここでは:
    ・元の動画は前へだけ進む。ただし速さを 0.75〜1.25 倍のあいだで、ゆっくり（1 コマに 1/8 段ずつ）変えてよい
      → 元の動画で口が開く瞬間を、歌の母音の頭へ寄せる。半端な位置のコマは、mv_compose.py が動きの流れで間を作る
    ・離れたコマへ飛ぶのは texture_select.py と同じ条件だけ（姿勢がとなりの 5 倍以内・目の開き方がそろう・1 秒かけて重ねる）
    ・ほしい口の開き（0〜1）は、歌詞の母音から: あ 1.0／お 0.8／え 0.7／い・う 0.5／ん 0.15。音の終わりで少し閉じ、
      ま・ば・ぱ行の頭では一瞬閉じる。休みは閉じる。3 秒より長い休み（前奏・間奏）は口を問わない
  python3 lipwarp_select.py <コマのフォルダ> <追跡 json> <曲.json> <bpm> <長さ秒> <出力 json>
出力: コマごとに [出す位置（小数可）, 重ねる前の位置(-1=なし), 前の濃さ]
"""
import sys, os, json, numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lyric_mouth as LM
FR, TRK, SONG, BPM, DUR, OUT = sys.argv[1:7]
BPM = float(BPM); DUR = float(DUR); FPS = 24
XF = int(os.environ.get("LW_XF", "24")); Q = 8                                    # 位置は 1/8 コマきざみ
DV = int(os.environ.get("LW_DV", "2")); VS = np.arange(8 - DV, 9 + DV); VC = DV   # 1 コマで進む量（既定 0.75〜1.25 倍）
JC = float(os.environ.get("LW_JC", "60")); WJ = float(os.environ.get("LW_WJ", "8.0")); RMAX = float(os.environ.get("LW_RMAX", "5.0"))
WM = float(os.environ.get("LW_WM", "2.0"))        # 口が合わない重さ
UW = float(os.environ.get("LW_USE", "0.03"))    # 最近使ったコマを重くする（同じ所ばかり使わない）
WV = float(os.environ.get("LW_WV", "0.15"))       # 速さを変える重さ（ふつうの速さからはなれる重さ）
trk = json.load(open(TRK)); K = len(trk)
area = np.array([t[6] for t in trk], float); op = np.clip((area - 60) / 300, 0, 1)
E = np.load(os.environ["LW_EYE"]) if os.environ.get("LW_EYE") else np.ones(K)
AV = np.load(os.environ["LW_AVOID"]) if os.environ.get("LW_AVOID") else np.zeros(K)
NQ = (K - 1) * Q + 1
qk = np.arange(NQ) / Q
op_q = np.interp(qk, np.arange(K), op); av_q = np.interp(qk, np.arange(K), AV)
# 姿勢の近さ・飛べる組
# 2026-11-11: 映像を層に分けた（wb_layers.py）ので、背景・雪はつなぎ目に関係しない。姿勢の近さは人物だけで測る（LW_MASK: 人物の形 npy）
PMASK = np.load(os.environ["LW_MASK"]) if os.environ.get("LW_MASK") else None
def small(k):
    im = cv2.imread(f"{FR}/{k + 1:03d}.png").astype(np.float32)
    if PMASK is not None: im = im * (PMASK[k][..., None] / 255.0)
    return cv2.GaussianBlur(cv2.resize(im, (160, 90), interpolation=cv2.INTER_AREA), (0, 0), 2).ravel()
S = np.array([small(k) for k in range(K)])
n2 = (S ** 2).sum(1); D = np.sqrt(np.maximum(n2[:, None] + n2[None] - 2 * S @ S.T, 0) / S.shape[1])
R = D / np.median([D[i, i + 1] for i in range(K - 1)])
J = np.full((K, K), np.inf)
for k in range(K - XF - 1):
    for j in range(K - 30):
        if abs(j - k) > 24 and R[k, j] <= RMAX and np.max(np.abs(E[k + 1:k + 1 + XF] - E[j:j + XF])) <= 0.3:
            if AV[k + 1:k + 1 + int(os.environ.get("LW_TAIL", XF))].max() >= 3: continue          # 重ねているあいだ前のコマも映るので、使わないと決めたコマ（重さ 3 以上）へ入る手前では飛ばない
            J[k, j] = JC + WJ * R[k, j]
# ほしい口
js = json.load(open(SONG)); kana = json.load(open(SONG + ".kana")); spb = 60 / BPM
notes = []; t = 0.0
for tok in js["vocals"][0]["notes"].split():
    p = tok.split(":"); L = float(p[1])
    if not tok.startswith("R") and len(p) >= 3: notes.append((round(t, 3), L, p[2]))
    t += L
kmap = {round(b, 3): ly for b, ly in kana}
N = int(DUR * FPS); want = np.zeros(N); wgt = np.ones(N); sing = np.zeros(N, bool)
OPEN = {"a": 1.0, "o": 0.8, "e": 0.7, "i": 0.5, "u": 0.5, "n": 0.15}
prev_v = "a"
for n, (b, L, ly) in enumerate(notes):
    ly = kmap.get(b, ly)
    if ly in ("ー", "-", "~"): v = prev_v
    else: v = LM.vowel(ly) or "a"
    prev_v = v
    i0 = int(b * spb * FPS); i1 = min(N, int((b + L) * spb * FPS))
    if i0 >= N: break
    nxt = notes[n + 1][0] if n + 1 < len(notes) else 1e9
    gap = (nxt - (b + L)) * spb
    o = OPEN.get(v, 0.8)
    for i in range(i0, max(i0 + 1, i1)):
        x = (i - i0) / max(1, i1 - i0)
        want[i] = o * min(1, (i - i0 + 1) / 2.5)                  # 開きはじめ
        if gap < 0.05 and i1 - i0 > 4 and i >= i1 - 2: want[i] = o * 0.6   # 次の音へつなぐ所で少し閉じる
        sing[i] = True
    c = LM.kata2hira(ly)[:1] if ly not in ("ー", "-", "~") else ""
    if c in LM.LIPS and i1 - i0 >= 4: want[i0] = 0.0
# 休み: 0.8 秒より短いのは軽く閉じる、3 秒より長いのは口を問わない
i = 0
while i < N:
    if not sing[i]:
        j = i
        while j < N and not sing[j]: j += 1
        if (j - i) > 3 * FPS: wgt[i + 6:max(i + 6, j - 6)] = 0.0
        elif (j - i) < 0.8 * FPS: want[i:j] = 0.15; wgt[i:j] = 0.5
        i = j
    else: i += 1
def mcost(i): return WM * wgt[i] * np.abs(op_q - want[i]) + av_q
# 状態 = (位置 q, 速さ v)
NV = len(VS); CH = 240; EXTRA = 120
usage = np.zeros(K); out_q = []; start = None
for c0 in range(0, N, CH):
    c1 = min(N, c0 + CH + EXTRA); T = c1 - c0
    cost = np.full((NQ, NV), np.inf)
    if start is None: cost[::Q, VC] = mcost(c0)[::Q] + UW * usage
    else: cost[start[0], start[1]] = 0.0
    bk = np.zeros((T, NQ, NV), np.int32)
    vpen = WV * np.abs(VS - 8) / 2.0
    for q in range(1, T):
        new = np.full((NQ, NV), np.inf); arg = np.zeros((NQ, NV), np.int32)
        for vi, v in enumerate(VS):                   # 速さは 1 段ずつだけ変える
            for pv in (vi - 1, vi, vi + 1):
                if pv < 0 or pv >= NV: continue
                src = cost[:NQ - v, pv] + (0.05 if pv != vi else 0.0)
                better = src < new[v:, vi]
                new[v:, vi] = np.where(better, src, new[v:, vi]); arg[v:, vi] = np.where(better, np.arange(NQ - v) * NV + pv, arg[v:, vi])
        # 飛ぶ（コマちょうどの位置から、ふつうの速さで）
        ck = cost[::Q].min(1); ckarg = cost[::Q].argmin(1)
        tot = ck[:, None] + J; kb = np.argmin(tot, 0); jb = tot[kb, np.arange(K)]
        tgt = np.arange(K) * Q; better = jb < new[tgt, VC]
        new[tgt, VC] = np.where(better, jb, new[tgt, VC]); arg[tgt, VC] = np.where(better, kb * Q * NV + ckarg[kb], arg[tgt, VC])
        uq = np.interp(qk, np.arange(K), usage)
        new += (mcost(c0 + q) + UW * uq)[:, None] + vpen[None]
        m = new[np.isfinite(new)].min(); cost = new - m; bk[q] = arg
    st = int(np.argmin(cost)); path = [st]
    for q in range(T - 1, 0, -1): st = int(bk[q].ravel()[st]); path.append(st)
    path = path[::-1]; keep = min(CH, T) if c1 < N else T
    out_q += [s // NV for s in path[:keep]]
    if c1 < N: start = divmod(path[keep], NV)
    usage *= 0.5; np.add.at(usage, np.array([s // NV // Q for s in path[:keep]]), 1.0)
out_q = np.array(out_q[:N])
pos = out_q / Q
out = []; fade = None
for i in range(N):
    d = out_q[i] - out_q[i - 1] if i else 8
    if i and not (VS[0] <= d <= VS[-1]): fade = [np.floor(pos[i - 1]) + 1, XF]
    if fade and fade[1] > 0:
        a = fade[1] / (XF + 1); out.append([float(pos[i]), float(min(K - 1, fade[0])), round(a, 3)]); fade[0] += 1; fade[1] -= 1
    else: out.append([float(pos[i]), -1, 0.0])
json.dump(out, open(OUT, "w")); np.save(OUT + ".sing.npy", sing)
jumps = [i for i in range(1, N) if not (VS[0] <= out_q[i] - out_q[i - 1] <= VS[-1])]
spd = np.diff(out_q) / 8.0; spd = spd[(spd >= VS[0] / 8) & (spd <= VS[-1] / 8)]
o_got = np.interp(pos, np.arange(K), op); m = wgt > 0
corr = np.corrcoef(o_got[m & sing], want[m & sing])[0, 1]
rj = [R[int(out_q[i - 1] // Q), int(out_q[i] // Q)] for i in jumps]
print("飛べる組", int(np.isfinite(J).sum()), "・飛んだ所の姿勢のちがい 平均 %.2f 最大 %.2f" % (np.mean(rj), np.max(rj)))
print(f"飛び {len(jumps)} 回（平均 {N / FPS / max(1, len(jumps)):.1f} 秒に1回・いちばん短い間 {np.diff([0] + jumps).min() / FPS:.1f} 秒）"
      f"・速さ 平均 {spd.mean():.2f}（1倍のコマ {np.mean(np.abs(spd - 1) < 0.01):.0%}）"
      f"・口の開きのずれ 平均 {np.mean(np.abs(o_got - want)[m]):.2f}・歌の所の口の開きと歌詞の一致（相関）{corr:.2f}")
