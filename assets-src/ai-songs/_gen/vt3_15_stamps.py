# vt3 15「おばあちゃんのスタンプ」Grandma's Stamps（仮）— ポルカ。152・4/4（2拍子のノリ）。D長調 → 最後のサビは +1（E♭）・テンポが上がる。
# 書き出しは全体を半音下げる（テトの声に入れるため・D♭長調 → 最後は D）。
# 第3弾（0時〜24時の街）の 14時。表は docs/sound/vt3-plan.md。
# 物語: 山のむこうに住むおばあちゃんの、はじめてのメッセージ「げんきですか」。指いっぽんで、何分かけて打ったのかな。
#   返事をしたら、すぐにスタンプ。おじぎするねこ、花をくれるくま、ハートが3つ。教えたのは孫のわたしなのに、こんなに押すなんて。
#   電車の中でも、ぴこんぴこん。言葉より、たくさんの気持ちがつまっている。届いた音声メッセージには、ばあちゃんの鼻歌。
#   こんど会いに行くから。そのときは、スタンプよりも、ぎゅっとして。
# 場面と強さ: アコーディオン（ひと息・弱）→ イントロ（ポルカの節）→ Aメロ1（はずむ・中）→ Bメロ1（ぴこんぴこん）→ サビ1（強）
#   → 間奏（クラリネット・節）→ Aメロ2 → Bメロ2 → サビ2 → 間奏2（アコーディオンのソロ）→ げんき（アコーディオンと声だけ・とても弱い）
#   → 最後のサビ（+1・テンポが上がる・いちばん強い）→ スタンプ連打（速い）→ 通知音1つ
# 旋律の性格: 軽やかにはねる8分の2拍子、同じ音のくり返しから跳ぶ。サビは「ばあちゃんのすたんぷ」で上がっていく。
# この曲だけの音: アコーディオンの「ブン・チャッ」とチューバの低音（ポルカ）。最後のサビでテンポがだんだん上がる。
#   合いことばの節（3・5・6・5・2）は、間奏のクラリネット（ばあちゃんの音声メッセージの鼻歌）。
from vt25_lib import *

S = Song("15", "stamps", "おばあちゃんのスタンプ（仮）", "Grandma's Stamps", 152, 4, "D", "major", "ポルカ（ボカロ）")
S.kit = "naked-x"
S.flags = S.flags + " --space room --space-wet 0.14"
S.keep_old_synth = True
S.no_depth = True
S.open_hat_vol = 0.4
S.drum_scale = 0.85
K = Key("D", "major")          # oct 4 で 1 = D4
KL = Key("Eb", "major")        # 最後のサビ（+1）

A_CH = ["D", "A7", "A7", "D", "D", "A7", "A7", "D"]
B_CH = ["G", "D", "A7", "D", "G", "D", "E7", "A7"]
C_CH = ["D", "D", "G", "D", "A7", "A7", "D", "D", "G", "G", "D", "Bm", "Em", "A7", "D", "D"]
TUNE = ["D", "A7", "D", "A7", "G", "D", "A7", "D"]

S.scene("アコーディオン", 4, "intro", ["D", "D", "A7", "A7"])
S.scene("イントロ", 12, "intro", TUNE + TUNE[:4])
S.scene("Aメロ1", 16, "verse", A_CH)
S.scene("Bメロ1", 8, "pre", B_CH)
S.scene("サビ1", 16, "chorus", C_CH)
S.scene("間奏", 8, "break", TUNE)
S.scene("Aメロ2", 16, "verse", A_CH)
S.scene("Bメロ2", 8, "pre", B_CH)
S.scene("サビ2", 16, "chorus", C_CH)
S.scene("間奏2", 8, "solo", TUNE)
S.scene("げんき", 8, "bridge", ["G", "D", "Em", "A7", "G", "D", "Em", "Bb7"])        # 最後は E♭ への入り口
S.scene("最後のサビ", 24, "chorus", [tr_chord(c, 1) for c in C_CH + C_CH[:8]])
S.scene("スタンプ連打", 8, "outro", [tr_chord(c, 1) for c in TUNE])
S.scene("通知", 2, "outro", ["Eb", "Eb"])
S.tempo = [{"bar": S.sc("最後のサビ")[0] + 1, "bpm": 156}, {"bar": S.sc("最後のサビ")[8] + 1, "bpm": 162, "ramp": 8},
           {"bar": S.sc("スタンプ連打")[0] + 1, "bpm": 172, "ramp": 4}]

V = Voice(S, vol=0.2, delay=0.5, bright=0.0, patch="kfbSineLead" if VOCAL else "clarinet", low=False)   # v3: BGM の旋律をホルンからクラリネットに（歌の版 7.62 に対し BGM 7.45。旋律の音色がこもっていた）
ACC = [S.track(f"アコーディオン{i + 1}", "accordion", volume=0.065, pan=-0.3, reverb=0.25, sustain=0.5) for i in range(3)]
ACCM = S.track("アコーディオン（旋律）", "accordion", volume=0.11, pan=-0.15, reverb=0.28)
CLA = S.track("クラリネット", "lead", patch="clarinet", volume=0.11, pan=0.2, reverb=0.3)
TUBA = S.track("チューバ", "brass", patch="tuba", volume=0.13, pan=0, reverb=0.2)
FID = S.track("フィドル（のばす対旋律）", "fiddle", volume=0.07, pan=0.3, reverb=0.4)   # v2
GLK = S.track("通知音（グロッケン）", "glockenspiel", volume=0.06, pan=0.3, reverb=0.35)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌 =================
VA = ["R:1 3:0.5 3:0.5 3:0.5 2:0.5 3:0.5 4:0.5", "5:1 3:1 1:1 R:1", "R:1 2:0.5 2:0.5 2:0.5 1:0.5 2:0.5 3:0.5", "4:1 2:1 7,:1 R:1",
      "R:1 3:0.5 3:0.5 3:0.5 2:0.5 3:0.5 4:0.5", "5:1 6:1 5:1 R:1", "R:1 4:0.5 3:0.5 2:0.5 3:0.5 4:0.5 2:0.5", "1:2 R:2"]
A1 = ("やまのむこうにすむ/おばあちゃんのすまほ/はじめてのめっせーじ/げんきですかと/"
      "ゆびいっぽんでゆっくり/なんぷんかけたかな/へんじしたらすぐに/すたんぷがきた")
A2 = ("ねこがおじぎをする/くまがはなをくれる/はーとがみっつならぶ/おばあちゃんたら/"
      "おしえたのはまごの/わたしなんだけどね/こんなにおすなんて/おもわなかったよ")
VB = ["R:1 4:1 4:1 4:1", "6:2 4:1 R:1", "R:1 3:1 3:1 3:1", "5:2 3:1 R:1",
      "R:1 4:1 4:1 6:1", "1':2 6:1 R:1", "R:0.5 5:0.5 #4:0.5 5:0.5 6:0.5 7:0.5 1':1", "R:4"]
B1 = "ぴこんぴこ/とまらない/でんしゃでも/ふきだしたよ"
B2 = "ことばより/たくさんの/きもちがね/つまってるんだ"
VC = ["5:0.5 5:0.5 1':1 7:0.5 6:0.5 5:1", "3:1 4:1 5:1 R:1", "6:0.5 6:0.5 1':1 7:0.5 6:0.5 5:1", "3:2 R:2",
      "4:0.5 4:0.5 6:1 5:0.5 4:0.5 3:1", "2:1 3:1 4:1 R:1", "5:0.5 5:0.5 3':1 2':0.5 1':0.5 7:1", "1':2 R:2",
      "6:0.5 6:0.5 2':1 1':0.5 6:0.5 5:1", "4:1 5:1 6:1 R:1", "5:0.5 5:0.5 1':1 7:0.5 6:0.5 5:1", "6:2 R:2",
      "4:0.5 4:0.5 2':1 1':0.5 6:0.5 5:1", "5:1 3:1 2:1 R:1", "R:0.5 3:0.5 4:0.5 5:0.5 6:0.5 7:0.5 1':1", "1':3 R:1"]
HOOK = "ばあちゃんのすたんぷ"
C1 = f"{HOOK}/ぽんぽんとどく/えがおのねこがまた/おじぎしてるよ/{HOOK}/とおいまちから/がめんいっぱいのはな/さいてるみたい"
C2 = f"{HOOK}/ぽんぽんとどく/まちがえたうさぎも/かわいいからね/{HOOK}/いっこじゃたりない/わたしもおかえしに/たくさんおくった"
C3 = (f"{HOOK}/あいにいくから/でんしゃとばすをのり/やまをこえてね/{HOOK}/ほんものにあう/そのときはぎゅっとして/すたんぷよりも/"
      f"{HOOK}/またとどいたよ/おやすみのねこがね/ねむそうにふる")
GEN = ["R:4", "R:1 3:1 2:1 3:1", "R:4", "R:0.5 5:0.5 5:0.5 3:0.5 2:1 1:1", "R:4", "R:1 3:0.5 3:0.5 4:0.5 5:0.5 6:1", "R:4", "5:1 4:1 3:1 2:1"]
LY = Lyrics(S)


def put(name, key, lines, text, o=4):
    bars = S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, text, name)


put("Aメロ1", K, VA + VA, A1)
put("Bメロ1", K, VB, B1)
put("サビ1", K, VC, C1)
put("Aメロ2", K, VA + VA, A2)
put("Bメロ2", K, VB, B2)
put("サビ2", K, VC, C2)
if VOCAL: put("げんき", K, GEN, "げんき/げんきだよ/あいたいね/こんどね")
else:
    for b, l in zip(S.sc("げんき"), GEN): ACCM.bar(b, K.mel(l, oct=4))
put("最後のサビ", KL, VC + VC[:8], C3)

# ================= アコーディオン（ブン・チャッ）・チューバ =================
def oompah(b, ch, center=62):
    v = voice(ch, center, 3)
    for j in range(3): ACC[j].bar(b, f"R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5 R:0.5 {nm(v[j])}:0.5")


def tuba(b, ch):
    r = low(ch, "A1")
    TUBA.bar(b, f"{nm(r)}:0.5 R:0.5 {nm(r + 7 if r + 7 < 48 else r - 5)}:0.5 R:0.5 {nm(r)}:0.5 R:0.5 {nm(r + 7 if r + 7 < 48 else r - 5)}:0.5 R:0.5")


PTUNE = ["F#5:0.5 A5:0.5 F#5:0.5 D5:0.5 A4:1 D5:1", "E5:0.5 G5:0.5 E5:0.5 C#5:0.5 A4:1 R:1", "F#5:0.5 A5:0.5 D6:0.5 A5:0.5 F#5:1 D5:1", "E5:1 C#5:1 A4:1 R:1",
         "G5:0.5 B5:0.5 G5:0.5 D5:0.5 B4:1 D5:1", "F#5:0.5 A5:0.5 F#5:0.5 D5:0.5 A4:1 D5:1", "E5:0.5 F#5:0.5 G5:0.5 E5:0.5 C#5:1 E5:1", "D5:3 R:1"]
MOTIF = ["R:1 F#5:0.5 A5:0.5 B5:1 A5:0.5 E5:0.5", "D5:3 R:1"]      # 合いことばの節（3・5・6・5・2）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "アコーディオン":
        v = voice(ch, 62, 3)
        for j in range(3): ACC[j].bar(b, f"{nm(v[j])}:4" if i % 2 == 0 else f"{nm(v[j])}:3 R:1")
    elif n == "イントロ":
        oompah(b, ch); tuba(b, ch); CLA.bar(b, PTUNE[i % 8])
    elif n in ("Aメロ1", "Aメロ2", "Bメロ1", "Bメロ2", "サビ1", "サビ2", "最後のサビ"):
        if n in ("Bメロ1", "Bメロ2") and i == 7: continue
        oompah(b, ch); tuba(b, ch)
        # v2: 全体が 6.6〜7.3（アコーディオンの刻みとチューバだけで薄く、くり返しに聞こえる）
        #     → Aメロ2・サビでフィドルが長い対旋律（和音の上の音を2分でのばす）を弾き、音に広がりを足す
        if n in ("Aメロ2", "サビ1", "サビ2", "最後のサビ") or (n == "Aメロ1" and i >= 8):
            t = tones(ch, "A4", "A5"); FID.bar(b, f"{nm(t[-1])}:2 {nm(t[-2])}:2" if i % 2 == 0 else f"{nm(t[-2])}:4")
        if n in ("サビ1", "サビ2", "最後のサビ") and i % 4 == 3: CLA.bar(b, "R:2 " + " ".join(f"{nm(x)}:0.5" for x in tones(ch, "A4", "A5")[:4]))
    elif n == "間奏":
        oompah(b, ch); tuba(b, ch)
        CLA.bar(b, MOTIF[i] if i < 2 else PTUNE[i])
    elif n == "間奏2":
        oompah(b, ch, 58); tuba(b, ch); ACCM.bar(b, PTUNE[i])
    elif n == "げんき":
        v = voice(ch, 62, 3)
        for j in range(3): ACC[j].bar(b, f"{nm(v[j])}:4")
    elif n == "スタンプ連打":
        oompah(b, ch); tuba(b, ch); CLA.bar(b, shift_oct(PTUNE[i], 0)); ACCM.bar(b, shift_oct(PTUNE[i], -1))
    elif n == "通知":
        if i == 0:
            v = voice(ch, 62, 3)
            for j in range(3): ACC[j].bar(b, f"{nm(v[j])}:0.5 R:3.5")
            TUBA.bar(b, f"{nm(low(ch, 'A1'))}:0.5 R:3.5")

# 通知音（ぴこん）
for name in ("Bメロ1", "Bメロ2"):
    for i, b in enumerate(S.sc(name)[:4]): GLK.bar(b, "R:3 E6:0.25 A6:0.75")
GLK.bar(S.sc("通知")[1], "R:1 E6:0.25 A6:1.75 R:1")

# ================= ドラム（ポルカの2ビート）=================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n in ("アコーディオン", "げんき"):
        if n == "げんき" and i == 7: put_fill(D, b, "build")
        continue
    if n == "通知":
        if i == 0: D.set(b, "X...............", "X...............", "................"); crash(D, b, "C2", 6)
        continue
    if n in ("Bメロ1", "Bメロ2") and i == 7: continue
    hh = "x.x.x.x.x.x.x.x." if n in ("サビ1", "サビ2", "最後のサビ", "スタンプ連打") else "x...x...x...x..."   # v2: Aメロにも4分のハイハット
    vgroove(D, b, "beat8", ghosts=0.15, seed=b, k="X.......X.......", s="....X.......X...", h=hh)
    if n in ("サビ1", "サビ2", "最後のサビ", "間奏", "スタンプ連打") and i % 8 == 0: crash(D, b)
    if i % 8 == 7 and not last: put_fill(D, b, "small")
    if last and n in ("Aメロ1", "Aメロ2", "サビ1", "サビ2", "間奏", "間奏2"): put_fill(D, b, "snare16")

for name in ("Bメロ1", "Bメロ2"): SIL.add(S.sc(name)[-1], 0, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: 重音テトのボカロ曲25曲・第3弾の15（14時）。ポルカ。D長調・152、最後のサビは +1 でテンポが上がる。書き出しは全体を半音下げる。"
          "山のむこうのおばあちゃんが、はじめてスタンプを送ってくる。アコーディオンのブン・チャッ・チューバ・クラリネット。"
          "合いことばの節は間奏のクラリネット（ばあちゃんの鼻歌）。通知音「ぴこん」で終わる。自作")
finish(S, LY, V, -1,
       level={"verse": -0.15}, special={"げんき": -0.7, "最後のサビ": 0.4, "スタンプ連打": 0.2})

# ================= v2（2026-11-11 作り直し。docs/sound/vt3-remake-plan.md）=================
# この曲（午後2時・おばあちゃんから届くスタンプ・ポルカ）で直すこと:
#   生の楽器の曲なので、電子の音は足さない（歌をなぞる音だけ、高さの揺れない音に）。アコーディオンの伴奏は1音ずつ強さを揺らす
#   歌: Aメロ・Bメロはクリア、サビはキュート（スタンプのにぎやかさ）、「げんき」の所はウィスパー（ひとことの重さ）。ハモリは サビ2 の頭から（合唱のように）と最後のサビ
from vt3x_lib import *
path = sys.argv[1]
humanize(path, "アコーディオン", mid=84, down=10, up=8, seed=5)
final_gain(path, {"アコーディオン": 4, "サビ1": -0.5, "サビ2": 0.3, "最後のサビ": 1.5})
if VOCAL:
    remark(path, S, std_mark(("chorus",), jump=5))
    vocal_polish(path, S, {"verse": 8, "pre": 12, "chorus": 20, "最後のサビ": 24, "bridge": 6, "outro": 0}, scoop=0.3, slash=0.8, vib_min_beats=1.5, vib_start=0.5, auto=0.5, breaths=0.5)
    harmony(path, S, [("サビ2", 0, None, K), ("最後のサビ", 0, None, KL)], vol=0.36, shift=-1)
    voice_by_scene(path, S, {"verse": "clear", "pre": "clear", "chorus": "cute", "bridge": "whisper"}, default="clear")
