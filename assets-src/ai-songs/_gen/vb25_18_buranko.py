# vb25 18「ブランコ・リバース」Swing Reverse（仮）— J-POP（3拍子）。D♭長調・144・3/4（Bメロは 6/8 のノリ）。最後のサビは +1（D長調）
# 2026-10-25 作り直し: 物語を人の気持ちの話に（大人になって、帰り道の公園のブランコで子どものころを思い出す）、歌を人が歌える旋律（8分と4分）に、テトの歌の版を足した。
#   テトの声に合うよう、曲全体を A♭長調から 7半音下げて D♭長調にした（書くのは A♭長調の度数のまま、書き出しの前に下げる）。
# 物語: 仕事の帰り道、だれもいない夕方の公園。子どものころ好きだったブランコに腰かけて、思いきりこぐ。ひと振りごとに時間が巻きもどって、
#   ちいさな自分が手をふっている。ブランコが止まると、大人の自分。どろだらけで泣いて笑った日の「風の強さ」を思い出して、もう一度こぐ。
#   いちばん高い所で、ちいさな自分の手をつかまえて「だいじょうぶだよ」と言う。ふわりと着地して「ただいま」。
# 場面と強さ: オルゴール（グロッケンだけ・小）→ 夕方の公園（アコーディオンのワルツ）→ こぎ始め（Aメロ・語る）
#   → 勢いをつける（6/8 の Bメロ・止め）→ 空へ（サビ・強）→ 風の中（アコーディオンのソロ）→ もう一度こぐ（2番。BGM は前半ピアノが歌を受け取る）
#   → 勢いをつける2 → いちばん高く（サビ）→ 風を切る（短い呼びかけ）→ 止まったブランコ（静けさ・1拍の無音）
#   → 子どものころ（Cメロ）→ もっと高く（+1・最大）→ 着地（ブランコのきしみと1音）
# 旋律の性格: ワルツの揺れ。Aメロは小節の2拍目から入る8分、サビは4分で大きく上下する（6度の跳躍）。最高音 F5（+1 のサビは F#5）。
# 派手な展開: Bメロ 6/8・最後のサビ +1・1拍の完全な無音・止め2回（Bメロの終わり）
# 定番以外のコード: Caug（増三和音）→ Fm7・Ebm7–Ab7（IV への副属和音）・C7（vi への副属和音）・D♭m6（同主短調の iv）・Ddim7・E7（新しい調の V7 で +1 へ）
from vb25_lib import *

S = Song("18", "buranko", "ブランコ・リバース（仮）", "Swing Reverse", 144, 3, "Ab", "major", "J-POP（3拍子・ボカロ）")
# 2026-10-26 人間「ドラムの音がデジタルすぎるのも原因かもね」: 07・18 で試すと、素直な生ドラム（Naked Drums）で点数が +0.3（07: 7.12→7.44、18: 7.22→7.51）
#   → 太鼓ごとに作り込んだ crocell-punch をやめて、Naked Drums に（太鼓の音量などの設定は今までと同じ）
S.kit = "naked-x"   # 前: "crocell-punch"
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags + " --piano salamander"
S.extra.update({"tone": "rock"})
K = S.key                    # A♭長調
KA = Key("A", "major")       # 最後のサビ（+1）
dbl = lambda xs: [x for c in xs for x in (c, c)]

A_CH = dbl(["Abmaj7", "Cm7", "Dbmaj7", "Eb7sus4"])
B_CH = ["Fm7", "Ebm7", "Ab7", "Dbmaj7", "Bbm7", "C7", "Fm7", "Eb7"]
CH = dbl(["Dbmaj7", "Eb", "Cm7", "Fm7"]) + ["Bbm7", "Eb7", "Ab", "Caug", "Fm7", "Dbm6", "Ab/Eb", "Eb7"]
STOP = dbl(["Dbmaj7", "Cm7", "Bbm7", "Ab/C", "Dbmaj7", "Ddim7", "Eb7sus4", "Eb7"])
CHILD = dbl(["Fm", "Fm/Eb", "Dbmaj7", "C7", "Bbm7", "Eb7", "Abmaj7", "E7"])
LAST = [tr_chord(c, 1) for c in CH] + [tr_chord(c, 1) for c in CH[:-1]] + ["A"]

S.scene("オルゴール", 8, "intro", CH[:8])
S.scene("夕方の公園", 8, "interlude", A_CH)
S.scene("こぎ始め", 16, "verse", A_CH)
S.scene("勢いをつける", 8, "pre", B_CH)
S.scene("空へ", 16, "chorus", CH)
S.scene("風の中", 16, "solo", A_CH)
S.scene("もう一度こぐ", 16, "verse", A_CH)
S.scene("勢いをつける2", 8, "pre", B_CH)
S.scene("いちばん高く", 16, "chorus", CH)
S.scene("風を切る", 8, "interlude", ["Dbmaj7", "Eb", "Fm7", "Ab/Eb", "Dbmaj7", "Eb", "Ab", "Ab"])
S.scene("止まったブランコ", 16, "break", STOP)
S.scene("子どものころ", 16, "bridge", CHILD)
S.scene("もっと高く", 32, "chorus", LAST)
S.scene("着地", 12, "outro", ["Dmaj7", "E", "C#m7", "F#m7", "Dmaj7", "E", "A", "A", "A", "A", "A", "A"])

V = Voice(S, vol=0.22, delay=1.0, patch="reedOrgan", low=True)   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
ACS = dict(volume=0.12, pan=-0.3, reverb=0.28, phrase=6, fx=[{"type": "eq", "low": -4, "mid": 2, "midHz": 2000, "high": 0.5}])
AC = S.track("アコーディオン（旋律）", "accordion", **ACS)
AC2 = [S.track(f"アコーディオン（和音{i + 1}）", "accordion", **ACS) for i in range(2)]
PNS = piano_spec(0.12, 0.25)
PN = S.track("ピアノ（右手）", "piano", **PNS)
PNL = S.track("ピアノ（左手）", "piano", **PNS)
PNM = S.track("ピアノ（歌の受け渡し）", "piano", **PNS)
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", **strings_spec(0.08, 0.5)) for i in range(3)]
MB = S.track("オルゴール風のグロッケン", "glockenspiel", patch="glockenspiel", volume=0.1, pan=0.1, reverb=0.4)
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.2))
CREAK = S.track("ブランコのきしみ（弦をこする音）", "guitar", patch="guitarFx", volume=0.06, pan=-0.2, reverb=0.3, modulate=False)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)
# 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ 足したパート:
#   ・ブランコが風を切る「シュッ」（左右にゆれる2本。往復ごとに左と右から。効果音なので小さく）
#   ・最後のサビにだけ足す新しい音: バイオリンの高い対旋律（柔らかく力強く、透き通るように。歌より小さく、ストリングスの右 0.5 とアコーディオンの左 0.3 の間）
SW = [S.track(f"ブランコの風（{['左', '右'][i]}）", "pad", patch="fxRiser", volume=0.06, pan=[-0.6, 0.6][i], reverb=0.35) for i in range(2)]
SWQ = S.track("ブランコの風（着地・小さく）", "pad", patch="fxRiser", volume=0.04, pan=0.3, reverb=0.45)
VLN = S.track("バイオリン（最後のサビの対旋律）", "fiddle", patch="violin", volume=0.08, pan=-0.12, reverb=0.42, gainDb=1, bright=-0.3, attack=0.08, release=0.5)
TR = -7                                   # 書き出しの前に全体を下げる半音（teto の transpose と同じ）

# ================= 歌の旋律と歌詞（A♭長調の度数。oct=4 で 1 = A♭4。書き出しの前に全体を 7半音下げる） =================
VERSE = ["R:1 3:0.5 3:0.5 2:0.5 1:0.5", "2:1 7,:1.5 R:0.5", "R:1 3:0.5 4:0.5 5:0.5 6:0.5", "5:1.5 R:1.5",
         "R:1 6:0.5 6:0.5 5:0.5 4:0.5", "3:1 1:1.5 R:0.5", "R:1 2:0.5 3:0.5 4:0.5 3:0.5", "2:2 R:1",
         "R:1 3:0.5 3:0.5 2:0.5 1:0.5", "2:1 1:1.5 R:0.5", "R:1 1:0.5 2:0.5 3:0.5 5:0.5", "7:1.5 R:1.5",
         "R:1 1':0.5 7:0.5 6:0.5 5:0.5", "4:1 3:1.5 R:0.5", "R:1 2:0.5 3:0.5 5:0.5 6:0.5", "5:2 R:1"]
V1 = "かえりみちに/よりみちを/だれもいない/こうえんで/ちいさなくつ/すりへらす/ぶらんこへと/こしかけた"
V2 = "ひざをのばし/こぎだせば/かぜのにおい/むかしいろ/ひとふりごと/まきもどる/さかさまへと/とんでゆく"
# 6/8 のノリの Bメロ（8分3つ＋付点4分）
VB = ["1:0.5 3:0.5 5:0.5 6:1.5", "5:0.5 b7:0.5 5:0.5 4:1 R:0.5", "3:0.5 5:0.5 b7:0.5 1':1.5", "1':0.5 6:0.5 4:0.5 3:1 R:0.5",
      "2:0.5 4:0.5 6:0.5 1':1.5", "3:0.5 #5:0.5 7:0.5 2':1 R:0.5", "6:0.5 1':0.5 2':0.5 1':1.5", "7:1 R:2"]
P1 = "くさりにぎりしめ/おもいきりけったら/そらがちかくなる/もっとたかく"
P2 = "ゆうひがゆれてる/あしもとのかげも/ながくのびてゆく/もっとたかく"
# サビ: 4分で大きく上下する（「そらへ そらへ」）
VC = ["4:1 6:1 1':1", "3':1.5 2':0.5 1':0.5 R:0.5", "2':1 7:1 5:1", "6:1.5 5:1 R:0.5",
      "3:1 5:1 7:1", "2':1.5 1':0.5 7:0.5 R:0.5", "1':1 6:1 5:1", "6:2 R:1",
      "2:0.5 4:0.5 6:0.5 1':0.5 2':1", "2':1 7:1 5:0.5 R:0.5", "1':1 5:1 3':1", "3':1 #5:1.5 R:0.5",
      "1':1 6:1 3':1", "2':1.5 b6:0.5 1':1", "3':1 2':1 1':1", "2':2 R:1"]
C1 = "そらへそらへ/かぜをきって/ゆうやけぞら/あのひへ/あのころのぼくが/てをふってる/あとすこしでとどくよ"
C2 = "そらへそらへ/もっとたかく/ほしがひかる/あのこえ/ごはんだよってよぶ/おかあさん/もうすこしだけあそぶ"
VCL = VC + VC[:12] + ["1':1 6:1 3':1", "2':1.5 b6:0.5 1':1", "3':1 2':1 7:1", "1':3"]
CL = ("そらへそらへ/もっとたかく/いまのぼくで/あのひへ/ちいさなぼくのて/つかまえた/だいじょうぶだよっていった"
      "/そらへそらへ/かぜをきって/ゆうやけぞら/こえてく/おとなのぼくだって/まだとべる/またあしたもこごうね")
VWIND = ["R:1 5:1 1':1", "3':2 R:1", "R:1 5:1 1':1", "1':2 R:1", "6:1 6:1 1':1", "3':1 2':1 7:1", "1':3", "R:3"]
VSTOP = ["4:2 6:1", "1':2 R:1", "7:2 5:1", "3:2 R:1", "2:1 4:1 6:1", "5:2 R:1", "3:1.5 5:1.5", "1:2 R:1",
         "4:1 6:1 1':1", "3':2 R:1", "#4:1.5 6:1.5", "1':2 R:1", "5:1 1':1 2':1", "1':2 R:1", "7:1 2':1 5:1", "5:1 R:2"]
VK = ["R:1 6,:0.5 1:0.5 3:0.5 6:0.5", "5:1 6:1.5 R:0.5", "R:1 1:0.5 3:0.5 5:0.5 6:0.5", "1':1 6:1.5 R:0.5",
      "R:1 4:0.5 6:0.5 1':0.5 3':0.5", "2':1 1':1.5 R:0.5", "R:1 3:0.5 #5:0.5 7:0.5 2':0.5", "7:1 #5:1.5 R:0.5",
      "R:1 2:0.5 4:0.5 6:0.5 1':0.5", "2':1 1':1.5 R:0.5", "R:1 5:0.5 7:0.5 2':0.5 3':0.5", "2':2 R:1",
      "5:1 1':1 3':1", "2':1.5 1':1.5", "#5:1 1':1 #2':1", "#2':1 R:2"]
VOUT = ["3':1.5 2':1.5", "1':2 R:1", "7:1.5 5:1.5", "6:2 R:1", "4:1 6:1 1':1", "2':3", "1':3", "R:3"]
LY = Lyrics(S)
def put(name, key, lines, text, low=True):
    bars = S.sc(name); mel = [key.mel(x, oct=4) for x in lines]
    for i, (b, m) in enumerate(zip(bars, mel)): V.bar(b, m, low=low if not callable(low) else low(i))
    LY.flow(bars[:len(mel)], mel, text, name)
put("こぎ始め", K, VERSE, V1)
if VOCAL: put("もう一度こぐ", K, VERSE, V2)
else:
    for i, b in enumerate(S.sc("もう一度こぐ")):
        if i < 8: PNM.bar(b, shift_oct(K.mel(VERSE[i], oct=4), 1))   # BGM: 前半はピアノが歌を受け取る（1オクターブ上）
        else: V.bar(b, K.mel(VERSE[i], oct=4))
put("勢いをつける", K, VB, P1); put("勢いをつける2", K, VB, P2)
put("空へ", K, VC, C1); put("いちばん高く", K, VC, C2)
put("風を切る", K, VWIND, "そらへ/かぜへ/どこまでもとべ")
put("止まったブランコ", K, VSTOP, "とまった/しずか/ゆうなぎ/ひとり/おとなの/ぼくに/ちいさな/あしあと", low=False)
put("子どものころ", K, VK, "どろだらけで/ないてわらった/ひざのきずも/くんしょうだよ/せがのびたら/わすれてた/このかぜのつよさを")
put("もっと高く", KA, VCL, CL)
put("着地", KA, VOUT, "ふわり/おりて/ただいまって", low=lambda i: i < 4)

# ================= オルゴール（グロッケン） =================
# 2026-10-26 人間「後半に行くにつれて曲の始まり方似てない？」→ オルゴールのぜんまいが巻かれて鳴り出す:
#   1小節目は、ぜんまいを巻く「ジジッ、ジジッ」（ピックで弦をこする短い音）のあと、3拍目でオルゴールが1音だけ鳴り出し、2小節目から旋律
for i, b in enumerate(S.sc("オルゴール")): MB.bar(b, K.mel(VC[i], oct=5) if i else K.mel("R:2 1':1", oct=5))
for i, b in enumerate(S.sc("止まったブランコ")):
    if i % 4 == 0: MB.bar(b, K.mel(["5:1 1':1 3':1", "4:1 1':1 4':1", "3:1 5:1 1':1", "6:1 1':1 4':1"][i // 4], oct=5))
MB.bar(S.sc("着地")[9], KA.mel("1':3", oct=5))                # 最後の1音

# ================= アコーディオン（ワルツの和音・風の中のソロ） =================
SOLO = ["5:0.5 3:0.5 1:0.5 3:0.5 5:1", "1':1.5 7:0.5 5:1", "7:0.5 5:0.5 3:0.5 5:0.5 7:1", "2':1.5 1':0.5 7:1",
        "6:0.5 4:0.5 1:0.5 4:0.5 6:1", "1':1 3':1 1':1", "2':0.5 1':0.5 7:0.5 5:0.5 4:1", "5:3",
        "5:0.25 6:0.25 5:0.25 3:0.25 1:0.5 3:0.5 5:1", "1':0.5 2':0.5 1':0.5 7:0.5 5:1", "7:0.25 1':0.25 7:0.25 5:0.25 3:0.5 5:0.5 7:1",
        "3':1.5 2':0.5 1':1", "6:0.25 1':0.25 6:0.25 4:0.25 1:0.5 4:0.5 6:1", "3':1 2':1 1':1", "2':0.5 1':0.5 7:0.5 5:0.5 2':1", "1':1.5 R:1.5"]
for i, b in enumerate(S.sc("風の中")): AC.bar(b, K.mel(SOLO[i], oct=4))
for i, b in enumerate(S.sc("夕方の公園")): AC.bar(b, K.mel(SOLO[i], oct=4) if i < 7 else K.mel("5:1.5 R:1.5", oct=4))
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; v = voice(ch, 62, 2)
    if n in ("夕方の公園", "こぎ始め", "風の中", "もう一度こぐ", "子どものころ", "着地") or (n in ("空へ", "いちばん高く", "もっと高く") and i >= 8):
        if n == "着地" and i >= 8: continue
        for j in range(2): AC2[j].bar(b, f"R:1 {nm(v[j])}:1 {nm(v[j])}:1")
    elif n.startswith("勢いを"):
        for j in range(2): AC2[j].bar(b, f"R:0.5 {nm(v[j])}:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5 {nm(v[j])}:0.5" if i < 7 else f"{nm(v[j])}:1 R:2")

# 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ 合いの手: Aメロの句の終わり（歌が伸ばして休む所）に短い返事。
#   1番はオルゴール（グロッケン）、2番はアコーディオンが受け取る（楽器の受け渡しで 2番を少し変える）
ANS = {3: "R:1.5 7:0.5 5:0.5 3:0.5", 7: "R:2 5:0.5 1':0.5", 11: "R:1.5 5:0.5 3:0.5 7,:0.5"}
for i, b in enumerate(S.sc("こぎ始め")):
    if i in ANS: MB.bar(b, K.mel(ANS[i], oct=5))
for i, b in enumerate(S.sc("もう一度こぐ")):
    if i in ANS: AC.bar(b, K.mel(ANS[i], oct=4))

# ================= ピアノ（サビは8分の分散、Aメロは左手の低音） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; t = tones(ch, "Ab3", "Ab5"); r = low(ch, "C2")
    if n in ("空へ", "いちばん高く", "もっと高く", "子どものころ", "風を切る"):
        PN.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 4, 3, 2, 1)))
        PNL.bar(b, f"{nm(r)}:1.5 {nm(r + 12)}:1.5")
    elif n in ("こぎ始め", "勢いをつける", "勢いをつける2") or (n == "もう一度こぐ" and i >= 8):
        PNL.bar(b, f"{nm(r)}:3")
        if n.startswith("勢いを"): PN.bar(b, f"{nm(t[1 % len(t)])}:1.5 {nm(t[3 % len(t)])}:1.5" if i < 7 else f"{nm(t[1])}:1 R:2")
    elif n == "止まったブランコ":
        if i % 2 == 0: PNL.bar(b, f"{nm(r)}:6")
    elif n == "着地" and i < 8:
        PN.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 4, 3, 2, 1)) if i < 4 else f"{nm(t[2])}:3")
        PNL.bar(b, f"{nm(r)}:3")

# ================= ストリングス =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n in ("空へ", "いちばん高く", "もっと高く", "子どものころ", "止まったブランコ", "風の中") or (n == "着地" and i < 8):
        if n == "止まったブランコ" and i < 8: continue
        v = voice(S.chords[b], 67, 3)
        for j in range(3): STR[j].bar(b, f"{nm(v[j])}:3")

# ================= ベース（ワルツ。歌うベース） =================
# 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ 3拍子の歌うベースに書きなおした（共通の sing_bass は4拍子用なので、曲の中で書く）。
#   前は E1 から数えて書いていたので、書き出しで 7半音下がると A0〜D#1（4弦のベースより低い）になっていた。B1 から数えて、下げたあと E1〜E3 に収める。
#   waltz＝1拍目と3拍目／long＝のばす／step＝和音を上っていく／lead＝次の和音へ寄っていく（歌が伸ばす小節で動く）／
#   six・sixrun＝6/8 の付点4分2つと、後ろを駆ける形／ch＝サビの形（前のまま）
BL = nm(28 - TR)
def b3(b, style):
    ch = S.chords[b].split("|")[0]; r = low(ch, BL)
    nx = low(S.chords[b + 1].split("|")[0], BL) if b + 1 < S.nb else r
    if nx - r > 6: nx -= 12
    if r - nx > 6: nx += 12
    up = tones(ch, nm(r + 1), nm(r + 12)); c1 = up[0] if up else r + 4; c2 = up[1] if len(up) > 1 else r + 7
    o, f5 = r + 12, r + 7
    a = nx - 1 if nx > r else (nx + 1 if nx < r else f5)
    N = nm
    return {"waltz": f"{N(r)}:1! R:1 {N(f5)}:1", "long": f"{N(r)}:2 {N(o)}:1", "step": f"{N(r)}:1! {N(c1)}:1 {N(c2)}:1",
            "lead": f"{N(o)}:1 {N(f5)}:1 {N(a)}:1", "six": f"{N(r)}:1.5! {N(f5)}:1.5", "sixrun": f"{N(r)}:1.5! {N(f5)}:0.5 {N(o)}:0.5 {N(a)}:0.5",
            "ch": f"{N(r)}:1! {N(o)}:1 {N(f5)}:0.5 {N(a)}:0.5", "hold": f"{N(r)}:6", "end": f"{N(r)}:1! R:2"}[style]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n in ("オルゴール",): continue
    if n == "止まったブランコ":
        if i % 2 == 0: BASS.bar(b, b3(b, "hold"))
    elif n.startswith("勢いを"):
        BASS.bar(b, b3(b, "end") if i == 7 else b3(b, "six" if i % 2 == 0 else "sixrun"))
    elif n in ("空へ", "いちばん高く", "もっと高く", "風を切る") or (n == "子どものころ" and i >= 8):
        BASS.bar(b, b3(b, {1: "step", 3: "lead"}.get(i % 4, "ch")))
    elif n == "子どものころ":
        BASS.bar(b, b3(b, "long" if i % 2 == 0 else "lead"))
    elif n == "着地":
        if i < 8: BASS.bar(b, b3(b, "waltz"))
        elif i == 8: BASS.bar(b, b3(b, "hold"))
    elif n in ("こぎ始め", "もう一度こぐ") and i >= 8:
        BASS.bar(b, b3(b, "step" if i % 2 == 0 else "lead"))
    elif n == "もう一度こぐ":
        BASS.bar(b, b3(b, "waltz" if i % 2 == 0 else "lead"))
    elif n == "風の中":
        BASS.bar(b, b3(b, "waltz" if i % 2 == 0 else ("lead" if i % 4 == 3 else "long")))
    else:
        BASS.bar(b, b3(b, "waltz" if i % 2 == 0 else "long"))

# ブランコのきしみ（弦をこする長い音・短い音）
for i, b in enumerate(S.sc("オルゴール")):
    if i % 4 == 3: CREAK.bar(b, "R:1.5 E2:1.5")
CREAK.bar(S.sc("オルゴール")[0], "D2:0.25 D2:0.25 R:0.25 D2:0.25 D2:0.25 R:0.25 D#2:0.5 R:1")   # ぜんまい
for i, b in enumerate(S.sc("止まったブランコ")):
    if i in (0, 6, 12): CREAK.bar(b, "F2:1 R:2")
for i, b in enumerate(S.sc("着地")):
    if i in (8, 10): CREAK.bar(b, "E2:3" if i == 8 else "F2:1.5 R:1.5")

# ブランコが風を切る（物語の音）: 1往復＝2小節。風を切る・最後のサビの前半でゆれ、着地でだんだん小さく・まばらになる
# 2026-10-26 人間「見直すならより良いのにしないとね」→ 全員が鳴る最後のサビでは、白い雑音の「シュッ」が歌と弦のじゃまになりやすいので入れない（風を切る・着地だけ）
for name, bars in (("風を切る", range(8)),):
    for i in bars:
        SW[i % 2].bar(S.sc(name)[i], "A4:1 R:2")
for i in (0, 2, 5): SWQ.bar(S.sc("着地")[i], "A4:1 R:2")
# 最後のサビの対旋律（A長調の音名で書く。書き出しで 7半音下がる）。後半の16小節
VLM = ["F#6:3", "E6:1.5 D6:1.5", "B5:3", "G#5:1.5 B5:1.5", "E6:3", "G#6:1.5 E6:1.5", "C#6:3", "A5:1.5 C#6:1.5",
       "D6:3", "D6:1.5 B5:1.5", "C#6:3", "F6:3", "F#6:3", "F6:1.5 D6:1.5", "C#6:3", "A5:3"]
for i, b in enumerate(S.sc("もっと高く")[16:]): VLN.bar(b, VLM[i])

# 効果音
riser(FX, S.sc("空へ")[0], 3, "C4"); riser(FX, S.sc("いちばん高く")[0], 3, "C4"); riser(FX, S.sc("もっと高く")[0], 6, "D4")
cym_swell(CYM, S.sc("風の中")[0], 3, "C4"); cym_swell(CYM, S.sc("子どものころ")[0], 3, "E4")

# ================= ドラム（3拍子: 12文字のグリッド） =================
def tomfill3(b):
    D.S[b] = D.S[b][:6] + "......"; D.H[b] = D.H[b][:6] + "......"; D.K[b] = D.K[b][:6] + "X.....X..."[:6]
    D.tom(b, "R:1.5 C4:0.25 A3:0.25 F3:0.25 D3:0.25 A2:0.5!")


def roll3(b):
    D.S[b] = "....x.xxXXXX"; D.H[b] = "x.x........."


W = {"waltz": ("X...........", "....x...x...", "x.x.x.x.x.x."),
     "waltz2": ("X.......x...", "....X...X...", "x.x.x.x.x.x."),
     "waltzP": ("X...x.......", "....X...Xo..", "XxxxXxxxXxxx"),
     "six8": ("X.....X.....", "......X.....", "X.x.x.X.x.x."),
     "six8b": ("X.x...X.....", "......X...o.", "X.x.x.X.x.x."),
     "halfw": ("X...........", "........X...", "x...x...x...")}
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "オルゴール": continue
    if n == "夕方の公園":
        put_groove(D, b, W["waltz"], ghosts=0.3, seed=b, hat_vary=False)
        if i == 0: crash(D, b, "G2", 3)
        if last: roll3(b)
    elif n in ("こぎ始め", "もう一度こぐ"):
        put_groove(D, b, W["waltz"] if i < 8 else W["waltz2"], ghosts=0.4, seed=b, hat_vary=False)
        if n == "もう一度こぐ" and i < 8: D.cym(b, "D2:1 D2:1 D2:1"); D.H[b] = "." * 12      # ライド
        if i == 0: crash(D, b, "C2", 3)
        if i == 7: tomfill3(b)
        if last: roll3(b)
    elif n.startswith("勢いを"):
        put_groove(D, b, W["six8"] if i % 2 == 0 else W["six8b"], ghosts=0.3, seed=b, hat_vary=False)
        if i == 0: crash(D, b, "B2", 3)
        if i == 6: roll3(b)
        if last: halt(D, b, 1, 3, 12)
    elif n in ("空へ", "いちばん高く", "もっと高く"):
        put_groove(D, b, W["waltzP"] if i >= 8 else W["waltz2"], ghosts=0.35, seed=b, hat_vary=False)
        if n == "もっと高く" and 16 <= i < 24: D.cym(b, "D2:1 D2:1 D2:1"); D.H[b] = "." * 12
        if i % 8 == 0 and not (n == "もっと高く" and i == 16): crash(D, b, "C2" if i % 16 == 0 else "G2", 3)
        if i % 8 == 7 and not last: tomfill3(b)
        if last and n != "もっと高く": roll3(b)
    elif n == "風の中":
        put_groove(D, b, W["waltz2"], ghosts=0.4, seed=b, hat_vary=False)
        D.cym(b, ("B2:1 " if i == 0 else "D2:1 ") + "D2:1 D2:1"); D.H[b] = "." * 12
        if i % 8 == 7: tomfill3(b)
    elif n == "風を切る":
        put_groove(D, b, W["waltzP"], ghosts=0.3, seed=b, hat_vary=False)
        if i == 0: crash(D, b, "G2", 3)
        if i == 6: roll3(b)
        if last: D.set(b, "X...........", "X...........", "." * 12); crash(D, b, "C2", 6)
    elif n == "止まったブランコ":
        if i >= 8: put_groove(D, b, W["halfw"], ghosts=0.2, seed=b, hat_vary=False)
    elif n == "子どものころ":
        put_groove(D, b, W["halfw"] if i < 8 else W["waltz2"], ghosts=0.4, seed=b, hat_vary=False)
        if i == 8: crash(D, b, "G2", 3)
        if i >= 8: D.cym(b, "D2:1 D2:1 D2:1"); D.H[b] = "." * 12
        if i == 14: roll3(b)
        if last: halt(D, b, 1, 3, 12)
    elif n == "着地":
        if i < 8: put_groove(D, b, W["waltz"], ghosts=0.3, seed=b, hat_vary=False)
        if i == 0: crash(D, b, "C2", 3)
        if i == 7: D.set(b, "X...........", "X...........", "." * 12); crash(D, b, "C2", 6)

# 2026-10-26 人間「ドラム強弱、アクセント、余韻も上手く使ってね」→ 3拍子のドラムは共通の遊び（kick_vary・spice は4拍子用）が入らないので、
#   ここで小さく足す: 同じ形が続く句の4小節目は3拍目の裏で開いたハイハットと次の小節へのキックの食い、6小節目はスネアのゴースト。
#   Aメロの前半はスネアを弱く（x）、サビの句の頭（8小節ごと）は強く
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n not in ("こぎ始め", "もう一度こぐ", "空へ", "いちばん高く", "もっと高く", "風の中") or i == L - 1: continue
    kk, ss, hh = list(D.K[b]), list(D.S[b]), list(D.H[b])
    if i % 8 == 3:
        if kk[10] == ".": kk[10] = "x"
        if hh[10] in "xX": hh[10] = "O"
    if i % 8 == 5 and ss[7] == ".": ss[7] = "o"
    if n in ("空へ", "いちばん高く", "もっと高く") and i % 8 == 0: kk[0] = "X"; ss[4] = "X" if ss[4] != "." else ss[4]
    D.K[b], D.S[b], D.H[b] = "".join(kk), "".join(ss), "".join(hh)

# 止め: 勢いをつけるの最後（1拍だけ）・子どものころの最後（1拍だけ）。1拍の完全な無音: 止まったブランコの最後の拍
for name in ("勢いをつける", "勢いをつける2", "子どものころ"): SIL.add(S.sc(name)[-1], 1, 3)
SIL.add(S.sc("止まったブランコ")[-1], 2, 3)
SIL.apply()
# 止めのあと: シンバルの鳴りを止めずに伸ばす（止めの消去のあとで、止めの小節の頭に長いクラッシュを置き直す）
for name in ("勢いをつける", "勢いをつける2", "子どものころ"):
    b = S.sc(name)[-1]
    D.C.ev = [e for e in D.C.ev if abs(e[0] - b * S.beats) > 1e-6]; D.cym(b, "C2:3")
# 書き出しの前の移調（−7半音）は、ブランコのきしみ（guitarFx の鍵盤＝こすり方の種類）を E2・F2 から A1・B♭1（種類の外）へずらしていた。先に +7 しておく
def keep_key(tracks, T):
    for t in tracks:
        t.ev = [(st, L, nm(midi(x.split(":")[0]) + T) + ":" + x.split(":", 1)[1]) for st, L, x in t.ev]
keep_key([CREAK], -TR)

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の18。J-POP（3拍子）。D♭長調・144・3/4（Bメロは 6/8 のノリ）・最後のサビ +1（D）。"
          "大人になって、帰り道の公園のブランコで子どものころを思い出す。オルゴール風のグロッケンで始まり、アコーディオンのワルツ、8分で語る Aメロ、"
          "6/8 のノリで勢いをつける Bメロと止め、大きな跳躍のサビ、アコーディオンのソロ、止まったブランコ（1拍の無音）、子どものころの Cメロ、"
          "+1 のいちばん高いサビ、最後はブランコのきしみと1音。自作")
# 季節の音（2026-10-25 人間「季節を感じれる様な音も欲しい」）
season(S, S.nb - 6, "夕方の蝉", S.beats * 6, vol=0.07)
S.no_depth = True
teto(S, LY, V, transpose=-7, special={"もっと高く": 0.55, "止まったブランコ": -0.5, "子どものころ": 0.0, "風を切る": 0.25, "着地": -0.35})
