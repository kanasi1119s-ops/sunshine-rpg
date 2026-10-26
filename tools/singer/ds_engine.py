#!/usr/bin/env python3
"""DiffSinger（AI の歌声）を、OpenUtau の画面を使わずに命令から動かす部品。

2026-10-27 人間「（作曲ソフトに）使えるようにできない？」→ OpenUtau＋DiffSinger を選んだ。
OpenUtau（stakira/OpenUtau・MIT）の DiffSinger の書き出し（DiffSingerRenderer.cs ほか）と同じ順番で、
onnx のモデルを onnxruntime で直接動かす。

  1. 長さモデル（dur）   … 子音をどれだけ前から入れるかを決める（音符の頭に母音が来るようにそろえる）
  2. 変化量モデル（variance）… 強さ（energy）・息（breathiness）などの線を予測する
  3. 音響モデル（acoustic）… 音素・長さ・音程（f0）から、声のメル（音の地図）を作る
  4. ボコーダー（vocoder） … メルと f0 から波形にする

音程（f0）は、sing.py が作る音程の線（しゃくり・ビブラート・なめらかなつなぎ）をそのまま渡す。
つまり「どう歌うか」は今までどおり作曲ソフトの歌の書き方で決め、「声そのもの」だけを AI にする。

ボイスバンクの置き場所: SUNSHINE_VOICEBANKS（sing.py と同じ）の下の ds/<名前>/（dsconfig.yaml がある所）。
ボコーダーは ds/_vocoders/<名前>/vocoder.yaml。音源・ボコーダーはリポジトリに入れない（規約で再配布できないものがあるため）。
"""
import os, sys, glob
import numpy as np
import yaml
import onnxruntime as ort

HEAD, TAIL = 8, 8          # OpenUtau と同じ前後の余白（フレーム）

def _sess(path):
    o = ort.SessionOptions()
    o.intra_op_num_threads = int(os.environ.get("DS_THREADS", "2")); o.inter_op_num_threads = 1
    o.log_severity_level = 3
    return ort.InferenceSession(path, o, providers=["CPUExecutionProvider"])

def _load_phonemes(path):
    if path.endswith(".json"):
        import json
        return {k: int(v) for k, v in json.load(open(path, encoding="utf-8")).items()}
    return {l.strip(): i for i, l in enumerate(open(path, encoding="utf-8").read().splitlines()) if l.strip() != "" or i == 0}

def _load_langs(path):
    if not path or not os.path.exists(path): return {}
    import json
    return {k: int(v) for k, v in json.load(open(path, encoding="utf-8")).items()}

class Part:
    """dsconfig.yaml 1 つ（音響・長さ・音程・変化量のどれか）"""
    def __init__(self, folder):
        self.dir = folder
        self.cfg = yaml.safe_load(open(os.path.join(folder, "dsconfig.yaml"), encoding="utf-8")) or {}
        c = self.cfg
        self.ph = _load_phonemes(os.path.join(folder, c.get("phonemes", "phonemes.txt")))
        self.langs = _load_langs(os.path.join(folder, c["languages"])) if c.get("languages") else {}
        self.frame_ms = 1000.0 * c.get("hop_size", 512) / c.get("sample_rate", 44100)
        self.spk = {}
        for s in c.get("speakers") or []:
            p = os.path.join(folder, s + ".emb")
            if os.path.exists(p): self.spk[s] = np.fromfile(p, dtype="<f4")
        self.sess = {}
        self.dict = {}
        dd = os.path.join(folder, "dsdict.yaml")
        if os.path.exists(dd): self.dict = yaml.safe_load(open(dd, encoding="utf-8")) or {}

    def s(self, key):
        if key not in self.sess: self.sess[key] = _sess(os.path.join(self.dir, self.cfg[key]))
        return self.sess[key]

    def tok(self, phs):
        out = []
        for p in phs:
            if p in self.ph: out.append(self.ph[p]); continue
            q = p.split("/", 1)[-1]
            if q in self.ph: out.append(self.ph[q]); continue
            raise KeyError(f"音素「{p}」がこのモデルにありません（{self.dir}）")
        return np.array(out, dtype=np.int64)[None]

    def lang_ids(self, phs):
        return np.array([self.langs.get(p.split("/")[0] if "/" in p else "", 0) for p in phs], dtype=np.int64)[None]

    def spk_embed(self, n, name=None, mix=None):
        """n フレーム（または音素）ぶんの話者の埋め込み [1, n, hidden]。mix={"名前": 割合} で声を混ぜられる"""
        if not self.spk: return None
        def find(nm):
            for k, v in self.spk.items():
                if k == nm or k.endswith("_" + nm) or k.endswith("/" + nm): return v
            raise KeyError(f"声の種類「{nm}」がありません（あるもの: {[k.rsplit('/', 1)[-1] for k in self.spk]}）")
        if mix:
            v = sum(find(k) * float(w) for k, w in mix.items()) / max(1e-9, sum(float(w) for w in mix.values()))
        else:
            v = find(name) if name else next(iter(self.spk.values()))
        return np.repeat(v[None, None, :], n, axis=1).astype(np.float32)

    def accel(self, sess, inputs, steps, depth=1.0):
        names = {i.name for i in sess.get_inputs()}
        c = self.cfg
        if c.get("use_continuous_acceleration"):
            if "depth" in names and (c.get("use_variable_depth") or c.get("use_shallow_diffusion")):
                inputs["depth"] = np.array([min(depth, float(c.get("max_depth", 1.0)))], np.float32)
            if "steps" in names: inputs["steps"] = np.array([steps], np.int64)
        else:
            sp = max(1, 1000 // steps)
            while 1000 % sp and sp > 1: sp -= 1
            if "speedup" in names: inputs["speedup"] = np.array([sp], np.int64)
            if "depth" in names and (c.get("use_variable_depth") or c.get("use_shallow_diffusion")):
                d = int(round(min(depth, float(c.get("max_depth", 1000)) / 1000) * 1000)); d = max(sp, d // sp * sp)
                inputs["depth"] = np.array([d], np.int64)

def run(sess, inputs):
    names = [i.name for i in sess.get_inputs()]
    feed = {k: v for k, v in inputs.items() if k in names}
    miss = [n for n in names if n not in feed]
    if miss: raise KeyError(f"モデルの入力が足りません: {miss}")
    outs = sess.run(None, feed)
    return {o.name: v for o, v in zip(sess.get_outputs(), outs)}

class Vocoder:
    def __init__(self, folder):
        self.cfg = yaml.safe_load(open(os.path.join(folder, "vocoder.yaml"), encoding="utf-8"))
        self.sess = _sess(os.path.join(folder, self.cfg["model"]))
        self.sr = int(self.cfg.get("sample_rate", 44100)); self.hop = int(self.cfg.get("hop_size", 512))
        self.mel_base = str(self.cfg.get("mel_base", "10"))

class DSBank:
    def __init__(self, root, vocoder_dir=None, vocoder="bigvgan"):
        self.root = root
        self.ac = Part(root)
        self.dur = self.var = self.pitch = None
        for y in glob.glob(os.path.join(root, "*", "dsconfig.yaml")):
            p = Part(os.path.dirname(y)); c = p.cfg
            if c.get("dur") and not self.dur: self.dur = p
            if c.get("variance") and not self.var: self.var = p
            if c.get("pitch") and not self.pitch: self.pitch = p
        self.voc = None
        if vocoder == "bigvgan":       # 商用可（MIT）の BigVGAN で鳴らす（既定）。ds_bigvgan.py
            self.frame_ms = self.ac.frame_ms
            vname = None
        else:
            vname = self.ac.cfg.get("vocoder", "")
        cands = [vocoder_dir] if vocoder_dir else []
        cands += [os.path.join(root, vname or ""), os.path.join(os.path.dirname(root), "_vocoders", vname or "")]
        if vname is not None:
            vd = next((c for c in cands if c and vname and os.path.exists(os.path.join(c, "vocoder.yaml"))), None)
            if not vd: raise FileNotFoundError(f"ボコーダー「{vname}」が見つかりません（{os.path.dirname(root)}/_vocoders/{vname}/vocoder.yaml）")
            self.voc = Vocoder(vd)
        self.frame_ms = self.ac.frame_ms
        # 日本語の辞書（かな → 音素）と、音素の種類（母音かどうか）
        self.g2p = {}; self.vowels = {"SP", "AP"}
        for part in (self.dur, self.var, self.ac):
            if part and part.dict:
                for e in part.dict.get("entries", []) or []:
                    self.g2p.setdefault(str(e["grapheme"]), list(e["phonemes"]))
                for sy in part.dict.get("symbols", []) or []:
                    if sy.get("type") == "vowel": self.vowels.add(str(sy["symbol"]))

    def is_vowel(self, ph):
        return ph in self.vowels or ph.split("/")[-1] in self.vowels

    def phonemes_of(self, kana):
        """かな 1 音 → 音素の列（辞書にない時は None）"""
        for key in (kana, kana.replace("ゔ", "ヴ")):
            if key in self.g2p: return list(self.g2p[key])
        return None

    # ---------- 1. 長さ（子音の入り方） ----------
    def place(self, words, f_ms):
        """words: [{"ms": 音符の頭（ミリ秒）, "end": 終わり, "midi": int, "phs": [音素]}]（1 フレーズ）
        → [(音素, 始まりms)]、最後の終わり ms"""
        frame = self.frame_ms
        groups = [{"ms": words[0]["ms"] - 500.0, "midi": words[0]["midi"], "phs": ["SP"]}]
        for w in words:
            phs = w["phs"]; vi = next((i for i, p in enumerate(phs) if self.is_vowel(p)), 0)
            groups[-1]["phs"] += phs[:vi]
            groups.append({"ms": w["ms"], "midi": w["midi"], "phs": phs[vi:] or phs[-1:]})
        end_ms = words[-1]["end"]
        allph = [p for g in groups for p in g["phs"]]
        if self.dur is not None:
            d = self.dur
            word_div = np.array([[len(g["phs"]) for g in groups]], np.int64)
            pos = [g["ms"] for g in groups] + [end_ms]
            fr = [int(round(b / frame)) - int(round(a / frame)) for a, b in zip(pos, pos[1:])]
            word_dur = np.array([[max(1, x) for x in fr]], np.int64)
            li = {"tokens": d.tok(allph), "word_div": word_div, "word_dur": word_dur}
            if d.langs: li["languages"] = d.lang_ids(allph)
            lo = run(d.s("linguistic"), li)
            di = {"encoder_out": lo["encoder_out"], "x_masks": lo["x_masks"],
                  "ph_midi": np.array([[g["midi"] for g in groups for _ in g["phs"]]], np.int64),
                  "word_div": word_div, "word_dur": word_dur}
            e = d.spk_embed(len(allph), f_ms.get("speaker"), f_ms.get("speakerMix"))
            if e is not None: di["spk_embed"] = e
            dur = run(d.s("dur"), di)
            dur = np.array(next(iter(dur.values()))).reshape(-1).astype(float)
        else:
            dur = np.array([(90.0 / frame) if not self.is_vowel(p) else 10.0 for p in allph])
        # OpenUtau と同じそろえ方: 最初の子音は長さそのまま、あとは音符の間に収まるよう伸び縮み
        starts = []
        idx = [0]
        for g in groups: idx.append(idx[-1] + len(g["phs"]))
        g0 = list(range(1, idx[1]))                       # 最初の SP をのぞく、歌い出し前の子音
        t = words[0]["ms"] - sum(dur[i] for i in g0) * frame
        for i in g0: starts.append((allph[i], t)); t += dur[i] * frame
        for k in range(1, len(groups)):
            a, b = idx[k], idx[k + 1]
            nxt_ms = groups[k + 1]["ms"] if k + 1 < len(groups) else end_ms
            seg = dur[a:b]; nxt_cons = []
            # 次の言葉の子音はこのグループの最後に入っている → 次の音符の頭で終わるように
            ratio = (nxt_ms - groups[k]["ms"]) / max(1e-6, seg.sum())
            t = groups[k]["ms"]
            for i in range(a, b): starts.append((allph[i], t)); t += dur[i] * ratio
        return starts, end_ms

    # ---------- 2〜4. 変化量 → 音響 → ボコーダー ----------
    def sing(self, phones, end_ms, f0_at, opts=None):
        """phones: [(音素, 始まりms)]、f0_at(ms の配列) → Hz。返り値: (波形, 始まりms, sr)"""
        opts = opts or {}
        fm = self.frame_ms
        t0 = phones[0][1]
        segs = [("SP", HEAD * fm)]
        for i, (p, s) in enumerate(phones):
            e = phones[i + 1][1] if i + 1 < len(phones) else end_ms
            segs.append((p, max(0.0, e - s)))
        segs.append(("SP", TAIL * fm))
        acc, prev, durs = 0.0, 0, []
        for _, d in segs:
            acc += d; f = int(round(acc / fm + 0.5)); durs.append(f - prev); prev = f
        phs = [p for p, _ in segs]
        N = sum(durs)
        tms = t0 - HEAD * fm + np.arange(N) * fm
        f0 = f0_at(tms).astype(np.float32)
        midi = (69 + 12 * np.log2(np.maximum(f0, 1.0) / 440.0)).astype(np.float32)
        ac = self.ac; c = ac.cfg
        A = {"tokens": ac.tok(phs), "durations": np.array([durs], np.int64), "f0": f0[None]}
        if ac.langs: A["languages"] = ac.lang_ids(phs)
        e = ac.spk_embed(N, opts.get("speaker"), opts.get("speakerMix"))
        if e is not None: A["spk_embed"] = e
        if c.get("use_key_shift_embed"): A["gender"] = np.full((1, N), float(opts.get("gender", 0.0)), np.float32)
        if c.get("use_speed_embed"): A["velocity"] = np.full((1, N), float(opts.get("velocity", 1.0)), np.float32)
        need = [k for k in ("energy", "breathiness", "voicing", "tension") if c.get(f"use_{k}_embed")]
        if need:
            if self.var is None: raise RuntimeError("この声は変化量モデルが必要ですが、見つかりません")
            v = self.var; vc = v.cfg
            vfm = v.frame_ms
            if abs(vfm - fm) > 1e-6: raise RuntimeError("変化量モデルのフレームの長さが音響モデルとちがいます（まだ対応していません）")
            L = {"tokens": v.tok(phs)}
            if vc.get("predict_dur", True):
                vi = [i for i, p in enumerate(phs) if 0 < i < len(phs) - 1 and self.is_vowel(p)] or [len(phs) - 2]
                wd = [vi[0]] + [b - a for a, b in zip(vi, vi[1:])] + [len(phs) - vi[-1]]
                wdur, o = [], 0
                for n in wd: wdur.append(sum(durs[o:o + n])); o += n
                L["word_div"] = np.array([wd], np.int64); L["word_dur"] = np.array([wdur], np.int64)
            else:
                L["ph_dur"] = np.array([durs], np.int64)
            if v.langs: L["languages"] = v.lang_ids(phs)
            lo = run(v.s("linguistic"), L)
            V = {"encoder_out": lo["encoder_out"], "ph_dur": np.array([durs], np.int64), "pitch": midi[None]}
            kinds = [k for k in ("energy", "breathiness", "voicing", "tension") if vc.get(f"predict_{k}", k in ("energy", "breathiness"))]
            for k in kinds: V[k] = np.zeros((1, N), np.float32)
            V["retake"] = np.ones((1, N, len(kinds)), bool)
            v.accel(v.s("variance"), V, int(opts.get("varSteps", 10)))
            ev = v.spk_embed(N, opts.get("speaker"), opts.get("speakerMix"))
            if ev is not None: V["spk_embed"] = ev
            vo = run(v.s("variance"), V)
            for k in need:
                cur = np.array(vo[f"{k}_pred"]).reshape(-1)[:N].astype(np.float32)
                add = opts.get(k)          # 1 フレームずつの足し算（dB など）。強弱の地図から作る
                if add is not None: cur = cur + np.asarray(add, np.float32)[:N]
                lo_, hi_ = (-10.0, 10.0) if k == "tension" else (-96.0, 0.0)
                A[k] = np.clip(cur, lo_, hi_)[None]
        ac.accel(ac.s("acoustic"), A, int(opts.get("steps", 20)), float(opts.get("depth", 1.0)))
        mel = run(ac.s("acoustic"), A)
        mel = np.array(next(iter(mel.values())), np.float32)
        ab = str(c.get("mel_base", "10"))
        if self.voc is None:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import ds_bigvgan
            w = ds_bigvgan.vocode(ds_bigvgan.ds_to_bigvgan_interp(mel, ab))
            return w, t0 - HEAD * fm, 44100
        vb = self.voc.mel_base
        if vb == "e" and ab == "10": mel = mel * 2.30259
        elif vb == "10" and ab == "e": mel = mel * 0.434294
        w = run(self.voc.sess, {"mel": mel, "f0": f0[None]})
        w = np.array(next(iter(w.values())), np.float32).reshape(-1)
        return w, t0 - HEAD * fm, self.voc.sr
