#!/usr/bin/env python3
"""歌う重音テトの動画（ボカロ25曲）。2026-10-26 人間「この動画を使って今回作った曲の動画を作りましょう。歌に合わせて体を動かしたり、口を動かしたりして」
2版目（同日、人間「口の動き、元の動画だけで完結して欲しかった。体の動きも」「体の動きも送った動画の動きだけでよかった」）:
  1版目は、口だけを別のコマから切り貼りし、拍に合わせて絵全体をはずませていた。2版目はそれをやめ、
  **元の動画のコマを、そのまま（1枚まるごと）並べ直すだけ**で作る。絵には手を加えない（曲名の文字と、下に文字を置くための縮小だけ）。
使い方: python3 teto_mv.py <素材の動画のコマのフォルダ> <追跡の json> <歌だけの wav> <音の mp3> <曲名> <出力 mp4> [<曲の JSON（tempo）> <歌の UST>]
  （曲の JSON と UST を渡すと、歌詞の母音に口の形を合わせる）
しくみ:
  ・元の動画（240コマ）のコマごとに「口が閉じている・少し開く・開く」が分かっている（追跡の json の5番目の値）
  ・歌だけの音の大きさから、曲のコマごとに「閉じる・少し開く・開く」のどれがほしいかを決める
  ・どのコマを次に出すかを、全体でいちばん自然になるように選ぶ（動的計画法）:
      となりのコマへ進む／戻る … 自然（元の動画の動きそのもの）
      向きを変える（行って戻る） … 少しだけ不自然
      同じコマで止まる           … 長く止まると固まって見えるので、続くほど不自然
      離れたコマへ飛ぶ           … 姿勢がほぼ同じコマどうしのときだけ許す（つなぎ目が見えないように）
      口がほしい形とちがう       … 不自然（歌っていないのに口が開いている、はとくに不自然）
"""
import sys, json, subprocess, numpy as np, cv2, soundfile as sf
from PIL import Image, ImageDraw, ImageFont
FR, TRK, VOC, AUDIO, TITLE, OUT = sys.argv[1:7]
SONG = sys.argv[7] if len(sys.argv) > 8 else None; UST = sys.argv[8] if len(sys.argv) > 8 else None
FPS = 24
import os; REV = float(os.environ.get("MV_REV", "3.0")); JUMP = float(os.environ.get("MV_JUMP", "2.0")); JNEAR = float(os.environ.get("MV_JNEAR", "1.6")); HOLD = float(os.environ.get("MV_HOLD", "1.2"))
trk = json.load(open(TRK)); K = len(trk)
mo = np.array([t[4] for t in trk], float)
state = np.where(mo < 80, 0, np.where(mo < 300, 1, 2))
def src(k): return cv2.imread(f"{FR}/{k + 1:03d}.png")

# ---- 姿勢の近さ（口のまわりを除いた、小さく縮めた絵どうしの差）----
MX0, MY0 = 342, 291
small = []
for k in range(K):
    g = cv2.cvtColor(src(k), cv2.COLOR_BGR2GRAY).astype(np.float32)
    _, dx, dy, _, _ = trk[k]; mx, my = MX0 + dx, MY0 + dy
    g[my - 45:my + 45, mx - 55:mx + 55] = 255                                  # 口のちがいは姿勢の差に入れない
    small.append(cv2.resize(g, (72, 128), interpolation=cv2.INTER_AREA).ravel())
small = np.array(small)
D = np.sqrt(((small[:, None, :] - small[None, :, :]) ** 2).mean(2))
step = np.median([D[k, k + 1] for k in range(K - 1)])                          # となりのコマどうしのふつうの差
Dn = D / step                                                                   # 1.0 ＝ となりのコマくらいの差

# ---- 曲のコマごとに、ほしい口 ----
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", AUDIO], capture_output=True, text=True).stdout)
N = int(dur * FPS)
v, sr = sf.read(VOC); v = v.mean(1) if v.ndim > 1 else v
hop = sr // FPS
env = np.array([np.sqrt(np.mean(v[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(N)])
db = 20 * np.log10(env + 1e-9); top = np.percentile(db[db > -60], 95) if (db > -60).any() else -20
want = np.where(db < top - 30, 0, np.where(db < top - 14, 1, 2))
for i in range(1, N - 1):
    if want[i - 1] == want[i + 1] != want[i]: want[i] = want[i - 1]
OPEN_W = float(os.environ.get("MV_OPENW", "0.35"))
MC = np.array([[0, 0.9, 2.5], [0.8 * OPEN_W, 0, 0.6 * OPEN_W], [1.6 * OPEN_W, 0.5 * OPEN_W, 0]])   # [ほしい口][コマの口]。黙っているのに口が開くのは強く避ける
CK = MC[:, state]; cls = want.copy()                                            # CK[種類][コマ] = そのコマを出したときの不自然さ
# ---- 歌詞があるときは、言葉の母音に口の形を合わせる（3版目。人間「口の動きも言葉の動きに合わせてほしいかも」）----
VOWELS = "naiueor"   # r = 短い息つぎ（口は軽くゆるむだけ。閉じ切らなくてよい）
if UST:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import lyric_mouth as LM, importlib.util as IU
    sp = IU.spec_from_file_location("sing", os.path.join(os.path.dirname(os.path.abspath(__file__)), "../singer/sing.py")); SG = IU.module_from_spec(sp); sp.loader.exec_module(SG)
    song = json.load(open(SONG)); b2s = SG.tempo_clock(song["bpm"], song.get("tempo"), song.get("beats", 4))
    tl = LM.timeline(UST, b2s, FPS, N)
    # 元のコマの口の幅と高さ（口の中のピンクと縁を数える）
    mw = np.zeros(K); mh = np.zeros(K)
    for k in range(K):
        _, dx, dy, _, _ = trk[k]; mx, my = MX0 + dx, MY0 + dy
        im = src(k)[my - 30:my + 30, mx - 40:mx + 40].astype(int)
        m = ((im[..., 1] < 170) & (im[..., 2] > 120)).astype(np.uint8)
        n_, lab, st, _ = cv2.connectedComponentsWithStats(m)
        if n_ > 1: i_ = 1 + np.argmax(st[1:, 4]); mw[k], mh[k] = st[i_, 2], st[i_, 3]
    # 母音ごとの口の形の見本（幅, 高さ。元の動画の口を測って決めた）
    PROTO = {"r": (30, 12), "n": (14, 5), "a": (42, 25), "i": (41, 12), "u": (25, 15), "e": (38, 18), "o": (27, 23)}
    VW = float(os.environ.get("MV_VW", "0.8"))
    CK = np.zeros((7, K))
    for ci, c in enumerate(VOWELS):
        pw, ph = PROTO[c]; dist = np.sqrt(((mw - pw) / 8) ** 2 + ((mh - ph) / 4) ** 2)
        CK[ci] = VW * np.minimum(dist, 5)
        if c == "n": CK[ci] = 0.9 * np.minimum(dist, 5)                             # 歌っていないのに開いているのは強く避ける
        if c == "r": CK[ci] = 0.25 * np.minimum(dist, 5) * (mh > 22)                # 息つぎ: 大きく開いていなければよい
    tl = list(tl); i = 0
    while i < N:                                                                    # 0.6 秒より短い休みは「息つぎ」に
        if tl[i] == "n":
            j = i
            while j < N and tl[j] == "n": j += 1
            if 0 < i and j < N and (j - i) < 0.6 * FPS:
                for q in range(i, j): tl[q] = "r"
            i = j
        else: i += 1
    cls = np.array([VOWELS.index(c) for c in tl])
    near = np.argmin(np.stack([np.sqrt(((mw - PROTO[c][0]) / 8) ** 2 + ((mh - PROTO[c][1]) / 4) ** 2) for c in VOWELS[:6]]), 0)

# ---- いちばん自然なコマの並びを選ぶ（状態 = コマ番号 × 進む向き(0:前,1:後)）----
S = 2 * K
kk = np.arange(S) % K; dd = np.arange(S) // K
T = np.full((S, S), np.inf)
for a in range(S):
    k, d = kk[a], dd[a]
    nxt = k + (1 if d == 0 else -1)
    if 0 <= nxt < K: T[a, nxt + K * d] = 0.0                                    # そのまま進む
    back = k + (-1 if d == 0 else 1)
    if 0 <= back < K: T[a, back + K * (1 - d)] = REV                          # 向きを変える
    T[a, a] = HOLD                                                               # 止まる
    near_ = np.where((Dn[k] < JNEAR) & (np.abs(np.arange(K) - k) > 2))[0]         # 姿勢がほぼ同じ離れたコマへ飛ぶ
    for j in near_:
        for d2 in (0, 1): T[a, j + K * d2] = min(T[a, j + K * d2], JUMP + 0.8 * Dn[k, j])
# 同じあたりのコマばかり使うと単調になるので、区切りごと（4秒）に解き、最近よく使ったコマを少し重くする
USE_W = float(os.environ.get("MV_USEW", "0.008")); CH = 96
usage = np.zeros(K); path = np.zeros(N, int); start = None
for c0 in range(0, N, CH):
    c1 = min(N, c0 + CH + 48)                                                   # 少し先まで見て解き、前の CH コマだけ使う
    extra = USE_W * usage[kk]
    cost = CK[cls[c0]][kk] + extra
    if start is not None: cost = np.where(np.arange(S) == start, 0.0, np.inf)
    back = np.zeros((c1 - c0, S), np.int16); hold = np.zeros(S); diag = np.arange(S)
    for i in range(c0 + 1, c1):
        tot = cost[:, None] + T
        tot[diag, diag] += hold * HOLD                                           # 止まりが続くと重くする
        arg = np.argmin(tot, 0); best = tot[arg, diag]
        hold = np.where(arg == diag, hold + 1, 0)
        cost = best + CK[cls[i]][kk] + extra; back[i - c0] = arg
        cost -= cost[np.isfinite(cost)].min()
    p_ = np.zeros(c1 - c0, int); p_[-1] = int(np.argmin(cost))
    for i in range(c1 - c0 - 1, 0, -1): p_[i - 1] = back[i, p_[i]]
    e = min(CH, c1 - c0); path[c0:c0 + e] = p_[:e]
    start = p_[e] if e < c1 - c0 else None
    usage *= 0.75; np.add.at(usage, kk[p_[:e]], 1.0)
seq = kk[path]
match = np.mean(state[seq] == want)
jumps = int(np.sum(np.abs(np.diff(seq)) > 1)); holds = int(np.sum(np.diff(seq) == 0))
dq = np.diff(seq); revs = int(np.sum(dq[1:] * dq[:-1] < 0))
sil = want == 0; quiet_ok = np.mean(state[seq][sil] == 0) if sil.any() else 1
if UST:
    sg = (cls > 0) & (cls < 6)
    print(f"歌っていない所で閉じている {np.mean(near[seq][cls == 0] == 0):.0%}・歌っている所で母音の形が合っている {np.mean(near[seq][sg] == cls[sg]):.0%}")
print(f"口の一致 {match:.0%}（歌っていない所で口が閉じている {quiet_ok:.0%}）/ 飛び {jumps} 回 / 向き変え {revs} 回 / 止まり {holds} コマ（全 {N} コマ）")

# ---- 曲名（下に置く。絵は 0.9 倍にして上へ寄せ、文字の場所をあける。動きはつけない）----
font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 40, index=0)
font2 = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 26, index=0)
ov = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
for dx_, dy_ in ((-2, 0), (2, 0), (0, -2), (0, 2)):
    d.text((36 + dx_, 1150 + dy_), TITLE, font=font, fill=(255, 255, 255, 255)); d.text((38 + dx_, 1204 + dy_), "歌：重音テト（仮）", font=font2, fill=(255, 255, 255, 255))
d.text((36, 1150), TITLE, font=font, fill=(170, 30, 50, 255)); d.text((38, 1204), "歌：重音テト（仮）", font=font2, fill=(90, 90, 100, 255))
OV = np.asarray(ov).astype(np.float32); OA = OV[..., 3:4] / 255.0; OC = OV[..., [2, 1, 0]]
G = np.float32([[0.9, 0, 36], [0, 0.9, 4]])
frames = {}
for k in range(K):
    img = cv2.warpAffine(src(k), G, (720, 1280), flags=cv2.INTER_AREA, borderValue=(255, 255, 255))
    frames[k] = (OC * OA + img.astype(np.float32) * (1 - OA)).astype(np.uint8).tobytes()
sing = want > 0; sing_open = np.mean(state[seq][sing] > 0) if sing.any() else 1
print(f"歌っている所で口が開いている {sing_open:.0%} / 1分ごとに使ったコマの種類", [len(set(seq[a:a + 1440])) for a in range(0, N, 1440)])
if os.environ.get("MV_DRY"): sys.exit(0)
proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "720x1280", "-r", str(FPS), "-i", "-", "-i", AUDIO,
                         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", OUT], stdin=subprocess.PIPE)
for k in seq: proc.stdin.write(frames[int(k)])
proc.stdin.close(); proc.wait()
json.dump([int(k) for k in seq], open(OUT + ".seq.json", "w"))
print("ok", OUT, N, "コマ")
