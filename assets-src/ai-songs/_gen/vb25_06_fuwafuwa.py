# vb25 06「ふわふわ現象論」Fluffy Phenomenon Theory（仮）— ダンス（フューチャーベース）。B長調（サビ・ドロップは G#短調）・150・4/4
# 2026-10-25 作り直し: 物語を人の気持ちの話に（前は雲が綿あめになる話）、歌を人が歌える旋律（8分と4分）に、音を Surge の音に、テトの歌の版を足した。
# 物語: 君が笑った瞬間、足もとがふわりと浮いた。朝の電車も、階段も、雲の上を歩いているみたい。この気持ちに名前をつけられないまま、
#   ふくらんでいく「会いたい」。途中で「ばかみたい」とこわくなって足がすくむけれど、もう一度上を向いて、雲の上の君のところへ。
# 場面と強さ: 短いサビ（ドロップの先取り）→ 君が笑った朝（Aメロ・歌と声のチョップの掛け合い）→ 名前がない（Bメロ・フィルターが閉じていく）
#   → ふわり（1サビ＝ドロップ・歌の呼びかけにチョップが答える）→ 間奏（ベルの主旋律）→ 朝の電車（2番。BGM はベルが歌を受け取る）→ Bメロ2
#   → ハーフのサビ → 1拍の完全な無音 → 足がすくむ（静けさ）→ 落ちサビ（ベルと歌だけ）→ もう一度上へ（フィルターが開く）→ 最後のドロップ → 風だけ残す
# 旋律の性格: Aメロは句の頭を休んで入る8分（D#4〜D#5）。ドロップは「ふわり」の同じ音3つの呼びかけ。最高音 F#5。
# ほかの曲とちがう所: 3・3・2 で刻む厚い和音とフィルターの開閉、声のチョップとの掛け合い、ドロップの後半だけ歌が続く。
from vb25_lib import *

S = Song("06", "fuwafuwa", "ふわふわ現象論（仮）", "Fluffy Phenomenon Theory", 150, 4, "B", "major", "ダンス（フューチャーベース・ボカロ）")
S.kit = "electro"
S.flags = "--ref-tone glossy-jrock " + S.flags
S.keep_old_synth = True
S.no_depth = True
K = S.key                    # B 長調（Aメロ・Bメロ）
KM = Key("G#", "minor")      # サビ・ドロップ（G# 短調）


def chk(*lists):
    for L in lists:
        for x in L:
            t = sum(float(tok.split(":", 1)[1].rstrip("!,'_~^/\\")) for tok in x.split())
            assert abs(t - 4) < 1e-6, ("4拍ではない行", t, x)


A_CH = ["Bmaj7", "D#m7", "Emaj7", "F#", "Bmaj7", "D#7", "G#m7", "F#sus4"]          # D#7＝vi（G#m）への副属和音
B_CH = ["Emaj7", "F#", "D#m7", "G#m7", "C#m7", "D#m7", "Emaj7", "F#"]
D_CH = ["Emaj7", "F#6", "D#m7", "G#m9", "Emaj7", "F#", "D#7", "G#m"]               # D#7＝G# 短調の V（長調の V）
GAP = ["Emaj9", "Emaj9", "C#m9", "C#m9", "Emaj9", "Emaj9", "C#m9", "D#7sus4"]
UP_CH = ["Emaj7", "F#", "D#m7", "G#m7", "C#m7", "D#m7", "Baug", "D#7"]             # Baug＝増三和音

S.scene("バスドラ2回", 1, "intro", [D_CH[-1]])        # 2026-10-26 人間「バスドラ２回踏んでから曲はいろうか」
S.scene("短いサビ", 8, "intro", D_CH)
S.scene("綿あめの朝", 16, "verse", A_CH)
S.scene("足元ふわふわ", 8, "pre", B_CH)
S.scene("雲の上へ", 16, "chorus", D_CH)
S.scene("鳥と並んで", 8, "interlude", D_CH)
S.scene("雲の通学路", 16, "verse", A_CH)
S.scene("足元ふわふわ2", 8, "pre", B_CH)
S.scene("ハーフのサビ", 16, "chorus", D_CH)
S.scene("雲が切れて", 8, "break", GAP)
S.scene("落ちサビ", 8, "bridge", D_CH)
S.scene("もう一度上へ", 8, "build", UP_CH)
S.scene("最後のドロップ", 32, "chorus", D_CH)
S.scene("風", 8, "outro", ["Emaj9", "Emaj9", "G#m9", "G#m9", "G#m9", "G#m9", "G#m9", "G#m9"])

# ================= パート =================
V = Voice(S, vol=0.22, delay=0.75, patch="surgeResofest", low=True)
# 2026-10-26 人間（06）「リードが歪強いから少し抑えよう」: 歌の役とチョップの高い所のざらつきを削る
V.main.spec["fx"].insert(1, {"type": "filter", "kind": "lowpass", "freq": 5800, "q": 0.7}); V.main.spec["fx"].insert(2, {"type": "eq", "low": 0, "mid": -2.5, "midHz": 3200, "high": -1})   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
CHOP = S.track("声のチョップ風シンセ", "lead", patch="surgeTropics", volume=0.12, pan=0.12, reverb=0.2, mono=True, gainDb=1,
               fx=[{"type": "filter", "kind": "highpass", "freq": 220, "q": 0.7}, {"type": "eq", "low": 0, "mid": 5, "midHz": 520, "high": 0},
                   {"type": "eq", "low": 0, "mid": 3.5, "midHz": 1150, "high": -1}, {"type": "filter", "kind": "lowpass", "freq": 5200, "q": 0.7},
                   {"type": "eq", "low": 0, "mid": -2, "midHz": 3000, "high": 0},
                   {"type": "pingpong", "beats": 0.5, "mix": 0.16, "feedback": 0.25}])
BELL = S.track("ベル（主旋律の受け渡し・きらめき）", "pad", patch="surgeKeysBellPiano", volume=0.09, pan=-0.2, reverb=0.45, sustain=1.0)
SAW = [S.track(f"スーパーソウ{i + 1}", "pad", **pad_spec("surgeChordFreeform", vol=0.055, pan=0.0, duck=0.6, sustain=0.8)) for i in range(4)]
SAWC = [S.track(f"閉じたスーパーソウ{i + 1}（800Hz）", "pad", patch="surgeChordFreeform", volume=0.06, pan=0.0, reverb=0.35, sustain=0.8, duck=0.4,
                fx=[{"type": "filter", "kind": "lowpass", "freq": 800, "q": 0.9}]) for i in range(3)]
SAWH = [S.track(f"半分ひらいたスーパーソウ{i + 1}（2kHz）", "pad", patch="surgeChordFreeform", volume=0.058, pan=0.0, reverb=0.35, sustain=0.8, duck=0.5,
                fx=[{"type": "filter", "kind": "lowpass", "freq": 2000, "q": 0.9}]) for i in range(3)]
# 2026-10-26 人間（06）「もうすこしベースの音大きくしていい」→ 0.24→0.29（1.2倍）、バスドラでの沈み 0.35→0.25、輪郭の 800Hz を少し足す
BASS = S.track("シンセベース", "bass", **synth_bass_spec("surgeBassWarmSquare", vol=0.29, duck=0.25))
BASS.spec["fx"] = list(BASS.spec.get("fx", [])) + [{"type": "eq", "low": 0, "mid": 2, "midHz": 800, "high": 0}]
ARP = S.track("プラックのアルペジオ", "pad", **pluck_spec("surgeWaveguide", vol=0.075, pan=0.35, delay=0.75, sustain=0.5))
PAD = [S.track(f"雲のパッド{i + 1}", "pad", **pad_spec("surgePadCrystals", vol=0.07, pan=0.0, duck=0.0, sustain=2.5)) for i in range(3)]
FX = S.track("効果音（風のノイズ・ライザー）", "pad", patch="fxRiser", volume=0.075, pan=0, reverb=0.4)
CYM = S.track("シンバルの効果音（風のロール）", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の旋律と歌詞（Aメロ・Bメロ・もう一度上へは B長調 oct=3＝B3。ドロップは G#短調 oct=3＝G#3（G#3 は使わない）） =================
VERSE = ["R:0.5 5:0.5 5:0.5 6:0.5 1':0.5 7:1 R:0.5", "5:1 3:1.5 R:1.5",
         "R:0.5 4:0.5 4:0.5 6:0.5 1':0.5 2':1 R:0.5", "1':1 7:1.5 R:1.5",
         "R:0.5 1':0.5 1':0.5 2':0.5 3':0.5 2':1 R:0.5", "7:1 2':1.5 R:1.5",
         "R:0.5 6:0.5 6:0.5 7:0.5 1':0.5 2':1 R:0.5", "1':1 5:1.5 R:1.5",
         "R:0.5 3':0.5 3':0.5 2':0.5 1':0.5 7:1 R:0.5", "6:1 5:1.5 R:1.5",
         "R:0.5 6:0.5 6:0.5 1':0.5 3':0.5 2':1 R:0.5", "2':1 1':1.5 R:1.5",
         "R:0.5 5:0.5 5:0.5 6:0.5 7:0.5 1':1 R:0.5", "2':1 7:1.5 R:1.5",
         "R:0.5 1':0.5 7:0.5 6:0.5 5:0.5 6:1 R:0.5", "5:1 4:1.5 R:1.5"]
V1 = "きみがわらうと/そのしゅんかんに/あしもとがほら/ふわりとうくの/かいだんさえも/くもあしになる/むねにわたぐも/これはなにかな"
V2 = "あさのでんしゃで/まどのむこうの/くもがきょうはね/わたあめみたい/つりかわさえも/ふうせんのよう/きみのなまえを/したでころがす"
BM = ["R:0.5 4:0.5 4:0.5 4:0.5 5:0.5 6:1 R:0.5", "5:1 2:1.5 R:1.5", "R:0.5 5:0.5 5:0.5 5:0.5 6:0.5 7:1 R:0.5", "1':1 6:1.5 R:1.5",
      "R:0.5 6:0.5 6:0.5 6:0.5 1':0.5 2':1 R:0.5", "2':1 7:1.5 R:1.5", "R:0.5 1':0.5 2':0.5 3':0.5 4':0.5 5':1 R:0.5", "4':1 2':1.5 R:1.5"]
P1 = "むねのたいこが/なりやまないの/このきもちには/なまえがないの"
P2 = "ねえきみはいま/なにをみてるの/おなじそらなら/ほほえむのにな"
DR = ["R:0.5 5':0.5 5':0.5 5':0.5 R:2", "R:0.5 4':0.5 4':0.5 4':0.5 6':1 3':1",
      "R:0.5 3':0.5 3':0.5 3':0.5 R:2", "R:0.5 5:0.5 3':0.5 5':0.5 4':2",
      "R:0.5 5':0.5 5':0.5 5':0.5 R:2", "R:0.5 4':0.5 4':0.5 4':0.5 6':1 3':1",
      "R:0.5 5:0.5 #7:0.5 2':0.5 4':1.5 2':0.5", "1':3 R:1",
      "R:0.5 5':0.5 5':0.5 5':0.5 4':0.5 3':0.5 1':1", "R:0.5 4':0.5 4':0.5 4':0.5 3':0.5 2':0.5 5:1",
      "R:0.5 5:0.5 5':0.5 4':0.5 3':1 2':1", "3':0.5 2':0.5 5:0.5 3':0.5 1':2",
      "R:0.5 6':0.5 6':0.5 6':0.5 5':1 1':1", "R:0.5 4':0.5 4':0.5 4':0.5 6':1 4':1",
      "R:0.5 5:0.5 #7:0.5 2':0.5 4':1.5 2':0.5", "1':2 3:1 1':1"]
D1A = "ふわり/そらへとぶ/ふわり/くもあし/ふわり/くもをこえ/きみのそばへ"
D1B = "あいたいのに/ふくらんでく/わたあめみたいだよね/ふわふわの/このこころ/きみにとどくかな"
D2A = "ふわり/ゆめのなか/ふわり/とけそう/ふわり/てをのばす/きみのそばへ"
D2B = "ふたもじのね/いえそうなの/くものうえにいこうよ/ふわふわの/このこころ/きみにとどけたい"
LASTX = ["R:0.5 6':0.5 6':0.5 6':0.5 5':0.5 4':0.5 3':1", "R:0.5 6':0.5 6':0.5 6':0.5 4':1 2':1",
         "R:0.5 5':0.5 5':0.5 5':0.5 3':0.5 1':0.5 3':1", "5':1 6':1 7':2",
         "R:0.5 6':0.5 6':0.5 6':0.5 5':0.5 4':0.5 3':1", "R:0.5 6':0.5 6':0.5 6':0.5 4':1 6':1",
         "R:0.5 5:0.5 #7:0.5 2':0.5 4':2", "4':2 3':1 1':1"]
LASTV = "だいすきだよ/むねがいう/そらのはてへとどけ/ふたもじをね/むねがいう/きみのそばにね"
GP = ["R:4", "R:2 3':1 2':1", "1':3 R:1", "R:2 5:1 7:1", "1':2 3':2", "2':3 R:1", "R:1 7:1 5:1 3:1", "5:4"]
GPV = "すくむ/おちそうで/それでも"
UPL = ["R:0.5 4:0.5 6:0.5 1':0.5 3':1 3':1", "R:0.5 5:0.5 7:0.5 2':0.5 4':1 4':1", "R:0.5 3:0.5 5:0.5 7:0.5 2':1 2':1", "R:0.5 6:0.5 1':0.5 3':0.5 5':2",
       "R:0.5 2':0.5 2':0.5 2':0.5 3':1 4':1", "R:0.5 3':0.5 3':0.5 3':0.5 4':1 5':1", "R:0.5 1':0.5 1':0.5 3':0.5 3':2", "R:0.5 2':0.5 7:0.5 2':0.5 3':1 R:1"]
UPV = "もういちど/うえをむく/ひざがゆれ/いくんだ/きみのいる/そらのうえ/はばたけ/いまだよ"
CHR = ["R:2 3':0.25 3':0.25 R:0.25 1':0.25 7:0.25 1':0.25 3':0.5", "R:2.5 4':0.25 2':0.25 7:0.25 2':0.25 R:0.5",
       "R:2 1':0.25 1':0.25 R:0.25 5:0.25 7:0.25 5:0.25 1':0.5", "R:3 2':0.25 1':0.25 7:0.25 5:0.25",
       "R:2 3':0.25 3':0.25 R:0.25 4':0.25 3':0.25 1':0.25 5:0.5", "R:2.5 2':0.25 1':0.25 7:0.25 4:0.25 R:0.5",
       "R:3.5 #7:0.25 2':0.25", "R:3 5:0.25 7:0.25 1':0.25 3':0.25"]
chk(VERSE, BM, DR, CHR, LASTX, GP, UPL)
LY = Lyrics(S)
def put(name, key, lines, text, low=True, rng=None, o=3):
    bars = S.sc(name)[rng] if rng else S.sc(name); mel = [key.mel(x, oct=o) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m, low=low)
    LY.flow(bars, mel, text, name)
put("綿あめの朝", K, VERSE, V1)
if VOCAL: put("雲の通学路", K, VERSE, V2)
else:
    for i, b in enumerate(S.sc("雲の通学路")):
        if i < 8: BELL.bar(b, K.mel(VERSE[i], oct=4))                # BGM: 2番の前半は、ベルが歌を受け取る（1オクターブ上）
        else: V.bar(b, K.mel(VERSE[i], oct=3))
put("足元ふわふわ", K, BM, P1); put("足元ふわふわ2", K, BM, P2)
put("雲の上へ", KM, DR, D1A + "/" + D1B); put("ハーフのサビ", KM, DR, D2A + "/" + D2B)
put("短いサビ", KM, DR[8:], D1B)                                     # 始まりは、ドロップの後半を先取り
put("雲が切れて", KM, GP, GPV, low=False)
put("落ちサビ", KM, DR[:8], D1A, low=False)
put("もう一度上へ", K, UPL, UPV)
put("最後のドロップ", KM, DR + LASTX + DR[8:], D2A + "/" + D1B + "/" + LASTV + "/" + D1B)


# ================= 声のチョップ =================
for name in ("雲の上へ", "最後のドロップ", "短いサビ"):
    for i, b in enumerate(S.sc(name)):
        if name == "短いサビ": CHOP.bar(b, KM.mel(CHR[i % 8], oct=4)); continue
        if i < 8 or (name == "最後のドロップ" and 16 <= i < 24): CHOP.bar(b, KM.mel(CHR[i % 8], oct=4))
for i, b in enumerate(S.sc("ハーフのサビ")):
    if i < 8: CHOP.bar(b, KM.mel(CHR[i % 8], oct=3))                     # ハーフでは1オクターブ下で答える
# Aメロ前半: 歌の休む最後の1拍に、チョップが答える
ANS = ["R:3 5:0.25 1':0.25 R:0.25 1':0.25", "R:3 3:0.25 7:0.25 R:0.25 7:0.25", "R:3 4:0.25 1':0.25 R:0.25 2':0.25", "R:3 5:0.25 7:0.25 2':0.25 R:0.25"]
for name in ("綿あめの朝",):
    for i, b in enumerate(S.sc(name)):
        if i < 7 and i % 2 == 1: CHOP.bar(b, K.mel(ANS[i % 4], oct=3))
# 間奏（鳥と並んで）: ベルの主旋律とチョップの掛け合い
BIRD = ["5':0.5 3':0.5 1':0.5 3':0.5 5':1 4':1", "3':0.5 2':0.5 1':0.5 7:0.5 2':2", "1':0.5 3':0.5 5':0.5 7':0.5 5':1 3':1", "4':1 3':0.5 2':0.5 #7:2"]
chk(BIRD)
for i, b in enumerate(S.sc("鳥と並んで")):
    BELL.bar(b, KM.mel(BIRD[i % 4], oct=4))
    CHOP.bar(b, KM.mel(["R:3 3':0.25 1':0.25 5:0.5", "R:3 2':0.25 7:0.25 4:0.5"][i % 2], oct=4))
# 落ちサビ: ベルが和音をゆっくり
for i, b in enumerate(S.sc("落ちサビ")):
    t = tones(S.chords[b], "G#4", "G#6"); BELL.bar(b, " ".join(f"{nm(t[q % len(t)])}:1" for q in (0, 2, 4, 3)))
for i, b in enumerate(S.sc("雲が切れて")):
    if i % 2 == 0: BELL.bar(b, KM.mel("5':1 3':1 1':2", oct=4))

# ================= 伴奏 =================
FB = "X:0.75 X:0.75 X:0.5 X:0.75 X:0.75 X:0.5"           # フューチャーベースの和音のノリ（3・3・2）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    v = voice(ch, 64, 4)
    drop = n in ("雲の上へ", "最後のドロップ", "短いサビ")
    if drop:
        for j in range(4): SAW[j].bar(b, FB.replace("X", nm(v[j])))
    elif n == "ハーフのサビ":
        for j in range(4): SAW[j].bar(b, f"{nm(v[j])}:2 {nm(v[j])}:1.5 {nm(v[j])}:0.5")
    elif n.startswith("足元ふわふわ"):
        if i >= 6:
            for j in range(3): SAWC[j].bar(b, FB.replace("X", nm(v[j])))       # フィルターが閉じる（800Hz）
        elif i >= 4:
            for j in range(3): SAWH[j].bar(b, FB.replace("X", nm(v[j])))       # 半分閉じる（2kHz）
    elif n == "もう一度上へ":
        if i < 4:
            for j in range(3): SAWC[j].bar(b, FB.replace("X", nm(v[j])))       # 閉じた所から
        else:
            for j in range(3): SAWH[j].bar(b, FB.replace("X", nm(v[j])))       # 開いていく → ドロップの頭で全部ひらく
    # 雲のパッド
    if n in ("綿あめの朝", "雲の通学路") or n in ("雲が切れて", "落ちサビ", "風") or (n.startswith("足元") and i < 4):
        if not (n == "風" and i >= 6):
            vv = voice(ch, 60, 3)
            for j in range(3): PAD[j].bar(b, f"{nm(vv[j])}:4")
    # プラックのアルペジオ（Aメロ・Bメロ）
    if n in ("綿あめの朝", "雲の通学路") and i >= 4 or n.startswith("足元"):
        t = tones(ch, "B3", "B5"); ARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 1, 3, 2, 4, 3, 1)))
    if drop and i % 4 == 3:
        t = tones(ch, "G#3", "G#5"); ARP.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" for q in (0, 1, 2, 3, 4, 5, 6, 7, 7, 6, 5, 4, 3, 2, 1, 0)))
    # ベース
    if drop: BASS.bar(b, bass_line(S, b, "oct8") if i % 2 == 0 else bass_line(S, b, "push"))
    elif n == "ハーフのサビ": BASS.bar(b, bass_line(S, b, "half"))
    elif n in ("綿あめの朝", "雲の通学路"): BASS.bar(b, bass_line(S, b, "long" if i < 8 else "root8"))
    elif n.startswith("足元"): BASS.bar(b, bass_line(S, b, "root8") if i < 6 else f"{nm(low(ch, 'E1'))}:4")
    elif n == "鳥と並んで": BASS.bar(b, bass_line(S, b, "house"))
    elif n == "落ちサビ": BASS.bar(b, f"{nm(low(ch, 'E1'))}:4" if i >= 4 else "R:4")
    elif n == "もう一度上へ": BASS.bar(b, bass_line(S, b, "root8" if i < 6 else "pulse"))

# 風の音（シンバルのロールとノイズで）・ライザー
riser(FX, S.sc("雲の上へ")[0], 8, "D4"); riser(FX, S.sc("ハーフのサビ")[0], 4, "C4"); riser(FX, S.sc("最後のドロップ")[0], 8, "D4")
FX.bar(S.sc("雲が切れて")[0], "G4:4")                                    # サブドロップ（下が見える）
FX.bar(S.sc("雲が切れて")[2], "A4:2 R:2"); FX.bar(S.sc("雲が切れて")[5], "A4:2 R:2")     # 風の「シュッ」
CYM.bar(S.sc("風")[0], "E4:8")                                          # 風がふくらむ（スウェル）
CYM.bar(S.sc("風")[2], "B4:24")                                         # ロールのディミヌエンドで、風だけが残る
FX.bar(S.sc("風")[5], "A4:3 R:1"); FX.bar(S.sc("風")[7], "A4:4")
cym_swell(CYM, S.sc("鳥と並んで")[0], 2, "C4")

# ================= ドラム（電子のドラム） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "バスドラ2回": D.set(b, "........X...X...", "." * 16, "." * 16)   # 3拍目・4拍目にバスドラだけ
    elif n == "短いサビ":
        vgroove(D, b, "four", seed=b)
        if i == 0: crash(D, b)
        if last: put_fill(D, b, "small")
    elif n in ("綿あめの朝", "雲の通学路"):
        if i < 8: vgroove(D, b, "twostep" if n == "綿あめの朝" else "trap", ghosts=0.25, seed=b)
        else: vgroove(D, b, "four16", seed=b)
        if i == 0: crash(D, b, "G2")
        if i == 7: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
    elif n.startswith("足元ふわふわ"):
        vgroove(D, b, "four" if i < 4 else "four16", seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: D.set(b, "X...X...X...X...", "....x...x.x.XXXX", "." * 16)
    elif n == "雲の上へ" or (n == "最後のドロップ" and i < 16):
        vgroove(D, b, "four", seed=b)                                        # 1サビ＝ドロップ（4つ打ち）
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16")
    elif n == "ハーフのサビ" or (n == "最後のドロップ" and i >= 16):
        vgroove(D, b, "half" if n == "ハーフのサビ" else "halfdrive", ghosts=0.3, seed=b)   # 2サビ＝ハーフ（Half feel）
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "tomtrip")
        if last and n == "最後のドロップ": D.set(b, "X.......X.......", "....X.......X...", "." * 16)
    elif n == "鳥と並んで":
        vgroove(D, b, "twostep", seed=b)
        D.cym(b, ("C2:0.5 " if i == 0 else "F2:0.5 ") + "D2:0.5 " * 7); D.H[b] = "." * 16
        if last: put_fill(D, b, "small")
    elif n == "雲が切れて":
        D.set(b, "." * 16, "." * 16, "." * 16)
    elif n == "落ちサビ":
        D.set(b, "." * 16, "." * 16, "x...x...x...x..." if i >= 4 else "." * 16)
        if last: put_fill(D, b, "build")
    elif n == "もう一度上へ":
        vgroove(D, b, "four", seed=b, s="............X..." if i < 4 else None)
        if i == 0: crash(D, b, "G2")
        if i == 6: put_fill(D, b, "build")
        if last: D.set(b, "X...X...X...X...", "XXXXXXXXXXXXXXXX", "." * 16)
    elif n == "風":
        if i == 0: D.set(b, "X" + "." * 15, "." * 16, "." * 16); crash(D, b, "C2", 8)

SIL.add(S.sc("ハーフのサビ")[-1], 3, 4)            # 雲が切れる直前の1拍は、完全な無音
SIL.add(S.sc("足元ふわふわ2")[-1], 3.5, 4)          # ハーフに入る前の短いブレイク（半拍）
SIL.apply()

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の06。ダンス（フューチャーベース）。B長調（サビ・ドロップは G#短調）・150。"
          "恋に落ちて、足もとがふわりと浮く気持ち。ドロップの先取りで始まり、歌とチョップが掛け合う Aメロ、フィルターが閉じていく Bメロ、「ふわり」の呼びかけのドロップ、"
          "ベルの間奏、ハーフのサビ、1拍の無音と足がすくむ静けさ、落ちサビ、フィルターが開いていく上り坂、最後のドロップ、風だけ残す。Surge の音。自作")
# 季節の音（2026-10-25 人間「季節を感じれる様な音も欲しい」）
season(S, S.sc("短いサビ")[0], "そよ風", S.beats * 8, vol=0.08)
season(S, S.nb - 6, "そよ風", S.beats * 6, vol=0.08)
S.flags += " --space sky --space-wet 0.18"
teto(S, LY, V, special={"最後のドロップ": 0.55, "雲が切れて": -0.6, "落ちサビ": -0.45, "短いサビ": 0.1}, vib={"build": 30})
