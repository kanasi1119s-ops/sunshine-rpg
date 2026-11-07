# vtp 06「白い息のリテイク」バラード版（仮）— 重音テト・ミドルテンポのバラードロック。88・4/4。G長調 → 最後のサビは +2（A長調）。
# 2026-11-07 人間「ちょっと曲調変えて作り直そうか。ギターは和音メインにして」→ 曲調は「ミドルテンポのバラードロック」（人間が選んだ）
#   ギター＝和音が主役（左右とも）。単音はリードの旋律・合いの手・ソロだけ。
#   弾く場所は曲の句に合わせて型で決め、本物のギタリストの揺れ方（GuitarSet）だけを借りる（strum_groove.py）。ドラムは人の演奏データ（83〜88）。
#   コード進行: 王道・カノン・丸サは使わない。Aメロ＝借りた和音（Dm7/F・Cm6・E7/G#）、サビ＝G→Gaug→G6→G7 の内声の上昇、
#   ♭Ⅵ→♭Ⅶ（E♭maj7→F）で開く、「ごめんね」は Dsus4 のまま、落ちサビの E7 で A長調へ。
import sys, os, json, copy, re, random
from vt25_lib import *
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../tools/composer'))
from strum_groove import Groove, Lanes
from gmd_to_parts import parts_from_gmd

BPM = 88
S = Song("06", "whitebreath-ballad", "白い息のリテイク（バラード・仮）", "White Breath Retake (Ballad)", BPM, 4, "G", "major", "バラードロック（冬）")
S.kit = "crocell-punch"
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags + " --piano salamander"
S.keep_old_synth = True
S.no_depth = True
K = Key("G", "major")
KL = Key("A", "major")

INTRO = ["Ebmaj7", "F", "G", "G"]
VCH = ["G", "Dm7/F", "Cmaj7", "Cm6", "G/B", "E7/G#", "Am7", "D7sus4"]
BCH = ["Ebmaj7", "F", "Am7", "D7sus4"]
CHB = ["G", "Gaug", "G6", "G7", "Cmaj7", "Cm6", "Bm7", "E7", "Am7", "Bm7", "Cmaj7", "D"]
CH1 = CHB + ["Ebmaj7", "Cm6", "Dsus4", "Dsus4"]
CH2 = CHB + ["Ebmaj7", "F", "G", "G"]
SOLOCH = ["Cmaj7", "D/C", "Bm7", "E7", "Am7", "Bm7", "Cmaj7", "D7sus4"]
CMCH = ["Em", "Em/D", "Cmaj7", "B7"]
OCH = CHB[:8]
LASTCH = [tr_chord(c, 2) for c in CH2]
OUTCH = ["A", "Fmaj7", "G", "A"]

S.scene("前奏", 4, "intro", INTRO)
S.scene("Aメロ1", 8, "verse", VCH)
S.scene("Bメロ1", 4, "pre", BCH)
S.scene("サビ1", 16, "chorus", CH1)
S.scene("間奏", 4, "solo", INTRO)
S.scene("Aメロ2", 8, "verse", VCH)
S.scene("Bメロ2", 4, "pre", BCH)
S.scene("サビ2", 16, "chorus", CH2)
S.scene("ソロ", 8, "solo", SOLOCH)
S.scene("Cメロ", 4, "bridge", CMCH)
S.scene("落ちサビ", 8, "bridge", OCH)
S.scene("最後のサビ", 16, "chorus", LASTCH)
S.scene("後奏", 4, "outro", OUTCH)

V = Voice(S, vol=0.2, delay=0.5, bright=0.2, patch="brightLead", low=False)
# 2026-11-07 人間「リードギターシンセサイザーに変更」: 単音の旋律・合いの手・ソロを、あたたかいノコギリ波の重ね（Surge XT のプリセットを録った音）に。
#   冬のバラードなので、少し長めの残響と、2拍ずつ遠くで返るやまびこで空間を作る
LEAD = S.track("リード（シンセ・単音）", "lead", patch="surgeHappySaws", volume=0.085, pan=0.1, reverb=0.28, mono=True, breath=True,
               fx=[{"type": "filter", "kind": "lowpass", "freq": 7000, "q": 0.6}, {"type": "pingpong", "time": 0.5, "feedback": 0.25, "mix": 0.18}])
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.23))
LY = Lyrics(S)

# ================= 歌（G長調・oct 3: 1＝G3、1'＝G4、6'＝E5、7'＝F#5） =================
VA = ["R:0.25 5:0.25 5:0.25 6:0.25 1':0.5 1':0.25 7:0.25 6:0.5 5:0.25 3:0.25 5:0.5 R:0.5",          # G
      "R:0.25 5:0.25 5:0.25 6:0.25 b7:0.5 b7:0.25 6:0.25 5:0.5 4:0.25 2:0.25 4:0.5 R:0.5",          # Dm7/F
      "R:0.25 3:0.25 5:0.25 6:0.25 1':0.5 2':0.5 3':0.25 2':0.25 1':0.25 1':0.25 6:0.25 5:0.25 R:0.5",  # Cmaj7
      "R:0.5 b6:0.25 b6:0.25 5:0.5 4:0.25 2:0.25 4:1.5 R:0.5",                                              # Cm6
      "R:0.25 5:0.25 5:0.25 6:0.25 1':0.5 1':0.25 7:0.25 6:0.5 5:0.25 6:0.25 1':0.5 R:0.5",          # G/B
      "R:0.25 6:0.25 6:0.25 7:0.25 #1':0.5 #1':0.25 7:0.25 6:0.5 5:0.25 3:0.25 6:0.5 R:0.5",         # E7/G#
      "R:0.25 2:0.25 4:0.25 6:0.25 1':0.5 2':0.5 4':0.25 2':0.25 1':0.25 1':0.25 6:0.25 2':0.25 R:0.5",  # Am7
      "R:0.5 5:0.25 5:0.25 1':0.5 2':0.25 1':0.25 5:1.5 R:0.5"]                                              # D7sus4
VB = ["R:0.5 5:0.5 b6:0.5 1':0.5 2':0.5 b3':1 R:0.5", "R:0.5 1':0.5 2':0.5 4':0.5 2':0.5 4':1 R:0.5",
      "R:0.5 2':0.5 4':0.5 5':0.5 4':0.5 6':1 R:0.5", "R:0.5 5':0.25 5':0.25 4':0.5 2':0.5 1':0.5 2':1.5"]
Q1 = ["3':1 2':0.5 1':0.5 2':1 3':0.5 5':0.5", "#5':1 3':0.5 3':0.5 2':0.5 1':0.5 R:1"]
Q2 = ["6':1 5':0.5 3':0.5 5':1 6':0.5 5':0.5", "4':0.5 3':0.5 2':0.5 b7:0.5 1':1 R:1"]
Q3 = ["5':1.5 3':0.5 5':1 6':1", "b6':1 5':0.5 4':0.5 2':0.5 1':0.5 2':0.5 R:0.5"]
Q4 = ["3':1 2':0.5 3':0.5 5':1 7:1", "6:0.5 6:0.5 #1':0.5 2':0.5 3':1 R:1"]
Q5 = ["1':1 2':0.5 4':0.5 2':1 4':0.5 6':0.5", "5':1 3':0.5 3':0.5 2':0.5 3':0.5 R:1"]
Q6 = ["3':1 5':0.5 6':0.5 5':1 3':0.5 5':0.5", "7':1 6':0.5 5':0.5 6':0.5 5':0.5 R:1"]
Q7S = ["5':1.5 b3':0.5 1':0.5 b3':0.5 5':1", "b6':0.5 b6':0.5 5':0.5 4':0.5 b3':1 R:1"]
Q7 = ["5':1.5 b3':0.5 1':0.5 b3':0.5 5':1", "4':0.5 4':0.5 2':0.5 4':0.5 5':1 R:1"]
Q8S = ["R:1 5':1 4':1 2':1", "1':3 R:1"]
Q8 = ["3':1 2':0.5 1':0.5 2':1 3':0.5 5':0.5", "3':1 2':0.5 2':0.5 1':2"]
CHM = Q1 + Q2 + Q3 + Q4 + Q5 + Q6
VCM = ["R:0.5 3':0.5 3':1 2':0.5 1':1 R:0.5", "R:0.5 2':0.5 2':1 1':0.5 6:1 R:0.5",
       "R:0.5 3':0.5 5':0.5 6':1 5':0.5 3':0.5 R:0.5", "R:0.5 #5':1 3':0.5 2':1 7:1"]

A1 = ("えきのまえのひかりに/かぜがほほをさしてく/てぶくろのなかでにぎった/ことばのたね/"
      "なんどもれんしゅうした/さいしょのひとことだけ/きみがふりむくまえにね/いきをすうの")
B1 = "ほしのした/きみがくる/あとすこし/いまいわなきゃ"
C1 = ("ふゆのよるにきみをよぶ/こごえたこえがこぼれた/すきといえたはじめて/しろいいきがきえてく/"
      "ふゆのよるにきみはいう/やさしいめでうつむいて/ありがとうでもいまは/ごめんね")
A2 = ("はるにかみをきってみた/なつのあさははしるの/にがてなこともいちから/やりなおした/"
      "あきのそらはたかくて/かがみのなかのわたし/すこしだけかおをあげた/まえをむいた")
B2 = "ふゆがくる/またおなじ/あのみちへ/こんどこそね"
C2 = ("ふゆがくるまでにかわる/きのうのわたしをこえる/だれのためでもなくて/わたしのためにはしる/"
      "ふゆがくるまでにかわる/ころんだかずだけつよく/なりたいからかおあげ/つぎのふゆまではしれ")
CMT = "ひととせ/このみち/しろいいき/きみのせ"
OC = "ふゆのよるにまたきたよ/いちねんぶんのことばを/こわいけれどいわせて/しろいいきにのせるよ"
C3 = ("ふゆのよるにまたここで/こごえないこえでいうよ/すきだよともういちど/しろいいきがかがやく/"
      "ふゆのよるにきみをよぶ/こごえたこえはもうない/すきだよともういちど/しろいいきのむこうへ")


def put(name, key, lines, text, o=3):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA, A1)
put("Bメロ1", K, VB, B1)
put("サビ1", K, CHM + Q7S + Q8S, C1)
put("Aメロ2", K, VA, A2)
put("Bメロ2", K, VB, B2)
put("サビ2", K, CHM + Q7 + Q8, C2)
put("Cメロ", K, VCM, CMT)
put("落ちサビ", K, Q1 + Q2 + Q3 + Q4, OC)
put("最後のサビ", KL, CHM + Q7 + Q8, C3)

# ================= リード（単音: 前奏・間奏の旋律、合いの手、ソロ） =================
INTRO_L = ["G5:2 F5:1 D5:1", "C5:1.5 D5:0.5 F5:1 E5:0.5 D5:0.5", "D5:3~. B4:1", "B4:2 A4:1 G4:1"]
INTER_L = ["D5:1 D#5:1 G5:2", "F5:1 D5:1 C5:1 A4:1", "B4:2^@0.3 A4:1 G4:1", "G4:4~."]
SOLO = ["E5:1.5 D5:0.5 B4:1 G4:1", "A4:1 B4:0.5 D5:0.5 F#5:2~.", "F#5:0.5 E5:0.5 D5:0.5 B4:0.5 D5:2^^@0.3",
        "G#4:1 B4:1 D5:1 E5:1", "C5:1.5 B4:0.5 A4:1 E5:1", "D5:2!~. F#5:1 A5:1", "G5:1 F#5:0.5 E5:0.5 D5:1 B4:1", "A4:2^^@0.4 G4:1 D5:1"]
for name, ph in (("前奏", INTRO_L), ("間奏", INTER_L), ("ソロ", SOLO)):
    for i, b in enumerate(S.sc(name)): LEAD.bar(b, ph[i])
for name, obb in (("サビ2", "R:3 B4:0.5 D5:0.5"), ("最後のサビ", "R:3 C#5:0.5 E5:0.5")):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 1 and i < 14: LEAD.bar(b, obb)

# ================= ベース =================
def bass_root(ch):
    bs = ch.split("/")[1] if "/" in ch else re.match(r"[A-G][#b]?", ch).group(0)
    return low(bs, "E1")
for b in range(S.nb):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]; r = bass_root(ch)
    if n == "前奏": BASS.bar(b, "R:4" if i < 2 else f"{nm(r)}:3 {nm(r)}:0.5 {nm(r + 12)}:0.5"); continue
    if n in ("Aメロ1", "Aメロ2"): BASS.bar(b, f"{nm(r)}:2.5 {nm(r)}:1 {nm(r + 7)}:0.5" if n == "Aメロ1" else f"{nm(r)}:1.5 {nm(r)}:0.5 R:0.5 {nm(r)}:1 {nm(r + 12)}:0.5"); continue
    if n in ("Bメロ1", "Bメロ2"): BASS.bar(b, " ".join([f"{nm(r)}:1"] * 4) if i < 3 else f"{nm(r)}:0.5 {nm(r)}:0.5 {nm(r)}:0.5 {nm(r)}:0.5 {nm(r)}:0.5 {nm(r)}:0.5 {nm(r + 12)}:0.5 {nm(r + 12)}:0.5"); continue
    if n == "サビ1" and i >= 14: BASS.bar(b, f"{nm(r)}:4" if i == 14 else "R:4"); continue
    if n == "Cメロ": BASS.bar(b, f"{nm(r)}:4"); continue
    if n == "落ちサビ": BASS.bar(b, "R:4" if i < 4 else f"{nm(r)}:4"); continue
    if n == "後奏": BASS.bar(b, f"{nm(r)}:4"); continue
    BASS.bar(b, f"{nm(r)}:1 {nm(r)}:0.5 {nm(r)}:0.5 {nm(r)}:1 {nm(r)}:0.5 {nm(r + 12)}:0.5")


# ================= ピアノ（2026-11-07 人間「ピアノも追加」）: 左手＝低い音、右手＝和音と単音を場面で使い分ける =================
PNL = S.track("ピアノ（左手）", "piano", volume=0.09, pan=-0.2, reverb=0.3, fx=[{"type": "eq", "low": -3, "mid": -1, "midHz": 400, "high": -1}])
PNR = [S.track(f"ピアノ（右手{j + 1}）", "piano", volume=0.06, pan=-0.12, reverb=0.3, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 2600, "high": 0}]) for j in range(3)]
PNA = S.track("ピアノ（右手の単音）", "piano", volume=0.07, pan=0.15, reverb=0.32, fx=[{"type": "eq", "low": -4, "mid": -1, "midHz": 2600, "high": 0}])
prev = None
for b in range(S.nb):
    n, i, L, k = S.scene_of(b); ch = S.chords[b]; r = bass_root(ch) + 12
    v = voice(ch.split("/")[0], 67 if n != "最後のサビ" else 69, 3, prev); prev = v
    t = tones(ch.split("/")[0], "G4", "D6")
    if n == "前奏":
        PNL.bar(b, f"{nm(r)}:4"); [PNR[j].bar(b, f"{nm(v[j])}:4") for j in range(3)]
        PNA.bar(b, " ".join(f"{nm(t[q % len(t)] + 12 if q >= 4 else t[q % len(t)])}:0.5" for q in (0, 1, 2, 3, 4, 3, 2, 1)) if i < 2 else "R:4")
    elif n in ("Aメロ1", "Aメロ2"):
        PNL.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2")
        if n == "Aメロ1": PNA.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 1, 3, 2, 1, 3, 2)))      # 単音の分散和音
        else: [PNR[j].bar(b, f"R:1 {nm(v[j])}:1 R:1 {nm(v[j])}:1") for j in range(3)]                        # 2番は裏で和音
    elif n in ("Bメロ1", "Bメロ2"):
        PNL.bar(b, f"{nm(r)}:4"); [PNR[j].bar(b, f"{nm(v[j])}:1 {nm(v[j])}:1 {nm(v[j])}:1 {nm(v[j])}:1") for j in range(3)]
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        if n == "サビ1" and i >= 14:
            if i == 14: PNL.bar(b, f"{nm(r)}:8"); [PNR[j].bar(b, f"{nm(v[j])}:8") for j in range(3)]
            if i == 15: PNA.bar(b, f"R:2 {nm(t[2])}:1 {nm(t[1])}:1")        # 「ごめんね」のあとに単音が2つだけ残る
            continue
        PNL.bar(b, f"{nm(r)}:1.5 {nm(r)}:0.5 {nm(r + 12)}:1 {nm(r)}:1")
        [PNR[j].bar(b, f"{nm(v[j])}:1.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:1.5") for j in range(3)]
        if n == "最後のサビ" and i % 2 == 1: PNA.bar(b, f"R:2 {nm(t[-1])}:0.5 {nm(t[-2])}:0.5 {nm(t[-3])}:1")
    elif n in ("間奏", "ソロ"):
        PNL.bar(b, f"{nm(r)}:2 {nm(r)}:2"); [PNR[j].bar(b, f"{nm(v[j])}:2 {nm(v[j])}:2") for j in range(3)]
    elif n == "Cメロ":
        PNL.bar(b, f"{nm(r)}:4")
        PNA.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 1, 2, 3, 2, 1, 2, 3)))
    elif n == "落ちサビ":                                   # 落ちサビの前半はピアノが主役（歌と、ギターののばす和音だけ）
        PNL.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2"); [PNR[j].bar(b, f"R:0.5 {nm(v[j])}:1.5 R:0.5 {nm(v[j])}:1.5") for j in range(3)]
        PNA.bar(b, " ".join(f"{nm(t[q % len(t)] + 12)}:0.5" for q in (0, 2, 1, 3, 2, 1, 3, 2)) if i < 4 else "R:4")
    elif n == "後奏":
        PNL.bar(b, f"{nm(r)}:4"); [PNR[j].bar(b, f"{nm(v[j])}:4") for j in range(3)]
        if i == 3: PNA.bar(b, f"{nm(t[0] + 12)}:1 {nm(t[1] + 12)}:1 {nm(t[2] + 12)}:2")

# ================= FX（2026-11-07 人間「FXも追加」）: 場面の変わり目に、本物のシンバルの効果音とライザーを重ねる =================
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.07, pan=0, modulate=False)
RISE = S.track("ライザー・サブドロップ", "lead", patch="fxRiser", volume=0.05, pan=0, reverb=0.3)
SNOW = S.track("雪の鈴", "lead", patch="seasonFx", volume=0.035, pan=0.3, reverb=0.4)
for name in ("サビ1", "サビ2"): cym_swell(CYM, S.sc(name)[0], 2, "C4")          # サビの手前: 逆再生のクラッシュ
cym_swell(CYM, S.sc("最後のサビ")[0], 4, "E4")                                   # 最後のサビの手前: スウェル（盛り上がるロール）
RISE.at(S.bar_beat(S.sc("最後のサビ")[0]) - 8, "C4:8")                           # 最後のサビへ: 2小節のライザー
RISE.at(S.bar_beat(S.sc("最後のサビ")[0]), "G4:4")                              # 入った所に低いサブドロップ
RISE.at(S.bar_beat(S.sc("落ちサビ")[0]) - 1, "E4:2")                            # 落ちサビへ: 下がっていく音
CYM.at(S.bar_beat(S.sc("後奏")[-1]), "B4:16")                                   # 最後: ロールのディミヌエンドで消えていく
for name in ("前奏", "落ちサビ"):
    SNOW.at(S.bar_beat(S.sc(name)[0]), "G#4:8")                                  # 雪の鈴（冬の夜の空気。音楽と重ねる）

S.fade_out = 0
S.desc = ("仮: 白い息のリテイク・バラード版（重音テト）。ミドルテンポのバラードロック・G・88、最後のサビは +2（A）。"
          "ギターは左右とも和音が主役（曲の句に合わせた型＋本物のギタリストの揺れ方）、単音はリードの旋律・合いの手・ソロ。ドラムは人の演奏データ。"
          "王道・カノン進行を使わず、借りた和音（Dm7/F・Cm6）、G→Gaug→G6→G7、♭Ⅵ→♭Ⅶ、解決しない「ごめんね」。自作")
finish(S, LY, V, 0, hi=81, level={"verse": -0.25}, special={"最後のサビ": 0.4, "サビ1": 0.15, "落ちサビ": -0.3})

# ================= 書き出したあとで、ギター（左右）とドラムを足す =================
path = sys.argv[1]
js = json.load(open(path))
NB = S.nb; TOTAL = NB * 4
VO = {"Ebmaj7": [None, "A#2", "D#3", "G3", "A#3", "D4"], "F": ["F2", "C3", "F3", "A3", "C4", "F4"], "G": ["G2", "B2", "D3", "G3", "B3", "G4"],
      "Gaug": ["G2", "B2", "D#3", "G3", "B3", "D#4"], "G6": ["G2", "B2", "D3", "G3", "B3", "E4"], "G7": ["G2", "B2", "D3", "G3", "B3", "F4"],
      "Cmaj7": [None, "C3", "E3", "G3", "B3", "E4"], "Cm6": [None, "C3", "D#3", "A3", "C4", "G4"], "Bm7": [None, "B2", "F#3", "A3", "D4", "F#4"],
      "E7": ["E2", "B2", "D3", "G#3", "B3", "E4"], "Am7": [None, "A2", "E3", "G3", "C4", "E4"], "D": [None, "A2", "D3", "A3", "D4", "F#4"],
      "Dsus4": [None, "A2", "D3", "A3", "D4", "G4"], "Dm7/F": ["F2", None, "D3", "A3", "C4", "F4"], "G/B": [None, "B2", "D3", "G3", "B3", "G4"],
      "E7/G#": ["G#2", None, "D3", "G#3", "B3", "E4"], "D7sus4": [None, "A2", "D3", "A3", "C4", "G4"], "Em": ["E2", "B2", "E3", "G3", "B3", "E4"],
      "Em/D": [None, None, "D3", "G3", "B3", "E4"], "B7": [None, "B2", "D#3", "A3", "B3", "F#4"], "D/C": [None, "C3", "D3", "A3", "D4", "F#4"],
      "A": [None, "A2", "E3", "A3", "C#4", "E4"], "Fmaj7": [None, None, "F3", "A3", "C4", "E4"]}
NN = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def mi(n): g = re.match(r"([A-G]#?)(-?\d)", n); return NN.index(g[1]) + (int(g[2]) + 1) * 12
def up(v, s): return [None if x is None else (lambda m: f"{NN[m % 12]}{m // 12 - 1}")(mi(x) + s) for x in v]
for c in CH2: VO[tr_chord(c, 2)] = up(VO[c], 2)
HI4 = lambda v: [None, None] + [x for x in v if x is not None][-4:]
def vo(b): return VO[S.chords[b]]
def vo_next(b): return VO[S.chords[min(NB - 1, b + 1)]]

gL, gR = Groove(seed=11, amount=0.8), Groove(seed=12, amount=0.8, takes=["00_Rock3-148-C_comp", "03_Rock3-148-C_comp", "02_Rock3-117-Bb_comp"])
LS, LL, RR = Lanes(), Lanes(), Lanes()   # 左（軽い歪み）・左（歪み）・右（歪み・高い押さえ方）
P = {"ring": "D---------------", "ring2": "D-------d-------",
     "verse": "D-----u-d-u-d-u-", "verse_end": "D-----u-d---.---",
     "pre": "D---D---D---D-d-", "pre_last": "D---D-d-D-dUD-dU",
     "ch_l": "D---d-u-D-d-u-du", "ch_l_push": "D---d-u-D-d-u-P-", "ch_r": "D-------D---d---",
     "last_r": "D-d-D-d-D-d-D-d-", "solo_l": "D---d-u-D---d-u-"}
for b in range(NB):
    n, i, L, k = S.scene_of(b)
    if n in ("前奏", "間奏"):
        LL.add(gL.bar(b, P["ring"] if i < 2 else P["ring2"], vo(b), vo_next(b), BPM, 1.0))
        if i >= 2 or n == "間奏": RR.add(gR.bar(b, P["ring"], HI4(vo(b)), HI4(vo_next(b)), BPM, 0.95))
    elif n in ("Aメロ1", "Aメロ2"):
        LS.add(gL.bar(b, P["verse_end"] if i == 7 else P["verse"], vo(b), vo_next(b), BPM, 0.85))
        if n == "Aメロ2": RR.add(gR.bar(b, P["ring"], HI4(vo(b)), HI4(vo_next(b)), BPM, 0.75))
    elif n in ("Bメロ1", "Bメロ2"):
        LL.add(gL.bar(b, P["pre_last"] if i == 3 else P["pre"], vo(b), vo_next(b), BPM, 0.88 + 0.04 * i))
        RR.add(gR.bar(b, P["ring2"], HI4(vo(b)), HI4(vo_next(b)), BPM, 0.85))
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        if n == "サビ1" and i >= 14:
            if i == 14: LL.add(gL.bar(b, P["ring"], vo(b), vo(b), BPM, 0.9)); RR.stop_at(b * 4)
            continue
        vv = 1.08 if n == "最後のサビ" else 1.0
        LL.add(gL.bar(b, P["ch_l_push"] if i % 4 == 3 else P["ch_l"], vo(b), vo_next(b), BPM, vv))
        RR.add(gR.bar(b, P["last_r"] if n == "最後のサビ" else P["ch_r"], HI4(vo(b)), HI4(vo_next(b)), BPM, vv * 0.92))
    elif n == "ソロ":
        LL.add(gL.bar(b, P["solo_l"], vo(b), vo_next(b), BPM, 0.95))
        RR.add(gR.bar(b, P["ring2"], HI4(vo(b)), HI4(vo_next(b)), BPM, 0.85))
    elif n == "Cメロ":
        LL.stop_at(b * 4); RR.stop_at(b * 4)
        LS.add(gL.bar(b, P["ring"], vo(b), vo(b), BPM, 0.8))
    elif n == "落ちサビ":
        LS.add(gL.bar(b, P["ring"], vo(b), vo(b), BPM, 0.72 if i < 4 else 0.82))
    elif n == "後奏":
        LL.add(gL.bar(b, P["ring"], vo(b), vo(b), BPM, 1.05)); RR.add(gR.bar(b, P["ring"], HI4(vo(b)), HI4(vo(b)), BPM, 1.0))
for l in (LS, LL, RR): l.stop_at(TOTAL)

src = json.load(open('/tmp/ab/i1_nodr.json'))
gt = [p for p in src['parts'] if p['instrument'] == 'distGuitar'][0]
gtmpl = {k: v for k, v in gt.items() if k not in ('notes', 'role', 'pan', 'volume', 'double')}
gtmpl.update(double=False, powerChord=False, humanTiming=0, release=0.15)
add = []
for side, lanes, pan, vol, over in (("L（軽い歪み）", LS, -0.8, 0.06, {"ampDrive": 0.14, "fx": gtmpl["fx"] + [{"type": "room", "mix": 0.12}]}),
                                     ("L", LL, -0.8, 0.045, {}), ("R", RR, 0.8, 0.045, {"ampCabIr": "jd-greenback-4x12-01"})):
    for st, n_ in enumerate(lanes.notes(TOTAL)):
        if not n_: continue
        p = copy.deepcopy(gtmpl); p.update(role=f"{side}ギター（和音）・弦{st + 1}", pan=pan, volume=vol, notes=n_, **over); add.append(p)

G = '/tmp/gmd/groove/'
PS = G + 'drummer7/session3/11_pop-soft_83_beat_4-4.mid'; R88A = G + 'drummer6/session2/3_rock_88_beat_4-4.mid'
R88B = G + 'drummer6/session3/6_rock_88_beat_4-4.mid'; R86 = G + 'drummer7/session1/1_rock_86_beat_4-4.mid'
dn = {k: [] for k in ('kick', 'snare', 'hihat', 'tom', 'crash')}
def dseg(f, b0, n):
    r = parts_from_gmd(f, b0, n)
    for k in dn: dn[k].append(r.get(k) or f'R:{n * 4}')
def dcus(n, **kw):
    for k in dn: dn[k].append(kw.get(k, f'R:{n * 4}'))
dcus(2); dseg(PS, 2, 2)                                  # 前奏: 2小節はギターだけ
dseg(PS, 8, 8)                                           # Aメロ1
dseg(R88B, 5, 4)                                         # Bメロ1（最後にフィル）
dseg(R86, 1, 8); dseg(R86, 13, 6); dcus(2, crash='C2:8%112', kick='x:8%105')   # サビ1（「ごめんね」で止まる）
dseg(R88A, 16, 4)                                        # 間奏
dseg(R88B, 13, 8)                                        # Aメロ2
dseg(R88B, 21, 4)                                        # Bメロ2
dseg(R86, 21, 8); dseg(R86, 29, 8)                       # サビ2
dseg(R88A, 33, 8)                                        # ソロ（ライド・最後にフィル）
dseg(PS, 16, 4)                                          # Cメロ
dcus(4); dseg(PS, 4, 4)                                  # 落ちサビ（前半は歌とギターだけ）
dseg(R86, 41, 8); dseg(R86, 49, 8)                       # 最後のサビ
dcus(4, kick='x:4%110 x:4%105 x:4%110 x:4%122', crash='C2:4%115 C2:4%110 C2:4%115 C2:4%126')   # 後奏
ref = {p['instrument']: p for p in json.load(open('/tmp/ab/gd.json'))['parts'] if p['instrument'] in dn}
for k, lst in dn.items():
    p = copy.deepcopy(ref[k]); p['notes'] = ' '.join(lst); add.append(p)
tot = {k: sum(float(re.match(r'[\d.]+', t.split(':', 1)[1]).group()) for t in ' '.join(v).split()) for k, v in dn.items()}
assert all(abs(x - TOTAL) < 0.05 for x in tot.values()), (tot, TOTAL)

js["parts"] = [p for p in js["parts"] if p["instrument"] not in ("kick", "snare", "hihat", "tom", "crash", "ride")] + add
json.dump(js, open(path, "w"), ensure_ascii=False)
flatten_arc(path, S)
# v1 の測定: Bメロ（-16.2）・ソロ（-15.7）がサビ1（-18.1）より大きかった → サビがいちばん大きくなるように
SCENE_GAIN = {"前奏": 0.95, "Aメロ1": 0.92, "Bメロ1": 0.85, "Bメロ2": 0.82, "間奏": 0.75, "ソロ": 0.72, "Aメロ2": 0.82, "サビ1": 1.18, "サビ2": 1.14, "最後のサビ": 1.15}
js = json.load(open(path))
for p in js["parts"]:
    g = p.get("barGain", [1] * NB)
    for b in range(NB):
        g[b] = round(min(2.0, g[b] * SCENE_GAIN.get(S.scene_of(b)[0], 1.0)), 4)
    p["barGain"] = g
json.dump(js, open(path, "w"), ensure_ascii=False)
print("ギター・ドラムを足した:", len(add), "パート")
