#!/usr/bin/env python3
"""「緋色の断章（空間版・6分）」の生成スクリプト。
既存の「緋色の断章（空間版）」と同じ旋律・コードを土台に、約6分（172BPM・258小節）へ広げた版。
ギターソロ（チョーキング）・タッピング・ベースソロ・ドラムソロを入れる。完全オリジナル（CLAUDE.md 1-1）。
実行: python3 assets-src/ai-songs/_gen/scarlet-chapter-space-long.py
注意: 曲の形式にはピッチベンドがないので、チョーキングは「半音ずつ素早く上げて、目標の音で伸ばす」音の並びで表している。
"""
import json
import random

BPM = 172
rnd = random.Random(7)
NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def nm(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"


def md(name):
    import re
    g = re.match(r"^([A-G]#?)(-?\d)$", name)
    return NAMES.index(g.group(1)) + 12 * (int(g.group(2)) + 1)


NAT = {1, 3, 4, 6, 8, 9, 11}   # 嬰ハ短調（自然的）
HAR = {1, 3, 4, 6, 8, 9, 0}    # 嬰ハ短調（和声的）。G#7 の上で使う


def scale_for(chord):
    return HAR if chord == "G#7" else NAT


def step(m, k, pcs):
    """音階の中で k 段動かす。"""
    d = 1 if k > 0 else -1
    for _ in range(abs(k)):
        m += d
        while m % 12 not in pcs:
            m += d
    return m


def snap(m, pcs):
    while m % 12 not in pcs:
        m -= 1
    return m


PROG = {
    "intro": "C#m C#m A B",
    "A": "C#m C#m A B C#m C#m F#m G#7",
    "B": "A B G#m E A B G#m G#7",
    "CH": "A B G#m F#m A B E G#7",
    "SOLO": "C#m A F#m G#7 C#m A B G#7",
    "BR": "F#m E G#m A F#m E B B",
}
# (名前, 種類, 進行, くり返し)
PLAN = [
    ("intro", "intro", "intro", 2),
    ("A1", "A", "A", 1), ("B1", "B", "B", 1), ("C1", "CH", "CH", 1),
    ("A2", "A", "A", 1), ("B2", "B", "B", 1), ("C2", "CH", "CH", 1),
    ("gsolo", "gsolo", "SOLO", 5),
    ("bridge", "bridge", "BR", 2),
    ("tap", "tap", "SOLO", 5),
    ("bsolo", "bsolo", "SOLO", 4),
    ("dsolo", "dsolo", "intro", 4),
    ("build", "build", "BR", 1),
    ("F1", "final", "CH", 1), ("F2", "final2", "CH", 1),
    ("space1", "space", "CH", 2),
    ("space2", "fade", "intro", 4),
    ("end", "end", "intro", 0),
]
# 258 小節に合わせる（最後の空間部は 16 + 16 + 2 小節）
bars = []   # {sec, kind, chord, i(セクション内の小節番号), n(セクションの小節数)}
for name, kind, prog, rep in PLAN:
    cs = PROG[prog].split() * rep
    if kind == "end":
        cs = ["C#m", "C#m"]
    for i, c in enumerate(cs):
        bars.append(dict(sec=name, kind=kind, chord=c, i=i, n=len(cs)))
assert len(bars) == 258, len(bars)

ROOT3 = {"C#m": "C#3", "A": "A2", "B": "B2", "G#m": "G#2", "F#m": "F#2", "E": "E2", "G#7": "G#2"}
TONES = {  # 根音・3度・5度（オクターブ4付近）
    "C#m": ["C#4", "E4", "G#4"], "A": ["A3", "C#4", "E4"], "B": ["B3", "D#4", "F#4"], "G#m": ["G#3", "B3", "D#4"],
    "F#m": ["F#3", "A3", "C#4"], "E": ["E3", "G#3", "B3"], "G#7": ["G#3", "C4", "D#4"],
}
FIFTH = {"C#m": "G#4", "A": "E5", "B": "F#5", "G#m": "D#5", "F#m": "C#5", "E": "B4", "G#7": "D#5"}

# ---- 旋律（既存曲と同じ）----
LEAD = {
    "A": "G#5:1 E5:0.5 G#5:0.5 B5:1.5 A5:0.5 G#5:2 F#5:1 E5:1 E5:1 A5:1 C#6:1.5 B5:0.5 D#6:2 B5:1 F#5:1 G#5:1 E5:0.5 G#5:0.5 B5:1 C#6:1 B5:1.5 G#5:0.5 E5:2 F#5:1 A5:1 C#6:1 A5:1 F#5:1 D#5:1 B4:1 G#4:1",
    "B": "C#6:1 B5:0.5 A5:0.5 E5:2 D#6:1 C#6:0.5 B5:0.5 F#5:2 B5:1 G#5:1 D#6:2 E6:1.5 B5:0.5 G#5:2 A5:1 C#6:1 E6:2 D#6:1 B5:1 F#5:2 C#6:2 B5:1 C#6:1 B5:1 D#6:1 B5:1 G#5:1",
    "CH": "E6:2 C#6:1 E6:1 D#6:2 B5:1 F#5:1 B5:1.5 D#6:0.5 B5:1 G#5:1 A5:1 C#6:1 E6:2 E6:1 C#6:1 A5:2 F#5:1 B5:1 D#6:1 B5:1 G#5:1 B5:1 E6:2 D#6:1.5 B5:0.5 G#5:1 F#5:1",
}


def parse(s):
    out = []
    for t in s.split():
        n, d = t.rsplit(":", 1)
        out.append((n, float(d)))
    return out


for k, v in LEAD.items():
    assert abs(sum(d for _, d in parse(v)) - 32) < 1e-9, k


class Part:
    def __init__(self, instrument, role, volume, pan, amp="auto"):
        self.meta = dict(instrument=instrument, role=role, volume=volume, pan=pan, amp=amp)
        self.ev = []

    def add(self, name, dur):
        self.ev.append((name, dur))

    def rest(self, dur):
        self.ev.append(("R", dur))

    def total(self):
        return sum(d for _, d in self.ev)

    def text(self):
        out = []
        for n, d in self.ev:
            if n == "R" and out and out[-1][0] == "R":
                out[-1] = ("R", out[-1][1] + d)
            else:
                out.append((n, d))
        toks = []
        for n, d in out:
            d = round(d, 4)
            while d > 32:   # 1 つの音符は最大 64 拍までなので、長い休みは分ける
                toks.append(f"{n}:32")
                d = round(d - 32, 4)
            toks.append(f"{n}:{d:g}")
        return " ".join(toks)

    def json(self):
        return dict(**self.meta, notes=self.text())


P = {k: Part(*v) for k, v in dict(
    lead=("leadGuitar", "リードギター（ソロ・タッピング）", 0.25, 0.2, "prs"),
    dist=("distGuitar", "刻みリフ", 0.13, -0.4, "metal"),
    echo=("echoGuitar", "エコーのリード（空間）", 0.2, 0.35, "shoegaze"),
    bass=("bass", "ベース", 0.22, 0, "overdrive"),
    slap=("slap", "ベースソロ（スラップ）", 0.24, 0, "funk"),
    strings=("strings", "弦の厚み", 0.13, 0, "auto"),
    keys=("keys", "鍵盤アルペジオ", 0.12, 0.35, "auto"),
    pad=("pad", "パッド（空間）", 0.15, 0, "auto"),
    bell=("bell", "鐘（遠い光）", 0.12, -0.3, "auto"),
    kick=("kick", "キック", 0.28, 0, "auto"),
    snare=("snare", "スネア", 0.24, 0, "auto"),
    hihat=("hihat", "ハイハット", 0.1, 0.1, "auto"),
    crash=("crash", "クラッシュ", 0.16, -0.2, "auto"),
    tom=("tom", "タム", 0.2, 0.1, "auto"),
).items()}

G = 32  # 1小節 = 32 マス（1マス 0.125 拍）


def drum_bar(grid):
    """grid: {パート名: {マス: 'x'|'X'|'o'}} を 1 小節ぶん書く。"""
    for key in ("kick", "snare", "hihat", "crash", "tom"):
        h = grid.get(key, {})
        for s in range(G):
            if s in h:
                P[key].add(h[s], 0.125)
            else:
                P[key].rest(0.125)


def pat16(kick=(), snare=(), hat=(), crash=(), tom=(), hv="x"):
    """16 分グリッドの番号（0〜15）を 32 マスに直す。"""
    c = lambda lst, v="x": {i * 2: v for i in lst}
    return dict(kick=c(kick), snare=c(snare, "X"), hihat=c(hat, hv), crash=c(crash, "X"), tom=c(tom))


def fill_bar(kind):
    snare = {}
    tom = {}
    for s in range(16, 32):
        (snare if s < 24 else tom)[s] = "x"
    snare[8] = "X"
    return dict(kick={0: "X"}, snare=snare, tom=tom, hihat={0: "x", 4: "x", 8: "x", 12: "x"}, crash={})


def band_drums(b, heavy=False):
    k = b["kind"]
    i, n = b["i"], b["n"]
    first = i == 0
    fill = (i % 4 == 3) and not (i == n - 1 and k in ("final2",))
    if k == "intro":
        g = pat16(kick=(0, 8), hat=(0, 4, 8, 12))
    elif k in ("final", "final2", "gsolo", "tap", "C1", "CH") or heavy:
        g = pat16(kick=(0, 2, 4, 6, 8, 10, 12, 14), snare=(4, 12), hat=tuple(range(0, 16, 2)))
    else:
        g = pat16(kick=(0, 3, 6, 8, 11, 14), snare=(4, 12), hat=tuple(range(0, 16, 2)))
    if fill and k != "intro":
        g = fill_bar(k)
    prev_fill = i > 0 and (i - 1) % 4 == 3
    if first or prev_fill:
        g["crash"] = {0: "X"}
    return g


def rhythm_bar(chord, kind):
    r = ROOT3[chord].replace("2", "3") if chord == "A" or chord in ("G#m", "F#m", "E", "G#7") else ROOT3[chord]
    # 刻みのリフ：3 連続 16 分 + 8 分（既存曲と同じ形）
    for _ in range(4):
        P["dist"].add(r, 0.25)
        P["dist"].add(r, 0.25)
        P["dist"].add(r, 0.5)


def bass_bar(b, nxt):
    c = b["chord"]
    lo = md(ROOT3[c]) - 12
    app = md(ROOT3[nxt]) - 12 - 1 if nxt != c else lo + 7
    seq = [lo, lo, lo + 12, lo, lo, lo, lo + 12, app]
    for m in seq:
        P["bass"].add(nm(m), 0.5)


# ------------------------------------------------------------------ ソロの部品
def bend(target, pcs, hold, steps=2):
    """チョーキング：目標の 1〜2 音下から半音刻みで素早く上げ、目標の音で伸ばす。"""
    lo = target - steps
    ev = [(nm(m), 0.125) for m in range(lo, target)]
    ev.append((nm(target), hold))
    return ev


def run(start, count, direction, pcs, dur=0.25):
    out = []
    m = start
    for _ in range(count):
        out.append((nm(m), dur))
        m = step(m, direction, pcs)
    return out


def pad_events(P_part, ev, total):
    s = sum(d for _, d in ev)
    assert s <= total + 1e-9, (s, total, ev)
    for n, d in ev:
        P_part.add(n, d)
    if total - s > 1e-9:
        P_part.rest(total - s)


def solo_bar(b, idx):
    """ギターソロ 1 小節（4 拍）。idx はソロの中の小節番号（0 始まり）。段々高く激しくなる。"""
    c = b["chord"]
    pcs = scale_for(c)
    t = TONES[c]
    prog = idx / 40.0
    octv = 12 if prog > 0.45 else 0
    root, third, fifth = [md(x) + 12 + octv for x in t]
    m = idx % 4
    if m == 0:  # チョーキング保持
        tgt = snap(fifth + 2 if prog < 0.5 else fifth + 7, pcs)
        ev = bend(tgt, pcs, 2.0, 2) + [(nm(step(tgt, -1, pcs)), 0.5), (nm(step(tgt, -2, pcs)), 0.5), (nm(step(tgt, -3, pcs)), 0.75)]
        ev = ev[:-1] + [(ev[-1][0], 0.5)]
    elif m == 1:  # 下降の 16 分ラン
        ev = run(snap(root + 12 + 4, pcs), 16, -1, pcs, 0.25)
    elif m == 2:  # チョーキング＋リリース、もう一度
        tgt = snap(third + 7, pcs)
        ev = bend(tgt, pcs, 0.875, 1) + [(nm(step(tgt, -1, pcs)), 0.5), (nm(tgt), 0.125)] + bend(snap(tgt + 2, pcs), pcs, 1.5, 2)
        ev.append((nm(snap(tgt, pcs)), 0.5))
    else:  # 上昇ラン＋高音の長いチョーク
        ev = run(snap(root, pcs), 8, +1, pcs, 0.25)
        tgt = snap(root + 14, pcs)
        ev += bend(tgt, pcs, 1.5, 2)
    s = sum(d for _, d in ev)
    # 4 拍に合わせる（足りなければ最後の音を伸ばす、はみ出せば切る）
    if s < 4:
        n, d = ev[-1]
        ev[-1] = (n, d + 4 - s)
    elif s > 4:
        out, acc = [], 0.0
        for n, d in ev:
            if acc + d >= 4:
                out.append((n, round(4 - acc, 4)))
                break
            out.append((n, d))
            acc += d
        ev = out
    for n, d in ev:
        P["lead"].add(n, d)


def tap_bar(b, idx):
    """ライトハンド（タッピング）：和音の 3 音を左手で、高い 1 音を右手で叩く 32 分の流れ。旋律は音階を上下する。"""
    c = b["chord"]
    pcs = scale_for(c)
    t = [md(x) for x in TONES[c]]
    a, bb, cc = t[0] + 12, t[1] + 12, t[2] + 12
    prog = idx / 40.0
    tapped = snap(cc + 12 + (4 if prog > 0.5 else 0), pcs)
    for beat in range(4):
        tp = step(tapped, [0, 2, 1, 3][beat] if idx % 2 == 0 else [3, 1, 2, 0][beat], pcs)
        seq = [a, cc, tp, cc, a, cc, step(tp, 1, pcs), cc]
        for m in seq:
            P["lead"].add(nm(snap(m, pcs) if m != a and m != bb and m != cc else m), 0.125)


# ------------------------------------------------------------------ ベースソロ
def bass_solo_bar(b, nxt, idx):
    c = b["chord"]
    lo = md(ROOT3[c]) - 12 + 12   # 1 オクターブ上（E2〜）。スラップで鳴らす
    fifth = lo + 7
    third = lo + (3 if c in ("C#m", "F#m", "G#m") else 4)
    nxt_lo = md(ROOT3[nxt]) - 12 + 12
    m = idx % 8
    ev = []
    if m < 3:  # 16 分のファンク・グルーブ（根音とオクターブのポップ）
        base = [lo, lo, lo + 12, lo, lo + 12, lo, fifth, lo, lo, lo + 12, lo, lo, fifth, lo + 12, lo, nxt_lo - 1]
        ev = [(nm(x), 0.25) for x in base]
    elif m < 5:  # 歌うフレーズ（長短を混ぜて旋律的に）
        pcs = scale_for(c)
        top = snap(lo + 14, pcs)
        ev = [(nm(top), 0.75), (nm(step(top, -1, pcs)), 0.25), (nm(step(top, -2, pcs)), 0.5), (nm(step(top, -3, pcs)), 0.5),
              (nm(step(top, -2, pcs)), 0.5), (nm(step(top, -4, pcs)), 0.5), (nm(lo + 12), 0.5), (nm(nxt_lo - 1), 0.5)]
    elif m < 7:  # 速い 16 分のハンマリング・ラン（上がって下りる）
        pcs = scale_for(c)
        up = [snap(lo, pcs)]
        for _ in range(7):
            up.append(step(up[-1], 1, pcs))
        seq = up + up[::-1][:-1] + [up[0]]
        ev = [(nm(x), 0.25) for x in seq]
    else:  # スライド風の下降（半音刻み）で次の根音へ
        start = lo + 12 + 7
        ev = [(nm(start - j), 0.25) for j in range(8)] + [(nm(lo + 12), 0.5), (nm(lo + 7), 0.5), (nm(lo), 0.5), (nm(nxt_lo - 1), 0.5)]
    s = sum(d for _, d in ev)
    if s < 4:
        n, d = ev[-1]
        ev[-1] = (n, d + 4 - s)
    elif s > 4:
        out, acc = [], 0.0
        for n, d in ev:
            if acc + d >= 4:
                out.append((n, round(4 - acc, 4)))
                break
            out.append((n, d))
            acc += d
        ev = out
    for n, d in ev:
        # スラップの楽器の音域（E1〜G3）に収める
        mm = md(n)
        while mm > md("G3"):
            mm -= 12
        P["slap"].add(nm(mm), d)


# ------------------------------------------------------------------ ドラムソロ
def drum_solo_bar(idx):
    """16 小節：1〜4 ゴースト、5〜8 ツーバス、9〜12 ずらし、13〜16 ロール。"""
    sec = idx // 4
    j = idx % 4
    if sec == 0:
        sn = {s: ("X" if s in (8, 24) else "o") for s in range(0, 32, 4)}
        if j == 3:
            sn.update({s: "x" for s in range(20, 32, 2)})
        return dict(kick={0: "X", 12: "x", 16: "x", 20: "x"}, snare=sn, hihat={s: "x" for s in range(0, 32, 4)}, crash={0: "X"} if j == 0 else {}, tom={})
    if sec == 1:
        kk = {s: "x" for s in range(0, 32, 2)}
        kk[0] = "X"
        tm = {}
        sn = {8: "X", 24: "X"}
        if j == 3:
            tm = {s: "x" for s in range(20, 32, 2)}
            sn = {8: "X", 16: "x", 18: "x"}
        return dict(kick=kk, snare=sn, hihat={}, crash={0: "X", 16: "X"} if j in (0, 2) else {}, tom=tm)
    if sec == 2:
        kk = {0: "X", 6: "x", 10: "x", 20: "x", 26: "x"}
        sn = {8: "X", 14: "o", 22: "o", 24: "X", 30: "x"}
        hh = {s: ("X" if s % 8 == 0 else "x") for s in range(0, 32, 2)}
        tm = {16 + 2 * q: "x" for q in range(4)} if j == 3 else {}
        return dict(kick=kk, snare=sn, hihat=hh, crash={0: "X"} if j == 0 else {}, tom=tm)
    # ロール：32 分のスネア→タムへ下りてクラッシュ
    if j < 3:
        sn = {s: "x" for s in range(0, 32) if (s < 16 or j == 2)}
        tm = {s: "x" for s in range(16, 32)} if j == 2 else {}
        if j == 2:
            sn = {s: "x" for s in range(0, 16)}
        return dict(kick={0: "X", 8: "x", 16: "x"}, snare=sn, hihat={}, crash={0: "X"} if j == 0 else {}, tom=tm)
    return dict(kick={0: "X", 8: "X", 16: "X", 24: "X"}, snare={s: "x" for s in range(0, 16)}, hihat={}, crash={0: "X"}, tom={s: "x" for s in range(16, 32)})


def soft_heart(b, bar_i):
    return dict(kick={0: "x"} if bar_i % 2 == 0 else {}, snare={}, hihat={}, crash={}, tom={})


def silent():
    return dict(kick={}, snare={}, hihat={}, crash={}, tom={})


# ------------------------------------------------------------------ 組み立て
sec_idx = {}   # セクション名ごとの通し番号
cnt = {}
for b in bars:
    cnt[b["kind"]] = cnt.get(b["kind"], 0)
    b["k"] = cnt[b["kind"]]
    cnt[b["kind"]] += 1

mel_pos = {}


def lead_melody(b, which):
    """A / B / CH の旋律を、セクション内の小節番号に合わせて 1 小節ぶん（4 拍）取り出す。"""
    key = which
    ev = parse(LEAD[key])
    start, acc = b["i"] % 8 * 4, 0.0
    out = []
    for n, d in ev:
        end = acc + d
        lo, hi = max(acc, start), min(end, start + 4)
        if hi > lo:
            out.append((n, round(hi - lo, 4)))
        acc = end
    return out


def third_above(ev, chord):
    pcs = scale_for(chord)
    return [(nm(step(md(n), 2, pcs)), d) for n, d in ev]


for bi, b in enumerate(bars):
    kind, c = b["kind"], b["chord"]
    nxt = bars[bi + 1]["chord"] if bi + 1 < len(bars) else c
    sec_i = b["i"]
    tone = TONES[c]
    fifth = FIFTH[c]

    def lead_set(ev):
        for n, d in ev:
            P["lead"].add(n, d)

    # ---- 既定：全パートを休みにしてから、必要なものだけ書く
    used = {k: False for k in P}

    def use(k):
        used[k] = True

    # リード
    if kind in ("A", "B", "CH"):
        lead_set(lead_melody(b, kind)); use("lead")
    elif kind in ("final", "final2"):
        lead_set(lead_melody(b, "CH")); use("lead")
    elif kind == "gsolo":
        solo_bar(b, b["i"]); use("lead")
    elif kind == "tap":
        tap_bar(b, b["i"]); use("lead")
    elif kind == "build" and b["i"] >= 4:
        # せり上げ：高い 16 分の同音連打（ピッキング）で上がる
        pcs = scale_for(c)
        m = snap(md("E5") + b["i"] - 4, pcs)
        for q in range(8):
            P["lead"].add(nm(step(m, q // 2, pcs)), 0.5)
        use("lead")

    # エコーギター
    if kind == "final2":
        lead_set  # noqa
        for n, d in third_above(lead_melody(b, "CH"), c):
            P["echo"].add(n, d)
        use("echo")
    elif kind == "space":
        for n, d in lead_melody(b, "CH"):
            P["echo"].add(n, d)
        use("echo")
    elif kind == "bridge":
        P["echo"].add(nm(md(tone[2]) + 12 + (12 if b["i"] % 2 else 0)), 4)
        use("echo")
    elif kind == "fade":
        P["echo"].add(nm(md(TONES[c][0]) + 24), 4)
        use("echo")
    elif kind == "end":
        P["echo"].add("C#6", 4)
        use("echo")

    # 刻み
    if kind in ("A", "B", "CH", "gsolo", "tap", "final", "final2", "build"):
        if kind == "build" and b["i"] < 4:
            pass
        else:
            rhythm_bar(c, kind); use("dist")
    elif kind == "dsolo" and b["i"] % 4 == 0:
        # バンドの一撃（1 小節目の頭だけ）
        P["dist"].add(ROOT3[c], 0.5); P["dist"].rest(3.5); use("dist")

    # ベース
    if kind in ("A", "B", "CH", "gsolo", "tap", "final", "final2"):
        bass_bar(b, nxt); use("bass")
    elif kind == "bsolo":
        # ソロの下で、根音をゆっくり支える
        for q in range(4):
            P["bass"].add(nm(md(ROOT3[c]) - 12), 1)
        use("bass")
        bass_solo_bar(b, nxt, b["i"]); use("slap")
    elif kind in ("bridge", "build"):
        for q in range(2):
            P["bass"].add(nm(md(ROOT3[c]) - 12), 2)
        use("bass")
    elif kind in ("space", "fade", "end") and b["i"] % 4 == 0:
        P["bass"].add(nm(md(ROOT3[c]) - 12), 4)
        use("bass")

    # 弦
    if kind in ("A", "B", "CH", "final", "final2", "build", "bridge", "tap"):
        P["strings"].add(fifth, 4); use("strings")
    elif kind == "gsolo" and b["i"] >= 16:
        P["strings"].add(fifth, 4); use("strings")
    elif kind in ("space", "fade"):
        P["strings"].add(fifth, 4); use("strings")

    # 鍵盤
    if kind in ("intro", "A", "B", "bridge", "bsolo", "space", "end", "dsolo"):
        t = [md(x) for x in tone] + [md(tone[0]) + 12]
        pat = [0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 1, 0, 1, 2, 3]
        if kind in ("dsolo",):
            pass
        elif kind in ("bridge", "space", "end", "bsolo"):
            for q in range(2):
                for j in (0, 1, 2, 3):
                    P["keys"].add(nm(t[j]), 0.5)
            use("keys")
        else:
            for j in pat:
                P["keys"].add(nm(t[j]), 0.25)
            use("keys")

    # パッド・鐘
    if kind in ("bridge", "space", "fade", "end", "final2", "dsolo", "bsolo"):
        P["pad"].add(nm(md(tone[1]) - 12), 4); use("pad")
    if kind in ("bridge", "space", "fade", "end") or (kind == "intro" and sec_i >= 4):
        P["bell"].add(nm(md(tone[2]) + 24 if md(tone[2]) + 24 <= md("C7") else md(tone[2]) + 12), 2)
        P["bell"].rest(2)
        use("bell")

    # ドラム
    if kind in ("intro", "A", "B", "CH", "gsolo", "tap", "final", "final2"):
        g = band_drums(b)
        if kind == "tap" and b["i"] < 16:
            g = pat16(kick=(0, 8), snare=(4, 12), hat=tuple(range(0, 16, 2)))
            if b["i"] % 4 == 0:
                g["crash"] = {0: "X"}
    elif kind == "dsolo":
        g = drum_solo_bar(b["i"])
    elif kind == "bsolo":
        g = pat16(kick=(0, 10), snare=(4, 12), hat=tuple(range(0, 16, 4)), hv="o")
    elif kind == "bridge":
        g = soft_heart(b, b["i"])
    elif kind == "build":
        if b["i"] < 4:
            g = soft_heart(b, b["i"])
        else:
            g = dict(kick={0: "x"}, snare={s: "x" for s in range(0, 32, 4 if b["i"] < 6 else 2)}, hihat={}, crash={}, tom={})
            if b["i"] == 7:
                g = dict(kick={0: "X"}, snare={s: "x" for s in range(0, 16)}, hihat={}, crash={}, tom={s: "x" for s in range(16, 32)})
    elif kind == "space":
        g = dict(kick={0: "x"} if b["i"] % 2 == 0 else {}, snare={}, hihat={s: "o" for s in range(0, 32, 8)}, crash={}, tom={})
    elif kind == "fade":
        g = dict(kick={0: "x"} if b["i"] % 4 == 0 else {}, snare={}, hihat={}, crash={}, tom={})
    else:
        g = silent()
    drum_bar(g)

    # 使わなかったパートは 1 小節ぶん休む
    for k in P:
        if k in ("kick", "snare", "hihat", "crash", "tom"):
            continue
        if not used[k]:
            P[k].rest(4)

TOTAL = 258 * 4
for k, p in P.items():
    assert abs(p.total() - TOTAL) < 1e-6, (k, p.total(), TOTAL)

song = dict(
    title="緋色の断章（空間版・6分）",
    description="「緋色の断章（空間版）」と同じ旋律・コードを土台に、約6分に広げた版（仮）。歪んだバンドで2周したあと、チョーキングを多用したギターソロ、32分のタッピング、スラップのベースソロ、ドラムソロを経て、最後のサビから、エコーの壁・パッド・鐘の空間へ溶けていく。注意: 曲の形式にピッチベンドがないため、チョーキングは半音ずつ素早く上げて伸ばす音の並びで表している。",
    bpm=BPM, beats=4,
    chords=" ".join(b["chord"] for b in bars),
    barsPerChord=1, repeats=1, autoAccompaniment=False, feel="rock", tone="rock",
    parts=[p.json() for p in P.values()],
)
import sys
out = sys.argv[1] if len(sys.argv) > 1 else "assets-src/ai-songs/scarlet-chapter-space-long.json"
json.dump(song, open(out, "w", encoding="utf-8"), ensure_ascii=False)
print("書き出し:", out, f"{258 * 4 * 60 / BPM:.0f}秒")
