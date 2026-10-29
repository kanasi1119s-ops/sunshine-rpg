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


TENSION = {"m": "m9", "m7": "m9", "": "add9", "maj7": "maj9", "7": "9"}


def tension_chord(ch):
    """伴奏の和音にテンションを足す（maj7→maj9、m→m9、長三和音→add9、7→9）。笛の旋律は素直なまま（docs/sound/layering-study.md）"""
    out = []
    for part in ch.split("|"):
        bass = None
        if "/" in part: part, bass = part.split("/")
        m = re.match(r"^([A-G][#b]?)(.*)$", part)
        q = TENSION.get(m.group(2), m.group(2))
        out.append(m.group(1) + q + (("/" + bass) if bass else ""))
    return "|".join(out)


def make(S, names, dyn_points, acc, flute_gain=None, intro=None, passing=False, tension=False):
    """names: 場面名の並び。dyn_points: [(場面名, オフセット, 強さ)]。acc/flute_gain: 場面名→倍率。intro: 前奏の場面名（弦を大きめに）"""
    c = C(); c.S = S; NB = S.nb; c.NB = NB
    if tension: S.chords = [tension_chord(x) for x in S.chords]
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


# ---------- 1回目で合格しやすくする「伴奏の厚さ」の床（2026-10-29 人間の指示：041番以降は最初から伴奏の厚さをそろえる） ----------
# 001〜040 を直してわかったこと（PQ が目標に届かなかった原因）:
#   ・前奏が楽器1つだけ（竪琴だけ・ピアノだけ・太鼓だけ）→ -35〜-50dB で「前奏が小さい」。ピアノの音源は特に小さい（×2.2 が要る）
#   ・笛が休む小節・止まる小節（問いかけ・ストップタイム・耳をすます）に何も残らない → 急に小さい所
#   ・終わりの場面が長く消えていく → 「段差大」
#   ・弦が2声だけ、チェロなし、パッドなし → 薄くて静の曲が 6.8〜7.1 に止まる
#   ・速い曲で太鼓とギターのストロークがない → 7.3 前後（7.8 に届くのは 012 の厚さ：ボーラン＋ギター＋竪琴＋チェロ＋弦＋笛の和声）
#   ・作った効果音・大きな環境音は CE（楽しさ）を下げる（空間は音楽の音で支配する。2026-10-29）
W_ROLE = {"piano": 0.45, "bell": 0.5, "pad": 0.6}
def _bar_weight(c):
    """小節ごとの伴奏の厚さ（笛以外の楽器の、音量×鳴っているかの合計）"""
    S = c.S; B = S.beats; w = [0.0] * c.NB
    for tr in S.tracks:
        if getattr(tr, "inst", "") == "panflute": continue
        v = tr.spec.get("volume", 0.05) * W_ROLE.get(tr.inst, 1.0)
        bars = set()
        for st, L, x in tr.ev:
            if x.startswith("R") or x.startswith("-"): continue
            b0 = int(st // B); b1 = int((st + L - 1e-6) // B)
            for b in range(b0, min(b1, c.NB - 1) + 1): bars.add(b)
        bg = tr.spec.get("barGain")
        for b in bars: w[b] += v * (bg[b] if bg and b < len(bg) else 1.0)
    return w

def floor_bed(c, min_w=0.11, skip=(), lo=52):
    """伴奏が薄い小節に、うすい弦3声とチェロの根音を足す（前奏も含む。曲の形は変えず、床だけ敷く）"""
    S = c.S; w = _bar_weight(c); n_add = 0
    for b in range(c.NB):
        if c.scene_of_bar[b] in skip or w[b] >= min_w: continue
        ch = S.chords[b].split("|")[0]
        busy = {int(st // S.beats) for tr in c.STR for st, L, x in tr.ev if not x.startswith("R")}
        if b not in busy:
            v = voice(ch, lo, 3, spread=True)
            for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:{S.beats}")
        r = low(ch, "C2"); r = r + 12 if r < 40 else r
        if not any(int(st // S.beats) == b for st, L, x in c.LOW.ev if not x.startswith("R")): c.LOW.bar(b, f"{nm(r)}:{S.beats}")
        n_add += 1
    return n_add

def thickness_report(c):
    """書き出す前に、薄い小節を数えて出す（1回目で合格しやすくするための自己検査）"""
    w = _bar_weight(c); B = c.S.beats
    thin = [b for b in range(c.NB) if w[b] < 0.09]
    intro = [b for b in range(c.NB) if c.scene_of_bar[b] == c.intro]
    iw = sum(w[b] for b in intro) / max(1, len(intro)) if intro else None
    print(f"厚さ検査: 薄い小節 {len(thin)}/{c.NB}" + (f"（{thin[:12]}…）" if thin else "") + (f"／前奏の厚さ {iw:.3f}" if iw is not None else ""))

def drive(c, scenes, kind="reel", soft_scenes=(), drum_vol=0.1, gtr_vol=0.05):
    """速い曲の推進力：ボーラン＋ギターの開放和音のストローク（012 の厚さ）。kind: reel/jig/slipjig/hornpipe/waltz/polka"""
    S = c.S; B = S.beats
    if not hasattr(c, "DRUM"):
        c.DRUM = S.track("ボーラン", "guitar", patch="frameDrum", volume=drum_vol, pan=-0.15, reverb=0.3, modulate=False, barGain=c.g())
        c.GTR = [S.track(f"ギター{i + 1}", "guitar", patch="nylonGuitar", volume=gtr_vol, pan=0.35 + 0.04 * i, reverb=0.35, barGain=c.g()) for i in range(5)]
    from c100_v2 import bodhran, strum, JIG_STRUM
    PAT = {"reel": [(0, 1, "d", "!"), (1, 0.5, "d", ","), (1.5, 0.5, "u", ","), (2, 1, "d", ""), (3, 0.5, "d", ","), (3.5, 0.5, "u", ",")],
           "hornpipe": [(0, 1, "d", "!"), (1, 0.5, "d", ","), (1.5, 0.5, "u", ","), (2, 1, "d", ""), (3, 0.5, "d", ","), (3.5, 0.5, "u", ",")],
           "jig": JIG_STRUM, "slipjig": [(0, 3, "d", "!"), (3, 3, "d", ""), (6, 2, "d", ","), (8, 1, "u", ",")],
           "waltz": [(0, 1, "d", "!"), (1, 1, "d", ","), (2, 1, "u", ",")], "polka": [(0, 0.5, "d", "!"), (0.5, 0.5, "u", ","), (1, 0.5, "d", ""), (1.5, 0.5, "u", ",")]}
    for b in range(c.NB):
        n = c.scene_of_bar[b]
        if n not in scenes: continue
        ch = S.chords[b].split("|")[0]; i = S.scene_of(b)[1]
        if kind == "polka": c.DRUM.bar(b, "D3:0.5! A3:0.5, D3:0.5 A3:0.5," if n not in soft_scenes else "D3:0.5, R:0.5 D3:0.5, R:0.5")
        else: bodhran(c.DRUM, b, B, kind, var=1 if i % 8 == 7 else 0, soft=n in soft_scenes)
        strum(c.GTR, b, B, ch, PAT[kind] if n not in soft_scenes else PAT[kind][:1] + [p for p in PAT[kind][1:] if p[3] == ""])

def finish(c, flags, desc, harm_scenes=None, tail_scene=None, tail_keep=99, silences=(), skip_scenes=(), double=True, fill=True, pads=True, pad_scenes=None, floor=False, floor_skip=()):
    S = c.S; NB = c.NB
    if floor:   # 041番以降：伴奏が薄い小節に床を敷く（前奏も）
        k = floor_bed(c, skip=floor_skip)
        print(f"床（弦3声＋チェロ）を足した小節: {k}")
    # 変に音が小さくなる所を作らない（2026-10-28 人間の指摘）：弦の持続が休んでいる小節には、小さな和音をのばして埋める。
    # 終わりの場面も最後まで弦とパッドをのばし、消え方は曲の最後のフェードにまかせる（ぷつっと落ちない）
    have = {int(st // S.beats) for st, L, x in c.STR[0].ev if not x.startswith("R")}
    for b in range(NB):
        n = c.scene_of_bar[b]
        if not fill or b in have or n in skip_scenes or n == c.intro: continue      # 始まりの場面は曲ごとに作るので、自動では埋めない（始まり方を曲ごとに変える。2026-10-28 人間の指摘）
        v = voice(S.chords[b].split("|")[0], 57, 3, spread=True)
        for j in range(3): c.STR[j].bar(b, f"{nm(v[j])}:{S.beats}")
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
    # 笛を2重にして深みを出す（2026-10-28 人間の提案。2026-10-28 18:57「音に深みが欲しい」で、全曲の既定にした）：同じ旋律を、少し遅らせて（0.04拍）、右寄り・小さめ・息の音なし・明るさを下げて重ねる
    if double:
        F2 = S.track("フルート（重ね）", "panflute", patch="flute", volume=0.22, bright=-0.8, pan=0.3, reverb=0.65, breath=False,
                     noRestrike=True, mono=True, sustain=1.12, phrase=16, gainDb=0,
                     barGain=[round(x * 0.85, 3) for x in c.FLUTE.spec["barGain"]])
        import random as _r
        rg = _r.Random(7)
        for st, L, x in list(c.FLUTE.ev):
            if L < 0.2 * S.beats / 4 * (2 if S.beats in (6, 9) else 1): continue      # 装飾音は重ねない
            F2.at(st + rg.uniform(0.0, 0.05), x)   # 一律にずらさず、1音ずつ少しランダムに（layering-study.md）
    # 旋律の1オクターブ下を竪琴がなぞる
    HM = S.track("竪琴（旋律の下）", "harp", patch="folkHarp", volume=0.05, pan=0.2, reverb=0.5, barGain=c.g())
    if harm_scenes:
        lo = min(c.s0[n] for n in harm_scenes) * S.beats
        hi = max(c.s0[n] + c.sc_len[n] for n in harm_scenes) * S.beats
        for st, L, x in list(c.FLUTE.ev):
            if lo <= st < hi:
                p = midi_of(x)
                if p is not None and p - 12 >= 52 and L >= 0.4: HM.at(st, shift_tok(x, -1))
    # 広がりのパッド（小）。終わりの手前まで（自然の音だけにならないように）
    PADS = [S.track(f"広がりのパッド{i + 1}", "pad", patch="modernPad", volume=0.03, pan=[-0.75, 0.75][i], reverb=0.5) for i in range(2)]
    for b in range(NB):
        n, i, L, k = S.scene_of(b)
        if tail_scene and n == tail_scene and i >= tail_keep: continue
        if not pads or n in skip_scenes or n == c.intro: continue
        if pad_scenes is not None and n not in pad_scenes: continue
        w = voice(S.chords[b].split("|")[0], 55, 2, spread=True)
        for j in range(2): PADS[j].bar(b, f"{nm(w[j])}:{S.beats}")
    # 笛（panflute）の音域は C4 から。C4 より低い音は1オクターブ上げる（低すぎる音は鳴らないか、質が落ちる）
    for tr in S.tracks:
        if getattr(tr, "inst", "") == "panflute":
            ev2 = []
            for st, L, x in tr.ev:
                p = midi_of(x)
                ev2.append((st, L, shift_tok(x, 1) if p is not None and p < 60 else x))
            tr.ev = ev2
    for (b, a, z) in silences: c.SIL.add(b, a, z)
    c.SIL.apply()
    S.fade_out = 0
    S.flags = flags
    S.desc = desc
    S.no_depth = True
    thickness_report(c)
    vwrite(S)


def _dia(S, m, k):
    """m（MIDI）から音階の上で k 段ずらした音（k<0 は下）"""
    sc = [(S.key.t + x) % 12 for x in S.key.steps]
    step = 1 if k > 0 else -1; n = abs(k); x = m
    while n:
        x += step
        if x % 12 in sc: n -= 1
    return x


def rich(c, choir_scenes=(), pulse_scenes=(), choir_vol=0.13, guitar=True, pizz=True, inner=True):
    """音を重ねて深みと細やかさを出す（2026-10-28 人間の提案：笛が主体のまま、音数を多く繊細に。一人で何声も重ねるような重ね方）。
    ・笛の和声：主旋律の下に、和音の音になる3度下（だめなら4度・5度下）を2本目・3本目の笛で重ねる（左右に分け、小さく）
    ・ナイロンギター：8分音符のやわらかい分散和音（右寄り）
    ・弦のピチカート：4分音符の軽い刻み（左寄り）
    どれも小さく、それぞれ別の音域・別の左右に置いて、笛の前に出ないようにする"""
    S = c.S; B = S.beats
    CH1 = S.track("笛の和声1", "panflute", patch="flute", volume=choir_vol, bright=-0.8, pan=-0.38, reverb=0.6, breath=False,
                  noRestrike=True, mono=True, sustain=1.12, phrase=16, barGain=c.g())
    CH2 = S.track("笛の和声2", "panflute", patch="flute", volume=choir_vol * 0.85, bright=-0.9, pan=0.4, reverb=0.65, breath=False,
                  noRestrike=True, mono=True, sustain=1.12, phrase=16, barGain=c.g())
    lo_b = {n: (c.s0[n], c.s0[n] + c.sc_len[n]) for n in choir_scenes}
    for st, L, x in list(c.FLUTE.ev):
        p = midi_of(x)
        if p is None or L < 0.4: continue
        bar = int(st // B)
        if not any(a <= bar < z for a, z in lo_b.values()): continue
        pcs = chord_pcs(S.chords[bar].split("|")[0])
        cands = [_dia(S, p, -k) for k in (2, 3, 4, 5)]
        ok = [q for q in cands if q % 12 in pcs]
        h1 = ok[0] if ok else cands[0]
        rest = [q for q in ok if q < h1 - 2]
        h2 = rest[0] if rest else _dia(S, h1, -2)
        v = x.split(":", 1)[1]
        if h1 >= 55: CH1.at(st, f"{nm(h1)}:{v}")
        if h2 >= 55 and L >= 1: CH2.at(st, f"{nm(h2)}:{v}")
    # 内声の動き：弦の1本が、和音の中のテンション（9th・maj7・6th）から一音ずつ動く（maj7→6、9→1 のように。クリシェ）
    IN = S.track("内声の動き（弦）", "strings", patch="slowStrings", volume=0.032, pan=0.15, reverb=0.55, barGain=c.g())
    sc = [(S.key.t + x) % 12 for x in S.key.steps]
    for b in range(c.NB):
        if c.scene_of_bar[b] not in pulse_scenes: continue
        ch = S.chords[b].split("|")[0]
        pcs = chord_pcs(ch)
        cand = [m for m in range(60, 70) if m % 12 in pcs]
        if not cand: continue
        a = cand[-1]
        z = a - 1
        while z % 12 not in sc: z -= 1
        h1 = {3: 2, 6: 3}.get(B, 2); h2 = B - h1
        if inner: IN.bar(b, f"{nm(a)}:{h1} {nm(z)}:{h2}" if b % 2 == 0 else f"{nm(z)}:{h1} {nm(a)}:{h2}")
    GT = S.track("ナイロンギター（刻み）", "guitar", patch="nylonGuitar", volume=0.055, pan=0.45, reverb=0.4, barGain=c.g())
    PZ = S.track("弦のピチカート", "strings", patch="pizzicato", volume=0.06, pan=-0.45, reverb=0.35, barGain=c.g())
    for b in range(c.NB):
        if c.scene_of_bar[b] not in pulse_scenes: continue
        ch = S.chords[b].split("|")[0]
        t = tones(ch, "G3", "G5")
        if len(t) < 4: t = t + [q + 12 for q in t]
        # 拍子に合わせた刻み（4/4：8分×8、3/4：8分×6、6/8（1拍＝8分）：8分×6）
        GP = {4: ((0, 2, 1, 3, 2, 1, 3, 2), 0.5), 3: ((0, 2, 1, 3, 2, 1), 0.5), 6: ((0, 2, 3, 1, 2, 3), 1)}.get(B, ((0, 2, 1, 3), B / 4))
        if guitar: GT.bar(b, " ".join(f"{nm(t[q % len(t)])}:{GP[1]}" for q in GP[0]))
        z = tones(ch, "C4", "C5")
        PP = {4: ((0, 1, 2, 1), 1), 3: ((0, 1, 2), 1), 6: ((0, 2), 3)}.get(B, ((0,), B))
        seq = PP[0] if b % 2 == 0 else tuple(reversed(PP[0]))
        if pizz: PZ.bar(b, " ".join(f"{nm(z[q % len(z)])}:{PP[1]}" for q in seq))


def dshift(line, k):
    """度数の旋律（"5':2 4':1" など）を、音階の上で k 段ずらす（k<0 は下。3度下＝-2）。臨時記号はそのまま"""
    out = []
    for tok in line.split():
        m = re.match(r"^([b#]?)([1-7])([',]*)(:.*)$", tok)
        if not m: out.append(tok); continue
        acc, d, marks, rest = m.groups()
        o = marks.count("'") - marks.count(",")
        z = (int(d) - 1) + k + 7 * o
        o2, d2 = divmod(z, 7)
        out.append(f"{acc}{d2 + 1}{chr(39) * o2 if o2 > 0 else ',' * (-o2)}{rest}")
    return " ".join(out)


def sparkle(c, scenes=None, glock_vol=0.03, harp_vol=0.05, seed=11, dense=False):
    """高い所のきらめき（グロッケンと竪琴の高い音を、和音の音でまばらに）。2026-10-29 試し：合格した静かな曲（035・009・010・006・002）は、
    どれも高いきらめきの層があり、7.0 前後で止まる曲（017・018・022・024 など）にはない"""
    import random as _r
    S = c.S; B = S.beats; rg = _r.Random(seed)
    GL = S.track("きらめき（グロッケン）", "bell", patch="glockenspiel", volume=glock_vol, pan=0.4, reverb=0.75, barGain=c.g())
    HP = S.track("きらめき（竪琴の高い音）", "harp", patch="folkHarp", volume=harp_vol, pan=-0.45, reverb=0.7, barGain=c.g())
    for b in range(c.NB):
        if scenes is not None and c.scene_of_bar[b] not in scenes: continue
        ch = S.chords[b].split("|")[0]
        hi = tones(ch, "C6", "C7"); hh = tones(ch, "G5", "G6")
        if b % 2 == 0 or dense: GL.at(b * B + rg.choice((0, B / 2)), f"{nm(rg.choice(hi))}:{B / 2},")
        k = rg.randrange(3, 6) if dense else rg.randrange(2, 4); pos = sorted(rg.sample([q * (B / 8 if B in (4, 2) else 1) for q in range(8 if B in (4, 2) else int(B))], k))
        for q in pos: HP.at(b * B + q, f"{nm(rg.choice(hh))}:1,")


def thick(c, scenes=None, lo=50, vol=0.045, cb_vol=0.07):
    """速い曲の厚さ：低めの弦3声（左右と中央）＋コントラバスの根音を、場面の全小節に（2026-10-29: 023 7.27→7.53、025 7.26→7.66）"""
    S = c.S; B = S.beats
    TH = [S.track(f"厚い弦{i + 1}", "strings", patch="slowStrings", volume=vol, pan=[-0.55, 0.55, 0.0][i], reverb=0.5, barGain=c.g()) for i in range(3)]
    CBt = S.track("コントラバス（厚さ）", "strings", patch="contrabass", volume=cb_vol, pan=0.0, reverb=0.4, barGain=c.g())
    for b in range(c.NB):
        if scenes is not None and c.scene_of_bar[b] not in scenes: continue
        ch = S.chords[b].split("|")[0]
        w = voice(ch, lo, 3, spread=True)
        for j in range(3): TH[j].bar(b, f"{nm(w[j])}:{B}")
        r = low(ch, "C2"); r = r + 12 if r < 36 else r
        CBt.bar(b, f"{nm(r)}:{B}")
