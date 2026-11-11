"""GuitarSet（CC BY 4.0）の本物のギタリストの伴奏（comp）から、弦ごとのパートを作る。

2026-11-07 人間「（直してほしいのは）弾き方だね」「ギター、ジャンジャン弾いて欲しいの」:
  これまでのストロークは、型（D.DU.UDU）から毎回同じ本数・同じずらし・同じ強さで作っていたので機械的だった。
  ここでは、人が実際に弾いたときの
    - 弦ごとのはじく時刻（ダウン・アップの向きと、弦から弦へのずれ）
    - 何本の弦を鳴らしたか（アップは高い弦だけ、ダウンでも低い弦を外すなど、毎回ちがう）
    - 音の長さ（左手で止める・次の打つまで鳴らす）
    - 強さ（マイク録音の音量から求める）
  をそのまま使い、押さえる音だけを、こちらの曲のコードに置きかえる。

使い方（Python から）:
  from gset_to_parts import string_parts
  notes6 = string_parts(segments, chords, voicings, bpm)
  segments = [("00_Rock3-148-C_comp", 源の小節, 何小節), ...]（並べた順に、曲の小節を埋める）
  返り値は、低い弦から 6 本ぶんの notes 文字列（"R:0.31 F#2:0.42%96 ..."）。
  注意（2026-11-07）: distGuitar のパートにするときは、必ず "powerChord": false を付ける。付けないと 1 音ごとに5度と1オクターブ上が足され、
  6 本の和音が 18 音になって、歪ませたときに汚く割れる（聞き比べD〜I1 はこの状態だった）。左右を分けるときは "double": false も付ける。

データ: /tmp/gset/ann（注釈）・/tmp/gset/mic（マイク録音）。入手元 https://zenodo.org/records/3371780
"""
import json, math, os
import numpy as np
import soundfile as sf

ANN = os.environ.get("GSET_ANN", "/tmp/gset/ann")
MIC = os.environ.get("GSET_MIC", "/tmp/gset/mic")
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def midi(name):
    import re
    g = re.match(r"([A-G])([#b]?)(-?\d)", name)
    n = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}[g[1]] + (1 if g[2] == "#" else -1 if g[2] == "b" else 0)
    return n + (int(g[3]) + 1) * 12


_cache = {}


def load(base):
    if base in _cache:
        return _cache[base]
    j = json.load(open(f"{ANN}/{base}.jams"))
    notes, beats = [], []
    for a in j["annotations"]:
        if a["namespace"] == "note_midi":
            s = int(a["annotation_metadata"]["data_source"])
            for d in a["data"]:
                notes.append([d["time"], s, d["duration"]])
        elif a["namespace"] == "beat_position":
            beats = [d["time"] for d in a["data"]]
        elif a["namespace"] == "tempo":
            bpm = a["data"][0]["value"]
    notes.sort()
    # 1 打ち（ストローク）ごとにまとめる（35ms 以内に続く音は同じ打ち）
    strums, cur = [], []
    for n in notes:
        if cur and n[0] - cur[0][0] > 0.035:
            strums.append(cur); cur = []
        cur.append(n)
    if cur:
        strums.append(cur)
    # 強さ: マイク録音の、打ちの頭 60ms の音量（dB）。曲ごとの中央値を 100% とする
    # 2026-11-11: マイク録音が手元に無い演奏（Funk・Bossa・Jazz・SS は注釈だけ取ってある）は、強さを「鳴らした弦の数」から決める
    #   （本数の多い打ち＝強い打ち。時刻・向き・弦から弦へのずれ・本数は注釈からそのまま取れる）
    mic = f"{MIC}/{base}_mic.wav"
    if os.path.exists(mic):
        y, sr = sf.read(mic)
    else:
        y, sr = None, 0
    if y is not None and y.ndim > 1:
        y = y.mean(1)
    dbs = []
    for s in strums:
        if y is None:
            dbs.append(-30.0 + 1.6 * min(6, len(s))); continue
        i0 = int(s[0][0] * sr); seg = y[i0:i0 + int(0.06 * sr)]
        pre = y[max(0, i0 - int(0.03 * sr)):i0]
        e = math.sqrt(max(1e-12, float(np.mean(seg ** 2)) - 0.5 * float(np.mean(pre ** 2)) if len(pre) else float(np.mean(seg ** 2))))
        dbs.append(20 * math.log10(max(1e-6, e)))
    med = float(np.median(dbs))
    sp = 60.0 / bpm
    t0 = beats[0] if beats else 0.0
    out = []
    for s, db in zip(strums, dbs):
        ss = [x[1] for x in s]
        out.append({
            "beat": (s[0][0] - t0) / sp,  # 源の拍
            "notes": [(x[1], x[0] - s[0][0], x[2] / sp) for x in s],  # (弦, 先頭からの秒, 長さ[拍])
            "up": len(ss) >= 2 and ss[0] > ss[-1],
            "vel": max(45, min(140, 100 + (db - med) * 3.2)),
        })
    _cache[base] = (out, bpm)
    return out, bpm


def string_parts(segments, chords, voicings, bpm, vel_scale=1.0, vel_floor=40, swap=None):
    """segments を並べて、曲の小節（chords の数）を埋める。voicings: コード名 → 6 本ぶんの音名か None（鳴らさない弦）。"""
    beats_per_bar = 4
    total = len(chords) * beats_per_bar
    sp_t = 60.0 / bpm
    ev = [[] for _ in range(6)]  # (拍, 長さ, 音名, 強さ)
    tb = 0.0
    for base, bar0, nbars in segments:
        if base is None:
            tb += nbars * beats_per_bar
            continue
        if base == "HIT":
            # 1小節に1回、ダウンで和音を弾いてのばす（Bメロの頭・Cメロ・最後の音など）。bar0 は強さ（100＝ふつう）
            for k in range(nbars):
                ci = int(tb // beats_per_bar) + k
                if ci >= len(chords) or chords[ci] == "-": continue
                vo = voicings[chords[ci]]
                for st in range(6):
                    if vo[st] is None: continue
                    bt = tb + k * beats_per_bar + st * 0.018 / sp_t
                    ev[st].append([bt, beats_per_bar - st * 0.018 / sp_t - 0.03, vo[st], bar0 * vel_scale])
            tb += nbars * beats_per_bar
            continue
        strums, _ = load(base)
        lo, hi = bar0 * beats_per_bar - 0.15, (bar0 + nbars) * beats_per_bar - 0.15
        # 源の小節ごとの「いちばん低く使った弦」（コードの根音の弦）
        lowest = {}
        for s in strums:
            k = int(math.floor((s["beat"] + 0.12) / beats_per_bar))
            lowest[k] = min(lowest.get(k, 5), min(x[0] for x in s["notes"]))
        for s in strums:
            if not (lo <= s["beat"] < hi):
                continue
            b = tb + (s["beat"] - bar0 * beats_per_bar)
            # 拍の頭のすこし前の打ちは、次のコード（先取り）
            ci = int(math.floor((b + 0.12) / beats_per_bar))
            if ci < 0 or ci >= len(chords):
                continue
            ch = chords[ci]
            if ch == "-":
                continue
            vo = voicings[ch]
            rs = lowest.get(int(math.floor((s["beat"] + 0.12) / beats_per_bar)), 0)
            rt = min(i for i in range(6) if vo[i] is not None)
            f = lambda st: rt + (max(st, rs) - rs) * (5 - rt) / max(1, 5 - rs)
            ns = sorted(s["notes"])  # 弦の低い順
            if len(ns) == 1:
                st, dt, dur = ns[0]
                tgt = [(int(round(f(st))), dt, dur)]
            else:
                a, z = int(round(f(ns[0][0]))), int(round(f(ns[-1][0])))
                ta, tz = ns[0][1], ns[-1][1]
                tgt = []
                for k in range(a, z + 1):
                    w = (k - a) / max(1, z - a)
                    # いちばん近い源の弦の長さ
                    near = min(ns, key=lambda x: abs(f(x[0]) - k))
                    tgt.append((k, ta + (tz - ta) * w, near[2]))
            for st, dt, dur in tgt:
                if vo[st] is None:
                    continue
                bt = b + dt / sp_t  # 弦のずれは秒のまま（手の速さは変わらない）
                ev[st].append([bt, dur, vo[st], s["vel"] * vel_scale])
        tb += nbars * beats_per_bar
    out = []
    for st in range(6):
        es = sorted(ev[st])
        parts, cur = [], 0.0
        for i, (bt, dur, name, v) in enumerate(es):
            if bt < cur - 1e-6 or bt >= total:
                continue
            nxt = es[i + 1][0] if i + 1 < len(es) else total
            # コードが変わる所では、前の音を止める（左手が離れる）
            bar_end = (math.floor(bt / beats_per_bar + 1e-9) + 1) * beats_per_bar
            ln = min(dur, nxt - bt - 0.02, total - bt)
            if es[i + 1:] and es[i + 1][2] != name:
                ln = min(ln, nxt - bt - 0.02)
            ln = max(0.09, ln)
            if bt > cur + 1e-4:
                parts.append(f"R:{bt - cur:.4f}")
            vv = int(round(max(vel_floor, min(150, v))))
            parts.append(f"{name}:{ln:.4f}%{vv}")
            cur = bt + ln
        if total > cur + 1e-4:
            parts.append(f"R:{total - cur:.4f}")
        out.append(" ".join(parts) if parts else f"R:{total}")
    return out


if __name__ == "__main__":
    V = {"F#m": ["F#2", "C#3", "F#3", "A3", "C#4", "F#4"], "E": ["E2", "B2", "E3", "G#3", "B3", "E4"]}
    for s in string_parts([("00_Rock3-148-C_comp", 0, 2)], ["F#m", "E"], V, 140):
        print(s[:160])
