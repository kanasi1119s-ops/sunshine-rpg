# vb25 22「7色シグナル」Seven-Color Signal（仮）— K-POP（ダンスポップ）。G#m（サビは平行調の B）・124 → 最後のサビは倍のノリ（体感 248）・4/4。最後のサビは +1（C）
# 2026-10-25 作り直し: 物語を人の気持ちの話に（毎朝、交差点の向こうにいる人に「おはよう」を言いたい）、歌を人が歌える旋律（8分と4分）に、テトの歌の版を足した。
#   テトの声に合うよう、曲全体を D短調から 6半音下げて G#短調にした（書くのは D短調／F長調の度数のまま、書き出しの前に下げる）。
# 物語: 毎朝8時、この交差点の向こう側に、名前も声も知らないきみがいる。赤信号のあいだだけ、そっと見つめて、青になればすれちがう。
#   今日は決めてきた。黄色、どきどき、胸の中の信号まで7色に変わる。目と目が合って、「はじめまして」。あしたもこの道で。
# 場面と強さ: 指パッチン（小）→ 青信号（シンセブラスのフック・中）→ 交差点（Aメロ）→ 黄色（Bメロ・溜め）→ 赤信号の止め（全員休み）
#   → 7色ドロップ（サビ・強。808 とブラス）→ 2番（BGM は前半ブラスが歌を受け取る）→ 赤信号の止め → 7色ドロップ2
#   → 赤信号（1小節の止め）→ ブレイクダンスの間奏（ブレイクビーツと 808。BGM は掛け声のチョップ）→ 夜明けの点滅（Cメロ・Half feel）
#   → 1拍の無音 → 倍のノリの最後のサビ（+1・最大）→ 信号の音で切る
# 旋律の性格: Aメロは句の頭を休んで8分で語る。サビは付点8分のはねるリズムの「なないろシグナル」。最高音 F#5。
# 定番以外の和音: サビの C#dim（vi へ入る減三和音）、Cメロの E♭maj7（♭VII）→ D♭7（半音上の調の属和音へ）
from vb25_lib import *

S = Song("22", "signal", "7色シグナル（仮）", "Seven-Color Signal", 124, 4, "D", "minor", "K-POP（ダンスポップ）")
S.kit = "electro"
S.flags = "--ref-tone glossy-jrock " + S.flags
K = S.key                    # D 短調（oct=4 で 1＝D4）
KF = Key("F", "major")       # サビ
KG = Key("Gb", "major")      # 最後のサビ（+1）


def chk(key, lines, beats=4):
    for l in lines: assert abs(total(key.mel(l, oct=4)) - beats) < 1e-6, ("拍の数", l)


HOOK_CH = ["Dm", "Bb", "C", "A7"]
A_CH = ["Dm", "Bb", "C", "Am"] * 3 + ["Dm", "Bb", "Gm7", "A7"]
B_CH = ["Gm7", "Am7", "Bbmaj7", "C", "Gm7", "Am7", "Bbmaj7", "C7sus4"]
C_CH = ["Bbmaj7", "C", "Am7", "Dm", "Bbmaj7", "C", "C#dim", "Dm"]
BRK_CH = ["Dm", "Dm", "Bb", "C"]
CM_CH = ["Bbmaj7", "Am7", "Gm7", "Fmaj7", "Ebmaj7", "Dm7", "Ebmaj7", "Db7"]
LAST_CH = ["Bmaj7", "Db", "Bbm7", "Ebm", "Bmaj7", "Db", "Ddim", "Ebm"]

S.scene("指パッチン", 4, "intro", ["Dm"] * 4)
S.scene("青信号", 8, "intro", HOOK_CH)
S.scene("交差点のラップ", 16, "verse", A_CH)
S.scene("黄色", 8, "pre", B_CH)
S.scene("7色ドロップ", 16, "drop", C_CH)
S.scene("点滅", 4, "interlude", HOOK_CH)
S.scene("交差点のラップ2", 16, "verse", A_CH)
S.scene("黄色2", 8, "pre", B_CH)
S.scene("7色ドロップ2", 16, "drop", C_CH)
S.scene("赤信号", 1, "break", ["A7"])
S.scene("ブレイクダンス", 16, "interlude", BRK_CH)
S.scene("夜明けの点滅", 8, "bridge", CM_CH)
S.scene("倍のノリ", 16, "chorus", LAST_CH)
S.scene("まだ踊る", 4, "outro", ["Bmaj7", "Db", "Ebm", "Ebm"])
S.scene("信号が戻る", 4, "outro", ["Ebm", "Ebm", "Ebm", "Ebm"])

V = Voice(S, vol=0.22, delay=0.75, patch="popLeadClear", low=True)   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
SB = [S.track(f"シンセのブラス{i + 1}", "pad", patch="polysynth", volume=0.075, pan=0.0, reverb=0.18, sustain=0.6, duck=0.2,
              fx=[{"type": "filter", "kind": "highpass", "freq": 200, "q": 0.7}, {"type": "eq", "low": 0, "mid": 3, "midHz": 1400, "high": 1}]) for i in range(3)]
BRM = S.track("ブラス（フック・歌の受け渡し）", "brass", patch="brassSection", volume=0.2, pan=-0.2, reverb=0.22, gainDb=3, phrase=4,
              fx=[{"type": "eq", "low": -3, "mid": 2, "midHz": 1800, "high": 0.5}])
B808 = S.track("808", "sub808", **sub_spec(0.21))
BASS = S.track("シンセベース（うなり）", "bass", **synth_bass_spec("synthBass2", vol=0.14, duck=0.3))
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("warmPad", vol=0.05, pan=0.0, duck=0.35)) for i in range(3)]
PLK = S.track("プラック（7色の光）", "pad", **pluck_spec("pluckSynth", vol=0.08, pan=0.45, delay=0.75, sustain=0.5))
SIG = S.track("信号の音（パルス波）", "lead", patch="chipPulse12", volume=0.08, pan=-0.35, reverb=0.25, mono=True,
              fx=[{"type": "filter", "kind": "highpass", "freq": 300, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.7}])
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の旋律と歌詞（D短調／F長調の度数。書き出しの前に全体を 6半音下げる） =================
VERSE = ["R:1 3:0.5 3:0.5 5:0.5 3:0.5 1':1", "6:1.5 3:0.5 R:2", "R:1 4:0.5 4:0.5 7:0.5 4:0.5 2':1", "7:1.5 5:0.5 R:2",
         "R:1 1':0.5 1':0.5 7:0.5 6:0.5 5:1", "6:1 3:1 R:2", "R:1 2:0.5 4:0.5 7:0.5 4:0.5 5:1", "5:2 R:2",
         "R:0.5 5:0.5 5:0.5 5:0.5 3:0.5 5:0.5 1':1", "6:1 1':1 R:2", "R:0.5 4:0.5 4:0.5 4:0.5 2:0.5 4:0.5 7:1", "5:1 7:1 R:2",
         "R:0.5 1':0.5 1':0.5 1':0.5 3':0.5 1':0.5 5:1", "6:1 1':1 3':1 R:1", "R:0.5 4:0.5 6:0.5 1':0.5 3':1 1':1", "#7:2 R:2"]
V1 = "まいあさはちじ/このこうさてん/むこうがわにね/きみがいるの/あかのあいだだけ/そっとみつめている/あおになればすぐに/すれちがうの"
V2 = "なまえもしらず/こえもしらない/だけどきょうはね/きめてきたの/おはようっていうよ/しんごうがかわる/むねのしんごうまで/いろがかわる"
BM = ["R:1 2:0.5 2:0.5 4:0.5 6:0.5 1':1", "7:1 5:1 3:1 R:1", "R:1 4:0.5 4:0.5 6:0.5 1':0.5 3':1", "2':1 7:1 5:1 R:1",
      "R:0.5 6:0.5 6:0.5 6:0.5 1':1 2':1", "3':1 2':1 7:1 R:1", "R:0.5 1':0.5 3':0.5 4':0.5 3':1 1':1", "2':1 R:3"]
P1 = "きいろにかわるよ/きみがこっちをみた/むねがさわいでる/とまれとまれ"
P2 = "ことばがつまるよ/あしがすくんでる/それでもいわなきゃ/いまだすすめ"
# サビ（F長調）: 付点8分ではねる「なないろシグナル」
HK = "R:0.5 1':0.5 1':0.5 6:0.5 1':0.75 3':0.75 2':0.5"
CH = [HK, "2':1.5 7:0.5 R:2", "R:0.5 1':0.5 1':0.5 7:0.5 1':0.75 2':0.75 1':0.5", "6:1.5 3:0.5 R:2",
      HK, "2':1.5 7:0.5 R:2", "R:0.5 7:0.5 7:0.5 #5:0.5 7:0.75 2':0.75 2':0.5", "1':2 R:2",
      HK, "2':1.5 7:0.5 R:2", "R:0.5 3':0.5 3':0.5 2':0.5 3':0.75 5':0.75 3':0.5", "3':1.5 1':0.5 R:2",
      "R:0.5 4':0.5 4':0.5 3':0.5 1':0.75 6:0.75 1':0.5", "2':1.5 5:0.5 R:2", "R:0.5 #5:0.5 7:0.5 2':0.5 2':1 7:1", "6:2 R:2"]
C1 = "なないろしぐなる/まちがひかりだす/なないろしぐなる/きみまでのみち/なないろしぐなる/あおでもあかでも/わたらせてほしい/このきもちを"
C2 = "なないろしぐなる/きみがふりむいた/なないろしぐなる/ふたりのあいだ/なないろしぐなる/まちがおどりだす/いまならいえるよ/はじめまして"
CM = ["R:1 1':1 6:1 4:1", "5:2 R:2", "R:1 2:1 4:1 6:1", "3:2 R:2", "R:1 b7:1 2':1 4':1", "3':2 R:2", "R:0.5 4:0.5 6:0.5 b7:0.5 2':2", "b6:1 1':1 b3':1 R:1"]
# 最後のサビ（G♭長調・+1）: いちばん高い所は F#5 に収める
LAST = CH[:10] + ["R:0.5 3':0.5 3':0.5 2':0.5 3':0.75 2':0.75 1':0.5", "3':1.5 1':0.5 R:2", HK, "2':1.5 7:0.5 R:2",
                  "R:0.5 7:0.5 2':0.5 #5:0.5 2':2", "1':4"]
CL = "なないろしぐなる/きみとならんでる/なないろしぐなる/ふたりでわたる/なないろしぐなる/あしたもこのみち/なないろしぐなる/わたれるよ"
TAG = [HK, "2':1.5 7:0.5 R:2", "R:4", "R:4"]
chk(K, VERSE); chk(KF, BM); chk(KF, CH); chk(KF, CM); chk(KG, LAST); chk(KG, TAG)

LY = Lyrics(S)
def put(name, key, lines, text, low=True, bars=None):
    bars = bars or S.sc(name); mel = [key.mel(x, oct=4) for x in lines]
    ob, om = [], []
    for i, (b, m) in enumerate(zip(bars, mel)):
        if lines[i] == "R:4": continue
        V.bar(b, m, low=low if not callable(low) else low(i)); ob.append(b); om.append(m)
    LY.flow(ob, om, text, name)
put("交差点のラップ", K, VERSE, V1)
if VOCAL: put("交差点のラップ2", K, VERSE, V2)
else:
    for i, b in enumerate(S.sc("交差点のラップ2")):
        if i < 8: BRM.bar(b, K.mel(VERSE[i], oct=4))           # BGM: ブラスが歌を受け取る
        else: V.bar(b, K.mel(VERSE[i], oct=4))
put("黄色", KF, BM, P1); put("黄色2", KF, BM, P2)
put("7色ドロップ", KF, CH, C1); put("7色ドロップ2", KF, CH, C2)
put("夜明けの点滅", KF, CM, "てんめつ/しんごう/ねむれず/きみをおもってた", low=lambda i: i >= 4)
put("倍のノリ", KG, LAST, CL)
put("まだ踊る", KG, TAG, "なないろしぐなる")
# ブレイクダンス: BGM だけ、歌の役は掛け声のチョップ（「ヘイ」「ホー」のような短い音）
CHOP = ["R:1 1':0.25 R:0.75 R:1 5:0.25 R:0.25 1':0.25 R:0.25", "R:4", "R:1 6:0.25 R:0.75 R:1 2':0.25 R:0.25 1':0.25 R:0.25",
        "R:2 3':0.25 3':0.25 R:0.5 2':0.25 R:0.75"]
if not VOCAL:
    for i, b in enumerate(S.sc("ブレイクダンス")):
        if i >= 4: V.bar(b, KF.mel(CHOP[i % 4], oct=4), low=False)

# ================= ブラスのフック =================
HOOK = ["1:0.25' 1:0.25' R:0.5 3:0.5 1:0.25' R:0.75 5:0.5 4:0.5 3:0.5", "6:0.25' 6:0.25' R:0.5 1':0.5 6:0.25' R:0.75 5:0.5 4:0.5 3:0.5",
        "7:0.25' 7:0.25' R:0.5 2':0.5 7:0.25' R:0.75 1':0.5 7:0.5 5:0.5", "#7:0.5 R:0.5 #7:0.5 2':0.5 R:0.5 4':0.5 #7:1"]
chk(K, HOOK)
for name in ("青信号", "点滅"):
    for i, b in enumerate(S.sc(name)): BRM.bar(b, K.mel(HOOK[i % 4], oct=4))
for i, b in enumerate(S.sc("ブレイクダンス")):
    if i >= 8: BRM.bar(b, K.mel(HOOK[i % 4], oct=4))

# ================= 伴奏 =================
def sb(b, ch, pat, center=66):
    vv = voice(ch, center, 3)
    for j in range(3):
        SB[j].bar(b, " ".join(("R:" + x.split(":")[1]) if x.startswith("R") else f"{nm(vv[j])}:{x.split(':')[1]}" for x in pat.split()))


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    r = low(ch, "C1")
    # 808（キックの位置から長く）と、うなりのシンセベース
    if n in ("青信号", "点滅"): B808.bar(b, f"{nm(r)}:1.5 {nm(r)}:1 {nm(r)}:1.5")
    elif n.startswith("交差点"): B808.bar(b, f"{nm(r)}:2.5 {nm(r)}:1.5" if i % 2 == 0 else f"{nm(r)}:1.5 {nm(r)}:0.5 {nm(r + 12)}:1 {nm(r)}:1")
    elif n.startswith("黄色"): B808.bar(b, f"{nm(r)}:4" if i < L - 1 else f"{nm(r)}:2 R:2")
    elif n.startswith("7色ドロップ"):
        B808.bar(b, f"{nm(r)}:0.75 {nm(r)}:0.75 {nm(r + 12)}:0.5 {nm(r)}:1 {nm(r)}:1")
        BASS.bar(b, bass_line(S, b, "house"))
    elif n == "ブレイクダンス": B808.bar(b, f"{nm(r)}:0.75 {nm(r)}:0.25 R:0.5 {nm(r)}:0.5 R:0.5 {nm(r + 12)}:0.5 {nm(r)}:1")
    elif n == "夜明けの点滅": BASS.bar(b, bass_line(S, b, "half"))
    elif n in ("倍のノリ", "まだ踊る"):
        B808.bar(b, f"{nm(r)}:1 {nm(r)}:1 {nm(r)}:1 {nm(r)}:1")
        BASS.bar(b, bass_line(S, b, "oct8"))                                    # 8分のオクターブで倍のノリを走らせる
    # シンセのブラス（和音の刻み）
    if n in ("青信号", "点滅"): sb(b, ch, "X:0.25 R:0.5 X:0.25 R:1 X:0.25 R:0.5 X:0.25 R:1")
    elif n.startswith("交差点") and i >= 8: sb(b, ch, "R:0.5 X:0.25 R:1.25 R:0.5 X:0.25 R:1.25")
    elif n.startswith("黄色"): sb(b, ch, "X:1 X:1 X:1 X:1" if i < L - 1 else "X:2 R:2", 62)
    elif n.startswith("7色ドロップ") or n in ("倍のノリ", "まだ踊る"): sb(b, ch, "X:0.75 X:0.75 X:0.5 R:0.5 X:0.5 X:1")
    elif n == "ブレイクダンス" and i < 8: sb(b, ch, "X:0.25 R:1.75 X:0.25 R:0.25 X:0.25 R:1.25")
    # パッド
    if n in ("夜明けの点滅",) or n.startswith("黄色") or n.startswith("7色") or n in ("倍のノリ", "まだ踊る"):
        vv = voice(ch, 58, 3)
        for j in range(3): PAD[j].bar(b, f"{nm(vv[j])}:4")
    # プラック（7色の光: 和音の音を16分で上下に散らす）
    if n.startswith("7色") or n == "倍のノリ" or (n.startswith("交差点") and i >= 8):
        t = tones(ch, "C4", "C6")
        PLK.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" for q in (0, 2, 4, 1, 3, 5, 2, 4, 6, 3, 5, 1, 4, 2, 6, 0)))
    if n == "夜明けの点滅":
        t = tones(ch, "C4", "C6"); PLK.bar(b, " ".join(f"{nm(t[q % len(t)])}:1" for q in (0, 2, 1, 3)))

# 信号の音（ピッ・ポッ）: 指パッチンの所・赤信号・最後
for i, b in enumerate(S.sc("指パッチン")):
    if i >= 2: SIG.bar(b, "A5:0.5 R:1.5 D6:0.5 R:1.5")
SIG.bar(S.sc("赤信号")[0], "A5:0.5 R:0.5 A5:0.5 R:2.5")
for i, b in enumerate(S.sc("信号が戻る")):
    SIG.bar(b, ["Bb5:0.5 R:1.5 Eb6:0.5 R:1.5", "Bb5:0.5 R:1.5 Eb6:0.5 R:1.5", "Bb5:0.5 R:0.5 Bb5:0.5 R:0.5 Bb5:0.5 R:0.5 Bb5:0.5 R:0.5", "Eb6:1 R:3"][i])
riser(FX, S.sc("7色ドロップ")[0], 4, "C4"); riser(FX, S.sc("倍のノリ")[0], 8, "D4")
FX.bar(S.sc("ブレイクダンス")[0], "G4:4")             # サブドロップ（ドーン）
cym_swell(CYM, S.sc("7色ドロップ2")[0], 2, "C4"); cym_swell(CYM, S.sc("倍のノリ")[0], 2, "C4")

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "指パッチン":
        D.set(b, "." * 16, "....o.......o...", "....x.......x...")          # 指パッチン（弱いスネアとハイハットを重ねて）
    elif n in ("青信号", "点滅"):
        vgroove(D, b, "four", seed=b, s="....X.......X...")
        if i == 0: crash(D, b)
        if last: put_fill(D, b, "snare16")
    elif n.startswith("交差点"):
        vgroove(D, b, "trap" if i < 8 else "twostep", ghosts=0.4, seed=b)
        if i == 0: crash(D, b)
        if i % 4 == 3: D.H[b] = D.H[b][:12] + "xxxx"
        if i == 15: put_fill(D, b, "small")
    elif n.startswith("黄色"):
        vgroove(D, b, "half" if i < 4 else "four", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 2)                                                   # 赤信号の止め
    elif n.startswith("7色ドロップ"):
        name = "four16" if n == "7色ドロップ" else ("jersey" if i < 8 else "four16")   # 2回目は前半をジャージークラブに入れかえ
        vgroove(D, b, name, ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16")
        if last: put_fill(D, b, "tomdown")
    elif n == "赤信号":
        D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "G2")
    elif n == "ブレイクダンス":
        # ブレイクビーツ（ゴーストの多いスネア、キックを動かす）
        kk = ["X.........X.....", "X.....X...X..X..", "X.........X.X...", "X.X.......X....."][i % 4]
        vgroove(D, b, "boombap", ghosts=0.7, seed=b, k=kk, s="....X..o.o..X..o")
        if i % 8 == 0: crash(D, b, "B2" if i else "C2")
        if i % 4 == 3: put_fill(D, b, "small" if i % 8 == 3 else "tomtrip")
    elif n == "夜明けの点滅":
        vgroove(D, b, "half", ghosts=0.5, seed=b, h="x...x...x...x...")
        if i == 0: crash(D, b)
        if last: D.set(b, "X.......X.......", "........X.XXXXXX", "." * 16)
    elif n in ("倍のノリ", "まだ踊る"):
        # 倍のノリ: キックは8分おき、スネアは8分の裏（体感 248 の 2・4拍）、ハイハットは16分
        D.set(b, "X...X...X...X..." if i % 4 != 3 else "X...X...X.X.X...", "..X...X...X...X." if i % 8 != 7 else "..X...X...XXXXXX",
              "XxxxXxxxXxxxXxxx")
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if n == "まだ踊る" and i == 2: crash(D, b, "C2")
        if n == "まだ踊る" and i == 3: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 8)
    elif n == "信号が戻る":
        pass

# 止め: 黄色の最後（2回）・赤信号の1小節（頭の一打のあと）・倍のノリの直前の1拍の無音
for name in ("黄色", "黄色2"): SIL.add(S.sc(name)[-1], 2, 4)
SIL.add(S.sc("赤信号")[0], 1, 4)
SIL.add(S.sc("夜明けの点滅")[-1], 3, 4)
SIL.apply()
# 赤信号の止めの中で、信号の音だけ鳴らす（無音のあとに置き直す）
SIG.bar(S.sc("赤信号")[0], "R:1.5 A5:0.5 R:0.5 A5:0.5 R:1")

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の22。K-POP（ダンスポップ）。G#短調・124（サビは B、最後のサビは倍のノリで +1 の C）。"
          "毎朝、交差点の向こうにいる人に「おはよう」を言いたい。指パッチンから、ブラスのフック、8分で語る Aメロ、黄色の Bメロと赤信号の止め、"
          "808 とブラスの7色ドロップ（2回目は前半ジャージークラブ）、ブレイクダンスの間奏、Half feel の夜明けの点滅、1拍の無音から倍のノリの最後のサビ、信号の音で切る。"
          "自作")
S.no_depth = True
teto(S, LY, V, transpose=-6, special={"倍のノリ": 0.55, "夜明けの点滅": -0.5, "まだ踊る": 0.3})
