"""『白い息のリテイク』の映像を「層」に分けて作る（2026-11-11 人間「動画色々細かく調整してスムーズにして。
背景も、雪も、他のエフェクト、口の動きも」）。
  これまでは元の動画のコマをまるごと並べていたので、口を歌詞に合わせるために速さを変えたり別のコマへ移ったりすると、
  背景の雪・白い息まで一緒に速くなったり、重なったりしていた。ここでは絵を 4 つの層に分ける:
    1. 背景 … 人物も雪もない 1 枚の絵（全コマの中央値。まったく動かないので、ゆれ・ちらつきが出ない）
    2. 雪 … 自分で降らせる（奥・中・手前の 3 層。いつも同じ速さで下へ降り続け、曲の最後までつながる）
    3. 人物 … 元の動画のテト（切り抜き）。口を合わせるための速さの変化・つなぎは、人物だけにかかる
    4. 白い息 … 歌いだし・のばす音・歌い終わりに、口もとから出して、ふわっと上へ流して消す
  雪・白い息は 1280×720 の絵の上に、時間（秒）から直接描く（コマの番号に左右されない）。
"""
import numpy as np, cv2

W, H = 1280, 720

class Snow:
    """雪。t 秒の絵を、いつ呼んでも同じに描ける（位置は時間の式で決まる）"""
    #        数   半径(px)      落ちる速さ(px/秒)  濃さ          ぼかし  横ゆれ(px)
    LAYERS = {"far": (230, (0.7, 1.5), (26, 44), (0.35, 0.75), 0.7, 5),
              "mid": (90, (1.6, 2.9), (50, 78), (0.55, 0.9), 1.1, 9),
              "near": (16, (4.5, 8.5), (95, 140), (0.22, 0.4), 3.2, 16)}
    def __init__(self, seed=20261111):
        r = np.random.default_rng(seed); self.p = {}
        for name, (n, rad, spd, alp, blur, sway) in self.LAYERS.items():
            self.p[name] = dict(x=r.uniform(-40, W + 40, n), y=r.uniform(0, H + 60, n), r=r.uniform(*rad, n), v=r.uniform(*spd, n),
                                a=r.uniform(*alp, n), ph=r.uniform(0, 6.28, n), fq=r.uniform(0.25, 0.6, n), sw=r.uniform(0.4, 1.0, n) * sway, blur=blur)
    @staticmethod
    def wind(t):                                       # ゆっくり向きが変わる弱い風（横へ流れた量 px）
        return 22 * np.sin(0.071 * t) + 9 * np.sin(0.19 * t + 1.3)
    def layer(self, name, t):
        """その層の雪の濃さ（0〜1、H×W）"""
        p = self.p[name]; depth = {"far": 0.5, "mid": 0.8, "near": 1.3}[name]
        x = (p["x"] + p["sw"] * np.sin(p["fq"] * t + p["ph"]) + depth * self.wind(t) + 40) % (W + 80) - 40
        y = (p["y"] + p["v"] * t) % (H + 60) - 30
        img = np.zeros((H, W), np.uint8); SH = 4; k = 1 << SH
        for i in range(len(x)):
            cv2.circle(img, (int(round(x[i] * k)), int(round(y[i] * k))), int(round(p["r"][i] * k)), int(255 * p["a"][i]), -1, cv2.LINE_AA, SH)
        return cv2.GaussianBlur(img, (0, 0), p["blur"]).astype(np.float32) / 255.0

class Breath:
    """白い息。口もとから小さな雲のつぶを出し、広がりながら上へ流して消す"""
    LIFE = 2.3
    def __init__(self, events, seed=7):
        """events: [(出す時刻 秒, 強さ 0〜1)]"""
        r = np.random.default_rng(seed); self.b = []
        for t0, s in events:
            side = -1 if r.random() < 0.65 else 1      # 顔にかぶらないよう、横（左が多め）へ流す
            for _ in range(5):                         # 1 回の息 = 少しずつずれた 5 つのかたまり
                self.b.append((t0 + r.uniform(0, 0.18), s * r.uniform(0.6, 1.0), r.uniform(-5, 5), r.uniform(-3, 3),
                               side * r.uniform(34, 62), r.uniform(-20, -7), r.uniform(0.8, 1.2)))
        self.b.sort()
    def draw(self, t, mouth_at):
        """t 秒の白い息の濃さ（0〜1、H×W）。mouth_at(時刻) → その時刻の口の位置 (x, y)"""
        out = np.zeros((H, W), np.float32)
        for t0, s, ox, oy, vx, vy, g in self.b:
            age = t - t0
            if age < 0: break
            if age > self.LIFE: continue
            u = age / self.LIFE
            mx, my = mouth_at(t0)
            ease = 1 - np.exp(-2.2 * age)              # はじめは速く、だんだんゆっくり
            cx = mx + ox + vx * ease * 1.9 + 0.35 * (Snow.wind(t) - Snow.wind(t0)); cy = my + 12 + oy + vy * ease * 1.9
            rad = (6 + 40 * (1 - np.exp(-1.5 * age))) * g
            a = 0.17 * s * min(1, age / 0.15) * (1 - u) ** 1.5
            x0, x1 = int(max(0, cx - 3 * rad)), int(min(W, cx + 3 * rad)); y0, y1 = int(max(0, cy - 3 * rad)), int(min(H, cy + 3 * rad))
            if x1 <= x0 or y1 <= y0: continue
            yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
            out[y0:y1, x0:x1] += a * np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * (rad * 0.62) ** 2))
        return np.clip(out, 0, 0.4)

def breath_events(sing, fps):
    """歌っているコマ（True/False の列）から、白い息を出す時刻を決める:
    歌いだし（小さめ）・1.2 秒より長くのびる所は 0.7 秒おき（弱め）・歌い終わり（いちばん大きい。吐ききる息）"""
    ev = []; n = len(sing); i = 0
    while i < n:
        if sing[i]:
            j = i
            while j < n and sing[j]: j += 1
            t0, t1 = i / fps, j / fps
            ev.append((t0 + 0.05, 0.55))
            t = t0 + 0.9
            while t < t1 - 0.4: ev.append((t, 0.4)); t += 0.7
            ev.append((t1 - 0.05, 1.0))
            i = j
        else: i += 1
    return ev

def screen(img, layer, col=(255, 255, 255)):
    """白（または col）を、濃さ layer で上にのせる（img は float32 の BGR）"""
    c = np.array(col, np.float32)
    return img + (c - img) * layer[..., None]
