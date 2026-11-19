# vt3 20「湯けむりスウィング」Steam-Bath Swing（仮）— エレクトロ・スウィング（4分の4・114・はねる8分）。ト短調（転調なし）。
# 第3弾（0時〜24時の街）の 19時。表は docs/sound/vt3-plan.md。
#
# v3（2026-11-19）: ゼロから作り直し。v1・v2 はビッグバンドのジャズ（176）。
#   人間の指示: 「18からは1曲ずつコンセプトとかジャンルをしっかり決めて作って行こうか。つまり作り直そう」。表を見せ、ジャンルは人間が B案（エレクトロ・スウィング）を選んだ（2026-11-19「bで」）。
#
# コンセプト: 夜の銭湯。ひとりで入ったお風呂で鼻歌を歌ったら、壁のむこうから同じ節が返ってくる。ひとりの時間を「みんなで歌う時間」に書きかえる。
# ジャンル: エレクトロ・スウィング。作る前に調べた決まりごと:
#   ・テンポ 110〜128。キックは4つ打ち、2拍めと4拍めにスネア（クラップ）、裏拍のハイハット。ハイハットと打楽器ははねさせる（55〜66%）
#   ・むかしの楽器（クラリネット・金管・ピアノ・ビブラフォン）を、フィルターをかけたり短く切ったりして、電子のキックとベースにのせる
#   ・しかけは少しずつ足して組み立てる
# 音の地図の場所: 電子の側（18・19 は生の楽器の側、16・17 はまん中）。ジャズの条件（電子の音を使わない）は、この曲では外す（人間が B案を選んだ）。
#
# 曲を決める表:
#   形: しずく（ビブラフォンと、古いラジオのようなピアノ）→ テーマ（ビートが入る・クラリネットの節）→ 鼻歌1（ひとり・左）→ 壁のむこう1（左が歌い、右のはなれた所から返事）
#       → サビ1（左ひとり）→ クラリネットの番 → 鼻歌2 → 壁のむこう2 → サビ2（左と右で同時に）→ 湯船が舞台（ビブラフォンの番。クラリネットが返事）→ もぐる（お湯の中。キックなし）→ 最後のサビ（まん中で重なる）→ 湯気（消えていく）
#   場面と強さ: しずく 中弱／テーマ 中強／鼻歌 中／壁のむこう 中（だんだん上げる）／サビ1 中強／クラリネットの番 中強／サビ2 強／もぐる 弱／最後のサビ 最強／湯気 弱 → 消える
#   旋律: 鼻歌は 5〜3' の音域でゆっくりはねる。1行ごとに2拍の休み（そこへクラリネットかビブラフォン）。いちばん高い音（7'）はサビの2行めだけ。
#   和音: Gm・Cm7・D7・E♭7（短調のスウィング）。サビは B♭ から始めて明るくする。
#   ベース: FM のシンセベースが根音とオクターブではねる。鼻歌は根音と5度の2つ打ち。下にサブベース。
#   ドラム: 電子のドラム。入り方は「ハイハットとクラップだけ → テーマでキックが入る」。鼻歌はキックを1拍めと3拍めだけ。
#   この曲だけ: ①壁ごしのかけ合い（歌が左、返事が右のはなれた所。サビ2 で左右同時、最後のサビで初めてまん中で重なる）②「もぐる」場面（お湯の中。あわの音）
#   声: ウィスパー 1 種類で最後まで（返事も同じ声を右に置く）。
#   終わり方: だんだん消える（19 の「1発で止める」と逆）。
#   ほかの曲とのちがい: 19（ブラスバンド）は生の太鼓とスーザフォン。こちらは4つ打ちのキックとシンセベースで、管はクラリネット1本とフィルターをかけた金管の合いの手だけ。
from vt25_lib import *
from vocalo_lib import KFX, fx_bar, rack_pluck, rack_supersaw, rack_bass, hat_roll
import re as _re

S = Song("20", "bathhouse", "湯けむりスウィング（仮）", "Steam-Bath Swing", 114, 4, "G", "minor", "エレクトロ・スウィング（ボカロ）")
S.kit = "electro"
S.flags = S.flags + " --space room --space-wet 0.1"
S.keep_old_synth = True
S.no_depth = True
S.keepers = {}
S.fade_out = 10
K = Key("G", "minor")          # oct 3 で 1 = G3。歌は 5（D4）〜 7'（F5）

_T = _re.compile(r"^([^:]+):([0-9.]+)(.*)$")


def warp(t):
    """はねる8分（62.5%）: 拍の前半を 0.625、後半を 0.375 に"""
    b = int(t + 1e-9); f = t - b
    return b + (f * 1.25 if f <= 0.5 + 1e-9 else 0.625 + (f - 0.5) * 0.75)


def sw(s):
    out, t = [], 0.0
    for x in s.split():
        m = _T.match(x); n, L, mk = m.group(1), float(m.group(2)), m.group(3)
        a, z = warp(t), warp(t + L); out.append(f"{n}:{z - a:.4f}".rstrip("0").rstrip(".") + mk); t += L
    return " ".join(out)


VA = ["Gm", "Gm", "Cm7", "D7", "Gm", "Eb7", "D7", "Gm"]
PRE = ["Cm7", "F7", "Bb", "Eb", "Cm7", "D7", "Gm", "D7"]
CHO = ["Bb", "D7", "Gm", "Cm7", "Bb", "D7", "Eb", "D7"]
BRG = ["Eb", "Eb", "Cm7", "Cm7", "Eb", "Eb", "D7", "D7"]
OUT = ["Gm", "Eb7", "Gm", "Eb7", "Gm", "Eb7", "Gm", "Gm"]
S.scene("しずく", 8, "intro", VA)
S.scene("テーマ", 8, "solo", VA)
S.scene("鼻歌1", 8, "verse", VA)
S.scene("壁のむこう1", 8, "pre", PRE)
S.scene("サビ1", 8, "chorus", CHO)
S.scene("クラリネットの番", 8, "solo", VA)
S.scene("鼻歌2", 8, "verse", VA)
S.scene("壁のむこう2", 8, "pre", PRE)
S.scene("サビ2", 8, "chorus", CHO)
S.scene("湯船が舞台", 8, "solo", VA)
S.scene("もぐる", 8, "bridge", BRG)
S.scene("最後のサビ", 16, "chorus", CHO + CHO)
S.scene("湯気", 12, "outro", OUT + ["Gm", "Eb7", "Gm", "Gm"])

V = Voice(S, vol=0.2, delay=0.25, bright=0.0, patch="kfbSineLead", low=False)
D = S.drumkit()
LY = Lyrics(S)

# ================= 歌 =================
# 1 回め、19 と同じリズムの形（8分が7つ → のばす）を使っていて「リズムが 100% 同じ」と出たので、形を作り直した:
#   長い音から入る・1拍休んでから入る・小節のまん中でのばす、を行ごとに入れかえる
M8a = ["5:1 5:0.5 7:0.5 1':1.5 1':0.5", "7:0.5 5:0.5 1':2 R:1"]
M7a = ["R:1 1':0.5 2':0.5 3':1.5 2':0.5", "3':0.5 1':0.5 2':2 R:1"]
M8b = ["5:1 7:0.5 1':0.5 3':1.5 3':0.5", "2':0.5 1':0.5 3':2 R:1"]
M7b = ["R:1 2':0.5 2':0.5 1':1.5 2':0.5", "1':0.5 5:0.5 1':2 R:1"]
TV1 = "のれんをくぐれば/ゆげがてをふる/ひとりのおふろで/はなうたひとつ"
TV2 = "となりのだれかも/おなじふしだね/しらないひとでも/うたならわかる"
# 壁のむこう: 2小節 歌（左）→ 2小節 返事（右）
P_M1 = ["3':1.5 3':0.5 2':0.5 1':1.5", "1':0.5 2':0.5 3':0.5 4':1.5 R:1"]
P_A1 = ["3':1.5 3':0.5 2':0.5 1':1.5", "2':0.5 3':0.5 3':2 R:1"]
P_M2 = ["3':1.5 3':0.5 2':0.5 1':1.5", "1':0.5 2':0.5 1':0.5 2':1.5 R:1"]
P_A2 = ["1':1.5 2':0.5 3':0.5 5':1.5", "3':0.5 2':0.5 2':2 R:1"]
TP1 = "かべのむこうから/おなじはなうた/だれだかしらない/けれどうたおう"
TP2 = "ゆぶねがぶたいだ/ひびくよたかく/のぼせちゃうまえに/もういちどだけ"
# サビ（いちばん高い音 7' は2行めだけ）
S1 = ["5':1 5':0.5 3':0.5 5':2", "6':0.5 5':0.5 3':0.5 5':1.5 R:1"]
S2 = ["3':1 5':0.5 5':0.5 7':2", "5':0.5 3':0.5 2':0.5 3':1.5 R:1"]
S3 = ["5':1 5':0.5 3':0.5 5':2", "6':0.5 5':0.5 6':0.5 5':1.5 R:1"]
S4 = ["6':1 5':0.5 3':0.5 5':2", "3':0.5 2':0.5 1':0.5 2':1.5 R:1"]
TS1 = "ゆけむりすいんぐ/つかれがとけてく/ゆけむりすいんぐ/ひとりじゃないよる"
TS2 = "ゆけむりすいんぐ/のぼせてもいいや/ゆけむりすいんぐ/あしたもきてよね"
# もぐる（お湯の中。ゆっくり）
BR = ["3':1 3':1 2':1 1':1", "1':0.5 2':0.5 3':2 R:1", "3':1 3':1 4':1 3':1", "2':0.5 1':0.5 2':0.5 1':1.5 R:1",
      "3':1 3':1 2':1 1':1", "1':0.5 2':0.5 3':2 R:1", "2':1 2':1 4':1 2':1", "5':0.5 4':0.5 5':2 R:1"]
TB = "おゆのなかでは/こえもまるくなる/かべがあるのに/とどいているよ"
OUTV = ["1':1 3':1 5':2", "R:4", "3':1 5':1 1':2", "R:4"]      # 2 回め: 低い鼻歌（D4〜G4）が伴奏より 13dB 小さく、うもれていた → 高さを上げた


def put(name, lines, text, at=0):
    bars = S.sc(name)[at:]; mel = [sw(K.mel(x, oct=3)) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars[:len(mel)], mel, text, name)


put("鼻歌1", M8a + M7a + M8b + M7b, TV1); put("壁のむこう1", P_M1 + P_A1 + P_M2 + P_A2, TP1); put("サビ1", S1 + S2 + S3 + S4, TS1)
put("鼻歌2", M8a + M7a + M8b + M7b, TV2); put("壁のむこう2", P_M1 + P_A1 + P_M2 + P_A2, TP2); put("サビ2", S1 + S2 + S3 + S4, TS2)
put("もぐる", BR, TB); put("最後のサビ", S1 + S2 + S3 + S4 + S1 + S2 + S3 + S4, TS1 + "/" + TS2)
put("湯気", OUTV, "るるる/るるる")

# ================= 楽器 =================
BST = lambda g: [{"type": "boost", "gain": g}]
RADIO = [{"type": "filter", "freq": 1400, "q": 0.9}, {"type": "bitcrusher", "bits": 11, "mix": 0.25}]      # 古いラジオのような音
CLA = S.track("クラリネット", "brass", patch="clarinet", volume=0.5, pan=0.2, reverb=0.25, fx=BST(7))      # 管の録音の音は volume だけでは小さい（19 で分かった）
BRS = [S.track(f"金管の合いの手{i + 1}（フィルター）", "brass", patch="brassSection", volume=0.5, pan=(-0.35, 0.0, 0.35)[i], reverb=0.2,
               fx=[{"type": "filter", "freq": 2200, "q": 0.7}] + BST(4)) for i in range(3)]
PNO = [S.track(f"ラジオのピアノ{i + 1}", "piano", volume=0.16, pan=(-0.25, -0.1, 0.05)[i], reverb=0.15, sustain=0.6, fx=RADIO) for i in range(3)]
VIB = S.track("ビブラフォン", "keys", patch="vibraphone", volume=0.45, pan=-0.3, reverb=0.35, fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.22, "feedback": 0.3}])
BASS = S.track("FM のベース", "bass", patch="kfbFmBass", volume=0.065, pan=0, duck=0.3, fx=rack_bass())
SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.016, pan=0, duck=0.4)
PAD = [S.track(f"きらめくパッド{i + 1}", "lead", patch="kfbSparklePad", volume=0.03, pan=(-0.45, 0.0, 0.45)[i], reverb=0.25, duck=0.6, fx=rack_supersaw()) for i in range(3)]
PLK = S.track("駆け上がるプラック", "lead", patch="kfbSquarePluck", volume=0.05, pan=0.3, reverb=0.25, fx=rack_pluck())
HAT = S.track("ハイハット（裏拍・はねる）", "guitar", patch="kawaiiFx", volume=0.08, pan=-0.2, reverb=0.08, modulate=False)
FXT = S.track("効果音（あわ・上がる音）", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.3, modulate=False)

root = lambda b: S.chords[b].split("|")[0].split("/")[0]
KC = lambda line, o=4: sw(K.mel(line, oct=o))


def skank(b, tracks=PNO, c=64, pat="R:0.5 x:0.5 R:0.5 x:0.5 R:0.5 x:0.5 R:0.5 x:0.5"):
    """裏拍で短く打つ和音（3音）"""
    v = sorted(voice(root(b), c, 3))
    for j, t in enumerate(tracks): t.bar(b, sw(" ".join(x if x.startswith("R") else f"{nm(v[j])}:{x.split(':')[1]}" for x in pat.split())))


def bass(b, kind):
    r = low(S.chords[b], "F1"); nx = low(S.chords[b + 1], "F1") if b + 1 < S.nb else r
    R_, O, F, A = nm(r), nm(r + 12), nm(r + 7), nm(nx - 1 if nx != r else r + 7)
    pats = {"bounce": f"{R_}:0.5 R:0.5 {O}:0.5 {R_}:0.5 R:0.5 {R_}:0.5 {F}:0.5 {A}:0.5",
            "bounce2": f"{R_}:0.5 {O}:0.5 R:0.5 {R_}:0.5 {F}:0.5 R:0.5 {O}:0.5 {A}:0.5",
            "two": f"{R_}:1.5 {R_}:0.5 {F}:1.5 {A}:0.5",
            "walk": f"{R_}:1 {nm(r + 3 if 'm' in root(b) and 'maj' not in root(b) else r + 4)}:1 {F}:1 {A}:1",
            "long": f"{R_}:4"}
    BASS.bar(b, sw(pats[kind])); SUB.bar(b, f"{R_}:{'4' if kind in ('long', 'two') else '2 ' + R_ + ':2'}")


def hats(b, open_last=False, busy=False):
    pat = "R:0.5 C#5:0.5 " * 3 + ("R:0.5 D5:0.5" if open_last else "R:0.5 C#5:0.5")
    if busy: pat = "R:0.5 C#5:0.5 R:0.5 C#5:0.25 C#5:0.25 R:0.5 C#5:0.5 R:0.5 " + ("D5:0.5" if open_last else "C#5:0.5")
    HAT.bar(b, sw(pat))


def pad(b, c=62):
    v = sorted(voice(root(b), c, 3))
    for j in range(3): PAD[j].bar(b, f"{nm(v[j])}:4")


def stabs(b, pat="R:1.5 x:0.5 R:1.5 x:0.5", c=65):
    skank(b, BRS, c, pat)


def arp(b, c=72):
    """16分で駆け上がって、最後の音が残る"""
    v = sorted(voice(root(b), c, 3)); n = [v[0], v[1], v[2], v[0] + 12, v[1] + 12, v[2] + 12]
    PLK.bar(b, "R:2 " + " ".join(f"{nm(x)}:0.25" for x in n) + f" {nm(n[5])}:0.5")


THEME = ["5:0.5 7:0.5 1':0.5 2':0.5 3':1 1':1", "5':1.5 3':0.5 1':1 R:1", "4:0.5 6:0.5 1':0.5 3':0.5 4':1 3':1", "2':0.5 #7:0.5 2':0.5 4':0.5 3':0.5 2':0.5 #7:0.5 5:0.5",
         "1':0.5 R:0.5 1':0.5 3':0.5 5':1 3':1", "6':1.5 5':0.5 3':1 1':1", "2':0.5 4':0.5 #7:0.5 2':0.5 5:1 #7:1", "1':1 R:3"]
THEME2 = ["1':0.5 3':0.5 5':0.5 3':0.5 1':0.5 3':0.5 5':1", "7':1 5':0.5 3':0.5 1':1 R:1", "3':0.5 4':0.5 6':0.5 4':0.5 3':1 1':1", "2':0.5 4':0.5 #7:0.5 4':0.5 2':1 5:1",
          "1':0.5 R:0.5 1':0.5 3':0.5 5':1 3':1", "6':1.5 5':0.5 3':1 1':1", "2':0.5 4':0.5 #7:0.5 2':0.5 5:1 #7:1", "1':1 R:3"]
FILL = ["R:3 5:0.5 7:0.5", "R:3 4':0.5 2':0.5", "R:3 3':0.5 6':0.5", "R:3 1':0.5 7:0.5"]          # 歌の行のあと（4拍め）の合いの手
HEAD = {2: "1':1 R:3", 6: "5':1 R:3"}                                                              # その続き（次の小節の1拍め。歌が1拍休んで入る行だけ）
DRIP = ["5'':1 R:1 3'':0.5 1'':1.5", "R:2 7':1 5':1", "6'':1 R:1 4'':0.5 3'':1.5", "R:2 2'':1 #7':1"]        # しずく（高い所から落ちる）
K4 = "X...X...X...X..."; K2 = "X.......X......."; CL = "....X.......X..."; CLs = "....x.......x..."; NO = "................"

for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "しずく":                                               # ラジオのピアノとしずく → ハイハットとクラップとベース（キックはまだ）
        skank(b); VIB.bar(b, KC(DRIP[i % 4], 3))
        if i % 2 == 0: FXT.bar(b, fx_bar((2.5, "awa", 1)))
        hats(b); bass(b, "two" if i < 4 else "walk")
        if i >= 4: D.set(b, NO, "............x...", NO)
        if last: FXT.bar(b, fx_bar((0, "up", 4))); hat_roll(HAT, b, 1)
    elif n in ("テーマ", "クラリネットの番"):
        two = n != "テーマ"
        D.set(b, K4, CL if not last else "....X.....x.XXXX", NO); hats(b, open_last=i % 2 == 1, busy=two); bass(b, "bounce" if i % 2 == 0 else "bounce2"); skank(b)
        CLA.bar(b, KC((THEME2 if two else THEME)[i]))
        if two and i % 2 == 1 and not last: arp(b)
        if two and i in (3, 7):                                     # ピアノを短く切ってくり返す（サンプルを刻んだような音）
            v = sorted(voice(root(b), 64, 3))
            for j in range(3): PNO[j].bar(b, sw("R:0.5 x:0.5 R:0.5 x:0.5".replace("x", nm(v[j]))) + " " + " ".join(f"{nm(v[j])}:0.25" for _ in range(8)))
        if i == 0: FXT.bar(b, fx_bar((0, "impact", 2)))
    elif n == "湯船が舞台":                                         # ビブラフォンがテーマを弾き、クラリネットが返事。プラックが駆け上がる
        D.set(b, K4, CL if not last else "....X...x.x.XXXX", NO); hats(b, open_last=i % 2 == 1, busy=True); bass(b, "bounce2" if i % 2 == 0 else "bounce"); skank(b)
        VIB.bar(b, KC(THEME[i], 4))
        if i % 2 == 1 and not last: CLA.bar(b, KC(FILL[(i // 2 + 1) % 4], 4))
        if i % 2 == 0: arp(b)
        if i == 0: FXT.bar(b, fx_bar((0, "impact", 2)))
    elif n.startswith("鼻歌"):                                     # ひとりの鼻歌。キックは1拍めと3拍めだけ。行のあとに合いの手（1番 クラリネット・2番 ビブラフォン）
        two = n.endswith("2")
        D.set(b, K2, CLs, NO); hats(b); bass(b, "two")
        if two: skank(b)
        if i % 2 == 1: (VIB if two else CLA).bar(b, KC(FILL[i // 2], 4))
        elif i in HEAD: (VIB if two else CLA).bar(b, KC(HEAD[i], 4))
        if i % 4 == 0: FXT.bar(b, fx_bar((3, "awa", 1)))
    elif n.startswith("壁のむこう"):                               # 左の歌 2小節 → 右の返事 2小節。だんだん足す
        D.set(b, K4, NO if i < 4 else CL, NO); hats(b, busy=i >= 4); bass(b, "bounce" if i % 2 == 0 else "bounce2"); skank(b)
        if i >= 4: pad(b)
        if i in (2, 3, 6, 7): VIB.bar(b, KC(DRIP[i % 4], 3))        # 返事の所で、しずくが落ちる
        if last: D.set(b, K4, "....X...x.x.XXXX", NO); FXT.bar(b, fx_bar((0, "up", 4))); hat_roll(HAT, b, 1)
    elif n.startswith("サビ") or n == "最後のサビ":
        lv = {"サビ1": 1, "サビ2": 2, "最後のサビ": 3}[n]; j = i % 8
        D.set(b, K4, CL if j != 7 or last else "....X.....x.XXXX", NO); hats(b, open_last=True, busy=lv >= 2); bass(b, "bounce" if i % 2 == 0 else "bounce2")
        skank(b); pad(b); stabs(b, "R:1.5 x:0.5 R:1.5 x:0.5" if j % 2 == 0 else "R:2.5 x:0.5 x:0.5 R:0.5")
        if j % 2 == 1: CLA.bar(b, KC(FILL[(j // 2) % 4], 4))       # 歌の休みにクラリネット
        if lv >= 2 and j % 2 == 0: arp(b)
        if lv == 3: VIB.bar(b, KC(DRIP[i % 4], 3))
        if i == 0: FXT.bar(b, fx_bar((0, "impact", 2), (2.5, "kira", 1)))
    elif n == "もぐる":                                             # お湯の中。キックなし。パッドとサブベースとしずくとあわ
        pad(b, 58); SUB.bar(b, f"{nm(low(S.chords[b], 'F1'))}:4"); VIB.bar(b, KC(DRIP[i % 4], 3))
        FXT.bar(b, fx_bar((1, "awa", 1), (3, "awa", 1)) if i < 6 else fx_bar((0, "up", 4)))
        if i >= 6: hats(b, busy=True); D.set(b, NO, NO if i == 6 else "........x.x.XXXX", NO)
        if last: hat_roll(HAT, b, 1)
    elif n == "湯気":                                               # 消えていく。ラジオのピアノとしずくとベース
        skank(b); VIB.bar(b, KC(DRIP[i % 4], 3)); bass(b, "long")
        if i < 6: hats(b); D.set(b, K2, CLs, NO)
        if i % 2 == 0: FXT.bar(b, fx_bar((2.5, "awa", 1)))

S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の20（19時）。エレクトロ・スウィング（114・はねる8分）。ト短調。夜の銭湯で鼻歌を歌ったら、壁のむこうから同じ節が返ってくる。"
          "歌は左、返事は右のはなれた所。最後のサビで初めてまん中で重なる。4つ打ちのキック・シンセベース・クラリネット・フィルターをかけた金管とピアノ・ビブラフォン。自作")
finish(S, LY, V, 0)

# ================= 仕上げのあとに足すもの =================
from vt3x_lib import *
path = sys.argv[1]
humanize(path, "クラリネット", mid=86, down=10, up=8, seed=3); humanize(path, "ピアノ", mid=80, down=10, up=8, seed=5); humanize(path, "ビブラフォン", mid=84, down=12, up=8, seed=7)
# 1 回めを曲から分けて測った: ドラム −30dB・ベース −23dB（歌より大きい）・前奏がテーマより 5dB 小さい・最後のサビ −16.1 より「湯船が舞台」−15.8 が大きい
#   → キックとクラップを上げ、ベースを下げ、前奏にハイハットとベースを最初から入れた。ビブラフォンを上げた
set_parts(path, "キック", volume=0.45); set_parts(path, "スネア", volume=0.26)
final_gain(path, {"しずく": 1.5, "最後のサビ": 1.2, "湯気": 0.5})
if VOCAL:
    backing(path, 0.9)   # 2026-11-13 人間「声以外のバック音量0.9ぐらいにしようか」
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 10, "pre": 10, "bridge": 10, "chorus": 20, "最後のサビ": 24, "outro": 10}, scoop=0.3, slash=0.7, vib_min_beats=1.5, vib_start=0.5, auto=0.6, breaths=0.0)
    harmony(path, S, [("サビ2", 0, None, K), ("最後のサビ", 0, None, K)], vol=0.4)
    voice_by_scene(path, S, {}, default="whisper")       # 1 曲 1 種類の声（2026-11-17 人間）
    sing_ends(path, S, max_len=2.0, throw=0.2)
    js = load(path)
    for v in js.get("vocals", []):
        v["debreath"] = 0.5; v["softCons"] = 0.3
        v["debreathAt"] = [[t + 0.03, 1.2] for t in [42.07, 71.56, 48.92, 77.76, 48.39, 107.34, 136.71, 69.34, 109.36, 79.97]]   # 息の点検が言った所だけ、追加で息の音を下げる

    # 壁ごしのかけ合い: 歌を置く場所で分ける（声の種類は同じ）。左＝歌、右＝返事（はなれた所。響きを多く）、まん中＝もぐる・最後のサビ・湯気
    def where(bar, harm):
        n, i, L, k = S.scene_of(bar)
        if n in ("もぐる", "最後のサビ", "湯気"): return "C"
        if harm: return "R"                                    # サビ2 のハモリは右（左と右で同時に歌う）
        if n.startswith("壁のむこう") and i in (2, 3, 6, 7): return "R"
        return "L"
    PLACE = {"L": dict(pan=-0.3), "R": dict(pan=0.4, reverb=0.42), "C": dict(pan=0.0)}
    new = []
    for vi, v in enumerate(js["vocals"]):
        per = {p: [] for p in PLACE}; t = 0.0
        for tok in v["notes"].split():
            L_ = float(tok.split(":")[1]); bar = min(S.nb - 1, int((t + 1e-6) // S.beats)); w = where(bar, vi > 0)
            for p in per: per[p].append(tok if (p == w or tok.startswith("R:")) else f"R:{L_:g}")
            t += L_
        for p, toks in per.items():
            if any(not x.startswith("R:") for x in toks):
                d = dict(v); d["notes"] = " ".join(toks); d.update(PLACE[p])
                if vi > 0 and p == "C": d["pan"] = 0.18
                new.append(d)
    js["vocals"] = new
    save(path, js); print(f"  歌を置く場所で分けた: {len(new)} 本")
