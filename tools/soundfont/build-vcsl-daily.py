# 使い方: python3 tools/soundfont/build-vcsl-daily.py <VCSL のフォルダ> [作業フォルダ]
# かわいい日常の曲の「録音の楽器」（2026-11-11 人間「他にも可愛い日常系の音源ない？あったら追加して」）。
# VCSL（Versilian Community Sample Library・CC0 https://github.com/sgossner/VCSL）の録音から、作曲ソフトの音源（SF3）を作る:
#   ocarina-vcsl（オカリナ）・harmonica-vcsl（ハーモニカ）・tubeglock-vcsl（筒の鉄琴）・wineglass-vcsl（グラスハープ）・balafon-vcsl（木琴の仲間バラフォン）・
#   strumstick-vcsl（ストラムスティック＝小さな3弦の弦楽器。ウクレレのように軽い）・toys-vcsl（おもちゃと小物の音。鍵盤ごとに別の音）
# VCSL のファイル名の音名はオクターブがずれていることがあるので、録音の高さを測って鍵盤を決める。
import os, re, sys, subprocess, glob
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "surge"))
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VC = sys.argv[1]; WORK = sys.argv[2] if len(sys.argv) > 2 else "/tmp/vcslb"
SR = 44100
N = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}


def read(p):
    x, sr = sf.read(p, always_2d=True)
    if x.shape[1] == 1: x = np.repeat(x, 2, 1)
    x = x[:, :2]
    if sr != SR:
        n = int(len(x) * SR / sr); x = np.stack([np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x[:, c]) for c in range(2)], 1)
    return x


def pitch(x, nominal_pc):
    """録音の基音（MIDI 番号）。名前の音名（高さの種類）と合う候補のうち、倍音の並びがいちばん合うオクターブ"""
    m = x.mean(1); on = np.argmax(np.abs(m) > np.abs(m).max() * 0.2); m = m[on + int(0.03 * SR): on + int(0.03 * SR) + int(0.6 * SR)]
    if len(m) < 2048: m = x.mean(1)
    sp = np.abs(np.fft.rfft(m * np.hanning(len(m)))); f = np.fft.rfftfreq(len(m), 1 / SR)
    best = None
    for o in range(1, 8):
        k = 12 * (o + 1) + nominal_pc; f0 = 440 * 2 ** ((k - 69) / 12)
        if f0 > 5000: continue
        s = 0
        for h in range(1, 7):
            i = np.argmin(np.abs(f - f0 * h)); s += sp[max(0, i - 4):i + 5].max() / h
        i = np.argmin(np.abs(f - f0 / 2)); s -= 1.5 * sp[max(0, i - 4):i + 5].max()
        i = np.argmin(np.abs(f - f0)); s += 2 * sp[max(0, i - 4):i + 5].max()
        if best is None or s > best[0]: best = (s, k)
    return best[1]


def trim(x, thr=0.004, pre=0.002):
    a = np.abs(x).max(1); on = np.argmax(a > a.max() * thr); return x[max(0, on - int(pre * SR)):]


def retune_to(x, k):
    """録音の高さが鍵盤の音から外れているとき（グラスハープ・バラフォン）、いちばん強い成分が鍵盤の音（かその倍音）に合うように、録音の速さを少し変える"""
    m = x.mean(1); m = m[int(0.02 * SR):int(0.6 * SR)]
    sp = np.abs(np.fft.rfft(m * np.hanning(len(m)), n=1 << 17)); f = np.fft.rfftfreq(1 << 17, 1 / SR)
    f0 = 440 * 2 ** ((k - 69) / 12); sel = (f > f0 * 0.92) & (f < f0 * 1.09)
    if not sel.any() or sp[sel].max() < sp.max() * 0.2: return x
    fr = f[sel][np.argmax(sp[sel])]; r = fr / f0
    if abs(r - 1) < 0.002: return x
    n = int(len(x) * r); t = np.linspace(0, len(x) - 1, n)
    return np.stack([np.interp(t, np.arange(len(x)), x[:, c]) for c in range(2)], 1)


def build(name, program, files, note_re, loop=False, release="0.5", maxsec=7.0, gain=0.8, fade_in=0.0, octave=None, retune=False):
    """note_re: ファイル名から (音名, オクターブ) を取る正規表現。鍵盤は「名前の音 ＋ オクターブのずれ」。
    オクターブのずれは、録音の高さを測って全体でいちばん多い値に決める（1つずつ測ると、鐘のような倍音の並ばない音でまちがえる）"""
    d = os.path.join(WORK, name); os.makedirs(d, exist_ok=True); tmp = []
    for p in files:
        mm = re.search(note_re, os.path.basename(p))
        if not mm: continue
        pc = N[mm.group(1)[0]] + (1 if "#" in mm.group(1) else 0); nom = 12 * (int(mm.group(2)) + 1) + pc
        x = trim(read(p)); tmp.append((nom, pitch(x, pc), x))
    if not tmp: print(name, "ファイルが見つかりません"); return
    off = 12 * octave if octave is not None else 12 * int(round(float(np.median([(m - n) / 12 for n, m, _ in tmp]))))
    regs = []
    for nom, _, x in tmp:
        k = nom + off
        if retune: x = retune_to(x, k)
        x = x[:int(maxsec * SR)].copy(); x = x / (np.abs(x).max() + 1e-9) * gain
        if fade_in: n = int(fade_in * SR); x[:n] *= np.linspace(0, 1, n)[:, None]
        n = int(0.03 * SR); x[-n:] *= np.linspace(1, 0, n)[:, None]
        regs.append((k, x))
    regs.sort(key=lambda r: r[0]); uniq = []
    for k, x in regs:
        if uniq and uniq[-1][0] == k: continue
        uniq.append((k, x))
    lines = []; longest = 0
    for i, (k, x) in enumerate(uniq):
        fn = f"{name}_{k}.wav"; extra = ""
        if loop and len(x) > 2.2 * SR:
            from sample import find_loop, crossfade_loop
            ls, le, c = find_loop(x, int(0.8 * SR), min(len(x) - 2205, int(4.5 * SR)), int(0.5 * SR))
            x = crossfade_loop(x, ls, le, int(0.08 * SR)); x = x[:le + 2205]; extra = f" loop_mode=loop_continuous loop_start={ls} loop_end={le}"
        sf.write(os.path.join(d, fn), x.astype(np.float32), SR, subtype="FLOAT"); longest = max(longest, len(x) / SR)
        lo = 0 if i == 0 else (uniq[i - 1][0] + k) // 2 + 1
        hi = 127 if i == len(uniq) - 1 else (k + uniq[i + 1][0]) // 2
        lines.append(f"<region> sample={fn} pitch_keycenter={k} lokey={lo} hikey={hi}{extra}")
    open(os.path.join(d, f"{name}.sfz"), "w").write("\n".join(lines) + "\n")
    cmd = ["node", "tools/soundfont/sfz-to-sf3.mjs", os.path.join(d, f"{name}.sfz"), name, "--program", str(program), "--seconds", f"{longest + 0.2:.2f}", "--rr", "1", "--q", "6",
           "--release", release, "--fade", "0.05", "--stereo"] + (["--loop"] if loop else [])
    o = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    print(name, "鍵盤", [k for k, _ in uniq][:3], "…", [k for k, _ in uniq][-2:], (o.stdout.strip().splitlines() or [""])[-1][-110:], o.stderr[-200:])


G = lambda pat: sorted(glob.glob(os.path.join(VC, pat), recursive=True))
build("ocarina-vcsl", 217, G("Aerophones/Edge-blown Aerophones/Ocarina, Typical/Sustains/**/*.wav"), r"_([A-G]#?)(\d)\.wav$", loop=True, release="0.25")
build("harmonica-vcsl", 218, G("Aerophones/Free Aerophones/Harmonica-Hohner-Special20-C/Sustains/**/*Normal*.wav"), r"_([A-G]#?)(\d)\.wav$", loop=True, release="0.2")
build("tubeglock-vcsl", 219, G("Idiophones/Struck Idiophones/Tubular Glockenspiel/*medium1.wav"), r"^([A-G]#?)(\d)_", release="0.8")
build("wineglass-vcsl", 220, G("Idiophones/Friction Idiophones/Wine Glasses/**/*Slow_1_[Mm]ain.wav"), r"_([A-G]#?)(\d)_", loop=True, release="0.6", fade_in=0.02, octave=1, retune=True)
build("balafon-vcsl", 221, G("Idiophones/Struck Idiophones/Balafon/**/*hardM*vl2_rr1_Mid.wav"), r"_([A-G]#?)(\d)_vl", release="0.5", octave=1, retune=True)
build("strumstick-vcsl", 222, G("Chordophones/Composite Chordophones/Strumstick/**/*Finger*vl2_rr1.wav"), r"_([A-G]#?)(\d)_vl", release="0.6", octave=1)

# ---- おもちゃと小物の音（toys-vcsl・patch "toysFx"）: 鍵盤ごとに別の録音。音程は変わらない（パートには modulate: false）
#   C4 おもちゃの汽笛（短い）  C#4 汽笛（2回）  D4 汽笛（下がる）  D#4 玉の入った笛（短い）  E4 玉の入った笛（長い）  F4 サイレン笛（ヒュー）  F#4 サイレン笛（別の吹き方）
#   G4 フレクサトーン（ぴよーん）  G#4 フレクサトーン（速い）  A4 ラチェット（カラカラ・速い）  A#4 ラチェット（1回まわす）  B4 スラップスティック（パン）
#   C5 ビブラスラップ（カーッ）  C#5 ウインドチャイム（上がる）  D5 ウインドチャイム（下がる）  D#5 フィンガーシンバル（チーン）  E5 トライアングル  F5 トライアングル（止める）  F#5 トライアングル（ロール）
T = "Idiophones/Struck Idiophones/"; A_ = "Aerophones/"
TOYS = [(60, A_ + "Edge-blown Aerophones/Train Whistle, Toy/Main_TrainLow_Short-001.wav"), (61, A_ + "Edge-blown Aerophones/Train Whistle, Toy/Main_TrainLow_Double-001.wav"),
        (62, A_ + "Edge-blown Aerophones/Train Whistle, Toy/Main_TrainLow_Fall-001.wav"), (63, A_ + "Edge-blown Aerophones/Ball Whistle/Main_BallWhistle_Short-001.wav"),
        (64, A_ + "Edge-blown Aerophones/Ball Whistle/Main_BallWhistle_Long-001.wav"), (65, A_ + "Free Aerophones/Siren/Main_SirenWhistle-002.wav"), (66, A_ + "Free Aerophones/Siren/Main_SirenWhistle-008.wav"),
        (67, T + "Flexatone/flexatone1.wav"), (68, T + "Flexatone/flexatone_fast.wav"), (69, T + "Ratchet/Ratchet1_Fast_rr1_Mid.wav"), (70, T + "Ratchet/Ratchet1_Crank_rr1_Mid.wav"),
        (71, T + "Slapstick/slapstick_rr1.wav"), (72, T + "Vibraslap/vibraslap_rr1.wav"), (73, T + "Mark Trees/windchimes_asc1.wav"), (74, T + "Mark Trees/windchimes_desc1.wav"),
        (75, T + "Finger Cymbals/Fing_Cymb.wav"), (76, T + "Triangles/triangle1_hit_mp.wav"), (77, T + "Triangles/triangle1_hit_mp_muted1.wav"), (78, T + "Triangles/triangle1_roll.wav")]
d = os.path.join(WORK, "toys-vcsl"); os.makedirs(d, exist_ok=True); lines = []; longest = 0
for key, rel in TOYS:
    p = os.path.join(VC, rel)
    if not os.path.exists(p):
        c = glob.glob(os.path.join(VC, os.path.dirname(rel), "**", os.path.basename(rel)), recursive=True)
        if not c: print("  なし", rel); continue
        p = c[0]
    x = trim(read(p))[:int(6.0 * SR)].copy(); x = x / (np.abs(x).max() + 1e-9) * 0.8
    n = int(0.05 * SR); x[-n:] *= np.linspace(1, 0, n)[:, None]
    fn = f"toys_{key}.wav"; sf.write(os.path.join(d, fn), x.astype(np.float32), SR, subtype="FLOAT"); longest = max(longest, len(x) / SR)
    lines.append(f"<region> sample={fn} pitch_keycenter={key} lokey={key} hikey={key}")
open(os.path.join(d, "toys-vcsl.sfz"), "w").write("\n".join(lines) + "\n")
o = subprocess.run(["node", "tools/soundfont/sfz-to-sf3.mjs", os.path.join(d, "toys-vcsl.sfz"), "toys-vcsl", "--program", "223", "--seconds", f"{longest + 0.1:.1f}", "--rr", "1", "--q", "6",
                    "--release", "0.6", "--fade", "0.05", "--stereo"], cwd=ROOT, capture_output=True, text=True)
print("toys-vcsl", len(lines), "音", (o.stdout.strip().splitlines() or [""])[-1][-100:], o.stderr[-200:])
