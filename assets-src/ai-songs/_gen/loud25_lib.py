# ラウドロック・ラウドメタル25曲の作曲エンジン（2026-10-21 人間「曲調を全部変えて同じような曲にならないようにラウドロック、ラウドメタルで25曲作ろう。
#   キーボードをバイオリンやチェロに変えて作ってもいいかも」「ベースでメロディラインをバッキバキに」「7.4を目指そう」）
# 1曲ごとの設計（loud25.py の SPEC）から、AIソング形式の JSON を作る。既存曲の旋律・リフ・進行は写さない（すべてここで作る）。
#   決まりごと（docs/sound/banned-sounds.md）: ギターのビブラート ~ は使わない／しゃくり・自動の揺れは止める（autoScoop・guitarWobble false）／
#   弾いている途中で急にミュートへ切りかえない（ブリッジミュートはパートごと）／音をすぐ切らない（シンバルは次まで鳴らす）／ドラムは単調にしない／
#   ベースの旋律は「動機・問いと答え・コードとの関係」を曲ごとに設計する（音階を上下するだけの自動の型にしない）／バイオリンは柔らかく力強く透き通る設定。
import json, random

NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
FLAT = {"Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#", "Bb": "A#"}
MODES = {
    "aeolian": [0, 2, 3, 5, 7, 8, 10], "phrygian": [0, 1, 3, 5, 7, 8, 10], "dorian": [0, 2, 3, 5, 7, 9, 10],
    "harmonic": [0, 2, 3, 5, 7, 8, 11], "ionian": [0, 2, 4, 5, 7, 9, 11], "lydian": [0, 2, 4, 6, 7, 9, 11],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10], "phrygdom": [0, 1, 4, 5, 7, 8, 10], "locrian5": [0, 1, 3, 5, 6, 8, 10],
}
QUAL = {"": [0, 4, 7], "m": [0, 3, 7], "5": [0, 7], "7": [0, 4, 7, 10], "m7": [0, 3, 7, 10], "maj7": [0, 4, 7, 11],
        "m9": [0, 3, 7, 10, 14], "add9": [0, 4, 7, 14], "madd9": [0, 3, 7, 14], "sus2": [0, 2, 7], "sus4": [0, 5, 7],
        "dim": [0, 3, 6], "aug": [0, 4, 8], "6": [0, 4, 7, 9], "m6": [0, 3, 7, 9], "7sus4": [0, 5, 7, 10]}
SIMPLE = {"5": "", "m9": "m7", "add9": "", "madd9": "m", "sus2": "sus4", "6": "", "m6": "m", "7sus4": "sus4", "aug": "aug"}

def midi(n):
    p, o = (n[:2], n[2:]) if len(n) > 2 and n[1] in "#b" else (n[:1], n[1:])
    p = FLAT.get(p, p)
    return NAMES.index(p) + (int(o) + 1) * 12
def name(m):
    return f"{NAMES[m % 12]}{m // 12 - 1}"
def at_least(pc, low):
    return low + ((pc - low) % 12)
def fold(m, lo, hi):
    while m > hi: m -= 12
    while m < lo: m += 12
    return m

class Chord:
    """'b6maj7' のような「音階の度数＋種類」を、根音の音名と構成音にする"""
    def __init__(self, sym, key, mode):
        acc = 0
        s = sym
        while s and s[0] in "b#":
            acc += -1 if s[0] == "b" else 1; s = s[1:]
        d = 0
        while d < len(s) and s[d].isdigit(): d += 1
        deg = int(s[:d]); q = s[d:]
        if q not in QUAL: raise ValueError(f"コードの種類が読めません: {sym}")
        self.root = (key + MODES[mode][deg - 1] + acc) % 12
        self.q = q; self.iv = QUAL[q]; self.sym = sym
        self.minor = 3 in self.iv and 4 not in self.iv
    def pcs(self):
        return [(self.root + x) % 12 for x in self.iv]
    def label(self):
        return NAMES[self.root] + SIMPLE.get(self.q, self.q)
    def third(self):
        return 3 if self.minor else (4 if 4 in self.iv else (5 if 5 in self.iv else 2 if 2 in self.iv else 4))
    def seventh(self):
        for x in (10, 11):
            if x in self.iv: return x
        return 10 if self.minor else 11

def dur_of(tok):
    return float(tok.split(":")[1].rstrip("!,'_~^/\\"))

class Song:
    def __init__(self, spec):
        self.s = spec
        self.key = NAMES.index(FLAT.get(spec["key"], spec["key"]))
        self.mode = spec["mode"]
        self.beats = spec.get("beats", 4)
        self.res = spec.get("res", 0.25)          # リフ・ドラムの型の1文字の長さ（拍）。6/8 を 8分＝1拍で書くときは 0.5
        self.steps = int(round(self.beats / self.res))
        self.n16 = self.beats * 4
        self.rng = random.Random(spec["seed"])
        self.bars = []  # (sec_id, kind, chord, k, n, sec_no)
        for no, (sid, kind, n, prog) in enumerate(spec["form"]):
            chs = prog.split()
            seq = [chs[i % len(chs)] for i in range(n)] if len(chs) < n else chs[:n]
            for k, c in enumerate(seq):
                self.bars.append((sid, kind, Chord(c, self.key, self.mode), k, n, no))
        self.NB = len(self.bars)
        self.scale = [(self.key + x) % 12 for x in MODES[self.mode]]
        self.low = midi(spec["tuning"])  # ギターのいちばん低い音

    # ── 共通 ──
    def join(self, bars, what=""):
        for i, b in enumerate(bars):
            t = sum(dur_of(x) for x in b.split())
            assert abs(t - self.beats) < 1e-6, (self.s["slug"], what, i, self.bars[i][:2], b, t)
        return " ".join(bars)
    def sec_of(self, i): return self.bars[i][0]
    def nxt(self, i): return self.bars[min(i + 1, self.NB - 1)][2]
    def first_of_sec(self, i): return self.bars[i][3] == 0
    def last_of_sec(self, i): return self.bars[i][3] == self.bars[i][4] - 1
    def has(self, i, sid_prefixes): return any(self.sec_of(i).startswith(p) for p in sid_prefixes)
    def rest(self): return f"R:{self.beats}"

    # ── ギターの刻み（リフの型。1文字＝16分）──
    # X 強い根音・x 根音・m 短く切った根音・- 休み・= 前の音をのばす・o オクターブ上・数字 1〜7＝音階の度数（その小節のコードの根音からの音階の上の音）・b 半音上・f 減5度
    def riff_note(self, ch, c, prev):
        R = at_least(ch.root, self.low)
        if c in "Xxm": return R
        if c == "o": return R + 12
        if c == "b": return R + 1
        if c == "f": return R + 6
        if c.isdigit():
            d = int(c)
            # コードの根音が音階の何番目かを探し、そこから d-1 段上
            pcs = self.scale
            j = pcs.index(ch.root) if ch.root in pcs else 0
            up = (pcs[(j + d - 1) % 7] - ch.root) % 12
            return R + up
        return prev
    def riff_bar(self, pattern, ch, accent_all=False):
        assert len(pattern) == self.steps, (self.s["slug"], pattern, len(pattern), self.steps)
        toks = []; cur = None; dur = 0; mark = ""
        def flush():
            if cur is None: return
            d = dur * self.res
            toks.append(f"{name(cur)}:{d:g}{mark}" if cur != -1 else f"R:{d:g}")
        prev = at_least(ch.root, self.low)
        for c in pattern:
            if c == "=" and cur is not None:
                dur += 1; continue
            flush()
            if c in "-=":
                cur, dur, mark = -1, 1, ""
            else:
                cur = self.riff_note(ch, c, prev); prev = cur; dur = 1
                mark = "!" if c == "X" or accent_all else ("'" if c == "m" else "")
        flush()
        # 休み同士をまとめる
        out = []
        for t in toks:
            if t.startswith("R:") and out and out[-1].startswith("R:"):
                out[-1] = f"R:{dur_of(out[-1]) + dur_of(t):g}"
            else:
                out.append(t)
        return " ".join(out)
    def hits(self, pattern):
        return [c not in "-=" for c in pattern]

    # ── 旋律（リードギター・バイオリン・ピアノの右手など）──
    def chord_tones_in(self, ch, lo, hi):
        return [m for m in range(lo, hi + 1) if m % 12 in ch.pcs()]
    def scale_in(self, lo, hi):
        return [m for m in range(lo, hi + 1) if m % 12 in self.scale]
    def melody(self, bars_idx, rhythm_motifs, lo, hi, start=None, peak_bar=None, end_long=True, var=0):
        """2小節ずつの「問い（A）→答え（B）」。強拍はコードの音、弱拍は音階で近づく。跳躍のあとは反対へ1歩。
        rhythm_motifs: 1小節ぶんの長さの並び（例 [1.5,0.5,1,1]）を複数。印は ! を強拍に付ける"""
        rng = random.Random(self.s["seed"] * 31 + bars_idx[0] * 7 + var)
        sc = self.scale_in(lo, hi)
        cur = start if start is not None else sc[len(sc) // 2]
        out = []
        n = len(bars_idx)
        for j, i in enumerate(bars_idx):
            ch = self.bars[i][2]
            rhy = rhythm_motifs[(j % 4) % len(rhythm_motifs)] if j % 4 != 3 else rhythm_motifs[-1]
            ct = self.chord_tones_in(ch, lo, hi)
            toks = []; pos = 0.0
            # 4小節目（答えの終わり）は長い音で落ち着く
            if end_long and j % 4 == 3:
                rhy = [r for r in rhythm_motifs[-1]]
            target_dir = 1 if (peak_bar is not None and j < peak_bar) else (-1 if peak_bar is not None and j > peak_bar else rng.choice([-1, 1]))
            for q, d in enumerate(rhy):
                strong = abs(pos - round(pos)) < 1e-6 and int(round(pos)) % 2 == 0
                if strong or q == 0 or d >= 0.75:   # 強拍と長い音はコードの音
                    cands = sorted(ct, key=lambda m: abs(m - (cur + target_dir * rng.choice([0, 2, 3, 4]))))
                    nxtm = cands[0] if cands else cur
                    if j % 4 == 3 and q == len(rhy) - 1:   # 答えの最後は根音か3度
                        stable = [m for m in ct if m % 12 in (ch.root, (ch.root + ch.third()) % 12)]
                        if stable: nxtm = min(stable, key=lambda m: abs(m - cur))
                else:
                    k0 = min(range(len(sc)), key=lambda k: abs(sc[k] - cur))
                    step = rng.choice([1, 1, 1, 2, -1]) * target_dir
                    if rng.random() < 0.1: step = target_dir * rng.choice([3, 4])
                    nxtm = sc[max(0, min(len(sc) - 1, k0 + step))]
                    # 和音の音の半音上（ぶつかる音）は避けて、もう1段進む
                    if any((nxtm - p) % 12 == 1 for p in ch.pcs()):
                        nxtm = sc[max(0, min(len(sc) - 1, k0 + step + (1 if step > 0 else -1)))]
                if abs(nxtm - cur) >= 5:   # 跳躍のあとは、次で反対向きに戻れるよう向きを変える
                    target_dir = -target_dir
                cur = nxtm
                mk = "!" if strong and q == 0 else ""
                toks.append(f"{name(cur)}:{d:g}{mk}")
                pos += d
            out.append(" ".join(toks))
        return out

    # ── ベース（曲ごとの動機。度数の記号で書く）──
    # 記号: R 根音・5・8（オクターブ）・3・7・4・9（2度）・6・b（次のコードの根音へ半音で寄る）・n（次の根音）・- 休み。長さは「記号:拍」。印 ! ' は旋律と同じ
    def bass_tone(self, ch, nxtch, sym, lo, hi):
        R = at_least(ch.root, lo)
        if sym == "R": return R
        if sym == "8": return fold(R + 12, lo, hi)
        if sym == "5": return fold(R + 7, lo, hi)
        if sym == "3": return fold(R + ch.third(), lo, hi)
        if sym == "7": return fold(R + ch.seventh(), lo, hi)
        if sym in "469":
            pcs = self.scale; j = pcs.index(ch.root) if ch.root in pcs else 0
            d = {"4": 3, "6": 5, "9": 1}[sym]
            return fold(R + (pcs[(j + d) % 7] - ch.root) % 12, lo, hi)
        nr = at_least(nxtch.root, lo)
        if sym == "n": return nr
        if sym == "b":   # 次の根音へ半音で寄る（同じなら5度）
            if nr % 12 == R % 12: return fold(R + 7, lo, hi)
            return fold(nr - 1 if (nr - R) % 12 <= 6 else nr + 1, lo, hi)
        if sym == "a":   # 次の根音へ全音で寄る（音階の上の音）
            return fold(nr - 2 if (nr - R) % 12 <= 6 else nr + 2, lo, hi)
        raise ValueError(sym)
    def bass_bar(self, motif, ch, nxtch, hi=None):
        hi = hi if hi is not None else midi("D3")
        toks = []
        for t in motif.split():
            sym, rest = t.split(":", 1)
            mk = "".join(c for c in rest if c in "!',")
            d = rest.rstrip("!',")
            if sym == "-":
                toks.append(f"R:{d}")
            else:
                toks.append(f"{name(self.bass_tone(ch, nxtch, sym, midi('A1'), hi))}:{d}{mk}")
        return " ".join(toks)

    def lock_bass(self, pattern, ch):
        """刻みの型と同じリズムで、根音（ベースの低い音域）を弾く。数字・o などの動く音も、ベースは根音のまま（低音を重ねて濁らせない）"""
        R = at_least(ch.root, midi("E1"))   # 刻みの1オクターブ下（ベースの低い音域 E1〜D#2）
        toks = []; cur = None; dur = 0; mark = ""
        def flush():
            if cur is None: return
            toks.append(f"{name(R)}:{dur * self.res:g}{mark}" if cur else f"R:{dur * self.res:g}")
        for c in pattern:
            if c == "=" and cur is not None:
                dur += 1; continue
            flush()
            cur, dur = (c not in "-="), 1
            mark = "!" if c == "X" else ("'" if c == "m" else "")
        flush()
        return " ".join(toks)

    def grid(self, rows, what):
        for i, r in enumerate(rows):
            assert len(r) == self.steps, (self.s["slug"], what, i, r, len(r))
        k = int(round(self.res / 0.25))
        return "g:" + "".join("".join(c + "." * (k - 1) for c in r) for r in rows)

def merge_long(tokens_by_bar, beats):
    """同じ音が続く全音符をつなげる（8拍まで）"""
    out = []
    for b in tokens_by_bar:
        out.extend(b.split())
    res = []
    for t in out:
        nm, d = t.split(":", 1)
        if res and nm != "R" and "!" not in d and "," in d and res[-1].split(":")[0] == nm and res[-1].endswith(",") and dur_of(res[-1]) + dur_of(t) <= 8:
            res[-1] = f"{nm}:{dur_of(res[-1]) + dur_of(t):g},"
        else:
            res.append(t)
    return " ".join(res)
