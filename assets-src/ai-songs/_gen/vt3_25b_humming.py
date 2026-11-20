# vt3 25「25時のハミング」Humming at 25 O'Clock（仮）— 8分の6拍子のアンセム（足ぶみ・手拍子・合唱）。8分音符＝192（付点4分＝64）。ニ長調 → 最後の鼻歌から全音上のホ長調。
# 第3弾（0時〜24時の街）の 24時（アルバムの最後）。
#
# v6（2026-11-21）: ゼロから作り直し。v1〜v5 はシンセポップ・アンセム（148・イ長調）で `vt3_25_humming.py`。
#   人間の指示: 「25もコンセプト練ろう」→ 表と「物語 → 音」を見せて、「25前奏に歌混ぜて作ってみよう」（2026-11-21）。
#   ＝ 前奏は「声だけ」ではなく、ピアノと鼻歌をいっしょに始める。
#
# コンセプト: 日付が変わっても眠れない。ひとりで口ずさんだ鼻歌が、街じゅうで起きている誰かの鼻歌とつながっていく。ひとりの夜を「みんな起きている夜」に書きかえる。
# この曲だけの物: リレー。18〜24 の曲の楽器が、1つずつ、合いことばの節（3・5・6・5・2）をそれぞれの弾き方で鳴らして加わる。
#   フィドル（18）→ チューバ（19）→ クラリネット（20）→ 歪みのギター（21）→ エレピ（22）→ 矩形波のプラック（23）→ カッティングのギター（24）。
#   最後の鼻歌では全員が同じ節を同時に鳴らし、「おやすみ」で来た順の逆に1つずつ抜けて、声だけの節で終わる。
#
# 物語の出来事 → その時の音:
#   ひとりの鼻歌（眠れずに口ずさむ）     → 1小節めから、ピアノの分散和音と鼻歌（合いことばの節）がいっしょに始まる。5小節めに足ぶみ
#   リレー1（夕方と商店街の人）          → 1小節めにフィドル、9小節めにチューバが、節を鳴らして加わる
#   窓の灯（ほかにも起きている人がいる） → 足ぶみと手拍子がそろう。和音が1段ずつ上がる
#   みんなの鼻歌1（声が重なる）          → 歌詞なしの鼻歌と手拍子。指弾きのベースが入る
#   節を回す（間奏）                     → フィドル → チューバ → ピアノ → 全員、と2小節ずつ節をわたす
#   リレー2（銭湯・屋上・丸い窓の前の人）→ クラリネット、歪みのギター、エレピが4小節ごとに加わる
#   窓の灯2・みんなの鼻歌2               → 鼻歌の返事に言葉が入る。ハモリ。足ぶみが増える
#   リレー3（浮かぶ人、鏡の前の人）      → プラック、カッティングのギター。ここで全員そろう。最後の小節の後ろ半分は無音
#   最後の鼻歌（街じゅうが同じ節）       → 全音上がる。合唱と全楽器が、同じ節をそれぞれの弾き方で同時に鳴らす
#   おやすみ（灯が1つずつ消える）        → 来た順の逆に、1小節に1つずつ抜ける。最後は声だけの節
# 歌詞: 曲名は歌わない。「ハミング」「25時」も使わない。
# 声: クリア 1 種類（最後の鼻歌だけ、合唱のパッドとハモリを重ねる）。
from vocalo_lib import *
import gtr2_lib as G2
import random as _r

S = Song("25", "humming", "25時のハミング（仮）", "Humming at 25 O'Clock", 192, 6, "D", "major", "8分の6拍子のアンセム（ボカロ）")
S.kit = "naked-x"; S.flags = "--bass bnb --piano salamander --space hall --space-wet 0.12 " + S.flags
K1, K2 = Key("D", "major"), Key("E", "major")


def up2(chs): return ["/".join(tr_chord(x, 2) for x in c.split("/")) for c in chs]


HCH = ["D", "Em7", "D/F#", "G", "Bm7", "E7", "G", "A7sus4"]
HCH2 = ["D", "Em7", "D/F#", "G", "Bm7", "E7", "A7sus4", "D"]
ACH = ["Bm7", "G", "D/F#", "A", "Bm7", "G", "Em7", "A7sus4"]
BCH = ["G", "A", "F#m7", "Bm7", "G", "A", "Em7", "A7sus4"]
S.scene("ひとりの鼻歌", 8, "verse", HCH)
S.scene("リレー1", 16, "verse", ACH * 2)
S.scene("窓の灯", 8, "pre", BCH)
S.scene("みんなの鼻歌1", 16, "chorus", HCH + HCH2)
S.scene("節を回す", 8, "break", HCH)
S.scene("リレー2", 16, "verse", ACH * 2)
S.scene("窓の灯2", 8, "pre", BCH)
S.scene("みんなの鼻歌2", 16, "chorus", HCH + HCH2)
S.scene("リレー3", 8, "bridge", ["G", "A", "F#m7", "Bm7", "G", "A", "B7sus4", "B7"])
S.scene("最後の鼻歌", 24, "chorus", up2(HCH + HCH2 + HCH2))
S.scene("おやすみ", 12, "outro", up2(["D", "Em7", "D/F#", "G", "D", "Em7", "D/F#", "G", "D", "Em7", "D", "Em7"]))
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.35
# 1回め（BGM）: 始まり −24.5（ピアノ −44）・足ぶみだけが大きい → ピアノ +10dB・フィドル +6dB・チューバ +12dB（boost）、足ぶみを下げる、歪みのギターを下げる
S.drum_gain = {"kick": {"gainDb": -6}, "snare": {"gainDb": -6}, "hihat": {"gainDb": -5}, "crash": {"gainDb": -4}}
MOD = S.sc("最後の鼻歌")[0]


def KEY(b): return K2 if b >= MOD else K1
def SCALE(b): return {(KEY(b).t + x) % 12 for x in (0, 2, 4, 5, 7, 9, 11)}
def chord_of(b): return S.chords[b].split("/")[0]
def root_of(b): return S.chords[b].split("/")[-1] if "/" in S.chords[b] else S.chords[b]


def BST(g): return [{"type": "boost", "gain": g}]


V = Voice(S, vol=0.16, delay=0.5, bright=0.0, patch="surgeFormantPulse", low=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m); RNG = _r.Random(2525)
PNO = [S.track(f"ピアノ{i + 1}", "piano", volume=0.2, pan=-0.05, reverb=0.25, sustain=1.2, fx=BST(10 if i in (0, 4) else 5)) for i in range(5)]      # 2回め: 分散和音（1本）は −32、和音（4本）は −21 と 10dB ちがった → 和音の3本は +5dB に
BASS = S.track("ベース（指弾き）", "bass", volume=0.2, pan=0, duck=0.08, fx=[{"type": "filter", "kind": "highpass", "freq": 30, "q": 0.7}] + BST(6))
FID = S.track("フィドル（18 から）", "strings", patch="violin", recipe="celtic-fiddle", volume=0.12, pan=0.25, reverb=0.4, sustain=1.0, fx=BST(11))
TU = S.track("チューバ（19 から）", "bass", patch="tuba", volume=0.5, pan=-0.1, reverb=0.12, sustain=0.9, fx=BST(12))
CLA = S.track("クラリネット（20 から）", "brass", patch="clarinet", volume=0.5, pan=-0.25, reverb=0.25, fx=BST(6))
GD = [S.track(f"歪みのギター{i + 1}弦め（21 から）", "distGuitar", **rock_gtr_spec(0.045, -0.5, tone="nu-metal-wall")) for i in range(4)]
EP = [S.track(f"エレピ{i + 1}（22 から）", "keys", volume=0.2, pan=0.15, reverb=0.18, sustain=1.2, fx=BST(5)) for i in range(3)]
PLK = S.track("矩形波のプラック（23 から）", "lead", patch="kfbSquarePluck", volume=0.05, pan=0.4, reverb=0.3, fx=[{"type": "pingpong", "beats": 1.5, "mix": 0.2, "feedback": 0.3}])
GC = [S.track(f"カッティングのギター{i + 1}弦め（24 から）", "guitar", amp="clean", volume=0.12, pan=0.5, reverb=0.15, chorus=0) for i in range(6)]
CHO = [S.track(f"合唱{i + 1}", "pad", patch="choir", volume=0.07, pan=0.0, reverb=0.45, fx=[{"type": "widen", "amount": 1.5}]) for i in range(3)]
CLP = S.track("手拍子", "guitar", patch="kawaiiFx", volume=0.06, pan=0.05, reverb=0.2, modulate=False)
SD, SC = G2.Strummer(GD, S, 21), G2.Strummer(GC, S, 24); TRI = [None]

# ================= 歌（度数:長さ。1拍＝8分音符。oct 4 で 1 = D4。最後の鼻歌からは 1 = E4）=================
HUM = ["3:1.5 5:1.5 6:2 5:1", "2:4.5 R:1.5"]                                    # 合いことばの節（3・5・6・5・2）
ANS1 = ["5:1.5 1':1.5 2':2 1':1", "6:4.5 R:1.5"]                                # 返事（上の形）
HUMU = ["3:1.5 5:1.5 6:2 5:1", "2':4.5 R:1.5"]                                  # 節の最後だけ、1オクターブ上へ開く
ANS2 = ["1':1.5 6:1.5 5:2 3:1", "2:4.5 R:1.5"]
ANSE = ["1':1.5 6:1.5 5:2 2:1", "1:5 R:1"]                                  # 主音でとまる返事
CHO8 = HUM + ANS1 + HUMU + ANS2
CHO16 = CHO8 + HUM + ANS1 + HUMU + ANSE
R2 = ["R:6", "R:6"]
VA = ["R:1.5 3:1.5 3:1 2:1 3:1", "5:1.5 3:1.5 2:2 R:1", "R:1.5 1:1.5 1:1 2:1 3:1", "2:1.5 1:1.5 7,:2 R:1",
      "R:1.5 3:1.5 3:1 5:1 6:1", "5:1.5 3:1.5 2:2 R:1", "R:1.5 2:1.5 2:1 4:1 3:1", "2:1.5 1:1.5 2:2 R:1",
      "R:1.5 3:1.5 5:1 6:1 5:1", "6:1.5 5:1.5 3:2 R:1", "R:1.5 1:1.5 2:1 3:1 5:1", "3:1.5 2:1.5 2:2 R:1",
      "R:1.5 3:1.5 3:1 5:1 6:1", "5:1.5 3:1.5 2:2 R:1", "R:1.5 2:1.5 4:1 5:1 6:1", "5:1.5 5:1.5 5:2 R:1"]
VB = ["6:3 6:1 5:1 6:1", "7:2 5:2.5 R:1.5", "5:3 5:1 3:1 5:1", "6:2 3:2.5 R:1.5", "6:3 1':1 7:1 6:1", "7:2 5:2.5 R:1.5", "5:3 5:1 6:1 7:1", "2':2 2':2.5 R:1.5"]
LA = "ららららら"


def put(name, lines, text, bars=None):
    bars = bars or S.sc(name); mel = [KEY(b).mel(x, oct=4) for b, x in zip(bars, lines)]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("ひとりの鼻歌", HUM + R2 + HUM + ANS2, f"{LA}/{LA}/るるるるる")
put("リレー1", VA, "ひづけがかわる/まくらはぬるい/ゆうやけのひと/まだおきてるか/みせじまいした/あのこえもまだ/くちびるがふと/ふしをさがした")
put("窓の灯", VB, "まどのあかり/ひとつふたつ/きえないまま/ゆれているよ")
put("みんなの鼻歌1", CHO16, "/".join([LA] * 8))
put("リレー2", VA, "ゆげのむこうで/だれかがうたう/やねのうえには/ほしをかぞえて/まわるまどべで/まつひともいる/ばらばらのよる/おなじふしだね")
put("窓の灯2", VB, "うかぶひとも/まようひとも/ねむれぬまま/ここにいるよ")
put("みんなの鼻歌2", CHO16, f"{LA}/きこえるよ/{LA}/おなじふし/{LA}/まちじゅうで/{LA}/おきている")
put("リレー3", VB[:4], "みんなおきて/くちずさんで", bars=S.sc("リレー3")[2:6])
put("最後の鼻歌", CHO16 + HUM + ANS1 + HUMU + ANSE, f"{LA}/きこえるよ/{LA}/おなじふし/{LA}/まだだれか/{LA}/おきている/{LA}/{LA}/{LA}/{LA}")
OY = S.sc("おやすみ")
put("おやすみ", HUM + ANS2 + HUM, f"{LA}/るるるるる/{LA}", bars=OY[0:2] + OY[4:6] + OY[10:12])

# ================= リレー: 楽器ごとの「節」の弾き方（2小節。度数:長さ、オクターブ）=================
MF = {"fid": (["3:3 5:1 6:1 5:1", "2:6"], 5), "tuba": (["3:1 R:1 5:1 6:1 R:1 5:1", "2:2 R:4"], 2), "cla": (["R:1 3:1 5:1 6:2 5:1", "2:3 R:3"], 4),
      "gd": (["3:2 5:1 6:2 5:1", "2:6"], 3), "ep": (["3:2 5:1 6:2 5:1", "2:4 R:2"], 4), "plk": (["3:1 3':1 5:1 6:1 6':1 5:1", "2:1 2':1 2:1 2':1 2:2"], 5),
      "pno": (["3:2 5:1 6:2 5:1", "2:4 R:2"], 5), "gc": (["3:2 5:1 6:2 5:1", "2:4 R:2"], 4)}


def motif(who, b, k):
    """who が、b 小節め（節の k 小節め＝0 か 1）に、自分の弾き方で節を鳴らす"""
    lines, o = MF[who]; s = KEY(b).mel(lines[k], oct=o); t = S.bar_beat(b)
    if who == "fid": FID.bar(b, s)
    elif who == "tuba": TU.bar(b, s)
    elif who == "cla": CLA.bar(b, s)
    elif who == "plk": PLK.bar(b, s)
    elif who == "pno": PNO[4].bar(b, s)
    elif who == "ep":                                                    # 上の声が節、下の2つは3度と6度下
        EP[0].bar(b, s)
        for j, d in ((1, -2), (2, -5)): EP[j].bar(b, " ".join(x if x.startswith("R") else f"{N(dia(midi(x.split(':')[0]), d, b))}:{x.split(':')[1]}" for x in s.split()))
    elif who == "gd": G2.octaves(SD, 0, 2, S, b, s)                      # オクターブ奏法
    elif who == "gc": G2.octaves(SC, 3, 5, S, b, s)


def dia(m, k, b):
    sc = [p for p in range(36, 100) if p % 12 in SCALE(b)]; i = min(range(len(sc)), key=lambda j: abs(sc[j] - m)); return sc[i + k]


def strum6(st, b, pat, shape, strong=100, mid=86):
    """8分の6拍子のかき鳴らし（1文字＝8分）。D/d＝ダウン、U/u＝アップ（高い3本）、-＝のばす、.＝止める"""
    t0 = S.bar_beat(b); n = len(shape)
    for i, c in enumerate(pat):
        if c in "-.": continue
        j = i + 1
        while j < 6 and pat[j] == "-": j += 1
        L = j - i - 0.05; hitl = shape if c in "Dd" else shape[-min(3, n):][::-1]
        for k_, (s, m) in enumerate(hitl):
            st.note(s, t0 + i + 0.02 * k_ + (0.01 if c in "Uu" else 0), L, N(m), (strong if c in "DU" else mid) - 2 * k_ + st.rng.randint(-3, 3))


# ---- 役（節を鳴らしていない小節で弾くこと）----
def pno(b, style):
    c = chord_of(b); v = sorted(voice(c, 62, 3)); r = low(root_of(b), "C2")
    if style in ("arp", "arp2"):                                         # 分散和音（右手）＋のばした和音（左手。音が細くならないように）
        PNO[0].bar(b, " ".join(f"{N(m)}:1" for m in ((r, v[0], v[1], v[2], v[1], v[0]) if style == "arp" else (r, v[1], v[2], v[0] + 12, v[2], v[1]))))
        for j in range(3): PNO[j + 1].bar(b, f"{N((r + 12, v[0], v[1])[j])}:6")
    else:                                                                # 和音を付点4分で2回（左手は根音）
        PNO[0].bar(b, f"{N(r)}:3 {N(r + 7)}:2 {N(r)}:1")
        for j in range(3): PNO[j + 1].bar(b, f"{N(v[j])}:3 {N(v[j])}:3" if style == "chord" else f"{N(v[j])}:2 {N(v[j])}:1 {N(v[j])}:2 {N(v[j])}:1")


def bass(b, fill=False):
    r = low(root_of(b), "E1"); nx = low(root_of(b + 1), "E1") if b + 1 < S.nb else r
    BASS.bar(b, f"{N(r)}:3 {N(r + 7)}:2 {N(nx - 1 if nx > r else nx + 1)}:1" if fill else f"{N(r)}:3 {N(r)}:2 {N(r + 7)}:1")


def tuba(b): r = low(root_of(b), "C2"); TU.bar(b, f"{N(r)}:1 R:2 {N(r + 7 if r + 7 <= 50 else r - 5)}:1 R:2")
def fid(b, two=False): v = sorted(voice(chord_of(b), 78, 2)); FID.bar(b, f"{N(v[1])}:6" if not two else f"{N(v[1])}:3 {N(v[0])}:3")
def cla(b): v = sorted(voice(chord_of(b), 68, 2)); CLA.bar(b, f"{N(v[0])}:4 R:2")
def gd(b, pat="D--D-U"): strum6(SD, b, pat, G2.low_shape(chord_of(b), with_third=False)[:3], strong=100, mid=88)
def epc(b): v = sorted(voice(chord_of(b), 64, 3)); [EP[j].bar(b, f"{N(v[j])}:3 {N(v[j])}:2 R:1") for j in range(3)]
def plk(b): v = sorted(voice(chord_of(b), 76, 3)); PLK.bar(b, " ".join(f"{N(m)}:1" for m in (v[0], v[1], v[2], v[0] + 12, v[2], v[1])))


def gc(b, pat="D-uD-u"):
    TRI[0] = G2.triad(chord_of(b), TRI[0]); strum6(SC, b, pat, TRI[0], strong=98, mid=84)


def choir(b):
    v = sorted(voice(chord_of(b), 67, 3))
    for j in range(3): CHO[j].bar(b, f"{N(v[j])}:6")


def g6(s): return s.replace(" ", "")


STOMP1 = (g6("X... .... .... .... .... ...."), "." * 24, "." * 24)                                                     # 足ぶみ1つ
STOMP2 = (g6("X... .... X... .... .... ...."), g6(".... .... .... X... .... ...."), "." * 24)                         # ドン・ドン・パン
STOMP3 = (g6("X... .... X... .... .... X..."), g6(".... .... .... X... .... ...."), g6("x... x... x... x... x... x..."))
STOMP4 = (g6("X... .... X... X... .... X..."), g6(".... .... .... X... .... x..."), g6("x... x... x... x... x... x..."))
FILL = g6("x... x... x.x. X.X. XXXX XXXX")


def stomp(b, g, fill=False, clap=True):
    k, s, h = g; D.set(b, k, FILL if fill else s, "." * 24 if fill else h)
    if clap and s != "." * 24: CLP.bar(b, "R:3 B4:1 R:2")


ORDER = ["fid", "tuba", "cla", "gd", "ep", "plk", "gc"]
ROLE = {"fid": fid, "tuba": tuba, "cla": cla, "gd": gd, "ep": epc, "plk": plk, "gc": gc}

for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1
    if n == "ひとりの鼻歌":                                              # 1小節めから、ピアノと鼻歌がいっしょに始まる
        pno(b, "arp" if not odd else "arp2")
        if i >= 4: stomp(b, STOMP1, clap=False)
    elif n == "リレー1":                                                 # フィドル → チューバ
        pno(b, "arp" if not odd else "arp2"); stomp(b, STOMP1 if i < 8 else STOMP2, fill=last)
        if i < 2: motif("fid", b, i)
        else: fid(b)
        if i >= 8:
            if i < 10: motif("tuba", b, i - 8)
            else: tuba(b)
    elif n in ("窓の灯", "窓の灯2"):
        two = n == "窓の灯2"; pno(b, "chord"); stomp(b, STOMP2 if not two else STOMP3, fill=last); fid(b, two=True); tuba(b)
        if two: cla(b); epc(b); gd(b, "D-----" if not last else "D--D-U"); bass(b)
    elif n in ("みんなの鼻歌1", "みんなの鼻歌2"):
        two = n == "みんなの鼻歌2"; hum_bar = i % 4 in (0, 1)
        pno(b, "chord" if not two else "chord2"); stomp(b, STOMP3 if not two else STOMP4, fill=last); bass(b, fill=i % 4 == 3); tuba(b)
        if i % 8 == 0: crash(D, b, "C2", 6)
        if hum_bar: motif("fid", b, i % 4)                               # 鼻歌の小節は、フィドルもいっしょに節を弾く
        else: fid(b, two=True)
        if two:
            cla(b) if not hum_bar else motif("cla", b, i % 4)
            epc(b); gd(b)
    elif n == "節を回す":                                                # 2小節ずつ、節をわたす: フィドル → チューバ → ピアノ → 全員
        pno(b, "arp" if not odd else "arp2"); stomp(b, STOMP2, fill=last); bass(b)
        who = [("fid",), ("tuba",), ("pno",), ("fid", "tuba", "pno")][i // 2]
        for w in who: motif(w, b, i % 2)
        if "fid" not in who: fid(b)
        if "tuba" not in who: tuba(b)
    elif n == "リレー2":                                                 # クラリネット → 歪みのギター → エレピ（4小節ごと）
        pno(b, "arp" if not odd else "arp2"); stomp(b, STOMP2 if i < 8 else STOMP3, fill=last); bass(b); fid(b); tuba(b)
        for w, start in (("cla", 0), ("gd", 4), ("ep", 8)):
            if start <= i < start + 2: motif(w, b, i - start)
            elif i >= start + 2: ROLE[w](b)
    elif n == "リレー3":                                                 # プラック → カッティングのギター。全員そろう。最後の小節の後ろ半分は無音
        if last:
            r = low(root_of(b), "E1"); v = sorted(voice(chord_of(b), 62, 3))
            D.set(b, g6("X... .... X... .... .... ...."), g6("X... .... X... .... .... ...."), "." * 24); BASS.bar(b, f"{N(r)}:2 {N(r)}:1 R:3"); TU.bar(b, f"{N(r + 12)}:2 {N(r + 12)}:1 R:3")
            for j in range(3): PNO[j + 1].bar(b, f"{N(v[j])}:2 {N(v[j])}:1 R:3"); EP[j].bar(b, f"{N(v[j])}:2 {N(v[j])}:1 R:3")
            strum6(SD, b, "D-D...", G2.low_shape(chord_of(b), with_third=False)[:3]); strum6(SC, b, "D-D...", G2.triad(chord_of(b), TRI[0])); FID.bar(b, f"{N(v[2] + 12)}:3 R:3"); CLA.bar(b, f"{N(v[1])}:3 R:3")
            continue
        pno(b, "chord2"); stomp(b, STOMP4); bass(b, fill=odd); fid(b, two=True); tuba(b); cla(b); gd(b); epc(b)
        for w, start in (("plk", 0), ("gc", 2)):
            if start <= i < start + 2: motif(w, b, i - start)
            elif i >= start + 2: ROLE[w](b)
    elif n == "最後の鼻歌":                                              # 全音上。鼻歌の小節は、全員がそれぞれの弾き方で同じ節
        hum_bar = i % 4 in (0, 1); pno(b, "chord2"); stomp(b, STOMP4, fill=i % 8 == 7 and not last); bass(b, fill=i % 4 == 3); choir(b)
        if i % 8 == 0: crash(D, b, "C2", 6)
        if hum_bar:
            for w in ORDER: motif(w, b, i % 4)
        else:
            for w in ORDER: ROLE[w](b) if w != "fid" else fid(b, two=True)
    elif n == "おやすみ":                                                # 来た順の逆に、1小節に1つずつ抜ける。最後は声だけ
        gone = ORDER[::-1][:i]                                           # i 小節めまでに抜けた楽器
        if i < 10: pno(b, "arp" if not odd else "arp2")
        if i < 8: stomp(b, STOMP2 if i < 4 else STOMP1, clap=i < 4); bass(b)
        for w in ORDER:
            if w not in gone: ROLE[w](b)

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の25（24時・アルバムの最後）。8分の6拍子のアンセム（付点4分＝64）。ニ長調 → ホ長調。眠れない夜の鼻歌が、街じゅうの鼻歌とつながる話。"
          "ピアノと鼻歌がいっしょに始まる → 18〜24 の曲の楽器（フィドル・チューバ・クラリネット・歪みのギター・エレピ・プラック・カッティングのギター）が、"
          "1つずつ合いことばの節を鳴らして加わる → 無音 → 全員が同じ節を鳴らす → 来た順の逆に抜けて、声だけの節で終わる。自作")
SD.end(S.nb); SC.end(S.nb)
finish(S, LY, V, 0)

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "ベース", mid=90, down=12, up=10, seed=25); humanize(path, "ピアノ", mid=82, down=12, up=12, seed=7); humanize(path, "エレピ", mid=80, down=10, up=10, seed=3)
js = load(path); print("  ギターの強さ:", SD.velocity(js) + SC.velocity(js)); save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 10, "pre": 12, "chorus": 24, "bridge": 12, "outro": 10}, scoop=0.12, slash=0.4, vib_min_beats=2.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("みんなの鼻歌2", 0, None, K1), ("最後の鼻歌", 0, None, K2)], vol=0.36)
    voice_by_scene(path, S, {}, default="clear")                        # 1 曲 1 種類の声
    sing_ends(path, S, human=0.5)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path); drum_center(js); save(path, js)
# 1回めを測った（LUFS）: ひとりの鼻歌 −22.9・リレー1 −18.6・窓の灯 −16.4・みんなの鼻歌1 −14.5・みんなの鼻歌2 −12.3・最後の鼻歌 −12.6（始まりが小さく、最後が鼻歌2 より小さい）
#   ピアノは鳴りつづけるので、場面のあいだの差は 1dB ずつの段にする
final_gain(path, {"ひとりの鼻歌": 3.0, "リレー1": 2.0, "窓の灯": 1.0, "みんなの鼻歌1": 0.5, "最後の鼻歌": 1.2, "おやすみ": 1.2})
