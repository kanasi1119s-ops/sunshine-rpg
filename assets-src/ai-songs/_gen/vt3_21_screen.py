# vt3 21「画面越しのハーモニー」Harmony Through the Screen（仮）— ディープハウス。120・4/4。F の短調（転調なし）。
# 第3弾（0時〜24時の街）の 20時。表は docs/sound/vt3-plan.md。
# 物語: 夜8時。はなれた町に住む友だちと、画面ごしに一緒に歌う。「いち、にの、さん」で歌いだすと、声が少しずれて届く。
#   ときどき画面がかたまっても、笑顔のまま。とちゅうで通信がとぎれる2小節。つながりなおすと、こんどは声がぴったりそろう。
# 場面と強さ: 呼び出し音 → イントロ（パッドの和音と声のチョップ → 4つ打ち）→ Aメロ1（中）→ Bメロ1 → サビ1（中強）
#   → 間奏（声のチョップの節）→ Aメロ2 → Bメロ2 → サビ2 → とぎれる（2小節・パッドだけ）→ つながりなおす（ブレイク）
#   → 最後のサビ（声がそろう・下に重なる声・いちばん厚い）→ またね（パッドとチョップ）
# 旋律の性格: 長く浮かぶ旋律。サビは6音の句を4つ、同じ形でくり返す（C4〜D♭5）。
# この曲だけの音: ディープハウスの9度・11度の和音（裏で刻むエレピ）、サブベース、声のチョップ。
#   合いことばの節（3・5・6・5・2＝A♭・C・D♭・C・G）は、声のチョップが間奏とイントロで鳴らす。
from vt25_lib import *

S = Song("21", "screen", "画面越しのハーモニー（仮）", "Harmony Through the Screen", 120, 4, "F", "minor", "ディープハウス（ボカロ）")
S.kit = "electro"
S.flags = S.flags + " --piano salamander --space room --space-wet 0.15"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.5
K = Key("F", "minor")          # oct 3 で 1 = F3（歌うのは 5＝C4 から上）

A_CH = ["Fm9", "Dbmaj9", "Bbm9", "Eb9"]
B_CH = ["Dbmaj7", "Eb9", "Cm7", "Fm9", "Bbm9", "Eb9", "Abmaj7", "C7sus4"]
C_CH = ["Dbmaj9", "Eb9", "Cm7", "Fm9", "Bbm9", "Eb9", "Abmaj9", "C7sus4"]

S.scene("呼び出し音", 2, "intro", ["Fm9", "Fm9"])
S.scene("イントロ", 16, "intro", A_CH)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 8, "break", A_CH)
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("とぎれる", 2, "break", ["Fm9", "Fm9"])
S.scene("つながりなおす", 8, "bridge", ["Dbmaj9", "Eb9", "Cm7", "Fm9", "Bbm9", "Eb9", "Abmaj9", "C7sus4"])
S.scene("最後のサビ", 16, "chorus", C_CH)
S.scene("またね", 6, "outro", ["Fm9", "Dbmaj9", "Bbm9", "Eb9", "Fm9", "Fm9"])

V = Voice(S, vol=0.21, delay=0.75, bright=0.2, patch="kfbSineLead", low=False)   # v2: 歌をなぞるシンセは、高さの揺れない音に
HARM = S.track("重なる声（下の3度）", "pad", patch="choir", volume=0.05, pan=-0.2, reverb=0.4)
EP = [S.track(f"エレピの和音{i + 1}", "keys", patch="kfbGlassEp", volume=0.055, pan=-0.3 + 0.2 * i, reverb=0.3, sustain=0.5) for i in range(4)]
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("kfbSparklePad", vol=0.03, pan=-0.4 + 0.4 * i, duck=0.45, sustain=1.6)) for i in range(3)]
CHOP = S.track("声のチョップ", "pad", patch="vocalChop", volume=0.08, pan=0.3, reverb=0.3)
BASS = S.track("ディープなベース", "bass", **synth_bass_spec("kfbFmBass", vol=0.13, duck=0.4))
SUB = S.track("サブベース", "sub808", volume=0.11, pan=0, sustain=0.8, fx=[{"type": "filter", "kind": "highpass", "freq": 28, "q": 0.7}])
BEEP = S.track("呼び出し音", "glockenspiel", volume=0.05, pan=0.2, reverb=0.35)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.05, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.05, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 5:0.5 1':1 7:0.5 1':0.5 3':1", "2':2 1':1 R:1", "R:0.5 5:0.5 6:1 5:0.5 6:0.5 1':1", "7:2 5:1 R:1",
      "R:0.5 5:0.5 1':1 7:0.5 1':0.5 4':1", "3':2 2':1 R:1", "R:0.5 2':0.5 3':1 2':0.5 1':0.5 7:1", "1':3 R:1"]
A1 = ("はなれたまちで/きみがてをふる/がめんのむこう/おなじよぞら/"
      "いやほんさして/いちにのさんで/すこしずれるの/とどくじかん")
A2 = "ちいさなまどに/ならんだかおが/わらいころげて/ゆれているよ"
VB = ["R:0.5 3':0.5 3':0.5 2':0.5 3':0.5 4':0.5 5':1", "4':2 3':1 R:1", "R:0.5 2':0.5 2':0.5 1':0.5 2':0.5 3':0.5 4':1", "3':2 2':1 R:1",
      "R:0.5 1':0.5 2':0.5 3':0.5 4':0.5 4':0.5 5':1", "6':2 5':1 R:1", "R:0.5 5':0.5 4':0.5 3':0.5 2':0.5 1':0.5 2':1", "1':3 R:1"]
B1 = "とおくのきみへと/ちいさなこえでも/ひかりのはやさで/とどけにいくよ"
B2 = "ときどきかたまる/えがおのままでね/それでもきこえる/きみのいきづき"
VC = ["R:0.5 3':0.5 5':1 4':0.5 3':0.5 2':1", "3':2 R:2", "R:0.5 2':0.5 4':1 3':0.5 2':0.5 1':1", "2':2 R:2",
      "R:0.5 3':0.5 5':1 4':0.5 3':0.5 6':1", "5':2 R:2", "R:0.5 4':0.5 3':0.5 2':0.5 1':1 7:1", "1':2 R:2"]
HOOK = "かさなるこえ"
C1 = f"{HOOK}/がめんごしに/とおくはなれ/おなじうたを/{HOOK}/よるをこえて/きみのとなり/うたうからね"
C2 = f"{HOOK}/とぎれぬよう/ゆびでなぞる/きみのえがお/{HOOK}/まちのあかり/ふたつぶんの/よるのうただ"
C3 = f"{HOOK}/こえがそろう/ほしのむこう/とどいたよね/{HOOK}/またあしたね/おやすみまで/となりにいる"
LY = Lyrics(S)


def put(name, lines, text, o=3):
    bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


def down3(line):
    """音階で3度下（重なる声用）"""
    out = []
    for t in line.split():
        n, L = t.split(":")
        if n == "R": out.append(t); continue
        d = int(n.rstrip("'")); p = n.count("'")
        idx = (d - 1) + 7 * p - 2
        out.append(f"{idx % 7 + 1}{chr(39) * (idx // 7)}:{L}")
    return " ".join(out)


put("Aメロ1", VA + VA, A1)
put("Bメロ1", VB, B1)
put("サビ1", VC + VC, C1)
put("Aメロ2", VA, A2)
put("Bメロ2", VB, B2)
put("サビ2", VC + VC, C2)
put("最後のサビ", VC + VC, C3)
for b, x in zip(S.sc("最後のサビ"), VC + VC): HARM.bar(b, K.mel(down3(x), oct=3))
for b, x in zip(S.sc("サビ2")[8:], VC): HARM.bar(b, K.mel(down3(x), oct=3))

# ================= 和音・パッド・チョップ =================
def ep(b, ch, full=True):
    """裏で刻むディープハウスの和音"""
    v = voice(ch, 63, 4)
    pat = "R:0.5 {0}:0.5 R:0.75 {0}:0.25 R:0.5 {0}:0.5 R:0.5 {0}:0.5" if full else "R:0.5 {0}:0.75 R:2.75"
    for j in range(4): EP[j].bar(b, pat.format(nm(v[j])))


def pad(b, ch, c=60):
    v = voice(ch, c, 3)
    for j in range(3): PAD[j].bar(b, f"{nm(v[j])}:4")


MOTIF = ["R:1 Ab4:0.5 C5:0.5 Db5:1 C5:0.5 G4:0.5", "F4:3 R:1"]     # 合いことばの節（3・5・6・5・2）
CHOPS = ["R:0.5 C5:0.25 R:0.25 Eb5:0.5 R:1 C5:0.25 Ab4:0.25 R:1", "R:1.5 F5:0.25 R:0.25 Eb5:0.5 C5:0.5 R:1",
         "R:0.5 Db5:0.25 R:0.25 F5:0.5 R:1 Eb5:0.25 Db5:0.25 R:1", "R:1.5 C5:0.5 Bb4:0.5 G4:1 R:0.5"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "呼び出し音":
        pad(b, ch)
    elif n == "イントロ":
        pad(b, ch)
        if i >= 4: ep(b, ch, full=i >= 8)
        CHOP.bar(b, MOTIF[i % 2] if i < 8 else CHOPS[i % 4])
    elif n in ("Aメロ1", "Aメロ2"):
        ep(b, ch); pad(b, ch, 58) if i >= 8 or n == "Aメロ2" else None
    elif n in ("Bメロ1", "Bメロ2"):
        ep(b, ch, full=i % 2 == 0); pad(b, ch, 62)
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        ep(b, ch); pad(b, ch, 64)
        if i % 4 == 3: CHOP.bar(b, CHOPS[(b // 4) % 4])
    elif n == "間奏":
        ep(b, ch); pad(b, ch, 60)
        CHOP.bar(b, MOTIF[i % 2] if i < 4 else CHOPS[i % 4])
    elif n == "とぎれる":
        pad(b, ch, 60)
        CHOP.bar(b, "C5:0.125 R:0.375 C5:0.125 R:1.375 Ab4:0.125 R:1.875" if i == 0 else "R:4")
    elif n == "つながりなおす":
        pad(b, ch, 62)
        if i >= 2: ep(b, ch, full=i >= 4)
        CHOP.bar(b, MOTIF[i % 2])
    elif n == "またね":
        pad(b, ch, 60)
        if i < 4: ep(b, ch, full=i < 2); CHOP.bar(b, MOTIF[i % 2])

BEEP.bar(S.sc("呼び出し音")[0], "C6:0.5 R:0.5 C6:0.5 R:2.5"); BEEP.bar(S.sc("呼び出し音")[1], "Eb6:0.5 R:0.5 C6:1 R:2")
BEEP.bar(S.sc("つながりなおす")[0], "C6:0.5 R:0.5 Eb6:1 R:2")

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n in ("呼び出し音", "とぎれる"):
        if n == "とぎれる" and i == 0: SUB.bar(b, f"{nm(r)}:2 R:2")
        continue
    if n == "イントロ" and i < 8:
        if i >= 4: SUB.bar(b, f"{nm(r)}:4")
        continue
    if n == "つながりなおす" and i < 4: SUB.bar(b, f"{nm(r)}:4"); continue
    if n == "またね" and i >= 4: SUB.bar(b, f"{nm(r)}:4" if i == 4 else "R:4"); continue
    BASS.bar(b, bass_line(S, b, "house" if i % 4 != 3 else "push", lo="E1"))
    SUB.bar(b, f"{nm(r)}:1.5 R:0.5 {nm(r)}:1.5 R:0.5")

riser(FX, S.sc("サビ1")[0], 4, "C4"); riser(FX, S.sc("最後のサビ")[0], 4, "C4")
cym_swell(CYM, S.sc("サビ2")[0], 2, "C4")

# ================= ドラム（4つ打ち）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("呼び出し音", "とぎれる"): continue
    if n == "イントロ":
        if i < 4: D.set(b, "................", "................", "..x...x...x...x."); continue
        if i < 8: D.set(b, "X...X...X...X...", "................", "..x...x...x...x."); continue
    if n == "つながりなおす":
        if i < 4: D.set(b, "................", "................", "..x...x...x...x." if i >= 2 else "................"); continue
        D.set(b, "X...X...X...X...", "....X.......X...", "..x...x...x...x.")
        if i == 7: put_fill(D, b, "build")
        continue
    if n == "またね":
        if i < 4: vgroove(D, b, "four", ghosts=0.15, seed=b)
        if i == 0: crash(D, b, "C2", 5)
        continue
    vgroove(D, b, "four", ghosts=0.15 if n in ("Aメロ1", "Aメロ2") else 0.2, seed=b)
    if n in ("サビ1", "サビ2", "最後のサビ") and i % 8 == 0: crash(D, b, "C2", 6 if n == "最後のサビ" and i == 0 else 4)
    if n == "イントロ" and i == 8: crash(D, b, "C2", 4)
    if i % 8 == 7 and not last: put_fill(D, b, "small")
    if last and n in ("Bメロ1", "Bメロ2", "イントロ", "間奏"): put_fill(D, b, "lift")

SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の21（20時）。ディープハウス。F の短調・120。はなれた町の友だちと、画面ごしに一緒に歌う。"
          "裏で刻む9度のエレピ・パッド・サブベース・声のチョップ。通信がとぎれる2小節のあと、最後のサビで声がそろう（下に重なる声）。"
          "合いことばの節は声のチョップ。呼び出し音で始まる。自作")
finish(S, LY, V, 0,
       level={"verse": -0.25}, special={"とぎれる": -0.4, "最後のサビ": 0.35, "またね": -0.2})

# ================= v2（2026-11-12 作り直し。docs/sound/vt3-remake-plan.md）=================
# この曲（午後8時・画面越しの通話でいっしょに歌う・ディープハウス）で直すこと:
#   電子の音: エレピをガラスのエレピ、パッドをきらきらのパッド、ベースをはじく FM のベースに。「とぎれる」所に、通信がとぎれるグリッチの音とレコードのパチパチ（この曲だけの音）。
#            サビの前に上がる音、サビの頭にきらきら
#   ボーカルチョップ: シンセの「声のチョップ」が鳴る小節に、歌入りの版ではテトの声の短い「や・は」を重ねる（画面の向こうの声）
#   歌: Aメロはウィスパー（夜、画面に向かって小声）、Bメロとサビはクリア、つながりなおす所と「またね」はウィスパー。ハモリは サビ2 の頭から（2人で歌う）と最後のサビ
from vt3x_lib import *
path = sys.argv[1]
fx = {}
tg = S.sc("とぎれる"); fx[tg[0]] = "D#6:2 R:2"
if len(tg) > 2: fx[tg[2]] = "R:1 D#6:1 R:2"
for name in ("サビ1", "サビ2", "最後のサビ"):
    b0 = S.sc(name)[0]; fx[b0] = "D4:2 R:2"; fx[b0 - 1] = "R:2 F#4:2"
add_parts(path, [pad_part(S, "カワイイ効果音", "kawaiiFx", fx, 0.06, pan=0.1, reverb=0.15, modulate=False, instrument="guitar"),
                 pad_part(S, "レコードのパチパチ", "kawaiiFx", {tg[0]: "A#5:12 R:4"}, 0.035, reverb=0.05, modulate=False, instrument="guitar")])
set_parts(path, "ディープなベース", sustain=1.1)
if VOCAL:
    cb = [b for b in active_bars(path, "声のチョップ") if S.scene_of(b)[3] not in ("verse", "pre", "chorus")]; ch_ = {}     # 歌っていない場面だけ（歌とぶつけない）
    for q, b in enumerate(cb):
        t = tones(S.chords[b].split("|")[0].split("/")[0], "C4", "A4")
        if len(t) >= 3: ch_[b] = (f"{nm(t[1])}:0.5:や R:0.5 {nm(t[2])}:0.5:は R:0.5 {nm(t[1])}:0.5:や R:1.5" if q % 2 == 0 else f"R:1 {nm(t[2])}:0.5:は R:0.25 {nm(t[2])}:0.25:は {nm(t[0])}:1:や R:1")
    set_parts(path, "声のチョップ", volume=0.035)
    remark(path, S, std_mark(("chorus",), jump=5))
    vocal_polish(path, S, {"verse": 6, "pre": 12, "chorus": 18, "最後のサビ": 22, "bridge": 6, "break": 0, "outro": 0}, scoop=0.25, slash=0.6, vib_min_beats=1.5, vib_start=0.5, auto=0.6, breaths=0.6)
    harmony(path, S, [("サビ2", 0, None, K), ("最後のサビ", 0, None, K)], vol=0.38)
    if ch_: chops(path, S, ch_, vol=0.3, pan=0.3)
    voice_by_scene(path, S, {"verse": "whisper", "pre": "clear", "chorus": "clear", "bridge": "whisper", "outro": "whisper"}, default="clear")
