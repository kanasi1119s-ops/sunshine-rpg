# vt3 14「工事中ステップ」Under-Construction Step（仮）— アフロビーツ。104・4/4。G短調（転調なし）。
# 第3弾（0時〜24時の街）の 13時。表は docs/sound/vt3-plan.md。
# 物語: 午後1時の工事現場。ヘルメットのひもをしめた新米の「わたし」。かなづちの「かんかん」、ドリルの「ずんずん」、
#   先輩の「おーい、こっちだ」── ばらばらの音が、だんだん一つのリズムにそろっていく。クレーンの上でだれかが歌う、どこかで聞いた5つの音。
#   空へ伸びる鉄骨の柱。きのうは無かった階段がひとつ。ここは、だれかが住む家になる。
# 場面と強さ: ヘルメット（打楽器だけが少しずつ増える・弱→中）→ イントロ（マリンバとギター）→ Aメロ1（ゆったり語る・中）→ Bメロ1（空へ）
#   → サビ1（強）→ サイレン（午後の合図・パッドとマリンバだけ・弱）→ Aメロ2 → Bメロ2 → サビ2 → 打楽器（どんどん増える）
#   → 最後のサビ（いちばん厚い）→ クレーン（止まる）
# 旋律の性格: ゆったり揺れる短い節のくり返し（D4〜F5）。サビは「こうじちゅうのすてっぷ」が4回もどってくる。
# この曲だけの音: 工事の音（ヘルメット・かなづち＝カホンとタム）がそのまま打楽器になり、アフロビーツの揺れるリズムを作る。
#   合いことばの節（3・5・6・5・2）は、サイレンのあとマリンバが弾く（B♭長調として D・F・G・F・C）。
from vt25_lib import *

S = Song("14", "construction", "工事中ステップ（仮）", "Under-Construction Step", 104, 4, "G", "minor", "アフロビーツ（ボカロ）")
S.kit = "electro"
S.flags = S.flags + " --space room --space-wet 0.14"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.45
K = Key("G", "minor")          # oct 4 で 1 = G4

LOOP = ["Gm9", "Cm9", "Ebmaj7", "D7sus4"]
C_CH = ["Ebmaj7", "F", "Gm9", "Gm9", "Ebmaj7", "F", "Dm7", "Gm9"]

S.scene("ヘルメット", 4, "intro", LOOP)
S.scene("イントロ", 8, "intro", LOOP)
S.scene("Aメロ1", 16, "verse", LOOP)
S.scene("Bメロ1", 8, "pre", ["Cm9", "Dm7", "Ebmaj7", "F", "Cm9", "Dm7", "Ebmaj7", "D7sus4"])
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("サイレン", 4, "break", ["Ebmaj7", "Bbmaj7", "Cm9", "D7sus4"])
S.scene("Aメロ2", 8, "verse", LOOP)
S.scene("Bメロ2", 8, "pre", ["Cm9", "Dm7", "Ebmaj7", "F", "Cm9", "Dm7", "Ebmaj7", "D7sus4"])
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("打楽器", 8, "solo", LOOP)
S.scene("最後のサビ", 16, "chorus", C_CH)
S.scene("クレーン", 4, "outro", ["Ebmaj7", "F", "Gm9", "Gm9"])

V = Voice(S, vol=0.2, delay=0.5, bright=0.0, patch="kfbSineLead", low=False)   # v2: 歌をなぞるシンセは、高さの揺れない音に
MAR = S.track("マリンバ", "strings", patch="marimba", volume=0.11, pan=-0.3, reverb=0.25)
GT = S.track("ギター（ハイライフの単音）", "guitar", amp="crystal", volume=0.07, pan=0.45, reverb=0.25, chorus=0, sustain=0.5)
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("kfbSparklePad", vol=0.02, pan=-0.5 + 0.5 * i, duck=0.35, sustain=1.5)) for i in range(3)]
BASS = S.track("ベース", "bass", **synth_bass_spec("kfbFmBass", vol=0.15, duck=0.25))
HELM = S.track("ヘルメットとかなづち（カホン）", "cajon", volume=0.09, pan=0.25, reverb=0.12)
CONGA = S.track("太鼓（コンガのかわり）", "inchTom", volume=0.08, pan=-0.35, reverb=0.15)
BELLS = S.track("カウベル", "pad", patch="seasonFx", volume=0.05, pan=0.4, reverb=0.1, modulate=False)
SIREN = S.track("サイレン", "pad", patch="fxRiser", volume=0.05, pan=0, reverb=0.4)
CRANE = S.track("クレーン（低い一撃）", "impactHit", volume=0.07, pan=0, reverb=0.35)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:1 5,:0.5 7,:0.5 1:0.75 7,:0.25 5,:1", "4,:1 5,:1 R:2", "R:1 5,:0.5 7,:0.5 1:0.75 3:0.25 2:1", "1:2 R:2",
      "R:1 3:0.5 3:0.5 4:0.75 3:0.25 2:1", "1:1 7,:1 R:2", "R:1 5,:0.5 7,:0.5 1:0.75 7,:0.25 5,:1", "5,:2 R:2"]
A1 = "いちじのげんば/てつのにおい/かなづちのおと/かんかんかん/どりるがうなって/ずんずんずん/ばらばらのおと/ひとつになる"
A2 = "くれーんのうえ/だれかうたう/どこかできいた/いつつのおと"
VB = ["R:0.5 3:0.5 3:0.5 4:0.5 5:1 4:1", "3:1 2:1 R:2", "R:0.5 4:0.5 4:0.5 5:0.5 6:1 5:1", "4:1 3:1 R:2",
      "R:0.5 5:0.5 5:0.5 6:0.5 7:1 6:1", "5:1 4:1 R:2", "R:0.5 4:0.5 5:0.5 6:0.5 7:0.5 6:0.5 5:0.5 4:0.5", "5:2 R:2"]
B1 = "そらへとのびる/てっこつのはしら/わたしたちのて/まちをつくってるよ"
B2 = "あせをぬぐったら/みあげたさきに/きのうはなかった/かいだんがひとつ"
VC = ["R:0.5 5:0.5 5:0.5 4:0.5 5:1 7:1", "6:1 5:1 4:0.5 3:0.5 R:1", "R:0.5 3:0.5 3:0.5 2:0.5 3:1 5:1", "4:1 3:1 2:1 R:1",
      "R:0.5 5:0.5 5:0.5 4:0.5 5:1 7:1", "6:1 5:1 4:0.5 3:0.5 R:1", "R:0.5 3:0.5 3:0.5 4:0.5 3:1 2:1", "1:2 R:2"]
HOOK = "こうじちゅうのすてっぷ"
C1 = f"{HOOK}/かんかんずんずん/{HOOK}/そらへのぼる/{HOOK}/とんとんがんがん/{HOOK}/あしたのまち"
C2 = f"{HOOK}/てっこつならべてく/{HOOK}/ひとつひとつ/{HOOK}/いのちづなつけて/{HOOK}/たかいところ"
C3 = f"{HOOK}/くみあがったよほら/{HOOK}/みらいのまど/{HOOK}/だれかがすむいえ/{HOOK}/できあがるよ"
LY = Lyrics(S)


def put(name, lines, text, o=4):
    bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", VA + VA, A1)
put("Bメロ1", VB, B1)
put("サビ1", VC + VC, C1)
put("Aメロ2", VA, A2)
put("Bメロ2", VB, B2)
put("サビ2", VC + VC, C2)
put("最後のサビ", VC + VC, C3)

# ================= マリンバ・ギター・パッド =================
def marimba(b, ch):
    t = tones(ch, "G4", "G5")
    MAR.bar(b, f"{nm(t[0])}:0.75 {nm(t[2 % len(t)])}:0.75 {nm(t[1])}:0.5 R:0.5 {nm(t[0])}:0.5 {nm(t[3 % len(t)])}:0.5 {nm(t[1])}:0.5")


def highlife(b, ch):
    t = tones(ch, "D5", "D6")
    GT.bar(b, f"R:0.5 {nm(t[0])}:0.25 {nm(t[1])}:0.25 R:0.5 {nm(t[2 % len(t)])}:0.5 R:0.5 {nm(t[1])}:0.25 {nm(t[0])}:0.25 R:1")


def pad(b, ch, c=62):
    v = voice(ch, c, 3)
    for j in range(3): PAD[j].bar(b, f"{nm(v[j])}:4")


MOTIF = "R:1 D5:0.5 F5:0.5 G5:1 F5:0.5 C5:0.5"     # 合いことばの節（3・5・6・5・2）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "イントロ":
        marimba(b, ch)
        if i >= 4: highlife(b, ch); pad(b, ch)
    elif n in ("Aメロ1", "Aメロ2"):
        marimba(b, ch)
        if n == "Aメロ2" or i >= 8: highlife(b, ch)
    elif n in ("Bメロ1", "Bメロ2"):
        marimba(b, ch); pad(b, ch, 60)
    elif n in ("サビ1", "サビ2", "最後のサビ", "打楽器"):
        marimba(b, ch); highlife(b, ch); pad(b, ch, 64)
    elif n == "サイレン":
        pad(b, ch, 62)
        MAR.bar(b, [MOTIF, "Bb4:3 R:1", "R:4", "R:4"][i])
    elif n == "クレーン":
        if i < 3: marimba(b, ch); pad(b, ch, 64)
        else: MAR.bar(b, "G4:3 R:1")

# ================= 工事の音（打楽器）=================
HPAT = ["D3:0.5 R:1 D3:0.5 R:2", "D3:0.5 R:1 D3:0.5 R:0.5 E3:0.25 E3:0.25 R:1", "D3:0.5 R:0.25 E3:0.25 R:0.5 D3:0.5 R:0.5 E3:0.25 E3:0.25 D3:1"]
CPAT = "A2:0.75 C3:0.75 C3:0.5 A2:0.75 C3:0.25 D#3:0.5 C3:0.5"
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "ヘルメット":
        HELM.bar(b, HPAT[min(i, 2)])
        if i >= 2: CONGA.bar(b, CPAT)
    elif n in ("サイレン", "クレーン"):
        if n == "クレーン" and i < 3: HELM.bar(b, HPAT[2]); CONGA.bar(b, CPAT)
    elif n == "打楽器":
        HELM.bar(b, HPAT[2]); CONGA.bar(b, CPAT if i < 4 else "A2:0.25 A2:0.25 C3:0.5 C3:0.5 D#3:0.5 A2:0.25 A2:0.25 C3:0.5 D#3:0.5 C3:0.5")
        if i >= 2: BELLS.bar(b, "C5:0.75 C5:0.75 C5:0.5 R:2")
    else:
        if n in ("サビ1", "サビ2", "最後のサビ") or (n in ("Aメロ1", "Aメロ2") and i % 2 == 1): HELM.bar(b, HPAT[1])
        CONGA.bar(b, CPAT)
        if n in ("サビ1", "サビ2", "最後のサビ") and i % 2 == 0: BELLS.bar(b, "C5:0.75 C5:0.75 C5:0.5 R:2")

SIREN.bar(S.sc("サイレン")[0], "D4:8"); CRANE.bar(S.sc("クレーン")[3], "G1:4")

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n in ("ヘルメット",) or (n == "イントロ" and i < 4): continue
    if n == "サイレン": BASS.bar(b, f"{nm(r)}:4" if i >= 2 else "R:4"); continue
    if n == "クレーン": BASS.bar(b, f"{nm(r)}:4" if i < 3 else "R:4"); continue
    BASS.bar(b, f"{nm(r)}:0.75 R:0.25 {nm(r)}:0.5 R:0.5 {nm(r + 7)}:0.75 R:0.25 {nm(r + 10)}:0.5 {nm(r + 12)}:0.5")

# ================= ドラム（アフロビーツ: 3＋3＋2 のキック・リムの裏）=================
AK, AS, AH = "X..X..X.X.......", "....X..x....X...", "x.xxx.xxx.xxx.xx"
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "ヘルメット" or (n == "イントロ" and i < 4) or n == "サイレン":
        if n == "サイレン" and i == 3: put_fill(D, b, "build")
        continue
    if n == "クレーン":
        if i == 0: crash(D, b, "C2", 6)
        if i < 3: vgroove(D, b, "beat8", ghosts=0.0, seed=b, k=AK, s=AS, h=AH)
        continue
    vgroove(D, b, "beat8", ghosts=0.0, seed=b, k=AK, s=AS, h=AH if n not in ("Aメロ1",) or i >= 4 else "x...x...x...x...")
    if n in ("サビ1", "サビ2", "最後のサビ") and i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
    if n in ("Bメロ1", "Bメロ2") and i == 7: put_fill(D, b, "snare16")
    elif i % 8 == 7 and not last: put_fill(D, b, "small")

SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の14（13時）。アフロビーツ。G短調・104。工事現場の音（ヘルメット・かなづち）がそのまま打楽器になる。"
          "マリンバ・ハイライフのギター・コンガのかわりの太鼓・カウベル。合いことばの節はサイレンのあとのマリンバ。クレーンが止まって終わる。自作")
finish(S, LY, V, 0,
       level={"verse": -0.2}, special={"サイレン": -0.6, "最後のサビ": 0.35, "打楽器": 0.1})

# ================= v2（2026-11-11 作り直し。docs/sound/vt3-remake-plan.md）=================
# この曲（午後1時・工事現場の音がリズムになる・アフロビーツ）で直すこと:
#   ギター: ハイライフの単音の線を、DI ギター（明るいクリーン・粒をそろえる）に。1音ずつ強さを揺らす
#   電子の音: パッドをきらきらのパッド、ベースをはじく FM のベースに
#   歌: Aメロ・Bメロはクリア、サビはキュート（現場のかけ声のように明るく）。ハモリは サビ2 の後半と最後のサビ
from vt3x_lib import *
path = sys.argv[1]
to_di(path, S, "ギター（ハイライフ", "bright_line", role="ギター（ハイライフの単音・DI）", vol=0.06, seed=4)
set_parts(path, "ベース", sustain=1.1)
final_gain(path, {"ヘルメット": 6, "イントロ": 1.5, "最後のサビ": 2.2})
if VOCAL:
    remark(path, S, std_mark(("chorus",), jump=5))
    vocal_polish(path, S, {"verse": 6, "pre": 12, "chorus": 18, "最後のサビ": 22, "break": 0, "outro": 0}, scoop=0.3, slash=0.8, vib_min_beats=1.5, vib_start=0.5, auto=0.5, breaths=0.5)
    harmony(path, S, [("サビ2", 8, None, K), ("最後のサビ", 0, None, K)], vol=0.36)
    voice_by_scene(path, S, {"verse": "clear", "pre": "clear", "chorus": "cute"}, default="clear")
