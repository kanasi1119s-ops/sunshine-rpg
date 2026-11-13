# vt3 09「遅刻の言いわけ選手権」Late-Excuse Championship（仮）— スラップベースのエレクトロ・ファンク（ギターなし）。108・4/4。E（Aメロはブルースの色、サビは明るく）。
# 第3弾（0時〜24時の街）の 8時。表は docs/sound/vt3-plan.md。
#
# v4（2026-11-13）: ゼロから作り直し（人間「全ての曲を1みたいにこだわって作って」「このレベル（02 v7）まで詰めて曲作って」）。
#   v1〜v3 はギターのカッティングとホーンのファンク。ギターは使わず（ギターに聞こえない音は使わない決まり）、ホーンは 04・08 で使ったので使わない。
#   主役はスラップベースのリフ。和音は FM のエレピの短い刻みと電子の短い和音、合いの手は矩形波のプラックの駆け上がり（人間が気に入った「ピロピロピロピーン」の音）。
#
# 物語: 8時のチャイムが鳴り終わる。校門の前で息を切らす「わたし」は、遅刻の言いわけを考え始める。
#   「ねこが道をふさいでいた」→「雲の船で海をこえた」→「虹の下まで行った」と、どんどん大げさに。教室のドアを開けると、先生までふきだして、教室じゅうが大笑い。
#   アルバムの考え「幸せで美しい物語に書き換えて行く」は、言葉でなく景色で表す: しかられるはずの時間が、拍手で終わる舞台になる。
#   最後はほんとうのこと（鼻歌が聞こえて足を止めた・朝の光に見とれていた）を言って、「ごめんなさい」。
#
# 曲を決める表（書く前に similar_check.py --plan で確かめる）:
#   形: ドラムだけ → スラップベースのリフ → Aメロ1（リフと歌だけ → 後半エレピ）→ Bメロ（のばす和音・止め）→ サビ1（「ちがうんです」とプラックの答え）
#       → 間奏 → Aメロ2（言いわけが大きくなる: プラックが歌の句ごとに高くなる）→ Bメロ2 → サビ2 → ほんとは（ベースとエレピだけ・白状）→ 最後のサビ → リフで終わり、最後に1拍の止め
#   旋律: Aメロ＝16分の弱起から8分で早口に語る7音 → 次の小節で5音の答え（♭3・♭7 のブルースの色）。Bメロ＝4分の長い音でためる。
#         サビ＝「ち・が・う・ん・で・す」を8分6つで言い切る → 次の小節で6音の言いわけ。後半は長い音で話をふくらませる
#   和音: Aメロ I7 → IV7 のひとつの型（ファンクのヴァンプ）。サビは I → ♭VII → IV → I（ミクソリディアンの明るさ）、後半 vi → V → IV → I/III → ii → IV → Vsus
#   ベース: スラップのリフが主役（同じ音を続けて打たない。人間「同じ音を連打する所で引っかかる感じがする」）。サビは和音を追って、オクターブ上をはじく
#   この曲だけ: ①スラップベースのリフが主役 ②言いわけが大きくなるたびに、プラックの駆け上がりが高くなる ③最後の「ごめんなさい」のあと1拍で止める
#
# ファンクの作り方（2026-11-13。作曲ソフトの手引き: bpm 95〜115、スラップベースの16分のシンコペーション、短い和音の刻み。
#   ハイハットは16分を少しはねさせ、キックとベースの打つ場所をそろえ、1拍目を強く、すき間を残す）
from vt25_lib import *

S = Song("09", "excuse", "遅刻の言いわけ選手権（仮）", "Late-Excuse Championship", 108, 4, "E", "major", "スラップベースのエレクトロ・ファンク（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --space room --space-wet 0.12"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.45
S.keepers = {}
K = Key("E", "major")          # oct 4 で 1 = E4

A_CH = ["E7", "E7", "A7", "E7", "E7", "E7", "A7", "B7"]
B_CH = ["C#m7", "F#7", "C#m7", "F#7", "A", "A", "B7sus4", "B7"]
C_CH = ["E", "D", "A", "E", "E", "D", "A", "B7", "C#m7", "B", "A", "E/G#", "F#m7", "A", "B7sus4", "B7"]

S.scene("ドラム", 2, "intro", ["E7", "E7"])
S.scene("リフ", 8, "intro", A_CH)
S.scene("Aメロ1", 16, "verse", A_CH + A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 4, "break", A_CH[:4])
S.scene("Aメロ2", 16, "verse", A_CH + A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("ほんとは", 8, "bridge", ["E7", "E7", "A7", "A7", "E7", "E7", "B7sus4", "B7"])
S.scene("最後のサビ", 16, "chorus", C_CH)
S.scene("おわり", 4, "outro", ["E7", "E7", "A7", "E7"])

V = Voice(S, vol=0.2, delay=0.4, bright=0.0, patch="kfbSineLead" if VOCAL else "kfbFutureSax", low=False)
SLAP = S.track("スラップベース（リフ）", "slap", volume=0.2, pan=0, reverb=0.05)
EP = [S.track(f"FM のエレピ{i + 1}", "fmEpiano", volume=0.075, pan=-0.3, reverb=0.2, sustain=0.5) for i in range(3)]
EPL = [S.track(f"FM のエレピ（のばす{i + 1}）", "fmEpiano", volume=0.06, pan=-0.2, reverb=0.3, sustain=1.5) for i in range(3)]
STAB = [S.track(f"電子の短い和音{i + 1}", "lead", patch="kfbSawStab", volume=0.034, pan=0.45 - 0.2 * i, reverb=0.2, duck=0.4,
                fx=[{"type": "filter", "kind": "highpass", "freq": 250, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 7000, "q": 0.6}]) for i in range(3)]
PLK = S.track("プラックの駆け上がり", "lead", patch="kfbSquarePluck", volume=0.06, pan=0.3, reverb=0.3, fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
ORG = [S.track(f"オルガン（のばす{i + 1}）", "drawbarOrgan", volume=0.024, pan=0.3 - 0.6 * i, reverb=0.25, sustain=1.2) for i in range(2)]
SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.028, pan=0, duck=0.5)
KDR = S.track("電子のクラップ", "guitar", patch="kawaiiFx", volume=0.06, pan=-0.05, reverb=0.1, modulate=False)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.045, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 5:0.25 5:0.25 b7:0.5 5:0.5 3:0.5 5:0.5 b7:0.5 R:0.5", "1':0.5 1':0.5 b7:0.5 5:0.5 5:1 R:1",
      "R:0.5 6:0.25 6:0.25 1':0.5 6:0.5 4:0.5 6:0.5 1':0.5 R:0.5", "b7:0.5 b7:0.5 5:0.5 3:0.5 1:1 R:1",
      "R:0.5 1:0.25 1:0.25 3:0.5 5:0.5 5:0.5 b7:0.5 1':0.5 R:0.5", "2':0.5 1':0.5 b7:0.5 5:0.5 b7:1 R:1",
      "R:0.5 1':0.25 1':0.25 1':0.5 6:0.5 1':0.5 6:0.5 4:0.5 R:0.5", "5:0.5 7:0.5 2':0.5 7:0.5 5:1 R:1"]
A1 = ("はちじのちゃいむ/なりおわる/こうもんのまえ/いききらす/なんていおうか/かんがえる/せんせいのかお/うかんでる/"
      "いいわけならば/まかせてよ/あたまのなかで/せんしゅけん/いちばんてはね/ねこのせい/にばんてからは/おおげさに")
A2 = ("きょうしつのどあ/あけたらね/みんなのしせん/つきささる/くちをひらけば/とまらない/はなしはふくれ/そらをとぶ/"
      "せんせいまでも/ふきだした/きょうしつじゅうが/おおわらい/しかられるはず/のじかんが/はくしゅでおわる/すてーじに")
VB = ["R:1 6:0.5 1':0.5 1':1 6:1", "2':1 1':1 6:1 R:1", "R:1 6:0.5 1':0.5 1':1 6:1", "2':1 1':1 6:1 R:1",
      "R:0.5 4:0.5 6:0.5 1':0.5 1':1 6:1", "1':1 2':1 1':1 R:1", "2':0.5 2':0.5 2':0.5 2':0.5 1':1 2':1", "2':2 R:2"]
B1 = "ただのねぼうは/つまらないから/すこしだけならば/はなしをもろう"
B2 = "ひとつつくたび/ふくらんでいく/もうとまらないよ/だれかとめてよ"
HOOK = "5:0.5 5:0.5 1':0.5 1':0.5 b7:0.5 5:1 R:0.5"
VC = [HOOK, "R:0.5 2:0.5 4:0.5 4:0.5 b7:0.5 b7:0.5 4:0.5 R:0.5", "6:0.5 6:0.5 1':0.5 1':0.5 6:0.5 4:1 R:0.5", "R:0.5 3:0.5 5:0.5 5:0.5 1':0.5 1':0.5 5:0.5 R:0.5",
      HOOK, "R:0.5 2:0.5 4:0.5 4:0.5 b7:0.5 b7:0.5 4:0.5 R:0.5", "6:0.5 6:0.5 1':0.5 1':0.5 6:0.5 4:1 R:0.5", "R:0.5 5:0.5 7:0.5 7:0.5 2':0.5 2':0.5 2':0.5 R:0.5",
      "1':1.5 1':0.5 7:1 5:1", "7:1.5 7:0.5 5:1 R:1", "6:1.5 6:0.5 1':1 6:1", "5:1.5 3:0.5 5:1 R:1",
      "4:1 6:1 1':1 6:1", "6:1 1':1 2':1 R:1", "5:0.5 5:0.5 2':0.5 2':0.5 1':0.5 2':1 R:0.5", "R:4"]
C1 = ("ちがうんです/ねぼうじゃない/ちがうんです/きいてほしい/ちがうんです/ほんとうです/ちがうんです/わけがあるの/"
      "ねこがみちをね/ふさいでいたの/まわりみちした/ちがうんです")
C2 = ("ちがうんです/うそじゃないよ/ちがうんです/めをみてよね/ちがうんです/まだあるんだ/ちがうんです/つづきがある/"
      "くものふねでね/うみをこえたの/にじのしたまで/ちがうんです")
C3 = ("ちがうんです/ほんとうはね/ちがうんです/はなうたがね/ちがうんです/きこえてきて/ちがうんです/あしをとめた/"
      "あさのひかりが/きれいすぎてね/みとれていたの/ごめんなさい")
VBR = ["R:2 1:0.5 3:0.5 5:1", "b7:2 R:2", "R:2 5:0.5 b7:0.5 1':1", "1':1 b7:1 R:2", "R:2 1:0.5 3:0.5 5:1", "6:2 R:2", "R:1 5:0.5 6:0.5 1':1 2':1", "2':1 1':1 R:2"]
CB = "ほんとは/ねぼうです/でもあさ/きれいでした"
LY = Lyrics(S)


def put(name, lines, text, o=4):
    bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", VA + VA, A1)
put("Bメロ1", VB, B1)
put("サビ1", VC, C1)
put("Aメロ2", VA + VA, A2)
put("Bメロ2", VB, B2)
put("サビ2", VC, C2)
put("ほんとは", VBR, CB)
put("最後のサビ", VC, C3)

# ================= スラップベース =================
root = lambda b: S.chords[b].split("|")[0].split("/")[0]
# リフ（E の形。同じ音を続けて打たない）。A7 は +5、B7 は +7
RIFF_A = "E2:1 R:0.5 G2:0.25 G#2:0.25 B2:0.5 D3:0.5 R:0.5 E3:0.5"
RIFF_B = "E2:1 R:0.5 D3:0.5 B2:0.5 A2:0.25 G2:0.25 G#2:0.5 R:0.5"
RIFF_C = "E2:0.75 R:0.25 E3:0.5 D3:0.5 R:0.5 B2:0.5 G2:0.25 G#2:0.25 B2:0.5"          # 2番で使う別の形


def tr_line(line, semi):
    return " ".join(t if t.startswith("R") else f"{nm(midi(t.split(':')[0]) + semi)}:{t.split(':')[1]}" for t in line.split())


def riff(b, i, alt=False):
    semi = {"E": 0, "A": 5, "B": -5}[root(b)[0]]
    SLAP.bar(b, tr_line((RIFF_C if alt and i % 4 == 2 else (RIFF_A if i % 2 == 0 else RIFF_B)), semi))


def pop(b, style):
    """サビのスラップ: 和音を追って、オクターブ上をはじく"""
    ch = S.chords[b]; r = low(ch, "E1"); nx = S.chords[b + 1] if b + 1 < S.nb else ch; rn = low(nx, "E1")
    up = tones(root(b), nm(r + 1), nm(r + 12)); t5 = next((m for m in up if (m - r) in (6, 7, 8)), r + 7); t7 = next((m for m in up if (m - r) in (9, 10, 11)), r + 10)
    o = r + 12; ap = t5 if rn == r else (rn - 1 if rn > r else rn + 1); N = nm
    SLAP.bar(b, {"a": f"{N(r)}:1 R:0.5 {N(o)}:0.5 R:0.5 {N(t5)}:0.5 {N(o)}:0.5 {N(ap)}:0.5",
                 "b": f"{N(r)}:0.75 R:0.25 {N(t5)}:0.5 {N(o)}:0.5 R:0.5 {N(t7)}:0.5 {N(t5)}:0.5 {N(ap)}:0.5",
                 "long": f"{N(r)}:1.5 {N(t5)}:0.5 {N(o)}:1.5 {N(ap)}:0.5",
                 "hit": f"{N(r)}:0.5 R:0.5 {N(r + 12)}:1 R:2"}[style])


# ================= 和音・合いの手 =================
CH_A = "R:0.5 x:0.25 R:0.75 x:0.5 R:1 x:0.25 x:0.25 R:0.5"     # エレピの短い刻み（すき間を多く）
CH_B = "R:1 x:0.5 R:0.5 x:0.25 R:0.25 x:0.5 R:1"


def ep(b, pat, c=64, tr=None):
    v = sorted(voice(root(b), c, 3)); tr = tr or EP
    for j in range(3): tr[j].bar(b, " ".join(t.replace("x", nm(v[j])) for t in pat.split()))


def stab(b, pat, c=68):
    v = sorted(voice(root(b), c, 3))
    for j in range(3): STAB[j].bar(b, " ".join(t.replace("x", nm(v[j])) for t in pat.split()))


def run(b, n_notes, lo="B4", hi="B6", lead=3.0):
    """プラックの駆け上がり（和音の音を16分で）。n_notes が多いほど高くまで上がる"""
    tn = tones(root(b), lo, hi)[:n_notes]; rest = lead - 0.25 * (len(tn) - 4)
    PLK.bar(b, f"R:{rest:g} " + " ".join(f"{nm(m)}:0.25" for m in tn))


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "リフ":
        riff(b, i)
        if i >= 4: ep(b, CH_A if i % 2 == 0 else CH_B)
        if i == 7: run(b, 6)
    elif n == "Aメロ1":
        riff(b, i)
        if i >= 8: ep(b, CH_A if i % 2 == 0 else CH_B)
        if i >= 8 and i % 4 == 3: run(b, 4)
    elif n == "Aメロ2":
        riff(b, i, alt=True); ep(b, CH_B if i % 2 == 0 else CH_A)
        if i % 2 == 1: run(b, 4 + i // 4)                         # 言いわけが大きくなるたびに、駆け上がりが高くなる（4 → 7 音）
        if i >= 8 and i % 2 == 0: stab(b, "R:3.5 x:0.5")
    elif n in ("Bメロ1", "Bメロ2"):
        if i < 6:
            ep(b, "x:4", 62 + i, EPL); pop(b, "long")
            if n == "Bメロ2": ep(b, CH_A, 66)
        elif i == 6: ep(b, "x:0.5 x:0.5 x:0.5 x:0.5 x:1 x:1", 68); stab(b, "x:0.5 x:0.5 x:0.5 x:0.5 x:1 x:1"); pop(b, "a")
        else: ep(b, "x:2 R:2", 69); stab(b, "x:2 R:2"); pop(b, "hit")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        pop(b, "a" if i % 2 == 0 else "b")
        ep(b, CH_A if i % 2 == 0 else CH_B, 66)
        v = sorted(voice(root(b), 60, 3)); ORG[0].bar(b, f"{nm(v[0])}:4"); ORG[1].bar(b, f"{nm(v[2])}:4")
        # 「ちがうんです」の小節: 最後の半拍で電子の和音がひとつ。言いわけの小節: プラックが駆け上がる（サビごとに高く）
        if i < 8 and i % 2 == 0: stab(b, "R:3.5 x:0.5" if n == "サビ1" else "x:0.5 R:3 x:0.5")
        elif i < 8: run(b, {"サビ1": 4, "サビ2": 6, "最後のサビ": 8}[n], lead=3.0)
        elif i < 14:
            if n != "サビ1": stab(b, "x:1.5 x:1.5 x:1" if i % 2 == 0 else "R:1 x:1.5 x:1.5")
        elif i == 14: stab(b, "R:3.5 x:0.5")
        else: run(b, 8, lead=1.0) if n != "最後のサビ" else stab(b, "x:1 R:3")
    elif n == "間奏":
        riff(b, i); ep(b, CH_A if i % 2 == 0 else CH_B); stab(b, "R:1.5 x:0.5 R:2" if i % 2 == 0 else "R:3 x:0.5 x:0.5")
    elif n == "ほんとは":                                          # ベースとエレピだけ
        ep(b, "x:4", 64, EPL)
        r = low(S.chords[b], "E1"); SLAP.bar(b, f"{nm(r)}:2.5 R:0.5 {nm(r + 12)}:0.5 {nm(r + 7)}:0.5" if i < 6 else (f"{nm(r)}:1 {nm(r + 2)}:1 {nm(r + 4)}:1 {nm(r + 5)}:1" if i == 7 else f"{nm(r)}:4"))
    elif n == "おわり":
        if i < 3: riff(b, i); ep(b, CH_A if i % 2 == 0 else CH_B); stab(b, "R:3.5 x:0.5")
        else: SLAP.bar(b, "E2:1 R:3"); ep(b, "x:1 R:3", 68); stab(b, "x:1 R:3")
    if n in ("サビ2", "最後のサビ"): SUB.bar(b, f"{nm(low(S.chords[b], 'E1'))}:1 R:3")

# ================= ドラム（ファンク: 1拍目を強く、16分のハイハットを少しはねさせる）=================
HH = "x.xxx.xxx.xxx.xx"
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "ドラム": D.set(b, "X.....x.x.X.....", "....X.......X..." if i == 0 else "....X.......X.XX", HH)
    elif n in ("リフ", "間奏", "Aメロ2"):
        vgroove(D, b, "beat8", ghosts=0.3, seed=b, k="X.....x.x.X....." if i % 2 == 0 else "X..x....x.X...x.", s="....X.......X...", h=HH, vary=False)
        if i == 0 and n != "Aメロ2": crash(D, b)
        if last: put_fill(D, b, "snare16" if n != "間奏" else "small")
        KDR.bar(b, "R:1 B4:1 R:1 B4:1") if n == "Aメロ2" and i >= 8 else None
    elif n == "Aメロ1":
        if i < 8: D.set(b, "X.....x.x.X....." if i % 2 == 0 else "X..x....x.X.....", "....x.......x...", "x.x.x.x.x.x.x.x.")       # 前半は縁の音と8分
        else: vgroove(D, b, "beat8", ghosts=0.3, seed=b, k="X.....x.x.X....." if i % 2 == 0 else "X..x....x.X...x.", s="....X.......X...", h=HH, vary=False)
        if last: put_fill(D, b, "snare16")
    elif n in ("Bメロ1", "Bメロ2"):
        if i < 6: D.set(b, "X.........x....." if i % 2 == 0 else "X.......x.......", "........X.......", "x.x.x.x.x.x.x.x.")                 # 半分の速さでためる
        elif i == 6: D.set(b, "X...X...X...X...", "X.X.X.X.X.X.XXXX", "................")
        else: halt(D, b, 2); D.K[b] = "X...X..........."; D.S[b] = "X...X..........."
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        vgroove(D, b, "beat8", ghosts=0.3 if n != "最後のサビ" else 0.4, seed=b, k="X..x..x...X....." if i % 2 == 0 else "X.....x.x.X..x..", s="....X.......X..." if i % 4 != 3 else "....X..x....X...", h=HH, vary=False)
        if i % 8 == 0: crash(D, b, "C2", 4)
        if i == 7: put_fill(D, b, "small")
        if last and n != "最後のサビ": put_fill(D, b, "tomtrip")
        KDR.bar(b, "R:1 B4:1 R:1 B4:1")
    elif n == "ほんとは":
        if i >= 4: D.set(b, "X...............", "........x......." if i < 7 else "....X...X.X.XXXX", "x...x...x...x..." if i < 7 else "................")
    elif n == "おわり":
        if i < 3: vgroove(D, b, "beat8", ghosts=0.3, seed=b, k="X.....x.x.X.....", s="....X.......X...", h=HH, vary=False)
        else: D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 4)
        if i == 0: crash(D, b)

cym_swell(CYM, S.sc("サビ1")[0], 2, "C4"); cym_swell(CYM, S.sc("サビ2")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 4, "E4")

# 止め: Bメロ の8小節目は、頭の2拍のあと全員休み
for nme in ("Bメロ1", "Bメロ2"): SIL.add(S.sc(nme)[-1], 2, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の09（8時）。スラップベースのエレクトロ・ファンク（ギターなし）。E・108。遅刻の言いわけがどんどん大げさになる。"
          "サビは「ちがうんです」。スラップベースのリフ、FM のエレピ、電子の短い和音、言いわけが大きくなるたびに高くなるプラックの駆け上がり。最後は「ごめんなさい」。自作")
finish(S, LY, V, 0,
       level={"verse": -0.2}, special={"ほんとは": -0.5, "最後のサビ": 0.4})

# ================= 仕上げのあとに足すもの =================
from vt3x_lib import *
path = sys.argv[1]
set_parts(path, "ハイハット", swing16=0.18)
humanize(path, "FM のエレピ", mid=82, down=10, up=8, seed=3); humanize(path, "スラップ", mid=88, down=8, up=8, seed=5)
# v4 を測ると、Aメロ1（−15.9）が サビ1（−14.9）に近く、最後のサビ（−14.9）が サビ2（−14.4）より小さかった → Aメロを少し下げ、山を最後に
final_gain(path, {"Aメロ1": -0.8, "Aメロ2": -0.5, "サビ1": 0.3, "サビ2": 0.5, "最後のサビ": 1.8, "おわり": 0.8})
if VOCAL:
    backing(path, 0.9)   # 2026-11-13 人間「声以外のバック音量0.9ぐらいにしようか」
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 6, "pre": 14, "chorus": 20, "最後のサビ": 24, "bridge": 6}, scoop=0.3, slash=0.7, vib_min_beats=1.5, vib_start=0.5, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 8, None, K), ("最後のサビ", 8, None, K)], vol=0.36)
    voice_by_scene(path, S, {"verse": "cute"}, default="clear")
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.4
    save(path, js)
