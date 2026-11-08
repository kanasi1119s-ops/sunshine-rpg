"""元の動画（10秒）を、なるべく切れ目を見せずに曲の長さまで流し続けるコマの並びを作る
（2026-11-08『白い息のリテイク』。人間「まだ動き変な部分ある」）。
  前の natural_select.py は、歌いはじめ・歌い終わりのたびに「口が動く区間の頭」へ戻っていた。戻り先の姿勢が大きくちがう
  （となりのコマの 8〜9 倍）うえ、0.5 秒で重ねていたので、体がぐにゃっと動いたり、止まって急に動くように見えた。
  ここでは「ビデオ・テクスチャ」の考え方で:
    ・コマは必ず 1 コマずつ前へ（1 倍の速さ。止めない・戻らない）
    ・飛ぶのは、いまのコマと姿勢がいちばん近いコマだけ（カメラの動きは stabilize_frames.py で先に止めておく）
    ・飛んだら 1 秒（24 コマ）かけて、動きの流れで重ねる。飛んだあと最低 MINGAP コマは飛ばない
    ・口は「歌っている所で動き、休みで閉じる」ほど良いが、飛ぶ回数を増やしてまで合わせない（自然さを先に）
    ・同じ所ばかり使わないよう、10 秒ごとに解きなおし、最近使ったコマを少し重くする
  python3 texture_select.py <コマのフォルダ> <追跡 json> <曲.json> <bpm> <長さ秒> <出力 json>
出力: コマごとに [出すコマ, 重ねる前のコマ(-1=なし), 前のコマの濃さ]（mv_compose.py の frames_wb がそのまま読む）
"""
import sys, os, json, numpy as np, cv2
FR, TRK, SONG, BPM, DUR, OUT = sys.argv[1:7]
BPM = float(BPM); DUR = float(DUR); FPS = 24
XF = int(os.environ.get("TX_XF", "24"))            # 重ねる長さ（コマ）
MINGAP = int(os.environ.get("TX_GAP", "60"))       # 飛んだあと、次に飛べるまで（コマ）
JC = float(os.environ.get("TX_JC", "40"))          # 1 回飛ぶ重さ（口が合わないコマ何コマぶんか）
WJ = float(os.environ.get("TX_WJ", "8"))           # 姿勢のちがいの重さ
RMAX = float(os.environ.get("TX_RMAX", "6.5"))     # これより姿勢がちがうコマへは飛ばない（となりのコマの何倍か）
trk = json.load(open(TRK)); K = len(trk)
talk = np.array([t[6] for t in trk]) >= 75
# 姿勢の近さ（ぼかして雪を消した小さい絵どうし）
S = np.array([cv2.GaussianBlur(cv2.resize(cv2.imread(f"{FR}/{k + 1:03d}.png"), (160, 90), interpolation=cv2.INTER_AREA), (0, 0), 2).astype(np.float32).ravel() for k in range(K)])
n2 = (S ** 2).sum(1); D = np.sqrt(np.maximum(n2[:, None] + n2[None] - 2 * S @ S.T, 0) / S.shape[1])
R = D / np.median([D[i, i + 1] for i in range(K - 1)])
J = np.full((K, K), np.inf)                         # J[k, j]: k を出したあと j へ飛ぶ重さ
for k in range(K - XF):                             # 重ねているあいだ、前のコマも前へ進めるよう、終わりの手前で飛ぶ
    for j in range(K - MINGAP):
        if abs(j - k) > 24 and R[k, j] <= RMAX: J[k, j] = JC + WJ * R[k, j]
# 2026-11-08 人間「瞬き…が変かな」: 目を閉じたコマと開いたコマを重ねると、半分透けた目が二重に見える。
#   重ねる 1 秒のあいだ、前のコマ（k+1…）と次のコマ（j…）の目の開き方がそろう組だけにする（TX_EYE: コマごとの目の開き 0〜1）
if os.environ.get("TX_EYE"):
    E = np.load(os.environ["TX_EYE"])
    for k in range(K - XF):
        for j in np.where(np.isfinite(J[k]))[0]:
            if j + XF > K or np.max(np.abs(E[k + 1:k + 1 + XF] - E[j:j + XF])) > 0.3: J[k, j] = np.inf
print("飛べる組 %d・いちばん近い組 %.2f（となりの何倍か）" % (np.isfinite(J).sum(), R[np.isfinite(J)].min()))
# 歌っている所（0.8 秒より短い休みは歌っている扱い）・3 秒より長い休みは口を問わない
js = json.load(open(SONG)); kana = json.load(open(SONG + ".kana")); spb = 60 / BPM
lens = {}; t = 0.0
for tok in js["vocals"][0]["notes"].split():
    p = tok.split(":"); L = float(p[1])
    if not tok.startswith("R") and len(p) >= 3: lens[round(t, 3)] = L
    t += L
N = int(DUR * FPS); sing = np.zeros(N, bool)
for b, ly in kana:
    L = lens.get(round(b, 3), 0.5); sing[int(b * spb * FPS):min(N, int((b + L) * spb * FPS) + 1)] = True
free = np.zeros(N, bool); i = 0
while i < N:
    if not sing[i]:
        j = i
        while j < N and not sing[j]: j += 1
        if 0 < i and j < N and (j - i) < 0.8 * FPS: sing[i:j] = True
        elif (j - i) > 3 * FPS: free[i:j] = True
        i = j
    else: i += 1
# なるべく使いたくないコマ（光のつぶがマフラーの上に少し残るコマなど）。npy にコマごとの重さを書いて TX_AVOID で渡す
AV = np.load(os.environ["TX_AVOID"]) if os.environ.get("TX_AVOID") else np.zeros(K)
def mouth_cost(i):
    if free[i]: return AV.copy()
    return np.where(talk == sing[i], 0.0, 1.0 if sing[i] else 0.6) + AV
# 状態 = (コマ k, 飛んでからのコマ数 c（MINGAP で頭打ち）)
G = MINGAP; CH = 240; EXTRA = 120
usage = np.zeros(K); seq = []; start = None
for c0 in range(0, N, CH):
    c1 = min(N, c0 + CH + EXTRA); T = c1 - c0
    cost = np.full((K, G + 1), np.inf)
    if start is None: cost[:, G] = mouth_cost(c0) + 0.02 * usage
    else: cost[start[0], start[1]] = 0.0
    bk = np.zeros((T, K, G + 1), np.int32)          # 前の状態（k*(G+1)+c）
    for q in range(1, T):
        mc = mouth_cost(c0 + q) + 0.02 * usage
        new = np.full((K, G + 1), np.inf); arg = np.zeros((K, G + 1), np.int32)
        # 1 コマ前へ
        new[1:, 1:] = cost[:-1, :-1]; arg[1:, 1:] = (np.arange(K - 1)[:, None] * (G + 1) + np.arange(G)[None])
        hold = cost[:-1, G]                         # 頭打ちのまま前へ
        better = hold < new[1:, G]; new[1:, G] = np.where(better, hold, new[1:, G])
        arg[1:, G] = np.where(better, np.arange(K - 1) * (G + 1) + G, arg[1:, G])
        # 飛ぶ（MINGAP たってから）
        tot = cost[:, G][:, None] + J; kb = np.argmin(tot, 0); jb = tot[kb, np.arange(K)]
        better = jb < new[:, 0]; new[:, 0] = np.where(better, jb, new[:, 0]); arg[:, 0] = np.where(better, kb * (G + 1) + G, arg[:, 0])
        new += mc[:, None]; m = new[np.isfinite(new)].min(); cost = new - m; bk[q] = arg
    st = int(np.argmin(cost)); path = [st]
    for q in range(T - 1, 0, -1): st = int(bk[q].ravel()[st]); path.append(st)
    path = path[::-1]; keep = min(CH, T) if c1 < N else T
    for s in path[:keep]: seq.append(s // (G + 1))
    if c1 < N: start = divmod(path[keep], G + 1) if keep < T else None
    usage *= 0.5; np.add.at(usage, np.array([s // (G + 1) for s in path[:keep]]), 1.0)
seq = seq[:N]
# 重ねの情報をつける（飛んだら XF コマ、前のコマも前へ進めながら薄くする）
out = []; fade = None
for i, k in enumerate(seq):
    if i > 0 and k != seq[i - 1] + 1: fade = [seq[i - 1] + 1, XF]
    if fade and fade[1] > 0:
        a = fade[1] / (XF + 1); out.append([int(k), int(min(K - 1, fade[0])), round(a, 3)]); fade[0] += 1; fade[1] -= 1
    else: out.append([int(k), -1, 0.0])
json.dump(out, open(OUT, "w"))
jumps = [i for i in range(1, N) if seq[i] != seq[i - 1] + 1]
rs = [R[seq[i - 1], seq[i]] for i in jumps]
gaps = np.diff([0] + jumps + [N])
m = ~free
print(f"飛び {len(jumps)} 回（平均 {N / FPS / max(1, len(jumps)):.1f} 秒に1回・いちばん短い間 {gaps.min() / FPS:.1f} 秒）"
      f"・姿勢のちがい 平均 {np.mean(rs):.2f} 最大 {np.max(rs):.2f}"
      f"・口が合う {np.mean(talk[np.array(seq)][m] == sing[m]):.0%}（歌う所で動く {np.mean(talk[np.array(seq)][sing]):.0%}）")
