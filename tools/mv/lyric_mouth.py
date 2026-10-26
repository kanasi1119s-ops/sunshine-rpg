#!/usr/bin/env python3
"""歌詞（UST）から、時間ごとの口の形（あ・い・う・え・お・閉じる）を決める。teto_mv.py から使う。
2026-10-26 人間「口の動きも言葉の動きに合わせてほしいかも」"""
import math
V = {}
for row, vs in (("あかさたなはまやらわがざだばぱぁゃ", "a"), ("いきしちにひみりぎじぢびぴぃ", "i"),
                ("うくすつぬふむゆるぐずづぶぷぅゅゔ", "u"), ("えけせてねへめれげぜでべぺぇ", "e"),
                ("おこそとのほもよろをごぞどぼぽぉょ", "o")):
    for ch in row: V[ch] = vs
LIPS = set("まみむめもばびぶべぼぱぴぷぺぽわ")                  # 唇を一度閉じてから出す音
def kata2hira(s): return "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c for c in s)
def vowel(ly):
    ly = kata2hira(ly.strip())
    for ch in reversed(ly):
        if ch in "んン": return "n"
        if ch == "っ": return "n"
        if ch in V: return V[ch]
        if ch == "ー": continue
    return None
def read_ust(path):
    raw = open(path, "rb").read()
    try: txt = raw.decode("cp932")
    except UnicodeDecodeError: txt = raw.decode("utf-8", "ignore")
    notes = []; cur = {}
    for line in txt.splitlines():
        if line.startswith("[#"):
            if "Length" in cur: notes.append(cur)
            cur = {}
        elif "=" in line:
            k, v = line.split("=", 1); cur[k] = v
    if "Length" in cur: notes.append(cur)
    out = []; beat = 0.0
    for n in notes:
        L = int(n["Length"]) / 480.0; ly = n.get("Lyric", "R")
        if ly not in ("R", "r", ""): out.append((beat, L, ly))
        beat += L
    return out
def timeline(ust, b2s, fps, nframes):
    """コマごとの口の形の文字列のリスト（"a" "i" "u" "e" "o" "n"=閉じる）。休みは "n"。
    前の音と同じ母音で続く「〜」はそのまま。唇を閉じる音（ま行・ば行・ぱ行）は、頭の 1 コマだけ閉じる"""
    tl = ["n"] * nframes; prev = "n"
    for beat, L, ly in read_ust(ust):
        s, e = b2s(beat), b2s(beat + L)
        v = vowel(ly.lstrip("+-~")) or prev
        i0, i1 = int(round(s * fps)), int(round(e * fps))
        for i in range(max(0, i0), min(nframes, i1)): tl[i] = v
        c = kata2hira(ly.strip())[:1]
        if c in LIPS and 0 <= i0 < nframes and i1 - i0 >= 3: tl[i0] = "n"
        prev = v
    return tl
