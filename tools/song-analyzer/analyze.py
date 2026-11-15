#!/usr/bin/env python3
"""曲の分析ソフト・段1（学習用）: 曲のファイルから「いつ・何が鳴って・何が休むか」と「強弱」のカルテを作る（2026-11-16）。
構想: docs/design/song-analyzer-plan.md
  1. 分ける: Demucs（htdemucs_6s・MIT）で、歌・ドラム・ベース・ギター・ピアノ・そのほか に分ける
  2. 測る: テンポと拍・小節の頭／場面の区切り／小節ごとの音量・帯域・左右の広がり／楽器ごとの「鳴っている・休んでいる」／ドラムの手数
  3. まとめる: カルテ（JSON）と、1枚の図（PNG）
使い方: python3 tools/song-analyzer/analyze.py <曲のファイル> --out <出力フォルダ> [--bpm 数字] [--name 名前] [--stems]
決まり: 保存するのは作り方の特徴だけ（旋律・歌詞・1曲ぶんのコード進行は保存しない）。分けた音（ステム）は --stems を付けたときだけ書き出す。
当たりやすさ: テンポは「2倍・半分」をまちがえることがある（--bpm で直せる）。小節の頭と場面の区切りは「たぶん」。細かい楽器名は分からない（6つの分類まで）。"""
import sys, os, json, subprocess, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SR = 44100
JP = {"vocals": "歌", "drums": "ドラム", "bass": "ベース", "chordal": "和音の楽器", "guitar": "ギター", "piano": "ピアノ", "other": "シンセ・弦など"}
ORDER = ["vocals", "drums", "bass", "chordal"]      # 当たりやすい4つの分類。和音の楽器＝ギター・ピアノ・シンセ・弦などをまとめたもの
SUB = ["guitar", "piano", "other"]                  # 和音の楽器の中身（たぶん。分ける道具が、ギターやピアノを「そのほか」に入れてしまうことがある）


def load_audio(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).T.copy()       # (2, n)


def separate(wav):
    import torch
    from demucs.pretrained import get_model
    from demucs.apply import apply_model
    torch.set_num_threads(max(1, os.cpu_count() or 1))
    model = get_model("htdemucs_6s"); model.eval()
    x = torch.from_numpy(wav); ref = x.mean(0); x = (x - ref.mean()) / (ref.std() + 1e-8)
    with torch.no_grad(): out = apply_model(model, x[None], device="cpu", shifts=0, split=True, overlap=0.1, progress=False)[0]
    out = out * (ref.std() + 1e-8) + ref.mean()
    return {n: out[i].numpy() for i, n in enumerate(model.sources)}


def db(x): return 20 * np.log10(np.maximum(x, 1e-9))


def rms_frames(mono, hop):
    n = len(mono) // hop; return np.sqrt((mono[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)


def analyze(path, bpm=None, name=None, keep_stems=None):
    import librosa
    wav = load_audio(path); dur = wav.shape[1] / SR; mono = wav.mean(0)
    cache = os.environ.get("SA_CACHE"); cf = os.path.join(cache, (name or "x") + ".stems.npz") if cache else None
    if cf and os.path.exists(cf): stems = dict(np.load(cf))
    else:
        stems = separate(wav)
        if cf: np.savez(cf, **{k: v.astype(np.float16) for k, v in stems.items()})
    stems = {k: v.astype(np.float32) for k, v in stems.items()}
    if keep_stems:
        import soundfile as sf
        os.makedirs(keep_stems, exist_ok=True)
        for k, v in stems.items(): sf.write(os.path.join(keep_stems, f"{k}.flac"), v.T, SR)
    sm = {k: v.mean(0) for k, v in stems.items()}; sm["chordal"] = sm["guitar"] + sm["piano"] + sm["other"]
    # ---- テンポ・拍・小節の頭 ----
    y22 = librosa.resample(sm["drums"] + sm["bass"] + 0.5 * (mono - sm["vocals"]), orig_sr=SR, target_sr=22050)
    oenv = librosa.onset.onset_strength(y=y22, sr=22050, hop_length=256)
    t0 = float(np.atleast_1d(librosa.feature.tempo(onset_envelope=oenv, sr=22050, hop_length=256))[0]) if not bpm else float(bpm)
    tempo, bf = librosa.beat.beat_track(onset_envelope=oenv, sr=22050, hop_length=256, start_bpm=t0, tightness=100 if not bpm else 400)
    beats = librosa.frames_to_time(bf, sr=22050, hop_length=256); tempo = float(np.atleast_1d(tempo)[0])
    if len(beats) < 16: raise SystemExit("拍が取れませんでした")
    # 小節の頭: 4つの候補のうち、低い音（キック・ベース）の立ち上がりと、和音の変わり目がいちばん強い所
    lowy = librosa.resample(sm["drums"] + sm["bass"], orig_sr=SR, target_sr=22050)
    S = np.abs(librosa.stft(lowy, n_fft=2048, hop_length=256)); fr = librosa.fft_frequencies(sr=22050, n_fft=2048)
    lenv = np.maximum(0, np.diff(S[fr < 150].sum(0), prepend=0)); harm = librosa.resample(mono - sm["drums"], orig_sr=SR, target_sr=22050)
    chroma = librosa.feature.chroma_cqt(y=harm, sr=22050, hop_length=512); cb = librosa.util.sync(chroma, librosa.time_to_frames(beats, sr=22050, hop_length=512), aggregate=np.median)
    nov = np.r_[0, 1 - np.sum(cb[:, 1:] * cb[:, :-1], 0) / (np.linalg.norm(cb[:, 1:], axis=0) * np.linalg.norm(cb[:, :-1], axis=0) + 1e-9)][:len(beats)]
    lb = np.array([lenv[max(0, f - 3):f + 4].max() for f in bf]); lb = lb / (lb.max() + 1e-9); nov = nov / (nov.max() + 1e-9)
    sc = [float(lb[p::4].mean() + nov[p::4][:len(lb[p::4])].mean()) for p in range(4)]; phase = int(np.argmax(sc)); conf = float((sorted(sc)[-1] - sorted(sc)[-2]) / (sorted(sc)[-1] + 1e-9))
    bar_t = beats[phase::4]; spb = float(np.median(np.diff(beats)))
    while bar_t[0] - 4 * spb > -1.0 * spb: bar_t = np.r_[bar_t[0] - 4 * spb, bar_t]      # 曲の頭まで小節をさかのぼる（前奏にドラムがなくて拍が取れなかった所）
    bar_t = np.r_[bar_t, bar_t[-1] + 4 * spb]; bar_t = bar_t[bar_t < dur + 0.5]; nb = len(bar_t) - 1
    idx = lambda t: int(max(0, min(wav.shape[1], round(t * SR))))
    # ---- 小節ごとの強弱・帯域・広がり ----
    def band_share(x):
        sp = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2; f = np.fft.rfftfreq(len(x), 1 / SR); tot = sp.sum() + 1e-12
        return [float(sp[(f >= a) & (f < b)].sum() / tot) for a, b in ((20, 150), (150, 2000), (2000, 16000))]
    bars = []
    for i in range(nb):
        a, b = idx(bar_t[i]), idx(bar_t[i + 1]); seg = wav[:, a:b]
        if seg.shape[1] < 2048: bars.append(dict(db=-90.0, low=0, mid=0, high=0, width=0)); continue
        m = seg.mean(0); side = (seg[0] - seg[1]) / 2; lo, mi, hi = band_share(m)
        bars.append(dict(db=float(db(np.sqrt((m ** 2).mean()))), low=lo, mid=mi, high=hi, width=float(np.sqrt((side ** 2).mean()) / (np.sqrt((m ** 2).mean()) + 1e-9))))
    loud = np.array([x["db"] for x in bars])
    # ---- 楽器ごとの「鳴っている・休んでいる」（16分ごと → 小節ごと）----
    hop = max(256, int(round(spb / 4 * SR))); mixr = db(rms_frames(mono, hop)); mix95 = float(np.percentile(mixr, 95))
    act16 = {}; present = {}; level = {}
    for k in ORDER:
        r = db(rms_frames(sm[k], hop)); p95 = float(np.percentile(r, 95)); present[k] = bool(p95 > mix95 - 22); level[k] = p95 - mix95
        act16[k] = (r > max(p95 - 26, mix95 - 40)) if present[k] else np.zeros(len(r), bool)
    n16 = min(len(v) for v in act16.values()); t16 = np.arange(n16) * hop / SR
    def bar_frac(v):
        return [float(v[(t16 >= bar_t[i]) & (t16 < bar_t[i + 1])].mean()) if ((t16 >= bar_t[i]) & (t16 < bar_t[i + 1])).any() else 0.0 for i in range(nb)]
    act_bar = {k: bar_frac(act16[k][:n16]) for k in ORDER}
    sub_e = {k: np.array([float((sm[k][idx(bar_t[i]):idx(bar_t[i + 1])] ** 2).sum()) for i in range(nb)]) for k in SUB}; tot_e = sum(sub_e.values()) + 1e-12
    sub_share = {k: sub_e[k] / tot_e for k in SUB}
    acc = np.zeros(n16, bool)
    for k in ORDER:
        if k != "vocals": acc |= act16[k][:n16]
    inside = (t16 >= bar_t[0]) & (t16 < bar_t[-1]); voc = act16["vocals"][:n16]
    rests = {"伴奏が休んでいる時間の割合": float(1 - acc[inside].mean()), "歌が休んでいる時間の割合": float(1 - voc[inside].mean()) if present["vocals"] else None,
             "全員が休んでいる時間の割合": float((~acc & ~voc)[inside].mean())}
    layers = np.array([sum(act_bar[k][i] > 0.3 for k in ORDER) for i in range(nb)])
    # ---- ドラムの手数（1拍あたり。低い・中くらい・高い音に分けて立ち上がりを数える）----
    drum = {}
    if present["drums"]:
        d22 = librosa.resample(sm["drums"], orig_sr=SR, target_sr=22050); Sd = np.abs(librosa.stft(d22, n_fft=1024, hop_length=256)); fd = librosa.fft_frequencies(sr=22050, n_fft=1024)
        for nm_, (a, b) in {"キック（低い音）": (30, 150), "スネア（中くらい）": (180, 2500), "刻み（高い音）": (6000, 11000)}.items():
            env = librosa.onset.onset_strength(S=librosa.amplitude_to_db(Sd[(fd >= a) & (fd < b)], ref=np.max), sr=22050, hop_length=256)
            on = librosa.onset.onset_detect(onset_envelope=env, sr=22050, hop_length=256, units="time", delta=0.25, wait=3)
            per = [float(((on >= bar_t[i]) & (on < bar_t[i + 1])).sum() / 4) for i in range(nb)]; drum[nm_] = per
    # ---- 場面の区切り（2拍ごとの特徴の変わり目。テンポを半分にまちがえても区切りを取りこぼさないよう、小節より細かく見る）----
    ut = np.r_[beats[phase % 2::2], beats[-1] + 2 * spb]; ut = ut[ut < dur + 0.5]; nu = len(ut) - 1
    mf = librosa.feature.mfcc(y=librosa.resample(mono, orig_sr=SR, target_sr=22050), sr=22050, n_mfcc=13, hop_length=512)
    ufr = librosa.time_to_frames(ut[:-1], sr=22050, hop_length=512); mb = librosa.util.sync(mf, ufr, aggregate=np.mean)[:, -nu:]; chb = librosa.util.sync(chroma, ufr, aggregate=np.mean)[:, -nu:]
    nu = min(nu, mb.shape[1], chb.shape[1]); mb, chb = mb[:, :nu], chb[:, :nu]
    au = np.array([[float(act16[k][:n16][(t16 >= ut[i]) & (t16 < ut[i + 1])].mean()) if ((t16 >= ut[i]) & (t16 < ut[i + 1])).any() else 0.0 for i in range(nu)] for k in ORDER])
    lu = np.array([float(db(np.sqrt((mono[idx(ut[i]):idx(ut[i + 1])] ** 2).mean() + 1e-12))) for i in range(nu)])
    z = lambda M: (M - M.mean(1, keepdims=True)) / (M.std(1, keepdims=True) + 1e-9)
    F = np.vstack([z(mb), 2 * z(chb), 3 * au, 0.25 * (lu - lu.mean())[None]])
    Fn = F / (np.linalg.norm(F, axis=0, keepdims=True) + 1e-9); SSM = Fn.T @ Fn; Kh = 8; novs = np.zeros(nu)
    for i in range(2, nu - 1):
        a0, a1, b1 = max(0, i - Kh), i, min(nu, i + Kh)
        if a1 - a0 < 2 or b1 - a1 < 2: continue
        novs[i] = (SSM[a0:a1, a0:a1].mean() + SSM[a1:b1, a1:b1].mean()) / 2 - SSM[a0:a1, a1:b1].mean()
    cand = [i for i in range(2, nu - 1) if novs[i] >= novs[i - 1] and novs[i] >= novs[i + 1] and novs[i] > np.percentile(novs, 55)]
    ub = [0]
    for i in sorted(cand, key=lambda i: -novs[i]):
        if all(abs(i - j) >= 6 for j in ub) and nu - i >= 3: ub.append(i)
    ub = sorted(sorted(ub, key=lambda i: -novs[i] if i else -9)[: max(4, int(dur / 11))])
    def snap(i):      # 区切りを、前後2つの中で「楽器の出入りと音量がいちばん変わる所」へ寄せる
        if i == 0: return 0
        c = [j for j in range(max(1, i - 2), min(nu - 1, i + 3))]; sc_ = [np.abs(au[:, j:j + 2].mean(1) - au[:, max(0, j - 2):j].mean(1)).sum() + 0.15 * abs(lu[j:j + 2].mean() - lu[max(0, j - 2):j].mean()) for j in c]
        return c[int(np.argmax(sc_))] if max(sc_) > 0.5 else i
    ub = sorted(set(snap(i) for i in ub))
    bsec = [float(ut[i]) for i in ub] + [float(bar_t[-1])]
    bar_of = lambda t: int(np.argmin(np.abs(bar_t - t)))
    segs = []
    for (ua, ta), (ub2, tb) in zip(zip(ub, bsec), zip(ub[1:] + [nu], bsec[1:])):
        a, b = bar_of(ta), max(bar_of(ta) + 1, bar_of(tb)); b = min(b, nb)
        if a >= nb: continue
        segs.append(dict(start_bar=int(a), bars=int(b - a), start_sec=float(ta), length_sec=float(tb - ta), feat=F[:, ua:ub2].mean(1)))
    # 似た場面に同じ文字を付ける
    labels = []; protos = []
    for s in segs:
        f = s["feat"] / (np.linalg.norm(s["feat"]) + 1e-9); sim = [float(f @ p) for p in protos]
        if sim and max(sim) > 0.82: labels.append(int(np.argmax(sim)))
        else: protos.append(f); labels.append(len(protos) - 1)
    for s, l in zip(segs, labels):
        a, b = s["start_bar"], s["start_bar"] + s["bars"]; s["kind"] = "ABCDEFGHIJKLMNOP"[l % 16]; del s["feat"]
        s["loud_db"] = float(np.mean(loud[a:b])); s["layers"] = float(np.mean(layers[a:b]))
        s["active"] = {k: float(np.mean(act_bar[k][a:b])) for k in ORDER if present[k]}
        s["chordal_mix_maybe"] = {k: round(float(np.mean(sub_share[k][a:b])), 2) for k in SUB}
        if drum: s["drum_hits_per_beat"] = {k: float(np.mean(v[a:b])) for k, v in drum.items()}
    top = max(s["loud_db"] for s in segs)
    for s in segs:
        s["note"] = ("いちばん大きい場面" if s["loud_db"] >= top - 0.3 else ("静かな場面" if s["loud_db"] < top - 6 else "")) + ("・歌なし" if present["vocals"] and s["active"].get("vocals", 0) < 0.15 else "")
    # 入り・抜け: 場面の頭で、前の場面にくらべて入った楽器・抜けた楽器
    for p, s in zip([None] + segs, segs):
        if p is None: s["enter"] = [k for k in ORDER if s["active"].get(k, 0) > 0.5]; s["leave"] = []
        else: s["enter"] = [k for k in ORDER if s["active"].get(k, 0) > 0.5 and p["active"].get(k, 0) < 0.25]; s["leave"] = [k for k in ORDER if s["active"].get(k, 0) < 0.25 and p["active"].get(k, 0) > 0.5]
    import stage2
    s2, raw2 = stage2.run(sm, beats, bar_t, spb, present, librosa)
    if os.environ.get("SA_RAW"):      # 答え合わせ用（自分の曲だけ）: 書き起こしそのものを別のファイルに出す
        import pickle; rp = os.environ["SA_RAW"]; pickle.dump(dict(bar_t=bar_t, raw=raw2), open(os.path.join(rp, (name or "x") + ".raw.pkl") if os.path.isdir(rp) else rp, "wb"))
    import stage3
    st2 = dict(stems); st2["chordal"] = stems["guitar"] + stems["piano"] + stems["other"]; s3 = stage3.run(st2, beats, bar_t, raw2, present, librosa)
    res = dict(name=name or os.path.splitext(os.path.basename(path))[0], seconds=round(dur, 1), tempo=round(60 / spb, 1), tempo_guess=round(tempo, 1), tempo_given=bool(bpm),
               bars=nb, downbeat_confidence=round(conf, 2), stems_present={k: present[k] for k in ORDER}, stem_level_db={k: round(level[k], 1) for k in ORDER},
               loudness=dict(max_db=round(float(loud.max()), 1), range_db=round(float(np.percentile(loud, 95) - np.percentile(loud, 10)), 1),
                             low=round(float(np.mean([x["low"] for x in bars])), 3), mid=round(float(np.mean([x["mid"] for x in bars])), 3), high=round(float(np.mean([x["high"] for x in bars])), 3),
                             width=round(float(np.mean([x["width"] for x in bars])), 3)),
               rests={k: (round(v, 3) if v is not None else None) for k, v in rests.items()}, layers=dict(mean=round(float(layers.mean()), 2), min=int(layers.min()), max=int(layers.max()), changes_per_8bars=round(float((np.diff(layers) != 0).sum() / max(1, nb) * 8), 2)),
               drums_hits_per_beat={k: round(float(np.mean(v)), 2) for k, v in drum.items()}, stage2=s2, stage3=s3, sections=segs,
               per_bar=dict(time=[round(float(t), 2) for t in bar_t[:-1]], db=[round(float(x), 1) for x in loud], low=[round(x["low"], 3) for x in bars], high=[round(x["high"], 3) for x in bars], width=[round(x["width"], 3) for x in bars],
                            layers=[int(x) for x in layers], chordal_mix_maybe={k: [round(float(x), 2) for x in sub_share[k]] for k in SUB}, active={k: [round(x, 2) for x in act_bar[k]] for k in ORDER}, drums={k: [round(x, 2) for x in v] for k, v in drum.items()}))
    return res


def chart(res, png):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    for f in ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", "/usr/share/fonts/opentype/noto/NotoSansCJKjp-Regular.otf"):
        if os.path.exists(f): font_manager.fontManager.addfont(f); plt.rcParams["font.family"] = font_manager.FontProperties(fname=f).get_name(); break
    pb = res["per_bar"]; nb = res["bars"]; x = np.arange(nb); ks = [k for k in ORDER if res["stems_present"][k]]
    fig, ax = plt.subplots(4, 1, figsize=(13, 9), sharex=True, gridspec_kw={"height_ratios": [2.2, 1.3, 1, 1.2]})
    A = np.array([pb["active"][k] for k in ks]); ax[0].imshow(A, aspect="auto", cmap="Blues", vmin=0, vmax=1, extent=(-0.5, nb - 0.5, len(ks) - 0.5, -0.5), interpolation="nearest")
    ax[0].set_yticks(range(len(ks))); ax[0].set_yticklabels([JP[k].split("（")[0] for k in ks]); ax[0].set_title(f"{res['name']}  — テンポ {res['tempo']}・{nb}小節・{res['seconds']}秒   （濃い＝鳴っている、白＝休み。上の文字＝場面と小節の数。同じ文字は似た場面）", loc="left", pad=24)
    ax[1].plot(x, pb["db"], color="#c0392b"); ax[1].set_ylabel("音量 (dB)"); ax[1].grid(alpha=0.3)
    ax[2].step(x, pb["layers"], where="mid", color="#2c3e50"); ax[2].set_ylabel("重なっている\n楽器の数"); ax[2].set_ylim(-0.2, 4.2); ax[2].grid(alpha=0.3)
    for k, c in zip(pb["drums"], ("#8e44ad", "#27ae60", "#e67e22")): ax[3].plot(x, pb["drums"][k], label=k, color=c, lw=1)
    ax[3].set_ylabel("ドラムの手数\n(1拍あたり)"); ax[3].set_xlabel("小節"); ax[3].grid(alpha=0.3)
    if pb["drums"]: ax[3].legend(loc="upper right", ncol=3, fontsize=8)
    for s in res["sections"]:
        for a in ax: a.axvline(s["start_bar"] - 0.5, color="k", lw=0.8, alpha=0.6)
        ax[0].text(s["start_bar"] - 0.3, -0.62, f"{s['kind']}（{s['bars']}）", fontsize=9, va="bottom")
    plt.tight_layout(); plt.savefig(png, dpi=110); plt.close()


def summary(res):
    L = [f"■ {res['name']}: テンポ {res['tempo']}{'（指定）' if res['tempo_given'] else '（たぶん。2倍・半分のまちがいに注意）'}・{res['bars']}小節・{res['seconds']}秒",
         "  鳴っている楽器: " + "・".join(JP[k].split("（")[0] for k in ORDER if res["stems_present"][k]),
         f"  休み: 伴奏 {res['rests']['伴奏が休んでいる時間の割合'] * 100:.1f}%・歌 {(res['rests']['歌が休んでいる時間の割合'] or 0) * 100:.1f}%・全員 {res['rests']['全員が休んでいる時間の割合'] * 100:.1f}%",
         f"  強弱: 小節ごとの音量の幅 {res['loudness']['range_db']}dB・重なる楽器の数 {res['layers']['min']}〜{res['layers']['max']}（平均 {res['layers']['mean']}）・8小節あたり {res['layers']['changes_per_8bars']} 回入れかわる",
         "  ドラムの手数（1拍あたり）: " + "・".join(f"{k} {v}" for k, v in res["drums_hits_per_beat"].items()), "  場面:"]
    for s in res["sections"]:
        act = "・".join(JP[k].split("（")[0] for k in ORDER if s["active"].get(k, 0) > 0.5)
        ent = (" ＋" + "・".join(JP[k].split("（")[0] for k in s["enter"])) if s["enter"] and s["start_bar"] > 0 else ""; lv = (" −" + "・".join(JP[k].split("（")[0] for k in s["leave"])) if s["leave"] else ""
        cm = s["chordal_mix_maybe"]; top_ = max(cm, key=cm.get); sub = f"（和音の楽器は、たぶん{JP[top_]}が中心 {cm[top_] * 100:.0f}%）" if s["active"].get("chordal", 0) > 0.5 else ""
        L.append(f"    {s['start_sec']:6.1f}秒 {s['kind']}（{s['bars']:2d}小節）{s['loud_db']:6.1f}dB  {act}{ent}{lv}  {s['note']} {sub}")
    return "\n".join(L)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("path"); ap.add_argument("--out", default="."); ap.add_argument("--bpm", type=float); ap.add_argument("--name"); ap.add_argument("--stems", action="store_true")
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True); nm = a.name or os.path.splitext(os.path.basename(a.path))[0]
    r = analyze(a.path, a.bpm, nm, os.path.join(a.out, nm + "-stems") if a.stems else None)
    json.dump(r, open(os.path.join(a.out, nm + ".karte.json"), "w"), ensure_ascii=False, indent=1); chart(r, os.path.join(a.out, nm + ".karte.png")); print(summary(r))
