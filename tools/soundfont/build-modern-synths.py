# 使い方: python3 tools/soundfont/build-modern-synths.py [作業フォルダ] [--only 名前の正規表現]
# 現代的なシンセの音（ボカロ曲・J-POP・フューチャーベース向け。2026-10-25 人間「電子音をもっと現代的に。ボカロっぽいシンセじゃない。シンセの音も勉強してきて」）を、
# このプログラム自身で合成する（外部の録音は使わない。作者の著作物として CC0 扱いにできる）。作り方の数値は docs/sound/modern-synth-study.md。
#   ・ステレオ（左右で別の位相・別のデチューンのユニゾン）。伸ばす音はループ（全オシレーターの周期の数を整数にそろえ、つなぎ目でプチッと鳴らさない）
#   ・フィルターの動き・音量の動き（アタック・ディケイ）はループの前の部分に焼き込み、ループの部分は止まった音にする
#   1) 音ごとの WAV（32bit 浮動小数・44.1kHz・ステレオ）と SFZ を作業フォルダに書く
#   2) tools/soundfont/sfz-to-sf3.mjs（--stereo）で SF3 にして assets-src/soundfont/extra/ に置く
import sys, os, re, math, subprocess
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt, lfilter

SR = 44100
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
args = sys.argv[1:]
WORK = os.path.abspath(args[0]) if args and not args[0].startswith("--") else "/tmp/modern-synths"
ONLY = re.compile(args[args.index("--only") + 1]) if "--only" in args else None
os.makedirs(WORK, exist_ok=True)


def hz(k): return 440.0 * 2 ** ((k - 69) / 12)


def cents(c): return 2 ** (c / 1200)


def blep(p, dt):
    """polyBLEP の補正（p: 位相 0〜1、dt: 1サンプルの位相の進み）"""
    y = np.zeros_like(p)
    a = p < dt; t = p[a] / dt; y[a] = t + t - t * t - 1
    b = p > 1 - dt; t = (p[b] - 1) / dt; y[b] = t * t + t + t + 1
    return y


def osc(kind, cyc, L, n, ph0=0.0, pw=0.5):
    """ループ全長 L の間にちょうど cyc 周期入る波（n サンプル）"""
    inc = cyc / L
    p = (ph0 + inc * np.arange(n)) % 1.0
    if kind == "saw": return 2 * p - 1 - blep(p, inc)
    if kind == "sq": return np.where(p < pw, 1.0, -1.0) + blep(p, inc) - blep((p - pw) % 1.0, inc)
    if kind == "tri": return 4 * np.abs(p - 0.5) - 1
    if kind == "sin": return np.sin(2 * np.pi * p)
    raise ValueError(kind)


def svf_lp(x, fc, q=0.707):
    """時間で変わるカットオフの 2 次ローパス（TPT 型の状態変数フィルタ。高いカットオフでも安定。fc は配列）"""
    y = np.zeros_like(x); ic1 = ic2 = 0.0; k = 1.0 / q
    g = np.tan(np.pi * np.clip(fc, 20, SR * 0.45) / SR)
    a1 = 1 / (1 + g * (g + k)); a2 = g * a1; a3 = g * a2
    for i in range(len(x)):
        v3 = x[i] - ic2
        v1 = a1[i] * ic1 + a2[i] * v3
        v2 = ic2 + a2[i] * ic1 + a3[i] * v3
        ic1 = 2 * v1 - ic1; ic2 = 2 * v2 - ic2
        y[i] = v2
    return y


def lp(x, fc, order=2):
    return sosfilt(butter(order, fc, "low", fs=SR, output="sos"), x)


def hp(x, fc, order=2):
    return sosfilt(butter(order, fc, "high", fs=SR, output="sos"), x)


def peak(x, f0, gain_db, q):
    A = 10 ** (gain_db / 40); w = 2 * np.pi * f0 / SR; al = np.sin(w) / (2 * q)
    b = [1 + al * A, -2 * np.cos(w), 1 - al * A]; a = [1 + al / A, -2 * np.cos(w), 1 - al / A]
    return lfilter(np.array(b) / a[0], np.array(a) / a[0], x)


def sat(x, drive=1.5):
    return np.tanh(drive * x) / np.tanh(drive)


def env_adr(n, a, d, s, curve=4.0):
    """アタック a 秒・ディケイ d 秒でサステイン s へ（指数）"""
    t = np.arange(n) / SR
    e = np.where(t < a, (t / max(a, 1e-4)) ** 0.7, s + (1 - s) * np.exp(-(t - a) / max(d, 1e-4) * curve / 4))
    return e


def unison(kind, f0, L, n, voices, detune, spread, rnd, pw=0.5, side_db=-3.0):
    """ユニゾン（voices 本を ±detune セントに広げ、spread で左右に振る）。戻り値 (左, 右)"""
    Lc = np.zeros(n); Rc = np.zeros(n)
    for v in range(voices):
        pos = 0.0 if voices == 1 else (v / (voices - 1)) * 2 - 1           # -1〜1
        dc = detune * (pos ** 3 * 0.6 + pos * 0.4)                            # 外側ほど大きくずらす（直線でない）
        cyc = max(1, round(f0 * cents(dc) * L / SR))
        g = 1.0 if abs(pos) < 0.2 else 10 ** (side_db / 20)
        x = osc(kind, cyc, L, n, rnd.random(), pw) * g
        pan = pos * spread
        Lc += x * math.cos((pan + 1) * math.pi / 4); Rc += x * math.sin((pan + 1) * math.pi / 4)
    return Lc / math.sqrt(voices), Rc / math.sqrt(voices)


# ---------------- 音色 ----------------
# keys: 鳴らす音（step 半音ごとにサンプル）、loop: ループの長さ（フレーム）、pre: ループの前（秒）、total: ループしない音の長さ（秒）
INSTR = {}


def instr(name, **kw):
    def deco(fn): INSTR[name] = dict(kw, render=fn); return fn
    return deco


@instr("synth-modern-lead", program=1, keys=(48, 96), step=3, loop=88200, pre=1.2, release=0.18, level=0.75)
def _(f0, L, n, rnd):
    """歌の役の現代的なリード（Syntorial のリードのレシピを元に）: ソー 6 本（±12 セント・広がり 0.4）＋1オクターブ下のソー（−12dB）、
    チューブ風の歪み（tanh 2.5 倍）→ ローパス 24dB（1オクターブ上から 0.3 秒で 5.5kHz 付近へ）、2.5kHz の明るさ、350Hz のこもりを引く"""
    l1, r1 = unison("saw", f0, L, n, 6, 12, 0.4, rnd, side_db=-3)
    sub = osc("saw", max(1, round(f0 / 2 * L / SR)), L, n, rnd.random()) * 0.25
    t = np.arange(n) / SR
    fc = (5500 + 6000 * np.exp(-t / 0.1)) * np.clip(f0 / 440, 0.75, 1.35)
    out = []
    for x in (l1 + sub, r1 + sub):
        y = sat(x * 0.8, 2.5)
        y = svf_lp(svf_lp(y, fc, 0.6), fc, 0.6)
        y = peak(y, 2500, 2.0, 0.9); y = peak(y, 350, -2.5, 0.8)
        out.append(hp(y, 120))
    e = env_adr(n, 0.006, 0.25, 0.85)
    return out[0] * e, out[1] * e


@instr("synth-modern-supersaw", program=5, keys=(36, 96), step=3, loop=88200, pre=1.2, release=0.35, level=0.7)
def _(f0, L, n, rnd):
    """サビの和音の壁: ソー 9 本（±28 セント・外側ほど大きく）、左右いっぱい、中央以外は −3dB、ハイパス 150Hz、
    ローパス 11kHz、2kHz を少し上げ、350Hz のこもりを引く"""
    l, r = unison("saw", f0, L, n, 9, 28, 1.0, rnd, side_db=-3)
    l2, r2 = unison("saw", f0 / 2, L, n, 3, 10, 0.5, rnd)                 # 1オクターブ下の層（3本）
    out = []
    for x in (l + l2 * 0.35, r + r2 * 0.35):
        y = lp(x, 11000); y = hp(y, max(150, f0 * 0.9), 2)
        y = peak(y, 350, -3, 0.8); y = peak(y, 2000, 1.5, 0.8)
        out.append(sat(y, 1.2))
    e = env_adr(n, 0.008, 0.3, 0.95)
    return out[0] * e, out[1] * e


@instr("synth-modern-fbchord", program=10, keys=(36, 96), step=3, loop=88200, pre=1.3, release=0.3, level=0.7)
def _(f0, L, n, rnd):
    """フューチャーベースの和音: ソー 7 本（±20）＋矩形 2 本（±10・1オクターブ上を小さく）、ローパスが開いていく（0.25 秒）、
    明るい 3〜5kHz、左右に広い。うねり（音量のサイドチェイン）は曲のパートの duck で付ける"""
    l1, r1 = unison("saw", f0, L, n, 8, 12, 1.0, rnd, side_db=-2.0)
    l2, r2 = unison("sq", f0 * 2, L, n, 2, 8, 0.6, rnd)
    t = np.arange(n) / SR
    fc = 2500 + 6000 * (1 - np.exp(-t / 0.25))
    out = []
    for x in (l1 + l2 * 0.25, r1 + r2 * 0.25):
        y = svf_lp(x, fc, 0.9); y = hp(y, 220)
        y = peak(y, 4000, 2.5, 0.9); y = peak(y, 400, -2.5, 0.8)
        out.append(sat(y, 1.3))
    e = env_adr(n, 0.01, 0.4, 0.92)
    return out[0] * e, out[1] * e


@instr("synth-modern-pluck", program=23, keys=(48, 108), step=3, total=1.6, release=0.2, level=0.7)
def _(f0, L, n, rnd):
    """現代的なプラック: ソー 3 本（±9）＋矩形 1 本、ピッチが鳴り始めに +4 半音から 20ms で戻る、
    ローパスが 10kHz から 0.12 秒で 900Hz へ閉じる、音量は 0.35 秒で減衰"""
    t = np.arange(n) / SR
    pitch = 1 + (cents(1200) - 1) * np.exp(-t / 0.012)
    ph = np.cumsum(f0 * pitch / SR)
    out = []
    for side in (0, 1):
        x = np.zeros(n)
        for d in (-9, 0, 9):
            p = (ph * cents(d + (3 if side else -3)) + rnd.random()) % 1
            x += 2 * p - 1 - blep(p, f0 / SR)
        p = (ph + rnd.random()) % 1
        x += (np.where(p < 0.5, 1, -1)) * 0.4
        fc = 900 + 9000 * np.exp(-t / 0.12)
        y = svf_lp(x / 3, fc, 1.1)
        out.append(hp(y, 150))
    e = np.exp(-t / 0.35) * np.minimum(1, t / 0.002)
    return out[0] * e, out[1] * e


@instr("synth-modern-bell", program=31, keys=(48, 108), step=3, total=2.6, release=0.6, level=0.65)
def _(f0, L, n, rnd):
    """ポップなベル（FM）: 搬送波サイン＋変調 3.5 倍（深さが 0.4 秒で減る）＋ 1オクターブ上の FM（変調 1.41 倍）を薄く。
    左右で少しずらす"""
    t = np.arange(n) / SR
    out = []
    for side in (0, 1):
        dt = 1 + (0.0015 if side else -0.0015)
        I1 = 2.2 * np.exp(-t / 0.4) + 0.3
        m1 = np.sin(2 * np.pi * f0 * 3.5 * dt * t)
        c1 = np.sin(2 * np.pi * f0 * dt * t + I1 * m1)
        I2 = 1.4 * np.exp(-t / 0.25)
        c2 = np.sin(2 * np.pi * f0 * 2 * dt * t + I2 * np.sin(2 * np.pi * f0 * 2 * 1.41 * t))
        x = c1 * np.exp(-t / 0.9) + c2 * 0.35 * np.exp(-t / 0.5)
        out.append(hp(x, 200))
    a = np.minimum(1, t / 0.001)
    return out[0] * a, out[1] * a


@instr("synth-modern-bass", program=44, keys=(24, 72), step=3, loop=88200, pre=1.2, release=0.12, level=0.8)
def _(f0, L, n, rnd):
    """現代的なシンセベース: ソー 2 本（±8）＋サブのサイン、ローパスが 3kHz から 0.15 秒で 1.1kHz へ、歪み、
    800Hz・2kHz を上げてゴリッと（人間「ベースは明るくゴリッと」）。モノラル（左右同じ）"""
    c0 = max(2, round(f0 * L / SR))
    x = osc("saw", max(1, round(f0 * cents(-8) * L / SR)), L, n, rnd.random()) * 0.5 + osc("saw", max(1, round(f0 * cents(8) * L / SR)), L, n, rnd.random()) * 0.5
    sub = osc("sin", c0, L, n, 0) * 0.7
    t = np.arange(n) / SR
    fc = 1100 + 1900 * np.exp(-t / 0.15)
    y = svf_lp(x, fc, 1.0)
    y = sat(y * 1.2, 2.0) + sub
    y = peak(y, 800, 3, 0.9); y = peak(y, 2000, 2, 1.0); y = hp(y, 30)
    e = env_adr(n, 0.003, 0.2, 0.9)
    return y * e, y * e


@instr("synth-modern-chop", program=69, keys=(48, 96), step=3, total=0.9, release=0.08, level=0.6)
def _(f0, L, n, rnd):
    """ボーカルチョップ風（声ではない。声の響きの山を持つシンセ）: パルス列（ソー＋矩形）を、母音「あ」の響きの山
    （800・1150・2900・3900Hz）の帯域フィルタに通す。短く切れる（0.18 秒で減衰）。ピッチの頭にわずかなしゃくり"""
    t = np.arange(n) / SR
    pitch = 1 - (1 - cents(-60)) * np.exp(-t / 0.03)
    ph = np.cumsum(f0 * pitch / SR)
    out = []
    for side in (0, 1):
        p = (ph + 0.1 * side) % 1
        src = (2 * p - 1 - blep(p, f0 / SR)) * 0.8 + np.where(p < 0.3, 1, -1) * 0.2 + rnd.r.standard_normal(n) * 0.06   # 息のノイズ
        y = np.zeros(n)
        for f, g, q in ((850, 1.0, 850 / 80), (1220, 0.55, 1220 / 100), (2810, 0.2, 2810 / 150), (3900, 0.08, 3900 / 200)):
            w = 2 * np.pi * f / SR; al = np.sin(w) / (2 * q)
            b = [al, 0, -al]; a = [1 + al, -2 * np.cos(w), 1 - al]
            y += lfilter(np.array(b) / a[0], np.array(a) / a[0], src) * g
        out.append(hp(y, 180))
    e = np.minimum(1, t / 0.006) * np.exp(-np.maximum(0, t - 0.05) / 0.18)
    return out[0] * e, out[1] * e


@instr("synth-modern-pad", program=74, keys=(36, 96), step=3, loop=88200, pre=1.2, release=1.2, level=0.6)
def _(f0, L, n, rnd):
    """現代的な広がるパッド: ソー 7 本（±18）＋ 1オクターブ上の三角、ローパス 3.5kHz、アタック 0.6 秒、左右いっぱい"""
    l1, r1 = unison("saw", f0, L, n, 7, 18, 1.0, rnd, side_db=-2)
    l2, r2 = unison("tri", f0 * 2, L, n, 2, 6, 0.8, rnd)
    out = []
    for x in (l1 + l2 * 0.4, r1 + r2 * 0.4):
        y = lp(x, 2600, 2); y = hp(y, 220); y = peak(y, 300, -3, 0.8)
        out.append(y)
    t = np.arange(n) / SR
    e = np.minimum(1, (t / 0.6) ** 1.5)
    return out[0] * e, out[1] * e


@instr("synth-modern-arp", program=76, keys=(48, 108), step=3, total=0.7, release=0.1, level=0.65)
def _(f0, L, n, rnd):
    """かわいいアルペジオ（Kawaii Future Bass 風）: 矩形 25% と三角を重ね、ローパスが 7kHz から 0.08 秒で 2.5kHz へ、
    0.22 秒で減衰。少し左右に"""
    t = np.arange(n) / SR
    out = []
    for side in (0, 1):
        ph = (f0 * cents(4 if side else -4) * t + rnd.random()) % 1
        x = (np.where(ph < 0.25, 1, -1) + blep(ph, f0 / SR) - blep((ph - 0.25) % 1, f0 / SR)) * 0.6 + (4 * np.abs(ph - 0.5) - 1) * 0.5
        fc = 2500 + 4500 * np.exp(-t / 0.08)
        y = svf_lp(x, fc, 1.0); out.append(hp(y, 200))
    e = np.minimum(1, t / 0.002) * np.exp(-t / 0.22)
    return out[0] * e, out[1] * e


@instr("synth-modern-brightlead", program=112, keys=(48, 96), step=3, loop=88200, pre=1.2, release=0.25, level=0.72)
def _(f0, L, n, rnd):
    """明るく太いリード（サビ・ソロ向け）: ソー 7 本（±22・広がり 0.6）＋1オクターブ上のソー 2 本を小さく。ローパス 9kHz、
    2〜3kHz の明るさ、軽い歪み"""
    l1, r1 = unison("saw", f0, L, n, 7, 22, 0.6, rnd, side_db=-3)
    l2, r2 = unison("saw", f0 * 2, L, n, 2, 9, 0.4, rnd)
    out = []
    for x in (l1 + l2 * 0.3, r1 + r2 * 0.3):
        y = lp(x, 9000, 2); y = hp(y, 150); y = peak(y, 2600, 2.5, 0.8); y = peak(y, 400, -2, 0.8)
        out.append(sat(y, 1.5))
    e = env_adr(n, 0.005, 0.25, 0.9)
    return out[0] * e, out[1] * e


@instr("synth-clear-lead", program=113, keys=(48, 96), step=3, loop=88200, pre=1.2, release=0.2, level=0.72)
def _(f0, L, n, rnd):
    """クリアで揺れの少ないリード（2026-10-25 人間「クリアで揺れの少ないシンセも欲しい」）: デチューンなしの1本。
    三角波＋ソー（小さく）＋サインの1オクターブ上を少し。ローパス 6kHz、歪みなし。ユニゾンのうねりがない、まっすぐな音"""
    c = max(1, round(f0 * L / SR)); c2 = max(1, round(2 * f0 * L / SR))
    x = osc("tri", c, L, n, 0) * 0.8 + osc("saw", c, L, n, 0) * 0.22 + osc("sin", c2, L, n, 0) * 0.12
    y = lp(x, 6000, 2); y = hp(y, 140); y = peak(y, 2500, 1.5, 0.9)
    e = env_adr(n, 0.008, 0.2, 0.9)
    return y * e, y * e


@instr("synth-clear-pad", program=114, keys=(36, 96), step=3, loop=88200, pre=1.2, release=1.0, level=0.62)
def _(f0, L, n, rnd):
    """クリアで揺れの少ない和音の音: ソー2本（±3 セントだけ）を左右に、三角の1オクターブ上。ローパス 4kHz、アタック 0.08 秒。
    スーパーソウのような厚いうねりはない、透き通った和音"""
    l, r = unison("saw", f0, L, n, 2, 3, 0.7, rnd)
    c2 = max(1, round(2 * f0 * L / SR)); t2 = osc("tri", c2, L, n, 0) * 0.35
    out = []
    for x in (l + t2, r + t2):
        y = lp(x, 4000, 2); y = hp(y, 160); y = peak(y, 350, -2.5, 0.8); out.append(y)
    t = np.arange(n) / SR
    e = np.minimum(1, t / 0.08)
    return out[0] * e, out[1] * e


def _voice(f0, L, n, rnd, formants, breath=0.05, bright=3.0):
    """声のように聞こえる伸ばす音（2026-10-25 人間「もっとボカロっぽい感じのが欲しい」）。声ではない。
    声帯の代わりのパルス列（ソー＋細い矩形）を、母音の響きの山（固定の Hz。音程が変わっても山は動かない＝声と同じ）に通す。
    息のノイズはループの長さで繰り返す（つなぎ目が切れない）。2.8〜3.2kHz の歌の明るさを足す"""
    c = max(1, round(f0 * L / SR))
    out = []
    for side in (0, 1):
        ph = rnd.random()
        src = osc("saw", c, L, n, ph) * 0.75 + osc("sq", c, L, n, ph, 0.12) * 0.25
        nb = np.random.default_rng(int(f0 * 10) + side).standard_normal(L)
        src = src + np.resize(nb, n) * breath
        y = np.zeros(n)
        for f, g, bw in formants:
            q = f / bw; w = 2 * np.pi * f / SR; al = np.sin(w) / (2 * q)
            b = [al, 0, -al]; a = [1 + al, -2 * np.cos(w), 1 - al]
            y += lfilter(np.array(b) / a[0], np.array(a) / a[0], src) * g
        y = peak(y, 3000, bright, 1.2)
        y = y + src * 0.04                       # ほんの少し元の音（芯）
        out.append(hp(lp(y, 9000), 150))
    e = env_adr(n, 0.02, 0.15, 0.9)
    return out[0] * e, out[1] * e


@instr("synth-voice-lead-a", program=54, keys=(48, 96), step=3, loop=88200, pre=1.2, release=0.15, level=0.75)
def _(f0, L, n, rnd):
    """歌の役（ボカロらしい声のようなリード・母音「あ」）: 女性の「あ」850/1220/2810/3900Hz"""
    return _voice(f0, L, n, rnd, ((850, 1.0, 90), (1220, 0.7, 110), (2810, 0.32, 170), (3900, 0.16, 250)))


@instr("synth-voice-lead-u", program=91, keys=(48, 96), step=3, loop=88200, pre=1.2, release=0.15, level=0.75)
def _(f0, L, n, rnd):
    """歌の役（やわらかい声のようなリード・母音「う」寄り）: 日本語の「う」400/1400/2700Hz（唇を丸めない）"""
    return _voice(f0, L, n, rnd, ((420, 1.0, 70), (1400, 0.45, 110), (2700, 0.25, 170), (3800, 0.1, 250)), breath=0.07, bright=2.0)


# ---------------- 書き出し ----------------
class R:
    def __init__(self, seed): self.r = np.random.default_rng(seed)
    def random(self): return float(self.r.random())


done = []
for name, d in INSTR.items():
    if ONLY and not ONLY.search(name): continue
    dirp = os.path.join(WORK, name); os.makedirs(dirp, exist_ok=True)
    keys = list(range(d["keys"][0], d["keys"][1] + 1, d["step"]))
    lines = []
    loop = d.get("loop")
    for k in keys:
        f0 = hz(k)
        if loop:
            L = loop; pre = int(d["pre"] * SR)
            # ループの中で全部の周期が整数になる（osc の cyc）。プレの部分も同じ位相で続く
            n = pre + L + 2205
            l, r = d["render"](f0, L, n, R(k * 7919 + len(name)))
            c = round(f0 * L / SR); f_eff = c * SR / L
            tune = round(-1200 * math.log2(f_eff / f0))
        else:
            n = int(d["total"] * SR); L = n; pre = 0
            l, r = d["render"](f0, L, n, R(k * 7919 + len(name))); tune = 0
        x = np.stack([l, r], 1)
        x -= x.mean(0) if not loop else 0
        pk = np.abs(x).max(); assert pk > 1e-6, (name, k)
        x = x / pk * d["level"]
        fade = int(0.003 * SR); x[:fade] *= np.linspace(0, 1, fade)[:, None]
        sf.write(os.path.join(dirp, f"{name}_{k}.wav"), x.astype(np.float32), SR, subtype="FLOAT")
        st = d["step"]
        lo = 0 if k == keys[0] else k - st // 2
        hi = 127 if k == keys[-1] else k + (st - st // 2) - 1
        lines.append(f"<region> sample={name}_{k}.wav pitch_keycenter={k} lokey={lo} hikey={hi} tune={tune}" +
                     (f" loop_mode=loop_continuous loop_start={pre} loop_end={pre + L}" if loop else ""))
    sfz = os.path.join(dirp, f"{name}.sfz"); open(sfz, "w").write("\n".join(lines) + "\n")
    secs = ((pre + L + 2205) / SR + 0.1) if loop else d["total"]
    cmd = ["node", "tools/soundfont/sfz-to-sf3.mjs", sfz, name, "--program", str(d["program"]), "--seconds", f"{secs:.2f}", "--rr", "1", "--q", "5",
           "--release", str(d["release"]), "--fade", "0.05" if loop else "0.2", "--stereo"]
    if loop: cmd.append("--loop")
    o = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    print(name, (o.stdout.strip().splitlines() or [""])[-1], o.stderr.strip()[-300:])
    done.append(name)
print("作った音色:", ", ".join(done))
