"""MV の仕上げ（YouTube 用・Instagram 用）。曲名（和・英）・歌詞（日本語＋英訳。歌った所から色が変わる）・歌・作者などの情報をのせる。
2026-11-08 人間「歌詞と曲名、英訳等の情報、作曲者、ボーカル等が動画に情報として載るようにしてください。インスタ用動画とyoutube用に作成してください」
  python3 mv_compose.py <曲の名前 whitebreath|honeysour> <形 yt|ig> <出力 mp4>
曲ごとの材料（下の SONGS）: 映像（元の動画のコマの並び、または作った映像）・歌の版の音・曲の JSON（歌詞の時刻）
形:
  yt … 1920×1080。白い息: 元の横長の動画を全面に。ハニー・サワー: 縦の映像を中央に、左に曲の情報、右に歌詞
  ig … 1080×1920・60秒（前に作ったインスタ用と同じ長さ）。上に曲名、まん中に映像、下に歌詞
"""
import sys, os, json, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lyric_lines as LL, lyrics_data as LD

NAME, FORM, OUT = sys.argv[1:4]
FPS = 24
NF = "/usr/share/fonts/opentype/noto/"
GF = "/usr/share/fonts/truetype/google-fonts/"
SONGS = {
    "whitebreath": dict(data=LD.WHITEBREATH, audio="/tmp/ab/wb9.mp3", song="/mnt/user-data/outputs/vbq/vtp-06-whitebreath-ballad-v9vo.json", lead=[0],
                        frames="/tmp/ab/wbmv/fr", seq="/tmp/ab/wbmv/seq.json", ig_start=237.0,
                        jp_font=(NF + "NotoSerifCJK-SemiBold.ttc", 0), en_font=(GF + "Lora-Italic-Variable.ttf", 0),
                        sans=(NF + "NotoSansCJK-Medium.ttc", 0), fill=(222, 230, 245), sung=(255, 228, 180), stroke=(16, 24, 52),
                        en_fill=(205, 218, 238), accent=(255, 196, 130)),
    "honeysour": dict(data=LD.HONEYSOUR, audio="/tmp/ab/hs6.mp3", song="/mnt/user-data/outputs/vbq/vtp-07-honeysour-v6vo.json", lead=[0, 2],
                      video="/tmp/ab/hsmv/ハニー・サワー 試作MV3（字幕なし）.mp4", ig_start=46.2,
                      jp_font=(NF + "NotoSansCJK-Black.ttc", 0), en_font=(GF + "Poppins-Bold.ttf", 0),
                      sans=(NF + "NotoSansCJK-Bold.ttc", 0), fill=(255, 255, 255), sung=(255, 206, 60), stroke=(150, 40, 110),
                      en_fill=(255, 245, 230), accent=(255, 190, 40)),
}
S = SONGS[NAME]; D = S["data"]
def F(spec, size): return ImageFont.truetype(spec[0], size, index=spec[1])
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", S["audio"]], capture_output=True, text=True).stdout)
T0 = S["ig_start"] if FORM == "ig" else 0.0
LEN = 60.0 if FORM == "ig" else dur
if os.environ.get("MV_T0"): T0 = float(os.environ["MV_T0"]); LEN = float(os.environ.get("MV_LEN", "4"))   # 試し書き用
N = int(LEN * FPS)
W, H = (1920, 1080) if FORM == "yt" else (1080, 1920)

# ---------- 歌う人（ハニー・サワー: テト・男性ボイス・ふたり）----------
js = json.load(open(S["song"]))
def spans(vi):
    out = []; t = 0.0
    if vi >= len(js["vocals"]): return out
    for tok in js["vocals"][vi]["notes"].split():
        L = float(tok.split(":")[1])
        if not tok.startswith("R"): out.append((t, t + L))
        t += L
    return out
SPB = 60 / D["bpm"]; sp0, sp2 = spans(0), spans(2) if NAME == "honeysour" else []
def who(t0, t1):
    m = (t0 + t1) / 2 / SPB
    a = any(x <= m < y for x, y in sp0); b = any(x <= m < y for x, y in sp2)
    return "both" if a and b else ("man" if b else "teto")
EV = LL.events(S["song"], LL.table_from(D["lines"]), D["bpm"], S["lead"], who_of=who)
WHO_COL = {"teto": (255, 110, 170), "man": (90, 170, 255), "both": (255, 190, 40)}

# ---------- 文字の絵（ふち・やわらかい影つき）----------
def text_img(txt, font, fill, stroke, sw, glow=0, glow_col=None, max_w=None):
    while max_w and font.getlength(txt) > max_w and font.size > 18: font = ImageFont.truetype(font.path, font.size - 2, index=getattr(font, "index", 0))
    bb = font.getbbox(txt, stroke_width=sw); pad = 24 + glow
    w, h = bb[2] - bb[0] + 2 * pad, bb[3] - bb[1] + 2 * pad
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((pad - bb[0], pad - bb[1]), txt, font=font, fill=fill, stroke_width=sw, stroke_fill=stroke)
    sh = Image.new("RGBA", (w, h), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    ds.text((pad - bb[0] + 2, pad - bb[1] + 3), txt, font=font, fill=(0, 0, 0, 150), stroke_width=sw + 2, stroke_fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(5))
    if glow:
        gl = Image.new("RGBA", (w, h), (0, 0, 0, 0)); dg = ImageDraw.Draw(gl)
        dg.text((pad - bb[0], pad - bb[1]), txt, font=font, fill=glow_col, stroke_width=sw + 3, stroke_fill=glow_col)
        sh = Image.alpha_composite(sh, gl.filter(ImageFilter.GaussianBlur(glow)))
    return Image.alpha_composite(sh, im)

# 歌詞の置き場所と大きさ
if FORM == "yt" and NAME == "whitebreath": LX, LY, LW, JS, ES, ALIGN = W // 2, 905, 1500, 54, 30, "c"
elif FORM == "yt": LX, LY, LW, JS, ES, ALIGN = 1590, 520, 560, 50, 26, "c"
else: LX, LY, LW, JS, ES, ALIGN = W // 2, 1690, 1000, 60, 30, "c"
jpF, enF = F(S["jp_font"], JS), F(S["en_font"], ES)
for e in EV:
    sw = 4
    st = S["stroke"] if NAME == "whitebreath" else WHO_COL[e["who"]]
    glow = 10 if NAME == "whitebreath" else 0
    if FORM == "yt" and NAME == "honeysour":     # 右の欄は狭いので、長い行は2行に分けない代わりに字を小さく
        pass
    e["im0"] = text_img(e["jp"], jpF, S["fill"], st, sw, glow, (120, 160, 230, 90), LW)
    e["im1"] = text_img(e["jp"], jpF, S["sung"], st, sw, glow, (255, 190, 120, 140), LW)
    if e["im1"].size != e["im0"].size: e["im1"] = e["im1"].resize(e["im0"].size)
    e["en"] = text_img(e["en"], enF, S["en_fill"], (20, 20, 40) if NAME == "whitebreath" else st, 2, 0, None, LW)
    e["show0"] = max(0, e["t0"] - 0.35); e["show1"] = e["t1"] + 0.8
for a, b in zip(EV, EV[1:]):
    a["show1"] = min(a["show1"], b["show0"] + 0.15)

def lyric_layers(t):
    """時刻 t に出す歌詞の [(絵, x, y, 不透明度)]"""
    out = []
    for e in EV:
        if not (e["show0"] <= t < e["show1"]): continue
        a = min(1, (t - e["show0"]) / 0.3, (e["show1"] - t) / 0.3)
        n = len(e["syl"]); done = 0.0
        for s0, s1, _ in e["syl"]:
            if t >= s1: done += 1
            elif t > s0: done += (t - s0) / max(0.05, s1 - s0)
        f = done / n
        im0, im1 = e["im0"], e["im1"]
        pad = 24 + (10 if NAME == "whitebreath" else 0); inner = im0.size[0] - 2 * pad
        cut = int(pad + inner * f)
        im = im0.copy()
        if cut > pad: im.paste(im1.crop((0, 0, cut, im1.size[1])), (0, 0))
        x = LX - im.size[0] // 2; y = LY - im.size[1] // 2
        out.append((im, x, y, a))
        en = e["en"]; out.append((en, LX - en.size[0] // 2, y + im.size[1] - 18, a))
    return out

# ---------- 曲の情報 ----------
sans = lambda s: F(S["sans"], s)
def info_block():
    """曲名（和・英）・歌・ジャンル（左上 / 左の欄 / 上）"""
    L = []
    if FORM == "yt" and NAME == "whitebreath":
        L.append((text_img(D["title_jp"], F(S["jp_font"], 56), (245, 248, 255), S["stroke"], 3, 12, (120, 170, 255, 110)), 40, 28))
        L.append((text_img(D["title_en"], F(S["en_font"], 32), S["accent"], (20, 20, 40), 2), 44, 118))
        L.append((text_img(f"{D['vocal_jp']}  /  {D['vocal_en']}", sans(22), (225, 232, 245), (20, 20, 40), 2), 44, 168))
    elif FORM == "yt":
        x = 60; MW = 560                            # 左の欄（映像は x=656 から）に収める
        L.append((text_img(D["title_jp"], F(S["jp_font"], 76), (255, 255, 255), (150, 40, 110), 6, max_w=MW), x, 300))
        L.append((text_img(D["title_en"], F(S["en_font"], 44), (255, 206, 60), (150, 40, 110), 3, max_w=MW), x + 4, 410))
        L.append((text_img(D["vocal_jp"], sans(28), (255, 255, 255), (150, 40, 110), 3, max_w=MW), x + 4, 500))
        L.append((text_img(D["vocal_en"], F(S["en_font"], 22), (255, 245, 230), (150, 40, 110), 2, max_w=MW), x + 4, 550))
        L.append((text_img(LD.CREDIT_JP, sans(20), (255, 240, 250), (150, 40, 110), 2, max_w=MW), x + 4, 900))
        L.append((text_img(LD.CREDIT_EN, F(S["en_font"], 16), (255, 240, 250), (150, 40, 110), 2, max_w=MW), x + 4, 940))
        xx = 1330
        for lab, col in (("● テト", WHO_COL["teto"]), ("● 男性ボイス", WHO_COL["man"]), ("● ふたり", WHO_COL["both"])):
            im_ = text_img(lab, sans(22), col, (40, 20, 40), 3); L.append((im_, xx, 960)); xx += im_.size[0] - 30
    else:
        L.append((text_img(D["title_jp"], F(S["jp_font"], 64), (255, 255, 255), S["stroke"] if NAME == "whitebreath" else (150, 40, 110), 4,
                           10 if NAME == "whitebreath" else 0, (120, 170, 255, 110)), None, 40))
        L.append((text_img(D["title_en"], F(S["en_font"], 34), S["accent"], (20, 20, 40) if NAME == "whitebreath" else (150, 40, 110), 2), None, 132))
        L.append((text_img(f"{D['vocal_jp']} / {D['vocal_en']}", sans(22), (235, 238, 248), (20, 20, 40), 2), None, 186))
        L.append((text_img(LD.CREDIT_EN, F(S["en_font"], 18), (225, 230, 240), (20, 20, 40), 2), None, 1858))
    return [(im, (W - im.size[0]) // 2 if x is None else x, y) for im, x, y in L]
INFO = info_block()
# 白い息の YouTube: 前奏と後奏で、作者とジャンルのカード（ゆっくり出て消える）
CARD = []
if FORM == "yt" and NAME == "whitebreath":
    # 2026-11-08 人間「曲のジャンルはいらないよ」: ジャンルは出さない
    for im, y in ((text_img(LD.CREDIT_JP, sans(26), (240, 244, 252), (20, 20, 40), 2), 945),
                  (text_img(LD.CREDIT_EN, F(S["en_font"], 24), (220, 228, 244), (20, 20, 40), 2), 990)):
        CARD.append((im, (W - im.size[0]) // 2, y))
def card_alpha(t):
    if not CARD: return 0
    for a, b in ((2.0, 19.5), (285.0, dur)):
        if a <= t < b: return min(1, (t - a) / 1.2, (b - t) / 1.2)
    return 0

# ---------- 映像 ----------
_dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
def morph(A, B, a):
    """2枚の絵のあいだを、動きの流れ（オプティカルフロー）で動かしながら重ねる（ただ重ねると、頭が二重に見える。2026-11-08）"""
    ga = cv2.cvtColor(A.astype(np.uint8), cv2.COLOR_BGR2GRAY); gb = cv2.cvtColor(B.astype(np.uint8), cv2.COLOR_BGR2GRAY)
    fab = _dis.calc(ga, gb, None); fba = _dis.calc(gb, ga, None)
    h, w = ga.shape; gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    wa = cv2.remap(A, gx + a * fba[..., 0], gy + a * fba[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    wb = cv2.remap(B, gx + (1 - a) * fab[..., 0], gy + (1 - a) * fab[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return wa * (1 - a) + wb * a
def frames_wb():
    """2026-11-08 人間「雪は降り続けるものだから戻るのはおかしいよ」: コマは前へ進むだけ（lipsync_select.py の MV_FORWARD=1）。
    離れたコマへ飛ぶ所は、元の続きのコマと飛んだ先のコマを 4 コマかけて重ねて切りかえる（雪がいきなり別の場所へ飛ばないように）"""
    seq = json.load(open(S["seq"])); cache = {}
    okset = set(range(0, 15)) | set(range(112, 240))                          # 生成AIの文字が映っているコマ（15〜111）は使わない
    def get(k):
        if k not in cache: cache[k] = cv2.imread(f"{S['frames']}/{k + 1:03d}.png").astype(np.float32)
        return cache[k]
    i0 = int(round(T0 * FPS)); fade = []                                       # 重ねる元のコマ（続き）の予定
    for i in range(N):
        g = min(len(seq) - 1, i0 + i); k = seq[g]
        if g > 0 and seq[g] != seq[g - 1] + 1:
            fade = [seq[g - 1] + 1 + m for m in range(4) if seq[g - 1] + 1 + m in okset]
            if len(fade) < 4: fade = []
            fade = list(enumerate(fade))
        img = get(k)
        if fade:
            m, kold = fade.pop(0); a = (m + 1) / 5.0
            img = morph(get(kold), img, a)
        yield img.astype(np.uint8)
def frames_video():
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(T0), "-i", S["video"], "-t", str(LEN), "-f", "rawvideo", "-pix_fmt", "bgr24", "-r", str(FPS), "-"],
                         stdout=subprocess.PIPE)
    w0, h0 = 720, 1280; last = None
    for i in range(N):
        b = p.stdout.read(w0 * h0 * 3)
        if len(b) == w0 * h0 * 3: last = np.frombuffer(b, np.uint8).reshape(h0, w0, 3)
        yield last
def cover(img, w, h):
    s = max(w / img.shape[1], h / img.shape[0]); r = cv2.resize(img, (int(img.shape[1] * s + 1), int(img.shape[0] * s + 1)), interpolation=cv2.INTER_AREA)
    y = (r.shape[0] - h) // 2; x = (r.shape[1] - w) // 2; return r[y:y + h, x:x + w]
def blur_bg(img, w, h, dark=0.55):
    s = cover(cv2.resize(img, (img.shape[1] // 8, img.shape[0] // 8), interpolation=cv2.INTER_AREA), w // 8, h // 8)
    s = cv2.GaussianBlur(s, (0, 0), 3); return (cv2.resize(s, (w, h), interpolation=cv2.INTER_LINEAR) * dark).astype(np.uint8)
def base(img):
    if NAME == "whitebreath" and FORM == "yt":
        return cv2.resize(img, (W, H), interpolation=cv2.INTER_LANCZOS4)
    if NAME == "whitebreath":                       # 3:4 に切り出して（テトが中心）、上下はぼかした背景
        c = img[:, 370:910]; c = cv2.resize(c, (1080, 1440), interpolation=cv2.INTER_LANCZOS4)
        bg = blur_bg(img, W, H); bg[240:1680] = c; return bg
    if FORM == "yt":                                # 縦の映像を中央に。左右はぼかした背景
        bg = blur_bg(img, W, H, 0.5); v = cv2.resize(img, (608, 1080), interpolation=cv2.INTER_AREA); bg[:, 656:1264] = v; return bg
    return cv2.resize(img, (W, H), interpolation=cv2.INTER_LANCZOS4)
# 歌詞と情報を読みやすくする、うすい暗がり（グラデーション）
shade = np.zeros((H, W), np.float32)
if FORM == "yt" and NAME == "whitebreath":
    y = np.arange(H); shade[:] = (np.clip((y - 760) / 320, 0, 1) * 0.55)[:, None]
    shade[:260, :900] = np.maximum(shade[:260, :900], (np.clip(1 - np.arange(260) / 260, 0, 1) * 0.35)[:, None] * np.clip(1 - np.arange(900) / 900, 0, 1)[None, :] * 1.6)
elif FORM == "ig":
    y = np.arange(H); shade[:] = (np.clip((y - 1520) / 300, 0, 1) * 0.6 + np.clip((300 - y) / 300, 0, 1) * 0.45)[:, None]
shade = np.clip(shade, 0, 0.75)[..., None]

src = frames_wb() if NAME == "whitebreath" else frames_video()
proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                         "-ss", str(T0), "-t", str(LEN), "-i", S["audio"], "-map", "0:v", "-map", "1:a",
                         "-af", f"afade=t=in:d={0.5 if FORM == 'ig' else 0.01},afade=t=out:st={LEN - 1.5:.2f}:d=1.5" if FORM == "ig" else "anull",
                         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k",
                         "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
static = Image.new("RGBA", (W, H), (0, 0, 0, 0))
for im, x, y in INFO: static.alpha_composite(im, (max(0, x), max(0, y)))
for i, img in enumerate(src):
    t = T0 + i / FPS
    b = base(img)[..., ::-1].astype(np.float32)
    b = (b * (1 - shade)).astype(np.uint8)
    fr = Image.fromarray(b).convert("RGBA")
    fr.alpha_composite(static)
    ca = card_alpha(t)
    if ca > 0:
        for im, x, y in CARD:
            a = im.copy(); a.putalpha(a.getchannel("A").point(lambda v: int(v * ca))); fr.alpha_composite(a, (x, y))
    for im, x, y, a in lyric_layers(t):
        if a < 1: im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v, a=a: int(v * a)))
        fr.alpha_composite(im, (max(0, x), max(0, y)))
    if FORM == "ig":                                # 頭と終わりを、やわらかく暗転
        k = min(1, (i / FPS) / 0.5, (LEN - i / FPS) / 1.2)
        if k < 1: fr = Image.eval(fr, lambda v, k=k: int(v * k))
    proc.stdin.write(fr.convert("RGB").tobytes())
proc.stdin.close(); proc.wait()
print("できた", OUT, f"{LEN:.1f}秒")
