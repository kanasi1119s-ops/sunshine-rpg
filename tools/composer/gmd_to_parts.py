#!/usr/bin/env python3
"""人がたたいたドラムの演奏（Groove MIDI Dataset・CC BY 4.0）を、タイミングのずれと強さを残したまま、作曲ソフトのドラムのパートにする（2026-11-07）。
これまで（loud25_drums.py）は 16分の格子に寄せて X/x/o の3段にしていたので、人らしさが消えていた。
使い方（ライブラリ）: parts_from_gmd(midi, bar0, nbars, quantize=False) → {"kick": notes, "snare": ..., "hihat": ..., "tom": ..., "crash": ...}
  quantize=True で「今までのやり方」（16分の格子・3段の強さ）にした同じ演奏（聞き比べ用）
"""
import mido

KIT = {36: "kick", 38: "snare", 40: "snare", 37: "snare_x",
       48: ("tom", "C4"), 50: ("tom", "C4"), 45: ("tom", "A3"), 47: ("tom", "A3"), 43: ("tom", "F3"), 58: ("tom", "D3"),
       42: "hh", 22: "hh", 44: "hhp", 46: "hho", 26: "hho",
       49: ("crash", "C2"), 55: ("crash", "C2"), 57: ("crash", "G2"), 52: ("crash", "B2"), 51: ("crash", "D2"), 59: ("crash", "D2"), 53: ("crash", "F2")}


def read(path):
    m = mido.MidiFile(path); tpb = m.ticks_per_beat; t = 0; out = []
    for msg in mido.merge_tracks(m.tracks):
        t += msg.time
        if msg.type == "note_on" and msg.velocity > 0 and msg.note in KIT:
            out.append((t / tpb, msg.note, msg.velocity))
    return out


def pct(v, part):
    # GMD の強さ 0〜127 → 作曲ソフトの強さ（100＝ふつう、130＝アクセント）。ゴーストは 35 くらいまで下がる
    base = {"kick": (30, 1.0), "snare": (25, 1.05), "hihat": (25, 0.95), "tom": (30, 1.0), "crash": (40, 0.85)}[part]
    return max(15, min(160, round(base[0] + v * base[1])))


def parts_from_gmd(path, bar0, nbars, quantize=False, beats=4):
    ev = read(path)
    lo, hi = bar0 * beats - 0.06, (bar0 + nbars) * beats - 0.06
    hits = {k: [] for k in ("kick", "snare", "hihat", "tom", "crash")}
    for pos, note, v in ev:
        if not (lo <= pos < hi): continue
        rel = max(0.0, pos - bar0 * beats)
        k = KIT[note]
        if isinstance(k, tuple): part, name = k
        elif k in ("hh", "hhp", "hho"): part, name = "hihat", k
        elif k == "snare_x": part, name = "snare", "x"      # クロススティック（縁）は弱いスネアに
        else: part, name = k, "x"
        if quantize:
            rel = round(rel * 4) / 4
            vv = "X" if v >= 100 else ("o" if v < 45 else "x")
        else:
            vv = None
        hits[part].append((rel, name, v, vv))
    total = nbars * beats; out = {}
    for part, hs in hits.items():
        hs.sort(); toks = []; t = 0.0
        # 同じ時刻（ほぼ同時）の重なりは強い方だけ
        merged = []
        for h in hs:
            if merged and abs(h[0] - merged[-1][0]) < 0.015:
                if h[2] > merged[-1][2]: merged[-1] = h
                continue
            merged.append(h)
        for i, (st, name, v, vv) in enumerate(merged):
            if st > t + 1e-4: toks.append(f"R:{st - t:.4f}")
            nxt = merged[i + 1][0] if i + 1 < len(merged) else total
            d = max(0.01, nxt - st)
            if part in ("tom", "crash"):
                nm = name
            else:
                nm = "x"
            mark = ""
            if name == "hho": mark = "*"
            if quantize:
                if part in ("tom", "crash"): toks.append(f"{nm}:{d:.4f}{'!' if vv == 'X' else (',' if vv == 'o' else '')}{mark}")
                else: toks.append(f"{'X' if vv == 'X' else ('o' if vv == 'o' else 'x')}:{d:.4f}{mark}")
            else:
                pv = pct(v, part) if name != "hhp" else min(45, pct(v, part))
                toks.append(f"{nm}:{d:.4f}{mark}%{pv}")
            t = st + d
        if t < total - 1e-4: toks.append(f"R:{total - t:.4f}")
        out[part] = " ".join(toks) if hs else ""
    return out
