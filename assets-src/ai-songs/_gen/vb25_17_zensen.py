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
# 2026-10-26 人間「ドラムの音がデジタルすぎるのも原因かもね」: 07・18 で試すと、素直な生ドラム（Naked Drums）で点数が +0.3（07: 7.12→7.44、18: 7.22→7.51）
#   → 太鼓ごとに作り込んだ crocell-punch をやめて、Naked Drums に（太鼓の音量などの設定は今までと同じ）
S.kit = "naked-x"   # 前: "crocell-punch"
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
# 2026-10-26 人間「エイトビートもライドで刻むとか、ハイハット以外もつかって曲に合うように変えてほしい。これ重要」:
#   前線が近づく（Bメロ）はライドで雲がかかるように、2回目のサビはライドのカップ、予報士がひと息は4分、北の町へは裏の開いたハイハット
# 2026-10-26 人間「オープンとクローズのハイハットの使い分けとかね」: 九州・四国が笑顔=openq
S.keepers = {'前線が近づく': 'ride', '前線が近づく2': 'ride', '関東が笑顔': 'bell', '予報士がひと息': 'quarter', '北の町へ': 'open', '九州・四国が笑顔': 'openq'}
# 2026-10-26 人間「シンプルなドラムのフレーズ色々入れて欲しい」「曲に合ったものを」「全部同じにするとつまらなくなる」:
#   中継（間奏）はテレビの中継のように、はねる3連の刻み。南の島（Aメロ）の前半はキック少なめ。最後のサビの前はハイハットを16分にしてためる
S.dmoves = [('中継', 'beat', 'shuffle'), ('南の島', 'beat', '8sparse', 0, 7), ('北の町に届く', 'lift')]

V = Voice(S, vol=0.22, delay=0.75, patch="brightLead", low=True)   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
PNS = piano_spec(0.12, -0.25)
PN = [S.track(f"ピアノ（右手{i + 1}）", "piano", **PNS) for i in range(2)]
PNL = S.track("ピアノ（左手）", "piano", **PNS)
PNM = S.track("ピアノ（歌の受け渡し）", "piano", **PNS)
# 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ ピアノの右手の和音（3音）を足す。PN と同じ設定なので同じチャンネル
PNC = [S.track(f"ピアノ（右手の和音{i + 1}）", "piano", **{**PNS, "volume": 0.085}) for i in range(3)]   # 3音の和音なので1本あたり 0.085（3本で分散和音 0.12 の1本と同じくらいの大きさ）
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", **strings_spec(0.08, 0.5)) for i in range(3)]
# 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ 最後のサビの高い対旋律（ストリングスの4本目。ほかの弦と同じ設定・0.08 より小さく 0.07）
STRC = S.track("ストリングス（最後のサビの高い声部）", "strings", patch="stringEnsemble", **strings_spec(0.07, 0.5))
T_ = -8   # 書き出しの前に全体を 8半音下げる。ベースは「下げたあと」に E1〜E3 に入るよう、書く高さを C2〜C4 にする
BL = nm(28 - T_)
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
            PNL.bar(b, "E3:12")
        continue
    if n in ("南の島",) and i < 8:
        v = voice(ch, 66, 2)
        for j in range(2): PN[j].bar(b, f"R:0.5 {nm(v[j])}:1 R:1 {nm(v[j])}:1.5")
        PNL.bar(b, f"{nm(low(ch, 'D3'))}:2 {nm(low(ch, 'D3') + 7)}:2"); continue
    if n == "予報士がひと息":
        v = voice(ch, 64, 2)
        for j in range(2): PN[j].bar(b, f"{nm(v[j])}:1 {nm(v[j])}:1 {nm(v[j])}:2")
        PNL.bar(b, f"{nm(low(ch, 'D3'))}:4"); continue
    if n == "予報図": continue
    # 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ ピアノはコード弾き（左手と右手）を場面で弾き分ける。
    #   左手は書く高さを C2 → D3 に（下げたあと F#2 から。下げたあと E1 まで下がって歌うベースと重なり、低音がにごっていた）
    #   Aメロ後半: 右手の和音の付点の刻み（分散和音から受け渡す）／サビの後半8小節: 和音を8分の裏で押す（前半は分散和音のまま）
    if n in ("南の島", "関西・東海") and i >= 8:
        v = voice(ch, 67, 3)
        for j in range(3): PNC[j].bar(b, f"{nm(v[j])}:1.5 {nm(v[j])}:1 {nm(v[j])}:1.5" if i % 2 == 0 else f"{nm(v[j])}:1.5 {nm(v[j])}:0.5 R:2")
        r = low(ch, "D3"); PNL.bar(b, f"{nm(r)}:1.5 {nm(r + 12)}:1 {nm(r + 7)}:1.5"); continue
    if n in ("九州・四国が笑顔", "関東が笑顔", "北の町に届く") and i % 16 >= 8 and not (n == "北の町に届く" and i >= 24):
        v = voice(ch, 67, 3)
        for j in range(3): PNC[j].bar(b, f"{nm(v[j])}:0.5! {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5 {nm(v[j])}:1")
        PNL.bar(b, piano_left8(ch, "D3")); continue
    PN[0].bar(b, piano_arp16(ch, "D4", "D6"))
    PNL.bar(b, piano_left8(ch, "D3"))

# 合いの手（ピアノ）: Aメロの句の終わり（歌が 2.5拍目から休む小節。グロッケンの小節とは別の小節）に、高い短い句
FILL = ["R:2.75 3'':0.25 2'':0.25 1'':0.25 5':0.5", "R:2.75 6':0.25 1'':0.25 2'':0.25 3'':0.5",
        "R:2.75 5'':0.25 3'':0.25 2'':0.25 1'':0.5", "R:2.75 4':0.25 6':0.25 1'':0.25 2'':0.5"]
for name in ("南の島", "関西・東海"):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 1 and not (name == "関西・東海" and i < 8 and not VOCAL): PNM.bar(b, K.mel(FILL[(i // 4) % 4], oct=4))

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
# 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ 最後のサビ（9〜24小節目）に、歌より上の高い対旋律（E長調の度数・下げたあと C5〜C6）。
#   歌が細かく動く所は全音符でのばし、歌が伸ばす小節の後半で動く。和音の音（3度・7度）を長い音に置く
CM_A = ["6':2 5':1 6':1", "7':4", "7':2 6':1 5':1", "3':2 5':2", "4':2 6':2", "#5':2 7':2", "3':4", "5':2 b7':2"]    # C_CH を +2 した8小節
CM_B = ["6':2 5':1 6':1", "7':4", "7':2 6':1 5':1", "3':4", "4':2 6':2", "5':2 7':1 6':1", "1'':4", "#5':4"]      # C_CH2 を +2 した8小節
for i, b in enumerate(S.sc("北の町に届く")):
    if 8 <= i < 16: STRC.bar(b, KE.mel(CM_B[i - 8], oct=4))
    elif 16 <= i < 24: STRC.bar(b, KE.mel(CM_A[i - 16], oct=4))

# ================= ギター（パワーコード） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    # 2026-10-26 ミックス: 書く高さ E2 は下げたあと G#1 になり、ギターの出ない音・ベースとの低音の二重になっていたので C3（下げたあと E2〜。ギターのふつうの低い音）に
    pw = power(S.chords[b].split("/")[0], "C3")   # 分数コードは上の和音で（A/G で G と D を弾くと A の和音とぶつかる）
    if n == "日本列島を横切る": pw = power(S.chords[b].split("/")[0], "F#2")   # ギターのソロの下では1オクターブ下へよけて、リードとぶつからない
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

# ================= ベース（歌うベース） =================
# 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ 根音の8分・オクターブだけだったのを、場面ごとに旋律のあるベースに（音量 0.2 はそのまま）。
#   あわせて、書き出しの前の −8半音で B♭0 まで下がっていた（ベースに出ない音）のを、書く高さを C2〜C4 にして、下げたあと E1〜E3 に入れた。
#   速報・サビ: 押す（drive）。歌が伸ばす句の終わり（4小節目）だけ駆ける（run）／予報図: ゆったり（ride）で前線の地図をなぞる
#   Aメロ前半: 押す形と歩く形を交互（語りを支える）／後半: 上る・下るで2番へ向けて動く／Bメロ: 上っていく（climb）
#   中継: 押す・駆ける／ソロ: 前半は歩く、後半は押す／ひと息: Half feel のまま、後半だけゆったり動く／北の町へ: 上る
sb = lambda b, st: sing_bass(S, b, st, lo=28 - T_, hi=52 - T_)
bl = lambda b, st: bass_line(S, b, st, lo=BL)
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, BL)
    if n == "全員でテンションの和音":
        if i == 0: BASS.bar(b, f"{nm(r)}:12")
        continue
    if n == "予報図": BASS.bar(b, sb(b, "ride") if i >= 4 else "R:4")
    elif n in ("南の島", "関西・東海"):
        if i < 8: BASS.bar(b, sb(b, "walk") if i % 2 == 1 else bl(b, "push"))
        else: BASS.bar(b, sb(b, "climb" if i % 2 == 0 else "fall"))
    elif n.startswith("前線") or n == "北の町へ": BASS.bar(b, sb(b, "climb") if i < L - 1 else f"{nm(r)}:1! R:3")
    elif n == "予報士がひと息": BASS.bar(b, bl(b, "half") if i < 8 else sb(b, "ride"))
    elif n in ("中継",): BASS.bar(b, sb(b, "run" if i % 4 == 3 else "drive"))
    elif n == "日本列島を横切る": BASS.bar(b, sb(b, "walk" if i < 8 else ("run" if i % 4 == 3 else "drive")))
    elif n == "北の町に届く" and i >= 28: BASS.bar(b, sb(b, "ride"))
    elif n == "笑顔のリレー": BASS.bar(b, sb(b, "ride" if i % 2 == 0 else "run"))
    else: BASS.bar(b, sb(b, "run" if i % 4 == 3 else "drive"))

# 効果音
riser(FX, S.sc("九州・四国が笑顔")[0], 4, "C4"); riser(FX, S.sc("関東が笑顔")[0], 4, "C4"); riser(FX, S.sc("北の町に届く")[0], 8, "D4")
cym_swell(CYM, S.sc("日本列島を横切る")[0], 2, "C4"); cym_swell(CYM, S.sc("北の町へ")[0], 2, "C4")
CYM.bar(S.sc("全員でテンションの和音")[0], "B4:16")
# 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ この曲の物語でしか出てこない音: 前線といっしょに空が変わっていく。
#   はじめは「そよ風」（南の島）→ 2番の「でんわのこえに あめもよう」で雨（0.05・小さく）→ 2回目のサビの頭で雨がやみ、グロッケンが虹をかける（上がる分散和音）
#   → 北の町へ（雪の町）で雪の鈴 → 笑顔のリレーで小鳥。音量はどれも 0.05〜0.06 の控えめ
season(S, S.sc("関西・東海")[0], "雨", 16 * 4, vol=0.05, every=16)
GL.bar(S.sc("関東が笑顔")[0], K.mel("R:2 1'':0.25 3'':0.25 5'':0.25 1''':0.25 3''':0.5 5''':0.5", oct=4))
season(S, S.sc("北の町へ")[0], "雪の鈴", 8 * 4, vol=0.05)
season(S, S.sc("笑顔のリレー")[0], "小鳥", 12 * 4, vol=0.05)

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

# 2026-10-26 人間「ドラム強弱、アクセント、余韻も上手く使ってね」→ 場面ごとの強弱と、止めのあとのシンバルの余韻
#   Aメロ: ハイハットは句の頭（4小節ごとの1拍目）だけ強く、ほかは軽く。前半8小節はスネアの2拍目も軽く（4拍目は強いまま）
#   Bメロ・北の町へ: 前半4小節は軽く、後半で強く（溜める）。止めの1打にはクラッシュを2小節ぶん鳴らしたまま残す
#   ひと息（Cメロ）: ハイハットを全部軽く。サビ: 8小節ごとの頭のクラッシュを長く（6拍）残す
def soft_hat(b, keep_head=True):
    h = list(D.H[b])
    for q in range(16):
        if h[q] == "X" and not (keep_head and q == 0): h[q] = "x"
    D.H[b] = "".join(h)
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if k == "verse":
        soft_hat(b, keep_head=(i % 4 == 0))
        if i < 8 and D.S[b][4] == "X": D.S[b] = D.S[b][:4] + "x" + D.S[b][5:]
    elif (n.startswith("前線") or n == "北の町へ") and i < 4: soft_hat(b, keep_head=(i == 0))
    elif n == "予報士がひと息": soft_hat(b, keep_head=False)
# 2026-10-26 人間「後半に行くにつれて曲の始まり方似てない？」→ 全員の一撃（25 と同じ入り方）をやめて、「ドラムだけ」で始める。
#   速報の前の4小節は、タムを回すドラムの独奏（と歌）。5小節目の2回目の「はっぴーえんど」でクラッシュとともにバンドが入る
TOMS = ["R:0.5 C4:0.5 R:0.5 A3:0.25 A3:0.25 F3:0.5 D3:0.5 R:0.5 A2:0.5!",
        "R:0.5 C4:0.25 C4:0.25 R:0.5 A3:0.5 F3:0.5 R:0.5 D3:0.25 D3:0.25 A2:0.5",
        "R:0.5 C4:0.5 R:0.5 A3:0.25 F3:0.25 R:0.5 D3:0.5 R:0.5 A2:0.25 A2:0.25"]
for i, b in enumerate(S.sc("速報")[:4]):
    if i < 3:
        D.set(b, "X.....X...X.....", "....X.......X..." if i != 2 else "....X.......X.o.", "." * 16); D.tom(b, TOMS[i])
    else:
        D.set(b, "X.......X.......", "....X...xxXXxXXX", "." * 16)
intro_end = S.bar_beat(S.sc("速報")[4])
for t in S.tracks:
    if t in (V.main, V.low) or "季節の音" in t.role: continue
    t.ev = [e for e in t.ev if e[0] >= intro_end - 1e-6]
crash(D, S.sc("速報")[4], "C2", 6)
for name in ("前線が近づく", "前線が近づく2"): crash(D, S.sc(name)[-1], "C2", 8)
crash(D, S.sc("北の町へ")[-1], "G2", 8)
for name in ("九州・四国が笑顔", "関東が笑顔"):
    for i, b in enumerate(S.sc(name)):
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2", 6)

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
