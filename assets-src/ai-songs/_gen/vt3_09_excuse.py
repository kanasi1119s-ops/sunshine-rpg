# vt3 09「遅刻の言いわけ選手権」Late-Excuse Championship（仮）— ファンク。110・4/4。E（Aメロはブルースのミクソリディアン、サビは長調）。
# 第3弾（0時〜24時の街）の 8時。表は docs/sound/vt3-plan.md。
# 物語: 8時のチャイムが鳴り終わる。校門の前で息を切らす「わたし」は、遅刻の言いわけを考え始める。
#   「ねこが道をふさいでいた」→「雲に乗って海を渡っていた」→「とちゅうで虹を渡って、鼻歌をうたっていた」と、どんどん大げさに。
#   教室のドアを開けると、みんなの視線がいっせいにこっちへ。先生もぷっと笑い出す。けっきょく最後は、ほんとうの言葉で「ごめんなさい」。
# 場面と強さ: ブレイク（ドラムだけ）→ イントロ（カッティングとベースとホーン・中）→ Aメロ1（語るような16分・中）→ Bメロ1（ふくらむ・止め）
#   → サビ1（強）→ 間奏（ホーンの合いの手・ベースが節）→ Aメロ2（もっと大げさに）→ Bメロ2 → サビ2
#   → ブレイク2（ベースとクラビネット風の鍵盤だけ）→ 最後のサビ（いちばん強い）→「すみません」の一言で止める
# 旋律の性格: 細かい言葉遊びの16分（B3〜E5）、ブルーノート（♭3・♭7）の飾り。サビは長調で明るく開く。
# この曲だけの音: 16分のカッティングギターとゴーストノートのドラム、ホーンの短い合いの手。最後は歌（またはホーン）の「すみません」だけで止める。
#   合いことばの節（3・5・6・5・2）は、間奏でベースが弾く（G#・B・C#・B・F#）。
from vt25_lib import *

S = Song("09", "excuse", "遅刻の言いわけ選手権（仮）", "Late-Excuse Championship", 110, 4, "E", "major", "ファンク（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --space room --space-wet 0.1"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.5
S.keepers = {"Aメロ1": "closed", "Aメロ2": "closed", "サビ2": "open", "最後のサビ": "open"}
K = Key("E", "major")          # oct 4 で 1 = E4

A_CH = ["E9", "E9", "A9", "E9", "E9", "E9", "G6", "A9"]
B_CH = ["C#m7", "F#m7", "A", "B7#9", "C#m7", "F#m7", "A", "B7#9"]
C_CH = ["Amaj7", "G#m7", "F#m7", "E9", "Amaj7", "G#m7", "F#m7", "B7sus4"]

S.scene("ブレイク", 2, "intro", ["E9", "E9"])
S.scene("イントロ", 8, "intro", ["E9", "E9", "A9", "B7#9"])
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 8, "break", ["E9", "E9", "A9", "B7#9"])
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("ブレイク2", 8, "bridge", ["E9", "E9", "A9", "E9", "E9", "E9", "A9", "B7#9"])
S.scene("最後のサビ", 16, "chorus", C_CH)
S.scene("すみません", 2, "outro", ["E9", "E9"])

V = Voice(S, vol=0.2, delay=0.5, bright=0.1, patch="surgeParaphonic", low=False)
CUTL = [S.track(f"カッティング L{i + 1}", "guitar", amp="jpopClean", volume=0.05, pan=-0.6, reverb=0.12, chorus=0, sustain=0.25) for i in range(3)]
CUTR = S.track("カッティング R（単音）", "guitar", amp="jpopClean", volume=0.06, pan=0.6, reverb=0.12, chorus=0, sustain=0.25)
CLV = [S.track(f"クラビネット風の鍵盤{i + 1}", "keys", patch="surgeKeysDxTonez", volume=0.05, pan=0.25, reverb=0.15, sustain=0.3) for i in range(3)]
TP = S.track("トランペット", "brass", patch="trumpet", volume=0.09, pan=0.2, reverb=0.22)
SX = S.track("アルトサックス", "brass", patch="altoSax", volume=0.09, pan=-0.1, reverb=0.22)
TB = S.track("トロンボーン", "brass", patch="trombone", volume=0.08, pan=-0.25, reverb=0.22)
BASS = S.track("ベース（指弾き）", "bass", **finger_bass_spec(vol=0.24))
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 5,:0.25 5,:0.25 b7,:0.5 5,:0.5 4,:0.25 3,:0.25 1:0.5 R:1".replace("1:0.5", "1:0.5"),
      "R:0.5 3:0.25 3:0.25 5:0.5 3:0.5 1:1 R:1",
      "R:0.5 5:0.25 5:0.25 b7:0.5 1':0.5 b7:0.25 5:0.25 4:0.5 R:1",
      "R:0.5 4:0.25 4:0.25 3:0.5 1:0.5 b3:0.5 1:0.5 R:1",
      "R:0.5 1':0.25 1':0.25 b7:0.5 5:0.5 b7:0.25 1':0.25 b7:0.5 R:1",
      "R:0.5 5:0.25 5:0.25 4:0.5 3:0.5 1:1 R:1",
      "R:0.5 4:0.5 4:0.5 3:0.5 4:0.5 5:0.5 b7:1", "5:2 R:2"]
VA[0] = "R:0.5 5:0.25 5:0.25 b7:0.5 5:0.5 4:0.25 3:0.25 1:0.5 R:1"
A1 = ("はちじのちゃいむ/なりおわる/こうもんしまる/いきがきれる/いいわけさがし/なにがいい/ねぼうじゃだめだ/ほんとうなのに/"
      "ろうかをあるく/あしおとで/せんせいのかお/うかんでくる/まずはこうだよ/ねこがみち/ふさいでいたって")
A1 = A1.replace("/ほんとうなのに", "")   # 15句（7句＋8句）: 2つ目の Aメロの最後の句まで
A2 = "もっとおおげさに/くもにのり/うみをわたってた/かぜがつよい/おまけにとちゅう/にじわたる/はなうたうたって"
VB = ["R:1 3:0.5 4:0.5 5:1 5:1", "6:1 5:1 3:1 R:1", "R:1 4:0.5 5:0.5 6:1 6:1", "7:1 6:1 5:1 R:1",
      "R:1 5:0.5 6:0.5 7:1 7:1", "1':1 7:1 6:1 R:1", "R:0.5 5:0.5 6:0.5 7:0.5 1':0.5 2':0.5 1':0.5 7:0.5", "R:4"]
B1 = "いいわけのたね/ふくらんでいく/うそじゃないけど/ほんとでもない"
B2 = "きょうしつのどあ/てをかけたらさ/みんなのしせん/ぜんぶこっちむく"
VC = ["R:0.5 5:0.5 1':0.5 1':0.5 2':0.75 1':0.25 6:1", "5:1.5 3:0.5 3:1 R:1",
      "R:0.5 4:0.5 6:0.5 6:0.5 1':0.75 6:0.25 5:1", "4:2 R:2",
      "R:0.5 3:0.5 5:0.5 5:0.5 1':0.75 7:0.25 6:1", "5:1 6:0.5 5:0.5 3:1 R:1",
      "R:0.5 2:0.5 3:0.5 4:0.5 5:0.5 6:0.5 5:0.5 4:0.5", "5:2 R:2",
      "R:0.5 5:0.5 1':0.5 1':0.5 2':0.75 1':0.25 6:1", "5:1.5 3:0.5 3:1 R:1",
      "R:0.5 4:0.5 6:0.5 6:0.5 1':0.75 6:0.25 5:1", "4:2 R:2",
      "R:0.5 1':0.5 1':0.5 2':0.5 1':0.75 7:0.25 6:1", "5:1 3:0.5 5:0.5 1':1 R:1",
      "R:0.5 6:0.5 5:0.5 4:0.5 3:0.5 2:0.5 3:0.5 2:0.5", "1:3 R:1"]
C1 = ("いいわけせんしゅけん/ゆうしょうはだれ/おおきなはなしほどね/きらきらひかるの/"
      "いいわけせんしゅけん/わたしがでるよ/せんせいもおもわずね/ぷっとわらいだした")
C2 = ("いいわけせんしゅけん/ゆうしょうはだれ/くもにのってにじをこえ/はなうたうたったの/"
      "いいわけせんしゅけん/ゆうしょうはむり/でもみんながわらってる/それならいいかな")
C3 = ("いいわけせんしゅけん/けっきょくさいごは/ほんとうのことばでね/ごめんなさいだよ/"
      "いいわけせんしゅけん/あしたはちこく/しないようにはやおき/めざましかけるよ")
LY = Lyrics(S)


def put(name, lines, text, o=4):
    bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", VA + VA, A1)
put("Bメロ1", VB, B1)
put("サビ1", VC, C1)
put("Aメロ2", VA, A2)
put("Bメロ2", VB, B2)
put("サビ2", VC, C2)
put("最後のサビ", VC, C3)
if VOCAL: put("すみません", ["R:1.5 5:0.5 5:0.5 4:0.5 3:0.5 1:0.5", "R:4"], "すみません")
else: SX.bar(S.sc("すみません")[0], K.mel("R:1.5 5:0.5 5:0.5 4:0.5 3:0.5 1:0.5", oct=4))

# ================= カッティング・鍵盤・ホーン =================
def cut16(b, ch, pat):
    v = voice(ch, 64, 3); hits = [q for q, c in enumerate(pat) if c in "xX"]
    for j in range(3):
        toks, t = [], 0
        for q in hits:
            if q > t: toks.append(f"R:{(q - t) * 0.25:g}")
            toks.append(f"{nm(v[j])}:0.25{'!' if pat[q] == 'X' else ''}"); t = q + 1
        if t < 16: toks.append(f"R:{(16 - t) * 0.25:g}")
        CUTL[j].bar(b, " ".join(toks))


def single(b, ch):
    t = tones(ch, "E4", "E5")
    CUTR.bar(b, f"R:0.25 {nm(t[0])}:0.25 R:0.5 {nm(t[1])}:0.25 R:0.25 {nm(t[0])}:0.25 R:0.25 R:0.5 {nm(t[2 % len(t)])}:0.25 R:0.25 {nm(t[1])}:0.25 R:0.75")


def clav(b, ch, pat="R:0.5 x:0.25 R:0.25 x:0.25 R:0.75 x:0.25 R:0.25 x:0.5 R:1"):
    v = voice(ch, 62, 3)
    for j in range(3): CLV[j].bar(b, " ".join(t.replace("x", nm(v[j])) for t in pat.split()))


def horns(b, ch, pat):
    v = voice(ch, 67, 3)
    TP.bar(b, pat.replace("x", nm(v[2]))); SX.bar(b, pat.replace("x", nm(v[1]))); TB.bar(b, pat.replace("x", nm(v[0] - 12)))


CUTP = ["X.x.x..xX.x..x.x", "x.x..xx.x.x.xx.x"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "イントロ":
        cut16(b, ch, CUTP[i % 2]); single(b, ch) if i >= 4 else None
        if i % 2 == 1: horns(b, ch, "R:2.5 x:0.25 R:0.25 x:0.5 x:0.5")
    elif n in ("Aメロ1", "Aメロ2"):
        cut16(b, ch, CUTP[i % 2])
        if n == "Aメロ2" or i >= 8: single(b, ch)
        if i % 4 == 3: horns(b, ch, "R:3 x:0.25 R:0.25 x:0.5")
    elif n in ("Bメロ1", "Bメロ2"):
        cut16(b, ch, "x.x.x.x.x.x.x.x."); clav(b, ch)
        if i < 7 and i % 2 == 1: horns(b, ch, "R:2 x:1 x:1")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        cut16(b, ch, CUTP[i % 2]); single(b, ch)
        if i % 2 == 1: horns(b, ch, "R:2.5 x:0.25 R:0.25 x:0.5 x:0.5" if i % 4 == 1 else "R:3 x:0.5 x:0.5")
        if n == "最後のサビ": clav(b, ch)
    elif n == "間奏":
        cut16(b, ch, CUTP[i % 2])
        horns(b, ch, ["x:0.5 R:0.25 x:0.25 R:1 x:0.5 x:0.5 R:1", "R:2 x:0.25 x:0.25 x:0.5 R:1"][i % 2])
    elif n == "ブレイク2":
        clav(b, ch, "x:0.25 R:0.5 x:0.25 R:0.5 x:0.25 R:0.25 x:0.25 R:0.5 x:0.25 R:0.5 x:0.5")
        if i >= 4: cut16(b, ch, CUTP[i % 2])
    elif n == "すみません":
        if i == 0: horns(b, ch, "x:0.5! R:3.5")

# ================= ベース（指弾き・ゴースト）=================
MOTIF = ["R:2 G#2:0.5 B2:0.5 C#3:1", "B2:0.5 F#2:1.5 R:2"]     # 合いことばの節（3・5・6・5・2）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    funk = f"{nm(r)}:0.5 R:0.25 {nm(r)}:0.25 R:0.5 {nm(r + 12)}:0.25 R:0.25 {nm(r + 10)}:0.5 {nm(r + 7)}:0.25 R:0.25 {nm(r)}:0.25 {nm(r + 3)}:0.25 {nm(r + 4)}:0.5"
    if n == "間奏" and i in (2, 3): BASS.bar(b, MOTIF[i - 2])
    elif n in ("イントロ", "Aメロ1", "Aメロ2", "間奏", "サビ1", "サビ2", "最後のサビ", "ブレイク2"):
        BASS.bar(b, funk if (n in ("イントロ", "Aメロ1", "Aメロ2", "間奏", "ブレイク2") or i % 2 == 0) else bass_line(S, b, "push", lo="E1"))
    elif n in ("Bメロ1", "Bメロ2") and i < 7: BASS.bar(b, bass_line(S, b, "root8", lo="E1"))
    elif n == "すみません" and i == 0: BASS.bar(b, f"{nm(r)}:0.5 R:3.5")

cym_swell(CYM, S.sc("サビ1")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 2, "E4")

# ================= ドラム（ファンク・ゴースト多め）=================
FK = ("X.....x...X..x..", "....X..o.o..X..o", "xxxxxxxxxxxxxxxx")
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "ブレイク":
        D.set(b, "X.....x...X.....", "....X..x.x..X..x", "x.x.x.x.x.x.x.x.") if i == 0 else D.set(b, "X.....x...X..x..", "....X..x.x..XxXx", "x.x.x.x.x.x.....")
    elif n in ("イントロ", "Aメロ1", "Aメロ2", "間奏", "ブレイク2"):
        if n == "ブレイク2" and i < 4: D.set(b, "X.........X.....", "....X.......X...", "x.x.x.x.x.x.x.x."); continue
        vgroove(D, b, "beat8", ghosts=0.6, seed=b, k=FK[0], s=FK[1], h=FK[2])
        if i == 0 and n != "Aメロ1": crash(D, b)
        if i % 8 == 7 and not last: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
    elif n in ("Bメロ1", "Bメロ2"):
        if i < 7: vgroove(D, b, "beat8", ghosts=0.5, seed=b, k="X.......X.X.....", s="....X.......X...", h="x.x.x.x.x.x.x.x.")
        if i == 6: put_fill(D, b, "build")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        vgroove(D, b, "beat8", ghosts=0.5, seed=b, k="X.....x.X.....x.", s="....X..o....X..o", h="x.xOx.x.x.xOx.x.".replace("O", "x"))
        if i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
        if i % 8 == 7 and not last: put_fill(D, b, "small")
        if last and n != "最後のサビ": put_fill(D, b, "tomdown")
    elif n == "すみません":
        if i == 0: D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 6)

for name in ("Bメロ1", "Bメロ2"): SIL.add(S.sc(name)[-1], 0, 4)          # 1小節の止め
SIL.add(S.sc("すみません")[0], 0, 1.5)                                    # 「すみません」の前の一瞬だけ、伴奏を止める
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の09（8時）。ファンク。E・110。遅刻の言いわけがどんどん大げさになっていく。"
          "16分のカッティングギター・ゴーストノートのドラム・指弾きのベース・ホーン。合いことばの節は間奏のベース。最後は「すみません」だけで止める。自作")
finish(S, LY, V, 0,
       level={"verse": -0.15}, special={"ブレイク2": -0.4, "最後のサビ": 0.4})
