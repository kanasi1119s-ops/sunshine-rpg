#!/usr/bin/env python3
"""歌う重音テトの動画（ボカロ25曲）。2026-10-26 人間「この動画を使って今回作った曲の動画を作りましょう。歌に合わせて体を動かしたり、口を動かしたりして」
使い方: python3 teto_mv.py <素材の動画のコマのフォルダ> <追跡の json> <歌だけの wav> <曲の JSON（歌の版。tempo・secs を読む）> <音の mp3> <曲名> <出力 mp4>
しくみ:
  ・体: 素材の動画（10秒）を行って戻ってくり返し（つなぎ目が出ない）。さらに曲の拍に合わせて、足もとを中心に小さくはずむ（サビは大きく、静かな所は小さく）
  ・口: 歌だけの音の大きさから、コマごとに「閉じる・少し開く・開く」を決める。素材のそのコマの口がちがうときは、
        同じ口の形で、顔の向きがいちばん近いコマから口だけを切り出して、顔の位置に合わせて貼る（まわりはぼかしてなじませる）
"""
import sys, json, math, subprocess, numpy as np, cv2, soundfile as sf, importlib.util
from PIL import Image, ImageDraw, ImageFont
FR, TRK, VOC, SONG, AUDIO, TITLE, OUT = sys.argv[1:8]
spec = importlib.util.spec_from_file_location("s", "/home/claude/wt-mix/tools/singer/sing.py"); S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
FPS = 24
trk = json.load(open(TRK)); NSRC = len(trk)
state = [0 if t[4] < 80 else (1 if t[4] < 300 else 2) for t in trk]
conf = [t[3] for t in trk]
MX0, MY0 = 342, 291
def src(k): return cv2.imread(f"{FR}/{k + 1:03d}.png")
# 口の部品の候補（状態ごと。追跡がしっかりしているコマ）
lib = {s: [k for k in range(NSRC) if state[k] == s and conf[k] > 0.7] for s in (0, 1, 2)}
song = json.load(open(SONG))
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", AUDIO], capture_output=True, text=True).stdout)
N = int(dur * FPS)
# 歌の大きさ → 口の状態
v, sr = sf.read(VOC); v = v.mean(1) if v.ndim > 1 else v
hop = sr // FPS
env = np.array([np.sqrt(np.mean(v[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(N)])
db = 20 * np.log10(env + 1e-9); top = np.percentile(db[db > -60], 95) if (db > -60).any() else -20
want = np.where(db < top - 30, 0, np.where(db < top - 14, 1, 2))
# 細かすぎる切りかえをならす（1コマだけの開閉は前後に合わせる）
for i in range(1, N - 1):
    if want[i - 1] == want[i + 1] != want[i]: want[i] = want[i - 1]
# 拍と場面の強さ
b2s = S.tempo_clock(song["bpm"], song.get("tempo"), song.get("beats", 4))
beats = []; b = 0
while True:
    t = b2s(b)
    if t > dur: break
    beats.append(t); b += 1
beats = np.array(beats)
try: secs = json.load(open(SONG + ".secs"))
except Exception: secs = []
KAMP = {"chorus": 1.0, "drop": 1.0, "solo": 0.8, "interlude": 0.7, "pre": 0.6, "build": 0.7, "verse": 0.45, "bridge": 0.35, "intro": 0.4, "outro": 0.3, "break": 0.1}
def amp_at(t):
    a = 0.4
    for s_ in secs:
        if s_["t"] <= t: a = KAMP.get(s_["kind"], 0.5)
    return a
# 文字（曲名）
font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 40, index=0)
font2 = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 26, index=0)
ov = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
for dx_, dy_ in ((-2, 0), (2, 0), (0, -2), (0, 2)):
    d.text((36 + dx_, 1150 + dy_), TITLE, font=font, fill=(255, 255, 255, 255)); d.text((38 + dx_, 1204 + dy_), "歌：重音テト（仮）", font=font2, fill=(255, 255, 255, 255))
d.text((36, 1150), TITLE, font=font, fill=(170, 30, 50, 255)); d.text((38, 1204), "歌：重音テト（仮）", font=font2, fill=(90, 90, 100, 255))
OV = np.asarray(ov).astype(np.float32); OA = OV[..., 3:4] / 255.0; OC = OV[..., [2, 1, 0]]
MASK = np.zeros((1280, 720), np.float32)
proc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "720x1280", "-r", str(FPS), "-i", "-", "-i", AUDIO,
                         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", OUT], stdin=subprocess.PIPE)
cache = {}
for i in range(N):
    t = i / FPS
    p = i % (2 * NSRC - 2); k = p if p < NSRC else 2 * NSRC - 2 - p          # 行って戻る
    if k not in cache:
        if len(cache) > 60: cache.clear()
        cache[k] = src(k)
    img = cache[k].copy()
    _, dx, dy, cf, _ = trk[k]
    w = int(want[i])
    if state[k] != w and lib[w]:
        j = min(lib[w], key=lambda q: abs(trk[q][1] - dx) + abs(trk[q][2] - dy) * 0.5)
        if j not in cache: cache[j] = src(j)
        sj = cache[j]; _, jx, jy, _, _ = trk[j]
        mx, my = MX0 + dx, MY0 + dy; sx, sy = MX0 + jx, MY0 + jy
        # 口のまわりを少し広めに（開いた口を、閉じた口で残さずおおう）
        patch = sj[sy - 32:sy + 32, sx - 42:sx + 42].astype(np.float32)
        m = np.zeros((64, 84), np.float32); cv2.ellipse(m, (42, 33), (31, 21), 0, 0, 360, 1.0, -1); m = cv2.GaussianBlur(m, (0, 0), 2.2)[..., None]
        reg = img[my - 32:my + 32, mx - 42:mx + 42].astype(np.float32)
        if reg.shape == patch.shape:
            img[my - 32:my + 32, mx - 42:mx + 42] = (patch * m + reg * (1 - m)).astype(np.uint8)
    # 拍に合わせてはずむ（拍の直後に少し沈んで戻る）・左右に小さくゆれる
    bi = np.searchsorted(beats, t) - 1
    ph = (t - beats[bi]) / max(1e-3, (beats[bi + 1] - beats[bi]) if bi + 1 < len(beats) else 0.5) if bi >= 0 else 0
    a = amp_at(t)
    pulse = math.exp(-ph * 4.0)
    sc = 1.0 + 0.018 * a * (1 - pulse) - 0.006 * a
    ang = 1.6 * a * math.sin(math.pi * (bi + ph)) if bi >= 0 else 0
    R = cv2.getRotationMatrix2D((360, 1240), ang, sc); R[1, 2] += 10 * a * pulse
    R = np.vstack([R, [0, 0, 1]]); G = np.array([[0.9, 0, 36], [0, 0.9, 4], [0, 0, 1]]) @ R; R = G[:2]   # 0.9倍にして上へ（下に曲名の場所）
    img = cv2.warpAffine(img, R, (720, 1280), flags=cv2.INTER_LINEAR, borderValue=(255, 255, 255))
    img = (OC * OA + img.astype(np.float32) * (1 - OA)).astype(np.uint8)
    proc.stdin.write(img.tobytes())
proc.stdin.close(); proc.wait()
print("ok", OUT, N, "コマ")
