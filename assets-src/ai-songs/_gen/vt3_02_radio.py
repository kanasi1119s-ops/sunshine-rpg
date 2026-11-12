# vt3 02「深夜ラジオのペンネーム」Pen Name on Midnight Radio（仮）— 夜の2ステップ・エレクトロポップ。128・4/4。E♭長調。
# 第3弾（0時〜24時の街）の 1時。表は docs/sound/vt3-plan.md。
#
# v5（2026-11-12）: ゼロから作り直し。人間「02クソつまらない。曲全くこだわりを感じない」「聴きたいって思う曲ではない」「プロが作る曲ではない」
#   「1曲1曲こだわりを持って作り直して」。v1〜v4 はシティポップのバンド（エレピの伴奏・のばす弦・ふつうのドラム）に音を足しただけだった。
#   → 曲そのものを変える: テンポ・ノリ・和音・旋律・歌詞のサビ・音の世界・展開を、この曲（午前1時のふとんの中のラジオ）のために決め直す。
#
# 物語（そのまま）: 午前1時。家族にないしょで、まくらもとのラジオを小さな音で聞いている「わたし」。
#   ペンネーム「ねむれないかもめ」で出したはがきが読まれる。DJ は「大丈夫、朝は来る。その前に、ちょっと歌おう」と言って、5つの音の鼻歌を口ずさむ。
#   ── この鼻歌（合いことばの節 3・5・6・5・2）が、ここから街じゅうへ伝わっていく（アルバムの始まり）。
#
# 曲を決める表:
#   形: ラジオのつまみを回す（電波の雑音の中から音楽が浮かぶ）→ ふとんの中（指パッチンとキックだけ・ささやき）→ 胸が高鳴る（4つ打ちでのぼる・止まる）
#       → 電波に乗って飛ぶ（2ステップのサビ。ペンネームを呼ぶ）→ CM → はがきが読まれる → 飛ぶ → 間奏（電子のサックスがペンネームの節を吹く）→ DJ の声（半分の速さ・ほぼ無音）→ いちばん高く飛ぶ → 鼻歌とスイッチを切る音
#   強さ: チューニング 弱→中／Aメロ1 とても弱い→弱／Bメロ 中→止め／サビ1 中強／CM 弱／Aメロ2 弱（ノリは続く）／Bメロ2 中／サビ2 強／DJ の声 とても弱い→のぼる／最後のサビ いちばん強い／鼻歌 消える
#   旋律: Aメロ＝低い所で話すように（拍の頭から・8分と付点）。Bメロ＝長い音から折れて上がる。サビ＝ペンネーム「ねむれないかもめ」を同じ形で2回呼び（2回目は上へ）、後半は「3・3・2」で押す
#   和音: Aメロは I → ♭VII → vi → iv（夜の色。E♭maj9・D♭maj9・Cm9・A♭m6）。サビは下がっていくベース（E♭→D→C→B♭→A♭）で、最後は A♭m6 で宙に浮いたまま終わる
#   音の世界（01 と同じ組み合わせにしない。01＝ファンクのギター・矩形波のプラックの駆け上がり・うねる和音）:
#     ガラスのエレピ（裏拍の短い和音）、のこぎり波の短い和音（サビ2 から）、明るいベル（ダイヤルの光）、電子のサックス（合いの手）、サブベース、
#     指パッチンと電子のクラップ、電波の雑音・上がる音・インパクト、テトの声のチョップ（ジングル）、AM ラジオの細い音（チューニングと CM）
#   この曲だけ: ①ラジオの中の細い音から本物の音に切りかわる出だし ②指パッチンだけの Aメロ ③AM ラジオの CM ④曲の終わりに初めて鳴る合いことばの節とスイッチの音
from vt25_lib import *

S = Song("02", "radio", "深夜ラジオのペンネーム（仮）", "Pen Name on Midnight Radio", 128, 4, "Eb", "major", "夜の2ステップ・エレクトロポップ（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --piano salamander --space room --space-wet 0.14"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.5
S.keepers = {"サビ2": "open", "最後のサビ": "ride"}
K = Key("Eb", "major")          # oct 4 で 1 = E♭4

A_CH = ["Ebmaj9", "Dbmaj9", "Cm9", "Abm6", "Ebmaj9", "Dbmaj9", "Cm9", "Bb7sus4"]
B_CH = ["Abmaj7", "Bb6", "Gm7", "Cm9", "Fm9", "Gm7", "Abmaj7", "Bb7sus4"]
C_CH = ["Ebmaj9", "Bb/D", "Cm9", "Bb6", "Abmaj9", "Gm7", "Fm9", "Bb7sus4", "Ebmaj9", "Bb/D", "Cm9", "Bb6", "Abmaj9", "G7", "Cm9", "Abm6"]

S.scene("チューニング", 8, "intro", ["Abmaj9", "Abmaj9", "Bb6", "Bb6", "Abmaj9", "Gm7", "Fm9", "Bb7sus4"])
S.scene("Aメロ1", 16, "verse", A_CH + A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("CM", 4, "break", ["Cm9", "Fm9", "Cm9", "Bb7sus4"])
S.scene("Aメロ2", 16, "verse", A_CH + A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("間奏", 8, "solo", C_CH[:8])
S.scene("DJの声", 8, "bridge", ["Cm9", "Abmaj7", "Fm9", "Gm7", "Cm9", "Abmaj7", "Dbmaj9", "Bb7sus4"])
S.scene("最後のサビ", 16, "chorus", C_CH)
S.scene("鼻歌", 6, "outro", ["Ebmaj9", "Abm6", "Ebmaj9", "Abm6", "Ebmaj9", "Ebmaj9"])

AM = [{"type": "filter", "kind": "highpass", "freq": 500, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 2600, "q": 0.9}]   # AM ラジオの細い音
V = Voice(S, vol=0.21, delay=0.75, bright=0.0, patch="kfbSineLead", low=False)
EP = [S.track(f"ガラスのエレピ{i + 1}", "keys", patch="kfbGlassEp", volume=0.07, pan=-0.3, reverb=0.28, sustain=0.9,
              fx=[{"type": "eq", "low": -2, "mid": 0, "midHz": 800, "high": 1}]) for i in range(4)]
RAD = [S.track(f"ラジオの中の音楽{i + 1}", "keys", patch="kfbGlassEp", volume=0.075, pan=0.0, reverb=0.1, sustain=0.6, fx=AM) for i in range(3)]
STAB = [S.track(f"のこぎり波の短い和音{i + 1}", "lead", patch="kfbSawStab", volume=0.036, pan=0.45 - 0.2 * i, reverb=0.2, duck=0.45,
                fx=[{"type": "filter", "kind": "highpass", "freq": 250, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 8000, "q": 0.6}]) for i in range(3)]
BELL = S.track("ダイヤルの光（明るいベル）", "lead", patch="kfbBrightBells", volume=0.04, pan=0.4, reverb=0.45,
               fx=[{"type": "filter", "kind": "lowpass", "freq": 7000, "q": 0.6}, {"type": "pingpong", "beats": 0.75, "mix": 0.14, "feedback": 0.25}])
SAX = S.track("電子のサックス（合いの手）", "lead", patch="kfbFutureSax", volume=0.085, pan=0.15, reverb=0.3)
STRL = S.track("弦の線", "strings", patch="stringEnsemble", volume=0.05, pan=0.3, reverb=0.4, sustain=1.2)
STRH = S.track("弦の高い線（最後のサビ）", "strings", patch="stringEnsemble", volume=0.035, pan=-0.3, reverb=0.45, sustain=1.3)
PADS = [S.track(f"夜の空気{i + 1}", "lead", patch="kfbSparklePad", volume=0.022, pan=-0.3 + 0.6 * i, reverb=0.4) for i in range(2)]
BASS = S.track("ベース（指弾き）", "bass", sustain=1.15, **finger_bass_spec(vol=0.21))
SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.032, pan=0, duck=0.5)
KFX = S.track("ラジオの効果音", "guitar", patch="kawaiiFx", volume=0.05, pan=0.1, reverb=0.15, modulate=False)
KDR = S.track("指パッチンと電子のクラップ", "guitar", patch="kawaiiFx", volume=0.07, pan=-0.05, reverb=0.1, modulate=False)
CMJ = S.track("CMの節（AMラジオ）", "lead", patch="kfbGlocken", volume=0.06, pan=0, reverb=0.1, fx=AM)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
# Aメロ: 低い所で話すように。拍の頭から入り、付点でひっかける。♭VII と iv の小節は、その和音に合う音だけ（1・2・4・5）
VA = ["1:0.5 1:0.5 2:0.5 3:1 R:0.5 3:0.5 2:0.5", "1:0.75 2:0.75 4:1.5 R:1",
      "R:1 3:0.5 5:0.5 5:1 3:0.5 2:0.5", "1:1 4:2 R:1",
      "3:0.5 3:0.5 5:0.5 6:1 R:0.5 6:0.5 5:0.5", "4:0.75 5:0.75 1':1.5 R:1",
      "R:1 5:0.5 7:0.5 1':1 7:0.5 5:0.5", "4:0.5 5:0.5 2:2 R:1"]
VA2 = ["5:0.5 5:0.5 6:0.5 1':1 R:0.5 7:0.5 5:0.5", "4:0.75 5:0.75 6:1.5 R:1",
       "R:1 5:0.5 7:0.5 1':1 7:0.5 5:0.5", "4:1 5:2 R:1",
       "3:0.5 3:0.5 5:0.5 6:1 R:0.5 6:0.5 5:0.5", "4:0.75 5:0.75 1':1.5 R:1",
       "R:1 5:0.5 7:0.5 1':1 7:0.5 5:0.5", "4:0.5 5:0.5 5:2 R:1"]
A1 = ("まくらもとのらじお/ごぜんいちじだ/ちいさくしぼったおと/かぞくにないしょで/"
      "やさしいわらいごえ/ひとりじゃないね/まどのそとはまっくら/ここだけあかるい")
# アルバムの考え（2026-11-12 人間）「物語は幸せで楽しいものに書き換えられる」: DJ が、悩みのおたよりを楽しく読んで、悲しい物語を幸せに書きかえる
A2 = ("つぎのおたよりはね/ぺんねーむから/ねむれないかもめって/わたしのなまえだ/"
      "なやみのおたよりを/たのしくよんだ/かなしいものがたり/しあわせにかえた")
# Bメロ: 長い音から始めて、折れながら上がる（胸が高鳴る）。最後は高い所で止まる
VB = ["1':2 1':0.5 7:0.5 1':1", "2':1 7:0.5 5:0.5 6:1 R:1", "7:2 7:0.5 6:0.5 7:1", "1':1 5:0.5 3:0.5 5:1 R:1",
      "6:1 1':1 2':1 1':1", "2':1.5 1':0.5 7:0.5 5:0.5 R:1", "R:0.5 5:0.5 6:0.5 1':0.5 2':1 1':1", "2':1 2':1 1':1 R:1"]
B1 = "かばんのそこにね/ねむっていたはがき/だれにもいえない/きもちをかいたの"
B2 = "ほんとうのなまえ/かくしたままでも/とどくことがある/よるのなみにのり"
# サビ: ペンネームを呼ぶ（「ねむれ・なーい・かもめー」）。2回目は上の高さで。後半は「3・3・2」で押して、最後は宙に浮いて終わる
VC = ["3:0.5 5:0.5 5:0.5 1':1.5 7:1", "5:0.5 6:0.5 5:2 R:1",
      "R:1 3:0.5 5:0.5 1':1 7:1", "6:0.5 5:0.5 2:2 R:1",
      "5:0.5 6:0.5 6:0.5 2':1.5 1':1", "7:0.5 1':0.5 7:2 R:1",
      "R:1 6:0.5 1':0.5 2':1 1':1", "6:0.5 5:0.5 5:2 R:1",
      "1':0.75 1':0.75 2':0.5 1':0.5 7:0.5 5:1", "7:0.75 1':0.75 2':1.5 R:1",
      "R:0.5 5:0.5 1':0.5 5:0.5 3:0.5 5:0.5 7:1", "6:1 5:2 R:1",
      "1':1 1':0.5 2':0.5 1':1 7:1", "7:1.5 2':1.5 R:1",
      "R:1 5:1 1':1 2':1", "1':3 R:1"]
C1 = ("ねむれないかもめ/よるをわたるよ/ねむれないかもめ/だれかのまどへ/"
      "まよなかのらじおは/ちいさなとうだい/ひとりじゃないって/ひかってる")
C2 = ("ねむれないかもめ/よばれたなまえ/ねむれないかもめ/なみだがおちた/"
      "ないしょのままでいい/やさしいそのこえ/とべるきがした/わらってる")
C3 = ("ねむれないかもめ/はなうたひろう/ねむれないかもめ/いつつのおとを/"
      "まよなかのらじおが/あしたのまちへと/ふしをつないで/とんでく")
# DJ の声: ほとんど同じ高さでつぶやく
VBR = ["R:2 3:0.5 3:0.5 2:0.5 3:0.5", "5:3 R:1", "R:2 4:0.5 4:0.5 3:0.5 4:0.5", "7:3 R:1",
       "R:1.5 5:0.5 5:0.5 6:0.5 7:1", "1':3 R:1", "R:1 1':1 6:0.5 4:0.5 6:1", "5:1 5:2 R:1"]
CB = "だいじょうぶ/あさはくる/そのまえに/ちょっとうたおう"
HUM = ["R:2 3:0.5 5:0.5 6:1", "5:0.5 2:1.5 R:2", "R:2 3:0.5 5:0.5 6:1", "5:0.5 2:3.5", "R:4", "R:4"]   # 合いことばの節（3・5・6・5・2）
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
put("DJの声", VBR, CB)
put("最後のサビ", VC, C3)
if VOCAL: put("鼻歌", HUM, "ららららら/ららららら")
else:
    for b, l in zip(S.sc("鼻歌"), HUM): SAX.bar(b, K.mel(l, oct=4))

# ================= 和音と線 =================
root = lambda b: S.chords[b].split("|")[0].split("/")[0]


def ep(b, pat, c=63):
    v = voice(root(b), c, 4)
    for j in range(4): EP[j].bar(b, " ".join(t.replace("x", nm(v[j])) for t in pat.split()))


def stab(b, pat, c=70):
    v = voice(root(b), c, 3)
    for j in range(3): STAB[j].bar(b, " ".join(t.replace("x", nm(v[j])) for t in pat.split()))


def top(b, lo, hi, k=-1): return nm(tones(root(b), lo, hi)[k])


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "チューニング":
        if i < 4:                                             # ラジオの中の細い音（つまみを回している）
            v = voice(root(b), 66, 3)
            for j in range(3): RAD[j].bar(b, f"R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5 R:1 {nm(v[j])}:1")
        else:                                                 # 電波が合う → 本物の音に切りかわる（3・3・2 の和音）
            ep(b, "x:0.75 x:0.75 R:0.5 x:0.5 R:0.5 x:1" if i < 7 else "x:1 x:1 x:1 R:1"); SUB.bar(b, f"{nm(low(S.chords[b], 'E1'))}:3.5 R:0.5")
        BELL.bar(b, ["R:3 G5:1", "R:4", "R:2 Bb5:1 C6:1", "R:4", "R:3 Bb5:0.5 Eb6:0.5", "R:4", "R:2 C6:0.5 Ab5:0.5 F5:1", "R:4"][i])
    elif n == "Aメロ1":
        if i < 8:                                             # 前半: 2拍目の裏に1回だけ。4小節ごとに下からそっと分散
            ep(b, "R:1.5 x:0.5 R:2" if i % 4 != 3 else "R:1.5 x:0.5 R:1 x:1")
        else:                                                 # 後半: 裏拍の短い和音が増える。ベルが2小節に1回、高い所でぽつん
            ep(b, "R:0.5 x:0.5 R:1 x:0.5 R:0.5 x:1" if i % 2 == 0 else "R:0.5 x:0.5 R:1.5 x:0.5 R:0.5 x:0.5")
            if i % 2 == 1: BELL.bar(b, f"R:3 {top(b, 'C5', 'C6', -2)}:0.5 {top(b, 'C5', 'C6')}:0.5")
    elif n == "Aメロ2":                                         # 2番はノリを止めない。エレピは3・3・2、合いの手は声のチョップ（歌の版）とベル
        ep(b, "x:0.75 x:0.75 R:0.5 x:0.5 R:0.5 x:1" if i % 2 == 0 else "R:0.5 x:0.5 R:1 x:0.75 x:0.75 R:0.5")
        if i in (1, 5, 9, 13): BELL.bar(b, f"R:3 {top(b, 'C5', 'C6')}:0.5 {top(b, 'C5', 'C6', -2)}:0.5")
        if i >= 8 and i % 2 == 0: stab(b, "R:1.5 x:0.5 R:2")          # 後半（物語が書きかわる）: のこぎり波がそっと入る
    elif n in ("Bメロ1", "Bメロ2"):                               # のばす和音の上を、弦の1本の線が折れながら上がる（2番は1オクターブ上）
        ep(b, "x:4" if i < 6 else ("x:2 x:2" if i == 6 else "x:1 x:1 x:1 R:1"), 63 + i)
        tn = tones(root(b), "G4", "G6"); a_ = min(tn, key=lambda m: abs(m - (70 + 1.6 * i + (12 if n == "Bメロ2" else 0)))); b_ = next((m for m in tn if m > a_), a_)
        STRL.bar(b, f"{nm(a_)}:3 {nm(b_)}:1" if i < 7 else f"{nm(a_)}:2 {nm(b_)}:1 R:1")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        ep(b, "x:0.75 x:0.75 R:0.5 x:0.5 R:0.5 x:1" if i % 4 != 3 else "x:0.75 x:0.75 R:0.5 x:0.5 x:0.5 x:1", 65)
        if n != "サビ1": stab(b, "R:0.5 x:0.5 R:1 x:0.5 R:0.5 x:0.5 R:0.5" if i % 2 == 0 else "R:1 x:0.5 R:0.5 x:0.75 x:0.75 R:0.5")   # のこぎり波は サビ2 から
        # 合いの手（歌が休む4拍目）: サビ1＝ベル、サビ2＝電子のサックスとベルが交代、最後のサビ＝ベルが8分で駆ける＋サックス
        if i % 2 == 1:
            tn = tones(root(b), "Bb4", "Eb6")
            if n == "サビ1" or (n == "サビ2" and i % 4 == 1): BELL.bar(b, f"R:3 {nm(tn[-1])}:0.5 {nm(tn[-2])}:0.5")
            elif n == "サビ2": SAX.bar(b, f"R:2.5 {nm(tn[1])}:0.5 {nm(tn[3])}:0.5 {nm(tn[2])}:0.5")
            else: SAX.bar(b, f"R:2.5 {nm(tn[2])}:0.5 {nm(tn[3])}:0.5 {nm(tn[1])}:0.5" if i % 4 == 3 else f"R:3 {nm(tn[1])}:0.5 {nm(tn[2])}:0.5")
        if n == "最後のサビ":
            if i % 2 == 0:
                tb = tones(root(b), "Bb4", "F6"); BELL.bar(b, " ".join(f"{nm(tb[q % len(tb)])}:0.5" for q in (0, 2, 4, 3, 5, 4, 2, 3)))
            STRH.bar(b, f"{top(b, 'Bb5', 'Bb6')}:4")
    elif n == "間奏":                                           # 歌のかわりに電子のサックスがペンネームの節を吹き、ベルが8分で駆ける。後半は上の高さで
        ep(b, "x:0.75 x:0.75 R:0.5 x:0.5 R:0.5 x:1", 65); stab(b, "R:0.5 x:0.5 R:1 x:0.5 R:0.5 x:0.5 R:0.5" if i % 2 == 0 else "R:1 x:0.5 R:0.5 x:0.75 x:0.75 R:0.5")
        SAX.bar(b, K.mel(VC[i], oct=4 if i < 4 else 4))
        if i % 2 == 1:
            tb = tones(root(b), "Bb4", "F6"); BELL.bar(b, "R:2 " + " ".join(f"{nm(tb[q % len(tb)])}:0.25" for q in (0, 2, 4, 2, 5, 4, 6, 4)))
    elif n == "CM":                                            # AM ラジオの細い音の、短い CM の節
        v = voice(root(b), 64, 3)
        for j in range(3): RAD[j].bar(b, f"R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5")
        CMJ.bar(b, ["G5:0.5 Eb5:0.5 G5:0.5 C6:1 Bb5:0.5 G5:1", "Ab5:0.5 F5:0.5 Ab5:0.5 C6:1 Ab5:0.5 F5:1", "G5:0.5 Eb5:0.5 G5:0.5 C6:1 Bb5:0.5 G5:1", "F5:0.5 Ab5:0.5 Bb5:1 R:2"][i])
    elif n == "DJの声":                                         # 半分の速さ。エレピの長い和音と、夜の空気だけ
        ep(b, "x:4")
        v = voice(root(b), 72, 3)
        for j in range(2): PADS[j].bar(b, f"{nm(v[j + 1])}:4")
        if i % 2 == 0: BELL.bar(b, f"R:2 {top(b, 'C6', 'G6')}:2")
    elif n == "鼻歌":
        if i < 5:
            ep(b, "x:4"); v = voice(root(b), 72, 3)
            for j in range(2): PADS[j].bar(b, f"{nm(v[j + 1])}:4")
        else:
            ep(b, "x:2 R:2")

# ================= ベース（この曲のために書く。共通の部品 bass_line は使わない）=================
def bl(b, style):
    ch = S.chords[b]; r = low(ch, "E1"); nx = S.chords[b + 1] if b + 1 < S.nb else ch; rn = low(nx, "E1")
    up = tones(root(b), nm(r + 1), nm(r + 12))
    t3 = next((m for m in up if (m - r) in (3, 4)), r + 7); t5 = next((m for m in up if (m - r) in (6, 7, 8)), r + 7); t7 = next((m for m in up if (m - r) in (9, 10, 11)), r + 12)
    o = r + 12; ap = t5 if rn == r else (rn - 1 if rn > r else rn + 1)
    N = nm
    return {"long": f"{N(r)}:4",
            "hold": f"{N(r)}:2.5 R:0.5 {N(o)}:0.5 {N(t5)}:0.5",                       # Aメロ1 前半: のばして、最後にオクターブ上をちょん
            "skip_a": f"{N(r)}:1 R:0.75 {N(r)}:0.25 R:0.5 {N(o)}:0.5 R:0.5 {N(ap)}:0.5",    # 2ステップのキックに合わせて跳ねる
            "skip_b": f"{N(r)}:0.75 {N(t5)}:0.75 R:0.5 {N(o)}:0.5 {N(t7)}:0.5 R:0.5 {N(ap)}:0.5",
            "four": f"{N(r)}:1 {N(r)}:1 {N(r)}:1 {N(t5)}:0.5 {N(ap)}:0.5",                # Bメロ: 4つ打ちに合わせて押す
            "four_up": f"{N(r)}:1 {N(t3)}:1 {N(t5)}:1 {N(t7)}:0.5 {N(ap)}:0.5",
            "stop": f"{N(r)}:1 {N(r)}:1 {N(t5)}:1 R:1",
            "cho_a": f"{N(r)}:0.75 {N(r)}:0.75 R:0.5 {N(o)}:0.5 R:0.5 {N(t5)}:0.5 {N(ap)}:0.5",   # サビ: 3・3・2 で和音と同じ所を踏む
            "cho_b": f"{N(r)}:0.75 {N(r)}:0.25 R:0.5 {N(t3)}:0.5 {N(t5)}:0.75 {N(t5)}:0.25 {N(t7)}:0.5 {N(o)}:0.5",
            "run": f"{N(r)}:0.5 {N(t3)}:0.5 {N(t5)}:0.5 {N(t7)}:0.5 {N(o)}:0.5 {N(t7)}:0.5 {N(t5)}:0.5 {N(ap)}:0.5",
            "drive": f"{N(r)}:0.75 {N(r)}:0.75 {N(o)}:0.5 {N(r)}:0.25 {N(t5)}:0.25 R:0.25 {N(t5)}:0.25 {N(t7)}:0.5 {N(ap)}:0.5"}[style]


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "チューニング" and i >= 4: BASS.bar(b, bl(b, "stop" if i == 7 else ("cho_a" if i % 2 == 0 else "cho_b")))
    elif n == "間奏": BASS.bar(b, bl(b, "run" if i == 7 else ("drive" if i % 2 == 0 else "cho_b")))
    elif n == "Aメロ1": BASS.bar(b, bl(b, "hold" if i < 8 else ("run" if i == 15 else ("skip_a" if i % 2 == 0 else "skip_b"))))
    elif n == "Aメロ2": BASS.bar(b, bl(b, "run" if i % 8 == 7 else ("skip_b" if i % 2 == 0 else "skip_a")))
    elif n in ("Bメロ1", "Bメロ2"): BASS.bar(b, bl(b, "stop" if i == L - 1 else ("four" if i < 4 else "four_up")))
    elif n == "サビ1": BASS.bar(b, bl(b, "run" if i % 8 == 7 else ("cho_a" if i % 2 == 0 else "cho_b")))
    elif n == "サビ2": BASS.bar(b, bl(b, "run" if i % 4 == 3 else ("cho_a" if i % 2 == 0 else "cho_b")))
    elif n == "最後のサビ": BASS.bar(b, bl(b, "run" if i % 4 == 3 else ("drive" if i % 2 == 0 else "cho_b")))
    elif n == "DJの声" and i >= 4: BASS.bar(b, bl(b, "long" if i < 7 else "four_up"))
    elif n == "鼻歌" and i < 5: BASS.bar(b, bl(b, "long"))
    # サブベース（深さ）: サビ1 は後半から、サビ2 と最後のサビは頭から。DJ の声は最初の4小節、サブベースだけが下で鳴る
    if (n == "サビ1" and i >= 8) or n in ("サビ2", "最後のサビ", "間奏"): SUB.bar(b, f"{nm(low(S.chords[b], 'E1'))}:2.5 R:0.5 {nm(low(S.chords[b], 'E1'))}:1" if i % 2 == 0 else f"{nm(low(S.chords[b], 'E1'))}:3.5 R:0.5")
    elif n == "DJの声" and i < 4: SUB.bar(b, f"{nm(low(S.chords[b], 'E1'))}:4")

# ================= ドラム（2ステップ）・指パッチン・クラップ・効果音 =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "チューニング":
        if i >= 4:
            D.set(b, "X.....x...X....." if i % 2 == 0 else "X..x......X..x..", "....x.......x...", "x.x.x.xxx.x.x.x.")
            KDR.bar(b, "R:1 C5:1 R:1 C5:1")
        if i == 3: put_fill(D, b, "small")
        if i == 7: halt(D, b, 3)
    elif n == "Aメロ1":
        if i < 8: D.set(b, "X.........x....." if i % 2 == 0 else "X......x..x.....", "................", "................")           # キックと指パッチンだけ
        else: D.set(b, "X.........x....." if i % 2 == 0 else "X......x..x..x..", "................", "..x...x...x...x." if i % 4 != 3 else "..x...x...x.x.xx")
        KDR.bar(b, "R:1 C5:1 R:1 C5:1" if not (i >= 8 and i % 4 == 3) else "R:1 C5:1 R:1 C5:0.5 C5:0.5")
        if last: put_fill(D, b, "small")
    elif n == "Aメロ2":                                         # 2番は2ステップのまま（スネアは縁、ハイハットは細かく）
        vgroove(D, b, "beat8", ghosts=0.3, seed=b, k="X.....x...X....." if i % 2 == 0 else "X..x......X..x..", s="....x.......x...", h="x.x.x.xxx.x.x.x.")
        KDR.bar(b, "R:1 C5:1 R:1 C5:1" if i < 8 else "R:1 C5:0.75 C#6:0.25 R:1 C5:1")      # 後半は縁をたたく音が16分の裏に
        if last: put_fill(D, b, "snare16")
    elif n in ("Bメロ1", "Bメロ2"):                               # 4つ打ちでのぼる → 最後の1拍は全員止まる
        D.set(b, "X...X...X...X...", "................" if i < 4 else ("........X......." if i < 6 else ("....X.......X..." if i == 6 else "X.X.X.X.XXXX....")),
              "..x...x...x...x." if i < 4 else "x.x.x.x.x.x.x.x.")
        KDR.bar(b, "R:1 B4:1 R:1 B4:1" if i < 6 else ("R:1 B4:1 R:1 B4:0.5 B4:0.5" if i == 6 else "B4:0.5 B4:0.5 B4:0.5 B4:0.5 D5:0.25 D5:0.25 D5:0.25 D5:0.25 R:1"))
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        kp = ["X.....x...X.....", "X..x......X..x..", "X.....x...X...x.", "X..x..x...X....."][i % 4]
        vgroove(D, b, "beat8", ghosts=0.3 if n != "最後のサビ" else 0.4, seed=b, k=kp, s="....X.......X..." if i % 4 != 3 else "....X.......X..x", h="x.x.x.xxx.x.x.xx" if i % 2 == 0 else "x.xxx.x.x.x.xxx.")
        if i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
        if i % 8 == 7 and not last: put_fill(D, b, "small" if n == "サビ1" else "tomtrip")
        if last and n != "最後のサビ": put_fill(D, b, "snare16")
        if n != "サビ1" or i >= 8: KDR.bar(b, ("R:1 B4:0.75 C#6:0.25 R:1 B4:1" if i % 4 == 1 else "R:1 B4:1 R:1 B4:1") if i % 4 != 3 else "R:1 B4:1 R:1 B4:0.5 D5:0.25 D5:0.25")    # 電子のクラップを重ねる
    elif n == "間奏":
        kp = ["X.....x...X.....", "X..x......X..x..", "X.....x...X...x.", "X..x..x...X....."][i % 4]
        vgroove(D, b, "beat8", ghosts=0.35, seed=b, k=kp, s="....X.......X...", h="x.x.x.xxx.x.x.xx" if i % 2 == 0 else "x.xxx.x.x.x.xxx.")
        if i == 0: crash(D, b)
        KDR.bar(b, "R:1 B4:1 R:1 B4:1" if i % 4 != 3 else "R:1 B4:1 R:0.5 D5:0.25 D5:0.25 B4:0.5 D5:0.25 D5:0.25")
        if last: halt(D, b, 1)
    elif n == "CM":
        D.set(b, "................", "................", "x.x.x.x.x.x.x.x.")
        if last: put_fill(D, b, "small")
    elif n == "DJの声":                                         # 半分の速さ → 最後の2小節でのぼる
        if i < 4: D.set(b, "................", "................", "................")
        elif i < 6: D.set(b, "X...............", "........X.......", "x...x...x...x...")
        elif i == 6: D.set(b, "X.......X.......", "....X...X.X.X.X.", "x.x.x.x.x.x.x.x.")
        else: D.set(b, "X...X...X.X.X.X.", "X.X.X.X.XXXXXXXX", "................")
        if 4 <= i < 6: KDR.bar(b, "R:2 C5:1 R:1")
    elif n == "鼻歌":
        if i == 0: crash(D, b, "C2", 6)
        if i < 4: D.set(b, "X.........x.....", "................", "................"); KDR.bar(b, "R:1 C5:1 R:1 C5:1")

# 効果音: 電波の雑音（チューニング・CM・終わり）、上がる音、インパクト、きらきら、サブドロップ、スイッチを切る音
for b in S.sc("チューニング")[:4] + S.sc("CM"): KFX.bar(b, "A#5:4")
KFX.bar(S.sc("チューニング")[3], "A#5:2 F#4:2"); KFX.bar(S.sc("チューニング")[4], "G5:2 R:2"); KFX.bar(S.sc("間奏")[0], "D4:2 R:2")
for nme in ("Bメロ1", "Bメロ2"): KFX.bar(S.sc(nme)[-2], "R:2 F#4:2")
KFX.bar(S.sc("サビ1")[0], "D4:2 R:2"); KFX.bar(S.sc("サビ2")[0], "G5:2 R:2"); KFX.bar(S.sc("最後のサビ")[0], "G5:2 D#4:2")
KFX.bar(S.sc("DJの声")[0], "G#5:3 R:1"); KFX.bar(S.sc("DJの声")[-1], "R:2 F#4:2")
KFX.bar(S.sc("鼻歌")[4], "A#5:4"); KFX.bar(S.sc("鼻歌")[5], "A#5:2 E4:0.5 R:1.5")
cym_swell(CYM, S.sc("サビ1")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 4, "E4")

# 止め: Bメロ の最後の1拍だけ全員休み（サビの頭を大きく聞かせる）
for nme in ("Bメロ1", "Bメロ2", "チューニング"): SIL.add(S.sc(nme)[-1], 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の02（1時）。夜の2ステップ・エレクトロポップ。E♭・128。深夜ラジオで、ペンネーム「ねむれないかもめ」のはがきが読まれる。"
          "DJ が口ずさむ5つの音の鼻歌（合いことばの節）が、ここで生まれる。ガラスのエレピ・明るいベル・電子のサックス・サブベース・指パッチン・AM ラジオの音。自作")
finish(S, LY, V, 0,
       level={"verse": -0.25}, special={"CM": -0.6, "DJの声": -0.6, "間奏": 0.1, "最後のサビ": 0.4, "鼻歌": -0.35})

# ================= 仕上げのあとに足すもの =================
from vt3x_lib import *
path = sys.argv[1]
# ギター: サビだけ。右に丸いクリーンのカッティング（高い4本の弦・消す音入り）。サビ1 は後半から入る（色が1つ増える）
GR = GuitarRig(S, "Rギター（カッティング）", "city_cut", 0.55, 0.05, style="funk_slow", seed=11)
prev = None
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    v = sorted(voice(root(b), 67, 4, prev)); prev = v; vo = [None, None] + [nm(x) for x in v]
    if (n == "サビ1" and i >= 8) or n in ("サビ2", "最後のサビ", "間奏"): GR.bar(b, "d..Ux.dU.xd.x.dU" if i % 4 != 3 else "d.xUx.dUd.xUD.dU", vo, vel=0.92 if n != "最後のサビ" else 1.02)
    else: GR.stop(b)
add_parts(path, GR.parts())
# 2ステップの決まり（2026-11-12 に調べた。MusicRadar・BeatsToRapOn の作り方）: テンポ 125〜138（典型は 130 前後）、キックは1拍目と3拍目の裏、
#   クラップは2・4拍、ハイハットは裏拍で16分をはねさせる（キックはまっすぐ、ハットだけ揺らす）、ベースはキックのあいた所に答える、声のチョップを裏拍に置く。
#   → テンポを 122 から 128 に、ハイハットと指パッチン・クラップだけ16分をはねさせる（キック・ベースはまっすぐ）
set_parts(path, "ハイハット", swing16=0.3); set_parts(path, "ライド", swing16=0.3); set_parts(path, "指パッチン", swing16=0.22)
humanize(path, "ガラスのエレピ"); humanize(path, "弦", mid=78, down=8, up=8, seed=9)
# 測ると、最後のサビ（−14.2）が サビ2（−13.9）より小さかった → 仕上げで山を最後にする
final_gain(path, {"チューニング": 1.5, "サビ2": -0.3, "間奏": -0.6, "最後のサビ": 1.3})
if VOCAL:
    remark(path, S, std_mark(("chorus",), plain=("鼻歌",)))
    vocal_polish(path, S, {"verse": 8, "pre": 16, "chorus": 24, "最後のサビ": 28, "bridge": 8, "outro": 6}, scoop=0.3, slash=0.7, vib_min_beats=1.5, vib_start=0.5, auto=0.6, breaths=0.6)
    harmony(path, S, [("サビ2", 8, None, K), ("最後のサビ", 0, None, K)], vol=0.36)
    # 声のチョップ: チューニングで、ラジオのジングルのようにテトの声を短く切って鳴らす。Aメロ2 では歌の合間に答える
    t0 = S.sc("チューニング")[0]; a2 = S.sc("Aメロ2")
    im = S.sc("間奏")
    chops(path, S, {t0 + 4: "G4:0.5:ら R:0.5 Bb4:0.5:ら R:0.5 Eb5:1:ら R:1", t0 + 6: "C5:0.5:ら R:0.25 C5:0.25:ら Ab4:1:ら R:2",
                    im[1]: "R:3 Bb4:0.5:や D5:0.5:や", im[3]: "R:3 F4:0.25:は F4:0.25:は Bb4:0.5:や", im[5]: "R:3 D5:0.5:や Bb4:0.5:や", im[7]: "R:1 Bb4:0.5:ら Eb5:0.5:ら F5:1:や R:1",
                    a2[1]: "R:3 F4:0.5:は Ab4:0.5:は", a2[5]: "R:3 Ab4:0.5:は Eb5:0.5:や"}, vol=0.3, pan=0.25)
    voice_by_scene(path, S, {"verse": "whisper", "pre": "clear", "chorus": "clear", "bridge": "whisper", "outro": "whisper"}, default="clear")
