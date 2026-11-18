# vt3 18「夕焼けの交代式」Changing of the Sunset Guard（仮）— ケルトのゆっくりの歌（4分の3・84）。D長調 → 受け渡しのあと E。
# 第3弾（0時〜24時の街）の 17時。表は docs/sound/vt3-plan.md。
#
# v3（2026-11-18）: ゼロから作り直し。v1・v2 はゴスペル（オルガンと聖歌隊）だった。
#   人間の指示: 11 から「ケルトで作り直す・構成を今までと変える」（2026-11-15）、「16.17 特徴なさすぎて」（2026-11-18）→「音の地図」のはしに置いて作る（2026-11-18「良い。18行こう」）。
#
# 音の地図の場所（docs/design/song-analyzer-plan.md）: 左下のはし。電子の音もドラムセットも歪みも使わない。ハープ・チェロ・フィドル・わく太鼓・声。
#   16・17 は地図の真ん中（横 −0.06・+0.07、縦 0.46・0.37）だった。この曲は「生の楽器だけ・軽い」に寄せきる。
#
# 物語: 夕方5時。一日じゅう空を守った「ひるの番人」が、金色のはしごをおりて息をつく。東から、ねぼけた「銀のくつ」の番人が少し遅れてやって来る。
#   光のかぎを手わたすと、町の窓にひとつずつ火がともる。やりのこした事は、星にして飾る。
#   アルバムの考え「幸せで美しい物語に書き換えて行く」は、言葉でなく景色で: やりのこした事 → 星。ひとりの帰り道 → 町じゅうの窓から同じ歌。
#   太陽・月という言葉は使わない（番人・銀のくつ・光のかぎ）。
#
# 曲を決める表:
#   形: Aメロ・Bメロ・サビの形は使わない。4小節で1行の歌。1行歌うごとに、楽器が1つ「またあした」の節（合いことばの節 3・5・6・5・2）をあいさつに弾いて入ってくる。
#       前奏（ハープ1本）→ 太陽の歌1（声とハープ → チェロ → フィドル → アコーディオン → わく太鼓）→ くり返し1 →
#       太陽の歌2（→ ウッドベース → 高いピアノ → 弦）→ くり返し2（→ 声の重ね）→ 受け渡し（フィドルが歌の節をひとりで弾き、E に上がってハープとピアノが受けとる）→
#       月の歌・月の歌2（楽器が1行ずつ、あいさつの節を順に回す。後半でわく太鼓とベースが歩き出す）→ くり返し3（全員・いちばん大きい）→ おわり（声とハープ → ハープだけ → 高いピアノの一番星）
#   場面と強さ: 前奏 弱（小さすぎない）／太陽の歌1 弱 → 中弱／くり返し1 中／太陽の歌2 中 → 中強／くり返し2 中強／受け渡し 弱（フィドル1本）→ 中／月の歌 中（透きとおる）／くり返し3 強／おわり 弱
#   旋律: 3拍子のゆっくりした歌。となりの音へ進む動きが中心で、行の終わりは長い音。1行め「きんいろのはしごを」は、はしごのように下から上へのぼる。2行め「おりる」は上からおりる。
#       歌の最高音はシ4（71）まで。いちばん高い音（ミ5・最後はファ#5）は、くり返しの「またあした」のためにとっておく。
#   和音: D・G・A・Bm・Em だけ。太陽の歌の間は、チェロがずっとレの音をのばす（夕焼けの空の色）。月の歌では E の音をのばす。
#   ベース: ウッドベースは太陽の歌2 から。付点2分の根音と、3拍めの5度。
#   ドラム: ドラムセットは使わない。わく太鼓（バウロンの役の低い太鼓）だけ。入り方は「鳴っている所へ、ロールでそっと足される」。
#   この曲だけ: ①楽器が1行ごとに「またあした」とあいさつして入ってくる（交代式）②「またあした」の5文字が、アルバムの合いことばの節そのもの
#              ③受け渡しで、歌の節をフィドル（ひる）からハープとピアノ（よる）へ手わたす ④ドラムセットも電子の音もない
#   声: クリア 1 種類で最後まで。
#   ほかの曲とのちがい: 11（ケルトのジグ・8分の6・速い・踊り）と楽器は近いが、こちらは 3拍子のゆっくりの歌で、踊りの曲がなく、楽器が1つずつ増える。08（3拍子のワルツ・156）とは速さと楽器がちがう。
from vt25_lib import *

S = Song("18", "sunset", "夕焼けの交代式（仮）", "Changing of the Sunset Guard", 84, 3, "D", "major", "ケルトのゆっくりの歌（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --piano salamander --space dome --space-wet 0.26"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.keepers = {}
K = Key("D", "major")          # oct 4 で 1 = D4
KE = Key("E", "major")
up2 = lambda L: [tr_chord(c, 2) for c in L]

V1_CH = ["D", "D", "G", "D", "G", "D", "A", "Bm", "D", "D", "A", "G", "D", "Em", "A", "D"]
V2_CH = ["D", "D", "G", "A", "Bm", "G", "D", "A", "D", "D", "G", "D", "G", "D", "A", "D"]
R_CH = ["D", "A", "A", "Bm", "G", "D", "Em", "A"]            # さいごは A で止まる（つづく感じ）
R2_CH = ["D", "A", "A", "Bm", "G", "D", "A", "D"]           # さいごは D に帰る

S.scene("前奏", 4, "intro", ["D", "A", "D", "A"])
S.scene("太陽の歌1", 16, "verse", V1_CH)
S.scene("くり返し1", 8, "chorus", R_CH)
S.scene("太陽の歌2", 16, "verse", V2_CH)
S.scene("くり返し2", 8, "chorus", R2_CH)
S.scene("受け渡し", 8, "solo", ["D", "D", "G", "B7", "E", "E", "A", "B"])
S.scene("月の歌", 16, "bridge", up2(V2_CH))
S.scene("月の歌2", 16, "verse", up2(V1_CH))
S.scene("くり返し3", 16, "chorus", up2(R_CH + R2_CH))
S.scene("おわり", 8, "outro", up2(["D", "A", "D", "D", "D", "A", "D", "D"]))

V = Voice(S, vol=0.2, delay=0.3, bright=0.0, patch="kfbSineLead", low=False)
D = S.drumkit()

# ================= 歌（1小節＝3拍）=================
# リズムの形: 3拍子のゆっくりした歌の「ゆれ」（付点4分＋8分、行の終わりの手前で 8分のひろい）。小節ごとに同じ形をくり返さない
L1 = ["5,:1.5 1:0.5 2:1", "3:2.5 2:0.5", "1:1 2:0.5 3:1.5", "5:2.5 R:0.5"]          # はしごをのぼる
L2 = ["6:1.5 5:1.5", "3:0.5 2:0.5 1:2", "2:2.5 1:0.5", "6,:2 R:1"]                  # おりる
L3 = ["1:1 2:1.5 3:0.5", "5:2 3:1", "2:0.5 3:0.5 5:2", "6:2.5 R:0.5"]
L4 = ["5:2.5 3:0.5", "2:1.5 1:0.5 2:1", "3:1.5 2:1.5", "1:2 R:1"]
L5 = ["1:1.5 2:0.5 3:1", "5:1.5 5:1.5", "6:1 5:1.5 3:0.5", "2:2.5 R:0.5"]
L6 = ["3:2.5 5:0.5", "6:0.5 5:0.5 3:2", "1:1.5 2:1.5", "2:2 R:1"]
L7 = ["5,:1 1:0.5 2:1.5", "3:2.5 5:0.5", "6:1.5 5:0.5 3:1", "5:2.5 R:0.5"]
L8 = ["6:1.5 5:1.5", "3:1 2:1.5 1:0.5", "2:2.5 7,:0.5", "1:2 R:1"]
VA = L1 + L2 + L3 + L4; VB = L5 + L6 + L7 + L8
T1 = "きんいろのはしごを/ばんにんがおりる/かたのにをおろして/ふかいいきひとつ"
T2 = "ひがしからねぼけた/ぎんのくつならし/ひかりのかぎわたす/まどにひがともる"
T3 = "やりのこしたことは/ほしにしてかざる/まちじゅうのまどから/おなじうたながれ"
T4 = "ひとりのかえりみち/あかりがならぶよ/ぎんのくつがそらを/しずかにわたるよ"
# くり返し: 「またあした」（5文字）＝ 合いことばの節 3・5・6・5・2
HOOK = ["3:1.5 5:0.5 6:1", "5:1.5 2:1 R:0.5"]
HOOK_UP = ["5:1.5 1':0.5 2':1", "1':1.5 5:1 R:0.5"]                     # 上で答える（ミ5 まで。ここだけの高さ）
RA = HOOK + ["2:0.5 3:0.5 5:2", "6:1 5:0.5 3:1 R:0.5"] + HOOK_UP + ["3:1 2:0.5 1:1.5", "2:2.5 R:0.5"]
RB = HOOK + ["2:0.5 3:0.5 5:2", "6:1 5:0.5 3:1 R:0.5"] + HOOK_UP + ["3:1 2:0.5 7,:1.5", "1:2.5 R:0.5"]
RC = HOOK_UP + ["6:0.5 1':0.5 2':2", "1':1 6:0.5 5:1 R:0.5"] + HOOK_UP + ["2':1 1':0.5 6:1.5", "1':2.5 R:0.5"]
TR1 = "またあした/あとをたのむ/またあした/よぞらを"
TR2 = "またあした/まかされたよ/またあした/おやすみ"
TR3 = "またあした/そらはつづく/またあした/おやすみ/またあした/あさがくるよ/またあした/かならず"
LY = Lyrics(S)


def put(name, lines, text, key=K, o=4, bars=None):
    bars = bars or S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("太陽の歌1", VA, T1); put("くり返し1", RA, TR1)
put("太陽の歌2", VB, T2); put("くり返し2", RB, TR2)
put("月の歌", VB, T3, key=KE); put("月の歌2", VA, T4, key=KE); put("くり返し3", RA + RC, TR3, key=KE)
put("おわり", HOOK, "またあした", key=KE, bars=S.sc("おわり")[:2])

# ================= 楽器（音量は最初から最後まで同じ。仕上げで持ち上げない）=================
# v3 のはじめの書き出しを、曲から分けて測った（月の歌）: 歌 −25.7・ウッドベース −16.9・弦とチェロとフィドル −26.6・ハープ −34〜−52・ピアノ −37。
#   2 回めの書き出し（tools/vt3/part_balance.py）: 月の歌で歌が伴奏より 5〜6dB 小さい（弦とチェロが大きい）・前奏のハープ −33dB・くり返し3 が月の歌2 より小さい。
#   → ハープ 1.5、弦 0.028、チェロ 0.09、ベース 0.045。くり返し3 にハープ（節）とアコーディオンを足す。おわりのフィドルをやめる
#   3 回め: ハープの volume を 1.5 にしても前奏は −34dB のままだった（パートの volume は 0.5 までしか効かない）。→ volume 0.5 ＋ fx の boost（+9dB）で上げる
#   ベースが歌より 9dB 大きく、ハープはほとんど聞こえず、前奏（ハープ1本）は −38dB だった。→ ベース 0.2 → 0.06、ハープ 0.2 → 0.62、ピアノ・わく太鼓を少し上げ、弦とチェロを少し下げた
HARP = S.track("ハープ（分散和音）", "harp", patch="folkHarp", recipe="celtic-harp", volume=0.5, pan=-0.12, reverb=0.4, sustain=1.7, fx=[{"type": "boost", "gain": 5}])
HARP2 = S.track("ハープ（節）", "harp", patch="folkHarp", recipe="celtic-harp", volume=0.5, pan=0.25, reverb=0.45, sustain=1.8, fx=[{"type": "boost", "gain": 9}])
CEL = S.track("チェロ（のばす音）", "strings", patch="cello", recipe="celtic-low", volume=0.09, pan=-0.2, reverb=0.35, sustain=1.0)
FID = S.track("フィドル", "strings", patch="violin", recipe="celtic-fiddle", volume=0.12, pan=0.22, reverb=0.45, sustain=1.0)
ACC = S.track("アコーディオン", "accordion", volume=0.085, pan=-0.3, reverb=0.3)
BOD = S.track("わく太鼓（バウロンの役の低い太鼓）", "inchTom", volume=0.12, pan=0.08, reverb=0.25)
BASS = S.track("ウッドベース（指弾き・丸い音）", "bass", sustain=1.0, **dict(finger_bass_spec(vol=0.045), fx=[{"type": "eq", "low": 1, "mid": 0, "midHz": 800, "high": -4}, {"type": "filter", "kind": "lowpass", "freq": 1200, "mix": 1.0}]))
PNO = S.track("ピアノ（高い所のあかり）", "piano", recipe="celtic-piano", volume=0.17, pan=0.35, reverb=0.5, sustain=1.8)
HARPL = S.track("ハープ（低い音・前奏とおわり）", "harp", patch="folkHarp", recipe="celtic-harp", volume=0.5, pan=0.0, reverb=0.4, sustain=2.0, fx=[{"type": "boost", "gain": 12}])
STR = [S.track(f"弦{i + 1}", "strings", patch="slowStrings", recipe="celtic-strings", volume=0.028, pan=-0.6 + 1.2 * i, reverb=0.5, sustain=1.5) for i in range(2)]

root = lambda b: S.chords[b].split("|")[0].split("/")[0]
key_of = lambda b: KE if S.scene_of(b)[0] in ("月の歌", "月の歌2", "くり返し3", "おわり") or (S.scene_of(b)[0] == "受け渡し" and S.scene_of(b)[1] >= 4) else K


def tr_line(line, semi):
    return " ".join(t if t.startswith("R") else f"{nm(midi(t.split(':')[0]) + semi)}:{t.split(':')[1]}" for t in line.split())


def harp(b, order=(0, 2, 3, 4, 3, 2), lo="D3", hi="D5"):
    tn = tones(root(b), lo, hi); HARP.bar(b, " ".join(f"{nm(tn[q % len(tn)])}:0.5" for q in order))


def greet(tr, b, o):
    """あいさつ（「またあした」の節 3・5・6・5・2 を、1小節で）。o: 高さ（4 ならその調の 1 がオクターブ4）"""
    tr.bar(b, key_of(b).mel("3:0.75 5:0.25 6:0.5 5:0.5 2:1", oct=o))


def strs(b, c=69):
    v = sorted(voice(root(b), c, 3)); STR[0].bar(b, f"{nm(v[0])}:3"); STR[1].bar(b, f"{nm(v[2])}:3")


def fid_long(b, c=78):
    v = sorted(voice(root(b), c, 3)); FID.bar(b, f"{nm(v[1])}:3")


def star(b, c=88):
    v = sorted(voice(root(b), c, 3)); PNO.bar(b, f"R:1 {nm(v[1 if b % 2 else 2])}:2")


LOB, HIB = "F1", "A1"
BOD_S = f"{LOB}:1.5 {HIB}:0.5 {HIB}:1"                       # 静かな型（ドン・・タ タ）
BOD_A = f"{LOB}:1 {HIB}:0.5 {HIB}:0.5 {LOB}:0.5 {HIB}:0.5"   # くり返しの型
BOD_B = f"{LOB}:1 {HIB}:1 {HIB}:0.5 {HIB}:0.5"
BOD_R = f"{LOB}:0.5 {LOB}:0.5 {HIB}:0.5 {HIB}:0.5 {HIB}:0.25 {HIB}:0.25 {HIB}:0.25 {HIB}:0.25"   # ロール（場面の変わり目）
A1 = [0, 2, 3, 4, 3, 2]; A2 = [0, 3, 2, 4, 2, 3]
HOOK_D = "F#4:1.5 A4:0.5 B4:1"; HOOK_D2 = "A4:1.5 E4:1.5"            # 前奏とおわりで、ハープが1本の線で弾く「またあした」

for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "前奏":                                                       # ハープ1本。1本の線で「またあした」→ 分散和音
        # 4 回めの直し: ハープ1本の線だけだと前奏が −31dB（歌1 より 8dB 小さい）。分散和音・節・低い音の 3 つを最初から鳴らす（楽器はハープだけのまま）
        harp(b, A1 if i % 2 == 0 else A2); HARPL.bar(b, f"{nm(low(S.chords[b], 'A1'))}:3")
        if i == 0: HARP2.bar(b, HOOK_D)
        elif i == 1: HARP2.bar(b, HOOK_D2)
        elif i == 2: HARP2.bar(b, "D5:1.5 F#5:0.5 A5:1")
        else: HARP2.bar(b, "E5:3")
    elif n == "太陽の歌1":                                                # 声とハープ → 行の終わりごとに、チェロ・フィドル・アコーディオン・わく太鼓
        harp(b, A1 if i % 2 == 0 else A2)
        if i == 3: greet(CEL, b, 3)
        elif i > 3: CEL.bar(b, "D2:3")
        if i == 7: greet(FID, b, 5)
        elif i > 7: fid_long(b)
        if i == 11: greet(ACC, b, 4)
        if i == 15: BOD.bar(b, BOD_R)
    elif n == "くり返し1":
        harp(b, A2 if i % 2 == 0 else A1); CEL.bar(b, f"{nm(low(S.chords[b], 'C2'))}:3"); BOD.bar(b, BOD_R if last else (BOD_A if i % 2 == 0 else BOD_B))
        if i in (0, 4): FID.bar(b, tr_line(K.mel((HOOK if i == 0 else HOOK_UP)[0], oct=5), 0))          # フィドルが「またあした」をいっしょに（1オクターブ上）
        elif i in (1, 5): FID.bar(b, K.mel("5:1.5 2:1.5" if i == 1 else "1':1.5 5:1.5", oct=5))
        else: fid_long(b)
        if i in (3, 7): greet(ACC, b, 4)
    elif n == "太陽の歌2":                                                # → ウッドベース → 高いピアノ → 弦
        harp(b, A1 if i % 2 == 0 else A2); CEL.bar(b, "D2:3"); BOD.bar(b, BOD_R if last else BOD_S)
        if i % 4 != 3: fid_long(b)
        if i == 3: greet(BASS, b, 2)
        if i == 7: greet(PNO, b, 6)
        elif i > 7: star(b)
        if i == 11: greet(FID, b, 5); greet(ACC, b, 4)
        if i >= 11: strs(b, 66)
    elif n == "くり返し2":
        harp(b, A2 if i % 2 == 0 else A1); CEL.bar(b, f"{nm(low(S.chords[b], 'C2'))}:3"); BOD.bar(b, f"{LOB}:3" if last else (BOD_A if i % 2 == 0 else BOD_B)); strs(b, 69); star(b)
        if i in (0, 4): FID.bar(b, K.mel((HOOK if i == 0 else HOOK_UP)[0], oct=5))
        elif i in (1, 5): FID.bar(b, K.mel("5:1.5 2:1.5" if i == 1 else "1':1.5 5:1.5", oct=5))
        else: fid_long(b)
        if i == 3: greet(ACC, b, 4)
    elif n == "受け渡し":                                                 # フィドル（ひる）が歌の節をひとりで → E に上がって、ハープとピアノ（よる）が受けとる
        if i < 4:
            FID.bar(b, K.mel(L1[i].replace("R:1", "R:1") if i < 3 else "5:3", oct=5)); CEL.bar(b, "D2:3" if i < 3 else "B1:3"); HARP.bar(b, f"{nm(low(S.chords[b], 'D3'))}:3")
        else:
            HARP2.bar(b, KE.mel(L1[i - 4] if i < 7 else "5:3", oct=5)); PNO.bar(b, KE.mel(L1[i - 4] if i < 7 else "5:3", oct=6)); harp(b, A1, "E3", "E5"); CEL.bar(b, "E2:3")
            if i >= 6: strs(b, 68)
            if last: BOD.bar(b, BOD_R)
    elif n == "月の歌":                                                   # 透きとおる場面。行の終わりごとに、あいさつの節を順に回す（フィドル → アコーディオン → ピアノ → みんな）
        harp(b, A1 if i % 2 == 0 else A2, "E3", "E5"); CEL.bar(b, "E2:3"); strs(b, 68)
        if i % 4 != 3: star(b)
        if i >= 8: BOD.bar(b, BOD_R if last else BOD_S)
        if i == 3: greet(FID, b, 5)
        if i == 7: greet(ACC, b, 4)
        if i == 11: greet(PNO, b, 6)
        if i == 15: greet(FID, b, 5)
    elif n == "月の歌2":                                                  # 月の歌のつづき。わく太鼓とベースが歩き出し、くり返し3 へふくらむ
        harp(b, A2 if i % 2 == 0 else A1, "E3", "E5"); CEL.bar(b, "E2:3"); strs(b, 68); BOD.bar(b, BOD_R if last else BOD_S)     # くり返し3 より大きくしない（わく太鼓は静かな型のまま・高いピアノは休む）
        if i >= 8 and i % 4 != 3: fid_long(b, 78)
        if i == 3: greet(ACC, b, 4)
        if i == 7: greet(FID, b, 5)
        if i == 11: greet(PNO, b, 6); greet(ACC, b, 4)
        if i == 15: greet(FID, b, 5); greet(ACC, b, 4); greet(PNO, b, 6)
    elif n == "くり返し3":                                                # 全員
        harp(b, A2 if i % 2 == 0 else A1, "E3", "E5"); CEL.bar(b, f"{nm(low(S.chords[b], 'C2'))}:3"); strs(b, 71); star(b)
        BOD.bar(b, f"{LOB}:3" if last else (BOD_R if i == 7 else (BOD_A if i % 2 == 0 else BOD_B)))
        if i in (0, 4, 8, 12): FID.bar(b, KE.mel(HOOK[0] if i == 0 else HOOK_UP[0], oct=5))
        elif i in (1, 5, 9, 13): FID.bar(b, KE.mel("5:1.5 2:1.5" if i == 1 else "1':1.5 5:1.5", oct=5))
        else: fid_long(b, 80)
        if i in (3, 11): greet(ACC, b, 4)
        else: ACC.bar(b, f"{nm(sorted(voice(root(b), 64, 3))[1])}:3")                                   # いちばん大きい場面: アコーディオンののばす音と、ハープが「またあした」をいっしょに
        if i in (0, 4, 8, 12): HARP2.bar(b, KE.mel(HOOK[0] if i == 0 else HOOK_UP[0], oct=4))
        elif i in (1, 5, 9, 13): HARP2.bar(b, KE.mel("5:1.5 2:1.5" if i == 1 else "1':1.5 5:1.5", oct=4))
    elif n == "おわり":                                                   # 声とハープ → ハープだけ → 高いピアノの一番星
        if i < 2: harp(b, A1, "E3", "E5"); CEL.bar(b, "E2:3")
        elif i == 2: harp(b, A1, "E3", "E5"); CEL.bar(b, "E2:3")
        elif i == 3: HARP.bar(b, "E3:3")
        elif i == 4: HARP2.bar(b, tr_line(HOOK_D, 2)); HARP.bar(b, "E3:3"); HARPL.bar(b, "E2:3")
        elif i == 5: HARP2.bar(b, tr_line(HOOK_D2, 2)); HARP.bar(b, "B2:3"); HARPL.bar(b, "B1:3")
        elif i == 6: PNO.bar(b, "E7:3"); HARP.bar(b, "E3:3")

# ================= ウッドベース（太陽の歌2 から。付点2分の根音と、3拍めの5度）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1"); nx = S.chords[b + 1] if b + 1 < S.nb else ch; rn = low(nx, "E1")
    up = tones(root(b), nm(r + 1), nm(r + 12)); t5 = next((m for m in up if (m - r) in (6, 7, 8)), r + 7); t3 = next((m for m in up if (m - r) in (3, 4)), r + 4)
    ap = t5 if rn == r else (rn - 2 if rn > r else rn + 2)
    long_ = f"{nm(r)}:3"; two = f"{nm(r)}:1.5 {nm(t5)}:1.5"; walk = f"{nm(r)}:1 {nm(t3)}:1.5 {nm(ap)}:0.5"; pick = f"{nm(r)}:2.5 {nm(ap)}:0.5"; sway = f"{nm(r)}:2 {nm(t5)}:0.5 {nm(r)}:0.5"      # のばす小節のかわりのゆれ（のばすだけの小節が多いと、ほかの3拍子の曲と同じ型になる）
    if n == "太陽の歌2" and i > 3: BASS.bar(b, two if i % 4 == 1 else (walk if i % 4 == 3 else (pick if i % 4 == 2 else sway)))
    elif n == "くり返し2": BASS.bar(b, walk if i in (3, 6) else (pick if i in (1, 5) else two))
    elif n == "受け渡し" and i >= 4: BASS.bar(b, long_)
    elif n == "月の歌": BASS.bar(b, two if i % 4 == 2 else (pick if i % 4 == 3 else (sway if i % 4 == 0 else long_)))
    elif n == "月の歌2": BASS.bar(b, (sway if i % 2 == 0 else pick) if i < 4 else (walk if i % 4 == 3 else (sway if i % 4 == 0 else two)))
    elif n == "くり返し3": BASS.bar(b, long_ if last else (walk if i % 4 == 3 else (pick if i % 4 == 1 else two)))
    elif n == "おわり" and i < 2: BASS.bar(b, long_)

S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の18（17時）。ケルトのゆっくりの歌（4分の3）。D→E。夕方5時、ひるの番人が金色のはしごをおり、銀のくつの番人に光のかぎを手わたす。"
          "1行歌うごとに、楽器が1つ「またあした」の節をあいさつに弾いて入ってくる。ハープ・チェロ・フィドル・アコーディオン・わく太鼓・ウッドベース・ピアノ・弦。ドラムセットと電子の音はなし。自作")
finish(S, LY, V, 0)

# ================= 仕上げのあとに足すもの =================
from vt3x_lib import *
path = sys.argv[1]
humanize(path, "ハープ", mid=82, down=10, up=8, seed=3); humanize(path, "フィドル", mid=84, down=8, up=8, seed=5); humanize(path, "わく太鼓", mid=80, down=12, up=10, seed=9); humanize(path, "ピアノ", mid=76, down=10, up=8, seed=11)
final_gain(path, {"くり返し3": 1.2})   # いちばん大きい場面を、月の歌2 より大きく（上げるのは 1.5dB まで。場面の変わり目で大きく下げない決まり）
if VOCAL:
    backing(path, 0.9)   # 2026-11-13 人間「声以外のバック音量0.9ぐらいにしようか」
    remark(path, S, std_mark(("chorus",)))
    vocal_polish(path, S, {"verse": 12, "bridge": 12, "chorus": 20, "くり返し3": 24, "outro": 10}, scoop=0.3, slash=0.7, vib_min_beats=1.5, vib_start=0.5, auto=0.6, breaths=0.0)
    harmony(path, S, [("くり返し2", 0, None, K), ("くり返し3", 0, None, KE)], vol=0.34)
    voice_by_scene(path, S, {}, default="clear")     # 2026-11-17 人間「各曲パートで変えないように」→ 1 曲 1 種類の声
    sing_ends(path, S, max_len=3.0, throw=0.25)      # 句の最後の音をのばす・消え方・音程の動き（2026-11-17）
    js = load(path)
    for v in js.get("vocals", []): v["debreath"] = 0.5; v["softCons"] = 0.3
    # 歌の大きさは決まりのまま（vocalLevel 0.6＝耳の感じ方に近い重みで、歌は伴奏より約 5dB 小さく。2026-10-25 人間「伴奏より圧倒的に声が大きく聞こえる」で決めた値）。
    #   いちど 1.2 に上げて書き出したら、歌が伴奏より 5〜7dB 大きくなったので戻した
    save(path, js)
