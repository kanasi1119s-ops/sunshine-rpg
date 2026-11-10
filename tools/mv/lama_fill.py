"""背景の絵の「人物に隠れて見えない所」を、絵をうめる AI（LaMa）で描き足す
（2026-11-11『白い息のリテイク』。人間「肩周りの背景がぼやけてる」「もっと際まで完全に」）。
  横につなぐ・鏡うつしにする、では、うめた所だけ のっぺりしたり、柱がななめに曲がったりして、人物の際で本物の背景と
  つながらなかった。LaMa は、まわりの絵（駅の屋根・窓・柱・雪の地面）の続きを考えて描くので、際までつながる。
    1 回目: 穴のまわり 720×720 を 512×512 に縮めて、全体の形（屋根の線・建物の続き）を描く
    2 回目: 穴のふち（本物の背景から 48px まで）だけを、縮めずに 512×512 ずつ描き直す
            → 人物が動いて見える所は、となりの本物の背景と同じ細かさになる
  モデル: Hugging Face の Carve/LaMa-ONNX（lama_fp32.onnx。Apache-2.0。元は advimman/lama）
  python3 lama_fill.py <背景（穴の前）png> <穴 png（白=穴）> <lama_fp32.onnx> <出力 png>
"""
import sys, cv2, numpy as np, onnxruntime as ort
RAW, HOLE, MODEL, OUT = sys.argv[1:5]
img = cv2.imread(RAW); hole = cv2.imread(HOLE, 0) > 127; H, W = hole.shape
sess = ort.InferenceSession(MODEL, providers=["CPUExecutionProvider"])
def lama(bgr, m):
    """bgr: 512×512 uint8, m: 512×512 bool（True=描く所）→ 512×512 uint8"""
    x = bgr[..., ::-1].astype(np.float32).transpose(2, 0, 1)[None] / 255.0
    mk = m.astype(np.float32)[None, None]
    y = sess.run(None, {sess.get_inputs()[0].name: x, sess.get_inputs()[1].name: mk})[0][0].transpose(1, 2, 0)
    if y.max() <= 1.5: y = y * 255.0
    return np.clip(y, 0, 255).astype(np.uint8)[..., ::-1]
EL = lambda n: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (n, n))
hd = cv2.dilate(hole.astype(np.uint8), EL(7)) > 0                 # 境目のにごりも一緒に描き直す
# 1 回目（全体）
ys, xs = np.where(hd); cx = int((xs.min() + xs.max()) / 2); S = H
x0 = int(np.clip(cx - S // 2, 0, W - S))
crop = img[:, x0:x0 + S]; mc = hd[:, x0:x0 + S]
small = cv2.resize(crop, (512, 512), interpolation=cv2.INTER_AREA); ms = cv2.resize(mc.astype(np.uint8), (512, 512), interpolation=cv2.INTER_NEAREST) > 0
big = cv2.resize(lama(small, ms), (S, S), interpolation=cv2.INTER_CUBIC)
out = img.copy().astype(np.float32)
fe = cv2.GaussianBlur(mc.astype(np.float32), (0, 0), 2)[..., None]
out[:, x0:x0 + S] = out[:, x0:x0 + S] * (1 - fe) + big.astype(np.float32) * fe
# 2 回目（ふちだけ、縮めずに）
dist = cv2.distanceTransform(hd.astype(np.uint8), cv2.DIST_L2, 5)
rim = hd & (dist < 48)
acc = np.zeros((H, W, 3), np.float32); wsum = np.zeros((H, W), np.float32)
win = np.outer(np.hanning(512), np.hanning(512)).astype(np.float32) + 1e-3
cur = np.clip(out, 0, 255).astype(np.uint8)
for ty in sorted(set(list(range(0, H - 512, 208)) + [H - 512])):
    for tx in sorted(set(list(range(0, W - 512, 256)) + [W - 512])):
        m = rim[ty:ty + 512, tx:tx + 512]
        if m.sum() < 50: continue
        r = lama(cur[ty:ty + 512, tx:tx + 512], m).astype(np.float32)
        acc[ty:ty + 512, tx:tx + 512] += r * win[..., None]; wsum[ty:ty + 512, tx:tx + 512] += win
ok = wsum > 0
ref = np.where(ok[..., None], acc / np.maximum(wsum, 1e-6)[..., None], out)
fr = cv2.GaussianBlur(rim.astype(np.float32), (0, 0), 1.5)[..., None]
out = out * (1 - fr) + ref * fr
cv2.imwrite(OUT, np.clip(out, 0, 255).astype(np.uint8)); print("ok", OUT)
