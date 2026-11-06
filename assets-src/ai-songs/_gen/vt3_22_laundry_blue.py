# vt3 22「コインランドリー・ブルー」Coin Laundry Blue（仮）— トリップホップ。86・4/4。C の短調（転調なし）。
# 第3弾（0時〜24時の街）の 21時。表は docs/sound/vt3-plan.md。
# 物語: 夜9時のコインランドリー。だれもいない店で、回るドラムをひとりで見ている。たたんだシャツの袖には、まだあの人のにおい。
#   百円玉をもうひとつ入れて、残り30分。窓のそとは雨。かなしい気持ちも、いっしょに乾かそう。ブザーが鳴るまで、もうすこしここで。
# 場面と強さ: 回る音（乾燥機の低い音と針の音）→ イントロ（重いブレイクビーツ・ビブラフォンの節）→ Aメロ1（語る・弱中）→ Bメロ1
#   → サビ1（乾燥が終わる・控えめ）→ 間奏（ビブラフォン）→ Aメロ2 → Bメロ2 → サビ2 → 機械の音だけ（ベースと回る音・静か）
#   → 最後のサビ（ストリングスがいちばん厚い）→ ブザー（終わりの合図）
# 旋律の性格: 低くけだるい短い句（C4〜F5）。Aメロは1小節に1つの句。
# この曲だけの音: 重いブレイクビーツ（ゆっくり・太いスネア）、サンプル風のストリングス（長い和音）、ビブラフォン、針の音（小さな雨の音で代わりに）。
#   合いことばの節（3・5・6・5・2＝E♭・G・A♭・G・D）は、ビブラフォン。
from vt25_lib import *

S = Song("22", "laundryblue", "コインランドリー・ブルー（仮）", "Coin Laundry Blue", 86, 4, "C", "minor", "トリップホップ（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --piano salamander --space room --space-wet 0.18"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.35
S.drum_scale = 1.0
K = Key("C", "minor")          # oct 4 で 1 = C4

A_CH = ["Cm9", "Abmaj7", "Fm9", "G7#9"]
B_CH = ["Ebmaj7", "Dm7b5", "Cm7", "Abmaj7", "Fm9", "Dm7b5", "Gsus4", "G7b9"]
C_CH = ["Abmaj7", "Bbadd9", "Gm7", "Cm9", "Fm9", "Bb7", "Ebmaj7", "G7sus4"]

S.scene("回る音", 4, "intro", ["Cm9", "Cm9", "Abmaj7", "G7#9"])
S.scene("イントロ", 8, "intro", A_CH)
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 8, "chorus", C_CH)
S.scene("間奏", 8, "solo", A_CH)
S.scene("Aメロ2", 8, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 8, "chorus", C_CH)
S.scene("機械の音だけ", 4, "break", ["Cm9", "Abmaj7", "Fm9", "G7#9"])
S.scene("最後のサビ", 16, "chorus", C_CH)
S.scene("ブザー", 2, "outro", ["Cm9", "Cm9"])

V = Voice(S, vol=0.21, delay=0.5, bright=-0.2, patch="surgeKeysFmPiano1", low=True)
VIB = S.track("ビブラフォン", "harp", patch="vibraphone", volume=0.08, pan=0.35, reverb=0.4, sustain=1.5, bright=-0.2)
STR = [S.track(f"ストリングス（サンプル風）{i + 1}", "strings", patch="stringEnsemble", volume=0.05, pan=-0.4 + 0.4 * i, reverb=0.5, sustain=1.6) for i in range(3)]
PN = [S.track(f"ピアノ{i + 1}", "piano", volume=0.06, pan=-0.2, reverb=0.35, fx=[{"type": "eq", "low": -3, "mid": -1, "midHz": 500, "high": -4}]) for i in range(3)]
BASS = S.track("ベース", "bass", **finger_bass_spec(vol=0.24))
HUM = S.track("乾燥機の回る音", "sub808", volume=0.07, pan=0, sustain=1.0, fx=[{"type": "filter", "kind": "highpass", "freq": 30, "q": 0.7}])
BUZ = S.track("ブザー", "pad", patch="squareLead", volume=0.04, pan=0, reverb=0.2)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.05, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:1 3:0.5 2:0.5 1:1 R:1", "R:0.5 1:0.5 3:0.5 4:0.5 5:1 R:1", "R:1 5:0.5 4:0.5 3:1 R:1", "R:0.5 2:0.5 3:0.5 2:0.5 1:1.5 R:0.5",
      "R:1 3:0.5 4:0.5 5:1 R:1", "R:0.5 6:0.5 5:0.5 4:0.5 3:1 R:1", "R:1 4:0.5 3:0.5 2:1 R:1", "R:0.5 3:0.5 2:0.5 2:0.5 1:1.5 R:0.5"]
A1 = ("まわる/どらむを/みてる/ひとりで/あわの/なかには/きのう/ことばが/"
      "よるの/くじすぎ/だれも/いないね/あかり/ちらちら/とけい/まわるよ")
A2 = "かごに/たたんだ/しゃつの/そでには/きみの/においが/まだね/のこるの"
VB = ["R:0.5 5:0.5 5:0.5 4:0.5 5:0.5 6:0.5 5:1", "4:2 R:2", "R:0.5 4:0.5 4:0.5 3:0.5 4:0.5 5:0.5 4:1", "3:2 R:2",
      "R:0.5 3:0.5 4:0.5 5:0.5 6:0.5 1':0.5 6:1", "7:2 R:2", "R:0.5 6:0.5 5:0.5 4:0.5 3:0.5 2:0.5 3:1", "2:2 R:2"]
B1 = "ひゃくえんだまを/ひとついれたら/のこりさんじゅう/かんがえごとを"
B2 = "まどのそとでは/あめがふりだす/かさはないけど/かわくまでいる"
VC = ["R:0.5 1':0.5 1':0.5 7:0.5 1':1 3':1", "2':1.5 1':0.5 7:1 R:1", "R:0.5 6:0.5 6:0.5 5:0.5 6:1 1':1", "5:1.5 4:0.5 3:1 R:1",
      "R:0.5 1':0.5 1':0.5 7:0.5 1':1 4':1", "3':1.5 2':0.5 1':1 R:1", "R:0.5 6:0.5 5:0.5 4:0.5 3:1 2:1", "1:3 R:1"]
HOOK = "こいんらんどりの"
C1 = f"{HOOK}/あおいよるのなか/まわるおもいでを/ほしてゆこう"
C2 = f"{HOOK}/ぶざあがなるまで/かなしいきもちも/かわかそうよ"
C3 = f"{HOOK}/あしたのしゃつには/ちいさなきぼうを/たたんでおく/{HOOK}/ぶざあがなるまで/もうすこしここで/やすんでこう"
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
put("最後のサビ", VC + VC, C3)

# ================= ストリングス・ピアノ・ビブラフォン =================
def strings(b, ch, c=60):
    v = voice(ch, c, 3)
    for j in range(3): STR[j].bar(b, f"{nm(v[j])}:4")


def piano(b, ch, busy=False):
    v = voice(ch, 60, 3)
    pat = "{0}:1.5 R:1 {0}:0.5 R:1" if busy else "{0}:2 R:2"
    for j in range(3): PN[j].bar(b, pat.format(nm(v[j])))


MOTIF = ["R:1 Eb4:0.5 G4:0.5 Ab4:1 G4:0.5 D4:0.5", "C4:3 R:1"]     # 合いことばの節（3・5・6・5・2）
SOLO = ["R:0.5 G4:0.5 Bb4:0.5 C5:0.5 Eb5:1 D5:1", "C5:1.5 Bb4:0.5 G4:2", "R:0.5 Ab4:0.5 C5:0.5 Eb5:0.5 F5:1 Eb5:1", "D5:1.5 B4:0.5 G4:2"]
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "回る音":
        # v2: 「回る音」の4小節が 5.66（乾燥機の低い音と雨の音だけで、音楽がなかった）
        #     → 1小節目からストリングス、3小節目からビブラフォンの節とピアノ
        strings(b, ch, 58)
        if i >= 2: VIB.bar(b, MOTIF[i % 2]); piano(b, ch)
    elif n == "イントロ":
        piano(b, ch); VIB.bar(b, MOTIF[i % 2])
        if i >= 4: strings(b, ch, 58)
    elif n in ("Aメロ1", "Aメロ2"):
        piano(b, ch, busy=i % 2 == 1)
        if n == "Aメロ2" or i >= 8: strings(b, ch, 56)
        if i % 4 == 3: VIB.bar(b, "R:2 G4:0.5 Eb4:0.5 C4:1")
    elif n in ("Bメロ1", "Bメロ2"):
        piano(b, ch); strings(b, ch, 60)
    elif n in ("サビ1", "サビ2", "最後のサビ"):
        piano(b, ch, busy=True); strings(b, ch, 62 if n == "最後のサビ" else 60)
        if i % 2 == 1: VIB.bar(b, "R:2.5 Eb5:0.5 D5:0.5 C5:0.5")
    elif n == "間奏":
        piano(b, ch); strings(b, ch, 58)
        VIB.bar(b, MOTIF[i % 2] if i < 2 else SOLO[(i - 2) % 4])
    elif n == "機械の音だけ":
        if i >= 2: VIB.bar(b, MOTIF[i % 2])
    elif n == "ブザー":
        strings(b, ch, 58) if i == 0 else None

BUZ.bar(S.sc("ブザー")[1], "C5:1.5 R:2.5")
season(S, S.sc("機械の音だけ")[0], "雨", beats=16, vol=0.03, every=4)

# ================= ベースと回る音 =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]; r = low(ch, "E1")
    if n in ("回る音", "機械の音だけ", "ブザー"):
        HUM.bar(b, "C1:4")
        if n == "機械の音だけ": BASS.bar(b, f"{nm(r)}:2.5 R:0.5 {nm(r)}:0.5 {nm(r + 7)}:0.5")
        continue
    if n in ("サビ1", "サビ2", "最後のサビ"):
        BASS.bar(b, f"{nm(r)}:1.5 {nm(r)}:0.5 R:0.5 {nm(r + 7)}:0.5 {nm(r + 10)}:0.5 {nm(r + 12)}:0.5")
    else:
        BASS.bar(b, f"{nm(r)}:2.5 R:0.5 {nm(r)}:0.5 {nm(r + 7)}:0.5")
    if n == "イントロ" and i < 2: HUM.bar(b, "C1:4")

cym_swell(CYM, S.sc("サビ1")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のサビ")[0], 2, "C4")

# ================= ドラム（重いブレイクビーツ）=================
BK, BSN, BH = "X.....X...X.....", "....X.......X..x", "x.x.x.x.x.x.x.x."
BK2 = "X.....X..XX....."
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("回る音", "ブザー"): continue
    if n == "機械の音だけ":
        if i >= 2: D.set(b, "................", "................", "x...x...x...x...")
        continue
    vgroove(D, b, "beat8", ghosts=0.25, seed=b, k=BK2 if i % 4 == 3 else BK, s=BSN, h=BH)
    if n in ("サビ1", "サビ2", "最後のサビ") and i % 8 == 0: crash(D, b, "C2", 4)
    if n == "イントロ" and i == 0: crash(D, b, "C2", 4)
    if last and n in ("Bメロ1", "Bメロ2", "間奏"): put_fill(D, b, "small")

SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の22（21時）。トリップホップ。C の短調・86。夜のコインランドリーで、回るドラムを見ながらひとりで考えごと。"
          "重いブレイクビーツ・サンプル風のストリングス・ビブラフォン・ベース。乾燥機の低い音で始まり、終わりのブザーで終わる。"
          "合いことばの節はビブラフォン。自作")
finish(S, LY, V, 0,
       level={"verse": -0.25}, special={"機械の音だけ": -0.4, "最後のサビ": 0.3, "回る音": -0.2})
