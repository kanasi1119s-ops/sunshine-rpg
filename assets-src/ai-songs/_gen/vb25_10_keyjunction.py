# vb25 10「鍵盤ジャンクション」Keyboard Junction（仮）— ロック（ピアノロック）。B長調・184・4/4
# 転調（2段）: 1番は B → 2番のサビで半音下げて B♭ → 最後のサビで、もとの B から短3度上げて D（直前に1拍の無音）
# 2026-10-25 作り直し: 物語を人の気持ちの話に（人見知りがピアノで人とつながる）、歌を人が歌える旋律（8分と4分）に、テトの歌の版を足した。
#   テトの声に合うよう、曲全体を F長調から 6半音下げて B長調にした（書くのは F長調の度数のまま、書き出しの前に下げる）。
# 物語: 駅前の古いストリートピアノ。人見知りの「ぼく」が、夕暮れにひとりでそっとふたを開ける。指がふるえて音が出ない。
#   1音目からゆっくり弾くと、通りの人が足をとめ、知らない人が隣に座って、何も言わずに弾きはじめる。名前も知らないまま、同じ音を鳴らす。
#   ひとり、またひとりと座って、最後は6人の連弾。「ひとりじゃないんだね」。
# 場面と強さ: 1音（ピアノの単音）→ 1人きり（ピアノだけで主題）→ 2人目（バンドが入る）→ Aメロ → Bメロ（溜め・止め）→ サビ
#   → 掛け合い（ピアノ2台）→ 2番（BGM はピアノが歌を受け取る）→ 2番のサビ（半音下）→ 隣に座る（歌とピアノが2小節ずつ受け渡す → Half feel）
#   → ピアノのソロ → 6人目（1拍の無音）→ 6人連弾の大サビ（短3度上・最大）→ ピアノだけ残る
# 旋律の性格: Aメロは句の頭を休む8分。サビは同じ音を3つ置いてから4度上へ跳ぶ。最高音 F#5。
# ほかの曲とちがう所: 主役はピアノ（2台・掛け合い・ソロ）。2段の転調。歌とピアノが旋律を受け渡す。
from vb25_lib import *

S = Song("10", "keyjunction", "鍵盤ジャンクション（仮）", "Keyboard Junction", 184, 4, "F", "major", "ピアノロック（ボカロ）")
S.kit = "crocell-punch"
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags + " --piano salamander"
S.extra.update({"tone": "rock"})
K = S.key                 # F
KE = Key("E", "major")    # 2番のサビ（半音下げ）
KA = Key("Ab", "major")   # 最後のサビ（もとの F から短3度上げ）
trs = lambda cs, n: [tr_chord(c, n) for c in cs]

INTRO = ["Fmaj7", "C/E", "Dm7", "Bbmaj7", "Gm7", "C7sus4", "Fmaj7", "C7"]
A_CH = ["Dm7", "Bbmaj7", "C", "Am7", "Dm7", "Bbmaj7", "Gm7", "C7"]                  # i–♭VI–♭VII–v（平行調の短調で）
B_CH = ["Bbmaj7", "C", "Am7", "Dm7", "Gm7", "A7", "Bbmaj7", "C7sus4"]               # A7＝vi への副属和音
C_CH = ["Bbmaj7", "A7", "Dm7", "Dm7/C", "Bbmaj7", "C", "C#dim", "Dm7"]              # IVM7–III7–vi・vi へ入る減三和音 C#dim
C_CH2 = ["Bbmaj7", "A7", "Dm7", "Cm7", "Bbmaj7", "C7", "Fmaj7", "Fmaj7"]           # Cm7＝同主調から借りた v
DUEL = ["Fmaj7", "C/E", "Dm7", "Bbmaj7", "Gm7", "Am7", "Bbmaj7", "C7"]
SIT = ["C#m7", "Amaj7", "B/D#", "E", "C#m7", "Amaj7", "F#m7", "B7sus4",
       "Amaj7", "G#7", "C#m7", "C#m7/B", "Amaj7", "F#m7", "G#m7", "B7"]
SOLO_CH = ["Emaj7", "B/D#", "C#m7", "Amaj7", "F#m7", "G#7", "C#m7", "B7"]
SIX = ["C#m7", "Amaj7", "F#m7", "B7sus4", "Amaj7", "B", "Bbm7", "Eb7"]
END8 = ["Bbmaj7", "C/Bb", "Am7", "Dm7", "Gm7", "C7sus4", "Fmaj7", "Fmaj7"]

S.scene("1音", 4, "intro", ["F"] * 4)
S.scene("1人きり", 8, "intro", C_CH)
S.scene("2人目", 8, "intro", INTRO)
S.scene("Aメロ", 16, "verse", A_CH)
S.scene("Bメロ", 8, "pre", B_CH)
S.scene("サビ", 16, "chorus", C_CH + C_CH2)
S.scene("掛け合い", 8, "interlude", DUEL)
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", trs(C_CH + C_CH2, -1))
S.scene("掛け合い2", 8, "interlude", trs(DUEL, -1))
S.scene("隣に座る", 16, "bridge", SIT)
S.scene("ピアノのソロ", 16, "solo", SOLO_CH)
S.scene("6人目", 8, "build", SIX)
S.scene("6人連弾", 24, "chorus", trs(C_CH + C_CH2 + END8, 3))
S.scene("ピアノだけ残る", 8, "outro", ["Dbmaj7", "Cm7", "Bbm7", "Ebsus4", "Dbmaj7", "Eb/Db", "Abmaj7", "Abmaj7"])

V = Voice(S, vol=0.22, delay=0.75, patch="violin", low=True)   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
PL = [S.track("ピアノ1台目（右手）", "piano", **piano_spec(0.12, -0.35, 0.22)), S.track("ピアノ1台目（左手）", "piano", **piano_spec(0.12, -0.35, 0.22))]
PR = [S.track(f"ピアノ2台目（和音{i + 1}）", "piano", **piano_spec(0.1, 0.35, 0.22)) for i in range(3)]
PRH = S.track("ピアノ2台目（高いきらめき）", "piano", **piano_spec(0.1, 0.35, 0.22))
PM = S.track("ピアノ（主旋律の受け渡し）", "piano", **piano_spec(0.17, 0.0, 0.22))
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.21))
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 旋律と歌詞（F長調の度数。oct=4 で 1 = F4。書き出しの前に全体を 6半音下げる） =================
VERSE = ["R:1 6:0.5 6:0.5 5:0.5 3:0.5 2:1", "1:1 2:1.5 R:1.5",
         "R:1 3:0.5 3:0.5 5:0.5 3:0.5 2:1", "3:2 R:2",
         "R:1 6:0.5 6:0.5 1':0.5 6:0.5 5:1", "4:1 3:1.5 R:1.5",
         "R:1 2:0.5 2:0.5 4:0.5 5:0.5 6:1", "5:2 R:2",
         "R:1 1':0.5 1':0.5 7:0.5 6:0.5 5:1", "4:1 6:1.5 R:1.5",
         "R:1 5:0.5 5:0.5 6:0.5 5:0.5 3:1", "5:2 R:2",
         "R:1 6:0.5 1':0.5 2':0.5 1':0.5 6:1", "4:1 5:1.5 R:1.5",
         "R:1 4:0.5 3:0.5 2:0.5 1:0.5 2:1", "5:2 R:2"]
V1 = "えきまえにある/ふるいぴあの/だれもいないの/ゆうぐれどき/ひとりでそっとね/ふたをあけた/ゆびがふるえて/おとがでない"
V2 = "いちおんめから/ゆっくりひいた/とおりのひとが/あしをとめた/しらないひとが/となりにきた/なにもいわずに/ひきはじめた"
BM = ["4:1 6:0.5 1':0.5 6:1 5:1", "5:1 7:0.5 2':0.5 1':1 R:1", "7:1 5:0.5 3:0.5 5:1 7:1", "6:2 R:1 6:0.5 1':0.5",
      "2':1 4':0.5 2':0.5 1':1 2':1", "#5:0.5 7:0.5 3':1 2':1 R:1", "1':1 2':1 4':2", "2':2 R:2"]
P1 = "ひとつのおとからね/ふたつになる/しらないひとのゆびがね/かさなる"
P2 = "なまえもしらないね/それでもいい/おなじおとをならしてる/それだけ"
CH1 = ["R:0.5 1':0.5 1':0.5 1':0.5 4':1.5 3':0.5", "2':1 7:0.5 #5:0.5 3':2", "R:0.5 3':0.5 3':0.5 3':0.5 5':1 3':1", "2':1 1':0.5 6:0.5 1':2",
       "R:0.5 6:0.5 1':0.5 2':0.5 4':1 2':1", "3':1.5 2':0.5 1':1 R:1", "#5:0.5 7:0.5 2':1 7:1 #5:1", "6:3 R:1"]
CH1b = [CH1[0], "2':1 7:0.5 #5:0.5 3':1 2':1", "R:0.5 3':0.5 3':0.5 3':0.5 4':1 3':1", "2':1.5 1':0.5 b7:1 5:1",
        "R:0.5 4':0.5 4':0.5 4':0.5 5':1 4':1", "3':1 2':1 1':1.5 R:0.5", "3':2 1':1 5:1", "1':4"]
CH2 = CH1[:6] + ["#5:0.5 7:0.5 2':0.5 3':0.5 2':1 7:1", "6:2 R:2"]
CH2b = CH1b[:6] + ["3':1 2':0.5 1':0.5 2':2", "1':2 R:2"]
CHL = ["R:0.5 1':0.5 1':0.5 1':0.5 3':1.5 2':0.5", "2':1 7:0.5 #5:0.5 3':2", "R:0.5 3':0.5 3':0.5 3':0.5 2':1 1':1", "2':1 1':0.5 6:0.5 1':2",
       "R:0.5 6:0.5 1':0.5 2':0.5 3':1 2':1", "3':1.5 2':0.5 1':1 R:1", "#5:0.5 7:0.5 2':1 7:1 #5:1", "6:3 R:1",
       "R:0.5 1':0.5 1':0.5 1':0.5 3':1.5 2':0.5", "2':1 7:0.5 #5:0.5 3':1 2':1", "R:0.5 3':0.5 3':0.5 3':0.5 2':1 3':1", "2':1.5 1':0.5 b7:1 5:1",
       "R:0.5 2':0.5 2':0.5 2':0.5 3':1 2':1", "3':1 2':1 1':1.5 R:0.5", "3':2 1':1 5:1", "1':3 R:1",
       "4:1 6:0.5 1':0.5 3':2", "2':1 1':0.5 7:0.5 5:1.5 R:0.5", "3':1 7:1 5:1 3:1", "6:1 1':1 3':1.5 R:0.5",
       "2':1.5 1':0.5 6:1 4:1", "5:2 2':2", "1':4", "R:4"]
C1 = "ひとりじゃないんだね/かさなるおとがほら/しらないままでも/わかりあえる/けんばんのうえでいま/であえたぼくらはね/ひとつのうたへと/とけてく"
C2 = "ひとりじゃないんだね/かさなるおとがほら/しらないままでも/わかりあえるよ/けんばんのうえでいま/であえたぼくらはね/ひとつのうたへと/とけてゆく"
CLV = C1 + "/ろくにんのおとで/まちがうたうよ/またあしたもね"
SITV = ["6:2 5:1 3:1", "4:3 R:1", "5:0.5 6:0.5 7:0.5 2':0.5 1':1 7:1", "5:4",
        "3:1 5:1 6:1 1':1", "7:2 6:2", "2':0.5 1':0.5 6:0.5 4:0.5 2:1 4:1", "5:2 R:2",
        "1':2 7:1 6:1", "7:1 #5:1 3':1 R:1", "3':1 1':1 6:2", "5:3 R:1", "4:1 6:1 1':1 3':1", "4':2 3':1 R:1", "3':1 5':1 3':1 2':1", "2':2 R:2"]
SITW = "となりに/すわるひとに/はじめまして/いえたら/ことばよりも/おとがいう"
LY = Lyrics(S)
def put(name, key, lines, text, low=True):
    bars = S.sc(name); mel = [key.mel(x, oct=4) for x in lines]
    for i, (b, m) in enumerate(zip(bars, mel)): V.bar(b, m, low=low if not callable(low) else low(i))
    LY.flow(bars, mel, text, name)
put("Aメロ", K, VERSE, V1)
if VOCAL: put("Aメロ2", K, VERSE, V2)
else:
    for i, b in enumerate(S.sc("Aメロ2")):
        line = K.mel(VERSE[i], oct=4)
        if i < 8: PM.bar(b, shift_oct(line, 1))                   # BGM: 2番の前半は、ピアノが歌を受け取る
        else: V.bar(b, line)
put("Bメロ", K, BM, P1); put("Bメロ2", K, BM, P2)
put("サビ", K, CH1 + CH1b, C1); put("サビ2", KE, CH2 + CH2b, C2); put("6人連弾", KA, CHL, CLV)
# 1音・1人きり: ピアノの単音から、サビの主題をピアノだけで（ゆっくり、すき間を残して）
ONE = ["1':1 R:1 5:2", "3':1 R:1 2':2", "1':1 R:0.5 5:0.5 6:2", "5:3 R:1"]
for i, b in enumerate(S.sc("1音")): PM.bar(b, K.mel(ONE[i], oct=4))
for i, b in enumerate(S.sc("1人きり")): PM.bar(b, K.mel(CH1[i], oct=4))
# 隣に座る（E）: 2小節ずつ、歌 → ピアノ → 歌 → ピアノ。後半は Half feel で歌が上がる
vb, vm = [], []
for i, b in enumerate(S.sc("隣に座る")):
    line = KE.mel(SITV[i], oct=4)
    if i < 8 and (i // 2) % 2 == 1: PM.bar(b, shift_oct(line, 1))
    else: V.bar(b, line, low=(i >= 8)); vb.append(b); vm.append(line)
LY.flow(vb, vm, SITW, "隣に座る")
# 6人目: 歌が D（もとの A♭）へ導く
SIXL = [KE.mel("3:2 5:2", oct=4), KE.mel("6:2 7:1 1':1", oct=4), KE.mel("2':2 1':1 6:1", oct=4), KE.mel("7:3 R:1", oct=4),
        KE.mel("1':2 2':2", oct=4), KE.mel("3':2 2':1 1':1", oct=4), KA.mel("2':2 1':1 6:1", oct=4), KA.mel("5:2 7:1 R:1", oct=4)]
for i, b in enumerate(S.sc("6人目")): V.bar(b, SIXL[i], low=(i >= 4))
LY.flow(S.sc("6人目"), SIXL, "ひとりまたひとりと/ろくにんめがすわったよ", "6人目")
# ピアノだけ残る
for i, b in enumerate(S.sc("ピアノだけ残る")):
    if i < 6: PM.bar(b, KA.mel(["3':2 2':1 1':1", "7:3 R:1", "6:2 1':2", "2':4", "4':2 3':1 1':1", "2':4"][i], oct=4))


# ================= ピアノのリフ・掛け合い・ソロ =================
RIFF = ["5':0.5 3':0.5 1':0.5 5:0.5 3':0.5 2':0.5 1':1", "7:0.5 1':0.5 3':0.5 5':0.5 3':1 2':1",
        "1':0.25 2':0.25 3':0.25 1':0.25 6:0.5 1':0.5 4':1 3':1", "2':0.5 1':0.5 6:0.5 4:0.5 6:2",
        "4':0.5 2':0.5 7:0.5 5:0.5 2':0.5 1':0.5 7:1", "3':0.5 1':0.5 6:0.5 3:0.5 1':1 7:1",
        "6:0.25 1':0.25 4':0.25 6':0.25 4':0.5 1':0.5 6:1 1':1", "7:0.5 2':0.5 4':0.5 5':0.5 4':1 2':1"]
for i, b in enumerate(S.sc("2人目")): PM.bar(b, K.mel(RIFF[i], oct=4))
# 掛け合い: 1台目と2台目が2小節ずつ受け渡す（1台目は低め、2台目は高め）
for i, b in enumerate(S.sc("掛け合い")):
    if (i // 2) % 2 == 0: PL[0].bar(b, K.mel(RIFF[i], oct=4))
    else: PRH.bar(b, K.mel(RIFF[i], oct=5))
# 掛け合い2（E）: 3人目が加わって、低い・高い・真ん中の順に2小節ずつ。最後の2小節は3人が同時に
for i, b in enumerate(S.sc("掛け合い2")):
    q = i // 2
    if q in (0, 3): PL[0].bar(b, KE.mel(RIFF[i], oct=4))
    if q in (1, 3): PRH.bar(b, KE.mel(RIFF[i], oct=5))
    if q in (2, 3): PM.bar(b, KE.mel(seq_up(RIFF[i], KE, 2), oct=4))
SOLO = ["3':0.25 5':0.25 7':0.25 5':0.25 3':0.25 1':0.25 7:0.25 5:0.25 3:0.5 5:0.5 7:1",
        "5':0.5 4':0.5 2':0.5 7:0.5 5:1 7:1", "6':0.25 5':0.25 3':0.25 1':0.25 6:0.5 1':0.5 3':1 1':1", "6:0.5 1':0.5 3':0.5 6':0.5 5':2",
        "4':0.25 6':0.25 1'':0.25 6':0.25 4':0.25 2':0.25 1':0.25 6:0.25 4:1 6:1", "#5:0.5 7:0.5 2':0.5 3':0.5 #5':1 3':1",
        "1'':0.75 7':0.25 6':0.5 5':0.5 3':1 1':1", "2':0.5 #4':0.5 5':0.5 7':0.5 5':2",
        "1'':0.25 7':0.25 5':0.25 3':0.25 1'':0.25 7':0.25 5':0.25 3':0.25 7':1 5':1", "7':0.5 5':0.5 2':0.5 7:0.5 5':2",
        "6':0.25 1'':0.25 6':0.25 3':0.25 6':0.25 1'':0.25 6':0.25 3':0.25 1'':2", "1'':1 6':1 4':1 1':1",
        " ".join(["4':0.125", "6':0.125"] * 8) + " 3':1 1':1", " ".join(["3':0.125", "#5':0.125"] * 8) + " 2':1 7:1",
        "6:0.25 1':0.25 3':0.25 6':0.25 1'':0.5 6':0.5 3':1 1':1", "2':1 #4':1 7':2"]
for i, b in enumerate(S.sc("ピアノのソロ")): PM.bar(b, KE.mel(SOLO[i], oct=4))
# 合いの手（Aメロ・サビの4小節目に、2台目の高い短い句）
for name, kk in (("Aメロ", K), ("Aメロ2", K), ("サビ", K), ("サビ2", KE), ("6人連弾", KA)):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3 and not (name == "Aメロ2" and i < 8): PRH.bar(b, kk.mel("R:2.5 5:0.25 6:0.25 1':0.5 3':0.5", oct=5 if name != "6人連弾" else 4))

# ================= 伴奏（ピアノ2台・ベース） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    v = voice(ch, 66, 3)
    rh = lh = None
    # 1台目: 右手16分の分散和音・左手8分のオクターブ（疾走ピアノ）
    if n == "1人きり": lh = f"{nm(low(ch, 'C2'))}:2 {nm(low(ch, 'C2') + 12)}:2"
    elif n == "2人目": rh = piano_arp16(ch, "C4", "C6") if i >= 4 else None; lh = piano_left8(ch, "C2")
    elif n in ("Aメロ", "Aメロ2"):
        if i >= 8 or n == "Aメロ2": rh = piano_arp16(ch, "C4", "C6", (0, 2, 1, 3, 2, 1, 2, 3))
        lh = f"{nm(low(ch, 'C2'))}:1.5 {nm(low(ch, 'C2') + 12)}:1 {nm(low(ch, 'C2'))}:1.5" if i < 8 else piano_left8(ch, "C2")
    elif n.startswith("Bメロ"):
        rh = piano_arp16(ch, "D4", "D6", (0, 1, 2, 3, 4, 3, 2, 1)); lh = piano_left8(ch, "C2")
        if i == L - 1: rh = f"{nm(v[2])}:1.5 R:2.5"; lh = f"{nm(low(ch, 'C2'))}:1.5 R:2.5"
    elif n in ("サビ", "サビ2", "6人連弾"):
        rh = piano_arp16(ch, "C4", "C6"); lh = piano_left8(ch, "C2")
    elif n == "隣に座る":
        lh = f"{nm(low(ch, 'C2'))}:4" if i < 8 else f"{nm(low(ch, 'C2'))}:2 {nm(low(ch, 'C2') + 12)}:2"
        if i >= 8: rh = " ".join(f"{nm(x)}:0.5" for x in tones(ch, "C4", "C6")[:4] * 2)
    elif n == "ピアノのソロ": lh = piano_left8(ch, "C2")
    elif n == "6人目": rh = piano_arp16(ch, "C4", "C6"); lh = piano_left8(ch, "C2")
    elif n == "ピアノだけ残る":
        t = tones(ch, "Ab3", "Ab5")
        rh = " ".join(f"{nm(t[q % len(t)])}:{0.5 if i < 4 else 1}" for q in ((0, 2, 1, 3, 2, 4, 3, 1) if i < 4 else (0, 2, 1, 3)))
        lh = f"{nm(low(ch, 'C2'))}:4"
        if i >= 6: rh = lh = None
    if rh and not n.startswith("掛け合い"): PL[0].bar(b, rh)
    if lh: PL[1].bar(b, lh)
    # 2台目: 和音（場面ごとに刻み方を変える）
    pat = None
    if n == "2人目": pat = "X:1.5 X:1 X:1.5"
    elif n in ("Aメロ", "Aメロ2"): pat = None if (n == "Aメロ" and i < 8) else "R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5"
    elif n.startswith("Bメロ"): pat = "X:2 X:2" if i < L - 1 else "X:1.5 R:2.5"
    elif n in ("サビ", "サビ2", "6人連弾"): pat = "X:1.5 X:1 X:1.5"
    elif n.startswith("掛け合い"): pat = "X:1 X:1 X:1 X:1"
    elif n == "隣に座る" and i >= 8: pat = "X:4"
    elif n == "ピアノのソロ": pat = "X:1.5 X:1 X:1.5"
    elif n == "6人目": pat = "X:4" if i < 4 else "X:2 X:2"
    if pat:
        vv = voice(ch, 64, 3)
        for j in range(3): PR[j].bar(b, pat.replace("X", nm(vv[j])))
    # 6人連弾: 2台目の高いきらめき（右手の16分を1オクターブ上で）
    if n == "6人連弾" and i % 4 != 3: PRH.bar(b, piano_arp16(ch, "C6", "C7", (3, 2, 1, 0, 1, 2, 3, 2)))
    # ベース
    r = low(ch, "E1")
    if n == "2人目": BASS.bar(b, bass_line(S, b, "root8") if i >= 4 else f"{nm(r)}:4")
    elif n in ("Aメロ", "Aメロ2"): BASS.bar(b, bass_line(S, b, "half" if i < 8 and n == "Aメロ" else "root8"))
    elif n.startswith("Bメロ"): BASS.bar(b, bass_line(S, b, "push") if i < L - 1 else f"{nm(r)}:1.5 R:2.5")
    elif n in ("サビ", "サビ2", "6人連弾"): BASS.bar(b, bass_line(S, b, "oct8"))
    elif n.startswith("掛け合い"): BASS.bar(b, bass_line(S, b, "walk"))
    elif n == "隣に座る": BASS.bar(b, bass_line(S, b, "long") if i < 8 else bass_line(S, b, "half"))
    elif n == "ピアノのソロ": BASS.bar(b, bass_line(S, b, "root8"))
    elif n == "6人目": BASS.bar(b, bass_line(S, b, "root8"))

# 終わり: ピアノだけで、テンションの和音（A♭maj7(9, #11)）を長くのばす
b_end = S.sc("ピアノだけ残る")[6]
PL[1].bar(b_end, "Ab2:8"); PL[0].bar(b_end, "Eb3:8")
for j, x in enumerate(["G4", "Bb4", "C5"]): PR[j].bar(b_end, f"{x}:8")
PM.bar(b_end, "D5:8")
# 効果音
riser(FX, S.sc("サビ")[0], 4, "C4"); riser(FX, S.sc("6人連弾")[0], 8, "D4")
cym_swell(CYM, S.sc("2人目")[0], 2, "C4"); cym_swell(CYM, S.sc("ピアノのソロ")[0], 4, "E4")

# ================= ドラム =================
def ride8(b, first="C2"):
    D.cym(b, f"{first}:0.5 " + "D2:0.5 " * 7); D.H[b] = "." * 16


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("1音", "1人きり", "ピアノだけ残る"):
        D.set(b, "." * 16, "." * 16, "." * 16)
        if n == "1人きり" and last: D.set(b, "." * 16, "........ooxxXXXX", "." * 16)
    elif n == "2人目":
        if i < 4: D.set(b, "X.......X.......", "....X.......X...", "x.x.x.x.x.x.x.x.")
        else: vgroove(D, b, "vrock2", ghosts=0.35, seed=b)
        if i == 0: crash(D, b)
        if last: put_fill(D, b, "tomdown")
    elif n in ("Aメロ", "Aメロ2"):
        vgroove(D, b, "beat8" if i < 8 else "vrock2", ghosts=0.4, seed=b, h="x.x.x.x.x.x.x.x." if i < 8 else None)
        if n == "Aメロ2" and i >= 8: ride8(b, "C2" if i == 8 else "D2")
        if i == 0: crash(D, b)
        if i == 7: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
    elif n.startswith("Bメロ"):
        vgroove(D, b, "half" if i < 4 else "vrock2", ghosts=0.3, seed=b)
        if i == 4: crash(D, b, "G2")
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 1.5 if n == "Bメロ" else 3); D.cym(b, "C2:1.5" if n == "Bメロ" else "R:4")
    elif n in ("サビ", "サビ2", "6人連弾"):
        vgroove(D, b, "vrock" if n != "サビ2" or i >= 8 else "vrock2", ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if n == "6人連弾" and 16 <= i < 22: ride8(b, "C2" if i == 16 else "D2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16" if i % 16 == 7 else "tomdown")
        if last and n != "6人連弾": put_fill(D, b, "tomdown")
        if last and n == "6人連弾": D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); D.cym(b, "C2:4")
    elif n.startswith("掛け合い"):
        vgroove(D, b, "vrock2", ghosts=0.4, seed=b)
        if i == 0: crash(D, b)
        if i % 2 == 1: put_fill(D, b, "small" if i < 7 else "tomdown")
    elif n == "隣に座る":
        if i < 8: D.set(b, "X...........X...", "." * 16, "x...x...x...x..." if i >= 2 else "." * 16)
        else:
            vgroove(D, b, "half", ghosts=0.45, seed=b, h="x...x...x...x...")
            if not last: D.cym(b, ("B2:1 " if i == 8 else "D2:1 ") + "D2:1 D2:1 D2:1"); D.H[b] = "." * 16
        if last: put_fill(D, b, "lift")
    elif n == "ピアノのソロ":
        vgroove(D, b, "vrock2", ghosts=0.4, seed=b)
        if i % 8 == 0: crash(D, b)
        if i % 4 == 3: put_fill(D, b, "small" if i % 8 == 3 else "tomtrip")
    elif n == "6人目":
        D.set(b, "X...X...X...X...", "....X.......X...", "xxxxxxxxxxxxxxxx")
        if i < 4: D.set(b, "X.......X.......", "....X.......X...", "x.x.x.x.x.x.x.x.")
        if i == 3: put_fill(D, b, "small")
        if i == 6: put_fill(D, b, "build")
        if last: D.set(b, "X...X...X.......", "xxxxXXXXXXXX....", "." * 16)

# 止め（Bメロの終わり）・1拍の完全な無音（2番のサビの前・6人連弾の前）
SIL.add(S.sc("Bメロ")[-1], 1.5, 4)
SIL.add(S.sc("Bメロ2")[-1], 3, 4)
SIL.add(S.sc("6人目")[-1], 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の10。ピアノロック。B長調・184。2番のサビは半音下（B♭）、最後のサビは短3度上（D）。"
          "人見知りの「ぼく」が、駅前のストリートピアノで知らない人とつながる。ピアノの単音で始まり、ピアノだけの主題、バンドが入る前奏、8分で語る Aメロ、"
          "4度上へ跳ぶサビ、ピアノ2台の掛け合い、半音下の2番のサビ、歌とピアノが受け渡す Cメロ、ピアノのソロ、1拍の無音から6人連弾の大サビ、ピアノだけ残る。自作")
S.no_depth = True
teto(S, LY, V, transpose=-6, special={"6人連弾": 0.55, "隣に座る": -0.45, "6人目": 0.1})
