# KFB 01「あたりつき」Lucky Extra（仮）— Kawaii future bass。4分の4・150・ニ長調。約4分10秒。
#
# v3（2026-11-23）: v2 は 歌入り 7.74・歌なし 7.44。前奏 −31dB（サビより 17dB 下）で小さすぎ、Bメロも Aメロより 5dB 下で下げすぎ、歌い出しが Aメロより大きかった。
#   → 和音が主役の所（前奏・歌い出し・Bメロ・静かな場面・おわり）に、大きめのこもらせた和音を別に用意。歌い出しのベースをやめた。Aメロを少し下げた。
# v2: 音色の重なりを減らした（ベル・パッドを入れかえ、上がっていく効果音とふくらむ和音を足した）。
# v1（2026-11-23）: 人間「kawaiiFutureベースで作ってみて」。旭さんの見本3曲を測った学び（docs/sound/kfb-study-user-refs.md）を使う。
#
# 物語: 夕方の自販機で、もう1本が当たる。2本は飲めないので、あげたい人の顔がうかぶ。ぬるくなる前にと走るが、見つけたときにはもうぬるい。それでも渡して、ならんで飲む。
# 見本から使う型（全部は当てはめない）:
#   テンポ150／前奏は和音だけ・せまく／歌い出しはドラムなし／Aメロの和音はこもらせて歌より下／Bメロはベースを抜く／歌のサビ → 歌なしのドロップ（和音が前に出る）／
#   キックでへこませる量は浅く／ベースはサイン波に近いサブを1小節3音・休み4割／和音は m7・sus・maj7、小節のまん中で変える小節を3〜5割／
#   歌は8分が中心、のばす音は少なくウラから入る、句の最後は短く切る／間は無音でなくパートを抜いて作る（全員がだまるのはドロップ直前の1拍だけ）
# 物語の出来事 → その時の音:
#   前奏（自販機の明かり）          → こもらせた和音だけ
#   歌い出し（小銭を数える）        → 歌と和音。ドラムなし
#   Aメロ（数字がそろい、2本落ちる）→ こもらせた和音・サブベース・少ないキック。8小節めに「ピロピロ」（数字がそろう）
#   Bメロ（だれにあげよう）         → ベースを抜く。手びょうし。最後に1拍の無音
#   サビ（ぬるくなる前に走る）      → 明るい和音
#   ドロップ（ルーレット）          → 歌なし。和音を前に、ルーレットの音が主役
#   静かな場面（見つけた。もうぬるい）→ 歌と和音だけ
#   立ち上げ（名前を呼ぶ）          → ドラムが少しずつ入る
#   最後のサビ・ドロップ            → 全員
# この曲だけの物: 自販機のルーレット（短い矩形波で和音を16分でかけ上がり、最後の音が残る）。
# 歌詞: 曲名の言葉（あたり）は歌わない。声: キュート 1 種類。オーケストラの楽器・アコーディオン・バンジョーは使わない。ゲームの話は出さない。
from vocalo_lib import *

S = Song("27", "ataritsuki", "あたりつき（仮）", "Lucky Extra", 150, 4, "D", "major", "カワイイ・フューチャーベース（ボカロ）")
S.kit = "electro"; S.flags = S.flags + " --space room --space-wet 0.08"
K1 = Key("D", "major")

ACH = ["Gmaj7", "A", "Bm7", "Bm7", "Gmaj7", "F#m7", "Em7", "A7sus4"]; AH = {1: "F#m7", 3: "A", 5: "Bm7", 7: "A"}                 # AH: 小節のまん中（3拍め）から変わる和音
BCH = ["Em7", "F#m7", "Gmaj7", "A7sus4", "Em7", "F#m7", "Gmaj7", "A"]; BH = {}
CCH = ["G", "A", "Bm7", "D", "G", "A", "Bm7", "Bm7", "G", "A", "Bm7", "D", "Em7", "F#m7", "Gmaj7", "A7sus4"]; CH = {1: "F#m7", 3: "A", 5: "F#m7", 7: "A", 9: "F#m7", 11: "A", 15: "A"}
HALF = {}


def scene(name, n, kind, chs, half=None, rep=1):
    b0 = sum(x[1] for x in getattr(S, "_sc", [])); S._sc = getattr(S, "_sc", []) + [(name, n)]
    S.scene(name, n, kind, chs)
    for k in range(rep):
        for i, c in (half or {}).items():
            if i + k * (n // rep) < n: HALF[b0 + i + k * (n // rep)] = c


scene("前奏", 4, "intro", CCH[:4], {1: "F#m7", 3: "A"})
scene("歌い出し", 4, "intro", ["Gmaj7", "A", "Bm7", "A7sus4"], {1: "F#m7"})
scene("1番A", 16, "verse", ACH * 2, AH, 2)
scene("1番B", 8, "pre", BCH, BH)
scene("サビ1", 16, "chorus", CCH, CH)
scene("ドロップ1", 8, "break", CCH[:8], {1: "F#m7", 3: "A", 5: "F#m7", 7: "A"})
scene("2番A", 16, "verse", ACH * 2, AH, 2)
scene("2番B", 8, "pre", BCH, BH)
scene("サビ2", 16, "chorus", CCH, CH)
scene("ドロップ2", 8, "break", CCH[:8], {1: "F#m7", 3: "A", 5: "F#m7", 7: "A"})
scene("静かな場面", 8, "bridge", ["Gmaj7", "A", "F#m7", "Bm7", "Gmaj7", "A", "Bm7", "Bm7"])
scene("立ち上げ", 8, "pre", BCH, BH)
scene("最後のサビ", 16, "chorus", CCH, CH)
scene("最後のドロップ", 16, "break", CCH, CH)
scene("おわり", 6, "outro", ["Gmaj7", "A", "Bm7", "A7sus4", "Gmaj7", "D"], {1: "F#m7"})
S.keep_old_synth = True; S.no_depth = True; S.keepers = {}; S.open_hat_vol = 0.3

V = Voice(S, vol=0.17, delay=0.2, bright=0.0, patch="kfbSineLead", low=False)
SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.085, pan=0, duck=0.12)                                             # サイン波に近い低い音。へこませる量は浅く
MUF = [S.track(f"こもらせた和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.03, pan=(0, 0.12, -0.12, 0.2, -0.2)[i], reverb=0.2, duck=0.12,
               fx=[{"type": "filter", "kind": "lowpass", "freq": 1300, "q": 0.7}]) for i in range(5)]                              # Aメロ・前奏: フィルターを閉じる・左右はせまく
# v5: 和音が主役の所に別の音を足す案（v3 こもらせたスーパーソウを大きく → 点 5.5、v4 ガラスのエレピ → 点 5.9〜6.6）はやめた。v2 の「こもらせた和音＋やわらかいパッド」（点 7.7〜7.9）にもどし、大きさはパッドで足す。
BRI = [S.track(f"明るい和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.032, pan=(0, 0.25, -0.5, 0.5, -0.25)[i], reverb=0.2, duck=0.15, fx=rack_supersaw()) for i in range(5)]   # サビ: 歌より下
DRP = [S.track(f"ドロップの和音{i + 1}", "lead", patch="kfbSupersawWide", volume=0.055, pan=(0, 0.25, -0.5, 0.5, -0.25)[i], reverb=0.2, duck=0.15, fx=rack_supersaw()) for i in range(5)]  # ドロップ: 前に出る
ROU = S.track("ルーレット（矩形波のプラック）", "lead", patch="kfbSquarePluck", volume=0.085, pan=0.1, reverb=0.25, fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.3, "feedback": 0.35}])
BELL = S.track("ベル", "lead", patch="kfbBrightBells", volume=0.06, pan=-0.3, reverb=0.35)
EP = [S.track(f"やわらかいパッド{i + 1}", "pad", patch="surgePadPad2Mw", volume=0.06, pan=(-0.2, 0.2, 0)[i], reverb=0.3) for i in range(3)]
FX = S.track("効果音（上がっていく音）", "pad", patch="fxRiser", volume=0.045, pan=0, reverb=0.3)
SWELL = [S.track(f"ふくらむスーパーソウ{i + 1}", "lead", patch="kfbSupersawSwell", volume=0.03, pan=-0.4 + 0.4 * i, reverb=0.3) for i in range(3)]   # Bメロ: 「ポワン」とふくらむ和音
CLP = S.track("手びょうし", "guitar", patch="kawaiiFx", volume=0.055, pan=-0.05, reverb=0.1, modulate=False)
D = S.drumkit(); LY = Lyrics(S); N = lambda m: nm(m)

# ================= 歌（度数:長さ。oct 4 で 1 = D4。低い 5, = A3、高い 3' = F#5）=================
VP = ["R:1 5,:0.5 1:0.5 3:0.5 2:0.5 1:0.5 2:0.5", "3:1.5 R:2.5", "R:1 3:0.5 5:0.5 6:0.5 5:0.5 3:0.5 5:0.5", "2:1.5 R:2.5"]
VA = ["R:0.5 5,:0.5 1:0.5 2:0.5 3:0.5 3:0.5 2:0.5 1:0.5", "3:0.5 5:1 3:0.5 R:2", "R:0.5 3:0.5 5:0.5 6:0.5 5:0.5 3:0.5 2:0.5 3:0.5", "2:0.5 1:1 R:2.5",
      "6,:0.5 1:0.5 2:0.5 3:0.5 5:1 6:0.5 5:0.5", "3:0.5 2:0.5 3:1 R:2", "R:1 5:0.5 6:0.5 1':0.5 6:0.5 5:0.5 3:0.5", "5:0.75 3:0.25 2:1 R:2"]
VA2 = ["5,:0.5 1:0.5 3:0.5 5:0.5 R:0.5 5:0.5 6:0.5 5:0.5", "3:1 2:0.5 1:0.5 R:2", "R:0.5 6:0.5 6:0.5 5:0.5 3:0.5 5:0.5 6:0.5 1':0.5", "6:0.5 5:1 R:2.5",
       "1':0.5 1':0.5 6:0.5 5:0.5 6:1 5:0.5 3:0.5", "2:0.5 3:0.5 5:1 R:2", "R:1 3:0.5 5:0.5 6:0.5 1':0.5 2':0.5 1':0.5", "6:0.75 5:0.25 5:1 R:2"]
VB = ["3:0.5 3:0.5 5:0.5 3:0.5 R:0.5 3:0.5 5:0.5 6:0.5", "5:1.5 R:2.5", "5:0.5 5:0.5 6:0.5 5:0.5 R:0.5 5:0.5 6:0.5 1':0.5", "6:1.5 R:2.5",
      "6:0.5 6:0.5 1':0.5 6:0.5 R:0.5 6:0.5 1':0.5 2':0.5", "1':1.5 R:2.5", "2':0.5 2':0.5 1':0.5 2':0.5 3':1 R:1", "R:4"]
VC = ["R:0.5 1':0.5 2':0.5 3':0.5 2':0.5 1':0.5 6:0.5 1':0.5", "R:0.5 2':1.5 1':0.5 6:0.5 R:1", "R:0.5 6:0.5 1':0.5 2':0.5 1':0.5 6:0.5 5:0.5 6:0.5", "R:0.5 5:1.5 3:0.5 5:0.5 R:1",
      "5:0.5 6:0.5 1':0.5 2':0.5 3':1 2':0.5 1':0.5", "R:0.5 2':1 1':0.5 6:1 R:1", "R:0.5 5:0.5 6:0.5 1':0.5 2':0.5 1':0.5 6:0.5 5:0.5", "6:0.5 1':1.5 R:2",
      "R:0.5 1':0.5 2':0.5 3':0.5 2':0.5 1':0.5 6:0.5 1':0.5", "R:0.5 2':1.5 1':0.5 6:0.5 R:1", "R:0.5 6:0.5 1':0.5 2':0.5 3':0.5 2':0.5 1':0.5 2':0.5", "R:0.5 3':1.5 2':0.5 1':0.5 R:1",
      "5:0.5 6:0.5 1':0.5 2':0.5 3':1 2':0.5 3':0.5", "R:0.5 2':1 1':0.5 2':1 R:1", "R:0.5 1':0.5 1':0.5 6:0.5 5:0.5 6:0.5 1':0.5 2':0.5", "1':2 R:2"]
VQ = ["3:1 2:0.5 1:0.5 R:0.5 1:0.5 2:0.5 3:0.5", "5:1.5 3:0.5 R:2", "5:1 3:0.5 2:0.5 R:0.5 2:0.5 3:0.5 5:0.5", "6:1.5 5:0.5 R:2",
      "3:1 2:0.5 1:0.5 R:0.5 1:0.5 2:0.5 3:0.5", "5:1.5 3:0.5 R:2", "6:1 5:0.5 3:0.5 R:0.5 5:0.5 6:0.5 1':0.5", "2':2 R:2"]
CA = "ぬるくなるそのまえに/きみのとこまでいくよ/"; CB = "ぐうぜんがくれたもの/はんぶんこしたいだけ/むねであわがはじける/とまらないこどう"


def put(name, lines, text, bars=None):
    bars = bars or S.sc(name); mel = [x if x == "R:4" else K1.mel(x, oct=4) for x in lines]
    for k, sg in enumerate(text.split("/")):                              # 2小節ごとに、音の数と文字の数が合っているか確かめる
        nn = sum(1 for x in " ".join(lines[k * 2:k * 2 + 2]).split() if not x.startswith("R"))
        assert nn == mora(sg), (name, k, sg, nn, mora(sg))
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("歌い出し", VP, "じはんきのまえ/こぜにがたりた")
put("1番A", VA + VA2, "ぼたんをおすとひかる/すうじがまわりだす/おなじすうじがならぶ/あかいらんぷがつく/がこんとにかいなるよ/つめたいのがにほん/ひとりじゃのみきれない/りょうてがふさがるよ")
put("1番B", VB, "だれにあげようか/かんがえるまえに/うかぶかおがある/かけだした")
put("サビ1", VC, CA + "しずくがゆびをつたう/いいわけはまだない/" + CB)
put("2番A", VA2 + VA, "いつものばしょにいない/べんちはからのまま/かんがあせをかいてる/てのひらもつめたい/さかみちをのぼりつつ/せりふをくりかえす/たまたまふたつでたの/それだけのことだよ")
put("2番B", VB, "うそじゃないけれど/ほんとでもないな/あげたいのはきみ/それだけだ")
put("サビ2", VC, CA + "かどのたびにさがすよ/ゆうやけがおいこす/" + CB)
put("静かな場面", VQ, "みつけたよせなか/こえがでてこない/かんはもうぬるい/それでもいいや")
put("立ち上げ", VB, "いきをすいこんで/あしをまえにだす/なまえをよんだら/ふりむいた")
put("最後のサビ", VC, "ぬるいけどこれどうぞ/きみがわらいうけとる/ぷしゅとふたつなるおと/いいわけはいらない/ぐうぜんがくれたもの/はんぶんこじゃなくても/むねであわがはじける/となりにすわるよ")
put("おわり", ["5:0.5 6:0.5 1':0.5 1':1.5 R:1", "R:4"], "かんぱい", bars=S.sc("おわり")[4:6])


# ================= 伴奏 =================
def ch2(b): return (S.chords[b], HALF.get(b))                             # (前半の和音, 後半の和音 か None)


def chords(tr, b, pat="hold", center=64):
    """5声の和音。hold＝のばす（まん中で変わる小節は2拍ずつ）、stab＝リズムで切る（16マスの x）"""
    c1, c2 = ch2(b); v1 = sorted(voice(c1, center, 5)); v2 = sorted(voice(c2, center, 5)) if c2 else v1
    for j in range(5):
        if pat == "hold": tr[j].bar(b, f"{N(v1[j])}:2 {N(v2[j])}:2" if c2 else f"{N(v1[j])}:4")
        else:
            out = []; i = 0
            while i < 16:
                L = 1
                while i + L < 16 and pat[i + L] == "-": L += 1
                out.append(f"R:{L * 0.25:g}" if pat[i] == "." else f"{N((v1 if i < 8 else v2)[j])}:{L * 0.25:g}"); i += L
            tr[j].bar(b, " ".join(out))


def sub(b, pat):
    """サブベースを8分のマスで。x＝弾く（前半は前半の和音の根音、後半は後半の和音の根音）、5＝5度、-＝のばす、.＝休み"""
    c1, c2 = ch2(b); r1 = low(c1, "D1"); r2 = low(c2, "D1") if c2 else r1; out = []; i = 0
    while i < 8:
        L = 1
        while i + L < 8 and pat[i + L] == "-": L += 1
        r = r1 if i < 4 else r2
        out.append(f"R:{L * 0.5:g}" if pat[i] == "." else f"{N(r + (7 if pat[i] == '5' else 0))}:{L * 0.5:g}"); i += L
    SUB.bar(b, " ".join(out))


def roulette(b, kind=0):
    """ルーレット: 和音の音を16分でかけ上がる。kind 0＝1拍め、1＝3拍め、2＝1小節ぜんぶ回って最後の音が残る"""
    c1, c2 = ch2(b); t = sorted(voice(c1, 76, 4)); u = sorted(voice(c2 or c1, 76, 4))
    if kind == 0: ROU.bar(b, " ".join(f"{N(x)}:0.25" for x in t) + f" {N(t[0] + 12)}:1 R:2")
    elif kind == 1: ROU.bar(b, "R:2 " + " ".join(f"{N(x)}:0.25" for x in u) + f" {N(u[0] + 12)}:1")
    else: ROU.bar(b, " ".join(f"{N(x)}:0.25" for x in t + [t[0] + 12, t[3], t[2], t[1]] + u) + f" {N(u[0] + 12)}:1")


def lead(b, i):
    """ドロップの主役: ルーレットの音で、短い旋律と、かけ上がりを1小節おきに"""
    if i % 2 == 0: ROU.bar(b, K1.mel(("3':0.5 R:0.25 3':0.25 2':0.5 1':0.5 R:0.5 6:0.5 1':0.5 2':0.5", "5':0.5 R:0.25 5':0.25 3':0.5 2':0.5 R:0.5 1':0.5 2':0.5 3':0.5")[(i // 2) % 2], oct=4))
    else: roulette(b, 2 if i % 4 == 3 else 1)


def bell(b, k=0): BELL.bar(b, K1.mel(("R:3 5':0.5 3':0.5", "R:1.5 1'':0.5 R:2", "3':0.5 5':0.5 R:3")[k], oct=4))
def ep(b):
    v = sorted(voice(S.chords[b], 62, 3))
    for j in range(3): EP[j].bar(b, f"{N(v[j])}:4")


def clap(b, pat="R:2 B4:1 R:1"): CLP.bar(b, pat)
# ドラム: キックは少なめ（1小節 2〜3 打）。スネア（手びょうし）は3拍め。刻みは1小節 7 打くらい
VER = [("X.........X.....", "........X.......", "x.x.x.x...x.x.x."), ("X......X..X.....", "........X.....x.", "x.x.x...x.x.x.x.")]
CHO = [("X.....X...X.....", "........X.......", "x.x.x.x.x.x...x."), ("X.....X....X..X.", "........X.....X.", "x.x.x.x...x.x.x.")]
DRO = [("X..X......X..X..", "........X.......", "x.x.x.x.x.x.x.x."), ("X.....X..X....X.", "........X...X...", "x.xxx.x.x.x...x.")]

for b in range(S.nb):
    n, i, L, kind = S.scene_of(b); odd = i % 2 == 1; last = i == L - 1
    if n == "前奏":                                                      # こもらせた和音だけ
        chords(MUF, b); ep(b); BELL.bar(b, K1.mel(("3':1 R:0.5 5:0.5 1':1 R:1", "2':1 R:0.5 5:0.5 6:1 R:1", "3':1 R:0.5 5:0.5 1':0.5 2':0.5 3':1", "5':2 R:2")[i], oct=4))   # v6: 前奏にベルの短い旋律（小さすぎたので）
    elif n == "歌い出し":                                                # 歌と和音。ドラムなし
        chords(MUF, b); ep(b)
        if last: D.set(b, "................", "..........x.x.xx", "................"); roulette(b, 1)
    elif n in ("1番A", "2番A"):                                          # 和音はこもらせて、歌より下。ベースは1小節3音
        g = VER[i % 2]; D.set(b, g[0], g[1] if not last else "........X...x.xx", g[2]); chords(MUF, b)
        sub(b, ("x------x", "x--x----", "x-----xx", "x----..x")[(i + (2 if n == "2番A" else 0)) % 4])
        if i >= 8: ep(b)
        if i == 7: roulette(b, 2)                                         # 数字がそろう
        if n == "2番A" and i % 4 == 3: bell(b, (i // 4) % 3)
        if i == 9 and n == "1番A": D.set(b, "X.........X.....", "........X.......", "x.x.x.x...x.x.x."); crash(D, b, "C2", 2)   # 「がこん」
    elif n in ("1番B", "2番B", "立ち上げ"):                              # ベースを抜く。1段ずつ上がる。最後の1拍は無音
        if last:
            FX.bar(b, "C5:3 R:1"); chords(MUF, b, "x-----------....", 64 + 5); D.set(b, "................", "x...x...x.xx....", "................"); continue
        chords(MUF, b, "hold", 64 + i // 2); ep(b)
        if i >= 4:
            v_ = sorted(voice(S.chords[b], 69, 3))
            for j in range(3): SWELL[j].bar(b, f"{N(v_[j])}:4")
        if i == 6: FX.bar(b, "C5:4")
        if n == "立ち上げ":
            D.set(b, "X..............." if i < 4 else "X.......X.......", "................" if i < 6 else "x...x...x.x.x.x.", "................" if i < 2 else "x...x...x...x...")
            if i >= 4: clap(b, "R:1 B4:1 R:1 B4:1")
        else:
            D.set(b, "X..............." if i < 4 else "X.........X.....", "................" if i < 6 else "....x.......x.x.", "x...x...x...x..." if i < 4 else "x.x.x.x.x.x.x.x."); clap(b, "R:2 B4:1 R:1" if i < 4 else "R:1 B4:1 R:1 B4:1")
        if i == 6: roulette(b, 1)
    elif n in ("サビ1", "サビ2", "最後のサビ"):                          # 明るい和音。歌が主役
        g = CHO[i % 2]; D.set(b, g[0], g[1] if i % 8 != 7 else "........X...X.XX", g[2]); clap(b)
        if i % 8 == 0: crash(D, b, "C2", 4)
        chords(BRI, b, "hold" if i % 4 != 3 else "x-----x---x-----"); sub(b, ("x------x", "x--x---5", "x-----x-", "x--x--xx")[i % 4])
        if i % 4 == 3: roulette(b, 1)
        if n != "サビ1" and i % 4 == 1: bell(b, (i // 4) % 3)
    elif n in ("ドロップ1", "ドロップ2", "最後のドロップ"):              # 歌なし。和音が前に出て、ルーレットが主役
        g = DRO[i % 2]; D.set(b, g[0], g[1] if i % 8 != 7 else "........X.x.XXXX", g[2]); clap(b)
        if i % 8 == 0: crash(D, b, "C2", 4)
        chords(DRP, b, ("x--x--x---x--x--", "x-----x--x--x---", "x--x--x-----x-x-", "x-----x---x-----")[i % 4]); sub(b, ("x--x--x-", "x-----xx", "x--x---5", "x----.x-")[i % 4]); lead(b, i)
        if n == "最後のドロップ" and i >= 8 and odd: bell(b, i % 3)
    elif n == "静かな場面":                                              # 歌と和音だけ
        chords(MUF, b); ep(b)
        if i == 7: roulette(b, 1)
    elif n == "おわり":                                                  # 前奏と同じ形にもどる。ひとこと
        chords(MUF, b); ep(b)
        if i == 0: crash(D, b, "C2", 4)
        if i == 3: roulette(b, 2)
        if i == 5: bell(b, 2)

S.fade_out = 0
S.desc = ("仮: 重音テトのカワイイ・フューチャーベース（150・ニ長調）。自販機でもう1本が当たり、あげたい人のところへ走る話。"
          "こもらせた和音だけの前奏 → ドラムなしの歌い出し → Aメロ → ベースを抜いたBメロ → 歌のサビ → 歌なしのドロップ（ルーレットの音が主役）→ 2番 → 静かな場面 → 立ち上げ → 最後のサビ → 最後のドロップ → ひとこと。自作")
finish(S, LY, V, 0, flat=True)

from vt3x_lib import *
path = sys.argv[1]
humanize(path, "ルーレット（矩形波のプラック）", mid=92, down=10, up=10, seed=27)
if VOCAL:
    backing(path, 0.9)
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"intro": 8, "verse": 8, "pre": 12, "chorus": 15, "bridge": 6, "outro": 6}, scoop=0.06, slash=0.25, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.0)
    harmony(path, S, [("最後のサビ", 0, None, K1)], vol=0.2)
    voice_by_scene(path, S, {}, default="cute", tweak={"cute": {"formant": 1.16, "consonant": 2.2, "glide": 0.7, "legato": 0.0}})   # 1 曲 1 種類の声。一音一音はっきり
    sing_ends(path, S, human=0.5)
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.0
    save(path, js)
js = load(path); drum_center(js)
# 強弱: Bメロは Aメロより少し下げる（ベースを抜くぶんに足して）。静かな場面・前奏・おわりは、急に小さくなりすぎないようにする
for p_ in js["parts"]:
    g = list(p_.get("barGain", [1] * S.nb)) + [1] * S.nb
    for name, k in (("1番A", 0.82), ("2番A", 0.82), ("前奏", 1.35), ("おわり", 1.2)):
        for b in S.sc(name): g[b] = round(g[b] * k, 4)
    p_["barGain"] = g[:S.nb]
save(path, js)
