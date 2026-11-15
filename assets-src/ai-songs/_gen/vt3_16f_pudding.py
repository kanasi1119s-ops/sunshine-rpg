# 16「おやつ宣戦布告」F版（大げさなバラード）。仮。
# 人間（2026-11-16）: スケッチ D・E・F を「全部」1曲に仕上げる。分析ソフト（段2）で分かった3つ（ベースの歩き・コードの動き・歌のリズムのくり返し）を直して作る。
# 曲を決める表:
#   形 … ピアノと歌だけで始まる → 弦が入る → サビの後半でやっとドラム → 弦の間奏 → 2番はバンド → ピアノだけのつなぎ（女神の声）→ 1音上がって最後のサビ → ピアノの和音ひとつで終わる
#   強さ … A 2 → A' 3.5 → サビ1 5→7 → 間奏 6 → A2 5.5 → サビ2 8.5 → つなぎ 1.5 → 最後のサビ 10 → おわり 2
#   旋律の性格 … プリンの取り合いを、わざと壮大に歌い上げる。Aメロは低く語り、サビは長い音で泣かせる（E7 のソ♯、A♭ のミ♭、Fm のラ♭）
# 使い方: VB_VOCAL=1 python3 vt3_16f_pudding.py <出力.json>
from vocalo_lib import *
import random as _r

S = Song("16", "pudding-f", "おやつ宣戦布告 F（仮）", "Snack War F", 84, 4, "C", "major", "大げさなバラード")
S.kit = "crocell-punch"; S.flags = "--bass bnb-loud --ref-tone glossy-jrock --piano salamander --space hall --space-wet 0.14 " + S.flags
K = Key("C", "major"); KD = Key("D", "major"); SC = {0, 2, 4, 5, 7, 9, 11}; SCD = {2, 4, 6, 7, 9, 11, 1}
A_CH = ["C", "Em", "F", "G", "Am", "Em", "F|Fm", "G"]                              # 根音がとなりへ（ミ→ファ→ソ→ラ）
C_CH = ["C", "E7", "Am", "Ab", "F", "Fm", "C|Am", "Bb|G"]                           # Am → A♭（♭VI）、F → Fm、B♭（♭VII）→ G
D_CH = ["D", "F#7", "Bm", "Bb", "G", "Gm", "D|Bm", "C|A"]
S.scene("Aメロ", 8, "verse", A_CH)
S.scene("Aメロ（弦）", 8, "verse", A_CH)
S.scene("サビ1", 8, "chorus", C_CH)
S.scene("間奏", 4, "break", ["Ab", "Bb", "C", "C"])
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("サビ2", 8, "chorus", C_CH)
S.scene("つなぎ", 2, "bridge", ["Ab", "A7"])
S.scene("最後のサビ", 12, "chorus", D_CH + ["G", "Gm", "D|Bm", "A"])
S.scene("おわり", 2, "outro", ["D", "D"])
S.keep_old_synth = True; S.no_depth = True; S.open_hat_vol = 0.35; S.keepers = {}

V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m); RNG = _r.Random(1606)

# ================= 歌 =================
G1, G2, G3, G4, G5, G6, G7, G8 = "x--xx-x-x---x-x-", "x-----x-----....", ".xx-x-x--xx-x---", "x-------x---....", "x-x--xx-x-x--xx-", "x-----------....", "..x-x-xx-x--x-x-", "x---x-------...."
AP = [G1, G2, G3, G4, G5, G6, G7, G8]
AD = ["1 1 1 2 3 2 1", "7, 3", "1 1 6, 1 4 3 1", "2 5", "1 1 3 3 5 3 1 3", "5", "6 6 1' 6 b6 b6 1'", "7 2'"]
A1 = ["さんじのかねがなる", "しろいとびらのおく", "きんのつきがねむる", "となりのおうがきた"]
A1b = ["めとめがあえばほら", "ひけないいくさだよ", "せなかにかぜがふく", "つるぎをぬくときだ"]
A2 = ["こぶしをにぎりしめ", "なんかいでもおなじ", "つきがぬるんでゆく", "わけあうなんていや"]
F1, F2, F3, F4, F5, F6, F7, F8 = "x---x-x-x---x---", "x-----x-------..", "x-x-x---x-x-x---", "x-------x-----..", "..x-x-x-x---x-x-", "x---x-x-------..", "x---x-x-x-x-x---", "x-----------...."
CP = [F1, F2, F3, F4, F5, F6, F7, F8]
CD = ["3 3 2 1 5", "6 #5", "6 6 5 6 1' 2'", "b3' 1'", "6 6 1' 6 1' 2'", "1' b6 1'", "3' 3' 2' 1' 2' 1'", "2'"]
C1 = ["さんじのらんせ", "つきはひとつだけ", "ぎんのつるぎかかげ", "ゆずれぬいくさ"]
C2 = ["さんじのらんせ", "あいこがつづくよ", "まんげつわるなんて", "できないふたり"]
C3 = ["さんじのはるだ", "つきはふたつぶだ", "ぎんのつるぎをおき", "わらうふたりだ", "あすのつきはさかな", "またらんせだね"]
TP, TD, TT = ["x---x-x-x-x-x---", "x-----------...."], ["b6 b6 1' b6 1' b3'", "3'"], ["もうひとつある"]


def put(name, pats, degs, phrases, key=K, o=4):
    lines, text = song_phrases(pats, degs, phrases); bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ", AP, AD, A1); put("Aメロ（弦）", AP, AD, A1b); put("サビ1", CP, CD, C1); put("Aメロ2", AP, AD, A2); put("サビ2", CP, CD, C2)
put("つなぎ", TP, TD, TT); put("最後のサビ", CP + CP[4:], CD + CD[4:], C3, key=KD)

# ================= 伴奏 =================
def halves(b):
    c = S.chords[b].split("|"); return c[0], c[-1]


def nxt(b): return S.chords[b + 1].split("|")[0] if b + 1 < S.nb else halves(b)[1]


def strum(tracks, b, pat, **kw):
    c1, c2 = halves(b)
    if c1 == c2: gtr_strum(tracks, S, b, pat, c1, RNG, **kw)
    else: gtr_strum(tracks, S, b, pat[:8] + "." * 8, c1, RNG, **kw); gtr_strum(tracks, S, b, "." * 8 + pat[8:], c2, RNG, **kw)


def bass(b, pat, kinds):
    c1, c2 = halves(b); BASS.bar(b, walk_bass(pat, kinds, c1, c2, nxt(b), SCD if S.scene_of(b)[0] in ("最後のサビ", "おわり") else SC))


PN = [S.track(f"ピアノ（右手{i + 1}）", "piano", volume=0.1, pan=-0.1 + 0.15 * i, reverb=0.3, sustain=1.6) for i in range(3)]
PL = S.track("ピアノ（左手）", "piano", volume=0.12, pan=-0.2, reverb=0.25, sustain=1.6)
ST = [S.track(f"弦{i + 1}", "strings", volume=0.05, pan=-0.3 + 0.3 * i, reverb=0.4) for i in range(3)]
GL = [S.track(f"Lギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.042, -0.6, drive=0.4)) for i in range(6)]
GR = [S.track(f"Rギター{i + 1}弦め", "distGuitar", **rock_gtr_spec(0.04, 0.6, drive=0.35)) for i in range(6)]
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.24))
# ピアノの右手: 分けて弾く型を小節ごとに変える（下・中・上の番号）
RH = [("x-x-x-x-x-x-x-x-", (0, 1, 2, 1, 0, 1, 2, 1)), ("x-x-x---x-x-x---", (0, 1, 2, 0, 1, 2)), ("x---x-x-x---x-x-", (0, 2, 1, 0, 2, 1)), ("x-x-x-x-x---x-x-", (0, 1, 2, 1, 2, 1, 0))]
WB = [("x-----x-x---x-x-", "1135d"), ("x---x---x-x-x-x-", "1351wd"), ("x-----x-x-x---x-", "1123d"), ("x---x-x-x---x-x-", "11875a"), ("x-----x-x---x-x-", "1535d"), ("x---x---x-x-x-x-", "1231wd")]


def piano(b, rh, stop=None, block=False):
    c1, c2 = halves(b); v = sorted(voice(c1, 64, 3)); v2 = sorted(voice(c2, 64, 3)); pat, order = RH[rh]; r1, r2 = low(c1, "E1") + 12, low(c2, "E1") + 12
    if stop: pat = pat[:stop] + "." * (16 - stop)
    seq = [(v if p < 8 else v2)[q] for p, q in zip([j for j, c in enumerate(pat) if c == "x"], order)]
    PN[0].bar(b, steps(pat, [N(m) for m in seq]))
    if block:                                                                    # サビ: 和音をいっしょに押さえる音も足す（左手と右手で弾く感じ）
        for j in (1, 2): PN[j].bar(b, steps("x-------x-------" if not stop else "x-------........", [N(v[j]), N(v2[j])]))
    PL.bar(b, steps("x-------x-----x-" if not stop else "x-------........", [N(r1), N(r2), N(r2 + 7)]))


def strings(b, pat="x-------x-------", up=12):
    c1, c2 = halves(b); v = sorted(voice(c1, 64, 3)); v2 = sorted(voice(c2, 64, 3))
    for j in range(3): ST[j].bar(b, steps(pat, [N(v[j] + up), N(v2[j] + up)]))


for b in range(S.nb):
    n, i, L, k = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1
    if n == "Aメロ":                                                               # ピアノと歌だけ。8小節目の後ろ1拍半は休み
        piano(b, [1, 2, 1, 2, 0, 2, 0, 1][i], stop=10 if last else None)
    elif n == "Aメロ（弦）":                                                        # 弦が下で支える。5小節目からベース
        piano(b, [0, 2, 0, 1, 0, 2, 3, 1][i], stop=10 if last else None); strings(b, "x---------------" if i < 4 else "x-------x-------", up=0 if i < 4 else 12) if not last else strings(b, "x---------......")
        if i >= 4 and not last: bass(b, "x-------x-----x-", "115")
        if last: bass(b, "x-------x-......", "15"); D.set(b, "................", "..........ooxxXX", "................")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        full = n != "サビ1" or i >= 4; big = n == "最後のサビ"; stop = (n == "サビ1" and i == 3) or (n == "サビ2" and last)
        piano(b, [0, 3, 0, 1][i % 4], stop=8 if stop else None, block=True); strings(b, "x-------x-------" if not stop else "x-------........")
        if full or n != "サビ1":
            bass(b, *(("x-----x-........", "13") if stop else WB[(i + (2 if big else 0)) % 6]))
            strum(GL, b, "x-------........" if stop else "x-------x-------", strings=3); strum(GR, b, "x-------........" if stop else "x-----------x---" if not odd else "x-------x---x---", strings=4)
            feel(D, b, "half", h="X.x.X.x.X.x.X.x." if not big else "X.x.X.xxX.x.X.x.", k="X.........x....." if not odd else "X.....x...x.....")
            if i % 4 == 0: crash(D, b, "C2", 6)
            if i % 4 == 3 and not last: fill_cresc(D, b, 1)
            if stop: fill_cresc(D, b, 2)
        elif i == 3: fill_cresc(D, b, 2)                                           # サビ1の4小節目: 伴奏が止まって、だんだん強くなるフィルで後半へ
        if big and last: fill_cresc(D, b, 2)
    elif n == "間奏":                                                              # 弦が歌う（A♭ → B♭ → C）
        piano(b, [0, 3, 0, 1][i], block=True); bass(b, *WB[i]); strum(GL, b, "x-------x-------", strings=3); strum(GR, b, "x---------------", strings=4)
        c1 = halves(b)[0]; t = [N(m) for m in tones(c1, "C5", "C6")]
        ST[2].bar(b, steps(["x-----x-x---x---", "x-----x-x-x-x---", "x-------x---x-x-", "x-----------...."][i], [[t[0], t[1], t[2], t[1]], [t[0], t[1], t[2], t[1], t[2]], [t[2], t[1], t[0], t[1]], [t[0]]][i]))
        for j in range(2): ST[j].bar(b, steps("x---------------", [N(sorted(voice(c1, 60, 3))[j])]))
        feel(D, b, "half", k="X.........x....." if not odd else "X.....x...x.....")
        if i == 0: crash(D, b, "C2", 6)
        if last: D.set(b, "X...............", "........X.......", "X.x.X.x.........")
    elif n == "Aメロ2":                                                            # バンドで。ベースが歩く。8小節目の後ろ1拍半は休み
        piano(b, [1, 2, 3, 2, 0, 2, 0, 1][i], stop=10 if last else None)
        bass(b, *(WB[(i + 3) % 6] if not last else ("x-----x-x-......", "135")))
        if i >= 4: strings(b, "x---------------" if not last else "x---------......", up=0)
        feel(D, b, "soul8", k=["X.......x.X.....", "X.....x.X.......", "X.......x.X.....", "X..x....X.x....."][i % 4], s="....x.......x..." if i < 4 else None, h="x...x...x...x..." if i < 4 else None)
        if last: D.set(b, "X.......x.......", "....x.....ooxxXX", "x...x...x.......")
    elif n == "つなぎ":                                                            # ピアノだけ。女神の声。2小節目の最後の1拍は休み
        piano(b, 1 if i == 0 else 2, stop=12 if i == 1 else None)
        if i == 1: strings(b, "x-----------....", up=0); D.set(b, "................", "............ooXX", "................")
    elif n == "おわり":
        if i == 0:
            piano(b, 1, block=True); strings(b, "x---------------"); strum(GL, b, "x---------------", strings=3); strum(GR, b, "x---------------", strings=4, lag_ms=20); bass(b, "x---------------", "1")
            D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 6)
        else:
            v = sorted(voice("D", 66, 3))
            for j in range(3): PN[j].bar(b, steps("x-----------....", [N(v[j])]))
            PL.bar(b, steps("x-----------....", [N(low("D", "E1") + 12)]))

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の16「おやつ宣戦布告」のF版（大げさなバラード・84・ハ長調 → 最後のサビはニ長調）。分析ソフトで分かった弱い所"
          "（ベースが根音ばかり・コードが4度5度ばかり・歌のリズムのくり返し）を直して作った。ピアノと歌だけで始まり、ピアノの和音ひとつで終わる。自作")
finish(S, LY, V, 0, level={"verse": -0.1}, special={"Aメロ": -0.3, "つなぎ": -0.5, "最後のサビ": 0.5})

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "ベース", mid=86, down=10, up=8, seed=17); humanize(path, "ピアノ", mid=80, down=12, up=10, seed=18)
js = load(path); gtr_velocity(js, "Lギター", 3); gtr_velocity(js, "Rギター", 4); save(path, js)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 6, "chorus": 20, "最後のサビ": 24, "bridge": 6}, scoop=0.25, slash=0.6, vib_min_beats=1.5, vib_start=0.5, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 4, None, K), ("最後のサビ", 0, None, KD)], vol=0.36)
    for sgn in (-1, 1): harmony(path, S, [("最後のサビ", 0, None, KD)], steps=0, vol=0.2, pan=0.6 * sgn, transpose=0.07 * sgn)
    voice_by_scene(path, S, {"Aメロ": "whisper", "つなぎ": "whisper", "Aメロ（弦）": "cute"}, default="clear")
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.4
    save(path, js)
js = load(path); drum_punch(js); save(path, js)
final_gain(path, {"Aメロ": 2.5, "Aメロ（弦）": 1.0, "サビ1": 0.8, "Aメロ2": -1.6, "サビ2": -0.5, "最後のサビ": 1.5, "おわり": 3.0})   # v1: 歌い出しが小さかった・Aメロ2がサビ1より大きかった・最後のサビがサビ2より小さかった
