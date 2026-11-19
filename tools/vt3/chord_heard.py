# 書き出した音から、小節ごとに「どの和音に聞こえるか」と「3度の音の強さ」を測る
import sys, numpy as np, librosa
CH = sys.argv[2].split(",") if len(sys.argv) > 2 else ["Bm", "G", "D", "A", "Em7", "F#m", "Asus4", "D"]; BPM = float(sys.argv[3]) if len(sys.argv) > 3 else 146
PCN = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def info(c):
    r = PCN.index(c[:2] if len(c) > 1 and c[1] == "#" else c[0]); q = c[len(PCN[r]):]
    third = 3 if q.startswith("m") and not q.startswith("maj") else (5 if "sus4" in q else 4)
    return r, (r + third) % 12, (r + 7) % 12
y, sr = librosa.load(sys.argv[1], sr=22050, mono=True)
C = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=512, n_chroma=12, fmin=librosa.note_to_hz("C2"), n_octaves=5)
bar = 4 * 60 / BPM; ok = 0; rat = []
tm = {}
for r in range(12):
    for name, iv in (("", (0, 4, 7)), ("m", (0, 3, 7)), ("sus4", (0, 5, 7)), ("5", (0, 7))):
        v = np.zeros(12); v[[(r + i) % 12 for i in iv]] = 1; tm[PCN[r] + name] = v / np.linalg.norm(v)
for i, c in enumerate(CH):
    a, b = int((i * bar + 0.15) * sr / 512), int(((i + 1) * bar - 0.1) * sr / 512); v = C[:, a:b].mean(1); v = v / (np.linalg.norm(v) + 1e-9)
    best = max(tm, key=lambda k: float(tm[k] @ v)); r, t, f = info(c); ratio = v[t] / max(v[r], v[f]); rat.append(ratio)
    want = c.replace("7", ""); hit = best == want; ok += hit
    print(f"  {c:6s} → 聞こえ方 {best:6s} {'○' if hit else '×'}  3度の強さ（根音・5度の強い方を1として）{ratio:.2f}")
print(f"  和音どおりに聞こえた: {ok}/{len(CH)}　3度の強さの平均 {np.mean(rat):.2f}")
