# vb25 15「フライパン・オーケストラ」Frying Pan Orchestra（仮）— ヒップホップ（トラップ）。Cm（サビは E♭）・104（ハーフの型。倍の 208 で感じる）・4/4。
#   最後のサビは +2（F）
# 2026-10-25 作り直し: 物語を人の気持ちの話に（ひとり暮らしで母の味をまねる）、歌を人が歌える旋律に、テトの歌の版を足した。
#   テトの声に合うよう、曲全体を Gm から 7半音下げて Cm にした（書くのは Gm の度数のまま、書き出しの前に下げる）。
# 物語: ひとり暮らしの台所。母の手書きのレシピを開くと「塩少し」。少しってどのくらい？ 電話しようか迷いながら、包丁の音を聞いていると、
#   あの日の台所みたい。鍋がことこと、フライパンがじゅっと答えて、ひとりのオーケストラ。少しさみしいけれど、母の背中が見える気がする。
#   「いただきます」をひとりで言って、今度帰ったら作ってあげると決める。
# 場面と強さ: 包丁（打楽器だけ）→ レシピ（Aメロ・ラップのように語る）→ 火をつける（Bメロ・止め）→ じゅうじゅう（サビ）→ お湯がわくまで（静けさ）
#   → 2品目（BGM はピッツィカートが歌を受け取る）→ 強火（Bメロ）→ サビ2（倍のノリ）→ 鍋のソロ → 1拍の無音 → 全部の鍋（+2）→ 盛りつけ → いただきます
# 旋律の性格: Aメロは低め（B♭3〜A♭4）で、16分の2つ組と3連で語る。サビは「じゅうじゅう」の16分の2つ組で入る。最高音 F5。
# ほかの曲とちがう所: 台所の音（包丁・鍋・ふた・泡）が楽器。トラップのハットと 808、ピッツィカート。
from vb25_lib import *

S = Song("15", "frypan", "フライパン・オーケストラ（仮）", "Frying Pan Orchestra", 104, 4, "G", "minor", "ヒップホップ（トラップ・ボカロ）")
S.kit = "electro"
S.flags = "--ref-tone glossy-jrock " + S.flags + " --piano salamander"
S.keep_old_synth = True
K = S.key                    # G の短調
KB = Key("Bb", "major")      # サビ（平行調）
KC = Key("C", "major")       # 最後のサビ（+2）
KAm = Key("A", "minor")

A_CH = ["Gm", "F", "Ebmaj7", "Ab"]
B_CH = ["Cm7", "D7", "Ebmaj7", "F", "Cm7", "D7", "Ebmaj7", "D7"]
C_CH = ["Ebmaj7", "F", "Dm7", "Gm7", "Ebmaj7", "F", "Bb", "Bbaug"]
C_CH2 = ["Ebmaj7", "F/A", "Bb", "G7", "Cm7", "F7", "Bb", "D7"]
WAIT = ["Gm7", "Ebmaj7", "Cm7", "D7sus4", "Gm7", "Ebmaj7", "Abmaj7", "D7"]
LAST = [tr_chord(c, 2) for c in C_CH] + [tr_chord(c, 2) for c in C_CH2[:6]] + ["Dm7", "G7"]

S.scene("包丁", 8, "intro", A_CH)
S.scene("下ごしらえ", 16, "verse", A_CH)
S.scene("火をつける", 8, "pre", B_CH)
S.scene("鍋がそろう", 16, "chorus", C_CH + C_CH2)
S.scene("お湯がわくまで", 8, "break", WAIT)
S.scene("2品目", 8, "verse", A_CH)
S.scene("火を強く", 8, "pre", B_CH)
S.scene("強火", 16, "chorus", C_CH + C_CH2)
S.scene("鍋のソロ", 8, "solo", A_CH[:3] + ["D7"])
S.scene("全部の鍋", 16, "chorus", LAST)
S.scene("盛りつけ", 4, "outro", ["Fmaj7", "G", "Em7", "Am7"])
S.scene("いただきます", 2, "outro", ["Cmaj9", "Cmaj9"])

V = Voice(S, vol=0.22, delay=0.75, patch="picoLead", low=True)   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
PZS = dict(patch="pizzicato", volume=0.12, pan=0.35, reverb=0.3, sustain=0.6)
PZ = [S.track(f"ピッツィカート{i + 1}", "strings", **PZS) for i in range(2)]
PZM = S.track("ピッツィカート（歌の受け渡し）", "strings", **PZS)
B808 = S.track("808", "sub808", volume=0.2, pan=0, sustain=1.0, fx=[{"type": "filter", "kind": "highpass", "freq": 30, "q": 0.7},
                                                                        {"type": "eq", "low": -2, "mid": 3, "midHz": 900, "high": 0}])
KNIFE = S.track("包丁とまな板（カホン）", "cajon", volume=0.14, pan=-0.3, reverb=0.12)
POT = S.track("鍋（大小のロートタム）", "rotoTom", patch="rotoTom", volume=0.13, pan=0.15, reverb=0.2)
LID = S.track("鍋のふた（短いベル）", "pad", patch="surgeBell1", volume=0.045, pan=-0.45, reverb=0.15, sustain=0.25,
              fx=[{"type": "filter", "kind": "highpass", "freq": 900, "q": 0.7}])
GLS = S.track("グラスの音（泡）", "pad", patch="surgeChordXyloChill", volume=0.055, pan=0.5, sustain=0.6, reverb=0.45,
              fx=[{"type": "filter", "kind": "highpass", "freq": 600, "q": 0.7}])
SAW = [S.track(f"厚い和音{i + 1}", "pad", **pad_spec("surgeChordMg", vol=0.05, pan=-0.5, duck=0.4, sustain=0.9)) for i in range(3)]
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の旋律と歌詞（G の短調の度数・oct 4 で 1 = G4。サビは B♭長調、最後は C長調 oct 5。書き出しの前に全体を 7半音下げる） =================
Pa = ["R:0.5 1:0.25 1:0.25 3:0.5 1:0.5 4:0.3333 3:0.3333 1:0.3334 3:1", "2:0.5 1:0.5 7,:1 R:2"]
Pb = ["R:0.5 3:0.25 3:0.25 5:0.5 3:0.5 4:0.3333 3:0.3333 1:0.3334 3:1", "b2:0.5 3:0.5 4:1 R:2"]
Pa2 = ["R:0.5 5:0.25 5:0.25 4:0.5 3:0.5 1:0.3333 3:0.3333 4:0.3334 5:1", "4:0.5 2:0.5 7,:1 R:2"]
Pb2 = ["R:0.5 5:0.25 5:0.25 3:0.5 5:0.5 6:0.3333 5:0.3333 3:0.3334 5:1", "4:0.5 b2:0.5 4:1 R:2"]
VA = Pa + Pb + Pa2 + Pb2 + Pa + Pb + Pa2 + Pb2
V1 = "ひとりぐらしのだいどこ/ははのれしぴをひらいて/てがきのもじがやさしい/しおすこしとかいてある/すこしってどのくらいなの/でんわしようかなまよって/ほうちょうのおとがひびく/あのひのだいどころだね"
V2 = "なべがことことうたうよ/ふらいぱんじゅっとこたえる/ひとりのおーけすとらだ/すこしだけさみしいけど"
VB = ["R:0.5 4:0.5 4:0.5 6:0.5 1':1 7:1", "#7:1 5:1.5 R:1.5", "R:0.5 6:0.5 6:0.5 1':0.5 3':1 2':1", "1':1 7:1.5 R:1.5",
      "R:0.5 4:0.5 4:0.5 6:0.5 1':1 3':1", "2':1 #7:1.5 R:1.5", "R:0.5 6:0.5 1':0.5 3':0.5 4':1 3':1", "#7:1 R:3"]
P1 = "ひをつけたらね/あぶらがはねる/てがきのめもを/みつめながら"
P2 = "ひをつよくして/いきおいよくね/ははのくちぐせ/おもいだすよ"
VC = ["R:0.5 5:0.25 5:0.25 5:0.5 6:0.5 1':1 6:1", "5:1 4:1.5 R:1.5",
      "R:0.5 3:0.25 3:0.25 3:0.5 4:0.5 6:1 5:1", "6:1 5:1.5 R:1.5",
      "R:0.5 5:0.25 5:0.25 5:0.5 6:0.5 1':1 2':1", "1':1 6:1.5 R:1.5",
      "R:0.5 1':0.5 2':0.5 1':0.5 6:1 5:1", "#5:2 R:2",
      "R:0.5 5:0.25 5:0.25 5:0.5 6:0.5 1':1 6:1", "5:1 4:1.5 R:1.5",
      "R:0.5 3:0.25 3:0.25 3:0.5 5:0.5 1':1 7:1", "6:1 3:1.5 R:1.5",
      "R:0.5 2':0.25 2':0.25 2':0.5 1':0.5 6:1 4:1", "5:1 3:1.5 R:1.5",
      "1':1.5 6:0.5 5:1 3:1", "#5:1 7:1 #5:1 R:1"]
VCL = [x.replace("2':", "1':") for x in VC]          # 最後のサビ（+2）はテトの高さに収める
C1 = "じゅうじゅうはねるよ/ふらいぱんのうた/ことこととなべが/こたえてるよ/あのひのあじへと/ちかづいていくよ/ひとりきりなのに/にぎやかなんだ"
C2 = "じゅうじゅうはねるよ/つよびにしたらね/においがへやじゅう/ひろがるのよ/ははのせなかがね/みえるきがしたよ/おなじあじだよと/いいたいんだよ"
CL = "/".join(C1.split("/")[:4]) + "/いただきますってね/ひとりでいうんだ/いつかかえったらね/つくってあげよう"
VW = ["5:3 4:1", "3:3 R:1", "4:2 6:2", "5:3 R:1", "1':3 7:1", "5:3 R:1", "b2':2 1':1 6:1", "#7:2 R:2"]
VTAG = ["3:1 5:1 6:2", "7:1 5:1 1':2", "1':1.5 7:0.5 5:1 3:1", "6:4"]
LY = Lyrics(S)
def put(name, key, lines, text, low=True, o=4):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m, low=low)
    LY.flow(bars, mel, text, name)
put("下ごしらえ", K, VA, V1)
if VOCAL: put("2品目", K, VA[:8], V2)
else:
    for i, b in enumerate(S.sc("2品目")):
        if i < 4: PZM.bar(b, K.mel(VA[i], oct=5))                  # BGM: 前半はピッツィカートが歌を受け取る
        else: V.bar(b, K.mel(VA[i], oct=4))
put("火をつける", K, VB, P1); put("火を強く", K, VB, P2)
put("鍋がそろう", KB, VC, C1); put("強火", KB, VC, C2)
put("全部の鍋", KC, VCL, CL, o=5)
put("盛りつけ", KC, VTAG, "もりつけたらできあがり", o=5)
put("いただきます", KC, ["3:0.5 5:0.5 6:0.5 5:0.5 3:0.5 1':1.5", "R:4"], "いただきます", o=5)
put("お湯がわくまで", K, VW, "まってて/まってて/ゆげが/あがるよ", low=False)


# ================= 鍋のソロ（大小の鍋＝ロートタムが旋律を叩く） =================
POTS = {"大": "F2", "中": "A2", "小": "C3", "ちび": "D#3", "片手": "F3", "ミルク": "A3"}
PS = ["F2:0.5! C3:0.25 C3:0.25 A2:0.5 F3:0.25 F3:0.25 D#3:0.5 C3:0.5 A3:0.5 F3:0.5",
      "A2:0.5! D#3:0.25 D#3:0.25 C3:0.5 A3:0.25 A3:0.25 F3:0.5 D#3:0.25 C3:0.25 A2:0.5 F2:0.5",
      "F2:0.25! F2:0.25 C3:0.25 F3:0.25 A3:0.25 F3:0.25 C3:0.25 F2:0.25 F2:0.25 A2:0.25 D#3:0.25 A3:0.25 F3:0.5 C3:0.5",
      "A3:0.25! A3:0.25 F3:0.25 F3:0.25 D#3:0.25 D#3:0.25 C3:0.25 C3:0.25 A2:0.25 A2:0.25 F2:0.25 F2:0.25 F2:1"]
for i, b in enumerate(S.sc("鍋のソロ")): POT.bar(b, PS[i % 4] if i < 7 else PS[3])
# 鍋は、サビの合いの手（4小節目ごと）と、包丁の場面にも
for name in ("鍋がそろう", "強火", "全部の鍋"):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3: POT.bar(b, "R:2.5 A3:0.25 F3:0.25 D#3:0.25 C3:0.25 A2:0.5")
for i, b in enumerate(S.sc("包丁")):
    if i == 7: POT.bar(b, "R:2 F3:0.5 D#3:0.5 C3:0.5 F2:0.5")

# 包丁とまな板（カホンのスラップと胴）
KN = ["E3:0.25! F3:0.25, E3:0.25 F3:0.25, E3:0.25! F3:0.25, D3:0.25 F3:0.25, E3:0.25! F3:0.25, E3:0.25 F3:0.25, E3:0.25! E3:0.25 D3:0.5",
      "E3:0.25! F3:0.25, E3:0.25 F3:0.25, E3:0.25! R:0.25 D3:0.25 F3:0.25, E3:0.25! F3:0.25, E3:0.25 F3:0.25, E3:0.25! F3:0.25 E3:0.25 E3:0.25"]
for i, b in enumerate(S.sc("包丁")): KNIFE.bar(b, KN[i % 2] if i < 6 else ("A2:1! " + KN[1].split(" ", 4)[-1] if i == 6 else KN[0]))
for name in ("下ごしらえ", "2品目"):
    for i, b in enumerate(S.sc(name)):
        if i % 2 == 0: KNIFE.bar(b, "R:3 E3:0.25! F3:0.25, E3:0.25 E3:0.25")
# 鍋のふた（短い FM ベル）: サビの裏拍
for name in ("鍋がそろう", "全部の鍋", "鍋のソロ"):
    for i, b in enumerate(S.sc(name)):
        LID.bar(b, "R:0.5 D6:0.5 R:0.5 D6:0.5 R:0.5 D6:0.5 R:0.75 G6:0.25" if i % 2 else "R:0.5 D6:0.5 R:0.5 D6:0.5 R:0.5 D6:0.5 R:0.5 D6:0.5")

# グラスの音（お湯の泡がだんだん増える）
rnd = random.Random(15)
for i, b in enumerate(S.sc("お湯がわくまで")):
    ts = tones(S.chords[b], "C6", "C7")
    n_ = 1 + i
    for j in range(n_):
        st = rnd.choice([x * 0.5 for x in range(8)])
        GLS.at(S.bar_beat(b) + st, f"{nm(rnd.choice(ts))}:0.5")
for i, b in enumerate(S.sc("鍋がそろう") + S.sc("全部の鍋")):
    if i % 8 == 7: GLS.bar(b, " ".join(f"{nm(m)}:0.25" for m in tones(S.chords[b], "C6", "C7")[:4]) + " R:3")

# ================= ピッツィカート（和音の分散） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "包丁" and i < 2: continue
    if n in ("いただきます",): continue
    t = tones(ch, "G3", "G5")
    if n in ("包丁", "下ごしらえ", "鍋のソロ") or (n == "2品目" and i >= 4):
        seq = [t[q % len(t)] for q in (0, 2, 1, 3, 2, 4, 3, 1)]
        PZ[0].bar(b, " ".join(f"{nm(m)}:0.5" for m in seq))
    elif n.startswith("火を"):
        v = voice(ch, 64, 2)
        for j in range(2): PZ[j].bar(b, " ".join(f"{nm(v[j])}:0.5" for _ in range(8)) if i < 7 else f"{nm(v[j])}:1 R:3")
    elif n == "お湯がわくまで":
        PZ[0].bar(b, f"{nm(t[0])}:1 R:1 {nm(t[2 % len(t)])}:1 R:1")
    elif n == "2品目":
        v = voice(ch, 60, 2)
        for j in range(2): PZ[j].bar(b, f"{nm(v[j])}:1 R:1 {nm(v[j])}:0.5 R:1.5")
    elif n in ("鍋がそろう", "強火", "全部の鍋", "盛りつけ"):
        seq = [t[q % len(t)] for q in (0, 1, 2, 3, 2, 1, 3, 4)]
        PZ[0].bar(b, " ".join(f"{nm(m)}:0.25" for m in seq) + " " + " ".join(f"{nm(m)}:0.5" for m in seq[:4]))

# 厚い和音（サビだけ）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n in ("鍋がそろう", "強火", "全部の鍋", "盛りつけ", "いただきます"):
        v = voice(S.chords[b], 62, 3)
        if n == "いただきます":
            if i == 0:
                for j in range(3): SAW[j].bar(b, f"{nm(v[j])}:6")
            continue
        for j in range(3): SAW[j].bar(b, f"{nm(v[j])}:1.5 {nm(v[j])}:1 {nm(v[j])}:1.5" if n != "強火" else f"{nm(v[j])}:4")

# ================= 808（キックの位置から長く鳴る） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "C1")
    if r < midi("D1"): r += 12
    if n == "包丁":
        if i >= 4: B808.bar(b, f"{nm(r)}:1.5! {nm(r)}:1 {nm(r)}:1.5")
    elif n in ("下ごしらえ", "2品目", "鍋のソロ"):
        B808.bar(b, f"{nm(r)}:1.5! {nm(r)}:0.5 {nm(r + 12)}:0.5 {nm(r)}:1.5" if i % 2 == 0 else f"{nm(r)}:2.5! {nm(r + 7)}:0.5 {nm(r)}:1")
    elif n.startswith("火を"):
        B808.bar(b, f"{nm(r)}:2! {nm(r)}:2" if i < 7 else f"{nm(r)}:1! R:3")
    elif n in ("鍋がそろう", "全部の鍋", "盛りつけ"):
        B808.bar(b, f"{nm(r)}:1.5! {nm(r)}:0.5 {nm(r)}:0.5 {nm(r + 12)}:0.5 {nm(r)}:1")
    elif n == "強火":
        B808.bar(b, " ".join(f"{nm(r + (12 if q % 2 else 0))}:0.5" for q in range(8)))       # 倍のノリ: 8分のオクターブ
    elif n == "お湯がわくまで":
        if i % 2 == 0: B808.bar(b, f"{nm(r)}:4")
    elif n == "いただきます" and i == 0:
        B808.bar(b, f"{nm(low('C', 'C1') + 12)}:6")

# 効果音
riser(FX, S.sc("鍋がそろう")[0], 4, "C4"); riser(FX, S.sc("強火")[0], 4, "C4")
FX.bar(S.sc("お湯がわくまで")[0], "G4:4")                    # 火を止めた「ドーン」
cym_swell(CYM, S.sc("全部の鍋")[0], 4, "E4"); cym_swell(CYM, S.sc("鍋のソロ")[0], 2, "C4")

# ================= ドラム（電子のドラム・トラップ） =================
TRAPH = ["xxxxxxxxxxxxXxXx", "x.x.xxxxx.x.XXXX", "xxxxx.x.xxxxx.xx", "x.x.x.x.xxxxXXXX"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "包丁":
        if i >= 4: vgroove(D, b, "trap", ghosts=0, seed=b, h=TRAPH[i % 4], vary=False)
        if i == 4: crash(D, b, "G2")
    elif n in ("下ごしらえ", "2品目"):
        vgroove(D, b, "trap", ghosts=0.2, seed=b, h=TRAPH[i % 4], vary=False,
                k="X.......X.X....." if i % 2 == 0 else "X.....X...X..X..")
        if i == 0: crash(D, b)
        if i % 8 == 7: put_fill(D, b, "small")
    elif n.startswith("火を"):
        vgroove(D, b, "halfdrive", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 1)
    elif n in ("鍋がそろう", "全部の鍋"):
        vgroove(D, b, "trap", ghosts=0.2, seed=b, h=TRAPH[(i + 1) % 4], vary=False,
                k="X.......X.X....." if i % 4 != 3 else "X.....X.X...X.X.")
        if i % 8 == 0: crash(D, b, "C2" if i == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "tomdown")
        if last and n == "鍋がそろう": D.set(b, "X.......X.......", "........X.......", "x.x.x.x.x.x.....")
    elif n == "強火":
        # サビごとのリズムの入れかえ: 倍のノリ（208 で感じるドラムンベース型）
        vgroove(D, b, "dnb", ghosts=0.35, seed=b, s="....X..o.o..X...")
        if i % 8 == 0: crash(D, b, "C2")
        if i % 4 == 3 and not last: put_fill(D, b, "snare16")
        if last: D.set(b, "X...............", "X...............", "................")
    elif n == "お湯がわくまで":
        D.set(b, "X......." * 2 if i >= 4 else "X" + "." * 15, "." * 16, "x...x...x...x..." if i >= 2 else "." * 16)
        if last: put_fill(D, b, "lift")
    elif n == "鍋のソロ":
        vgroove(D, b, "trap", ghosts=0.3, seed=b, h="x.x.x.x.x.x.x.x.", vary=False)
        D.cym(b, ("B2:1 " if i == 0 else "D2:1 ") + "D2:1 D2:1 D2:1"); D.H[b] = "." * 16      # ライド
        if last: put_fill(D, b, "tomtrip")
    elif n == "盛りつけ":
        vgroove(D, b, "trap", ghosts=0.2, seed=b, h=TRAPH[i % 4], vary=False)
        if i == 0: crash(D, b, "G2")
        if last: put_fill(D, b, "snare16")
    elif n == "いただきます":
        if i == 0: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 8)

# 止め: 火をつける・火を強くの最後の小節（1拍だけ叩いて全員休み）。1拍の完全な無音: 最後のサビの直前
for name in ("火をつける", "火を強く"): SIL.add(S.sc(name)[-1], 1, 4)
SIL.add(S.sc("全部の鍋")[0] - 1, 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の15。ヒップホップ（トラップ）。Cm（サビは E♭）・104、最後のサビは +2（F）。"
          "ひとり暮らしの台所で、母の手書きのレシピの味をまねる。包丁の音で始まり、ラップのように語る Aメロ、止めのある Bメロ、「じゅうじゅう」のサビ、お湯がわくまでの静けさ、"
          "倍のノリの2サビ、鍋のソロ、1拍の無音から +2 の最後のサビ、盛りつけ、「いただきます」の和音。台所の音・808・ピッツィカート。自作")
S.no_depth = True
teto(S, LY, V, transpose=-7, level={"verse": -0.2}, special={"全部の鍋": 0.55, "お湯がわくまで": -0.55, "盛りつけ": 0.0, "いただきます": -0.2})
