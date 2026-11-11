# vt3 11「洗濯日和のステップ」Laundry-Day Step（仮）— レゲトン（ラテンポップ）。96・4/4（デンボウ）。A短調 → 最後のサビは +1（B♭短調）。
# 第3弾（0時〜24時の街）の 10時。表は docs/sound/vt3-plan.md。
# 物語: 晴れた10時。洗濯機がぐるりと回り、雲ひとつない空。はだしでベランダに出て、白いシーツをぱたぱた干していると、
#   風に背中を押されて、からだが勝手にゆれ出す。口ずさむのは、けさ聞いた鼻歌。となりのばあちゃんが手拍子をくれて、
#   シャツもくつしたも踊り出す。くつしたが片方とんでいっても、まあいいか。最後は洗濯ばさみの「パチン」。
# 場面と強さ: 洗濯機（回る低い音とギター・弱）→ Aメロ1（はずむ語り・中）→ Bメロ1（ためる・止め）→ サビ1（強）→ 間奏（スパニッシュギター・節）
#   → Aメロ2 → Bメロ2 → サビ2 → 洗濯機が止まる（ギターだけ・弱）→ 最後のサビ（+1・ハイハットが倍・いちばん強い）→ パチン
# 旋律の性格: デンボウ（3＋3＋2）に乗る歯切れのよい言葉（C4〜E4 中心）、サビは明るく C5〜F5 まで開く。
# この曲だけの音: デンボウのリズムと、スパニッシュギターのかき鳴らし（ラスゲアード）。洗濯機の回る音で始まり、洗濯ばさみの「パチン」で終わる。
#   合いことばの節（3・5・6・5・2）は、間奏のスパニッシュギター（C長調として E・G・A・G・D）。
from vt25_lib import *

S = Song("11", "laundry", "洗濯日和のステップ（仮）", "Laundry-Day Step", 96, 4, "A", "minor", "レゲトン（ラテンポップ・ボカロ）")
S.kit = "electro"
S.flags = S.flags + " --space room --space-wet 0.12"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.5
K = Key("A", "minor")          # oct 3 で 1 = A3
KL = Key("Bb", "minor")        # 最後のサビ（+1）

A_CH = ["Am", "Fmaj7", "Dm7", "E7"]
B_CH = ["Dm7", "Em7", "Fmaj7", "G", "Dm7", "Em7", "Fmaj7", "E7sus4"]
C_CH = ["Fmaj7", "G", "Em7", "Am", "Fmaj7", "G", "E7sus4", "E7"]

S.scene("洗濯機", 4, "intro", ["Am", "Fmaj7", "Dm7", "E7"])
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 8, "break", A_CH)
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("洗濯機が止まる", 4, "bridge", ["Dm7", "Em7", "Fmaj7", "F7"])     # 最後は B♭m への入り口
S.scene("最後のサビ", 16, "chorus", [tr_chord(c, 1) for c in C_CH])
S.scene("パチン", 2, "outro", ["Bbm", "Bbm"])

V = Voice(S, vol=0.2, delay=0.5, bright=0.0, patch="kfbSineLead", low=False)   # v2: 歌をなぞるシンセは、高さの揺れない音に
GS = [S.track(f"スパニッシュギター{i + 1}", "guitar", patch="nylonGuitar", amp="crystal", volume=0.07, pan=-0.35, reverb=0.25, chorus=0, sustain=0.5) for i in range(4)]
GSL = S.track("スパニッシュギター（旋律）", "guitar", patch="nylonGuitar", amp="crystal", volume=0.11, pan=-0.15, reverb=0.3, chorus=0, sustain=0.8)
MAR = S.track("マリンバ（分散和音）", "strings", patch="marimba", volume=0.09, pan=0.35, reverb=0.25)
BRS = [S.track(f"シンセのブラス{i + 1}", "brass", patch="brassSection", volume=0.05, pan=0.3, reverb=0.25, sustain=0.4) for i in range(3)]
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("fbChord", vol=0.03, pan=-0.5 + 0.5 * i, duck=0.45, sustain=1.2)) for i in range(3)]
SUB = S.track("808", "sub808", volume=0.16, pan=0, sustain=0.9, fx=[{"type": "filter", "kind": "highpass", "freq": 30, "q": 0.7}])
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.06, pan=0, reverb=0.3)
WASH = S.track("洗濯機の回る音", "pad", patch="surgePadMwPulsating", volume=0.04, pan=0, reverb=0.2, sustain=1.0,
               fx=[{"type": "filter", "kind": "lowpass", "freq": 500, "q": 0.9}])
CLIP = S.track("洗濯ばさみ（カホンの縁）", "cajon", volume=0.09, pan=0.2, reverb=0.08)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 5:0.25 5:0.25 5:0.5 4:0.25 3:0.25 4:0.5 3:0.5 1:0.5 R:0.5", "R:1 3:0.5 4:0.5 5:1 R:1",
      "R:0.5 6:0.25 6:0.25 6:0.5 5:0.25 4:0.25 5:0.5 4:0.5 3:0.5 R:0.5", "R:1 2:0.5 3:0.5 4:1 R:1",
      "R:0.5 1':0.25 1':0.25 1':0.5 7:0.25 6:0.25 7:0.5 6:0.5 5:0.5 R:0.5", "R:1 4:0.5 5:0.5 6:1 R:1",
      "R:0.5 5:0.5 4:0.5 3:0.5 2:0.5 3:0.5 4:0.5 #5:0.5", "#7:2 R:2"]
A1 = ("せんたくきまわる/ぐるり/そらはまっさおだね/はれた/べらんだはだしで/でたよ/しーついっぱいだよ/"
      "ぱたぱたはたけば/かぜが/せなかをおしたら/ほらね/からだがかってにね/ゆれる/けさのはなうただ")
A2 = "となりのばあちゃん/みてる/てびょうしをくれた/にこり/しゃつもくつしたも/おどる/ものほしすてーじ"
VB = ["R:0.5 4:0.5 4:0.5 4:0.5 5:1 6:1", "5:1 4:1 3:1 R:1", "R:0.5 5:0.5 5:0.5 5:0.5 6:1 7:1", "6:1 5:1 4:1 R:1",
      "R:0.5 6:0.5 6:0.5 6:0.5 7:1 1':1", "7:1 6:1 5:1 R:1", "R:0.5 3':0.5 2':0.5 1':0.5 7:0.5 6:0.5 7:1", "R:4"]
B1 = "やることはいっぱい/でもいまはいいの/かぜがふくうちは/おどっていたい"
B2 = "くるくるまわるよ/あたまもからだも/よごれもなやみも/あわになあれ"
VC = ["R:0.5 1':0.5 1':0.5 3':0.5 2':0.75 1':0.25 7:1", "1':1.5 5:0.5 5:1 R:1",
      "R:0.5 7:0.5 7:0.5 2':0.5 1':0.75 7:0.25 6:1", "5:2 R:2",
      "R:0.5 1':0.5 1':0.5 3':0.5 4':0.75 3':0.25 2':1", "3':1.5 1':0.5 1':1 R:1",
      "R:0.5 6:0.5 7:0.5 1':0.5 2':0.5 1':0.5 7:0.5 6:0.5", "#7:2 R:2",
      "R:0.5 3':0.5 3':0.5 5':0.5 4':0.75 3':0.25 2':1", "3':1.5 1':0.5 1':1 R:1",
      "R:0.5 2':0.5 2':0.5 4':0.5 3':0.75 2':0.25 1':1", "7:2 R:2",
      "R:0.5 1':0.5 3':0.5 5':0.5 6':0.75 5':0.25 4':1", "3':1.5 2':0.5 1':1 R:1",
      "R:0.5 6:0.5 7:0.5 1':0.5 2':0.5 3':0.5 2':0.5 #7:0.5", "1':3 R:1"]
C1 = ("せんたくびよりだよ/しーつはためく/かぜのりずむにのって/そらまでおどろう/"
      "せんたくびよりだよ/あわもはじける/まっしろなきもちなら/どこへでもいける")
C2 = ("せんたくびよりだよ/くつしたかたっぽ/どこかにとんでいった/それでもいいかな/"
      "せんたくびよりだよ/ばあちゃんおどる/ちいさなべらんだが/ぶたいにかわるよ")
C3 = ("せんたくびよりだよ/おひさまいっぱい/ふかふかにかわいて/おひさまのにおい/"
      "せんたくびよりだよ/あしたもはれる/せんたくばさみがね/ぱちんとなるんだ")
LY = Lyrics(S)


def put(name, key, lines, text, o=3):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA + VA, A1)
put("Bメロ1", K, VB, B1)
put("サビ1", K, VC, C1)
put("Aメロ2", K, VA, A2)
put("Bメロ2", K, VB, B2)
put("サビ2", K, VC, C2)
put("最後のサビ", KL, VC, C3)

# ================= ギター・マリンバ・ブラス =================
def rasg(b, ch):
    """スパニッシュギターのかき鳴らし（3＋3＋2）。低音は根音、上は和音"""
    r = low(ch, "E2"); v = voice(ch, 62, 3)
    GS[0].bar(b, f"{nm(r)}:0.75 {nm(r)}:0.75 {nm(r + 7)}:0.5 {nm(r)}:0.75 {nm(r)}:0.75 {nm(r + 7)}:0.5")
    for j in range(3): GS[j + 1].bar(b, f"{nm(v[j])}:0.75 {nm(v[j])}:0.75 {nm(v[j])}:0.5 {nm(v[j])}:0.75 {nm(v[j])}:0.75 {nm(v[j])}:0.5")


def marimba(b, ch):
    t = tones(ch, "A4", "A5")
    MAR.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 1, 3, 2, 1, 3, 2)))


def brass(b, ch, pat):
    v = voice(ch, 66, 3)
    for j in range(3): BRS[j].bar(b, " ".join(t.replace("x", nm(v[j])) for t in pat.split()))


def pad(b, ch):
    v = voice(ch, 62, 3)
    for j in range(3): PAD[j].bar(b, f"{nm(v[j])}:4")


MOTIF = "R:1 E5:0.5 G5:0.5 A5:1 G5:0.5 D5:0.5"   # 合いことばの節（3・5・6・5・2）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "洗濯機":
        WASH.bar(b, f"{nm(low(ch, 'A2'))}:4")
        if i >= 2: rasg(b, ch)
    elif n in ("Aメロ1", "Aメロ2"):
        rasg(b, ch)
        if n == "Aメロ2" or i >= 8: marimba(b, ch)
    elif n in ("Bメロ1", "Bメロ2"):
        if i < 7: rasg(b, ch); pad(b, ch)
        if i % 2 == 1 and i < 7: brass(b, ch, "R:2.5 x:0.5 x:0.5 x:0.5")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        rasg(b, ch); marimba(b, ch); pad(b, ch)
        brass(b, ch, "x:0.75 x:0.75 x:0.5 R:2" if i % 2 == 0 else "R:2 x:0.75 x:0.75 x:0.5")
    elif n == "間奏":
        rasg(b, ch)
        SOLO = [MOTIF, "C5:3 R:1", "R:0.5 A4:0.5 C5:0.5 D5:0.5 E5:1 F5:1", "E5:1 D5:1 B4:1 G#4:1",
                "R:0.5 E5:0.5 F5:0.5 E5:0.5 D5:1 C5:1", "A4:2 C5:2", "R:0.5 D5:0.5 C5:0.5 B4:0.5 C5:1 D5:1", "E5:3 R:1"]
        GSL.bar(b, SOLO[i])
    elif n == "洗濯機が止まる":
        rasg(b, ch) if i % 2 == 0 else None
        WASH.bar(b, f"{nm(low(ch, 'A2'))}:2 R:2" if i == 0 else "R:4")
    elif n == "パチン":
        if i == 0: rasg(b, ch)

CLIP.bar(S.sc("パチン")[1], "R:1 F3:0.25 R:2.75")       # 洗濯ばさみの「パチン」

# ================= 808 =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "C1")
    if n in ("Aメロ1", "Aメロ2", "サビ1", "サビ2", "最後のサビ", "間奏") or (n in ("Bメロ1", "Bメロ2") and i < 7):
        SUB.bar(b, f"{nm(r)}:0.75 R:0.75 {nm(r)}:0.5 {nm(r)}:0.75 R:0.75 {nm(r + 7)}:0.5")
    elif n == "パチン" and i == 0: SUB.bar(b, f"{nm(r)}:2 R:2")

riser(FX, S.sc("サビ1")[0], 4, "C4"); riser(FX, S.sc("最後のサビ")[0], 4, "C4")

# ================= ドラム（デンボウ）=================
DK, DS, DH = "X...X...X...X...", "...x..x....x..x.", "x.x.x.x.x.x.x.x."
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "洗濯機":
        if i == 3: D.set(b, "................", "...x..x....x..x.", "x.x.x.x.x.x.x.x.")
    elif n in ("Aメロ1", "Aメロ2", "間奏"):
        vgroove(D, b, "beat8", ghosts=0.0, seed=b, k=DK, s=DS, h=DH if (n != "Aメロ1" or i >= 4) else "................")
        if i == 0: crash(D, b)
    elif n in ("Bメロ1", "Bメロ2"):
        if i < 7: vgroove(D, b, "beat8", ghosts=0.0, seed=b, k="X.......X.......", s=DS, h=DH)
        if i == 6: put_fill(D, b, "build")
    elif n in ("サビ1", "サビ2"):
        vgroove(D, b, "beat8", ghosts=0.0, seed=b, k=DK, s=DS, h="x.xxx.x.x.xxx.x.")
        if i % 8 == 0: crash(D, b)
        if i % 8 == 7 and not last: put_fill(D, b, "small")
    elif n == "最後のサビ":   # ハイハットが倍（16分）
        vgroove(D, b, "beat8", ghosts=0.0, seed=b, k=DK, s=DS, h="xxxxxxxxxxxxxxxx")
        if i % 8 == 0: crash(D, b, "C2", 6 if i == 0 else 4)
        if i % 8 == 7 and not last: put_fill(D, b, "small")
    elif n == "洗濯機が止まる":
        if i == 3: put_fill(D, b, "build")
    elif n == "パチン":
        if i == 0: D.set(b, "X...............", "................", "................"); crash(D, b, "C2", 6)

for name in ("Bメロ1", "Bメロ2"): SIL.add(S.sc(name)[-1], 0, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の11（10時）。レゲトン（ラテンポップ）。A短調・96、最後のサビは +1。晴れた日、洗濯物を干しながら踊ってしまう。"
          "デンボウのリズム・スパニッシュギターのかき鳴らし・マリンバ・808。合いことばの節は間奏のスパニッシュギター。洗濯機の音で始まり、洗濯ばさみの「パチン」で終わる。自作")
finish(S, LY, V, 0,
       level={"verse": -0.2}, special={"洗濯機が止まる": -0.6, "最後のサビ": 0.4})

# ================= v2（2026-11-11 作り直し。docs/sound/vt3-remake-plan.md）=================
# この曲（午前10時・屋上の洗濯物・レゲトン）で直すこと:
#   電子の音: パッドをキックで凹むうねる和音（fbChord）に。洗濯の「泡」と「水滴」の効果音（kawaiiFx）を、洗濯機の場面と間奏、サビの頭に置く（この曲だけの音）。
#            サビ2 と最後のサビの句の終わりに、短い矩形波のプラックが「上がって下がる」山の形で入る（ほかの曲とは形を変える）
#   ギター: スパニッシュギターの1音ずつの強さを揺らす
#   歌: Aメロ・Bメロはクリア、サビはキュート（晴れた屋上）、洗濯機が止まる所はウィスパー。ハモリは サビ2 の後半と最後のサビ
from vt3x_lib import *
path = sys.argv[1]
fx, run = {}, {}
w = S.sc("洗濯機"); fx[w[0]] = "C4:1 R:1 C#4:0.5 R:1.5"; fx[w[-1]] = "R:2 C4:0.5 C4:0.5 C#4:1"
for q, b in enumerate(S.sc("間奏")):
    if q % 2 == 0: fx[b] = "R:3 C4:0.5 C#4:0.5"
for name in ("サビ1", "サビ2", "最後のサビ"): fx[S.sc(name)[0]] = "D4:2 R:2"
for name in ("サビ2", "最後のサビ"):
    for q, b in enumerate(S.sc(name)):
        t = tones(S.chords[b].split("|")[0].split("/")[0], "A4", "E6")
        if q % 4 == 3 and len(t) >= 5: run[b] = "R:2 " + " ".join(f"{nm(t[z])}:0.25" for z in (0, 2, 3, 4, 4, 3, 2, 0))
parts = [pad_part(S, "泡と水滴", "kawaiiFx", fx, 0.06, pan=0.2, reverb=0.2, modulate=False, instrument="guitar"),
         pad_part(S, "プラック（山の形）", "kfbSquarePluck", run, 0.042, pan=0.35, reverb=0.25, fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.15, "feedback": 0.25}])]
add_parts(path, parts)
humanize(path, "スパニッシュギター", mid=84, down=12, up=10, seed=7)
if VOCAL:
    remark(path, S, std_mark(("chorus",), jump=5))
    vocal_polish(path, S, {"verse": 8, "pre": 14, "chorus": 20, "最後のサビ": 24, "bridge": 0, "outro": 0}, scoop=0.3, slash=0.8, vib_min_beats=1.5, vib_start=0.5, auto=0.6, breaths=0.5)
    harmony(path, S, [("サビ2", 8, None, K), ("最後のサビ", 0, None, KL)], vol=0.36)
    voice_by_scene(path, S, {"verse": "clear", "pre": "clear", "chorus": "cute", "bridge": "whisper"}, default="clear")
