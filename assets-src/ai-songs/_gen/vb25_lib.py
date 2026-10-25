# ボカロ曲インスト25曲（作り直し・vb25）の部品（2026-10-25）。
# 表は docs/sound/vp25b-plan.md、依頼文は docs/sound/vocaloid-inst-prompt.md、学んだ型は docs/sound/vocaloid-study.md。
# vp25_lib（場面・度数・ドラムの型）を土台に、ボカロ曲のための部品を足す:
#   ・歌の役のシンセ（声のように聞こえるリード）と、1オクターブ下の重ね（くじらさんの方法）
#   ・歌のような音程の動き（跳躍だけのしゃくり、長い音の後半だけの浅いビブラート）
#   ・ボカロのドラムの型（16分の4つ打ちロック・ハーフ・ジャージークラブ・ドラムンベース・トラップ・ディスコ・8ビート）
#   ・止め（全員休み）・1拍の完全な無音・最後のサビ前の「こもり」（ローパスの写しへの入れかえ）
from vp25_lib import *
from lm25_lib import midi, nm, shift_oct, tok_beats

VGROOVE = {
    # 名前: (キック, スネア, ハイハット)  16分×16
    "vrock": ("X...X...X...X...", "....X.......X...", "XxxxXxxxXxxxXxxx"),       # 16分の4つ打ちロック（wowaka 型）
    "vrock2": ("X.x.X...X.x.X...", "....X..o....X..o", "X.x.X.x.X.x.X.x."),      # 8ビート寄りの疾走
    "beat8": ("X.....x.X.......", "....X.......X...", "X.x.X.x.X.x.X.x."),
    "punk": ("X.X.....X.X.....", "....X.......X...", "X.x.X.x.X.x.X.x."),       # ポップパンクの2ビート寄り
    "half": ("X.........X.....", "........X.......", "X.x.X.x.X.x.X.x."),      # Half feel
    "halfdrive": ("X.....X...X.....", "........X.......", "XxxxXxxxXxxxXxxx"),
    "four": ("X...X...X...X...", "....X.......X...", "..O...O...O...O."),       # 4つ打ち（裏で開く）
    "four16": ("X...X...X...X...", "....X.......X...", "xxOxxxOxxxOxxxOx"),
    "disco": ("X...X...X...X...", "....X.......X...", "x.O.x.O.x.O.x.O."),
    "jersey": ("X..X..X.X..X..X.", "....X.......X...", "x.x.x.x.x.x.x.x."),    # ジャージークラブ（キックの3つ割り）
    "dnb": ("X.........X.....", "....X.......X...", "x.x.x.x.x.x.x.x."),       # ドラムンベース（倍のノリ）
    "trap": ("X.......X.X.....", "........X.......", "xxxxxxxxxxxxXxXx"),      # トラップ（ハットの細かい連打）
    "boombap": ("X.....x...X..x..", "....X.......X...", "x.x.x.x.x.x.x.x."),
    "shuffle": ("X.....X...X.....", "....X.......X...", "x..x..x.x..x..x."),
    "twostep": ("X.......x.x.....", "....X.......X...", "x.xox.x.x.xox.x."),
    "none": ("................", "................", "................"),
}


def vgroove(D, b, name, ghosts=0.3, seed=0, k=None, s=None, h=None, vary=True):
    gk, gs, gh = VGROOVE[name]
    put_groove(D, b, (k or gk, s or gs, h or gh), ghosts=ghosts, seed=seed, hat_vary=vary)


def halt(D, b, beats_on=0, total_beats=4, n=16):
    """止め: 頭の beats_on 拍だけ叩いて、あとは全員休む（ドラム側）"""
    on = int(beats_on * n / total_beats)
    D.K[b] = ("X" + "." * (on - 1) if on else "") + "." * (n - on)
    D.S[b] = ("X" + "." * (on - 1) if on else "") + "." * (n - on)
    D.H[b] = "." * n


class Silence:
    """1拍の完全な無音や止めを記録して、全パートの音をその拍から消す（write の前に apply）"""
    def __init__(self, song):
        self.song = song; self.spans = []

    def add(self, b, from_beat, to_beat):
        B = self.song.beats
        self.spans.append((b * B + from_beat, b * B + to_beat))

    def apply(self):
        for t in self.song.tracks:
            keep = []
            for st, L, x in t.ev:
                en = st + L
                cut = None
                for a, z in self.spans:
                    if st < z - 1e-6 and en > a + 1e-6:
                        cut = (a, z); break
                if cut is None: keep.append((st, L, x)); continue
                a, z = cut
                if st < a - 1e-6: keep.append((st, a - st, x))   # 前は短くする
                # 無音の中で始まる音は消す。無音の後ろにはみ出す長い音は鳴らし直さない（無音のあとは新しい音で入る）
            t.ev = keep
        D = self.song.drums
        if D:
            n = D.n; B = self.song.beats
            for a, z in self.spans:
                b = int(a // B)
                i0 = int(round((a - b * B) * n / B)); i1 = int(round((z - b * B) * n / B))
                for arr in (D.K, D.S, D.H):
                    row = list(arr[b]);
                    for i in range(i0, min(i1, n)): row[i] = "."
                    arr[b] = "".join(row)
                for tr_ in (D.T, D.C):
                    tr_.ev = [(st, L, x) if not (a - 1e-6 <= st < z - 1e-6) else (st, L, "R:" + str(L)) for st, L, x in tr_.ev]
                    tr_.ev = [e for e in tr_.ev if not e[2].startswith("R:")]


# ---------------- 歌の役のシンセ ----------------
def voice_lead_spec(vol=0.21, pan=0.0, delay=0.75, bright=0.0, patch="squareLead"):
    """声のように聞こえるリード（docs/sound/vocaloid-study.md の 3・19〜22）。
    矩形波（squareLead）に、母音「あ」の響きの山（900Hz・1800Hz）と、歌の明るさ（3kHz）を EQ で作る。150Hz より下を切る"""
    fx = [{"type": "filter", "kind": "highpass", "freq": 150, "q": 0.7},
          {"type": "eq", "low": 0, "mid": 5.0, "midHz": 900, "high": 0},
          {"type": "eq", "low": 0, "mid": 3.5, "midHz": 1800, "high": 0},
          {"type": "eq", "low": -1, "mid": 2.5 + bright, "midHz": 3000, "high": -1.5},
          {"type": "filter", "kind": "lowpass", "freq": 8500, "q": 0.7},
          {"type": "pingpong", "beats": delay, "mix": 0.14, "feedback": 0.22},
          {"type": "plate", "mix": 0.15}]
    return P(patch=patch, volume=vol, pan=pan, phrase=8, reverb=0.15, noRestrike=True, mono=True, gainDb=3, fx=fx,
             vibrato={"rate": 5.8, "depth": 24, "delay": 0.45}, autoScoop=False, breath=True)


def voice_low_spec(vol=0.21, patch="squareLead"):
    """1オクターブ下の重ね（ローパス 2kHz、−9dB 相当）"""
    fx = [{"type": "filter", "kind": "highpass", "freq": 120, "q": 0.7},
          {"type": "filter", "kind": "lowpass", "freq": 2000, "q": 0.7},
          {"type": "plate", "mix": 0.12}]
    return P(patch=patch, volume=round(vol * 0.36, 3), pan=0.0, phrase=8, reverb=0.12, noRestrike=True, mono=True, gainDb=0, fx=fx, autoScoop=False)


_TOK = re.compile(r"^([A-G][#b]?-?\d)(:)([0-9.]+)(.*)$")


def sing(s):
    """歌のような音程の動きを付ける: 長二度より大きく上へ跳ぶ音には短いしゃくり（/@0.06）、
    1.5拍以上の音にはビブラート（~。パートの vibrato の delay で後半だけ揺れる）"""
    out, prev = [], None
    for x in s.split():
        m = _TOK.match(x)
        if not m: out.append(x); continue
        n, _, L, mk = m.groups()
        p = midi(n); Lf = float(L)
        if prev is not None and p - prev >= 4 and Lf >= 0.5 and "/" not in mk: mk += "/@0.06"
        if Lf >= 1.5 and "~" not in mk: mk += "~"
        out.append(f"{n}:{L}{mk}"); prev = p
    return " ".join(out)


def plain(s):
    """記号を外す（重ねのパート用）"""
    out = []
    for x in s.split():
        m = _TOK.match(x)
        if not m: out.append(x); continue
        n, _, L, mk = m.groups()
        out.append(f"{n}:{L}")
    return " ".join(out)


class Voice:
    """歌の役（本体＋1オクターブ下の重ね）。v.bar(b, 音の並び) で両方に置く。lo=False で重ねなし"""
    def __init__(self, song, vol=0.21, delay=0.75, bright=0.0, patch="squareLead", low=True):
        self.main = song.track("歌の役（声のシンセ）", "lead", **voice_lead_spec(vol, 0.0, delay, bright, patch))
        self.low = song.track("歌の役（1オクターブ下の重ね）", "pad", **voice_low_spec(vol, patch)) if low else None

    def bar(self, b, s, off=0.0, low=True):
        self.main.bar(b, sing(s), off)
        if low and self.low is not None: self.low.bar(b, shift_oct(plain(s), -1), off)

    def at(self, beat, s, low=True):
        self.main.at(beat, sing(s))
        if low and self.low is not None: self.low.at(beat, shift_oct(plain(s), -1))


def melody(S, K, bars, lines, oct=4):
    """度数の行（1小節1つ）を、bars の小節に置くための音名の並びにする"""
    return [K.mel(l, oct=oct) for l in lines]


# ---------------- 伴奏の部品 ----------------
def piano_arp16(ch, lo="C4", hi="C6", pat=(0, 1, 2, 3, 2, 1, 2, 3)):
    """右手の16分の分散和音（1小節＝16音）"""
    t = tones(ch, lo, hi)
    seq = [t[pat[i % len(pat)] % len(t)] for i in range(16)]
    return " ".join(f"{nm(m)}:0.25" for m in seq)


def piano_left8(ch, lo="C2"):
    r = low(ch, lo)
    return " ".join(f"{nm(r if i % 2 == 0 else r + 12)}:0.5" for i in range(8))


def kick_bass(S, b, style="oct8", lo="E1"):
    return bass_line(S, b, style, lo=lo)


def vtag(S):
    """書き出しの名前（vb25-NN-slug）と、ドラムの音源（crocell-punch を含む）"""
    pass


def vwrite(S, extra_flags=""):
    """vb25 の名前で書き出す。S.kit が crocell-punch のときもフラグを書く"""
    path = sys.argv[1] if len(sys.argv) > 1 else f"/tmp/vp25/vb25-{S.no}-{S.slug}.json"
    kitflag = {"electro": "--drums electro", "naked": "--drums naked", "jpop": "--drums jpop", "crocell-punch": "--drums crocell-punch",
               "crocell": "--drums crocell"}.get(S.kit, "")
    kit0 = S.kit
    if S.kit not in ("electro", "naked", "jpop"): S.kit = "jpop"   # 太鼓の設定（音量など）は jpop と同じ扱い
    S.write(path)
    S.kit = kit0
    open(path + ".flags", "w").write(f"{kitflag} {S.flags} {extra_flags}".strip())
