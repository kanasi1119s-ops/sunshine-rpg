# vb25 17「ハッピーエンド前線」Happy-End Front（仮）— J-POP（疾走）。F#長調・180・4/4。最後のサビは +2（G#長調）
# 2026-10-25 作り直し: 物語を人の気持ちの話に（遠くの町へ引っ越した友だちに、元気を届けたい）、歌を人が歌える旋律（8分と4分）に、テトの歌の版を足した。
#   テトの声に合うよう、曲全体を D長調から 8半音下げて F#長調にした（書くのは D長調の度数のまま、書き出しの前に下げる）。
# 物語: けさの天気予報で聞いた「ハッピーエンド前線」。南の島から北へ上がって、通った町から晴れていく。北の果ての町へ引っ越して2年の君は、
#   電話の声がさみしそうだった。ぼくにできることは、この歌に元気をのせて、前線といっしょに君の町まで届けること。最後は君の笑い声が聞こえる。
# 場面と強さ: 速報（サビの先取り）→ 予報図（グロッケンのリフ）→ けさの予報（Aメロ）→ 前線が近づく（Bメロ・止め）→ はっぴーえんど（サビ）
#   → 中継（ブラスの間奏）→ 電話の声（2番。BGM はピアノが歌を受け取る）→ Bメロ2 → サビ2 → 日本列島を横切る（ギターのソロ）
#   → ひと息（Half feel）→ 1拍の無音 → 北の町へ（Cメロ）→ 北の町に届く（+2・最大）→ 笑顔のリレー（歌とブラス）→ テンションの和音
# 旋律の性格: Aメロは句の頭を休む8分。サビは同じ音を3つ置いてから上がる「はっぴーえんど」。最高音 F#5。
# ほかの曲とちがう所: いちばん王道の J-POP。ピアノ・ストリングス・ブラス・グロッケン・ギターのソロ。王道を外した進行（IV から始まる・♭VI–♭VII–I）。
from vb25_lib import *

S = Song("17", "zensen", "ハッピーエンド前線（仮）", "Happy-End Front", 180, 4, "D", "major", "J-POP（ボカロ）")
S.kit = "crocell-punch"
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags + " --piano salamander"
S.extra.update({"tone": "rock", "diGuitar": "emily"})
K = S.key                    # D長調
KE = Key("E", "major")       # 最後のサビ（+2）

A_CH = ["Dmaj7", "Bm7", "Gmaj7", "A7sus4", "Dmaj7", "Bm7", "Gmaj7", "A7"]
B_CH = ["Em7", "F#m7", "Gmaj7", "A", "Bbmaj7", "C", "D", "Daug"]
C_CH = ["G", "A/G", "F#m7", "Bm7", "Em7", "F#7", "Bm", "D7"]
C_CH2 = ["G", "A/G", "F#m7", "B7", "Em7", "A7", "D", "Daug"]
BREATH = ["Gmaj7", "F#m7", "Em7", "Dmaj7/F#", "Gmaj7", "A7sus4", "Bm7", "Bm7/A",
          "Gmaj7", "F#7", "Bm7", "D7", "Gmaj7", "Gm6", "D/A", "A7"]
LAST = [tr_chord(c, 2) for c in C_CH + C_CH2] + [tr_chord(c, 2) for c in C_CH] + ["A", "B/A", "G#m7", "C#m7", "F#m7", "B7sus4", "B7", "E"]

S.scene("速報", 8, "intro", C_CH)
S.scene("予報図", 8, "interlude", A_CH)
S.scene("南の島", 16, "verse", A_CH)
S.scene("前線が近づく", 8, "pre", B_CH)
S.scene("九州・四国が笑顔", 16, "chorus", C_CH + C_CH2)
S.scene("中継", 8, "interlude", A_CH)
S.scene("関西・東海", 16, "verse", A_CH)
S.scene("前線が近づく2", 8, "pre", B_CH)
S.scene("関東が笑顔", 16, "chorus", C_CH + C_CH2)
S.scene("日本列島を横切る", 16, "solo", C_CH + C_CH2)
S.scene("予報士がひと息", 16, "bridge", BREATH)
S.scene("北の町へ", 8, "pre", ["Em7", "F#m7", "Gmaj7", "A", "Bbmaj7", "C", "D", "B7"])
S.scene("北の町に届く", 32, "chorus", LAST)
S.scene("笑顔のリレー", 8, "outro", ["A", "B/A", "G#m7", "C#m7", "Amaj7", "B", "C#m7", "B/D#"])
S.scene("全員でテンションの和音", 4, "outro", ["Emaj9"] * 4)

V = Voice(S, vol=0.22, delay=0.75, patch="brightLead", low=True)   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
PNS = piano_spec(0.12, -0.25)
PN = [S.track(f"ピアノ（右手{i + 1}）", "piano", **PNS) for i in range(2)]
PNL = S.track("ピアノ（左手）", "piano", **PNS)
PNM = S.track("ピアノ（歌の受け渡し）", "piano", **PNS)
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", **strings_spec(0.08, 0.5)) for i in range(3)]
BR = [S.track(f"ブラス{i + 1}", "brass", patch="brassSection", volume=0.13, pan=0.3, reverb=0.22, gainDb=2,
              fx=[{"type": "eq", "low": -3, "mid": 2, "midHz": 1600, "high": 0.5}]) for i in range(3)]
GL = S.track("グロッケン", "glockenspiel", patch="glockenspiel", volume=0.09, pan=-0.45, reverb=0.35)
GT = [S.track(f"ギター（{['根音', '5度'][i]}）", "distGuitar", **rock_gtr_spec(0.08, 0.0), double=True) for i in range(2)]
LG = S.track("リードギター（列島を横切る）", "distGuitar", **lead_gtr_spec(0.14, -0.05))
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.2))
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の旋律と歌詞（D長調の度数。oct=4 で 1 = D4。書き出しの前に全体を 8半音下げる） =================
VERSE = ["R:1 3:0.5 3:0.5 5:0.5 3:0.5 1':1", "7:1 6:1.5 R:1.5",
         "R:1 4:0.5 5:0.5 6:1 5:1", "4:2 R:2",
         "R:0.5 3:0.5 5:0.5 1':0.5 1':0.5 7:0.5 1':1", "2':1 6:1.5 R:1.5",
         "R:1 6:0.5 6:0.5 5:0.5 4:0.5 3:1", "5:2 R:2",
         "R:1 1':0.5 1':0.5 7:0.5 6:0.5 5:1", "6:1 1':1.5 R:1.5",
         "R:1 4:0.5 6:0.5 1':1 7:1", "5:2 R:2",
         "R:1 3':0.5 3':0.5 2':0.5 1':0.5 7:1", "6:1 5:1.5 R:1.5",
         "R:1 6:0.5 5:0.5 4:1 3:1", "5:2 R:2"]
V1 = "けさのよほうで/きいたんだ/みなみのしまから/はれのせんが/きみのいるまち/きたのはて/はなれてからね/もうにねん"
V2 = "でんわのこえに/あめもよう/だいじょうぶだよって/からげんきで/できることはさ/なんだろう/このうたにのせ/とどけるよ"
VB = ["R:0.5 4:0.5 4:0.5 5:0.5 6:1 5:1", "6:1 7:1.5 R:1.5", "R:0.5 6:0.5 6:0.5 7:0.5 1':1 2':1", "2':1 1':1.5 R:1.5",
      "R:0.5 b6:0.5 1':0.5 b3':0.5 5':1 b3':1", "b7:1 b3':1.5 R:1.5", "R:0.5 3':0.5 2':0.5 3':0.5 5':2", "#5':1 R:3"]
P1 = "ぜんせんがくる/きたへきたへと/まちをこえてく/えがおがね"
P2 = "しずくのまども/くもりのひにも/はれまがのぞく/もうすぐだ"
VC = ["R:0.5 5':0.5 5':0.5 5':0.5 6':0.5 6':0.5 5':1", "R:0.5 4':0.5 4':0.5 4':0.5 5':1 3':0.5 R:0.5",
      "3':0.5 2':0.5 1':0.5 5:0.5 6:1 3':1", "2':0.5 1':0.5 6:0.5 1':0.5 3':1.5 R:0.5",
      "R:0.5 5':0.5 5':0.5 5':0.5 1'':1 6':1", "3':0.5 #5':0.5 7':0.5 #5':0.5 3':1 2':0.5 R:0.5",
      "1':0.5 2':0.5 3':0.5 6':0.5 5':1 3':1", "3':0.5 5':0.5 b7':0.5 5':0.5 3':1.5 R:0.5",
      "R:0.5 5':0.5 5':0.5 5':0.5 6':0.5 6':0.5 5':1", "R:0.5 4':0.5 4':0.5 4':0.5 5':1 3':0.5 R:0.5",
      "3':0.5 2':0.5 1':0.5 5:0.5 6:1 3':1", "#2':0.5 3':0.5 6':0.5 5':0.5 #2':1.5 R:0.5",
      "R:0.5 2':0.5 2':0.5 2':0.5 5':1 2':1", "7:0.5 2':0.5 5':0.5 4':0.5 2':1 7:0.5 R:0.5",
      "1':1 3':1 5':2", "#5':2 R:2"]
C1 = "はっぴーえんど/ぜんせんが/きみのまちまでのぼってく/しぐれのよるもあしたは/えがおびよりになるから/はっぴーえんど/ぜんせんよ/このうたごとつれていけ/とおくのきみのそらまで/はれるよ"
C2 = "はっぴーえんど/ぜんせんが/かんさいかんとうをこえ/どしゃぶりのまちにもほら/にじがかかりはじめたよ/はっぴーえんど/ぜんせんよ/このうたごとつれていけ/とおくのきみのそらまで/はれるよ"
VCx = [x.replace("1'':1 6':1", "6':1 5':1").replace("7':0.5", "6':0.5") for x in VC]    # 最後のサビ（+2）はテトの高さに収める
END = ["R:0.5 5':0.5 5':0.5 5':0.5 6':2", "R:0.5 5':0.5 5':0.5 5':0.5 6':1 5':0.5 R:0.5", "3':0.5 2':0.5 1':0.5 3':0.5 5':2", "6':1 5':1 3':1.5 R:0.5",
       "R:0.5 3':0.5 3':0.5 3':0.5 6':1.5 R:0.5", "5':1.5 4':0.5 3':1 2':1", "4':2 2':2", "1':4"]
CL = C1 + "/はっぴーえんど/ぜんせんが/きみのまちにとどいたよ/ゆきのまちもあたたかく/えがおびよりになったよね/とどいた/きみのこえ/わらってるきこえる/ありがと/またあえるよね"
VBR = ["5:2 6:1 1':1", "3':3 R:1", "1':2 7:1 5:1", "6:3 R:1", "1':2 2':1 3':1", "5':3 R:1", "3':2 2':1 1':1", "6:2 1':1 R:1",
       "2':2 1':1 6:1", "#5:3 R:1", "2':2 1':2", "b7':3 R:1", "6:2 1':1 2':1", "b6:2 2':1 R:1", "1':2 5:2", "5:2 7:2"]
VK = ["R:0.5 4:0.5 6:0.5 1':0.5 2':1 1':1", "R:0.5 5:0.5 7:0.5 2':0.5 3':1 2':1", "R:0.5 6:0.5 1':0.5 3':0.5 4':1 3':1",
      "R:0.5 7:0.5 2':0.5 4':0.5 5':2", "R:0.5 b6:0.5 1':0.5 b3':0.5 b6':1 5':1", "R:0.5 b7:0.5 2':0.5 4':0.5 6':1 4':1", "1':1 3':1 5':1 6':1", "6':2 R:2"]
RELAY = ["R:0.5 5':0.5 5':0.5 5':0.5 6':1 5':1", "R:0.5 4':0.5 4':0.5 4':0.5 5':1 3':1", "R:0.5 3':0.5 3':0.5 3':0.5 5':1 3':1",
         "3':0.5 2':0.5 1':0.5 5:0.5 6:1 3':1", "R:0.5 5':0.5 5':0.5 5':0.5 6':1 5':1", "4':1 2':1 7:1 5:1", "3':0.5 5':0.5 6':0.5 5':0.5 3':2", "2':2 7:2"]
LY = Lyrics(S)
def put(name, key, lines, text, low=True):
    bars = S.sc(name); mel = [key.mel(x, oct=4) for x in lines]
    for i, (b, m) in enumerate(zip(bars, mel)): V.bar(b, m, low=low if not callable(low) else low(i))
    LY.flow(bars, mel, text, name)
put("速報", K, VC[:8], "/".join(C1.split("/")[:5]))
put("南の島", K, VERSE, V1)
if VOCAL: put("関西・東海", K, VERSE, V2)
else:
    for i, b in enumerate(S.sc("関西・東海")):
        if i < 8: PNM.bar(b, shift_oct(K.mel(VERSE[i], oct=4), 1))   # BGM: 前半はピアノが歌を受け取る（1オクターブ上）
        else: V.bar(b, K.mel(VERSE[i], oct=4))
put("前線が近づく", K, VB, P1); put("前線が近づく2", K, VB, P2)
put("九州・四国が笑顔", K, VC, C1); put("関東が笑顔", K, VC, C2)
put("予報士がひと息", K, VBR, "ひといき/ついたら/そらみて/まぶたうら/あのひの/えがお/ちずのはし/つながる", low=lambda i: i >= 8)
put("北の町へ", K, VK, "きたのまち/ゆきのまち/きみのまち/とどけよ/くもをこえ/やまこえていまとどけ")
put("北の町に届く", KE, VCx + VCx[:8] + END, CL)
vb_, vm_ = [], []
for i, b in enumerate(S.sc("笑顔のリレー")):
    if (i // 2) % 2 == 0: m = KE.mel(RELAY[i], oct=4); V.bar(b, m); vb_.append(b); vm_.append(m)
    else:
        m = KE.mel(RELAY[i], oct=4)
        BR[0].bar(b, shift_oct(m, -1)); BR[1].bar(b, shift_oct(KE.mel(seq_up(RELAY[i], KE, -2), oct=4), -1))
LY.flow(vb_, vm_, "わらえたね/ありがとう/はっぴーえんどだよね", "笑顔のリレー")
V.bar(S.sc("全員でテンションの和音")[0], KE.mel("2':12", oct=4))    # 9th をのばす（歌の役だけ）


# ================= グロッケン（予報図のリフ・サビのきらめき） =================
GR = ["1'':0.5 5':0.5 3'':0.5 1'':0.5 5':0.5 1'':0.5 2'':1", "6':0.5 3'':0.5 2'':0.5 6':0.5 1'':1 6':1",
      "5':0.5 2'':0.5 1'':0.5 5':0.5 7':0.5 5':0.5 3'':1", "4'':0.5 2'':0.5 1'':0.5 5':0.5 2'':2"]
for i, b in enumerate(S.sc("予報図")): GL.bar(b, K.mel(GR[i % 4], oct=4))
for name in ("南の島", "関西・東海"):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3: GL.bar(b, K.mel("R:2 5':0.5 6':0.5 1'':1", oct=4))
for name in ("九州・四国が笑顔", "関東が笑顔", "北の町に届く", "速報"):
    kk = KE if name == "北の町に届く" else K
    for i, b in enumerate(S.sc(name)):
        if i % 2 == 1: GL.bar(b, kk.mel("R:3 1'':0.5 5':0.5", oct=4))

# ================= ブラス（中継の主旋律・サビの合いの手） =================
BH = ["5:0.5 5:0.25 5:0.25 1':0.5 5:0.5 R:0.5 3':0.5 2':0.5 1':0.5", "6:0.5 6:0.25 6:0.25 2':0.5 6:0.5 R:0.5 1':0.5 7:0.5 6:0.5",
      "5:0.5 5:0.25 5:0.25 1':0.5 3':0.5 R:0.5 5':0.5 4':0.5 3':0.5", "2':1 1':0.5 7:0.5 5:2"]
for i, b in enumerate(S.sc("中継")):
    BR[0].bar(b, K.mel(BH[i % 4], oct=4)); BR[1].bar(b, K.mel(seq_up(BH[i % 4], K, -2), oct=4))
for name in ("九州・四国が笑顔", "関東が笑顔", "北の町に届く", "速報"):
    for i, b in enumerate(S.sc(name)):
        v = voice(S.chords[b], 64, 3)
        if name == "北の町に届く" and i >= 28: continue
        if i % 4 == 1:
            for j in range(3): BR[j].bar(b, f"R:3 {nm(v[j])}:0.25' R:0.25 {nm(v[j])}:0.5!")
        elif i % 8 == 7:
            for j in range(3): BR[j].bar(b, f"R:2 {nm(v[j])}:0.5' {nm(v[j])}:0.5' {nm(v[j])}:1")

# ================= ギターのソロ（日本列島を横切る） =================
SOLO = ["5:0.5 6:0.5 1':0.5 2':0.5 3':1 2':0.5 1':0.5", "4':1.5 3':0.5 2':1 1':1",
        "3':0.25 2':0.25 1':0.25 7:0.25 6:0.5 5:0.5 6:1 3':1", "4':0.5 3':0.5 2':0.5 1':0.5 6:2",
        "5:0.5 2':0.5 5':1 4':0.5 2':0.5 5:1", "#5:0.5 3':0.5 #5':0.5 7':0.5 6':1 #5':1",
        "6':0.25 5':0.25 3':0.25 2':0.25 1':0.5 6:0.5 3':1 2':1", "b7':1 6':0.5 5':0.5 3':2",
        "5':0.5 4':0.5 3':0.5 2':0.5 1':1 5:1", "6:0.5 1':0.5 4':0.5 5':0.5 3':2",
        "3':0.25 4':0.25 5':0.25 6':0.25 5':0.5 3':0.5 1':1 3':1", "#2':1 3':0.5 6':0.5 5':2",
        "2':0.5 5':0.5 2'':1 1'':0.5 7':0.5 5':1", "7:0.5 2':0.5 5':0.5 7':0.5 6':1 5':1",
        "3':1 5':1 1'':2", "#5':4^"]
for i, b in enumerate(S.sc("日本列島を横切る")): LG.bar(b, K.mel(SOLO[i], oct=3))

# ================= ピアノ（右手16分の分散和音・左手8分のオクターブ） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "全員でテンションの和音":
        if i == 0:
            v = voice("Emaj9", 66, 2)
            for j in range(2): PN[j].bar(b, f"{nm(v[j])}:12")
            PNL.bar(b, "E2:12")
        continue
    if n in ("南の島",) and i < 8:
        v = voice(ch, 66, 2)
        for j in range(2): PN[j].bar(b, f"R:0.5 {nm(v[j])}:1 R:1 {nm(v[j])}:1.5")
        PNL.bar(b, f"{nm(low(ch, 'C2'))}:2 {nm(low(ch, 'C2') + 7)}:2"); continue
    if n == "予報士がひと息":
        v = voice(ch, 64, 2)
        for j in range(2): PN[j].bar(b, f"{nm(v[j])}:1 {nm(v[j])}:1 {nm(v[j])}:2")
        PNL.bar(b, f"{nm(low(ch, 'C2'))}:4"); continue
    if n == "予報図": continue
    PN[0].bar(b, piano_arp16(ch, "D4", "D6"))
    PNL.bar(b, piano_left8(ch, "C2"))

# ================= ストリングス =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n in ("九州・四国が笑顔", "関東が笑顔", "北の町に届く", "予報士がひと息", "前線が近づく", "前線が近づく2", "速報", "北の町へ", "全員でテンションの和音", "笑顔のリレー"):
        v = voice(S.chords[b], 67, 3)
        if n == "全員でテンションの和音":
            if i == 0:
                for j in range(3): STR[j].bar(b, f"{nm(voice('Emaj9', 70, 3)[j])}:12")
            continue
        if n.startswith("前線") or n == "北の町へ":
            for j in range(3): STR[j].bar(b, f"{nm(v[j])}:4" if j else f"{nm(v[j] + 12)}:0.5' {nm(v[j] + 12)}:0.5' {nm(v[j] + 12)}:0.5' {nm(v[j] + 12)}:0.5' {nm(v[j] + 12)}:2")
        else:
            for j in range(3): STR[j].bar(b, f"{nm(v[j])}:4")

# ================= ギター（パワーコード） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    pw = power(S.chords[b], "E2")
    if n in ("予報図", "予報士がひと息"): continue
    if n == "全員でテンションの和音":
        if i == 0:
            for j in range(2): GT[j].bar(b, f"{nm(pw[j])}:12")
        continue
    if n in ("南の島", "関西・東海"):
        pat = "X:1.5! X:1 X:1.5" if i % 2 == 0 else "X:1.5! X:0.5 X:2"
        if i < 4 and n == "南の島": continue
    elif n.startswith("前線") or n == "北の町へ":
        pat = "X:1! X:1 X:1 X:1"
    else:
        pat = " ".join("X:0.5" + ("!" if q % 2 == 0 else "") for q in range(8))
    for j in range(2): GT[j].bar(b, pat.replace("X", nm(pw[j])))

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n == "全員でテンションの和音":
        if i == 0: BASS.bar(b, "E1:12")
        continue
    if n == "予報図": BASS.bar(b, bass_line(S, b, "long") if i >= 4 else "R:4")
    elif n in ("南の島", "関西・東海"): BASS.bar(b, bass_line(S, b, "root8" if i < 8 else "push"))
    elif n.startswith("前線") or n == "北の町へ": BASS.bar(b, bass_line(S, b, "root8"))
    elif n == "予報士がひと息": BASS.bar(b, bass_line(S, b, "half"))
    else: BASS.bar(b, bass_line(S, b, "oct8"))

# 効果音
riser(FX, S.sc("九州・四国が笑顔")[0], 4, "C4"); riser(FX, S.sc("関東が笑顔")[0], 4, "C4"); riser(FX, S.sc("北の町に届く")[0], 8, "D4")
cym_swell(CYM, S.sc("日本列島を横切る")[0], 2, "C4"); cym_swell(CYM, S.sc("北の町へ")[0], 2, "C4")
CYM.bar(S.sc("全員でテンションの和音")[0], "B4:16")

# ================= ドラム（生ドラム・TRiDENT の音） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "笑顔のリレー":
        vgroove(D, b, "punk" if i < 6 else "vrock", ghosts=0.4, seed=b)
        if i == 0: crash(D, b, "G2")
        if i == 4: crash(D, b, "B2")
        if last: put_fill(D, b, "tomdown")
    elif n in ("速報", "九州・四国が笑顔", "関東が笑顔", "北の町に届く"):
        vgroove(D, b, "vrock", ghosts=0.3, seed=b)
        if n == "関東が笑顔" and i >= 8: vgroove(D, b, "vrock2", ghosts=0.4, seed=b, h="XxxxXxxxXxxxXxxx")   # 後半は跳ねるキックに
        if n == "北の町に届く" and 16 <= i < 24:
            D.cym(b, "D2:0.5 " * 8); D.H[b] = "." * 16                                  # ライドで押す
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "tomdown" if i % 16 == 15 else "snare16")
        if last and n == "速報": put_fill(D, b, "small")
        if last and n == "九州・四国が笑顔": put_fill(D, b, "tomdown")
        if last and n == "関東が笑顔": put_fill(D, b, "tomtrip")
        if last and n == "北の町に届く": put_fill(D, b, "snare16")
    elif n == "予報図":
        if i < 4: D.set(b, "X.......X.......", "." * 16, "x.x.x.x.x.x.x.x.")
        else: vgroove(D, b, "beat8", ghosts=0.3, seed=b)
        if last: put_fill(D, b, "snare16")
    elif n in ("南の島", "関西・東海"):
        vgroove(D, b, "vrock2", ghosts=0.4, seed=b)
        if n == "関西・東海" and i < 8: D.cym(b, "D2:0.5 " * 8); D.H[b] = "." * 16
        if i == 0: crash(D, b, "G2" if n == "南の島" else "C2")
        if i % 8 == 7: put_fill(D, b, "small" if i < 15 else "build")
    elif n.startswith("前線") or n == "北の町へ":
        vgroove(D, b, "half" if i < 4 else "vrock2", ghosts=0.3, seed=b)
        if i == 4: crash(D, b, "B2")
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 1 if n.startswith("前線") else 2)
    elif n == "中継":
        vgroove(D, b, "punk", ghosts=0.3, seed=b)
        if i == 0: crash(D, b)
        if last: put_fill(D, b, "tomdown")
    elif n == "日本列島を横切る":
        vgroove(D, b, "vrock", ghosts=0.4, seed=b)
        D.cym(b, ("B2:0.5 " if i % 8 == 0 else "D2:0.5 ") + "D2:0.5 " * 7); D.H[b] = "." * 16
        if i % 4 == 3: put_fill(D, b, "tomtrip" if i % 8 == 7 else "small")
    elif n == "予報士がひと息":
        if i < 4: D.set(b, "X...............", "." * 16, "x...x...x...x...")
        else: vgroove(D, b, "half", ghosts=0.4, seed=b)
        if i == 8: crash(D, b, "G2")
        if i == 14: put_fill(D, b, "lift")
    elif n == "全員でテンションの和音":
        if i == 0: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 12)

# 止め: Bメロの終わり2回（1拍だけ）・北の町への終わり（2拍）。1拍の完全な無音: 予報士がひと息の最後の拍
for name in ("前線が近づく", "前線が近づく2"): SIL.add(S.sc(name)[-1], 1, 4)
SIL.add(S.sc("北の町へ")[-1], 2, 4)
SIL.add(S.sc("予報士がひと息")[-1], 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の17。J-POP（疾走）。F#長調・180、最後のサビは +2（G#）。"
          "遠い北の町へ引っ越した友だちに、「ハッピーエンド前線」といっしょに元気を届けたい。サビの先取りで始まり、グロッケンのリフ、8分で語る Aメロ、止めのある Bメロ、"
          "「はっぴーえんど」のサビ、ブラスの中継、ギターのソロ、Half feel のひと息と1拍の無音、+2 の最後のサビ、歌とブラスの笑顔のリレー、テンションの和音。自作")
# 季節の音（2026-10-25 人間「季節を感じれる様な音も欲しい」）
season(S, 0, "そよ風", S.beats * 8, vol=0.06)
S.no_depth = True
teto(S, LY, V, transpose=-8, special={"北の町に届く": 0.55, "予報士がひと息": -0.5, "北の町へ": 0.1, "速報": 0.2})
