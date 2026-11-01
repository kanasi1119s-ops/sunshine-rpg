# 「銀の笛と百の夜」全100曲の動画（src.png・鐘のある崖の上で笛を吹く少女と、雲の海に浮かぶ島々の絵）
# 2026-11-02 人間「笛の音色が画面上に音符で流れるだけで」: 動きは、笛の先から音符が出て、光の流れにそって右へ流れていくことだけ。
#   ほかの部分（空・雲・滝・人物）は動かさない。すべての音符の周期を 20秒にして、つなぎ目のない20秒ループ（1920x1080・30fps・600フレーム）にする。
#   音符の作り方は、ケルト異世界ファンタジーの動画（2026-10-20 人間「アウトラインはいらない」「もっと幻想的に」）と同じ：
#   やわらかい白い芯＋色のついた光のにじみ＋きらきらの尾。色は金・桃・すみれ（この絵では水色の光の流れの上でも見えるよう、金と桃を多めに）。
# 試し（2026-11-02）: 金・桃・すみれのままだと、明るい桃色の空に溶けて見えにくかった → 色を濃く、芯をはっきり。流れる向きも、光の流れにそって右下へ出てから少し昇るように。
# 使い方: python3 anim.py <出力.mp4>  /  python3 anim.py --frame <秒> <出力.png>
import sys, os, math, subprocess
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS, T = 1920, 1080, 30, 20.0
NF = int(FPS * T)
img0 = cv2.imread(os.path.join(HERE, "src.png"))[:, :, ::-1].astype(np.float32) / 255.0
h0, w0 = img0.shape[:2]
S = max(H / h0, W / w0)
W1, H1 = int(round(w0 * S)), int(round(h0 * S)); OX, OY = (W1 - W) // 2, (H1 - H) // 2
big = cv2.resize(img0, (W1, H1), interpolation=cv2.INTER_LANCZOS4)
bl = cv2.GaussianBlur(big, (0, 0), 1.2)
base = np.clip(big + 0.3 * (big - bl), 0, 1)[OY:OY + H, OX:OX + W]
def P(x, y): return (x * S - OX, y * S - OY)
rng = np.random.default_rng(7)

def add_sprite(acc, spr, cx, cy, gain=1.0):
    h, w = spr.shape[:2]; x0, y0 = int(round(cx - w / 2)), int(round(cy - h / 2))
    xa, ya = max(0, x0), max(0, y0); xb, yb = min(W, x0 + w), min(H, y0 + h)
    if xa >= xb or ya >= yb: return
    acc[ya:yb, xa:xb] += gain * spr[ya - y0:yb - y0, xa - x0:xb - x0]

TIP = P(628, 290)                                    # 笛の先
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
NOTE_COLORS = [np.array([1.0, 0.72, 0.18], np.float32), np.array([1.0, 0.42, 0.72], np.float32), np.array([0.45, 0.85, 1.0], np.float32)]   # 金・桃・水色（明るい桃色の空でも見えるよう、色を濃く）
def note_sprite(ch, size, col):
    pad = size; im = Image.new("L", (size * 2 + pad, size * 2 + pad), 0)
    ImageDraw.Draw(im).text((pad // 2 + size // 4, pad // 2), ch, font=ImageFont.truetype(FONT, int(size * 1.5)), fill=255)
    a = np.asarray(im.filter(ImageFilter.GaussianBlur(0.9)), np.float32) / 255.0
    g1 = np.asarray(im.filter(ImageFilter.GaussianBlur(size * 0.12)), np.float32) / 255.0
    g2 = np.asarray(im.filter(ImageFilter.GaussianBlur(size * 0.35)), np.float32) / 255.0
    core = np.clip(a, 0, 1)
    halo = np.clip(g1 * 2.2 + g2 * 1.8, 0, 1) * 0.85
    alpha = np.clip(np.maximum(core, halo), 0, 1)
    rgb = core[..., None] * np.array([1.0, 0.99, 0.95], np.float32) * 0.35 + (1 - core[..., None] * 0.35) * col * 0.92
    glow = (g2 * 0.8)[..., None] * col
    return rgb.astype(np.float32), alpha.astype(np.float32), glow.astype(np.float32)
GLYPHS = ["♪", "♫", "♩", "♬"]
NOTE_SPR = {(g, s, c): note_sprite(g, s, NOTE_COLORS[c]) for g in GLYPHS for s in (40, 50, 60) for c in range(3)}
_sg = np.mgrid[0:25, 0:25] - 12; _sd = (_sg ** 2).sum(0).astype(np.float32)
SPARK_SPR = (np.exp(-_sd / (2 * 1.3 ** 2)) + 0.3 * np.exp(-_sd / (2 * 4.0 ** 2)))[..., None]
NOTES = []
for k in range(28):                                   # 20秒に28個。笛の先から右へ、光の流れにそってゆれながら流れる
    NOTES.append(dict(t0=k * (T / 28) + rng.uniform(-0.15, 0.15), life=rng.uniform(5.0, 6.5), g=GLYPHS[k % 4], s=int(rng.choice([40, 50, 60])),
                      vx=rng.uniform(95, 150), vy=rng.uniform(4, 34), sw=rng.uniform(14, 30), sf=rng.uniform(0.25, 0.45), ph=rng.random(),
                      c=(0, 1, 0, 2, 1, 0)[k % 6]))
def notes_layer(out, acc, t):
    gx, gy = TIP
    for nt in NOTES:
        age = (t - nt["t0"]) % T
        if age > nt["life"]: continue
        u = age / nt["life"]
        def pos(a_):
            x = gx + 10 + nt["vx"] * a_ + 0.0 * a_ * a_
            y = gy - 6 + nt["vy"] * a_ - 3.2 * a_ * a_ + nt["sw"] * math.sin(2 * math.pi * (nt["sf"] * a_ + nt["ph"]))
            return x, y
        x, y = pos(age)
        a = min(1.0, u / 0.1) * (1 - max(0.0, (u - 0.62) / 0.38)) ** 1.5
        sc_in = 0.55 + 0.45 * min(1.0, u / 0.15)                 # 笛の先では小さく、出てすぐ大きく
        tw = 0.82 + 0.18 * math.sin(2 * math.pi * (1.6 * age + nt["ph"]))
        rgb, al, gl = NOTE_SPR[(nt["g"], nt["s"], nt["c"])]
        if sc_in < 0.999:
            hh, ww = al.shape; nh, nw = max(4, int(hh * sc_in)), max(4, int(ww * sc_in))
            rgb = cv2.resize(rgb, (nw, nh)); al = cv2.resize(al, (nw, nh)); gl = cv2.resize(gl, (nw, nh))
        h, w = al.shape; x0, y0 = int(round(x - w / 2)), int(round(y - h / 2))
        xa, ya, xb, yb = max(0, x0), max(0, y0), min(W, x0 + w), min(H, y0 + h)
        if xa < xb and ya < yb:
            sl = (slice(ya - y0, yb - y0), slice(xa - x0, xb - x0)); A_ = (al[sl] * a * 1.0 * tw)[..., None]
            out[ya:yb, xa:xb] = out[ya:yb, xa:xb] * (1 - A_) + rgb[sl] * A_
            acc[ya:yb, xa:xb] += gl[sl] * a * tw * 0.7
        for j in range(1, 6):                                      # きらきらの尾
            ag = age - 0.14 * j
            if ag < 0: break
            px, py = pos(ag); px -= 6; py += 8 * math.sin(7.0 * j + nt["ph"] * 6)
            add_sprite(acc, SPARK_SPR * NOTE_COLORS[nt["c"]], px, py, a * 0.5 * (1 - j / 6) * (0.6 + 0.4 * math.sin(9 * ag + j)))

def frame(t):
    out = base.copy(); acc = np.zeros_like(out)
    notes_layer(out, acc, t)
    out = 1 - (1 - out) * (1 - np.clip(acc, 0, 1))              # 光は「スクリーン」で重ねる
    return (np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)

if __name__ == "__main__":
    if sys.argv[1] == "--frame":
        Image.fromarray(frame(float(sys.argv[2]))).save(sys.argv[3]); sys.exit()
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-g", str(NF), sys.argv[1]], stdin=subprocess.PIPE)
    for i in range(NF):
        p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
