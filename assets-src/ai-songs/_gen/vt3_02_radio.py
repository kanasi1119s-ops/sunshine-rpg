# vt3 02「深夜ラジオのペンネーム」Pen Name on Midnight Radio（仮）— シティポップ。104・4/4。E♭長調（転調なし）。
# 第3弾（0時〜24時の街）の 1時。表は docs/sound/vt3-plan.md。
# 物語: 午前1時。家族にないしょで、まくらもとのラジオを小さな音で聞いている「わたし」。
#   かばんの底で眠っていたはがき（だれにも言えない気持ち）を、ペンネーム「ねむれないかもめ」で出していた。それが読まれる。
#   DJは「大丈夫、朝は来る。その前に、ちょっと歌おう」と言って、5つの音の鼻歌を口ずさむ。
#   ── この鼻歌（合いことばの節）が、ここから街じゅうへ伝わっていく（アルバムの始まり）。
# 場面と強さ: ジングル（ホーンの短い合図・中）→ Aメロ1（語りかける・弱）→ Bメロ1 → サビ1（中強）→ CM（こもった短い音楽・弱）
#   → Aメロ2（はがきが読まれる）→ Bメロ2 → サビ2（強）→ サックスのソロ → Cメロ（DJの言葉・とても弱い）
#   → 最後のサビ（いちばん強い）→ DJの鼻歌（節・だんだん消える）
# 旋律の性格: なめらかな7thの旋律、語りかける中音域（B♭3〜F5）。サビは 5 → 1' → 2' と上がってなだらかに降りる。
# この曲だけの音: 曲の終わりに「合いことばの節」が初めて鳴る（3・5・6・5・2＝G・B♭・C・B♭・F）。歌の版はテトの鼻歌、BGM はサックス。
#   CMの間だけ、音がAMラジオのように細く・こもる。
from vt25_lib import *

S = Song("02", "radio", "深夜ラジオのペンネーム（仮）", "Pen Name on Midnight Radio", 104, 4, "Eb", "major", "シティポップ（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --piano salamander --space room --space-wet 0.16"
S.keep_old_synth = True
S.no_depth = True
S.live_bass = True
S.open_hat_vol = 0.5
S.keepers = {"Aメロ1": "closed", "Aメロ2": "closed", "サビ2": "open", "最後のサビ": "ride"}
K = Key("Eb", "major")          # oct 4 で 1 = E♭4

JINGLE = ["Ebmaj9", "Abmaj9", "Fm9", "Bb7sus4"]
A_CH = ["Ebmaj7", "Gm7", "Abmaj7", "Bb/Ab", "Gm7", "Cm9", "Fm9", "Bb7sus4"]
B_CH = ["Abmaj7", "Bb/Ab", "Gm7", "C7", "Fm7", "Gm7", "Abmaj7", "Bb7sus4"]
C_CH = ["Abmaj7", "Bb6", "Gm7", "Cm9", "Fm9", "Bb7", "Ebmaj7", "Eb7", "Abmaj7", "Bb6", "Gm7", "C7", "Fm9", "Gm7", "Abmaj7", "Bb7sus4"]

S.scene("ジングル", 4, "intro", JINGLE)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("CM", 4, "break", ["Cm9", "Fm9", "Cm9", "Bb7sus4"])
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("サックスのソロ", 8, "solo", JINGLE * 2)
S.scene("Cメロ", 8, "bridge", ["Cm9", "Abmaj7", "Fm9", "Gm7", "Cm9", "Abmaj7", "Dbmaj7", "Bb7sus4"])
S.scene("最後のサビ", 16, "chorus", C_CH[:15] + ["Bb7"])
S.scene("鼻歌", 6, "outro", ["Ebmaj9", "Abmaj9", "Ebmaj9", "Abmaj9", "Ebmaj9", "Ebmaj9"])

V = Voice(S, vol=0.21, delay=0.75, bright=0.0, patch="kfbSineLead", low=False)   # v2: 歌をなぞるシンセは、高さの揺れない音に
EP = [S.track(f"エレピ{i + 1}", "keys", patch="kfbGlassEp", volume=0.075, pan=-0.3, reverb=0.28, sustain=0.9,
              fx=[{"type": "eq", "low": -2, "mid": 0, "midHz": 800, "high": 1}]) for i in range(4)]
CUT = [S.track(f"カッティングギター{i + 1}", "guitar", amp="jpopClean", volume=0.05, pan=0.55, reverb=0.18, chorus=0, sustain=0.3) for i in range(3)]
ARPG = S.track("ギター（アルペジオ）", "guitar", amp="crystal", volume=0.06, pan=-0.55, reverb=0.3, chorus=0, sustain=0.9)
SAX = S.track("アルトサックス", "brass", patch="altoSax", volume=0.12, pan=0.1, reverb=0.3)
BR = [S.track(f"ホーン{i + 1}", "brass", patch="brassSection", volume=0.05, pan=0.25, reverb=0.25, sustain=0.5) for i in range(3)]
STR = [S.track(f"ストリングス{i + 1}", "strings", patch="stringEnsemble", volume=0.045, pan=-0.6 + 0.6 * i, reverb=0.4, sustain=1.4) for i in range(3)]
GLK = S.track("グロッケン（星）", "glockenspiel", volume=0.05, pan=0.35, reverb=0.45)
BASS = S.track("ベース（指弾き）", "bass", **finger_bass_spec(vol=0.21))
CMR = [S.track(f"CMの音楽{i + 1}", "keys", patch="surgeKeysLightEp", volume=0.06, pan=0.0, reverb=0.1, sustain=0.5,
               fx=[{"type": "filter", "kind": "highpass", "freq": 500, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 2600, "q": 0.9}]) for i in range(3)]
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:1 5,:0.5 1:0.5 2:0.5 3:0.5 3:0.5 2:0.5", "1:1.5 7,:0.5 1:1 R:1",
      "R:1 5,:0.5 1:0.5 2:0.5 3:0.5 5:0.5 3:0.5", "2:2 R:2",
      "R:1 6,:0.5 1:0.5 3:0.5 5:0.5 6:0.5 5:0.5", "3:1.5 2:0.5 1:1 R:1",
      "R:0.5 4:0.5 3:0.5 2:0.5 1:0.5 2:0.5 3:0.5 4:0.5", "2:3 R:1"]
A1 = ("まくらもとのらじお/ごぜんいちじだ/ちいさくしぼったおと/かぞくにないしょで/"
      "やさしいわらいごえ/ひとりじゃないね/まどのそとはまっくら/ここだけあかるい")
A2 = "つぎのおたよりはね/ぺんねーむから/ねむれないかもめって/わたしのなまえだ"
VB = ["R:0.5 3:0.5 4:0.5 5:0.5 6:1 5:1", "4:1 3:1 2:1 R:1", "R:0.5 3:0.5 4:0.5 5:0.5 6:1 1':1", "7:1.5 6:0.5 5:1 R:1",
      "R:0.5 6:0.5 7:0.5 1':0.5 2':1 1':1", "7:1 6:1 5:1 R:1", "R:0.5 5:0.5 6:0.5 7:0.5 1':0.5 2':0.5 1':0.5 7:0.5", "5:2 R:2"]
B1 = "かばんのそこにね/ねむっていたはがき/だれにもいえない/きもちをかいたの"
B2 = "ほんとうのなまえ/かくしたままでも/とどくことがある/よるのなみにのり"
VC = ["R:0.5 5:0.5 1':0.5 2':0.5 1':1 7:0.5 6:0.5", "5:1.5 3:0.5 3:1 R:1",
      "R:0.5 4:0.5 6:0.5 1':0.5 7:1 6:0.5 5:0.5", "6:2 R:2",
      "R:0.5 5:0.5 1':0.5 2':0.5 1':1 7:0.5 6:0.5", "5:1.5 3:0.5 5:1 R:1",
      "R:0.5 4:0.5 3:0.5 2:0.5 1:0.5 2:0.5 3:0.5 2:0.5", "1:2 R:2",
      "R:0.5 6:0.5 6:0.5 7:0.5 1':1 2':1", "2':1.5 1':0.5 7:1 R:1",
      "R:0.5 5:0.5 5:0.5 6:0.5 7:1 1':1", "6:2 R:2",
      "R:0.5 6:0.5 7:0.5 1':0.5 2':1 1':0.5 7:0.5", "1':1.5 6:0.5 5:1 R:1",
      "R:0.5 4:0.5 3:0.5 2:0.5 3:1 2:0.5 1:0.5", "1:3 R:1"]
C1 = ("まよなかのらじおに/ちゃんねるあわせ/だれかのものがたり/まちじゅうのこえを/"
      "おなじそらのした/おきてるひと/しらないだれかとね/つながってるんだ")
C2 = ("まよなかのらじおで/わたしのことば/やさしいこえがよむ/なみだがこぼれた/"
      "なまえはないしょで/いいんだよね/ねむれないかもめも/とべるきがした")
C3 = ("まよなかのらじおで/ふいのはなうた/だれかがくちずさむ/いつつのおとだけ/"
      "おなじそらのした/あしたのまち/そのふしをだれかが/つないでいくよ")
VBR = ["R:1 3:1 3:0.5 2:0.5 3:1", "5:2 R:2", "R:1 4:1 4:0.5 3:0.5 4:1", "6:2 R:2",
       "R:1 5:1 5:0.5 6:0.5 7:1", "1':2 R:2", "R:0.5 7:0.5 6:0.5 5:0.5 6:1 7:1", "5:3 R:1"]
CB = "だいじょうぶ/あさはくる/そのまえに/ちょっとうたおう"
HUM = ["R:2 3:0.5 5:0.5 6:1", "5:0.5 2:1.5 R:2", "R:2 3:0.5 5:0.5 6:1", "5:0.5 2:3.5", "R:4", "R:4"]   # 合いことばの節（3・5・6・5・2）
LY = Lyrics(S)


def put(name, lines, text, o=4):
    bars = S.sc(name); mel = [K.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", VA + VA, A1)
put("Bメロ1", VB, B1)
put("サビ1", VC, C1)
put("Aメロ2", VA, A2)
put("Bメロ2", VB, B2)
put("サビ2", VC, C2)
put("Cメロ", VBR, CB)
put("最後のサビ", VC, C3)
if VOCAL: put("鼻歌", HUM, "ららららら/ららららら")
else:
    for b, l in zip(S.sc("鼻歌"), HUM): SAX.bar(b, K.mel(l, oct=4))

# ================= 鍵盤・ギター・弦 =================
def ep(b, ch, style):
    v = voice(ch, 63, 4)
    if style == "long": pats = [f"{nm(x)}:4" for x in v]
    elif style == "push": pats = [f"{nm(x)}:1.5 {nm(x)}:1 R:0.5 {nm(x)}:1" for x in v]
    else: pats = [f"R:0.5 {nm(x)}:1 R:0.5 {nm(x)}:0.75 R:0.25 {nm(x)}:1" for x in v]     # 16分のノリで少し前に
    for j in range(4): EP[j].bar(b, pats[j])


def cut(b, ch, pat):
    v = voice(ch, 67, 3); hits = [q for q, c in enumerate(pat) if c == "x"]
    for j in range(3):
        toks, t = [], 0
        for q in hits:
            if q > t: toks.append(f"R:{(q - t) * 0.25:g}")
            toks.append(f"{nm(v[j])}:0.25"); t = q + 1
        if t < 16: toks.append(f"R:{(16 - t) * 0.25:g}")
        CUT[j].bar(b, " ".join(toks))


def strings(b, ch, c=70):
    v = voice(ch, c, 3)
    for j in range(3): STR[j].bar(b, f"{nm(v[j])}:4")


def horns(b, ch, pat):
    v = voice(ch, 68, 3)
    for j in range(3): BR[j].bar(b, " ".join(t.replace("x", nm(v[j])) for t in pat.split()))


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "ジングル":
        ep(b, ch, "long"); strings(b, ch)
        horns(b, ch, ["x:0.5! R:0.25 x:0.25 x:1 R:2", "R:2 x:0.5 x:0.5 x:1", "x:0.5! R:0.25 x:0.25 x:1 R:2", "R:1 x:3"][i])
        GLK.bar(b, ["R:3 G6:1", "R:4", "R:3 Bb6:1", "R:4"][i])
    elif n in ("Aメロ1", "Aメロ2"):
        ep(b, ch, "push" if i % 2 == 0 else "skip")
        if n == "Aメロ2" or i >= 8: cut(b, ch, "....x.......x...")
        if i % 4 == 3: ARPG.bar(b, " ".join(f"{nm(x)}:0.5" for x in (tones(ch, "Bb3", "Bb5") * 2)[:8]))
    elif n in ("Bメロ1", "Bメロ2"):
        ep(b, ch, "skip"); cut(b, ch, "..x...x...x...xx")
        strings(b, ch, 68)
        ARPG.bar(b, " ".join(f"{nm(x)}:0.5" for x in (tones(ch, "Bb3", "Bb5") * 2)[:8]))
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        ep(b, ch, "skip"); cut(b, ch, "..x.x.x...x.x.x.")
        strings(b, ch, 72)
        if i % 4 == 3: horns(b, ch, "R:2.5 x:0.5 x:0.5 x:0.5")
        if i % 8 == 7: GLK.bar(b, "R:2 " + " ".join(f"{nm(x)}:0.5" for x in tones(ch, "G5", "G6")[:4]))
        if n == "最後のサビ" and i in (3, 11): SAX.bar(b, "R:2 " + K.mel("3:0.5 5:0.5 6:0.5 5:0.5", oct=5))   # 節の頭がちらりと
    elif n == "CM":
        v = voice(ch, 64, 3)   # AMラジオの細い音の、短い明るい音楽
        for j in range(3): CMR[j].bar(b, f"R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5")
    elif n == "サックスのソロ":
        ep(b, ch, "skip"); cut(b, ch, "....x..x....x...")
        SOLO = ["R:0.5 Bb4:0.5 C5:0.5 D5:0.5 Eb5:1 G5:1", "F5:1.5 Eb5:0.5 D5:0.5 C5:0.5 Bb4:1", "R:0.5 Ab4:0.5 C5:0.5 Eb5:0.5 G5:1.5 F5:0.5", "Eb5:0.5 D5:0.5 C5:1 Bb4:2",
                "R:0.5 G4:0.5 Bb4:0.5 D5:0.5 F5:1 Eb5:0.5 D5:0.5", "C5:1 Eb5:1 Ab5:1.5 G5:0.5", "F5:0.5 Eb5:0.5 D5:0.5 C5:0.5 D5:1 Eb5:1", "F5:3 R:1"]
        SAX.bar(b, SOLO[i])
        strings(b, ch, 70)
    elif n == "Cメロ":
        v = voice(ch, 63, 4)
        for j in range(4): EP[j].bar(b, f"{nm(v[j])}:4")
        if i >= 4: strings(b, ch, 68)
    elif n == "鼻歌":
        if i < 5:
            v = voice(ch, 63, 4)
            for j in range(4): EP[j].bar(b, f"{nm(v[j])}:4")
            strings(b, ch, 70)
        else:
            v = voice(ch, 63, 4)
            for j in range(4): EP[j].bar(b, f"{nm(v[j])}:3 R:1")
            GLK.bar(b, "G6:2 R:2")

# ================= ベース =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    if n == "ジングル": BASS.bar(b, bass_line(S, b, "long", lo="E1"))
    elif n in ("Aメロ1", "Aメロ2"): BASS.bar(b, bass_line(S, b, "half" if i < 4 and n == "Aメロ1" else "push", lo="E1"))
    elif n in ("Bメロ1", "Bメロ2"): BASS.bar(b, bass_line(S, b, "root8", lo="E1"))
    elif n in ("サビ1", "サビ2", "最後のサビ", "サックスのソロ"): BASS.bar(b, bass_line(S, b, "oct8" if i % 4 != 3 else "walk", lo="E1"))
    elif n == "Cメロ" and i >= 4: BASS.bar(b, bass_line(S, b, "long", lo="E1"))
    elif n == "鼻歌" and i < 5: BASS.bar(b, bass_line(S, b, "long", lo="E1"))

cym_swell(CYM, S.sc("Aメロ1")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 4, "E4")

# ================= ドラム（16ビートのシティポップ）=================
K16, S16, H16 = "X.....x...X..x..", "....X.......X...", "xxxxxxxxxxxxxxxx"
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "ジングル":
        if i == 0: crash(D, b)
        if i == 3: put_fill(D, b, "small")
    elif n in ("Aメロ1", "Aメロ2"):
        if n == "Aメロ1" and i < 4: D.set(b, "X.......X.......", "....x.......x...", "x.x.x.x.x.x.x.x.")
        else: vgroove(D, b, "beat8", ghosts=0.45, seed=b, k=K16, s=S16, h=H16)
        if i % 8 == 7 and not last: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
    elif n in ("Bメロ1", "Bメロ2"):
        vgroove(D, b, "beat8", ghosts=0.4, seed=b, k="X.....x...x.....", s=S16, h="x.x.x.x.x.x.x.x.")
        if i == 7: put_fill(D, b, "tomdown")
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        vgroove(D, b, "beat8", ghosts=0.35, seed=b, k="X.....x.X.....x.", s=S16, h="x.xox.xox.xox.xo".replace("o", "x"))
        if i % 8 == 0: crash(D, b, "C2", 6 if (n == "最後のサビ" and i == 0) else 4)
        if i % 8 == 7 and not last: put_fill(D, b, "small" if i < 8 else "tomtrip")
        if last and n != "最後のサビ": put_fill(D, b, "snare16")
    elif n == "CM":
        D.set(b, "................", "................", "x.x.x.x.x.x.x.x.")
        if last: put_fill(D, b, "small")
    elif n == "サックスのソロ":
        vgroove(D, b, "beat8", ghosts=0.45, seed=b, k=K16, s=S16, h=H16)
        if i == 0: crash(D, b)
        if last: halt(D, b, 1)
    elif n == "Cメロ":
        if i >= 4: D.set(b, "X.......X.......", "........X.......", "x.x.x.x.x.x.x.x.")
        if last: put_fill(D, b, "build")
    elif n == "鼻歌":
        if i == 0: crash(D, b, "C2", 6)
        if i < 4: D.set(b, "X.......X.......", "....x.......x...", "x...x...x...x...")

# 止め: Bメロ2 の最後の1拍だけ全員休み
SIL.add(S.sc("Bメロ2")[-1], 3, 4)
SIL.apply()

S.fade_out = 6
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の02（1時）。シティポップ。E♭・104。深夜ラジオで、ペンネームのはがきが読まれる。"
          "DJ が口ずさむ5つの音の鼻歌（合いことばの節）が、ここで生まれる。エレピ・カッティングギター・指弾きのベース・アルトサックス・ホーン。自作")
finish(S, LY, V, 0,
       level={"verse": -0.25}, special={"CM": -0.7, "Cメロ": -0.6, "最後のサビ": 0.4, "鼻歌": -0.35})

# ================= v2（2026-11-11 作り直し。docs/sound/vt3-remake-plan.md）=================
# 人間「他24曲もとことん作りこんでください」。この曲（午前1時・ふとんの中のラジオ・シティポップ）で直すこと:
#   ギター: 右＝セミアコ寄りの丸いクリーンのカッティング（高い4本の弦・9th と maj7 の押さえ方・消す音入り。Aメロは間をあけ、サビで細かく）、
#           左＝クリーンのアルペジオ（音を伸ばして重ねる）。どちらも DI を弦ごとに弾く。コーラスなし
#   電子の音: エレピを kfbGlassEp（ガラスのような FM のエレピ）に。Cメロと鼻歌に、うすいきらきらのパッド（kfbSparklePad）で夜の空気を足す
#   歌: Aメロはふとんの中の小声（ウィスパー）、Bメロとサビはクリア、Cメロ（DJ の言葉）と鼻歌はウィスパー。ハモリは サビ2 の後半と最後のサビ
#   ベース: 同じ音を続ける所の穴をなくす（sustain 1.15）
from vt3x_lib import *
path = sys.argv[1]
GR = GuitarRig(S, "Rギター（カッティング）", "city_cut", 0.55, 0.055, style="funk_slow", seed=11)
PAT2 = {"verse": "....D.....x.d..U", "verse_b": "....D..U..x.d.xU", "pre": "..d.x.dU..d.x.dU", "pre_b": "d.xU..dUx.dUD.DU", "cho": "d..Ux.dU.xd.x.dU", "cho_b": "d.xUx.dUd.xUD.dU",
        "solo": "....d..U....d.x.", "jingle": "D.......x.d..U.."}
prev = None; arp = {}
for b in range(S.nb):
    n, i, L, k = S.scene_of(b); last = i == L - 1
    ch = S.chords[b].split("|")[0].split("/")[0]
    v = sorted(voice(ch, 67, 4, prev)); prev = v; vo = [None, None] + [nm(x) for x in v]
    if n == "ジングル": GR.bar(b, PAT2["jingle"], vo, vel=0.9)
    elif n == "Aメロ1":
        if i >= 8: GR.bar(b, PAT2["verse_b"] if i % 4 == 3 else PAT2["verse"], vo, vel=0.78)
        else: GR.stop(b)
    elif n == "Aメロ2": GR.bar(b, PAT2["verse_b"] if i % 4 == 3 else PAT2["verse"], vo, vel=0.82)
    elif n in ("Bメロ1", "Bメロ2"): GR.bar(b, PAT2["pre_b"] if i >= 6 else PAT2["pre"], vo, vel=0.84 + 0.02 * i)
    elif n in ("サビ1", "サビ2", "最後のサビ"): GR.bar(b, PAT2["cho_b"] if i % 4 == 3 else PAT2["cho"], vo, vel=0.96 if n != "最後のサビ" else 1.04)
    elif n == "サックスのソロ": GR.bar(b, PAT2["solo"], vo, vel=0.85)
    else: GR.stop(b)
    # 左のアルペジオ: Aメロは4小節ごと、Bメロは毎小節（下から上へ、上で折り返す）、Cメロは1小節に4つの音を長く
    tn = tones(ch, "Bb2", "G4")
    if len(tn) >= 4:
        up8 = [tn[q % len(tn)] for q in (0, 2, 3, 4, 5, 4, 3, 2)]
        if n in ("Aメロ1", "Aメロ2") and i % 4 == 3: arp[b] = " ".join(f"{nm(x)}:0.5" for x in up8)
        elif n in ("Bメロ1", "Bメロ2"): arp[b] = " ".join(f"{nm(x)}:0.5" for x in (up8 if i % 2 == 0 else up8[::-1]))
        elif n == "Cメロ": arp[b] = " ".join(f"{nm(tn[q % len(tn)])}:1" for q in (0, 2, 4, 3))
        elif n == "鼻歌" and i < 5: arp[b] = f"{nm(tn[0])}:1 {nm(tn[2])}:1 {nm(tn[3])}:2"
parts = GR.parts() + [line_part(S, "Lギター（アルペジオ）", "clean_arp", -0.55, 0.06, arp, seed=4)]
# 夜の空気: Cメロと鼻歌に、うすいきらきらのパッド（和音の上2つの音）
sp = {}
for b in S.sc("Cメロ") + S.sc("鼻歌")[:5]:
    v = voice(S.chords[b].split("|")[0].split("/")[0], 72, 3); sp[b] = v
for j in range(2):
    toks = []; cur = 0
    for b in sorted(sp):
        if b * S.beats > cur: toks.extend(rests(b * S.beats - cur))
        toks.append(f"{nm(sp[b][j + 1])}:4"); cur = (b + 1) * S.beats
    toks.extend(rests(S.nb * S.beats - cur))
    parts.append({"role": f"きらきらのパッド{j + 1}", "instrument": "lead", "patch": "kfbSparklePad", "notes": " ".join(toks), "volume": 0.022, "pan": -0.3 + 0.6 * j, "reverb": 0.4})
add_parts(path, parts, drop=lambda p: p.get("role", "").startswith("カッティングギター") or p.get("role", "").startswith("ギター（アルペジオ）"))
set_parts(path, "ベース", sustain=1.15)
if VOCAL:
    remark(path, S, std_mark(("chorus",), plain=("鼻歌",)))
    vocal_polish(path, S, {"verse": 8, "pre": 16, "chorus": 24, "最後のサビ": 28, "bridge": 10, "outro": 6}, scoop=0.3, slash=0.7, vib_min_beats=1.5, vib_start=0.5, auto=0.6, breaths=0.6)
    harmony(path, S, [("サビ2", 8, None, K), ("最後のサビ", 0, None, K)], vol=0.36)
    voice_by_scene(path, S, {"verse": "whisper", "pre": "clear", "chorus": "clear", "bridge": "whisper", "outro": "whisper"}, default="clear")
