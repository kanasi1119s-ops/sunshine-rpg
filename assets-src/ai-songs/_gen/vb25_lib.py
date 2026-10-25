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
def voice_lead_spec(vol=0.21, pan=0.0, delay=0.75, bright=0.0, patch="picoLeadRound"):
    """歌の役（2026-10-25 人間「リードをもう少しクリアのがいい」「この感じいい」→ 25曲もこれで）: クリアなポップのリード（popLeadClear）。
    うねり・歪み・下の重ねなし。EQ は 3kHz を少しだけ。ピンポンディレイ 10%・プレート 14%、ビブラートは浅く音の後半だけ"""
    fx = [{"type": "filter", "kind": "highpass", "freq": 170, "q": 0.7},
          {"type": "eq", "low": 0, "mid": 1.0 + bright, "midHz": 3000, "high": 0},
          {"type": "pingpong", "beats": delay, "mix": 0.16, "feedback": 0.3},
          {"type": "plate", "mix": 0.18}]
    return P(patch=patch, volume=vol, pan=pan, phrase=8, reverb=0.14, noRestrike=True, mono=True, gainDb=3, fx=fx,
             vibrato={"rate": 5.5, "depth": 14, "delay": 0.5}, autoScoop=False, breath=True)


def voice_low_spec(vol=0.21, patch="picoLeadRound"):
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


class _NoTrack:
    """重ねなしのときの空のパート（台本が V.low に書いても鳴らない）"""
    spec = {}; ev = []
    def bar(self, *a, **k): return 0
    def at(self, *a, **k): return 0


class Voice:
    """歌の役（本体＋1オクターブ下の重ね）。v.bar(b, 音の並び) で両方に置く。lo=False で重ねなし"""
    def __init__(self, song, vol=0.21, delay=0.75, bright=0.0, patch="picoLeadRound", low=False):
        self.main = song.track("歌の役（声のシンセ）", "lead", **voice_lead_spec(vol, 0.0, delay, bright, patch))
        # 重ねのパートはいつも作る（台本が V.low に直接書く「こもった歌」に使う）。low=False のときは、歌の役を写して重ねない
        self.double = low
        self.low = song.track("歌の役（こもった写し）", "pad", **voice_low_spec(vol, patch))

    def bar(self, b, s, off=0.0, low=True):
        self.main.bar(b, sing(s), off)
        if low and self.double: self.low.bar(b, shift_oct(plain(s), -1), off)

    def at(self, beat, s, low=True):
        self.main.at(beat, sing(s))
        if low and self.double: self.low.at(beat, shift_oct(plain(s), -1))


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


def playable(S):
    """人間が叩ける打ち込みにする（2026-10-25 人間「テンポは速いけど、打ち込みの数も多い必要はない。人間が絶対叩けない打ち込みが多すぎるのも違う」）。
    ・16分のハイハットは、16分の速さが 1秒に 10 打を超える（テンポ 150 より上）と片手では刻めないので、8分にする（強い打ちは残す）
    ・キックの16分の連打（となりどうし）は、テンポ 150 より上では後ろを消す（1つの足で踏めない）
    ・スネア・タムは両手なので16分のフィルはよいが、32分（0.125 拍）の連打は消す（テンポ 120 より上）
    S.allow_fast（場面の名前の集合）に入れた場面だけは、そのまま（トラップのハットの細かい連打など、打ち込みの音楽として作る所）"""
    D = S.drums
    if D is None: return 0
    n = D.n; B = S.beats; changed = 0
    allow = getattr(S, "allow_fast", set())
    tmap = {e["bar"] - 1: e["bpm"] for e in S.tempo}
    bpm = S.bpm
    for b in range(S.nb):
        if b in tmap: bpm = tmap[b]
        name = S.scene_of(b)[0]
        if name in allow: continue
        rate = bpm / 60 * (n / B)          # 1秒の16分の数
        if rate > 10:
            h = list(D.H[b])
            for i in range(1, n, 2):
                if h[i] != "." and h[i] != "O": h[i] = "."; changed += 1
                elif h[i] == "O" and h[i - 1] == ".": h[i - 1] = "O"; h[i] = "."; changed += 1
            D.H[b] = "".join(h)
            k = list(D.K[b])
            for i in range(1, n):
                if k[i] != "." and k[i - 1] != ".": k[i] = "."; changed += 1
            D.K[b] = "".join(k)
    if bpm > 120:
        for tr_ in (D.T,):
            tr_.ev = [e for e in tr_.ev if e[1] > 0.13]
    if changed: print(f"  人間が叩ける打ち込みにした: {changed}打を減らした")
    return changed


# 2026-10-25 人間「電子音をもっと現代的に。ボカロっぽいシンセじゃない」→ 作曲ソフトに現代的なシンセ10種を足した（docs/sound/modern-synth-study.md）。
# 書き出しのときに、古いシンセの音色を新しいものへ置きかえる（台本の中の名前はそのままでよい）。チップチューンの音はそのまま（わざとの懐かしい音）
MODERN = {"squareLead": "modernLead", "sawLead": "brightLead", "supersawPad": "modernSupersaw", "pluckSynth": "modernPluck",
          "warmPad": "modernPad", "synthBass1": "modernBass", "synthBass2": "modernBass", "polysynth": "fbChord"}


def modernize(S):
    n = 0
    for t in S.tracks:
        p = t.spec.get("patch")
        if p in MODERN and not getattr(S, "keep_old_synth", False):
            t.spec["patch"] = MODERN[p]; n += 1
    if n: print(f"  現代的なシンセに置きかえた: {n}パート")


def muffle(S, tracks, bars, freq=800):
    """最後のサビの前の「こもり」: tracks の、bars の間の音を、ローパスを掛けた写しのパートへ移す（写しは1つの楽器に1つ作る）"""
    bars = set(bars); B = S.beats
    for t in tracks:
        cp = S.track(t.role + "（こもり）", t.inst, **dict(t.spec))
        fx = [f for f in cp.spec.get("fx", []) if f.get("kind") != "lowpass"]
        cp.spec["fx"] = [{"type": "filter", "kind": "lowpass", "freq": freq, "q": 0.9}] + fx
        keep = []
        for e in t.ev:
            if int(e[0] // B) in bars: cp.ev.append(e)
            else: keep.append(e)
        t.ev = keep
    return S


def ride(D, b, pattern="x.x.x.x.", note="D2"):
    """ライド（8分の型。x=ふつう・X=強く・B=ベル）。シンバルのパートに書く"""
    step = D.song.beats / len(pattern)
    for i, c in enumerate(pattern):
        if c == ".": continue
        nn = "F2" if c == "B" else note
        D.C.at(b * D.song.beats + i * step, f"{nn}:{step:g}" + ("!" if c in "XB" else ""))


SEASON = {"蝉": "C4", "夕方の蝉": "C#4", "鈴虫": "D4", "コオロギ": "D#4", "雨": "E4", "風鈴": "F4", "小鳥": "F#4", "波": "G4",
          "雪の鈴": "G#4", "秋風": "A4", "そよ風": "A#4", "手拍子": "B4", "カウベル": "C5", "指パッチン": "C#5", "花火": "D5"}


def season(S, bar, kind, beats=16, vol=0.09, pan=0.0, every=None):
    """季節の音（作曲ソフトの seasonFx。2026-10-25 人間「季節を感じれる様な音も欲しい」）。
    bar 小節目から beats 拍ぶん。every を書くと、その拍ごとに鳴らし直す（長い雨や虫の声をつなぐ）"""
    key = f"season-{kind}"
    t = getattr(S, "_season", {}).get(key)
    if t is None:
        t = S.track(f"季節の音（{kind}）", "pad", patch="seasonFx", volume=vol, pan=pan, reverb=0.15, modulate=False)
        S.__dict__.setdefault("_season", {})[key] = t
    st = bar * S.beats; step = every or beats; k = 0
    while k < beats - 1e-6:
        L = min(step, beats - k); t.at(st + k, f"{SEASON[kind]}:{L:g}"); k += L
    return t


def depth(S):
    """深み・スケール・頭の中を支配する感じ（2026-10-25 人間「音に深みとスケール、頭の中を支配する感じが欲しい」）。
    ・左右いっぱいの深いパッド（低めの和音をのばす。小さく）を、止め・ブレイク以外の全場面に
    ・サビ（chorus）では高いきらめき（C6〜C7 のベル。2小節に1回）
    ・空間はホールを薄く（--space hall --space-wet 0.15。曲に空間の指定があればそちら）"""
    if getattr(S, "no_depth", False): return
    PADD = [S.track(f"深いパッド{i + 1}", "pad", patch="modernPad", volume=0.04, pan=[-0.75, 0.75][i], reverb=0.5) for i in range(2)]
    SPK = S.track("高いきらめき", "bell", patch="popBell", volume=0.045, pan=0.5, reverb=0.6)
    for b in range(S.nb):
        n, i, L, k = S.scene_of(b)
        if k in ("break",): continue
        ch = S.chords[b].split("|")[0]
        w = voice(ch, 55, 2, spread=True)
        for j in range(2): PADD[j].bar(b, f"{nm(w[j])}:{S.beats}")
        if k in ("chorus", "drop") and i % 2 == 1:
            t = tones(ch, "C6", "C7")[:S.beats]
            SPK.bar(b, " ".join(f"{nm(x)}:1" for x in t))
    if "--space" not in S.flags: S.flags += " --space hall --space-wet 0.15"


def vwrite(S, extra_flags=""):
    """vb25 の名前で書き出す。S.kit が crocell-punch のときもフラグを書く"""
    path = sys.argv[1] if len(sys.argv) > 1 else f"/tmp/vp25/vb25-{S.no}-{S.slug}.json"
    playable(S)
    depth(S)
    modernize(S)
    kitflag = {"electro": "--drums electro", "naked": "--drums naked", "jpop": "--drums jpop", "crocell-punch": "--drums crocell-punch",
               "crocell": "--drums crocell"}.get(S.kit, "")
    kit0 = S.kit
    if S.kit not in ("electro", "naked", "jpop"): S.kit = "jpop"   # 太鼓の設定（音量など）は jpop と同じ扱い
    S.write(path)
    S.kit = kit0
    open(path + ".flags", "w").write(f"{kitflag} {S.flags} {extra_flags}".strip())
