# vt25 20「となりのセンパイ・ブルース」Senpai Next Door Blues（仮）— ブルースロック（8分のシャッフル）。120・4/4。E（12小節のブルース）→ 最後のサビは F。
# 物語: となりの席のセンパイは、いつもため息で「まあいいか」が口ぐせ。コーヒーに砂糖を3つ入れる、苦いのがきらいな人。
#   かっこつけないのが、ずるい。教わったことは「まあいいか」だけ……と思っていた。来月から、となりの席にはだれも座らない。
#   砂糖があまる。今度は「わたし」が、だれかのとなりで「まあいいか」って言う番。ありがとう。
# 場面と強さ: イントロ（ギターのブギ）→ Aメロ1（12小節のブルース。歌って、ギターが答える）→ Bメロ1 → サビ1 → 間奏 → Aメロ2 → Bメロ2 → サビ2
#   → ギターソロ（サチュレーターで温かく歪ませる）→ ストップタイム（バンドは小節の頭だけ。歌が一人で語る）→ 落ちサビ（静か）
#   → 最後のサビ（F へ +1・いちばん強い）→ 終わり（ブルースの決めで終わる）
# 旋律の性格: Aメロは「歌う → ギターが答える」のかけ合い（ブルースの型）。♭3（G）を3（G#）へずり上げる青い音。サビはのびやかなポップ。
# ほかの曲とちがう所: 全体が3連で跳ねるシャッフル（旋律もベースもギターも、まっすぐ書いて3連の長さに直す）。ストップタイム。
import math
import re
from vt25_lib import *

S = Song("20", "senpai", "となりのセンパイ・ブルース（仮）", "Senpai Next Door Blues", 120, 4, "E", "major", "ロック（ブルースロック・シャッフル・ボカロ）")
S.kit = "jpop"
S.flags = S.flags + " --piano salamander --space room --space-wet 0.16"
S.no_spice = True        # 遊びの16分（まっすぐ）を足さない（シャッフルがくずれるため）
K = Key("E", "mixolydian")      # 歌（oct 4 で 1 = E4。歌うのは B3〜F#5）
KL = Key("F", "major")          # 最後のサビ（oct 4 で 1 = F4）

_DUR = re.compile(r"^([0-9.]+)(.*)$")


def warp(t):
    """シャッフルの時間の曲げ方: 拍の前半（0〜0.5）を 0〜2/3 に、後半（0.5〜1）を 2/3〜1 に"""
    b = math.floor(t + 1e-9); f = t - b
    return b + (f * 4 / 3 if f <= 0.5 + 1e-9 else 2 / 3 + (f - 0.5) * 2 / 3)


def swing(s):
    """まっすぐ書いた並び（1小節）を、3連の跳ねる長さに直す"""
    out, t = [], 0.0
    for x in s.split():
        n, v = x.split(":", 1)
        m = _DUR.match(v); L = float(m.group(1)); mk = m.group(2)
        a, z = warp(t), warp(t + L)
        out.append(f"{n}:{z - a:.4f}{mk}"); t += L
    return " ".join(out)


BLUES = ["E7", "A9", "E7", "E7", "A9", "A9", "E7", "C#7", "F#m7", "B7", "E7", "B7"]
B_CH = ["C#m7", "G#m7", "Amaj7", "B7"]
C_CH = ["Amaj7", "B7", "G#m7", "C#m7", "F#m7", "B7", "E", "E7"]
STOP = ["E7", "E7", "A7", "A7", "E7", "E7", "B7", "B7"]
LAST = [tr_chord(c, 1) for c in C_CH + C_CH] + ["Bb9", "F7", "Gm7", "F"]

S.scene("イントロ", 12, "intro", BLUES)
S.scene("Aメロ1", 12, "verse", BLUES)
S.scene("Bメロ1", 4, "pre", B_CH)
S.scene("サビ1", 8, "chorus", C_CH)
S.scene("間奏", 8, "break", BLUES[4:])
S.scene("Aメロ2", 12, "verse", BLUES)
S.scene("Bメロ2", 4, "pre", B_CH)
S.scene("サビ2", 8, "chorus", C_CH)
S.scene("ギターソロ", 12, "solo", BLUES)
S.scene("ストップタイム", 8, "bridge", STOP)
S.scene("落ちサビ", 8, "bridge", C_CH[:7] + ["C7"])       # 最後の小節は F への入り口（C7）
S.scene("最後のサビ", 20, "chorus", LAST)
S.scene("終わり", 8, "outro", ["F7", "Bb9", "F7", "D7", "Gm7", "C7", "F9", "F9"])

V = Voice(S, vol=0.21, delay=0.75, bright=0.6, patch="popLeadClear", low=True)
GR = S.track("ギター1（ブギの根音）", "distGuitar", **rock_gtr_spec(0.055, -0.5, drive=0.45))
GU = S.track("ギター1（ブギの上の音）", "distGuitar", **rock_gtr_spec(0.05, -0.35, drive=0.45))
LG = S.track("ギター2（答え・ソロ）", "leadGuitar", **lead_gtr_spec(0.12, 0.25))
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.22))
PNFX = [{"type": "eq", "low": -3, "mid": -1, "midHz": 400, "high": 2.5}]
PN = [S.track(f"ピアノ{i + 1}", "piano", volume=0.085, pan=0.2, reverb=0.22, fx=PNFX) for i in range(3)]
PNL = S.track("ピアノ（左手）", "piano", volume=0.08, pan=0.15, reverb=0.2, fx=PNFX)
EP = [S.track(f"エレピ{i + 1}", "keys", patch="surgeKeysDxEp", volume=0.06, pan=-0.2 + 0.2 * i, reverb=0.3, sustain=1.2) for i in range(3)]
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.05, pan=-0.35 + 0.35 * i, reverb=0.45, sustain=1.5) for i in range(3)]
_dspec = lambda k: {kk: vv for kk, vv in NAKED[k].items() if kk != "human"}
HATS = S.track("ハイハット（シャッフル）", "hihat", **_dspec("hihat"))
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.05, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 5,:0.5 1:0.5 1:0.5 b3:0.5 3:0.5 1:1", "5,:1 1:2 R:1", "R:4", "R:4",
      "R:0.5 4:0.5 4:0.5 4:0.5 6:0.5 4:0.5 b3:1", "1:1 1:2 R:1", "R:4", "R:4",
      "R:0.5 5:0.5 5:0.5 5:0.5 b7:0.5 5:0.5 4:1", "4:0.5 2:1.5 R:2", "R:4", "R:4"]
A1 = "となりのせんぱい/いつもためいきで/まあいいかのひと"
A2 = "こーひーにさとう/さんこもいれてる/にがいのはきらい"
VB = ["R:1 3:0.5 3:0.5 3:0.5 2:0.5 1:1", "2:2 R:2", "R:1 4:0.5 4:0.5 4:0.5 3:0.5 2:1", "5:2 R:2"]
B1 = "かっこつけない/ずるいひとね"
B2 = "ならったことは/まあいいかね"
VC = ["R:0.5 1:0.5 3:0.5 4:0.5 6:1 5:1", "5:1.5 4:0.5 3:1 R:1", "R:0.5 3:0.5 5:0.5 1':0.5 7:1 5:1", "5:1.5 6:0.5 5:1 R:1",
      "R:0.5 6:0.5 6:0.5 6:0.5 1':1 6:1", "5:1.5 4:0.5 2:1 R:1", "R:0.5 3:0.5 5:0.5 6:0.5 1':1 2':1", "1':2 R:2"]
VCL = VC[:6] + ["R:0.5 3:0.5 5:0.5 6:0.5 7:1 1':1", "1':2 R:2"]
TAG = ["R:0.5 5:0.5 5:0.5 5:0.5 6:1 5:1", "3:1 1:1 R:2", "R:1 2:1 3:1 5:1", "1':3 R:1"]
C1 = "せんぱいのとなり/ちょっとだけぶるーす/まあいいかっていう/そのよこがお"
C2 = "せんぱいのとなり/ちょっとだけあまくて/さとうさんこぶん/おひるやすみ"
C3 = "せんぱいのとなり/こんどはわたしが/まあいいかっていう/ばんなのかな"
CL = ("せんぱいのとなり/ちょっとだけぶるーす/まあいいかっていう/そのよこがお/"
      "せんぱいのとなり/いまでもあまいよ/さとうさんこぶん/ありがとうね/まあいいかってね/わらおう")
VX = ["R:0.5 5:0.5 5:0.5 5:0.5 b7:0.5 5:0.5 3:1", "b3:1 1:1 R:2", "R:0.5 4:0.5 4:0.5 4:0.5 6:0.5 4:0.5 b3:1", "1:1 1:1 R:2",
      "R:0.5 1':0.5 1':0.5 b7:0.5 5:0.5 b7:0.5 1':1", "5:1 5:1 R:2", "R:0.5 2':0.5 2':0.5 1':0.5 b7:0.5 1':0.5 5:1", "5:1 4:1 R:2"]
X1 = "らいげつからはね/となりのせきには/だれもすわらない/さとうがあまるよ"
LY = Lyrics(S)


def put(name, key, lines, text, o=4):
    bars = S.sc(name); mel = [swing(key.mel(x, oct=o)) for x in lines]
    for b, m in zip(bars, mel):
        if m.strip() != "R:4.0000": V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA, A1)
put("Bメロ1", K, VB, B1); put("Bメロ2", K, VB, B2)
put("サビ1", K, VC, C1); put("サビ2", K, VC, C2)
put("ストップタイム", K, VX, X1)
put("落ちサビ", K, VC, C3)
put("最後のサビ", KL, VCL + VCL + TAG, CL)
if VOCAL: put("Aメロ2", K, VA, A2)
else:                                         # 歌なしの版: 2番の Aメロはギターが歌う
    for b, l in zip(S.sc("Aメロ2"), VA):
        if l != "R:4": LG.bar(b, swing(K.mel(l, oct=4)))

# ================= ギターの答え・ソロ（E のブルースの音階） =================
LICK = {
    "a": ["G4:0.5 G#4:0.5 E4:0.5 D4:0.5 E4:2", "R:0.5 B3:0.5 D4:0.5 E4:0.5 G4:0.5 E4:1.5"],
    "b": ["B4:0.5 A4:0.5 G#4:1 E4:2", "R:0.5 F4:0.5 G#4:0.5 B4:0.5 C#5:2"],
    "c": ["E5:0.5 D5:0.5 B4:0.5 A4:0.5 G4:0.5 G#4:0.5 E4:1", "R:1 D#4:0.5 F#4:0.5 A4:0.5 B4:1.5"],
    "d": ["E5:1.5 D5:0.5 B4:1 A4:1", "G4:0.5 A4:0.5 B4:1 B4:2"],
    "e": ["A4:0.5 C5:0.5 A4:0.5 G4:0.5 E4:1 G4:1", "A4:3 R:1"],
    "f": ["R:0.5 E5:0.5 G5:0.5 E5:0.5 D5:0.5 B4:0.5 D5:1", "E5:4"],
}


def lick(b, name):
    for j, s in enumerate(LICK[name]): LG.bar(b + j, swing(s))


for name in ("Aメロ1", "Aメロ2"):
    bs = S.sc(name)
    lick(bs[2], "a"); lick(bs[6], "b"); lick(bs[10], "c")
bs = S.sc("イントロ"); lick(bs[4], "a"); lick(bs[8], "c")
bs = S.sc("間奏"); lick(bs[0], "e"); lick(bs[2], "a"); lick(bs[4], "d"); lick(bs[6], "c")
bs = S.sc("ギターソロ")
for j, nmx in zip(range(0, 12, 2), ["f", "a", "e", "d", "b", "c"]): lick(bs[j], nmx)
lick(S.sc("終わり")[4], "d")

# ================= 伴奏 =================
QUAL = lambda ch: "m" if re.match(r"^[A-G][#b]?m(?!aj)", ch) else ("maj" if "maj" in ch or ch in ("E", "F", "A", "B") else "dom")


def boogie(b, ch):
    r = low(ch, "E2"); q = QUAL(ch)
    up = [7, 7, 9, 9, 10, 10, 9, 9] if q == "dom" else ([7, 7, 9, 9, 11, 11, 9, 9] if q == "maj" else [7, 7, 10, 10, 12, 12, 10, 10])
    GR.bar(b, swing(" ".join(f"{nm(r)}:0.5" for _ in range(8))))
    GU.bar(b, swing(" ".join(f"{nm(r + u)}:0.5" for u in up)))


def walk(b, ch, i):
    r = low(ch, "E1"); q = QUAL(ch)
    w = [0, 4, 7, 9] if q != "m" else [0, 3, 7, 10]
    if i % 2 == 1: w = [10 if q == "dom" else (11 if q == "maj" else 12), 9 if q != "m" else 10, 7, w[1]]
    BASS.bar(b, " ".join(f"{nm(r + x)}:1" for x in w))


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    v = voice(ch, 64, 3); ev = voice(ch, 62, 3)
    if n == "イントロ" and i < 4:                       # ギター1本のブギで始まる
        boogie(b, ch)
        if i >= 2: BASS.bar(b, f"{nm(r)}:1 R:3" if i == 2 else " ".join(f"{nm(r)}:1" for _ in range(4)))
        continue
    if n == "ストップタイム":                            # 小節の頭だけ、全員で「ジャン」
        GR.bar(b, f"{nm(low(ch, 'E2'))}:0.75 R:3.25"); GU.bar(b, f"{nm(low(ch, 'E2') + 7)}:0.75 R:3.25")
        BASS.bar(b, f"{nm(r)}:0.75 R:3.25")
        for j in range(3): PN[j].bar(b, f"{nm(v[j])}:0.75 R:3.25")
        continue
    if n == "終わり" and i >= 6:
        if i == 6:
            GR.bar(b, f"{nm(low(ch, 'E2'))}:8"); GU.bar(b, f"{nm(low(ch, 'E2') + 7)}:8"); BASS.bar(b, f"{nm(r)}:8")
            for j in range(3): PN[j].bar(b, f"{nm(v[j])}:8"); EP[j].bar(b, f"{nm(ev[j])}:8")
            LG.bar(b, swing("R:1 F5:0.5 Ab5:0.5 A5:0.5 C6:0.5 F5:1"))
        continue
    if n in ("Bメロ1", "Bメロ2"):                       # 跳ねるのを少し休んで、のばす
        GR.bar(b, f"{nm(low(ch, 'E2'))}:2 {nm(low(ch, 'E2'))}:2"); GU.bar(b, f"{nm(low(ch, 'E2') + 7)}:2 {nm(low(ch, 'E2') + 7)}:2")
        BASS.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2")
        for j in range(3): EP[j].bar(b, f"{nm(ev[j])}:4")
        continue
    if n == "落ちサビ":
        for j in range(3): EP[j].bar(b, f"{nm(ev[j])}:4"); PN[j].bar(b, swing(f"R:1 {nm(v[j])}:0.5 R:1.5 {nm(v[j])}:0.5 R:0.5"))
        BASS.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2" if i >= 4 else f"{nm(r)}:4")
        continue
    boogie(b, ch); walk(b, ch, i)
    chorus = n.startswith(("サビ", "最後"))
    if chorus:
        for j in range(3):
            EP[j].bar(b, f"{nm(ev[j])}:4")
            PN[j].bar(b, f"{nm(v[j])}:1 R:0.6667 {nm(v[j])}:0.3333 {nm(v[j])}:1 R:0.6667 {nm(v[j])}:0.3333")
        PNL.bar(b, swing(f"{nm(r + 24)}:0.5 {nm(r + 31)}:0.5 {nm(r + 33)}:0.5 {nm(r + 31)}:0.5 " * 2))
    else:
        for j in range(3): PN[j].bar(b, f"R:1 {nm(v[j])}:0.6667 R:0.3333 R:1 {nm(v[j])}:0.6667 R:0.3333")
    if n in ("サビ2", "最後のサビ") or n == "ギターソロ":
        sv = voice(ch, 67, 3)
        for j in range(3): STR[j].bar(b, f"{nm(sv[j])}:4")
cym_swell(CYM, S.sc("最後のサビ")[0], 2, "E4")

# ================= ドラム（シャッフル: ハイハットは3連の「チッ・キ」） =================
SH = "x:0.6667 o:0.3333 x:0.6667 o:0.3333 x:0.6667 o:0.3333 x:0.6667 o:0.3333"
SHX = "X:0.6667 o:0.3333 x:0.6667 o:0.3333 X:0.6667 o:0.3333 x:0.6667 o:0.3333"
SHF = "x:0.6667 o:0.3333 x:0.6667 o:0.3333 R:2"            # フィルの小節（後ろ半分はハットを休む）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "イントロ" and i < 4:
        if i == 3: D.set(b, "." * 16, "........X.X.XXXX", "." * 16)
        continue
    if n == "ストップタイム":
        D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 2)
        if last: D.set(b, "X" + "." * 15, "X.......X.X.XXXX", "." * 16)
        continue
    if n == "終わり" and i >= 6:
        if i == 6: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 8)
        else: D.set(b, "." * 16, "." * 16, "." * 16)
        continue
    if n == "落ちサビ":
        D.set(b, "X......." + ("X......." if i >= 4 else "........"), "." * 16, "." * 16)
        HATS.bar(b, "o:1 o:1 o:1 o:1" if i < 4 else SH.replace("x:", "o:"))
        if last: D.set(b, "X.......X.......", "........X.X.XXXX", "." * 16); HATS.bar(b, "o:1 o:1 R:2")
        continue
    chorus = n.startswith(("サビ", "最後")) or n == "ギターソロ"
    kick = "X...X...X...X..." if (n in ("最後のサビ", "ギターソロ") or (n == "終わり")) else "X.......X......."
    if n in ("Bメロ1", "Bメロ2"): kick = "X.......X......."
    fill = last or (chorus and i % 4 == 3)
    D.set(b, kick, "....X.......X...", "." * 16)
    HATS.bar(b, SHF if fill else (SHX if chorus else SH))
    if fill:
        put_fill(D, b, "snare16" if last else "small")
    if (chorus and i % 4 == 0) or (i == 0 and n not in ("Bメロ1", "Bメロ2")): crash(D, b, "C2", 4)

SIL.add(S.sc("落ちサビ")[-1], 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の20。ブルースロック（8分のシャッフル）。E・120、最後のサビは F。"
          "となりの席のセンパイの「まあいいか」を、いつのまにか受けつぐ話。12小節のブルースで「歌う → ギターが答える」かけ合い、"
          "3連で跳ねるブギのギターと歩くベース、サチュレーターで温かく歪ませたギターソロ、小節の頭だけ鳴らすストップタイム。自作")
# v2: v1 は BGM 7.48・歌 7.24。場面ごとに比べると、歌の入った所（Bメロ・サビ・最後のサビ）だけが歌なしより 0.9〜1.4 下がっていた。
#   サビは E5〜F#5（最後のサビは F5）の高い所に歌が長くいる → 曲全体を 2半音下げて（D・最後のサビは E♭）、歌の高さを楽にする。最後のサビの持ち上げも少し弱く
finish(S, LY, V, -2, fx=[{"type": "sat", "scenes": ["ギターソロ"], "drive": 0.4}, {"type": "sat", "scenes": ["最後のサビ"], "drive": 0.2}],
       level={"verse": -0.2}, special={"ストップタイム": -0.3, "落ちサビ": -0.5, "最後のサビ": 0.35})
