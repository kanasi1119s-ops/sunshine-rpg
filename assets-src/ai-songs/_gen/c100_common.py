"""ケルト・フルート100曲「銀の笛と百の夜」の共通部品（2026-10-28）。
001 で人間に聴いてもらって決まったことを、全曲の土台にする:
  ・笛は mono・noRestrike・sustain 1.12・bright -0.6・phrase 16・gainDb 2（なめらかで優しく）
  ・C6 より高い音は1オクターブ下げる（硬く耳が痛い）。高い小節ほど息をやわらかく
  ・弦の持続は小さく（0.03）。前奏だけ大きめ。シンセ系の自動パッド・きらめき・シンバル効果音は入れない
  ・広がりのパッド（小）と、旋律の1オクターブ下をなぞる竪琴で厚みを足す（点数のため）
  ・自然の音だけが鳴る時間を作らない（前置き 1.2 秒・後ろ 4 秒、終わりも弦とパッドをのばす）
使い方: 各曲のファイルで Song と scene を作り、setup() → put_melody() → 伴奏 → finish()
"""
import re, collections
from vb25_lib import *

_N = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def midi_of(tok):
    m = re.match(r"^([A-G])([#b]?)(-?\d+)(:|$)", tok)
    if not m: return None
    return (int(m.group(3)) + 1) * 12 + _N[m.group(1)] + (1 if m.group(2) == "#" else -1 if m.group(2) == "b" else 0)


def shift_tok(txt, d):
    out = []
    for tok in txt.split():
        m = re.match(r"^([A-G][#b]?)(-?\d+)(:.*)$", tok)
        out.append(f"{m.group(1)}{int(m.group(2)) + d}{m.group(3)}" if m else tok)
    return " ".join(out)


def hi_soft(txt, top=84):
    """C6より高い音は1オクターブ下げる"""
    out = []
    for tok in txt.split():
        p = midi_of(tok)
        out.append(shift_tok(tok, -1) if p is not None and p > top else tok)
    return " ".join(out)


def curve(NB, points):
    out = []
    pts = sorted(points)
    for b in range(NB):
        for (b0, v0), (b1, v1) in zip(pts, pts[1:]):
            if b0 <= b <= b1:
                out.append(round(v0 + (v1 - v0) * (b - b0) / max(1, b1 - b0), 3)); break
        else: out.append(pts[-1][1])
    return out


class C:
    pass


def make(S, names, dyn_points, acc, flute_gain=None, intro=None, passing=False):
    """names: 場面名の並び。dyn_points: [(場面名, オフセット, 強さ)]。acc/flute_gain: 場面名→倍率。intro: 前奏の場面名（弦を大きめに）"""
    c = C(); c.S = S; NB = S.nb; c.NB = NB
    if passing:
        # 一段ずつ上がる型など、1拍の経過音は和音の外でもよい（長い音と小節頭の長めの音だけ、アヴォイドノートを直す）
        import types
        def fix_avoid(self, t):
            n = 0; B = self.beats
            for k, (st, L, x) in enumerate(t.ev):
                nt, v = x.split(":", 1)
                if nt in ("R", "-"): continue
                bar = min(int(st // B + 1e-6), self.nb - 1)
                pcs = chord_pcs(self.chords[bar].split("|")[0])
                m = midi(nt); pc = m % 12
                pos = st - bar * B
                strong = L >= 2 - 1e-6 or (abs(pos) < 1e-6 and L >= 1.5)
                if strong and pc not in pcs and (pc - 1) % 12 in pcs:
                    t.ev[k] = (st, L, nm(m - 1, "b" in nt[1:2]) + ":" + v); n += 1
            return n
        S.fix_avoid = types.MethodType(fix_avoid, S)
    c.s0 = {n: S.sc(n)[0] for n in names}
    c.sc_len = {n: len(S.sc(n)) for n in names}
    c.DYN = curve(NB, [(min(NB - 1, c.s0[n] + off), v) for n, off, v in dyn_points])
    c.scene_of_bar = [S.scene_of(b)[0] for b in range(NB)]
    c.ACC = [acc.get(c.scene_of_bar[b], 1.0) for b in range(NB)]
    fg = flute_gain or {}
    c.FG = [fg.get(c.scene_of_bar[b], 1.0) for b in range(NB)]
    c.intro = intro

    def g(extra=None):
        return [round(d * c.ACC[b] * (extra[b] if extra else 1), 3) for b, d in enumerate(c.DYN)]
    c.g = g
    c.FLUTE = S.track("フルート", "panflute", patch="flute", volume=0.42, bright=-0.6, pan=-0.05, reverb=0.5, breath=True,
                      noRestrike=True, mono=True, sustain=1.12, phrase=16, gainDb=4.5,   # 主旋律なのでもう少し表に（2026-10-28 人間の指示。2→4.5）
                      barGain=[round(max(d, 0.82) * c.FG[b], 3) for b, d in enumerate(c.DYN)])
    c.HARP = S.track("ハープ", "harp", patch="folkHarp", recipe="celtic-harp", volume=0.105, pan=-0.1, reverb=0.45, barGain=g())
    c.HARP2 = S.track("ハープ（高い響き）", "harp", patch="folkHarp", volume=0.055, pan=0.4, reverb=0.6, barGain=g())
    c.STR = [S.track(f"弦の持続{i}", "strings", patch="slowStrings", recipe="celtic-strings", volume=0.03, pan=[-0.7, 0.7, 0][i], reverb=0.55,
                     barGain=g([1.6 if c.scene_of_bar[b] == intro else 1.0 for b in range(NB)])) for i in range(3)]
    c.LOW = S.track("チェロ", "strings", patch="cello", recipe="celtic-low", volume=0.07, pan=-0.15, reverb=0.35, barGain=g())
    c.SIL = Silence(S)
    return c


def put_melody(c, scene, phrases, oct_):
    """phrases: 4小節ごとのフレーズ（度数の文字列4つ）のリスト。小節数＝フレーズ数×4 ぶん置く"""
    bars = c.S.sc(scene)
    for p, ph in enumerate(phrases):
        for j, s in enumerate(ph):
            if p * 4 + j < len(bars):
                c.FLUTE.bar(bars[p * 4 + j], hi_soft(c.S.key.mel(s, oct=oct_)))


def put_bars(c, scene, lines, oct_):
    """小節ごとの度数の文字列（1小節＝1つ）"""
    for b, s in zip(c.S.sc(scene), lines):
        c.FLUTE.bar(b, hi_soft(c.S.key.mel(s, oct=oct_)))


def finish(c, flags, desc, harm_scenes=None, tail_scene=None, tail_keep=6, silences=(), skip_scenes=(), double=False):
    S = c.S; NB = c.NB
    # 高い小節ほど息をやわらかく
    pb = collections.defaultdict(list)
    for st, L, x in c.FLUTE.ev:
        p = midi_of(x)
        if p is not None: pb[int(st // S.beats)].append(p)
    bg = c.FLUTE.spec["barGain"]
    for b, ps in pb.items():
        m = sum(ps) / len(ps)
        k = min(1.0, max(0.0, (m - 74) / 10))
        bg[b] = round(bg[b] * (1 - 0.35 * k), 3)
    # 笛を2重にして深みを出す（2026-10-28 人間の提案）：同じ旋律を、少し遅らせて（0.04拍）、右寄り・小さめ・息の音なし・明るさを下げて重ねる
    if double:
        F2 = S.track("フルート（重ね）", "panflute", patch="flute", volume=0.22, bright=-0.8, pan=0.3, reverb=0.65, breath=False,
                     noRestrike=True, mono=True, sustain=1.12, phrase=16, gainDb=0, push=0.04,
                     barGain=[round(x * 0.85, 3) for x in c.FLUTE.spec["barGain"]])
        for st, L, x in list(c.FLUTE.ev): F2.at(st, x)
    # 旋律の1オクターブ下を竪琴がなぞる
    HM = S.track("竪琴（旋律の下）", "harp", patch="folkHarp", volume=0.05, pan=0.2, reverb=0.5, barGain=c.g())
    if harm_scenes:
        lo = min(c.s0[n] for n in harm_scenes) * S.beats
        hi = max(c.s0[n] + c.sc_len[n] for n in harm_scenes) * S.beats
        for st, L, x in list(c.FLUTE.ev):
            if lo <= st < hi:
                p = midi_of(x)
                if p is not None and p - 12 >= 52: HM.at(st, shift_tok(x, -1))
    # 広がりのパッド（小）。終わりの手前まで（自然の音だけにならないように）
    PADS = [S.track(f"広がりのパッド{i + 1}", "pad", patch="modernPad", volume=0.03, pan=[-0.75, 0.75][i], reverb=0.5) for i in range(2)]
    for b in range(NB):
        n, i, L, k = S.scene_of(b)
        if tail_scene and n == tail_scene and i >= tail_keep: continue
        if n in skip_scenes: continue
        w = voice(S.chords[b].split("|")[0], 55, 2, spread=True)
        for j in range(2): PADS[j].bar(b, f"{nm(w[j])}:{S.beats}")
    for (b, a, z) in silences: c.SIL.add(b, a, z)
    c.SIL.apply()
    S.fade_out = 0
    S.flags = flags
    S.desc = desc
    S.no_depth = True
    vwrite(S)
