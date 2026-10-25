# vb25 12「月曜日シンドローム・リセット」Monday Syndrome Reset（仮）— エレクトロニカ（エレクトロハウス）。D短調（サビは平行調の F長調）・176・4/4
# 最後のサビは +1（F#長調）
# 2026-10-25 作り直し: 歌を人が歌える旋律（8分と4分）に、音を Surge の音に、テトの歌の版を足した。04 と同じ「目覚まし」で始まらないよう、始まりをピアノのため息に変えた。
#   テトの声に合うよう、曲全体を G#短調から 6半音下げて D短調にした（書くのは G#短調の度数のまま、書き出しの前に下げる）。
# 物語: 憂うつな月曜の朝。目覚ましを止めて布団にもぐる。寝ぐせも直らない、ボタンもかけちがえる。でも、ため息をひとつ消して窓をあけたら、
#   朝の光。夢の中で小さい自分が「大丈夫、毎日が新しい始まり」と言ってくれた。いやな気分を上書きして、スキップで出かける。
# 場面と強さ: ため息（ピアノの下がる2音だけ）→ ベッドの中（Half feel・静か）→ 起き上がる（4つ打ち）→ ぼやき（Aメロ）→ 着がえる（Bメロ・止め）
#   → リセット（サビ・一気に開く）→ 駅まで（間奏・ピアノとベルの掛け合い）→ 2番（BGM はハウスのピアノが歌を受け取る）→ サビ2 → 跳ねる道
#   → 夢の中（Cメロ・Half feel）→ 上書き中（こもった音）→ 1拍の完全な無音 → 最後のサビ（+1）→ スキップで出かける
# 旋律の性格: Aメロは低め（A3〜A4）でぼやくように。サビは同じ音を3つ置いてオクターブ上へ一気に開く。最高音 F#5。
# ほかの曲とちがう所: ハウスのピアノ（M7・m7 の裏打ち）が主役のエレクトロハウス。Half feel で始まり、♭II（ナポリ）の明るいずれ。
from vb25_lib import *

S = Song("12", "mondayreset", "月曜日シンドローム・リセット（仮）", "Monday Syndrome Reset", 176, 4, "G#", "minor", "エレクトロハウス（ボカロ）")
S.kit = "electro"
S.flags = "--ref-tone glossy-jrock " + S.flags + " --piano salamander"
S.keep_old_synth = True
S.no_depth = True
K = S.key                       # G#短調
KB = Key("B", "major")          # サビ（平行調）
KC = Key("C", "major")          # 最後のサビ（+1）
up1 = lambda cs: [tr_chord(c, 1) for c in cs]

A_CH = ["G#m", "F#", "E", "A", "G#m", "F#", "Emaj7", "D#7"]               # i–♭VII–♭VI–♭II（A＝♭II）と長調の V（D#7）
B_CH = ["Emaj7", "F#", "D#m7", "G#m7", "C#m7", "F#", "Emaj7", "F#7sus4"]
C_CH = ["Emaj7", "B", "F#", "G#m7", "Emaj7", "B/D#", "C#m7", "F#"]         # IV–I–V–vi
C_CH2 = ["Emaj7", "B", "Baug", "Emaj7", "C#m7", "D#7", "Emaj7", "F#7sus4"]  # Baug＝増三和音・D#7＝vi への副属和音
BED = ["Emaj7", "D#m7", "C#m7", "G#m7"]
HOP = ["Emaj7", "F#", "D#m7", "G#m7", "Emaj7", "F#", "B", "B"]
DREAM = ["Emaj7", "D#m7", "C#m7", "G#m7", "Emaj7", "D#m7", "C#m7", "D#7",
         "A", "G#m7", "F#", "Emaj7", "C#m7", "D#m7", "Emaj7", "F#7sus4"]
OVER = ["Emaj7", "F#", "D#m7", "G#m7", "C#m7", "D#m7", "Emaj7", "G7"]       # 最後の G7 で C長調へ
TAG = up1(HOP)

S.scene("目覚ましの鳴りやみ", 2, "intro", ["G#m", "G#m"])
S.scene("ベッドの中", 8, "intro", BED * 2)
S.scene("起き上がる", 12, "intro", A_CH[:4] * 3)
S.scene("ぼやき", 16, "verse", A_CH)
S.scene("着がえる", 8, "pre", B_CH)
S.scene("スキップ", 16, "chorus", C_CH + C_CH2)
S.scene("駅まで", 16, "interlude", HOP * 2)
S.scene("ぼやき2", 16, "verse", A_CH)
S.scene("着がえる2", 8, "pre", B_CH)
S.scene("スキップ2", 16, "chorus", C_CH + C_CH2)
S.scene("跳ねる道", 8, "interlude", HOP)
S.scene("ベッドの中2", 16, "bridge", DREAM)
S.scene("上書き中", 8, "build", OVER)
S.scene("リセット", 24, "chorus", up1(C_CH + C_CH2) + TAG)
S.scene("スキップで出かける", 8, "outro", ["Fmaj7", "G", "Em7", "Am7", "Fmaj7", "G", "C", "C"])

V = Voice(S, vol=0.22, delay=0.75, patch="picoLeadRound", low=True)   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
PN = [S.track(f"ハウスのピアノ{i + 1}", "piano", **piano_spec(0.11, -0.15, 0.2)) for i in range(4)]
PNM = S.track("ハウスのピアノ（歌の受け渡し）", "piano", **piano_spec(0.17, -0.15, 0.2))
BELL = S.track("ベル", "pad", patch="surgeKeysBellKeys2156", volume=0.08, pan=0.35, reverb=0.4, sustain=1.2, gainDb=1)
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("surgePadPad2Mw", vol=0.06, pan=0.0, duck=0.4, sustain=1.6)) for i in range(3)]
BASS = S.track("シンセベース", "bass", **synth_bass_spec("surgeBassPop", vol=0.23, duck=0.3))
ALARM = S.track("ため息（電子ピアノ）", "pad", patch="surgeKeysLightEp", volume=0.12, pan=0.2, reverb=0.2, mono=True,
                fx=[{"type": "filter", "kind": "highpass", "freq": 600, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.7}])
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.075, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
LPF = {"type": "filter", "kind": "lowpass", "freq": 800, "q": 0.8}
PNF = [S.track(f"こもったピアノ{i + 1}", "piano", **{**piano_spec(0.12, -0.15, 0.2), "fx": [LPF]}) for i in range(3)]
PADF = [S.track(f"こもったパッド{i + 1}", "pad", **{**pad_spec("surgePadPad2Mw", vol=0.07, pan=0.0, duck=0.4, sustain=1.6), "fx": [LPF, {"type": "reverb", "mix": 0.3}]}) for i in range(3)]
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の旋律と歌詞（G#短調の度数。oct=4 で 1 = G#4。サビは B長調で oct=3。書き出しの前に全体を 6半音下げる） =================
VERSE = ["R:1 1:0.5 1:0.5 3:0.5 1:0.5 5,:1", "7,:1 2:1.5 R:1.5",
         "R:1 6,:0.5 1:0.5 3:0.5 1:0.5 6,:1", "b2:2 R:2",
         "R:1 3:0.5 3:0.5 5:0.5 3:0.5 2:1", "7,:2 R:2",
         "R:1 6,:0.5 1:0.5 3:1 5:1", "#7,:2 R:2",
         "R:1 5:0.5 5:0.5 4:0.5 3:0.5 1:1", "2:2 R:2",
         "R:1 6,:0.5 1:0.5 3:1 1:1", "b2:2 R:2",
         "R:1 1:0.5 3:0.5 5:0.5 3:0.5 1:1", "2:1 7,:1.5 R:1.5",
         "R:1 3:0.5 3:0.5 2:1 1:1", "#7,:2 R:2"]
V1 = "めざましとめて/ふとんのなか/げつようびの/あさがきた/ゆううつがね/かおをだす/あとごふんだけ/ねかせてよ"
V2 = "はぶらしくわえ/かがみのまえ/ねぐせのかみ/わらえない/でもふしぎね/わらってみた/そしたらすこし/かるくなる"
BM = ["3:1 5:0.5 6:0.5 5:1 3:1", "2:1 4:0.5 7:0.5 4:1.5 R:0.5", "5:1 7:0.5 1':0.5 7:1 5:1", "1':2 R:1 5:0.5 7:0.5",
      "6:1 1':0.5 6:0.5 4:1 6:1", "7:1 2':0.5 7:0.5 4:1.5 R:0.5", "1':1 7:1 6:1 5:1", "7:2 R:2"]
P1 = "ぼたんかけちがえた/ためいきつく/でもそのためいきをほら/けしてみる"
P2 = "まどをあけてみたら/あさのひかり/あたらしいいちにちがね/はじまるよ"
CH1 = ["R:0.5 5':0.5 5':0.5 5':0.5 1'':2", "7':1 6':0.5 5':0.5 3':2", "R:0.5 5':0.5 7':0.5 1'':0.5 7':1 6':1", "6':3 R:1",
       "R:0.5 3':0.5 3':0.5 3':0.5 6':1 5':1", "4':0.5 3':0.5 1':1 5':1.5 R:0.5", "6':1 1'':1 7':1 6':1", "7':3 R:1"]
CH1b = [CH1[0], "7':1 6':0.5 5':0.5 3':1 5':1", "R:0.5 #5':0.5 #5':0.5 #5':0.5 1'':2", "6':1.5 5':0.5 4':2",
        "R:0.5 6':0.5 6':0.5 6':0.5 1'':1 6':1", "7':1 #5':1 3':1.5 R:0.5", "6':2 5':1 3':1", "5':2 R:2"]
CH2 = CH1[:6] + ["6':0.5 7':0.5 1'':1 7':1 5':1", "6':2 R:2"]
CH2b = CH1b[:6] + ["6':1 1'':1 7':1 6':1", "5':4"]
TAGL = ["R:0.5 5':0.5 5':0.5 5':0.5 1'':1 7':1", "7':1 5':1 2':1.5 R:0.5", "7':1 5':1 3':2", "6':3 R:1",
        "R:0.5 3':0.5 3':0.5 3':0.5 6':1 5':1", "5':1 7':1 1'':2", "1'':4", "R:4"]
C1 = "げつようびりせっと/すきっぷしよう/ゆううつをうわがき/かけだそう/ひとつずつすすめば/そらもあおいね/こころのぼたんを/おしてく"
C2 = "げつようびりせっと/すきっぷしよう/ゆううつをうわがき/かけだしたら/ひとつずつすすめば/そらもあおいね/こころのぼたんを/おしてゆく"
CL = C1 + "/げつようびりせっと/いこうよ/さあいってきますよと"
DR = ["3:2 5:1 6:1", "5:3 R:1", "4:2 6:1 4:1", "3:3 R:1", "6:1 5:1 3:1 5:1", "7:2 5:1 R:1", "6:1 4:1 6:1 1':1", "#7:3 R:1",
      "b2':2 1':1 6:1", "7:2 5:1 R:1", "2':1 7:1 4:1 7:1", "1':2 6:1 R:1", "1':1 3':1 6:2", "7:1 2':1 3':1 R:1", "3':1 1':1 6:2", "7:2 R:2"]
DRV = "ゆめでね/ちいさな/わたしがいて/いってくれた/だいじょうぶ/まいにちがね/あたらしいの/はじまり"
OV = ["3:2 5:2", "4:2 7:2", "5:2 7:1 1':1", "1':3 R:1", "6:2 1':2", "7:2 2':2", "3':2 2':1 1':1", "#7:3 R:1"]
OVV = "うわがきしてゆく/わたしのきもちを"
OUTL = ["3':2 5':2", "7':2 5':2", "5':1 3':1 2':2", "1':3 R:1", "3':1 5':1 6':1 5':1", "7':4", "R:4", "R:4"]
LY = Lyrics(S)
def put(name, key, lines, text, low=True, o=4):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for i, (b, m) in enumerate(zip(bars, mel)): V.bar(b, m, low=low if not callable(low) else low(i))
    LY.flow(bars, mel, text, name)
put("ぼやき", K, VERSE, V1)
if VOCAL: put("ぼやき2", K, VERSE, V2)
else:
    for i, b in enumerate(S.sc("ぼやき2")):
        line = K.mel(VERSE[i], oct=4)
        if i < 8: PNM.bar(b, shift_oct(line, 1))                    # BGM: 2回目の前半は、ハウスのピアノが歌を受け取る
        else: V.bar(b, line)
put("着がえる", K, BM, P1); put("着がえる2", K, BM, P2)
put("スキップ", KB, CH1 + CH1b, C1, o=3); put("スキップ2", KB, CH2 + CH2b, C2, o=3)
put("リセット", KC, CH1 + CH1b + TAGL, CL)                          # C は B より半音上（C4 が B3 の半音上）なので oct=4
put("ベッドの中2", K, DR, DRV, low=lambda i: i >= 8)
put("上書き中", K, OV, OVV, low=lambda i: i >= 4)
put("スキップで出かける", KC, OUTL, "すきになれるかも/げつようび")


# ================= ハウスのピアノ・ベル =================
# 起き上がる・駅まで・跳ねる道: ハウスのピアノの和音の句（M7・m7 の裏打ち）
HOUSE = ["X:0.5 R:0.25 X:0.5 R:0.25 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5", "R:0.5 X:0.75 X:0.75 R:0.5 X:0.5 X:1",
         "X:0.75 X:0.75 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5", "R:0.25 X:0.5 X:0.5 X:0.75 R:0.5 X:0.5 R:0.5 X:0.5"]
# 駅まで: ピアノとベルが2小節ずつ掛け合う旋律
STN = ["1':0.5 7:0.5 5:0.5 3:0.5 5:0.5 1':0.5 3':1", "2':0.5 1':0.5 7:0.5 5:0.5 7:1 2':1", "5':0.5 4':0.5 3':0.5 1':0.5 3':1 5':1", "6':2 5':1 3':1",
       "3':0.25 4':0.25 5':0.25 3':0.25 1':0.5 3':0.5 5':1 3':1", "4':0.5 5':0.5 7':0.5 5':0.5 4':1 2':1", "1':0.5 3':0.5 5':0.5 1'':0.5 7':1 5':1", "1'':4"]
for i, b in enumerate(S.sc("駅まで")):
    if (i // 2) % 2 == 0: PNM.bar(b, KB.mel(STN[i % 8], oct=3))
    else: BELL.bar(b, KB.mel(STN[i % 8], oct=4))
# 合いの手（Aメロの4小節目・サビの4小節目にベル）
for name in ("ぼやき", "ぼやき2"):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3 and not (name == "ぼやき2" and i < 8): BELL.bar(b, K.mel("R:2.5 5':0.25 4':0.25 3':0.5 1':0.5", oct=4))
for name, kk in (("スキップ", KB), ("スキップ2", KB), ("リセット", KC)):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3: BELL.bar(b, kk.mel("R:3 5:0.25 3:0.25 2:0.25 5:0.25", oct=5 if kk is KB else 6))

# ================= 伴奏 =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    v = voice(ch, 64, 4)
    r = low(ch, "E1")
    pat = None
    if n in ("起き上がる", "跳ねる道") or (n == "駅まで"): pat = HOUSE[i % 4]
    elif n == "ベッドの中": pat = "X:4" if i % 2 == 0 else "X:2 X:2"
    elif n in ("ぼやき", "ぼやき2"):
        if not (n == "ぼやき2" and i < 8): pat = "R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5" if i >= 4 else None
    elif n.startswith("着がえる"): pat = "X:1.5 X:1 X:1.5" if i < L - 1 else "X:1 R:3"
    elif n in ("スキップ", "スキップ2", "リセット"): pat = HOUSE[i % 4] if i % 8 < 4 else "R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5"
    elif n == "ベッドの中2": pat = "X:4" if i < 8 else "X:2 X:2"
    elif n == "スキップで出かける": pat = HOUSE[i % 4] if i < 6 else None
    if pat:
        for j in range(4): PN[j].bar(b, pat.replace("X", nm(v[j])))
    if n == "上書き中":
        vv = voice(ch, 64, 3)
        for j in range(3): PNF[j].bar(b, HOUSE[i % 4].replace("X", nm(vv[j])))
    # パッド
    vp = voice(ch, 60, 3)
    if n in ("ベッドの中", "着がえる", "着がえる2", "スキップ", "スキップ2", "リセット", "ベッドの中2") and not (n.startswith("着がえる") and i == L - 1):
        for j in range(3): PAD[j].bar(b, f"{nm(vp[j])}:4")
    if n == "上書き中":
        for j in range(3): PADF[j].bar(b, f"{nm(vp[j])}:4")
    # ベース（ハウスの裏・根音に沿わせる）
    if n == "ベッドの中": BASS.bar(b, f"{nm(r)}:4" if i >= 4 else "R:4")
    elif n == "起き上がる": BASS.bar(b, bass_line(S, b, "house") if i < 8 else bass_line(S, b, "oct8"))
    elif n in ("ぼやき", "ぼやき2"): BASS.bar(b, bass_line(S, b, "house" if i < 8 else "push"))
    elif n.startswith("着がえる"): BASS.bar(b, bass_line(S, b, "root8") if i < L - 1 else f"{nm(r)}:1 R:3")
    elif n in ("スキップ", "スキップ2", "リセット"): BASS.bar(b, bass_line(S, b, "oct8"))
    elif n in ("駅まで", "跳ねる道"): BASS.bar(b, bass_line(S, b, "house" if i % 8 < 4 else "disco"))
    elif n == "ベッドの中2": BASS.bar(b, bass_line(S, b, "long") if i < 8 else bass_line(S, b, "half"))
    elif n == "上書き中": BASS.bar(b, bass_line(S, b, "long") if i < 4 else bass_line(S, b, "house"))
    elif n == "スキップで出かける": BASS.bar(b, bass_line(S, b, "house") if i < 6 else "R:4")

# ため息（2026-10-25: 04 と同じ目覚ましで始めないよう、電子ピアノの下がる2音と和音に変えた）
ALARM.bar(S.sc("目覚ましの鳴りやみ")[0], "D#5:1.5 B4:2.5")
ALARM.bar(S.sc("目覚ましの鳴りやみ")[1], "G#3:4")
# 終わり: 軽いスタブで切る
b_end = S.sc("スキップで出かける")[6]
for j, x in enumerate(voice("Cmaj9", 66, 4)): PN[j].bar(b_end, f"{nm(x)}:0.5' R:3.5")
BASS.bar(b_end, "C2:0.5 R:3.5")
BELL.bar(b_end, "G5:0.5 R:3.5")
# 効果音
riser(FX, S.sc("スキップ")[0], 4, "C4"); riser(FX, S.sc("リセット")[0], 16, "D4")
cym_swell(CYM, S.sc("起き上がる")[0], 2, "C4"); cym_swell(CYM, S.sc("スキップ2")[0], 2, "C4"); cym_swell(CYM, S.sc("跳ねる道")[0], 2, "C4")
FX.bar(S.sc("ベッドの中2")[0], "E4:4")             # ダウンリフター（夢に落ちる）

# ================= ドラム（電子のドラム） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "目覚ましの鳴りやみ": D.set(b, "." * 16, "." * 16, "." * 16)
    elif n == "ベッドの中":                       # Half feel（布団の中）
        vgroove(D, b, "half", ghosts=0.3, seed=b, h="x...x...x...x..." if i >= 2 else "................")
        if i < 2: D.set(b, "X.........X.....", "." * 16, "." * 16)
        if last: put_fill(D, b, "build")
    elif n in ("起き上がる", "駅まで", "跳ねる道"):
        vgroove(D, b, "four" if i % 8 < 4 else "four16", ghosts=0.25, seed=b)
        if i == 0: crash(D, b)
        if i % 8 == 7 or last: put_fill(D, b, "snare16" if last else "small")
    elif n in ("ぼやき", "ぼやき2"):
        vgroove(D, b, "four" if i < 8 else "disco", ghosts=0.3, seed=b)
        if i == 0: crash(D, b)
        if i == 7: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
    elif n.startswith("着がえる"):
        vgroove(D, b, "twostep" if i < 4 else "four16", ghosts=0.3, seed=b)
        if i == 4: crash(D, b, "G2")
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 1); D.cym(b, "C2:1")
    elif n in ("スキップ", "スキップ2", "リセット"):
        vgroove(D, b, "four16", ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16" if i % 16 == 7 else "tomdown")
        if last: put_fill(D, b, "tomdown" if n != "リセット" else "snare16")
    elif n == "ベッドの中2":                      # Half feel（夢の中）
        if i < 4: D.set(b, "X.........X.....", "." * 16, "x...x...x...x...")
        else: vgroove(D, b, "half", ghosts=0.4, seed=b, h="x.x.x.x.x.x.x.x." if i >= 8 else "x...x...x...x...")
        if i == 8: crash(D, b, "B2")
        if last: put_fill(D, b, "lift")
    elif n == "上書き中":
        D.set(b, "X...X...X...X...", "." * 16, "." * 16 if i < 4 else "..x...x...x...x.")
        if i == 6: put_fill(D, b, "build")
        if last: D.set(b, "X...X...X.......", "xxxxXXXXXXXX....", "." * 16)
    elif n == "スキップで出かける":
        if i < 6: vgroove(D, b, "four", ghosts=0.25, seed=b)
        if i == 0: crash(D, b)
        if i == 5: put_fill(D, b, "small")
        if i == 6: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16)
        if i == 7: D.set(b, "." * 16, "." * 16, "." * 16)

# 止め・1拍の完全な無音
SIL.add(S.sc("着がえる")[-1], 1, 4)
SIL.add(S.sc("上書き中")[-1], 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の12。エレクトロハウス。D短調（サビは F長調）・176、最後のサビは +1（F#）。"
          "憂うつな月曜の朝を、スキップで上書きしていく。電子ピアノのため息で始まり、Half feel のベッドの中、4つ打ちで起き上がる、低めにぼやく Aメロ、止めのある Bメロ、"
          "オクターブ上へ開くサビ、ハウスのピアノとベルの掛け合い、夢の中の Cメロ、こもった上書きと1拍の無音、+1 の最後のサビ。Surge の音と生のピアノ。自作")
# 季節の音（2026-10-25 人間「季節を感じれる様な音も欲しい」）
season(S, 0, "小鳥", S.beats * 4, vol=0.06)
S.flags += " --space hall --space-wet 0.14"
teto(S, LY, V, transpose=-6, special={"リセット": 0.55, "ベッドの中2": -0.5, "上書き中": -0.1, "スキップで出かける": 0.1})
