# vt3 23「くらげの夜間飛行」Jellyfish Night Flight（仮）— ポストロック。104・4/4。D長調（転調なし）。
# 第3弾（0時〜24時の街）の 22時。表は docs/sound/vt3-plan.md。
# 物語: 閉館後の水族館。長ぐつをぬいだ飼育員が、くらげの水そうの前でひとやすみする。青い光のなかで、くらげがゆらゆら浮かぶ。
#   一日のつかれが水の音にとけていく。くらげがほのかに光りはじめて、だんだん水そういっぱいに光る。夜の海を飛んでいくみたいに。
# 場面と強さ: 泡（水の泡の音）→ ギターだけ（クリーンギター2本・弱）→ Aメロ1（ベースが入る）→ Bメロ1（タムが入る）→ サビ1（中）
#   → 間奏（グロッケンの節）→ Aメロ2 → Bメロ2 → サビ2（中強）→ 光りはじめる（トレモロとタム・ゆっくり大きくなる）
#   → クライマックス（くらげが光る・いちばん強い）→ グロッケン（最後の1音）
# 旋律の性格: 少ない言葉、長い音（A3〜F#5）。句は4〜5音で、最後の音を長く伸ばす。
# この曲だけの音: コーラスをかけないクリーンギター2本の8分のアルペジオ、グロッケン、ストリングス。
#   いちども音量を落とさず、ゆっくり大きくなっていく。合いことばの節（3・5・6・5・2＝F#・A・B・A・E）は、グロッケン。
from vt25_lib import *

S = Song("23", "jellyfish", "くらげの夜間飛行（仮）", "Jellyfish Night Flight", 104, 4, "D", "major", "ポストロック（ボカロ）")
S.kit = "naked-x"
S.flags = "--bass bnb-loud " + S.flags + " --space hall --space-wet 0.2"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.45
K = Key("D", "major")          # oct 3 で 1 = D3（Aメロ・Bメロ）、oct 4 で 1 = D4（サビ）

A_CH = ["Dadd9", "Bm7", "Gmaj7", "Aadd9"]
B_CH = ["Gmaj7", "F#m7", "Em7", "Bm7", "Gmaj7", "F#m7", "Em7", "Asus4"]
C_CH = ["Gmaj7", "Aadd9", "F#m7", "Bm7", "Gmaj7", "Aadd9", "Dadd9", "Dadd9"]

S.scene("泡", 2, "intro", ["Dadd9", "Dadd9"])
S.scene("ギターだけ", 8, "intro", A_CH)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 8, "break", A_CH)
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("光りはじめる", 12, "bridge", ["Gmaj7", "Aadd9", "Bm7", "Bm7", "Gmaj7", "Aadd9", "Bm7", "Bm7", "Em7", "F#m7", "Gmaj7", "Asus4"])
S.scene("クライマックス", 16, "chorus", C_CH)
S.scene("グロッケン", 4, "outro", ["Gmaj7", "Aadd9", "Dadd9", "Dadd9"])

V = Voice(S, vol=0.2, delay=0.75, bright=-0.1, patch="kfbSineLead", low=False)   # v2: 歌をなぞるシンセは、高さの揺れない音に
GA = S.track("クリーンギター（アルペジオ）", "guitar", amp="crystal", volume=0.08, pan=-0.35, reverb=0.35, chorus=0, sustain=0.9)
GB = S.track("クリーンギター（うしろ）", "guitar", amp="jpopClean", volume=0.065, pan=0.4, reverb=0.4, chorus=0, sustain=0.9)
GD = [S.track(f"歪みのギター{i + 1}", "distGuitar", **rock_gtr_spec(0.035, 0.6 if i % 2 else -0.6, drive=0.4)) for i in range(3)]
GL = S.track("グロッケン", "glockenspiel", volume=0.07, pan=0.15, reverb=0.5)
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.05, pan=-0.4 + 0.4 * i, reverb=0.5, sustain=1.6) for i in range(3)]
BASS = S.track("ベース", "bass", **rock_bass_spec(0.22))
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:1 5:1 1':1 2':1", "3':3 R:1", "R:1 3':1 2':1 1':1", "6:3 R:1",
      "R:1 5:1 1':1 2':1", "3':2 5':1 R:1", "R:1 4':1 3':1 2':1", "1':3 R:1"]
A1 = "しずかな/すいそう/ゆらゆらと/うかぶよ/ながぐつ/ぬいだら/ひとやすみ/ほおづえ"
A2 = "ひかりが/ちいさく/またたいて/ゆれてる"
VB = ["R:1 6:1 5:1 6:1", "1':2 2':1 R:1", "R:1 3':1 2':1 1':1", "2':3 R:1",
      "R:1 6:1 1':1 2':1", "3':2 4':1 R:1", "R:1 5':1 4':1 3':1", "2':3 R:1"]
B1 = "いちにちを/おえたら/ほのかにね/ひかるよ"
B2 = "みずのおと/とけてく/きみのいろ/みせてよ"
VC = ["R:1 1':1 7:1 6:1", "5:3 R:1", "R:1 6:1 5:1 3:1", "5:3 R:1",
      "R:1 1':1 2':1 3':1", "2':2 1':1 R:1", "R:1 6:1 1':1 7:1", "1':3 R:1"]
HOOK = "ひかれよ/くらげよ"
C1 = f"{HOOK}/よるのうみ/とんでけ/{HOOK}/あおいほし/みたいに"
C2 = f"{HOOK}/つかれたひ/とかして/{HOOK}/またあした/あおうね"
C3 = f"{HOOK}/ゆめのなか/とんでく/{HOOK}/おやすみと/てをふる"
LY = Lyrics(S)


def put(name, lines, text, o):
    bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", VA + VA, A1, 3)
put("Bメロ1", VB, B1, 3)
put("サビ1", VC + VC, C1, 4)
put("Aメロ2", VA, A2, 3)
put("Bメロ2", VB, B2, 3)
put("サビ2", VC + VC, C2, 4)
put("クライマックス", VC + VC, C3, 4)

# ================= ギター・ストリングス・グロッケン =================
def arp(b, ch, trem=False):
    """コーラスなしのクリーンギター。中音域の8分のアルペジオ（2本目は少しずらして上の音）"""
    t = tones(ch, "D3", "D5")
    cyc = [t[0], t[2 % len(t)], t[1], t[3 % len(t)], t[2 % len(t)], t[1], t[3 % len(t)], t[2 % len(t)]]
    GA.bar(b, " ".join(f"{nm(x)}:0.5" for x in cyc))
    u = tones(ch, "A3", "A5")
    if trem:
        GB.bar(b, " ".join(f"{nm(u[-1] if q < 8 else u[-2])}:0.25" for q in range(16)))
    else:
        GB.bar(b, f"R:0.5 {nm(u[-1])}:1.5 {nm(u[-2])}:1 {nm(u[-3])}:1")


def strings(b, ch, c=62):
    v = voice(ch, c, 3)
    for j in range(3): STR[j].bar(b, f"{nm(v[j])}:4")


def dist(b, ch, pat="x:0.5 x:0.5 x:0.5 x:0.5 x:0.5 x:0.5 x:0.5 x:0.5"):
    pw = power(ch, "E2")
    for j in range(3): GD[j].bar(b, " ".join(t.replace("x", nm(pw[j])) for t in pat.split()))


MOTIF = ["R:1 F#5:0.5 A5:0.5 B5:1 A5:0.5 E5:0.5", "D5:3 R:1"]     # 合いことばの節（3・5・6・5・2）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "泡":
        GL.bar(b, ["R:0.5 A6:0.25 R:0.75 F#6:0.25 R:1.25 D7:0.25 R:0.75", "R:1 B6:0.25 R:0.5 A6:0.25 R:2"][i])
    elif n == "ギターだけ":
        arp(b, ch)
    elif n in ("Aメロ1", "Aメロ2"):
        arp(b, ch)
        if n == "Aメロ2" or i >= 8: strings(b, ch, 60)
        if i % 4 == 3: GL.bar(b, "R:3 F#5:0.5 E5:0.5")
    elif n in ("Bメロ1", "Bメロ2"):
        arp(b, ch); strings(b, ch, 62)
    elif n in ("サビ1", "サビ2"):
        arp(b, ch); strings(b, ch, 64)
        if n == "サビ2" or i >= 8: dist(b, ch, "x:2 x:2")
        if i % 4 == 3: GL.bar(b, MOTIF[0])
    elif n == "間奏":
        arp(b, ch); strings(b, ch, 60)
        GL.bar(b, MOTIF[i % 2] if i < 4 else ["R:1 A5:1 B5:1 D6:1", "C#6:3 R:1", "R:1 B5:1 A5:1 F#5:1", "E5:3 R:1"][i - 4])
    elif n == "光りはじめる":
        arp(b, ch, trem=i >= 4); strings(b, ch, 62 + (i // 4) * 2)
        if i >= 8: dist(b, ch)
        if i % 2 == 1: GL.bar(b, MOTIF[0])
    elif n == "クライマックス":
        arp(b, ch, trem=True); strings(b, ch, 67); dist(b, ch)
        GL.bar(b, MOTIF[i % 2] if i % 4 < 2 else "R:4")
    elif n == "グロッケン":
        if i < 2: arp(b, ch); strings(b, ch, 64)
        elif i == 2: strings(b, ch, 62); GA.bar(b, f"{nm(tones(ch, 'D3', 'D5')[0])}:4")
        else: GL.bar(b, "D6:4")

season(S, S.sc("泡")[0], "波", beats=8, vol=0.03, every=4)

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n in ("泡", "ギターだけ"): continue
    if n in ("Aメロ1", "Aメロ2", "間奏"): BASS.bar(b, f"{nm(r)}:3 {nm(r + 7)}:1" if n != "Aメロ1" or i >= 4 else f"{nm(r)}:4"); continue
    if n in ("Bメロ1", "Bメロ2"): BASS.bar(b, f"{nm(r)}:2 {nm(r)}:1 {nm(r + 7)}:1"); continue
    if n == "グロッケン":
        if i < 3: BASS.bar(b, f"{nm(r)}:4")
        continue
    if n == "光りはじめる" and i < 4: BASS.bar(b, f"{nm(r)}:2 {nm(r)}:2"); continue
    BASS.bar(b, bass_line(S, b, "root8", lo="E1"))

cym_swell(CYM, S.sc("サビ1")[0], 2, "C4"); cym_swell(CYM, S.sc("光りはじめる")[0], 4, "C4"); cym_swell(CYM, S.sc("クライマックス")[0], 4, "C4")

# ================= ドラム（ゆっくり増える）=================
RIDE8 = "D2:0.5 D2:0.5 D2:0.5 D2:0.5 D2:0.5 D2:0.5 D2:0.5 D2:0.5"
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("泡", "ギターだけ"): continue
    if n == "Aメロ1":
        if i >= 8: D.set(b, "X.......X.......", "................", "................"); D.R.bar(b, "D2:1 D2:1 D2:1 D2:1")
        continue
    if n in ("Bメロ1", "Bメロ2"):
        D.set(b, "X.......X.......", "....x.......x...", "................"); D.R.bar(b, RIDE8)
        if last: put_fill(D, b, "build")
        continue
    if n == "Aメロ2" or n == "間奏":
        D.set(b, "X.......X.......", "....x.......x...", "................"); D.R.bar(b, "D2:1 D2:1 D2:1 D2:1")
        if last: put_fill(D, b, "small")
        continue
    if n == "光りはじめる":
        if i < 4: D.set(b, "X.......X.......", "................", "................"); D.R.bar(b, RIDE8)
        elif i < 8: D.set(b, "X.......X.......", "....X.......X...", "................"); D.R.bar(b, RIDE8)
        else: vgroove(D, b, "beat8", ghosts=0.15, seed=b)
        if last: put_fill(D, b, "snare16")
        continue
    if n == "グロッケン":
        if i == 0: D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 8)
        continue
    # サビ・クライマックス
    if n == "クライマックス":
        D.set(b, "X.......X.X.....", "....X.......X...", "................"); D.R.bar(b, RIDE8)
        if i % 4 == 0: crash(D, b, "C2", 6)
    else:
        D.set(b, "X.......X.X.....", "....X.......X...", "................"); D.R.bar(b, RIDE8)
        if i % 8 == 0: crash(D, b, "C2", 4)
    if i % 8 == 7 and not last: put_fill(D, b, "small")
    if last and n in ("サビ1", "サビ2"): put_fill(D, b, "snare16")

SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の23（22時）。ポストロック。D長調・104。閉館後の水族館で、飼育員がくらげの水そうの前でひとやすみ。"
          "コーラスなしのクリーンギター2本・グロッケン・ストリングス。ギターだけの前半から、くらげが光るクライマックスまでゆっくり大きくなる。"
          "合いことばの節はグロッケン。水の泡の音で始まり、グロッケンの1音で終わる。自作")
finish(S, LY, V, 0,
       level={"verse": -0.2}, special={"ギターだけ": -0.3, "クライマックス": 0.45, "光りはじめる": 0.15})

# ================= v2（2026-11-12 作り直し。docs/sound/vt3-remake-plan.md）=================
# この曲（午後10時・水族館のくらげ・ポストロック）で直すこと:
#   ギター: アルペジオと、うしろのクリーンギターを DI ギターに（音を伸ばして重ねる。左は明るく、右は丸く）。歪みのギターは、静かな所は8分のかき鳴らし、
#          クライマックスは16分を弾きつづける（ポストロックのトレモロ弾き）。コーラスなし
#   歌: Aメロ・Bメロはウィスパー（水の中のように）、サビとクライマックスはクリア。ハモリはクライマックス
from vt3x_lib import *
path = sys.argv[1]
to_di(path, S, "クリーンギター（アルペジオ）", "clean_arp", vol=0.075, seed=4)
to_di(path, S, "クリーンギター（うしろ）", "clean_arp", vol=0.06, seed=9, di="gretsch")
pd = restrum(path, S, "歪みのギター", 0.0, lambda n, i, end, b: "D.u.d.u.D-------" if end else ("DuDuDuDuDuDuDuDu" if n == "クライマックス" else ("D.u.d.u.D.u.d.u." if i % 2 == 0 else "D...d.u.D.u.d.u.")), seed=6, lag=0.016)
add_parts(path, pd, drop=lambda p: p.get("role", "").startswith("歪みのギター"))
final_gain(path, {"泡": 10, "ギターだけ": 7, "光りはじめる": 0.5, "クライマックス": 2.0})
if VOCAL:
    remark(path, S, std_mark(("chorus",), jump=5, minlen=1.5))
    vocal_polish(path, S, {"verse": 0, "pre": 8, "chorus": 18, "クライマックス": 24, "bridge": 0, "outro": 0}, scoop=0.2, slash=0.6, vib_min_beats=2.0, vib_start=0.55, auto=0.7, breaths=0.7)
    harmony(path, S, [("クライマックス", 0, None, K)], vol=0.36)
    voice_by_scene(path, S, {"verse": "whisper", "pre": "whisper", "chorus": "clear", "bridge": "whisper"}, default="whisper")
