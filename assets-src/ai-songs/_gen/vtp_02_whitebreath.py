# vtp 02「白い息のリテイク」作り直し（仮）— ボカロック（冬）。168・4/4。F#m（A長調の平行調）→ 最後のサビは +1（Gm／B♭長調）。
# 2026-11-07 人間「根本的にギターの弾き方音の出し方変だよね」「曲自体がクソつまらない」→ v1（vtp_01）を捨てて、作り方から作り直す。
# 物語: 冬の夜、駅前で好きな人に告白する → 「ありがとう、でもいまは…ごめんね」。春に髪を切り、夏は走り、苦手なこともやり直した。
#   1年後の冬、同じ場所で、こごえない声で、もう一度「好きだよ」と言う。答えは聞かずに曲が終わる。
# v1 がつまらなかった理由と、この版で変えたこと:
#   ・旋律: v1 はどの句も「半拍休み＋8分＋長い音」の同じ形 → この版は、
#       サビ＝合いことばの節（裏から入る・同じ音の連打・16分の食い）を、高さと長さを変えて4回くり返す（フック）。3回目で F#5 まで跳ぶ。
#       Aメロ＝低い音域の同音連打と16分の語り。句のあとの2拍をギターが答える（かけ合い）。Bメロ＝長い音で1拍ずつ上る。
#   ・展開: 物語の山を音の事件にする。曲の頭は声だけ（アカペラの2小節）→ バンドがいっせいに入る。
#       サビ1 の最後「ごめんね」でバンドが止まり、ピアノと声だけ。2番のAメロは季節が4小節ごとに変わる（楽器が入れかわる）。
#       Cメロで調を外し、最後のサビは +1。最後の「好きだよ」のあと全員が止まり、答えのかわりに白い息（声の息）だけ。
#   ・ギター: v1 は和音の音を1本ずつ別のパートで鳴らしていた（本物はまとめてかき鳴らす）→ この版は、
#       左右のギター＝パワーコード（1本の中で5度とオクターブが鳴る）を「2回別々に弾いた」ダブル（double）で左右いっぱいに。
#       弾き方はダウン中心＋アクセント（1拍目と2拍目の裏）・場面によってのばす・キメ。
#       Aメロのきれいなギター＝分散和音の音を次の音まで鳴らし続ける（3本で受けもち、弦が残って響く）。リード＝イントロのリフと、歌の合間のオブリ（合いの手）とソロ。
from vt25_lib import *
import json as _json2, os as _os2

SKETCH = _os2.environ.get("VTP_SKETCH") == "1"     # 頭の試作（アカペラ＋イントロ＋Bメロ＋サビ1）だけ書き出す
S = Song("02", "whitebreath2", "白い息のリテイク（仮）", "White Breath Retake", 168, 4, "A", "major", "ボカロック（冬）")
S.kit = "crocell-punch"
S.flags = "--bass bnb-loud --ref-tone glossy-jrock " + S.flags + " --piano salamander --space room --space-wet 0.12"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.4
S.drum_scale = 0.9
K = Key("A", "major")          # oct 3 で 1 = A3（歌うのは A3〜F#5）
KL = Key("Bb", "major")        # 最後のサビ（+1）

CH1 = ["Dmaj7", "E/D", "C#m7", "F#m7", "Bm7", "C#7", "F#m7", "F#m/E"]
CH2 = ["Dmaj7", "E/D", "C#m7", "F#m7", "Bm7", "E", "A", "A"]
CH2SAD = ["Dmaj7", "E/D", "C#m7", "F#m7", "Bm7", "E", "Dmaj7", "Dmaj7"]   # 「ごめんね」は解決しない
VCH = ["F#m", "F#m/E", "Dmaj7", "C#7"]
BCH = ["Bm7", "C#m7", "Dmaj7", "E", "Bm7", "C#m7", "Dmaj7", "E"]
CMCH = ["Fmaj7", "G", "A", "A", "Fmaj7", "G", "Bbmaj7", "F7"]          # Cメロ: 借りた和音（♭VI・♭VII）→ ♭II → 最後のサビ（B♭長調）へ
LAST = [tr_chord(c, 1) for c in CH1 + CH2 + CH1]
RIFFCH = ["F#m", "Dmaj7", "E", "C#7"]

S.scene("アカペラ", 2, "intro", ["Dmaj7", "E/D"])
S.scene("イントロ", 8, "intro", RIFFCH + RIFFCH)
if not SKETCH:
    S.scene("Aメロ1", 16, "verse", VCH * 4)
S.scene("Bメロ1", 8, "pre", BCH)
S.scene("サビ1", 16, "chorus", CH1 + CH2SAD)
if not SKETCH:
    S.scene("ためいき", 4, "break", ["Dmaj7", "Dmaj7", "E", "E"])
    S.scene("Aメロ2", 16, "verse", VCH * 4)
    S.scene("Bメロ2", 8, "pre", BCH)
    S.scene("サビ2", 16, "chorus", CH1 + CH2)
    S.scene("間奏", 8, "solo", RIFFCH + RIFFCH)
    S.scene("Cメロ", 8, "bridge", CMCH)
    S.scene("落ちサビ", 8, "bridge", [tr_chord(c, 1) for c in CH1[:7]] + ["F7"])
    S.scene("最後のサビ", 24, "chorus", LAST)
    S.scene("白い息", 4, "outro", ["Ebmaj7", "Ebmaj7", "Ebmaj7", "Ebmaj7"])

V = Voice(S, vol=0.2, delay=0.5, bright=0.2, patch="brightLead", low=False)
GTR = S.track("L・Rギター（パワーコードのダブル）", "distGuitar", **{**rock_gtr_spec(0.06, 0.0, drive=0.42), "powerChord": True, "double": {"spread": 1.0}})
CL = [S.track(f"きれいなギター（分散和音・弦{i + 1}）", "guitar", amp="crystal", volume=0.055, pan=0.45, reverb=0.25, chorus=0, sustain=1.6) for i in range(3)]
LEAD = S.track("リードギター", "distGuitar", **{**lead_gtr_spec(0.1, -0.1), "powerChord": False})
PNL = S.track("ピアノ（左手）", "piano", volume=0.085, pan=-0.2, reverb=0.25, fx=[{"type": "eq", "low": -3, "mid": -1, "midHz": 400, "high": -1}])
PNR = [S.track(f"ピアノ（右手{i + 1}）", "piano", volume=0.055, pan=-0.15, reverb=0.25, fx=[{"type": "eq", "low": -3, "mid": -2, "midHz": 2600, "high": 0}]) for i in range(3)]
GLK = S.track("冬の鈴（グロッケン）", "glockenspiel", volume=0.07, pan=0.25, reverb=0.45)
SPC = [S.track(f"弦の刻み（スピッカート）{i + 1}", "strings", patch="stringsSpiccato", volume=0.05, pan=-0.5 + 1.0 * i, reverb=0.3) for i in range(2)]
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.04, pan=-0.45 + 0.45 * i, reverb=0.4, sustain=1.4) for i in range(3)]
BASS = S.track("ベース（指弾き）", "bass", **rock_bass_spec(0.23))
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
# サビの合いことばの節（裏から入る・同じ音の連打・16分の食い）。句は 11・11・10・10 音
VC = ["R:0.5 3':0.5 3':0.25 2':0.25 1':0.5 2':1 3':1", "R:0.25 5:0.25 6:0.5 1':0.5 2':0.5 2':2",
      "R:0.5 3':0.5 3':0.25 2':0.25 1':0.5 5':1 4':1", "3':0.5 2':0.5 1':0.5 2':0.5 3':1.5 R:0.5",
      "R:0.5 4':0.5 5':0.5 6':0.5 5':1 4':0.5 3':0.5", "3':1 2':0.5 1':0.5 2':2",
      "R:0.5 1':0.25 1':0.25 1':0.5 2':0.5 3':0.5 2':0.5 1':1", "6:0.5 5:0.5 1':3"]
VSAD = VC[:6] + ["R:1 2':1 1':1 6:1", "5:3 R:1"]                              # 「ごめんね」: 4音だけ、低く下りる
VAC = ["R:0.5 3':0.5 3':0.25 2':0.25 1':0.5 2':1 3':1", "R:0.25 5:0.25 6:0.5 1':0.5 2':0.5 2':2"]   # アカペラ＝サビの1句目
# Aメロ: 低い音域の同音連打と16分の語り。句のあとの2拍はギターが答える
VA = ["R:0.5 1:0.25 1:0.25 1:0.5 2:0.5 3:0.5 2:0.5 1:0.5 R:0.5", "2:0.5 1:0.5 2:1 R:2",
      "R:0.5 3:0.25 3:0.25 3:0.5 4:0.5 5:0.5 4:0.5 3:0.5 R:0.5", "4:0.5 3:0.5 2:1 R:2",
      "R:0.5 5:0.25 5:0.25 5:0.5 6:0.5 1':0.5 6:0.5 5:0.5 R:0.5", "6:0.5 5:0.5 4:0.5 3:0.5 R:2",
      "R:0.5 3:0.5 4:0.5 5:0.5 3:1 2:1", "1:2 R:2"]
# Bメロ: 長い音で1拍ずつ上る。最後は E5 を1拍だけ鳴らして、全員止まる
VB = ["R:1 4:1 5:1 6:1", "1':2 7:1 R:1", "R:1 5:1 6:1 7:1", "2':2 1':1 R:1",
      "R:1 6:1 7:1 1':1", "3':2 2':1 R:1", "R:0.5 2':0.5 2':0.5 3':0.5 4':1 4':1", "5':1 R:3"]
VCM = ["R:1 1':1 1':1 2':1", "3':3 R:1", "R:1 2':1 1':1 6:1", "5:3 R:1",
       "R:1 1':1 2':1 3':1", "5':2 4':1 R:1", "R:1 3':1 2':1 1':1", "2':3 R:1"]
ZA = "ふゆのよるにきみをよぶ"
C1 = ("ふゆのよるにきみをよぶ/こごえたこえがこぼれた/すきといえたはじめて/しろいいきがきえてく/"
      "ふゆのよるにきみはいう/やさしいめでうつむいて/ありがとうでもいまは/ごめんね")
C2 = ("ふゆがくるまでにかわる/きのうのわたしをこえる/だれのためでもなくて/わたしのためにはしる/"
      "ふゆがくるまでにかわる/ころんだかずだけつよく/なりたいからかおあげ/つぎのふゆまではしれ")
C3 = ("ふゆのよるにまたここで/こごえないこえでいうよ/すきだよともういちど/しろいいきがかがやく/"
      "ふゆのよるにきみがいう/こたえはまだいらないよ/いまはただとどけたい/ことしのわたしのこえ/"
      "ふゆのよるにきみをよぶ/こごえたこえはもうない/すきだよともういちど/しろいいきのむこうへ")
OC = "ふゆのよるにまたきたよ/いちねんぶんのことばを/こわいけれどいわせて/しろいいきにのせるよ"
A1 = ("えきのまえのひかりに/かぜがほほをさしてく/てぶくろのなかでにぎった/ことばのたね/"
      "なんどもれんしゅうした/さいしょのひとことだけ/きみがふりむくまえにね/いきをすうの")
A2 = ("はるにかみをきってみた/なつのあさははしるの/にがてなこともいちから/やりなおした/"
      "あきのそらはたかくて/かがみのなかのわたし/すこしだけかおをあげた/まえをむいた")
B1 = "ほしのした/きみがくる/あとすこし/いまいわなきゃ"
B2 = "ふゆがくる/またおなじ/あのみちへ/こんどこそね"
CMT = "ひととせ/このみち/しろいいき/きみのせ"
LY = Lyrics(S)


def put(name, key, lines, text, o=3):
    if name not in [x[0] for x in S.scenes]: return
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("アカペラ", K, VAC, ZA)
put("Aメロ1", K, VA + VA, A1)
put("Bメロ1", K, VB, B1)
put("サビ1", K, VC + VSAD, C1)
put("Aメロ2", K, VA + VA, A2)
put("Bメロ2", K, VB, B2)
put("サビ2", K, VC + VC, C2)
put("Cメロ", K, VCM, CMT)
put("落ちサビ", KL, VC, OC)
put("最後のサビ", KL, VC + VC + VC, C3)


def has(n): return n in [x[0] for x in S.scenes]


# ================= ギター =================
def gtr(b, pat):
    """左右のギター（パワーコード・ダブル）。根音を書くと、1本の中で5度とオクターブが鳴る。
    pat: drive＝ダウン中心の8分（1拍目と2拍目の裏にアクセント・4拍目の裏はのばして次へ）／push＝食いの8分（4拍目の裏から次の小節へ）
         ring＝のばす（全音符）／half＝2分で2回／stab＝1拍目だけ短く（キメ）／riff＝イントロのリフの土台"""
    r = nm(low(S.chords[b].split("/")[0], "E2"))
    P_ = {"drive": f"{r}:0.5! {r}:0.5 {r}:0.5 {r}:0.5! {r}:0.5 {r}:0.5 {r}:0.5 {r}:0.5",
          "push": f"{r}:0.5! {r}:0.5 {r}:0.5 {r}:0.5! {r}:0.5 {r}:0.5 {r}:1",
          "ring": f"{r}:4!", "half": f"{r}:2! {r}:2", "stab": f"{r}:0.5! R:3.5",
          "riff": f"{r}:0.75! {r}:0.75 {r}:0.5! R:0.5 {r}:0.5 {r}:1"}[pat]
    GTR.bar(b, P_)


def clean_arp(b, ch, shape=(0, 2, 1, 2, 3, 2, 1, 2)):
    """分散和音を3本で受けもち、各音を次にその弦が鳴るまでのばす（弦が残って響く）"""
    t = tones(ch.split("/")[0], "E3", "E5")
    seq = [t[k % len(t)] for k in shape]
    lanes = [[] for _ in range(3)]
    for q, m in enumerate(seq):
        lanes[q % 3].append((q * 0.5, m))
    for j in range(3):
        toks = []; cur = 0.0; ev = lanes[j]
        for k, (st, m) in enumerate(ev):
            if st > cur: toks.append(f"R:{st - cur:g}")
            end = ev[k + 1][0] if k + 1 < len(ev) else 4.0
            toks.append(f"{nm(m)}:{end - st:g}{'!' if st == 0 else ''}"); cur = end
        CL[j].bar(b, " ".join(toks))


RIFF = ["F#4:0.25 R:0.25 A4:0.25 C#5:0.25 R:0.25 B4:0.25 A4:0.5 C#5:0.5 E5:0.5 C#5:0.25 B4:0.25 A4:0.5",
        "D5:0.75 C#5:0.75 B4:0.5 A4:0.5 B4:0.5 C#5:1",
        "E5:0.25 R:0.25 E5:0.25 F#5:0.25 R:0.25 E5:0.25 C#5:0.5 B4:0.5 A4:0.5 B4:0.5 C#5:0.5",
        "B4:0.5 A4:0.5 G#4:1 E4:1^ R:1"]
OBB = ["R:2 C#5:0.5 E5:0.5 F#5:1~", "R:2.5 E5:0.25 C#5:0.25 B4:1", "R:2 A5:0.5 F#5:0.5 E5:1~", "R:3 C#5:0.5 B4:0.5"]
SOLO = ["F#4:0.5 A4:0.5 C#5:0.5 E5:0.5 F#5:1.5^ E5:0.5", "C#5:0.5 B4:0.5 A4:0.5 B4:0.5 C#5:2~",
        "E5:0.25 F#5:0.25 E5:0.25 C#5:0.25 B4:0.5 A4:0.5 B4:0.5 C#5:0.5 E5:1", "F#5:2^^~ E5:1 C#5:1",
        "A5:0.5 F#5:0.5 E5:0.5 C#5:0.5 E5:0.5 F#5:0.5 A5:1", "B5:1.5^ A5:0.5 F#5:1 E5:1",
        "C#5:0.25 E5:0.25 F#5:0.25 A5:0.25 B5:0.5 A5:0.5 F#5:0.5 E5:0.5 C#5:1", "E5:4~"]


def piano(b, ch, style):
    r = low(ch.split("/")[0], "E2"); bs = ch.split("/")[1] if "/" in ch else None
    if bs: r = low(bs, "E2")
    v = voice(ch.split("/")[0], 65, 3)
    if style == "drive":
        PNL.bar(b, f"{nm(r)}:1.5 {nm(r + 12)}:0.5 {nm(r)}:1 {nm(r + 12)}:1")
        for j in range(3): PNR[j].bar(b, f"{nm(v[j])}:1.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:1.5")
    elif style == "soft":
        PNL.bar(b, f"{nm(r)}:4")
        for j in range(3): PNR[j].bar(b, f"{nm(v[j])}:4")
    elif style == "half":
        PNL.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2")
        for j in range(3): PNR[j].bar(b, f"R:0.5 {nm(v[j])}:1.5 R:0.5 {nm(v[j])}:1.5")


def strings(b, ch, c=66):
    v = voice(ch.split("/")[0], c, 3)
    for j in range(3): STR[j].bar(b, f"{nm(v[j])}:4")


def spic(b, ch):
    t = tones(ch.split("/")[0], "A3", "A4")
    for j in range(2):
        seq = [t[(q + j) % len(t)] for q in (0, 1, 2, 1, 0, 1, 2, 1)]
        SPC[j].bar(b, " ".join(f"{nm(m)}:0.5{'!' if q % 2 == 0 else ''}" for q, m in enumerate(seq)))


GLK_IN = ["C#6:0.5 E6:0.5 F#6:1 E6:0.5 C#6:0.5 B5:1", "A5:1 B5:0.5 C#6:0.5 E6:2"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "アカペラ":
        continue                                    # 声だけ
    elif n in ("イントロ", "間奏"):
        gtr(b, "riff"); LEAD.bar(b, RIFF[i % 4] if (n == "イントロ" or i < 4) else SOLO[i])
        piano(b, ch, "drive")
        if i >= 4: GLK.bar(b, GLK_IN[i % 2])
    elif n == "Aメロ1":
        clean_arp(b, ch)
        if i % 2 == 1: LEAD.bar(b, ["R:2 A4:0.5 C#5:0.5 B4:1", "R:2 C#5:0.5 E5:0.5 D5:1", "R:2 E5:0.5 F#5:0.5 E5:1", "R:3 C#5:1"][(i // 2) % 4] if i % 8 != 7 else "R:4")
        if i % 8 == 7: gtr(b, "stab")                # キメ
        if i >= 8: piano(b, ch, "half")
    elif n == "Aメロ2":                              # 季節が4小節ごとに変わる（春＝鈴・夏＝刻み・秋＝弦の刻み・冬の手前＝全部）
        season_ = i // 4
        clean_arp(b, ch)
        if season_ == 0: GLK.bar(b, ["R:2 E6:0.5 C#6:0.5 A5:1", "R:2 F#6:0.5 E6:0.5 C#6:1"][i % 2])
        if season_ == 1: gtr(b, "push")
        if season_ == 2: spic(b, ch)
        if season_ == 3: gtr(b, "drive"); spic(b, ch); piano(b, ch, "half")
    elif n in ("Bメロ1", "Bメロ2"):
        gtr(b, "ring" if i < 4 else ("half" if i < 7 else "stab"))
        strings(b, ch, 62 + i)
        if n == "Bメロ2": spic(b, ch)
        piano(b, ch, "half" if i < 7 else "soft") if i < 7 else None
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        sad = n == "サビ1" and i >= 14
        if sad:
            piano(b, ch, "soft")
            continue
        gtr(b, "drive" if i % 4 != 3 else "push")
        piano(b, ch, "drive"); strings(b, ch, 68 if n == "最後のサビ" else 66)
        if n in ("サビ2", "最後のサビ") and i % 2 == 1: LEAD.bar(b, OBB[(i // 2) % 4])
        if n == "最後のサビ": spic(b, ch)
        if n == "最後のサビ" and i % 8 == 0: GLK.bar(b, "A6:2 F#6:2")
    elif n == "ためいき":
        piano(b, ch, "soft") if i < 2 else (clean_arp(b, ch))
    elif n == "Cメロ":
        clean_arp(b, ch); strings(b, ch, 62)
        gtr(b, "ring" if i % 2 == 0 else "half") if i >= 4 else None
    elif n == "落ちサビ":
        piano(b, ch, "soft"); strings(b, ch, 62)
        if i >= 4: clean_arp(b, ch)
    elif n == "白い息":
        if i == 0: piano(b, ch, "soft"); GLK.bar(b, "D6:4")

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; nb_ = ch.split("/")[1] if "/" in ch else ch
    r = low(nb_, "E1")
    if n in ("アカペラ", "白い息"): continue
    if n == "サビ1" and i >= 14: continue
    if n in ("Aメロ1",) and i < 4: BASS.bar(b, f"{nm(r)}:4"); continue
    if n in ("Aメロ1", "Aメロ2"): BASS.bar(b, f"{nm(r)}:1.5 {nm(r)}:0.5 R:0.5 {nm(r)}:1 {nm(r + 12)}:0.5" if i % 8 != 7 else f"{nm(r)}:0.5 R:3.5"); continue
    if n in ("Bメロ1", "Bメロ2"): BASS.bar(b, f"{nm(r)}:4" if i < 4 else (f"{nm(r)}:2 {nm(r)}:2" if i < 7 else f"{nm(r)}:0.5 R:3.5")); continue
    if n == "ためいき": BASS.bar(b, f"{nm(r)}:4" if i >= 2 else "R:4"); continue
    if n == "Cメロ": BASS.bar(b, f"{nm(r)}:2 {nm(r + 7)}:2"); continue
    if n == "落ちサビ": BASS.bar(b, f"{nm(r)}:4" if i >= 4 else "R:4"); continue
    if n in ("イントロ", "間奏"): BASS.bar(b, f"{nm(r)}:0.75 {nm(r)}:0.75 {nm(r)}:0.5 R:0.5 {nm(r)}:0.5 {nm(r + 12)}:1"); continue
    BASS.bar(b, bass_line(S, b, "oct8" if i % 4 != 3 else "push", lo="E1"))

for name in ("サビ1", "サビ2", "最後のサビ"):
    if has(name): cym_swell(CYM, S.sc(name)[0], 2, "C4")

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("アカペラ", "白い息"):
        if n == "白い息" and i == 0: crash(D, b, "C2", 8)
        continue
    if n in ("イントロ", "間奏"):
        D.set(b, "X.....X...X.....", "....X.......X...", "x.x.x.x.x.x.x.x.")      # リフのアクセント（1・2拍目の裏・3拍目）にキックを合わせる
        if i == 0: crash(D, b, "C2", 6)
        if i == 4: crash(D, b, "C2", 4)
        if last: put_fill(D, b, "tomdown")
        continue
    if n in ("Aメロ1", "Aメロ2"):
        if n == "Aメロ2" and i // 4 == 1: vgroove(D, b, "punk", ghosts=0.2, seed=b)
        elif n == "Aメロ1" and i < 4: D.set(b, "X.......X.......", "................", "x.x.x.x.x.x.x.x.")
        else: vgroove(D, b, "beat8", ghosts=0.3, seed=b)
        if i % 8 == 7: D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 4)   # キメ
        elif i % 4 == 3: put_fill(D, b, "small")
        continue
    if n in ("Bメロ1", "Bメロ2"):
        if i < 4: D.set(b, "X.......X.......", "........X.......", "................"); D.R.bar(b, "D2:1 D2:1 D2:1 D2:1")
        elif i < 7: vgroove(D, b, "halfdrive", ghosts=0.25, seed=b)
        if i == 6: put_fill(D, b, "snare16")
        if last: halt(D, b, 1)                       # 1拍だけ鳴らして、全員止まる
        continue
    if n in ("サビ1", "サビ2", "最後のサビ"):
        if n == "サビ1" and i >= 14:
            if i == 14: crash(D, b, "C2", 8)
            continue
        vgroove(D, b, "vrock", ghosts=0.15, seed=b)
        if i % 8 == 0: crash(D, b, "C2", 7 if (n == "最後のサビ" and i == 0) else 5)
        if i % 8 == 7 and not last: put_fill(D, b, "tomtrip" if i % 16 == 15 else "tomdown")
        elif i % 4 == 3: put_fill(D, b, "small")
        if n == "最後のサビ" and last: halt(D, b, 1)
        continue
    if n == "ためいき":
        if i >= 2: D.set(b, "X...............", "................", "................")
        if last: put_fill(D, b, "lift")
        continue
    if n == "Cメロ":
        D.set(b, "X.......X.......", "....x.......x...", "................"); D.R.bar(b, "D2:1 D2:1 D2:1 D2:1")
        if last: put_fill(D, b, "snare16")
        continue
    if n == "落ちサビ":
        if i >= 4: D.set(b, "X.........X.....", "................", "................"); D.R.bar(b, "D2:2 D2:2")
        if last: put_fill(D, b, "build")

for name in ("Bメロ1", "Bメロ2"):
    if has(name): SIL.add(S.sc(name)[-1], 1, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: プロ仕様のボカロ曲（重音テト）02。v1 を作り直し。冬のボカロック。F#m（A長調）・168、最後のサビは +1。"
          "アカペラ2小節で始まり、サビは合いことばの節（裏から入る・同音連打・16分の食い）を4回くり返す。「ごめんね」でバンドが止まる。"
          "左右のギターはパワーコードのダブル、Aメロは弦が残る分散和音、リードはリフ・オブリ・ソロ。2番のAメロは季節ごとに楽器が入れかわる。自作")
finish(S, LY, V, 0,
       level={"verse": -0.2}, special={"アカペラ": -0.1, "落ちサビ": -0.3, "最後のサビ": 0.4, "サビ1": 0.3})
