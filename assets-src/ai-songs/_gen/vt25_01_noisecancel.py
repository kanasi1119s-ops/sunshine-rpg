# vt25 01「ハロー・ノイズキャンセル」Hello, Noise Cancel（仮）— テクノポップ。140・4/4。Bm（サビは平行調の D）→ 最後のサビは +1（E♭）。
# 物語: 毎朝、イヤホンで世界にふたをして駅へ向かう「わたし」。駅のざわめきの中に、いつも同じ時間に君の声がまじる。
#   聞こえないふりをしながら、本当は君の声のたびに音量を上げていた。ある朝、片方だけイヤホンを外す。
#   左耳だけの世界から、両耳の世界へ。うるさい街の中で、君の「おはよう」がいちばんに届く。最後は自分から「おはよう」を言う。
# 場面と強さ: ざわめき（雑音が「すっと」消えて、ベルの3音・中）→ Aメロ1（片耳・語る・弱）→ Bメロ1（ためる）→ サビ1（両耳に開く・強）
#   → 間奏（ベル）→ Aメロ2（片方を外す）→ Bメロ2 → サビ2 → 間奏2（ベルの旋律とアルペジオ）→ 落ちサビ（また片耳・とても弱い）
#   → 1拍の無音 → 最後のサビ（+1・いちばん強い）→ おはよう（和音で切る）
# 旋律の性格: Aメロは同じ音の8分の連打で語り（D4〜A4）、句の終わりで少し下がる。サビは5度・オクターブの跳躍で開き（A4〜E5）、
#   「はろー」の3音が毎回同じ形で戻ってくる。最高音は最後のサビの F5。
# ほかの曲とちがう所（この曲だけの音）: Aメロ・Bメロ・落ちサビは音が左にかたよる（片耳のイヤホン）。サビで左右いっぱいに広がる（ワイダー）。
#   始まりは街の雑音が鳴っていて、ノイズキャンセルが入るように「すっと」消える。
from vt25_lib import *

S = Song("01", "noisecancel", "ハロー・ノイズキャンセル（仮）", "Hello, Noise Cancel", 140, 4, "B", "minor", "テクノポップ（ボカロ）")
S.kit = "electro"
S.flags = S.flags + " --piano salamander --space sky --space-wet 0.16"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.6
K = Key("B", "minor")          # Aメロ（oct 3 で 1 = B3）
KD = Key("D", "major")         # Bメロ・サビ（oct 4 で 1 = D4）
KE = Key("Eb", "major")        # 最後のサビ（+1）

INTRO = ["Bm7", "Gmaj7", "D/F#", "Em7"]
A_CH = ["Bm7", "Gmaj7", "D/F#", "Em7", "Bm7", "Gmaj7", "Asus4", "A"]
B_CH = ["Em7", "F#m7", "Gmaj7", "A", "Em7", "Bm7", "Gmaj7", "A7"]
C_CH = ["D", "Bm7", "Gmaj7", "A/C#", "D", "Em7", "Gmaj7", "D/F#", "D", "Bm7", "Gmaj7", "F#m7", "D", "Em7", "Gmaj7", "Asus4"]
LAST = [tr_chord(c, 1) for c in C_CH]

S.scene("ざわめき", 8, "intro", INTRO)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 8, "break", INTRO)
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("間奏2", 8, "solo", INTRO + ["Bm7", "Gmaj7", "Em7", "A7"])
S.scene("落ちサビ", 8, "bridge", C_CH[:7] + ["Bb"])          # 最後の小節は E♭ への入り口（B♭）
S.scene("最後のサビ", 24, "chorus", LAST + LAST[8:16])
S.scene("おはよう", 6, "outro", ["Abmaj7", "Bb", "Gm7", "Cm7", "Ebmaj9", "Ebmaj9"])

V = Voice(S, vol=0.22, delay=0.75, bright=1.0, patch="popLeadClear", low=True)
BELL = S.track("ベル（はろーの3音）", "pad", patch="surgeBell1", volume=0.075, pan=0.0, reverb=0.4, sustain=1.2,
               fx=[{"type": "filter", "kind": "highpass", "freq": 300, "q": 0.7}, {"type": "pingpong", "beats": 0.75, "mix": 0.18, "feedback": 0.3}])
ARP = S.track("アルペジオ（街の信号）", "lead", patch="surgeDnaSeq", volume=0.06, pan=-0.25, reverb=0.25, mono=True,
              fx=[{"type": "filter", "kind": "highpass", "freq": 400, "q": 0.7}])
PL = S.track("ピアノ（左手）", "piano", volume=0.12, pan=-0.1, reverb=0.22, fx=[{"type": "eq", "low": -2, "mid": -2, "midHz": 400, "high": 3}])
PR = S.track("ピアノ（右手）", "piano", volume=0.12, pan=-0.1, reverb=0.22, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 4}])
PRM = S.track("ピアノ（歌を受け取る）", "piano", volume=0.16, pan=-0.1, reverb=0.22, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 3}])
BASS = S.track("シンセベース", "bass", **synth_bass_spec("surgeBassAnalogBassImaged", vol=0.24, duck=0.3))
PAD = [S.track(f"きらめくパッド{i + 1}", "pad", **pad_spec("surgePadSparkly", vol=0.045, pan=-0.3 + 0.3 * i, duck=0.3, sustain=1.2)) for i in range(3)]
SAW = [S.track(f"サビの厚い和音{i + 1}", "pad", **pad_spec("surgeHappySaws", vol=0.04, pan=-0.4 + 0.4 * i, duck=0.45, sustain=0.9)) for i in range(3)]
PLK = S.track("プラック（裏のきらめき）", "pad", patch="surgeNicePluck", volume=0.05, pan=0.4, reverb=0.35, sustain=0.6,
              fx=[{"type": "filter", "kind": "highpass", "freq": 500, "q": 0.7}])
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.06, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の旋律と歌詞 =================
VA = ["R:0.5 3:0.5 3:0.5 3:0.5 3:0.5 4:0.5 3:0.5 2:0.5", "1:1 2:1 3:1 R:1",
      "R:0.5 5:0.5 5:0.5 5:0.5 5:0.5 6:0.5 5:0.5 4:0.5", "3:1.5 2:0.5 3:1 R:1",
      "R:0.5 3:0.5 3:0.5 3:0.5 5:0.5 5:0.5 7:0.5 6:0.5", "5:1 4:1 3:1 R:1",
      "R:0.5 4:0.5 4:0.5 4:0.5 3:0.5 2:0.5 1:0.5 2:0.5", "2:2 R:2"]
A1 = ("いやほんでふたをした/あさのえきのざわめき/きこえないふりをして/きょうもかいさつへ/"
      "きみのこえがするたび/ぼりゅーむをあげてたの/ほんとうはしってるんだ/きいてみたいのに")
A2 = ("かたほうだけはずした/ひだりのみみがあつい/しんごうのおとまじり/きみのあしおとが/"
      "おはようっていえたなら/なにかがかわるかなって/こころのすいっちをおす/ゆびがふるえてる")
VB = ["R:0.5 3:0.5 3:0.5 4:0.5 5:1 3:1", "2:1.5 1:0.5 2:1 R:1", "R:0.5 4:0.5 4:0.5 5:0.5 6:1 4:1", "3:1.5 2:0.5 3:1 R:1",
      "R:0.5 5:0.5 5:0.5 6:0.5 7:1 5:1", "6:1 7:1 1':1 R:1", "R:0.5 2':0.5 1':0.5 7:0.5 6:0.5 5:0.5 6:0.5 7:0.5", "5:2 R:2"]
B1 = "ひとごみのなかで/きみだけがひかる/そのこえききたい/かたほうはずせば"
B2 = "まちのおとがする/うるさいけどいい/そのなかのきみを/みつけにいくから"
VC = ["R:0.5 5:0.5 1':1 7:0.5 1':0.5 2':1", "1':1.5 5:0.5 5:1 R:1", "R:0.5 4:0.5 6:1 5:0.5 6:0.5 1':1", "7:1.5 5:0.5 6:1 R:1",
      "R:0.5 5:0.5 1':1 7:0.5 1':0.5 2':1", "2':1 1':1 6:1 R:1", "R:0.5 4:0.5 4:0.5 5:0.5 6:1 7:1", "1':2 R:2",
      "R:0.5 5:0.5 1':1 7:0.5 1':0.5 2':1", "1':1.5 5:0.5 5:1 R:1", "R:0.5 4:0.5 6:1 5:0.5 6:0.5 1':1", "7:1.5 5:0.5 6:1 R:1",
      "R:0.5 5:0.5 1':1 7:0.5 1':0.5 2':1", "2':1 1':1 6:1 R:1", "R:0.5 6:0.5 6:0.5 5:0.5 4:0.5 3:0.5 2:0.5 3:0.5", "1:2 R:2"]
C1 = "はろーきみのこえ/ちゃんときこえるよ/のいずのむこうに/きみがいたの/はろーあさのまち/みみをすましたら/きみのおはようが/いちばんにとどく"
C2 = "はろーきこえてる/ふるえるこえだって/そのままでいいよ/かくさないで/はろーりょうみみで/せかいをきいたら/こんなにあかるい/きみのいるあさだ"
CL = ("はろーおはようを/いまならいえるよ/のいずもぜんぶね/うたになるよ/はろーはろーきみ/はじめましてだね/いやほんはずして/おはようっていうよ/"
      "はろーはろーきょう/あさのおとがする/きみのとなりまで/あとすこしなんだ")
CO = "はろーきこえるの/かたほうのみみで/ちいさなこえでも/とどいてるよ"
LY = Lyrics(S)


def put(name, key, lines, text, o=4):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA + VA, A1, o=3)
put("Bメロ1", KD, VB, B1)
put("サビ1", KD, VC, C1)
put("Bメロ2", KD, VB, B2)
put("サビ2", KD, VC, C2)
put("落ちサビ", KD, VC[:8], CO)
put("最後のサビ", KE, VC + VC[8:16], CL)
put("おはよう", KE, ["R:4"] * 4 + ["R:1 5:1 3:0.5 2:0.5 1:1", "R:4"], "おはよう")
if VOCAL: put("Aメロ2", K, VA + VA, A2, o=3)
else:
    # BGM: Aメロ2 の前半はピアノが歌を受け取り、後半は歌の役のシンセ
    for i, (b, l) in enumerate(zip(S.sc("Aメロ2"), VA + VA)):
        if i < 8: PRM.bar(b, K.mel(l, oct=4))
        else: V.bar(b, K.mel(l, oct=3))

# ================= ベル（「はろー」の3音: 5 → 1' → 7。サビの頭と同じ形） =================
HELLO = "R:0.5 A5:0.5 D6:1 C#6:0.5 D6:0.5 E6:1"
for i, b in enumerate(S.sc("ざわめき")):
    if i in (3, 5, 7): BELL.bar(b, "R:2 F#5:0.5 B5:1 A5:0.5" if i < 7 else HELLO)
for b in S.sc("間奏"): BELL.bar(b, HELLO if (b - S.sc("間奏")[0]) % 2 == 0 else "D6:1.5 A5:0.5 A5:1 R:1")
for name in ("サビ1", "サビ2"):
    for i, b in enumerate(S.sc(name)):
        if i % 8 == 7: BELL.bar(b, "R:2 A5:0.5 D6:0.5 F#6:1")
SOLO = ["R:0.5 A5:0.5 D6:1 C#6:0.5 D6:0.5 E6:1", "F#6:1.5 E6:0.5 D6:1 R:1", "R:0.5 G5:0.5 B5:1 A5:0.5 B5:0.5 D6:1", "C#6:2 A5:1 R:1",
        "R:0.5 F#5:0.5 B5:1 A5:0.5 B5:0.5 D6:1", "E6:1 D6:1 B5:1 R:1", "R:0.5 G5:0.5 G5:0.5 A5:0.5 B5:1 D6:1", "C#6:3 R:1"]
for i, b in enumerate(S.sc("間奏2")): BELL.bar(b, SOLO[i])
for i, b in enumerate(S.sc("最後のサビ")):
    if i % 8 == 7: BELL.bar(b, "R:2 Bb5:0.5 Eb6:0.5 G6:1")

# ================= 和音・ピアノ・アルペジオ =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    t = tones(ch, "F#4", "F#6")
    if n == "ざわめき":
        if i >= 4:
            v = voice(ch, 64, 3)
            for j in range(3): PAD[j].bar(b, f"{nm(v[j])}:4")
        continue
    if n in ("Aメロ1", "Aメロ2"):
        # 片耳の Aメロ: 左手は2分、右手は裏で短く（電車の揺れ）
        r = low(ch, "B1")
        PL.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2")
        v = voice(ch, 67, 3)
        PR.bar(b, " ".join(f"R:0.5 {nm(v[q % 3])}:0.5'" for q in range(4)) if i % 2 == 0 else f"R:1 {nm(v[0])}:1 {nm(v[1])}:1 {nm(v[2])}:1")
        if n == "Aメロ2" or i >= 8:
            for j in range(3): PAD[j].bar(b, f"{nm(voice(ch, 62, 3)[j])}:4")
        if n == "Aメロ2" and i >= 8: ARP.bar(b, piano_arp16(ch, "B4", "B5", pat=(0, 2, 1, 3)))
    elif n in ("Bメロ1", "Bメロ2"):
        r = low(ch, "B1")
        PL.bar(b, " ".join(f"{nm(r if q % 2 == 0 else r + 12)}:0.5" for q in range(8)))
        v = voice(ch, 66, 4)
        PR.bar(b, " ".join(f"{nm(x)}:1" for x in v[:4]) if i % 2 == 0 else f"{nm(v[1])}:2 {nm(v[3])}:2")
        for j in range(3): PAD[j].bar(b, f"{nm(voice(ch, 62, 3)[j])}:4")
        ARP.bar(b, piano_arp16(ch, "D5", "D6", pat=(0, 1, 2, 3)))
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        r = low(ch, "B1")
        PL.bar(b, f"{nm(r)}:1.5 {nm(r + 12)}:0.5 {nm(r + 7)}:1 {nm(r + 12)}:1")
        v = voice(ch, 69, 4)
        PR.bar(b, f"{nm(v[0])}:0.75 {nm(v[1])}:0.75 {nm(v[2])}:0.5 {nm(v[3])}:1 {nm(v[1])}:1")
        sv = voice(ch, 64, 3)
        for j in range(3): SAW[j].bar(b, f"{nm(sv[j])}:1.5 {nm(sv[j])}:1 {nm(sv[j])}:1.5")
        ARP.bar(b, piano_arp16(ch, "A4", "A6", pat=(0, 2, 4, 3, 1, 3, 2, 4)))
        if i % 2 == 1: PLK.bar(b, " ".join(f"R:0.5 {nm(t[q % len(t)])}:0.5" for q in (2, 3, 4, 3)))
    elif n == "間奏":
        for j in range(3): PAD[j].bar(b, f"{nm(voice(ch, 64, 3)[j])}:4")
        ARP.bar(b, piano_arp16(ch, "B4", "B5", pat=(0, 2, 1, 3)))
    elif n == "間奏2":
        r = low(ch, "B1")
        PL.bar(b, f"{nm(r)}:1.5 {nm(r + 12)}:0.5 {nm(r + 7)}:1 {nm(r + 12)}:1")
        for j in range(3): PAD[j].bar(b, f"{nm(voice(ch, 62, 3)[j])}:4")
        ARP.bar(b, piano_arp16(ch, "D5", "D6", pat=(0, 3, 1, 2)))
    elif n == "落ちサビ":
        # とても弱い: ピアノの和音だけ（左手は全音符）
        r = low(ch, "B1")
        PL.bar(b, f"{nm(r)}:4")
        v = voice(ch, 67, 4)
        PR.bar(b, " ".join(f"{nm(x)}:1" for x in v) if i < 7 else f"{nm(v[0])}:2 {nm(v[2])}:2")
    elif n == "おはよう":
        v = voice(ch, 64, 4)
        if i < 4:
            PL.bar(b, f"{nm(low(ch, 'B1'))}:4"); PR.bar(b, " ".join(f"{nm(x)}:1" for x in v))
            for j in range(3): SAW[j].bar(b, f"{nm(v[j])}:4")
        elif i == 4:
            PL.bar(b, f"{nm(low(ch, 'B1'))}:2 R:2")
            PR.bar(b, f"{nm(v[0])}:0.5 {nm(v[1])}:0.5 {nm(v[2])}:0.5 {nm(v[3])}:1.5")
            for j in range(3): PAD[j].bar(b, f"{nm(voice(ch, 66, 3)[j])}:6")
        else:
            BELL.bar(b, "Eb6:0.5! R:3.5")

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "ざわめき":
        if i >= 6: BASS.bar(b, bass_line(S, b, "long", lo="B1"))
    elif n in ("Aメロ1", "Aメロ2"): BASS.bar(b, bass_line(S, b, "half" if i < 8 else "push", lo="B1"))
    elif n in ("Bメロ1", "Bメロ2"): BASS.bar(b, bass_line(S, b, "root8", lo="B1"))
    elif n in ("サビ1", "サビ2", "最後のサビ", "間奏2"): BASS.bar(b, bass_line(S, b, "oct8" if i % 4 != 3 else "push", lo="B1"))
    elif n == "間奏": BASS.bar(b, bass_line(S, b, "house", lo="B1"))
    elif n == "落ちサビ":
        if i == 7: BASS.bar(b, bass_line(S, b, "long", lo="B1"))
    elif n == "おはよう" and i < 5: BASS.bar(b, bass_line(S, b, "long", lo="B1"))

# ================= 効果音 =================
riser(FX, S.sc("サビ1")[0], 4, "C4"); riser(FX, S.sc("サビ2")[0], 4, "C4")
cym_swell(CYM, S.sc("Aメロ1")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 4, "E4")

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "ざわめき":
        if i >= 4: vgroove(D, b, "four", ghosts=0, seed=b, s="................", h="..x...x...x...x.")
        if i == 7: put_fill(D, b, "lift")
    elif n in ("Aメロ1", "Aメロ2"):
        vgroove(D, b, "beat8" if i < 8 else "four", ghosts=0.25, seed=b)
        if i == 0: crash(D, b)
        if i % 8 == 7 and not last: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
    elif n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "halfdrive", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 1)
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        vgroove(D, b, "four16" if n != "サビ1" else "four", ghosts=0.2, seed=b)
        if i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
        if i % 8 == 7 and not last: put_fill(D, b, "tomdown" if i == 7 else "small")
        if last and n != "最後のサビ": put_fill(D, b, "snare16")
    elif n == "間奏":
        vgroove(D, b, "four", ghosts=0, seed=b, s="................")
    elif n == "間奏2":
        vgroove(D, b, "twostep" if i < 4 else "four16", ghosts=0.3, seed=b)
        if i == 0: crash(D, b)
        if last: put_fill(D, b, "lift")
    elif n == "落ちサビ":
        if i >= 4: D.set(b, "X" + "." * 15, "." * 16, "x...x...x...x...")
    elif n == "おはよう":
        if i == 0: crash(D, b, "C2", 6); D.set(b, "X.......X.......", "........X.......", "x.x.x.x.x.x.x.x.")
        elif i in (1, 2): D.set(b, "X.......X.......", "........X.......", "x.x.x.x.x.x.x.x.")
        elif i == 3: D.set(b, "X.......X.......", "........X.......", "x.x.x.x.x.x.x.x.")

# 止め: Bメロの最後（1拍だけ叩いて全員休み）。1拍の完全な無音: 最後のサビの直前
for name in ("Bメロ1", "Bメロ2"): SIL.add(S.sc(name)[-1], 1, 4)
SIL.add(S.sc("最後のサビ")[0] - 1, 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の01。テクノポップ。Bm（サビは D）・140、最後のサビは +1（E♭）。"
          "イヤホンで世界にふたをしていた子が、片方を外して君の声を聞く。Aメロ・Bメロ・落ちサビは音が左にかたより（片耳）、サビで左右いっぱいに開く。"
          "街の雑音がすっと消えて始まり、「おはよう」の和音で切る。FM ベル・アルペジオ・シンセベース・ピアノ・スーパーソー。自作")
ONE_EAR = ["Aメロ1", "Bメロ1", "Aメロ2", "Bメロ2", "落ちサビ"]
finish(S, LY, V, 0,
       fx=[{"type": "noise", "scene": "ざわめき", "db": -20, "cut": 0.8},
           {"type": "width", "scenes": ONE_EAR, "mode": "left"},
           {"type": "width", "scenes": ["サビ1", "サビ2", "最後のサビ"], "mode": "wide", "amount": 0.5}],
       level={"verse": -0.3}, special={"落ちサビ": -0.6, "最後のサビ": 0.5, "おはよう": -0.1})
