# vb25 10「鍵盤ジャンクション」Keyboard Junction（仮）— ロック（ピアノロック）。F長調・184・4/4
# 転調（2段）: 1番は F → 2番のサビで半音下げて E → 最後のサビで、もとの F から短3度上げて A♭（直前に1拍の無音）
# 物語: 駅前のストリートピアノ。1人が弾きはじめると、知らない人が1人、また1人と隣に座り、最後は6人の連弾になる。
# 場面と強さ: 1音（ピアノの単音・極小）→ 1人きり（ピアノだけで主題・静か）→ 2人目（バンドが入る・中強）→ Aメロ（語る・中）→ Bメロ（溜め・止め）
#   → サビ（強）→ 掛け合い（ピアノ2台が2小節ずつ受け渡す）→ 2番（ピアノが歌を受け取る）→ 2番のサビ（半音下の E・ひやりと明るさが変わる）
#   → 隣に座る（Cメロ・ピアノと歌が2小節ずつ受け渡し → Half feel）→ ピアノのソロ → 6人目（1拍の無音）→ 6人連弾の大サビ（A♭・最大）→ ピアノだけ残る
# 旋律の性格: ピアノと歌の役が受け渡す。Aメロは16分の早口。サビは同じ音の3連打から短6度・オクターブの跳躍。最高音 C6
# 派手な展開: 主旋律の受け渡し（歌の役・ピアノ・ピアノ2台）・2段の転調・1拍の完全な無音2回・止め・Half feel
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

V = Voice(S, vol=0.22, delay=0.75)
PL = [S.track("ピアノ1台目（右手）", "piano", **piano_spec(0.12, -0.35, 0.22)), S.track("ピアノ1台目（左手）", "piano", **piano_spec(0.12, -0.35, 0.22))]
PR = [S.track(f"ピアノ2台目（和音{i + 1}）", "piano", **piano_spec(0.1, 0.35, 0.22)) for i in range(3)]
PRH = S.track("ピアノ2台目（高いきらめき）", "piano", **piano_spec(0.1, 0.35, 0.22))
PM = S.track("ピアノ（主旋律の受け渡し）", "piano", **piano_spec(0.17, 0.0, 0.22))
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.21))
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 旋律 =================
A1 = ["R:0.25 6,:0.25 6,:0.25 1:0.25 2:0.25 1:0.25 6,:0.5 R:0.25 6,:0.25 1:0.25 3:0.25 2:0.5 1:0.5",
      "R:0.25 1:0.25 1:0.25 1:0.25 2:0.25 1:0.25 6,:0.5 R:0.25 5,:0.25 6,:0.25 1:0.25 4:1",
      "R:0.25 3:0.25 3:0.25 3:0.25 5:0.25 3:0.25 2:0.25 1:0.25 R:0.25 2:0.25 3:0.25 5:0.25 6:0.5 5:0.5",
      "3:0.5 1:0.25 7,:0.25 R:0.5 6,:0.25 7,:0.25 1:1.5 R:0.5",
      "R:0.25 6,:0.25 1:0.25 2:0.25 3:0.25 2:0.25 1:0.25 6,:0.25 R:0.25 1:0.25 2:0.25 4:0.25 3:0.5 1:0.5",
      "R:0.25 4:0.25 4:0.25 4:0.25 3:0.25 2:0.25 1:0.5 R:0.25 6,:0.25 1:0.25 2:0.25 1:1",
      "R:0.25 2:0.25 2:0.25 4:0.25 5:0.25 4:0.25 2:0.25 4:0.25 5:0.5 6:0.5 5:0.5 4:0.5",
      "5:0.75 3:0.25 5:0.5 1':0.5 4:1 R:1"]
A1b = ["R:0.25 6,:0.25 6,:0.25 1:0.25 2:0.25 3:0.25 5:0.25 3:0.25 R:0.25 2:0.25 1:0.25 2:0.25 3:0.5 2:0.5",
       "R:0.25 1:0.25 2:0.25 4:0.25 6:0.25 4:0.25 2:0.5 R:0.25 1:0.25 2:0.25 4:0.25 6:1",
       "R:0.25 5:0.25 5:0.25 5:0.25 6:0.25 5:0.25 3:0.25 2:0.25 R:0.25 3:0.25 5:0.25 1':0.25 7:0.5 5:0.5",
       "3:0.5 5:0.25 6:0.25 R:0.5 7:0.25 6:0.25 5:1.5 R:0.5",
       A1[4],
       "R:0.25 6:0.25 6:0.25 6:0.25 5:0.25 4:0.25 2:0.5 R:0.25 1:0.25 2:0.25 4:0.25 6:1",
       "R:0.25 4:0.25 5:0.25 6:0.25 5:0.25 4:0.25 2:0.25 1:0.25 2:0.5 4:0.5 5:0.5 6:0.5",
       "5:0.5 #4:0.5 5:1 R:2"]
A2b = ["R:0.25 1:0.25 3:0.25 5:0.25 6:0.25 5:0.25 3:0.25 1:0.25 R:0.25 6,:0.25 1:0.25 3:0.25 2:0.5 1:0.5",
       "R:0.25 4:0.25 4:0.25 6:0.25 1':0.25 6:0.25 4:0.5 R:0.25 2:0.25 4:0.25 6:0.25 5:1",
       "R:0.25 3:0.25 5:0.25 1':0.25 7:0.25 5:0.25 3:0.25 5:0.25 R:0.25 2:0.25 3:0.25 5:0.25 6:0.5 5:0.5",
       "3:0.5 1:0.25 7,:0.25 R:0.5 1:0.25 3:0.25 5:1.5 R:0.5",
       "R:0.25 6:0.25 6:0.25 6:0.25 1':0.25 6:0.25 5:0.25 4:0.25 R:0.25 3:0.25 2:0.25 1:0.25 2:0.5 3:0.5",
       "R:0.25 4:0.25 6:0.25 1':0.25 2':0.25 1':0.25 6:0.5 R:0.25 4:0.25 2:0.25 1:0.25 2:1",
       "R:0.25 2:0.25 4:0.25 6:0.25 5:0.25 4:0.25 2:0.25 4:0.25 5:0.5 6:0.5 1':0.5 2':0.5",
       "1':1 5:1 R:2"]
BM = ["4:1 6:0.5 1':0.5 6:1 5:1", "5:1 7:0.5 2':0.5 1':1 7:1", "7:1 5:0.5 3:0.5 5:1 7:1", "6:2 R:1 6:0.5 1':0.5",
      "2':1 4':0.5 2':0.5 1':1 2':1", "#5:0.5 7:0.5 3':1 2':1 #5:1", "1':1 2':1 4':2", "2':2 R:2"]
BM2 = BM[:4] + ["2':0.5 1':0.5 2':0.5 4':0.5 2':1 1':1", "3':1 2':0.5 7:0.5 #5:1 7:1", "6:1 1':1 4':1 3':1", "2':1 R:3"]
CH1 = ["R:0.5 1':0.5 1':0.5 1':0.5 4':1.5 3':0.5", "2':1 7:0.5 #5:0.5 3':2", "R:0.5 3':0.5 3':0.5 3':0.5 5':1 3':1", "2':1 1':0.5 6:0.5 1':2",
       "R:0.5 6:0.5 1':0.5 2':0.5 4':1 2':1", "3':1.5 2':0.5 1':1 7:1", "#5:0.5 7:0.5 2':1 7:1 #5:1", "6:3 R:1"]
CH1b = [CH1[0], "2':1 7:0.5 #5:0.5 3':1 2':1", "R:0.5 3':0.5 3':0.5 3':0.5 4':1 3':1", "2':1.5 1':0.5 b7:1 5:1",
        "R:0.5 4':0.5 4':0.5 4':0.5 5':1 4':1", "3':1 2':1 1':1 2':1", "3':2 1':1 5:1", "1':4"]
CH2 = CH1[:6] + ["#5:0.5 7:0.5 2':0.5 3':0.5 2':1 7:1", "6:2 R:2"]
CH2b = CH1b[:6] + ["3':1 2':0.5 1':0.5 2':2", "1':2 R:2"]
# 6人連弾（A♭）: いちばん高い音を C6（3'）にそろえる
CHL = ["R:0.5 1':0.5 1':0.5 1':0.5 3':1.5 2':0.5", "2':1 7:0.5 #5:0.5 3':2", "R:0.5 3':0.5 3':0.5 3':0.5 2':1 1':1", "2':1 1':0.5 6:0.5 1':2",
       "R:0.5 6:0.5 1':0.5 2':0.5 3':1 2':1", "3':1.5 2':0.5 1':1 7:1", "#5:0.5 7:0.5 2':1 7:1 #5:1", "6:3 R:1",
       "R:0.5 1':0.5 1':0.5 1':0.5 3':1.5 2':0.5", "2':1 7:0.5 #5:0.5 3':1 2':1", "R:0.5 3':0.5 3':0.5 3':0.5 2':1 3':1", "2':1.5 1':0.5 b7:1 5:1",
       "R:0.5 2':0.5 2':0.5 2':0.5 3':1 2':1", "3':1 2':1 1':1 2':1", "3':2 1':1 5:1", "1':4",
       "4:1 6:0.5 1':0.5 3':2", "2':1 1':0.5 7:0.5 5:2", "3':1 7:1 5:1 3:1", "6:1 1':1 3':2",
       "2':1.5 1':0.5 6:1 4:1", "5:2 2':2", "1':4", "R:4"]

for name, lines in (("Aメロ", A1 + A1b), ("Aメロ2", A1 + A2b)):
    for i, b in enumerate(S.sc(name)):
        line = K.mel(lines[i], oct=4)
        if name == "Aメロ2" and i < 8: PM.bar(b, shift_oct(line, 1))      # 2番の前半は、ピアノが歌を受け取る
        else: V.bar(b, line)
for name, lines in (("Bメロ", BM), ("Bメロ2", BM2)):
    for i, b in enumerate(S.sc(name)): V.bar(b, K.mel(lines[i], oct=4))
for i, b in enumerate(S.sc("サビ")): V.bar(b, K.mel((CH1 + CH1b)[i], oct=4))
for i, b in enumerate(S.sc("サビ2")): V.bar(b, KE.mel((CH2 + CH2b)[i], oct=4))
for i, b in enumerate(S.sc("6人連弾")): V.bar(b, KA.mel(CHL[i], oct=4))
# 1音・1人きり: ピアノの単音から、サビの主題をピアノだけで（ゆっくり、すき間を残して）
ONE = ["1':1 R:1 5:2", "3':1 R:1 2':2", "1':1 R:0.5 5:0.5 6:2", "5:3 R:1"]
for i, b in enumerate(S.sc("1音")): PM.bar(b, K.mel(ONE[i], oct=4))
for i, b in enumerate(S.sc("1人きり")): PM.bar(b, K.mel(CH1[i], oct=4))
# 隣に座る（E）: 2小節ずつ、歌の役 → ピアノ → 歌の役 → ピアノ。後半は Half feel で歌が上がる
SITV = ["6:2 5:1 3:1", "4:3 R:1", "5:0.5 6:0.5 7:0.5 2':0.5 1':1 7:1", "5:4",
        "3:1 5:1 6:1 1':1", "7:2 6:2", "2':0.5 1':0.5 6:0.5 4:0.5 2:1 4:1", "5:2 R:2",
        "1':2 7:1 6:1", "7:1 #5:1 3':2", "3':1 1':1 6:2", "5:3 R:1", "4:1 6:1 1':1 3':1", "4':2 3':1 2':1", "3':1 5':1 3':1 2':1", "2':2 R:2"]
for i, b in enumerate(S.sc("隣に座る")):
    line = KE.mel(SITV[i], oct=4)
    if i < 8 and (i // 2) % 2 == 1: PM.bar(b, shift_oct(line, 1))
    else: V.bar(b, line, low=(i >= 8))
# 6人目: 歌の役が A♭ へ導く
for i, b in enumerate(S.sc("6人目")):
    V.bar(b, [KE.mel("3:2 5:2", oct=4), KE.mel("6:2 7:1 1':1", oct=4), KE.mel("2':2 1':1 6:1", oct=4), KE.mel("7:3 R:1", oct=4),
              KE.mel("1':2 2':2", oct=4), KE.mel("3':2 2':1 1':1", oct=4), KA.mel("2':2 1':1 6:1", oct=4), KA.mel("5:2 7:1 R:1", oct=4)][i], low=(i >= 4))
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
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の10。ピアノロック。F長調・184。2番のサビで半音下げて E、最後のサビは F から短3度上げて A♭。"
          "駅前のストリートピアノに、知らない人が次々と連弾に加わる。ピアノの単音で始まり、ピアノだけで主題、バンドが入って16分の分散和音で走る。"
          "Aメロは16分の早口、サビは同じ音の3連打から高く跳ぶ。ピアノ2台の掛け合い、2番はピアノが歌を受け取り、Cメロは歌とピアノが2小節ずつ受け渡して Half feel へ。"
          "ピアノのソロ、1拍の無音のあと6人連弾の大サビ。最後はピアノだけ残って A♭maj7(9,#11) をのばす。歌の役は声のように聞こえるシンセ。自作")
vwrite(S)
