"""元の動画のコマを並べ直して、歌詞に口を合わせる（2026-11-08『白い息のリテイク』。人間「このテトに歌わせてください」）。
絵には手を加えない（口の切り貼り・はずみ・ゆれはしない。2026-10-26 の人間の指示）。teto_mv.py と同じ考え方を、横長の動画用にまとめ直したもの。
  python3 lipsync_select.py <コマのフォルダ> <追跡 json> <使えるコマ "0-14,112-239"> <曲.json> <bpm> <長さ秒> <出力 seq.json> [lead]
追跡 json: [[コマ, dx, dy, 合い具合, 口の幅, 口の高さ, 口の面積], ...]（口のまわりの四角で測ったもの。必ず目で確かめてから使う）
  ・使えるコマ: 元の動画に、生成AIが勝手に入れた文字が映っているコマ（白い息: 15〜111）は使わない
  ・コマごとの口: 閉じる(n)・大きく開く(a)・横に開く(i/e)・すぼめる(o/u)
  ・曲のコマごとのほしい口: 歌っている音のひらがなの母音。休みは閉じる。0.5秒より短い休み（息つぎ）は、軽く開いたままでよい
  ・並べ方: 隣のコマへ進む・戻るは自然。向きを変える・止まるは少し不自然。離れたコマへ飛ぶのは、姿勢がほぼ同じときだけ
"""
import sys, json, glob, os, numpy as np, cv2
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lyric_mouth as LM

FR, TRK, OK, SONG, BPM, DUR, OUT = sys.argv[1:8]
LEAD = [int(x) for x in sys.argv[8].split(",")] if len(sys.argv) > 8 else [0]
BPM = float(BPM); DUR = float(DUR); FPS = 24
trk = json.load(open(TRK))
ok = []
for part in OK.split(","):
    a, b = part.split("-"); ok += list(range(int(a), int(b) + 1))
K = len(ok)
w = np.array([trk[k][4] for k in ok], float); h = np.array([trk[k][5] for k in ok], float); ar = np.array([trk[k][6] for k in ok], float)
cls_src = np.where(ar < 75, 0, np.where((w >= 27) & (h >= 13), 1, np.where(w >= 24, 2, 3)))   # 0=n 1=a 2=i/e 3=o/u
print("使えるコマ", K, "・口の種類の数", [int((cls_src == c).sum()) for c in range(4)])
# 姿勢の近さ（口のまわりを消して、小さく縮めた絵どうし）
small = []
for k in ok:
    g = cv2.cvtColor(cv2.imread(f"{FR}/{k + 1:03d}.png"), cv2.COLOR_BGR2GRAY).astype(np.float32)
    _, dx, dy = trk[k][:3]; mx, my = 638 + dx, 307 + dy
    g[my - 25:my + 25, mx - 40:mx + 40] = 200
    small.append(cv2.resize(g, (128, 72), interpolation=cv2.INTER_AREA).ravel())
small = np.array(small); Dm = np.sqrt(((small[:, None] - small[None]) ** 2).mean(2))
adj = [Dm[i, i + 1] for i in range(K - 1) if ok[i + 1] == ok[i] + 1]
Dn = Dm / np.median(adj)
# ほしい口
js = json.load(open(SONG)); kana = json.load(open(SONG + ".kana")); spb = 60 / BPM
lens = {}
for vi in LEAD:
    t = 0.0
    for tok in js["vocals"][vi]["notes"].split():
        p = tok.split(":"); L = float(p[1])
        if not tok.startswith("R") and len(p) >= 3 and p[2] not in ("ー", "-", "~"): lens[round(t, 3)] = L
        elif not tok.startswith("R") and len(p) >= 3: pass
        t += L
N = int(DUR * FPS); want = np.zeros(N, int)
VMAP = {"a": 1, "i": 2, "e": 2, "u": 3, "o": 3, "n": 0}
for q, (b, ly) in enumerate(kana):
    L = lens.get(round(b, 3), 0.5); nb = kana[q + 1][0] if q + 1 < len(kana) else b + L
    e = min(b + L, nb)
    v = LM.vowel(ly) or "a"
    i0, i1 = int(b * spb * FPS), int(e * spb * FPS)
    want[max(0, i0):min(N, i1)] = VMAP.get(v, 1)
    c = LM.kata2hira(ly)[:1]
    if c in LM.LIPS and i1 - i0 >= 4 and 0 <= i0 < N: want[i0] = 0
# 短い休みは「息つぎ」= どの口でもよい（大きく開くのだけ避ける）
BR = -1; i = 0
while i < N:
    if want[i] == 0:
        j = i
        while j < N and want[j] == 0: j += 1
        if i > 0 and j < N and (j - i) < 0.5 * FPS: want[i:j] = BR
        i = j
    else: i += 1
C = np.array([[0, 2.5, 1.6, 1.2], [1.4, 0, 0.5, 0.7], [1.2, 0.5, 0, 0.8], [1.2, 0.8, 0.8, 0]])   # [ほしい][コマ]
def cost_of(c):
    if c == BR: return np.where(cls_src == 1, 0.5, 0.0)
    return C[c][cls_src]
# コマの並び（状態 = コマ × 向き）
S = 2 * K; kk = np.arange(S) % K; dd = np.arange(S) // K
T = np.full((S, S), np.inf)
for a in range(S):
    k, d = kk[a], dd[a]
    for nxt, d2, c in ((k + (1 if d == 0 else -1), d, 0.0), (k + (-1 if d == 0 else 1), 1 - d, 1.2)):
        if 0 <= nxt < K and abs(ok[nxt] - ok[k]) == 1: T[a, nxt + K * d2] = c
    T[a, a] = 0.5
    for j in np.where((Dn[k] < float(os.environ.get('MV_JNEAR', '2.6'))) & (np.abs(np.arange(K) - k) > 2))[0]:
        for d2 in (0, 1): T[a, j + K * d2] = min(T[a, j + K * d2], 2.5 + 0.8 * Dn[k, j])
# 同じあたりのコマばかり使うと単調なので、4秒ごとに解き、最近よく使ったコマを少し重くする（teto_mv.py と同じ）
USE_W = float(os.environ.get("MV_USEW", "0.012")); CH = 96
usage = np.zeros(K); p = np.zeros(N, int); start = None; diag = np.arange(S)
for c0 in range(0, N, CH):
    c1 = min(N, c0 + CH + 48); extra = USE_W * usage[kk]
    cost = cost_of(want[c0])[kk].astype(float) + extra
    if start is not None: cost = np.where(diag == start, 0.0, np.inf)
    back = np.zeros((c1 - c0, S), np.int16); hold = np.zeros(S)
    for i in range(c0 + 1, c1):
        tot = cost[:, None] + T; tot[diag, diag] += hold * 0.35
        arg = np.argmin(tot, 0); best = tot[arg, diag]
        hold = np.where(arg == diag, hold + 1, 0)
        cost = best + cost_of(want[i])[kk] + extra; back[i - c0] = arg; cost -= cost[np.isfinite(cost)].min()
    q = np.zeros(c1 - c0, int); q[-1] = int(np.argmin(cost))
    for i in range(c1 - c0 - 1, 0, -1): q[i - 1] = back[i, q[i]]
    e = min(CH, c1 - c0); p[c0:c0 + e] = q[:e]; start = q[e] if e < c1 - c0 else None
    usage *= 0.7; np.add.at(usage, kk[q[:e]], 1.0)
seq = [ok[kk[x]] for x in p]
sc = cls_src[kk[p]]
m = want >= 0
print(f"口の形が合っている {np.mean(sc[m] == want[m]):.0%}（歌っていない所で閉じている {np.mean(sc[want == 0] == 0):.0%}）"
      f"・飛び {int(np.sum(np.abs(np.diff(seq)) > 1))} 回・止まり {int(np.sum(np.diff(seq) == 0))} コマ / {N}")
json.dump(seq, open(OUT, "w"))
