# vb25 24「星屑コンビニエンス」Stardust Convenience（仮）— テクノポップ（エレクトロスウィング）。E♭ 短調・152・4/4。転調なし
# 2026-10-25 作り直し: 物語を人の気持ちの話に（夢を追いながら、夜中のコンビニで働く）、歌を人が歌える旋律（8分と4分）に、テトの歌の版を足した。
#   テトの声に合うよう、曲全体を G短調から 4半音下げて E♭短調にした（書くのは G短調の度数のまま、書き出しの前に下げる）。
# 物語: 夜中の2時半、コンビニのレジ。眠い目をこすって棚をならべる。疲れた背広の人、ママの誕生日のろうそくを買う小さなきょうだい。
#   わたしの夢は音楽の仕事。レジの音はリズム、はなうたに乗せて。夜明けの静かな町で、星屑は夢のかけら。「ありがとうございました」。
# 場面と強さ: 自動ドア（チャイムとドアの音）→ 入店（ブラスのスウィング・中）→ 夜中の棚（Aメロ・シャッフル）→ 何を買う？（Bメロ・溜め・止め）
#   → レジが鳴る（サビ・強・シャッフル）→ 店内放送（ブラスの間奏）→ 星のダンス（2番。ここからストレートに切りかわる。BGM は前半ピアノが歌を受け取る）
#   → 何を買う？2（止め）→ レジが鳴る2（ストレートの4つ打ち）→ 1拍の完全な無音（自動ドアが閉まる）→ 閉まったドアの前（Half feel・弱）
#   → 星屑のソロ（ブラス）→ 最後のレジ（最大）→ ありがとうございました（シャッフルに戻って、和音で終わる）
# 旋律の性格: Aメロは句の頭を休んで8分で語る（シャッフルの所は跳ねる）。サビは4分と8分の「ほしくずコンビニ」。最高音 F#5。
# 定番以外の和音: E♭7→D7（属7の半音の連鎖）、サビの A♭7（♭II の属7＝D7 の裏）、F7→B♭maj7（副属和音）
from vb25_lib import *

S = Song("24", "hoshikuzu", "星屑コンビニエンス（仮）", "Stardust Convenience", 152, 4, "G", "minor", "テクノポップ（エレクトロスウィング）")
S.kit = "jazz"   # 2026-10-26 人間「24のドラムジャズっぽいのにしよう」（もとは electro）
S.flags = "--ref-tone glossy-jrock " + S.flags + " --piano salamander"
K = S.key   # G 短調（oct=4 で 1＝G4）


def chk(lines, beats=4):
    for l in lines: assert abs(total(K.mel(l, oct=4)) - beats) < 2e-3, ("拍の数", l, total(K.mel(l, oct=4)))


_DUR = re.compile(r"^([0-9.]+)(.*)$")


def warp(t):
    """シャッフルの時間の曲げ方: 拍の前半（0〜0.5）を 0〜2/3 に、後半（0.5〜1）を 2/3〜1 に"""
    b = math.floor(t + 1e-9); f = t - b
    return b + (f * 4 / 3 if f <= 0.5 + 1e-9 else 2 / 3 + (f - 0.5) * 2 / 3)


def swing(s):
    """ストレートで書いた並び（1小節）を、3連の跳ねる長さに直す（8分の裏を3連の3つ目へ）"""
    out, t = [], 0.0
    for x in s.split():
        n, v = x.split(":", 1)
        m = _DUR.match(v); L = float(m.group(1)); mk = m.group(2)
        a, z = warp(t), warp(t + L)
        out.append(f"{n}:{z - a:.4f}{mk}"); t += L
    return " ".join(out)


A_CH = ["Gm", "Gm/F", "Eb7", "D7", "Gm", "Cm7", "Am7b5", "D7"]
B_CH = ["Cm7", "F7", "Bbmaj7", "Ebmaj7", "Am7b5", "D7", "Gm", "D7"]
C_CH = ["Eb", "F", "Dm7", "Gm", "Cm7", "F7", "Bbmaj7", "D7", "Eb", "F", "Dm7", "Gm", "Cm7", "Ab7", "D7sus4", "D7"]
CM_CH = ["Cm7", "Cm7/Bb", "Am7b5", "D7", "Gm", "Gm/F", "Eb7", "D7"]
LAST_CH = C_CH + ["Eb", "F", "Dm7", "Gm", "Cm7", "Ab7", "D7", "Gm6"]

S.scene("自動ドア", 2, "intro", ["Gm", "Gm"])
S.scene("入店", 8, "intro", A_CH)
S.scene("夜中の棚", 16, "verse", A_CH)
S.scene("何を買う？", 8, "pre", B_CH)
S.scene("レジが鳴る", 16, "chorus", C_CH)
S.scene("店内放送", 8, "interlude", A_CH)
S.scene("星のダンス", 16, "verse", A_CH)
S.scene("何を買う？2", 8, "pre", B_CH)
S.scene("レジが鳴る2", 16, "chorus", C_CH)
S.scene("閉まったドアの前", 16, "bridge", CM_CH)
S.scene("星屑のソロ", 16, "solo", A_CH)
S.scene("最後のレジ", 24, "chorus", LAST_CH)
S.scene("ありがとうございました", 8, "outro", ["Cm7", "D7", "Gm", "Eb7", "Cm7", "D7", "Gm6", "Gm6"])
SHUF = set(S.sc("入店") + S.sc("夜中の棚") + S.sc("何を買う？") + S.sc("レジが鳴る") + S.sc("店内放送") + S.sc("閉まったドアの前") + S.sc("ありがとうございました"))

V = Voice(S, vol=0.22, delay=0.75, patch="mutedTrumpet", low=True)   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
BR = [S.track(f"ブラス{i + 1}", "brass", patch="brassSection", volume=0.13, pan=0.25, reverb=0.22, gainDb=3, phrase=4,
              fx=[{"type": "eq", "low": -3, "mid": 2, "midHz": 1800, "high": 0.5}]) for i in range(3)]
BRM = S.track("ブラス（リフ・ソロ）", "brass", patch="brassSection", volume=0.2, pan=0.25, reverb=0.22, gainDb=3, phrase=4,
              fx=[{"type": "eq", "low": -3, "mid": 2, "midHz": 1800, "high": 0.5}])
PIANO_FX = [{"type": "eq", "low": -3, "mid": -2, "midHz": 400, "high": 1}]
PN = [S.track(f"ピアノ（右手{i + 1}）", "piano", volume=0.1, pan=-0.25, reverb=0.22, fx=PIANO_FX) for i in range(3)]
PNL = S.track("ピアノ（左手）", "piano", volume=0.12, pan=-0.25, reverb=0.22, fx=PIANO_FX)
PNM = S.track("ピアノ（歌の受け渡し）", "piano", volume=0.18, pan=-0.25, reverb=0.22, fx=PIANO_FX)
BASS = S.track("ウッドベース風", "bass", patch="acousticBass", volume=0.24, pan=0, duck=0.15,
               fx=[{"type": "filter", "kind": "highpass", "freq": 40, "q": 0.7}, {"type": "eq", "low": -2, "mid": 3, "midHz": 900, "high": 0},
                   {"type": "eq", "low": 0, "mid": 2.5, "midHz": 2200, "high": 1}])
PAD = [S.track(f"パッド{i + 1}", "pad", **pad_spec("warmPad", vol=0.05, pan=0.0, duck=0.25)) for i in range(3)]
PLK = S.track("プラック（星屑）", "pad", **pluck_spec("pluckSynth", vol=0.075, pan=0.45, delay=0.75, sustain=0.5))
BELL = S.track("レジとチャイムの電子音", "fmBell", volume=0.1, pan=-0.3, reverb=0.3, sustain=0.9, gainDb=1)
FX = S.track("効果音（自動ドア・ライザー）", "pad", patch="fxRiser", volume=0.07, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
_dspec = lambda k: {kk: vv for kk, vv in NAKED[k].items() if kk != "human"}
HATS = S.track("ハイハット（シャッフル）", "hihat", **_dspec("hihat"))
SNG = S.track("スネア（シャッフルのゴースト）", "snare", **_dspec("snare"))
RIDE = S.track("ライド", "crash", **_dspec("crash"))
D = S.drumkit()
SIL = Silence(S)


def put(tr_, b, s):
    """シャッフルの小節なら跳ねる長さに直して置く"""
    tr_.bar(b, swing(s) if b in SHUF else s)


T3 = "0.3333"
# ================= 歌の旋律と歌詞（G短調の度数。oct=4 で 1 = G4。シャッフルの小節は跳ねる長さに直す。書き出しの前に全体を 4半音下げる） =================
VERSE = ["R:1 1:0.5 1:0.5 3:0.5 1:0.5 5:1", "4:1 3:1 1:1 R:1", "R:1 1:0.5 3:0.5 6:0.5 3:0.5 1:1", "#7,:1 2:1 R:2",
         "R:1 5:0.5 5:0.5 3:0.5 5:0.5 1':1", "6:1 4:1 R:2", "R:1 4:0.5 4:0.5 6:0.5 4:0.5 2:1", "#7,:2 R:2",
         "R:0.5 5:0.5 5:0.5 5:0.5 3:0.5 5:0.5 1':1", "7:1 5:1 R:2", "R:0.5 6:0.5 6:0.5 6:0.5 5:0.5 3:0.5 1:1", "#7,:1 2:1 4:1 R:1",
         "R:0.5 1':0.5 1':0.5 7:0.5 5:0.5 3:0.5 5:1", "6:1 4:1 1:1 R:1", "R:0.5 2:0.5 4:0.5 6:0.5 1':1 6:1", "#7:2 R:2"]
V1 = "よなかのにじはん/こんびにのれじ/ねむいめこすり/たなをならべ/つかれたせびろが/おにぎりふたつかう/おつかれさまですって/めだけでいう"
V2 = "ちいさなきょうだい/ろうそくをかう/たんじょうびだと/はにかむかお/わたしのゆめはね/ごせんふのむこうだ/れじのおとはりずむ/はなうたにね"
BM = ["4:1 6:1 1':1 R:1", "7:1 6:1 4:1 R:1", "3:1 5:1 7:1 R:1", "6:1 1':1 5:1 R:1",
      "R:0.5 1':0.5 1':0.5 1':0.5 2':1 1':1", "#7:1 2':1 #7:1 R:1", "R:0.5 3':0.5 2':0.5 1':0.5 5:1 3:1", "#7,:1 R:3"]
P1 = "まぶた/おもい/そらに/ほしが/ながれていくのが/まどにみえた"
P2 = "いつか/かなう/ほしを/かぞえ/りゅうせいにねがい/かけてみるの"
# サビ: 4分と8分の「ほしくずコンビニ」
HK = "1':1 1':0.5 6:0.5 1':0.5 3':1.5"
CH = [HK, "2':1.5 1':0.5 7:1 R:1", "R:0.5 5:0.5 7:0.5 2':0.5 2':1 7:1", "1':2 R:2",
      "1':1 1':0.5 6:0.5 1':0.5 3':1.5", "2':1.5 6:0.5 7:1 R:1", "R:0.5 3:0.5 5:0.5 7:0.5 2':1 7:1", "#7:2 R:2",
      HK, "2':1.5 1':0.5 7:1 R:1", "R:0.5 2':0.5 2':0.5 7:0.5 5:1 7:1", "1':2 R:2",
      "R:0.5 6:0.5 6:0.5 1':0.5 3':1 1':1", "b2':1.5 6:0.5 4:1 R:1", "R:0.5 5:0.5 1':0.5 2':0.5 2':1 1':1", "#7:2 R:2"]
C1 = "ほしくずこんびに/よなかのみせ/いらっしゃいませだよ/ちいさなこえ/ほしくずこんびに/よふかしびと/あたたかいものを/てわたしたよ"
C2 = "ほしくずこんびに/ゆめのとちゅう/ひかりのたなには/なにがあるの/ほしくずこんびに/あさまでには/すこしずつできる/はなうたから"
C3 = "ほしくずこんびに/あさのひかり/まどのむこうから/とりがなくよ/ほしくずこんびに/ゆめかけらを/かばんにしまったら/かえりみちへ"
LAST_X = [HK, "2':1.5 1':0.5 7:1 R:1", "R:0.5 7:0.5 2':0.5 2':0.5 2':1 7:1", "1':2 R:2",
          "R:0.5 6:0.5 1':0.5 3':0.5 3':1 1':1", "b2':2 6:1 R:1", "R:1 5:1 #7:1 2':1", "1':4"]
CM = ["R:1 5:1 3:1 1:1", "7,:2 R:2", "R:1 1:1 3:1 6:1", "#7,:2 R:2", "R:1 6:1 1':1 3':1", "2':2 R:2", "R:1 1':1 6:1 4:1", "#7:2 R:2",
      "R:0.5 1:0.5 3:0.5 5:0.5 1':1 5:1", "7:2 R:2", "R:0.5 1:0.5 3:0.5 6:0.5 1':1 6:1", "#7:2 R:2"]
THANKS = ["R:4", "R:1 2:0.5 2:0.5 2:0.5 2:0.5 #7,:0.5 #7,:0.5", "1:0.5 1:0.5 3:0.5 2:0.5 1:2"] + ["R:4"] * 5
chk(VERSE); chk(BM); chk(CH); chk(LAST_X); chk(CM); chk(THANKS)

LY = Lyrics(S)
def putv(name, lines, text, low=True, bars=None):
    bars = bars or S.sc(name)
    ob, om = [], []
    for i, (b, x) in enumerate(zip(bars, lines)):
        if x == "R:4": continue
        m = K.mel(x, oct=4); m = swing(m) if b in SHUF else m
        V.bar(b, m, low=low if not callable(low) else low(i)); ob.append(b); om.append(m)
    LY.flow(ob, om, text, name)
putv("夜中の棚", VERSE, V1)
if VOCAL: putv("星のダンス", VERSE, V2)
else:
    for i, b in enumerate(S.sc("星のダンス")):
        if i < 8: PNM.bar(b, K.mel(VERSE[i], oct=5))     # BGM: ピアノが歌を受け取る（1オクターブ上）
        else: V.bar(b, K.mel(VERSE[i], oct=4))
putv("何を買う？", BM, P1); putv("何を買う？2", BM, P2)
putv("レジが鳴る", CH, C1); putv("レジが鳴る2", CH, C2)
putv("閉まったドアの前", CM, "あけがた/しずかな/まちにね/ほしくず/きらめいてる/ゆめのかけら", bars=S.sc("閉まったドアの前")[4:], low=lambda i: i >= 4)
putv("最後のレジ", CH + LAST_X, C3 + "/ほしくずこんびに/よがあけるよ/またあしたもね/おやすみ")
putv("ありがとうございました", THANKS, "ありがとうございました", low=False)

# ================= ブラス（リフ・ソロ・合いの手） =================
RIFF = ["1:0.5 3:0.5 5:0.5 #4:0.25 5:0.25 1':1 R:1", "7,:0.5 2:0.5 4:0.5 7:0.5 6:1 R:1",
        "6,:0.5 1:0.5 3:0.5 b5:0.5 4:0.5 3:0.5 1:1", "#7,:0.5 2:0.5 4:0.5 2:0.5 #7,:2"]
SOLO = ["1':0.5 5:0.5 3:0.5 5:0.5 1':1 2':0.5 3':0.5", "2':1 7:0.5 4:0.5 2:1 4:1", "6:0.5 b5:0.5 3:0.5 1:0.5 3:0.5 6:0.5 1':1", "#7:1.5 6:0.25 5:0.25 4:1 R:1",
        "5:0.25 #4:0.25 5:0.25 6:0.25 5:0.5 3:0.5 1:1 3:1", "6:0.25 5:0.25 6:0.25 1':0.25 6:0.5 4:0.5 3:1 4:1",
        "1':0.5 6:0.5 4:0.5 2:0.5 4:0.5 6:0.5 1':0.5 2':0.5", "#7:2 R:2",
        "1':0.25 2':0.25 3':0.25 2':0.25 1':0.5 5:0.5 3:1 5:1", "7:0.25 1':0.25 2':0.25 1':0.25 7:0.5 4:0.5 2:1 4:1",
        "6:0.25 7:0.25 1':0.25 7:0.25 6:0.5 b5:0.5 3:1 1:1", "#7,:0.5 2:0.5 4:0.5 #7:0.5 2':1 R:1",
        "5:0.25 #4:0.25 5:0.25 6:0.25 5:0.5 3:0.5 1:1 3:1", "6:0.25 5:0.25 6:0.25 1':0.25 6:0.5 4:0.5 3:1 4:1",
        "4:0.5 6:0.5 1':0.5 2':0.5 3':1 2':1", "#7:3 R:1"]
chk(RIFF); chk(SOLO)
for name in ("入店", "店内放送"):
    for i, b in enumerate(S.sc(name)): put(BRM, b, K.mel(RIFF[i % 4], oct=4 if (name == "入店" or i < 4) else 3))
for i, b in enumerate(S.sc("星屑のソロ")): BRM.bar(b, K.mel(SOLO[i], oct=4))
for name in ("レジが鳴る", "レジが鳴る2", "最後のレジ"):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3:
            vv = voice(S.chords[b], 64, 3)
            for j in range(3): put(BR[j], b, f"R:2 {nm(vv[j])}:0.5' R:0.5 {nm(vv[j])}:1")

# ================= 伴奏 =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    if n == "自動ドア" or (n == "ありがとうございました" and i >= 6): continue
    r = low(ch, "E1")
    vv = voice(ch, 64, 3)
    # ピアノ: シャッフルは左手が1・3拍、右手が2・4拍（ブンチャッ）。ストレートは和音の刻みと16分の分散和音
    if b in SHUF and n not in ("閉まったドアの前",):
        PNL.bar(b, f"{nm(r + 12)}:1 R:1 {nm(r + 19)}:1 R:1")
        for j in range(3): PN[j].bar(b, f"R:1 {nm(vv[j])}:0.6667' R:0.3333 R:1 {nm(vv[j])}:0.6667' R:0.3333")
    elif n == "閉まったドアの前":
        PNL.bar(b, f"{nm(r + 12)}:4")
        for j in range(3): PN[j].bar(b, f"R:{0.6667 * j} {nm(vv[j])}:{4 - 0.6667 * j:.4f}")
    elif n in ("星のダンス", "星屑のソロ") or n.startswith("何を買う") or n.startswith("レジ") or n == "最後のレジ":
        PNL.bar(b, piano_left8(ch, "C2"))
        if n.startswith("レジ") or n == "最後のレジ":
            for j in range(3): PN[j].bar(b, f"{nm(vv[j])}:0.75 {nm(vv[j])}:0.75 {nm(vv[j])}:0.5 R:0.5 {nm(vv[j])}:0.5 {nm(vv[j])}:1")
        else:
            for j in range(3): PN[j].bar(b, f"R:0.5 {nm(vv[j])}:0.5 R:0.5 {nm(vv[j])}:0.5 R:0.5 {nm(vv[j])}:0.5 R:0.5 {nm(vv[j])}:0.5")
    # ウッドベース風（シャッフルは4分のウォーキング、ストレートは8分のオクターブ）
    # 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ 歌うベース（sing_bass。音域は元と同じ E1 から）を場面ごとに:
    #   シャッフルの所は、1小節おきに8分の跳ねるつなぎ（オクターブ上へ跳んで次の根音へ寄る walk。跳ねる長さに直す）を混ぜて、4分だけの歩きにしない
    #   ストレートの所: 2番の後半は上って下りる、サビ2と最後のサビは押す（drive）と、歌が伸ばす4小節目で駆ける（run）、ソロの後半は押す
    sw = lambda st: swing(sing_bass(S, b, st))
    if b in SHUF:
        if n == "入店" and i < 4: BASS.bar(b, f"{nm(r)}:1 R:3" if i == 0 else bass_line(S, b, "walk"))
        elif n == "閉まったドアの前": BASS.bar(b, bass_line(S, b, "half") if i >= 4 else f"{nm(r)}:4")
        elif n == "ありがとうございました": BASS.bar(b, bass_line(S, b, "walk") if i < 6 else (f"{nm(r)}:8" if i == 6 else ""))
        elif n.startswith("何を買う") and i == L - 1: BASS.bar(b, f"{nm(r)}:2 R:2")
        elif (n == "夜中の棚" and i >= 8) or n in ("店内放送", "レジが鳴る") or (n == "何を買う？" and i >= 4):
            BASS.bar(b, sw("walk") if i % 2 == 1 else bass_line(S, b, "walk"))
        else: BASS.bar(b, bass_line(S, b, "walk"))
    else:
        if n.startswith("何を買う") and i == L - 1: BASS.bar(b, f"{nm(r)}:2 R:2")
        elif n == "星のダンス" and i >= 8: BASS.bar(b, sing_bass(S, b, "climb" if i % 2 == 0 else "fall"))
        elif n in ("レジが鳴る2", "最後のレジ"): BASS.bar(b, sing_bass(S, b, "run" if i % 4 == 3 else "drive"))
        elif n == "星屑のソロ" and i >= 8: BASS.bar(b, sing_bass(S, b, "drive" if i % 2 == 0 else "run"))
        else: BASS.bar(b, bass_line(S, b, "oct8" if (n.startswith("レジ") or n == "最後のレジ" or n == "星屑のソロ") else "root8"))
    # パッド
    if n in ("閉まったドアの前",) or n.startswith("何を買う") or n.startswith("レジ") or n == "最後のレジ":
        pv = voice(ch, 58, 3)
        for j in range(3): PAD[j].bar(b, f"{nm(pv[j])}:4")
    # プラック（星屑。ストレートの所は16分、シャッフルは3連）
    t = tones(ch, "D4", "C6")
    if n in ("星のダンス",) and i >= 8 or n == "レジが鳴る2" or n == "最後のレジ":
        PLK.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" for q in (0, 2, 4, 2, 1, 3, 5, 3, 0, 2, 4, 2, 6, 4, 3, 1)))
    elif n == "夜中の棚" and i >= 8 or n == "レジが鳴る":
        PLK.bar(b, " ".join(f"{nm(t[q % len(t)])}:{T3}" for q in (0, 2, 4, 1, 3, 5, 2, 4, 6, 3, 1, 4)))

# 自動ドア（チャイムのピン・ポーン、ドアのシュッ）と、レジの電子音（ピッ）
BELL.bar(0, "B5:1 G5:3"); FX.bar(1, "A4:2 R:2")
for name in ("レジが鳴る", "レジが鳴る2", "最後のレジ"):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 1: put(BELL, b, "R:3 G6:0.25 R:0.25 G6:0.25 R:0.25")
FX.bar(S.sc("閉まったドアの前")[0], "A4:2 R:2")
BELL.bar(S.sc("閉まったドアの前")[0], "R:2 B5:0.5 G5:1.5")
riser(FX, S.sc("レジが鳴る")[0], 4, "C4"); riser(FX, S.sc("最後のレジ")[0], 8, "D4")
cym_swell(CYM, S.sc("星のダンス")[0], 2, "C4"); cym_swell(CYM, S.sc("最後のレジ")[0], 2, "C4")
# ありがとうございました: 最後はブラスと歌の役とピアノで Gm6 の和音をのばす
bx = S.sc("ありがとうございました")[6]
gv = voice("Gm6", 64, 3)
for j in range(3): BR[j].bar(bx, f"{nm(gv[j])}:8")
V.bar(bx, K.mel("5:8", oct=4))
for j in range(3): PN[j].bar(bx, f"R:{0.25 * j} {nm(voice('Gm6', 70, 3)[j])}:{8 - 0.25 * j}")
PNL.bar(bx, "G2:8"); BASS.bar(bx, "G1:8")
for i, b in enumerate(S.sc("ありがとうございました")):
    if i < 6: V.bar(b, swing(K.mel(["5:1 4:0.5 3:0.5 4:2", "#7,:1 2:1 4:2", "3:1 2:0.5 1:0.5 5,:2", "6,:1 1:1 b5:2", "6:1 5:0.5 4:0.5 6:2", "#7:2 2':2"][i], oct=4)), low=False)

# 2026-10-26 人間「後半の曲の作り込みが低く感じる」→ 足した工夫:
#   ・合いの手: Aメロで歌が2拍休む所に、ピアノ（歌の受け渡しのパート）の短い答え（和音の音で。弱く。シャッフルは跳ねる）
#   ・Bメロ（何を買う？）の前半: 歌が4拍目で休む所に、ブラスの「パッ」（溜め）
#   ・この曲の物語でしか出ない音: 店内放送の「ピンポンパンポーン」（はじめは上がり、終わりは下がる。作った和音の上下）
#   ・星屑: 閉まったドアの前（夜明け・ドラムなし）にグロッケンの流れ星。最後のサビは、歌が休む所にグロッケンの高い答え（新しい音）
def fill(tr_, b, k, lo="D5", hi="D6", swing_=False):
    tt = tones(S.chords[b], lo, hi)
    pats = [[(2, 0.5), (1, 0.5), (0, 1)], [(None, 0.5), (0, 0.5), (1, 0.5), (2, 0.5)], [(3, 0.5), (2, 0.5), (1, 0.5), (None, 0.5)], [(1, 0.5), (2, 0.5), (4, 1)]]
    sss = "R:2 " + " ".join(f"R:{L:g}" if q is None else f"{nm(tt[min(q, len(tt) - 1)])}:{L:g}," for q, L in pats[k % 4])
    tr_.bar(b, swing(sss) if swing_ else sss)
for i, b in enumerate(S.sc("夜中の棚")):
    if i in (5, 7, 9, 15): fill(PNM, b, i // 2, swing_=True)
for i, b in enumerate(S.sc("星のダンス")):
    if i in (9, 15): fill(PNM, b, i // 2 + 1)
for i, b in enumerate(S.sc("何を買う？")):
    if i < 4:
        vv = voice(S.chords[b], 61, 3)   # ブラスの自然な音域に収める
        for j in range(3): put(BR[j], b, f"R:3 {nm(vv[j])}:0.5' R:0.5")
for i, b in enumerate(S.sc("何を買う？2")):
    if i < 4 and i % 2 == 1:
        vv = voice(S.chords[b], 61, 3)   # ブラスの自然な音域に収める
        for j in range(3): put(BR[j], b, f"R:3 {nm(vv[j])}:0.5' R:0.5")
put(BELL, S.sc("店内放送")[0], "Bb5:0.5, D6:0.5, F6:0.5, Bb6:1.5, R:1")
put(BELL, S.sc("店内放送")[-1], "R:2 A5:0.5, F#5:0.5, D5:0.5, A4:0.5,")
GLK = S.track("グロッケン（星屑）", "glockenspiel", volume=0.06, pan=0.35, reverb=0.45)
for i, b in enumerate(S.sc("閉まったドアの前")):
    if i < 4: put(GLK, b, K.mel(["R:1 5:0.5 3:0.5 1:1 R:1", "R:2 1':0.5 6:0.5 4:1", "R:0.5 3':0.5 1':0.5 6:0.5 5:2", "R:4"][i], oct=6))
for i, b in enumerate(S.sc("最後のレジ")):
    if i % 4 == 3 and i < 20: GLK.bar(b, K.mel(["R:2 5:0.5 1':0.5 3':1", "R:2 2':0.5 1':0.5 6:1", "R:2 3':0.5 5':0.5 3':1", "R:2 6:0.5 5:0.5 3:1", "R:2 5:0.5 7:0.5 2':1"][i // 4], oct=6))
    if i == 23: GLK.bar(b, K.mel("R:1 5:0.5 1':0.5 3':1 5':1", oct=6))
# 2026-10-26 人間「ミックスのバランスをよくするのが大事」: サビでブラスの和音が鳴る2拍（4小節目の後半）は、同じ高さのピアノの右手を休ませて、
#   ブラスに場所をゆずる（同じ音域の重なりを時間で受け渡す）
for name in ("レジが鳴る", "レジが鳴る2", "最後のレジ"):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3:
            for t_ in PN: t_.ev = [e for e in t_.ev if not (b * 4 + 2 - 1e-6 <= e[0] < b * 4 + 4)]

# ================= ドラム =================
def hats_cut(b, a, z):
    """シャッフルのハイハットとゴーストを、クラッシュやフィルの所だけ抜く（両手がふさがるので）"""
    for t in (HATS, SNG):
        t.ev = [e for e in t.ev if not (b * 4 + a - 1e-6 <= e[0] < b * 4 + z - 1e-6)]


# 2026-10-26 人間（24）「24のドラムジャズっぽいのにしよう」→ ジャズのドラムに（キットは jazz）。
#   ライド: 2・4拍に重みを置く「チーン、チッキ、チーン、チッキ」（シャッフルの所は3連で跳ね、ストレートの所は8分）。鳴りは伸ばす
#   ハイハット: 足で 2・4拍を「チッ」。キック: 4分をごく弱く（フェザリング）、ときどき裏で「ドン」（ボム）。
#   スネア: 小節ごとに形を変える合いの手（コンピング）とゴースト。場面の強さで、ライドの強さと合いの手の数を変える
def rideb(b, strong=False, straight=False):
    a_ = "!" if strong else ""
    if straight: RIDE.bar(b, " ".join(f"D2:0.5{a_ if q in (2, 6) else ''}" for q in range(8)))
    else: RIDE.bar(b, f"D2:1 D2:0.6667{a_} D2:0.3333 D2:1 D2:0.6667{a_} D2:0.3333")
COMP = ["R:1.5 o:0.5 R:2", "R:2.5 x:0.5 R:1", "R:0.5 o:0.5 R:2 o:0.5 o:0.5", "R:3.5 x:0.5", "R:1 o:0.5 o:0.5 R:1.5 o:0.5",
        "R:1.5 x:0.5 R:1.5 o:0.5", "R:2 o:0.5 R:0.5 o:0.5 x:0.5", "R:0.5 x:0.5 R:3"]
COMP_SOFT = ["R:1.5 o:0.5 R:2", "R:3.5 o:0.5", "R:2.5 o:0.5 R:1", "R:4"]
def compb(b, i, busy, straight):
    pool = COMP if busy else COMP_SOFT
    c = pool[(i * 3 + b) % len(pool)]
    SNG.bar(b, c if straight else swing(c))
def kickb(b, i, busy):
    k = list("o...o...o...o...")
    if busy and i % 4 == 2: k[14] = "x"          # ボム（4拍目の裏）
    if busy and i % 8 == 5: k[6] = "x"           # ボム（2拍目の裏）
    return "".join(k)
HH24 = "....x.......x..."
S.no_spice = True   # 合いの手は小節ごとに変えているので、全曲共通の「遊び」は足さない（ロックの食いが入るため）
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "自動ドア": continue
    straight = b not in SHUF
    busy = n.startswith("レジ") or n == "最後のレジ" or n == "星屑のソロ" or n == "店内放送"
    if n == "入店" and i < 4:
        D.set(b, "o...o...o...o...", "." * 16, HH24 if i >= 2 else "." * 16)
        if i >= 2: rideb(b)
        continue
    if n == "閉まったドアの前":
        if i < 4: continue
        D.set(b, "o.......o.......", "." * 16, HH24)          # 静かな所: ライドは拍だけ、ゴーストを少し
        RIDE.bar(b, "D2:1 D2:1 D2:1 D2:1"); compb(b, i, False, straight)
        if i == 4: crash(D, b, "C2", 8); RIDE.ev = [e for e in RIDE.ev if not (abs(e[0] - b * 4) < 1e-6)]
        if last: put_fill(D, b, "tomtrip"); RIDE.ev = [e for e in RIDE.ev if not (b * 4 + 2 - 1e-6 <= e[0] < b * 4 + 4)]; SNG.ev = [e for e in SNG.ev if not (b * 4 <= e[0] < b * 4 + 4)]
        continue
    if n == "ありがとうございました" and i >= 6:
        if i == 6: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16); crash(D, b, "C2", 8)
        else: D.set(b, "." * 16, "." * 16, "." * 16)
        continue
    D.set(b, kickb(b, i, busy), "." * 16, HH24)
    rideb(b, strong=busy, straight=straight)
    compb(b, i, busy or n in ("夜中の棚", "星のダンス") and i >= 8, straight)
    if i == 0 or (busy and i % 8 == 0):
        crash(D, b, "C2" if i % 16 == 0 else "G2"); RIDE.ev = [e for e in RIDE.ev if not (abs(e[0] - b * 4) < 1e-6)]
    if i % 8 == 7 and not last:
        put_fill(D, b, "small"); SNG.ev = [e for e in SNG.ev if not (b * 4 + 3 - 1e-6 <= e[0] < b * 4 + 4)]
    if last and n != "ありがとうございました":
        if n.startswith("何を買う"): halt(D, b, 2); RIDE.ev = [e for e in RIDE.ev if not (b * 4 + 2 - 1e-6 <= e[0] < b * 4 + 4)]; SNG.ev = [e for e in SNG.ev if not (b * 4 + 2 - 1e-6 <= e[0] < b * 4 + 4)]
        else: put_fill(D, b, "tomtrip"); RIDE.ev = [e for e in RIDE.ev if not (b * 4 + 2 - 1e-6 <= e[0] < b * 4 + 4)]; SNG.ev = [e for e in SNG.ev if not (b * 4 + 2 - 1e-6 <= e[0] < b * 4 + 4)]

# 2026-10-26 人間「ドラム強弱、アクセント、余韻も上手く使ってね」: 24 はジャズにしたばかりなので形は変えず、余韻だけ:
#   クラッシュの一打を、次のシンバルまで最大 8拍のばす（すぐ止めない）
D.C.ev = [(st, max(L, 8.0), x) for st, L, x in D.C.ev]

# 止め（Bメロの最後 ×2）・1拍の完全な無音（自動ドアが閉まる直前）
for name in ("何を買う？", "何を買う？2"): SIL.add(S.sc(name)[-1], 2, 4)
SIL.add(S.sc("レジが鳴る2")[-1], 3, 4)
SIL.apply()

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の24。テクノポップ（エレクトロスウィング）。E♭ 短調・152・転調なし。夢を追いながら、夜中のコンビニで働く。"
          "自動ドアのチャイムから、ブラスのスウィング、8分で語る Aメロ（シャッフル）、「ほしくずコンビニ」のサビ。2番からストレートに切りかわり、"
          "1拍の無音で自動ドアが閉まって Half feel、ブラスのソロ、最後のサビ、シャッフルに戻って Gm6 の和音で終わる。自作")
S.no_depth = True
teto(S, LY, V, transpose=-4, special={"最後のレジ": 0.55, "閉まったドアの前": -0.5, "ありがとうございました": -0.3})
