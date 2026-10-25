# vb25 04「日曜日はハイパーモード」Sunday Is Hyper Mode（仮）— エレクトロニカ（ハイパーポップ）。C#短調（サビは平行調の E長調）・168・4/4。
#   大サビで +1（F長調）、最後の24小節でさらに +1（F#長調）＝半音ずつ2回の転調
# 2026-10-25 作り直し: 物語を人の気持ちの話に（前は迷子の犬との冒険）、歌を人が歌える旋律（8分と4分。テンポ 200→168）に、音を Surge の音に、テトの歌の版を足した。
# 物語: 「今日は何もしない」と決めた日曜日。スヌーズを3回押して、パジャマのまま昼すぎ。スマホの中のきらきらした誰かと比べて、
#   置いていかれる気がして焦る。でも、空っぽの冷蔵庫の前でばからしくなって、サンダルでコンビニへアイスを1つ買いに行く。
#   昼寝の夢で小さいころの自分に「休むのも大切」と言われ、夕焼けのベランダで、何もしない日を「最高の一日」と思えるようになる。
# 場面と強さ: スヌーズ（目覚ましの連打）→ 起き上がる（全員・フック）→ 何もしない朝（Aメロ）→ 冷蔵庫が空っぽ（Bメロ・溜め）
#   → ハイパーモード（サビ1）→ コンビニまで（間奏・歪んだシンセの主旋律とオーケストラヒット）→ 昼すぎのスマホ（2番。BGM はプラックが歌を受け取る）
#   → Bメロ2 → 夕方の散歩（サビ2・重いノリ）→ 昼寝（Half feel・逆再生）→ 寝ぼけたグリッチ（ソロ）→ 夕焼けの坂（だんだん高く）
#   → 1拍の完全な無音 → 夕方のベランダ（大サビ・+1）→ もう一段（+1）→ いきなり止めて目覚まし1音
# 旋律の性格: Aメロは跳ねるように上下する8分（C#4〜E5）。サビは同じ音を3つ置いてから下がる形、最高音は各調の主音（E5・F5・F#5）。
# ほかの曲とちがう所: 半音ずつ2回の転調、歪んだシンセとオーケストラヒット、逆再生、目覚まし1音でいきなり終わる。
from vb25_lib import *

S = Song("04", "hypersunday", "日曜日はハイパーモード（仮）", "Sunday Is Hyper Mode", 168, 4, "C#", "minor", "エレクトロニカ（ハイパーポップ・ボカロ）")
S.kit = "electro"
S.flags = "--ref-tone glossy-jrock " + S.flags
S.keep_old_synth = True
S.no_depth = True
K = S.key                    # C# 短調
KE = Key("E", "major")       # サビ（平行調）
KF = Key("F", "major")       # 大サビ（+1）
KG = Key("F#", "major")      # もう一段（+1）


def chk(*lists):
    """手で書いた行が、どれも1小節（4拍）ちょうどかを確かめる"""
    for L in lists:
        for x in L:
            t = sum(float(tok.split(":", 1)[1].rstrip("!,'_~^/\\")) for tok in x.split())
            assert abs(t - 4) < 1e-6, ("4拍ではない行", t, x)


A1_CH = ["C#m", "A", "B", "G#m", "C#m", "A", "B", "G#"]
A2_CH = ["C#m", "B", "A", "D", "C#m", "B", "A", "G#7"]              # D＝♭II（ナポリの和音）
B_CH = ["Amaj7", "B", "G#m7", "C#m7", "F#m7", "G#m7", "Asus2", "Baug"]   # Baug＝増三和音（サビの E へ）
C_CH = ["Amaj7", "G#7", "C#m7", "E7/B", "Amaj7", "G#7", "C#m7", "C#7",
        "F#m7", "B", "G#m7", "C#m7", "Amaj7", "B", "D", "E"]                 # IVM7–III7–vi の変形・E7/B（IV への副属和音）・♭VII の D
NAP = ["C#m9", "Amaj9", "E/G#", "F#m9"]
CM_CH = ["F#m7", "G#m7", "Amaj7", "B", "F#m7", "G#m7", "Amaj7", "B", "C#m7", "B", "Amaj7", "G#7", "F#m7", "G#m7", "A", "C7"]

S.scene("スヌーズ", 8, "intro", ["C#m"] * 4 + ["A", "B", "G#m", "G#"])
S.scene("起き上がる", 8, "intro", A1_CH)
S.scene("何もしない朝", 16, "verse", A1_CH)
S.scene("冷蔵庫が空っぽ", 8, "pre", B_CH)
S.scene("出かけるしかない", 16, "chorus", C_CH)
S.scene("コンビニまでの冒険", 16, "interlude", A2_CH)
S.scene("公園の迷子の犬", 16, "verse", A2_CH)
S.scene("冷蔵庫が空っぽ2", 8, "pre", B_CH)
S.scene("犬と走るサビ", 16, "chorus", C_CH)
S.scene("帰り道", 8, "interlude", A1_CH)
S.scene("昼寝", 16, "bridge", NAP)
S.scene("寝ぼけたグリッチ", 8, "solo", A1_CH)
S.scene("夕焼けの坂", 16, "build", CM_CH)
S.scene("夕方のベランダ", 24, "chorus", [tr_chord(c, 1) for c in C_CH + C_CH[:8]])
S.scene("もう一段", 24, "chorus", [tr_chord(c, 2) for c in C_CH + ["Amaj7", "B", "G#m7", "C#m7", "Amaj7", "B", "Asus2", "E"]])
S.scene("目覚まし", 2, "outro", ["F#", "F#"])

# ================= パート =================
V = Voice(S, vol=0.22, delay=0.75, bright=0.0, patch="surgeDnaSeq", low=True)
V.main.spec["fx"].insert(1, {"type": "filter", "kind": "lowpass", "freq": 6500, "q": 0.7})   # 2026-10-26 人間「４も３と同様にリードの歪をちょっと抑えよう」   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
DIST = S.track("のこぎり波のリード（主旋律の受け渡し・リフ）", "lead", patch="surgeHappySaws", volume=0.11, pan=0.0, reverb=0.12, mono=True, gainDb=1, breath=True,
               fx=[{"type": "filter", "kind": "highpass", "freq": 180, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 4300, "q": 0.7},
                   {"type": "eq", "low": 0, "mid": -4.5, "midHz": 2800, "high": -3}, {"type": "pingpong", "beats": 0.75, "mix": 0.1, "feedback": 0.2}])
ALARM = S.track("目覚まし（ベル）", "pad", patch="surgeBell1", volume=0.08, pan=0.2, reverb=0.15, mono=True,
                fx=[{"type": "filter", "kind": "highpass", "freq": 400, "q": 0.7}, {"type": "filter", "kind": "lowpass", "freq": 6000, "q": 0.7}])
# 2026-10-26 人間（04）「ほんのほんの少しだけベースの音大きく」→ 0.23→0.242（1.05倍）
BASS = S.track("太いシンセベース", "bass", **synth_bass_spec("surgeBassModernDirtyFat", vol=0.242, duck=0.3))
SAW = [S.track(f"厚い和音{i + 1}", "pad", **pad_spec("surgeChordUnisonMinority", vol=0.05, pan=0.0, duck=0.45, sustain=0.9)) for i in range(3)]
PLK = S.track("プラック（歌の受け渡し・アルペジオ）", "pad", **pluck_spec("surgeConvex", vol=0.09, pan=0.3, delay=0.75, sustain=0.5))
GLI = S.track("グリッチ（ビットクラッシャーのプラック）", "pad", patch="surgeRetroWave", volume=0.07, pan=-0.3, sustain=0.3, reverb=0.15,
              fx=[{"type": "bitcrusher", "bits": 6, "mix": 0.5}, {"type": "filter", "kind": "highpass", "freq": 300, "q": 0.7}])
BR = [S.track(f"オーケストラヒット（金管{i + 1}）", "brass", patch="brassSection", volume=0.13, pan=0.0, reverb=0.3, gainDb=2) for i in range(3)]
STR = [S.track(f"弦（ヒットと伸ばし{i + 1}）", "strings", patch="stringEnsemble", volume=0.09, pan=0.0, reverb=0.35, sustain=1.4) for i in range(3)]
HIT = S.track("ヒットの低音（インパクト）", "impactHit", volume=0.09, pan=0.0, reverb=0.35)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.075, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音（逆再生）", "guitar", patch="cymbalFx", volume=0.065, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の旋律と歌詞（Aメロ・Bメロ・昼寝・坂は C#短調で oct=4＝C#4。サビは E長調 oct=4＝E4） =================
VERSE = ["R:1 5:0.5 5:0.5 1':0.5 7:0.5 5:1", "3:2 R:2",
         "R:1 4:0.5 4:0.5 7:0.5 6:0.5 4:1", "5:1 7:1.5 R:1.5",
         "R:0.5 1:0.5 1:0.5 3:0.5 5:0.5 1':0.5 7:1", "6:1 3:1.5 R:1.5",
         "R:1 2:0.5 2:0.5 4:0.5 7:0.5 6:1", "5:2 R:2",
         "R:0.5 3:0.5 3:0.5 3:0.5 5:0.5 1':0.5 3':1", "1':1 6:1.5 R:1.5",
         "R:1 2':0.5 2':0.5 1':0.5 7:0.5 4:1", "5:1 7:1.5 R:1.5",
         "R:1 1':0.5 7:0.5 5:1 3:1", "6:2 R:2",
         "R:1 4:0.5 5:0.5 6:0.5 7:0.5 2':1", "#7:1 5:1.5 R:1.5"]
V1 = "きょうはなにも/しないときめた/すぬーずさんかい/まくらのなか/みんなはいまごろ/どこかへでかけ/わたしだけ/のりおくれてる"
V2 = "ひるすぎてね/ぱじゃまのままで/すまほのなかでは/きらきらして/くらべてしまうの/すっぴんのひびを/でもきいて/やすむひなんだ"
BM = ["R:0.5 3:0.5 3:0.5 3:0.5 4:0.5 5:0.5 6:1", "7:1 5:1.5 R:1.5", "R:1 5:0.5 5:0.5 5:0.5 6:0.5 7:1", "1':1 3:1.5 R:1.5",
      "R:1 6:0.5 6:0.5 6:0.5 7:0.5 1':1", "7:1 5:1.5 R:1.5", "R:0.5 6:0.5 6:0.5 7:0.5 1':0.5 2':0.5 3':1", "2':1 2':1.5 R:1.5"]
P1 = "このままでいいの/わからないけど/おなかはすいた/からのれいぞうこ"
P2 = "なにかしなくちゃと/じりじりむねが/ばからしくなる/ぜんぶわすれちゃえ"
CH = ["R:0.5 1':0.5 1':0.5 1':0.5 6:0.5 1':0.5 7:1", "#5:1 7:1.5 R:1.5",
      "R:1 6:0.5 6:0.5 5:0.5 3:0.5 5:1", "5:2 R:2",
      "R:1 4:0.5 4:0.5 6:0.5 1':0.5 7:1", "7:1 #5:1.5 R:1.5",
      "R:0.5 3:0.5 3:0.5 3:0.5 5:0.5 6:0.5 1':1", "5:1 6:1.5 R:1.5",
      "R:1 2:0.5 3:0.5 4:1 6:1", "5:2 R:2",
      "R:1 3:0.5 5:0.5 7:0.5 6:0.5 5:1", "6:2 R:2",
      "R:1 1':0.5 1':0.5 1':0.5 7:0.5 6:1", "7:1 5:1.5 R:1.5",
      "R:0.5 b7:0.5 b7:0.5 b7:0.5 1':0.5 b7:0.5 4:1", "5:0.5 3:0.5 1':2 R:1"]
C1 = "はいぱーもーどで/なにもしない/それでいいじゃん/にちようびだもん/ねころんで/そらをみてる/それだけでもう/さいこうのいちにち"
C2 = "はいぱーもーどで/ゆうやけまで/ぶらぶらあるく/さんだるのおとで/こんびにで/あいすひとつ/それだけでもう/さいこうのいちにち"
C3 = "はいぱーもーどで/ねじをゆるめ/そんなひもいい/はなまるあげよう/あしたには/またはしるよ/だからきょうはね/さいこうのいちにち"
BIGX = ["R:0.5 5:0.5 6:0.5 1':0.5 1':2", "7:1 6:1 3:2", "R:0.5 3:0.5 3:0.5 3:0.5 5:1 3:1", "2:1 3:1 5:2",
        "R:0.5 1:0.5 3:0.5 5:0.5 6:2", "3:1 7:1 6:1 3:1", "R:0.5 6:0.5 1':0.5 6:0.5 5:1 3:1", "5:3 R:1"]
BIGV = "ゆうやけそらが/いちごみるくだよ/なんにもしないひ/それがいいの"
ENDX = ["R:0.5 1':0.5 1':0.5 1':0.5 6:1 4:1", "5:1 2:1 5:2", "R:0.5 3:0.5 3:0.5 5:0.5 7:1 5:1", "6:2 R:2",
        "R:0.5 4:0.5 6:0.5 1':0.5 1':2", "7:1 1':1 7:1 5:1", "6:1 5:1 3:1 5:1", "1':4"]
ENDV = "げつようびくるよ/それまではね/はいぱーもーどのにちようび"
NP = ["R:1 3:1 5:1 2':1", "1':3 7:1", "7:2 5:1 3:1", "4:3 R:1", "R:1 5:1 7:1 4':1", "3':3 2':1", "2':2 7:1 5:1", "6:4",
      "R:4", "R:2 5:1 1':1", "3':2 2':1 1':1", "7:2 4:2", "R:1 3:1 6:1 1':1", "7:3 R:1", "R:1 4:1 6:1 2':1", "1':4"]
NPV = "ひるねしてゆめでね/ちいさなわたしがね/ねえいいんだよ/やすむの/たいせつ"
CM = ["R:1 4:0.5 6:0.5 1':1 6:1", "7:2 5:2", "R:1 5:0.5 7:0.5 2':1 7:1", "1':4",
      "R:1 6:0.5 1':0.5 3':1 1':1", "2':2 7:2", "R:1 7:0.5 2':0.5 4':1 2':1", "3':4",
      "R:0.5 3:0.5 3:0.5 3:0.5 5:1 5:1", "R:0.5 5:0.5 5:0.5 5:0.5 7:1 7:1", "R:0.5 6:0.5 6:0.5 6:0.5 1':1 1':1", "#7:2 2':2",
      "R:0.5 4:0.5 6:0.5 1':0.5 3':2", "R:0.5 5:0.5 7:0.5 2':0.5 4':2", "3':2 1':2"]
CMV = "ゆうやけいろ/べらんだで/ひとりきりで/わらえたよ/なにもない/ひだけれど/ゆうやけぶろで/ぽかぽか/ひだまりへいこうよ"
chk(VERSE, BM, CH, BIGX, ENDX, NP, CM)
LY = Lyrics(S)
def put(name, key, lines, text, low=True):
    bars = S.sc(name); mel = [key.mel(x, oct=4) for x in lines]
    for b, m in zip(bars, mel): V.bar(b, m, low=low)
    LY.flow(bars, mel, text, name)
for i, b in enumerate(S.sc("公園の迷子の犬")[:8]):
    if not VOCAL: PLK.bar(b, K.mel(VERSE[i], oct=4))           # BGM: 2番の前半は、プラックが歌を受け取る
put("何もしない朝", K, VERSE, V1)
if VOCAL: put("公園の迷子の犬", K, VERSE, V2)
else:
    for i, b in enumerate(S.sc("公園の迷子の犬")[8:]): V.bar(b, K.mel(VERSE[8 + i], oct=4))
put("冷蔵庫が空っぽ", K, BM, P1); put("冷蔵庫が空っぽ2", K, BM, P2)
put("出かけるしかない", KE, CH, C1); put("犬と走るサビ", KE, CH, C2)
put("昼寝", K, NP, NPV, low=False)
bars = S.sc("夕焼けの坂"); mel = [K.mel(x, oct=4) for x in CM] + [KF.mel("5:1 6:1 7:1 R:1", oct=4)]   # 最後の小節は C7（F長調の V）の上。最後の1拍は完全な無音
for b, m in zip(bars, mel): V.bar(b, m)
LY.flow(bars, mel, CMV, "夕焼けの坂")
put("夕方のベランダ", KF, CH + BIGX, C3 + "/" + BIGV)
put("もう一段", KG, CH + ENDX, C1 + "/" + ENDV)

# ================= 目覚まし =================
def snooze(b, n=4, p="A5"):
    """ピピピピ（16分の2つ組を n 回）"""
    ALARM.bar(b, " ".join([f"{p}:0.125 R:0.125 {p}:0.125 R:0.375"] * n) + (f" R:{4 - n * 0.75:g}" if n * 0.75 < 4 else ""))
for i, b in enumerate(S.sc("スヌーズ")):
    if i in (0, 1): snooze(b, 4)
    elif i == 2: ALARM.bar(b, "R:4")                                  # スヌーズを押した（1回目）
    elif i == 3: snooze(b, 5, "A5")
    elif i >= 4: snooze(b, 2, "C#6")

# ================= 歪みシンセ（起き上がるのフック・冒険の主旋律・グリッチのソロ） =================
HOOK = ["1':0.25 1':0.25 R:0.25 1':0.25 7:0.25 5:0.25 R:0.25 3:0.25 5:0.5 7:0.25 1':0.25 R:0.5 3':0.5",
        "1':0.25 1':0.25 R:0.25 6:0.25 5:0.25 3:0.25 R:0.25 1:0.25 3:0.5 5:0.25 6:0.25 R:0.5 1':0.5",
        "2':0.25 2':0.25 R:0.25 7:0.25 6:0.25 4:0.25 R:0.25 2:0.25 4:0.5 6:0.25 7:0.25 R:0.5 2':0.5",
        "#7:0.5 2':0.5 5':0.5 2':0.5 #7:1 R:1"]
ADV = ["5':0.5 3':0.5 1':0.5 3':0.5 5':1 7':1", "6':0.5 5':0.5 3':0.5 1':0.5 7:1 2':1", "1':0.5 3':0.5 6':0.5 5':0.5 3':1 1':1", "b2':2 1':1 7:1",
       "5':0.25 5':0.25 3':0.5 1':0.5 3':0.5 5':0.5 1'':0.5 7':1", "6':0.5 7':0.5 1'':0.5 7':0.5 6':1 5':1",
       "1':0.5 2':0.5 3':0.5 6':0.5 5':0.5 3':0.5 1':1", "b2':1.5 1':0.5 7:1 #7:1"]
GSOLO = ["1':0.25 3':0.25 5':0.25 3':0.25 1':0.25 3':0.25 5':0.25 1'':0.25 7':0.5 5':0.5 3':1",
         "6:0.25 1':0.25 3':0.25 6':0.25 5':0.25 3':0.25 1':0.25 6:0.25 1':1 R:1",
         "4':0.125 " * 8 + "2':0.125 " * 8 + "7:0.5 2':0.5 4':1",                           # スタッター
         "5':1.5 4':0.5 2':1 #7:1",
         "3':0.25 3':0.25 5':0.25 5':0.25 1'':0.25 1'':0.25 5':0.25 5':0.25 3':0.5 1':0.5 5:1",
         "1':0.25 1':0.25 3':0.25 3':0.25 6':0.25 6':0.25 3':0.25 3':0.25 1':0.5 6:0.5 3:1",
         "7:0.125 " * 8 + "2':0.125 " * 8 + "4':0.125 " * 8 + "7':0.125 " * 8,          # スタッター
         "#7':2 R:2"]
chk(HOOK, ADV, [x.strip() for x in GSOLO])
for i, b in enumerate(S.sc("起き上がる")): DIST.bar(b, K.mel(HOOK[i % 4], oct=4))
for i, b in enumerate(S.sc("帰り道")): DIST.bar(b, K.mel(HOOK[i % 4], oct=4) if i < 7 else K.mel("#7:2 R:2", oct=4))   # 帰り道は歪みシンセがフックを歌う
for i, b in enumerate(S.sc("コンビニまでの冒険")): DIST.bar(b, K.mel(ADV[i % 8], oct=4) if i < 15 else K.mel("1':2 R:2", oct=4))
for i, b in enumerate(S.sc("寝ぼけたグリッチ")): DIST.bar(b, K.mel(GSOLO[i].strip(), oct=4))
# サビの後ろで、歪みシンセが低い所でフックを支える（歌の役とぶつからない C#4〜C#5）
for name, kk in (("出かけるしかない", KE), ("犬と走るサビ", KE), ("夕方のベランダ", KF), ("もう一段", KG)):
    for i, b in enumerate(S.sc(name)):
        if i % 4 == 3: DIST.bar(b, kk.mel("R:2 1:0.25 3:0.25 5:0.25 1':0.25 7:0.5 5:0.5", oct=4))
# 昼寝: フックを逆から（逆行）、グリッチのプラックでぼんやり
RETRO = [retro(HOOK[0]), retro(HOOK[1]), retro(HOOK[2]), retro(HOOK[3])]
for i, b in enumerate(S.sc("昼寝")):
    if 8 <= i < 12: GLI.bar(b, K.mel(RETRO[i - 8], oct=4))
for i, b in enumerate(S.sc("スヌーズ")):
    if i >= 4: GLI.bar(b, K.mel(HOOK[i - 4], oct=4))                   # 起きる前の、寝ぼけたフック

# ================= 伴奏 =================
def orch_hit(b, off=0.0, ch=None, L=0.5):
    """オーケストラヒット: 金管と弦の和音を短く、インパクトの低音を重ねる"""
    ch = ch or S.chords[b]
    v = voice(ch, 66, 3)
    for j in range(3):
        BR[j].bar(b, f"{nm(v[j])}:{L:g}!", off); STR[j].bar(b, f"{nm(v[j] + 12)}:{L:g}!", off)
    HIT.bar(b, f"{nm(low(ch, 'C2'))}:2", off)

for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    v = voice(ch, 64, 3)
    chorus = n in ("出かけるしかない", "犬と走るサビ", "夕方のベランダ", "もう一段")
    if chorus:
        for j in range(3): SAW[j].bar(b, f"{nm(v[j])}:1.5 {nm(v[j])}:1 {nm(v[j])}:1.5")
        t = tones(ch, "C4", "C6"); PLK.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.5" for q in (0, 2, 1, 3, 2, 4, 3, 1)))
    if n in ("何もしない朝",) and i >= 8 or n == "公園の迷子の犬" and i >= 8:
        t = tones(ch, "C4", "C6"); PLK.bar(b, " ".join(f"{nm(t[q % len(t)])}:0.25" + ("," if q % 2 else "") for q in (0, 1, 2, 3, 2, 1, 2, 3, 0, 1, 2, 3, 4, 3, 2, 1)))
    if n.startswith("冷蔵庫") and i < 7:
        for j in range(3): STR[j].bar(b, f"{nm(v[j])}:4")
    if n == "昼寝":
        vv = voice(ch, 60, 3)
        for j in range(3): STR[j].bar(b, f"{nm(vv[j])}:4")
    if n == "夕焼けの坂":
        for j in range(3): STR[j].bar(b, f"{nm(v[j])}:2 {nm(v[j])}:2" if i < 8 else " ".join(f"{nm(v[j])}:0.5" for _ in range(8)))
    # オーケストラヒット: 冒険の間奏の4小節ごと、サビの頭、起き上がるの頭
    if (n == "コンビニまでの冒険" and i % 4 == 0) or (chorus and i % 8 == 0) or (n == "起き上がる" and i in (0, 4)):
        orch_hit(b)
    if n == "コンビニまでの冒険" and i % 4 == 2: orch_hit(b, 1.5, L=0.5)
    # ベース
    if n == "スヌーズ": BASS.bar(b, f"{nm(low(ch, 'E1'))}:4") if i >= 6 else None
    elif n == "起き上がる": BASS.bar(b, bass_line(S, b, "oct8"))
    elif n in ("何もしない朝", "公園の迷子の犬"): BASS.bar(b, bass_line(S, b, "push" if i < 8 else "oct8"))
    elif n.startswith("冷蔵庫"): BASS.bar(b, bass_line(S, b, "root8") if i < 7 else f"{nm(low(ch, 'E1'))}:4")
    elif chorus: BASS.bar(b, bass_line(S, b, "oct8") if n != "犬と走るサビ" else bass_line(S, b, "half" if i % 2 else "push"))
    elif n == "コンビニまでの冒険": BASS.bar(b, bass_line(S, b, "disco"))
    elif n == "帰り道": BASS.bar(b, bass_line(S, b, "house") if i < 7 else f"{nm(low(ch, 'E1'))}:2")
    elif n == "昼寝": BASS.bar(b, f"{nm(low(ch, 'E1'))}:4" if i >= 4 else "R:4")
    elif n == "寝ぼけたグリッチ": BASS.bar(b, bass_line(S, b, "pulse"))
    elif n == "夕焼けの坂": BASS.bar(b, bass_line(S, b, "root8" if i < 8 else "oct8"))

FX.bar(S.sc("スヌーズ")[2], "A4:2 R:2")                                # スヌーズを押す「シュッ」
riser(FX, S.sc("出かけるしかない")[0], 4, "C4"); riser(FX, S.sc("犬と走るサビ")[0], 4, "C4")
FX.bar(S.sc("昼寝")[0], "G4:4")                                        # サブドロップ（ベッドに倒れこむ）
riser(FX, S.sc("夕方のベランダ")[0] - 0.25, 8, "D4")
# 逆再生のシンバル（C＝逆再生クラッシュ・D＝逆再生チャイナ）
cym_swell(CYM, S.sc("起き上がる")[0], 2, "C4"); cym_swell(CYM, S.sc("コンビニまでの冒険")[0], 2, "D4")
cym_swell(CYM, S.sc("昼寝")[8], 4, "C4"); cym_swell(CYM, S.sc("寝ぼけたグリッチ")[0], 2, "D4")
cym_swell(CYM, S.sc("もう一段")[0] - 0.25, 1, "C4")

# ================= ドラム（電子のドラム） =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    chorus = n in ("出かけるしかない", "犬と走るサビ", "夕方のベランダ", "もう一段")
    if n == "スヌーズ":
        if i >= 4: D.set(b, "X.......X.......", "....x.......x..." if i < 7 else "....x...x.x.XXXX", "x.x.x.x.x.x.x.x.")
    elif n == "起き上がる":
        vgroove(D, b, "four16", seed=b)
        if i == 0: crash(D, b)
        if last: put_fill(D, b, "snare16")
    elif n in ("何もしない朝", "公園の迷子の犬"):
        if n == "公園の迷子の犬" and i < 8: vgroove(D, b, "trap", seed=b)
        else: vgroove(D, b, "dnb" if i < 8 else "vrock", ghosts=0.3, seed=b)
        if i == 0: crash(D, b)
        if i == 7: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
    elif n.startswith("冷蔵庫"):
        vgroove(D, b, "half" if i < 4 else "vrock2", ghosts=0.3, seed=b)
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 1)                                              # 全員の止め（Baug の伸ばしだけ残る）
    elif chorus:
        name = "vrock"
        if n == "犬と走るサビ": name = "halfdrive" if i < 8 else "vrock"   # 2回目は重いノリに入れかえる
        if n == "もう一段" and i >= 8: name = "punk"
        vgroove(D, b, name, ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16" if i % 16 == 7 else "tomtrip")
        if last and n != "夕方のベランダ" and n != "もう一段": put_fill(D, b, "tomdown")
    elif n == "コンビニまでの冒険":
        vgroove(D, b, "four16", seed=b)
        if i % 8 == 0: crash(D, b, "B2")
        if i % 4 == 3: put_fill(D, b, "small" if i % 8 == 3 else "snare16")
    elif n == "帰り道":
        vgroove(D, b, "trap", seed=b)
        if i == 0: crash(D, b, "G2")
        if last: halt(D, b, 2)
    elif n == "昼寝":
        if i < 4: D.set(b, "." * 16, "." * 16, "." * 16)
        else: vgroove(D, b, "half", ghosts=0.15, seed=b, h="x...x...x...x...")
        if i == 12: crash(D, b, "C2", 8)
        if last: put_fill(D, b, "build")
    elif n == "寝ぼけたグリッチ":
        vgroove(D, b, "four16", seed=b)
        if i == 0: crash(D, b)
        if i in (2, 6): D.set(b, "X.X.X.X.XXXXXXXX", "....X.......XXXX", "xxxxxxxxxxxxxxxx")
    elif n == "夕焼けの坂":
        vgroove(D, b, "half" if i < 4 else ("vrock2" if i < 12 else "vrock"), ghosts=0.3, seed=b)
        if i in (0, 8): crash(D, b, "G2")
        if i == 7: put_fill(D, b, "tomtrip")
        if i == 14: put_fill(D, b, "build")
        if last: D.set(b, "X...X...X.X.X...", "....X...X.XXX...", "." * 16)
    elif n == "目覚まし":
        D.set(b, "." * 16, "." * 16, "." * 16)

SIL.add(S.sc("夕焼けの坂")[-1], 3, 4)                    # 大サビの直前の1拍は、完全な無音
SIL.add(S.sc("夕方のベランダ")[-1], 3.75, 4)               # 2回目の転調の前のごく短いブレイク（16分）
SIL.add(S.sc("目覚まし")[0], 0, 2)                         # いきなり止める
SIL.apply()
ALARM.bar(S.sc("目覚まし")[0], "R:2 C#6:1.5 R:0.5")                   # 最後: いきなり止めて、目覚まし1音

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の04。エレクトロニカ（ハイパーポップ）。C#短調（サビは E）・168。大サビで +1（F）、最後の24小節でさらに +1（F#）。"
          "何もしないと決めた日曜日の、焦りと開き直り。目覚ましのスヌーズで始まり、跳ねる8分の Aメロ、同じ音を3つ置いてから下がるサビ、のこぎり波のリードとオーケストラヒットの間奏、"
          "重いノリの2サビ、Half feel の昼寝（フックの逆行と逆再生のシンバル）、グリッチのソロ、だんだん高くなる夕焼けの坂と1拍の無音、大サビ、もう一段の転調、目覚まし1音で終わる。Surge の音。自作")
S.flags += " --space sky --space-wet 0.15"
teto(S, LY, V, special={"夕方のベランダ": 0.5, "もう一段": 0.6, "夕焼けの坂": 0.1}, vib={"build": 30})
