# vt25 22「明日の天気はハレルヤ」Tomorrow's Forecast: Hallelujah（仮）— 渋谷系（ポップス）。136・4/4。B → サビ2で C → 最後のサビで D♭（転調が2回）。
# 物語: 朝のテレビの天気予報は「一日、雨」。わたしの心も、きのうの夜にきみとけんかしてから、ずっとくもり。
#   傘の中でふと思う、明日の空はどんな色。泣いたあとの空は少し明るい。「ごめんね」のメッセージを送ったら、返事が来た。
#   明日の天気は、晴れのち、ハレルヤ。傘をたたんだら、あの交差点まで、きみに会いに行く。
# 場面と強さ: 天気予報のチャイム（ベルのファンファーレ）→ イントロ（ピチカートとフルート）→ Aメロ1（語る）→ Bメロ1 → サビ1（B）
#   → 間奏（トランペットとフルート）→ Aメロ2 → Bメロ2 → サビ2（C へ転調）→ Cメロ（雨の日の思い出・短調で静か）
#   → チャイム2（ベルのファンファーレで、もう一度転調）→ 最後のサビ（D♭・いちばん強い）→ 終わり（ベルのファンファーレ）
# 旋律の性格: Aメロは8分で軽やかに語る。サビは「5 → 1' → 2' → 3'」と晴れ上がる形。
# ほかの曲とちがう所: 天気予報のチャイム（ベルのファンファーレ）が、曲の頭・転調の前・終わりに鳴る。ピチカートの弦、転調が2回。
from vt25_lib import *

S = Song("22", "hallelujah", "明日の天気はハレルヤ（仮）", "Tomorrow's Forecast: Hallelujah", 136, 4, "B", "major", "ポップス（渋谷系・ボカロ）")
S.kit = "jpop"
S.flags = S.flags + " --piano salamander --space room --space-wet 0.18"
K = Key("B", "major")           # oct 3 で 1 = B3（歌うのは A#3〜D#5）
K2 = Key("C", "major")          # サビ2・Cメロ（oct 4 で 1 = C4）
K3 = Key("Db", "major")         # 最後のサビ（oct 4 で 1 = D♭4）

A_CH = ["Bmaj7", "G#m7", "C#m7", "F#7", "D#m7", "G#7", "C#m7", "F#7"]
B_CH = ["Emaj7", "D#m7", "C#m7", "F#7sus4", "Emaj7", "D#7", "G#m7", "F#7"]
C_CH = ["Emaj7", "F#", "D#m7", "G#m7", "C#m7", "F#7", "Bmaj7", "B7", "Emaj7", "F#", "D#m7", "G#7", "C#m7", "F#7", "Bmaj7", "Bmaj7"]
up = lambda cs, s: [tr_chord(c, s) for c in cs]
X_CH = ["Am7", "Dm7", "G7", "Cmaj7", "Fmaj7", "Dm7", "E7", "Am7"]
TAG_CH = ["Gbmaj7", "Ab", "Fm7", "Bbm7", "Gbmaj7", "Dbmaj7", "Dbmaj7", "Dbmaj7"]

S.scene("天気予報のチャイム", 4, "intro", ["Bmaj7", "Bmaj7", "Emaj7", "F#7"])
S.scene("イントロ", 8, "intro", A_CH)
S.scene("Aメロ1", 16, "verse", A_CH * 2)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 8, "break", A_CH)
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH[:7] + ["G7"])               # 最後の小節は C への入り口（G7）
S.scene("サビ2", 16, "chorus", up(C_CH, 1))
S.scene("Cメロ", 16, "bridge", X_CH * 2)
S.scene("チャイム2", 2, "break", ["Ab7sus4", "Ab7"])            # D♭ への入り口
S.scene("最後のサビ", 24, "chorus", up(C_CH, 2) + TAG_CH)
S.scene("終わり", 6, "outro", ["Gbmaj7", "Ab7", "Dbmaj9", "Dbmaj9", "Dbmaj9", "Dbmaj9"])

V = Voice(S, vol=0.21, delay=0.75, bright=0.6, patch="popLeadClear", low=True)
PNFX = [{"type": "eq", "low": -3, "mid": -1.5, "midHz": 400, "high": 2.5}]
PN = [S.track(f"ピアノ{i + 1}", "piano", volume=0.085, pan=-0.15, reverb=0.25, fx=PNFX) for i in range(4)]
BASS = S.track("ベース（指弾き）", "bass", **finger_bass_spec(vol=0.2))
PIZZ = S.track("ピチカート", "strings", patch="pizzicato", volume=0.07, pan=0.35, reverb=0.35)
PIZ2 = S.track("ピチカート（低い弦）", "strings", patch="pizzicato", volume=0.06, pan=-0.35, reverb=0.35)
FL = S.track("フルート", "panflute", patch="flute", volume=0.16, bright=-0.5, pan=-0.2, reverb=0.45, breath=True, mono=True, sustain=1.0)
TP = [S.track(f"トランペット{i + 1}", "brass", patch="trumpet", volume=0.075, pan=0.25 - 0.5 * i, reverb=0.35, breath=True, attack=0.04,
              release=0.3, bright=-0.4, fx=[{"type": "eq", "low": 0, "mid": -2, "midHz": 3000, "high": -4}]) for i in range(2)]
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.05, pan=-0.35 + 0.35 * i, reverb=0.45, sustain=1.4) for i in range(3)]
BELL = S.track("ベル（天気予報のチャイム）", "bell", patch="glockenspiel", volume=0.07, pan=0.2, reverb=0.5)
VIB = S.track("ビブラフォン", "harp", patch="vibraphone", volume=0.06, pan=0.4, reverb=0.4, sustain=1.5, bright=-0.2)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.05, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 3:0.5 3:0.5 3:0.5 2:0.5 3:0.5 5:1", "3:1.5 2:0.5 1:1 R:1",
      "R:0.5 4:0.5 4:0.5 4:0.5 3:0.5 4:0.5 6:1", "5:1.5 4:0.5 3:1 R:1",
      "R:0.5 5:0.5 5:0.5 5:0.5 6:0.5 5:0.5 7:1", "1':1.5 7:0.5 6:1 R:1",
      "R:0.5 4:0.5 4:0.5 3:0.5 2:0.5 3:0.5 4:1", "3:2 R:2"]
A1 = ("あさのてれびのなか/おねえさんがいうの/きょうはいちにちあめ/かさをひらいて/"
      "わたしのこころもね/ずっとどんよりぐもり/きみとけんかしたの/きのうのよるに")
A2 = "ないたあとのそらは/すこしだけあかるい/ごめんねってめっせーじ/いまおくったんだ"
VB = ["R:1 6:0.5 6:0.5 6:1 5:1", "3:1 2:1 R:2", "R:1 6:0.5 6:0.5 6:1 5:1", "4:2 R:2",
      "R:1 1':0.5 1':0.5 1':1 7:1", "7:1 5:1 R:2", "R:1 1':0.5 2':0.5 3':1 2':1", "5:2 R:2"]
B1 = "かさのなかで/ふとおもう/あしたのそら/どんないろ"
B2 = "へんじがきた/ほらみてよ/あしたははれ/そのあとは"
VC = ["R:0.5 5:0.5 1':0.5 2':0.5 3':1 2':1", "2':1.5 1':0.5 7:1 R:1", "R:0.5 5:0.5 1':0.5 2':0.5 3':1 2':1", "3':1.5 2':0.5 1':1 R:1",
      "R:0.5 6:0.5 6:0.5 6:0.5 1':1 6:1", "5:1.5 4:0.5 3:1 R:1", "R:0.5 3:0.5 4:0.5 5:0.5 1':1 2':1", "1':2 R:2"]
VC16 = VC + VC[:6] + ["R:0.5 3:0.5 4:0.5 5:0.5 1':1 3':1", "1':2 R:2"]
TAGM = VC[:4] + ["R:0.5 3:0.5 4:0.5 5:0.5 1':1 3':1", "1':4", "R:4", "R:4"]
C1 = ("あしたのてんきは/はれのちはれるや/なみだのあめあと/にじがかかる/"
      "かさをたたんだら/きみにあいにいく/あのこうさてんで/はれるやだね")
C2 = ("あしたのてんきは/はれのちはれるや/ごめんのそのあと/そらがひらく/"
      "ふたりのよほうは/かならずあたるの/やさしいかぜふく/はれるやだね")
CL = C1 + "/はれるやはれるや/あしたはふたりで/はれるやだね"
VX = ["R:1 3:1 2:1 1:1", "6,:3 R:1", "R:1 4:1 3:1 2:1", "3:3 R:1", "R:1 6:1 5:1 4:1", "4:3 R:1", "R:1 #5:1 7:1 2':1", "1':3 R:1"]
X1 = "あめのひ/ふたりで/ひとつの/かさにね/ぬれたね/わらうの/だいじな/おもいで"
LY = Lyrics(S)


def put(name, key, lines, text, o=3):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA + VA, A1)
put("Bメロ1", K, VB, B1); put("Bメロ2", K, VB, B2)
put("サビ1", K, VC16, C1)
put("サビ2", K2, VC16, C2, o=4)
put("Cメロ", K2, VX + VX, X1, o=4)
put("最後のサビ", K3, VC16 + TAGM, CL, o=4)
if VOCAL: put("Aメロ2", K, VA, A2)
else:                                          # 歌なしの版: 2番の Aメロはフルートが歌う
    for b, l in zip(S.sc("Aメロ2"), VA): FL.bar(b, K.mel(l, oct=4))

# ================= 天気予報のチャイム（ベルのファンファーレ） =================
def chime(b, key, down=False):
    t = [key.deg(d, 5) for d in ("1", "3", "5", "1'")]
    if down: t = t[::-1]
    BELL.bar(b, " ".join(f"{x}:0.5" for x in t) + f" {t[-1]}:2")
    BELL.bar(b + 1, f"R:1 {t[2]}:0.5 {t[3]}:2.5")


bs = S.sc("天気予報のチャイム"); chime(bs[0], K); chime(bs[2], K)
chime(S.sc("サビ2")[0] - 2, K2)                   # Bメロ2 の最後の2小節（G7 の上で、ひと足先に）
bs = S.sc("チャイム2"); chime(bs[0], K3)
chime(S.sc("終わり")[2], K3); chime(S.sc("終わり")[4], K3, down=True)

# ================= フルートとトランペット =================
FL_I = ["R:0.5 F#5:0.5 G#5:0.5 A#5:0.5 B5:1 A#5:1", "G#5:1.5 F#5:0.5 D#5:2", "R:0.5 E5:0.5 F#5:0.5 G#5:0.5 B5:1 G#5:1", "F#5:3 R:1",
        "R:0.5 F#5:0.5 A#5:0.5 C#6:0.5 D#6:1 C#6:1", "B5:1.5 A#5:0.5 G#5:2", "R:0.5 G#5:0.5 F#5:0.5 E5:0.5 D#5:1 C#5:1", "A#4:3 R:1"]
for name in ("イントロ", "間奏"):
    for b, l in zip(S.sc(name), FL_I): FL.bar(b, l)
TPH = ["R:2.5 {a}:0.25 {a}:0.75 ", "{a}:0.5 R:0.5 {a}:0.5 R:2.5", "R:1.5 {a}:0.5 R:1 {a}:0.25 {a}:0.75", "R:3 {a}:0.5 {a}:0.5"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    # v2: v1 は BGM 7.50・歌 7.45。サビだけが 6.9〜7.2 と低かった（前奏・間奏・Cメロは 7.6〜7.8）→ サビを軽く:
    #   トランペットの合いの手は間奏と最後のサビの後半だけ、ハットは 16分の4つ打ちをやめて8分、弦はサビ2と最後のサビだけ
    if n == "間奏" or (n == "最後のサビ" and i >= 16 and i % 2 == 1):
        tv = voice(S.chords[b], 72, 2)
        for j in range(2): TP[j].bar(b, TPH[i % 4].format(a=nm(tv[j])).strip())

# ================= 伴奏 =================
COMP = ["{a}:0.75 {a}:0.75 R:0.5 {a}:0.5 R:0.5 {a}:1", "R:0.5 {a}:0.75 {a}:0.75 R:1 {a}:0.5 R:0.5", "{a}:1 R:0.5 {a}:0.75 {a}:0.75 R:1"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1"); v = voice(ch, 64, 4); t = tones(ch, "B3", "B5")
    if n == "天気予報のチャイム":
        if i >= 2:
            for j in range(4): PN[j].bar(b, f"{nm(v[j])}:4")
        continue
    if n == "終わり":
        if i < 3:
            for j in range(4): PN[j].bar(b, f"{nm(v[j])}:4" if i < 2 else f"{nm(v[j])}:12")
            BASS.bar(b, f"{nm(r)}:4" if i < 2 else f"{nm(r)}:12")
            VIB.bar(b, " ".join(f"{nm(x)}:0.5" for x in t[:4]) + " R:2")
        continue
    if n == "チャイム2":
        for j in range(4): PN[j].bar(b, f"{nm(v[j])}:4")
        BASS.bar(b, f"{nm(r)}:4")
        continue
    if n == "Cメロ":                                   # 雨の日: ピアノの和音をのばし、ピチカートが雨つぶ
        for j in range(4): PN[j].bar(b, f"{nm(v[j])}:2 {nm(v[j])}:2" if i >= 8 else f"{nm(v[j])}:4")
        PIZZ.bar(b, " ".join(f"{nm(t[(q * 3 + i) % len(t)] + 12)}:0.5" if q % 2 == 0 else "R:0.5" for q in range(8)))
        BASS.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2" if i >= 8 else f"{nm(r)}:4")
        if i >= 8:
            sv = voice(ch, 62, 3)
            for j in range(3): STR[j].bar(b, f"{nm(sv[j])}:4")
        continue
    chorus = n.startswith(("サビ", "最後"))
    for j in range(4): PN[j].bar(b, COMP[(i + (1 if chorus else 0)) % 3].format(a=nm(v[j])))
    # ベース: 根音と5度の跳ねる型（渋谷系の軽いベース）。サビは8分で歩く
    if chorus: BASS.bar(b, f"{nm(r)}:0.5 {nm(r + 12)}:0.5 {nm(r + 7)}:0.5 {nm(r + 12)}:0.5 {nm(r)}:0.5 {nm(r + 12)}:0.5 {nm(r + 7)}:0.5 {nm(r + 10 if '7' in ch and 'maj' not in ch else r + 9)}:0.5")
    else: BASS.bar(b, f"{nm(r)}:1.5 {nm(r + 7)}:0.5 R:0.5 {nm(r + 7)}:0.5 {nm(r + 12)}:1")
    # ピチカート: 8分の分散和音（Aメロ・Bメロ・イントロ）、サビは裏で
    if n.startswith(("Aメロ", "Bメロ", "イントロ")):
        PIZZ.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 1, 3, 2, 4, 3, 1)))
        PIZ2.bar(b, f"{nm(r + 24)}:1 R:1 {nm(r + 31)}:1 R:1")
    elif chorus:
        PIZZ.bar(b, " ".join(f"R:0.5 {nm(t[(q + 2) % len(t)])}:0.5" for q in range(4)))
    if n in ("サビ2", "最後のサビ"):
        sv = voice(ch, 67, 3)
        for j in range(3): STR[j].bar(b, f"{nm(sv[j])}:4")
    if chorus and i % 4 == 3:
        VIB.bar(b, "R:2 " + " ".join(f"{nm(x + 12)}:0.5" for x in t[:4]))
cym_swell(CYM, S.sc("サビ2")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 2, "E4")

# ================= ドラム（渋谷系: 軽い 16分のハット、2・4のスネア） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "天気予報のチャイム":
        if i == 3: D.set(b, "." * 16, "........X.X.XXXX", "." * 16)
        continue
    if n == "終わり":
        if i == 2: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 8)
        continue
    if n == "チャイム2":
        D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16) if i == 0 else put_fill(D, b, "build")
        if i == 0: crash(D, b, "C2", 4)
        continue
    if n == "Cメロ":
        if i >= 8: vgroove(D, b, "half", ghosts=0.1, seed=b, h="x.x.x.x.x.x.x.x.")
        continue
    chorus = n.startswith(("サビ", "最後"))
    if n.startswith(("Aメロ", "イントロ")):
        vgroove(D, b, "beat8", ghosts=0.2, seed=b, k="X.......X.x.....", h="x.xxx.xxx.xxx.xx")
    elif n.startswith("Bメロ"):
        vgroove(D, b, "beat8", ghosts=0.2, seed=b, k="X.....x.X.......", h="x.x.x.x.x.x.x.x.")
    else:
        vgroove(D, b, "beat8", ghosts=0.25, seed=b, k="X...X...X...X..." if chorus else None, h="x.x.x.x.x.x.x.x." if chorus else None)
    if i == 0 or (chorus and i % 8 == 0): crash(D, b, "C2", 4)
    if last and n not in ("Bメロ2",): put_fill(D, b, "snare16")
    elif chorus and i % 4 == 3: put_fill(D, b, "small")
    if n == "Bメロ2" and i >= 6: halt(D, b, 1 if i == 6 else 0)

SIL.add(S.sc("Cメロ")[-1], 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の22。渋谷系のポップス。B・136 → サビ2で C → 最後のサビで D♭（転調が2回）。"
          "けんかして心がくもりの子が、「ごめんね」を送って、明日は晴れのちハレルヤ。天気予報のチャイム（ベルのファンファーレ）が、"
          "曲の頭・転調の前・終わりに鳴る。ピチカートの弦、フルート、トランペットの合いの手、軽い 16分のハット、雨の日の Cメロ。自作")
finish(S, LY, V, 0, level={"verse": -0.25}, special={"Cメロ": -0.45, "最後のサビ": 0.5})
