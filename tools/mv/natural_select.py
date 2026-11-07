"""元の動画を、自然な速さのまま前へ流し続けて、歌っている所は「口が動いているところ」、休みは「口を閉じているところ」を使う
（2026-11-08『白い息のリテイク』。人間「雪とか、息とか自然じゃないね。なんか途中止まって急に動いたりするし」）。
  前の作り方（lipsync_select.py）は 1 音ずつ口を合わせるために、コマを細かく飛ばしていた。そのたびに雪・白い息・体の動きがつながらず、
  止まったり急に動いたりして見えた。ここでは:
    ・コマは必ず 1 コマずつ前へ（速さはいつも 1 倍。止めない・戻らない・細かく飛ばない）
    ・切りかえるのは「歌いはじめ」「歌い終わり」と、元の動画の区間が終わる所だけ。切りかえは 0.5 秒かけて重ねる（雪が自然につながる）
    ・切りかえ先は、いまの絵といちばん姿勢の近いコマ（重ねても二重に見えにくい）
  python3 natural_select.py <コマのフォルダ> <追跡 json> <曲.json> <bpm> <長さ秒> <出力 json>
出力: コマごとに [出すコマ, 重ねる前のコマ(-1=なし), 前のコマの濃さ]
"""
import sys, json, numpy as np, cv2
FR, TRK, SONG, BPM, DUR, OUT = sys.argv[1:7]
BPM = float(BPM); DUR = float(DUR); FPS = 24; XF = 12                                # 重ねる長さ（コマ）
trk = json.load(open(TRK)); K = len(trk)
area = np.array([t[6] for t in trk]); talk_src = area >= 75
# 元の動画の区間（口が動く／閉じている）。短いゆれ（3コマ以下）はならす
runs = []; s = 0
for k in range(1, K + 1):
    if k == K or talk_src[k] != talk_src[s]:
        runs.append([s, k - 1, bool(talk_src[s])]); s = k
merged = []
for r in runs:
    if merged and (r[1] - r[0] < 4 or merged[-1][2] == r[2]): merged[-1][1] = r[1]
    else: merged.append(r)
runs = [r for r in merged if r[1] - r[0] >= 12]
print("元の区間", runs)
small = np.array([cv2.resize(cv2.cvtColor(cv2.imread(f"{FR}/{k + 1:03d}.png"), cv2.COLOR_BGR2GRAY), (128, 72), interpolation=cv2.INTER_AREA).astype(np.float32).ravel() for k in range(K)])
def pose_d(a, b): return float(np.sqrt(((small[a] - small[b]) ** 2).mean()))
# 歌っている所（かなの開始と長さ）。0.8 秒より短い休みは歌っている扱い
js = json.load(open(SONG)); kana = json.load(open(SONG + ".kana")); spb = 60 / BPM
lens = {}; t = 0.0
for tok in js["vocals"][0]["notes"].split():
    p = tok.split(":"); L = float(p[1])
    if not tok.startswith("R") and len(p) >= 3: lens.setdefault(round(t, 3), 0); lens[round(t, 3)] = L
    t += L
N = int(DUR * FPS); sing = np.zeros(N, bool)
for q, (b, ly) in enumerate(kana):
    L = lens.get(round(b, 3), 0.5); e = b + L
    sing[int(b * spb * FPS):min(N, int(e * spb * FPS) + 1)] = True
i = 0
while i < N:
    if not sing[i]:
        j = i
        while j < N and not sing[j]: j += 1
        if 0 < i and j < N and (j - i) < 0.8 * FPS: sing[i:j] = True
        i = j
    else: i += 1
# 区間ごとに流す
out = []; cur = 0; fade = None   # fade = [前のコマ, 残り]
def run_of(k):
    if want_now is None: return [0, K - 1, None]
    for r in runs:
        if r[0] <= k <= r[1]: return r
    return None
def pick(want, frm, need):
    """want（歌う=True）の区間の中で、frm と姿勢が近く、need コマ以上つづけて流せる開始コマ"""
    best = None
    for r in runs:
        if want is not None and r[2] != want: continue
        for k in range(r[0], max(r[0], r[1] - min(need, r[1] - r[0]) ) + 1, 2):
            d = pose_d(frm, k) - 0.02 * min(need, r[1] - k) + 6.0 * recent.get((r[0], k // 24), 0)   # 同じ所ばかり使わない
            if best is None or d < best[0]: best = (d, k)
    for key in list(recent): recent[key] *= 0.6
    rr = next(r for r in runs if r[0] <= best[1] <= r[1]) if want is not None else [0]
    recent[(rr[0], best[1] // 24)] = recent.get((rr[0], best[1] // 24), 0) + 1
    return best[1]
want_now = True; recent = {}
i = 0
while i < N:
    want = bool(sing[i]); j = i; want_now = want
    while j < N and bool(sing[j]) == want: j += 1
    need = j - i
    if not want and need > 3 * FPS: want = None; want_now = None                                        # 長い休み（前奏・間奏）: 口の形は問わず、元の動画をそのまま長く流す
    r = run_of(cur)
    if r is None or (want is not None and r[2] != want) or cur >= r[1]:
        nk = pick(want, cur, need)
        if nk != cur: fade = [cur, XF]
        cur = nk
    for q in range(i, j):
        r = run_of(cur)
        if want is None: r = [0, K - 1, None]
        if r is None or cur >= r[1]:                                                   # 区間の終わり: 同じ種類の別の所へ
            nk = pick(want, cur, j - q); fade = [cur, XF]; cur = nk
        if fade and fade[1] > 0:
            a = fade[1] / (XF + 1); out.append([int(cur), int(min(K - 1, fade[0])), round(a, 3)]); fade[0] += 1; fade[1] -= 1
        else: out.append([int(cur), -1, 0.0])
        cur += 1
    i = j
json.dump(out, open(OUT, "w"))
cuts = sum(1 for i in range(1, len(out)) if out[i][1] >= 0 and out[i - 1][1] < 0)
mouth_ok = np.mean([(talk_src[o[0]] == sing[n]) for n, o in enumerate(out)])
print(f"切りかえ {cuts} 回（平均 {N / FPS / max(1, cuts):.1f} 秒に1回）・歌う所で口が動き、休みで閉じている {mouth_ok:.0%}")
