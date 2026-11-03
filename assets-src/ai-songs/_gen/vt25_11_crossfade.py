# vt25 11「片想いクロスフェード」Crush Crossfade（仮）— ダンス（UK ガラージ）。134・4/4。D の短調（サビは F 長調）→ 最後のサビは +1（G♭）。
# 物語: 好きな人のプレイリストを、夜にこっそり聞いている。1曲目は明るい歌、2曲目は切ないバラード。曲が変わるたびに、こころも変わる。
#   明日「好きです」と言うって決めたのに、次の曲はやきもちの歌で、やめようかなと指が止まる。シャッフルのボタンを押して、運命まかせ。
#   この曲が終わるまでに決めなきゃ。曲と曲のすきまの静けさで、息を吸う。最後は、わたしの歌が、きみの世界へ流れだす。
# 場面と強さ: 前の曲（別の曲＝ピアノのバラードが、フェードで消えていく）→ イントロ（2ステップと声のチョップ）→ Aメロ1（語る）→ Bメロ1
#   → サビ1（強）→ クロスフェード（間奏で別の曲調＝バラードへ移り、また戻る）→ Aメロ2 → Bメロ2 → サビ2
#   → 曲と曲のすきま（ほとんど無音・とても弱い）→ 最後のサビ（+1・いちばん強い）→ 次の曲へ（フェードで別の曲調へ移りながら終わる）
# 旋律の性格: 跳ねる2ステップのリズムで、短い句で揺れる（A3〜A4）。サビは「クロスフェードして」の8音が毎回同じ形（C5 C5 D5 C5 A4 C5）。
# ほかの曲とちがう所（この曲だけの音）: 間奏で、曲そのものが別の曲調（ピアノとストリングスのバラード）へクロスフェードし、また戻ってくる。
#   始まりは「前の曲」が消えていくところから、終わりは「次の曲」へ移るところで終わる（プレイリストの中の1曲）。
from vt25_lib import *

S = Song("11", "crossfade", "片想いクロスフェード（仮）", "Crush Crossfade", 134, 4, "D", "minor", "ダンス（UK ガラージ・ボカロ）")
S.kit = "electro"
S.flags = S.flags + " --piano salamander --space room --space-wet 0.16"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.5
K = Key("D", "minor")           # Aメロ（oct 3 で 1 = D3。歌うのは A3〜A4）
KF = Key("F", "major")          # Bメロ・サビ（oct 4 で 1 = F4）
KL = Key("Gb", "major")         # 最後のサビ（+1）

A_CH = ["Dm9", "Bbmaj7", "Gm9", "A7"]
B_CH = ["Bbmaj7", "C", "Am7", "Dm7", "Bbmaj7", "C", "Gm7", "A7"]
C_CH = ["Bbmaj7", "C", "Am7", "Dm7", "Gm7", "C", "Fmaj7", "A7"]
C_CH2 = C_CH[:6] + ["Bbmaj7", "F"]
BAL = ["Fmaj7", "C/E", "Dm7", "Bbmaj7"]          # 別の曲（バラード）の和音
LAST = [tr_chord(c, 1) for c in C_CH + C_CH2]

S.scene("前の曲", 4, "intro", BAL)
S.scene("イントロ", 8, "intro", A_CH * 2)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH + C_CH2)
S.scene("クロスフェード", 16, "solo", A_CH + BAL * 2 + A_CH)
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH + C_CH2)
S.scene("すきま", 4, "break", ["Bbmaj7", "Bbmaj7", "Gm7", "Db7"])     # 最後の小節は +1 への入り口
S.scene("最後のサビ", 16, "chorus", LAST)
S.scene("次の曲へ", 8, "outro", [tr_chord(c, 1) for c in A_CH] + [tr_chord(c, 1) for c in BAL])

V = Voice(S, vol=0.21, delay=0.75, bright=0.6, patch="voiceLeadModern", low=True)
ORG = S.track("オルガンのベース（ガラージ）", "bass", **synth_bass_spec("synthBass1", vol=0.21, duck=0.35))
SUB = S.track("サブベース", "sub808", volume=0.12, pan=0, sustain=0.8, fx=[{"type": "filter", "kind": "highpass", "freq": 28, "q": 0.7}])
KEYS = [S.track(f"ガラージの和音{i + 1}", "keys", patch="surgeKeysNanowave2Oscs", volume=0.06, pan=-0.3 + 0.3 * i, reverb=0.25, sustain=0.4) for i in range(3)]
CHOP = S.track("声のチョップ", "pad", patch="vocalChop", volume=0.07, pan=0.3, reverb=0.25)
PADS = [S.track(f"パッド{i + 1}", "pad", **pad_spec("surgePadVerbPad", vol=0.035, pan=-0.35 + 0.35 * i, duck=0.4, sustain=1.4)) for i in range(3)]
# 別の曲（バラード）: ピアノとストリングス。クロスフェードのときだけ前に出る
BP = [S.track(f"別の曲のピアノ{i + 1}", "piano", volume=0.13, pan=-0.1, reverb=0.3, fx=[{"type": "eq", "low": -2, "mid": -2, "midHz": 400, "high": 2}]) for i in range(2)]
BS = [S.track(f"別の曲のストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.06, pan=-0.3 + 0.3 * i, reverb=0.45, sustain=1.5) for i in range(3)]
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.06, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.05, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 5:0.25 1':0.25 R:0.5 1':0.5 3':0.5 1':0.5 7:1", "1':1.5 R:2.5", "R:0.5 5:0.25 6:0.25 R:0.5 6:0.5 1':0.5 6:0.5 5:1", "#7:1.5 R:2.5"]
A1 = "きみのりすとを/よるにきいてる/さいしょのきょくは/あかるいうたで/つぎのきょくはね/せつないうたで/きょくがかわると/こころもかわる"
A2 = "あしたいうんだ/すきですってこと/でもつぎのきょく/しっとのうたでね/やめようかなと/ゆびがとまるの/しゃっふるのぼたん/うんめいまかせ"
VB = ["R:0.5 3:0.5 3:0.5 4:0.5 5:1 3:1", "2:1.5 1:0.5 2:1 R:1", "R:0.5 3:0.5 3:0.5 5:0.5 6:1 5:1", "3:1.5 2:0.5 1:1 R:1",
      "R:0.5 4:0.5 4:0.5 5:0.5 6:1 4:1", "5:1.5 4:0.5 3:1 R:1", "R:0.5 2:0.5 3:0.5 4:0.5 5:1 6:1", "#5:2 R:2"]
B1 = "このきょくがおわる/そのときまでにね/きめなきゃいけない/わたしのこと"
B2 = "いまながれてるの/きみのすきなうた/さびのまえまでに/いきをすうよ"
VC = ["R:0.5 5:0.25 5:0.25 R:0.5 6:0.5 5:0.5 3:0.5 5:1", "6:1 5:1 R:2", "R:0.5 3:0.25 3:0.25 R:0.5 5:0.5 3:0.5 2:0.5 3:1", "1:1 2:1 R:2",
      "R:0.5 5:0.25 5:0.25 R:0.5 6:0.5 5:0.5 3:0.5 1':1", "7:1 5:1 R:2", "R:0.5 3:0.5 5:0.5 6:0.5 7:1 6:1", "#5:2 R:2"]
VC2 = VC[:6] + ["R:0.5 3:0.5 5:0.5 6:0.5 5:1 3:1", "1:2 R:2"]
C1 = "くろすふぇーどして/きもちがゆれるよ/かなしいうたから/あかるいうた/くろすふぇーどして/つぎのきょくへとね/すきってきもちだけ/かわらないの"
C2 = "くろすふぇーどして/なみだのきょくもね/きみのすきなうた/だいすきだよ/くろすふぇーどして/ためらいのおとも/ゆっくりとけていく/ほらきえたよ"
CL = "くろすふぇーどして/あしたのわたしへ/すきですっていうよ/このきょくでね/くろすふぇーどして/きみのせかいへと/わたしのうたがね/ながれだすよ"
LY = Lyrics(S)


def put(name, key, lines, text, o):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA * 4, A1, 3)
put("Bメロ1", KF, VB, B1, 4); put("Bメロ2", KF, VB, B2, 4)
put("サビ1", KF, VC + VC2, C1, 4); put("サビ2", KF, VC + VC2, C2, 4)
put("最後のサビ", KL, VC + VC2, CL, 4)
if VOCAL: put("Aメロ2", K, VA * 4, A2, 3)
else:
    for i, (b, l) in enumerate(zip(S.sc("Aメロ2"), VA * 4)):
        if i < 8: CHOP.bar(b, K.mel(l, oct=4))
        else: V.bar(b, K.mel(l, oct=3))

# ================= 別の曲（バラード）の部品 =================
BALM = ["A5:2 G5:1 F5:1", "E5:3 C5:1", "D5:1.5 E5:0.5 F5:1 A5:1", "G5:4"]


def ballad(b, i, vel=""):
    ch = S.chords[b]; v = voice(ch, 64, 4); r = low(ch, "C2")
    BP[0].bar(b, f"{nm(r)}{':2' + vel} {nm(r + 7)}{':2' + vel}")
    BP[1].bar(b, BALM[i % 4].replace(":", ":", 1) if not vel else " ".join(x + vel for x in BALM[i % 4].split()))
    sv = voice(ch, 62, 3)
    for j in range(3): BS[j].bar(b, f"{nm(sv[j])}:4{vel}")


for i, b in enumerate(S.sc("前の曲")): ballad(b, i, "," if i >= 2 else "")      # 前の曲が消えていく（後半は弱く）
for i, b in enumerate(S.sc("クロスフェード")):
    if 4 <= i < 12: ballad(b, i, "," if i in (4, 5, 10, 11) else "")
for i, b in enumerate(S.sc("次の曲へ")):
    if i >= 2: ballad(b, i, "," if i < 5 else "")

# ================= ガラージの部品 =================
GARAGE_BARS = []
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "前の曲" or n == "すきま": continue
    if n == "クロスフェード" and 6 <= i < 10: continue                  # 真ん中はバラードだけ
    if n == "次の曲へ" and i >= 6: continue
    GARAGE_BARS.append(b)
    ch = S.chords[b]; v = voice(ch, 65, 3); r = low(ch, "E1")
    soft = "," if (n == "クロスフェード" and i in (4, 5, 10, 11)) or (n == "次の曲へ" and i >= 3) else ""
    # ガラージの和音: 2ステップの位置で短く
    for j in range(3): KEYS[j].bar(b, f"R:0.75 {nm(v[j])}:0.25{soft} R:1 {nm(v[j])}:0.5{soft} R:0.25 {nm(v[j])}:0.25{soft} R:1")
    # オルガンのベース: 跳ねる
    if n not in ("Aメロ1",) or i >= 4:
        ORG.bar(b, f"{nm(r)}:0.75{soft} R:0.25 {nm(r + 12)}:0.25 R:0.75 {nm(r)}:0.5 {nm(r + 10)}:0.25 R:0.25 {nm(r + 7)}:0.5 R:0.5")
    if n.startswith(("サビ", "最後")): SUB.bar(b, f"{nm(r)}:1.5 R:0.5 {nm(r)}:1 R:1")
    if n.startswith(("サビ", "最後")) or n == "Bメロ1" or n == "Bメロ2":
        pv = voice(ch, 60, 3)
        for j in range(3): PADS[j].bar(b, f"{nm(pv[j])}:4")
    if n in ("イントロ",) or (n.startswith(("サビ", "最後")) and i % 4 == 3):
        t = tones(ch, "A4", "A5")
        CHOP.bar(b, f"R:0.5 {nm(t[2])}:0.25 {nm(t[2])}:0.25 R:0.5 {nm(t[1])}:0.25 R:0.25 {nm(t[3 % len(t)])}:0.5 R:0.5 {nm(t[2])}:0.25 R:0.75")
for i, b in enumerate(S.sc("すきま")):
    if i >= 2:
        pv = voice(S.chords[b], 60, 3)
        for j in range(3): PADS[j].bar(b, f"{nm(pv[j])}:4,")
riser(FX, S.sc("最後のサビ")[0], 4, "C4")
cym_swell(CYM, S.sc("サビ1")[0], 2, "C4")

# ================= ドラム（2ステップ。前の曲・真ん中のバラード・すきまでは止まる） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if b not in GARAGE_BARS:
        if n == "クロスフェード" and 6 <= i < 10 and i % 2 == 1: D.set(b, "X.......X.......", "....X.......X...", "................")  # バラードの静かなドラム
        continue
    if n == "イントロ":
        vgroove(D, b, "twostep", ghosts=0.2, seed=b, s="................" if i < 4 else None)
        if i == 4: crash(D, b)
    elif n in ("Aメロ1", "Aメロ2"):
        vgroove(D, b, "twostep", ghosts=0.25, seed=b)
        if i == 0: crash(D, b, "C2", 3)
        if last: put_fill(D, b, "small")
    elif n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "halfdrive", ghosts=0.25, seed=b)
        if i == 6: put_fill(D, b, "build")
    elif n.startswith(("サビ", "最後")):
        vgroove(D, b, "twostep", ghosts=0.3, seed=b, k="X.......X.X...X.", h="x.xOx.x.x.xOx.xx")
        if i % 8 == 0: crash(D, b, "C2", 4)
        if i % 8 == 7 and not last: put_fill(D, b, "small")
    elif n == "クロスフェード":
        vgroove(D, b, "twostep", ghosts=0.2, seed=b, s=("....o.......o..." if i in (4, 5, 10, 11) else None))
    elif n == "次の曲へ":
        vgroove(D, b, "twostep", ghosts=0.1, seed=b, s=("................" if i >= 3 else None))

# 曲と曲のすきま: はじめの2小節は完全な無音
SIL.add(S.sc("すきま")[0], 0, 4); SIL.add(S.sc("すきま")[1], 0, 4)
SIL.apply()

S.fade_in = 0; S.fade_out = 6
S.desc = ("仮: 重音テトのボカロ曲25曲・第2弾の11。ダンス（UK ガラージ）。D の短調（サビは F）・134、最後のサビは +1。"
          "好きな人のプレイリストを聞きながら、曲が変わるたびに気持ちが揺れる。前の曲（ピアノのバラード）が消えていくところから始まり、2ステップのリズム、"
          "間奏で曲そのものがバラードへクロスフェードしてまた戻る、曲と曲のすきまの無音、最後は次の曲へ移りながらフェードで終わる。自作")
finish(S, LY, V, 0, level={"verse": -0.25}, special={"最後のサビ": 0.5})
