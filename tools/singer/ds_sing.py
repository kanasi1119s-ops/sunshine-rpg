#!/usr/bin/env python3
"""作曲ソフトの歌（"vocals" の書き方）を、DiffSinger の声で歌わせる（sing.py から呼ばれる）。

歌の書き方は今までと同じ。"voice" に "ds:<声の名前>" を書くと DiffSinger になる。
  {"voice": "ds:ruko", "dsSpeaker": "Normal", "notes": "R:4 D4:1:よ ...", ...}
  - dsSpeaker: 声の種類（ルコは Normal / Soft）。dsSpeakerMix: {"Normal": 0.6, "Soft": 0.4} で混ぜる
  - dsGender: 声の太さ（-1〜1。+ で細く若く、- で太く大人っぽく。音の高さは変わらない）
  - dsTension: 声の張り（足し算。+ で張りのある声、- でやわらかい声）。強弱の地図 "dynamics" も張りに足す
  - dsSteps: AI の書き込みの回数（多いほどていねい・遅い。既定 20）
音程の線（しゃくり・ビブラート・つなぎ）は sing.py と同じものを使う。
フレーズ（休みで区切られたまとまり）ごとに作り、結果は ~/.cache/sunshine-singer/ds にためる（同じフレーズは作り直さない）。
"""
import os, sys, json, hashlib
import numpy as np
from scipy import signal

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sing as S
import ds_engine as D

CACHE = os.path.expanduser("~/.cache/sunshine-singer/ds")
_banks = {}

def bank(name):
    if name not in _banks:
        for r in S.bank_roots():
            p = os.path.join(r, "ds", name)
            if os.path.exists(os.path.join(p, "dsconfig.yaml")):
                _banks[name] = D.DSBank(p); break
        else:
            raise FileNotFoundError(f"DiffSinger の声「{name}」が見つかりません（SUNSHINE_VOICEBANKS の下の ds/{name}/dsconfig.yaml）")
    return _banks[name]

def build_vocal_ds(vdef, bpm, sr_out, total_sec=None, seed=1, tempo=None, beats=4):
    b = bank(vdef["voice"].split(":", 1)[1])
    notes = S.parse_notes(vdef["notes"])
    b2s = S.tempo_clock(bpm, tempo, beats)
    rng = np.random.default_rng(seed)
    # 1) 歌う音をまとめる（sing.py と同じ。「ー」は前の音をのばして音程だけ変える）
    pieces, prev_rest = [], True
    for n in notes:
        s, e = b2s(n["beat"]), b2s(n["beat"] + n["len"])
        if n["lyric"] is None: prev_rest = True; continue
        if n["lyric"] in ("ー", "-", "~") and pieces and not prev_rest:
            pieces[-1]["end"] = e; pieces[-1]["events"].append((s, e, n["midi"], n["vel"], n["fl"], n["beat"])); continue
        pieces.append({"lyric": n["lyric"], "start": s, "end": e, "events": [(s, e, n["midi"], n["vel"], n["fl"], n["beat"])], "head": prev_rest, "beat": n["beat"]})
        prev_rest = False
    if not pieces: return np.zeros(int(sr_out * (total_sec or 1)))
    total = max(total_sec or 0, max(p["end"] for p in pieces) + 1.5)
    # 2) 音程の線（sing.py と同じ作り方）
    vib0 = float(vdef.get("vibrato", 16)); scoop0 = float(vdef.get("scoop", 0.0))
    events, prevm = [], None
    for p in pieces:
        for k, (s, e, m, v, fl, bt) in enumerate(p["events"]):
            vb = S.interp_map(vdef.get("vibratoMap"), bt, vib0) * (1.6 if "~" in fl else 1.0)
            sc = 0.0
            if "/" in fl: sc = 1.4
            elif scoop0 > 0 and k == 0 and (p["head"] or (prevm is not None and m - prevm >= 4 and e - s >= 0.35)): sc = scoop0
            events.append({"s": s, "e": e, "m": m, "fl": fl, "vib": vb, "scoop": sc}); prevm = m
    t, semis = S.pitch_curve(events, total, rng, vdef)
    semis = semis + float(vdef.get("transpose", 0))
    hz = 440.0 * 2 ** ((semis - 69) / 12)
    tms_grid = t * 1000.0
    f0_at = lambda ms: np.interp(ms, tms_grid, hz)
    # 3) フレーズごとに歌わせる
    out = np.zeros(int(total * sr_out) + sr_out)
    phrases, cur = [], []
    for i, p in enumerate(pieces):
        if p["head"] and cur: phrases.append(cur); cur = []
        cur.append(i)
    if cur: phrases.append(cur)
    tr = float(vdef.get("transpose", 0))
    opts_base = {"speaker": vdef.get("dsSpeaker"), "speakerMix": vdef.get("dsSpeakerMix"),
                 "gender": float(vdef.get("dsGender", 0.0)), "steps": int(vdef.get("dsSteps", 20)),
                 "depth": float(vdef.get("dsDepth", 1.0))}
    os.makedirs(CACHE, exist_ok=True)
    win = os.environ.get("DS_WINDOW")          # 試し聞き用: "始まり秒,終わり秒" の間のフレーズだけ作る
    if win: wa, wb = (float(x) for x in win.split(","))
    for ph in phrases:
        if win and not (pieces[ph[0]]["start"] < wb and pieces[ph[-1]]["end"] > wa): continue
        words = []
        for i in ph:
            p = pieces[i]
            phs = b.phonemes_of(p["lyric"])
            if phs is None:
                print(f"注意: DiffSinger の辞書に「{p['lyric']}」がありません。「あ」で代わりに歌います", file=sys.stderr)
                phs = b.phonemes_of("あ")
            words.append({"ms": p["start"] * 1000, "end": p["end"] * 1000, "midi": int(round(p["events"][0][2] + tr)), "phs": phs, "beat": p["beat"]})
        # 歌い終わりは少しのばして、自然に消えるように
        words[-1]["end"] += 60.0
        placed, end_ms = b.place(words, opts_base)
        # 強弱の地図と「!」「?」を、声の張り（tension）に足す
        fm = b.frame_ms; t0 = placed[0][1] - D.HEAD * fm
        nfr = int((end_ms - t0) / fm) + D.HEAD + D.TAIL + 4
        fr_ms = t0 + np.arange(nfr) * fm
        beat_of = lambda ms: np.interp(ms, [w["ms"] for w in words], [w["beat"] for w in words])
        dyn = np.array([S.interp_map(vdef.get("dynamics"), bt, 0.0) for bt in beat_of(fr_ms)])
        vel = np.ones(nfr)
        for i in ph:
            for (s, e, m, v, fl, bt) in pieces[i]["events"]:
                vel[(fr_ms >= s * 1000) & (fr_ms < e * 1000)] = v
        ten = float(vdef.get("dsTension", 0.0)) + 1.6 * dyn + 4.0 * (vel - 1.0)
        opts = {**opts_base, "tension": ten}
        key = hashlib.sha1(json.dumps([b.root, placed, end_ms, list(np.round(f0_at(fr_ms), 2)), list(np.round(ten, 3)),
                                       {k: v for k, v in opts_base.items()}], default=str).encode()).hexdigest()[:20]
        cp = os.path.join(CACHE, key + ".npz")
        if os.path.exists(cp):
            z = np.load(cp); w, st, sr = z["w"], float(z["st"]), int(z["sr"])
        else:
            w, st, sr = b.sing(placed, end_ms, f0_at, opts)
            np.savez(cp, w=w, st=st, sr=sr)
        # 前後のはみ出しを、ふわっと消す
        n = len(w); f = min(n // 4, int(0.03 * sr))
        if f > 0: w = w.copy(); w[:f] *= np.linspace(0, 1, f); w[-f:] *= np.linspace(1, 0, f)
        if sr != sr_out: w = signal.resample_poly(w, sr_out, sr)
        n0 = int(round(st / 1000 * sr_out))
        if n0 < 0: w = w[-n0:]; n0 = 0
        m_ = min(len(w), len(out) - n0)
        if m_ > 0: out[n0:n0 + m_] += w[:m_]
    return out[: int(total * sr_out)]
