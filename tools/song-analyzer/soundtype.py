#!/usr/bin/env python3
"""音の種類の聞き分け（2026-11-17 人間「使ってる楽器、コード、音の種類、ジャンルなどあらゆるものがわかる用に」）。
作曲ソフトの音色（正解がわかっている約 200 種類）を 1 音ずつ鳴らして「音の指紋」を取り、知らない音がどの音色・どの種類（のこぎり波・矩形波・ベル・プラック・パッド…）に近いかを答える。
使い方:
  python3 tools/song-analyzer/soundtype.py learn <見本のフォルダ（ptNN.wav と ptNN.names）> <出力 JSON>   … 指紋の表を作る
  python3 tools/song-analyzer/soundtype.py eval <指紋の JSON>                                        … 当たり具合（1 つ抜いて確かめる・高さを変えて確かめる）
  python3 tools/song-analyzer/soundtype.py what <指紋の JSON> <音のファイル> [分けた音の名前 bass/other/piano/guitar]   … 曲（または 1 本の音）の中の、のびている音を見つけて答える
指紋の中身（1 音ぶん）: 倍音の強さの形（1〜16 番め）・奇数と偶数の倍音のつり合い・明るさ・倍音からはずれた音（ざらつき・金属っぽさ）の割合・
  立ち上がりの時間・鳴らしている間の減り方（0.5 秒・1 秒・1.9 秒）・音を止めたあとの消え方・明るさの時間変化・大きさのうねり（重ねた波のうなり）・高さのゆれ・左右の広がり
見本の 1 こま（8 秒・テンポ 120）: ド4 短い音 → ド4 を 2 秒のばす → ド3 → ド5 → ソ4 を 4 回"""
import sys, os, json, glob, warnings
warnings.filterwarnings("ignore")
import numpy as np, soundfile as sf
from scipy import signal
SLOT = 8.0
TYPES = {
 "のこぎり波のシンセ（リード・スーパーソウ）": "sawLead supersawPad modernSupersaw kfbSupersaw kfbSupersawSwell kfbSupersawWide kfbSawStab kfbTranceLead kfbHoover kfbRaveStab kfbHardcoreLead surgeHappySaws fbChord polysynth charang fifths brightLead modernLead kfbDreamLead kfbWobbleLead surgeChordUnisonMinority surgeChord5thElement surgeChordMg",
 "矩形波・パルス波のシンセ": "squareLead chipPulse25 chipPulse12 kfbSquarePluck kfbSquareLead kfbChipLead picoLead picoLeadRound surgeFormantPulse surgeChordBellSquare2 kfbBoops",
 "サイン波に近い丸い音": "kfbSineLead kfbSub ocarina calliope chiff kfbFlute wineGlass",
 "ベル・鉄琴・オルゴール": "glockenspiel celesta vibraphone kfbGlocken kfbMusicBox kfbBrightBells popBell surgeBell1 surgeFantasyBell tubeGlock crystal kalimbaReal marimba xylophone balafon surgeKeysBellKeys3135 surgeKeysBellKeys2156 surgeKeysGluckophone iceRain brightness starTheme surgeChordXyloChill",
 "エレピ・FM の鍵盤": "kfbGlassEp surgeKeysDxEp surgeKeysDxTonez surgeKeysFmPiano1 surgeKeysFmEPiano135 surgeKeysLightEp popKeys surgeKeysBellPiano surgeKeysAliasGlassPiano2 surgeKeysNanowave2Oscs surgeKeysNanowaveWithNimbus surgeKeysElectricNightmares surgeKeysDizzy honkyTonk clavinet surgeChordMinorSynthPiano",
 "プラック（はじいて減る音）": "pluckSynth glassPluck modernPluck kawaiiArp surgePopcorn surgeNicePluck surgeWaveguide surgeGuzheng surgeRetroWave surgeConvex surgeWoody surgeFriendly surgeMixedFeelings surgeChordPluckCharacter pizzicato folkHarp surgeTropics surgeDnaSeq",
 "パッド（ゆっくり広がる音）": "warmPad newAge halo sweep metalPad bowedGlass modernPad kfbSparklePad surgePadHineVertigo surgePadNeverending surgePadSparkly surgePadVerbPad surgePadCrystals surgePadNewtonWasEvil surgePadStringPad surgePadMwPulsating surgePadBellPad surgePadBright surgePadFifths6 surgePadClassicStrings surgePadBowed surgePadPad2Mw atmosphere synthStrings1 synthStrings2 slowStrings soundtrack goblin echoDrops",
 "シンセベース": "synthBass1 synthBass2 reeseBass modernBass kfbGrowlBass kfbNeuroBass kfbFmBass surgeBassPasty surgeBassAnalogBassImaged surgeBassCatBass surgeBassWarmSquare surgeBassEmulation surgeBassPop surgeBassModernDirtyFat bassLead",
 "生のベース": "acousticBass fretlessBass slapBass",
 "ギター（録音の音）": "nylonGuitar steelGuitar jazzGuitar cleanGuitar mutedGuitar strumstick",
 "弦（バイオリンなど）": "violin viola cello contrabass stringEnsemble stringsSpiccato stringsTremolo",
 "金管": "trumpet trombone tuba horn brassSection mutedTrumpet synthBrass1 synthBrass2",
 "木管・サックス・笛": "oboe bassoon clarinet piccolo flute tinWhistle tenorSax altoSax bariSax kfbFutureSax",
 "オルガン・リード楽器": "churchOrgan reedOrgan percussiveOrgan rockOrgan kfbCharmOrgan accordion harmonica",
 "声に似せたシンセ": "vocalChop voiceLeadModern kfbFormantLead",
}
TYPE_OF = {p: t for t, s in TYPES.items() for p in s.split()}

def fingerprint(x, sr, f0, t_on, t_off, full=True):
    """x: [n] か [n,2]。t_on〜t_off にのびている 1 音（高さ f0）の指紋。full=False は倍音の形だけ（短い音・曲の中の音）"""
    st = x if x.ndim > 1 else np.stack([x, x], 1); m = st.mean(1); a, b = int(t_on * sr), int(t_off * sr); d = t_off - t_on
    w0, w1 = a + int(min(0.25, 0.3 * d) * sr), a + int(min(max(0.35, 0.75 * d), d) * sr); seg = m[w0:w1]
    if len(seg) < 2048: return None
    N = 1 << int(np.ceil(np.log2(len(seg)))); N = max(N, 16384); S = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), N)); fr = sr / N
    # 高さをこまかく合わせ直す（±3%）
    best, bf = -1, f0
    for c in np.linspace(f0 * 0.97, f0 * 1.03, 61):
        e = sum(S[int(round(c * h / fr))] for h in range(1, 9) if c * h < sr / 2 - 100)
        if e > best: best, bf = e, c
    f0 = bf; H = []
    for h in range(1, 17):
        k = int(round(f0 * h / fr)); H.append(S[max(0, k - 3):k + 4].max() if f0 * h < sr / 2 - 200 else 1e-9)
    H = np.array(H); Hd = 20 * np.log10(H / (H.max() + 1e-12) + 1e-6); Hd = np.maximum(Hd, -70)
    tot = np.sum(S ** 2) + 1e-12; harm = 0.0
    for h in range(1, 41):
        k = int(round(f0 * h / fr))
        if k + 4 < len(S): harm += np.sum(S[max(0, k - 4):k + 5] ** 2)
    f = np.arange(len(S)) * fr; cen = float(np.sum(f * S ** 2) / tot / f0)
    odd = 10 * np.log10(np.sum(H[0::2][1:] ** 2) + 1e-12); even = 10 * np.log10(np.sum(H[1::2] ** 2) + 1e-12)
    slope = float(np.polyfit(np.log2(np.arange(1, 17)), Hd, 1)[0])
    out = {f"h{i + 1}": float(Hd[i]) for i in range(16)}
    out.update(cen=float(np.log2(max(cen, 0.5))), odd_even=float(np.clip(odd - even, -30, 30)), slope=slope, noise=float(10 * np.log10(max(1 - harm / tot, 1e-4))))
    if not full: return out
    hop = 256; e = np.sqrt(np.convolve(m ** 2, np.ones(1024) / 1024, "same"))[::hop] + 1e-9; t = np.arange(len(e)) * hop / sr
    seg_e = e[(t >= t_on - 0.02) & (t < t_off)]; pk = seg_e.max(); edb = 20 * np.log10(seg_e / pk)
    i10 = np.argmax(seg_e >= 0.1 * pk); i90 = np.argmax(seg_e >= 0.9 * pk); out["attack"] = float(np.log10(max((i90 - i10) * hop / sr, 0.003)))
    def at(s): 
        i = int((s + 0.02) * sr / hop); return float(max(edb[min(i, len(edb) - 1)], -60))
    out["d05"], out["d10"], out["d19"] = at(min(0.5, d * 0.25)), at(min(1.0, d * 0.5)), at(d * 0.95)
    rel = e[(t >= t_off) & (t < t_off + 1.4)]; lv = 20 * np.log10(rel / max(seg_e[-1], pk * 0.01)); w = np.where(lv < -20)[0]; out["release"] = float(np.log10(max((w[0] * hop / sr) if len(w) else 1.4, 0.01)))
    # 明るさの時間変化（はじめ 0.08 秒と、うしろ）
    def cent(a_, b_):
        s_ = m[a_:b_]
        if len(s_) < 512: return cen
        Z = np.abs(np.fft.rfft(s_ * np.hanning(len(s_)))); ff = np.fft.rfftfreq(len(s_), 1 / sr); return float(np.sum(ff * Z ** 2) / (np.sum(Z ** 2) + 1e-12) / f0)
    out["bright_move"] = float(np.log2(max(cent(a, a + int(0.08 * sr)), 0.5)) - np.log2(max(cent(w0, w1), 0.5)))
    se = e[(t >= t_on + 0.3) & (t < t_off - 0.1)]
    if len(se) > 40:
        z = 20 * np.log10(se) ; z = z - np.convolve(np.pad(z, 20, mode="edge"), np.ones(41) / 41, "valid"); out["wobble"] = float(np.log10(max(np.std(z), 0.01)))
    else: out["wobble"] = -2.0
    mid = st[w0:w1].mean(1); side = (st[w0:w1, 0] - st[w0:w1, 1]) / 2; out["width"] = float(10 * np.log10((np.mean(side ** 2) + 1e-12) / (np.mean(mid ** 2) + 1e-12))); out["width"] = max(out["width"], -50)
    return out

def embed(mono16k):
    """聞き分けモデル（AST）が音を聞いたときの「まとめ」（768 この数字）。音色どうしの近さを測るのに使う"""
    import torch
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import stage4 as S4
    fe, m, _ = S4._model(); seg = np.asarray(mono16k, dtype=np.float32); seg = seg / (np.abs(seg).max() + 1e-9) * 0.5
    with torch.no_grad(): return m.audio_spectrogram_transformer(**fe(seg, sampling_rate=16000, return_tensors="pt")).pooler_output[0].numpy()

KEYS_H = [f"h{i}" for i in range(1, 17)] + ["cen", "odd_even", "slope", "noise"]
KEYS_F = KEYS_H + ["attack", "d05", "d10", "d19", "release", "bright_move", "wobble", "width"]
WEIGHT = {**{f"h{i}": 0.5 for i in range(1, 17)}, "cen": 2, "odd_even": 1.5, "slope": 1.5, "noise": 1.5, "attack": 2, "d05": 1.5, "d10": 1.5, "d19": 2, "release": 1.5, "bright_move": 1.5, "wobble": 1, "width": 0.7}

class Table:
    def __init__(self, tb):
        self.tb = tb; self.names = list(tb["patches"])
        def mat(key, keys): return np.array([[tb["patches"][n][key].get(k, 0.0) for k in keys] for n in self.names])
        self.F = mat("c4", KEYS_F); self.mu = self.F.mean(0); self.sd = self.F.std(0) + 1e-6
        self.H = {k: mat(k, KEYS_H) for k in ("c4", "c3", "c5")}; self.muH = self.H["c4"].mean(0); self.sdH = self.H["c4"].std(0) + 1e-6
        E = tb.get("emb", {}); self.en = [n for n in self.names if n in E]
        if self.en:
            X = np.array([E[n] for n in self.en]); self.emu = X.mean(0); self.esd = X.std(0) + 1e-6; X = (X - self.emu) / self.esd; self.EX = X / np.linalg.norm(X, axis=1, keepdims=True)
    def near_emb(self, e, k=5, skip=None):
        v = (np.asarray(e) - self.emu) / self.esd; v = v / (np.linalg.norm(v) + 1e-9); sim = self.EX @ v
        order = [i for i in np.argsort(-sim) if self.en[i] != skip][:k]
        return [(self.en[i], float(1 - sim[i]), TYPE_OF.get(self.en[i], "そのほか")) for i in order]
    def near(self, fp, full=True, skip=None, k=5, reg=None):
        keys = KEYS_F if full else KEYS_H; w = np.array([WEIGHT[q] for q in keys]); v = np.array([fp.get(q, 0.0) for q in keys])
        if full: D = np.sqrt((((self.F - v) / self.sd) ** 2 * w).sum(1) / w.sum())
        else:
            regs = [reg] if reg else ["c3", "c4", "c5"]; D = np.min([np.sqrt((((self.H[r] - v) / self.sdH) ** 2 * w).sum(1) / w.sum()) for r in regs], axis=0)
        order = [i for i in np.argsort(D) if self.names[i] != skip][:k]
        return [(self.names[i], float(D[i]), TYPE_OF.get(self.names[i], "そのほか")) for i in order]
    def vote(self, nn):
        sc = {}
        for n, d, t in nn: sc[t] = sc.get(t, 0) + 1.0 / (d + 0.15)
        return sorted(sc.items(), key=lambda z: -z[1])

COARSE = {"プラック（はじいて減る音）": "打って減る音", "ベル・鉄琴・オルゴール": "打って減る音", "エレピ・FM の鍵盤": "打って減る音", "ギター（録音の音）": "打って減る音",
          "のこぎり波のシンセ（リード・スーパーソウ）": "のびるシンセ", "矩形波・パルス波のシンセ": "のびるシンセ", "サイン波に近い丸い音": "のびるシンセ", "声に似せたシンセ": "のびるシンセ",
          "パッド（ゆっくり広がる音）": "パッド", "シンセベース": "ベース", "生のベース": "ベース", "弦（バイオリンなど）": "生楽器ののびる音", "金管": "生楽器ののびる音", "木管・サックス・笛": "生楽器ののびる音", "オルガン・リード楽器": "生楽器ののびる音"}

def describe(fp):
    """指紋を言葉にする（決まりで言い切れる分だけ。聞き分けの表は使わない）"""
    d = []
    h = [fp[f"h{i}"] for i in range(1, 11)]; oe = fp["odd_even"]
    if max(h[1:]) < -30: d.append("倍音がほとんどない（サイン波に近い）")
    elif oe >= 12: d.append("奇数の倍音だけが強い（矩形波の形）")
    elif fp["slope"] > -9 and np.mean(h[1:6]) > -22: d.append("倍音が上までそろっている（のこぎり波の形）")
    else: d.append("倍音が上へ行くほど弱い（やわらかい音・フィルターで丸めた音）")
    if "attack" in fp:
        a = 10 ** fp["attack"]; d.append("立ち上がりが速い（%d ミリ秒）" % (a * 1000) if a < 0.03 else ("立ち上がりがゆっくり（%.2f 秒）" % a if a > 0.12 else "立ち上がりはふつう（%d ミリ秒）" % (a * 1000)))
        d.append("鳴らしている間に減っていく（プラック・ベル・ピアノの形）" if fp["d10"] <= -9 else "鳴らしている間はのびる")
        if fp["bright_move"] >= 0.6: d.append("出だしだけ明るく、すぐ丸くなる")
        if 10 ** fp["wobble"] >= 1.2: d.append("大きさがうねる（少しずらした波を重ねた音）")
        if fp["width"] >= -10: d.append("左右に広い")
    if fp["noise"] >= -4: d.append("倍音からはずれた音が多い（金属っぽい・ざらついた・重ねた音）")
    return d

def cmd_learn(folder, outp):
    tb = {"patches": {}}
    for nf in sorted(glob.glob(os.path.join(folder, "pt*.names"))):
        wav = nf[:-6] + ".wav"
        if not os.path.exists(wav): continue
        x, sr = sf.read(wav); names = json.load(open(nf))
        for i, n in enumerate(names):
            o = i * SLOT; seg = x[int(o * sr):int((o + SLOT) * sr)]
            if len(seg) < sr * 3 or np.abs(seg).max() < 1e-4: print("  音が出ていない:", n); continue
            c4 = fingerprint(seg, sr, 261.63, 0.5, 2.5); c3 = fingerprint(seg, sr, 130.81, 3.5, 4.0, False); c5 = fingerprint(seg, sr, 523.25, 4.5, 5.0, False)
            if c4 is None: continue
            tb["patches"][n] = {"c4": c4, "c3": c3 or c4, "c5": c5 or c4, "type": TYPE_OF.get(n, "そのほか")}
    if os.path.exists(outp):                      # 聞き分けモデルの埋め込み（時間がかかるので、前に取った分は使い回す）
        old = json.load(open(outp)).get("emb", {}); tb["emb"] = {n: old[n] for n in tb["patches"] if n in old}
    else: tb["emb"] = {}
    todo = [n for n in tb["patches"] if n not in tb["emb"]]
    if todo:
        import librosa
        for nf in sorted(glob.glob(os.path.join(folder, "pt*.names"))):
            names = json.load(open(nf))
            if not any(n in todo for n in names): continue
            x, sr = sf.read(nf[:-6] + ".wav"); mono = librosa.resample(x.mean(1).astype(np.float32), orig_sr=sr, target_sr=16000)
            for i, n in enumerate(names):
                if n in todo: tb["emb"][n] = [round(float(v), 3) for v in embed(mono[int(i * SLOT * 16000):int((i * SLOT + 7.4) * 16000)])]
    json.dump(tb, open(outp, "w"), ensure_ascii=False); print("指紋を取った音色:", len(tb["patches"]), "・埋め込み:", len(tb["emb"]))

def cmd_eval(tp):
    T = Table(json.load(open(tp))); ok = tot = 0; per = {}
    for n in T.names:
        t = TYPE_OF.get(n)
        if not t: continue
        nn = T.near(T.tb["patches"][n]["c4"], True, skip=n); g = T.vote(nn)[0][0]; tot += 1; ok += g == t; a, b = per.get(t, (0, 0)); per[t] = (a + (g == t), b + 1)
    print(f"■ 種類の当たり具合（その音色を表から抜いて、残りから答える）: {tot} 音色のうち {ok}（{100 * ok / tot:.0f}%）")
    for t, (a, b) in sorted(per.items(), key=lambda z: -z[1][0] / z[1][1]): print(f"    {t}: {a}/{b}")
    if T.en:
        for nm, use_h in (("聞き分けモデルの埋め込みだけ", False), ("指紋と埋め込みの両方", True)):
            okf = okc = t3 = tot = 0
            for n in T.en:
                t = TYPE_OF.get(n)
                if not t: continue
                ne = T.near_emb(T.tb["emb"][n], k=len(T.en), skip=n); sc_ = {q[0]: q[1] for q in ne}
                if use_h:
                    nh = T.near(T.tb["patches"][n]["c4"], True, skip=n, k=len(T.names)); dh = {q[0]: q[1] for q in nh}; a_ = np.array(list(sc_.values())); b_ = np.array(list(dh.values()))
                    sc_ = {q: 2 * (sc_[q] - a_.mean()) / a_.std() + (dh.get(q, b_.mean()) - b_.mean()) / b_.std() for q in sc_}
                order = sorted(sc_, key=sc_.get)[:5]; v1 = {}; v2 = {}
                for r, q in enumerate(order):
                    tq = TYPE_OF.get(q)
                    if tq: v1[tq] = v1.get(tq, 0) + 1 / (r + 1); v2[COARSE[tq]] = v2.get(COARSE[tq], 0) + 1 / (r + 1)
                if not v1: continue
                tot += 1; okf += max(v1, key=v1.get) == t; okc += max(v2, key=v2.get) == COARSE[t]; t3 += t in sorted(v1, key=v1.get, reverse=True)[:3]
            print(f"■ {nm}: こまかい種類（15）{100 * okf / tot:.0f}%・3 位までに入る {100 * t3 / tot:.0f}%・大きな分け方（5）{100 * okc / tot:.0f}%")
    for reg in ("c3", "c5"):
        hit = top3 = ty = 0
        for n in T.names:
            nn = T.near(T.tb["patches"][n][reg], False, reg="c4"); hit += nn[0][0] == n; top3 += n in [q[0] for q in nn[:3]]; ty += T.vote(nn)[0][0] == TYPE_OF.get(n, "そのほか")
        print(f"■ 高さを変えて確かめる（{'ド3' if reg == 'c3' else 'ド5'} の音を、ド4 の表に当てる。倍音の形だけ）: 同じ音色が 1 位 {100 * hit / len(T.names):.0f}%・3 位まで {100 * top3 / len(T.names):.0f}%・種類が合う {100 * ty / len(T.names):.0f}%")

def cmd_what(tp, path, stem=None):
    import librosa
    T = Table(json.load(open(tp)))
    if stem:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import analyze as A
        st = A.separate(A.load_audio(path)); x = np.asarray(st[stem]); x = x.T if x.shape[0] < x.shape[1] else x; sr = A.SR
    else: x, sr = sf.read(path)
    m = x.mean(1) if x.ndim > 1 else x
    f0, vf, _ = librosa.pyin(m.astype(np.float32), fmin=40, fmax=1600, sr=sr, frame_length=4096, hop_length=512); t = np.arange(len(f0)) * 512 / sr
    semi = 69 + 12 * np.log2(np.where(vf, f0, np.nan) / 440); runs = []; i = 0
    while i < len(semi):
        if np.isfinite(semi[i]):
            j = i
            while j + 1 < len(semi) and np.isfinite(semi[j + 1]) and abs(semi[j + 1] - np.nanmedian(semi[i:j + 1])) < 0.4: j += 1
            if (j - i) * 512 / sr >= 0.3: runs.append((t[i], t[j], float(np.nanmedian(semi[i:j + 1]))))
            i = j + 1
        else: i += 1
    runs.sort(key=lambda r: -(r[1] - r[0])); votes = {}; pv = {}; used = 0
    for a, b, s in runs[:40]:
        fp = fingerprint(x, sr, 440 * 2 ** ((s - 69) / 12), a, b, full=False)
        if fp is None: continue
        nn = T.near(fp, False); used += 1
        for ty, sc in T.vote(nn)[:2]: votes[ty] = votes.get(ty, 0) + sc
        for n, d, ty in nn[:3]: pv[n] = pv.get(n, 0) + 1 / (d + 0.15)
    if T.en:                                   # 聞き分けモデルの埋め込みで（10 秒ずつ。重なった音でも使える）
        import librosa
        m16 = librosa.resample(m.astype(np.float32), orig_sr=sr, target_sr=16000); ev = {}; ep = {}; ec = {}; lv = []
        segs = [m16[a_:a_ + 160000] for a_ in range(0, max(1, len(m16) - 80000), 160000)]; rms = [np.sqrt(np.mean(q ** 2)) for q in segs]; thr = max(rms) * 10 ** (-20 / 20) if rms else 0
        for q, r_ in zip(segs, rms):
            if r_ < thr or len(q) < 32000: continue
            nn = T.near_emb(embed(q), k=5)
            for r, (n, d_, ty) in enumerate(nn):
                ep[n] = ep.get(n, 0) + 1 / (r + 1)
                if ty in COARSE: ev[ty] = ev.get(ty, 0) + 1 / (r + 1); ec[COARSE[ty]] = ec.get(COARSE[ty], 0) + 1 / (r + 1)
        te = sum(ev.values()) + 1e-9; tc = sum(ec.values()) + 1e-9
        print(f"■ {os.path.basename(path)}{'（分けた音: ' + stem + '）' if stem else ''}: 聞き分けモデルの埋め込みで（10 秒ずつ）")
        print("  大きな分け方: " + "・".join(f"{ty} {100 * v / tc:.0f}%" for ty, v in sorted(ec.items(), key=lambda z: -z[1])[:3]))
        print("  種類: " + "・".join(f"{ty} {100 * v / te:.0f}%" for ty, v in sorted(ev.items(), key=lambda z: -z[1])[:4]))
        print("  近い音色: " + "・".join(n for n, _ in sorted(ep.items(), key=lambda z: -z[1])[:6]))
    tot = sum(votes.values()) + 1e-9
    print(f"  のびている音 {used} こ（倍音の形だけ）で答えると:")
    print("  種類: " + "・".join(f"{ty} {100 * v / tot:.0f}%" for ty, v in sorted(votes.items(), key=lambda z: -z[1])[:4]))
    print("  近い音色: " + "・".join(n for n, _ in sorted(pv.items(), key=lambda z: -z[1])[:6]))
    return votes, pv

if __name__ == "__main__":
    c = sys.argv[1]
    if c == "learn": cmd_learn(sys.argv[2], sys.argv[3])
    elif c == "eval": cmd_eval(sys.argv[2])
    elif c == "what":
        if len(sys.argv) > 4 and "," in sys.argv[4]:      # 分けた音をいくつも: 1 回だけ分けて、順に答える
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import analyze as A, tempfile
            st = A.separate(A.load_audio(sys.argv[3])); d = tempfile.mkdtemp()
            for k in sys.argv[4].split(","):
                x = np.asarray(st[k]); x = x.T if x.shape[0] < x.shape[1] else x; sf.write(f"{d}/{k}.wav", x, A.SR)
            del st
            for k in sys.argv[4].split(","): print(f"【分けた音: {k}】"); cmd_what(sys.argv[2], f"{d}/{k}.wav"); os.remove(f"{d}/{k}.wav")
        else: cmd_what(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
