"""ケルト・フルート100曲「銀の笛と百の夜」— 作り方 第2版の部品（2026-10-28）。
旭さん「正直このままじゃつまらない曲になる」を受けて作り直した。根拠は docs/sound/celtic-study/README.md。

第1版（c100_common）との違い:
  ・旋律は「動機」と「8小節の型」で書く（各曲のファイルで手で書く）。ここでは、それを鳴らすための部品を用意する
  ・笛の装飾（cut・tap・roll・cran・slide）と、はずみ（リールの長短・ジグの3つ組）を、決まりに沿って自動で付ける
  ・拍子ごとの伴奏の型（ボーラン・開放和音のギター・ハープのローヴィング・サム／オスティナート・ピアノ）
  ・楽器の出入りは、各曲の「編曲の表」で場面ごとに決める（全部を鳴らしっぱなしにしない）
使い方: 各曲で Song と scene を作り、c100_common.make() で基本の楽器を作ったあと、
        play_melody() で旋律を置き、伴奏の部品で場面ごとに楽器を出し入れし、finish(..., fill=False) で書き出す。
"""
import random
from c100_common import *

# ---------------- 旋律を「音の並び」にする ----------------

def mel_events(key, s, oct_, start):
    """度数の旋律（'1:2 3:1 5:3' など）を、(開始拍, 長さ, MIDI) の並びにする。R は休み"""
    out = []; t = start
    for tok in key.mel(s, oct=oct_).split():
        n, v = tok.split(":", 1)
        L = tok_beats(tok)
        if not n.startswith("R"): out.append([t, L, midi_of(tok)])
        t += L
    return out


def section_events(c, scene, bars, oct_, key=None):
    """場面に、小節ごとの度数の旋律（リスト）を置いた音の並び"""
    key = key or c.S.key; B = c.S.beats
    ev = []
    for j, s in enumerate(bars):
        b = c.s0[scene] + j
        if b >= c.s0[scene] + c.sc_len[scene]: break
        ev += mel_events(key, s, oct_, b * B)
    return ev


# ---------------- はずみ（リルト） ----------------

def lilt(ev, beats, kind):
    """拍の中の長さの配分を変える（はずみ）。kind: jig（3つ組 38:28:34）・reel（2つ組 56:44）・hornpipe（2つ組 64:36）・straight。
    6/8 は1拍＝8分で書いているので、3つ組は「拍の頭が3の倍数」の所。4/4 は 0.5 拍の組"""
    if kind == "straight": return ev
    out = [list(e) for e in ev]
    if kind == "jig":
        W = (1.14, 0.84, 1.02)
        for k in range(len(out) - 2):
            a, b_, c_ = out[k], out[k + 1], out[k + 2]
            if abs(a[0] % 3) < 1e-6 and all(abs(x[1] - 1) < 1e-6 for x in (a, b_, c_)) and abs(b_[0] - a[0] - 1) < 1e-6 and abs(c_[0] - a[0] - 2) < 1e-6:
                a[1] = W[0]; b_[0] = a[0] + W[0]; b_[1] = W[1]; c_[0] = b_[0] + W[1]; c_[1] = W[2]
    else:
        r = 0.56 if kind == "reel" else 0.64
        for k in range(len(out) - 1):
            a, b_ = out[k], out[k + 1]
            if abs(a[0] % 1) < 1e-6 and abs(a[1] - 0.5) < 1e-6 and abs(b_[1] - 0.5) < 1e-6 and abs(b_[0] - a[0] - 0.5) < 1e-6:
                a[1] = r; b_[0] = a[0] + r; b_[1] = 1 - r
    return out


# ---------------- 装飾 ----------------

def _scale(key):
    return [(key.t + x) % 12 for x in key.steps]


def _dia(key, m, k):
    sc = _scale(key); x = m; n = abs(k); st = 1 if k > 0 else -1
    while n:
        x += st
        if x % 12 in sc: n -= 1
    return x


def ornament(ev, key, bpm, kind, beats, density=1.0, seed=1, lo_tap=62):
    """装飾を付ける（Larsen ほか。docs/sound/celtic-study/README.md B）。
    返り値: (開始拍, 長さ, MIDI, 記号) の並び。装飾音は短く（cut 30ms ほど）、主音は拍ちょうどのまま（装飾のぶん主音を短くする）。
    kind: air（ゆっくり：slide と軽い cut だけ）・jig・reel・hornpipe・waltz"""
    rg = random.Random(seed)
    g = 0.032 * bpm / 60          # 32ms を拍に
    gs = 0.13 * bpm / 60          # slide 130ms
    unit = 1.0 if beats == 6 or beats == 9 else 0.5   # 8分音符の長さ（拍）
    out = []; per_bar = {}
    prev = None
    for k, (t, L, m) in enumerate(ev):
        bar = int(t // beats + 1e-6)
        used = per_bar.get(bar, 0)
        lim = 2 if kind != "air" else 1
        strong = abs((t / unit) % (3 if beats in (6, 9) else 2)) < 1e-6
        nxt = ev[k + 1][2] if k + 1 < len(ev) else None
        done = False
        if used < lim and kind != "air":
            # ロール：付点4分（ジグ）／4分（リール）の長い音で、拍の頭
            if strong and ((beats in (6, 9) and abs(L - 3 * unit) < 0.2) or (beats == 4 and abs(L - 1) < 0.1)) and rg.random() < 0.45 * density:
                up = _dia(key, m, 2); dn = _dia(key, m, -1)
                if m < lo_tap:                           # 低い音は tap ができないので cran（cut を3回）
                    q = L / 4
                    out += [(t, q, m, ""), (t + q, g, _dia(key, m, 2), ""), (t + q + g, q - g, m, ""), (t + 2 * q, g, _dia(key, m, 3), ""),
                            (t + 2 * q + g, q - g, m, ""), (t + 3 * q, g, _dia(key, m, 4), ""), (t + 3 * q + g, q - g, m, "")]
                else:
                    q = L / 3
                    out += [(t, q, m, ""), (t + q, g, up, ""), (t + q + g, q - g, m, ","), (t + 2 * q, g, dn, ""), (t + 2 * q + g, q - g, m, "")]
                per_bar[bar] = used + 1; done = True
            # 同じ音が続く所：cut で区切る
            elif prev is not None and prev == m and rg.random() < 0.8 * density:
                out += [(t, g, _dia(key, m, 2 if m < 67 else 1 + rg.randint(1, 2)), ""), (t + g, L - g, m, "")]
                per_bar[bar] = used + 1; done = True
            # 下がって長い音に着地：tap
            elif prev is not None and prev > m and L >= 2 * unit - 1e-6 and strong and m >= lo_tap and rg.random() < 0.4 * density:
                out += [(t, L * 0.45, m, ""), (t + L * 0.45, g, _dia(key, m, -1), ""), (t + L * 0.45 + g, L * 0.55 - g, m, "")]
                per_bar[bar] = used + 1; done = True
            # 上がって拍の頭に着いた音：cut
            elif prev is not None and prev < m and strong and L >= unit - 1e-6 and rg.random() < 0.3 * density:
                out += [(t, g, _dia(key, m, 2), ""), (t + g, L - g, m, "")]
                per_bar[bar] = used + 1; done = True
        elif used < lim and kind == "air":
            if L >= 2 and (prev is None or abs(prev - m) >= 2) and rg.random() < 0.35 * density:          # 長い音へ下からすべり込む
                out += [(t, gs, m - 1 if (m - 1) % 12 in _scale(key) else m - 2, ""), (t + gs, L - gs, m, "")]
                per_bar[bar] = used + 1; done = True
            elif L >= 1.5 and prev is not None and prev > m and rg.random() < 0.3 * density:               # 下がって長い音：ゆっくりした tap
                gg = g * 1.6
                out += [(t, L * 0.4, m, ""), (t + L * 0.4, gg, _dia(key, m, -1), ""), (t + L * 0.4 + gg, L * 0.6 - gg, m, "")]
                per_bar[bar] = used + 1; done = True
            elif prev is not None and prev == m:
                out += [(t, g, _dia(key, m, 2), ""), (t + g, L - g, m, "")]
                per_bar[bar] = used + 1; done = True
        if not done:
            mark = ""
            if kind in ("jig", "reel", "hornpipe") and not strong and L <= unit + 1e-6: mark = ","   # 拍の頭でない短い音は少し弱く
            out.append((t, L, m, mark))
        prev = m
    return out


def play(track, notes):
    """(開始拍, 長さ, MIDI, 記号) の並びを、トラックに置く"""
    for t, L, m, mk in notes:
        track.at(round(t, 4), f"{nm(m)}:{round(L, 4)}{mk}")


def play_melody(c, scene, bars, oct_, kind, key=None, density=1.0, seed=1, track=None, lift=0):
    """場面に旋律を置く（はずみ→装飾→置く）。lift: 半音で上げる（転調）"""
    S = c.S; key = key or S.key
    if lift: key = key.up(lift)
    ev = section_events(c, scene, bars, oct_, key)
    ev = [[t, L, (m if m <= 84 else m - 12)] for t, L, m in ev]       # C6 より上は硬いので下げる（第1版と同じ）
    ev = lilt(ev, S.beats, {"jig": "jig", "reel": "reel", "hornpipe": "hornpipe"}.get(kind, "straight"))
    notes = ornament(ev, key, S.bpm, kind, S.beats, density=density, seed=seed)
    play(track or c.FLUTE, notes)
    return notes


# ---------------- 伴奏の型 ----------------

def bodhran(tr, b, beats, kind, var=0, soft=False):
    """ボーラン（枠太鼓）。低い音＝D3（下の打ち）、高い音＝A3（上の打ち）。
    jig: 下上下・下上下（1・4拍目アクセント）。var=1 で4拍目の前に3連の詰め。slow: 1小節に1〜2打。hornpipe: 下（休）上"""
    w = "," if soft else ""
    if kind == "jig":
        s = f"D3:1!{w} A3:1, D3:1, D3:1! A3:1, D3:1" if var == 0 else f"D3:1!{w} A3:1, D3:1, D3:0.5 D3:0.5 A3:1, D3:1,"
    elif kind == "slipjig":
        s = "D3:1! A3:1, D3:1, D3:1 A3:1, D3:1, D3:1! A3:1, D3:1,"
    elif kind == "reel":
        s = " ".join(["D3:0.5! A3:0.5, D3:0.5, A3:0.5"] * 2) if var == 0 else "D3:0.5 A3:0.5! D3:0.5, A3:0.5 D3:0.5 A3:0.5! D3:0.5, A3:0.5"
    elif kind == "hornpipe":
        s = "D3:0.75! R:0.25 A3:1, D3:0.75! R:0.25 A3:1,"
    elif kind == "waltz":
        s = "D3:1! A3:1, A3:1,"
    else:  # slow
        s = f"D3:{beats / 2}{w} R:{beats / 2}" if var == 0 else f"D3:{beats / 2 + 1}{w} A3:{beats / 2 - 1},"
    tr.bar(b, s)


def open_chord(ch, lo=50, hi=74):
    """開放的な和音（3度を抜き、5度・オクターブ・9度/4度）。DADGAD の響きに近づける"""
    r = PC[re.match(r"^([A-G][#b]?)", ch).group(1)]
    m = 38 + (r - 2) % 12           # 根音 D2〜C#3
    while m < lo - 12: m += 12
    v = [m, m + 7, m + 12, m + 14, m + 19]
    return [x for x in v if x <= hi + 5]


def strum(trs, b, beats, ch, pattern, start_beat=0.0):
    """開放和音のギターのストローク。trs: ギターのトラック（声部の数だけ）。pattern: [(拍, 長さ, 'd' か 'u', 強さの記号)]。
    下ストロークは低い弦から、上は高い弦から、0.02 拍ずつずらす"""
    v = open_chord(ch)
    for pos, L, d, mk in pattern:
        order = list(range(len(trs))) if d == "d" else list(reversed(range(len(trs))))
        for j, i in enumerate(order):
            if i >= len(v): continue
            trs[i].at(round(b * beats + start_beat + pos + 0.02 * j, 4), f"{nm(v[i])}:{L}{mk}")


JIG_STRUM = [(0, 3, "d", "!"), (3, 2, "d", ""), (5, 1, "u", ",")]
JIG_STRUM_LIGHT = [(0, 3, "d", ","), (3, 3, "d", ",")]


def roving_thumb(tr, b, beats, ch, up=True):
    """ハープのローヴィング・サム（根音・5度・オクターブ＋上の経過音）"""
    t = tones(ch.split("|")[0], "D3", "D6")
    r = [x for x in t if x % 12 == PC[re.match(r"^([A-G][#b]?)", ch).group(1)]][0]
    seq = [r, r + 7, r + 12, r + 14, r + 12, r + 7] if up else [r + 12, r + 7, r, r + 7, r + 12, r + 16]
    n = 6 if beats in (3, 6) else 8
    if n == 8: seq = seq + [r + 16, r + 12]
    L = beats / n
    tr.bar(b, " ".join(f"{nm(x)}:{L}" for x in seq[:n]))


def harp_ostinato(tr, b, beats, notes3):
    """右手の3音のオスティナート（8分で回す）"""
    n = int(beats / 0.5) if beats not in (6, 9) else beats
    L = beats / n
    tr.bar(b, " ".join(f"{nm(notes3[i % 3])}:{L}" for i in range(n)))


def drone(trs, b, beats, tonic_midi):
    """ドローン（主音と5度）"""
    trs[0].bar(b, f"{nm(tonic_midi)}:{beats}")
    if len(trs) > 1: trs[1].bar(b, f"{nm(tonic_midi + 7)}:{beats}")
