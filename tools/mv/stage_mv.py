#!/usr/bin/env python3
"""舞台の上で重音テトが歌う YouTube 用の動画（ボカロ25曲『SCARLET FREQUENCY』）。
2026-10-26 人間「テトが立つ舞台です。ようつべ用の動画で使います。左には歌詞と曲タイトルを記載。歌詞ボードの後ろ側は曲に合わせてゲージが動くように。
歌詞は少しデジタルっぽい文字で。テトは歌の時歌詞に口の動きを合わせて。今まで作ってきたようつべ動画と同じ情報を記載」

1曲ぶんの動画（1920x1080・24コマ/秒・音つき）を作る。25曲をつなぐのは別（ffmpeg の concat）。
  ・背景: 人間が用意した舞台の絵（左に歌詞ボード、右に台）
  ・テト: 元の動画のコマを白い背景から切り抜いたもの（matte.py）を、台の上に立たせる。並びは teto_mv.py が歌詞の母音から選んだもの（*.seq.json）
          絵には手を加えない（口の切り貼りや、はずみ・ゆれはつけない）
  ・歌詞ボード: アルバム名（和名・英名）・♪ NN / 25・曲名（和名・英名）・ジャンル（和名・英名）・歌：重音テト / Vocal: Kasane Teto
          歌詞（デジタル風の字体 DotGothic16）。いま歌っている行は、歌った所から色が変わる（左から右へぬっていく）
          ボードの奥に、曲の音に合わせて動くゲージ（30本の棒）。右上の PLAYING に、曲の進み具合と時間
使い方: python3 stage_mv.py <曲番号> <songs.tsv> <歌の版 mp3> <曲の JSON（tempo）> <UST> <コマ並び json> <切り抜いたコマのフォルダ> <背景の絵> <出力 mp4>
"""
import sys, os, json, math, subprocess, importlib.util
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
NO, TSV, AUDIO, SONG, UST, SEQ, TM, BG, OUT = sys.argv[1:10]
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); import lyric_mouth as LM
sp = importlib.util.spec_from_file_location("sing", os.path.join(HERE, "../singer/sing.py")); SG = importlib.util.module_from_spec(sp); sp.loader.exec_module(SG)
FONT_J = os.path.join(HERE, "fonts/DotGothic16-Regular.ttf"); FONT_E = os.path.join(HERE, "fonts/Orbitron.ttf")
W, H, FPS = 1920, 1080, 24
ALBUM_J, ALBUM_E, KIND_J, KIND_E = "スカーレット・フリークエンシー", "SCARLET FREQUENCY", "ボカロ曲", "Vocaloid Songs"   # 人間が選んだアルバム名（2026-10-26）
rows = {r[0]: r for r in (l.rstrip("\n").split("\t") for l in open(TSV, encoding="utf-8")) if r and r[0]}
_, TJ, TE, GJ, GE = rows[NO]; TOTAL = len(rows)
PINK, PINK2, WHITE, GRAY = (255, 70, 120), (255, 150, 180), (245, 240, 245), (170, 160, 170)
def font(p, s): return ImageFont.truetype(p, s)

# ---------- 音 ----------
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", AUDIO], capture_output=True, text=True).stdout)
N = int(dur * FPS)
if os.environ.get("MV_MAXSEC"): N = min(N, int(float(os.environ["MV_MAXSEC"]) * FPS))
SR = 24000
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", AUDIO, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, stdin=subprocess.DEVNULL).stdout
au = np.frombuffer(raw, np.float32)
# ゲージ: 30本。40Hz〜12kHz を対数で分ける
NB = 30; NFFT = 2048; hop = SR / FPS
edges = np.geomspace(40, 12000, NB + 1); fr = np.fft.rfftfreq(NFFT, 1 / SR)
bidx = [np.where((fr >= edges[i]) & (fr < edges[i + 1]))[0] for i in range(NB)]
bidx = [b if len(b) else np.array([np.argmin(abs(fr - edges[i]))]) for i, b in enumerate(bidx)]
win = np.hanning(NFFT).astype(np.float32)
lev = np.zeros((N, NB), np.float32)
for i in range(N):
    c = int(i * hop + hop / 2); s = c - NFFT // 2
    seg = au[max(0, s):s + NFFT]
    if len(seg) < NFFT: seg = np.pad(seg, (0, NFFT - len(seg)))
    m = np.abs(np.fft.rfft(seg * win)) ** 2
    lev[i] = [10 * np.log10(m[b].mean() + 1e-12) for b in bidx]
lev += np.linspace(0, 14, NB)[None, :]                  # 高い音は小さいので、少し持ち上げて見やすく
top = np.percentile(lev, 98)
lev = np.clip((lev - (top - 48)) / 48, 0, 1) ** 1.3
sm = np.zeros_like(lev); cur = np.zeros(NB, np.float32)
for i in range(N):
    cur = np.maximum(lev[i], cur * 0.86); sm[i] = cur      # すっと上がって、ゆっくり下がる
peak = np.zeros_like(sm); pk = np.zeros(NB, np.float32)
for i in range(N):
    pk = np.maximum(sm[i], pk - 0.012); peak[i] = pk

# ---------- 歌詞の行 ----------
song = json.load(open(SONG)); b2s = SG.tempo_clock(song["bpm"], song.get("tempo"), song.get("beats", 4))
notes = [(b2s(b), b2s(b + L), LM.kata2hira(ly.strip().lstrip("+-~")), b) for b, L, ly in LM.read_ust(UST)]
notes = [n for n in notes if n[2] and n[2] not in ("R", "r", "息", "br")]
# のばしの母音（「しまう」のあとの「う」「う」…）は「〜」1つにまとめる（表示だけ）
VOW = {}
for row, v in (("あかさたなはまやらわがざだばぱゃぁ", "あ"), ("いきしちにひみりぎじぢびぴぃ", "い"), ("うくすつぬふむゆるぐずづぶぷゅぅ", "う"),
               ("えけせてねへめれげぜでべぺぇ", "え"), ("おこそとのほもよろをごぞどぼぽょぉ", "お")):
    for ch in row: VOW[ch] = v
disp = []; k = 0
while k < len(notes):
    j = k
    while j + 1 < len(notes) and notes[j + 1][2] == notes[k][2] and len(notes[k][2]) == 1 and notes[k][2] in "あいうえおん" and notes[j + 1][0] - notes[j][1] < 0.05: j += 1
    disp.append(notes[k])
    if j - k >= 2:                         # 同じ母音が3つ以上続く（のばし）ときだけ「〜」に
        disp.append((notes[k + 1][0], notes[k + 1][1], "〜", notes[k + 1][3]))
        for q in range(k + 2, j + 1): disp.append((notes[q][0], notes[q][1], "", notes[q][3]))
    else:
        for q in range(k + 1, j + 1): disp.append(notes[q])
    k = j + 1
notes = disp
# 行に分ける: 休み（0.32秒以上）で切る。続けて歌う所は、7〜16文字の間で「切りやすさ」がいちばん高い所で切る
#   切りやすさ = すきまの長さ ＋ のばした音（句の終わりに多い）＋ 助詞・語尾（を・は・が・に・で・て・ね・よ など）のあと
gaps = [(notes[k + 1][0] - notes[k][1]) if k + 1 < len(notes) else 99 for k in range(len(notes))]
P1, P2 = set("をはがにでてねよへ〜"), set("のともたいうかな")
# 言葉の切れ目（janome で、休みまでのひとまとまりを言葉に分ける）。知っている短い言葉の途中では切らない
wordok = [True] * len(notes)
try:
    from janome.tokenizer import Tokenizer
    TK = Tokenizer(); k = 0
    while k < len(notes):
        j = k
        while j < len(notes) - 1 and gaps[j] < 1.0: j += 1
        seg = notes[k:j + 1]; txt = "".join(n[2].replace("〜", "") for n in seg)
        cuts = set(); inside_long = set(); pos = 0
        for tk in TK.tokenize(txt):
            L_ = len(tk.surface)
            if L_ > 5: inside_long.update(range(pos + 1, pos + L_))
            pos += L_; cuts.add(pos)
        pos = 0
        for q, n in enumerate(seg):
            pos += len(n[2].replace("〜", ""))
            wordok[k + q] = pos in cuts or pos in inside_long
        k = j + 1
except Exception as e:
    print("言葉の切れ目なし:", e)
def score(j):
    t = notes[j][2]; sc = gaps[j] / 0.1 + (1.5 if notes[j][1] - notes[j][0] >= 0.38 else 0) + (1.0 if gaps[j] > 0.04 else 0)
    BPB = song.get("beats", 4)
    if j + 1 < len(notes) and int(notes[j + 1][3] // BPB) > int(notes[j][3] // BPB): sc += 0.8
    if t and t[-1] in P1: sc += 1.0
    elif t and t[-1] in P2: sc += 0.5
    sc += 2.0 if wordok[j] else -4.0
    return sc
lines = []; k = 0
while k < len(notes):
    chars = 0; j = k; best = None
    while j < len(notes):
        chars += len(notes[j][2])
        if gaps[j] >= 0.32 and chars >= 3 and (wordok[j] or gaps[j] >= 1.2 or chars >= 14): best = j; break
        if 6 <= chars <= 16 and (best is None or score(j) > score(best) + 0.05): best = j
        if chars > (20 if not wordok[j] else 16): break
        j += 1
    if best is None: best = min(j, len(notes) - 1)
    lines.append(notes[k:best + 1]); k = best + 1
LS = [l[0][0] for l in lines]; LE = [l[-1][1] for l in lines]
# 英訳（人間「歌詞も英訳を載せよう」2026-10-26）: 行と同じ数・同じ順の JSON（MV_EN）。いま歌っている行の下に出す
EN = None
if os.environ.get("MV_EN") and os.path.exists(os.environ["MV_EN"]):
    EN = json.load(open(os.environ["MV_EN"], encoding="utf-8"))
    if len(EN) != len(lines): print(f"注意: 英訳の行数 {len(EN)} が歌詞の行数 {len(lines)} とちがうので、英訳を出しません"); EN = None

# ---------- 文字の絵 ----------
def text_img(t, f, color, glow=None, stroke=0):
    bb = f.getbbox(t); w, h = bb[2] + 24, bb[3] + 24
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if glow:
        g = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ImageDraw.Draw(g).text((12, 12), t, font=f, fill=glow)
        im = Image.alpha_composite(im, g.filter(ImageFilter.GaussianBlur(6))); d = ImageDraw.Draw(im)
    d.text((12, 12), t, font=f, fill=color, stroke_width=stroke, stroke_fill=(10, 5, 10, 255))
    return im
def fit_font(path, t, size, maxw):
    while size > 16:
        f = font(path, size)
        if f.getbbox(t)[2] <= maxw: return f
        size -= 2
    return font(path, size)
BX0, BX1 = 140, 896                      # 歌詞ボードの中（ガラスの内側）
LYW = BX1 - BX0 - 20
cache = {}
def line_imgs(i, big):
    key = (i, big)
    if key in cache: return cache[key]
    t = "".join(n[2] for n in lines[i])
    f = fit_font(FONT_J, t, 50 if big else 34, LYW)
    if big:
        base = text_img(t, f, (240, 232, 240, 255), glow=(0, 0, 0, 255), stroke=3)
        hi = text_img(t, f, (255, 95, 140, 255), glow=(255, 40, 100, 230), stroke=3)
        # 1文字ずつの右端（ぬっていく位置）
        xs = []; acc = ""
        for n in lines[i]:
            acc += n[2]; xs.append(12 + f.getbbox(acc)[2])
        r = (np.asarray(base).astype(np.float32), np.asarray(hi).astype(np.float32), xs, [12 + f.getbbox("".join(n[2] for n in lines[i][:k]))[2] if k else 12 for k in range(len(lines[i]))])
    else:
        r = np.asarray(text_img(t, f, (225, 210, 225, 235), glow=(0, 0, 0, 255), stroke=3)).astype(np.float32)
    cache[key] = r
    if len(cache) > 12: cache.pop(next(iter(cache)))
    return r

en_cache = {}
def en_img(i):
    if i not in en_cache:
        t = EN[i]; f = fit_font(FONT_J, t, 27, LYW)
        en_cache[i] = np.asarray(text_img(t, f, (255, 205, 220, 245), glow=(0, 0, 0, 255), stroke=2)).astype(np.float32)
    return en_cache[i]
def blend(dst, src, x, y, alpha=1.0):
    h, w = src.shape[:2]
    x0, y0 = max(0, x), max(0, y); x1, y1 = min(dst.shape[1], x + w), min(dst.shape[0], y + h)
    if x1 <= x0 or y1 <= y0: return
    s = src[y0 - y:y1 - y, x0 - x:x1 - x]
    a = s[..., 3:4] / 255.0 * alpha
    d = dst[y0:y1, x0:x1].astype(np.float32)
    dst[y0:y1, x0:x1] = (s[..., :3][..., ::-1] * a + d * (1 - a)).astype(np.uint8)   # src は RGB、dst は BGR

# ---------- 動かない部分（背景＋ボードの文字）----------
bg = Image.open(BG).convert("RGB").resize((W, H), Image.LANCZOS)
bg = bg.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
base = np.asarray(bg)[..., ::-1].copy()
# ガラスの内側を暗くして（もとの動かない棒の絵を沈める）、文字とゲージを見やすく
gx0, gy0, gx1, gy1 = 118, 132, 918, 948
reg = base[gy0:gy1, gx0:gx1].astype(np.float32)
yy = np.linspace(0, 1, gy1 - gy0)[:, None, None]
base[gy0:gy1, gx0:gx1] = (reg * (0.42 + 0.1 * yy)).astype(np.uint8)
st = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(st)
def put(t, f, xy, col, glow=None):
    global st
    im = text_img(t, f, col + (255,), glow=glow); st.alpha_composite(im, (xy[0] - 12, xy[1] - 12))
put(ALBUM_E, font(FONT_E, 32), (BX0, 146), PINK, glow=(255, 40, 100, 170))
put(ALBUM_J, font(FONT_J, 19), (BX0 + 2, 194), GRAY)   # 人間「音楽ジャンルは動画からすべて外してほしい」（2026-10-26）
put(f"♪", font(FONT_J, 30), (BX0, 244), PINK)
put(f"{int(NO):02d} / {TOTAL}", font(FONT_E, 28), (BX0 + 36, 246), PINK2)
put(TJ, fit_font(FONT_J, TJ, 58, LYW), (BX0, 290), WHITE, glow=(255, 60, 120, 120))
put(TE, fit_font(FONT_E, TE, 28, LYW), (BX0 + 2, 364), (230, 215, 230))
put("歌：重音テト  /  Vocal: Kasane Teto", font(FONT_J, 22), (BX0 + 2, 418), PINK2)
d = ImageDraw.Draw(st)
for k in range(0, BX1 - BX0, 6): d.line([(BX0 + k, 484), (BX0 + k + 3, 484)], fill=(255, 70, 120, 150), width=2)
# テトの影（台の上）
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse((1434 - 120, 840, 1434 + 120, 878), fill=(0, 0, 0, 120))
st = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), st)
base_rgba = np.asarray(st).astype(np.float32)
a = base_rgba[..., 3:4] / 255.0
base = (base_rgba[..., :3][..., ::-1] * a + base * (1 - a)).astype(np.uint8)

# ---------- ゲージの棒 ----------
GB_Y1, GB_HMAX = 930, 420
nbw = (BX1 - BX0) / NB; bw = int(nbw * 0.72)
grad = np.zeros((GB_HMAX, bw, 4), np.float32)
tcol = np.linspace(0, 1, GB_HMAX)[::-1][:, None]
grad[..., 0] = (120 + 135 * tcol) ; grad[..., 1] = (20 + 80 * tcol); grad[..., 2] = (60 + 90 * tcol)   # RGB: 下は深い赤、上はピンク
grad[..., 3] = 120 + 60 * tcol
for k in range(0, GB_HMAX, 7): grad[k:k + 2, :, 3] *= 0.35                                     # 横すじ（デジタルのメーター）

# ---------- テト ----------
seq = json.load(open(SEQ))
tfr = {}
def teto(k):
    if k not in tfr: tfr[k] = cv2.imread(f"{TM}/{k:03d}.png", cv2.IMREAD_UNCHANGED)   # uint8 のまま持つ（float だと 240 コマで 1.8GB になり、メモリが足りなくなる）
    return tfr[k]
t0 = teto(0); al = t0[..., 3].astype(np.float32); ys = np.where(al.max(1) > 128)[0]; xs = np.where(al.max(0) > 128)[0]
TX = 1434 - (xs.min() + xs.max()) // 2; TY = 862 - ys.max()

def blend_bgra(dst, s, x, y):
    h, w = s.shape[:2]; x0, y0 = max(0, x), max(0, y); x1, y1 = min(W, x + w), min(H, y + h)
    s = s[y0 - y:y1 - y, x0 - x:x1 - x].astype(np.float32); a = s[..., 3:4] / 255.0
    dst[y0:y1, x0:x1] = (s[..., :3] * a + dst[y0:y1, x0:x1].astype(np.float32) * (1 - a)).astype(np.uint8)

fE18 = font(FONT_E, 16)
def mmss(t): return f"{int(t // 60)}:{int(t % 60):02d}"
proc = None if os.environ.get("MV_STILL") else subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", AUDIO,
                         "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", "-tune", "animation", "-pix_fmt", "yuv420p", "-g", "48",
                         "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-shortest", OUT], stdin=subprocess.PIPE)
time_cache = {}
STILL = [float(x) for x in os.environ.get("MV_STILL", "").split(",") if x]
for i in ([int(x * FPS) for x in STILL] if STILL else range(N)):
    t = i / FPS
    img = base.copy()
    # ゲージ
    for b in range(NB):
        h = int(sm[i, b] * GB_HMAX)
        x = int(BX0 + b * nbw + (nbw - bw) / 2)
        if h > 2:
            s = grad[GB_HMAX - h:]
            a = s[..., 3:4] / 255.0 * 0.6
            reg = img[GB_Y1 - h:GB_Y1, x:x + bw].astype(np.float32)
            img[GB_Y1 - h:GB_Y1, x:x + bw] = (s[..., [2, 1, 0]] * a + reg * (1 - a)).astype(np.uint8)
        py = GB_Y1 - int(peak[i, b] * GB_HMAX) - 4
        img[py:py + 3, x:x + bw] = (img[py:py + 3, x:x + bw] * 0.3 + np.array([150, 120, 255]) * 0.7).astype(np.uint8)
    # 歌詞
    ci = max([k for k in range(len(lines)) if LS[k] - 0.35 <= t] or [-1])
    if ci >= 0 and t > LE[ci] + 1.6 and ci + 1 < len(lines) and LS[ci + 1] - t > 1.2: ci_show = None       # 長い間奏: いまの行は消す
    else: ci_show = ci if ci >= 0 else None
    nxt = (ci + 1) if ci + 1 < len(lines) else None
    if ci_show is not None and ci_show - 1 >= 0 and t < LE[ci_show] + 1.6:
        blend(img, line_imgs(ci_show - 1, False), BX0 - 12, 534, 0.6)
    if ci_show is not None:
        bimg, himg, xe, xs_ = line_imgs(ci_show, True)
        blend(img, bimg, BX0 - 12, 592)
        # ぬる位置: 音の頭から終わりにかけて、その文字の左端から右端へ
        wx = 0
        for k, n in enumerate(lines[ci_show]):
            if t >= n[1]: wx = xe[k]
            elif t >= n[0]:
                wx = xs_[k] + (xe[k] - xs_[k]) * min(1, (t - n[0]) / max(0.08, min(0.35, n[1] - n[0]))); break
            else: break
        if wx > 0: blend(img, himg[:, :int(wx)], BX0 - 12, 592)
        if EN: blend(img, en_img(ci_show), BX0 - 12, 662)
    if nxt is not None:
        al_ = 0.9 if ci_show is None else 0.75
        blend(img, line_imgs(nxt, False), BX0 - 12, 716 if EN else 690, al_)
        if nxt + 1 < len(lines) and ci_show is not None: blend(img, line_imgs(nxt + 1, False), BX0 - 12, 772 if EN else 746, 0.45)
    # PLAYING の進み具合と時間
    px0, px1, py0 = 768, 888, 158
    img[py0:py0 + 9, px0:px0 + int((px1 - px0) * t / dur)] = (90, 70, 255)
    sec = int(t)
    if sec not in time_cache:
        time_cache.clear(); time_cache[sec] = np.asarray(text_img(f"{mmss(t)} / {mmss(dur)}", fE18, (255, 150, 180, 255))).astype(np.float32)
    blend(img, time_cache[sec], 760, 172)
    # テト
    blend_bgra(img, teto(int(seq[min(i, len(seq) - 1)])), TX, TY)
    if STILL: cv2.imwrite(f"{OUT}.still{t:.0f}.png", img); continue
    proc.stdin.write(img.tobytes())
if proc: proc.stdin.close(); proc.wait()
json.dump([{"t": LS[k], "end": LE[k], "text": "".join(n[2] for n in lines[k])} for k in range(len(lines))], open(OUT + ".lyrics.json", "w"), ensure_ascii=False)
print("ok", OUT, N, "コマ", len(lines), "行")
