# ギターの試聴セット（assets-src/ai-songs/_gen/guitar_audition.py）の WAV を、6つのフレーズごとに数字で点検する。
#   2026-10-21 人間「数字は基準で必要。でも実際聞かないとわからない」: 耳の代わりではなく、聞く前に「明らかにおかしい所」を見つけるため。
#   今日見つかった不具合（右が無音・音程が揺れる・二重の歪みで高域がジリジリ・暗すぎて1音1音が聞こえない・ゲートのバタつき）を数字で拾う。
# 使い方: python3 tools/audio-check/guitar-check.py <試聴セット.wav> [--bpm 100]
import sys, subprocess, numpy as np

path = sys.argv[1]
bpm = float(sys.argv[sys.argv.index("--bpm") + 1]) if "--bpm" in sys.argv else 100.0
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", "48000", "-f", "f32le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(float)
SR = 48000
bar = 4 * 60 / bpm
NAMES = ["パワーコード", "ストローク", "アルペジオ", "単音のリフ", "リード", "カッティング"]
db = lambda v: 20 * np.log10(v + 1e-12)
BANDS = [(80, 250, "低"), (250, 800, "中低"), (800, 1600, "中"), (1600, 3200, "中高"), (3200, 6400, "高"), (6400, 12000, "ジリ")]
print(f"■ ギターの点検「{path.split('/')[-1]}」（数字は目安。最後は耳で）")
print("  フレーズ        大きさ  左右差  " + "  ".join(f"{n:>4}" for _, _, n in BANDS) + "   揺れ  バタつき  気づいたこと")
for i, name in enumerate(NAMES):
    a, b = int(i * 5 * bar * SR), int((i * 5 + 4) * bar * SR)
    seg = x[a:b]
    if len(seg) < SR:
        continue
    m = seg.mean(axis=1)
    rms = np.sqrt((m ** 2).mean())
    lr = db(np.sqrt((seg[:, 0] ** 2).mean())) - db(np.sqrt((seg[:, 1] ** 2).mean()))
    S = np.abs(np.fft.rfft(m)) ** 2; f = np.fft.rfftfreq(len(m), 1 / SR); tot = S.sum()
    bands = [10 * np.log10(S[(f >= lo) & (f < hi)].sum() / tot + 1e-12) for lo, hi, _ in BANDS]
    # 揺れ: 10ms ごとの大きさの変化のうち、4〜9Hz（ビブラート・ループの周期の速さ）の成分の強さ（伸ばした音の多いフレーズで効く）
    env = np.array([np.sqrt((m[k:k + 480] ** 2).mean()) for k in range(0, len(m) - 480, 480)])
    e = db(env); e = e - np.convolve(e, np.ones(25) / 25, "same")
    E = np.abs(np.fft.rfft(e * np.hanning(len(e)))); fe = np.fft.rfftfreq(len(e), 0.01)
    wob = E[(fe >= 4) & (fe <= 9)].mean() / (E[(fe >= 1) & (fe <= 20)].mean() + 1e-9)
    # バタつき: 50ms のうちに 15dB 以上落ちて、200ms 以内に戻る回数（ゲートが音の途中で開け閉めしている）
    flick = 0
    for k in range(5, len(env) - 20):
        if e[k] - e[k + 5] > 15 and e[k + 20] - e[k + 5] > 12:
            flick += 1
    notes = []
    if abs(lr) > 3: notes.append(f"左右の大きさが {lr:+.1f}dB ずれている")
    if bands[3] < -22: notes.append("中高（1.6〜3.2kHz）が弱く、1音1音が聞こえにくいかも")
    if bands[5] > -18: notes.append("6.4kHz 以上が多く、ジリジリ・ガチャつきが出やすい")
    if wob > 1.8: notes.append("4〜9Hz の揺れが目立つ（ビブラート・ループの揺れ）")
    if flick > 3: notes.append("音の途中のバタつき（ゲート）")
    print(f"  {name:<10} {db(rms):6.1f} {lr:+6.1f}  " + "  ".join(f"{v:5.1f}" for v in bands) + f"  {wob:5.2f}  {flick:4d}    " + ("・".join(notes) or "－"))
