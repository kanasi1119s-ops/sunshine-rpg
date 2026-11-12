# vt3 03「夜勤明けのカフェオレ」Café au Lait After the Night Shift（仮）— 8分の6拍子のフューチャー・ソウル・バラード。8分音符＝174（付点4分＝58）。F長調。
# 第3弾（0時〜24時の街）の 2時。表は docs/sound/vt3-plan.md。
#
# v4（2026-11-12）: ゼロから作り直し。人間「全ての曲を1みたいにこだわって作って」「似た曲を作らない」「次の曲作る時、1回曲調が以前のものと似てないか確認してから」。
#   前の版（ネオソウル・4拍子・84・ローズとギター）は、旋律のリズムが 02 と 88% 同じ・ベースは共通の部品だった。曲そのものを決め直す。
#
# 作る前の確かめ（tools/vt3/similar_check.py --plan）: テンポ 186→174・和音・音色を今までの全曲とくらべ、いちばん近い曲で近さ 26%（目安 50% 未満）。
#   01＝4つ打ちのフューチャーファンク（118）、02＝2ステップのエレクトロポップ（128）。03 は拍子から変える（8分の6＝ゆれる3つ割り）。
#
# 調べた作り方（2026-11-12）:
#   ・6/8 のソウルのベース（No Treble）: 小節の頭に根音、根音・3度・5度で形を作り、最後の3つ（4・5・6拍）で次の和音へ近づく。
#   ・フューチャーベースのドロップ（Loopcloud）: のこぎり波の和音はすき間をあけたリズムで鳴らし、ドラムはそのリズムに合わせる。和音とベースはキックとスネアで引っこめる。
#     ドロップの前はドラムを抜く。フィルは2小節ごとの終わり。声のチョップは和音が鳴っていないすき間に置く。
#   ・6/8 のバラードのドラム（ふつうの決まり）: キックは1拍目、スネアは4拍目、刻みは8分6つ（1と4を強く）。
#
# 物語: 病院の夜勤。午前2時、ナースコールが鳴りやんだ休けい室。自販機の紙コップのカフェオレが「コトン」と落ちる。
#   1時のラジオで聞いた鼻歌が、まだ頭の中で回っている。だれかの痛みに手を当ててきた手のひらに、カフェオレのあたたかさが残る。
# v5（2026-11-12）: 人間「1 残らない 2 気持ちよさが欲しい 3 少しうるさい 4 外して 5 ある 6 やや単調。ベースラインを少し丸くして。中に収める様な感じ」→ 下の v5 の所を直した。
# アルバムの考え「幸せで美しい物語に書き換えて行く」（言葉では言わず、景色で）: 紙コップの湯気がのぼって星になり、長い廊下が川に変わり、足音が歌になる。
#
# 曲を決める表:
#   形: 紙コップが落ちる → ひとりの休けい室（ピアノの分散和音だけ・ささやき）→ 手のひらを見る（弦がのぼる・止まる）→ あたたかさが広がる（半分の速さのドロップ）
#       → 鼻歌がよみがえる（間奏。合いことばの節が筒の鉄琴に1回だけ）→ 口ずさんでみる（ドラムが入ったまま）→ 広がる → ナースコールが鳴りやむ（ほぼ無音）
#       → ピアノとチェロの二重奏 → いちばん広がる → 廊下へもどる（ピアノだけ）
#   強さ: 紙コップ 弱／Aメロ1 とても弱い→弱／Bメロ1 中→止め／サビ1 中強（後半から厚く）／間奏 弱／Aメロ2 中弱／Bメロ2 中／サビ2 強／ブリッジ とても弱い→のぼる
#        ／間奏2 中／最後のサビ いちばん強い／アウトロ 消える
#   旋律: Aメロ＝「長い・短い」のゆれる形で、低い所を語る。Bメロ＝長い音から始めて上がる。サビ＝「あったかいね」を6度跳んでのばす（2回、2回目は高く）。最後は高い主音でのばして終わる
#   音の世界: フェルトのように丸めたピアノ（分散和音）、グラスハープ（のびる光）、筒の鉄琴（星）、オルゴール（サビ2 から）、チェロ（対旋律）、
#            のこぎり波の和音（サビだけ・キックで引っこむ・すき間のあるリズム）、サブベース、指弾きのベース。ギターは入れない
#   この曲だけ: ①8分の6拍子 ②紙コップの「コトン」で始まる ③サビで初めてドラムが半分の速さで入る ④ピアノとチェロの二重奏の間奏
from vt25_lib import *

S = Song("03", "cafeaulait", "夜勤明けのカフェオレ（仮）", "Café au Lait After the Night Shift", 174, 6, "F", "major", "8分の6拍子のフューチャー・ソウル・バラード（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --piano salamander --space room --space-wet 0.18"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
K = Key("F", "major")          # oct 4 で 1 = F4

INTRO = ["Fmaj9", "Dm9", "Bbmaj9", "C7sus4"]
A_CH = ["Fmaj9", "C/E", "Dm9", "Bbmaj7", "Gm9", "Am7", "Bbmaj9", "C7sus4"]
B_CH = ["Bbmaj7", "C/Bb", "Am7", "D7"]
C_CH = ["Gm9", "C9", "Fmaj9", "Dm9", "Gm9", "C7sus4", "Fmaj9", "F7", "Bbmaj9", "C9", "Am7", "Dm9", "Gm9", "C7sus4", "Fmaj9", "Fmaj9"]

S.scene("紙コップ", 4, "intro", INTRO)
S.scene("Aメロ1", 16, "verse", A_CH + A_CH)
S.scene("Bメロ1", 4, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 4, "break", INTRO)
S.scene("Aメロ2", 16, "verse", A_CH + A_CH)
S.scene("Bメロ2", 4, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("ブリッジ", 8, "bridge", ["Bbmaj7", "Am7", "Gm9", "Fmaj7", "Bbmaj7", "Am7", "Gm9", "C7sus4"])
S.scene("間奏2", 8, "solo", ["Bbmaj9", "C9", "Am7", "Dm9", "Gm9", "C7sus4", "Fmaj9", "C7sus4"])
S.scene("最後のサビ", 16, "chorus", C_CH)
S.scene("アウトロ", 6, "outro", ["Fmaj9", "Bbmaj9", "Fmaj9", "Bbmaj9", "Fmaj9", "Fmaj9"])

FELT = [{"type": "eq", "low": -2, "mid": -1, "midHz": 500, "high": -2}, {"type": "filter", "kind": "lowpass", "freq": 5200, "q": 0.6}]   # フェルトをはさんだような丸いピアノ
V = Voice(S, vol=0.2, delay=1.5, bright=-0.1, patch="kfbSineLead", low=False)
PR = S.track("ピアノ（右手の分散和音）", "piano", volume=0.115, pan=-0.15, reverb=0.3, sustain=1.6, fx=FELT)
PL = S.track("ピアノ（左手）", "piano", volume=0.12, pan=-0.15, reverb=0.3, sustain=1.6, fx=FELT)
PC = [S.track(f"ピアノ（和音{i + 1}）", "piano", volume=0.085, pan=-0.15, reverb=0.3, sustain=1.4, fx=FELT) for i in range(3)]
PM = S.track("ピアノ（間奏の旋律）", "piano", volume=0.16, pan=-0.05, reverb=0.32, sustain=1.5)
WG = [S.track(f"グラスハープ{i + 1}", "lead", patch="wineGlass", volume=0.05, pan=-0.35 + 0.7 * i, reverb=0.5) for i in range(2)]
TG = S.track("筒の鉄琴（星）", "lead", patch="tubeGlock", volume=0.06, pan=0.35, reverb=0.5)
MB = S.track("オルゴール", "lead", patch="kfbMusicBox", volume=0.04, pan=0.4, reverb=0.4,
             fx=[{"type": "pingpong", "beats": 1.5, "mix": 0.14, "feedback": 0.25}])
CELLO = S.track("チェロ", "strings", patch="cello", volume=0.075, pan=0.2, reverb=0.35, sustain=1.2)
STRL = S.track("弦の線", "strings", patch="stringEnsemble", volume=0.05, pan=-0.3, reverb=0.42, sustain=1.2)
STRH = S.track("弦の高い線（最後のサビ）", "strings", patch="stringEnsemble", volume=0.035, pan=0.3, reverb=0.45, sustain=1.3)
# v5（人間「3 少しうるさい」）: のこぎり波は音量を半分近くに・高い所を丸く（8.5k→4.5k）・すき間のあるリズムをやめて、のばしてキックでゆっくり引っこむ形に。サビ2 の後半と最後のサビだけ
SAW = [S.track(f"のこぎり波の和音{i + 1}", "lead", patch="kfbSupersaw", volume=0.022, pan=-0.5 + 0.5 * i, reverb=0.25, duck=0.6,
               fx=[{"type": "filter", "kind": "highpass", "freq": 220, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 4500, "q": 0.6}]) for i in range(3)]
STP = [S.track(f"弦の低い和音{i + 1}", "strings", patch="stringEnsemble", volume=0.03, pan=-0.4 + 0.8 * i, reverb=0.4, sustain=1.5) for i in range(2)]
# v5（人間「ベースラインを少し丸くして。中に収める様な感じ」）: 指弾きのベースの、弦をはじく高い成分（1k・2.2k の持ち上げ）をやめて 900Hz から上を丸める。
#   動きも、オクターブ上へ跳ばず、根音と5度のあいだに収める
BASS = S.track("ベース（指弾き）", "bass", sustain=1.25, **dict(finger_bass_spec(vol=0.2), fx=[{"type": "eq", "low": 1, "mid": -1, "midHz": 1000, "high": -4}, {"type": "filter", "kind": "lowpass", "freq": 900, "q": 0.6}]))
SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.032, pan=0, duck=0.5)
KDR = S.track("電子のクラップ", "guitar", patch="kawaiiFx", volume=0.06, pan=-0.05, reverb=0.12, modulate=False)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.05, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌（1拍＝8分音符。1小節＝6拍。句は2小節）=================
# Aメロ: 「長い・短い」のゆれる形。低い所で語る
VA = ["3:2 3:1 5:2 3:1", "2:2 3:1 2:1 5,:1 R:1",
      "R:1 1:1 3:1 5:2 3:1", "4:1 4:1 3:1 2:2 R:1",
      "2:1 2:1 4:1 6:2 5:1", "5:1 3:1 5:1 7:1 5:1 R:1",
      "R:1 6:1 5:1 4:1 2:1 4:1", "5:2 4:1 2:2 R:1"]
VA2 = ["5:2 5:1 6:2 5:1", "3:2 5:1 3:1 2:1 R:1",
       "R:1 3:1 5:1 1':2 6:1", "5:1 5:1 4:1 3:2 R:1",
       "2:1 2:1 4:1 6:2 5:1", "5:1 3:1 5:1 7:1 5:1 R:1",
       "R:1 6:1 5:1 4:1 2:1 4:1", "5:2 4:1 5:2 R:1"]
A1 = ("かみこっぷがおちる/やきんのきゅうけい/ろうかのあかりひとつ/ちいさなためいき/"
      "ねむるいきのおと/しずかにならんで/わたしのあしおとだけ/ろうかにひびくよ")
A2 = ("つけっぱなしらじお/さっきのあのふしが/あたまのなかでまわる/くちずさんでみる/"
      "ないしょのはなうた/だれもきいてない/あかいらんぷがともる/すてーじみたいだ")
# Bメロ: 長い音から始めて上がる。最後は属和音の上で止まる
VB = ["6:3 6:1 5:1 6:1", "7:2 1':1 7:1 5:1 R:1", "5:3 5:1 7:1 5:1", "6:2 6:1 6:2 R:1"]
B1 = "だれかのいたみを/てあてしてきた"
B2 = "よあけまではまだ/すこしとおいね"
# v5（2026-11-12 人間「1 残らない」）: サビを書き直す。調べた決まり（BMI「メロディのフックを強くする5つのこつ」）: 同じリズムを何行にもくり返す・音の数をそろえる・
#   サビのあとに題の言葉をもう一度言う所を作る・曲の頭から楽器でくり返す短い節を置く。
#   → 「あったかいね」を1小節の同じ形（ド・ファ・ミ・レ・ド＝4度跳んで順に降りる）で、すぐ2回続けて歌う（2回目は1段下）。これを2行。
#     サビの最後の5文字（ほしになる・うたになる・あさがくる）も同じ形で歌う。同じ節を、出だしと終わりのピアノも弾く
HOOK = "5:1 1':1 7:1 6:1 5:1.5 R:0.5"
VC = [HOOK, "4:1 6:1 5:1 4:1 3:1.5 R:0.5",
      "R:1 3:1 5:1 6:2 5:1", "3:1 2:1 1:2 1:1 R:1",
      HOOK, "4:1 6:1 5:1 4:1 5:1.5 R:0.5",
      "R:1 5:1 6:1 1':2 6:1", "5:1 6:1 5:2 3:1 R:1",
      "6:2 6:1 1':2 6:1", "5:2 3:1 5:2 R:1",
      "7:2 7:1 5:2 3:1", "3:2 1:3 R:1",
      "R:1 2:1 4:1 6:2 5:1", "4:3 5:2 R:1",
      "5:1 1':1 7:1 5:1 1':2", "R:6"]
C1 = "あったかいね/あったかいね/てのひらのなかで/あったかいね/あったかいね/かみこっぷひとつで/だれかのよるを/まもったてにも/ゆげがのぼって/ほしになる"
C2 = "あったかいね/あったかいね/さっきのはなうたを/あったかいね/あったかいね/くちびるにのせて/ながいろうかも/かわにかわって/あしおとさえ/うたになる"
CL = "あったかいね/あったかいね/よあけのてまえで/あったかいね/あったかいね/からっぽのそこにも/あまいにおいと/ふしがのこる/さあもどろう/あさがくる"
# ブリッジ: ナースコールが鳴りやむ。ほとんど同じ高さでつぶやく
VBR = ["R:3 6:1 6:1 5:1", "6:2 5:3 R:1", "R:3 4:1 4:1 3:1", "5:2 3:3 R:1",
       "R:3 6:1 6:1 7:1", "7:2 5:3 R:1", "R:2 4:1 4:1 5:1 6:1", "5:2 5:3 R:1"]
CB = "なりやんだ/ろうかには/わたしだけ/ひといきつく"
LY = Lyrics(S)


def put(name, lines, text, o=4):
    bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", VA + VA2, A1)
put("Bメロ1", VB, B1)
put("サビ1", VC, C1)
put("Aメロ2", VA + VA2, A2)
put("Bメロ2", VB, B2)
put("サビ2", VC, C2)
put("ブリッジ", VBR, CB)
put("最後のサビ", VC, CL)

# ================= 和音と線 =================
root = lambda b: S.chords[b].split("|")[0].split("/")[0]


def arp(b, idx, lo="A3", hi="C6", tr=PR, L=1):
    t = tones(root(b), lo, hi); tr.bar(b, " ".join(f"{nm(t[q % len(t)])}:{L:g}" for q in idx))


def chord(b, pat, c=62):
    v = voice(root(b), c, 3)
    for j in range(3): PC[j].bar(b, " ".join(t.replace("x", nm(v[j])) for t in pat.split()))


def saw(b, pat, c=67):
    v = voice(root(b), c, 3)
    for j in range(3): SAW[j].bar(b, " ".join(t.replace("x", nm(v[j])) for t in pat.split()))


def top(b, lo, hi, k=-1): return nm(tones(root(b), lo, hi)[k])


def lowp(b): return nm(low(S.chords[b], "E1") + 12)       # ピアノの左手（ベースの1オクターブ上）


SOLO = ["D5:1 F5:1 A5:3 G5:1", "E5:2 G5:1 D5:3", "C5:1 E5:1 G5:3 E5:1", "F5:2 E5:1 D5:3",
        "Bb4:1 D5:1 F5:3 A5:1", "G5:2 F5:1 D5:2 C5:1", "A5:3 G5:1 E5:1 C5:1", "D5:2 F5:1 G5:2 R:1"]     # 間奏2: ピアノの旋律（チェロが下で歌う）
MOTIF = ["R:6", "R:3 A5:1 C6:1 D6:1", "C6:2 G5:4", "R:6"]                                           # 合いことばの節（F長調で 3・5・6・5・2）。間奏に1回だけ

for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "紙コップ":                                                                              # 出だし: ピアノがサビの節（あったかいね）を先に弾く → 分散和音
        PL.bar(b, f"{lowp(b)}:6")
        if i == 0: PR.bar(b, "C5:1 F5:1 E5:1 D5:1 C5:2")
        elif i == 2: PR.bar(b, "Bb4:1 D5:1 C5:1 Bb4:1 A4:2")
        else: arp(b, (0, 2, 4, 5, 4, 2))
        if i >= 2: WG[0].bar(b, f"{top(b, 'C5', 'C6')}:6")
    elif n == "Aメロ1":
        PL.bar(b, f"{lowp(b)}:6")
        if i < 8: arp(b, (0, 2, 4, 5, 4, 2) if i % 2 == 0 else (1, 3, 4, 6, 4, 3))                 # 前半: ピアノの分散和音だけ
        else:                                                                                      # 後半: 分散和音が広がり、グラスハープが2小節ごとにのびる
            arp(b, (0, 3, 5, 7, 5, 3) if i % 2 == 0 else (1, 4, 6, 7, 6, 4))
            if i % 2 == 0: WG[0].bar(b, f"{top(b, 'C5', 'C6')}:6")
            if i % 4 == 3: TG.bar(b, f"R:4 {top(b, 'A5', 'A6', -2)}:1 {top(b, 'A5', 'A6')}:1")
    elif n == "Aメロ2":                                                                              # 2番: ドラムが入ったまま。ピアノは1拍目と4拍目の和音、チェロが下で長く歌う
        chord(b, "x:2 R:1 x:2 R:1" if i % 4 != 3 else "x:2 R:1 x:1 x:1 x:1")
        t = tones(root(b), "C3", "C4"); CELLO.bar(b, f"{nm(t[1 if i % 2 == 0 else 2])}:6" if i % 4 != 3 else f"{nm(t[1])}:3 {nm(t[2])}:3")
        if i % 4 == 3: arp(b, (2, 4, 5, 7, 5, 4))
        if i >= 8 and i % 2 == 1: TG.bar(b, f"R:4 {top(b, 'A5', 'A6')}:1 {top(b, 'A5', 'A6', -2)}:1")
    elif n in ("Bメロ1", "Bメロ2"):                                                                   # ピアノの和音がのぼり、弦の線が上がる。最後の2拍は全員止まる
        chord(b, "x:3 x:3" if i < 3 else "x:2 x:2 R:2", 62 + 2 * i); PL.bar(b, f"{lowp(b)}:6" if i < 3 else f"{lowp(b)}:4 R:2")
        tn = tones(root(b), "A4", "A6"); a_ = min(tn, key=lambda m: abs(m - (72 + 2.5 * i + (5 if n == "Bメロ2" else 0)))); b_ = next((m for m in tn if m > a_), a_)
        STRL.bar(b, f"{nm(a_)}:4 {nm(b_)}:2" if i < 3 else f"{nm(a_)}:2 {nm(b_)}:2 R:2")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        thick = n != "サビ1" or i >= 8                                                              # サビ1 は後半から厚くなる
        # v5（人間「2 気持ちよさが欲しい」）: サビでもピアノの分散和音を止めない（8分6つのゆれを流しつづける）。和音は下でのばし、弦の低い和音が包む
        chord(b, "x:6", 60); PL.bar(b, f"{lowp(b)}:6"); arp(b, (0, 2, 4, 5, 4, 2) if i % 2 == 0 else (1, 3, 4, 6, 4, 3), lo="C4", hi="F6")
        if thick:
            v = voice(root(b), 55, 3)
            for j in range(2): STP[j].bar(b, f"{nm(v[j + (1 if j else 0)])}:6")
        if (n == "サビ2" and i >= 8) or n == "最後のサビ": saw(b, "x:3 x:3")
        # 星（筒の鉄琴）: 「ねー」とのばす小節（2・6小節目）で答える。4小節ごとの終わりにも
        if i in (1, 5): TG.bar(b, f"R:2 {top(b, 'A5', 'A6', -3)}:1 {top(b, 'A5', 'A6', -2)}:1 {top(b, 'A5', 'A6')}:2")
        elif i % 4 == 3: TG.bar(b, f"R:4 {top(b, 'A5', 'A6')}:1 {top(b, 'A5', 'A6', -2)}:1")
        if n != "サビ1" and i % 2 == (1 if n == "サビ2" else 0):                                      # オルゴール: サビ2 は1小節おき、最後のサビは別の小節で
            tb = tones(root(b), "C5", "F6"); MB.bar(b, " ".join(f"{nm(tb[q % len(tb)])}:1" for q in (0, 2, 4, 3, 5, 4)))
        if n == "最後のサビ": STRH.bar(b, f"{top(b, 'A5', 'A6')}:6")
        if n != "サビ1":
            t = tones(root(b), "C3", "D4"); CELLO.bar(b, f"{nm(t[2])}:6" if i % 2 == 0 else f"{nm(t[2])}:4 {nm(t[1])}:2")
    elif n == "間奏":                                                                                # 鼻歌がよみがえる: 筒の鉄琴が合いことばの節を1回だけ
        arp(b, (0, 2, 4, 5, 4, 2) if i % 2 == 0 else (1, 3, 5, 6, 5, 3)); PL.bar(b, f"{lowp(b)}:6"); TG.bar(b, MOTIF[i])
        if i % 2 == 0: WG[1].bar(b, f"{top(b, 'C5', 'C6')}:6")
        t = tones(root(b), "C3", "D4"); CELLO.bar(b, [f"{nm(t[2])}:6", f"{nm(t[1])}:4 {nm(t[2])}:2", f"{nm(t[2])}:3 {nm(t[3 % len(t)])}:3", f"{nm(t[1])}:6"][i])   # v5（「6 やや単調」）: チェロが下で動く
    elif n == "ブリッジ":                                                                            # ナースコールが鳴りやむ: グラスハープだけ → 最後の2小節でピアノがのぼる
        v = voice(root(b), 72, 3)
        for j in range(2): WG[j].bar(b, f"{nm(v[j + 1])}:6")
        if i >= 4: PL.bar(b, f"{lowp(b)}:6")
        if i == 6: chord(b, "x:3 x:3", 64)
        if i == 7: chord(b, "x:1 x:1 x:1 x:1 x:1 x:1", 66); STRL.bar(b, f"{top(b, 'C5', 'C6', -2)}:3 {top(b, 'C5', 'C6')}:3")
    elif n == "間奏2":                                                                               # ピアノとチェロの二重奏
        PM.bar(b, SOLO[i]); PL.bar(b, f"{lowp(b)}:6"); chord(b, "R:1 x:2 R:1 x:2", 60)
        t = tones(root(b), "C3", "D4"); CELLO.bar(b, f"{nm(t[1])}:3 {nm(t[2])}:3" if i % 2 == 0 else f"{nm(t[3 % len(t)])}:4 {nm(t[2])}:2")
        if i >= 4:                                                                                   # v5（「6 やや単調」）: 後半は筒の鉄琴がピアノの旋律を1オクターブ上で重ね、弦の低い和音が入る
            TG.bar(b, " ".join(t if t.startswith("R") else nm(midi(t.split(":")[0]) + 12) + ":" + t.split(":")[1] for t in SOLO[i].split()))
            v = voice(root(b), 55, 3)
            for j in range(2): STP[j].bar(b, f"{nm(v[j + (1 if j else 0)])}:6")
    elif n == "アウトロ":
        if i < 5: arp(b, (0, 2, 4, 5, 4, 2) if i % 2 == 0 else (1, 3, 4, 6, 4, 3)); PL.bar(b, f"{lowp(b)}:6")
        else: PR.bar(b, "C5:1 F5:1 E5:1 D5:1 C5:2"); PL.bar(b, f"{lowp(b)}:6")                         # 終わり: ピアノがサビの節をもう一度
        if i in (0, 2, 4): WG[0].bar(b, f"{top(b, 'C5', 'C6')}:6")

# ================= ベース（8分の6。頭に根音、最後の3つで次の和音へ近づく。共通の部品は使わない）=================
def bl(b, style):
    ch = S.chords[b]; r = low(ch, "E1"); nx = S.chords[b + 1] if b + 1 < S.nb else ch; rn = low(nx, "E1")
    up = tones(root(b), nm(r + 1), nm(r + 12))
    t3 = next((m for m in up if (m - r) in (3, 4)), r + 7); t5 = next((m for m in up if (m - r) in (6, 7, 8)), r + 7)
    o = r + 12; ap = t5 if rn == r else (rn - 1 if rn > r else rn + 1)
    N = nm
    return {"long": f"{N(r)}:6",
            "one": f"{N(r)}:4.5 R:0.5 {N(ap)}:1",                           # 頭でのばして、6拍目で次へ
            "sway": f"{N(r)}:3 {N(t5)}:2 {N(ap)}:1",                        # 1拍目と4拍目（ゆれる）。切らずにつなぐ
            "walk": f"{N(r)}:2 {N(t3)}:1 {N(t5)}:2 {N(ap)}:1",              # 根音・3度・5度でのぼって、近づく（オクターブへは跳ばない）
            "push": f"{N(r)}:3 {N(r)}:1 {N(t5)}:1 {N(ap)}:1",               # サビ: 頭を長く、後ろの3つで動く
            "stop": f"{N(r)}:3 {N(t5)}:1 R:2"}[style]


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "Aメロ1" and i >= 8: BASS.bar(b, bl(b, "walk" if i == 15 else "one"))
    elif n == "Aメロ2": BASS.bar(b, bl(b, "walk" if i % 4 == 3 else "sway"))
    elif n in ("Bメロ1", "Bメロ2"): BASS.bar(b, bl(b, "stop" if i == 3 else ("long" if i < 2 else "push")))
    elif n in ("サビ1", "サビ2", "最後のサビ"): BASS.bar(b, bl(b, "walk" if i % 4 == 3 else ("push" if i % 2 == 0 else "sway")))
    elif n == "間奏": BASS.bar(b, bl(b, "one"))
    elif n == "間奏2": BASS.bar(b, bl(b, "walk" if i % 4 == 3 else "sway"))
    elif n == "ブリッジ" and i >= 6: BASS.bar(b, bl(b, "long" if i == 6 else "walk"))
    elif n == "アウトロ" and i < 5: BASS.bar(b, bl(b, "long"))
    # サブベース（深さ）: サビ1 は後半から、サビ2・最後のサビ・間奏2 の後半。ブリッジの前半はサブベースだけが下にいる
    if (n == "サビ1" and i >= 8) or n in ("サビ2", "最後のサビ") or (n == "間奏2" and i >= 4): SUB.bar(b, f"{nm(low(S.chords[b], 'E1'))}:5 R:1")
    elif n == "ブリッジ" and i < 4: SUB.bar(b, f"{nm(low(S.chords[b], 'E1'))}:6")

# ================= ドラム（8分の6。1小節＝24マス）=================
def g6(s): return s.replace(" ", "")


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "Aメロ1" and i >= 8:                             # キックと、スネアの縁をそっと。刻みは1・3・4・6拍
        D.set(b, g6("X... .... .... .... .... ...."), g6(".... .... .... o... .... ...."), g6("x... .... x... x... .... x..."))
    elif n == "間奏":
        D.set(b, g6("X... .... .... .... .... ...."), g6(".... .... .... o... .... ...."), g6("x... .... x... x... .... x..."))
    elif n == "Aメロ2":                                      # 8分6つの刻み。2小節に1回、キックが6拍目に入る
        D.set(b, g6("X... .... .... .... .... x...") if i % 2 == 1 else g6("X... .... .... .... .... ...."),
              g6(".... .... .... x... .... ....") if i % 4 != 3 else g6(".... .... .... x... .... ..o."),
              g6("x... x... x... x... x... x...") if i % 4 != 3 else g6("x... x... x... x... x.x. x.x."))
    elif n in ("Bメロ1", "Bメロ2"):                           # キックが1・4拍 → 最後はスネアでのぼって止まる
        if i < 3: D.set(b, g6("X... .... .... X... .... ...."), "." * 24 if i < 2 else g6(".... .... .... X... .... ...."), g6("x... x... x... x... x... x..."))
        else: D.set(b, g6("X... .... X... .... .... ...."), g6("X... X... X.X. XXXX .... ...."), "." * 24)
    elif n in ("サビ1", "サビ2", "最後のサビ"):               # 半分の速さ: キック1拍目、スネア4拍目。のこぎり波のリズムに合わせて、キックを足す
        # v5（「2 気持ちよさが欲しい」。調べた決まり＝UJAM: キックとスネアは半分の速さで間をあけ、編成は簡単に・息ができるすき間を残す）:
        #   小節ごとに型を変えない。キックは1拍目と、次の小節へ押す6拍目。スネアは4拍目。ハイハットは8分6つで、3拍目と6拍目の裏に小さく1つ（ゆれ）
        kk = g6("X... .... .... .... .... x...")
        ss = g6(".... .... .... X... .... ....") if i % 2 == 0 else g6(".... .... ..o. X... .... ....")
        hh = g6("x... x... x.x. x... x... x.x.")
        if i % 8 == 7 and not last:                          # フィルは8小節の終わり（タムで降りる）
            ss = g6(".... .... .... X... .... ...."); hh = g6("x... x... x... .... .... ...."); D.tom(b, "R:4 C4:0.5 A3:0.5 F3:0.5 D3:0.5!")
        D.set(b, kk, ss, hh)
        if i % 8 == 0: crash(D, b, "C2", 6)
        if n != "サビ1": KDR.bar(b, "R:3 B4:1 R:2")           # サビ2 からクラップを重ねる
    elif n == "ブリッジ":
        if i == 6: D.set(b, g6("X... .... .... X... .... ...."), "." * 24, g6("x... .... x... x... .... x..."))
        if i == 7: D.set(b, g6("X... .... .... X... .... X..."), g6("x... x... x... x.x. x.x. XXXX"), "." * 24)
    elif n == "間奏2":                                       # 二重奏: 前半はキックと縁だけ、後半からサビと同じ半分の速さ
        if i < 4: D.set(b, g6("X... .... .... .... .... ...."), g6(".... .... .... o... .... ...."), g6("x... x... x... x... x... x..."))
        else:
            D.set(b, g6("X... .... .... .... .... x..."),
                  g6(".... .... .... X... .... ....") if i < 7 else g6(".... .... .... X... X.X. XXXX"), g6("x... x... x.x. x... x... x.x.") if i < 7 else g6("x... x... x... .... .... ...."))
        if i == 4: crash(D, b, "C2", 6)
    elif n == "アウトロ" and i == 0: crash(D, b, "C2", 6)

# v5: 紙コップの「コトン」は外した（人間「4 外して」）
cym_swell(CYM, S.sc("サビ1")[0], 3, "C4"); cym_swell(CYM, S.sc("サビ2")[0], 3, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 6, "E4")

# 止め: Bメロ の最後の2拍は全員休み（サビの「あったかいね」を大きく聞かせる）
for nme in ("Bメロ1", "Bメロ2"): SIL.add(S.sc(nme)[-1], 4, 6)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の03（2時）。8分の6拍子のフューチャー・ソウル・バラード。F・8分音符 174。病院の夜勤の休けい室で、紙コップのカフェオレが手のひらをあたためる。"
          "丸いピアノの分散和音・グラスハープ・筒の鉄琴・オルゴール・チェロ・のこぎり波の和音・サブベース。合いことばの節は間奏の筒の鉄琴に1回だけ。自作")
finish(S, LY, V, 0,
       level={"verse": -0.2}, special={"ブリッジ": -0.6, "最後のサビ": 0.35, "アウトロ": -0.3})

# ================= 仕上げのあとに足すもの =================
from vt3x_lib import *
path = sys.argv[1]
humanize(path, "ピアノ（右手", mid=80, down=12, up=8, seed=3); humanize(path, "ピアノ（和音", mid=82, down=8, up=8, seed=5); humanize(path, "チェロ", mid=80, down=6, up=8, seed=7)
# 測ると、紙コップ（−30／BGM −43）が小さすぎ、2番の Aメロ・Bメロ（−14.9）が サビ1（−15.3）より大きく、最後のサビ（−14.7）が サビ2（−13.9）より小さかった → 仕上げで直す
final_gain(path, {"紙コップ": 10, "Aメロ1": 2.5, "Aメロ2": -1.0, "Bメロ2": -0.8, "サビ1": 0.3, "サビ2": 0.5, "最後のサビ": 2.2, "アウトロ": 1.5} if VOCAL else {"紙コップ": 16, "Aメロ1": 2.5, "Aメロ2": -1.3, "Bメロ2": -1.3, "間奏2": -1.0, "最後のサビ": 2.0, "アウトロ": 1.5})   # v5: 測って決めた
if VOCAL:
    remark(path, S, std_mark(("chorus",), jump=7, minlen=2.5))
    # 息つぎの音は入れない（2026-11-12 人間「吐息みたいなノイズ、こう言うのいらない」）。ウィスパーは息の成分を減らして使う
    vocal_polish(path, S, {"verse": 8, "pre": 14, "chorus": 24, "最後のサビ": 28, "bridge": 6}, scoop=0.3, slash=0.7, vib_min_beats=2.5, vib_start=0.5, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 8, None, K), ("最後のサビ", 0, None, K)], vol=0.36)
    # 声のチョップ: 間奏で、鼻歌を思い出すように「ら」を短く置く（筒の鉄琴の節のすき間に）
    im = S.sc("間奏")
    chops(path, S, {im[0]: "R:3 C5:1:ら A4:2:ら", im[3]: "R:1 F4:1:ら A4:1:ら C5:2:ら R:1"}, vol=0.26, pan=-0.25)
    # v5（人間「5 ある」＝声に息のようなノイズがまだある）: ウィスパーの声は、息の成分を減らしても、弱音源を 75% まぜているので息の音が残る。
    #   ピアノだけの静かな Aメロでは目立つ → ウィスパーを使わず、全部クリアの声にして、静かな場面は強さ（level・special）で小さく歌う
    voice_by_scene(path, S, {}, default="clear")
