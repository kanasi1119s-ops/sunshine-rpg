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

# v5（2026-11-11 作り直し）人間「電子系音源は Kawaii future bass 系に」: BGM の旋律は brightLead、うねるパッドは fbChord（キックで凹む和音）、
#   きらきらのアルペジオ（kawaiiArp）とベル（popBell）を足す。ギターは CUT（録音の和音を型で鳴らす）をやめ、下で DI ギターを弦ごとに弾く
# v6（2026-11-11 人間「25曲すすめようか。電子系の音は Kawaii_future_bass で」）: 電子の音を、足したカワイイ・フューチャーベースの音に替える。
#   旋律 brightLead → kfbSquareLead／エレピ surgeKeysDxEp → kfbGlassEp／アルペジオ kawaiiArp → kfbSquarePluck／ベル popBell → kfbGlocken／
#   サビに丸いサブベース（kfbSub）／最後のサビにスーパーソー（kfbSupersaw・キックで凹む）／効果音は kawaiiFx（上がる音・インパクト・きらきら・泡）。
#   構成: 間奏2 の前半4小節を「ドロップ」にする（ハーフテンポ・スーパーソーの和音の刻み・声のチョップ・サブベース）。後半4小節で4つ打ちに戻り、ストリングスが歌う
V = Voice(S, vol=0.2, delay=0.75, bright=0.1, patch="kfbSquareLead", low=False)
# v3: v1 7.16・v2 7.21（サビを薄くしても変わらない）→ 音色を変える。FM のエレピ → エレピ（DX）、スラップ → 指弾き
EP = [S.track(f"エレピ{i + 1}", "keys", patch="kfbGlassEp", volume=0.075, pan=-0.35, reverb=0.25, sustain=0.8,
              fx=[{"type": "eq", "low": -3, "mid": 0, "midHz": 700, "high": 1}]) for i in range(4)]
STR = [S.track(f"ディスコのストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.06, pan=0.45, reverb=0.35, sustain=0.9) for i in range(3)]
STRL = S.track("ストリングス（上がる節）", "strings", patch="stringEnsemble", volume=0.075, pan=-0.2, reverb=0.35, sustain=0.8)
BR = [S.track(f"ブラスのスタブ{i + 1}", "brass", patch="brassSection", volume=0.055, pan=0.2, reverb=0.25, sustain=0.4) for i in range(3)]
CUT = [S.track(f"カッティングギター{i + 1}", "guitar", amp="jpopClean", volume=0.05, pan=-0.6, reverb=0.15, chorus=0, sustain=0.3) for i in range(3)]
# v9（2026-11-11 人間「ベースラインで音連打で出している部分が、次の音出す時に引っかかる感じがする」）: 測ると、同じ音を続けて弾く所で、前の音が切れてから
#   次の音が立ち上がるまでに 6〜12ms の穴（−24dB）があいていた → 音を 15% 長くして次の音に重ねる（穴は −11〜−13dB に。休みの所はちゃんと止まる）
BASS = S.track("ベース（指弾き）", "bass", sustain=1.15, **finger_bass_spec(vol=0.22))
PAD = [S.track(f"うねる和音{i + 1}", "lead", patch="fbChord", volume=0.034, pan=-0.4 + 0.4 * i, reverb=0.22, duck=0.55) for i in range(3)]
ARP = S.track("きらきらのアルペジオ", "lead", patch="kfbSquarePluck", volume=0.045, pan=0.35, reverb=0.25, fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.16, "feedback": 0.25}])
SAW = [S.track(f"スーパーソー{i + 1}", "lead", patch="kfbSupersaw", volume=0.05, pan=-0.5 + 0.5 * i, reverb=0.18, duck=0.6,
               fx=[{"type": "filter", "kind": "highpass", "freq": 220, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 9000, "q": 0.6}]) for i in range(3)]
SUB = S.track("サブベース", "bass", patch="kfbSub", volume=0.035, pan=0, duck=0.5)
KFX = S.track("カワイイ効果音", "guitar", patch="kawaiiFx", volume=0.06, pan=0.1, reverb=0.15, modulate=False)
KDR = S.track("電子のクラップ・ハット", "guitar", patch="kawaiiFx", volume=0.07, pan=-0.05, reverb=0.08, modulate=False)
BELL = S.track("ベル（合いの手）", "lead", patch="kfbGlocken", volume=0.05, pan=-0.3, reverb=0.3)
STRH = S.track("ストリングス（1オクターブ上の線）", "strings", patch="stringEnsemble", volume=0.045, pan=0.3, reverb=0.4, sustain=0.9)
CELLO = S.track("チェロ（低い線）", "strings", patch="cello", volume=0.06, pan=-0.15, reverb=0.3, sustain=0.9)
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
    return   # v5: ギターは下の GuitarRig（DI ギター・弦ごと・本物の揺れ方）で弾く
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
        if n == "Aメロ2" and i % 2 == 1:      # v5: 2番は、歌の句の終わり（小節の後半）にベルが答える
            tb = tones(ch, "C#5", "C#6"); BELL.bar(b, f"R:2.5 {nm(tb[-1])}:0.5 {nm(tb[-2])}:0.5 {nm(tb[-3])}:0.5")
    elif n in ("Bメロ1", "Bメロ2"):
        ep_comp(b, ch, "bounce"); strum16(b, ch, "..x.x.x...x.x.x.")
        strings_long(b, ch, 70)
        for j in range(3): PAD[j].bar(b, f"{nm(voice(ch, 60, 3)[j])}:4")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        # v2: サビの点数が 6.7〜7.1。楽器が重なりすぎ（パッド・エレピの刻み・ギター・弦・ブラス）→ パッドを外し、エレピは押しだけ、ブラスは2小節に1回
        # v7: サビ2 6.93・最後のサビ 6.73（重なりすぎ）→ サビのエレピは サビ1 だけ。最後のサビは長いストリングスをやめ（1オクターブ上の線とチェロが弦の役）、ブラスもやめる
        if n == "サビ1": ep_comp(b, ch, "push")
        if n != "最後のサビ": strings_long(b, ch, 70)
        # v5: サビの厚みは、キックで凹むうねる和音（カワイイ・フューチャーベースの「ポンプ」）で作る。エレピの押しは小さく残す
        vv = voice(ch, 62, 3)
        for j in range(3): PAD[j].bar(b, f"{nm(vv[j])}:4")
        if n == "最後のサビ": rs = low(ch, "C1"); SUB.bar(b, f"{nm(rs)}:2.5 R:0.5 {nm(rs)}:1" if i % 2 == 0 else f"{nm(rs)}:3.5 R:0.5")   # v7: サブベースは最後のサビとドロップだけ
        if n == "最後のサビ" and i >= 16:     # v7: スーパーソーは、最後の8小節（くり返しの山）だけ      # 最後だけ、スーパーソーが 8分の裏で押す（i が進むほど長く）
            sv = voice(ch, 69, 3)
            for j in range(3): SAW[j].bar(b, f"{nm(sv[j])}:1.5 {nm(sv[j])}:1 {nm(sv[j])}:1.5" if i % 4 != 3 else f"{nm(sv[j])}:0.75 {nm(sv[j])}:0.75 {nm(sv[j])}:0.5 {nm(sv[j])}:0.75 {nm(sv[j])}:0.75 {nm(sv[j])}:0.5")
        if n == "最後のサビ":
            # スケール: 弦の1オクターブ上の線（和音のいちばん上の音を2分で動かす）と、チェロの低い線（根音→5度）で上下を広げる
            top = voice(ch, 76, 3)[-1]; t2 = tones(ch, nm(top - 5), nm(top + 4))
            # v11（2026-11-11 人間「ピヨピヨ消えてないな」「ストリングスかも？」）: 1オクターブ上のストリングスの線（2分音符で上下する高い音）をやめる。
            #   かわりに、サビ2 と同じ中くらいの高さの長いストリングスに戻す（上はチェロと長い弦で支える）
            strings_long(b, ch, 70)
            r_ = low(ch, "C2"); CELLO.bar(b, f"{nm(r_)}:3 {nm(r_ + 7)}:1")
            ta = tones(ch, "A4", "E6")
            # v10（2026-11-11 人間「最後のサビのヒヨコがピヨピヨ鳴いているみたいな音はいらないかも」）: 2小節に1回、16分で行ったり来たりしつづけるアルペジオをやめる。
            #   気に入ってもらえた サビ2 の形（4小節ごとの最後の小節の後半に、8つ駆け上がる）にする。最後の8小節は 2小節ごと
            if i % 4 == 3 or (i >= 16 and i % 2 == 1): ARP.bar(b, "R:2 " + " ".join(f"{nm(ta[q % len(ta)])}:0.25" for q in ((0, 2, 4, 5, 4, 2, 4, 6) if i % 8 == 3 else (0, 1, 2, 4, 5, 6, 5, 7))))
        elif n == "サビ2" and i % 4 == 3:
            ta = tones(ch, "A4", "E6"); ARP.bar(b, "R:2 " + " ".join(f"{nm(ta[q % len(ta)])}:0.25" for q in (0, 2, 4, 5, 4, 2, 4, 6)))
        if i % 2 == 1 and n != "最後のサビ": stabs(b, ch, "R:3.5 x:0.25 R:0.25")
        if i % 8 == 7:   # 句の終わりに、ストリングスが1オクターブ駆け上がる
            t = tones(ch, "C5", "C6"); STRL.bar(b, "R:2 " + " ".join(f"{nm(x)}:0.25" for x in (t * 3)[:8]))
    elif n == "間奏":
        ep_comp(b, ch, "bounce"); strum16(b, ch)
        CHOP.bar(b, "R:0.5 A4:0.5 C#5:0.5 E5:0.5 R:1 F#5:0.5 E5:0.5" if i % 2 == 0 else "C#5:1 B4:0.5 A4:0.5 R:2")
    elif n == "間奏2":
        if i < 4:     # ドロップ（ハーフテンポ）: スーパーソーの和音の刻み＋声のチョップ＋サブベース
            sv = voice(ch, 67, 3)
            rh = ["x:0.75 x:0.75 x:1 R:0.5 x:0.5 x:0.5", "x:1.5 x:0.5 R:0.5 x:0.75 x:0.75", "x:0.75 x:0.75 x:1 R:0.5 x:0.5 x:0.5", "x:0.5 x:0.5 x:0.5 x:0.5 x:0.25 x:0.25 x:0.25 x:0.25 x:0.25 x:0.25 x:0.25 x:0.25"][i]
            for j in range(3): SAW[j].bar(b, " ".join(t.replace("x", nm(sv[j])) for t in rh.split()))
            rs = low(ch, "C1"); SUB.bar(b, f"{nm(rs)}:3 R:0.5 {nm(rs)}:0.5")
            CHOP.bar(b, ["E5:0.5 R:0.25 E5:0.25 C#5:0.5 R:0.5 A4:0.5 C#5:0.5 E5:1", "R:1 F#5:0.5 E5:0.5 R:0.5 C#5:0.5 B4:0.5 R:0.5", "D5:0.5 R:0.25 D5:0.25 F#5:0.5 R:0.5 A5:0.5 F#5:0.5 D5:1", "R:0.5 E5:0.5 G#5:0.5 B5:0.5 R:2"][i])
            if i == 3: KFX.bar(b, "R:2 F#4:2")          # 上がる音 → 4つ打ちに戻る
            continue
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
    elif n == "間奏2" and i < 4: BASS.bar(b, bass_line(S, b, "long", lo="E1"))      # ドロップは長い音（サブベースと同じ動き）
    elif n in ("サビ1", "サビ2", "最後のサビ", "間奏", "間奏2"):
        # v5: 8分のオクターブの型をやめ、手で書いたファンクの線に（1拍目の頭を長く・16分の裏で跳ねる・最後は次の根音へ半音で寄る）
        ch_ = S.chords[b].split("|")[0]; r_ = low(ch_, "E1"); o_ = r_ + 12; f_ = r_ + 7
        nx_ = low(S.chords[b + 1].split("|")[0], "E1") if b + 1 < S.nb else r_
        ap_ = nx_ - 1 if nx_ >= r_ else nx_ + 1
        pats = [f"{nm(r_)}:0.75 {nm(r_)}:0.25 R:0.5 {nm(o_)}:0.5 {nm(r_)}:0.25 R:0.25 {nm(f_)}:0.5 {nm(o_)}:0.25 R:0.25 {nm(ap_)}:0.5",
                f"{nm(r_)}:1 R:0.25 {nm(o_)}:0.25 {nm(o_)}:0.5 {nm(r_)}:0.5 {nm(f_)}:0.25 {nm(o_)}:0.25 R:0.5 {nm(f_)}:0.25 {nm(ap_)}:0.25",
                f"{nm(r_)}:0.75 {nm(o_)}:0.25 R:0.5 {nm(r_)}:0.5 R:0.25 {nm(r_)}:0.25 {nm(o_)}:0.5 {nm(f_)}:0.5 {nm(ap_)}:0.5",
                f"{nm(r_)}:1.5 {nm(f_)}:0.25 {nm(o_)}:0.25 R:0.5 {nm(o_)}:0.25 {nm(f_)}:0.25 {nm(r_)}:0.5 {nm(ap_)}:0.5"]
        BASS.bar(b, pats[i % 4])
    elif n == "ろうそく" and i < 3: BASS.bar(b, bass_line(S, b, "long", lo="E1"))

# ================= 効果音 =================
riser(FX, S.sc("サビ1")[0], 4, "C4"); riser(FX, S.sc("サビ2")[0], 4, "C4")
# v6: カワイイ効果音。サビの頭のインパクト、Bメロの終わりの上がる音、Aメロ2 の泡と水滴、イントロのきらきら、最後のサビの前の逆再生シンバル風
for nme in ("サビ1", "サビ2", "最後のサビ"): KFX.bar(S.sc(nme)[0], "G5:2 R:2" if nme != "サビ1" else "D4:2 R:2")
for nme in ("Bメロ1", "Bメロ2"): KFX.bar(S.sc(nme)[-2], "R:2 F#4:2")
KFX.bar(S.sc("イントロ")[3], "R:3 D4:1"); KFX.bar(S.sc("間奏")[3], "R:2 D#4:2")
for q in (1, 5): KFX.bar(S.sc("Aメロ2")[q], "R:3.5 C4:0.5" if q == 1 else "R:3 C#4:0.5 C4:0.5")
KFX.bar(S.sc("間奏2")[0], "G#5:3 R:1")       # ドロップの頭のサブドロップ
# 電子のクラップ: サビの 2・4拍に生のスネアへ重ねる（最後のサビだけ）。ドロップは 3拍目のクラップと、ハイハットの転がり
for b in S.sc("最後のサビ")[16:]: KDR.bar(b, "R:1 B4:1 R:1 B4:1")
for q, b in enumerate(S.sc("間奏2")[:4]):
    KDR.bar(b, "R:2 B4:1 R:0.5 D5:0.125 D5:0.125 D5:0.125 D5:0.125" if q % 2 == 0 else "R:2 B4:1 D5:0.25 D5:0.25 D5:0.167 D5:0.167 D5:0.166")
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
        if i < 4: D.set(b, "X.........X....." if i % 2 == 0 else "X......X..X.....", "........X.......", "x.x.x.x.x.x.x.x.")     # ハーフテンポ（スネアは3拍目だけ）
        else: vgroove(D, b, "four16", ghosts=0.3, seed=b)
        if i in (0, 4): crash(D, b)
        if i == 3: put_fill(D, b, "snare16")
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
finish(S, LY, V, -1, double=[("最後のサビ", 0.4)],
       level={"verse": -0.2}, special={"秒読み": -0.8, "サビ1": 0.3, "間奏": -0.8, "Aメロ2": -0.9, "Bメロ2": -0.5, "間奏2": -0.3, "最後のサビ": 1.0, "ろうそく": -0.2})   # v7: サビがいちばん大きく、最後のサビが山

# ================= v5（2026-11-11 作り直し。docs/sound/vt3-remake-plan.md）=================
from vt3x_lib import *
import random as _rnd
path = sys.argv[1]
TR = -1
# ---- ギター（プロの弾き方・音作り）: 左＝高い4本の弦の和音のカッティング（9th・maj7 の押さえ方、消す音「チャッ」入り）、
#      右＝単音の「チキチキ」の線（サビと間奏2だけ）。揺れ方は本物のファンクのギタリスト（GuitarSet の Funk）から借りる
GL = GuitarRig(S, "Lギター（カッティング）", "funk_cut", -0.55, 0.05, style="funk", seed=3)
PAT = {"intro": "x.xUx.dU.xxUd.xU", "verse": "..x.d..U.x..d.xU", "verse_b": "..x.d..U.x.xd.dU", "pre": "D...x.dU....d.xU", "pre_b": "d.xUd.xUd.xUD.DU",
       "cho": "d.xUx.dUx.xUd.xU", "cho_b": "d.xUx.dUx.dUd.DU", "solo": "x.dUx.xUd.xUx.dU"}
prev = None
for b in range(S.nb):
    n, i, L, k = S.scene_of(b); last = i == L - 1
    v = sorted(voice(S.chords[b].split("|")[0].split("/")[0], 66, 4, prev)); prev = v
    vo = [None, None] + [nm(x + TR) for x in v]
    if n == "イントロ": GL.bar(b, PAT["intro"], vo, vel=0.85 if i < 4 else 0.95)
    elif n == "Aメロ1":
        if i >= 8: GL.bar(b, PAT["verse_b"] if i % 4 == 3 else PAT["verse"], vo, vel=0.8)     # 1番の前半はギターなし（エレピと歌）
        else: GL.stop(b)
    elif n == "Aメロ2": GL.bar(b, PAT["verse_b"] if i % 4 == 3 else PAT["verse"], vo, vel=0.85)
    elif n in ("Bメロ1", "Bメロ2"):
        if last: GL.stop(b)                                                                     # 止めの小節
        else: GL.bar(b, PAT["pre_b"] if i >= 4 else PAT["pre"], vo, vel=0.85 + 0.03 * i)
    elif n in ("サビ1", "サビ2", "最後のサビ"): GL.bar(b, PAT["cho_b"] if i % 4 == 3 else PAT["cho"], vo, vel=1.0 if n != "最後のサビ" else 1.06)
    elif n == "間奏": GL.bar(b, PAT["intro"], vo, vel=0.95)
    elif n == "間奏2":
        if i < 4: GL.stop(b)                      # ドロップはギターなし（電子の音だけ）→ 5小節目で戻る
        else: GL.bar(b, PAT["solo"], vo, vel=1.0)
    else: GL.stop(b)
parts = GL.parts()
# 右の単音の線: 和音の音を16分で短く切って歩く。2小節でひとまとまり、強さと時刻を少し揺らす
rr = _rnd.Random(7); toks = []; cur = [0.0]
def ev(t, note, dur, vel):
    t += rr.uniform(-0.012, 0.012)
    if t > cur[0] + 1e-4: toks.extend(rests(t - cur[0]))
    toks.append(f"{note}:{dur:.4f}%{int(vel + rr.uniform(-6, 6))}"); cur[0] = t + dur
LINE = [(0.5, 0, 96), (0.75, 1, 80), (1.25, 2, 100), (1.75, 1, 78), (2.5, 3, 98), (2.75, 2, 82), (3.25, 1, 92), (3.5, 0, 84)]   # (拍, 何番目の音, 強さ)
LINE2 = [(0.25, 1, 84), (0.75, 2, 98), (1.5, 3, 100), (1.75, 2, 80), (2.25, 1, 90), (3.0, 0, 96), (3.5, 2, 86), (3.75, 3, 94)]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n not in ("サビ1", "サビ2", "最後のサビ", "間奏2"): continue
    if n == "間奏2" and i < 4: continue
    if n == "サビ1" and i < 8: continue                       # 1回目のサビは後半から入る（2回目・最後は頭から）
    tn = tones(S.chords[b].split("|")[0].split("/")[0], "A3", "B4")[:6]
    if len(tn) < 4: continue
    for (t, q, vl) in (LINE if i % 2 == 0 else LINE2): ev(b * S.beats + t, nm(tn[min(q + 1, len(tn) - 1)] + TR), 0.17, vl)
tot = S.nb * S.beats
if tot > cur[0] + 1e-4: toks.extend(rests(tot - cur[0]))
pr = copy.deepcopy(GT_BASE); pr.update(RIGS["funk_line"]); pr.update(role="Rギター（単音の線）", pan=0.6, volume=0.05, notes=" ".join(toks)); parts.append(pr)
add_parts(path, parts)
# v8: 場面ごとの大きさを測ったら、2番の Aメロ・間奏が サビ1 より大きく、最後のサビも山になっていなかった（サビ1 −16.0・Aメロ2 −15.1・サビ2 −15.0・最後 −15.4）
#     → 伴奏のパートを場面ごとに上げ下げする（サビ1 < サビ2 < 最後のサビ。Aメロ・Bメロ・間奏はサビより下）
scene_gain(path, S, {"サビ1": 1.08, "間奏": 0.9, "Aメロ2": 0.86, "Bメロ2": 0.9, "サビ2": 1.06, "間奏2": 0.97, "最後のサビ": 1.14})

if VOCAL:
    # ---- 歌い方: Aメロは話すように（しゃくりなし・ビブラートごく浅く）、Bメロでだんだん、サビは句の頭を下からすくい、長い音の後ろ半分だけ揺らす。
    #      秒読みは数を数えるだけ（揺らさない）。最後のサビがいちばん深い
    def mark(x):
        mk = x["mark"].replace("/", "")
        if x["kind"] == "chorus":
            if x["head"] and x["pos"] < 1.01 and x["bar"] % 2 == 0: mk += "/"                   # 「はっぴー…」の入り（2小節ごとの句の頭）
            elif x["prev"] is not None and x["midi"] - x["prev"] >= 5 and x["len"] >= 0.75: mk += "/"   # 大きく跳んで伸ばす音
        elif x["kind"] == "pre" and x["prev"] is not None and x["midi"] - x["prev"] >= 5 and x["len"] >= 1.0: mk += "/"
        if x["scene"] == "秒読み": mk = mk.replace("~", "")
        return mk
    remark(path, S, mark)
    vocal_polish(path, S, {"verse": 12, "pre": 20, "chorus": 28, "最後のサビ": 34, "秒読み": 0}, scoop=0.3, slash=0.8, vib_min_beats=1.5, vib_start=0.45, auto=0.6, breaths=0.5)
    # ---- ハモリ: サビ1 は一人。サビ2 の後半から3度下が入り、最後のサビは頭から（人が増えていく）
    harmony(path, S, [("サビ2", 8, None, K), ("最後のサビ", 0, None, KL)], vol=0.38, shift=TR)

    # ---- ボーカルチョップ（v6）: ドロップ（間奏2 の前半）で、テトの声を短く切って鳴らす。意味のない「や・は・ら・あ」
    d0 = S.sc("間奏2")[0]
    chops(path, S, {d0: "E4:0.5:や R:0.25 E4:0.25:や C#4:0.5:は R:0.5 A3:0.5:ら C#4:0.5:は E4:1:や",
                    d0 + 1: "R:1 F#4:0.5:は E4:0.5:や R:0.5 C#4:0.5:ら B3:0.5:は R:0.5",
                    d0 + 2: "D4:0.5:や R:0.25 D4:0.25:や F#4:0.5:は R:0.5 A4:0.5:ら F#4:0.5:は D4:1:や",
                    d0 + 3: "R:0.5 E4:0.5:は G#4:0.5:や B4:0.5:あ R:2"}, vol=0.34, pan=0.25, shift=TR)
    # ---- 声の種類（v9）: Aメロは打っては消す夜のひとりごと＝ウィスパー、Bメロはクリア、サビはキュート（明るく幼く）、秒読みはウィスパー
    voice_by_scene(path, S, {"verse": "whisper", "pre": "clear", "chorus": "cute", "秒読み": "whisper"}, default="clear")
