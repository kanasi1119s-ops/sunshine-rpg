#!/usr/bin/env python3
"""DiffSinger のメルを、NVIDIA の BigVGAN（MIT ライセンス・商用可）で波形にする部品。

2026-10-27: DiffSinger でふつう使うボコーダー（openvpi の NSF-HiFiGAN）は、重みの規約が CC BY-NC-SA 4.0（営利目的は不可）。
収益化する動画やゲームでも安心して使えるよう、MIT ライセンスの BigVGAN v2（44.1kHz・128本・hop 512）で鳴らせるようにした。
DiffSinger のメル（40〜16000Hz・slaney）と BigVGAN のメル（0〜22050Hz・slaney）は帯域がちがうので、
いったん「周波数ごとの大きさ」に戻してから、BigVGAN のメルに作り直す（mel_matrix）。

  python3 tools/singer/ds_bigvgan.py test <歌声.wav> <出力フォルダ>   … 本物の歌声で、変換の劣化を確かめる
"""
import os, sys
import numpy as np
import torch, librosa

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VDIR = os.path.join(os.environ.get("SUNSHINE_VOICEBANKS", os.path.join(_ROOT, "assets-src", "voicebanks")), "ds/_vocoders/bigvgan-v2-44k")
_model = None

def load(vdir=VDIR):
    global _model
    if _model is None:
        sys.path.insert(0, vdir)
        import bigvgan, json
        from env import AttrDict
        h = AttrDict(json.load(open(os.path.join(vdir, "config.json"))))
        m = bigvgan.BigVGAN(h, use_cuda_kernel=False)
        sd = torch.load(os.path.join(vdir, "bigvgan_generator.pt"), map_location="cpu")
        m.load_state_dict(sd["generator"]); m.remove_weight_norm(); m.eval()
        torch.set_num_threads(int(os.environ.get("DS_THREADS", "2")))
        _model = (m, h)
    return _model

def mel_matrix(sr=44100, n_fft=2048, n_mels=128, src=(40, 16000), dst=(0, None)):
    """DiffSinger のメル（大きさ）→ BigVGAN のメル（大きさ）にかける行列"""
    A = librosa.filters.mel(sr=sr, n_fft=n_fft, n_mels=n_mels, fmin=src[0], fmax=src[1])
    B = librosa.filters.mel(sr=sr, n_fft=n_fft, n_mels=n_mels, fmin=dst[0], fmax=dst[1])
    # 大きさ → メル（A）の逆を、なめらかさの制約つきの最小二乗で（ふつうの擬似逆行列だと、帯域の外でゆれるため）
    lam = 1e-3
    D = np.diff(np.eye(A.shape[1]), axis=0)
    P = np.linalg.solve(A.T @ A + lam * (D.T @ D) + 1e-6 * np.eye(A.shape[1]), A.T)
    return (B @ P).astype(np.float32), A, B

def _centers(n_mels, fmin, fmax, sr=44100):
    return librosa.mel_frequencies(n_mels=n_mels + 2, fmin=fmin, fmax=fmax if fmax else sr / 2)[1:-1]

def ds_to_bigvgan_interp(mel, mel_base="e", hi_slope=-0.9):
    """（方法2）メルの各帯の「平均の大きさ」を、中心の周波数で読みかえる。slaney の正規化で、
    どちらのメルも「帯の中の平均の大きさ」に比例するので、対数のまま周波数で補間できる。
    16kHz より上は、いちばん上の帯から、1 帯ごとに hi_slope（自然対数）ずつ下げてのばす"""
    m = np.asarray(mel, np.float32)[0] * (np.log(10) if str(mel_base) == "10" else 1.0)
    cs = _centers(128, 40, 16000); cd = _centers(128, 0, None)
    lcs = np.log(cs); out = np.empty((m.shape[0], 128), np.float32)
    for j, f in enumerate(cd):
        if f <= cs[0]: out[:, j] = m[:, 0]
        elif f >= cs[-1]:
            k = (np.log(f) - lcs[-1]) / (lcs[-1] - lcs[-2]); out[:, j] = m[:, -1] + hi_slope * k
        else:
            i = np.searchsorted(cs, f); w = (np.log(f) - lcs[i - 1]) / (lcs[i] - lcs[i - 1])
            out[:, j] = (1 - w) * m[:, i - 1] + w * m[:, i]
    # 帯の幅の比（BigVGAN の帯は広さがちがう）による大きさの差は、slaney の正規化で打ち消されているので、そのまま
    return np.maximum(out, np.log(1e-5)).T[None].astype(np.float32)

_T = None
def ds_to_bigvgan(mel, mel_base="e"):
    """mel: [1, フレーム, 128]（DiffSinger の出力。対数） → [1, 128, フレーム]（BigVGAN の入力。自然対数）"""
    global _T
    if _T is None: _T = mel_matrix()[0]
    m = np.asarray(mel, np.float32)[0]
    mag = np.exp(m * (np.log(10) if str(mel_base) == "10" else 1.0))
    out = np.maximum(mag @ _T.T, 1e-5)
    return np.log(out).T[None].astype(np.float32)

def vocode(mel_bv):
    m, h = load()
    with torch.inference_mode():
        y = m(torch.from_numpy(mel_bv)).squeeze().numpy()
    return y.astype(np.float32)

def ds_mel_from_wave(y, sr=44100, fmin=40, fmax=16000, n_mels=128):
    """（確かめ用）DiffSinger と同じ作り方のメル（自然対数）を、波形から作る"""
    pad = (2048 - 512) // 2
    yp = np.pad(y, (pad, pad), mode="reflect")
    S = np.abs(librosa.stft(yp, n_fft=2048, hop_length=512, win_length=2048, window="hann", center=False))
    M = librosa.filters.mel(sr=sr, n_fft=2048, n_mels=n_mels, fmin=fmin, fmax=fmax)
    return np.log(np.maximum(M @ S, 1e-5)).T[None]

if __name__ == "__main__" and len(sys.argv) >= 4 and sys.argv[1] == "test":
    import soundfile as sf
    x, sr = sf.read(sys.argv[2]); x = x.mean(1) if x.ndim > 1 else x
    if sr != 44100: x = librosa.resample(x, orig_sr=sr, target_sr=44100); sr = 44100
    sec = float(os.environ.get("SEC", "30")); off = float(os.environ.get("OFF", "20"))
    x = x[int(off * sr):int((off + sec) * sr)]; x = x / (np.abs(x).max() + 1e-9) * 0.9
    os.makedirs(sys.argv[3], exist_ok=True)
    sf.write(os.path.join(sys.argv[3], "0_original.wav"), x, sr)
    dsm = ds_mel_from_wave(x)
    y1 = vocode(ds_to_bigvgan(dsm))
    y2 = vocode(ds_to_bigvgan_interp(dsm))
    sf.write(os.path.join(sys.argv[3], "3_bigvgan_from_ds_mel_interp.wav"), y2, sr)
    pad = (2048 - 512) // 2
    S = np.abs(librosa.stft(np.pad(x, (pad, pad), mode="reflect"), n_fft=2048, hop_length=512, center=False))
    B = librosa.filters.mel(sr=sr, n_fft=2048, n_mels=128, fmin=0, fmax=None)
    y0 = vocode(np.log(np.maximum(B @ S, 1e-5))[None].astype(np.float32))
    sf.write(os.path.join(sys.argv[3], "1_bigvgan_true_mel.wav"), y0, sr)
    sf.write(os.path.join(sys.argv[3], "2_bigvgan_from_ds_mel.wav"), y1, sr)
    def lsd(a, b, lo=60, hi=15000):
        n = min(len(a), len(b)); A_ = np.abs(librosa.stft(a[:n], n_fft=2048)); B_ = np.abs(librosa.stft(b[:n], n_fft=2048))
        fr = np.fft.rfftfreq(2048, 1 / 44100); sel = (fr >= lo) & (fr <= hi)
        e = np.sum(A_ ** 2, 0); act = e > np.percentile(e, 30)
        d = 20 * np.log10((A_[sel] + 1e-4) / (B_[sel] + 1e-4))
        return float(np.mean(np.sqrt(np.mean(d ** 2, axis=0))[act]))
    print("周波数のずれ（60〜15000Hz・歌っている所・dB・小さいほど元に近い）: 本物のメル", round(lsd(x, y0), 2),
          "／ DSメルから(方法1)", round(lsd(x, y1), 2), "／ DSメルから(方法2)", round(lsd(x, y2), 2))
