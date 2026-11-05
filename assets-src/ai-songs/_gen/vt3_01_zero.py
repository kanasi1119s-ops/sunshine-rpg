# vt3 01「ハッピーバースデー・ゼロ」Happy Birthday, Zero（仮）— フューチャーファンク。118・4/4。F#m（Aメロ）→ A（サビ）→ 最後のサビは +1（B♭）。書き出しは全体を半音下げる（テトの声に入れるため・A♭/A）。
# 第3弾『HUMMING RELAY』（仮）は「ひとつの街の 0時から24時まで」。この曲は 23時50分〜0時。表は docs/sound/vt3-plan.md。
# 物語: 親友の誕生日の前の夜。日付が変わる瞬間に、だれよりも先に「おめでとう」を言いたい「わたし」。
#   打っては消すメッセージ。机には、自分で買った小さなカップケーキとろうそく1本。去年はきみが、わたしより先に言ってくれた。
#   秒読み → 0時ちょうど（1拍の無音）→ 送信。既読がついて、「いちばんだったよ」と返ってくる。ろうそくを吹き消して終わる。
#   （鼻歌の節はまだ無い。2曲目の深夜ラジオで生まれる）
# 場面と強さ: 秒針（時計の音だけ・弱）→ イントロ（こもったディスコの輪 → 開く・中）→ Aメロ1（語る・弱〜中）→ Bメロ1（ためる）
#   → サビ1（強）→ 間奏 → Aメロ2 → Bメロ2 → サビ2（強）→ 間奏2（スラップとストリングス）→ 秒読み（時計の音と数を数える声だけ・とても弱）
#   → 1拍の無音（0時）→ 最後のサビ（+1・いちばん強い・24小節）→ ろうそく（和音 → 吹き消す息）
# 旋律の性格: Aメロははずむ16分のつまった言葉（A3〜B4）、サビは「はっぴーばーすでー」の8分の連なり（C#5 中心）から、後半で F#5 まで上がる。
#   有名な誕生日の歌の節とは、高さもリズムもまったく別にした（4分の3拍子の上り下りは使わない）。
# この曲だけの音: 秒針の「カチ」が、そのまま曲の拍になる（始まりと秒読み）。最後は、ろうそくを吹き消す息（ホワイトノイズの「シュッ」）。
from vt25_lib import *

S = Song("01", "zero", "ハッピーバースデー・ゼロ（仮）", "Happy Birthday, Zero", 118, 4, "A", "major", "フューチャーファンク（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --space room --space-wet 0.12"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.6
S.keepers = {"Aメロ1": "closed", "Aメロ2": "closed", "サビ2": "open", "最後のサビ": "open"}
K = Key("A", "major")          # oct 3 で 1 = A3（Aメロ・Bメロ）、oct 4 で 1 = A4（サビ）
KL = Key("Bb", "major")        # 最後のサビ（+1）

INTRO = ["Dmaj9", "C#m7", "Bm9", "E7sus4"]
A_CH = ["F#m9", "Bm9", "E7sus4", "Amaj7", "F#m9", "Bm9", "Dmaj7", "E7sus4"]
B_CH = ["Dmaj7", "E/D", "C#m7", "F#m7", "Bm7", "C#m7", "Dmaj7", "E7sus4"]
C_CH = ["Dmaj9", "E6", "C#m7", "F#m9", "Bm9", "E9", "Amaj9", "A7", "Dmaj9", "E6", "C#m7", "F#m9", "Bm9", "C#m7", "Dmaj9", "E7sus4"]
LAST = [tr_chord(c, 1) for c in C_CH]

S.scene("秒針", 4, "intro", ["F#m9", "F#m9", "Dmaj9", "E7sus4"])
S.scene("イントロ", 8, "intro", INTRO * 2)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 4, "break", INTRO)
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("間奏2", 8, "solo", INTRO * 2)
S.scene("秒読み", 4, "bridge", ["Dmaj9", "C#m7", "Bm9", "F7sus4"])     # 最後の小節は B♭ への入り口
S.scene("最後のサビ", 24, "chorus", LAST + LAST[:8])
S.scene("ろうそく", 4, "outro", ["Ebmaj9", "F6", "Dm7", "Bbmaj9"])

V = Voice(S, vol=0.21, delay=0.75, bright=0.0, patch="surgeDnaSeq", low=False)
# v3: v1 7.16・v2 7.21（サビを薄くしても変わらない）→ 音色を変える。FM のエレピ → エレピ（DX）、スラップ → 指弾き
EP = [S.track(f"エレピ{i + 1}", "keys", patch="surgeKeysDxEp", volume=0.07, pan=-0.35, reverb=0.25, sustain=0.8,
              fx=[{"type": "eq", "low": -3, "mid": 0, "midHz": 700, "high": 1}]) for i in range(4)]
STR = [S.track(f"ディスコのストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.06, pan=0.45, reverb=0.35, sustain=0.9) for i in range(3)]
STRL = S.track("ストリングス（上がる節）", "strings", patch="stringEnsemble", volume=0.075, pan=-0.2, reverb=0.35, sustain=0.8)
BR = [S.track(f"ブラスのスタブ{i + 1}", "brass", patch="brassSection", volume=0.055, pan=0.2, reverb=0.25, sustain=0.4) for i in range(3)]
CUT = [S.track(f"カッティングギター{i + 1}", "guitar", amp="jpopClean", volume=0.05, pan=-0.6, reverb=0.15, chorus=0, sustain=0.3) for i in range(3)]
BASS = S.track("ベース（指弾き）", "bass", **finger_bass_spec(vol=0.22))
PAD = [S.track(f"うねるパッド{i + 1}", "pad", **pad_spec("surgePadHineVertigo", vol=0.035, pan=-0.5 + 0.5 * i, duck=0.45, sustain=1.4)) for i in range(3)]
CHOP = S.track("声のチョップ風", "pad", patch="vocalChop", volume=0.06, pan=0.3, reverb=0.3, sustain=0.5,
               fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.2, "feedback": 0.3}])
TICK = S.track("秒針（カホンの縁）", "cajon", volume=0.08, pan=0.15, reverb=0.1)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.06, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:0.5 3:0.25 3:0.25 3:0.5 5:0.5 6:0.75 5:0.25 3:0.5 R:0.5", "3:0.5 2:0.5 2:0.75 3:0.25 3:1 R:1",
      "R:0.5 3:0.25 3:0.25 3:0.5 5:0.5 1':0.75 7:0.25 6:0.5 R:0.5", "5:0.5 6:0.5 5:0.75 3:0.25 2:1 R:1",
      "R:0.5 6:0.25 6:0.25 6:0.5 1':0.5 2':0.75 1':0.25 6:0.5 R:0.5", "5:0.5 3:0.5 5:0.75 6:0.25 6:1 R:1",
      "R:0.5 4:0.5 4:0.5 3:0.5 2:0.5 3:0.5 4:0.5 R:0.5", "5:1.5 #4:0.5 5:1 R:1"]
A1 = ("ろうそくいっぽん/まどのそば/うってはけしてる/おめでとう/あとじゅっぷんだよ/どきどきだ/いちばんにね/とどけ/"
      "きみのとくべつ/ひがくるよ/すたんぷじゃだめ/ことばでね/こごえでいうの/てれるけど/ぜろじちょうど/まってて")
A2 = "けんかもしたね/ゆきのひも/かさわすれたひ/てまねきで/ぜんぶまとめて/ひとことに/のこりいっぷん/いくよ"
VB = ["R:0.5 1':0.5 1':0.5 7:0.5 6:0.75 5:0.25 5:0.5 R:0.5", "6:0.5 5:0.5 4:0.5 3:0.5 3:1 R:1",
      "R:0.5 2':0.5 2':0.5 1':0.5 7:0.75 6:0.25 6:0.5 R:0.5", "7:0.5 1':0.5 2':0.5 3':0.5 3':1 R:1",
      "R:0.5 4':0.5 3':0.5 2':0.5 1':0.75 7:0.25 6:0.5 R:0.5", "5:0.5 6:0.5 7:0.5 1':0.5 2':1 R:1",
      "R:0.5 3':0.5 3':0.5 3':0.5 3':0.5 2':0.5 1':0.5 2':0.5", "3':3 R:1"]
B1 = "がめんのなか/きみのかお/きょねんのきみ/ろうそくに/ふきけしてた/ことしはね/さきにいわせてね"
B2 = "とけいのはり/かさなるよ/ゆびがふるえ/そうしんの/ぼたんのうえ/いきとめて/だれよりもはやく"
VC = ["R:0.5 3:0.5 3:0.25 2:0.25 3:0.5 5:0.5 5:0.5 6:0.5 5:0.5", "3:1 2:0.5 1:1 R:1.5",
      "R:0.5 6,:0.5 1:0.5 2:0.5 3:0.5 2:0.5 1:0.5 2:0.5", "3:2 R:2",
      "R:0.5 3:0.5 3:0.25 2:0.25 3:0.5 5:0.5 5:0.5 6:0.5 5:0.5", "6:1 5:0.5 3:1 R:1.5",
      "R:0.5 4:0.5 4:0.5 3:0.5 2:0.5 2:0.5 3:0.5 2:0.5", "1:2 R:2",
      "R:0.5 5:0.5 5:0.5 6:0.5 5:0.5 3:0.5 2:0.5 3:0.5", "5:1 6:1 5:1 R:1",
      "R:0.5 3:0.5 3:0.5 4:0.5 3:0.5 2:0.5 1:0.5 2:0.5", "3:2 R:2",
      "R:0.5 5:0.5 6:0.5 6:0.5 6:0.5 5:0.5 6:0.5 5:0.5", "6:1.5 5:0.5 3:1 R:1",
      "R:0.5 2:0.5 3:0.5 2:0.5 1:0.5 6,:0.5 1:0.5 2:0.5", "1:3 R:1"]
C1 = ("はっぴーばーすでーきみへ/ひとりめはわたし/はっぴーばーすでーぜろの/あいずでおくるよ/"
      "きのうときょうのすきま/まっすぐかけぬけて/だれもいないあしたへ/さきまわりするよ")
C2 = ("はっぴーばーすでーきみへ/まだいえないけど/はっぴーばーすでーぜろの/かねがなるまでは/"
      "てのひらでまつでんぱ/はーとをそえるよ/あとすこしでひづけが/かわるしゅんかんに")
CL = ("はっぴーばーすでーきみへ/いまとどいたかな/はっぴーばーすでーぜろの/きどくがついたよ/"
      "かえってきたへんじには/いちばんだったよって/ろうそくふきけしたら/らいねんもいうよ/"
      "はっぴーばーすでーきみへ/うまれてくれてね/はっぴーばーすでーぜろの/ありがとうきみに")
COUNT = ["R:2 5:0.5 5:0.5 5:0.5 5:0.5", "5:0.5 5:0.5 5:0.5 5:0.5 5:0.5 5:0.5 5:1", "5:0.5 5:0.5 5:0.5 5:0.5 5:1 1':0.5 1':0.5", "R:4"]
LY = Lyrics(S)


def put(name, key, lines, text, o=4):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA + VA, A1, o=3)
put("Bメロ1", K, VB, B1, o=3)
put("サビ1", K, VC, C1)
put("Aメロ2", K, VA, A2, o=3)
put("Bメロ2", K, VB, B2, o=3)
put("サビ2", K, VC, C2)
put("秒読み", K, COUNT, "じゅうきゅうはちななろくごよんさんにいち", o=3)
put("最後のサビ", KL, VC + VC[:8], CL)

# ================= 和音の楽器 =================
def ep_comp(b, ch, style):
    v = voice(ch, 64, 4)
    if style == "pad": pat = [f"{nm(x)}:4" for x in v]
    elif style == "push": pat = [f"R:1.5 {nm(x)}:0.5 R:1 {nm(x)}:1" for x in v]
    else: pat = [f"{nm(x)}:0.75 R:0.75 {nm(x)}:0.5 R:1 {nm(x)}:0.5 R:0.5" for x in v]   # はずむ刻み
    for j in range(4): EP[j].bar(b, pat[j])


def strum16(b, ch, pat="..x...x...x.x.x."):
    v = voice(ch, 62, 3)
    hits = [q for q, c in enumerate(pat) if c == "x"]
    for j in range(3):
        toks, t = [], 0
        for q in hits:
            if q > t: toks.append(f"R:{(q - t) * 0.25:g}")
            toks.append(f"{nm(v[j])}:0.25"); t = q + 1
        if t < 16: toks.append(f"R:{(16 - t) * 0.25:g}")
        CUT[j].bar(b, " ".join(toks))


def stabs(b, ch, pat):
    v = voice(ch, 67, 3)
    for j in range(3): BR[j].bar(b, " ".join(t.replace("x", nm(v[j])) for t in pat.split()))


def strings_long(b, ch, center=72):
    v = voice(ch, center, 3)
    for j in range(3): STR[j].bar(b, f"{nm(v[j])}:4")


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "秒針":
        if i >= 2: ep_comp(b, ch, "pad")
    elif n == "イントロ":
        # v4: イントロの前半が 6.25 → 前半からパッドを入れる
        ep_comp(b, ch, "bounce"); strum16(b, ch)
        for j in range(3): PAD[j].bar(b, f"{nm(voice(ch, 60, 3)[j])}:4")
        if i >= 4: strings_long(b, ch)
        if i in (3, 7): CHOP.bar(b, "R:2 E5:0.5 C#5:0.5 B4:0.5 A4:0.5")
    elif n in ("Aメロ1", "Aメロ2"):
        ep_comp(b, ch, "push" if i % 4 != 3 else "bounce")
        if n == "Aメロ2" or i >= 8: strum16(b, ch, "..x...x...x...x.")
    elif n in ("Bメロ1", "Bメロ2"):
        ep_comp(b, ch, "bounce"); strum16(b, ch, "..x.x.x...x.x.x.")
        strings_long(b, ch, 70)
        for j in range(3): PAD[j].bar(b, f"{nm(voice(ch, 60, 3)[j])}:4")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        # v2: サビの点数が 6.7〜7.1。楽器が重なりすぎ（パッド・エレピの刻み・ギター・弦・ブラス）→ パッドを外し、エレピは押しだけ、ブラスは2小節に1回
        ep_comp(b, ch, "push"); strum16(b, ch, "..x...x...x...x.")
        strings_long(b, ch, 70)
        if i % 2 == 1: stabs(b, ch, "R:3.5 x:0.25 R:0.25")
        if i % 8 == 7:   # 句の終わりに、ストリングスが1オクターブ駆け上がる
            t = tones(ch, "C5", "C6"); STRL.bar(b, "R:2 " + " ".join(f"{nm(x)}:0.25" for x in (t * 3)[:8]))
    elif n == "間奏":
        ep_comp(b, ch, "bounce"); strum16(b, ch)
        CHOP.bar(b, "R:0.5 A4:0.5 C#5:0.5 E5:0.5 R:1 F#5:0.5 E5:0.5" if i % 2 == 0 else "C#5:1 B4:0.5 A4:0.5 R:2")
    elif n == "間奏2":
        ep_comp(b, ch, "push"); strum16(b, ch, "x.x...x.x.x...x.")
        strings_long(b, ch, 72)
        # ストリングスの節（ディスコのソロ）
        SOLO = ["R:0.5 E5:0.5 F#5:0.5 A5:0.5 G#5:1 E5:1", "F#5:1.5 E5:0.5 C#5:1 R:1", "R:0.5 D5:0.5 E5:0.5 F#5:0.5 A5:1 B5:1", "G#5:3 R:1",
                "R:0.5 E5:0.5 F#5:0.5 A5:0.5 C#6:1 B5:1", "A5:1.5 F#5:0.5 E5:1 R:1", "R:0.5 D5:0.5 C#5:0.5 B4:0.5 C#5:1 E5:1", "E5:2 G#5:2"]
        STRL.bar(b, SOLO[i])
    elif n == "秒読み":
        if i < 3:
            v = voice(ch, 62, 4)
            for j in range(4): EP[j].bar(b, f"{nm(v[j])}:4")
    elif n == "ろうそく":
        if i < 3:
            ep_comp(b, ch, "pad"); strings_long(b, ch, 70)
            for j in range(3): PAD[j].bar(b, f"{nm(voice(ch, 60, 3)[j])}:4")
        else:
            v = voice(ch, 64, 4)
            for j in range(4): EP[j].bar(b, f"{nm(v[j])}:2.5 R:1.5")
            strings_long(b, ch, 70)

# v2: こもらせたイントロの前半は 5.98 → こもらせるのをやめ、前半はエレピとギターだけにする

# ================= 秒針（カホンの縁「カチ」）=================
for b in S.sc("秒針"): TICK.bar(b, "E3:1 E3:1 E3:1 E3:1")
for b in S.sc("秒読み")[:3]: TICK.bar(b, "E3:1 E3:1 E3:1 E3:1")
TICK.bar(S.sc("秒読み")[3], "E3:1 E3:1 E3:1 R:1")

# ================= ベース（スラップ）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "イントロ": BASS.bar(b, bass_line(S, b, "long" if i < 4 else "oct8", lo="E1"))
    elif n in ("Aメロ1", "Aメロ2"): BASS.bar(b, bass_line(S, b, "push" if i % 4 != 3 else "oct8", lo="E1"))
    elif n in ("Bメロ1", "Bメロ2"): BASS.bar(b, bass_line(S, b, "oct8", lo="E1"))
    elif n in ("サビ1", "サビ2", "最後のサビ", "間奏", "間奏2"): BASS.bar(b, bass_line(S, b, "oct8" if i % 4 != 3 else "push", lo="E1"))   # v4: 16分のオクターブ → 8分
    elif n == "ろうそく" and i < 3: BASS.bar(b, bass_line(S, b, "long", lo="E1"))

# ================= 効果音 =================
riser(FX, S.sc("サビ1")[0], 4, "C4"); riser(FX, S.sc("サビ2")[0], 4, "C4")
cym_swell(CYM, S.sc("イントロ")[4], 2, "C4"); cym_swell(CYM, S.sc("Aメロ1")[0], 2, "C4")
FX.bar(S.sc("ろうそく")[3], "R:2.5 A4:1.5")          # ろうそくを吹き消す息（ホワイトノイズの「シュッ」）

# ================= ドラム =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "イントロ":
        if i < 4: vgroove(D, b, "four", ghosts=0, seed=b, s="................", h="x.x.x.x.x.x.x.x.")
        else: vgroove(D, b, "four", ghosts=0.2, seed=b)
        if i == 4: crash(D, b)
        if i == 7: put_fill(D, b, "snare16")
    elif n in ("Aメロ1", "Aメロ2"):
        vgroove(D, b, "four" if i % 8 < 4 else "disco", ghosts=0.3, seed=b)
        if i == 0: crash(D, b)
        if i % 8 == 7 and not last: put_fill(D, b, "small")
        if last: put_fill(D, b, "lift")
    elif n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "halfdrive" if i < 4 else "four16", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 1)
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        # v4: サビは 7.0 前後のまま → 16分のハイハット（disco）をやめ、間奏2（8.0）に近い軽い刻みに
        vgroove(D, b, "four", ghosts=0.25, seed=b, h="x.x.x.x.x.x.x.x.")
        if i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
        if i % 8 == 7 and not last: put_fill(D, b, "tomdown" if i % 16 == 15 else "small")
        if last and n != "最後のサビ": put_fill(D, b, "snare16")
    elif n == "間奏":
        vgroove(D, b, "four16", ghosts=0.3, seed=b)
        if last: put_fill(D, b, "lift")
    elif n == "間奏2":
        vgroove(D, b, "break1" if i % 2 == 0 else "break2", ghosts=0.3, seed=b)
        if i == 0: crash(D, b)
        if last: halt(D, b, 1)
    elif n == "ろうそく":
        if i == 0: crash(D, b, "C2", 6); D.set(b, "X.......X.......", "........X.......", "x.x.x.x.x.x.x.x.")
        elif i < 3: D.set(b, "X.......X.......", "........X.......", "x.x.x.x.x.x.x.x.")

# 止め: Bメロの最後。0時ちょうどの1拍の無音（最後のサビの直前の拍）
for name in ("Bメロ1", "Bメロ2"): SIL.add(S.sc(name)[-1], 1, 4)
SIL.add(S.sc("秒読み")[-1], 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の01（0時）。フューチャーファンク。F#m（サビは A）・118、最後のサビは +1（B♭）。"
          "親友の誕生日の前の夜、0時ちょうどに「おめでとう」を送る。秒針の音から始まり、秒読みと1拍の無音（0時）のあと最後のサビ。"
          "ろうそくを吹き消す息で終わる。FMエレピ・ディスコのストリングス・ブラスのスタブ・カッティングギター・スラップベース。自作")
finish(S, LY, V, -1,
       level={"verse": -0.2}, special={"秒読み": -0.8, "最後のサビ": 0.4, "ろうそく": -0.2})
