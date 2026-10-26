# vb25 11「ゼロイチ・ワンダーランド」Zero-One Wonderland（仮）— エレクトロニカ（デジタルの世界）。B短調（サビは平行調の D長調）・154・4/4。最後のサビは +2（E長調）
# 2026-10-25 人間「デジタルな感じの世界の曲も欲しいかも」→「25曲の中に入れる」「ふつうの曲」。
# 2026-10-25 作り直し: 物語を人の気持ちの話に（画面ごしの友だち）、歌を人が歌える旋律（8分と4分）に、音を Surge の音に（自作のシンセをやめた）、テトの歌の版を足した。
#   テトの声に合うよう、曲全体を E短調から 5半音下げて B短調にした（書くのは E短調の度数のまま、書き出しの前に下げる）。
# 物語: 夜中、画面の中で光る友だちの名前。会ったことはないけれど、0と1でつながっている。おはようより、おやすみより、たくさんの文字を送り合う。
#   本当の君はどんな人か知りたいけれど、こわくもなる。それでも、いつか会いに行く。画面の中は、二人だけのワンダーランド。
# 場面と強さ: 起動（ベースだけ。0と1のように1オクターブを跳ぶ旋律）→ ログイン（アルペジオ → キックとハイハット → パッドの順に入る）→ 夜中の画面（Aメロ・0と1のオクターブ）→ ほんとうの君（Bメロ・溜め・止め）
#   → ワンダーランド（サビ・4つ打ち）→ 2番（BGM は声のようなシンセが歌を受け取る）→ Bメロ2 → サビ2（ジャージークラブ）
#   → バグの嵐（グリッチ・1拍の無音）→ おやすみ（Half feel・こもり）→ サーバーの夜景（アルペジオのソロ）→ 光の線（最後のサビ +2）→ ログアウト
# 旋律の性格: Aメロは同じ音と1オクターブ上の音を行き来する（0と1）。サビは跳ねる8分の句を2小節ずつ。最高音 F#5。
# ほかの曲とちがう所: いちばん電子的な曲。ビットの崩れ・グリッチ・ナポリの和音の不安定さ、アルペジオのソロ。
from vb25_lib import *

S = Song("11", "zeroichi", "ゼロイチ・ワンダーランド（仮）", "Zero-One Wonderland", 154, 4, "E", "minor", "エレクトロニカ（ボカロ・デジタルの世界）")
S.kit = "electro"
S.flags = "--ref-tone glossy-jrock " + S.flags
S.keep_old_synth = True
S.no_depth = True
K = S.key                    # E短調
KG = Key("G", "major")       # サビ
KA = Key("A", "major")       # 最後のサビ（+2）
KF = Key("F#", "minor")

A_CH = ["Em", "Em/D", "Cmaj7", "B7", "Em", "Em/D", "Am7", "B7sus4"]
B_CH = ["Cmaj7", "D", "Bm7", "Em", "Am7", "D", "A#dim", "B7"]                # A#dim＝♯iv°（次の Em への準備）
C_CH = ["Cmaj7", "D", "Bm7", "Em", "Cmaj7", "D", "G", "B/D#"]                # B/D#＝vi への副属和音
C_CH2 = ["Cmaj7", "D", "Bm7", "Em", "Am7", "D", "Gmaj7", "Gmaj7"]
BUG = ["Em", "F", "Em", "F", "Em", "F", "B7", "B7"]                           # F＝♭II（ナポリ。グリッチの不安定さ）
NIGHT = ["Am7", "Bm7", "Cmaj7", "D", "Am7", "Bm7", "Cmaj7", "D/F#"]
LAST = ["Dmaj7", "E", "C#m7", "F#m", "Dmaj7", "E", "A", "C#/F"]
LAST2 = ["Dmaj7", "E", "C#m7", "F#m", "Bm7", "E", "Amaj7", "Amaj7"]

S.scene("起動", 4, "intro", ["Em", "Em", "Cmaj7", "B7sus4"])
S.scene("ログイン", 8, "intro", A_CH)
S.scene("データの川", 16, "verse", A_CH)
S.scene("ファイアウォール", 8, "pre", B_CH)
S.scene("ネットの空", 16, "chorus", C_CH + C_CH2)
S.scene("キャッシュの迷路", 16, "verse", A_CH)
S.scene("ファイアウォール2", 8, "pre", B_CH)
S.scene("ネットの空2", 16, "chorus", C_CH + C_CH2)
S.scene("バグの嵐", 8, "break", BUG)
S.scene("再起動", 8, "bridge", NIGHT)
S.scene("サーバーの夜景", 16, "solo", NIGHT)
S.scene("光回線", 24, "chorus", LAST + LAST2 + LAST)
S.scene("ログアウト", 8, "outro", ["Amaj7", "E", "F#m", "D", "Amaj7", "E", "Amaj7", "Amaj7"])

V = Voice(S, vol=0.22, delay=0.75, patch="modernLead", low=True)   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
ARP = S.track("デジタルのアルペジオ", "pad", patch="surgeKeysNanowave2Oscs", volume=0.07, pan=0.35, reverb=0.25,
              fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.18, "feedback": 0.3}])
ARP2 = S.track("アルペジオ（ソロ）", "lead", patch="surgeKeysDizzy", volume=0.12, pan=-0.1, reverb=0.25, mono=True,
               fx=[{"type": "pingpong", "beats": 0.75, "mix": 0.15, "feedback": 0.25}])
CHOP = S.track("声のようなシンセ", "lead", patch="surgeFormantPulse", volume=0.1, mono=True, pan=-0.25, reverb=0.3)
# 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ 最後のサビで「画面の向こうの君」が返事をするように、声のようなシンセの対旋律。
#   主役（歌）より小さく 0.07。上の「声のようなシンセ」と同じ設定（音量だけちがう）なので、MIDI のチャンネルを分け合う（チャンネルを増やさない）
REPLY = S.track("君の返事（声のようなシンセ・対旋律）", "lead", patch="surgeFormantPulse", volume=0.07, mono=True, pan=-0.25, reverb=0.3)
FB = [S.track(f"フューチャーベースの和音{i + 1}", "pad", patch="surgeChordVisitorPlayground", volume=0.05, pan=[-0.6, 0.6, 0][i], reverb=0.3, duck=0.5) for i in range(3)]
SAW = [S.track(f"厚い和音{i + 1}", "pad", patch="surgePadNeverending", volume=0.045, pan=[-0.7, 0.7][i], reverb=0.3, duck=0.45) for i in range(2)]
# 2026-10-26: 歌の版で MIDI のチャンネルが1つ足りず、シンバルの効果音がパッドの音で鳴っていた（点検の注意）。
#   こもったパッド2本の左右（-0.5・0.5）を真ん中にそろえて、1つのチャンネルを分け合う（ローパスの奥の音なので、真ん中でも歌のじゃまをしない）
PAD = [S.track(f"こもったパッド{i + 1}", "pad", patch="surgePadVerbPad", volume=0.06, pan=0.0, reverb=0.4,
               fx=[{"type": "filter", "kind": "lowpass", "freq": 900, "q": 0.8}]) for i in range(2)]
BELL = S.track("ガラスのような鍵盤（データの粒）", "pad", patch="surgeKeysAliasGlassPiano2", volume=0.07, pan=0.25, reverb=0.45)
GLITCH = S.track("グリッチ（ビットの崩れ）", "lead", patch="surgeDnaSeq", volume=0.06, pan=0.0, mono=True,
                 fx=[{"type": "bitcrusher", "bits": 6, "mix": 0.8}, {"type": "filter", "kind": "highpass", "freq": 500, "q": 0.7}])
BASS = S.track("シンセベース", "bass", **synth_bass_spec("surgeBassEmulation", vol=0.22, duck=0.25))
BLO, BR = "A1", {"lo": 33, "hi": 57}
# 2026-10-26 人間「後半に行くにつれて曲の始まり方似てない？」（11 と 20 がどちらも「起動」の物の音で始まっていた）→ ベースの旋律1本だけで始める。
#   Aメロの「0と1」（同じ音と1オクターブ上を行き来する）を、ベースが先に弾く。16分の食いと休みで、画面の点滅のようにはずむ（E短調で書く。鳴るのは B短調）
BOOT = ["E2:0.75! E3:0.25 R:0.5 E2:0.5 B2:0.5 E3:0.5 D3:0.5 B2:0.5",
        "E2:0.75! E3:0.25 R:0.5 E2:0.5 G2:0.5 A2:0.5 B2:1",
        "C2:0.75! C3:0.25 R:0.5 C2:0.5 G2:0.5 B2:0.5 C3:0.5 E3:0.5",
        "B1:0.75! B2:0.25 R:0.5 B1:0.5 E2:0.5 F#2:0.5 A2:0.5 B2:0.5"]   # ベースを書く高さ（書き出しの前に 5半音下げたあとで E1〜E3。E1 から書くと B0 まで下がっていた）
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 旋律と歌詞（E短調の度数。oct=4 で 1 = E4。サビは G長調。書き出しの前に全体を 5半音下げる） =================
VERSE = ["R:1 1:0.5 1:0.5 1':0.5 1:0.5 7:1", "5:2 R:2",
         "R:1 3:0.5 3:0.5 3':0.5 3:0.5 2':1", "#7:2 R:2",
         "R:1 1:0.5 1:0.5 1':0.5 7:0.5 5:1", "3:2 R:2",
         "R:1 6:0.5 6:0.5 1':0.5 7:0.5 6:1", "5:2 R:2",
         "R:1 5:0.5 5:0.5 1':0.5 5:0.5 7:1", "1':2 R:2",
         "R:1 3':0.5 3':0.5 2':0.5 1':0.5 7:1", "#7:2 R:2",
         "R:1 1:0.5 1':0.5 1:0.5 1':0.5 7:1", "5:2 R:2",
         "R:1 6:0.5 6:0.5 5:0.5 4:0.5 3:1", "4:2 R:2"]
V1 = "よなかのにじ/あおいまどに/きみのなまえ/ともっているよ/あえたことは/まだないけど/ぜろといちで/つながってるの"
V2 = "おはようより/おやすみより/たくさんとぶ/もじぼたるよ/わらうかおも/なくかおもね/しらないけど/すけるきがね"
BV = ["R:0.5 3:0.5 3:0.5 4:0.5 5:1 6:1", "6:1 5:1.5 R:1.5", "R:0.5 2':0.5 2':0.5 1':0.5 7:1 6:1", "5:2 R:2",
      "R:0.5 1':0.5 1':0.5 2':0.5 3':1 2':1", "1':1 2':1.5 R:1.5", "R:0.5 3':0.5 3':0.5 1':0.5 #4:1 3:1", "#7:2 R:2"]
P1 = "ほんとうのきみ/どんなひとか/のぞきたいけど/ゆびがとまる"
P2 = "がめんごしでも/それでもいい/でもいつかはね/まどをこえる"
CV = ["R:0.5 5:0.5 1':0.5 5:0.5 2':1 1':1", "7:0.5 6:0.5 5:0.5 6:0.5 3':2", "R:0.5 6:0.5 1':0.5 6:0.5 3':1 2':1", "1':0.5 7:0.5 6:0.5 7:0.5 5:2",
      "R:0.5 5:0.5 1':0.5 5:0.5 2':1 3':1", "3':1 2':0.5 1':0.5 7:0.5 6:0.5 R:1", "2':1 3':1 2':0.5 1':0.5 7:1", "#2':3 R:1"]
CV2 = CV[:6] + ["3':1 2':0.5 1':0.5 2':1 7:1", "1':4"]
C1 = "ぜろといちのそらへと/とばしたもじぼたるが/ひかりのつぶになってね/きみにとどく/ここはわんだーらんど/あったことのないきみと/おなじよるをわらってる/ゆめのなかで"
C2 = "ぜろといちのそらへと/きみのもじがふってくる/ひかりのつぶになってね/むねにともる/ここはわんだーらんど/あったことのないきみと/おなじよるをわらってる/ゆめのなかで"
LASTX = ["R:0.5 5:0.5 1':0.5 5:0.5 2':1 1':1", "7:0.5 6:0.5 5:0.5 6:0.5 2':2", "R:0.5 6:0.5 1':0.5 6:0.5 2':1 1':1", "1':0.5 7:0.5 6:0.5 7:0.5 5:2",
         "R:0.5 4:0.5 6:0.5 1':0.5 2':2", "1':1 7:1 6:1 5:1", "6:1 7:1 1':2", "1':4"]
fin = lambda xs: [x.replace("#2':3", "7:3").replace("3':", "2':") for x in xs]   # 最後のサビ（+2）はテトの高さに収める
CL = C1 + "/ひかりのせんのうえを/はしってゆくよきみへと/いつかきっとあいにいくよね"
RV = ["3:2 5:2", "6:3 R:1", "1':2 7:1 6:1", "5:3 R:1", "3:2 5:2", "6:2 1':1 R:1", "2':2 3':2", "#4':4"]
RVV = "あさが/くるまえ/おやすみ/きみへ"
LY = Lyrics(S)
def put(name, key, lines, text, low=True, o=4):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m, low=low)
    LY.flow(bars, mel, text, name)
put("データの川", K, VERSE, V1)
if VOCAL: put("キャッシュの迷路", K, VERSE, V2)
else:
    for i, b in enumerate(S.sc("キャッシュの迷路")):
        line = K.mel(VERSE[i], oct=4)
        if i < 8: CHOP.bar(b, line)                                  # BGM: 2番の前半は、声のようなシンセが歌を受け取る
        else: V.bar(b, line)
put("ファイアウォール", K, BV, P1); put("ファイアウォール2", K, BV, P2)
put("ネットの空", KG, CV + CV2, C1); put("ネットの空2", KG, CV + CV2, C2)
for name in ("ネットの空", "ネットの空2"):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3: CHOP.bar(b, KG.mel("R:2 5':0.25 R:0.25 5':0.25 3':0.25 1':1", oct=4))     # 合いの手
put("再起動", K, RV, RVV)
put("光回線", KA, fin(CV + CV2) + LASTX, CL)
put("ログアウト", KA, ["5:2 3:2", "2:2 5,:2", "3:2 1:2", "1:4", "R:4", "R:4", "R:4", "R:4"], "おやすみなさい")


# ================= ソロ・グリッチ =================
SOLO = ["1:0.25 3:0.25 5:0.25 1':0.25 " * 2 + "2:0.25 4:0.25 6:0.25 2':0.25 " * 2,
        "3:0.25 5:0.25 7:0.25 3':0.25 " * 2 + "4:0.25 6:0.25 1':0.25 4':0.25 " * 2,
        "1':0.25 7:0.25 6:0.25 5:0.25 4:0.25 3:0.25 2:0.25 1:0.25 2:0.25 3:0.25 4:0.25 5:0.25 6:0.5 5:0.5",
        "3:1 R:0.5 5:0.25 6:0.25 7:1 1':1"]
for i, b in enumerate(S.sc("サーバーの夜景")):
    s_ = SOLO[i % 4].strip() if i < 12 else ["5':0.25 3':0.25 1':0.25 5:0.25 " * 4, "6':0.25 4':0.25 1':0.25 6:0.25 " * 4,
                                             "7':0.5 5':0.5 2':0.5 7:0.5 5:0.5 2:0.5 7,:1", "#4:4"][i - 12].strip()
    # 2026-10-26: 同じ4小節が3回続いていた（点検の注意）ので、2回目は逆から（下りの分散和音）、3回目の前半は1オクターブ上で
    if 4 <= i < 8: s_ = retro(s_)
    if 8 <= i < 10: s_ = shift_oct(K.mel(s_, oct=4), 1); ARP2.bar(b, s_); continue
    ARP2.bar(b, K.mel(s_, oct=4))
for i, b in enumerate(S.sc("バグの嵐")):
    if i % 2 == 0: GLITCH.bar(b, K.mel(" ".join(["1':0.125"] * 8 + ["b2':0.125"] * 8) + " R:2", oct=4))
    else: GLITCH.bar(b, K.mel("R:2 " + " ".join(["5:0.125", "1':0.125"] * 8), oct=4))
for name in ("ログイン", "データの川"):
    for i, b in enumerate(S.sc(name)):
        if i % 8 == 7: GLITCH.bar(b, K.mel("R:3 " + " ".join(["1'':0.0625"] * 8) + " R:0.5", oct=4))   # 1拍だけのビットの崩れ

# ================= 伴奏 =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; v = voice(ch, 64, 3)
    t = tones(ch, "B4", "B6")
    # デジタルのアルペジオ（起動からずっと。バグの嵐と再起動では止まる）
    # 2026-10-26 人間「後半に行くにつれて曲の始まり方似てない？」→ 起動はベースだけ。アルペジオはログインから
    if n not in ("バグの嵐", "再起動", "サーバーの夜景", "起動"):
        ARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" for q in (0, 2, 1, 3, 2, 4, 3, 1) * 2))
    # ベース
    # 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ 根音の8分（oct8）だけだった所を歌うベースに。Aメロの後半は、歌が「R:2」で休む
    #   奇数小節でベースが上る（climb・walk）。サビは歌が細かい偶数小節を押して（drive）、伸ばす奇数小節で駆ける（run）、句の終わりは下りる（fall）。
    #   ファイアウォール（Bメロ）は歌といっしょに上っていく。ログイン・夜景はハウスの裏のまま（場面の色）。音量はそのまま
    if n == "起動": BASS.bar(b, BOOT[i])
    elif n == "ログイン": BASS.bar(b, bass_line(S, b, "push", lo=BLO))
    elif n in ("データの川", "キャッシュの迷路"):
        BASS.bar(b, bass_line(S, b, "push", lo=BLO) if (i < 8 or i % 2 == 0) else sing_bass(S, b, "climb" if i % 4 == 1 else "walk", **BR))
    elif n.startswith("ファイアウォール"): BASS.bar(b, sing_bass(S, b, "climb", **BR) if i < 7 else bass_line(S, b, "long", lo=BLO))
    elif n.startswith("ネットの空") or n == "光回線": BASS.bar(b, sing_bass(S, b, "fall" if i % 8 == 7 else ("run" if i % 2 == 1 else "drive"), **BR))
    elif n == "バグの嵐": BASS.bar(b, bass_line(S, b, "half", lo=BLO))
    elif n in ("再起動", "サーバーの夜景"): BASS.bar(b, bass_line(S, b, "long" if n == "再起動" else "house", lo=BLO))
    elif n == "ログアウト" and i < 6: BASS.bar(b, bass_line(S, b, "half", lo=BLO))
    # フューチャーベースの和音（サビ）・厚い和音（光回線）
    if n.startswith("ネットの空") or n == "光回線":
        for j in range(3): FB[j].bar(b, f"{nm(v[j])}:0.75 {nm(v[j])}:0.75 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:1.5")
    if n == "光回線" or (n == "ネットの空2" and i >= 8):
        w = voice(ch, 60, 2, spread=True)
        for j in range(2): SAW[j].bar(b, f"{nm(w[j])}:4")
    # こもったパッド（起動・再起動・ログアウト）
    if n in ("再起動", "ログアウト", "サーバーの夜景") or (n == "ログイン" and i >= 4):   # 起動では鳴らさず、ログインの後半から
        w = voice(ch, 60, 2)
        for j in range(2): PAD[j].bar(b, f"{nm(w[j])}:4")
    # ベル（データの粒）
    if n in ("ネットの空", "ネットの空2", "光回線") and i % 2 == 1:
        BELL.bar(b, " ".join(f"{nm(x)}:0.5" for x in tones(ch, "B5", "B6")[:4]) + " R:2")
# 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ この物語でしか出てこない音: Aメロで歌が休む所（2・6・10・14小節目の後半）に、
#   画面に君の文字が届く「ぽろん」（ガラスの鍵盤の上がる2音。0.07 のまま）。「既読」の合図のように、歌のすき間だけで鳴らす
for name in ("データの川", "キャッシュの迷路"):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 1: BELL.bar(b, K.mel("R:2.5 5':0.5 1'':1", oct=4))
FX.bar(S.sc("ログイン")[0], "G4:4")                    # 2026-10-26: 電源が入る「ドーン」（サブドロップ）。ベースだけの起動から一気に走り出す
# 最後のサビ（光回線）の9〜22小節目: 君の返事の対旋律（歌が伸ばす所でゆっくり動く2分音符・全音符。A長調の度数）
RP = ["3:2 6:2", "5:2 7:2", "5:2 3:2", "6:3 R:1", "4:2 6:2", "5:1 6:1 7:2", "1':4", "7:3 R:1"]   # 4小節ごとに息つぎ
RP2 = ["3:2 6:2", "5:2 7:2", "5:2 3:2", "6:3 R:1", "6:2 3:2", "5:1 6:1 7:1 R:1"]
for i, b in enumerate(S.sc("光回線")):
    if 8 <= i < 16: REPLY.bar(b, KA.mel(RP[i - 8], oct=4))
    elif 16 <= i < 22: REPLY.bar(b, KA.mel(RP2[i - 16], oct=4))
riser(FX, S.sc("ネットの空")[0] - 2, 8, "C4"); riser(FX, S.sc("ネットの空2")[0] - 2, 8, "C4"); riser(FX, S.sc("光回線")[0] - 4, 16, "D4")
cym_swell(CYM, S.sc("ネットの空")[0] - 1, 2, "C4"); cym_swell(CYM, S.sc("光回線")[0] - 1, 2, "C4")
FX.bar(S.sc("ログアウト")[-1], "E4:4")                  # 電源が落ちる（ダウンリフター）

# ================= ドラム =================
def shape(b, kind, i, L):
    """2026-10-26 人間「ドラム強弱、アクセント、余韻も上手く使ってね」: 場面の強さに合わせた叩き分け（型を置いた直後に呼ぶ）。
    Aメロ・Cメロ: スネアは句の頭の小節（4小節に1回）だけ強く（X）、ほかはふつう（x）。ハイハットは拍の頭だけ強く。Bメロは前半を抑えて後半で上げる"""
    s_, h_ = list(D.S[b]), list(D.H[b])
    if kind in ("verse", "bridge"):
        if i % 4: s_ = ["x" if c == "X" else c for c in s_]
        h_ = [c if j % 4 == 0 else ("x" if c == "X" else c) for j, c in enumerate(h_)]
    elif kind == "pre" and i < L // 2:
        s_ = ["x" if c == "X" else c for c in s_]
    D.S[b], D.H[b] = "".join(s_), "".join(h_)


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "起動":
        D.set(b, "................", "................", "................")      # ベースだけ
    elif n == "ログイン":
        # 1〜2小節目はキックだけ、3小節目からハイハット、5小節目からスネア（順に入る）
        vgroove(D, b, "four", seed=b, s="................" if i < 4 else None, h="................" if i < 2 else None)
        if i == 0: crash(D, b, "C2", 8)                                    # 電源が入る所。クラッシュを長く鳴らす
        if last: put_fill(D, b, "snare16")
    elif n in ("データの川", "キャッシュの迷路"):
        vgroove(D, b, "twostep" if i < 8 else "four", ghosts=0.3, seed=b)
        shape(b, k, i, L)
        if i == 0: crash(D, b)
        if i % 8 == 7: put_fill(D, b, "small")
    elif n.startswith("ファイアウォール"):
        vgroove(D, b, "half" if i < 4 else "four16", ghosts=0.2, seed=b)
        shape(b, k, i, L)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 2); crash(D, b, "G2", 4)                       # 余韻: 止めのあとも、クラッシュの鳴りを止めの終わりまで残す
    elif n.startswith("ネットの空") or n == "光回線":
        name = "jersey" if (n == "ネットの空2" and i < 8) else "four16"
        vgroove(D, b, name, ghosts=0.25, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16")
        if last and n != "光回線": put_fill(D, b, "tomdown")
    elif n == "バグの嵐":
        D.set(b, "X..X..X.X..X....", "....X.......X...", "xxxx....xxxx....")
        if i % 2 == 1: D.S[b] = "....X...xxxxXXXX"
    elif n == "再起動":
        vgroove(D, b, "half", seed=b, h="x...x...x...x...")
        shape(b, k, i, L)
        if last: put_fill(D, b, "build")
    elif n == "サーバーの夜景":
        vgroove(D, b, "four", seed=b)
        if i == 0: crash(D, b)
        if i % 4 == 3: ride(D, b, "x.x.x.x.")
        if last: put_fill(D, b, "lift")
    elif n == "ログアウト":
        vgroove(D, b, "half", seed=b) if i < 6 else D.set(b, "X" + "." * 15, "." * 16, "." * 16)
        if i == 0: crash(D, b)
        if i == 6: crash(D, b, "C2", 8)                                    # 余韻: 電源が落ちる最後の2小節は、シンバルの鳴りだけ長く残す

# こもり（再起動の場面は、ベルとアルペジオがないので、歌の役と和音だけ。光回線の前4小節）
muffle(S, [ARP2, BASS], S.sc("サーバーの夜景")[-4:], 800)
# 止めと1拍の完全な無音
for name in ("ファイアウォール", "ファイアウォール2"): SIL.add(S.sc(name)[-1], 2, 4)
SIL.add(S.sc("バグの嵐")[-1], 3, 4)
SIL.apply()
S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の11。エレクトロニカ（デジタルの世界）。B短調（サビは D長調）・154、最後のサビは +2（E）。"
          "画面ごしの、まだ会ったことのない友だちへの気持ち。ベースだけで始まり、0と1のように1オクターブを行き来する Aメロ、止めのある Bメロ、4つ打ちのサビ、ジャージークラブの2サビ、"
          "バグの嵐と1拍の無音、Half feel の「おやすみ」、アルペジオのソロ、+2 の最後のサビ、ログアウト。Surge の音。自作")
S.flags += " --space sky --space-wet 0.16"
teto(S, LY, V, transpose=-5, special={"光回線": 0.55, "再起動": -0.5, "ログアウト": -0.5})
