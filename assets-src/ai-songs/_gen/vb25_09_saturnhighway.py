# vb25 09「ゴーゴー土星ハイウェイ」Go-Go Saturn Highway（仮）— ロック（ポップパンク）。D長調・208・4/4。最後のサビは +2（E長調）
# 2026-10-25 作り直し: 物語を人の気持ちの話に（前は自転車にロケット）、歌を人が歌える旋律（8分と4分）に、テトの歌の版を足した。
#   テトの声に合うよう、曲全体を A長調から 7半音下げて D長調にした（書くのは A長調の度数のまま、書き出しの前に下げる）。
# 物語: 免許を取りたての友だちと、父の車で夜中のハイウェイを走る。卒業したらばらばらになる。将来のことは何もわからない。
#   それでもラジオを大きくして、窓から夜風を入れて、土星が見える夜空の下で「どこまでも行ける」と笑い飛ばす。夜明けに戻ってくる。
# 場面と強さ: 秒読み（歌の役が数える）→ 発進（全員）→ 夜中のハイウェイ（Aメロ）→ アクセル（Bメロ・溜め・止め）→ どこまでも（サビ1・8ビート）
#   → 掛け声（歌とオルガンの言い合い）→ 窓をあける（間奏・オルガン）→ 2番（BGM はオルガンが歌を受け取る）→ アクセル2 → サビ2（Half feel）
#   → 掛け声2 → 無音2拍 → 星が近い（Cメロ）→ ギターソロ → もう一度（Bメロの形）→ 1拍の無音 → 最後のサビ（+2・2ビート）→ 掛け声3 → 夜明け（急に止める）
# 旋律の性格: Aメロは句の頭を休んで入る8分。サビは同じ音を3つ置いて休む「呼びかけ」。掛け声は「ごごいこう」「おおいえい」。最高音 F#5。
# ほかの曲とちがう所: いちばん勢いのあるポップパンク。2ビート、オルガン、手拍子、歌とオルガンの言い合い。
from vb25_lib import *

S = Song("09", "saturnhighway", "ゴーゴー土星ハイウェイ（仮）", "Go-Go Saturn Highway", 208, 4, "A", "major", "ラップロック／ニューメタル（ボカロ）")
S.kit = "crocell-punch"
# 2026-10-26 人間「09の音リンキン・パークに変えようか」: ニューメタル／ラップロックの音（参考の音 bright-nu-wall・ギター nu-metal-wall）。
#   曲そのもの（旋律・コード・フレーズ）はまねず、音の作り方と編成だけ（重い歪みの壁＋暗いシンセ＋ピアノのフック＋ヒップホップ寄りのドラム＋スクラッチ風の飾り）
S.flags = "--bass bnb-loud --ref-tone bright-nu-wall " + S.flags
S.extra.update({"tone": "rock"})
K = S.key
K2 = K.up(2)           # 最後のサビ（B長調）

RIFF_CH = ["A", "C#m", "D", "Dm"]                                       # Dm＝同主調から借りた iv
V_CH = ["A", "C#m", "D", "E", "A", "C#m", "Bm7", "E7"]
B_CH = ["D", "E", "F#m", "C#m", "D", "E", "Bm7", "Eaug"]                 # Eaug＝増三和音（定番以外）
C_CH = ["D", "E", "C#m7", "F#m", "D", "E", "A", "A"]
C_CH2 = ["D", "E", "C#7", "F#m", "Bm7", "D/E", "A", "E/G#"]              # C#7＝vi への副属和音
SHOUT = ["A", "G", "D", "A", "A", "G", "D", "E"]                          # G＝♭VII
FLOAT = ["F#m", "D", "A/C#", "Dmaj7", "Bm7", "C#m7", "Dmaj7", "E7sus4",
         "F#m", "F#m/E", "Dmaj7", "C#7", "Bm7", "E/G#", "Dmaj7", "E"]
LAST3 = ["D", "E", "F#m", "G", "D", "E", "A", "A"]
up2 = lambda cs: [tr_chord(c, 2) for c in cs]

S.scene("秒読み", 4, "intro", ["A", "A", "E", "E"])
S.scene("発射", 12, "intro", RIFF_CH)
S.scene("大気圏", 16, "verse", V_CH)
S.scene("加速", 8, "pre", B_CH)
S.scene("輪っか", 16, "chorus", C_CH + C_CH2)
S.scene("掛け声", 8, "interlude", SHOUT)
S.scene("無重力", 16, "interlude", RIFF_CH)
S.scene("大気圏2", 16, "verse", V_CH)
S.scene("加速2", 8, "pre", B_CH)
S.scene("輪っか2", 16, "chorus", C_CH + C_CH2)
S.scene("掛け声2", 8, "interlude", SHOUT)
S.scene("ただよう", 16, "bridge", FLOAT)
S.scene("ギターソロ", 16, "solo", RIFF_CH)
S.scene("再突入", 8, "build", ["D", "E", "F#m", "D", "Bm7", "C#m7", "D", "E"])
S.scene("輪っかを抜ける", 24, "chorus", up2(C_CH + C_CH2 + LAST3))
S.scene("掛け声3", 8, "interlude", up2(SHOUT))
S.scene("着陸", 12, "outro", up2(SHOUT + SHOUT[:4]))
# 2026-10-26 人間「エイトビートもライドで刻むとか、ハイハット以外もつかって曲に合うように変えてほしい。これ重要」:
#   加速（Bメロ）は裏の開いたハイハット、最初のサビ（輪っか）はライドのカップ、ギターのソロはライド、再突入はフロアタムの8分で低くためる
S.keepers = {'加速': 'open', '加速2': 'open', '輪っか': 'bell', 'ギターソロ': 'ride', '再突入': 'floor'}

V = Voice(S, vol=0.22, delay=0.5, patch="voiceLeadModern", low=True)   # 2026-10-25 人間「全部にこのリードを入れるわけじゃないよね」→ 曲に合わせて選ぶ
GL = [S.track(f"ギター左（{['根音', '5度'][i]}・ニューメタルの壁）", "distGuitar", **rock_gtr_spec(0.08, -0.6, tone="nu-metal-wall")) for i in range(2)]
GR = [S.track(f"ギター右（{['根音', 'オクターブ'][i]}・ニューメタルの壁）", "distGuitar", **rock_gtr_spec(0.08, 0.6, tone="nu-metal-wall")) for i in range(2)]
# 2026-10-26 人間「リフは少し音を小さくしよう」: リフ 0.14→0.10。ソロは別のパート
LG = S.track("リードギター（リフ）", "distGuitar", **lead_gtr_spec(0.10, -0.08))
LGS = S.track("リードギター（ソロ）", "distGuitar", **lead_gtr_spec(0.15, 0.0))
# 2026-10-26 人間「09はベース表に出すようなメロディ入れようか」: ベースを大きく（0.21→0.26）、旋律を弾く
BASS = S.track("ベース（指弾き・旋律）", "bass", **rock_bass_spec(0.26))
# オルガンのかわりに、暗いシンセのパッド（和音）とピアノ（フック・歌の受け渡し）
ORG = [S.track(f"暗いシンセのパッド{i + 1}", "pad", patch="surgePadNewtonWasEvil", volume=0.07, pan=0.0, reverb=0.3, sustain=2.0, duck=0.3,
               fx=[{"type": "filter", "kind": "highpass", "freq": 200, "q": 0.7}]) for i in range(3)]
ORGM = S.track("ピアノ（フック・歌の受け渡し）", "piano", volume=0.15, pan=-0.1, reverb=0.3, fx=[{"type": "eq", "low": -3, "mid": -1.5, "midHz": 400, "high": 1}])
# 手拍子のかわりに、スクラッチ風の飾り（ギターのピックで弦をこする音を短く）
CLAP = S.track("スクラッチ風の飾り（ピックスクレイプ）", "guitar", patch="guitarFx", volume=0.07, pan=0.25, amp="clean", chorus=0, reverb=0.15)
FX = S.track("効果音", "pad", patch="fxRiser", volume=0.075, pan=0, reverb=0.3)
CYM = S.track("シンバルの効果音", "guitar", patch="cymbalFx", volume=0.06, pan=0, modulate=False)
D = S.drumkit()
SIL = Silence(S)

# ================= 歌の旋律と歌詞（A長調の度数。oct=4 で 1 = A4。書き出しの前に全体を 7半音下げる。使う音は 5,〜3'） =================
CD = ["5:0.5' R:1.5 4:0.5' R:1.5", "3:0.5' R:1.5 2:0.5' R:1.5", "1:0.5' R:1.5 5,:0.5' R:1.5", "R:1 1:0.5 3:0.5 5:0.5 1':1.5"]
for i, b in enumerate(S.sc("秒読み")): V.bar(b, K.mel(CD[i], oct=4), low=(i == 3))
VERSE = ["R:1 1:0.5 1:0.5 3:0.5 1:0.5 5,:1", "7,:1 3:1.5 R:1.5",
         "R:1 4:0.5 4:0.5 6:0.5 4:0.5 2:1", "5,:1 7,:1.5 R:1.5",
         "R:0.5 3:0.5 3:0.5 3:0.5 5:0.5 3:0.5 1:1", "7,:1 5,:1.5 R:1.5",
         "R:1 4:0.5 4:0.5 4:0.5 3:0.5 2:1", "2:1 7,:1.5 R:1.5",
         "R:1 5:0.5 5:0.5 6:0.5 5:0.5 3:1", "5:1 3:1.5 R:1.5",
         "R:1 6:0.5 6:0.5 5:0.5 4:0.5 6:1", "5:1 2:1.5 R:1.5",
         "R:1 3:0.5 4:0.5 5:0.5 6:0.5 5:1", "3:2 R:2",
         "R:1 4:0.5 3:0.5 2:0.5 1:0.5 2:1", "5,:1 7,:1.5 R:1.5"]
V1 = "めんきょとりたて/ちちのくるまで/よなかのはいうぇい/ふたりではしる/さくらがさけば/ちがうほしだと/わらうきみの/よこがおみてた"
V2 = "らじおのおとを/おおきくしたら/まどからよかぜが/ふきこんでくる/みらいのちずは/まだしろいまま/いまはただね/このみちをいく"
BM = ["R:0.5 4:0.5 4:0.5 6:0.5 1':1 6:1", "5:2 R:2", "R:0.5 6:0.5 6:0.5 7:0.5 1':1 7:1", "5:2 R:2",
      "R:0.5 6:0.5 6:0.5 6:0.5 1':1 2':1", "1':1 7:1.5 R:1.5", "R:0.5 6:0.5 1':0.5 2':0.5 3':1 2':1", "7:2 R:2"]
P1 = "あしたのこと/いまはいいよ/あくせるふんで/はしりだそう"
P2 = "くもりぼしも/わらいとばせ/こえをあわせて/うたおうよね"
CH1 = ["R:0.5 1':0.5 1':0.5 1':0.5 R:0.5 6:0.5 1':1", "R:0.5 2':0.5 2':0.5 2':0.5 R:0.5 7:0.5 5:1",
       "R:0.5 3:0.5 5:0.5 1':0.5 7:1 5:1", "6:1.5 5:0.5 6:2",
       "R:0.5 1':0.5 1':0.5 1':0.5 R:0.5 6:0.5 1':1", "R:0.5 2':0.5 2':0.5 2':0.5 3':1 2':1",
       "1':1 7:0.5 6:0.5 5:1 3:1", "5:3 R:1"]
CH1b = ["R:0.5 1':0.5 1':0.5 1':0.5 R:0.5 6:0.5 1':1", "R:0.5 2':0.5 2':0.5 2':0.5 R:0.5 7:0.5 5:1",
        "R:0.5 #5:0.5 #5:0.5 #5:0.5 3':1 #5:1", "6:1 1':1 3':1.5 R:0.5",
        "2':1 1':0.5 6:0.5 4:1 6:1", "5:1 7:1 2':1.5 R:0.5", "1':2 3':1 2':1", "1':2 R:2"]
CH2 = CH1[:6] + ["1':0.5 2':0.5 1':0.5 6:0.5 5:1.5 R:0.5", "5:2 3:1 5:1"]
CH2b = CH1b[:4] + ["2':1 1':0.5 6:0.5 2':1 3':1", "3':1 2':1 7:1.5 R:0.5", "6:1 1':1 2':1 3':1", "1':2 R:2"]
LASTX = ["R:0.5 1':0.5 1':0.5 1':0.5 2':1 1':1", "R:0.5 2':0.5 2':0.5 2':0.5 1':1 7:1", "6:1 1':1 2':2", "b7:1 1':1 2':2",
         "R:0.5 1':0.5 1':0.5 1':0.5 R:0.5 6:0.5 1':1", "2':1 1':1 7:1 5:1", "1':4", "R:4"]
C1 = "どこまでも/いけるよね/どせいのわっかまで/とばしてく/ごーごーはいうぇいよるへ/くもりぼし/のせてゆく/ちずにないみちへ/ふみだしていこう/いますぐ"
C2 = "どこまでも/いけるよね/よあけのそらまで/とばしてく/ごーごーはいうぇいだよ/いこう/くもりぼし/のせてゆく/ちずにないみちへ/ふみだしていこう/このみちを"
CL = "どこまでも/いけるよね/どせいのわっかまで/とばしてく/ごーごーはいうぇいよるへ/くもりぼし/のせてゆく/ちずにないみちへ/ふみだしていこう/いますぐ/どこまでも/いけるんだあさひのなか/ごーごーはいうぇいへと"
SH = ["1':0.5 R:0.5 1':0.5 R:0.5 5:0.5 6:0.5 1':1", "b7:0.5 R:0.5 b7:0.5 R:0.5 4:0.5 5:0.5 b7:1",
      "6:0.5 R:0.5 6:0.5 R:0.5 4:0.5 2:0.5 4:1", "5:2 R:2",
      "1':0.5 R:0.5 1':0.5 R:0.5 2':0.5 1':0.5 5:1", "b7:0.5 R:0.5 b7:0.5 R:0.5 2':0.5 1':0.5 b7:1",
      "6:0.5 R:0.5 1':0.5 R:0.5 2':1 1':1", "7:2 R:2"]
FL = ["R:2 3:1 5:1", "6:3 R:1", "5:2 3:1 1:1", "2:3 R:1", "4:1 5:1 6:1 1':1", "7:2 5:1 R:1", "6:1 5:1 4:1 6:1", "5:3 R:1",
      "6:1 1':1 3':2", "2':2 1':1 R:1", "6:1 1':1 2':1 3':1", "3':3 R:1", "2':1 1':1 6:1 4:1", "5:2 7:1 R:1", "1':1 2':1 3':2", "2':3 R:1"]
FLV = "ほしが/ちかいね/このよるがね/とまるなら/いいのにな/でもあした/ぼくらはまた/ちらばる"
RE = ["4:1 6:1 1':2", "7:1 5:1 7:1 R:1", "6:1 1':1 3':2", "1':3 R:1", "2':1 1':1 6:1 4:1", "5:2 7:1 R:1", "6:1 1':1 2':1 3':1", "2':2 R:2"]
REV = "なんどでもね/ここから/ちずのそとへ/とびだそう"
LAND = ["5:2 3:2", "2:3 R:1", "1:2 3:1 5:1", "5:3 R:1", "1':2 7:1 5:1", "b7:3 R:1", "6:1 4:1 6:1 1':1", "2':3 R:1",
        "1':0.5 R:0.5 1':0.5 R:0.5 5:0.5 6:0.5 1':1", "b7:0.5 R:0.5 b7:0.5 R:0.5 2':0.5 1':0.5 b7:1", "6:0.5 R:0.5 1':0.5 R:0.5 2':1 1':1", "1':1! R:3"]
LANDV = "あさだ/まぶしい/きっとまた/このみちを/ごごいこうごごいこうおおいえい"
LY = Lyrics(S)
def put(name, key, lines, text, low=True, rng=None):
    bars = S.sc(name)[rng] if rng else S.sc(name); mel = [key.mel(x, oct=4) for x in lines]
    for i, (b, m) in enumerate(zip(bars, mel)): V.bar(b, m, low=low if not callable(low) else low(i))
    LY.flow(bars, mel, text, name)
put("大気圏", K, VERSE, V1)
if VOCAL: put("大気圏2", K, VERSE, V2)
else:
    for i, b in enumerate(S.sc("大気圏2")):
        if i < 8: ORGM.bar(b, K.mel(VERSE[i], oct=4))              # BGM: 2番の前半は、オルガンが歌を受け取る
        else: V.bar(b, K.mel(VERSE[i], oct=4))
put("加速", K, BM, P1); put("加速2", K, BM, P2)
put("輪っか", K, CH1 + CH1b, C1); put("輪っか2", K, CH2 + CH2b, C2)
put("輪っかを抜ける", K2, [x.replace("3':", "2':") for x in CH1 + CH1b] + LASTX, CL)   # 最後のサビ（+2）はテトの高さに収める（3' → 2'）
for name in ("掛け声", "掛け声2"):
    bars = [b for i, b in enumerate(S.sc(name)) if i % 2 == 0]; mel = [K.mel(SH[i], oct=4) for i in range(0, 8, 2)]
    for b, m in zip(bars, mel): V.bar(b, m)
    LY.flow(bars, mel, "ごごいこう/おおいえい/ごごいこう/おおいえ", name)
    for i, b in enumerate(S.sc(name)):
        if i % 2 == 1: ORGM.bar(b, K.mel(SH[i], oct=4))           # 歌とオルガンが言い合う
put("ただよう", K, FL, FLV, low=lambda i: i >= 8)
put("再突入", K, RE, REV)
put("掛け声3", K2, SH, "ごごいこうごごいこうおおいえいえ/ごごいこうごごいこうおおいえい")   # 最後は言い合わずに声をそろえる
put("着陸", K2, LAND, LANDV, low=lambda i: i >= 8)

# 無重力の後半: オルガンのソロ（主旋律の受け渡し）
OS = ["5:0.5 3:0.5 5:0.5 1':0.5 7:1 5:1", "3:0.5 5:0.5 7:0.5 2':0.5 3':1 7:1", "6:0.5 4:0.5 6:0.5 1':0.5 2':1 1':1", "b6:1 4:1 2:1 7,:1",
      "1':0.25 7:0.25 6:0.25 5:0.25 3:0.5 5:0.5 1':2", "3':0.25 2':0.25 1':0.25 7:0.25 5:0.5 7:0.5 3':2", "4':0.5 2':0.5 1':0.5 6:0.5 4:0.5 6:0.5 1':1", "b6:2 5:2"]
for i, b in enumerate(S.sc("無重力")):
    if i >= 8: ORGM.bar(b, K.mel(OS[i - 8], oct=4))

# ================= リードギター =================
RIFF = ["1':0.5 5:0.5 1':0.5 3':0.5 2':0.5 1':0.5 5:0.5 3:0.5", "3':0.5 7:0.5 3':0.5 5:0.5 3':0.5 2':0.5 1':0.5 7:0.5",
        "4':0.5 1':0.5 6:0.5 4:0.5 6:0.5 1':0.5 2':0.5 4':0.5", "4':0.75 1':0.25 b6:0.5 4:0.5 b6:0.5 1':0.5 5:1"]
for name in ("発射", "無重力"):
    for i, b in enumerate(S.sc(name)):
        if name == "無重力" and i >= 8: break
        LG.bar(b, K.mel(RIFF[i % 4] if not (name == "発射" and i >= 8) else seq_up(RIFF[i % 4], K, 2), oct=3))
SOLO = ["5:0.5 1':0.5 3':0.5 5':0.5 3':1 1':1", "3':0.5 5':0.5 7':0.5 5':0.5 3':2", "6':1 4':0.5 1':0.5 6:1 1':1", "4':0.75 3':0.25 b3':0.5 1':0.5 7:2",
        "1':0.25 2':0.25 3':0.25 5':0.25 3':0.25 2':0.25 1':0.5 5:0.5 1':0.5 3':1", "5':1.5 3':0.5 5':1 7':1", "1'':2 6':1 4':1", "b6':1 4':1 1':1 7:1",
        "5':0.5 5':0.5 6':0.5 5':0.5 3':0.5 5':0.5 1'':1", "7':0.5 7':0.5 1'':0.5 7':0.5 5':0.5 3':0.5 5':1", "6':0.5 1'':0.5 6':0.5 4':0.5 1':0.5 4':0.5 6':1", "4':2 b3':1 1':1",
        "1'':0.5 7':0.25 1'':0.25 7':0.5 5':0.5 5':1 3':1", "3':1 5':1 7':1 1'':1", "6':1 1'':1 6':1 5':1", "5':4"]
# 2026-10-26 人間（08 で）「ギターの音は聞きにくい」: 08 と同じ 32分の連打（トレモロ・1音 44ms）がソロ13小節目にあったので、09 も歌えるフレーズに
for i, b in enumerate(S.sc("ギターソロ")): LGS.bar(b, K.mel(SOLO[i], oct=3))

def mbass(b, style):
    """表に出る歌うベース（E1〜D3）。r＝根音、c1・c2＝根音の上の和音の音、o＝オクターブ、a＝次の根音へ寄る音"""
    ch = S.chords[b]; r = low(ch, "E1")
    nx = low(S.chords[b + 1], "E1") if b + 1 < S.nb else r
    if nx - r > 6: nx -= 12
    if r - nx > 6: nx += 12
    up = tones(ch, nm(r + 1), nm(r + 12))
    c1 = up[0] if up else r + 4; c2 = up[1] if len(up) > 1 else r + 7
    o = r + 12
    a = nx - 1 if nx > r else (nx + 1 if nx < r else nx + 2)
    w = nx - 2 if nx > r else nx + 2
    P_ = {"walk": [(r, 1, "!"), (c2, 0.5, ""), (o, 0.5, ""), (c1 + 12, 1, ""), (w, 0.5, ""), (a, 0.5, "")],
          "climb": [(r, 0.5, "!"), (r, 0.5, ""), (c1, 0.5, ""), (c2, 0.5, ""), (o, 1, "!"), (c2, 0.5, ""), (a, 0.5, "")],
          "drive": [(r, 0.5, "!"), (r, 0.5, ""), (o, 0.5, ""), (r, 0.5, ""), (c2, 0.5, "!"), (o, 0.5, ""), (c1 + 12, 0.5, ""), (a, 0.5, "")],
          "run": [(r, 0.5, "!"), (c1, 0.5, ""), (c2, 0.5, ""), (o, 0.5, ""), (c2 + 12, 0.5, ""), (o, 0.5, ""), (w, 0.5, ""), (a, 0.5, "")],
          "ride": [(r, 1.5, "!"), (c2, 0.5, ""), (o, 1, ""), (a, 1, "")]}[style]
    fix = lambda m: m + 12 if m < 30 else (m - 12 if m > 52 else m)   # 書き出しで 7半音下がるので、B0 より下に行かないように
    return " ".join(f"{nm(fix(m))}:{d}{acc}" for m, d, acc in P_)


# ================= 伴奏 =================
for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    ch = S.chords[b]
    pw = power(ch, "E2")
    v = voice(ch, 64, 3)
    # 歪みのギター（パワーコード。ポップパンクの8分）
    gpat = None
    # ニューメタルの壁: Aメロの前半はギターを休み（シンセ・ピアノ・ベース・ドラムだけ）、後半から重い和音。サビは大きくのばす壁
    if n in ("発射", "無重力"): gpat = "X:1.5! X:1 X:1.5" if not (n == "無重力" and i >= 8) else None
    elif n.startswith("大気圏"): gpat = None if i < 8 else "X:2! X:2"
    elif n.startswith("加速"): gpat = "X:4!" if i < 7 else "X:2! R:2"
    elif n in ("輪っか", "輪っかを抜ける"): gpat = "X:1.5! X:1 X:1.5"
    elif n == "輪っか2": gpat = "X:4!"                                   # Half feel: のばす壁
    elif n.startswith("掛け声") or (n == "着陸" and i >= 8): gpat = "X:1.5! X:1 X:1.5"
    elif n == "ただよう" and i >= 8: gpat = "X:4!"
    elif n == "ギターソロ": gpat = "X:2! X:2"
    elif n == "再突入": gpat = "X:4!" if i < 4 else "X:2! X:2"
    elif n == "着陸": gpat = "X:1.5! X:1 X:1.5"
    if n == "着陸" and i == L - 1: gpat = "X:1! R:3"
    if gpat:
        for j in range(2):
            GL[j].bar(b, gpat.replace("X", nm(pw[j])))
            GR[j].bar(b, gpat.replace("X", nm([pw[0], pw[2]][j])))
    # オルガン（裏のスタブ・のばす和音）
    opat = None
    if n.startswith("大気圏"): opat = "R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5 R:0.5 X:0.5" if i >= 4 else None
    elif n.startswith("加速"): opat = "X:4" if i < 7 else "X:2 R:2"
    elif n in ("輪っか", "輪っか2", "輪っかを抜ける"): opat = "X:2 X:2" if n != "輪っか2" else "X:4"
    elif n == "無重力": opat = "X:4" if i < 8 else None
    elif n == "ただよう": opat = "X:4"
    elif n == "再突入": opat = "X:4"
    if n.startswith("大気圏"): opat = "X:4"                        # Aメロは暗いパッドをのばす
    if opat:
        if n.startswith("大気圏2") and i < 8 and not VOCAL: opat = None     # BGM: ピアノが歌を受け取る所は和音を休む
    if opat:
        for j in range(3): ORG[j].bar(b, opat.replace("X", nm(v[j])))
    # ベース（根音に沿わせる。サビは8分のオクターブ）
    r = low(ch, "E1")
    if n == "秒読み": BASS.bar(b, f"{nm(r)}:4" if i == 3 else "R:4")
    elif n in ("発射", "無重力"): BASS.bar(b, mbass(b, "run" if i % 2 else "drive"))
    elif n.startswith("大気圏"): BASS.bar(b, mbass(b, "walk" if i % 2 == 0 else "climb"))
    elif n.startswith("加速"): BASS.bar(b, bass_line(S, b, "root8") if i < 7 else f"{nm(r)}:2 R:2")
    elif n in ("輪っか", "輪っかを抜ける"): BASS.bar(b, mbass(b, "drive" if i % 4 != 3 else "run"))
    elif n == "輪っか2": BASS.bar(b, mbass(b, "ride"))
    elif n.startswith("掛け声"): BASS.bar(b, f"{nm(r)}:0.5 R:0.5 {nm(r)}:0.5 R:0.5 {nm(r)}:0.5 {nm(r)}:0.5 {nm(r + 12)}:1")
    elif n == "ただよう": BASS.bar(b, bass_line(S, b, "long") if i < 8 else bass_line(S, b, "half"))
    elif n == "ギターソロ": BASS.bar(b, mbass(b, "climb" if i % 2 else "walk"))
    elif n == "再突入": BASS.bar(b, bass_line(S, b, "long" if i < 4 else "root8"))
    elif n == "着陸": BASS.bar(b, bass_line(S, b, "root8") if i < L - 1 else f"{nm(r)}:1 R:3")
    # スクラッチ風の飾り（ピックスクレイプの短い音を、区切りの手前と掛け声の裏に）
    if n.startswith("掛け声") and i % 2 == 1: CLAP.bar(b, "R:2.5 D2:0.25 D#2:0.25 R:0.5 D2:0.5")
    elif n.startswith("大気圏") and i % 4 == 3: CLAP.bar(b, "R:3 D2:0.25 R:0.25 D#2:0.5")
    elif n == "秒読み" and i == 3: CLAP.bar(b, "R:2 C2:2")

riser(FX, S.sc("輪っか")[0], 4, "C4"); riser(FX, S.sc("輪っかを抜ける")[0], 16, "D4")
FX.bar(S.sc("ただよう")[0], "G4:4")                         # 宇宙に出た「ドーン」（サブドロップ）
cym_swell(CYM, S.sc("発射")[0], 2, "C4"); cym_swell(CYM, S.sc("無重力")[0], 2, "C4"); cym_swell(CYM, S.sc("輪っか2")[0], 2, "C4"); cym_swell(CYM, S.sc("ギターソロ")[0], 4, "E4")

# ================= ドラム =================
def ride8(b, first="C2"):
    D.cym(b, f"{first}:0.5 " + "D2:0.5 " * 7); D.H[b] = "." * 16


for b in range(S.nb):
    n, i, L, k = S.scene_of(b)
    last = i == L - 1
    if n == "秒読み":
        D.set(b, "." * 16, "." * 16, "x.......x......." if i < 3 else "x.x.x.x.x.x.x.x.")
        if i == 3: D.set(b, "X.......X.X.X.X.", "........XXXXXXXX", "." * 16)
    elif n in ("発射", "無重力"):
        vgroove(D, b, "punk" if n == "発射" else "beat8", ghosts=0.3, seed=b)
        if i == 0: crash(D, b)
        if n == "無重力" and i >= 4: ride8(b, "C2" if i == 4 else "D2")
        if last: put_fill(D, b, "tomdown")
    elif n.startswith("大気圏"):
        # ヒップホップ寄りの Half feel（キックがはねる・スネアは3拍目）。後半は重く
        vgroove(D, b, "halfdrive" if i >= 8 else "half", ghosts=0.45, seed=b, k="X.....X...X..X.." if i < 8 else None)
        if i == 0: crash(D, b)
        if i == 7: put_fill(D, b, "small")
        if last: put_fill(D, b, "snare16")
    elif n.startswith("加速"):
        vgroove(D, b, "half" if i < 4 else "vrock2", ghosts=0.3, seed=b)
        if i == 4: crash(D, b, "G2")
        if i == 6: put_fill(D, b, "build")
        if last: halt(D, b, 1); D.cym(b, "C2:1")
    elif n == "輪っか":                            # 1回目: 重い8ビート
        vgroove(D, b, "vrock2", ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i == 0 else "G2")
        if i % 8 == 7: put_fill(D, b, "snare16" if i == 7 else "tomdown")
    elif n == "輪っか2":                           # 2回目: Half feel（サビごとにリズムを入れかえる）
        vgroove(D, b, "halfdrive", ghosts=0.45, seed=b)
        if 4 <= i < 12: D.cym(b, ("C2:1 " if i == 4 else "D2:1 ") + "D2:1 D2:1 D2:1"); D.H[b] = "." * 16
        if i % 8 == 0: crash(D, b, "C2" if i == 0 else "B2")
        if i % 8 == 7: put_fill(D, b, "tomtrip" if i == 7 else "tomdown")
    elif n.startswith("掛け声"):
        vgroove(D, b, "punk", ghosts=0.2, seed=b, s="....X.......X.X.")
        if i == 0: crash(D, b)
        if last and n == "掛け声": put_fill(D, b, "small")
    elif n == "ただよう":
        if i < 8: D.set(b, "." * 16, "." * 16, "." * 16 if i < 4 else "x...x...x...x...")
        else:
            vgroove(D, b, "half", ghosts=0.4, seed=b, h="x...x...x...x...")
            if not last: D.cym(b, ("C2:1 " if i == 8 else "D2:1 ") + "D2:1 D2:1 D2:1"); D.H[b] = "." * 16
        if last: put_fill(D, b, "lift")
    elif n == "ギターソロ":
        vgroove(D, b, "vrock2", ghosts=0.35, seed=b)
        if i % 8 == 0: crash(D, b)
        if i % 4 == 3: put_fill(D, b, "small" if i % 8 == 3 else "tomdown")
    elif n == "再突入":
        D.set(b, "X.......X.......", "........X.......", "x.x.x.x.x.x.x.x.")
        if i >= 4: D.set(b, "X...X...X...X...", "....X.......X...", "xxxxxxxxxxxxxxxx")
        if i == 6: put_fill(D, b, "build")
        if last: D.set(b, "X...X...X.......", "xxxxXXXXXXXX....", "." * 16)
    elif n == "輪っかを抜ける":                     # 最後: 重い4分のキック（壁）
        vgroove(D, b, "vrock", ghosts=0.3, seed=b)
        if i % 8 == 0: crash(D, b, "C2" if i % 16 == 0 else "G2")
        if 8 <= i < 16: ride8(b, "D2")
        if i % 8 == 7 and not last: put_fill(D, b, "snare16" if i % 16 == 7 else "tomdown")
        if last: put_fill(D, b, "snare16")
    elif n == "着陸":
        vgroove(D, b, "punk", ghosts=0.3, seed=b)
        if i == 0: crash(D, b)
        if last: D.set(b, "X" + "." * 15, "X" + "." * 15, "." * 16)

# 止め・宇宙の無音2拍・1拍の完全な無音・急停止
SIL.add(S.sc("加速")[-1], 1, 4); SIL.add(S.sc("加速2")[-1], 1, 4)
SIL.add(S.sc("掛け声2")[-1], 2, 4)                 # 宇宙の無音（2拍）
SIL.add(S.sc("再突入")[-1], 3, 4)                  # 1拍の完全な無音（転調の直前）
SIL.add(S.sc("着陸")[-1], 1, 4)                    # 急に止める
SIL.apply()

S.fade_out = 0
S.desc = ("仮: ボカロ曲インスト25曲（作り直し）の09。ラップロック／ニューメタル（重い歪みの壁・暗いシンセ・ピアノ・歌うベース）。D長調・208（最後のサビは E長調 +2）。免許を取りたての友だちと夜中のハイウェイを走り、将来の不安を笑い飛ばす。"
          "秒読みで始まり、8分で語る Aメロ、止めのある Bメロ、休みで区切る呼びかけのサビ、歌とオルガンの掛け声、Half feel の2サビ、星が近い Cメロ、ギターソロ、+2 の最後のサビ、夜明けに急に止める。自作")
S.no_depth = True
teto(S, LY, V, transpose=-7, special={"輪っかを抜ける": 0.55, "ただよう": -0.45, "掛け声": 0.3, "掛け声2": 0.3, "掛け声3": 0.5, "着陸": -0.1})
