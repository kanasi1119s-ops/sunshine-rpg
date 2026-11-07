"""歌詞の行と、1音ずつの時刻（MV の字幕・カラオケのように色が変わる表示・口の形に使う）。2026-11-08
  events(曲.json, 表, lead=[0]) → [{"t0","t1","jp","en","who","syl":[(開始秒, 終わり秒, ひらがな), ...]}]
  表: {ひらがなの行: (漢字まじり, 英語)}。曲.json.kana（拍・ひらがな）を先頭から、表の行に合う長さでつないで行にする。
  lead: 歌の本線（vocals の番号）。ハモリ・コーラスは入れない。2人で歌い分ける曲は両方（例 [0, 2]）。
"""
import json, re


def _notes(v):
    """vocal の notes → [(開始拍, 長さ拍, 歌詞)]。「ー」は前の音をのばす"""
    out = []; t = 0.0
    for tok in v["notes"].split():
        p = tok.split(":"); L = float(p[1])
        if not tok.startswith("R") and len(p) >= 3:
            ly = p[2]
            if ly in ("ー", "-", "~") and out: s, l0, y0 = out[-1]; out[-1] = (s, t + L - s, y0)
            else: out.append((t, L, ly))
        t += L
    return out


def events(song_path, table, bpm, lead=(0,), who_of=None):
    js = json.load(open(song_path)); kana = json.load(open(song_path + ".kana"))
    spb = 60.0 / bpm
    starts = {}
    for vi in lead:
        if vi < len(js["vocals"]):
            for s, L, ly in _notes(js["vocals"][vi]): starts.setdefault(round(s, 3), (L, set()))[1].add(vi)
    keys = sorted(table, key=len, reverse=True)
    ev = []; i = 0
    while i < len(kana):
        hit = None
        for k in keys:
            s = ""; j = i
            while j < len(kana) and len(s) < len(k):
                s += kana[j][1]; j += 1
            if s == k: hit = (k, j); break
        if hit is None: i += 1; continue
        k, j = hit; syl = []; voices = set()
        for q in range(i, j):
            b = kana[q][0]; L, vs = starts.get(round(b, 3), (0.5, set())); voices |= vs
            nb = kana[q + 1][0] if q + 1 < len(kana) else b + L
            syl.append((b * spb, min(b + L, nb) * spb, kana[q][1]))
        jp, en = table[k]
        ev.append({"t0": syl[0][0], "t1": syl[-1][1], "jp": jp, "en": en, "syl": syl,
                   "who": who_of(syl[0][0], syl[-1][1]) if who_of else None}); i = j
    return ev


def table_from(text_pairs):
    """[(ひらがなの行, 漢字まじり, 英語), ...] → 表"""
    return {k: (j, e) for k, j, e in text_pairs}
