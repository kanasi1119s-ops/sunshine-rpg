# vt3 13「お弁当交換条約」Lunchbox Treaty（仮）— シンセのファンク（Kawaii future bass の音）。96・4/4。C のドリア（短調にラのナチュラル）。
# 第3弾（0時〜24時の街）の 12時。表は docs/sound/vt3-plan.md。
#
# v2（2026-11-15）: ゼロから作り直し。人間の指示（2026-11-15）: 6ジャンル（この曲はファンク）・構成を今までと変える・電子音は Kawaii future bass。
#   v1 はニュージャックスウィングだった。09（スラップベースのファンク・E・108）とは、調（短調のドリア）・主役（FM のベースとサックス風のリード）・構成を変える。
#
# 構成（Aメロ・Bメロ・サビの形を使わない）: サビから始まる。そのあとは2人の「かけ合い」（1小節ずつ、クリアの声とキュートの声が交代で話す）で進む。
#   頭のサビ → リフ → かけ合い1（おかずの交渉）→ サビ → リフ → かけ合い2（みんなが集まる）→ 条約（手拍子とベースだけ。「じょうやく・ていけつ」）
#   → 最後のサビ（2回り）→ リフで終わり、最後に全員の1打（あくしゅ）
#
# 物語: 昼休み。たまごやきとからあげの交換から始まる、おかずの交渉。「ふたつとひとつでどう」「よくばりだなあ」「成立」。
#   みんなが集まってきて、つくえの上は世界地図になる。さかいめなんて、いらない。
#   アルバムの考え「幸せで美しい物語に書き換えて行く」は、言葉でなく景色で表す: ひとりで食べるお弁当が、みんなの味でにぎやかになる。分けたら2つになる。
#
# 曲を決める表:
#   旋律: サビ＝「こ・う・か・ん・し・よ」を8分6つで言い切る → 次の小節で5音の返事（裏から入る）。かけ合い＝16分2つから入る7音を、1小節ごとに2人が交代
#   和音: i7 → IV7 のひとつの型（ドリアのヴァンプ）。サビの後半だけ ♭VI → ♭VII → i
#   ベース: FM のベースのリフ（根音 → オクターブ上 → ♭7 → 5度。16分のすき間が多い）
#   この曲だけ: ①サビから始まる ②2人の声のかけ合いが「Aメロ」の代わり ③手拍子とベースだけの「条約」の場面 ④最後は全員の1打で終わる
#   音色（Kawaii future bass）: kfbFmBass・kfbSquarePluck（短い刻み）・kfbGlassEp・kfbSawStab・kfbFutureSax・kfbSub
from vt25_lib import *

S = Song("13", "lunchbox", "お弁当交換条約（仮）", "Lunchbox Treaty", 96, 4, "C", "minor", "シンセのファンク（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --space room --space-wet 0.1"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.45
S.keepers = {}
K = Key("C", "minor")          # oct 4 で 1 = C4。ドリアの「ラ」は #6

C_CH = ["Cm7", "F7", "Cm7", "F7", "Abmaj7", "Bb", "Cm7", "Cm7"]
K_CH = ["Cm7", "F7", "Cm7", "F7", "Ebmaj7", "F7", "Gm7", "G7"]
R_CH = ["Cm7", "F7", "Cm7", "F7"]

S.scene("頭のサビ", 8, "chorus", C_CH)
S.scene("リフ", 8, "break", R_CH + R_CH)
S.scene("かけ合い1", 16, "verse", K_CH + K_CH)
S.scene("サビ", 8, "chorus", C_CH)
S.scene("リフ2", 4, "break", R_CH)
S.scene("かけ合い2", 16, "verse", K_CH + K_CH)
S.scene("条約", 8, "bridge", ["Cm7", "Cm7", "Cm7", "Cm7", "Cm7", "Cm7", "Abmaj7", "G7"])
S.scene("最後のサビ", 16, "chorus", C_CH + C_CH)
S.scene("おわり", 12, "outro", R_CH + R_CH + ["Cm7", "F7", "Cm7", "Cm7"])

V = Voice(S, vol=0.2, delay=0.4, bright=0.0, patch="kfbSineLead" if VOCAL else "kfbFutureSax", low=False)   # v6: 歌のない版の旋律はサックス風のリード（サイン波のリードで16分の語りを弾くと、その場面だけ採点が 7.1〜7.4 に落ちた。リフの場面は 7.7〜7.9）
FMB = S.track("FM のベース（リフ）", "bass", patch="kfbFmBass", volume=0.1, pan=0, duck=0.25)
SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.03, pan=0, duck=0.5)
CHK = [S.track(f"プラックの短い刻み{i + 1}", "lead", patch="kfbSquarePluck", volume=0.04, pan=-0.4 + 0.15 * i, reverb=0.15) for i in range(3)]
EP = [S.track(f"ガラスのエレピ{i + 1}", "lead", patch="kfbGlassEp", volume=0.055, pan=0.3 - 0.15 * i, reverb=0.25) for i in range(3)]
STAB = [S.track(f"電子の短い和音{i + 1}", "lead", patch="kfbSawStab", volume=0.034, pan=0.45 - 0.45 * i, reverb=0.2, duck=0.4,
                fx=[{"type": "filter", "kind": "highpass", "freq": 250, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 7000, "q": 0.6}]) for i in range(3)]
SAX = S.track("サックス風のリード（リフ）", "lead", patch="kfbFutureSax", volume=0.075, pan=0.15, reverb=0.3)
KDR = S.track("手拍子（電子のクラップ）", "guitar", patch="kawaiiFx", volume=0.065, pan=-0.05, reverb=0.1, modulate=False)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.045, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
HOOK = "5:0.5 5:0.5 7:0.5 1':0.5 1':0.5 7:1 R:0.5"
VC = [HOOK, "R:0.5 1':0.5 #6:0.5 5:0.5 4:1 5:0.5 R:0.5", HOOK, "R:0.5 3':0.5 1':0.5 #6:0.5 1':1 #6:0.5 R:0.5",
      "6:0.5 1':0.5 3':1 1':0.5 6:0.5 1':1", "7:0.5 2':0.5 2':1 7:1 R:1", "5:0.5 5:0.5 7:0.5 1':0.5 3':0.5 1':1 R:0.5", "R:4"]
C1 = "こうかんしよ/たまごやき/こうかんしよ/からあげと/ふたつとひとつでどう/こうかんしよ"
C2 = "こうかんしよ/みにとまと/こうかんしよ/はんばーぐ/それはすこしたかいな/こうかんしよ"
C3 = ("こうかんしよ/えがおとね/こうかんしよ/えがおをね/わけたらふたつになる/こうかんしよ/"
      "こうかんしよ/きょうのひも/こうかんしよ/あしたにも/じょうやくはえいえんに/こうかんしよ")
# かけ合い: 1小節ずつ、2人が交代（奇数の小節＝クリアの声・低め、偶数の小節＝キュートの声・高め）
PA = "R:0.5 1:0.25 1:0.25 3:0.5 4:0.5 5:0.5 4:0.5 3:0.5 R:0.5"
PBF = "R:0.5 #6:0.25 #6:0.25 1':0.5 #6:0.5 5:0.5 #6:0.5 1':0.5 R:0.5"
PAE = "R:0.5 3:0.25 3:0.25 5:0.5 7:0.5 5:0.5 3:0.5 5:0.5 R:0.5"
PGM = "R:0.5 5:0.25 5:0.25 7:0.5 2':0.5 7:0.5 5:0.5 7:0.5 R:0.5"
PG7 = "R:0.5 5:0.5 #7:0.5 2':0.5 4':1 R:1"
VK = [PA, PBF, PA, PBF, PAE, PBF, PGM, PG7]
K1 = ("たまごやきだよ/からあげひとつ/それじゃたりない/じゃあふたつでは/れもんもつけて/よくばりだなあ/てをうちましょう/せいりつ/"
      "とまとをふたつ/はんばーぐとは/つりあわないよ/にんじんつける/ぴーまんはなし/ちゅうもんおおい/これでさいごね/せいりつ")
K2 = ("みんなあつまる/わたしもいれて/おにぎりひとつ/つけものふたつ/つくえのうえは/せかいちずだね/さかいめなんて/いらない/"
      "ひとりでたべる/おべんとうがね/みんなのあじで/にぎやかになる/ははのあじにも/ともだちのあじ/まぜてしまおう/せいりつ")
VT = ["1:1 1:1 1:1 1:1", "R:4", "3:1 3:1 3:1 3:1", "R:4", "5:1 5:1 5:1 5:1", "R:4", "7:1 1':1 1':1 R:1", "R:4"]
CT = "じょうやく/ていけつ/はんこは/あくしゅ"
LY = Lyrics(S)


def put(name, lines, text, o=4):
    bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("頭のサビ", VC, C1)
put("かけ合い1", VK + VK, K1)
put("サビ", VC, C2)
put("かけ合い2", VK + VK, K2)
put("条約", VT, CT)
put("最後のサビ", VC + VC, C3)

# ================= ベースのリフ・和音 =================
root = lambda b: S.chords[b].split("|")[0].split("/")[0]


def riff(b, i, sparse=False):
    ch = S.chords[b]; r = low(ch, "F1"); o = r + 12
    up = tones(root(b), nm(r + 1), nm(r + 12)); t5 = next((m for m in up if (m - r) in (6, 7, 8)), r + 7); t7 = next((m for m in up if (m - r) in (10, 11)), r + 10); t3 = next((m for m in up if (m - r) in (3, 4)), r + 3)
    N = nm
    if sparse: FMB.bar(b, f"{N(r)}:0.75 R:1.75 {N(t7)}:0.5 {N(o)}:0.5 R:0.5")
    elif i % 2 == 0: FMB.bar(b, f"{N(r)}:0.75 R:0.25 {N(o)}:0.25 {N(t7)}:0.25 R:0.5 {N(t5)}:0.5 {N(t7)}:0.5 {N(o)}:0.5 R:0.5")
    else: FMB.bar(b, f"{N(r)}:0.75 R:0.25 {N(o)}:0.25 {N(t7)}:0.25 R:0.5 {N(t5)}:0.5 {N(t3)}:0.5 {N(t3 - 1)}:0.25 {N(t3)}:0.25 {N(t5)}:0.5")


CK_A = "R:0.5 x:0.25 x:0.25 R:0.5 x:0.25 R:0.25 R:0.5 x:0.25 x:0.25 R:0.5 x:0.5"       # プラックの16分の刻み（すき間を多く）
CK_B = "R:0.25 x:0.25 R:0.5 x:0.25 x:0.25 R:0.5 R:0.25 x:0.25 R:0.5 x:0.25 x:0.25 R:0.5"
EP_A = "R:1.5 x:0.5 R:1 x:1"
EP_L = "x:4"


def ch3(tracks, b, pat, c=64):
    v = sorted(voice(root(b), c, 3))
    for j in range(3): tracks[j].bar(b, " ".join(t.replace("x", nm(v[j])) for t in pat.split()))


SAX_RIFF = ["R:0.5 G4:0.25 Bb4:0.25 C5:0.5 Eb5:0.5 R:0.5 D5:0.5 C5:0.5 Bb4:0.5", "C5:1 R:0.5 A4:0.5 C5:0.5 Eb5:0.5 F5:1",
            "R:0.5 G4:0.25 Bb4:0.25 C5:0.5 G5:0.5 R:0.5 F5:0.5 Eb5:0.5 C5:0.5", "A4:0.5 C5:0.5 Eb5:0.5 F5:0.5 A5:1 R:1"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n in ("頭のサビ", "サビ", "最後のサビ"):
        j = i % 8
        riff(b, i); ch3(CHK, b, CK_A if j % 2 == 0 else CK_B, 67); ch3(EP, b, EP_L if j in (4, 5) else EP_A, 64)
        # 「こうかんしよ」の小節: 最後の半拍に電子の和音。返事の小節: 何も足さない（歌を聞かせる）。7・8小節目: サックス風のリードが答える
        if j in (0, 2): ch3(STAB, b, "R:3.5 x:0.5", 70)
        elif j in (4, 5) and n != "頭のサビ": ch3(STAB, b, "x:1.5 x:1.5 x:1", 67)
        elif j == 7: SAX.bar(b, SAX_RIFF[1] if (n != "最後のサビ" or i < 8) else SAX_RIFF[3])
    elif n in ("リフ", "リフ2"):
        riff(b, i); ch3(CHK, b, CK_A if i % 2 == 0 else CK_B, 67); SAX.bar(b, SAX_RIFF[i % 4])
        if i >= 4: ch3(EP, b, EP_A, 64)
    elif n in ("かけ合い1", "かけ合い2"):
        riff(b, i, sparse=(n == "かけ合い1" and i < 8))           # 1番の前半はベースを減らす（2人の声を前に）
        if n == "かけ合い2" or i >= 8: ch3(CHK, b, CK_B if i % 2 == 0 else CK_A, 67)
        if n == "かけ合い2": ch3(EP, b, EP_A, 64)
        if i % 8 == 7: ch3(STAB, b, "R:2 x:0.5 R:0.5 x:1", 70)    # 「成立」のあとに和音が2つ
    elif n == "条約":                                              # 手拍子とベースだけ
        if i % 2 == 0: FMB.bar(b, f"{nm(low(S.chords[b], 'F1'))}:1 R:3")
        else: riff(b, 1)
        if i == 7: ch3(STAB, b, "x:0.5 x:0.5 x:0.5 x:0.5 x:1 R:1", 67); SAX.bar(b, "G4:0.5 B4:0.5 D5:0.5 F5:0.5 G5:1 R:1")
    elif n == "おわり":
        if i < 10: riff(b, i); ch3(CHK, b, CK_A if i % 2 == 0 else CK_B, 67); SAX.bar(b, SAX_RIFF[i % 4]); ch3(EP, b, EP_A, 64)
        elif i == 10: FMB.bar(b, "C2:1 R:3"); ch3(STAB, b, "x:1 R:3", 72); ch3(EP, b, "x:1 R:3", 67)       # 全員の1打（あくしゅ）
    if n in ("最後のサビ", "サビ") or (n == "おわり" and i < 10): SUB.bar(b, f"{nm(low(S.chords[b], 'F1'))}:1 R:3")

# ================= ドラム・手拍子 =================
HH = "x.xxx.xxx.xxx.xx"
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("頭のサビ", "サビ", "最後のサビ", "リフ", "リフ2", "おわり"):
        if n == "おわり" and i >= 10:
            if i == 10: D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 6)
            continue
        vgroove(D, b, "beat8", ghosts=0.3, seed=b, k="X.....x...X..x.." if i % 2 == 0 else "X..x......X.....", s="....X.......X..." if i % 4 != 3 else "....X..x....X...", h=HH, vary=False)
        if i % 8 == 0: crash(D, b, "C2", 4)
        if last and n not in ("最後のサビ", "おわり"): put_fill(D, b, "small" if n.startswith("リフ") else "snare16")
        if last and n == "最後のサビ": put_fill(D, b, "tomtrip")
        if n != "頭のサビ": KDR.bar(b, "R:1 B4:1 R:1 B4:1")
    elif n in ("かけ合い1", "かけ合い2"):
        if n == "かけ合い1" and i < 8: D.set(b, "X.........X.....", "....x.......x...", "x.x.x.x.x.x.x.x.")
        else: D.set(b, "X.....x...X....." if i % 2 == 0 else "X..x......X..x..", "....X.......X...", HH)
        if i % 8 == 7: put_fill(D, b, "small" if not last else "snare16")
        if n == "かけ合い2": KDR.bar(b, "R:1 B4:1 R:1 B4:0.5 B4:0.5" if i % 2 == 1 else "R:1 B4:1 R:1 B4:1")
    elif n == "条約":
        KDR.bar(b, "B4:1 B4:1 B4:1 B4:1" if i % 2 == 1 else "R:1 B4:1 R:1 B4:1")              # 歌の「じょ・う・や・く」に手拍子が答える
        D.set(b, "X...............", "................" if i < 7 else "X...X...X.X.XXXX", "................")

cym_swell(CYM, S.sc("サビ")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 4, "E4")

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の13（12時）。シンセのファンク（Kawaii future bass の音）。C のドリア・96。昼休みのおかずの交換が、みんなの条約になる。"
          "サビ「こうかんしよ」から始まり、2人の声のかけ合いで進む。FM のベースのリフ、プラックの刻み、サックス風のリード、手拍子。自作")
finish(S, LY, V, 0,
       level={"verse": -0.15}, special={"条約": -0.4, "最後のサビ": 0.4})

# ================= 仕上げのあとに足すもの =================
from vt3x_lib import *
path = sys.argv[1]
set_parts(path, "ハイハット", swing16=0.18)
humanize(path, "プラックの短い刻み", mid=78, down=12, up=8, seed=3); humanize(path, "FM のベース", mid=88, down=8, up=8, seed=5)
if VOCAL:
    backing(path, 0.9)   # 2026-11-13 人間「声以外のバック音量0.9ぐらいにしようか」
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 6, "chorus": 20, "最後のサビ": 24, "bridge": 4}, scoop=0.3, slash=0.7, vib_min_beats=1.5, vib_start=0.5, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ", 4, None, K), ("最後のサビ", 0, None, K)], vol=0.36)
    voice_by_scene(path, S, {}, default="clear")
    # かけ合い: 偶数の小節（2人目）はキュートの声にする（主の歌を、小節ごとに2つの歌に分ける）
    import copy
    js = load(path); main = js["vocals"][0]
    second = set(b for nme in ("かけ合い1", "かけ合い2") for q, b in enumerate(S.sc(nme)) if q % 2 == 1)
    A, B, t = [], [], 0.0
    for tok in main["notes"].split():
        L_ = float(tok.split(":")[1]); bi = int((t + 1e-6) // 4); t += L_
        if tok.startswith("R:"): A.append(tok); B.append(tok)
        elif bi in second: A.append(f"R:{L_:g}"); B.append(tok)
        else: A.append(tok); B.append(f"R:{L_:g}")
    cute = copy.deepcopy(main); cute.update(copy.deepcopy(TETO_VOICES["cute"])); cute["notes"] = " ".join(B); cute["pan"] = 0.25
    main["notes"] = " ".join(A); main["pan"] = -0.1; js["vocals"].insert(1, cute)
    print("  かけ合いの2人目（キュート）:", sum(1 for x in B if not x.startswith("R:")), "音")
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.4
    save(path, js)
